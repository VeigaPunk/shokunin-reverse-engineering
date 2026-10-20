# SourcesRowAudit — round 19 (kaidoku), census at B

Read-only seat. Lane files untouched except this report; no subagents; no REA/Ghidra analysis; no carrier executed; no tools installed.

**Base.** `git -C /tmp/kr19-SourcesRowAudit rev-parse HEAD` → `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (exit 0). Clone `git clone -q --no-hardlinks LANE /tmp/kr19-SourcesRowAudit` + `checkout --detach 8a8da7e…`.
**File identity (observation).** `sha256sum corpus/SOURCES.md` → `a0cbfdc47fa176e37ae95e24fea7f15bbc2118e41ef1d8bd6071d1c42a603f07`, 78 lines, in both the B clone and the lane worktree; `git show 8a8da7e…:corpus/SOURCES.md | sha256sum` gives the same digest. Every command below therefore produces the same bytes whether run from the B clone root or the lane root. Commands were run from `/tmp/kr19-SourcesRowAudit` (the lane-root equivalent at B); command text is copied verbatim from `CORPUS.md:135,137,139,141,143,145,147`.

## 1. Frozen census — commands, outputs, exits (observation)

```
# rows (spacing-tolerant)                                        CORPUS.md:135
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
36
EXIT=0
# malformed rows — 11 columns means NF=13; must print 0           CORPUS.md:137
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
0
EXIT=0
# tier histogram                                                 CORPUS.md:139
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
A=31 B=4 C=1 
EXIT=0
# status histogram                                               CORPUS.md:141
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
mined=34 rejected=2 
EXIT=0
# duplicate ids — must print nothing                             CORPUS.md:143
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
(no output)
EXIT=0
# enum violations and tier inflation — must print nothing        CORPUS.md:145
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
(no output)
EXIT=0
# mined rows whose used-by paths do not exist — must print nothing  CORPUS.md:147
awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
(no output)
EXIT=0
```

(Commands and their comment lines are the frozen text at the cited CORPUS.md lines, verbatim.)

**Reading (observation).** 36 rows = 34 mined + 2 rejected; tiers 31 A + 4 B + 1 C; no malformed row, duplicate id, enum/tier violation, or dangling `used-by` path. This is exactly the `claims.json` frontier "before" (36 rows, exit 0, W04 S033) and matches the sibling draft's baseline count (`SourcesRowsDraft.md`, "baseline 36, lane").

## 2. Are the zeros non-vacuous? Positive control (observation)

Fixture `/tmp/kr19-census-fixture/corpus/SOURCES.md` (7 rows: 1 valid, 1 NF≠13, 2 duplicate `S901`, 1 bad kind/tier/status, 1 community-at-A, 1 mined with a missing `used-by`). Same seven commands, run from the fixture root:

```
rows 7                              EXIT=0
malformed 1                         EXIT=0
tier A=5 B=1 D=1                    EXIT=0
status mined=6 open=1               EXIT=0
dup ids S901                        EXIT=0
enum  tier S902 D
      status S902 open
      kind S902 blog
      tier-inflation S903           EXIT=0
used-by missing: corpus/knowledge/does-not-exist.md   EXIT=0
```

**Inference.** All four "must print nothing" detectors fire on their target defect class in this run, so the baseline zeros are a clean-table result, not a broken detector. Note the frozen `used-by` pipeline's exit code is the `while` loop's, so its criterion is output-only — the control demonstrates output detection, not exit signalling.

## 3. Maintained parser cross-check (observation; tool is fleet-repo, outside frozen v1)

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh {validate,census,overdue} --today 2026-10-20 /tmp/kr19-SourcesRowAudit` (exit 0 each):

```
validate → kr19-SourcesRowAudit  W04  S033 duplicate url …/ghidra/pull/9348 across scopes
           kr19-SourcesRowAudit  ok   /tmp/kr19-SourcesRowAudit/corpus/SOURCES.md
census   → rows 36 | tier.A 31 tier.B 4 tier.C 1 tier.invalid 0
           status.mined 34 status.rejected 2 status.queued 0 status.invalid 0 | missing 0
overdue  → 36 × cadence lines, 0 × overdue lines
```

`W04` is the expected S032/S033 superseding pair (round-18 spot-check, `corpus/lessons/round-18-verifier-spotcheck.md:172`). Census totals agree with §1 on every metric.

## 4. Rows whose recheck is due by 2026-10-20 (observation)

**Rule used (from the maintained grammar, `scripts/sources-census.sh:28,34-37,672-684`):** an ISO `recheck` is due on that date; `NNd` is due at `opened + N days`; symbolic cadences (`on-release`) are event-driven and never date-due.

**Result: 0 of 36 rows are date-due on 2026-10-20.** There are **0 ISO recheck values** in the registry (all 36 are cadence/event). Dated dues come only from `NNd`:

| cadence | rows | opened → due |
|---|---|---|
| `90d` | S015 (`:21`), S032 (`:38`), S033 (`:39`) | S015 2026-10-19 → 2027-01-17; S032/S033 2026-10-20 → 2027-01-18 |
| `180d` | S008–S011 (`:14-17`) | 2026-10-19 → 2027-04-17 |
| `365d` | S016 (`:22`), S018 (`:24`), S027 (`:33`) | S016/S018 → 2027-10-19; S027 → 2027-10-20 |
| `on-release` | 26 rows: S001–S007, S012–S014, S017, S019–S026, S028–S031, S034–S036 | event-driven; no release event is recorded in-row |

