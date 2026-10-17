## CLAIM
VB4 (2nd opinion, no Lane-A reading first): independently verify the two README stale-content claims — targets relocated to `corpus/README.md:131` and `:163` at HEAD `cfc84c2` (Lane-A P0), drifted from inherited pointers `:128`/`:160`.

## METHOD
Primary sources only while drafting: `git show HEAD:corpus/README.md | grep -n` (HEAD = cfc84c2; README last changed at 6a71cd5, unchanged after); rev-loop over c265db9…cfc84c2 for the two target strings; SCORECARD.md:68-72; LOG.md:385-401; knowledge files r5-02 (`:18,53`), r9-02 (header), r11-01 (`:3,185,316-317`), r4-16 (`:160,262`). `git status --porcelain` → only untracked `.ufo/` paths; no tracked file touched. No live probes.

## FINDINGS
1. Positions exact at HEAD: `:131` = `lessons/round-13-distillation` row ending `SKILL.md:81-195; verify-lane VERIFIED, 4 nits fixed`; `:163` = Frontier bullet ``Runtime-obs extended: process-capture, managed `verify`/`project` ops, native call-target resolution (per r4-16 rescan: ~26 self-provisionable)``. P0's corrected `:131,:163` confirmed.
2. Drift confirmed: SCORECARD.md:68-70 still cites `:160`/`:128`, which match the round-1-era README (a3f2e1b: row at :128, bullet at :160). Post-drift positions by 6a71cd5 are `:131`/`:163` (+3 lines).
3. `:131` staleness confirmed: "4 nits fixed" is unsupported. LOG.md:395-401 (round-13 tail correction) records only 2 fixes at integration (r9-02 anchor range; heading scope) + 1 pre-land self-correction (r10-02 anchor) + 1 accepted (LOG.md:389-391). P0's replacement enumeration matches LOG.md:395-401.
4. `:163` staleness confirmed: all three listed families are held — `capture-process` exercised (r11-01:316-317, exit 0, controlled-replay/observed), managed verify/project exercised (r9-02 header on Pinta), call targets probed (r5-02:18 census 286 GOT-indirect; `:53` 3/3 resolved). README:47,53,125 record the same. The quoted "~26 self-provisionable" is r4-16:262's pre-drain census.

## THREATS
Textual verification only; no live re-runs (independence rule honored — P0 read only after the primary-source draft). `:131` staleness rests on the LOG tail correction being the authoritative recount; the line positions themselves are mechanical and exact — verified by `grep -n` on `git show HEAD:corpus/README.md`. Anything beyond these two sites was out of scope.

## VERDICT
CLEAN — both stale-content claims verified at HEAD cfc84c2; P0's `:131/:163` relocation and the SCORECARD `:128/:160` drift are exact.
