import json, os, shutil, subprocess, sys
S = os.environ["S"]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
B = "2cf0b7ff93c698809bed321f7338276a22d6beb9"
ENV = dict(os.environ, TMPDIR=os.path.join(S, "tmp"))
REC = os.path.join(S, "receipts"); WORK = os.path.join(S, "work"); FX = os.path.join(S, "fx")
for d in (REC, WORK, FX, os.path.join(S, "tmp")):
    os.makedirs(d, exist_ok=True)
C1 = os.path.join(LANE, "tools/round-86/record-agreement.py")
C2 = os.path.join(LANE, "tools/round-86/gate-registry.py")
REG_CLOSE = "<!-- /instrument-registry -->"

def blob(path, rev=B):
    return subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], capture_output=True, check=True).stdout.decode()

SOURCES = blob("corpus/SOURCES.md")
MC = blob("tools/round-84/mutation-closure.py")
CARD = blob("SCORECARD.md")
SKILL = blob("SKILL.md")
PB = blob("tools/round-85/predicate-bind.py")
CLAIMS85 = blob(".ufo/waves/round-85/claims.json")
RCPT84 = blob(".ufo/waves/round-84/l1/scores/coverage-selfcheck.json")
GATE_FILE = blob("tools/round-86/gate-registry.py", "HEAD")
R85_RECEIPT = '{"rev": "%s", "ok": true}\n' % ("0" * 40)
EXIT2 = '#!/usr/bin/env python3\nimport sys\nsys.exit(2)\n'
R84 = ".ufo/waves/round-84/l1/scores/coverage-selfcheck.json"
R85 = ".ufo/waves/round-85/l1/scores/coverage-selfcheck.json"

def git(D, *a, check=True):
    return subprocess.run(["git", "-C", D, *a], capture_output=True, text=True, check=check)

def write(D, files):
    for rel, text in files.items():
        p = os.path.join(D, rel); os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as f:
            f.write(text)

def repo(name, files):
    D = os.path.join(FX, name)
    shutil.rmtree(D, ignore_errors=True); os.makedirs(D)
    git(D, "init", "-q")
    write(D, files)
    return D

def commit(D, msg):
    top = git(D, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(D), (top, D)
    git(D, "add", "-A")
    subprocess.run(["git", "-C", D, "-c", "user.name=critic", "-c", "user.email=critic@invalid",
                    "commit", "-q", "-m", msg], check=True, capture_output=True)
    return git(D, "rev-parse", "HEAD").stdout.strip()

def c1(D, rev, tag):
    out = os.path.join(REC, tag + ".json")
    p = subprocess.run([sys.executable, "-I", "-B", C1, "--root", D, "--rev", rev, "--json-out", out],
                       capture_output=True, text=True, env=ENV)
    return p.returncode, json.load(open(out))

def c2(D, rev, tag):
    out = os.path.join(REC, tag + ".json"); work = os.path.join(WORK, tag); os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-I", "-B", C2, "--root", D, "--rev", rev, "--work", work,
                        "--json-out", out], capture_output=True, text=True, env=ENV)
    return p.returncode, json.load(open(out))

RESULTS = []
def rec(tag, expect, code, d):
    atoms = {a["id"]: {"ok": a["ok"], "detail": a["detail"]} for a in d["atoms"]}
    RESULTS.append({"fixture": tag, "expect": expect, "exit": code, "agreed": f'{d["agreed"]}/{d["total"]}',
                    "mismatches": d["mismatches"], "atoms": atoms})
    print(f'{tag:44s} exit={code} agreed={d["agreed"]}/{d["total"]} mismatches={d["mismatches"]}  | expect: {expect}')

# ---------- C1 fixture builders
def mc_word(word):
    old = "an absent declared case is inconclusive, never a pass"
    assert MC.count(old) == 1
    return MC.replace(old, f"an absent declared case is {word}, never a pass")

def sup_row(rid, count, ids):
    return (f"| {rid} | superseding row — S303 correction (fixture) | docs | A | x | x | "
            f"supersedes S303 — count {count} ({'/'.join(ids)}) | rejected | 2026-11-04 | on-release | "
            f"corpus/lessons/round-86.md |")

CORRECT = ["S079", "S080", "S083", "S090", "S092", "S119", "S123"]

