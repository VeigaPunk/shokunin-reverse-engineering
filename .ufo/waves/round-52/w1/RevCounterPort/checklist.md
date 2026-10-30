# R52 C1 counter port-fidelity checklist

Axes: semantic preservation; explicit round deltas; fail-closed controls; traceable evidence.

Static source review only. `v1:L` below means `tools/round-50/c1-counter.py:L`; `claims:L` means `plans/round-52-claims.md:L` (claims draft supplied by assignment). No v2 implementation is adjudicated here. Checkboxes are acceptance requirements, not reported passes. LSP unavailable: reading `xd://lsp` returned “No such tool”; all locations below are literal source inspection, not semantic-reference proof.

## A. Preserve the v1 behavior except the explicit deltas in B

| Check | v1 source | Demanded v2 behavior |
|---|---|---|
| [ ] Frozen object reads | v1:460-470,2147-2197 | Read score inputs from git objects at REV/FREEZE, not mutable worktree copies; external bytes only from the explicit pinned carrier cache. Resolve REV/FREEZE as commits. |
| [ ] Counter identity | v1:517-568,2155-2163 | Running counter bytes equal counter at FREEZE or exit 2 `counter_not_frozen`; every written score receipt carries absolute `counter` and byte SHA256 `counter_sha256`; reread and verify written receipt. |
| [ ] Receipt verification CLI | v1:533-554,2536-2550 | `--verify-receipt` returns 0 honest identity, 1 missing/null/malformed/mismatched identity (including unavailable named counter), 2 unreadable/non-JSON receipt. Never confuse this digest with evidence-id validation. |
| [ ] Raw receipt binding | v1:2302-2311,2433-2435 | Hash exact committed after.json bytes into carrier `receipt_digest`; emit `evidence_digests` mapping carrier to path and SHA256. |
| [ ] Envelope vs score | v1:2321-2322 | Reject committed after-envelopes containing either `counter_sha256` or `exit_code`; never accept counter scores as REA evidence. |
| [ ] Subject equals pin | v1:2323-2325 | `subject.digest.sha256 == frozen carrier pin`, independently of carrier hash and evidence-id correctness; reminting an envelope does not waive it. |
| [ ] Evidence-id recomputation | v1:615-699,2420-2425 | Recompute using frozen XPIN and REA package's own semanticProjection/digest code; stored and recomputed id equal and begin `ev_`; package version/package.json/package-lock hashes match frozen package doc. Missing package/tool/node, xpin failure, wrong output count/format are unevaluable. |
| [ ] Receipt addition history | v1:1572-1593,2313-2317 | Inspect EVERY addition over `git log -m --full-history --diff-filter=A`, not simplified history or only newest add; all adds must strictly descend from receipt freshness base, not equal it. Preserve `receipt_adds` and oldest `receipt_first_add`; side-branch pre-base add/re-add remains red. B changes the configurable base, not this invariant. |
| [ ] Carrier nonvacuity | v1:872-987,2204-2213 | Exactly target 4 distinct expected ids (case-insensitive id set), distinct valid pins, mandatory positive budgets with max_depth exactly 1, explicit `plus-extractor` profile, and well-formed oracle/nonregular/path or external chain. Do not silently default away malformed spec. |
| [ ] External chain | v1:927-985,2237-2249 | Validate URL/image hash/member/member hash/positive carve length and nested SHA when nested; no simultaneous committed path and external source. Cache `<pin>.bin` hashes to pin before derivation/rerun; missing/bad cache not green. |
| [ ] Layout | v1:992-1056,2252-2271 | LE `hsqs`, v4.0, xz compression 4, 96-byte superblock, `mkfs_time == bytes_used`, valid ordered inode/directory offsets and bytes_used within file. Exact carve length == bytes_used == file size. No BE block-length special case or gzip diversity requirement. Marker is pinned-layout evidence, not provenance. |
| [ ] Regular oracle grammar | v1:704-739 | Nonempty exactly-three-column `(relative path,64-hex sha256,nonnegative decimal size)` set; reject duplicate paths, illegal components, malformed size/hash. |
| [ ] Regular oracle rerivation | v1:2094-2142,2273-2293 | Frozen `/usr/bin/unsquashfs` 4.7.5 extracts regular-file `(rel,sha,size)` set; compare in BOTH directions. Missing/wrong-version/nonrunning reader or no output tree -> exit 2 `oracle_env_error`, never green. Exclude symlinks/nonregular objects; clean scratch. Nonregular derivation is added, not substituted for this check. |
| [ ] Nonregular grammar | v1:742-768,2295-2300 | Parse `(rel,kind[,detail])`, tolerated header, lowercase kind, optional detail, empty table legal, duplicate `(rel,kind)` illegal. Score all frozen nonregular kinds. |
| [ ] Root derivation | v1:1190-1241,2336-2347 | Root comes from derivation child with exact HANDLER equality; exactly one root or frozen valid oracle_root naming an actual root; otherwise fail closed, no text reconstruction or suffix guess. Preserve root/source/chunk_roots diagnostics. |
| [ ] Path identity | v1:1085-1187,1289-1325,1365-1437 | Strip `$output/` once; whole-segment containment; exact relative equality, no suffix collisions; outside-root files belong to another namespace; nested extraction roots cannot publish outer oracle rows. |
| [ ] Published regular set | v1:2345-2356 | Every oracle row matches exact relative path/hash/size and no extra regular path under subject root. Nested and outside namespaces do not create false extras or satisfy rows. |
| [ ] Published nonregular prohibition | v1:1427-1437,2372-2375 | No published regular file path may equal any nonregular oracle path; a preserved gap does not excuse materializing a symlink/device. |
| [ ] Operation/handler/chunks | v1:2326-2335 | `extract_firmware`, provider `unblob`; at least one SquashFS-family handler and EVERY such handler exactly `squashfs_v4_le`; no failed chunk. Actual code allows multiple same-handler chunks: do not replace this with cardinality-one assertion from doc shorthand. |
| [ ] Disposition, not counting shortcut | v1:1458-1569,2360-2371 | Every pathful gap resolves to exactly one nonregular row with allowed kind; every configured removal diagnostic resolves to exact permitted row, never both gap and removal; every required row has disposition or matching silent detail. Unknown root, pathless unallowed gap, pathful structural gap, over-limit structural count -> red. Preserve exact-path lookup and per-detail symlink silence. |
| [ ] Removal trust boundary | v1:1071-1080,1244-1276,1525-1547 | `report.link` must be under trusted parent of this receipt's absolute output directory; filesystem-root parent and foreign run root cannot map a removal. |
| [ ] Legal receipt path spellings | v1:1148-1177,2376-2378 | Reject absolute paths, empty/dot/dot-dot components, trailing slash in normalized receipt paths; do not normalize invalid spellings into a pass. |
| [ ] Provenance scope | v1:1061-1068,2379 | Absolute output path STARTS WITH round scratch base; reject `..`, relative path and substring-only provenance. Parameter hashing is evidence consistency, not writer authentication. |
| [ ] Frozen parameters | v1:909-919,2380-2389,2043-2050 | Compare exact max_depth/max_output_bytes/max_output_files to frozen table with non-bool integer validation; replay frozen table values, never receipt-selected budgets/depth. |
| [ ] Projection must be real | v1:2391-2417,2555-2563 | Counter runs same pinned bytes on fresh extraction root; absent receipt/bytes or bad pin skips but leaves projection false. Full predicate never accepts `--no-rerun` (exit 2 `rerun_disabled`). Offline controls must be separately labeled and cannot mean full predicate met. |
| [ ] Canonical package/runtime | v1:1937-2002,2005-2050 | Fixed-PATH node executes CLI entry of same bound REA 6.5.0 package used for evidence-id computation, never npx/registry/ambient runner. Require unblob 26.6.4 and fixed-PATH sasquatch, not sasquatch-v4be. Record path/hash/version toolchain; caller PATH shim cannot satisfy dependencies. |
| [ ] Projection schema | v1:1753-1900 | Preserve sorted normalized subject digest, files `(rel,sha,size,mime,md5,sha1)`, chunks `(handler,start,end,failed)`, gaps `(kind,rel,deps)`, unpublished entries `(kind,rel)`, diagnostics `(typename,rel)`, derivations, engine name/version, published_bytes and coverage for mandatory plus-extractor. Exclude run-varying ids/times/absolute roots; removal of another link must differ. |
| [ ] Projection diffs | v1:1903-1918,2405-2412 | Semantic mismatch -> projection false; expose differing keys and compact details, never evidence-id equality as substitute. |
| [ ] Prior pins | v1:1596-1646,2216-2218 | Union explicit prior_pins and prior tables/docs at FREEZE; record `prior_pin_sources`; no post-freeze source may retroactively bless a replay. Explicit four-pin exception is B, not removal of history checks. |
| [ ] Frozen-input presence | v1:2181-2193,2483-2492 | Tables already exist at FREEZE; every observed nonregular kind appears in rule allowed map. Missing-at-freeze table cannot become a frozen oracle by later add. |
| [ ] Drift is gating | v1:1649-1723,2199-2202 | Freeze-range merged edits, merge-commit edits, M/D/R/T/U and applicable A, plus endpoint blob differences, all exit 2 `frozen_path_changed` with named paths. Change-then-restore remains blocked. Preserve clean-merge green. Expand paths per B. |
| [ ] Full conjunction | v1:432-441,2422-2428,2494-2496 | Every original clause is exactly True for matched carrier; exactly 4 matched, unchanged tables, every binding exactly True. New clauses must join actual verdict, not only receipt decoration. |
| [ ] Diagnostics and exits | v1:2500-2508,2564-2598 | `failing`, `bindings_false`, argv, revision/freeze,target, met_target and semantic exit_code remain visible. 0 predicate met; 1 evaluable not met; 2 unable to evaluate (incl bad args, counter/drift/runtime/oracle failures). Failed receipt-identity write returns 2. B specifies exhausted retry red semantics. |
| [ ] Scratch isolation | v1:476-487,2220-2223,2436-2437,4466-4473 | --work > HYAKU_SCRATCH > fixed fast scratch, no gettempdir; isolated fixture top-level assertion before commits; fixtures/scratch removed; production main never injects simulated runner. |

