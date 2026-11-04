# CriticClaims — R79 claim-shape falsification (seat r79-w1)

Target: falsify the **shape** of R79-C1/C2 (sizing, axis naming, causal separability, do-nothing
controls), not their arithmetic. Base `29d2ca30`, declaration `a1f9b81`, freeze `ed68cd0`.
Lane bounds: no production file edited; every write is under this seat's evidence dir plus
`/fast/scratch/hyaku/kaidoku-r79/CriticClaims/` (deleted before yield).

Read in full: `plans/round-79-claims.md`, `.ufo/waves/round-79/claims.json`,
`tools/round-79/gate-mutation.py`, `tools/round-79/pointer-bind.py`,
`tools/round-78/surface-recheck.py`, `tools/round-78/attack-gate.py` (selftest + mutation-relevant
functions), `SCORECARD.md` rounds 73–78, and the six pre receipts + two controls.

Receipts: `w1/CriticClaims/` — `c1-textcase.json` (+ validate), `c2-selfpointer.json`,
`c2-path-only-at-base.json` (+ validate), `c1-empty-at-base.json`, `r78-surface-at-decl.json`,
`combined-forged.json` (+ both validates), `validate-c1-sole-false.txt`,
`validate-c2-no-checked-at.txt`, `validate-c1-cases-26.txt`, `validate-c1-pin-actual-diverges.txt`,
`validate-c2-selfpointer.txt`. The C1 counterexample is reproducible from the preserved evidence
bytes `textcase-target.py` (sha256 `d9145e9f…`, the receipt's target) and `textcase-instrument.py`
(pin patched to that digest) — see `w1/CriticClaims/textcase-README.md`; `textcase-target.py` is a
doctored evidence copy, not a production file.

---

## 1. Questions and verdicts

### Q1. Is R79-C2 a re-score of a rule the lane already holds rather than a new surface?

**Verdict: yes — a rule re-score on the round-78 `surface recheck` surface, not a new surface.**

- The same five pointer cells and the same five live objects were already checked by
  `tools/round-78/surface-recheck.py`: `DECLARED` pins exactly devin/omp/kimi/bashrc/ghidra
  (`tools/round-78/surface-recheck.py:50-56`), and the round-78 predicate already claimed
  “a pointer rule” — `SCORECARD.md:6061-6063` says the capability is eight values
  “with `checked_at`, an `unparsed` id list and **a pointer rule**”.
- The only thing R79-C2 changes is that rule: round 78 compared
  `pointer.split(":")[0]` (`tools/round-78/surface-recheck.py:203-204`, path-only), round 79
  binds the line/range (`tools/round-79/pointer-bind.py:79-121`, frozen declaration bytes;
  the worktree copy carries an unrelated +3-line CLI edit — see §5). The *surface* did not move.
- Command that shows it unmoved: at the declaration rev the round-78 rule scores the same five
  paths green —
  `python3 -I -B tools/round-78/surface-recheck.py --root . --rev a1f9b81cf0cd5065df3a9b25b30ce2eb184d012d --battery --json-out <scratch>`
  → `{"checks": 8, "matched": 8, "mismatches": 0, "ok": true, "unparsed": 0}`
  (`w1/CriticClaims/r78-surface-at-decl.json`, `checked_at 2026-11-04T10:10:06-03:00`).
- The base arm is a record-text repair, not a live-object drift: the two base mismatches are
  line numbers only (`omp-pin` record `:8`, `kimi-pin` record `:4126`), both paths resolve
  (`pre/c2-at-base.json`). The live files never moved; the record's own line numbers did. A
  round that did nothing but edit those two integers would move C2's counter.
- Consequence for the capabilities table: if a new row is entered for R79-C2, the table carries
  two rows over one surface (`surface recheck`, first-working 78, and the new row), the second a
  strictness increment of the first's pointer rule — duplicate authority over the same surface.
  The smallest safe correction is to fold the line-bound rule into the existing `surface recheck`
  row as a revision (and to say so in the claims), or to state that C2 is a re-score and not a
  capability acquisition.

### Q2. Does R79-C1's `sole_detector` clause actually bind case independence?

**Verdict: no. The field is computed but never admitted; the only binding clause is “the declared
case's `pass` flag is false”, which a source-text assertion satisfies.**

Evidence, instrument-level:

- `judge()` defines killed as “declared case present and `pass` false” and sets
  `"killed_by_declared": killed` — a tautology (`tools/round-79/gate-mutation.py:188,193`).
  Therefore `declared_case_hits` (sum of `killed and declared in failed_cases`, lines 225-227,
  290-292) is identically `killed`: the kill rule's clause “a mutant killed by a case other than
  its declared one counted in `declared_case_hits`” can never fire.
- `sole_detector` is computed (`:196`) but is **not** in `battery()`'s `ok` formula (`:313-317`)
  and is **not** checked by `validate_receipt()` (`:200-238`). Probe: the landing receipt with
  `m03-near-miss-re-dead.sole_detector` flipped to `false` validates
  `{"defects": [], "mutants": 8, "survivors": 0}` exit 0
  (`validate-c1-sole-false.txt`). Same for `pristine.cases` set to 26
  (`validate-c1-cases-26.txt`) and for `target_pin.actual` diverging from `target.sha256`
  (`validate-c1-pin-actual-diverges.txt`) — the predicate's “29 cases” and the kill rule's “own
  target pin” are prose-only in admission.
- Constructive demo: I copied the declaration's 29-case gate into a scratch git fixture and
  replaced the three new cases' bodies with source-text presence assertions (`src = …read_text()`;
  the literals are split so the assertion does not match itself) that call **no** gate function.
  The frozen battery still reports `mutants_total 8`, `killed 8`, `survivors 0`,
  `declared_case_hits 8`, `pristine {cases 29, failures 0, ok true}`, `ok true`, exit 0, and
  `--validate` defect-free; `m03`, `m05`, `m08` are each `sole_detector true` with their declared
  case the sole failure (`w1/CriticClaims/c1-textcase.json`, `validate-c1-textcase.txt`). The
  three text cases assert the anchor literal is in the file — zero behavioural detection, exactly
  the class the claim says it closes.
