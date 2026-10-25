# kaidoku round 35: verifier spot-check (non-author)

author: hyaku closure (non-author integrator, @m_sonnet)

Session `CloseKaidokuR35`, 2026-10-25. Range `aa04633a686d49756763b1feed4be6830d5bb479..3ca5a80f81922eb5f9182d9d176955423261b975`.
Report `.ufo/reports/round-35/kaidoku.md` (fleet commit `33be25b89c2ac4633e5bf62a586008ca7b4e1a54`, author `kaidoku-shokunin`).
Claims read: **R35-C1** (coverage, jsc2js `.jsc -> source mapping`) and **R35-C2** (calibration, round-34 defects D1-D4).
Both were declared, frozen, then stopped by the lane under its own kill rule.

No seat dispatched; every re-check below ran inline. No lane counter, gate or selftest was executed
(PROTOCOL §Gate standard, Closure consequence): committed receipts were read, claim state was re-measured
with git/grep/jq/curl over committed bytes and live sources. The only lane-side command was
`jj-lane.sh state` (pure git). Nothing installed or updated.

Driver digest (`.ufo/watchdog.log`, mutable):

```
2026-10-25T15:56:13-03:00 launch kaidoku round=35 pgid=3181248 driver=hyaku-inline attempt=1
2026-10-25T17:26:44-03:00 complete kaidoku round=35; hyaku-inline attempt=1
```

## Step-1 conformance

| check | observed | result |
|---|---|---|
| report author | `git log --format='%an %H' -- .ufo/reports/round-35/kaidoku.md` -> `kaidoku-shokunin 33be25b8...` | pass |
| `SHONEN` heading | `grep -c '^## SHONEN'` = 1; 4 `[~]` lines; lane SHONEN.md has 4 boxes | pass |
| real report, not marker | names real work, 5 landed commits, LOG entries, evidence paths | pass (status `ok`) |
| cited hashes exist and are ancestors of `main` | d2729cba, a85ca674, 2323d197, 3ecf4298, ee0c865c, aa04633a, 3ca5a80f: `cat-file` ok and `merge-base --is-ancestor <h> main` ok for all | pass |
| pushed | `jj-lane.sh state`: `local=3ca5a80f remote=3ca5a80f ahead=0 behind=0`; `ls-remote origin refs/heads/main` = 3ca5a80f | pass |
| uncommitted round work | `git status --porcelain`: 14 untracked files under `.ufo/waves/round-35/` (`claims-canonical-note.md`, `w1-settle.json`, 12 seat reports `w1/R35{Audit13,45,46,48,49,ConnectorCensus,ConnectorOverlap,MutationC2,PlannerDataWalk,ReconJscRows,ReviewerC1,ReviewerC2}.md`) | defect, status-neutral |
| prompt template contract | `.ufo/prompts/kaidoku-round-35.md` carries sections 2b frontier step, 3 L2 floor, SHONEN contract, hyaku addendum (section 6) | pass |

Conformance defects (status-neutral): (1) the report (16:20) was filed before the lane's last commit `3ca5a80f` (16:43) and says the wave had not settled, so its seat accounting is explicitly unverified; (2) `w1-results.json` lists 64 seats with all 64 `output: null` (orchestrator kernel restart), and the untracked `w1-settle.json` is malformed (`{"spawned": 2, "settled": 2, "dead": 0, "spawned": 7}` with a duplicate key) so no settled/dead count is derivable from committed bytes; (3) 14 wave artifacts left untracked in the lane; (4) the report declares the lane SHONEN boxes `[~]` only, none checkable by a non-author this round; (5) the report's trend `quality: improved` is not supported by LEARNING.md's definition (see trends).

## Per-claim re-check (all re-measured over committed bytes at `3ca5a80f`; the lane's C1/C2 counters were not executed)

### R35-C1 (coverage): not met

After-state needed: two knowledge entries, SOURCES rows S125/S129, PROVINCE and README mentions.

