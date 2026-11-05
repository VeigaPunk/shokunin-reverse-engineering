author: hyaku closure (non-author integrator, @m_zfl)

# Round 90 — non-author spot-check (kaidoku)

Non-author closure review of kaidoku round 90. I did not author this round and did not improve it:
I re-derived what is countable, re-opened the sources the gate judged, and verified the committed
evidence of the lane's counters without executing them (PROTOCOL §Gate standard, closure
consequence).

Lane HEAD before the round `54c277868511b2868b9fd46285a0e3e30106003e`; after
`6e47538b6bb8d42c64039a2feef2ae0e0548fbce`. Report base `fc52cc9dc`; declaration
`18b21f092429383d498572a422bc7294beb0ce7e`.

Driver digest (copied from `.ufo/watchdog.log`, mutable):
`2026-11-04T22:12:36-03:00 launch kaidoku round=90 pgid=2559947 driver=hyaku-inline attempt=1`;
`2026-11-04T22:31:23-03:00 lane-dead-no-report kaidoku round=90; retry same round (hyaku-inline attempt=1)`;
`2026-11-04T22:31:25-03:00 launch kaidoku round=90 pgid=2928275 driver=hyaku-inline attempt=2`;
`2026-11-04T22:32:19-03:00 lane-dead-no-report kaidoku round=90; retry same round (hyaku-inline attempt=2)`;
`2026-11-04T22:32:21-03:00 launch kaidoku round=90 pgid=2942391 driver=hyaku-inline attempt=3`;
`2026-11-04T22:32:59-03:00 lane-dead-no-report kaidoku round=90; retry same round (hyaku-inline attempt=3)`;
`2026-11-04T23:51:46-03:00 launch kaidoku round=90 pgid=3151696 driver=hyaku-inline attempt=1`;
`2026-11-05T00:31:43-03:00 complete kaidoku round=90; hyaku-inline attempt=1`.

## 1. Status ruling — a real report, `ok`

`.ufo/reports/round-90/kaidoku.md` is 16,587 B / 217 lines, carries the six contract sections, the
`SHONEN` heading with four `[~]` lines, seven lane-commit citations and resolvable evidence pointers.
It is not a completion marker: the landed-change table names real committed work and the
before→after section names its commands.

```
$ wc -c -l .ufo/reports/round-90/kaidoku.md
   217  16587 .ufo/reports/round-90/kaidoku.md
$ grep -c '^## SHONEN' .ufo/reports/round-90/kaidoku.md      -> 1
$ grep -cE '^- \[[x~ ]\] ' .ufo/reports/round-90/kaidoku.md  -> 4   (all [~], each with a pointer)
```

## 2. Step-1 conformance

| item | observed | verdict |
|---|---|---|
| report committed in the fleet repo by the lane identity | `git log --format='%an %H' -- .ufo/reports/round-90/kaidoku.md` → `kaidoku-shokunin 88206994bfba444591722ee8a474f18656ef4e8e` (2026-11-05 00:30:25 -0300) | conformant |
| report lands after the lane work | lane tip commit `6e47538b6` at 00:30:16 -0300; report commit at 00:30:25 -0300 (9 s later) | conformant |
| `SHONEN` heading, one line per box | 1 heading, 4 mark lines (`[~]` ×4), each with a resolvable pointer | conformant |
| every cited lane commit exists and is an ancestor of the branch | the 7 cited hashes (`18b21f09`, `5f8ea076`, `499d2183`, `d3983785`, `8346eacc`, `c264f7a4`, `6e47538b`) each pass `git cat-file -e <h>^{commit}` and `git merge-base --is-ancestor <h> main` | conformant |
| lane repo clean of round work and pushed | `jj-lane.sh state` → `branch=main local=6e47538b6bb8d42c64039a2feef2ae0e0548fbce remote=6e47538b6bb8d42c64039a2feef2ae0e0548fbce ahead=0 behind=0 head=detached tracked=0 untracked=0`; `git status --porcelain` empty | conformant |
| prompt carries the template contract | `.ufo/prompts/kaidoku-round-90.md` §1–§5 reproduce `templates/round-prompt.md` modulo substitution (normalized diff: 34 lines, every one a lane/round/path/axes substitution); §4 carries the report path+filename and the `SHONEN` section, §5 the commit-then-push order and the push scope, run-13 addendum item 4 the commit-before-report order ("the report lands last and cites the pushed lane hash") and the landed-hash citation rule, item 5 the lane write scope; no L2 route map is quoted beyond the run-15 hand-off lines, and `MISSION.md` §L2 concurrency is role-class-only | conformant |
| L2 floor and wave shape | `r90-w1-spec.json`/`r90-w1-dispatch.json`: 13 spawn, 0 resume, band 8–16; `w1/swarm-registry.json` 13 members — executor 4, scribe 2, reviewer 2, critic 1, mutation-tester 1, sentinel 1, scout 1, connector 1; one wave, no second | conformant |
| attack share ≥25 % | reviewer 2 + critic 1 + mutation-tester 1 = 4/13 = 30.8 % under the run-89 house list; the report says 5/13 = 38.5 % (it counts an extra seat). The floor holds either way | conformant, arithmetic label off (D-6) |
| `LOG.md` + `SCORECARD.md` records | round-90 entries present in both, plus the retroactive round-89 record; their source/QUALITY counts are stale (D-1) | conformant; defect D-1 |
| report minimum content | all six sections present, but the `c264f7a4` landed-change row has no `LOG.md` cell (D-2) | defect D-2 |

