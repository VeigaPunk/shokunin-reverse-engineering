# RevLogExtractScope — where the aether strings live, and the EOF parse rule

Snapshot: live working tree `W17/tools/log-extract.py` sha256
`1cc7e59ace32839a75d16a9323380448653d81c44e2d8e6b28fee3ebc11c5094` (concurrent
`LogExtractEof` edit; committed baseline `9011581` sha256
`37a2da2c460fe7519cf528985c9faf71ca145d529b5cb307d266c4a56e1f4454`).
Read-only: no REA analyze/search/decompile, no carrier execution, no installs.
Axes: **A1 calibration** (do the cited lines mean what the labels say?),
**A2 operability** (can a parser recover the pair from the retained bytes?),
**A3 depth** (does the capture mechanism support the claim?).

Verdict: `Go analysis failure` occurs only on the timestamped `ERROR` record at
**line 97**; `Unable to read past EOF: 17645861, 111938854` occurs only on the
non-record `Caused by:` continuation at **line 177**. Both retained aether logs
(pass 1 `da64646`, pass 2 working tree) have them at the same lines; the other
14 of the 16 logs contain neither string. The live edit already scans raw lines
and recovers `[[17645861, 111938854]]` on both aether logs with old fields equal
on 16/16; the remaining advice is to harden that rule against torn polling
captures and to tighten two regex details.

## 1. Corpus and hit map (16 logs, all checked)

`W17` = `.ufo/waves/round-17`; paths below are relative to LANE
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

| label | lines WT / rev | grep rc WT | grep rc rev | hits |
|---|---|---|---|---|
| calib-esbuild-0.25.12 | 124 / 124 | 1 | 1 | none |
| calib-shfmt | 125 / 125 | 1 | 1 | none |
| **pro-aether** | **244 / 244** | **0** | **0** | **97, 177** |
| pro-containerd-shim | 282 / 282 | 1 | 1 | none |
| pro-esbuild-0.21.5 | 123 / 123 | 1 | 1 | none |
| pro-esbuild-0.27.7 | 104 / 104 | 1 | 1 | none |
| pro-notesmd-cli | 127 / 127 | 1 | 1 | none |
| pro-op | 115 / 115 | 1 | 1 | none |

Aether paths and identities:

- pass 1 (`da64646`, first-run): `W17/runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log`,
  244 lines, 22,462 bytes, sha256 `f39c329338a7fc2262eceaaa681a8ad9328feef05b61ebbaba4417e2a9f0b4ed`.
- pass 2 (working tree): `W17/runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log`,
  244 lines, 22,463 bytes, sha256 `5e6d8563050dea00507d0b8a75817bc6945cd56b33176ddc71aa48cd51dc2939`;
  the receipt records this exact sha and 148 polls
  (`W17/runs/pro-aether/receipt.json` → `retained_logs[0].files.ghidra.log.sha256`,
  `polls`, `last_copy_utc = 2026-10-20T14:32:02.978472+00:00`).
- Both passes: line 177 is byte-identical; line 97's message (after the
  timestamp) is identical. Raw line-by-line comparison: 96 differing lines
  (timestamps, session path, analysis timings); after normalizing timestamps and
  session paths, 28 line pairs differ (28 insertions / 28 deletions), all
  timings. Line 177 is in neither set.
  Pass-1 line 97 is `10:50:08`, pass-2 line 97 is `11:30:53`.

All 16 files end with `\n` (checked with `tail -c1`/Python); no torn final line
in this corpus.

## 2. Exact placement and stack-trace format

Working-tree aether, lines 97–200 (`repr()` of the parsed lines):

```
97   '... 11:30:53 ERROR (GolangSymbolAnalyzer) Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException'
98   '\tat ghidra.app.util.bin.format.golang.structmapping.ReflectionHelper.callGetter(ReflectionHelper.java:330)'
...  (frames; each line begins with TAB + "at ")
172  'Caused by: java.lang.reflect.InvocationTargetException'
176  '\t... 73 more'
177  'Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854'
178  '\tat ghidra.app.util.bin.MemoryByteProvider.ensureBounds(MemoryByteProvider.java:312)'
...  (frames)
197  '\tat java.base/jdk.internal.reflect.DirectMethodHandleAccessor.invoke(DirectMethodHandleAccessor.java:103)'
198  '\t... 75 more'
199  ' '          (one space; log4j separator)
200  '... 11:30:54 ERROR (PngDataType) Invalid PNG data at 00659d7a  '
```

