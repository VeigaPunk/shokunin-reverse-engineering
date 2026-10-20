# C3 binding audit — `t1250-preprofile`

## Scope and axes

Read-only audit of the `t1250-preprofile` producer/receipt, retained Ghidra log, pre/post/mid pin snapshots, validation record, and frozen prediction. No production files or receipts were changed; no REA/Ghidra analysis was run.
Path shorthand: bare run filenames below are under `.ufo/waves/round-19/runs/t1250-preprofile/`; `claims.json` and `predictions/...` are under `.ufo/waves/round-19/`; `evidence/...` is under `.ufo/waves/round-19/`.

- **Calibration:** report only this run's binding and its contribution to the frozen C3 decision rule.
- **Freshness:** compare the current carrier with the prediction as stored at the producer's frozen commit, not with an inferred later prediction.
- **Depth:** independently verify the retained log/map digests, map cardinalities, and runtime identity.

## Evidence and interpretation

**Observed — carrier identity is consistent.** `producer.json:2-5` records `t1250-preprofile` and branch tip `a1140e76fffdc1be032d9d813dbb686157803bbc`. `receipt.json:5-9` binds `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/preprofile` with pre/post SHA-256 `eff3b19676f41d95eb598fa7520a9f44c2014db65a5a7470a2ca5c4cfa3f840b` and MD5 `3c3de3622961b949ae8134796c2a72d4`. Independently hashing the carrier produced those same digests. The prediction at the recorded commit has the same carrier SHA (`predictions/t1250-preprofile.prediction.json:32-34`, read from commit `a1140e76fffdc1be032d9d813dbb686157803bbc`). The run's analyzed subject also names the same path and SHA (`runs/t1250-preprofile/analyze.json:1`, `.subject`). In the retained Ghidra log, import uses the receipt's session target path and reports the same MD5 (`logs/rea-ghidra-aURSDn/ghidra.log:46,59`).

**Observed — one canonical bound runtime.** `receipt.json:2-4` has one bound session; `receipt.json:1892-1914` has one retained-log record for that same session directory, with `logfile_ok`, `md5_ok`, and `target_ok` all true; `receipt.json:1916-1918` reports no baseline session or leftovers; `receipt.json:1991` has no unbound sessions. The analyze step records exit 0 and a single mid-map check (`receipt.json:1919-1943`); `carrier-run.exit:1` and `compare.exit:1` both contain `0`. The log records Go API snapshot 1.25.0, Go version 1.25.0, and analysis success (`logs/rea-ghidra-aURSDn/ghidra.log:103-108,157`).

**Observed — bound log hash matches.** The receipt records the retained `ghidra.log` as 15,980 bytes with SHA-256 `4815553d653a8fc8bf126c85671405e249705d2c7ced05baadd7b9612eb99242` (`receipt.json:1899-1908`, also `:1946-1958`). An independent `sha256sum` of the retained file returned the same digest.

**Observed — pin snapshots match across the sampled points.** `receipt.json:348-355` records equal pre/post maps with no changed, missing, or errored entries. The embedded pre/post snapshots occupy `receipt.json:356-1121` and `receipt.json:1122-1887`. The sole file in `pins/` matching `mid-*.json` is `pins/mid-1.json:1-3,764-765`; it contains 152 entries. Independent structured comparison found 152 entries in each of pre, post, and mid, with all three entry maps equal. Receipt `steps.analyze.pin_checks` likewise records 152 entries, `equal: true`, no changes/missing entries, and the mid file's SHA-256 (`receipt.json:1934-1943`).

**Observed — retained validation is a clean historical record.** `evidence/receipt-validation/t1250-preprofile.json:2-22` records one valid receipt, 360 checks, no findings, exit 0, and `require_mid_maps: true`. The target-scoped diff from the recorded run tip to current `refs/heads/main` adds the run artifacts and this validation record; the prediction file itself has no diff in that comparison.

