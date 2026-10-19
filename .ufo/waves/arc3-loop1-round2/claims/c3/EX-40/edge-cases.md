# EX-40 — custody receipt v2 edge cases: missing / unreadable / symlinked paths

Seat EX-40 · chain c3 · role executor · wave `arc3-loop1-round2` · 2026-10-19.
Task (seat line): edge cases — missing path, unreadable path, symlinked path in
the custody set — **against SCRATCH fixtures only**; each behavior declared
(exit class).

Tool under test (the chain's real target, read-only for this seat):
`.ufo/gates/custody-pair/custody-pair.py`, sha256
`112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
(889 lines, 39 157 B, mtime 2026-10-19 09:05:19 -03; EX-31's revision, base of
this artifact's patch). The tool was revised twice mid-seat (38 891 B @09:03 →
39 157 B @09:05); every measurement below was re-run against `112d01dc…` after
the second revision, and the three headline probes reproduce identically.

Scratch root: `/var/tmp/ex40/` (`/tmp` is excluded repo-wide — EDQUOT; the
fixtures are rebuilt deterministically by `fixtures.sh`, the oracle by
`receipt-v2-scratch.py`, both in this artifact dir). **No custody path was
written, renamed or opened for writing by this seat**; the 5 real paths were
only lstat'ed/hashed read-only (all five are regular files, mode 600/644 — the
symlink cases below are robustness shapes, not live hazards).

## 1. Declared behavior table (exit class per shape)

Convention: the tool's own ladder (0 MATCH / 10 CONTENT-DRIFT / 11 REWRITE-DRIFT
/ 12 METADATA-DRIFT / 13 ABSENT / 2 USAGE / 3 SELFTEST-FAIL,
`custody-pair.py:119-142`). This artifact adds **14 UNEVALUABLE** — a path that
exists but could not be evaluated — with severity order
`CONTENT-DRIFT(5) > UNEVALUABLE(4) > ABSENT(3) > REWRITE-DRIFT(2) > METADATA-DRIFT(1) > MATCH(0)`:
an unread path is a weaker statement than a measured drift but a **stronger
alarm than a definitive absence** (the entry is there; its bytes are hidden).

| # | shape (fixture) | landed tool `112d01dc…` — measured | declared class (this artifact) | patch § |
|---|---|---|---|---|
| 1 | regular readable (`good.txt`) | exit 0 · SHA256+INODE+CTIME_NS | exit 0 | — |
| 2 | **missing** (`missing.txt`) | exit **13** `ABSENT`, receipt written (`EXISTS: no`) | exit 13 `ABSENT` (tool-declared; confirmed) | — |
| 3 | **unreadable** — regular, EACCES on open (`unreadable.txt`, mode 000) | **crash**: `PermissionError` traceback, exit **1** (not in the declared table), **no receipt written at all** — even mixed with healthy paths | exit **14** `UNEVALUABLE`, receipt still written, path carries `READ-ERROR:` | P1 |
| 4 | **unreadable** — EACCES on path resolution (parent dir mode 000, `blocked_dir/inner.txt`) | capture exit **13** (`EXISTS: no` + `STAT-ERROR: [Errno 13]`), then `verify --live` → **`VERDICT: MATCH exit 0`** — a fail-open on a path that was never evaluated | exit **14** `UNEVALUABLE` in capture and in verify; **never** `MATCH` | P1 |
| 5 | **symlink → regular** (`link_ok.txt`) | exit 0 · `TYPE: symlink` · `SYMLINK-TARGET: good.txt` · `SHA256` = sha256 of the **link text** (0-copy, no follow) | exit 0 (declared); link identity recorded; verify catches a link swap — measured: file replaced by symlink → **10 `CONTENT-DRIFT`** | — |
| 6 | **dangling symlink** (`link_dangling.txt`) | exit 0 · `TYPE: symlink` · sha256 of link text · counted **present 1/1** | exit 0 (declared: "present" = the *entry* exists, not that the byte source resolves) | residual R1 |
| 7 | symlink **cycle** (`link_loop_a ↔ link_loop_b`) | exit 0 (lstat only; never followed → no `ELOOP`) | exit 0 (declared) | — |
| 8 | symlink → **directory** (`link_dir`) | exit 0 · `TYPE: symlink` | exit 0 (declared) | — |
| 9 | symlink → **device** (`link_devnull → /dev/null`) | exit 0 · `TYPE: symlink` | exit 0 (declared) — note the naive alternative: `sha256sum` prints `e3b0c442…` rc 0, a **valid-looking fake** | — |
| 10 | **fifo** (`pipe.fifo`) | exit 0 · `TYPE: other` · **never opened** (no hang) | exit 0 (declared: non-regular recorded by identity, not hashed) | — |
| 11 | **directory** (`dir_target`) | exit 0 · `TYPE: other` | exit 0 (declared) | — |

Measured receipts for shapes 1-11 (verbatim, one run each):
`real-tool-matrix-before.txt`. Oracle cross-check (same shapes, declared status
nouns): `matrix-run.txt` → 12/12 `MATRIX: PASS`.

Verify-side classes (same tool, fixture pairs in `/var/tmp/ex40/vtest`,
`real-tool-verify-edges.txt`): missing → **13 `ABSENT`** · dangling-symlink swap
→ **10 `CONTENT-DRIFT`** · same-content rewrite with new inode → **11
`REWRITE-DRIFT` (`moved=inode,mtime_ns`)** · chmod-000-then-verify → **crash,
exit 1** (same root cause as shape 3; fixed by P1).

Why the nanosecond pins matter (measured, `/var/tmp/ex40/ctime_test` run in
`real-tool-matrix-before.txt` context): an in-place same-content rewrite moves
`ctime_ns` by **+42 720 ns** while the second-resolution ctime render is
**byte-identical** — a second-resolution `CTIME_UTC` pin would be blind to a
same-second rewrite. The tool pins `CTIME_NS` (`custody-pair.py:210-211`,
`:281`): declared correct. Same measurement: a temp+rename replace moves the
inode (separate detector, covered by the tool's selftest cases 2-3).

Why non-regular must never be opened (measured): `timeout 3 sha256sum pipe.fifo`
→ **rc 124** (hangs; a custody capture that opened a fifo would wedge the
round's pre-pair); `sha256sum` through `link_devnull` → exit 0 with the
empty-string digest. The tool's `lstat → islink/isfile` partition
(`:212-221`) avoids both; declared correct.

## 2. Before → after (this seat's measurement of the chain's claim)

Command shape: `TOOL=<tool> bash edge-matrix-real.sh` (11 capture shapes + 2
type assertions + an aggregate run + a verify fail-closed probe = 17 checks).

```
BEFORE  (landed tool 112d01dc…):  real-tool-matrix-before.txt
        MATRIX: FAIL pass=11 fail=6
        FAIL capture unreadable.txt          exit=1  (declared 14)   ← crash
        FAIL capture blocked_dir/inner.txt   exit=13 (declared 14)
        FAIL aggregate good+unreadable       exit=1  (declared 14); receipt stanzas=0
        FAIL verify unevaluable-vs-live      exit=0  (declared 14)
        FAIL verify printed MATCH (fail-open)

AFTER   (patch P1 applied to a scratch copy; sha256 4aedb0307f8313e7…):
        patched-tool-matrix-after.txt      MATRIX: PASS pass=17 fail=0
        patched-selftest.txt               CUSTODY_PAIR_SELFTEST: CLEAN cases=17 passed=17 failed=0 exit=0
                                           (15 original cases + 2 new; original 15 unchanged)
```

The patch applies cleanly to a fresh copy of the landed bytes
(`patch -p4 --dry-run` clean; result sha `4aedb030…` reproduced independently in
`/var/tmp/ex40/applytest/`).

## 3. Proposed change (patch text)

`proposed-edge-classes.patch` (unified diff against `112d01dc…`, 167 lines, 11
hunks — apply from repo root with `patch -p1`); companion explanation
`proposed-edge-classes.patch.md`; hunk generator `gen-patch.py` (exact-string
anchors — refuses to "apply" if the base revision moved). **Not applied by this
seat**: only EX-31 may write `.ufo/gates/custody-pair/` this round.

## 4. Attacks / refutations attempted

- **A1 "naive sha256 tooling is equivalent for these shapes"** — REFUTED:
  fifo → hang (rc 124); `/dev/null`-via-link → rc 0 with a valid-looking digest.
- **A2 "lstat-not-follow breaks custody (a legitimate symlinked config would be
  mis-hashed)"** — ACCEPTED AS DECLARED BEHAVIOR, with the consequence measured:
  the receipt hashes the link *text* and names `SYMLINK-TARGET`, so a swap is a
  first-class custody event (verify: 10 `CONTENT-DRIFT`). Residual R1 (dangling
  reads present) named, not papered over.
- **A3 "second-resolution ctime is enough for the rewrite class"** — REFUTED by
  measurement (§1): ns pins are load-bearing; the landed tool pins ns → declared
  correct.
- **A4 "one bad path degrades gracefully"** — REFUTED for the landed bytes: one
  unreadable path aborts the whole capture (no partial receipt, no sidecar).
- **A5 "verify fails closed on unevaluable paths"** — REFUTED: `MATCH exit 0`
  (§1 shape 4). Fixed by P1 (after: exit 14, no MATCH printed).
- **A6 "the fixtures themselves could be wrong"** — CAUGHT AND FIXED mid-seat:
  the first cycle fixture was dangling (`link_loop_a -> loop_b`); corrected to a
  real 2-cycle, which changed the oracle's class for that shape from
  `SYMLINK_DANGLING` to `SYMLINK_LOOP`. The first harness run was also bogus
  (relative oracle path after `cd`) and was fixed and re-run (both are visible in
  the artifact history: `matrix-run.txt` is the post-fix run).
- **A7 "mode-000 is the wrong probe for unreadable"** — PARTIALLY TRUE, stated:
  mode bits do not block root, so the declared class is EACCES-derived, not
  mode-derived; the new selftest cases guard on `os.geteuid() == 0`. Shape 4
  (parent-dir EACCES) is the root-robust variant and is covered separately.
- **A8 "the patch could break the tool's own contract"** — TESTED: patched copy
  selftest 17/17 CLEAN, the original 15 cases unchanged, and the live 5-path
  capture/verify behavior is untouched by P1 (no code path for regular readable
  files changed).

## 5. Residuals (named, not fixed here)

- **R1 dangling symlink reads `present`, exit 0** (`custody-pair.py:212-216`):
  the receipt is honest (`TYPE: symlink` + `SYMLINK-TARGET`) but has no
  `DANGLING:` marker, and `# paths: N present: M` counts the entry. Optional
  follow-up, not in the patch.
- **R2 patch base**: `112d01dc…` only. If EX-31 revises again, re-run
  `gen-patch.py` (anchors asserted) before applying.
- **R3 root caveat**: as in A7.
- **R4 vocabulary**: this artifact's oracle uses `UNREADABLE` where the tool
  names `UNEVALUABLE`; the patch adopts the tool's vocabulary.
- **R5** `/tmp` scratch exclusion is already implemented in the tool
  (`default_scratch`, `warn_if_tmp`) — verified present, not a residual.

## 6. Evidence index (this artifact dir)

| file | what |
|---|---|
| `fixtures.sh` | deterministic rebuild of `/var/tmp/ex40/fix` (scratch only) |
| `receipt-v2-scratch.py`, `edge-matrix.sh`, `matrix-run.txt` | declared-class oracle + 12/12 matrix |
| `edge-matrix-real.sh`, `real-tool-matrix-before.txt`, `patched-tool-matrix-after.txt` | the 17-check matrix against the real tool, before/after P1 |
| `real-tool-unreadable.txt` | the crash traceback + the no-receipt result (aggregate run) |
| `real-tool-silent-match-probe.txt` | the exists-but-EACCES → `MATCH` fail-open reproduction |
| `real-tool-verify-edges.txt` | verify-side classes: 13 / 10 / 11 / crash-on-14 |
| `real-tool-selftest.txt` | landed tool selftest CLEAN 15/15 |
| `patched-selftest.txt` | patched copy selftest CLEAN 17/17 |
| `proposed-edge-classes.patch` (+ `.patch.md`), `gen-patch.py` | the proposed change and its generator |
| `IDENTITY.txt` | sha256 of every artifact above + tool sha at measurement time |
