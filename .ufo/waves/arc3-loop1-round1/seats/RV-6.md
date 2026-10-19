# RV-6 seat report — arc3-loop1-round1, chain c2, role reviewer

Seat: RV-6 | chain c2 | role reviewer
Task: verify the exit-2 finding strings match the registry-row semantics exactly;
hunt for any remaining silent-rc-0 path on tampered/absent table (read the
implemented code). Verdict in this report.

Status at write time: **EX-16's guard change had NOT landed** (see §5). This
report therefore states the pre-state verdict from the code that is actually
implemented at HEAD, verifies the *row-side* semantics against the landed patch
text, and names the after-state gap precisely.

## 1. Work performed (evidence pointers)

- Read the frozen claims and seat rules: `.ufo/waves/arc3-loop1-round1/claims-frozen.md:40-54`
  (C2 claim), `:73-88` (seat discipline).
- Fingerprinted the pre-state inputs (sha256, all four files):
  `claims/c2/RV-6/pre-state-hashes.txt`
  - probe `3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f`
  - expected.json `4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33`
  - pointer-table.json `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`
  - SKILL.md `5c93c7c1bf45c72ca518f87fbba6f2a0bbf5685f67d263714b210a9a058830d4`
- Read the implemented probe end-to-end: `.ufo/gates/citation-drift/citation-drift-probe.py:1-467`.
- Confirmed the worktree matches HEAD for the graded surfaces:
  `git diff --stat HEAD -- .ufo/gates/ SKILL.md` → empty (no worktree drift).
- Read the protocol authority for the required semantics:
  `/home/vgpnk/Projects/shokunin/PROTOCOL.md:355-412` (Gate standard, "Two
  evidences": `expected.json` MUST pin the digest of every snapshot input file;
  digests verified **before comparing verdicts**; edited snapshot =
  `snapshot_tampered` (could-not-evaluate); baseline without digests =
  `unpinned (legacy)`).
- Read the registry row: `SKILL.md:371` (citation-drift row) and cross-checked
  each clause against the code (see §4, attack 8).
