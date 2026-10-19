# SC-3 injection ledger — chain c2, wave `arc3-loop1-round3`

Seat SC-3 (scribe) · chain c2 · task: "injection ledger: the four holes × before ×
after × declared class, one table". Artifact: this file. Scratch: `/var/tmp/sc3`
(never `/tmp`). No git mutations; no writes to `.ufo/gates/custody-pair/` (EX-21's
target) or to any custody path (read-only stat/hash only).

## Identity (rule #14) and method

| role | object | revision | re-derived |
|---|---|---|---|
| BEFORE | `.ufo/gates/custody-pair/custody-pair.py` (round-2 landed, EX-31) | sha256 `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`, 889 L | copied to `/var/tmp/sc3/tool-before/custody-pair.py`, sha re-derived at copy (10:07 −03) |
| AFTER | same path (EX-21, round-3) | sha256 `7cd19c3cfd835c7807d5e60dece1c2592c9df6c319a78deb14469dd6ebe8ab09`, 1155 L | stable ≥120 s (stabilizer: 8 × 15 s identical bytes, declared STABLE 10:15:26 −03) and re-derived at the repo path before (10:16:07) and after (10:16:17) my runs — identical both times |

Measured 2026-10-19 10:07–10:17 −03 (13:07–13:17 Z), Python 3.14.7, uid 1000.
Method: an injection harness (`harness/injections.sh`) plus a sandboxed-HOME
guard harness (`harness/guard-sandbox.sh`), each run twice — once per revision —
on scratch copies. All injection fixtures live under `/var/tmp/sc3`; custody
paths were never opened for writing. Raw outputs: `evidence/before/` and
`evidence/after/` (per-injection `.out` files + `summary.txt` + `guard.log`).

Method defect found and fixed mid-task (recorded for peers): the tool's TZ
selftest case re-invokes `custody-pair.py` **next to itself**, so running the
selftest from a renamed copy (e.g. `7cd19c3c….py`) produces one spurious FAIL
(`can't open file '…/custody-pair.py'`). All numbers below come from a copy
named `custody-pair.py` in its own directory; any seat running a renamed copy
will see that false FAIL.

## The ledger — four holes × before × after × declared class

Tool revision BEFORE = `112d01dc…` (889 L); AFTER = `7cd19c3c…` (1155 L).
Command shapes are scratch fixtures; "R" = a receipt written by the tool itself.

