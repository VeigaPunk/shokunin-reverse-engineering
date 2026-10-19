# EX-5 — C1 Vyper London target probe

**Claim:** C1 coverage; selected the frozen candidate “a Vyper hardfork variant or `-O` form the r8 entry did not cover” (`claims-frozen.md:22-24`). I tested one explicit Vyper 0.4.3 EVM target, London, against an explicit Prague control using the same K8 source. The corpus entry is a draft only: `EX-5/evidence/entry-draft.md`.

## Re-derived

- Worktree `HEAD` is `5694506a862c32d2f7aac44935778bce4b6184f2`; the supplied work revision `eb5a2c4af9d910bb7a3d4fced780f4641e341a24` exists. I executed Command A against immutable Git objects at both revisions, following `SCORECARD.md:88-124`. Both returned `knowledge_files=88`, `mapped=88`, `missing=[]`, `dangling=[]`, `rule_blocks=15`, `citation_resolved_rules=15`; captured output is `EX-5/evidence/command-A-baseline.json:1` and `command-A-work.json:1`.
- Re-derived source identity: `.ufo/waves/arc3-loop1-round4/claims/c1/CR-1/vy/K8.vy` SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`. Compiler identity captured from the local Vyper package: `0.4.3+commit.bff19ea2`; Python 3.14.7, `/usr/bin/python3.14` SHA-256 `d78f9cf7178ecff09963551399855543c297f37ac207e626228bfe43cb26a70c`. Scratch/TMPDIR used `/var/tmp/kaidoku-ex5-r10.IQ52sM` only.
- Recompiled the source with `-O gas` for explicit `prague` and `london` targets. Each initial two-pass pair compared byte-identically (`EX-5/evidence/compile-determinism.txt:1-6`); a further compile recheck of each retained runtime also matched (`compile-recheck.txt:1-4`). Fresh ABI/method-identifiers agree; independently Keccak-derived IDs match all eight ABI function signatures. The selector set also matches all 8 raw and all 8 normalized REA rows for each target, and all eight opcode-boundary `PUSH4` values (`EX-5/evidence/measure.py`, `measurement.txt:1`).
- Target delta independently measured: Prague runtime 418 bytes, decoded SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`; London runtime 423 bytes, decoded SHA-256 `d1af44a952ac9775dd45eae83e2f4d167d311f9f7f3db8bf762592eb979060d2`. Prague prefix `5f3560e01c`; London `60003560e01c`. Both have 8 `PUSH4`/`DUP2 XOR` selector legs, one `MOD`, and one `CODECOPY`; the selectors are unchanged. REA offsets are all +2 in the London target.
- REA pin was queried locally: `6.7.0`; provider `evmole-interface`, `evmole@0.9.3`. Both envelopes say inferred, `discovery_completeness=unknown`, `runtime_execution=not-performed`, and bytecode hardfork unknown. In both, REA infers `payable` although the fresh compiler ABI says `view`; this is not a mutability verification.

## Per-item verdicts

- **VERIFIED — input/toolchain identity:** see `EX-5/evidence/compiler-identity.txt:1-10` and `EX-5/evidence/K8.vy:1-43`.
- **REPRODUCED — compiler determinism:** the initial two-pass compile pairs compare byte-identically (`EX-5/evidence/compile-determinism.txt:1-6`), and a further recompile of each retained output matches (`compile-recheck.txt:1-4`).
- **VERIFIED — selector recovery on these compiled bytes:** compiler method identifiers match independent Keccak; opcode-boundary `PUSH4` and both REA result sets match all eight selectors (`EX-5/evidence/measurement.txt:1`, `probe/{prague,london}.json:1`). This is a selector-only result, not a complete-interface or runtime claim.
- **VERIFIED — London target is byte-distinct while selector set is preserved:** settings, byte digests, prefixes, opcode counts, and offsets are in `EX-5/evidence/measurement.txt:1` and `compile/{prague,london}.{settings.json,opcodes.txt,runtime.hex}`.
- **VERIFIED — Command A pre-landing baseline:** at the supplied work revision, 88 knowledge files and 88 mapped with empty missing/dangling sets (`EX-5/evidence/command-A-work.json:1`).
- **UNVERIFIABLE — post-landing coverage count:** this seat is restricted to its own wave artifact directory; the corpus entry and map token are deliberately unlanded. An actual 89/89 Command A result requires the integrator to land both and rerun Command A at the resulting work commit.
- **UNVERIFIABLE — behavior/generalization:** no EVM execution or on-chain/deployment lookup was performed; no claim is made about other sources, targets, Vyper versions, or optimizer settings.

## Deliverables and boundary

- Draft corpus entry: `EX-5/evidence/entry-draft.md`; proposed destination `corpus/knowledge/2026-10-19-arc3-r10-vyper-london-hardfork.md`, proposed EVM-map token `2026-10-19-arc3-r10-vyper-london-hardfork`.
- Full compiler outputs and REA envelopes are under `EX-5/evidence/compile/` and `EX-5/evidence/probe/`; command recipe is `EX-5/evidence/reproduction.txt`.
- No corpus, map, gate, skill, custody path, or tracked source file was changed.