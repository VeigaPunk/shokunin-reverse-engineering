# MutPlan — round 50 attempt 2, wave 3: pre-freeze mutation attack on both claims' instruments

**Verdict: PASS WITH ONE MATERIAL FINDING.** Both instruments survive the attack in
substance, but the C1 counter's freeze-drift arm has a **real coverage hole** (the
`R` status code is load-bearing and untested), and the C3 v5 instrument has one
**live table-vs-evaluator divergence that the selftest cannot see**. Neither is a
false alarm: both were confirmed by direct execution against the real bytes.

Everything below was measured on scratch copies only. **No REA run was made** (no
`npx rea-agents`, no `rea`); the only executables invoked were `python3`, `git`,
and `fnmatch`. The lane tree was never written except for this seat's own
`.ufo/waves/round-50/w3/MutPlan/` directory.

---

## 0. Scope note (a wave event the L1 must know about)

The C3 landing **landed mid-wave**, in this lane, while this seat was running:
`1439dfe9` (freeze+landing), `addbfb4d` (scored), `c3121c4f` (instrument
finalized). `SKILL.md` now carries **rule block 26** with
`<!-- sqfs-triage-table v5 -->` at line 550, and the instrument landed at
`tools/round-50-c3/sqfs-triage-v5.py`.

Two consequences this seat measured, both re-checked after the landing:

1. **The C1 freeze is intact.** All eight `FROZEN_PATHS` blobs are byte-identical
   between the C1 freeze `435d41fd` and `HEAD`
   (`git rev-parse 435d41fd:<path>` == `git rev-parse HEAD:<path>` for each), and
   `tools/round-50/c1-counter.py` is still `547c1ea05ca108d52b079bfcfa61e25e93ca3b8e`
   at both ends. The new instrument sits under `tools/round-50-c3/`, **not** under
   the frozen prefix family `tools/round-50/`, so the C1 `frozen_drift` prefix arm
   does not fire on it. Good: the C3 landing did not break the C1 freeze.
2. **The v4 interpreter is unaffected by the landing.** Re-running the unmodified
   v4 evaluator over the 126 held-out envelopes against the **post-landing**
   `SKILL.md` gives byte-identical output to the pre-landing baseline
   (`diff_lines=0` over the sorted 126-line label dump; both exit 0). The v4
   evaluator still finds `<!-- sqfs-triage-table v4 -->` at line 526 (the craft
   section holds v1..v5; the v4 marker is the one it reads, and the v5 block sits
   after it). So table v4 remains the routing surface for
   `tools/round-42/sqfs-triage-v4.py`, and rule block 26 is additive, not a
   replacement, for that instrument.

The claim file (`plans/round-50-attempt2-claims.md`) already says
`tools/round-50-c3/sqfs-triage-v5.py` and "rule block 26" (lines 23, 61-63,
76, 133); the paths and block number are as claimed. My task brief named
`tools/round-50/sqfs-triage-v5.py` and "rule block 22" — **the brief is stale**;
the claim file (the rule) says `round-50-c3` and block 26, and block 22 is
already the freeze-integrity block, which is why 26 was chosen. **No defect; the
brief's path and block number should not be used.**

3. **NEW: the landed rule-block ORDER in `SKILL.md` is out of sequence.** Before
   the landing the numbered craft blocks ran `22, 23, 24, 25` in document order
   (lines 548, 613, 633, 644). After the landing the craft section reads
   **`26` at line 548, then `22` (574), `23` (639), `24` (659), `25` (670)** —
   block 26 sits *between* the unnumbered v4 triage heading (line 458) and block
   22, so the section now reads `26, 22, 23, 24, 25`. Measured:

   ```
   before (1439dfe9~1):  548:22   613:23   633:24   644:25
   after  (HEAD):        548:26   574:22   639:23   659:24   670:25
   ```

   The block *number* (26) is the correct next-free number and matches the
   claim; only the **placement** is out of sequence. No instrument is affected
   (both the v4 and v5 interpreters locate their table by **marker**, not by
   block order — `parse_skill` finds `<!-- sqfs-triage-table v4 -->` /
   `<!-- sqfs-triage-table v5 -->` wherever it sits; measured §4 row "v4
   evaluator still reads table v4 after the landing", 126/126 labels
   unchanged). The impact is **reader-facing only**: a reader walking the
   craft blocks in document order meets `26` before `22`.
   *Suggested fix (one-line move, no content change):* relocate the block-26
   paragraph (lines 548-572) to **after** block 25 (i.e. after line 672) so the
   numbered blocks ascend; then re-run the v5 before/after counting command
   (the table bytes are unchanged, so `pair_mismatches` should stay 0, but the
   receipts name the revision, so they must be regenerated after the move).

