# ConnAdjacencyReport — fleet adjacency for REA-Ghidra log/session tooling

Seat: connector (author-side advisory), wave 1, read-only. Axes: **calibration**, **depth**.
Read at 2026-10-20 ~10:30-10:45 -03. No REA analyze/search/decompile, no Ghidra, no carrier execution.
No installs. One write: this file.

## 1. Search boundary (observation)

| # | Pattern | Surface | Result |
|---|---|---|---|
| 1 | `rea-ghidra-` | all 21 `*-shokunin` lanes, `*.md,*.py,*.json,*.sh,*.txt` | 2 lanes only: kaidoku (corpus `.ufo/` pilot) and tameshi (1 line) |
| 2 | `ghidra\.log\|analyzeHeadless\|runtime root` | same | kaidoku corpus/`.ufo` (many, incl. `2026-10-13-r4-10-real-version-pair.md:73`), tameshi:179, revenger `native-route.md:19`, game-dev-3d `F6-rea-census.md:157-172`, souji test fixtures |
| 3 | `ghidra.log` / `script.log` **files** | `find /home/vgpnk/Projects/shokunin` | 4 files, all in `kaidoku-shokunin/.ufo/waves/round-17/pilot/` |
| 4 | `inspect-go-binary` | all lanes | **no hit outside kaidoku** |
| 5 | `/tmp/rea` | all lanes | tameshi:179; revenger `extract_artifact` output roots (`corpus/live/runs/round-10/extraction.json:1`, `round-11/outer-extraction.json:1`) — different prefix, not Ghidra; other hits are unrelated `/tmp` paths (`audio-shokunin/corpus/live/r83-verifier/post-state.txt:12`, `mado-shokunin/.ufo/waves/round-13/w1/ReanchorErratum.md:47`) |
| 6 | `rea-agents@` | all lanes | version pins only (§6) |
| 7 | fleet root `/home/vgpnk/Projects/shokunin/.ufo` + `scripts/` | protocol lane | `reports/round-1/kaidoku.md:25,57`; `prompts/kaidoku-round-17.md:221`; `reports/round-1/revenger.md:85` |
| 8 | REA package source | `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` (6.5.0) | mechanism confirmed (§3) |

## 2. Bounded no-finding (explicit)

**No sibling lane holds REA-Ghidra log-retention or session-tooling.** Within the surface above:
no sibling `.ufo`/corpus file names `rea-ghidra-`, no sibling tool copies `ghidra.log`, and no
`ghidra.log`/`script.log` exists outside kaidoku's own pilot. The only cross-lane mention is a
**citation of our contract, not an observation**:

- `tameshi-shokunin/.ufo/waves/round-16/w1/Overlap2.md:178-180`: "Contention, not collision: kaidoku
  is running Ghidra analyze sessions (`/tmp/rea-ghidra-*`, **per its `contract.md`**), kama launches
  an ephemeral llama-server…". Same file's `:11-15` says kaidoku r17 C1(a) "is repairing exactly the
  defect class that tameshi C2's single `skill_sha256` pin can fall into".

Consequences for wording (calibration):
- C2 may say "no other fleet lane holds retained REA Ghidra-session log capture" only as a
  **searched-surface** claim; cite §1 patterns.
- tameshi's line **cannot** be counted as second-lane/independent evidence for the capability. It is
  a reading of our own round-17 contract, written at 10:29, after the pilot.
