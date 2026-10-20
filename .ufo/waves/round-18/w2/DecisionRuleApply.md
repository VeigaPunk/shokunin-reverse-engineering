PARTIAL

# DecisionRuleApply — round 18 wave 2 (falsify)

Seat `KaidokuR18.DecisionRuleApply`. This is an author-side advisory seat and a read-only one. This file is the only lane write.
Shorthand: `LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `F=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` (the freeze),
`REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, `W=.ufo/waves/round-18`. Every anchor is a `git show REV:<path>` line.
The 33 prediction blobs are byte-identical between F and REV. `git status --porcelain` lists only untracked wave-2 files, so for every tracked file read here the working tree equals REV.

## Verdict

- **Rule applied mechanically → `confirmed` (holds).** Both held-out D labels show their exact frozen H1 read. The only noswiss sibling of a D label is clean, and so are all 11 non-D synthetic labels. No refute clause fires, and no "unresolved" example applies. All 15 labels pass the binding gate. The C3 count is 15.
- **The rule is falsifiable.** Four counterfactual mutations each flip the verdict to `refuted` (M1–M4). The confirm branch needs two exact integers, out of 2³² possible values each, from bytes the emulator was never fitted on. The rule does have three latent precedence gaps (M2, M5, M6). The actual data triggers none of them.
- **The held-out members were held out from the outcome.** No Git object before F and no host file I searched holds a Ghidra observation of either held-out carrier. Each held-out read can be re-derived by hand from three byte fields of its carrier. But "before any round-18 REA run" is false as written: REA `inspect-go-binary` read kimi-webbridge's build info 48 min before F. It ran no Ghidra, so the outcome did not leak.
- **"Calibrated only on aether" is false as written.** calib-notesmd-cli's round-17 no-failure log was a second calibration input, a negative one, and `decision-rule.json:3-6` itself lists it. It does not change any frozen read.

PARTIAL = the mechanism verdict holds, but two provenance statements in scope are false as written (details below). Neither one changes the verdict.

## 1. Frozen rule, clause by clause (observation)

Rule text: `W/predictions/decision-rule.json:2` (binding_gate), `:7` (confirmed), `:19` (refuted), `:20` (route_fields),
`:197` (unresolved), `:8` (count_rule), `:15-18` (held_out_D). `gen-predictions.py:80-82` derives D and held_out_D from the emulator's
`diagnostic` flag (`tools/swiss-misread.py:1531`: `predicted_kind_h1 != predicted_kind_h0`). Nobody chose D by hand.

| clause | labels | observed (`runs/<label>/observation.json`, re-derived from the log) | result |
|---|---|---|---|
| binding gate | 15 | `receipt-validate.py --require-mid-maps` exits 0 ×15. `carrier.sha256_pre == sha256_post ==` prediction sha ×15. On-disk log sha256 `==` receipt `==` observation ×15. Log line `target-<sha12>.bin?MD5=<md5>` equals the file's sha prefix and md5 for the 3 D labels. Prediction blobs F == REV == tree (33/33). | pass |
| held-out D exact H1 read | s1246-swiss-nethttp | `Go analysis failure` (`ghidra.log:408`), `Invalid index: 22386945` (`:451`); frozen `[22386945]` (`decision-rule.json:145-147`) | pass |
| | real-kimi-webbridge | `Go analysis failure` (`ghidra.log:73`), `Invalid index: 15606016` (`:206`); frozen `[15606016]` (`:191-193`) | pass |
| noswiss sibling of D clean | s1246-noswiss-nethttp (the only one; aether and kimi have none) | analyzer_errors `[]`, 0 failure lines | pass |
| non-D synthetics clean | 11 | 0 `Go analysis failure` / `Invalid index` / `past EOF` lines in any of the 11 logs | pass |
| refuted (any of 3) | — | none fires | — |
| unresolved examples | — | compare `all_match` true ×15 (no route mismatch). All logs are bound. No timeouts (`carrier-run.exit` 0 ×15). No D label shows a different read. | none |
| count_rule | 15 | each `compare.json` carries the `extra.eof_reads` field | 15 |

The calibration label calib-aether reproduced its pair exactly (`ghidra.log:97,177`). The rule does not require that (see M5).

## 2. Is the rule weak or unfalsifiable? (observation, then inference)

