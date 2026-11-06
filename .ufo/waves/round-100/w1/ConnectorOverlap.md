# ConnectorOverlap — sibling-overlap and consistency scan (round 100, attempt 1)

Scope: findings only. No edits to the lane, siblings or fleet. Revisions: A2 = cbd224ef9b9d2271f415d823bdc4d1e70a0d281c (scratch clone, detached, toplevel verified). Lane main read-only at HEAD b0a7bb8ca (A2 is its ancestor; four commits ahead). Milestone: R100-C1 (UPX PE payload checksum refusal) and R100-C2 (registry self-test count truth). Supporting files: `ConnectorOverlap/sibling-and-frontier-evidence.md`, `ConnectorOverlap/registry-row-check.md`, `ConnectorOverlap/c2-selftest-at-cbd224ef.txt`, `ConnectorOverlap/probe-*.stdout`.

## Item 1 — sibling overlap

**F1. No sibling lane covers UPX PE checksum/payload refusal.** Three scans, all read-only:
- File names (`*upx*`, `*packhead*`, `*pe-*corrupt*`, `*selftest-truth*`, `*registry*selftest*`) across the 19 sibling `*-shokunin` repos, excluding `.git .ufo evidence reports waves`: no match.
- Content (`c_adler|OverlayException|PackHeader|Adler-32|adler32|upx -t|UPX!`) across the same 19 repos: matches only in `revenger-shokunin`, and only as zlib/DEX Adler-32 (`corpus/knowledge/round-64-firmware-region-byte-evidence.md:91,95,172,179,215,278-280,489`; `round-65-apk-axml-byte-evidence.md:103`; `round-67…:106`; `round-68…`). Different artifact classes; no UPX, no PackHeader, no refusal rule. Not overlap.
- Pattern `upx` in sibling tools/corpus: base64 noise and pacman logs only (`game-dev-3d-shokunin/reports/round-102/adversary/F6.md:54`). No sibling UPX tooling.

**F2. No sibling lane checks registry self-test count truth (R100-C2).** Sibling SKILL-reading registry checkers test presence or paths, not printed counts:
- `kama-shokunin/tools/gate-registry-check.py` — path existence and self-test column presence.
- `kotodama-shokunin/tools/check-gate-registry.py` — row vs instrument files.
- `mori-shokunin/tools/mori-gate-registry.py` — `no_selftest` means "no real `--selftest` argv branch" (presence, not count).
- `tameshi-shokunin/tools/registry-check.py` — its own `registry.json`, no SKILL.md.
- `tsukuroi-shokunin/tools/append-receipt.py`, `mado-shokunin`, `souji-shokunin` — no registry-count logic.

**F3. No intra-lane counter compares printed case counts to SKILL claims.** Several print their own counts and none reads a SKILL row's claimed count: `tools/round-46/registry.py:530-531`, `round-48/meanings.py:741`, `round-68/registry-conformance.py:270`, `round-71/registry-census.py:294-297`, `round-86/gate-registry.py:324`. `tools/round-99/self-assessment-audit.py` A4 checks that rows *exist* for `tools/round-97|98|99/*.py` only. So R100-C2 is not a duplicate; it is the first count-vs-printed check in the lane.

## Item 2 — frontier sites that state "payload corruption at intact length" (or equivalent) at A2

Narrow or supersede for the pinned PE set only. Lane main already adds the round-100 note at `corpus/README.md:411` and rows at `:142` and `:289`; it does not touch the sites below.

**F4. `corpus/README.md:407` (round-99 frontier note)** — "Still Frontier: payload corruption at intact length, Mach-O, …". Unchanged at HEAD. R100-C1 narrows this to: compressed-data corruption at intact length is Core for the ten pinned carriers. Pointer to `2026-11-05-r100-pe-upx-payload-checksum-refusal` recommended (append-only).

