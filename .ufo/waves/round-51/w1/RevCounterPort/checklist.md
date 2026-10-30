# R51 C1 counter v2 port-fidelity checklist

## Scope, axes, and evidence

Axes: semantic fidelity; freeze/receipt integrity; offline-control isolation; documentation-contract coverage; auditable test inventory.

Canonical authority: `plans/round-51-claims.md:22-104` (plus device-law grounding at 187-191). All `v1:L` references below mean **`tools/round-50/c1-counter.py:L`**, not the round-41 ancestor. All `plan:L` references mean **`plans/round-51-claims.md:L`**. Checkboxes are integration acceptance items, **not checks run or passed**.

The reviewed v1 and claims have no working-tree diff against assignment base `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`; exact command/exit/stdout hash/UTC and source hashes are in `source-review.json`; captured empty diff is `base.diff`. LSP unavailable: `read xd://lsp` returned “No such tool”; definition/caller/diagnostic semantic queries could not run. Source ranges, literal search, and AST enumeration are static evidence only. No v2 implementation was assigned for review; this is the integration checklist, not a v2 pass verdict. No tools installed; no scratch/heavy pass needed; no tests, controls, REA, downloads, or fixture mutations run.

## A. Preserve the scoring boundary and identity

- [ ] **Canonical execution identity** — v1:517-568, 2152-2163. Running counter bytes must equal the counter blob at FREEZE; absent/different => exit 2 `counter_not_frozen`. Resolve the v2 path, not v1. The production entry must still use the real runner; simulated rerun/rederive remain selftest-only (v1:2220-2223, 2567-2569, 4531-4534).
- [ ] **Git-object input boundary** — v1:460-470, 2165-2197, 2237-2243, 2273-2302, 2441-2482. Read freeze configuration and measured REV artifacts via `git show`, not uncommitted lane files; external firmware only from `<carrier-cache>/<pin>.bin`. Scratch/output only, never vendor bytes in lane. Honor `--work` before environment/default scratch, never `gettempdir()` (v1:476-487); clean work in finally (2436-2437, 2140-2142).
- [ ] **Score receipt file identity** — v1:517-568, 2592-2597. Every `--json-out` score carries absolute `counter` and actual `counter_sha256`; write, re-read, verify; identity failure => 2. `--verify-receipt` returns 0 matching, 1 missing/mismatched/invalid digest or missing/unreadable named counter, 2 unreadable/invalid JSON receipt (2536-2550). Maintain failure-receipt stamping too (2561-2562, 2578-2579).
- [ ] **Evidence-byte digest binding** — v1:2302-2311, 2433-2435. Hash the exact committed raw REA receipt bytes, expose `receipt_digest` per carrier and `evidence_digests[id]={path,sha256}`. Do not substitute an evidence-id or a JSON reserialization hash.
- [ ] **No score-as-evidence confusion** — v1:2320-2322. Presence of `counter_sha256` OR `exit_code` disqualifies a committed REA envelope (`evidence_envelope_ok=false`).
- [ ] **Evidence id bound to package** — v1:615-699, 2420-2425. Frozen first-present `rea-pkg.json` must bind package version 6.5.0 plus package.json and adjacent package-lock.json SHA256. Missing/malformed/mismatched pin, missing frozen XPIN/node, failed/malformed xpin output => unevaluable 2. Use frozen `tools/round-27/xpin-attribute.mjs` and the package's semanticProjection/digest, not a retyped substitute. Stored/recomputed ids equal and start `ev_`.
- [ ] **Subject equality independent of evidence id** — v1:2323-2325. `subject.digest.sha256 == frozen carrier pin`; re-minting another subject's envelope cannot bypass this clause.
- [ ] **Receipt first-add-after-freeze** — v1:1572-1593, 2313-2317. Enumerate EVERY adding commit using `git log -m --full-history --diff-filter=A --format=%H REV -- path`; require a nonempty successful list, and every add a STRICT descendant of FREEZE, never FREEZE itself. Keep `receipt_adds` and oldest `receipt_first_add`; no simplified-history/last-add shortcut. Side-branch pre-freeze add/re-add remains red (3482-3500). This requirement stays on production fresh R51 evidence, not historical control input.
- [ ] **Frozen inputs exist at FREEZE** — v1:2165-2193. Carrier spec and gap rule read there, JSON parse errors unevaluable; non-object carrier spec unevaluable; missing oracle/nonregular paths listed in spec make `frozen_tables_valid=false`. Later addition cannot bless an oracle. Keep `tables_absent_at_freeze`, `carriers_unchanged`, `gap_rule_unchanged`.
- [ ] **Freeze drift history, not just endpoints** — v1:1649-1723, 2199-2202, 2570-2580. Preserve merged-branch and evil-merge detection; M/D/R/T/U, additions in frozen prefix, re-addition of a path existing at freeze, and endpoint inequality all count. Edit-then-restore remains exit 2, named paths in `frozen_path_changed`. No scoring/rerun after drift preflight fails.
- [ ] **Conjunction cannot weaken** — v1:432-441, 2420-2435, 2494-2496. Carrier `matched` iff every listed CLAUSE is literally true; result met iff frozen tables unchanged, matched == 4, every required binding literally true. Keep failing clause lists, binding lists, truthful exit code and argv (2500-2508, 2581-2598). New documentation requirements must enter the conjunction, not only descriptive output.

## B. Preserve every per-carrier clause

| Required v2 clause | v1 implementation | Required unchanged behavior (except explicit R51 deltas below) |
|---|---|---|
| `carrier_present` | 2237-2247 | committed bytes at REV, or external cache bytes present |
| `carrier_pin_ok` | 2248-2249 | SHA256 of actual bytes equals frozen pin |
| `carrier_fresh_ok` | 1596-1646, 2250-2251 | exclude frozen prior pins; preserve prior-pin provenance sources; do NOT add R50's same four pins to exclusion for this declared re-run |
| `layout_ok` | 992-1056, 2252-2254 | little-endian `hsqs`, v4.0, xz id 4, `mkfs_time==bytes_used`, 96-byte SB; 0<used<=size and 0<inode<directory<=used; not an AVM authenticity discriminator |
| `carve_ok` | 2260-2271 | external carve length == bytes_used == byte length; committed byte length == bytes_used |
| `oracle_ok` | 704-739, 2273-2277 | nonempty unique paths, exactly path/hash/size columns, 64-hex hashes, nonnegative decimal sizes; normalized relative spelling (actual `strip_rel` at1310-1318 removes repeated `./` and leading `/` before validation; do not claim raw absolute-table-path rejection) |
| `oracle_rederived_ok` | 2094-2142, 2278-2293 | independent scoring-time regular-file set EXACTLY equals frozen (rel,hash,size) set in both directions; missing/wrong-version/unusable tool => 2, not green |
| `nonregular_ok` | 742-768, 2295-2300 | parses rel/kind/optional detail, tolerate header/empty table, reject duplicate (rel,kind) |
| `receipt_present` | 2302-2311 | committed receipt JSON object at actual selected path |
| `receipt_fresh` | 2313-2317 | EVERY add strict descendant of FREEZE |
| `evidence_envelope_ok` | 2320-2322 | no counter_sha256 or exit_code score keys |
| `subject_pin_ok` | 2323-2325 | subject SHA256 equals frozen carrier pin |
| `operation_ok` | 2326-2328 | `extract_firmware`, provider.id `unblob` |
| `handler_ok` | 1344-1352, 2329-2334 | nonempty SquashFS-family handlers; EVERY one exactly `squashfs_v4_le`; no prefix/default/mixed-BE escape |
| `chunks_ok` | 1354-1357, 2335 | no chunk has truthy extraction_failed |
| `oracle_hits_ok` | 1365-1424, 2336-2356 | every oracle (rel,hash,size) published under derivation-derived subject root, no extras in that namespace; nested roots excluded |
| `gaps_ok` | 1440-1569, 2360-2371 | data-driven nonregular disposition check; preserve all symlink, root, diagnostic, structural guards; change device requirement by law, not path-specific code |
| `nonregular_unpublished_ok` | 1427-1436, 2372-2375 | no regular publication at any exact nonregular path; do NOT disable this when devices become non-required |
| `path_shape_ok` | 1099-1177, 2376-2378 | all normalized receipt paths checked; no absolute/empty/dot/dotdot components or trailing slash; strip `$output/` only once |
| `run_provenance_ok` | 1061-1068, 2379 | absolute correct round prefix, not substring; reject dotdot; hashed parameters, not writer authentication |
| `parameters_ok` | 2380-2389 | exactly frozen max_depth / max_output_bytes / max_output_files, non-bool integers; max_depth 1 |
| `evidence_id_ok` | 659-699, 2420-2425 | genuine frozen-package recomputation equals stored ev_ id |
| `projection_ok` | 2391-2417 | real rerun of pinned bytes equals semantic projection; no receipt/pin/bytes => false, never skipped-green |

