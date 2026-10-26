# R36W2ReviewerCustodyOrder — git custody order over the round-36 landing

Advisory, read-only, leaf seat. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` unless a
path is absolute. Assigned scope: (1) the round-36 commit inventory and the order
freeze → controls → after receipts → C2 landing → C1 landing → integration; (2) immutability of the
frozen files after the freeze; (3) that the `after-run.json` `utc` stamps are later than the controls
commit time. Nothing in the lane, the fleet repo or `/home/vgpnk/Projects/shokuknow` was written.

VCS was read-only throughout (`log`, `show`, `diff`, `ls-tree`, `cat-file`, `rev-parse`,
`merge-base`, `for-each-ref`, `reflog`, `status`). No `add/commit/checkout/reset/stash/pull/push`,
no mutating `jj`, no fixture repo, no subagent, no REA run, no network fetch, no pacman/`uv`/`npx`
install. Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerCustodyOrder` was created and
removed at the end; it held nothing but an empty directory (one 12-line expected-blob table was
written to `/tmp/frozen_expect.txt` and deleted — a temp file, not evidence; every number below is
reproduced by the command beside it).

## Verdict up front

**Custody holds on all three assigned checks; no defect found.** The six round-36 commits form a
single-parent chain in the claimed order, in both ancestry and committer time; twelve frozen files are
byte-identical at the freeze commit, at the integration tip, at the current lane HEAD, in the working
tree, and in **every** one of the lane's refs (857 refs / 349 instances at `6f2ba761`, 866 / 457 at
`2618cf07`, `divergent=0` both times); and the four `after-run.json` `utc` stamps
(`2026-10-26T04:22:42Z`) are later than the controls commit (`2026-10-26T04:22:29Z`) by 13 s.

Three calibration findings, none of which breaks the claim, are recorded in §6:

1. `utc` in `after-run.json` is the **harness invocation start time**, not the completion time
   (`tools/round-36/c1-run.sh:29` runs before the REA call at `:81`), and the four carriers share one
   identical second — the stamps are a batch-start marker, so they cannot order the four runs among
   themselves, and nothing in git or in either frozen counter binds their values.
2. The 13 s margin is thin; it is independently anchored by the installed `sasquatch` binary's
   filesystem times (`2026-10-26 01:22:37.798 -03`, i.e. `04:22:37.798Z`), which sit *between* the
   controls commit and the four run starts, and by the digest chain
   (`after-run.json.sasquatch_sha256` = `ad02d27a…4754` = the installed binary).
3. The five mutant revisions named by four frozen control receipts do not exist in the lane object
   store, so those controls are reproducible only from their `.out` logs plus the counters'
   selftests — not from git objects.

## 1. Commit inventory (assigned range)

`git log --format='%H %cI %s' cab59f22…b8a73..01a44dbf…22cb930` → exit 0, exactly six commits, each
with exactly one parent (`git log -1 --format=%p`, and `merge-base --is-ancestor` on each adjacent
pair, all exit 0). Times are the committer dates; UTC derived with
`TZ=UTC git log -1 --format=%cd --date=format-local:…`; file counts from
`git show --pretty='' --name-only <c> | grep -c .`.

