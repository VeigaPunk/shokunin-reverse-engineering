# C2Quote — Round 48 quote-correction attack

## Scope and captured baseline

Read the frozen claim instrument `plans/round-48-claims.md` in full. Tested frozen `tools/round-48/record2.py`, without modifying it, at freeze/revision `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`. Baseline exact command:

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C2Quote python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/record2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out .ufo/waves/round-48/w1/C2Quote/receipt.json
```

Exit 1 on the unlanded freeze: round 47 has no seat atom or re-derived seats correction; no round-48 correction section exists; quote binding flags `exempted 2`. The round-47 oracle reports `mismatches []`, `met_target true`, `atoms 44`; its `exempted` collection length is **1**, while the round-47 SCORECARD text quotes `exempted 2`. `receipt.json` and identical stdout copy `counter-receipt.json` preserve the full output. Receipt digests and UTC timestamp are in `sha256.txt` and `capture-time.txt`.

## Clause 4 attacks

Scratch-only fixture driver imported the frozen counter and evaluated synthetic card text with committed `--rev` file lookups. Output JSON is retained for each case:

- `misquote-repaired.json`: add `- corrects quote round-47: exempted 1 (receipt .ufo/waves/round-47/l1/scores/c2-at-A7.json)`. The quote correction re-derives (`corrections_bad []`), records quote `exempted 2` corrected to 1, and clears `quotes_bad`. Overall exit stays 1 only for the separate missing seat atom. This reproduces the target misquote and confirms a correct quote correction can account for it.
- `already-right-parsed.json`: add `- corrects quote round-47: exempted 1` to a quote already equal to 1. It is rejected in `corrections_bad`, reason `the section already quotes that value`.
- `outside-window.json`: add `- corrects quote round-45: exempted 1`. It is rejected, reason `no round-45 section in scope`; the unsupported round-47 quote remains flagged.

The initial `already-right.json` was a malformed fixture that failed to place a correction in the parsed section; do not use it as evidence. The parsed replacement is `already-right-parsed.json`.

## Evidence limits

The custom fixture calls used `python3 -I -B - "$L" "$R"`, importing `record2` from the lane and calling `score(text, files, L, rev, 'v3', None)`; only scratch card text changed. Their exact JSON stdout is retained. The report itself does not claim the full C2 predicate passes; baseline exits 1. I did not run the v2/v3 five-forgery battery or the tautology comparison. No build, tests, lint, formatter, or install. Disk guard status was checked before the pass. No fixture repo or git mutation was needed.
