# R40W2ConnRouted — routed-defect state at tip 4d62ee5a + round-41 routing

**Verdict: DONE.** Re-checked every routed defect carried into round 40 — R39-CL1..CL6, R36-CL5, the round-39 "still open" items and the wave-1 ledger `.ufo/waves/round-40/w1/R40ConnRouted.md` flags — against the committed landing at `4d62ee5a86b4692a13f682b29ed7975e8d7e5326` (measured landing `42c10a58cb2cae3a4a0122af35a0cf95ac718043`). Attacked: the closure state of each carried defect, and which round-40 defects must be routed into round 41 (the C1 suffix false negative and its refreeze).

Method: read-only git (`show/log/ls-tree/diff`), committed score receipts (`l1/scores/*`), control files (`controls/`), selftest outputs, SKILL v2 block, SOURCES rows, held-out manifest, and one cheap `sqfs-triage-v2.py --table-only` validation run on the CTL-C2 controls. No REA/unblob/sasquatch run, no carrier run, no VCS mutation, no install, no scratch (all reads from committed bytes; the single `--table-only` run wrote nothing). No subagents.

## 1. State at tip — what the landing looks like

- C1 main counter at `42c10a58`: exit 1, `carriers_matched 3/4`, `met_target false`, `frozen_path_changed []`, all doc bindings true. Only L2 fails, and only `nonregular_unpublished_ok`: `nonregular_published = ["firmware.bin_extract/usr/bin/busy"]` (`l1/scores/c1-at-42c10a58.json` L2 block). C1-extra met (exit 0, `oracle_rederived` ok on all four, `sourced_new` S124–S126). C2 met: 26/26, exit 0, `met_target_consistent true`, `unclassified_expected 2 observed 2`, `distinct_decisions 12`, `replicates_identical_in_class []` (`l1/scores/c2-at-42c10a58.json`).
- The demotion record is committed at tip: PROVINCE.md line 394 carries the "Round-40 frontier note … AVM-BE is **measured, not promoted** … stopped at 3/4 on a counter false negative" sentence; the knowledge entry `2026-10-26-r40-avm-be-squashfs-core.md` has "Measured; R40-C1 stopped, not promoted" and names the exact L2 failure (line 29). This is the honest stop, recorded.
- Drift: `git diff --stat 7fce3086 4d62ee5a -- tools/round-40 plans/round-40-claims.md .ufo/waves/round-40/c1` is empty; c1-counter.py sha256 `8d288e4c…` identical at freeze and tip. Freeze-integrity intact for both claims.

## 2. Routed-defect ledger (status per item)

### R39-CL1 (no domain guard; non-firmware envelopes labelled) — FIXED
Evidence: SKILL v2 table (block 19) puts `operation`/`provider` immediately after `label` (`SKILL.md:363`); held-out manifest declares `out_of_domain = {operation: inspect-firmware-regions, label: unclassified, action: none}` (`corpus/evidence/round-40/c2/heldout/manifest.json`); c2 score observes exactly 2 `unclassified` pairs (`l1/scores/c2-at-42c10a58.json`); kill control CTL-C2-4 (no domain guard) scores 24/26 failing only out-of-domain (`controls/c2-dev-scores.json`); c2-counter selftest includes the red case "best table + `*` default row instead of the domain guard" (`w1/R40C2Counter.md` E1).

### R39-CL2 (v1 block lacks mixed-symlink caveat; K5/K6 action contradiction) — FIXED
Evidence: SKILL v2 table has `mixed-symlinks` row ahead of `escaping-symlink-removed` (`SKILL.md:371` before `:372`), action `audit-symlinks`, cause explicitly guards "never read this as permission to ignore the in-tree gaps"; held-out class `mixed-symlinks` (H11/H12) present; control CTL-C2-5 (no mixed row) 24/26 failing only mixed-symlinks.

