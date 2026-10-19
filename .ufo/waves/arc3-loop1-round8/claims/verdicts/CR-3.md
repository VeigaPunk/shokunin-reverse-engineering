# CR-3 — arc3-loop1-round8 reconciliation

Seat CR-3, verdicts/convergence chain. I compared the current R8 claim artifacts and independently re-ran the relevant gate, live-pin, corpus-count and Vyper checks. Repository `HEAD` is `904b724258fc9396a016bd9952b5cd40225fb7d8`; the frozen prior work object resolves to `7deeb36045209f3fbeb4460edd7aef5b5270af22`. Git was read-only. This file is the only CR-3 write; source, corpus, receipt and gate files remain untouched.

## Per-claim rulings

### C1 — operability: `ptr_check` reachability

- **REPRODUCED — blind spot and live helper behavior.** `.ufo/gates/c1-census-v10.py:511-514` only collects `PTR` when no other occurrence was found. The `PROVINCE.md:18` clause contains a pin/version as well as the full path pointer, so the unmodified classifier misses that pointer. An independent helper invocation returned:

  ```text
  live_pins={'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
  ptr_check(config.toml:3546)=('stale', "line holds no rea-agents pin: 'max_output_size = 64000'")
  ptr_check(config.toml:4126)=('ok', 'pins 6.7.0')
  ptr_check(config.toml:999999)=('unresolved', 'line 999999 beyond EOF (4150 lines)')
  ```

- **DISCREPANCY — unmodified HEAD is already red.** `python3 .ufo/gates/c1-census-v10.py --json` exited 1 / `FAIL` before any candidate change. The JSON reports 19 keys, base counts `PROVINCE 162 lines/6 loci; SCORECARD 1813/10; SKILL 413/2`, G21 `14` rows with no frontier errors, G2 true, and the undeclared `SCORECARD.md:1776-1783` block (line 1780 has unscoped `6.4.0` and `6.7.0`). The gate’s declared SCORECARD scope ends at line 855 (`.ufo/gates/c1-census-v10.py:274-275`). A candidate must account for that independent HEAD failure to show the frozen clean-PASS behavior.
- **REPRODUCED — RV-2 candidate and seeded fault, on scratch only.** I recommend RV-2’s narrower patch text at `.ufo/waves/arc3-loop1-round8/claims/c1/RV-2.md:32-54`: collect pointers in CURRENT scope despite another locus and add a DATED row for the measured R7 assertion block `1776-1783`, marker at line 1777. `python3 -m py_compile /var/tmp/kaidoku-rv2-arc3-r8-rytct4hf/c1-census-v10.py` passed. The candidate’s clean scratch fixture also simulated C2’s `:3546` → live `:4126` change; it is not the actual source tree:

  ```text
  clean: exit=0 verdict=PASS keys=19
    counts={PROVINCE.md:162/6, SCORECARD.md:1813/10, SKILL.md:413/2}
    current_ok={PROVINCE.md:20, SCORECARD.md:15, SKILL.md:3}
    undeclared=[] unresolved=[] G21=14 frontier_errors=[] G2=True
  fault: exit=1 verdict=FAIL
    PROVINCE.md block 15-26: :999999 -> UNRESOLVED (line 999999 beyond EOF (4150 lines))
    counts unchanged; G21=14 frontier_errors=[] G2=True
  ```

  The exact candidate patch is not landed. The clean run depends on both the scratch pointer correction and candidate gate/scope changes.
- **DISCREPANCY / interpretation required — “all existing counters intact.”** Structural `counts`, the 19-key JSON contract and G21 are preserved. The derived `current_ok_per_file` output changes from baseline `17/14/3` to `20/15/3` because new pointer assertions (and the added dated scope) are now counted. If “all counters” literally requires those positive assertion totals to stay numerically fixed, the candidate does not satisfy it; if it means preserve the schema, structural counts and G21 while correctly counting newly reached assertions, it does. Do not conceal this distinction in integration.
- **UNVERIFIABLE — landing.** Current HEAD still has the blind spot and the unrelated undeclared SCORECARD block. This seat was authorized to supply verdict evidence only, not edit the gate.

### C2 — freshness: PROVINCE pointer and receipt

- **VERIFIED / CORRECTED — live anchor.** A fresh byte read of `/home/vgpnk/.kimi-code/config.toml` found `4150` lines and exactly one `rea-agents@` match:

  ```text
  4126: args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  line 3546: max_output_size = 64000
  SHA-256 of line content without terminator: eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
  SHA-256 including LF: eb1c7da74fc5f870d7c6537e87beeaf043491b5cdd00ee7a2f65e426d9f2b675
  ```

  `HEAD:PROVINCE.md:18` still cites `:3546`; the proposed `:3546` → `:4126` text and matching line-content receipt are present in the C2 seat artifacts (for example `.ufo/waves/arc3-loop1-round8/claims/c2/EX-5.md:13-31` and `.ufo/waves/arc3-loop1-round8/claims/c2/CR-2/receipt.txt:1-11`). The file remains 162 lines; the patch is one same-line token replacement.
