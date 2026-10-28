# R44W2Province — PROVINCE.md audit after the R44-C1 honest stop

Seat `R44W2Province` · lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · base
`c29360e3ba5381a5ab69e372d0d9577970f85018` · freeze `c48f8a4bfd449300c975668e59aae5b5538b6a84` ·
measured revision `55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac` · lane HEAD at audit
`8bb1090af3fef64477c4337855e4347472db2701`.

Scope: the PROVINCE landing at the measured revision (prefix-preservation binding, the
`## Round-44 measured, not promoted` section, the Round-44 frontier note, the round-42 note it sits
after, the `## Adjacent` refusal region, and whether any promotion is left standing in prose), plus
the record's claims about the two frozen counters and M44-2. All artifacts and receipts:
`.ufo/waves/round-44/w2/artifacts/R44W2Province/` (`receipt.json` + every stdout/JSON cited here).
No claim, counter, rubric, frozen byte or production doc was modified.

**Record snapshot.** Record citations are pinned to the committed HEAD `8bb1090a` via
`git show HEAD:<file>`; every counter run is revision-pinned (`git show <rev>`), so worktree dirt
cannot move them. During this audit `LOG.md`, `SCORECARD.md` and
`corpus/lessons/round-44.md` were **dirty in the worktree** (other seats' in-flight edits at
11:26–11:27, `git status --porcelain`), so the worktree copies were not used as evidence for the
committed record. Where the in-flight lesson edit already changes a row I attack, D5 says so.

## Verdict

| # | Question | Verdict |
|---|---|---|
| 1 | Prefix binding: bytes `1..53354` unchanged at `55bcce69`? | **CONFIRMED.** `sha256(base blob) = sha256(rev[1..53354]) = e385f119569024152a55f5d27f4812e2951f1a990924fb21c68db9848c34e848`; `cmp` identical. 422 lines/53354 B → 430 lines/54780 B; appended 1426 B, sha256 `89d2a46f01011dd5840b1a5bffa40adda102b11a362eac3c79758e4886ac52e4`. SHONEN's PROVINCE pointers (:157, :376, :378-384, :386-394, :97-125) cannot drift; largest is 394 < 422. |
| 2 | Is the Round-44 section's status accurate? | **STATUS YES, CAUSE NO.** "measured, not promoted" and "v1/v2 remain Frontier" match measurement (C1 4/4 at the measured revision, no Core row anywhere in the live docs). The stated cause misreports what the instrument returned → D1, D3. |
| 3 | Frontier statement accurate for `squashfs_v1`/`squashfs_v2`? | **YES on status, wrong mechanism word** ("aligns the predicate and instrument" names the wrong pair) → D3. |
| 4 | Conflict with the round-42 frontier note (`PROVINCE.md:416`)? | **NONE.** :416 keeps `SquashFS v1/v2` Frontier; :430 keeps it Frontier with a measurement record. The round-44 note asserts no supersession, so it does not contradict :416. |
| 5 | `## Adjacent` refusal region untouched? | **CONFIRMED.** sha256 of lines 97-125, 223-249, 266-267, 276-312, 374 is `e2b943eb…fd68` at both base and rev; the whole prefix is byte-identical, so every Adjacent line is untouched by construction. |
| 6 | Promotion left standing in prose? | **NO in live docs** (PROVINCE, `corpus/README.md`, the entry, SCORECARD at `55bcce69`, SHONEN, LOG). Two hazards: synthetic promotion prose in the committed positive-control tree, and the withdrawn promotion's `met_target true` receipt still in evidence → D7. |
| 7 | C1 verdict (`carriers_matched 4`, `met_target false`, exit 1 at `55bcce69`)? | **CONFIRMED, reproduced** (7.3 s). |
| 8 | Is the honest stop the only correct reading? | **CONFIRMED under the intended reading**, but the record's stronger "internally unsatisfiable / no real run can satisfy" is not established by the frozen bytes → D2. |
| 9 | Does the record say exactly that? | **PARTLY.** `LOG.md:3201` and `SCORECARD.md:3525` at HEAD `8bb1090a` do (they include the `4cc1ac11` exit 0 and the BOTH-clauses wording). PROVINCE:428-430 does not → D1, D4. |
| 10 | M44-2: honest, sufficient, gate really catches it? | **Incident confirmed at both counters and at HEAD; the gate catches it** (exit 1, 8 touched/8 blob-changed). Sufficiency is pathspec-dependent and the gate's no-pathspec default is broken/misdocumented → D5, D6. |