### R39-CL3 (rows 5/8 excluded outcomes; cause→action unscored; 20 = 9 decisions) — FIXED
Evidence: v2 table adds `partial-body-failure` (`published files >0` → `salvage-partial`, `SKILL.md:370`) and `clean-empty` (`published files 0` → `confirm-empty`, `:375`); the `action` column is scored against a closed vocabulary; the counter reports `distinct_decisions 12`; `replicates_identical_in_class []` and manifest `replicate_variation = [compression, tree-shape, endianness-where-the-class-allows]` prove the two per-class envelopes differ in non-decision features. Control CTL-C2-2 (v1 transcribed) 18/26 misses exactly clean-empty/mixed/out-of-domain/partial; CTL-C2-3 (actions rotated) 2/26.

### R39-CL4 (kill-control `.formatfix` inputs landed after the freeze) — FIXED
Evidence: `CTL-C2-0..6.md`, `score-c2-controls.py` and `c2-dev-scores.json` are all first added at the freeze `7fce3086` (`ls-tree 7fce3086 -- .ufo/waves/round-40/controls`). I re-validated the control tables with the frozen interpreter: `python3 -I -B tools/round-40/sqfs-triage-v2.py --table-only --skill <ctl>` → CTL-C2-1..6 exit 0, CTL-C2-0 exit 2 (the intended negative: no v2 table). Dev scores recorded before any held-out data (seed `96832afb…` = sha256("dev40")): 0/4/18/2/24/24/24, none meets target — kill rule did not fire. C1 control inputs (gap-rule.json, carriers.json) are at the freeze; the ctl-c1 receipts/selftest outputs landed in the control-receipts commit `45e89864` (post-freeze, pre-data, the normal scoring flow).

### R39-CL5 (C1 counter cannot refuse a re-minted fabricated receipt) — FIXED (as claimed, limit disclosed)
Evidence: c1-counter.py `measure()` runs `make_real_runner` (REA 6.5.0 `extract-firmware --max-depth 1`, fresh outdir) on each carrier's bytes at scoring time and compares the frozen `plus-extractor` projection; at `42c10a58` `projection_ok true` and `projection_diff []` for all four carriers. The dev selftest log `w1/artifacts/R40C1Counter/selftest-detail.log` shows the red case "oracle-only fabrication with re-minted evidence id" → exit 1, failing `handler_ok`/`projection_ok` (projection_diff chunks+diagnostics) — the required kill control runs red. Committed selftest: 70 cases, 5 green / 65 red, 0 failures (`controls/c1/c1-counter-selftest.json`). Disclosed limit stands unchanged: a receipt equal to a real run of the same bytes passes by design (claims :85-88).

### R39-CL6 (no exit codes in receipts; no cross-domain-evidence line; seat status null) — PARTLY FIXED
- Exit-code half: fixed. Every round-40 receipt carries `exit_code` (c1-at-42c10a58 `1`, c1-extra `0`, c2 `0`, controls `1`/`2`/`0`, fetch-vendor `0`). `score-receipt.sh` wraps counters with `exit_code/argv/counter_sha256/utc_*/lane_revision_arguments` and collision-protects the exit code (selftest 51/51; `w1/R40CL6Receipts.md`).
- Seat status: `ledger-status.py` (43/43 selftest) exists and was exercised on the round-39 ledgers; the wave-2 `swarm-registry.json` members still carry no `status` value — filling is a closure/landing step, not done yet.
- Cross-domain-evidence line: belongs to the final L1/closure report; not yet produced (wave 2 in flight).

