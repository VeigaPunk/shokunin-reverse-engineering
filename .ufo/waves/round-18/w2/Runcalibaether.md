HOLDS

# Runcalibaether: independent re-derivation of carrier run `calib-aether`

Seat KaidokuR18.Runcalibaether (author-side advisory, read-only). Lane HEAD = REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (observed via `git rev-parse HEAD`, exit 0). Freeze commit is `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. In this report, LOG = `.ufo/waves/round-18/runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log`, PRED = `.ufo/waves/round-18/predictions/calib-aether.prediction.json`, RCPT = `.ufo/waves/round-18/runs/calib-aether/receipt.json`, and RV = `.ufo/waves/round-17/tools/receipt-validate.py`. Every `path:line` anchor is at REV (`git show REV:path`). I did not run REA, Ghidra or the carrier. I installed no tools.

## Verdict per field (all OBSERVED unless labelled)

| Field | Frozen (PRED at eb6c266) | Raw log line (LOG at REV) | Verdict |
|---|---|---|---|
| snapshot_route | `"fallback"` PRED:34 | LOG:92 `WARN (GoApiSnapshot) Falling back from 1.25.14 to 1.25.0`. This is the only `(GoApiSnapshot)` line; there is no INFO GoApiSnapshot line. | HOLDS |
| fallback_to | `"1.25.0"` PRED:31 | LOG:92 `to 1.25.0`. The installed snapshot dir has only `go1.24.0.json` and `go1.25.0.json` for 1.24/1.25. The `go1.25.0.json` sha256 `54d10162…` equals PRED:60. | HOLDS |
| snapshot_label | `"1.25.14"` PRED:33 | LOG:93 `Using Go API snapshot for version 1.25.14`. This echoes the request, so the field carries no information; compare.py:47 already labels it that way. | HOLDS (non-discriminating) |
| untested_version | `null` PRED:35 | No `Untested Go version` line anywhere in LOG. | HOLDS |
| missing_bootstrap | `false` PRED:32 | No `Missing Go bootstrap type info` line (the string log-extract.py:97 looks for). There is one `Reading Go binary info` line, LOG:91. | HOLDS |
| extra.analyzer_errors_contain | `"Go analysis failure"` PRED:38 | LOG:97 `ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException…` | HOLDS |
| extra.eof_reads | `[[17645861,111938854]]` PRED:39-44 | LOG:177 `Unable to read past EOF: 17645861, 111938854`. This is the only EOF line; it is thrown at LOG:178 `MemoryByteProvider.ensureBounds(…:312)`. | HOLDS, and the pair is re-derived from the carrier bytes (below) |
| extra.invalid_index_reads | `[]` PRED:45 | No `Invalid index:` line. | HOLDS |
| Binding: session path | RCPT:2-3, :1911 `/tmp/kr17-rea-f5gqd29i/rea-ghidra-HtDopV` | LOG:2 `Using log file: /tmp/kr17-rea-f5gqd29i/rea-ghidra-HtDopV/ghidra.log` | HOLDS |
| Binding: target-<sha12> | sha256[:12] = `06c91f55df41` | LOG:46 `IMPORTING: file:///tmp/kr17-rea-f5gqd29i/rea-ghidra-HtDopV/target-06c91f55df41.bin` | HOLDS |
| Binding: MD5 | RCPT:6 `7ed7b4528c1a6db417ae00742ba81fcf` | LOG:65 `…target-06c91f55df41.bin?MD5=7ed7b4528c1a6db417ae00742ba81fcf`, which equals `md5sum /usr/bin/aether`. | HOLDS |
| Carrier sha256 | PRED:28 `06c91f55…6178006e` | `sha256sum /usr/bin/aether` gives the same value. It also equals RCPT:8-9 (pre/post), `inspect-go.json`, and the frozen emulator output `predictions/swiss-misread/calib-aether.json`. | HOLDS |
| receipt-validate `--require-mid-maps` | decision-rule.json:2 binding gate | exit 0: `status: valid`, `checks_performed: 372`, `findings: []`. The validator blob `bf04388` is identical at REV and in the working tree; its sha256 `70672eb3…` equals the producer.json pin. | HOLDS |
| Freeze integrity | decision-rule.json:2 | Blob `fff13331` is identical at the freeze commit and at REV. `git log eb6c266..REV -- predictions/` is empty. The freeze tree contains 0 `round-18/runs` files. Freeze commit time is 16:23:55Z and producer `recorded_at` is 16:24:07Z, with `branch_tip` = eb6c266. | HOLDS (timestamps are self-asserted) |
| Retained artifacts at REV | n/a | All 20 run/prediction files are blob-identical between REV and the working tree. | HOLDS |

Timing (OBSERVED, consistent): pins_pre was taken at 16:24:07.2Z. LOG runs from 13:24:09 to 13:25:17 (-03:00). Mid-maps were taken at 16:24:08, 16:24:38 and 16:25:08Z; their sha256 values equal the receipt's `map_sha256`. The last log copy was 16:25:18.27Z and pins_post was 16:25:18.8Z.

