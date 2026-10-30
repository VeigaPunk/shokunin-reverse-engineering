# CritCounterV2 — report (round-52 wave-1, attack of the R52-C1 v2 counter design)

Seat: `CritCounterV2`, role critic, leaf member (no subagent dispatch).
Round base `c525de54`, claims draft `ab0eafed` (plans/round-52-claims.md read in full, treated
as the round's rule).

## Verdict

The R52-C1 v2 counter design is **attackable on three load-bearing points before the freeze**
(stale rule bytes, receipt mutation after the freeze, and a retry loop that erases its own
evidence), and the `law_shape_ok` clause as worded does not yet encode the law. The law itself
is real: measured over the committed round-50 envelopes, the round-52 law rule scores 4 of 4
while the round-50 rule reproduces the miss at exactly 2 of 4, and the law fails closed on a
future device gap where the round-50 rule admits one. Numbered findings F1–F12 with severities
and the minimal correction set are in
`.ufo/waves/round-52/w1/CritCounterV2/findings.md`.

## What I ran (receipts, exact commands, exit codes)

No REA run, no git mutation. All commands were read-only over the lane tree; outputs copied
into this seat directory; scratch removed after copying.

1. `python3 -I -B .ufo/waves/round-52/w1/CritCounterV2/probe-r52-law.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin`
   — exit 0, 2026-10-30T11:15:21Z, stdout sha256 `7a7916d8dbe3c572eef13deceb971df091fa29bcf8e0150ef943196801b6a91d`
   (saved as `probe-r52-law.out.txt`). Loads the frozen v1 counter module (sha256
   `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`) and its frozen gap rule
   (`43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef`) and scores candidate rules
   over the committed round-50 envelopes + oracle tables. Probe sha256
   `18c3ca46af86600d079fb0c0a3255cd29a578f02ffb451bce967399b516badc3`.
2. `unsquashfs -lln` on a mksquashfs fixture with pseudo-file device rows (char 247:0, char 4:64,
   block 7:1, fifo) — the `c1-run.sh` census regex matched all four rows; recorded in F10.
3. Read-only checks on the v1 source (`grep`/`sed`) cited per finding: `receipt_fresh`
   (`--diff-filter=A` only, line 2317), `FROZEN_PATHS` (line 416), drift selftest `want 2`
   (lines 4225–4257), retry loop `return 'ok', data` (line 2088), `main()` exit-2 receipt shape
   (lines 2570–2582), `prior_pins()` (line 1596), `_frozen_paths` (line 1649).

## Key findings (full detail in findings.md)

- **F1 (high)** the v2 controls take `--gap-rule`; v1's receipt has no rule sha256, so a stale or
  overridden rule can pass unnoticed. Receipt must name the rule path + sha256 and equate them
  to the frozen bytes; the predicate must refuse `--gap-rule`.
- **F2 (high)** `receipt_fresh` proves only the receipt was *added* after the freeze; a post-freeze
  `M`/`D` on a committed receipt is not drift and `evidence_id_ok` recomputes, so it passes too.
- **F3 (high)** the retry loop returns `('ok', data)` — attempts and earlier diagnostics vanish on
  success; the claim's required record is not produced on the success path, and the ENOENT
  branch does not exist in v1.
- **F4 (high)** `law_shape_ok` as worded admits a rule whose `removed.kinds` or `structural` names a
  device kind (probe cases K1/K2: claimed shape True, extended shape False). The all-thirteen
  whitelist is green on disposition (4/4) and red only through this clause, so the clause is the
  entire M1 discriminator and must be exact.
- **F5 (medium-high)** ported bindings/constants are round-50-valued: `OPENED_DATES`, `FRONTIER_MARK`,
  the hard-coded `claim == 'R50-C1'` checks in `carriers_spec` and `gap_rule_model`, and the absence
  of bindings that `hsqs` left the Frontier list, that the entry cites S252, that the SCORECARD
  coverage head moved 141→142, and the LOG entry.
- **F6 (medium)** drift exit-2 receipts carry no `carriers_matched`/`met_target`; a tabulator that
  defaults missing to 0 misreads a drifted freeze as 0 matched. `is_ancestor(FREEZE, REV)` is never
  checked.
- **F7/F8 (medium)** the walk is right in v1 (producer identity unrecorded, though); the
  `re_scored_pins` waiver is self-inflicted — the four round-50 pins are not prior today, and joining
  `tools/round-50/carriers.json` to PRIOR_CARRIER_TABLES is what manufactures the waiver surface.
- **F9 (medium)** `depth_gap_recorded` cannot fail as worded: all four committed receipts carry the
  identical `input_path "$output/firmware.bin_extract"` and the same continuation id.

## Verification status

- CTL-OLD 2 of 4 / CTL-NEW 4 of 4 / M1 disposition 4 of 4 / M2 law green + whitelist red /
  M3 2 of 4: **measured**, probe output committed in this seat dir.
- Fail-closed on a future device gap under the law rule: **measured** (4/4 red).
- `unsquashfs -lln` census-regex parse of char/block/fifo rows: **measured** on a fixture.
- Not run (out of seat scope): any REA invocation, any counter `--selftest`, any data run.
- Tooling installed or upgraded: none (pacman transactions are host-paused; nothing needed).

## Files

- `.ufo/waves/round-52/w1/CritCounterV2/findings.md` — numbered findings F1–F12 + correction set.
- `.ufo/waves/round-52/w1/CritCounterV2/probe-r52-law.py` — the read-only probe (sha256 above).
- `.ufo/waves/round-52/w1/CritCounterV2/probe-r52-law.out.txt` — captured output (sha256 above).
- `.ufo/waves/round-52/w1/CritCounterV2/status.json` — wave accounting record.
