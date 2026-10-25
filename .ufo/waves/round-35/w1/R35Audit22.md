# R35Audit22 — PROVINCE `.jsc` Frontier inspection (wave 1, read-only)

Seat: R35Audit22 (leaf auditor). Scope: inspect the `.jsc` → source mapping frontier and the two frozen claims' current-state evidence; build first falsifications. **No lane file was written except this report; no VCS mutation; source trees read-only.** All commands read immutable git objects or files.

## 1. Commands executed (read-only)

Lane root `REPO` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base `aa04633a`, HEAD `3ecf4298`, freeze rev `2323d197` (first commit adding `claims-canonical.json`; predicate byte-match verified because runs reached the check stage, exit 1 not 2).

```
python3 -I -B tools/round-35/c1-coverage-counter.py --root $REPO --rev 3ecf4298 --freeze 2323d197
python3 -I -B tools/round-35/c1-coverage-counter.py --root $REPO --rev aa04633a   --freeze 2323d197
python3 -I -B tools/round-35/c2-calibration-counter.py --root $REPO --base aa04633a --rev 3ecf4298 --freeze 2323d197
python3 -I -B tools/round-35/c2-calibration-counter.py --root $REPO --base aa04633a --rev aa04633a   --freeze 2323d197
```

### Results

| run | exit | output |
|---|---|---|
| C1 @ HEAD `3ecf4298` | 1 | `C1_FAIL: entry_missing:corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md; entry_missing:corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md; registry_row_missing:S125; registry_row_missing:S129; province_missing:2026-10-25-r35-jsc2js-mapper-contract; province_missing:2026-10-25-r35-jsc2js-release-inventory; readme_missing:corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md; readme_missing:corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md` |
| C1 @ base `aa04633a` | 1 | identical failure set (do-nothing control red, as designed) |
| C2 @ HEAD `3ecf4298` | 1 | `D1_no_sources_change_after_base; D2_lesson_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry` |
| C2 @ base `aa04633a` | 1 | `D1_census_start_missing; D2_lesson_missing; D3_source_missing; D3_verified_at_missing; D3_recheck_missing; D3_source_not_s106; D4_not_eight_cells:### Round-32 instrument registry:line1081:cells=4; D4_section_missing:### Round-34 run-6 instrument registry` (control red) |

Baseline sanity of the instrument's row parser against the live file: `ROW_RE` parses all 106 `corpus/SOURCES.md` rows (S001..S106), no duplicate ids, every status ∈ {mined, rejected} — the frozen parser works on the current format and will accept S125/S129 rows in the same shape.

## 2. Frontier inspection (claim C1 surface)

