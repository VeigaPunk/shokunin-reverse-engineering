# Round 88 — claims (kaidoku), frozen before data

Base revision `0cf8e3243059e0bc510b90c880d13d191e78d732` (lane `main`, = remote tip at round start).
Round-87 non-author spot-check (`corpus/lessons/round-87-verifier-spotcheck.md`) is the input: its
routed defects V87-1…V87-4 and the carried M87-3 ("a chain-walk-free heuristic also scores 8/8")
define what this round must not repeat.

Axis state (SCORECARD, all four owned axes at the saturation line 10.0/10): the stagnation nudge
(`AXES.md` §*The stagnation nudge*) waives the lowest-axis obligation and asks for a
frontier/capability move. R88-C1 is that move; R88-C2 is a depth move on the surface R88-C1 opens.

## R88-C1 — coverage (capability acquisition, frontier → core)

**Claim.** A packed UPX 5.2.0 little-endian ELF whose first `b_info` block's `sz_cpr` word has been
zeroed — `upx -t` answers `CantUnpackException: b_info corrupted`, and the round-87 repair refuses
with `p_info is not followed by a plausible b_info` — is repaired from chain geometry: the next
block starts exactly `12 + sz_cpr` bytes after this one, so the smallest offset above `block0 + 12`
that forms a plausible `b_info` under block0's method whose own chain reaches the end-of-chain
sentinel yields `sz_cpr = candidate - (block0 + 12)`; candidates are bounded by block0's `sz_unc`,
and the winner is the one that accounts for the most of the PackHeader's declared uncompressed
length `u_len` (a candidate claiming more than `u_len` is impossible; a shared object whose chain
does not cover its appended data still yields its single structural candidate).

**Predicate (one sentence, same in the counter and the receipt).**
`tools/round-88/upx-chain-battery.py --repair-cmd tools/round-88/upx-chain-repair.py` reports
`recovered 4 of 4`, `controls_ok` all true (`N1-refuse-plain`, `N2-corrupt-payload`,
`N3-intact-idempotent`), the round-87 regression arm met (`recovered 8 of 8`, its controls true), and
exit 0, where a case is recovered only when the repair exits 0, the output's only changed bytes lie
inside block 0's 4-byte `sz_cpr` window, `upx -t` on the output exits 0, `upx -d` restores the
carrier's pinned sha256, and REA 6.5.0 `analyze` of the restored bytes reports the carrier's declared
round-70 procedure count.

**Label.** `recovered 4 of 4`.

**Kill rule.** `recovered < 4`; any control false; the regression arm unmet; a case recovered through
a change outside the `sz_cpr` window; a repair that names, reads or hashes a carrier source path or
pin; a counter, population, tamper, arm, control or carrier changed after this declaration; REA or
packer pin drift.

**Counter.** `tools/round-88/upx-chain-battery.py` (pinned below). **Claimed artifact.**
`tools/round-88/upx-chain-repair.py`.

**Controls, scored by the frozen counter before this freeze** (all four receipts committed under
`.ufo/waves/round-88/pre/`):

| control | what it skips | measured |
|---|---|---|
| `identity` (do-nothing) | all repair work | `recovered 0 of 4`, exit 1 (`c1-control-identity-at-base.json`) |
| `naive-global` (round-87 cheap rule) | the geometry, global tail-word replace | `recovered 0 of 4`, exit 1 (`c1-control-naive-global-at-base.json`) |
| `r87-anchor` (base state: the round-87 repair unchanged) | the new class entirely | `recovered 0 of 4`, all three controls true, exit 1 (`c1-control-r87-anchor-at-base.json`) |
| candidate repair | — | `recovered 4 of 4`, controls true, regression 8/8, exit 0 (`c1-candidate-at-declaration.json`) |

The `r87-anchor` control is the base-state control: the round-87 repair refuses this class on every
carrier, so the target is not reachable without new work.

## R88-C2 — depth

**Claim.** The `## Queue-drain craft` rule block for packed-ELF refusal signatures lands: a tamper
that reaches a field of a packed UPX 5.2.0 LE ELF is triaged by the refusal UPX itself prints, from a
measured 4-carrier × 17-field matrix (`tools/round-88/field-tamper-matrix-v2.py`, 68 cells, 63
effective, 10-label vocabulary — the v1 instrument's 7 labels left 5 cells unclassified; the v2
supersession is recorded in `claims.json` `instrument_supersessions`) rather than from a guess, with the repair move each signature implies.