- The landed three cases are genuinely behavioural (they call `judge_group`, `bind_clause`,
  `validate_receipt`; `tools/round-78/attack-gate.py:903-921`), so the *measured* landing is not
  false. What is false is the clause: nothing in the frozen predicate, kill rule or instrument
  requires a declared case to exercise the mutated code path.

### Q3. Are the two claims causally separable (neither counter reads the other's receipt)?

**Verdict: yes at the counter/value level, with one authoring caveat.**

- `grep` over both instruments: `gate-mutation.py` contains no `pointer-bind`, `PROVINCE`,
  `checks_total` or `mismatches`; `pointer-bind.py` contains no `attack-gate`, `gate-mutation`,
  `mutants`, `survivors` or selftest-target reads. Inputs differ (`git show <rev>:tools/round-78/
  attack-gate.py` vs `git show <rev>:PROVINCE.md` + five host files); counters differ
  (`survivors` vs `mismatches`); schemas and validators are disjoint (each validator rejects the
  other shape as a defect).
- Shared state is the revision (`--rev`) and the claims container, not a produced value.
- Caveat: **both “after” states are authored by the same declaration commit**, so a single commit
  can move both counters; separability of readings is not independence of authorship.

### Q4. Does the base arm separately measure a do-nothing control for each claim, and can either control meet the target?

**Verdict: both claims have a base arm and a dedicated control. C1's control cannot reach the
target at any revision; C2's `path-only` control *does* reach the counter's numeric target and
self-declares `ok: true` — it is blocked only by the separate `--validate` call, not by the
counting command.**

- C1 base arm (`pre/c1-at-base.json`): `survivors 3`, `killed 5`, `pristine.cases 26`,
  `target_pin.matched false`, `ok false`. The base arm is also a *confounded* do-nothing state:
  it is guaranteed to miss the target on the pin and the case count alone, independently of the
  three survivors. The dedicated `empty-set` control isolates vacuity: `mutants_total 0`,
  `survivors 0`, `ok false`, exit 1 (`pre/controls/c1-empty-set.json`; reproduced at base,
  `w1/CriticClaims/c1-empty-at-base.json`). `battery()`'s `ok` requires a non-empty result list and
  `len(results) == len(MUTANTS)` (`:313-317`), so the empty set cannot pass at any rev. **Cannot
  meet the target.**
