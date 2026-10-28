# Round 44 verifier spot-check — kaidoku (non-author closure)

author: hyaku closure (non-author integrator, @m_zfl)

Lane repo: /home/vgpnk/Projects/shokunin/kaidoku-shokunin. Round start `c29360e3ba5381a5ab69e372d0d9577970f85018`;
freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84` (`plans/round-44-claims.md`); measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; lane tip at judging `4503fb7860ac35bd3ba08def65a82a505d7b779b`.
Driver digest (copied from `.ufo/watchdog.log`):
`2026-10-28T07:42:04-03:00 launch kaidoku round=44 pgid=3257226 driver=hyaku-inline attempt=1` /
`2026-10-28T11:09:13-03:00 launch kaidoku round=44 pgid=943219 driver=hyaku-inline attempt=2` /
`2026-10-28T11:37:36-03:00 complete kaidoku round=44; hyaku-inline attempt=2`.
Report: `.ufo/reports/round-44/kaidoku.md`, committed on the fleet repo by the lane identity
(`kaidoku-shokunin <kaidoku@shokunin.local>`, fleet commit `86a44acf64e5f492c01f335d22ae49506dcae316`, 11:37:03-03).

## 1. Conformance (step 1)

- Report sections in required order, all present (Work performed / Landed changes / Before → after
  measurements / Sources & frontier / Trend verdicts / SHONEN). SHONEN.md has 4 boxes; the report
  carries one `[~]` line per box with resolvable pointers. Real committed work, not a marker.
- All 17 cited lane hashes resolve and are ancestors of `refs/heads/main` (tested with
  `git merge-base --is-ancestor <hash> refs/heads/main`, never `@{u}`): `b33a4738fa8000dff…`,
  `c1ff9e899a5cb09f…`, `2081dc069e9f5a15…`, `7ed97668cc8e17eb…`, `b2a1bd91f5dffabd…`,
  `c48f8a4bfd449300…`, `fee6e98a454859ba…`, `4cc1ac11657590c2…`, `9d3d1862e565e345…`,
  `75a5cb427d09e645…`, `e9e3abd1f6638adc…`, `55bcce69c2f48549…`, `c86ea508188c50e2…`,
  `8bb1090af3fef644…`, `923fa87072cc1a72…`, `f370592b729a3a20…`, `4503fb7860ac35bd…` — all `anc`.
- Push state at judging: `scripts/hyaku/jj-lane.sh state <lane>` →
  `branch=main local=4503fb78… remote=4503fb78… ahead=0 behind=0` (exit 0).
- `git status --porcelain` at judging is NOT clean: ` M .ufo/waves/round-44/w2/R44W2LessonGate.md`
  (final audit text, blob `9f9ac8a5…`, vs committed draft `e1164575…` at `f370592b`), plus untracked
  `w2/R44W2Record.md`, `w2/R44W2Distill.md`, `artifacts/R44W2Record/`, `artifacts/R44W2Distill/`,
  `artifacts/R44W2LessonGate/{final-tip-4503fb78-counters.json,supplementary-probes.json}`. These are
  the two late seats and the final LessonGate text — post-filing addenda, not yet committed. **Defect
  (conformance, status-neutral): uncommitted round work in the lane worktree at closure — the exact
  pre-sweep state that produced `c86ea508`.** Round 45 or the operator must land them deliberately;
  a blind sweep must not commit them.
- Claims file integrity: `git show c48f8a4b:plans/round-44-claims.md | sha256sum` =
  `369a6201b4e9171a95d8c3d346d5cf8a091237b1e9f8f85eca2697be2b99c654` = worktree blob. Not mutated.
- SCORECARD reversion verified: `git rev-parse 55bcce69:SCORECARD.md` = `git rev-parse 4503fb78:SCORECARD.md`
  = `af5a3f1a68fc2db273c6336895675513497917bb`. Ledger lives at `LOG.md:3218`
  (`### Round 44 claim ledger`).

## 2. Claim re-checks (step 2) — both re-measured by me at `55bcce69`

**R44-C1 (coverage) — NOT MET, honest stop; verdict confirmed.** My own run of the frozen counter:

```
python3 -I -B tools/round-44/c1-counter.py --root <lane> --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac \
  --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /tmp/k44v-c1 --json-out /tmp/k44v-c1/out.json
→ exit_code 1, met_target false, carriers_matched 4, frozen_path_changed [],
  bindings_false ["province_core_section","province_core_row","frontier_note"]
```

Byte-agrees with the committed receipt `.ufo/waves/round-44/l1/c1-score-at-55bcce69.json`. The
dual-clause premise is real: `plans/round-44-claims.md:34-35` (controls amendment: output_directory
must name a `corpus/evidence/round-44/c1/` path) vs `:137-139` (predicate: the `/kaidoku-r44/`
scratch segment + runner binding). The four receipts carry the plain scratch form
(e.g. `corpus/evidence/round-44/c1/v1le/after.json` →
`/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out`), so neither clause's
composite is realized. The green precursor at `4cc1ac11` is committed and disclosed
(`corpus/evidence/round-44/c1/counter-at-4cc1.json`: rev `4cc1ac11…`, exit 0, met_target true);
promotion was withdrawn at `55bcce69` (PROVINCE.md ×4 "measured, not promoted"; corpus/README.md ×3;
entry title "R44-C1 not promoted"). **Falsifier corrections adopted:** the exit-1 cause is the three
withdrawn promotion-document bindings, not provenance (`provenance_ok` true for all four carriers —
four independent reruns incl. mine); "internally unsatisfiable" is false (a composite path, or a
3-line PROVINCE-only restore, scores green); the stop is *a* defensible policy choice, not the only
reading. SOURCES census `137 → 139` (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'`: 137 at
`c29360e3`, 139 at tip; S138/S139 additive only, tier A).

**R44-C2 (calibration) — MET at the measured revision; inadmissible at the lane tip under its own
freeze rule.** My own run of the frozen counter:

```
python3 -I -B tools/round-44/c2-counter.py --root <lane> --rev 55bcce69 --freeze c48f8a4b \
  --work /tmp/k44v-c2 --json-out /tmp/k44v-c2/out.json
→ exit 0, entries_evaluated 80, mismatches [], mismatches_count 0, frozen_path_changed [],
  met_target true, claim_score true; counter/rubric sha256 equal to their freeze values
```

Agrees with `l1/c2-score-at-55bcce69.json`; the committed evidence receipt
`corpus/evidence/round-44/c2/c2-score-9d3d.json` measures `9d3d1862…` (exit 0, 80 entries) — the
report attributes both revisions correctly. Correction block live at tip (`SCORECARD.md:3512-3517`
`c2-correction` markers; rows 23/24 unchanged by design — append-only repair, carried debt D-17).
At the tip the same instrument exits 2 with 8 `frozen_path_changed` (the sweep-committed
`tools/round-44/control-fixtures/**` mutations in `c86ea508`), so the claim is admissible only at
`55bcce69`, as the round states. **Instrument limits (falsifier-verified, routed):** the claimed B2
substring gate is implemented nowhere (and 71/80 entries would fail it literally — C-2/C-5); the
"a later restore does not un-block" clause is unimplemented — break-then-restore on SCORECARD yields
exit 0/80/80/met, and the M44-3 fix is exactly that shape (C-3, NEW); the counter's freeze set is
narrower than the claim's `## Frozen paths` (R44-CL7); the three corrected observables are
freeze-tree-scoped (R44-CL9).

**External contamination, named as a defect class:** the freeze violation at the tip was created by
the **fleet orchestrator's non-author lane sweep**, which committed attempt 1's dirty worktree
46 minutes after the L1 stopped: `c86ea508` author `2026-10-28T09:57:16-03:00` (= the stop-time
snapshot), committer `2026-10-28T10:43:43-03:00`, **432 paths** (400 A / 32 M), 8 under the frozen
`tools/round-44/control-fixtures/`. The lane's record originally said "74 paths" (porcelain lines,
dirs collapsed). The round did not author that commit; the record's M44-2 account (mtimes 09:50:09/
09:50:30, no gate sees a dirty tree) is accurate. Routed class: **sweep-contamination** — any
non-author sweep that commits a lane worktree can retroactively violate a frozen pathspec; the sweep
must run a frozen-path preflight (dirty-tree arm + mandatory pathspec + placement in the
sweep/pre-push path) before committing. Parent addendum's cross-lane instances (r42 `d0f6d91b`,
r43 `a39e722b`) did **not** resolve via `git rev-parse` in any of the 21 lane repos — unverified by
this closure; the kaidoku instance above is verified from git metadata.

