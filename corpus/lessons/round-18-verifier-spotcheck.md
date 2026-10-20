author: hyaku closure (non-author integrator, @m_opus)

# Round 18 — independent closure and admit/reject spot-check

Date: 2026-10-20. Status **ok**; **admitted**. Three claims verify: C1 calibration, C2 operability (fleet axis, unowned proxy) and C3 depth (sourced). No axis is harmed. Seven status-neutral defects are routed below. This closure authorizes no promotion, mint or `[x]`.

## Revisions and scope

- Baseline B: `9011581d84527ba34c675f9cf912e54d2e72d470`.
- Predictions frozen: `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
- Verification source S: `db4bdb16b842a93f8ec07523c1275c6dfe0f5229`. Evidence: `454dee6923750698cc36041236db13b52c6fcade`.
- Delivered A: `a245bb00c581ae3423a10a055c77d4bc873918df`.
- Fleet report: `.ufo/reports/round-18/kaidoku.md`, committed as `kaidoku-shokunin` in fleet `4338083062a98a770eb95f254eb6b04cb870292c` (14:23:14-03:00). The appended erratum is in `e9eec367992f9180b644170370c806d46eb05c00` (14:24:15). The filed bytes are a byte prefix of the current file.
- This closure dispatched seven read-only re-check seats; the lane did not dispatch them. They are `ClosureKaidokuR18-3.PromptFidelityR18`, `.C1RoutedDefectsR18`, `.C2HeadPinsR18`, `.C3FrozenReplayR18`, `.NoHarmR18`, `.SourcesGateSampleR18` and `.WavesInstallsR18`. I adjudicated their findings, and I re-ran the decisive checks myself (marked "own").

Committed dispatch/completion digest (the mutable watchdog log is not the durable pointer):

```text
2026-10-20T12:07:53-03:00 launch kaidoku round=18 pgid=4070059 driver=hyaku-inline attempt=1
2026-10-20T14:31:43-03:00 complete kaidoku round=18; hyaku-inline attempt=1
```

This closure did not execute any lane tool, gate or selftest: `routed-defects.py`, `head-rev-lint.py`, `jj-red-before.py`, `revpin.py`, `receipt-validate.py`, `measure.py`, `controls.py`, `verify.py`, `run-carriers.sh`, citation-drift or custody-pair. I verified their committed outputs. I executed Git-object censuses, independent parsers over `git show` blobs, the shared sources census, and web re-opens. This closure installed or updated no tools.

## Step-1 conformance

Own commands and outputs:

```text
git -C /home/vgpnk/Projects/shokunin log --format='%an %ae %H %s' -- .ufo/reports/round-18/kaidoku.md
kaidoku-shokunin kaidoku@shokunin.local e9eec367992f9180b644170370c806d46eb05c00 round-18: kaidoku report erratum (dead seat)
kaidoku-shokunin kaidoku@shokunin.local 4338083062a98a770eb95f254eb6b04cb870292c round-18: kaidoku report

