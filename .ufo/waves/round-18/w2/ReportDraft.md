HOLDS

Seat: KaidokuR18.ReportDraft (wave 2, scribe, author-side advisory). Task: draft the round-18 report sections "Work performed" and "Before → after measurements" from REV evidence only. REV = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (lane HEAD, `git rev-parse HEAD` exit 0); baseline = `9011581d84527ba34c675f9cf912e54d2e72d470`; freeze = `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. Tracked tree equals REV (`git status --porcelain` exit 0 lists only untracked wave-2 scratch: `carriers/bin/`, `gen-wave2.py`, `w2/`, `wave2-assignments.json`, `wave2-dispatch.json`), so working-tree reads of tracked files are REV reads; tool files were read with `git show REV:path`.

Verdict HOLDS: every before→after number in the amended claims (`.ufo/waves/round-18/claims.json:37-39`) re-derived exactly from REV evidence with the commands below. Two wording findings in LOG (F1, F2) are low-severity and leave no number wrong.

## Draft

### Work performed

**Wave 1 (before any measurement).** Round 18 ran 89 wave-1 seats in one validated `task` call (`LOG.md:2133-2134`): `wave1-registry.json` `.members` has 89 entries, with roles scout 23, executor 19, reviewer 15, scribe 10, connector 8, critic 6, revenger 4, sentinel 2 and simplifier 2. `wave1-dispatch.json` `.counts` is `{spawn: 89, resume: 0, total: 89}`, and `.ufo/waves/round-18/w1/` holds 89 `*.md` reports (commands C-17..C-19). Critics changed the round before anything was measured (`LOG.md:2135-2139`; amendment `claims.json:35-36`):
- The C1 token checks were circular.
- C2's "3" came from audit prose.
- C3's methods/nomethods pair was predicted non-diagnostic.

The fixes were substance checks, a scope rule written before measuring, four nethttp carriers plus one real carrier, and a frozen decision rule.

**Tool changes (in place, contracted)** (`LOG.md:2140-2147`), each confirmed in the file at REV:
- citation-drift: when `--rev` is omitted, it resolves to `refs/heads/<branch>`. A literal `--rev HEAD` is accepted only when it equals the branch tip (`.ufo/gates/citation-drift/citation-drift-probe.py:44,314-333`).
- custody-pair: emits `# repo-branch-tip:`, `# repo-HEAD-is-branch-tip:` and `# repo-dirty:` (`.ufo/gates/custody-pair/custody-pair.py:113-121,410-411`).
- round-17 `verify.py`: pins `refs/heads/main` and refuses otherwise (`.ufo/waves/round-17/verify.py:11,110`).
- `carrier-run.py`: writes each mid-run pin map to `pins/mid-<n>.json` with a digest (`.ufo/waves/round-17/tools/carrier-run.py:7-8,371-372,495`).
- `receipt-validate.py`: gains `--require-mid-maps` (its `--help` output; `SKILL.md:541`).
- `log-extract.py`: gains `eof_reads`, `invalid_index_reads` and `symbol_analysis_failures` (`.ufo/waves/round-17/tools/log-extract.py:14-15,24-32,170-172`).
- `compare.py`: gains the matching expectations `analyzer_errors_empty`, `eof_reads` and `invalid_index_reads` (`.ufo/waves/round-17/tools/compare.py:197-206,207,212`).

The backward-compatibility claim (`LOG.md:2148-2149`) has three parts, each recorded by the seat that produced it at REV:
- All 16 r17 logs keep their old fields byte-equal (`w1/LogExtractEof.md:70,100,103`).
- All 8 r17 compare outputs are byte-identical, with exits unchanged 0→0 (`w1/CompareEofFields.md:52`).
- All 8 r17 receipts exit 0 without the new flag and exit 1 `mid_map_missing` with it (`w1/CarrierRunMidMaps.md:152-157`).

This seat did not re-run these; see Limits.

**Prediction freeze before any run.** Predictions for 15 labels, `decision-rule.json` and `SHA256SUMS` were committed at `eb6c266…`, with commit instant `2026-10-20T13:23:55-03:00` (= 16:23:55Z) (`LOG.md:2150-2151`; `SKILL.md:565`; C-15). The first carrier started at `13:24:07-03:00` (`.ufo/waves/round-18/runs/run-log.txt:2`), 12 s later; the ordering follows from comparing the two instants. The freeze is intact at REV:
- `git diff eb6c266… b2aad08… -- .ufo/waves/round-18/predictions` is empty (C-8).
- `sha256sum -c predictions/SHA256SUMS` verifies 32/32 (C-9).

