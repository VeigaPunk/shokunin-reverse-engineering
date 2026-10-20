HOLDS

# EmulatorIndependence: is swiss-misread.py carrier-independent? (round 18, wave 2)

Seat: KaidokuR18.EmulatorIndependence, an author-side advisory critic. REV b2aad08ceeee8dd125ce0d316056d8bd766c7f94, freeze eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0.
Scope: `.ufo/waves/round-18/tools/swiss-misread.py`. I checked whether it hard-codes carrier-specific values or is tuned to outcomes, and whether re-runs reproduce the frozen outputs.

**Verdict: HOLDS.**
- The tool contains no carrier-specific literal.
- The held-out indices 22386945 and 15606016, and the calibration pair [17645861, 111938854], come from carrier bytes.
- Re-running the frozen bytes reproduces all 15 frozen outputs as JSON. Each re-run also matches its frozen file byte for byte once the tool's final newline is removed (F4).
- Six sensitivity mutations, including one that fixes a real fidelity bug (F1), change none of the frozen `predicted_*`, `diagnostic` or count fields.
- I found five fixable defects or tradeoffs (F1–F5). None changes a frozen prediction.

Axes named (godspeed): independence (no carrier constants), reproducibility (re-run = frozen), robustness (sensitivity to arbitrary choices), provenance (freeze before runs).

## Blob identity (observation)

| Command | Exit | Result |
|---|---|---|
| `git -C LANE show eb6c266:.ufo/waves/round-18/tools/swiss-misread.py > /tmp/swiss_eb6c/swiss-misread.py && sha256sum …` | 0 | `14924bd6999b2cef4e1d217fa01d5fbb959ec8bb6e58b12959d4f4907f0e3b60`, 1846 lines |
| `git -C LANE diff --quiet b2aad08 eb6c266 -- .ufo/waves/round-18/tools/swiss-misread.py` | 0 | Identical at REV and at the freeze, so the line anchors below hold at REV |
| `git -C LANE diff --quiet eb6c266 -- .ufo/waves/round-18/tools/swiss-misread.py` | 0 | Working tree is unchanged |
| `git -C LANE diff --quiet eb6c266 b2aad08 -- .ufo/waves/round-18/gen-predictions.py .ufo/waves/round-18/predictions` | 0 | Predictions and generator are unchanged from freeze to REV |
| `sha256sum -c predictions/SHA256SUMS` (cwd `.ufo/waves/round-18`) | 0 | 32/32 OK |

The same sha appears as `emulator_sha256` at `.ufo/waves/round-18/predictions/s1246-swiss-nethttp.prediction.json:18` and `predictions/real-kimi-webbridge.prediction.json:18` (REV).

Carrier digests (`sha256sum`, exit 0) match `predictions/carriers.tsv` and the prediction `carrier.sha256`:
- s1246: `5c9faf23…01b6`
- kimi: `71067480…d35d`
- aether: `06c91f55…006e`

## Re-run on the frozen bytes (observation)

Every run below used the frozen tool with `--golang-root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`.

| Command | Exit | Result |
|---|---|---|
| `python3 -I -B /tmp/swiss_eb6c/swiss-misread.py --carrier ~/.local/share/kaidoku-r18/carriers/s1246-swiss-nethttp …` | 0 | |
| `cmp` of that output against `predictions/swiss-misread/s1246-swiss-nethttp.json` | 1 | `EOF on frozen after byte 17560`: re-run is 17561 B, frozen is 17560 B |
| Same pair for `~/.kimi-webbridge/bin/kimi-webbridge` | 0 / 1 | 66675 B vs 66674 B |
| Same pair for `/usr/bin/aether` (calibration) | 0 / 1 | 56517 B vs 56516 B |
| Python check: `json.loads(rerun) == json.loads(frozen)` and `sha256(rerun[:-1])` | 0 | All three are JSON-equal. Without the final LF the shas are 98e079e9…, 9d7d46f6… and 3a99b910…, which equal the SHA256SUMS entries |
| `python3 -I -B /tmp/swiss_eb6c/replay_all.py` (all 15 `carriers.tsv` rows) | 0 | `SUMMARY: 15/15 reproduce`: exit 0, JSON-equal, byte-equal apart from the final LF |
| `python3 -I -B /tmp/swiss_eb6c/swiss-misread.py --selftest` | 0 | `SELFTEST: CLEAN cases=15` |