---

## 1. Findings table — C1 counter (`tools/round-50/c1-counter.py`), 16 single-point mutations

Method: each mutation is one text substitution applied to a **copy** of the frozen
counter under the seat's scratch; the copy's own `--selftest` is run. KILLED =
selftest exit != 0 (the defect was caught). SURVIVED = exit 0.

Command for every row (run in a per-mutation scratch root holding
`tools/round-50/c1-counter.py` + `tools/round-27/xpin-attribute.mjs`):

```
python3 -I -B tools/round-50/c1-counter.py --selftest
```

Baseline (pristine, unmodified counter, same scratch layout):
`exit 0`, stdout sha256 `…`, `{"selftest": "c1-counter", "cases": 169,
"green_ok": 17, "red_ok": 152, …, "failures": []}` — 93 s wall.

| # | Mutation | Verdict | Exit | stdout sha256 (12) | What the selftest caught |
|---|---|---|---|---|---|
| 1 | `handler-name-compare`: `h == HANDLER` -> `h.startswith('squashfs_v4')` | KILLED | 1 | `c7226aef9fd6c075` | `chunk handler is the BE handler (squashfs_v4_be)` + `chunk handler is the bare prefix squashfs_v4` |
| 2 | `handler-constant-widened`: `HANDLER = 'squashfs_v4_le'` -> `'squashfs_v4'` | KILLED | 1 | `e11a1f3c161daa8e` | 3 root probes (`single chunk root`, `portion chunk root`, `portion chunk, shallow publish`) |
| 3 | `marker-equality`: `mkfs_time == bytes_used` -> `>=` | KILLED | 1 | `ce14579eff9608e1` | spec probe `standard-LE carrier` + `marker off by one` |
| 4 | `bytes-used-lower-bound`: `0 < bytes_used` -> `0 <= bytes_used` | **SURVIVED** | 0 | `9bd9fd283b1cd30e` | — |
| 5 | `target-constant`: `TARGET = 4` -> `3` | KILLED | 1 | `4c287f7c89a3830c` | spec probes `external carrier with a member_sha256` / `nested.sha256` / `oracle_root is a relative path` / `target frozen at 3` |
| 6 | `receipt-first-add`: drop `a != freeze` | KILLED | 1 | `a0a2bb08c6ab565d` | `receipt added at freeze` |
| 7 | `full-history-flag`: drop `--full-history` from `all_adds` | **SURVIVED** | 0 | `54df25883382520a` | — |
| 8 | `unblob-version-pin`: `ver != UNBLOB_VERSION` -> `not ver.startswith('26.')` | KILLED | 1 | `ada72e2af3d780c9` | spec probe `unblob that is not 26.6.4 is refused` |
| 9 | `evidence-id-recompute`: drop the `ev[key][0] == ev[key][1]` comparison | KILLED | 1 | `74f5713782318895` | `evidence id stale after an edit` |
| 10 | `projection-files-key`: drop `'files'` from `PROJECTION_KEYS` | KILLED | 1 | `15adc71c03f60deb` | `fabrication differing only in one published sha256` |
| 11 | `oracle-path-map-size`: drop `z == want_size` from the oracle hit test | KILLED | 1 | `47f8396f941d047e` | `a published file with the oracle sha256 but another size` |
| 12 | `parameters-prefix-test`: compare only `max_depth` | KILLED | 1 | `c4e17514720accde` | `receipt made under a smaller output budget than the frozen one` + `receipt without recorded parameters` |
| 13 | `sasquatch-presence-pin`: a missing `sasquatch` no longer refuses the rerun | KILLED | 1 | `c9ea6ca27e73f18d` | spec probe `sasquatch not on the child PATH` |
| 14 | `minor-version-clause`: `(major, minor) == (4, 0)` -> `major == 4` | KILLED | 1 | `cbc0d276db114940` | spec probe `squashfs 4.1 minor` |
| 15 | `score-receipt-shape`: drop `'exit_code'` from the score-receipt set | KILLED | 1 | `5a9eaa9d01677c65` | `a score receipt (exit_code) committed as the after-receipt` |
| 16 | `frozen-drift-rename-code`: `'MDRTU'` -> `'MDTU'` | **SURVIVED** | 0 | `0eae1f3660600342` | — |

