# R38CriticClaimsC2 — attack on frozen R38-C2 (calibration counter)

Seat: `R38CriticClaimsC2` (leaf critic, wave 1). Claim attacked: `plans/round-38-claims.md`
R38-C2 / P38-C2 (freeze `e059ca9391642d5b71b6662cabcbdce0d9308719`; controls
`efd5c47a72a50b3a434783f82268fb4a96e636a1`; base `77091b492cc53f8743bd0701b1e7d5e66123dd84`).
Counter under test: `tools/round-38/c2-counter.py` (frozen). Nothing was repaired in the lane;
every fixture lived in a scratch git clone and the counter was run read-only against it.

## 0. Bottom line — kill signals, stated plainly

1. **The frozen C2 counter is defeated by 8 shortcut payloads.** Five of them falsify the frozen
   predicate's own sentence ("every backticked lane-repo pointer in them resolves ... every pointer
   unresolved at the base repaired by a resolving pointer **to the same document**") while the
   counter returns `met_target: true`, exit 0:
   - **K1** shadow duplicate `## Core` row (bad pointer kept verbatim),
   - **K2** shadow duplicate `SHONEN.md` box (contradictory count kept verbatim),
   - **K3** shadow duplicate `## Owned axes` row (wrong count kept verbatim),
   - **K4** substitution by a **different document with the same basename** `evidence/doctor`
     (forged copies created during the claim round),
   - **K5/K6** decoy `## Core` row whose backticked lane path is unresolvable but written as a glob
     or a `#fragment`, i.e. invisible to the counter's token grammar.
   Two more (**K7/K8**) go green by rewriting the ground-truth input `evidence/round-1-2026-10-15/result.json`
   (2-of-2 or 14-of-14 obligations) — that is not a counter bug in the narrow sense, it is a
   **frozen-predicate hole**: P38-C2's "no unit removed" guard covers SCORECARD/SHONEN/PROVINCE
   rows only, never command B's obligation set.
2. **The base 1 mismatch is real.** Re-derived at `77091b49` and at the current integration tip
   `cb4326b2`: `mismatches 1`, `unresolved [["prov_core:REA MCP server","evidence/doctor/"]]`,
   `guards false`, exit 1. `evidence/doctor/` does not exist at the base; the intended
   `.ufo/waves/round-19/evidence/doctor/{doctor-6.5.0.txt,doctor-6.7.0.txt}` does.
3. **The four frozen C2 controls are all red** (exit 1, re-derived), but **`ctl-c2-2` and `ctl-c2-3`
   are the same fixture in effect** (byte-identical measured delta and guard state), and neither
   substitutes a *resolving* document. The `unrepaired` guard is therefore exercised only in its
   trivially-failing form — as soon as the substitute resolves with the same suffix (K4) the guard
   passes. The "fewer pointers" guard is never exercised by any frozen control.

A payload produced with K1..K4 would be admitted as "calibration: 0 mismatches" while the lane's
scored surface still contains the exact unresolved pointer the claim says was repaired.

## 1. Method (exact commands)

```bash
S=/fast/scratch/hyaku/kaidoku-r38/R38CriticClaimsC2; mkdir -p "$S"; export TMPDIR="$S"
git clone -q /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/fx"      # read-only on the lane
git -C "$S/fx" rev-parse --show-toplevel                                # -> $S/fx  (checked)
# per variant: git -C "$S/fx" checkout -q -B <branch> 77091b49...; apply edit; git commit; then
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-38/c2-counter.py \
  --root "$S/fx" --rev <branch-sha> --base 77091b492cc53f8743bd0701b1e7d5e66123dd84 \
  --json-out "$S/<branch>.json"
```

Fixture commits are ephemeral, so each variant is a script in
`.ufo/waves/round-38/w1/artifacts/R38CriticClaimsC2/repro/` (`variants.py`, `compose.py`,
`probes2.py`…`probes5.py`, all parameterised by `$S`). The full result matrix with every branch
sha and every counter field is `.../artifacts/R38CriticClaimsC2/variant-matrix.json`.
Baseline measurement: `.../base-measurement.json`. No tool was installed or upgraded.

## 2. Verdict matrix (frozen counter vs. 4-element corrected counter)

