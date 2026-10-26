# R39W2Separability — causal separability of R39-C1 and R39-C2 on landed bytes

**Verdict: CONFIRMED — neither frozen counter verifies because the other claim landed.** Eight
constructed states in a `--shared` clone score C1 6/6 exactly when C1's own receipts + Core landing
exist and C2 20/20 exactly when C2's own held-out set exists; removing the other claim's landing
changes nothing. Two bounded defects were found on the way (neither moves a claim verdict): the
frozen claims file's separability sentence names SOURCES rows that are **not** shared and omits the
premise that *is*, and all 20 held-out `run.json` records mis-state the executed REA argv.

Freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b`, author-measured rev
`6fdaf4f162aff156fcef0e52998a5469c64fd6f0`, lane HEAD when measured
`e40a25df3987d881513de581112d2dad30605673`. Counter invocations are byte-for-byte the frozen
commands (C1 with `--pkg65`, both with `--freeze <freeze>`); nothing in the lane, fleet or
`/home/vgpnk/Projects/shokuknow` was written, and no VCS state in the lane was mutated.

## 1. States I built (scratch clone only)

`S=/fast/scratch/hyaku/kaidoku-r39/R39W2Separability`; `git clone -q --shared <lane> "$S/clone"`,
`git status --porcelain` = 0, HEAD `e40a25df`. All state commits are local to the clone
(`states.txt` records every `--name-status`).

| state | rev | construction (relative to `e40a25df`) |
|---|---|---|
| A | `bfa22bf0015f…` | reverse of `6fdaf4f1` on its own 16 paths: delete `K1..K6/{after,run}.json`, the C1 knowledge entry, `PROVINCE.md`→freeze bytes, `SOURCES.md`→freeze bytes, remove the 3 C1 README lines (coverage row, knowledge row, `sasquatch-v4be` note). **C2 data untouched.** |
| B | `b85e076e38dc…` | `git rm -r corpus/evidence/round-39/c2` (101 files). **C1 untouched.** |
| C | `b4290e85c557…` | B applied on top of A (neither landing) |
| D | `2cfcf14325c6…` | A **plus** `git rm -r corpus/evidence/round-37/c1 corpus/evidence/round-39/c1` — C1 has no carriers, oracles or symlink tables left at all |
| E | `868fcf68ed3a…` | B plus `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` removed (C2's data *and* its backing entry gone, SKILL untouched) |
| F | `f21dcef302e3…` | both landings present; one marker line added inside `tools/round-39/c1-counter.py` (C1 frozen path touched) |
| G | `d4dd85dfa353…` | both landings present; one marker line added inside `tools/round-39/sqfs-triage.py` (C2 frozen path touched) |
| H | `3689abd36842…` | both landings present; one line appended to `plans/round-39-claims.md` (the **shared** frozen file) |

State A keeps `PROVINCE`'s and `SOURCES`' freeze bytes and drops the three README lines exactly;
the only side effect is that `52b0eb29`'s extension of the round-39 frontier note (a sentence about
R39-C1) also disappears with the section, which is inside the C1 landing block either way.
[INFERENCE] No other post-freeze commit touches `PROVINCE.md`/`corpus/SOURCES.md`/`corpus/README.md`
except `6fdaf4f1` (C1) and `52b0eb29` (one README lessons row + the note extension), verified with
`git diff 8fcda41c e40a25df -- <file>`.

## 2. Counter matrix

| state | C1 `c1-counter.py` | C2 `c2-counter.py` |
|---|---|---|
| freeze `8fcda41c` (control) | exit **1**, `carriers_matched 0`, `met_target false` | exit **2**, `no_manifest_at_rev` |
| HEAD `e40a25df` (both landed) | exit **0**, `carriers_matched 6`, `frozen_path_changed []` | exit **0**, `matched 20`, `bindings_false []`, `triage_table_identical true` (3086 B) |
| author rev `6fdaf4f1` (re-run) | exit **0**, 6/6, `[]` — agrees with `.ufo/waves/round-39/l1/scores/c1-at-6fdaf4f1.json` | exit **0**, 20/20, `[]` — agrees with `c2-at-6fdaf4f1.json` |
| **A** (C1 landing absent) | exit **1**, `carriers_matched 0` | exit **0**, `matched 20`, `bindings_false []` |
| **B** (C2 data absent) | exit **0**, `carriers_matched 6`, `[]` | exit **2**, `no_manifest_at_rev` |
| **C** (both absent) | exit **1**, 0 | exit **2**, `no_manifest_at_rev` |
| **D** (C1 carriers+receipts+landing absent) | exit **2**, `frozen_path_changed` (18 frozen carrier/oracle/symlink paths) | exit **0**, `matched 20` |
| **E** (C1 landed; C2 data+entry absent) | exit **0**, `carriers_matched 6` | exit **2**, `no_manifest_at_rev` |
| **F** (C1 frozen tool touched) | exit **2**, `frozen_path_changed ["tools/round-39/c1-counter.py"]` | exit **0**, `matched 20` |
| **G** (C2 frozen tool touched) | exit **0**, `carriers_matched 6` | exit **2**, `frozen_path_changed` |
| **H** (shared claims file touched) | exit **2**, `frozen_path_changed ["plans/round-39-claims.md"]` | exit **2**, `frozen_path_changed` |

What moves and what does not:

- **A** is the decisive counterexample to "C2 passes because C1 landed". With no C1 receipts, no
  Core row, no frontier note, no `S122`, no C1 entry and no README rows, C2 still scores 20/20 with
  every binding true and the SKILL block byte-identical (3086 B). C1 in the same state fails on
  exactly the landing: per carrier `carrier_present/carrier_pin_ok/oracle_ok/symlinks_ok` are all
  `true` (frozen inputs intact) while `receipt_present/receipt_fresh/evidence_id_ok` are `false`;
  the false boolean bindings are exactly `province_core_section, province_core_row, frontier_note,
  entry_present, sourced, coverage_map_row`, and the non-vacuity bindings `carriers_spec_ok,
  symlink_coverage, xz_leg` stay `true` in every state (they are properties of the frozen inputs,
  not of the landing).
- **B/E** are the decisive counterexample in the other direction: C1 6/6 with C2's held-out set,
  manifest and even the C2 knowledge entry absent.
- **D** goes further than the assignment: C1 loses its *carriers* and becomes unevaluable by its own
  freeze rule, and C2 is still 20/20. The two claims do not share a single byte of carrier, oracle,
  symlink table or envelope.
- **F/G** show verdicts are separable even in the unevaluable class: a C1 freeze violation does not
  block C2 and vice versa. **H** is the one exception, and it is symmetric and intended.

## 3. Why this is causal, not coincidental

1. **Landing order already forbids the forward hypothesis.** `3c07eed7` (C2 held-out, parent
   `72359309`) is the *parent* of `6fdaf4f1` (C1 receipts). Every committed C2 envelope existed
   before any round-39 C1 receipt existed, so C1's landing cannot have fed C2's data. The reverse
   ordering argument does not apply, which is why state B/E carry the weight there.
2. **Zero byte overlap** (`crosscheck.txt` §1): six C1 pins `K1..K6`; 20 distinct C2 manifest pins;
   pin-set intersection **EMPTY**; no `H*/carrier.sqsh` hashes to a C1 pin; 0 of the 101 held-out
   files are byte-identical to any round-38 C1 file; the 20 held-out subject digests share nothing
   with the round-38 C1 subject digests.
3. **Zero textual cross-references** (`crosscheck.txt` §2): 0 files under
   `corpus/evidence/round-39/c2/` mention `round-39/c1` or `round-37/c1`; 0 files under
   `corpus/evidence/round-39/c1/` mention `round-39/c2`, `heldout` or `triage`; `c1-counter.py` has
   0 references to `round-39/c2|sqfs-triage|heldout` and **0 references to `SKILL`**;
   `c2-counter.py` and `heldout-gen.py` have 0 references to `round-39/c1|round-37/c1`.

## 4. Shared-input audit of the three named surfaces

**SOURCES.** Row-level first-add (`git log -S'| Snnn |'`, fixed string):
`S118, S119, S120, S121` → `8fcda41c` (the freeze); `S122` → `6fdaf4f1` (the C1 landing).
Used-by (cell 10): `S118–S121` → `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`;
`S122` → `corpus/knowledge/2026-10-26-r39-be-squashfs-v4-core.md`. Entry citations are disjoint:
the C1 entry carries exactly one `source:` line (`S122`); the C2 entry carries `S112, S118, S119,
S120, S121`. `c1-counter.py` requires only a row whose used-by names the C1 entry (`S122`), and
`c2-counter.py` reads `corpus/SOURCES.md` **not at all**. → **not shared**.

**README.** The three C1 lines landed in `6fdaf4f1`; C2's coverage-map row and knowledge-index row
already exist at the freeze. `c1-counter.py` reads only the `## Coverage map` section for the entry
stem; `c2-counter.py` reads no README. → **not shared**.

