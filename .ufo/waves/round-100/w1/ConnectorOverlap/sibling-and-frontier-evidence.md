# ConnectorOverlap supporting evidence (round 100, read-only)

Revisions: A2 = cbd224ef9b9d2271f415d823bdc4d1e70a0d281c (scratch clone, detached). Lane main HEAD = b0a7bb8ca (read-only `git -C` only; A2 is its ancestor).

## Sibling file-name scan
Command: `find /home/vgpnk/Projects/shokunin/*-shokunin` excluding `.git`, `.ufo`, `evidence`, `reports`, `waves`, `kaidoku-shokunin`, names matching `*upx*`, `*registry*selftest*`, `*selftest-truth*`, `*packhead*`, `*pe-*corrupt*`.
Result: no match in any of the 19 sibling repos.

## Sibling content scan (19 repos, excluding .git .ufo waves reports evidence captures __pycache__)
Pattern: `c_adler|OverlayException|PackHeader|Adler-32|adler32|upx -t|UPX!`
Result: matches only in revenger-shokunin:
- corpus/knowledge/round-64-firmware-region-byte-evidence.md:91,95,172,179,215,278-280,489 — RFC 1950 zlib stream Adler-32 trailer check on firmware members.
- corpus/knowledge/round-65-apk-axml-byte-evidence.md:103; round-67:106; round-68 (S045 header) — DEX header checksum equals Adler-32 of body.
- corpus/SOURCES.md:59 — DEX spec row.
Judgement: different artifact classes (zlib members, DEX). No UPX, no PackHeader, no refusal rule. Not an overlap for R100-C1.

Pattern `upx` (sibling tools/corpus, excluding evidence): hits only base64 noise (chousa captures, game-dev 3d vendor JS) and pacman logs in game-dev-3d reports/round-102. No sibling UPX tooling.

## Sibling registry self-test checkers (SKILL.md-reading tools)
- kama-shokunin/tools/gate-registry-check.py: row path existence, self-test column presence; `GATE_SELFTEST pass= fail=`. No count comparison.
- kotodama-shokunin/tools/check-gate-registry.py: registry rows vs instrument files; SELFTEST PASS/FAIL checks count. No printed-count comparison.
- mori-shokunin/tools/mori-gate-registry.py: `no_selftest` = tool has no real `--selftest` argv branch (presence, not count).
- tameshi-shokunin/tools/registry-check.py: own registry.json schema; no SKILL.md.
- tsukuroi-shokunin/tools/append-receipt.py, mado, souji: no registry-count logic.
Judgement: presence/path checks only. R100-C2 (count of printed `cases` vs claimed count, 93 rows) is not duplicated.

## Intra-lane counters that print case counts (none compares to SKILL claims)
- tools/round-46/registry.py:530-531 prints `REGISTRY_SELFTEST: cases=%d`.
- tools/round-48/meanings.py:741 prints `MEANINGS_SELFTEST: cases=`.
- tools/round-68/registry-conformance.py:270 prints a JSON case count.
- tools/round-71/registry-census.py:294-297 prints case map.
- tools/round-86/gate-registry.py:324 prints `SELFTEST cases=`.
- tools/round-99/self-assessment-audit.py A4 checks registry rows exist for `tools/round-97|98|99/*.py` (direct children; `controls/` and `forgeries/` excluded). Row existence only, rounds 97-99 only.

## Frontier sites that state "payload corruption at intact length" or equivalent (A2 line numbers)
1. corpus/README.md:407 — round-99 frontier note: "Still Frontier: payload corruption at intact length, Mach-O, ...". Lane HEAD: line unchanged (diff adds only rows 142, 289 and the r100 note at 411). NARROW: pinned ten PE carriers, compressed-data corruption at intact length is Core under R100-C1.
2. corpus/knowledge/2026-11-05-r99-pe-upx-truncation-refusal.md:72-76 (## Limits) — "Only truncation is decided. A pack whose bytes are corrupted but whose length is intact is not detected by this rule". Lane HEAD: file unchanged. SUPERSEDE for the pinned set by pointer to r100 entry.
3. corpus/knowledge/2026-11-05-r98-pe-upx-tamper-repair.md:73-74 — "A packed PE truncated ... ok intact ... the tool checks structure, not payload integrity. Routed." Routed to r99 for length; payload half now routed to r100. Pointer only.
4. corpus/lessons/round-99.md:75 — deferred repair item list ends "payload corruption at intact length." Filed lesson; append pointer, do not rewrite.
5. corpus/README.md:405 (round-98 note) — "truncated payloads (reported ok intact)" already superseded by README:407 (round-99). No action.
6. PROVINCE.md — no `## Round-92` .. `## Round-99` sections (last `## Round-91 additions to Core` at :766; file is 770 lines). PE UPX frontier wording at :717 ("big-endian and PE UPX carriers"), :742, :764 ("PE carriers"), :770 ("big-endian and PE carriers"). HEAD untouched. Stale for PE, which corpus/README calls Core for r98/r99.
7. SKILL.md:2145 — round-87 ELF repair row: "Any upx -t failure is a different defect (payload corruption); the repair does not reach it." ELF scope. Not narrowed by R100-C1; keep.
8. ELF "adler / p_filesize / p_blocksize" frontier (r88 knowledge:79-80; r89:107-111; r90 limits; PROVINCE:716, :741; SKILL:724-732) — ELF scope. NOT the R100-C1 class. Do not narrow with this round.

## Registry state
- A2 SKILL.md: marker block `<!-- instrument-registry v2 -->` at :1883 to `<!-- /instrument-registry -->` at :2079. Zero `tools/round-100/*.py` tool rows. Seven round-100 mentions are the C2 corrections inside rows for rounds 46, 47, 71, 76, 89 ("re-run by tools/round-100/registry-selftest-truth.py").
- Lane HEAD b0a7bb8ca adds exactly four rows (SKILL.md +4, insertions before `<!-- /instrument-registry -->`).
