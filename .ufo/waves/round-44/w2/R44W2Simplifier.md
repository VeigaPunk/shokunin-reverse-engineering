# R44W2Simplifier — dead-weight scan of the round-44 additions

Seat `R44W2Simplifier`, round 44 wave 2. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
(`<LANE>` below). Base `c29360e3ba5381a5ab69e372d0d9577970f85018`; freeze
`c48f8a4bfd449300c975668e59aae5b5538b6a84`; admissible measured revision
`55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac`; lane tip at dispatch
`c86ea508188c50e2645b1f9bba65df4177cda6b1`, observed tip during this seat
`8bb1090af3fef64477c4337855e4347472db2701`. Scratch
`/fast/scratch/hyaku/kaidoku-r44/R44W2Simplifier` (deleted before yield; see §7).

**Deleted: nothing.** No mutating `git`/`jj` command was run against the lane, the fleet repo or
any sibling tree; the only commits made anywhere were inside throwaway fixture repos under this
seat's own scratch (`mktemp -d`, `git -C "$D" rev-parse --show-toplevel` asserted to equal `$D`
before the first commit, removed after) — the prompt's sanctioned fixture exception. No tool was
installed, upgraded or removed (operator rule 2026-10-19: no installs; `pacman` untouched). The
only files this seat wrote are this report and
`.ufo/waves/round-44/w2/artifacts/R44W2Simplifier/**`.

Axes used for the scan (Godspeed: keep moves that improve an axis and harm none):

- **A1 predicate necessity** — every frozen byte must be read by a predicate clause or a control,
  otherwise touching it can only manufacture an exit-2, never a correct score.
- **A2 single authority** — one copy authoritatively owns each fact; a second copy that can
  diverge is a correctness hazard, not just weight.
- **A3 evidence sufficiency** — the record cites bytes that exist at a committed revision, and a
  verdict is not re-stored at O(rubric) cost per run.

---

## 1. Receipts (seat `R44W2Simplifier`)

All commands are read-only. `python3` is `Python 3.14.8`, `git 2.56.0`, `jj 0.45.1`. `sha256` is
over the command's stdout. Walls are `time.monotonic()` around the child.

| # | command (exact; `<S>` = scratch) | exit | stdout sha256 | bytes | wall |
|---|---|---|---|---|---|
| R1 | `python3 -I -B <LANE>/tools/round-44/c1-counter.py --root <LANE> --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac --freeze c48f8a4bfd449300c975668e59aae5b5538b6a84 --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work <S>/c1work2 --json-out <S>/c1-55bc-recheck2.json` | **1** | `eea45d374bb450f15c549ca5e7c7803ac9e6c31bb982fae45d6542ee8cac9f8d` | 1324 | 7.254 s |
| R2 | `python3 -I -B <LANE>/tools/round-44/c2-counter.py --root <LANE> --rev 55bcce69… --freeze c48f8a4b… --work <S>/c2work2 --json-out <S>/c2-55bc-recheck2.json` | **0** | `dd7c529bb6340c364854093937bce3d90ec980ebdea951263bb38dc52316a9b3` | 1050 | 4.320 s |
| R3 | R1 with `--rev 8bb1090af3fef64477c4337855e4347472db2701` | **2** | `0e1c1f556d375f025f83bd0405e8dbb52de5021a9e69c2838d22eb832e4e3845` | 1313 | 0.077 s |
| R4 | R2 with `--rev 8bb1090af3fef64477c4337855e4347472db2701` | **2** | `0a81b8b2e85b08914b5a2f1b3856601f53d8c6f491ae5e00794c9bcf9a064c64` | 1676 | 0.082 s |
| R5 | `python3 -I -B <LANE>/tools/round-45/frozen-path-preflight.py --root <LANE> --freeze c48f8a4b… --rev c86ea508188c50e2645b1f9bba65df4177cda6b1 --pathspec tools/round-44 --json-out <S>/pf_c86.json` | **1** | `20a87d4d81eedaa79defea6c0fcbbe248bd415e35460b48dd6b66fffe0a28896` | 2092 | 0.085 s |
| R6 | R5 with `--rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac` | **0** | `c8a03c2673a9bfd52b23077a604e48288e44c70ff5cedd5782bc4fa6430a870f` | 226 | 0.085 s |
| R7 | R5 with `--rev 8bb1090af3fef64477c4337855e4347472db2701` | **1** | `c302813c8069f581e4674d3f5335f9a8f4db903015df772eaa509ee08a1cdf99` | 2092 | 0.083 s |
| R8 | R5 with no `--pathspec`, `--rev 8bb1090a…` | **1** | `ea8cfe7638b88ed0319ac7c987e6f288b186ea2b98b590d846eb6f2a771e0b08` | 84351 | 0.032 s |
| R9 | R5 with `--rev 55bcce69… --pathspec SCORECARD.md` | **1** | `cfd07d85ba3e663bdd96d5c1ec728bb3fc58eabefac147c9a950d4c33b011359` | 345 | 0.032 s |

