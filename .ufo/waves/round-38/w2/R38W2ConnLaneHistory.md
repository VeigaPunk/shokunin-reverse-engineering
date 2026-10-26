# R38W2ConnLaneHistory — QUALITY 79 vs 55/66: not a duplicate, it executes what 55 held as prose

**Verdict: CONFIRMED — QUALITY 79 is not a duplicate of 55/66 in practice. For the round-38
freeze shape (markdown plan, no `claims.json`), row 55's named gate cannot run at all (exit 2),
row 66 declares map-free claims unevaluable, and only `freeze-drift.py` (79) plus `gen-controls.py`
(80) provide executable checks. 79 additionally carries an adjudication clause that neither 55 nor
66 states. Overlap exists only inside the `claims.json`+`instruments` family, and there only for the
detection half.**

## What I attacked

Cross-round pattern question: connect M38-1/M38-2 (round-38 lesson) to the earlier freeze lessons and
criteria (QUALITY 55, 66, 68, 73; round-24*/round-34/round-36 lessons; `claim-freezes.tsv`). Is
QUALITY 79 a duplicate of 55/66 in practice, or does it add an executable check? Recommend
consolidation with pointers.

## Evidence (exact commands, outputs, exit codes)

1. **Row 55's named gate cannot execute on round-38.** `tools/round-31/freeze-integrity.py`
   locates the freeze commit as "the first commit … that adds `.ufo/waves/round-<N>/claims.json`"
   and reads `instruments`/`frozen_inputs` digests from that JSON. Round-38 has no `claims.json`:
   - `python3 -I -B tools/round-31/freeze-integrity.py --root <LANE> --round 38 --rev 0fc6113376a156fddc3ec385386d71c3a4a9f690`
     → `freeze-integrity: ERROR no commit adds .ufo/waves/round-38/claims.json at 0fc61133…`, exit **2**.
   - `git ls-tree -r --name-only 0fc61133 -- .ufo/waves/round-$r/ | grep -c claims.json` → **0** for r=36, 37, 38.
   - `corpus/claim-freezes.tsv` tail: last rows are round-32/34/35 — the ledger stops where the lane
     migrated to markdown plans (`plans/round-36-claims.md`, `plans/round-37-claims.md`,
     `plans/round-38-claims.md`). The claims.json-bound instrument family (rows 33, 46, 47, 55, 66,
     68) silently went inert from round 36 onward. M38-1 is the first concrete failure of that gap.
2. **Row 66 confirms the gap, it does not fill it.** "A map-free legacy claim is unevaluable, never
   vacuously CLEAN" — i.e., under 66 the pin-gate certifies nothing for round-38; there is no verdict
   at all, let alone a scoreable one.
3. **`freeze-drift.py` (79) is pin-free and path-based.** It reads only git objects, takes
   repo-relative paths or globs (default: claims doc, both counters, carriers manifest, oracle glob),
   exits 0 clean / 1 drift (commits listed) / 2 unevaluable. Committed receipts:
   - `.ufo/waves/round-38/l1/freeze-drift-077e212b.json` — exit 1, lists `f1010f67` (03:32:55,
     counter only) and `79f69347` (03:30:33, claims doc + counter).
   - `.ufo/waves/round-38/l1/freeze-drift-cb4326b2.json` — exit 0 (after the harness fix, kill-rule
     paths clean).
   - `.ufo/waves/round-38/l1/freeze-drift-gen-controls.json` — exit 1, lists `efd5c47a` for
     `tools/round-38/gen-controls.py` (M38-2; passed explicitly — it is not in the default set).
   - My re-runs at the judged revisions: `--freeze e059ca93 --rev 3b960fe5` → exit **1**,
     drift exactly `[f1010f67, 79f69347]`; `--rev 0fc61133` → exit **1**, same list. The attempt-2
     landing commits left the kill-rule paths otherwise untouched; the drift is stable at both judged
     revisions.
