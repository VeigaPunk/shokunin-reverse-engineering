# SkillStalePins — REA version / tool-count sweep (round 19, wave 1)

- **Seat:** `KaidokuR19.SkillStalePins`, read-only advisory. No subagents, no lane writes beyond this report.
- **Baseline:** `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (B). Lane `HEAD` = `refs/heads/main` = `85589ac757f9ca3cb25efcd702d0963e25c9c4df` at my read; `git diff --name-only B HEAD -- SKILL.md PROVINCE.md corpus/README.md corpus/QUALITY.md` printed nothing (exit 0), so every anchor below is identical at B and at HEAD.
- **Live pin truth (task premise, re-observed):** all three clients resolve `rea-agents@6.7.0` — Devin `~/.config/devin/mcp_config.json:7`, OMP `~/.omp/agent/mcp.json:8`, Kimi `~/.kimi-code/config.toml:4126`.
- **Classification used:** `current` = describes live state and matches it; `historical-labelled` = describes a past run/observation and carries a historical marker (the word "historical", a date, a round/section, or a DATED scope row); `stale-unlabelled` = present-tense/current-value statement that no longer matches live state and carries no such marker (or cites an anchor that now contradicts it). This mirrors `.ufo/gates/c1-census-v10.py:129-136` (CURRENT vs DATED; historical by construction).
- **Tags:** OBS = observed with the command in §6; INF = inference.

## 1. Verdict

| Class | Loci | Where |
|---|---|---|
| **stale-unlabelled** | **8** (10 client-attributions) | `SKILL.md:18-19`, `PROVINCE.md:9` (+`:8`), `:12` (cache clause), `:16`, `:17`, `:44`, `:24` (sha), `corpus/QUALITY.md:18` (example) |
| current | 6 (2 partial) | `PROVINCE.md:10-11,19-20,20-21,24` (v42/207), `:45`; `SKILL.md:20` (Kimi clause) |
| historical-labelled | 18 grouped loci, 45 README lines | `SKILL.md:12,512`; `PROVINCE.md:12` (6.4.0 leg), `:21-23,24` (doctor), `:25,26,67,125`; `QUALITY.md:18` (v37 token); README groups in §3 |

The lane's own census agrees: at B it returns `verdict: FAIL`, exit 1, with **4 stale blocks** (`PROVINCE.md` 8-13, 15-26, 44-44; `SKILL.md` 18-20) and **7 stale pin assertions** — 4 blocks but only **2 distinct clients** (Devin, OMP), which is why C2 phrases the metric as "expected 2".

## 2. Live-surface statements (each classified)

| # | Anchor (B) | Statement as written (trimmed) | Class | Live check (OBS) |
|---|---|---|---|---|
| A1 | `SKILL.md:11-12` | "`npx -y rea-agents@6.4.0`, 170 MCP tools / 127 CLI commands; historical, verified 2026-10-13" | historical-labelled | 6.4.0 cache is gone (see A7); the sentence claims history, not present state |
| A2 | `SKILL.md:18-20` | "Current REA package inventory ... Devin/OMP `rea-agents@6.5.0` (207 / 153); Kimi `rea-agents@6.7.0` (207 / 153; `af39310c…`; 6.4.0 historical ...)" | **stale-unlabelled** (Devin, OMP); Kimi and 6.4.0 clauses correct | live Devin=OMP=Kimi=6.7.0; census flags this block STALE |
| A3 | `SKILL.md:512` | "round 17 ... runs real, pinned Go carriers through REA 6.5.0" | historical-labelled (round-17 section) | true of that run; census marks 511-519 UNDECLARED, not historical (see F7) |
| A4 | `PROVINCE.md:8-9` | "Devin and OMP use `rea-agents@6.5.0` (207 MCP tools + 153 CLI commands; catalog tools_sha256 `805433f1…`)" | **stale-unlabelled** (both clients **and the hash**) | live 6.7.0; the correct catalog hash is `af39310c…` (F2) |
| A5 | `PROVINCE.md:10-11` | "Kimi uses `rea-agents@6.7.0` (207 / 153; `af39310c…` — the package's compiled, recorded identity)" | current | `dist/recordedCatalogDigests.js` states exactly `af39310c9591…` |
| A6 | `PROVINCE.md:12` | "Historical: Kimi resolved the historical pin `rea-agents@6.4.0` (170 / 127; `25802f6d…`) before 2026-10-18" | historical-labelled | 6.4.0 not installed; facts are a 2026-10-13/18 record |
| A7 | `PROVINCE.md:12` | "both versions have separate npx cache installs" | **stale-unlabelled** | `~/.npm/_npx/dea9475797100b20` (6.4.0) is absent, `ls` exit 2; only 6.7.0 (`a1722018f28f9df2`) and 6.5.0 (`ad9a3fdbcad992c6`) trees hold `rea-agents` |
| A8 | `PROVINCE.md:15-18` | "Drift-prone values: reverified 2026-10-18 — ... Devin `rea-agents@6.5.0` (`/home/vgpnk/.config/devin/mcp_config.json:7`), OMP `rea-agents@6.5.0` (`/home/vgpnk/.omp/agent/mcp.json:8`), Kimi `rea-agents@6.7.0` (`...config.toml:4126` ...)" | **stale-unlabelled** (two pins); Kimi correct | the cited anchors `:7`/`:8` are the right lines but now read `rea-agents@6.7.0` — the citation contradicts the sentence (F5) |
| A9 | `PROVINCE.md:18-20` | 6.7.0 cache identity: `a1722018f28f9df2` — 153 CLI commands, 207 MCP tools, `af39310c…` | current | dir present, `package.json` 6.7.0, embedded digest matches |
| A10 | `PROVINCE.md:20-21` | 6.5.0 cache identity: `ad9a3fdbcad992c6` — 153 CLI commands, 207 MCP tools, `805433f1…` | current as a cache record, **unlabelled** as no longer the Devin/OMP pin | dir present, `package.json` 6.5.0; `805433f1` is not embedded anywhere in either installed tree (F8) |
| A11 | `PROVINCE.md:21-23` | 6.4.0 cache identity: `dea9475797100b20` — 127 / 170, `25802f6d…` "(historical pin)" | historical-labelled; the path is a record, not live | dir absent; the name is still the correct `sha512('rea-agents@6.4.0')[:16]` = `dea9475797100b20` |
| A12 | `PROVINCE.md:24` | "Installed shared REA skill is v42/207 tools" | current | `~/.agents/skills/reverse-engineer-anything/SKILL.md` frontmatter `version: "42"`, `tool_count: 207` |
| A13 | `PROVINCE.md:24` | "(installed sha256 `c8639823…`)" | **stale-unlabelled** | installed file sha256 = `fbcd39d6abe8…`; `c8639823…` is now the sha of the sibling `SKILL.md.rea.backup.c8639823….recovery` (F4) |
| A14 | `PROVINCE.md:24` | "Devin/OMP 6.5.0 doctor reported aligned at luna-round-2 (historical)" | historical-labelled | past doctor reading |
| A15 | `PROVINCE.md:25` | "the 2026-10-18 6.7.0 doctor reports those registrations stale; 6.4.0 expects v37 and reports stale (L10 receipts ...)" | historical-labelled | dated; the 6.4.0 leg is no longer re-runnable (A7) |
| A16 | `PROVINCE.md:26` | "The r5-audit C8 correction was for REA 6.4.0 ..." | historical-labelled | explicit past tense |
| A17 | `PROVINCE.md:44` | "registers per-client pinned `rea-agents` (Devin/OMP 6.5.0, Kimi 6.7.0; pins per the 2026-10-18 custody receipt ...)" | **stale-unlabelled** | present-tense configuration row; live 6.7.0/6.7.0 |
| A18 | `PROVINCE.md:45` | "153 commands on the 6.5.0/6.7.0 pins, 127 on 6.4.0 (historical)" | current (statement true) | 6.7.0 `dist/cliCommandNames.js` `CLI_COMMANDS` = **153 unique** names; evidence cell cites a 6.4.0 `--version` receipt, which does not source the 153 — claim-source caveat only |
| A19 | `PROVINCE.md:67` | "a version drift past the historical Kimi 6.4.0 pin" | historical-labelled | explicit "historical" |
| A20 | `PROVINCE.md:125` | "key name corrected to the one REA 6.4.0 actually reads" | historical-labelled | inside DATED scope 119-131 (marker `:119`) |
| A21 | `corpus/QUALITY.md:18` | "Capability claims pin tool/provider versions (`rea-agents@6.4.0`, Ghidra 12.1.4, JDK 21) ..."; lesson cell "skill v37 vs release skew" | **stale-unlabelled** (example pin); v37 token historical | normative example now teaches a two-minor-old pin; current is 6.7.0 / v42 |

## 3. Historical provenance rows (classified, grouped)

All are dated knowledge rows; none asserts the live surface. The date is in the entry name or the date column, so each is `historical-labelled` even where the version token itself is not prefixed "historical".

| # | Anchor (B) | Token(s) | Basis |
|---|---|---|---|
| B1 | `corpus/README.md:16` | "127 commands" (CLI inventory) | entry `2026-10-13-rea-cli-surface` |
| B2 | `corpus/README.md:17` | "REA skill contract (v37)" | entry dated 2026-10-13; current installed skill is v42 |
| B3 | `corpus/README.md:46-60` (15 rows) | "REA 6.4.0" evidence column | entries `2026-10-13-*` / `2026-10-14-*` |
| B4 | `corpus/README.md:62-68` (7 rows) | "REA 6.5.0"; `:68` also "REA 6.4.0 (170-name tools/list)" | entries `2026-10-16-*` |
| B5 | `corpus/README.md:74` | "127-command CLI inventory", `npx rea-agents@6.4.0 --help ×16` | date column 2026-10-13 |
| B6 | `corpus/README.md:122-136` (15 rows) | "REA 6.4.0" | entries `2026-10-13-*` / `2026-10-14-*` |
| B7 | `corpus/README.md:147-153` (also `:150`, `:151` bare "6.5.0") | `rea-agents@6.5.0` / "REA 6.5.0"; `:153` "REA 6.4.0 ... 170 tools" | date column 2026-10-16 |
| B8 | `corpus/README.md:188` | "`37/170/stale`" doctor reading | refs `2026-10-13-*` |

No row in §3 needs a change for freshness; the version tokens are true of the dated run. If the lane wants unambiguous labels, adding "historical" to B2 (`v37`) and B1 (`127 commands`) is optional polish, not a defect.

**Numeric coincidences, not version statements (excluded):** `SKILL.md:150` (`...:197-207`, a corpus line range), `SKILL.md:248` (`...:149-153`, same), `PROVINCE.md:53` (`http://127.0.0.1:9222`, a port), `corpus/README.md:93` ("170-node graph", an asar graph). Provider versions (Ghidra 12.1.4, JDK 21) appear in all four files but are outside this sweep's REA-package scope.

