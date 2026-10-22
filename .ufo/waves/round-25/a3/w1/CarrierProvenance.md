# R25 a3 w1 — CarrierProvenance

Seat: leaf, lane read-only. Commands ran from the lane root; the full log with UTC times and exit codes is `transcript.txt` in the scratch dir. No lane file was written except this report.

## Verdict

- **Observation:** all six carriers in `corpus/evidence/round-25/a2/c2/carriers.tsv` (6 data rows, no header; `cat`, exit 0, 2026-10-22T10:49:09Z) are lane-authored, lane-compiled contracts from arc3-loop1 rounds 1, 3 and 4. Every source, compile driver or receipt, ABI and bytecode is committed in the wave tree. None is a shipped, deployed or third-party artifact; no deployment address or verified-source record appears in the `carriers.tsv` rows, ABIs or compile receipts.
- **Observation:** no producing round referenced 4byte.directory or openchain. `grep -rl '4byte\.directory\|openchain'` over the three round trees returned no file, `grep_exit=1` (2026-10-22T10:49:10Z). Round 1's plan says "no signature DB exists" (`PL-1/plan.md:392`); the round-3 entry says "selectors stay as bare hashes (no signature DB → no name resolution)" (`corpus/knowledge/2026-10-13-r3-evm-interface.md:142`).
- **Verdict on "were names chosen to collide": holds as "no".** No evidence of database-driven naming. `[inference]` names follow the intended shape (ERC-20 set, vault vocabulary, deliberately unusual account-level names), not a lookup table.
- **But the sample is strongly biased toward database-known vocabulary.** Observation: 61 of 69 selector rows and 36 of 43 distinct selectors already had the ABI signature in a saved lookup; 21 of 69 rows are ten ERC-20-family signatures.

## Per-carrier provenance

| carrier | produced in / seat | compiler and version | optimizer | ABI shape (K) | DB truth rows |
|---|---|---|---|---|---|
| rv2token | round 1 / RV-2 (reviewer) | solc 0.8.37+commit.f401782d.Emscripten.clang | disabled (`solc-input.json`: `enabled:false`) | canonical 5-function ERC-20 (5) | 5/5 |
| kdxtoken | round 1 / source EX-06, selected bytes EX-05 | solc 0.8.37+commit.f401782d.Emscripten.clang | no optimizer key in either driver; solc default off `[inference]` | ERC-20-style plus `mint` (6) | 6/6 |
| vaultb-opt200 | round 3 / EX-10 | solc 0.8.37+commit.f401782d.Emscripten.clang | enabled, runs=200 | non-ERC-20 vault (13) | 13/13 |
| carrierb | round 3 / EX-05 | solc 0.8.37+commit.f401782d.Emscripten.clang | enabled, runs=200 | non-ERC-20, payable receive+fallback (8) | 7/8 |
| stewardtoken | round 4 / EX-03 | Vyper 0.4.3+commit.bff19ea2 | no `-O` flag; Vyper default `-O gas` | ERC-20 set plus steward role (22) | 18/22 |
| carrierv | round 4 / EX-04 | Vyper 0.4.3+commit.bff19ea2 | no `-O` flag; Vyper default `-O gas` | non-ERC-20 vault, zero ERC-20 selectors (15) | 12/15 |

Pins (sources hashed by `sha256sum`, exit 0, 10:46–10:53Z):

- **rv2token** — source `claims/c1/RV-2/Rv2Token.sol` `a4bc2d78…328c`; seat report lines 21-22: "**Independent carrier authored + compiled on-host** with the wave's solc / 0.8.37 prefix" (`grep`, exit 0). `solc-out.json` deployed bytecode equals the committed runtime hex (`solc_out_equals_file True bytes 1943`, decoded `c1081a56…5e74`).
- **kdxtoken** — source by EX-06, "`KdxToken.sol` (ERC-20-style, 6 external functions)", compiler "solc **0.8.37**+commit.f401782d" (`EX-06/comparison.md:26-27`). Selected file from EX-05's `compile-kdx.js`, "byte-identical to EX-06's recorded subject digest" (`EX-05/README.md:27`); decoded runtime `9c40940e…580e`, 1789 B.
- **vaultb-opt200** — EX-10's own `VaultB.sol` (source `6b3d04cb…afd0`; decoded runtime `b24a0115…40b6`, 1621 B), called "extra replication evidence and it is never presented as the wave's carrier B" (`EX-10/recon-B.md`); compiler receipt `solcjs --version → 0.8.37+commit.f401782d.Emscripten.clang` (`recon-B.md:56`).
- **carrierb** — EX-05's own `CarrierB.sol`, written although its seat line says "compile carrier B (same optimizer settings)" (`seats/EX-05.md:2-3`). Report output: `compiler 0.8.37+commit.f401782d.Emscripten.clang`, `optimizer {'enabled': True, 'runs': 200}` (`out/CarrierB.report.json`, exit 0). Header: "Shape planted deliberately"; names `owner, tally, credit, tag, rate, fund, sweep, note`.
- **stewardtoken** — EX-03's Vyper token: "ERC-20-selector-bearing token (the r1 entry's `Rv2Token` class)" (`token.vy:8`). Receipt: `vyper --version → 0.4.3+commit.bff19ea2`; four `vyper -f …` commands, no `-O`/`--no-optimize` (`compile-receipt.txt:29-37`).
- **carrierv** — EX-04's Vyper carrier, "Deliberately carries zero ERC-20 selectors" (`src/CarrierV.vy:8`). Receipt: `vyper_version: 0.4.3+commit.bff19ea2`, `combined_exit=0`, runtime 1562 B `57d6fd0a…1dae0`.

