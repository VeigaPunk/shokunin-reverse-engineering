# R35Audit41 — sasquatch alternative-theme comparison

## Finding
**Counterexample:** the sasquatch/unblob theme is not simply “unblob needs an unavailable AUR tool, therefore the frontier is blocked.” The existing evidence already establishes a useful two-stage path: unblob identifies and preserves the SquashFS bytes and 7z independently opens the carved image. This means the operational gap is specifically *automatic in-process recursion / tree publication by `extract-firmware`*, not identification, carving, or all access to contents. Any alternative-theme claim phrased as “cannot extract SquashFS without sasquatch” would be falsified by the lane’s own 7z observation.

## Evidence (read-only)
- `corpus/knowledge/2026-10-13-r4u-03-unblob-extract.md:91-133,157-158,173-183`: AppImage SquashFS starts at offset 188392; unblob preserved the 127.53 MB chunk and produced typed `ExtractorDependencyNotFoundReport` for dependency `sasquatch`; 7z listed `.DirIcon` from the standalone chunk. Entry explicitly distinguishes this verified carve-then-7z route from native unblob recursion.
- Same entry `:159-163`: identical inputs yielded different `evidence_id`s; IDs are run-scoped, not content-stable. A new run cannot be attributed merely by matching an old ID.
- `corpus/README.md:44,162,227` and `PROVINCE.md:147-148`: current summary still records sasquatch as missing/AUR-only and 7z fallback as covering the carved-image path. This supports the narrower residual frontier, not a general inability to inspect SquashFS.
- The actual current lane has no `merge/kaidoku/` directory (glob returned path not found); therefore I found no candidate sasquatch source entries in that requested source location. This is absence evidence only, not proof no sources exist elsewhere.
- Frozen round-35 plan explicitly selects `.jsc -> source mapping` rather than sasquatch because its candidates cite external sources (S125/S129); sasquatch is an alternative theme, not a permitted change to frozen C1/C2.

## Impacted axes / claim boundary
Potentially **coverage** if a future claim measures whether `extract-firmware` recursively publishes SquashFS contents. The extant evidence does not demonstrate that capability; it demonstrates carve-plus-independent-reader. It does not directly establish depth or calibration improvement. Do not count the fallback as native recursive extraction or as a fresh/current host capability observation.

## Smallest safe correction
For any sasquatch follow-on, narrow the claim to the exact delta: *with sasquatch available, does unblob recurse and publish the same pinned AppImage’s SquashFS tree that the established 7z fallback can read?* Preserve the old known-good carve/7z control and compare tree/content outputs, not run-scoped evidence IDs. Treat install availability as prerequisite and keep the existing 7z route as an explicit comparator; no change to round-35 frozen predicates.

## Commands and limits
Read-only commands used: `grep -n` against lane `corpus/SOURCES.md`, `corpus/README.md`, `PROVINCE.md`; `sed -n '138,160p' PROVINCE.md`; `ls` for knowledge-entry existence; `git status --porcelain` and `git log --oneline -8`. Read relevant knowledge entry, README, freeze status, claims and wave spec through file reads. No install, REA run, source fetch, VCS mutation, `/fast/scratch` access, or production edit. `S125`/`S129` rows and both C1 entries are not present in the current worktree at this observation; `corpus/SOURCES.md` ends at 106 and the C1 entry files were absent. Worktree showed only untracked orchestration files before this report; do not infer them as authored by this seat.
