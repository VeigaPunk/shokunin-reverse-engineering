# R38W2MistakeHunt — unmined round-38 mistakes (both attempts)

**DEFECTS FOUND** — three defects plus one stray file survive at the current landing `7a1ac7fe` (the
suite's sixth group, `G`, is the documented id-space overlap treated as calibration in §5); six further defects existed at the
landings named in my brief (`3b960fe5`, `0fc61133`) and were closed by `7a1ac7fe` **during** this review
(07:13:36Z). **The author verdicts are not falsified**: the first-freeze C1 rule gives
`carriers_matched 3 / exit 1` at `3b960fe5` *and* at `7a1ac7fe`, and the frozen C2 counter gives
`mismatches 0 / exit 0` at `0fc61133` *and* at `7a1ac7fe`, on runs I made from frozen bytes.

Seat `R38W2MistakeHunt`, leaf, advisory. Judged on coverage, calibration. Read-only over the lane
(`show`/`ls-tree`/`ls-files`/`archive`/`cat-file`), the read-only assimilation package, and one live
`curl`; no REA invocation, no VCS mutation in the lane, no writes outside this report and
`.ufo/waves/round-38/w2/artifacts/R38W2MistakeHunt/`. No tool installed. Scratch removed.

---

## 0. The verdicts under attack reproduce

| check | command (abridged) | result |
|---|---|---|
| first-freeze C1 rule @ `3b960fe5` | `git archive e059ca93 → $S/treefreeze`; `$S/treefreeze/tools/round-38/c1-counter.py --root <lane> --rev 3b960fe5… --freeze e059ca93… --pkg65 <rea-agents 6.5.0 root>` | `carriers_matched 3`, `met_target false`, exit 1; keys identical to the committed `l1/scores/c1-v1-at-3b960fe5.json` (`receipt-frozen-v1-counter-at-3b960fe5.json`) |
| first-freeze C1 rule @ `7a1ac7fe` | `tools/round-38/c1-counter.py … --rev 7a1ac7fe…` (the path now ships the freeze blob, sha `a7a62b09…` = `git show e059ca93:…`) | `carriers_matched 3`, `met_target false`, exit 1 (`receipt-frozen-v1-at-7a1ac7fe.json`) — verdict stable across both landings |
| freeze counter selftest | `c1-counter.py --selftest --pkg65 …` at freeze bytes | `{"cases": 15, "green_ok": 1, "red_ok": 14, "failures": []}`, exit 0 |
| v2 counter selftest | same at `79f69347` (`git archive`) | `{"cases": 18, "green_ok": 1, "red_ok": 17, "failures": []}`, exit 0 — the commit message's "selftests 18/18" holds |
| C2 rule | `c2-counter.py --root <lane> --rev 0fc61133… / 7a1ac7fe… --base 77091b49…` | `mismatches 0`, `guards_ok true`, `met_target true`, exit 0 at both revisions (`receipt-c2-repro-at-0fc61133.json`, `receipt-c2-repro-at-7a1ac7fe.json`) |
| QUALITY 79 gate | `freeze-drift.py --root <lane> --freeze e059ca93… --rev 7a1ac7fe…` | `verdict: drift`, exit 1, `net_changed: []`, `ships_freeze_bytes: true` |
| C2 repair is genuine, not a stub | `git show 0fc61133:PROVINCE.md` row `REA MCP server` names `.ufo/waves/round-19/evidence/doctor/`; both `doctor-6.5.0.txt` / `doctor-6.7.0.txt` exist at base `77091b49` with unchanged blobs | the counter is non-discriminating (a stub also scores 0 — now disclosed in the landed SCORECARD row), but the *repair itself* is real |

Calibration on the C1 score: bindings at the measured revision are `coverage_map_row true,
entry_present true, frontier_note true, sourced true, province_core_row false, province_core_section false`.
`frontier_note` was already true at the **base** (wave-1 `R38ReviewerPredicateIdentity` D1), so the C1
verdict rests on `carriers_matched` alone. The landed SCORECARD wording ("Core-row bindings false") is
accurate; it does not claim the pre-satisfied binding.

---

## 1. Residual defects at the current landing `7a1ac7fe`

The suite that produces these numbers is `checks.py` (`checks-run-landing-7a1ac7fe.txt`): A 0, **B 4**,
C 0, **D 2**, E 0, F 0, G 6, H 0 → exit 1. Each fix below is a check that fails on the landing and passes on
a corrected fixture (`fixture-proof.txt`).

### R1 — MED — the frozen instrument map still misdescribes itself and reaches outside the lane

- **Class**: false statement in a frozen artifact; lane-external dependency in a frozen instrument list.
- **Evidence**: `.ufo/waves/round-38/instruments.json` is byte-identical at `e059ca93` and `7a1ac7fe`:
  `"frozen_at_commit": "{{FREEZE}}"` (line 4, unsubstituted template), and the note "Every instrument
  below is committed at the freeze commit" is false for `c1_receipts`
  (`corpus/evidence/round-38/c1/K*/after.json`, absent at the freeze by design), `controls_dir`
  (`.ufo/waves/round-38/controls`, lands at `efd5c47a`), and `census_script`
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh` — an absolute **fleet-repo** path; the lane has
  no `scripts/` at any round-38 commit). The freeze-drift gate's default path set does not include this
  file, so the round's own gate cannot see the placeholder.
- **Captured-by**: none by a criterion; wave-1 `R38ReviewerPredicateIdentity.md:104-105` and wave-2
  `R38W2FreezeDriftFixtures.md` §4 report it, the latter under "Calibration notes (not defects)".
  `grep -n 'instruments.json\|frozen_at_commit' corpus/lessons/round-38.md` → no hit at `7a1ac7fe`.
- **Fix**: substitute the freeze sha; add a `phases` map (`frozen` / `claim_data` / `post_freeze`); vendor
  the census script into `tools/round-38/` or drop the row. Check B (glob- and phase-aware).
- **Shown able to fail**: B = 4 findings on the landing; a fixture with the map repaired (freeze sha, phases
  declared, census script vendored, all other instruments present) → 0.

### R2 — MED — QUALITY 79's text and the final landing's own gate disagree, and the field that lets the landing pass is not in the criterion

- **Class**: contract/receipt mismatch — the round's newest criterion is violated by the round's final
  landing, adjudicated by a field the criterion does not mention.
- **Evidence**: `corpus/QUALITY.md:87` (unchanged at `7a1ac7fe`) still requires that the gate "must print
  zero commits". At `7a1ac7fe` the gate prints drift (exit 1; commits `79f69347`, `f1010f67`), with
  `net_changed: []` and `ships_freeze_bytes: true` — a field `7a1ac7fe` added to
  `tools/round-38/freeze-drift.py` (the diff adds `net_changed` + `ships_freeze_bytes` and a `git log`
  failure branch that returns `unevaluable`). The drift list has **three** entries at the final landing,
  the third being `7a1ac7fe` itself (the restore touches both kill-rule paths), so "print zero commits" is
  structurally unreachable for any round that amends and then restores. The lesson's M38-9 states "the commit list stays non-empty, because
  the history is not r[e-writable]" — i.e. the round knows the literal clause cannot hold, but the clause
  was not amended, so a future verifier following QUALITY 79 literally must reject the landing.
- **Captured-by**: none by a criterion; M38-9 (recorded at `7a1ac7fe`) states the history part but not the
  text/verdict mismatch.
- **Fix**: amend QUALITY 79 to the two-part test — `exit 0`, **or** `exit 1` with `net_changed: []` and
  `ships_freeze_bytes: true` as an explicit restore, with the gate's own blob id in the instrument map
  (`freeze-drift.py` is itself unfrozen: it changed again in `7a1ac7fe`). Check: criterion text contains the
  field, and the gate's output at the landing satisfies one branch.
- **Shown able to fail**: the check on the current text/gate pair → mismatch (exit 1, but criterion demands
  exit 0); on the amended criterion in a fixture → pass. The gate's output is quoted above and is
  reproducible with one command.

### R3 — LOW — the two duplicate rows do not tell a reader they describe the same documents as S108 / S110

- **Class**: registry hygiene / unlinked duplicate authority.
- **Evidence**: `corpus/SOURCES.md` at `7a1ac7fe`: `S108` and `S112` share the same URL, tag
  `1fcc7a0a…`, digest `2d7b901b…9287` and opened date; `S110` and `S117` share URL and digest
  `6544d60f…3716`. Neither `S112` nor `S117` carries `supersedes S…` or any `S108`/`S110` mention in
  `teaches`; the explanation lives only in the lesson ("S112 stays: the registry is append-only…",
  "S117 = new scope row on the document S110 holds"). The lane's earlier practice in this registry is the
  opposite — `S033`, `S054`, `S062`, `S069` all name the row they supersede in `teaches`. The new
  `registry-immutable.sh` enforces the *other* half of M38-8 (in-place column edits) and cannot see a
  duplicate: it compares only cells 2–12 of rows present at BASE.
- **Captured-by**: recorded at `7a1ac7fe` as M38-8 (the committed landing's `S112`; the in-place `S110`
  edit) — the *unlinked* half is disclosed as tolerated, but no check covers it and the registry cell a
  reader lands on carries no pointer to the other row.
- **Fix**: since S112/S117 are new rows this round, put "same document as S108, narrower scope" (resp.
  "S110") in `teaches` or `scope` while they are still appendable; extend check D to require a
  cross-reference whenever URL+digest repeats.
- **Shown able to fail**: D = 2 findings at the landing; a fixture with `supersedes S108` / `supersedes S110`
  in the two `teaches` cells → 0.

### R4 — LOW — a stray untracked file sits at the lane root of the final landing

- **Evidence**: `paths_raw.txt`, 86 lines / 2,770 B, mtime 04:01, `git status --short` → `?? paths_raw.txt`
  at `7a1ac7fe`; content is a bare list of lane-relative paths (`corpus/evidence/doctor/…`,
  `corpus/evidence/round34/…`). Wave-2 `R38W2Sentinel.md` §F1c flagged it; the final commit neither
  committed nor removed it, and the lesson does not mention it.
- **Fix**: delete it or file it under `.ufo/waves/round-38/w2/artifacts/<seat>/`; a landing check is
  `git status --porcelain` limited to the lane root.
- **Shown able to fail**: trivially — present ⇒ finding, absent ⇒ clean.

---

## 2. Defects that existed at the named landings and are closed at `7a1ac7fe` (audit trail)

Listed so the L1 can see exactly what my checks found and that the closures are real, not nominal.

| id (this report) | was (named landing) | now (`7a1ac7fe`) |
|---|---|---|
| F1 — C2 after-receipt cited under a name that never existed | `SCORECARD.md` row `R38-C2` and `corpus/lessons/round-38.md:11` cited `.ufo/waves/round-38/l1/scores/c2-final.json`; `find . -name 'c2-final*.json'` → only round-36; the real receipt `c2-at-0fc61133.json` was **untracked**; the lesson's "R37-CL1 closed — every receipt this round cites is committed" was false | row now cites `l1/scores/c2-at-0fc61133.json`, measured at `0fc61133`, and states "met by the frozen counter, which is shown non-discriminating"; the receipt and its `revision` field are committed (check A 0) |
| F2a — S110's scope cell widened in place | `3b960fe5` changed column 6 of an existing row | `S110` byte-identical to base (`diff` of the base and landing rows → empty); `registry-immutable.sh 77091b49 7a1ac7fe` → exit 0; M38-8 |
| F3 — the counter path shipped post-freeze logic, so `--freeze` was an argv label | worktree counter `d9aa8b62…`; run with `--freeze e059ca93` it produced a first-freeze-labelled receipt with `carriers_matched 4` (`receipt-worktree-counter-claiming-freeze-e059.json`) | `tools/round-38/c1-counter.py` at `7a1ac7fe` = freeze blob `a7a62b09…`; check C 0; M38-9 adds `ships_freeze_bytes` |
| F5 — wave-1 result ledger untracked, so seat accounting was not derivable from committed bytes | `r38-w1-results.json` (seats 40 / results 40) and `l1/attempt1-scratch-leftovers.txt` untracked at `3b960fe5`; round 36 had committed both and its verifier scored `seat accounting … pass` (`corpus/lessons/round-36-verifier-spotcheck.md:39`) | both tracked at `7a1ac7fe` (check E 0) |
| F6 — a QUALITY row cited a lesson row and a tool that did not exist at measurement time | at 04:05 `QUALITY.md` row 81 cited `M38-6` (no row in the lesson) and untracked `tools/round-38/intended-doc.py`, with three untracked receipts | `M38-6` row present, tool + receipts tracked (check H 0) |
| G — lane ids appended over staged ids of other documents | at `0fc61133` the guard output was 6 (`S106–S111`), while the append used `S112–S116` — all staged ids of different documents (staged `S113` = adb page vs lane `S113` = unblob BE fixtures; `id-collision-table.txt`) | the lesson now states 12 collisions (`S106–S117`) and why, and every Quarantine mention is prefixed "staged S…" — see §5 for the residual ambiguity |

In-flight cross-check (07:20Z, uncommitted): the L1's own final receipts
`l1/scores/c1-v1-at-final.json` (`carriers_matched 3`, `met_target false`), `l1/scores/c2-final.json`
(`mismatches 0`, `guards_ok true`) and `l1/freeze-drift-final.json` (`verdict drift`,
`ships_freeze_bytes true`, `net_changed []`, 3 entries) reproduce my independent runs exactly — so the
"measured at the landing commit" gap noted at the named landings is closed in flight.

Check-suite, three runs (`fixture-proof.txt`, `checks-run-landing-7a1ac7fe.txt`):

| run | A | B | C | D | E | F | G | H | total |
|---|---|---|---|---|---|---|---|---|---|
| named landing `0fc61133` (fixture repo from `git archive`, freeze object fetched in) | 2 | 4 | 1 | 1 | 1 | 0 | 5 | 0 | 14 |
| final landing `7a1ac7fe` (live worktree) | 0 | 4 | 0 | 2 | 0 | 0 | 6 | 0 | 12 |
| corrected fixtures | 0 | 0 | 0 | 0 | — | — | 0 | — | 0 |

Every check therefore discriminates: it flags the named landing, still flags what the final landing did not
fix, and passes once the fix is in place.

---

## 3. Premise corrections (assignment items that do not hold)

1. **"Attempt 1's entry title '(standard BE v4 → Core)'" — no such artifact.** No round-38 entry file exists
   at any attempt-1 commit (`git ls-tree -r` over `79f69347`, `f1010f67`, `3b0da5dd`, `077e212b` → only the
   round-36 entry). The wave-1 draft entry's own H1 is non-promoting
   (`w1/artifacts/R38ScribeEntry/entry.md:9`). Outcome-asserting wording exists only in *other* drafts:
   `R38ExecProvincePatch/patch.txt:29,34,44` (inserts `## Round-38 additions to Core` and "…is superseded
   for standard big-endian SquashFS v4"), `R38ExecReadmePatch/README.patched.md:236` ("standard big-endian
   SquashFS v4 is now Core"), `R38ScribeScorecardDraft/scorecard-section.md:20` ("## Round 38 — standard
   big-endian SquashFS v4 to Core").
2. **A frontier note claiming supersession did not land.** `PROVINCE.md` at `3b960fe5` says the opposite
   ("Round 38: standard BE v4 measured … not promoted — R38-C1 honest stop") and `LOG.md:3129` records that
   "the attempt-1 frontier note that claimed supersession was replaced before landing". The drafts' H1s
   carry `DRAFT` and `R38ExecReadmePatch.md` §2 says "claim-form text, not a landed edit". Residual, minor:
   the artifacts carry no machine-readable status line. **I do not propose a body-phrase grep as the fix**:
   it returns 36 hits on this wave, almost all embedded claims text inside counter snapshots (measured) — a
   check that cannot discriminate.
3. **"Seats writing into the fleet root" — none found.** The only fleet-repo references in `w1/*.md` are
   read-only calls of `scripts/sources-census.sh validate --file "$S/…"` (`R38ExecMirrorGate.md:101,240`) and
   citations. The out-of-lane instrument path is the L1's own `instruments.json` row (R1), and the
   fleet-root `unblob.log` leak is now recorded as M38-7 and removed (`ls -l
   /home/vgpnk/Projects/shokunin/unblob.log` → absent).

---

## 4. Negative results (searched, clean)

- `corpus/evidence/round-38/c1/K{1..4}/{before,after}.json`: before arm 0 files +
  `missing-extractor-dependency` on all four; after arm 5/3/4/4 with K2's single `unpublished-entry` —
  matches the entry's table and the SCORECARD's C1 row exactly.
- Carrier pins: K3 `9c7c523c…97c0` (4096 B), K4 `a29ddc15…56ed` (307 B) — equal to `carriers.json` and the
  S113 LFS oids.
- S116 / the assimilated entry: page byte-identical on refetch (HTTP 200, 216890 B, `sha256 8f8c29af…bbc5`),
  97 `<h2 id=`, "more than 30" ×3, ten unique `SquashFS (…)` names, lowercase `v4-broadcom` (9 occurrences
  of the lowercase form, 0 of `v4-Broadcom`), 42 `Vendor` occurrences. The final landing's per-section
  reading ("42 of 97 sections carry one `Vendor:` field, one value `unknown`") matches my count.
- S114's URL resolves (HTTP 200, 1496 B, `sha256 c1c43f6f…a5d5`) and equals the committed
  `.ufo/waves/round-37/probes/avm.txt` — the row is correct; the wave-1 draft had cited the
  `Freetz-NG/freetz-ng` wiki rendering (`sha256 100948f3…`) instead.
- Ledger tallies at `7a1ac7fe`: 117 rows; `A/mined` 101 → 105 and `A/rejected` 3 → 4 as the lesson states
  (plus `B/mined` 6 → 7); `registry-immutable.sh 77091b49 7a1ac7fe` exit 0.

---

## 5. Calibration observations (not defects)

- **Id-space ambiguity is now a labelled convention, not a silent collision.** `S113`/`S117` still denote
  two different documents depending on surface (lane row vs staged absent-defect register), but the landing
  prefixes every Quarantine mention with "staged S…" and states the 12-collision count. The residual risk is
  a bare `S113`/`S117` in a future report or grep joining the wrong row; a `pkg:`/`lane:` prefix would be
  stronger than prose.
- **The shipped rule text still contains the premise the round disproved.** `tools/round-38/c1-counter.py`
  and `plans/round-38-claims.md` at `7a1ac7fe` are the freeze bytes, whose docstring says "stock unblob
  26.6.4; no external extractor dependency" — contradicted by the four before receipts and by the entry's
  §"Why the dependency is structural". Unavoidable under QUALITY 79 (the bytes *are* the rule) and recorded
  as M38-3; flagged so a future round reusing the counter does not inherit the false premise silently.
- **The gate is not itself frozen.** `freeze-drift.py` changed in `7a1ac7fe` (+`ships_freeze_bytes`, +git
  failure handling) and is absent at the freeze; nothing pins its bytes. R2's fix should put its blob id in
  the instrument map.

---

## 6. Artifacts and reproduction

`.ufo/waves/round-38/w2/artifacts/R38W2MistakeHunt/`

| file | what it is |
|---|---|
| `checks.py` | checks A cited receipts, B instrument map, C counter identity, D registry cross-reference, E seat accounting, F draft titles, G id space, H criterion refs; `--root --freeze --landing --only` |
| `checks-run-lane.txt` | live snapshot 07:13:40Z during the review (13 findings) |
| `checks-run-landing-7a1ac7fe.txt` | final landing: A 0, B 4, C 0, D 2, E 0, F 0, G 6, H 0 |
| `fixture-proof.txt` | lane vs corrected fixture: A/D/G `2,2,6 → 0,0,0`; B/C `4,1 → 0,0` |
| `receipt-worktree-counter-claiming-freeze-e059.json` | F3-as-it-was: v3 counter, `freeze: e059ca93…`, `carriers_matched 4` |
| `receipt-frozen-v1-counter-at-3b960fe5.json`, `receipt-frozen-v1-at-7a1ac7fe.json` | the rule: 3 at both landings |
| `receipt-c2-repro-at-0fc61133.json`, `receipt-c2-repro-at-7a1ac7fe.json` | C2 re-derived at both revisions: `mismatches 0`, exit 0 |
| `freeze-selftest.txt` | freeze counter selftest 15/15 |
| `id-collision-table.txt` | lane `S106–S117` beside the staged id of the same number |

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 .ufo/waves/round-38/w2/artifacts/R38W2MistakeHunt/checks.py --root . \
        --landing 7a1ac7fe39410a3c9df13d97c14ba17f4d036ab6     # 12 findings, exit 1
python3 .ufo/waves/round-38/w2/artifacts/R38W2MistakeHunt/checks.py --root . --only A,C,E,H
```

Fixtures were built in scratch: `git init` in a `mktemp -d`, `rev-parse --show-toplevel` verified, two
commits with `-c user.email/-c user.name` local to that repo, then the three/five fixes applied by text
substitution and the suite re-run.

---

## 7. Compliance

- Writes: this report + `.ufo/waves/round-38/w2/artifacts/R38W2MistakeHunt/` only. No `corpus/`,
  `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/`; no fleet-repo, sibling-lane or shokuknow
  write; no campaign tool run in shokuknow (read-only reads of `merge/kaidoku/SOURCES.append.md`).
- VCS: read-only only in the lane; the only commits anywhere are inside the scratch fixture repo.
- REA: not invoked; both counters were re-run from frozen/copied bytes.
- Tools: none installed or upgraded. Scratch `/fast/scratch/hyaku/kaidoku-r38/R38W2MistakeHunt` removed.