- **Line 97**: level `ERROR`, component `GolangSymbolAnalyzer`; message begins
  `Go analysis failure ` and carries the *outer* exception's `toString`
  (`java.io.IOException: java.lang.reflect.InvocationTargetException`). It does
  **not** contain the EOF text and has no trailing two-space padding (unlike
  most record lines, e.g. line 200).
- **Line 177**: **no timestamp, no level, no component**. It is the second
  `Caused by:` line and starts at **column 0** (the frames are tab-indented).
  The EOF text is therefore invisible to `LINE_RE` and to `message`.
- Trace extent: record 97 → `... 75 more` 198 = **10,097 bytes**;
  line 177 starts at byte 16,964 and ends at 17,041; file 22,463 bytes.
- Format source (installed `Base-src.zip`):
  `ghidra/app/util/bin/MemoryByteProvider.java:289-293` rejects a negative or
  oversized length first; `:311-312` is
  `throw new EOFException("Unable to read past EOF: %s, %d".formatted(Long.toUnsignedString(index), length))`.
  So: index is **unsigned decimal** (1–20 ASCII digits), length is decimal
  `0..Integer.MAX_VALUE`, separator is exactly `, `.
  `ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java:181-182` is
  `catch (IOException e) { Msg.error(this, "Go analysis failure", e); }`;
  the record line is the logger's rendering of that call.

## 3. Why the current parser cannot see line 177

`W17/tools/log-extract.py:153` splits on `"\n"` only; `:155-157` matches
`LINE_RE` and `continue`s on any non-record. Line 177 has no timestamp, so it is
dropped before component/message handling. Observation on the committed tool:

- `go_lines` line numbers on the aether log: `[91,92,93,94,95,96,97,207]` —
  177 absent.
- `analyzer_errors = ['Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException']`;
  `classification = 'snapshot_loaded'`; no EOF field existed.
- The record already appears in the pass-2 r17 observation three times
  (`observation.json:3, :55, :56`) but the EOF pair appears nowhere outside
  `ghidra.log`; searching all `W17/runs` artifacts found the pair only in that
  one file. There is no JSON fallback.
- `predictions/replicate-expectations.json:32` records `log_contains` for the
  pair, but no `.py`/`.sh` in the lane reads `log_contains`
  (`grep -rn "log_contains" --include='*.py' --include='*.sh' .` → rc=1).
  Both aether `compare.json` are `"all_match": true` (`compare.json:2`), so the
  r17 comparison was blind to the failure. The new `eof_reads` extra expectation
  is the first mechanical consumer.

## 4. Is a stack-trace line inside the polling-prefix capture guaranteed?

**No by construction; yes for this capture, conditionally.**

Mechanism:

- `W17/tools/carrier-run.py:9-11` states the limitation ("polling copy ... lines
  written after the final poll before REA deletes its runtime root can be
  missing"); `:42-44` repeats it as `LOG_CAPTURE_LIMIT`.
- `:226` does `data = open(src, "rb").read()` — a whole-file read with no lock
  or size snapshot against the writer; `:241-247` writes `.tmp` then
  `os.replace`.
- `:465-498` polls while the child runs (`:663`, `--poll` default 0.5 s), then
  after `proc.wait` calls `poller.scan()` as a "final best-effort catch".
- Therefore the retained `ghidra.log` is the log's **byte prefix at the last
  successful copy** (assuming an append-only file), and a read can end anywhere,
  including mid-line.

Observation for aether: the capture extends 46 lines beyond the trace end
(lines 199–244; `244 − 198`) and 67 lines beyond line 177, with the last line at
11:32:02 versus the failure at 11:30:53 (69 s). Both aether passes have the trace. All 16 captures
end at the same phase line (`ANALYZING changes made by post scripts: ...`), as
do the pilot and the `verify/replicate/calib-shfmt` capture; whether that is the
log's natural end or a common capture boundary is **inference** the retained
files cannot settle. What is certain is the ordering: line 244 (22,304–22,462 B)
is in the capture, so if the file is append-only, every byte before it,
including the whole 97–198 trace, is in the capture. That is why line 177 is
present here.

The counter-case is real: a copy that ends in the 79-line / 7,929-byte band
between line 98 (byte 9,035) and line 176 (byte 16,963) contains
`symbol_analysis_failures` but **no** `eof_reads`; a copy ending inside a
partially written line can even truncate the second number. So the two new
fields are independent evidence:

- EOF pair present ⇒ record present (file order), but
- record present ⇏ EOF pair present (capture may cut between 97 and 177).

Do not make `eof_reads` a precondition for recognizing a failure, and do not
read `eof_reads: []` as "no EOF failure" when the record line is present.

## 5. Parse rule for LogExtractEof (live snapshot)

What the live edit already does correctly:

- `:106` `EOF_READ_RE = re.compile(r"Unable to read past EOF: (\d+), (-?\d+)")`;
  `:168-171` scans **every raw line before the `LINE_RE` guard**, so line 177 is
  caught; duplicates and file order are preserved.
- `:179-180` collects `symbol_analysis_failures` from the parsed record
  `message` with the exact phrase, before the component gate; `:283` dedupes it
  like `analyzer_errors`.
- `:282-283` adds only the two top-level keys. Live output on aether:
  `eof_reads = [[17645861, 111938854]]`,
  `symbol_analysis_failures = ['Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException']`,
  `classification` and `analyzer_errors` unchanged.

Keep all of that. Tighten, in priority order:

1. **Anchor the match at end of line** (medium). Use
   `r"Unable to read past EOF: ([0-9]{1,20}), ([0-9]{1,10})\s*$"`. The observed
   and source-defined line ends exactly after the length; `\s*$` tolerates log
   padding while rejecting a suffixed line (`... 111938854x`). For the special case of
   an **unterminated final line** (`text` does not end with `\n`), decide
   explicitly: either accept it (it may be complete but missing the newline) or
   skip it (it may be a truncated number). The current regex silently accepts
   `... 111938` as `[17645861, 111938]`; the 16 retained logs do not exercise
   this, but the same poller runs in r18. A conservative skip is a defensible
   choice; if taken, add a `trailing_newline=False` selftest so the choice is
   tested.
2. **ASCII digits only** (low). `\d` matches Unicode decimal digits and
   `int("١٢")` succeeds; the Ghidra format is ASCII `Long.toString`/`%d`.
   `[0-9]` states the actual grammar.
3. **Drop `-?` on the length** (low). `MemoryByteProvider.java:289-293` throws a
   *different* IOException for `length < 0` before reaching the EOF branch at
   `:311-312`, so a negative length can never follow this prefix. `([0-9]+)`
   is the calibrated shape.
4. **Make the positive fixture byte-faithful** (low). The `eof_stacktrace` case
   (`log-extract.py:476-499`) appends two spaces to the `Caused by:` and `at`
   lines; the real aether continuation lines have **no** trailing spaces
   (record lines mostly do; line 97 itself does not). Keep a record-line variant with trailing spaces; make the
   continuation variant match the observed bytes, otherwise the test proves a
   shape that never occurs.
5. **Add red cases for the capture shapes** (low): an unterminated final
   `Caused by: ... 111938`; `... 111938854x`; and the sibling EOF message
   `java.io.EOFException: Invalid index: 549696843`
   (`MemoryByteProvider.java:302`) which must not populate `eof_reads`. The
   existing `eof_near_miss` covers `1 , 2`, `just 42`, and lowercase phrase.

Backward-compatibility method (matches the dispatch):

- Run the committed bytes (`git show 9011581:.ufo/waves/round-17/tools/log-extract.py`)
  and the edited bytes on the **same path**; compare parsed JSON minus
  `{eof_reads, symbol_analysis_failures}`. Do not compare against the r17
  `observation.json` files directly: `log_path` is an absolute old field and
  differs for extracted `da64646` copies.
- Harness result here (16/16, live snapshot): `oldfields_equal=True` for every
  log; `pro-aether` (both passes) `eof=[[17645861, 111938854]]`, `symfail=1`;
  the other 14 `eof=[]`, `symfail=0` — including the three bootstrap-missing
  logs whose messages are `Go symbol analyzer error: unable to get
  GoRttiMapper`, which correctly do **not** match the phrase.

Consumer note (CompareEofFields): the live `compare.py` adds
`eof_reads` by exact list equality with `observation.get("eof_reads")`; an
observation from the old tool lacks the key, so a predicted `[]` mismatches
even when no EOF occurred. r18 observations must be regenerated by the edited
`log-extract.py`; r17 predictions without the key are unaffected. If a mismatch
occurs, render `symbol_analysis_failures` alongside `eof_reads` so the
truncation signature (`record present, pair absent`) is visible.

## 6. Limits

- One EOF occurrence in 16 logs; the rule's generality rests on the Ghidra
  source format (`MemoryByteProvider:312`) and the two independent passes, not
  on a large sample.
- Append-only assumption for the prefix argument; no lock is held against the
  writer, so a torn tail is possible even though none of the 16 tails is torn.
- A carrier-controlled message could contain the literal prefix; the contract
  says "any line", so the raw scan counts it. Low risk; do not add a component
  filter that would contradict the contract.
- The live file is a concurrent executor's working tree, not a committed
  revision; re-check the sha before integration.

## 7. Commands and exits (observations above)

```text
A=.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log
B=.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-JpGezV/ghidra.log

$ for f in .ufo/waves/round-17/runs/*/logs/*/ghidra.log; do out=$(grep -n -E 'Unable to read past EOF|Go analysis failure' "$f"); rc=$?; printf 'rc=%d %s :: %s\n' "$rc" "$f" "${out:-<none>}"; done
# per-file rc: 1 1 0 1 1 1 1 1; pro-aether rc=0 -> lines 97 and 177; loop exit 0
$ for f in $(git ls-tree -r --name-only da64646 -- .ufo/waves/round-17/runs | grep 'ghidra.log$'); do out=$(git show da64646:$f | grep -n -E 'Unable to read past EOF|Go analysis failure'); rc=$?; printf 'rc=%d %s :: %s\n' "$rc" "$f" "${out:-<none>}"; done
# same 8 rcs; pro-aether rc=0 -> lines 97 and 177; loop exit 0
$ sha256sum "$A"
# 5e6d8563050dea00507d0b8a75817bc6945cd56b33176ddc71aa48cd51dc2939  (22,463 bytes, 244 lines)
$ git show da64646:"$B" | sha256sum
# f39c329338a7fc2262eceaaa681a8ad9328feef05b61ebbaba4417e2a9f0b4ed  -  (22,462 bytes, 244 lines)
$ git show 9011581:.ufo/waves/round-17/tools/log-extract.py | python3 -I -B - --log "$A"
# exit 0; go_lines [91..97,207] (177 absent); no eof_reads/symbol_analysis_failures keys
$ python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log "$A"
# exit 0; eof_reads [[17645861, 111938854]]; symbol_analysis_failures has 1 entry
$ git show 9011581:.ufo/waves/round-17/tools/log-extract.py | python3 -I -B - --selftest
# SELFTEST: CLEAN cases=8 ; exit 0
$ python3 -I -B .ufo/waves/round-17/tools/log-extract.py --selftest
# SELFTEST: CLEAN cases=11 ; exit 0
$ unzip -p /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip ghidra/app/util/bin/MemoryByteProvider.java | sed -n '289,293p;311,312p'
# exit 0; negative/oversized-length guard and "Unable to read past EOF: %s, %d"
$ unzip -p /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip ghidra/app/plugin/core/analysis/GolangSymbolAnalyzer.java | sed -n '181,182p'
# exit 0; catch (IOException e) / Msg.error(this, "Go analysis failure", e)
$ diff -u <(git show da64646:"$B" | sed -E 's/^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}/TS/; s#/tmp/kr17-rea-[a-z0-9]+/rea-ghidra-[A-Za-z0-9]+#/SESS#g') <(sed -E 's/^[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}:[0-9]{2}/TS/; s#/tmp/kr17-rea-[a-z0-9]+/rea-ghidra-[A-Za-z0-9]+#/SESS#g' "$A")
# exit 1 (expected: content differs); 28 changed line pairs (28 insertions / 28 deletions), all analysis timings; line 177 not in the diff
$ python3 - <<'PY'   # 16-log old-vs-new harness: old script via `git show 9011581:...`; temp copies of the 8 da64646 logs; compare parsed JSON minus the two new keys
# exit 0; oldfields_equal=True 16/16; pro-aether eof pair on both passes, 14 empty
PY
$ grep -rn "log_contains" --include='*.py' --include='*.sh' .
# exit 1; no code consumer
```

This seat wrote only this report; no `jj`/git writes, no REA run, no installs.
