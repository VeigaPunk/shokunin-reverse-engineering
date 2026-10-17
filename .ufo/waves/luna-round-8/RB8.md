# RB8 — append-only landing audit

## CLAIM
The pending landing — one new file `corpus/knowledge/2026-10-16-l8-01-6p4-symmetry-battery.md` plus two appended `corpus/README.md` rows (1 map, 1 Knowledge) — changes nothing else, keeps the prior 78 knowledge files byte-identical, and yields post-landing command A = 79/79, missing `[]`, dangling `[]`, coverage 10.0 (denominator 78→79).

## METHOD
Read-only at HEAD `6e2ee8f`; no live probes. Command A recipe verbatim (`SCORECARD.md:88-123`) at `REV=6e2ee8f`. Byte baseline from the working tree after confirming zero tracked modifications (`git diff --name-only HEAD` empty). Append-only simulation, in-memory only (no writes): current README via `git show`, placeholder rows inserted after `:67`/`:151`, target stem added to the stem set, same regex pipeline re-run. Precedent read via `git show` of `1cfd2a3 3395b6d 6e2ee8f`.

## FINDINGS
- 78 tracked knowledge `.md` (+`.gitkeep`); target file absent; zero `l8-*` files. Command A at 6e2ee8f: `{"citation_resolved_rules":9,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":78,"mapped":78,"missing":[],"rule_blocks":9}`.
- Target stem fullmatches the map-token regex `2026-10-\d{2}-[a-z0-9-]+`, no underscores. Simulation yields files 79, mapped 79, missing `[]`, dangling `[]`, coverage 10.0; all original README lines preserved byte-identical by construction and prefix check.
- Append points: line 67 (map tail — stays inside the `## Coverage map` slice the regex reads) and line 151 (Knowledge tail). Round-7 precedent: `1cfd2a3` files-only; `3395b6d` README +12 as two pure +6 tail-insert hunks, 0 deletions; records separate in `6e2ee8f` — 2 rows per entry is the standing convention.
- `git grep '2026-10-16-l7-06'` → only `corpus/README.md` references entry stems outside `knowledge/`. LOG.md:811,828 and SCORECARD.md:23,501-521 pin "78" to measured commits — untouched and still true.
- Baseline digests: 78-file sorted combined sha256 `694f8ed35bc701755040be7397a2f0d5188a4e36a14db136d657c45dd0844a97` (per-file manifest at `/tmp/rb8-knowledge-manifest.txt`); `corpus/README.md` sha256 `1cf5b7694a34db7c040f10cc63664858429b58d0eec7249cc52a35b6a1558afc`.

## THREATS
- Byte-identity holds only for tail appends. Merging the entry into an existing grouped map row, or mid-table insertion, rewrites a prior line — require the README hunks to be pure `+2` insertions.
- Simulation uses placeholder cell prose; it proves token/section arithmetic, not row content.
- AGENTS.md:4 LOG append is deferred to the parent records commit (established split); records must land or the change is unlogged.
- Parent post-landing check: `sha256sum -c /tmp/rb8-knowledge-manifest.txt` (78/78 OK) and `git show --stat <landing>` = 1 new file + README 2 insertions.

## VERDICT
CLEAN — tail-append landing is consistent as planned: baseline 78/78 measured, simulated 79/79, prior-78 digest pinned for byte-identity re-verification.