## A2. Exact original binding inventory and markers

All nine remain operative, with round-sensitive marker substitution below (v1:432-434,2440-2496). Required R52 landing obligations beyond these nine must also be re-derivable; do not assume v1 `sourced` proves all R52 source citations.

| Binding | v1 definition | Exact marker / acceptance in v2 |
|---|---|---|
| [ ] `province_core_section` | v1:2443-2444 | `PROVINCE.md`, heading `## Round-52 additions to Core` (v1 was `## Round-50 additions to Core`). |
| [ ] `province_core_row` | v1:2445-2451 | Row inside that section; FIRST cell has bounded `squashfs_v4_le`; row excluding ENTRY matches `AVM[ _-]marker`; cites exact new entry path. |
| [ ] `frontier_note` | v1:2452-2456 | One line with `Round-52 frontier note`, new STEM, and separate `LE[ _-]AVM` or `AVM[ _-]LE` token after removing STEM; stem's own `avm-le` must not satisfy token. R52 additionally removes LE hsqs from Frontier list. |
| [ ] `entry_present` | v1:2457-2458 | `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md` exists at REV. |
| [ ] `sourced` | v1:2459-2478 | Only entry lines starting `source:` yield bounded `S\d{3,}` tokens; match actual 11-column `corpus/SOURCES.md` S-id row, opened `2026-10-30`, used-by exact new path or stem. Old opened window was 2026-10-28/29. Preserve substring rejection. |
| [ ] `coverage_map_row` | v1:2479-2482 | `corpus/README.md` `## Coverage map` table row names `2026-10-30-r52-avm-le-squashfs-core`. |
| [ ] `carriers_spec_ok` | v1:2204-2205,2483 | No carrier-spec problem; keep prior requirements plus explicit frozen four-pin rescore list validation. |
| [ ] `gap_rule_ok` | v1:2214-2215,2484-2489 | Valid grammar and zero uncovered nonregular kinds; `{R50-C1,R52-C1}` labels per B; law-shape is independently enforced, not inferred from this. |
| [ ] `frozen_tables_valid` | v1:2181-2193,2492 | Carrier/rule documents valid at FREEZE, every referenced oracle/nonregular exists there. |