## Depth: the EOF pair re-derived from carrier bytes (OBSERVED)

I wrote my own decoder from the Ghidra 12.1.4 `Base-src.zip` source and the Go ABI; it uses none of the emulator's code. The source facts it relies on:
- `MemoryByteProvider.ensureBounds` throws `Invalid index: %s` at :302 and `Unable to read past EOF: index, length` at :311-312.
- `GoVarlenString.readFrom` reads an LEB128 length, then `readNextByteArray(len)`.
- `GoName.readStructure` reads flags, then name, then tag (if HAS_TAG), then pkgPath (if HAS_PKGPATH, bit 1<<2); `getPkgPath` is at :123-124.
- `GoType.getUncommonType` reads at `context.getStructureEnd()`.
- `GoMapType` maps only `{runtime.maptype, internal/abi.MapType, internal/abi.OldMapType}`. In `go1.25.0.json`, `runtime.maptype` is an alias of `internal/abi.OldMapType`.

What the decoder found:
- **Types base is valid.** The `.typelink` section starts at 0x13b4c40 and has 3739 entries. Resolving entries against types = 0x954020 (`.rodata` starts at 0x954000) gives sane names: `***linux._Ctype_char`, `**abi.Type`, `*struct {}`.
- **Exactly 7 uncommon map types.** A brute-force scan of [types, etypes) for kind 21 with tflag&1 finds 7, the same count as PRED `misread_map_types` = 7 and `uncommon_map_types` = 7.
- **Correct reading (H0) fails nothing.** For `http.Header` (0xa350a0), `textproto.MIMEHeader` and `url.Values`, the true uncommon block at +112 resolves pkgPath to `net/http`, `net/textproto` and `net/url` (mcount 13, 5, 6).
- **Swiss layout confirmed.** These three types have SlotSize 40 and GroupSize 328 = 8 + 8×40.
- **The H1 misread reproduces the pair.** Reading uncommon at +88 (OldMapType is 88 bytes) gives pkgPath nameOff 40. The GoName at types+40 (0x954048) has flags 110, so HAS_PKGPATH is set; its pkgPath nameOff is 7864576. The GoName at 0x10d4120 then claims a length of **111938854** with data at index **17645861**. That is exactly LOG:177, for all 3 types.
- **The other 4 types stay silent.** They have SlotSize 24 or 32, so the misread pkgPath GoName lacks HAS_PKGPATH and mcount = 0. This is the same 3 fail / 4 silent split as the emulator's `per_type`.
- **No hard-coded pair.** The emulator source at eb6c266 (sha `14924bd6…`, equal to PRED:18) contains neither literal 17645861 nor 111938854.

The stack frames fit this chain: interface method → func → map type → `getUncommonType` → GoName → `getPkgPath`, at LOG:97-196. [INFERENCE] The log does not name which of the 3 slot-40 types failed first. That does not matter, because all three produce the same pair.

Calibration framing (OBSERVED): calib-aether is listed as `calibration_only` (decision-rule.json:3-7) and is not in `held_out_D` (:15-18). By the frozen rule, its match carries no H1 verdict weight. The r18 log (sha `bb3d2e16…`) is a fresh session, not the r17 `pro-aether` log (sha `5e6d8563…`). After normalizing timestamps, session ids and analyzer durations, the two logs differ in only 2 ms-timing lines (ClassSearcher, Headless startup). So this run is a deterministic replay on identical bytes (same sha256 and MD5) with Ghidra 12.1.4 and rea-agents 6.5.0 (from the npx `package.json`).

## Findings (by severity; none breaks the verdict)

**LOW-1 (OBSERVED): receipt-validate ignores the receipt's self-reported binding fields.** `check_binding` (RV:131-192) re-derives the binding from raw log lines and the on-disk carrier MD5 (RV:155-188). That is the safe direction. But it never reads `carrier.md5_pre` (RCPT:6) or `retained_logs[].binding.*` (RCPT:1893-1895). A receipt that misstates either one still validates. There is no impact on calib-aether: its recorded values agree with the recomputed ones. Reproduction (scratch dir in /tmp, removed afterwards):
```
T=$(mktemp -d /tmp/ca-neg-XXXXXX) && python3 -I -B -c "
import json,subprocess,sys,copy,os
T=sys.argv[1]; V='.ufo/waves/round-17/tools/receipt-validate.py'
base=json.load(open('.ufo/waves/round-18/runs/calib-aether/receipt.json'))
def mut(name,f):
    d=copy.deepcopy(base); f(d); p=os.path.join(T,name+'.json'); json.dump(d,open(p,'w'),indent=1)
    r=subprocess.run(['python3','-I','-B',V,'--require-mid-maps',p],capture_output=True,text=True)
    rc=json.loads(r.stdout)['receipts'][0]; print(name,r.returncode,rc['status'],[x.get('code') for x in rc['findings']])
mut('md5_pre_wrong',lambda d:d['carrier'].__setitem__('md5_pre','0'*32))
mut('binding_flag_false',lambda d:d['retained_logs'][0]['binding'].__setitem__('md5_ok',False))
mut('sha256_post_wrong',lambda d:d['carrier'].__setitem__('sha256_post','0'*64))
" "$T"; rm -rf "$T"     # run in the lane root
```
Results (OBSERVED): `md5_pre_wrong` exit 0 valid; `binding_flag_false` exit 0 valid. The controls are caught: `sha256_post_wrong` exit 1 (`carrier_not_pinned`, `binding_mismatch`, `sha256_mismatch`). Also caught, each exit 1: wrong `session_dir` and wrong `bound_sessions` (`binding_mismatch`), wrong log sha (`sha256_mismatch`), dropped mid-maps (`mid_checks_absent`), and carrier path changed to `/usr/bin/true` (`carrier_not_pinned`, `sha256_mismatch`). The unmodified copy is exit 0 valid.