/home/vgpnk/Projects/shokunin/scripts/hyaku/jj-lane.sh state /home/vgpnk/Projects/shokunin/kaidoku-shokunin
state branch=main local=a245bb00c581ae3423a10a055c77d4bc873918df remote=a245bb00c581ae3423a10a055c77d4bc873918df ahead=0 behind=0 head=detached tracked=0 untracked=0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain | wc -l
0   (before closure writes)

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-remote origin refs/heads/main
a245bb00c581ae3423a10a055c77d4bc873918df	refs/heads/main
```

- **Ancestry.** For B, `eb6c266`, `b2aad08`, S, `454dee6`, `06df023`, `af2861c` and A, `git cat-file -t` returns `commit` and `merge-base --is-ancestor <h> refs/heads/main` returns 0. `e9eec36`, which the report cites, is a fleet-repo commit and an ancestor of fleet HEAD; it is not a lane commit.
- **Ordering.** The `refs/remotes/origin/main` reflog shows the following push times (-03:00):

  | Commit | Pushed |
  |---|---|
  | `eb6c266` | 13:23:57 |
  | `b2aad08` | 13:38:11 |
  | S | 14:16:47 |
  | `454dee6` | 14:17:37 |
  | `06df023` | 14:20:09 |
  | `af2861c` | 14:20:46 |
  | A | 14:21:05 |

  The report followed at 14:23:14, so the report lands last. `eb6c266` has author date 12:06:56. That date is the creation time of the jj change and comes before the launch; its committer time is 13:23:55. All seven lane commits are authored by `kaidoku-shokunin`.
- **Report content.** The report has work performed, LOG-tied landed changes, Sources & frontier, all three trend verdicts, and `## SHONEN` with 4 `[~]` lines (`SHONEN.md` has 4 boxes). It is not a marker.
- **Prompt.** `.ufo/prompts/kaidoku-round-18.md` was committed as `kaidoku-shokunin` in `149c5af4837e70e32d7cbad32fb6231cfa21b91c` at 12:07:52. The PromptFidelityR18 seat re-rendered `templates/round-prompt.md` with `scripts/shokunin-watchdog.sh:172-184` substitutions; the diff against prompt lines 1–140 exits 0, and the §6 addendum (from line 141) equals `lane-addendum.md` after `inline.sh` substitution. Every round-level and child-lane item is present:

  | Item | Prompt lines |
  |---|---|
  | Claims/axes | 3–17 |
  | L2 ≥8 in one batch | 82–84 |
  | Commit-then-push | 133–134 |
  | Push scope | 135–137 |
  | L0 | 138–140 |
  | Report path | 101–102 |
  | SHONEN | 118–119 |
  | Hash citation | 263–269 |
  | Write scope | 244–249 |
  | Report lands last | 284–289 |

- **Template note (operator-side, not lane debt).** §3 lists `1× planner` in the L2 split, while §6:198-201 says the validator rejects a planner role and gives that seat to the L1. The lane followed §6 and disclosed it.
- **Stale lane.** The mission was open 2h24m from launch to completion. The report grades it *progressing*, and seven lane-authored commits inside the window confirm that.

## Claims — independent re-check

### C1 calibration — improved (re-derived from blobs; gate evidence verified)

The author disclosed that wave-2 seats closed defects with fabricated evidence that the first checks accepted. I therefore re-derived every defect without the gate.

| Defect | Re-derivation at B and A |
|---|---|
| R17-PINMAP | At B, both the r17 knowledge entry and `SCORECARD.md` are exact byte prefixes of their A versions, and A appends the named correction ("mid-run instants retain the comparator verdict … not the map"). The correction's fact holds: the `d0ab299` pass-2 receipts carry 29 `pin_checks` with only the keys {changed, entries, equal, missing, taken_at_utc}. Substance: all 22 round-18 `pin_checks` across 15 receipts have a retained `pins/mid-*.json`. For 22/22, the blob sha256 equals `map_sha256`, the count and instant match, and the entries equal `pins_pre`. QUALITY #21 is added. |
| R17-VALIDATE16 | `evidence/validate16/summary.json` reports 8/8 exit 0, and its labels equal the 8 run directories at `da64646`. All 8 retained stdout sha256 values match. `validator_sha256` equals `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py \| sha256sum` (`618448829ba6…126f`). The gate checks only the format of that field, but the value is the true digest. `checks_performed` = 341 per pass-1 receipt agrees with the B-era pass-2 runs (341 + pin_checks). |
| R17-PRODUCER-REV | `2711674…` and `95e34db…` are named in SCORECARD, LOG, the knowledge entry and `round-18.md:56`, and both are ancestors of `refs/heads/main`. The `carrier-run.py` blob history is `bc964ac` at `2711674`/`da64646` (pass 1, 13:47:05–14:00:05Z), `c536e3e` at `95e34db` (pass 2, 14:27:41–14:40:02Z) and `f91bbc7` at `d0ab299`. Receipt fields fit that attribution: pass 1 has no `pin_checks`, pass 2 has them, and no receipt has `md5_pre`. The attribution is correct, which the author had marked as not checkable offline. |
| R17-SUMS-RUNLOG | All 17 lines of `2711674:…/predictions/SHA256SUMS` are byte-exact at A. The restored `carriers.tsv` line `8ac38afe…` equals the A blob hash, and all 18 lines re-hash clean. The `da64646` `run-log.txt` has 7 start and 7 end lines, no calib-shfmt and no aggregate exit, as `round-18.md:57` discloses. |
| R17-REGISTRY | `SKILL.md:540-542,545` carry `Pinned values:` and `Write scope:`, and every cited path exists at A (9 blobs). `:448` is `gate / kaidoku` with `--strict`, and the probe has a `return 1` path. |
| R17-S032-DIGEST | `git ls-remote https://github.com/NationalSecurityAgency/ghidra refs/pull/9348/head` returns `a214355498e84aa86280be0c31c955aaf94f2d12`; the PR is open and unmerged, and its title is exact. Two fresh `.patch` fetches hash to S033's `ae5dc2e3…a11`. The head is real and the patch digest reproduces, which the author had marked as not checkable offline. |

