| tool | gate or probe | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner |
|---|---|---|---|---|---|---|
| `tools/round-44/c2-counter.py` | gate — R44-C2 calibration: re-derives each of the 80 frozen rubric statements at `--rev` from the rubric blob at `--freeze`; admissible only when every frozen path is byte-identical at `--rev` | `0` met; `1` not met (each mismatching entry id named in `mismatches`); `2` could-not-evaluate, including `frozen_path_changed` — a commit in `FREEZE..REV` that touches a plain frozen path still reds after a later restore, but an `expected_edit`-bound path (`SCORECARD.md`) restored to its freeze bytes reads `unchanged` (R44-CL10) | `python3 -I -B tools/round-44/c2-counter.py --selftest` — 24 arms, exit 0, green at `f762b72` (2026-10-28) | `tools/round-44/c2-rubric.json` and `tools/round-44/c2-counter.py` (frozen by constant), the rubric's `frozen_paths` `SCORECARD.md`, `SHONEN.md`, `SKILL.md` and `frozen_dirs` `tools/round-44`; `plans/round-44-claims.md` is pinned by `tools/round-44/c1-counter.py`, not by this counter | `--work` scratch, `--json-out` | kaidoku |

## Cell map (7 columns, matching the `### Round-44/45 instrument registry` header)

1. tool — exact backticked repo-relative path (what `tools/round-45/c2-counter.py`
   `ROW_TOOL`/`parse_rows` matches and compares by path equality).
2. gate or probe — `gate`: it emits a claim score (`claim_gate.usable_as_claim_score`), it
   does not merely probe.
3. verdict map — `0`/`1`/`2`, each with its reason class; the restore caveat is stated
   because the claim text's "a later restore does not un-block" is only true for the
   plain-frozen arm (measured, see `receipts/restore-probe.json` vs `receipts/bound-probe.json`).
4. self-test command — the exact argv that runs green from the lane root, with the measured
   arm count.
5. pinned-value path — what the counter itself freezes (`frozen_spec` = 5 paths +
   `frozen_dirs` = 1), not what the claims file freezes in prose.
6. write scope — `--work` (scratch clone and exported tree, removed unless `--keep-work`)
   and `--json-out`; nothing is written to the lane tree.
7. owner — `kaidoku`.

## Row validated against the round-45 registry scorer

```
$ python3 -I -B -c "…import tools/round-45/c2-counter.py; parse_rows(row); exits_ok(cells[2])…"
rows 1 cells 7 tool tools/round-44/c2-counter.py
first_cell_exact True
exits_ok True
trailing_pipe_ok True
```
(UTC 2026-10-28T15:43:46Z, exit 0 — `receipts/row-final.txt`.)

## Delta against the row already landed at `SKILL.md:1638`

The landed row passes the R45-C2 predicate (exact first cell, exit cell names `0`/`1`/`2`),
so this draft is an accuracy correction, not a rescue. Three changes:

1. **pinned-value path** — landed: "`tools/round-44/c2-rubric.json` (frozen) and
   `plans/round-44-claims.md`". The counter never adds the claims file to `frozen_spec`
   (measured: `frozen_spec == ['SCORECARD.md', 'SHONEN.md', 'SKILL.md',
   'tools/round-44/c2-counter.py', 'tools/round-44/c2-rubric.json']`; the claims path occurs
   only in the module docstring at `tools/round-44/c2-counter.py:4` and a comment at `:129`).
   `plans/round-44-claims.md` **is** pinned — by `tools/round-44/c1-counter.py:273`.
2. **self-test cell** — landed carries no arm count, unlike every sibling row. Measured:
   24 arms, all `ok`, exit 0.
3. **gate cell** — "admissible only when every frozen path is byte-identical at `--rev`" states
   the actual claim gate; plus the exit cell now states the `expected_edit` restore hole
   instead of implying the claim's blanket "a later restore does not un-block".
