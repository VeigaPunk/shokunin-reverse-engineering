# C2Floor — R48-C2 completeness floor

## Frozen measurement

Command run from the lane root (write target is this seat's report directory):

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C2Floor python3 -I -B tools/round-48/record2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out .ufo/waves/round-48/w1/C2Floor/receipt.json
```

Exit **1** (not met), stdout SHA-256 `f0bf3d66c54b8d954b6f6e0bec2916d31b1afccde806da2ce20ae2260c1ab6be`, captured UTC `2026-10-28T18:47:20.912386+00:00`. Full JSON receipt: `C2Floor/receipt.json`.

At the declared freeze revision, the round-47 oracle is green (`mismatches []`, `met_target true`, 44 atoms); Owned-axes yields 2 axes atoms and both score cells correctly derive (coverage 138/138 => 10.0; depth 24/24 => 10.0). The floor nevertheless fails on round 47: its extracted classes contain window/path/rev but **zero seat atom** (`round-47: no seat atom and no re-derived seats correction`). Round 46 passes the seat/path/rev and claim-id floor. Further red conditions: no re-derived line under `## Record corrections — round 48`; `exempted 2` is unsupported by the two cited round-47 receipts. Thus battery was skipped as structural clauses failed, not passed.

## Source-derived completeness result

Inspected the counter's floor logic at `tools/round-48/record2.py:207-244`: `seats_ok` means either one oracle-derived seat atom in that round's section or a keyed `seats` correction; path and rev atoms are independently required; claim IDs must be present and are rejected if shared across the two sections. Oracle section scan at freeze finds sections `round-46`, `round-47`. Round 46 has seats=1, path=4, rev=18, claims `R46-C1`,`R46-C2`; round 47 has no seats class, path=4, rev=13, claims `R47-C1`,`R47-C2`. The explicit failing reason names round 47. The frozen card's corrections section is `## Record corrections — round 47`, not the required round-48 heading, and its quoted `exempted 2` is not equal to the cited receipt values as reported in `quotes_bad`.

## Tautology attack status

The frozen counter implementation itself defines `gold-tautology` to replace both round sections with tautologies retaining only seat and window atoms (`record2.py:345-363`), and calls it among five battery mutations (`:422-426`). Clause 2 checks path and rev atoms too, so the intended v3 rejection mechanism is present. However this freeze's own genuine card fails structural checks first, and its battery receipt explicitly says `skipped: the card fails a structural clause first`. Therefore **the requested observation that this tautology is red under v3 and green under v2 is not established by this measurement**. Profile v2 was not run; reporting the requested green/red results as observed would be fabrication. Exact standalone tamper measurement not run.

## Evidence and limits

- The report directory and `receipt.json` are the only files written by this seat. Lane tracked/other wave changes were present before this work; no attempt was made to alter them.
- C2 floor result and genuine-card clause failures are directly recorded in receipt. `SCORECARD.md` round-section atom counts above are the source context for why the missing seat atom is surprising: regex-like seat wording exists in the Round 46 paragraph, but oracle collection does not derive a round-47 seat atom. This is a source/parser derivation, not a claim that the text lacks all seat-like prose.
- The requested v3/v2 tautology pair remains a risk/open evidence item; no synthetic fixture was created or modified.
- No build, lint, formatter, or tests run. No tool installed.
