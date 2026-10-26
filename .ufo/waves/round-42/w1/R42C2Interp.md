# R42C2Interp — SquashFS triage interpreter v4 (13-column grammar, A1 implemented, self-tested)

**Verdict: DONE.** `sqfs-triage-v4.py` parses the v4 block, implements every A1 clause as a
first-match row, refuses a v3 marker / duplicate label / undeclared action / dead handler
glob / 12-column header, and passes `--selftest` 123/123 with 20/20 single-point mutants
killed. One item of the assignment changed under me mid-wave (L1 grammar decision): the
handler domain is two columns (`handler` over F, `failing handler` over HF), not one
column matched against a computed candidate set — implemented as decided; the `## A1
delta` section records what moved.

Draft-attack sub-verdicts (evidence in §4): **CONFIRMED** A1 step 4 (dependency names on
real envelopes), step 2 (container), step 9 (residue); **FALSIFIED** two generator
assumptions (a repeated-byte tail is `padding`, not residue; a fixture file name does not
select the DD-WRT handler).

## 1. What was delivered

`artifacts/R42C2Interp/` (all paths relative to the lane):

| file | role |
|---|---|
| `sqfs-triage-v4.py` | the interpreter (2839 lines). Source of record for `tools/round-42/sqfs-triage-v4.py`; the L1 moves it. sha256 `497bab6766a0b0c6d6f36cb58cadc531bddf9dd3231f6100bf46cf6ff552a2e9`. |
| `probe-table-v4.md` | test input, **not** block 21: the A1 precedence transcribed one row per clause, 13 columns. |
| `controls-ctl-c2-0b.md` | CTL-C2-0b built for this grammar: the round-41 v3 rows transcribed into 13 columns (`*` in `failing handler`). |
| `measure.sh` | reproduction driver (selftest, probe parse, 12 real envelopes v3-vs-v4, 52 held-out pairs, 4 C1 receipts, base-SKILL refusal). |
| `mutants.py` | 20 single-point mutants; a mutant survives only if `--selftest` still exits 0. |
| `envelopes/` (12) | real `rea-agents@6.5.0` envelopes from unblob 26.6.4 fixtures (MIT). |
| `fixtures/` | the fixture bytes (MIT, ≤ 4 KiB) plus cut/damaged derivatives. |
| `README.md` | provenance, rebuild commands, envelope table, rerun instructions. |

## 2. Grammar as implemented (the binding definitions)

