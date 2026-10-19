# EX-45 — needle-quality review of the new arc3-era entries (chain c3)

Seat EX-45 · chain c3 · role executor (review) · wave `arc3-loop1-round3` ·
2026-10-19 · repo `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

Reviewed revision: the landed artifact pair at worktree, HEAD (committed) =
`c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`. Identities re-derived at
2026-10-19T13:16:03Z (rule #14 — every value below re-measured, none carried):

| artifact | bytes | sha256 |
|---|---|---|
| `.ufo/gates/citation-drift/pointer-table.json` (landed) | 30,348 | `bfc42f1bb131cbe3a972a16647d24b1f16d936083dd61496589540e791d58bb7` |
| `.ufo/gates/citation-drift/expected.json` (landed) | 2,154 | `d97dd60a942eaf53771c8224e84a9e8cdaf976dc66c3a543a450b1f1fa3827e2` |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | — | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` |
| base table at HEAD (`git show HEAD:…`) | 14,694 | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` |

The landed `expected.json` pins `bfc42f1b…` (derived == pinned, checked twice:
before and after EX-41's final `expected.json` rewrite; the rewrite moved only
the pin value — `git diff` shows the single line, old `738b3a56…` → new
`bfc42f1b…`, `selftest`/`snapshots`/`frozen_run` untouched).

Review target: **the 26 entries and 5 `exempt` rows added by this round**
(31 → 57 entries; quoted unchanged at 4; exempt 3 → 8). Pure addition verified
mechanically: 0 removed, 0 changed (`/var/tmp/ex45/review/` diff of
`git show HEAD:` table vs worktree; also EX-41 `05-identity-and-diff.txt`).

## 1. Work performed (evidence pointers)

Every transcript in `claims/c3/EX-45/evidence/`; harness scripts in
`evidence/scripts/`. All runs read-only against the repo; all mutation ran in
isolated fixture Git repos under `/var/tmp/ex45-*` (never `/tmp`).

- **Landed-table resolution audit** — `needle-review.py --table pointer-table.json`
  (probe-identical Git-object resolution, plus anchoring/boundedness extras):
  `evidence/landed-audit.txt` + `landed-audit.json`; **61/61 needles live**
  (57 entries + 4 quoted), NOT-LIVE = 0.
- **Probe modes at HEAD (post-landing)** — default `reported findings=0 exit=0`;
  `--strict` `clean findings=0 exit=0`; `--selftest` (disk-backed
  `TMPDIR=/var/tmp/ex45`) `CLEAN cases=13 passed=13 failed=0 exit=0`.
- **Citing-side mutation battery** — `attack-battery.py`, one isolated fixture
  per needle (only the files that needle cites), control run first:
  `evidence/landed-battery.txt` (61 controls clean; every mutation red).
- **Target-side neuter battery** — `target-mutation.py`, sentinel replaces every
  `must_match` occurrence in the target: `evidence/landed-tmut.txt` —
  **14/14 new `extracted` entries NON-VACUOUS**; plus the form-insensitivity
  demonstration for `sc-arc3r2-cites-shonen` (below).
- **Endpoint-drift (slack) measurement** — `slack.py`: `evidence/landed-slack.txt`
  for the landed pair; `evidence/base-slack-clean.txt` for the 31-entry base.
- **Post-landing coupling simulation** — `sim-landing.py`: a scratch Git repo
  built from the WORKTREE bytes of all 26 files the table cites (including C2's
  revised `custody-pair/README.md` and `custody-pair.py`), committed, probed:
  `evidence/sim-landing.txt` — **clean in both modes** (so the new anchors into
  the custody README survive C2's same-round revision as of that revision).
- **Baseline (pre-landing) audit** — 35/35 needles live at HEAD:
  `evidence/baseline-audit.json`, `evidence/base-battery-clean.txt`,
  `evidence/range-slack.txt`; extension review of EX-43's scratch table
  (digest re-derived = its own `0b01f521…` claim):
  `evidence/ext-audit.json`, `ext-battery-v2.txt`, `ext-slack-v2.txt`.

## 2. Review criteria and how each was measured

1. **`must_match` actually matches at HEAD** — resolved exactly as the probe
   does (`git show <rev>:<file>`, `re.search` on the pinned line / target blob),
   entry by entry; not inferred from a green probe run alone.
2. **Patterns bounded** — static audit of every new `pattern`: capture groups
   must be digits-only, must sit inside literal context (filename + separator),
   and must not tolerate over-broad wildcards (`.*`, `.+`, `\w*`, `\s*`).
   Measured also as **multiplicity**: the number of matches the pattern yields
   on its pinned citing line (a second match would let the extractor read the
   wrong number).
3. **Line anchors correct** — pinned line number valid and matching at HEAD;
   plus two quality extras the probe does not grade: (a) **in-file hit
   multiplicity** of the needle (duplicate text = ambiguity), and (b)
   **endpoint-drift slack** for range-form entries — the interval of `d` for
   which a renumbered citation `lo+d…hi+d` still probes green, measured
   empirically at the boundary in a fixture.
4. **Non-vacuity** (added, per the wave's rule that an unrun check has not
   passed): each needle must actually redden when its subject moves — citing-side
   wrong-number, target-side neuter, anchor deletion, 1-line shift.

## 3. Results — the 26 new entries

All 26: `must_match` live at HEAD; no unbounded wildcard anywhere; every new
`pattern` is digits-only and literal-anchored with **multiplicity 1** on its
citing line (10 of the 14 patterns capture a range `(\d+)-(\d+)`; the other 4 a
single number). All 26 redden under mutation. Line anchors: every pinned line
matches at HEAD; the 10 new anchors are deliberately unpinned with in-file hit
multiplicity 1, except `custody-readme-v2-fieldset` (hits `[46, 67]` — both hits
are the v2 labeled-render convention; content-anywhere semantics, correct for an
anchor).

Endpoint-drift slack of the 14 new `extracted` entries (empirical boundary:
`d` green, `d+1` red unless noted):

| entry | stated | target lines | must_match hits | slack | first red |
|---|---|---|---|---|---|
| `arc3r1-entry-r3-offsets` | 149-155 | 155 | [152] | 0 (`d+1` = out-of-range, EOF-bound) | +1 |
| `arc3r1-entry-r3-stub-mutability` | 59-70 | 155 | [66] | **+7** | +8 |
| `arc3r1-entry-quality-ids` | 24-25 | 36 | [24] | 0 | +1 |
| `arc3r1-entry-quality-11` | 21-21 | 36 | [21] | 0 | +1 |
| `arc3r1-entry-r3-hypothesis` | 44-45 | 155 | [45] | +1 | +2 |
| `arc3r1-entry-r3-cli-quirk` | 93-96 | 155 | [93] | 0 | +1 |
| `skill-rule14-entry-recheck` | 7-7 | 33 | [7] | 0 | +1 |
| `skill-rule14-cr2-identity` | 86-89 | 247 | [86] | 0 | +1 |
| `skill-rule14-verdict-identities` | 149-153 | 207 | [150] | +1 | +2 |
| `skill-rule14-log-fresh-identity` | 1411-1412 | 1455 | [1412] | +1 | +2 |
| `sc-arc3r2-cites-shonen` | 6-6 | 12 | [6] | 0 | +1 |
| `census-cites-sc-e22-debt` | 850-852 | 1496 | [851] | +1 | +2 |
| `census-cites-sc-laundering-refusal` | 908-908 | 1496 | [908] | 0 | +1 |
| `census-cites-sc-round4-range` | 856-1336 | 1496 | [857] | +1 | +2 |

Verdict on slack: these are **containment anchors**, not endpoint pins — a range
is green while it still contains its needle, so the slack equals the distance from
range start (or end) to the nearest needle hit. Slack ≤ 7 lines for 13 of 14; the
481-line `census-cites-sc-round4-range` is slack +1 only because its needle
`^## arc2-loop1-round4` occurs exactly once (`SCORECARD.md:857`, verified), and
its note already says the span is a scope declaration graded at its start
(accurate). The one note that would overstate its needle is **pre-existing**:
`readme175-sc1217` says the citation "must land on the retirement line, not
merely somewhere in the file", but `rerun id-stability` occurs on **6** SCORECARD
lines (`1121, 1155, 1216, 1266, 1282, 1318`); measured slack **+102** (a
renumbering to `SCORECARD.md:1318` still probes clean). Proposed patch:
`proposed-tighten-sc1217.patch.md` (below).

