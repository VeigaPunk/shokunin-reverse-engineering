# C1NewRows — scoped findings

## Behavior and gates
Read `plans/round-48-claims.md` in full before running any command. Observed declared freeze `dc73587a8b9c1a23ba5a91dc7707ac7381a8b873`; the read-only `git rev-parse` returned the same hash. Read both frozen tool headers and both `--help` outputs. `meanings.py --help` exited 0 and describes C1 meaning-class verdict maps, per-routed-id arm binding, mutation digest, interpreter pin, census derivation, and exit semantics 0 met / 1 not met / 2 could-not-evaluate. `record2.py --help` exited 0 and describes committed-byte oracle execution, completeness floor, correction checks, receipt binding, score-cell binding, and the same exit semantics. Both advertise `--selftest`; self-test commands were not run. No counter run/battery/forgery fixture was performed; no claim gate is asserted passed.

The required disk guard command `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` ran and returned its disk table (scratch space available was shown). No tooling was installed. Initial lane status showed unrelated existing dirty/untracked files including `tools/round-48/meanings.py`; this seat did not alter any lane product or frozen path.

## Touched surfaces
Created only `.ufo/waves/round-48/w1/C1NewRows.md` and `.ufo/waves/round-48/w1/C1NewRows/rows.md`. No product, frozen, sibling-lane, state, watchdog, scratch, or fleet files were edited by this seat. No git mutation was run.

## Findings and limits
The requested seven-cell row drafts are in `C1NewRows/rows.md`, with counter-specific scope, meaning-bound verdict requirements, help-indicated self-test command, pin path, write scope and owner. Help is interface evidence only: the self-tests and frozen counter behavior were not executed. Exact stdout hashes/UTC timestamps were not captured for these commands, so they are not presented as complete receipts. The failed attempt `git -C <lane> show <freeze>:tools/round-48/meanings.py --help` was a malformed Git invocation (Git printed usage); it does not constitute helper execution. No finding about counter pass/fail or forgery resistance is made.

## Artifacts
- Report: `.ufo/waves/round-48/w1/C1NewRows.md`
- Draft rows: `.ufo/waves/round-48/w1/C1NewRows/rows.md`
- Receipts: none (help command stdout was observed but not captured as receipt with required hash/time fields).
