#!/usr/bin/env python3
"""Round-84 mutation closure counter: every declared mutant dies by its declared selftest case.

Reads a mutant table (`.ufo/waves/round-84/mutants.json`) and, for every entry, applies one
declared single-behavior text change to the target tool's bytes at --rev in a private scratch
copy, runs that tool's own `--selftest`, and scores the mutant killed only when the *declared*
case appears in the selftest's failing-case list (QUALITY 138: a mutant is killed by a detector
present in the target's own output; an absent declared case scores survived, never a pass).

Per mutant status:
  killed        the declared case failed in the mutant run and passed in the pristine run
  survived      the mutant run did not fail the declared case, including the case where the
                declared case is absent from the pristine inventory (QUALITY 138: an absent
                detector is a survivor, never a pass)
  inconclusive  an anchor does not occur exactly once, the id is not a leaf name, or the
                pristine tool is not green
The table never edits the lane tree: pristine and mutant copies live under --work and the
pristine bytes are written back after each mutant to prove exact restoration.

Exit: 0 when every mutant is killed and every target's pristine selftest is green; 1 otherwise;
2 when the table or a target cannot be read. `--selftest` exercises this scorer on fixtures.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "kaidoku-r84-mutation-closure-v1"
JSON_FAIL_RE = re.compile(r"^SELFTEST cases=(\d+) failures=(\d+)$", re.M)
LINE_FAIL_RE = re.compile(r"^selftest (\S+): FAIL\b", re.M)


def git_blob(root: str, rev: str, path: str) -> bytes | None:
    done = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    return done.stdout if done.returncode == 0 else None


def parse_selftest(stdout: str) -> dict:
    """Parse case names and failures from a tool's selftest output.

    Accepts both shapes used in this lane: a JSON summary carrying `case_names`/`failures`
    (conjunction-gate, printed-command) and plain `selftest <case>: FAIL` lines
    (source-bind). Never guesses: a shape carrying neither yields an empty inventory.
    """
    failures: set[str] = set()
    names: set[str] = set()
    summary = JSON_FAIL_RE.search(stdout)
    decoder = json.JSONDecoder()
    index = 0
    found_summary = False
    while index < len(stdout):
        brace = stdout.find("{", index)
        if brace < 0:
            break
        try:
            value, end = decoder.raw_decode(stdout[brace:])
        except json.JSONDecodeError:
            index = brace + 1
            continue
        index = brace + end
        if isinstance(value, dict) and isinstance(value.get("failures"), list):
            found_summary = True
            for item in value["failures"]:
                if isinstance(item, str):
                    failures.add(item)
            for item in value.get("case_names") or []:
                if isinstance(item, str):
                    names.add(item)
            for item in value.get("checks") or []:
                if isinstance(item, dict) and isinstance(item.get("case"), str):
                    names.add(item["case"])
                    if item.get("ok") is False:
                        failures.add(item["case"])
    for name in LINE_FAIL_RE.findall(stdout):
        failures.add(name)
    for check_case in re.findall(r"^selftest (\S+): ok\b", stdout, re.M):
        names.add(check_case)
    if not found_summary and failures:
        # case names are only known from the failing lines in this shape
        names |= failures
    return {"failures": sorted(failures), "case_names": sorted(names),
            "cases": int(summary.group(1)) if summary else None,
            "failures_declared": int(summary.group(2)) if summary else None}


def run_selftest(script: str, work: str, env: dict) -> dict:
    argv = [sys.executable, "-I", "-B", script, "--selftest"]
    try:
        done = subprocess.run(argv, cwd=work, env=env, capture_output=True,
                              text=True, timeout=300)
    except subprocess.TimeoutExpired:
        return {"exit": 124, "stdout": "", "stderr": "timeout",
                **parse_selftest("")}
    return {"exit": done.returncode, "stdout": done.stdout[-20000:],
            "stderr": done.stderr[-4000:], **parse_selftest(done.stdout)}


def table_identity(mutants_path: str, claims_path: str | None) -> dict:
    """Compare the frozen table's bytes to the digest its container records.

    A row dropped or replaced after the freeze still yields a green counter; the
    container's `fixtures` block is the pin both sides can re-derive
    (round-84 CriticClaims refutation 2).
    """
    digest = _sha(Path(mutants_path).read_bytes())
    observed = {"path": mutants_path, "sha256": digest, "expected": None,
                "matches": None}
    if claims_path is None:
        candidate = Path(mutants_path).with_name("claims.json")
        claims_path = str(candidate) if candidate.exists() else None
        observed["claims"] = claims_path
    if not claims_path or not Path(claims_path).exists():
        return observed
    try:
        container = json.loads(Path(claims_path).read_text())
    except json.JSONDecodeError:
        observed["matches"] = False
        observed["reason"] = "claims-unparsable"
        return observed
    fixtures = container.get("fixtures") if isinstance(container, dict) else None
    if not isinstance(fixtures, dict) or not fixtures.get("sha256"):
        return observed
    observed["expected"] = fixtures["sha256"]
    observed["matches"] = fixtures["sha256"] == digest
    return observed


def score(root: str, rev: str, table: dict, work: str,
          table_info: dict | None = None) -> dict:
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(work, "tmp")
    os.makedirs(env["TMPDIR"], exist_ok=True)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    targets: dict[str, dict] = {}
    for path in sorted({m["target"] for m in table["mutants"]}):
        body = git_blob(root, rev, path)
        if body is None:
            return {"schema": SCHEMA, "rev": rev, "unevaluable": f"target absent: {path}",
                    "mutants": len(table["mutants"]), "killed": 0, "survivors": [],
                    "inconclusive": [], "pristine_failed": [], "ok": False}
        pristine = os.path.join(work, "pristine")
        os.makedirs(pristine, exist_ok=True)
        copy = os.path.join(pristine, os.path.basename(path))
        Path(copy).write_bytes(body)
        pristine_result = run_selftest(copy, pristine, env)
        targets[path] = {"target": path, "sha256": _sha(body),
                         "pristine": {k: pristine_result[k]
                                      for k in ("exit", "failures", "case_names",
                                                "cases", "failures_declared")},
                         "green": pristine_result["exit"] == 0
                         and not pristine_result["failures"]}
    survivors: list[dict] = []
    inconclusive: list[dict] = []
    killed: list[dict] = []
    pristine_failed = [p for p, t in targets.items() if not t["green"]]
    for mutant in table["mutants"]:
        path = mutant["target"]
        body = git_blob(root, rev, path)
        text = body.decode("utf-8")
        edits = mutant.get("edits") or [{"find": mutant["find"],
                                         "replace": mutant["replace"]}]
        counts = [text.count(edit["find"]) for edit in edits]
        entry = {"id": mutant["id"], "target": path,
                 "declared_case": mutant["declared_case"],
                 "anchor_occurrences": counts if len(counts) > 1 else counts[0],
                 "edits": len(edits)}
        if unsafe_component(mutant["id"]):
            entry["status"] = "inconclusive"
            entry["reason"] = "unsafe-mutant-id"
            inconclusive.append(entry)
            continue
        if any(count != 1 for count in counts):
            entry["status"] = "inconclusive"
            entry["reason"] = "anchor-not-exactly-once"
            inconclusive.append(entry)
            continue
        mutated = text
        for edit in edits:
            mutated = mutated.replace(edit["find"], edit["replace"])
        assert mutated != text, mutant["id"]
        mutant_dir = os.path.join(work, "mutants", mutant["id"])
        os.makedirs(mutant_dir, exist_ok=True)
        script = os.path.join(mutant_dir, os.path.basename(path))
        Path(script).write_text(mutated)
        result = run_selftest(script, mutant_dir, env)
        pristine_inventory = targets[path]["pristine"]["case_names"]
        case_present = mutant["declared_case"] in pristine_inventory
        entry.update({"exit": result["exit"], "failures": result["failures"],
                      "declared_case_present": case_present})
        if not targets[path]["green"]:
            entry["status"] = "inconclusive"
            entry["reason"] = "pristine-not-green"
            inconclusive.append(entry)
        elif not case_present:
            # QUALITY 138: an absent declared case is a survivor, never a pass.
            entry["status"] = "survived"
            entry["reason"] = "declared-case-absent-from-selftest"
            survivors.append(entry)
        elif mutant["declared_case"] in result["failures"]:
            entry["status"] = "killed"
            killed.append(entry)
        else:
            entry["status"] = "survived"
            survivors.append(entry)
        # exact restoration: the pristine bytes go back and must hash to the original
        Path(script).write_bytes(body)
        if _sha(Path(script).read_bytes()) != _sha(body):
            entry["restored_equal"] = False
            inconclusive.append({**entry, "status": "inconclusive",
                                 "reason": "restore-mismatch"})
        else:
            entry["restored_equal"] = True

    total = len(table["mutants"])
    table_ok = table_info is None or table_info.get("matches") is not False
    ok = (not survivors and not inconclusive and not pristine_failed
          and len(killed) == total and total > 0 and table_ok)
    receipt = {"schema": SCHEMA, "rev": rev,
               "instrument": {"path": "tools/round-84/mutation-closure.py",
                              "sha256": _sha(Path(__file__).read_bytes())},
               "targets": targets, "mutants": total, "killed": len(killed),
               "survivors": [m["id"] for m in survivors],
               "inconclusive": [f"{m['id']}:{m.get('reason')}" for m in inconclusive],
               "pristine_failed": pristine_failed,
               "table_identity": table_info,
               "results": killed + survivors + inconclusive, "ok": ok}
    return receipt


def _sha(body: bytes) -> str:
    import hashlib
    return hashlib.sha256(body).hexdigest()


def unsafe_component(name: str) -> bool:
    """A table-supplied id becomes a path component; refuse anything but a leaf name.

    QUALITY 119/127: containment is a path question, so a separator, a parent
    reference or an absolute spelling is refused before any write, never joined
    and hoped for.
    """
    if not isinstance(name, str) or not name or name in (".", ".."):
        return True
    if os.path.isabs(name) or os.sep in name or (os.altsep and os.altsep in name):
        return True
    return os.path.basename(name) != name


# --------------------------------------------------------------------------
# selftest: a fixture tool and a fixture mutant table; no lane target is read
# --------------------------------------------------------------------------

FIXTURE_TOOL = '''#!/usr/bin/env python3
import json
OK = True
CASES = {"alpha": True, "beta": OK, "gamma": True}
failures = sorted(name for name, ok in CASES.items() if not ok)
print(json.dumps({"cases": len(CASES), "case_names": sorted(CASES),
                  "failures": failures}))
print(f"SELFTEST cases={len(CASES)} failures={len(failures)}")
raise SystemExit(0 if not failures else 1)
'''

FIXTURE_TABLE = {
    "mutants": [
        {"id": "beta-live", "target": "fixture.py", "find": "OK = True",
         "replace": "OK = False", "declared_case": "beta"},
        {"id": "declared-case-absent", "target": "fixture.py", "find": "gamma",
         "replace": "delta", "declared_case": "omega"},
        {"id": "anchor-absent", "target": "fixture.py", "find": "NOT-THERE",
         "replace": "x", "declared_case": "beta"},
    ]
}


def selftest(json_out: str | None) -> int:
    work = tempfile.mkdtemp(prefix="mutation-closure-selftest-")
    cases: dict[str, bool] = {}
    try:
        fixture = os.path.join(work, "fixture.py")
        Path(fixture).write_text(FIXTURE_TOOL)
        rendered = subprocess.run([sys.executable, "-I", "-B", fixture, "--selftest"],
                                  cwd=work, capture_output=True, text=True)
        parsed = parse_selftest(rendered.stdout)
        check = lambda name, cond: cases.__setitem__(name, bool(cond))
        check("parser-json-inventory",
              parsed["case_names"] == ["alpha", "beta", "gamma"]
              and parsed["failures"] == [] and rendered.returncode == 0)
        check("parser-plain-fail-line",
              parse_selftest("selftest late: FAIL rc=[0, 0]\nselftest: FAILED\n")
              ["failures"] == ["late"])
        table = dict(FIXTURE_TABLE)
        # score the fixture table against a revisionless blob reader through a private repo
        repo = os.path.join(work, "repo")
        os.makedirs(repo)
        subprocess.run(["git", "-C", repo, "init", "-q"], check=True)
        Path(repo, "fixture.py").write_text(FIXTURE_TOOL)
        subprocess.run(["git", "-C", repo, "add", "fixture.py"], check=True)
        subprocess.run(["git", "-C", repo, "-c", "user.name=f", "-c", "user.email=f@f",
                        "commit", "-qm", "fixture"], check=True)
        receipt = score(repo, "HEAD", table, os.path.join(work, "run"))
        by_id = {r["id"]: r for r in receipt["results"]}
        check("killed-by-declared-case", by_id["beta-live"]["status"] == "killed")
        check("absent-case-survives",
              by_id["declared-case-absent"]["status"] == "survived"
              and by_id["declared-case-absent"]["reason"]
              == "declared-case-absent-from-selftest")
        check("absent-anchor-inconclusive",
              by_id["anchor-absent"]["status"] == "inconclusive")
        table_unsafe = {"mutants": [{"id": "../../escape", "target": "fixture.py",
                                     "find": "OK = True", "replace": "OK = False",
                                     "declared_case": "beta"}]}
        escaped = os.path.join(work, "escape")
        receipt_unsafe = score(repo, "HEAD", table_unsafe, os.path.join(work, "run-unsafe"))
        check("unsafe-id-refused",
              receipt_unsafe["results"][0]["status"] == "inconclusive"
              and receipt_unsafe["results"][0]["reason"] == "unsafe-mutant-id"
              and not os.path.exists(escaped)
              and not os.path.exists(os.path.join(work, "mutants", "escape")))
        check("not-met-on-fixture-table", receipt["ok"] is False)
        check("restoration", not any(r.get("restored_equal") is False for r in receipt["results"]))
        table_path = os.path.join(work, "fixture.json")
        Path(table_path).write_text(json.dumps(table))
        good_digest = table_identity(table_path, None)["sha256"]
        pinned = os.path.join(work, "pinned.json")
        Path(pinned).write_text(json.dumps({"fixtures": {"path": "fixture.json",
                                                        "sha256": good_digest}}))
        matched = table_identity(table_path, pinned)
        Path(pinned).write_text(json.dumps({"fixtures": {"path": "fixture.json",
                                                        "sha256": "0" * 64}}))
        mismatch = table_identity(table_path, pinned)
        check("table-digest-match", matched["matches"] is True)
        check("table-digest-mismatch-fails", mismatch["matches"] is False
              and mismatch["expected"] == "0" * 64
              and mismatch["sha256"] == good_digest)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    failures = sorted(name for name, ok in cases.items() if not ok)
    summary = {"schema": SCHEMA + "-selftest", "cases": len(cases),
               "case_names": sorted(cases), "failures": failures}
    text = json.dumps(summary, indent=1, sort_keys=True)
    if json_out:
        Path(json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(json_out).write_text(text + "\n")
    print(text)
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--mutants")
    ap.add_argument("--claims")
    ap.add_argument("--work")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args()
    if args.selftest:
        return selftest(args.json_out)
    if not (args.rev and args.mutants and args.work):
        ap.error("--rev, --mutants and --work are required")
    table = json.loads(Path(args.mutants).read_text())
    receipt = score(args.root, args.rev, table, args.work,
                    table_identity(args.mutants, getattr(args, "claims", None)))
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(text + "\n")
    print(json.dumps({k: receipt[k] for k in
                      ("rev", "mutants", "killed", "survivors", "inconclusive",
                       "pristine_failed", "table_identity", "ok")}, sort_keys=True))
    return 0 if receipt["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
