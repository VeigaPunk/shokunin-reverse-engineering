# R41W2Freeze — freeze-integrity audit

**Verdict: CONFIRMED** — no commit in `d764389e..7a24ff74` touches a frozen path of either claim; every frozen tool, input and table is hash-identical between freeze and tip; the frozen `tools/round-41/c1-counter.py` is a distinct third version (reproduced below), which is exactly what the wave-1 artifact README records.

Attacked: the freeze-integrity rule of `plans/round-41-claims.md` (both claims) — commit/path inventory of `d764389e9cbe61b9d1b07538ff3bff02d50bb34f..7a24ff74736e84b1903db7ba01891c406a6e32a2`, frozen-path drift, frozen-tool hash equality, and the three-way `c1-counter.py` provenance diff (frozen tool vs freeze-committed wave-1 artifact vs post-freeze artifact).

## 1. Range and commit inventory

Range is linear: `d764389e` → `9a8fb260` → `5ca6941b` → `8a1f4c73` → `042b8769` → `e9a24d07` → `bf5286c9` → `7a24ff74` (parent of `9a8fb260` is `d764389e`; `d764389e` is an ancestor of tip — `git merge-base --is-ancestor` ok). Seven commits:

| Commit | Touched paths (summary) |
|---|---|
| `9a8fb260` pre-data controls | `.ufo/waves/round-41/controls/**` (c1 do-nothing, relabel-r40, c2-at-freeze, selftests), `.ufo/waves/round-41/r41-w1-results.json` |
| `5ca6941b` C1 receipts | `corpus/evidence/round-41/c1/{V3,V4,L3,L4}/{after.json,run.json}`; V4 `run-harness-failure.log` |
| `8a1f4c73` C2 held-out | `corpus/evidence/round-41/c2/heldout/**` (52 carriers: C01–C12, H01–H40, `manifest.json`) — all additions |
| `042b8769` C1 landing | `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md` (M); `corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md` (A) |
| `e9a24d07` V4 receipt | `corpus/evidence/round-41/c1/V4/after.json` (A) |
| `bf5286c9` scores | `.ufo/waves/round-41/l1/{score.sh,c1-run-*.log,heldout-gen-v3-at-freeze.log,scores/**}` |
| `7a24ff74` w1 evidence | `.ufo/waves/round-41/w1/artifacts/R41C1Counter-postfreeze/**`, `R41C1DevCore/rea-7430-core-after*.json`, `R41C2Interp/precedence-check-full.tsv` |

Full `--name-status` listing: `.ufo/waves/round-41/w2/artifacts/R41W2Freeze/commits-in-range.txt`.

## 2. Frozen-path drift: none

