PARTIAL

# DecisionRuleApply — round 18 wave 2 (falsify)

Seat `KaidokuR18.DecisionRuleApply`. This is an author-side advisory seat and a read-only one. This file is the only lane write.
Shorthand: `LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `F=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` (the freeze),
`REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, `W=.ufo/waves/round-18`. Every anchor is a `git show REV:<path>` line. The 33
prediction blobs are byte-identical from F to REV. `git status --porcelain` lists only untracked wave-2 files, so every tracked
file read here is identical to REV. Every step is re-run by `repro.sh` (§6). It exited 0, and §7 reproduces it verbatim.

## Verdict

- **Applying the rule mechanically gives `confirmed`, and that verdict holds.**
  - Both held-out D labels show their exact frozen H1 read.
  - The only noswiss sibling of a D label is clean, and so are all 11 non-D synthetic labels.
  - No refute clause fires, and no "unresolved" example applies.
  - All 15 labels pass the binding gate.
  - The C3 count is 15.
- **The rule is falsifiable.**
  - Four single-field counterfactual mutants each flip the verdict to `refuted` (M1–M4).
  - Confirmation needs two exact integers. Each is `types` plus a 32-bit name offset read from the carrier's own bytes; neither was fitted.
  - The rule has three latent precedence gaps (M2, M5, M6). The actual data triggers none of them.
- **The held-out members were held out from the outcome.** No Git object before F and no host file searched holds a Ghidra observation of either held-out carrier. Each held-out read can be re-derived by hand from three byte fields.
  - However, the phrase "before any round-18 REA run" is false as written. REA `inspect-go-binary` read kimi-webbridge's build info 48 min before F.
  - That command returns build metadata only and runs no Ghidra, so the outcome did not leak.
- **"Calibrated only on aether" is false as written.** calib-notesmd-cli's r17 no-failure log was a second calibration input, a negative one. `decision-rule.json:3-6` itself lists it. It changes no frozen read.

PARTIAL means: the mechanism verdict holds, but two provenance statements in scope are false as written. Neither changes the verdict.

## 1. Frozen rule, clause by clause (observation)

The rule text is at `W/predictions/decision-rule.json`:

| clause | lines |
|---|---|
| binding_gate | `:2` |
| confirmed | `:7` |
| count_rule | `:8` |
| frozen_by | `:14` |
| held_out_D | `:15-18` |
| refuted | `:19` |
| route_fields | `:20` |
| unresolved | `:197` |

D and held_out_D are derived by `gen-predictions.py:80-82` from the emulator's `diagnostic` flag. That flag is `predicted_kind_h1 != predicted_kind_h0` (`tools/swiss-misread.py:1531`). D was not chosen by hand.

| clause | labels | observed (retained `runs/<label>/observation.json`, re-derived from the log) | result |
|---|---|---|---|
| binding gate | 15 | `receipt-validate.py --require-mid-maps` rc=0 ×15. Carrier `sha256_pre == sha256_post ==` prediction sha ×15. On-disk log sha256 `==` receipt `==` observation ×15. `target-<sha12>.bin` appears in the log ×15. Carrier md5 `==` receipt `md5_pre ==` log `MD5=` for the 3 D labels. Prediction blobs F == tree (33/33). | pass |
| held-out D exact H1 read | s1246-swiss-nethttp | `Go analysis failure` (`runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log:408`), `Invalid index: 22386945` (`:451`); frozen `[22386945]` (`decision-rule.json:145-147`) | pass |
| | real-kimi-webbridge | `Go analysis failure` (`…/rea-ghidra-ZSUHpG/ghidra.log:73`), `Invalid index: 15606016` (`:206`); frozen `[15606016]` (`:191-193`) | pass |
| noswiss sibling of D clean | s1246-noswiss-nethttp (the only one; aether and kimi have no sibling) | 0 failure lines | pass |
| non-D synthetics clean | 11 | 0 `Go analysis failure` / `Invalid index` / `past EOF` lines in all 11 logs | pass |
| refuted (any of 3) | — | none fires | — |
| unresolved examples | — | compare `all_match` true ×15 (no route mismatch). Every log is bound. `carrier-run.exit` 0 ×15. No D label shows a different read. | none |
| count_rule | 15 | every `compare.json` carries `extra.eof_reads` | 15 |

calib-aether reproduced its pair (`…/rea-ghidra-HtDopV/ghidra.log:97,177`). The rule does not require this (M5).

## 2. Weak or unfalsifiable? (observation, then inference)

`rule.py` applies the clauses to the retained observations and to six single-field mutants (repro step 7):

