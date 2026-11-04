# ExecBinder — round 80, w1

Candidate `tools/round-80/pointer-bind.py` (delivered at
`.ufo/waves/round-80/w1/ExecBinder/pointer-bind.py`, 755 lines, sha256
`b01e7b494acd88caed037a473824ab0b0cb524b520659114c4d46234a1ff8f8a`), its selftest
log and the live receipts. No lane production file was touched; every write is
under `.ufo/waves/round-80/w1/ExecBinder/` plus this report.

## Change

1. **Exact-token matching.** `bind()` now requires *every* occurrence of every
   declared token in the pointed slice to be delimited on both sides — start/end
   of the slice, or a character outside `[A-Za-z0-9._-]`. A non-delimited
   occurrence refuses and names the maximal `[A-Za-z0-9._-@]` run around it, so
   `rea-agents@6.7.0` against `"rea-agents@6.7.05"` refuses with
   `token 'rea-agents@6.7.0' occurs inside the longer token 'rea-agents@6.7.05' on line 1`.
   A token that appears both exactly and inside a longer token is refused (the
   "every occurrence" clause), and each refusal carries per-token
   `delimiter_evidence` (`token`, `occurrences`, `delimited`).
2. **Duplicate cells.** `parse_record()` returns
   `(checks, unparsed, duplicates)`; every declared cell is a check (a second OMP
   cell makes `checks_total` 6), each duplicate cell binds independently, and the
   duplicated id goes into the receipt's `duplicates`. `bounded()` adds
   `not duplicates` to round 79's 5/5/unparsed-0 verdict, so `ok` is false and
   the arm exits 1.
3. **Receipt.** `instrument.path` is the landing path, `instrument.sha256` this
   file's digest, `checked_at`, `record.rev` resolved by `git rev-parse` to a
   40-hex commit (`rev_arg` keeps what was asked for), `duplicates`, and per
   matched cell the pointed slice's `line_sha256` only — never the slice bytes.
4. **`--validate`.** Keeps round 79's guards (re-derived counts, declared path,
   line digest, 1-based range, 64-hex record digest, 40-hex rev, `checked_at`,
   instrument digest, `ok`/control) and adds: `duplicates` is a list of check ids
   and re-derives from the check list, a matched cell needs delimiter evidence,
   and `ok true` with duplicates is a defect. `is_commit_sha()` is shared by the
   resolver and the rev guard. Each guard has an isolating selftest case whose
   expected defect list is exact.
5. **Selftest.** 61 cases (21 round-79 cases kept, all green) — the six required
   new ones plus boundary (`line start`/`line end`/prefixed/followed), evidence
   shape, non-hex rev, record-absence and verdict-conjunct cases.

CLI, the five check ids, `DECLARED`, the receipt schema conventions
(`schema`/`round`/`predicate`/`checks`/`would_pass`/`ok`) and the exit contract
(0 bound / 1 defect / 2 unevaluable) are unchanged.

## Evidence (commands run from the lane root)

