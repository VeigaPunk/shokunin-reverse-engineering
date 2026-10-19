# RV-3 — C3 coverage: Vyper optimizer-form Unknown

## Verdict and selection

**REPRODUCED, bounded to one synthesized K8 fixture; canonical corpus landing PENDING.** I selected the r4 entry's still-open Vyper non-default-optimizer dispatcher characterization (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`), not the alternate r8 candidates. Fresh Vyper builds and REA calls reproduced the `--no-optimize` and `-O codesize` forms; a separate fresh `-O none` build was byte-identical to `--no-optimize`. This verifies the bounded experiment, not a general Vyper claim.

Proposed single corpus filename/token: `2026-10-19-arc3-r7-vyper-optimizer-forms` (append exactly this token to the EVM coverage-map row in `corpus/README.md:38`). The complete candidate entry is included below. I did not modify `corpus/` or `corpus/README.md`; landing and the post-landing Command A result are therefore **UNVERIFIABLE in this seat**.

## First-hand re-derivation

- **Source/compiler identity — VERIFIED.** The source is the synthesized eight-function K8 test contract at `.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy`, SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`. A scratch copy had the same hash. Compiler `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper` re-hashed to `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`; `--version` printed `0.4.3+commit.bff19ea2`.
- **Independent selector derivation — REPRODUCED.** The fresh ABI has 8 functions and the fresh method-id output has 8 entries. Python `Crypto.Hash.keccak` independently derived the 4-byte Keccak selectors from those ABI signatures; the set equals the compiler method identifiers and both REA result sets: `f0(uint256)=2ae1431c`, `f1(uint256)=9adbf691`, `f2(uint256)=bf3724af`, `f3(uint256)=d7b7913b`, `f4(uint256)=d7531d91`, `f5(uint256)=cf35f823`, `f6(uint256)=9b7c2962`, `f7(uint256)=364605a1`.
- **`--no-optimize` — REPRODUCED.** Fresh runtime: 617 bytes, decoded-byte SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`; hex-input SHA-256 `1dfe2699e61e8d82570dc3272d9679880e5a2fa765a0e4ce9169331ecedd939c`. `-f settings` printed `{"optimize": "none", "experimental_codegen": false}`. A second compile compared byte-identical with `cmp` (exit 0). The opcode walk found 8 opcode-boundary `PUSH4` sites and 8 `PUSH4; DUP2; EQ; ISZERO; PUSH2; JUMPI` legs. REA 6.7.0 returned 8 raw / 8 normalized rows, all `dispatch:"abi"`, selectors matching the independent set, decoded SHA matching the runtime; this run's Evidence ID is `ev_618b3a81a3fece920c4a6c106462488025a416a0c6fb6b7cbfa9ae3210c3dc55`.
- **`-O none` alias — REPRODUCED.** Fresh `-O none -f bytecode_runtime` output compared byte-identical to `--no-optimize` (same 617 decoded bytes and SHA above); its settings output also says `optimize:"none"`. No separate REA call was needed for byte-identical input bytes; the `--no-optimize` call is the REA result for that same runtime.
- **`-O codesize` — REPRODUCED.** Fresh runtime: 360 bytes, decoded-byte SHA-256 `bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5`; hex-input SHA-256 `c4af8ebcb724788f56c341c3dd0bfdb0d97aae74e1100e1c881d625f6c7ad68e`. Settings output: `{"optimize": "codesize", "experimental_codegen": false}`. The opcode-boundary walk found `PUSH4:0`, `EQ:1`, `MOD:1`, and `CODECOPY:2`. Its complete tail is `[0x12b,0x168)`, 61 bytes: header `01c3013008` (5 bytes) followed by 8 records of 7 bytes (`selector[4] || target[2, big-endian] || 0x25`). Every record selector matches the independent set and every target byte is `0x5b` (`JUMPDEST`). REA 6.7.0 returned 8 raw / 8 normalized rows with the matching selector set and decoded hash; Evidence ID `ev_bb59f5bcb7e3838dd9bc46b4588872c0b5a668de42e72f9a6bf944befcbb7b39`.
- **CODECOPY span reconciliation — CORRECTED.** The fresh byte walk gives PCs `0x05:PUSH1 0x05`, `0x07:PUSH2 0x012b`, `0x0a:PUSH1 0x1b`, `0x0c:CODECOPY`; in EVM stack order this copies **5 bytes** from code offset `0x12b` to memory offset `0x1b`. This is the five-byte header. The 61-byte tail is the full selector/target table; its first 27 bytes are only a prefix slice, not the full table and not the first copy's size. The final independent output records both facts at `evidence/rederived-lookup.json`. This reconciles, rather than averages, the R7 evidence: EX-5's “5 bytes” first-copy statement is correct (`claims/c2/EX-5/draft-corpus-entry.md:26`); EX-4's evidence explicitly labels a 27-byte tail slice (`claims/c2/EX-4/evidence/dispatch-walk.txt:22-26`); CR-1/CR-2 preserve the copy-window operands (`claims/c2/CR-1/entry-draft.md:16`, `claims/c2/CR-2/evidence/bytecode-characterization.jsonl:3`).
- **REA offsets — DISCREPANCY if interpreted as per-function handler locations.** On noopt, the 8 offsets are 31, 104, 177, 250, 323, 396, 469, 542; each is its `PUSH4` PC + 12 and points at `CALLVALUE` (`0x34`). On codesize, all 8 rows report offset 65, whose byte is `DUP1` (`0x80`), not one of the distinct table targets. The offsets are recorded tool output, not evidence that these are handler entries.
- **Mutability inference — DISCREPANCY against the compiler ABI.** The ABI declares `view` for all 8; REA infers `payable` for all 8; agreement is 0/8 on both forms. This is an upstream-inference delta, not runtime behavior or a contract defect.
- **REA limits.** The retained envelopes identify `rea-agents@6.7.0` calls, provider `evmole-interface` / `evmole@0.9.3`, `confidence:"inferred"`, `discovery_completeness:"unknown"`, and `runtime_execution:"not-performed"`. Selector/argument/mutability findings are inferences. The compiler fixture is synthesized and not a deployed or shipped contract; no EVM execution, chain/RPC lookup, or deployment identity check was performed.

