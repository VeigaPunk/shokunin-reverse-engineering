# Round 88 — non-author verifier spot-check

author: hyaku closure (non-author integrator, @m_zfl)

Reviewed 2026-11-04. This is closure evidence, not a lane-authored correction and not a promotion.
Nothing below rewrites a lane-authored byte.

- Lane base (HEAD before the round): `0cf8e3243059e0bc510b90c880d13d191e78d732`.
- Lane tip (HEAD after the round): `a242fff3fe339ffae31d83960062609a784b97c4`, equal to
  `git ls-remote origin refs/heads/main`.
- Report: fleet `.ufo/reports/round-88/kaidoku.md`, committed by the lane identity at
  `dd258908d24ce0d0a35ca466a020e0b88ff62fb0` (earlier landings of the same path `e4bc0520`, `f6af95e3`).
- Dispatched prompt: fleet `.ufo/prompts/kaidoku-round-88.md`.

## 1. Disposition and method

**Status: ok. Admitted: true. Verdict: admitted.** Both declared claims verify against the committed
bytes and against one measurement the integrator ran itself; no owned axis is harmed; every record
file this round touched is append-only (`git diff --numstat 0cf8e324 a242fff3` → no record byte deleted in any
of the seven files it touched; the one `-` line is the blank line the two SOURCES rows replaced). The round's own instruments are **not** discriminating — the lane says so itself and routed the
consequence; that is a defect in the *measures*, recorded in §7, not a false claim.

Method. Committed bytes were read with `git show <rev>:<path>`, recounted with `grep -c`, `awk`,
`sha256sum`, `git diff --numstat`, `git merge-base --is-ancestor` and
`scripts/sources-census.sh validate`. No lane-owned gate, counter or `--selftest` was executed as a
verdict (PROTOCOL §Gate standard, *Closure consequence*); every gate/selftest statement below is
committed-evidence verification. The one thing the integrator re-measured end to end is the C1
capability itself, as a black-box repair on one carrier in a private scratch tree — the counter (the
gate-shaped instrument) was not run.

## 2. Step-1 conformance

| check | command / evidence | observed result |
|---|---|---|
| Report landed by the lane identity | `git -C /home/vgpnk/Projects/shokunin log --format='%an %ae %H' -- .ufo/reports/round-88/kaidoku.md` | `kaidoku-shokunin kaidoku@shokunin.local dd258908d24ce0d0a35ca466a020e0b88ff62fb0` (three landings: `e4bc0520`, `f6af95e3`, `dd258908`) — not swept by another identity |
| Report is substantive, not a marker | report body | Two declared claims with frozen predicates, ten cited lane commits, before→after with counting commands and measured revisions, `Sources & frontier` with both census results, three trend verdicts, `## SHONEN`; not a marker |
| Required sections and order | `grep -n '^## ' .ufo/reports/round-88/kaidoku.md` | `Work performed`(6) → `Landed changes`(73) → `Before → after measurements`(90) → `Sources & frontier`(131) → `Trend verdicts`(155) → `SHONEN`(168) → `Notes`(175) — contract order, one extra trailing section the contract does not forbid |
| `SHONEN` heading with one line per box | `git show a242fff3:SHONEN.md`; report lines 170-173 | 4 boxes in `SHONEN.md`, 4 lines in the report, `[~]` each, box order 1:1, every line carries a resolvable pointer; **no `[x]`** (correct — the lane may not self-attest) |
| Cited commits exist and are ancestors | `git rev-parse --verify <h>^{commit}`; `git merge-base --is-ancestor <h> refs/heads/main` for `7fbe16d4 70d6f7de d190c5b5 6d235a4c 01ffb937 a14f0a42 1a72fdef bd74e8bc 5cd1b164 a242fff3` | All ten resolve and all ten are ancestors of `refs/heads/main` (tested against the branch ref, never `@{u}`; the repo is jj-colocated and `head=detached`) |
| Lane pushed, no uncommitted round work | `scripts/hyaku/jj-lane.sh state kaidoku-shokunin`; `git -C kaidoku-shokunin status --porcelain` | `branch=main local=a242fff3… remote=a242fff3… ahead=0 behind=0 head=detached tracked=0 untracked=8`; the eight untracked entries are the orchestrator handoff markers `.ufo/waves/round-{85,86,87,88}/r8*-w1.ready(.dispatched)` — no lane round work uncommitted |
| Prompt carries the template contract | rendered `templates/round-prompt.md` vs `.ufo/prompts/kaidoku-round-88.md` §1-§5 | §1-§5 byte-identical to the rendering; round-level items present verbatim (mission/axes binding §1; L2 floor "at least 8 L2 subagents in ONE batched AgentSwarm call" §3; commit-then-push §5; push scope §5; L0 side channel §5); five child-lane items present (report path+filename §4; commit-before-report §5 sentence sequence; `SHONEN` heading §4; commit-hash citation §4; lane write scope §5). No missing item |
| L2 route map matches the authority | `.ufo/prompts/kaidoku-round-88.md` addendum; `MISSION.md`; `~/.omp/agent/config.yml` `task.agentModelOverrides` | `MISSION.md` pins no model alias (routes resolve through the host table), so there is no MISSION bucket to contradict. The addendum's quoted maps are dated snapshots: its "ONLY reviewer uses `@m_zfl`" line and its last restore line both disagree with the live table (`reviewer`+`executor` `@m_zfl`, `scout`+`scribe` `@m_mim`, `connector` `@m_antigravity`). Conformance defect D5, status-neutral |
| Wave shape | `r88-w1-spec.json`, `r88-w1-dispatch.json`, `r88-w1-results.json` | one wave, `counts={spawn:14,resume:0,total:14}` inside the 8-16 band; roles executor 4, scout 2, scribe 2, reviewer 2, critic 1, mutation-tester 1, sentinel 1, connector 1; strict attack set (reviewer/critic/mutation-tester/labrat) 4/14 = 28.6 % ≥ 25 %; connector 1 ≤ 2; 7 delivered / 7 partial matches the report and the results file |

