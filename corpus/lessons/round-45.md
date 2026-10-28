# Round 45 — the freeze rule becomes an instrument with four red arms, and the registry names the instruments that carry the claims

Lane `kaidoku`, round 45, attempt 1. Base `149133d47aa7e90796f96047afe6d251a3e65b2c`;
freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` (`plans/round-45-claims.md` and
`tools/round-45/`); instruments `tools/round-45/{frozen-path-preflight.py,c1-counter.py,c2-counter.py}`.
Two claims on two distinct tied-lowest axes — R45-C1 depth (SKILL rule block 22, the
freeze-integrity decision table, and its four-arm interpreter) and R45-C2 calibration
(the instrument registry vs the instruments the round-44 and round-45 frozen claim files
name). The measured revision and verdicts are recorded in the fleet report and in
`SCORECARD.md` `## Round 45`; this lesson holds the mistakes and the source gate.

## Mistakes

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M45-1 | `sweep-contamination` — a writer that is not the lane left eight files dirty under the frozen directory pathspec `tools/round-44/control-fixtures/`, and a non-author lane sweep then committed them inside a 432-path bulk commit. No commit-time gate saw the dirty tree and no gate saw the sweep, so the loss surfaced only when the round's counters were re-run at the tip and exited 2 `frozen_path_changed`. | `corpus/lessons/round-44.md:18` (the M44-2 row with the author/committer stamp pair), `corpus/lessons/round-44.md:63` (R44-CL1), and the re-derived audit of commit `c86ea508` (432 paths, the eight `control-fixtures` paths, author 09:57:16 vs committer 10:43:43) in `.ufo/waves/round-45/l1/inh-sweep-evidence.txt` — re-derived by the L1 because the assigned seat `R45W1InhSweepEvidence` was a job-cap loss and never created its directory | `none` at round 44: the freeze rule was enforced only when a counter scored, and the lane's own commit helper never looked at the worktree | `tools/round-45/frozen-path-preflight.py` gains the `--check-dirty` worktree arm, the `--require-pathspec` rule for a directory freeze, the `restored` classifier (history, not tip equality) and an `--selftest` whose red cases are exactly this shape: `red-dirty`, `red-dirfreeze-no-pathspec`, `red-restored`, and `red-bulk-sweep` (eight frozen fixtures plus one unrelated path in one commit). Shown able to fail: deleting the dirty arm makes `red-dirty` return 0 and the selftest fails 1 of 11; deleting the pathspec check makes `red-dirfreeze-no-pathspec` return 0. |
| M45-2 | `unopened-descendant-credit` — an S-row `opened` cell credited a listing replay of descendant paths while the row's own top URL was never fetched; the registry said "opened this round" for a document this lane had not opened. | round-44 closure routing item 4; the row is `corpus/SOURCES.md` S138 and the claim is in `corpus/lessons/round-44.md` `## Gate` (the contents-API listings are descendants of the row URL, not the URL) | `none` in the instrument: `tools/sources-census.sh` validates schema and duplicate URLs, never whether the opened endpoint is the row's own URL | the append-only correction below (CORPUS rule 2 forbids editing the `opened` column): the top URL is fetched live this round with its HTTP status and byte count, the located quote is recorded, and the Gate states which endpoints were actually opened (a `github.com` HTML sha256 is *not* a page identity — two fetches differ by per-request nonce, R45-CL12). Honest limit: this fix cannot fail mechanically — it is a receipt discipline, and the only thing an instrument could check is that a Gate block exists per new row. Recorded here rather than claimed. |
| M45-3 | `proxy-only-target` — the freeze controlled for a do-nothing surface and for structural red cases, but not for the *cheapest forgery that satisfies the structural proxy*. Wave 1 built both: a 44-line C1 artefact (garbage rows, four line-less citations, a stub interpreter) and a C2 artefact (six fenced table rows anywhere in SKILL.md) each score `met_target: true` under the frozen counters. The landed artefacts are genuine and were read independently; the measure is the weak link. | `.ufo/waves/round-45/w1/R45W1CritC1/report.md` §"Cheapest artefact that scores green" (receipt sha256 `34336cf7…`); `.ufo/waves/round-45/w1/R45W1CritC2/report.md` §3; the same gap in `R45W1C1SelftestFromFreeze` §4 (A1–A6) | prompt §9 requires "the cheapest control that skips the claimed work"; this round read that as a do-nothing control only and did not build the green-shortcut control before freezing | routed as R45-CL13 (C1) and R45-CL14 (C2) with the exact hardening each needs; shown able to fail: the critic's `fx-a6-cheapest-green` scores 0 today and would score 1 under the pinned-interpreter-sha256 rule, because its interpreter is a 4-line stub with a different hash (the critic's fixtures are committed under its seat dir) |

