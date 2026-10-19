# EX-7 — C3 coverage: Vyper optimizer dispatcher forms

## Selection and verdicts

Selected the still-open Vyper 0.4.3 K8 optimizer-form Unknown named in `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`, limited to `--no-optimize` and `-O codesize`. **Evidence verdict: REPRODUCED within that bound.** The delivered corpus entry is a draft only; no corpus or map edit was authorized for this seat.

- `--no-optimize` runtime characterization and selector recovery: **REPRODUCED**. Fresh Vyper compile, full byte walk, independent ABI Keccak cross-check, and fresh REA 6.7.0 probe agree; see `EX-7/evidence/characterize-final.txt:7-13` and `EX-7/evidence/verify-final.txt:4`.
- `-O codesize` runtime characterization and selector recovery: **REPRODUCED**. The packed tail contains the same eight selectors and targets eight JUMPDESTs; see `EX-7/evidence/characterize-final.txt:14-21` and `EX-7/evidence/verify-final.txt:5`.
- R7 draft discrepancy on the codesize tail: **CORRECTED interpretation**. EX-4's 27-byte sequence (`.ufo/waves/arc3-loop1-round7/claims/c2/EX-4/evidence/draft-2026-10-19-arc3-r7-vyper-optimizer-dispatch-shapes.md:10`) is an exact prefix, not the whole tail. My byte walk computes the compared sequence as 27 bytes and confirms `matches_tail_prefix=True`; the full runtime tail from `0x12b` is 61 bytes with eight records (`EX-7/evidence/characterize-final.txt:17-22`). EX-5 and CR-2's full-tail accounting is consistent with this measurement (`.ufo/waves/arc3-loop1-round7/claims/c2/EX-5/draft-corpus-entry.md:26`; `.ufo/waves/arc3-loop1-round7/claims/c2/CR-2/evidence/entry-draft.md:15`).
- Explicit `-O none` compile: **UNVERIFIABLE / not measured separately**. The fresh `--no-optimize -f settings` output says `optimize: none`, but that is not a separate `-O none` compile; the draft does not claim equivalence for that invocation.
- Command A current baseline: **VERIFIED** at HEAD `904b724258fc9396a016bd9952b5cd40225fb7d8`: `knowledge_files=86`, `mapped=86`, `missing=[]`, `dangling=[]`, `citation_resolved_rules=15`, `rule_blocks=15` (`EX-7/evidence/command-A-before.json:1`). The new entry plus one EVM map token should make 87/87, but **post-landing 87/87 is UNVERIFIABLE in this seat** because C3 requires a draft and the write fence forbids editing `corpus/` and `corpus/README.md`.

## First-hand re-derivation

`git rev-parse HEAD` returned `904b724258fc9396a016bd9952b5cd40225fb7d8`. Command A was rerun against this immutable revision using the recipe at `SCORECARD.md:88-124`; exact JSON is retained at `EX-7/evidence/command-A-before.json:1`.

The copied synthetic source `K8.vy` hashes to `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`. The compiler binary remeasured at `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper` hashes to `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10` and reports `0.4.3+commit.bff19ea2`. I compiled `-O gas`, `--no-optimize`, and `-O codesize` on scratch under `/var/tmp/kaidoku-arc3-r8-ex7-vyper/`; each runtime was compiled twice and compared byte-identical. Exact commands and identities: `EX-7/evidence/rebuild-receipt.txt`; retained ABI, method identifiers, settings, opcodes, and hex runtimes: `EX-7/evidence/compiler/`.

Fresh `npx -y rea-agents@6.7.0 inspect-evm-interface <runtime> hex --format json` runs returned the same eight compiler/Keccak-cross-checked selectors on each form, all `dispatch:"abi"`; decoded runtime SHA-256 and byte count match the compiled inputs. Evidence IDs and first-hand checks are in `EX-7/evidence/verify-final.txt:1-5`; full envelopes are in `EX-7/evidence/probe/{gas,noopt,codesize}-6.7.0.json`. The provider is `evmole-interface` / `evmole@0.9.3`.

## R7 draft reconciliation and landing proposal

I compared the R7 Vyper proposals from EX-4, EX-5, CR-1, and CR-2 rather than importing their numeric results. My fresh rebuild confirms the common core: eight selectors; the no-opt `PUSH4/DUP2/EQ/ISZERO/PUSH2/JUMPI` chain; the codesize form's embedded table; and distinct, form-specific REA offsets. The apparent 27-versus-61 disagreement is resolved by the byte-prefix comparison above. CR-1's proposal includes a separate `-O none` equivalence that I did not test; the selected draft deliberately leaves it unknown. The present coverage map has no R7 Vyper token (Grep of `corpus/README.md` returned no R7 Vyper match; no `2026-10-19-arc3-r7-vyper*.md` exists under `corpus/knowledge/`).

Draft entry: `EX-7/evidence/entry-draft.md`. Proposed new knowledge filename and sole map token: `2026-10-19-arc3-r8-vyper-optimizer-forms`; append that token once to the EVM row at `corpus/README.md:38` when integration scope permits. Run Command A on the actual landing revision; until then, report only the verified 86/86 baseline, not a projected after-result.

## Scope and custody

The K8 carrier is synthetic, not a deployed or shipped contract. REA marks the result inferred, `discovery_completeness:"unknown"`, and `runtime_execution:"not-performed"`; no runtime behavior, deployment identity, chain lookup, or other Vyper version/source/optimizer setting is claimed. Compiler and REA scratch plus TMPDIR were under `/var/tmp`; the corpus, map, gate source, PROVINCE, SKILL, SCORECARD, LOG, and custody paths were not edited. The pre-existing worktree modification `.ufo/waves/arc2-loop1-round10/C3.md` was left untouched.
