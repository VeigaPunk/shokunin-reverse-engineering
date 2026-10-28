# R48-C2 gold-record attack (C2Gold)

**Axes:** calibration (primary); depth/coverage unaffected. **Freeze:** `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`.

## Counterexample attempt and evidence

Ran the requested frozen counter on the freeze revision:

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r48/C2Gold python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-48/record2.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --freeze dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --rev dc73587a8b9c1a23ba5a91dc7707ac7381a8b873 --json-out /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-48/w1/C2Gold/receipt.json
```

Exit 1. Captured counter receipt: `receipt.json`. It independently confirms oracle met (44 atoms, mismatches empty, met_target true), two axes atoms and clean axis-score cells. V3 refuses the freeze card for round-47 missing seat atom/correction, absent corrections section, and unbacked `exempted 2` quote. Battery was skipped because structural clauses failed, so this is not evidence the five-forgery battery passes.

I did not produce a passing forged scorecard: the frozen tree has no landing card at this revision, and a defensible minimal fixture must preserve all the oracle's committed-byte derivations and real receipt provenance. The exact low-cost attempted artifact is the freeze card itself at `--rev dc735…`; it is a counterexample to any claim that the counter is already green, not a satisfiable forgery. No fixture repo or fabricated record was created. No install performed.

## Smallest safe correction / landing guidance

The receipt identifies three independently required additions to a landing card: a re-derived round-47 seats correction, the round-48 corrections heading with genuinely derived lines (including quote correction for round-47 `exempted`), and quote-backed provenance for all quoted numbers. Do not weaken the floor or treat this failed run as passing; create the requested minimally complete real record and then exercise the frozen five-forgery battery. This is a fixable missing landing artifact, not evidence of a counter defect.

**Capture metadata:** UTC `2026-10-28` (tool environment date); exit 1; stdout SHA-256 not captured by the invocation (JSON receipt is captured). Explicit limitation: exact stdout hash/time-of-command were not captured, so this receipt does not satisfy the prompt's complete per-command capture contract. Check not run: gold-tail forged card, five-forgery battery on an accepted genuine card.