### R36-CL5 (instruments still fail QUALITY rows 33/39/45/58/60/68) — OPEN (carried by the w1 ledger, still unbound)
- The w1 ledger is committed at the freeze (`ls-tree 7fce3086 -- .ufo/waves/round-40/w1/R40ConnRouted.md` → present), so the defect is no longer "silently dropped"; but the round-40 claims bind no QUALITY-conformance clause and the round-40 lesson file does not exist at tip (`ls-tree 4d62ee5a -- corpus/lessons/round-40.md` → absent).
- Per-row check against the round-40 instruments:
  - QUALITY 33: all instruments and the claims file first land in the same freeze commit `7fce3086` (not instruments-before-claims); there is no machine-readable `instruments` pin container (claims file is markdown; grep for `instruments` in `plans/round-40-claims.md` → none). The counters' `FROZEN_PATHS`/`frozen_drift` implements the drift guard instead. Partial.
  - QUALITY 39: receipts record only the unblob provider version; no per-call REA package.json sha column, and the counters do not reject a committed receipt whose recorded version differs (the rerun pins the CLI via `npx rea-agents@6.5.0` at scoring time). Not met.
  - QUALITY 45: the entry cites S124–S126 (new since base, opened 2026-10-26) and c1-extra requires them opened+used-by (`sourced_new`), but the claims file never names the row ids (no `claim_row`), and the round-40 lesson `## Gate` listing does not exist yet. Partial.
  - QUALITY 58: not applicable — no repertoire-calibration counter this round.
  - QUALITY 60: the literal scratch-disk-inventory restriction is in the wave-2 context/bounds; a retained-command audit with a red prohibited-command case is not part of the round-40 instrumentation. Partly satisfied structurally.
  - QUALITY 68: predicates are echoed as constants (`P40-C1`/`P40-C2`); neither counter reads the predicate from the claims file, and there is no pins container. Not met.

### Round-39 "still open" carried items
- **`heldout-gen.py` `corruption_bad_minor` docstring erratum — OPEN (bytes frozen; forward-resolved).** The stale docstring is still at `tools/round-39/heldout-gen.py:218` (frozen; measured opposite per `w2/R39W2C2Shortcut.md` D1). The round-40 generator `heldout-gen-v2.py` drops the class entirely (corruptions are `zero-id-table`/`bad-major`/`partial`; no version-minor recipe), so the defect cannot recur in v2. Needs its lesson record at round end.
- **Surviving round-39 interpreter/counter mutants — CARRIED, not re-swept on the new tools.** The `R40MutR39` artifacts reproduce the round-39 survivors (51 probe mutants: 47 SURVIVED, 4 KILLED-SELFTEST; triage 21/23 survive) — that is a re-measurement of the old tools, not a fresh sweep of the round-40 tools. The new counters ship large named red sets (c1 65/70 red; c2 31/42 red, including domain-guard/catch-all/rotated-actions/no-mixed-row cases), but no published mutation sweep over the v2 interpreter/counters exists as of tip. Item remains open/unbound.
- **Loose anchors S118/S121 — PARTLY FIXED.** S121 now records `debian/rules` lines 15-18 with the exact `CFLAGS=-DFIX_BE dh_auto_build` quote and the installed binary digests (`corpus/SOURCES.md:127`), but still no URL/sha for that second file. S118 (`:124`) still omits the second report site (recursive-link loop branch, lines 58-65); the row cites 73-77/79-87/88-91 only.

## 3. Round-40 defects to route into round 41

1. **C1 counter suffix false negative (`nonregular_unpublished_ok`) — the only C1 failure.** Root cause: `nonregular_published`/`same_rel` uses path-suffix matching (`candidate.endswith('/' + rel)`), so the published regular file `firmware.bin_extract/usr/bin/busy` is read as the symlink row `bin/busy` (repro: `same_rel(..., 'bin/busy')` → True; after stripping the `*_extract` prefix, `usr/bin/busy != bin/busy`). L2's receipt itself is correct and complete (6/6 oracle, 2 `unpublished-entry` + 1 `depth-limited` gaps, one `squashfs_v4_be` chunk not failed; no published symlink path). Fix: compare non-regular entries by exact rel path after `rel_suffix` (and audit `oracle_hits` for the same over-match), and add a red selftest case with exactly this shape (regular file whose path ends with a symlink row path).
2. **Refreeze is mandatory.** `tools/round-40/c1-counter.py` is a frozen path; editing it after the freeze blocks every future C1 score (`frozen_path_changed`), and a later restore does not un-block. Round 41 must re-freeze the counter (same carriers/data — V1/V2/L1/L2 pins are fine; the round-40 receipts `73c7bf9c` remain valid evidence), re-run controls/selftests, then re-score; expected result 4/4.
3. **Promotion wording.** After a pass on the re-frozen counter, update PROVINCE.md:394 and `2026-10-26-r40-avm-be-squashfs-core.md` from "measured, not promoted" to a Core row (the entry and note already exist and cite the right surfaces).
4. **R39-CL6 remainder** (cross-domain-evidence line in the closure report; seat-status fill in the wave-2 ledgers).
5. **R36-CL5 remaining legs**: bind QUALITY 68 (predicate read from the claims file/container, not echoed) and QUALITY 39 (per-call REA package.json-sha check with red fixtures) for the re-frozen counters; add the claims-file `instruments` pin map; record R36-CL5 state in the round-40 lesson.
6. **Carried-item ids**: give the erratum, S118/S121 anchor appends and the mutant-sweep-missing item explicit ids in the round-41 freeze/lesson (they were flagged in the w1 ledger but still have no ids; the round-40 lesson does not exist yet).
7. **Minor, no action needed**: the `same_rel` suffix over-match is lineage-shared with the oracle-hit path; the fix in (1) covers both sites, and the L2 carrier intentionally contains the `bin/busy` symlink + `usr/bin/busy` regular pair, so it doubles as the permanent regression fixture.

