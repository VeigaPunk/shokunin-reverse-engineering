# PL-2 plan — C2 citation-drift probe: frozen-run guard (R6 debt)

Seat PL-2, chain c2, wave arc3-loop1-round1, 2026-10-19. Planner artifact. The
validated patch text lives beside this file at
`claims/c2/PL-2/frozen-run-guard.patch.md`; EX-16 is the only seat allowed to
write the real target `.ufo/gates/citation-drift/`.

## 1. Debt and claim (frozen)

- Debt (R6), named carried debt from `SCORECARD.md:925-926` (arc2-loop1-round4):
  "the probe's frozen-run guard (R6: expected.json pins no digest of
  pointer-table.json — probe-exempt by kind, gate-blocking if ever promoted)".
- Claim (`claims-frozen.md:46-54`): after the round's commit, `.ufo/gates/
  citation-drift/` pins the sha256 of `pointer-table.json` in `expected.json`;
  a tampered or absent table yields the declared preflight could-not-evaluate
  class (exit 2), never silent findings; the SKILL.md registry row states the
  guard semantics; selftest 11 → 13 cases (clean-tree, tampered-table,
  absent-table) at exit 0; findings = 0 at HEAD.

## 2. Before-state (measured by this seat; commands in §6)

| Item | Value |
|---|---|
| HEAD | `e845c2b524ad2e59871e004c51a1386e192a74ab` |
| pointer-table.json sha256 (worktree == committed; `git status` clean) | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` |
| expected.json sha256 | `4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33` |
| citation-drift-probe.py sha256 | `3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f` |
| selftest | 11/11 CLEAN, exit 0 |
| live probe at HEAD | `CITATION_DRIFT_VERDICT: reported findings=0 exit=0` |
| tampered table (valid JSON, `entries` emptied) | **`findings=0 exit=0` — silent false-clean (THE GAP)** |
| absent table | exit 2, `pointer_table_unreadable` (already correct; untested by any selftest case) |

The gap in one line: a tampered table that still parses is graded as if it were
the baseline, so removing every entry produces a clean verdict. The guard makes
the table's bytes part of the frozen-run contract.

## 3. Guard design

**Preflight order** in `run_check` (after the existing `root_ok` /
`rev_ok` checks, whose order and findings are unchanged):

1. load `expected.json` — unreadable/invalid → `pointer_table_unreadable`
   (existing string, basename of the expected file), exit 2, stop. (expected is
   now load-bearing because it holds the pin; before it was loaded after the
   table and evaluation continued. Exit code and finding string are unchanged
   for every reachable input; see §7 attack A5.)
2. read the pin `expected["pointer_table"]["sha256"]` (dict-guarded). Pin
   absent/malformed container → `pointer_table_unpinned` (NEW), exit 2, stop.
   Fail-closed: a baseline that pins no digest is not a frozen run (mirrors the
   existing `unpinned_legacy` snapshot semantics, exit 2).
3. read `--table` bytes; absent/unreadable → `pointer_table_unreadable`
   (existing string), exit 2, stop.
4. `sha256(bytes) != pin` → `pointer_table_tampered` (NEW), exit 2, stop.
5. parse the table; parse failure → `pointer_table_unreadable` (existing
   string), exit 2, stop. (The `table_unreadable` case still reaches this step:
   its expected file pins the digest of the garbage bytes, which therefore
   matches.)
6. evaluate entries exactly as today.

**Finding ids.** `pointer_table_tampered` and `pointer_table_unpinned` join the
could-not-evaluate set in `Findings.verdict()`; the CNE check runs before the
`--strict` branch, so the guard exits 2 in BOTH probe and gate modes. The
parallel is deliberate: `snapshot_missing` / `snapshot_tampered` already
separate "unreadable" from "digest mismatch" in this same file; the table gets
the same two classes plus the unpinned class.

**Probe kind preserved.** The only `verdict()` change is the CNE tuple. The
drift class is untouched: probe mode still returns 0 ("reported") for
citation findings, `--strict` still returns 1. Measured at the frozen revision
(§6, K/L): 16 findings → probe rc 0 / strict rc 1.

**expected.json schema (new top-level key, sibling of `snapshots`):**