R1/R2 reproduce the committed scores exactly (same field values as
`.ufo/waves/round-44/l1/c1-score-at-55bcce69.json` and `c2-score-at-55bcce69.json`); R3/R4
reproduce the tip exit-2 that M44-2 records; R5–R8 reproduce the preflight table in
`w2/R44W2Preflight.md` byte-for-byte (same stdout sha256), independently. Fixture runs (§3.3) are
in `artifacts/R44W2Simplifier/fixture-matrix.json`; every fixture repo was
`mktemp -d`-created under the scratch dir, `git -C "$D" rev-parse --show-toplevel` asserted to
equal `$D` before the first commit, and removed after.

Caller analysis caveat: the `lsp` device is **not mounted in this seat** (the tool list carries
`read/bash/edit/eval/glob/grep/task/wait/web_search/write/yield` plus MCP tools; no `lsp`
`references`). Deletion-candidate caller evidence below is therefore **literal `grep`/`git grep`,
not semantic reference proof**; that limitation applies to every "no caller" claim in §2.

---

## 2. Candidate-by-candidate

### 2.1 `tools/round-44/c1-oracle.py` — **used as a builder, not as a runtime instrument; keep**

- Evidence of use: `.ufo/waves/round-44/l1/c1-oracle-final-receipt.json` records the exact argv
  (`python3 -I -B c1-oracle.py … --merge-carriers tools/round-44/carriers.json`) with
  `exit_code 0`; the same run's `oracle` rows are the frozen `oracle` blocks inside
  `tools/round-44/carriers.json`. It is the only published derivation of those rows.
- Evidence of non-use at score time: `grep -rn "c1-oracle" tools/round-44/*.py tools/round-44/*.sh
  tools/round-44/*.json` matches **only inside `c1-oracle.py` itself** (exit 0, hits are its own
  `prog=`, schema and messages). `c1-counter.py` reads `carriers.json`, never this tool.
- Risk of deleting: `tools/round-44/` is a frozen **directory** pathspec for both counters
  (`c1-counter.py:286 FROZEN_PREFIXES`, `c2-rubric.json` `frozen_dirs: ["tools/round-44"]`).
  Deleting it after the freeze is a `frozen_path_changed` (exit 2) on both counters and destroys
  the reproduciblity of the frozen oracle rows.
- **Recommendation: keep.** Round 45 may delete only its hardcoded `CARRIERS` fallback (S-6) and
  add the builder digest to the receipt (S-5).

### 2.2 `tools/round-44/c1-run.sh` (+ `c1-run.py`) — **used; keep**

- `c1-run.sh` is exercised by
  `.ufo/waves/round-44/w1/artifacts/R44C1Run/verification-receipt.json` (V2 dry-run, V3 default
  scratch, V4 evidence-mode, V5 guard-without-data-run → exit 2) and is named by the frozen claim
  as the data procedure (`plans/round-44-claims.md:160-162`). It is also an entry of the counter's
  `FROZEN_PATHS` (`c1-counter.py:275`), so touching it is an immediate exit 2.