**13 killed, 3 survived.** Every kill is on the intended clause (the failure text
names the case, not an unrelated crash) — receipts: `counter-mut-results-*.json`,
summary `counter-mut-summary.json`.

### 1.1 SURVIVORS — one is a real defect, two are masked or inert

**(a) `frozen-drift-rename-code` — REAL COVERAGE HOLE, and the mutant is
load-bearing.** The `R` (rename) status code in `frozen_drift` is removed from the
frozen-path walk, and the selftest still passes. I then ran the pristine and the
mutated `frozen_drift` on a purpose-built fixture: a path that is **frozen but
absent at the freeze** (an oracle table named by `carriers.json`, committed after
the freeze) and **renamed** afterwards.

```
pristine frozen_drift -> ['corpus/evidence/round-50/c1/g7581/oracle.tsv']   (drift DETECTED)
mutant   frozen_drift -> []                                                  (drift MISSED)
```

The mutant **loses a real freeze-drift detection**: the rename of a frozen path
that did not exist at the freeze is caught only by the status-code arm, because
the endpoint blob comparison skips a path that exists at neither end. The
selftest has no case that renames a frozen path.
*Suggested case:* a fixture where a frozen path **absent at the freeze** is added
after the freeze and then renamed (`git mv`) before the scored revision; the
counter must report it in `frozen_path_changed`.
*Second suggested case* (the cheaper one): a frozen path that **exists at the
freeze** is renamed; the blob arm catches that today (the path is gone at the
revision), so the status-code arm is the *only* witness in the absent-at-freeze
shape — the selftest should pin that shape specifically.

**(b) `full-history-flag` — INERT, not a hole.** Dropping `--full-history` from
`all_adds` survives, but the flag is **redundant given the `-m` already in the
same invocation**. I measured this on five merge topologies and on the git-log
manual's canonical TREESAME topology:

| topology | `-m --full-history` | `-m` alone | plain (no `-m`) |
|---|---|---|---|
| side-add only, then merge | 2 commits | 2 commits (identical sha) | 1 commit |
| side add + main re-add (same content) | 2 | 2 (identical sha) | 1 |
| side add + main re-add (other path) | 2 | 2 (identical sha) | 1 |
| side, two commits | 2 | 2 (identical sha) | 1 |
| **git-log manual: Q TREESAME to one parent** | Q + X | **Q + X (identical sha `6af94e05…`)** | X only |

`m_equals_m_full_history: true` in every case; only the bare form (no `-m`)
loses the side-branch commit. So `-m` alone already carries the round-50 S4
shortcut defence (the S4 critique names *both* flags; the `-m` is the
load-bearing half), and the `--full-history` token is documentation, not
behaviour.
*Suggested case (cheap):* assert the **pair** — the counter's receipt-add scan
must see a receipt added pre-freeze on a side branch and merged after the freeze.
That case already exists in the selftest (`a receipt added pre-freeze on a side
branch and re-added after the freeze, merged: not fresh`) and it is what kills
the *first*-add removal; what it does not pin is that `--full-history` is
load-bearing, because it is not. **Recommend the L1 drop the redundant flag and
amend the comment** ("`--full-history -m`" -> "`-m` (with `--full-history`
harmless)") rather than add a case.

**(c) `bytes-used-lower-bound` — masked, verdict-equivalent.** `0 < bytes_used`
-> `0 <= bytes_used` survives. Direct probe of `layout_probe` on a carrier with
`bytes_used == 0` and `mkfs_time == 0`:

```
pristine: ok=False  reason='bytes_used 0 outside 1..640'   bytes_used_sane=False
mutant:   ok=False  reason='inode_table_start 96 / directory_table_start 128 not inside bytes_used 0 in order'
```

