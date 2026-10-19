# CN-2 — cross-chain verdict (arc3-loop1-round9)

## Scope and evidence boundary

Measured against `HEAD=947091d6b6f52684faf9ca53adf94ff8a0f6b006`. I re-ran the listed commands and REA calls; I did not use another seat's numeric values as evidence. Source, gate, corpus, and operator config were read-only. My only workspace write is this verdict artifact. Scratch data was under `/var/tmp`.

## C1 — freshness

**Live archive inventory — VERIFIED; PROVINCE row — CORRECTED in proposal only.** `PROVINCE.md:50` currently says `1556 signed archives` without a local as-of date. My direct output:

```text
$ ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l
1350
$ ls /var/cache/pacman/pkg/*.sig | wc -l
1350
$ wc -l PROVINCE.md
162 PROVINCE.md
$ python3 - <<'PY'  # independently pair archive filenames with .sig sidecars
from pathlib import Path
root = Path('/var/cache/pacman/pkg')
archives = {p.name for p in root.iterdir() if p.is_file() and p.name.endswith('.pkg.tar.zst')}
signatures = {p.name for p in root.iterdir() if p.is_file() and p.name.endswith('.pkg.tar.zst.sig')}
expected = {name + '.sig' for name in archives}
print(f'archives={len(archives)} signature_sidecars={len(signatures)} missing={len(expected-signatures)} orphan={len(signatures-expected)}')
PY
archives=1350 signature_sidecars=1350 missing=0 orphan=0
```

Thus the live pathname counts are 1,350 and 1,350. The difference against the dated literal still in the row is `1350 - 1556 = -206`; the historical cache itself is not reconstructable from the current filesystem, so that baseline is not a fresh observation. The pathname count does not cryptographically verify every detached signature.

**Other row perishables — VERIFIED / UNVERIFIABLE.** I rechecked the installed-jq result directly:

```text
$ pacman -Q jq
jq 1.8.2-1
$ pacman -Qkk jq
jq: 25 total files, 0 altered files
$ sha256sum /usr/bin/jq
 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
$ tar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum
 e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  -
cmp=identical
```

The byte-identity statement is VERIFIED for this recheck and should be dated in replacement text. `available:true in live session` is UNVERIFIABLE as a current REA-session status here; the table context at `PROVINCE.md:40` dates its recorded survey, and I had no attached `binary_session` tool. `.MTREE per-file sha256`, `pacman -Qkk verify`, and `binary_session {}` are format/procedure/probe descriptions rather than additional live numeric values.

Among the delivered C1 drafts, `claims/c1/PL-2.md:23` is the best integration candidate: it preserves the old count as dated, points to the append-only erratum at `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`, dates the live recount and the historical availability, and dates the fresh jq check. Other patches that leave either volatile statement undated need that qualifier added. All C1 reports are patch text only; none changed `PROVINCE.md`.

**Census requirement — DISCREPANCY.** The checked-in instrument does not pass at HEAD, before a proposed row patch. I ran `python3 .ufo/gates/c1-census-v10.py --quiet`; decisive output:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=17, SKILL.md=3; total loci=19; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
exit=1
```

`python3 .ufo/gates/c1-census-v10.py --json` identifies the sole blocker as `SCORECARD.md` block `1833-1839`, line `1834`, an unscoped `6.7.0` pin assertion. The gate SCOPE ends the SCORECARD range at `1813` (`.ufo/gates/c1-census-v10.py:276`); the offending text is beyond it. This is independent of the PROVINCE row, and the frozen “instrument still PASS” condition is not met. The gate and SCORECARD are outside this seat's write scope, so I did not attempt a repair.

## C2 — coverage

**Command A baseline — VERIFIED at HEAD; post-landing result — UNVERIFIABLE.** I ran the `SCORECARD.md:88-124` recipe over the immutable HEAD object. Exact result:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 87, "mapped": 87, "missing": [], "revision": "947091d6b6f52684faf9ca53adf94ff8a0f6b006", "rule_blocks": 15}
```

**Selected still-open Unknown — R6 viaIR final selector-miss interaction with `fallback()` (EX-8): REPRODUCED, narrowly.** The frozen C2 scope permits one cited Unknown. The R6 entry explicitly leaves the `SUB`-leg/fall-through interaction with a real fallback unmeasured (`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`). I selected EX-8's paired synthetic `ViaIrVault` sources because they test that exact residual under solc 0.8.37, `viaIR:true`, optimizer enabled/runs=200, and the proposed corpus draft has a runnable recheck (`claims/c2/EX-8/evidence/draft-corpus-entry.md:1-15`). I independently copied those read-only source bytes under `/var/tmp`, recompiled each twice using the existing wave-1 solc prefix, re-ran REA 6.7.0, and ran the seat's byte-walk script. Reproduction commands (all outputs and scratch remain under `/var/tmp`; every REA call sets disk-backed TMPDIR):

