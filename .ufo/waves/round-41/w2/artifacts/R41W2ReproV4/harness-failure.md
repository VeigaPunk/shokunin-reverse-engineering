# V4 receipt pair: why there is no `run.json`

**Defect (non-scoring for R41-C1, real for evidence traceability).**
`tools/round-41/c1-run.sh` cannot write `run.json` for the V4 carrier. The harness' own
log is committed at `corpus/evidence/round-41/c1/V4/run-harness-failure.log`:

```
tools/round-41/c1-run.sh: line 547: /home/vgpnk/.local/bin/jq: Argument list too long
```

## Mechanism (measured, not inferred)

1. Line 543-547 builds the `receipt` variable:

   ```bash
   receipt=$(jq -n \
     --arg sha "$(sha256sum "$outdir/after.json" | cut -d' ' -f1)" \
     --argjson bytes "$(stat -c%s "$outdir/after.json")" \
     --argjson summary "$summary" \
     '{path: "after.json", sha256: $sha, bytes: $bytes} + $summary')
   ```

   `$summary` is the compact JSON rebuilt at line 524-537 from the receipt's gaps and
   unpublished entries. For the committed V4 receipt that string is **146,561 bytes**
   (recomputed here with the harness' own filter on the committed `after.json`;
   `summary.bin` in the scratch, 146,561 bytes; command substitution strips the newline,
   so the argv string delivered to `jq` is 146,560 bytes).

2. Linux caps a **single** argv/env string at `MAX_ARG_STRLEN = 32 * PAGE_SIZE`
   = **131,072** bytes (host `getconf PAGESIZE` = 4096). Measured with an execve probe:

   | single-arg bytes | result |
   |---|---|
   | 120,000 / 130,000 | execve ok |
   | 131,072 / 140,000 / 200,000 / 400,000 | `OSError errno 7 Argument list too long` |

3. Reproduced end-to-end from a script file: `bash repro-ebig.sh` →
   `repro-ebig.sh: line 4: /home/vgpnk/.local/bin/jq: Argument list too long`, exit **126**
   — the same message and class as the harness log. (In the interactive tool shell `jq` is
   a shell builtin, so the first attempt printed nothing: the builtin receives the string
   in-process and no execve happens. Only a plain script reproduces it.)

## Consequence chain in the harness

`set -euo pipefail` + `mv -f "$scratch/after.json" "$outdir/after.json"` on line **541**
runs *before* the failing command, so:

* `after.json` lands in the evidence dir — the receipt the claim scores;
* `receipt` is never assigned, the shell aborts at line 547, **`run.json` is never written**;
* `c1-run.sh after` exits non-zero for this carrier (126), contrary to its own contract
  ("Exit: 0 ok", "writes OUTDIR/run.json").

V4 is the only carrier affected because only V4's summary crosses the limit:

| carrier | summary bytes | run.json present |
|---|---|---|
| L3 | 1,479 | yes |
| L4 | 1,465 | yes |
| V3 | 18,441 | yes |
| **V4** | **146,561** | **no** |

`run.json` is also the only artifact that would record, for V4, the harness argv, the
UTC start/end and duration, the `unblob`/`sasquatch-v4be` paths + sha256 + versions, the
child PATH, the superblock summary, the envelope digest and the receipt digest. None of
that is committed for V4; the committed `after.json` carries only
`parameters.{path,output_directory,max_depth,max_output_bytes,max_output_files}`,
`provider`/`engine` name+version+sha256, the subject digest and the
`evidence_id`. This report's independent runs supply the missing toolchain record
(`commands.txt`, `run1.envelope.json.gz`).

## Why this does not falsify R41-C1

The frozen counter never reads `run.json`: `run_provenance_ok` is
`provenance_ok(parameters.output_directory)` (`tools/round-41/c1-counter.py:1645`,
definition at :141 — "names this round's scratch"). Measured: the frozen counter at
`e9a24d07` scores V4 `matched: true` with `run_provenance_ok: true`,
`output_directory: /fast/scratch/hyaku/kaidoku-r41/run-V4/extract`
(`.ufo/waves/round-41/l1/scores/c1-at-e9a24d07.json`), and in my fixture run
(`score-myreceipt.json`) it likewise scores `true` for an output directory under a
different seat's scratch. So the missing `run.json` costs no binding.

The defect is disclosed by L1 in the commit message of `5ca6941b`
("V4 run.json not written: c1-run.sh jq ARG_MAX on a 615-link summary, log kept") and the
raw log is committed, so it is not hidden. What is not disclosed is that the failure is
**size-driven and silent for any future carrier**: any receipt whose gap + unpublished-row
JSON passes ~131 KB loses `run.json`, and the harness has no size guard and no
`--argjson`-from-file path (`--slurpfile`/`--rawfile`, or `jq -s` over a temp file, would
remove the limit). Threshold estimate [INFERENCE]: per-row cost ≈ (146,561 − ~1.4 KB
baseline) / 1,223 rows ≈ 119 B, so ≳ 1,090 gap+unpublished rows, or fewer with long paths,
cross the cap.

## Secondary documentary gap (same run)

`corpus/evidence/round-41/c1/V4/oracle-run.json` records the oracle reader as
`tools/round-40/sqfs-list.py` (sha256 `1079fa9b…`), not the frozen
`tools/round-41/sqfs-list.py` (sha256 `a8e633f5…`) that the claim names. The two differ by
231 diff lines (in-memory image support / `extract_file` / `--extract`, added for the
fetch-chain nested step). Re-running the **frozen** round-41 reader on the same carrier
reproduces `oracle.tsv` and `nonregular.tsv` **byte-identically** (`oracle-repro.json`), so
there is no scoring impact — the claim text overstates what its artifact shows.
