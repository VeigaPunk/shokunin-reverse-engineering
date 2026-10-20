HOLDS

`calib-notesmd-cli` (go1.25.8, sha256 `412dc532…802d`) was re-derived from the raw `ghidra.log` lines at REV `b2aad08c`. All of the following hold:
- all 8 compared fields;
- the three log-binding facts;
- the carrier sha256;
- freeze integrity;
- `receipt-validate --require-mid-maps`.

One finding sits outside the verdict. The frozen emulator's `walk` record for this label comes from an emulator defect: the variadic bit is not masked (F1). Wave 1's explanation of that record is wrong (F2). The defect changes **no** frozen compared field on any of the 15 labels.

Seat: KaidokuR18.Runcalibnotesmdcli, author-side advisory, round 18 wave 2.

Abbreviations used below:
- `REV` = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`
- `FRZ` = `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`
- `RUN` = `.ufo/waves/round-18/runs/calib-notesmd-cli`
- `LOG` = `$RUN/logs/rea-ghidra-tpzD5t/ghidra.log`
- `PRED` = `.ufo/waves/round-18/predictions/calib-notesmd-cli.prediction.json`
- `SM` = `.ufo/waves/round-18/tools/swiss-misread.py`

Every `path:line` is taken from `git show REV:path`. For RUN files the working tree is byte-identical to REV: `git hash-object` matches the REV blob for all 17 files, with no extras. [OBS] means observed; [INF] means inference.

## 1. Per-field verdicts

| Field | Frozen (PRED; FRZ blob == REV blob) | Raw-log re-derivation [OBS] | compare.json | Verdict |
|---|---|---|---|---|
| snapshot_route | `fallback` (PRED:34) | LOG:68 is the only `(GoApiSnapshot)` line: WARN `Falling back from 1.25.8 to 1.25.0 for Go API snapshot`. There are 0 INFO `(GoApiSnapshot)` lines. GoApiSnapshot.java:159-163 emits exactly one of the two. | :25-26 true | HOLDS |
| fallback_to | `1.25.0` (PRED:31) | LOG:68 gives `to` = `1.25.0`. The base `go1.25.0.json` sha256 is `54d10162…`, which matches PRED:55. `patchverdiffs/` contains no `go1.25.N` diff (the newest is go1.24.6), consistent with `base_only` (PRED:74). | :31-32 true | HOLDS |
| snapshot_label | `1.25.8` (PRED:33) | LOG:69 `(GoRttiMapper) Using Go API snapshot for version 1.25.8`. This is an echo of the requested version, so it does not discriminate (compare.py:47). | :11-12 true | HOLDS (non-discriminating) |
| untested_version | null (PRED:35) | 0 `Untested Go version` lines. 1.25.8 is inside the supported range 1.15-1.25. | :5-6 true | HOLDS |
| missing_bootstrap | false (PRED:32) | 0 `Missing Go bootstrap` lines. LOG:71 reads `Found 2302 Go types`. | :19-20 true | HOLDS |
| extra.analyzer_errors_empty | true (PRED:38) | 0 ERROR-level lines anywhere in the log, and 0 `Go analysis failure` lines. | :39-40 true | HOLDS |
| extra.eof_reads | `[]` (PRED:39) | 0 `Unable to read past EOF:` lines on any raw line, continuation lines included. | :45-46 true | HOLDS |
| extra.invalid_index_reads | `[]` (PRED:40) | 0 `Invalid index:` lines. | :51-52 true | HOLDS |
| c3 h1_kind/h0_kind `none`, diagnostic false (PRED:16,19-20) | No failure, and symbol markup ran to completion. LOG:76-78 (`Marked 58 Go funcs as NoReturn`, two signature-fix lines) and LOG:87 (`Go missing type names: 11`) appear here but are absent from all 3 failing logs (aether, kimi, s1246-swiss-nethttp). | — | HOLDS (vacuous; see R1) |
| c3 true_kind `swiss` (PRED:23) | Build info is `go1.25.8` with no `X:` suffix and no GOEXPERIMENT key in `$RUN/inspect-go.json`. The binary has 60 `map.group[` strings and 0 `map.bucket[` strings. My census finds 63 Swiss-shaped map descriptors and 0 OldMapType-shaped ones. | — | HOLDS |
| c3 uncommon_map_types / misread_map_types `0/0` (PRED:24,22) | Independent byte census of moduledata `[types,etypes)` = `[0x601000,0x6d60e1)`, with moduledata found at `0x821f20`. Result: 63 Swiss map types (`0x62dc60`…`0x62fb60`), all with tflag=2, so 0 uncommon and 0 named. These are the same 63 addresses, names and slot sizes as the frozen `per_type`. The four slot-40 maps (`map[string][]string`, `map[string][]obsidian.NoteMatch`, `map[reflect.visit]bool`, `map[reflect.Type][]toml.field`) are unnamed, so the H1 uncommon read is never reached. | — | HOLDS |

Exit files: compare.json:2 has `all_match: true`, and `$RUN/{compare,observation,carrier-run}.exit` are all `0`.

The observation file agrees with my extraction field for field: observation.json:2-6, :160, :168-180 (route `fallback`, `from` 1.25.8 → `to` 1.25.0 at :171-172).

## 2. Binding, custody and freeze [OBS]

Log binding (the three facts carrier-run.py checks):
- **Log path:** LOG:2 is `Using log file: /tmp/kr17-rea-mv6bwf7_/rea-ghidra-tpzD5t/ghidra.log`. That is receipt `session_dir` (receipt.json:1911) plus `/ghidra.log`, matching the regex at carrier-run.py:143-145. All 13 `/tmp` session paths in the log name this one directory.
- **Target:** LOG:46 reads `IMPORTING: file:///tmp/kr17-rea-mv6bwf7_/rea-ghidra-tpzD5t/target-412dc532d278.bin`. The suffix is sha256[:12] of the carrier (carrier-run.py:146-148). All 6 `target-*` mentions carry `412dc532d278`.
- **MD5:** LOG:57 carries `?MD5=a2d7519de311acb58691fb6fcbbcb270`. This equals receipt `md5_pre` (receipt.json:6) and `md5sum` of the carrier today (carrier-run.py:151-154).

Receipt state:
- Binding flags `logfile_ok`, `md5_ok` and `target_ok` are all true (receipt.json:1893-1895).
- There is exactly one bound session (receipt.json:2-4). `unbound_sessions` (:1998), `session_dir_baseline` (:1914) and `session_parent_leftovers` (:1916) are all empty.

Timing:
- The log spans 13:25:20–13:25:58 −03:00.
- That lies inside the analyze step, 16:25:19.64Z–16:25:59.27Z (receipt.json:1972, :1929).
- `last_copy_utc` is 16:25:58.77Z (receipt.json:1909).

Carrier and retained files:
- `sha256sum` of the carrier today is `412dc532d278b9e4…802d`. This equals PRED:28 and receipt `sha256_pre`/`sha256_post` (receipt.json:8-9).
- The log's sha256 `47a14c63…c4db` and size of 11897 bytes equal the receipt's `retained_logs` entry and observation.json:166.

Freeze:
- The `predictions/` directory is unchanged from FRZ to REV (`git diff --quiet` exit 0), and FRZ is an ancestor of REV.
- PRED's sha256 `2c55b739…8f4f` equals its `pins_pre` entry, taken at receipt.json:1884 (16:25:18.97Z).
- FRZ was committed at 13:23:55 −03:00, before that pin snapshot. producer.json:3-5 records `branch_tip` = FRZ at 16:25:18Z.

Emulator:
- The emulator's sha256 `14924bd6…` is the same at FRZ, at REV and in the working tree, and equals PRED's `c3.emulator_sha256`.
- Replaying the FRZ emulator in memory on the carrier reproduces `predictions/swiss-misread/calib-notesmd-cli.json` byte for byte (`replay==frozen_blob: True`).

Validator:
- `receipt-validate.py --require-mid-maps` exits 0: 1 receipt, valid, `checks_performed` 366, `findings` `[]`.
- The two mid-run pin checks report `equal: true` (receipt.json:1936-1946).

## 3. Findings (by severity)

**F1 — Medium (latent); zero effect on REV's frozen fields. The emulator does not mask FuncType's variadic bit.**

The defect:
- SM:939 computes `count = in_count + out_count`.
- Ghidra masks the bit. In `Base-src.zip:ghidra/app/util/bin/format/golang/rtti/types/GoFuncType.java`, :79 is `return outCount & 0x7fff;` and :86 is `return inCount + (outCount & 0x7fff);`. The param slice is sized from `getParamCount()` at :98.

What it does on this carrier [OBS]:
- The function type at `0x629ce0` is `func(interface {}, func(int) string, ...interface {}) (int, error)`.
- Its InCount is 3 and its OutCount is `0x8002`, so it has 5 real parameters.
- The emulator instead walks 3+0x8002 slots. Slot [5], the word just past the real array, is `0x8`.
- That is exactly the frozen walk failure: `unmapped at 0x8` reached via `type@0x613180 → elem → interface.imethod[0].typ → func.param[5]`, under both hypotheses. It is recorded in `predictions/swiss-misread/calib-notesmd-cli.json:1086-1118`.

Counterfactual [OBS]:
- Masking that one line in memory changes `walk.failed` from {h1: True, h0: True} to {False, False}.
- Every prediction key is unchanged (`none`/`none`, `[]`, `[]`, 63/0).
- Across all 15 carriers, masking changes no frozen predicted key (kind, eof and invalid for both h1 and h0, plus diagnostic).
- notesmd is the only label whose walk flips. aether and kimi still fail under both hypotheses, and s1246-swiss-nethttp still fails under h1, so those failures have other causes, which I did not examine.

Latent risk [INF, from code]:
- The first walk failure's EOF or `invalid_index` is folded into the frozen lists and the predicted kind (SM:1445-1447, SM:1454-1456, SM:1479-1482).
- `read()` classifies any word above `max_index` as `invalid_index` (SM:671-672). Slot [7] on this carrier is `0x330808028f0776ef`.
- On another carrier, the same bug could therefore inject a spurious `invalid_index_reads_h1` into a frozen prediction.
- Here it stayed benign only because slot [5] happened to be a small, unmapped word.

**F2 — Low. Wave 1's root cause for the notesmd walk false positive is wrong, and "never used as a prediction" is imprecise.**

What the lane says:
- w1/SwissMisreadTool.md:151-153 attributes the notesmd walk false positive to "refs this emulator follows but Ghidra's discovery/alignment filters evidently do not".
- corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:117-118 repeats "produces false positives (notesmd-cli) and was never used as a prediction".
- SM:1441-1442 says "The walk is the observed Ghidra path".

What I found:
- For notesmd the cause is F1. The masked counterfactual removes the failure entirely, and LOG:76-78 and LOG:87 show Ghidra's markup finishing.
- "Never used as a prediction" holds only for the boolean `predicted_failure` (SM:1465). It does not hold for the eof/invalid lists or the predicted kind (SM:1445-1456, SM:1479).

**F3 — Low / informational. The amendment timestamp is forward-dated.**
- claims.json:35 says `"at": "2026-10-20T13:25:00-03:00 (after wave 1, before any round-18 REA run)"`.
- The only commit that touches claims.json is FRZ, committed at 13:23:55 −03:00.
- calib-aether's REA run began at 16:24:07Z, i.e. 13:24:07 −03:00 (`runs/calib-aether/receipt.json:1884`; its ghidra.log:1 is 13:24:09).
- So the label is dated 65 s after its own commit, and "before any REA run" is false at the stated time.
- The real ordering still holds: freeze commit, then first REA run 12 s later, then this run 83 s after the commit. [INF] All of these timestamps are self-recorded; there is no external timestamp authority.

## 4. Residual risk and verification gaps

- **R1 — non-diagnostic label.**
  - h0 = h1 = `none` (PRED:19-20), and decision-rule.json:3-5 lists it as `calibration_only`. Its table row is decision-rule.json:38-47.
  - A match here carries no weight for H1 versus H0. w1/SwissMisreadTool.md:46 already calls it a "vacuous negative".
  - The census explains why: the binary has no named map types.
- **R2 — polling-copy truncation (receipt.json:24).**
  - The log ends at LOG:127, terminated by a newline, 0.5 s before the analyze step exits.
  - [INF] A Go markup failure cannot be hiding in the missing tail. In all 3 failing logs the failure line comes before `REPORT: Analysis succeeded`:
    - aether: lines 97/177, before 238;
    - kimi: lines 73/206, before 257;
    - s1246-swiss-nethttp: lines 408/451, before 498.
  - This log already reached REPORT at LOG:121, with the completion markers present.
- **R3 — weak in-log hash.** The log carries only a 48-bit sha256 prefix plus the full MD5. Binding to the full sha256 rests on the receipt's pre/post hashes (receipt.json:8-9).
- **R4 — benign WARN lines.**
  - LOG:73-75 are GoTypeManager WARNs such as `Failed to get subtype '[46912496118442]runtime.elfSym'…`.
  - They are not counted as analyzer errors, which are ERROR-level `Golang*` only (log-extract.py:243-244).
  - Lines of this kind appear in all 12 non-failing logs (3–4 each), including the noswiss controls, so they are a baseline rather than a misread signal [OBS].
- **R5 — no semantic tooling.** No `lsp` device is mounted in this session. The caller and definition checks on `_markup_func` and on walk folding are literal reads plus in-memory execution, not semantic proof.
- **R6 — single log.** There was no REA or Ghidra rerun, which the contract forbids. The observation rests on the single retained log.

## 5. Commands and exit codes (cwd = lane root)

Short checks:

```
git show FRZ:$PRED                                                        # exit 0
git diff FRZ REV -- $PRED ; git diff --quiet FRZ REV -- .ufo/waves/round-18/predictions/   # empty, exit 0 / 0
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $RUN/receipt.json  # exit 0: valid 1, checks_performed 366, findings []
sha256sum ~/.local/bin/notesmd-cli ; md5sum ~/.local/bin/notesmd-cli    # 412dc532…802d / a2d7519d…b270, exit 0
git show REV:$LOG | grep -n -E '\(GoApiSnapshot\)|Using Go API snapshot|Go analysis failure|Invalid index:|Unable to read past EOF:|Untested Go version|Missing Go bootstrap|Using log file:|IMPORTING:|\?MD5='
  # -> lines 2,46,57,62,68,69 only; exit 0
git show REV:$LOG | grep -c -E 'Go analysis failure|Invalid index:|Unable to read past EOF:|Untested Go version|Missing Go bootstrap'
  # -> 0; exit 1 (no match)
git show REV:$LOG | grep -n -E 'Go funcs as NoReturn|Go function signatures|Go missing type names|REPORT: Analysis succeeded'
  # -> 76,77,78,87,121; exit 0
git ls-tree -r REV -- $RUN/ | while read m t b p; do [ "$(git hash-object "$p")" = "$b" ] && echo SAME || echo DIFF "$p"; done   # 17x SAME, exit 0
unzip -p ~/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip ghidra/app/util/bin/format/golang/rtti/types/GoFuncType.java | grep -n -E 'return outCount & 0x7fff|return inCount \+ \(outCount & 0x7fff\)|int count = getParamCount\(\)'   # 79, 86, 98; exit 0
git log -1 --format='%H %cI' FRZ ; git show REV:.ufo/waves/round-18/claims.json | grep -n '"at"'   # 13:23:55-03:00 / :35; exit 0
```

Earlier I also ran a longer independent heredoc extraction over the raw log (exit 0), which gave:
- ERROR lines `[]`;
- WARN lines 68, 73-75;
- MD5 at 57; log path at 2;
- one target `412dc532d278`;
- one session directory, appearing 13 times;
- sha256 `47a14c63…`, file ending in a newline.

Independent census (F-table row; exit 0). Output: `swiss_map_types 63 first 0x62dc60 last 0x62fb60 tflag_values [2] uncommon 0 named 0`.

```
python3 -I -B -c '
import struct;d=open("/home/vgpnk/.local/bin/notesmd-cli","rb").read()
ph,=struct.unpack_from("<Q",d,32);n,=struct.unpack_from("<H",d,56)
L=[struct.unpack_from("<IIQQQQ",d,ph+56*i) for i in range(n)]
def o(v):
  for t,_,f,a,_,s in L:
    if t==1 and a<=v<a+s: return f+v-a
Q=lambda v:struct.unpack_from("<Q",d,o(v))[0]
T0,T1,X0,X1=0x601000,0x6d60e1,0x401000,0x600c11
hits=[]
for t in range(T0,T1-112,8):
  sz,pb=struct.unpack_from("<QQ",d,o(t)); b=d[o(t)+20:o(t)+24]
  if (sz,pb)!=(8,8) or b[3]&31!=21 or b[1:3]!=b"\x08\x08": continue
  k,e,g,h,gs,sl,eo=struct.unpack_from("<7Q",d,o(t)+48)
  if all(T0<=x<T1 for x in (k,e,g)) and o(h) and X0<=Q(h)<X1 and Q(g)==gs and 0<sl and eo<=sl: hits.append((t,b[0]))
print("swiss_map_types",len(hits),"first",hex(hits[0][0]),"last",hex(hits[-1][0]),"tflag_values",sorted({f for _,f in hits}),"uncommon",sum(f&1 for _,f in hits),"named",sum(bool(f&4) for _,f in hits))'
```

F1 variadic decode (exit 0). Output: `InCount 3 OutCount 0x8002 params ['0x626040', '0x6200c0', '0x619300', '0x61c5a0', '0x62ad80', '0x8', '0x8']`.

```
python3 -I -B -c '
import struct;d=open("/home/vgpnk/.local/bin/notesmd-cli","rb").read()
ph,=struct.unpack_from("<Q",d,32);n,=struct.unpack_from("<H",d,56)
L=[struct.unpack_from("<IIQQQQ",d,ph+56*i) for i in range(n)]
o=lambda v:next(f+v-a for t,_,f,a,_,s in L if t==1 and a<=v<a+s)
fn=0x629ce0;i,oc=struct.unpack_from("<HH",d,o(fn)+48)
print("InCount",i,"OutCount",hex(oc),"params",[hex(struct.unpack_from("<Q",d,o(fn+56+8*k))[0]) for k in range(7)])'
```

F1 counterfactual plus frozen-record replay (exit 0). Output:
- `frozen replay==frozen_blob: True walk.failed {'h1': True, 'h0': True} walk.h1.path [... 'func.param[5]'] kind_h1/h0 none none eof_h1 [] inv_h1 [] maps/uncommon 63 0`
- `masked … walk.failed {'h1': False, 'h0': False} walk.h1.path None kind_h1/h0 none none eof_h1 [] inv_h1 [] maps/uncommon 63 0`

```
python3 -I -B -c '
import sys,types,json,subprocess
g=lambda p:subprocess.run(["git","show","eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:"+p],capture_output=True,check=True).stdout.decode()
s=g(".ufo/waves/round-18/tools/swiss-misread.py");R="/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang"
for tag,src in (("frozen",s),("masked",s.replace("count = in_count + out_count","count = in_count + (out_count & 0x7FFF)"))):
    m=types.ModuleType(tag);sys.modules[tag]=m;exec(src,m.__dict__)
    r=m.analyse("/home/vgpnk/.local/bin/notesmd-cli",R)
    print(tag,"replay==frozen_blob:",json.dumps(r,sort_keys=True,indent=2)==g(".ufo/waves/round-18/predictions/swiss-misread/calib-notesmd-cli.json"),"walk.failed",r["walk"]["failed"],"walk.h1.path",(r["walk"]["h1"] or {}).get("path"),"kind_h1/h0",r["predicted_failure_kind_h1"],r["predicted_failure_kind_h0"],"eof_h1",r["predicted_eof_reads_h1"],"inv_h1",r["predicted_invalid_index_reads_h1"],"maps/uncommon",r["map_types"],r["uncommon_map_types"])'
```

F1 sweep over the 15 labels (exit 0). The command is the same loader as above, iterating FRZ `predictions/carriers.tsv` and diffing `predicted_failure_kind_h1/h0`, `predicted_eof_reads_h1/h0`, `predicted_invalid_index_reads_h1/h0` and `diagnostic`. Result:
- `changed_keys []` for all 15 labels.
- `walk.failed.h1/h0` flips only for calib-notesmd-cli (`True -> False`).

## 6. Writes and installs

- Installs: none.
- Writes: this report only.
- During the review I created five scratch files of my own: `/tmp/pred_rev.json`, `/tmp/pred_eb6c.json`, `/tmp/rcn_fs.txt`, `/tmp/rcn_tree.txt`, `/tmp/rcn_emu.json`. All were deleted (`rm -v`, exit 0).
- The emulator runs executed in memory from `git show` source under `python3 -I -B`. No lane file was edited.
- Git was used read-only: `show`, `diff`, `log`, `ls-tree`, `cat-file`, `merge-base`, and `hash-object` without `-w`. No jj, and REA/Ghidra were not run.