`rule.py` (§7) applies the rule's clauses to the retained observations and to six single-field mutants:

```
M0 actual observations                       confirmed  refuted_by=[] unresolved_by=[] ambiguity=[]
   held_out_D=['s1246-swiss-nethttp', 'real-kimi-webbridge'] noswiss_siblings=['s1246-noswiss-nethttp'] count_rule=15
M1 nethttp no failure (H0 outcome)           refuted    refuted_by=[('held_out_H0', 's1246-swiss-nethttp')] ...
M2 kimi fails, different index               refuted    refuted_by=[('swiss_unpredicted_read', 'real-kimi-webbridge')] unresolved_by=[('D_different_read', 'real-kimi-webbridge')] ambiguity=['refuted-vs-unresolved']
M3 s1250-swiss-methods fails                 refuted    refuted_by=[('swiss_unpredicted_read', 's1250-swiss-methods')] ...
M4 s1246-noswiss-nethttp fails               refuted    refuted_by=[('noswiss_fails', 's1246-noswiss-nethttp')] ...
M5 calib-aether does not fail                confirmed  refuted_by=[] unresolved_by=[] ambiguity=[]
M6 kimi route mismatch, exact read           unresolved ... unresolved_by=[('route_mismatch', 'real-kimi-webbridge')] ambiguity=['confirmed-vs-unresolved']
```

- **Not unfalsifiable (observation).** Any H0-like outcome on a held-out label (M1), any noswiss failure (M4), or any failure on a Swiss label that H1 predicts silent (M3) refutes. Confirmation needs 14 label conditions at once. Two of them are exact integers; a "close" index fails (M2).
- **Discriminating power is narrow (inference).** Only 2 labels discriminate between H1 and H0. The other 12 synthetic conditions are controls where H1 and H0 agree on `none`. They guard against an "everything fails" mechanism, not against H0. The real carrier has no noswiss control. Its failure alone does not exclude H2 (fallback-caused), because its route is a fallback. H2 is excluded by s1246-swiss-nethttp, which runs on an INFO exact-diff route (`observation.json` `snapshot_route: info`).
- **Latent defect R-A, precedence (observation).** A held-out D label that fails with a different read matches both `refuted` (`:19`, "a Swiss label fails with a read not predicted under H1") and `unresolved` (`:197`, "a D label failing with a different read") (M2). The rule names no precedence. The actual data does not trigger this.
- **Latent defect R-B, route (observation).** `:20` says a route mismatch "is reported, not a mechanism verdict", while `:197` lists "route mismatch" as an unresolved example (M6). These contradict each other. Not triggered.
- **Latent gap R-C, calibration replicate (observation).** If calib-aether had not reproduced in round 18, the rule would still say `confirmed` (M5). Not triggered: aether reproduced its exact pair.

Impacted axes: calibration and operability, for the next round's rule template. These are fixable defects, not tradeoffs the judge must reject.

## 3. Were D's held-out members truly held out?

**No outcome leak (observation).**
- `git rev-list --all` covers every `refs/jj/keep/*` snapshot. All 10 commits that contain `W/predictions` hold the same tree `3b2ab6ffa0b2`, so the predictions were never revised in any snapshot. A `W/runs` tree first appears in the 13:38:07 commits (`2a7c37f`, `5441b83`, `bcc21ba`, REV), after F (13:23:55).
- Every `producer.json` records `branch_tip` `eb6c2668…`, between 16:24:07Z and 16:31:09Z. A run could only record that hash after F existed. `run-log.txt:2` shows the first measured run started at 13:24:07-03:00.
- Before F, 22386945 appears only in static byte probes: `w1/ConnC3Prediction.md:39,130` (`/tmp/r18net2.py`) and `w1/RevNotesmdMaps.md:134`. The wave-1 tool seat ran no REA and no Ghidra (`w1/SwissMisreadTool.md:4-5`).
- Host search for `target-71067480bd99` / `target-5c9faf239ed2`, excluding the lane: the only hits are a wave-2 peer clone, `/tmp/r18v17.pO3tbs/cloneA`, whose directory mtime is 13:56:33, after the runs. tabi-shokunin references kimi-webbridge only as a sha pin; grep for `ghidra|Invalid index|Go analysis failure` there exits 1.
- Limit: the `/tmp/kr17-rea-*` session dirs are gone. A pre-F REA session that left no file and no Git trace cannot be excluded by file evidence. That residual is [INFERENCE]-level.

