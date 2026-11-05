# CriticC1 — falsification of R94-C1 (calibration)

Seat: CriticC1 (critic, leaf). Lane: kaidoku, round 94, attempt 1. Scratch clone at declaration commit
`dd4524916a0332bb65f83525532da1c1b8d709de`; base clone at `8a40ceb6516bb38c19c37bcbff2bb3332f31c832`.
Lane was read-only: no lane file edited, no mutating git. Scratch removed after copying receipts.

## Summary

| # | Attack | Status |
|---|--------|--------|
| 1 | Do-nothing control honest (base v3 receipts, commands, rc, stderr) | HELD |
| 2 | Receipt agrees with stdout while misstating the frozen verdict | BROKEN |
| 3 | Fabricated stdout+receipt pair passes without running the public battery | BROKEN |
| 4 | Cheaper control reaches 4 of 4 | BROKEN as a measure of the claimed design (crash fix only); do-nothing HELD (2 of 4) |

The frozen target as written is satisfiable by a receipt triple that does not state the verdict the frozen predicate requires,
and by a fabricated triple with no repair run. The honest L1 result (4 of 4) is reproducible, but the counter cannot
distinguish it from a forgery. Counter sha256 pins are unchanged, so any repair of the counter needs a new declaration.

## Attack 1 — do-nothing control: HELD

Checks:
- `claims.json` `before`: revision `8a40ceb6…`, counter `tools/round-93/stop-boundary-repair-battery-v3.py`
  (sha `60026511…d4e3`). `git diff --stat 8a40ceb6 dd452491 -- tools/ plans/ corpus/ SKILL.md` shows only
  `tools/round-94/` (v4 + agreement) and `plans/round-94-claims.md` added. v3 is byte-identical at base and declaration.
- Committed pre receipts vs claim wording:
  - `pre/c1-base-v3-pos.stderr`: `TypeError: Object of type bytes is not JSON serializable` at `json.dump` (matches claim).
  - `pre/c1-base-v3-pos.rc` = 1; `pre/c1-base-v3-pos.stdout` empty; `pre/c1-base-v3-pos.json` truncated at byte 706 (`"output": `).
  - `pre/c1-base-v3-F3.*`: same crash, truncated receipt at byte 703. Claim wording matches.
  - `pre/c1-base-v3-F1.json` / `F2.json`: valid JSON, `label` `repaired 10 of 12; ... intact 5 of 6 / 6 of 6; fresh-roundtrip 0 of 2`, `met_target` false, `exit` 1. Matches claim `before.expected`.
  - `pre/c1-base-v3-agreement.json`: `counts_of_4` valid 2, agree 2, predicted 2, `met` false. Matches claim.
  - `pre/c1-base-revision.txt` = `base 8a40ceb6…`. Receipt `revision` field is `8a40ceb65` (short).
- Reproduction at base (`$S/clone-base`, v3 sha `60026511…`), command:
  `python3 -I -B tools/round-93/stop-boundary-repair-battery-v3.py --root <base> --repair-cmd <cmd> --work <w> --rev 8a40ceb6… --expect '<frozen label>' --json-out <j>`
  Results: pos rc 1 (TypeError), F1 rc 1 (10/12, valid), F2 rc 1 (10/12, valid), F3 rc 1 (TypeError). Agreement counter on these: valid 2, agree 2, predicted 2, exit 1. Same as committed pre.
- Caveats (do not break the claim, recorded for the L1):
  - `--rev` is an operator-supplied string, not checked against `git rev-parse HEAD`. The before receipts say `8a40ceb65` because the operator passed it; nothing in v3 measures the revision.
  - The before-run `--root` was the lane base tree; the after-run `--root` was the declaration clone. Repair tools and controls are byte-identical across both (`tools/round-92/upx-stop-boundary-search-repair.py` unchanged; `.ufo/waves/round-93/controls/*` tracked, same bytes).
  - F1, F2 in the claim are described as "the two forgery receipts that do write", which holds. F3 is truncated, matching `before.receipt` wording.

## Attack 2 — receipt agrees with stdout while misstating the verdict: BROKEN

