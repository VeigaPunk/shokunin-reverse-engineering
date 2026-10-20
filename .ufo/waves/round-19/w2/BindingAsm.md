# C3 binding review — `t1250-asm`

## Scope and verdict

**Axes:** depth (C3) was reviewed; calibration (C1) and freshness (C2) were not assessed here.

**Recommendation:** no actionable carrier, prediction, or pin-map identity mismatch was found for `t1250-asm`. The retained record supports counting this as **one of eight** run-bound labels, and its captured outcome matches the frozen predicted-silent/non-D result. This is not a conclusion about the other seven labels or overall C3 confirmation.

## Findings

None on the identity/hash checks performed.

### Observations

- `runs/t1250-asm/producer.json:3-5` records the run at branch tip `a1140e76fffdc1be032d9d813dbb686157803bbc`; the amended claim also says predictions were frozen at that tip before analyze (`claims.json:36-40`). The current `refs/heads/main` tip observed for this review is `279e8b19c51658bfd05b9e31a1c0894ab2e70537`, so the later branch advancement does not change the recorded run tip. The live prediction file SHA-256 equals the blob read from the frozen tip.
- The carrier identity agrees three ways: the frozen prediction records SHA-256 `a7ed400a04009488ea819eb06aeb912dc3537125cceef036743641060fd797f4` (`predictions/t1250-asm.prediction.json:32-35`); the receipt records that same pre/post SHA (`runs/t1250-asm/receipt.json:5-9`); and the independent `sha256sum` of `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/asm` returned the same value. The retained log names `target-a7ed400a0400.bin` as the imported target (`runs/t1250-asm/observation.json:161-168`; `logs/rea-ghidra-cWUKB0/ghidra.log:163,167`).
- The receipt records one bound session and no unbound sessions (`runs/t1250-asm/receipt.json:2-4,2009`). Its retained-log binding flags are all true (`:1892-1903`). Independently hashing the retained `ghidra.log` returned `c350a577d36682ca7099585481bf246344317a178abfe3349fbf4dfc3f723795`, matching both the receipt (`:1900-1903,1967-1970`) and observation (`observation.json:165-168`).
- There are exactly three standalone `pins/mid-*.json` files. Their independent SHA-256 values match the receipt's `steps.analyze.pin_checks` at `receipt.json:1934-1960`. The three maps each contain 152 entries; the receipt's embedded pre/post maps each contain 152 entries too, and all three mid-map `entries` objects compare equal to both pre and post. The receipt reports `pins_compare.equal: true`, with no changed, missing, or error entries (`receipt.json:348-355`).
- Retained validation evidence is clean: `evidence/receipt-validation/t1250-asm.json:2-22` reports one valid receipt, zero invalid/unreadable, exit 0, and `require_mid_maps: true`. The independent `compare.json` says `all_match: true` and records matches for every listed field including empty analyzer errors, EOF reads, and invalid-index reads (`runs/t1250-asm/compare.json:1-53`); `compare.exit:1` contains `0`.
- The prediction is non-D and expects snapshot route `info`, snapshot label `1.25.0`, and no analyzer errors, EOF reads, or invalid-index reads (`predictions/t1250-asm.prediction.json:15-47`; `predictions/decision-rule.json:2-6`). The structured observation records route `info`, version `1.25.0`, and empty analyzer-error, mapper-error, symbol-failure, EOF, and invalid-index lists (`observation.json:1-8,158-177`). The retained log records the Go 1.25.0 snapshot route and successful analysis (`ghidra.log:168-172,221`). This is an observed prediction match for this non-D carrier; it is not the D/vet discriminator.
- The captured validator digest is `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145` (`producer.json:6-13`), while the current validator file hashes to `6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762`. The post-freeze diff is the forward fix to how list-shaped `steps` identify the analyze step; this receipt uses object-shaped `steps.analyze` (`receipt.json:1919-1934`). Per the assignment, this expected current-file digest mismatch is not treated as a defect. I did not rewrite the receipt or claim to have rerun the historical validation with the current validator.

## Residual risk and verification gaps

