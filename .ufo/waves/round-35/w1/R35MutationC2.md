# R35MutationC2 — C2 mutation probe (wave one, round 35)

Seat: `R35MutationC2` (leaf; no subagents, no background work). Scratch: `/tmp/r35c2-mutprobe/` only.
Lane production files, counters, VCS state untouched; sole lane write is this report.

## Claimed invariant probed (C2 / D-1)

`plans/round-35-claims.md` Claim C2, D-1: the census-start receipt
`.ufo/waves/round-35/assimilation/census-start.txt` is "committed **no later than** the first
commit that changes `corpus/SOURCES.md` after the base".

`tools/round-35/c2-calibration-counter.py` (frozen, sha256
`576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94` — matches
`.ufo/waves/round-35/claims-canonical.json` instruments pin; re-verified unchanged after the
probe) implements this as a **committer-date comparison**, not ancestry:

```
ct = git log --format=%cI -1 rev -- <census>      # census commit time
fc = git log --format=%cI base..rev -- corpus/SOURCES.md; lines[-1]  # oldest by date
D-1 fails only if parse_iso(ct) > parse_iso(fc)
```

## Mutant (one plausible defect, smallest behavior-bearing point)

Fixture-repo state in `/tmp/r35c2-mutprobe/fx` (all four D-checks otherwise satisfiable,
mirroring the counter's own selftest green state): the census receipt commit is placed
**topologically after** the first post-base `corpus/SOURCES.md` change, with its author and
committer dates backdated (`GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` = 10:00Z) before the
SOURCES commit (11:00Z). Invariant violated in ancestry terms; counter sees `ct=10:00 <= fc=11:00`.

Generator: `/tmp/r35c2-mutprobe/gen.py` (modes `pristine` / `mutant` / `honestlate`).
Detector (identical, bounded): `python3 -I -B tools/round-35/c2-calibration-counter.py --root <fx> --base <base> --rev <rev> --freeze <base>`.

## Expected detector outputs

- pristine → exit 0 `C2_CLEAN` (baseline; a baseline failure would be inconclusive)
- mutant → exit 1 `C2_FAIL: D1_census_after_first_sources_change` (killed) if the counter
  really enforced "committed no later than"
- honest-late control (same topology, honest dates) → exit 1 (proves the check bites at all)
- restored pristine bytes → exit 0, identical HEAD/tree SHAs

## Actual outputs

- Instrument baseline: `C2_SELFTEST: ok` / `green=0 red=1`.
- Pristine: `C2_CLEAN revision=1475cc49274530599ffb2f177e033e4ae6e1a3a9`, rc=0
  (HEAD tree `4373f6c519e9f4c121febc4f5f2722c08755c287`, `git ls-tree -r HEAD | sha256sum`
  = `438c1562b4af7493f3d49309f4a695ef9e41a1482f7d18997edd8faf746e33cd`).
- Mutant history (real):
  `cf0dbd2 2026-10-25T10:00:00Z census-start BACKDATED after sources change` ← child of
  `0b48a8c 2026-10-25T11:00:00Z sources s130 FIRST` ← `32ed3af … base`.
  Detector: `C2_CLEAN revision=cf0dbd24e4e2e265a9d0635075be639970278e3f`, **rc=0**.
- Honest-late control: `C2_FAIL: D1_census_after_first_sources_change`, rc=1.
- Restored: rebuilt pristine at same path; HEAD `1475cc49…`, tree `4373f6c5…`, ls-tree
  sha256 `438c1562…` — all identical to pre-mutation baseline; detector `C2_CLEAN`, rc=0.
- Counter bytes before/after: `576c14dd95c0a54b2de05b765d171b25429a893289b85516258e83daa9179b94` (unchanged).

## Verdict

**SURVIVED** (coverage finding, not a contract change). The frozen counter accepts a D-1
state where the census receipt is committed after the round's first `corpus/SOURCES.md`
change, because D-1 tests forgeable/rewritable committer dates (`%cI`) instead of commit
ancestry. The committed selftest cannot catch a code-level analog either: its only red
fixture exercises D-2 (`green=0 red=1`), so no red case pins D-1 ordering semantics — today
the canonical hash pin is the sole guard of that behavior. Advisory only: an
`git merge-base --is-ancestor` (or topology-order) check would match the predicate wording.
No instrument, predicate, scope, or claim file was modified.

## Limits

- /tmp fixture proxies the lane topology; lane git history itself was not mutated or rewritten.
- Counter reads fixture via the same `git show`/`git log` code paths as it would on the lane repo.
- Probe run before C2 data scoring; result is advisory evidence for the wave, not a score.
- `find`/`du` avoided everywhere; no installs performed.
