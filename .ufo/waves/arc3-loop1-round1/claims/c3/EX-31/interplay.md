# EX-31 — instrument-interplay check: census scope re-key vs citation-drift needles

Seat EX-31 · chain c3 · role executor · wave arc3-loop1-round1 · 2026-10-19.
Task (seat line): after EX-28's census edit lands, run the citation-drift probe —
its pinned needles must NOT have been staled by the census scope re-key
(findings=0); analyze why/why not.

Frozen prediction (from the r10 readme175-sc1217 lesson, `SCORECARD.md:1297-1303`):
an edit landing in one instrument's surface can stale another instrument's
pinned needles in the same commit (r10: README:175's `SCORECARD.md:1217→:1216`
re-point vs the probe's `must_match`; caught in-round). This round's prediction:
the census re-key's edit surface is the instrument file itself, so the probe's
needles cannot be staled — and the check must be shown to have teeth, not to
pass vacuously.

## 0. Verdict

**Both edits landed and the prediction holds on the actual bytes.** EX-28's
census edit (`6f1d19ff…`, +65 lines: header disposition stanza, a real scope-row
re-key, new G18 assertion) and EX-16's probe edit (`e2665074…` + `expected.json`
`ff47bfd6…`: frozen-run guard, selftest 11→13) are both in the worktree. With
them landed, at HEAD `e845c2b`:

- probe (probe semantics): `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`
- probe `--strict`: `clean findings=0 exit=0`
- probe `--selftest`: `cases=13 passed=13 failed=0 exit=0`
- census v10: `VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, exit 0

Records-commit simulation in a scratch clone with the landed bytes committed
(`a53a8e8`), plus the round's SCORECARD records draft appended (`5b7b53b`):
probe `findings=0` in both modes and census `PASS 0/0/0/0` at both commits.
Structural reason: the 17-file needle-target set and the census edit surface
(`.ufo/gates/c1-census-v10.py` only) are disjoint by construction, and the probe
grades Git objects at `--rev`, not the worktree. Teeth test against the *new*
probe: a one-line insertion into SCORECARD.md fires 9 findings — including the
r10 lesson's own `readme175-sc1217`. The check is not vacuous.

## 1. Instrument state pinned (sha256)

| file | pre-landing (this seat's baseline) | landed (final, measured) |
|---|---|---|
| `.ufo/gates/c1-census-v10.py` | `36e96cd59b62…` (mtime 10-18 20:31) | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` (mtime 10-19 07:18 local) |
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `3067621ac44d…` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` |
| `.ufo/gates/citation-drift/pointer-table.json` | `738b3a569fb7…` | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` (unchanged) |
| `.ufo/gates/citation-drift/expected.json` | `4e28ba908bcd…` | `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` |

Landed-state capture: `claims/c3/EX-31/landed-state.txt` (HEAD, sha256s, git
status/diff). EX-28's edit diff: `claims/c3/EX-31/ex28-census.diff`; EX-16's:
`claims/c3/EX-31/ex16-gate.diff`. Whole-tree `git diff --stat HEAD` touches only
the three gate files (+ an unrelated pre-existing `arc2-round10/C3.md` worktree
modification, present since this seat's first `git status` — not this wave's
gate work): PROVINCE.md, SCORECARD.md, SKILL.md, corpus/README.md are untouched.

## 2. Before — probe at HEAD, pre-landing baseline

```
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py          → reported findings=0 exit=0
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --strict → clean findings=0 exit=0
```

Reproduced byte-faithfully in a scratch clone at `e845c2b` (identical gate-file
sha256s). Scratch root `/var/tmp/ex31` (`/tmp` is quota-exhausted for this user —
the standing hazard, `SCORECARD.md:990-991`; same relocation as EX-20/PL-3/SC-7).

## 3. Needle-target set vs census edit surface (the static reason)

Extracted programmatically from `pointer-table.json` (entries + quoted), 17
distinct target files (`claims/c3/EX-31/needle-targets.txt`):

```
.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt
.ufo/waves/arc2-loop1-round8/E2.md
.ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json
LOG.md  PROVINCE.md  SCORECARD.md  SHONEN.md  SKILL.md
corpus/QUALITY.md  corpus/README.md  corpus/lessons/2026-10-15-round-1.md
corpus/knowledge/2026-10-13-mcp-registrations.md
corpus/knowledge/2026-10-13-r4-12-godot-arm64-scale.md
corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md
corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md
corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md
evidence/round-1-2026-10-15/rea-bundle.json
```

