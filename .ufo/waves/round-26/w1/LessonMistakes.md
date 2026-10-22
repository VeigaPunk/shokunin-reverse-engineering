# LessonMistakes — round-26 `## Mistakes` entries (ready to paste)

Seat `KaidokuR26.LessonMistakes`, round 26 attempt 1, wave 1. Scope: mine round-25 and earlier
mistakes with evidence pointers for the L1's `corpus/lessons/round-26.md` `## Mistakes` section.
Format copied from `corpus/lessons/round-25.md` `## Mistakes` (attempt-3 table: id | class |
evidence pointer | captured-by | fix and how it was shown able to fail). The L1 owns the file and
the numbering; the ids below are proposals.

Bounds honoured: lane read-only except this report file; no git write, no `jj`, no REA call, no
network, no install. All findings below are observations of committed bytes unless labelled
`[inference]`. Nothing here is a claim-verdict, an admission or a promotion.

## Behavior

Read the round-25 lesson, the round-25 non-author spot-check, both round-25 wave-1 mutation seat
reports, the committed round-25 fleet report and its prompt contract, `LOG.md`, `corpus/QUALITY.md`,
the wave-dispatch-counting lane rule and the frozen round-26 claims. Re-measured the SOURCES row
counts and the wave-2 dispatch artifacts. Produced three paste-ready Mistakes entries.

## Mistakes (paste-ready)

