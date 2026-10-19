# RV-7 seat report — arc3-loop1-round1, chain c2, role reviewer

Seat: RV-7 | chain c2 | role reviewer
Task: verify at HEAD — selftest 13/13 green, findings=0, `--rev deadbeef` exit 2,
`--rev HEAD` clean — run them myself after EX-16 lands. Verdict in this report.

## Verdict

**ALL FOUR NAMED CHECKS PASS on the settled landed artifact.** EX-16's guard is
present, correct on every attack I could construct, and byte-identical to an
independent reconstruction of PL-2's spec that I built before the landing.

Landed target (settled 07:16, stable across a 60 s sample; `git status` shows
both files modified, table untouched):

| file | sha256 |
|---|---|
| `.ufo/gates/citation-drift/citation-drift-probe.py` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` |
| `.ufo/gates/citation-drift/expected.json` | `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` |
| `.ufo/gates/citation-drift/pointer-table.json` | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` (unchanged) |

| # | check | result |
|---|---|---|
| N1 | `--selftest` | `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`, rc=0 |
| N2 | `--rev HEAD` | `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`, rc=0 |
| N2b | `--rev HEAD --strict` | `clean findings=0 exit=0`, rc=0 |
| N3 | `--rev deadbeef` | `could-not-evaluate findings=1 exit=2`, finding `revision_unresolvable`, rc=2 |
| N3b | `--rev deadbeef --strict` | `could-not-evaluate findings=1 exit=2`, rc=2 |

Raw output: `claims/c2/RV-7/named-checks-landed.log`.

## 1. Work performed (evidence pointers)

- Read the frozen claims/rules: `claims-frozen.md:40-54` (C2 claim), `:73-88`
  (seat discipline), `:90-104` (roster).
- **Pre-change baseline** at HEAD `e845c2b` — gate sha256 (`3067621a…` /
  `4e28ba90…` / `738b3a56…`), `expected.json` keys `['_doc','frozen_run',
  'snapshots','selftest']` with **no table digest anywhere**, selftest 11/11,
  `--rev HEAD` findings=0, `--rev deadbeef` exit 2: `claims/c2/RV-7/verify-pre.log`.
- **Own attack harness** (read-only over the repo; scratch under this seat's
  artifact dir): `claims/c2/RV-7/verify.py`, log `verify-post.log` (10 case
  families + a 26-run selftest sensitivity sweep); `claims/c2/RV-7/verify-extra.py`,
  log `verify-extra-post.log` (11 further attacks: byte-level reformat, unpinned
  expected, drift preservation, consistent re-pin, foreign CWD, symlinked table,
  single-finding preflight, honest custom table).
