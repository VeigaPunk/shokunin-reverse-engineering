# EX-17 tamper-injection results — C2 citation-drift frozen-run guard

Seat EX-17, chain c2, wave arc3-loop1-round1, 2026-10-19. Executor artifact for the
frozen claim (`claims-frozen.md:46-54`): a tampered or absent `pointer-table.json`
must yield the declared preflight could-not-evaluate class (exit 2), never silent
findings. HEAD for all runs: `e845c2b524ad2e59871e004c51a1386e192a74ab`.

Verdict in one line: **4/4 injections exit 2 against the landed instrument; the
before-state's silent false-clean class (a valid-JSON tamper graded `findings=0
exit=0` with a verdict line byte-identical to the honest run) is closed.**

## 1. Instrument identity

| artifact | before (HEAD, pre-EX-16) | landed (EX-16, post-landing) |
|---|---|---|
| citation-drift-probe.py | `3067621ac44d6a153f45076c947926b56e3f34fbd4a907458273d97d1a47803f` | `e2665074a685ca65966f291f98b5e264b15c67827982811a24dc73b16497a36a` |
| expected.json | `4e28ba908bcd8e71586d0f8e376b1343bd7e305144f48c484f8ef788d36a2e33` | `ff47bfd60b383c22c0897e8c89081dd738f67d7f28904292c47f5d09e4173ba7` |
| pointer-table.json | `738b3a569fb7dc96e1097de0121a19d86856fb8de43030a8cba0394428dd6e3f` | unchanged `738b3a56…` |

- Landing caught by this seat's poller at 10:15:31Z (first bytes `4e89502c…`/`07701885…`),
  revised by ~10:18Z; final hashes re-verified stable at 10:20:14Z
  (`logs/poll-ex16.log`).
- **Independent reproduction**: this seat hand-applied PL-2's patch text
  (`claims/c2/PL-2/frozen-run-guard.patch.md`) to its own lab copy; the result is
  **byte-identical** to the landed instrument (both hashes above), reproducing
  PL-2's declared prototype values exactly. `diff landed vs reproduction: empty`.

## 2. Method

The probe+table+expected were rsync'd to a scratch lab and all tampering was done
on lab copies only (rule: only EX-16 may write the real target; the repo tree was
read via `git show`). Each corruption is a **single-byte flip** applied by script
(`gen-i1.py`, `gen-i2.py`, `gen-i4.py`), recorded with offset, before/after byte,
and sha256 of the tampered file.

Scratch location: `/dev/shm/ex17-c2-tamper` — **deviation from the `/tmp` rule**,
forced by the host's exhausted per-UID tmpfs quota on `/tmp` (`usrquota`; even a
1-byte write fails EDQUOT — `logs/scratch-location-evidence.txt`). Same hazard and
same fallback as seats EX-02 (`claims/c1/EX-02/install-receipt.txt:116-119`),
EX-14 (`claims/c1/EX-14/attack-manifest-integrity.sh:8-14`) and EX-15
(`claims/c1/EX-15/containment.md:22`, "per-UID 12.1G tmpfs quota saturated").
Cleaned up after the run.

## 3. Injections — before (HEAD) vs after (landed)

| id | corruption | byte flip | tampered sha256 | before | after (landed) |
|---|---|---|---|---|---|
| I1 | structural: `"entries"` key quote → `!` (invalid JSON) | off 917, `0x22`→`0x21` | `3423f1d1…` | exit 2, `pointer_table_unreadable` | exit 2, `pointer_table_tampered` |
| I2 | semantic: `"line": 59` → `69` (valid JSON, wrong citation) | off 1041, `0x35`→`0x36` | `c0b0792e…` | default **exit 0** (`reported findings=1`); `--strict` exit 1 — never 2 | exit 2, `pointer_table_tampered` (both modes) |
| I3 | absent table | — | — | exit 2, `pointer_table_unreadable` | exit 2, `pointer_table_unreadable` |
| I4 | semantic: `"entries"`→`"entrieX"` (valid JSON; 31 of 35 checks silently skipped) | off 924, `0x73`→`0x58` | `613a7873…` | **exit 0, `findings=0` — SILENT FALSE-CLEAN** | exit 2, `pointer_table_tampered` (both modes) |

Baseline (I0) both phases: pristine table → `findings=0 exit=0` (default
`reported`/strict `clean`), so the after-runs are not masking pre-existing findings.

### The silent class, byte-for-byte (before-state)

I4's default verdict line vs the honest I0-clean line:

```
CITATION_DRIFT_VERDICT: reported findings=0 exit=0     (I0-clean, honest)
CITATION_DRIFT_VERDICT: reported findings=0 exit=0     (I4-keyrename, tampered)
```

`cmp` of the two extracted lines: identical. Before the guard, an operator could
not distinguish the tampered run from the honest run. I2 additionally shows
**misattribution**: the tamper is reported as `citation_dead SCORECARD.md:69`,
blaming the citing file for a table edit.

Raw logs: `before.txt` (8 runs), `landed.txt` (8 runs) in this directory.

## 4. Selftest

- before: `CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0`
- after (landed): `… cases=13 passed=13 failed=0 exit=0`, with the two new rows
  `table_tampered → exit 2, pointer_table_tampered` and
  `table_absent → exit 2, pointer_table_unreadable`.
- Host hazard: `/tmp` quota exhaustion can break the selftest's temp fixtures
  mid-run (leftover `/tmp/citation-drift-selftest-*` dirs from crashed runs were
  observed). Runs above used `TMPDIR=/dev/shm/ex17-c2-tamper/tmp`; an explicit
  `TMPDIR=/tmp` run also passed at 10:10Z when /tmp briefly had room. Record the
  TMPDIR when citing selftest results on this host.

## 5. Attacks / refutations attempted

- **A1 fail-closed check** — landed probe + an *unpinned* expected (pre-landing
  `expected.json`): exit 2, `pointer_table_unpinned`. A baseline that pins nothing
  cannot silently skip the guard.
- **A2 alternative guard shape** — RV-6's prototype
  (`claims/c2/RV-6/proto-test/probe.py`, sha `776cef6a…`) with its *unpinned*
  `expected-as-shipped.json` and the I4 tampered table: `reported findings=0
  exit=0` — the fail-open variant still passes a tampered table silently. Verdict:
  only the fail-closed shape (PL-2's, landed) closes the class. (RV-6's variant is
  not the landed instrument; recorded as design evidence.)
- **Cross-check vs EX-16's independent injections**
  (`claims/c2/EX-16/after-injections.txt`, cases A-L): tampered/whitespace-append/
  absent/unpinned/malformed/type-confused all exit 2; byte-identical copy and
  custom-table-with-custom-pin run clean. Consistent with I1-I4 here;
  `claims/c2/EX-16/after-sha256.txt` matches the landed hashes measured above.

## 6. Gaps / observations

- EX-16's seat report was absent during my measurement window (written 10:20Z,
  after my injections) — the landing itself is verified by bytes and hashes, not
  by their report. `seats/EX-16.md` exists as of this artifact's write time.
- The landed `expected.json` hash equals PL-2's scratch value `ff47bfd6…`, i.e.
  the trailing-newline caveat in PL-2's patch note did not materialize; landed
  bytes are the exact validated prototype.
- Untracked `__pycache__` dirs under `.ufo/gates/` (visible in EX-16's
  `git-status.txt`) are a side effect of some seat importing instruments as
  modules; not created by this seat (my `py_compile` ran on the lab copy only).
  Parent may want them removed before integration.
