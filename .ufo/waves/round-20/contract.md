# kaidoku round 20 — shared seat contract (L1-authored)

LANE = /home/vgpnk/Projects/shokunin/kaidoku-shokunin. W20 = LANE/.ufo/waves/round-20 (W19, W18, W17 likewise).
Baseline B = 14f0260ad319ecc26994381b2415d5a999003375 (refs/heads/main at dispatch). Claims: W20/claims.json.
Previous outside check: LANE/corpus/lessons/round-19-verifier-spotcheck.md (routed D1-D6 at :178-190).
Round-19 lesson: LANE/corpus/lessons/round-19.md (Mistakes :82-91, Open :95-101, residual limits :180-186).

## Writers: one integration owner (the L1), separate clones OUTSIDE the lane

- Every seat that changes or creates a lane file works in its OWN clone:
  `git clone -q --no-hardlinks LANE /tmp/kr20-<SeatName>` then
  `git -C /tmp/kr20-<SeatName> checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375`
  (record `git -C <clone> rev-parse HEAD` as your observed base). Edit and test only there.
- Deliver as a patch: `cd /tmp/kr20-<SeatName> && git add -A && git diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > LANE/.ufo/waves/round-20/<wave>/patches/<SeatName>.patch`
  (mkdir -p the patches dir). Never include `__pycache__`, `.pyc`, nested `.git` dirs, or files outside your
  assignment. Paste `git -C <clone> diff --cached --stat 14f0260` in your report.
- Never write the LANE working tree except your report and your patch file. Never run git writes or any `jj`
  command in LANE. Read-only git in LANE is fine; use `refs/heads/main` or the full baseline hash, never bare
  `HEAD`, `@`, or `HEAD~N`.
- Never write the fleet repo /home/vgpnk/Projects/shokunin (except via your LANE report path), sibling lanes,
  `.ufo/state/`, MANIFEST.json, client configs (`~/.omp/agent/*`, `~/.config/devin/*`, `~/.kimi-code/*`),
  REA/Ghidra/Go/WABT installs.
- **Selftests and fixtures (round-19 D1):** every selftest, fixture repo and scratch dir lives under
  `tempfile.mkdtemp()` in the system temp dir (never inside LANE or any Git worktree) and is removed on exit.

## Tool conventions

- Python tools: `#!/usr/bin/env python3`, stdlib only, run as `python3 -I -B`; `--selftest` prints
  `SELFTEST: CLEAN cases=N` (exit 0) or `SELFTEST: FAILED ... cases=N fails=M` (exit 1), each case with a
  stable id. Revision-scoped checks read Git objects (`git --no-optional-locks show REV:path`), never the
  working tree, unless the tool's contract says live. Exit codes: 0 clean, 1 findings under `--strict` (or
  red), 2 unusable input/refusal. Every count printed carries its rule; every refusal names its cause.
- Any timestamp you write into evidence is taken from the clock at write time (`date -Iseconds`); never
  write a future or estimated instant (round-19 D2).

## Interfaces fixed for this round (both the fixing seat and the counter rely on them)

- D1 `LANE/.ufo/gates/custody-pair/custody-pair.py selftest --scratch DIR`: exit 2 with stderr containing
  `scratch_inside_worktree` when DIR is inside any Git worktree (walk parents for `.git`); otherwise runs
  and leaves no `custody-pair-selftest-*` dir under DIR on exit.
- D2 `W20/tools/evidence-timestamps.py --root LANE --rev REV --path <lane-relative dir> [--strict] [--selftest]`:
  for every tracked file under the path at REV, every timestamp with an explicit zone on a line
  (`YYYY-MM-DDTHH:MM[:SS][.f](Z|±HH:MM)`, plus `YYYY-MM-DD HH:MM[:SS] ±HH[MM]` / ` -03`) is compared with the
  committer time of the commit that introduced that line (`git blame --porcelain REV`); finding
  `future_dated <path>:<line>`; JSON on stdout; `--strict` exit 1 on any finding.
- D3 `W20/tools/carrier-guard.py {arm,check,disarm} --manifest TSV --record DIR` and `--selftest`. arm records
  per-carrier sha256/size/mode/ctime_ns then clears every exec bit (writes `arm.json`); check verifies modes
  still exec-free, ctime and content unchanged since arm (writes `check-<UTC>.json`; exit 1 with findings
  `mode_restored`, `ctime_changed`, `content_changed`); disarm restores recorded modes (`disarm.json`).
  Selftest (case `exec_refused`): an armed fixture copy of `/usr/bin/true` in mkdtemp raises PermissionError
  on execve; tamper case `mode_restored` exits 1. Declared limit: loader-mapped execution
  (`ld-linux … <file>`) and root are not prevented.