## 4. Census cross-check (the lane's own instrument)

`python3 -I -B .ufo/gates/c1-census-v10.py --root LANE --json` at B: **exit 1, `verdict: FAIL`**, live `{devin: 6.7.0, omp: 6.7.0, kimi: 6.7.0}`, `stale` = 4 blocks, `ambiguous` = 0, `undeclared` = 2, `current_ok_per_file` = `{PROVINCE.md: 10, SCORECARD.md: 12, SKILL.md: 1}`.

- Stale pin assertions it names: `PROVINCE.md:9` (omp), `:16` (devin), `:17` (omp), `:44` (devin, omp), `SKILL.md:19` (devin, omp) — **7 assertions, 4 blocks, 2 clients**.
- It marks `PROVINCE.md:12` and `:24`, `:26` historical via inline markers; `SKILL.md:20` and `:12` are not in its current-ok set because the block already fails.
- Its L1 SCOPE (`:253-276`) covers only `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`. `corpus/README.md` and `corpus/QUALITY.md` have **no freshness gate at all** (F6).
- Nearest-preceding attribution logs `PROVINCE.md:9` as omp-only although `:8` says "Devin and OMP"; a fix keyed only to per-line census output must still replace both names.

## 5. Findings beyond the carried C2 route

- **F1 (HIGH, calibration).** The carried item names `PROVINCE.md:8-26,44` only (`corpus/lessons/round-18-verifier-spotcheck.md:189,202`). `SKILL.md:18-19` carries the same two stale pins and the census already classes it CURRENT/STALE. A PROVINCE-only rewrite leaves the skill's "Current REA package inventory" teaching 6.5.0 and leaves `stale=1`. [OBS: census block SKILL 18-20 STALE]
- **F2 (HIGH, depth).** `PROVINCE.md:9`'s `805433f1…` is the **6.5.0** catalog identity. Replacing only the version token `6.5.0`→`6.7.0` would attach the 6.5.0 hash to the 6.7.0 pin; the 6.7.0 identity is `af39310c…`, confirmed by the package's own `dist/recordedCatalogDigests.js`. The frozen 6.7.0 digest file exists only in the 6.7.0 tree; the 6.5.0 tree embeds no digest. [OBS]
- **F3 (MEDIUM, freshness).** `PROVINCE.md:12`'s "both versions have separate npx cache installs" is false today: the 6.4.0 tree `dea9475797100b20` is absent (`ls` exit 2), while its name still matches `sha512('rea-agents@6.4.0')[:16]`. The surrounding 6.4.0 facts are labelled historical; this one clause is present tense. [OBS]
- **F4 (MEDIUM, freshness).** `PROVINCE.md:24`'s "(installed sha256 `c8639823…`)" no longer names the installed bytes: the live installed skill is `fbcd39d6…` (v42/207); `c8639823…` is the sha of the `.recovery` sibling. The v42/207 count is still correct; only the identity is stale. [OBS]
- **F5 (MEDIUM, calibration).** `PROVINCE.md:16-17`'s own citations (`mcp_config.json:7`, `mcp.json:8`) now print `rea-agents@6.7.0`. The anchors are right; the values beside them are wrong, so a reader who checks the citation sees the contradiction immediately. [OBS]
- **F6 (MEDIUM, coverage).** The census never reads `corpus/README.md` or `corpus/QUALITY.md`; `QUALITY.md:18` is the only stale *example* outside all gates. Its correction is normative (criterion 8), so leaving `6.4.0` teaches new claims the wrong pin. [OBS: SCOPE list; INF: "ungated" follows from the file set]
- **F7 (MEDIUM, gate mechanics).** `SKILL.md:512`'s `REA 6.5.0` is a true round-17 record but lies in the census's `UNDECLARED` range `511-519` (the other undeclared block is `SCORECARD.md:2380-2382`). Pin edits alone cannot take the gate to exit 0; the L1 must also declare/route that range, without widening a DATED bound. [OBS]
- **F8 (LOW, calibration).** `207` is **not** independently reproduced: 6.7.0's `CLI_COMMANDS` is exactly 153 (confirmed), and the package names 65 `MCP_TOOLS_WITHOUT_DEDICATED_CLI`; 153 + 65 = 218, so 207 implies 11 CLI commands without an MCP twin (INF, consistent but not proven from a static MCP list). 153 is solid; 207 remains a recorded runtime identity. [OBS counts; INF composition]
- **F9 (LOW, freshness).** `SKILL.md:12` and B1/B5's 127/170 are unverifiable on host now (6.4.0 evicted). They are correctly labelled historical, so no edit is required; a future verification claim must not retest them against the live host. [OBS]
- **F10 (INFO).** All four files' `Ghidra 12.1.4` / `JDK 21` statements were outside this sweep; the census's own re-verification of Ghidra/JDK is another seat's claim (`KaidokuR19.GhidraJdkRecheck` report present in this wave).