**Pre-F REA contact (observation; reproduces `w2/FreezeBeforeRun.md` F1).** `git grep -F ev_3eb9c851… F` hits
`W/evidence/real-carrier-census.json:468` (kimi), and the census was generated at 15:35:51Z (`:1473`). The method is "REA `inspect-go-binary` (6.5.0, read-only)" (`w1/RealCarrierCensus.md:23,113-114`). Its provider is `go-build-info`. `grep -ci ghidra` on `runs/real-kimi-webbridge/inspect-go.{json,stderr}` gives 0/0, and the step took 0.66 s. It returned build metadata, not the markup outcome. kimi's frozen route came from the lane's own `buildinfo-probe.py` (`gen-predictions.py:45-48`), not from that REA call. So `decision-rule.json:14` ("frozen_by … before any round-18 REA run") and `claims.json:26,35` are false as written. The correct scope is "before any round-18 REA `analyze` (Ghidra) run". kimi stays held out with respect to the outcome.

**The held-out reads come from three byte fields, not from fitted parameters (observation, `bytes.py` §7).**

```
== s1246-swiss-nethttp .rodata=0x553000 emulator_types=0x553000 last_PT_LOAD_end=0x7461b0
   *textproto.MIMEHeader @0x58b0a0: H1 PkgPath=u32@+88=40 Mcount=u16@+92=0
   *url.Values @0x58dc60: H1 PkgPath=u32@+88=40 Mcount=u16@+92=0
   GoName@types+40 flags=0x6d len=0 tag=0 pkgPath=1 off=0x1006901 -> read at 22386945 (0x1559901) > end: True
== real-kimi-webbridge .rodata=0x882000 emulator_types=0x882000 last_PT_LOAD_end=0xdc7b50
   *textproto.MIMEHeader @0x944e80 / *url.Values @0x94b780 / *http.Header @0x95f5a0: PkgPath=40 Mcount=0
   GoName@types+40 flags=0x67 len=0 tag=1 pkgPath=1 off=0x660100 -> read at 15606016 (0xee2100) > end: True
```

The nethttp `types` base also equals the `runtime.types` symtab value. kimi is stripped, so its base is the emulator's moduledata value, which equals the `.rodata` start; the map addresses come from the frozen emulator output. The held-out failure class (`invalid_index`) differs from the only calibrated class (`past_eof`, aether). Both held-out logs end in the frames H1 predicts: `GoName.getPkgPath(GoName.java:124)` → `resolveNameOff(1063)` → `getGoName(1074)` → `GoName.readStructure(94)` → `ensureBounds(302)` (nethttp `ghidra.log:451-465`, kimi `:206-220`). The getters are reflective, so no frame names the map type: the stack alone does not witness the mechanism; the exact index does.
- Inference: all three D failures pass through the same stdlib slot-40 maps (`textproto.MIMEHeader`, `url.Values`, and `http.Header` except on nethttp). The held-out test is out-of-sample in bytes, not in type family. `knowledge/2026-10-20-r18-swiss-map-replay.md:94` already scopes this to 3 carriers.

**"Calibrated only on aether"? No (observation, plus one inference).** The calibration inputs on record:
- aether's pair: an exact-match acceptance case (`w1/SwissMisreadTool.md:36-45`).
- aether's log type counts (`w1/CriticC3.md:43`; `SwissMisreadTool.md:123-128`).
- notesmd-cli as an acceptance case expecting `none` (`SwissMisreadTool.md:40-46`), checked against its r17 log (`w1/ConnC3Prediction.md:133`). The walk channel was kept out of `predicted_failure` because it "produces false positives on notesmd-cli" (`SwissMisreadTool.md:151-154`; `swiss-misread.py:1461-1464`).

`decision-rule.json:3-6` therefore correctly lists `calib-notesmd-cli` as calibration-only. `knowledge/…r18-swiss-map-replay.md:56` "(calibrated only on aether's logged pair)" is inaccurate.
- Effect on D: none. Map-path-only reads equal the frozen lists for all 15 labels. For kimi, the walk's `unmapped` failure is never merged into a read list, and the kind is computed with `walk=None` (`swiss-misread.py:1479-1482`).
- Inference: notesmd-cli's role is choosing which channel the emulator reports, not fitting a value.

