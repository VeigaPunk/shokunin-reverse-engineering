PARTIAL — both production variadic-mask removals survive `--selftest`; the combined probes reject all three mutants, but null inversion is killed by a crash rather than a semantic comparison.

# MutateEmulatorV2 — author-side C3 falsification probe

Written: 2026-10-21T04:15:11-03:00. Seat: `KaidokuR20Recovery.MutateEmulatorV2-3`.

Axes: **calibration** (baseline-aware verdicts and exact restoration), **coverage** (both variadic call sites, failure nullability, uncommon offset), **depth** (fresh predictions from all eight round-19 carriers against the retained bound logs).

Scope: C3 at `S:.ufo/waves/round-20/claims.json:33-39`, contract `:76-81`, and `S:corpus/lessons/round-20.md:36-37` (retro is consistency, not prospective evidence). B=`14f0260ad319ecc26994381b2415d5a999003375`; F=`808cbb31a1e24656da5ba4967497e602fbca7415`; measured S=`5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`. This probes detector sensitivity, not freeze ordering or the held-out runs.

## Isolation and command binding — observations

- `tempfile.mkdtemp(prefix="kr20w2-MutateEmulatorV2-3-")` allocated `/tmp/kr20w2-MutateEmulatorV2-3-jngeg0ub`. `git clone -q --no-hardlinks --no-checkout <LANE> <clone>` and `git -C <clone> checkout -q --detach 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` each exited **0**; `git -C <clone> rev-parse HEAD` exited **0**, stdout `5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`.
- Original source bytes came from `git -C <LANE> show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/tools/swiss-misread-v2.py` (**0**). Mutation locations below use S line numbers. Every restored run also serves as the next mutant's pristine baseline.
- The eight carrier paths and SHA-256 values were read from S's `.ufo/waves/round-20/evidence/retro-v2/t1250-*.json` Git blobs. All live carrier hashes matched those records before and after the probe. All eight log files matched S's Git blobs. Detectors below were run at the requested lane paths only after their hashes matched S; they remained unchanged.
- Each phase used a **fresh** `/tmp/kr20w2-MutateEmulatorV2-evidence-0tltqeyz/<phase>/v2/` directory. Captured carrier stdout was written to `<label>.json`, including empty stdout on a crash; no old prediction could leak into another phase. Up to four independent Python processes ran concurrently; source edits were sequential. Each selftest was bounded to 60 s, each carrier prediction and retro to 120 s; no timeout occurred.

