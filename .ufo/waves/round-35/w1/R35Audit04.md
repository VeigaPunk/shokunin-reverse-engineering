# R35Audit04 — jsc2js duplication scan (wave 1)

Seat: R35Audit04 (executor). Item: "Search lane corpus for jsc2js duplication."

 Read-only / private /tmp only. **No lane file was written or modified by this seat; no VCS mutation.** The only file this seat creates is this report.

Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (HEAD `3ecf42981a0b63414de90ade643040d609dbb8a5`; base `aa04633a686d49756763b1feed4be6830d5bb479`).

## 0. Verification commands (all read-only)

```
grep -rn "jsc2js" corpus/ 2>/dev/null | cut -d: -f1 | sort -u
grep -c "jsc2js" corpus/SOURCES.md          # 0
ls -d considerthese                          # exit 2 — does not exist (plan's required line)
glob 'corpus/knowledge/*r35*'                # no files — planned C1 entries do not exist yet
git status --porcelain=v1 -- . ':!/.ufo/waves/round-35/w1'   # only dispatcher's untracked files; none mine
python3 -c '...' prep/jsc-sources/releases-{page1,page7}.json  # release inventory stats
```

Limits: gitignore=true greps; no `find`/`du` under `/fast/scratch`; no background work; no pacman.

## 1. Corpus inventory of jsc2js mentions

| Location | What it says |
|---|---|
| `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` | **Only knowledge entry mentioning jsc2js** (122 knowledge files). Four spots: L145-146 residual gap (`jsc2js's patched-d8 loadjsc() walk (xqy2006/jsc2js: disasm text → View8 → approximate JS)`), L152 frontier path #1 (`jsc2js/View8 (github xqy2006/jsc2js; disasm→JS approx)`), L162 path #4 (`jsc2js patched-d8 releases (need a V8-14.8 build)`), L208 summary (`feeding a View8/jsc2js-style text mapper`). Already records the two-part architecture, disasm-text intermediate, approximation bounds, version-matching requirement — from the lane's own r4 probe, without citing the README. |
| `PROVINCE.md` L147-148 | Frontier bullet (C1's named surface): "`.jsc` → source mapping — Ignition disassembly held; a View8/jsc2js-style bytecode-to-source mapper is the next frontier for typora's real app." Also capability-table row `.jsc` V8 bytecode (L129). |
| `corpus/README.md` L224 | Mirrored copy of the same frontier bullet; coverage-map rows already list r4-07 under Electron/ASAR/JS (L23-24). |
| `SKILL.md` L56 | Capability-table row `.jsc` V8 bytecode held r4; **no** `jsc2js`/`View8` string in SKILL.md. |
| `corpus/lessons/round-4.md` | `.jsc` decompilation-adjacent recipe; "Source mapping remains frontier" — does not name jsc2js. |
| `corpus/lessons/round-13.md`, `round-14-verifier-spotcheck.md`, `round-14.md` | Quote/verification rows for S017 (upstream View8) and S018 (Check Point JSCeal); no jsc2js row. |
| `.ufo/waves/arc3-loop1-round1/…`, `c3/…` etc. | ~49+ archived copies of the same frontier bullet text in historical wave artifacts (README.before/after, PROVINCE scratch copies). Archived, not live production docs. |

## 2. Source-registry adjacency (SOURCES.md)

- Registry ends at **S106** (106 rows = base census count). `grep jsc2js corpus/SOURCES.md` = **0 matches** → no pre-existing row, no URI collision for S125/S129.
- Closest existing rows (none duplicates): **S017** = upstream `suleram/View8` pinned at commit `ef39099b…`; **S018** = Check Point JSCeal static pipeline; **S022** = JSC Decompiler (rejected); **S016** = V8 heap-snapshot tampering. jsc2js (`xqy2006/jsc2js`) is a different repo whose View8 is a **customised fork** of S017's upstream — S125 contract facts must not be attributed to S017's pinned upstream commit.
- SOURCES.md "Not opened" list already names the family: "A version-matched `.jsc` route for Electron 42 / V8 14.8, including current `jscd`/View8-family work: this round opened View8 and the Check Point case study, neither of which establishes that version combination." S125/S129 are consistent successors; no stale row promises them.

## 3. Planned C1 entries vs existing content

- `2026-10-25-r35-jsc2js-mapper-contract.md` (S125): content will necessarily restate facts already in r4-07 (d8+View8 two-part architecture, disasm-text intermediate, approximate reconstruction, version matching). This is **thematic continuity, not literal duplication**: r4-07 wrote its version from the host probe with no README citation, and C1's frontier is precisely this bullet. Advisory: the new entry should cross-reference r4-07 (host-side probe) and S017 (upstream View8) to avoid two unlinked descriptions of the same tool; anything about the integrated fork must stay scoped to the fork, not S017's commit.
- `2026-10-25-r35-jsc2js-release-inventory.md` (S129): **no existing counterpart anywhere** in the corpus. No file inventories jsc2js releases/d8 binaries/asset shape/version bounds. Genuinely novel content.
- The two planned entries have **distinct scopes** (tool contract vs release inventory) and **distinct sources** (README vs GitHub Releases API) — no self-duplication.
- No draft of either slug exists anywhere in the lane (grep hits are only the predicate/counter/claim texts).

## 4. Prep captures (S125/S129 raw material)

`.ufo/waves/round-35/prep/jsc-sources/`:
- `jsc2js-readme.md` — README capture (S125 source).
- `releases-page1.json` — GitHub Releases API list, **100 releases**, tags `15.6.75.19` → `11.1.111`; each has 2 assets: `d8-<ver>-linux.tar.gz` + `d8-<ver>-windows.zip`.
- `releases-page7.json` — **77 releases**, tags `12.9.202.26` → `12.0.157`; same 2-asset shape.
- Total captured ≥177 releases; among captured pages **no V8 14.8.x tag** (page1 has `15.3.53`). README states patch coverage V8 5.1–15.3.25 with the 14.7.84–15.3.25 modern compatibility layer.

## 5. Verdict

- **No literal duplication of jsc2js documentation exists** in the corpus: only r4-07 + the frontier bullet (live copies: PROVINCE.md, corpus/README.md — exactly the two C1 targets, so consistency, not duplication).
- **S125/S129 are new, non-colliding rows** (registry ends S106; URI grep = 0); the two entries do not duplicate each other.
- **Overlap risk (advisory, not a frozen-check failure):** mapper-contract will overlap r4-07's architecture facts and S017's View8 subject unless it cross-references both and scopes the fork facts; the counter does not test this (it checks trio + row citation + PROVINCE/READMEME presence), so this is a corpus-quality recommendation for the writer seat.
- No frozen C1/C2 check is falsified by these findings.
- `considerthese/` does not exist in this lane (verified, plan-required line).

## 6. Risks / notes

- Multi-seat overlap: peer seats (R35Audit08, R35Audit24, R35ReconJscRows) are already auditing the same counter/rows; R35Audit24 independently confirms no duplicate SOURCES URI. No conflicts with this report.
- The report trailer `.ufo/waves/round-35/w1/R35Audit04.md` is the only lane write by this seat (unique path, verified absent before writing).
