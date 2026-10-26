# R40W2Sentinel — round-40 wave-2 seam check and sentinel pass

**DEFECTS FOUND** — both author verdicts reproduce (R40-C1 NOT MET at 3/4, exit 1; R40-C2 MET at 26/26, exit 0),
but five defects stand: (F1) C1's frozen target was **unreachable at the freeze** — L2's frozen oracle and
non-regular tables make two of its clauses jointly unsatisfiable, so the "honest stop" was entailed, not
discovered; (F2) the C2 counter returns `met_target: true` for a tree whose commit touched a **declared frozen
C2 path** (`tools/round-39/gen-squashfs.py`), violating the shared freeze-integrity rule; (F3) the same rule's
"a later restore does not un-block" clause is not enforced for the SKILL v2 block (mutate → restore → 26/26 met);
(F4) `SKILL.md` is modified and uncommitted in the lane at wave-2; (F5) `c2-counter.py`'s selftest leaks
`gen.*` dirs into the shared scratch root (584 → 625 while I watched). No frozen path was touched between the
freeze and the measured revision, so the two published scores are admissible as they stand.

Attacked: the landing (its verdicts, its arithmetic, its admissibility rule, its evidence chain), not the round's
tools' design intent. Surface inspected: both counters, `c1-extra.py`, `sqfs-list.py`, `sqfs-triage-v2.py`,
`heldout-gen-v2.py`, `fetch-vendor.py`, the claims, PROVINCE/README/knowledge landing text, the committed
receipts, the frozen tables, `/fast/scratch`, and the fleet/lane working trees.

## 1. What I ran (all read-only on the lane; mutations only in throwaway clones)

| # | command (abridged) | result |
|---|---|---|
| R1 | `python3 -I -B tools/round-40/c1-counter.py --root LANE --rev 42c10a58 --freeze 7fce3086 --pkg65 <rea 6.5.0> --carrier-cache /fast/scratch/hyaku/kaidoku-r40/_l1/cache --json-out $S/c1-repro.json` | **exit 1**, `carriers_matched 3/4`, `met_target false`; L2 sole false clause `nonregular_unpublished_ok`; V1/V2/L1 matched. 8.7 s wall — the counter's own four REA reruns all `projection_ok: true`, i.e. a fresh 26.6.4/sasquatch-v4be run of each carrier at scoring time matched the committed receipt |
| R2 | `python3 -I -B tools/round-40/c2-counter.py --root LANE --rev 42c10a58 --freeze 7fce3086 --json-out $S/c2-repro.json` | **exit 0**, `matched 26`, `bindings_ok true`, `bindings_false []`, `frozen_paths_changed []`, `met_target true` |
| R3 | `git show 42c10a58:SKILL.md > $S/SKILL-42c10a58.md && python3 -I -B tools/round-40/sqfs-triage-v2.py --skill $S/SKILL-42c10a58.md --json corpus/evidence/round-40/c2/heldout/H*/envelope.json` | exit 0; my own join of the 26 outputs against the manifest's `label`/`action` → **26/26 pairs, 0 mismatches**, 12 distinct pairs |
| R4 | `python3 -I -B tools/round-40/sqfs-list.py --layout avm --files F --nonregular N <carrier>` on all four carriers (vendor bytes from the sha-pinned cache) | `diff` against each frozen `oracle.tsv` and `nonregular.tsv`: **byte-identical on all four** (`artifacts/R40W2Sentinel/reader-rederivation.txt`) |
| R5 | `artifacts/R40W2Sentinel/satisfiability.py` — frozen tables only, no REA, no counter code | `target_reachable: false`, `unsatisfiable: ["L2"]` — see F1 |
| R6 | counter sha256 vs the L1's receipts | `8d288e4c…` (c1), `9bd79249…` (c2), `5ba40129…` (c1-extra) — identical to `.ufo/waves/round-40/l1/scores/*.receipt.json` |
| R7 | sandbox clone, touch `tools/round-40/c1-run.sh` → commit → counter | **exit 2**, `reason frozen_path_changed`, `frozen_path_changed: ["tools/round-40/c1-run.sh"]`, no `met_target` key, clone `git status --porcelain` empty (`c1-drift.json`) |
| R8 | same clone, restore the file → commit → counter | **exit 2** again (restore does not un-block) (`c1-drift2.json`) |
| R9 | sandbox clone, edit one L1 receipt file size 70000 → 70001 → commit → counter | **exit 1**, L1 false clauses `evidence_id_ok`, `projection_ok`; `carriers_matched 2` (`c1-tamper.json`) — a 1-byte semantic edit of a committed receipt is caught by both the evidence-id recomputation and the rerun projection |
| R10 | sandbox clone, swap the `clean-empty` action cell `confirm-empty` → `none` → commit → c2-counter | **exit 1**, `bindings_false: ["v2_table_identical"]`, `matched 24` (`c2-drift.json`) |
| R11 | same, then restore `SKILL.md` to the pre-mutation bytes → commit → c2-counter | **exit 0**, `matched 26`, `met_target true`, `bindings_false []` (`c2-restore.json`) — the block-restore un-blocks |
| R12 | sandbox clone, append a comment to `tools/round-39/gen-squashfs.py` → commit → c2-counter | **exit 0**, `matched 26`, `met_target true`, `bindings_false []` (`c2-writer.json`) |