## Gate

### Sources opened this round (2026-10-28)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S140 | https://git-scm.com/docs/git-status | 2026-10-28T15:31Z, HTTP 200, 99,934 bytes, page sha256 `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9`; anchors `Porcelain Format Version 1` and the `-z` machine-parsing paragraph | "guaranteed not to change in a backwards-incompatible way between Git versions or based on user configuration … ideal for parsing by scripts" (21 words, excluding the elision marker) |
| S141 | https://git-scm.com/docs/git-diff-tree | 2026-10-28T15:31Z, HTTP 200, 256,810 bytes, page sha256 `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640`; anchors `-z` and the raw output format | "When --raw, --numstat, --name-only or --name-status has been given, do not munge pathnames and use NULs as output field terminators." (20 words) |

Both rows are cited by the round's R45-C1 landing: block 22's dirty arm parses
`git status --porcelain -z` (S140 says the v1 porcelain format is stable for scripts and
that `-z` is the machine form) and its commit arm parses
`git log --name-status`/`diff-tree` records (S141 says `-z` NUL-terminates the fields and
does not munge pathnames). The rows enter the registry as `mined`, tier A, recheck
`on-release`, `used-by corpus/lessons/round-45.md`.

### S138 correction (append-only)

The row's top URL `https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs`
is the endpoint the `opened` cell names, and round 44 opened its descendants instead
(contents-API listings under `squashfs_v1|v2/.../__output__`). This round fetches the top
URL itself (receipt `.ufo/waves/round-45/w1/R45W1SrcS138Fix/report.md`, committed at `0ee50aaf`; the seat directory is not present in the measured revision `f59565b7`, so the citation resolves from `0ee50aaf` on), so the cell's claim
is true as of 2026-10-28 and false as of 2026-10-28T11:12Z. The column cannot be edited
(CORPUS rule 2: a row present at BASE may differ only in status, recheck, used-by), so the
correction lives here: the row is `mined`, the evidence is the descendant member set
(22 members, 4 endian trees) plus this round's live top-page fetch, and no `used-by` row
is added because no round-45 claim cites S138.

### Admission and rejection

- **Admit** S140 and S141 as registry rows (docs, tier A): both were opened this round and
  both are cited by R45-C1's landed block.
- **Assimilation: none.** The round-44 quarantine refusals stand (S150 fabrication-class:
  the quoted Japanese heading is absent from the live page; S113/S136/S147 present with
  anchor caveats; S117 unverifiable), and no admitted round-45 entry cites a staged row, so
  no row is appended. `considerthese/` is absent in this lane.
- **Census before → after:** `corpus/SOURCES.md` rows 139 → 141
  (`grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`). Round-start census:
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
  → `kaidoku ok`, exit 0, 14 W04 duplicate-URL warnings. Round end: same command, exit 0,
  14 W04 warnings — S140 and S141 add no new duplicate-URL warning, and the class counts
  were classified by `R45W1CensusDupClass` (every current W04 is a same-URL scope variant,
  four of them deliberate CORPUS-rule-2 supersession rows). An earlier draft of this
  paragraph said 16; the measured number is 14 at both ends (corrected after wave-1 seat
  `R45W1SrcGitDiffTree` F5). No `status` / `recheck` / `used-by` cell of an existing row
  changed except the `used-by` values that name `corpus/lessons/round-45.md` on the two new
  rows.

## Routed defects (for round 46)

- **R45-CL1.** The preflight is a *lane-side* gate. Round 44's defect came from a
  non-author fleet sweep, and the fleet's `scripts/hyaku/` tree is read-only for this lane
  (prompt §3), so placement in the sweep/pre-push path is an operator/integrator request,
  not a lane landing. The lane can prove the arm works; it cannot make the sweep run it.
  The achievable substitute landed this round: every L1 commit is preceded by the gate on
  the round's own frozen paths, and the gate's `--check-dirty` arm catches the precursor
  (eight dirty files) before a sweep exists.
- **R45-CL2.** `c2-counter.py` does not verify that a registry row's tool exists at `--rev`.
  A row naming a deleted path would still satisfy a scope path. The frozen target does not
  claim otherwise; a round-46 refreeze should add `tool_present_at_rev`.
