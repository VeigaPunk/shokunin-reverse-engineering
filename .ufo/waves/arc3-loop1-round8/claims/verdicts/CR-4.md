# CR-4 — arc3-loop1-round8 verdict reconciliation

Review basis: frozen claims in `claims-frozen.md`; current repo HEAD `904b724258fc9396a016bd9952b5cd40225fb7d8`; work commit `7deeb36045209f3fbeb4460edd7aef5b5270af22`. Numeric values below were re-derived in this seat, not copied from previous-round measurements. Gate/fixture tests were scratch-only.

## Rulings

- **C1 operability — blind spot VERIFIED; live-anchor patch REPRODUCED; full landing UNVERIFIABLE.** The collector drops a pointer whenever the same unit already has a pin/version. A narrow scratch patch evaluates the re-anchored live `:4126` pointer as current-ok and catches a dead re-key. The actual gate and PROVINCE line remain unchanged; the clean PASS is a scratch result, not a landed same-commit result. The required content-hash receipt is not consumed by the selected gate diff, so machine-enforced receipt binding remains an integration question.
- **C2 freshness — live pointer and hash VERIFIED; correction text VERIFIED; durable same-commit landing UNVERIFIABLE.** All six C2 seats agree on `:3546` → `:4126` and the line-content digest. Their receipts are only in seat artifact directories; no shared receipt file or source update is landed.
- **C3 coverage — bounded Vyper evidence REPRODUCED; one draft recommended; 87/87 landing UNVERIFIABLE.** The r4 Unknown remains open and the current Command A baseline is 86/86. Fresh compilation and REA calls support closure for this K8 fixture and the two named settings only. Recommend integrating only SC-1’s R8 draft/token; do not land the competing drafts together.

## C1 — pointer reachability, clean PASS and seeded fault

First-hand source identity and baseline:

```text
$ wc -l .ufo/gates/c1-census-v10.py
713 .ufo/gates/c1-census-v10.py
$ sha256sum .ufo/gates/c1-census-v10.py
8002757078a685f515804fc6128ebf76b9925d2033be99a293621e18d14aecca  .ufo/gates/c1-census-v10.py
```

`.ufo/gates/c1-census-v10.py:511-514` puts `PTR.finditer()` behind `if not occ`. My direct `classify('PROVINCE.md', ...)` probe returned `pointer_assertions=0`; the line-18 unit already has the Kimi version pin. Direct calls to the existing helper at `:465-481` returned:

```text
ptr_check(~/.kimi-code/config.toml:3546)=stale; line holds no rea-agents pin
ptr_check(~/.kimi-code/config.toml:4126)=ok; pins 6.7.0
ptr_check(~/.kimi-code/config.toml:999999)=unresolved; line 999999 beyond EOF (4150 lines)
```

I re-ran the unmodified gate on current HEAD. It already exits FAIL on the R7 scorecard record, separate from the pointer defect:

```text
python3 .ufo/gates/c1-census-v10.py --json
exit=1 verdict=FAIL
counts={PROVINCE.md:162 lines/6 loci, SCORECARD.md:1813 lines/10 loci, SKILL.md:413 lines/2 loci}
frontier_rows=14 frontier_errors=[] g2_ok=true
current_ok_per_file={PROVINCE.md:17,SCORECARD.md:14,SKILL.md:3}
undeclared=[SCORECARD.md block 1776-1783; line 1780 values 6.4.0 and 6.7.0]
```

### Candidate selection and scratch re-run

I reviewed the six C1 artifacts. RV-1's collector-only candidate leaves this current-HEAD failure unresolved; PL-2's clean PASS is on the older work snapshot and its own current-HEAD test still fails. EX-1/EX-2/PL-1 add a wider R7 scorecard scope. I selected RV-2's narrower candidate: add the DATED `SCORECARD.md:1776-1783` scope row (marker at line 1777), then collect pointers where `ptr_scope == "CURRENT"` even when another locus exists, retaining the old pointer-only path otherwise. The extra scope row is necessary for a clean current-HEAD result; without it a pointer-only patch still fails on line 1780.

I checked the candidate diff against the unchanged gate and re-ran both candidate trees from RV-2's `/var/tmp` scratch root. Candidate SHA-256: `1cc82e78c91700966b9ffb68239a8c878359521121ad24dafa733f49278a0d83` (717 lines).

```text
clean: exit=0 verdict=PASS
PROVINCE :18 pointer=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
frontier_rows=14 frontier_errors=[] g2_ok=true
counts={PROVINCE.md:162/6,SCORECARD.md:1813/10,SKILL.md:413/2}
current_ok_per_file={PROVINCE.md:20,SCORECARD.md:15,SKILL.md:3}

fault: exit=1 verdict=FAIL
PROVINCE :18 pointer=~/.kimi-code/config.toml:999999 -> UNRESOLVED (line 999999 beyond EOF (4150 lines))
frontier_rows=14 frontier_errors=[] g2_ok=true
current_ok_per_file={PROVINCE.md:19,SCORECARD.md:15,SKILL.md:3}
```

My JSON comparison found 19 keys for baseline, clean and fault, with identical key sets. The per-file count/locus objects and G21 register are preserved; `current_ok_per_file` increases because the newly reachable pointers and the dated R7 record now count. If “all existing counters intact” requires identical numeric positive counts, that is not the observed result; the fields and their meanings remain present.

