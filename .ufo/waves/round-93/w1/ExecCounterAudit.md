# ExecCounterAudit — kaidoku round 93, wave r93-w1 (seat report)

Seat: executor. Item: reproduce every committed pre-freeze receipt and verify every
pin in `.ufo/waves/round-93/claims.json`, in a scratch clone at the freeze commit.
Environment: scratch clone `git clone --shared` of the lane at
`92a240521bd1bf2213b75d18d9b176a8dafdc67c`; `git rev-parse --show-toplevel` asserted
equal to the clone dir; `git status --porcelain` clean; run window 2026-11-05
11:00:21–11:00:35 (-03). Tooling authorization: no tools installed or upgraded
(no pacman, no uv, no cargo/npm) — host toolchain (python3, upx, jq, git) sufficed.

## 1. sha256 pins audit — all pins match

Source of pins: `.ufo/waves/round-93/claims.json`. Method: `sha256sum` inside the
scratch clone. Full detail in `ExecCounterAudit/pins-audit.json`.

| Artifact | Role | Pinned | Observed | Match |
|---|---|---|---|---|
| `tools/round-93/stop-boundary-repair-battery-v3.py` | C1 counter | `60026511e54c…bd4e3` | same | ✅ |
| `tools/round-93/craft-citation-semantic.py` | C2 counter | `34cf6579d7d0…05340` | same | ✅ |
| `tools/round-92/stop-boundary-repair-battery.py` | C1 import (r92 battery) | `63e9df431f5d…388bc` | same | ✅ |
| `tools/round-92/stop-boundary-battery-v2.py` | C1 import (v2 instrument) | `f6ddb48b4d9c…f1874` | same | ✅ |
| `tools/round-92/upx-stop-boundary-search-repair.py` | C1 positive-control repair | `ce1b1769d56c…a70c1` | same | ✅ |
| `manifests/block31-before.json` | C2 before manifest | `4792fca48e3e…082c` | same | ✅ |
| `manifests/block32-after.json` | C2 after manifest | `a28d841f0345…8bf90` | same | ✅ |
| `/usr/bin/env` (fresh-pack oracle source) | C1 oracle | `a9ba02dcad33…d202301` | same | ✅ |

Controls (no pin in claims.json; computed and recorded; cross-checked against the
`repair_sha256` field the committed receipts recorded pre-freeze — all three match):

| Control | Computed sha256 | Cross-check |
|---|---|---|
| `controls/table5-window.py` (F1) | `3271c1ca07cd…c65b` | == committed F1 receipt `repair_sha256` ✅ |
| `controls/carrierread5.py` (F2) | `cc6a07c74a7f…6e23` | == committed F2 receipt `repair_sha256` ✅ |
| `controls/identity_noop.py` (F3) | `518422b56015…19337` | == committed F3 receipt `repair_sha256` ✅ |

Receipt: `ExecCounterAudit/pins-audit.json` — `all_match: true`.

## 2. Before-receipt reproductions (R93-C1 before arms) — all four identical

Command shape (each arm sequential, shared scratch work dir, `TMPDIR` under scratch):

```
cd $S/clone && TMPDIR=$S/tmp python3 -I -B tools/round-92/stop-boundary-repair-battery.py \
  --root $S/clone --repair-cmd <arm repair> --work $S/work \
  --rev base-0a2a23da5eb50410a8a0df90c031d9f4fdadb024 \
  --expect 'repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10' \
  --json-out $S/out-<arm>.json
```

Comparison: `diff <(jq -S . committed) <(jq -S . reproduced)` — empty for all four
arms, i.e. byte-identical receipts in canonical form (not only label/met/exit: every
carrier sha, all 20 cells, counts, revision, tool fields).