**Predicate.** `tools/round-88/depth-blocks.py --root . --rev <measured>` reports `blocks 28`,
`resolved 28`, `unresolved []`, exit 0, where a block resolves only when every
`corpus/knowledge/<name>.md[:line[-line]]` citation it carries exists at that revision and its range
is inside the file.

**Label.** `blocks 28, resolved 28`.

**Kill rule.** `resolved < 28`; any unresolved block; a block that carries no citation; a revision
that does not contain the new block; the block text changed after this declaration.

**Counter.** `tools/round-88/depth-blocks.py` (pinned below). **Evidence.**
`tools/round-88/field-tamper-matrix.py` receipt at the measured revision.

**Controls, scored by the frozen counter before this freeze:**

| control | what it skips | measured |
|---|---|---|
| base (do-nothing) | the new block | `blocks 27`, `resolved 27` (`c2-depth-at-base.json`) |
| junk blocks | content and citation | `blocks 29`, `resolved 27`, unresolved `[no-citation, absent-file]`, exit 1 (`c2-control-junk-blocks.json`) |

The new block cites `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md` (present at base)
and the matrix receipt path, so R88-C2 is verifiable without R88-C1 having landed.

## Instruments (committed before this file; pinned by sha256 in `claims.json`)

| path | role |
|---|---|
| `tools/round-88/upx-chain-repair.py` | claimed artifact (R88-C1) |
| `tools/round-88/upx-chain-battery.py` | R88-C1 counter, population and arms |
| `tools/round-88/field-tamper-matrix.py` | R88-C2 evidence instrument |
| `tools/round-88/depth-blocks.py` | R88-C2 counter |

Each ships `--selftest` (11, 6, 11 and 7 cases respectively) in the same commit as the instrument and
before the data it scores. No round-87 instrument is modified: the new repair composes the frozen
round-87 module by path and records its sha256 in every record.

## Named limits (declared now, not after data)

1. The repair derives `sz_cpr` from geometry and bounds it by `u_len` accounting; it does not
   decompress the block. The counter's `upx -t`/`upx -d` arms, not the repair, refuse a wrong
   derivation. A non-zero but wrong `sz_cpr` is left alone by the composed repair (selftest case
   `szcpr-nonzero-not-derived`). A carrier whose chain accounts for less than `u_len` (the shared
   object, 98,592 of 108,560) is accepted on its single structural candidate.
2. The class is one 4-byte field on four carriers. `p_blocksize`, `p_filesize`, adler and
   PackHeader-field tampers are measured by the matrix but are not repaired this round.
3. A repair that reads the original carrier and re-packs it would produce the same bytes; the counter
   scores bytes, not provenance.
4. The `sz_cpr` search is O(window) per l_info candidate with the round-87 walk memoised; a hostile
   file may still cost a linear scan (sentinel seat's subject).

## Frontier step (§2b)

- **Sources.** New rows opened this round for the geometry law (UPX v5.2.0 sources that define
  `b_info`/`p_info` layout and the "corrupted" refusals); at least one admitted row is cited by the
  R88-C1 knowledge entry (the sourced claim). Census before/after with
  `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`.
- **Mistake mined.** From round 87's own attack record (M87-3 overstatement, V87-1 instrument
  deleted with scratch) into `corpus/lessons/round-88.md` `## Mistakes`, with a fix shown able to
  fail.
- **Assimilation.** None this round (two-claim budget); `merge/kaidoku/` untouched. No
  `considerthese/` directory exists in this lane.

## Wave plan (one v1 wave, 8–16 seats)

`r88-w1`, 14 seats: executor 4 (matrix, independent geometry cross-check, mutation table, r87
regression), scout 2 (UPX source locators, host-class reconnaissance), scribe 2 (knowledge entry,
SOURCES rows), reviewer 2 (C1, C2), critic 1, mutation-tester 1, sentinel 1, connector 1. Attack
seats 5/14 = 36 % (≥ 25 %); one connector (≤ 2); the L1 holds the planner seat (the validator
rejects `planner`).
