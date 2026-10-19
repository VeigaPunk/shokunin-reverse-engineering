# SC-4 seat report — arc3-loop1-round1, chain c2, role scribe

Seat: SC-4 | chain c2 | role scribe | 2026-10-19
Task: patch-set consolidation — EX-16's actual diff (captured read-only via
`git diff`) + EX-20/EX-21 patch texts into one reviewable changeset listing.
Deliverable: `.ufo/waves/arc3-loop1-round1/claims/c2/SC-4/changeset.md`
(finalized 07:18, after EX-16's landing at 07:15).

## 1. Work performed (each with an evidence pointer)

- Read the frozen claims and seat rules: `claims-frozen.md:40-54` (C2 claim),
  `:73-88` (seat discipline). Baseline: HEAD
  `e845c2b524ad2e59871e004c51a1386e192a74ab`; pre-state sha256s probe
  `3067621ac44d…`, expected `4e28ba908bcd…`, table `738b3a569fb7…` (all three
  reproduce RV-6's `pre-state-hashes.txt` and EX-25's `before-sha256.txt`).
- Built `claims/c2/SC-4/verify-changeset.sh` (11 checks: selftest case list,
  committed case table, probe + `--strict` at HEAD, emptied-table attack,
  weakened-`must_match` attack, absent table, pin consistency, unpinned attack,
  single-finding assertion, default-path run from a foreign CWD, forged
  `--expected` residual check) and ran **before** → `verify-before.txt`.
- Verified EX-20's `SKILL.md` patch text: extracted the diff
  (`scratch/registry-row.diff`, `dc99484b…`), applied to a pristine
  `git show HEAD:SKILL.md` copy (`patch -p1` dry-run + apply rc 0), 371 → 371
  lines, 5 cells; row `6413e8dc…` → `08be1ec2…`, file `fa94a469…` all reproduce.
- Measured EX-21's prototype: `verify-proto.sh` → `verify-proto.txt`
  (P1-P7b, incl. the unpinned hole P4 and the stale-diff defect P7/P7b).
- Measured the fail-closed variant before the landing: `verify-failclosed.sh`
  → `verify-failclosed.txt` (F1-F6b; variant sha `28cc1187…`).
- **Captured EX-16's landed diff** at 07:15:44 and again at 07:16:
  `git diff --stat` + full `git diff -- .ufo/gates/citation-drift/` →
  `claims/c2/SC-4/diff-ex16.txt` (`78ae7971…`, 95 lines); post sha256s probe
  `e2665074…`, expected `ff47bfd6…`, table unchanged; pin equals table bytes.
- Ran the **after** leg: `verify-after.txt` (11 checks; every guard attack
  flipped from silent rc 0 to the declared exit-2 class).
- Verified landing fidelity against the authoring patch (PL-2's
  `frozen-run-guard.patch.md`): patch 1 extracted + applied to a pristine HEAD
  copy reproduces the landed probe byte-identically (`e2665074…`); patch 2's
  three text edits replayed by SC-4 reproduce the landed `expected.json`
  byte-identically (`ff47bfd6…`, valid JSON).
- Compared the two competing `SKILL.md:371` row texts (EX-20's and PL-2's
  patch 3): both leave 371 lines / 5 cells; EX-20's row names `table_tampered`
  (≠ landed `pointer_table_tampered`), PL-2's names the landed ids; shas
  `08be1ec2…`/`fa94a469…` vs `d25c5292…`/`483b0eba…`.
- Wrote the consolidated listing `claims/c2/SC-4/changeset.md` (final: landed
  diff verbatim + traceability + acceptance table + coupling verdicts +
  residual risks + close-out) and a verified fallback patch kit
  `proposed-guard-failclosed.patch.md`.
- Polled `seats/` and `claims/` on the wave cadence (25×60s background loop
  from 06:59, plus direct checks); EX-16's artifact dir appeared 07:15 and its
  gate writes at 07:15:44.

## 2. Proposed changes

**None authored by SC-4 against the real target.** The reviewable set is the
listing (`changeset.md`) plus one patch-text artifact:

- `claims/c2/SC-4/changeset.md` — the consolidation deliverable; its embedded
  landed diff is byte-identical to the capture file (self-checked).
- `claims/c2/SC-4/proposed-guard-failclosed.patch.md` — patch text only
  (extracted diff re-applies byte-identically to `28cc1187…`); **superseded by
  the landed shape** (flat `table_sha256` vs landed `pointer_table.sha256`),
  kept as a fallback.
- Recommendation carried to the parent: land PL-2's patch 3 as the
  `SKILL.md:371` row, or apply EX-20's with the `table_tampered` →
  `pointer_table_tampered` substitution (changeset §3).

All SC-4 writes are confined to `claims/c2/SC-4/`; no repo file outside it was
modified; no git mutation was run (only `status`, `diff`, `show`, `rev-parse`);
the real gate was only read.

## 3. Before→after measurement relevant to the C2 claim

Before (HEAD `e845c2b`, `verify-before.txt`):

- `--selftest` → `CLEAN cases=11 passed=11 failed=0 exit=0`; committed case
  table 11 cases; no table digest anywhere in `expected.json`.
- probe at HEAD → `reported findings=0 exit=0`; `--strict` → `clean findings=0
  exit=0`.
- emptied table via `--table` → `reported findings=0 exit=0` (**silent**);
  weakened `must_match` → same; unpinned expected → silent; `finding_lines=0`.

After (landed, `verify-after.txt`):

- `--selftest` → `CLEAN cases=13 passed=13 failed=0 exit=0`; committed case
  table 13 (`table_tampered` exit 2 `pointer_table_tampered`; `table_absent`
  exit 2 `pointer_table_unreadable`).
- probe at HEAD → `reported findings=0 exit=0`; `--strict` → `clean findings=0
  exit=0`.
- emptied / weakened table → `pointer_table_tampered … exit=2`;
  absent table → `pointer_table_unreadable … exit=2`;
  unpinned expected → `pointer_table_unpinned … exit=2`;
  `finding_lines=1` on a guard trip (no entry evaluation);
  pin `pointer_table.sha256 = 738b3a56…` equals the table's bytes;
  default-path run from a foreign CWD → `findings=0 exit=0`.

Every C2 claim leg is therefore measured at the landed sha256s: pin present and
correct, tampered/absent → declared exit-2 class (never silent), selftest
13/13, findings=0 at HEAD.

## 4. Attacks / refutations attempted (with verdicts)

1. **`--table` path swap with a semantically tampered table.** Before: silent
   rc 0. After: exit 2 `pointer_table_tampered` (non-default paths fire) —
   **closed by the landing**.
2. **Pin-field deletion (unpinned expected) with a tampered table.** Before:
   silent. EX-21 prototype: still silent (P4, skip-on-unpinned). Fail-closed
   variant measured pre-landing (F3/F4, 13/13 selftest). **After: the landed
   guard is fail-closed — exit 2 `pointer_table_unpinned`. Closed.**
3. **Forged `--expected` (pin recomputed for a tampered table).** Before:
   silent. After: **still silent rc 0** (check 11). **Residual limit, inherent
   to a pin file the caller can point elsewhere; recorded in changeset §6.**
4. **EX-21's published `proto-probe.diff` as a landing patch.** Applies rc 0
   but yields `ea364f2d…` ≠ its prototype `776cef6a…`; the applied result
   fails 4 selftest cases (9/13, exit 1). **Defect D1 — the diff must not be
   applied.**
5. **Finding-id reconciliation (patch texts vs landed code).** EX-20's row
   names `table_tampered`; landed code emits `pointer_table_tampered`; PL-2's
   patch 3 names the landed ids. **Verdict: EX-20's row needs one
   substitution; PL-2's is consistent (changeset §3).**
6. **Landing fidelity to the authoring patch.** PL-2's probe diff and its
   `expected.json` text edits each reproduce the landed files
   byte-identically. **Verdict: proposal == landing for the two code artifacts;
   the third (SKILL.md row) is the open decision.**
7. **Default-path invocation from a foreign CWD.** Before and after: resolves
   to the gate's own table, `findings=0 exit=0` (checks 10). **No defect.**
8. **Single-finding assertion** (guard fires before entry grading): after,
   `finding_lines=1` with no `citation_*` rows. **Ordering as claimed.**
9. **PL-2 patch-2 hash note.** PL-2 records that its resulting-file hash
   "includes a trailing newline the real file should not gain"; the landed file
   has no trailing newline and still hashes to `ff47bfd6…`. **Doc nit only,
   recorded in changeset §2.**
10. Cross-referenced, not re-run: RV-6's silent matrix and `--table` bypass
    (`harness-pre.out`), EX-24's co-mutation/forged-`--expected` attacks
    (T2/T5/T6) — same residual class as attack 3.

## 5. Blockers / gaps

1. **Resolved:** EX-16's landing (absent until 07:15) — captured, verified, and
   reconciled in the final changeset. The earlier "not landed" state of this
   report is superseded by §3's after leg.
2. **Open decision for the parent:** two `SKILL.md:371` row patch texts compete
   (EX-20's id-inconsistent vs PL-2's id-consistent); apply exactly one
   (changeset §3).
3. **Housekeeping:** untracked bytecode appeared under `.ufo/gates/` and
   `.ufo/gates/citation-drift/` (`__pycache__/*.pyc`) — drop at integration.
4. **`/tmp` quota** (`tee: /tmp/sc4-baseline.txt: Disk quota exceeded`; tmpfs
   13G/16G, `usrquota`): all SC-4 scratch lives under
   `claims/c2/SC-4/scratch/` with `TMPDIR` redirected there (same workaround as
   RV-6/EX-24). Scratch is retained because the harnesses re-create their own
   inputs from it.
5. EX-20's and EX-21's seat reports landed after this seat's first assembly;
   the final changeset is built from their artifacts and the landed code, so it
   is self-contained either way.
