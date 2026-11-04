# ExecR87Regress — independent no-harm evidence for R88-C1

Round 88 (kaidoku), wave r88-w1. Leaf executor. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
HEAD at run start `a14f0a426` (`round-88: integrate chain-geometry entry, S309/S310, craft block 28, Core row and the lesson`);
the lane advanced to `1a72fdef4` while this seat ran (`round-88: measured receipts, SCORECARD capability row and round section, LOG entry`).
Re-checked after the advance: all four C1-relevant instrument hashes are unchanged and `tools/` is clean in the
working tree, so every number below stands at the current revision.
No file under the lane was modified by this seat except the files listed at the bottom.

## Pins re-verified before any run

| object | measured sha256 | matches claims.json / task pin |
|---|---|---|
| `/usr/bin/upx` (`upx 5.2.0`) | `cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969` | yes |
| rea-agents `package.json` | `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` | yes |
| `/usr/bin/jq` | `e8156675…f7806` | yes |
| `/usr/bin/xxd` | `7b1e5d0c…ae65` | yes |
| `/usr/lib/libz.so.1.3.2` | `6c78c5e5…075ca9` | yes |
| `/usr/bin/docker-init` | `0bd49c8d…3e115` | yes |
| `tools/round-88/upx-chain-repair.py` | `59ee51b0e63d3e089c23cee066b637841133412cee50748d84d717d61f8a0b46` | yes (instrument pin) |
| `tools/round-88/upx-chain-battery.py` | `a01ed6227878db2a64c7274d6ad2f37aa7c2e3462629cbb1f8619094bc037160` | yes (instrument pin) |
| `tools/round-87/upx-tamper-battery.py` | `0f2d2bd80108ded5282dbb8cbf79044357538458143c97ee591cc78e8e5384b0` | yes (`pins.r87_counter_sha256`) |
| `tools/round-87/upx-magic-repair.py` | `96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24` | yes (`pins.r87_module_sha256`) |

Host: `python3 3.14.8`, `node v24.21.0`, 32 cores, work dir on `/fast` (330 GB free).
No tool install or upgrade was performed (nothing was missing); no pacman transaction.

## Receipts and measured numbers

All receipts live in this seat directory. Scratch `/fast/scratch/hyaku/kaidoku-r88/ExecR87Regress/`
was deleted after the receipts were copied out.

### 1 — frozen round-87 counter with the new repair (REA on)

```
python3 -I -B tools/round-87/upx-tamper-battery.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --repair-cmd /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-88/upx-chain-repair.py \
  --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
  --work /fast/scratch/hyaku/kaidoku-r88/ExecR87Regress \
  --json-out …/w1/ExecR87Regress/r87-with-r88-repair.json \
  --evidence-dir …/w1/ExecR87Regress/rea-r87-with-r88-repair
```

**`recovered 8 of 8`, target 8, `controls_ok` all true, `met_target` true, exit 0, wall 139.87 s.**
Per case (T1-zero / T2-foreign × 4 carriers) all five arms true; REA procedure counts equal
`DECLARED_ORIG`: jq 167, xxd 99, libz 184, dinit 1268 (segment/string counts 30/190, 29/103,
29/199, 29/1111). Controls: `N1-refuse-plain` 4/4 refused (rc 2); `N3-intact-idempotent` 4/4
byte-identical; `N2-corrupt-payload` 0/4 recovered (repair rc 0 on all four — see finding F6).
Receipt: `r87-with-r88-repair.json`; REA evidence: `rea-r87-with-r88-repair/`.

### 2 — round-88 counter, `--no-rea` vs REA, same tree

```
python3 -I -B tools/round-88/upx-chain-battery.py --root <lane> \
  --repair-cmd <lane>/tools/round-88/upx-chain-repair.py --pkg <rea pkg> \
  --work <scratch> --json-out …/r88-no-rea.json   --evidence-dir …/rea-r88-no-rea   --no-rea
python3 -I -B tools/round-88/upx-chain-battery.py --root <lane> \
  --repair-cmd <lane>/tools/round-88/upx-chain-repair.py --pkg <rea pkg> \
  --work <scratch> --json-out …/r88-with-rea.json --evidence-dir …/rea-r88-with-rea
```

| run | recovered | controls | regression arm | exit | wall |
|---|---|---|---|---|---|
| `--no-rea` (`r88-no-rea.json`) | 0 of 4 (target 4) | all true | 8 of 8, met | 1 | **90.01 s** |
| REA on (`r88-with-rea.json`) | **4 of 4** | all true | 8 of 8, met | **0** | **154.95 s** |

