PARTIAL

# SkillDeletedLines — SKILL.md deleted/replaced lines, B→REV (round 18, wave 2)

Seat `KaidokuR18.SkillDeletedLines` (reviewer). This is an author-side advisory, not an outside review.
- B = `9011581d84527ba34c675f9cf912e54d2e72d470`, REV = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`.
- Anchors are `git show REV:<path>` lines unless marked `B:`. For every cited lane file the worktree equals REV: `git diff --quiet REV -- .ufo/gates/citation-drift/ .ufo/waves/round-17/tools/ .ufo/waves/round-18/ SKILL.md corpus/` exited 0.
- Row-field authority: `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/PROTOCOL.md:414-416`. The fields are name, `gate|probe`, entry command, verdict map (code → class), self-test command and spelling, pinned-value path, write scope, and owner.
- Related PROTOCOL rules: gate/probe definition `:390-392`; drift pins `:383-386`.
- What I wrote:
  - In the lane: this file only.
  - Dynamic checks ran in a `mktemp -d /tmp/kr18w2-sdl.*` clone whose `origin` I removed first. I deleted it afterwards.
  - I ran no REA, Ghidra or `jj`, and executed no carrier.
  - I installed no tools.

## Verdict basis

- **Observation.** The diff is 53 insertions and 6 deletions.
  - All 6 deletions are same-line replacements, at 448, 528, 540, 541, 542 and 545.
  - All 47 new lines come after line 546.
  - No table, decision row or registry row was removed. Every external `SKILL.md:≤546` citation still lands on its row.
- Four replacements only add text or relabel: 448, 540, 542, and the 528 status upgrade.
  - The 528 upgrade holds against the retained evidence (H1).
  - The 448 and 542 relabels hold only partly: see L2 and L3.
- One replacement deletes a stated limit (M1). One narrows a design fact (L4).
- All 9 new rows fill the 5 merged columns. In 7 of them, the field values are incomplete or inaccurate: M2, L1, L5 and L6.
- Hence PARTIAL: no table or decision is lost, but some registry facts were weakened and some field values are incomplete.

| B→REV line | Row | Deleted text | Result |
|---|---|---|---|
| 448 | citation-drift | `probe` → `gate`; "13" → "15" cases; "the case table" → "the original case table" | Holds. The relabel is routed by `corpus/lessons/round-17-verifier-spotcheck.md:146`, and 15 cases were reproduced. See L2, L3, L7 |
| 528 | aether `Go analysis failure` | "INFERENCE, not replayed: Swiss maps … from `go1.25.0.json` (S032 lead)" | Holds (H1); one residual |
| 540 | go-route-compare | none (insertions only) | Holds. The 7 listed keys are exactly `compare.py:177-216` |
| 541 | receipt-validate | "Consistency of recorded digests, pins and log binding now; … and not during-run integrity" | **Weakened (M1)** |
| 542 | pins | `tool` → `probe`; "2 unreadable" extended | Text holds (`pins.py:117-122`, `:249-261`; "never continuity" kept); the kind rule fails (L3) |
| 545 | go-buildinfo-probe | "Stdlib reader modelled on go1.25.0 `debug/buildinfo`" | **Narrowed (L4)** |

## Findings (by severity)

### M1 (Medium, calibration) — receipt-validate lost its time-of-check and run-window limit, and its pins re-compare
- **Observation.**
  - B:541 says: "Consistency of recorded digests, pins and log binding now; not authenticity against a forger who rewrites and rehashes, and not during-run integrity".
  - REV:541 keeps only "Not authenticity against a forger who rewrites and rehashes". "now", "pins" and "not during-run integrity" are gone.
- **Observation.** The tool at REV still states both points:
  - Step 4, "Re-runs pins.compare on the recorded pins_pre/pins_post snapshots" (`.ufo/waves/round-17/tools/receipt-validate.py:23-25`).
  - "validation proves only that the recorded digests match the bytes present NOW. Bytes could have been modified and restored between the run and validation" (`:46-49`).
- **Inference.** REV:541 adds mid-map recomputation, the very capability a reader would take for run-window integrity.
  - The rule survives elsewhere: QUALITY #19 ("Continuity between recorded instants is never admitted", `corpus/QUALITY.md:29`) and REV:542 ("never continuity").
  - The validator's own row no longer carries it.
- **Repro:**
```
$ git show B:SKILL.md | sed -n 541p | grep -c 'not during-run integrity'                      → 1   EXIT=0
$ git show REV:SKILL.md | sed -n 541p | grep -c 'during-run integrity'                        → 0   EXIT=1
$ git show REV:SKILL.md | sed -n 541p | grep -c -E 'pins\.compare|pins_post|pins_compare'     → 0   EXIT=1
$ git show REV:.ufo/waves/round-17/tools/receipt-validate.py | sed -n '23,25p;46,49p'          → step 4 + Limitation text   EXIT=0
```
- **Fix.** Restore "recorded digests match the bytes present now; not run-window integrity (mid maps are identical bytes at retained instants only)" and name the pins_pre/pins_post re-compare.

### M2 (Low–Medium, operability) — the go-carrier-run-r18 row (REV:591) under-states the runner
- **Observation: verdict map.** "nonzero if any is nonzero" merges two classes:
  - exit 1: a run, compare or preflight failure;
  - exit 2: `carriers.tsv` has no trailing newline or no rows (`.ufo/waves/round-18/run-carriers.sh:11-13,187,191`).
- **Observation: write scope.** The row omits that each run deletes and recreates `runs/<LABEL>`: `rm -rf "$outabs"; mkdir -p "$outabs"` (`run-carriers.sh:216`).
  - The r17 sibling row keeps this warning; REV:591 does not.
- **Observation: pinned-value path.** The sums file read at run time sits outside the repo: `SUMS="${SUMS:-/home/vgpnk/.local/share/kaidoku-r18/carriers/SHA256SUMS}"` (`:28`).
  - It is currently byte-identical to the in-repo `.ufo/waves/round-18/carriers/SHA256SUMS`.
  - The row says only "synthetic `SHA256SUMS`" (see PROTOCOL.md:383-386: pins persisted inside the repo).
- **Inference.** Running the registered entry for one label deletes that label's committed run evidence from the worktree. Git can recover it, but the next `jj` command in this colocated lane would snapshot the deletion.
- **Repro:**
```
$ git show REV:SKILL.md | sed -n 537p | grep -c 'the default `runs/<LABEL>` is replaced'      → 1   EXIT=0
$ git show REV:SKILL.md | sed -n 591p | grep -c 'replaced'                                     → 0   EXIT=1
$ git show REV:.ufo/waves/round-18/run-carriers.sh | grep -n -E '^SUMS=|^  rm -rf "\$outabs"|exit 2$'   → :28, :187, :191, :216   EXIT=0
$ cmp /home/vgpnk/.local/share/kaidoku-r18/carriers/SHA256SUMS .ufo/waves/round-18/carriers/SHA256SUMS   EXIT=0
```

### L1 (Low) — r18-prediction-freeze (REV:565): the failure path writes files, despite "(nothing frozen)"
- **Observation: write order.** `gen-predictions.py` writes per label as it goes:
  - `swiss-misread/<label>.json` at `:49-50`, before the `unknown` check at `:52-53`;
  - `<label>.prediction.json` at `:71-72`.
  - `decision-rule.json` and `SHA256SUMS` are written only after the loop (`:91-97`).
  - So an abort leaves new per-label files that the old manifest does not cover.
- **Observation: exit code.** "nonzero" is observed as exit 1.
- **Observation: no recheck form.** The registered entry has no output-directory option (`PRED` is hard-coded at `:22`), so any recheck rewrites the lane's frozen predictions in place.
  - For one carrier the rewritten bytes were identical to the frozen ones.
  - Byte-identity for the other 14 is **INFERENCE**.
- **Self-test.** "no selftest" is stated honestly. PROTOCOL.md:398 binds self-tests to gates, and `gen-predictions.py` is not in the contract's tool list (`contract.md:8-146`).
- **Repro.** In the temp clone: `T=$(mktemp -d /tmp/kr18w2-sdl.XXXXXX); git clone -q --no-local LANE $T/c` (EXIT=0); `git -C $T/c remote remove origin` (EXIT=0); `git -C $T/c checkout -q --detach REV` (EXIT=0). Then:
```
$ printf 'sdl-probe\t/home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-noswiss-nomethods\tsynthetic-minimal-pair\nsdl-bogus\t/nonexistent/sdl-bogus\tsynthetic-minimal-pair\n' > $P/carriers.tsv
$ python3 -I -B $T/c/.ufo/waves/round-18/gen-predictions.py      EXIT=1  stderr: failed (2): … buildinfo-probe.py /nonexistent/sdl-bogus
$ git -C $T/c status --porcelain --untracked-files=all -- .ufo/waves/round-18/predictions   EXIT=0
   M carriers.tsv | ?? sdl-probe.prediction.json | ?? swiss-misread/sdl-probe.json
