#!/usr/bin/env python3
"""M1-M6 mutation probe for tools/round-68/registry-conformance.py.

Copies the pristine instrument into mut/<ID>.py, applies one exact textual
substitution, then scores each copy with (a) --selftest and (b) --root/--rev
against four scratch git fixtures (plus the read-only lane at the frozen base).
The pristine instrument is never written.
"""
from __future__ import annotations

import hashlib
import json
import pathlib
import shutil
import subprocess
import sys

PRISTINE = pathlib.Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-68/registry-conformance.py")
LANE = pathlib.Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
SCRATCH = pathlib.Path("/fast/scratch/hyaku/kaidoku-r68/MutRegistry")
MUT = SCRATCH / "mut"
FIX = SCRATCH / "fixtures"
WAVE = LANE / ".ufo/waves/round-68/w1/MutRegistry"
BASE_REV = "fcbe200f6739c38939e0dabf3f251de2cc6bd727"
FULL = "0=met; 1=not met; 2=could-not-evaluate"

MUTANTS = {
    "M1": (
        "drop the own-round check -> a plan's foreign tool enters scope",
        [
            (
                "            if not tool.startswith(own):\n"
                "                continue  # a foreign round's tool belongs to that round's regime\n",
                "            pass  # M1: own-round check dropped\n",
            )
        ],
    ),
    "M2": (
        "drop `thin` from `mismatches`",
        [
            (
                "    mismatches = len(unregistered) + len(duplicate_rows) + len(row_absent) + len(thin)\n",
                "    mismatches = len(unregistered) + len(duplicate_rows) + len(row_absent)\n",
            )
        ],
    ),
    "M3": (
        "drop the duplicate test",
        [
            (
                "    duplicate_rows = sorted(p for p, r in by_path.items() if len(r) > 1)\n",
                "    duplicate_rows = []  # M3: duplicate test dropped\n",
            )
        ],
    ),
    "M4": (
        "census returns mismatches: 0 unconditionally",
        [
            (
                "    mismatches = len(unregistered) + len(duplicate_rows) + len(row_absent) + len(thin)\n",
                "    mismatches = 0  # M4: unconditional\n",
            )
        ],
    ),
    "M5": (
        'relax the verdict grammar to re.search("0|1|2", cell)',
        [
            (
                'VERDICT_RE = (re.compile(r"(?:^|[;|]\\s*|\\s)0\\s*(?:[=:]|\\s+[A-Za-z(])"),\n'
                '              re.compile(r"(?:^|[;|]\\s*|\\s)1\\s*(?:[=:]|\\s+[A-Za-z(])"),\n'
                '              re.compile(r"(?:^|[;|]\\s*|\\s)2\\s*(?:[=:]|\\s+[A-Za-z(])"))\n',
                'VERDICT_RE = (re.compile(r"0|1|2"),)\n',
            )
        ],
    ),
    "M6": (
        "--selftest executes 10 cases (drops row-absent) but prints the registered 11",
        [
            (
                '    r = census(clean_plans, skill([row("tools/round-67/a.py"),\n'
                '                                   row("tools/round-50/a.py"),\n'
                '                                   row("tools/round-99/gone.py")]),\n'
                '               execs | {"tools/round-99/other.py"})\n'
                '    cases.append(("row-absent", r["row_absent"] == ["tools/round-99/gone.py"]\n'
                '                  and r["mismatches"] == 1))\n',
                "    # M6: row-absent case dropped\n",
            ),
            (
                '    print(json.dumps({"selftest": TOOL, "cases": len(cases), "failed": failed,\n',
                '    print(json.dumps({"selftest": TOOL, "cases": len(REGISTERED_CASES), "failed": failed,\n',
            ),
        ],
    ),
}


def run(argv: list[str], cwd: pathlib.Path) -> tuple[int, str, str]:
    p = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


def git_fixture(name: str, plans: dict[str, str], skill_rows: list[str],
                tools: list[str]) -> pathlib.Path:
    root = (FIX / name).resolve()
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    (root / "plans").mkdir()
    for rel, text in plans.items():
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
    for rel in tools:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("# fixture tool\n", encoding="utf-8")
    skill = "\n".join([
        "<!-- instrument-registry v2 -->",
        "",
        "| tool | gate or probe - purpose | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |",
        "|---|---|---|---|---|---|---|",
        *skill_rows,
        "",
        "<!-- /instrument-registry -->",
        "",
    ])
    (root / "SKILL.md").write_text(skill, encoding="utf-8")
    run(["git", "init", "-q", "-b", "main"], root)
    top = run(["git", "rev-parse", "--show-toplevel"], root)[1].strip()
    assert pathlib.Path(top).resolve() == root, (top, root)
    run(["git", "-c", "user.name=mut", "-c", "user.email=mut@localhost",
         "add", "-A"], root)
    rc, out, err = run(["git", "-c", "user.name=mut", "-c", "user.email=mut@localhost",
                        "commit", "-q", "-m", "fixture " + name], root)
    assert rc == 0, err
    return root