- C2 base arm (`pre/c2-at-base.json`): `mismatches 2`, `ok false`, exit 1 — cannot meet.
- C2 control (`pre/controls/c2-path-only.json`): `checks_total 5`, `matched 5`,
  `mismatches 0`, `unparsed 0`, **`ok true`**. Reproduced at base:
  `python3 -I -B tools/round-79/pointer-bind.py --root . --rev 29d2ca30 --control path-only
  --battery --json-out …` → `{"exit": 0, …, "mismatches": 0, "ok": true}`
  (`w1/CriticClaims/c2-path-only-at-base.json`). The receipt's only discriminators are
  `control: "path-only"` and null `line_start`/`line_sha256`. A separate
  `--validate` exits 1 with 10 defects (“matched without a pointed-line digest / 1-based line
  range”, `validate-c2-path-only-at-base.txt`), so the *complete* predicate is blocked — but the
  claim's `counting_command` does not run `--validate`, and the control's own `ok` is true.
  **§9 defect: the do-nothing control reaches the counter's target.** Smallest fix:
  `receipt["ok"] = … and control is None`; report `would_pass: true` separately, and/or make
  `--battery` refuse to emit `ok true` under `--control`.

### Q5. Is the lowest-axis obligation met, and is the nudge waiver correctly not claimed?

**Verdict: met by C1; the waiver is correctly not claimed; but C2's axis is a fleet axis the lane
does not own.**

- At the start of round 79 the three lane-owned proxies were tied at 10.0 — the round-78 section
  states it (`SCORECARD.md:6048-6049`), and every round 73–78 header repeats it. R79-C1's axis is
  `calibration`, so C1 works a tied-lowest axis. Obligation met.
- Nudge waiver rule (as corrected in round 73): the waiver applies only when **no capability rows
  entered inside the 10-round window**; the round-72 “nudge applies” rationale was superseded
  because rows entered in rounds 70–71 were inside the window (`SCORECARD.md:5737-5740`). Round
  78 entered two capability rows (`attack-class refusal`, `surface recheck`, `SCORECARD.md:660-661`),
  and rounds 73–77 entered capability rows; all are inside the window. So the waiver condition is
  not met and the claims correctly do not claim it.
- Naming caveat: `freshness` is recorded as a **fleet axis, unowned proxy** (`SCORECARD.md:376,402`),
  not one of the three lane-owned proxies. R79-C2 therefore moves no lane-owned axis. The claims'
  sentence “Two claims on two distinct axes” is literally true, but one of the two axes is not
  scored by the lane; the §9 lowest-axis obligation is carried entirely by C1. The plans text
  should say “one owned axis (calibration) + one fleet axis (freshness)”.

### §9 sizing (do-nothing controls) — section absent

`plans/round-79-claims.md` has per-claim “Controls (scored before data)” but no
“§9 sizing (do-nothing controls)” section of the shape used at rounds 59/60
(`plans/round-59-claims.md:131`, `plans/round-60-claims.md:140`). The before-arms are committed
before the data, which satisfies the ordering half; the sizing half fails for C2 as measured
above (its control reaches the target).

---

## 2. `both_pass_forgery`

Two constructions were tried; **neither is blocked by any implemented clause**.

**(a) One hand-written receipt object passes both admission validators.** A single JSON object
carrying both key sets (8 `killed` mutants with `failed_cases == [declared_case]` and `sole_detector
true`; 5 `checks` with `matched true`, `line_sha256`, 1-based `line_start/line_end`; 64-hex
`target.sha256` and `record.sha256`; `pristine {cases 29, failures 0}`; `checked_at` present;
`ok true`) is accepted by both `--validate` invocations with `defects []`, exit 0
(`w1/CriticClaims/combined-forged.json`, `validate-combined-c1.txt`, `validate-combined-c2.txt`).
The intended blocking clauses are prose: C1's “a receipt admitted without re-deriving its own target
pin” and C2's “a receipt without its `checked_at`”. `gate-mutation.py --validate` never opens the
repo (it checks only that `target.sha256` is 64 hex and that `pin.expected == target.sha256` when
`matched`; it does not check `pin.actual`, the case count, `measured_at` or any instrument digest);
`pointer-bind.py --validate` never checks `checked_at` (deleting it still yields `defects []`,
`validate-c2-no-checked-at.txt`) and never re-derives `record.sha256` from `record.rev`. Neither
receipt records the producing instrument's path/digest, and neither battery's `--validate` is
part of its `counting_command`.

