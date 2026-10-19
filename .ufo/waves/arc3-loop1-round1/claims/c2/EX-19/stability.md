# EX-19 — frozen-run byte-stability + non-guard code-path diff (C2)

Seat EX-19, chain c2, wave arc3-loop1-round1, 2026-10-19. HEAD measured:
`e845c2b524ad2e59871e004c51a1386e192a74ab`.

Task: in a /tmp copy pinned to the ORIGINAL pre-guard `expected.json` + original
table, re-run the original 11 selftest cases — all must behave exactly as before
the guard (guard purely additive). Also diff the probe's non-guard code paths
vs HEAD.

Status: **core check PASSES against EX-21's prototype guard** (EX-16's landing
still pending at report time — see §7; the same harness re-runs against the
landed artifact in one command).

## 0. Scratch location deviation (EDQUOT)

`/tmp` and `/dev/shm` are both tmpfs under a per-user quota saturated by the
64-seat wave — `cp` of the 20KB probe returned `Disk quota exceeded` and
truncated files at 0/4096 bytes (observed 07:00–07:01 local, repeated). Scratch
therefore lives OUTSIDE the repo at `~/.cache/kaidoku-arc3l1r1-ex19/`
(removed at seat close; all verdict-relevant outputs are transcribed verbatim
in this artifact). `TMPDIR` was redirected there too so the probe's selftest
fixture repos never touch the saturated tmpfs. No repo path other than this
artifact + the seat report was written.

## 1. Pinning the ORIGINAL pre-guard inputs to HEAD

`git show`/`git cat-file -p` fail in this environment (rc 255/128, empty
stderr); `git hash-object` + `git ls-tree` work and give the same byte-identity
proof:

```
$ git ls-tree HEAD:.ufo/gates/citation-drift/
100644 blob ab3146c092d67b7eb691caed13342d9efd9eef7f	citation-drift-probe.py
100644 blob b08956492e0b5d756ed0f9a0d74d0054ea3600ce	expected.json
100644 blob 1f83c091c9816bc7f522edc1f5d8ade54acd2ecc	pointer-table.json

$ git hash-object <pinned copies>       # == HEAD blobs above
ab3146c092d67b7eb691caed13342d9efd9eef7f
b08956492e0b5d756ed0f9a0d74d0054ea3600ce
1f83c091c9816bc7f522edc1f5d8ade54acd2ecc
```

Pinned copies (sha256), used as "ORIGINAL expected + original table" throughout:

```
3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f  citation-drift-probe.py
4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33  expected.json   (keys: _doc, frozen_run, snapshots, selftest; 11 selftest cases)
738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f  pointer-table.json (31 entries + 4 quoted; 0 `@` targets)
```

## 2. Pre-guard baseline (measured at HEAD, pinned originals)

| # | command (probe `$O`, expected `$O/expected.json`, table `$O/pointer-table.json`) | exit | verdict line | output sha256 |
|---|---|---|---|---|
| B1 | `--selftest --expected $O/expected.json` | 0 | `CLEAN cases=11 passed=11 failed=0 exit=0` | `f052da2e142fc5accc568643957327b2abeebe728f47d0dd09c64e5f3899efca` |
| B2 | `--root $R --rev HEAD --table $O/pointer-table.json --expected $O/expected.json` | 0 | `reported findings=0 exit=0` | `5df5df85c4fcba409f3818d5391622f7bfbde9d13f235e0d614602fe72c5a2a1` |
| B3 | as B2 `--strict` | 0 | `clean findings=0 exit=0` | `ba6e259e84c402d2030e9bf2ec6d04d63125cdd8e7f8a9bacb04f94891d2cd5a` |
| B4 | `--rev 679af5d749f2fd48b9d543e3c99d348d5458f90f` (frozen_run rev), real table | 0 | `reported findings=16 exit=0` | `846bd462057cac0cc14f7f6cb2243e380d994743d30b1ca5c89c4a28f6bf777d` |
| B5 | B2 with table `entries` emptied | 0 | `reported findings=0 exit=0` | `c4fdd7215ce66fb679987d4c8d9a557cd52d1e9cc1b3cc132b3ffb8edfaf20d4` |
| B6 | B2 with one `must_match` tampered | 0 | `reported findings=1 exit=0` (`citation_dead`, no table-integrity class) | `6a834731251ac9ae0ff05a1deb2985e9e12b467e50d3ed624fa7216ea2229c43` |
| B7 | B2 with table path absent | 2 | `could-not-evaluate findings=1 exit=2` (`pointer_table_unreadable`) | `887e2410a29ef8650df353398a5307ca04c8e65666bb66185a1a1d3b2057c0d4` |

