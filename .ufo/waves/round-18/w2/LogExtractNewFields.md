HOLDS

# LogExtractNewFields — r18 wave-2 falsification of w1 LogExtractEof

Re-ran `.ufo/waves/round-17/tools/log-extract.py` (REV b2aad08, sha256
`eb8f2c7858869a84010be8f964b845a53f200f28c6f256899ab7f77e79a83d74`;
`git status --porcelain` on the file = clean, i.e. working tree == REV)
on all 15 r18 logs + 16 r17 logs (8 working-tree
`.ufo/waves/round-17/runs/*/logs/*/ghidra.log` + 8 extracted via
`git archive da64646 .ufo/waves/round-17/runs` into `/tmp/logext-w2/r17-archive`
— same 16-log convention as w1/LogExtractEof.md). All observations.

## 1. Selftest

| command | exit |
|---|---|
| `python3 -I -B .ufo/waves/round-17/tools/log-extract.py --selftest` | 0 — `SELFTEST: CLEAN cases=13` |

## 2. Per-log extraction (all 31 exits 0)

Current tool `--log <path>` exit 0 for all 15 r18 + 16 r17 logs.
New-field JSON output vs `grep -nE` on raw lines (OBSERVATION):

| log | `eof_reads` | `invalid_index_reads` | raw anchor |
|---|---|---|---|
| r17 wt+arc `pro-aether` (2 logs) | `[[17645861, 111938854]]` | `[]` | `ghidra.log:177` continuation `Caused by: java.io.EOFException: Unable to read past EOF: 17645861, 111938854` |
| r18 `calib-aether` (HtDopV) | `[[17645861, 111938854]]` | `[]` | `ghidra.log:177` identical continuation |
| r18 `real-kimi-webbridge` (ZSUHpG) | `[]` | `[15606016]` | `ghidra.log:206` `Caused by: java.io.EOFException: Invalid index: 15606016` |
| r18 `s1246-swiss-nethttp` (zHRS1l) | `[]` | `[22386945]` | `ghidra.log:451` `Caused by: java.io.EOFException: Invalid index: 22386945` |
| all other 26 logs | `[]` | `[]` | `grep -nE '…[ \t]*$'` exit 1 (no match) |

Commands (each per log, all 31):
`grep -nE 'Unable to read past EOF: [0-9]+, [0-9]+[ \t]*$' <log>` — exit 0 on the
3 logs listed above, exit 1 elsewhere.
`grep -nE 'Invalid index: [0-9]+[ \t]*$' <log>` — exit 0 on the 2 r18 logs above,
exit 1 elsewhere.
Unanchored control `grep -cE 'Unable to read past EOF|Invalid index'` — same
counts (1 each in exactly those logs): no near-miss lines the anchoring drops,
no suffixed forms. `cat -A` on all five matched lines: each ends exactly at the
digits (`…111938854$`, `…15606016$`, `…22386945$`), no trailing whitespace.
All 31 logs end with `0a` and contain zero `\r` bytes (`grep -c $'\r'` = 0,
`tail -c1 | xxd -p` = `0a`), so the tool's torn-line and CR-strip paths
(`log-extract.py:181-183`) cannot diverge from grep here.
Field order/count verified: JSON arrays equal grep match lists 1:1 (max one
match per line by EOL anchor, and grep `-n` confirms exactly one matching line
per log).

Note (INFERENCE): the two r18 `Invalid index` hits arrive via the
`Caused by: java.io.EOFException: Invalid index: N` continuation form —
emission site `MemoryByteProvider.java:302` per the adjacent stack frame
(`ghidra.log:207`/`452`: `at ghidra.app.util.bin.MemoryByteProvider.ensureBounds(MemoryByteProvider.java:302)`),
distinct from aether's `Unable to read past EOF` pair (`:311-312`). The
EOL-anchored raw-line scan at `log-extract.py:188-190` catches it as designed.
Also observed: `symbol_analysis_failures` non-empty in exactly the same 5 logs
(`["Go analysis failure java.io.IOException: java.lang.reflect.InvocationTargetException"]`,
records at `ghidra.log:97` aether-wt/arc + calib-aether, `:73` kimi, `:408`
swiss-nethttp) — consistent with each failure having an EOF-flavoured cause.

## 3. Old-field byte-equality vs baseline extractor (16 r17 logs)

Baseline tool materialised read-only:
`git show 9011581d84527ba34c675f9cf912e54d2e72d470:.ufo/waves/round-17/tools/log-extract.py > /tmp/logext-w2/log-extract-baseline.py`
→ sha256 `37a2da2c460fe7519cf528985c9faf71ca145d529b5cb307d266c4a56e1f4454`
— identical to w1's recorded pre-edit sha (w1/LogExtractEof.md "pre-edit
sha256"), confirming `9011581` predates the r18 additive change.

For each of the 16 logs:
`python3 -I -B /tmp/logext-w2/log-extract-baseline.py --log <L>` (exit 0) and
`python3 -I -B .ufo/waves/round-17/tools/log-extract.py --log <L>` (exit 0);
then in Python: drop `eof_reads`, `invalid_index_reads`,
`symbol_analysis_failures` from the new output and compare
`json.dumps(…, sort_keys=True, indent=2)` byte strings.

Result: `16 EQUAL / 16`, zero mismatches (loop printed `TOTAL=16`, every line
`EQUAL old_exit=0 new_exit=0`).

## Verdict

HOLDS on all three assignment axes: selftest clean (13 cases), new
`eof_reads`/`invalid_index_reads` fields reproduce exactly against anchored
`grep -nE` on all 31 logs (including the two r18-only `Invalid index` hits the
r17 corpus never exercised — the wave-1 claim "all 16 logs yield
invalid_index_reads: []" still holds for r17, and the field is live and
correct on r18 data), and old fields are byte-equal to the `9011581` baseline
extractor on all 16 r17 logs.

## Reproduction / hygiene

- No lane writes; all artifacts under `/tmp/logext-w2/` (archive extraction,
  baseline tool copy, per-log JSON).
- No installs; python3 stdlib + git + GNU grep only.
- Read-only git used (`git archive`, `git show`, `git ls-tree`, `git status`).
- INFERENCE vs OBSERVATION: all field/grep/diff results above are direct
  command output (observation); the `MemoryByteProvider.java:302` emission-site
  attribution is inference from the adjacent stack frame, not a re-verified
  source read.