- **Gate evidence (verified, not executed).**
  - Final recheck: `final-recheck/routed-defects.receipt.json` has `--rev 454dee6 --strict` and exit 0. The stdout sha256 `7873566c…` equals the recorded value, and it reports `open_count`/`named`/`substance` = 0/0/0.
  - Baseline: the verification-pass baseline run at B reports open 6/6/6. Its retained run is non-strict (exit 0). The strict exit 1 at B appears only in seat prose (w2 `LessonMistakesAudit.md`, `GateREGISTRY.md`); minor, routed below.
  - Selftest and pass bounds: `selftest-routed-defects` has exp 0 and got 0 in `verification.json`. The pass is at source S (`head_equals_source: true`, `source_pushed: true`, `unexpected_exits: []`). It ran 17:16:56–17:17:11Z, after S was pushed at 17:16:47Z and before `454dee6`.
- **QUALITY.** Rows go 20 → 21. Own command: `grep -E '^\| *([1-9]|1[0-9]|20) *\|'` gives sha256 `be170f23…22ec` at both B and A. A seat's independent parser agrees.
- **Residuals.** No fabrication survives, and none reopens a defect:
  - The `validator-sha256-pinned` gate check is format-only.
  - The VALIDATE16 remapped inputs carry no digest of the `/tmp` copies. Their tie to `da64646` rests on the label set and the 341-count consistency.
  - The `pins` and `go-buildinfo-probe` "Pinned values" cells name no path.
  - The frozen r17 `SHA256SUMS` was edited in place (disclosed).

### C2 operability — improved (re-measured)

- Independent grep: `git grep -n -I -F -e '"HEAD"' -e "'HEAD'" <rev> -- .ufo/gates ':(glob).ufo/waves/round-17/**/*.py' ':(glob).ufo/waves/round-18/**/*.py'`.
  - At B there are 14 hits: 3 live revision pins and 11 fixture reads. The live pins are citation-drift `:477`, custody-pair `:327` and round-17 `verify.py:59`, exactly the three sites R1–R3 that `JjAuditKaidoku.md` §5 names.
  - At A there are 54 textual hits, and none is an unannotated live source pin; the rest are lint documentation, selftest fixtures and annotated sites.
  - Under the lint's documented rule this agrees with live 3 → 0 (fixture 8 → 15, annotated 0 → 6).
- The receipt `final-recheck/head-rev-lint.receipt.json` is at `--rev 454dee6` with exit 0, and its stdout sha256 `6e562380…` matches. The baseline-strict run in `verification.json` has exp 1 and got 1 (live 3). `git diff --name-only 454dee6 A` over gates and round-14–18 sources is empty.
- `verify/jj-red-before.stdout`: 14 of 14 expectations `held: true`, and the lane tip is unchanged before and after.
- The limits match the disclosure:
  - Two compare-only nested HEAD reads (`round-17/verify.py:83`, `round-18/tools/revpin.py:108`) are invisible to the lint, but neither selects a run revision.
  - citation-drift `:329` guards only `rev == "HEAD"`, so `HEAD~1`/`@` reach `rev_ok`.
  - "0 live" is therefore a lint-rule count, as the author states.