- **Log-tail completeness is not established.** The receipt itself discloses that polling capture can miss lines written after the final poll and before REA deletes its runtime root (`receipt.json:24`). The final retained copy is timestamped `2026-10-20T19:01:35.627283Z`, while the analyze step ended at `19:01:36.127947Z` (`receipt.json:1911-1933`); the stored log's last line is the post-script analysis notice at `ghidra.log:227`. The runner does perform a final best-effort scan after waiting for the process (`round-17/tools/carrier-run.py:523-533`), but that does not prove the session log was still present for that scan. **Inference:** the hash proves integrity of the retained copy, not that it is the complete final log. The expected Go snapshot and successful-analysis messages are present before the end, and no failure is shown in the captured bytes, but the negative/no-failure conclusion should remain bounded to those bytes.
- The round-19 amendment explicitly narrows C3 to artifact-held-out Go 1.25.0 toolchain ELFs, not application ELFs or version-held-out evidence (`claims.json:37,40`). This asm record supports only that narrowed cohort claim.
- No LSP device is mounted in this session: `read xd://lsp` returned `No such tool: xd://lsp`. The reviewed target is retained JSON/log evidence; no references/definition/diagnostics claims are made. A literal search was used only to locate runner lines, then those source ranges were read directly.

## Commands and results

Commands below were read-only. Exit codes are included; no carrier was executed, no REA/Ghidra run was performed, and no receipt was changed.

```text
$ sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-asm/logs/rea-ghidra-cWUKB0/ghidra.log /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-asm/pins/mid-1.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-asm/pins/mid-2.json /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-asm/pins/mid-3.json
c350a577d36682ca7099585481bf246344317a178abfe3349fbf4dfc3f723795  .../ghidra.log
a8376053e4a303a28ccf5add4a355a7ec5c74e114dc668d3413dcca0d6270790  .../mid-1.json
a32388f539332013c41b6d821ff1dd9df5b256894014b4e4d727e94c63310dfb  .../mid-2.json
5ce4e0bd60339f8a6af0e9d5d2d21c34a7fd9ffeb08c97c6570339c649227314  .../mid-3.json
exit=0

$ find .ufo/waves/round-19/runs/t1250-asm/pins -maxdepth 1 -type f -name 'mid-*.json' -print | sort | wc -l
3
exit=0

$ jq -s '.[0] as $r | .[1:] as $mid | {pre_entries:($r.pins_pre.entries|length),post_entries:($r.pins_post.entries|length),pre_post_equal:($r.pins_pre.entries == $r.pins_post.entries),mids:[$mid[]|{taken_at_utc,entries:(.entries|length)}],mid_vs_pre:[$mid[]|(.entries == $r.pins_pre.entries)],mid_vs_post:[$mid[]|(.entries == $r.pins_post.entries)]}' .ufo/waves/round-19/runs/t1250-asm/receipt.json .ufo/waves/round-19/runs/t1250-asm/pins/mid-1.json .ufo/waves/round-19/runs/t1250-asm/pins/mid-2.json .ufo/waves/round-19/runs/t1250-asm/pins/mid-3.json
{"pre_entries":152,"post_entries":152,"pre_post_equal":true,"mids":[{"taken_at_utc":"2026-10-20T19:00:33.972127+00:00","entries":152},{"taken_at_utc":"2026-10-20T19:01:04.048111+00:00","entries":152},{"taken_at_utc":"2026-10-20T19:01:34.125939+00:00","entries":152}],"mid_vs_pre":[true,true,true],"mid_vs_post":[true,true,true]}
exit=0

$ sha256sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/asm /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py
asm: a7ed400a04009488ea819eb06aeb912dc3537125cceef036743641060fd797f4
receipt-validate.py: 6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762
exit=0

$ sha256sum .ufo/waves/round-19/predictions/t1250-asm.prediction.json
 ae0c3cad056061a2daf1f9f98df6a43149e947599116f13b781f60075484ce4b
exit=0
$ git show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-asm.prediction.json | sha256sum
 ae0c3cad056061a2daf1f9f98df6a43149e947599116f13b781f60075484ce4b
exit=0

$ git diff --no-ext-diff --unified=3 a1140e76fffdc1be032d9d813dbb686157803bbc refs/heads/main -- .ufo/waves/round-17/tools/receipt-validate.py
post-freeze change handles list-shaped analyze-step identity; exit=0
```