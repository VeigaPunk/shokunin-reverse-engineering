# CR-1 — C1 coverage draft

Assigned chain: C1; frozen roster maps `CR-1` to `c1` (`.ufo/waves/arc3-loop1-round10/claims-frozen.md:69-70`). This artifact provides a draft corpus entry and first-hand evidence for one narrow Vyper hardfork Unknown. The seat report is `.ufo/waves/arc3-loop1-round10/claims/c1/CR-1.md`; the draft and experiment outputs are confined to `.ufo/waves/arc3-loop1-round10/claims/c1/CR-1/`. No corpus, README, gate, custody path, or tracked source file was edited; no Git index/ref mutation was performed.

## Re-derived result

The selected item is frozen claim candidate (c), a Vyper hardfork variant (`claims-frozen.md:22-24`); the corpus boundary is the r8 entry's explicit limitation that EVM targets are not established (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:15`). I copied the K8 source from `.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/evidence/K8.vy` to this seat's evidence directory and re-hashed it. I compiled it from scratch twice each for Paris and Prague with the already-installed Vyper 0.4.3, then independently compared ABI/method IDs, Keccak-derived selectors, raw runtime bytes, opcode-boundary dispatch legs, and REA results. No prior-round measurement value is used as evidence; see `CR-1/evidence/rederive.sh` and its captured output files.

- Same-source, same-compiler builds with the emitted `optimize: gas` setting were byte-identical across five output forms for both forks: `CR-1/evidence/reproduction.txt:13`.
- Paris and Prague each yielded 8/8 ABI functions = 8/8 compiler method IDs = 8/8 independently Keccak-derived selectors = 8/8 REA rows; exact selector set, runtime identities, REA Evidence IDs, and byte-walk output: `CR-1/evidence/measurement.txt:1-28`.
- Paris prefix: `PUSH1 0x00 CALLDATALOAD PUSH1 0xe0 SHR`; Prague: `PUSH0 CALLDATALOAD PUSH1 0xe0 SHR`. Both byte-walks find the `MOD` table prefix and eight `PUSH4,DUP2,XOR,PUSH2,JUMPI` legs. REA's eight offsets each equal the corresponding selector `PUSH4` PC + 11 and land at `PUSH1` (`measurement.txt:9-12,22-25`).
- Tool limitation measured on both carriers: compiled ABI says `view` ×8 while REA infers `payable` ×8; this is recorded as an inference delta, not contract behavior (`measurement.txt:13,26`; full envelopes in `CR-1/evidence/probe/`).
- Current Command A at `HEAD` (resolved to `5694506a862c32d2f7aac44935778bce4b6184f2`; `CR-1/evidence/git-head.txt:1`) was freshly run from the recipe at `SCORECARD.md:88-124`: `knowledge_files=88`, `mapped=88`, `missing=[]`, `dangling=[]`, `rule_blocks=15`, `citation_resolved_rules=15`, coverage/depth `10.0/10.0` (`CR-1/evidence/command-A-head.json:1`). Since this seat is permitted to deliver only a draft, the post-integration `89/89` is **UNVERIFIABLE here**; it must be re-measured after the parent integrates both the draft and map token.

## Per-item verdicts

- **Chain assignment — VERIFIED:** frozen claims roster `claims-frozen.md:69-70` assigns CR-1 to C1.
- **Unknown provenance — VERIFIED:** frozen candidate (c) is a Vyper hardfork variant (`claims-frozen.md:22-24`), and the prior r8 Vyper entry explicitly leaves EVM targets unestablished (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:15`).
- **Paris/Prague bytecode comparison — REPRODUCED:** compiler identity, two settings, five-form duplicate-build comparisons, runtime byte counts/digests and decoder outputs are in `CR-1/evidence/reproduction.txt:3-14` and `CR-1/evidence/measurement.txt:1-28`.
- **Selector recovery — REPRODUCED:** K/K for each fork, including independent Keccak and compiled method-ID agreement, in `measurement.txt:5-8,18-21,27`; retained raw REA Evidence is in `CR-1/evidence/probe/paris.rea.json:1` and `prague.rea.json:1`.
- **Command A current baseline — REPRODUCED:** output at `CR-1/evidence/command-A-head.json:1`.
- **Expected mapped count after integration — UNVERIFIABLE:** no corpus or map edits were authorized for this seat. The draft proposes one knowledge entry and one EVM-map token; do not report 89/89 until Command A is run after those edits land.

## Draft and integration boundary

Draft entry: `CR-1/draft-corpus-entry.md`. Proposed destination: `corpus/knowledge/2026-10-19-arc3-r10-vyper-hardfork-dispatch.md`. Proposed EVM coverage-map token: `2026-10-19-arc3-r10-vyper-hardfork-dispatch`. The entry closes only the exact Paris-versus-Prague comparison on this fixture; it does not claim that all Vyper hardfork/compiler combinations are characterized.

Recheck from the lane root:

```bash
bash .ufo/waves/arc3-loop1-round10/claims/c1/CR-1/evidence/rederive.sh
```

The script uses only `/var/tmp` for scratch and `TMPDIR`, removes the scratch tree on exit, compiles the local source copy with the existing Vyper install, invokes cached `rea-agents@6.7.0`, and regenerates the retained probe and measurement files. The current worktree's unrelated pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification was left untouched.