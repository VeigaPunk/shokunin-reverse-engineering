# ReviewerScope — contract-conformance review of the frozen round-96 declaration

Reviewer leaf seat, round 96 w1. Read-only on the lane except this seat directory.
Scratch used and removed: /fast/scratch/hyaku/kaidoku-r96/ReviewerScope (extracted decl/sup
trees via `git archive`, no git mutation anywhere, no tool installs — no RULES.md install
record needed).

Canonical bytes: declaration commit `e4d1f7de9deae83e6d5f78d2d7f0157196002af0`
(parent = base `0ea695e826f2dca53dd55ac0bafead93de26b173`, verified by
`git rev-parse`/`git log --format='%H %P'`), supersession commit
`3baac2ef4b9b2830d299125b8184ca06d9e6584d` (child of declaration, HEAD of the lane
working tree). All checks below ran against those committed bytes.

## Item 1 — plan ↔ claims.json agreement: PASS

Cross-checked: base revision, pins path, frozen labels (both the C1 target label and the
battery label, verbatim), before-receipt lists (C1 three, C2 three, same paths), S321
source + sha256 + evidence receipt + closed round-93 carried limit, expect 35, mutant
table + fixtures paths, after-receipt placeholders, kill-rule clauses. All agree.
Declared, disclosed differences (not contradictions):

- `instrument_supersessions` + `kill_rule_amendment` exist ONLY in the supersession
  claims.json (verified by diff: the supersession commit's only claims.json change is
  additive — those two keys plus a comma). The frozen declaration's twin is silent on
  them, exactly as a freeze-ahead-of-supersession should be; they are the disclosed
  amendment channel.
- R95-VD-2 (numerical claim without a counting command, corrected by an appended lesson
  entry) is stated in the plan but not referenced in claims.json — attribution omission
  only, no conflicting statement.
- claims.json C2 does not name the three measuring tools or addressee expectations
  (the plan does; the pins file is structural so no byte-level conflict).
- Auxiliary paths named only in the plan (not contradictions): `upx-stop-boundary-search-repair.py`,
  `identity_noop.py`, `gen-forgery-fixtures.py`.

## Item 2 — structural facts from committed bytes: PASS

Before receipts (all committed at declaration, `world_revision` = base):
- pre/c1-legacy-rule-at-base.json: counts {killed: 5, mutants: 10}, met_target false,
  exit 1, label "r95-rule mutants killed 5 of 10"; row flags give survivors EXACTLY
  {M2, M3, M4, M6, M10} and killed {M1, M5, M7, M8, M9}. Matches plan.