- The archival ancestry is our own lane, not another: `.ufo/reports/round-1/kaidoku.md:25`
  ("session lifecycle (`/tmp/rea-ghidra-*` ephemeral)") and `:57` ("zero `/tmp/rea-ghidra-*`
  orphans post-wave"). Both are prior **round-1** observations of ephemerality; neither retains bytes.
- Prior-art inventory (r4-10 `:72-73` "dir since deleted, so this is observed-not-cited"; r4-12,
  r4-14) is already tabulated in `w1/ConnCapabilityHistory.md:30-49` — not restated here.

## 3. Mechanism confirmed in the pinned package (observation; not inference)

REA 6.5.0, package root `P=/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`:

- Root allocation: `$P/dist/ghidra/GhidraClient.js:397` `prefix: "rea-ghidra-"`, parent
  `SESSION_ROOT` (`GhidraSessionRoot.js:28-38` = `tmpdir()`, falling back to `/tmp` when the base
  path has a dot-prefixed element). On Linux that is `/tmp/rea-ghidra-XXXXXX`.
- Log paths: `$P/dist/ghidra/GhidraLauncher.js:449-450` — `ghidra.log`, `script.log` **inside the
  root**.
- Argv: `GhidraLauncher.js:380-385` `-readOnly`, `-deleteProject`, `-log <root>/ghidra.log`,
  `-scriptlog <root>/script.log`.
- Deletion: `GhidraClient.js:614` calls `#removeRuntimeRoots()`; `:638-668` `root.close()` →
  `PrivateRuntimeRoot.close()` = `rm(path,{recursive:true,force:true})`
  (`$P/dist/process/PrivateRuntimeRoot.js:47-50`). If removal fails the root is **retained** and the
  close reports `ProviderCleanupError` (`GhidraClient.js:665`). So "REA deletes its runtime root at
  close" is true for 6.5.0 **except** on cleanup failure — the one case where a post-run root can
  still be read.
- No keep knob: `grep -rno 'REA_GHIDRA_[A-Z_]*' $P/dist` yields exactly
  `COMPILER_SPEC_ID, DISABLED_ANALYZERS, LANGUAGE_ID, NATIVEAOT_JAR, SEED_FILE,
  STARTUP_TIMEOUT_MS` — identical to the pilot's list (`pilot/README.txt:5`). Independent confirmation
  that the polling copy is the only route without patching REA.

**Import for the knowledge entry:** pin both the version (6.5.0) and the npx cache hashed path; a
6.4.0/6.7.0 reader is not covered by these anchors (§6).

## 4. Attribution hazard — two descriptors, one carries a bearer token (observation)

- `$P/dist/ghidra/GhidraLauncher.js:95-106` writes `<root>/session.json` containing
  `token`, `run_id`, `target_sha256`, `provider_version`, `profile_digest`, `endpoint_path`.
  Written mode `0o600` (`:511-517`) — **same-user only**, and the whole fleet runs as one user.
- `:195-206` writes `<root>/ownership.json` containing `run_id`, `pid`, `process_group_id`,
  `parent_pid`, `launcher`, `headless_script`, `created_at` — **no token**.

Hazard: `contract.md:36-39` licenses copying only `ghidra.log`/`script.log`. An executor that
"improves attribution" by copying `session.json` or the whole root writes a **bearer token into a
receipt** that is then committed. The report should state this as a hard boundary; if any receipt
field is added for attribution, it must come from `ownership.json` only.

Concurrency (observation): `ps` shows a live `npm exec rea-agents@6.5.0 mcp` (pid 3221, ppid 3092,
started 09:57:31, cwd `/home/vgpnk/Projects/shokunin`); the host-registered MCP is recorded at
`.ufo/reports/round-1/revenger.md:85`, and CLI-only use is mandated at
`.ufo/prompts/kaidoku-round-17.md:221` ("never through `xd://mcp__rea_*` devices"). The prohibition is
on **use**, not on the process existing. A peer wrote `/tmp/rea-go.json` at 10:32 (esbuild 0.27.7,
`ev_a1e7ac…`), so other seats are running REA CLI commands concurrently. [INFERENCE] Only
Ghidra-opening routes create `rea-ghidra-` roots, so same-prefix contamination is plausible but not
observed today (`ls -d /tmp/rea-ghidra-*` → none). The naive selector "any *new* `/tmp/rea-ghidra-*`
dir since T0" is therefore unsafe under any concurrent MCP/CLI native session; bind by
`ownership.json.parent_pid`/`created_at` inside the child's window and record ambiguity rather than
silently choosing.

## 5. Fleet Ghidra-availability claims are probe-pattern and time dependent (observation)

- `game-dev-3d-shokunin/reports/round-102/repairs/F6-rea-census.md:172`: "Ghidra: absent (no PATH
  hit, no `/opt`/`/usr/share`/`~` install) — census clause still true". Already corrected in-lane:
  `game-dev-3d-shokunin/corpus/knowledge/rea.md:67-71` — the probe missed
  `~/.local/opt/ghidra_12.1.4_PUBLIC` (`application.version=12.1.4`, present since 2026-09-21, not on
  PATH); route receipt `reports/round-106/morphology.md:608`.