## 4. Evidence base (all committed; closure can re-run these reads)

- `l1/scores/c1-at-42c10a58.json` (L2 block: `nonregular_unpublished_ok false`, `nonregular_published ["firmware.bin_extract/usr/bin/busy"]`, every other clause true; `carriers_matched 3`, `exit_code 1`).
- `corpus/evidence/round-40/c1/L2/after.json` (files 6/6 oracle suffix+sha; gaps `depth-limited`×1 + `unpublished-entry`×2; chunk `squashfs_v4_be` not failed).
- `corpus/evidence/round-40/c1/L2/nonregular.tsv` (row `bin/busy symlink /usr/bin/busy`).
- `tools/round-40/c1-counter.py:606-649` (`same_rel`/`nonregular_published`), `:1090-1092` (binding).
- `l1/scores/c1-extra-at-42c10a58.json` (exit 0, `met true`); `l1/scores/c2-at-42c10a58.json` (26/26, exit 0).
- `corpus/evidence/round-40/c2/heldout/manifest.json` (seed = freeze hash; `out_of_domain`; `replicate_variation`; 26 carriers).
- `.ufo/waves/round-40/controls/c2-dev-scores.json`; `controls/c1/ctl-c1-0-do-nothing.json` (0/4, exit 1), `controls/c1/ctl-c1-0-extra.json`, `controls/c2-counter-at-freeze.json` (exit 2 `no_manifest_at_rev`), `controls/c1/fetch-vendor-at-freeze.json` (exit 0).
- `.ufo/waves/round-40/w1/R40C1Counter/selftest-detail.log` (fabrication red case fails on projection), `controls/c1/c1-counter-selftest.json` (70 cases, 0 failures), `w1/R40C2Counter.md` (42/42), `w1/R40CL6Receipts.md` (51/51, 43/43), `w1/R40MutR39/results.json` (r39 survivor re-measurement).
- `SKILL.md:361-375` (v2 table), `corpus/SOURCES.md:124,127` (S118/S121), `tools/round-39/heldout-gen.py:218` (erratum), `tools/round-40/heldout-gen-v2.py` (no version-minor recipe), `tools/round-40/mk-l-carriers.py:56-77` (L2 tree).
- Git: `git log --diff-filter=A --format=%H -1 -- <path>` for claims/tools/controls (all `7fce3086`; c1 receipt outputs `45e89864`); `git ls-tree 7fce3086 -- .ufo/waves/round-40/controls`; `git diff --stat 7fce3086 4d62ee5a -- tools/round-40 plans/round-40-claims.md .ufo/waves/round-40/c1` → empty; `PROVINCE.md:394`.

Artifacts: `.ufo/waves/round-40/w2/artifacts/R40W2ConnRouted/` (`l2-suffix-repro.txt`, `routed-ledger.json`).

Report: .ufo/waves/round-40/w2/R40W2ConnRouted.md