Frozen held-out values:
- s1246: `predicted_invalid_index_reads_h1 = [22386945]`, h0 `none`.
- kimi: `[15606016]`, h0 `none`.

## No carrier-specific literal (observation)

- **Literal search.** `git show REV:…/swiss-misread.py | grep -n -i -E "22386945|15606016|17645861|111938854|0x0*1559901|0x0*ee2100|0x0*10d4125|5c9faf|71067480|06c91f55|kimi|nethttp|webbridge|notesmd"` exits 1 (no match). The list covers the decimal values, their hex forms (0x1559901, 0xee2100, 0x10d4125), the sha prefixes and the label names.
- **"aether" mentions.** "aether" appears only in comments: the docstring at `swiss-misread.py:8` and the fixture comment at `:1679`.
- **Address-scale literals.** These appear only in selftest fixture code: `:1601`, `:1675`, `:1724` and `:1764`.
- **Inputs.** The tool reads only three things: carrier bytes (`:1254`), snapshot JSON (`:300`) and the diff-directory names (`:271`). It has no subprocess, network or environment input; the imports are at `:43-51`.
- **Generator.** The generator passes only `--carrier` and `--golang-root` (`.ufo/waves/round-18/gen-predictions.py:47`). It computes D from the emulator's own `diagnostic` (`gen-predictions.py:77`).
- **Computed diagnostic set.** Across the 15 frozen outputs, `diagnostic = true` holds exactly for {calib-aether, s1246-swiss-nethttp, real-kimi-webbridge}. Those three labels are D in `decision-rule.json`, so D was not hand-picked.
- **Hard-coded ABI constants.** The remaining constants are amd64 ABI values: `0x30`, `0x17` and `0x28` at `:511-520`, and the `0x58` SlotSize read at `:1364`. On amd64 they equal the values the tool's own `Layout` derives from `go1.24.0.json`: Type size 0x30, `Kind_` 0x17, `Str` 0x28, `SwissMapType.SlotSize` 0x58. The `0x58` read feeds only the report field `slot_size` (`:1368`), never an outcome.

## Independent byte derivation (observation; no code shared with the tool)

`/tmp/swiss_eb6c/derive_all.py` re-reads the pkgPath chain from raw ELF bytes:
- Uncommon type at map + 88 (H1) or map + 112 (H0).
- The name is flags u8, then LEB length and bytes, then an optional tag, then pkgPath u32.
- `invalid_index` when the address is past the last PT_LOAD byte; `past_eof` when the read's tail crosses it.

Result: `SUMMARY: 15/15 agree` (exit 0). H1 and H0 eof/invalid lists equal the frozen lists for every label.

Limitation: the script takes `module.types` and the map addresses from the frozen JSON. I corroborated `types` separately:
- `nm` gives `runtime.types` 0x553000 (s1246) and 0x552000 (s1250), equal to the emulator's values.
- kimi is stripped; its `.rodata` starts at 0x882000, equal to the emulator's value.
- aether is stripped; the emulator uses 0x954020 (.rodata + 0x20). That value is validated by the retained calibration EOF match, not by this check.

Self-contained reproduction (exit 0). The only inputs are the types base (from nm/readelf) and the map addresses:

```
python3 -I -B -c '<inline script: map+88 -> pkgPath; name at types+pkgPath; skip LEB name and tag; next = types + u32>'
s1246-swiss-nethttp map=0x58b0a0 H1 pkgPath=40 name@0x553028 flags=0x6d next_name_index=22386945 max_index=7627183 invalid_index=True
s1246-swiss-nethttp map=0x58dc60 H1 pkgPath=40 name@0x553028 flags=0x6d next_name_index=22386945 max_index=7627183 invalid_index=True
kimi-webbridge map=0x944e80 H1 pkgPath=40 name@0x882028 flags=0x67 next_name_index=15606016 max_index=14449487 invalid_index=True
(also 0x94b780, 0x95f5a0 -> 15606016)
```