- The after-receipts prove `c1-run.py` actually ran: their scratch dirs are named
  `c1-run.<id>.1342995`, the exact pattern built at `c1-run.py:334`.
- **Recommendation: keep.** The `.sh`/`.py` split is a thin PATH-pinning wrapper, not a second
  authority. (Note: `c1-run.py` is not in `FROZEN_PATHS` but is covered by the directory prefix —
  a harmless duplicated freeze declaration.)

### 2.3 `tools/round-44/c2-rubric.json` (680,016 B) — **not dead by count, dead by duplication**

- Is every entry evaluated? **Yes, 80 of 80.** `entries` length 80, `dropped` length 10 (rows, not
  entries); my R2 run reports `entries_evaluated 80`, `mismatches 0`, exit 0; the committed score's
  80 per-entry records are all `match: true`, `reads_subject: true`,
  `match_reason: "equal"`, `exit_code: 0`. The "680 KB for how many rows?" suspicion is
  **falsified**: all 80 rows do work.
- Where the weight is: `entries[].command` = **540,909 B (79.5 % of the file)**. Every command is
  an inline `python3 -c` program; the 4,324-byte prelude (helpers `show`/`exists`/`correction`, …)
  is byte-identical across all 80 → **345,920 B (50.9 % of the file) is one prelude copied 80
  times**; the unique remainder is 155,498 B. (The counter's own header already sketches the fix:
  `c2-counter.py:66` shows the intended shape `["python3","-I","-B","tools/round-44/c2-checks.py",
  "<kind>"]` — but no `c2-checks.py` exists; the shipped rubric inlines the programs instead.)
- Amplification: the counter echoes every entry (including `command`) into its score JSON. At the
  first count the round held **27 tracked JSON files ≥ 400 KB** re-embedding `entries[].command`
  = **13,685,201 B of re-stored command text** (largest 780,208 B; 9 of the 27 were wave-2 seat
  outputs written while this scan ran). Re-counted when the artifacts were emitted minutes later:
  **41 files, 22,503,905 B** — the figure grows with every re-score, which is the point. Round-44's
  own tracked bytes:
  `tools/round-44` 2,626,064 (47 files) + `.ufo/waves/round-44` 17,648,098 (651) +
  `corpus/evidence/round-44` 3,424,841 (126) = **23,699,003 B**.
- Risk of deleting/refactoring now: frozen directory; any byte change → exit 2.
- **Recommendation: no edit this round.** Round 45: move the prelude into one
  `tools/round-45/c2-checks.py` (or `<round>/c2-checks.py`) and let each entry carry
  `{kind, params}`; have the counter store `argv_digests` (it already does) instead of the command
  text in the receipt. Expected saving ≈ 345,920 B in the rubric and ≈ 13.7–22.5 MB across receipts
  (first count vs artifact snapshot; it grows per re-score),
  without weakening a single check.

### 2.4 `tools/round-44/control-fixtures/` (38 files, 1,420,988 B) — **98.5 % duplicated elsewhere; frozen; keep**

Measured with `git hash-object --no-filters` against the `HEAD` blob map:

| subdir | bytes | what it is | external byte-identical copy |
|---|---|---|---|
| `c1/` | 1,060,803 | 4 after.json planted for CTL-C1-1 | **exactly** `corpus/evidence/round-42/c1/{DW-FONERA,DW-MEGA,OW-A8092,OW-X86FS}/after.json` |
| `pos/` | 227,260 | CTL-C1-POS landing tree | `.ufo/waves/round-44/controls/pos/tree/**` and `.ufo/waves/round-44/w1/artifacts/R44C1Controls/controls/pos/tree/**` |
| `c5/` | 55,576 | 12 mutated 4 KiB superblocks | `.ufo/waves/round-44/controls/c5/tree/**` (and the wave-1 copy) |
| `c4/` | 48,601 | prior-round envelopes planted | same pattern |
| `c2/` | 17,470 | fabricated oracle-only envelopes | same pattern |
| `c3/` | 11,278 | sasquatch-absent capture | `corpus/evidence/round-44/controls/c3/tree/**` |

