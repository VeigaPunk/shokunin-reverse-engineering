DONE — R42-V3 repaired as a 4-line insertion (one status sentence per block); the patch applies cleanly to the base and reproduces the edited file byte-for-byte, the v4 table region / the counter's v4 `rule_block` / the v3 table region all `cmp` equal to `d1681696`, the frozen interpreter parses 15 rules unchanged and labels all 78 committed dev envelopes identically, and SCORECARD command A stays 21/21 with citations resolving.

# R43SkillMark — in-SKILL claim status for SKILL rule blocks 20 and 21 (routed defect R42-V3)

Seat: `R43SkillMark`, round 43 wave 1 (pre-freeze). Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base
`6b9e64fe7e0de202d9383baad5792fbfe039a743`. Nothing frozen; the L1 integrates and commits. I wrote only my report and
`…/.ufo/waves/round-43/w1/artifacts/R43SkillMark/`.

## 1. Deliverables

| path (under `artifacts/R43SkillMark/`) | what |
|---|---|
| `skill-r42v3-status.patch` | the exact edits, unified diff against `git show 6b9e64fe…:SKILL.md`; `a/SKILL.md` `b/SKILL.md` prefixes so `git apply -p1` works from the lane root. sha256 `7378eccb…b9f7377f` |
| `SKILL.edited.md` | the resulting document (1572 lines). sha256 `32fb1a26…13c03b724` |
| `SKILL.base.md` | `git show 6b9e64fe…:SKILL.md` (1568 lines). sha256 `2288e088…f2fc1b3f0` |
| `region-extract.py` | the region extractor (interpreter-documented rule + counter `rule_block`) |
| `evidence/` | region cmp receipts, interpreter `--table-only` output, label diffs (3 required + all 78), command A JSON, census before/after JSON + delta, citation-drift before/after |

Artifact bytes are small; scratch (`/fast/scratch/hyaku/kaidoku-r43/w1-R43SkillMark`) is removed and every cited byte
lives in `evidence/`.

## 2. The diff (exact)

```diff
--- a/SKILL.md
+++ b/SKILL.md
@@ -435,6 +435,8 @@
   and the firmware input limit is 128 MiB with a 120 s timeout per run (S119
   `FirmwareRelease.js:27-32`).
 
+  **Status — unscored claim.** Table v3 carries no scored claim: R41-C2 stopped at the round-41 scoring on a counter key mismatch, not on the table — the C2 counter took the combo carriers' declared tuple under `class_expected.features`/`features`/`declared_features` while the generator wrote it under `declared` (M41-1, R41-CL1), so R41-C2 exited 1 with `observed_features_match_declared` false (receipt `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json`, `matched 52` of `n 52`) — and v3 is superseded for routing and for the action column by rule block 21 (table v4).
+
   <!-- sqfs-triage-table v3 -->
   <!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty -->
   | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
@@ -518,6 +520,8 @@
   `-be` reads `n/a`), which is why no row below requires `yes`. The firmware input limit is
   128 MiB with a 120 s timeout per run (S119 `FirmwareRelease.js:27-32`).
 
+  **Status — unscored claim.** Table v4 matched its independent evaluator 78 of 78 at `eb8215ac` (receipt `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`, `pair_mismatches []`, `evaluator_missing []`, `evaluator_extra []`), but R42-C2 stopped on `observed_features_match_declared` — combo C02 declared the gap set {`extractor-failure`, `unpublished-entry`} while its own extraction run also observed `depth-limited` (M42-2, R42-CL1) — so the table is unscored as a claim and round 43 re-scores it under P43-C1.
+
   <!-- sqfs-triage-table v4 -->
   <!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be cross-read-legacy isolate-residue preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty -->
   | label | operation | provider | handler | failing handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |
```

`git diff --no-index --numstat SKILL.base.md SKILL.edited.md` → `4  0` (four insertions, no deletion, no byte of an
existing line touched). Each status sentence is one physical line, 2-space indented so it stays inside the bullet, and
it does not begin with `- **`, `|` or `#` — command A's `re.split(r'(?m)^- \*\*', craft)` therefore still yields 21
rule blocks, and neither sentence adds a `corpus/knowledge/…md` reference.

Apply proof (pristine clone of the lane at base, fixture identity `-c user.name=fx -c user.email=fx@fx`):
`git apply --check -p1` exit 0 → `git apply -p1` exit 0 → result `cmp`-equal to `SKILL.edited.md`; fixture commit
`affcac31d0d9e62b7d5da8d0e4ceb635f8686402`, `SKILL.md | 4 ++++`.

## 3. Placement, and why it is forced

The claim (`plans/round-43-claims.md`, P43-C1) freezes **the v4 table region = the v4 marker line through the end of
the first markdown table after it**, and the frozen round-42 counter additionally binds
`v4_block_identical`/`skill_block_drift` on `rule_block()` = marker line → next `- **` bullet / ATX heading
(`tools/round-42/c2-counter.py:295-320`). Anything inserted **at or after** the marker — including between the table
and the next heading — changes one or both. So each status sentence sits at the **end of the block's prose,
immediately before that block's marker line**, and both regions are provably untouched.