Agreement on non-REA arms: **0 disagreements**. For all 4 carriers `repair_rc0`, `field_only`,
`test_ok`, `identity` are identical between the two runs, as are `block0`, `packed_sha256`,
`tampered_sha256`, `repaired_sha256`, `unpacked_sha256`; controls and regression arm identical.
The only differing field is `recovered` (4 cases), which follows from `rea_recover` being false by
construction under `--no-rea`. The REA-on receipt is byte-identical, case for case, to the frozen
pre-declaration receipt `.ufo/waves/round-88/pre/c1-candidate-at-declaration.json`
(0 disagreements over arms, hashes and offsets; block0 = 576/576/9304/576).

### 3 — selftests

`selftests.txt`:

| tool | cases | failures | exit |
|---|---|---|---|
| `tools/round-87/upx-tamper-battery.py --selftest` | 8 | 0 | 0 |
| `tools/round-88/upx-chain-battery.py --selftest` | 6 | 0 | 0 |
| `tools/round-88/upx-chain-repair.py --selftest` | 11 | 0 | 0 |

### 4 — repair on plain originals and non-ELF (must refuse)

`repair-refusals.txt` (`python3 -I -B …/upx-chain-repair.py --in <X> --out <Y>`):

| input | rc | output written | message |
|---|---|---|---|
| `/usr/bin/jq` (plain) | 2 | no | `refused: no validated PackHeader in the tail window; no validated PackHeader in the tail window` |
| `/usr/bin/xxd` (plain) | 2 | no | same |
| `/usr/lib/libz.so.1.3.2` (plain) | 2 | no | same |
| `/usr/bin/docker-init` (plain) | 2 | no | same |
| `MZ\0\0` stub | 2 | no | `refused: not a little-endian ELF` |
| 4 KiB random bytes | 2 | no | `refused: not a little-endian ELF` |
| a directory | 2 | no | `refused: --in is not a regular file: <path>` |

All refusals exit 2 and write nothing (F2 on the duplicated message).

## Independent checks beyond the assignment (same receipts)

### 5 — derivation vs ground truth (`geometry-derivation-vs-truth.json`)

Packed each carrier with the pinned packer, read the **true** block-0 `sz_cpr` from the untampered
packed file, zeroed it, ran the repair with `--json`:

| carrier | block0 | true `sz_cpr` | derived | `sz_unc0` | next block | sentinel | accounted / `u_len` | class |
|---|---|---|---|---|---|---|---|---|
| jq | 576 | 252 | **252** | 904 | 840 | 13988 | 30800 / 30800 | chain-geometry |
| xxd | 576 | 249 | **249** | 904 | 837 | 19509 | 38928 / 38928 | chain-geometry |
| libz | 9304 | 201 | **201** | 680 | 9517 | 63717 | 98592 / 108560 | chain-geometry |
| dinit | 576 | 226 | **226** | 736 | 814 | 357734 | 851288 / 851288 | chain-geometry |

4/4 derived value equals ground truth; repaired output equals the untampered packed bytes
byte-for-byte on all four; `upx -t` on the repaired file exits 0, on the zeroed file exits 1 with
`CantUnpackException: b_info corrupted` (all four). The round-87 repair alone refuses the same
files with rc 2 and `refused: p_info is not followed by a plausible b_info` — the base-state
behaviour the plan quotes, reproduced.

### 6 — candidate space and the `u_len` tiebreak (`geometry-candidate-space.json`)

Re-enumerated the search space independently (acceptance predicate as written in the repair) and
scored it with the declared rule:

| carrier | candidates | fitting `u_len` | accounted values | winner = truth |
|---|---|---|---|---|
| jq | 1 | 1 | 30800 | yes |
| xxd | 1 | 1 | 38928 | yes |
| libz | 1 | 1 | 98592 | yes |
| dinit | **3** | 2 | 123942159 (fits false), **851288**, 850696 | yes (851288) |

Only dinit exercises the tiebreak: an over-claiming decoy (derived 136 → 123,942,159 > `u_len`) is
rejected by `fits_u_len`, and the second fitting candidate (derived 440 → 850,696) loses to the true
one on "largest accounted". jq/xxd/libz have a single structural candidate each, so the rule is
trivially satisfied there.

### 7 — `--no-rea` is not transitive; REA cost and engine (`execve-no-rea-summary.txt`, `execve-no-rea-trace.log`)

`strace -f -e trace=execve` over the whole `--no-rea` run: **8 `node … rea.mjs analyze` execve**s
(lines 101, 190, 287, 379, 479, 577, 686, 844), all in the regression arm; 62 `upx`, 38 `python3`
execs. The main-body carrier loop runs none (its execs end before line 100), so `--no-rea`
suppresses REA in the scored body but not in the embedded round-87 regression run — which is why
that receipt reports `regression.met = true` (impossible without `rea_recover` arms) and why the
`--no-rea` wall time is 90.01 s, not seconds. Each `rea.mjs analyze` spawns `/usr/bin/java`, the
Ghidra decompiler (`/opt/ghidra/…/linux_x86_64/decompile`, 68 execs) and `jspawnhelper`; one call
on `/usr/bin/jq` measured 5.63 / 5.30 / 5.48 s.