R52 extra landing checks (claims:162-176): entry cites S243/S244/S245/S249, S250/S251 and source rows opened this round and fresh receipt paths; SOURCES new rows use-by the entry; SCORECARD coverage head 141/141 -> 142/142; LOG entry; instrument-registry v2 exactly one row for each new named .py/.sh/.json instrument, no extra code. These are not checks v1's nine bindings already prove; the v2 package must make each re-derivable rather than imply coverage from `entry_present`/`sourced` alone.

## B. Required explicit changes (not permissions to weaken A)

| Check | v1 origin | R52 requirement / claims source |
|---|---|---|
| [ ] Round identity and predicate text | v1:2-42,374-404,2150,2557 | New counter `tools/round-52/c1-counter.py`, predicate/receipt label R52/P52 identity and sentence matching claims:86-98. Claims file, docstring, receipt must describe same freeze-descendant, unchanged-path, four-carrier conjunction, not old P50 semantics. |
| [ ] Data/rule/carrier defaults | v1:374-376,2235,2513-2529 | Round-52 carriers/rule, `corpus/evidence/round-52/c1`; preserve committed round-50 independent oracle inputs, not blind global r50 replacement. R52 table added at freeze; claims:71-74,79-83,89-90,115-133. |
| [ ] Knowledge/doc constants | v1:377-380,393,396-397 | ENTRY/STEM = `2026-10-30-r52-avm-le-squashfs-core`; Core heading and frontier note above; OPENED dates `2026-10-30`; provenance base `/fast/scratch/hyaku/kaidoku-r52/`. claims:162-171. |
| [ ] Unchanged format/runtime constants | v1:381-412 | Keep HANDLER squashfs_v4_le, TARGET 4, IDS g7581/g7582/c6490/c6430, XPIN, REA 6.5.0, unblob 26.6.4, unsquashfs 4.7.5, xz 4, SB 96, fixed PATH. No authority here to change these with the round number. |
| [ ] Frozen dependency closure | v1:386-425,1649-1658 | Freeze R52 claims and entire tools/round-52 family, all carrier/oracle/nonregular refs, reader/xpin/package pin dependencies and historical prior inputs actually read. Keep R50 inputs needed for controls immutable. claims:87-88,148-153. |
| [ ] Explicit flags | v1:2147-2149,2513-2529 | Expose `--gap-rule`, `--receipts`, `--provenance-base`, `--receipt-fresh-base`; default production round-52 values; control driver explicitly pins round-50 values. Flag wiring must reach rule read, receipt lookup, provenance check and strict history freshness respectively. claims:126-133. |
| [ ] Freeze ancestry gating | v1:2152-2153,1591-1593,2199-2202 | Require REV descends from R52 FREEZE; commit existence alone is not proof of ancestry. Any modified frozen path -> exit 2 with named paths, not advisory receipt field. Add one-mutated-byte fixture proof. claims:86-98,148-150. |
| [ ] `re_scored_pins` | v1:386-390,887-892,1596-1646,2250 | Add tools/round-50/carriers.json to prior carrier tables; R52 prior_pins contains all four measured pins. Freeze explicit allow-list exactly those four pins. `carrier_fresh_ok = valid pin AND (not prior OR on frozen allow-list)`. Emit allow-list and prior_pin_sources; don't relabel old coverage as novel or let arbitrary prior pin through. claims:77-85. This is table policy, not a fourth boolean law clause. |
| [ ] Rule grammar labels | v1:791-793,875-876 | gap_rule_model accepts R50-C1 and R52-C1 for OLD/NEW; frozen production law rule claims R52-C1. Update carrier spec's hardcoded R50-C1 to production R52-C1 too. Preserve other grammar validations; do not accidentally leave v2 rule rejected or allow arbitrary claim labels. claims:151-153. |
| [ ] `law_shape_ok` | v1:771-869,1458-1569,2214-2215,2426,2494 | New fail-closed verdict: char-device/fifo/socket/block-device allowed lists empty, no device detail whitelist under removed.silent; required.char-device false; absence of disposition is lawful without per-detail exemptions. All-thirteen whitelist is RED even if all measured disposition rows pass. Do not change symlink accounting/removal. claims:38-69,91-94,137-145. |
| [ ] `census_rederived_ok` | v1:742-768,2094-2142,2295-2300 | Add score-time independent nonregular census re-derivation using frozen reader / unsquashfs -lln; compare full nonregular row sets BOTH directions, not counts or only device types. Missing/wrong/unrunnable reader -> exit 2 oracle_env_error; row mismatch -> not met. Preserve regular oracle derivation separately. claims:94-97. |
| [ ] `depth_gap_recorded` | v1:1360-1362,1464-1468,1830-1837,2368-2371 | Retain depth-limited structural accounting and expose each such gap's input_path and continuation_id in score receipt; boolean must enforce recording, not merely exist. Null relative_path does not identify stopped subtree; do not infer reached-device proof for unvisited subtrees. claims:58-62,97-98. |
| [ ] New booleans gate result | v1:435-441,2426-2428,2494-2496,2500-2508 | law_shape_ok, census_rederived_ok and depth_gap_recorded must be required in the appropriate carrier/global conjunction and failure diagnostics, not output-only. claims:91-98. |
| [ ] Offline rule-controls mode | v1:2222-2223,2278-2293,2391-2425,2555-2569 | Explicitly separate offline disposition verdict `gaps_ok AND nonregular_unpublished_ok`, over committed round-50 after.json envelopes + frozen oracle/nonregular tables (never run.json). Do not run REA, require vendor cache, claim full predicate success, or fabricate byte/provenance/freshness clauses. Controls pin R50 overrides and still recompute via v2 rule semantics. claims:115-133. |
| [ ] OLD/NEW/DN/JUNK controls | v1:3115-3123,4293-4301 | OLD R50 rule -> Cable pass, FRITZ!Box gaps fail, 2/4 exit 1. NEW law -> 4/4 exit 0. No-receipt do-nothing -> 1 or 2 never 0. All-required impossible syntactically valid junk -> 0/4 exit 1. NEW red or OLD 4 -> stop, not silently change scope. claims:120-147. |
| [ ] Law mutation controls | v1:4087-4095,4140-4158 (closest legacy defenses) | Add M1 all-thirteen whitelist required true -> RED on law shape; M2 new fourteenth device `dev/ttyS0 4:64` -> law GREEN, detail whitelist RED; M3 only247:0 required true -> old 2/4 miss; M4 strict-subset -> RED. Independently distinguish grammar validity, disposition and law-shape outcomes. claims:137-147. |
| [ ] Bounded retry classes | v1:1923-1926,2051-2088,2394-2404 | Up to 3 attempts for REA-own provider_timeout; up to 2 for execution_failure ONLY when failing diagnostic is ENOENT naming an inside-extraction-tree path; every attempt fresh extraction root; record attempt count and failing diagnostic including recovery. No arbitrary retryable flag, outside-tree ENOENT, other errors or malformed output treated as eligible. claims:105-114. |
| [ ] Exhaustion is falsifiable | v1:2397-2404,3168-3172 | Claims now say persisting eligible failure stays RED and any other rerun error red; deterministic inside-tree ENOENT frozen fixture must remain red after all attempts. Old timeout exhaustion was exit 2 rerun_env_error; don't silently preserve its old outcome as successful measurement or conflate RED with passed projection. L1 must freeze explicit timeout-exhaustion disposition in amendments if retaining 2, since claims' new retry paragraph says exhausted failure scores red. g7581 exhaustion misses, no narrowing. |
| [ ] Selftest port and additions | v1:2868-4594,4630-4832 | Preserve inventory below with legitimate round/date/pin-waiver expectation changes only; add law/census/depth/rescore/offline/retry/drift fixtures. Do not weaken every red to “any reason”: preserve named failing clause / expected reason assertions. Offline deterministic ENOENT control does not invoke REA. Actual selftest-rea is L1-only after wave. |
| [ ] Honest scope | v1:44-61,192-199,353-362 | Four existing carrier remeasurements, not four new carriers; observed device width 28 char-device rows (1 Cable/13 FRITZ per carrier), no measured fifo/socket/block rows; source-ground generalization and unreached depth limit stated. No fabricated runtime pass or pre-freeze full-predicate success. claims:54-69,77-85,126-133. |