- D4 `LANE/.ufo/gates/c1-census-v10.py --root LANE` → `VERDICT: PASS` exit 0 at the delivered tip, by declaring
  the two round-17 blocks in its scope table with their true class, not by deleting or widening checks.
- D5 final census record `W20/verify/final-census.json` {rev, argv, exit, stdout_path, stdout_sha256}.
- D6a `LANE/.ufo/waves/round-18/tools/head-rev-lint.py` reports nested compare-only HEAD reads in a `nested`
  class (round-17 `verify.py`, `revpin.py`), selftest clean.
- D6b `W20/tools/revexec.py run --root LANE --rev REV --entry <lane path> [--extra <lane path>...] -- ARGS` extracts the REV blobs into
  mkdtemp and executes `python3 -I -B` on them in an OS sandbox (no network namespace access; writes outside
  the work dir refused; bwrap is NOT installed — use util-linux `unshare` user/mount/net namespaces or a
  `systemd-run --user` unit). `--selftest` cases `write_outside_refused`, `net_refused`, `runs_ok`.
- D6c `LANE/.ufo/gates/citation-drift/citation-drift-probe.py`: snapshot slug must match `^[A-Za-z0-9._-]+$`,
  contain no `..`, and resolve inside `--snapshot-dir`; otherwise exit 2 with `slug_unsafe`. Selftest case
  `slug_escape_refused`.
- D6d `W17/tools/receipt-validate.py`: an analyze step is authenticated only when its argv has the token
  `analyze` immediately after the `rea-agents@<version>` package token (npx form); a decoy `analyze` token
  elsewhere is rejected with `analyze_step_unauthenticated`. Selftest case `argv_decoy_refused`.
- D6e `W19/tools/wave-outcomes.py`: a seat literally named `causes` never collides with the wrapper key;
  selftest case `seat_named_causes`.
- D6f `W18/tools/jj-red-before.py --selftest`: new named cases for the round-19 gaps, ids prefixed `jj_`.
- C2 `W20/tools/verb-coverage.py --root LANE --rev REV [--package-dir DIR] [--selftest]`: CLI_COMMAND_NAMES from
  rea-agents@6.5.0 (`~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cliCommandNames.js` via node);
  per command the knowledge entries at REV naming it (hyphen or underscore form, token boundary); per target
  `exercised` = some naming entry also carries an `ev_<64 hex>` id and a path under
  `.ufo/waves/round-20/evidence/c2/` that exists at REV.
- C3 `W20/tools/swiss-misread-v2.py --carrier PATH [--label L] [--snapshot-dir DIR] [--selftest]`: the round-18
  emulator with the func-type variadic bit masked and a `first_failure` object per hypothesis
  (`{"h1": {"kind": "invalid_index"|"eof"|..., "index": int|null, "va": int|null, "phase": str} | null, "h0": …}`;
  null = predicted silent). `W20/tools/first-failure-extract.py LOG` → first Go-analysis failure of a bound
  Ghidra log in the same object shape. `W20/tools/compare-first-failure.py --prediction P --log L` → exit 0 match,
  1 mismatch, 2 unevaluable.

## REA / Ghidra / carriers

- REA CLI only: `npx -y rea-agents@6.5.0 <command>` (the OMP rea MCP entry is operator-owned; never use
  xd://mcp__rea_* devices; never edit ~/.omp/agent/mcp.json). WABT 1.0.42 (official release, installed by the
  L1): `REA_WABT_BIN_DIRECTORY=/home/vgpnk/.local/opt/wabt-1.0.42/bin`. Rizin 0.8.2 at /usr/bin/rizin.
- C3 carriers: the Go 1.24.6 toolchain ELFs under /home/vgpnk/.local/opt/go-1.24.6 (`bin/*`,
  `pkg/tool/linux_amd64/*`). Their exec bits are cleared (W20/evidence/carrier-guard/manual-arm.json). Seats
  NEVER execute any Go toolchain binary (1.24.6, 1.25.0, 1.27.3) and never run REA analyze/search/decompile
  or Ghidra analyzeHeadless on go-1.24.6 files: the L1 runs them after freezing predictions. Byte reading
  (python, readelf, strings, the emulators) is fine.
- Ghidra 12.1.4 at /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC (source: Ghidra/Features/Base/lib/Base-src.zip;
  Go type data: Ghidra/Features/Base/data/typeinfo/golang).

## Reports

Every `Report:` trailer path is relative to LANE — write it at LANE/<that path>. Observation vs inference
labelled; every command pasted with its exit; path:line anchors; never fabricate. A dead or partial result is
reported as such. Keep reports concise; return a final message of at most 8 lines.
