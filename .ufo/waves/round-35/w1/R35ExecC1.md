# R35ExecC1 — wave-1 executor report (kaidoku round 35)

Seat: `R35ExecC1` (executor) | Wave: `r35-build` | Milestone: Build evidence and first falsifications
Date: 2026-10-25 | Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`

## Item
Run cloned C1 green/red /tmp fixture; verify Git root.

## 1. Git root verification (lane)
- `git -C <lane> rev-parse --show-toplevel` → `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- HEAD `3ecf42981a0b63414de90ade643040d609dbb8a5`; status clean apart from orchestrator's untracked wave files (`w1-spec.json`, `w1-dispatch.json`, `w1.ready*`, `claims-canonical-note.md`).
- Base (canonical claims): `aa04633a686d49756763b1feed4be6830d5bb479`; freeze (first commit adding `claims-canonical.json`): `2323d197456f1328459d9420aff025cffbcb3e27`, matching committed control receipt `.ufo/waves/round-35/controls/c1-do-nothing.json` (`freeze=2323d197…`).

## 2. Cloned C1 green/red fixture (`/tmp`)
`git clone -q <lane> /tmp/r35w1-c1-fixture-20261025`

- Git root verified: `git rev-parse --show-toplevel` → `/tmp/r35w1-c1-fixture-20261025`; HEAD `3ecf4298…` == lane HEAD; `origin` → lane; `git status --porcelain=v1 --branch` → `## main...origin/main` (clean).
- Instrument pin parity: `sha256sum tools/round-35/c1-coverage-counter.py` = `e28792c7e54fcfa2185fe12f07c9e3eb328652d405e98d1ffaf2737b28d24220` == canonical `instruments` pin in `claims-canonical.json`.
- claims-canonical.json readable at freeze via `git show`: round 35, base `aa04633a` (predicate match confirmed by counter run, not exited 2).

### Selftest (green/red synthetic fixture)
```
python3 -I -B tools/round-35/c1-coverage-counter.py --root . --selftest
```
Output: `C1_SELFTEST: ok` / `green=0 red=1`; exit 0. Fully-passing green tip accepted (exit 0); provenance-trio-removal red tip rejected (exit 1).

### Do-nothing red control at base (clone)
```
python3 -I -B tools/round-35/c1-coverage-counter.py --root . \
  --rev aa04633a686d49756763b1feed4be6830d5bb479 \
  --freeze 2323d197456f1328459d9420aff025cffbcb3e27 \
  --json-out /tmp/r35w1-c1-base-red-receipt.json
```
Exit 1; `C1_FAIL` names 8 failures — identical to committed control receipt `.ufo/waves/round-35/controls/c1-do-nothing.json`: `entry_missing` (both entries), `registry_row_missing:S125/S129`, `province_missing` (both stems), `readme_missing` (both filenames).

## 3. Observations / limits
- Frozen instrument behaves as pinned: counter bytes in lane worktree and clone match canonical hash; all checks read only immutable git objects (`git show`/`ls-tree`) in the clone. No worktree/REA/source-fetch at score time.
- Receipt `checks` sub-map enumerates coarse labels and reads all-`true` even with a non-empty failing list; `pass`/exit code are governed by the failing list (exit 1 here). Behavior identical to the committed control receipt — frozen behavior, not altered.
- Known frozen-state debt (recorded in `.ufo/waves/round-35/freeze-status.md`): r34 gate pinned earlier counter bytes at the first-added claims file `13d7a815…` → `INSTRUMENT_REVISED`; canonical freeze `2323d197…` carries the final pins and the counter file hash confirms them. C1 remains un-scored until claim data lands; this seat writes no data.
- No lane production file/corpus/VCS mutated; only the `/tmp` clone and `/tmp/r35w1-c1-base-red-receipt.json` were created. No installs needed (Pacman paused; none run).

## Files changed
- `.ufo/waves/round-35/w1/R35ExecC1.md` (this report) — the only lane write.