- `revenger-shokunin/corpus/live/runs/round-1/wave/native-route.md:19` says Ghidra is `not_configured`
  because "`GHIDRA_INSTALL_DIR` unset". Current observation: the variable **is set**, to the same
  `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC` path; `kumitate-shokunin/corpus/knowledge/kimi-config-plane.md:258`
  records it in the MCP child env. The revenger line is stale, not false-at-time
  (`revenger-shokunin/corpus/knowledge/2026-10-12-rea-readiness-checklist.md:16`).
- REA's own remediation string requires an **absolute extracted Ghidra 12.1.x root**
  (`$P/dist/cli-runtime/IdaConfiguration-CtGP7EKo.js:761-762`).

**Import:** do not cite any fleet "Ghidra absent" line as a current fact in the r17 knowledge entry;
the lane's own PROVINCE wording (Ghidra 12.1.4 provider) is the correct claim.

## 6. Fleet version skew on the same package (observation)

- 6.4.0: `game-dev-3d-shokunin/corpus/knowledge/rea.md:6,53`; `kumitate-shokunin/corpus/knowledge/kimi-config-plane.md:257,348`.
- 6.5.0: this round's contract; live process at `kagi-shokunin/.ufo/round-20/pane-attestation.json:41-43`
  (`npm exec rea-agents@6.5.0 mcp`).