def row(path: str, verdict: str = FULL) -> str:
    return f"| `{path}` | g | {verdict} | s | p | w | o |"


def build_fixtures() -> dict[str, pathlib.Path]:
    F = {}
    F["foreign"] = git_fixture(
        "foreign",
        {"plans/round-67-claims.md":
         "uses `tools/round-67/reg.py` and `tools/round-50/foreign.py`\n"},
        [row("tools/round-67/reg.py")],
        ["tools/round-67/reg.py", "tools/round-50/foreign.py"],
    )
    F["thin"] = git_fixture(
        "thin",
        {"plans/round-67-claims.md": "uses `tools/round-67/reg.py`\n"},
        [row("tools/round-67/reg.py", "0=met; 1=not met")],
        ["tools/round-67/reg.py"],
    )
    F["duplicate"] = git_fixture(
        "duplicate",
        {"plans/round-67-claims.md": "uses `tools/round-67/reg.py`\n"},
        [row("tools/round-67/reg.py"), row("tools/round-67/reg.py")],
        ["tools/round-67/reg.py"],
    )
    F["unregistered"] = git_fixture(
        "unregistered",
        {"plans/round-67-claims.md":
         "uses `tools/round-67/a.py` and `tools/round-67/b.py`\n"},
        [row("tools/round-67/a.py")],
        ["tools/round-67/a.py", "tools/round-67/b.py"],
    )
    return F


def score(copy: pathlib.Path, root: pathlib.Path, rev: str) -> dict:
    out = copy.with_suffix("").with_suffix(".receipt.json")
    rc, stdout, stderr = run([sys.executable, "-I", "-B", str(copy),
                              "--root", str(root), "--rev", rev,
                              "--json-out", str(out)], SCRATCH)
    res: dict = {"rc": rc, "stderr": stderr.strip()[:300]}
    try:
        data = json.loads(stdout)
        for k in ("mismatches", "scope_size", "registry_rows", "unregistered",
                  "duplicate_rows", "thin", "row_absent", "ok"):
            res[k] = data.get(k)
    except json.JSONDecodeError:
        res["stdout"] = stdout.strip()[:300]
    return res


def selftest(copy: pathlib.Path) -> dict:
    rc, stdout, stderr = run([sys.executable, "-I", "-B", str(copy), "--selftest"], SCRATCH)
    try:
        data = json.loads(stdout)
    except json.JSONDecodeError:
        return {"rc": rc, "raw": stdout.strip()[:300], "stderr": stderr.strip()[:300]}
    return {"rc": rc, "cases": data.get("cases"), "failed": data.get("failed"),
            "ok": data.get("ok")}


def main() -> int:
    MUT.mkdir(parents=True, exist_ok=True)
    WAVE.mkdir(parents=True, exist_ok=True)
    pristine_bytes = PRISTINE.read_bytes()
    pristine_sha = hashlib.sha256(pristine_bytes).hexdigest()
    out: dict = {"pristine_sha256": pristine_sha, "base_rev": BASE_REV, "mutants": {}}

    fixtures = build_fixtures()
    out["fixtures"] = {k: str(v) for k, v in fixtures.items()}

    sources = {"PRISTINE": (pristine_bytes, PRISTINE)}
    for mid, (desc, edits) in MUTANTS.items():
        text = pristine_bytes.decode("utf-8")
        for old, new in edits:
            n = text.count(old)
            assert n == 1, f"{mid}: anchor count {n} for {old[:60]!r}"
            text = text.replace(old, new)
        dst = MUT / f"{mid}.py"
        dst.write_text(text, encoding="utf-8")
        sources[mid] = (dst.read_bytes(), dst)

    for name, (blob, path) in sources.items():
        entry = {"sha256": hashlib.sha256(blob).hexdigest(),
                 "path": str(path), "selftest": selftest(path),
                 "fixtures": {}, "base": {}}
        if name != "PRISTINE":
            entry["mutation"] = MUTANTS[name][0]
        for fname, froot in fixtures.items():
            entry["fixtures"][fname] = score(path, froot, "main")
        entry["base"] = score(path, LANE, BASE_REV)
        out["mutants"][name] = entry

    after = PRISTINE.read_bytes()
    out["pristine_after_sha256"] = hashlib.sha256(after).hexdigest()
    out["pristine_unchanged"] = after == pristine_bytes
    (WAVE / "mutants.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n",
                                       encoding="utf-8")
    print(json.dumps(out, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