def with_rows(src, *rows):
    return src.rstrip("\n") + "\n" + "\n".join(rows) + "\n"

def s079_rewrite(src):
    out = []
    for line in src.split("\n"):
        if line.startswith("| S079 |"):
            assert "rea-agents-6.5.0.tgz" in line
            line = line.replace("rea-agents-6.5.0.tgz", "rea-agents-6.5.0")
        out.append(line)
    return "\n".join(out)

def card_variant(card, remove_history, repath, round_to=None):
    out, seen = [], False
    for line in card.split("\n"):
        if line.startswith("| coverage |"):
            if seen and remove_history:
                continue
            if not seen:
                seen = True
                if repath:
                    assert "round-84/l1/scores/coverage-selfcheck.json" in line
                    line = line.replace("round-84/l1/scores/coverage-selfcheck.json",
                                        "round-85/l1/scores/coverage-selfcheck.json")
                if round_to is not None:
                    assert "| 85 (self-assessment" in line
                    line = line.replace("| 85 (self-assessment", f"| {round_to} (self-assessment")
        out.append(line)
    return "\n".join(out)

def c1_files(src=SOURCES, mc=MC, card=CARD, r85=False):
    f = {"corpus/SOURCES.md": src, "tools/round-84/mutation-closure.py": mc, "SCORECARD.md": card, R84: RCPT84}
    if r85:
        f[R85] = R85_RECEIPT
    return f

# ---------- C2 fixture builders
GOOD = ("| `tools/round-85/predicate-bind.py` | gate — fixture row (R86-C2 check) | 0=clean; 1=flagged; 2=unreadable | "
        "`python3 -I -B tools/round-85/predicate-bind.py --selftest` — exit 0 | `.ufo/waves/round-85/claims.json` | "
        "none (read-only) | kaidoku-r85 |")
DUP6 = ("| `tools/round-85/predicate-bind.py` | dup malformed row | 0=; 1=; 2= | "
        "`python3 -I -B tools/round-85/predicate-bind.py --selftest` — exit 0 | `.ufo/waves/round-85/claims.json` | kaidoku-r85 |")

def skill_with(*rows):
    assert SKILL.count(REG_CLOSE) == 1
    return SKILL.replace(REG_CLOSE, "".join(r + "\n" for r in rows) + REG_CLOSE, 1)

def swap(row, old, new):
    assert row.count(old) == 1, (old, row)
    return row.replace(old, new)

def c2_files(skill, pb=PB, claims=CLAIMS85, extra=None):
    f = {"SKILL.md": skill, "tools/round-85/predicate-bind.py": pb, ".ufo/waves/round-85/claims.json": claims}
    if extra:
        f.update(extra)
    return f

PRINT_TAGS = []

# ================= C1 scenarios
print("== R86-C1 record agreement (3 atoms)")
D = repo("c1-base-sanity", c1_files()); s = commit(D, "base"); rec("c1-base-sanity", "0/3 (pre receipt reproduces)", *c1(D, s, "c1-base-sanity"))
D = repo("c1-a2-survived", c1_files(mc=mc_word("survived"))); s = commit(D, "a2 survived")
rec("c1-a2-survived (plan's status word)", "A2 green", *c1(D, s, "c1-a2-survived"))
D = repo("c1-a2-survivor", c1_files(mc=mc_word("a survivor"))); s = commit(D, "a2 survivor")
rec("c1-a2-survivor (noun, not the status)", "A2 green (falsifier)", *c1(D, s, "c1-a2-survivor"))
D = repo("c1-a2-surviving", c1_files(mc=mc_word("surviving"))); s = commit(D, "a2 surviving")
rec("c1-a2-surviving (not the status)", "A2 green (falsifier)", *c1(D, s, "c1-a2-surviving"))
D = repo("c1-a2-killed", c1_files(mc=mc_word("killed"))); s = commit(D, "a2 killed")
rec("c1-a2-killed (wrong status)", "A2 red", *c1(D, s, "c1-a2-killed"))