### Exact-path and gap invariants (preserve)

- [ ] v1:1134-1145, 1180-1235, 1289-1325: strip `$output/` once; root only from exact HANDLER derivation edges, one root or validated frozen `oracle_root`; ambiguous/no root fails closed. Whole-segment containment (`x_extract` never owns `x_extract2`). Never reconstruct root or satisfy oracle rows by suffix. Padded/carved root and nested namespaces preserved (1386-1399).
- [ ] v1:1244-1276: removal path comes from `report.link` under trusted parent of receipt output_directory, never filesystem-root trust; subject root located as whole segments. Foreign diagnostics cannot satisfy removals.
- [ ] v1:1499-1547: each path gap resolves to exactly one nonregular entry and allowed kind; pathless gaps require frozen structural allowance and bounded count; structural kind with path fails; missing-extractor-dependency without allowance fails; removal diagnostic resolves to an admitted kind, never a nonexistent/regular row, never both removal and gap.
- [ ] v1:1440-1455, 1549-1569: required rows need gap/removal or per-detail silent admission; `empty-target` matches empty third column, missing detail matches nothing, nonempty target cannot hide. Keep symlink requirements. **Actual-code caveat:** despite docstring “exactly one disposition”, lines 1555-1556 accept any nonempty same-family gap/removal count; don't describe duplicate rejection as an existing implementation guarantee. Exclusivity across gap/removal IS implemented at 1544-1545.

## C. Preserve rerun/projection/toolchain behavior

- [ ] v1:1968-2002, 2005-2088: node executes the package.json bin of the SAME `--pkg65` package used for id recomputation; version REA 6.5.0, unblob exactly 26.6.4, sasquatch/node resolved on FIXED_PATH. No npx/ambient resolver/second runtime, no sasquatch-v4be requirement. Record real paths, hashes and versions in `rerun_toolchain`; caller shim PATH must not win.
- [ ] v1:2031-2059: private per-carrier scratch input/output, REA_UNBLOB_COMMAND absolute, TMPDIR private, PATH fixed; flags `extract-firmware --format json --full-output` and FROZEN depth/budgets, not receipt-selected budgets. Failure to start, outer timeout, malformed/nonobject stdout => `rerun_env_error` 2.
- [ ] v1:1923-1926, 2051-2088, 2395-2404: at most three attempts ONLY for REA's own `provider_timeout`, removing output before retry; exhausted timeout => 2, not semantic projection miss. Other valid no-data responses make projection false => 1 if evaluable. Never general retries or fabrication fallback.
- [ ] v1:1753-1918: explicit frozen `plus-extractor` mandatory (882-886), not core/plus-mime/missing/unknown fallback acceptance. Preserve sorted multiset comparison of subject hash; files (root-normalized rel,sha,size,mime,md5,sha1); chunks (handler,offset,end,failed); gap kind/path/deps; unpublished kind/path; diagnostics (typename,root-mapped identity); derivation parent/child/handler; engine name/version; published_bytes; coverage. Preserve full equality (diff truncation is diagnostics only). Absolute run paths, ids/timestamps excluded; removal of another link changes projection.
- [ ] v1:2094-2142: fixed `/usr/bin/unsquashfs` 4.7.5, flags `-no-xattrs -no-progress -f -no-exit-code`; only regular nonsymlink files, exact SHA256/size walk, cleanup even on errors. Nonregular census is frozen-table input, not rederived by unprivileged extraction. No new claim that second-reader equality is recomputed: v1 docstring mentions it, but measure only rederives via unsquashfs.

## D. Preserve bindings, update exact markers, strengthen to the plan

The entire v1 required BINDINGS tuple is at **432-434**; exact implementation is **2439-2496**. None may disappear silently.

| Binding | v1 marker/check and location | demanded v2 marker/check |
|---|---|---|
| `province_core_section` | heading `## Round-50 additions to Core`, 379, 2443-2444 | exact `## Round-51 additions to Core` (plan:92-96) |
| `province_core_row` | first table cell token `squashfs_v4_le`; `AVM[ _-]marker` independently of entry-path text; cites full ENTRY, 426-428, 2445-2451 | same handler/marker discipline, full new ENTRY in R51 section |
| `frontier_note` | same line contains `Round-50 frontier note`, STEM, independent LE AVM/AVM LE token; remove STEM before token search, 2452-2456 | `Round-51 frontier note`, new STEM, independent LE token; additionally confirm LE `hsqs` no longer active Frontier (plan:96-97) |
| `entry_present` | ENTRY exists at REV, 2457-2458 | `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md` |
| `sourced` | `source:` lines only; exact bounded S-id tokens; SOURCES 11-cell row; opened field c[8] in window; used-by c[10] contains ENTRY or STEM, 2459-2478 | window exactly `2026-10-30`; require in-round source row(s) used-by entry AND citations S243/S244/S245/S249 (plan:94-95,187-191); old baseline rows do not replace new opens |
| `coverage_map_row` | `corpus/README.md` exact `## Coverage map` section table row contains STEM, 2479-2482 | same marker/section, new STEM; row must correspond to new entry |
| `carriers_spec_ok` | 872-987, 2483 | preserve target==4, four distinct expected ids/pins, chain and parameters validation; round claim tag R51-C1 |
| `gap_rule_ok` | valid rule plus every observed nonregular kind in allowed, 771-869, 2484-2489 | valid R51 law rule, no uncovered census kind; historical OLD rule evaluated only through explicit offline control route |
| `frozen_tables_valid` | config parses at freeze and all listed tables there, 2181-2193,2492 | same at R51 FREEZE; carried R50 oracle tables remain pinned/frozen inputs |