Refusals (exit 2, never a silent non-match): missing v4 marker; a v1/v2/**v3** marker in
the craft section with no v4 marker; wrong header (**including the 12-column v3 header**);
duplicate label; an action token not in the `<!-- sqfs-triage-actions: … -->` line; a
`cause` cell without `->`; a set cell with an empty/repeated/reserved member; a handler
cell that is not `*`/`none`/a glob, does not begin `squashfs`, or matches none of the ten
unblob 26.6.4 SquashFS handler names (`KNOWN_HANDLERS`: `squashfs_v1`, `_v2`,
`_v2_nonstandard`, `_v3`, `_v3_ddwrt`, `_v3_broadcom`, `_v3_nonstandard`, `_v4_le`,
`_v4_be`, `_v4_broadcom`). No match → `(unclassified, none)` (A1 step 15).

Columns (13, exact names): `label | operation | provider | handler | failing handler |
gap kinds | dependencies | -be in child argv | symlink removed | published files | action |
cause | source`.

Set cells: `gap kinds` and `dependencies` both take `*`, `none`, exact `a` / `a+b`, and
the contains form `a+` / `a,b+`. The `dependencies` contains form is new in v4 (A1 step 4
"holds"; v3 refused it, `R41W2C2InterpMut.md` §6 K6/K7).

Handler cells:

* `handler` globs over **F** = the `squashfs`-prefixed members of H (H =
  `chunks[].handler` ∪ `extraction_gaps[].handler`, nulls dropped). `none` = F is empty;
  `*` = any, emptiness included; a pattern needs at least one member of F to match.
* `failing handler` globs over **HF** = the `squashfs`-prefixed `handler` of every
  `extractor-failure` gap row; when no such row records one, **HF = F**. `*` matches an
  empty HF too (that is why every row outside A1 steps 6/7 carries `*`); `none` = HF empty.
* Consequences worth stating: after step 3, `handler: squashfs_*` is entailed (F ≠ ∅), so
  it is *not* a narrowing — it is how a row says "this clause is about a run that has a
  SquashFS chunk at all". `squashfs_v4_*` in `handler` **is** a narrowing, and it loses
  every legacy chunk (CTL-C2-9, §5).

Features (round-41 definitions, three deliberate tightening choices, all disclosed in the
module docstring and in §6):
`SR` = a `MaliciousSymlinkRemoved` `__typename__` on a `normalized_result.diagnostics[]`
entry or its nested `report`, **or** on any dict under `raw_result`; a substring in printed
stdout is not a report. `BE` counts only argvs whose basename starts `sasquatch`
(`command` / `argv` / `args` under diagnostics holders or `raw_result`), token `-be` is
never substring-matched. `P` = `len(normalized_result.files)`, exact, absent reads 0.

## 3. A1 steps → rows (expressibility check)

| A1 step | row cells (other than label/action/domain) | expressible because |
|---|---|---|
| 2 `F=∅ ∧ depth-limited∈G` | `handler none`, `gaps depth-limited+` | `none` tests F |
| 3 `F=∅` | `handler none`, `gaps *` | same |
| 4 dependency | `handler squashfs_*`, `gaps missing-extractor-dependency+`, `deps sasquatch-v4be+` then `sasquatch+` | dependencies contains form |
| 5 `extractor-failure ∧ P>0` | `handler squashfs_*`, `gaps extractor-failure+`, `files >0` | contains form |
| 6 `P=0 ∧ BE=no ∧ squashfs_v4_be∈HF` | `handler squashfs_*`, `failing handler squashfs_v4_be`, `be no`, `files 0` | second handler column |
| 7 `P=0 ∧ HF∩L≠∅` | `handler squashfs_*`, `failing handler squashfs_v[123]*`, `files 0` | second handler column + glob |
| 9 `unknown-chunk-handler∈G` | `handler squashfs_*`, `gaps unknown-chunk-handler+` | contains form |
| 10–14 | `gaps depth-limited+` / `unpublished-entry+` / `none` / `unpublished-entry` / `none` with `sr`/`files` cells | unchanged from v3 |
| 15 | no row matches | default pair |

Not expressible, and not needed by A1: a *negative* handler cell ("some v4 handler that is
not `squashfs_v4_be`"); a second disjoint condition set for one label (duplicate labels are
refused).

## 4. Attack of the draft — measured on real REA output

All envelopes are real `rea-agents@6.5.0` runs on unblob 26.6.4 fixtures (§7). Nothing here
is synthetic.

**4.1 A1 step 4 CONFIRMED on real envelopes.** With `$HOME/.local/bin` stripped from the
child PATH (`REA_UNBLOB_COMMAND` absolute), the dependency gap names exactly one binary:

| chunk handler (runtime) | `extraction_gaps[0].dependencies` | A1 branch |
|---|---|---|
| `squashfs_v3` (LE) | `["sasquatch"]` | `dep-missing-le` |
| `squashfs_v4_le` | `["sasquatch"]` | `dep-missing-le` |
| `squashfs_v4_be` | `["sasquatch-v4be"]` | `dep-missing-be` |

so A1's "every v1–v3 chunk of either byte order and every v4 LE chunk resolves plain
`sasquatch`" holds. Mechanism: `unblob/extractors/command.py:101-102`
(`Command.get_dependencies` returns `[self._executable]`, the resolved one), **not** the
handler's own `get_dependencies` (`handlers/filesystem/squashfs.py:64-66`, which lists
both binaries and is what a reader of that file alone would assume). Because D is a
singleton on real envelopes, exact `sasquatch` and contains `sasquatch+` agree there; the
contains form still matters for the round-41 K6/K7 superset shapes and for combos.

**4.2 A1 step 2 CONFIRMED.** `container.tar` (a v3 image inside a tar) at `--max-depth 1`:
`chunks ["tar"]` (so F=∅), `extraction_gaps [("depth-limited", null)]`, `files 1`
(`firmware.bin_extract/firmware.bin`). The v3 table reads `no-squashfs-chunk` /
`inspect-input`; A1's table reads `container-depth-limited` / `raise-depth`. Note for the
generator: the container envelope is **not** file-empty (P=1), so the row must not pin
`published files`.

**4.3 A1 step 9 CONFIRMED, and one generator trap FALSIFIED.** A v4-LE image followed by
128 random bytes gives `chunks [null, "squashfs_v4_le"]`,
`extraction_gaps [("unknown-chunk-handler", null)]`, `files` 5 including
`308-436.unknown` → `unknown-residue` / `isolate-residue` (v3: `unclassified`). But the
same image followed by **100 bytes of `0xAA`** yields `chunks ["padding", …]`, `gaps []`,
no residue gap: unblob's padding handler claims a uniform tail. A residue generator that
repeats one byte will produce a `padding` chunk and no `unknown-residue` class.

**4.4 Fixture trap measured.** `squashfs_v3/little_endian/__input__/squashfs_v3_le.bin` and
`squashfs_v3_ddwrt/little_endian/__input__/squashfs_v3_le.bin` are byte-identical (4096 B,
sha256 `0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7`), so the file
name in the DD-WRT directory does **not** select `squashfs_v3_ddwrt`; only
`…/squashfs_v3.le.nopad.bin` there (magic `68737174`) does. A1's "per handler means the
runtime handler name" is therefore not a formality.

**4.5 Legacy failure argv (feeds A1 step 7's rationale).** A damaged v3 body fails with
`report.command = "sasquatch -le -no-exit-code -f -d <out> <in>"`, `handler
"squashfs_v3"`, `files 0`, BE=`no`. Source: `handlers/filesystem/squashfs.py:40-54` —
`(Endian.BIG, _)` appends `-be`, `(Endian.LITTLE, _)` appends `-le`, `(Endian.BIG, 4)`
uses `sasquatch-v4be` and appends `-be` only for a non-AVM body. Two consequences: (i) a
legacy **BE** failure records `-be`, so BE is not a v4-only signal — A1 step 7 correctly has
no BE condition; (ii) a *standard* v4-BE failure also records `-be`, so it falls through
step 6 to step 8 (`body-extractor-failure`), which is what A1 says.

**4.6 A1's "unmoved" command.** On the base `SKILL.md` the v4 interpreter exits 2:
`line 434: refused marker '<!-- sqfs-triage-table v3 -->'; this interpreter reads only
'<!-- sqfs-triage-table v4 -->' …`. Measured, exit code 2.

## 5. Measurements (exact commands, exits, results)

Scratch: `/fast/scratch/hyaku/kaidoku-r42/R42C2Interp` (removed at exit; everything cited
is copied into the artifacts dir). Nothing installed this wave: python3 stdlib only, and
`npx -y rea-agents@6.5.0` ran the already-cached package. No pacman/uv transaction.

| # | command | exit | result |
|---|---|---|---|
| 1 | `python3 -I -B sqfs-triage-v4.py --selftest` | 0 | `SELFTEST cases=123 pass=123 fail=0` |
| 2 | `… --skill probe-table-v4.md --table-only` | 0 | 15 rules, 14 action tokens, handler-semantics line |
| 3 | `… --skill "$LANE/SKILL.md" --table-only` | 2 | refuses the v3 marker by name (A1's unmoved command) |
| 4 | 12 real envelopes, v4 probe table | 0 | legacy clean → `depth-limited`, legacy failure → `legacy-body-failure`, container → `container-depth-limited`, residue → `unknown-residue`, dependencies → `dep-missing-le/be`, no-chunk → `no-squashfs-chunk` |
| 5 | same 12 envelopes, base v3 interpreter + base `SKILL.md` | 0 | 8 of 12 differ: 7× `unclassified`, 1× `no-squashfs-chunk`; the 2 v4 dependency rows and the 2 truncated images agree |
| 6 | 52 round-41 held-out envelopes, v3 vs v4 | 0 / 0 | `holdout compared=52 identical=52` |
| 7 | 4 round-41 C1 carriers (`after.json`), v3 vs v4 | 0 / 0 | 4/4 identical (`depth-limited` / `raise-depth`) |
| 8 | CTL-C2-0b (13-column v3 transcription) on the 12 real envelopes | 0 | 7 `unclassified`, 3 `no-squashfs-chunk`, 2 correct → the control is do-nothing, as intended |
| 9 | CTL-C2-0b written **verbatim** (12 columns) under the v4 marker | 2 | header mismatch — a verbatim copy is not a control, it is a malformed table |
| 10 | CTL-C2-8 (A1 table minus the legacy row), real legacy failure | 0 | `body-extractor-failure` / `preserve-failure` |
| 11 | CTL-C2-9 (both handler columns at `squashfs_v4_*`), legacy clean | 0 | `unclassified` / `none` |
| 12 | CTL-C2-10 (A1 table minus container and residue rows) | 0 | container → `no-squashfs-chunk`, residue → `unclassified` |
| 13 | `python3 -I -B mutants.py --work "$TMPDIR"` | 0 | `MUTANTS total=20 killed=20 survived=0` |

Mutation axes covered (all killed): `none` semantics; column-4 tested against the wrong
set (both directions); `*` no longer matching an empty set; the handler glob vocabulary
check and the `squashfs` prefix check; H losing its gap-row source; HF losing its
`extractor-failure` filter; `dependencies` contains form; SR raw-result path; SR
diag-level holder; BE sasquatch filter; BE `argv` key; P collapsed to a boolean; rule
order reversed; the `files 0` guard; v3-marker refusal; duplicate-label check; action
vocabulary check; provider domain guard. First-mutation-failure case names are in the
sweep log; every kill came from `--selftest` (the held-out pairs kill nothing on their own,
matching round-41 `R41W2C2InterpMut.md` §7 — which is why the selftest is the load-bearing
oracle here and why it pins feature values, not just pairs).

## 6. What the freeze must pin so the evaluator can agree

The v4 predicate compares this interpreter's pair with `indep-eval-v4.py` on every
held-out envelope. The five round-41 shapes where the two round-41 tools disagreed
(`R41W2C2InterpMut.md` §6) are decided here as follows; either the evaluator adopts them,
or the generator must never emit such an envelope:

1. **SR source.** Diagnostics (`diagnostics[]` or its `report`) *and* `raw_result`
   `__typename__`; **not** a stdout substring (round-41 evaluator: stdout accepted →
   K8 disagreement).
2. **BE source.** Only argvs naming a `sasquatch*` binary; keys `command`/`argv`/`args`
   (round-41 evaluator: any argv → disagreement on a non-sasquatch `-be`).
3. **D semantics.** Membership by exact name (contains cell), never substring.
4. **HF.** The `extractor-failure` gap handlers only, restricted to `squashfs`-prefixed
   names, falling back to F. The restriction changes no decision (steps 6/7 compare
   against squashfs-prefixed sets) but keeps a malformed gap row from widening HF.
5. **P.** Exact count; the round-41 pair oracle could not see magnitude, so this selftest
   asserts it (`p-count-is-exact`).

For the counter (R41-CL1): `--json` emits, per envelope, `label`, `action`, `rule`, `row`
and `features` with keys `OP, PV, H, F, HF, G, D, BE, SR, P` (+ `commands`). The
held-out manifest should declare the same tuple under the single key `declared_features`
with exactly those names and the same value shapes (`H/F/HF/G/D` sorted lists, `P` int,
`BE/SR` `yes|no|n/a` / `yes|no`).

## 7. Limits and risks

* The interpreter cannot verify that the lane table pins `operation`/`provider` on every
  row; a `*` domain cell would let A1 step 1 fall through to a later clause. Carried from
  v3, documented in the module docstring.
* `KNOWN_HANDLERS` is pinned to unblob 26.6.4. A handler a later unblob adds is not
  nameable until the interpreter is extended — deliberate, not a wildcard.
* The 12-column v3 grammar is **refused**, so any round-41 table text pasted under the v4
  marker exits 2 (measured, row 9 of §5).
* Cell text is split on `|`; a literal pipe inside a cell is unsupported.
* A rule's `failing handler` glob is a set-intersection test, not equality; a row cannot
  say "HF is exactly {…}".
* One label per row; A1 needs no duplicated label.
* The interpreter reads no carrier, invokes no extractor, writes nothing; `--selftest`
  uses `tempfile.mkdtemp(dir=$TMPDIR)` and removes it.
* Real-envelope evidence covers gzip v3 (LE and BE), v3-DD-WRT LE, v4 LE, v4 BE, a tar
  container and a random-tail residue. **Not** measured on real output: v1/v2/v2-nonstandard
  handlers, v3-Broadcom, v3-nonstandard, `squashfs_v4_broadcom`, a real
  `unpublished-entry`/`MaliciousSymlinkRemoved` pair on a legacy chunk (A1 already states
  the legacy fixtures hold no links), and a partial legacy failure (P>0) — no recipe yet.
  The selftest covers those labels synthetically; the C2 held-out arm is where they must be
  produced for real.

## 8. Evidence index

Artifacts dir sha256 (`sha256sum *` inside it): `sqfs-triage-v4.py`
`497bab67…52a2e9`; `probe-table-v4.md` `e2f5f8fa…31ccd2da`; `measure.sh` `5634efe7…706183e`;
`mutants.py` `5bdb4598…4608fe268`; `controls-ctl-c2-0b.md` `0f59b363…c5cb190`; `README.md`
`10af3a63…8c80d2`. Per-envelope and per-fixture sha256 are in `README.md` (12 envelopes,
9 fixtures) together with the exact REA commands, the fetch URLs and the rebuild one-liners.
`artifacts/R42C2Interp/runlogs/` holds the raw transcripts behind §5: `measure4.log` (the
A1 / 13-column full driver run), `mutants5.log` (20/20), `selftest7.log` (123/123) and
`ctl0b13.tsv` (the CTL-C2-0b pairs).

No VCS mutation was performed (read-only `git show`/`rev-parse` only); nothing was written
outside `artifacts/R42C2Interp/` and this report.

## A1 delta

Mid-wave the L1 amended the precedence (A1) and then fixed the grammar; both landed after
my first implementation, which had:

* one `handler` column matched against a computed candidate set `HC = HF or F`;
* 12 columns; A1 steps numbered 1–13 (my selftest named `step5`/`step6` for AVM/body and
  had no container, residue or 15-step cases).

What changed, in order:

1. **A1 precedence (15 steps).** Every clause is now a row and every new decision is
   measured end-to-end: `container-depth-limited` (tar at `--max-depth 1`, §4.2),
   `legacy-body-failure` (damaged v3 body, §4.5), `unknown-residue` (random tail, §4.3),
   dependency-by-membership (§4.1). Selftest cases added per step: `container-*`,
   `residue-*` (6 shapes incl. residue after a partial/body failure and residue beating
   `depth-limited`), `ctl10-*`, `step6-*` (7 legacy handler names), `step7-*`
   (including `squashfs_v4_broadcom` → body), plus the 15-row `shape-*` sweep (18 checks).
   Action vocabulary gained `isolate-residue`; labels `container-depth-limited`,
   `unknown-residue`, `legacy-body-failure`. Selftest count 113 → 120.
2. **L1 grammar decision: 13 columns.** `failing handler` inserted after `handler`;
   `handler` globs over F, `failing handler` over HF (`*` matches an empty HF); steps 6/7
   carry `squashfs_*` in `handler` and the family glob in `failing handler`. Implemented
   by (a) adding the column to `HEADER`, the parser and `rule_matches` (two independent
   `match_glob` calls), (b) removing the `HC` feature (`--json` now prints F and HF
   separately), (c) retargeting every AVM row (12) and legacy row (10) in the selftest to
   the new cell, (d) making the header check refuse a 12-column document, (e) adding three
   cases that only the new column can satisfy: `failing-handler-column-separates-f-and-hf`
   (F={v4_be,v3}, HF={v3}: a `handler squashfs_v4_be` row must not fire), `star-matches-
   empty-hf`, `twelve-column-table-refused`. Probe table rewritten to 15 rows × 13
   columns. Selftest count 120 → 123; mutants re-anchored (M01–M04 now exercise the two
   columns) and 20/20 killed.
3. **Measurements re-run after both changes** (§5 rows 4–7): the 12 real-envelope labels,
   the 52 held-out pairs and the 4 C1 receipts are unchanged by the column split — the
   only label change in the whole wave came from A1 (container, residue, legacy), never
   from the grammar.
4. **Contract change the L1 must carry into block 21 and the controls:** CTL-C2-0b must be
   a 13-column transcription of the v3 rows (`*` in `failing handler`, §5 row 8); the
   verbatim 12-column block exits 2 (row 9) and would score as a malformed-table control,
   not a do-nothing control.