`mm` = `mismatches`, `met` = `met_target`. Full matrix in `variant-matrix.json`.

| fixture | rev | frozen exit | mm | guards_ok | frozen met | patched exit | patched mm | patched met |
|---|---|---|---|---|---|---|---|---|
| `v0` (base, do-nothing) | `77091b492cc5` | 1 | 1 | False | **False** | 1 | 1 | **False** |
| `v-intended-repair` (control-positive) | `8c726d12b482` | 0 | 0 | True | **True** | 0 | 0 | **True** |
| **K1** `c-shadow-and-range` | `f98b6e6cac4e` | 0 | 0 | True | **True** | 1 | 1 | **False** |
| **K2** `c-shonen-shadow-and-repair` | `4f4a331395c7` | 0 | 0 | True | **True** | 1 | 1 | **False** |
| **K3** `e2-shadow-owned-axis` | `855071d9dd13` | 0 | 0 | True | **True** | 1 | 1 | **False** |
| **K4** `v-same-basename-doc` | `31e142aa5379` | 0 | 0 | True | **True** | 1 | 0 | **False** |
| **K5** `e-decoy-glob` | `1d3ecf3c913f` | 0 | 0 | True | **True** | 1 | 1 | **False** |
| **K6** `e-decoy-frag` | `ff98e8abcaca` | 0 | 0 | True | **True** | 1 | 1 | **False** |
| **K7** `f-fewer-obligations` | `e7f9421a9566` | 0 | 0 | True | **True** | 1 | 1 | **False** |
| **K8** `f-extra-obligations` | `97400f7b0dba` | 0 | 0 | True | **True** | 1 | 1 | **False** |
| limit `c-junk-unit-and-repair` | `0f7f8ae6bb74` | 0 | 0 | True | True | 0 | 0 | True |
| limit `d-history-count` | `f423594eb7b0` | 0 | 0 | True | True | 0 | 0 | True |
| (c) `v-delete-padded` | `b149e1fb2c63` | 1 | 0 | False | False | 1 | 0 | False |
| (e) `v-remove-unit` | `7611180513e5` | 1 | 1 | False | False | 1 | 1 | False |
| (f) `v-decoy-row` (unique first cell) | `3fd19e7bc4b2` | 1 | 2 | False | False | 1 | 2 | False |
| (b) `v-shadow-row-before` (order control) | `b0c32db1d874` | 1 | 2 | False | False | 1 | 3 | False |
| (a) `v-junk-counts` | `497f8b302e45` | 1 | 1 | False | False | 1 | 1 | False |

## 3. The kills

All fixtures start from base `77091b49` and touch only the scored surfaces; the intended repair is
`evidence/doctor/` → `.ufo/waves/round-19/evidence/doctor/` in the single `| REA MCP server |` row.

### K1 — (b) shadow duplicate `## Core` row: `evidence/doctor/` stays verbatim, counter green

Fixture: insert **after** the bad row, still inside `## Core` (lines 39–72), a second row whose
first cell is again `REA MCP server` and whose two pointers (`.ufo/waves/round-19/evidence/province-pins-integrated.json`,
`.ufo/waves/round-19/evidence/doctor/`) resolve; and refresh `SHONEN.md` box 4 `PROVINCE.md:97-125`
→ `98-126` (the inserted line shifts `## Adjacent`, which is the only *collateral* red).

Observed (`f98b6e6cac4e`): `{"mismatches": 0, "unresolved": [], "guards_ok": true, "met_target": true}`,
exit 0, `pointers 48`, `unrepaired []`.

Cause: `units()` stores rows in a dict keyed by first cell (`u['prov_core:' + first_cell(l)] = l`),
so the **last** duplicate silently replaces the first. The predicate is violated — the committed row
still holds `` `evidence/doctor/` `` — but the counter never reads it.

Order sensitivity (evidence that this is dict overwrite, not luck): `v-shadow-row-after` (duplicate
**after** the bad row) yields `unresolved []`, `guards_ok true`, `mismatches 1` whose only cause is
the collateral `R3 SHONEN box4 Adjacent range` drift (`stated [97,125] observed [98,126]`);
`v-shadow-row-before` (duplicate **above** the bad row) leaves
`unresolved [["prov_core:REA MCP server","evidence/doctor/"]]` and `unrepaired` firing (`mismatches 2`).
So the semantics are "last row wins": a lane that appends a corrected twin at the bottom of Core
passes while the top row a reader sees is still broken — and the only thing that stopped the bare
`after` fixture was a line-count side effect, which the same fixture removes by refreshing the box-4
range (that is K1 above).

