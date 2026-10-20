# RevBaseSumsRunlog — is R17-SUMS-RUNLOG open at `9011581`?

**Verdict: open for the manifest half, mis-stated for the run-log half.** The
`predictions/SHA256SUMS` loss is real at the round-18 baseline. The
"7/8 carriers, no final exit line" artifact exists only at `da64646`; the
run-log retained at `9011581` (and at delivered A `de6c721`) is the *second-pass*
log: 8/8 labels and `run-carriers exit=0`. It is not already-closed (the manifest
line is genuinely absent), and not open in both halves.

Revision aliases are the lesson's own (round-17-verifier-spotcheck.md:9-12):
B `b563c799…`, frozen `2711674…`, S `d0ab299…`, A `de6c721…`. Round-18 baseline
is `9011581d84527ba34c675f9cf912e54d2e72d470` (claims.json:4). All commands below
are read-only Git objects in LANE.

## O1 — Manifest half: open (observation)

```console
$ git show 9011581:.ufo/waves/round-17/predictions/SHA256SUMS        # exit 0, 17 lines
$ git show 9011581:.ufo/waves/round-17/predictions/SHA256SUMS | grep -c 'predictions/carriers.tsv'
0                                                                     # grep exit 1 (no match)
$ git show 9011581:.ufo/waves/round-17/predictions/SHA256SUMS | sha256sum
1b46b3edf114d98d93c39b92397cea5dcbe2c5699703f17a0abc7a3fd97ab42e  -
$ git show 2711674:.ufo/waves/round-17/predictions/SHA256SUMS | grep carriers.tsv   # exit 0
8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv
$ git show 2711674:.ufo/waves/round-17/predictions/SHA256SUMS | sha256sum
d89e6de808fbba17b5dc5e3f88c83c102eadb956e797b1e35a8c0748637b9b26  -
$ git diff 2711674 9011581d84527ba34c675f9cf912e54d2e72d470 -- .ufo/waves/round-17/predictions/SHA256SUMS
1 file changed, 1 insertion(+), 1 deletion(-)                         # exit 0
-8ac38afefb60279eaf74610c03ec3526613c109cfb2b1c8fde8eb3ff5c4d3eb5  predictions/carriers.tsv
+f5ce3d6ba0da04749a65f63295540f82610e13adfe931fb39c67be75b7cb72d5  predictions/replicate-expectations.json
```

- Removal commit is `95e34db`, not the diff endpoints: `git show 95e34db --
  .ufo/waves/round-17/predictions/SHA256SUMS` exit 0 shows exactly the deletion;
  `git merge-base --is-ancestor 95e34db 9011581` exit 0; `git log --oneline --all
  -- …/predictions/SHA256SUMS` returns only `95e34db` and `2711674`.
- Timing (observation): `95e34db` is 11:27:35-03:00; the second pass's first
  receipt is 14:27:41.944Z = 11:27:41-03. The manifest was already blind to
  `carriers.tsv` six seconds before the replicate pass began.
- The file is genuinely unchanged: `git rev-parse <rev>:…/carriers.tsv` is
  `e232bf2bdcc607bcb577d1fb788b785cc6821188` at `2711674`, `da64646`, `95e34db`,
  `d0ab299`, `de6c721` and `9011581`; content sha256 is `8ac38af…` (753 B per
  verification.json). The digest removed from the manifest is still the digest.
- No alternate manifest covers it: `git show 9011581:…/pilot/SHA256SUMS | grep -i
  carriers` exit 1; `custody/custody-r17.v2.txt.sha256` covers only
  `custody-r17.v2.txt`; `replicate-expectations.json` has no carriers reference
  (grep exit 1). So the lesson sentence at round-17-verifier-spotcheck.md:141 is
  accurate.

## O2 — Run-log half: true of `da64646`, false of the measured revision (observation)

```console
$ git show da64646:…/runs/run-log.txt        # exit 0
14 lines; 7 start/end pairs; calib-shfmt absent; no argv header; no exit line.
first: == calib-esbuild-0.25.12 start 2026-10-20T10:47:42-03:00
last:  == pro-op end 2026-10-20T11:00:05-03:00 carrier-run=0 compare=0
$ git show 9011581:…/runs/run-log.txt | cat -n    # exit 0, 18 lines
     1  argv: bash …/run-carriers.sh (all labels), cwd …, started 2026-10-20T11:27:41-03:00
     2  == calib-shfmt start 2026-10-20T11:27:41-03:00
     …
    18  run-carriers exit=0
$ git rev-parse de6c721:…/runs/run-log.txt; git rev-parse 9011581:…/runs/run-log.txt
e33131dcf0dde23791e83a5f0d86aa907f3ed407      # identical: A and baseline share this blob
$ git log --oneline --all -- …/runs/run-log.txt
d0ab299 round-17: w2 integration — … second carrier pass …
da64646 round-17: carrier runs, integrated tools, … (pre-falsify)
```

Binding by receipt windows (observation; parsed from `git show <rev>:…/runs/<label>/receipt.json`):

| pass | first receipt window | last receipt window | labels | exits |
|---|---|---|---|---|
| 1 (`da64646`) | `calib-shfmt` 13:47:05.973Z → 13:47:37.353Z | `pro-op` 13:55:55.592Z → 14:00:05.292Z | 8 run dirs | 8/8 `carrier-run=0 compare=0`, `pins_compare.equal=true` |
| 2 (`de6c721`) | `calib-shfmt` 14:27:41.944Z → 14:28:19.545Z | `pro-esbuild-0.27.7` 14:38:16.815Z → 14:40:02.318Z | 8 | 8/8 `0/0`, `equal=true` |