## 3. Per-claim re-check

**R90-C1 (coverage; capability `T5-chain-szcpr-wrong-later`, Frontier → Core).** Evidence-verified —
I did not execute the lane's battery. What I re-derived myself: the receipt's binding pins and the
before arm.

```
$ jq '{revision,expect,recovered,exit,met_target,controls_ok}' .ufo/waves/round-90/l1/scores/c1-at-499d2183.json
 revision 499d2183a67058d5648b51a2abf50c10012b1292
 expect   "P1 6 of 6; P2 4 of 4; P3 4 of 4"
 recovered {P1:6, P2:4, P3:4}   exit 0   met_target true
 controls_ok {N1-refuse-plain,N2-corrupt-payload,N3-intact-idempotent,carrier_blind,
              cheat_repack,isolation,no_work,rea} = all true
$ jq -r '.cases | to_entries[] | "\(.key): n=\(.value|length) recovered=\([.value[]|select(.recovered)]|length) allarms=\([.value[]|(.arms|to_entries|all(.value))]|all)"' <receipt>
 P1-later-block: n=6 recovered=6 allarms=true
 P2-first-block: n=4 recovered=4 allarms=true
 P3-zeroed:      n=4 recovered=4 allarms=true
$ jq '{recovered: .controls.no_work.recovered, n: (.controls.no_work.cases|length)}' .ufo/waves/round-90/pre/c1-candidate-at-declaration.json
 {recovered: 0, n: 6}          # the unchanged round-89 repair on P1 = the declared before arm
$ git show 499d2183:tools/round-90/upx-break-repair.py | sha256sum
 90dea08720a37e876e7f08eafe339a62c710baf402c1342924f9b41b44d5cd6a   (= receipt repair.sha256)
$ git show 6e47538b:tools/round-90/upx-break-repair.py | sha256sum   -> 90dea087…  (tip identical)
$ git show 6e47538b:tools/round-90/upx-later-block-battery.py | sha256sum -> 5462ef13…  (= 499d2183)
```

Controls read from the receipt: `carrier_blind` `blind_ok true`, 6/6 cells, decoy probe listing the
same decoy sha256 for all four pinned paths; `cheat_repack` `{"blinded":false,"unblinded":true}`.
Committed self-test tallies: `w1/CriticClaims/CriticClaims.md` R8 → `cases=8 failures=0`, R9 →
`cases=17 failures=0`. **Verdict: improved** — the after-receipt's revision is four commits behind
the tip, but both instrument files are byte-identical at the tip (sha256 above), so the receipt
grades the tip's bytes; the wave's survivor (a source-free cheat that ships its own carrier copies,
`w1/MutCounter/receipts/matrix-summary.txt` `base-copy met=True exit=0`) is disclosed in the report
and QUALITY 174 and confines the claim to *capability*, not mechanism.

**R90-C2 (depth; craft rule block 30).** Re-measured by me with my own parser (not the lane's
counter): the `## Queue-drain craft` section's `^- \*\*` blocks, each block's
`corpus/knowledge/…` citations resolved and range-checked against the file at the same revision.

```
54c277868  blocks 29  unresolved []
fc52cc9dc  blocks 29  unresolved []
8346eacc   blocks 30  unresolved []
6e47538b   blocks 30  unresolved []
```

