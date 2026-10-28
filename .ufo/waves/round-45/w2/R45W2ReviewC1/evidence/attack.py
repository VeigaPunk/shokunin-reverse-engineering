#!/usr/bin/env python3
"""R45W2ReviewC1 — falsification fixtures for tools/round-45/c1-counter.py.

Every fixture is a throwaway git repo under $S. The counter under test is the
byte-frozen copy at $S/c1-counter.py (sha256 checked against
`git show f762b72:tools/round-45/c1-counter.py`).
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

S = os.environ["S"]
COUNTER = os.path.join(S, "c1-counter.py")
OUT = os.path.join(S, "results")
os.makedirs(OUT, exist_ok=True)

MARKER = "<!-- freeze-integrity-table v1 -->"
PREFLIGHT = "tools/round-45/frozen-path-preflight.py"
CRAFT_HEAD = "# SKILL\n\n## Queue-drain craft (test)\n\n"
GOOD_HEADER = "| trigger | arm | exit | receipt |\n|---|---|---|---|\n"
GOOD_ROW = "| post-freeze commit touches a frozen path | commit arm | 1 | `--json-out` receipt |\n"

STUB_OK = ("#!/usr/bin/env python3\n"
           "import sys\n"
           "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\n"
           "sys.exit(0)\n")
STUB_RED = ("#!/usr/bin/env python3\n"
            "import sys\n"
            "print('PREFLIGHT_SELFTEST: cases=11 failures=1')\n"
            "sys.exit(1)\n")


def git(d, *args):
    return subprocess.run(["git", "-C", d, *args], capture_output=True, text=True)


def make_repo(d, files):
    git(d, "init", "-q")
    git(d, "config", "user.email", "r45w2@selftest")
    git(d, "config", "user.name", "r45 w2 reviewer")
    for p, text in files.items():
        full = os.path.join(d, p)
        parent = os.path.dirname(full)
        if parent:
            os.makedirs(parent, exist_ok=True)
        if isinstance(text, tuple) and text[0] == "symlink":
            os.symlink(text[1], full)
        else:
            with open(full, "w") as fh:
                fh.write(text)
    git(d, "add", "-A")
    git(d, "commit", "-q", "-m", "fixture")
    top = git(d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    return git(d, "rev-parse", "HEAD").stdout.strip()


def corpus():
    return {
        "corpus/lessons/round-44.md": "l1\n" * 60,
        "corpus/lessons/round-44-verifier-spotcheck.md": "s1\n" * 40,
        "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md": "k1\n" * 30,
        "plans/round-45-claims.md": "claims\n" * 10,
    }


def plain(n, start=1):
    return "".join(f"- **{i}. Plain rule {i}.** body\n" for i in range(start, start + n))


def good_block(label="22", refs=None, extra="", tail=""):
    refs = refs if refs is not None else (
        "corpus/lessons/round-44.md:38", "plans/round-45-claims.md:1",
        "corpus/lessons/round-44-verifier-spotcheck.md:12",
        "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9")
    b = f"- **{label}. Freeze integrity.** " + MARKER + " S140 " + PREFLIGHT + "\n\n"
    b += extra
    b += GOOD_HEADER + GOOD_ROW * 8
    b += "\n  Refs: " + ", ".join(refs) + "\n\n"
    b += tail
    return b


RESULTS = []


def run(name, attacks, expect, skill, preflight=STUB_OK, files=None, env_extra=None,
        freeze_mutator=None, cwd=None, extra_argv=()):
    d = tempfile.mkdtemp(dir=S, prefix="fx-")
    allf = {"SKILL.md": skill, PREFLIGHT: preflight}
    allf.update(corpus())
    if files:
        allf.update(files)
    f = make_repo(d, allf)
    rev = f
    if freeze_mutator:
        rev = freeze_mutator(d, f)
    out_json = os.path.join(OUT, name + ".json")
    argv = [sys.executable, "-I", "-B", COUNTER, "--root", d,
            "--freeze", f, "--rev", rev, "--json-out", out_json, *extra_argv]
    env = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
    if env_extra:
        env.update(env_extra)
    t0 = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    proc = subprocess.run(argv, capture_output=True, text=True, env=env,
                          cwd=cwd or d, timeout=300)
    sha = hashlib.sha256(proc.stdout.encode()).hexdigest()
    receipt = None
    try:
        receipt = json.loads(proc.stdout)
    except Exception:
        pass
    rec = {
        "case": name, "attacks": attacks, "expect": expect, "exit": proc.returncode,
        "stdout_sha256": sha, "utc": t0,
        "argv": " ".join(argv),
        "met_target": (receipt or {}).get("met_target"),
        "failing": (receipt or {}).get("failing"),
        "receipt_subset": {k: (receipt or {}).get(k) for k in
                           ("rule_blocks", "block22_present", "block22_rows",
                            "block22_refs", "block22_unresolved_citations",
                            "block22_cites", "block22_header_ok",
                            "preflight_selftest", "interpreter_present")},
        "stderr_tail": proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "",
        "json_out_written": os.path.exists(out_json),
    }
    rec["ok"] = rec["exit"] == expect
    RESULTS.append(rec)
    print(json.dumps({k: rec[k] for k in ("case", "expect", "exit", "ok", "met_target")}))
    return rec


# ---------------------------------------------------------------- baseline
def case_base():
    run("A0-base-green", "A1-A5 baseline (fixture the counter's own green case mirrors)",
        0, CRAFT_HEAD + plain(21) + good_block())


# ------------------------------------------------- A1 fenced `## ` in a body
def case_a1_fragile():
    """A rule body holding a fenced block with a `## ` line, before block 22."""
    fence = "  ```markdown\n## Not a section heading, an example\n  ```\n"
    skill = CRAFT_HEAD + plain(4) + f"- **5. Plain rule 5.** body\n{fence}" + plain(16, 6) + good_block()
    # human count of `^- **` blocks inside the section = 22; counter should too
    run("A1a-fence-before-block22", "A1: split stability (fragile direction)",
        1, skill)


def case_a1_false_pass():
    """A second marker block hidden past a fenced `## ` inside block 22."""
    fence = "\n  ```markdown\n## Worked example heading\n  ```\n"
    hidden = (f"- **23. Duplicate rule.** {MARKER} S140 {PREFLIGHT}\n\n"
              + GOOD_HEADER + GOOD_ROW * 2 + "\n")
    skill = CRAFT_HEAD + plain(21) + good_block(tail=fence + hidden)
    run("A1b-fence-hides-second-marker", "A1: split stability (false-pass direction)",
        0, skill)


def case_a1_crash():
    """Heading without a trailing qualifier: craft_blocks indexes [1] -> IndexError."""
    skill = "# SKILL\n\n## Queue-drain craft\n\n" + plain(21) + good_block()
    run("A1c-heading-indexerror", "A1: split stability / exit-code semantics",
        1, skill)


# ------------------------------------------------- A2 first table vs later tables
def case_a2_later_not_first():
    """Later table cannot be graded: first table wins -> false negative."""
    first = "| note |\n|---|\n| x |\n| y |\n\n"
    skill = CRAFT_HEAD + plain(21) + good_block(extra=first)
    run("A2a-first-table-decoy", "A2: which table is graded", 1, skill)


def case_a2_concat_false_pass():
    """Two tables concatenated: foreign rows inflate block22_rows to >= 8."""
    first = GOOD_HEADER + GOOD_ROW * 2
    second = ("\n| rank | item | 1 | note |\n|---|---|---|---|\n"
              + "".join(f"| r{i} | item {i} | {i % 3} | note |\n" for i in range(6)))
    skill = CRAFT_HEAD + plain(21) + good_block(extra="")  # good_block builds table
    # rebuild: block = header + 2 decision rows + second table
    blk = f"- **22. Freeze integrity.** {MARKER} S140 {PREFLIGHT}\n\n"
    blk += first + second
    blk += "\n  Refs: corpus/lessons/round-44.md:38, plans/round-45-claims.md:1, " \
           "corpus/lessons/round-44-verifier-spotcheck.md:12, " \
           "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9\n\n"
    skill = CRAFT_HEAD + plain(21) + blk
    run("A2b-concat-two-tables", "A2: row counting across concatenated tables", 0, skill)


def case_a2_example_table():
    """Example table first (8 rows), decision table second (2 rows) -> green."""
    example = GOOD_HEADER + GOOD_ROW * 8
    decision = ("\n| trigger | arm | exit | receipt |\n|---|---|---|---|\n"
                "| a | b | 0 | c |\n| d | e | depends | f |\n")
    blk = f"- **22. Freeze integrity.** {MARKER} S140 {PREFLIGHT}\n\n"
    blk += "Worked examples:\n\n" + example + "\nThe decision table:\n" + decision
    blk += "\n  Refs: corpus/lessons/round-44.md:38, plans/round-45-claims.md:1, " \
           "corpus/lessons/round-44-verifier-spotcheck.md:12, " \
           "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9\n\n"
    skill = CRAFT_HEAD + plain(21) + blk
    run("A2c-example-table-first", "A2: real decision table is the second one", 0, skill)


# ------------------------------------------------- A3 header substring match
def case_a3_single_cell():
    head = "| triggeralarmexitreceipt | note | a | b |\n|---|---|---|---|\n"
    rows = "".join("| 1 | n | x | y |\n" for _ in range(8))
    blk = f"- **22. Freeze integrity.** {MARKER} S140 {PREFLIGHT}\n\n" + head + rows
    blk += "\n  Refs: corpus/lessons/round-44.md:38, plans/round-45-claims.md:1, " \
           "corpus/lessons/round-44-verifier-spotcheck.md:12, " \
           "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9\n\n"
    skill = CRAFT_HEAD + plain(21) + blk
    run("A3a-one-cell-all-substrings", "A3: header check via substring", 0, skill)


def case_a3_realistic_near_miss():
    head = "| triggering event | alarm | exit-status | receipts |\n|---|---|---|---|\n"
    rows = "".join("| t | a | %d | r |\n" % (i % 3) for i in range(8))
    blk = f"- **22. Freeze integrity.** {MARKER} S140 {PREFLIGHT}\n\n" + head + rows
    blk += "\n  Refs: corpus/lessons/round-44.md:38, plans/round-45-claims.md:1, " \
           "corpus/lessons/round-44-verifier-spotcheck.md:12, " \
           "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9\n\n"
    skill = CRAFT_HEAD + plain(21) + blk
    run("A3b-near-miss-headers", "A3: header check via substring (realistic)", 0, skill)


# ------------------------------------------------- A4 REF resolution
def case_a4_duplicate_refs():
    skill = CRAFT_HEAD + plain(21) + good_block(
        refs=("corpus/lessons/round-44.md:38",) * 4)
    run("A4a-duplicate-refs", "A4: refs>=4 by repetition", 0, skill)


def case_a4_unmatched_classes():
    refs = ("corpus/lessons/round-44.md:38", "plans/round-45-claims.md:1",
            "corpus/lessons/round-44-verifier-spotcheck.md:12",
            "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9",
            "corpus/SOURCES.md:9999", "SKILL.md:9999",
            "tools/round-45/c1-counter.py:9999")
    run("A4b-unmatched-citation-classes", "A4: unchecked citation classes", 0,
        CRAFT_HEAD + plain(21) + good_block(refs=refs))


def case_a4_suffix_path():
    refs = ("corpus/lessons/round-44.md:38", "plans/round-45-claims.md:1",
            "corpus/lessons/round-44-verifier-spotcheck.md:12",
            "plans/round-45-claims.md.bak:9999")
    run("A4c-bak-suffix-ref", "A4: regex prefix match swallows out-of-range ref", 0,
        CRAFT_HEAD + plain(21) + good_block(refs=refs))


def case_a4_in_file_range():
    refs = ("corpus/lessons/round-44.md:58-60", "corpus/lessons/round-44.md:59",
            "corpus/lessons/round-44-verifier-spotcheck.md:40",
            "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:30")
    run("A4d-in-file-but-wrong-content", "A4: bounds-only line check", 0,
        CRAFT_HEAD + plain(21) + good_block(refs=refs))


def case_a4_out_of_range():
    refs = ("corpus/lessons/round-44.md:61", "plans/round-45-claims.md:1",
            "corpus/lessons/round-44-verifier-spotcheck.md:12",
            "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9")
    run("A4e-out-of-range-caught", "A4: bounds check (holds direction)", 1,
        CRAFT_HEAD + plain(21) + good_block(refs=refs))


# ------------------------------------------------- A5 preflight execution
def case_a5_skill_cannot_execute():
    markerfile = os.path.join(S, "PWNED-skill")
    if os.path.exists(markerfile):
        os.remove(markerfile)
    blk = (f"- **22. Freeze integrity.** {MARKER} S140 {PREFLIGHT}\n\n"
           f"`__import__('subprocess').run(['touch', '{markerfile}'])`\n\n"
           + GOOD_HEADER + GOOD_ROW * 8
           + "\n  Refs: corpus/lessons/round-44.md:38, plans/round-45-claims.md:1, "
             "corpus/lessons/round-44-verifier-spotcheck.md:12, "
             "corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:9\n\n")
    rec = run("A5a-skill-not-executed", "A5: SKILL.md -> subprocess path", 0,
              CRAFT_HEAD + plain(21) + blk)
    rec["marker_created"] = os.path.exists(markerfile)


def case_a5_stub_passes():
    """Zero-test interpreter that prints the magic line and exits 0."""
    stub = ("#!/usr/bin/env python3\n"
            "import subprocess, sys\n"
            f"open('{S}/PWNED-preflight','w').write('executed')\n"
            "subprocess.run(['touch', '%s/PWNED-preflight-subprocess'])\n"
            "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\n"
            "sys.exit(0)\n")
    for f in (f"{S}/PWNED-preflight", f"{S}/PWNED-preflight-subprocess"):
        if os.path.exists(f):
            os.remove(f)
    rec = run("A5b-selfreported-selftest", "A5: selftest claim is stdout-only", 0,
              CRAFT_HEAD + plain(21) + good_block(), preflight=stub)
    rec["wrote_outside_work"] = os.path.exists(f"{S}/PWNED-preflight")
    rec["ran_subprocess"] = os.path.exists(f"{S}/PWNED-preflight-subprocess")


def case_a5_gates():
    stub10 = ("#!/usr/bin/env python3\nimport sys\n"
              "print('PREFLIGHT_SELFTEST: cases=10 failures=0')\nsys.exit(0)\n")
    run("A5c-cases-10", "A5: cases>=11 gate (holds direction)", 1,
        CRAFT_HEAD + plain(21) + good_block(), preflight=stub10)
    stub3 = ("#!/usr/bin/env python3\nimport sys\n"
             "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\nsys.exit(3)\n")
    run("A5d-exit-3", "A5: returncode gate (holds direction)", 1,
        CRAFT_HEAD + plain(21) + good_block(), preflight=stub3)


def case_a5_isolation():
    evil = os.path.join(S, "evil")
    os.makedirs(evil, exist_ok=True)
    with open(os.path.join(evil, "json.py"), "w") as fh:
        fh.write(f"open('{S}/PWNED-pythonpath','w').write('imported')\n")
    marker = f"{S}/PWNED-pythonpath"
    if os.path.exists(marker):
        os.remove(marker)
    rec = run("A5e-pythonpath-ignored", "A5: -I isolation", 0,
              CRAFT_HEAD + plain(21) + good_block(), env_extra={"PYTHONPATH": evil})
    rec["pythonpath_module_imported"] = os.path.exists(marker)


def case_a5_symlink():
    d = tempfile.mkdtemp(dir=S, prefix="fx-")
    allf = {"SKILL.md": CRAFT_HEAD + plain(21) + good_block(),
            PREFLIGHT: ("symlink", "/bin/echo")}
    allf.update(corpus())
    f = make_repo(d, allf)
    out_json = os.path.join(OUT, "A5f-symlink-interpreter.json")
    argv = [sys.executable, "-I", "-B", COUNTER, "--root", d, "--freeze", f,
            "--rev", f, "--json-out", out_json]
    proc = subprocess.run(argv, capture_output=True, text=True,
                          env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S), cwd=d)
    try:
        receipt = json.loads(proc.stdout)
    except Exception:
        receipt = {}
    rec = {"case": "A5f-symlink-interpreter", "attacks": "A5: symlink redirect",
           "expect": 1, "exit": proc.returncode, "ok": proc.returncode == 1,
           "met_target": receipt.get("met_target"),
           "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
           "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
           "argv": " ".join(argv),
           "receipt_subset": {"preflight_selftest": receipt.get("preflight_selftest")},
           "failing": receipt.get("failing")}
    RESULTS.append(rec)
    print(json.dumps({k: rec[k] for k in ("case", "expect", "exit", "ok")}))


def case_a5_attr_filter():
    """A smudge filter / eol attr must not alter the executed bytes."""
    d = tempfile.mkdtemp(dir=S, prefix="fx-")
    stub = ("#!/usr/bin/env python3\nimport sys\n"
            "print('PREFLIGHT_SELFTEST: cases=11 failures=0')\nsys.exit(0)\n")
    allf = {"SKILL.md": CRAFT_HEAD + plain(21) + good_block(),
            PREFLIGHT: stub,
            ".gitattributes": "*.py text eol=crlf filter=evil\n",
            }
    allf.update(corpus())
    # configure the filter to corrupt content on checkout/smudge
    d2 = d
    f = make_repo(d2, allf)
    git(d2, "config", "filter.evil.smudge", "tr 'P' 'X'")
    out_json = os.path.join(OUT, "A5g-attributes.json")
    argv = [sys.executable, "-I", "-B", COUNTER, "--root", d2, "--freeze", f,
            "--rev", f, "--json-out", out_json]
    proc = subprocess.run(argv, capture_output=True, text=True,
                          env=dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S), cwd=d2)
    try:
        receipt = json.loads(proc.stdout)
    except Exception:
        receipt = {}
    RESULTS.append({"case": "A5g-gitattributes-filter", "attacks": "A5: git show vs filters",
                    "expect": 0, "exit": proc.returncode, "ok": proc.returncode == 0,
                    "met_target": receipt.get("met_target"),
                    "stdout_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest(),
                    "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "argv": " ".join(argv)})
    print(json.dumps({"case": "A5g-gitattributes-filter", "exit": proc.returncode}))


def case_a5_shebang_ignored():
    """A non-python shebang in the blob does not matter: sys.executable runs it as py."""
    stub = "#!/bin/sh\necho nope\n"
    run("A5h-shell-shebang", "A5: executed as python regardless of shebang", 1,
        CRAFT_HEAD + plain(21) + good_block(), preflight=stub)


if __name__ == "__main__":
    only = sys.argv[1:] or None
    fns = [v for k, v in sorted(globals().items()) if k.startswith("case_")]
    for fn in fns:
        if only and not any(o in fn.__name__ for o in only):
            continue
        fn()
    with open(os.path.join(OUT, "results.json"), "w") as fh:
        json.dump(RESULTS, fh, indent=1)
    bad = [r for r in RESULTS if not r["ok"]]
    print(json.dumps({"cases": len(RESULTS), "unexpected": [r["case"] for r in bad]}))