## Measured facts (each with a receipt in `artifacts/R44W2Province/`)

| receipt | command (argv in `receipt.json`) | exit | stdout sha256 | wall |
|---|---|---|---|---|
| `c1-55.json` | `python3 -I -B <LANE>/tools/round-44/c1-counter.py --root <LANE> --rev 55bcce69… --freeze c48f8a4b… --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | **1** | `eea45d37…cac9f8d` | 7.29 s |
| `c1-4cc1.json` | same, `--rev 4cc1ac11…` | **0** | `8742a90d…d8fee6a` | 7.05 s |
| `c2-55.json` | `python3 -I -B <LANE>/tools/round-44/c2-counter.py --root <LANE> --rev 55bcce69… --freeze c48f8a4b…` | **0** | `dd7c529b…316a9b3` | 4.60 s |
| `pf-c86ea508…stdout` | preflight `--rev c86ea508… --pathspec tools/round-44` | **1** | `20a87d4d…0a28896` | 93 ms |
| `pf-55bcce69…stdout` | preflight `--rev 55bcce69… --pathspec tools/round-44` | **0** | `c8a03c26…430a870f` | 89 ms |
| `pf-8bb1090a…stdout` | preflight `--rev 8bb1090a… (HEAD) --pathspec tools/round-44` | **1** | `c302813c…a1cdf99` | 90 ms |
| `pf-nopathspec.stdout` | preflight `--rev 55bcce69…` (no `--pathspec`) | **1** | `df657c50…a68c0cc` | 32 ms |

Observed values, `c1-55.json`: `exit_code 1`, `carriers_matched 4`, `met_target false`,
`bindings_false ["province_core_section","province_core_row","frontier_note"]`, `failing []`,
`frozen_path_changed []`; per carrier `run_provenance_ok`, `evidence_id_ok`, `projection_ok`,
`subject_pin_ok`, `oracle_hits_ok` all `true`; published/oracle hits 3/3, 3/3, 4/4, 4/4.
`counter_sha256 9f2cc140…ffea993` (matches the committed receipt), `revision`/`freeze` as frozen.
`c2-55.json`: `exit_code 0`, `entries_evaluated 80`, `mismatches []`, `frozen_path_changed []`,
`met_target true`, `counter_sha256 085192ea…636c277`, `rubric_sha256_at_rev e8cc0ded…55e755e` — all
equal to `.ufo/waves/round-44/l1/c2-score-at-55bcce69.json`. Every field I compared equals the
committed scores; nothing needed re-measuring from the record's side.

## Numbered defects

**D1 (medium) — `PROVINCE.md:428` states a cause the frozen counter does not report, and omits half
of the frozen claim's contradiction.**
Line 428 says: "The counter matched 4/4 and published every oracle file, but the frozen R44-C1 claim
and counter disagree about `parameters.output_directory`: the claim required the committed evidence
path, while the counter accepts only the `/kaidoku-r44/` scratch provenance. The score therefore does
not satisfy the frozen predicate".
Measured, at exactly the cited revision:
`python3 -I -B <LANE>/tools/round-44/c1-counter.py --root <LANE> --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --pkg65 <rea-agents 6.5.0>` → exit **1**,
`carriers_matched 4`, `met_target false`, `bindings_false = [province_core_section, province_core_row,
frontier_note]`; `run_provenance_ok` is **true** on all four carriers. The exit 1 is therefore entailed
by *not promoting* (the three document bindings), not by the provenance disagreement; the provenance
conjunct of the predicate passes. The sentence's "therefore" asserts otherwise. The frozen claim text
(`plans/round-44-claims.md:34-36` amendment item 3 **and** `:136-138` predicate) required the field to
name the committed path *and* the scratch segment; line 428 keeps only the first half, so a reader of
PROVINCE alone sees an instrument that deviated from a satisfiable claim rather than a frozen text that
contradicts itself. LOG.md:3201 and SCORECARD.md:3525 do state it exactly (including the `4cc1ac11`
exit 0). Fix: an appended dated correction on `PROVINCE.md:428` mirroring the LOG wording.

**D2 (medium) — "internally unsatisfiable on one field" / "no real run can satisfy" is stronger than
the frozen bytes support, because the counter's provenance binding is a bare substring test.**
`tools/round-44/c1-counter.py:1176-1182`:
`provenance_ok(od)` = `isabs(od) and '/kaidoku-r44/' in od and '..' not in od.split('/')`.
Measured by importing the frozen module (no mutation; `provenance-probe.txt`):

```
True   /fast/scratch/hyaku/kaidoku-r44/probe/c1-run.v1le.1/rea-out
False  /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-44/c1/v1le
True   /fast/scratch/hyaku/kaidoku-r44/corpus/evidence/round-44/c1/v1le
True   /tmp/kaidoku-r44/x
True   /home/someone/else/kaidoku-r44/run
```

Consequences: (a) a scratch output root spelled `…/kaidoku-r44/corpus/evidence/round-44/c1/<id>`
satisfies the counter *and* a literal reading of amendment item 3 simultaneously, so the two clauses
are contradictory in intent but jointly satisfiable in letter; (b) the binding is not anchored to
`$HYAKU_SCRATCH`, so it does not establish "this round's scratch segment" as the claim words require —
any absolute path containing the token passes. The honest stop still stands (the only constructions
that satisfy both clauses are pathological scratch spellings, and the intended reading forbids them),
but the record's load-bearing sentence must be weakened, and round 45's satisfiability preflight
should anchor `provenance_ok` to the round scratch root and reject the committed relative segment in
the scratch path (or make the claim single-sourced).

**D3 (low) — `PROVINCE.md:430` names the wrong conflicting pair.**
"The frozen claim's output-directory clause disagreed with the counter's `/kaidoku-r44/` provenance
binding" is right; the following "pending a new pre-data freeze that aligns the predicate and
instrument" is not: the predicate (`plans/round-44-claims.md:136-138`) and the instrument agree
(all four `run_provenance_ok` true, exit 0 at `4cc1ac11`). The disagreement is between the amendment
record (`:34-36`) and the predicate. A round-45 reader "aligning the predicate and instrument" would
change the wrong side.

**D4 (medium) — PROVINCE does not disclose the `4cc1ac11` `met_target true`, so its two-line record
cannot be audited from PROVINCE alone.**
Measured: `python3 -I -B …/c1-counter.py --rev 4cc1ac11657590c25b6565d6ab220f53372a94d3 …` → exit
**0**, `carriers_matched 4`, `met_target true`, `bindings_false []`,
`province_core_section/province_core_row/frontier_note` all true (my `c1-4cc1.json`; the committed
`corpus/evidence/round-44/c1/counter-at-4cc1.json` records the same). PROVINCE:428 says only "The
counter matched 4/4" and never mentions that the same receipts scored met at the promotion state, nor
that `55bcce69` removed that promotion. LOG.md:3201 does. Because the claim names PROVINCE as the
landing document, the province ledger should carry the one fact that makes its own exit-1 meaningful.

**D5 (low) — lesson M44-2's "added/edited 8 files" is imprecise (all 8 are modifications), and the
committed row attributes the write to a commit while the in-flight worktree edit says the commit came
from the orchestrator's non-author sweep.**
`git -C <LANE> log -m --diff-merges=first-parent --name-status c48f8a4bfd449300c975668e59aae5b5538b6a84..c86ea508188c50e2645b1f9bba65df4177cda6b1 -- tools/round-44` → exactly 8 rows, status `M`
on `tools/round-44/control-fixtures/{pos,c3}/…`, **no `A`**. The rest of the row checks out: both
counters exit 2 at the tip with those same paths (`c1-score-at-tip.json`, `c2-score-at-tip.json`), and
the violation is still present at HEAD (preflight exit 1, same 8). Timeline: `c86ea508` is committed
**10:43:43**, 46 min after the honest stop `55bcce69` at 09:57:16, and all eight commits
`fee6e98a..8bb1090a` carry the same author/committer `kaidoku-shokunin <kaidoku@shokunin.local>` — so
git identity cannot distinguish a lane commit from the fleet orchestrator's sweep; the worktree
lesson edit (not yet committed) now says attempt 1 mutated the 8 files in the worktree at 09:50 and
the sweep committed them, and its R44-CL1 fix text already asks for the gate to run in the
sweep/pre-push path. If that edit lands, D5's attribution half is closed; the committed HEAD row still
needs the "all `M`, none added" correction. This is also why D6 matters: a gate wired only into the
lane's own commit sequence would not have stopped a sweep commit.

**D6 (medium, this is the M44-2 fix) — `tools/round-45/frozen-path-preflight.py` catches the incident,
but its no-pathspec mode is broken and its documented default is false, and the demonstrated pathspec
covers one of the claim's frozen families.**
Tool help: `--pathspec … Default: none (tree backstop only)`. Measured with *no* `--pathspec` at
`55bcce69`: exit **1**, `verdict frozen_path_changed`, `touched 110` (first paths `PROVINCE.md`,
`corpus/README.md`, the round-44 entry, `corpus/evidence/round-44/controls/…`). With an empty pathspec
the tree backstop is skipped (`if pathspec:` guard), so that mode is neither "tree backstop only" nor
usable. With `--pathspec tools/round-44` it is correct: exit 1 at `c86ea508` (8 `touched`, 8
`blob_changed`) and at HEAD, exit 0 at `55bcce69`. The claim's frozen set is wider than that one
family — `plans/round-44-claims.md`, `tools/round-42/fixtures.json`, `tools/round-42/c1-counter.py`,
`tools/round-43/c1-counter.py`, the four carrier bins under `corpus/evidence/round-42/c2/fixtures/`,
`corpus/evidence/round-44/oracle/`, `tools/round-44/control-fixtures/**` — so a caller following the
demonstrated invocation would miss a post-freeze oracle or claims edit. Fix: make the pathspec list a
flag file/`--claim round-44` preset, fix the help string, and make the empty-pathspec case exit 2
rather than red on every changed path.

**D7 (low, hazard) — promotion prose survives in the committed positive-control trees and in the
SCORECARD row's claim-surface phrase.**
`corpus/evidence/round-44/controls/pos/tree/PROVINCE.md:424` carries `## Round-44 additions to Core`
and `:430` "SquashFS v1/v2 moved Frontier → Core" (430 lines; sha256 `1aab8d0d…b3e128`, a synthetic
control tree, not the withdrawn `9d3d1862:PROVINCE.md` blob `b7db0721…a5abdc`); the same promotion
text also sits at `tools/round-44/control-fixtures/pos/PROVINCE.md` (the frozen fixture),
`corpus/evidence/round-44/controls/pos/tree/corpus/README.md`, and the `pos/tree` copies under
`.ufo/waves/round-44/controls/`. Separately, `SCORECARD.md:3525` (HEAD) describes the claim surface as
"`squashfs_v1`/`squashfs_v2` Frontier → Core", with the same row's verdict cell
"**not met — honest stop (measured 4/4, no Core promotion)**" and the counter-met precursor cited.
None of these is a live promotion: the counter reads only the root `PROVINCE.md`
(`c1-counter.py:2149` `show(root, rev, 'PROVINCE.md')`), and the POS tree exists to make CTL-C1-POS
green. But any repo-wide grep/regex validator for `## Round-44 additions to Core` or
`Frontier → Core` hits them and could report a live promotion that does not exist.

## Residual risk and verification gaps

- **Unscored claim binding.** The counter never reads `provenance.json` and never compares the
  committed evidence tree with the scratch tree (no `provenance.json` reference in
  `tools/round-44/c1-counter.py`). The predicate's "the runner binds the scratch-produced tree to the
  verbatim committed copy" is therefore a runner assertion, not a scored binding:
  `corpus/evidence/round-44/c1/v1le/provenance.json` records `rea_output_directory
  /fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/c1-run.v1le.1342995/rea-out`, `rewritten false`.
  This is R44-CL3/D-13 territory and is correctly disclosed as a limit — but it means the four
  receipts prove projection equality, not that the committed tree is the produced tree.
- **The frontier-note binding cannot see a non-promoting note.** `frontier_note` requires the entry
  stem on the line (`c1-counter.py:2161` `FRONTIER_MARK in l and STEM in l and SQFS12_TEXT_RE`), and
  the honest-stop note omits the stem, so "note present but not superseding" is indistinguishable from
  "note missing". Deliberate and harmless here; note it if the binding is reused.
- **No C2 entry checks the new section.** All 21 rubric rows that touch PROVINCE read the SHONEN box-4
  pointers into the prefix (97-125, 157, 376, 378-384, 386-394); none evaluates the appended section.
  C2's exit 0 therefore says nothing about PROVINCE's round-44 text — this audit is its only check.
- I did not re-run the C1 controls/selftest or the dev arms (control seats' scope); I did not re-execute
  REA by hand (the counter's `projection_ok` rerun did, 4 carriers, inside the 7.3 s run); REA's
  committed receipts could not be attributed to a process (R40-CL2 stays open).
- Tooling: nothing installed or upgraded. No mutating git/jj command was run anywhere; every git call
  was `show`/`log`/`diff`/`rev-parse`/`ls-tree`. One lane, no fixture repo, no `/tmp` evidence path.
  Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2Province/` removed before this file was written.