Designed insensitivity of `sc-arc3r2-cites-shonen` — demonstrated, not asserted
(`evidence/landed-tmut.txt`): range-end refresh `81-255` → `81-399` **green**;
count refresh `14/14` → `15/15` **green**; wording break `craft section` →
`craft area` **red**. The note's claim (it pins the FORM, not the values) is
accurate; the count is graded by command A instead, per the census dispositions.

New `exempt` rows (5) spot-checked against the tree: the "measured stale"
example holds (`SKILL.md:371` = `## Refuses`, verified), `corpus/README.md:38`
still the EVM map row, `SCORECARD.md:857` = `## arc2-loop1-round4 …`, and the
append-convention the section-key pins rely on is re-verified from history: the
r1/r2 records commits change SCORECARD.md and LOG.md by pure insertion at EOF
(`c07af80`: +79 lines at 1415; `14b1682`: +81 at 1334; LOG +25 at 1428) — 0
deletions, so `:1338`, `:1419` and `LOG.md:1411-1412` cannot move when the
round-3 records are appended.

## 4. Attacks/refutations attempted, with verdicts

| # | attack | result | verdict |
|---|---|---|---|
| A1 | base table probe, both modes, at HEAD | 0 findings, exit 0; selftest 13/13 | needle set green before the round |
| A2 | landed table probe, both modes, at HEAD (re-run after the final `expected.json` rewrite) | 0 findings; 13/13 | claim's "findings = 0" holds on landed bytes |
| A3 | resolution audit, 61 needles, not trusting the probe | 61/61 live | needles resolve; no dead/ambiguous entry |
| A4 | isolated-fixture control per needle (61) | 61/61 clean | no fixture artifact masks a red |
| A5 | citing-side wrong-number, span-precise (14 new extracted) | all red; 4 needed +99999 (needle mid-range, containment) | NON-VACUOUS; the +99999 need is the slack property, not blindness |
| A6 | target-side neuter, all `must_match` occurrences (14 new extracted) | 14/14 `citation_dead` | NON-VACUOUS from the target side |
| A7 | 1-line insertion above the pin (2 new `exact`, all `exact`/`quoted` at large) | all red | line pins are load-bearing |
| A8 | anchor deletion (10 new + 7 pre-existing anchors) | all red | anchors are content load-bearing |
| A9 | renumbered range boundary, per entry (14 new) | table in §3 | slack quantified; notes accurate except `sc1217` (pre-existing) |
| A10 | form-pin insensitivity (`sc-arc3r2-cites-shonen`) | green/green/red as designed | matches its note |
| A11 | post-landing worktree simulation (26 files, incl. C2's revised custody README/tool) | clean both modes | new README anchors survive C2's revision so far |
| A12 | exemption-ledger fact checks (3 spot rows) + append-convention re-derivation | all hold | exempt causes are measured |

Refutation attempted and **rejected**: "the short needles are over-broad".
Measured: `JUMPDEST` occurs **once** in its whole target
(`corpus/knowledge/2026-10-13-r3-evm-interface.md:152`), `content-addressed`
once in `QUALITY.md` (`:24`); every new needle's in-blob hit is unique. Short ≠
ambiguous here.

Refutation attempted and **upheld (pre-existing entry)**: `readme175-sc1217`'s
note overstates its needle's specificity; measured counterexample and slack in
§3. Its `must_match` is a 3-word phrase, not a unique one.

## 5. Proposed changes

`claims/c3/EX-45/proposed-tighten-sc1217.patch.md` — a FUTURE-round patch
(landing it requires the F3 re-pin of `expected.json` in the same commit; this
round's pair is already landed and pinned, so it is deliberately NOT applied
now): tighten `readme175-sc1217`'s `must_match` from `rerun id-stability` to
`pre-fall wall text \(R2 — next README-touching round\); rerun id-stability\.`
(measured unique in SCORECARD.md: `grep -c` = 1, at `:1216`), and correct the
entry's note to state containment semantics instead of "must land on the
retirement line". No other changes proposed: the 26 new entries pass every
criterion of §2 as landed.

## 6. Blockers and watch items

- **No blockers** for the review; every measurement above is first-hand.
- **Watch (cross-chain coupling, for the records commit).** The table now pins
  C2-owned surfaces with exact phrases: `skill-registry-custody-pair-row`
  (`precedence CONTENT-DRIFT > ABSENT > REWRITE-DRIFT > METADATA-DRIFT > MATCH`),
  the four `custody-readme-*` anchors, and `skill-registry-citation-drift-row`
  (`frozen-run preflight`). C2's round-3 claim revises the custody row/README in
  the same commit; if any pinned phrase is reworded, the probe reports findings
  and C3's "findings = 0 at the work commit" is falsified. My `sim-landing` run
  covers the revision as of 13:16Z; it must be re-run against the final C2/C1
  landing (or a re-pin/re-needle decision taken) before the records commit.
  C1's line-neutral map token is safe by construction (`readme38-arc3r1-token`
  is an anchor, no line pin).
- **Watch (round-3 records).** SCORECARD.md/LOG.md appends at EOF are verified
  safe for the section-key and LOG pins; a records rewrite ABOVE the pinned
  lines would redden them (append convention is the load-bearing assumption).