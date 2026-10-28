# R46W1RegM — round-46, wave 1, tag `reg-m`

Seat: leaf executor. Lane read-only; write scope this seat's report dir plus scratch
`/fast/scratch/hyaku/kaidoku-r46/R46W1RegM` (removed at yield). Freeze read:
`31820472784284727546808acc31b3ea1e73919b`.

Deliverables in this directory:

- `rows.md` — the paste-ready registry rows (this is the artefact; paste from here verbatim).
- `receipt.md` — every command, its exit code, stdout sha256 and UTC time.
- `evidence-m-2rows-frozen.json`, `evidence-r-full38-frozen.json`,
  `evidence-t-full38-patched.json` — the three counters' receipts behind the finding below.

**Installs: none.** No package, binary or model change; pacman untouched.

## Rows (2, not 3 — deliberate)

`rows.md` carries two rows:

1. `` | `tools/round-41/sqfs-triage-v3.py` | `` — probe: labels REA extract-firmware
   envelopes from the craft-section table v3; verdict map `0`=table parsed and every
   envelope printed a label line (or `--table-only`, or `--selftest` green), `1`=only a
   `--selftest` case failed, `2`=malformed/refused table, unreadable envelope, or missing
   `--skill`.
2. `` | `tools/round-43/c2-score-r43.py` | `` — gate: 13 checks bound into one receipt;
   `0`=all 13 true, `1`=a check false, `2`=clone failure or usage error.

Both are 7 cells, 8 pipes, single-line, cell 0 exactly the backticked path, cell 3 binding
`0=`, `1=`, `2=` (verified mechanically: `ROWS_OK count=2`, `row1 cells=7
cell1_exact_path=True exitmap=['0','1','2']`, same for row 2).

**Why two and not the "three" the seat spec asks for.** The spec names two instruments and
`w1-spec.json` item `R46W1RegM` lists exactly those two. The census has 38 paths for 13
registry seats: twelve seats own three and one owns two. The round-41 group has 13 paths for
13 seats and the round-43 group's fourth path is `c2-score-r43.py` after RegA/RegB/RegL took
`heldout-gen-v4r43.py`, `verify-copies-r43.py` and `c1-counter.py`, so this seat is the
2-path one and `three` is stale boilerplate. Every other census path is already assigned to a
sibling (RegK: `mk-l-carriers.py`, `unblob-logtee.sh`, `gate.py`; RegL: `sqfs-list.py`,
`c1-run.sh` group leftovers, `registry.py`); a third row here would duplicate a sibling's
assignment. If the L1 wants three rows from this tag regardless, say which path — I will not
invent ownership.

## Evidence the rows are true (not read off a docstring)

`sqfs-triage-v3.py` (`6ad2b4e1…` at the freeze):

- `--selftest` → **0**, `SELFTEST cases=69 pass=69 fail=0` (16:55:35Z).
- Minimal valid v3 document: `--table-only` → 0, `rules: 1`; one envelope → 0,
  `env-ok.json<TAB>clean<TAB>none`.
- Refusals all exit **2**, never 1: `--table-only` without `--skill` (`--skill is
  required…`), an absent document, a `v2` marker (`refused marker`), argparse-rejected
  `--print-table`.
- A domain-mismatched envelope prints `unclassified none` and still exits **0** — recorded in
  the row as "label line", not "labelled", because 0 means *evaluated*.
- No exit code outside {0,1,2} exists in the source (`return 1` occurs only at the end of
  `selftest()`).

`c2-score-r43.py` (`459cbccb…` at the freeze):

- `--help` → 0 (eight flags, **no `--selftest`**; `grep -c -- --selftest` = 0, so the self-test
  cell is `none`).
- No args → 2 (argparse); `--selftest` → 2 `unrecognized arguments`.
- Clone from an empty root → **2**, receipt `exit_code 2`, `clone.exit 128`.
- Fixture repo containing only the tool, cloned clean at the measured rev → **1**,
  `checks_ok false` on the 13-key check map.
- The 13 check names and the pinned `MAP_SHA256` were read from the source at the freeze; the
  row's pinned-value cell names `corpus/evidence/local-sources.json` because that digest is
  a literal there.

**Calibration caveat encoded in row 2's cell 3.** A sub-receipt that cannot be produced at
all (wrapper or gate missing from the clone) is *not* mapped to 2: `receipt_wrapped` returns
2 with `receipt-unreadable`, that 2 lands in `gate_exit_zero: false`, and the process exits
**1**. Measured in the fixture receipt: `gate.error = "receipt-unreadable: …gate-receipt.json"`,
`wrapper_exit 2`, outer exit 1. An uncaught Python exception would land on 1 the same way. The
row says 1 includes "a sub-receipt that could not be produced at all" rather than claiming a
purity the source does not have. If the L1 prefers the row to claim only "a check false", the
instrument needs a could-not-evaluate branch it does not have.