```json
"pointer_table": {"sha256": "<64 hex of pointer-table.json>", "note": "frozen-run guard (R6 debt, arc3-loop1-round1): sha256 of pointer-table.json at the frozen run; any byte difference is pointer_table_tampered, an absent table is pointer_table_unreadable, an unpinned baseline is pointer_table_unpinned -- all exit 2"}
```

Pin value for this round: `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f`
(the table is not edited by this claim; if EX-16 changes the table for any
reason, compute the pin over the FINAL bytes in the same commit).

**Maintenance rule (stated in the SKILL.md row):** any edit to
`pointer-table.json` must re-pin its digest in `expected.json` in the same
commit; a run over a different table requires its own expected file pinning
that table (the selftest harness already follows this pattern per case).

## 4. The two new selftest cases (exact spec)

Harness change (both cases need it): the per-case expected file now pins the
digest of the table the harness just wrote, for EVERY case —
`{"snapshots": digests, "pointer_table": {"sha256": sha256_bytes(table_bytes)}}`
— so all 11 existing cases exercise the guard-passing path and stay CLEAN.

- **case 12 `table_tampered`** — tree: `build_fixture("clean")`; table:
  `fixture_table("clean")` serialized to `table.json` (bytes B0); expected pins
  `sha256(B0)`; THEN the table is overwritten with `{"entries": []}` (valid
  JSON, the silent-clean shape). Want: exit 2, finding `pointer_table_tampered`.
  Discrimination: the same table without the guard measures `findings=0 exit=0`
  (before-state §2 row 7) — this case pins exactly the hole being closed.
- **case 13 `table_absent`** — tree: `build_fixture("clean")`; table: B0;
  expected pins `sha256(B0)`; THEN `os.remove(table)`. Want: exit 2, finding
  `pointer_table_unreadable`.

Case rows appended to `expected.json` `selftest` (after `rev_unresolvable`):

```json
{"case": "table_tampered", "exit_code": 2, "finding": "pointer_table_tampered"},
{"case": "table_absent", "exit_code": 2, "finding": "pointer_table_unreadable"}
```

`_doc` update: "…pins the digest of every snapshot input file AND of the
pointer table itself (a tampered or absent table is could-not-evaluate, never
silent findings), and…". The `frozen_run` block and the 11 existing rows are
untouched.

## 5. SKILL.md registry-row wording (exact; full row in the patch artifact)

Kind stays `probe / kaidoku`; the verdict-map cell keeps "0 reported (drift is
reported, never failed) and 2 could-not-evaluate". Three edits to row
`SKILL.md:371`:

1. Entry/verdict map cell, append: "**frozen-run preflight: the table's sha256
   must match the digest pinned in `expected.json` — a tampered table (exit 2,
   finding `pointer_table_tampered`) or an absent table (exit 2, finding
   `pointer_table_unreadable`) is could-not-evaluate before any entry is
   graded; a baseline that pins no digest is exit 2, finding
   `pointer_table_unpinned`; drift reporting is unchanged (rc 0)**".
2. Self-invocation cell: "11 isolated-fixture cases" → "13 isolated-fixture
   cases", and after the existing eleventh-case clause add: "the twelfth is a
   tampered table → exit 2, finding `pointer_table_tampered`; the thirteenth is
   an absent table → exit 2, finding `pointer_table_unreadable`".
3. Pinned-values cell: "`expected.json` pins the self-test case table" →
   "`expected.json` pins the self-test case table **and the sha256 of
   `pointer-table.json` (frozen-run guard; any edit to the table must re-pin
   the digest in the same commit)**".

## 6. Prototype validation (scratch copies only — this seat may not write the target)

Prototype built from byte-identical copies (sha256-verified) of the three gate
files in `/home/vgpnk/.pl2-tmp/gate/` (scratch; /tmp is quota-exhausted this
wave — see §8). Prototype probe sha256
`e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`; prototype
expected.json sha256 `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7`.

- **Selftest: 13/13 CLEAN exit 0** — all 11 existing cases byte-identical
  verdicts, plus `table_tampered` exit 2 `pointer_table_tampered` and
  `table_absent` exit 2 `pointer_table_unreadable`.
