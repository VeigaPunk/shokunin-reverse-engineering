# R38ReviewerCodeAudit — frozen counters + harness protocol audit (round 38, wave 1)

Seat: R38ReviewerCodeAudit (leaf, reviewer). Scope: protocol compliance of the frozen R38
counters and harness — scratch discipline, git-fixture discipline, receipt argv, write
envelope, VCS immutability, exit-code contract, selftest fixture identity, scratch cleanup.
No counter, harness, carrier, oracle or frozen predicate was modified by this seat. No VCS
mutation was performed (read-only git only). No tools were installed or upgraded (no pacman
transactions).

Audited bytes: `c1-counter.py` blob `8e33ac68` and `c2-counter.py` blob `04a0bc63` — identical
at freeze `e059ca93` and HEAD `cb4326b2` (verified via `git ls-tree` + `git show | cmp`).
Harness `c1-run.sh`: freeze blob `96666472`, HEAD blob `a95a1a9e` — changed post-freeze by
`cb4326b2` (see F3). Line numbers below cite the frozen counter bytes and the HEAD harness;
the worktree `c1-counter.py` is NOT the frozen bytes (F1).

Artifacts (evidence copies): `.ufo/waves/round-38/w1/artifacts/R38ReviewerCodeAudit/` —
`worktree-diff-c1-counter.txt` (mutation diff, refreshed at audit end: 50 insertions,
21 deletions), `freeze-to-head-diff-c1-run.txt`, `worktree-status-head60.txt`,
`cb4326b2-stat.txt`.

## Findings (by severity)

### F1 — CRITICAL: frozen counter `c1-counter.py` is mutated in the worktree, uncommitted, and still being edited
- `git status --porcelain` → ` M tools/round-38/c1-counter.py`; worktree blob evolved during
  the audit: `e405d11b` (03:25) → `7cf40c80` (03:27:58 mtime) vs frozen `8e33ac68`. A wave-1
  sibling is actively rewriting the frozen counter.
- The mutation rewrites the frozen predicate docstring (frozen lines 7–13) from "stock unblob
  26.6.4; no external extractor dependency" to "sasquatch-v4be available, as unblob 26.6.4's
  SquashFSExtractor requires" plus a new committed-before-receipt requirement, and rewrites
  `measure()` (frozen ~164–200) to require `before.json` receipts carrying a
  `missing-extractor-dependency` gap; the selftest gains before-arm cases (diff artifact).
- This violates the kill rule in `plans/round-38-claims.md`: "the counter, predicate, carriers
  and oracle are never changed after this commit" (freeze `e059ca93`). The committed history
  is intact (freeze..HEAD diff for `c1-counter.py` is empty) — the violation is live in the
  worktree.
- Operational hazard: any invocation of `python3 tools/round-38/c1-counter.py` from the
  worktree right now executes the mutated predicate, not the frozen one. The frozen harness
  has no `before` mode, so the `before.json` receipts the mutation demands cannot be produced
  by frozen tooling.
- Substance note (not a defense of the procedure): the mutation's mechanism claim matches
  observation — see F2. Whether to restore the frozen bytes (`git checkout --`) or re-freeze
  through a new claims commit is the L1's decision; this seat changed nothing.

### F2 — HIGH: frozen P38-C1 premise "no external extractor dependency" is false (experiment)
- unblob 26.6.4 source (installed at
  `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`)
  lines 25–26: `EXECUTABLE = "sasquatch"`, `V4BE_EXECUTABLE = "sasquatch-v4be"`; lines 44–46:
  BE v4 selects `sasquatch-v4be`; `get_dependencies()` (lines 62–64) returns both. unblob's
  BE-v4 extraction shells out to an external sasquatch binary.
- Experiment A (default PATH, `sasquatch-v4be` present at `~/.local/bin`): harness `after` on
  K1 → exit 0; envelope: handlers `['squashfs_v4_be']`, `extraction_gaps []`, provider
  `unblob`, operation `extract_firmware`, 5 files, evidence id `ev_e6705900…`.
- Experiment B (PATH stripped of `~/.local/bin` → neither `sasquatch` nor `sasquatch-v4be`
  resolvable; unblob still invoked via absolute `REA_UNBLOB_COMMAND`): harness `after` on K1 →
  exit 0; envelope: handlers `['squashfs_v4_be']`, `extraction_gaps =
  [{'kind': 'missing-extractor-dependency', 'handler': 'squashfs_v4_be', 'dependencies':
  ['sasquatch-v4be'], …}]`, 0 files.
