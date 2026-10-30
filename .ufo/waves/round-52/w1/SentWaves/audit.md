# r52-w1 spec write-scope audit (SentWaves, read-only)

Source: `.ufo/waves/round-52/w1-spec.json`, 64 items. Verdicts are per item, against the
contract in the spec `context`: writes only to `.ufo/waves/round-52/w1/<Seat>/` (+ `<Seat>.md`)
and the seat's scratch; no lane-tree, fleet-repo, `.scratch/`, `.ufo/state/`, sibling-lane,
REA, `--data-run`, `corpus/evidence/`, or git-mutation.

Method: each prompt read in full (`all_prompts.txt` in scratch); deliverable paths extracted by
pattern; write verbs and target paths checked; URLs and credential-shaped strings scanned.
Receipts: `receipts/receipts.txt` (command, exit, UTC, stdout sha256).

## Global results

- **Credentials:** none. Scans for `Bearer`, private-key headers, 80+ char base64, `user:pass@`
  URLs: 0 hits in the spec or context. `cookie`/`token`/`secret` occur only as nouns in
  prohibitions or scan scopes (SentCreds, SentSecrets, ScribeReadme, RevClaimsFrozen).
- **URLs:** three named literals, all justified by their task: `man7.org/.../mknod.2.html`
  (ScoutMknod, ScribeSources) and `man7.org/.../capabilities.7.html` (ScoutMknod). Vendor
  carriers are reached by reference through `tools/round-50/carriers.json`; all four are
  `download.avm.de` (receipt `carrier-hosts`). See F6.
- **Unresolved placeholders:** 0 (`placeholder-scan`). Matches of `{...}` are JSON or regex
  text, not markers.
- **Spawning:** no item instructs a subagent or labrat spawn. The only `subagent` string is the
  shared Godspeed preamble.
- **REA execution:** no item runs REA. ExecRunsh and ExecOracleDry drive `c1-run.sh` only via
  `--dry-run`; the harness' dry-run prints the argv and exits before any write (verified).
  See F5 for the counter's `--selftest`.
- **Attack share:** 24 of 64 by role label (reviewer 8, critic 7, mutation-tester 4,
  sentinel 3, revenger 2) = 37.5%. Counting LB1-LB4 (labelled `executor`, falsifiable probes)
  gives 28/64 = 43.8%. Both clear the 25% floor. No `labrat` role is used.

## Findings

- **F1 (medium) ExecMisrootSweep (item 06): fleet-repo deletion is authorised in the artifact.**
  The prompt says "copy byte-exact into the lane, cmp, delete the fleet copy (the one permitted
  fleet deletion)" and asks for an `--apply` mode that performs that copy+cmp+delete. The
  contract forbids touching the fleet repo, and no such permission exists in the contract. The
  seat is not told to run `--apply` against the fleet, but the tool it ships would delete fleet
  files if anyone ran it there. Fix: remove the fleet-delete clause from the item. The helper
  should be read-only (classify and report) plus lane-side copy into the seat dir. Any fleet
  deletion is an operator action outside the wave, recorded in the report, not a seat capability.

- **F2 (medium) ExecOracleDry (15) and ExecRunsh (03): the round-50 harness, with defaults that
  write outside the seat's scratch.** Both items run `c1-run.sh` from the lane path and do not
  pin `--outdir` or `--scratch`. Verified defaults (receipts `harness-oracle-dryrun-default-scratch`,
  `harness-after-dryrun-default-outdir`):
  - default scratch: `scratch_base=/fast/scratch/hyaku/kaidoku-r50` (a round-50 scratch tree, not
    `kaidoku-r52/w1-<Seat>`);
  - default OUTDIR: `<lane>/corpus/evidence/round-50/c1/<id>`, which is `corpus/evidence/`.
  The guards hold today. After-arm without `--data-run` exits 2 (receipt
  `harness-after-without-data-run`). Oracle-arm under `corpus/evidence` without `--data-run` is
  refused (`c1-run.sh:171-172`). Default OUTDIR from a scratch copy exits 2. But the spec does not
  say to pass `--outdir` and `--scratch`, and does not forbid `--data-run`. A seat that adds
  `--data-run` to "exercise the oracle arm" would write into `corpus/evidence/round-50/`. Fix:
  require `--outdir $S/oracle-out --scratch $S` in both items, and state that `--data-run` and
  `KAIDOKU_C1_DATA_RUN` are not to be used.

- **F3 (medium) ExecControls (01): the receipt directory is not named.** "writes a JSON receipt
  per control" with no path. Under the lane default, a receipt could land in `.ufo/waves/round-52/l1/`
  or `corpus/`. Fix: name `.ufo/waves/round-52/w1/ExecControls/receipts/` in the item.

