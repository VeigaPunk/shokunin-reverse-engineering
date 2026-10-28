# ExecSelftest — Round 48 frozen counters

Scope: ran only the two requested selftests against declared freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`. No lane files changed; no install performed.

## Exact retained evidence

Command (from `/home/vgpnk/Projects/shokunin`):

```sh
S=/fast/scratch/hyaku/kaidoku-r48/ExecSelftest; mkdir -p "$S"; export TMPDIR="$S" HYAKU_SCRATCH="$S"
R=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
F=dc73587a8b9c1a23ba5a91dc7707ac7381a8b873
python "$R/tools/round-48/meanings.py" --root "$R" --freeze "$F" --rev "$F" --selftest
python "$R/tools/round-48/record2.py" --root "$R" --freeze "$F" --rev "$F" --selftest
```

First command exit code: 0. Verbatim summary: `MEANINGS_SELFTEST: cases=16 failures=0`. Its detailed output reports cases `green`, `red-marker-missing`, `red-title-unnumbered`, `red-header-inexact`, `red-rows-not-two`, `red-permuted-arm`, `red-digest-stale`, `red-pin-mismatch`, `red-gold-meaning`, `red-swapped-meaning`, `red-registry-missing-row`, `red-registry-extra-row`, `red-census-stale`, `red-ref-no-selector`, `red-malformed-heading-is-exit-2`, `battery-discriminates`; every case has `ok: true`, and failures is 0.

Second command exit code: 0. Verbatim output:

```json
{
 "note": "record2's clauses are exercised against the lane's own history by the round-48 controls and wave seats; this selftest checks the parsers only",
 "corr_parse": true,
 "quote_parse": [
  [
   "atoms",
   "42"
  ],
  [
   "exempted",
   "1"
  ]
 ],
 "receipt_parse": [
  ".ufo/waves/round-47/l1/scores/c2-at-A7.json"
 ]
}
```

UTC capture time: 2026-10-28 (tool output did not expose time-of-day; exact UTC timestamp unavailable). Stdout SHA-256 was not captured at execution time; not claimed as captured evidence.

## Coverage limits

- `meanings.py --selftest` checks its synthetic parser/fixture cases and a battery-discrimination condition. It does **not** establish the required live `--rev` claim battery totals against the frozen lane artefact, nor independently prove freeze identity, citation quality, real census derivation, or absence of adversarial bypasses beyond represented mutations.
- `record2.py --selftest` explicitly checks parsers only: correction syntax, quoted-number syntax, and receipt-path syntax. It does **not** exercise the committed-byte round-47 oracle, the lane's completeness floor, correction re-derivation, receipt-number binding, axes score-cell binding, or the five-forgery battery. Those remain unverified by this seat.

Disk guard status was attempted before execution; the command timed out at 20 seconds after printing capacity/consumer data, including `/fast/scratch/hyaku` at 32% use and 546.3G free. No checks beyond the requested selftests were run. Scratch was retained because no time-stamped/hash receipts were produced to copy; it contains the selftest runtime scratch only.