- Therefore the round-37 "missing-extractor-dependency" before-arm DOES reproduce when
  `sasquatch-v4be` is off PATH. The frozen claims doc sentences "no external extractor
  dependency", "publishing all oracle files without any external extractor", "the round-37
  … before-arm does not reproduce on these carriers and is reported as a corrected premise",
  and the "Not claimed: … or that sasquatch-v4be is required" disclaimer are contradicted by
  this experiment. The earlier base probes that produced the "corrected premise" most likely
  ran with `sasquatch-v4be` on PATH (installed 01:22, before the probes).
- Consequence: the counter is still scoreable — with `sasquatch-v4be` on PATH (the default
  here) gaps are empty and P38-C1 can be met — but the claim would land on a false stated
  premise. Harness comments share the error: `c1-run.sh:6` ("no external extractor needed for
  standard BE v4") and `:9` ("never runs sasquatch" — true of the harness shell code, but the
  unblob it invokes runs sasquatch-v4be).
- Also observed: the harness `after` mode exits 0 even when the envelope carries the gap and
  zero files — the envelope is the artifact and the counter is the judge; operators must read
  the envelope, not the harness exit code.
- L1 decision needed (reword via a new freeze, or land with a disclosed caveat); this seat
  repaired nothing.

### F3 — HIGH: `c1-run.sh:27` `rm -rf "$OUT"` — unguarded recursive delete of a caller path, introduced post-freeze
- Commit `cb4326b2` (03:19:01, after freeze `e059ca93`) changed after-mode `mkdir -p "$OUT"`
  → `rm -rf "$OUT"` (diff artifact). The freeze commit's own message lists the harness among
  frozen artifacts; the kill rule text names only counter/predicate/carriers/oracle, so this
  is at minimum a freeze-discipline observation.
- The delete is unguarded: no refusal of `/`, `.`, `..`, `~`, no `realpath` (the r37 harness
  resolved `outdir=$(realpath "$outdir")` at its line 31), no existence/ownership check. A
  caller passing a relative path from the wrong cwd — or `.` — destroys data. Oracle mode has
  the same `rm -rf "$OUT"` at `:31` (that one was already in the freeze).
- Doc/behavior contradiction: `c1-run.sh:8` says "OUTDIR must not exist; REA creates it", but
  the code silently deletes an existing OUTDIR instead of refusing.

### F4 — MEDIUM: documented exit-code contract "2 = unevaluable (bad args, git/node failure)" not honored on crash paths
- `c1-counter.py:25` documents "Exit: 0 target met, 1 target not met, 2 unevaluable (bad
  args, git/node failure)". Empirical probes on the frozen bytes:
  - `--selftest` without `--pkg65` → exit **1**, `TypeError: expected str, bytes or
    os.PathLike object, not NoneType` (`c1-counter.py:260` passes `a.pkg65` unvalidated into
    `subprocess.run`). Bad args should exit 2.
  - `node` absent from PATH → exit **1**, `FileNotFoundError: 'node'` (`c1-counter.py:97` in
    `evidence_ids`, `:283` in selftest `mint`). Documented as 2.
  - corrupt `carriers.json` at freeze → exit **1**, `JSONDecodeError` traceback
    (`c1-counter.py:153` `json.loads(frozen)`; also `KeyError` risk at `:157`
    `c['id']`/`c['sha256']`). Should be unevaluable (2).
  - unwritable `--json-out` → stdout receipt printed, then exit **1**,
    `FileNotFoundError` at `c1-counter.py:267` (`json.dump(res, open(a.json_out, 'w'))` —
    handle also never closed).
- `c2-counter.py` same class: corrupt `evidence/round-1-2026-10-15/result.json` → exit **1**,
  `JSONDecodeError` at `c2-counter.py:155` (`json.loads(t)` unwrapped); `command_a`'s
  `ls-tree` (`c2-counter.py:127`) is unwrapped — a git failure there yields empty counts and
  exit 1 (false "not met") instead of unevaluable. c1 wraps its git calls (`:47–51`) and
  correctly exits 2 (verified: `--root /nonexistent-r38` → exit 2 with receipt).
- Working paths verified: missing args → 2 on both counters (`c1:261–263`, `c2:251–253`);
  harness usage error → 2 (`c1-run.sh:39`).
- Risk: every crash path exits 1 = "target not met", indistinguishable from an honest miss —
  a driver keying on exit codes can record a false falsification.

### F5 — MEDIUM: argv/receipt contract gaps
- `c2-counter.py:257` — the unevaluable receipt is `{'unevaluable': str(e)}` with **no
  argv** (c1 has it at `:259`), and the c2 unevaluable path (`:256–259`) never writes
  `--json-out` at all (c1 does, `:260–262`). `gen-controls.py:212` — the fatal receipt
  `{'control': …, 'fatal': str(e)}` also lacks argv.