```
for r in aa04633a 3ca5a80f:
  git show $r:corpus/SOURCES.md | grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'   -> 106 / 106
  git ls-tree -r --name-only $r | grep -c corpus/knowledge/                              -> 129 / 129
  git ls-tree -r --name-only $r | grep r35-jsc2js                                         -> (none) / (none)
git diff --stat aa04633a 3ca5a80f -- corpus/SOURCES.md corpus/knowledge PROVINCE.md corpus/README.md SKILL.md corpus/QUALITY.md   -> empty
git diff --name-only aa04633a 3ca5a80f -- . ':!.ufo'
  -> LOG.md SCORECARD.md corpus/claim-freezes.tsv corpus/lessons/round-35.md plans/round-35-claims.md tools/round-35/c{1,2}-*.py
```

Registry rows, knowledge entries, PROVINCE, README and SKILL are byte-identical to base. Committed receipt
`.ufo/waves/round-35/controls/c1-do-nothing.json` (evidence-verified, not re-executed): exit-1 control at base, 8 named
missing conditions. Re-measured conclusion: nothing landed; coverage `unchanged`. The lane stopped the claim for a
real counter defect (PROVINCE/README checks are substring-anywhere, `w1/R35CriticClaims.md:53-54`); that stop is a
non-pass, not an improvement.

### R35-C2 (calibration): not met

Re-measured by hand each frozen condition at `3ca5a80f`:

- D-1 (census-start before first SOURCES change): SOURCES.md has no change after base (diff empty above); counter lines 71-75 of `tools/round-35/c2-calibration-counter.py` (`first_change_time(... "corpus/SOURCES.md")` -> `D1_no_sources_change_after_base`) confirm the coupling to C1 that the critic found (`w1/R35CriticClaims.md:9-20`). Genuine severability defect: only C1's rows could supply the change. Verified by reading the counter, not by execution.
- D-2 (r34 seat-accounting correction plus a `Seat accounting (round 35)` line in the lesson): `corpus/lessons/round-35.md` has no such line; and the settle receipts it must match do not exist in committed form (see defects). Not met.
- D-3 (r34b entry trio citing S106): `corpus/knowledge/` unchanged, so the r34b entry is unchanged. Counter line 126 `re.search(r"(?m)^source\s*:.*S106", body)` is a substring and would accept `S1060` (critic F2 finding, code read confirms). Not met.
- D-4 (8-cell registry rows in SKILL.md): SKILL.md unchanged. The do-nothing receipt records `D4_section_missing:### Round-34 run-6 instrument registry` and a 4-cell round-32 table; the shape mismatch is real. Not met.

Kill rule: any failing -> stop. Three of four conditions were simply not done (D-1 impossible without C1; D-2/D-3/D-4 not attempted), so the stop is consistent with the unchanged bytes. Observation, routed below: D-2/D-3 were doable without any C1 dependency and were not attempted after the falsification; the lane chose a strict no-repair reading of "no re-freeze".
Calibration: `unchanged`. The SCORECARD round-35 table matches observed repo state (scores 10->10, no capability, no axis harmed), which is calibration-consistent but not a new move.

### Axis verdicts

`git diff aa04633a 3ca5a80f -- SCORECARD.md` = +11 lines, the round-35 section only; no score line changed; spot reads show 10/10/10 for coverage/depth/calibration preserved.

| axis | verdict | basis |
|---|---|---|
| coverage | unchanged | C1 measured not met (rows 106->106, entries 129->129, no PROVINCE/README edit); not harmed |
| depth | unchanged | not claimed; SKILL.md and knowledge byte-identical |
| calibration | unchanged | C2 measured not met; SCORECARD honestly records the stop; no overreach found; not harmed |
| operability | unchanged | not claimed; new counters have selftest tallies `green=0 red=1` as lane-claimed mechanism only |
| freshness | unchanged | not claimed |
| adjacency | unchanged | not claimed; kaidoku/revenger arbitration remains open per the report |

Neither claim verified and no axis is harmed -> `admitted=false`, verdict `rejected-honest-stop`. No capability row.

## Discernment spot-check (`corpus/lessons/round-35.md` `## Gate`)