## C. Known v1 wording/implementation traps to avoid cargo-culting

- v1:166-168 says handlers exactly one-element list; actual v1:2333-2334 accepts one or more all-equal SquashFS handlers and tests multi-root semantics. Preserve implementation invariant.
- v1:1765 says plus-extractor is plus-mime, but actual v1:1793-1813 also includes MD5/SHA1. Preserve actual projection bytes/keys, not abbreviated prose.
- v1:183-184 says exactly one disposition; v1:1555 accepts any nonempty gapped/removal count (only gap-vs-removal exclusivity is explicitly enforced). Do not describe this checklist as proving duplicate-record rejection. Tightening is a separate pre-freeze policy decision, not an existing v1 guarantee.
- v1:316-317 calls projection optional; carriers_spec v1:882-886 actually requires explicit plus-extractor. Preserve the enforced check.
- v1:4737-4743 selftest-rea's specimen carrier table omits mandatory `projection`; a literal copy cannot meet current carriers_spec. Preserve intended real green + fabricated-red coverage, not this defect; production run not exercised here.

## D. Complete static selftest case inventory

The following appendix is extracted from the v1 AST WITHOUT importing/executing the counter. It lists every literal named add/layout/path/runner/spec test and direct probe descriptor, with source line and expected arguments where applicable. Dynamic probe expansions are listed explicitly afterward. None is reported run or passed.