- 32 of the 38 unique blobs also exist at another committed path; **1,399,776 B (98.5 %)** of the
  tree is byte-identical to a blob committed outside it. Only the six per-control `manifest.json`
  files (20,180 B total) are unique.
- The reader is real, so this is **not** unused weight: `c1-controls.py:88` `FIXTURES =
  'tools/round-44/control-fixtures'`. CTL-C1-1…4 and CTL-C1-POS consume these bytes.
- `pos/` is **not** "duplicated corpus files" as the seat brief hypothesised: none of its files is
  byte-identical to the lane's current `PROVINCE.md`/`corpus/README.md`/entry. It is a synthetic
  landing tree = base blob + append: `pos/PROVINCE.md` is 55,426 B vs the 53,354-B base blob
  (**+2,072 B**), `pos/corpus/README.md` is 85,484 B vs 84,621 B (**+863 B**), and the 20,280-B
  entry is byte-identical to `.ufo/waves/round-44/w1/artifacts/R44EntryDraft/…`.
- Risk of deleting: frozen directory; and deleting an input makes CTL-C1-1…5/POS unrunnable.
- **Recommendation: keep this round.** Round 45: (a) CTL-C1-1 reads the four round-42 receipts
  from their committed paths and ships only a `{path, sha256}` manifest; (b) the other controls
  read their inputs from the already-committed `controls/<id>/tree/**` copies; (c) `pos/` ships
  append deltas, not whole files. Expected saving ≈ 1.4 MB of checkout weight (git stores each
  identical blob once, so pack size shrinks only for the 6 unique manifests — the real cost is
  three diverging checkouts of the same bytes).

### 2.5 Wave-artifact tool copies — **byte-identical duplicates; not frozen; propose round-45 removal**

`.ufo/waves/round-44/w1/artifacts/R44C1Oracle/c1-oracle.py` and
`.ufo/waves/round-44/w1/artifacts/R44C1Run/{c1-run.py,c1-run.sh}` are **byte-identical** to the
shipped tools (`sha256 455c8a55…1336`, `55e2692a…061a7`, `c35d4b9b…0b263`), 106,536 B total. They
were the seats' deliverables that the L1 installed; once installed identically they are a second
copy that can drift. Not under any frozen family, so a round-45 cleanup may replace them with the
three digest lines that `R44C1Run/verification-receipt.json` already contains.
**Recommendation: do not delete mid-round** (wave evidence is cited by `R44W2C1Oracle` /
`R44C1Run` reports); round 45 collapse to digests.

### 2.6 The two 754 KB `c2-score-9d3d.json` files — **one measurement stored twice**

`corpus/evidence/round-44/c2/c2-score-9d3d.json` (753,998 B, added `75a5cb42`) and
`corpus/evidence/round-44/c1/c2-score-9d3d.json` (754,008 B, added by `c86ea508` — the M44-2
commit). Top-level keys are identical and every top-level value is equal except `wall_seconds`
(`4.227988` vs `4.439709`); all 80 entry records differ only in per-run metadata. No `*.md` in the
round cites the `c1/` copy except `w2/R44W2RevAttempt1.md:204`, which identifies it as attempt 1's.
It is a C2 score filed under the C1 evidence directory. **Recommendation:** the `c2/` copy is the
record; round 45 may delete the `c1/` copy (or move it under an `attempt-1/` prefix), saving 754 KB
of checkout and removing a second authority for one verdict.

### 2.7 Lane-root strays — **explainable; historical provenance; keep**

| path | bytes | why it is there | cite |
|---|---|---|---|
| `glibc-tag-object.json` | 26,073 | M34-5 misroot capture (fleet→lane byte-exact copy) | `corpus/lessons/round-34.md:19`; `prep/R34SourceNovelty.md:55` (path cited; `prep/` is **not present** in this lane at the tip, so that cite cannot resolve — see §4) |
| `unblob.log` | 2,652 | M38-7 misroot: unblob writes `./unblob.log` in its cwd | `corpus/lessons/round-38.md:38` |
| `kaidoku-r26/seats/EntryCorrection/final-report.md` | — | M26-7 misroot (fleet-root seat file moved into the lane) | `corpus/lessons/round-26.md:71`; `round-26-verifier-spotcheck.md:36` |