### C3 depth (sourced S034/S035) — improved (re-derived from raw logs)

- **Freeze before run.**
  - Own check: the reflog shows `eb6c266` pushed 13:23:57-03:00, and `runs/run-log.txt` starts at 13:24:07.
  - `git ls-tree -r eb6c266 -- .ufo/waves/round-18/runs` is empty.
  - The `predictions/` tree id `3b2ab6ff…` is identical at all seven round commits (34 blobs).
  - Each receipt pins the prediction sha256 equal to the `eb6c266` blob.
  - All ISO timestamps in the 248 `runs/` blobs fall between 13:23:55 and 13:32:10-03:00, before `b2aad08`'s commit at 13:38:07.
- **15/15 matched.** The seat parsed each `ghidra.log` directly, not `compare.json`, for failure presence, `Invalid index` and EOF sets, route, fallback and `Untested`. All 15 equal the frozen `expected`/`extra_expectations`, and all 15 retained `ghidra.log`/`script.log` sha256 values match their receipts.
- **Held-out failures (own).** In `git show A:…/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log`, line 451 reads `Invalid index: 22386945`. In `real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log`, line 206 reads `Invalid index: 15606016`. Both equal `eb6c266:predictions/<label>.prediction.json:41`. Neither index occurs anywhere at B (`git grep -F`), so no run leaked into the predictions.
- **Go 1.25 scope is honest.** The only Go 1.25 failure is `calib-aether`, the calibration carrier, whose EOF read was already in r17 at B. The six go1.25.0 synthetics and notesmd-cli were predicted silent and observed silent. The entry's title, `:102-105` and decision-table `:113` all say the 1.25 half rests on calibration plus source.
- **Gate evidence (verified).** In `final-recheck/measure.receipt.json`, the stdout sha256 `9e0e5e0d…` matches and `c3_compare_jsons_with_extra` = 15.

### No-harm (B→A)

- **Blob census.** B has 15713 blobs and A has 16482: 15698 identical, 15 modified, 769 added and 0 deleted. All 15 modifications are scoped to the round:
  - three pin fixes;
  - round-17 tools `carrier-run.py`, `compare.py`, `log-extract.py` and `receipt-validate.py` (mid-map retention, C3 parsing);
  - the restored SUMS line;
  - LOG, SCORECARD, SKILL, QUALITY, README, SOURCES and the r17 knowledge entry.
- **Append-only records.** `LOG.md` (94/0) and `SCORECARD.md` (45/0) are prefix-exact, checked with `cmp -n` against the B byte size (own). The r17 knowledge entry is 9/0 and prefix-exact, and no prior lesson changed.
- **Scores.** No owned score decreased: calibration, depth and coverage stay at 10.0, and saturation 10.0 and window 10 are unchanged. `SKILL.md` is 54/7; the 7 deletions are rewritten registry rows. Root `README.md` and `PROVINCE.md` are unchanged.
- **Corpus maps.** The coverage map goes 95/95 → 96/96 with 0 missing and 0 dangling. SOURCES rows go 32 → 36 (own `grep -cE`). In S001–S032, only the `used-by` cells of S003 and S023 changed, as appends (own `git diff -U0`).
- **Hygiene.** No `__pycache__`/`.pyc` is committed and there are 0 `local://` pointers. `/tmp` appears only as REA session-path metadata; the logs themselves are committed.

### Waves and installs