- **Pre-landing reconstruction of PL-2's spec** on scratch copies:
  `claims/c2/RV-7/reconstruct-pl2.py`, log `reconstruct-pl2.log`. Extracted PL-2's
  ```` ```diff ```` block, applied it with `patch -p1` (rc=0), applied PL-2's three
  `expected.json` edits, then ran the harnesses against it
  (`verify-reconstruction.log`, `verify-extra-reconstruction.log`).
- **Landed-vs-spec identity**: `diff` of both landed files against the
  reconstruction is empty; `sha256sum` agrees on both. The landed probe also
  equals PL-2's own claimed prototype hash `e2665074…` (`plan.md` §6).
- Read the chain's design record and the competing patch texts: `PL-2/plan.md`,
  `PL-2/frozen-run-guard.patch.md`, `EX-20/registry-row.patch.md` (v2),
  `SC-4/scratch/registry-row.diff`, `EX-21/selfinvocation.patch.md`,
  `EX-21/logs/proto-probe.diff`, `EX-23/harness/{guardA,guardB,guardC}.py` +
  `census-results.json` + `selftest-proof.log`, `EX-24/pin-mutability.md`,
  `RV-8/guard-compat-matrix.md`, peer reports `RV-6.md`, `RV-8.md`.
- **Mid-landing capture**: at 07:15:49 the real target hashed to
  `53a94df2628ddb1ca194a66cb5138d499ae465b086ea303917c01c1ef5ee43bd` and its
  selftest read `FAILED cases=13 passed=1 failed=12 exit=1`. Reproduced
  mechanically from the landed probe by reverting exactly PL-2's last hunk:
  `claims/c2/RV-7/reproduce-midlanding.py`, log `reproduce-midlanding.log`
  (derived sha == observed sha, same 1/13 result).
- Read EX-16's own after-measurements: `claims/c2/EX-16/after-sha256.txt`,
  `after-selftest-13.txt`, `after-selftest-reps.txt`, `git-status.txt` — all
  corroborate this seat's readings independently.
- Finding-id token audit across the landed probe and every registry-row patch
  text (exact-token regex, so `table_tampered` inside `pointer_table_tampered`
  does not count): landed probe emits `pointer_table_unpinned` (`:297`),
  `pointer_table_tampered` (`:306`), `pointer_table_unreadable`
  (`:292,:303,:312`); `table_tampered` occurs once (`:444`) as a **case name**.

## 2. Proposed changes

One artifact: `claims/c2/RV-7/proposed-registry-row-id-correction.patch.md` —
patch text only, **not applied**. It records that three c2 patch-text artifacts
(`SC-4/scratch/registry-row.diff:8` + its `patchtest` copy, `RV-6/patchtest/`
copy of the same text, `EX-21/selfinvocation.patch.md:61,100,112,144`) declare
the finding id `` `table_tampered` ``, which the landed probe **never emits**;
the correct text already exists as `EX-20/registry-row.patch.md` v2. Integrate
EX-20 v2, not SC-4's diff and not EX-21's row.

This seat wrote nothing else outside `claims/c2/RV-7/` and this report. No git
mutation was run; no LOG/SCORECARD/SKILL/corpus/prose file was touched.

## 3. Before→after measurement (C2 claim)

Same commands, same harness, pre (HEAD `e845c2b`) → post (landed):

| probe input | pre | post |
|---|---|---|
| `--selftest` | 11/11 CLEAN exit 0 | **13/13 CLEAN exit 0** |
| default run `--rev HEAD` | findings=0 exit 0 | findings=0 exit 0 (unchanged) |
| `--rev deadbeef` | exit 2 `revision_unresolvable` | exit 2 `revision_unresolvable` |
| **emptied table + real expected** | **rc 0, findings=0 — SILENT** | **rc 2 `pointer_table_tampered`** |
| weakened `must_match` table | **rc 0 — SILENT** | rc 2 `pointer_table_tampered` |
| one-byte table flip | rc 0 findings=1 "reported" | rc 2 `pointer_table_tampered` |
| tampered table in a copied gate dir | **rc 0 — SILENT** | rc 2 `pointer_table_tampered` |
| absent table | rc 2 `pointer_table_unreadable` | rc 2 (unchanged) |
| byte-identical table copy | rc 0 | rc 0 (preserved) |
| drift at an old rev | 26 findings, rc 0 probe / rc 1 strict | identical (preserved) |
| unpinned expected + emptied table | **rc 0 — SILENT** | rc 2 `pointer_table_unpinned` |
| selftest case-table mutation sweep | 11/11 assertions bite | 13/13 assertions bite |

Commands and verbatim output: `verify-pre.log` vs `verify-post.log`,
`verify-extra-pre.log` vs `verify-extra-post.log`. The four claim-specific
readings are in `named-checks-landed.log`.

## 4. Attacks / refutations attempted (verdicts)

1. **"The claim's hole was already closed"** — REFUTED, then confirmed closed.
   Pre-landing I measured an emptied table, a weakened table and a tampered table
   at a copied default path each reading `rc=0 findings=0` — a silent clean in
   both probe and `--strict` modes. Post-landing all four are exit 2. Note the
   claim's own framing is generous: an **absent** table already exited 2 before
   the guard, so the genuinely new coverage is the *tampered* class.
2. **"A custom `--table` is unchecked"** (the strongest pre-change bypass) —
   CONFIRMED pre, CLOSED post. The landed guard checks whatever table is loaded,
   not the default path (`C2/C3/C5/C6` post all exit 2).
3. **"The guard can be turned off by deleting the pin key"** — the EX-21
   prototype shape. CLOSED on the landed artifact: deleting the pin yields exit 2
   `pointer_table_unpinned` (fail-closed), so an emptied table under an unpinned
   baseline is no longer silent (`verify-extra-post.log` X2/X3).
4. **"The guard swallows real drift into the exit-2 bucket"** — REFUTED. At
   `66455858` (26 findings) and `HEAD~10` (2 findings) the probe still reports
   (`reported … exit=0`, `--strict` `failed … exit=1`). `verdict()` changed only
   by the CNE tuple.
5. **"The pin is stale or self-referential"** — REFUTED for staleness.
   `expected.json`'s pin equals the sha256 of both the worktree table and the
   `HEAD:` Git object (`verify-post.log` C9), and the default run is clean.
6. **"The guard is byte-level, so an honest reformat reddens"** — CONFIRMED and
   intended: a semantically identical re-serialization exits 2
   `pointer_table_tampered` (X1). Documented cost of a digest pin; the
   maintenance rule (re-pin in the same commit) is the answer.
7. **"The r10 experiment shape still works"** (RV-8's S2 consumer) — REFUTED as
   a compatibility claim: an honest, narrower custom table + the committed
   `expected.json` now exits 2 (X11). Declared consequence, and the escape hatch
   is real — a custom `expected.json` carrying a custom digest runs clean (X6
   demonstrates the same mechanism from the other side).
8. **"A same-authority writer can defeat the guard by re-pinning"** — CONFIRMED,
   out of scope. Editing the table *and* its pin in the same edit reads clean
   (X6); the pin terminates at `expected.json`, which carries no self-digest.
   This is a scope boundary, not a defect — recorded by PL-2 §7 A4, EX-24 §1 and
   RV-6 attack 11; my addition is the runnable measurement.
9. **"The selftest passes tautologically"** — REFUTED. Mutating each case's
   expected exit code, then each expected finding id, turns the suite red for
   **all 13** cases (26 runs, `verify-post.log` C11/C12). Every assertion bites.
10. **"The landed artifact diverges from the frozen spec"** — REFUTED. Byte
    identical to my independent reconstruction of PL-2's patch text, and equal to
    PL-2's own claimed prototype hash.
11. **"The selftest is green at every instant of the landing"** — REFUTED, and
    this is the one live defect I found. A snapshot at 07:15:49 (`53a94df2…`,
    guard present but the harness hunk not yet applied) read
    `FAILED cases=13 passed=1 failed=12 exit=1`: with no per-case pin, every
    fixture expected.json is unpinned, so all 12 pin-reachable cases exit 2. A
    parent committing during that window would have committed a red instrument.
    Fully reproduced by `reproduce-midlanding.py`. The settled state is green.
12. **"Every registry-row patch documents the landed ids"** — REFUTED. See §2:
    `table_tampered` is a case name, never an emitted finding id. EX-20's v2 text
    is correct; SC-4's diff and EX-21's row are not.
13. **"The output-parse contract holds"** — CONFIRMED. The verdict line remains
    last and keeps its format/labels; a tampered run emits exactly one finding
    line before it (`verify-extra-post.log` X8), and a foreign-CWD default-path
    invocation is unchanged (X7).

## 5. Blockers / notes

- **No blocker to the verdict.** EX-16 landed at ~07:16 and every required check
  was run by this seat against the real target afterwards; nothing here is
  inferred from a proxy.
- **`/tmp` is quota-exhausted this wave** (Errno 122 on a 14 KB copy; also hit by
  PL-2, RV-6, RV-8, EX-19, SC-4). All scratch lived under
  `claims/c2/RV-7/tmp/` with `TMPDIR` redirected there, and the bulk of it was
  removed at seat close (24 KB remains: the mid-landing reproduction output).
- **Untracked `__pycache__` directories exist inside the graded surface**:
  `.ufo/gates/citation-drift/__pycache__/citation-drift-probe.cpython-314.pyc`
  (07:16) and `.ufo/gates/__pycache__/`. They must not be committed. This seat
  did not remove them (removing files in the real target is outside a reviewer's
  write scope) — flagging for the integrator, alongside PL-2's note on
  `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc`.
- `.ufo/gates/c1-census-v10.py` is also modified in the worktree — C3's EX-28
  landing, outside this chain, not measured here.
- The instrument is green **only in its settled state**; if the parent re-runs
  after further edits, re-run `claims/c2/RV-7/named-checks-landed.log`'s four
  commands rather than trusting this snapshot.