| id | class | evidence pointer | captured-by | fix and how it was shown able to fail |
|---|---|---|---|---|
| M26-1 | counter frozen without a demonstrated red case; the false accept surfaced only after the freeze, which then barred the repair | `.ufo/waves/round-25/a3/w1/C1Mutation.md:38` (M9 decoy `\| coverage \|` row, live row `90/90`, exit 0 / I4 true), `:61-63` (same, false-accept #4), `:89-93` ("I4 never reads `corpus/README.md`"; first-match-wins over the whole file); `.ufo/waves/round-25/a3/w1/C2Mutation.md:51-54` ("The instrument never opens anything"), `:59-70` (M10 fabricated row, M8 never-fetched URL, M26 forged `opened` cell), `:42` (M26 mutant row), `:112-116` (verdict on the frozen claim); routed: `corpus/lessons/round-25-verifier-spotcheck.md:190-192`; disclosed, unrepaired: `.ufo/reports/round-25/kaidoku.md:19` | partial, and only after the freeze: `corpus/QUALITY.md:43` (row 33) pins a frozen instrument but binds no red case; `corpus/QUALITY.md:39,42` (rows 29, 32) require a retained red/green outcome for a named false accept only inside a red repair demonstration, and the freeze rule then blocked the repair. The wave-1 mutation seats (`C1Mutation.md`, `C2Mutation.md`) are the only detectors, and they ran after the freeze | The round-25 instruments are not reused. Round 26's counters are written to rules that already carry the repair: `tools/round-26/c2-calibration.py` scopes rows to the SCORECARD `## Owned axes` section ("Rows elsewhere in SCORECARD are never read (round-25 first-row false accept)") and ships a red fixture per item, "including a decoy `\| coverage \|` row outside `## Owned axes`"; `tools/round-26/c1-id-identity.py` re-derives each verdict from the three committed envelopes (subject sha256 = carrier pin) instead of trusting a declared cell. Shown able to fail this round: the C2 selftest must exit 1 on its decoy-row fixture and at base `a0639d8e` (5 of 6 mismatches, K4), and the C1 counter must report rows_complete 0 of 8 and entry_ok 0 at the same base. Not yet observed: both instruments are being written this wave, so the red runs are an obligation on the L1, not a result |
| M26-2 | the round's falsify wave was validated, counted as spawned, and never ran; the round was admitted on wave-1 seats alone | `corpus/lessons/round-25-verifier-spotcheck.md:18-23` (33 seats, 8 attack seats = 24.2%, one short of the session's 25% attack floor of 9; wave 2 cut by the 2 h scope freeze); `LOG.md:2960` ("Wave 2 (32 attack seats … validated) was not dispatched: Main froze scope at 11:20Z before wave 1 finished"); `.ufo/waves/round-25/a3/w2-dispatch.json` counts `{"spawn": 32, "resume": 0, "total": 32}`; `.ufo/waves/round-25/a3/w2/swarm-registry.json` (32 members, every `agentId` null); `.ufo/waves/round-25/a3/w2/` holds only `swarm-registry.json` — 0 seat reports | none for the admission: the same spot-check records the 25% attack floor as "not a protocol admission criterion". The count rule that would have caught the artifact, `corpus/lessons/2026-10-18-wave-dispatch-counting.md` rule 1 ("Count the items array, not the intent"), was applied to wave 1 but not to wave 2, whose own dispatch artifact says `spawn: 32` | Seats are counted from the task result's agent ids and the returned report files; a validated-but-undispatched wave is recorded as not dispatched with its spec path, and a dispatch artifact's `spawn` number never stands for seats that ran. Shown able to fail this round: the same count applied to round 25 reads 33 spawned (65 wave-1 registry members minus 32 with `agentId` null; 33 report files under `.ufo/waves/round-25/a3/w1/`) and 0 wave-2 spawned, while a registry-or-dispatch reading would report 65 and 32 — the exact M25-10 slip. Round-26 wave 1's seat census and the round report's attack-seat number must come from that artifact |
| M26-3 | Sources before-count taken at a superseded attempt freeze instead of the lane-round base | `.ufo/reports/round-25/kaidoku.md:49` ("Rows 74 → 78 (`git show <REV>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3} \|'` at `7ef837a4` and `1e064f9b`)") against lane-round base `18e7eb6d`; `corpus/lessons/round-25-verifier-spotcheck.md:49-52` (72 at `18e7eb6d`, 74 at `7ef837a4`, 78 at `cce7504a`; attempt-1's S073 and S074 are not in the tally) and `:198-199` (routed defect 6). Re-measured by this seat, exit 0, 2026-10-22T12:18:12Z: 72 / 74 / 78 at those revisions, 78 at round-26 base `a0639d8e` | none: `.ufo/prompts/kaidoku-round-25.md:109-110` requires the counting command and the commit measured against, and `:111-114` requires the before→after pair, but nothing names the lane-round base as the "before" anchor. Only the outside closure's conformance step caught it. Aggravating disclosed fact: the round carries two freezes (`corpus/claim-freezes.tsv` row `round-25` is FLAGGED for both), so a superseded attempt freeze sits in the lane where the base belongs | The Sources before→after pair is anchored at the lane-round base named in the report's own base line and at the lane tip, with the counting command naming both revisions; a superseded attempt freeze is reported in its own epoch line and never used as the "before". Shown able to fail this round: a base-anchored counter run over the committed round-25 report reads 72 at `18e7eb6d` and must exit 1 on the report's stated 74 — that report is already a red fixture; the same check over the round-26 report must compare against `a0639d8e61e486e2a716ff94cddd89a73200a02c` (78 rows) and the lane tip |

Disclosed residual for M26-1 [observation]: `R26-C1`'s `entry_ok` rule still reads a SOURCES
`opened` cell, but the row's id must also appear in the lesson's `## Gate` section, which this
round's contract fills with URL, access date, sha256 of the bytes read and a located quote — an
independent corroboration the round-25 C2 counter lacked. The cell itself is still cell-driven.

## Gates

* Lane files read-only: only this report was written. No SCORECARD / LOG / SKILL / PROVINCE /
  SHONEN / QUALITY / SOURCES / corpus / tools edit; no Git write; no `jj`; read-only `git show`,
  `git log`, `git ls-tree` only.
* No REA call (not needed for this scope), no network fetch, no tool install. Nothing to record
  under the tooling directive.
* No product code, judge, commit, push, publish, deploy or second runtime touched.

## Touched surfaces

* `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-26/w1/LessonMistakes.md` —
  this report (the only lane write).
* `/fast/scratch/hyaku/kaidoku-r26/seats/LessonMistakes/notes/collect.sh` — evidence script.
* `/fast/scratch/hyaku/kaidoku-r26/seats/LessonMistakes/notes/collect.out` — its raw output.

## Out of scope

* Writing `corpus/lessons/round-26.md` itself (L1 owns it), and any `## Gate`, `## Custody` or
  scorecard text.
* Running the round-26 counters (`tools/round-26/c1-id-identity.py`, `tools/round-26/c2-calibration.py`);
  they are other seats' subjects and the M26-1 red obligation is the L1's to discharge.
* Round-25 attempt-1 and attempt-2 artifacts beyond what the entries cite.

## Sources

Opened by ordinary local file read on 2026-10-22; sha256 of the bytes read; one located quote of
at most 25 words each.

| path (or file) | sha256 | located quote | where |
|---|---|---|---|
| `corpus/lessons/round-25-verifier-spotcheck.md` | `3d6bc116ff538843efb8556d7508c440f128096eb4788c01aeb48248bd707948` | "Wave 2 (32 attack seats, validated, `.ufo/waves/round-25/a3/w2-spec.json`) was cut by the 2 h scope freeze" | Decision, lines 19-23 |
| same | same | "Sources before→after counts from the attempt-2 freeze (`7ef837a4`, 74 rows) instead of the lane-round base." | Step-1 conformance defect 1, lines 49-52 |
| same | same | "Do not reuse them as frozen counters without fixing those paths first, with a red-before fixture." | Routed defects item 3, lines 190-192 |
| same | same | "Reports: count Sources before→after from the lane-round base, and list every lane-round commit" | Routed defects item 6, lines 198-199 |
| `.ufo/waves/round-25/a3/w1/C1Mutation.md` | `df6fbc43fb6924b6aed4b40be86c48af66f46b96da771fef37da7389911b114d` | "SCORECARD.md:23 is a decoy `\| coverage \|` row stating `108/108 knowledge files mapped`" | false accepts #4, lines 61-63 |
| same | same | "I4 never reads `corpus/README.md`: it compares the card's own N/N with the number of" | Coverage notes, lines 89-90 |
| `.ufo/waves/round-25/a3/w1/C2Mutation.md` | `4be2b903fe2dc527b7c04ca74b5831124a6d8ff8e17c2081e0bfb82fdbe3b072` | "The instrument never opens anything. It parses the `corpus/SOURCES.md` blob and tests three literal cell strings" | lines 51-52 |
| same | same | "Forging only its `opened` cell to `2026-10-22` and extending its `used-by` makes the entry \"sourced\"" | false accept #3, lines 67-70 |
| `.ufo/reports/round-25/kaidoku.md` | `ba4d9095e2a1a640232aa70707badf808d4b419a926afffdda5ba536be30cd62` | "Rows 74 → 78 (`git show <REV>:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3} \|'` at `7ef837a4` and `1e064f9b`)" | Sources & frontier, line 49 |
| same | same | "both have false accepts (`C1Mutation.md` 6, `C2Mutation.md` including \"opened\" not checked)" | Landed changes, line 19 |
| `.ufo/prompts/kaidoku-round-25.md` | `c134f584005ed86c3d87aab91d36308da150aa407856f4bf1b4006abe738ecb4` | "`SOURCES.md` rows before→after with the counting command, rows added by tier, rows touched old→new" | §4 Report contract, lines 111-114 |
| same | same | "Before → after measurements — one per claim, each with the counting command and the commit it was measured against" | §4 Report contract, lines 109-110 |
| `LOG.md` (lane) | `60dc8c45c4f6637de56d96aa91e8e1ac47a7184023f3ac82da43c729e8dd18f6` | "Wave 2 (32 attack seats, `.ufo/waves/round-25/a3/w2-spec.json`, validated) was not dispatched" | round-25 wave note, line 2960 |
| `corpus/lessons/2026-10-18-wave-dispatch-counting.md` | `83e52c33ffa686c67f635c2c71701ce85d56337592d9f675467f68a27521201f` | "Count the items array, not the intent." | Standing rules, rule 1 |
| `corpus/QUALITY.md` | `e200c853a31c00fc15ff56c6889f2bffa01a612393a4ee115188c35c4e9cbfb0` | "Retain positive control plus the intended named false accept in every red repair demonstration" | row 32, line 42 |
| `.ufo/waves/round-25/a3/w2-dispatch.json` | `50dc6536ea0deae35bfd65bdd094a7c9f5b52befb4083eb7af0cdfb9c366c65c` | `"spawn": 32, "resume": 0, "total": 32` | `counts` |
| `.ufo/waves/round-25/a3/w2/swarm-registry.json` | `ea6c2aa2fca4ef2aff830ced57b60e66c105fa8361421c82c3acc61e0da2b119` | `"C1I1I2Truth": {"kind": "spawn", "agentId": null, "role": "critic", "item": null}` | `members` |
| `.ufo/waves/round-26/claims.json` | `1137c312d9d1a4aa83ec4f7b167bcd03423de955d89ede1e53f3c6bf6bfbcb5f` | "Rows elsewhere in SCORECARD are never read (round-25 first-row false accept)." | `claims[1].rules.row_scope` |
| `corpus/lessons/round-25.md` | `cef06cbc995c47a71310d08f64a0fba299da7e00cdcbea44e7c00fdbe9b95f61` | "Shown able to fail only by the seats' finding it; no automatic check exists." | M25-9 fix cell |
| `.ufo/waves/round-25/a3/w2-spec.json` | `2316c239aa5584371d56b4cb2484c1337677456c74c33f20178670d460c890c8` | "schema" (validated wave spec; 32 attack seats, never dispatched) | file root |
| `.ufo/waves/round-25/a3/w1/swarm-registry.json` | `90c586bbdb99686f98d50ecaa352d4cf61dd1b08e9b8e4b48f3c6561c88eb499` | "kind" / "agentId" per member (65 members, 32 with `agentId` null) | `members` |

## Findings (observations, with producing command)

| finding | command | exit | UTC | output excerpt |
|---|---|---|---|---|
| SOURCES rows 72 / 74 / 78 at the round-25 base, attempt-2 freeze and lane tip; 78 at round-26 base | `for r in 18e7eb6d 7ef837a4 cce7504a a0639d8e…; do git show $r:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3} \|'; done` | 0 | 2026-10-22T12:18:12Z | `rev=18e7eb6d rows=72` / `rev=7ef837a4 rows=74` / `rev=cce7504a rows=78` / `rev=a0639d8e… rows=78` |
| round-25 wave 2 was validated with 32 attack seats and never dispatched | `python3 -c "…w2-dispatch.json['counts']…"`; `…w2/swarm-registry.json['members']…`; `ls .ufo/waves/round-25/a3/w2/` | 0 | 2026-10-22T12:18:12Z | `{"spawn": 32, "resume": 0, "total": 32}`; `members 32` / `agentId_null 32`; dir listing `swarm-registry.json` only |
| wave 1 really ran 33 seats; the wave-1 registry lists 65 members because the undispatched v2 spec shares the directory | `python3 -c "…w1/swarm-registry.json['members']…"`; `ls .ufo/waves/round-25/a3/w1/ \| grep -v swarm-registry.json \| wc -l` | 0 | 2026-10-22T12:18:12Z | `members 65` / `agentId_null 32`; `33` |
| the round-25 report itself disclosed the instrument false accepts and left them unrepaired | `grep -n "both have false accepts" .ufo/reports/round-25/kaidoku.md` | 0 | 2026-10-22T12:18:12Z | line 19: "…not repaired, because QUALITY row 33 forbids changing frozen instruments after the freeze." |
| the round-25 lesson already carries the "not yet shown able to fail" wording for unproven fixes | read `corpus/lessons/round-25.md` M25-8 / M25-9 rows | 0 | 2026-10-22T12:15Z | M25-9 fix cell ends "Shown able to fail only by the seats' finding it; no automatic check exists." |

Inferences, labelled: [inference] M26-2's class is a counting defect rather than a protocol
breach, because the spot-check itself states the attack floor is not an admission criterion and
the wave-2 dispatch was cut by an operator scope freeze, not by a lane fault.
[inference] M26-3's class is an epoch mix-up, because the lane-round base and the attempt-2
freeze are two different "before" revisions and the report used the latter.

## Artifacts (seat dir, sha256)

* `notes/collect.sh` — `d071f5b48129eb073b36ce24a523c82daad624e727a1287c587f5d5cac708be5`
* `notes/collect.out` — `e02e400863ad6043120269acba41e9e41b4c00cc3d1b940f9087955670c6c815`

No other artifact was produced; no REA run, no source fetch, no install.