```
M0 actual observations                       confirmed  refuted_by=[] unresolved_by=[] ambiguity=[]
   held_out_D=['s1246-swiss-nethttp', 'real-kimi-webbridge'] noswiss_siblings=['s1246-noswiss-nethttp'] count_rule=15
M1 nethttp no failure (H0 outcome)           refuted    refuted_by=[('held_out_H0', 's1246-swiss-nethttp')] unresolved_by=[] ambiguity=[]
M2 kimi fails, different index               refuted    refuted_by=[('swiss_unpredicted_read', 'real-kimi-webbridge')] unresolved_by=[('D_different_read', 'real-kimi-webbridge')] ambiguity=['refuted-vs-unresolved']
M3 s1250-swiss-methods fails                 refuted    refuted_by=[('swiss_unpredicted_read', 's1250-swiss-methods')] unresolved_by=[] ambiguity=[]
M4 s1246-noswiss-nethttp fails               refuted    refuted_by=[('noswiss_fails', 's1246-noswiss-nethttp')] unresolved_by=[] ambiguity=[]
M5 calib-aether does not fail                confirmed  refuted_by=[] unresolved_by=[] ambiguity=[]
M6 kimi route mismatch, exact read           unresolved refuted_by=[] unresolved_by=[('route_mismatch', 'real-kimi-webbridge')] ambiguity=['confirmed-vs-unresolved']
```

- **Not unfalsifiable (observation).** Any of these outcomes refutes the rule:
  - an H0-like outcome on a held-out label (M1);
  - a noswiss failure (M4);
  - a failure on a Swiss label that H1 predicts silent (M3).

  Confirmation needs 14 label conditions to hold together. Two of them are exact reads, and an index that is merely close refutes (M2).
- **Narrow discrimination (inference).** Only the 2 held-out labels separate H1 from H0.
  - The other 12 synthetic conditions are controls where H1 and H0 both say `none`. They guard against an "everything fails" mechanism, not against H0.
  - kimi has no noswiss control, and its route is a fallback, so kimi alone cannot exclude H2 (the failure is caused by the fallback).
  - H2 is excluded by s1246-swiss-nethttp, whose route is INFO (`snapshot_route: info`).
- **R-A, precedence gap (observation).** A D label that fails with a different read matches both `:19` ("a Swiss label fails with a read not predicted under H1") and `:197` ("a D label failing with a different read"). The rule states no precedence between them (M2). Not triggered.
- **R-B, contradictory route handling (observation).** `:20` says a route mismatch "is reported, not a mechanism verdict", yet `:197` lists "route mismatch" as an unresolved example (M6). Not triggered.
- **R-C, calibration-replicate gap (observation).** If calib-aether had not reproduced in round 18, the rule would still say `confirmed` (M5). Not triggered: aether reproduced exactly.

These three are fixable defects in the rule template, not tradeoffs that the judge must reject. Axes: calibration and operability.

## 3. Were D's held-out members truly held out?

**No outcome leak (observation).**
- **Git objects.** `git rev-list --all` includes every `refs/jj/keep/*` snapshot (repro step 9).
  - All 9 commits that contain `W/predictions` hold one tree, `3b2ab6ffa0b2`, so the predictions were never revised in any snapshot.
  - A `W/runs` tree first appears in the 13:38:07 commits (`2a7c37f`, `5441b83`, `bcc21ba`, REV), after F at 13:23:55.
- **Producer records.** Every `producer.json` records `branch_tip` `eb6c2668…` between 16:24:07Z and 16:31:09Z (step 8). The first measured run started at 13:24:07-03:00 (`runs/run-log.txt:2`).
- **Values at F.**
  - `git grep -l -e 22386945 -e 0x1559901 F` finds only the three prediction files plus `w1/ConnC3Prediction.md` (`:39,130`, the static probe `/tmp/r18net2.py`), `w1/RevNotesmdMaps.md:134` and `w1/SwissMisreadTool.md`.
  - The same search for `15606016|0xee2100` finds only the three prediction files.
  - The emulator seat ran no REA and no Ghidra (`w1/SwissMisreadTool.md:4-5`).
- **Host search** (step 11; untruncated, excluding the lane) for `target-71067480bd99|target-5c9faf239ed2` in `/tmp`, `~/.cache`, `~/.local/state` and `~/.local/share`:
  - It found 60 files in 13 `/tmp` dirs, all wave-2 scratch copies. The earliest mtime is 13:43:48, and 0 files predate F.
  - My first pass piped each root through `head -5`; it is superseded.
  - All tabi-shokunin files that cite the kimi sha contain no `ghidra`, `Invalid index`, `Go analysis failure` or REA-analyze text (step 12: xargs exit 123, so grep matched nothing).