## 6. Commands (exit codes as observed)

LANE = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; B = `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`; baseline copies read with `git show B:<path>` into `/tmp/kr19-SkillStalePins-base/`.

```
git -C LANE rev-parse HEAD                                                   # 0: 85589ac757f9ca3cb25efcd702d0963e25c9c4df
git -C LANE rev-parse refs/heads/main                                        # 0: same
git -C LANE merge-base --is-ancestor B HEAD                                  # 0
git -C LANE diff --name-only B HEAD -- SKILL.md PROVINCE.md corpus/README.md corpus/QUALITY.md   # 0: (no output)
git -C LANE show B:<each of the four files> > /tmp/kr19-SkillStalePins-base/<name>  # 0 x4
grep -nE 'rea-agents@|REA [0-9]+\.[0-9]+\.[0-9]+|\b(207|153|170|127)\b' <four baseline files>  # 0
grep -nE '6\.4\.0|6\.5\.0|6\.7\.0|v37|v42' <four baseline files>              # 0
grep -nE 'REA[ -]?v?[0-9]+\.[0-9]+|[0-9]+ (MCP )?tools|[0-9]+-command|[0-9]+ CLI' <four files>  # 0
grep -n -m1 'rea-agents@' ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json   # 0: :7 and :8 = rea-agents@6.7.0
grep -n -m1 'rea-agents@' ~/.kimi-code/config.toml                           # 0: 4126: rea-agents@6.7.0
for d in a1722018f28f9df2 ad9a3fdbcad992c6 dea9475797100b20; do package.json version; done  # 0: 6.7.0, 6.5.0, ABSENT
ls -d ~/.npm/_npx/dea9475797100b20                                           # 2: No such file or directory
printf '%s' 'rea-agents@6.4.0' | sha512sum | cut -c1-16                     # 0: dea9475797100b20 (name still matches spec)
grep -o '"tools_sha256":"[0-9a-f]*"' .../a1722018f28f9df2/.../dist/recordedCatalogDigests.js  # 0: af39310c9591...
grep -rl af39310c .../a172... .../ad9a...                                    # 0: three 6.7.0 files (catalogIdentity, serverIdentity, recordedCatalogDigests)
grep -rl 805433f1 .../a172... .../ad9a...                                    # 1: no match
grep -rl 25802f6d .../a172... .../ad9a...                                    # 1: no match
sha256sum ~/.agents/skills/reverse-engineer-anything/SKILL.md                # 0: fbcd39d6abe8...
grep -nE '^\s+(version|tool_count):' ~/.agents/skills/reverse-engineer-anything/SKILL.md  # 0: :5 version "42", :6 tool_count 207
python3 -I -B .ufo/gates/c1-census-v10.py --root LANE --json                 # 1: FAIL, stale 4, ambiguous 0, undeclared 2
python3 (AST-parse dist/cliCommandNames.js CLI_COMMANDS)                     # 0: 153 entries, 153 unique
grep -n 'CLI_COMMAND_TOOL_ALIASES' + read constant                            # 0: 19 alias keys; 65 MCP-only names
```

## 7. Write / install record

- **Installs or updates: none.** No pacman, npx install, uv, cargo or npm write. The only npx-cache reads were `package.json`/dist greps.
- **Writes:** this report only. No lane working-tree edit, no clone, no patch, no git/jj write, no REA `analyze`/`search`/`decompile`, no Ghidra, no carrier executed, no client-config edit.

## 8. Residual unknowns

- **U1.** Whether the L1's `.ufo/waves/round-19/tools/province-pins.py` (absent from `round-19/tools/` when I listed it) scans `SKILL.md` as well as `PROVINCE.md`. If it counts only PROVINCE, the "2 -> 0" metric can go green while `SKILL.md:18-19` stays stale (F1). [OBS: directory absent at read time]
- **U2.** Whether the lane's custody convention treats the `.recovery`/`.rea.backup` siblings as part of the "installed skill" identity. I observed only the sha mismatch (F4), not the intended record.
- **U3.** The authoritative 207-name MCP catalog list was not located as a static file; the 207 total is accepted from the 6.7.0 recorded identity, not re-derived (F8).
- **U4.** The census's `UNRESOLVED` on `PROVINCE.md:21,25` is purely the missing 6.4.0 cache; I did not run a 6.4.0 catalog to re-derive 170/127 after eviction.
