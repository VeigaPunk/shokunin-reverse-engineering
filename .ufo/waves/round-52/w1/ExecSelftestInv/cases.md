# R52 C1 counter selftest inventory

Source inspected: `tools/round-50/c1-counter.py`, `selftest()` (lines 2868–4594). “Port” means preserve the asserted behavior while migrating round-specific paths/constants and claim labels to R52; cases depending on changed law must be adapted rather than copied verbatim.

| Case id/name (v1 selftest label) | What it asserts | R52 disposition | Why |
|---|---|---|---|
| green (4 AVM carriers, fresh receipts, docs) | Complete four-carrier predicate can pass. | adapt-for-r52 | Baseline, new law/bindings and receipt shape. |
| do-nothing (freeze files only) | Missing receipts cannot pass. | keep/port-as-is | Essential negative control. |
| receipt missing (g7582) | Incomplete receipt set fails. | keep/port-as-is | Required evidence completeness. |
| receipt added at freeze | A receipt already present at freeze is stale. | keep/port-as-is | Freshness invariant. |
| receipt added before freeze | Pre-freeze receipt remains stale across history. | keep/port-as-is | Full-history freshness invariant. |
| oracle-only fabrication with re-minted evidence id | Re-minting does not hide fabricated chunk geometry from projection. | keep/port-as-is | Projection must compare fresh run. |
| fabrication differing only in one published sha256 | One altered output digest fails projection. | keep/port-as-is | Projection integrity. |
| fabrication differing only in an extra gap | Added gap fails law disposition. | adapt-for-r52 | Gap-law semantics change; still require exact disposition. |
| fabrication differing only in the diagnostics multiset | Dropped diagnostic fails projection. | keep/port-as-is | Projection integrity. |
| rerun yields no evidence object (REA ok=false) | Failed extraction run is red. | keep/port-as-is | Fail closed. |
| rerun environment error (no npx) is unevaluable, never met | Runner setup error exits 2, not green. | keep/port-as-is | Unevaluable distinction. |
| rerun hits REA provider_timeout (3 attempts) is unevaluable, never a projection verdict | Exhausted timeout retry remains unevaluable. | adapt-for-r52 | Retain for new bounded retry policy; exact attempt contract updated. |
| subject digest names another carrier | Receipt subject pin is bound to carrier. | keep/port-as-is | Pin integrity. |
| standard-LE carrier (mkfs_time is a timestamp, no AVM marker) | Rejects ordinary image lacking marker. | keep/port-as-is | Layout scope. |
| marker off by one (mkfs_time == bytes_used + 1) | Rejects malformed marker. | keep/port-as-is | Layout scope. |
| big-endian AVM-marker image (sqsh) is not the little-endian layout | Rejects BE image. | keep/port-as-is | Layout scope. |
| standard big-endian image (sqsh, no marker) | Rejects standard BE image. | keep/port-as-is | Layout scope. |
| hsqs magic over big-endian fields is not a little-endian image | Rejects hybrid superblock. | keep/port-as-is | Layout parsing. |
| compression id 1 (gzip) is not the frozen xz | Rejects gzip layout. | keep/port-as-is | Frozen carrier layout. |
| compression id 2 (lzma; round 41 counted it as xz) | Rejects LZMA. | keep/port-as-is | Frozen carrier layout. |
| compression id 6 (zstd) | Rejects Zstd. | keep/port-as-is | Frozen carrier layout. |
| squashfs 3.0 major | Rejects v3. | keep/port-as-is | Frozen carrier layout. |
| squashfs 4.1 minor | Rejects unsupported minor version. | keep/port-as-is | Frozen carrier layout. |
| bytes_used beyond the file | Rejects invalid size bound. | keep/port-as-is | Layout parser boundary. |
| inode table after the directory table | Rejects invalid table order. | keep/port-as-is | Layout parser boundary. |
| directory table past bytes_used | Rejects out-of-bound table. | keep/port-as-is | Layout parser boundary. |
| inode table at offset 0 | Rejects invalid table offset. | keep/port-as-is | Layout parser boundary. |
| shorter than a superblock | Rejects truncated image. | keep/port-as-is | Layout parser boundary. |
| frozen layout is accepted (layout probe) | Positive direct probe accepts valid shape. | keep/port-as-is | Confirms adversarial fixtures discriminate. |
| CTL-C1-4 standard LE carrier planted under genuine pin (carrier_pin_ok) | Wrong bytes under expected digest fail pin. | keep/port-as-is | Pin security. |
| CTL-C1-4 standard LE carrier planted under genuine pin (layout_ok) | Bad layout independently fails. | keep/port-as-is | Layout security. |
| carrier listed but never committed | Missing frozen carrier fails. | keep/port-as-is | Frozen input completeness. |
| malformed oracle row | Invalid oracle syntax fails. | keep/port-as-is | Frozen table parsing. |
| malformed nonregular row | Invalid census syntax fails. | keep/port-as-is | Frozen table parsing; now census critical. |
| wrong operation (extract_filesystem) | Operation must be extract_firmware. | keep/port-as-is | Receipt identity. |
| provider is not unblob | Provider must match. | keep/port-as-is | Receipt identity. |
| failed chunk | Failed extraction chunk fails. | keep/port-as-is | Extraction validity. |
| chunk handler is the BE handler (squashfs_v4_be) | Handler must be LE. | keep/port-as-is | Handler binding. |
| chunk handler is squashfs_v3 | Handler must be v4 LE. | keep/port-as-is | Handler binding. |
| chunk handler is the bare prefix squashfs_v4 | Handler must be exact. | keep/port-as-is | Handler binding. |
| one LE chunk and one BE chunk | All SquashFS chunks must match. | keep/port-as-is | Prevents mixed-handler laundering. |
| no squashfs chunk at all (padding only) | Requires a relevant filesystem chunk. | keep/port-as-is | Scope binding. |
| disallowed gap kind on a symlink entry | Disallowed disposition fails. | adapt-for-r52 | Rule's allowed kinds may evolve; retain violation test. |
| gap on a path that is not a non-regular entry | Orphan gap fails. | keep/port-as-is | Exact census/gap matching. |
| required gap missing (symlink materialised) | Missing required symlink disposition fails. | keep/port-as-is | Symlink rule remains separate from devices. |
| escaping symlink published as a regular file | Symlink cannot be represented as ordinary published file. | keep/port-as-is | Nonregular integrity. |
| oracle file missing from published set | Missing oracle output fails. | keep/port-as-is | Completeness. |
| foreign scratch provenance (/kaidoku-r39/) | Wrong run provenance fails. | adapt-for-r52 | Change prefix to round-52. |
| provenance path climbs out with .. | Traversal cannot satisfy provenance. | adapt-for-r52 | Change prefix to round-52. |
| evidence id stale after an edit | Receipt evidence ID binds contents. | keep/port-as-is | Envelope integrity. |
| extra regular file published under extract root | Unlisted output fails. | keep/port-as-is | Exact oracle set. |
| published file with oracle sha256 but another size | Size is part of oracle identity. | keep/port-as-is | Exact oracle tuple. |
| oracle table row without size column | Required table column enforced. | keep/port-as-is | Parser contract. |
| oracle table row with non-numeric size | Size type enforced. | keep/port-as-is | Parser contract. |
| oracle table row with a .. component | Oracle path traversal rejected. | keep/port-as-is | Path safety. |
| receipt path with a .. component | Receipt path traversal rejected. | keep/port-as-is | Path safety. |
| score receipt counter_sha256 committed as after-receipt | Score receipt is not valid evidence envelope. | keep/port-as-is | Evidence type separation. |
| score receipt exit_code committed as after-receipt | Score receipt is not valid evidence envelope. | keep/port-as-is | Evidence type separation. |
| provenance by substring only | Prefix substring is insufficient. | adapt-for-r52 | Update provenance prefix. |
| provenance names previous round scratch | Prior-round provenance fails. | adapt-for-r52 | Update round-specific constants. |
| provenance is a relative path | Provenance must be absolute/trusted. | keep/port-as-is | Path validation. |
| receipt made at max_depth 3 | Frozen depth parameter enforced. | keep/port-as-is | Parameter binding. |
| receipt made under smaller output budget | Frozen output budget enforced. | keep/port-as-is | Parameter binding. |
| receipt without recorded parameters | Missing parameters fail. | keep/port-as-is | Parameter binding. |
| missing-extractor-dependency gap (sasquatch absent) | Dependency gap is not accepted as normal coverage. | keep/port-as-is | Extraction environment accounting. |
| failed chunk reported when sasquatch absent | Failed chunk remains red. | keep/port-as-is | Extraction environment accounting. |
| real runner uses package CLI, frozen flags, FIXED_PATH/toolchain | Executes pinned package and arguments. | keep/port-as-is | Runner/toolchain contract. |
| unblob that is not 26.6.4 is refused | Pins unblob version. | keep/port-as-is | Toolchain pin. |
| package that is not 6.5.0 is refused | Pins REA version. | keep/port-as-is | Toolchain pin. |
| package without bin entry is refused | Requires executable package entry. | keep/port-as-is | Runner setup. |
| package whose bin entry is missing is refused | Requires existing CLI file. | keep/port-as-is | Runner setup. |
| shim sasquatch on caller PATH is not resolved | Fixed child PATH defeats shim. | keep/port-as-is | Toolchain trust. |
| running counter is not counter frozen at freeze | Counter identity mismatch exits 2. | keep/port-as-is | Freeze identity. |
| no counter at freeze | Missing frozen counter exits 2. | keep/port-as-is | Freeze identity. |
| side-branch receipt re-added after freeze is not fresh | Full-history freshness detects pre-freeze add. | keep/port-as-is | Freshness invariant. |
| same history, receipt added only after freeze is fresh | Legitimate post-freeze addition passes freshness. | keep/port-as-is | Positive freshness control. |
| oracle re-derivation equal to frozen tables | Matching independent result passes. | keep/port-as-is | Independent data verification. |
| frozen oracle table shrunk | Omitted carrier file detected. | keep/port-as-is | Set equality. |
| frozen oracle table extended | Phantom table row detected. | keep/port-as-is | Set equality. |
| frozen oracle row with another sha256 | Digest mismatch detected. | keep/port-as-is | Set equality. |
| frozen oracle row with another size | Size mismatch detected. | keep/port-as-is | Set equality. |
| carrier derives nothing while table lists files | Empty re-derivation is red. | keep/port-as-is | Set equality. |
| unsquashfs cannot run | Reader unavailable exits 2, never green. | keep/port-as-is | Unevaluable boundary. |
| real unsquashfs equals built fixture tree | Independent executable probe agrees with source tree. | keep/port-as-is | Reader integration probe. |
| real unsquashfs differs from doctored table | Real reader probe discriminates table mutation. | keep/port-as-is | Reader integration probe. |
| real unsquashfs leaves no scratch tree | Temporary extraction cleanup. | keep/port-as-is | Resource cleanup. |
| real unsquashfs missing tool / wrong version | Both environment failures rejected. | keep/port-as-is | Reader pin and prerequisite. |
| real runner sasquatch not on child PATH | Missing dependency is unevaluable. | keep/port-as-is | Runner prerequisite. |
| four external carriers, cache green | Cache bytes supply external carriers. | adapt-for-r52 | Carrier table/pin schema changes; retain. |
| four external carriers, empty cache | Missing cached bytes fail. | keep/port-as-is | Offline data path. |
| four external carriers, no carrier-cache | Missing cache argument fails. | keep/port-as-is | Offline data path. |
| four external carriers, cache bytes not pinned | Cache digest enforced. | keep/port-as-is | Carrier integrity. |
| external carve length differs from bytes_used | Carve size must match. | keep/port-as-is | Carrier layout. |
| REA package does not match frozen pin | Package mismatch unevaluable. | adapt-for-r52 | R52 pin location/version contract. |
| no rea-pkg pin at freeze | Missing package pin unevaluable. | adapt-for-r52 | R52 pin location. |
| regular usr/bin/busy vs symlink bin/busy | Exact path matcher avoids suffix false positive. | keep/port-as-is | Historical path bug guard. |
| regular sbin/tool vs symlink usr/sbin/tool | Exact path matcher avoids inverse suffix confusion. | keep/port-as-is | Historical path bug guard. |
| materialised symlink at own entry path | Exact matcher still catches link publication. | keep/port-as-is | Positive path check. |
| deeper-than-oracle file vs oracle row | Deeper path cannot satisfy row. | keep/port-as-is | Exact path identity. |
| nested chunk root file vs outer-root row | Nested namespace isolated. | keep/port-as-is | Chunk namespace. |
| plain oracle row | Ordinary exact row matches. | keep/port-as-is | Matcher positive control. |
| regular usr/bin/busy does not satisfy symlink bin/busy | Extraction scores without false symlink disposition. | keep/port-as-is | Regression guard. |
| regular sbin/tool does not satisfy symlink usr/sbin/tool | No suffix collision. | keep/port-as-is | Regression guard. |
| published regular at symlink entry caught | Materialized link flagged. | keep/port-as-is | Nonregular integrity. |
| deeper file with oracle row sha does not publish row | Oracle path exactness. | keep/port-as-is | Regression guard. |
| gap on usr/bin/busy does not resolve symlink bin/busy | Gap matching exact. | keep/port-as-is | Regression guard. |
| two chunks with oracle_root | Explicit root disambiguates. | keep/port-as-is | Root selection. |
| two roots without oracle_root fail closed | Ambiguity not guessed. | keep/port-as-is | Root selection. |
| oracle_root names no derivation root | Invalid hint fails closed. | keep/port-as-is | Root selection. |
| nested chunk file does not publish outer-root row | Namespace isolation. | keep/port-as-is | Root selection. |
| padded carrier oracle resolves under portion chunk directory | Correct nested path handling. | keep/port-as-is | Measured geometry. |
| padded carrier rows one level too shallow score nothing | Rejects incorrect geometry. | keep/port-as-is | Measured geometry. |
| two AVM chunks in one receipt ambiguous | Ambiguous root fails closed. | keep/port-as-is | Root selection. |
| two handler chunks, no input handler fail closed | Missing top-level relationship fails closed. | keep/port-as-is | Root selection. |
| file outside subject root is another namespace | Ignores unrelated namespace rather than treating as extra. | keep/port-as-is | Root selection. |
| no squashfs derivation edge fails closed | Requires derivation edge. | keep/port-as-is | Root selection. |
| removal diagnostic admitted for symlink | Valid removal disposition recognized. | keep/port-as-is | Removal accounting. |
| removal link outside run root cannot be mapped | Unmappable diagnostic fails. | keep/port-as-is | Removal accounting. |
| removal with filesystem-root run root cannot be mapped | Invalid root fails mapping. | keep/port-as-is | Removal accounting. |
| entry cannot be both gapped and removed | Mutually exclusive dispositions. | keep/port-as-is | Accounting exclusivity. |
| required symlink with no disposition fails | Required entry accounted. | keep/port-as-is | Required disposition. |
| removal resolves to no symlink row fails | Orphan diagnostic fails. | keep/port-as-is | Exact accounting. |
| removal naming unlisted kind fails | Removal cannot hide device row. | adapt-for-r52 | Must specifically preserve no-device-disposition law. |
| silent empty-target symlink admitted | Explicit silent rule permits exact case. | keep/port-as-is | Symlink-specific allowance. |
| non-empty symlink cannot use silent allowance | Silent detail is exact. | keep/port-as-is | Symlink-specific allowance. |
| rerun removed a different link breaks projection | Removal identity is projected. | keep/port-as-is | Projection completeness. |
| relabelled previous-round pins (prior_pins) | Prior pins are not fresh coverage under v1. | adapt-for-r52 | R52 explicitly allows only frozen four-pin re-score; assert allow-list and source visible. |
| round-41 carrier table names frozen pins | Prior source pins detected. | adapt-for-r52 | Must be visible and permitted only via explicit re-scored allow-list. |
| round-49 carrier table names frozen pin | Prior source pins detected. | adapt-for-r52 | Same explicit allow-list behavior. |
| prior-pins document names frozen pin | Prior source pins detected. | adapt-for-r52 | Same explicit allow-list behavior. |
| prior_pins not 64-hex | Invalid pins rejected. | keep/port-as-is | Schema validation. |
| external spec missing member_sha256 | External pin required. | keep/port-as-is | Vendor chain integrity. |
| external spec missing positive carve length | Length required. | keep/port-as-is | Vendor chain integrity. |
| external spec with member_sha256 | Valid external shape accepted. | keep/port-as-is | Positive schema probe. |
| nested external block missing sha256 | Nested pin required. | keep/port-as-is | Vendor chain integrity. |
| nested external block with sha256 | Valid nested shape accepted. | keep/port-as-is | Positive schema probe. |
| oracle_root relative accepted / absolute rejected | Hint path shape enforced. | keep/port-as-is | Schema validation. |
| target missing / target frozen at 3 | Target is fixed at four. | keep/port-as-is | Carrier set contract. |
| rea_parameters missing, depth 3, missing budget, noninteger budget | Frozen run parameters are complete and typed. | keep/port-as-is | Parameter schema. |
| carrier ids compare case-insensitively | IDs normalized consistently. | keep/port-as-is | Schema behavior. |
| fifth carrier id outside claim | Out-of-scope member rejected. | keep/port-as-is | Carrier-set boundary. |
| carrier longer than bytes_used (sloppy carve) | Extra bytes fail carve check. | keep/port-as-is | Carrier exactness. |
| carrier bytes changed after freeze | Drift exits 2. | keep/port-as-is | Freeze gate. |
| carrier bytes changed then restored | Historical transient drift still exits 2. | keep/port-as-is | Freeze gate. |
| oracle changed after freeze | Oracle drift exits 2. | keep/port-as-is | Freeze gate. |
| nonregular table changed after freeze | Census drift exits 2. | keep/port-as-is | Freeze gate. |
| carriers.json changed after freeze | Spec drift exits 2. | keep/port-as-is | Freeze gate. |
| gap-rule changed after freeze / touched then restored | Rule drift history exits 2. | keep/port-as-is | Freeze gate. |
| counter edited after freeze | Counter drift exits 2. | keep/port-as-is | Freeze gate. |
| claims edited after freeze | Claims drift exits 2. | keep/port-as-is | Freeze gate. |
| new file under tools/round-50 after freeze | New frozen-family file detected. | adapt-for-r52 | Prefix must become tools/round-52. |
| rea-pkg pin edited after freeze | Pin drift exits 2. | adapt-for-r52 | R52 pin path. |
| carried-over second reader edited after freeze | Reader drift exits 2. | keep/port-as-is | Frozen dependency. |
| carried-over fetcher edited after freeze | Fetcher drift exits 2. | adapt-for-r52 | R52 fetcher path/pin. |
| xpin tool edited after freeze | External tool drift exits 2. | keep/port-as-is | Frozen dependency. |
| oracle table first committed after freeze | Cannot retroactively freeze table. | keep/port-as-is | Freeze completeness. |
| frozen plan edited by merge commit itself (evil merge) | Merge commit diff included in drift walk. | keep/port-as-is | History robustness. |
| frozen counter edited on side branch and merged | Side-branch change detected. | keep/port-as-is | History robustness. |
| clean merge touching nothing frozen | Harmless merge passes. | keep/port-as-is | Positive drift control. |
| frozen pin wrong | Carrier digest mismatch fails. | keep/port-as-is | Pin integrity. |
| carriers.json drops carrier (target 4) | Wrong count fails schema. | keep/port-as-is | Carrier-set boundary. |
| all four carriers read gzip | Wrong layout fails. | keep/port-as-is | Layout enforcement. |
| gap rule omits device kind | Incomplete old rule fails. | adapt-for-r52 | Replace with rule-shape tests requiring empty device allowances, no device silent details. |
| gap rule JSON not object | Malformed rule fails. | keep/port-as-is | Frozen schema. |
| gap rule names another claim | Claim mismatch fails. | adapt-for-r52 | Accept R50 and R52 arms; R52 rule must label R52-C1. |
| structural gap within allowance / over allowance / path-less unallowed / path-bearing structural | Enforces bounded structural gap rules and path shape. | adapt-for-r52 | R52 specifically records depth-limited input_path and continuation_id; test these fields, not just count. |
| frozen core profile fabrication refused; plus-extractor profile detects projection delta | Frozen projection profile and semantic comparison. | keep/port-as-is | Projection contract. |
| projection missing / plus-mime / unknown profile | Only approved projection accepted. | keep/port-as-is | Schema contract. |
| rerun passes frozen max_depth/output budgets; uses frozen values not receipt | Runner replays frozen parameters. | keep/port-as-is | Replay integrity. |
| province Core section absent; row outside section; wrong handler; bare handler; no AVM marker; wrong AVM layout; row absent; wrong cited entry | Documentation bindings are enforced. | adapt-for-r52 | Replace round-50 names with R52 constants. |
| frontier note absent / lacks LE AVM / BE token rejected / AVM-LE accepted | Frontier migration binding enforced. | adapt-for-r52 | Update round-52 note and entry. |
| entry absent; wrong S-id substring; source opened outside window; used-by wrong; coverage map wrong | Source and entry bindings enforced. | adapt-for-r52 | Update entry stem, S243/S244/S245/S249/S250/S251/S252, date and coverage constants. |

