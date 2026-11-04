# SentinelScope — round-75 instrument security review

Axes: path containment, pin-before-execution, environment confidentiality,
executable provenance/process lifetime, new-code attack surface. Scope: the five
`tools/round-75/*.py` instruments, source review with benign refusal/selftest
execution only; no hostile payload, no mutation battery run, no lane edits.
Verdicts follow the assignment's SS74 numbering (round-74 report numbers in
parentheses where they differ). Evidence: `containment-tests.txt`,
`selftests.txt` beside this file.

## Verdicts

**SS74-1 — FIXED.** `freeze-pins.py` enforces containment before every open.
`lexical_ok` (45-53) rejects absolute paths and `.`/`..` segments
(backslash-normalized); `contained` (55-71) re-checks lexically, realpaths root
and candidate, and requires commonpath == root before the worktree open;
`blob_at` calls `lexical_ok` at 75 in BOTH branches, so the Git-object
expression gets the same lexical rule (76-86; a git tree read follows no
worktree symlink). The claims container itself is covered: `check` lexically
checks at 89 and opens only `contained(root, claims_path)` (92). Runtime
confirmation (scratch fixture, lane tool): benign claims rc=0; pin naming a
symlink to an outside dir rc=2 "resolves outside the worktree root"; `../`
traversal rc=2; absolute rc=2; the claims container itself symlinked outside
rc=2 (transcript in `containment-tests.txt` T1-T5). Residuals (low, not
claim-dependent): realpath→open is not atomic (a concurrent FS attacker could
swap a component in the microsecond window; the threat model here is a hostile
claims container, which is closed); docstring promises exit 2 for "a pinned
path absent from the world" but absent paths exit 1 via `missing` (107-115).

**SS74-2 (round-74 SS74-5) — FIXED.** `probe-mutation.py` compares the
supplied pin before any generated copy executes. `score` hashes the
caller-selected `git show {rev}:{tool}` blob (288-292), then `check_pin` at 294
raises Unevaluable (exit 2, nothing executed, no scratch writes — the first
write is inside `score_text`, called at 299) on mismatch; selftest case
`pin-mismatch-refused` green (`selftests.txt`). R75-C1's "target pinned before
execution" rests on this order. Other pre-execution reads of caller-selected
revisions: only the `git show` acquisition the pin authenticates; `--validate`
executes nothing. Observation N5 below on the receipt flag.