| v1 source | Test type | Exact case name | Expected invariant |
|---|---|---|---|
| v1:3115 | add | green (4 AVM carriers, fresh receipts, docs) | exit=0 |
| v1:3117 | add | do-nothing (freeze files only) | exit=1; want_fail='receipt_present' |
| v1:3118 | add | receipt missing (g7582) | exit=1; want_fail='receipt_present' |
| v1:3121 | add | receipt added at freeze | exit=1; want_fail='receipt_fresh' |
| v1:3122 | add | receipt added before freeze | exit=1; want_fail='receipt_fresh' |
| v1:3148 | add | oracle-only fabrication with re-minted evidence id | exit=1; want_fail='projection_ok' |
| v1:3152 | add | fabrication differing only in one published sha256 | exit=1; want_fail='projection_ok' |
| v1:3157 | add | fabrication differing only in an extra gap | exit=1; want_fail='gaps_ok' |
| v1:3160 | add | fabrication differing only in the diagnostics multiset | exit=1; want_fail='projection_ok' |
| v1:3163 | add | rerun yields no evidence object (REA ok=false) | exit=1; want_fail='projection_ok' |
| v1:3165 | add | rerun environment error (no npx) is unevaluable, never met | exit=2; reason='rerun_env_error' |
| v1:3171 | add | rerun hits REA provider_timeout (3 attempts) is unevaluable, never a projection verdict | exit=2; reason='rerun_env_error' |
| v1:3173 | add | subject digest names another carrier | exit=1; want_fail='subject_pin_ok' |
| v1:3190 | layout_case | standard-LE carrier (mkfs_time is a timestamp, no AVM marker) | exit=1; layout_ok false; paired layout probe |
| v1:3192 | layout_case | marker off by one (mkfs_time == bytes_used + 1) | exit=1; layout_ok false; paired layout probe |
| v1:3195 | layout_case | big-endian AVM-marker image (sqsh) is not the little-endian layout | exit=1; layout_ok false; paired layout probe |
| v1:3197 | layout_case | standard big-endian image (sqsh, no marker) | exit=1; layout_ok false; paired layout probe |
| v1:3201 | layout_case | hsqs magic over big-endian fields is not a little-endian image | exit=1; layout_ok false; paired layout probe |
| v1:3203 | layout_case | compression id 1 (gzip) is not the frozen xz | exit=1; layout_ok false; paired layout probe |
| v1:3205 | layout_case | compression id 2 (lzma; round 41 counted it as xz) | exit=1; layout_ok false; paired layout probe |
| v1:3207 | layout_case | compression id 6 (zstd) | exit=1; layout_ok false; paired layout probe |
| v1:3209 | layout_case | squashfs 3.0 major | exit=1; layout_ok false; paired layout probe |
| v1:3211 | layout_case | squashfs 4.1 minor | exit=1; layout_ok false; paired layout probe |
| v1:3213 | layout_case | bytes_used beyond the file | exit=1; layout_ok false; paired layout probe |
| v1:3216 | layout_case | inode table after the directory table | exit=1; layout_ok false; paired layout probe |
| v1:3219 | layout_case | directory table past bytes_used | exit=1; layout_ok false; paired layout probe |
| v1:3222 | layout_case | inode table at offset 0 | exit=1; layout_ok false; paired layout probe |
| v1:3224 | layout_case | shorter than a superblock | exit=1; layout_ok false; paired layout probe |
| v1:3226 | direct probe | layout probe: the frozen layout is accepted | see probe fields at cited line |
| v1:3237 | add | CTL-C1-4: a standard LE carrier planted under the genuine pin (carrier_pin_ok) | exit=1; want_fail='carrier_pin_ok' |
| v1:3239 | add | CTL-C1-4: a standard LE carrier planted under the genuine pin (layout_ok) | exit=1; want_fail='layout_ok' |
| v1:3244 | add | carrier listed but never committed | exit=1; want_fail='carrier_present' |
| v1:3247 | add | malformed oracle row | exit=1; want_fail='oracle_ok' |
| v1:3249 | add | malformed nonregular row | exit=1; want_fail='nonregular_ok' |
| v1:3253 | add | wrong operation (extract_filesystem) | exit=1; want_fail='operation_ok' |
| v1:3256 | add | provider is not unblob | exit=1; want_fail='operation_ok' |
| v1:3259 | add | failed chunk | exit=1; want_fail='chunks_ok' |
| v1:3263 | add | chunk handler is the BE handler (squashfs_v4_be) | exit=1; want_fail='handler_ok' |
| v1:3267 | add | chunk handler is squashfs_v3 | exit=1; want_fail='handler_ok' |
| v1:3271 | add | chunk handler is the bare prefix squashfs_v4 | exit=1; want_fail='handler_ok' |
| v1:3275 | add | one LE chunk and one BE chunk: every squashfs handler must be the frozen one | exit=1; want_fail='handler_ok' |
| v1:3283 | add | no squashfs chunk at all (padding only) | exit=1; want_fail='handler_ok' |
| v1:3287 | add | disallowed gap kind on a symlink entry | exit=1; want_fail='gaps_ok' |
| v1:3291 | add | gap on a path that is not a non-regular entry | exit=1; want_fail='gaps_ok' |
| v1:3295 | add | required gap missing (symlink materialised) | exit=1; want_fail='gaps_ok' |
| v1:3303 | add | escaping symlink published as a regular file | exit=1; want_fail='nonregular_unpublished_ok' |
| v1:3308 | add | oracle file missing from the published set | exit=1; want_fail='oracle_hits_ok' |
| v1:3311 | add | foreign scratch provenance (/kaidoku-r39/) | exit=1; want_fail='run_provenance_ok' |
| v1:3315 | add | provenance path climbs out with .. | exit=1; want_fail='run_provenance_ok' |
| v1:3319 | add | evidence id stale after an edit | exit=1; want_fail='evidence_id_ok' |
| v1:3325 | add | an extra regular file published under the extract root | exit=1; want_fail='oracle_hits_ok' |
| v1:3330 | add | a published file with the oracle sha256 but another size | exit=1; want_fail='oracle_hits_ok' |
| v1:3333 | add | oracle table row without the size column | exit=1; want_fail='oracle_ok' |
| v1:3337 | add | oracle table row with a non-numeric size | exit=1; want_fail='oracle_ok' |
| v1:3342 | add | oracle table row with a .. component | exit=1; want_fail='oracle_ok' |
| v1:3346 | add | receipt path with a .. component | exit=1; want_fail='path_shape_ok' |
| v1:3350 | add | a score receipt (counter_sha256) committed as the after-receipt | exit=1; want_fail='evidence_envelope_ok' |
| v1:3353 | add | a score receipt (exit_code) committed as the after-receipt | exit=1; want_fail='evidence_envelope_ok' |
| v1:3356 | add | provenance by substring only (/tmp/.../kaidoku-r50/...) | exit=1; want_fail='run_provenance_ok' |
| v1:3360 | add | provenance names the previous round scratch (kaidoku-r41) | exit=1; want_fail='run_provenance_ok' |
| v1:3364 | add | provenance is a relative path | exit=1; want_fail='run_provenance_ok' |
| v1:3368 | add | receipt made at max_depth 3 (the claim freezes depth 1) | exit=1; want_fail='parameters_ok' |
| v1:3371 | add | receipt made under a smaller output budget than the frozen one | exit=1; want_fail='parameters_ok' |
| v1:3374 | add | receipt without recorded parameters | exit=1; want_fail='parameters_ok' |
| v1:3377 | add | missing-extractor-dependency gap (sasquatch absent from the child PATH) | exit=1; want_fail='gaps_ok' |
| v1:3385 | add | a failed chunk reported by REA when sasquatch is absent | exit=1; want_fail='chunks_ok' |
| v1:3442 | runner_probe | node executes the package CLI at --pkg65 (no npx), frozen flags, FIXED_PATH, toolchain recorded | want_ok=True |
| v1:3445 | runner_probe | unblob that is not 26.6.4 is refused | want_ok=False; reason text='unblob version' |
| v1:3447 | runner_probe | a package that is not 6.5.0 is refused | want_ok=False; reason text='REA package version' |
| v1:3449 | runner_probe | a package without a bin entry is refused | want_ok=False; reason text='no rea-agents bin' |
| v1:3451 | runner_probe | a package whose bin entry is missing is refused | want_ok=False; reason text='is not a file' |
| v1:3464 | runner_probe | a shim sasquatch on the caller PATH is not resolved | want_ok=True |
| v1:3474 | add | the running counter is not the counter frozen at the freeze | exit=2; reason='counter_not_frozen' |
| v1:3477 | add | no counter at the freeze | exit=2; reason='counter_not_frozen' |
| v1:3483 | add | a receipt added pre-freeze on a side branch and re-added after the freeze, merged: not fresh | exit=1; want_fail='receipt_fresh' |
| v1:3491 | add | the same history with the receipt added only after the freeze is fresh | exit=0 |
| v1:3527 | add | oracle re-derivation equal to the frozen tables (green) | exit=0 |
| v1:3529 | add | frozen oracle table shrunk: the carrier holds a file the table omits | exit=1; want_fail='oracle_rederived_ok' |
| v1:3531 | add | frozen oracle table extended: a row the carrier does not hold | exit=1; want_fail='oracle_rederived_ok' |
| v1:3533 | add | frozen oracle row with another sha256 than the carrier holds | exit=1; want_fail='oracle_rederived_ok' |
| v1:3535 | add | frozen oracle row with another size than the carrier holds | exit=1; want_fail='oracle_rederived_ok' |
| v1:3537 | add | the carrier derives nothing while the table lists files | exit=1; want_fail='oracle_rederived_ok' |
| v1:3539 | add | unsquashfs cannot run: unevaluable, never green | exit=2; reason='oracle_env_error' |
| v1:3548 | direct probe | real unsquashfs re-derivation: lane image | see probe fields at cited line |
| v1:3562 | direct probe | real unsquashfs re-derivation equals the built tree | see probe fields at cited line |
| v1:3565 | direct probe | real unsquashfs re-derivation differs from a doctored table | see probe fields at cited line |
| v1:3568 | direct probe | real unsquashfs re-derivation leaves no scratch tree | see probe fields at cited line |
| v1:3607 | direct probe | real runner: sasquatch not on the child PATH | see probe fields at cited line |
| v1:3622 | add | four external carriers, bytes from --carrier-cache (green) | exit=0 |
| v1:3624 | add | four external carriers, empty cache | exit=1; want_fail='carrier_present' |
| v1:3626 | add | four external carriers, no --carrier-cache | exit=1; want_fail='carrier_present' |
| v1:3628 | add | four external carriers, cache bytes are not the pinned carrier | exit=1; want_fail='carrier_pin_ok' |
| v1:3634 | add | external carve length differs from bytes_used | exit=1; want_fail='carve_ok' |
| v1:3639 | add | rea package does not match the frozen pin | exit=2; reason='unevaluable' |
| v1:3643 | add | no rea-pkg pin at the freeze | exit=2; reason='unevaluable' |
| v1:3684 | probe | dir 1: regular usr/bin/busy vs symlink entry bin/busy | exact=False; legacy=True |
| v1:3686 | probe | dir 2: regular sbin/tool vs symlink entry usr/sbin/tool | exact=False; legacy=False |
| v1:3688 | probe | materialised symlink at its own entry path | exact=True; legacy=True |
| v1:3690 | probe | deeper-than-oracle file vs oracle row usr/bin/busy | exact=False; legacy=True |
| v1:3692 | probe | nested chunk root file vs outer-root table row lib/x | exact=False; legacy=True |
| v1:3694 | probe | plain oracle row | exact=True; legacy=True |
| v1:3705 | add | regular usr/bin/busy does not satisfy the symlink entry bin/busy | exit=0 |
| v1:3714 | add | regular sbin/tool does not satisfy the symlink entry usr/sbin/tool | exit=0 |
| v1:3722 | add | published regular at the symlink entry usr/sbin/tool is still caught | exit=1; want_fail='nonregular_unpublished_ok' |
| v1:3730 | add | deeper file with the oracle row sha256 does not publish oracle bin/busy | exit=1; want_fail='oracle_hits_ok' |
| v1:3742 | add | gap on usr/bin/busy does not resolve to the symlink entry bin/busy | exit=1; want_fail='gaps_ok' |
| v1:3773 | add | two chunks with oracle_root: the nested file is another namespace | exit=0 |
| v1:3777 | add | two squashfs roots without oracle_root fail closed | exit=1; want_fail='oracle_hits_ok' |
| v1:3783 | add | oracle_root that names no derivation root fails closed | exit=1; want_fail='oracle_hits_ok' |
| v1:3790 | add | two chunks: the nested chunk file does not publish outer-root row lib/x | exit=1; want_fail='oracle_hits_ok' |
| v1:3856 | add | padded carrier: the oracle resolves under the portion chunk directory | exit=0 |
| v1:3861 | add | padded carrier: the same rows one level too shallow score nothing | exit=1; want_fail='oracle_hits_ok' |
| v1:3917 | add | two AVM chunks in one receipt are ambiguous, not guessed | exit=1; want_fail='gaps_ok' |
| v1:3922 | direct probe | two portion chunk roots | see probe fields at cited line |
| v1:3954 | add | two handler chunks and no input handler chunk fail closed | exit=1; want_fail='gaps_ok' |
| v1:3959 | direct probe | ambiguous handler chunks | see probe fields at cited line |
| v1:3971 | add | a file outside the subject root is another namespace, not an extra | exit=0 |
| v1:3975 | direct probe | outside-namespace file | see probe fields at cited line |
| v1:3984 | add | receipt with no squashfs derivation edge fails closed | exit=1; want_fail='gaps_ok' |
| v1:4020 | add | a removal diagnostic is an admitted disposition for a symlink row | exit=0 |
| v1:4028 | add | a removal whose link lies outside the run root cannot be mapped | exit=1; want_fail='gaps_ok' |
| v1:4036 | add | a removal with a run root that is the filesystem root cannot be mapped | exit=1; want_fail='gaps_ok' |
| v1:4042 | add | an entry cannot be both gapped and removed | exit=1; want_fail='gaps_ok' |
| v1:4048 | add | a required symlink with no disposition fails | exit=1; want_fail='gaps_ok' |
| v1:4055 | add | a removal that resolves to no symlink row fails | exit=1; want_fail='gaps_ok' |
| v1:4071 | add | a removal naming a row of an unlisted kind fails | exit=1; want_fail='gaps_ok' |
| v1:4087 | add | a silent empty-target symlink is admitted with no record | exit=0 |
| v1:4093 | add | a symlink with a non-empty target cannot hide behind the silent allowance | exit=1; want_fail='gaps_ok' |
| v1:4135 | add | a rerun that removed a different link breaks the projection | exit=1; want_fail='projection_ok' |
| v1:4140 | add | relabelled previous-round pins (prior_pins) | exit=1; want_fail='carrier_fresh_ok' |
| v1:4146 | add | round-41 carrier table in the lane names two frozen pins | exit=1; want_fail='carrier_fresh_ok' |
| v1:4149 | add | round-49 carrier table in the lane names a frozen pin | exit=1; want_fail='carrier_fresh_ok' |
| v1:4153 | add | prior-pins document names a frozen pin | exit=1; want_fail='carrier_fresh_ok' |
| v1:4156 | add | prior_pins that are not 64-hex | exit=1; want_fail='b:carriers_spec_ok' |
| v1:4180 | probe_spec | external carrier without member_sha256 | want_ok=False; reason text='lacks member_sha256' |
| v1:4183 | probe_spec | external carrier without a positive carve length | want_ok=False; reason text='lacks length' |
| v1:4186 | probe_spec | external carrier with a member_sha256 | want_ok=True |
| v1:4188 | probe_spec | external carrier with a nested block and no nested.sha256 | want_ok=False; reason text='nested.sha256' |
| v1:4190 | probe_spec | external carrier with nested.sha256 | want_ok=True |
| v1:4192 | probe_spec | oracle_root is a relative path | want_ok=True |
| v1:4194 | probe_spec | oracle_root that is absolute | want_ok=False; reason text='oracle_root' |
| v1:4197 | probe_spec | target missing from carriers.json | want_ok=False; reason text='frozen target' |
| v1:4199 | probe_spec | target frozen at 3 | want_ok=False; reason text='frozen target' |
| v1:4200 | probe_spec | rea_parameters missing | want_ok=False; reason text='rea_parameters is not an object' |
| v1:4202 | probe_spec | rea_parameters at depth 3 | want_ok=False; reason text='max_depth' |
| v1:4205 | probe_spec | rea_parameters without a budget | want_ok=False; reason text='max_output_files' |
| v1:4208 | probe_spec | rea_parameters with a non-integer budget | want_ok=False; reason text='max_output_files' |
| v1:4211 | probe_spec | carrier ids compare case-insensitively | want_ok=True |
| v1:4213 | probe_spec | a fifth carrier id outside the claim | want_ok=False; reason text='carrier ids' |
| v1:4219 | add | carrier longer than its bytes_used (sloppy carve) | exit=1; want_fail='carve_ok' |
| v1:4223 | add | carrier bytes changed after freeze | exit=2; reason='frozen_path_changed' |
| v1:4226 | add | carrier bytes changed then restored | exit=2; reason='frozen_path_changed' |
| v1:4230 | add | oracle changed after freeze | exit=2; reason='frozen_path_changed' |
| v1:4233 | add | nonregular table changed after freeze | exit=2; reason='frozen_path_changed' |
| v1:4236 | add | carriers.json changed after freeze | exit=2; reason='frozen_path_changed' |
| v1:4239 | add | gap-rule.json changed after freeze | exit=2; reason='frozen_path_changed' |
| v1:4243 | add | gap-rule.json touched then restored | exit=2; reason='frozen_path_changed' |
| v1:4246 | add | counter edited after freeze | exit=2; reason='frozen_path_changed' |
| v1:4249 | add | claims edited after freeze | exit=2; reason='frozen_path_changed' |
| v1:4252 | add | a new file under tools/round-50 after the freeze | exit=2; reason='frozen_path_changed' |
| v1:4255 | add | rea-pkg pin edited after the freeze | exit=2; reason='frozen_path_changed' |
| v1:4258 | add | carried-over second reader edited after the freeze | exit=2; reason='frozen_path_changed' |
| v1:4261 | add | carried-over fetcher edited after the freeze | exit=2; reason='frozen_path_changed' |
| v1:4264 | add | xpin tool edited after the freeze | exit=2; reason='frozen_path_changed' |
| v1:4266 | add | oracle table first committed after the freeze is not frozen | exit=1; want_fail='b:frozen_tables_valid' |
| v1:4272 | add | frozen plan edited only by the merge commit itself (evil merge) | exit=2; reason='frozen_path_changed' |
| v1:4275 | add | frozen counter edited on a side branch and merged | exit=2; reason='frozen_path_changed' |
| v1:4279 | add | a clean merge touching nothing frozen does not trip the freeze walk | exit=0 |
| v1:4284 | add | frozen pin wrong (carrier untouched) | exit=1; want_fail='carrier_pin_ok' |
| v1:4287 | add | carriers.json drops a carrier at the freeze (target 4) | exit=1; want_fail='b:carriers_spec_ok' |
| v1:4290 | add | all four carriers read gzip (compression id 1) | exit=1; want_fail='layout_ok' |
| v1:4295 | add | gap rule omits the device kind | exit=1; want_fail='b:gap_rule_ok' |
| v1:4296 | add | gap rule is JSON but not an object at the freeze | exit=1; want_fail='b:frozen_tables_valid' |
| v1:4298 | add | gap rule names another claim | exit=1; want_fail='b:gap_rule_ok' |
| v1:4318 | add | structural gap within its frozen allowance | exit=0 |
| v1:4324 | add | structural gaps over the allowance | exit=1; want_fail='gaps_ok' |
| v1:4329 | add | path-less gap kind with no structural allowance | exit=1; want_fail='gaps_ok' |
| v1:4334 | add | structural gap kind that carries a path | exit=1; want_fail='gaps_ok' |
| v1:4342 | add | a frozen core profile (oracle-closed: it would accept the fabrication) is refused | exit=1; want_fail='b:carriers_spec_ok' |
| v1:4345 | add | the frozen plus-extractor profile refuses a projection-different fabrication | exit=1; want_fail='projection_ok' |
| v1:4347 | add | projection missing from carriers.json | exit=1; want_fail='b:carriers_spec_ok' |
| v1:4350 | add | plus-mime is not the frozen profile | exit=1; want_fail='b:carriers_spec_ok' |
| v1:4353 | add | unknown projection profile in carriers.json | exit=1; want_fail='b:carriers_spec_ok' |
| v1:4374 | add | rerun passes the frozen max_depth (1) to REA | exit=0 |
| v1:4376 | add | rerun passes the frozen output budgets to REA | exit=0 |
| v1:4378 | add | rerun takes the parameters from the frozen table, not from the receipt | exit=1; want_fail='parameters_ok' |
| v1:4383 | add | province has no Core section at all | exit=1; want_fail='b:province_core_section' |
| v1:4386 | add | province row outside the round-50 section | exit=1; want_fail='b:province_core_row' |
| v1:4389 | add | province row names the BE handler, not the LE one | exit=1; want_fail='b:province_core_row' |
| v1:4392 | add | province row without the handler in the first cell | exit=1; want_fail='b:province_core_row' |
| v1:4395 | add | province row that does not name the AVM marker | exit=1; want_fail='b:province_core_row' |
| v1:4398 | add | province row that names the round-41 AVM layout, not the marker | exit=1; want_fail='b:province_core_row' |
| v1:4401 | add | province row absent | exit=1; want_fail='b:province_core_row' |
| v1:4403 | add | province row cites another entry | exit=1; want_fail='b:province_core_row' |
| v1:4407 | add | frontier note absent | exit=1; want_fail='b:frontier_note' |
| v1:4409 | add | frontier note without the LE-AVM token | exit=1; want_fail='b:frontier_note' |
| v1:4414 | add | frontier note with the round-41 BE token (AVM BE) | exit=1; want_fail='b:frontier_note' |
| v1:4417 | add | frontier note with the AVM-LE spelling is accepted | exit=0 |
| v1:4419 | add | entry absent | exit=1; want_fail='b:entry_present' |
| v1:4420 | add | S-id substring S1120 | exit=1; want_fail='b:sourced' |
| v1:4422 | add | source row opened before the window | exit=1; want_fail='b:sourced' |
| v1:4425 | add | source row opened after the window | exit=1; want_fail='b:sourced' |
| v1:4428 | add | source row opened on the last day of the window (2026-10-29) | exit=0 |
| v1:4430 | add | used-by lacks the entry | exit=1; want_fail='b:sourced' |
| v1:4433 | add | coverage map lacks the stem | exit=1; want_fail='b:coverage_map_row' |

