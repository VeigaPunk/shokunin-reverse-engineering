# R44C2Readme — corpus/README.md census for the C2 rubric

Seat: `R44C2Readme` · wave 1 pre-freeze · rev `c29360e3ba5381a5ab69e372d0d9577970f85018` (base; worktree
`f5fb8d59` is +2 commits — dispatch only; `git diff c29360e3..HEAD` on `corpus/README.md`, `corpus/knowledge`,
`PROVINCE.md`, `SCORECARD.md` is empty, so every observed value equals the base).

**Verdict: mismatches found — C2 does not need the honest stop.** Four confirmed mismatches below; a
do-nothing round leaves them standing, so CTL-C2-0 exits non-zero at the freeze.

Full machine-readable census: `R44C2Readme.json` (same directory).

## Command A (the lane's own check, SCORECARD.md:92-123) at base

```json
{"citation_resolved_rules": 21, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 137, "mapped": 137, "missing": [], "revision": "c29360e3..."}
```
Receipt: `.ufo/waves/round-44/w1/artifacts/R44C2Readme/command-a.json`
(sha256 `66a78f754537aa209babee60da641e38959e1f7f04bd6fd88ee5397b69338529`, exit 0).

## Confirmed mismatches (rubric candidates)

| id | README line | asserted | observed |
|---|---|---|---|
| r44readme-06 | 172 | `lessons/round-13-distillation` is a Knowledge-index entry | no `corpus/lessons/round-13-distillation*` object exists — the row itself says it is a SKILL.md craft section, not a corpus note; its first cell syntactically claims a `lessons/` path |
| r44readme-07 | 183 | verified-at of `2026-10-16-l7-03-inspect-electron-fuses` | `2026-10-16-l7-03` — a malformed date that mints a phantom stem `2026-10-16-l7-03` under the canonical `2026-10-\d{2}-[a-z0-9-]+` regex (would become a dangling token if it ever appeared in `## Coverage map`) |
| r44readme-09 | 230 | all `## Lessons` rows carry 3 cells under `| entry | round | gist |` | row 230 parses as 4 cells: unescaped `|` inside `` `grep -o|wc -l` `` |
| r44readme-12 | 156 | source pointer `.ufo/waves/kaidoku-r5/05-riscv-deep.md` | **dangling** — 0 objects under `.ufo/waves/kaidoku-r5` in any `--all` history; the wave is `luna-round-5` |

## Clean checks (pass; freeze only if rubric wants them)

- **r44readme-01/03** coverage-map ↔ knowledge stems: `mapped 137/137, missing [], dangling []` (the draft's
  headline check).
- **r44readme-04/05** table shapes uniform (Coverage-map 90×3 cells, Knowledge 117×4 cells).
- **r44readme-10** all 26 Lessons rows resolve to `corpus/lessions/*.md`.
- **r44readme-13** 86 unique in-repo path / path:line refs: all resolve within bounds except r44readme-12.
  Out-of-repo refs (`binaryTarget.js:105`, `GhidraClient.js:607`) → exit 2 could-not-evaluate for any rubric row.
- **r44readme-14** README `## Frontier` (17 bullets) is consistent with PROVINCE.md `## Frontier` (10 bullets
  + dated notes); latest sasquatch frontier sets match modulo `v4 Broadcom` being folded into README's
  "other vendor-mangled images". Bullet counts differ by design; include an equality check only if the
  rubric defines the subset semantics (see note).
- **n-m-r25…r43b** every re-derivable `N of M` count reproduces: r25 6 carriers/69+69 lookups; r26 24 json;
  r27 48/50; r28 187 selectors/61 carriers/61 env/187+187 db +manifest (asserted "374" = data rows)/
  230 openchain +manifest; r29 152 sel/16 carriers/16 env/152+152 +manifest ("304")/178 +manifest;
  r30 16+19; r31 12+23; r36 K1 3/3, K2 4/4, K3 K4 2130/2130 oracle rows; r39 K1-K6; r40 V1/V2/L1/L2;
  r41 V3/V4/L3/L4; r42 4 carriers; r43 sasquatch 8 tags (3-arch from v1.0.1, v1.0 amd64-only);
  r43 heldout 78 scored dirs (54 H + 24 C) + manifest; formats.html `grep -c '<h2 id='` = 97.

## Rubric-design warnings for R44C2Rubric / L1

1. **r44readme-02 is ambiguous.** "coverage-map row count vs knowledge file count" reads 88 pipe-rows ≠ 137
   files unless "row" means distinct mapped stems (then it is exactly r44readme-01). Freeze the definition
   or drop it — as written it either duplicates r44readme-01 or manufactures a 88≠137 false mismatch.
2. **Index-completeness rows (r44readme-08: 20 unindexed knowledge files; r44readme-11: 44 unindexed
   lessons) are observed but NOT asserted** by the tables — include only if the rubric declares
   completeness a claim; otherwise they are new-found debt for the lesson, not counter ground.
3. **r44readme-12 repair** is a pointer fix (`kaidoku-r5` → `luna-round-5` after verifying the file
   exists there — it does not; the deep receipt itself may need relocating or the pointer re-scoped).
   Do not let the landing rewrite the frozen blob outside C2's append/expected-diff mechanics.
4. Numbers behind live tools (127 commands, 3/7 surfaces, 18 ops, doctor registry, ADB 22/24 live,
   per-envelope member counts for r38 5/5-3/3-4/4-4/4, 97-section re-fetch) are **could-not-evaluate
   (exit 2)** for a repo-only counter unless the rubric pins a committed receipt to parse.

## Frontier bullets ↔ PROVINCE detail

README `- ` bullets 256-272 vs `PROVINCE.md:82-119`: every README item resolves to a PROVINCE bullet or
dated frontier note. PROVINCE-only items (EVM residuals, malware triage, non-REA dynamic, reconstruction,
engine installs, quality-verdict scope, tooling 2026-10-26) are PROVINCE policy surface, not README debt.
Sasquatch chain: README:266-268 still-frontier set ⊂ PROVINCE:416 set; the only named delta is
`v4 Broadcom` (PROVINCE) vs generic `other vendor-mangled images` (README) — flagged borderline, not
counted as a mismatch.
