# CN-4 — arc3-loop1-round9 reconciliation verdict

Measured against repository HEAD `947091d6b6f52684faf9ca53adf94ff8a0f6b006`. This artifact is the only path I wrote; source, gate, receipt, corpus, coverage map, and peer artifacts remain read-only. Scratch and compiler outputs used for my checks are under `/var/tmp`.

## C1 — freshness: CORRECTED as proposal; gate condition DISCREPANCY

The live row at `PROVINCE.md:50` still states `1556 signed archives` without its own as-of qualifier. My fresh census returned:

```text
archive_count=1350 signature_count=1350 missing_signature_count=0 orphan_signature_count=0
jq 1.8.2-1
jq: 25 total files, 0 altered files
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  -
162 PROVINCE.md
```

The measured delta is `1350 - 1556 = -206`, but the original 1,556 count is only a dated record (`corpus/knowledge/2026-10-13-pacman-packages.md:21-25`); it cannot be reconstructed from today's cache. The equal `.sig` sidecar count establishes pairing, not cryptographic validity of every signature. The installed/archive `jq` digest agrees; the `available:true` live-session observation is not re-probed and should be dated to the enclosing 2026-10-13 table observation (`PROVINCE.md:40`). `.MTREE` and the named verification commands are format/method descriptions, not additional volatile outcomes. This matches the C1 census in `claims/c1/PL-2.md:28-34` and `claims/c1/EX-3.md:19-24`.

**Recommended same-line patch text (not applied):**

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session, 2026-10-13); pacman `.pkg.tar.zst` corpus: 1,556 signed archives (2026-10-13 snapshot; live re-count 2026-10-19: 1,350 archives and 1,350 matching `.sig` sidecars, −206; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq 1.8.2-1` byte-identical to its signed archive member (reverified 2026-10-19; SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`) |
```

The count/JQ facts and rationale are independently recorded in `claims/c1/PL-2.md:10-16,20-34`; the previous 1,556 count is properly treated as a recorded snapshot, not a fresh measurement. The row patch preserves 162 lines, but the frozen requirement that the instrument still PASS is **DISCREPANCY**. I reran `python3 .ufo/gates/c1-census-v10.py --root .`; it exited 1 with:

```text
-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
FRONTIER register (G21): 14 rows asserted, errors: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

The candidate row cannot clear that unrelated `SCORECARD.md:1834` locus; the gate's declared SCORECARD scope ends at line 1813, so this finding is out of scope for its current register (`claims/c1/PL-2.md:38-50`, `claims/c1/EX-3.md:46-48`). The C1 scratch-after result is the same. I did not edit the gate or SCORECARD.

## C2 — coverage: REPRODUCED with a qualified extension beyond r8

All 12 rostered C2 artifacts are now present: `EX-5` through `EX-12` and `CR-1` through `CR-4`. The current selection split is six Vyper boundary seats (`CR-2`, `CR-3`, `CR-4`, `EX-7`, `EX-9`, `EX-10`), two viaIR fallback seats (`EX-6`, `EX-8`), two other-solc-version seats (`EX-5`, `EX-12`), and two verb-family Evidence-ID seats (`CR-1`, `EX-11`).

My fresh compilation of exact `K8.vy` bytes and Vyper 0.4.3 reproduced the already-recorded runtime boundary:

```text
source_sha256=62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d
compiler=0.4.3+commit.bff19ea2
noopt runtime repeat: cmp OK
none runtime repeat: cmp OK
bytecode_runtime cross-form: cmp OK
abi cross-form: cmp OK
method_identifiers cross-form: cmp OK
settings cross-form: cmp OK
noopt: runtime_bytes=617 runtime_sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc settings={"experimental_codegen":false,"optimize":"none"}
none: runtime_bytes=617 runtime_sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc settings={"experimental_codegen":false,"optimize":"none"}
raw_rows=[8, 8] normalized_rows=[8, 8] raw_functions_identical=True normalized_functions_identical=True decoded_hex_identical=True decoded_hashes_equal=True
noopt_selector_set_matches_compiler=True none_selector_set_matches_compiler=True
```