The retained log's whole span is 11:27:41–11:40:02-03 = 14:27:41–14:40:02Z, i.e.
the pass-2 window to the second. It cannot be the pass-1 record. Consequences:

- The omitted carrier **ran**: `calib-shfmt` pass-1 receipt shows pins window
  13:47:05.973Z → 13:47:37.353Z with `carrier-run.exit=0` and `compare.exit=0`.
  "Lists 7/8 carriers" is a capture gap, not a run gap; the wording invites the
  wrong reading.
- "No final exit line" is not a `run-carriers.sh` behaviour. The script's last
  statement is `exit $overall` (`run-carriers.sh:39`); it never echoes
  `run-carriers exit=`. The only occurrence of that string at `9011581` is inside
  the log itself (`git grep -n 'run-carriers exit'` exit 0 → `runs/run-log.txt:18`),
  and `argv:` likewise only at `runs/run-log.txt:1`. Both wrapper lines were
  written by the invoking capture, not by the committed script. So "restore
  coverage" cannot mean a script fix, and the pass-1 blob cannot be completed
  in place without editing a retained r17 log.
- The pass-1 log survives only as the historical blob `b7939a5` at `da64646`
  (overwritten at `d0ab299`). What is open at the baseline is therefore a
  *retention* defect, not a live 7/8 coverage defect.

## O3 — Coverage counterweight (observation)

`git show 9011581:…/round-17/verify.py` lines 60-67 (pin loop at `:66`) pin every
entry of `predictions/` pre and post. `verification.json` records:
`predictions/carriers.tsv` sha256 `8ac38af…` at both `pins_pre` and `pins_post`,
and `predictions/SHA256SUMS` `1b46b3ed…` at both. So the loss is *manifest
completeness* — a `sha256sum -c predictions/SHA256SUMS` would skip the carrier
list — not missing byte coverage. The lesson's "the frozen manifest no longer
covers it" is literally true; it should not be read as "the file is unpinned".
This makes R17-SUMS-RUNLOG the lightest of the six routed defects, although the
contract's `open_count` weights it equally.

## O4 — Remedy conflict (observation + inference)

round-17-verifier-spotcheck.md:143 says "Restore coverage and append the
correction". claims.json:32 (non_goals) forbids editing round-17 retained
receipts/logs. The manifest line is restorable in the current tree; the pass-1
log is not. The correction must split: (a) restore
`8ac38af…  predictions/carriers.tsv`; (b) state that the pass-1 log at `da64646`
is 7/8 with no exit marker while the log retained at A is pass 2 (8/8, exit 0).
Inference: this is why a prose correction, not a rewrite, is the only honest fix.

## Minimal objective test

`T(REV, pass)` — all three clauses, no prose:

1. **Manifest.** `count(lines in REV:predictions/SHA256SUMS matching
   ^([0-9a-f]{64})  predictions/carriers\.tsv$ with capture ==
   sha256(REV:predictions/carriers.tsv)) == 1`.
2. **Run record for the asserted pass.** start-label set = end-label set =
   labels(carriers.tsv), each exactly once; last non-empty line matches
   `^run-carriers exit=([0-9]+)$`; that N equals 0 iff every bound
   `carrier-run.exit`/`compare.exit` pair is `(0,0)`.
3. **Binding.** Each label's start/end instants fall inside its receipt's
   `[pins_compare.pre_taken_at_utc, pins_compare.post_taken_at_utc]` (±5 s). A log
   that fails this is not that pass's record — this is what rejects the
   baseline's pass-2 log when the asserted pass is pass 1.

Closed(REV) iff 1 ∧ 2 ∧ 3. At `9011581`, clause 1 fails → **open**. Clauses 2-3
pass for pass 2 and fail for pass 1, which is exactly the retention defect and
the reason a pass-blind check reports a false "already-closed".

## Contract comparison (contract.md:38-40)

Ruling: **too weak on substance, too strong/mis-shaped on form.**

- The manifest clause is sound and correctly revision-scoped: it recomputes
  sha256 from the blob at REV, so it cannot be satisfied by a stale hardcoded
  digest (and would fail if `carriers.tsv` ever changed). Add uniqueness
  (exactly one matching line) and optionally verify every manifest line whose
  path exists at REV.
- The run-log half has **no artifact assertion**; it collapses to a `LOG.md`
  substring. `R17-SUMS-RUNLOG … 7/8` is satisfied by a sentence that is false of
  the measured revision (the retained log there is 8/8) and by a sentence that
  merely restates the defect. It also hardcodes the defect's numeral: a better
  correction that spells "seven of eight", or that reports the restored 8/8
  postcondition, fails. Minimum repair: require the LOG line to name `da64646`
  and distinguish 7/8 (pass 1) from 8/8 (retained), or replace the token with
  clauses 2-3 above (cheap from Git objects). Fixing the site to `LOG.md` is a
  form constraint, not a truth condition; the lesson's own remedy is
  site-neutral.
- It does not over-constrain the manifest fix; it under-tests the run-log fix and
  rewards the defect's wording over the corrected state.

## Limits

- Read-only Git only; no `jj`, no lane tool, no REA/Ghidra, no carrier executed.
  Aliases B/S/A come from the lesson header; the pass binding is from receipt
  timestamps, not from re-running anything.
- Inference (labeled): the wrapper wrote the `argv:` and exit lines — argued from
  their absence in `run-carriers.sh` and their presence only in the log; the
  wrapper's own bytes are not retained.
- No tools installed or upgraded.
