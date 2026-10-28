# C2Selftest — Round 48

## Scope and axes

Read-only check of the frozen C2 counter's built-in parser selftest and its required adversarial case table. Axes: coverage (per-clause green/red cases), calibration (five frozen forgeries), evidence integrity (exact command/status/output digest/time). No source or frozen bytes changed.

## Case table required for the counter

`record2.py --selftest` explicitly says it checks parsers only; therefore these are cases for the **counter clause battery**, not claimed results from the parser selftest. Genuine card means the complete revision-backed intended record.

| Clause | Green card required | Red card required |
|---|---|---|
| Oracle from `--rev` | committed round-47 oracle executes from revision bytes; `mismatches=[]`, `met_target=true` | oracle fails/rejects or any independently re-derived atom mismatches |
| Completeness floor | each of last two round sections has seat atom (or re-derived seats correction), path, rev, unique claim ID; Owned axes has >=2 atoms | remove any required atom/claim ID, duplicate claim ID, or remove an Owned-axes atom |
| Corrections | every seats/window/path/rev correction agrees with oracle `corrects()`, axes correction agrees with card, quote correction re-derives against cited receipt | alter a correction value/target, malformed axes correction, or quote unrelated to cited receipt |
| Quoted numbers | every quoted atoms/exempted/corrections/mismatches number matches a cited receipt cell or valid quote correction | increment a quoted number without correcting it from the cited receipt |
| Owned-axes score cell | coverage/depth score equals rounded 10*n/d from the evidence fraction | decrement/change either score cell while leaving fraction intact |
| Battery | all five forgeries are v2 green, v3 red; genuine v3 green; crash=0 | each mutation must be rejected under v3; any forgery green fails claim |

Frozen five-forgery cards: `gold-tautology` (replace both sections with seat/window-only tautologies); `seats-moved` (put seat total in older section only); `quote-off-by-one` (increment first quoted receipt number); `axes-score-cell-off` (decrement score cell); `axes-correction-forged` (`999/999`).

## Executed evidence

Exact command (from lane root; scratch environment set):

```sh
S=/fast/scratch/hyaku/kaidoku-r48/C2Selftest
mkdir -p "$S"
export TMPDIR="$S" HYAKU_SCRATCH="$S"
/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status
python /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/record2.py --selftest
```

- Exit code: 0 (selftest; disk guard also returned normally).
- UTC time: 2026-10-28 (tool environment supplied date; exact time-of-day unavailable in captured tool result).
- Selftest stdout:

```json
{
 "note": "record2's clauses are exercised against the lane's own history by the round-48 controls and wave seats; this selftest checks the parsers only",
 "corr_parse": true,
 "quote_parse": [["atoms", "42"], ["exempted", "1"]],
 "receipt_parse": [".ufo/waves/round-47/l1/scores/c2-at-A7.json"]
}
```

- stdout sha256: not captured during execution; no digest is asserted.
- Existing controls read from lane listing: `ctl-c2-0-do-nothing.json`, `ctl-c2-1-v2-profile.json`, `ctl-c2-a1-before.json`, and probe files exist. Their contents were not read or rerun in this seat.
- Checks not run: full counter evaluation, clause fixture attacks, controls verification; these are not part of parser-only `--selftest` and must not be represented as passed.
- No tools installed or updated.

## Findings / risks

The parser selftest is explicitly parser-only and does not exercise any frozen predicate or mutation battery. It demonstrates that the corrections regex recognizes an axes correction, quote parsing extracts two keys, and the receipt path regex extracts the sample path. This is not evidence for C2 clauses or any of the five forgery outcomes. Preserve the case table above as the acceptance target when interpreting actual counter receipts. No independent falsification result was produced in this seat.

## Blockers

The tool result omitted exact UTC time-of-day and stdout digest; those evidence fields cannot honestly be reconstructed after the fact. No install or source changes were made.