- **R45-CL3.** The C2 scope is the six instruments the two most recent frozen claim files
  name. Rounds 41–43 tools (`tools/round-41/*`, `tools/round-42/*`, `tools/round-43/*`)
  remain unregistered; a later round should widen the scope only with its own census, not
  silently.
- **R45-CL4.** `c1-counter.py`'s "actionable table" test is structural (header cells, row
  count, exit cells, citations). A table of structurally valid but semantically empty rows
  would pass. The claim says nothing stronger; the disclosure belongs in the report.
- **R45-CL5.** The r44 counters still exit 2 at the lane tip on the eight sweep-committed
  control-fixture paths. That is a *correct* report of a real post-freeze touch whose author
  was external; the lane does not rewrite the r44 record to make them green.
- **R45-CL6 (HIGH; wave-1 `R45W1RevFreezeCommit` F1).** Both round-45 counters enforce the
  freeze with `git log --name-only <freeze>..<rev> -- <paths>`, which prints **no diff for a
  merge commit**: an edit made by the merge's own resolution is invisible, so a tampered
  frozen path can still be scored `met_target`. The probe is
  `.ufo/waves/round-45/w1/R45W1RevFreezeCommit/fixtures/evil_merge_probe.sh` (preflight 1,
  both counters 0 on the same fixture). The measured range `f762b727..1f4b27f8` contains no
  merge, so the score stands; the fix (`-m --diff-merges=first-parent` plus a tip-blob arm)
  cannot land this round because the counters are frozen.
- **R45-CL7 (wave-1 `R45W1C1CounterMutants`).** Two c1-counter selftest selftest holes:
  `rule_blocks >= 22` and a deleted `block22_present != 1` reason both survive the 9-case
  selftest (clause 1 is exercised only from below, clause 2 by no case). The code is
  correct; the case set must add a 23-block fixture and a two-marker fixture.
- **R45-CL8 (wave-1 `R45W1C2CounterMutants`).** Two c2-counter selftest holes: an
  `endswith` lookup and an "any cell contains the path" lookup both survive the 7-case
  selftest (the wrong-path fixture uses paths that are no suffix of a scope path). Add a
  fixture whose row names `c1-counter.py` (a suffix) and one whose cell contains the path
  beside other text.
- **R45-CL9 (wave-1 `R45W1C1SelftestFromFreeze` §4; six landed mutants).** The counters'
  checks are narrower than the claim sentences they implement: (A1) `craft_blocks` splits on
  `^- \*\*` anywhere in the section, so a top-level `- **…**` line inside a rule body
  manufactures a block; (A2) the citation regex validates only `corpus/knowledge/**`,
  `corpus/lessons/**` and `plans/**`, so `SKILL.md:99999`, `LOG.md:9999`,
  `corpus/SOURCES.md:9999` and `tools/…:7` are invisible to both the `>= 4` count and the
  resolution arm; (A3) `parse_rows` accepts a row under any heading, not only a registry
  table; (A4) it uses `re.search` on the first cell, so extra text beside the backticked
  path still matches; (A5) `scope_size` counts list entries without de-duplication; (A6)
  `\b0\b`/`\b1\b`/`\b2\b` anywhere in the exit cell passes. None was exploited by the
  landed bytes (all six landed rows carry the exact path as the whole first cell, the
  landed refs are all of the validated forms, and the scope file has six distinct paths);
  the landing was also verified against the claim text directly, not only through the
  counter.
- **R45-CL10 (wave-1 `R45W1RevFreezeCommit` F2/F3/F4).** The published gate invocation
  covered only `tools/round-45/` and missed `plans/round-45-claims.md` (one of the two
  frozen paths); the gate's exit is `1` where a counter reports the same condition as `2`;
  and `blob_changed` can name a frozen subtree oid, not only blobs. The corrected
  invocation names both pathspecs and both `--freeze-path` values
  (`.ufo/waves/round-45/l1/preflight-round45-frozen-both.json`).
- **R45-CL11 (wave-1 `R45W1SrcGitDiffTree` F3).** The preflight docstring says the commit
  arm reads NUL-terminated `--name-status` output, but the code invokes plain
  `git log --name-status` and splits on tabs; S141 still grounds the field-separator
  statement, not a `-z` usage this arm does not have. The docstring is frozen; block 22 now
  states the plain form.
- **R45-CL12 (wave-1 `R45W1SrcS138Fix` F1).** A `github.com` HTML page's sha256 is not a
  page identity: two fetches of the S138 top URL differ in 667 bytes (per-request nonce and
  request-id), so a future row must cite the located quote and the paths it lists, not an
  HTML digest. The round-45 Gate cites no HTML digest for S138.