- **Limit.** The `/tmp/kr17-rea-*` session dirs no longer exist. A pre-F session that left no file and no Git trace cannot be ruled out by file evidence ([INFERENCE]-level residual).

**Pre-F REA contact (observation; reproduces `w2/FreezeBeforeRun.md` F1).**
- `git grep -F ev_3eb9c851… F` hits `W/evidence/real-carrier-census.json:468` (kimi). The census was generated at 15:35:51Z (`:1473`). Its method is "REA `inspect-go-binary` (6.5.0, read-only)" (`w1/RealCarrierCensus.md:23,113-114`).
- That step's provider is `go-build-info`. `grep -ci ghidra` on `runs/real-kimi-webbridge/inspect-go.{json,stderr}` gives 0/0, and the measured step took 0.66 s (receipt `steps.inspect-go-binary`).
- The frozen route and version came from the lane's own `buildinfo-probe.py` and `predict.py` (`gen-predictions.py:43-46`), not from that REA call.
- So `decision-rule.json:14` ("before any round-18 REA run") and `claims.json:26,35` are false as written. The accurate scope is "before any round-18 REA `analyze` (Ghidra) run".
- kimi remains held out with respect to the outcome.

**The held-out reads follow from three byte fields per carrier (observation, step 13; `bytes.py` reads bytes only).**

```
== s1246-swiss-nethttp .rodata=0x553000 emulator_types=0x553000 last_PT_LOAD_end=0x7461b0
   *textproto.MIMEHeader @0x58b0a0: H1 PkgPath=u32@+88=40 Mcount=u16@+92=0
   *url.Values @0x58dc60: H1 PkgPath=u32@+88=40 Mcount=u16@+92=0
   GoName@types+40 flags=0x6d len=0 tag=0 pkgPath=1 off=0x1006901 -> read at 22386945 (0x1559901) > end: True
== real-kimi-webbridge .rodata=0x882000 emulator_types=0x882000 last_PT_LOAD_end=0xdc7b50
   *textproto.MIMEHeader @0x944e80 / *url.Values @0x94b780 / *http.Header @0x95f5a0: PkgPath=40 Mcount=0
   GoName@types+40 flags=0x67 len=0 tag=1 pkgPath=1 off=0x660100 -> read at 15606016 (0xee2100) > end: True
```

- **Inputs.** For nethttp, `types` also equals the `runtime.types` value in the ELF symbol table, so it does not depend on the emulator. kimi is stripped: its `types` is the emulator's moduledata value, which equals the `.rodata` start. The map addresses come from the frozen emulator output.
- **Class.** The held-out class (`invalid_index`) differs from the only calibrated class (`past_eof`, aether).
- **Stacks.** Both held-out stacks end in the chain H1 names: `GoName.getPkgPath(GoName.java:124)` → `resolveNameOff(1063)` → `getGoName(1074)` → `GoName.readStructure(94)` (nethttp `ghidra.log:451-465`, kimi `:206-220`; step 15). The getters are invoked by reflection, so no frame names the map type. The stack alone is therefore not a mechanism witness; the exact index is.
- **Inference: type family.** All three D failures go through the same stdlib maps with 40-byte slots (`textproto.MIMEHeader`, `url.Values`, and `http.Header` except in nethttp). The test is out-of-sample in bytes, not in type family. `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:94` already scopes the claim to 3 carriers.

**Calibrated only on aether? No (observation; one inference).**
- **The calibration inputs on record:**
  - aether's logged pair, as an exact-match acceptance case (`w1/SwissMisreadTool.md:36-45`);
  - aether's log type counts (`w1/CriticC3.md:43`, `SwissMisreadTool.md:123-128`);
  - notesmd-cli, as an acceptance case expecting `none` (`SwissMisreadTool.md:40-46`), checked against its r17 log (`w1/ConnC3Prediction.md:133`).
- **How notesmd-cli was used.** The walk channel was kept out of `predicted_failure` because it "produces false positives on notesmd-cli" (`SwissMisreadTool.md:151-154`, `swiss-misread.py:1461-1464`).
- **Consequence.** `decision-rule.json:3-6` correctly lists calib-notesmd-cli as calibration-only, so `knowledge/2026-10-20-r18-swiss-map-replay.md:56` "(calibrated only on aether's logged pair)" is inaccurate.
- **Effect on D: none.** For all 15 labels, the map-path-only reads equal the frozen lists (step 8, `checks.py` `mappath_eq_frozen`). kimi's walk failure (`unmapped`) is never merged into a list, and the kind is computed with `walk=None` (`swiss-misread.py:1479-1482`).
- **Inference.** notesmd-cli's role was to decide which channel the tool reports, not to fit a value.