| arm | command (with `TMPDIR=/fast/scratch/hyaku/kaidoku-r80/ExecBinder`) | result |
|---|---|---|
| selftest | `python3 -I -B .ufo/waves/round-80/w1/ExecBinder/pointer-bind.py --selftest` | exit 0, `SELFTEST cases=61 failures=0` (≥27 required) |
| live at base | `... --root . --rev 16dfa009 --json-out live-16dfa009.json` | exit 0, `checks_total 5, matched 5, mismatches 0, unparsed 0, duplicates []` |
| validate | `... --validate live-16dfa009.json` | exit 0, `{"checks": 5, "defects": [], "matched": 5}` |
| live at tip | `... --rev 84d68e90 --json-out live-84d68e90.json` | identical 5/5/0/0, `duplicates []` |
| control | `... --rev 16dfa009 --control path-only` | exit 1, `matched 5` (round 78's rule cannot fail on a moved line); its receipt carries no digest/evidence and is refused by `--validate` by design |
| unevaluable | `... --rev 0123…4567` (absent commit) | exit 2, `{"ok": false, "unevaluable": "rev … does not resolve to a commit"}` |
| frozen fixtures | `fixture-probe.py --candidate …/pointer-bind.py --control tools/round-79/pointer-bind.py --fixtures .ufo/waves/round-80/l1/fixtures/strictness.json` | `cases 4, green_cases 2, candidate_false_greens 0, control_false_greens 4, candidate_green_refusals 0, control_green_refusals 0`, pass true |
| duplicate end-to-end | `... --root <scratch git fixture with a second OMP cell> --rev HEAD` | exit 1, `checks_total 6, matched 6, duplicates ["omp-pin"]`, both OMP cells bound (`cell` 1 and 2), `--validate` defects `[]` |
| mutation sweep | 20 anchored one-edit mutants of the candidate, each `--selftest` | 20/20 killed; pristine 61/0 |

The live cells at base are whole tokens: the three pins are quoted on both
sides, `application.version=12.1.4` sits at start-of-line/end-of-line, and
`.bashrc:28-29` carries `GHIDRA_INSTALL_DIR=` (space/quote) and `JAVA_HOME=`
(space/slash). The strict rule therefore refuses nothing in the live record.

The first mutation pass scored 11/12 and exposed a real gap — a 40-character
non-hex `record.rev` was accepted. `is_commit_sha()` now checks the hex charset
and `red-commit-sha-nonhex` / `red-forged-rev-nonhex` pin it; the re-run kills
20/20.

## Boundaries and coordination

- `parse_record()` changed arity to `(checks, unparsed, duplicates)` — the
  battery seat must consume three values (or count check ids itself). The
  interface is documented in the module docstring; `bind()` is unchanged.
- The substring refusal is proven at the bind level and through the frozen
  fixtures. It is not reachable end-to-end at a record revision: `DECLARED` pins
  the live paths, so a record cannot point at a substitute line without also
  failing `path_is_declared`. The frozen C1 red arms are bind-level fixtures,
  which is the surface the predicate names.
- `instrument.path` is `tools/round-80/pointer-bind.py` and the digest is this
  file's bytes, so R80-C2's committed-blob check matches only if the L1 lands the
  file byte-identically; any edit after landing invalidates the delivered
  receipts.
- `duplicates` is emitted in canonical client order (Devin, OMP, Kimi); a second
  client cell that points at an undeclared path is still bound and still fails
  the declared-path guard.
- Scratch: one dir `/fast/scratch/hyaku/kaidoku-r80/ExecBinder/`, passed as
  `TMPDIR`; the git fixture repo was created with `mktemp -d` under it,
  `rev-parse --show-toplevel` was asserted equal before the single commit, and
  the whole dir is removed before hand-off. No `/tmp` dependency; no
  `git`/`jj` write outside that fixture repo; no pacman, no tool install.

## Files written

- `.ufo/waves/round-80/w1/ExecBinder/pointer-bind.py`
- `.ufo/waves/round-80/w1/ExecBinder/fixture-probe.py`
- `.ufo/waves/round-80/w1/ExecBinder/selftest.log`
- `.ufo/waves/round-80/w1/ExecBinder/live-16dfa009.json`
- `.ufo/waves/round-80/w1/ExecBinder/live-84d68e90.json`
- `.ufo/waves/round-80/w1/ExecBinder/control-path-only.json`
- `.ufo/waves/round-80/w1/ExecBinder/fixture-probe.json`
- `.ufo/waves/round-80/w1/ExecBinder/dup-receipt.json`
- `.ufo/waves/round-80/w1/ExecBinder/mutation-sweep.json`
- `.ufo/waves/round-80/w1/ExecBinder/RECEIPTS.json`
- `.ufo/waves/round-80/w1/ExecBinder.md` (this report)
