# LogExtractEof — r18 wave-1 report

Scope: additive `eof_reads` + `symbol_analysis_failures` in
`.ufo/waves/round-17/tools/log-extract.py` (contract.md:123-125), tightened
per L1 follow-up (RevLogExtractScope).

## Files changed
- `.ufo/waves/round-17/tools/log-extract.py` (in place; pre-edit sha256
  `37a2da2c460fe7519cf528985c9faf71ca145d529b5cb307d266c4a56e1f4454`,
  backup at `/tmp/log-extract-before.py` — outside lane).
- `.ufo/waves/round-18/w1/LogExtractEof.md` (this report).

## What changed (path:line)
- `log-extract.py:23-34` — docstring: new output fields documented with
  source grounding (`MemoryByteProvider.java:311-312` emits
  `Unable to read past EOF: %s, %d` = unsigned index, int length;
  `:302` emits `EOFException("Invalid index: %s")`, `:173` the IOException
  variant; `GolangSymbolAnalyzer.java:182` emits `Msg.error(this, "Go
  analysis failure", e)`; verified against `Base-src.zip` members). States
  the torn-final-line rule.
- `log-extract.py:106-115` — `EOF_READ_RE = re.compile(r"Unable to read
  past EOF: ([0-9]+), ([0-9]+)[ \t]*$")` and
  `INVALID_INDEX_RE = re.compile(r"Invalid index: ([0-9]+)[ \t]*$")` —
  ASCII digits only (`[0-9]`, not `\d`; both indices are
  `Long.toUnsignedString`), no `-?`, anchored at end of line with optional
  trailing spaces, per L1 RevLogExtractScope/ConnC3Prediction tightening.
- `log-extract.py:170-172` — accumulators `eof_reads`,
  `invalid_index_reads`, `symbol_analysis_failures`.
- `log-extract.py:177-190` — `eof_reads` collects the `[int, int]` pair
  and `invalid_index_reads` collects the `[int]` index from **every raw
  line** via EOL-anchored `search`, before the `LINE_RE` record gate, so
  stack-trace continuations (`Caused by: java.io.EOFException: ...`)
  count; order preserved, duplicates kept. A final line lacking a
  terminating `\n` is torn: `terminated` caps the scanned range (`:181`)
  so it is skipped for both fields only — record parsing of that line is
  unchanged.
- `log-extract.py:198-199` — any parsed record `message` containing
  `Go analysis failure` is collected (before the Go-component gate;
  literal contract reading: "messages containing").
- `log-extract.py:301-303` — output keys: `eof_reads` (all occurrences,
  JSON arrays), `invalid_index_reads` (all occurrences, JSON ints),
  `symbol_analysis_failures` (deduped, first-occurrence order — same
  convention as `analyzer_errors`).
- `log-extract.py:308-637` — selftest cases 8 → 13:
  `eof_stacktrace` (`:497`; EOL-anchored pair on a real-form continuation
  line `Caused by: java.io.EOFException: Unable to read past EOF: A, B`
  with no timestamp, mirrors retained aether log :177),
  `eof_multi_and_failure_dedupe` (`:526`; record + continuation pairs,
  order, dup pairs kept, failure messages deduped),
  `eof_near_miss` (`:553`, RED: `EOF: 1 , 2`, `EOF: just 42`, suffixed
  `EOF: 11, 22 (retrying)`, negative `-3, 7`, lowercase
  `go analysis failure` must NOT populate the new fields),
  `eof_torn_final` (`:578`, RED: complete pair `7, 8` and
  `Invalid index: 9` on an unterminated final line are not counted while
  the earlier terminated lines are), and `invalid_index_case` (`:602`;
  positive `Invalid index: 987654321` on a continuation line, RED shapes
  suffixed `12 (retrying)`, negative `-4`, and Arabic-Indic digits
  `١٢` — the last fails only if `\d` is used instead of `[0-9]`).
  `run_case` gained `trailing_newline` (`:317`) for the torn fixture.

## Backward-compatibility proof (observation)
All 16 retained logs: 8 working tree under
`.ufo/waves/round-17/runs/*/logs/*/ghidra.log` + 8 extracted from
`git archive da64646 .ufo/waves/round-17/runs` into `/tmp/tmp.ru0RJaZL1k`.
For each, pre-edit script output vs post-edit output minus the three new
keys (`eof_reads`, `invalid_index_reads`, `symbol_analysis_failures`) is
**byte-equal** after identical re-serialization
(`sort_keys=True, indent=2`). Verification script:
`/tmp/verify-log-extract-compat.py` (outside lane). Result:
`ALL 16 LOGS: OLD FIELDS BYTE-EQUAL`, exit 0 — rerun after each L1
tightening with the same result. All 16 logs yield
`invalid_index_reads: []` (independent confirmation: `grep -l 'Invalid
index'` over both sets exits 1, no matches).