4. **Why adjudication is needed: the amendment changed the outcome on identical receipts.**
   - `.ufo/waves/round-38/l1/scores/c1-v1-at-3b960fe5.json` → `carriers_matched 3`, `met_target false`.
   - `.ufo/waves/round-38/l1/scores/c1-v3-at-3b960fe5-NOT-THE-RULE.json` → `carriers_matched 4`.
   - Wave-1 seats had already scored with the first-freeze counter bytes before the amendment:
     `R38ExecAfterK1.md` §2e (frozen sha `a7a62b09…`; D5 records the worktree counter had already
     been rewritten when K1 was scored) and `R38ExecAfterK2.md` lines 7–11 (K2's symlink gap —
     `unpublished-entry`, `var/lib/run-link` — reported before the v3 counter excluded exactly that
     gap class). The v1→v3 flip on the same receipts is the M38-1 fact.
   - The `-NOT-THE-RULE` suffix on the v3 receipt shows the supremacy adopted (score with first-freeze
     bytes; amendment reported, never adopted).
5. **C2 side:** `c2-at-0fc61133.json` — `mismatches 0`, `guards_ok true`, `met_target true`, exit 0;
   the C2 counter itself is drift-free at the landing (only the v1/v3 pair is in the drift list).

## Mapping: 55 vs 66 vs 68 vs 73 vs 79 vs 80 (in practice)

| Row | Container required | Detection | Adjudication | On round-38 |
|---|---|---|---|---|
| 55 | `claims.json` `instruments`/`frozen_inputs` | digest at measured rev **and** commits_after_freeze per pin | none | gate exits 2 — cannot run |
| 66 | `claims.json` map | schema refusal (absent/empty/malformed) | map-free claims unevaluable, never CLEAN | no verdict (unevaluable by design) |
| 68 | `claims.json` `instruments` | re-hash pins, predicate byte-identity across claim/config/counter/receipt (one revision) | none | container absent — inert |
| 73 | — | receipt binds argv/reader digest/commit/instant | receipts unbound = reproduce by hand | complementary; the v3 receipts' reader digest would not match the frozen counter |
| 79 | none | any kill-rule path touched between freeze and rev (commit list) | **yes** — first-freeze bytes are the rule; amendment reported, never adopted, whatever it calls itself | **executes** — exit 1 at 077e212b/3b960fe5/0fc61133 |
| 80 | none | same drift tool over control generators | drift = reproducibility defect to disclose | **executes** — exit 1 at efd5c47a |

So: 79 overlaps 55 only in the detection half, only for freezes that ship `claims.json`+pins, and
even there 79 contributes the adjudication clause plus coverage of unpinned kill-rule paths (oracles,
carriers, prose claims doc). 66/68/73 are orthogonal — schema guard, single-source predicate identity,
receipt binding — none duplicated by 79.

## Recommendation (consolidation, with pointers)

- **No row should be marked superseded.** Keep 55, 66, 68, 73, 79, 80 as-is; the bar's own rule is
  "a criterion is replaced by a new row naming the row it supersedes, never rewritten", and 79's
  supersedes cell ("executes 55") is the correct relation: it makes 55 executable for the freeze
  family 55's gate cannot see.
- **Add a future domain-split pointer** (next lesson appendix or a new row naming 55/79, whichever the
  L1 prefers — this seat only recommends): 55 = pin-schema detection for `claims.json` freezes; 79 =
  pin-free drift + adjudication for non-map freezes; 66 = schema guard for the pin gate. Record that
  rounds 36–38 migrated off `claims.json` (ledger stops at round-35) — that migration is the root why
  55 was "held as prose".
- **Freeze-drift default-set wrinkle:** `gen-controls.py` is not in the default pathspec; row 80 must
  keep passing it explicitly (the committed receipt did). If control generators become a standard
  member of kill-rule sets, add it to the default and note the change.
- **Conservative-bias note (second-order):** `freeze-drift` lists touching commits, not content
  equality — a revert still reports drift (and correctly scores first-freeze bytes, which equal the
  revert). Where a `claims.json` map exists, keep 55's digest check for the stronger "unchanged"
  claim; the two are complementary, not redundant.
- **Verification surface:** the tool reads only git objects (no worktree dependence), so any seat can
  reproduce it — consistent with the lane's reviewer/spot-check model (e.g., `R38ReviewerControlReplay.md`).

**Affected axes:** calibration (the adjudication rule removes the "pre-scoring" laundering path) and
verification coverage (the missing executable check for non-map freezes). No score moves; the verdicts
of record are unchanged (C1 honest stop 3/4; C2 met).