### Dynamic probe expansions and suite integrity

- v1:3181-3187: EACH of the 15 layout_case calls above also yields `layout probe: <case name>` and expected reason substring; v1:3226-3230 adds accepted frozen layout.
- v1:3572-3587: real unsquashfs environment probes expand into missing executable (`not executable`) and wrong version (`lacks 9.9.9`).
- v1:3793-3806: root probes: single chunk root -> firmware.bin_extract/single derivation; two roots with oracle_root -> named root/table hint; two roots without hint -> None/ambiguous.
- v1:3864-3873: portion chunk root and shallow-publish portion chunk both derive `firmware.bin_extract/4096-4500.squashfs_v4_le_extract`, regardless of published rows; source single derivation.
- v1:3922-3925: two portion chunk roots -> None/ambiguous. v1:3959-3962: ambiguous handler chunks -> None/ambiguous. v1:3975-3978: outside-namespace file -> unchanged single root.
- v1:3425-3427: each runner_probe is named `real runner: <case>`; v1:3585 prefixes unsquashfs environment names. These are probe wrappers, not additional omitted case families.
- v1:4440-4451: exact-vs-legacy path probes assert BOTH expected results and at least 3 discriminating cases; do not drop negative legacy expectations.
- v1:4452-4464: root result AND source checked; spec/runner/layout probes check want_ok AND required problem substring.
- v1:4465-4584: each fixture measures the final REV with its specified FREEZE, runner/cache/rederive; assert exact exit, exact reason when specified, and exact wanted failing clause when specified, not merely nonzero exit. Every isolated repository is top-level checked before commits and cleaned.
- v1:4586-4594: preserve suite output counts, green_ok/red_ok, path/root/spec probe results and failures; suite returns 0 only when failures empty. Static inventory is not an execution count.
- v1:4630-4832: separate real-REA suite (NOT RUN): independently extract oracle, first real run committed after freeze, second run scores green target 1, then reminted oracle-only fabrication must remain not met with projection_ok failure. Preserve image pin/layout, evidence id, projection diagnostics and cleanup; update round identity, mandatory table projection and new law/census fixtures as needed. No live execution is permitted to this seat.