**SKILL.** `c1-counter.py` has no SKILL reference (count 0). The only SKILL read is C2's: the
`## Queue-drain craft` block after `<!-- sqfs-triage-table v1 -->`. `52b0eb29` edited SKILL.md
(the `### Round-35/37/38/39 instrument registry`) *outside* the block; at HEAD the block is still
3086 bytes and `triage_table_identical true`, so C2 still scores 20/20 — the block-scoped freeze
regime absorbs the later edit as designed. → **not shared**.

**The one real shared input** is `plans/round-39-claims.md`, which both counters freeze-drift on.
State H: one appended line blocks **both** with exit 2. That is symmetric, intended by the freeze
rule, and cannot make one claim pass — but it does mean the two claims share a single point of
failure for admissibility.

## 5. The coupling the claims file does not name: a shared premise, not a shared input

The counters are separable; the *evidence* is correlated. Both claims rest on one unblob 26.6.4
behaviour — extraction-root containment decides remove-vs-keep:

- C1 states the rule before data and its receipts must show exactly one `unpublished-entry` gap per
  in-tree link and no path for an escaping link; the entry's only source is `S122` (`is_safe_path`).
- C2's `escaping-symlink-removed` / `in-tree-symlink-metadata` rows cite `S118` (`fix_symlink`,
  `MaliciousSymlinkRemoved`), and 4 of its 20 held-out carriers are those two classes.