- **D clean (pinned table copy):** `reported findings=0 exit=0` — guard passes
  silently, probe output shape unchanged.
- **E tampered:** `CITATION_DRIFT: pointer_table_tampered … sha256
  1ee2bd73… != pinned 738b3a56…` → `could-not-evaluate findings=1 exit=2`.
- **F absent:** `pointer_table_unreadable` → exit 2.
- **G unpinned baseline** (expected copy without the key): exit 2
  `pointer_table_unpinned` — fail-closed demonstrated.
- **H tampered under `--strict`:** exit 2 (CNE class wins in both modes).
- **I/J missing `--expected` file:** original and prototype produce IDENTICAL
  output (exit 2, `pointer_table_unreadable entry=nope.json …`) — byte-stable.
- **K/L frozen revision `679af5d…`, pinned table, prototype:** 16 findings →
  probe mode `reported … exit=0`, strict mode `failed … exit=1` — the probe
  kind and the gate map are both preserved with drift present.

## 7. Attacks attempted (verdicts)

- A1 "a tampered table is already caught (JSON parse fails)" — REFUTED by
  measurement: a valid-JSON emptied table grades `findings=0 exit=0`.
- A2 "the guard adds nothing for the absent case" — PARTIALLY TRUE: absent
  already exits 2 via `pointer_table_unreadable`; the guard's new value is the
  tampered class, the pinned contract, and the explicit case (absent was
  untested). Stated honestly in the claim's before→after.
- A3 "the guard is bypassable by deleting the pin key" — CLOSED by fail-closed
  `pointer_table_unpinned` (exit 2, measured demo G).
- A4 "the pin cannot defend against tampering of expected.json itself" — TRUE
  and out of scope: expected.json is the baseline of record, the same trust
  class as the committed case table; any change to it is a baseline change,
  visible in the diff.
- A5 "reordering expected-before-table changes behavior" — CHECKED: no
  existing case or reachable invocation changes exit code or finding id; the
  only delta is that an unreadable expected file stops evaluation instead of
  grading against `expected={}` (both were exit 2, same finding string;
  measured I vs J identical).
- A6 "guard fires only in gate mode" — REFUTED: the CNE set is checked before
  the `--strict` branch; demos E (probe mode) and H (strict) both exit 2.
- A7 "drift semantics broken by the guard" — REFUTED: K/L show rc 0 probe /
  rc 1 strict with 16 live drift findings; `verdict()` changed only by two CNE
  ids.

## 8. Blast radius, handoff, notes

- Only `.ufo/gates/citation-drift/{citation-drift-probe.py, expected.json}` +
  `SKILL.md:371` change. `pointer-table.json` content untouched; `frozen_run`
  block untouched; the 11 case rows untouched; `--table/--expected/--root/
  --rev/--strict` CLI unchanged.
- Preserve expected.json's no-trailing-newline single-line style when applying
  the patch (text edit, not rewrite).
- After-measurement EX-16 must run (claim's own falsifiable): selftest → 13/13
  exit 0; live at the work commit → `findings=0 exit=0`; tampered/absent demos
  on scratch copies (never in the repo) → exit 2 with the declared ids;
  sha256sum receipts for the three files.
- Flag (not this seat's to fix): `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc`
  (mtime 2026-10-19 07:04:16 -0300) appeared untracked during this wave — a
  concurrent seat imported the census module; EX-16/C3 seats should keep it out
  of any commit.
- Blocker (fleet-wide): `/tmp` is a tmpfs with `usrquota`, exhausted — even a
  4 KiB write fails ("Disk quota exceeded"), and the probe selftest needs
  writable temp dirs. This seat used `TMPDIR=/home/vgpnk/.pl2-tmp` (scratch,
  removed after; the round-4 `/tmp-quota abort` defect note shows this hazard
  class). The selftest's temp dirs honor TMPDIR, so this is a pure environment
  workaround, not a behavior change.

## 9. Open items for the chain

- EX-16: apply the patch artifact verbatim, re-pin if the table changes, run
  the after-measurements, record file sha256s in its report.
- If reviewers want the unpinned path case-covered too, that would be a 14th
  case — the frozen claim fixes 13; PL-2 recommends keeping 13 and citing demo
  G as the unpinned-path evidence.