D = repo("c1-a3-history-kept-r85", c1_files(card=card_variant(CARD, False, True), r85=True)); s = commit(D, "a3 kept")
rec("c1-a3-history-kept + round-85 receipt", "A3 red (found 23)", *c1(D, s, "c1-a3-history-kept-r85"))
D = repo("c1-a3-history-removed-r85", c1_files(card=card_variant(CARD, True, True), r85=True)); s = commit(D, "a3 removed")
rec("c1-a3-22-history-rows-deleted + r85 receipt(rev=0s)", "A3 green (falsifier: needs history deleted; fabricated rev)", *c1(D, s, "c1-a3-history-removed-r85"))
D = repo("c1-a3-history-removed-basepaths", c1_files(card=card_variant(CARD, True, False))); s = commit(D, "a3 base paths")
rec("c1-a3-history-removed, row unchanged (plan's cause)", "A3 red (predates r85)", *c1(D, s, "c1-a3-history-removed-basepaths"))
D = repo("c1-a3-round-rewrite-0", c1_files(card=card_variant(CARD, True, False, round_to=0))); s = commit(D, "a3 round0")
rec("c1-a3-claimed-round rewritten 85->0", "A3 green (falsifier: round cell rewritten)", *c1(D, s, "c1-a3-round-rewrite-0"))

D = repo("c1-a1-genuine", c1_files(src=with_rows(SOURCES, sup_row("S305", 7, CORRECT)))); s = commit(D, "a1 genuine")
rec("c1-a1-genuine (count 7, 7 ids)", "A1 green", *c1(D, s, "c1-a1-genuine"))
D = repo("c1-a1-s079-rewrite", c1_files(src=with_rows(s079_rewrite(SOURCES), sup_row("S305", 6, CORRECT[1:])))); s = commit(D, "a1 rewrite")
rec("c1-a1-S079 source rewritten, count 6", "A1 green (falsifier: registry is its own oracle)", *c1(D, s, "c1-a1-s079-rewrite"))
D = repo("c1-a1-stale-five", c1_files(src=with_rows(SOURCES, sup_row("S305", 5, ["S083", "S090", "S092", "S119", "S123"])))); s = commit(D, "a1 five")
rec("c1-a1-count 5 (S303's own stale claim)", "A1 red", *c1(D, s, "c1-a1-stale-five"))
D = repo("c1-a1-wrong-first", c1_files(src=with_rows(SOURCES, sup_row("S305", 3, ["S083", "S090", "S119"]), sup_row("S306", 7, CORRECT)))); s = commit(D, "a1 wrong first")
rec("c1-a1-wrong superseder first, correct last", "A1 green (falsifier: 'newest' = file order)", *c1(D, s, "c1-a1-wrong-first"))
D = repo("c1-a1-correct-first", c1_files(src=with_rows(SOURCES, sup_row("S305", 7, CORRECT), sup_row("S306", 3, ["S083", "S090", "S119"])))); s = commit(D, "a1 correct first")
rec("c1-a1-correct first, wrong superseder last", "A1 red", *c1(D, s, "c1-a1-correct-first"))

# ================= C2 scenarios
print("== R86-C2 gate registration (5 atoms)")
D = repo("c2-base-sanity", c2_files(SKILL)); s = commit(D, "base"); rec("c2-base-sanity", "0/5 (pre receipt reproduces)", *c2(D, s, "c2-base-sanity"))
D = repo("c2-genuine", c2_files(skill_with(GOOD))); s = commit(D, "genuine row")
rec("c2-genuine (real tool, honest row)", "5/5 green", *c2(D, s, "c2-genuine"))
D = repo("c2-foreign-cmd", c2_files(skill_with(swap(GOOD, "`python3 -I -B tools/round-85/predicate-bind.py --selftest` — exit 0",
                                                     "`python3 -c \"import sys; sys.exit(0)\"` — exit 0")))); s = commit(D, "foreign cmd")
rec("c2-self-test cell names no tool path (python -c)", "G3 green (falsifier)", *c2(D, s, "c2-foreign-cmd"))
D = repo("c2-gate-registry-cmd", c2_files(skill_with(swap(GOOD, "`python3 -I -B tools/round-85/predicate-bind.py --selftest` — exit 0",
                                                          "`python3 -I -B tools/round-86/gate-registry.py --selftest` — exit 0")),
                                          extra={"tools/round-86/gate-registry.py": GATE_FILE})); s = commit(D, "other tool cmd")