- [ ] **NEW plan-only bindings, no v1 equivalent:** plan:94-99 requires entry names fresh R51 receipts, all required source citations, LE removal from Frontier, `SCORECARD.md` coverage head **141/141** (map's 141st file this entry), and LOG entry. v1:432-434 and 2439-2496 do NOT inspect SCORECARD/LOG, fresh-receipt references, all four required source ids, nor active Frontier removal. Add enforceable binding checks to the final conjunction; merely porting the nine old boolean names is insufficient. Exact new binding names/LOG heading syntax are not fixed by the plan: do not invent an allegedly canonical marker.
- [ ] Registry obligation plan:103-104: exactly one `instrument-registry v2` row per new `.py`/`.sh` under tools/round-51, no unnamed code files. This is package integration acceptance, not an existing v1 binding.

## E. Exact change ledger (keep everything else)

| v1 site | Required R51 delta |
|---|---|
| 2-42,267-362; claim labels 792-793,875-876,2150,2557; selftest fixture tags | R50-C1/P50-C1 to consistent R51-C1/P51-C1 identity. Counter docstring and receipt label must carry same predicate sentence as plan:53-58, not a weaker old sentence. Historical control labels remain honest. |
| 374 CARRIERS | Use R51 frozen spec location (normally `tools/round-51/carriers.json`); plan does not explicitly name the carrier-spec path, so L1 must freeze chosen path and all real dependencies, not infer that R50 oracle paths must move. |
| 375 GAPRULE | `tools/round-51/gap-rule.json`; new rule expresses kind-level law, not thirteen-detail whitelist (plan:35-45,47). |
| 376 AFTERDIR;2235 rpath;2514-2531 CLI | Default `corpus/evidence/round-51/c1`; implement advertised `--receipts` argument and thread into path selection. Plan command uses `run.json` receipts (62-65,87-88), whereas v1 fallback is `<id>/after.json` and spec receipt overrides win. Ensure requested directory actually selects fresh `<id>/run.json` and cannot silently retain a frozen R50 explicit receipt path. |
| 377-380 | ENTRY=`corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md`; STEM=`2026-10-30-r51-avm-le-squashfs-core`; CORE_HEADING=`## Round-51 additions to Core`; FRONTIER_MARK=`Round-51 frontier note`. |
| 393,396-397;476-487; fixtures 2659,2845,3315-3317,3356-3367,4639,4805 | OPENED_DATES=`('2026-10-30',)`; scratch/provenance base `/fast/scratch/hyaku/kaidoku-r51/` (plan constant omits trailing slash; retain separator boundary); update all positive fixtures/help strings. Update out-of-window tests to remain genuinely outside new single-date window. Keep foreign/substring/dotdot negatives red. |
| 386-392,413-425 | Repoint R51-owned pin/package/fetcher/claims/counter/harness/control dependency paths and frozen prefix to R51; retain XPIN/second-reader/R50 oracle/nonregular dependencies actually read. Package pin must remain 6.5.0. Prior freshness exclusions retain earlier distinct carrier families; do NOT mechanically add R50 carriers to prior exclusions, since plan explicitly reruns those four. |
| 404 COUNTER_PATH | `tools/round-51/c1-counter.py`, including frozen-self identity, fixture files, diagnostics and help. |
| 381-382,394-395,398-405,409-412 | PRESERVE HANDLER, XPIN, target 4, exact id set, versions/layout constants, oracle flags and fixed child PATH unless separately justified by amended freeze. These are not round-number substitutions. |
| 771-869 and1440-1569 plus new gap rule | Preserve parser/disposition algorithm except law support needed. Kind-level non-required char-device/fifo/socket can use existing required=false semantics (1552-1554), not enumerated details. Keep allowed-kind coverage and nonregular-unpublished guard. Plan does not dictate a novel JSON field or broader treatment of block devices/directories; derive and freeze actual classes, not expand by assumption. |
| 2199-2202,1661-1723,2573-2574;4223-4278 | Preserve fail-closed drift and add/retain mutated frozen byte fixture demonstrating exit2 plus named path. **Source discrepancy:** contrary to plan:80-83 (“v1 only reported drift”), this exact v1 already raises FrozenPathChanged and contains exit2 tests. Re-freeze and port it, don't replace an existing hard gate with report-only code; amend historical explanation before freeze. |
| 2152-2153,2199 | Explicitly enforce REV descends from R51 FREEZE (plan:54). v1 validates both commit ids but has no global `is_ancestor(freeze,rev)` preflight; receipt-add ancestry is not a substitute for explicit revision contract. |
| 2517,2564-2566 vs plan:56-57 | Exact advertised predicate omits --pkg65 but v1 requires it. Resolve via deterministic 6.5.0 package discovery plus frozen-pin verification (existing find_rea_pkg at595-611), or amend predicate before freeze to include --pkg65. Do not publish an unexecutable counting command or select another runtime. |
| NEW offline entry / `c1-controls.py`; old main 2555-2569 | Add separate, explicitly labelled OFFLINE controls mode over committed R50 receipts+R50 tables, evaluating OLD versus NEW rule without fetching/rerunning firmware, id-reminting, or claiming fresh R51 evidence. No production `--no-rerun` success path: it remains exit2 `rerun_disabled`. Plan fixes outcome semantics, NOT flag spelling; L1 freezes interface and isolation. |

### Offline controls: all required outcomes and boundary checks

- [ ] plan:62-70: same committed four R50 `<id>/run.json` receipts and R50 oracle tables; exercise Cable AND FRITZ!Box. CTL-OLD **2/4, exit1**; CTL-NEW **4/4, exit0**; control receipt states offline consistency, never production coverage/promotion.
- [ ] v1 gap parser rejects nonmatching claim tag (792-793); v2 must deliberately support frozen R50 OLD rule in offline comparison without making arbitrary claim tags acceptable to production. Likewise old provenance prefix/receipt first-add and documentation checks cannot simply be relabelled and passed: define control applicability explicitly; production gates remain strict.
- [ ] plan:71-77: CTL-DN no receipts exits1 or2 never0; CTL-JUNK every kind required/impossible allowance => **0/4 exit1**. Requiring char-device with only247:0 stays red, and strict-subset-of-thirteen whitelist stays red. Do not mutate only Cable fixtures and call it both-class coverage.
- [ ] plan:78-79: CTL-NEW red OR CTL-OLD green OR expected-red mutation green => stop before live data; controls need real per-carrier gap computation, not hard-coded outcome counts or synthetic all-green rows.
- [ ] Offline mode cannot enter production receipt's `met_target`/identity/predicate flow as a fake rerun. Frozen R51 controls and control fixtures included in drift scope; controls receipts committed at freeze; no live REA during this build wave.

## F. Selftest preservation inventory

The appendix below is generated by Python AST parsing only (no module import or selftest execution). It lists every literal `add`, `layout_case`, `probe`, `probe_spec`, and `runner_probe` invocation within v1 selftest, including expected return/failing-clause arguments verbatim. Dynamic case-generation calls are marked and their expansions listed separately. Preserve each distinction in v2, updating round paths/dates/tags, never merely preserving a total count. Production no-rerun, identity verify and actual command failure paths also need CLI-level coverage; old measure-only tests are not proof of CLI exit behavior.

Additional inventory outside those literal calls:
- v1:3181-3187,3226-3230: every layout_case also a reason-sensitive direct layout probe, plus accepted-layout probe.
- v1:3542-3571: actual lane-built image independent-unsquashfs probes: matches built tree, differs doctored table, leaves no oracle scratch; image-build failure records failed positive probe. 3572-3587 expands missing-tool and wrong-version negative probes; 3589-3609 missing child sasquatch probe.
- v1:3793-3806: root probes single root; two with hint; two without hint. 3864-3873: portion root and shallow portion publication. 3920-3925: two portion roots ambiguous. 3957-3962: ambiguous handler roots. 3973-3978: outside-namespace publication leaves subject root unchanged.
- v1:4437-4464: assert exact vs legacy matcher expectations and >=3 discriminating path probes; root source/root equality; every spec probe expected boolean and reason text. Preserve these assertions, not just probe collection.
- v1:4465-4594: fixture top-level guard before commits; measure simulated runner/rederive only in fixture; assert requested exit AND reason AND named failing clause; counters/probe results/failures output; cleanup. Red on failed expectation.
- v1:4630-4832: separate --selftest-rea intended real two-run green then re-minted oracle-only fabrication projection-red; **NOT RUN here**. Existing fixture at4737-4743 omits mandatory projection field despite carriers_spec requiring it at882-886; cannot cite this dormant path as already green. Port with explicit plus-extractor if retained, without running REA in wave1.

Required R51 additions: law fixtures representing one-device and thirteen-device classes; OLD/NEW/JUNK/subset controls; mode isolation; `--receipts` routing; freeze-mutated-byte CLI exit2 naming path; REV ancestry; single-date source bindings and added landing bindings; updated --pkg65 command behavior. Claims fixes belong before freeze, never after failed frozen score.

### Literal selftest cases and direct probes

- [ ] **v1:3115-3116**

```python
add('green (4 AVM carriers, fresh receipts, docs)', [green_frozen, green_receipts],
        0, 0)
```

- [ ] **v1:3117-3117**

```python
add('do-nothing (freeze files only)', [frozen], 0, 1, want_fail='receipt_present')
```

- [ ] **v1:3118-3120**

```python
add('receipt missing (g7582)',
        [frozen, {k: v for k, v in good.items() if '/g7582/' not in k}], 0, 1,
        want_fail='receipt_present')
```

- [ ] **v1:3121-3121**

```python
add('receipt added at freeze', [{**frozen, **good}], 0, 1, want_fail='receipt_fresh')
```

- [ ] **v1:3122-3123**

```python
add('receipt added before freeze', [frozen, good, {}, {}], 2, 1,
        want_fail='receipt_fresh')
```

- [ ] **v1:3148-3150**

```python
add('oracle-only fabrication with re-minted evidence id',
        [frozen, relabel(green_envs, 'g7581', oracle_only)], 0, 1,
        want_fail='projection_ok')
```

- [ ] **v1:3152-3154**

```python
add('fabrication differing only in one published sha256',
        [frozen, relabel(green_envs, 'g7582', one_file_off)], 0, 1,
        want_fail='projection_ok')
```

- [ ] **v1:3157-3158**

```python
add('fabrication differing only in an extra gap',
        [frozen, relabel(green_envs, 'c6490', extra_gap)], 0, 1, want_fail='gaps_ok')
```

- [ ] **v1:3160-3162**

```python
add('fabrication differing only in the diagnostics multiset',
        [frozen, relabel(green_envs, 'c6430', diags_dropped)], 0, 1,
        want_fail='projection_ok')
```

- [ ] **v1:3163-3164**

```python
add('rerun yields no evidence object (REA ok=false)',
        [frozen, good], 0, 1, want_fail='projection_ok', runner=boom_runner)
```

- [ ] **v1:3165-3166**

```python
add('rerun environment error (no npx) is unevaluable, never met',
        [frozen, good], 0, 2, 'rerun_env_error', runner=env_boom_runner)
```

- [ ] **v1:3171-3172**

```python
add('rerun hits REA provider_timeout (3 attempts) is unevaluable, never a projection verdict',
        [frozen, good], 0, 2, 'rerun_env_error', runner=timeout_runner)
```

- [ ] **v1:3173-3175**

```python
add('subject digest names another carrier',
        [frozen, mutant('g7581', lambda e: e['subject']['digest'].__setitem__(
            'sha256', '2' * 64))], 0, 1, want_fail='subject_pin_ok')
```

- [ ] **v1:3183-3183**

```python
add(name, [lf, lr], 0, 1, want_fail='layout_ok')
```

- [ ] **v1:3190-3191**

```python
layout_case('standard-LE carrier (mkfs_time is a timestamp, no AVM marker)',
                sb_carrier(XZ_ID, b'g7581-std', marker=False), 'AVM marker absent')
```

- [ ] **v1:3192-3193**

```python
layout_case('marker off by one (mkfs_time == bytes_used + 1)',
                sb_carrier(XZ_ID, b'g7581-off', mkfs_value=641), 'AVM marker absent')
```

- [ ] **v1:3195-3196**

```python
layout_case('big-endian AVM-marker image (sqsh) is not the little-endian layout',
                sb_carrier(XZ_ID, b'g7581-be', big=True), 'not little-endian hsqs')
```

- [ ] **v1:3197-3199**

```python
layout_case('standard big-endian image (sqsh, no marker)',
                sb_carrier(XZ_ID, b'g7581-bestd', big=True, marker=False),
                'not little-endian hsqs')
```

- [ ] **v1:3201-3202**

```python
layout_case('hsqs magic over big-endian fields is not a little-endian image',
                hybrid, 'version')
```

- [ ] **v1:3203-3204**

```python
layout_case('compression id 1 (gzip) is not the frozen xz',
                sb_carrier(1, b'g7581-gz'), 'compression id 1')
```

- [ ] **v1:3205-3206**

```python
layout_case('compression id 2 (lzma; round 41 counted it as xz)',
                sb_carrier(2, b'g7581-lzma'), 'compression id 2')
```

- [ ] **v1:3207-3208**

```python
layout_case('compression id 6 (zstd)', sb_carrier(6, b'g7581-zstd'),
                'compression id 6')
```

- [ ] **v1:3209-3210**

```python
layout_case('squashfs 3.0 major', sb_carrier(XZ_ID, b'g7581-v3', major=3),
                'version 3.0')
```

- [ ] **v1:3211-3212**

```python
layout_case('squashfs 4.1 minor', sb_carrier(XZ_ID, b'g7581-v41', minor=1),
                'version 4.1')
```

- [ ] **v1:3213-3215**

```python
layout_case('bytes_used beyond the file',
                sb_carrier(XZ_ID, b'g7581-used', marker_value=0xFFFFFFF0),
                'bytes_used')
```

- [ ] **v1:3216-3218**

```python
layout_case('inode table after the directory table',
                sb_carrier(XZ_ID, b'g7581-order', its=128, dts=96),
                'in order')
```

- [ ] **v1:3219-3221**

```python
layout_case('directory table past bytes_used',
                sb_carrier(XZ_ID, b'g7581-dts', dts=639, marker_value=600),
                'in order')
```

- [ ] **v1:3222-3223**

```python
layout_case('inode table at offset 0', sb_carrier(XZ_ID, b'g7581-its0', its=0),
                'in order')
```

- [ ] **v1:3224-3225**

```python
layout_case('shorter than a superblock', sb_carrier(XZ_ID, b'g7581-short')[:64],
                'shorter than a 96-byte superblock')
```

- [ ] **v1:3237-3238**

```python
add('CTL-C1-4: a standard LE carrier planted under the genuine pin (carrier_pin_ok)',
        [plant_frozen, good], 0, 1, want_fail='carrier_pin_ok')
```

- [ ] **v1:3239-3240**

```python
add('CTL-C1-4: a standard LE carrier planted under the genuine pin (layout_ok)',
        [plant_frozen, good], 0, 1, want_fail='layout_ok')
```

- [ ] **v1:3244-3245**

```python
add('carrier listed but never committed', [no_carrier, good], 0, 1,
        want_fail='carrier_present')
```

- [ ] **v1:3247-3247**

```python
add('malformed oracle row', [bad_oracle, good], 0, 1, want_fail='oracle_ok')
```

- [ ] **v1:3249-3250**

```python
add('malformed nonregular row', [bad_nonreg, good], 0, 1,
        want_fail='nonregular_ok')
```

- [ ] **v1:3253-3255**

```python
add('wrong operation (extract_filesystem)',
        [frozen, mutant('g7581', lambda e: e.__setitem__('operation', 'extract_filesystem'))],
        0, 1, want_fail='operation_ok')
```

- [ ] **v1:3256-3258**

```python
add('provider is not unblob',
        [frozen, mutant('g7582', lambda e: e['provider'].__setitem__('id', 'binwalk'))],
        0, 1, want_fail='operation_ok')
```

- [ ] **v1:3259-3262**

```python
add('failed chunk',
        [frozen, mutant('c6490', lambda e: e['normalized_result']['chunks'][0]
                        .__setitem__('extraction_failed', True))], 0, 1,
        want_fail='chunks_ok')
```

- [ ] **v1:3263-3266**

```python
add('chunk handler is the BE handler (squashfs_v4_be)',
        [frozen, mutant('c6430', lambda e: [c.__setitem__('handler', 'squashfs_v4_be')
                                            for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
```

- [ ] **v1:3267-3270**

```python
add('chunk handler is squashfs_v3',
        [frozen, mutant('c6430', lambda e: [c.__setitem__('handler', 'squashfs_v3')
                                            for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
```

- [ ] **v1:3271-3274**

```python
add('chunk handler is the bare prefix squashfs_v4',
        [frozen, mutant('c6430', lambda e: [c.__setitem__('handler', 'squashfs_v4')
                                            for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
```

- [ ] **v1:3275-3282**

```python
add('one LE chunk and one BE chunk: every squashfs handler must be the frozen one',
        [frozen, mutant('c6430', lambda e: e['normalized_result']['chunks'].append(
            {'input_path': '$input', 'provider_id': 'p9',
             'range': {'offset': 4096, 'length': 100}, 'handler': 'squashfs_v4_be',
             'encrypted': False,
             'root_file_range': {'offset': 4096, 'length': 100},
             'extraction_failed': False}))],
        0, 1, want_fail='handler_ok')
```

- [ ] **v1:3283-3286**

```python
add('no squashfs chunk at all (padding only)',
        [frozen, mutant('c6430', lambda e: [c.__setitem__('handler', 'padding')
                                            for c in e['normalized_result']['chunks']])],
        0, 1, want_fail='handler_ok')
```

- [ ] **v1:3287-3290**

```python
add('disallowed gap kind on a symlink entry',
        [frozen, mutant('g7581', lambda e: e['normalized_result']['extraction_gaps'][0]
                        .__setitem__('kind', 'extractor-failure'))], 0, 1,
        want_fail='gaps_ok')
```

- [ ] **v1:3291-3294**

```python
add('gap on a path that is not a non-regular entry',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['extraction_gaps'].append({
            'kind': 'unpublished-entry', 'relative_path': 'firmware.bin_extract/var/ghost',
            'dependencies': []}))], 0, 1, want_fail='gaps_ok')
```

- [ ] **v1:3295-3302**

```python
add('required gap missing (symlink materialised)',
        [frozen, mutant('c6490', lambda e: (
            e['normalized_result']['extraction_gaps'].pop(),
            e['normalized_result']['unpublished_entries'].pop(),
            e['normalized_result']['files'].append({
                'relative_path': 'firmware.bin_extract/usr/lib/libfoo.so',
                'path': '/x/usr/lib/libfoo.so', 'size': 3, 'sha256': 'f' * 64})))],
        0, 1, want_fail='gaps_ok')
```

- [ ] **v1:3303-3307**

```python
add('escaping symlink published as a regular file',
        [frozen, mutant('g7581', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/usr/share/demo/escape',
            'path': '/x/escape', 'size': 3, 'sha256': 'e' * 64}))], 0, 1,
        want_fail='nonregular_unpublished_ok')
```

- [ ] **v1:3308-3310**

```python
add('oracle file missing from the published set',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['files'].pop())], 0, 1,
        want_fail='oracle_hits_ok')
```

- [ ] **v1:3311-3314**

```python
add('foreign scratch provenance (/kaidoku-r39/)',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r39/l1/K1-after'))],
        0, 1, want_fail='run_provenance_ok')
```

- [ ] **v1:3315-3318**

```python
add('provenance path climbs out with ..',
        [frozen, mutant('g7582', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r50/../kaidoku-r39/x'))],
        0, 1, want_fail='run_provenance_ok')
```

- [ ] **v1:3319-3323**

```python
add('evidence id stale after an edit',
        [frozen, mutant('c6430', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/extra.txt', 'path': '/x/extra.txt',
            'size': 1, 'sha256': 'd' * 64}), remint=False)], 0, 1,
        want_fail='evidence_id_ok')
```

- [ ] **v1:3325-3329**

```python
add('an extra regular file published under the extract root',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/var/extra.txt',
            'path': '/x/extra.txt', 'size': 5, 'sha256': 'd' * 64}))], 0, 1,
        want_fail='oracle_hits_ok')
```

- [ ] **v1:3330-3332**

```python
add('a published file with the oracle sha256 but another size',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['files'][0]
                        .__setitem__('size', 41))], 0, 1, want_fail='oracle_hits_ok')
```

- [ ] **v1:3333-3336**

```python
add('oracle table row without the size column',
        [{**frozen, f'{AFTERDIR}/g7581/oracle.tsv':
          ''.join(f'{rel}\t{h}\n' for rel, h, _s in spec_data['g7581']['files']).encode()},
         good], 0, 1, want_fail='oracle_ok')
```

- [ ] **v1:3337-3341**

```python
add('oracle table row with a non-numeric size',
        [{**frozen, f'{AFTERDIR}/g7581/oracle.tsv':
          ''.join(f'{rel}\t{h}\tbig\n' for rel, h, _s in
                  spec_data['g7581']['files']).encode()}, good], 0, 1,
        want_fail='oracle_ok')
```

- [ ] **v1:3342-3345**

```python
add('oracle table row with a .. component',
        [{**frozen, f'{AFTERDIR}/g7582/oracle.tsv':
          b'../etc/x\t' + fsha(3).encode() + b'\t40\n'}, good], 0, 1,
        want_fail='oracle_ok')
```

- [ ] **v1:3346-3349**

```python
add('receipt path with a .. component',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['files'].append({
            'relative_path': 'firmware.bin_extract/../etc/x', 'path': '/x/etc/x',
            'size': 5, 'sha256': 'd' * 64}))], 0, 1, want_fail='path_shape_ok')
```

- [ ] **v1:3350-3352**

```python
add('a score receipt (counter_sha256) committed as the after-receipt',
        [frozen, mutant('c6490', lambda e: e.__setitem__('counter_sha256', '0' * 64))],
        0, 1, want_fail='evidence_envelope_ok')
```

- [ ] **v1:3353-3355**

```python
add('a score receipt (exit_code) committed as the after-receipt',
        [frozen, mutant('c6490', lambda e: e.__setitem__('exit_code', 0))],
        0, 1, want_fail='evidence_envelope_ok')
```

- [ ] **v1:3356-3359**

```python
add('provenance by substring only (/tmp/.../kaidoku-r50/...)',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'output_directory', '/tmp/fast/scratch/hyaku/kaidoku-r50/x'))],
        0, 1, want_fail='run_provenance_ok')
```

- [ ] **v1:3360-3363**

```python
add('provenance names the previous round scratch (kaidoku-r41)',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'output_directory', '/fast/scratch/hyaku/kaidoku-r41/run-V4/extract'))],
        0, 1, want_fail='run_provenance_ok')
```

- [ ] **v1:3364-3367**

```python
add('provenance is a relative path',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'output_directory', 'fast/scratch/hyaku/kaidoku-r50/x'))],
        0, 1, want_fail='run_provenance_ok')
```

- [ ] **v1:3368-3370**

```python
add('receipt made at max_depth 3 (the claim freezes depth 1)',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__('max_depth', 3))],
        0, 1, want_fail='parameters_ok')
```

- [ ] **v1:3371-3373**

```python
add('receipt made under a smaller output budget than the frozen one',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__(
            'max_output_files', 10000))], 0, 1, want_fail='parameters_ok')
```

- [ ] **v1:3374-3376**

```python
add('receipt without recorded parameters',
        [frozen, mutant('g7581', lambda e: e['parameters'].pop('max_output_bytes'))],
        0, 1, want_fail='parameters_ok')
```

- [ ] **v1:3377-3384**

```python
add('missing-extractor-dependency gap (sasquatch absent from the child PATH)',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['extraction_gaps']
                        .append({'kind': 'missing-extractor-dependency',
                                 'input_path': '$output/firmware.bin_extract',
                                 'relative_path': None, 'handler': HANDLER,
                                 'dependencies': ['sasquatch'],
                                 'continuation_id': 'continuation-dep'}))],
        0, 1, want_fail='gaps_ok')
```

- [ ] **v1:3385-3388**

```python
add('a failed chunk reported by REA when sasquatch is absent',
        [frozen, mutant('g7582', lambda e: e['normalized_result']['chunks'][0]
                        .__setitem__('extraction_failed', True))],
        0, 1, want_fail='chunks_ok')
```

- [ ] **v1:3442-3444**

```python
runner_probe('node executes the package CLI at --pkg65 (no npx), frozen flags, '
                 'FIXED_PATH, toolchain recorded', stub_unblob('26.6.4'), stub_pkg(),
                 True, check=argv_ok)
```

- [ ] **v1:3445-3446**

```python
runner_probe('unblob that is not 26.6.4 is refused', stub_unblob('26.6.3'),
                 stub_pkg(), False, 'unblob version')
```

- [ ] **v1:3447-3448**

```python
runner_probe('a package that is not 6.5.0 is refused', stub_unblob('26.6.4'),
                 stub_pkg(version='6.4.0', name='old'), False, 'REA package version')
```

- [ ] **v1:3449-3450**

```python
runner_probe('a package without a bin entry is refused', stub_unblob('26.6.4'),
                 stub_pkg(bin_entry=None, name='nobin'), False, 'no rea-agents bin')
```

- [ ] **v1:3451-3453**

```python
runner_probe('a package whose bin entry is missing is refused',
                 stub_unblob('26.6.4'), stub_pkg(bin_entry='scripts/gone.mjs',
                                                 name='gone'), False, 'is not a file')
```

- [ ] **v1:3464-3469**

```python
runner_probe('a shim sasquatch on the caller PATH is not resolved', stub_unblob('26.6.4'),
                     stub_pkg(), True, cid='probe-shim',
                     check=lambda data, tc: (
                         not tc['sasquatch']['path'].startswith(shim)
                         and os.path.dirname(tc['sasquatch']['path']) in FIXED_PATH.split(':')
                         and data['path'] == FIXED_PATH and shim not in data['path']))
```

- [ ] **v1:3474-3476**

```python
add('the running counter is not the counter frozen at the freeze',
        [{**frozen, 'tools/round-50/c1-counter.py': b'# some other counter\n'}, good],
        0, 2, 'counter_not_frozen')
```

- [ ] **v1:3477-3479**

```python
add('no counter at the freeze',
        [{**frozen, 'tools/round-50/c1-counter.py': None}, good], 0, 2,
        'counter_not_frozen')
```

- [ ] **v1:3483-3490**

```python
add('a receipt added pre-freeze on a side branch and re-added after the freeze, '
        'merged: not fresh',
        [{'base.txt': b'b\n'},
         {'__ops__': [('git', 'checkout', '-q', '-b', 'side'), ('write', fh_good),
                      ('commit', 'P1'), ('git', 'checkout', '-q', '-')]},
         frozen, fh_good, {'__ops__': [('git', 'merge', '--no-ff', '-q', '-m', 'M',
                                        'side')]}],
        2, 1, want_fail='receipt_fresh')
```

- [ ] **v1:3491-3498**

```python
add('the same history with the receipt added only after the freeze is fresh',
        [{'base.txt': b'b\n'},
         {'__ops__': [('git', 'checkout', '-q', '-b', 'side'),
                      ('write', {'side.txt': b's\n'}), ('commit', 'S1'),
                      ('git', 'checkout', '-q', '-')]},
         frozen, fh_good, {'__ops__': [('git', 'merge', '--no-ff', '-q', '-m', 'M',
                                        'side')]}],
        2, 0)
```

- [ ] **v1:3527-3528**

```python
add('oracle re-derivation equal to the frozen tables (green)', [frozen, good], 0, 0,
        rederive=exact_rows)
```

- [ ] **v1:3529-3530**

```python
add('frozen oracle table shrunk: the carrier holds a file the table omits',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=extra_row)
```

- [ ] **v1:3531-3532**

```python
add('frozen oracle table extended: a row the carrier does not hold',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=short_rows)
```

- [ ] **v1:3533-3534**

```python
add('frozen oracle row with another sha256 than the carrier holds',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=wrong_sha)
```

- [ ] **v1:3535-3536**

```python
add('frozen oracle row with another size than the carrier holds',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=wrong_size)
```

- [ ] **v1:3537-3538**

```python
add('the carrier derives nothing while the table lists files',
        [frozen, good], 0, 1, want_fail='oracle_rederived_ok', rederive=nothing)
```

- [ ] **v1:3539-3540**

```python
add('unsquashfs cannot run: unevaluable, never green', [frozen, good], 0, 2,
        'oracle_env_error', rederive=no_unsquashfs)
```

- [ ] **v1:3622-3623**

```python
add('four external carriers, bytes from --carrier-cache (green)',
        [ext_frozen, ext_recs], 0, 0, cache=cache_ok)
```

- [ ] **v1:3624-3625**

```python
add('four external carriers, empty cache', [ext_frozen, ext_recs], 0, 1,
        want_fail='carrier_present', cache=cache_empty)
```

- [ ] **v1:3626-3627**

```python
add('four external carriers, no --carrier-cache', [ext_frozen, ext_recs], 0, 1,
        want_fail='carrier_present', cache=None)
```

- [ ] **v1:3628-3629**

```python
add('four external carriers, cache bytes are not the pinned carrier',
        [ext_frozen, ext_recs], 0, 1, want_fail='carrier_pin_ok', cache=cache_bad)
```

- [ ] **v1:3634-3636**

```python
add('external carve length differs from bytes_used',
        [{**ext_frozen, CARRIERS: json.dumps(ext_len, indent=1)}, ext_recs], 0, 1,
        want_fail='carve_ok', cache=cache_ok)
```

- [ ] **v1:3639-3642**

```python
add('rea package does not match the frozen pin',
        [{**frozen, 'tools/round-50/rea-pkg.json': json.dumps({
            'version': REA_VERSION, 'package_json_sha256': '0' * 64,
            'package_lock_sha256': '0' * 64})}, good], 0, 2, 'unevaluable')
```

- [ ] **v1:3643-3645**

```python
add('no rea-pkg pin at the freeze', [{**frozen, 'tools/round-50/rea-pkg.json': None,
                                          'tools/round-42/rea-pkg.json': None}, good],
        0, 2, 'unevaluable')
```

- [ ] **v1:3684-3685**

```python
probe('dir 1: regular usr/bin/busy vs symlink entry bin/busy',
          'firmware.bin_extract/usr/bin/busy', 'bin/busy', False, True)
```

- [ ] **v1:3686-3687**

```python
probe('dir 2: regular sbin/tool vs symlink entry usr/sbin/tool',
          'firmware.bin_extract/sbin/tool', 'usr/sbin/tool', False, False)
```

- [ ] **v1:3688-3689**

```python
probe('materialised symlink at its own entry path',
          'firmware.bin_extract/usr/sbin/tool', 'usr/sbin/tool', True, True)
```

- [ ] **v1:3690-3691**

```python
probe('deeper-than-oracle file vs oracle row usr/bin/busy',
          'firmware.bin_extract/x/usr/bin/busy', 'usr/bin/busy', False, True)
```

- [ ] **v1:3692-3693**

```python
probe('nested chunk root file vs outer-root table row lib/x',
          'firmware.bin_extract/core.sqsh_extract/lib/x', 'lib/x', False, True)
```

- [ ] **v1:3694-3695**

```python
probe('plain oracle row', 'firmware.bin_extract/var/info.txt', 'var/info.txt',
          True, True)
```

- [ ] **v1:3705-3706**

```python
add('regular usr/bin/busy does not satisfy the symlink entry bin/busy',
        [deep_file, deep_recs], 0, 0, runner=same_run(deep_recs))
```

- [ ] **v1:3714-3715**

```python
add('regular sbin/tool does not satisfy the symlink entry usr/sbin/tool',
        [short_file, short_recs], 0, 0, runner=same_run(short_recs))
```

- [ ] **v1:3722-3724**

```python
add('published regular at the symlink entry usr/sbin/tool is still caught',
        [materialised, materialised_recs], 0, 1,
        want_fail='nonregular_unpublished_ok', runner=same_run(materialised_recs))
```

- [ ] **v1:3730-3732**

```python
add('deeper file with the oracle row sha256 does not publish oracle bin/busy',
        [oracle_shadow, oracle_shadow_recs], 0, 1,
        want_fail='oracle_hits_ok', runner=same_run(oracle_shadow_recs))
```

- [ ] **v1:3742-3744**

```python
add('gap on usr/bin/busy does not resolve to the symlink entry bin/busy',
        [wrong_gap, wrong_gap_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(wrong_gap_recs))
```

- [ ] **v1:3773-3774**

```python
add('two chunks with oracle_root: the nested file is another namespace',
        [two_ok, two_ok_recs], 0, 0, runner=same_run(two_ok_recs))
```

- [ ] **v1:3777-3779**

```python
add('two squashfs roots without oracle_root fail closed',
        [two_amb_frozen, two_amb_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(two_amb_recs))
```

- [ ] **v1:3783-3785**

```python
add('oracle_root that names no derivation root fails closed',
        [two_wrong_frozen, two_wrong_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(two_wrong_recs))
```

- [ ] **v1:3790-3792**

```python
add('two chunks: the nested chunk file does not publish outer-root row lib/x',
        [two_shadow, two_shadow_recs], 0, 1, want_fail='oracle_hits_ok',
        runner=same_run(two_shadow_recs))
```

- [ ] **v1:3856-3857**

```python
add('padded carrier: the oracle resolves under the portion chunk directory',
        [pad_frozen, pad_recs], 0, 0, runner=same_run(pad_recs))
```

- [ ] **v1:3861-3863**

```python
add('padded carrier: the same rows one level too shallow score nothing',
        [pad_shallow_frozen, pad_shallow_recs], 0, 1,
        want_fail='oracle_hits_ok', runner=same_run(pad_shallow_recs))
```

- [ ] **v1:3917-3919**

```python
add('two AVM chunks in one receipt are ambiguous, not guessed',
        [two_frozen, two_recs2], 0, 1, want_fail='gaps_ok',
        runner=same_run(two_recs2))
```

- [ ] **v1:3954-3956**

```python
add('two handler chunks and no input handler chunk fail closed',
        [amb_frozen, amb_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(amb_recs))
```

- [ ] **v1:3971-3972**

```python
add('a file outside the subject root is another namespace, not an extra',
        [mix_frozen, mix_recs], 0, 0, runner=same_run(mix_recs))
```

- [ ] **v1:3984-3986**

```python
add('receipt with no squashfs derivation edge fails closed',
        [nod_frozen, nod_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(nod_recs))
```

- [ ] **v1:4020-4021**

```python
add('a removal diagnostic is an admitted disposition for a symlink row',
        [rem_frozen, rem_recs], 0, 0, runner=same_run(rem_recs))
```

- [ ] **v1:4028-4030**

```python
add('a removal whose link lies outside the run root cannot be mapped',
        [foreign_frozen, foreign_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(foreign_recs))
```

- [ ] **v1:4036-4038**

```python
add('a removal with a run root that is the filesystem root cannot be mapped',
        [nopar_frozen, nopar_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(nopar_recs))
```

- [ ] **v1:4042-4044**

```python
add('an entry cannot be both gapped and removed',
        [both_frozen, both_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(both_recs))
```

- [ ] **v1:4048-4050**

```python
add('a required symlink with no disposition fails',
        [none_frozen, none_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(none_recs))
```

- [ ] **v1:4055-4057**

```python
add('a removal that resolves to no symlink row fails',
        [stray_frozen, stray_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(stray_recs))
```

- [ ] **v1:4071-4073**

```python
add('a removal naming a row of an unlisted kind fails',
        [dev_frozen, dev_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(dev_recs))
```

- [ ] **v1:4087-4088**

```python
add('a silent empty-target symlink is admitted with no record',
        [sil_frozen, sil_recs], 0, 0, runner=same_run(sil_recs))
```

- [ ] **v1:4093-4095**

```python
add('a symlink with a non-empty target cannot hide behind the silent allowance',
        [sil2_frozen, sil2_recs], 0, 1, want_fail='gaps_ok',
        runner=same_run(sil2_recs))
```

- [ ] **v1:4135-4137**

```python
add('a rerun that removed a different link breaks the projection',
        [proj_frozen, proj_recs], 0, 1, want_fail='projection_ok',
        runner=other_removal_runner)
```

- [ ] **v1:4140-4142**

```python
add('relabelled previous-round pins (prior_pins)',
        [{**frozen, CARRIERS: spec_json(prior_pins=[pins[k] for k in ids])}, good],
        0, 1, want_fail='carrier_fresh_ok')
```

- [ ] **v1:4146-4148**

```python
add('round-41 carrier table in the lane names two frozen pins',
        [{**frozen, '.ufo/waves/round-41/c1/carriers.json': prior_tbl}, good], 0, 1,
        want_fail='carrier_fresh_ok')
```

- [ ] **v1:4149-4152**

```python
add('round-49 carrier table in the lane names a frozen pin',
        [{**frozen, 'tools/round-49/carriers.json': json.dumps(
            {'carriers': [{'id': 'v1le', 'sha256': pins['g7582']}]})}, good], 0, 1,
        want_fail='carrier_fresh_ok')
```

- [ ] **v1:4153-4155**

```python
add('prior-pins document names a frozen pin',
        [{**frozen, 'tools/round-42/prior-pins.json': json.dumps(
            {'pins': [pins['c6490']]})}, good], 0, 1, want_fail='carrier_fresh_ok')
```

- [ ] **v1:4156-4158**

```python
add('prior_pins that are not 64-hex',
        [{**frozen, CARRIERS: spec_json(prior_pins=['not-a-pin'])}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
```

- [ ] **v1:4180-4182**

```python
probe_spec('external carrier without member_sha256',
               spec_json(external='g7581', external_drop=('member_sha256',)),
               False, 'lacks member_sha256')
```

- [ ] **v1:4183-4185**

```python
probe_spec('external carrier without a positive carve length',
               spec_json(external='g7581', external_drop=('length',)),
               False, 'lacks length')
```

- [ ] **v1:4186-4187**

```python
probe_spec('external carrier with a member_sha256',
               spec_json(external='g7581'), True)
```

- [ ] **v1:4188-4189**

```python
probe_spec('external carrier with a nested block and no nested.sha256',
               nested_spec(drop=True), False, 'nested.sha256')
```

- [ ] **v1:4190-4191**

```python
probe_spec('external carrier with nested.sha256',
               nested_spec(drop=False), True)
```

- [ ] **v1:4192-4193**

```python
probe_spec('oracle_root is a relative path',
               spec_json(oracle_root={'g7581': 'firmware.bin_extract'}), True)
```

- [ ] **v1:4194-4196**

```python
probe_spec('oracle_root that is absolute',
               spec_json(oracle_root={'g7581': '/firmware.bin_extract'}), False,
               'oracle_root')
```

- [ ] **v1:4197-4198**

```python
probe_spec('target missing from carriers.json',
               spec_json(omit=('target',)), False, 'frozen target')
```

- [ ] **v1:4199-4199**

```python
probe_spec('target frozen at 3', spec_json(target=3), False, 'frozen target')
```

- [ ] **v1:4200-4201**

```python
probe_spec('rea_parameters missing', spec_json(omit=('rea_parameters',)), False,
               'rea_parameters is not an object')
```

- [ ] **v1:4202-4204**

```python
probe_spec('rea_parameters at depth 3',
               spec_json(rea=dict(FIXTURE_REA_PARAMETERS, max_depth=3)), False,
               'max_depth')
```

- [ ] **v1:4205-4207**

```python
probe_spec('rea_parameters without a budget',
               spec_json(rea={'max_depth': 1, 'max_output_bytes': 1}), False,
               'max_output_files')
```

- [ ] **v1:4208-4210**

```python
probe_spec('rea_parameters with a non-integer budget',
               spec_json(rea=dict(FIXTURE_REA_PARAMETERS, max_output_files='many')),
               False, 'max_output_files')
```

- [ ] **v1:4211-4212**

```python
probe_spec('carrier ids compare case-insensitively',
               spec_json().replace('"g7581"', '"G7581"'), True)
```

- [ ] **v1:4213-4214**

```python
probe_spec('a fifth carrier id outside the claim',
               spec_json().replace('"g7581"', '"z9999"'), False, 'carrier ids')
```

- [ ] **v1:4219-4220**

```python
add('carrier longer than its bytes_used (sloppy carve)',
        [o_frozen, o_recs], 0, 1, want_fail='carve_ok', runner=same_run(o_recs))
```

- [ ] **v1:4223-4225**

```python
add('carrier bytes changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/g7581/carrier.sqsh': b'changed carrier\n'}],
        0, 2, 'frozen_path_changed')
```

- [ ] **v1:4226-4229**

```python
add('carrier bytes changed then restored',
        [frozen, {**good, f'{AFTERDIR}/g7581/carrier.sqsh': b'changed carrier\n'},
         {**good, f'{AFTERDIR}/g7581/carrier.sqsh': carriers['g7581']}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4230-4232**

```python
add('oracle changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/g7582/oracle.tsv': oracle_tsv('g7582') + b'extra.txt\t'
          + b'3' * 64 + b'\t1\n'}], 0, 2, 'frozen_path_changed')