A systematically wrong reading of containment (the `w1/R39C1SymlinkK1K4.md` "POSIX join clamps `..`"
draft, lesson M39-6) would move both claims in the same direction. They also share the host
toolchain: `sasquatch-v4be` 4.5.1 and unblob 26.6.4 on the child PATH (`S121`/`S112`) underwrite C1's
receipts and C2's dependency/`-be` classes. So this round holds **two separable measurements of one
premise**, not two independent confirmations of it. [INFERENCE] The premise itself is supported
twice from different files of the same program (`file_utils.py` vs `extractor.py`), which is weaker
than a second independent implementation.

## 6. Defects found (none moves a C1 or C2 verdict)

**D1 — the frozen claims' separability sentence is mis-stated (documentation, frozen bytes).**
`s/round-39-claims.md` says: *"The two share the SOURCES rows S118/S119 only as citations."*
Measured: C1 cites `S122` only and C2 cites `S112, S118–S121`; the row sets are **disjoint**, and
`S118/S119` are C2-only rows added at the freeze. The sentence at once claims a shared row that does
not exist and omits the shared premise of §5. Impact: a reader takes the round's separation to be
fuller than it is. Smallest safe correction: do **not** touch the frozen file; L1 records the errata
in `corpus/lessons/round-39.md` (wave-2 corrections) — source-row sets disjoint, the actual shared
dependency is unblob containment (`S122` vs `S118`) plus the host binaries, so C1 and C2 must not be
scored as two independent confirmations of the symlink rule.

**D2 — all 20 held-out `run.json` records mis-state the executed REA argv (evidence provenance).**
`tools/round-39/heldout-gen.py:408-409` executes
`['npx','-y',P_REA,'extract-firmware','--format','json','--full-output',carrier,outdir]`, but
`:416` records `[REA_PACKAGE,'extract-firmware'] + cmd[3:6] + [carrier,'$out']` = 
`rea-agents@6.5.0 extract-firmware extract-firmware --format json <carrier> $out` — the subcommand
is duplicated. `20 of 20` committed `corpus/evidence/round-39/c2/heldout/H*/run.json` carry the
duplicated token. The score is unaffected — `c2-counter.py` has 0 references to `run.json` or
`rea_argv` and scores from `envelope.json` — so this is a bad *provenance record*, exactly the class
the round's own freeze rule exists to prevent. Correction: `heldout-gen.py` is a frozen C2 path, so
no edit; treat `rea_argv` in those 20 files as a mis-render (the executed command is the one at
`:408`), state that in the lesson, and if the record is to be repaired it belongs to a new round's
tool with a new freeze — never to an in-place rewrite of committed evidence.