- **CORRECTED — scope description.** The frozen claims describe `PROVINCE.md:15-26` as DATED (`.ufo/waves/arc3-loop1-round8/claims-frozen.md:39-45`), but the live gate declares that block CURRENT (`.ufo/gates/c1-census-v10.py:255-257`). Therefore `:18` must be evaluated against the live pin, not excused as dated history.
- **UNVERIFIABLE — same-commit receipt landing.** `HEAD` still contains `:3546`; `.ufo/receipts/` is absent in the worktree and has no entries in `HEAD`. C2 receipts are retained only under seat artifact paths. Neither the pointer edit nor a durable shared receipt is in the same commit as C1. Integration must remeasure the line/hash at landing and co-land the receipt with the chosen C1 patch.

### C3 — coverage: one Vyper optimizer-form Unknown

- **REPRODUCED — bounded byte characterization and real REA calls.** I freshly compiled the retained synthetic K8 source using the lane’s Vyper `0.4.3+commit.bff19ea2` executable. Both compiler outputs compared byte-identically with SC-2’s retained carriers; decoded runtimes were `--no-optimize` 617 bytes / SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc` and `-O codesize` 360 bytes / SHA-256 `bf5afe485f0aa298c488ba7101dfe99f8ab372174cee605ffec4a4d796ca2ba5`. Fresh local REA 6.7.0 calls plus `.ufo/waves/arc3-loop1-round8/claims/c3/SC-2/evidence/rederive.py` produced:

  ```text
  abi_function_count=8
  independent_selector_count=8
  compiler_methodid_count=8
  selector_set_matches_methodids=True
  [noopt] REA_function_count=8 unique_selector_count=8 REA_missing=[] REA_extra=[]
  noopt_selector_chain_sites=8 all_expected_sequence=True
  [codesize] PUSH4_sites=[] CODECOPY_pcs=[12, 45] EQ_count=1 MOD_count=1
  codesize_table_start=0x12b first_CODECOPY_size=5 table_bytes=61 header=01c3013008 header_bytes=5 record_width=7
  codesize_table_selectors_match=True codesize_targets_are_jumpdest=True
  ```

  Fresh REA raw/normalized results each contained the eight selectors; codesize likewise returned 8/8, with no missing/extra selectors. The noopt offsets are `PUSH4 PC + 12` and point to `CALLVALUE`; codesize offsets all point to `DUP1`, not the distinct table targets. The retained source/evidence and independent derivation are at `.ufo/waves/arc3-loop1-round8/claims/c3/SC-2/evidence/`; the rederived table/selector details are in the output above. This is a synthetic fixture and static inference only: no deployment identity, runtime execution, chain query, or general Vyper rule is established.
- **VERIFIED — Command A baseline; projection is not a landing measurement.** Running the `SCORECARD.md:88-124` recipe against both immutable revisions returned:

  ```json
  {"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":86,"mapped":86,"missing":[],"revision":"904b724258fc9396a016bd9952b5cd40225fb7d8","rule_blocks":15}
  {"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":86,"mapped":86,"missing":[],"revision":"7deeb36045209f3fbeb4460edd7aef5b5270af22","rule_blocks":15}
  ```

  An in-memory addition of the proposed `2026-10-19-arc3-r7-vyper-optimizer-forms` file stem and matching map token projects to 87 files / 87 mapped, `missing=[]`, `dangling=[]`. The stem and file are absent from HEAD; this is set arithmetic, not Command A after landing.
- **REPRODUCED / UNVERIFIABLE — draft versus corpus closure.** I recommend RV-3’s single `2026-10-19-arc3-r7-vyper-optimizer-forms` draft as the base, not a merge of competing entries. Its embedded draft names the absolute K8 source path and SHA-256 (`.ufo/waves/arc3-loop1-round8/claims/c3/RV-3.md:42-77`, especially line 47), satisfying `corpus/QUALITY.md:14`’s artifact-identity requirement; it also resolves the R7 table-length/copy-window discrepancy and rechecks the `-O none` alias within this fixture. This does not make the draft landed. The candidate entry still needs a corpus-contract correction: the admission contract requires each count in the form `<number> — <command> <date>` (`/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md:33-37`). Its counts, including the eight-function / 8-of-8 tallies and byte/table totals in `.ufo/waves/arc3-loop1-round8/claims/c3/RV-3.md:72-75`, do not use that form; `verified-at:` alone is not the count’s command/date. Correct the selected draft before integration. I do not recommend CN-2’s EX-8 draft as-is: `.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/entry-draft.md:1` groups `rederive.sh` and `measure.py` under `evidence/`, while the actual files are `.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/rederive.sh` and `.ufo/waves/arc3-loop1-round8/claims/c3/EX-8/measure.py` at the seat root.
- **UNVERIFIABLE — corpus landing and 86→87 after-state.** No canonical knowledge entry or EVM map token is in HEAD, so the frozen C3 closure condition and post-landing Command A remain outstanding.

## Integration boundaries

- Apply the selected C1 patch only after resolving the counter semantics; re-run clean and dead-pointer fixtures against the combined candidate.
- Re-anchor `PROVINCE.md:18` and store a remeasured content receipt in the durable receipt path in the same commit as C1.
- Correct the RV-3 corpus draft’s count notation, land exactly one knowledge entry plus one EVM map token, then execute Command A at that landing revision. Do not report the 87/87 projection as measured.
- Peer verdicts VZ-1/VZ-2 record earlier inventories without the later R8 candidate files; their early “no candidate visible” observations are superseded by the artifacts now present, not by the measurements above.
