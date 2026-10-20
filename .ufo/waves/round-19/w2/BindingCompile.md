# t1250-compile C3 binding review

## Axes exercised

- **Calibration:** frozen H1 prediction versus the retained observation and raw Ghidra log.
- **Freshness:** producer-pinned revision, carrier identity, log digest, and pin-map digests.
- **Depth:** embedded pre/post maps plus all six periodic mid-run maps.

**Scope:** read-only check of `runs/t1250-compile/{receipt.json,producer.json,pins/,logs/*/ghidra.log}`, the retained receipt validation, and the frozen prediction at `a1140e76fffdc1be032d9d813dbb686157803bbc`. No REA/Ghidra analysis, carrier execution, builds, mutations, or installs were performed.

## Finding

### Medium — the error-free auxiliary prediction passes despite a retained Ghidra analyzer exception

**Observation:** The bound log records `ERROR (AnalysisTaskWrapper) Analysis Task: Golang RTTI Propagation (deferred) - ... NullPointerException: element cannot be mapped to a null key` at `runs/t1250-compile/logs/rea-ghidra-uEQQSP/ghidra.log:347`. The failing activity is specifically the deferred RTTI propagation task; the same log later says `Analysis succeeded` at line 426. Separately, `runs/t1250-compile/observation.json:2` records `"analyzer_errors": []`, and `runs/t1250-compile/compare.json:37-41` marks `extra.analyzer_errors_empty` as matching `true` and the whole comparison `all_match: true`. The frozen prediction explicitly requires `analyzer_errors_empty: true` (`predictions/t1250-compile.prediction.json:43-47`).

**Inference:** The snapshot-selection result itself is supported: the log says it used the 1.25.0 snapshot (`ghidra.log:332-337`), while the observation and comparison report `snapshot_route: info` and the expected 1.25.0 label (`observation.json:3-8, 158-163`; `compare.json:10-29`). But the passing auxiliary “no analyzer errors” claim is not supported by the raw log. Unless `analyzer_errors` is explicitly defined to exclude Ghidra `ERROR (AnalysisTaskWrapper)` events, the extractor/comparison has a false-clean result; at minimum the field's narrower scope must be disclosed before treating this compile run as error-free.

## Binding and freshness checks

**Observation:** The producer records branch tip `a1140e76fffdc1be032d9d813dbb686157803bbc` (`runs/t1250-compile/producer.json:2-5`), matching the requested frozen prediction revision. The frozen prediction at that revision names the compile carrier SHA-256 `20dbac54f9f897582aedafea7207976f0300cfd4992429814d00bccbea7a4083` (`predictions/t1250-compile.prediction.json:32-35`). The receipt's carrier pre/post hashes are both that value (`runs/t1250-compile/receipt.json:5-10`), and the independently hashed current carrier also matches. The receipt binds `/tmp/kr17-rea-9nv8amxo/rea-ghidra-uEQQSP`, lists no unbound sessions, and records `logfile_ok`, `md5_ok`, and `target_ok` as true (`receipt.json:2-4, 1892-1914, 2036`). Its retained log path, byte count, and SHA-256 are `.../ghidra.log`, `77180`, and `fcad067469e3470db9a03536983c2243434ba6e2fdcca4fe606616a50f6ea7f0` (`receipt.json:1899-1904`); the independent hash below matches. The raw log's imported target is the carrier-named temporary image (`ghidra.log:46`), with MD5 `62abe5762a6fe2d42cf22297728a7f3f` matching the receipt's `md5_pre` (`ghidra.log:58`; `receipt.json:5-8`).

The pin directory contains six `mid-*.json` maps. Pre/post snapshots are embedded in the receipt, not separate files there: the receipt says `pins_compare.equal: true` with empty `changed`, `missing`, and `errors` (`receipt.json:348-355`); an independent JSON comparison found 152 entries in each and equality. The six recorded mid-map checks each have 152 entries, `equal: true`, and empty `changed`/`missing` (`receipt.json:1934-1988`). Independently recomputed SHA-256 values match every recorded `map_sha256` (commands/results below). The retained validator record says one receipt valid, zero invalid/unreadable, 390 checks, and `require_mid_maps: true` (`evidence/receipt-validation/t1250-compile.json:2-22`).