- `PROVINCE.md:147-148` holds the frontier bullet: **"`.jsc` → source mapping" — "Ignition disassembly held; a View8/jsc2js-style bytecode-to-source mapper is the next frontier for typora's real app."** Exact surface named by P35-c1.
- `corpus/README.md:224` (## Frontier) carries the same `.jsc` → source mapping bullet. `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md:145-146,152,162,187,208` holds the jsc2js/View8 prior-art context (S125/S129 will be its source rows).
- `PROVINCE.md` currently contains **no** round-35/Core-addition text (grep `Round-35|round-35|r35` = no matches), and README's coverage/knowledge tables list **no** r35 entry names → both C1 `province_missing` and `readme_missing` are live until data lands.
- Prep captures already committed at `d2729cba` under `.ufo/waves/round-35/prep/jsc-sources/`: `jsc2js-readme.md` (8,996 B), `releases-page1.json` (631,043 B), `releases-page7.json` (487,166 B) — GitHub API releases JSON for `xqy2006/jsc2js` (tags e.g. `15.6.75.19`, `12.9.202.26`). These ground the two external-source rows: S125 (README) and S129 (Releases inventory). No evidence-fetch/own-work rows are needed.

## 3. Claim C1 — first falsification traps (exact frozen-instrument contract)

Counter `tools/round-35/c1-coverage-counter.py` demands, at the measured revision:

1. Both entry files exist at `corpus/knowledge/2026-10-25-r35-jsc2js-mapper-contract.md` and `corpus/knowledge/2026-10-25-r35-jsc2js-release-inventory.md`.
2. Each entry opens with a provenance trio, each key at column 0: `^source\s*:`, `^verified-at\s*:`, `^recheck\s*:` (regex `(?m)`; a leading space or plural `sources:` fails).
3. The `source:` line must contain the literal row id on the same line: regex `(?m)^source\s*:.*S125` / `.*S129`. (Recommended shape: `source: S125 — https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md`.)
4. `corpus/SOURCES.md` rows `| S125 |` / `| S129 |` with exactly 11 `|`-cells (matches existing row shape). Cell constraints: status cell must equal exactly `mined`; opened cell must start with `2026-10-25`; used-by cell must contain the full entry path (any extra text allowed, but no `|` inside, and the row must be one physical line).
5. `PROVINCE.md` must contain the stems `2026-10-25-r35-jsc2js-mapper-contract` and `2026-10-25-r35-jsc2js-release-inventory` as substrings (a "Round-35 Core-addition table row naming both entry stems" satisfies this).
6. `corpus/README.md` must contain both full entry filenames as substrings (the "## Knowledge"/coverage-map tables satisfy this).

These six are independent; any one missing fails the claim (`C1_FAIL` with named id). Predicate identity is revalidated against `claims-canonical.json` at the freeze rev on every run.

## 4. Claim C2 — current-state evidence and falsifications (D-1..D-4)

- **D-1** — census-start receipt already committed at `d2729cba` (first round-35 commit, parent of the base's child; committed before any round-35 `corpus/SOURCES.md` change). Content verified: `rows=106`, `EXIT=0`, and 9 W04 warnings (S033, S047, S054, S062, S069, S083, S090, S092, S102). Sole current failure is `D1_no_sources_change_after_base` — SOURCES has not been touched since base yet; D-1 will pass once S125/S129 rows land (census commit is strictly earlier). No blocker.
- **D-2** — `corpus/lessons/round-35.md` does not exist at HEAD (`D2_lesson_missing`). Requires: text containing `AAdjacencyCite` and `31/32`; a line exactly `Seat accounting (round 35): spawned=<N> settled=<M> dead=<K>` where N/M/K equal the sums of `spawned/settled/dead` over `.ufo/waves/round-35/w1-settle.json` + `w2-settle.json` (these receipts must exist, be JSON objects with int fields — currently absent).
- **D-3** — `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md` exists but **lacks the appended trio**: it opens with `author:/status:/sources:/revisions:` front matter, no `source:`/`verified-at:`/`recheck:` lines at column 0, and nothing citing `S106` on a `source:` line → `D3_source_missing`, `D3_verified_at_missing`, `D3_recheck_missing`, `D3_source_not_s106`. Needs an appended trio, `source:` line containing `S106`.
- **D-4** — two concrete blockers at HEAD:
  1. `SKILL.md:1081` — the "Residual witness registry" table (`| name / kind | entry / inputs | verdict / self-invocation | pins / write scope / owner |`, 4 cells) sits under a plain paragraph at line 1079, **inside the frozen Round-32 registry scan window** (window = `### Round-32 instrument registry` at line 1064 until the next `##`/`###` heading). The frozen scanner counts it → `D4_not_eight_cells:line1081:cells=4`. Data-side fixes (either): promote the "Residual witness registry …" paragraph to a `###` heading (terminates the window before it) or convert those rows to exactly 8 cells.
  2. The frozen section match is exact text `### Round-34 run-6 instrument registry`, but `SKILL.md:1209` reads `### Round-34 run-6 instrument registry — the shortcut-replay gate (stopped capability)` → `D4_section_missing`. Also, the table under it is currently 5-column (header at line 1213: `| tool | purpose | command | exit codes | selftest |`); even after an exact heading rename, its data rows have 5 cells and would still fail the 8-cell rule — the table must be restructured so every data row has exactly 8 cells (NF=9).

## 5. Limits / notes

- `freeze-status.md` discloses the setup debt: the round-34 `freeze-integrity.py` gate fails on pin mismatch (frozen `f1ea3a6d` vs canonical pins), so the canonical freeze is a documented supersession (`claims-canonical-note.md`); counters' green/red selftests passed immediately before it. My runs used freeze rev `2323d197` (first add of `claims-canonical.json`) — predicate match confirmed by exit 1 (not 2).
- Orchestrator wave artifacts (`w1-dispatch.json`, `w1-spec.json`, `w1.ready*`, `claims-canonical-note.md`) are untracked; not scored. No seat-owned changes to production/corpus/counters/plans/claims were observed; wave-one data (entries, SOURCES rows, lesson, settle receipts, SKILL.md/PROVINCE.md/README edits) has not landed yet, so both frozen claims currently fail exactly as the controls do — no pre-data claim can pass.
- `corpus/SOURCES.md` rows parse cleanly under the frozen regex at HEAD (106/106), so adding S125/S129 in the existing row shape is safe; the only structural novelty required is the 8-cell/S-3 SKILL.md table work and the exact-heading constraints above.
- No `find`/`du` under `/fast/scratch`; no delegation/background work; no pacman installs; no lane writes other than this report.