### K2 — (b) shadow duplicate `SHONEN.md` box: two contradictory counts, counter green

Fixture: change the first box's `17/17 rule blocks` → `3/3 rule blocks` (false: command A observes
17/17), then append a byte-identical second `- [~] SKILL.md contains real decision tables …` box with
the correct `17/17`. Observed (`4f4a331395c7`, with the intended pointer repair already applied):
`mismatches 0`, `assertion_mismatches []`, `guards_ok true`, `met_target true`.

Cause: `units()` keys SHONEN boxes by full box text (`u['shonen:' + m.group(1).strip()]`) and
overwrites; `O4`/`R2` read only the surviving copy. The file ships a self-assessment that contradicts
observed state, which is exactly what P38-C2 forbids.

### K3 — (b) shadow duplicate `## Owned axes` row: wrong count stays in the card

Fixture: the real `| coverage |` row's `124/124 knowledge files mapped` → `7/7 knowledge files mapped`,
then a duplicate `| coverage |` row carrying `124/124` and the same **six** lane pointers
(`corpus/knowledge/…r36…`, `corpus/knowledge/…unblob…`, `tools/round-36/c2-counter.py`,
`corpus/README.md`, `plans/round-36-claims.md`, `.ufo/waves/round-31/w1/ScribeScorecardRows.md`).
Observed (`855071d9dd13`): `met_target true`, exit 0, and `'7/7 knowledge files mapped' in SCORECARD.md`
→ `True`. Pointer count must be matched (`O1..O4` aside, `pointers_not_fewer` compares totals: an
unmatched duplicate scored 46 < 48 and went red — the guard is a **global** count, not per row).

### K4 — (d) substitution by a different document with the same basename

Fixture: create `corpus/evidence/doctor/doctor-6.5.0.txt` and `doctor-6.7.0.txt` containing `forged`,
and repoint the Core row to `` `corpus/evidence/doctor/` ``. **This is the assignment's variant (d).**
Observed (`31e142aa5379`): `{"mismatches": 0, "unresolved": [], "guards_ok": true, "met_target": true}`,
exit 0.

Cause: the repair guard is a pure path-suffix test —
`p2.rstrip('/') == path or p2.rstrip('/').endswith('/' + path)` with `path == 'evidence/doctor'` —
so *any* directory whose path ends in `/evidence/doctor` counts as "the same document". The intended
tree `.ufo/waves/round-19/evidence/doctor/` is never referenced. A lane can therefore satisfy C2 by
writing its own copy of the evidence during the claim round (false provenance).

### K5 / K6 — (f) decoy `## Core` row whose pointer is invisible to the token grammar

Fixtures (each on top of the intended repair, plus the `98-126` box-4 refresh):
- K5 row cell: `` `corpus/evidence/round-38/c1/*` `` (unresolvable glob) → `1d3ecf3c913f`,
  `mismatches 0`, `guards_ok true`, **met_target true**, `pointers 48`.
- K6 row cell: `` `corpus/evidence/round-38/c1/K1/after.json#L5` `` (unresolvable fragment) →
  `ff98e8abcaca`, same verdict.

Cause: `PTR = ^([A-Za-z0-9_.][A-Za-z0-9_./+-]*?)(?::(\d+)(?:-(\d+))?)?$` — any token containing
`*`, `?`, `#` fails the match and is **dropped**, so a new unresolved lane pointer is neither an
`unresolved` entry nor a guard failure. The same evasion exists for a reference written without
backticks (`d-decoy-plaintext`, `7129d46e0471`): invisible by construction. Any new "receipts
pending" pointer in a glob form is free.

### K7 / K8 — (a)/(e) command-B evidence rewrite: obligations are units the guard does not count

