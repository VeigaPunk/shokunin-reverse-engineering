# R45-W1 — registry row for `tools/round-44/c1-run.sh`

Measured at `HEAD = faa875bc0eb839d15b83c4afa6078819e5a7b381`; the two instrument
files are byte-identical at the round-45 freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`
(sha256 in `receipt.md`). Frozen instrument directory `tools/round-45/` was read only;
nothing in `SKILL.md`, `plans/` or `tools/` was edited.

## The row (7 cells: tool | gate or probe | verdict map | self-test | pinned value | write scope | owner)

```markdown
| `tools/round-44/c1-run.sh` | probe — the after-freeze R44-C1 data procedure: one `npx -y rea-agents@6.5.0 extract-firmware` run per carrier (the four `scope.target_ids` by default), each written as a receipt tree; the wrapper pins `PATH` at `c1-run.sh:50`, appends `/kaidoku-r44` to the scratch base, and refuses the default evidence root without `--data-run`/`KAIDOKU_C1_DATA_RUN=1`; it does not run the oracle (`tools/round-44/c1-oracle.py` belongs to the counter) and does not verify `--freeze` (recorded only, `c1-run.py:897`) | `0` every carrier exited 0 and wrote its receipt, **or** `--dry-run` printed the plan and wrote nothing (`c1-run.py:952`, no receipt on this arm); `1` at least one carrier failed (pin mismatch, REA exit != 0, or no receipt; `c1-run.py:1045`), **and, undeclared in the header, any earlier abort**: a `set -euo pipefail` abort (`env -u HOME`, `c1-run.sh:50`) and an uncaught Python traceback (unwritable `--scratch`, `c1-run.py:841`) also exit 1 with no classification; `2` usage or environment refusal — `err()` (`c1-run.sh:43,45,52`), argparse usage error, missing lane root, unreadable carriers, `--carrier` matching nothing, the committed-evidence-root refusal (`c1-run.py:835`) | no self-test in either file; probes `bash tools/round-44/c1-run.sh --help` -> 0, `--definitely-not-an-option` -> 2, `C1_RUN_PY=/nonexistent ... --help` -> 2 (receipts `.ufo/waves/round-45/w1/R45W1RegR44C1Run/receipt.md`) | `tools/round-44/carriers.json` — the default carriers/pin file (`c1-run.py:111`), one `sha256` per carrier; evidence at `corpus/evidence/round-44/c1/` (`c1-run.py:112`) | the given evidence root (committed root only with `--data-run`/`KAIDOKU_C1_DATA_RUN=1`), plus `$HYAKU_SCRATCH/kaidoku-r44` scratch, kept only with `--keep-scratch` | kaidoku |
```

## Conformance to the frozen R45-C2 predicate

Checked against the frozen parser itself (`tools/round-45/c2-counter.py`, `parse_rows`
+ `exits_ok`):

```
parsed_rows 1
cells 7 tool tools/round-44/c1-run.sh
exits_ok True
```

So the row satisfies both clauses the counter scores for this path: first cell is the
exact backticked path, and the third cell names `0`, `1` and `2`.

## Deltas from the row landed at HEAD (`e715263c`, amended `1f4b27f8`, SKILL.md:1637)

The landed row already passes the counter (it names 0/1/2 and the exact path). These are
accuracy deltas, not a claim break; each is backed by a probe or a source line.

| # | landed cell | measured | evidence |
|---|---|---|---|
| 1 | `1` "at least one carrier failed" — nothing else | exit 1 is also produced by the harness with no carrier failing: `env -u HOME` aborts on `c1-run.sh:50` (`HOME: unbound variable`), and an uncaught Python exception propagates as 1 (e.g. `c1-run.py:841` `os.makedirs` under an unwritable `--scratch`: `FileNotFoundError`, traceback, rc 1) | probes `unset_home` rc 1, `env_abort` rc 1 |
| 2 | `0` "every carrier produced a receipt" | `--dry-run` returns 0 having written nothing and produced no receipt (`c1-run.py:952`, then `return 0`); the header's own comment (`c1-run.sh:30`) has the same gap | probe `dry_run` rc 0, stdout 22 lines, no manifest |
| 3 | `2` "usage or environment refusal (`err()` in the script header)" | `err()` is only one of several 2 arms: argparse usage error, missing lane root (`:819`), unreadable carriers (`:847`), `--carrier` matching nothing (`:853`), scope ids unknown (`:879`), committed-evidence-root refusal (`:835`) | probes `badflag` 2, `unknown_carrier` 2, `refusal_default` 2 |
| 4 | pinned value `corpus/evidence/round-44/c1/carriers.json` | no such file; the pin file is `tools/round-44/carriers.json` (`DEFAULT_CARRIERS`, `c1-run.py:111`), one `sha256` per carrier; `corpus/evidence/round-44/c1/` holds the produced receipts, not pins | `ls` fails; `git ls-tree` lists `tools/round-44/carriers.json` |
| 5 | "one REA run per carrier plus the independent oracle arm" | the runner never touches the oracle: `grep -c oracle tools/round-44/c1-run.py` prints `0` (rc 1). The oracle is `tools/round-44/c1-oracle.py`, driven by the counter; the runner only produces and publishes the evidence tree | `grep -c` rc 1; `c1-oracle.py` is a sibling, unreferenced by the runner |
| 6 | (unstated) `--freeze` | `--freeze` is recorded in the manifest/receipts and never verified: no ancestry check and no `frozen-path-preflight.py` call (`c1-run.py:784-785` help text says "recorded"; `:897`, `:965` are the only uses) | source; `pin_mismatch` manifest has `"freeze": null` |
