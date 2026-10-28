# R47-C2 — exemption-mechanism attack: scoped findings

Seat `C2Vacuity`. All mutations ran on throwaway clones of `SCORECARD.md` at base `13a9e9e1…`;
the lane tree, the frozen bytes and the fleet repo are untouched. Receipts, 16 cards, builder,
`exits.txt`, `manifest.json` and the full table: `.ufo/waves/round-47/w1/C2Vacuity/` (`report.md`).

**Instrument measured.** Lane's `tools/round-47/record.py` at git blob
`636506bcb31d894343f9883621efdc4ffa22a38b` (`sha256 abf35257…`), `2026-10-28T18:01Z`. The lane
landed amendments *during* this seat (`9018c53b`, `62e33f7d`, `2e4ae434`, `1e2c3102`, `07d2894e`,
`f54b3b6d` touch the frozen paths); the first pass ran at the pre-A5 bytes and every verdict
reproduced after re-measurement. `exits.txt` records the blob per run.

**Bottom line.** Against the do-nothing record the mechanism is sound (base exit 1 reproduces the
claim's `Before` exactly: 4 mismatches, same atoms and values, receipt `53d81a3d27a4c0c8`).
Four constructions still reach `met_target: true` with a false or unverifiable record, and C2 has
no freeze arm at all.

## HIGH

**F1 — a false per-wave split scores green.** `cards/A6-false-split-exempt.md` states
`Wave 1: 36 seats; wave 2: 40 seats` while dispatch says `40, 36`; the true-total correction
`- corrects seats round-45: 2 waves, 76 seats total` exempts it (`exempt()` keys on class+key;
`corrects()` binds only `(len, sum)` — `record.py:267-268`, `:330-338`). `exit 0, met_target true,
exempted [seats:45], mismatches []`, receipt `attack-A6-false-split-exempt.json` `437e13e38fd8ca0a`.

**F2 — the unverifiable `<tip>` window claim survives, exempted by an unrelated window.**
`cards/A13-window-unrelated-pair.md` keeps round 46's `0425224..<tip> -- tools/round-46 …` sentence
and exempts it with `- corrects window round-46: empty in 13a9e9e1..13a9e9e1 -- corpus/knowledge/`.
`exempt()` returns `True` for any atom whose `pair` is `None` (`:335`); nothing binds the
correction's window to the atom. `exit 0, corrections_bad []`, receipt
`attack-A13-window-unrelated-pair.json` `aacc28fc2f9646da`. Isolated lever: A5 is exempted with
`corrections_bad []` too (`74ccf448c4069976`). Claim clause 4 authorises this; clause 1's gloss
("none is `unverifiable`") is then false.

**F3 — C2 has no freeze arm; its interpreter is unpinned and moved 6× after the freeze.**
`grep -c 'freeze_state\|frozen_path_changed' tools/round-47/record.py` = 0; `--freeze` is rejected
by argparse (exit 2, not `frozen_path_changed`). `plans/round-47-claims.md:10-11` still claims a
change makes "both counters exit 2 `frozen_path_changed`" — false for C2. A3 (`2e4ae434`) changed
scoring semantics (the historical exemption) and A4–A6 changed fixtures/citations with no
claims-file paragraph for A3/A4. Proof the arm matters: a copy with `EXEMPT_MAX = 3` → `99`
(one line, 36) turns A11 from `exit 1 failing ['exempted 4 > 3']` (`attack-mut-orig.json`,
`a7cf8386db0cd303`) into `exit 0 met_target true` (`attack-mut-weak.json`, `e39d809ecdf3652e`).
*For C1 (not run here; `gate.py:156-196`):* `freeze_state` unions both ends, so at any rev ≥
`62e33f7d` the amendments make `frozen_path_changed` non-empty for `tools/round-47/` +
`plans/round-47-claims.md`; C1 needs a re-declared freeze before exit 0 is reachable.

## MEDIUM

**F4 — clause 3's `axes` correction form is unreachable.** `CORR` = `(seats|window|path|rev)`
(`:50`), so `- corrects axes coverage: 138/138` is silently dropped: A12 has 4 correction lines, the
counter reports `corrections: 2`, `corrections_bad []`, exit 0 (`0a8e4759a8bb697d`). `corrects()`
also carries an `axes` branch (`:280-290`) and a duplicated unreachable one naming an undefined
`atom` (`:292-296`). Consequence: the two `## Owned axes` rows must be edited in place, and "exempt
every atom" can never be green — A1b (all-true corrections, record untouched) exits 1 with
`mismatches 2` = the two axes atoms (`7874a823e3eed8be`).

**F5 — a `rev` correction re-derives less than the atom.** Atom: resolves **and** is an ancestor
(`:231-237`); correction: resolves only (`:300-302`). A7 cites non-ancestor side commit
`ea6d6e27…` and exempts it: exit 0, `exempted [seats:45, rev:ea6d6e27]` (`1a1b9b3b5cd2b706`) — the
R46-V3 defect class re-entering. The cap does hold: 4 exemptions → `exempted 4 > 3`, exit 1 (A11,
`c792c86735422cd3`).

**F6 — `corrections >= 2` is satisfiable by out-of-scope corrections.** A3 (`2e4ae434`) exempts
`seats`/`window` keys older than the window from the "atom does not exist" arm. A14's
`- corrects seats round-40: 2 waves, 80 seats total` (round 40 = 42+38 dispatches; card covers
45–46) is accepted with `corrections_bad []`, exit 0 (`74c6752abc5084ee`) — contradicting the
claims' clause 3 sentence "A correction that exempts an atom the card does not contain is itself a
defect".

**F7 — landing trap: the battery requires `round-<N>` and an `empty in` line.** `wrong_total`
matches `- corrects seats round-[0-9]+:`; the counter-acceptable short key `seats 45:` makes the
forgery a no-op → `forgeries_green 1` → permanent red (A9, exit 1, `dca58a1d8b2fb634`). No window
correction → same (A8, `a68048d238d248ca`). Neither rule is in the claims file.

## LOW

**F8 — `--json-out` into a missing directory reports "not met".** `gate.emit` does not create
parents and the `FileNotFoundError` escapes `main_guard`: observed exit **1**, traceback, no
receipt, where the correct verdict is exit 2 could-not-evaluate.

## Passes (red for the right reason)
Exempt-everything (A1/A1b) · ghost atom (A2: two `corrections_bad`) · contradicted seat total
(A3: `claimed [2,75]` vs `derived [2,76]`) · non-empty window (A4: `empty False`) · exemption cap
(A11: `exempted 4 > 3`) · window over a nonexistent pathspec (A15: the atom verifies, the battery's
root..rev forgery stays empty → exit 1, `9b4a149695d7c0e7`).

## Measured landing path
A10 is the known-green shape: record made true by hand, `## Owned axes` rows edited to `138/138` /
`23/23`, one `seats round-45: 2 waves, 76 seats total`, one empty `window round-46` line. Exit 0,
`exempted []` (`7797253dec9fabad`). Its window is degenerate (`A..A`) — a "reproducibly empty"
window survives clause 3 while the battery's root..rev forgery stays non-empty, the same concession
A2's paragraph makes ("empty by construction"). Corrections become decoration once the record is
true, which is why F1/F2 matter.

## Files changed by this seat
Only `.ufo/waves/round-47/w1/C2Vacuity/` (report, receipts, cards, builder, two interpreter copies)
and this file. No lane file, no frozen byte, no git state. Scratch
`/fast/scratch/hyaku/kaidoku-r47/C2Vacuity` removed after the receipts were copied. No installs.
Not run: `exact.py` (C1), `record.py --selftest` (L1 gate).