Raw fresh outputs, input carriers, settings/ABI/method-id outputs, and the replay checker are under `.ufo/waves/arc3-loop1-round8/claims/c3/RV-3/evidence/`. `rederive.py` asserts source/selector identity, REA-vs-runtime hashes and selector sets, the two dispatcher shapes, offset observations, the full table, the CODECOPY operand window, and the `-O none` alias; running it with the round-4 Vyper venv's Python exits 0 and emits `rederived-lookup.json`. All compiler/REA scratch and worker TMPDIR were under `/var/tmp/kaidoku-rv3-r8.RIBKPo`; `/tmp` was not used.

## R7 draft reconciliation

The R7 Vyper option was proposed independently in EX-4, EX-5, CR-1, and CR-2, while that round selected the competing Evidence-ID candidate. Their useful common core is confirmed by this seat's fresh run. The selected filename/token above avoids the four competing draft stems. The `-O none` disagreement is resolved by this seat's fresh same-source compile and byte comparison; it is safe to state as an alias only for this fixture/compiler. The table notes are resolved by distinguishing the 5-byte CODECOPY from the 61-byte full tail and 27-byte prefix slice. I do not carry forward broad claims about other Vyper sources or versions.

## Command A and landing state

I re-ran the SCORECARD Command A recipe (`SCORECARD.md:88-124`) against both specified revisions. Exact JSON outputs:

```text
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 86, "mapped": 86, "missing": [], "revision": "7deeb36045209f3fbeb4460edd7aef5b5270af22", "rule_blocks": 15}
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 86, "mapped": 86, "missing": [], "revision": "904b724258fc9396a016bd9952b5cd40225fb7d8", "rule_blocks": 15}
```

Thus the current baseline is independently VERIFIED at 86/86. A post-landing 87/87 is **UNVERIFIABLE here** because the corpus entry and README token are drafts only; no overlay projection is represented as a real Command A pass.

## Proposed corpus entry draft

Proposed destination: `corpus/knowledge/2026-10-19-arc3-r7-vyper-optimizer-forms.md`. The map-token addition is exactly `2026-10-19-arc3-r7-vyper-optimizer-forms` on the existing EVM row; integrate both only under the parent’s authorized landing scope.

