# w2 / Runs1246swissmethods — independent re-derivation of carrier run `s1246-swiss-methods`

HOLDS

All predicted fields re-derive from the raw retained log; log binding, carrier digest, freeze integrity, and `receipt-validate.py --require-mid-maps` all check out. No installs were performed (pacman pause respected; none needed).

Evidence anchors: REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`, freeze `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. Paths below relative to repo root; `L` = `.ufo/waves/round-18/runs/s1246-swiss-methods/logs/rea-ghidra-mXzzav/ghidra.log` (5,828 lines).

## Commands run (all exit 0 unless noted)

1. `git show eb6c2668:…/predictions/s1246-swiss-methods.prediction.json` — EXIT=0
2. `diff` freeze-blob vs `git show REV:…prediction.json` vs worktree → `REV==FREEZE`, `WORKTREE==REV` — EXIT=0
3. `grep -n "GoApiSnapshot\|Go analysis failure\|Invalid index:\|Unable to read past EOF:\|Untested Go version\|Using Go API snapshot" $L` — EXIT=0, only matches L:111-112
4. `sha256sum` / `md5sum` carrier; `sha256sum ghidra.log script.log`
5. `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/s1246-swiss-methods/receipt.json` — EXIT=0: `valid:1, invalid:0, checks_performed:360, findings:[]`, `pins_available:true`
6. `sha256sum -c predictions/SHA256SUMS` from `.ufo/waves/round-18/` — exit 0, 32 `: OK`, 0 FAILED
7. `compare.exit`, `observation.exit`, `carrier-run.exit` — each `0`; per-pattern counts via `grep -c` (0 each, exit 1 = no match, expected)

## Field verdicts (each: predicted vs my raw-log extraction — OBSERVATION unless labeled)

| Field | Predicted (freeze blob) | Observed (raw log) | Verdict |
|---|---|---|---|
| snapshot_route | `info` | `INFO (GoApiSnapshot) Using Go API snapshot for 1.24.6` at L:111; zero `WARN (GoApiSnapshot)` lines → route `info` | HOLDS |
| snapshot_label | `1.24.6` | L:111 (GoApiSnapshot) and L:112 (GoRttiMapper) both say `1.24.6` | HOLDS (non-discriminating request echo — compare.json rules note this; route is the discriminating field) |
| untested_version | `null` | zero `Untested Go version` matches in 5,828 lines | HOLDS |
| missing_bootstrap | `false` | bootstrap attempt present (L:110 `Reading Go binary info`, `bootstrap_attempts:1`); no GoRttiMapper missing-bootstrap line | HOLDS |
| fallback_to | `null` | zero GoApiSnapshot fallback lines; `snapshot_fallbacks:[]` | HOLDS |
| extra.eof_reads | `[]` | zero `Unable to read past EOF:` matches anywhere in L | HOLDS |
| extra.invalid_index_reads | `[]` | zero `Invalid index:` matches anywhere in L | HOLDS |
| extra.analyzer_errors_empty | `true` | zero `Go analysis failure`; zero `ERROR (Golang*` lines | HOLDS under the frozen scope rule — see R1 below |

compare.json `all_match:true` reproduces independently; all three step exits are 0.

## Binding and custody