## Inherited state

Nothing from an earlier attempt of round 45 (the round launched once). The round-44
worktree was clean at `149133d4` (`jj-lane.sh state` `ahead=0`, worktree clean), so no
inherited uncommitted lane work was reused or discarded.
- **R45-CL13 (HIGH; wave-1 `R45W1CritC1`, ten forgery fixtures).** The frozen R45-C1 predicate is
  a structural proxy and **not a discriminator**: a 44-line artefact with garbage rows, four
  line-less or off-topic citations and a 4-line stub interpreter scores `met_target: true`
  (`fx-a6-cheapest-green`, receipt sha256 `34336cf7…`). Named defects: (a) the interpreter
  selftest binding proves only that *some* script prints `PREFLIGHT_SELFTEST: cases=11
  failures=0` — no sha256 pin, so a stub passes; (b) a bare/off-topic/self-citation resolves and
  counts (the regex validates path+line, not topicality, and accepts refs with no line
  selector); (c) header cells are substring tests (`"exit" in "no-exit-code"` passes); (d) the
  marker is counted once per block, so two markers in one block pass; (e) `rule_blocks` counts a
  top-level `- **…**` line inside a rule body, so 19 real rules + two scratch bullets + a marker
  block reach 22 while 22 real rules + an extra bullet fail (false negative); (f) a
  `## Queue-drain craft` heading without the trailing space raises `IndexError` and exits 1 with
  empty stdout instead of exit 2. The landed artefact is genuine and was read independently
  (ten real rows whose arms match the interpreter's five arms; the interpreter's 11 fixtures are
  real) — the defect is the measure, not the landing. Round 46 re-freeze: pin the interpreter's
  sha256, require line selectors inside the validated path set, require exact header cell
  equality and an exact marker count, count blocks by a marker-adjacent identity rather than a
  bullet proxy, and exit 2 on a malformed heading.
- **R45-CL14 (HIGH; wave-1 `R45W1CritC2`, cheapest bypass named).** The frozen R45-C2 predicate
  is likewise not a discriminator: **six fenced table rows with embedded paths and a junk exit
  cell, anywhere in `SKILL.md`, score green**. Named defects: (a) rows inside a fenced block, an
  HTML comment, or under no registry heading register; (b) `re.search` on cell 0 lets
  ``see `path` (wrapper)`` register; (c) first-wins dedupe means a fenced good row shadows an
  honest thin row when it comes first (order-dependent); (d) no header validation, and any cell
  containing `0`, `1` and `2` passes (`0 rows, 1 column, 2 bytes`); (e) a scope path that exists
  at no revision registers if a row names it (the `tool_present_at_rev` gap, R45-CL2); (f) the
  freeze arm prints `met_target: true` for a merge-introduced touch (same root cause as
  R45-CL6). The landed six rows are genuine and were read independently (exact first cells, real
  verdict maps) — the defect is the measure. Round 46 re-freeze: require an explicit registry
  section bound by marker, exact cell-0 equality, a header row with the exit column named, row
  presence at `--rev`, and the `-m --diff-merges=first-parent` freeze arm.
- **R45-CL15 (HIGH; wave-1 `R45W1PreflightArms`).** The preflight's eleven cases are
  **arm-covering but not arm-isolating**: deleting the `restored` branch (`m2`) or the blob arm
  (`x4`) alone leaves `cases=11 failures=0`, because `touched` absorbs the kill; `restored` and
  `blob` have **zero unique detection** and their evidence is the arm-coverage matrix, not the
  selftest. Worse, the pristine instrument has a **false-clean** under `--dirty-pathspec` (`x2`):
  the flag *replaces* the dirty arm's scope (`scope_paths = dirty_pathspecs or pathspecs`) instead
  of adding to it, so `--dirty-pathspec other.txt` with a dirty `frozen/b.txt` exits 0 `clean`
  (reproducer `receipts/x2b.json`). Two more untested shapes: untracked entries (`??`, which the
  arm does handle — `x3`) and a log scope narrower than the frozen path, where the blob arm is
  the only defence (`x4b`). Round 46: make the dirty scope the union, add per-arm isolation
  cases, pin `covers()`'s direction, and state the arm matrix in the block.
- **R45-CL16 (MEDIUM; wave-1 `R45W1RegR44C1Run`).** The round's `tools/round-44/c1-run.sh`
  registry row first said the script "plus the independent oracle arm"; the script does not run
  the oracle (`c1-oracle.py` belongs to the counter) and `--dry-run` exits 0 without writing.
  Corrected in amendment A3; the other five rows matched their seat-derived source reads.
