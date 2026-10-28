# C1Digest — R47-C1 clause 6 verified on the frozen counter, and block-24 rows drafted

Lane `kaidoku-shokunin`, round 47, wave 1. Read-only on the lane; writes only under
`.ufo/waves/round-47/w1/C1Digest/`. No installs, no commits in the lane, no subagents.

Detail: `C1Digest/report.md` (runs table, findings), `C1Digest/rows.md` (paste-ready rows and
values), `C1Digest/receipts/` (raw stdout per run, variant block bytes, driver sources).

## Verdict

Clause 6 — `mutations_sha256` = `sha256("\n".join(name for name, _ in MUTATIONS))` plus the four
mutation names in the block — is **met by block 24 as landed**, and it **fails** for every digest
or name set it is supposed to catch. Measured revision
`REV = 2e4ae43463aabdae707f8c8a4daa41441ad67a71`; counter exit 0, `failing []`, battery
`forgeries 4 / v2 4 / v3 0 / genuine 1 / crash 0` (stdout sha256 `43cc50b1…`, `receipts/e4-lane-self-freeze.out`).

At the brief's freeze `5017e1f` the clause is unreachable — the counter exits 1 with
`block_present 0`, `rule_blocks 23`, `marker_occurrences 0` (stdout sha256 `88fafc60…`,
`receipts/e1-freeze-do-nothing.out`), exactly as the brief states.

The two pins, re-derived independently (`ast` walk + `re` over the `MUTATIONS` literal, and
`git show REV:tools/round-47/exact.py | sha256sum`):

- `mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112`
- `interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`
  (byte-identical at the freeze, A1, A2 and `REV` — the amendments touched claims and `record.py`, never `exact.py`)

Isolation, one commit each in a fixture clone, `--freeze REV`:

| probe | counter |
|---|---|
| digest over three names / sorted / trailing newline | exit 1, exactly `mutations_sha256 does not match the counter's own mutation list` |
| four names removed | exit 1, exactly `mutation names not stated in the block: [all four]` |
| both broken | exit 1, exactly those two entries |

## Rows

The arm cells must be **bare tokens** (`exact.py:235-239` compares the stripped cell for
equality). The landing commit `e856beb` satisfied clause 6 and failed only clause 5 on four cells
(`symbol: the arm cell must equal …` etc.); A2 fixed it by deleting the explanations. Paste-ready
alternatives, all measured green (`receipts/raw/P1-candidate.out`):

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL4 deleting a mutation changes the denominator the claim is judged on | `forgeries_total` is compared with a number the code computes, and nothing pins the list | `digest` | 1 |

plus `symbol` / `once` / `order` rows in the same form, and an optional `Arms:` paragraph that
restores the per-token semantics outside the cells. `rows.md` §4 has them verbatim, with the
line-selector table that resolves at `REV` (`refs 8`).

## Findings the L1 needs before writing the landing report

1. **HIGH — the freeze series.** A1, A2 and A3 each modify a frozen path, so only a freeze equal
   to the last such commit evaluates. At `rev 2e4ae43`: `--freeze 5017e1f` / `9018c53` /
   `62e33f7` all exit 2 `frozen_path_changed`; `--freeze 2e4ae43` exits 0. The existing
   `l1/scores/c1-at-A2.json` receipt (freeze = rev = `62e33f7`) no longer covers A3. One more
   frozen-path commit resets it again.
2. **MEDIUM — the clause-6 anchor moved** from `plans/round-47-claims.md:78-79` (freeze, 190
   lines) to `:99-100` (`REV`, 211 lines). Clause 8 checks resolution only: a citation moved to
   lines addressing a different paragraph still scores exit 0 (fixture `K8`).
3. **MEDIUM — the name half is a substring test.** A block that keeps all four names while
   saying three of them are unscored scores exit 0 (fixture `K7`) — R46-CL3's class re-entering.
4. **LOW-MEDIUM — first pin wins.** A second stale `mutations_sha256` under the table is not read
   (fixture `K6`, exit 0); same for `interpreter_sha256`.
5. **MEDIUM — the pin covers names, not mutators.** A no-op mutation is counted as a green v2
   forgery (`exact.py:351-357`), so clause 9 passes with a dead forgery
   (`receipts/noop-mutator.json`). Guarded only by the interpreter pin and the freeze/dirty arms.
6. **INFO — block 24 cannot cite `tools/round-46/gate.py`**: outside `ALLOW`
   (`exact.py:36`), so citing it exits 1 `outside the validated path set` (fixture `K9`).
7. **INFO — S143's `used-by` cell** names `corpus/lessons/round-47.md`, which is absent at `REV`.

Nothing frozen was edited, and no fix is proposed inside frozen bytes: these are round-48 routed
defects if the L1 wants them closed.
