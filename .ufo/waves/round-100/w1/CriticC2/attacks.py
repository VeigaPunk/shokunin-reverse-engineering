import subprocess, os, sys, json
S = "/fast/scratch/hyaku/kaidoku-r100/CriticC2"
A2 = "cbd224ef9b9d2271f415d823bdc4d1e70a0d281c"
REC = "tools/round-47/record.py"
ATT = [
 ("ctl-words-only", [
   ("10 cases, `RECORD_SELFTEST: cases=10 failures=0`", "ten cases, `RECORD_SELFTEST: failures=0`"),
   ("this cell said 9 cases at `5017e1f7`", "this cell said nine cases at `5017e1f7`")]),
 ("f1-second-false-count-same-cell", [
   ("are required even for --selftest", "are required even for --selftest; a later re-run on 2026-11-05 printed 15 cases")]),
 ("f2-words-false-digits-later", [
   ("10 cases, `RECORD_SELFTEST: cases=10 failures=0`", "fifteen cases, `RECORD_SELFTEST: cases=10 failures=0`")]),
 ("f3-wrong-command-and-exit", [
   ("`python3 -I -B tools/round-47/record.py --selftest --root . --rev <R>`: 10 cases", "`python3 -I -B tools/round-47/record.py --run-battery --rev <R>`: 10 cases"),
   ("exit 0 on 2026-11-05 (re-run by tools/round-100/registry-selftest-truth.py; this cell said 9", "exit 2 on 2026-11-05 (re-run by tools/round-100/registry-selftest-truth.py; this cell said 9")]),
 ("f4-verdict-and-scope-false", [
   ("0=met; 1=not met, mismatches and bad corrections listed", "0=not met; 1=met, mismatches and bad corrections listed"),
   ("not pinned by the block | none — writes only the `--json-out` receipt", "not pinned by the block | none — writes SCORECARD.md in place, then the `--json-out` receipt")]),
 ("f5-count-in-purpose-cell", [
   ("`--control` the three do-nothing controls", "`--control` the three do-nothing controls; `--selftest` prints 4 cases")]),
 ("f6-prose-outside-markers", [
   ("<!-- /instrument-registry -->", "<!-- /instrument-registry -->\n\nNote: tools/round-47/record.py runs 12 cases.")]),
 ("f7-mangled-key-second-row", [
   ("| `tools/round-47/record.py` | gate", "| `tools/round-47/record.py` (copy) | gate - copy | 0=met | `python3 -I -B tools/round-47/record.py --selftest` 3 cases | none | none | kaidoku |\n| `tools/round-47/record.py` | gate")]),
]
ORDER = ["f1-second-false-count-same-cell", "f3-wrong-command-and-exit", "f2-words-false-digits-later", "f4-verdict-and-scope-false", "f5-count-in-purpose-cell", "f6-prose-outside-markers", "f7-mangled-key-second-row"]
D = dict(ATT)
ALL = [e for n in ORDER for e in D[n]]
ATT.append(("f8-all-admitted", ALL))
out = {}
ONLY = sys.argv[1:]
for name, edits in ATT:
    if ONLY and name not in ONLY: continue
    fx = os.path.join(S, "fx", name)
    subprocess.run(["rm", "-rf", fx]); os.makedirs(os.path.dirname(fx), exist_ok=True)
    subprocess.run(["git", "clone", "-q", "--shared", os.path.join(S, "clone"), fx], check=True)
    subprocess.run(["git", "-C", fx, "checkout", "-q", "--detach", A2], check=True)
    top = subprocess.run(["git", "-C", fx, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(fx), top
    p = os.path.join(fx, "SKILL.md"); t = open(p, encoding="utf-8").read()
    for old, new in edits:
        n = t.count(old)
        assert n == 1, (name, old[:60], n)
        t = t.replace(old, new)
    open(p, "w", encoding="utf-8").write(t)
    subprocess.run(["git", "-C", fx, "add", "SKILL.md"], check=True)
    subprocess.run(["git", "-C", fx, "-c", "user.name=CriticC2", "-c", "user.email=critic@local", "-c", "commit.gpgsign=false",
                    "commit", "-q", "-m", "fixture " + name], check=True)
    rev = subprocess.run(["git", "-C", fx, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    out[name] = rev
    print(name, rev, "edits=%d" % len(edits))
print(out)