Command templates actually exercised (C is the clone above, LANE=`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, O is the phase's fresh output directory):

```sh
python3 -I -B "$C/.ufo/waves/round-20/tools/swiss-misread-v2.py" --selftest
python3 -I -B "$C/.ufo/waves/round-20/tools/swiss-misread-v2.py" --carrier "$carrier" --label "$label"
python3 -I -B "$LANE/.ufo/waves/round-20/tools/retro-v2.py" --v2-dir "$O" --pass2-dir "$LANE/.ufo/waves/round-19/runs/pass2" --extractor "$LANE/.ufo/waves/round-20/tools/first-failure-extract.py"
```

The carrier command ran for asm, cgo, compile, cover, go, gofmt, preprofile, vet (labels `t1250-*`), using their exact S-recorded paths. All eight generator exits were **0** in every phase except M2, where all eight were **1** with empty stdout and the TypeError below. The selftest and retro exits are recorded for every invocation:

| Phase | Selftest start (clock) | Selftest exit | Retro exit | Retro yes / no / unevaluable |
|---|---|---:|---:|---:|
| 00-pristine | 2026-10-21T04:10:42-03:00 | 0 | 0 | 8/0/0 |
| 01-mask-removed | 2026-10-21T04:11:00-03:00 | 0 | 1 | 3/5/0 |
| 02-mask-restored | 2026-10-21T04:11:17-03:00 | 0 | 0 | 8/0/0 |
| 03-null-branch-inverted | 2026-10-21T04:11:41-03:00 | 1 | 2 | 0/0/8 |
| 04-null-branch-restored | 2026-10-21T04:12:01-03:00 | 0 | 0 | 8/0/0 |
| 05-uncommon-offset-plus-ptr | 2026-10-21T04:12:23-03:00 | 1 | 1 | 0/8/0 |
| 06-uncommon-offset-restored | 2026-10-21T04:12:42-03:00 | 0 | 0 | 8/0/0 |

## Killed / survived table

| Mutant (smallest behavior-bearing edit) | Expected detector / finding | Observed selftest | Observed retro | Verdict |
|---|---|---|---|---|
| **M1** remove `_mask_func_out_count(...)` at **both** production sites, `swiss-misread-v2.py:950-951,1061-1062`; retain the helper and its test | Variadic production traversal should be checked; `variadic_masked` is the named check (`:1788-1790`); retro should reject changed kind/index or false failures on silent logs | **0**, `SELFTEST: CLEAN cases=17` | **1**, five `no`, three `yes`; all predictions usable | **SURVIVED selftest; KILLED retro** |
| **M2** invert `if walk is None:` to `if walk is not None:` in `first_failure_record`, `:1464` | `first_failure_shape` (`:1809-1819`) or null/non-null comparison should reject the reversal | **1**, empty stdout; `TypeError: 'NoneType' object is not subscriptable` at `:1467`, before the named assertion | **2**, eight `unevaluable`; generators failed, so each empty JSON gives `prediction_unreadable: Expecting value: line 1 column 1 (char 0)` | **KILLED by selftest crash; retro INCONCLUSIVE**, not a semantic kill |
| **M3** shift `uncommon_addr` from `type_addr + self.bound_size(kind)` to `type_addr + self.bound_size(kind) + self.ptr`, `:744` (+8 bytes on these amd64 inputs) | Slot-40 H1 map-path failure / EOF should disappear or move; retro should reject changed first failures | **1**, `SELFTEST: FAILED slot40-h1-fail: ` | **1**, eight `no`; all predictions usable | **KILLED by both** |

**Coverage finding:** M1 leaves the helper-only `variadic_masked` assertion green while bypassing that helper in both real call paths. This is an observed selftest blind spot, not permission to weaken the mask contract. Retro catches it on asm, compile, cover, go, vet; cgo, gofmt and preprofile alone would not kill this mutant. M2 does not demonstrate that `first_failure_shape` or the comparator catches a valid but reversed projection: the minimal predicate inversion crashes earlier. M3's observed first selftest failure is `slot40-h1-fail`, not the later EOF-equality assertion. No production fix was made.

## Before / mutant / restored SHA-256

All phase hashes were stable from detector start to detector end.

| Mutant | Pristine source | Mutated source | Restored source |
|---|---|---|---|
| M1 | `a4810430ff152043faca9fa19cb6942af711df9d2cf150e1c9f0544eba35cf1e` | `f0c829e03f36a93a90f1fd2d7fe3b909ac621a78ff8444280ec8b48c6684d0d2` | `a4810430ff152043faca9fa19cb6942af711df9d2cf150e1c9f0544eba35cf1e` |
| M2 | `a4810430ff152043faca9fa19cb6942af711df9d2cf150e1c9f0544eba35cf1e` | `22772738e5852b3c9e68235037a6cfe1e587af443a8f91fc8dc9b09072bec233` | `a4810430ff152043faca9fa19cb6942af711df9d2cf150e1c9f0544eba35cf1e` |
| M3 | `a4810430ff152043faca9fa19cb6942af711df9d2cf150e1c9f0544eba35cf1e` | `006657fdb36c619d6f72d2422861a9702ac2e196554fbd3d391ed5939e7d56c1` | `a4810430ff152043faca9fa19cb6942af711df9d2cf150e1c9f0544eba35cf1e` |

After the last restoration, `cmp - <clone>/.ufo/waves/round-20/tools/swiss-misread-v2.py` with S's original Git blob on stdin exited **0**, empty stdout/stderr: exact-byte restoration. Every restored selftest stdout and retro stdout was byte-identical to the pristine run. All input, dependency and carrier hashes remained unchanged. Both mkdtemp trees were then removed successfully; no source patch is delivered and the only lane write is this report.

## Actual retrospective stdout

Comparator equality is kind+index (or both null), deliberately ignoring VA/phase: `compare-first-failure.py:28-34`. These are captured CSV bytes, not reconstructed expected results. The seven silent original labels plus vet index 13902080 are reproduced in every restored run.

### Pristine and every restoration (identical bytes of stdout)

```csv
label,predicted,observed,match
t1250-asm,null,null,yes
t1250-cgo,null,null,yes
t1250-compile,null,null,yes
t1250-cover,null,null,yes
t1250-go,null,null,yes
t1250-gofmt,null,null,yes
t1250-preprofile,null,null,yes
t1250-vet,"{""index"":13902080,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":7599264}","{""index"":13902080,""kind"":""invalid_index"",""phase"":""markup"",""va"":null}",yes
```

### M1 mask removal

```csv
label,predicted,observed,match
t1250-asm,"{""index"":20,""kind"":""unmapped"",""phase"":""markup_walk"",""va"":6395840}",null,no
t1250-cgo,null,null,yes
t1250-compile,"{""index"":8,""kind"":""unmapped"",""phase"":""markup_walk"",""va"":14828480}",null,no
t1250-cover,"{""index"":8,""kind"":""unmapped"",""phase"":""markup_walk"",""va"":6394880}",null,no
t1250-go,"{""index"":8,""kind"":""unmapped"",""phase"":""markup_walk"",""va"":11225568}",null,no
t1250-gofmt,null,null,yes
t1250-preprofile,null,null,yes
t1250-vet,"{""index"":1801722468838924630,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":7586208}","{""index"":13902080,""kind"":""invalid_index"",""phase"":""markup"",""va"":null}",no
```

### M2 null-branch inversion

```csv
label,predicted,observed,match
t1250-asm,null,null,unevaluable
t1250-cgo,null,null,unevaluable
t1250-compile,null,null,unevaluable
t1250-cover,null,null,unevaluable
t1250-go,null,null,unevaluable
t1250-gofmt,null,null,unevaluable
t1250-preprofile,null,null,unevaluable
t1250-vet,null,null,unevaluable
```

### M3 uncommon offset + pointer

```csv
label,predicted,observed,match
t1250-asm,"{""index"":23147009,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":6395328}",null,no
t1250-cgo,"{""index"":39810136,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":6243040}",null,no
t1250-compile,"{""index"":39120130,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":14828224}",null,no
t1250-cover,"{""index"":834163201,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":6384384}",null,no
t1250-go,"{""index"":61354547,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":11222304}",null,no
t1250-gofmt,"{""index"":22299649,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":5539232}",null,no
t1250-preprofile,"{""index"":29241600,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":5161888}",null,no
t1250-vet,"{""index"":852107777,""kind"":""invalid_index"",""phase"":""markup_walk"",""va"":7585760}","{""index"":13902080,""kind"":""invalid_index"",""phase"":""markup"",""va"":null}",no
```

## Input pins

Observed detector hashes (all match S):

- `retro-v2.py`: `57d95bf0cdf5f6cb617b5a11ada67c895dd71318ae2c9cd48292b21e4fda659f`.
- `first-failure-extract.py`: `aa4372b28d7228d07d44980c8bf3ebe3ed65b1fab5ca38bcee5d76c273b8e485`.
- `compare-first-failure.py`: `44150d137c8ac07321da133d50e7c8f12c664bb12d64cf0a9a66c0ab9595121f`.
- Installed snapshot `go1.25.0.json`: `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252` (unchanged).

Observed bound-log hashes (all match S and unchanged):

| Lane-relative log | SHA-256 |
|---|---|
| `.ufo/waves/round-19/runs/pass2/t1250-asm/logs/rea-ghidra-nVeBgA/ghidra.log` | `6decce08ea7db0985ac1bff4597130c94d2d3240c7a0f8a32963cdce363dc13d` |
| `.ufo/waves/round-19/runs/pass2/t1250-cgo/logs/rea-ghidra-vPyu5c/ghidra.log` | `1f31c0f54e6b1b929303532d17714810b215752fdac1d2abe8daee445b375f3d` |
| `.ufo/waves/round-19/runs/pass2/t1250-compile/logs/rea-ghidra-07WMDZ/ghidra.log` | `d95116cbf2e92b05fd3829b3317a9d4ff37446e9a77794943e9d7101371448b9` |
| `.ufo/waves/round-19/runs/pass2/t1250-cover/logs/rea-ghidra-OkHIR2/ghidra.log` | `b0eaedb1d554d154308d3596bec8a6c5db4940891ee2c52a00b0a36c407827cb` |
| `.ufo/waves/round-19/runs/pass2/t1250-go/logs/rea-ghidra-WJgbct/ghidra.log` | `57e64377385b1f431b5e060f9ef75e78426b3f8dc07404df0bb42cbbf0629bd7` |
| `.ufo/waves/round-19/runs/pass2/t1250-gofmt/logs/rea-ghidra-DttY3R/ghidra.log` | `d3fa1232f60cc2255ffcd5c11a8f095d2a18b387d7f174a70d0eeb3f12a38773` |
| `.ufo/waves/round-19/runs/pass2/t1250-preprofile/logs/rea-ghidra-npYN1g/ghidra.log` | `816ca3c64a7b8e14c6821ef12fdc3ec06fcb90b621b97abaabe9918185c92601` |
| `.ufo/waves/round-19/runs/pass2/t1250-vet/logs/rea-ghidra-PEkTou/ghidra.log` | `621e0ef90478935a1f3a81c9bc318f675d93666b5f1649276f0a42446ff4296c` |

No Go toolchain binary, REA command, Ghidra analyzer, or alternative runtime was invoked. Only Python byte emulation/read-only log extraction and Git/coreutils provenance operations were used. Installs/updates: **none**.