| Arm | `--repair-cmd` | Committed (label / met / exit) | Reproduced (label / met / rc) | Verdict |
|---|---|---|---|---|
| F1_admitted | `controls/table5-window.py` | `repaired 10 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 10 of 10` / true / 0 | same label / true / 0 | identical ✅ |
| F2_admitted | `controls/carrierread5.py` | same expect label / true / 0 | same label / true / 0 | identical ✅ |
| F3_negative | `controls/identity_noop.py` | `repaired 0 of 10; wrong 0; unsafe 0; intact 5 of 5; far-refused 0 of 10` / false / 1 | same label / false / 1 | identical ✅ |
| positive | `tools/round-92/upx-stop-boundary-search-repair.py` | expect label / true / 0 | same label / true / 0 | identical ✅ |

Expected-vs-required: F1 met True ✅, F2 met True ✅, F3 met False ✅, positive met
True ✅ — the five-carrier forgeries ride the round-92 label at base exactly as
declared, and the honest repair stays admitted. Receipts:
`ExecCounterAudit/before-reproductions.json` plus the reproduced receipts
`reproduced-F1.json`, `reproduced-F2.json`, `reproduced-F3-negative.json`,
`reproduced-positive.json` (copies of the run outputs).

## 3. Checker (R93-C2) at base — selftest and before-manifest as declared

```
cd $S/clone && TMPDIR=$S/tmp python3 -I -B tools/round-93/craft-citation-semantic.py --selftest --work $S/work
```
→ 10 per-case `ok` lines, last line `SELFTEST cases=10 failures=0`, rc 0. ✅

```
cd $S/clone && TMPDIR=$S/tmp python3 -I -B tools/round-93/craft-citation-semantic.py \
  --root $S/clone --manifest .ufo/waves/round-93/manifests/block31-before.json \
  --block 31 --rev 0a2a23da5eb50410a8a0df90c031d9f4fdadb024 \
  --work $S/work --json-out $S/out-c2.json
```
→ rc 1, stdout exactly:
`row 'intact input refused by mistake': QUALITY 169 lacks ['never refuse an intact input', "packer's verdict"]`
— matches the claims atom verbatim. ✅ Reproduced receipt is byte-identical
(canonical diff empty) to the committed `.ufo/waves/round-93/pre/r93-c2-block31-before.json`.
Receipts: `ExecCounterAudit/checker-before.json`, `reproduced-c2-block31-before.json`.

## 4. Probe receipt check (unscored v3 F1 probe) — zero drift

Read-only assertions against `.ufo/waves/round-93/pre/probe-v3-F1-unscored.json`:

| Assert | Expected | Observed |
|---|---|---|
| label | `repaired 10 of 12; wrong 0; unsafe 0; intact 5 of 6; far-refused 12 of 12; fresh-roundtrip 0 of 2` | exact match ✅ |
| met_target | false | false ✅ (exit 1) |
| fresh near cells refused, rc 2 | both | delta −7 and delta +7, carrier `fresh-env`, `class: refused`, `rc: 2`, `typed_strict: true`, stdout `refused: "no pinned carrier matches within window"` (non-empty) ✅ |
| counter / import shas | `60026511…`, `63e9df43…`, `f6ddb48b…` | match ✅ |
| provenance atoms | marker present in mutated / absent in original, deterministic, no public collision | all present and true ✅ (source sha `a9ba02dc…d202301`, nonce `6c798579b314f8da`) |

Drift: none.

## Verdict

Every committed pre-freeze receipt reproduces byte-identically at the freeze commit
and every claims.json pin (counters, imports, repair candidate, manifests, oracle
source, controls) matches. No kill-rule input trips: shas pinned, receipts present,
F1/F2 admitted at base under the round-92 label, F3 negative and positive control as
declared. No drift found in the unscored probe.

## Notes / risks

- The battery arms completed in ~2–4 s each on this host (estimate in the item was
  ~2–4 min); receipts are complete and byte-identical to the committed ones, so the
  speed gap is a host property, not a reproduction defect.
- Nothing outside the seat directory and the (deleted) scratch was written; no lane
  file was modified; no git-mutating command ran in the lane; scratch dir
  `/fast/scratch/hyaku/kaidoku-r93/ExecCounterAudit` was removed after receipts were
  copied into the seat directory.