`verdict_equal: true`, `reason_differs: true`. The mutant is **masked** by the
`tables_sane` clause (`0 < its < dts <= bytes_used` cannot hold when
`bytes_used == 0`), so the verdict never changes — only the diagnostic string.
*Suggested case:* a probe that pins the **reason text** for the `bytes_used == 0`
shape (the selftest already pins reason text for the marker/version/compression
shapes, so this is a one-line addition to `spec_probes`).

---

## 2. Findings table — the v4 TABLE vs the planned v5 precedence

Method: the **v4 table** in a scratch copy of `SKILL.md` is mutated; the
**unmodified** v4 evaluator (a scratch copy of `tools/round-42/sqfs-triage-v4.py`)
is run over the 126 committed round-42 recon envelopes
(`.ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/`). The label diff
against the baseline is the measurement.

Baseline (pristine `SKILL.md`, unmodified v4 evaluator): exit 0, 126 envelopes,
and the four `squashfs_v2_nonstandard_*_ddefault` rows read
**`clean` / `none`** — exactly the F2 defect the round-49 `W2Skill.md` recorded.

### 2.1 The four `v2ns *_ddefault` rows: the load-bearing defect is F2, not F1

**Measured on the committed corpus, the four `v2ns *_ddefault` rows are reached
through the `clean` row, not through `legacy-body-failure`.** Their gap set is
empty and their published-file count is > 0, so they match `clean` (gaps `none`,
files `>0`) and never reach the `legacy-body-failure` row (gaps `extractor-failure+`,
files `0`). The family census over the 126 envelopes:

| handler family | envelopes | gap sets seen | v4 label |
|---|---|---|---|
| `squashfs_v2_nonstandard` | 8 | `()` x4, `('depth-limited',)` x4 | `clean` x4 |
| `squashfs_v3_broadcom` | 14 | `()` x7, `('depth-limited',)` x7 | `clean` x7 |
| `squashfs_v3_nonstandard` | 16 | `()` x8, `('depth-limited',)` x8 | `clean` x8 |
| `squashfs_v3_ddwrt` | 14 | `()` x7, `('depth-limited',)` x6, `('extractor-failure',)` x1 | `clean` x7, `legacy-body-failure` x1 |

So **the 19 no-reader-family `clean` rows (4 + 7 + 8), not the four v2ns rows
alone, are what the v5 rule changes** on this corpus — the round-49 F2 note
counted the four v2ns rows because the reader census was fixture-level
(`v3_broadcom` 7/8 partial-reader) while the routing rule is handler-level. The
landed C3 receipts agree: `before 19 mismatches at base`, `after 0`. **The claim
and the landing are consistent with the corpus; only my task brief's phrasing
("the four v2ns `_ddefault` labels") undercounts the family.**

### 2.2 Table mutants and their label diffs (all measured)

| mutant | what it changes | corpus label diff | verdict |
|---|---|---|---|
| `A_legacy_narrow_bare_v123` | `legacy-body-failure` failing handler `squashfs_v[123]*` -> `squashfs_v[123]` | **1**: `dmg_Z3_v3ddwrt_inode_table` `legacy-body-failure`->`body-extractor-failure` | a **reader-backed cross-flip** (v3_ddwrt loses the cross-read row) |
| `B_legacy_narrow_v123_star` | control: keep the shipped wide glob | 0 | control |
| `B2_legacy_narrow_v12_star` | failing handler -> `squashfs_v[12]*` | 5: five `legacy-body-failure` -> `body-extractor-failure` | drops every v3 family, reader-backed and not |
| `C_clean_handler_narrowed` | `clean` row handler -> `squashfs_v[1345]*` | 9: eight `squashfs_v2` + one `dep_A2` `clean` -> `unclassified` | wrong: it drops reader-backed v2 and v3 clean runs to `unclassified` |
| `D_v5_shaped_minimal` | **the minimal v5-shaped table inside the v4 grammar**: two new rows above `clean` and above `legacy-body-failure`, the no-reader families selected by `squashfs_v[23]_[bn]*`, `record-unverified` + `preserve-unresolved` added to the vocabulary line | **19**, all `clean` -> `clean-unverified`, **all in the three no-reader families**, zero reader-backed cross-flip | **this is the minimal correct v4-table mutant** |
| `E_v5_shaped_plus_F1_narrow` | D plus the F1 narrowing (`squashfs_v[123]`) | **20**: D's 19 plus `dmg_Z3_v3ddwrt` -> `body-extractor-failure` | the F1 narrowing costs the reader-backed v3_ddwrt family |
| `F_clean_row_renamed` | rename the `clean` row's label | 51: every clean row in every family | a cross-flip across all ten families |
| `D2` (row-order variant) | the no-reader rows placed **above** `partial-body-failure`, plus a `no-reader-partial` row | 0 corpus diff; the synthetic no-reader partial probe flips `partial-body-failure`->`no-reader-partial` | an alternative shape; not required |