- **W1.** 89 seats in one dispatch: executor 19, scout 23, reviewer 15, scribe 10, connector 8, critic 6, revenger 4, sentinel 2, simplifier 2. There are 89/89 reports.
- **W2.** 98 seats in one dispatch: reviewer 53, executor 9, scout 9, critic 8, mutation-tester 4, revenger 4, connector 4, scribe 3, sentinel 2, simplifier 2. There are 94 reports; missing are `GatePRODUCERREV`, `GateSUMSRUNLOG`, `ShonenLines` and `TruthREGISTRY`.
- **Totals.** 187 seats in total, within 200; no per-seat `model` key; the L2 floor is met.
- **Dead seats.** The causes (policy refusal, 429s) appear only in the fleet report and erratum. The committed `wave2-result.txt` and registration files record the four seats only as `kind:"spawn"`. `SCORECARD.md:2462` still says "1 dead … 4 not returned" against the erratum's 3 dead (routed).
- **Go installs.** `~/.local/opt/go-1.24.6` and `go-1.25.0` exist, `bin/go version` reports go1.24.6 and go1.25.0, and `command -v go` finds none. The `go.dev/dl/?mode=json&include=all` sha256 values `bbca37cc…8712` and `2852af0c…b613` equal the report's. Tool, version, channel and reason are recorded in the fleet report (`:90`), but no install record is in `corpus/lessons/round-18.md` (minor). Pacman was paused, which justifies the tarball channel.

## Outside discernment sample

Sources were re-opened 2026-10-20. "Own" means I re-opened the source personally; a closure seat re-opened the other rows, and I adjudicated them.

| Item | Gate decision | Re-opened source | Outside decision | Reason |
|---|---|---|---|---|
| S034 Go 1.24 notes (own) | admit (mined) | `curl -sL https://go.dev/doc/go1.24`: sha256 `d35c2d52…c4e7` equals the row. Raw line 572 is inside the 571–573 anchor; tag-stripped text contains the quoted sentence contiguously | agree | The quote is exact at 21 words (≤25). It grounds the Swiss default and the opt-out; the row correctly makes no Go 1.25 claim |
| S035 `internal/abi` | admit (mined) | raw go1.25.0 `map_select_swiss.go:22` and `type.go:358-362`; `cmp` against local `~/.local/opt/go-1.25.0` | agree | Both quotes are exact, local equals upstream, and the recorded hashes match |
| S036 jj 0.45.1 | admit (mined) | raw `v0.45.1/docs/git-compatibility.md:114-116` | agree | The quote is exact, including the upstream "there is not concept" typo, and the sha matches |
| S033 PR #9348 | admit (B, supersedes S032) | `git ls-remote … refs/pull/9348/head` → `a214355…`; `.patch` sha `ae5dc2e3…` ×2 | agree | Title, head and patch digest reproduce. Tier B is correct for community material |
| go1.25 notes as a Swiss source (own) | reject | `curl -sL https://go.dev/doc/go1.25 \| grep -ci -e swiss -e noswissmap` → `0` | agree | The page cannot ground the claim; S031 already registers it |
| jj `latest` as the S036 anchor | reject | `docs.jj-vcs.dev/latest/git-compatibility/` links to `main`; raw `main` ≠ `v0.45.1` | agree | An unversioned anchor violates the CORPUS anchor rule |
| "Go 1.25.0 Swiss carriers are safe" | reject | `s1250-swiss-nethttp` prediction (H1 `slot_size=40`, `pkg_path=40`, `mcount=0`), run `all_match`, no failure lines; entry `:87-96` | agree | Silence comes from a name with no pkgPath, not from a correct read. The entry labels the silent-case reading INFERENCE (no program-database inspection) |

Required census (own):

```text
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
exit=0
```

The W04 warning is expected: S033 is the superseding row for S032 at a narrower, re-anchored scope, and CORPUS rule 2 requires the correction to be a new row.

## Axis and trend verdicts

| Axis | Verdict | Scope / evidence |
|---|---|---|
| calibration | improved | Routed defects 6 → 0, re-derived per defect from blobs. QUALITY 20 → 21, with rows 1–20 identical and #21 grounded in the r17 partial disagreement (`round-17-verifier-spotcheck.md:108`). Both items the author marked not checkable offline verify here |
| operability | improved | Live HEAD-keyed pins 3 → 0 by independent grep, and the jj sandbox holds 14/14. The disclosed limits (nested compare reads, HEAD aliases) stand |
| depth | improved | 15/15 frozen-before-run predictions match the raw logs, and both held-out indices are exact. The scope is held to Go 1.24 held-out plus 1.25 calibration |
| coverage | unchanged | 95/95 → 96/96 is index integrity on held Go ground |
| freshness | unchanged | S033 re-read the PR state. The PROVINCE REA-pin drift was caused outside the lane (13:35:56 config rewrite); it is disclosed and carried |
| adjacency | unchanged | Nothing was absorbed. The jj-doc triple registration is reported, and the revenger/kaidoku contest stays integrator-owned |

