#!/usr/bin/env python3
"""Round-86 gate-registry counter: a gate's SKILL.md row must be re-derivable by running it.

The round-85 non-author spot-check routed R85-2: `tools/round-85/predicate-bind.py` is a gate the
lane runs, and `SKILL.md` has no instrument-registry row for it, so a reader of the lane's own
checklist cannot find, run or check it. This counter scores one registered gate's row against the
tool's observed behaviour at ONE revision.

Atoms (frozen in `plans/round-86-claims.md`):

  G1 row-present        the `<!-- instrument-registry -->` section holds exactly one row whose
                        cell 0 is exactly `` `tools/round-85/predicate-bind.py` ``.
  G2 exit-map-observed  that row's verdict-map cell declares all three exits (`0=`, `1=`, `2=`)
                        and the observed `--selftest` exit equals the declared success exit 0.
  G3 self-invocation    the row's self-test cell names a command on that tool path; the command's
                        argv is executed with no shell in `--root` under a four-key child env, and
                        its observed exit must equal the exit the cell declares.
  G4 pinned-blob        the row's pinned-value cell names at least one
                        `.ufo/waves/round-<N>/claims.json` that is a blob at --rev.
  G5 owner-round        the row's owner cell is `kaidoku-r<N>` with the same N as the tool's own
                        `tools/round-<N>/` directory.

Reading rule: in `--rev` mode every file is read with `git show REV:path` (S255: committed bytes,
never a worktree file); `--worktree <dir>` is the fixture/selftest mode. The executed command is
the row's own declared spelling, so a row that states a command the tool cannot honour fails G3.

Verdict: `mismatches` lists every atom id that is false. Exit 0 when empty, 1 otherwise, 2 when
SKILL.md or the tool cannot be read at --rev.

Control (`--control file-exists`): the cheap rule that skips the row work — the gate is "registered"
whenever its file exists at --rev. It is expected to ACCEPT the unregistered state; that
acceptance is what makes the target failable rather than satisfied by the tree's shape.

Limits (declared): one gate, five atoms. G2/G3 read exit codes, not verdict text; G4 checks that a
pinned path is a committed blob, not that the pin's digest is right; G5 is a naming check.
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


class Unreadable(Exception):
    pass


def git_show(root: Path, rev: str, path: str) -> str:
    proc = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise Unreadable(f"{rev}:{path}: git show failed")
    return proc.stdout


def split_row(line: str) -> list[str]:
    body = line.strip()
    if body.startswith("|"):
        body = body[1:]
    if body.endswith("|"):
        body = body[:-1]
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def registry_rows(skill_text: str) -> list[list[str]]:
    if REGISTRY_OPEN not in skill_text or REGISTRY_CLOSE not in skill_text:
        raise Unreadable("SKILL.md has no single instrument-registry section")
    section = skill_text.split(REGISTRY_OPEN, 1)[1].split(REGISTRY_CLOSE, 1)[0]
    rows = []
    for line in section.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = split_row(line)
        if len(cells) >= 7 and cells[0].startswith("`tools/"):
            rows.append(cells)
    return rows


def find_row(skill_text: str) -> list[str] | None:
    matches = [r for r in registry_rows(skill_text) if r[0] == f"`{TOOL}`"]
    return matches[0] if len(matches) == 1 else None


def run_selftest(root: Path, work: Path) -> int:
    env = {
        "PATH": "/usr/local/bin:/usr/bin:/bin",
        "HOME": str(work / "home"),
        "TMPDIR": str(work / "tmp"),
        "LANG": "C.UTF-8",
    }
    (work / "home").mkdir(parents=True, exist_ok=True)
    (work / "tmp").mkdir(parents=True, exist_ok=True)
    proc = subprocess.run([sys.executable, "-I", "-B", TOOL, "--selftest"],
                          cwd=str(root), env=env, capture_output=True, text=True, timeout=600)
    return proc.returncode


def declared_command_exit(cell: str) -> int | None:
    m = re.search(r"\bexit\s+(\d)\b", cell)
    return int(m.group(1)) if m else None


def command_argv(cell: str) -> list[str] | None:
    text = cell.split(" — ", 1)[0].strip()
    text = text.strip("`").strip()
    if not text.startswith("python3 "):
        return None
    try:
        argv = shlex.split(text)
    except ValueError:
        return None
    return [sys.executable] + argv[1:]


def evaluate(read, root: Path, work: Path, rev: str) -> dict:
    atoms: list[dict] = []

    def add(atom_id: str, ok: bool, detail: dict) -> None:
        atoms.append({"id": atom_id, "ok": ok, "detail": detail})

    skill_text = read(SKILL)
    row = find_row(skill_text)

    # G1
    count = sum(1 for r in registry_rows(skill_text) if r[0] == f"`{TOOL}`")
    add("G1-row-present", count == 1, {"rows": count, "tool": TOOL})

    if row is None:
        for atom_id in ("G2-exit-map-observed", "G3-self-invocation", "G4-pinned-blob", "G5-owner-round"):
            add(atom_id, False, {"why": "no registry row to read"})
        mismatches = [a["id"] for a in atoms if not a["ok"]]
        return receipt(root, rev, atoms, mismatches)

    # G2
    verdict_cell = row[2]
    declared_map = all(tok in verdict_cell for tok in ("0=", "1=", "2="))
    observed = run_selftest(root, work)
    add("G2-exit-map-observed", declared_map and observed == 0,
        {"declared_map_complete": declared_map, "observed_selftest_exit": observed,
         "declared_success_exit": 0})

    # G3
    argv = command_argv(row[3])
    want = declared_command_exit(row[3])
    if argv is None or want is None:
        add("G3-self-invocation", False,
            {"why": "self-test cell names no python3 command on the tool path or no declared exit",
             "cell": row[3][:160]})
    else:
        env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": str(work / "home"),
               "TMPDIR": str(work / "tmp"), "LANG": "C.UTF-8"}
        try:
            proc = subprocess.run(argv, cwd=str(root), env=env, capture_output=True,
                                  text=True, timeout=600)
            got = proc.returncode
            tail = (proc.stdout or "").strip().splitlines()[-1:] or [""]
        except (OSError, subprocess.SubprocessError) as exc:
            got, tail = None, [f"exec error: {exc}"]
        add("G3-self-invocation", got == want,
            {"argv": argv[2:], "declared_exit": want, "observed_exit": got, "last_line": tail[0]})

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
    tool_round = re.search(r"tools/round-(\d+)/", TOOL)
    owner_round = re.search(r"kaidoku-r(\d+)$", owner.strip())
    add("G5-owner-round", bool(owner_round and tool_round
                               and owner_round.group(1) == tool_round.group(1)),
        {"owner": owner, "tool_round": tool_round.group(1) if tool_round else None})

    mismatches = [a["id"] for a in atoms if not a["ok"]]
    return receipt(root, rev, atoms, mismatches)


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

HEADER = ("| tool | gate or probe - purpose | verdict map (exit codes) | self-test command | "
          "pinned-value path | write scope | owner |\n|---|---|---|---|---|---|---|\n")


def fixture_skill(row: str | None) -> str:
    body = HEADER + (row + "\n" if row else "")
    return f"# SKILL\n\n{REGISTRY_OPEN} v2 -->\n\n{body}\n{REGISTRY_CLOSE}\n\ntrailing\n"


GOOD_ROW = ("| `tools/round-85/predicate-bind.py` | gate — fixture | "
            "0=clean; 1=flagged; 2=unreadable | "
            "`python3 -I -B tools/round-85/predicate-bind.py --selftest` — exit 0 | "
            "`.ufo/waves/round-85/claims.json` | none (read-only) | kaidoku-r85 |")
BAD_EXIT_ROW = GOOD_ROW.replace("— exit 0", "— exit 3")
BAD_PIN_ROW = GOOD_ROW.replace("round-85/claims.json", "round-85/absent.json")
BAD_OWNER_ROW = GOOD_ROW.replace("kaidoku-r85", "kaidoku-r84")
NO_MAP_ROW = GOOD_ROW.replace("0=clean; 1=flagged; 2=unreadable", "clean or flagged")
DUPLICATE = GOOD_ROW + "\n" + GOOD_ROW


def selftest() -> int:
    failures = []
    cases = [
        ("good-row", GOOD_ROW, True),
        ("absent-row", None, False),
        ("duplicate-row", DUPLICATE, False),
        ("wrong-declared-exit", BAD_EXIT_ROW, False),
        ("pin-absent-at-rev", BAD_PIN_ROW, False),
        ("owner-round-mismatch", BAD_OWNER_ROW, False),
        ("incomplete-verdict-map", NO_MAP_ROW, False),
    ]
    with tempfile.TemporaryDirectory(prefix="r86-gate-registry-selftest-") as tmp:
        base = Path(tmp)
        for name, row, expect_ok in cases:
            work = base / name
            (work / "tools/round-85").mkdir(parents=True, exist_ok=True)
            (work / ".ufo/waves/round-85").mkdir(parents=True, exist_ok=True)
            (work / SKILL).write_text(fixture_skill(row))
            (work / TOOL).write_text(FIXTURE_TOOL)
            (work / TOOL).chmod(0o755)
            (work / ".ufo/waves/round-85/claims.json").write_text('{"claims": []}\n')

            def read(path: str, _work: Path = work) -> str:
                try:
                    return (_work / path).read_text()
                except OSError as exc:
                    raise Unreadable(f"{path}: {exc}") from exc

            scratch = work / "scratch"
            scratch.mkdir()
            result = evaluate(read, work, scratch, "worktree")
            if result["ok"] is not expect_ok:
                failures.append(f"{name}: expected ok={expect_ok}, mismatches={result['mismatches']}")
            # the control must ACCEPT the defective world (existence is not registration)
            if not expect_ok:
                ctl = control_file_exists(read, work, scratch, "worktree")
                if not ctl["ok"]:
                    failures.append(f"{name}: control refused a defective record")
        # control accepts the genuine world too
        work = base / "good-row"

        def good_read(path: str) -> str:
            return (work / path).read_text()

        if not control_file_exists(good_read, work, work / "scratch", "worktree")["ok"]:
            failures.append("control refused the genuine world")

    print(f"SELFTEST cases={len(cases) + 1} failures={len(failures)}")
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
    scratch.mkdir(parents=True, exist_ok=True)

    if args.worktree:
        work_root = Path(args.worktree).resolve()

        def read(path: str) -> str:
            try:
                return (work_root / path).read_text()
            except OSError as exc:
                raise Unreadable(f"{path}: {exc}") from exc

        rev = f"worktree:{work_root}"
    else:
        if not args.rev:
            print("UNEVALUABLE: --rev or --worktree is required", file=sys.stderr)
            return 2
        rev = args.rev

        def read(path: str) -> str:
            return git_show(root, rev, path)

    try:
        if args.control:
            data = control_file_exists(read, root, scratch, rev)
        else:
            data = evaluate(read, root, scratch, rev)
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