**D3 — the C2 interpreter's `--selftest` surface is neither separable nor portable (instrument
limit).** `tools/round-39/sqfs-triage.py:98-107` hard-codes `LANE` and points `SELFTEST_ENVELOPES`
at round-38 C1 receipts plus `SELFTEST_SKILL = LANE + '/SKILL.md'`, read at `:1023-1030`. The scored
path is clean — `c2-counter.py` materialises the interpreter and SKILL from git and invokes it with
`--skill <copy> <envelopes>` only, which is why my clone-only state runs are valid — but the frozen
claims' "C2 reads SKILL.md, its three tools, the writer and its own held-out evidence" does not hold
for the instrument's self-invocation, and a wave-2 seat cannot reproduce the 35-case selftest outside
the lane. Same file also embeds a second copy of the table (`TABLE_BLOCK`, used by `--print-table`
and as selftest skeletons) whose cells differ from the SKILL block — a duplicate authority that only
does not matter because the scoring path requires `--skill`. Correction: disclose in the instrument
registry/lesson; no edit to the frozen file. [INFERENCE] The 35 selftest cases that read the lane are
the ones that cannot be replayed in a clean clone.

**D4 — the cited wave-1 evidence surface is being mutated by concurrent wave-2 seats (observed, not
mine).** At measurement time the lane working tree showed
`git diff --stat HEAD -- .ufo/waves/round-39/w1` = 4 paths, 54 insertions / 18 deletions:
`R39C1IndepReader.md`, `R39C1SymlinkK1K4.md`, `.../R39C1SymlinkK1K4/symlink-tables.py`, and the
**deletion** of `.../R39C1SymlinkK1K4/evidence/carrier.sqsh` (365 B). No commit yet, so committed
bytes are intact. The frozen claims cite `.ufo/waves/round-39/w1/artifacts/R39C1Controls/` and w1
reports as kill-control evidence, and neither counter's frozen-path list covers `.ufo/waves/round-39/w1`,
so a commit of this drift would silently change cited evidence with no gate. Correction: wave-2
seats write new files under `w2/artifacts/`; L1 checks `git diff HEAD -- .ufo/waves/round-39/w1`
before committing and restores the deleted carrier (or lands a `w2/` errata file that quotes the
original bytes rather than rewriting them).

## 7. Impacted axes

- **coverage (R39-C1):** unmoved. 6/6 in every state where its own landing exists (B, E, G, HEAD,
  `6fdaf4f1`); never met without it. The score is attributable to C1's own receipts and Core row.
- **depth (R39-C2):** unmoved. 20/20 in every state where its own held-out set exists (A, D, F, HEAD,
  `6fdaf4f1`); unevaluable (`exit 2`) without it. The score is attributable to its own data.
- No frozen predicate, counter, carrier, oracle or table was changed; no lane write outside
  `.ufo/waves/round-39/w2/`.
- Residual risk carried by D1 (§5 correlated premise) and D2/D3 (evidence quality), not by the
  counters.

## 8. Limits of this seat

- This measures **counter-level separability on committed bytes**, not provenance. A fabricated
  receipt re-minted under the 6.5.0 rule (C1's disclosed `CTL-C1-3` limit) or a fabricated envelope
  would satisfy its own counter; separability says nothing about authenticity. Independent wave-2
  re-runs own that.
- My state commits exist only in a `--shared` scratch clone that I delete; `states.txt` and
  `commands.txt` reproduce them from the lane's own commits. The clone shares the lane's object
  store, so it can read every lane object; it wrote nothing back (the lane's
  `git rev-parse HEAD` is unchanged at `e40a25df` and my only untracked additions are under
  `.ufo/waves/round-39/w2/`).
- The freeze-ancestry checks mean a state that deletes frozen inputs (D) yields `exit 2` rather than
  `exit 1` for C1; that is the frozen rule working, not a claim result.

## 9. Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r39/R39W2Separability; mkdir -p "$S"; export TMPDIR="$S" HYAKU_SCRATCH=/fast/scratch/hyaku
git clone -q --shared /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$S/clone"
# build states A..H exactly as commands.txt / states.txt record, then for each rev:
python3 -I -B "$S/clone/tools/round-39/c1-counter.py" --root "$S/clone" --rev <REV> \
  --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <RECEIPT>
python3 -I -B "$S/clone/tools/round-39/c2-counter.py" --root "$S/clone" --rev <REV> \
  --freeze 8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b --json-out <RECEIPT>
```

Artifacts: `receipts/` (22 JSON counter receipts — one pair for each of the eight states, the two
freeze controls, and the two author-rev re-runs), `states.txt` (every state's rev, parent and `--name-status`), `commands.txt`
(exact commands, all exit codes, state recipes), `crosscheck.txt` (pin/hash/textual disjointness,
SOURCES first-adds and used-by, entry citations, SKILL block identity). Tooling: nothing installed
or upgraded for this seat (python3, node v24.21.0, the pinned rea-agents 6.5.0 npx cache used
read-only).