**The four `v2ns *_ddefault` labels do NOT flip under any F1-only mutation**
(`A`, `B`, `B2` all leave them at `clean`/`none`), because those rows are decided
by the `clean` row. They flip only under `C`/`D`/`D2`/`E`/`F`, i.e. only when the
`clean` row's routing or the label itself changes. **So the glob-widening (F1) is
NOT the load-bearing defect for the four v2ns `_ddefault` labels; F2 (the `clean`
row's action/label for a family with no oracle) is.** F1 is load-bearing for a
*different* shape — a no-reader family with an `extractor-failure` gap and zero
files — and **no committed envelope has that shape** (the corpus families above
show no no-reader row with an `extractor-failure` gap). I confirmed the shape
exists and is mis-routed with **synthetic** envelopes (below), and it is exactly
what the C3 instrument's `v2ns-failed` fixture carries.

### 2.3 Synthetic probe: F1 is real, and the v5 shape fixes it without a cross-flip

Synthetic envelopes (scratch only), evaluated by the **unmodified v4 evaluator**:

| shape | baseline v4 | mutant A (F1 narrowed) | mutant D (v5-shaped) |
|---|---|---|---|
| `squashfs_v2_nonstandard` failure, 0 files | `legacy-body-failure` / `cross-read-legacy` | `body-extractor-failure` / `preserve-failure` | **`no-reader-failure` / `preserve-unresolved`** |
| `squashfs_v3_broadcom` failure, 0 files | `legacy-body-failure` / `cross-read-legacy` | `body-extractor-failure` / `preserve-failure` | **`no-reader-failure` / `preserve-unresolved`** |
| `squashfs_v3_nonstandard` failure, 0 files | `legacy-body-failure` / `cross-read-legacy` | `body-extractor-failure` / `preserve-failure` | **`no-reader-failure` / `preserve-unresolved`** |
| `squashfs_v3_ddwrt` failure, 0 files | `legacy-body-failure` / `cross-read-legacy` | `body-extractor-failure` / `preserve-failure` | `legacy-body-failure` / `cross-read-legacy` (**reader-backed, kept**) |
| `squashfs_v1` / `v2` / `v3` failure, 0 files | `legacy-body-failure` | `legacy-body-failure` | `legacy-body-failure` |
| `squashfs_v2_nonstandard` clean, 2 files | `clean` / `none` | `clean` / `none` | **`clean-unverified` / `record-unverified`** |
| `squashfs_v4_le` failure, 0 files | `body-extractor-failure` | `body-extractor-failure` | `body-extractor-failure` |

This is the decisive measurement of task 2: **the F1 glob-widening is the
load-bearing defect for the no-reader *failure* shape, and the minimal correct
fix is D** — two rows inserted in the v4 table grammar, the no-reader families
selected by one glob that matches exactly
{`squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`},
and **the `legacy-body-failure` row left untouched** (mutant A/E show that
narrowing it to `squashfs_v[123]` costs the reader-backed `squashfs_v3_ddwrt`
family its cross-read row).

**The glob `squashfs_v[23]_[bn]*` is exact**: it matches the three no-reader
names and excludes `squashfs_v3_ddwrt` (`_d` vs `_b`/`_n`), `squashfs_v3`, and
all `squashfs_v4_*`. It needs no grammar extension.

### 2.4 The reader-backed legacy set is NOT selectable by one v4-grammar glob

The claim's evaluator narrows `legacy-body-failure`'s failing-handler cell to the
reader-backed v1-v3 families. **Inside the v4 single-glob cell grammar that set
{`squashfs_v1`, `squashfs_v2`, `squashfs_v3`, `squashfs_v3_ddwrt`} is not
expressible as one glob.** Complete structural enumeration (5 847 candidates:
every `[*]C[*]` form with every single-char class over the suffix alphabet,
`?`, and star runs 0..3) returns **zero** globs selecting exactly that set,
because any glob matching the one-character suffix `1` can carry at most one
non-wildcard character before its trailing stars, and `3_ddwrt` vs `3_broadcom` /
`3_nonstandard` differ only *after* the `3_` — a single trailing `*` cannot
separate them. The v5 instrument therefore needs a **list-valued handler cell**
(`squashfs_v1,squashfs_v2,squashfs_v3,squashfs_v3_ddwrt`), which is exactly
the grammar delta the landed draft implements
(`_parse_handler_cell` accepts a comma-separated list; the v4 evaluator's
`_parse_handler_cell` does not). **The landed v5 instrument is right to extend
the grammar, and the v4 evaluator must keep refusing it** — the v4 table stays
parseable by the v4 evaluator, which is what preserves the v4 instrument.

### 2.5 Corpus coverage gap in the C3 held-out dir (measured, not inferred)

The 126-envelope corpus contains **no no-reader-family envelope with an
`extractor-failure` gap**, so the F1 half of the C3 rule is **not exercised by
the held-out dir at all** — the 19 mismatches are all F2 (`clean` ->
`clean-unverified`). The corpus cannot see F1. The landed instrument covers F1
with its own fixture (`v2ns-failed`), which is the right place for it, and its
`legacy-glob-widened` control flips exactly that fixture. **This is a coverage
fact the L1 should record, not a defect:** the C3 score of 19/19-then-0 measures
F2 on the corpus and F1 on the fixtures, and the two halves should not be
reported as one number.

---

## 3. Findings table — the landed C3 v5 instrument (`tools/round-50-c3/sqfs-triage-v5.py`)

The draft landed mid-wave, so I attacked it too (scratch copy only; sha256 of the
copy I attacked: `05df514ffff3ee07e1cc04d5a874986dd966a30873246c3cdb2591fdbe7198fd`).
Its own selftest at that copy: **exit 0, 18 cases, pass 18, fail 0**, stdout
sha256 `788945d22526e6567f1226da80468a4c89203ce29de68ce8147ac76e0bbcf441`.

11 single-point mutations; command for every row:
`python3 -I -B sqfs-triage-v5.py --selftest` (run in a per-mutation scratch root).

| # | Mutation | Verdict | Exit | stdout sha256 (12) | Caught by |
|---|---|---|---|---|---|
| 1 | no-reader set loses `squashfs_v3_broadcom` | KILLED | 1 | `ca0307aab33e` | fixture `v3bc-clean` |
| 2 | no-reader set loses `squashfs_v2_nonstandard` | KILLED | 1 | `4085b911d4b6` | fixtures `v2ns-clean-*`, `v2ns-failed` |
| 3 | reader-backed set loses `squashfs_v3_ddwrt` | KILLED | 1 | `ab8239513b92` | fixture `v3ddwrt-legacy` |
| 4 | the `no-reader-failure` row is renamed out of the way | KILLED | 1 | `75632256c7d9` | fixture `v2ns-failed` |
| 5 | `clean-unverified` published-files cell `>0` -> `*` | **SURVIVED** | 0 | `788945d22526` | — |
| 6 | `clean-unverified` symlink-removed cell `no` -> `*` | **SURVIVED** | 0 | `788945d22526` | — |
| 7 | evaluator's `_meets` becomes ALL-match instead of ANY-match | KILLED | 1 | `64e6fa5a8039` | fixture set |
| 8 | evaluator never returns `clean-unverified` | KILLED | 1 | `276e7ac219e4` | fixture set |
| 9 | evaluator never returns `no-reader-failure` | KILLED | 1 | `59ca56a27f17` | fixture `v2ns-failed` |
| 10 | evaluator sends every zero-file failure to `cross-read-legacy` | KILLED | 1 | `2cf61d962369` | fixture `v2ns-failed` |
| 11 | the table keeps the v4 wide failing-handler glob | KILLED | 1 | `b84ef9500487` | fixture `v2ns-failed` |

**9 killed, 2 survived.** The draft's own committed battery (7 table mutations)
plus my 4 evaluator-level mutations all die; the draft's selftest is a genuine
kill-surface, not a rubber stamp.

### 3.1 SURVIVOR `clean-unverified-row-files-cell-widened` — a REAL table/evaluator divergence

Widening the `clean-unverified` row's published-files cell from `>0` to `*`
survives the selftest **and** produces a **table-vs-evaluator disagreement** —
the exact thing the C3 predicate forbids (`table_labels == evaluator_labels`).
Measured on the draft's own table and evaluator, on a no-reader family with
**zero** published files and no gaps:

```
pristine            table: clean-empty / confirm-empty      evaluator: clean-empty / confirm-empty    agree
files-cell-widened  table: clean-unverified / record-unverified  evaluator: clean-empty / confirm-empty   DISAGREE
```

and the same disagreement for `squashfs_v3_broadcom` and `squashfs_v3_nonstandard`.
The 126 committed envelopes show **0** mismatches for this mutant
(`corpus_table_evaluator_mismatches: 0`) because **no committed envelope is a
no-reader family with zero published files and no gaps** — so neither the corpus
nor the selftest fixtures can see it. The draft's own docstring names this shape
as a stated limit ("a no-reader family whose tree is empty keeps v4's
`clean-empty`"), and the pristine draft honours it; the mutant breaks the
stated limit and the predicate without any red case.

*Suggested case:* a fixture `v2ns-empty` — a no-reader family, no gaps, **0**
published files — expecting `('clean-empty', 'confirm-empty')`. It costs one
fixture and pins the `>0` cell of the `clean-unverified` row, which is
currently unpinned.

### 3.2 SURVIVOR `clean-unverified-row-symlink-cell-widened` — equivalent mutant

Widening the `clean-unverified` row's symlink-removed cell `no` -> `*` survives,
but it is **behaviourally inert**: the v4 `escaping-symlink-removed` row
(gaps `none`, symlink removed `yes`) and `mixed-symlinks` both sit **above**
`clean-unverified`, so a no-reader run that removed a symlink still lands on
those rows. Measured: on `v2ns-symlink-removed` and
`v2ns-symlink-removed-unpublished`, the pristine and the mutant give identical
(table, evaluator) pairs, and the corpus shows 0 mismatches. **Equivalent mutant;
no case needed.** (It is still worth pinning the cell, because it is a load-bearing
column today only by row order — but that is a robustness note, not a gap.)

---

## 4. Cross-version / landing-consistency checks (all measured)

| check | command | result |
|---|---|---|
| C1 freeze intact after the C3 landing | `git rev-parse 435d41fd:<p>` vs `HEAD:<p>` for all 8 `FROZEN_PATHS` | **8/8 SAME**; the counter blob `547c1ea0…` at both ends |
| C1 freeze walk itself, at HEAD | `frozen_drift('435d41fd', HEAD, <carriers.json at the freeze>)` run from the frozen counter's own module | **`[]`** (no drift) at `HEAD = c67b741e8f6bd8d64adbdb15e059d47fde004c77`; `tools/round-50-c3/sqfs-triage-v5.py` is in neither `FROZEN_PATHS` nor the `tools/round-50/` prefix family |
| new instrument is outside the C1 frozen prefix family | `git rev-parse HEAD:tools/round-50-c3/sqfs-triage-v5.py` | `10f9df4b3655…`; under `tools/round-50-c3/`, **not** `tools/round-50/`, so the C1 prefix arm does not fire |
| v4 evaluator still reads table v4 after the landing | `python3 -I -B sqfs-triage-v4.py --skill <post-landing SKILL.md> <126 envelopes>` | exit 0; **126 labels byte-identical** to the pre-landing baseline (`diff_lines=0`) |
| v4 table still parseable by the v4 evaluator after the landing | same command, exit 0, 15 rules | the v5 block (line 550) sits after the v4 block (line 526) in the craft section; the v4 marker is what the v4 evaluator reads |
| claim path / block number | `grep -n sqfs-triage-v5 plans/round-50-attempt2-claims.md` | claim says `tools/round-50-c3/sqfs-triage-v5.py` and "rule block 26"; the landing matches. **My task brief's `tools/round-50/…` and "rule block 22" are stale** (block 22 is the freeze-integrity block). |
| registry row for the new instrument | `grep -n round-50-c3 SKILL.md` | one row at `SKILL.md:1800` |
| C3 before/after counts vs my measurement | `.ufo/waves/round-50/c3/c3-before.json`, `c3-after.json` | 19 before / 0 after — **matches my independent D-mutant count of 19** |

---

## 5. What the L1 should do with this (ordered by severity)

1. **C1 counter — add the rename case** (`frozen-drift-rename-code` survivor,
   §1.1a). A frozen path **absent at the freeze** and renamed afterwards escapes
   the mutant's freeze-drift walk; the pristine catches it. One fixture. This is
   the only finding that touches a frozen instrument's bytes.
2. **C3 v5 instrument — add the zero-file no-reader fixture**
   (`clean-unverified-row-files-cell-widened` survivor, §3.1). Without it the
   `clean-unverified` row's `>0` cell is unpinned and a widening mutant produces
   a table/evaluator disagreement the predicate forbids, invisibly to both the
   corpus and the selftest.
3. **C1 counter — amend the `--full-history` comment** (§1.1b). The flag is inert
   given `-m`; the S4 defence is carried by `-m`. Either drop the flag or say so
   in the comment. No new case can pin it.
4. **C1 counter — pin the `bytes_used == 0` reason text** (§1.1c). Verdict-equivalent
   today; one line in the existing `spec_probes` block pins the diagnostic.
5. **Record the F1/F2 split in the C3 receipt** (§2.5). The 19 corpus mismatches
   are all F2; F1 is covered only by the instrument's own fixture. Do not report
   "19" as if it measured both halves.
6. **Move the landed rule block 26 after block 25** (§0.3) so the craft section's
   numbered blocks ascend `22…26`. Content-neutral; regenerate the C3 receipts
   afterwards because they name the revision.
7. **The C3 landing's `v5` grammar delta (list-valued handler cell) is correct and
   necessary** (§2.4): the reader-backed legacy set is not expressible as one
   v4-grammar glob, and the v4 evaluator must keep refusing it.
8. **No REA run was needed or made** for any of this. Every measurement is
   offline and reproducible from the seat's artifacts.

---

## 6. Reproduction (scratch copies only; lane tree untouched)

Seat artifacts: `.ufo/waves/round-50/w3/MutPlan/`

| file | what it is |
|---|---|
| `mutate-counter.py` | the C1 mutation battery (16 mutations, scratch copies only) |
| `mutate-table.py` | the v4-table mutation battery (7 table mutants + baseline, v4 evaluator unmodified) |
| `mutate-v5.py` | the C3 v5 draft mutation battery (11 mutations, scratch copy only) |
| `synthetic-probe.py` | the synthetic envelope probe (F1 shapes the corpus lacks) |
| `survivor-probes.py`, `survivor-probes2.py`, `survivor-probes3.py` | the survivor characterisation probes (full-history topologies, rename drift, masking) |
| `v5-survivor-probe.py`, `v5-survivor-probe2.py` | the v5 survivor characterisation (table-vs-evaluator on purpose-built shapes) |
| `glob-reader-backed.py` | the complete glob-reachability enumeration (§2.4) |
| `final-checks.py` | the D2 row-order variant |
| `counter-mut-results-*.json`, `v5-mut-results.json`, `receipts.json` | the machine-readable receipts (command, exit, stdout sha256, UTC start, mutant sha256) |
| `table-mut-report.json`, `synthetic-report.json`, `survivor-probes*.json`, `v5-survivor-probe*.json`, `glob-*.json`, `full-history-decisive.json` | the raw measurements |

Scratch (removed before yield, after the receipts above were copied):
`/fast/scratch/hyaku/kaidoku-r50/w3-MutPlan`.

## 7. Limits of this seat

- No REA run, so every statement about REA behaviour is about the committed
  envelopes and the synthetic probes, never about a live provider.
- The 126-envelope corpus is the round-42 recon set; it is not fresh data, and
  §2.5 shows it cannot exercise the F1 shape at all.
- `full-history` inertness is measured on **git 2.56.0**; the `-m`/`--full-history`
  interaction is version-dependent in principle.
- The v5 draft I attacked was the copy at sha256 `05df514f…`; the instrument was
  still being edited by its owning seat during this wave, so a later byte may
  differ. The two survivors are reported against that copy.
- The glob-reachability enumeration in §2.4 is complete **for the v4 single-glob
  cell grammar** (every `[*]C[*]` form over the suffix alphabet); it says
  nothing about the v5 list-valued grammar, which can express the set directly.
