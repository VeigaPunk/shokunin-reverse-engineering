# EX-8 — C3 corpus Unknown: Vyper optimizer dispatch forms

## Finding

**Chosen Unknown:** Vyper's `--no-optimize` and `-O codesize` dispatcher forms left open in `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`.

**Bounded evidence verdict: VERIFIED.** Fresh builds from the retained synthetic K8 source and fresh REA calls reproduce two distinct non-default dispatch encodings and the same compiler-derived selector set. This establishes only these source bytes with Vyper 0.4.3; it does not establish arbitrary Vyper forms or deployed behavior.

**Corpus landing: pending integration.** This seat produced a copy-ready entry draft and map token but did not edit `corpus/knowledge/` or `corpus/README.md`, per the write fence. The post-landing coverage count is therefore **UNVERIFIABLE** here.

## First-hand re-derivation

- Source and tool identity were freshly measured: the copied K8 source matches the source SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`; Vyper reports `0.4.3+commit.bff19ea2`, and its executable SHA-256 is `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10` (`claims/c3/EX-8/evidence/identity.txt:1-7`).
- `rederive.sh` compiled each setting's runtime twice in scratch under `/var/tmp`; all same-setting `cmp` checks passed. Explicit `-O gas` equals the default build, and explicit `-O none` equals `--no-optimize` byte-for-byte (`evidence/reproduction.txt:4-10`; hashes for retained outputs are also in `evidence/measure.txt:5-6,13-14,21-22`). Effective settings are recorded in `evidence/compile/{noopt,none,codesize}.settings.json`.
- `measure.py` independently Keccak-hashed the freshly emitted ABI signatures and matched the compiler `method_identifiers`: its exact output lists the signatures and identical 8-selector sets (`evidence/measure.txt:1-4`). Real `rea-agents@6.7.0` calls against the three retained gas/no-optimize/codesize runtimes each returned matching raw and normalized selector sets, with the decoded-bytecode digest equal to the fresh compile (`evidence/measure.txt:7-9,15-17,23-25`; full envelopes in `evidence/probe/`).
- The no-optimize byte walk found the linear `PUSH4; DUP2; EQ; ISZERO; PUSH2; JUMPI` chain. Its reported offsets are each `PUSH4` PC + 12 and land on `CALLVALUE` (`evidence/measure.txt:14,30,32-34`).
- The codesize byte walk found no opcode-boundary `PUSH4`, with one `EQ`, one `MOD`, and two `CODECOPY` instructions. The runtime tail at `0x12b` is 61 bytes: header `01c3013008` followed by eight selector/target/`0x25` records; every target is a `JUMPDEST`. REA reports the same offset 65 (`DUP1`) for every selector, not the record targets (`evidence/measure.txt:21-22,31,35-38`).
- The probe's mutability is explicitly an inference: the fresh compiler ABI says `view`, while REA infers `payable` on each measured form (0/8 agreement; `evidence/measure.txt:18-20,26-28`). The raw envelopes also say `confidence=inferred`, `authority=shipped-artifact`, `discovery_completeness=unknown`, and `runtime_execution=not-performed` (`evidence/probe/{gas,noopt,codesize}.json`).

The fresh Command A before measurement ran the exact `SCORECARD.md:88-124` recipe at both HEAD `904b724258fc9396a016bd9952b5cd40225fb7d8` and the frozen work object `7deeb36045209f3fbeb4460edd7aef5b5270af22`. Both returned `knowledge_files:86`, `mapped:86`, `missing:[]`, `dangling:[]`, and `citation_resolved_rules:15` (`evidence/command-a-before.txt:1-19`). No after-landing result is claimed.

## R7 draft reconciliation

The R7 Vyper drafts are alternative copies of the same K8 optimizer-form investigation, not four separate corpus Unknowns: EX-4's draft (`.ufo/waves/arc3-loop1-round7/claims/c2/EX-4/evidence/draft-2026-10-19-arc3-r7-vyper-optimizer-dispatch-shapes.md`), EX-5's (`.ufo/waves/arc3-loop1-round7/claims/c2/EX-5/draft-corpus-entry.md`), CR-1's (`.ufo/waves/arc3-loop1-round7/claims/c2/CR-1/entry-draft.md`), and CR-2's (`.ufo/waves/arc3-loop1-round7/claims/c2/CR-2/evidence/entry-draft.md`). Their proposed entry names differ. EX-8 chose one R8 destination/token and rebuilt the evidence rather than importing prior numeric results or IDs.

The drafts differ on whether explicit `-O none` was separately compiled. EX-8 freshly invoked both `--no-optimize` and `-O none`; the retained outputs compare byte-identically, and both report `optimize:none`. Thus this fixture supports that equality; it does not establish behavior for other source/compiler combinations. The different R7 REA versions and invocation IDs are not merged as identity evidence; this artifact's three probes all use 6.7.0 and retain their own raw envelopes.

## Per-item verdicts

- Named Vyper optimizer-form Unknown, limited to K8 / Vyper 0.4.3 / the two named options: **VERIFIED**.
- Fresh output identities and byte-level forms: **REPRODUCED** by `evidence/rederive.sh` and `evidence/measure.txt`.
- Explicit `-O none` versus `--no-optimize` for this fixture: **CORRECTED / VERIFIED** by the fresh compile-and-compare; the two outputs are byte-identical.
- Command A before: **VERIFIED**, 86 files / 86 mapped, no missing or dangling tokens at the recorded revision.
- Command A after landing the entry plus map token: **UNVERIFIABLE** until the integrator lands both and runs Command A at that revision; the expected 87/87 is not reported as measured.
- Other Vyper source shapes, selector counts, releases, optimizer/EVM settings, deployment identity, and runtime execution: **UNVERIFIABLE / remain Unknown**.

## Draft deliverable and boundary

Copy-ready corpus entry: `claims/c3/EX-8/entry-draft.md`. Proposed destination and EVM coverage-map token: `2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes`. Recheck command: `bash .ufo/waves/arc3-loop1-round8/claims/c3/EX-8/rederive.sh` from the repository root. All persistent source, commands, compiled evidence, probe envelopes, and measurements are under this seat's artifact directory; scratch was under `/var/tmp`, not `/tmp`. No corpus, README, SKILL, PROVINCE, SCORECARD, LOG, gate source, or peer seat artifact was changed.