## 4. Other depth observations

- **The walk false positive also hits the held-out real carrier.**
  - kimi's walk reports `unmapped:8` under both H1 and H0 (step 8), but Ghidra failed at 15606016.
  - This contradicts the code comment "The walk is the observed Ghidra path" (`swiss-misread.py:1441-1442`).
  - `knowledge:117-118` names only notesmd-cli as a walk false positive.
- **The walk was folded into the frozen lists, not "never used as a prediction".**
  - Walk reads of kind `past_eof`/`invalid_index` are merged into the frozen lists (`swiss-misread.py:1445-1456`).
  - They coincide with the map path on all 15 labels (nethttp walk `invalid_index:22386945`, aether walk = the same pair), so the outcome is unchanged.
  - The prose at `knowledge:106,117-118` is therefore imprecise.
- **Post-hoc type counts are not evidence.** This comparison was not pre-registered and is not counted.
  - The emulator's H1 discovery count equals the logged `Found − Discovered unindexed` on 6/6 Swiss synthetics (nethttp: 1674 = 1713 − 39). Its H0 count is 22 or 72 lower.
  - The cause is an emulator artifact: `_type_refs` follows only `Key/Elem/Bucket` (`swiss-misread.py:1062`), so H0 never follows the `SwissMapType.Group` pointer. A faithful true-layout reader would.
  - So the counts do not discriminate, and `knowledge:96` ("silent case is INFERENCE") stands.