The local REA 6.7.0 calls returned IDs `ev_3228b4e0c550f16b7dafc91da9105d6ae9c5eb8a9b0ec26c1487527938498a22` and `ev_150deb7930edef6252baea0081befb463dbd260178a553a7b0e82acc88b4a83b`; both remain static inferred results with unknown discovery completeness and `runtime_execution=not-performed`. Scratch: `/var/tmp/kaidoku-cn4-r9-vyper.LBH77P`.

The narrow equivalence is already in the canonical r8 entry (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:7-11`) and mapped at `corpus/README.md:38`. But r8 compared runtime, ABI, method IDs, and settings—not the full compiler output surface. I independently extended the check to all 31 Vyper `-f` formats, two runs per flag, in `/var/tmp/kaidoku-cn4-r9-vyper-allformats.aOifrp`. The command form was `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper [--no-optimize|-O none] -f <format> .ufo/waves/arc3-loop1-round9/claims/c2/EX-10/evidence/K8.vy`; the 124 calls used TMPDIR under the scratch directory. The full format list and peer command transcript are at `claims/c2/EX-10/evidence/commands.txt:1-124`:

```text
source_bytes=580 source_sha256=62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d
vyper_version=0.4.3+commit.bff19ea2
formats=31 compile_calls=124 cross_flag_raw_equal_count=28 cross_flag_raw_different=['ast', 'annotated_ast', 'archive']
ast: raw_equal=False canonical_json_equal=True stdout_bytes=(15213,15213)
annotated_ast: raw_equal=False canonical_json_equal=True stdout_bytes=(18294,18294)
archive: raw_cross_equal=False archive_member_count=7 payloads_all_equal=True distinct_member_timestamp_sets=2 stdout_bytes=(1280,1280)
noopt: runtime_bytes=617 runtime_sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
none: runtime_bytes=617 runtime_sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
REA raw_rows=[8, 8] normalized_rows=[8, 8] normalized_functions_identical=True decoded_hashes=["1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc","1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc"] discovery_completeness=['unknown','unknown'] runtime_execution=['not-performed','not-performed']
```

The four `ast` and `annotated_ast` raw stdout captures varied across repeats, but all four canonical JSON values matched for each format. Archive member timestamps observed in this run were 2026-10-19 15:35:18 for both `--no-optimize` repeats and 15:35:24 for both `-O none` repeats; raw archive bytes matched within each flag, and all seven member payloads matched across the four archives. The comparison does not attribute every changed ZIP-container byte exclusively to timestamps. Thus the runtime/deployable payload is identical, while raw AST renderings and the archive wrapper retain byte-level differences. This is a real, bounded residual and makes the broader frozen candidate (“any residual byte-level distinction,” `claims-frozen.md:30-42`) eligible for C2; the five runtime-only Vyper reports are corroborating but add no scope beyond r8. The wider result and carefully qualified interpretation are in `claims/c2/EX-10.md:3-9` and its draft at `claims/c2/EX-10/evidence/entry-draft.md:9-21`.

**Integration recommendation:** use the single EX-10 draft, destination `corpus/knowledge/2026-10-19-arc3-r9-vyper-noopt-none-boundary.md`, token `2026-10-19-arc3-r9-vyper-noopt-none-boundary`. Do not add a duplicate entry asserting only runtime equivalence. The other candidate families are also independently valid bounded work: I recompiled/re-probed EX-6's viaIR fallback carrier and EX-5's solc 0.8.28 case (details below), while EX-8, EX-12, CR-1, and EX-11 provide separate peer evidence. Integrate only one candidate and rerun Command A.

My independent EX-6 compile/probe in `/var/tmp/kaidoku-cn4-r9-ex6.D5ZHLy` reproduced the explicit r6 fallback gap (`corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`): solc 0.8.37 produced runtime 366 B / SHA-256 `2948d578ae460119f777eb379febc2738dbec14d03c76d5f100777c9552ce6fc`, creation 392 B / `a24cb1651e78dd159425d5b27c9ba513b50b0401f5bcf3589f259b0a70d0ba9e`; REA recovered 3/3 compiler selectors and marked the result inferred, discovery unknown, execution not performed. Its opcode walk confirmed `PUSH4 0xdb1d0fd5; SUB; PUSH2 0x000e; JUMPI`; this is a viable alternative, not an executed-call claim (`claims/c2/EX-6/evidence/corpus-draft.md:10-20`).

My independent offline EX-5 recompile used `solc@0.8.28` tarball SHA-256 `8fb2c6144f01797f352a8284914ee4436462db7a96108e49826f3311e2aef32d`; the 1,517-byte viaIR runtime SHA-256 was `3f28f35ea804ce431cca75f3c2b6602aaeaf17938f4d4a773654e19a95f07967`, and bytes `[0,1464)` matched the 0.8.37 control prefix (`34a46554c003760ddc41c3e7c2ec94cdc08b0d162a75a763d6f06c49ed03ed15`). REA's 15 raw and normalized rows matched compiler method IDs for both versions; results were inferred and not executed. This independently narrows the separate r6 solc-version Unknown (`claims/c2/EX-5.md:7-11`).

Command A baseline at HEAD is `knowledge_files=87`, `mapped=87`, `missing=[]`, `dangling=[]`, `citation_resolved_rules=15`, `rule_blocks=15` (`SCORECARD.md:88-124`; also `claims/c2/CR-4.md:18`). No post-landing result exists: all corpus drafts and tokens remain unintegrated, so the required 87→88 check is **UNVERIFIABLE**.

## C3 — calibration: positional drift reproduced; historic intermediate partly unverifiable

The live `/home/vgpnk/.kimi-code/config.toml` is 4,150 lines with one `rea-agents@` match:

```text
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
config_lines=4150 match_count=1
```

The current `PROVINCE.md:18` pointer is therefore correctly keyed to line 4126. The gate grades that individual assertion `current-ok (pins 6.7.0)`, but the same whole-gate run is `FAIL` on the unrelated undeclared `SCORECARD.md:1834` finding shown under C1. Per-pointer success is not overall gate PASS.

I independently exercised the gate's `ptr_check()` with a synthetic config under `/var/tmp/kaidoku-cn4-pin-probe` (live config untouched):

```text
before insertion: ('ok', 'pins 6.7.0')
after insertion, old pointer: ('stale', "line holds no rea-agents pin: '# inert probe'")
after insertion, re-anchored pointer: ('ok', 'pins 6.7.0')
after trailing insertion, current pointer: ('ok', 'pins 6.7.0')
```

This reproduces a physical-line locator: insertions before the target stale the stored coordinate until re-keyed; trailing edits do not move it. The implementation confirms the boundary: `live_pins()` takes the first regex match (`.ufo/gates/c1-census-v10.py:324-334`), `ptr_check()` reads the nominated physical line and checks the version (`:466-482`), and `classify()` routes pointer assertions through it (`:538-544`). The instrument does not enforce uniqueness, although the current live config has exactly one occurrence. The broader characterization agrees with `claims/c3/SC-1.md:64-68` and `claims/c3/EX-13.md:73-97`.

The current line and insertion behavior are **VERIFIED/REPRODUCED**. The claimed historical `:3546` intermediate is **UNVERIFIABLE** from the available config backups I inspected: the observed archived positions include 2915, 2932, 2940, 3227, 3298, and 3157, but none at 3546 (`claims/c3/SC-1.md:38-51` records the same bounded backup result). Do not present the entire `2940 → 3227 → 3298 → 3546 → 4126` sequence as independently reconstructed. The durable C3 characterization is present in the seat artifact (`SC-1.md:64-68`); no receipt or canonical corpus edit was made here.

## Final disposition

- C1: the correct row repair is evidenced as patch text, but the frozen gate-PASS condition is **DISCREPANCY** until the out-of-scope SCORECARD locus is addressed by its owner.
- C2: the runtime equivalence is already mapped in r8, but the broader Vyper output-boundary residuals are **REPRODUCED** across 31 formats; integrate the EX-10 draft as the single C2 entry, then rerun Command A.
- C3: current pin uniqueness, `current-ok`, and positional drift are **VERIFIED/REPRODUCED**; the old `:3546` intermediate remains **UNVERIFIABLE** from available snapshots, and the complete census gate remains FAIL for the same unrelated SCORECARD locus.

No project tests were run; this verdict changes no executable source. The pre-existing dirty `.ufo/waves/arc2-loop1-round10/C3.md` was not touched.