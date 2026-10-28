# Round 47 — an equality, not a containment; and the record re-derived against the repo

Lane `kaidoku`, round 47, attempt 1. Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`. Freeze series
`5017e1f7` → A1 `9018c53b` → A2 `62e33f7d` → A3 `2e4ae43` → A4 `1e2c310295` → A5 `07d2894e` → A6 `f54b3b6d` (declared freeze).
Instruments `tools/round-47/{exact,record}.py`; landing `SKILL.md` craft block 24, the SCORECARD
corrections section and the two axis heads, S143/S144.

The round exists because the round-46 non-author spot-check routed four instrument defects and one
HIGH record defect, and the lane had no command that could read its own record: every counting
command it owned read the artefact, none read the claim.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M47-1 | `unreachable-clause` — the first frozen `record.py` required a `window` correction's `A..B` pair to already appear in the card, while the only in-scope window atom names a `<tip>` placeholder, so no conforming correction could satisfy it and the C2 target was unreachable | `plans/round-47-claims.md` (A1 paragraph) against `.ufo/waves/round-47/controls/ctl-c2-2-freeze-amendment.json` (`corrections_bad: [window pair names no atom in scope]`, exit 1) | `none` — the pre-freeze satisfiability check asked "can the counter compute this value", never "can a truthful artefact satisfy this clause" | A1 `9018c53b` deletes the clause; the red-before receipt is committed and the landing's own corrections section then re-derives |
| M47-2 | `no-op-forgery`, twice — (a) the `correction-window-not-empty` forgery replaced the correction's window with `<A>..<tip>`, but `<A>..<tip>` is empty by construction, so the forgery scored green (`forgeries_green 1`); (b) after the record section landed, the `correction-ghost-atom` forgery appended its line at the end of the card, outside the corrections section the parser reads, and scored green again | (a) `l1/scores/c2-at-L1.json`; (b) `l1/scores/c2-at-R1.json` — both `battery.forgeries_green 1`, exit 1 | the battery asserted green/red counts but never that a forgery differs from the artefact in the dimension it names, and never that its injection point is inside the surface the parser reads | A2 `62e33f7d` makes the forged window root..tip; A5 `07d2894e` injects the ghost line inside the corrections section; `c2-at-A5.json` reads `forgeries_green 0` |
| M47-3 | `scope-rule-broken-by-the-record` — the counter reads the last two `## Round N` sections; appending this round's own section moves the round-45 seats atom out of scope, so its correction would become a ghost exemption and fail the round's own target | `tools/round-47/record.py` `corrections()` ghost check against the round-47 section this commit adds | `none` | A3 `2e4ae43` treats a seats/window correction for a round older than the window as historical evidence that must still re-derive; selftest case `green-historical-correction` |
| M47-4 | `abbreviation-ambiguity` — the record cited `1e2c3103`, an 8-hex abbreviation git resolves ambiguously, so the claim's own `rev` atom would have failed `rev-parse` | `git rev-parse --verify '1e2c3103^{commit}'` → "unknown revision" while `1e2c310295` resolves | the `rev` atom class (it is exactly the check that catches this) | the record states `1e2c310295`; the class re-derives every cited hash |
| M47-5 | `claim-that-failed-its-own-clause` — the first landed block 24 carried prose in the arm cells (`symbol: the arm cell must equal …`) while clause 5 binds the cell to exactly one token | `l1/scores/c1-at-L1.json` (exit 1, `arm cells not exact vocabulary tokens`) | clause 5, the exactness binding the round added — the defect was caught by measuring the landing against the freeze, not by prose review | block 24's arm cells now read `symbol`, `once`, `digest`, `order`; `c1-at-A2.json` and `c1-at-A4.json` read exit 0 |

| M47-6 | `proxy-harm-recurrence` — block 24 first landed citing lessons and plans only, so command A read `citation_resolved_rules 23/24`, `depth_score 9.58`: a depth claim that lowers the depth proxy. This is round-46's M46-4 exactly, one round after `QUALITY.md` row 77 required a new craft block to cite a knowledge entry | the worktree re-derivation (`rule_blocks 24 resolved 23`) against the record's `24/24` cell | `QUALITY.md` row 77 — it existed and was not applied, so the rule's *enforcement* is what failed, not its content | the block now cites `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`; the worktree re-derivation reads 24/24 before the landing commit |
| M47-7 | `pin-couples-the-landing-to-the-freeze` — block 24 pins `exact.py`'s sha256, so every counter amendment invalidates the landed pin: after A6 the claim failed on `interpreter sha256 pin does not match the bytes at rev` and needed a second landing edit | `l1/scores/c1-at-A6.json` (exit 1, pin mismatch) | `none` — the pin is the point, and nothing told the author that its cost is one landing edit per amendment | the pin now reads A6's bytes (`01a4bca7…`); `c1-at-A7.json` exits 0; routed as R47-CL8 |
- **R47-CL6 (wave-1 `C1Battery`).** Clause 5 binds *membership*, not row→arm: a permutation of
  the four tokens across the four rows passes with every routed id intact, so the matrix can state
  the wrong arm for a defect and still score met. Closing it needs a per-row expected token keyed by
  routed id, which the block would have to carry.