```sh
ROOT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
ART="$ROOT/.ufo/waves/arc3-loop1-round9/claims/c2/EX-8/evidence"
PREFIX="$ROOT/.ufo/waves/arc3-loop1-round1/tools/solc-prefix"
REA=/home/vgpnk/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents
RUN=$(mktemp -d /var/tmp/kaidoku-cn2-ex8.XXXXXX)
mkdir -p "$RUN/src" "$RUN/compile" "$RUN/probes" "$RUN/tmp"
cp "$ART/source/ViaIrVault.no-fallback.sol" "$ART/source/ViaIrVault.fallback.sol" "$RUN/src/"
TMPDIR="$RUN/tmp" node "$ART/compile.js" "$PREFIX" "$RUN/src" "$RUN/compile" > "$RUN/compile-summary.json"
python3 "$ART/walk.py" "$RUN/compile" > "$RUN/dispatch-walk.txt"
TMPDIR="$RUN/tmp" node "$REA/scripts/rea.mjs" inspect-evm-interface "$RUN/compile/no-fallback/runtime.hex" hex --format json > "$RUN/probes/no-fallback.json"
TMPDIR="$RUN/tmp" node "$REA/scripts/rea.mjs" inspect-evm-interface "$RUN/compile/payable-fallback/runtime.hex" hex --format json > "$RUN/probes/payable-fallback.json"
```

First-hand outputs:

```text
compiler=0.8.37+commit.f401782d.Emscripten.clang
soljson_sha256=221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c
no-fallback source_sha256=f53911672f2e33eaabaeff85e75c2565bb2899638d194fb3ffe6747abe80cbbe
payable-fallback source_sha256=9c5c2d461bc2a3142984c6adb0f2082d3d3fd8ec3753105d3342bef812b51e6d
no-fallback: runtime_bytes=1517 runtime_sha256=2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a repeat=True abi_functions=15 fallback=0 receive=1 selector_sets_match=True decoded_sha_match=True
payable-fallback: runtime_bytes=1525 runtime_sha256=a064b8de5b7d0aa924980f21df768e9338d41678d9e04bb0acebe8dcd029968d repeat=True abi_functions=15 fallback=1 receive=1 selector_sets_match=True decoded_sha_match=True
COMPARE_ROWS=15 EQ=14 SUB=1 SELECTOR_SET=01681a62,1c8e5adb,2e1a7d4d,3f4ba83a,5ff1f6ee,6901eb1e,69fe0e2d,6e69f38c,78d20574,8456cb59,8e943bce,90ab171e,9389acb5,d0e30db0,ee02438e
no-fallback: SUB_LEG_PC=0xc2 MISMATCH_BRANCH_TARGET=0xe; nonempty unknown selector path ends at REVERT
payable-fallback: SUB_LEG_PC=0xcf MISMATCH_BRANCH_TARGET=0xe; nonempty unknown selector path reaches CALLVALUE, SLOAD slot 2, then SSTORE slot 2
SAME_15_SELECTOR_SET=True
```

The REA raw/normalized selector sets matched each compiler ABI method-identifier set (15/15); each decoded-bytecode digest matched its freshly compiled runtime. The retained peer captures are at `claims/c2/EX-8/evidence/probe/{no-fallback,payable-fallback}.json`, and the independent compile/walk implementation is `claims/c2/EX-8/evidence/{compile.js,walk.py}`. The miss-path interpretation is **static control-flow inference**, not executed contract behavior: empty calldata branches separately to `receive()`, and the payable fallback's source adds `msg.value` to `fee_`. This closes only the measured source/compiler/settings dispatcher question; it does not establish execution, deployment identity, or general behavior for other fallback bodies or solc settings.

**Candidate reconciliation.** I select EX-8's one draft and token (`corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md`; `2026-10-19-arc3-r9-viair-fallback-miss`). EX-6 measures the same R6 Unknown with another carrier and is a valid alternative, but I will not co-land both. EX-8 has the exact paired no-fallback/fallback case, a repeatable draft recheck, and my independent fresh compile/probe/walk. Other candidates are also technically supported but answer different or less direct questions: CR-1/EX-11 test different `ev_` verb families; EX-5/EX-12 test other solc versions; the Vyper candidates revisit the R8 boundary. R8 already records runtime equivalence for `--no-optimize` and `-O none` (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:11`), while EX-10's broader format sweep reports differing raw AST/ZIP outputs but equal canonical JSON/archive-member payloads and varying repeat timestamps (`claims/c2/EX-10/evidence/measure.txt:17-18,34`; `claims/c2/EX-10/evidence/compile/comparison.json:38-50,101-108,170-177,228-235`). That sweep is useful residual characterization, but it does not demonstrate a flag-caused bytecode difference. I therefore do not claim every Vyper question is redundant; I prefer the separately named, explicitly unmeasured R6 fallback interaction.