## 3. Per-claim re-check

### R88-C1 (coverage, capability) — `recovered 0 of 4` → `recovered 4 of 4`

Frozen container `git show a242fff3:.ufo/waves/round-88/claims.json`. Pins re-hashed by the
integrator against committed bytes and the host:

```
git show a242fff3:tools/round-88/upx-chain-repair.py   | sha256sum → 59ee51b0…b46   (= instruments pin)
git show a242fff3:tools/round-88/upx-chain-battery.py  | sha256sum → a01ed622…160   (= instruments pin)
git show a242fff3:tools/round-88/field-tamper-matrix.py| sha256sum → 0e055486…d1a   (= instruments pin)
git show a242fff3:tools/round-88/depth-blocks.py       | sha256sum → 458eeabd…d5b   (= instruments pin)
git show a242fff3:tools/round-87/upx-magic-repair.py   | sha256sum → 96da7d8e…c24   (= r87_module_sha256)
git show a242fff3:tools/round-87/upx-tamper-battery.py | sha256sum → 0f2d2bd8…4b0   (= r87_counter_sha256)
sha256sum /usr/bin/upx                                 → cf2f6e7c…969  (upx 5.2.0)
sha256sum …/rea-agents/package.json                    → a5003023…a6c  (rea-agents 6.5.0)
```

The r87 module and counter hashes are identical at base and tip — the composed anchor repair is the
base-state bytes.

**Integrator's own measurement (black box, one carrier, no counter).** In
`/fast/scratch/hyaku/closure-r88/jq`, from the pinned `/usr/bin/jq` (sha256 `e8156675…`):

```
upx --best -q -o packed orig                      → packed sha256 e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a
                                                    (= the receipt's packed_sha256 for jq)
first b_info at b0=576: sz_unc=904, sz_cpr=252    (the r87 locator law; 252 = ExecGeomCross's derived value)
zero b0+4..8 → upx -t -q                          → rc 1  "CantUnpackException: b_info corrupted"
repair --in tampered --out repaired               → rc 0  "chain-geometry: restored 0 anchor(s) derived sz_cpr 252"
byte diff tampered vs repaired                    → exactly one changed byte, offset 580, inside the 580-584 sz_cpr window
repaired == packed                                → True
upx -t -q repaired                                → rc 0  "Tested 1 file."
upx -d -q -o unpacked repaired                    → rc 0  "Unpacked 1 file."
sha256(unpacked)                                  → e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806 (= carrier pin)
control N1 (repair the plain original)            → rc 2  "refused: no validated PackHeader in the tail window"
control N3 (repair the intact packed file)        → rc 0, output byte-identical to `packed`
```