Source rows S125/S129 are gate decisions in the lesson only; the registry holds 106 rows, none new (diff of SOURCES.md empty). So no "newly written row" exists to quote-check; the lesson's own quotes were checked instead.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S125 jsc2js README | admit (bounded: tool contract, not recovery fidelity) | `curl https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md` -> 8996 bytes, sha256 `df85060f...ade3` equal to the lane's pinned digest | agree | line 130: "choose the V8 version that is **identical to** the one that produced your target `.jsc`" (14 words once bold markers are stripped; <=25); line 205 "reconstruction cannot be 100% identical to the original" confirms the caveat the lane attached |
| S129 jsc2js releases | admit (inventory only) | `api.github.com/repos/xqy2006/jsc2js/releases?per_page=100&page=1` | agree | `jq '.[0]'` -> tag `15.6.75.19`, body "Patched d8 for V8 15.6.75.19 (includes d8 + snapshot_blob.bin)." (10 words) exact; page1 length 100, page7 length 77, page8 length 0 -> 677 releases on 7 pages, as claimed |
| S150 Zenn article | reject (payload-absent) | `curl https://zenn.dev/yasu01/articles/7370bd5d414ec4` -> 174088 bytes (same as lane) | agree | `grep -c 'シンボルがない場合のヒント'` = 0; the real H2 `パターン認識のコツ` appears 4 times; the registered quote is absent, so refusal is right |
| S117 DOI | unverifiable (not fabrication) | `curl -w '%{http_code}' https://doi.org/10.1109/SP46214.2022.9833799` | agree | HTTP 202, empty body; could not be re-opened, therefore unprovable, not rejected |
| S113/S136/S147 | locatable, not adopted | not re-opened | not checked | outside the required sample; no entry cites them and none were admitted |

`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`: exit 0, `kaidoku ok .../corpus/SOURCES.md`, 9 W04 duplicate-URL warnings (S033, S047, S054, S062, S069, S083, S090, S092, S102), matching the report.

## Trend verdicts

- **expansion: unchanged.** No knowledge entry or SOURCES row admitted (entries 129->129, rows 106->106); no capability.
- **quality: unchanged.** The report self-grades `improved`, but LEARNING.md defines improvement as a weaker entry superseded or stale entries re-verified with none failing; no entry was touched and QUALITY.md is byte-identical. Lessons M35-1..M35-4 are mined mistakes (a requirement of the round) and do not move the observable. Disagree with the self-grade; not `harmed` since no admitted entry fails a bar.
- **discernment: improved.** The outside spot-check agrees with the gate on admits (S125, S129) and on the reject (S150) and on the unverifiable (S117), each re-opened. The lane had graded itself `unprovable-but-better` pending this check; outside confirmation upgrades it. Caveat: the admits touched no corpus entry, so the evidence is on source/quote fidelity only, and no QUALITY.md criterion was added from a disagreement (there was none).

## Routed defects (lane fixes next round)

1. R35-D1: self-graded `quality: improved` without a LEARNING.md observable; grade by the definition or name the superseded/re-verified entry.
2. R35-D2: the wave's seat accounting is not derivable from committed bytes (`w1-results.json` all-null, `w1-settle.json` untracked and malformed with a duplicate key). Commit the 14 untracked artifacts, or record why they stay out, and file a correction naming the supersession of the report's "not yet verified" accounting.
3. R35-D3: C2 design: D-1 coupled to C1 (severability), D-3 substring `S106`, D-4 heading/table shape unreconciled with historical layout; new C2 attempt must be severable and token-exact. D-2/D-3 are independently doable and still owed (these are the r34 verifier-routed defects D1-D4, still open).
4. R35-D4: the C1 package (S125/S129, two entries, PROVINCE/README rows) is staged but unadopted; the frontier row `.jsc -> source mapping` stays open. Reattempt with a frozen counter whose PROVINCE/README checks are table-scoped, not substring-anywhere.
5. R35-D5: report filed before the final lane commit; file/append late artifacts as an erratum, never rewrite.

SHONEN boxes: all four are `[~]` author assertions; none is fully checkable by a non-author from this round's evidence; no promotion request.
