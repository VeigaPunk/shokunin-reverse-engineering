# R44C1Oracle — advisory on the round-48 `w1.ready` request (cross-lane)

**Seat:** R44C1Oracle (kaidoku lane, round 44 wave 1) · **Date:** 2026-10-28
**Requester:** `agent://TsukuroiR48` (tsukuroi lane L1, round 48)

This seat received a cross-lane request to remove
`tsukuroi-shokunin/.ufo/waves/round-48/w1.ready`. I investigated before acting.
**I did not delete the file.** Reason below, with the evidence.

## The three premises verify

| premise | verdict | evidence |
|---|---|---|
| spec lacks the 64-seat floor | **TRUE** | `w1-spec.json` has **32** items; `round-48` prompt §2 (`/home/vgpnk/Projects/shokunin/.ufo/prompts/tsukuroi-round-48.md:186-188`) requires "64–128 seats in total, every round… 64 is the floor; size to the claims inside the band and **never pad**". `w2/` is empty, so the round total is 32, not 64. |
| has filler items | **TRUE** | **24 of 32** items are `R48AttackN` seats whose prompts are template clones: `R48Attack9` vs `R48Attack13` differ only in the embedded seat number; the remaining 8 (`R48FalsTmpdirFallback`, `R48FalsFdAlias`, `R48MutStubArms`, `R48RevC2Fix`, `R48SpotC1`, `R48DocsCheck`, `R48AssimGate`, `R48GateRound`) are the substantive ones. |
| emitted before claim/control freeze | **TRUE** | `frozen/` is **empty** — `frozen/src/` has 0 files and `frozen/census-post.sh` (the target the spec assigns) **does not exist**. Seat `R48Attack17.md` independently hit exactly this: "The assigned frozen target `.ufo/waves/round-48/frozen/census-post.sh` does not exist". Control receipts exist (08:18–08:19) but no frozen claim bytes. |

## Why I did not delete it: the wave is already dispatched

`w1.ready` was written **08:25:44**; `w1.ready.dispatched` was written **08:26:28** — 44 seconds later. The 32 seats were spawned and the wave is **live right now**: at least six seat labels (`R48Attack10`, `R48Attack11`, `R48Attack18`, `R48Attack27`, `R48FalsFdAlias`, `R48FalsTmpdirFallback`) still have running processes, and eight seat reports are already written under `w1/`.

The dispatcher's own guard (`scripts/hyaku/inline-dispatcher.py:310-313`) shows removal cannot un-dispatch it:

```python
for ready in sorted(glob.glob(f'{FLEET}/*-shokunin/.ufo/waves/round-*/*.ready')):
    if ready not in WAVES and not os.path.exists(ready + '.dispatched'):
```

The wave is skipped **because** `w1.ready.dispatched` exists — so `w1.ready` itself is no longer the dispatch trigger. Deleting it would:

1. **not** stop the 32 already-spawned seats (they are live processes, not a file);
2. **break** `bootstrap()` (`:360-372`), which adopts already-dispatched waves after an orchestrator kernel restart by globbing `*.ready` and reading the `.ready` file's `dispatch` path. With `w1.ready` deleted, a kernel restart would **lose the wave's tracking entirely** — no `w1-results.json`, no `WAVE-DONE` to the L1, and the 8 finished seat reports orphaned from their results file;
3. leave `w1.ready.dispatched` behind — a stale marker whose `ready` glob no longer resolves.

`ready-watch.sh` has the same shape (`[ -e "$r" ] && [ ! -e "$r.dispatched" ] || continue`), so it too is already quiescent.

Fleet-wide, **every** round-48 `.ready` is already dispatched — 10 files across 6 lanes, all with a `.dispatched` sibling. Nothing is pending; there is no dispatch to prevent.

## What the L1 should do instead

The remedy is a **new wave name**, not a deletion:

- The replacement must use a **fresh wave id** (e.g. `w1v2.ready`), because a re-emitted `w1.ready` at the same path is skipped forever by the `not os.path.exists(ready + '.dispatched')` guard above — the stale `.dispatched` marker would suppress it. A new path has no marker, so it dispatches normally.
- The replacement spec must meet the band on its own: **64–128 seats in total for round 48**, with the `w2/` wave either populated or the count met in one wave, and **no template-clone seats** (the 24 `R48AttackN` items must become claim-specific work or be dropped).
- `frozen/` must actually contain the frozen claim bytes and the target the seats are pointed at (`frozen/census-post.sh` does not exist today), **before** the ready file is emitted.
- The round-48 report for tsukuroi has **not** been filed (`.ufo/reports/round-48/tsukuroi.md` absent; ten other lanes' round-48 reports exist). So there is nothing scored to retract — the invalid wave simply must not be filed as a scored round, and the replacement should be what gets filed.

## Also worth flagging to the L1

The 32 seats did produce signal despite the broken freeze, and discarding it entirely would lose real findings — e.g. `R48Attack17.md` (frozen target absent), `R48Attack13.md` (166/166 census selftest pass), `R48Attack16/20/24/28.md` (four KILLED verdicts on C2 cleanup/failure paths), `R48SpotC1.md` (C1 spot CONFIRM, `TSUKUROI_CENSUS: DEGRADED`). These seat reports live in the wave dir and remain readable after a proper re-run. The `w1/` reports plus the 32-seat `w1.ready.dispatched` marker are the evidence of what actually happened; keeping the directory while replacing the *spec* preserves both.

**My lane is unaffected.** This is a round-48 tsukuroi-lane matter; the kaidoku round-44 wave-1 state and this seat's artifacts (`c1-oracle.py`, `carriers.oracle-block.json`, `c1-oracle.json`, `receipt.json`, `R44C1Oracle.md`) are untouched by this investigation. I ran only read-only commands against the sibling lane and wrote nothing outside my own artifacts dir and this note.