All three are tracked, all three are explicitly *historical* records of incidents, and each is
cited by path in its lesson. Provenance explicitly marked historical is never a deletion
candidate. **Recommendation: keep.** (If the lane wants a tidy root in round 45, move them under
`corpus/evidence/misroot/` **and** update the three lesson cites in the same commit — never one
without the other.)

### 2.8 Working-tree dead weight — **untracked, ignored**

`.ufo/waves/round-44/w1/artifacts/R44C1Counter/__pycache__/c1-counter.cpython-314.pyc` exists on
disk; `git ls-files | grep -c '__pycache__\|\.pyc$'` = **0**; `.gitignore:1:__pycache__/` covers it.
It never entered the record. **Recommendation:** checkout hygiene only (the wave's stakes are zero
here); not a repository deletion.

---

## 3. Contract verdicts (falsify / confirm)

### 3.1 R44-C1 — **confirmed**: 4/4 matched, `met_target false`, exit 1; the stop is the only reading

My R1 run: `carriers_matched 4`, `target 4`, `met_target false`, `exit_code 1`,
`frozen_path_changed []`, `bindings_false = ["province_core_section","province_core_row",
"frontier_note"]`, `failing []`. Per carrier (all four: v1le, v1be, v2le, v2be) `matched true`,
`run_provenance_ok true`, `evidence_id_ok true`, `oracle_hits_ok true`, `gaps_ok true`,
`projection_ok true`, `handler_ok true`. So the four REA receipts do publish every oracle file at
its exact path, no gaps, and the counter-time rerun projects equal. The claim fails on
documentation bindings only.

Why this is the only correct reading of the frozen text:

1. `plans/round-44-claims.md:34` (amendment 3, D1) — `parameters.output_directory` **must name a
   `corpus/evidence/round-44/c1/` path and the evidence id must be minted over that path**.
2. `plans/round-44-claims.md:137` (predicate) — `parameters.output_directory` **names this round's
   `/kaidoku-r44/` scratch segment**.
3. Every receipt carries `"output_directory": "/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Run/
   c1-run.<id>.1342995/rea-out"` (e.g. `corpus/evidence/round-44/c1/v1le/after.json:121`).

One JSON field cannot be both the committed evidence path and the scratch segment; a nested path
that contains both literal segments still fails amendment 3's second conjunct (the id is minted
over the scratch path, and `evidence_id_ok: true` proves it is). The two clauses are therefore
jointly unsatisfiable, and the round's stop is honest.

**The instrument was nonetheless satisfiable, and the record says so.** At `4cc1ac11` the same
frozen counter over the **same receipt bytes** (`git ls-tree` blob ids of
`corpus/evidence/round-44/c1/*/after.json` are byte-identical at `4cc1ac11`, `55bcce69` and the
tip) returned `met_target true`, `bindings_false []`, exit 0
(`corpus/evidence/round-44/c1/counter-at-4cc1.json`, `frozen_path_changed []`). The difference
between the two revisions is the **documents**: `PROVINCE.md:424` at `4cc1ac11` is
`## Round-44 additions to Core` with a promotion frontier note; at `55bcce69` it is
`## Round-44 measured, not promoted (R44-C1 honest stop)` and the frontier note no longer names
the stem. The counter never implements amendment 3: `c1-counter.py:258 PROV_SEGMENT =
'/kaidoku-r44/'` is checked at `c1-counter.py:1180`, and no code path inspects `output_directory`
for the committed path. The record discloses exactly this — `SCORECARD.md:3525` calls
`counter-at-4cc1.json` "the counter-met precursor", the lesson `R44-CL2` calls the text
"internally unsatisfiable on one field", and the entry's `status:` block says the run "does not
satisfy the frozen predicate". **No record defect here**; the residual risk is routed as R44-CL2
(a satisfiability preflight on the next freeze) and is the reason S-2/S-3 matter.