**Validator digest note (not a finding):** `producer.json:11` records the run-time `receipt-validate.py` SHA-256 as `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145`; the current file hashes to `6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762`. This is the expected forward-fix mismatch called out in the assignment. It does not alter the retained validation result, and I did not rewrite the receipt or validation record.

## Commands and exit codes

Commands below ran from `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; all were read-only.

```text
sha256sum .ufo/waves/round-19/runs/t1250-compile/logs/rea-ghidra-uEQQSP/ghidra.log .ufo/waves/round-19/runs/t1250-compile/pins/mid-*.json /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/compile
fcad067469e3470db9a03536983c2243434ba6e2fdcca4fe606616a50f6ea7f0  .../logs/rea-ghidra-uEQQSP/ghidra.log
97ebc1e98d974511189d96d7afd42046abf35b52a5f4102748b3a6df3d3bd765  .../pins/mid-1.json
21ced074f094f67cbb1e5cd48c55a279276b15170bf4d66db18b36a91c35bed3  .../pins/mid-2.json
6b41a6af3f520034380e92c7b7ecd7915586cc07296ac4b49e6a68487912117c  .../pins/mid-3.json
6c8a16c2429e1f5096bac0df238c390c738e6c2011fcb5329c00665d9ee84c2e  .../pins/mid-4.json
e27996b4a6af871c8e5968f0f28b4e7137f8652d99e81f9bbef08178d224118e  .../pins/mid-5.json
b32252b227ea1dd006756ccdec693590f2e117e06ce5e3abc237bae45bd9359a  .../pins/mid-6.json
20dbac54f9f897582aedafea7207976f0300cfd4992429814d00bccbea7a4083  /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/compile
exit=0

find .ufo/waves/round-19/runs/t1250-compile/pins -maxdepth 1 -type f -name 'mid-*.json' -printf '%f\n' | sort | wc -l
6
exit=0

set -o pipefail; git show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-compile.prediction.json | jq '{carrier, expected, extra_expectations, hypothesis:.c3.hypothesis_frozen}'
# carrier.sha256 = 20dbac54f9f897582aedafea7207976f0300cfd4992429814d00bccbea7a4083
# extra_expectations.analyzer_errors_empty = true
# hypothesis = H1
exit=0

git show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-compile.prediction.json | sha256sum
651d6b125ddbbaa6a67b7da274ee525eb56c24a9f16a4d8858dae3c229f64f7f  -
exit=0

jq '{pre_entries:(.pins_pre.entries|length), post_entries:(.pins_post.entries|length), pre_post_equal:(.pins_pre.entries == .pins_post.entries)}' .ufo/waves/round-19/runs/t1250-compile/receipt.json
# {"pre_entries":152,"post_entries":152,"pre_post_equal":true}
exit=0

jq -e '.pins_pre.entries == .pins_post.entries' .ufo/waves/round-19/runs/t1250-compile/receipt.json >/dev/null
exit=0

sha256sum .ufo/waves/round-17/tools/receipt-validate.py
6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762  .ufo/waves/round-17/tools/receipt-validate.py
exit=0

jq -r '.tool_sha256["/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py"]' .ufo/waves/round-19/runs/t1250-compile/producer.json
70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145
exit=0
```

## Residual risk and verification gaps

**Observation:** The receipt explicitly says log capture is a polling copy and lines written after its final poll but before REA removes its runtime directory may be absent (`receipt.json:24`). Its retained copy timestamp is `19:05:05.644661Z` (`receipt.json:1911-1913`); the copied log ends at `ghidra.log:432` while it is processing post-script changes, so the bytes are integrity-bound but the retained log's completeness is not established.

**Inference:** Treat the observed snapshot route and carrier/map identity as bound, but do not infer that no later analyzer diagnostics existed or that the compile analysis was wholly clean. No edits outside this report were made.