- Verified good elsewhere: c1 success `:272` and c1 unevaluable `:259` carry argv; c2 success
  `:260` carries argv; all seven committed control receipts carry argv.

### F6 — MEDIUM: c1 selftest mints into a fixed name in the shared scratch root (collision)
- `c1-counter.py:281` — `mint()` writes `mint.wrapped.json` directly into
  `$HYAKU_SCRATCH/kaidoku-r38/` (verified leftover after an isolated run), a fixed name in a
  root shared by every seat, never cleaned up. Two concurrent selftest/gen-controls runs
  overwrite each other's file mid-mint → wrong `evidence_id` → flaky selftest verdicts.
  Violates the counter's own docstring `:26–27` ("writes only a private scratch dir").
  `gen-controls.py:53` does it correctly (mint file inside the per-run fixture dir).

### F7 — LOW: harness regressions vs the r36/r37 convention
- `c1-run.sh:20` — scratch default uses a `$$` suffix (`c1-run-$$`) instead of r37's
  `mktemp -d "$root/c1-run.XXXXXX"` (r37 `c1-run.sh:34`); mktemp is strictly collision-safe.
- Dropped r37's input validation (`r37:20` checked the mode set and `-f $carrier` → usage
  exit 2): r38 never checks that CARRIER exists, so a missing carrier surfaces as an
  npx/sasquatch runtime failure (exit 1) instead of a usage error (exit 2).
- Dropped r37's `realpath` on OUTDIR (`r37:31`) — compounds F3.
- Comment `:16–17` says "Scratch for npx caches etc. lives under $SCRATCH", but nothing points
  npm's cache at `$S` (only `TMPDIR` is exported, `:23`); npx still writes `~/.npm/_npx`.

### F8 — LOW: oracle-mode diagnostics swallowed; env-precondition exit code
- `c1-run.sh:32–33` — sasquatch stderr goes to `/dev/null`; failure prints only
  "sasquatch-v4be failed" with zero diagnostics.
- `:26` — missing `REA_UNBLOB_COMMAND` exits 1 (observed) rather than 2; defensible as a
  runtime precondition, but the harness header documents no exit contract for it.

### F9 — LOW: control fixtures do not isolate their named defects; CTL-C1-0 scored at the freeze, not the base
- `gen-controls.py:73,88–89` — c1 control fixtures carry ALL bindings false (no entry,
  SOURCES row, README row, frontier note), so CTL-C1-1/CTL-C1-2 exit 1 for many reasons, not
  specifically "three carriers" / "wrong handler". Safe direction (a control can never
  falsely meet target), but the selftest variants are the only properly isolated reds.
- `ctl-c1-0-do-nothing.json` argv shows `--rev e059ca93 --freeze e059ca93`, while the claims
  doc says "CTL-C1-0 do-nothing at the base" (`77091b49`). At the true base the counter would
  exit 2 unevaluable (`carriers.json absent at freeze`), not the observed exit 1 — doc vs
  receipt mismatch.
- `gen-controls.py:11` — "(removed on exit)" is inaccurate: only the per-run `ctl.*` dirs are
  removed; the `controls-<kind>/` container persists. `:18` hardcodes the pkg65 default
  (the counters require the flag explicitly).

### F10 — LOW: frozen binding/guard looseness (report-only; frozen bytes untouched)
- `c1-counter.py:208–209` — `frontier_note` = any PROVINCE.md line containing both
  'big-endian' and 'superseded'; not scoped to the Frontier section or the round-38 note.
- `c2-counter.py:229` — the "repaired by the same document" guard accepts suffix matches:
  `d/z/y.md` would "repair" `y.md` (different document). The fixture ships `d/z/y.md` but no
  case exercises it.

### F11 — INFO: environment/hygiene observations
- Counters accept no scratch argument (env-only, `c1:56–59`, `c2:311–312`) — consistent with
  the r36 (`:52–55`) and r37 (`:41–44`) counter precedent; the harness carries `[SCRATCH]`
  (`:20`). No hardcoded `/tmp` anywhere; default root is `/fast/scratch/hyaku`.
- `tools/round-38/__pycache__/*.pyc` exist but are gitignored (`.gitignore:1–2`) — evidence of
  a counter run without the documented `-I -B`; harmless.
- An untracked `unblob.log` appeared at the lane root in my 03:20 status snapshot and was
  gone by 03:33 (removed by a peer). Verified NOT harness-produced: an `after` run with
  cwd in scratch leaves the cwd clean (unblob's cwd log default, `cli.py:309`, applies to
  direct unblob runs).
- Untracked `w1.ready` / `w1.ready.dispatched` stamps — the R36-CL1 untracked-stamp pattern
  recurs in round 38; L1 integrates.