**Wave accounting:** wave 1 `r44-w1-results.json` carries 37 seats, 37 result entries
(agent/name/note/output each). Wave 2: 42/42 seat reports exist at judging time — the two late
reports (`R44W2Record.md`, `R44W2Distill.md`) and the final `R44W2LessonGate.md` text are
**worktree addenda, uncommitted** (see §1). Filing at 40/42 was settled with the orchestrator
(request budget); no claim number derives from the missing two.

## 3. Discernment spot-check (step 3) — admits and reject re-opened

| item | decision | re-opened source (this closure) | agree/disagree | reason |
|---|---|---|---|---|
| S138 admit (unblob 26.6.4 SquashFS `__output__` trees, tier A) | admit | `https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs` → HTTP 200; contents API `…/squashfs_v2/big_endian/__output__?ref=26.6.4` → `['squashfs_v2.0_be.bin_extract','squashfs_v2.1_be.bin_extract']` | **agree** with the decision; **disagree** with the row's citation | Source is live and members match the receipts; but the lesson's cited manifest digest `4bc53dbb…c1a13` matches **no committed object** — true digest `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe` (my sha256sum + blob scan) — and the lane's own open receipts cover only subdirectory listings, never the cited tree URL (LessonGate D1/D3/D4) |
| S139 admit (squashfs-tools 4.7.5 release, tier A) | admit | `https://api.github.com/repos/plougher/squashfs-tools/releases` → 9 releases; `tag_name "4.7.5"`, `name "Squashfs tools 4.7.5"`, `published_at 2026-03-01T23:05:47Z` | **agree** | Matches the SOURCES row byte-for-byte; the located quote exists in the committed capture (`w1/R44SrcOracle/receipts/s139-releases-page.json`, LessonGate D2) — the Gate cell should cite it |
| Assimilation quarantine reject (no adoption) | reject | `…/squashfs_v4_be/__input__?ref=26.6.4` listing → 4 v4 fixtures live (the slice's present-with-anchor class) | **agree** | Slice digest `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a` present at `w1/R44Quarantine.md:5`; no staged row is cited by an admitted entry, so non-adoption is correct |
| Census | — | `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → `kaidoku ok`, exit 0, 14 W04 (13 pre-existing + S138's within-scope URL) | **agree** with round-end state; **disagree** with the lesson's round-start cell | Round-start count 14 is actually the end receipt; the only start artifact is a baseclone-scoped replay with an `ERROR:` line and 13 W04 (Record D-3 / LessonGate D7) |

## 4. Per-axis verdicts

| axis | verdict | evidence |
|---|---|---|
| coverage | **unchanged** (score 10 → 10; claim's promotion not met, honestly stopped) | my C1 rerun; PROVINCE/README/entry measured-not-promoted; entry + S138/S139 landed as measurement-only |
| depth | **unchanged** (21/21 rule blocks, `depth_score 10.0`) | command A at tip per C2Corrections a2 (21/21 at freeze and REV); no depth claim |
| calibration | **improved** at the measured revision `55bcce69` (3 → 0 mismatches over the frozen 80-entry rubric; reproduced by me and two seats); **inadmissible at the lane tip** under the claim's own freeze rule (exit 2, sweep-committed fixture mutations); corrected values live in SCORECARD at tip via the append block | my C2 rerun; `l1/c2-score-at-tip.json`/`-final-tip.json` exit 2 with 8 paths |

## 5. Trend verdicts

- **expansion: improved** — one new knowledge entry on previously unmapped v1/v2 ground
  (`corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md`) citing S138/S139; registry 137 → 139,
  additive only; census exit 0 at round end (mine). Honesty held: no promotion claimed.
- **quality: improved** — two instrument defects walked into and named with executable evidence
  (output-directory dual clause R44-CL2; post-freeze fixture mutation M44-2 →
  `tools/round-45/frozen-path-preflight.py` red/green reproduced by me via the committed receipts
  and by two seats); the round refused the naming-loophole promotion. Marked but unfixed record
  defects remain (§6) — they are routed, and the falsifiers' reports are committed, so the corpus
  entries themselves stand; none was found false.
- **discernment: improved** — the lane demoted its own green precursor, disclosed tip
  inadmissibility, retracted its own second freeze violation (M44-3) when its falsification wave
  caught it, and re-derived the 80 rubric entries. My spot-check agrees with all gate decisions
  (2 admits, 1 reject); disagreements are citation hygiene, already surfaced by the lane's own
  wave-2 seats.

## 6. Routed defects (round 45 must fix; none re-opens the round)

1. **Record defects false at the committed blob** (`corpus/lessons/round-44.md` = `2e4c22d2…`,
   LOG.md, report): S138 manifest digest `4bc53dbb…` matches nothing (true `06a72dd5…f5fe`);
   `QUALITY 86`/`QUALITY 87` cited at `LOG.md:3229` and in the fleet report but `corpus/QUALITY.md`
   max row id is 85 (no 86/87 anywhere in the file); round-start census cell wrong (13 W04,
   baseclone-scoped, ERROR line); `R43-CL1..CL4` phantom (only `R43-CL1a` exists, in
   `.ufo/waves/round-43/`); `opened_source_rows` cited as open-evidence while the instrument reads
   only SOURCES date/used-by cells (`c1-counter.py:2184`); S138 "opened" cell = descendant-listing
   replay (top URL never fetched by the lane); S138 quote is 10 repo-side words labeled 12; S139
   Gate cell omits its committed capture pointer.
2. **Residual stale mentions:** "unsatisfiable / no run can satisfy" wording was corrected in
   LOG/lesson at `923fa87` but survives in PROVINCE/README/entry per Distill C-2 (corrections must
   sweep every mention).
3. **Instrument gaps:** B2 substring gate unimplemented (C-2; 71/80 literal failures — C-5);
   "later restore does not un-block" unimplemented (C-3 NEW); preflight holes — false-green outside
   a caller-supplied pathspec, false-red on the C2 bound edit without an allow-list, no dirty-tree
   arm, not wired into commit/sweep/jj sequence, docstring over-promises pre-commit (C-4, C-6,
   D13, R44W2Preflight D-1..D-3); C2 freeze set narrower than claim (R44-CL7); freeze-tree-scoped
   observables (R44-CL9); runner-tree binding unimplemented (R44-CL8); **no SKILL.md registry rows
   for the round-44 counters** (Gate standard, Delivery — both counters have committed selftests
   but no registry row at the lane's registry home).
4. **Worktree leftovers at closure (sweep-contamination risk):** modified `R44W2LessonGate.md`
   (final text uncommitted), untracked `R44W2Record.md`, `R44W2Distill.md` + artifact dirs, plus
   the stray duplicate `corpus/evidence/round-44/c1/c2-score-9d3d.json` (RA-5). Land deliberately;
   never sweep-commit blindly.
5. **Sweep class (fleet-level):** non-author sweep commits of stopped lanes' dirty worktrees create
   freeze violations with misleading author stamps (verified instance: `c86ea508`, 432 paths,
   author 09:57:16 / committer 10:43:43). The sweep must preflight frozen pathspecs before
   committing. Addendum's r42/r43 instances unverified (hashes unresolved in all 21 lane repos).

## 7. Closure verdict

- R44-C1: not met, honest stop — **confirmed** (verdict stands; recorded cause corrected to the
  three withdrawn promotion-document bindings).
- R44-C2: **met at `55bcce69`** (80/80, reproduced), inadmissible at tip under its own freeze rule;
  instrument limits disclosed by falsifiers and routed.
- Round verdict: **rejected-honest-stop**, admitted=false; no axis harmed; status ok.
