# CriticNoHarmPlan: in-place edits to the round-17 tools vs copies under round-18

Seat: author-side advisory critic, read-only. Baseline `B` = `9011581d` (`refs/heads/main` == HEAD, tracked tree clean at start).
Axes: calibration (are the no-harm claims true?), operability (is there one authority, can rechecks run?), depth (producer identity of evidence).
I installed nothing.

## Verdict

**Keep the edits in place.** Copies under `round-18/` would be worse. The plan still has four fixable defects: D1–D4 below. D1 and D2 are the most important.

- Editing in place does **not** damage reproducibility of r17 evidence when the reproduction names a revision. It also does **not** break `round-17/controls.py`, which only reports and is not a gate.
- What it does damage is anything that relies on **working-tree paths without a revision**: rechecks, line anchors and producer identity.
- r17 already shows this harm happening once, at d0ab299 (see O5).

## Observations (commands + exits)

**O1. r17 bytes stay recoverable and pinned by content.**
- `verification.json` `pins_pre.entries[*].sha256` equals sha256(`git show d0ab299:<p>`), which equals sha256(`git show refs/heads/main:<p>`), which equals the working-tree bytes.
- This holds for all 8 checked paths: `tools/{carrier-run,receipt-validate,log-extract,compare}.py`, `verify.py`, `controls.py`, `measure.py`, `run-carriers.sh`. Example: carrier-run is `953373e52ab9…` on all four sides.
- Commands: `git merge-base --is-ancestor d0ab299 refs/remotes/origin/main` → exit 0; same check for `da64646` → exit 0.

**O2. r17 controls only reports; it does not fail. In-place edits show up in the report rather than being hidden.**
- Setup: a mkdtemp clone at `B`. I appended one line to each of the 4 tools and `verify.py`, plus one line to `predictions/SHA256SUMS`, then committed.
- Command: `python3 -I -B <clone>/.ufo/waves/round-17/controls.py 9011581… HEAD` → exit 0.
- Result: `prior_wave_evidence_blobs` `checked: 15523, unchanged: 15517`. The changed list is exactly those 6 paths. `conformance_gate: false`.
- Control run with the same revision on both sides → exit 0, 15523/15523.
- The clone was removed (`rm -rf` exit 0).
- Code: scope at `round-17/controls.py:56,242-265`; no gate at `:370`; exit 0 whenever the report completes at `:34-36,505-514`. The selftest uses fixtures only (`:445-502`), so lane edits cannot turn it red.

**O3. The lane's established no-harm figure is "N/N frozen blobs byte-identical".**
- r17 reported `14943/14943` (`LOG.md:2112`; `final-recheck/controls-final.receipt.json.stdout` and `verify/controls.stdout` both show checked = unchanged = 14943).
- r16 reported `126/126` (`SCORECARD.md:2323`).
- So r18 is the first round to change prior-wave blobs on purpose.

**O4. The registry and the recheck point at working-tree W17 paths, with no revision.**
- `SKILL.md:537,538,540,541` (carrier-run / go-log-extract / go-route-compare / receipt-validate).
- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:3` gives the recheck as `round-17/tools/receipt-validate.py …/runs/<label>/receipt.json` (exit 0 expected), plus a `RUNS_DIR=/tmp` rerun that compares **fields**, not bytes.
- Current validator on the 8 r17 receipts: `python3 -I -B tools/receipt-validate.py runs/<label>/receipt.json` → exit 0 for all 8 labels. My loop also caught `runs/run-log.txt`; that is a glob artifact (exit 2) and not a receipt.

**O5. r17's own in-place edit already broke working-tree reproduction of retained outputs.**
Each tool version was run on every retained pair under `round-17/runs/`, comparing output against the retained file with `cmp`:

| Tool version | Retained file | Byte-identical |
|---|---|---|
| `compare.py` at d0ab299 (current) | `compare.json` | 8/8 |
| `compare.py` at 95e34db | `compare.json` | 8/8 |
| `log-extract.py` at d0ab299 (current) | `observation.json` | 5/8 |
| `log-extract.py` at 95e34db | `observation.json` | 8/8 |

- The 3 labels that differ are calib-esbuild-0.25.12, pro-esbuild-0.21.5 and pro-notesmd-cli.
- The difference is extra `FixGcWriteBarrierFlagBackgroundCommand` DEBUG events emitted by the d0ab299 parser. Example: `diff runs/calib-esbuild-0.25.12/observation.json -` → exit 1, hunk `142a143,149`.
- Timeline: the run started at 11:27:41-03:00 (`runs/run-log.txt:1`). 95e34db was committed at 11:27:35 and d0ab299 at 11:47:24.
- This is the producer-revision defect (R17-PRODUCER-REV, `corpus/lessons/round-17-verifier-spotcheck.md:139`), measured here.
- Note: an early pass of my loop reported compare 0/8. That was my own `runs/<l>//observation.json` double-slash path artifact; the corrected run is the 8/8 above.

**O6. The contract requires in-place edits.**
- `contract.md:32` (R17-PINMAP check (d)) requires the literal `map_sha256` in `round-17/tools/carrier-run.py`.
- `contract.md:134` has W18 `run-carriers.sh` take "tools from `W17/tools`".
- `contract.md:83-86` edits `round-17/verify.py`.

## Why copies under round-18 lose (inference from O4 and O6)