So four of the five arms (`repair_rc0`, `field_only`, `test_ok`, `identity`) and two of the three
controls were re-measured by the integrator on 1 of 4 carriers; the `rea_recover` arm is
evidence-verified (below). A repair that reads a carrier path or pin is excluded by inspection:
`grep -nE '/usr/|jq|xxd|libz|docker-init|e8156675|7b1e5d0c|6c78c5e5|0bd49c8d|1268|e8b6c9e7'` over
the repair source matches only its shebang.

Committed receipts (evidence-verified, not re-executed):

| receipt | label | arms | controls | regression | exit | pins |
|---|---|---|---|---|---|---|
| `l1/scores/c1-at-5cd1b164.json` | `recovered 4 of 4` | 20 true / 0 false (4 carriers × 5) | N1 all refused, N2 `[false×4]`, N3 all identical | `recovered 8`, `met true`, rc 0 | 0 | `repair_sha256`/`tool_sha256` = the pins |
| `l1/scores/c1-at-a14f0a42.json` | same | 20/0 | same | 8/8 met | 0 | same |
| `l1/scores/c1-at-bd74e8bc.json` | same | 20/0 | same | 8/8 met | 0 | same |

`rea.counts.procedure_count` = 167 / 99 / 184 / 1268 = the round-70 declared inventory
(`.ufo/waves/round-70/claims.json`); `unpacked_sha256` = the four carrier pins. Before-state
`pre/c1-control-r87-anchor-at-base.json`: 4 cases, every arm false, `repair_rc0` rc 2
`refused: p_info is not followed by a plausible b_info`; `identity` and `naive-global` controls 0 of 4
each.

**Ruling: claim met as reported; label honest but not mechanism-unique** (two committed cheats score
4 of 4 with all controls true — `w1/CriticClaims/receipts/cheat-c1-sibling-v2.json` and
`cheat-c1-oracle-v2.json`, both confirmed by the integrator, with the cheat scripts' hashes equal to
the receipts' `repair_sha256`). The lane discloses this in three places (entry limits, SCORECARD
round section, QUALITY 158 / M88-4, M88-8).

### R88-C2 (depth) — `blocks 27, resolved 27` → `blocks 28, resolved 28, unresolved []`

Integrator's own count over committed bytes, reproducing the counter's rule
(`SKILL.md` → `## Queue-drain craft` section → split on `^- \*\*`):

```
git show 0cf8e324:SKILL.md  → blocks 27
git show a242fff3:SKILL.md  → blocks 28
block 28's corpus/knowledge citations at a242fff3:
  2026-11-04-r87-upx-magic-tamper-repair.md   exists, 125 lines
  2026-11-04-r88-binfo-chain-geometry.md       exists,  99 lines
git cat-file -e 0cf8e324:corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md
  → "path … exists on disk, but not in '0cf8e324'"  (the block cites a document C1 creates)
```

Committed receipts: `pre/c2-depth-at-base.json` = `blocks 27, resolved 27, met_target true,
unresolved []` at `0cf8e324`; `pre/c2-control-junk-blocks.json` = `blocks 29, resolved 27`,
`unresolved` = `[{block 28: no-citation}, {block 29: absent …}]`; `l1/scores/c2-at-5cd1b164.json` =
`blocks 28, resolved 28, unresolved []` at `5cd1b164`; `l1/scores/c2-at-a14f0a42.json` = same.
`tools/round-88/depth-blocks.py:86` sets `"met_target": not unresolved`, so the counter exits 0 at
base with 27 blocks, and `w1/CriticClaims/receipts/cheat-c2-oneline-block.json` shows a one-line
citation-only block scoring 28/28.

