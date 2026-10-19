# SC-2 — C3 corpus Unknown: Vyper optimizer dispatcher forms

## Verdict summary

- **REPRODUCED — selected Unknown:** the r4 Vyper entry still names non-default optimizer dispatcher forms as uncharacterized (`corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`). I freshly compiled its K8 source with the existing Vyper 0.4.3 binary, independently derived the selector set and bytecode structures, and ran REA 6.7.0 on the resulting gas, `--no-optimize`, and `-O codesize` carriers. On this fixture, noopt is an 8-leg `PUSH4/DUP2/EQ/ISZERO/PUSH2/JUMPI` chain; codesize has no opcode-boundary `PUSH4` and recovers the same selector set from a packed byte tail. The full corpus-entry draft is `claims/c3/SC-2/entry-draft.md`.
- **VERIFIED — independent selector and analyzer agreement:** eight ABI function signatures yielded eight distinct Keccak selectors; they match the compiler `method_identifiers` and each of the three REA result sets, 8/8 with missing `[]` and extra `[]` (`claims/c3/SC-2/evidence/rederive-output.txt:1-8,16-22,34-40,54-60`).
- **CORRECTED — offset rule is form-scoped:** the gas control's offsets are +11 from its selector PUSH4 and point to `PUSH1`; noopt offsets are +12 and point to `CALLVALUE`; all codesize offsets collapse to 65 (`DUP1`). Do not extend the gas-form offset convention to these variants (`evidence/rederive-output.txt:23-26,41-46,61-64`).
- **VERIFIED — Command A baseline:** at HEAD `904b724258fc9396a016bd9952b5cd40225fb7d8`, 86 knowledge files, 86 mapped, missing `[]`, dangling `[]`, 15/15 citation rules (`evidence/command-A-head.txt:1-7`).
- **UNVERIFIABLE — after-landing 87/87:** this seat did not and may not edit `corpus/knowledge/` or `corpus/README.md`. The draft is not a landed knowledge file or map token. Integration must add exactly one entry and one EVM-row token, then run Command A at the actual landing commit; no 87/87 result is claimed.

## Fresh first-hand measurements

The source was extracted from immutable HEAD into `/var/tmp`, not copied from another seat's values. `evidence/compile-receipt.txt` records the exact source/compiler identities and compile commands. Source SHA-256 is `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`; compiler is `0.4.3+commit.bff19ea2`, executable SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`. Repeated compiles of gas, noopt, and codesize each compared byte-identically; default gas and explicit `-O gas` also compared byte-identically.

| Fresh compile | Decoded runtime | Decoded SHA-256 | REA 6.7.0 Evidence ID |
|---|---:|---|---|
| default gas / `-O gas` control | 418 B | `72e5d886da7ccaf633b957738456323e22043275092e001fbc06847b57b06814` | `ev_fda90d5edf37c63add499f46475be10083d02a11bf1039d770f3b0e2b58cdab4` |
| `--no-optimize` | 617 B | `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc` | `ev_93e469a3888286e97751b6d0edce23f6aea6a3e40941cb52c01011d1e5ef0915` |
| `-O codesize` | 360 B | `bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5` | `ev_41eca23defd5329b8212a96be7529a7fbe0641bc8b6dd46c245f24d7fbecbc47` |

Probe envelopes retain input paths, full normalized results, provider and limitations at `claims/c3/SC-2/evidence/probe-{gas,noopt,codesize}-6.7.0.json`; exact CLI calls are in `evidence/probe-receipt.txt`. The analyzer is `evmole-interface` / `evmole@0.9.3`. Independent Keccak and opcode/table decoding are reproducible with `evidence/rederive.py`; exact output is `evidence/rederive-output.txt:1-69`.

## R7 draft reconciliation

The prior r7 C2 artifacts offered several competing Vyper corpus stems and one competing Evidence-ID Unknown; I used those drafts only to identify the open question and compare candidate scope. I chose EX-5's `2026-10-19-arc3-r7-vyper-optimizer-forms` stem as the one proposed entry/token. The reconciled draft uses that two-option scope, adds the fresh gas control, folds in CR-2's per-form offset/table detail and the peers' independent selector/bytecode cross-checks, and replaces prior-round IDs/results with the current evidence in this artifact. It excludes CR-1's `-O none` conclusion because this recheck did not separately invoke `-O none`.

Evidence reviewed for reconciliation: r7 `claims/c2/EX-4/evidence/draft-2026-10-19-arc3-r7-vyper-optimizer-dispatch-shapes.md:1-15`; `EX-5/draft-corpus-entry.md:1-31`; `CR-1/entry-draft.md:1-26`; `CR-2/evidence/entry-draft.md:1-18`; CN-2's motion accounting and K8 scope at `claims/verdicts/CN-2.md:25-44`. The fresh measurement, not any r7 number, is the evidence for the verdicts above.

## Write-scope and remaining work

In the repository, only this seat artifact directory was written: `claims/c3/SC-2.md`, `claims/c3/SC-2/entry-draft.md`, and its `evidence/` files; temporary builds and rerun scratch stayed under `/var/tmp`. No canonical corpus file, map, gate, `PROVINCE.md`, `SKILL.md`, `SCORECARD.md`, `LOG.md`, or other seat artifact was changed; no Git mutation was run. The pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` was left untouched.

Integration proposal in the draft: copy `entry-draft.md` to `corpus/knowledge/2026-10-19-arc3-r7-vyper-optimizer-forms.md`, append token `2026-10-19-arc3-r7-vyper-optimizer-forms` to the EVM map row (`corpus/README.md:38`), and re-run Command A at the landing revision. Until then, the C3 content is reproduced and drafted, but the required after-state remains pending.