Fixture: `$S/fixtures` copy of `.ufo/waves/round-94/l1/scores/c1-v4-*` (pos, F1, F2, F3 × json/stdout/stderr/rc). Each case run as
`python3 -I -B tools/round-94/c1-receipt-agreement.py --dir <case> --prefix c1-v4`. Full generator: `fixtures/alter.py`; case list: `fixtures/cases.txt`.

| case | alteration | exit | counts (valid/agree/predicted) |
|------|------------|------|--------------------------------|
| 00 | none (control) | 0 | 4/4/4 |
| A | F1 receipt `label` set to frozen label; stdout unchanged | 1 | 4/3/4 |
| B | F1 stdout label set to frozen label; receipt unchanged | 1 | 4/3/4 |
| C | F1 receipt `met_target` True; stdout unchanged | 1 | 4/3/3 |
| D | F1 receipt and stdout `met True` (exit 1 kept) | 1 | 4/4/3 |
| E | F1 receipt `exit` 0, stdout `exit 0`, rc 0 | 1 | 4/4/3 |
| F | F1 rc file 0 only | 1 | 4/3/4 |
| G | F3 receipt truncated to 700 bytes | 1 | 3/3/3 |
| **H** | **F1 receipt `label` = frozen label AND stdout `repaired 12 of 12 … met False exit 1`** | **0** | **4/4/4** |
| **J** | **pos receipt label `repaired 0 of 12 …` AND stdout `repaired 0 of 12 … met True exit 0`** | **0** | **4/4/4** |
| **K** | **F1 receipt `expect` = "anything"** | **0** | **4/4/4** |

Reading: the counter enforces that receipt and stdout agree, that met/exit match the predicted control values, and that rc matches exit.
It never checks that `label` equals the frozen label when `met_target` is true, that `label` is consistent with `counts`,
or that `expect` equals the frozen label. So a receipt can state `repaired 12 of 12 … 2 of 2` and `met False` for a control that scored 10 of 12,
or `met True` beside a label saying `0 of 12`, and pass. H is the sharpest case: the label the frozen predicate names is misstated and the counter reports 4 of 4.

Catch that exists (not in the agreement counter): recompute the label from the receipt's `counts` and require `met_target == (label == expect and counts thresholds)`.
That check lives in v3's `score()`, not in the agreement counter, so it only holds if the receipt was produced by v3/v4 and not edited afterwards.

## Attack 3 — fabricated stdout+receipt pair passes without running the battery: BROKEN

Fixture `FAB_pos_fabricated`: pos receipt replaced by `{"label": "<frozen label>", "met_target": true, "exit": 0}`, stdout `<frozen label> met True exit 0`, rc `0`. F1–F3 real.
Agreement counter: `counts_of_4 {valid 4, agree 4, predicted 4}`, `met` true, exit 0.

Why: the counter reads only the receipt JSON (valid dict, `label`, `met_target`, `exit`), the last stdout line, and the rc file. It does not read
`repair_sha256`, `counter_sha256`, `verdict_sha256`, `imported_*_sha256`, `revision`, `public_*`, or `fresh_provenance`. A forger who
writes `met True exit 0` for pos and copies F1–F3 from a real run passes. The forgery needs only the three values the honest control has to produce anyway.

What in the pinned chain would catch it, and what does not:
- Re-running the frozen command (`v4 --json-out` on the same repair) produces the same public cells and label, and a fresh nonce. A verifier comparing a receipt to a re-run catches the fabrication. Nothing in the frozen counter does this.
- Pinned repair sha: the receipt records `repair_sha256` for pos `ce1b1769…70c1`, matching `tools/round-92/upx-stop-boundary-search-repair.py` bytes (verified). The fabricated pos receipt has no such field, but the agreement counter does not require one.
- Pinned upx sha `cf2f6e7c…c969`: checked only inside a live `v2.invoke`/`v2.pack` (`stop-boundary-battery-v2.py` line 209, `packer sha256 drift` → exit 2). **No receipt records the upx sha** (grep: no `upx` field in any L1 receipt; the only `upx` hits are the `upx-stop-boundary-search-repair.py` path string). The kill rule "wrong upx sha" is therefore not checkable from receipts; it holds only if the live run executed.
- Pinned v3/round-92 sha: recorded as `verdict_sha256`, `imported_r92_battery_sha256`, `imported_v2_sha256` in the receipt. Self-reported; the counter does not compare them.

