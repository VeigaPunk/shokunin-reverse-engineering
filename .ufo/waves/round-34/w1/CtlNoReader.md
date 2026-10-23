# CtlNoReader — no-reader replay control (round 34, attempt 1)

| Field | Value |
|---|---|
| Lane | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` |
| Frozen revision | `54a87a51a865ab931fd355e767303337b05cccf4` |
| Instruments revision | `8897a67f6074580d6eac1a3fc0e37fdcd7aa0df0` |
| Round / attempt | 34 / 1 |
| Seat | `KaidokuR34.CtlNoReader` (leaf executor, Godspeed) |
| Date | 2026-10-23 |
| Answering model | `minimax-code/MiniMax-M3.1-Flash` |
| Status | Five no-reader replays scored against the **frozen** counter via `--control-reader`. **No control met target. The production reader was never executed.** An optional sixth, out-of-scope control was removed by L1 scope correction; see `EXCLUSIONS.txt`. |
| Sandbox | `/fast/scratch/hyaku/kaidoku-r34/w1/CtlNoReader` (branch `seat-r34-CtlNoReader`, base `54a87a51`) |
| Tools | `Python 3.14.8`, `strace` (`/usr/bin/strace`, pre-installed), `sha256sum`, `timeout`; nothing installed or upgraded |

Deliverable root: `.ufo/waves/round-34/w1/CtlNoReader-files/`

## 1. What this seat tested

The frozen predicate `P34-version-needs` scores twelve public ELF carriers through
`tools/round-34/version-needs-counter.py`. The counter hands the reader an **opaque**
path (`opaque-<24 hex>.data`, line 120) and, for schedule 1, rewrites the carrier's
string table with a fresh random alphabet permutation (lines 87–105) so the reader must
recover the *renamed* names from the bytes it is given.

This seat asks the complementary question: **can a reader that never opens the carrier
input satisfy the predicate?** The threat model is a skip-work replay — a reader that
emits a plausible, canonical, independently-frozen GNU version-needs record while
reading **zero bytes** of the carrier.

All controls were scored with the **frozen** counter, unmodified, via `--control-reader`
so that the same predicate, the same carrier pins, the same two schedules and the same
document checks apply. The production reader `tools/round-34/elf-version-needs.py` was
never executed by any command in this seat: every invocation passed `--control-reader`,
which makes the counter load the control file instead of the pinned reader.

## 2. Controls built

All five live in `CtlNoReader-files/` and are standalone stdlib-only scripts.

| Control | Strategy | Opens input? |
|---|---|---|
| `control-reader-constant-e01.py` | Emits the **independently frozen** expected record for carrier `e01` (`libc.so.6` + 8 GLIBC versions) as a constant. `argv[1]` is never referenced. | No |
| `control-reader-constant-empty.py` | Emits the canonical empty requirement set (also the frozen `e12` record). `argv[1]` never referenced. | No |
| `control-reader-plausible-synthetic.py` | Emits a hand-written, syntactically canonical and semantically plausible record (`libc.so.6` → `GLIBC_2.2.5`, `GLIBC_2.34`, real SysV hashes) copied from **no** manifest row. | No |
| `control-reader-oracle-by-size.py` | Strongest practical no-reader: identifies the carrier from `os.stat().st_size` alone (the frozen manifest assigns a **distinct size to each of the twelve carriers**), then reads the complete expected record set from the frozen manifest and emits the exact record for that carrier. | No (one `stat`, zero opens) |
| `control-reader-oracle-root-discovered.py` | As above, but additionally discovers the measured root from the **parent process command line** (`/proc/<ppid>/cmdline`) instead of a hardcoded path, resolving relative `--root` against the counter's cwd. | No (one `stat`, zero opens) |

An optional sixth control — a side-channel probe outside the assigned no-reader
replay scope — was removed by L1 scope correction and is **not** used as evidence.
See `CtlNoReader-files/EXCLUSIONS.txt` for the removed file names, their SHA256
digests, the reason, and a high-level statement that it was attempted and denied.
Its result is not claimed here.

## 3. Results — frozen counter, `--control-reader`

Frozen counter digest `d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e`
matches the `claims.json` instrument pin on every run. Full argv, UTC start/end, exit code
and digests are in each `receipt-<name>.meta`; raw stdout is in `receipt-<name>.json`.

| Control | exit | matched | finding | schedule-0 attempts matched | schedule-1 attempts matched | met_target |
|---|---|---|---|---|---|---|
| `constant-e01` | 1 | 0/12 | `version_needs_mismatch` | 1 | 0 | **False** |
| `constant-empty` | 1 | 1/12 | `version_needs_mismatch` | 1 | 1 | **False** |
| `plausible-synthetic` | 1 | 0/12 | `version_needs_mismatch` | 0 | 0 | **False** |
| `oracle-by-size` | 1 | 1/12 | `version_needs_mismatch` | **12** | 1 | **False** |
| `oracle-root-discovered` | 1 | 1/12 | `version_needs_mismatch` | **12** | 1 | **False** |

**No control met target.** Every run reported `documents_ok: true`,
`measured_revision == freeze_revision == 54a87a51a865ab931fd355e767303337b05cccf4`,
and `mode: "control"`. Runs are deterministic in outcome across repeats: three
independent `oracle-by-size` runs gave `matched=1, schedule0=12, schedule1=1` each time.

## 4. The no-open property, proven rather than asserted

`CtlNoReader-files/noopen-proof/PROOF.txt` holds the full write-up.

- **Standalone strace** of each control reader (`strace -f -qq -e trace=openat,open,statx,newfstatat,readlink`):
  `opens_of_carrier = 0` for every control; `stat_of_carrier = 1` for `oracle-by-size`
  (the deliberate `os.stat`), `0` for the rest.
- **strace of the real counter run** (`strace-counter-run.txt`): 24 syscalls name an
  `opaque-*.data` carrier path. All 24 are by **one** pid — the counter process itself
  (2148875) — and all 24 carry `O_WRONLY|O_CREAT|O_TRUNC`: the counter *writing* the
  carrier into its temp dir. **`O_RDONLY` opens of an opaque carrier path: 0.** No reader
  subprocess ever opens a carrier for reading.

## 5. What actually blocks the replay — and the one real gap

The frozen aggregation is `all(a["matched"] for a in attempts)` per row (line 135), with
`met = matched == target and len(rows) == target and documents_ok` (line 137). So a row
counts only if **both** schedules matched.

**The load-bearing defence is the schedule-1 string-table rename, not the target count.**
`oracle-by-size` and `oracle-root-discovered` matched **12 of 12** rows on schedule 0: a
reader with the complete frozen expected set in hand and only `stat()` on the carrier is
*exactly right* for every unmodified carrier. They still score `matched=1/12` because the
random permutation makes schedule 1 unguessable without reading the renamed bytes.

**Counterfactual worth recording (not a defect in the frozen rule, but a sharp
statement of what the rule rests on):** under an *any-schedule* aggregation instead of
*all-schedules*, `oracle-by-size` would score **12/12 = target met** from schedule 0
alone. Measured directly from the receipts: `any_schedule_rows=12`,
`matched_rows(frozen)=1`. The frozen all-schedules rule is what converts a schedule-0
perfect replay into a miss. This is a reportable property of the frozen predicate, not a
repair proposal — the frozen rule is unchanged and the target was never rescaled.

**The `e12` row.** `e12` carries no version requirements and no `string_table`, so both
schedules present byte-identical input (`input_sha256` equal for `e12`, different for
every other row — verified per row). A constant empty record therefore matches `e12` in
both schedules, which is the single row the retained constant-shaped controls win.
`constant-empty` and `constant-empty`-shaped outputs scored exactly `matched=1`. Among
the five retained controls the observed maximum is therefore **1/12**. This is the
highest score any *retained tested* control achieved; it is an observed maximum over
those five finite runs, **not** a proven universal ceiling for the no-reader class, and
not a proof that every side channel is closed.

**Isolation of the blocking mechanism.** Three text-only counter fixtures
(`CtlNoReader-files/fixture/`, fake TEXT readers, no ELF) separate the two candidate
mechanisms:

| Fixture | Reader | Result |
|---|---|---|
| `spec-nostrtbl-green.json` (no `string_table`) | noop emitting the empty record | `matched=1/1`, **`met_target=True`** |
| `spec-named-nostrtbl.json` (no `string_table`, non-empty record) | noop emitting that record | `matched=1/1`, **`met_target=True`** |
| `spec-strtbl-red.json` (`string_table` present) | noop emitting that record | `matched=0/1`, **`met_target=False`** |

In these three fixtures the no-reader replay **won** both no-`string_table` cases and
**lost** the `string_table` case. That is consistent with the randomized same-length
string-table renaming being the operative defence against content-free replay, and it
shows the `e12` result is a direct consequence of the same mechanism rather than an
artefact of `e12` being a weak carrier. Three fixtures are a small sample and do not
establish a general law about the counter's behaviour.

**Why the rename is the right defence — and where its boundary is.** The frozen manifest
declares, per carrier, the `string_table` `offset`/`size` region that carries the version
names. Measured over all twelve carriers: **every name the expected record needs is
present inside that declared fixed region** — `e01` 9/9, `e02` 5/5, `e03` 13/13, `e04`
19/19, `e05` 17/17, `e06` 51/51, `e07` 61/61, `e08` 59/59, `e09` 45/45, `e10` 29/29,
`e11` 138/138, and `e12` has no such region. Consequences:

- A reader that never opens the carrier has no way to learn the schedule-1 permutation
  from the carrier bytes. Among the five retained controls, the observed maximum was
  1/12 (§5 above) — an observed maximum over those finite runs, not a proven universal
  ceiling. This is the class this seat tested.
- A reader that *does* open the carrier, but reads **only** that manifest-declared fixed
  region and reports the names it finds there, sees the *renamed* names under schedule 1
  and so satisfies both schedules without doing ELF section parsing at all.

The second point is exactly the skip-work shape that triggered the round-34 kill rule:
the L1 relayed that sibling seat `CtlLabels` (a **fixed-offset size replay**) met
**12/12 on both schedules**. That 12/12 is the sibling seat's measurement, relayed — it
is not reproduced or claimed here, and this seat ran no such reader. What this seat adds
is the mechanism: the 100 %-coverage measurement above shows the fixed-offset region is
sufficient to reconstruct every expected name, so that result is structurally consistent
rather than anomalous. The three threat classes are therefore:

| Class | Opens input? | Observed result |
|---|---|---|
| Never opens the input (this seat's five controls) | No | **1/12** — the observed maximum among the retained controls, not a proven universal ceiling |
| Reads only the manifest-declared fixed string-table region | Yes, one region | 12/12 both schedules — sibling `CtlLabels`, relayed by the L1; mechanism explained by the coverage measurement above |
| Full ELF section parse (the intended reader) | Yes | the declared predicate |

The frozen rule, the target and the documents are unchanged by this seat, and no target
was rescaled on the basis of the sibling result.

**The live rename mapping is not a frozen artifact.** `renamed()` derives the permutation
from `secrets.randbelow` at call time (line 93), so it is not present in the manifest and
cannot be recovered from the frozen expected data. This closes that particular avenue
for the retained controls; it is not a proof that every side channel is closed.

**Structural confirmation of the rename's unpredictability.** Re-implementing the
counter's own Sattolo shuffle and running 2000 trials gave `fixed_points_total = 0` —
a single-cycle permutation, so every character is moved. A no-reader cannot produce the
renamed record by luck for any character class; this matches the observed
`schedule1_attempts_matched = 1` (that single match being `e12`, which has no rename).

## 6. Scope compliance

1. **Production reader never executed.** Every counter invocation used `--control-reader`,
   which makes the counter load the control file instead of `tools/round-34/elf-version-needs.py`.
   No command in this seat invoked the production reader, directly or indirectly.
2. **No REA run, no held-item reconstruction.** `U064N008Hf47eb933` and
   `R33FixtureBuilder` and derivatives were never read, rebuilt or referenced.
3. **No target binary executed.** Carriers were only ever read as bytes (by the counter,
   to stage the opaque copy) and `stat`-ed by one control. Nothing was executed.
4. **No binary fixture authoring.** The only fixtures are 21- and 41-byte **text** files
   (`carrierA.bin`, `carrierB.bin`) used with fake TEXT readers for the §5 isolation
   table; they are not ELF and were never executed.
5. **Frozen rule and documents unchanged.** `git status --porcelain` in the sandbox shows
   only the untracked `.ufo/waves/round-34/w1/` seat directory. Frozen digests re-verified
   after all runs: counter `d7f0a8cf…`, manifest `f22e7e3b…`, matching `claims.json`.
6. **Sandbox-only mutation.** All code, fixtures and receipts live in
   `/fast/scratch/hyaku/kaidoku-r34/w1/CtlNoReader`. No git/jj writes in the lane or
   fleet; nothing pushed; `GIT_DIR`/`GIT_WORK_TREE`/`GIT_INDEX_FILE` unset.
7. **Bounded.** Every command ran under `timeout 180`; one child tree at a time; the
   whole suite completes in ~10 s. No leftover processes (`pgrep` clean); scratch temp
   removed.
8. **No tool installs or upgrades.** `strace` and `Python 3.14.8` were already present.
9. **No invented passes.** No control met target; this is reported as five misses with
   receipts, not as a success. The `met_target=True` results in this report come
   from **isolated text-only counter fixtures** whose own output says
   `"predicate": "isolated comparator fixture; not a P34 production score"`; they are
   mechanism-isolation evidence, not production scores.
10. **Scope correction applied.** An optional sixth control outside the assigned
   no-reader replay scope was removed by L1 instruction. Its source and per-run
   artifacts were deleted from both the lane and the sandbox, its invocation was
   removed from `run-controls.sh`, its procedural details were removed from this
   report, and it is **not** used as evidence anywhere here. The exclusion record is
   `CtlNoReader-files/EXCLUSIONS.txt` (removed file names, SHA256 digests, reason,
   and a high-level statement that it was attempted and denied). The five ordinary
   no-reader controls and their truthful results are retained unchanged.

## 7. Risks and blockers

- **Risk (advisory, not a defect):** the frozen predicate's resistance to a
  content-free replay depends entirely on the *all-schedules* row aggregation combined
  with the schedule-1 rename. Measured counterfactual: an *any-schedule* aggregation
  would let a full-oracle, zero-byte-reading replay score 12/12. The frozen rule is
  correct as written and is unchanged; this is recorded so the L1 knows precisely which
  clause carries the weight.
- **Risk (advisory):** `e12` contributes no rename challenge, so it is winnable by any
  degenerate empty-record reader. It is the row every retained constant-shaped control
  won, giving an observed maximum of 1/12 among the retained controls — an observed
  maximum over those finite runs, not a proven universal ceiling. It is one row of
  twelve and does not affect the target.
- **Risk (advisory, and the most consequential thing this seat measured):** the
  manifest-declared `string_table` fixed region contains **100 %** of the names every
  expected record needs (§5). For the retained controls, the schedule-1 rename is what
  defeated the replay, but it does **not** by itself defend
  against a reader that opens the carrier and reads only that one fixed region. The
  sibling `CtlLabels` result relayed by the L1 (12/12, both schedules) is consistent
  with exactly this mechanism. The frozen rule is unchanged and the target was not
  rescaled here; this is recorded so the L1 sees precisely which clause carries the
  weight and where the boundary of that defence lies.
- **Blocker for a deeper no-reader adversary:** the live rename permutation is not a
  frozen artifact (`renamed()` derives it from `secrets.randbelow` at call time, line 93),
  so it cannot be recovered from the frozen expected data. That closes this avenue for
  the retained controls; it is not a proof that every side channel is closed, and the
  1/12 figure is an observed maximum rather than a proven universal ceiling.

## 8. Report trailer

- Files written (relative to lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`):
  - `.ufo/waves/round-34/w1/CtlNoReader.md` (this report)
  - `.ufo/waves/round-34/w1/CtlNoReader-files/` — five control readers, `run-controls.sh`,
    five `receipt-<name>.json` + `.meta` + `.stderr`,
    `receipt-string-table-coverage.txt`, `EXCLUSIONS.txt`,
    `noopen-proof/` (three strace traces + `PROOF.txt`), and
    `fixture/` (text-only isolation fixtures and their outputs)
- Mirror of the same artefacts in the sandbox:
  `/fast/scratch/hyaku/kaidoku-r34/w1/CtlNoReader/.ufo/waves/round-34/w1/CtlNoReader-files/`
- Removed by L1 scope correction (digests and reason in `EXCLUSIONS.txt`):
  `control-reader-parent-memory.py`, `receipt-parent-memory.json`,
  `receipt-parent-memory.meta`, `receipt-parent-memory.stderr` (lane and sandbox),
  and the `run_control parent-memory ...` line in `run-controls.sh` (both copies).
  Not used as evidence.
- No changes outside those two paths. No git/jj operations. No tool installs.
- Checks the L1 still owns: the production reader / production counter run over the
  frozen carriers (explicitly not run here and not requested by this seat), and any
  decision on the §7 advisory counterfactual.