## 4. Region `cmp` — v4 table region is byte-identical to the round-42 freeze

Extraction script implements the frozen interpreter's documented rule ("the FIRST markdown table that follows a line
containing the marker … plus the closed action vocabulary declared by the line directly above that table") and,
separately, the counter's `rule_block()`:

```
$ python3 -I -B region-extract.py --skill <SKILL> --mode table      # P43-C1 region
$ cmp reg.freeze.table reg.base.table    -> exit 0   (base already equalled the freeze here)
$ cmp reg.freeze.table reg.edited.table  -> exit 0   <-- the requirement
$ sha256sum reg.*.table
99cd54d7fe8847486175db9fbf06fa4da3c891a17dd74ffc00eacd64c8ddd6da  reg.freeze.table
99cd54d7fe8847486175db9fbf06fa4da3c891a17dd74ffc00eacd64c8ddd6da  reg.base.table
99cd54d7fe8847486175db9fbf06fa4da3c891a17dd74ffc00eacd64c8ddd6da  reg.edited.table      (19 lines: marker, actions, header, sep, 15 rows)

$ python3 -I -B region-extract.py --skill <SKILL> --mode ruleblock  # counter v4_block_identical region
$ cmp rb.freeze.txt rb.edited.txt        -> exit 0
b967a30d…b4ccbd  (22 lines, identical in all three states)

$ --mode table --marker '<!-- sqfs-triage-table v3 -->'             # v3 table, not frozen by P43-C1
5ecae76f…3cc5f7f1 (16 lines, identical in all three states)
```

So landing this edit cannot trip `v4_block_identical`, `skill_block_drift`, or the round-43 predicate's byte-identity
clause. Note the base already differs from `d1681696` by one **prose** line (457, the block-21 citation added by
`46486e7a` *after* the round-42 freeze); that line is outside the frozen region, which is why `cmp` passes at the base
too — measured, not assumed.