### Inventory interpretation under R52

Keep every listed semantic test, but substitute R52 constants in round-sensitive fixtures. In particular v1:4425's 2026-10-30 opened date becomes a positive current-day case and the old accepted 2026-10-29 becomes an out-of-window negative; preserve both sides of the date-window check with new dates. Prior-pin negatives at v1:4140-4158 need non-allowlisted prior pins when the new explicit four-pin waiver is present; add separate green exactly-waived and red unwaived/overbroad-list cases rather than delete freshness tests. Production law-shape gating may require law-compliant base fixtures for symlink and legacy generic-device tests: isolate parser/disposition tests instead of weakening the production law to keep old fixtures green.

## E. Verification gaps and decisions for freeze owner

1. No counter, controls, REA, downloads, synthetic extractor probes, or tests were run. This is the requested source-to-contract checklist, not a v2 conformance verdict.
2. LSP device is unmounted; references/definition/diagnostics could not be obtained. Source references above are direct literal readings.
3. Retry wording needs explicit frozen semantics for timeout exhaustion (v1 exit 2 vs claims red); `re_scored_pins` is an allow-list policy, not a boolean fourth carrier clause. Freeze owner must avoid claiming four new booleans or silently changing exits.
4. New source/date/receipt/SCORECARD/LOG/registry obligations exceed v1's nine bindings; preserve original bindings AND derive new obligations. A green old `sourced` alone proves only one matching opened source row, not all named source citations.
5. No installed or updated tools; no scratch directory created, so no scratch cleanup outstanding. Only this seat's assigned artifact directory/report are written.
