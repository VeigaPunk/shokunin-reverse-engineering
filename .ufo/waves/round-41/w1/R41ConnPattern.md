# R41ConnPattern — cross-tool pattern finder (path-domain comparisons + stale embedded copies)

Verdict: **DEFECTS FOUND** — one live inherited suffix-matcher in the round-41 generator draft, two latent
basename/diagnostic variants in round-41 drafts, one confirmed-but-never-routed cross-root fixture defect in the
frozen round-40 interpreter, plus two routed round-40 defects confirmed fixed in the round-41 drafts.

Seat: R41ConnPattern (leaf). Base `49096c7e6f226af0c750c4b003be58883cb6049f` (verified `git rev-parse HEAD`).
No REA/unblob/sasquatch runs (seat names no extractor work); all evidence is static reads plus stdlib-only Python
drivers over committed bytes and peer round-41 tool drafts. Machine-readable hits:
`artifacts/R41ConnPattern/hits.json`; evidence transcripts `artifacts/R41ConnPattern/evidence-*.txt`,
`evidence-M1-table-divergence.diff`.

## 1. What I searched

- `tools/round-38`, `tools/round-39`, `tools/round-40` at the base for: `endswith`, `startswith`, `basename`,
  ` in ` substring tests, `same_rel`/path-equality helpers, `relpath`/`normpath`/`realpath` joins
  (path-domain comparisons within or across two roots), and embedded document copies
  (triple-quoted `TABLE_BLOCK`s, expectation tables, per-round constants) that can go stale (R40-CL5 M1 class).
- Round-41 drafts already in flight under `.ufo/waves/round-41/w1/artifacts/`
  (R41C1Counter, R41C1Extra, R41C1Fetch, R41C1LCarriers, R41C2Counter, R41C2Interp, R41C2Gen) scanned for
  inheritance of every hit.

## 2. Class A — suffix/`endswith`/basename/`in` on paths (R40-CL1 class)