## My rows measured against the frozen counter (self-attack, before data)

Fixture repo (`git rev-parse --show-toplevel` asserted) containing only `SKILL.md`,
`census.json` (the two paths), `plans/round-46-claims.md`, and the two tools:

- honest rows → **0**, `registered` both, `unregistered []`, `thin []`, `absent_at_rev []`,
  `failing []`, `met_target true` (`evidence-m-2rows-frozen.json`).
- verdict-map cell rewritten to `0 of 1, 2` → **1**, `thin ['tools/round-41/sqfs-triage-v3.py']`.
- cell 0 rewritten `see \`path\` (wrapper)` → **1**, `unregistered ['…sqfs-triage-v3.py']`.
- honest rows restored → **0** again.

So the rows are accepted by the same clauses they will be scored under, and the two ways a row
can look right while being empty are both red.

## Finding: R46-C2 clause 6 is unsatisfiable as frozen (reported, not fixed)

`tools/round-46/registry.py` computes the battery's `v1_green` with
`score(text, f, spec_name, "v1", frev)`. Inside `score()`, `strict_header`, the section
binding and the header check are gated on `hard = profile == "v2"`, but `strict_cell` and
`strict_exit` are read straight off `SPECS[spec_name]` **without** that gate. With the
counting command's default `--spec r46`, the v1 profile therefore still demands exact cell-0
equality and a real `0=/1=/2=` map, so the `substring-cell` and `prose-exit` forgeries are
rejected by v1 too.

Measured, on a synthetic **full-census 38-row** section whose v2 score is fully green
(`unregistered []`, `thin []`, `absent_at_rev []`, `genuine_green 1`, `v2_green 0`,
`forgeries_total 7`):

```
failing = ['battery v1_green 5 != 7']          registry.py --root <fixture> … exit 1
  substring-cell  v1=1 v2=1   prose-exit  v1=1 v2=1
  fenced v1=0  off-section v1=0  html-comment v1=0  first-wins-shadow v1=0  no-header v1=0
```

`v1_green` is at most 5 of 7 on any section, clause 6 requires 7, so `met_target` is always
false and R46-C2 can never exit 0 — and `tools/round-46/` is frozen, so a repair is itself a
`frozen_path_changed` for both counters. This is a pre-data kill of the claim, not a
calibration nicety.

The root cause is one predicate. A scratch copy with
`if spec["strict_cell"]` → `if hard and spec["strict_cell"]` and the same for `strict_exit`
(no other change) scores the identical section **0** with `v1_green 7`, `v2_green 0`,
`forgeries_total 7`, `genuine_green 1`, `failing []`
(`evidence-t-full38-patched.json`). Commands R and T in `receipt.md` are the pair.

The C2 preflight sentence in the claims file does not cover this: `registry.py --selftest`
(`cases=11 failures=0`) only asserts that v1 accepts the *fenced* forgery
(`red-v1-accepts-fenced`), never that v1 accepts `substring-cell` or `prose-exit`.

Related, smaller: `plans/round-46-claims.md` cites `controls/ctl-c2-1-v1-profile.json` for
"the v1 clause set scores all seven forgery classes green". That file does not exist. The
nearest receipt, `controls/ctl-c2-1-v1-scope.json`, is `counter: round-45-c2`,
`scope_size 6`, and has no `battery` key — a six-row scope, not a seven-class battery. The
7/7 sentence is unreceipted.

Observation, not a verdict, on C1: `attest.py`'s structural clause guards are consistently
`hard`-gated (`if hard and` on `block_is_last`, the title prefix and row cell-count in the
lines read at the freeze), so the same defect class does not appear there. Whether
`battery.v1_green == 9` is reachable in `attest.py` is not this seat's measurement — **not
run**.

## Risks and blockers

- **R46-C2 cannot reach its target** in the frozen configuration; the L1 must decide between
  accepting the claim fails, a new freeze (which resets the frozen-path baseline), or a
  documented exception. I did not touch the instrument.
- My two rows are correct against everything except clause 6, which no row can satisfy.
- Row count is 2 by construction of the census/seat split; if the wave validator requires a
  literal three, the extra row must be assigned explicitly rather than invented here.
- Not run: any REA/extraction work, `attest.py` battery, `registry.py` on the real lane tree
  (its `--json-out` must stay inside `--root`, and the real tree is read-only for this seat;
  the fixture reproduces the whole clause set with the frozen `gate.py`).

## Cleanup

`/fast/scratch/hyaku/kaidoku-r46/R46W1RegM` removed at yield after copying the three
receipts above. Nothing was written under `/tmp`; no mutating git verb ran in the lane.