Census edit surface (EX-28's write target, per the frozen rules, confirmed by
the landed diff): exactly `.ufo/gates/c1-census-v10.py`. **Intersection:
EMPTY.** No needle reads the census file. Note the sharp form of this: the
landed re-key *names* `PROVINCE.md` line 45 in its SCOPE metadata
(`c1-census-v10.py:144`) — but it edits the instrument's own table, not
PROVINCE.md (worktree diff confirms PROVINCE.md byte-unchanged), so the
probe's `prov18-*` pins on PROVINCE.md:18 cannot move.

## 4. EX-28's landed edit (actual bytes, not the draft)

`ex28-census.diff` (+65/−1): (a) a 44-line header disposition stanza
(`c1-census-v10.py:1-44`); (b) the scope-row re-key
`("PROVINCE.md", 45, 62, "DATED", 40, r"verified on this host 2026-10-13")` →
`("PROVINCE.md", 45, 62, "DATED", 45, r"2026-10-13")` (`:144`) — the old row
dated itself by a line outside its own range; (c) new assertion G18
(marker line must lie inside its own range; `assert_markers` at `:255`, check at
`:263-267`). The edit is therefore *more* than the drafted header note — a real
scope re-key plus a new guard class — and still confined to the census file.
EX-28's own capture (`claims/c3/EX-28/census-at-HEAD-after.txt`) ends
`VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`; this seat
re-ran it independently (`claims/c3/EX-31/census-head-quiet.txt`,
`census-head-verbose.txt`) with the same result.

## 5. After — landed state and records-commit simulation

**Landed state, real repo** (files: `probe-head-probe-mode.txt`,
`probe-head-strict.txt`, `probe-selftest.txt`):

```
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py          → reported findings=0 exit=0
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --strict → clean findings=0 exit=0
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest
  → cases=13 passed=13 failed=0 exit=0
$ python3 .ufo/gates/c1-census-v10.py --quiet → VERDICT: PASS  (stale=0 …), exit 0
```

**Records-commit simulation** (scratch clone, commits `a53a8e8` → `5b7b53b`):

- `a53a8e8` = landed census + probe + expected committed (the diff-file-list is
  exactly those three paths).
  `probe → reported findings=0 exit=0`; `--strict → clean findings=0 exit=0`;
  census on the clone tree → `PASS 0/0/0/0` (`records-sim2a-probe.txt`).
- `5b7b53b` = + SC-7's drafted SCORECARD records section appended (3298 bytes;
  clone SCORECARD 1336 → 1387 lines).
  `probe → reported findings=0 exit=0`; `--strict → clean findings=0 exit=0`;
  census → `PASS 0/0/0/0` (`records-sim2b-probe.txt`, `records-sim2b-census.txt`).

## 6. Teeth — would this check have caught the r10-class defect?

Counterfactual in the clone (then reverted), **against the new probe** (guard
active): `teeth-new-probe.txt`.

- **T1 — one line inserted at the top of SCORECARD.md** (simulates a re-key that
  edits a pinned surface): **9 findings** — `citation_dead` on
  `sc59-stanza-key-anchor`, `sc59-receipt-stamp`, `sc68-discharge-record`,
  `sc69-readme-177`, `sc72-readme-nitrow`, `sc270-dated-record`,
  `sc698-sc2-refuted-record`, `readme175-sc1217`, `sc622-capability-r8`. The r10
  lesson's own needle (`readme175-sc1217`) is among them.
- **T2 — one line appended at EOF of SCORECARD.md**: `findings=0`. Append-only
  growth cannot move pins; insertion/removal can.
- **T3 — C1's README primary variant** (`claims/c1/EX-13/README.primary.md`,
  sha256 `b74b8d34…`) applied: single-line in-place replacement at README:38;
  190 lines both sides (line-neutral); `findings=0` — the needles on
  README:22/:175 and the `readme175-sc1217` extraction are untouched.

## 7. Why the needles were not staled — four isolation channels

1. **Target-set disjointness** (§3): the census edit surface is not in the
   needle-target set; nothing pins the census file, so nothing can go stale
   there.
2. **Line-shift isolation**: needle staleness requires an edit *inside a pinned
   file* at or before a pinned line (T1 is the positive control). The re-key
   moves line numbers only inside `c1-census-v10.py` (header/SCOPE/assert);
   every pinned line (SCORECARD :59/:60/:68/:69/:72/:270/:622/:699,
   PROVINCE :18, README :22/:175, …) is unaffected — PROVINCE.md itself is
   byte-unchanged.
3. **Read-path isolation**: the probe resolves targets as Git objects at
   `--rev` (`citation-drift-probe.py:100` `git_show`, `:125` `Tree.lines`;
   default `--rev HEAD` at `:477`). Seats never commit, so a worktree-level
   census edit is *invisible* to a probe run at HEAD — which makes the literal
   pre-integration run trivially green by construction (honest limitation of
   the task wording); §5's records-commit simulation is where the edit becomes
   a graded object, and it still yields findings=0.