- **Re-derivation is clean.**
  - Tool digests equal every `producer.json` (drift 0).
  - `log-extract.py` and `compare.py`, re-run on the retained logs and the F prediction blobs, reproduce all 15 observations key for key and all 15 compare vectors (step 6).
  - `swiss-misread.py` (sha `14924bd6…`, equal to the predictions' `emulator_sha256`) re-run on the 3 D carriers reproduces their kinds and reads (step 14).
- **Timestamp (also `w2/FreezeBeforeRun.md` F2).** The amendment is stamped 13:25:00 (`claims.json:35`), but F was committed at 13:23:55, and 13:25:00 falls inside the calib-aether run (`run-log.txt:2-3`). The content predates the run; only the stamp is wrong.

## 5. Counterexamples, impacted axes, smallest safe corrections

| # | counterexample (repro step) | axes | smallest safe correction |
|---|---|---|---|
| P1 | notesmd-cli's negative r17 log drove the channel choice, yet `knowledge:56` says "calibrated only on aether" (§3) | calibration | Named append-only correction: "calibrated on aether's logged pair (positive) and calib-notesmd-cli's r17 no-failure log (negative; walk kept out of `predicted_failure`)". This matches `decision-rule.json:3-6`. |
| P2 | REA `inspect-go-binary` touched kimi before F (step 10) | calibration | Rescope `decision-rule.json:14` and `claims.json:26,35` to "before any round-18 REA `analyze` (Ghidra) run", and record the build-info contact. This is shared with FreezeBeforeRun F1. |
| P3 | kimi walk `unmapped:8` versus the logged 15606016, and the walk reads are merged (step 8) | depth | Append to `knowledge:117-118`: held-out kimi is also a walk false positive. Walk reads are merged (`:1445-1456`) and equal the map-path reads on 15/15. |
| R-A/B/C | M2, M6, M5 (step 7) | operability, calibration | In the next round's rule template: (1) refuted wins over unresolved when a D label shows a different read; (2) state one route-mismatch rule; (3) a calibration label that fails to reproduce makes the result unresolved. |

None of these changes `confirmed`. Not examined:
- determinism (one pass only);
- Ghidra getter identities per stack frame (Base-src.zip was not read);
- any new REA run (none was made).

## 6. Repro run and exits

`bash repro.sh` exited 0 (wall time 59.8 s). It needs `rule.py`, `checks.py` and `bytes.py` beside it (§7). sha256 of each file:

| file | sha256 |
|---|---|
| repro.sh | `3ff23bd4…4c19` |
| rule.py | `8673c8ae…33b2` |
| checks.py | `e6edd844…f3fe` |
| bytes.py | `be985fbd…0361` |

| step | what | result |
|---|---|---|
| 1 | frozen rule parses | exit=0 |
| 2 | prediction blobs F vs tree | `33 SAME` |
| 3 | `sha256sum -c --quiet predictions/SHA256SUMS` from `$W` | exit=0 |
| 4 | receipt-validate `--require-mid-maps` | `15 rc=0` |
| 5 | md5 tie, D labels | OK ×3 |
| 6 | log-extract + compare re-derivation | `15 le=0 cmp=0 obs_same=True cmp_same=True all_match=True` |
| 7 | rule + mutants | output in §2; exit=0 |
| 8 | checks.py | `ALL_OK`, exit=0. Per label: OK. `at=` 16:24:07Z…16:31:09Z. Walk: aether `past_eof:17645861`, nethttp `invalid_index:22386945`, notesmd and kimi `unmapped:8`. Counts as in §4. |
| 9 | Git objects | 9 commits with pred `3b2ab6ffa0b2`; runs only in the 13:38:07 commits |
| 10 | `git grep` of the evidence ID at F | `census.json:468`, exit=0; ghidra count 0/0 |
| 11 | host search | `files=60 dirs=13 earliest=13:43:48 pre_freeze=0` |
| 12 | tabi grep | exit=123 (no match) |
| 13 | bytes.py | output in §3; exit=0 |
| 14 | emulator re-run | `same=True` ×3, exit=0 ×3 |
| 15 | stack tails | `Invalid index: 22386945` / `15606016`, then `GoName.java:94`, `GoRttiMapper.java:1074`, `:1063`, `GoName.java:124` |
| 16 | failure lines | `gaf=1` only for calib-aether, real-kimi-webbridge and s1246-swiss-nethttp |

My own errors, superseded by the runs above:
- My first `receipt-validate` loop used a non-existent `--receipt` flag, which is a usage error (rc=2 ×15).
- My first `sha256sum -c` ran from `$W/predictions`, where the sum paths do not resolve: exit 1, 32 "FAILED open or read".
- My first host search piped each root through `head -5`.

## 7. Scripts (verbatim; written only under `mktemp -d /tmp/dra-final.*`)

`repro.sh`:

```bash
#!/usr/bin/env bash
# DecisionRuleApply repro (read-only on the lane; scratch only under a fresh mktemp dir). Needs rule.py, checks.py, bytes.py beside it.
set -u
LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; F=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0; W=.ufo/waves/round-18
G=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang
HERE=$(cd "$(dirname "$0")" && pwd); T=$(mktemp -d /tmp/dra-repro.XXXXXX); cd "$LANE" || exit 2
LABELS=$(cd $W/runs && ls -d */ | tr -d /)
echo "## 1 frozen rule parses"; git show $F:$W/predictions/decision-rule.json | python3 -I -B -c 'import json,sys; json.load(sys.stdin)'; echo "exit=$?"
echo "## 2 prediction blobs F vs tree"; for f in $(git ls-tree -r --name-only $F -- $W/predictions/); do a=$(git show $F:"$f" | sha256sum | cut -d' ' -f1); b=$(sha256sum "$f" | cut -d' ' -f1); [ "$a" = "$b" ] && echo SAME || echo "DIFF $f"; done | sort | uniq -c
echo "## 3 SHA256SUMS"; (cd $W && sha256sum -c --quiet predictions/SHA256SUMS); echo "exit=$?"
echo "## 4 receipt-validate --require-mid-maps"; for l in $LABELS; do python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $W/runs/$l/receipt.json > $T/rv.$l 2>&1; echo "rc=$?"; done | sort | uniq -c
echo "## 5 md5 tie (D labels)"; for l in calib-aether s1246-swiss-nethttp real-kimi-webbridge; do p=$(python3 -I -B -c "import json;print(json.load(open('$W/runs/$l/receipt.json'))['carrier']['path'])"); m=$(md5sum "$p" | cut -c1-32); r=$(python3 -I -B -c "import json;print(json.load(open('$W/runs/$l/receipt.json'))['carrier']['md5_pre'])"); g=$(grep -o -m1 'MD5=[0-9a-f]*' $W/runs/$l/logs/*/ghidra.log | cut -c5-); [ "$m" = "$r" ] && [ "$m" = "$g" ] && echo "$l md5 tie OK" || echo "$l md5 tie BAD"; done
echo "## 6 re-derive observation/compare"; for l in $LABELS; do git show $F:$W/predictions/$l.prediction.json > $T/$l.p; python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log $W/runs/$l/logs/*/ghidra.log > $T/$l.o; e1=$?; python3 -I -B .ufo/waves/round-17/tools/compare.py --prediction $T/$l.p --observation $T/$l.o > $T/$l.c; e2=$?; python3 -I -B -c "import json; a=json.load(open('$T/$l.o')); b=json.load(open('$W/runs/$l/observation.json')); c=json.load(open('$T/$l.c')); d=json.load(open('$W/runs/$l/compare.json')); v=lambda x:[(f['field'],f['match']) for f in x['fields']]; print('le=$e1 cmp=$e2 obs_same=%s cmp_same=%s all_match=%s' % (a==b, v(c)==v(d), c['all_match']))"; done | sort | uniq -c
echo "## 7 rule + mutants"; git show $F:$W/predictions/decision-rule.json | python3 -I -B $HERE/rule.py; echo "exit=$?"
echo "## 8 checks.py"; python3 -I -B $HERE/checks.py; echo "exit=$?"
echo "## 9 Git objects holding predictions/runs (all refs incl. refs/jj/keep)"; for c in $(git rev-list --all); do p=$(git rev-parse -q --verify "$c:$W/predictions"); r=$(git rev-parse -q --verify "$c:$W/runs"); [ -n "$p$r" ] && echo "$(git log -1 --format='%ci %h' $c) pred=${p:0:12} runs=${r:0:12}"; done | sort
echo "## 10 pre-F REA build-info contact"; git grep -n -F ev_3eb9c851f876fdf456420e056d8bd0c70066cdd6762f33485926313cb722dc24 $F -- . | cut -c1-120; echo "exit=$?"; grep -ci ghidra $W/runs/real-kimi-webbridge/inspect-go.json $W/runs/real-kimi-webbridge/inspect-go.stderr
echo "## 11 host search (untruncated), mtimes vs F"; for d in /tmp "$HOME/.cache" "$HOME/.local/state" "$HOME/.local/share"; do [ -d "$d" ] || continue; timeout 150 grep -rIl --exclude-dir=kaidoku-shokunin -e target-71067480bd99 -e target-5c9faf239ed2 "$d" 2>/dev/null; done | python3 -I -B -c "
import sys,os,datetime
F=datetime.datetime(2026,10,20,13,23,55).timestamp()
ps=[p for p in sys.stdin.read().split(chr(10)) if p and not p.startswith('$T')]
ms=[os.stat(p).st_mtime for p in ps]
print('files=%d dirs=%d earliest=%s pre_freeze=%d' % (len(ps), len({'/'.join(p.split('/')[:3]) for p in ps}), datetime.datetime.fromtimestamp(min(ms)).strftime('%H:%M:%S') if ms else '-', sum(m < F for m in ms)))"
echo "## 12 tabi files citing the kimi sha: any Ghidra/REA-analyze text?"; timeout 60 grep -rIl --exclude-dir=.git -e 71067480bd99 /home/vgpnk/Projects/shokunin/tabi-shokunin | xargs -d '\n' grep -Il -i -e ghidra -e "Invalid index" -e "Go analysis failure" -e "rea-agents.*analyze"; echo "exit=$? (123 = grep found nothing in any file)"
echo "## 13 bytes.py"; python3 -I -B $HERE/bytes.py; echo "exit=$?"
echo "## 14 emulator re-run vs frozen (D carriers)"; for l in calib-aether s1246-swiss-nethttp real-kimi-webbridge; do p=$(python3 -I -B -c "import json;print(json.load(open('$W/predictions/$l.prediction.json'))['carrier']['path'])"); python3 -I -B $W/tools/swiss-misread.py --carrier "$p" --golang-root $G > $T/$l.sm; e=$?; python3 -I -B -c "import json; a=json.load(open('$T/$l.sm')); b=json.load(open('$W/predictions/swiss-misread/$l.json')); k=('predicted_failure_kind_h1','predicted_eof_reads_h1','predicted_invalid_index_reads_h1','predicted_failure_kind_h0','diagnostic'); print('$l exit=$e same=%s %s' % (all(a[x]==b[x] for x in k), [a[x] for x in k]))"; done
echo "## 15 held-out stack tails"; sed -n '451p;457p;463,465p' $W/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log; sed -n '206p;212p;218,220p' $W/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log
echo "## 16 failure lines per log"; for l in $LABELS; do L=$(ls $W/runs/$l/logs/*/ghidra.log); echo "$l gaf=$(grep -c 'Go analysis failure' $L) inv=$(grep -o 'Invalid index: [0-9]*' $L | sort -u | tr '\n' ';') eof=$(grep -o 'Unable to read past EOF: [0-9]*, [0-9]*' $L | sort -u | tr '\n' ';')"; done
```

`rule.py`:

```python
# usage (from LANE): git show F:.ufo/waves/round-18/predictions/decision-rule.json | python3 -I -B rule.py
import json, sys, copy
R = json.load(sys.stdin)
W = ".ufo/waves/round-18/runs/"
T = {t["label"]: t for t in R["table"]}
O0 = {l: json.load(open(W + l + "/observation.json")) for l in T}
C0 = {l: json.load(open(W + l + "/compare.json")) for l in T}

def apply(O, C):
    fail = lambda l: any("Go analysis failure" in e for e in O[l]["analyzer_errors"])
    exact = lambda l: (O[l]["eof_reads"] == T[l]["eof_reads_h1"]
                       and O[l]["invalid_index_reads"] == T[l]["invalid_index_reads_h1"])
    swiss = lambda l: "noswissmap" not in T[l]["go_version"]
    D, H = R["diagnostic_set_D"], R["held_out_D"]
    syn = [l for l in T if l.startswith("s12")]
    sib = [l.replace("-swiss-", "-noswiss-") for l in D if "-swiss-" in l]
    conf = (all(fail(l) and exact(l) for l in H) and all(not fail(l) for l in sib)
            and all(not fail(l) for l in syn if l not in D))
    ref = ([("held_out_H0", l) for l in H if not fail(l)]
           + [("noswiss_fails", l) for l in syn if not swiss(l) and fail(l)]
           + [("swiss_unpredicted_read", l) for l in T
              if swiss(l) and fail(l) and (T[l]["h1"] == "none" or not exact(l))])
    unres = ([("D_different_read", l) for l in D if fail(l) and not exact(l)]
             + [("route_mismatch", l) for l in T if not C[l]["all_match"]])
    count = sum(any(f["field"] == "extra.eof_reads" for f in C[l]["fields"]) for l in T)
    return conf, ref, unres, count, sib

def show(name, O, C):
    conf, ref, unres, count, sib = apply(O, C)
    v = "refuted" if ref else ("confirmed" if conf and not unres else "unresolved")
    amb = []
    if ref and unres: amb.append("refuted-vs-unresolved")
    if conf and unres and not ref: amb.append("confirmed-vs-unresolved")
    print("%-44s %-10s refuted_by=%s unresolved_by=%s ambiguity=%s" % (name, v, ref, unres, amb))
    return v, count, sib

v, count, sib = show("M0 actual observations", O0, C0)
print("   held_out_D=%s noswiss_siblings=%s count_rule=%d" % (R["held_out_D"], sib, count))
def mut(name, f):
    O, C = copy.deepcopy(O0), copy.deepcopy(C0); f(O, C); show(name, O, C)
mut("M1 nethttp no failure (H0 outcome)", lambda O, C: O["s1246-swiss-nethttp"].update(analyzer_errors=[], invalid_index_reads=[]))
mut("M2 kimi fails, different index", lambda O, C: O["real-kimi-webbridge"].update(invalid_index_reads=[15606017]))
mut("M3 s1250-swiss-methods fails", lambda O, C: O["s1250-swiss-methods"].update(analyzer_errors=["Go analysis failure x"]))
mut("M4 s1246-noswiss-nethttp fails", lambda O, C: O["s1246-noswiss-nethttp"].update(analyzer_errors=["Go analysis failure x"]))
mut("M5 calib-aether does not fail", lambda O, C: O["calib-aether"].update(analyzer_errors=[], eof_reads=[]))
mut("M6 kimi route mismatch, exact read", lambda O, C: C["real-kimi-webbridge"].update(all_match=False))
sys.exit(0 if v == "confirmed" else 1)
```

`checks.py`:

```python
# usage (from LANE): python3 -I -B checks.py   -- binding, producer, map-path, walk, type-count checks per label
import json, glob, os, hashlib, re
W = ".ufo/waves/round-18/"
F = "eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0"
labels = sorted(os.path.basename(p.rstrip("/")) for p in glob.glob(W + "runs/*/"))
ok = True
for l in labels:
    r = json.load(open(W + "runs/%s/receipt.json" % l)); o = json.load(open(W + "runs/%s/observation.json" % l))
    p = json.load(open(W + "predictions/%s.prediction.json" % l)); pr = json.load(open(W + "runs/%s/producer.json" % l))
    sm = json.load(open(W + "predictions/swiss-misread/%s.json" % l))
    c, L = r["carrier"], r["retained_logs"][0]; g = L["files"]["ghidra.log"]
    text = open(g["path"], "rb").read()
    b = dict(carrier=c["sha256_pre"] == c["sha256_post"] == p["carrier"]["sha256"],
             log=hashlib.sha256(text).hexdigest() == g["sha256"] == o["log_sha256"] and o["log_path"] == g["path"],
             binding=all(L["binding"].values()),
             pins=bool(r["pins_compare"]["equal"]) and not r["pins_compare"]["changed"],
             target=("target-%s.bin" % p["carrier"]["sha256"][:12]).encode() in text,
             tip=pr["branch_tip"] == F,
             tools=all(hashlib.sha256(open(t, "rb").read()).hexdigest() == h for t, h in pr["tool_sha256"].items()))
    eof, inv = [], set()
    for t in sm["per_type"]:
        h = t.get("h1") or {}
        if h.get("outcome") == "fail" and h.get("eof") and h["eof"] not in eof: eof.append(h["eof"])
        if h.get("outcome") == "invalid_index": inv.add(h["index"])
    b["mappath_eq_frozen"] = eof == sm["predicted_eof_reads_h1"] and sorted(inv) == sm["predicted_invalid_index_reads_h1"]
    s = text.decode("utf-8", "replace")
    fo = re.findall(r"Found (\d+) Go types", s); un = re.findall(r"Discovered (\d+) unindexed Go types", s)
    idx = int(fo[0]) - (int(un[0]) if un else 0) if fo else None
    wk = sm.get("walk") or {}; it = wk.get("indexed_types") or {}; w1 = wk.get("h1") or {}; w0 = wk.get("h0") or {}
    ok = ok and all(b.values())
    print("%-24s %s at=%s walk_h1=%s:%s walk_h0=%s:%s log_indexed=%s emu_h1=%s emu_h0=%s%s" % (
        l, "OK " if all(b.values()) else "BAD", pr["recorded_at_utc"], w1.get("kind"), w1.get("index"),
        w0.get("kind"), w0.get("index"), idx, it.get("h1"), it.get("h0"),
        "" if all(b.values()) else " " + str([k for k, v in b.items() if not v])))
print("ALL_OK" if ok else "SOME_FAILED")
```

`bytes.py` (reads carrier bytes; never executes a carrier):

```python
# usage (from LANE): python3 -I -B bytes.py  -- reads carrier bytes only; never executes them
import json, struct
SM = ".ufo/waves/round-18/predictions/swiss-misread/%s.json"
def load(path):
    d = open(path, "rb").read()
    ph, sh = struct.unpack_from("<Q", d, 0x20)[0], struct.unpack_from("<Q", d, 0x28)[0]
    phes, phn = struct.unpack_from("<HH", d, 0x36); shes, shn, shx = struct.unpack_from("<HHH", d, 0x3A)
    loads = [struct.unpack_from("<IIQQQQQQ", d, ph + i * phes) for i in range(phn)]
    loads = [(va, off, fs, ms) for t, _, off, va, _, fs, ms, _ in loads if t == 1]
    secs = [struct.unpack_from("<IIQQQQIIQQ", d, sh + i * shes) for i in range(shn)]
    names = {d[secs[shx][4] + s[0]:].split(b"\0", 1)[0].decode(): s[3] for s in secs}
    return d, loads, names
def rd(d, loads, va, n):
    for pva, off, fs, _ in loads:
        if pva <= va < pva + fs: return d[off + va - pva: off + va - pva + n]
for lab in ("s1246-swiss-nethttp", "real-kimi-webbridge"):
    em = json.load(open(SM % lab)); d, loads, names = load(em["carrier"]["path"])
    types = names[".rodata"]; end = max(va + ms for va, _, _, ms in loads)
    print("== %s .rodata=0x%x emulator_types=0x%x last_PT_LOAD_end=0x%x" % (lab, types, em["module"]["types"], end))
    for t in em["per_type"]:
        if t.get("uncommon") and t.get("slot_size") == 40:
            b = rd(d, loads, t["addr"] + 88, 6)
            print("   %s @0x%x: H1 PkgPath=u32@+88=%d Mcount=u16@+92=%d" % (t["name"], t["addr"], *struct.unpack("<IH", b)))
    n = rd(d, loads, types + 40, 64); fl, ln = n[0], n[1]; p = 2 + ln
    if fl & 2: p += 1 + n[p]
    off = struct.unpack_from("<i", n, p)[0]
    print("   GoName@types+40 flags=0x%02x len=%d tag=%d pkgPath=%d off=0x%x -> read at %d (0x%x) > end: %s"
          % (fl, ln, bool(fl & 2), bool(fl & 4), off, types + off, types + off, types + off > end))
```

**Tooling.** No installs or upgrades. I used the host's python3, git and coreutils, plus the lane's own round-17 and round-18 tools. No REA, no Ghidra, no `jj`, no git writes. No carrier was executed.