$ sha256sum -c pre.sums   (SHA256SUMS, decision-rule.json)        both OK  EXIT=0
$ grep -c sdl-probe $P/SHA256SUMS                                 → 0  EXIT=1
$ cmp $P/sdl-probe.prediction.json $P/s1246-noswiss-nomethods.prediction.json   EXIT=0
```

### L2 (Low) — the citation-drift row (REV:448) gives the wrong finding ID, and its pin cell is incomplete
- **Observation: finding ID.** REV:448 says "a literal `--rev HEAD` is accepted only when HEAD equals that tip, else exit 2 `head_not_branch_tip` (`branch_missing` when the branch is absent)".
  - With the branch absent, `--rev HEAD` emits `head_not_branch_tip` (`citation-drift-probe.py:329-336`).
  - `branch_missing` comes only from an omitted `--rev` (`:321-326`).
- **Observation: pin cell.** The 5th cell still says `expected.json` pins "the self-test case table", but it holds 13 of the 15 cases.
  - The two round-18 cases are literals in the script (`:502-503`).
  - This is allowed by PROTOCOL.md:398-400, which only requires committed values. The cell is incomplete, not wrong.
- **Repro** (temp clone, after `git -C $C branch -D main`, EXIT=0):
```
$ python3 -I -B $G/citation-drift-probe.py --root $C --rev HEAD --table $G/pointer-table.json --expected $G/expected.json --strict
   EXIT=2  CITATION_DRIFT: head_not_branch_tip entry=main HEAD b2aad08… != refs/heads/main (missing)