- **Two authorities.** Copies leave the registered gate (`SKILL.md:541`) and the knowledge recheck (`…diagnostics.md:3`) on unfixed W17 bytes while new behaviour lives in W18. That means two diverging `carrier-run.py` / `receipt-validate.py` files, and the mid-map fix would never reach the registered validator.
- **Contract churn.** R17-PINMAP check (d) (`contract.md:32`) could never close, so `open_count` would stay ≥ 1. The contract would need edits at `:32`, `:123-131` and `:134`, and SKILL registry edits, which are L1-only.
- **Copies protect nothing extra.** O1 shows Git already keeps the exact r17 bytes, pinned by sha256 in `verification.json`. O5 shows that a working-tree path never was a reproducibility guarantee: only `git show <producer-rev>:…` reproduces r17 outputs.

## Counterexamples and corrections

**D1 — Loss of controls coverage (calibration; most important).**
- The W18 controls spec (`contract.md:142-145`) and the Controls18 brief (`wave1-spec.json`, item Controls18) list LOG, knowledge, QUALITY, SOURCES, W17 predictions and SKILL. Neither keeps r17's generalized `prior_wave_evidence_blobs` check.
- Without it, the other 15517 prior-wave blobs go unchecked, in the same round that starts editing W17. That includes `round-17/runs/**` logs and receipts, `verify/**`, `verification.json`, `custody/**` and rounds 14–16.
- The Controls18 acceptance run uses the same revision on both sides (`B B`), so it cannot show this gap.
- **Smallest fix:** W18/controls.py keeps r17's `frozen_report` (`round-17/controls.py:242-265`) and adds an explicit allowlist of exactly the 6 paths from O2.
  - Allowlisted paths are reported as `changed_allowed`, with their B blob sha and owner.
  - Any other changed prior-wave blob counts as harm.
  - Selftest red case: one changed non-allowlisted file under `round-17/runs/`.
  - LOG and SCORECARD should then say "15517/15517 non-allowlisted frozen blobs byte-identical; 6 named in-place edits (B blobs recoverable)", not "N/N".

**D2 — r18 runs will not record which tool bytes produced them (depth/operability).**
- `contract.md:135-136` pins only the carrier, the prediction, swiss-misread, `selection.py` and Go data.
- `round-17/run-carriers.sh:14,26` pinned likewise; it ran `tools/log-extract.py` and `tools/compare.py` unpinned (`:33-34`).
- With five seats editing W17 tools in place during wave 1, r18 receipts would repeat R17-PRODUCER-REV (O5).
- **Smallest fix:** W18 `run-carriers.sh` adds `--pin` for `W17/tools/{carrier-run,pins,log-extract,compare,receipt-validate}.py`. The L1 commits the edits before the first carrier run, with the branch tip clean and the tip recorded as the producer revision.

**D3 — Line anchors drift (calibration).**
- The committed lesson cites `carrier-run.py:481-486` without a revision (`corpus/lessons/round-17-verifier-spotcheck.md:108,137`). The r18 drafts cite `carrier-run.py:479-487` (`w1/DraftPinmapCorrection.md:29,41`; `w1/DraftQualityRow21.md:17`).
- The pin_checks block sits exactly there today (`round-17/tools/carrier-run.py:475-487`, read above).
- The R17-PINMAP edit (writing `pins/mid-<n>.json` and `map_path`/`map_sha256`) goes inside that block. At the delivered revision those anchors would therefore point at different code.
- **Smallest fix:** every r18 text that cites W17 tool lines names the revision, e.g. `9011581:.ufo/waves/round-17/tools/carrier-run.py:481-486`, or cites lines after the edit lands. The frozen lesson cannot be edited; it is read as pre-r18.

**D4 — The fixed `round-17/verify.py` still writes to cited r17 evidence paths (operability; a tradeoff, not a blocker).**
- It writes `W17/verify/*` (`verify.py:24,73`), `W17/custody/custody-r17.v2.txt` (`:143-146`) and `W17/verification.json` (`:179-180`).
- The branch-tip gate makes a clean rerun succeed, and that rerun overwrites r17 evidence. Without D1, the r18 controls spec would not detect the overwrite.
- [INFERENCE] The hazard existed before r18; the fix makes a rerun look safe.
- **Smallest fix:** the required header comment (`contract.md:86`) also states "historical r17 pass; rerunning overwrites r17 evidence; run only in a clone". D1 then turns any overwrite red.

**D5 — The back-compat acceptance is weaker than it could be (calibration).**
- **compare.py:** the CompareEofFields brief (`wave1-spec.json`) accepts "exits unchanged". O5 shows the current compare reproduces 8/8 retained `compare.json` byte-identically, so require byte-identical stdout on all 8 retained pairs after the edit. That is stronger and achievable, provided new keys are emitted only when a prediction carries them.
- **log-extract.py:** compare old fields against the **pre-edit tool's output** (`git show 9011581:…/log-extract.py`), not against the retained `observation.json`. Otherwise 3/8 (O5) go red for reasons that predate r18.
- [INFERENCE] New keys emitted always will make full-output bytes differ for 8/8. The field-level "minus new keys" diff in the LogExtractEof brief is the right test.

## Axes impact

| Axis | Effect |
|---|---|
| Calibration | D1, D3, D5 |
| Operability | D2, D4 |
| Depth | D2 |

None of these needs moving the tools: all five fixes are additive to W18 and to r18 wording.