- **F4 (medium, routed defect 2) status.json and report contract: 61 of 64 prompts omit it.**
  Only ExecStatusHelper, ScribeLesson and CritBand name `status.json`. The shared `context` carries
  the requirement (verified). Whether the dispatcher renders `context` into every seat is not
  shown in the spec, and the wave accounting depends on it. Fix: the L1 checks that the rendered
  dispatch for each seat contains the context block (ExecWaveCheck can be extended to assert it),
  or adds one status.json line to every item.

- **F5 (low-medium) ExecCounterV2 (00): "offline `--selftest`" is not pinned against REA.**
  The v1 counter's `--selftest` runs `selftest(a.pkg65 or find_rea_pkg())`
  (`tools/round-50/c1-counter.py:2551-2552`). `find_rea_pkg()` (`:595`) locates the rea-agents
  package in the npx cache, and the evidence-id recompute runs `node tpath --pkg65 ...`
  (`:686`). I did not confirm whether `selftest` (`:2868`) reaches `:686`; that is [INFERENCE],
  not run. The item also does not forbid `--selftest-rea` (`:4630`, which runs REA) or a
  projection run without `--no-rerun`. Fix: prohibit `--selftest-rea`, `--dev-image`, and any
  counter invocation lacking `--no-rerun`. Require the port's selftest to set PATH to a stub
  directory so that any `node`/`npx` child fails loudly.

- **F6 (low) ExecCarrierProbe (10) and ScoutCarrierChain (27): vendor HEAD requests by reference.**
  The four vendor URLs are reached through `carriers.json`, not named in the prompt. The HEAD-only
  limit is in prompt text, with no guard. The network use is justified by the task (HEAD
  receipts for the four pinned carriers). Fix: name the four URLs literally, or accept as
  justified.

- **F7 (low) ConnSiblings (60): reads of sibling lanes.** The item reads sibling
  `PROVINCE.md` files and `corpus/lessons/round-5*.md` titles in three sibling lanes. The
  contract says "never touch a sibling lane". The item says "read-only", so the reading is
  allowed, but the scope is ambiguous. Fix: name the exact read paths, and say "no `.ufo/state/`,
  `.scratch/`, or other sibling file".

- **F8 (low, spec defect not scope) LB3CensusIdem (53): step (2) names a mode that does not exist.**
  The item asks for a "`--file`-style invocation". `census3.py --help` shows `--root --rev
  --check --historical --selftest --out --census`. A tampered census is reachable only as
  `--root <scratch> --rev WORKTREE --check --census <repo-relative path>` (receipt
  `census3-has-no-file-mode`). Fix: state that exact command.

- **F9 (low) ExecV5Baseline (11): scoring output path not named.** v5 requires `--json-out` for a
  run (`sqfs-triage-v5.py:2290-2293`). `resolve_json_out` refuses `tools/`, `plans/`, `corpus/`,
  so no lane write is possible from the graded surfaces. Fix: name `.ufo/waves/round-52/w1/ExecV5Baseline/`
  as the `--json-out` directory.

- **F10 (low) py_compile writes `__pycache__` beside its source, even without `-B`.** Verified in
  scratch (receipt `py-compile-writes-pycache`). ScoutDraftsInventory (29) and RevV6Draft (37)
  say "in your scratch", so they are clean if followed. The lane already holds 50 gitignored
  `.pyc` files under `.ufo/waves/` (receipt `lane-preexisting-gitignored-pycache`). Note only;
  no spec change required.

## Per-item verdicts

Legend: `clean` = writes confined to `w1/<Seat>/` (or `w1/<Seat>.md`) and scratch, reads only.
`finding` = see the finding ID.