**Mechanism.** The 40 is the low dword of SwissMapType.SlotSize, which is 40 for `map[string][]string`. Read early, it sends the name lookup to `types+40`, which is the first rtype's Str/PtrToThis bytes. That name's pkgPath then points past the image. Every number in this chain comes from bytes.

## Provenance (observation; bounded)

- **Freeze before runs.**
  - The freeze commit eb6c266 is at 2026-10-20T13:23:55-03:00 and is an ancestor of REV (`git merge-base --is-ancestor`, exit 0).
  - The runs start after it: `runs/run-log.txt:1` names producing revision eb6c266; `:2` aether starts 13:24:07, `:22` s1246 at 13:28:55, `:30` kimi at 13:31:09.
  - `git log -S 22386945` and `-S 15606016` first hit eb6c266.
- **No earlier Ghidra run found.** I searched pre-freeze `ghidra.log` files under /tmp (depth ≤ 7) for the REA target names `target-5c9faf239ed2` and `target-71067480bd99`: no match (`xargs grep`, exit 123). The only pre-freeze occurrence of either index string is the wave-1 connector's own byte derivation (`w1/ConnC3Prediction.md:130`). That is a prediction, not an observation.
- **Retained compares at REV.** `runs/s1246-swiss-nethttp/compare.json:51-57` and `runs/real-kimi-webbridge/compare.json:53-59` record `extra.invalid_index_reads` match true with observed [22386945] and [15606016]. I only read these files; I did not re-run them.
- [INFERENCE] The commit and run-log timestamps are self-reported. My search does not prove that no off-tree run happened.

## Sensitivity: the strongest counterexample available

`python3 -I -B /tmp/swiss_eb6c/mutate.py` (exit 0) applied six mutations to /tmp copies. Each anchor had to match exactly. Every mutation ran on s1246-swiss-nethttp, kimi, aether, s1246-noswiss-nethttp and s1250-swiss-nethttp, and the result was compared against the frozen `predicted_*`/`diagnostic`/count fields:

| Mutation | Effect on frozen fields |
|---|---|
| M1: mask the variadic bit, `out_count & 0x7FFF` (`:939`, `:1047-1048`) | none |
| M2: `tflag > 0x0F` → `> 0x1F` (`:748`) | none |
| M3: caps ×8–250 (`:54-55`, `min(…,4096)`, `60000`) | none |
| M4: wider moduledata window and span (`:583`, `:593`) | none |
| M5: fold walk failures into the boolean (`:1465-1466`) | kimi and aether only: `predicted_failure_h0` false→true, `kind_h0` none→unknown. H1 fields unchanged |
| M6: no gap scan | none |

The frozen held-out H1 predictions do not depend on the tool's arbitrary bounds or approximations.

## Findings (all fixable; none changes a frozen prediction or the C3 verdict path)

### F1. Unmasked variadic OutCount (fidelity defect in the walk)

**Observation.**
- `swiss-misread.py:939` (`count = in_count + out_count`) and `:1047-1048` do not mask bit 0x8000.
- Ghidra masks it: `Base-src.zip:ghidra/app/util/bin/format/golang/rtti/types/GoFuncType.java:85-86` (`inCount + (outCount & 0x7fff)`), used at `:98`.
- Repro: monkeypatch `Machine._markup_func` and run on kimi (exit 0). Both the h0 and h1 walks end at func 0x8cf120 with `InCount=2 OutCount=0x8000`. The tool walks 32770 params instead of 2, reads `func.param[5]` = 8, and reports "unmapped at 0x8".
- So the frozen `walk` blocks are emulator artifacts: kimi h0 and h1, and aether h0 (M1 turns aether h0 from `unmapped` into `invalid_data`).
- The comment at `:1461-1464` attributes walk divergence to "alignment/validity" filtering. On kimi the first divergence is actually this bug.