Sandboxes: `git clone -q --shared <lane> $S/fx.XXXX/lane`, toplevel asserted equal to the clone before any commit,
fixtures committed as `-c user.name=fx -c user.email=fx@fx`. No vendor firmware bytes and no extracted vendor files
were copied into the lane; all REA output stayed in my scratch.

## 2. Verdict verification

**R40-C1 = NOT MET: CONFIRMED.** R1 reproduces the L1's score exactly (3/4, exit 1, L2 the only miss, sole false
clause `nonregular_unpublished_ok`). The L1's causal account is also correct, and I verified it from the committed
receipt rather than from the counter's summary: `corpus/evidence/round-40/c1/L2/after.json` publishes
`firmware.bin_extract/usr/bin/busy` (sha `e28f81fc…`, 40000 bytes — the oracle's regular file) and keeps
`firmware.bin_extract/bin/busy` (symlink, REA-reported target `../usr/bin/busy`) as an `unpublished-entry` gap.
The counter's `same_rel` (`c1-counter.py:606-607`) then sees `/usr/bin/busy`.endswith(`/bin/busy`) and reports the
symlink as published. The demotion at `4d62ee5a` (PROVINCE `## Round-40 measured, not promoted`, README and the
knowledge entry reworded) states exactly this and does not over-claim.

**R40-C2 = MET: CONFIRMED.** R2 reproduces 26/26 with all 26 bindings true, and R3 reproduces the pair agreement
without the counter at all: the frozen interpreter over the 26 committed envelopes, joined to the frozen manifest,
gives 26/26. The interpreter shows no class-, id-, or envelope-name special-casing on its scoring path
(`HELDOUT_EXPECT` at `sqfs-triage-v2.py:838-845` is selftest-only and points at the round-39 held-out dir,
`HELDOUT_DIR` = `corpus/evidence/round-39/c2/heldout`). Expected pairs come from the manifest, which the counter
cross-checks against a fresh regeneration from the freeze seed; they are not read from the table.

## 3. Findings

### F1 — medium — P40-C1's target was unreachable from the freeze: L2's two clauses are jointly unsatisfiable

**Evidence (frozen inputs only; `artifacts/R40W2Sentinel/satisfiability.py`, output
`artifacts/R40W2Sentinel/satisfiability.json`).** At the freeze, L2's `oracle.tsv` contains the regular file
`usr/bin/busy` and L2's `nonregular.tsv` contains the symlink `bin/busy`. The counter's matcher is
`candidate == rel or candidate.endswith('/' + rel)`. `usr/bin/busy` ends with `/bin/busy`, so **every** published
path that satisfies `oracle_hits_ok` for `usr/bin/busy` (i.e. any `P` with `same_rel(P, 'usr/bin/busy')`, which
entails `same_rel(P, 'bin/busy')`) also trips `nonregular_published` and makes `nonregular_unpublished_ok` false.
Both are members of `CLAUSES`, so `matched` for L2 is false for **any** extraction that publishes the oracle — a
fabricated or ideal run included. `carriers_matched == 4` was therefore impossible at the freeze revision and at
every later revision that keeps the frozen counter and L2's frozen tables. The check finds no such collision on
V1 (697×381), V2 (8×95) or L1 (7×13); L2 is the only carrier, and the collision is structural, not run-dependent.

**Impact.** (a) The round's honest stop is right, but its cause is stronger than "a counter false negative": the
Core promotion could not have happened at 42c10a58 or anywhere else without a re-freeze, and the demotion text
(`PROVINCE.md`, `4d62ee5a`) should say so — "promotion waits for a re-frozen counter" is correct but leaves a
reader thinking a luckier run might have passed. (b) The kill rule's control (CTL-C1-0, do-nothing at the freeze)
cannot distinguish "4/4 achievable" from "impossible", so nothing in the wave-1 control set could have caught this
before the freeze; one dev receipt on the frozen carriers (the same 9 s run as R1) would have. (c) The target
number was set against a carrier whose tables were authored in the same freeze — the collision is between
`mk-l-carriers.py:62` (`'bin/busy': '/usr/bin/busy'`, an absolute link to a real in-tree file) and the counter's
suffix matcher, not between the run and the image.

**Smallest remediation (not applied — frozen path).** In the counter, run the oracle and non-regular comparisons on
the same normalisation the projection already uses: `rel_suffix()` (already defined at `c1-counter.py:745-764`,
strips up to the first `*_extract` segment) instead of bare `same_rel`, then compare exactly. On L2 that yields
`usr/bin/busy` vs `bin/busy` — no match — while V1/V2/L1 keep passing. Re-freeze, then re-score. Until then the
record should carry the entailment, not just "false negative".

### F2 — medium — the shared freeze-integrity rule is not enforced for one declared frozen C2 path

The claims' rule: "A score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path of that
claim; a later restore does not un-block (exit 2 `frozen_path_changed`, never `met_target`)." C2's frozen paths
include "`tools/round-39/gen-squashfs.py` (the generator's writer)". `c2-counter.py:75` is
`FROZEN = (INTERP, GEN, COUNTER, CLAIMS)` — the writer is absent, and its only check (`writer_matches_manifest`)
compares the sha of the **freeze** blob against the manifest's declared sha (`c2-counter.py:508-513`), so a
post-freeze edit of that file is invisible to it. R12: a commit in `FREEZE..REV` that appends a comment to
`tools/round-39/gen-squashfs.py` yields **exit 0, `matched 26`, `met_target true`** — the counter declares the
score admissible and met on a tree the claim calls inadmissible.

**Impact.** Not exploited at the measured revision: `git log 7fce3086..42c10a58 -- SKILL.md
tools/round-39/gen-squashfs.py tools/round-40/{sqfs-triage-v2.py,heldout-gen-v2.py,c2-counter.py}
plans/round-40-claims.md` is empty, so 26/26 stands. The exposure is future-facing and structural: the *only*
thing that would catch a behaviour-changing writer edit is the carrier regeneration (`carriers_regenerated`,
which materialises the writer from the **freeze** tree at `c2-counter.py:494-505`), so an edit that changes output
fails a binding (exit 1) while an edit that does not change output passes as `met` — and either way the reason
code is not the promised exit 2.

**Smallest remediation.** Add `'tools/round-39/gen-squashfs.py'` to `FROZEN` in `c2-counter.py` (one string), so
`frozen_changes()` raises `frozen_path_changed` (exit 2) like the other four; re-freeze.

### F3 — medium — "a later restore does not un-block" fails for the SKILL v2 block

The v2 block is a declared frozen C2 unit but not a path, and the counter governs it with a byte-equality binding
(`v2_table_identical`), not drift. Consequences I measured:
* still-present mutation: R10 → **exit 1**, `bindings_false ["v2_table_identical"]`, `matched 24`. The claims say
  a frozen-path change is `exit 2 frozen_path_changed`; the counter's own docstring lists that reason code among
  its exit-2 set, so a consumer keying on the reason code sees "not met" where the contract says "inadmissible".
* mutate → restore (`SKILL.md` byte-identical to the freeze at the scoring rev, R11) → **exit 0, 26/26,
  `met_target true`** — precisely the "restore does not un-block" case the rule forbids.

**Impact.** The claim cannot be inflated this way (the final bytes must equal the freeze's, so a different table can
never be scored), and no such commit exists before 42c10a58. What breaks is the round's own provenance statement:
a scorer reading the counter's verdict cannot tell that a frozen unit was edited and reverted inside the scored
range. That is the class of thing the rule was written to stop (round 39's `e40a25df` "post-freeze edit
quarantine"), and it is the one place the two claims implement the same sentence differently — C1 does it by path
(R7/R8, both exit 2).

**Smallest remediation.** Add a `first_parent`-free path check for `SKILL.md` that compares the `<!--
sqfs-triage-table v2 -->` block across every commit in `FREEZE..REV` (the counter already parses blocks at two
revisions via `parse_v2_rows`) and raises `frozen_path_changed` when any intermediate commit's block differs, even
if the scored rev matches. Re-freeze.

### F4 — low — `SKILL.md` carries an uncommitted modification in the lane during wave 2

`git -C kaidoku-shokunin status --porcelain` → ` M SKILL.md`; the diff is 19 added lines at EOF ("### Round-40
instrument registry", a 12-row tool table). mtime `2026-10-26 16:24:08`, i.e. **after** the wave-2 dispatch commit
`0b15c8b2` (16:23:11), so it belongs to wave 2, not to the freeze. It is **outside** the frozen v2 block: the block
(380 lines from the `<!-- sqfs-triage-table v2 -->` marker through the last row) hashes identically at
`7fce3086`, `42c10a58`, `HEAD` and the worktree (`sha256 6b0123e5…`), and `w2-spec.json` contains no seat that
owns an "instrument registry" edit.

**Impact.** No claim effect (counters read git objects at a revision, never the worktree; C2's binding reads the
block). The hazard is that the worktree no longer matches the measured revision: a wave-2 report that cites the
registry as a measured artifact would be citing bytes no revision contains, and the L1's eventual commit would
place wave-2 text under a wave-1-style instrument heading with no review record. Worth naming in the wave-2
ledger rather than silently reverting — I did not touch the file.

**Remediation for the L1.** Either commit it as a labelled wave-2 change (with the seat that authored it), or
discard it; do not let it ride along inside another commit's diff.

### F5 — low — the C2 counter's selftest leaks `gen.*` dirs into the shared scratch root

`/fast/scratch/hyaku/kaidoku-r40/` held **584** `gen.*` dirs at 16:27 and **625** at 16:33 (650 top-level entries;
seat dirs and `_l1`, `counter` make up the rest). Each holds `H01…H26/` fixture trees and no vendor bytes. Source:
`c2-counter.py:1080` `gdir = tempfile.mkdtemp(prefix='gen.', dir=sroot)` inside the selftest's `build()`, with no
removal (the sibling `c2-case.*` dirs *are* cleaned: 0 on disk). One per selftest invocation per seat, hence a
~41-dir batch at each of 15:23-15:29 (wave 1), 16:05, 16:10 and 16:25+ (wave 2). The path is frozen, so this is a
note for the re-freeze, not an edit.

Residue in the same root, also from this round: `_l1/V1.carrier` (5 442 392 B), `_l1/V2.carrier` (26 013 550 B) and
`_l1/cache/{ac4098bd…,5ccc7614…}.bin` hold **vendor-derived bytes**. Permitted (never committed, and the counters
need the cache), but it is 31 MB of AVM-licensed material parked in shared scratch with no owner; the licence rule
is about redistribution, and this is not redistribution — flagging it for the scratch sweep, not as a breach.

## 4. Round-end seam check

1. **Fleet root** — `git -C /home/vgpnk/Projects/shokunin status --porcelain` → exactly one line,
   `?? .ufo/reports/round-48/tameshi.md` (11 014 B, first line `# tameshi — round 48 report (attempt 3, L1
   TameshiR48a3)`). Nothing untracked names kaidoku or round-40. **PASS** (the one item is a different lane/round;
   untouched).
2. **Lane** — `git -C kaidoku-shokunin status --porcelain` at 16:24: ` M SKILL.md` (F4) and three untracked
   wave-2 operational files: `.ufo/waves/round-40/r40-w1-status.json`, `w2.ready`, `w2.ready.partial` (empty at the
   check; the dispatch marker advanced to `w2.ready.dispatched` during the seat, and other wave-2 seats' reports
   and `l1/scores/` receipts appear as untracked files as they land — expected). Ignored: 9 entries — `.jj/` (the
   colocated jj store) and 8 `__pycache__/` dirs (`tools/round-3{4,5,6,7,8,9}/`, `.ufo/waves/round-34/…`,
   `.ufo/waves/round-40/w1/artifacts/R40C1Projection/`). No tracked file other than `SKILL.md` differs
   from `HEAD`; `tools/round-40/` is clean, so the working tree I ran R1/R2 against is the frozen tool set
   (sha256s match the L1's receipts, R6). **One deferral, otherwise PASS.**
3. **Wave-1 reports** — 42 `.md` in `.ufo/waves/round-40/w1/`, none at `round-40/*.md`, none under
   `round-40/artifacts/` (there is no such dir; wave-1 artifacts live under `w1/artifacts/`).
   `git diff --stat 7fce3086..HEAD -- .ufo/waves/round-40/w1/` is empty and `git status` shows no modified w1 file;
   newest w1 mtime `2026-10-26 15:58:44` < freeze `16:13:52`. **PASS** — no post-freeze edit, and no round-39-style
   "report written outside the wave dir" recurrence.
4. **Secrets / home-dir leaks** — `corpus/evidence/round-40/`: 90 files containing `/home/vgpnk`, 64 containing
   `/fast/scratch`; `.ufo/waves/round-40/`: 587 and 535. Those are REA receipt `parameters.path` /
   `parameters.output_directory` and `run.json` `outdir`/`cwd` values, i.e. the provenance the predicate requires
   (`run_provenance_ok` demands a `/kaidoku-r40/` scratch segment) — expected, not a leak of anything secret.
   Credential patterns: `-----BEGIN … PRIVATE KEY-----` 7 files, `ghp_` 5, `password` 10, `api[_-]key` 1,
   `AKIA…` 0. Every hit is pattern *text*: the round-39 sentinel transcripts re-committed under
   `w1/artifacts/R40CL6Receipts/*.json` and `r40-w*-status.json` (which embed the previous seat's report body,
   including its grep patterns), `w1/artifacts/R40Sentinel/04-secrets.txt`, `w1/R40Sentinel.md`, and FRITZ!OS
   release-note prose under `w1/artifacts/R40C1VendorScout/info/` and `R40SrcAvmVendor/info_en.txt`. **No
   credential found.** One structural note: `r40-w1-status.json` / `r40-w1-results.json` embed whole seat reports,
   which is how the same pattern text lands in two places; harmless here, worth knowing before those files are
   quoted elsewhere.
5. **Leftover scratch** — see F5: 650 top-level entries, 625 of them `gen.*`; plus `_l1/` (vendor-derived bytes)
   and `counter/`. My own scratch root is removed at the end of this seat.

## 5. Sentinel clauses

* **`resume_continuity_v1`** — not applicable, and for the same reason stated in round 19: nothing in this round's
  surface resumes a run. `grep -rn resume_continuity_v1` over the lane matches only narrative text in
  `corpus/evidence/round-25/proposal/planner-advisory.md`, `.ufo/waves/round-{17,18,19}/…`; no counter, carrier
  driver or REA wrapper implements session selection, resume or run-state mutation. There is no rejection path to
  exercise, so the zero-mutation property is vacuous here rather than assumed. **[INFERENCE]** the same clause will
  stay vacuous until a tool in this lane keeps run state.
* **Zero mutation on rejection** — exercised on the one rejection path that exists, the freeze-drift gate: R7 and
  R8 both exit 2 with the offending path named and no `met_target`, and the sandbox clone's `git status
  --porcelain` is empty afterwards (the counter's only writes are `--json-out` and its own
  `$HYAKU_SCRATCH/kaidoku-r40/counter` scratch). R9 shows the fabrication gate firing in the safe direction too:
  a 1-byte receipt edit breaks `evidence_id_ok` **and** `projection_ok`.
* **Faithful-readers check** — the fs/trust boundaries I cared about all hold: every input is read with
  `git show REV:path` (`show()` at `c1-counter.py:301`), never from the worktree, so F4's dirty `SKILL.md` cannot
  move a score; the evidence-id rule is not retyped but executed from the freeze's `xpin-attribute.mjs` against the
  installed package; the regeneration materialises generator + writer from the **freeze** tree, so a post-freeze
  edit cannot change what the replay compares against.
* **One leniency worth knowing (no action needed now)** — `same_rel` is also used by `gap_check`, so a gap whose
  `relative_path` names a *published regular file* can be counted as the colliding symlink's gap (on L2,
  `X_extract/usr/bin/busy` would count as `bin/busy`'s `unpublished-entry`). Unreachable without a matching real
  run because `projection_ok` compares the committed receipt to a fresh one; it is the same root cause as F1 and
  the same one-line fix.
* **REA-reported symlink targets are post-resolution** (`dev/new_led` → `null`, `lib/ld-uClibc.so.0` →
  `ld-uClibc-1.0.31.so`, absolute `/proc/mounts` → `../proc/mounts`; 44/263 mismatches on V1, 5/85 on V2, 1/2 on
  each lane carrier). So `unpublished_entries[].link_target` is not the stored SquashFS target and must not be
  used to classify absolute-vs-relative links. The counter does not use it (kind + gap only), and the frozen
  reader is faithful (it prints the stored target) — recorded so a future reader of the gap rule does not build on
  `link_target`.

## 6. Calibration — what these findings do not show

* They do not unmake R40-C2: the 26/26 is real, reproduced twice (counter and bare interpreter), the block bytes
  are the freeze's, the seed is the freeze hash, and the manifest precedes its envelopes (`2d1abc`, same commit —
  "no later than" holds by equality).
* They do not make the measured C1 score inadmissible: no C1 or C2 frozen path was touched in `FREEZE..42c10a58`
  (checked per claim), and `frozen_path_changed` is empty in both reproductions.
* F1 is a statement about the *predicate's reachability*, not about the extraction: all four carriers publish every
  oracle file, the handler is `squashfs_v4_be` with no failed chunk on all four, gaps follow the frozen rule
  (L1/L2: one `unpublished-entry` per symlink + one `depth-limited`; V1: 264 gaps on 381 non-regular entries), and
  the four carrier pins verify (`ac4098bd…`, `5ccc7614…`, `2521ded6…`, `fec0f72d…`).
* The C2 action half is partly self-corroborating, not independent: the generator's selected action map
  (`ACTION_SETS['interp']`) and the table's action column come from the same wave-1 prototype
  (`heldout-gen-v2.py:96-99`, source comment "interp — artifacts/R40C2Interp/v2-block.md:2"). A token mismatch
  could only have appeared if the table had been edited away from that prototype, so treat the label half as the
  load-bearing one. The claims' disclosed limits cover the closed-class and operation/provider coupling but not
  this one; worth one clause in the re-freeze.
* My C1 reproduction used the counter's own rerun path (four fresh REA runs), not an independent REA invocation;
  the independence in this seat's evidence is R4 (reader) and R3 (interpreter), which share no code with the
  counters' gate logic.

## 7. Tooling and hygiene

Nothing installed, upgraded, moved or removed — python3 3.14, `unblob` 26.6.4, `sasquatch-v4be` 4.5.1,
`rea-agents` 6.5.0 used read-only as the counters invoke them. No `pacman`, no `npx -y` of anything new (the
counters' own `npx -y rea-agents@6.5.0` resolved from the existing cache). Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40W2Sentinel` removed before yielding; everything cited is under
`.ufo/waves/round-40/w2/artifacts/R40W2Sentinel/`. No VCS mutation anywhere: clones under my scratch only, all
toplevels asserted, no `git add/commit/checkout/reset/stash/pull/push` in the lane or the fleet repo (every
`commit`/`checkout` in R7-R12 ran inside a throwaway clone whose toplevel I asserted first).

Artifacts: `satisfiability.py`, `satisfiability.json` (F1 proof), `c1-repro.json`, `c2-repro.json`, `interp.json`,
`c1-drift.json`, `c1-drift2.json`, `c1-tamper.json`, `c2-drift.json`, `c2-restore.json`, `c2-writer.json`,
`reader-rederivation.txt`.