"No Core row is claimed" checks out: `PROVINCE.md:424-430` says measured-not-promoted,
`corpus/README.md:104` and `:224` say measured-not-promoted, the entry stem exists and its three
`source:` lines carry S138/S139/S112. `province_core_row false` is therefore correct, not a
counter false negative.

### 3.2 R44-C2 — **confirmed**: 80/80, `mismatches []`, exit 0; not vacuous

My R2 run: `entries_evaluated 80`, `mismatches_count 0`, `met_target true`, `exit_code 0`,
`frozen_path_changed []`; `counter_sha256 085192ea…36c277` equals the on-disk
`tools/round-44/c2-counter.py`; `rubric_sha256 = rubric_sha256_at_freeze = rubric_sha256_at_rev =
e8cc0ded…55e755e` equals the on-disk `tools/round-44/c2-rubric.json`, so the rubric was not
touched after the freeze.

Attacks and results:

- **Free pass / unevaluated rows** — none: 80/80 `match true`, 80/80 `reads_subject true`,
  80/80 `match_reason "equal"`, 80/80 check `exit_code 0`. No entry is skipped.
- **Vacuity (all rows pinned historically)** — false. `pin` distribution: `REV` 35,
  `HYAKU_FREEZE` 7, and 38 historical hex pins. 42 entries test the current/freeze tree; 38 test
  immutable historical pins. A vacuous rubric would have 80 historical pins.
- **Note-vs-value** — no entry's verdict rests on a `note`: the pass value is `observed`, compared
  `eq` to `asserted`, and `asserted` is required to be a substring of the base line whose sha256
  is pinned in `line_sha256`.
- **Dropped rows** — 10 rows carry `not-checkable-because` dispositions (D1–D10), but the counter
  never reads them (S-1). That is the one soft spot: the disposition discipline is prose, so a
  future rubric could drop a mismatching row and still exit 0.
- Limits: I did not audit the 80 inline programs line by line; free-pass risk is bounded by
  "each entry reads the subject it asserts" and by the wave-1 fitness witnesses
  (`mutation_witness`, 19,906 B) that I did not re-execute.

### 3.3 M44-2 / freeze defect — **confirmed and honestly recorded; the gate catches it**

- Both counters exit 2 at the tip: my R3 (c1) and R4 (c2) → exit 2, `frozen_path_changed`; the
  committed receipts agree (`.ufo/waves/round-44/l1/{c1,c2}-score-at-tip.json`).
- Only `c86ea508` touched `tools/round-44/` after the freeze:
  `git log --oneline c48f8a4b..main -- tools/round-44/` → one line. The preflight at `c86ea508`
  lists 8 `M` paths and 8 `blob_changed`, all under `control-fixtures/{c3,pos}`.
- The round's statement "measure at `55bcce69`, say so" is present in `SCORECARD.md:3521,3530`,
  `LOG.md:3203` and lesson M44-2, and `55bcce69` is a strict ancestor of the violating commit. The
  disclosure is honest. What it does **not** do is gate future commits — see S-2/S-3.