| # | hole (round-2 id) | injection (command shape) | BEFORE — `112d01dc…` | AFTER — `7cd19c3c…` | declared class (AFTER) |
|---|---|---|---|---|---|
| 1 | **D2 — unreadable-path fail-open** (2 facets) | (a) `capture --paths <path under chmod-000 parent> --out R`; then `verify R --live` and `verify R R`. (b) `capture --out - --paths <chmod-000 file>`; `verify R --live` with R captured while readable. | (a) capture `PARTIAL paths=0/1 exit=13`, stanza `EXISTS: no` + `STAT-ERROR: [Errno 13]`; `verify --live` → `PATH …: MATCH compared=0/11`, `SHA256-CONTRACT: 0/0`, `VERDICT: MATCH … exit=0`; pair mode also `MATCH exit=0`. (b) **traceback** `PermissionError` exit 1 at `custody-pair.py:219` via `:168`, **no receipt written**, outside the declared map. | (a) capture `UNEVALUABLE paths=0/1 exit=14`, stanza `EXISTS: no` + `STAT-ERROR` (marker preserved); `verify --live` → `UNEVALUABLE compared=0/11 moved=unevaluable`, `exit=14`; pair mode `UNEVALUABLE exit=14`. (b) capture `UNEVALUABLE paths=1/1 exit=14`, receipt written with `EXISTS: yes` + `TYPE: file` + `READ-ERROR: [Errno 13] …`, no `SHA256`; `verify --live` → `UNEVALUABLE exit=14`. | `14 UNEVALUABLE` — "a path exists but could not be evaluated (EACCES on open, or a stat error other than ENOENT); the receipt is still written, carrying STAT-ERROR/READ-ERROR"; severity `CONTENT-DRIFT > UNEVALUABLE > ABSENT > …`; "verify never reads such a path as MATCH". Tool docstring `:100-107`/`:111`, README `:122`. Classified at `:485-489`, before the both-absent MATCH branch. |
| 2 | **D3 — partial-reference coverage** | `capture --paths <1 path> --out R` (reference carries 1 of the 5 canonical paths); `verify R --live`; then `verify R --live --require-paths 5`. Control: 5-path reference + `--require-paths 5`. | `VERDICT: MATCH paths=1 MATCH=1 exit=0` — the other 4 custody paths unexamined. No coverage flag exists (`--require-paths` / `--cover-default-paths` → argparse `unrecognized arguments`, exit 2). | without flag: unchanged `MATCH 1/1 exit=0` (gate is opt-in by declaration); with `--require-paths 5`: `USAGE: reference covers 1 of the required 5 paths` + `REFERENCE-COVERAGE: 1/5 paths present in reference; unaccounted: <5 canonical>`, `exit=2`. Control 5-of-5 → `MATCH 5/5 exit=0` (no false positive). | `2 USAGE` — "insufficient reference coverage under `--require-paths`"; gate `reference_coverage()` `:591-600`, invoked `:677-685`; `--require-paths N` in `verify --help` ("exit 2 (USAGE) when the reference carries fewer than N paths (D3 coverage gate)"). README `:123`. |
| 3 | **write-guard scope** (VZ-4 A11 finding; adjacent D7 inode alias) | `capture --paths X --out X`; hardlink alias `X'→X` as `--out`; canonical directions under **sandboxed `$HOME`** (G2 `--out ~/.bashrc`; G3 scope includes `~/.profile`). | G1 scoped-as-out: `OK paths=1/1 exit=0`, victim **clobbered** (sha `b3487765…` → `080e0183…`, file replaced by receipt text). G4 hardlink alias: **clobbered**, exit 0. G2/G3 (canonical): refused `USAGE exit=2`, unchanged (guard covered the canonical 5 only; `:564`). | G1–G4 all refused: `USAGE: refusing to write a receipt over a path it measures or a custody path (path or inode)`, `exit=2`; every victim sha byte-identical before/after. Guard = `set(paths) ∪ CUSTODY_PATHS` resolved-path test **plus** `_same_file()` inode arm (`:648-649`). | `2 USAGE` — a refused write. Scope statement on the tool itself: "self-harm guard, not a security boundary" (docstring `:50-53`); README exit `2` row. |
| 4 | **D6 — selftest scratch guard** (2 shapes) | `selftest --scratch <missing dir>`; `selftest --scratch <regular file>`. (Explicit `/tmp/…` base inspected by code, not run — EDQUOT standing rule.) | missing dir: **traceback** `FileNotFoundError` exit 1 at `:630`. Regular file: `NotADirectoryError` exit 1. Explicit `--scratch /tmp/…` bypassed the `/tmp` refusal (`:627` guard carried `and not args.scratch`). | missing dir: `USAGE: scratch base is not a directory: …`, `exit=2`. Regular file: same, `exit=2`. Explicit `/tmp/…` now refused `USAGE: /tmp is excluded scratch (EDQUOT hazard)` regardless of explicitness (`:723-725`); `mkdtemp` `OSError` wrapped to `USAGE` (`:730-733`). Control `selftest` (existing dir) → `CLEAN cases=22 passed=22 failed=0 exit=0`. | `2 USAGE` — "unusable selftest scratch dir" / "bad arguments"; `:726-733`, README `:123`, `selftest --help` states "a missing / non-directory / `/tmp` base is a USAGE exit 2". |

### Controls

- Selftest case count: BEFORE `CLEAN cases=15 passed=15 failed=0 exit=0`;
  AFTER `CLEAN cases=22 passed=22 failed=0 exit=0` (7 new fixtures:
  `unreadable-path-is-unevaluable`, `unevaluable-never-matches`,
  `parsed-unevaluable-reference-never-matches`,
  `partial-reference-require-paths-gate`, `refuses-to-write-over-scoped-path`,
  `selftest-missing-scratch-usage-exit`, `refuses-write-through-hardlink-alias`).