## 4. Other depth observations

- **The walk false positive also hits the held-out real carrier.** kimi's walk gives `unmapped at 0x8` under both H1 and H0 (frozen `predictions/swiss-misread/real-kimi-webbridge.json` `walk`), but Ghidra failed at 15606016. That contradicts the comment "The walk is the observed Ghidra path" (`swiss-misread.py:1441-1442`), and `knowledge:117-118` names only notesmd-cli as a walk false positive.
- **The walk is not "never used as a prediction".** Its `past_eof`/`invalid_index` reads are merged into the frozen lists (`swiss-misread.py:1445-1456`). For all 15 labels they coincide with the map path (nethttp walk `invalid_index 22386945`, aether walk = same pair), so the outcome is unchanged. The prose at `knowledge:106,117-118` is imprecise.
- **Post-hoc type counts are not evidence.** The emulator's H1 discovery count equals the logged `Found − Discovered unindexed` count on 6/6 Swiss synthetics (e.g. nethttp 1674 = 1713 − 39), while H0 is 22 or 72 lower. The gap is an emulator artifact: `_type_refs` follows only `Key/Elem/Bucket` (`swiss-misread.py:1062`), so H0 never follows the `SwissMapType.Group` pointer. A faithful true-layout reader would follow it. The counts therefore do not discriminate H1 from H0, and `knowledge:96` ("silent case is INFERENCE") stands. This comparison is not pre-registered and is not counted.
- **Re-derivation is clean.** `log-extract.py` and `compare.py` (tool digests equal to every `producer.json`, drift 0), re-run into a mkdtemp on the retained logs and the F prediction blobs, reproduce all 15 `observation.json` files key for key and all 15 `compare.json` field/match vectors. Re-running `swiss-misread.py` (sha256 `14924bd6…`, which equals the `emulator_sha256` in the predictions) on the 3 D carriers reproduces their frozen predictions.
- **Timestamp.** The amendment is stamped 13:25:00 (`claims.json:35`), but its commit F is 13:23:55, and the stamp falls inside the calib-aether run (`run-log.txt:2-3`). The content predates the run, so the time stamp is what is wrong (also `w2/FreezeBeforeRun.md` F2).

## 5. Counterexamples, impacted axes, smallest safe corrections

| # | counterexample (reproducing command in §6) | axes | smallest safe correction |
|---|---|---|---|
| P1 | notesmd-cli's r17 negative log calibrated the channel choice, yet `knowledge:56` says "calibrated only on aether" | calibration | named append-only correction: "calibrated on aether's logged pair (positive) and calib-notesmd-cli's r17 no-failure log (negative; walk kept out of `predicted_failure`)", matching `decision-rule.json:3-6` |
| P2 | REA `inspect-go-binary` touched kimi before F (`census.json:468,1473`), contradicting `decision-rule.json:14` and `claims.json:26,35` | calibration | rescope to "before any round-18 REA `analyze` (Ghidra) run"; record the build-info contact (shared with FreezeBeforeRun F1) |
| P3 | kimi's walk is `unmapped at 0x8` while Ghidra read 15606016; the walk's reads are merged into the lists | depth | append to `knowledge:117-118`: add held-out kimi to the walk's false positives, and state that walk reads merge (`:1445-1456`) and equal the map-path reads on 15/15 |
| R-A/B/C | M2, M6, M5 | operability, calibration | next round's rule template: refuted takes precedence over unresolved for a D label's different read; one route-mismatch rule; a calibration label that fails to reproduce → unresolved |

None of these changes `confirmed`. Not examined: determinism (one pass), Ghidra's getter-level stack identities (Base-src.zip not read), and any REA run (none made).

## 6. Commands and exits (run from `$LANE` unless noted)

