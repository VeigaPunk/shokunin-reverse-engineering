source: `.ufo/waves/arc3-loop1-round8/claims/c3/SC-1/evidence/` (`K8.vy`; fresh `gas`, `noopt` and `codesize` runtime hex, ABI, method-id and settings outputs; complete `rea-noopt.json` and `rea-codesize.json` envelopes; `rederive-output.txt`; `recheck-output.txt`). Rebuild and analysis scripts: `.ufo/waves/arc3-loop1-round8/claims/c3/SC-1/reproduce.sh` and `rederive.py`. The source was extracted from work commit `7deeb36045209f3fbeb4460edd7aef5b5270af22` and rehashed before compiling.
verified-at: 2026-10-19
recheck: `bash .ufo/waves/arc3-loop1-round8/claims/c3/SC-1/reproduce.sh` → expects source SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`, Vyper `0.4.3+commit.bff19ea2`, and fresh `--no-optimize` / `-O codesize` runtimes of 617 B / `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc` and 360 B / `bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5`; it invokes `rea-agents@6.7.0 inspect-evm-interface` on each, then independently checks the compiler method identifiers, Keccak selectors, REA raw/normalized results and byte-level shapes. Temporary files and REA `TMPDIR` are under `/var/tmp`, never `/tmp`. Per-invocation Evidence IDs may change with the temporary input path; compare decoded bytecode SHA-256 and the returned selector payload, not IDs.

# Vyper 0.4.3 K8 alternate optimizer forms — linear EQ chain and packed selector table (8/8)

This entry closes only the byte-characterization Unknown named in `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28` for this synthesized K8 fixture, Vyper 0.4.3, and the two settings below. It does not claim coverage of every Vyper mode or contract.

## Fixture and compiled artifacts

The fixture is the eight-function `K8.vy` carrier (`f0`–`f7`, each one `uint256` argument and return; ABI mutability `view`). Its SHA-256 is `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`. The existing local compiler executable is `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper`, Vyper `0.4.3+commit.bff19ea2`, executable SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`. No compiler was installed or changed for this check.

Fresh output from the pinned source and compiler:

- Default `optimize: gas` control: runtime 418 B, decoded-byte SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`.
- `--no-optimize` (`optimize: none`): runtime 617 B, decoded-byte SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`.
- `-O codesize` (`optimize: codesize`): runtime 360 B, decoded-byte SHA-256 `bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5`.

The independent Keccak-256 derivation, fresh Vyper `method_identifiers`, and fresh ABI each yield eight selectors: `f0(uint256)=2ae1431c`, `f1(uint256)=9adbf691`, `f2(uint256)=bf3724af`, `f3(uint256)=d7b7913b`, `f4(uint256)=d7531d91`, `f5(uint256)=cf35f823`, `f6(uint256)=9b7c2962`, `f7(uint256)=364605a1` (`evidence/rederive-output.txt:1-6`).

## Observations — bytecode and REA output

For `--no-optimize`, the direct opcode-boundary walk finds eight `PUSH4 <selector>; DUP2; EQ; ISZERO; PUSH2; JUMPI` compare legs, one for each derived selector. The leg PCs are `19, 92, 165, 238, 311, 384, 457, 530`. REA reports offsets `31, 104, 177, 250, 323, 396, 469, 542`; each equals its selector's `PUSH4` PC + 12 and points at `CALLVALUE` (`0x34`), not a distinct `JUMPDEST` (`evidence/rederive-output.txt:9-11`).

For `-O codesize`, the executable prefix has no opcode-boundary `PUSH4`, one `EQ`, one `MOD`, and two `CODECOPY` instructions at PCs 12 and 45. The final 61 bytes begin at code offset `0x12b`: a five-byte header `01c3013008` followed by eight seven-byte records (`selector[4] || target[2] || marker[1]`). The recorded selector-to-target pairs are `d7b7913b→0x00a6`, `9adbf691→0x0074`, `2ae1431c→0x005b`, `9b7c2962→0x00f1`, `cf35f823→0x00d8`, `364605a1→0x010a`, `bf3724af→0x008d`, and `d7531d91→0x00bf`. Every record marker is `0x25`; every target byte is `JUMPDEST` (`0x5b`). The prefix at PCs 5–12 is `PUSH1 0x05; PUSH2 0x012b; PUSH1 0x1b; CODECOPY`; the record table is 61 bytes, not merely the first copied/header slice (`evidence/rederive-output.txt:15-19`). REA reports bytecode offset 65 (`DUP1`, `0x80`) for all eight functions; that shared offset is not a per-selector table target.

Fresh `rea-agents@6.7.0 inspect-evm-interface` calls through `evmole-interface` (`evmole@0.9.3`) returned 8 raw and 8 normalized functions for each runtime, with the independently derived selector set, `dispatch: "abi"` for all, and decoded-byte SHA-256 matching the freshly compiled runtime. Recorded Evidence IDs are `ev_3f69b0f5c4cbd0ad6c46ac46cebdc70856a40085cedc7fedd1ca6ff48905d7b1` (`--no-optimize`) and `ev_16a332913c9aef774e137825b708c6b2b74f3efe662acc2746afefc599d5c864` (`-O codesize`); full envelopes are retained alongside the carrier bytes. Both envelopes say `confidence: inferred`, `authority: shipped-artifact`, and `discovery_completeness: unknown`. The carrier is a synthesized fixture, not an identified deployed or shipped contract.

## Observation, inference and residual Unknowns

**Observation:** These two settings produce different byte-level dispatch representations on this exact K8 source: a per-selector `PUSH4`/`EQ` chain under `--no-optimize`, and a compact table suffix with no opcode-boundary selector `PUSH4` under `-O codesize`. The REA calls recover the compiler-derived selectors for both. The byte-level and REA offset results are recorded separately; offsets are not treated as execution evidence.

**Inference:** On this one source/compiler pair, the extractor recognizes both forms and returns the complete eight-selector set derivable from the compiler ABI/method identifiers. REA's `inferred_state_mutability` says `payable` for all eight in both modes, while the fresh compiler ABI says `view` for all eight (0/8 agreement); these are upstream inferences, not verified mutability or contract behavior (`evidence/rederive-output.txt:7-14`).

**Unknown / limitations:** `discovery_completeness` is `unknown`; 8/8 is agreement with the compiler-derived fixture set, not proof that all possible callable dispatch is covered. The check did not execute a contract, query a chain/RPC, establish deployment identity, or test another Vyper release, K value, source shape, EVM target, or runtime. `-O none` was not compiled in this recheck and remains outside the closure, despite a conflicting R7 draft assertion; only the literal `--no-optimize` and `-O codesize` settings are in scope. Other optimizer forms and dispatcher offset conventions remain unknown.
