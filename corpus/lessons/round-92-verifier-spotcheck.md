# Round 92 — verifier spot-check (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane `kaidoku-shokunin`, lane-round 92, attempt 1. Base `73a882712907606eba074377b536c6dd82517e25` → tip `5815996883426673daeb8ba3c0e78eebb537f8f4`. Report `.ufo/reports/round-92/kaidoku.md`. This file is written by the non-author closure judge; the lane did not author it.

## 1. Conformance (step 1)

- Report committed in the fleet repo by the lane identity: `git -C /home/vgpnk/Projects/shokunin log --format='%an <%ae> %H %ad' -- .ufo/reports/round-92/kaidoku.md` → `kaidoku-shokunin <kaidoku@shokunin.local> ef55f097a4cb552fe55e81c15fad13693172a1b0 Thu Nov 5 10:01:53 2026 -03:00` (lands last: before the driver's `complete` line 10:05:56-03:00).
- `SHONEN` heading present with one line per box (4 boxes, all `[~]` + resolvable pointers — correct: no non-author verifier existed at filing time).
- Prompt `.ufo/prompts/kaidoku-round-92.md` carries the template contract verbatim: MISSION/AXES binding (§1–2), L2 ≥8 in one batched call (§3), commit-then-push (§5), push scope (§5), L0 side channel (§5); the five child-lane items — report path, commit-before-report ordering, `SHONEN` heading, commit-hash citation rule, write scope; hyaku addendum §6.
- Every cited lane commit exists and is an ancestor of the branch ref (`merge-base --is-ancestor <h> main` for `73a882712…`, `11f8606178…`, `a3d3c649…`, `97bb81ef2…`, `581599688…` → all yes; git HEAD detached, jj-colocated).
- `scripts/hyaku/jj-lane.sh state <repo>` → `branch=main local=5815996… remote=5815996… ahead=0 behind=0`; `git status --porcelain` empty; `git ls-remote origin refs/heads/main` → `5815996883426673daeb8ba3c0e78eebb537f8f4`.
- Write scope: the 226-file round diff touches only `corpus/`, `LOG.md`, `plans/`, `PROVINCE.md`, `SCORECARD.md`, `SKILL.md`, `tools/round-92/`, `.ufo/waves/round-92/` — no MANIFEST/state/other-lane files.
- Not a marker: the report names two declared claims with committed receipts, four landed commits tied to LOG entries, and resolvable evidence pointers.

## 2. Claims (step 2) — re-measured over committed bytes

Both claims rest on lane-owned gates (frozen counters). Per PROTOCOL §Gate standard I verified the committed evidence (self-test tally, frozen-run verdicts, the revision measured) and re-derived the labels from the committed receipts with jq; I did not execute the lane's gates.

**Gate evidence (both claims).** Registry rows exist at the lane registry home (`SKILL.md:1990–1992`: tool + both counters, verdict maps 0/1/2, self-test spelling, pins, write scope, owner `kaidoku-r92`). Self-test tally committed: `w1/ExecRepair/selftest.log` → `SELFTEST cases=6 failures=0`. Frozen instruments unchanged since the declaration: `git show 11f8606:tools/round-92/stop-boundary-repair-battery.py | sha256sum` = `63e9df431f5d7aeeca2bd5384efff36b4f2ebedfdc3ee71aaa250287fc9388bc` = tip bytes = the `counter_sha256` pin in `.ufo/waves/round-92/claims.json`; `git diff --stat 11f8606..581599688 -- tools/round-92/stop-boundary-battery-v2.py tools/round-92/stop-boundary-repair-battery.py` empty. Every receipt carries its measured revision.

**R92-C1 (coverage, capability) — re-measured: improved.**
- Before (do-nothing control = round-91 repair at base): jq over `.ufo/waves/round-92/pre/c1-control-do-nothing-round91-repair.json` → label `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, exit 1 (met False), rev pin `base-73a882712`.
- After: jq over `.ufo/waves/round-92/l1/scores/c1-at-a3d3c649ddfef2b4c850ec950e9f633194f08efc.json` → label `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10`, exit 0, label == frozen `--expect`, rev `a3d3c649ddfef2b4c850ec950e9f633194f08efc`.
- Candidate identity: `sha256sum tools/round-92/upx-stop-boundary-search-repair.py` at tip and at `a3d3c649` both `ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1` — the measured revision is the landed tool.
- Named limits disclosed and scoped in the claim (pinned-image table passes the label, M92-d; window ±16 is a cap, not a fitted cliff — critic): the frozen predicate as declared verifies.

**R92-C2 (calibration) — re-measured: improved.**
- Before (round-91 label at base): jq over `pre/c2-do-nothing-v1-counterfeit-{A,B,C}.json` → all `refused 8 of 8; unsafe 0; intact 4 of 4`, exit 0 — admitted 3 of 3.
- After (v2 at `a3d3c649`): jq over `l1/scores/c2-counterfeit-{A,B,C}-v2-at-a3d3c649….json` → A and B `intact 4 of 5`, C `typed 0`, all exit 1 — admitted 0 of 3.
- Positive control: `c2-positive-v2-round91-at-a3d3c649….json` → `refused 10 of 10; typed 10; unsafe 0; intact 5 of 5`, exit 0 (v2 still admits the honest refusal). Do-nothing positive at base identical (exit 0).
- Claim headline narrowed to "the three named round-91 counterfeits" (CHEAT-D five-carrier carrier-read and CHEAT-E five-entry table still pass v2 — critic + MutCounter M1/M2, receipts `w1/CriticClaims/receipts/v2-cheat{D,E}-*.json`); narrowing recorded as M92-c, so the headline matches the measured set.

**Harm check — no owned axis harmed.** `git diff 73a882712 581599688 -- SCORECARD.md` shows the round-92 section only; no numeric score moves (coverage and calibration stay 10.0 on saturated finite proxies; depth unchanged). Regression receipts: `pre/regress-base-round91-repair.json` (round-91 tool at base) and `l1/scores/regress-candidate-at-a3d3c649….json` both `P1 6 of 6; P2 4 of 4; P3 4 of 4`, exit 0 — the round-90 surface is intact. No exploratory claim this round, so no `unprovable-but-better` ruling is needed.

Summary: both claims **re-measured** (jq over committed receipts + pin/hash identity checks); gate evidence **evidence-verified** (selftest tally, frozen counter sha, registry rows).

## 3. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | improved | Frontier last-block class → Core repair inside ±16; frozen C1 label met at `a3d3c649`, do-nothing control met False; capability row enters SCORECARD; PROVINCE Core bullet landed |
| calibration | improved | v2 counter refuses all three named round-91 counterfeits (met False ×3) while the honest refusal stays met True; before: 3 of 3 admitted |
| depth | unchanged | not claimed; no score move; D-91-3 block-31 correction deliberately routed to round 93 |
| freshness | unchanged | not claimed; master drift at S313 line 506 recorded by the scout; no stale item left unmarked |

## 4. Discernment spot-check (step 3)

Sampled from `corpus/lessons/round-92.md` `## Gate`: one new-row admit (S317), one re-opened admit (S313), and one rejection decision (the S313 "every executable carrier" scope wording, rejected by the scout; the Gate's only reject-shaped decision — no source row was rejected this round, stated in the Gate).

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S317 (new row, tier A, `mined`) | admit | `curl -fsSL https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_lx_elf.cpp` → HTTP 200, 373743 bytes, sha256 `551fc8675a59493793f59b64eb8bb9cc208a34f701ccd2bda8c9aaafb228d2dc` (matches row and Gate); `sed -n '8065p'` → `if (sz_cpr != UPX_MAGIC_LE32)  // sz_cpr must be h->magic` — exact | **agree** | the located quote grounds `teaches` (the caller's EOF trailer check that decides the stop boundary); ≤25 words, frontmatter-row location correct |
| S313 (re-opened by ScoutSource) | admit (scope re-grounded) | `curl -fsSL …/v5.2.0/src/p_unix.cpp` → HTTP 200, 24181 bytes, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` (matches); `sed -n '496p'` → `if (sz_cpr > sz_unc \|\| sz_unc > (int)blocksize)` — exact | **agree** | the bound quote is real and the row is the right primary source for the block-loop bound |
| S313 "every executable carrier" wording | reject (wording not used; recorded in Gate, knowledge Limit 8) | fetched `p_unix.cpp` and `p_lx_elf.cpp`: `PackUnix::unpack` at p_unix.cpp:609 / `unpackExtent` at :476; ELF carriers have their own unpack paths — `PackLinuxElf64::unpack` p_lx_elf.cpp:7755, `PackLinuxElf32::unpack` :9023 | **agree** | the ELF packers' unpack does not ride `PackUnix::unpack`, so "every executable carrier" is demonstrably too broad; rejecting the wording without editing the row respects SOURCES append-only rule 2 |
| C1 frozen label vs the pinned-image table (M92-d) | named limit, not fixed | critic `c1-table-repair-5.json` met True; MutCounter `N1i`; `ReviewerRepair.md` HIGH | **agree (as a limit)** | a table of the five pinned packed images passes the frozen label without packer calls; scoping the credit to "five pinned carriers" and routing a fresh-pack oracle to round 93 is the honest handling |
| C2 headline vs CHEAT-D/CHEAT-E (M92-c) | narrowed, not hidden | `w1/CriticClaims/receipts/v2-cheatD-carrierread5.json`, `v2-cheatE-table5.json` met True | **agree (as a limit)** | the membership counterfeits over the public carrier set pass v2; narrowing the headline to the three named counterfeits matches the measured set |

Census gate re-run by the non-author: `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → exit 0, `ok`, 30 `W04` (the S317 duplicate-URL warning against S311 is expected, distinct scope), no `E01/E03/E04`. Row counts re-derived: 221 at base → 222 at tip (`grep -cE '^\|\s*S[0-9]{3,}\s*\|'`).

## 5. Trend verdicts (verified)

- **expansion: improved.** Frontier class moved to Core with a capability row (SCORECARD round-92 section, PROVINCE.md:769), a knowledge entry with the provenance trio citing S313+S317 (`corpus/knowledge/2026-11-05-r92-stop-boundary-repair.md`), registry 221→222, all on uncovered coverage-map ground.
- **quality: improved.** Two instruments with frozen labels and pinned sha; QUALITY rows 184–187; D-91-1 repaired by a sweep shown able to fail (`7 != 29`, rc 1 on the round-91 report; rc 0 on the corrected fixture — `w1/ScribeQuality/receipts/sweep-w04-fixtures.log`); no admitted entry failed a re-check.
- **discernment: improved.** The attack seats broke two claim headlines and the lane narrowed them on the record (M92-c, M92-d) instead of shipping the wider claims; the non-author spot-check (this file, §4) agrees with every sampled gate decision — no disagreement left unlearned.

## 6. Routed defects and notes for round 93 (status-neutral)

1. **S313 `teaches` still carries the over-broad "every executable carrier" wording.** The narrowing lives in the Gate and the knowledge entry's Limit 8, and the row itself was correctly left unedited; per SOURCES rule 2 a lasting correction is a new row whose `teaches` opens `supersedes S313 —`. Route: land that superseding row (or fold it into the round-93 fresh-pack work).
2. **No planner seat** in `r92-w1` (the L1 reports the wave validator refuses `planner`; the L1 held the seat). Wave shape 8–16 band otherwise met: 12 seats, attack share 4/12 = 33 %, one connector.
3. **C2 parser is key-presence-only** (`refused: null` counts as typed — ReviewerContract). Bounded by arithmetic in v2; the round-93 fresh-pack oracle should also tighten this.
4. **W04 duplicate URL S317/S311** — expected warning (distinct scope), no action beyond awareness.
5. D-91-3 (craft block 31 cites QUALITY 169) consciously deferred to round 93 with the frozen predicate kept — accepted; it stays on the routed queue.
6. SHONEN boxes remain `[~]` — all four are checkable by a non-author from committed evidence (SKILL.md decision row + registry, LOG round-92 entry + counters at `a3d3c649`, selftest rc 0, PROVINCE Core/Frontier + ConnectorOverlap). Operator may treat this file as non-author verification input for promotion review (promotion itself is operator-owned).