Aether (working tree `pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log` and
archived `rea-ghidra-JpGezV/ghidra.log`) yields
`eof_reads: [[17645861, 111938854]]` and
`symbol_analysis_failures: ["Go analysis failure java.io.IOException:
java.lang.reflect.InvocationTargetException"]` — pair observed at
`pro-aether/.../ghidra.log:177` (continuation line; `cat -A` confirms it
ends exactly at `111938854` with no trailing whitespace), failure record
at `:97`. All other 14 logs yield `eof_reads: []`,
`symbol_analysis_failures: []`.

## Commands run
| command | exit |
|---|---|
| `find .ufo/waves/round-17/runs -name ghidra.log \| sort` | 0 |
| `git -C LANE ls-tree -r --name-only da64646 -- .ufo/waves/round-17/runs \| grep ghidra.log$` | 0 |
| `grep -n 'EOF\|Go analysis failure' .../pro-aether/.../ghidra.log \| head -40` | 0 |
| `sed -n '90,190p' .../pro-aether/.../ghidra.log` | 0 |
| per-log `grep -c` count loop (8 working-tree logs) | 1 (last `grep -c` had 0 hits) |
| `git archive da64646 ... \| tar -x -C $T` + per-log `grep -c` loop | 1 (same; archive+extract succeeded, 8 logs listed) |
| `cp log-extract.py /tmp/log-extract-before.py && sha256sum` | 0 |
| `unzip Base-src.zip MemoryByteProvider.java GolangSymbolAnalyzer.java` + `grep` | 0 |
| `sed -n '97p;177p' aether log \| cat -A`; `tail -c 20 ... \| xxd` | 0 (EOF line ends at digits; file ends `0a`) |
| `python3 -I -B LANE/.ufo/waves/round-17/tools/log-extract.py --selftest` (first pass) | 0 — `SELFTEST: CLEAN cases=11` |
| `python3 -I -B LANE/.ufo/waves/round-17/tools/log-extract.py --selftest` (after L1 tightening) | **0 — last line: `SELFTEST: CLEAN cases=12`** |
| `python3 /tmp/verify-log-extract-compat.py /tmp/tmp.ru0RJaZL1k` (first pass) | 0 |
| `python3 /tmp/verify-log-extract-compat.py /tmp/tmp.ru0RJaZL1k` (after L1 tightening) | 0 — `ALL 16 LOGS: OLD FIELDS BYTE-EQUAL` |
| `sed -n '165,180p;295,315p' MemoryByteProvider.java` | 0 (`Invalid index: %s` at :302 EOFException, :173 IOException) |
| `python3 -I -B LANE/.ufo/waves/round-17/tools/log-extract.py --selftest` (after ConnC3Prediction) | **0 — last line: `SELFTEST: CLEAN cases=13`** |
| `python3 /tmp/verify-log-extract-compat.py /tmp/tmp.ru0RJaZL1k` (after ConnC3Prediction) | 0 — `ALL 16 LOGS: OLD FIELDS BYTE-EQUAL`; `idx=[]` for all 16 |
| `grep -l 'Invalid index'` over both 8-log sets | 1 (no matches in either set) |

## Decisions / inference
- `symbol_analysis_failures` deduped (INFERENCE: mirrors `analyzer_errors`
  convention; a distinct-messages view is what a comparison consumer
  wants). `eof_reads` and `invalid_index_reads` keep every occurrence in
  log order, one match max per line (EOL anchor), literal contract
  "every line matching".
- L1 tightening applied to both EOF fields: suffixed text after a value,
  `N , N`, a missing second number, a negative length/index, non-ASCII
  digits, and a torn final line do not count. Either dedupe choice for
  `eof_reads` is defensible; only aether's single pair is pinned by
  acceptance.
- The compat harness (`/tmp/verify-log-extract-compat.py`) had to learn
  the third new key; its first run after adding the field reported
  16 × `OLD-FIELD MISMATCH` purely because `invalid_index_reads` was not
  stripped — not a tool regression (the same run showed the field present
  with `[]` everywhere). Corrected harness then passed.
- No installs performed; Python 3 stdlib only.

## Risks / blockers
None. Tool stays read-only on the log; exits 0/1/2 unchanged.