### 8 — the repair reads only its own inputs (`repair-opens-summary.txt`)

`strace -f -e trace=openat,open,execve` of the repair on the zeroed dinit image: it opens
`--in`, `--out`, its own source and `tools/round-87/upx-magic-repair.py` (plus an ignored
`__pycache__` `.pyc` for the composed module). No carrier source path, no pin file, no network.
The source contains no carrier path or sha256 literal (grep: only the `#!/usr/bin/env` shebang).

## Findings that contradict, qualify or limit the claim / plan

- **F1 (no contradiction of the R88-C1 predicate).** The declared predicate reproduces exactly:
  `recovered 4 of 4`, all three controls true, regression arm `8 of 8` met, exit 0; and the frozen
  round-87 counter with the new repair is `recovered 8 of 8` with its controls true and exit 0.
  No arm, control or case was recovered through a byte outside the `sz_cpr` window
  (`field_only` true 4/4; `windows_only` true 8/8).
- **F2 (defect, calibration).** On a plain original the composed repair's refusal message is the
  same clause twice: `refused: no validated PackHeader in the tail window; no validated PackHeader
  in the tail window`. `repair()` concatenates the anchor refusal with the geometry refusal, and
  `geometry()` fails at the same `find_packheader` call, so the two halves are identical. Behaviour
  (rc 2, no output) is correct; the message is misleading about which stage failed.
- **F3 (counter semantics).** `--no-rea` is not transitive to the counter's regression arm: the
  regression invocation forwards `--pkg` and no `--no-rea`, so 8 REA calls still run (F7 evidence),
  and `--no-rea` can never report `met_target` because `rea_recover` is false by construction. The
  mode is a partial-instrumentation run, not a REA-free one; a reader comparing wall times should
  not attribute the whole 90 s to non-REA work.
- **F4 (population power).** The `fits_u_len` / largest-accounted tiebreak is exercised by 1 of 4
  carriers (dinit). jq, xxd and libz each admit exactly one structural candidate, so their recovery
  is single-candidate and does not test the rule. This is a limit of the evidence, not a
  contradiction; it is consistent with the plan's named limit 1.
- **F5 (named limit 1 confirmed verbatim).** libz accounts for 98,592 of `u_len` 108,560 and is
  accepted on its single structural candidate, exactly as declared.
- **F6 (control mechanism).** In `N2-corrupt-payload` the repair exits 0 on all four payload-
  corrupted files (it performs no integrity check); the control holds only because `upx -t`/`upx -d`
  reject the result. Consistent with named limit 1 ("the counter's arms, not the repair, refuse a
  wrong derivation"), but the repair itself never validates.
- **F7 (cost/calibration).** REA `analyze` ≈ 5.3–5.6 s per call and forks java + a Ghidra
  decompiler; the REA-on counter run is 154.95 s vs 90.01 s with `--no-rea`. Relevant to the
  sentinel's subject and to any future per-case budget.
- **F8 (container state, outside my scope).** `claims.json` carries an `instrument_supersessions`
  entry for `tools/round-88/field-tamper-matrix-v2.py` (R88-C2 instrument). It does not touch any
  C1 pin; all four C1-relevant hashes match `claims.json` and no counter, population, tamper, arm,
  control or carrier changed after the declaration.

## Not run (and why)

No build, lint, formatter or test suite: this seat is a leaf and the parent owns the post-integration
gate. No mutation of the lane, no git/jj write command, no spawn, no `agent://all` message.

## Files written by this seat

All under `.ufo/waves/round-88/w1/ExecR87Regress/` unless stated:

| path | what |
|---|---|
| `r87-with-r88-repair.json` | receipt 1 — round-87 counter, new repair, REA on |
| `r88-no-rea.json` / `r88-with-rea.json` | receipt 2 — round-88 counter, `--no-rea` / REA |
| `rea-r87-with-r88-repair/`, `rea-r88-with-rea/` | REA evidence JSONs behind the `rea_recover` arms |
| `selftests.txt` | receipt 3 — three `--selftest` runs |
| `repair-refusals.txt` | receipt 4 — plain originals, non-ELF, directory |
| `geometry-derivation-vs-truth.json` | receipt 5 — derived vs true `sz_cpr` |
| `geometry-candidate-space.json` | receipt 6 — candidate enumeration and tiebreak |
| `execve-no-rea-summary.txt`, `execve-no-rea-trace.log` | receipt 7 — `--no-rea` execve trace |
| `repair-opens-summary.txt`, `execve-repair-opens.log` | receipt 8 — repair file opens |
| `report.md` | this report |
| `.ufo/waves/round-88/w1/ExecR87Regress.md` (parent dir) | scoped findings trailer |