Earliest scheduled recheck is 2027-01-17 (S015). The maintained `overdue` run printed no `overdue` line for any row, independently agreeing.

**On-release events checkable from the host (observation).** Anchors of the installed-artifact on-release rows still match byte-for-byte, so no release event is evidenced for them this run:

```
sha256sum Base-src.zip        f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804  (= S003 anchor)
sha256sum go1.25.0.json       54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252  (= S023 anchor)
sha256sum map_swiss.go        0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383  (= S035 anchor)
sha256sum map_noswiss.go      03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291  (= S035 anchor)
Ghidra application.properties:17 → application.version=12.1.4
/home/vgpnk/.local/opt/go-1.25.0/VERSION → go1.25.0 / 2025-08-08T19:33:32Z
```

## 5. Rows citing REA versions (observation)

- **S001 (`corpus/SOURCES.md:7`)** — source "REA installed skill v42", scope "installed v42 skill", anchor `v42; Route the target first`. **S002 (`:8`)** — source "REA native-artifact guide v42", anchor `v42; Recorded Linux crashes`. These are the only two rows citing an REA version.
- **Zero rows cite a `rea-agents` CLI/package version**: `grep -c 'rea-agents' corpus/SOURCES.md` → `0`; `grep -oE '@[0-9]+\.[0-9]+\.[0-9]+'` → no match. REA is mentioned without a version in the `teaches` cells of S019 (`:25`) and S020 (`:26`) only.
- **Anchor still resolves (observation).** Installed skill `SKILL.md:4-6` has `metadata.version "42"`, `tool_count 207`; heading `## Route the target first` at `SKILL.md:85`; `references/native-and-artifacts.md:41` has `## Recorded Linux crashes`. The 6.7.0 bundle carries the same heading at its own `:41`.

**Freshness observation on those two rows' file identity — the installed skill was replaced today, 2026-10-20 13:35:56 -03, while remaining v42/207:**

```
installed  ~/.agents/skills/reverse-engineer-anything/SKILL.md
           23523 B  sha256 fbcd39d6abe803cf7aa49c1880815bc8e22ba2af87a23681944f687bb7629eb1
6.7.0 bundle ~/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/skills/reverse-engineer-anything/SKILL.md
           23523 B  sha256 fbcd39d6…7629eb1   (identical)
6.5.0 bundle …/ad9a3fdbcad992c6/…/SKILL.md
           22513 B  sha256 3456aab99d48c3294726065c9d5bd586bc165f2849fd5a3d5080381630564715
pre-change installed variant, preserved as
  SKILL.md.rea.backup.c86398238b2a382dd34f4df230f83a5a1c3377a4f0c4df39ea43053ea0b49da0.recovery
           22513 B  sha256 c8639823…b49da0
diff -rq installed-references/ vs 6.7.0-bundle-references/  → only installed-side *.rea.backup* files differ
```

**Inference (out of the SOURCES registry, flagged for C2).** `PROVINCE.md:24` still states the installed shared skill is `c8639823…` and "not byte-identical to either bundled v42/207 skill"; live evidence now contradicts both halves (hash `fbcd39d6…`; byte-identical to the 6.7.0 bundle). C2's declared falsifiable probe compares client config pins only, so this stale value is likely outside its red→green check even though C2's claim text covers "npx cache and catalog identities". S001/S002 stay truthful at version/title granularity (v42, headings present); the drift is a byte-identity claim in PROVINCE, not a row defect. Sibling `ProvinceSkillConsistency.md` did not observe this change.

## 6. Calibration notes (observation unless marked)

- Frozen census is clean at B (7/7 commands exit 0; four negative commands silent) and reproduces the round's declared baseline exactly; the sibling draft's post-integration expectation (38 rows) starts from this 36.
- Ids are contiguous `S001`–`S036` with no gaps or duplicates, so the next unused id is **S037** — the two rows drafted for C2/C3 (`SourcesRowsDraft.md`) fit and must not reuse S032/S033 (supersession already occupies that pair).
- The frozen census does **not** validate the `recheck` domain. `CORPUS.md:105-106` lists (`90d`, `180d`, `on-release`) while S016/S018/S027 carry `365d`; the maintained E09 grammar accepts any `^[0-9]+d$` (`scripts/sources-census.sh:672-675`). **Inference:** the parenthetical is illustrative, so `365d` is conformant; the frozen text alone is ambiguous, not the row.
- Two rule checks absent from the frozen census, run manually and clean: mined rows with `—`/empty `used-by` → 0; empty cells in columns 2–12 → 0.
- **Inference (cosmetic, fleet tool).** `scripts/sources-census.sh:675-677` prints a `cadence` line for every `NNd` row as well as symbolic ones, while its own header (`:34-37`) describes `cadence` as symbolic-only. No misclassification results here (0 `overdue` lines, exit 0); the label just conflates "scheduled, not yet due" with "event-driven".

## Remaining unknowns

- Whether any external on-release source released after 2026-10-19/20: 19 of the 26 on-release rows are externally hosted and were not network-probed (out of this census assignment). The other 7 point at installed host files (S001–S003, S006, S007, S023, S035); S001/S002/S003/S023/S035 were re-verified above, S006/S007 were not re-read.
- Whether C2 intends `PROVINCE.md:24`'s installed-skill identity in its rewrite scope (inference only; the declared probe does not test it).
- Row-level quote accuracy was not re-verified (Gate/outside-review work, not census).