4. **Append-safety asymmetry (mirror image)**: the records commit appends the
   round section at SCORECARD EOF; appends are needle-safe (T2). The *census*
   is the instrument that is NOT append-tolerant by construction: its
   fixed-bound posture means the uncovered tail must stay locus-free or the
   bound must be re-keyed in the same commit (`c1-census-v10.py:139-161` SCOPE;
   EX-28's landed stanza states the standing rule; PL-3 plan §4-5 attacks
   A2/A4/A5c; SC-6 fixtures; SC-7 records-tree simulation). The round's real
   coupling risk therefore runs the *other* direction: a records append could
   trip the census (SCORECARD tail), not the census edit staling the probe.
   This is the r10 lesson's mirror image, and it is owned by the census chain,
   not by the probe.

## 8. Adjacency (round-level, measured cheaply — not this chain's claim)

The other edits that touch needle-target files: C1's README edit (in-place,
line-neutral; T3 findings=0) and C2's SKILL.md registry-row rewrite (EX-20 §7:
line-neutral 371→371; the probe's only SKILL.md entries are
`skill-registry-row` — an anchor with no `pin_line`, `pointer-table.json:107-110`
— and `shonen-skill-range`'s range 81-243, which does not contain :371). The
r10-class hazard would be (a) any line insertion/removal in a pinned file at or
before a pin, or (b) a re-point of README:175's `SCORECARD.md:NNNN` citation.
No landed or planned edit in this round does either; the parent's records commit
should keep this invariant (verified again by the probe re-run C2's claim
requires).

## 9. Attacks / refutations attempted

- **A1 "the check is vacuous — the probe passes anything"** — REFUTED by T1
  (9 findings on a 1-line insertion, r10 needle included) and by the selftest
  (13/13 committed cases, `expected.json` `selftest` table).
- **A2 "the round's edit shape is append; appends could still stale the
  README:175 extraction"** — REFUTED for the drafted text and C1's variant:
  T2 (append → 0 findings) + T3 (C1's README edit leaves :175 byte-identical).
- **A3 "the census stanza is a big header insert and might shift something the
  probe reads"** — REFUTED: the insert and the row re-key are inside the census
  file; landed state and both sim commits yield 0 findings.
- **A4 "run-the-probe-after-EX-28 is trivially green and proves nothing"** —
  PARTIALLY TRUE, accepted and handled: the git-object read path (§7.3) makes
  the literal pre-integration run insensitive to worktree edits; the check is
  made meaningful by the records-commit simulation (§5). The gap is named, not
  papered over.
- **A5 "C2's frozen-run guard (EX-16) would invalidate these numbers"** —
  REFUTED in the landed state: the guard is live (selftest 13/13) and the
  landed probe still reports findings=0 both modes; the guard grades the
  *table*, whose sha256 is unchanged (`738b3a56…`), so census↔needle
  disjointness is untouched. The parent's records-commit re-run (C2's claim)
  supersedes §5's numbers if any gate file changes again.
- **A6 "EX-28 might land a row addition rather than a header note — would that
  change the answer?"** — ANSWERED on actual bytes: EX-28 landed *both* (header
  stanza + row re-key + G18). Both forms edit only `c1-census-v10.py`; result
  unchanged (§4/§5).
- **A7 "the re-key's new marker regex (`2026-10-13` at PROVINCE.md:45) might
  interact with the probe's PROVINCE needles"** — REFUTED: the probe pins
  PROVINCE.md:18 content (`prov18-stamp-named`, `prov18-receipt-exists`,
  `prov18-pin-value`); PROVINCE.md is byte-unchanged; probe 0 findings.

## 10. Residuals / gaps for the parent

- EX-16 and EX-28 have **not written seat reports** (`seats/EX-16.md`,
  `seats/EX-28.md` absent as of this seat's last poll, 10:2x UTC; EX-28's
  evidence file `claims/c3/EX-28/census-at-HEAD-after.txt` and EX-16's artifact
  set are present). Not this seat's to write — flagged for the chain close.
- **The records-commit probe re-run remains mandatory at integration** (C2's
  claim; also the actual committed records text may differ from SC-7's draft —
  re-grade it; if C1's final README edit differs from `README.primary.md` in any
  line ≤175, re-run the T3 shape before sealing).
- EX-16's guard adds the invariant: **any later edit to `pointer-table.json`
  must re-pin its digest in `expected.json` in the same commit** — the records
  commit must not edit the table, or it must re-pin.
- Scratch `/var/tmp/ex31` removed at seat close; all quoted outputs are
  committed under `claims/c3/EX-31/`.