| # | commit | committer (local `-03:00`) | UTC | files | label (verbatim, truncated) |
|---|---|---|---|---|---|
| 0 | `cab59f221fe19726b5692bfa4d9a9679e96b8a73` | 2026-10-25T23:16:39-03:00 | `2026-10-26T02:16:39Z` | 14 | hyaku run 7 interrupted: in-flight snapshot … lane L1 resumes from here |
| 1 | `790561d4e3aca732a434081aa9573ec2fa5fd7d0` | 2026-10-26T01:21:38-03:00 | `2026-10-26T04:21:38Z` | 36 | freeze R36-C1/C2 predicates, counters, selftests, carriers, oracle and before receipts |
| 2 | `6a870b9290e9566468d7d9e6d1b8308daf025b12` | 2026-10-26T01:22:29-03:00 | `2026-10-26T04:22:29Z` | 14 | frozen-counter control receipts (C1 ×3, C2 ×4, all exit 1) before any sasquatch-enabled carrier run |
| 3 | `3310d8fa27bfaa95ad858c4aaad6f6377f853982` | 2026-10-26T01:22:59-03:00 | `2026-10-26T04:22:59Z` | 8 | R36-C1 after receipts (sasquatch 4.5.1 official deb; rea-agents 6.5.0 extract-firmware on K1-K4) |
| 4 | `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be` | 2026-10-26T01:27:16-03:00 | `2026-10-26T04:27:16Z` | 2 | R36-C2 self-assessment repairs (coverage row 122/122; receipts-B and ScoutSkillPlacement pointers repaired by document) |
| 5 | `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95` | 2026-10-26T01:47:30-03:00 | `2026-10-26T04:47:30Z` | 20 | R36-C1 landing — sasquatch SquashFS recursion to Core …; assimilated unblob-sasquatch-dependency |
| 6 | `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` | 2026-10-26T01:50:56-03:00 | `2026-10-26T04:50:56Z` | 57 | lesson (M36-1..7, Gate, assimilation), QUALITY 77-78, SCORECARD round-36 section, LOG, routed-defect corrections, receipts, wave-1 spec and reports |
| — | `6f2ba761bb5bcd6482d45523379376dcb6a386f6` | 2026-10-26T02:01:31-03:00 | `2026-10-26T05:01:31Z` | 6 | wave-1 results (43/43 settled) and last report; wave-2 spec/dispatch |
| — | `38c1a8be78906b1b031eb2035766d9f24d22f0d7` | 2026-10-26T02:11:08-03:00 | `2026-10-26T05:11:08Z` | 29 | wave-2 corrections (assimilated entry pip-route scope + Very-beta attribution, S107 asset set, S111 teaches, lesson quote count, dated pointers on superseded PROVINCE/README lines) |
| — | `2618cf0726d8a96360e489482b29ad4cfd455199` (current `HEAD`/`main` at the time of writing) | 2026-10-26T02:11:32-03:00 | `2026-10-26T05:11:32Z` | 10 | r4u-03 entry supersession note (wave-2 R36W2CriticTrends quality leg); final receipts and census end |

- Claimed order `790561d4 < 6a870b92 < 3310d8fa < d2e46ef5 < ffc81341 < 01a44dbf` holds in ancestry
  (parent chain `cab59f22 → 790561d4 → 6a870b92 → 3310d8fa → d2e46ef5 → ffc81341 → 01a44dbf`, each
  `merge-base --is-ancestor` exit 0) **and** in committer time, strictly increasing, with no author
  date differing from its committer date on any of them.
- `git reflog show main --date=iso` (342 entries at `6f2ba761`, 344 at `2618cf07`) shows one
  `export from jj` line per commit with no intervening reset/amend entry between `cab59f22` and the
  tip; the six hashes appear there in the same order, so no tip rewrite is visible in the lane's own
  pointer history.
- Factual, not a defect: the assigned integration tip `01a44dbf` is not the repository tip. The lane
  kept moving while this review ran — `01a44dbf` → `6f2ba761` (bookkeeping + wave-1 reports + wave-2
  dispatch) → `38c1a8be` (wave-2 corrections to PROVINCE/README/SOURCES/the assimilated entry/the
  lesson) → `2618cf07` (report collection, the r4u-03 entry note, `.ufo/waves/round-36/after/c1-final.json`
  and `c2-final.json`, `census-end.txt`; it also commits an earlier snapshot of this report). None of
  the three post-range commits touches a frozen path (§3, re-verified at `2618cf07`), and the report
  below states the revision at which each check was run.

## 2. Commit content matches its label (custody of the object graph)

`git show --pretty='' --name-status --no-renames <c>` per commit:

- `790561d4` (36 A): `plans/round-36-claims.md`, both counters, `c1-run.sh`, the four selftest files,
  `carriers.json`, the ten K1/K2 fixture files, K1–K4 `before.json`/`before-run.json`/`oracle.tsv`/
  `oracle-run.json`, and `.ufo/waves/round-36/census-start.txt`. This is exactly the freeze set; the
  census file lands with the freeze, as the r34 D-1 correction requires.
- `6a870b92` (14 A): only `.ufo/waves/round-36/controls/` — 7 `.json` + 7 `.out`. No lane surface.
- `3310d8fa` (8 A): only `corpus/evidence/round-36/c1/K{1,2,3,4}/after.json` + `after-run.json`.
- `d2e46ef5` (2 M): only `SCORECARD.md`, `SHONEN.md` — the C2 landing touches no C1 surface, so the
  plan's separability statement has a visible object-graph witness.
- `ffc81341` (20): the two round-36 knowledge entries, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`,
  `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, the ten assimilation evidence files, and two
  counter receipts (`c2/after-at-d2e46ef5.json`, `interim/c1-after-receipts-only.json`).
- `01a44dbf` (57): `corpus/lessons/round-36.md` (new), `corpus/QUALITY.md`, `SCORECARD.md`, `LOG.md`,
  the routed-defect corrections (`corpus/lessons/round-34.md`, `round-35.md`,
  `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md`), the two wave-1 counter
  receipts, the wave-1 spec/dispatch files and 43 wave-1 report/registry files (42 `.md` +
  `swarm-registry.json`).

The two receipts committed in `ffc81341` and `01a44dbf` still measure their *named* revisions because
both counters read git objects, not the worktree:
`tools/round-36/c1-counter.py:48` `git show {rev}:{path}` and
`tools/round-36/c2-counter.py:34-35` `git -C root show {rev}:{path}` (module docstring `:20`:
"Reads only git objects"). Receipt contents:

| receipt | file | `revision` | result |
|---|---|---|---|
| interim C1 (committed in `ffc81341`) | `.ufo/waves/round-36/interim/c1-after-receipts-only.json` | `3310d8fa` | `carriers_matched 4`, **`met_target false`**, all seven bindings false |
| C2 at its own landing (committed in `ffc81341`) | `.ufo/waves/round-36/c2/after-at-d2e46ef5.json` | `d2e46ef5` | `mismatches 0`, `guards_ok true`, `pointers 36`, `met_target true` |
| C1 at the C1 landing (committed in `01a44dbf`) | `.ufo/waves/round-36/after/c1-at-ffc81341.json` | `ffc81341` | `carriers_matched 4`, `carriers_unchanged true`, `met_target true`, bindings `coverage_map_row/entry_present/province_core_row/province_core_section/sourced` all true, `entry_source_ids = opened_source_rows = [S107,S108,S109]` |
| C2 at the C1 landing (committed in `01a44dbf`) | `.ufo/waves/round-36/after/c2-at-ffc81341.json` | `ffc81341` | `mismatches 0`, `guards_ok true`, `pointers 38`, `met_target true` |

The interim receipt is the useful custody datum: the four carriers already matched at `3310d8fa`
while every surface binding was false, so the claimed data alone did not satisfy the frozen
predicate — the verdict needed the landing commit. That is consistent with the freeze's
control-before-data discipline rather than with a verdict assembled after the fact.

## 3. Frozen files unchanged after the freeze

Frozen set as assigned: `plans/round-36-claims.md`, `tools/round-36/c1-counter.py`,
`tools/round-36/c2-counter.py`, `corpus/evidence/round-36/c1/carriers.json`,
`corpus/evidence/round-36/c1/K*/oracle.tsv`, `corpus/evidence/round-36/c1/K*/before.json` (12 files).
The glob form was proved to match before use: `git ls-files -- 'corpus/evidence/round-36/c1/K*/oracle.tsv'`
lists 4 files, and the `K*/before.json` form likewise.