- **R45-CL17 (LOW; wave-1 `R45W1RegScopeAudit`).** The frozen scope file's sentence "the
  instruments named as instruments by the round-44 and round-45 frozen claim files"
  over-attributes the word: round-44 calls its three programs a carrier harness/counter and a
  data procedure, never "instrument", and it also names `tools/round-42/c1-counter.py` and
  `tools/round-43/c1-counter.py` as audit-only port sources, which are outside the six. The
  six-path list itself is the round-45 claim's own enumeration; the honest wording is "the six
  instruments this round's claim enumerates, three of them from round 44". `tools/round-44/c1-run.py`
  is the wrapper's unnamed body (the scope names the `.sh`). The file is frozen, so the wording
  is corrected here and the scope widening is R45-CL3.
- **R45-CL18 (HIGH; wave-2 `R45W2C1Rerun` E and `R45W2RestoredArm` A5).** The gate's `touched`
  comes only from `git log` scoped by `--pathspec`; a path named **only** by `--freeze-path` is
  blob-compared (so a net modification is caught) but never appears in `touched`, so a
  tamper-then-**restore** of it exits 0 `clean` while block 22's row 1 declares 1. Reproducer: the
  round's own two-path frozen set with `--pathspec tools/round-45/` only and the claims file named
  by `--freeze-path` (tamper+restore → exit 0; adding the claims pathspec → `restored` populated,
  exit 1). `--require-pathspec` also checks only *tree* freeze-paths, so a file freeze-path can be
  left uncovered. This is R44-CL10's class re-entering through the pathspec boundary; the round's
  own invocation names both pathspecs, which is why the measured score is unaffected. Round 46:
  union the log scope with the freeze-paths and require pathspec coverage for every freeze-path.
- **R45-CL19 (HIGH; wave-2 `R45W2RestoredArm` A6).** A tamper+restore committed on a side branch
  and folded with `git merge --squash` is invisible to the gate (`--diff-merges=first-parent` sees
  the squash as one commit whose net diff is empty). Inherent limit: history the branch no longer
  contains cannot be read from it; the blob arm is what remains, and after a restore it is clean.
  The table must not claim to see what a squash removed.
- **R45-CL20 (MEDIUM; wave-2 `R45W2NoTmp` A4/A5 and `R45W2ConnFormat` F1).** With both
  `HYAKU_SCRATCH` and `TMPDIR` unset the preflight's selftest falls back to `tempfile.gettempdir()`
  (`/tmp`), so its docstring "never a bare /tmp root" is an over-claim; and the registry table is
  7 columns while `PROTOCOL.md`'s house schema is 8 (`entry command` absent). Nothing in the frozen
  files may change this round; the rows are also indexed by column 3, so widening them needs a
  counter change first. Routed.
- **R45-CL21 (MEDIUM; wave-2 `R45W2Rollback` and `R45W2Pins`).** The record's first drafts carried
  three false or stale statements that wave 2 refuted and this commit corrects: "every earlier
  measurement reports the same values" (`block22_refs` grew 6 → 7 → 8), "wave 2 32 seats" (it is
  36), and "no fleet-root file edited" (`.ufo/l0-questions.md` carries the permitted two-line
  append). The wave-2 spec/dispatch committed at `faa875bc` still carries the pre-A2 "16 W04"
  phrase; it is frozen evidence and is not rewritten, so the discrepancy is recorded here.
- **R45-CL22 (MEDIUM; wave-2 `R45W2SecShell` B1/B2).** All three round-45 tools trust `--json-out`:
  `--json-out ../../SKILL.md` overwrites the graded surface, and a `--json-out` onto a frozen path
  writes even on an exit-2 path. No shell injection exists (four `subprocess.run` sites, all list
  argv; no token can start with `-`), and the write scope of a *normal* run holds — but the output
  path is unchecked. Round 46: refuse an output path inside the lane tree's graded/frozen surfaces
  or require it under the caller's scratch.
- **R45-CL23 (LOW; wave-2 `R45W2SentPreflight` (c)).** A pathname containing a newline or tab is
  recorded C-quoted in `touched`/`restored`, so the receipt's path string never equals the real
  path and the `restored` arm is dead for such paths (the verdict is still right through the blob
  arm). A `U+2028` path truncates the recorded path. Nothing in this lane's surfaces has such a
  name; routed for completeness.
