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
| M45-1 | `sweep-contamination` — a writer that is not the lane left eight files dirty under the frozen directory pathspec `tools/round-44/control-fixtures/`, and a non-author lane sweep then committed them inside a 432-path bulk commit. No commit-time gate saw the dirty tree and no gate saw the sweep, so the loss surfaced only when the round's counters were re-run at the tip and exited 2 `frozen_path_changed`. | `corpus/lessons/round-44.md:18` (the M44-2 row with the author/committer stamp pair), `corpus/lessons/round-44.md:63` (R44-CL1), and the re-derived audit of commit `c86ea508` (path count, the eight `control-fixtures` paths, author 09:57:16 vs committer 10:43:43) in `.ufo/waves/round-45/w1/R45W1InhSweepEvidence/` | `none` at round 44: the freeze rule was enforced only when a counter scored, and the lane's own commit helper never looked at the worktree | `tools/round-45/frozen-path-preflight.py` gains the `--check-dirty` worktree arm, the `--require-pathspec` rule for a directory freeze, the `restored` classifier (history, not tip equality) and an `--selftest` whose red cases are exactly this shape: `red-dirty`, `red-dirfreeze-no-pathspec`, `red-restored`, and `red-bulk-sweep` (eight frozen fixtures plus one unrelated path in one commit). Shown able to fail: deleting the dirty arm makes `red-dirty` return 0 and the selftest fails 1 of 11; deleting the pathspec check makes `red-dirfreeze-no-pathspec` return 0. |
| M45-2 | `unopened-descendant-credit` — an S-row `opened` cell credited a listing replay of descendant paths while the row's own top URL was never fetched; the registry said "opened this round" for a document this lane had not opened. | round-44 closure routing item 4; the row is `corpus/SOURCES.md` S138 and the claim is in `corpus/lessons/round-44.md` `## Gate` (the contents-API listings are descendants of the row URL, not the URL) | `none` in the instrument: `tools/sources-census.sh` validates schema and duplicate URLs, never whether the opened endpoint is the row's own URL | the append-only correction below (CORPUS rule 2 forbids editing the `opened` column): the top URL is fetched live this round with its HTTP status, bytes and sha256, the located quote is recorded, and the Gate states which endpoints were actually opened. Honest limit: this fix cannot fail mechanically — it is a receipt discipline, and the only thing an instrument could check is that a Gate block exists per new row. Recorded here rather than claimed. |

## Gate

### Sources opened this round (2026-10-28)

| row | URL | opened | located quote (≤25 words) |
|---|---|---|---|
| S140 | https://git-scm.com/docs/git-status | 2026-10-28T15:31Z, HTTP 200, 99,934 bytes, page sha256 `903e31c527d443ab4051f7b4e0225058efd96a45d0400538f6ba19b5c9c59ad9`; anchors `Porcelain Format Version 1` and the `-z` machine-parsing paragraph | "guaranteed not to change in a backwards-incompatible way between Git versions or based on user configuration … ideal for parsing by scripts" (21 words) |
| S141 | https://git-scm.com/docs/git-diff-tree | 2026-10-28T15:31Z, HTTP 200, 256,810 bytes, page sha256 `f81c1e3141b2e8e2cfc5790b8923881862f964ae5e3f85c157299b71f80c9640`; anchors `-z` and the raw output format | "When --raw, --numstat, --name-only or --name-status has been given, do not munge pathnames and use NULs as output field terminators." (23 words) |

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
URL itself (receipt `.ufo/waves/round-45/w1/R45W1SrcS138Fix/report.md`), so the cell's claim
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
  16 W04 warnings (S140 and S141 are new URLs; the two added warnings are the within-scope
  URL repeats class recorded by `R45W1CensusDupClass`). No `status` / `recheck` / `used-by`
  cell of an existing row changed except the `used-by` values that name
  `corpus/lessons/round-45.md` on the two new rows.

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

## Inherited state

Nothing from an earlier attempt of round 45 (the round launched once). The round-44
worktree was clean at `149133d4` (`jj-lane.sh state` `ahead=0`, worktree clean), so no
inherited uncommitted lane work was reused or discarded.
