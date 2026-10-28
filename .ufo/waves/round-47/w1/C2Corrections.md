# C2Corrections — R47-C2 draft + verification (seat report)

Full report, receipts and reproduction scripts:
`.ufo/waves/round-47/w1/C2Corrections/` (`report.md`, `draft-section.md`, `probes.json`,
`probe-receipts/`, `receipt.json`, `receipt-at-pin.json`, `receipts.jsonl`, `driver.py`,
`driver2.py`, `probes.py`).

Counter: `tools/round-47/record.py` sha256 `abf35257…779e7`. Base `13a9e9e1`, pin `f7d6e58d`.

## Delivered

1. The draft section (verbatim): `.ufo/waves/round-47/w1/C2Corrections/draft-section.md`.
   Two parsed correction lines plus two `axes` facts stated with their counting command.
2. Proof each line re-derives (scratch copy of `SCORECARD.md`, one-commit fixture repos):
   - base card + draft + both axis heads repaired → exit 0, `corrections 2`,
     `corrections_bad []`, `exempted 1`, battery `3/0` (fixture `6611552`, `draft-fixtures.json`);
   - base card + draft only → exit 1, `mismatches 2` (the two heads), `exempted 2` — each line
     binds exactly the atom it names (fixture `f5c0cdf`);
   - pin card as committed → exit 0 at `f7d6e58d` (`receipt-at-pin.json`).
3. Values, each with its command (`receipts.jsonl`): round-45 dispatch `40` + `36` = **2 waves,
   76 seats**; `git log --name-status --format= 332f4884..58eb04b6 -- tools/round-46
   plans/round-46-claims.md` = **0 lines** (also `58eb04b6..13a9e9e1` = 0); knowledge files at rev
   = **138**, coverage pair `(138,138)`; craft rules = **24**, all citations resolving, depth pair
   `(24,24)` at the pin and `(23,23)` at the base.

## Findings (exact command, differing value, fixture)

| id | severity | finding | evidence |
|---|---|---|---|
| D1 | HIGH | C2 is not separable from C1: the `depth` head is derived from `SKILL.md`, so an unresolvable citation in block 24 fails C2 clause 1. The claims file's "it never reads the craft section" is false. | probe `P1`: rename block 24's `interpreter_sha256` citation → exit 1, `axes depth claimed [24,24] derived [23,24]` |
| D2 | HIGH | `axes` corrections are unparseable (`CORR` = `seats\|window\|path\|rev`), so clause 3's axes grammar is dead code and a false axes line passes. The two landed `- corrects axes …` lines are inert (`corrections 2`, never 4). | probe `P7`: `- corrects axes coverage: 999/999` inside the section → exit 0 |
| D3 | HIGH | A window exemption is not bound to the atom: any empty window over any path exempts every placeholder atom (A1 removed the pair check and nothing replaced it). | probe `P8` (corpus/knowledge path exempts the round-46 frozen-path claim) → exit 0; `P6` one line exempts two placeholders (`exempted 3`) |
| D4 | MED | "at least two re-derived corrections" needs no correction: in-place repair + two true lines → `exempted 0`, exit 0; a correction for round 44 (no such heading in the card) is accepted. | probes `P4`, `P12` → exit 0 |
| D5 | MED | The claims file's "a change makes both counters exit 2 `frozen_path_changed`" cannot hold for `record.py` (no `--freeze`, no freeze arm); six byte states this round; `git log -1 -- plans/round-47-claims.md` = `62e33f7d` ≠ declared freeze `f54b3b6d`; the **frozen** `record.py` scores the landed corrections red ("window pair names no atom in scope"). | `receipt-at-e856beb5.json`, `ctl-c2-2-freeze-amendment.json` |
| D6 | MED | The round-46 window claim was false, not merely unverifiable: `0425224..58eb04b6` touches `tools/round-46/attest.py` and `gate.py`. | probe `P9` → exit 1, `{empty: false}` |
| D7 | MED | The round-47 C2 row quotes `atoms 50` / `exempted 2` at `a0753786`, where the counter reports `atoms 42` / `exempted 1` (window now `[round-46, round-47]`). | `probe-receipts/at-a0753786.json` |
| D8 | LOW | The pre-A2 window forgery was a no-op (window empty by construction) — reproduced; A2's `root..tip` fixture is now red by construction, so `P9` is the honest version of that attack. | `receipt-at-e856beb5.json` |

Strengths confirmed: repair-by-deletion refused (`P5`), plausible non-empty window refused (`P9`),
false seat total refused (`P10`, `derived [2,80]`), ghost path refused twice (`P11`), and the base
measurement reproduces all four `Before` values.

## Landing checklist

Block 24 first (citations resolving) → append the draft verbatim → repair the two `## Owned axes`
heads in place (no exemption path exists) → re-run the counting command at the landing rev and quote
that rev's numbers. Not run: C1's `exact.py`, `--profile v2`, network. No installs; lane left
untouched (`git status --porcelain -- SKILL.md SCORECARD.md plans tools corpus LOG.md QUALITY.md`
empty).
