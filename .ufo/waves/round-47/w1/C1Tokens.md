# C1Tokens — R47-C1 clause 5: verified, attacked, rows drafted (and the block has since landed)

Seat `C1Tokens`, round 47 wave 1. Scope: **R47-C1 clause 5 only** — every v3-arm cell is an
equality (`symbol`, `once`, `digest`, `order`), not a containment. Frozen surfaces read, never
edited: `plans/round-47-claims.md` and `tools/round-47/` (`tools/round-47/exact.py` sha256
`dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` at `5017e1f`, unchanged at
the current tip).

Full report with the run ledger, attack matrix and evidence index:
`.ufo/waves/round-47/w1/C1Tokens/report.md`. Drafted block:
`.ufo/waves/round-47/w1/C1Tokens/rows.md`.

## Verdict

| question | answer | evidence |
| --- | --- | --- |
| Does the frozen clause 5 close the round-46 substring hole? | **yes** on the cell: `order-ish`, `symbolmap`, `the symbol arm`, `Symbol`, zero-width suffix all go v2 green → v3 red | `attack-matrix.json` |
| Does it bind the arm to the defect its row names? | **no** — the landed block with four `order` arms scores exit 0, full battery green | `receipt-landed-allorder.json` |
| Is the landed block landable? | **yes** — exit 0, `failing []`, `refs 8`, battery 4/4/0/1/0 at freeze = tip `1e2c3102` | `tip-freeze-1e2c310.json` |
| Is the round's stated freeze still scoreable? | **no** — at tip, freeze `5017e1f` returns exit 2 `frozen_path_changed` | `tip-freeze-5017e1f.json` |
| Is the freeze's own before-state reproduced? | **yes** — exit 1, `block_present 0`, `rule_blocks 23`, `marker_occurrences 0` | `receipt.json` |

## Findings

**F1 (HIGH, claim-strength, not code-vs-claim).** Clause 5 tests each cell against `VOCAB`
individually (`tools/round-47/exact.py:235-243`). Neither the multiset `{symbol, once, digest,
order}` nor the id→arm pairing is bound, and the claims sentence — "every row's v3-arm cell is
exactly one token of …" — does not require them either. Measured **on the landed block**:
four `order` cells → exit **0**; CL2/CL6 arms swapped (`order, once, digest, symbol`, a matrix
stating the opposite of its rows) → exit **0**; both keep `battery {forgeries_total 4,
v2_green 4, v3_green 0, genuine_green 1, crash 0}`. The claims' kill rule (`blobberish` fails
clause 5) is a one-cell test, and the counter's selftest has 16 cases with no multiset case.
Fixtures `fx-landed-allorder-8ZsdXK` rev `b1af38d3b175c7ccfd48bb61d9cfb758bbb8a832` and
`fx-landed-swapped-tELJn3` rev `2f6a8ad38ddc6b2815ceb1e6c5428d350b4a756d`, rebuildable with
`fixtures/landed.sh`. A later-round repair is one condition
(`sorted(arm) != sorted(VOCAB)`) plus a claims sentence; the frozen bytes were not touched, and
the landed block does not need to change to satisfy the clause as written.

**F2 (MEDIUM, landing trap).** `ALLOW` (`tools/round-47/exact.py:36`) excludes
`tools/round-46/`, so block 24 **must not** name `tools/round-46/gate.py` even though clause 7
is a statement about that file — one such token fails clause 8 with `outside the validated
path set`. Block 23 cites `tools/round-46/attest.py` (`SKILL.md:612`), so the natural
continuation is the red one. The landed block keeps the gate file unnamed and is green; my
draft did the same.

**F3 (LOW).** `exact.py --selftest` exits 2 on missing required args; green (16 cases, 0
failures) only when `--root/--freeze/--rev` are passed. Same family convention as
`attest.py` (`SKILL.md:1743`), so the instrument row should record the argument-bearing spelling.

**F4 (INFO).** `strip("` ")` runs after `_cells` has already stripped whitespace, so only
backtick/space decoration is tolerated; no over-accept found beyond decoration. The looseness
in this clause is F1, not decoration.

**F5 (HIGH, operational — freeze drift).** The lane moved under this seat: `9018c53b` (freeze
amendment A1), `e856beb5` (land craft block 24), `62e33f7d` (A2, arm cells), `2e4ae434` (A3),
`1e2c3102` (A4), `07d2894e` (A5), `a631bba0` (A5 receipts) — and the tip advanced twice while
this seat was measuring it. Every one of A2–A4 edits a frozen path, so at the tip the prompt's freeze
`5017e1f` yields exit **2** with `frozen_path_changed ['plans/round-47-claims.md',
'tools/round-47/', 'tools/round-47/record.py']`. The claims file declares a two-commit freeze
series (`5017e1f`, then A1); scoring at the tip needs the series to end at the last commit that
touches either frozen path. A 2 is not a pass, so as the round stands the *stated* freeze cannot
produce a green R47-C1. Re-measured at `a631bba0`: freeze `5017e1f` → exit 2
(`tip-a631bba-at-promptfreeze.json`), freeze `a631bba0` → exit 0 with the landed block
(`tip-a631bba-at-self.json`).

## Deliverable

`rows.md` carries the ready-to-paste block 24 (insert after `SKILL.md:612-631`, before
`SKILL.md:632` at the freeze), sha256
`a57ce1214f830ca62fe7ef52e3b4d9403814a6e616ad5e9e39b9408f22e0694b` over the 1916 canonical
bytes, with `mutations_sha256`
`19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112`, `interpreter_sha256`
`dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`, and citation selectors
`corpus/lessons/round-46.md:51-69,57-59,60-62,63-64,65-69` and
`plans/round-47-claims.md:76-77` (freeze numbering). Run D is the counter executed on exactly
those published bytes: exit 0, `refs 7`, `failing []`, battery 4/4/0/1/0. The block that
actually landed (`e856beb5`, arm cells normalised at `62e33f7d`) carries **the same four
clause-5 cells in the same id order**; its prose and `Refs` are the L1's own wording.

## Risks

1. A green block is not a bound matrix: the landing record must not claim clause 5 proves each
   hole is closed by the arm its row names (F1, measured on the landed block).
2. Any permutation of the four arm cells still scores 0, so a red cell cannot be the signal
   that the pairing is wrong.
3. Freeze drift (F5) is the live scoring risk: measured revision, cited freeze and the
   claims-file bytes must name one commit.

## Tooling

No install, no package transaction, no `uv`/`npx`; `pacman` untouched. Python 3.14 stdlib and
read-only `git` (`show`, `log`, `rev-parse`, `diff`) only. Every fixture repo was created under
`/fast/scratch/hyaku/kaidoku-r47/C1Tokens` with `git -C "$D" rev-parse --show-toplevel` asserted
equal to `$D` before its single commit. Scratch was removed after the receipts were copied into
`.ufo/waves/round-47/w1/C1Tokens/`; rebuild scripts are in
`.ufo/waves/round-47/w1/C1Tokens/fixtures/` (`cli.sh`, `mkb.py`, `drive.py`, `verify_rows.sh`,
`gen_rows.py`, `tip.sh`, `landed.sh`).