**Ruling: claim met as reported; the counter is target-blind** (`met_target` does not encode 28), the
landed block is not causally separable from C1 (it cites C1's entry), and the block's
`b_info corrupted` row routes `sz_unc` and `sz_cpr` to one move while only `sz_cpr` is recoverable.
All three are disclosed (M88-5, M88-7, M88-9) and routed. The *artifact* delta is real and countable:
28 vs 27 blocks, block 28 = a 9-row refusal table backed by a 68-cell measured matrix, and its
citations resolve at the measured revision.

### No axis harmed

`git diff --numstat 0cf8e324 a242fff3 --` → `SCORECARD.md 27/0`, `PROVINCE.md 23/0`, `SKILL.md 17/0`,
`corpus/QUALITY.md 14/0`, `corpus/README.md 4/0`, `LOG.md 11/0`, `corpus/SOURCES.md 2/1` — **no
record byte deleted**: the single `-` line in `corpus/SOURCES.md` is the blank line the two new rows
were inserted into (no row's `status`/`recheck`/`used-by` was rewritten). `SCORECARD.md` gains one
capability row (20 → 21, `awk` over the `## Capabilities` section: `^| \`` rows) and one round
section; no pre-existing
score row is rewritten or lowered (`coverage 10.0`, `depth 10.0`, `calibration 10.0`, `freshness
10.0` all unchanged, and the round says so instead of claiming a rise on a saturated proxy).
`corpus/QUALITY.md` appends criteria Rows 154-160 after Row 153 and nothing else.

## 4. Axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | **improved** | a new corruption class (first-block `b_info.sz_cpr` zeroed) enters Core with a capability row `packed-ELF b_info chain geometry` (rows 20 → 21) and a measured 4-of-4 receipt at three revisions; `PROVINCE.md` `## Round-88 additions to Core`; `corpus/README.md` coverage row + frontier note. Score number unchanged (saturated proxy, disclosed), surface moved |
| depth | **improved** | craft rule block 28 lands (27 → 28 blocks, integrator-counted) as a 9-row refusal-signature table with named error strings and thresholds, backed by a 68-cell / 63-effective matrix with 0 unclassified; its citations resolve at `a242fff3`. Counter defect routed (§7 D3) |
| calibration | **unchanged** | no calibration claim or score row this round. The round's self-falsification of both instruments is calibration-positive *evidence* but no measured move; nothing in `SCORECARD.md` claims one |
| freshness | **unchanged** | no re-verification sweep of pre-existing entries claimed; the round's own receipts are new, not a freshness re-check of old ones |
| adjacency | **unchanged** | ConnectorR88's sibling scan (`w1/ConnectorR88/links.md`) found no sibling lane holding this ground; nothing moved in or out of the province |

## 5. Discernment spot-check (LEARNING.md — checked from outside)

Every decision below was re-opened by the integrator on 2026-11-04 with `curl` against the URL the
lane recorded; the recorded byte counts and sha256s are reproduced exactly.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S309 — UPX v5.2.0 `src/packhead.h` | **admit** (code, tier A, absent → mined) | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/packhead.h` → HTTP 200, 3678 bytes, sha256 `6cf2b14d…672`; `sed -n '55,59p'` | **agree** | The quoted lines are exactly `unsigned u_len; unsigned c_len; unsigned u_adler; unsigned c_adler; unsigned u_file_size;` at lines 55-59, and line 37 is `struct PackHeader final` / line 66 `int header_checksum;` as the row states. Source code of the packer is primary for its own header layout — tier A is correct for that scope, and the row's scope excludes the checksum algorithm (S308) and the ELF header writer |
| S310 — UPX v5.2.0 `src/packer.cpp` | **admit** (code, tier A, absent → mined) | same URL form → HTTP 200, 44586 bytes, sha256 `ab274d67…040`; `sed -n '540,550p'` | **agree** | Line 546 is `throwCantUnpack("header corrupted");` and lines 544-545 carry the `c_len`/`u_len`/`file_size_u`/version bounds, exactly as the row and the ≤25-word quote claim. The `teaches` cell's benefit (a field tamper is refused by an arithmetic gate before any checksum) is what those lines do |
| `src/headers.h` | **reject** (no row) | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/headers.h` → HTTP 404, 14 bytes | **agree** | The path does not exist at the tag; the recorded rejection (and its flip) is the right call, and rejecting rather than silently dropping it is the taste signal the registry is for |
| `src/p_unix.cpp` (re-opened; r87 rejection kept) | **reject — unchanged** (no row) | HTTP 200, 24181 bytes, sha256 `bf83c413…42e`; `sed -n '682,690p'`; `curl …/src/p_lx_elf.cpp` → 200, 373743 bytes | **agree** | Lines 682-690 do carry the `corrupt b_info %#x %#x` sanity checks, as the row says — but they are in `PackUnix::unpack`, and the lane's carriers are Linux ELF: `grep -n "PackUnix::unpack" src/p_lx_elf.cpp` → no match, while `PackLinuxElf64::unpack` (line 7755) and `PackLinuxElf32::unpack` (9023) carry their own `corrupt b_info` throws (7105, 7308). The r87 flip condition ("a carrier class unpacked through `PackUnix::unpack`") is therefore not met, and keeping the rejection is correct rather than convenient |

**New-row quote check.** S309's `teaches` cell quote is the 10-token field list at lines 55-59
(≤25 words) and S310's is the 3-token throw at line 546 (≤25 words); both locate their quote, both
match the bytes. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
→ `ok …/corpus/SOURCES.md`, exit 0, 27 `W04` duplicate-URL warnings (all pre-existing rows), no
`E03`/`E04`; rows `213` at `0cf8e324` → `215` at `a242fff3`
(`grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|'`). S309/S310 carry all 11 columns, tier `A`,
status `mined`, `used-by corpus/knowledge/2026-11-04-r88-binfo-chain-geometry.md`, which exists at the
tip.

**Gate-decision agreement: 4 of 4** (2 admits, 2 rejects). No disagreement to mine.

## 6. Trend verdicts

| trend | verdict | evidence |
|---|---|---|
| expansion | **improved** | one new admitted `corpus/knowledge/` entry on ground the coverage map did not hold (`packed-ELF b_info chain geometry`), its `source:` citing two `mined` rows opened this round (S309, S310); registry 213 → 215 rows, tier A +2 (census exit 0 before and after); one capability row enters (20 → 21); `PROVINCE.md` moves the class Frontier → Core |
| quality | **improved** | seven grounded `QUALITY.md` criteria (Rows 154-160) land, each citing the lesson that produced it (no-op tamper, off-vocabulary message, routing row vs field, target-as-argument, answer-in-input-dir, base-citing separability, measured cost bound); six corrections land in-round (QUALITY 156-160, PROVINCE receipt pointer → the measured `c1-at-a14f0a42.json`, the plan's stale 7-label sentence, the entry's sentinel wording); the matrix instrument is superseded v1 → v2 with a re-taken before record (`claims.json` `instrument_supersessions`, `01ffb937`) rather than an edit of frozen bytes. Caveat routed as D1/D3: two documentation mentions of the pre-M88-3 rule survive |
| discernment | **improved** | this spot-check agrees with the gate on 4 of 4 sampled decisions (§5); the round reports both claims **met** and both measures **non-discriminating** in the same breath (SCORECARD round section, report verdicts, M88-4/M88-7/M88-8/M88-9) instead of claiming a stronger result; and the disagreement-shaped findings became criteria (Rows 156-160), not prose |

## 7. Routed defects (kaidoku must fix; none bars this admission)

- **D1 — frozen instrument's docstring documents the falsified rule.** `tools/round-88/upx-chain-repair.py:13-18`
  says the repair "searches, from the smallest offset above `block0 + 12` … requires `0 < sz_cpr <=
  sz_unc`. Candidates whose `l_info` carries `p_filesize == PackHeader.u_file_size` are preferred",
  while the code selects on `key = (fits, total, -derived)` (`:136`) and treats the `u_file_size`
  match as a hard precondition of `l_info_candidates` (`:70-78`). This is the rule M88-3 records as
  wrong (dinit 136 vs 226), left standing in the file the correction was written for — an
  Evidence-standard *corrections-sweep* miss, and a case for the lane's own Row 150. Fix in the next
  instrument revision (the bytes are frozen this round): docstring = code.
- **D2 — plan still states the superseded rule.** `plans/round-88-claims.md:17-21` ("the smallest
  offset above `block0 + 12` …", "a candidate claiming more than `u_len` is impossible"). ReviewerC1
  §6 flagged items 5.1-5.3 as DRIFT; M88-6 corrected a different sentence (the 7-label vocabulary),
  so the drift survives. Append a correction naming the superseded text (append-only discipline).
- **D3 — the C2 counter does not encode its target.** `tools/round-88/depth-blocks.py:86`
  `met_target = not unresolved`, so it exits 0 at base (27 blocks) and on a citation-only stub
  (28 blocks). Route already named by the lane (M88-7, QUALITY 157): `--expect-blocks N` required,
  `met_target = blocks == N and resolved == N and not unresolved`, with the base arm and the stub as
  red controls in the selftest.
- **D4 — C1's counter leaves the answer beside the input.** `upx-chain-battery.py` writes `packed`,
  `n3.out` and `chain.repaired` into the same directory as the repair's `--in`, so a sibling-copy
  repair scores 4 of 4 with zero packer probes (`w1/CriticClaims/receipts/cheat-c1-sibling-v2.json`).
  Fix: one private directory per invocation holding the tampered input alone, plus the sibling-copy
  cheat as a declared red control (M88-8, QUALITY 158). The kill-rule clause "a repair that names,
  reads or hashes a carrier source path or pin" is also audit-only — no machine check exists.
- **D5 — prompt's quoted L2 route map is a superseded snapshot.** The addendum's net maps disagree
  with the live `task.agentModelOverrides` (`reviewer`+`executor` `@m_zfl`, `scout`+`scribe`
  `@m_mim`, `connector` `@m_antigravity`). Operator-side: the addendum should cite the host table, not
  restate it. `MISSION.md` stays model-agnostic and is not contradicted.
- **D6 — attack-share arithmetic mislabels the sentinel seat.** Report and `LOG.md` say "attack 5/14 =
  36 %"; the run-15 attack set is reviewer/critic/mutation-tester/labrat, so the strict figure is
  4/14 = 28.6 % (still ≥ 25 %). Correct the sentence in the next round's records; no gate outcome
  changes.
- **D7 — no planner seat.** Prompt §3's minimum role split asks for 1 planner; the wave validator
  rejects the `planner` role, so the L1 held that seat (disclosed in the report and `LOG.md`). This is
  a template/validator conflict to fix operator-side, not lane debt — the wave still carried 14 seats
  and ≥ 25 % attack.
- **D8 — pointer ambiguity in "QUALITY rows 154-160".** The round's rows exist at criteria *numbering*
  154-160 (file lines 250-262); file lines 154-160 hold criteria Rows 96-100. Content verified; a
  line-based checker would misread it. Say "criteria Rows 154-160" in the next record.

## 8. Dispatch/complete digest (from `.ufo/watchdog.log`, mutable — this copy is the closure pointer)

```
2026-11-04T19:39:05-03:00 launch kaidoku round=88 pgid=3790618 driver=hyaku-inline attempt=1
2026-11-04T20:36:02-03:00 lane-dead-no-report kaidoku round=88; retry same round (attempt=1: FAIL report_of)
2026-11-04T20:36:04-03:00 launch kaidoku round=88 pgid=1030863 driver=hyaku-inline attempt=2
2026-11-04T20:43:28-03:00 lane-dead-no-report kaidoku round=88; retry same round (attempt=2: FAIL report_of)
2026-11-04T20:43:30-03:00 launch kaidoku round=88 pgid=1882083 driver=hyaku-inline attempt=3
2026-11-04T20:57:25-03:00 complete kaidoku round=88; hyaku-inline attempt=3
```

Attempts 1 and 2 terminated without a landed report; attempt 3 landed it. The round's work was
authored across those attempts (`a14f0a42` … `a242fff3`), and attempt 3 re-measured both frozen
counters at the final tip — the receipts it cites are the ones this spot-check verifies.

## 9. Note for the operator (promotion is operator-owned)

All four `SHONEN.md` boxes now look checkable by a non-author from committed artifacts: a decision
table with named refusal signatures and cited sources (block 28, 68-cell matrix), an end-to-end
domain task (pack → zero `sz_cpr` → repair → `upx -t`/`upx -d` to the carrier pin → REA inventory),
instructions a fresh seat reproduced (seven wave seats reproduced the predicates from the plan and
tools alone), and no cross-domain bleed (ConnectorR88's sibling scan). This round wrote `[~]`
everywhere, correctly. Promotion remains an operator decision; nothing here writes `[x]`.
