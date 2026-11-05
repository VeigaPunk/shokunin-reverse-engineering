# ExecPremise — R93-C1 fresh-pack premise probes (exploratory, unscored)

Seat: ExecPremise (executor), lane kaidoku, round 93, attempt 1. Freeze commit
`92a240521bd1bf2213b75d18d9b176a8dafdc67c`. Scratch clone verified
(`git -C <clone> rev-parse --show-toplevel` = clone dir; HEAD = freeze commit).
Counter and repair pins re-checked by `sha256sum` against `claims.json`:
v3 `60026511…4cd3`, round-92 repair `ce1b1769…2301`, round-92 battery `63e9df43…`,
v2 `f6ddb48b…`, `/usr/bin/upx` `cf2f6e7c…` (upx 5.2.0), `/usr/bin/jq` `e8155…`
(`e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`), `/usr/bin/env` `a9ba02dc…`.
All probes are exploratory; none is a frozen counter and none edits a counter, label or manifest.
Python 3.14.8. Driver: `probe-driver.py` (copied to seat dir). Invocation for each:
`TMPDIR=$S/tmp python3 -I -B $S/probe.py {fresh|public|forgery|strict}` (`S=/fast/scratch/hyaku/kaidoku-r93/ExecPremise`).

## Probe results

| # | Probe (command arg) | Exit | Result | Receipt |
|---|---|---|---|---|
| 1 | `fresh` — `v3.fresh_arm(REPAIR, env, work, rep, r88, {"sentinel-deadbeef"}, clone)` | 0 | PASS, all 11 checks true | `fresh-arm-premise.json` |
| 2 | `public` — `v2.pack` on `/usr/bin/jq` twice | 0 | PASS: byte-equal (14036 bytes, sha256 `e8b6c9e7…5268`) | `public-determinism.json` |
| 3 | `forgery` — F1 and F2 invoked directly on fresh cells | 0 | PASS (assertion: no forger emits output on any fresh tampered cell) | `f1-fresh-direct.json`, `f2-fresh-direct.json` |
| 4 | `strict` — `v3.strict_typed` on round-91 refusals and synthetics | 0 | PASS: refusal True; 7 of 7 synthetic cases as expected | `strict-typed.json` |

Logs: `probe-logs/log-{fresh,public,forgery,strict}.txt` (each ends `exit=0`).

### 1. Fresh-arm premise (`fresh-arm-premise.json`)
Nonce `99361468162c63d3`; `/usr/bin/env` marker at offset 97640 in mutated bytes.
- deterministic pack: true (two fresh packs byte-equal); marker in mutated: true; marker absent in original: true;
  no collision with `{"sentinel-deadbeef"}`: true; walkable chain: 5 blocks; unevaluable: none.
- near ±7 (last block sz_cpr 575 → 568 / 582): both `repaired`, rc 0, `roundtrip` true.
- far ±40 (→ 535 / 615): both `refused`, rc 2, `typed_strict` true.
- intact fresh packed image: rc 0, identity true.

### 2. Public determinism (`public-determinism.json`)
`/usr/bin/jq` packed twice via `v2.pack`: byte-equal, 14036 bytes. Informational: the other four public carriers
also byte-equal and their raw sha256 pins match. `/usr/bin/upx` sha matches `UPX_SHA256`.

### 3. Forgeries direct, no battery (`f1-fresh-direct.json`, `f2-fresh-direct.json`)
Fresh cell built from `/usr/bin/env` with fixed nonce `0123456789abcdef`, last block (block 29841, sz_cpr 575, sz_unc 2392) tampered ±7 / ±40, plus intact.
Each forger run as `python3 -I -B <forger> --in <cell> --out <scratch>/out/<name>.bin`.

| Forger | ±7 near (−/+) | ±40 far (−/+) | intact |
|---|---|---|---|
| F1 `table5-window.py` | rc 2, no output, typed refusal | rc 2, no output | rc 2, no output (typed refusal) |
| F2 `carrierread5.py` | rc 2, no output, typed refusal `stop-boundary: no green value in the +/-16 window` | rc 2, no output, same typed class | rc 0, output byte-equal to packed input (identity pass-through) |

Observations (no action taken):
- F1 refuses the intact fresh image with rc 2. Its pinned table only matches the five public images, so an intact fresh input gets a typed refusal instead of identity. That is an intact-input refusal, relevant to the R93-C2 rule.
- F2 returns identity on the intact fresh image (rc 0, output == input), not a repair. It never repairs any tampered fresh cell.
- F2 hard-codes `ROOT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin` and imports the lane's `tools/round-92/upx-stop-boundary-search-repair.py`. The lane file's sha256 is recorded in the receipt (`lane_repair_sha256_F2_imports`). `git diff` against the freeze commit for `tools/round-91..93` in the lane was empty, so the lane copy equals the clone copy.

### 4. Strict typed parsing (`strict-typed.json`)
`tools/round-91/upx-stop-boundary-repair.py` (clone copy) on fresh cells:
- ±40: rc 2, no output, last stdout line is a JSON object with `refused` = `stop-boundary: the walk's last storable ...`, `strict_typed` True.
- ±7: rc 2, no output, `strict_typed` True. (The round-91 tool refuses the near cells too; round-92 is the one that repairs them.)

Synthetic `strict_typed` inputs (rc, stdout → got / expected):
- `{"refused": null}`, rc 2 → False / False ✔
- `{"refused": ""}`, rc 2 → False / False ✔
- `{"refused": 7}`, rc 2 → False / False ✔
- `{"refused": "stop-boundary: x"}`, rc 2 → True / True ✔
- `{"refused": "x"}`, rc 1 → False / False ✔
- `{"error": "x"}`, rc 2 → False / False ✔
- non-JSON last line, rc 2 → False / False ✔

## Checks not run
None of the frozen counters were run and no frozen target was evaluated. The seat's assignment is premise only; R93-C2 (craft citation) was not in this seat's item.

## Host and tooling
- No tool installed or upgraded. No host state changed (no sysctl, no pacman, no namespace change).
- Lane: no file written, edited or staged. Seat directory writes only. `git status` in the lane lists untracked files from other seats and the L1 (`.ufo/waves/round-93/l1/`, `r93-w1-dispatch.json`, `r93-w1.ready*`, `w1-run.out`); none are mine.
- Scratch `/fast/scratch/hyaku/kaidoku-r93/ExecPremise` removed after copying receipts.

## Files written
- `.ufo/waves/round-93/w1/ExecPremise.md` (this report)
- `.ufo/waves/round-93/w1/ExecPremise/ExecPremise.md` (copy)
- `.ufo/waves/round-93/w1/ExecPremise/{fresh-arm-premise,public-determinism,f1-fresh-direct,f2-fresh-direct,strict-typed}.json`
- `.ufo/waves/round-93/w1/ExecPremise/probe-driver.py`
- `.ufo/waves/round-93/w1/ExecPremise/probe-logs/log-{fresh,public,forgery,strict}.txt`