(Observed mid-wave, for the L1's attention: `plans/round-43-claims.md` is modified in the working tree by the L1 —
R43-C1's axis moves from depth to calibration and the freeze-integrity rule is tightened. I re-read the revised
P43-C1 clause; its region definition is unchanged ("from the line containing `<!-- sqfs-triage-table v4 -->` through
the end of the first markdown table after it … byte-identical to the same region at `d1681696`"), so this patch's
placement remains compliant under the revised text. That file is the L1's, not mine: I did not write it.)

## 5. Frozen-interpreter verification

Interpreter is the `git show` copy of `tools/round-42/sqfs-triage-v4.py`, sha256
`497bab6766a0b0c6d6f36cb58cadc531bddf9dd3231f6100bf46cf6ff552a2e9`, git blob `79265904…` at **both** `6b9e64fe` and
`d1681696` (unchanged, as the claim requires).

`--table-only`: **exit 0**, `rules: 15`, actions line unchanged, and the parsed rule text + action vocabulary is
byte-identical to the base parse (`diff <(tail -n +3 base) <(tail -n +3 edited)` empty; both sha
`87fff6d6…e9143166f1`). Only the reported line numbers move: marker/actions/table `521/522/523 → 525/526/527`.

Labels — the three required **committed** round-42 dev envelopes, frozen interpreter CLI, base vs edited:

```
C02/envelope.json  partial-body-failure  salvage-partial
H11/envelope.json  mixed-symlinks        audit-symlinks
H23/envelope.json  no-squashfs-chunk     inspect-input
$ diff labels.base.txt labels.edited.txt   -> empty (identical)
```

Superset (all 78 committed dev envelopes, both skills): `diff` empty, both files sha `914bf9c4…6102af3`; 16 distinct
`(label, action)` pairs exercised. An in-process cross-check (importing the frozen interpreter, 78 envelopes) also
reports `label/action mismatches base-vs-edited: 0`.

## 6. SCORECARD command A (recipe A, verbatim from `SCORECARD.md:92-123`)

Run in the fixture clone, `--rev` = base and `--rev` = the commit that carries the patch:

```
base   6b9e64fe: {"citation_resolved_rules": 21, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
                  "knowledge_files": 135, "mapped": 135, "missing": [], "revision": "6b9e64fe…", "rule_blocks": 21}
edited affcac31: {"citation_resolved_rules": 21, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
                  "knowledge_files": 135, "mapped": 135, "missing": [], "revision": "affcac31…", "rule_blocks": 21}
```

**21/21 rule blocks, citations resolving, depth 10.0, coverage 135/135 — unchanged.** Rule 20 keeps
`2026-10-26-r41-sqfs-triage-v3.md:11-25` (111 lines) and rule 21 keeps `2026-10-26-r42-sqfs-triage-v4.md:1-14`
(88 lines); the status sentences add no knowledge reference, so no rule can be invalidated by a bad range.

## 7. First-hand grounding of the two sentences

Every number in the inserted text was re-derived this round, not copied from a lesson:

- **R41-C2 stop**: `.ufo/waves/round-41/l1/scores/c2-at-e9a24d07.json` → `exit_code 1`, `matched 52`, `n 52`,
  `met_target false`, `bindings_false ["observed_features_match_declared"]`, `pair_mismatches` empty. Cause
  re-read from `corpus/lessons/round-41.md` M41-1 and `corpus/lessons/round-41-verifier-spotcheck.md:58`: the combos'
  declared tuple sat under manifest key `declared`, the frozen counter read
  `class_expected.features`/`features`/`declared_features`. Hence "stopped on a counter key mismatch, not on the table".
  (Precision note vs the seat brief: 52/52 **labels** matched their evaluator; the claim's failure was the declared-tuple
  binding alone. The sentence says so.)
- **R42-C2 stop**: `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` → `matched 78`, `n 78`, `pair_mismatches []`,
  `evaluator_missing []`, `evaluator_extra []`, `exit_code 1`, `met_target false`,
  `bindings_false ["observed_features_match_declared"]`, `counter_sha256 f1089167…` (the round-42 verifier spot-check
  reports the same). Combo C02 re-derived with the frozen counter's own `observed_features()`:
  observed `{depth-limited, extractor-failure, unpublished-entry}` vs manifest-declared
  `{extractor-failure, unpublished-entry}`; `combo: true`, `pair_match: true`, `features_match: false`.
- `plans/round-43-claims.md` names the round-43 predicate **P43-C1**, which the v4 sentence cites.
- SHONEN.md:6 already states both statuses in prose; this edit makes them exist **in SKILL.md**, which is what R42-V3
  asked for.

## 8. No-harm on the lane's gates (measured, both directions)

- **`c1-census-v10.py`** — **pre-existing red at the base**: `VERDICT FAIL`, `undeclared=44`, `stale=1`,
  `declared_fail_classes ['FRONTIER-UNEVALUABLE']`, 8 scope errors (including the already-ambiguous
  `r17-go-carrier-diagnostics.md` anchor and an absent marker at `SKILL.md:511`). I therefore compared instead of
  claiming green: every classified bucket is identical before→after (stale 1/18, ambiguous 0/0, undeclared 44/52,
  unresolved 0/0, current-ok 4/4, historical 8/13 asserts), `SKILL.md` loci 24→24, frontier errors identical (24),
  declared fail classes identical, verdict FAIL→FAIL, exit 1→1. The **only** delta is the prose quoted by the
  pre-existing `SKILL.md:511` marker error, which changed because line 511 moved — same error, same count, same class.
- **`citation-drift-probe.py`** — 11 findings before and after; full-output `diff` differs only in the
  `CITATION_DRIFT_REV_REQUESTED`/`_RESOLVED` lines. Its SKILL.md line pins (`:246 :248 :252 :254`) are all above the
  insertion point; its other SKILL.md entries are content anchors.
- Note recorded for the L1 so nobody mistakes a harness artifact for an instrument defect: a shell using `mapfile` +
  process substitution stalled twice here; the bare frozen-interpreter CLI handles **78 envelopes in ≈1 s**, exit 0.
  The interpreter is fine.

## 9. Risks / things the L1 owns

1. **Line shift.** +2 lines per block, +4 total: `SKILL.md` 1568 → 1572; v3 marker `438→440`, v4 marker `521→525`,
   actions `522→526`, table `523→527`; everything below shifts by 2 or 4. Dated records stay true as written
   (`SCORECARD.md:24` `SKILL.md:387-449`/`81-449` and `SHONEN.md:6` `81-449` are explicitly pinned at `e1c83313` /
   round 41). If the round-43 current-surface line ranges are to be restated, that is a `SHONEN.md`/`SCORECARD.md`
   edit — outside this seat's write scope.
2. **Placement is load-bearing.** Do not move either sentence to the other side of its marker: the v4 side would break
   P43-C1's byte-identity and the counter's `rule_block` binding (proved above, both directions).
3. **The status lines are temporary and greppable** (`**Status — unscored claim.**`, one per block). When a round's
   claim verifies, delete exactly one line per block; the blank separators then collapse cleanly.
4. **Untouched by me**: `corpus/SOURCES.md` (S135), the round-42 fixtures, `tools/round-43/*` (another seat's), the
   round-42 stop receipt `c2-at-eb8215ac.json`. `plans/round-43-claims.md` is the L1's and the L1 is editing it
   mid-wave (§4); I read it, never wrote it. No tool was installed or upgraded. No extractor or REA run of any kind was
   performed — readers only, and only on committed JSON envelopes.

## 10. Cross-domain evidence

None encountered. The whole move reads committed JSON/genuine lane text; no native binary, firmware image, or
third-party artifact was executed or inspected.

Report: `.ufo/waves/round-43/w1/R43SkillMark.md`
