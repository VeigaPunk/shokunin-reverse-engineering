# CriticPreregistration — r17 w2 FALSIFY (KaidokuR17.CriticPreregistration)

Target: the claim that predictions were committed at `271167473d87ef710f07ecdd98caf0ce12091686` before any final run, and the label "prospective" on the six `pro-*` carriers.
Revision attacked: `da64646adcb19c1ede7537b799b8c7d283fe43da`. Axes: calibration, depth.
Read-only. I ran no REA analyze/search/decompile, no Ghidra, and no carrier. I installed nothing. My only scratch file was `/tmp/kr17-critpre-pats.txt`, which I removed.

## Verdict

- **Pre-registration timing holds.** The freeze is corroborated by an external witness: a GitHub PushEvent 18 s after the commit and before the first analyze. No prediction byte changed between the freeze and integration.
- **"Prospective" is earned in time and bytes for all six `pro-*` carriers.**
- **"Six prospective" overstates how many independent predictive tests the round has.** Three of the six repeat a route branch that had already been observed before the freeze (F1). Two minor provenance gaps follow (F2, F3).

## Checks with no finding (bounded)

**N1 — Commit order is corroborated by four independent clocks.** Observation.
- `git log --format='%H %ai | %ci'` shows `2716747… 2026-10-20 10:46:45 -0300` (author = committer) and `da64646… 11:06:06`.
- `git reflog --date=iso`: `2711674 HEAD@{2026-10-20 10:46:45 -0300}`.
- Loose object mtime: `stat .git/objects/27/1167473d…` gives `10:46:45.380`.
- Remote-tracking reflog: `2711674 refs/remotes/origin/main@{2026-10-20 10:46:47 -0300}: update by push`.
- **External witness:**
  ```
  gh api 'repos/VeigaPunk/shokunin-reverse-engineering/events?per_page=100' --jq '…PushEvent…'
  {"before":"b563c799…","created_at":"2026-10-20T13:46:48Z","head":"271167473d87ef710f07ecdd98caf0ce12091686"}
  ```
- The earliest analyze start in any receipt is `calib-shfmt` `steps.analyze.started_at_utc` `13:47:06.688621Z`. The earliest `pro-*` start is `pro-notesmd-cli` `13:49:25.022848Z`. Both come after the GitHub-recorded push.

**N2 — No prediction was edited after any observation.** Observation. For each label I compared five values: the receipt `pins_pre` and `pins_post` sha256 of `predictions/<label>.prediction.json`, `git show <rev>:…` at 2716747 and at da64646, the file on disk, and `predictions/SHA256SUMS`. All five are equal for all 8 labels: `pins_compare.equal: true`, `changed: []`. Example: `pro-op d13875e23f791ed9` everywhere, and `pro-esbuild-0.27.7 7dc311b6fc6e2eb7` everywhere.
- The pinned prediction `mtime_ns` falls between 10:46:25 and 10:46:38 -03, before the commit.
- `git diff --stat 2716747 da64646 -- predictions claims.json contract.md measure.py controls.py pilot` shows only `tools/buildinfo-probe.py` and `tools/temporal-sweep.py`. Neither one produces predictions.

**N3 — No hidden pre-freeze or repeated analyze run of any `pro-*` carrier was found.** Observation, bounded.
- (a) `carrier-run.py:263` creates `tempfile.mkdtemp(prefix="kr17-rea-")` and only the selftest removes roots (`:513`, `:587`). `ls -ld /tmp/kr17-rea-*` shows exactly 8 directories, created between 10:47:37 and 11:00:05. Each one is the single `bound_sessions` entry of exactly one receipt, with `unbound_sessions: []`.
- (b) `/tmp/kr17-pilot` holds exactly two sessions, `logs/rea-ghidra-LuPZRm` (10:17:27) and `logs2/rea-ghidra-r9xmGu` (10:18:19), which are shfmt and esbuild 0.25.12.
- (c) REA analyze Evidence IDs are deterministic: the calib runs reproduced the pilot IDs. I searched the 8 analyze IDs across `/home/vgpnk/Projects` (grep, gitignore off) and across `/tmp` and `/var/tmp` (`rg -l -F -f`). The six `pro-*` IDs appear only under `round-17/runs/`, the r17 knowledge entry, and a post-commit checkout `/tmp/r17-da646` (mtime 11:06:06).
  - The pre-freeze `/tmp` files that hold `pro-*` carrier sha256s are `rea-go.json` 10:32, `census-stdout.json` 10:37, and `r17-inspect-esb21/27.json` 10:39. All contain `"operation":"inspect_go_binary"`, which is build-info only, and 0 analyze IDs.
- Limit: an analyze run under the default TMPDIR whose stdout was thrown away would leave no trace, because REA deletes `rea-ghidra-*`. That case cannot be excluded.

**N4 — Pilot timing is as stated.** Observation.
- Pilot files in `/tmp/kr17-pilot` run from 10:17:26 to 10:19:55. `pilot/README.txt:1` says "~10:17-10:19".
- `sha256sum -c pilot/SHA256SUMS` returns 6/6 OK, and `cmp` shows the repo pilot JSON is identical to the `/tmp` originals.
- The pilot analyzed only the two `calib-*` carriers. `carriers.tsv:1-2` labels them "calibration (pilot-seen)", and `knowledge …r17-go-carrier-diagnostics.md:37-38` discloses this.