1. **Assigned command form.** `git diff --name-status 790561d4 01a44dbf -- <the 12 paths>` → no output,
   exit 0. Same with `--stat` (no output), and same against the later tips `6f2ba761` and `2618cf07`
   (no output both times).
   The full `git diff --name-status 790561d4 01a44dbf` lists 98 paths; filtering its path column with
   `grep -E '^(plans/round-36-claims\.md|tools/round-36/(c1|c2)-counter\.py)$|^corpus/evidence/round-36/c1/(carriers\.json|K[1-4]/(oracle\.tsv|before\.json))$'`
   returns no line, exit 1 — zero of the twelve frozen names appear.
2. **Per-file blob equality** (`git rev-parse <rev>:<path>`, compared against `git hash-object` of the
   worktree file): 12/12 `SAME`, and 12/12 worktree = freeze = tip. E.g.
   `plans/round-36-claims.md` = `899b87bd…1ac0`; `c1-counter.py` = `654c3cd0…951c` (mode 100755);
   `c2-counter.py` = `4b91f374…07fc`; `carriers.json` = `99e34e84…c322`; `K1/oracle.tsv` =
   `edd39fab…4c73`; `K3/oracle.tsv` = `10c8f40b…12bf`; `K4/before.json` = `cbbac532…2a89`.
3. **History touch test.** `git log --format='%h %cI %s' cab59f22..01a44dbf -- <the 12 paths>` returns
   exactly one commit, `790561d4`. The wider `-- tools/round-36 corpus/evidence/round-36/c1` returns
   only `790561d4` and `3310d8fa`, the latter exclusively for the `after*` files (added alongside,
   not overwriting anything), so the harness `c1-run.sh` and the selftest fixtures named by the
   freeze message are also unchanged.
4. **Every ref, not just the first-parent line.** `git for-each-ref` (all namespaces: `refs/heads`,
   `refs/jj`, `refs/remotes`; no tags in this repo) was swept with `git ls-tree -r <ref> -- <12 paths>`
   and every blob compared to the frozen value. Two sweeps, because the tip moved during the review:
   - at `6f2ba761` (857 refs: 4 heads + 843 `refs/jj/keep` + 10 remotes) →
     `refs_scanned=857 frozen_path_instances=349 divergent=0`;
   - at `2618cf07` (866 refs) → `refs_scanned=866 frozen_path_instances=457 divergent=0`
     (the +9 refs × 12 = +108 instances are exactly the wave-2 commits and their jj snapshots).
   Mechanics were proved before trusting the sweep: `git ls-tree -r main -- <12 paths>` → 12 lines,
   same at `790561d4` → 12, same at `cab59f22` → 0 (the files did not exist at the base).
   The only non-ancestor commits that carry frozen paths at all are two jj keep snapshots,
   `787926b61de60dc6caf61e930f7e5598a03ee1e8` and `c341c6f89b379c18c77657d39f2fc9e2aec2cc42`, both with
   the freeze commit's own `change-id oxpvyylvqwowonskttoknqokynxouwkx`, both parented on `cab59f22`,
   and both carrying the **same** blobs (`899b87bd`, `654c3cd0`, `4b91f374`). So no alternate version
   of any frozen file exists anywhere in the lane's object store reachable from a ref.

## 4. `after-run.json` `utc` versus the controls commit

| file | field | local (`-03:00`) | UTC |
|---|---|---|---|
| `6a870b92` controls commit (committer) | — | 01:22:29 | **`04:22:29Z`** |
| `K1/after-run.json` … `K4/after-run.json` | `utc` | 01:22:42 | **`2026-10-26T04:22:42Z`** (all four identical) |
| `sasquatch` binary (on disk, independent witness) | `mtime` | 01:22:37.798098889 | `04:22:37.798Z` |
| `3310d8fa` after-receipts commit (committer) | — | 01:22:59 | `04:22:59Z` |
| `K*/before-run.json`, `K*/oracle-run.json` (8 files) | `utc` | 01:17:49 | `04:17:49Z` |
| `790561d4` freeze commit (committer) | — | 01:21:38 | `04:21:38Z` |

