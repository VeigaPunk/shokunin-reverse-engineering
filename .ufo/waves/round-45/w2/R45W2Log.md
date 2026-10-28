# R45W2Log — attacking the round-45 `LOG.md` record

Seat `R45W2Log` (reviewer), leaf: no subagent. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
read-only. Freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`; landing
`e715263cb51b713c342ab992d527fe9d61d6f8ff`; A1 `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`;
A2 `fedd11bf5ff9fe42d061169f78d77df59af4eca1`; A3 `f59565b782c18b0eb691bec12f52d2f80d9f5032`;
tip `a63d109faa050207d4c184471889049741c9ebbf`.

**Snapshot note.** The wave-2 prompt names A1 as the measured revision. The lane moved on:
A2 (`fedd11bf`) and A3 (`f59565b7`) landed, and `LOG.md:3309-3316` records A3 as *the* measured
revision. I attacked the record as it stands at `HEAD`, i.e. with A2/A3 included; every claim below
is pinned to the revision the record pins it to.

Method: re-ran the two frozen counters (`tools/round-45/{c1,c2}-counter.py`), the
`frozen-path-preflight.py` selftest and gate, and SCORECARD recipe A (verbatim, Git objects only) at
each cited revision; re-read the wave artifacts, the controls and the lesson. Scratch
`/fast/scratch/hyaku/kaidoku-r45/R45W2Log` with `TMPDIR`/`HYAKU_SCRATCH` pointed there; receipts
copied to `receipts/`; scratch removed. No install; nothing written outside this directory.

**Headline.** The two claim numbers and every cited hash hold, byte-identically. Three sentences of
the record do not: two are numeric (`wave 2 32 seats`; "every earlier measurement … reports the same
values") and one is a routing map (`R45-CL1..CL8`). One control receipt cannot be reproduced from
the record as written.

---

## 1. Attack register

| # | attack (what it names) | verdict |
|---|---|---|
| A1 | `LOG.md:3250-3251` — C2 at `1f4b27f8`: all six registered, `unregistered []`, `thin []`, `scope_size 6`, exit 0 | **holds** |
| A2 | `LOG.md:3245-3249` — C1 at `1f4b27f8`: `rule_blocks 22`, `block22_present 1`, `block22_rows 10`, `block22_refs 7`, `unresolved []`, `preflight_selftest 11/0`, exit 0 | **holds** |
| A3 | `LOG.md:3248-3249` — C1 before-state at the freeze (`21 != 22`, `block22_present 0`) and its control receipt | **holds** |
| A4 | `LOG.md:3235-3236` — table shape `trigger \| arm \| exit \| receipt`, 10 rows | **holds** (header verbatim; 10 data rows; exit cells `1,1,1,1,2,1,2,2,0,0`) |
| A5 | `LOG.md:3235-3237` — preflight arms `commit/restored/blob/dirty/pathspec`, 11-case selftest, red case per R44-CL1/R44-CL10 item | **holds** (11 cases named; `red-dirty`, `red-dirfreeze-no-pathspec`, `red-restored` present) |
| A6 | `LOG.md:3240` + every cited hash — ancestry of `main` | **holds** (10/10 are ancestors; `--merges` over `f762b727..a63d109f` = 0) |
| A7 | `LOG.md:3239-3240` — "Frozen at `f762b727` (`plans/round-45-claims.md` + `tools/round-45/`)" | **holds** (first commit touching the claims file is `f762b727`) |
| A8 | `LOG.md:3255-3261` — Amendment A1 narrative: command A reads `21/22`, `depth_score 9.55` at `e715263c`; `22/22`, `10.0` at `1f4b27f8`; block 22 cites the `:40-66` knowledge range | **holds** (both numbers reproduced; block 22 has zero `corpus/knowledge` refs at `e715263c` and exactly that ref at `1f4b27f8`) |
| A9 | `LOG.md:3284-3286` — owned scores: coverage `138/138`, depth `21 → 22` / `22/22` / `10.0`, calibration `6 → 0` | **holds** (recipe A) |
| A10 | `LOG.md:3268-3272` — SOURCES `139 → 141`; S140/S141 tier A, opened in-round, both cited by block 22; census exit 0 at start and end | **holds** (row counts 139/139/141; both rows tier `A` with sha256s; both tokens in block 22 at every rev; census exit 0 with 14 `W04`, byte-identical stdout at freeze and tip) |
| A11 | `LOG.md:3286` — "No capability row enters. No axis is harmed." | **holds** (no capability row in the round-45 region; no axis harm at the measured revision — the `9.55` harm is disclosed in A1) |
| A12 | `LOG.md:3301-3307` — A2: `block22_refs 8`, gate clean over both frozen pathspecs, no merge in range, counters use `git log --name-only` | **holds** (8; preflight exit 0 with `touched/blob_changed/restored` empty; 0 merges; code read) |
| A13 | `LOG.md:3315-3316` — "every earlier measurement (`e715263c`, `1f4b27f8`, `fedd11bf`) reports the same values" | **FALSIFIED** → F1 |
| A14 | `LOG.md:3273-3275` — "wave 1 40 seats and wave 2 32 seats …; role mix, dead seats and per-seat outputs are read from `{r45-w1,r45-w2}-results.json`" | **FALSIFIED** → F2 |
| A15 | `LOG.md:3267` — "CL2/CL3/CL4/CL5/CL8 remain open and are routed as R45-CL1..CL8" | **unsupported as written** → F3 |
| A16 | `LOG.md:3252-3254` + `controls/ctl-c2-0-base-unevaluable.json` — the base `could_not_evaluate` receipt | **not reproducible as recorded** → F4 |
| A17 | `LOG.md:3234` — "four red arms" | **holds under one reading, ambiguous** → F5 |
| A18 | `LOG.md:3275` — "Tools installed this round: none." | **holds, limited** (no instrument can prove a negative; corroborated, uncountered) → F6 |
| A19 | `LOG.md:3270-3271` — "Assimilation `none`" | **not run** → F7 |

---

## 2. Findings

### F1 — MEDIUM — "every earlier measurement reports the same values" is false on the field it lists, and the record's own receipts say so

Phrase (`LOG.md:3315-3316`):

> A3 is the round's measured revision; every earlier measurement (`e715263c`, `1f4b27f8`, `fedd11bf`) reports the same values.

Measured (frozen counter, `--freeze f762b727`; each output byte-identical to the committed receipt of
the same name, so this is not my instrument diverging from theirs):

| rev | `block22_refs` | receipt sha256 = `l1/scores/c1-at-*.json` | command A `citation_resolved_rules` / `depth_score` |
|---|---|---|---|
| `e715263c` (landing) | **6** | `03200e3b92f01f7a03a1f19a40b1d2bd89850fa9f883db231eac7a2d56b3b590` | 21/22, **9.55** |
| `1f4b27f8` (A1) | **7** | `da9d99b4d1388e8274ef49e0735a38622308b5b411bc344f370ab8df417936de` | 22/22, 10.0 |
| `fedd11bf` (A2) | **8** | `3fa65f25351e9ed399d34431052313cc011a16d52136c07e5e550ca88a306bdf` | 22/22, 10.0 |
| `f59565b7` (A3) | **8** | `5663b064282f72215c9bbf28666a53a0dd48739d7a6166fe39560a3d072edc89` | 22/22, 10.0 |

`LOG.md:3257-3260` already states the `21/22` / `9.55` reading for `e715263c` — the A3 sentence
contradicts the A1 sentence in the same document, and the A2 paragraph cites `block22_refs 8` while
the A1 paragraph cites `7` for the earlier revision.

What does survive, narrowly: `exit 0` and `met_target true` at all four revisions (the frozen
threshold is `block22_refs >= 4`, so 6/7/8 all pass). The sentence as written is nonetheless false
for the fields it enumerates and for the depth proxy.

Fix (append-only, for both records): "…A3 is the round's measured revision. Both counters exit 0
with `met_target true` at `e715263c`, `1f4b27f8`, `fedd11bf` and A3; `block22_refs` rose 6 → 7 → 8 → 8
as block 22 acquired citations (A1 +1 knowledge ref, A2 +1 plain-form claims ref), and command A read
`citation_resolved_rules 21/22`, `depth_score 9.55` at the landing, `22/22`, `10.0` from A1 on."

Cross-reference: the same false stability sentence sits in `SCORECARD.md:3581` ("every value is
identical at both", `1f4b27f8` vs A2 — refs 7 vs 8) and `SCORECARD.md:3591` ("identical at
`e715263c`, `1f4b27f8`, `fedd11bf` and A3"). One correction has to cover all three sites.

Severity rationale: it does not change either verdict, but it is a stability claim about the exact
field the frozen predicate bounds, it is refuted by the record's own committed receipts, and it hides
that block 22 was edited (and changed the counter's output) twice after the landing.

### F2 — MEDIUM — wave-2 seat count is wrong and half its stated source does not exist

Phrase (`LOG.md:3273-3275`):

> - **Waves:** wave 1 40 seats and wave 2 32 seats under `.ufo/waves/round-45/`; role mix, dead seats and per-seat outputs are read from `{r45-w1,r45-w2}-results.json` and recorded in the fleet report.

Contradictions, each from a committed artifact:

- wave 2 is **36**, not 32: `.ufo/waves/round-45/w2-dispatch.json` `counts = {"spawn": 36, "resume": 0, "total": 36}`; `w2-spec.json` `items` = 36; `w2/swarm-registry.json` `members` = 36. All three are committed at `faa875bc` and unchanged since (`git log --oneline -- <those paths>` returns only that commit).
- `r45-w2-results.json` **does not exist** (not tracked at `HEAD`; `.ufo/waves/round-45/` holds `r45-w1-results.json` only). A present-tense "are read from" names a file that is absent.
- `r45-w1-results.json` carries **no** role or dead-seat field — its result entries have exactly `{agent, name, note, output}` and `Counter(role=None) = 40`. "Role mix" and "dead seats" are not read from it; role mix lives in `w1-dispatch.json`/`w2-dispatch.json` (`registry.members[*].role`).
- wave 1 = 40 **does** hold: `r45-w1-results.json` `seats: 40`, 40 results; `w1-dispatch.json` `counts.total: 40`, 40 registry members.

Fix: "wave 1 40 seats (`r45-w1-results.json` `seats: 40`, `w1-dispatch.json` `counts.total: 40`) and
wave 2 36 (`w2-dispatch.json` `counts.total: 36`, `w2-spec.json` 36 items); role mix from the two
dispatch registries; wave-2 results pending."

Cross-reference: `SCORECARD.md:3527-3528` carries the identical wrong count and the identical absent
citation ("Wave 1: 40 seats; wave 2: 32 seats (counts from `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json`)").

### F3 — LOW — the routed range conflates round-44 remainders with wave-1 findings

Phrase (`LOG.md:3266-3267`):

> CL2/CL3/CL4/CL5/CL8 remain open and are routed as R45-CL1..CL8.

The routed list at `corpus/lessons/round-45.md:68-105` does not support that mapping: `R45-CL1` is the
*residual* of `R44-CL1` decided this round (fleet-side placement), and `R45-CL6`, `R45-CL7`,
`R45-CL8` are labelled as wave-1 discoveries — `R45-CL6 (HIGH; wave-1 R45W1RevFreezeCommit F1)`,
`R45-CL7 (wave-1 R45W1C1CounterMutants)`, `R45-CL8 (wave-1 R45W1C2CounterMutants)`. The LOG's own A2
paragraph says the same (`LOG.md:3299`: "routed the wave-1 instrument findings as R45-CL6..R45-CL12").
So the range `R45-CL1..CL8` cannot be the routing of five round-44 remainders; at most the first five
entries carry them, and the mapping is not stated anywhere.

Fix: name the five remainders' new ids one by one, or write "the five remaining round-44 items are
routed as `R45-CL1..CL5`; `R45-CL6..CL12` are wave-1 findings". Not a number error — a reader cannot
recover which item became which.

### F4 — LOW — the base `could_not_evaluate` receipt is not reproducible as recorded and lacks every field its siblings carry

`controls/ctl-c2-0-base-unevaluable.json` is three keys:

```
{"counter": "round-45-c2", "reason": "scope file absent at rev", "verdict": "could_not_evaluate"}
```

Every sibling control is a full counter receipt with `freeze`, `rev`, `scope_size`, lists and
`met_target` (`ctl-c1-0-do-nothing.json`, `ctl-c2-0-do-nothing.json`, `ctl-c1-0-base.json`). This one
has no `freeze`, no `rev`, no `exit`, no argv, no stdout sha256.

Running the freeze-byte counter at the base under the round's own freeze does **not** produce that
reason:

- `--freeze f762b727 --rev 149133d4` → exit 2, `{"reason": "freeze is not an ancestor of rev"}`
- `--freeze 149133d4 --rev 149133d4` → exit 2, `{"reason": "scope file absent at rev"}` (the recorded text)

So the receipt is a self-referential run (freeze = rev = base) that does not say so. The LOG's
sentence ("at the base the instrument does not exist yet, so the base reads `could_not_evaluate`",
`LOG.md:3252-3254`) is true as an exit-code statement — `tools/round-45/` at the base contains only
`frozen-path-preflight.py`, so neither counter exists there — but the receipt as committed cannot be
tied to any invocation.

Fix: regenerate with `freeze`/`rev`/`exit`/argv in the body, or annotate it
`freeze = rev = 149133d4` and state the reason it demonstrates.

### F5 — INFO — "four red arms" vs five documented arms

`LOG.md:3234` says the freeze rule "becomes an instrument with four red arms". The interpreter's
docstring lists **five** arms (`commit`, `blob`, `restored`, `dirty`, `pathspec`) and the selftest has
11 cases of which 4 are green (`green-clean`, `green-dirty-without-arm`,
`green-dirfreeze-pathspec`, `green-empty-range`) and 7 red. The count is defensible only as "four arms added over the base's
commit arm": the base preflight at `149133d4` exposes `--freeze/--rev/--pathspec/--json-out` only, and
the freeze revision adds `--check-dirty`, `--require-pathspec`, `--freeze-path`, `--selftest`. Not
falsified, but a reader counting arms in block 22 sees five. Suggest "four new arms over the base's
single commit arm".

### F6 — INFO — "Tools installed this round: none." (`LOG.md:3275`)

No receipt can prove a negative of this class, so this is **unverified by instrument**. It is
corroborated: every round-45 wave-1 report that mentions installs says none (`R45W1C1CounterMutants.md:213`,
`R45W1CensusDupClass.md:3`, `R45W1PreflightDirtyReplay.md:8`, `R45W1PreflightReplay.md:12,299`,
`R45W1RegR44C1Run.md:6`, `R45W1RegScopeAudit.md:3`), and nothing in the record contradicts it. I
found no install record and made none. Scored **holds, limited**.

### F7 — "Assimilation `none`" (`LOG.md:3270-3271`) — not run

This asserts that no admitted round-45 entry cites a staged/quarantined row. Checking it needs the
round-44 quarantine set enumerated and every round-45 reference intersected with it; the census
(`sources-census.sh validate`) checks schema and duplicate URLs only (the lesson says so itself at
`corpus/lessons/round-45.md:17`), so no committed instrument answers the claim. Not run rather than
asserted: I did not reconstruct the quarantine set. What I did verify: `considerthese/` is absent and
the census is byte-identical at freeze and tip.

---

## 3. What holds, with the command that shows it

All commands run from the lane root; `TMPDIR`/`HYAKU_SCRATCH` in scratch.

| claim | command | result |
|---|---|---|
| C1 at `1f4b27f8` | `python3 -I -B tools/round-45/c1-counter.py --root . --freeze f762b727 --rev 1f4b27f8` | exit **0**; stdout sha256 `d30817c559e0949ab8500a9f04e5349db79cac5d2bb8df2d8f88f6732463a32b`; `rule_blocks 22`, `block22_present 1`, `rows 10`, `refs 7`, `unresolved []`, `cites {S140, interpreter}`, selftest `cases 11 failures 0`, `met_target true` |
| C2 at `1f4b27f8` | `python3 -I -B tools/round-45/c2-counter.py --root . --freeze f762b727 --rev 1f4b27f8` | exit **0**; stdout sha256 `2b401a9ae5a6e562178561fba15b2ae2199f019e9b1059b0b6f65175d5e4d1ca`; six registered, `unregistered []`, `thin []`, `scope_size 6` |
| C1 before, at the freeze | `… --rev f762b727 --json-out` | exit **1**; `failing` = `rule_blocks 21 != 22`, `block22_present 0 != 1`, `rows 0 < 8`, header lacks, `refs 0 < 4`; JSON sha256 `5cf74c78468785e429075d5f6b6ce98ece64debb986c64d8a47ff28e3aa57fcf` = the committed `ctl-c1-0-do-nothing.json` **byte-identically** |
| C2 before, at the freeze | `… c2-counter … --rev f762b727` | exit **1**; all six unregistered; sha256 `f61c6b997f6151ea3cd086bce9625ad6e1a27e558c5c3c74961023d705d2c630` = `ctl-c2-0-do-nothing.json` **byte-identically** |
| preflight at A2/A3, both frozen pathspecs | `frozen-path-preflight.py --freeze f762b727 --rev <A2|A3> --pathspec tools/round-45/ --pathspec plans/round-45-claims.md` | exit **0**, `verdict clean`, `touched [] blob_changed [] restored [] dirty []` at both |
| preflight selftest from the freeze bytes | `git show f762b727:tools/round-45/frozen-path-preflight.py \| … --selftest` | exit **0**; `PREFLIGHT_SELFTEST: cases=11 failures=0`; cases: `green-clean, red-touched, red-restored, red-dirty, green-dirty-without-arm, red-dirfreeze-no-pathspec, green-dirfreeze-pathspec, red-unknown-freeze, red-nonancestor, red-bulk-sweep, green-empty-range` |
| recipe A (coverage/depth) | SCORECARD §Measurement recipes A, verbatim | base & freeze: 138/138, 21 blocks/21 resolved, 10.0/10.0; `e715263c`: 22 blocks, 21, **9.55**; `1f4b27f8`/A2/A3/tip: 22, 22, 10.0; `missing []`, `dangling []` everywhere |
| ancestry of every cited hash | `git rev-parse <r>^{commit}` + `git merge-base --is-ancestor <r> main` | `f762b727, e715263c, 1f4b27f8, fedd11bf, f59565b7, 92b4970c, 1d04c6af, a63d109f` **all ancestors** (also `149133d4`, `faa875bc`) |
| freeze provenance | `git log --reverse --format=%H -- plans/round-45-claims.md \| head -1` | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` |
| no merge in the measured range (A2's premise) | `git rev-list --merges f762b727..a63d109f \| wc -l` | `0` |
| no post-freeze commit on a frozen path | `git log --name-only f762b727..a63d109f -- plans/round-45-claims.md tools/round-45` | empty |
| SOURCES rows | row count at `149133d4` / `f762b727` / `1f4b27f8` / A3 | 139 / 139 / **141** / 141; `S140`,`S141` last |
| census, round start | `receipts.log` R1 (`sources-census.sh validate --root … kaidoku`) | exit **0**, 14 `W04`, stdout sha256 `9f32a8a8…cf19`, 1518 B |
| census, round end (mine) | same command at the tip | exit **0**, 14 `W04`, stdout sha256 `9f32a8a84ef13933a0539a92a4475534aeb2ae858a407d35b176aa26662acf19`, 1518 B — **byte-identical to the round-start run** |
| capability row / axis harm | grep over `SCORECARD.md:3519-3625` | no capability row; only the two negative sentences (`:3550-3551`) |

---

## 4. Residual risk and verification gaps

- **R1.** F1/F2 are *record* defects, not claim defects: both claims are met at every revision, and
  the counters' own outputs are genuine. What is at stake is that the record's stability and
  seat-count prose is not derivable from the artifacts it points at — the next wave-1 seat that
  checks a number will find another one.
- **R2.** A3 is the measured revision but the *fleet-facing* round header (`SCORECARD.md:3525-3528`)
  still says `1f4b27f8` and 32 seats, and its amendments say A2 then A3. Three "measured revisions"
  and two counts live in one document. Append-only rules make that legal; it is not readable without
  reading to the end of the section.
- **R3.** Both counters' freeze arm uses `git log --name-only` (no merge diff). Verified true of the
  code and verified harmless for this range (0 merges), but the *claim* survives only because the
  range is linear — that is already routed as `R45-CL6`, not re-filed here.
- **R4.** Every number I produced for the counters is *the same instrument* the record used. Agreement
  is reproduction, not independent corroboration: `R45-CL13/C14` (proxy-only target) already says the
  frozen predicates are non-discriminating. I did not attempt to forge a passing artifact, so nothing
  here should be read as a discrimination test.
- **R5.** The block-22 `block22_refs` rise (6/7/8) is expected given A1/A2 edits. If the L1 changes
  block 22 again before the record is closed, `block22_refs` changes again — the receipt set must be
  re-run, not extrapolated, because `refs` is the field that moved.
- **R6.** Not run: "assimilation `none`" (F7); "tools installed: none" has no possible receipt (F6).

## 5. Receipts

`receipts/` holds every raw output cited above: `c1-<rev>.json` and `c2-<rev>.json` for
`f762b727, e715263c, 1f4b27f8, fedd11bf, f59565b7, 92b4970c, 1d04c6af, a63d109f`, the literal LOG
commands (`logcmd-c1.out`, `logcmd-c2.out`), the preflight runs (`pf-A2.json`, `pf-A3.json`), the base
controls (`c2-base-self.json` = freeze=rev=base, `c2-base-roundfreeze.out` = freeze=`f762b727`),
and the round-end census (`census-now.out`). All captured 2026-10-28T16:03Z–16:05Z UTC.

Installations recorded this seat: **none**.