```

- [ ] **v1:4233-4235**

```python
add('nonregular table changed after freeze',
        [frozen, {**good, f'{AFTERDIR}/c6490/nonregular.tsv': b'usr/lib/libfoo.so\tsymlink\n'
         b'usr/lib/extra\tsymlink\n'}], 0, 2, 'frozen_path_changed')
```

- [ ] **v1:4236-4238**

```python
add('carriers.json changed after freeze',
        [frozen, {**good, CARRIERS: spec_json(drop=('c6430',))}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4239-4242**

```python
add('gap-rule.json changed after freeze',
        [frozen, {**good, GAPRULE: json.dumps({'claim': 'R50-C1', 'allowed': {
            'symlink': ['unpublished-entry']}}).encode()}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4243-4245**

```python
add('gap-rule.json touched then restored',
        [frozen, {**good, GAPRULE: b'{}\n'}, {**good, GAPRULE: rule.encode()}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4246-4248**

```python
add('counter edited after freeze',
        [frozen, {**good, 'tools/round-50/c1-counter.py': b'#!/usr/bin/env python3\n'
         b'print(0)\n'}], 0, 2, 'frozen_path_changed')
```

- [ ] **v1:4249-4251**

```python
add('claims edited after freeze',
        [frozen, {**good, 'plans/round-50-claims.md': b'# new plan\n'}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4252-4254**

```python
add('a new file under tools/round-50 after the freeze',
        [frozen, {**good, 'tools/round-50/extra.py': b'print(1)\n'}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4255-4257**

```python
add('rea-pkg pin edited after the freeze',
        [frozen, {**good, 'tools/round-50/rea-pkg.json': b'{}\n'}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4258-4260**

```python
add('carried-over second reader edited after the freeze',
        [frozen, {**good, 'tools/round-41/sqfs-list.py': b'# edited\n'}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4261-4263**

```python
add('carried-over fetcher edited after the freeze',
        [frozen, {**good, 'tools/round-41/fetch-vendor.py': b'# edited\n'}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4264-4265**

```python
add('xpin tool edited after the freeze',
        [frozen, {**good, XPIN: b'// edited\n'}], 0, 2, 'frozen_path_changed')
```

- [ ] **v1:4266-4269**

```python
add('oracle table first committed after the freeze is not frozen',
        [{**frozen, f'{AFTERDIR}/g7582/oracle.tsv': None},
         {**good, f'{AFTERDIR}/g7582/oracle.tsv': oracle_tsv('g7582')}], 0, 1,
        want_fail='b:frozen_tables_valid')
```

- [ ] **v1:4272-4274**

```python
add('frozen plan edited only by the merge commit itself (evil merge)',
        [frozen, {'__merge__': {'plans/round-50-claims.md': b'# new plan\n'}}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4275-4278**

```python
add('frozen counter edited on a side branch and merged',
        [frozen, {'__merge__': {}, '__side__': {'tools/round-50/c1-counter.py':
                                                 b'print(0)\n'}}], 0, 2,
        'frozen_path_changed')
```

- [ ] **v1:4279-4280**

```python
add('a clean merge touching nothing frozen does not trip the freeze walk',
        [frozen, {**good}, {'__merge__': {'notes.txt': b'n\n'}}], 0, 0)
```

- [ ] **v1:4284-4286**

```python
add('frozen pin wrong (carrier untouched)',
        [{**frozen, CARRIERS: spec_json(pin_map=bad_pins)}, good], 0, 1,
        want_fail='carrier_pin_ok')
```

- [ ] **v1:4287-4289**

```python
add('carriers.json drops a carrier at the freeze (target 4)',
        [{**frozen, CARRIERS: spec_json(drop=('g7582',))}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
```

- [ ] **v1:4290-4292**

```python
add('all four carriers read gzip (compression id 1)',
        list(build(blob_over={k: sb_carrier(1, ('%s-gzip' % k).encode())
                              for k in ids})), 0, 1, want_fail='layout_ok')
```

- [ ] **v1:4295-4295**

```python
add('gap rule omits the device kind', [f2, r2], 0, 1, want_fail='b:gap_rule_ok')
```

- [ ] **v1:4296-4297**

```python
add('gap rule is JSON but not an object at the freeze',
        list(build(rule_text='[]')), 0, 1, want_fail='b:frozen_tables_valid')
```

- [ ] **v1:4298-4301**

```python
add('gap rule names another claim',
        list(build(rule_text=json.dumps({'claim': 'R39-C1', 'allowed': {
            'symlink': ['unpublished-entry'], 'device': ['unpublished-entry']}}))),
        0, 1, want_fail='b:gap_rule_ok')
```

- [ ] **v1:4318-4321**

```python
add('structural gap within its frozen allowance',
        [st_frozen, st_receipts], 0, 0,
        runner=mk_same_runner({**green_envs, 'g7581': json.loads(st_receipts[
            receipt_path('g7581')])}))
```

- [ ] **v1:4324-4325**

```python
add('structural gaps over the allowance', [st2_frozen, st2_receipts], 0, 1,
        want_fail='gaps_ok')
```

- [ ] **v1:4329-4330**

```python
add('path-less gap kind with no structural allowance', [st3_frozen, st3_receipts],
        0, 1, want_fail='gaps_ok')
```

- [ ] **v1:4334-4335**

```python
add('structural gap kind that carries a path', [st4_frozen, st4_receipts], 0, 1,
        want_fail='gaps_ok')
```

- [ ] **v1:4342-4343**

```python
add('a frozen core profile (oracle-closed: it would accept the fabrication) is refused',
        [core_frozen, core_receipts], 0, 1, want_fail='b:carriers_spec_ok')
```

- [ ] **v1:4345-4346**

```python
add('the frozen plus-extractor profile refuses a projection-different fabrication',
        [plus_frozen, plus_receipts], 0, 1, want_fail='projection_ok')
```

- [ ] **v1:4347-4349**

```python
add('projection missing from carriers.json',
        [{**frozen, CARRIERS: spec_json(omit=('projection',))}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
```

- [ ] **v1:4350-4352**

```python
add('plus-mime is not the frozen profile',
        [{**frozen, CARRIERS: spec_json(projection='plus-mime')}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
```

- [ ] **v1:4353-4355**

```python
add('unknown projection profile in carriers.json',
        [{**frozen, CARRIERS: spec_json(projection='plus-everything')}, good], 0, 1,
        want_fail='b:carriers_spec_ok')
```

- [ ] **v1:4374-4375**

```python
add('rerun passes the frozen max_depth (1) to REA', [frozen, good], 0, 0,
        runner=depth_runner(1))
```

- [ ] **v1:4376-4377**

```python
add('rerun passes the frozen output budgets to REA', [frozen, good], 0, 0,
        runner=budget_runner)
```

- [ ] **v1:4378-4380**

```python
add('rerun takes the parameters from the frozen table, not from the receipt',
        [frozen, mutant('g7581', lambda e: e['parameters'].__setitem__('max_depth', 3))],
        0, 1, want_fail='parameters_ok', runner=depth_runner(1))
```

- [ ] **v1:4383-4385**

```python
add('province has no Core section at all',
        [{**frozen, 'PROVINCE.md': '# P\n\n## Next\n- x\n'}, good], 0, 1,
        want_fail='b:province_core_section')
```

- [ ] **v1:4386-4388**

```python
add('province row outside the round-50 section',
        [{**frozen, 'PROVINCE.md': _province(heading='## Round-49 additions to Core')},
         good], 0, 1, want_fail='b:province_core_row')
```

- [ ] **v1:4389-4391**

```python
add('province row names the BE handler, not the LE one',
        [{**frozen, 'PROVINCE.md': _province(cell='`squashfs_v4_be`')}, good], 0, 1,
        want_fail='b:province_core_row')
```

- [ ] **v1:4392-4394**

```python
add('province row without the handler in the first cell',
        [{**frozen, 'PROVINCE.md': _province(cell='`squashfs_v4`')}, good], 0, 1,
        want_fail='b:province_core_row')
```

- [ ] **v1:4395-4397**

```python
add('province row that does not name the AVM marker',
        [{**frozen, 'PROVINCE.md': _province(layout='little-endian squashfs')}, good],
        0, 1, want_fail='b:province_core_row')
```

- [ ] **v1:4398-4400**

```python
add('province row that names the round-41 AVM layout, not the marker',
        [{**frozen, 'PROVINCE.md': _province(layout='AVM layout')}, good], 0, 1,
        want_fail='b:province_core_row')
```

- [ ] **v1:4401-4402**

```python
add('province row absent', [{**frozen, 'PROVINCE.md': _province(row=False)}, good],
        0, 1, want_fail='b:province_core_row')
```

- [ ] **v1:4403-4406**

```python
add('province row cites another entry',
        [{**frozen, 'PROVINCE.md': _province(
            cited='corpus/knowledge/2026-10-26-r41-avm-be-squashfs-core.md')}, good],
        0, 1, want_fail='b:province_core_row')
```

- [ ] **v1:4407-4408**

```python
add('frontier note absent', [{**frozen, 'PROVINCE.md': _province(note=False)}, good],
        0, 1, want_fail='b:frontier_note')
```

- [ ] **v1:4409-4413**

```python
add('frontier note without the LE-AVM token',
        [{**frozen, 'PROVINCE.md': (f'# P\n\n{CORE_HEADING}\n\n| Surface | Layout | a | Entry |\n'
                                    f'|---|---|---|---|\n| `squashfs_v4_le` | AVM marker | x | '
                                    f'`{ENTRY}` |\n\n## Next\n- {FRONTIER_MARK}: `{STEM}`.\n')},
         good], 0, 1, want_fail='b:frontier_note')
```

- [ ] **v1:4414-4416**

```python
add('frontier note with the round-41 BE token (AVM BE)',
        [{**frozen, 'PROVINCE.md': _province(token='AVM BE')}, good], 0, 1,
        want_fail='b:frontier_note')
```

- [ ] **v1:4417-4418**

```python
add('frontier note with the AVM-LE spelling is accepted',
        [{**frozen, 'PROVINCE.md': _province(token='AVM-LE')}, good], 0, 0)
```

- [ ] **v1:4419-4419**

```python
add('entry absent', [{**frozen, ENTRY: None}, good], 0, 1, want_fail='b:entry_present')
```

- [ ] **v1:4420-4421**

```python
add('S-id substring S1120', [{**frozen, ENTRY: _entry('S1120')}, good], 0, 1,
        want_fail='b:sourced')
```

- [ ] **v1:4422-4424**

```python
add('source row opened before the window',
        [{**frozen, 'corpus/SOURCES.md': _registry(opened='2026-10-27')}, good], 0, 1,
        want_fail='b:sourced')
```

- [ ] **v1:4425-4427**

```python
add('source row opened after the window',
        [{**frozen, 'corpus/SOURCES.md': _registry(opened='2026-10-30')}, good], 0, 1,
        want_fail='b:sourced')
```

- [ ] **v1:4428-4429**

```python
add('source row opened on the last day of the window (2026-10-29)',
        [{**frozen, 'corpus/SOURCES.md': _registry(opened='2026-10-29')}, good], 0, 0)
```

- [ ] **v1:4430-4432**

```python
add('used-by lacks the entry',
        [{**frozen, 'corpus/SOURCES.md': _registry(used='corpus/lessons/round-49.md')},
         good], 0, 1, want_fail='b:sourced')
```

- [ ] **v1:4433-4435**

```python
add('coverage map lacks the stem',
        [{**frozen, 'corpus/README.md': _readme(stem='2026-10-26-r41-other')}, good], 0, 1,
        want_fail='b:coverage_map_row')
```

## Static-review conclusions / residual risk

This checklist is complete against the reviewed v1 scoring boundary, clause tuple, binding tuple, CLI paths and static selftest inventory. It does not certify an as-yet-unreviewed v2 implementation or a live outcome. Highest integration risks are mode isolation from historical evidence, missing new documentation predicates, and publishing the predicate command without resolving --pkg65. The baseline already implements freeze drift gating, contrary to the draft claim. Runtime controls and L1-only post-freeze production score remain not run.