- All four holes' fixtures are covered by the new selftest cases except the
  hardlink-alias case name difference (`refuses-write-through-hardlink-alias`) —
  both names are listed in `evidence/after/selftest-cases.txt` from the final bytes.
- BEFORE runs used HEAD `c07af80f…` (receipt header, `evidence/before/receipt-d2a-eacces-before.txt`).

## Named residuals (not hidden, not claimed as closed)

- **R1 — pure-ENOENT both-sides still reads `MATCH` exit 0** (ghost path: capture
  `PARTIAL 0/1 exit 13`; `verify --live` → `MATCH 1/1 exit 0`, `compared=0/11`,
  unchanged before/after). This is by declaration, not by omission: the AFTER
  map defines UNEVALUABLE as "a stat error **other than ENOENT**"; a genuinely
  absent path is the declared `ABSENT` class on capture (exit 13) and
  absence-agreement on verify. The EACCES facet (the fail-open named by D2) is
  closed; this ENOENT case is a different, declared status.
- **R2 — the coverage gate is opt-in.** Without `--require-paths N` a 1-of-5
  receipt still verifies `exit 0` (code comment: "falsy (None/0) = no gate — the
  declared default; opt-in by design"). Any gate keyed on `verify` exit 0 for a
  canonical-set claim must pass the flag; the declaration lives in `--help` and
  README.
- **R3 — write guard remains a self-harm guard.** The inode arm closes the
  pre-existing-alias case (G4); a TOCTOU alias created between the guard check
  and the write is inherent and declared out of scope on the tool itself
  (docstring `:50-53`). The D7 alias-evasion class is closed for the measured
  shape.
- **R4 — README churn after tool stabilization.** README sha moved
  `83f07f83…` (10:15) → `f30df42e…` (10:16:00) while the tool stayed
  `7cd19c3c…`; citations above are to the README bytes at 10:16 −03. If the
  parent lands a later README revision, the class *semantics* (14 UNEVALUABLE /
  2 USAGE) must be re-checked against the landed table, not assumed.

## Evidence index (each pointer is a file in `claims/c2/SC-3/`)

- Harness: `harness/injections.sh` (I0–I7), `harness/guard-sandbox.sh` (G1–G4).
- BEFORE: `evidence/before/summary.txt`;
  `i1a/i1b` (D2a), `i2a/i2b` (ghost), `i3a/i3b/i3c` (D2b crash + control),
  `i4a–i4d` (D3), `i5a/i5b` (write-guard + sha delta), `i6a/i6b` (D6 + control),
  `i7a–i7c` (CLI surface), `guard.log` (G1–G4), `receipt-d2a-eacces-before.txt`,
  `receipt-d2b-ghost-before.txt`, `receipt-d3-1of5-before.txt`.
- AFTER: `evidence/after/summary.txt`; same matrix files; plus
  `i1c-pair-verify-eacces.out` (receipt-vs-receipt mode),
  `receipt-d2a-eacces-after.txt`, `receipt-d2c-readerror-after.txt`,
  `declared-map.txt` (docstring exit map at final bytes),
  `selftest-cases.txt`, `guard.log`.
- Cross-corroboration: peers measured the same before-state independently —
  EX-22 `seats/EX-22.md` §§1–3 (same four holes, plus receipt-vs-receipt and
  file-as-scratch shapes), RV-5 `claims/c2/RV-5/before-112d01dc/` (before
  battery), CR-4 `claims/c2/CR-4/attack-battery.sh` (T0 control = G1).

## Notes for the parent / reviewers

- The ledger's "declared class" column cites the AFTER revision only. In the
  BEFORE revision the three defect classes were **outside** the declared map
  (`exit 1` tracebacks) or inside it as wrong-but-passing classes (`MATCH` at
  exit 0, `OK` at exit 0) — that asymmetry is the defect, per the round-2
  verdict's wording.
- The claim's other clauses (live pre/post pair MATCH 5/5 captured by the
  revised tool; registry row + README in the same commit; v1 receipts
  sha256-verifiable; command A unchanged) are outside this ledger's scope and
  are measured by EX-21/EX-29/RV-8/RV-9/VZ-2 artifacts.