## Findings

### F1 — "six prospective" counts three branch replicates as independent predictive tests (calibration, medium)

Where:
- `SKILL.md:515` "Eight of eight matched, including six prospective carriers."
- `corpus/lessons/round-17.md:26` "8/8 compare exit 0 (6 prospective)".
- `predictions/carriers.tsv:3-8`.

Counterexample (observation). The fields that `compare.py` checks are a function of the r16 selection status alone (`tools/predict.py:43-45`: `missing_bootstrap` iff `missing_base`). Three `pro-*` carriers fall on a status that had already been observed, with the same Ghidra 12.1.4, before the freeze:

| pro carrier | predicted route / status | already observed before freeze on |
|---|---|---|
| `pro-containerd-shim` go1.27.2-X:nodwarf5 | none / `missing_base` | `calib-shfmt` go1.27.0-X:nodwarf5, pilot 10:17 (`pilot/shfmt-log/ghidra.log`): same status, same Arch toolchain suffix |
| `pro-op` go1.26.8 | none / `missing_base` | `calib-shfmt` pilot (same status). Also `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:19,69-72`: op 2.40.0 **go1.26.8** on **Ghidra 12.1.4**, where "`Missing Go bootstrap type info` seen in its `ghidra.log`" |
| `pro-esbuild-0.21.5` go1.20.12 | info / `exact_diff` | `calib-esbuild-0.25.12` go1.23.12, pilot 10:18 (`pilot/esbuild-0.25.12-log/ghidra.log`, INFO line, per `w1/SelectionPreviewRun.md:27-43`) |

Only three `pro-*` carriers exercised a route that nobody had observed at freeze time:
- `pro-notesmd-cli` and `pro-aether`: the fallback WARN. The knowledge entry's own ":68 the fallback WARN is real" is its first observation.
- `pro-esbuild-0.27.7`: no build-info, hand-predicted.

So the round has **2 new branches tested prospectively, across 3 carriers**, plus 3 prospective replicates of calibration branches. w1 had already flagged this structure: `w1/CriticSampleSize.md:78-81` called notesmd-cli "the only predictive row" and esbuild 0.21.5 "a replicate; adds no branch", and `w1/CriticC2Novelty.md:38-39,75` noted that op shares r4-10's Go version. The integrated summary line drops that distinction.

Impacted axes: calibration (the success rate is read as 6 independent tests) and depth (the novelty of the predictor is overstated).

Smallest fix, wording only: keep "prospective" (it is earned in time and bytes), and qualify the count at `SKILL.md:515` and `lessons/round-17.md:26` as "six prospective carriers (three on routes unseen at freeze: fallback ×2, no-build-info ×1; three replicate pilot-seen routes)". Optionally, label `carriers.tsv` rows 5-7 as "prospective (replicate of calib route)".

### F2 — the run harness and the full run sequence are not frozen or retained (provenance, low)

- `run-carriers.sh` is not in the freeze commit. `git diff --name-status 2716747 da64646` shows `A .ufo/waves/round-17/run-carriers.sh`, and its file mtime is 10:47:01, 16 s after the freeze. Its header (`run-carriers.sh:2`) nonetheless says "predictions frozen … before any run". The per-run `orig_argv` in each receipt is retained, so this does not threaten pre-registration.
- `runs/run-log.txt:1` starts at `== calib-esbuild-0.25.12 start 2026-10-20T10:47:42` and has no `calib-shfmt` lines, although `calib-shfmt` ran 13:47:05–13:47:37Z (receipt).
  - The gap from shfmt's `compare.exit` (10:47:37.412) to the esbuild start is about 4.6 s. Every later end→start gap in run-log is 0 s.
  - Inference: shfmt was a separate `run-carriers.sh calib-shfmt` invocation. The other seven were launched by a wrapper invocation that is not retained. A full loop of the script as written would have re-run shfmt first, because it does `rm -rf "$out"` (`run-carriers.sh:15`).
  - This conflicts with QUALITY #18 (retain the producing argv).
- Smallest fix: append one line to `runs/run-log.txt`, or a note beside it, giving the exact shell invocation(s) and stating that shfmt ran separately at 10:47:05–10:47:37. Keep the script header but note that it was added at 10:47:01, after the freeze.

### F3 — "before any run" is literally false for the two calib carriers (calibration, low)

- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:1` and `run-carriers.sh:2` say "predictions frozen … before any run".
- The pilot analyze runs at 10:17–10:19 came before the 10:46:45 freeze, and the `calib-*` predictions were therefore written after their routes had been observed.
- The entry corrects this at `:37-38`, and `lessons/round-17.md:26` already uses the precise wording "before the first run".
- Smallest fix: change `:1` to "before any measured run (the pilot at 10:17–10:19 preceded it; calib-* are pilot-seen)".

## Notes (not findings)

- `claims.json:5` has `declared_at` "10:25:00-03:00", but the file mtime is 10:21:53. The declared time is later than the last write, so it is a hand-entered approximation. It has no effect on prediction order.
- `pro-esbuild-0.27.7` carries `extra_expectations` (for example `analyzer_errors_contain`) that `compare.py` does not check: its compare.json lists only the 5 standard fields. The entry's table row `:58` reports those facts from the log, not from compare.
- This overlaps the scope of peer seat `CompareAttack`, so I did not pursue it.

Tool installs: none.
