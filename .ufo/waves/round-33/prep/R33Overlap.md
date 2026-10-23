# R33Overlap — CHPE structure validation / map bounds / forged tags sweep

- **Seat:** `KaidokuR33.R33Overlap` (UFO-FSD connector)
- **Base:** `428315a8f5674b952def862910af6e07a6c2224b` (round-32 verifier spot-check), measured 2026-10-23T08:10:11Z
- **Scope:** read-only lane production; no git/jj writes; no SKILL/PROVINCE/LOG edits
- **Inputs:** prep contract `.ufo/waves/round-33/prep-contract.txt`; prior defect `corpus/lessons/round-32-verifier-spotcheck.md:117` ("metadata-only hybrid classifier accepts forged tags")

## 1. Bounded sweep

Command (run from repo root, output captured at `/fast/scratch/hyaku/kaidoku-r33/R33Overlap/sweep.txt`, exit 0):

```sh
git show -s --format='%H %cI %s' HEAD
grep -nE "CHPE|ARM64X|ARM64EC|forged" README.md SKILL.md PROVINCE.md LOG.md corpus/knowledge/*.md
grep -nE "map bound|structure valid|code[- ]map|malformed" SKILL.md PROVINCE.md README.md
```

Observed (bounded excerpt):

- `SKILL.md:1050` `## ARM64X hybrid PE — round 32 native-view boundary`; decision table at `:1054-1060` covers only: raw COFF machine 0xAA64 is insufficient; declared ARM64+ARM64EC ranges exercise REA native view; EC view not recoverable from native counts; internal/published/runtime untested. No row validates map bounds, section containment, overlap, tag legality, or malformed metadata.
- `SKILL.md:1075` retains S100 rejection for CHPE offset/tag authority only.
- `PROVINCE.md:82,357` Core row names "raw COFF 0xAA64 plus CHPE ARM64/ARM64EC ranges"; no structural-validation clause.
- `corpus/knowledge/2026-10-23-r32-arm64x-hybrid-pe.md:34-35` states classify is structural classification over declared ranges, "not proof of Windows loader validity or execution"; limits note no section with VirtualSize > SizeOfRawData tested.
- `corpus/lessons/round-32-verifier-spotcheck.md:117` is the only "forged tags" hit in tracked knowledge; it is an open defect, not a rule/table.
- `tools/round-32/arm64x_oracle.py` `classify()` (`:104-109`) requires machine 0xAA64 plus at least one ARM64 and one ARM64EC range; `code_map()` (`:79-96`) reads tag/length with no bounds, containment, overlap, or tag-range checks. `independent-pe/pe_indep.py` reads the same fields and validates file offsets only, not range/section containment.
- Sweep for "forged tags" across the repo: single hit (spotcheck line 117). Sweep for "map bound/structure valid/malformed metadata": none in SKILL/PROVINCE/README; only generic malformed-JSON/ELF rows.

Exit codes: grep 0 for first pattern set (matches found), 1 for the second targeted "map bound/…" set in SKILL/PROVINCE/README (no matches) — confirming the absence below.

## 2. Rule/table absent at base

Absent at base: any CHPE structural-validation / map-bounds / forged-tag rule or table in tracked knowledge, README, SKILL, PROVINCE, or wave/LOG. The only related text is the round-32 caveat that classify is metadata-only and the open defect that the classifier accepts forged tags. `arm64x_oracle.classify` accepts a pure-ARM64 file with hand-written, structurally well-formed CHPE metadata (A2CHPEBits §4).

## 3. Is this actual new technical depth or only retest?

**Verdict: bounded new technical depth, not a retest — but only for malformed-structural-metadata rejection.** It is not merely re-running classify over the same twelve carriers; it adds checks that do not exist at base (range containment in sections, tag legality {0,1,2}, non-zero/non-overflow lengths, count sanity, pointer containment, overlap/disjointness). Those checks can reject malformed metadata that currently passes.

It is **not** new depth against forged tags in the strong sense: a tag that is structurally well-formed but semantically false (e.g. an ARM64 range tagged ARM64EC, as A2CHPEBits probe B2) cannot be detected by structure alone, because the tag is the only type carrier and no instruction bytes are read. Therefore the move must be scoped as "separates valid mapped mixed-code ranges from malformed metadata," with forged-but-structurally-valid tags explicitly retained as a residual/Frontier item. Selling it as forgery immunity would overclaim and harm calibration.

