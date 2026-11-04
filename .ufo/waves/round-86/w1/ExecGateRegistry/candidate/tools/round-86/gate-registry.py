#!/usr/bin/env python3
"""Round-86 gate-registry counter: a gate's SKILL.md row must be re-derivable by running it.

The round-85 non-author spot-check routed R85-2: `tools/round-85/predicate-bind.py` is a gate the
lane runs, and `SKILL.md` has no instrument-registry row for it, so a reader of the lane's own
checklist cannot find, run or check it. This counter scores one registered gate's row against the
tool's observed behaviour at ONE revision.

Atoms (frozen in `plans/round-86-claims.md`):

  G1 row-present        the `<!-- instrument-registry -->` section holds exactly one row whose
                        cell 0 is exactly `` `tools/round-85/predicate-bind.py` ``, seven cells wide.
  G2 exit-map-observed  that row's verdict-map cell declares all three exits (`0=`, `1=`, `2=`)
                        and the observed `--selftest` exit equals the declared success exit 0.
  G3 self-invocation    the row's self-test cell names a command on that tool path; the command's
                        argv is executed with no shell under a four-key child env, and its
                        observed exit must equal the exit the cell declares.
  G4 pinned-blob        the row's pinned-value cell names at least one
                        `.ufo/waves/round-<N>/claims.json` that is a blob at --rev.
  G5 owner-round        the row's owner cell is `kaidoku-r<N>` with the same N as the tool's own
                        `tools/round-<N>/` directory.

Reading rule: in `--rev` mode every file is read with `git show REV:path` (S255: committed bytes,
never a worktree file). G2/G3 execute the tool's COMMITTED bytes: `git show REV:<tool>` is written to
`--work/export/<tool>` and the child runs there, so an uncommitted or edited tool in the `--root`
working tree can never satisfy them. `--worktree <dir>` is the fixture/selftest mode, where the
directory itself is the tree read and executed.

Hardening (round-86 candidate; the atom rules above are unchanged):
  - the registry markers must each occur exactly once, open before close; otherwise unevaluable.
  - a registry row is judged at its declared width: a target-path row that is not seven cells
    wide fails G1 (it is never read for G2-G5).
  - G3 executes only `python3 [-I|-B|-E|-s|-S|-u]... <TOOL> ...`: the tool path must be the first
    non-flag argument, so `python3 -c ...` naming the tool elsewhere is refused. The command is the
    first backtick span of the cell (or the text before ` — `); the declared exit is read from the
    cell outside that span.
  - an executed self-test that exits 0 while writing nothing to stdout or stderr is not evidence:
    the counter refuses to score it (unevaluable, exit 2) instead of recording a green.
  - G4 requires every pinned path the cell names to be a blob at --rev (stricter than "at least
    one"; see the round-86 notes for the divergence and why it refuses, never greens, more).
  - --rev must be 40 lowercase hex; --work (or $TMPDIR) inside `<root>/.ufo/waves` is refused.
  - child processes: argv list, no shell, stdin closed, env exactly PATH/HOME/TMPDIR/LANG with
    HOME and TMPDIR inside --work, a 600 s timeout; the last output line is recorded as `last_line`.

Verdict: `mismatches` lists every atom id that is false. Exit 0 when empty, 1 otherwise, 2 when
SKILL.md or the tool cannot be read at --rev, or the counter refuses to evaluate (see Hardening).

Control (`--control file-exists`): the cheap rule that skips the row work — the gate is "registered"
whenever its file exists at --rev. It is expected to ACCEPT the unregistered state; that
acceptance is what makes the target failable rather than satisfied by the tree's shape.

Limits (declared): one gate, five atoms. G2/G3 read exit codes, not verdict text (a silent exit 0
is refused rather than scored, see Hardening); G4 checks that a pinned path is a committed blob, not
that the pin's digest is right; G5 is a naming check.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

SKILL = "SKILL.md"
TOOL = "tools/round-85/predicate-bind.py"
REGISTRY_OPEN = "<!-- instrument-registry"
REGISTRY_CLOSE = "<!-- /instrument-registry -->"
ROW_WIDTH = 7
REV_RE = re.compile(r"[0-9a-f]{40}")
BACKTICK_RE = re.compile(r"`([^`]+)`")
INTERPRETER_FLAGS = ("-I", "-B", "-E", "-s", "-S", "-u")
CHILD_PATH = "/usr/local/bin:/usr/bin:/bin"
CHILD_LANG = "C.UTF-8"
CHILD_TIMEOUT = 600


class Unreadable(Exception):
    pass


def valid_rev(rev: str) -> bool:
    return REV_RE.fullmatch(rev) is not None


def inside_lane_waves(root: Path, work: Path) -> bool:
    waves = (root / ".ufo" / "waves").resolve()
    return work == waves or waves in work.parents


def git_show_bytes(root: Path, rev: str, path: str) -> bytes:
    proc = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"], capture_output=True)
    if proc.returncode != 0:
        raise Unreadable(f"{rev}:{path}: git show failed")
    return proc.stdout


def git_show(root: Path, rev: str, path: str) -> str:
    return git_show_bytes(root, rev, path).decode("utf-8")


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def registry_rows(skill_text: str) -> list[list[str]]:
    if skill_text.count(REGISTRY_OPEN) != 1 or skill_text.count(REGISTRY_CLOSE) != 1:
        raise Unreadable("SKILL.md must carry exactly one instrument-registry open and close marker")
    if skill_text.index(REGISTRY_OPEN) > skill_text.index(REGISTRY_CLOSE):
        raise Unreadable("SKILL.md registry close marker precedes its open marker")
    section = skill_text.split(REGISTRY_OPEN, 1)[1].split(REGISTRY_CLOSE, 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = split_row(line)
        if cells[0].startswith("`tools/"):
            rows.append(cells)
    return rows


def child_env(work: Path) -> dict[str, str]:
    return {"PATH": CHILD_PATH, "HOME": str(work / "home"),
            "TMPDIR": str(work / "tmp"), "LANG": CHILD_LANG}


def run_child(argv: list[str], cwd: Path, work: Path) -> tuple[int | None, str]:
    (work / "home").mkdir(parents=True, exist_ok=True)
    (work / "tmp").mkdir(parents=True, exist_ok=True)
    try:
        proc = subprocess.run(argv, cwd=str(cwd), env=child_env(work), stdin=subprocess.DEVNULL,
                              capture_output=True, text=True, timeout=CHILD_TIMEOUT)
    except (OSError, subprocess.SubprocessError) as exc:
        return None, f"exec error: {exc}"
    out = [ln for ln in proc.stdout.splitlines() if ln.strip()]
    err = [ln for ln in proc.stderr.splitlines() if ln.strip()]
    if proc.returncode == 0 and not out and not err:
        raise Unreadable(f"`{' '.join(argv[1:])}` exited 0 and printed nothing: "
                         "a silent exit is not a self-test")
    return proc.returncode, (out or err)[-1]


def declared_command_exit(text: str) -> int | None:
    m = re.search(r"\bexit\s+(\d+)\b", text)
    return int(m.group(1)) if m else None


def split_command(cell: str) -> tuple[str, str]:
    m = BACKTICK_RE.search(cell)
    if m:
        return m.group(1).strip(), cell[:m.start()] + " " + cell[m.end():]
    head, _, rest = cell.partition(" — ")
    return head.strip(), rest


def command_argv(command: str) -> list[str] | None:
    if not command.startswith("python3 "):
        return None
    try:
        argv = shlex.split(command)
    except ValueError:
        return None
    rest = argv[1:]
    i = 0
    while i < len(rest) and rest[i] in INTERPRETER_FLAGS:
        i += 1
    if i >= len(rest) or rest[i] != TOOL:
        return None
    return [sys.executable] + rest


def evaluate(read, root: Path, work: Path, rev: str, exec_dir: Path | None = None) -> dict:
    run_dir = exec_dir if exec_dir is not None else root
    atoms: list[dict] = []

    def add(atom_id: str, ok: bool, detail: dict) -> None:
        atoms.append({"id": atom_id, "ok": ok, "detail": detail})

    skill_text = read(SKILL)
    target = [r for r in registry_rows(skill_text) if r[0] == f"`{TOOL}`"]
    widths = [len(r) for r in target]
    row = target[0] if len(target) == 1 and widths[0] == ROW_WIDTH else None

    # G1
    add("G1-row-present", row is not None, {"rows": len(target), "cells": widths, "tool": TOOL})

    if row is None:
        for atom_id in ("G2-exit-map-observed", "G3-self-invocation",
                        "G4-pinned-blob", "G5-owner-round"):
            add(atom_id, False, {"why": "no single seven-cell registry row to read"})
        mismatches = [a["id"] for a in atoms if not a["ok"]]
        return receipt(root, rev, atoms, mismatches)

    # G2
    verdict_cell = row[2]
    declared_map = all(re.search(rf"(?<!\d){d}=", verdict_cell) for d in "012")
    observed, last = run_child([sys.executable, "-I", "-B", TOOL, "--selftest"], run_dir, work)
    add("G2-exit-map-observed", bool(declared_map) and observed == 0,
        {"declared_map_complete": bool(declared_map), "observed_selftest_exit": observed,
         "declared_success_exit": 0, "last_line": last})

    # G3
    command, rest = split_command(row[3])
    argv = command_argv(command)
    want = declared_command_exit(rest)
    if argv is None or want is None:
        add("G3-self-invocation", False,
            {"why": "self-test cell names no python3 command on the tool path or no declared exit",
             "cell": row[3][:160]})
    else:
        got, last = run_child(argv, run_dir, work)
        add("G3-self-invocation", got == want,
            {"argv": argv[1:], "declared_exit": want, "observed_exit": got, "last_line": last})

    # G4
    pins = re.findall(r"\.ufo/waves/round-\d+/claims\.json", row[4])
    present = []
    for pin in pins:
        try:
            read(pin)
            present.append(pin)
        except Unreadable:
            continue
    add("G4-pinned-blob", bool(pins) and len(present) == len(pins),
        {"declared_pins": pins, "blobs_at_rev": present})

    # G5
    owner = row[6]
    owner_m = re.fullmatch(r"kaidoku-r(\d+)", owner.strip())
    tool_m = re.search(r"tools/round-(\d+)/", TOOL)
    add("G5-owner-round", bool(owner_m and tool_m and owner_m.group(1) == tool_m.group(1)),
        {"owner": owner, "tool_round": tool_m.group(1) if tool_m else None})

    mismatches = [a["id"] for a in atoms if not a["ok"]]
    return receipt(root, rev, atoms, mismatches)


def evaluate_at_rev(root: Path, rev: str, work: Path) -> dict:
    """Score the committed registry at REV, executing the committed tool bytes from --work."""
    tool_bytes = git_show_bytes(root, rev, TOOL)
    export = work / "export" / TOOL
    export.parent.mkdir(parents=True, exist_ok=True)
    export.write_bytes(tool_bytes)

    def read(path: str) -> str:
        return git_show(root, rev, path)

    return evaluate(read, root, work, rev, exec_dir=work / "export")


def receipt(root: Path, rev: str, atoms: list[dict], mismatches: list[str]) -> dict:
    instrument = Path(__file__).resolve()
    try:
        rel = str(instrument.relative_to(root))
    except ValueError:
        rel = str(instrument)
    return {
        "schema": "kaidoku-r86-gate-registry-v1",
        "rev": rev,
        "tool": TOOL,
        "instrument": {"path": rel, "sha256": hashlib.sha256(instrument.read_bytes()).hexdigest()},
        "atoms": atoms,
        "mismatches": mismatches,
        "agreed": len(atoms) - len(mismatches),
        "total": len(atoms),
        "ok": not mismatches,
    }


def control_file_exists(read, root: Path, work: Path, rev: str) -> dict:
    try:
        read(TOOL)
        ok = True
        why = "tool blob exists at rev, so the cheap rule calls it registered"
    except Unreadable as exc:
        ok, why = False, str(exc)
    atoms = [{"id": a, "ok": ok, "detail": {"rule": why}} for a in
             ("G1-row-present", "G2-exit-map-observed", "G3-self-invocation",
              "G4-pinned-blob", "G5-owner-round")]
    mismatches = [a["id"] for a in atoms if not a["ok"]]
    instrument = Path(__file__).resolve()
    try:
        rel = str(instrument.relative_to(root))
    except ValueError:
        rel = str(instrument)
    return {
        "schema": "kaidoku-r86-gate-registry-v1-control",
        "control": "file-exists",
        "rev": rev,
        "tool": TOOL,
        "instrument": {"path": rel, "sha256": hashlib.sha256(instrument.read_bytes()).hexdigest()},
        "atoms": atoms,
        "mismatches": mismatches,
        "ok": not mismatches,
        "note": "expected to ACCEPT the unregistered state: existence is not registration",
    }


# ---------------------------------------------------------------- selftest

FIXTURE_TOOL = '''#!/usr/bin/env python3
import sys
if "--selftest" in sys.argv:
    print("SELFTEST cases=1 failures=0")
    sys.exit(0)
sys.exit(2)
'''

SILENT_TOOL = "#!/usr/bin/env python3\nimport sys\nsys.exit(0)\n"

FAIL_TOOL = ('#!/usr/bin/env python3\nimport sys\n'
             'print("SELFTEST cases=1 failures=1")\nsys.exit(1)\n')

ENV_TOOL = '''#!/usr/bin/env python3
import os, sys
keys = sorted(os.environ)
home_ok = os.environ.get("HOME", "").startswith(os.getcwd())
tmp_ok = os.environ.get("TMPDIR", "").startswith(os.getcwd())
if keys == ["HOME", "LANG", "PATH", "TMPDIR"] and home_ok and tmp_ok:
    print("SELFTEST env=four-keys")
    sys.exit(0)
print("SELFTEST env=bad " + ",".join(keys))
sys.exit(1)
'''

HEADER = ("| tool | gate or probe - purpose | verdict map (exit codes) | self-test command | "
          "pinned-value path | write scope | owner |\n|---|---|---|---|---|---|---|\n")


def fixture_skill(row: str | None) -> str:
    body = HEADER + (row + "\n" if row else "")
    return f"# SKILL\n\n{REGISTRY_OPEN} v2 -->\n\n{body}\n{REGISTRY_CLOSE}\n\ntrailing\n"


GOOD_ROW = ("| `tools/round-85/predicate-bind.py` | gate — fixture | "
            "0=clean; 1=flagged; 2=unreadable | "
            "`python3 -I -B tools/round-85/predicate-bind.py --selftest` — exit 0 | "
            "`.ufo/waves/round-85/claims.json` | none (read-only) | kaidoku-r85 |")
SIX_COL_ROW = ("| `tools/round-85/predicate-bind.py` | gate — fixture | "
               "0=clean; 1=flagged; 2=unreadable | "
               "`python3 -I -B tools/round-85/predicate-bind.py --selftest` — exit 0 | "
               "`.ufo/waves/round-85/claims.json` | none (read-only) |")
BAD_EXIT_ROW = GOOD_ROW.replace("— exit 0", "— exit 3")
BAD_PIN_ROW = GOOD_ROW.replace("round-85/claims.json", "round-85/absent.json")
BAD_OWNER_ROW = GOOD_ROW.replace("kaidoku-r85", "kaidoku-r84")
NO_MAP_ROW = GOOD_ROW.replace("0=clean; 1=flagged; 2=unreadable", "clean or flagged")
DUPLICATE = GOOD_ROW + "\n" + GOOD_ROW

R85_CLAIMS = {".ufo/waves/round-85/claims.json": '{"claims": []}\n'}
R84_CLAIMS_ONLY = {".ufo/waves/round-84/claims.json": '{"claims": []}\n'}


def write_fixture(work: Path, skill: str, tool: str | None, files: dict[str, str]) -> None:
    (work / "tools/round-85").mkdir(parents=True, exist_ok=True)
    (work / SKILL).write_text(skill)
    if tool is not None:
        (work / TOOL).write_text(tool)
        (work / TOOL).chmod(0o755)
    for rel, text in files.items():
        path = work / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)


def commit_files(repo: Path, files: dict[str, str]) -> str:
    """Build one commit from `files` with plumbing only (hash-object, update-index, write-tree)."""
    repo.mkdir(parents=True, exist_ok=True)
    git = ["git", "-C", str(repo)]
    subprocess.run(git + ["init", "-q"], check=True, capture_output=True)
    index_env = dict(os.environ, GIT_INDEX_FILE=str(repo / "fixture.idx"))
    for rel, text in files.items():
        blob = subprocess.run(git + ["hash-object", "-w", "--stdin"], input=text, text=True,
                              capture_output=True, check=True).stdout.strip()
        subprocess.run(git + ["update-index", "--add", "--cacheinfo", f"100644,{blob},{rel}"],
                       env=index_env, check=True, capture_output=True)
    tree = subprocess.run(git + ["write-tree"], env=index_env, capture_output=True,
                          text=True, check=True).stdout.strip()
    ident = dict(index_env, GIT_AUTHOR_NAME="fixture", GIT_AUTHOR_EMAIL="fixture@example.invalid",
                 GIT_COMMITTER_NAME="fixture", GIT_COMMITTER_EMAIL="fixture@example.invalid")
    return subprocess.run(git + ["commit-tree", tree, "-m", "fixture"], env=ident,
                          capture_output=True, text=True, check=True).stdout.strip()


def selftest() -> int:
    failures: list[str] = []
    cases = [
        # name, SKILL.md, tool bytes (None = absent), fixture files, expected outcome
        ("good-row", fixture_skill(GOOD_ROW), FIXTURE_TOOL, R85_CLAIMS, "ok"),
        ("absent-row", fixture_skill(None), FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("duplicate-row", fixture_skill(DUPLICATE), FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("six-column-row-missing-owner", fixture_skill(SIX_COL_ROW), FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("path-only-in-prose-outside-markers", fixture_skill(None) + GOOD_ROW + "\n",
         FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("doubled-open-marker", fixture_skill(GOOD_ROW) + REGISTRY_OPEN + " v2 -->\n",
         FIXTURE_TOOL, R85_CLAIMS, "unevaluable"),
        ("wrong-declared-exit", fixture_skill(BAD_EXIT_ROW), FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("selftest-cell-without-declared-exit", fixture_skill(GOOD_ROW.replace(" — exit 0", "")),
         FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("silent-exit-0-tool", fixture_skill(GOOD_ROW), SILENT_TOOL, R85_CLAIMS, "unevaluable"),
        ("tool-exits-1-declared-0", fixture_skill(GOOD_ROW), FAIL_TOOL, R85_CLAIMS, "fail"),
        ("tool-file-absent", fixture_skill(GOOD_ROW), None, R85_CLAIMS, "fail"),
        ("pin-absent-at-rev", fixture_skill(BAD_PIN_ROW), FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("pin-round-85-only-round-84-exists", fixture_skill(GOOD_ROW), FIXTURE_TOOL,
         R84_CLAIMS_ONLY, "fail"),
        ("owner-kaidoku-r850-wrong-n", fixture_skill(GOOD_ROW.replace("kaidoku-r85 |", "kaidoku-r850 |")),
         FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("owner-round-mismatch", fixture_skill(BAD_OWNER_ROW), FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("incomplete-verdict-map", fixture_skill(NO_MAP_ROW), FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("verdict-map-two-digit-exit", fixture_skill(GOOD_ROW.replace("2=unreadable", "12=unreadable")),
         FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("command-names-other-tool", fixture_skill(GOOD_ROW.replace(
            "predicate-bind.py --selftest`", "other.py --selftest`")), FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("python-c-names-tool-only-as-string", fixture_skill(GOOD_ROW.replace(
            "python3 -I -B tools/round-85/predicate-bind.py --selftest`",
            "python3 -c 'print(1)' tools/round-85/predicate-bind.py --selftest`")),
         FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("non-python-command", fixture_skill(GOOD_ROW.replace(
            "`python3 -I -B tools/round-85/predicate-bind.py --selftest`",
            "`sh tools/round-85/predicate-bind.py --selftest`")), FIXTURE_TOOL, R85_CLAIMS, "fail"),
        ("env-is-exactly-four-keys", fixture_skill(GOOD_ROW), ENV_TOOL, R85_CLAIMS, "ok"),
    ]
    checks = [
        ("waves-tree-refused", inside_lane_waves(Path("/x/lane"),
                                                 Path("/x/lane/.ufo/waves/round-86/w1")) is True),
        ("scratch-outside-waves-accepted", inside_lane_waves(Path("/x/lane"),
                                                             Path("/x/scratch")) is False),
        ("waves-sibling-prefix-accepted", inside_lane_waves(Path("/x/lane"),
                                                            Path("/x/lane/.ufo/wavesX")) is False),
        ("short-rev-refused", valid_rev("2cf0b7f") is False),
        ("full-rev-accepted", valid_rev("2cf0b7ff93c698809bed321f7338276a22d6beb9") is True),
    ]
    with tempfile.TemporaryDirectory(prefix="r86-gate-registry-selftest-") as tmp:
        base = Path(tmp).resolve()
        for name, skill, tool, files, expect in cases:
            work = base / name
            write_fixture(work, skill, tool, files)

            def read(path: str, _work: Path = work) -> str:
                try:
                    return (_work / path).read_text()
                except OSError as exc:
                    raise Unreadable(f"{path}: {exc}") from exc

            scratch = work / "scratch"
            scratch.mkdir()
            result = None
            try:
                result = evaluate(read, work, scratch, "worktree", exec_dir=work)
                outcome = "ok" if result["ok"] else "fail"
            except Unreadable:
                outcome = "unevaluable"
            if outcome != expect:
                detail = result["mismatches"] if result else "refused"
                failures.append(f"{name}: expected {expect}, got {outcome} ({detail})")
            if name == "good-row" and result:
                g3 = next(a for a in result["atoms"] if a["id"] == "G3-self-invocation")
                if g3["detail"].get("last_line") != "SELFTEST cases=1 failures=0":
                    failures.append(f"{name}: last_line not recorded from the child")
            if tool is not None:
                ctl = control_file_exists(read, work, scratch, "worktree")
                if not ctl["ok"]:
                    failures.append(f"{name}: control refused a tool present at rev")

        # rev mode: the verdict must come from the COMMITTED tool, never the working tree
        skill_files = {SKILL: fixture_skill(GOOD_ROW), **R85_CLAIMS}
        rev_cases = [
            ("rev-committed-red-worktree-green", {**skill_files, TOOL: FAIL_TOOL}, FIXTURE_TOOL, "fail"),
            ("rev-committed-green", {**skill_files, TOOL: FIXTURE_TOOL}, None, "ok"),
        ]
        for name, files, worktree_tool, expect in rev_cases:
            repo = base / name
            rev = commit_files(repo, files)
            if worktree_tool is not None:
                (repo / TOOL).parent.mkdir(parents=True, exist_ok=True)
                (repo / TOOL).write_text(worktree_tool)
            work = repo / "scratch"
            work.mkdir(parents=True, exist_ok=True)
            try:
                result = evaluate_at_rev(repo, rev, work)
                outcome = "ok" if result["ok"] else "fail"
            except Unreadable:
                result, outcome = None, "unevaluable"
            if outcome != expect:
                detail = result["mismatches"] if result else "refused"
                failures.append(f"{name}: expected {expect}, got {outcome} ({detail})")

    for name, ok in checks:
        if not ok:
            failures.append(f"check {name} failed")

    total = len(cases) + len(rev_cases) + len(checks)
    print(f"SELFTEST cases={total} failures={len(failures)}")
    for failure in failures:
        print(f"FAIL {failure}")
    return 0 if not failures else 1


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--rev")
    ap.add_argument("--worktree")
    ap.add_argument("--work")
    ap.add_argument("--control", choices=["file-exists"])
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args()

    if args.selftest:
        return selftest()

    root = Path(args.root).resolve()
    scratch = Path(args.work or os.environ.get("TMPDIR", tempfile.gettempdir())).resolve()
    if inside_lane_waves(root, scratch):
        print(f"UNEVALUABLE: --work {scratch} is inside {root / '.ufo' / 'waves'}", file=sys.stderr)
        return 2
    scratch.mkdir(parents=True, exist_ok=True)

    try:
        if args.worktree:
            work_root = Path(args.worktree).resolve()

            def read(path: str) -> str:
                try:
                    return (work_root / path).read_text()
                except OSError as exc:
                    raise Unreadable(f"{path}: {exc}") from exc

            rev = f"worktree:{work_root}"
            if args.control:
                data = control_file_exists(read, work_root, scratch, rev)
            else:
                data = evaluate(read, work_root, scratch, rev, exec_dir=work_root)
        else:
            if not args.rev:
                print("UNEVALUABLE: --rev or --worktree is required", file=sys.stderr)
                return 2
            if not valid_rev(args.rev):
                print("UNEVALUABLE: --rev must be 40 lowercase hex", file=sys.stderr)
                return 2
            rev = args.rev
            if args.control:
                def read(path: str) -> str:
                    return git_show(root, rev, path)

                data = control_file_exists(read, root, scratch, rev)
            else:
                data = evaluate_at_rev(root, rev, scratch)
    except Unreadable as exc:
        print(f"UNEVALUABLE: {exc}", file=sys.stderr)
        return 2

    text = json.dumps(data, indent=1, sort_keys=True)
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text + "\n")
    print(text)
    if args.control:
        print(f"CONTROL {args.control} mismatches={len(data['mismatches'])} accepted={data['ok']}")
        return 0 if data["ok"] else 1
    print(f"GATE_REGISTRY agreed={data['agreed']}/{data['total']} mismatches={data['mismatches']}")
    return 0 if data["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