**LOW-2 (OBSERVED): compare.json does not document the extra-field rules.** Its `rules` block (compare.json:71; source `RULES` at compare.py:45-51) lists only the 5 route fields. The semantics of the three `extra.*` fields are not emitted: `analyzer_errors_contain` is an any-substring test (compare.py:196), and `eof_reads` / `invalid_index_reads` are exact list equality (:211, :216). On its own, `analyzer_errors_contain` would match any Go failure. The mechanism is pinned only by the exact `eof_reads` match. Reproduce with: `git show REV:.ufo/waves/round-18/runs/calib-aether/compare.json | grep -n -A6 '"rules"'`.

## Residual risk and verification gaps

- **The log is a truncated polling copy.** It ends at LOG:244 (`ANALYZING changes made by post scripts`), the same cut point as the r17 log; RCPT:24 acknowledges this. All Go lines come before LOG:208, so the fields are unaffected. [INFERENCE] The post-script re-analysis emitted no further Go errors; this is unobserved.
- **Re-validation depends on the host.** RV:216-245 (`verify_file`, called from :291 and :313) re-hashes the carrier, so after an aether package upgrade this receipt will fail loudly (`missing_file` / `sha256_mismatch`) rather than pass silently. The `md5_ok=None` pass branch (RV:157, :185-189) cannot be reached while those checks fire. [INFERENCE] from the code plus the `sha256_post_wrong` probe.
- **Two decoder inputs came from the emulator's output.** These are the types base (0x954020) and the etypes scan bound. I validated the base independently through `.typelink` names and the `.rodata` start.
- **Ghidra was not run** (contract). Ghidra's read semantics come only from reading its source. Commit timestamps are self-asserted.
- **Scratch files.** I wrote files outside the lane (`/tmp/pred-frozen.json`, `/tmp/r1[78]-aether.log`, `/tmp/r1[78]n`, `/tmp/ca-pred.json`, `/tmp/ca-log`, plus mkdtemp dirs) and removed them all. In the lane I wrote only this report.

## Commands (cwd = lane root unless noted; exit codes observed)

```
git show eb6c2668…:.ufo/waves/round-18/predictions/calib-aether.prediction.json                    # exit 0
grep -n -E "GoApiSnapshot|Go analysis failure|Invalid index|Unable to read past EOF|Using Go API snapshot|Untested Go version|snapshot" ghidra.log   # (log dir) exit 0 -> lines 92,93,97,177
grep -n -E "kr17-rea-f5gqd29i|rea-ghidra-HtDopV|target-06c91f55df41|MD5|…" ghidra.log              # (log dir) exit 0 -> 2,46,65
sha256sum /usr/bin/aether; md5sum /usr/bin/aether                                                    # exit 0 -> 06c91f55…006e / 7ed7b452…1fcf
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/calib-aether/receipt.json   # exit 0, valid, 372 checks, 0 findings
diff <(git show eb6c266:PRED) PRED; git rev-parse eb6c266:PRED REV:PRED                              # exit 0; both fff13331…
git log eb6c266..REV -- .ufo/waves/round-18/predictions/                                             # exit 0, empty
git ls-tree -r REV -- runs/calib-aether PRED decision-rule.json | (git hash-object per path)         # exit 0, 20/20 SAME
python3 -I -B -c '<raw-line field compare vs frozen PRED: route/fallback/label/untested/failure/eof/invalid>'   # exit 0, 7/7 MATCH
diff <(normalize r17 pro-aether log) <(normalize r18 log)                                            # exit 1: only 2 ms-timing lines differ
unzip -p …/Ghidra/Features/Base/lib/Base-src.zip ghidra/app/util/bin/MemoryByteProvider.java | sed -n '296,316p'   # exit 0
python3 -I -B -c '<ELF PT_LOAD + Go ABI decoder: typelink names, 3 slot-40 maps, +88 vs +112 uncommon, GoName chain>'  # exit 0, match=True x3
python3 -I -B -c '<scan [types,etypes) step 8 for kind 21 & tflag&1, recompute H1 chain>'           # exit 0: 7 types, 3 failing, pairs [(17645861, 111938854)]
<LOW-1 mutation script above>                                                                        # exit 0 (harness); per-mutation exits as listed
```