rec("c2-self-test cell names the OTHER counter's selftest", "G3 green (falsifier)", *c2(D, s, "c2-gate-registry-cmd"))
D = repo("c2-dup-malformed", c2_files(skill_with(GOOD, DUP6))); s = commit(D, "dup")
rec("c2-second row for tool, 6 cells (malformed)", "G1 green (falsifier: two rows exist)", *c2(D, s, "c2-dup-malformed"))
D = repo("c2-pin-partial", c2_files(skill_with(swap(GOOD, "`.ufo/waves/round-85/claims.json`",
                                                    "`.ufo/waves/round-85/claims.json` and `.ufo/waves/round-85/absent.json`")))); s = commit(D, "pin partial")
rec("c2-pins: one present, one absent", "G4 green per atom text 'at least one' (counter red)", *c2(D, s, "c2-pin-partial"))
D = repo("c2-map-substring", c2_files(skill_with(swap(GOOD, "0=clean; 1=flagged; 2=unreadable", "10=clean; 1=flagged; 2=unreadable")))); s = commit(D, "map")
rec("c2-verdict map with '10=' (no real 0=)", "G2 green (falsifier: substring '0=')", *c2(D, s, "c2-map-substring"))
D = repo("c2-owner-backtick", c2_files(skill_with(swap(GOOD, "| kaidoku-r85 |", "| `kaidoku-r85` |")))); s = commit(D, "owner")
rec("c2-owner cell with backticks", "G5 red (strictness/ambiguity)", *c2(D, s, "c2-owner-backtick"))

# worktree vs --rev: committed tool red, worktree tool green
D = repo("c2-worktree-green", c2_files(skill_with(GOOD), pb=EXIT2)); rev_red = commit(D, "committed tool exit 2")
committed_rc = subprocess.run([sys.executable, "-I", "-B", "-c", EXIT2, "--selftest"], capture_output=True).returncode
write(D, {"tools/round-85/predicate-bind.py": PB})
rec(f"c2-worktree-green (committed tool exits {committed_rc}, worktree real)", "G2 green at --rev (falsifier: worktree executed)", *c2(D, rev_red, "c2-worktree-green"))
D = repo("c2-worktree-red", c2_files(skill_with(GOOD), pb=PB)); rev_green = commit(D, "committed good tool")
write(D, {"tools/round-85/predicate-bind.py": EXIT2})
rec("c2-worktree-red (committed real, worktree exit 2)", "G2 red at --rev (shows worktree read)", *c2(D, rev_green, "c2-worktree-red"))

# ================= separability
print("== separability: C1 at C2-only commit, C2 at C1-only commit")
D = repo("sep", c1_files() | {} if False else {**c1_files(), "SKILL.md": SKILL, "tools/round-85/predicate-bind.py": PB, ".ufo/waves/round-85/claims.json": CLAIMS85})
s1 = commit(D, "sep base")
write(D, {"SKILL.md": skill_with(GOOD)}); s2 = commit(D, "C2 only: registry row")
write(D, {"corpus/SOURCES.md": with_rows(SOURCES, sup_row("S305", 7, CORRECT)), "tools/round-84/mutation-closure.py": mc_word("survived")})
s3 = commit(D, "C1 only: A1 + A2 edits")
rec("sep C1 @ base (C2 unlanded)", "C1 0/3", *c1(D, s1, "sep-c1-s1"))
rec("sep C1 @ C2-only landing (C1 unchanged)", "C1 identical to base", *c1(D, s2, "sep-c1-s2"))
rec("sep C1 @ C1-only edits (A1,A2 green; A3 red)", "C1 moves on its own axis", *c1(D, s3, "sep-c1-s3"))
rec("sep C2 @ base (C1 unlanded)", "C2 0/5", *c2(D, s1, "sep-c2-s1"))
rec("sep C2 @ C2-only landing", "C2 5/5", *c2(D, s2, "sep-c2-s2"))
rec("sep C2 @ C1 edits added (C2 unchanged)", "C2 identical to C2-only landing", *c2(D, s3, "sep-c2-s3"))

with open(os.path.join(REC, "fixture-summary.json"), "w") as f:
    json.dump(RESULTS, f, indent=1, sort_keys=True)
print("WROTE", os.path.join(REC, "fixture-summary.json"), len(RESULTS), "fixtures")