- **expansion: unchanged.** The new entry deepens held Go ground. There is no new coverage-map row and no capability row.
- **quality: improved.** The r17 aether INFERENCE is superseded by a frozen-before-run replay that I re-derived 15/15 from raw logs. The six r17 overstatements are corrected append-only. S032 is superseded by S033, whose head and patch digest reproduce. No admitted entry failed its re-check.
- **discernment: improved.** This outside sample agrees on 7/7 decisions: 4 admits (S033–S036) and 3 rejects. The one r17 partial disagreement became the grounded QUALITY #21 with a lesson behind it, so no disagreement is left unlearned.

SHONEN is **not** fully checkable by a non-author: instructions are not outside-executed, and `PROVINCE.md:8-26,44` is stale on REA pins. All four `[~]` remain, and promotion is operator-owned.

## Routed defects (kaidoku, next round; status-neutral)

1. **R18-MIDMAP-LISTSTEP.** `.ufo/waves/round-17/tools/receipt-validate.py:576-578`: under `--require-mid-maps`, a list-shaped `steps` passes if *any* step has `pin_checks`. The `analyze` step is not required, which contradicts the flag's documented contract. Real round-18 receipts are object-shaped, so the 15/15 result is unaffected. Require the `analyze` step in the list branch and add a red fixture.
2. **R18-VALIDATOR-DIGEST.** `routed-defects.py` `validator-sha256-pinned` checks only the format. Compare it with `git show 9011581:.ufo/waves/round-17/tools/receipt-validate.py | sha256sum`; the value is correct today (`618448829ba6…126f`) but is unguarded. Also retain the digest of each remapped receipt copy in `validate16/summary.json`, so the input binding stops resting on prose.
3. **R18-STRICT-BASELINE.** The "exit 1 at `9011581`" for `routed-defects.py --strict` (SCORECARD round 18, report) has no retained receipt. The verification pass keeps only the non-strict baseline (open 6, exit 0). Retain the strict baseline run.
4. **R18-HEAD-ALIASES.** citation-drift `:329` refuses only the literal `HEAD`, so `@`, `HEAD~0` and `HEAD^{commit}` pass. The two nested compare-only reads (`round-17/verify.py:83`, `revpin.py:108`) are invisible to `head-rev-lint.py`. Carried in the lesson's Open list; fix it or register the limits in the SKILL rows.
5. **R18-DEADSEAT-RECORD.** `SCORECARD.md:2462` says "1 dead … 4 not returned (GatePRODUCERREV, TruthREGISTRY, DecisionRuleApply, ShonenLines)", while the report erratum says 3 dead. The committed wave-2 records hold no error text for any dead seat. Append a correction and retain the failure causes.
6. **R18-REGISTRY-PINNED.** The `pins` ("none") and `go-buildinfo-probe` (constants in code) rows name no pinned-value path. The gate checks only the token, so name the path or state that the row is a probe with no persisted baseline.
7. **R18-INSTALL-RECORD.** Go 1.24.6/1.25.0 (tool, version, channel, sha, reason) are recorded only in the fleet report. Add the record to the round lesson, as round 17 did.

Carried open (lane-owned, already listed in `round-18.md` Open):
- PROVINCE REA-pin drift: client configs are now `rea-agents@6.7.0`.
- custody-pair `repo-root` records the argument.
- jj-red-before env scrub and path guard.
- `revpin.py:6` `@-` wording.
- The r12 S###/custody/operability-decision items.

Operator/protocol (not lane debt): the template's §3 L2 split lists `1× planner`, while the hyaku §6 addendum moves the planner seat to the L1 because the validator rejects the role. One of the two needs reconciling.
