# W2 re-derivation — carrier run `s1246-noswiss-nomethods`

HOLDS

Seat: KaidokuR18.Runs1246noswissnomethods (leaf, read-only; no installs performed — pacman pause respected, no tool added).
REV = `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`; freeze = `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`.
All cited run artifacts are byte-identical at REV vs worktree (verified: `git show REV:<f> | cmp - <f>` → IDENTICAL for observation.json, receipt.json, compare.json, ghidra.log, script.log), so `path:line` below is valid at REV. Prediction blob is byte-identical freeze→REV→worktree (`diff` exit 0 both ways).

## Commands run (with exit codes)

```
cd .ufo/waves/round-18/runs/s1246-noswiss-nomethods/logs/rea-ghidra-jDVuh0
grep -n -E "\(GoApiSnapshot\)|Go analysis failure|Invalid index:|Unable to read past EOF:" ghidra.log   # exit=0 (1 hit, line 113)
grep -c "ERROR (Golang" ghidra.log          # 0, exit=1
grep -c -i -E "go analysis failure|invalid index|past EOF" ghidra.log   # 0, exit=1
grep -c "Untested Go version" ghidra.log    # 0, exit=1
grep -c "Missing Go bootstrap type info" ghidra.log   # 0, exit=1
sha256sum ghidra.log      # cc00ad4d8f37f415e5bcab22e865945e298edf8773aedbe0c67d910aaf1acfe0
sha256sum script.log      # 12f7a356143f3871eeea67e3267ff7b10e1cb428a68072452c38b4a84b4961ea
sha256sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-noswiss-nomethods
                          # e06aae7909c1dff17c1f51356f576995714fd96f98956c21a1a1cfee7b72549d
md5sum  /home/vgpnk/.local/share/kaidoku-r18/carriers/s1246-noswiss-nomethods
                          # c339635d9be4049c822dd63d00cc4289
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps \
  .ufo/waves/round-18/runs/s1246-noswiss-nomethods/receipt.json   # exit=0
```
Validator output: `{"counts":{"invalid":0,"receipts":1,"unreadable":0,"valid":1},"exit":0,"pins_available":true,"require_mid_maps":true,"receipts":[{"checks_performed":360,"findings":[],"kind":"carrier","status":"valid","valid":true}]}`.

## Per-field verdicts (prediction at freeze, lines per `git show eb6c2668:.ufo/waves/round-18/predictions/s1246-noswiss-nomethods.prediction.json`)

| Field | Predicted | Independently observed | Verdict |
|---|---|---|---|
| snapshot_route | `info` (:34) | exactly one GoApiSnapshot record, INFO, `Using Go API snapshot for 1.24.6` — ghidra.log:113; zero GoApiSnapshot WARN/fallback lines (grep exit 0, single hit) | HOLDS |
| snapshot_label | `1.24.6` (:33) | ghidra.log:113 (GoApiSnapshot), echoed :114 (GoRttiMapper), `Go version 1.24.6` :221 (GolangSymbolAnalyzer) | HOLDS |
| fallback_to | `null` (:31) | no `Falling back from …` line (FALLBACK_RE, log-extract.py:103 REV); observation.snapshot_fallbacks=[] (observation.json:164) | HOLDS |
| missing_bootstrap | `false` (:32) | no `Missing Go bootstrap type info` (grep exit 1; text def log-extract.py:97, check :240-241); bootstrap_attempts=1 = one `Reading Go binary info:` READING_RE match (log-extract.py:106,296) at ghidra.log:112 | HOLDS |
| untested_version | `null` (:35) | no `Untested Go version` (grep exit 1); observation.untested_versions=[] (observation.json:170) | HOLDS |
| extra.analyzer_errors_empty | `true` (:38) | 0 ERROR lines from components starting `Golang` (grep exit 1; definition log-extract.py:243-244 REV); observation.analyzer_errors=[] (observation.json:2) | HOLDS (scoped — see caveat 1) |
| extra.eof_reads | `[]` (:39) | zero `Unable to read past EOF:` anywhere, case-insensitive (grep exit 1; extractor anchors end-of-line, log-extract.py:113) | HOLDS |
| extra.invalid_index_reads | `[]` (:40) | zero `Invalid index:` anywhere (grep exit 1; log-extract.py:114) | HOLDS |
| carrier.sha256 | `e06aae79…549d` (:28) | computed sha256 of the on-disk carrier = identical; receipt sha256_pre == sha256_post == same (receipt.json:8-9) → no mutation | HOLDS |
| input / normalized | `go1.24.6 X:noswissmap` / `1.24.6` (:43-44) | inspect-go.json build_info.go_version = `go1.24.6 X:noswissmap`, module settings `GOEXPERIMENT=noswissmap, GOARCH=amd64, GOOS=linux`; artifact sha256/bytes match | HOLDS |
| selection base/diff | go1.24.0.json `aab28c8f…`/10039962 (:54-55); go1.24.6.json.diff `e169e8dd…`/118810 (:73-74) | receipt pins_post entries carry exactly these sha256+size; on-disk Ghidra typeinfo files hash identically today | HOLDS |
| c3 block | diagnostic=false, h0=h1=none, H1 frozen, emulator swiss-misread.py `14924bd6…` (:15-25) | pinned swiss-misread.py sha256 = `14924bd6…` (= prediction emulator_sha256 = producer tool_sha256); decision-rule.json:60-70 row matches (non-diagnostic, h0/h1 none, route info) | HOLDS |