- **Assigned check: passes.** `04:22:42Z` > `04:22:29Z` by 13 s. The same stamps are also later than
  the freeze commit (64 s) and earlier than the after-receipts commit (17 s), so the receipts were
  written by a run that started inside that window.
- **Independent anchor.** `stat -c '%n mtime=%y ctime=%z size=%s' /home/vgpnk/.local/bin/sasquatch` →
  `mtime=ctime=2026-10-26 01:22:37.798 -03`, `size=382824`, `sha256 ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`,
  `-version` → `unsquashfs version 4.5.1 (2022/03/17)`. All four `after-run.json` record exactly that
  path and digest, and the `before-run.json` record `sasquatch=""`, `sasquatch_sha256=""` (all four).
  Since `mtime` = `ctime` (no later metadata write) and the binary landed 8.8 s after the controls
  commit and 4.2 s before the runs started, "the after runs could not have preceded the controls"
  rests on a second, receipt-independent clock, not only on commit timestamps.
- **Control verdicts.** All seven `.out` logs end `<label> exit=1`
  (`ctl-c1-0-do-nothing`, `ctl-c1-1-no-sasquatch-pipeline`, `ctl-c1-2-forged-oracle-copy`,
  `ctl-c2-0-do-nothing`, `ctl-c2-1-junk-count`, `ctl-c2-2-delete-bad-pointers`,
  `ctl-c2-3-substitute-other-document`), matching `SCORECARD.md:3387` ("all seven controls exit 1").
  The three C1 control JSONs carry `freeze = 790561d4…` and `met_target false`; the four C2 control
  JSONs carry `base = cab59f22…`, `met_target false`, and `guards_ok false`.

## 5. Carrier identity is pinned to committed bytes

`carriers.json` K1 `93802938486d…a589`, K2 `ce5bf60e765e…084f` equal the sha256 of the committed
fixtures (`git show 01a44dbf:corpus/evidence/round-36/c1/fixtures/k{1-le-xz,2-le-gzip}.sqsh | sha256sum`)
and equal the `carrier_sha256` recorded in each `before-run.json`/`after-run.json`, even though the
receipts name a scratch path (`/fast/scratch/hyaku/kaidoku-r36/L1/carriers/…`). K3 `b644d034…f29fb`
and K4 `8efcec73…e1c2` are the shipped-AppImage digests in `carriers.json` (file not committed by
design; its identity is the digest, checked against the upstream release by the wave-1 scout seats).
So the scratch path in the receipts does not make the measured bytes unidentifiable.

## 6. Disagreements / calibration caveats (none falsifies the assigned claim)

1. **`utc` is a start stamp, self-asserted, and unenforced.** `tools/round-36/c1-run.sh:29`
   `now=$(date -u +%FT%TZ)` is evaluated before the PATH work (`:69-78`) and before the REA call
   (`:81`); the value is only written at `:84-87`, after the run. So `after-run.json.utc` bounds the
   *start* of the invocation, not its completion — which is the conservative direction for the
   assigned ordering, but it also means the stamp is a self-description by the same process that owns
   the receipt. Neither frozen counter reads these files at all:
   `grep -n "utc\|run\.json\|run_json\|-run" tools/round-36/c1-counter.py tools/round-36/c2-counter.py`
   → no matches, exit 1; the counters read `{EVDIR}/{k}/{before,after}.json` only
   (`c1-counter.py:163`). Nothing in git or in the predicate would catch a backdated `utc`; the
   ordering's real strength is §4's independent install clock plus §1's commit chain.
   [INFERENCE] the stamps are therefore corroboration, not proof, of their own ordering.