**SS74-3 — FIXED.** No receipt serialises raw environment values.
`_parse_shims` (seam-probe.py:636-643) emits `recorded`, sorted key NAMES,
`canary_present` bool, `keys_exact` — no `values` key (round-74's defect);
`kernel_witness` samples (524-532) keep key names, canary bool, containment
booleans; A11 shim rows in `a11_verdict` (385-399) are booleans derived from a
local `values` variable that never leaves the function (the only other
`values` occurrences are selftest fixtures at 1300 and the redaction assertion
at 1509). Sweep of every JSON write across the five tools plus the committed
`.ufo/waves/round-75/pre/*.json` and `claims.json`: no HOME/PATH/TMPDIR
values, no canary values (`probe-canary*` absent); receipts carry only key
names, booleans, counts, lane `root`, and battery `work` scratch paths.
Capsule/scratch paths in receipts are the instruments' own directories, not
environment values. Latent windows noted in N2. (The measured round-74 blob
still contains `"values": env` at tools/round-74/seam-probe.py:357,635 — its
own frozen history; the round-75 landing checker is the round-75 blob.)

**SS74-4 — FIXED.** The A11 shim is fixed-source + sidecar: `checker_env_arm`
reuses `_write_shims` with `TRUTHFUL_SHIM` (332-335); `SHIM_PRELUDE` reads all
paths from `<shim>.cfg` (582-588); cfg values are newline-sanitized (627-628);
selftest case `a11-shim-sidecar` asserts the scratch root appears nowhere in
the generated perl (1504-1514). `LYING_SHIM` and `DIRTY_PRODUCER` are likewise
fixed templates; the only interpolated code path left is the A1 impostor shell,
built from two constants plus a `mkdtemp` path (844-848) — mkdtemp names are
alphanumeric, so no quote can reach the script. No `shell=True` anywhere in
the five tools (grep clean).

**SS74-5 — FIXED (battery); NEW VARIANT of round-74 SS74-6 (seam-probe).** The
battery timeout path kills the process group: `run_detector` starts the
detector with `start_new_session=True` (222) and on timeout calls `kill_group`
— `os.killpg(os.getpgid(pid), SIGKILL)` with exception-safe wait (200-209,
225-231), plus a `finally` re-kill (232-233). Not fixed, by contrast:
`seam-probe.py` `forged_subrun` (712-722) and `kernel_witness_arm`
(752-770) still start Popen children and witness threads with no cleanup
`finally`; a `p.wait(timeout=600)` raise leaves children running and the
witness thread alive until its own 180 s deadline. Severity LOW, claim-
independent: any such failure surfaces as a red/unevaluable arm (fails closed)
and R75-C1's detector path is the battery's, which is fixed.

## New observations on the round-75 code

- **N1 (LOW, extends SS74-5 class to controls.py).** `controls.py` fetches a
  caller-selected `--after-rev` blob (`git_show` 66-71) and executes it:
  `run_detector` on the after-rev pristine (115-122) and a subprocess audit
  run (151-158), with no pin check. The battery was fixed for exactly this;
  controls is a counter-instrument whose receipt no claim binds, so impact is
  bounded, but the asymmetry is worth one sentence in the next lesson.
- **N2 (LOW, latent SS74-3 channel).** `checker_env_arm` embeds
  `checker_stdout_tail` (600 chars of the measured checker's receipt,
  seam-probe.py:368) and the battery rows embed a 400-char `stderr_tail`
  (probe-mutation.py:238) — unredacted windows into measured-tool output.
  Empty/benign in every committed receipt today (sweep above); a future mutant
  or measured tool that prints env values would ride these into a committed
  file. The declared round-75 patch sets cannot trigger it.
- **N3 (INFO).** `probe-mutation.py:311` records `"pinned_before_exec": True`
  unconditionally; `validate` (385-386) checks presence, not evidence. The
  guarantee is the source order verified in SS74-2 — the flag is a label, not
  proof. Fine at the freeze; a moved `check_pin` would not flip it.
- **N4 (INFO).** `record-audit.py` `atom_grammar_reds` evaluates the LIVE
  `grammar_cases()` (352-353) while every sibling atom reads the `--rev` world;
  an audit of a historical revision scores current grammars. Harmless for
  R75-C2 (the audit runs at the landing revision) and fails closed.
- **N5 (INFO, new-code correctness).** `_name_samples` (646-661) buckets any
  sample whose argv names no shim under `?`; `a12_verdict` fails closed on a
  dirty `?` (all-samples conjunct on genuine, any-sample on forged).
  `_samples`/`_name_samples` tolerate both dict and list shapes deliberately;
  a non-dict sample would AttributeError the probe, not the detector — a
  wrong-direction crash, never a green. The `sole` computation
  (probe-mutation.py:263-265) is exact list equality `failed == [expect_case]`
  and is re-derived independently by `validate` (374-384); no ordering or
  superset loophole. The audit's `grammar_cases` fixtures (record-audit.py:
  235-260) are pure lambdas over string literals; its subprocess calls
  (91-112, 381-386) are constant-path `git -C root show/log`, no shell.

## Claim dependence

None of the findings blocks R75-C1 or R75-C2. Every residual fails closed
(red arm, unevaluable exit 2, or validate defect) rather than manufacturing a
green. The claim-bearing flows — battery pin ordering, sole computation,
`_samples`/`_name_samples` merge semantics, freeze-pins containment, receipt
redaction — are fixed and runtime-confirmed where a benign test could confirm
them.

## Evidence and limits

- `containment-tests.txt`: T1-T5 freeze-pins refusal transcript (symlink
  escape attempted against a scratch fixture and refused; no lane or host file
  outside the fixture was read by the tool under test — the refusal precedes
  the open).
- `selftests.txt`: freeze-pins (7 cases), probe-mutation (9), record-audit
  (10), all rc=0, including `pin-mismatch-refused`,
  `containment-{absolute,traversal}-refused`, and `a12-shim-values-redacted` /
  `a11-shim-sidecar` names per the atom-22 security arm.
- Committed-receipt env sweep: `.ufo/waves/round-75/pre/*.json`,
  `claims.json` — no values, key names only.
- No tools installed; no git mutations; no exploit run; scratch
  `/fast/scratch/hyaku/kaidoku-r75/SentinelScope` removed before yield.
- [INFERENCE] tags: exploit consequences for the residuals were reasoned, not
  executed, matching the no-exploit-run bound.