Per-claim frozen sets (plan `## Frozen paths` + counters' `FROZEN_PATHS` + carriers.json-named files):

- C1: `plans/round-41-claims.md`; `tools/round-41/{c1-counter.py,c1-extra.py,c1-run.sh,fetch-vendor.py,sqfs-list.py,mk-l-carriers.py,gen-squashfs.py}`; `tools/round-40/gen-squashfs.py`; `.ufo/waves/round-41/c1/{carriers.json,gap-rule.json}`; every path named by carriers.json: `corpus/evidence/round-41/c1/{V3,V4,L3,L4}/oracle.tsv`, `nonregular.tsv`, plus `{L3,L4}/carrier.sqsh`; oracle-run.json (V3/V4) also checked.
- C2: `plans/round-41-claims.md`; `SKILL.md` (v3 block); `tools/round-41/{sqfs-triage-v3.py,indep-eval-v3.py,heldout-gen-v3.py,c2-counter.py}` (counter also freezes the whole `tools/round-41` tree and the heldout manifest dir); writer candidates `tools/round-40|round-39/gen-squashfs.py`.

Check: `git log --oneline FREEZE..TIP -- <path>` returns **empty** for every frozen path/dir, including `tools/round-41`, `tools/round-40`, `tools/round-39`, `SKILL.md`, `.ufo/waves/round-41/c1`, `plans/round-41-claims.md`. The only writes in the range are round-41 claim data/blob (receipts, held-out), claim-surface documents (PROVINCE/README/SOURCES/knowledge) and wave-1 artifacts/controls — none frozen. `.ufo/waves/round-41/c1/` is untouched in the range (0 commits).

## 3. Frozen-tool and frozen-input hash equality: all SAME

sha256 (first 16 hex) of every frozen file at `d764389e` vs `7a24ff74`, via `git cat-file blob REV:path`:

- claims: `plans/round-41-claims.md` 64ec060dce1cd487 SAME
- C1 tools: c1-counter.py bbabbfecb229e899 · c1-extra.py 531724e1c7215ed6 · c1-run.sh bdb97632d21bac71 · fetch-vendor.py 1cb0a34688488160 · sqfs-list.py a8e633f5fe34ad94 · gen-squashfs.py (round-41) 309c502d21dfeef9 · mk-l-carriers.py fa2debc06264cf9d
- round-40 writer: `tools/round-40/gen-squashfs.py` 309c502d21dfeef9 — **byte-identical to the round-41 copy** (matches the claim's "byte copy" note)
- C2 tools: sqfs-triage-v3.py 6ad2b4e1638a2b5f · indep-eval-v3.py 26178d71c0f7634c · heldout-gen-v3.py 652d71afe464856c · c2-counter.py c6c1ea64f07884a3 · c2-controls.py (extra) · local-source-gate.py cafe232a196dd844
- tables: SKILL.md 94d13b445701609f · carriers.json 65dc5c141153d4fe · gap-rule.json 73acb2622329e639 · oracle.tsv/nonregular.tsv ×4 · L3/L4 carrier.sqsh (04cfb4cd…/4c0e5459…) · V3/V4 oracle-run.json — all SAME
- All 13 files under `tools/round-41` at freeze vs tip: 13× SAME.

No frozen file changed between freeze and tip. Control tables (CTL-C2-0..7, dev, dev-scores-prefreeze) were committed **in** the freeze (d764389e stat shows them), so "controls before data" holds; the pre-data control *runs* landed at `9a8fb260` before any receipt data.

Score receipts at tip record `frozen_path_changed: []` and exit 0 (C1 4/4 at e9a24d07; C1-extra 0) / exit 1 (C2 52/52, `observed_features_match_declared` false) — consistent with the admissibility rule.

## 4. Three-way c1-counter.py provenance

Three distinct byte versions exist:

| version | sha256 | lines |
|---|---|---|
| freeze-committed w1 artifact `.ufo/waves/round-41/w1/artifacts/R41C1Counter/c1-counter.py` | 9a3dcf4b1303bc1ecd45aa39d2277fff2e55b69109ffdb76f7c59d213524ed28 | 3447 |
| frozen tool `tools/round-41/c1-counter.py` (at freeze AND tip) | bbabbfecb229e8992fb07149cad0cf9171a2bf31513bd5db77ddb3c4f8845cfc | 3413 |
| post-freeze artifact `R41C1Counter-postfreeze/c1-counter.py` | 06cd72c45cc6ef8b6e208a2d9028d1f5f810d25fadb65b0d4320842db770335a | 3588 |

All three hashes match the README's record exactly; the committed artifact is byte-identical at freeze and tip (`cmp` IDENTICAL), confirming the freeze bytes were restored in place. Diffs (artifacts): `c1-counter-frozen-vs-w1-artifact-at-freeze.diff` (1 hunk, −34), `c1-counter-frozen-vs-postfreeze-artifact.diff` (16 hunks, −200/+35), `c1-counter-w1-artifact-vs-postfreeze.diff` (15 hunks, +166/−35).

**Features of the frozen counter (bbabbfec):**
- Shared with both artifacts: derivation-rooted exact-path rule (`subject_root` reads `derivations[].child_path`, `extract_rel` = whole-segment prefix match, `same_rel` exact equality — R40-CL1 suffix defect fixed; `legacy_same_rel` kept for selftest discrimination); gap disposition families (path-resolved / structural / removal) per `gap-rule.json`; per-row silent admission keyed on the nonregular.tsv third column; `carrier_fresh_ok` from `prior_pins` + `PRIOR_CARRIERS` (round-40 table) read at the freeze; `plus-extractor` rerun projection incl. removal paths; no retry of REA runs; exit 2 on env failure; selftest covering both collision directions, deeper-path publication, removal on non-symlink path, missing member digest.
- vs the freeze-committed w1 artifact: the frozen counter **lacks only the recorded-not-scored chunk-geometry cross-check** (`chunk_summary`/`geometry_agrees` report block, R41CritC1Draft 2) — that is the entire diff (−34 lines, nothing added). That block is diagnostic, not a binding, and is absent from the claim's clause list, so its omission does not change scorable behavior.
- vs the post-freeze artifact: the post-freeze artifact **adds** (frozen lacks): (a) `geometry_agrees` as a *scored* clause in `CLAUSES`; (b) strengthened `carrier_fresh_ok` that scans **all** committed `.ufo/waves/round-*/c1/carriers.json` pins and all `corpus/evidence/**/after.json` subject digests at the freeze; (c) `handler_ok` = exactly one `squashfs_v4_be` chunk (frozen: at least one); (d) REA inventory-race retry (`RETRY_ATTEMPTS=3`, `rea_inventory_race`, `projection_attempts` recorded). The frozen counter is therefore the *earlier/simpler* of the three.

The score at `e9a24d07` was produced by the frozen counter (bbabbfec), unchanged since the freeze. The wave-1 artifact divergence is fully explained by the seat's own README; nothing in the committed tree contradicts it.

## 5. Residual risk / verifier gaps

- The freeze-integrity rule is a gate, not a guarantee of claim correctness: freeze integrity alone cannot show C1's oracle/publication math or C2's evaluator equivalence are right (those are covered by C1/C2 scoring seats).
- C2's `frozen_drift` exempts plain additions (`A`) under the heldout dir — this is the intended `manifest_after_freeze` binding, but the exemption means a future *creation* inside a frozen path after the freeze is tolerated; only later modifications/deletes trip exit 2. Consistent with the claims text.
- C1's `frozen_drift` uses `--name-only` (any touch, incl. creations, counts) — stricter; no drift found either way.
- Working tree has uncommitted non-frozen dirt (`M corpus/QUALITY.md`, untracked w2/ files, `corpus/evidence/round-41/c1/V4/green.err`/`red.err`, `corpus/lessons/round-41.md`) — none on a frozen path; audit covers committed revisions as scored.

## Evidence

- Artifacts: `.ufo/waves/round-41/w2/artifacts/R41W2Freeze/` — `commits-in-range.txt`, `evidence-notes.txt`, three counter diffs (above).
- Commands: `git log --format='%H %ad %s' --name-status`; `git log --oneline FZ..TIP -- <frozen path>`; `git cat-file blob REV:path | sha256sum`; `git merge-base --is-ancestor`; `git show --stat d764389e`; `git diff` (not used — `diff -u` on `cat-file` extracts); `git status --porcelain` (read-only). No git/jj mutation performed; no tools installed (none needed).

Report: `.ufo/waves/round-41/w2/R41W2Freeze.md`
Artifacts: `.ufo/waves/round-41/w2/artifacts/R41W2Freeze/`