Fixtures (on top of the intended repair):
- K7 `f-fewer-obligations` (`e7f9421a9566`): rewrite `evidence/round-1-2026-10-15/result.json` to keep
  only the first two `aligned` obligations and state `2/2 preselected reconciliation obligations
  aligned`. Counter: `observed.command_b [2,2]`, `mismatches 0`, **met_target true**.
- K8 `f-extra-obligations` (`97400f7b0dba`): append five `{'id': 'junkN', 'status': 'aligned'}`
  obligations and state `14/14`. Counter: `observed.command_b [14,14]`, `mismatches 0`, **met_target true**.

This is "junk counts that still match" (a) and "removing a unit" (e) in their strongest form: the
denominator of the calibration observable is editable, `rubric.json`'s nine frozen obligations are
never consulted, and `guards.missing_units` only tracks SCORECARD/SHONEN/PROVINCE rows. A lane can
make the number agree with the card by editing the ground truth.

## 4. Variants the counter does defend (report, do not "fix")

- **(c) deletion of the bad pointer**: `v-delete-padded` (`b149e1fb2c63`) — pointer deleted,
  padding attempt landed outside the scored `## Core` span → `pointers 47 < base 48`
  (`pointers_not_fewer false`) and `unrepaired [["prov_core:REA MCP server","evidence/doctor"]]`; red.
  Deletion is caught by the conjunction of the global-count guard and the same-unit repair rule.
- **(e) removing a unit**: `v-remove-unit` (`7611180513e5`) — deleting the round-36 squashfs
  Capabilities row → `missing_units ["cap:REA SquashFS recursion through sasquatch (LE v4)"]`,
  `pointers 45 < 48`; red.
- **(f) decoy row with a unique first cell**: `v-decoy-row` (`3fd19e7bc4b2`) — bad row untouched →
  `unresolved ["evidence/doctor/"]`; red. (Only the *masked* forms K5/K6 escape.)
- **(a) junk count that matches**: this is self-consistent by design — stated values are compared to
  command A/B at the measured revision, so `c-junk-unit-and-repair` (`0f7f8ae6bb74`) is green with one
  empty 1-line `corpus/knowledge/2026-10-26-zzz-stub.md` plus one README coverage-map token counted as
  `125/125 knowledge files mapped`. Not a predicate violation (P38-C2 defines the counts by command A),
  but it shows there is **no quality floor**: the count is index arithmetic, and the SCORECARD's own
  text says so ("index integrity only").
- `d-history-count` (`f423594eb7b0`): `999/999 at cab59f22…` inside the scored coverage cell is green —
  the revision-labelled historical recounts are never re-measured. Also predicate-scope (the predicate
  names only "the four stated counts"), disclosed as a limit, not a kill.

## 5. Base-mismatch verification (assigned check: real?)

```
$ python3 -I -B tools/round-38/c2-counter.py --root <lane> --rev 77091b49… --base 77091b49…
{"assertion_mismatches": [], "guards_ok": false, "met_target": false, "mismatches": 1,
 "unresolved": [["prov_core:REA MCP server", "evidence/doctor/"]]}          exit 1
   pointers 48, base_pointers 48, base_unresolved [["prov_core:REA MCP server","evidence/doctor"]],
   unrepaired [["prov_core:REA MCP server","evidence/doctor"]]
$ python3 -I -B tools/round-38/c2-counter.py --root <lane> --rev cb4326b2… --base 77091b49…
{"mismatches": 1, "unresolved": [["prov_core:REA MCP server","evidence/doctor/"]]}   exit 1
$ git -C <lane> ls-tree -r --name-only 77091b49 -- evidence | head
evidence/round-1-2026-10-15/{baseline,rea-bundle,result,rubric}.json      # no evidence/doctor/
$ git -C <lane> ls-tree -r --name-only 77091b49 -- .ufo/waves/round-19/evidence/doctor
.ufo/waves/round-19/evidence/doctor/doctor-6.5.0.txt
.ufo/waves/round-19/evidence/doctor/doctor-6.7.0.txt
```

Real: the row's `evidence/doctor/` is at `PROVINCE.md:44`, inside `## Core` (38–72), it does not
resolve at the base, and the claimed intended document is committed at the base (so K4's forged copies
are unambiguously *not* it). The live integration tip is still at this 1 mismatch — the claim's
before-number is accurate and unimplemented.

## 6. Control verification (assigned check: not green?)

