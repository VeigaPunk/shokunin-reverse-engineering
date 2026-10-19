# EX-7 — C2 seat artifact

**Per-item verdicts**

- **REPRODUCED:** On the exact K8 source and Vyper executable identified below, `--no-optimize` and `-O none` produced byte-identical runtime hex, ABI, method identifiers, and compiler settings. Two separate runtime compilations per flag spelling also matched.
- **UNVERIFIABLE beyond this scope:** This does not establish equivalence for other Vyper releases, source shapes, or compiler output formats not measured here. It does not close the wider offset-generalization Unknown.
- **UNVERIFIABLE until integration:** The post-landing Command A gate was not run because the corpus and map are explicitly draft-only. The baseline and exact-token projection are recorded below.

## Draft corpus entry

<!-- DRAFT for parent integration only. Proposed destination: corpus/knowledge/2026-10-19-arc3-r9-vyper-noopt-alias-equivalence.md. Proposed EVM-map token: 2026-10-19-arc3-r9-vyper-noopt-alias-equivalence. No corpus or index edit was made by this seat. -->

# Vyper 0.4.3 K8 `--no-optimize` and `-O none` are byte-identical on the pinned source

source: `.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/evidence/K8.vy` (SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`); fresh copy `/var/tmp/kaidoku-ex7-r9.j7kZMW/K8.vy` has the same SHA-256. Compiler `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper`, SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`, version `0.4.3+commit.bff19ea2`.

verified-at: 2026-10-19

The named optimizer-form Unknown is in `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`. This entry answers only the narrow residual question: whether these two flag spellings leave a byte-level distinction for this exact K8 source on this exact compiler build. No prior-round measurement is used as evidence here; the source was freshly compiled and compared in `/var/tmp/kaidoku-ex7-r9.j7kZMW/` with `TMPDIR=/var/tmp/kaidoku-ex7-r9.j7kZMW/tmp`.

- **Observation — fresh compile and byte-level comparison.** The runtime was independently compiled twice under each of `--no-optimize`, `-O none`, and default gas optimization. Each same-mode pair passed `cmp`. The `--no-optimize` and `-O none` outputs passed `cmp` for `bytecode_runtime`, `abi`, `method_identifiers`, and `settings`; their file SHA-256 values are respectively `1dfe2699e61e8d82570dc3272d9679880e5a2fa765a0e4ce9169331ecedd939c`, `026745a7e293ff3aa32a3c4f6fd33973c5a143b637782776e6b497e96952e0d3`, `3b50906530daa351f192ed05c321c2e239d45fbd2b86a2765ac33568b9fda8ea`, and `547d3edca5c61dde1f0cea725eee658497c916c908c9b7e66c178e56bee54332`. Both settings outputs are exactly `{"optimize": "none", "experimental_codegen": false}`. Decoding either runtime gives 617 bytes, SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`; the hex carrier text is 1,237 bytes. As a distinct optimizer control, the default-gas runtime is 418 bytes, decoded SHA-256 `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814`, and is not byte-identical to the no-optimize output.
- **Observation — REA corroboration.** Fresh `rea-agents@6.7.0` `inspect-evm-interface` calls used provider `evmole-interface` / `evmole@0.9.3`, `hex` input, and `--format json`. The no-optimize result is `/var/tmp/kaidoku-ex7-r9.j7kZMW/out/noopt.rea.json`, Evidence ID `ev_c4a54993852c439300b51f9d1ef32b392bf99e19552013d35a1ecf382e4e7356`; the `-O none` result is `/var/tmp/kaidoku-ex7-r9.j7kZMW/out/none.rea.json`, Evidence ID `ev_8d9ac395050aa84f9d94cf2e5cd5b134e5d2a18e60e9722f84f0a0123168277a`. Both envelopes report `confidence=inferred`, `authority=shipped-artifact`, decoded bytecode `617` bytes / SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`, and eight rows with `dispatch="abi"`. The normalized function rows compare equal. Selectors are `2ae1431c, 364605a1, 9adbf691, 9b7c2962, bf3724af, cf35f823, d7531d91, d7b7913b`; both REA selector sets equal the freshly compiled method-identifier values after removing the `0x` prefix. Selector/offset pairs in both fresh envelopes are `(2ae1431c,31), (364605a1,542), (9adbf691,104), (9b7c2962,469), (bf3724af,177), (cf35f823,396), (d7531d91,323), (d7b7913b,250)`. The IDs are per-call references; byte equality is established by the compile-output `cmp` checks and decoded SHA-256, not by comparing Evidence IDs.
- **Reproduction commands.** The actual runtime compile invocations were `env TMPDIR=/var/tmp/kaidoku-ex7-r9.j7kZMW/tmp /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper --no-optimize -f bytecode_runtime /var/tmp/kaidoku-ex7-r9.j7kZMW/K8.vy` and the same command with `-O none` in place of `--no-optimize`; each was run twice to separate `.runtime.1.hex` and `.runtime.2.hex` files and the pairs compared with `cmp`. Other formats were compiled with the same flag forms and `-f abi`, `-f method_identifiers`, and `-f settings`. REA calls were `env TMPDIR=/var/tmp/kaidoku-ex7-r9.j7kZMW/tmp npx -y rea-agents@6.7.0 inspect-evm-interface /var/tmp/kaidoku-ex7-r9.j7kZMW/out/noopt.runtime.hex hex --format json` and the corresponding `none.runtime.hex` call. The compiler version command returned `0.4.3+commit.bff19ea2`; REA `--version` returned `6.7.0`.
- **Scope and limitations.** The measurement is for one synthetic 8-function source and one compiler executable/version. It supports no universal equivalence claim for other Vyper source forms or versions. REA selector/argument/mutability fields are inferred; no target execution, deployment identity, chain lookup, or network activity was performed. In particular, this result does not prove the broader non-default-optimizer offset rule for other carriers.

## Seat-only Command A staging check (not part of the corpus entry)

Command A from `SCORECARD.md:88-124`, run against immutable revision `947091d6b6f52684faf9ca53adf94ff8a0f6b006`, returned:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 87, "mapped": 87, "missing": [], "revision": "947091d6b6f52684faf9ca53adf94ff8a0f6b006", "rule_blocks": 15}
```

A separate in-memory projection verified the proposed filename stem and map token are both absent at that revision; adding exactly that filename and token yields `knowledge_files=88`, `mapped=88`, `missing=[]`, `dangling=[]`. This is a projection, not a post-landing Command A result. The parent must land the draft and EVM-row token, then run Command A against the landing revision.