**(b) One declaration commit passes both battery counters with no behavioural work.** The C1 half
is the text-presence target above (`c1-textcase.json`: 8/8 killed, 29 pristine cases, `ok true`,
validate defect-free). The C2 half is a record that repoints each of the five cells at a file under
the record author's control. Demonstrated in a scratch git fixture whose `PROVINCE.md` points its
three pin cells at `PROVINCE.md:1` (the line carrying `rea-agents@6.7.0`), its Ghidra cell at a
synthetic `Ghidra/application.properties:1`, and its `.bashrc` cell at a synthetic `fake.bashrc:1`:
the frozen binder reports `checks_total 5`, `matched 5`, `mismatches 0`, `unparsed 0`, `ok true`,
exit 0, and `--validate` defect-free (`c2-selfpointer.json`). No host config is read. This is a
**regression against round 78**, whose `compare()` pinned the expected absolute path via
`same_path(expand(clean), DECLARED[client])`; round 79 drops `DECLARED` entirely and takes the path
from the record (`pointer-bind.py:79-121,123-168`, frozen declaration bytes). The C2 kill rule “a file read outside the
pointer's declared path” is the opposite protection (it forbids reading a *different* file than the
record names; it does not forbid the record naming the wrong file).

**Blocking clause: none in the frozen sentence or the instruments.** The nominally relevant clauses
(“own target pin”, “no `checked_at`”, “declared case … in the target's selftest”) are unenforced
or do not apply to these constructions.

---

## 3. Weakest clause per claim and next-round hardening

### R79-C1

Weakest: **“each mutant's declared case is present … and fails there”** — admission reads only the
case's boolean, and `sole_detector` is computed but never gated (`gate-mutation.py:196,313-317,
200-238`), so a source-text assertion passes. Second weakness: `declared_case_hits` is
definitionally equal to `killed`, so the kill rule's “killed by a case other than its declared
one” clause is unreachable, and `pristine.cases == 29` is not checked.

Hardening (smallest safe set):
1. `battery()["ok"]` must additionally require, for every mutant, `sole_detector is True`, and
   `validate_receipt()` must flag `sole_detector` false when `killed`.
2. Drop or redefine `declared_case_hits` (it carries no information); require instead
   `detector_count == 1` for the declared case in the receipt and in `--validate`.
3. Bind behaviour, not text: run each declared case against a second mutant with the **same
   behaviour change written differently** (or with the dead constant re-expressed) and require it
   to fail there too; a text-presence case passes that second mutant and is refused. Cheaper
   variant: require the declared case's source to call the mutated symbol (a static check on the
   target's case body), recorded in the receipt.
4. Add `pristine.cases == 29` to `--validate`; require `target_pin.actual == target.sha256` and
   re-derive `target.sha256` from `target.rev` inside `--validate`; embed the instrument
   `{path, sha256}` and `argv` in the receipt and authenticate them (the round-78 `receipt_auth`
   pattern) so a hand-written receipt cannot pass.

### R79-C2

Weakest: **the recorded pointer's path is taken from the record with no expected-path pin**
(`pointer-bind.py:79-121,123-168`, frozen declaration bytes). A record can repoint all five cells at any token-bearing file
(including itself) and score 5/5; the round-78 `DECLARED` path table was dropped. Second weakness:
the do-nothing (`path-only`) control reaches `mismatches 0` **and `ok true`**; only the separate
`--validate` blocks it, and the kill rule's “path-only control used as the claim's counter” is
prose. Third weakness: `checked_at` is required by the kill rule but not by `--validate`; the pin
cells are parsed with `findall` into a dict (last duplicate wins) and the ghidra/bashrc cells with
`search` (first match wins), so a duplicated/historical cell silently wins — the round-78
“first regex match in the file” limit is inherited, not closed.

Hardening:
1. Reinstate the round-78 `DECLARED` table: `{"devin-pin","omp-pin","kimi-pin","ghidra-version",
   "bashrc-exports" → expected absolute path}` and require `same_path(expand(check.path),
   DECLARED[id])` per check; add that to `--validate` and to the kill rule.
2. Reject a pointed path that resolves inside the lane's record (`PROVINCE.md`) or the instrument
   tree; a record that names itself is unparsed, not matched.
3. `ok` must be false whenever `control is not None`; the control should report
   `would_pass`/`counter_reached` and never `ok true`.
4. `--validate` must require `checked_at`, reject duplicate ids/cells, and re-derive
   `record.sha256` from `record.rev`; embed the instrument digest (as for C1) so admission is
   provenance-bound.
5. State in the claims that C2 is a **revision** of the round-78 `surface recheck` pointer rule
   (same surface, same five objects), not a new capability row — or fold it into that row.

---

## 4. Receipt JSON

```json
{
  "seat": "CriticClaims",
  "round": 79,
  "base": "29d2ca30b83a6a0d85b0aa979de0138fde1660e6",
  "declaration": "a1f9b81cf0cd5065df3a9b25b30ce2eb184d012d",
  "freeze": "ed68cd0a6cc790cca342380a2d80d1927a668c8c",
  "questions": [
    {
      "question": "Is R79-C2 a re-score of a rule the lane already holds rather than a new surface?",
      "verdict": "yes - rule re-score on the round-78 surface recheck surface; same five cells, same five live objects; only path-only -> line-bound moved",
      "evidence": "tools/round-78/surface-recheck.py:50-56 (DECLARED pins the same five paths), :203-204 (pointer.split(':')[0]); SCORECARD.md:6061-6063 (round-78 capability already claims 'a pointer rule'); r78-surface-at-decl.json = checks_total 8, matched 8, mismatches 0, ok true at rev a1f9b81; pre/c2-at-base.json mismatches are line numbers only (omp :8, kimi :4126), both paths resolve. Command showing unmoved: python3 -I -B tools/round-78/surface-recheck.py --root . --rev a1f9b81cf0cd5065df3a9b25b30ce2eb184d012d --battery --json-out <scratch>"
    },
    {
      "question": "Does R79-C1's sole_detector clause actually bind what the claim says (case independence)?",
      "verdict": "no - computed but unenforced; killed is defined as the declared case's false flag and declared_case_hits is identically killed; a source-text assertion satisfies it",
      "evidence": "gate-mutation.py:188 (killed definition), :193 (killed_by_declared = killed), :196 (sole_detector), :200-238 (validate ignores sole_detector), :313-317 (ok ignores sole_detector); validate-c1-sole-false.txt (m03 sole_detector false -> defects [] exit 0); validate-c1-cases-26.txt (pristine.cases 26 -> defects []); validate-c1-pin-actual-diverges.txt; c1-textcase.json: three source-text cases, killed 8, survivors 0, declared_case_hits 8, pristine cases 29 failures 0, ok true, validate defect-free; c1-at-landing.json has sole true for m03/m05/m08, so the measured landing happens to hold while the clause does not bind"
    },
    {
      "question": "Are the two claims causally separable (neither counter reads the other's receipt)?",
      "verdict": "yes at the counter/value level; no cross-reads; caveat both afters are authored by one declaration commit",
      "evidence": "grep over tools/round-79/gate-mutation.py: no pointer-bind/PROVINCE/checks_total/mismatches; grep over tools/round-79/pointer-bind.py: no attack-gate/gate-mutation/mutants/survivors; inputs differ (git blob of attack-gate.py vs PROVINCE.md + five host files); counters differ (survivors vs mismatches); each --validate rejects the other schema as a defect"
    },
    {
      "question": "Does the base arm separately measure a do-nothing control for each claim, and can either control meet the target?",
      "verdict": "C1: base arm + empty-set control cannot meet the target at any rev. C2: base arm cannot, but the path-only control reaches the counter's numeric target with ok true; only the separate --validate blocks it",
      "evidence": "pre/c1-at-base.json survivors 3, ok false; pre/controls/c1-empty-set.json mutants_total 0, ok false; c1-empty-at-base.json exit 1; gate-mutation.py:313-317 requires a non-empty result set and len(results)==len(MUTANTS). pre/c2-at-base.json mismatches 2, ok false; pre/controls/c2-path-only.json matched 5, mismatches 0, ok true; c2-path-only-at-base.json exit 0, ok true; validate-c2-path-only-at-base.txt exit 1 with 10 'matched without a pointed-line digest / 1-based line range' defects; the predicate's counting_command does not run --validate"
    },
    {
      "question": "Is the lowest-axis obligation met (C1 on a tied-lowest axis) and is the nudge waiver correctly not claimed?",
      "verdict": "yes via C1; waiver correctly not claimed; freshness is a fleet axis the lane does not own",
      "evidence": "SCORECARD.md:6048-6049 (coverage/depth/calibration tied at 10.0); R79-C1 axis calibration; SCORECARD.md:5737-5740 (waiver only when no capability rows in the 10-round window) vs SCORECARD.md:660-661 (two capability rows, first-working round 78) and rounds 73-77 rows; SCORECARD.md:376,402 (freshness = fleet axis, unowned proxy)"
    }
  ],
  "both_pass_forgery": {
    "single_receipt": {
      "file": "combined-forged.json",
      "result": "both --validate invocations: defects [], exit 0",
      "blocking_clause": "none implemented; C1 kill rule 'a receipt admitted without re-deriving its own target pin' and C2 kill rule 'a receipt without its checked_at' are prose only; --validate never opens the repo, never checks checked_at, pin.actual, pristine.cases or any instrument digest"
    },
    "single_declaration_commit": {
      "c1": "three source-text selftest cases (no gate call): killed 8, survivors 0, declared_case_hits 8, pristine 29 cases 0 failures, ok true, validate defect-free (c1-textcase.json)",
      "c2": "record repoints its five pointer cells at token-bearing files under the author's control (including the record itself): matched 5, mismatches 0, unparsed 0, ok true, validate defect-free (c2-selfpointer.json); no host config read",
      "blocking_clause": "none; C1's 'case exists only in the battery's own text' does not apply (the cases live in the target), and C2 has no expected-path pin"
    }
  },
  "weakest_clauses": [
    {
      "claim": "R79-C1",
      "clause": "each mutant's declared case is present in the mutant's selftest output and fails there",
      "why": "admission reads only the case's boolean; sole_detector is computed (gate-mutation.py:196) but absent from ok (:313-317) and validate (:200-238); declared_case_hits is identically killed; pristine.cases 29 is not checked",
      "hardening": "gate sole_detector for every mutant; replace declared_case_hits with detector_count/sole; require each declared case to fail on a textually distinct same-behaviour mutant; check pristine.cases==29; re-derive target.sha256 and pin.actual in --validate; embed and authenticate the instrument digest"
    },
    {
      "claim": "R79-C2",
      "clause": "every declared token occurs on a line inside the range named by the record's pointer",
      "why": "the pointer's path is taken from the record with no expected-path pin (DECLARED dropped from round 78); a self-referential record scores 5/5 with ok true; the path-only control also reaches ok true; checked_at is required by the kill rule but not by --validate",
      "hardening": "reinstate DECLARED and require same_path(check.path, DECLARED[id]); reject a pointed path inside PROVINCE.md or the instrument tree; make ok false under any --control; require checked_at and duplicate-cell rejection; re-derive record.sha256 in --validate; fold the rule into the existing surface recheck capability row"
    }
  ],
  "risks": [
    "C2's declared 'before' is a record-prose repair (two stale line numbers), not a live-object drift; a do-nothing round could move the same counter by editing two integers",
    "C2 entered as a new capability row would duplicate the round-78 'surface recheck' capability over the same PROVINCE.md surface",
    "freshness is unowned; only C1 satisfies the lane's lowest-axis obligation",
    "both receipts are self-consistency objects with no instrument identity, so the combined-forged receipt passes both admission validators",
    "the round-78 'first regex match in the file' limit is inherited by C2's scalar parses; duplicate cells silently win"
  ]
}
```

## 5. Scope note

No production file was edited. All probes ran read-only against the lane and wrote only to this
seat's evidence dir and `/fast/scratch/hyaku/kaidoku-r79/CriticClaims/` (git fixtures used
`git -C "$D"` with the toplevel asserted equal to `$D`; the scratch dir was removed before yield).
No subagent dispatch; no `agent://all` message.

**Instrument-byte note.** The worktree copy of `tools/round-79/pointer-bind.py` was modified by
another seat (`sha256 3f07bd2a…` vs the frozen pin `91d23dad…` in `claims.json`); the diff makes
`--battery` optional when `--rev` is supplied and does not touch `bind`, `parse_record`, the
counter or `validate_receipt`. Every C2 receipt in this seat was re-produced with the **frozen
declaration bytes** extracted by `git show a1f9b81:tools/round-79/pointer-bind.py`
(sha256 `91d23dad…`, the digest `claims.json` pins), so the evidence matches the frozen instrument.
The C1 instrument's worktree bytes equal its pin (`682f1e78…`).

**Disclosure.** Two transient validate outputs were briefly written to `/tmp/pb.out` and
`/tmp/pb2.out` by an aborted shell line; both were removed immediately and contain no evidence not
already in this seat's evidence dir. No other write left the lane evidence dir or the scratch root.