- Session path: receipt `bound_sessions[0]` = `retained_logs[0].session_dir` = `/tmp/kr17-rea-t18t8d1r/rea-ghidra-mXzzav` = logs dir name = `import_target` in observation.json; log self-identifies the same session at L:46, L:63, L:104, L:5822, L:5828.
- target-sha12: L:46 `IMPORTING …/target-f8205baadc27.bin`; `f8205baadc27` = first 12 hex of carrier sha256 — OBSERVATION.
- MD5: L:63 `?MD5=5475d396e70395cb0b3bbf75556cfd10` = receipt `md5_pre` = my fresh `md5sum` of the live carrier — OBSERVATION.
- Log integrity: my `sha256sum` ghidra.log `bd33648e5a8b…7ff1712`, script.log `dd49ace32579…aba5f63` = receipt `retained_logs[0].files.*.sha256` = observation `log_sha256`/`log_bytes` (975,271 B) — OBSERVATION.
- Carrier sha256: live `f8205baadc27fcf8f5a7f13bd5e68ce2522ec70a11cb768ee5b1f61c62aa48ac` = prediction `.carrier.sha256` = receipt `sha256_pre`=`sha256_post` — OBSERVATION.
- Freeze: prediction blob byte-identical across eb6c2668 → REV → worktree; `SHA256SUMS` entry `98a2187f96ccdf338102e6b5eadbae47f5bef4410277adbd55bbc9ccb6da3bd9` matches; manifest 32/32 OK; freeze commit 16:23:55Z predates run start 16:26:45Z (receipt `steps`) — OBSERVATION.
- receipt-validate exit 0 with `--require-mid-maps`; `pins/mid-1.json` present (152 entries, `pins_compare.equal:true`, pre 16:26:44.99Z / post 16:27:07.35Z) — OBSERVATION.

## Findings

**R1 (observation, no defect): `analyzer_errors_empty` is scoped, not absolute.** The raw log contains 5,554 `ERROR (GoFuncData) Failed to add source file mapping: new entry would overlap …` lines (e.g. L:221, L:5777) and 47 DWARF ERROR lines (5 `DWARFDataTypeImporter`, 42 `DWARFImportSummary`). log-extract.py's rule (`level=="ERROR" and component.startswith("Golang")`, .ufo/waves/round-17/tools/log-extract.py:243-244; failure text "Go analysis failure" per GolangSymbolAnalyzer Msg.error, :24-34,115) excludes both classes. The frozen expectation targets the map-read failure signature only, so `analyzer_errors_empty:true` is honest — but the field name overpromises if read as "no analyzer errors". INFERENCE: the overlap noise is DWARF comp-dir related and mechanism-irrelevant; it appears unrelated to Swiss-map reads (no EOF/index/failure signature co-occurs).

**R2 (observation): capture-tail risk is real but does not touch compared fields.** receipt `log_capture_limit` declares a polling copy; last poll 16:27:06.803Z vs analyze step end 16:27:07.305Z, and L's last line (5828) is `ANALYZING changes made by post scripts` — teardown lines may be missing. All route/EOF/index/failure lines occur 13:26:47–13:26:54 local, well before the final poll, so post-poll loss cannot alter any compared field. INFERENCE.

**R3 (observation): 3 `WARN (GoTypeManager)` lines (L:3480-3482, subtype failures echoing the DWARF bad array sizes at L:105-109) are not GoApiSnapshot WARNs** and do not affect `snapshot_route` (derived from GoApiSnapshot component only, log-extract.py:271-279).

**R4 (inference, scope note): this label is non-diagnostic.** decision-rule.json `diagnostic_set_D` = {calib-aether, s1246-swiss-nethttp, real-kimi-webbridge}; s1246-swiss-methods contributes only the "no non-D synthetic label shows a failure" conjunct of `confirmed`. Its 8/8 field match plus satisfied binding gate (valid receipt, carrier sha equal to prediction, blob unchanged since freeze) makes it count toward C3's bound-label count; it cannot alone confirm or refute the mechanism.

## Residual risk / verification gaps

- Could not and did not re-run REA (lane contract) — re-derivation is from the retained raw log only; authenticity of the log rests on the sha256 agreement between receipt, observation.json, and the live files, plus in-log session/MD5 self-identification.
- `compare.py`/`log-extract.py` logic was read (pinned copies) but not re-executed against the log; the per-field table above is my independent grep-based extraction and agrees with their outputs everywhere they were checked.
- Receipt `orig_argv` shows `--pin` coverage of the prediction blob pre/post run; I did not re-hash all 152 pin entries (receipt-validate's 360 checks passed; pins/mid-1.json sha256 `20f9f479…` recorded).