Re-derived by importing the committed generator (`tools/round-38/gen-controls.py`) and running the
frozen counter on fresh fixtures; receipts in `.../artifacts/R38CriticClaimsC2/control-rederivation.json`.

| control | re-derived exit | mismatch detail | guards |
|---|---|---|---|
| `ctl-c2-0` do-nothing @ base | 1 | `unresolved [["prov_core:REA MCP server","evidence/doctor/"]]` | `guards_ok false` |
| `ctl-c2-1` junk count | 1 | `O1 stated [999,999] observed [3,3]` — matches the committed receipt exactly | `guards_ok false` |
| `ctl-c2-2` "delete the bad pointer" | 1 | `pointers 4 < base 5`, `unrepaired [["prov_core:REA MCP server","evidence/doctor"]]` | `guards_ok false` |
| `ctl-c2-3` "substitute other resolving documents" | 1 | **identical to c2-2**: same removed lines, same `pointers 4`, same `unrepaired` | `guards_ok false` |

No control is green — the kill rule is not tripped by the frozen controls. Two defects in the control
*set*, not in the verdicts:

1. **c2-2 and c2-3 are the same test.** Both replace the Core row's `` `evidence/doctor/` `` with
   `docs/x.md`-class text; `docs/x.md`/`d/y.md`/`x.md` do not match
   `LANE = ^(corpus/|tools/|\.ufo/|plans/|evidence/|scripts/|considerthese/|SCORECARD\.md|…)`, so the
   replacement is not a pointer at all. Neither control substitutes a *resolving* document, and the
   only difference between the fixtures (`cap_ptr` `x.md` vs `d/y.md` in an unscored Capabilities cell)
   cannot reach the measurement. Verified: `git diff <base> <rev> --name-only` is `PROVINCE.md`,
   `SCORECARD.md` for both, and the removed lines are
   `| REA MCP server | x | \`evidence/doctor/\`  |` for both.
2. **Two guards are never exercised by any frozen control**: `pointers_not_fewer` in its intended
   form (delete with the total held constant) and `unrepaired` in its *passing-but-wrong* form — K4.
   The receipts also cite scratch fixture revisions (`87dc8502…`, `d8fe10c7…`, `21028bcd…`) that were
   deleted by `shutil.rmtree`, so they are regenerable but not replayable from committed bytes; only
   the generator is an artifact. (Same class as routed R36-CL6: receipt identity should be the subject
   digest, here the fixture tree digest, not a dead revision id.)

Corroboration, independently reached: while this review ran, an in-flight uncommitted edit to
`plans/round-38-claims.md` (not mine — the C2 predicate, target, counting command and kill rule are
byte-identical to freeze `e059ca93`; I diffed that section) added a wave-1 disclosure that "several
red cases fail via `guards_ok` rather than the named clause, and three cases use paths the LANE
allowlist rejects". That is the same attribution weakness as point 1 above. My K1..K8 findings are
*not* covered by it: they are green payloads, not mis-attributed reds.

## 7. Smallest safe correction (drafted, not applied)

`.../artifacts/R38CriticClaimsC2/c2-counter-minimal-patch.diff` — four mechanical edits to
`tools/round-38/c2-counter.py`, no change to the predicate, carriers, oracle or receipts:

1. **Duplicate units are mismatches.** `units()` records repeated first cells (Owned axes,
   Capabilities, `## Core`, `## Frontier`, SHONEN boxes) into `duplicate_units` and counts each once
   in `mismatches` and forces `guards_ok false`. This closes K1, K2, K3 with one rule.
2. **A repair must point at a document that already existed at the base**:
   `exists(root, base, p2.rstrip('/'))` added to the `unrepaired` predicate. This closes K4 without
   changing the suffix rule (the intended `.ufo/waves/round-19/evidence/doctor/` exists at the base;
   forged `corpus/evidence/doctor/` does not).
3. **Tokens that name a lane path but not a numeric range are still pointers**: widen `PTR` to admit
   `*?#` so such tokens are tested for existence instead of dropped. This closes K5/K6.
4. **Command B's input is pinned to the base blob**: add `G0 command-B evidence pinned to base`
   comparing `git rev-parse <rev>:evidence/round-1-2026-10-15/result.json` with the base blob id.
   This closes K7/K8.

