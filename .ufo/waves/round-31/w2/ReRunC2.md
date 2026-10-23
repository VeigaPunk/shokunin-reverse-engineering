# ReRunC2 — R31-C2 counter re-run at lane tip (falsify wave 2)

- Seat: `KaidokuR31.ReRunC2` (UFO-FSD reviewer, leaf — no subagents)
- Runs: 2026-10-23T01:30Z (UTC); report written 2026-10-23T04:31Z
- Assignments: re-run C2 counter at lane tip, diff vs committed receipt, run `--selftest`

## Commands executed

1. Lane revision check (read-only git):
   `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse 1288285eed81395e6af7c279a173b117b2c2eaa3`
   → `1288285eed81395e6af7c279a173b117b2c2eaa3` (commit 1792729627, "round-31: SCORECARD … C2 23/23 …").
2. Measure run:
   `cd /fast/scratch/hyaku/kaidoku-r31/seats/w2/ReRunC2 && TMPDIR=/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReRunC2/tmp timeout 900 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c2-sqlite-refusals.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 1288285eed81395e6af7c279a173b117b2c2eaa3`
   (measure mode; no `--write-evidence`; lane untouched).
3. Diff vs committed receipt:
   `diff /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-31/after/c2-sqlite-refusals-at-0007731e.txt out-measure.txt`
4. Selftest:
   `cd /fast/scratch/hyaku/kaidoku-r31/seats/w2/ReRunC2 && TMPDIR=… timeout 300 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-31/c2-sqlite-refusals.py --selftest`

## Verdicts per checked item

| Item | Verdict | Evidence |
|---|---|---|
| Lane tip rev exists | holds | rev-parse output, commit subject |
| REA pin 6.5.0 present | holds | `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` exists, `version == 6.5.0` |
| Measure run at tip | holds | exit `0`; summary line exactly `requests=23 matches=23 target=23 entry_ok=1 (ok) skill_ok=1 (ok)`; stderr empty; wall 18.37s |
| All 23 request rows = P2-match | holds | each row printed `P2-match` with the frozen code/reason/message (e.g. `q-missing-table … refused invalid_request invalid_format`, `q-ok-rows … accepted, 3 Album rows`, `m-journal-empty … accepted, report equals oracle`); any committed-envelope mismatch would have downgraded to `P2-miss` |
| Diff vs committed receipt | holds | only difference: the receipt's trailing `exit=0` trailer line (L1-added; same trailer on C1 receipt; not counter stdout). All 23 request lines + summary byte-identical |
| Selftest | holds | exit `0`; `selftest cases=12 failures=0`; all 9 judge cases + 3 strip_meta cases `ok` |
| Counter code unchanged between receipt commit and tip | holds | `git diff --stat 0007731e..1288285 -- tools/round-31/c2-sqlite-refusals.py tools/round-31/sqlite_oracle.py` → empty; `git log 0007731e..1288285 -- <files>` → no commits |

## Findings by severity

No concrete defect found in scope. No overstated or unbacked behavior observed.

Observations (label: observation for each):
- The committed receipt is a faithful record: the re-run at the lane tip reproduces it exactly (modulo the L1 `exit=0` trailer). P2-match holds at the tip.
- PIN checks inside `measure()` ran and passed silently: base carrier `chinook.sqlite` sha256, each mutant sha256 (zero-magic/pagesize-768/journal-hot/journal-short/journal-empty/journal-zero28/journal-symlink/wal-sparse/sparse-268435457) and mutant siblings, carrier shas from the frozen list, predictions file equal to the rev, `len(rows)==23`. Exit 0 means none of the PIN guards fired (`PIN … absent or altered` would have produced exit 2 and a required L1 report; none occurred).
- Single-identity rerouting: every request path is the frozen absolute path under `/fast/scratch/hyaku/kaidoku-r31/{carriers,mutants}/`; `run_rea` invokes `npx -y rea-agents@6.5.0 inspect-sqlite-database <path> <args> --format json --full-output` live per row.
- Committed-envelope rule (M30-3 repair) exercised: in measure mode, every matched row runs `committed_check`, requiring the git-stored envelope at the tip to (a) exist, (b) be first added after the freeze commit (claims.json `--diff-filter=A` time), (c) be valid JSON, (d) equal the live envelope in every field except `meta`; all 23 passed (else verdict would be `P2-miss` with a reason).

## Residual risk / verification gaps

- I did not run `--write-evidence` (it writes into the lane corpus — forbidden read-only). Envelope equality therefore rests on `committed_check` against git-stored envelopes at the rev, which passed for all 23; envelopes were not regenerated.
- [INFERENCE] The live `npx` binary is REA 6.5.0: the pinned cache package.json (the path the counter itself validates) reports 6.5.0, and the spec `rea-agents@6.5.0` is exact; I did not independently trace the npx resolution at run time.
- The receipt was produced at `0007731e`; the counter file is unchanged between that commit and the tip, so the comparison is directly meaningful.

## Artifacts (all under `/fast/scratch/hyaku/kaidoku-r31/seats/w2/ReRunC2/`)

- `out-measure.txt` — sha256 `d28f042036fef2af8e4f32cf33b02ae92bbbfacf9c1f43c5227eccf76a85386d`
- `err-measure.txt` — empty; sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `out-selftest.txt` — sha256 `7980ca43b4cae5894cae1371172ab2a2cabe01f1d88a0c425e0038947ca871bb`
- `err-selftest.txt` — empty; sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- `tmp/` — TMPDIR for REA runs

## Tooling

No tools installed or updated (nothing needed; no pacman transactions, no uv/npx installs).

## Verdict

P2-match HOLDS for all 23 requests at the lane tip `1288285e`. The committed receipt equals the re-run exactly (modulo the L1 `exit=0` trailer). Nothing falsified in scope.