No corpus entry/map token has been landed. The measured after-state remains **UNVERIFIABLE**: Command A must be rerun after the integrator lands exactly one entry and matching map token, and must then show `knowledge_files=88`, `mapped=88`, `missing=[]`, `dangling=[]`.

## C3 — pin-line drift class

**Live pin and instrument assertion — REPRODUCED.** First-hand read-only output:

```text
$ grep -n 'rea-agents@' /home/vgpnk/.kimi-code/config.toml
4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
$ grep -c 'rea-agents@' /home/vgpnk/.kimi-code/config.toml
1
```

I called the gate's `classify()` on current `PROVINCE.md` and `live_pins()` from the current gate. Its assertion-level output was:

```text
{'block': '15-26', 'record_disposition': 'info', 'assertions': [
 {'kind': 'ptr', 'value': '/home/vgpnk/.config/devin/mcp_config.json:7', 'disp': 'current-ok', 'why': 'pins 6.5.0'},
 {'kind': 'ptr', 'value': '/home/vgpnk/.omp/agent/mcp.json:8', 'disp': 'current-ok', 'why': 'pins 6.5.0'},
 {'kind': 'ptr', 'value': '~/.kimi-code/config.toml:4126', 'disp': 'current-ok', 'why': 'pins 6.7.0'}]}
```

The containing record aggregates as `info`, but the Kimi pointer assertion itself is `current-ok`. The complete gate still exits 1 for the same unrelated SCORECARD undeclared locus stated above.

**Pointer volatility — REPRODUCED in a synthetic scratch config, not by editing the live config.** With the actual gate's `ptr_check()` and a minimal config under `/var/tmp`, inserting two lines before the pin produced:

```text
synthetic_anchor: {'devin': '6.7.0', 'omp': '6.7.0', 'kimi': '6.7.0'}
line_5_before_edit: ('ok', 'pins 6.7.0')
line_5_after_edit: ('stale', "line holds no rea-agents pin: '# synthetic'")
line_7_after_edit: ('ok', 'pins 6.7.0')
```

The live file currently has one match, but the gate's `live_pins()` uses a first-match search (`.ufo/gates/c1-census-v10.py:324-334`) and does not enforce uniqueness. `ptr_check()` dereferences the literal line (`:466-482`); insertions/deletions before the stanza therefore move the pin and require re-anchoring. This is a positional pointer, not a stable stanza key. No operator config edit or historical movement chronology is claimed. The frozen C3 request also requires this characterization to land as a corpus erratum or measured receipt note; neither canonical path was changed in this seat, so that placement remains **UNVERIFIABLE / pending authorized integration**.

## Peer convergence and limits

At final inventory, all 12 C1, all 12 C2, and all 12 C3 seat reports and all 12 verdict artifacts were present. C1/C3 peers and my checks agree on the live 1,350 archive/sidecar counts, the jq recheck, the out-of-scope SCORECARD gate failure, and the live Kimi pointer's `current-ok` / positional-drift behavior. I do not claim the full historical line-movement chronology; peers mark the intermediate `:3546` unverified from available snapshots.

C2 recommendations remain divided, not unanimous: CN-1, CR-7, and VZ-3 select EX-8; CN-4 prefers EX-6's related fallback carrier; CR-5, CR-6, and VZ-4 select EX-10's Vyper output-boundary sweep; CN-3 selects CR-1's SQLite Evidence-ID case; VZ-2 selects EX-5's other-solc version case; CR-8 and VZ-1 select the Vyper creation-bytecode residual. I select EX-8. This is four of twelve verdict seats, not a majority; EX-6 independently supports the same explicitly named R6 fallback Unknown. The alternatives are valid, bounded measurements of different candidates, not reasons to co-land multiple entries for one frozen C2 move. Earlier peer reports with incomplete inventory counts reflect their write-time snapshots, not the final set.

Overall: C1's count correction is supported but its frozen gate-PASS condition is discrepant; C2's chosen candidate is independently reproduced but no corpus/map token is landed and post-landing Command A remains unverified; C3's targeted pin check and drift class are reproduced while the whole gate remains red.