The patch uses live `ptr_check()` rather than a hard-coded current-ok exemption, so the live pointer/fault behavior is reproduced. It contains no lookup of the C2 line-content receipt. If “receipt anchor” requires the instrument itself to validate that digest, this candidate has not established that requirement. No patch was applied to `.ufo/gates/`; the real `PROVINCE.md:18` still points at `:3546`.

## C2 — pointer, patch text and receipt

My fresh config search returned:

```text
/home/vgpnk/.kimi-code/config.toml:4124:[mcp_servers.rea]
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
file_lines=4150
```

`PROVINCE.md:18` still contains `~/.kimi-code/config.toml:3546`; that target currently holds no REA pin. My in-memory one-token substitution found one occurrence, changed only line 18, preserved 162 lines and left total file bytes at 19,908. The proposed correction is exactly `:3546` → `:4126`, not applied.

I read and hashed the exact live `args` line bytes:

```text
line_content_sha256 (UTF-8, no terminator)=eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
line_record_sha256 (including LF)=eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675
```

The six C2 artifacts agree on the replacement and these digests. Receipt copies are present in, for example, `claims/c2/CR-1/evidence/live-config-receipt.txt`, `claims/c2/EX-3/receipt.txt`, and `claims/c2/CR-2/receipt.txt`. `Glob(.ufo/receipts/**/*)` found no shared receipt file. Neither the pointer update nor a durable receipt is in a commit with C1.

Non-blocking chronology note: CR-2 records capture time `17:55:09Z`, while the unchanged PROVINCE prose refers to a `17:55:49Z` receipt. That text was 40 seconds ahead of CR-2’s capture; it does not conflict with the current line hash, but the historical suffix should be checked at integration rather than silently refreshed from this capture.

## C3 — fresh Vyper check and draft reconciliation

The named Unknown remains at `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`. Grep of `corpus/` and Glob of `corpus/knowledge/*arc3-r7-vyper-*` found no landed R7 Vyper entry or proposed token. I independently ran Command A from `SCORECARD.md:88-124` against both immutable revisions:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":86,"mapped":86,"missing":[],"revision":"904b724258fc9396a016bd9952b5cd40225fb7d8","rule_blocks":15}
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":86,"mapped":86,"missing":[],"revision":"7deeb36045209f3fbeb4460edd7aef5b5270af22","rule_blocks":15}
```

For an independent fresh measurement, I copied the current K8 source to `/var/tmp/kaidoku-cr4-r8.mvALLg`, compiled gas, `--no-optimize`, `-O none`, and `-O codesize` with the existing Vyper executable, and ran REA 6.7.0 on fresh noopt/codesize hex carriers. Source SHA-256: `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`; Vyper `0.4.3+commit.bff19ea2`, executable SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`. The explicit `-O gas` output matched default gas; `-O none` matched `--no-optimize` byte-for-byte for this fixture.

```text
noopt: 617 bytes; SHA-256 1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
codesize: 360 bytes; SHA-256 bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5
ABI/method identifiers/independent Keccak: 8 distinct selectors, sets equal
noopt byte walk: 8 PUSH4/DUP2/EQ/ISZERO/PUSH2/JUMPI compare legs
codesize byte walk: no opcode-boundary PUSH4; one EQ, one MOD, two CODECOPY
codesize suffix at 0x12b: 61 bytes, five-byte header + eight 7-byte records
codesize selectors match; all eight record targets point to JUMPDEST bytes
```

Fresh REA returned 8 raw and 8 normalized functions for each carrier, `dispatch=abi`, matching compiler selectors and decoded bytecode hash. Evidence IDs: noopt `ev_c4382c20ec6ecb64298a9619243dd3c7cc218f7eadfb67cd8fa90eb575b3dc79`; codesize `ev_631504bd09345844d6ff6b0870d646d801ff49ff899b9acd09d493fcd0af0e66`. Full JSON and byte-walk output are retained under `claims/verdicts/CR-4/evidence/`. These are static/inferred results: `discovery_completeness=unknown`, `runtime_execution=not-performed`; the carrier is synthetic, not a deployed contract. The fresh `-O none` equality is fixture-scoped and is not needed for the chosen two-option closure.

R7 EX-4’s cited 27-byte sequence is an excerpt/prefix, not a competing full-tail measurement; my independent parse measures the full suffix as 61 bytes. Drafts EX-7, EX-8, SC-1 and SC-2 offer different filenames/tokens. I recommend **SC-1’s** single bounded entry at `claims/c3/SC-1/entry-draft.md`, destination `2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md`, token `2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes`. It explicitly reconciles the R7 drafts, keeps only the two settings needed for this Unknown, and records scope and analyzer limits. EX-8 separately verifies `-O none` equality; that can remain an optional fixture observation, not a second entry. Do not land multiple competing entries/tokens.

C3 remains pending integration: only after one new knowledge file and its one EVM map token land should Command A be run on that commit for the expected 87/87. No 87/87 result is claimed here.

## Peer reconciliation and write boundary

C1/C2 peer artifacts are now present and their principal measurements match the first-hand checks above. VZ-1/VZ-2 were written before those artifacts appeared; their “not present” statements are point-in-time snapshots, not the current inventory. At this review, no CN-1, CN-2 or CR-3 verdict artifact was visible, so their convergence cannot be reported.

Only this seat’s deliverables were written: `claims/verdicts/CR-4.md` and `claims/verdicts/CR-4/evidence/*`. No gate, PROVINCE, SCORECARD, SKILL, corpus, map, LOG or receipt outside this seat directory was changed. The unrelated pre-existing worktree modification `.ufo/waves/arc2-loop1-round10/C3.md` was left untouched.