| # | command | exit / result |
|---|---|---|
| 1 | `git show $F:$W/predictions/decision-rule.json` | 0 |
| 2 | `for f in $(git ls-tree -r --name-only $F -- $W/predictions/); do a=$(git show $F:"$f"\|sha256sum\|cut -d' ' -f1); b=$(sha256sum "$f"\|cut -d' ' -f1); [ "$a" = "$b" ] && echo SAME \|\| echo DIFF; done` | 0; 33 SAME, 0 DIFF |
| 3 | `cd $W && sha256sum -c predictions/SHA256SUMS` | 0; 32 OK. My first try ran from `$W/predictions` and gave exit 1, 32 "FAILED open or read": my cwd error, since the sum paths are relative to `$W` |
| 4 | `for d in $W/runs/*/; do [ -f $d/receipt.json ] \|\| continue; python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $d/receipt.json; echo $d rc=$?; done` | rc=0 ×15. My first try with a non-existent `--receipt` flag gave rc=2 ×15, a usage error |
| 5 | python binding check over `runs/*/{receipt,observation}.json` + prediction sha (carrier pre/post sha, on-disk log sha, binding flags, `pins_compare.equal`, `target-<sha12>.bin` in log) | 0; `ALL_OK` 15/15 |
| 6 | `md5sum <carrier>` vs `receipt.carrier.md5_pre` vs `grep -o -m1 'target-[0-9a-f]*\.bin?MD5=[0-9a-f]*' runs/<D>/logs/*/ghidra.log` | 0; equal for calib-aether, s1246-swiss-nethttp, real-kimi-webbridge |
| 7 | in `mktemp -d`: `git show $F:$W/predictions/<l>.prediction.json > p; log-extract.py --log <log> > o; compare.py --prediction p --observation o` ×15 | log-extract 0 ×15, compare 0 ×15; observation keys identical, compare vectors identical |
| 8 | `git show $F:$W/predictions/decision-rule.json \| python3 -I -B rule.py` | 0; output in §2 |
| 9 | `for c in $(git rev-list --all --since='2026-10-20 11:00'); do git rev-parse -q --verify $c:$W/predictions; git rev-parse -q --verify $c:$W/runs; done` (+ `git for-each-ref`) | 0; one predictions tree `3b2ab6ffa0b2`; first runs tree at 13:38:07 |
| 10 | `python3 -I -B -c` over `runs/*/producer.json` → `branch_tip`, `recorded_at_utc`; tool digests vs current files | 0; all `eb6c2668…`; drift 0 |
| 11 | `grep -rIl --exclude-dir=kaidoku-shokunin -e target-71067480bd99 -e target-5c9faf239ed2 /tmp ~/.cache ~/.local/state ~/.local/share`; fleet `grep -rIl -e 71067480bd99 …` then `grep -rIl -i "ghidra\|Invalid index\|Go analysis failure"` on the 4 tabi knowledge files | 0 (only the post-run peer clone); fleet: tabi sha pins only; tabi grep exit 1 |
| 12 | `git grep -n -F ev_3eb9c851f876fdf456420e056d8bd0c70066cdd6762f33485926313cb722dc24 $F -- .`; `grep -ci ghidra $W/runs/real-kimi-webbridge/inspect-go.json $W/runs/real-kimi-webbridge/inspect-go.stderr` | 0 (`census.json:468`); 0/0 |
| 13 | `python3 -I -B bytes.py` | 0; output in §3 |
| 14 | `python3 -I -B $W/tools/swiss-misread.py --carrier <c> --golang-root ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang` for aether, nethttp, kimi | 0 ×3; kinds/reads equal the frozen values |
| 15 | python: per_type map-path reads vs `predicted_*_reads_h1` for all 15 `predictions/swiss-misread/*.json` | 0; equal 15/15 |
| 16 | python: dump `walk` of the frozen swiss-misread JSON for D labels | 0; kimi h1/h0 `unmapped` index 8 |
| 17 | python: logged `Found`/`Discovered unindexed` vs `walk.indexed_types` | 0; table in §4 |
| 18 | `sed -n '451,466p' $W/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log`; `sed -n '206,221p' $W/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log` | 0 |
| 19 | per log: `grep -c "Go analysis failure"`, `grep -o "Invalid index: [0-9]*"`, `grep -o "Unable to read past EOF: [0-9]*, [0-9]*"` | 0; failures only in the 3 D labels |

## 7. Scripts (verbatim; written only under `mktemp -d /tmp/dra-final.*`)

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

`bytes.py` (reads carrier bytes only; never executes a carrier):

```python
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

Tooling: no installs or upgrades. Used the host python3, git and coreutils, plus the lane's own round-17/round-18 tools. No REA, no Ghidra, no `jj`, no git writes, and no carrier was executed.