Vyper's default was measured: the pinned binary's help says `-O, --optimize {gas,codesize,none}` / "Optimization flag (defaults to 'gas')" (exit 0, 10:49:10Z). The two solc drivers that set no optimizer block contain zero occurrences of "optimizer" (`grep -c`, 0/0); solc's standard-JSON default of off is `[inference]`.

## Was any name chosen to collide with a database entry?

- **Observation:** no reference to either database appears in rounds 1/3/4 (same grep, `grep_exit=1`), and no saved lookup response is committed there. Round 4's only collision check compared type variants of one source name: "fee_quote(uint256) -> 6e8efde2 | fee_quote(int128) -> 59e91d89 | collide=False" and "collisions found: 0 (expected 0)" (`EX-05/attacks.txt:23-25`, exit 0).
- **Observation against deliberate collision:** seven rows have no candidate in either database, including `note(bytes32,uint256)` (`3efdef66`, carrierb) and `fee_of(uint256,uint256)` (`0c751377`, carrierv and stewardtoken). A collision-seeking author would be unlikely to plant these.
- **Inference:** the high resolution rate comes from conventional naming. Three carriers deliberately reproduce the canonical ERC-20 set; the vault carriers use OpenZeppelin-style names (`owner`, `deposit`, `withdraw`, `pause`, `unpause`, `paused`, `balances`).

## Why the sample is biased

1. **Label and artifact share one origin.** Each "true" name is read from the ABI emitted by the same compile that produced the bytecode. This measures compiler-to-ABI mapping on lane-written sources, not name recovery on deployed or verified contracts.
2. **Vocabulary bias.** Observation: 21 of 69 rows are ten ERC-20-family signatures (`transfer`, `approve`, `transferFrom`, `balanceOf`, `allowance`, `totalSupply`, `name`, `symbol`, `decimals`, `mint`). Sixteen selectors repeat across carriers: ten appear three times (the five ERC-20 core names plus `owner`, `pause`, `unpause`, `paused`, `deposit`) and six twice. Row-level rates over-weight a handful of ubiquitous names; the sample is only 43 distinct selectors.
3. **Shape and build bias.** Small hand-written contracts (5–22 functions), one solc version, one optimizer point (runs=200 for the two enabled builds), no explicit EVM version, no Vyper `-O` variant, no proxy, no obfuscation, no compiler-mangled names. `__default__` carries no selector, so Vyper fallbacks add nothing to the test.
4. **Selection is a judgement subset, not a census.** Observation: the three rounds contain 117 `*runtime.hex` paths (8 / 64 / 45; counts include duplicates and variants) versus six chosen. `carriers.tsv` is the only record of the selection; round-25 `a2/claims.json` names no carriers and records no inclusion rule. Exclusions include the round's nominal carrier B (EX-04 `VaultB`, K=11), round-1's other compiled carriers (`EX-04/ex03-token/token.runtime.hex` 3457 B, `CR-1/evidence/solc-runtime.hex` 1508 B), and round-4 CR-1's optimizer/EVM shape family. Unknown: why these six.
5. **Name ambiguity inside the source tree.** Observation: three round-3 artifacts carry the "carrier B"/"VaultB" name (EX-04 `VaultB` K=11, EX-05 `CarrierB` K=8, EX-10 `VaultB` K=13; `recon-B.md:176-181`). EX-05 also has `recompiled/opt200/VaultB.runtime.hex`, a recompile of EX-04's source (decoded `aaf85cea…9412`, 1850 B), not the selected EX-10 file (`b24a0115…40b6`). The `carriers.tsv` paths disambiguate; bare names do not.

## Limits and remaining unknowns

- **Observation:** neither `LOG.md` nor the new C2 knowledge entry records carrier provenance: `grep -i 'kdx\|rv2\|carrierb\|vaultb\|steward\|carrierv' LOG.md` matched no line (`grep_exit=1`, 10:53:26Z), and the C2 entry contains zero `arc3-loop1-round` strings (`grep_exit=1`). This trace rests entirely on the committed wave tree (sources, drivers, receipts, seat reports).
- The six-carrier selection rule is not recorded; independence from database resolvability cannot be tested from committed evidence.
- The two solc builds without an optimizer block, and their EVM version, are inferred from absent keys; I did not recompile to confirm.
- Vyper's `-O gas` is observed from the pinned 0.4.3 binary's help, not from a per-carrier flag.
- `[inference]` The excluded carriers are also conventional lane-written contracts, so the direction of selection bias is plausibly small but is not measured here.

## Scratch artifacts (sha256)

`analyze-rows.py` `3cfbaed37cff27d632696918b78361e40895087d8d92795a7cf9e9a54361faed`; `carrier-identity.txt` `17cebeee1f32c569b0c0fa3649acf4b0074ba7bf8cf1e080d30d093281b3f73e`; `transcript.txt` `34cf3469a7c13aa0e62ad99bcb11fdf6e988679d50310fd57423089b4e2a0a21`; `provenance.json` `8358de3ae2883b51f04f3fd85f7681eb7e2e72defa3a5ea76edfb118951e1cbf`.

No tools were installed or upgraded for this seat.

Report: .ufo/waves/round-25/a3/w1/CarrierProvenance.md