```markdown
<!-- DRAFT corpus entry — arc3-loop1-round8 RV-3. Synthetic compiler fixture; not deployed or shipped. -->

# Vyper 0.4.3 K8 optimizer forms — noopt EQ chain and codesize selector table recovered 8/8

source: `.ufo/waves/arc3-loop1-round8/claims/c3/RV-3/evidence/{noopt,codesize}.{runtime.hex,abi.json,methodids.json,settings.json}`, `evidence/rea-{noopt,codesize}.json`, `evidence/rederive.py`, `evidence/rederived-lookup.json`; source `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy` (SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`). Vyper executable `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper` (SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`), version `0.4.3+commit.bff19ea2`. K8 is a synthesized test contract with eight external `view` functions, not an externally sourced or deployed contract.

verified-at: 2026-10-19

recheck: from the lane root; all scratch and worker TMPDIR stay under `/var/tmp` (this host's `/tmp` quota is exhausted):

```bash
set -euo pipefail
V=.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper
SRC=.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy
W=$(mktemp -d /var/tmp/kaidoku-vyper-r7-recheck.XXXXXX)
mkdir -p "$W/tmp"
cp "$SRC" "$W/K8.vy"
TMPDIR="$W/tmp" "$V" --no-optimize -f bytecode_runtime "$W/K8.vy" > "$W/noopt.runtime.hex"
TMPDIR="$W/tmp" "$V" -O none -f bytecode_runtime "$W/K8.vy" > "$W/none.runtime.hex"
TMPDIR="$W/tmp" "$V" -O codesize -f bytecode_runtime "$W/K8.vy" > "$W/codesize.runtime.hex"
TMPDIR="$W/tmp" "$V" --no-optimize -f abi "$W/K8.vy" > "$W/noopt.abi.json"
TMPDIR="$W/tmp" "$V" --no-optimize -f method_identifiers "$W/K8.vy" > "$W/noopt.methodids.json"
TMPDIR="$W/tmp" "$V" --no-optimize -f settings "$W/K8.vy"
TMPDIR="$W/tmp" "$V" -O codesize -f settings "$W/K8.vy"
cmp "$W/noopt.runtime.hex" "$W/none.runtime.hex"
TMPDIR="$W/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$W/noopt.runtime.hex" hex --format json
TMPDIR="$W/tmp" npx -y rea-agents@6.7.0 inspect-evm-interface "$W/codesize.runtime.hex" hex --format json
```

- **Observation — selector set.** Fresh ABI Keccak-256 selectors match Vyper's method identifiers and both REA result sets: `2ae1431c`, `364605a1`, `9adbf691`, `9b7c2962`, `bf3724af`, `cf35f823`, `d7531d91`, `d7b7913b` (8/8). The set is specific to this source.
- **Observation — `--no-optimize` / `-O none`.** Both settings report `optimize:"none"`; their runtime hex files are byte-identical. Runtime is 617 bytes, SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`. Its 8 opcode-boundary `PUSH4` selector sites each use `PUSH4; DUP2; EQ; ISZERO; PUSH2; JUMPI`. REA 6.7.0 returned 8 rows / 8 unique selectors, all `dispatch:"abi"`; this run's Evidence ID is `ev_618b3a81a3fece920c4a6c106462488025a416a0c6fb6b7cbfa9ae3210c3dc55`.
- **Observation — `-O codesize`.** Runtime is 360 bytes, SHA-256 `bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5`. The 61-byte tail at `[0x12b,0x168)` is a 5-byte header (`01c3013008`) plus eight 7-byte selector/target/marker records. All eight selector bytes match the independently derived set; all record targets point at `JUMPDEST` (`0x5b`). At PC `0x0c`, `PUSH1 0x05; PUSH2 0x012b; PUSH1 0x1b; CODECOPY` copies the 5-byte header from code offset `0x12b` to memory offset `0x1b`; do not confuse that copy size with the complete 61-byte tail. REA returned 8 rows / 8 unique selectors, all `dispatch:"abi"`; Evidence ID `ev_bb59f5bcb7e3838dd9bc46b4588872c0b5a668de42e72f9a6bf944befcbb7b39`.
- **Observation — offsets and inference delta.** Noopt offsets are `PUSH4_pc + 12` and point at `CALLVALUE` (`0x34`); all eight codesize offsets collapse to 65 (`DUP1`, `0x80`) rather than per-selector table targets. The ABI says `view` for all eight while REA infers `payable` for all eight (0/8 mutability agreement). These offsets and mutability labels are analyzer output, not verified handler identity or runtime behavior.
- **Inference / scope.** The bytes encode two distinct dispatcher forms for this Vyper 0.4.3 K8 fixture: a noopt linear EQ/ISZERO chain and a codesize packed selector table. This bounds the r4 Unknown only to this source/compiler/options. Other Vyper versions, source shapes, optimizer settings, EVM targets and deployed contracts remain unknown. REA's `discovery_completeness` is `unknown`; no contract execution, chain/RPC query or deployment-authenticity check was performed. REA selectors, argument strings and mutability are upstream inferences.
```

## Scope and remaining gate

The seat wrote this report plus fresh evidence only under `.ufo/waves/arc3-loop1-round8/claims/c3/RV-3/`. No canonical corpus entry/token was landed, no other seat or tracked source was edited, and no post-landing Command A pass is claimed. Integrator: land the one draft + one map token, then run Command A on the actual landing revision and report the real count/map/missing/dangling result.
