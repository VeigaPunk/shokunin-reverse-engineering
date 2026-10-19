# EX-22 — early smoke check of EX-21's IN-FLIGHT revision (not a verdict on the landing)

**Status of this file: advisory, single-instant, and superseded by EX-21's own evidence.**
While this seat was re-deriving its BEFORE-state identity, EX-21 (chain c2's designated
implementer) began writing `.ufo/gates/custody-pair/custody-pair.py`. The worktree diverged
from HEAD at **2026-10-19T13:09:24Z** and kept moving:

| instant (UTC) | worktree sha256 of `custody-pair.py` | note |
|---|---|---|
| ≤13:08:0x | `112d01dc…` (== HEAD blob `f3abeb2`) | the BEFORE rev this seat measured (§ baseline.md) |
| 13:09:24Z | `460a01f0…` | first divergent read |
| 13:09:29Z | blob `7388108` (diff index) | moved again |
| 13:09:39Z | `9860149d94371dc49e3b3c1b96d49e0092118c0aa8957ad3a6f1e0f02fc24a7f` | **snapshot tested below** (frozen into `/var/tmp/ex22-after/tool/`) |
| 13:10:06Z | `08fb6833c87d10a07e90ea84186993e95a6b81b853e9ae74045b2b3c2a3618e2` | moved again after the test |

So: **these numbers describe one instant of a file under active edit.** They are an early
signal for the parent, not the round's after-state measurement, which belongs to EX-21's
evidence and the RV/VZ seats' verdicts. Test fixture: `/var/tmp/ex22-after` (scratch), the
measured snapshot copied to `/var/tmp/ex22-after/tool/`; snapshot re-hashed before and after
the run — unchanged (`transcripts-after/s0-…`, `s1-…`). No repo file was written except this
seat's artifacts; the 5 custody paths were verified untouched after the run
(`f2-verify-vs-pre`: `SHA256-CONTRACT: 5/5`, `VERDICT: MATCH paths=5 exit=0`).

## Results at snapshot `9860149d…` (frozen 13:09:39Z, run 13:09:44–13:10:16Z)

| probe | result at the snapshot | vs the BEFORE rev (§ baseline.md) |
|---|---|---|
| (a) EACCES (dir 000) → `verify --live` | `UNEVALUABLE … moved=unevaluable`, **exit 14** | was `MATCH exit 0` → **fail-open closed in verify** |
| (a) → `verify` receipt-vs-receipt | `UNEVALUABLE`, **exit 14** | was `MATCH exit 0` → closed in both modes |
| (a) → `capture` | exit **13** (`PARTIAL paths=0/1`), receipt `EXISTS: no` + `STAT-ERROR` | docstring promises 14 — capture-side class not yet landed |
| (a′) file 000 (statically readable, unreadable bytes) → `capture` | **no traceback**; stanza `EXISTS: yes` `TYPE: file` `READ-ERROR: …`; but `CUSTODY_PAIR_CAPTURE: OK paths=1/1 exit=0` | was a traceback; the receipt field landed, the exit class did not |
| (a′) → `verify --live` | `UNEVALUABLE`, **exit 14** | was a traceback exit 1 → closed |
| E2 format-tag mislabel (baseline §5) | an EACCES-only receipt now prints `A format: v2` | closed at the snapshot |
| (b) 1-of-5 receipt vs live, no flag | `VERDICT: MATCH … exit=0` | unchanged — still open |
| (b) `--require-paths 5` | `error: unrecognized arguments: --require-paths`, exit 2 | flag not yet registered (docstring describes it) |
| (c) `--paths X --out X` | **clobbered again**: X = 17 B canary → receipt `40a480a2…`, `OK paths=1/1 exit=0` | unchanged — write-guard scope not landed |
| (c′) hardlink alias as `--out` | allowed; shared inode rewritten, both names now `f8bc392d…` (the receipt) | inode arm not landed |
| (d) `selftest --scratch <missing dir>` | raw `FileNotFoundError` traceback, exit 1 | unchanged |
| (d) `selftest --scratch <regular file>` | raw `NotADirectoryError` traceback, exit 1 | unchanged |
| (e) `selftest` happy path | `CLEAN cases=15 passed=15 failed=0 exit=0` | still 15, not yet ≥17 |

Correction for honesty: the first `d3`/`d4` rows in `transcripts-after/` are invalid — I
pointed `--scratch` at a directory that did not exist in *that* scratch root, so they are a
second instance of the (d) crash, not a selftest result; the re-run against an existing
directory is the table's row (e) (`d3-selftest-happy.txt`, `case lines: 15`).

## What this means for the round

At that instant the revision was **half-hardened**: the verify-side UNEVALUABLE class
(exit 14, checked before the both-absent MATCH branch) and the `READ-ERROR` receipt field
were in, while the capture-side exit classes, `--require-paths`, the write-guard scope and
the scratch guard were not, and the selftest still counted 15. The claim's falsifiable line
("the four injections reproduce as their declared classes … selftest 15 → ≥17") is therefore
**not yet satisfied at `9860149d…`** — expected, since the file was still being written.
Re-measure at the landing commit's revision; do not treat this table as EX-21's after-state.

Transcripts: `transcripts-after/` (same one-command-per-file format as the baseline's).
Snapshot hash file: `transcripts-after/s0-snapshot-hash.txt` == `s1-…` (unchanged during run).