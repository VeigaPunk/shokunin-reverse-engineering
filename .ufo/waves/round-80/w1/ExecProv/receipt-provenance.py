#!/usr/bin/env python3
"""Round-80 receipt provenance: every landing receipt's instrument digest names a committed blob.

Population (revision-pinned): `.ufo/waves/round-<N>/l1/scores/*.json` for
N in [--from-round (60), --to-round (79)] under `--root`, any path containing
`/attacks/` excluded, read from git at `--rev` (`git show <commit>:<path>` — the
working tree is never the population source), keeping only JSON objects that
carry an `instrument.path` string and a 64-hex `instrument.sha256` (either hex
case; the digest is compared case-insensitively).  A receipt that does not exist
at `--rev` is skipped.

Provenance: the digest is committed iff it equals the sha256 of
`git show <tip>:<instrument.path>` or of `git show <r>:<instrument.path>` for
some committed revision `r` of that path (`git rev-list --all -- <path>`).  A
digest that matches only the working tree is NOT committed.  A symbolic
revision (`@HEAD@`, `main`, `HEAD`) is never treated as a committed revision:
`--rev` must be a hexadecimal commit id (a symbolic-full-name resolves to a ref
means refusal), and a receipt's declared `rev`/`record.rev` is recorded, never
used as an anchor.  An `instrument.path` that is absolute or carries a `..`
segment is a named defect and is never passed to git.

Classification: `expected_controls` is the declared basename list
`["prov-forged-instrument.json"]`; a flagged receipt whose basename is in it
counts as `expected_control_flags`, every other flag counts as `unexpected`.

Modes:
    --rev <commit>          sweep and write the receipt (the default mode)
    --selftest              fixture-repo unit cases, printed one JSON line each
    --validate <receipt>    re-derive every count from `rows` and check them

Exit: 0 no unexpected flag; 1 one or more unexpected flags; 2 could-not-evaluate.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import time

ROUND = 80
INSTRUMENT = "tools/round-80/receipt-provenance.py"
POPULATION_TEMPLATE = ".ufo/waves/round-{round}/l1/scores"
CONTROLS = ("prov-forged-instrument.json",)
PREDICATE = (
    "R80-C2 is verified iff `python3 -I -B tools/round-80/receipt-provenance.py "
    "--root . --rev <measured> --from-round 60 --to-round 79 --json-out <receipt>` "
    "exits 0 with `receipts 34`, `flagged 1`, `expected_control_flags 1`, "
    "`unexpected 0` and a defect-free `--validate`, while at base `16dfa009` the "
    "same command exits 1 with `flagged 2`, `expected_control_flags 1`, "
    "`unexpected 1` and the unexpected flag names "
    "`.ufo/waves/round-79/l1/scores/c2-at-landing.json`."
)

RE_HEX64 = re.compile(r"[0-9a-f]{64}")
RE_HEX64_ANY = re.compile(r"[0-9a-fA-F]{64}")
RE_ABBREV = re.compile(r"[0-9a-f]{4,40}")
RE_FULL = re.compile(r"[0-9a-f]{40}")
VERDICTS = ("committed", "uncommitted", "defect")

# Git accounting for the receipt: one counter per invoked subcommand.
GIT_CALLS = {"rev_parse": 0, "show": 0, "rev_list": 0, "cat_file": 0, "other": 0}

# (tip, instrument.path) -> [(revision, sha256 of the blob], tip first.
INDEX_CACHE: dict[tuple[str, str], list[tuple[str, str]]] = {}


class Unevaluable(Exception):
    """Exit-2 class: the population or the revision cannot be read."""


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def self_digest() -> str:
    return sha256_bytes(pathlib.Path(__file__).read_bytes())


def _git_kind(args: list[str]) -> str:
    verb = args[0] if args else ""
    return {"rev-parse": "rev_parse", "show": "show", "rev-list": "rev_list",
            "cat-file": "cat_file"}.get(verb, "other")


def git(root: str, args: list[str], stdin: bytes | None = None) -> subprocess.CompletedProcess:
    """One git process, counted; never called with an unvetted instrument path."""
    GIT_CALLS[_git_kind(args)] += 1
    return subprocess.run(["git", "-C", root, *args], input=stdin,
                          capture_output=True)


def resolve_commit(root: str, rev: str) -> str:
    """Resolve `rev` to one literal commit; a symbolic revision is refused."""
    if not isinstance(rev, str) or not RE_ABBREV.fullmatch(rev):
        raise Unevaluable(
            f"rev {rev!r} is not a hexadecimal commit id; a symbolic revision "
            "is never treated as a committed revision")
    symbolic = git(root, ["rev-parse", "--symbolic-full-name", rev])
    name = symbolic.stdout.decode("utf-8", "replace").strip()
    if symbolic.returncode == 0 and name:
        raise Unevaluable(
            f"rev {rev!r} names the symbolic ref {name}; a symbolic revision is "
            "never treated as a committed revision")
    verified = git(root, ["rev-parse", "--verify", f"{rev}^{{commit}}"])
    if verified.returncode != 0:
        raise Unevaluable(f"rev {rev!r} does not name a commit")
    resolved = verified.stdout.decode("utf-8", "replace").strip()
    if not RE_FULL.fullmatch(resolved):
        raise Unevaluable(f"rev {rev!r} resolved to {resolved!r}, not a 40-hex commit")
    return resolved


def path_defect(path: str) -> str:
    """A named defect for an instrument path that must never reach git."""
    if not path:
        return "instrument.path is empty"
    if "\n" in path or "\r" in path or "\0" in path:
        return f"instrument.path {path!r} carries a control character"
    if path.startswith("/"):
        return f"instrument.path {path!r} is absolute"
    if ".." in pathlib.PurePosixPath(path).parts:
        return f"instrument.path {path!r} contains a '..' segment"
    return ""


def parse_batch(data: bytes, expressions: list[str]) -> dict[str, bytes]:
    """Bodies from a `git cat-file --batch` stream, keyed by the expression order."""
    bodies: dict[str, bytes] = {}
    pos = 0
    for expression in expressions:
        newline = data.find(b"\n", pos)
        if newline < 0:
            raise Unevaluable("git cat-file --batch output ended early")
        header = data[pos:newline].decode("utf-8", "replace")
        fields = header.split()
        if len(fields) == 3 and fields[1] in {"blob", "tree", "commit", "tag"}:
            size = int(fields[2])
            body = data[newline + 1:newline + 1 + size]
            if len(body) != size:
                raise Unevaluable("git cat-file --batch body is short")
            bodies[expression] = body
            pos = newline + 1 + size + 1
        else:
            # "<expression> missing" (or an ambiguous expression): no body.
            pos = newline + 1
    return bodies


def digest_index(root: str, path: str, tip: str) -> list[tuple[str, str]]:
    """[(revision, sha256 of the blob)] for the tip and every committed revision."""
    cached = INDEX_CACHE.get((tip, path))
    if cached is not None:
        return cached
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    at_tip = git(root, ["show", f"{tip}:{path}"])
    if at_tip.returncode == 0:
        pairs.append((tip, sha256_bytes(at_tip.stdout)))
        seen.add(tip)
    listed = git(root, ["rev-list", "--all", "--", path])
    if listed.returncode != 0:
        raise Unevaluable(f"git rev-list could not list the revisions of {path!r}")
    revisions = [rev for rev in listed.stdout.decode("ascii", "replace").split()
                 if RE_FULL.fullmatch(rev) and rev not in seen]
    if revisions:
        expressions = [f"{rev}:{path}" for rev in revisions]
        batch = git(root, ["cat-file", "--batch"],
                    stdin=("\n".join(expressions) + "\n").encode("utf-8"))
        if batch.returncode != 0:
            raise Unevaluable(f"git cat-file could not read the blobs of {path!r}")
        bodies = parse_batch(batch.stdout, expressions)
        for revision, expression in zip(revisions, expressions):
            body = bodies.get(expression)
            if body is not None:
                pairs.append((revision, sha256_bytes(body)))
    INDEX_CACHE[(tip, path)] = pairs
    return pairs


def discover(root: str, from_round: int, to_round: int) -> list[str]:
    """Repo-relative `l1/scores/*.json` candidates; `/attacks/` never enters."""
    root_abs = os.path.abspath(root)
    found: list[str] = []
    for number in range(from_round, to_round + 1):
        scores = os.path.join(root_abs, POPULATION_TEMPLATE.format(round=number))
        try:
            names = sorted(os.listdir(scores))
        except OSError:
            continue
        for name in names:
            if not name.endswith(".json"):
                continue
            full = os.path.join(scores, name)
            if not os.path.isfile(full):
                continue
            relative = os.path.relpath(full, root_abs).replace(os.sep, "/")
            if "/attacks/" in "/" + relative:
                continue
            found.append(relative)
    return found


def classify(rows: list[dict]) -> tuple[int, int, int, int]:
    """(receipts, flagged, expected_control_flags, unexpected) from the rows."""
    receipts = len(rows)
    flagged_rows = [row for row in rows if row.get("verdict") != "committed"]
    expected = [row for row in flagged_rows
                if os.path.basename(str(row.get("path", ""))) in CONTROLS]
    return receipts, len(flagged_rows), len(expected), len(flagged_rows) - len(expected)


def sweep(root: str, rev: str, from_round: int = 60, to_round: int = 79) -> dict:
    """The provenance battery; writes nothing but git reads."""
    INDEX_CACHE.clear()
    for key in GIT_CALLS:
        GIT_CALLS[key] = 0
    started = time.monotonic()
    commit = resolve_commit(root, rev)
    rows: list[dict] = []
    for relative in discover(root, from_round, to_round):
        blob = git(root, ["show", f"{commit}:{relative}"])
        if blob.returncode != 0:
            continue  # the receipt does not exist at --rev
        try:
            data = json.loads(blob.stdout)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise Unevaluable(f"{relative} at {commit} is not readable JSON ({exc})")
        if not isinstance(data, dict):
            continue
        instrument = data.get("instrument")
        if not isinstance(instrument, dict):
            continue
        path = instrument.get("path")
        digest = instrument.get("sha256")
        if not isinstance(path, str) or not isinstance(digest, str):
            continue
        if not RE_HEX64_ANY.fullmatch(digest):
            continue
        declared = ""
        record = data.get("record")
        if isinstance(record, dict) and isinstance(record.get("rev"), str):
            declared = record["rev"]
        elif isinstance(data.get("rev"), str):
            declared = data["rev"]
        row = {"path": relative, "instrument": path, "digest": digest,
               "verdict": "uncommitted", "matched_rev": "", "defect": "",
               "declared_rev": declared, "declared_rev_literal": bool(RE_FULL.fullmatch(declared))}
        named = path_defect(path)
        if named:
            row["verdict"] = "defect"
            row["defect"] = named
            rows.append(row)
            continue
        for candidate_rev, candidate_digest in digest_index(root, path, commit):
            if candidate_digest == digest.lower():
                row["verdict"] = "committed"
                row["matched_rev"] = candidate_rev
                break
        rows.append(row)
    rows.sort(key=lambda row: row["path"])
    receipts, flagged, expected, unexpected = classify(rows)
    receipt = {
        "schema": "kaidoku-r80-receipt-provenance-v1",
        "round": ROUND,
        "predicate": PREDICATE,
        "checked_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "instrument": {"path": INSTRUMENT, "sha256": self_digest()},
        "rev": commit,
        "rev_arg": rev,
        "population": {"from_round": from_round, "to_round": to_round,
                       "scores_glob": POPULATION_TEMPLATE.format(round="<N>") + "/*.json",
                       "attacks_excluded": True},
        "controls": list(CONTROLS),
        "receipts": receipts,
        "flagged": flagged,
        "expected_control_flags": expected,
        "unexpected": unexpected,
        "rows": rows,
        "git_calls": dict(GIT_CALLS),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "ok": unexpected == 0,
    }
    return receipt


def validate_receipt(receipt: dict) -> dict:
    """Re-derive every count from `rows`; returns the defects and the counts."""
    defects: list[str] = []
    if not isinstance(receipt, dict):
        return {"defects": ["receipt is not a JSON object"], "receipts": 0,
                "flagged": 0, "expected_control_flags": 0, "unexpected": 0}
    rows = receipt.get("rows")
    if not isinstance(rows, list):
        defects.append("rows is not a list")
        rows = []
    controls = receipt.get("controls")
    if not (isinstance(controls, list)
            and all(isinstance(item, str) and "/" not in item for item in controls)):
        defects.append("controls is not a list of basenames")
        controls = []
    if len(controls) != len(set(controls)):
        defects.append("duplicate control basename")
    seen_paths: set[str] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            defects.append(f"row {index} is not an object")
            continue
        label = str(row.get("path") or f"row {index}")
        for key in ("path", "instrument", "digest", "verdict", "matched_rev"):
            if key not in row:
                defects.append(f"{label}: {key} is absent")
        path = row.get("path")
        instrument = row.get("instrument")
        digest = row.get("digest")
        verdict = row.get("verdict")
        matched = row.get("matched_rev")
        if not isinstance(path, str) or not path:
            defects.append(f"{label}: path is not a non-empty string")
        elif path in seen_paths:
            defects.append(f"{label}: duplicate row path")
        else:
            seen_paths.add(path)
        if not isinstance(instrument, str):
            defects.append(f"{label}: instrument is not a string")
            instrument = ""
        if not isinstance(digest, str) or not RE_HEX64_ANY.fullmatch(digest):
            defects.append(f"{label}: digest is not a 64-hex sha256")
        if verdict not in VERDICTS:
            defects.append(f"{label}: verdict {verdict!r} is not one of {VERDICTS}")
            continue
        named = path_defect(instrument)
        if verdict == "committed":
            if not isinstance(matched, str) or not RE_FULL.fullmatch(matched):
                defects.append(f"{label}: committed without a matched 40-hex revision")
            if named:
                defects.append(f"{label}: committed with an escaping instrument path")
        elif verdict == "defect":
            if not isinstance(row.get("defect"), str) or not row.get("defect"):
                defects.append(f"{label}: defect verdict without a named defect")
            if not named:
                defects.append(f"{label}: defect verdict on a clean instrument path")
        else:
            if named:
                defects.append(f"{label}: uncommitted with an escaping instrument path")
        if verdict != "committed" and matched not in ("", None):
            defects.append(f"{label}: a flagged row carries matched_rev {matched!r}")
        if verdict != "defect" and row.get("defect"):
            defects.append(f"{label}: defect text on a non-defect row")
        if "declared_rev" in row:
            declared = row.get("declared_rev")
            if not isinstance(declared, str):
                defects.append(f"{label}: declared_rev is not a string")
            elif "declared_rev_literal" in row:
                if row.get("declared_rev_literal") is not bool(RE_FULL.fullmatch(declared)):
                    defects.append(f"{label}: declared_rev_literal does not re-derive")
    receipts, flagged, expected, unexpected = classify(
        [row for row in rows if isinstance(row, dict)])
    if receipt.get("receipts") != receipts:
        defects.append("receipts does not re-derive from rows")
    if receipt.get("flagged") != flagged:
        defects.append("flagged does not re-derive from rows")
    if receipt.get("expected_control_flags") != expected:
        defects.append("expected_control_flags does not re-derive from rows")
    if receipt.get("unexpected") != unexpected:
        defects.append("unexpected is not flagged minus expected_control_flags")
    if receipt.get("ok") is not (unexpected == 0):
        defects.append("ok does not re-derive from unexpected")
    revision = receipt.get("rev")
    if not isinstance(revision, str) or not RE_FULL.fullmatch(revision):
        defects.append("rev is not a 40-hex commit")
    if not receipt.get("checked_at"):
        defects.append("checked_at is absent")
    instrument_block = receipt.get("instrument")
    if not isinstance(instrument_block, dict):
        defects.append("instrument is not an object")
    else:
        if instrument_block.get("path") != INSTRUMENT:
            defects.append("instrument.path is not the landing path")
        if instrument_block.get("sha256") != self_digest():
            defects.append("instrument sha256 is not this file's digest")
    if receipt.get("round") != ROUND:
        defects.append("round is not 80")
    return {"defects": defects, "receipts": receipts, "flagged": flagged,
            "expected_control_flags": expected, "unexpected": unexpected}


# ---------------------------------------------------------------------------
# Selftest: one throwaway git fixture repo under TMPDIR (never a fixed path).


def _fixture_digest(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def _build_fixture(repo: str) -> dict:
    def run(*args: str) -> subprocess.CompletedProcess:
        return subprocess.run(["git", "-C", repo, *args], capture_output=True,
                              check=True)

    def write(relative: str, text: str) -> None:
        target = os.path.join(repo, relative)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as handle:
            handle.write(text)

    def commit(message: str) -> str:
        run("add", "-A")
        run("commit", "-qm", message)
        return run("rev-parse", "HEAD").stdout.decode().strip()

    run("init", "-q", "-b", "main")
    run("config", "user.name", "r80-fixture")
    run("config", "user.email", "r80@example.invalid")
    run("config", "commit.gpgsign", "false")

    v1, v2, v3 = "version one\n", "version two tip\n", "version three working tree\n"
    write("inst.py", v1)
    c1 = commit("fixture instrument v1")
    write("inst.py", v2)
    c2 = commit("fixture instrument v2")

    scores = ".ufo/waves/round-60/l1/scores"
    write(f"{scores}/tip.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": _fixture_digest(v2)}}))
    write(f"{scores}/upper.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": _fixture_digest(v2).upper()}}))
    write(f"{scores}/history.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": _fixture_digest(v1)}}))
    write(f"{scores}/uncommitted.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": "f" * 64}}))
    write(f"{scores}/working-tree.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": _fixture_digest(v3)}}))
    write(f"{scores}/prov-forged-instrument.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": "e" * 64}}))
    write(f"{scores}/no-instrument.json", json.dumps({"note": "no instrument block"}))
    write(f"{scores}/bad-digest.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": "not-a-digest"}}))
    write(f"{scores}/attacks/forged.json", json.dumps(
        {"instrument": {"path": "inst.py", "sha256": "f" * 64}}))
    write(f"{scores}/escape.json", json.dumps(
        {"instrument": {"path": "../outside.txt", "sha256": "f" * 64}}))
    write(f"{scores}/absolute.json", json.dumps(
        {"instrument": {"path": "/etc/passwd", "sha256": "f" * 64}}))
    tip = commit("fixture receipts")
    write("inst.py", v3)  # working-tree-only copy: never committed, never an anchor
    return {"repo": repo, "c1": c1, "c2": c2, "tip": tip,
            "v1": _fixture_digest(v1), "v2": _fixture_digest(v2),
            "v3": _fixture_digest(v3)}


def _raises(action) -> bool:
    try:
        action()
    except Unevaluable:
        return True
    return False


def selftest() -> int:
    cases: list[dict] = []

    def case(name: str, got, want) -> None:
        cases.append({"case": name, "got": got, "want": want, "pass": got == want})

    scratch = tempfile.mkdtemp(prefix="r80-receipt-provenance-")
    try:
        repo = os.path.join(scratch, "fixture")
        os.makedirs(repo)
        fixture = _build_fixture(repo)
        full = subprocess.run(["git", "-C", repo, "rev-parse", "HEAD"],
                              capture_output=True, check=True).stdout.decode().strip()
        case("green-fixture-toplevel",
             os.path.realpath(subprocess.run(
                 ["git", "-C", repo, "rev-parse", "--show-toplevel"],
                 capture_output=True, check=True).stdout.decode().strip()),
             os.path.realpath(repo))

        # Sweep with a spy on the module-level git so an escaping path is visible.
        recorded: list[tuple[str, ...]] = []
        real_git = globals()["git"]

        def spy(root: str, args: list[str], stdin: bytes | None = None):
            recorded.append(tuple(args))
            return real_git(root, args, stdin)

        globals()["git"] = spy
        try:
            result = sweep(repo, full, 60, 60)
        finally:
            globals()["git"] = real_git

        rows = {row["path"]: row for row in result["rows"]}
        prefix = ".ufo/waves/round-60/l1/scores/"

        case("green-tip-digest",
             (rows[prefix + "tip.json"]["verdict"], rows[prefix + "tip.json"]["matched_rev"]),
             ("committed", fixture["tip"]))
        case("green-history-digest",
             (rows[prefix + "history.json"]["verdict"], rows[prefix + "history.json"]["matched_rev"]),
             ("committed", fixture["c1"]))
        case("green-uppercase-digest",
             (rows[prefix + "upper.json"]["verdict"], rows[prefix + "upper.json"]["matched_rev"]),
             ("committed", fixture["tip"]))
        case("red-uncommitted-digest",
             rows[prefix + "uncommitted.json"]["verdict"], "uncommitted")
        case("red-working-tree-only",
             rows[prefix + "working-tree.json"]["verdict"], "uncommitted")
        case("red-attacks-excluded",
             [path for path in rows if "/attacks/" in path], [])
        case("red-no-instrument-skipped",
             [name for name in ("no-instrument.json", "bad-digest.json") if prefix + name in rows],
             [])
        case("green-expected-control",
             (result["expected_control_flags"], result["flagged"], result["unexpected"],
              result["receipts"]),
             (1, 5, 4, 8))
        escape = rows[prefix + "escape.json"]
        case("red-path-escape",
             (escape["verdict"], ".." in escape["defect"]), ("defect", True))
        absolute = rows[prefix + "absolute.json"]
        case("red-absolute-path",
             (absolute["verdict"], "absolute" in absolute["defect"]), ("defect", True))
        case("red-no-git-with-escaping-path",
             any(".." in argument for args in recorded for argument in args), False)
        case("green-path-defect-clean", path_defect("tools/round-80/x.py"), "")
        case("red-symbolic-rev",
             [_raises(lambda: resolve_commit(repo, name))
              for name in ("HEAD", "main", "@HEAD@")], [True, True, True])
        case("green-abbreviated-rev", resolve_commit(repo, full[:8]), full)
        case("green-validate-consistent",
             validate_receipt(json.loads(json.dumps(result)))["defects"], [])
        wrong_count = json.loads(json.dumps(result))
        wrong_count["unexpected"] = 0
        case("red-validate-unexpected-mismatch",
             validate_receipt(wrong_count)["defects"] != [], True)
        wrong_receipts = json.loads(json.dumps(result))
        wrong_receipts["receipts"] = 99
        case("red-validate-receipts",
             validate_receipt(wrong_receipts)["defects"] != [], True)
        wrong_digest = json.loads(json.dumps(result))
        wrong_digest["instrument"]["sha256"] = "0" * 64
        case("red-validate-self-digest",
             any("instrument sha256" in defect
                 for defect in validate_receipt(wrong_digest)["defects"]), True)
        wrong_row = json.loads(json.dumps(result))
        for row in wrong_row["rows"]:
            if row["path"].endswith("tip.json"):
                row["matched_rev"] = ""
        case("red-validate-committed-without-rev",
             validate_receipt(wrong_row)["defects"] != [], True)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)

    failures = [entry for entry in cases if not entry["pass"]]
    for entry in cases:
        print(json.dumps(entry, sort_keys=True))
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=".")
    parser.add_argument("--rev", help="literal commit to measure (never symbolic)")
    parser.add_argument("--from-round", type=int, default=60)
    parser.add_argument("--to-round", type=int, default=79)
    parser.add_argument("--json-out")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--validate", metavar="RECEIPT")
    args = parser.parse_args(argv)

    if args.selftest:
        return selftest()

    if args.validate:
        try:
            receipt = json.loads(
                pathlib.Path(args.validate).read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(json.dumps({"ok": False,
                              "unevaluable": f"cannot read receipt {args.validate}: {exc}"}))
            return 2
        result = validate_receipt(receipt)
        print(json.dumps(result, sort_keys=True))
        return 0 if not result["defects"] else 1

    if args.rev is None:
        print("usage: receipt-provenance.py --rev <hex commit> [--root .] "
              "[--from-round 60] [--to-round 79] [--json-out <path>]",
              file=sys.stderr)
        return 2
    if not 0 < args.from_round <= args.to_round:
        print(json.dumps({"ok": False,
                          "unevaluable": "--from-round must be <= --to-round and positive"}))
        return 2
    try:
        receipt = sweep(os.path.abspath(args.root), args.rev,
                        args.from_round, args.to_round)
    except Unevaluable as exc:
        print(json.dumps({"ok": False, "unevaluable": str(exc)}))
        return 2

    text = json.dumps(receipt, indent=1, sort_keys=True) + "\n"
    if args.json_out:
        pathlib.Path(args.json_out).write_text(text, encoding="utf-8")
    unexpected_paths = [row["path"] for row in receipt["rows"]
                        if row["verdict"] != "committed"
                        and os.path.basename(row["path"]) not in CONTROLS]
    print(json.dumps({"exit": 0 if receipt["unexpected"] == 0 else 1,
                      "rev": receipt["rev"],
                      "receipts": receipt["receipts"],
                      "flagged": receipt["flagged"],
                      "expected_control_flags": receipt["expected_control_flags"],
                      "unexpected": receipt["unexpected"],
                      "unexpected_paths": unexpected_paths,
                      "ok": receipt["ok"],
                      "git_calls": receipt["git_calls"],
                      "elapsed_seconds": receipt["elapsed_seconds"]},
                     sort_keys=True))
    return 0 if receipt["unexpected"] == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