- Does `tools/round-45/frozen-path-preflight.py` really catch it? Yes for the graded incident and
  for the semantically hard cases, measured in fixtures (scratch; each repo `mktemp -d`, toplevel
  asserted): modify-in-frozen → 1 (1 touched, 1 blob); **add-in-frozen → 1 (1 touched, 0 blob —
  caught by the commit walk, not the backstop)**; delete-in-frozen → 1; change-outside-frozen
  with the matching pathspec → 0; tamper-then-restore → **1** with `blob_changed 0` (so a restore
  does not un-block, as the claim requires); no `--pathspec` → 1 with 557 `touched` (see S-2 in
  `w2/R44W2Preflight.md` D-2; I reproduce it as R8). One false-red class I did not see reported by
  peers is §4 S-2 (C2's own admissible edits).

---

## 4. Defects the L1 must act on

Each line carries the exact path, the command, its exit code and the observed value.

**S-1 — the rubric's dropped-row dispositions are not read by the counter.**
`grep -c "dropped" <LANE>/tools/round-44/c2-counter.py` → **exit 1, count 0**;
`grep -c "inventory" …` → **exit 1, count 0**. Observed: `c2-rubric.json` carries top-level
`dropped` (10 rows, 2,995 B) and `inventory` (2,439 B), and the counter loads only the
`ENTRY_LIST_KEYS` list (`c2-counter.py:150`, loop at `:343-357`). Consequence: claim rule
"no mismatching row may be dropped without an exact `not-checkable-because` disposition reviewed
before freeze" has no instrument; the list is documentation, so a dropped mismatch cannot red the
count. Peer `w2/R44W2ScoutDebt.md:34` (D-15) records the 10 rows but not that they are unread.
Action: none this round (frozen); add to the round-45 routed list.

**S-2 — the preflight false-reds C2's own admissible edits when given C2's declared frozen set.**
`python3 -I -B <LANE>/tools/round-45/frozen-path-preflight.py --root <LANE> --freeze
c48f8a4b… --rev 55bcce69c2f4854958d054bcab6d5f0c6fb8a6ac --pathspec SCORECARD.md
--json-out <S>/pf-55bc-scorecard.json` → **exit 1**, `verdict frozen_path_changed`,
`touched 1` (`SCORECARD.md`), `blob_changed 1`, while `tools/round-44/c2-counter.py` at the same
revision exits **0** (R2) because the claim declares SCORECARD/SHONEN/SKILL base-pinned with exact
`expected_edits`. Observed: R9 stdout sha `cfd07d85…1359`. Consequence: wiring the gate for C2 with
its own `frozen_paths` would block every legitimate C2 repair, including the three this round
landed. Action (round-45 wiring): either feed the gate the expected-edit allowance for
base-pinned files, or do not apply it to `SCORECARD.md`/`SHONEN.md`/`SKILL.md`. This is distinct
from peer `w2/R44W2Preflight.md` D-3 and `w2/R44W2C2Freeze.md` F-6, which cover the
claims-pathspec miss and the no-caller fact.

**S-3 — the lane is a jj repo, so the "wire it into the commit sequence" fix needs a jj-level
gate, not a git hook.**
`ls -d <LANE>/.jj` → **exit 0**; `jj --version` → **exit 0**, `jj 0.45.1-7c41cdeb…`. Observed:
`.jj/working_copy/tree_state` is present and `jj` is the working VCS; `grep -rn
"frozen-path-preflight"` finds only prose/receipts (no hook, no runner, no alias). A git
`pre-commit` hook will not fire for `jj commit`. Action (round 45): wire the preflight into the L1
commit recipe / a jj alias, with the exact per-claim pathspec list (see S-2).

**S-4 — the record cites a receipt that is not committed.**
`corpus/lessons/round-44.md:49` cites `.ufo/waves/round-44/l1/sources-census-end.txt`.
`git -C <LANE> ls-files --error-unmatch .ufo/waves/round-44/l1/sources-census-end.txt` → **exit 1**
(`did not match any file(s) known to git`); `git -C <LANE> status --porcelain` → `?? …/sources-
census-end.txt`. Observed: the cite resolves only in the L1's working tree, at no revision. Peer
`w2/artifacts/R44W2ConnSibling/R15-cited-receipt-tracked.txt` covers the same class. Action: commit
that file (with `selftest-c1-counter.txt` / `selftest-c2-counter.txt` /
`sources-census-start-replay.txt`, also untracked, if they are meant to be receipts) in the wave-2
landing commit.

**S-5 — the frozen oracle block has no builder-digest binding.**
`sha256sum <LANE>/tools/round-44/c1-oracle.py` → **exit 0**, `455c8a553a058c7fa01cc6930d30d5319b
7815c70c68854fac86834163981336`; `grep -c 455c8a55` in
`.ufo/waves/round-44/l1/c1-oracle-final-receipt.json` and
`corpus/evidence/round-44/oracle/manifest.json` → **exit 1, count 0**; the receipt has
`counter_sha256: null` and no `artifacts` field. Observed: the rows in `carriers.json` that the
counter calls the "independent oracle" cannot be tied to a tool version by digest, although the
sibling `R44C1Run/verification-receipt.json` already records `c1-run.sh`/`c1-run.py` digests.
Action: record the builder digest in the next round's receipt (no frozen byte changes now).

**S-6 — `c1-oracle.py` still ships a second pin authority.**
`grep -n "^CARRIERS = (" <LANE>/tools/round-44/c1-oracle.py` → **exit 0**, line **129**;
observed a hardcoded 4-carrier table (`v1-le`, `v1-be`, `v2-le`, `v2-be`, with fixture names and
sha256 pins) beside `tools/round-44/carriers.json`. Wave-1 `w1/R44Simplify.md` S2 flagged exactly
this fallback and it shipped unfixed. It is not read by any scoring path; a `--carriers`-less run
silently builds from the fallback. Action (round 45): delete the fallback, require `--carriers`.

---

## 5. Frozen-path statement (explicit)

**`tools/round-44/**` may not be touched this round.** It is a frozen directory pathspec for both
instruments (`c1-counter.py:286` `FROZEN_PREFIXES = ('tools/round-44/', …)`;
`c2-rubric.json` `frozen_dirs: ["tools/round-44"]`). Any add, edit, delete or rename under it
after `c48f8a4b` makes **both** counters exit 2 `frozen_path_changed` and destroys the only
admissible measured revision (`55bcce69`). Every deletion recommendation in §2 for that tree is
therefore a **round-45** action, after a new freeze. `corpus/evidence/round-44/oracle/` is frozen
for C1 by the same `FROZEN_PREFIXES`; `SCORECARD.md`/`SHONEN.md`/`SKILL.md` are base-pinned, not
byte-frozen (C2), and their exact expected edits are in the rubric's `expected_edits`.

## 6. Tradeoffs and unperformed work

- I did not delete anything, even where the weight is provable: every candidate is either under a
  frozen path, is a control input the claim's kill rule names, or is historical provenance. The
  cheapest real saving (≈ 13.7 MB of re-embedded command text at first count, 22.5 MB at the
  artifact snapshot) needs a rubric schema change, which
  is a freeze-time decision, not a wave-2 edit.
- I did not re-run the C1 control arms (`c1-controls.py`) or `c1-oracle.py --selftest`; their
  receipts are frozen evidence and out of this seat's falsification scope.
- I did not audit all 80 C2 inline programs line by line; the pass/fail mechanics, pins,
  subject-reads and byte bindings are verified, not the truth of each assertion.
- `prep/R34SourceNovelty.md:55` (cited by M34-5 for `glibc-tag-object.json`) does not exist in the
  lane at the tip — `ls -d prep` → **exit 2**. That is a pre-existing round-34 cite, not a
  round-44 defect; noted so the stray file's "explainable" status is qualified: the lesson cite
  resolves, the prep cite does not.
- The lane's shared tree was not modified by this seat. `git -C <LANE> status --porcelain` before
  writing showed only other seats' wave-2 outputs plus the L1's untracked receipts; after writing
  it shows the same set plus exactly `M`/`??` entries for this report and
  `artifacts/R44W2Simplifier/**`.

## 7. Scratch hygiene

Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2Simplifier` (counter `--work` dirs, fixture repos,
captured receipts) is deleted before yield; the parent `/fast/scratch/hyaku/kaidoku-r44` is left
in place for sibling seats. Receipt copies are committed in
`.ufo/waves/round-44/w2/artifacts/R44W2Simplifier/`: `counter-rechecks.json`,
`preflight-receipts.json`, `fixture-matrix.json`, `measurements.json`. No `/tmp` path is cited as
evidence anywhere in this report.
