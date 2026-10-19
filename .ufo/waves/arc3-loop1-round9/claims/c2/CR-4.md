# CR-4 — C2 coverage: Vyper optimizer-flag boundary

## Selection and verdict

Selected the frozen C2 candidate: whether Vyper `--no-optimize` and `-O none` leave any residual byte-level distinction on the r8 K8 fixture. **REPRODUCED:** for the exact K8 source and Vyper 0.4.3 named below, freshly compiled runtime bytes, ABI, method identifiers, compiler settings, and the two REA function payloads are identical. The corpus-entry draft is `claims/c2/CR-4/evidence/entry-draft.md`; proposed knowledge path and map token are named at its top. No corpus or map file was edited.

## First-hand evidence

- Source: `.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy`; SHA-256 re-derived as `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`, matching the copy in this seat's evidence.
- Compiler: Vyper `0.4.3+commit.bff19ea2`; CLI launcher SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10` (`evidence/identity.txt`). Two fresh runtime compilations per flag spelling compared byte-identically; cross-flag `cmp` succeeded for runtime hex, ABI, method identifiers, and settings (`evidence/rederive.sh`, `evidence/reproduction.txt`).
- Both decoded runtimes: 617 bytes, SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`. Each ABI and method-identifiers output contains 8 entries; settings are `{"experimental_codegen":false,"optimize":"none"}` (`evidence/measure.txt`).
- `rea-agents@6.7.0` probes returned 8 raw and normalized rows apiece through `evmole-interface` / `evmole@0.9.3`; both decoded hashes match the fresh runtime, selector sets match the 8 compiler method identifiers, and both raw and normalized function payloads compare equal. Evidence IDs: `ev_d5150418480de1c0dc0eb1259378c51a65e8ce1468e98998826cd30fbbb6b8d1` (`--no-optimize`) and `ev_ea1168eee4711b5bc705ef0808a0b744ee7f949295137bd6636898b7522a20c3` (`-O none`). REA reports `confidence=inferred`, `authority=shipped-artifact`, `runtime_execution=not-performed`; this is not execution evidence. Full envelopes are in `evidence/probe/`.

All measurements above come from this seat's compiler calls and REA envelopes; r8 material was used to identify the fixture and the named boundary, not as a source for the reported measurements. Scratch/TMPDIR were placed under `/var/tmp`.

## Command A and landing state

**VERIFIED baseline:** Command A (`SCORECARD.md:88-124`) at source HEAD `947091d6b6f52684faf9ca53adf94ff8a0f6b006` returned `{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15}`; captured in `evidence/command-a-before.txt`.

**UNVERIFIABLE post-integration count:** this seat is required to leave the corpus and `corpus/README.md` untouched. The expected 87→88, mapped 88, missing `[]`, dangling `[]` must be measured by the integrator after landing both the draft entry and its proposed EVM map token.