Affected axes: **depth** (primary, new decision table + runnable parser); **operability** (if a selftest with malformed cases lands); **calibration** (must name the residual forgery limit honestly). Coverage unchanged by contract. Adjacency: PE format-level authority belongs to revenger (sibling overlap audit); kaidoku must not absorb build-tool or PE-format maintenance — report contested scope rather than absorbing it.

## 4. Proposed move

Add one bounded CHPE structural decision table to `SKILL.md` (round-33 section) plus a read-only parser (new `tools/round-33/` script, not an edit to the round-32 oracle) that, for a candidate DLL, validates and reports:

1. MZ + `PE\0\0`, PE32+ magic 0x20B, machine 0xAA64.
2. Load config present, size >= 0xD0, `CHPEMetadataPointer` non-zero and section-contained.
3. Metadata `CodeMap RVA`/count within a section; count bounded (e.g. <= 1024 and <= section capacity).
4. Each range: tag in {0,1,2}; `start & ~3` + length within the containing section's virtual size; length > 0; no overflow; ranges non-overlapping (or at least no duplicate/overflow).
5. At least one ARM64 and one ARM64EC range for "hybrid-declared" classification.

Explicitly state what it does **not** prove: instruction/ABI decoding, Windows loader acceptance, execution, or detection of structurally well-formed forged tags. Keep scope to round-32 synthetic exported-leaf DLLs; no published hybrids; no coverage widening.

Selftest (`--selftest`) with CLEAN plus malformed cases: bad magic, machine != 0xAA64, missing/zero CHPE pointer, pointer outside sections, invalid tag 3, zero length, range past section end, overlapping ranges, count overflow, count 0. Do not mutate the round-32 oracle or carriers.

## 5. Risks

- Overclaim: structural validity can be mistaken for forgery immunity (A2CHPEBits §4). Mitigation: decision table names the residual explicitly.
- Adjacency: CHPE metadata is PE-format territory (revenger); kaidoku owns reader-coverage only. Keep parser as a read-only oracle, not format authority.
- False confidence from synthetic-only carriers (12 leaf DLLs, one LLVM release); no published hybrid exercised.
- Selftest gaps: a parser can pass its own malformed cases yet miss others; inherited conformance limitation (no separate selftest credit) unless added.
- Tool maintenance: new script must be pinned and freeze-integrity checked if used in a claim.

## 6. Verification (to be run by main agent, not this seat)

- `python3 -I -B tools/round-33/<parser>.py --selftest` → 0 (CLEAN + malformed cases).
- Re-run on the 12 pinned carriers: all must classify as before (no regression of the round-32 predicate).
- Re-run forged fixture from A2CHPEBits §4: must still classify structurally valid (documenting the residual), not silently change behavior.
- `tools/round-32/freeze-integrity.py --round 32 --claims ...` unaffected (no round-32 edits).
- No builds/tests/formatters beyond the assigned bounded selftest.

## Limitations

- No code was written by this seat (leaf, read-only production). No REA/Ghidra run. No published hybrid inspected. Sweep was grep-based over tracked text only; interactive-session transcripts and venv files were excluded by construction. Base pinned at `428315a8`.

Trailer: `.ufo/waves/round-33/prep/R33Overlap.md`
## Correction (appended after peer review; no rewrite of above)

- **Sweep scope correction.** The bounded sweep in §1 searched only `README.md`, `SKILL.md`, `PROVINCE.md`, `LOG.md`, `corpus/knowledge/*.md`, and `tools/round-32/*` in the worktree. It did **not** search `.ufo/waves/*` or interactive-session transcripts. The absence claim in §2 is therefore narrowed to those explicitly searched files, not to all tracked paths.
- **Immutable-base pin.** `git grep -n -I -E "CHPE|ARM64X|ARM64EC|forged|map bound|structure valid|code[- ]map|malformed metadata" 428315a8 -- README.md SKILL.md PROVINCE.md LOG.md 'corpus/knowledge/*' 'tools/round-32/*'` returns 45 matches across 131 tracked paths in scope (exit 0). `git grep -l -I "forged" 428315a8 -- README.md SKILL.md PROVINCE.md LOG.md 'corpus/knowledge/*' 'tools/round-32/*'` returns only `SKILL.md` and `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`. No CHPE structural-validation/map-bounds/forged-tag rule or table exists in those scoped files at base.
- **No selftests run.** This seat ran no builds, tests, formatters, or selftests. Items listed in §6 are recommendations for the main agent; the only command this seat executed was the grep/git-grep sweep and `git show`/`rev-parse` reads. No production writes were made.

Trailer: `.ufo/waves/round-33/prep/R33Overlap.md`