**Inference — no C3 binding defect found for this run.** Carrier identity, runtime/session identity, retained-log hash, and all sampled pin-map entry values cross-check. The evidence supports counting `t1250-preprofile` as a bound retained-log run. It does not, by itself, discriminate H1: the frozen prediction says `h1_kind: none` (`predictions/t1250-preprofile.prediction.json:15-30`), and the amended C3 rule names only `t1250-vet` as discriminator D (`claims.json:40`). Therefore this is one of the predicted non-discriminating/silent carriers, not independent confirmation of H1.

## Findings by severity

- **Critical:** none.
- **High:** none.
- **Medium:** none.
- **Low:** none.

No actionable C3 binding finding in scope.

## Residual risk and verification gaps

- **Log completeness is not established.** The receipt explicitly warns that polling-copy capture can miss lines emitted after the last poll (`receipt.json:24`). Its last copy is `19:06:14.206423Z`, while the analyze step ended at `19:06:14.707052Z` (`:1911-1913,1931`); the retained log ends at line 163 while post-script analysis is in progress (`ghidra.log:157-163`). The logged snapshot/version and primary analysis-success lines are present, and the receipt records analyze exit 0, but the retained file should not be represented as a complete teardown transcript.
- **Pin stability is snapshot evidence, not continuous observation.** One mid map was present, and pre/mid/post entries match; this does not exclude a transient change and reversion between sampled snapshots. No such event is evidenced here.
- **Validator digest drift is expected, not a finding.** `producer.json:11` pins `receipt-validate.py` at `70672eb3bd0c06e93ca439a31558f35ab7f76bd23aa74acd026290972553d145`; the current file hashes to `6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762`. Per the assignment this is the forward-fix mismatch; I did not rerun validation or rewrite the retained receipt. The retained pass is evidence of its recorded validation, not a fresh run of the current validator.
- This review covered only `t1250-preprofile` binding. It does not verify the other seven carriers or the aggregate C3 decision, and makes no broader analyzer-quality claim.

## Commands and exit codes

Commands below were read-only; all returned exit 0.

```text
sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-preprofile/logs/rea-ghidra-aURSDn/ghidra.log /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-preprofile/pins/mid-1.json /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/preprofile
# exit 0
# 4815553d653a8fc8bf126c85671405e249705d2c7ced05baadd7b9612eb99242  ghidra.log
# 4047691cb1efdeccadb0dbd9b1859d834142760305fa8ef4b81ba91e7805cba9  mid-1.json
# eff3b19676f41d95eb598fa7520a9f44c2014db65a5a7470a2ca5c4cfa3f840b  preprofile
md5sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/preprofile
# output: 3c3de3622961b949ae8134796c2a72d4  preprofile; exit 0


set -o pipefail; find /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-preprofile/pins -maxdepth 1 -type f -name 'mid-*.json' -print | wc -l
# output: 1; exit 0

jq -n --slurpfile r /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-preprofile/receipt.json --slurpfile m /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19/runs/t1250-preprofile/pins/mid-1.json '{pre_entries:($r[0].pins_pre.entries|length),post_entries:($r[0].pins_post.entries|length),mid_entries:($m[0].entries|length),pre_eq_post:($r[0].pins_pre.entries == $r[0].pins_post.entries),pre_eq_mid:($r[0].pins_pre.entries == $m[0].entries),post_eq_mid:($r[0].pins_post.entries == $m[0].entries)}'
# output: 152/152/152; all three equal; exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show a1140e76fffdc1be032d9d813dbb686157803bbc:.ufo/waves/round-19/predictions/t1250-preprofile.prediction.json | jq -r '.carrier.sha256'
# output: eff3b19676f41d95eb598fa7520a9f44c2014db65a5a7470a2ca5c4cfa3f840b; exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat a1140e76fffdc1be032d9d813dbb686157803bbc refs/heads/main -- .ufo/waves/round-19/runs/t1250-preprofile .ufo/waves/round-19/evidence/receipt-validation/t1250-preprofile.json .ufo/waves/round-19/predictions/t1250-preprofile.prediction.json
# output: 17 files changed, 5201 insertions(+); exit 0

sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py
# output: 6afb7ef6600cdc7907d5eb4af1ac97b9dae1a10c648c50474d249fca2ac2c762; exit 0
```