| id | hit | status | round-41 inheritance |
|---|---|---|---|
| A1 | `tools/round-40/c1-counter.py:606-607` `same_rel` (`candidate == rel or candidate.endswith('/' + rel)`; used at :638 `oracle_hits`, :647 `nonregular_published`, :682 `gap_check`) | frozen defect R40-CL1 (confirmed by closure plain-read) | **FIXED** in `artifacts/R41C1Counter/c1-counter.py:769-803`: `extract_rel(path, root)` is component-exact against a `subject_root` derived from the receipt (:743-766, ambiguity fails closed); the old rule survives only as `legacy_same_rel` (:810) so each selftest collision case asserts the defect shape mis-scores what `same_rel` scores right. Both collision directions self-tested at :2064-2071 (`usr/bin/busy` vs `bin/busy` and `sbin/tool` vs `usr/sbin/tool`). `root_prefix` (:705) identifies the extract dir by a component-level `endswith('_extract')` — suffix on one component, governs root derivation only, fails closed on ambiguity; noted, not a defect at receipt-path granularity. |
| A2 | `tools/round-39/c1-counter.py:229-230` `same_rel` (uses :279-281, :294-297, :307-310) | origin of A1 | superseded, not ported |
| A3 | `tools/round-38/c1-counter.py:137-140` `matched()` | earlier lineage | superseded, not ported |
| A4 | `tools/round-37/c1-counter.py:116` | earliest occurrence (lineage note; out of seat scope) | superseded |
| A5 | `tools/round-38/c2-counter.py:222-231` pointer-repair suffix: a base pointer counts as repaired by any current pointer `p2` with `p2.rstrip('/').endswith('/' + path)` | latent false-"repaired" (same shape the r38 `intended-doc.py` M38-6 seat fixed for the positive arm) | **NOT inherited**: r39/r40/r41 c2-counters drop the repair arm (`grep -c endswith tools/round-40/c2-counter.py` = 0). Failing input on r38 semantics: base `evidence/x.txt` "repaired" by materialising a stub at `docs/y/evidence/x.txt`. |
| A6 | `tools/round-39/heldout-gen.py:141-147` and `tools/round-40/heldout-gen-v2.py:272-279` `writer_logical_path`: `resolved.endswith(marker[:-1])` canonicalises any path ending in `tools/round-39/gen-squashfs.py` to the lane-relative logical path | suffix canonicalisation erases the writer's true location from the manifest | **INHERITED VERBATIM** at `artifacts/R41C2Gen/heldout-gen-v3.py:487-490`. Demonstrated (`evidence-E1-writer-logical-path.txt`): a writer copy at `$S/deep/mirror/tools/round-39/gen-squashfs.py` — and at a fleet mirror — both canonicalise to `'tools/round-39/gen-squashfs.py'`. Blast radius is manifest provenance (the binding pin is the writer sha256, which is computed from the real file), but the manifest then asserts a lane-relative writer path for a file that is not in the lane. Failing input: run the generator from a sandbox clone/scratch whose tree contains any `…/tools/round-39/gen-squashfs.py` copy and read `manifest.generator.writer.path`. |
| A7 | `tools/round-40/c1-counter.py:597-604` `provenance_ok`: `PROV_SEGMENT not in output_directory` | substring `in` on a path; guards (absolute, no `..`, trailing-slash segment) leave no false pass I could construct | **inherited with the segment updated** to `/kaidoku-r41/` (`artifacts/R41C1Counter/c1-counter.py:232,:635`). If the port had kept `/kaidoku-r40/`, round-40 receipts would pass provenance — the constant flip is load-bearing. |
| A8 | `artifacts/R41C1DevCore/devcore-probe.py:166` diagnostic tail bucket `r == rel or r.endswith('/' + rel)` | probe only (gating `hits` is exact at :152-156); a collision-shaped regular file with no exact-published oracle row is bucketed as `depth_mismatch` ("published under another extract root") rather than flagged as a name collision | live in a probe, not a gate; flagged so the probe's bucket names are not read as verdicts |
| A9 | `artifacts/R41C2Counter/c2-counter.py:408-415` `norm_id`: join key is the basename with `.json` stripped | basename class; safe only while envelope basenames are unique carrier ids | **live in draft** (replaces r40's `os.path.normpath` argmap join — hazard shape changed, not eliminated). Demonstrated (`evidence-E4-norm-id.txt`): `norm_id('corpus/.../H05/envelope.json') -> 'envelope'`, and `setA/H07.json` / `setB/H07.json` both join as `'H07'`, so two distinct envelopes sharing a basename would collide silently (`out[cid] = val`). Today's layout materialises `<id>.json` (:895-897) so the join holds; the hazard is latent for any layout change. |

## 3. Class B — comparisons of paths across two roots

| id | hit | status | round-41 inheritance |
|---|---|---|---|
| B1 | `tools/round-40/sqfs-triage-v2.py:137-140`: `HELDOUT_DIR = LANE + '/corpus/evidence/round-39/c2/heldout'`, `C1_DIR = …/round-39/c1` while `HELDOUT_EXPECT` (:838-858) and the R40-C2 claim target the round-40 heldout set (H01..H20 + H21..H26) | **confirmed defect, never routed.** Same id denotes different envelopes across roots: `H05` labels `escaping-symlink-removed` in round-39 bytes but `clean-empty` in round-40 bytes. The v2 selftest's "committed-heldout" and "heldout-manifest-agrees" cases therefore validate the interpreter against **round-39** envelopes/manifest, not the set the claim scores. Prior waves observed the path (`w2/R40W2Sentinel.md`, `w1/R40C2Interp.md`: "selftest-only") and treated it as benign because the scoring path reads the manifest; it was not filed in `## Routed defects into round 41` | **FIXED by design** in the v3 interpreter: `artifacts/R41C2Interp/sqfs-triage-v3.py` contains no evidence fixtures, no `HELDOUT_*`/`C1_DIR`/expectation tables (grep-empty). Failing input for the frozen v2 selftest (`evidence-E3-heldout-swap.txt`): point `HELDOUT_DIR`/`HELDOUT_MANIFEST` at the round-40 set → `c_committed_heldout` FAILS (`H05 -> ('clean-empty','confirm-empty'), expected ('escaping-symlink-removed','expect-link-absent')`) and `c_heldout_manifest_agrees` FAILS (`H05 manifest label 'clean-empty', selftest expects 'escaping-symlink-removed'`). The frozen 45/45 selftest passes precisely because it grades round-39 bytes. |
| B2 | `tools/round-39/c2-counter.py:373-385`, `tools/round-40/c2-counter.py:641-647` `argmap` join on `os.path.normpath` | cross-form comparison: normalisation-only equality between the path handed to the interpreter and the path it echoes | replaced by `norm_id` in the r41 draft (see A9) |
| B3 | `tools/round-40/c1-run.sh:332-364` oracle-vs-check and `:267-287` oracle/nonregular overlap | **CLEAN** — exact component-wise relpath equality on both roots; the table validator rejects any path overlap outright | r41 `sqfs-list.py` (from R41C1Fetch) keeps component-exact handling (`_split`, :135; symlink resolution :742-772); no suffix/`in` path compares found |
| B4 | `tools/round-40/fetch-vendor.py:79-83` member lookup `names.get(member) or names.get('./' + member.lstrip('./'))` | name-equality with a `./` fallback; ambiguous only if both spellings exist as distinct tar members, and the chain is sha-pinned either way | inherited at `artifacts/R41C1Fetch/fetch-vendor.py:117-118` (low risk; now chain-pinned by `member_sha256`, see D1) |

## 4. Class C — embedded copies of documents that can go stale (R40-CL5 M1 class)

| id | hit | status | round-41 inheritance |
|---|---|---|---|
| C1 | `tools/round-40/sqfs-triage-v2.py:171` `TABLE_BLOCK` vs the frozen SKILL.md v2 block | **STALE — routed (R40-CL5 M1), independently reproduced.** Whitespace-normalised diff (`evidence-M1-table-divergence.diff`): divergence confined to the `avm-marker-be-dropped` row's `cause`+`source` cells (7 diff lines); the embedded copy still carries the pre-rewrite cause ("the removal of -be, not damage, decides this row") where the frozen SKILL table carries the handshake-vs-damage walk. Decision cells identical, so scoring is unaffected — matches `w2/R40W2C2TableReview.md` M1 | **FIXED by design**: the v3 interpreter embeds no table ("NO table is embedded in this file", `:45`) and its selftest hard-fails if any `TABLE_BLOCK` assignment appears (`:1355-1357`, mutant guard). This is the right repair pattern for the M1 class: no second copy, plus a tripwire. |
| C2 | `tools/round-39/sqfs-triage.py:130` `TABLE_BLOCK` (v1 interpreter) | same class one round earlier (historical: the pattern predates round 40 and went unnoticed because v2 replaced v1) | v1 interpreter not ported |
| C3 | `tools/round-40/sqfs-triage-v2.py:838-877` `HELDOUT_EXPECT`/`C1_EXPECT`, cross-checked against the round-39 manifest (:911-926) | **STALE cross-round (data face of B1); never routed.** Expectations keyed to round-40 ids are asserted against round-39 envelopes and a v1-era manifest whose `action` column is absent (never checked) | **FIXED by design** (no expectation tables in the v3 interpreter selftest) |
| C4 | `tools/round-40/c1-counter.py:188-220` per-round constants (`CARRIERS`, `GAPRULE`, `AFTERDIR`, `ENTRY`, `STEM`, `CORE_HEADING`, `IDS`, `PROV_SEGMENT`, `FROZEN_PATHS`) + the P40-C1 docstring | stale-constant class: any surviving constant silently scores round-40 semantics | **all updated** in the draft (`artifacts/R41C1Counter/c1-counter.py:223-232` round-41 entry stem/heading; `c1-extra.py:42-44` likewise) |
| C5 | `tools/round-40/c2-counter.py:56-84` `FROZEN`/`MANIFEST`/`INTERP`/`GEN`/`MARKER_V1/V2` | stale-constant class | **updated** in the draft (`WRITER_CANDIDATES` at `:103-105`, v3 marker) |
| C6 | SKILL.md v2 table prose: `partial-body-failure` and `clean` rows advise "match files to the oracle by relative-path suffix and sha256" | the R40-CL1 advice survives inside the live frozen document an operator would follow | owned by the v3 table draft seat; **flag**: the v3 rows must drop the suffix phrase or the table re-teaches the defect the counter now fails closed on |
| C7 | `tools/round-40/heldout-gen-v2.py` `RECIPES`/`ACTIONS` class map → manifest `expected_label` | D3: expected labels must not come from the generator's class map alone | addressed by design in round 41: the frozen independent evaluator is the label source (`evaluator_covers_all`/`evaluator_pairs` bindings in the r41 c2-counter); the generator's own expectation is demoted to a cross-check that disagreements fail |

## 5. Adjacent defects verified in passing

- **D1 (R40-CL6) fetch chain lacks `member_sha256` — CONFIRMED, fixed in draft.** Driver with an identical fake spec whose pinned `member_sha256` is deliberately wrong (`0`*64): the frozen `tools/round-40/fetch-vendor.py` reports `ok=True` (the pinned field is never read), while `artifacts/R41C1Fetch/fetch-vendor.py` fails closed with `link='member_sha256'` (`evidence-E2-member-sha256.txt`, spec now treats the field as mandatory, `:199-208`).
- **D2 host-local constant**: `artifacts/R41C2Interp/sqfs-triage-v3.py:178` still hard-codes `LANE = '/home/vgpnk/…'` for `DEFAULT_SKILL` (selftest convenience). Round-40 D1 class (durability), not a scoring path; a fresh checkout elsewhere breaks only `--selftest` defaults.

## 6. Net assessment for the freeze

- The headline R40-CL1 defect is fixed properly in the round-41 c1-counter draft (component-exact `extract_rel` + fail-closed root derivation + legacy-rule discrimination selftest + both collision directions), and the M1 embedded-table class is fixed properly in the v3 interpreter (no copy + tripwire).
- **One live inheritance remains**: `writer_logical_path`'s suffix canonicalisation in `heldout-gen-v3.py:487-490` (A6). Cheapest correct move: compare against the lane root prefix resolved from the generator file location (or record the realpath), never `endswith`.
- **Two latent shapes to keep honest**: `norm_id` basename join (A9) and the `devcore-probe` diagnostic suffix bucket (A8) — both safe only under the current layouts.
- The frozen v2 interpreter's round-39 fixture paths (B1/C3) die with the v3 interpreter; if any seat proposes reintroducing committed-fixture selftest cases into the v3 selftest, they must take paths from argv/env and expectations from the *same* root's manifest.

## 7. Non-findings (calibration)

- `sqfs-list.py` (r39 lineage, r40, and the r41 draft), `gen-squashfs.py`, `mk-carriers.py`, `mk-l-carriers.py` (`inside()` is realpath + separator-terminated prefix, exact), `c1-run.sh`'s oracle/check comparison and table validator: no R40-CL1-class compares. `mk-l-carriers.py:136-147` `endswith` calls are literal spec self-checks asserting the deliberate collision shapes — correct use.
- All remaining `endswith('/' + rel)` occurrences in round-41 drafts are deliberate legacy copies kept for selftest discrimination (`R41C1Counter:810`, `R41C1Collide/score-matchers.py`, `R41C1Revenger/rel-exact-rule.py`) or analysis probes (`R41C1Reader/suffix-*.py`, `R41MistakeHunt/registry-body-reach.py:93` — prose token dedup, not filesystem paths).
- No extractor (REA/unblob/sasquatch) was run; no reserved carrier touched; nothing written outside this report and `artifacts/R41ConnPattern/`.

Limits: round-41 drafts are peer work in flight — my inheritance claims cite their bytes as of this wave; the L1 re-freezes them. E2/E3/E4 drivers import the tools and call functions directly (no network, no extractors); transcripts in `artifacts/R41ConnPattern/`.