- pre/c1-v5-admits-unbound-at-base.json: unbound {accepted 5, crashed 1, total 6, typed_refusals 0};
  forge-unlabelled row carries error `KeyError: 'fresh_scored'`; `nojson` {exit 0,
  receipt_written false}; met_target true. Matches plan ("accepted 5 of 6 … bare
  KeyError … no-json-out exits 0 without a receipt").
- pre/c1-probe-writer-unbound-at-base.json: before leg (round-95 probe) `victim_intact:
  false`, after leg (v2 probe) `victim_intact: true`, label "before victim_intact False;
  after victim_intact True". Matches plan.
- C2 base receipts all exit 1 with expect 35: block35-after-manifest "failing exit 1 —
  block 35 missing (craft has 34 blocks)"; depth-v2 "blocks 34 resolved 34 expect 35 …
  met=False exit=1"; depth-v3 "blocks 34, resolved 34 … expect 35 … met=False exit=1".
 Matches plan.
- S321: pre/s321-fresh-source2-at-base.json — exit 0, met_target true, counts
  {repaired 2, far_refused 2, near 2, far 2}, deterministic true, intact_identity true,
  source "/usr/bin/printf", source_sha256 = b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7
  (re-verified live against /usr/bin/printf — still matches), revision = base.

Mutant table (decl + sup): M0 identity control (find == replace, must NOT be killed) +
M1..M10. Every `find` string occurs EXACTLY ONCE in its target's committed bytes —
checked in BOTH trees (sup's mutant-relevant regions are identical, so the table is
unaffected by the supersession; `build_copy` applies `data.count(find) == 1` as the
exactly-once rule at run time). Files: M1-M6 → stop-boundary-repair-battery-v6.py;
M7-M9 → round-95/c1-agreement-v2.py; M10 → symlink-probe-v2.py; kills_via annotations
match the plan's adaptation description. forgery_reasons map = the six plan reasons,
verbatim.

Fixtures (6 × {json, stdout, rc} in both trees; final json bytes = sup):
Each forge-<name>.json deviates from the honest v6 receipt (honest-pos.json as template)
in EXACTLY ONE field, and it is the designated lie:
  unlabelled  → counts drops `fresh_scored` (met_target False, exit 1)
  met-lying   → met_target False, exit 1 (label still == expect) → met-not-recomputed
  head-mismatch → head = "a"*40, all pins honest
  counter-pin → counter_sha256 = "0"*64, all others honest
  verdict-pin → verdict_sha256 = "f"*64, all others honest
  repair-pin  → repair_sha256 = "0123456789abcdef"*4, all others honest
(Verified by field-by-field comparison against the honest template; each differing-key
list minus meta-keys had exactly the designated pathology. Confirmed against the pinned
generator gen-forgery-fixtures.py: it writes each forge-<name>.{json,stdout,rc} triple
with stdout = "<label> met <bool> exit <int>" SYNTHETICALLY — the .stdout/.rc files are
NOT counter runs; they are the template export, so mixed exit 0/1 values are correct.)
world_revision (fixture `revision`/`head` fields) = base for all six, per plan
("world revision = base").

## Item 3 — pins: PASS

- `sha256sum -c .ufo/waves/round-96/pins.sha256` → 0 mismatches, 51 entries in the
  declaration tree; regenerated pins in the supersession tree: 60 entries, 0 mismatches.
- Coverage: every tool the claims/plan name is pinned (all 13 paths + mutants.json +
  both C2 manifests). Round-95 instruments explicitly pinned and unedited (battery-v5,
  c1-agreement-v2, c1-forgery-refusal, symlink-probe; round-94 v4 battery + receipt
  agreement too). Round-93 battery-v3 bytes referenced by the frozen verdict pin remain
  unpinned at path level — disclosed in named limits; the receipt still binds them by
  `verdict_sha256` inside every receipt byte.
- The three C2 kill-rule sha256s (34cf65…, 359f15…, bcf6c4…) all appear verbatim in the
  declaration pins file (3/3).
- Declared supersession deltas are exactly: kill-rule-v2.py
  11907b35…→3b8c7583…, battery-v6.py a9ba5d46…→7d7d559a… (re-verified directly =
  7d7d559ac144eda6d163dd1d9ab26ed95ac089e18ccbb029bd91ae4277e46c06, byte-count independent),
  symlink-probe-v2.py pin UNCHANGED at 67b74a4b… (matches "probe v2 unedited by the
  supersession"), 6 forge .json files re-pinned, plus additive entries for the new
  receipt/evidence artifacts. Nothing else moved.

## Item 4 — supersession disclosure: PASS

- claims.json (sup) names the supersession commit hash `3baac2ef…` THREE times, once per
  disclosed `of` clause; the lane's HEAD is exactly that commit; no silent mutation of
  plan/manifests/mutant table/pre-receipts/SKILL.md/corpus (verified by `git diff
  --name-status` decl→sup: only the disclosed files + claims.json's additive keys).
- Red evidence exists and is honest: honest-pos-red-head-not-bound.{json,stdout,stderr,rc}.
  rc=1, stderr "selfverify reason: head-not-bound", stdout "selfverify ok=False reasons=1
  / repaired 12 of 12; … met True exit 1" — the fail-closed gate turning a green verdict
  into exit 1. JSON: head: null (root cause: resolve_rev(None) for HEAD), revision =
  declaration, met_target true, counter_sha256 = the PRE-fix v6 bytes a9ba5d46 (coherent:
  the run executed the pre-fix counters). Green evidence honest-pos.json (exit 0,
  selfverify ok=True reasons=0, head = declaration) also committed.
- v6 `verify_receipt` (sup bytes, read in full) implements every binding the plan
  asserts: schema-valid counts, label recompute + frozen-label membership, met direction,
  revision-not-bound, head-not-bound, counter/verdict/repair-pin-not-bound. K-forgeries
  in kill-rule-v2 passes the FIXTURE's OWN revision as the reference — the same shift the
  set → not half-aware (see residual): the head-mismatch fixture's head≠revision
  violation triggers head-not-bound regardless, so the intended tuned reasons still fire;
  I flag this as a discoverable-but-immaterial artifact of the fix (visible only when
  re-deriving WHY the forged revision satisfies the check).
- Extra receipt c1-at-decl-worktree.json (super-committed, name not frozen anywhere):
  kill-rule green at the working bytes — counts {mutants 10/10, forgeries 10/10,
  negctl 3/3, probe 1/1, honest 1/1}, exit 0, world_revision = declaration, revision
  = null (worktree, no clean checkout hash to name — consistent with the
  claim receipt's schema where `revision` names the measured clean tree and is null for
  worktree measurements). This is the sixth supersession's green_evidence; it is not
  named in claims.json but is referenced as "kill rule green at working bytes" in the
  commit subject. Immaterial: documentation-level, not contract-level.

## Residual risks / gaps

1. The frozen C1 target label arithmetic ("forgeries refused 10 of 10") counts only the
   six round-96 fixtures; the r95 forgery battery re-run is a separate regression gate
   (captured by K-forgeries' non-exact leg and/or the round-95 forgery instrument). A
   re-deriver who reads the label as "all forgeries ever" will mismatch the count.
   Documentation-level ambiguity, disclosed in the plan's frozen counting command notes.
2. The forged fixtures' revision/head fields sit at the BASE revision, NOT the
   declaration — deliberate (the frozen counting command runs K-forgeries against
   `--mutants`…`--fixtures` at whatever revision the checker resolves for the fixture
   world), but it means the forge fixtures do not bind to the declaration bytes, only to
   the pins baked inside them. Consistent with "world revision = base"; declared.
3. `verdict_sha256` (round-93 battery-v3 bytes) is bound into every receipt by value but
   has no *.py path pin in pins.sha256. Disclosed named limit; if v3 bytes were ever
   regenerated the pin file wouldn't catch it (only a receipt re-run would). Carried,
   not new.

## Tooling authorization record

No tool installed or updated. RULES.md read (official channels + update-safety gate).
All checks via existing git/python/coreutils.