That reproduces `pre/c2-depth-at-base.json` (`blocks 29, exit 1, met_target false`) and
`l1/scores/c2-at-8346eacc.json` (`blocks 30, resolved 30, unresolved [], exit 0`). Block 30's ten
criteria rows — QUALITY 146, 157, 159, 161, 162, 163, 167, 168, 169, 170, 171 — are each present at
the base revision (`grep -c` = 1 each), and the table body has ten rows routing a defect class to a
signature, a guard and a criterion (`SKILL.md:739-755`). **Verdict: improved.**

## 4. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | improved | a Frontier class moved to Core on four pinned carriers (`PROVINCE.md:745-753`, `corpus/README.md:131,272,382`), knowledge entry `corpus/knowledge/2026-11-04-r90-interior-block-szcpr.md` citing mined S313/S314/S316, capability row entered in `SCORECARD.md` |
| depth | improved | block 30's ten-row supersession-guard table; 29 → 30 blocks, every citation resolves at the measured revision, every criterion row present at base |
| calibration | improved | D-89-5/D-89-6 repairs (retroactive round-89 record, the two dead pointers), QUALITY 172-177 added from the round's own instrument defects, limits declared before data. Qualified by D-1 |
| freshness | unchanged | no re-verification claim this round; the entry carries `recheck: 180d`; nothing observed stale and left unmarked beyond D-1's counts |
| operability | unchanged | not claimed; the entry's counting command and the counters' `--selftest` paths exist at the tip |
| adjacency | unchanged | the connector's exact-scope sweep found 0 matches on the new Core ground in sibling lanes (`w1/ConnectorOverlap/receipts/exact-sibling.json`); no contested scope |

No owned axis is harmed: `git diff 54c2778 6e47538b -- SCORECARD.md` adds the round-89 retro record,
the round-90 record and one capabilities row, and changes no existing axis score.

## 5. Discernment spot-check (`corpus/lessons/round-90.md` `## Gate`)

Every source below was re-opened by me at its canonical URL on 2026-11-05, with its size and sha256
measured locally.

| item | decision | re-opened source | agree/disagree | reason |
|---|---|---|---|---|
| S313 `src/p_unix.cpp`, `PackUnix::unpackExtent` | admit (A, code) | `https://raw.githubusercontent.com/upx/upx/v5.2.0/src/p_unix.cpp` — 24,181 B, sha256 `bf83c4133c27d39433db63bf604daf577d429d734c542d29c0b9cc8ed229642e` | agree | line 472 reproduces the 12-word quote verbatim; lines 485 `fi->readx(&hdr, szb_info);` and 504 `fi->readx(ibuf+j, sz_cpr);` are exactly as cited, so the consumer's header-then-payload loop grounds the chain law the entry states |
| S314 `src/p_lx_elf.h`, `o_binfo` | admit (A, code) | `…/v5.2.0/src/p_lx_elf.h` — 31,147 B, sha256 `895da5cd72da32bf17846ef4b8088b1ed75dc35ac2506f694098bb30c90c7d89` | agree | line 107 is `unsigned o_binfo;  // offset to first b_info` (7 words); the source names the first block's start, which is what the row claims it teaches |
| S316 `src/p_unix.cpp` pack side | admit (A, code) | same URL as S313 | agree | lines 335 `void PackUnix::packExtent(`, 439 `set_te32(&tmp.sz_unc, ph.u_len);`, 449 `fo->write(&tmp, sizeof(tmp));`, 458 `fo->write(obuf, ph.c_len);` all reproduce; a distinct scope on one URL is legitimate and the census reports it as warning W04 only (exit 0) |
| S315 `NEWS` | reject (C, docs) | `…/v5.2.0/NEWS` — 26,202 B, sha256 `7eafd96adc1674a390a89bb1c96e9ec92686e5b1f002aa048c4a0fc26bc758f4` | agree | my own sweep `grep -c 'b_info\|sz_cpr' NEWS` → 0: the negative claim reproduces, and the row states its flip condition ("a release entry that changes the block format or its bounds") |
| S311 anchor drift (recorded, row untouched) | note, not an edit | `…/v5.2.0/src/p_lx_elf.cpp` — 373,743 B, sha256 `551fc8675a59493793f59b64eb8bb9cc208a34f701cc2bda8c9aaafb228d2dc` | agree | line 7067 is the `l_magic` test and 7098-7099 are comments; the cited cross-check is at 7069 (`get_te32(&hdr.p.p_filesize)`) and `unpackExtent` at 7102 — the old→new drift is real and the append-only rule was kept |