Verdict: a fabricated pos triple satisfies the frozen command. The honest L1 run is valid evidence only because the L1 ran the public battery. The frozen counter cannot tell.

## Attack 4 — cheaper control reaching 4 of 4: BROKEN as a measure of the design; do-nothing HELD

- Do-nothing (v3 unchanged): 2 of 4 valid, agree 2, predicted 2 — target not reached. HELD.
- Cheapest real control: v3 with one-line change `json.dump(receipt, fh, indent=1, sort_keys=True)` → `…, default=str)` in a scratch copy (`clone-cheap`, not the lane). Ran the four public runs (`work/cheap/c1-cheap-*`):
  - pos rc 0, `repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0`
  - F1 rc 1 (10/12), F2 rc 1 (10/12), F3 rc 1 (0/12)
  - Agreement counter: `counts_of_4 {valid 4, agree 4, predicted 4}`, exit 0.

So the target is reached by a one-line writer patch that does **not** implement the claimed design: bytes become `str(b'…')` instead of `{"bytes": n, "sha256": hex}`, and there is no `<json-out>.tmp` write-then-rename (D-93-D atomicity). The counter cannot see either, because it reads only label/met/exit. The claimed work's crash is fixed by both; the claimed structure is not verified. The v4 writer is correct against its own design (the `write_receipt` atomic path and `_default` are present, verified: `fresh_cells[*].output` is `{'bytes','sha256'}`, no `.tmp` left in `work/after`), but nothing in the frozen target tests that.

## Pins and reproduction (all HELD)

- sha256 at dd452491 (clone bytes): v4 `c41d54d7…7272`; agreement `dc384a44…36c9`; v3 `60026511…d4e3`; round-92 battery `63e9df43…38bc`; round-92 v2 `f6ddb48b…4f1874`. All match claim pins. Independently confirmed; ReviewerV4 reported the same.
- host `/usr/bin/upx` sha `cf2f6e7c6846a7c9…c969` matches the kill-rule prefix and `UPX_SHA256` in v2.
- fresh source `/usr/bin/env` sha `a9ba02dc…2301` matches the pin.
- After-run (v4, dd452491, `--root` clone): `c1-v4-pos` rc 0 `met True exit 0`; F1 rc 1 (10/12); F2 rc 1 (10/12); F3 rc 1 (0/12). Agreement counter: 4/4/4, exit 0. Matches L1 `scores/`.

## Not tested

- Multi-line stdout where an earlier line contradicts the last line: the counter reads `splitlines()[-1]` only. Not run (reason: out of the listed attacks; the counter's last-line rule is visible in source).
- Honest-run receipt field `counter_sha256` vs live file sha: not compared by any counter; not separately tested beyond the pin list above.

## Smallest safe correction (for L1, not applied)

The claim's `frozen_command` plus its agreement counter (sha `dc384a44…`) cannot be changed in this round: counter, label and predicate are frozen. Options for L1:
1. Record as a named limit in the landing report: the agreement counter reads receipt label/met/exit only; attacks 2 (H, J, K) and 3 (fabricated triple) pass it.
2. Re-check at landing with a separate step (not a counter edit): re-run each public `v4 --json-out` command and compare the public fields and `label` to the receipt; recompute `label` from `counts`; check `repair_sha256`, `verdict_sha256`, `counter_sha256` against pins.
3. A future round's counter (new declaration) should require `label == expect` when `met_target` is true, and require `revision` to equal `git rev-parse` of the measured tree.

## Receipts written to this seat

- `repro-base-v3/c1-base-v3-*.{json,stdout,stderr,rc}`: do-nothing reproduction at 8a40ceb6.
- `repro-after-v4/c1-v4-*.{json,stdout,stderr,rc}`: v4 reproduction at dd452491.
- `repro-cheap-writer-only/c1-cheap-*.{json,stdout,stderr,rc}`: one-line `default=str` writer-only control.
- `fixtures/alter.py`, `fixtures/cases.txt`: alteration generator and case list (paths inside it point at deleted scratch; re-run `alter.py <l1 scores dir> <fixture dir>` to rebuild).

No install, no sysctl, no pacman, no host state change.