| # | item | role | verdict |
|---|---|---|---|
| 00 | ExecCounterV2 | executor | finding F5 (no REA prohibition on selftest) |
| 01 | ExecControls | executor | finding F3 (receipt dir unnamed) |
| 02 | ExecTriV6 | executor | clean |
| 03 | ExecRunsh | executor | finding F2 (dry-run defaults; pin --outdir/--scratch) |
| 04 | ExecFetchVendor | executor | clean (selftest must stay offline; enforced by prompt) |
| 05 | ExecRuleFixtures | executor | clean |
| 06 | ExecMisrootSweep | executor | finding F1 (fleet deletion authorised) |
| 07 | ExecGrammar | executor | clean |
| 08 | ExecStatusHelper | executor | clean (names status.json; scratch --work) |
| 09 | ExecCensusCheck | executor | clean (scratch clone, deleted after) |
| 10 | ExecCarrierProbe | executor | finding F6 (HEAD-only by reference) |
| 11 | ExecV5Baseline | executor | finding F9 (json-out unnamed; low) |
| 12 | ExecSelftestInv | executor | clean |
| 13 | ExecPriors | executor | clean (git cat-file only) |
| 14 | ExecSbProbe | executor | clean (no network; scratch fixtures) |
| 15 | ExecOracleDry | executor | finding F2 (medium; harness defaults write outside scratch) |
| 16 | ExecWaveCheck | executor | clean |
| 17 | ScribeEntryC1 | scribe | clean |
| 18 | ScribeProvince | scribe | clean |
| 19 | ScribeReadme | scribe | clean |
| 20 | ScribeScorecard | scribe | clean |
| 21 | ScribeLesson | scribe | clean |
| 22 | ScribeSources | scribe | clean (literal mknod URL, scratch fetch, justified) |
| 23 | ScribeBlock27 | scribe | clean |
| 24 | ScribeMergeAdopt | scribe | clean (reads shokuknow read-only; "nothing appends") |
| 25 | ScoutMknod | scout | clean (two literal URLs, both named by the task) |
| 26 | ScoutMergeThemes | scout | clean (reads shokuknow; no fetch) |
| 27 | ScoutCarrierChain | scout | finding F6 (HEAD-only by reference) |
| 28 | ScoutCensusRecheck | scout | clean |
| 29 | ScoutDraftsInventory | scout | clean (py_compile "in your scratch"; F10 note) |
| 30 | ScoutV6Corpus | scout | clean |
| 31 | ScoutQualRows | scout | clean |
| 32 | RevCounterPort | reviewer | clean |
| 33 | RevTriPort | reviewer | clean |
| 34 | RevRunshPort | reviewer | clean (rea-agents string is a pin reference) |
| 35 | RevFetchGuards | reviewer | clean (reads ExecFetchVendor output, read-only) |
| 36 | RevDocsDrafts | reviewer | clean |
| 37 | RevV6Draft | reviewer | clean (py_compile "in your scratch"; F10 note) |
| 38 | RevClaimsFrozen | reviewer | clean (git show only) |
| 39 | RevGrammarOffline | reviewer | clean |
| 40 | CritRuleDerive | critic | clean |
| 41 | CritCounterV2 | critic | clean |
| 42 | CritRetry | critic | clean |
| 43 | CritTriV6 | critic | clean |
| 44 | CritClaims | critic | clean |
| 45 | CritFetchChain | critic | clean |
| 46 | CritBand | critic | clean (names status.json) |
| 47 | MutGapRule | mutation-tester | clean (reads corpus/evidence; writes w1 only) |
| 48 | MutTriV6 | mutation-tester | clean |
| 49 | MutControlsV2 | mutation-tester | clean |
| 50 | MutC1Bindings | mutation-tester | clean |
| 51 | LB1V5Audit | executor | clean (scratch script; receipts in w1) |
| 52 | LB2OfflineClause | executor | clean (independent implementation; read corpus/evidence) |
| 53 | LB3CensusIdem | executor | finding F8 (spec defect: no `--file` mode) |
| 54 | LB4Mknod | executor | clean (mknod/mkfifo in $S only; add a non-root check) |
| 55 | SentCreds | sentinel | clean (read-only scan; >1 MiB listing) |
| 56 | SentSecrets | sentinel | clean (read-only) |
| 57 | SentWaves | sentinel | clean (this audit; read-only on lane) |
| 58 | RevExtractor | revenger | clean (reads npx-cache source the task names; no execution) |
| 59 | RevCounterEscape | revenger | clean |
| 60 | ConnSiblings | connector | finding F7 (sibling-lane reads; ambiguous) |
| 61 | ConnSources | connector | clean |
| 62 | ConnDocs | connector | clean |
| 63 | SimpV1Audit | simplifier | clean |

## Recommended spec edits (not applied; the L1 decides)

1. Item 06: strip the fleet-delete / `--apply` fleet clause; keep read-only classify plus lane copy into the seat dir.
2. Items 03 and 15: add `--outdir $S/...` and `--scratch $S` to every harness invocation, and forbid `--data-run`.
3. Item 01: name `.ufo/waves/round-52/w1/ExecControls/receipts/`.
4. Item 00: forbid `--selftest-rea`, `--dev-image`, and counter runs without `--no-rerun`; require a PATH stub that fails any node/npx child.
5. Global: the L1 verifies the rendered dispatch carries the shared context (status.json rule) into every seat.
6. Item 53: replace "`--file`-style" with the exact `--census`/`--rev WORKTREE` command.
7. Item 60: name the exact sibling read paths.
8. Items 10, 27: name the four carrier URLs literally, or confirm HEAD-only is accepted by reference.