Registry census (my command, base vs tip): rows 217 → 221; tiers A 198 → 201, B 11 → 11, C 8 → 9;
statuses mined 194 → 197, rejected 23 → 24 — every number in the report's Sources & frontier
reproduces. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` →
29 W04 duplicate-URL warnings (including the new S316`|`S313 pair), `ok`, exit 0.

## 6. Trend verdicts

- **expansion — improved.** A new knowledge entry on ground the coverage map did not hold (interior
  block boundaries), citing three rows opened and mined this round; a Frontier line became a Core row
  on four pinned carriers; the registry gained three admitted sources. The surface moved, not only a
  number.
- **quality — improved.** The instrument supersession closed four wave defects before the landing
  measurement (REA arm required, `--rev` pinned to a commit, isolation wording, filter docstring),
  block 30 landed with criteria that exist at base, and QUALITY 172-177 turn the round's own defects
  into criteria. Named limits: the last-block fall-through (QUALITY 176), the blind arm's `boxes`
  tree (174), six untyped crashes on 27 hostile inputs (177), the depth predicate not entailing a
  table (175), and 15 of 17 mutants surviving (`w1/ExecMutation/ExecMutation.md`).
- **discernment — improved.** The attack seats found real defects, three were closed before landing,
  the survivors are disclosed rather than suppressed, every round-89 routed defect has a disposition,
  and my re-opened sample agrees on all four gate decisions.

## 7. Routed defects — kaidoku owes these to round 91

- **D-1 (record drift).** `SCORECARD.md`'s round-90 paragraph says the census ran "217 rows … after
  (220 rows): S313, S314 admitted, S315 rejected" and names "QUALITY 172-173"; `LOG.md`'s round-90
  "Sources and frontier" bullet says "217 → 220 rows" and "QUALITY rows 172-173". The measured tree
  is 221 rows with S313/S314/S316 admitted and S315 rejected, and QUALITY reaches 177. Both were
  written before the last wave commit and never swept (PROTOCOL §Evidence standard, "corrections
  sweep every mention"). `LOG.md` is append-only: add a correction entry naming the superseded text;
  correct the SCORECARD paragraph by a new naming row.
- **D-2 (report minimum content).** The `c264f7a4` row of the report's Landed-changes table carries
  no `LOG.md` entry cell; every other row does.
- **D-3 (receipt/revision attribution).** The report cites
  `.ufo/waves/round-90/pre/c2-depth-at-base.json` as taken "at `fc52cc9dc`", while the receipt's own
  `revision` field is `54c277868511…`. `sha256(SKILL.md)` is `56736cb8…` at both revisions, so the
  measurement transfers, but the citation names a revision the receipt does not.
- **D-4 (registry home).** No `SKILL.md` instrument-registry row exists for
  `tools/round-90/upx-break-repair.py`, `tools/round-90/upx-later-block-battery.py` or
  `tools/round-90/control-cheat-repack.py`; the last `tools/round-*` row is round-89's
  (`SKILL.md:1979`). Per the Gate standard, a counter with `--selftest`, an exit map and a pinned
  `--expect` is a gate, and a gate without a registry row is not conformant. Register all three.
- **D-5 (SCORECARD counting command).** The C1 row's command still reads `--rev <measured>` and names
  no receipt file, which is the defect QUALITY 173 (added this round) names; pin `499d2183…` and the
  receipt path in the row.
- **D-6 (attack-share label).** The report's 5/13 = 38.5 % counts one seat more than the run-89
  house list (reviewer + critic + mutation-tester = 4/13 = 30.8 %); the ≥25 % floor holds either way.

## 8. SHONEN — note for the operator

I wrote no `[x]` and edited no lane file. All four `SHONEN.md` boxes now look fully checkable by a
non-author from the cited evidence: block 30 states its criteria as `QUALITY.md` rows that exist at
the base revision (box 1); the four-carrier repair ran with its receipts committed under
`.ufo/waves/round-90/l1/scores/` and is logged in the round-90 `LOG.md` entry (box 2); the entry's
counting command and limits are self-contained (box 3); the new Core row is packed-ELF ground only
and the connector's sweep found no sibling overlap (box 4). Promotion stays operator-owned.
