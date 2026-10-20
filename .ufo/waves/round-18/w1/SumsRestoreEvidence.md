# SumsRestoreEvidence — R17-SUMS-RUNLOG evidence

Seat: `KaidokuR18.SumsRestoreEvidence` (executor, round-18 wave 1). Target:
`corpus/lessons/round-17-verifier-spotcheck.md:140-143`. Deliverable written:
`.ufo/waves/round-18/evidence/sums-runlog.json` (parses clean). No other lane
file touched; the r17 `SHA256SUMS` restore is the L1's move.

## Findings (observations unless marked inference)

1. **Dropped line.** `git diff 2711674..B -- .ufo/waves/round-17/predictions/SHA256SUMS`
   is exactly +1/−1 in hunk `@@ -2,7 +2,6 @@`:
   - removed (old-file line 5): `8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv`
   - added: `f5ce3d6ba0da04749a65f63295540f82610e13adfe931fb39c67be75b7cb72d5  predictions/replicate-expectations.json`
   - The only commit in `2711674..B` touching the file is `95e34db`
     (2026-10-20T11:27:35-03:00, "w2-hardened tools and frozen replicate
     expectations (pre-rerun)"). Inference: when `replicate-expectations.json`
     was frozen into the manifest, the `carriers.tsv` entry was dropped in the
     same edit. `SHA256SUMS` blob `b808abf5…` is identical at 2711674 and
     da64646; B has `99d122c5…`.
   - Restore line for the L1:
     `8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv`

2. **carriers.tsv never changed.** `sha256` of `predictions/carriers.tsv` is
   `8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5`
   (matches the `8ac38afe…` prefix in the assignment) at all three revisions
   — 2711674, da64646, B. Only manifest coverage was lost, not bytes.

3. **All other lines at B verify.** Every one of the 17 lines in B's
   `SHA256SUMS` recomputes byte-for-byte against `git show B:.ufo/waves/round-17/<path>`
   (17 OK, 0 mismatches, including the new `replicate-expectations.json` line).
   The lone coverage gap is the absent `carriers.tsv` line.

4. **da64646 run-log is a partial capture.**
   `da64646:.ufo/waves/round-17/runs/run-log.txt` has 14 lines, all of the
   `== <label> start|end` shape that `run-carriers.sh:24,36` emits. It logs
   7 of 8 carriers; **`calib-shfmt` is the missing carrier**. It also lacks
   the `argv: … run-carriers.sh (all labels) …` header and the
   `run-carriers exit=0` footer — both present in the 18-line B copy
   (committed `d0ab299`, pass 2). Inference: capture of pass-1 output began
   after calib-shfmt's echoes and the file was committed with a partial stream
   (da64646, 11:06:06-03:00, ~6 min after the last logged line 11:00:05).
   Extra signal: the logged order `pro-esbuild-0.27.7` (10:53:40) before
   `pro-op` (10:55:55) differs from `carriers.tsv` order (pro-op line 7,
   pro-esbuild-0.27.7 line 8) and from the pass-2 order — consistent with
   pass-1 having been driven per-label rather than as one sequential read
   (`run-carriers.sh:17` iterates the TSV).

5. **calib-shfmt's pass-1 receipt exists at da64646.**
   `runs/calib-shfmt/` is a full tree at da64646; `receipt.json` blob sha256
   `03ba37a086899d1083e4c7a949e751a5840993e365c411f64df0f0d2e3096c69` records:
   - `steps.inspect-go-binary` exit 0, 2026-10-20T13:47:05.973747+00:00 →
     13:47:06.688417Z
   - `steps.analyze` exit 0, 13:47:06.688621Z → 13:47:37.309101Z,
     `evidence_id ev_2b29a1ddfaead9d13a3d8923a2edc176dbe8ebda0ac776707625c6c1de3c5be3`
   - `carrier.sha256_pre == sha256_post ==
     58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459` (/usr/bin/shfmt)
   - `carrier-run.exit` = `0`, `compare.exit` = `0`, `compare.json` `all_match: true`
   - bound session `/tmp/kr17-rea-y138m4zi/rea-ghidra-j5AXOZ`
   Its window (10:47:05–10:47:37 local) ends 5 s before the log's first line
   (calib-esbuild-0.25.12 start 10:47:42), consistent with calib-shfmt being the
   first pass-1 carrier whose echoes preceded capture. The B receipt
   (`404a6f59…`, steps 14:27:41–14:28:19Z) is the pass-2 rerun, so da64646's
   copy is uniquely pass-1 evidence.

## Commands run (all read-only git; no installs, no writes outside assigned files)

| Command | Exit |
|---|---|
| `ls -la .ufo/waves/round-18{,/tools,/evidence,/w1}` + r17 dirs | 0 (tools/evidence absent at start) |
| `cat .ufo/waves/round-18/wave1-assignments.json` | 0 |
| `grep -n "SumsRestore\|sums-runlog\|…" wave1-dispatch.json wave1-spec.json gen-wave1.py` | 0 |
| `grep -c "selftest once" wave1-dispatch.json`; `grep -o "your tool's --selftest…"` | 0 |
| `grep -n "selftest" .ufo/waves/round-17/tools/*.py` | 0 |
| `grep -rn "selftest" .ufo/waves/round-17/w1/*.md w2/*.md`; `ls` w1 w2 | 0 |
| `git diff 2711674 9011581d84527ba34c675f9cf912e54d2e72d470 -- .ufo/waves/round-17/predictions/SHA256SUMS` | 0 |
| `git show {2711674,B,da64646}:.ufo/waves/round-17/predictions/SHA256SUMS` | 0 |
| `git show REV:.ufo/waves/round-17/predictions/carriers.tsv \| sha256sum` (×3 revs) | 0 |
| `git log --format='%h %ci %s' -3 2711674` / `-3 da64646` | 0 |
| `git show da64646:.ufo/waves/round-17/runs/run-log.txt` | 0 |
| `git ls-tree -r --name-only da64646 .ufo/waves/round-17/runs/` | 0 |
| per-line verify of B's SHA256SUMS vs `git show B:<path> \| sha256sum` | 0 (17 OK) |
| `git show da64646:…/calib-shfmt/receipt.json` | 0 |
| `git show da64646:…/calib-shfmt/{carrier-run.exit,compare.json,compare.exit}` | 0 |
| `git show B:.ufo/waves/round-17/runs/run-log.txt` | 0 |
| `grep -n "run-log\|run_log\|LOG" run-carriers.sh` (no matches; then `cat`) | 0 |
| `cat .ufo/waves/round-17/run-carriers.sh` | 0 |
| blob sha256 of da64646 `calib-shfmt/{receipt,compare,observation}.json`, `carrier-run.stdout`; receipt field extraction via `python3 -c json` | 0 |
| `git show 2711674:.ufo/waves/round-17/predictions/carriers.tsv` | 0 |
| `git log --follow -5 -- runs/run-log.txt`; `wc -l` on both copies | 0 |
| `git log 2711674..B -- .ufo/waves/round-17/predictions/SHA256SUMS`; `git rev-parse` of the three SHA256SUMS blobs | 0 |
| `git show B:…/calib-shfmt/receipt.json \| sha256sum` + field extraction | 0 |
| `grep -n 'echo "==\|exit $overall\|while IFS' run-carriers.sh` | 0 |
| `python3 -c json.load` on the written evidence file | 0 |

## Selftest

No tool is assigned to this seat (contract.md:11 scopes `--selftest` to new
tools; this item produces evidence only). `--selftest`: **N/A**, consistent
with the r17 precedent (`.ufo/waves/round-17/w1/DraftLogEntry.md:59`).

## Risks / notes for the L1

- The restore is one line; `predictions/carriers.tsv` re-inserts at old line 5
  (sorted position after `calib-shfmt.prediction.json`).
- Pass-1 run-log cannot be made complete retroactively — da64646's copy is
  frozen; the named correction should state "7/8 carriers logged, calib-shfmt
  receipt retained" (the routed-defects check wants `R17-SUMS-RUNLOG` + `7/8`
  in LOG.md).
- Pass-1 carrier order ≠ `carriers.tsv` order (depth observation, flagged
  above); if the L1 reconstructs pass-1 invocation semantics, run-log order is
  not TSV order.