- `tools/round-38/selftest/dev-before.json` is committed but unreferenced by the frozen
  counter (selftest reads `dev-after.json` + `dev-oracle.tsv` only, `c1:273–274`).

## Verified good (checklist, with evidence)
- HYAKU_SCRATCH honoured everywhere (`c1:56–59`, `c2:311–312`, `gen-controls:19,23`,
  harness `:20`); no hardcoded `/tmp`.
- Git fixture discipline: `tempfile.mkdtemp` + `git -C <d> init -q` +
  `rev-parse --show-toplevel` equality check before the first commit — `c1:375–377`,
  `c2:320–323`, gen-controls both fixtures; every git call in all four tools names `-C`
  (grep-verified). No VCS mutation against the lane: counters use only
  cat-file/show/ls-tree; the harness contains no git at all.
- argv in receipts: c1 both paths (`:259`, `:272`), c2 success (`:260`), gen-controls normal
  path, all 7 committed control receipts (gaps → F5).
- Write envelope: counters write only scratch + `--json-out`; harness writes only `$S` +
  OUT; verified empirically (selftests wrote only under my HYAKU_SCRATCH; harness left cwd
  clean; `xpin-attribute.mjs` writes nothing — grep shows only `process.exitCode`).
- Exit codes on documented paths: missing args → 2 (both counters, observed); usage → 2
  (harness, observed); wrapped git failure → 2 (c1, observed); success/failure 0/1 on all
  exercised runs (crash-path gaps → F4).
- Selftest fixtures are dev envelopes, never carriers: c1 selftest builds its own carrier
  spec and reads `selftest/dev-after.json` + `dev-oracle.tsv` (`c1:273–274`);
  `dev-after.json` subject digest `acc64a3d…` == sha256(`dev-le-xz.sqsh`) — a round-36 LE xz
  dev image, not K1–K4; the real `carriers.json`/round-37 oracles are never read by selftest.
- Harness removes its scratch on exit: trap at `:22`; verified h1–h4 all absent after runs.
- Selftests green on frozen bytes: c1 → `{"cases": 15, "green_ok": 1, "red_ok": 14,
  "failures": []}` exit 0; c2 → `{"cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}`
  exit 0 — both match the claims doc's case counts and named reds.
- Harness exercised: `oracle` on K1 → exit 0, output byte-identical to committed
  `corpus/evidence/round-37/c1/K1/oracle.tsv` (diff clean); `after` on K1 → exit 0, envelope
  complete (handler `squashfs_v4_be`, gaps `[]`, provider `unblob`, 5 files,
  `ev_e6705900…`); REA invoked only via `npx -y rea-agents@6.5.0` through the harness.
- Carrier pins: all four `carriers.json` sha256 pins match the committed carrier bytes
  (K1 `1cfb6c33…`, K2 `403cb0a8…`, K3 `9c7c523c…`, K4 `a29ddc15…` — recomputed).
- Separability: c2 reads only SCORECARD/SHONEN/PROVINCE/SKILL/README/knowledge/result.json;
  c1 reads none of SCORECARD/SHONEN (inspection).
- Committed counter blobs intact at HEAD == freeze (c1 `8e33ac68`, c2 `04a0bc63`); the
  freeze is intact in history — the violations are the dirty worktree (F1) and the
  post-freeze harness commit (F3).

## Tooling record
No tools installed or upgraded; no pacman transactions; no host services touched. Used only
pre-existing system python3 3.14, git, node v24.21.0, the L1-installed
`~/.local/bin/sasquatch-v4be` + unblob (uv), and REA 6.5.0 via `npx -y` through the harness.

## Scratch
`S=/fast/scratch/hyaku/kaidoku-r38/R38ReviewerCodeAudit` (frozen-byte extractions, probe
outputs, fixture repos) — removed at session end; every cited byte is copied into
`.ufo/waves/round-38/w1/artifacts/R38ReviewerCodeAudit/`.

## Residual risk / verification gaps
- The worktree mutation was not executed by this seat (audit target is the frozen bytes);
  its current blob `7cf40c80` may differ from the diff snapshot taken minutes earlier — the
  editor was still active at 03:27:58. Attribution of the editor not established (shared
  worktree, many live siblings) — left to L1.
- Only K1 was exercised through the harness (after + oracle); K2–K4 after-runs are the
  executors' claim-data work.
- The no-sasquatch probe used a PATH-stripped environment rather than a hermetic container;
  unblob's `get_dependencies()` (`squashfs.py:62–64`) makes the sasquatch-v4be requirement
  structural, so the conclusion does not hinge on the probe environment.
- Exit-code probes covered the documented failure classes; exotic failures (disk full,
  signals) were not exercised.
