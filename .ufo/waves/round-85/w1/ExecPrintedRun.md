# ExecPrintedRun — round85 w1 scoped findings (R85-C2, tools/round-82/printed-command.py)

Result: 8/8 owned rows KILLED by their declared cases; pristine target green.

- Lane: kaidoku-shokunin; declaration 91eeb72f6a7b13dc96e826117956f90ed89ae3f3 (target blob
  a0d9905aac4067c0e8fb0d8d4b0bd5939433edd0, sha256 91a01190bed4e5cd957177b77e6633e2928ead2a6b8bac581ee5ab7193b92a9f).
- Sandbox commit scored: 752e7a3e8b3a8a1f8c93aa48f1ac34daf8127cfd (declaration bytes + candidate only).
- Counter (frozen, run as given): tools/round-84/mutation-closure.py --root <sandbox> --rev
  752e7a3e… --mutants .ufo/waves/round-85/mutants.json → killed=11, survivors=10, inconclusive=0,
  pristine_failed=[], table restored_equal everywhere. Survivors in this isolated sandbox are
  exclusively rows owned by other seats (7 pc rows → ExecPrintedCmd; sb-emdash-optional,
  sb-id-substring → source-bind seat; cg-frozen-detector-ge → conjunction seat). Note:
  sb-window-13th, sb-two-fields-first, cg-floor-le are already killed by pre-existing cases at
  declaration bytes — those rows were not mine.
- My rows (all killed, sole failing case = declared case, no collateral):
  pc-pin-normprefix/dot-slash-script-refused, pc-run-rc1-strict/rc1-without-expectation-executable,
  pc-run-counter-type/string-counter-refused, pc-run-counter-mismatch-raw/int-counter-equals-string-expectation,
  pc-run-defects-static-dropped/static-defect-ledger-copied, pc-token-metachar-drop-pipe/pipe-metachar-refused,
  pc-token-ellipsis-drop-ascii/ascii-ellipsis-refused, pc-token-allowlist-widened/unbound-plan-variable-refused.
- Selftests: declaration bytes exit 0, cases=22 failures=0 (selftest-pristine.txt); candidate
  exit 0, cases=30 failures=0 (selftest-candidate.txt) — pre-existing 22 cases unchanged and
  passing; +8 r85b cases.
- Candidate construction: additive only — eight top-level `r85b_*` case functions + three
  `r85b_` fixture helpers before `__main__`; one `# R85-B cases` block (eight one-line
  `guarded(...)` registrations) at the end of `selftest()` after the fixture_roots cleanup.
  No predicate, kill rule, target semantics, tools/round-84 file, mutant table, or
  .ufo/waves/round-85/pre fixture touched. All 15 pc mutant anchors still occur exactly once
  in the candidate (verified before scoring).
- Coordination: ExecPrintedCmd (sibling, same file) registers `# R85-A` before the
  fixture_roots cleanup with r85a_ prefixes; my `# R85-B` block sits after that cleanup —
  disjoint seams, additive merge.
- Tool installs: none. pacman: not used (paused host-wide). Git writes: sandbox clone only
  (/fast/scratch/hyaku/kaidoku-r85/ExecPrintedRun/clone.DoPZ, toplevel-verified before commit);
  lane untouched, nothing committed/pushed outside it.
- Risks: none identified for these eight rows. Merge note: parent should keep both
  registration blocks and both function groups (r85a_*, r85b_*) when assembling the integrated
  candidate; total expected selftest cases after merge ≈ 30 + 7 new r85a cases (per sibling's
  design) with the sibling's one pre-existing-fixture replacement.
- Blockers: none.

Receipts (this dir): after-printed-run.json, selftest-pristine.txt, selftest-candidate.txt,
candidate.diff, candidate/tools/round-82/printed-command.py, per-row.md, DONE.