## Log binding chain (decision-rule.json:2 gate)

- Session path: ghidra.log:2 `Using log file: /tmp/kr17-rea-iimd1bcb/rea-ghidra-jDVuh0/ghidra.log` == receipt bound_sessions[0] (receipt.json:2) == retained session_dir (receipt.json:1911). HOLDS.
- target-<sha12>: ghidra.log:65 `Loading file:///tmp/kr17-rea-iimd1bcb/rea-ghidra-jDVuh0/target-e06aae7909c1.bin?MD5=c339635d9be4049c822dd63d00cc4289...`; `e06aae7909c1` = first 12 hex of the carrier sha256; observation.import_target (observation.json:154) agrees. HOLDS.
- MD5: log:65 MD5 `c339635d9be4049c822dd63d00cc4289` == receipt.carrier.md5_pre (receipt.json:6) == computed `md5sum` of the carrier file. HOLDS.
- Retained bytes: computed ghidra.log sha256 `cc00ad4d…` and script.log sha256 `12f7a356…` == receipt.json:1900-1908; receipt binding flags logfile_ok/md5_ok/target_ok all true (receipt.json:1892-1896). Log ends with `\n` (no torn final line). HOLDS.
- Prediction blob unchanged from freeze commit: `diff` exit 0 freeze↔worktree and REV↔worktree. HOLDS.
- Tool identity: all 7 pinned tools (carrier-run, pins, log-extract, compare, receipt-validate, swiss-misread, selection) — working-tree sha256 == producer.json tool_sha256 == `git show REV:` blob sha256 (7× REV_MATCH). The validator I ran is the one recorded. HOLDS.
- Mid-run pin map: pins/mid-1.json sha256 `8568eef8…` == receipt steps.analyze.pin_checks[0].map_sha256 (receipt.json:1938); --require-mid-maps path is receipt-validate.py:453-467 REV (every pin_checks entry must carry map_path+map_sha256, analyze step ≥1 check). HOLDS.

## C3 rule position (decision-rule.json REV)

- count_rule (:8): this label has a bound retained log (all binding flags true) and compare.json carrying `extra.eof_reads` (compare.json:43-48) → counts toward the 0→15 count. OBSERVATION.
- confirmed clause (:7): this is a non-D synthetic label showing **no** Go analysis failure → satisfies the necessary "no non-D synthetic label shows a failure" condition. It is non-diagnostic, so it cannot confirm H1 by itself (h0=h1=none in its row, decision-rule.json:60-70). INFERENCE (rule application, not new evidence).
- compare.json:2 `all_match: true` over 8 fields (compare.json:5-54) — independently re-derived above, agrees.

## Caveats / residual risk (no defect found; each labeled)

1. OBSERVATION — `analyzer_errors_empty` is definitionally scoped: log-extract.py:243-244 REV collects ERROR lines only from components starting `Golang`. The log contains 5495 ERROR lines from non-Golang components (e.g. DWARFDataTypeImporter "Bad value … for array's size" ghidra.log:107-111; DWARFImportSummary un-recoverable expressions :179-193) plus 3 GoTypeManager WARNs (:873-875). These are outside the frozen field and outside the compared fields; the prediction was frozen against the same extractor, so there is no calibration gap. A reader parsing "analyzer_errors_empty" as "zero ERROR lines in the log" would be misled — the scoped meaning is the frozen one.
2. OBSERVATION — receipt.json:23 `log_capture_limit`: "polling copy; lines written after the final poll before REA deletes its runtime root can be missing" (42 polls, last copy 16:26:44.291Z; analyze step ended 16:26:44.793Z). A post-final-poll line carrying an EOF/index read could in principle be absent from the retained log. Residual risk judged low (log ends with normal completion, ghidra.log tail), but the empty eof/invalid lists are bounded by this disclosed capture limit, not by absolute saturation. INFERENCE.
3. INFERENCE — `snapshot_route=info` derivation: fallbacks=[] and api_info_labels=["1.24.6"] → route `info` per log-extract.py:276-277 REV; only the GoApiSnapshot component discriminates the route (log-extract.py:98-102 comment; GoRttiMapper :114 echoes the requested version). Consistent with prediction basis (GoApiSnapshot.java:148-166).

## Findings

None. No field contradicts the frozen prediction; binding chain, validator, tool identity, and freeze immutability all verified. No reproducing defect exists to cite.

## Verification gaps

- I did not re-run the REA analyze step itself (out of scope: no REA analyze/search/decompile, no carrier execution); re-derivation is from the retained log + receipt + hashes.
- The `md5_ok`/`target_ok` flags were re-checked semantically (log:65 vs computed hashes) rather than by re-running carrier-run.py's binding code.