2. **All four stamps are one identical second, including the two 10 MB AppImages** (K3/K4 publish
   2130 regular files each). Under `c1-run.sh:29` a *sequential* loop would stamp each invocation
   seconds apart, so the four after invocations must have been launched within one wall-clock second —
   [INFERENCE] a parallel batch (the eight before/oracle stamps behave the same, all `04:17:49Z`).
   Consequence: the stamps cannot order the four carriers among themselves, and any reader who treats
   them as per-run completion times would mis-order the batch. The 17 s from run start to the
   after-receipts commit is only plausible under that parallel launch; I did not re-run REA to time a
   K3 extraction (out of scope, and not decisive either way).
3. **The frozen controls' mutant revisions are not lane objects.** The four shortcut-control receipts
   name `104dd4a24e62…`, `6a16267c37c4…` (C1) and `f5679b9c342b…`, `a7a9fdb223bf…`,
   `94cd0035f3af…` (C2); `git cat-file -t` is `fatal: could not get object info` for all five, i.e.
   they were fixture-repo commits, not lane commits. Their reproducibility therefore rests on the
   `.out` logs (which carry no counter digest) plus the counters' own selftests that rebuild the
   fixtures. The kill rule is unaffected — the controls' verdicts are install-state independent and all
   red — but a later round cannot re-derive those five revisions from this repo.
4. **Tip scoping of the C2 verdict.** The last C2 measurement is `after/c2-at-ffc81341.json`
   (`revision ffc81341`). `01a44dbf` then changed `SCORECARD.md` again: a new `## Capabilities` row is
   inserted after line 626 (shifting all later lines by +1) and the 14-line round-36 section is
   appended at 3384. Checked structurally and cheaply: no line-range pointer inside the C2 units
   (`## Owned axes`, `## Capabilities`) names `SCORECARD.md:>627`, so the shift does not move a
   C2-checked range; `SHONEN.md` is untouched at `01a44dbf`, and no knowledge file was added there, so
   the 124/124 count cannot have moved. I did **not** re-run either frozen counter (other seats own
   that); the point is only that the frozen C2 verdict is revision-scoped to `ffc81341` and the tip's
   self-assessment state is, strictly, outside it. The same holds for the later wave-2 commits:
   `38c1a8be` edits PROVINCE/README/SOURCES/the assimilated entry/the lesson, and `2618cf07` edits the
   r4u-03 knowledge entry (a content edit, so the file count cannot move) — the wave-2 final receipts
   that do cover this state measure `38c1a8be` (`after/c1-final.json`: `revision 38c1a8be`,
   `carriers_matched 4`, `met_target true`; `after/c2-final.json`: `revision 38c1a8be`, `mismatches 0`,
   `guards_ok true`, `pointers 41`, `met_target true`), i.e. one commit behind the tip at the time of
   writing. I verified the receipts' `revision` fields only; their verdicts are other seats' work.
5. Found nothing else. I looked for: a frozen path modified anywhere (none), a divergent blob in any
   ref (none), a merge or extra commit in the range (none), a tip rewrite in the reflog (none), a
   receipt whose `revision` post-dates its commit (none: `3310d8fa` receipt ≤ `3310d8fa` commit,
   `d2e46ef5` receipt committed in `ffc81341`, `ffc81341` receipts committed in `01a44dbf`), and a
   carrier digest that disagrees with its committed fixture or its run receipt (none).

## 7. Not checked here (other seats)

Evidence-id recomputation and predicate semantics for C1/C2 (assigned elsewhere in wave 2), the
substance of the PROVINCE/SOURCES/README/SKILL edits, the truth of the lesson's M36 rows and QUALITY
77-78 text, K3/K4 upstream digest equality beyond the `carriers.json` record, and any REA execution.
No statement above depends on those.

## Tooling record

Nothing installed, upgraded or downloaded: no pacman/`uv`/`npx`/`cargo` transaction, no host service
touched, no `~/.local/bin` write. Tools used as found: git 2.x (read-only modes listed in the
preamble), `sha256sum`, `stat`, `python3` (json parsing only), `awk`/`sed`/`grep` for counting.
Scratch `/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerCustodyOrder` and `/tmp/frozen_expect.txt`
removed at the end.