## Required new R52 cases absent from v1

| New case | Fixture required | Expected exit / finding |
|---|---|---|
| Frozen-path-drift exit 2 | Isolated fixture git repository with the R52 freeze committed, then mutate one frozen R52 instrument byte (e.g. `tools/round-52/gap-rule.json`) at REV; include exact clone-root assertion before commits. | Exit 2; `reason=frozen_path_changed`, changed path named. |
| ENOENT-retry-exhausted red | Deterministic runner fixture returns `execution_failure` with `ENOENT` naming a path inside the extraction tree on both allowed attempts; fresh extraction roots and attempt diagnostics represented. | Exit 1 (semantic red), `projection_ok=false`; exhaustion/attempt count and final ENOENT reported. Must not become exit 2 or green. |
| law_shape_ok red: all-thirteen whitelist | Valid frozen rule mutation with `required.char-device=true` and `removed.silent.char-device` containing all thirteen measured device details (the extensionally equivalent whitelist). | Exit 1; `law_shape_ok=false` even if the four measured carriers otherwise satisfy rule disposition. |
| Census re-derivation fail | Deterministic re-derive fixture returns non-regular row set differing from frozen `*.nonregular.tsv` in either direction; additionally model unavailable reader separately. | Mismatch: exit 1, `census_rederived_ok=false`. Reader unavailable: exit 2 `oracle_env_error`. |
| Prior-pin allow-list visible in receipt | Frozen R52 carrier spec lists exactly the four approved prior pins in `re_scored_pins`; freeze includes source pin tables; score fixture returns receipt JSON. Mutant omits/changes allow-list or prior-pin source. | Valid set may pass `carrier_fresh_ok`; receipt must expose exact allow-list and `prior_pin_sources`. Missing/extra/changed pin must be red and receipt cannot silently waive freshness. |
| depth_gap_recorded | Receipt fixture includes depth-limited gap with `input_path` and `continuation_id`; paired mutants omit either field or the gap. | Complete evidence produces `depth_gap_recorded=true`; missing evidence yields exit 1 and `depth_gap_recorded=false`. |
| wrong-carrier-set: only two receipts | Frozen spec still expects g7581, g7582, c6490, c6430; fixture provides valid-looking receipts for only two. | Exit 1, `carriers_matched` at most 2 (not target 4), carrier-set binding false; must never pass on subset. |