**F5. `corpus/knowledge/2026-11-05-r99-pe-upx-truncation-refusal.md:72-76` (## Limits)** — "Only truncation is decided. A pack whose bytes are corrupted but whose length is intact is not detected by this rule." Unchanged at HEAD. This is the entry R100-C1 most directly narrows. Needs a supersession pointer.

**F6. `corpus/knowledge/2026-11-05-r98-pe-upx-tamper-repair.md:73-74`** — "tool checks structure, not payload integrity. Routed." Length half routed to r99; payload half now belongs to r100. Pointer only.

**F7. `corpus/lessons/round-99.md:75`** — deferred repair list ends "payload corruption at intact length." Filed lesson: append a pointer; do not rewrite.

**F8. `PROVINCE.md` is stale for PE.** No `## Round-92` … `## Round-99` sections; the last is `## Round-91 additions to Core` at `:766` (file 770 lines). PE UPX still reads as frontier at `:717` ("big-endian and PE UPX carriers"), `:742`, `:764` ("PE carriers"), `:770` ("big-endian and PE carriers"). `corpus/README.md` calls PE Core for r98/r99. HEAD does not touch PROVINCE. L1 decision: add a round-98..100 section or state the scope limit explicitly.

**F9 (do-not-narrow).** ELF-scope "adler / p_filesize / p_blocksize" frontier items (`knowledge/2026-11-04-r88…:79-80`, `r89…:107-111`, `r90` limits, `PROVINCE.md:716,:741`, `SKILL.md:724-732`) are ELF classes. R100-C1 is PE-only. Narrowing them would over-claim. Likewise `SKILL.md:2145` (round-87 ELF repair row) stays.

## Item 3 — SKILL.md registry rows for round-100 tools

**F10. At A2: zero `tools/round-100/*.py` tool rows.** The registry block is `<!-- instrument-registry v2 -->` at `SKILL.md:1883` to `<!-- /instrument-registry -->` at `:2079`. Seven A2 mentions of round-100 are C2 corrections inside rows for rounds 46, 47, 71, 76 and 89 ("re-run by tools/round-100/registry-selftest-truth.py"). Lane HEAD adds exactly four rows (SKILL +4). Rows the L1 must add or confirm, exit maps verified against source at A2:

| tool | row sha256 = A1 = A2 blob | exit map | source check |
|---|---|---|---|
| `tools/round-100/pe-upx-corrupt-battery.py` | `8f148d33…3183` (F = A2) | 0 label; 1 other; 2 preflight | :461, :278-336 — matches |
| `tools/round-100/upx-pe-repair.py` | `15ada0b0…9a37` (absent at F) | 0 repaired/intact; 2 refusal | :217, :177, :221 — matches but see F11 |
| `tools/round-100/gen-forgeries.py` | `c3f3c425…a586` | 0 written; 1 missing anchor | :87 — missing-anchor path not re-run |
| `tools/round-100/registry-selftest-truth.py` | `496a4979…e1f4` (F = A2) | 0 label; 1 other; 2 could-not-evaluate | :288, :246-273 — matches |

Sha pins in lane HEAD rows equal the A2 blob for all four. Full detail in `ConnectorOverlap/registry-row-check.md`.

**F11. `upx-pe-repair.py` exit map omits exit 1.** The round-100 row says `0 ... 2 ...`. The round-98 row for the same family says `1=uncaught CLI error`. Probe (`python3 -I -B tools/round-100/upx-pe-repair.py --in <f> --out <f>.out --json`) on four hostile inputs (empty file, `MZ`-only, MZ+PE short section table, `e_lfanew=0x7fffffff`) gave exit 2 each, with typed JSON refusals `not-mz`, `not-mz`, `sections`, `not-pe`, and no `.out` written. Exit 1 was **not observed**; `main` catches only `(Refuse, struct.error)` around `repair()`, so [INFERENCE] an uncaught class is possible. L1: add `1=uncaught` to the row, or prove the path absent.

**F12. Nothing enforces rule 201 for round 100.** QUALITY row 201 requires a registry row per landed `tools/round-N/*.py` before filing. The round-99 self-assessment-audit A4 covers rounds 97–99 only. The four rows are therefore a manual landing duty; the L1 must check them by reading.

**F13. C2 counter self-test at A2 is green.** `python3 -I -B tools/round-100/registry-selftest-truth.py --selftest` in the scratch clone at cbd224ef → exit 0, `SELFTEST cases=22 failures=0`. Copy in `ConnectorOverlap/c2-selftest-at-cbd224ef.txt`. The registry row's case-count cell was not confirmed in this pass (row text truncated in my read); L1 should confirm it says 22.

## Consistency notes for the L1
- The frontier fix for item 2 is narrowing by pointer, not rewriting filed records (QUALITY append-only rule). F4 and F5 are the two sites a reader will hit first.
- Freeze/candidate blobs match: battery and registry-selftest blobs at F equal A2 and HEAD; gen-forgeries equals F/A1/A2/HEAD. The repair blob is absent at F (sha `e3b0c442…` = empty) as expected, since it landed at A1.

## Commands run (exit codes)
- `git clone --shared` + `git checkout --detach cbd224ef` + `rev-parse --show-toplevel` → toplevel `ConnectorOverlap/clone` (ok).
- `git merge-base --is-ancestor` for B0, F, CT, A1, A2 vs HEAD → all ancestors (ok).
- `git show <rev>:<path> | sha256sum` for four tools at F, A1, A2, HEAD → blobs as tabled.
- `python3 -I -B tools/round-100/registry-selftest-truth.py --selftest` → exit 0, `cases=22 failures=0`.
- `python3 -I -B tools/round-100/upx-pe-repair.py` × 4 hostile inputs → exit 2 each.
- Glob-verified sibling scans (19 SKILL.md, 21 knowledge dirs); no edits outside my wave directory.

## Verdict
findings: 13. No sibling overlap for R100-C1 or R100-C2. Frontier sites F4–F8 need pointers or narrowing; F8 (PROVINCE) needs an L1 decision. Four round-100 registry rows are required and present at lane main b0a7bb8ca with matching sha pins; the `upx-pe-repair` row needs exit 1 added or disproved (F11).