B1–B7 were re-run through the harness (`before-matrix/`, 13 runs incl. the
new-pins legs) with identical bytes; per-run exit codes stored in
`before-matrix/*.exit`. Independently cross-confirmed by EX-25's pre-wave logs
(`claims/c2/EX-25/logs/before-sha256.txt` — same three hashes;
`before-selftest.txt` / `before-probe-head.txt` — same verdicts).

### The named debt, demonstrated (not merely cited)

`SCORECARD.md:925-926` (R6): "expected.json pins no digest of
pointer-table.json — probe-exempt by kind, gate-blocking if ever promoted".
Executed evidence for the gap:

- **B4 vs B5**: at the same frozen revision `679af5d`, the real table yields 16
  findings while an emptied table yields `findings=0 exit=0` — the census can be
  laundered by swapping the table, silently, in both probe and `--strict` modes.
- **B6**: a tampered table surfaces only as a *tree* finding (`citation_dead`);
  no class reports the table itself as untrustworthy.

## 3. The check: frozen-run byte-stability (new probe + ORIGINAL pins)

Harness `run-after.sh <new-probe> <new-expected> <new-table>` runs 13 legs and
byte-compares each against the pre-guard baseline (`before-matrix/`):

- **Section A (the seat check)** — new probe + ORIGINAL `expected.json` +
  ORIGINAL table: selftest (11 cases), full run at HEAD, `--strict`, frozen-rev
  run, tampered-table, empty-table, absent-table. **All 7 must be byte-identical
  and same-exit to the pre-guard baseline.**
- Section B — new probe + NEW expected + NEW table: the guard's own legs.
- Section C — OLD probe + NEW expected: cross-version attack (JSON additivity).

### Landed artifact (EX-16, applied 07:15:38–47) — the authoritative result

Landed inputs (stable across two hash reads 8s apart; matches EX-16's own
`after-sha256.txt`):

- probe `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a`
- expected `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7`
  (13 cases; `pointer_table` key; fail-closed)
- table unchanged `738b3a56…`

**Section A (the seat check): `selftest-newprobe-orgexpected` IDENTICAL** —
the original 11 selftest cases print byte-identical output (sha256
`f052da2e…`) at exit 0 with the ORIGINAL pre-guard `expected.json`. The landed
guard is purely additive for the selftest case semantics.

Full-run legs with the ORIGINAL (unpinned) expected read the declared
fail-closed class instead of byte-stability:

```
$ landed --root $R --rev HEAD --table <orig> --expected <orig>
CITATION_DRIFT: pointer_table_unpinned entry=expected.json no pointer-table
                digest pinned in expected.json
CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
```

Exit-code deltas vs baseline: fullrun 0→2, `--strict` 0→2, frozen-rev 0→2,
emptied 0→2, tampered 0→2; absent-table 2→2 (text changed — the unpinned class
fires first); old-probe leg 0→0 (path-line-only diff). Per RV-6 §4.7 and
EX-24 R2 this is the protocol-conformant `unpinned (legacy)` semantics — the
divergence is declared, not silent. The landed selftest pins each fixture
table (`landing-diff.md:81-83`), so the 11 original cases pass under
fail-closed too.

Landed legs (default recipe and injections):