**Axes:** depth, calibration (evidentiary value of `walk`).

**Fix:** mask at `:939` and `:1047-1048` in a future tool version. Note in the knowledge entry that the r18 `walk` blocks for kimi and aether are artifacts. The frozen tool must not be edited.

### F2. H0 "none" on real carriers rests on an undocumented carve-out (tradeoff)

**Observation.**
- `:1461-1466` excludes walk failures from `predicted_failure`, while `:1445-1456` folds walk eof/invalid reads into the lists.
- With M1 applied, the emulator's own true-layout walk still fails on kimi and aether (`invalid_data`). M5 shows that the frozen H0 `none` depends on the carve-out.
- The carve-out applies to every carrier and leaves the H1 fields unchanged, so it is not tuned to the held-out outcomes.
- It is not listed in `limits` (`:1486-1495`).

**[INFERENCE]** No effect on the verdict: "refuted" requires a held-out D label to show no Go analysis failure, and both retained compares show the failure.

**Axes:** calibration.

**Fix:** add a `limits` line, or report `predicted_failure_h0_walk` separately.

### F3. amd64-only literals contradict the 32-bit `limits` claim

**Observation.**
- `:1494-1495` says 32-bit carriers use "the same JSON layout law with ptr_size=4".
- But `:511-520` (0x30/0x17/0x28), `:1364` (0x58) and the `<Q`/`<QQQ` unpacks are fixed amd64 values.
- For ptr 4 the snapshot gives Type size 0x20, `Kind_` 0xf, `Str` 0x18, SlotSize 0x34 (layout check, exit 0).
- No impact on the 15 amd64 labels.

**Axes:** calibration.

**Fix:** derive these values from `Layout`, or raise `EvalError` for ELFCLASS32.

### F4. Frozen JSON is re-serialized, not raw stdout (operability)

**Observation.**
- The tool writes a final LF (`:1840-1841`).
- `gen-predictions.py:50` re-dumps the parsed JSON with no trailing LF.
- So a naive `cmp`/`sha256sum` of a re-run against SHA256SUMS fails by one byte. Equality holds as JSON or as stdout minus its final LF.

**Fix:** document that comparison recipe, or have the generator write the tool's stdout verbatim.

### F5. Selftest never exercises the branch both held-out predictions use (coverage)

**Observation.**
- `git show REV:…/swiss-misread.py | awk 'NR>=1746&&NR<=1812' | grep -c -E "invalid_index|predicted_invalid"` prints 0 (exit 1).
- The selftest asserts only the aether-shaped `past_eof` branch (`:1764`). Both held-out predictions take the `invalid_index` branch of `read()` (`:671-672`).
- The REV compares validate that branch after the fact, but the tool itself does not.

**Fix:** add a fixture whose pkgPath target is past `max_index`, asserting `[index]`.

### Minor: hard-coded selftest root

The selftest default `--golang-root` (`:1824`) is a fixed path on this host, not a carrier value; frozen runs pass the root explicitly (`gen-predictions.py:47`).

## Impacted axes

- **Calibration (F2, F3):** the `limits` text and the H0 wording overstate the tool's results.
- **Depth (F1, F5):** the `walk` blocks are emulator artifacts, and the selftest does not cover the `invalid_index` branch.
- **Operability (F4):** a raw byte or sha comparison of a re-run against SHA256SUMS fails by one byte.

**No regression and no duplicate authority found.**

## Housekeeping

- **Tools:** no installs or updates. I used the existing `python3`, `git`, `readelf`, `nm` and `unzip -p` (to read source text only). No REA, no Ghidra, and no carrier execution.
- **Scratch:** everything lives in `/tmp/swiss_eb6c/` (frozen tool copy, outputs, `replay_all.py`, `independent_derive.py`, `derive_all.py`, `mutate.py`, `mut-*.py`), outside the lane. This report is my only lane write.