- 6.7.0: registry latest per `game-dev-3d-shokunin/reports/round-102/repairs/F6-rea-census.md:183-202`
  and the skill name at `corpus/knowledge/rea.md:74-76`; open fleet question at
  `.ufo/reports/round-1/revenger.md:85` ("Which version should lane producer runs pin going
  forward?").

**Import:** `log-extract.py`'s component vocabulary and the `-log` mechanics are 6.5.0 facts. Say
"6.5.0" in the entry, not "REA". Whether 6.7.0 changes analyzer component names or the unretained
env knobs is **unknown** — do not claim either way.

## 7. Craft convergence (calibration)

- `tameshi-shokunin/.ufo/waves/round-16/w1/Overlap2.md:15` independently identifies the C1(a) defect
  class, and its bounded move (`:188-215`) proposes a `skill_pins {pre, post, compare}` object — the
  same shape as `pins.py`. This is **convergent design, not outside verification** (tameshi is an
  author seat, not a reviewer of kaidoku).
- `:128` quotes the exact phrase our C1(a) corrections should adopt — the pin pair proves "same
  bytes at two instants", never "unchanged throughout"; `:204-205` repeats the "two-instant"
  wording as its axis argument. Use that phrase in the corrections and lesson.
- `kumitate-shokunin/corpus/QUALITY.md:74-75` (Q14): "evidence pointers never live under `/tmp`".
  Our receipts must carry copies under the lane (contract already does). The pilot's `/tmp` strings
  (`README.txt:2-4`) are **argv/cwd provenance**, not evidence pointers; the report should say which
  is which so a reviewer does not read it as a Q14-class defect.

## 8. One bounded move (proposal, for L1 to accept or reject)

**Add a token-free `capture_window` block to `carrier-run.py`'s receipt and have `log-extract.py`
derive terminal-stage fields from the retained log.**

- Receipt block (from `ownership.json` only, token-bearing `session.json` never read):
  `{root_basename, run_id, pid, process_group_id, created_at, attribution: "ownership.json"|null,
  ambiguity: [root_basenames]|null}`.
- Extract additions: last `(HeadlessAnalyzer)` message class + line number + byte count, and
  `complete: false` with reason `"runtime root removed at close; poll prefix"`.

Why non-obvious, and why now: the two pilot captures stop at **different lifecycle stages** —
`pilot/shfmt-log/ghidra.log:125` (125 lines) ends at `ANALYZING changes made by post scripts`;
`pilot/esbuild-0.25.12-log/ghidra.log:123` (123 lines) ends one stage earlier at `SCRIPT: …`.
The stage is therefore informative and falsifiable, and it converts "retained the log" into
"retained a prefix ending at stage X" without weakening the Go-analyzer findings (all Go lines sit
well before both ends: shfmt `:83-84`, esbuild `:63-64,67`). The static `log_capture_limit` string
(`contract.md:46`) becomes a measured, per-run fact.

- **Axes.** Calibration: improves (mechanical prefix labelling; ambiguous attribution cannot be
  reported as certain). Depth: improves marginally (stage is comparable across carriers and is the
  boundary at which the Go diagnostics stop being observable). No axis harmed: no new tool, no
  dependency, no execution.
- **Risks.** (1) `receipt.json` is a named interface; `receipt-validate.py` must accept the new block
  in the same commit or the receipt becomes invalid — amend both contract sections together.
  (2) `ownership.json` is written only after launch (`GhidraLauncher.js:195`); a killed pre-launch
  run yields no descriptor, so `attribution: null` must be a recorded outcome, never a failure.
  (3) `ownership.json.parent_pid` is the **REA node process**, not the `npx` child the tool spawns
  (one generation off); prefer matching `run_id`/`created_at` within the Popen window and the
  carrier pin, and never process-walk without recording what was unknown.
  (4) Do **not** generalize to "REA always deletes": cleanup failure retains the root
  (`GhidraClient.js:665`).
- **Verification (read-only, reproducible).**
  1. `sha256sum -c pilot/SHA256SUMS` → 6 × OK (ran: all OK).
  2. `tail -1` on the two logs → the two distinct stages above (ran).
  3. `wc -l` → 125 / 123 (ran).
  4. After landing: `receipt-validate.py` accepts a receipt carrying `capture_window`, and each of
     the three measured carriers records a terminal stage + line number; the observed set of stages
     is reported as-is (not required to differ — the poll boundary is timing-dependent).
  5. `ls -d /tmp/rea-ghidra-*` after each run → empty unless a cleanup failure is recorded.

## 9. Drop-in lines for the report's cross-domain section (observation-labelled)

- No fleet lane outside kaidoku holds REA-Ghidra log/session tooling: `rea-ghidra-` appears in 2 of 21
  lanes, and the sole cross-lane hit (`tameshi …/Overlap2.md:178-180`) cites our contract rather than
  observing a session; no `ghidra.log`/`script.log` exists outside kaidoku's pilot.
- The deletion claim is package-versioned: REA 6.5.0 allocates `/tmp/rea-ghidra-*`
  (`GhidraClient.js:397`), writes `ghidra.log`/`script.log` inside it (`GhidraLauncher.js:449-450`),
  and removes it at close (`GhidraClient.js:614,638-668`), retaining it only on cleanup failure
  (`:665`). No keep knob exists; the `REA_GHIDRA_*` env list is six non-retention variables.
- Fleet "Ghidra absent/unconfigured" statements are probe-pattern and date dependent
  (`game-dev-3d …/F6-rea-census.md:172` corrected at `corpus/knowledge/rea.md:67-71`;
  `revenger …/native-route.md:19` vs current `GHIDRA_INSTALL_DIR`); do not reuse them as current.
- The runtime root holds a bearer `token` in `session.json` (`GhidraLauncher.js:98`); receipts must
  copy only the two logs and attribute via the token-free `ownership.json`.

## Files written

- `.ufo/waves/round-17/w1/ConnAdjacencyReport.md` (this file)

## Tool installs/updates

None. No pacman/npm/uv/cargo operation was run.