- **R47-CL7 (wave-1 `C1Battery`).** Clause 8 counts resolved references, not distinct ones: six
  copies of `corpus/lessons/round-46.md:1-2` satisfy `refs >= 3` while grounding nothing. The block
  as landed cites five distinct paths, but the clause does not require that.
- **R47-CL9 (wave-1 `C1Battery`, F4).** The `--profile` switch also moves the battery gate, so
  `--profile v2` alone exits 1 on a genuine block (`battery genuine_green 0 != 1`); the ported-profile
  control must be `--profile v2 --no-battery`, which is what `controls/ctl-c1-1-v2-profile.json` runs.
  A profile is not a pure selector while the battery result is applied in both profiles.

## Gate

### Sources opened this round (2026-10-28)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S143 | https://docs.python.org/3/library/re.html | 2026-10-28T17:52Z, HTTP 200, 257,706 bytes, page sha256 `f169ed065bf6e6ad779dd7049e6e4ce4ac1081c10eb3f40cd079b0a1f9d11f6a`; anchor `re.fullmatch(pattern, string, flags=0)` | "If the whole string matches the regular expression pattern, return a corresponding Match. Return None if the string does not match the pattern" (24 words) |
| S144 | https://docs.python.org/3/howto/regex.html | 2026-10-28T18:01Z, HTTP 200, 165,172 bytes, sha256 `5e205f7d5a4e3c66f9d044625d170059a16f979cf996b6ccaa1ba37f7da7f9be`; the token `fullmatch` occurs 0 times in the rendered text | REJECTED — "the page teaches regex syntax and never defines the whole-string primitive"; flip: an edition that documents `fullmatch` beside `search` with its return semantics |

S143 is cited by block 24's R46-CL2 row and by `tools/round-47/exact.py`'s arm clause: the equality
`re.fullmatch` gives is what makes `order-ish` fail a `order` token test that `re.search` passes. It
enters as `mined`, tier A, `recheck on-release`, `used-by corpus/lessons/round-47.md`. S144 enters
as a `rejected` row with its flip condition, `used-by —`.

Status / recheck / used-by changes to existing rows this round: none. No row was re-pointed.

### Admission and rejection

- **Admit** S143 (`docs`, tier A): opened this round, cited by the round's C1 landing.
- **Reject** S144 (`docs`, tier C): opened and refused as redundant — the HOWTO never defines
  `fullmatch`; flip condition recorded in its row.
- **Assimilation: none.** No `merge/kaidoku/` theme and no `considerthese/` proposal applies to an
  instrument-exactness round (`considerthese/` is absent in this lane); the round-44 quarantine
  refusals stand and nothing is adopted.
- **Census before → after:** `corpus/SOURCES.md` rows 142 → 144
  (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`), of which one admitted and one
  rejected. Round-end census: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
  exit 0.

## Routed defects (for round 48)

- **R47-CL1.** Both counters grade committed bytes but EXECUTE from the worktree; `gate.freeze_state`
  refuses a dirty *frozen* path only, so a replaced non-frozen helper is still an unexamined
  instrument. Stated, not closed.
- **R47-CL2.** The `axes` class binds the row's leading fraction, not the 0–10 score cell beside it:
  a stale score with a fresh fraction passes.
- **R47-CL3.** `CORR_MIN = 2` is a floor on how many corrections exist, not on whether the corrected
  claims matter; a round could correct two trivial atoms and exempt a serious one (bounded by
  `exempted <= 3`).
- **R47-CL5.** The freeze is a series whenever the instrument is authored in the same round as the artefact it scores: five amendments before verdict here. A counter amendable after the landing cannot be told apart from one tuned to it, so the only defence is the red-before receipt per amendment, which this round commits.
- **R47-CL8.** A self-pinning artefact couples the freeze series to the landing: each counter amendment forces a pin update in the artefact, so a round that amends its counter also rewrites the thing it grades. The alternative (pin the *interpretation*, not the bytes) loses the anti-stub guarantee.
- **R47-CL4.** `mutations_sha256` is over the mutation *names* in order; a behaviour change that
  keeps the names (a mutation body edited to return the block unchanged) is invisible to the pin,
  though the battery's `v2_green` count would move.
- **Inherited, still open:** R46-CL1 (squash-invisible tamper), R46-CL5 (registry `purpose` cell
  unchecked), R46-CL7 (HIGH: verdict-map digits, not meanings), R46-CL8 (claims-file `cases=11` and
  the non-runnable `--selftest` form).
