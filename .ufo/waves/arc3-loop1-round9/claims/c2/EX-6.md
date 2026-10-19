# EX-6 — C2: viaIR fallback dispatcher

## Finding

**REPRODUCED (bounded closure).** A new solc 0.8.37 viaIR carrier with payable `fallback()` and `receive()` compiled twice byte-identically. `inspect-evm-interface` returned exactly the compiler ABI's three ordinary function selectors. The final `SUB` selector mismatch branches to the compiled fallback path; a matching final selector falls through to its function body. This closes the named r6 fallback-interaction Unknown for this fixture and settings only.

## First-hand evidence

- Fresh source: `evidence/ViaIRFallback.sol`; SHA-256 `615edcdecab9a6b3b4d9b6965c416406f133d43b1144eb2e13985bf17580f11a`.
- Compiler: existing lane prefix, solc-js `0.8.37+commit.f401782d.Emscripten.clang` (`soljson.js` SHA-256 `221d7a667378b5068d913e75fe092507e061363cd1d23b64c49ae82febabad4c`); Node `v26.12.0`. Standard JSON input enables `viaIR` and optimizer runs 200. No install or compiler modification.
- Two independent compilation invocations in `evidence/out-a/` and `evidence/out-b/` match: 366-byte runtime SHA-256 `2948d578ae460119f777eb379febc2738dbec14d03c76d5f100777c9552ce6fc`; 392-byte creation SHA-256 `a24cb1651e78dd159425d5b27c9ba513b50b0401f5bcf3589f259b0a70d0ba9e`. Exact stdout in `compile-a.txt` / `compile-b.txt`, byte comparison in `compile-compare.txt`.
- Compiler ABI has three functions (`alpha()` / `db1d0fd5`, `load()` / `86d5c4be`, `store(uint256)` / `6057361d`) plus `fallback` and `receive`. `method-identifiers.json` independently binds the three selector strings.
- REA CLI `rea-agents@6.7.0`, provider `evmole@0.9.3`: exit 0, Evidence ID `ev_5272b1d8547672b56597c8aaccc6cf675675d128ace33cb3e590545feae1bddd`, 3 returned selectors matching the compiler set, decoded runtime SHA equal to the fresh compile (`evidence/probe.json`). Carrier text SHA is `4736cecce7f1977a80f9401bcce111bf2b78b65e9f1f31397b2327dff0d3488f` (733 B); decoded bytes are 366 B. REA reports `discovery_completeness=unknown`, `runtime_execution=not-performed`, and inferred evidence; this is not a completeness or execution claim.
- Byte-level finding from the independent opcode walk (`evidence/walk.txt`): the three dispatch selector immediates are at PCs `0x99`, `0xa4`, `0xae`; final `PUSH4 0xdb1d0fd5; SUB; PUSH2 0x000e; JUMPI` routes mismatch to the common fallback path. Empty calldata branches to receive at `0x0087`; nonempty unknown calldata continues to fallback. A match falls through at `0x00b8` (decimal 184), matching REA's reported `alpha()` offset. This is static control-flow inference only. The walk excludes the 51-byte CBOR metadata trailer (code prefix 313 B, which matches REA's decoded `bytecodeOffset=313`, `cborLength=51`); its five opcode-boundary PUSH4 sites include two panic-data constants as well as the three dispatch selectors. REA also inferred `alpha()` as `view`, while the fresh compiler ABI says `pure`; selector recovery matches, mutability remains an upstream inference.
- A third compile into `/var/tmp` reproduced both runtime and creation bytes; the independent opcode walk also compared identical. A second REA probe on that recompile returned the same three-selector set and decoded runtime digest (`evidence/verification.txt`). The two REA evidence IDs are not compared because the carrier paths differ.

## Corpus draft and coverage

Full proposed entry and map token are in `evidence/corpus-draft.md`:

- destination: `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-dispatch.md`
- EVM row token: `2026-10-19-arc3-r9-viair-fallback-dispatch`
- no tracked corpus or map file was edited.

Command A against frozen HEAD `947091d6b6f52684faf9ca53adf94ff8a0f6b006` returned `knowledge_files=87`, `mapped=87`, `missing=[]`, `dangling=[]`, `citation_resolved_rules=15`, `rule_blocks=15`, `coverage_score=10.0`, `depth_score=10.0` (`evidence/command-A-before.json`). The required post-landing 88/88 result remains for the integrator after both draft and map token are landed.

## Reproduction

From the lane root, compile to a new output directory inside `/var/tmp`, then probe with the local REA CLI and `TMPDIR=/var/tmp/kaidoku-r9-ex6`. Full original outputs are in `evidence/`; the compiler accepts the source and output directory as arguments. The worktree had unrelated pre-existing modifications at start; this seat changed only its own round-9 artifact directory.