- Read the named debt source: `SCORECARD.md:925-926` (R6: "expected.json pins no
  digest of pointer-table.json — probe-exempt by kind, gate-blocking if ever
  promoted").
- Read the row-side patch text and the changeset: `claims/c2/EX-20/registry-row.patch.md`,
  `claims/c2/SC-4/changeset.md`. Independently reproduced EX-20's/SC-4's hashes
  on a private copy (`claims/c2/RV-6/patchtest/`):
  - old row sha256 `6413e8dc6384b9e0e34fca9903b55a4b8bba96066c26ca28789dc1939361d57f` ✓
  - `patch -p1` applies rc=0; line count 371 → 371; row still 5 cells
  - new row sha256 `08be1ec217322bbe0498b72012f3b0dab3f451b3fae12454dd66b62fb26d07a8` ✓
  - patched whole-file sha256 `fa94a4696ce68f96c8cdf717ac6d270ca7f0df5a4b590585bdedec95ff1628c5` ✓
  - row tokens present: `table_tampered`, `pointer_table_unreadable`, `unpinned`,
    `13 isolated-fixture` (one each).
- Ran the pre-state probes (§3) and the silent-rc-0 matrix:
  `claims/c2/RV-6/harness.sh` → output `claims/c2/RV-6/harness-pre.out`.
- Ran the suppression demonstrations (§4, attacks 4/5) with fixture tables under
  `claims/c2/RV-6/table-*.json`, including the frozen-rev run.
- Launched a 25×60s poll for EX-16's landing: `claims/c2/RV-6/poll-ex16.sh`,
  log `claims/c2/RV-6/poll.log` (fingerprint-change and artifact-dir detection).
- Built the ready-to-run after-state matrix: `claims/c2/RV-6/after-harness.sh`
  (14 probes incl. default-path tampering, `--table` bypass, unpinned expected,
  whitespace reformat, absent-at-default-path) and
  `claims/c2/RV-6/verify-landing.sh` (landed diff, pin-vs-actual digest, code's
  emitted id set vs row's declared id set, selftest case table, full matrix).
- Cross-read sibling c2 evidence for independent corroboration: SC-4's
  `verify-before.txt` (checks 4/5/6/8 reproduce my silent/guarded classes),
  EX-25's `logs/before-*.txt` (NO-PIN pre-state; frozen-rev run), RV-7's
  `verify-pre.log` (NO PIN FOUND; selftest-table sensitivity sweep).

## 2. Proposed changes

None by this seat (reviewer; no write scope beyond this report and its
artifacts). One conditional duty handed forward, not discharged here: the row
patch's three coupling tokens (`table_tampered`, `pointer_table_unreadable`,
`unpinned`) must be reconciled against EX-16's landed identifiers before the row
is applied — `verify-landing.sh` §G prints that exact string-set comparison. If
EX-16 lands different ids (e.g. `pointer_table_tampered`), the row patch must be
corrected to match the code, not the reverse.

## 3. Before→after measurement relevant to the C2 claim

Before (measured at HEAD `e845c2b`, pre-EX-16), commands and outputs verbatim:

- `python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest`
  → `CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0`, rc=0.
- `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD`
  → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0`, rc=0.
- `... --strict` → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`, rc=0.
- `expected.json` keys: `['_doc', 'frozen_run', 'snapshots', 'selftest']` — no
  table digest anywhere (`grep` for `pointer_table` finds only the finding-id
  strings). The named debt is present exactly as recorded.
- At the frozen-run revision `679af5d749f2fd48b9d543e3c99d348d5458f90f` with the
  current table: `CITATION_DRIFT_VERDICT: reported findings=16 exit=0` (probe),
  `failed findings=16 exit=1` (`--strict`) — the `frozen_run` block's recorded
  `"verdict": "failed"` / `citation_dead` is reproduced at that rev.
- Silent-rc-0 matrix (`harness-pre.out`):
  - absent table path → `CITATION_DRIFT: pointer_table_unreadable entry=nope.json
    [Errno 2] ...` rc=2 — **guarded**.
  - truncated table → `pointer_table_unreadable` rc=2 — **guarded**.
  - table = `[]` (type confusion) → `internal_error entry=gate AttributeError:
    'list' object has no attribute 'get'` rc=2 — **guarded** (generic id).
  - table = `{"entries":[],"quoted":[]}` → `reported findings=0 exit=0` rc=0 —
    **SILENT**.
  - table = `{}` → `reported findings=0 exit=0` rc=0 — **SILENT**.
  - table with every `must_match` weakened to `.*` → `reported findings=0
    exit=0` rc=0 — **SILENT**.
  - table with `entries` emptied but `quoted` kept → rc=0 — **SILENT**.
  - absent `expected.json` → `pointer_table_unreadable` rc=2 — guarded.
- Suppression at the frozen revision: same command as the 16-finding run above,
  only `--table` swapped to the emptied fixture → `clean findings=0 exit=0`
  (strict), rc=0. A hand-edit of the table erases the frozen baseline's verdict.

After (required by the C2 claim): selftest 13/13, tampered/absent table each
exit 2 with a declared finding id, findings=0 at HEAD. **Not measured — the
implementation did not land in this seat's window** (§5). The exact commands are
frozen in `after-harness.sh` and `verify-landing.sh` so the after-state is a
one-command rerun.

## 4. Attacks / refutations attempted (with verdicts)

1. **Absent table → silent?** REFUTED. `citation-drift-probe.py:280-284` catches
   `OSError` on the table load and files `pointer_table_unreadable`, which is in
   the CNE id list (`:72-75`) → exit 2. Run confirms (§3).
2. **Invalid JSON → silent?** REFUTED. Same `json.load` guard; run confirms rc=2.
3. **Type-confused table (list/dict-of-str) → silent?** REFUTED. The
   `AttributeError` escapes `run_check` and is caught in `main` (`:459-461`) as
   `internal_error` → CNE exit 2. (The id is generic rather than typed, but the
   class is right: never rc 0.)
4. **Tampered-but-valid-JSON table → silent?** **CONFIRMED.** The table is read
   from the worktree filesystem (`:281`), never as a Git object and never
   digest-checked; `table.get("entries", [])` (`:291`) makes an emptied table
   indistinguishable from a clean run. Demonstration with a real finding in
   play: `table-with-dead.json` (one injected impossible `exact` entry) →
   `CITATION_DRIFT: citation_dead entry=rv6-injected-dead SKILL.md:1 lacks
   'ZZZ-rv6-no-such-text'`; the same invocation shape with the entries emptied
   → `reported findings=0 exit=0`. The finding vanishes with no signal.
5. **Gate-mode promotion → silent?** **CONFIRMED.** With `--strict` the
   dead-entry table reads `failed findings=1 exit=1`; the emptied table reads
   `clean findings=0 exit=0`. A hand-edit of the table converts a *failed gate
   verdict* into a *clean gate verdict*. The strongest instance is the frozen
   revision itself: 16 findings (`failed exit=1`) → `clean findings=0 exit=0`
   with the emptied table. This is precisely the debt's "gate-blocking if ever
   promoted" clause, now measured rather than asserted.
6. **`--table` argument bypass:** **CONFIRMED (no check exists at all).** All
   tampered-table runs above passed `--table <non-default path>`; the probe has
   no path identity check, so nothing constrains which table was graded. A
   digest pin must therefore be enforced on whatever table is actually loaded,
   not only on the default path. `after-harness.sh` cases 5/14a/14b keep this
   test alive for the landed guard.
7. **`expected.json` unpinned / absent:** absent → exit 2 (finding
   `pointer_table_unreadable`, §3). Unpinned: currently there is nothing to
   check — a valid expected.json without any table digest is silently accepted
   (this is also the *current* committed state). After the guard lands this must
   read as the protocol's `unpinned (legacy)` class (could-not-evaluate), not as
   a pass; EX-20's row claims exactly that, so the landed code must implement it
   or the row's `unpinned` token must be deleted before the row is applied.
8. **Registry-row semantics vs implemented code (clause-by-clause):**
   - Row says probe semantics "0 reported ... and 2 could-not-evaluate;
     `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate".
     Code `verdict()` (`:69-84`) implements exactly this. MATCH.
   - Row says "the eleventh is dead/absent `--rev` → exit 2, finding
     `revision_unresolvable`". `expected.json` selftest[10] is exactly
     `{case: rev_unresolvable, exit_code: 2, finding: revision_unresolvable}`;
     selftest run prints it CLEAN. MATCH.
   - Row's pinned-values column says pointer-table.json "pins every in-repo
     citation" and expected.json "pins the self-test case table" — it does NOT
     claim a table digest. Consistent with the debt; the guard semantics are
     therefore **absent from the row today**, so no guard exit-2 string exists
     to match yet. The row-side strings to check live in EX-20's patch text.
   - Landed-row string-set duty: the patch declares `table_tampered` (digest
     mismatch), `pointer_table_unreadable` (absent), `unpinned` → CNE, 13 cases,
     guard fires "before any entry is evaluated". Of these, only
     `pointer_table_unreadable` is already an emitted id in the current code;
     `table_tampered` does not exist in the code today, and no unpinned-table
     class exists at all. So the row is currently *ahead* of the code by two
     tokens — exactly the coupling EX-20/SC-4 flagged. Unverified until EX-16
     lands.
9. **Inert declared semantics (adjacent, recorded not weaponized):**
   `pointer-table.json`'s `exempt` block and `expected.json`'s `frozen_run`
   block are read by nothing in the probe (grep: no reference to `exempt` or
   `frozen_run` in the script). The frozen-run baseline is documentation, not an
   enforced comparison; the digest pin (the C2 fix) is what makes a rerun
   reproducible, and even then the probe will not compare against
   `frozen_run.expected_findings`. Worth one line in the row so no reader
   believes the frozen verdict is machine-checked.
10. **Frozen-rev reproduction (corrected):** my first harness run reported
    findings=0 at the frozen rev — that was **my own harness bug**: `run()`
    hardcodes `--rev HEAD`, so the labelled "frozen-rev" case never used the
    frozen rev. Caught by reading EX-25's `before-frozen-run-rev.txt`, then
    re-measured directly: at `679af5d` the current table yields 16 findings
    (`failed` under `--strict`), reproducing `frozen_run`'s recorded
    `"verdict": "failed"` with `citation_dead` among them. The block is coherent;
    no defect. (Recorded because the wrong reading was published in this
    report's first revision — the correction is the evidence, not the errata.)
11. **Fabricated `(table, expected)` pair (residual, pre-registered):** a
    same-privilege writer who edits both files can always re-pin; the pin chain
    terminates at `expected.json`, which carries no self-digest. Pre-state this
    is trivially silent; post-landing `verify-landing.sh` §J measures it. This is
    an accepted residual already recorded by EX-20 ("What this patch does NOT
    do") and SC-4 §6 — my addition is only the runnable probe. Note for the row:
    its sentence "a tampered table can never read as silent findings" should be
    read as "while the pin is in force"; the pair-fabrication path is outside
    its scope.

## 5. Blockers / gaps

- **EX-16's real-target write landed at ~07:20 during this seat's poll window.**
  Landing evidence: `.ufo/waves/arc3-loop1-round1/claims/c2/EX-16/` (before/after
  captures, `landing-diff.md`); `git status` shows
  `.ufo/gates/citation-drift/{citation-drift-probe.py,expected.json}` modified;
  probe `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`
  (byte-identical to PL-2's validated prototype), expected.json
  `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7`;
  `pointer-table.json` byte-stable at `738b3a56…`. After-state verification is
  §7. (The pre-landing polling gap is recorded in `claims/c2/RV-6/poll.log`:
  unchanged fingerprints through check 9, the EX-16 dir appearing at 07:15, the
  file hashes changing at ~07:20.)
- **VERDICT (the seat's answer to its task).** Read against the code that
  actually exists — the unlanded real target plus EX-21's published guarded
  prototype (`claims/c2/EX-21/tmp/proto/probe.py`, sha256 `776cef6a…`, the
  closest-to-implemented artifact; §6):
  1. **Row strings do NOT match the code.** EX-20's row patch declares the
     digest-mismatch finding as `table_tampered`; the prototype emits
     `pointer_table_tampered` (CNE list + guard site). One of the two must
     change; as written, applying the row would document an id the instrument
     never emits.
  2. **A silent-rc-0 path remains in the prototype.** The guard is
     `if pinned_table is not None and sha256(table) != pinned_table` — delete
     the `table_sha256` key from `expected.json` and the guard skips entirely:
     an emptied table reads `reported findings=0 exit=0` (and `clean` under
     `--strict`). Independently reproduced (my §6/H, SC-4's verify-proto P4).
     EX-20's row claims "unpinned → exit 2"; the code does not implement it.
     Because the selftest's fixtures always write their own pinned expected,
     the instrument can run 11/11–13/13 green while the real guard is inert —
     live instance: EX-21's own proto directory ships an unpinned 11-case
     `expected.json` (byte-identical to the repo pre-state, `4e28ba90…`) next
     to the guarded probe, and I measured its selftest at 11/11 green with the
     guard off.
  3. When the pin IS in force, the guard is correct as claimed: preflight
     (fires with `entries` emptied, no entry evaluation, exactly one finding),
     both modes exit 2, absent table → `pointer_table_unreadable`, non-default
     `--table` still enforced (not path-keyed). Byte-level pin: a whitespace
     append reddens as `pointer_table_tampered` (intended cost, worth a row
     line).
  Recommended resolution: implement unpinned → CNE in the landed code (then
  the row's `unpinned` token is right), and correct the row token to whatever
  id the landed code emits (`pointer_table_tampered` in the prototype). If the
  implementer prefers skip-on-unpinned, EX-20's own instruction applies: delete
  the `unpinned` token — but then the claim's "never silent findings" does not
  hold in the pin-deleted state, and the round should say so.
- `/tmp` hit the user disk quota this wave (`printf: write error: Disk quota
  exceeded`, tmpfs 80% full) — all scratch was relocated inside this seat's
  allowed artifact directory with `TMPDIR` redirected there
  (`claims/c2/RV-6/tmp/`). `patch` also failed until `TMPDIR` was redirected.
  Other seats' harnesses that assume `/tmp` may be affected; recorded for the
  wave integrator.
- After-state one-command rerun for whoever lands EX-16 (or the parent):
  `bash .ufo/waves/arc3-loop1-round1/claims/c2/RV-6/verify-landing.sh` — prints
  the landed diff, the pin-vs-actual digest, the code's emitted guard id set
  next to the row's declared set (§G), the selftest case table, the clean-run
  readings, the full 14-case matrix, and the fabricated-pair residual.

## 6. Prototype-code review (EX-21's guarded probe; evidence `claims/c2/RV-6/proto-attacks.out`)

Artifact reviewed: `claims/c2/EX-21/tmp/proto/probe.py`, sha256
`776cef6af5b7404f6a0d0667727ecf99a6bb32a6db357b443e6fa5c1585ca283`
(21841 B, mtime 07:03:11-03:00). Read-only copy under `claims/c2/RV-6/proto-test/`.
Its sibling `expected.json` at review time: sha256 `4e28ba90…` — byte-identical
to the repo's pre-state file (11 cases, **no `table_sha256` key**).

Guard implementation (probe.py `run_check`):
`pinned_table = expected.get("table_sha256")` then
`if pinned_table is not None and sha256_bytes(table_bytes) != pinned_table:`
→ `findings.add("pointer_table_tampered", …)`, `return findings` (before the
entries loop). CNE list gains `pointer_table_tampered`.

Measured (commands in `proto-attacks.sh`; all runs `--root <repo> --rev HEAD`):

| # | table | expected | rc | verdict / finding |
|---|---|---|---|---|
| B | real | pinned | 0 | `reported findings=0 exit=0` |
| C | emptied | pinned | 2 | `could-not-evaluate` / `pointer_table_tampered` |
| C2 | emptied | pinned `--strict` | 2 | `could-not-evaluate` / `pointer_table_tampered` |
| D | absent path | pinned | 2 | `could-not-evaluate` / `pointer_table_unreadable` |
| E | real + one appended space | pinned | 2 | `pointer_table_tampered` (byte-level pin) |
| F | real (non-default `--table` path) | pinned | 0 | pin enforced on the loaded table, not the path |
| H | emptied | **unpinned (key deleted)** | **0** | **`reported findings=0 exit=0` — SILENT** |
| H2 | emptied | unpinned `--strict` | **0** | **`clean findings=0 exit=0` — SILENT** |
| H3 | real | unpinned | 0 | guard inert (indistinguishable from clean) |
| I | emptied | expected absent | 2 | `pointer_table_unreadable` (expected-load failure) |
| A | — | selftest, as-shipped (unpinned, 11 cases) | 0 | `11 passed=11 failed=0` — **green while inert** |
| A2 | — | selftest, my pinned 13-case table | 0 | `13 passed=13 failed=0` |
| J | emptied | pin = `12345` (int) | 2 | `pointer_table_tampered` — fails closed |
| K | emptied | pin = `""` (empty string) | 2 | `pointer_table_tampered` — fails closed |
| L | emptied | expected.json = `[]` (list) | 2 | `internal_error` — fails closed |
| M | absent path | pinned | 2 | `pointer_table_unreadable` (table-load precedes digest) |

The pin-field type-confusion sweep (J/K/L) closes cleanly: every malformed pin
still exits 2. Combined with A–M, the prototype's *only* silent-rc-0 path is the
missing-pin skip (H) — there is no second hole in this artifact.

String-set comparison (probe code vs EX-20's patched row):
- code emits `pointer_table_tampered` (guard site + CNE list); row declares
  `table_tampered` → **MISMATCH** (the row's own coupling note anticipated this
  substitution).
- code's selftest *case name* is `table_tampered` while the *finding id* is
  `pointer_table_tampered` — the row's phrase "finding `table_tampered`" reads
  the case name as an id; correct the row to the emitted id.
- absent table: code `pointer_table_unreadable` == row `pointer_table_unreadable`
  → MATCH.
- unpinned: code skips (silent), row declares exit 2 → **MISMATCH**.
- case count: prototype's 13 = existing 11 + `table_tampered` + `table_absent`
  (case names), consistent with the claim's 11 → 13; "clean-tree" in the claim's
  parenthetical maps to the existing `clean` case, not a third new one.

Artifact-integrity notes for the integrator (not this seat's write scope):
- EX-21's published `logs/proto-probe.diff` does **not** reproduce EX-21's own
  `probe.py`: applying it yields sha256 `ea364f2d…` vs `776cef6a…`, missing the
  `build_fixture` case-routing hunk; the diff-applied probe then fails its own
  selftest 9/13 (SC-4 `verify-proto.txt` P7/P7b). Integrate the probe.py, not
  the diff, or fix the diff.
- EX-21's proto dir currently pairs the guarded probe with the unpinned
  pre-state `expected.json` (mtime 07:07:32, after SC-4's 07:06:59 run against
  hash `376f9fc5…`) — if that directory is treated as the integration source,
  the pin travels only in the probe, not in the expected file.

## 7. After-state verification (EX-16's landed write; evidence `claims/c2/RV-6/verify-landing.out`)

Landed files (sha256): probe `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`,
expected.json `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7`,
pointer-table.json unchanged `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`.
The landed probe/expected are **byte-identical to PL-2's validated prototype**
hashes (`PL-2/frozen-run-guard.patch.md:11-15`) — the plan's design is what
landed, not EX-21's divergent prototype (which used a flat `table_sha256` key
and skip-on-unpinned). One bookkeeping note: PL-2's parenthetical "includes a
trailing newline" is inaccurate — the landed file has no trailing newline and
still hashes to `ff47bfd6…`, so the hash match is real, the note is not.

The claim's falsifiable legs, measured:

| leg | reading |
|---|---|
| selftest 11 → 13 at exit 0 | `CITATION_DRIFT_SELFTEST: CLEAN cases=13 passed=13 failed=0 exit=0`, rc=0; new cases `table_tampered` → exit 2 `pointer_table_tampered`, `table_absent` → exit 2 `pointer_table_unreadable` |
| pin present and correct | `expected.json` key `/pointer_table/sha256` = `738b3a56…` = actual sha256(pointer-table.json) |
| findings = 0 at HEAD | `reported findings=0 exit=0` (probe), `clean findings=0 exit=0` (`--strict`) |
| drift semantics preserved | at frozen rev `679af5d…`: 16 findings, probe rc=0 / strict `failed exit=1` |

Silent-rc-0 hunt, re-run against the landed guard (matrix cases 4-14c):

| attack | reading | verdict |
|---|---|---|
| emptied/weakened/dead-injected table, non-default `--table` | exit 2 `pointer_table_tampered`, exactly 1 finding | closed |
| emptied table at the DEFAULT path | exit 2 `pointer_table_tampered` | closed |
| emptied table at the DEFAULT path, `--strict` | exit 2 (CNE wins in both modes) | closed |
| table path absent (default and non-default) | exit 2 `pointer_table_unreadable` | closed |
| expected.json absent | exit 2 `pointer_table_unreadable` | closed |
| **pin key deleted (the EX-21-prototype hole)** | exit 2 `pointer_table_unpinned` | **closed by the landed design** |
| table = `[]`, `{}`, truncated, non-UTF8 | exit 2 (`pointer_table_tampered` when the bytes mismatch the pin; `pointer_table_unreadable` after a matching pin) | closed |
| whitespace-only reformat of the table | exit 2 `pointer_table_tampered` (byte-level pin; intended cost) | closed (noisy, not silent) |
| fabricated (table, expected) pair | rc=0 | accepted residual (pin chain terminates at `expected.json`; recorded by EX-20/SC-4, unchanged) |

Verdict on the seat's own task: **no remaining silent-rc-0 path on a tampered or
absent table in the landed code** — the guard is preflight (fires with `entries`
emptied, before any entry is graded), enforced on whatever table the invocation
loads (not path-keyed), and fails closed on every malformed pin shape
(`None` → unpinned; int/empty-string → tampered). The only silent reading left
requires editing `expected.json` itself, which is the baseline of record.

**Row reconciliation (the exact-string duty), final:**
- Landed code's guard finding ids: `pointer_table_tampered` (digest mismatch),
  `pointer_table_unreadable` (absent/unreadable/parse failure),
  `pointer_table_unpinned` (no pin). Note the string `table_tampered` exists in
  the code only as the selftest *case name*, never as a finding id.
- **PL-2's row text (patch 3) matches the landed code exactly**: all three ids
  named with exit 2, "13 isolated-fixture cases" with the twelfth/thirteenth
  clauses, and the pinned-values cell naming the table digest + re-pin rule. It
  is patch text only (SKILL.md is protected); `SKILL.md` sha256 is still
  `5c93c7c1…` — the row is **not yet in the repo**, so the C2 claim's
  "the SKILL.md registry row states the guard semantics" leg is **unsatisfied
  pending parent integration**.
- **EX-20's row text must NOT be applied as written**: it declares
  `table_tampered` (an id the instrument never emits) and omits
  `pointer_table_unpinned` (an id it does emit). EX-20's own coupling note
  anticipated the id substitution; it did not know about the third class. Use
  PL-2's row text (verified byte-exact by SC-4, `fa94a469…` whole-file hash
  reproduced by this seat) or reconcile EX-20's text to the landed ids.