Verification of the correction (same matrix, `patched` columns):

- all 8 kills → exit 1 (`c-shadow-and-range` 1, `c-shonen-shadow-and-repair` 1, `e2-shadow-owned-axis` 1,
  `v-same-basename-doc` 1, `e-decoy-glob` 1, `e-decoy-frag` 1, `f-fewer-obligations` 1,
  `f-extra-obligations` 1);
- the intended repair stays green: `v-intended-repair`, `c-repair-only` → exit 0, `met_target true`;
- the frozen 14-case selftest still passes unchanged:
  `{"selftest": "c2-counter", "cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}`;
- no false positives on real history: at `77091b49` and `cb4326b2` the patched counter returns
  `mismatches 1`, `duplicate_units []`, same single `unresolved` (`artifacts/patched-at-base.json`);
- still green after the patch, and left as disclosed predicate-scope limits, not kills:
  `c-junk-unit-and-repair` (count equality is by definition) and `d-history-count` (historical
  recounts are not among "the four stated counts").

If the L1 wants to keep the frozen predicate byte-exact, the alternative is not a counter change but
a **disclosure**: C2 must not be admitted on a revision whose green came from any of K1..K8, and the
after-receipt must be read with the projection above. I did not edit the counter, the predicate, the
carriers, the oracle or any receipt.

## 8. Impacted axes

- **calibration** (C2's own axis): direct. A C2-green payload built on K1..K4 reports zero mismatches
  while the card still carries the unresolved pointer and the fabricated document — the axis would
  move on a false observation.
- **coverage**: indirect but real. K1/K3 show that any *count* surface (knowledge-map rows, rule
  blocks, obligation denominators) can be shadowed or re-based; the same `units()` mechanism scores
  the depth/coverage observables, so a coverage claim built on the same pattern would inherit K1/K3.
- **freshness/provenance**: K4 and K7/K8 are provenance defects (self-authored "evidence" satisfying
  its own counter). The claim's C1 half is unaffected (C1 reads no SCORECARD/SHONEN), so the two
  claims remain separable — my fixtures touched only C2's surfaces.

## 9. Limits of this review

- I attacked the **counter against its predicate**, not the truth of C1, and ran no REA extraction.
- Fixture revisions are ephemeral by design; the scripts in `repro/` regenerate them. The *lane*
  revisions quoted in this report are the base/freeze/control commits above.
- The 4-element patch is a draft for the L1/round-39: applying it in round 38 would change a frozen
  counter (forbidden here).
- The lane working tree was dirty while I measured (`plans/round-38-claims.md`,
  `tools/round-38/c1-counter.py` modified; not mine). Every fixture was taken from committed base
  `77091b49`, and `tools/round-38/c2-counter.py` is unmodified (`git status --porcelain` empty for it),
  so no result here depends on the dirty files.
- `c-junk-unit-and-repair` and `d-history-count` are green under both counters; whether they are
  acceptable is a predicate question the canonical judge must answer, not a counter fix.

## 10. Artifacts (all under `.ufo/waves/round-38/w1/artifacts/R38CriticClaimsC2/`)

| file | sha256 | content |
|---|---|---|
| `base-measurement.json` | `826880a3…` | frozen counter at `77091b49` (1 mismatch, 48 pointers) |
| `variant-matrix.json` | `84108fc1…` | all 24 fixtures: branch, sha, frozen + patched verdicts |
| `control-rederivation.json` | `89600dc3…` | c2-2/c2-3 full guard detail and removed lines |
| `composed-and-controls-raw.json` | `0fa87ab4…` | composed-fix runs + regenerated c2-1/2/3 outputs |
| `patched-at-base.json` | `0560e756…` | patched counter on the real lane at base (no false positives) |
| `c2-counter-minimal-patch.diff` | `85f3d734…` | 4-element draft correction |
| `repro/{variants,compose,probes2,probes3,probes4,probes5}.py` | — | regeneration drivers (parameterised by `$S`) |

Scratch `/fast/scratch/hyaku/kaidoku-r38/R38CriticClaimsC2` (clone, fixtures, patched counter copy)
was removed after the artifacts were copied; nothing outside this report and that artifacts directory
was written.