- default recipe (no args): `reported findings=0 exit=0`; `--strict`: `clean findings=0 exit=0`
- `--selftest` (landed expected): `cases=13 passed=13 failed=0 exit=0`
- tampered table via `--table`: `pointer_table_tampered … exit=2` ✓
- absent table via `--table`: `pointer_table_unreadable … exit=2` ✓
- custom legit table via `--table` (empty entries): `pointer_table_tampered
  exit=2` — the unscoped digest contract (RV-8's D2) persists on the landed
  artifact; the registry row must state it
- EDGE 1 (both unreadable): landed = 1 finding (`entry=nope1.json`, expected
  basename); old = 1 finding (`entry=nope2.json`, table basename) — count and
  class preserved; the subject named differs (landed reads expected first)
- EDGE 2 (expected unreadable, table valid): identical to old (1 finding,
  exit 2)

### Pre-landing prototype history (superseded by the landing above)

Prototype inputs (`claims/c2/EX-21/tmp/proto/`), version churn recorded:

- **v1** (07:03): probe.py `776cef6a…`, expected.json `376f9fc5…` (13 cases,
  id `pointer_table_tampered`), skip-on-unpinned.
- **v2** (07:09:58, current): probe.py
  `794e57bc951eabd5f91da82bbba14715561c0f30ad9d402b60c038dd0df4915a`,
  expected.json
  `3f45a2b55e6fc932b0d303b3cf3f58f0e45ecf0b44f1fe53a3c8de49aed04073`
  (13 cases; id `table_tampered`; `table_pin_absent` + `unpinned_legacy` added
  to the CNE set), **fail-closed on unpinned expected**.

**Section A (the seat check, both versions): the original 11 selftest cases
behave byte-identically** — `SELFTEST … cases=11 passed=11 failed=0 exit=0`,
same bytes (`f052da2e…`), under v1 AND v2. The guard never touches the
selftest's case semantics: the harness pins each fixture table in the per-case
expected.json, so even the fail-closed v2 passes the original 11 unchanged.

Full-run legs with the ORIGINAL (unpinned) expected differ by version:

- v1 (skip): 7/7 byte-identical, exits unchanged.
- v2 (fail-closed): every full-run leg flips 0 → 2 —
  `CITATION_DRIFT: table_pin_absent entry=expected.json no table_sha256 pinned;
  fail-closed preflight` / `could-not-evaluate findings=1 exit=2`; absent-table
  stays 2→2 (identical bytes); old-probe leg unchanged (path-line-only diff).

Section B/C measurements (v2; v1 noted where the semantic changed):

| leg | result |
|---|---|
| selftest, NEW expected (13 cases) | `cases=13 passed=13 failed=0 exit=0` |
| full run at HEAD, NEW pins | `reported findings=0 exit=0` (v1: same verdict; both differ from baseline only in the printed table path) |
| tampered table + NEW expected | `CITATION_DRIFT: table_tampered …` / `could-not-evaluate findings=1 exit=2` (v1 id: `pointer_table_tampered`) — declared class, never silent |
| absent table + NEW expected | `could-not-evaluate … exit=2` (`pointer_table_unreadable`, existing class) |
| identical-bytes table + NEW expected | `reported findings=0 exit=0` (digest matches) |
| OLD probe + NEW expected, `--selftest` | `cases=13 passed=11 failed=2 exit=1` — the old probe cannot build the two new cases (`table_tampered`, `table_absent`); probe + expected must be versioned as a pair |
| custom (legit, empty) table + NEW expected | `could-not-evaluate findings=1 exit=2` (`table_tampered`; v1 `pointer_table_tampered`) — the check is **not path-scoped** (RV-8's D2). Once the new expected.json lands, every historical custom-`--table` recipe (r10 practice) becomes exit 2 unless the registry row declares the contract or recipes pin their own digest |
| default recipe (no `--table`/`--expected`, HERE-relative), v2 scratch gate dir | clean → `reported findings=0 exit=0`; tampered at default path → `table_tampered` exit 2; absent at default path → `pointer_table_unreadable` exit 2; `--selftest` → 13/13 exit 0 |

Note: EX-21 revised the prototype while this seat measured it (v1 → v2 at
07:09:58); every number above was re-measured against v2. The authoritative
target remains EX-16's landing.

### The shape discriminator: skip-on-unpinned vs fail-closed

The additive property (section A) depends on the landing's choice for an
*unpinned* expected.json — a fork the wave has left open (EX-24 §5 R2
recommends fail-closed; RV-6 §4.7 reads the protocol's `unpinned (legacy)` as
could-not-evaluate). Both shapes measured:

- **Skip-on-unpinned (EX-21 v1 only; superseded by v2)**: section A 7/7
  byte-identical. Cost: an unpinned expected.json silently disables the guard
  (EX-24's T3: deleting the pin key reads `findings=0 exit=0`).
- **Fail-closed — now the current prototype (EX-21 v2) and EX-24 proto-B**
  (probe sha256 `f7d5128e…`, `table.sha256`-shape pin): selftest 11/11
  IDENTICAL, but every legacy full-run leg flips 0 → 2:

  ```
  $ v2 --root $R --rev HEAD --table <orig> --expected <orig>
  CITATION_DRIFT: table_pin_absent entry=expected.json no table_sha256
                  pinned; fail-closed preflight
  CITATION_DRIFT_VERDICT: could-not-evaluate findings=1 exit=2
  ```

  Deltas vs baseline (v2 exit codes): fullrun 0→2, `--strict` 0→2, frozen-rev
  0→2, emptied 0→2, tampered 0→2; absent-table stays 2→2 (identical bytes);
  old-probe leg stays 0 (path-line-only diff); selftest legs identical. proto-B
  measured the same shape independently (its `table_pin_absent` message names
  the unpinned_legacy class; pinned re-run = `reported findings=0 exit=0`).

**Consequence for this seat's check**: the original 11 selftest cases are
byte-stable under BOTH shapes. Full-run byte-stability with OLD pins holds
under skip-on-unpinned and is *by design* broken under fail-closed: unpinned
inputs read the declared `unpinned_legacy` CNE class (exit 2), which RV-6 §4.7
reads as the protocol-conformant semantics and EX-24 R2 recommends. The
divergence is a declared semantic, not a defect — but the landed registry row
must name which shape is in force.

## 4. Non-guard code paths vs HEAD (landed artifact + prototypes)

Method: top-level AST node source-segment sha256 per node (script
`fingerprint.py`; JSON `before/probe-fingerprint-orig.json` vs
`after/probe-fingerprint-landed.json`; prototype JSONs in `proto-matrix/`,
`proto-v2-matrix/`) + unified diff (`after/probe-landed-vs-orig.diff`).

**Landed: 10 of 13 top-level nodes byte-identical**, including every non-guard
path: `sha256_bytes`, `git_show`, `Tree`, `check_entry`, `root_ok`, `rev_ok`,
`report`, `build_fixture`, `fixture_table`, `main`. (Same node set for v1/v2.)

Changed nodes (all guard-surface; landed line numbers):

| node | orig lines | landed lines | what changed |
|---|---|---|---|
| `Findings` | 59-84 | 67-93 | `pointer_table_tampered` + `pointer_table_unpinned` added to the CNE class set |
| `run_check` | 270-296 | 279-320 | expected read first (unreadable → return); `pointer_table` pin read; unpinned → `pointer_table_unpinned` (fail-closed); table read as bytes; digest → `pointer_table_tampered`; JSON parse → `pointer_table_unreadable` |
| `selftest` | 381-439 | 405-471 | fixture-table digest written into each per-case expected; `table_tampered` = valid-empty table written after pinning; `table_absent` = table removed |

Diff totals: landed 4 hunks, +38 −7 lines (v1 +34 −12; v2 +38 −12), all
inside the three nodes above. No non-guard behavior change is reachable from
the diff.

**Corner-case deltas (EDGE 1/2) on the landed artifact** — `run_check`'s
reorder changes one input class, both `--expected` and `--table` unreadable:

```
OLD probe:    1 finding (pointer_table_unreadable nope2.json)  exit=2
LANDED:       1 finding (pointer_table_unreadable nope1.json)  exit=2
EX-21 v1/v2:  2 findings (nope1 + nope2)                       exit=2
```

Landed preserves count and class; the subject named flips from the table to
the expected file (reads expected first). EDGE 2 (expected unreadable, table
valid) is byte-identical to the old probe. Only v1/v2's 2-finding variant was
a count delta, and the landing does not have it.

## 5. Attacks / refutations attempted

1. **Table-swap laundering (pre-guard)** — B4 vs B5: confirmed the debt class
   (16 findings → 0, exit 0). Verdict: debt real at HEAD.
2. **Tampered-table silent acceptance (pre-guard)** — B6: surfaces as
   `citation_dead` only. Verdict: confirmed.
3. **Guard breaks old pins** (the seat's own falsifier) — LANDED verdict:
   the original 11 selftest cases are **byte-identical** (the seat check
   passes); full-run legs with the unpinned pre-guard expected read the
   declared fail-closed class (`pointer_table_unpinned`, exit 2). Prototypes
   v1: 7/7 identical; v2/landed: selftest identical, unpinned full runs
   declared-CNE. Verdict: refuted for selftest semantics; for unpinned
   full-runs the divergence is declared, not silent.
4. **Non-guard drift smuggled inside the guard diff** — AST fingerprint
   (landed): all 10 non-guard nodes byte-identical; 4 hunks confined to guard
   surface. Verdict: not observed.
5. **Old probe consumes new expected** — selftest exit 1 (2 unknown cases).
   Verdict: constraint confirmed; the pair must move together. (Not a defect
   of the landed design as long as the registry row and recipes say so.)
6. **Custom-table recipes after promotion** — LANDED: exit 2
   `pointer_table_tampered` under the unscoped check. Verdict: RV-8's D2 break
   confirmed on the landed artifact; r10-style custom-table recipes must pin
   their own digest or the row must declare the contract.
7. **Byte-compare asymmetry** — the harness compares same-tag runs; one initial
   "DIVERGED" (`frozenrev-empty-table` vs `emptytable` at different revs) was my
   own harness mismatch, corrected before use (the fixed harness self-comparison
   is all-identical).
8. **Both-unreadable corner (EDGE 1)** — LANDED: 1 finding (`entry=nope1.json`)
   vs old probe's 1 (`entry=nope2.json`): count and class preserved, subject
   name flips. v1/v2 had a 2-finding count delta; the landing does not.
   Verdict: minor, class-preserving.
9. **Fail-closed shape** — LANDED: legacy unpinned full runs flip 0 → 2
   `pointer_table_unpinned`. Verdict: declared semantics (RV-6 §4.7,
   EX-24 R2); the registry row must state it. This is the one full-run
   byte-stability cost of the landing, and it is announced in the finding text
   and expected.json's own note.
10. **Pinned-expected re-run** — LANDED default recipe: `reported findings=0
    exit=0`; `--strict`: `clean findings=0 exit=0`; injections tampered/absent
    → exit 2 typed ids. Verdict: the guard is functional once pinned; the
    defect class closes.

## 6. Reproduction

The re-runnable kit is committed at `claims/c2/EX-19/tools/`: `run-after.sh`
(13-leg harness, self-locating), `fingerprint.py` + `fingerprint-orig.json` +
`fingerprint-landed.json` (AST node diff), `orig/` (pinned pre-guard inputs,
verified == HEAD blobs `ab3146c`/`b089564`/`1f83c09`), `before-matrix/` +
`after/` (all outputs + exits), `matrix-manifest.txt` (exits + output sha256).

```sh
D=.ufo/waves/arc3-loop1-round1/claims/c2/EX-19/tools
OUTDIR=$D/recheck bash $D/run-after.sh \
  .ufo/gates/citation-drift/citation-drift-probe.py \
  .ufo/gates/citation-drift/expected.json \
  .ufo/gates/citation-drift/pointer-table.json
# landed result (re-verified from the kit at close): selftest leg IDENTICAL;
# full-run legs diverge only on unpinned inputs to the declared
# pointer_table_unpinned CNE class
python3 $D/fingerprint.py .ufo/gates/citation-drift/citation-drift-probe.py
# compare against $D/fingerprint-orig.json / fingerprint-landed.json
```

Note: the seat's working scratch (`~/.cache/kaidoku-arc3l1r1-ex19`, used
because /tmp and /dev/shm were quota-exhausted) was removed at close; the kit
above is self-contained.

## 7. EX-16 landing status — LANDED AND VERIFIED

EX-16 applied the guard at 07:15:38–47 (worktree writes only; HEAD unchanged
at `e845c2b`). Landed inputs (stable across two hash reads 8s apart; equal to
EX-16's own `after-sha256.txt`): probe `e2665074…`, expected `ff47bfd6…`,
table `738b3a56…` (unchanged). The landed-artifact run of §3/§4 was performed
against exactly these bytes — the poller detected the change at check 14 and
the after-matrix ran after an 8-second stability check.

Outstanding at close: EX-16's seat report was not yet present at
`.ufo/waves/arc3-loop1-round1/seats/EX-16.md` (their claims dir exists with
`landing-diff.md` and `after-*` evidence). If the files change again, the §6
command re-runs the whole check in under a second. The unscoped `--table`
contract (§3) and the EDGE 1 subject-name flip are the two behaviors the
registry row should state (RV-8/RV-6 own the row text).