`eb6c266` is an ancestor of the local `refs/remotes/origin/main` (= `b2aad08`) (C-23). That shows a push; it does not show when the push happened.

**Carrier pass.** One pass of 15 labels ran under `run-carriers.sh` at producing revision `eb6c266…`, from `13:24:07` to `13:32:10-03:00`. Every label ends `carrier-run=0 compare=0`, and the last line is `run-carriers exit=0` (`.ufo/waves/round-18/runs/run-log.txt:1-32`; `LOG.md:2151-2153`).

**Routed r17 corrections (append-only).**
- **R17-VALIDATE16** (`LOG.md:2159`; `SCORECARD.md:2439`): the 8 `da64646` first-pass receipts validate 8/8 exit 0 under the `9011581` validator, using prefix-remapped copies. Evidence: `.ufo/waves/round-18/evidence/validate16/summary.json:2-81` has 8 entries, all `exit: 0`, with `rev` `da64646…` (`:80`) and `validator_rev` `9011581…` (`:81`).
- **R17-SUMS-RUNLOG** (`LOG.md:2160`): the dropped `carriers.tsv` manifest line is restored. Evidence: `.ufo/waves/round-18/evidence/sums-runlog.json`; the routed-defects checks `sums-restored-from-2711674`, `carriers-tsv-identical` and `log-fraction-true` all pass at REV (C-5).
- **R17-PRODUCER-REV** (`LOG.md:2161`; `SCORECARD.md:2440`; `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:206`): pass 1 was produced by `271167473d87…` and pass 2 by `95e34db62f26…`. Both are ancestors of REV (check `producer-revs-are-ancestors`, C-5).
- **R17-PINMAP**: the correction is appended in the r17 knowledge entry (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:204-205`) and in `SCORECARD.md:2438`.

**Landed artifacts** (`LOG.md:2162-2167`):
- Knowledge entry `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:1-3`, with sources, a `verified-at` line that labels itself author-side, and `recheck:` commands.
- QUALITY #21 at `corpus/QUALITY.md:31`.
- SOURCES rows S033–S036 at `corpus/SOURCES.md:39-42`. The round-18 census line (`corpus/SOURCES.md:67`) reads "included 4 rows (S033–S036); excluded 7".
- Go row token `2026-10-20-r18-swiss-map-replay` at `corpus/README.md:35` (see F1).
- Aligned SKILL rows: citation-drift `SKILL.md:448`, go-route-compare `:540`, receipt-validate `:541`, pins `:542`, go-buildinfo-probe `:545`. The r17 aether row is qualified in place at `:528`.
- Two round-18 SKILL sections: "Swiss-map misread replay — round 18" at `SKILL.md:548` and "Revision pins under jj — round 18" at `:567`.
- Lessons `corpus/lessons/round-18.md`, whose `## Mistakes` section (`:58`) has rows 1–5 at `:62-66` (named at `SCORECARD.md:2432-2433` and `claims.json:31`).

### Before → after measurements

This seat re-derived every value below. Baseline values are Git-object reads at `9011581…`; after values are reads at `b2aad08…`.

| Claim | Metric | Before | After | Command |
|---|---|---|---|---|
| C1 | open routed R17 defects (named / substance) | 6 (6 / 6) | **0** (0 / 0) | C-4, C-5 |
| C1 | QUALITY data rows (rows 1–20 byte-identical) | 20 | **21** | C-13 |
| frontier | SOURCES rows | 32 | **36** | C-14 |
| C2 | live HEAD-as-revision call sites | 3 | **0** | C-6, C-7 |
| C2 | jj sandbox expectations held | — | **14/14** | `evidence/jj-red-before.json` |
| C3 | labels with bound retained log + compare carrying `extra.eof_reads` | 0 | **15** | C-16 |
| C3 | Swiss-map mechanism status | unreplayed INFERENCE | **replayed-confirmed** (frozen rule) | C-20, C-21 |

**C1 (calibration).** The command is `routed-defects.py --root . --rev <REV>`; both runs exit 0.
- At `9011581…`: `open_count: 6`, `named_open_count: 6`, `substance_open_count: 6`. All six defects are open: R17-PINMAP, R17-VALIDATE16, R17-PRODUCER-REV, R17-SUMS-RUNLOG, R17-REGISTRY and R17-S032-DIGEST. For example, R17-PINMAP reports "SCORECARD.md: no line containing 'R17-PINMAP' + 'comparator verdict'", and `r18-receipt-pinmaps` reports ".ufo/waves/round-18/runs/ absent at rev".
- At `b2aad08…`: `open_count: 0`, and every named and substance check is `ok: true`. For example, `r18-receipt-pinmaps` reports "runs/calib-aether/receipt.json: 3 pin_checks each carry map_path + verified map_sha256".
- This matches amendment C1, "Before 6 at 9011581 (named 6, substance 6) -> after 0" (`claims.json:37`).
- QUALITY grows 20 → 21: `git diff 9011581… b2aad08… -- corpus/QUALITY.md` is a single added line (row 21, `corpus/QUALITY.md:31`) with no modified or removed lines. Rows 1–20 are therefore byte-identical.
- SOURCES grows 32 → 36 (`claims.json:31` "SOURCES census before (exit 0, 32 rows)").

**C2 (operability).** The command is `head-rev-lint.py --root . --rev <REV>`; both runs exit 0.
- At `9011581…`: `live_count: 3`, at exactly the three amended sites:
  - `.ufo/gates/citation-drift/citation-drift-probe.py:477` `ap.add_argument("--rev", default="HEAD")`
  - `.ufo/gates/custody-pair/custody-pair.py:327` `["git", "rev-parse", "HEAD"],`
  - `.ufo/waves/round-17/verify.py:59` `source = git("rev-parse", "HEAD")`

  Also `fixture_count: 8`, `annotated_count: 0`, `files_scanned: 27`.
- At `b2aad08…`: `live_count: 0`, `fixture_count: 15`, `annotated_count: 6`, `files_scanned: 39`. The six annotated sites are `citation-drift-probe.py:304`, `custody-pair.py:381,1350,1353` and `jj-red-before.py:377,659`, each tagged `head-rev-lint: compare-only` or `red-before`. Excluded seat-directory sites are listed with reasons.
- This matches amendment C2 (`claims.json:38`).
- Sandbox receipt `.ufo/waves/round-18/evidence/jj-red-before.json`:
  - `"all_held": true` (`:2`)
  - `expectations` array (`:39-174`): 14 entries, all `held: true`
  - `"not_runnable": []` (`:180`)
  - `baseline_rev` `9011581…` (`:37`)

**C3 (depth).**
- **Count 0 → 15**, under the frozen `count_rule` (`.ufo/waves/round-18/predictions/decision-rule.json:8`). Before: `.ufo/waves/round-18/runs/` does not exist at `9011581…` (C-4 check detail). After: each of the 15 run directories has exactly one `logs/rea-ghidra-*/ghidra.log`, a `compare.json` carrying `extra.eof_reads`, and `all_match: true` (C-16).
- **Binding gate** (`decision-rule.json:2`): all three clauses hold for 15/15 labels.
  1. `receipt-validate.py --require-mid-maps` returns `{invalid: 0, receipts: 15, unreadable: 0, valid: 15}`, exit 0 (C-12).
  2. Each prediction's carrier sha256 equals its receipt's `sha256_pre`/`sha256_post` (C-22).
  3. Prediction blobs are unchanged since the freeze (C-8, C-9).
- **Observed outcomes**, per-label from `runs/<label>/observation.json` (C-20). Exactly three labels carry a `Go analysis failure`:
  - calib-aether: `eof_reads [[17645861, 111938854]]` (calibration only)
  - s1246-swiss-nethttp: `invalid_index_reads [22386945]`, `snapshot_route: info`
  - real-kimi-webbridge: `invalid_index_reads [15606016]`, `snapshot_route: fallback`, `fallback_to ["1.24.6"]`

  The other 12 labels have `analyzer_errors` and `symbol_analysis_failures` both empty. That includes the noswiss sibling s1246-noswiss-nethttp, the other Swiss nethttp carrier s1250-swiss-nethttp, and calib-notesmd-cli. The two held-out `Invalid index` lines also appear verbatim, once each, in the bound logs (C-10, C-11). This matches "both exactly as frozen" (`LOG.md:2153-2156`).
- **Predicted against observed** (C-21):
  - H1 predicts failure on exactly {calib-aether, real-kimi-webbridge, s1246-swiss-nethttp}; H0 predicts failure on none.
  - The observed failure set equals the H1 set exactly (`H1==observed: True`).
  - H1 and H0 disagree on only those 3 labels.
- **Verdict.** Under the frozen `confirmed` clause (`decision-rule.json:7`), the mechanism status moves from unreplayed INFERENCE to **replayed-confirmed** (`LOG.md:2157`; `claims.json:39`). The three conditions were each read directly from the observations:
  - each held-out D label (`decision-rule.json:15-18`) shows its exact H1 outcome;
  - the noswiss sibling shows no failure;
  - no non-D synthetic label fails.
- **Calibration note.** The 12 labels where H0 and H1 agree test only the "no spurious failure" arms. The H1-versus-H0 discrimination rests on 2 held-out labels, because calib-aether calibrated the emulator (`decision-rule.json` `calibration_only`).
- **Real carrier.** `.ufo/waves/round-18/evidence/real-carrier-census.json` classifies 35 binaries as 31 go-toolchain, 3 r17-carrier and 1 real-application: `/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge`, go1.24.13. This is the only real non-r17 Go 1.24/1.25 ELF (`claims.json:39`). It exercised the first intermediate patch fallback, WARN 1.24.13 → 1.24.6 (`LOG.md:2157-2158`; its `compare.json` `fallback_to`).

## Findings (author-side; wording only, no number affected)

- **F1 (low, observation):** `LOG.md:2164` says "README Go row token (in place, line 35)", but the lane's top-level `README.md` has 24 lines. The token is at `corpus/README.md:35`. Reproduce: `wc -l README.md corpus/README.md` → `24 README.md`, `190 corpus/README.md`; `grep -n r18-swiss-map-replay README.md corpus/README.md` → only `corpus/README.md:35`. The final report should name `corpus/README.md:35`.
- **F2 (low, observation):** `LOG.md:2155-2156` says "the noswiss sibling and all 11 non-diagnostic synthetic carriers did not fail". The sibling s1246-noswiss-nethttp is one of those 11 (12 synthetic carriers minus held-out s1246-swiss-nethttp), so the phrase counts it twice. It also leaves out calib-notesmd-cli, which did not fail either. Reproduce: C-20, which shows 12 of 15 labels with `ae=0 saf=0`. Suggested wording: "the 11 non-D synthetic carriers (including the noswiss sibling) and calib-notesmd-cli did not fail".

## Commands run by this seat (read-only; cwd = lane root unless noted; python as `python3 -I -B`)

| id | command | exit | result |
|---|---|---|---|
| C-1 | `git rev-parse HEAD` | 0 | `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` |
| C-2 | `git log --oneline -3` | 0 | b2aad08 / eb6c266 / 9011581 |
| C-3 | `git status --porcelain` | 0 | untracked wave-2 scratch only |
| C-4 | `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev 9011581d84527ba34c675f9cf912e54d2e72d470` | 0 | `open_count 6`, named 6, substance 6 |
| C-5 | `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --root . --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94` | 0 | `open_count 0`, named 0, substance 0 |
| C-6 | `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev 9011581d84527ba34c675f9cf912e54d2e72d470` | 0 | `live_count 3`, fixture 8, annotated 0, files 27 |
| C-7 | `python3 -I -B .ufo/waves/round-18/tools/head-rev-lint.py --root . --rev b2aad08ceeee8dd125ce0d316056d8bd766c7f94` | 0 | `live_count 0`, fixture 15, annotated 6, files 39 |
| C-8 | `git diff --stat eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .ufo/waves/round-18/predictions` | 0 | empty |
| C-9 | (cwd `.ufo/waves/round-18`) `sha256sum -c predictions/SHA256SUMS --quiet` | 0 | 32/32 OK |
| C-10 | `grep -c "Invalid index: 22386945" .ufo/waves/round-18/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log` | 0 | 1 |
| C-11 | `grep -c "Invalid index: 15606016" .ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log` | 0 | 1 |
| C-12 | `find .ufo/waves/round-18/runs -mindepth 2 -maxdepth 2 -name receipt.json \| sort \| xargs python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps` | 0 | `{invalid 0, receipts 15, unreadable 0, valid 15}` |
| C-13 | `git diff 9011581… b2aad08… -- corpus/QUALITY.md` | 0 | one `+` line (row 21) |
| C-14 | `git show <rev>:corpus/SOURCES.md \| grep -c '^\| S'` at 9011581 / b2aad08 | 0 | 32 / 36 |
| C-15 | `git show -s --format="%cI %H" eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` | 0 | `2026-10-20T13:23:55-03:00` |
| C-16 | python: per run directory, count `logs/rea-ghidra-*/ghidra.log`, check `compare.json` fields for `extra.eof_reads`, read `all_match` | 0 | 15 labels, each 1 log, `eof_reads` present, `all_match` true |
| C-17 | python `Counter(role)` over `wave1-registry.json` `.members` | 0 | 89; scout 23, executor 19, reviewer 15, scribe 10, connector 8, critic 6, revenger 4, sentinel 2, simplifier 2 |
| C-18 | python read `wave1-dispatch.json` `.counts` | 0 | spawn 89, resume 0, total 89 |
| C-19 | `ls .ufo/waves/round-18/w1/*.md \| wc -l` | 0 | 89 |
| C-20 | python: per label, `analyzer_errors`/`eof_reads`/`invalid_index_reads`/`symbol_analysis_failures` from `observation.json` | 0 | failures only in calib-aether, real-kimi-webbridge, s1246-swiss-nethttp; 12 labels clean |
| C-21 | python: `predicted_failure_h1`/`_h0` from `predictions/swiss-misread/*.json` against observed failures | 0 | H1≠H0 on 3; H1 failure set = observed failure set (`True`) |
| C-22 | python: prediction `carrier.sha256` ∈ receipt `sha256_pre`/`sha256_post` | 0 | 15/15 |
| C-23 | `git merge-base --is-ancestor eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 refs/remotes/origin/main` | 0 | ancestor (origin/main = b2aad08) |
| C-24 | `git show REV:<tool> \| grep -n <marker>` for the seven changed tools; `git show 9011581…:.ufo/waves/round-17/verify.py \| sed -n 59p` | 0 | markers at the cited lines; `source = git("rev-parse", "HEAD")` |
| C-25 | `wc -l README.md corpus/README.md`; `grep -n r18-swiss-map-replay README.md corpus/README.md` | 0 | 24 / 190; only `corpus/README.md:35` (F1) |

Self-corrections (my invocation errors, not lane defects):
- Running C-9 from the lane root first exited 1, because the SHA256SUMS paths are prefixed `predictions/`.
- C-12 with the glob `runs/*/receipt.json` first exited 2, because the glob also matched `run-log.txt`, giving 1 unreadable.

Both were rerun correctly, and only the clean results are cited.

## Observation vs inference

- **Observation:** every command result above and every cited path:line.
- **Inference (only one):** the freeze-before-run ordering is inferred by comparing the commit instant 13:23:55 with the first-carrier instant 13:24:07 (-03:00).
- **Recorded but not re-run:** the backward-compatibility proofs (16 logs byte-equal, 8 compares byte-identical, 8 receipts exit 0 without the flag) are cited from w1 seat reports at REV. The verification scripts they used live in `/tmp`, outside the lane and outside REV evidence.

## Limits

- Wrote only this report. No lane file was edited; no `jj` or git write was run; no REA, Ghidra or carrier binary was run; no subagent was dispatched.
- No tool installs or upgrades.
- The "Measured records" subsection that `SCORECARD.md:2434` promises is not yet present: the round-18 SCORECARD section ends at `:2440`, and `LOG.md:2167` says "Measured values follow in the next entry". That is the expected mid-round state, and this draft is the source material for that subsection.
- Carrier sha256 equality was checked between the recorded prediction and the receipt fields. The carrier binaries were not re-hashed.
- Push status (C-23) is read from the local remote-tracking ref only. No network read was made, and the push instant is not established.
