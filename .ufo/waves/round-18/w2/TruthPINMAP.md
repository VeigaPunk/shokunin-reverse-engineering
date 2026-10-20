PARTIAL

# TruthPINMAP: is R17-PINMAP discharged at REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`?

This is an author-side advisory seat (KaidokuR18.TruthPINMAP, wave 2), not outside verification. All anchors are `git show REV:path` line numbers unless another revision is named. I only read the lane. Probes ran in mkdtemp copies or clones with the origin remote removed, and all of them were deleted afterwards. I installed nothing; python3 3.14.8 and git 2.56.0 were already present. LANE = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Verdict

- **The substance HOLDS.** Every number, key set, quote and anchor in the two R17-PINMAP correction lines (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:204-205`, `SCORECARD.md:2438`) re-derives exactly from Git objects. The forward fix also holds on all 15 round-18 receipts (22/22 mid maps).
- **`routed-defects.py` does not prove the closure.**
  - Its R17-PINMAP checks still pass on a commit where:
    - the correction numbers are false;
    - the producer and validator are back at their `9011581` bytes;
    - the only "retained mid map" is a fabricated `{}`.
  - Its own `--selftest` exits 1 at REV. That makes a round-18 claim false (F1).
- **Is the closure deserved?** Yes, on substance. It rests on my independent re-derivation and on `receipt-validate.py --require-mid-maps` (15/15 r18 exit 0, 8/8 r17 red). It does not rest on the routed-defects count going 6 → 0.

## Re-derived claims (observation)

| Claim at REV | Re-derivation | Result |
|---|---|---|
| knowledge:204 "29 second-pass `pin_checks[]` entries" | compact cmd (A) | 29, split 2,2,2,3,4,4,4,8 over 8 receipts. All under `steps.analyze`; `inspect-go-binary` has 0 |
| knowledge:204 key set `{taken_at_utc, equal, entries, changed, missing}` | (A) | 29/29 have exactly that key set. None has `map_path`/`map_sha256` |
| knowledge:204 "29 … `equal: true` against the pre map" | (A); `95e34db:…/carrier-run.py:461` `pins.compare(pins_pre, mid)` | 29/29 `equal: true`, `entries` 146, `changed`/`missing` empty |
| knowledge:204 "pre/post maps identical" | (A) | `pins_pre.entries == pins_post.entries` in 8/8 receipts |
| knowledge:204 anchor `9011581:…/carrier-run.py:479-487` | `git show 9011581:…` | Exactly the snapshot/compare/append block. The producer blob `c536e3e` has identical text at `95e34db:…:460-468`: `git diff 95e34db 9011581` has no hunk past :411, so the block only shifts +19 |
| knowledge:204 quote at `:30-32`; knowledge:205 quote at `:3` | `diff` of the first 198 lines between `9011581` and REV | Byte-identical; both quotes present |
| knowledge:205 "the `9011581` validator only tested `equal`" | `9011581:…/receipt-validate.py:187-191`; forge probe (C) | Confirmed. A forged `entries:7` / 1970 / bare `{"equal":true}` gives exit 0, `findings: []` |
| knowledge:205 producer writes `pins/mid-<n>.json` + `map_path`/`map_sha256` | `carrier-run.py:495-517`; `runs/*/producer.json` | The code is present. The producer.json `tool_sha256` `6665dc7a…` equals the REV blob sha256 |
| knowledge:205 validator recomputes (`mid_map_sha256_mismatch`, `mid_map_compare_mismatch`, `mid_entries_mismatch`, `--require-mid-maps`) | `receipt-validate.py:453-586` and runs (D) | Holds, scoped to the recorded absolute path (F7) |
| SCORECARD:2374 "pre/mid/post pin maps with instants" | `git show REV:SCORECARD.md`, line 2374 | Present; the first 2426 lines are byte-identical to `9011581` |
| SCORECARD:2438 "round-18 receipts retain each mid map with `map_sha256`" | compact cmd (B) | 22/22 maps check out against Git blobs at REV: blob sha256 = `map_sha256`; 152 entries = recorded = `len(pins_pre)`; map = pre; map's own `taken_at_utc` = recorded; `monotonic_ns` pre < mid < post. There are no orphan `pins/` files |
| QUALITY rows 1–20 unchanged, #21 added | `git diff 9011581 b2aad08 -- corpus/QUALITY.md` | One added line (`corpus/QUALITY.md:31`) |
| round-18.md:51 "29/29"; round-18.md:62 red/green; r18 entry `:66-68` "15/15 exit 0, 22 mid-run maps recomputed" | (A), (B), (D) | All hold |

## Findings (by severity)

### F1 — MEDIUM: `routed-defects.py --selftest` is red at REV, so round-18.md:67 is false

- **Observation.** `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --selftest` exits 1 with:
  - `SELFTEST: FAILED closed-fixture-cli: rc=0 opened=['R17-PINMAP', 'R17-PRODUCER-REV'] broken=['receipt-validate-mid-finding', 'producer-revs-are-ancestors']`
  - `closed-fixture-inprocess: open_count=1 broken=['receipt-validate-mid-finding']`
  - five failures of the form `token-only-R17-{VALIDATE16,PRODUCER-REV,SUMS-RUNLOG,REGISTRY,S032-DIGEST}: … extra_open=['R17-PINMAP']`
- **Cause (observation).**
  - The tool's only change from `eb6c266` to REV (blob `31413a2` → `bd6390e`) is the L1 amendment at `routed-defects.py:277-288`. It now requires both `mid_map_sha256_mismatch` and `mid_map_compare_mismatch`.
  - The closed fixture still writes `FINDING = "mid_map_mismatch"` (`routed-defects.py:914`).
  - The `eb6c266` blob prints `SELFTEST: CLEAN cases=17` and exits 0.
- **New overstatement.** `corpus/lessons/round-18.md:67` says "`routed-defects.py --selftest` CLEAN 17". That is true of the `eb6c266` blob only. `SKILL.md:586` registers this selftest for the gate.
- **Fix.**
  - Update the fixture at `:914` to name both ids.
  - Restate the case count from a rerun.

### F2 — MEDIUM: the routed-defects R17-PINMAP checks can be passed without the substance

- **What the checks do (observation from code).**
  - `_pinmaps_retained_check` returns ok on the first receipt, in tree order, whose `pin_checks` each resolve to a blob with sha256 = `map_sha256` (`routed-defects.py:345-368`).
  - It never parses the map, checks `entries`, compares the map with `pins_pre`, or looks at the other 14 receipts.
  - `carrier-run-map-code` and `receipt-validate-mid-finding` only test that a token appears in non-comment code (`:264-270`, `:281-288`).
  - The knowledge and scorecard substance checks only look for three substrings on one line (`:240-245`).
- **Reproduction (Appendix A, mkdtemp clone, origin removed).**
  - m1: strip map fields and `pins/` from 14 of the 15 receipts. `--strict` exits 0, `open_count=0`. On the same tree, `receipt-validate.py --require-mid-maps` exits 1 with 14 invalid.
  - m5: three changes in one commit. `--strict` still exits 0 and R17-PINMAP stays closed.
    - Falsify the correction: 29 → 31, `equal: false`, "pre/post maps differ", and the scorecard line becomes "discard every mid map".
    - Revert `carrier-run.py` and `receipt-validate.py` to their `9011581` bytes, plus one dead token line each.
    - Replace every run with one 2-file receipt whose "map" is `{}`.
- **What this contradicts.** `routed-defects.py:10-11` ("tokens alone cannot close it") and the fix claimed in round-18.md:67.
- **Inference.** At REV the closure is right only because the real state is good. The tool would print the same "closed" on m5. Peer `RoutedBaselineRerun.md:56` (worktree) also re-opened only calib-aether.
- **Fix.** Iterate over every r18 receipt and compare each map with `pins_pre`. Alternatively, run `receipt-validate --require-mid-maps` on a `git archive REV` copy.

### F3 — LOW-MEDIUM: the knowledge:205 correction of the recheck line is accurate but incomplete

- **Observation.**
  - :205 confines the overstatement to the `9011581` validator.
  - The live r17 recheck (`knowledge:3`) runs without `--require-mid-maps`, because the flag fails every r17 receipt.
  - I ran the REV validator without the flag on `pro-aether` with two forged verdicts appended: a 1970 instant with `entries:146`, and a bare `{"equal":true}`. It exits 0 with `findings: []`. Verdict-only entries pass through at `receipt-validate.py:493-500`.
- **Consequence.** At REV, ":3 exit 0 = … mid-run checks consistent" still means verdicts accepted, not verified. QUALITY #21 (`corpus/QUALITY.md:31`) requires the wording "accepted, not verified", and no appended line says it.

### F4 — LOW: the correction lines carry no recheck command that #21 accepts

- **Observation.** `corpus/QUALITY.md:31` admits a retention statement "only with a recheck command that prints the keys the tool actually retained". `knowledge:204-205` and `SCORECARD.md:2438` state retained keys and maps but carry no such command. Commands do exist elsewhere: `round-18.md:62` (validator red/green) and `w1/CriticDiscernment.md:56` (jq).
- **Inference.** #21 applies to these corrections.

### F5 — LOW: anchor drift and imprecision

- **round-18.md:62.** The unrevisioned "`carrier-run.py:475` even tagged (QUALITY #19)" now points at `if time.monotonic() > deadline:` at REV. The tag is at REV:482, or `9011581:475`.
- **knowledge:204.** It cites the verification-era blob `9011581:…:479-487` for what the producer wrote. The producer's text is identical at `95e34db:…:460-468`, so the content is true, but this is the same producer-vs-verification distinction that R17-PRODUCER-REV routes.
- **knowledge:202.** "Routed by `…spotcheck.md:137-139`" spans R17-VALIDATE16 (:138), which this entry does not correct. Nit.

### F6 — LOW (inference): "mid-run" includes a check taken at child spawn

- **Observation.** `last_pin_check = 0.0` (`carrier-run.py:470`, :484; same at the producer) makes the first check fire on the first poll. That is 0.048–0.064 s after the analyze child starts in r17 and 0.045–0.053 s in r18.
  - 8 of the 29 r17 verdicts and 15 of the 22 r18 maps are these spawn-time checks.
  - 9 of the 15 r18 runs (20.6–28.6 s analyses) have no mid map later than spawn + 0.053 s.
- **Inference.** Those instants carry no information about the Ghidra window. The claims stay true under #19's "at the named instants". Wording "at spawn, then every 30 s" would be calibrated.

### F7 — LOW (already known): the validator hashes the absolute recorded `map_path`

- **Observation.** `receipt-validate.py:508-517` reads the live lane worktree, not the checkout being validated.
  - In a clone at REV I appended a byte to the clone's `calib-aether/pins/mid-1.json`; the validator on the clone receipt still exits 0.
  - After remapping `map_path` to the clone, it exits 1 with `mid_map_sha256_mismatch` and `sha256_mismatch`.
- **Consequence.** "Recomputes it" (knowledge:205) holds for the recorded path only. This was already raised in `w1/RevValidatorPaths.md:112-116`.

## Commands (exit codes)

All commands run from `/tmp` or LANE.

```text
routed-defects.py --root LANE --rev b2aad08… [--strict]   -> exit 0 / 0; open_count 0; PINMAP 10/10 ok
routed-defects.py --root LANE --rev 9011581… [--strict]   -> exit 0 / 1; open_count 6; PINMAP 10/10 red
routed-defects.py --root LANE --rev eb6c266…               -> exit 0; open_count 6 (PINMAP code checks already green)
routed-defects.py --selftest                               -> exit 1 (F1 text above)
git show eb6c266:…/routed-defects.py > $T/rd.py; python3 -I -B $T/rd.py --selftest -> exit 0 "SELFTEST: CLEAN cases=17"
receipt-validate.py --require-mid-maps <15 r18 receipts from git ls-tree> -> exit 0 {valid 15}
receipt-validate.py --require-mid-maps <8 r17 receipts>                   -> exit 1 {invalid 8}; mid_map_missing ×29
receipt-validate.py <8 r17 receipts>                                      -> exit 0 {valid 8}
receipt-validate.py --selftest                                            -> exit 0 "SELFTEST: CLEAN cases=18"
git show 9011581:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md | grep -c R17-PINMAP -> 0, exit 1
```

A shell glob `runs/*/receipt.json` in my harness also expanded to `runs/run-log.txt/receipt.json`, which gave exit 2 "unreadable". The results above use explicit `git ls-tree` lists.

(A) r17, from LANE, exit 0 → `29 [2, 2, 2, 3, 4, 4, 4, 8] {(('changed', 'entries', 'equal', 'missing', 'taken_at_utc'), True, 146): 29} pre==post 8 / 8`:

```text
python3 -I -B -c '
import json,subprocess as s,collections as c
R="b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
ps=[p for p in s.run(["git","ls-tree","-r","--name-only",R,"--",".ufo/waves/round-17/runs"],capture_output=True,text=True).stdout.split() if p.endswith("receipt.json")]
k=c.Counter();n=[];pp=0
for p in ps:
  d=json.loads(s.run(["git","show",R+":"+p],capture_output=True).stdout);pc=d["steps"]["analyze"]["pin_checks"];n.append(len(pc));k.update((tuple(sorted(x)),x["equal"],x["entries"]) for x in pc);pp+=d["pins_pre"]["entries"]==d["pins_post"]["entries"]
print(sum(n),sorted(n),dict(k),"pre==post",pp,"/",len(ps))'
```

(B) r18, from LANE, exit 0 → `receipts 15 maps ok 22 / 22 single-check runs 9 first-check offset s 0.044637 - 0.053189`:

```text
python3 -I -B -c '
import json,hashlib,subprocess as s
from datetime import datetime as T
R="b2aad08ceeee8dd125ce0d316056d8bd766c7f94";g=lambda p:s.run(["git","show",R+":"+p],capture_output=True).stdout
ps=[p for p in s.run(["git","ls-tree","-r","--name-only",R,"--",".ufo/waves/round-18/runs"],capture_output=True,text=True).stdout.split() if p.endswith("receipt.json")]
ok=tot=single=0;first=[]
for p in ps:
  d=json.loads(g(p));a=d["steps"]["analyze"];st=T.fromisoformat(a["started_at_utc"]);pc=a["pin_checks"];single+=len(pc)==1
  for i,x in enumerate(pc):
    b=g(x["map_path"][x["map_path"].find(".ufo/"):]);m=json.loads(b);tot+=1
    ok+=(hashlib.sha256(b).hexdigest()==x["map_sha256"] and len(m["entries"])==x["entries"]==len(d["pins_pre"]["entries"]) and (m["entries"]==d["pins_pre"]["entries"])==x["equal"] and m["taken_at_utc"]==x["taken_at_utc"] and d["pins_pre"]["monotonic_ns"]<m["monotonic_ns"]<d["pins_post"]["monotonic_ns"])
    if i==0: first.append((T.fromisoformat(x["taken_at_utc"])-st).total_seconds())
print("receipts",len(ps),"maps ok",ok,"/",tot,"single-check runs",single,"first-check offset s",min(first),"-",max(first))'
```

(C) Forge probe. In mkdtemp `$T`, put `receipt-validate.py` and `pins.py` from `9011581` in `$T/b/tools` and from REV in `$T/r/tools`. Append `{"taken_at_utc":"1970-01-01T00:00:00+00:00","equal":true,"entries":7,"changed":[],"missing":[]}` and `{"equal":true}` to the `pin_checks` of `git show REV:.ufo/waves/round-17/runs/pro-aether/receipt.json`.

| Validator on the forged receipt | Exit | Findings |
|---|---|---|
| `$T/b/tools/receipt-validate.py` | 0 | `[]` |
| `$T/r/tools/receipt-validate.py` | 1 | `mid_entries_mismatch` at `pin_checks[3]` |
| `$T/r/tools/receipt-validate.py --require-mid-maps` | 1 | `mid_map_missing` ×5, `mid_entries_mismatch` |
| `$T/r/tools/receipt-validate.py`, same append with `entries:146` | 0 | `[]` (F3) |

(D) This is the validator rows in the command block above.

## Residual risk and gaps

- I cannot tell from the artifacts whether each mid map was computed at its own instant rather than copied. The code says it was (INFERENCE).
- I did not run `carrier-run.py --selftest`, and I executed no carrier, REA or Ghidra.
- The other five routed defects are out of scope, but F1 also reddens their token-only selftest cases.

## Appendix A — `repro.py` (I ran it as `python3 -I -B repro.py LANE`; exit 0; its clone is deleted on exit)

Output:

```text
REV: exit=0 open_count=0 R17-PINMAP.open=False
m1-strip-14-of-15: exit=0 open_count=0 R17-PINMAP.open=False
  m1 receipt-validate --require-mid-maps: exit=1 {'invalid': 14, 'receipts': 15, 'unreadable': 0, 'valid': 1}
m5-falsified-regressed-fabricated: exit=0 open_count=0 R17-PINMAP.open=False
```

```python
import hashlib, json, os, shutil, subprocess, sys, tempfile
LANE = sys.argv[1]
REV, B = "b2aad08ceeee8dd125ce0d316056d8bd766c7f94", "9011581d84527ba34c675f9cf912e54d2e72d470"
TMP = tempfile.mkdtemp(prefix="truthpinmap-repro-"); C = os.path.join(TMP, "l")
ENV = dict(os.environ, GIT_AUTHOR_NAME="p", GIT_AUTHOR_EMAIL="p@t", GIT_COMMITTER_NAME="p", GIT_COMMITTER_EMAIL="p@t")
R18, KN = ".ufo/waves/round-18/runs", "corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md"
TOOL = os.path.join(LANE, ".ufo/waves/round-18/tools/routed-defects.py")  # the REV blob (worktree == REV)
def git(*a): return subprocess.run(["git", "-C", C, *a], env=ENV, capture_output=True, check=True).stdout.decode().strip()
def rd(rev):
    p = subprocess.run([sys.executable, "-I", "-B", TOOL, "--root", C, "--rev", rev, "--strict"], capture_output=True)
    d = json.loads(p.stdout); pm = next(x for x in d["defects"] if x["id"] == "R17-PINMAP")
    return f"exit={p.returncode} open_count={d['open_count']} R17-PINMAP.open={pm['open']}"
def put(rel, text):
    f = os.path.join(C, rel); os.makedirs(os.path.dirname(f), exist_ok=True); open(f, "w").write(text)
def dirs(): return sorted(n for n in os.listdir(os.path.join(C, R18)) if os.path.isdir(os.path.join(C, R18, n)))
def case(name, *muts):
    git("checkout", "-qf", "-B", name, REV)
    for m in muts: m()
    git("add", "-A"); git("-c", "commit.gpgsign=false", "commit", "-qm", name)
    print(f"{name}: {rd('HEAD')}")
def strip14():   # keep calib-aether; drop map fields and pins/ from the other 14 receipts
    for r in dirs()[1:]:
        p = f"{R18}/{r}/receipt.json"; d = json.load(open(os.path.join(C, p)))
        for pc in d["steps"]["analyze"]["pin_checks"]: pc.pop("map_path"); pc.pop("map_sha256")
        put(p, json.dumps(d)); shutil.rmtree(os.path.join(C, R18, r, "pins"))
def falsify():   # keep every token the checks look for; make the numbers and verdicts false
    t = open(os.path.join(C, KN)).read()
    put(KN, t.replace("each of the 29 second-pass", "each of the 31 second-pass").replace(
        "pre/post maps identical; 29 mid-run comparator verdicts `equal: true`",
        "pre/post maps differ; 31 mid-run comparator verdicts `equal: false`"))
    s = open(os.path.join(C, "SCORECARD.md")).read()
    put("SCORECARD.md", s.replace("round-18 receipts retain each mid map with `map_sha256`.", "round-18 receipts discard every mid map."))
def regress():   # producer and validator back to 9011581 bytes, plus one dead token line each
    for rel, tok in ((".ufo/waves/round-17/tools/carrier-run.py", '_T = "map_sha256"\n'),
                     (".ufo/waves/round-17/tools/receipt-validate.py", '_T = ("mid_map_sha256_mismatch", "mid_map_compare_mismatch")\n')):
        put(rel, git("show", f"{B}:{rel}") + "\n" + tok)
def fabricate(): # every real run removed; one 2-file receipt whose "mid map" is {}
    for r in dirs(): shutil.rmtree(os.path.join(C, R18, r))
    put(f"{R18}/fake/pins/x.json", "{}\n")
    put(f"{R18}/fake/receipt.json", json.dumps({"steps": {"analyze": {"pin_checks": [
        {"map_path": "pins/x.json", "map_sha256": hashlib.sha256(b"{}\n").hexdigest()}]}}}))
try:
    subprocess.run(["git", "clone", "-q", "--no-local", LANE, C], check=True)
    git("remote", "remove", "origin"); assert git("remote") == ""
    print(f"REV: {rd(REV)}")
    case("m1-strip-14-of-15", strip14)
    v = subprocess.run([sys.executable, "-I", "-B", os.path.join(C, ".ufo/waves/round-17/tools/receipt-validate.py"),
                        "--require-mid-maps", *[os.path.join(C, R18, r, "receipt.json") for r in dirs()]], capture_output=True)
    print(f"  m1 receipt-validate --require-mid-maps: exit={v.returncode} {json.loads(v.stdout)['counts']}")
    case("m5-falsified-regressed-fabricated", falsify, regress, fabricate)
finally:
    shutil.rmtree(TMP)
```

F7 reproduction, in a no-origin clone at REV:

1. `printf ' ' >> $C/.ufo/waves/round-18/runs/calib-aether/pins/mid-1.json`
2. `receipt-validate.py --require-mid-maps $C/…/calib-aether/receipt.json` → exit 0.
3. Rewrite `map_path` from the LANE prefix to `$C` in a copy of the receipt, then validate the copy → exit 1 (`mid_map_sha256_mismatch`, `sha256_mismatch`).
