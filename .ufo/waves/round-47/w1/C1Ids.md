# C1Ids — R47-C1 clause 4 (routed-id cardinality): verified, falsified, rows drafted

Freeze `5017e1f7299c3a812e87e7950148f54313dd279e`, measured lane rev `3186f69b49798f2cc05727bbfd1604505fcee03b`.
Full report: `.ufo/waves/round-47/w1/C1Ids/report.md`; paste-ready rows:
`.ufo/waves/round-47/w1/C1Ids/rows.md`; receipts `.ufo/waves/round-47/w1/C1Ids/receipts/`.

## The clause

`plans/round-47-claims.md:74-75` — every row's trigger cell names exactly one `R46-CL<n>` id,
multiset exactly `{R46-CL2, R46-CL3, R46-CL4, R46-CL6}`. Code: `tools/round-47/exact.py:217-233`
(`ID.findall(r[0])`, `len(ids) != 1` → `rows naming != 1 routed id`, then
`sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}` → `routed cardinality …`).
Claim and code agree; the scan is trigger-cell-only (`r[0]`).

## Measured

| fact | evidence |
|---|---|
| freeze run: exit 1, `block_present 0`, `rule_blocks 23`, `marker_occurrences 0` | `receipts/freeze-run.json`, stdout sha256 `88fafc60…` (2026-10-28 17:48Z) |
| the failing list there is 2 marker lines because `score()` early-returns at `exact.py:186-188` — clauses 2–9 are never reached | receipt + code |
| block 24 is **uncommitted** (`git show 3186f69b:SKILL.md` = 23 craft blocks, 0 markers; ` M SKILL.md`) | `receipts/head-commit-run.json`, sha256 `01078be6…` |
| clause 4 fires: `dup-id`, `multi-id-cell`, `id-in-hole-cell` → exit 1 with clause-4 messages | `receipts/clause4-v3.json` |
| clause 4 satisfied: `full` → exit 0, `routed_counts {CL2:1,CL3:1,CL4:1,CL6:1}`, battery 4/4/0 | same receipt, case `full` |
| clause 4 independent: `partial-header-digest-ref` keeps it green while clauses 2/6/8 are red | receipt shows no clause-4 line in `failing` |

## Falsification (the valuable part)

Clause 4 does **not** close R46-CL3. Three tables keep the id multiset perfect and pair ids
with the wrong holes — all **exit 0, battery 4/4/0**:

- `permute-ids` — CL2/CL3 trigger ids swapped, holes left behind;
- `copyrow` — rows 2–4 are row 1's hole/arm with ids CL3/CL4/CL6;
- `one-hole-four-ids` — four distinct ids, four distinct arms `symbol/once/digest/order`, and
  **all four holes are R46-CL2's hole**.

`dup-arm` (arms `order`×4) is also exit 0, consistent with the frozen text (membership, not
distinctness). Net: id→hole and id→arm are unbound; a green `failing == []` certifies the
token multiset, not the matrix. Not fixable without changing frozen bytes — I did not.

Two adjacent findings: `ALLOW` (`exact.py:36`) excludes `tools/round-46/gate.py`, so citing
the file clause 7 reads fails clause 8 with `outside the validated path set` (`cite-gate46`,
exit 1); and `--profile v2` still scores the genuine block with the v3 scorer
(`exact.py:346`), so v2 is not a lenient escape (`multi-id-cell` (v2) → exit 1,
`battery genuine_green 0 != 1`).

## Landing state — and the freeze has moved

Block 24 landed at `e856beb5`; its arm cells were rewritten to single tokens at `62e33f7d`
(that rewrite is the mid-wave edit I saw: the same fixture scored exit 1 on clause 5,
`arm cells not exact vocabulary tokens`, at 17:51:11Z and exit 0 after). Clause 4 on the landed
bytes: `routed_counts {CL2:1,CL3:1,CL4:1,CL6:1}`, green. `rows.md` §5 still holds four drop-in
rows that keep the arm explanation in the hole cell (clause 5 is an equality on that cell) and
`rows.md` §6 the whole block I measured (`df731f78…`), in case you prefer either.

Three real-repo runs at the current tip `caafeffa330a15e59412bc037591f6942b51e5aa`:

| freeze | exit | result |
|---|---|---|
| `5017e1f…` (this wave's freeze) | **2** | `frozen_path_changed` — `touched` = `plans/round-47-claims.md`, `tools/round-47/record.py` |
| `9018c53b…` (A1 — the freeze the claims file *declares*) | **2** | `frozen_path_changed`, same two paths |
| `1e2c3102…` (A4 — newest commit touching a frozen path) | **0** | `failing []`, `met_target true`, `routed_counts` each 1, battery 4/4/0, `gate_order_literal 1` / reversed `0` |

So the amendment series is **four**, not the "series of two" the claims file declares, and the
sentence naming A1 as the freeze is falsified by its own frozen paths: A2/A3/A4 edited the set
after it. The only freeze that reaches a verdict at the tip is A4. Receipts:
`receipts/at-tip-stale-freeze.json` (`0f5dfd70…`), `receipts/at-tip-a1-freeze.json`
(`2782b5fd…`), `receipts/at-tip-a4-freeze.json` (`10f49044…`). Pins verified from the green
receipt: `interpreter_sha256 dcef54f1…`, `mutations_sha256 19a2166e…`.