$ python3 -I -B $G/citation-drift-probe.py --root $C --table $G/pointer-table.json --expected $G/expected.json --strict
   EXIT=2  CITATION_DRIFT: branch_missing entry=main refs/heads/main does not resolve to a commit
$ python3 -I -B $C/.ufo/gates/citation-drift/citation-drift-probe.py --selftest    EXIT=0  CLEAN cases=15 passed=15
$ git show REV:.ufo/gates/citation-drift/expected.json | python3 -I -B -c '…len(selftest)'   → 13  EXIT=0
```

### L3 (Low, calibration) — the kind column follows no single rule at REV
- **Observation.**
  - REV:448 relabels citation-drift `gate` because "the registered argv carries `--strict` and can exit 1".
  - REV:542 relabels pins `probe`, although its registered `compare` exits 1 on "differ". Its stated reason, "PROTOCOL row kinds are gate or probe", argues against `tool`; it says nothing for `probe` over `gate`.
  - REV:540 keeps go-route-compare `probe`. It exits 1 on mismatch against frozen predictions persisted in the repo, which its new pinned-values cell names. That is a gate under PROTOCOL.md:390-392.
  - REV:449 custody-pair stays `tool / kaidoku`, contrary to REV:542's own rule.
- **Repro:** `git show REV:SKILL.md | sed -n 449p | cut -d'|' -f2,3` → ` custody-pair | tool / kaidoku ` (EXIT=0). Compare the verdict maps at REV:540 ("1 any mismatch") and REV:542 ("1 differ").

### L4 (Low) — go-buildinfo-probe (REV:545): the design fact was narrowed to "constants"
- **Observation.** B:545 has "Stdlib reader modelled on go1.25.0 `debug/buildinfo`". REV:545 has "Pinned values: the build-info magic and header constants of go1.25.0 `debug/buildinfo` (keeps the writable-segment fallback …)".
  - The stdlib-only fact and the algorithm-model fact are gone.
  - The parenthetical now attaches to "constants".
- **Observation.** The tool's actual pinned basis is not named: go1.25.0 `buildinfo.go`, sha256 `332fff28…` (`buildinfo-probe.py:2-5,15-18`).
- **Repro:**
```
$ git show B:SKILL.md | sed -n 545p | grep -c 'Stdlib reader modelled on go1.25.0'   → 1  EXIT=0
$ git show REV:SKILL.md | sed -n 545p | grep -c -E 'reader|modelled|[Ss]tdlib'      → 0  EXIT=1
```

### L5 (Low) — routed-defects (REV:586): "Git objects at REV only" is inaccurate
- **Observation.** The tool also reads blobs at `2711674` and `da64646` (`routed-defects.py:566,581,592`), plus ancestry. Its own pinned-values cell names those revisions. `contract.md:26` repeats the same wording.
- **Repro:** `git show REV:.ufo/waves/round-18/tools/routed-defects.py | grep -n -E '_show\(root, (HIST_SUMS_REV|RUNLOG_REV)'` → 566, 581, 592 (EXIT=0).

### L6 (Low, field completeness) — new rows omit the self-test write scope
- **Observation.** Five new rows say nothing about where their self-test writes:

  | Row | REV line | Where the self-test writes |
  |---|---|---|
  | head-rev-lint | 587 | `head-rev-lint.py:803,888` |
  | revpin | 588 | `revpin.py:161,281` |
  | swiss-misread | 590 | `swiss-misread.py:1748,1809` |
  | go-carrier-run-r18 | 591 | `run-carriers.sh:34,36` (`mktemp -d /tmp/…` plus `trap rm`) |
  | round18-structural-controls | 593 | `controls.py:620,786` |

- The same commit adds "`--selftest` writes only a removed mkdtemp tree" to REV:540, 541, 542 and 545, and REV:586 and the exemplar row REV:447 state it too.
- head-rev-lint's pinned scope has two further gaps:
  - It omits the file-type filter (tracked `*.py`/`*.sh` only, `head-rev-lint.py:7-8`).
  - It writes `w[0-9]/` where the code matches `^w[0-9]+$` (`:83`).
- All of these temp trees are removed. The behaviour is benign; the field is incomplete.

### L7 (Low) — stale intro prose
- **Observation.** REV:440 still reads "citation-drift probe, custody-pair tool", against REV:448 `gate`.
- **Repro:** `git show REV:SKILL.md | sed -n 440p` (EXIT=0).

## Holds (observations)

### H1 — REV:528 upgrade (INFERENCE → replayed and confirmed on held-out carriers)
Every limb of the frozen rule (`predictions/decision-rule.json`) holds:
- **Predictions unchanged since the freeze.** `git diff --stat eb6c266 REV -- .ufo/waves/round-18/predictions/ | wc -l` → 0 (EXIT=0). The freeze commit `eb6c266` is dated 13:23:55-03:00, and the first run started 13:24:07-03:00 (`runs/run-log.txt`).
- **Receipts valid.** `find .ufo/waves/round-18/runs -mindepth 2 -maxdepth 2 -name receipt.json -print0 | sort -z | xargs -0 python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps` → `valid 15, invalid 0, unreadable 0`, EXIT=0.
- **Per-label checks.** A read-only script over `receipt.json`, `*.prediction.json`, `observation.json` and `compare.json` (EXIT=0) shows:
  - carrier sha256 binding 15/15;
  - `all_match` 15/15;
  - `Go analysis failure` only on the 3 diagnostic-set labels;
  - s1246-swiss-nethttp `invalid_index_reads` `[22386945]` and real-kimi-webbridge `[15606016]`, both equal to the frozen values;
  - calib-aether `eof_reads` `[[17645861, 111938854]]`;
  - no failure on the noswiss sibling or on any of the 11 non-diagnostic synthetic labels.
- **"Not the patch fallback" holds.** s1246-swiss-nethttp failed on the exact INFO route, with no fallback.
- **"(S033 supersedes the S032 lead)" holds.** `git show REV:corpus/SOURCES.md | grep -c 'supersedes S032'` → 1 (EXIT=0).
- **`go1.25.0.json` → "the snapshot" is supported by the lane's frozen emulator outputs.** The 1.24 carriers bind through `go1.24.0.json` → `internal/abi.OldMapType`, 88 B (`predictions/swiss-misread/{s1246-swiss-nethttp,real-kimi-webbridge}.json`).
- **Residual.** No SOURCES row anchors `go1.24.0.json`.
  - `git show REV:corpus/SOURCES.md | grep -c 'go1\.24\.0\.json'` → 0 (EXIT=1).
  - S023 anchors only `go1.25.0.json` `all.Types.runtime.moduledata.Fields[1]` (`SOURCES.md:29`), yet REV:550 cites S023 for the 1.24/1.25 binding.

### Field matrix — new rows vs PROTOCOL row fields
The 9 new rows (REV:565 and REV:586-593) all carry name, a `gate|probe` kind, `/ kaidoku` owner, an absolute entry command, and pinned-value and write-scope text. All gates (586, 587, 589) have `--selftest` and a 0/1/2 map. Only 589 (jj-red-before) and 592 (round18-measure) have no gaps. The gaps:
- 565: verdict map says only "nonzero", and there is no self-test (stated) — L1.
- 586: write scope is inaccurate — L5.
- 587, 588, 590, 593: self-test write scope missing — L6.
- 591: map, write scope and pinned path — M2, plus L6.

The R17-REGISTRY rows REV:540, 541, 542 and 545 now carry both `Pinned values:` and `Write scope:` (`corpus/lessons/round-18.md:55` holds). M1 and L4 concern the content those edits removed.

## Residual risk and verification gaps
- **Not run by me:** REA/Ghidra, carrier reruns, and the self-tests of head-rev-lint, routed-defects, revpin, swiss-misread and jj-red-before (other seats own those). The H1 verdict rests on retained logs plus the frozen rule, which I applied by hand.
- **L3 is a classification judgment** under PROTOCOL.md:390-392, not a runtime defect.
- **Distillation gap, not a deletion.** The new SKILL Swiss table (REV:557-561) carries 3 of the knowledge entry's 4 decision rows. It omits the following from `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md`:
  - "Do not generalize '1.25.0 is safe'" (`:97`);
  - the dual-path INFERENCE about aether's stack (`:101`).
- **Harness artifact.** My first validator run used a shell glob and exited 2. The session shell had expanded `runs/*/receipt.json` to the nonexistent `runs/run-log.txt/receipt.json`. I filed this to `xd://report_issue`; with an explicit `find` list the run exits 0. It is not a lane defect.
- **Lane status:** `git status --porcelain --untracked-files=all` showed only untracked w2 seat reports and `gen-wave2.py`, and no tracked modification.
