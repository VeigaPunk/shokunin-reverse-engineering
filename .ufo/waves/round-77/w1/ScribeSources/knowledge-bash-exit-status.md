source: own-work — `tools/round-77/prefile-receipt.py`, with receipts `.ufo/waves/round-77/pre/c2-at-base.json` (rev `188562d4`, `arms_ok 4` of 6) and its 13-case selftest `pre/selftest-c2.json`; S290 grounds the exit-status binding; the outside population is `corpus/lessons/round-76-verifier-spotcheck.md` section 6 items 3-4
verified-at: 2026-11-04
recheck: `python3 -I -B tools/round-77/prefile-receipt.py --root . --rev <rev> --work <scratch> --battery --json-out <receipt>` (`arms_ok`, `arms_total`); `--check-receipt <file> [--expect-rev <rev>]`

# A gate verdict nobody retained is a verdict nobody can re-check

Round 76's filing report said "the tree is clean and `prefile-check.sh` passes at that revision". No output of
`tools/round-29/prefile-check.sh` was retained under `.ufo/waves/round-76/`, and the round's `gate-at-tip.txt`
carried a disclosures block, `required_failed: []` and its `rev` — but no wrapper exit. The next reader has the
sentence and nothing to run it against.

## Gate

| field | value |
|---|---|
| row | S290 — GNU Bash Reference Manual, Edition 5.3, `docs`, tier A, `mined` |
| URL | https://www.gnu.org/software/bash/manual/bash.html |
| accessed | 2026-11-04 |
| snapshot | `.ufo/waves/round-77/l1/sources/page-721dd237.html`, 1 040 954 B, sha256 `78d0eefbe60cfe7345ffdafede7294f055b04e53bd520360ff699b24f81e2b4b` |
| located quote | "Bash itself returns the exit status of the last command" — section 3.7.5 Exit Status (heading line 4392), quote line 4435, 10 words, contiguous rendered text (not composite); the sentence continues at lines 4436-4437 with the syntax-error exception |
| consumer | `tools/round-77/prefile-receipt.py` line 114, `"exit": proc.returncode` |

## What the receipt binds

`prefile-receipt.py` runs the round-29 gate as a child under exactly four environment keys (`PATH`, `HOME`,
`TMPDIR`, `LANG`, with `TMPDIR` and `HOME` pinned inside the private work root), then writes a receipt carrying:

| field | what it is | how `--check-receipt` re-derives it |
|---|---|---|
| `argv` | the exact command (`bash <lane>/tools/round-29/prefile-check.sh <lane>`) | must name the gate script; a string list, no shell |
| `rev` | the gate tree's `HEAD` | compared to `--expect-rev` when given |
| `exit` | the child's exit status | must be an integer (never a string, never a bool) |
| `prefile_line` | the last `prefile: PASS` or `prefile: FAIL` line | must equal the verdict line recomputed from `stdout` |
| `stdout` / `stdout_sha256` | the child's stdout and its digest | digest recomputed over `stdout` |
| `passed` | `exit == 0 and verdict == PASS` | recomputed from `exit` and the verdict token |
| `env_keys` | the child's non-empty keys | must equal the four-key allowlist |

A *failing* gate is a valid receipt: `exit 1` with `prefile: FAIL` passes `--check-receipt` — the checker binds
the record's honesty, not the tree's cleanliness.

## The battery

Six arms at a measured revision:

1. `clone-run` — a `git clone --shared` of the lane at `--rev` runs the gate clean; the receipt it writes passes
   `--check-receipt`.
2. `record-receipt` — the record's own filing receipt (`.ufo/waves/round-77/l1/scores/prefile-at-filing.json`)
   exists at `--rev` and passes with `exit 0`.
3. `gate-exits` — every `l1/scores/gate-*` receipt in the newest round directory at `--rev` carries its exit.
4-6. `red-no-exit`, `red-verdict`, `red-rev` — doctored receipts are refused, each by its named clause.

## Why the exit belongs in the receipt

S290 (GNU Bash manual, section 3.7.5) documents that a shell returns the exit status of the last command, a
syntax error being the stated exception. That is what makes `exit` a faithful field: the wrapper does not
interpret the gate, it records what the shell returned. It also bounds the claim — a bound exit is the gate's
own verdict, never a re-derivation of the gate's checks.

## Limits

- `git clone --shared` reads the lane and writes only the clone; the lane tree is untouched, and the gate itself
  runs `GIT_OPTIONAL_LOCKS=0 git status`, which refreshes nothing.
- The newest-round-dir rule means the `gate-exits` arm follows the lane's live round; a round with no gate
  receipts fails the arm rather than passing vacuously.
- The receipt binds bytes, not provenance: a receipt produced by another tool and copied in could satisfy the
  field checks. The claim is record honesty, not authenticity.

## Round-77 measurement

Base `188562d4`: `arms_ok 4` of 6 — `record-receipt` absent and three round-76 gate receipts lacking `exit`;
`clone-run` passes, so the gate itself is not the defect.
