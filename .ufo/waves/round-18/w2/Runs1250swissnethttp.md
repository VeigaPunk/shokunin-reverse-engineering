HOLDS

# W2 falsify — carrier run `s1250-swiss-nethttp` (independent re-derivation)

Seat: KaidokuR18.Runs1250swissnethttp (leaf, no subagents). REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`; `git rev-parse HEAD` → `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (exit 0), so working-tree line numbers are valid at REV. Blob-identity at REV verified for every artifact cited: `git show REV:<p> | sha256sum` vs `sha256sum <p>` → SAME for receipt.json, observation.json, compare.json, logs/rea-ghidra-I0vJ0A/ghidra.log, analyze.json, producer.json (6/6, exit 0). Prediction blob unchanged from freeze: sha256 `16dc3c0b9788cb4d0f616d11257247d4a5e5e9bb25d85e0a33504d9f1d465864` identical at freeze `eb6c2668`, REV, and worktree (exit 0 ×3). No tool installs (none needed).

## Per-field verdicts

All paths relative to `kaidoku-shokunin/`; log = `.ufo/waves/round-18/runs/s1250-swiss-nethttp/logs/rea-ghidra-I0vJ0A/ghidra.log` (10651 lines). Prediction = frozen `.ufo/waves/round-18/predictions/s1250-swiss-nethttp.prediction.json`.

| Field | Predicted | Independently observed | Verdict |
|---|---|---|---|
| snapshot_route | `info` | Only GoApiSnapshot record is log:179 `INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0`; zero `Falling back from` records | HOLDS |
| snapshot_label | `1.25.0` | log:179 (GoApiSnapshot) and log:180 (GoRttiMapper echo) both `1.25.0` | HOLDS (non-discriminating: request echo — compare.py:19) |
| fallback_to | `null` | `grep -E "Falling back from"` → no match (exit 1); observation.snapshot_fallbacks=`[]` | HOLDS |
| untested_version | `null` | `grep -i "untested"` → no match (exit 1) | HOLDS |
| missing_bootstrap | `false` | `grep "Missing Go bootstrap"` → no match; bootstrap_attempts=1 (single log:178 `Reading Go binary info:`) | HOLDS |
| extra.analyzer_errors_empty | `true` | Zero ERROR records from `Golang*` components (ERROR breakdown below); observation.analyzer_errors=`[]` | HOLDS per frozen definition — see scope note O1 |
| extra.eof_reads | `[]` | `grep -i "past eof"` → no match (exit 1) | HOLDS |
| extra.invalid_index_reads | `[]` | `grep -i "invalid index"` → no match (exit 1) | HOLDS |
| carrier sha256 | `bd12f678…eed4` | computed `bd12f6783479d1f87c83a7a704e445533b4b5d75c3501416df34e9dd41a6eed4` = prediction = receipt sha256_pre/sha256_post = analyze.json subject digest = carriers/SHA256SUMS entry | HOLDS |
| log binding: session path | — | log:2 `Using log file: /tmp/kr17-rea-cj4qb4t6/rea-ghidra-I0vJ0A/ghidra.log` = receipt.bound_sessions[0] = retained_logs[0].session_dir = observation.log_file_line | HOLDS |
| log binding: target-<sha12> | — | carrier sha256[:12]=`bd12f6783479`; present at log:46, :65, :172, :178, :10645, :10651 | HOLDS |
| log binding: MD5 | — | computed md5 `7950fc7d647fe3655f9afd1d0f6d27ed` = log:65 `…target-bd12f6783479.bin?MD5=7950fc7d647fe3655f9afd1d0f6d27ed` = receipt.carrier.md5_pre (md5_ok=true) | HOLDS |
| receipt-validate --require-mid-maps | exit 0 | ran: exit 0, `valid:1 invalid:0 unreadable:0`, findings `[]`, 366 checks, pins_available=true | HOLDS |
| mid-run pins | equal | mid-1/mid-2 sha256 match receipt map_sha256 values; 152/152 pinned file sha256 re-verified on disk, 0 missing; entries identical (only monotonic_ns/taken_at_utc differ) | HOLDS |
| go version input | `go1.25.0` | inspect-go.json `go_version:"go1.25.0"`; log:356 `Go version 1.25.0` | HOLDS |
| base snapshot | go1.25.0.json `54d10162…` size 10081618 | pinned entry `…/typeinfo/golang/go1.25.0.json` sha256+size match exactly | HOLDS |

## Commands pasted (all with exit codes)

```
# route / failure / read markers (exit 0; only 2 hits)
$ grep -n -E "GoApiSnapshot|Go analysis failure|Invalid index:|Unable to read past EOF:|Untested Go version|Using Go API snapshot" <log>
179:2026-10-20 13:30:06 INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0
180:2026-10-20 13:30:06 INFO  (GoRttiMapper) Using Go API snapshot for version 1.25.0

# case-insensitive absence sweep (exit 1 = no match)
$ grep -n -i -E "invalid index|past eof|analysis failure|untested" <log>   # exit 1
$ grep -n -E "Falling back from|Missing Go bootstrap|Invalid Go version" <log>  # exit 1

# carrier identity (exit 0)
$ sha256sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-nethttp
bd12f6783479d1f87c83a7a704e445533b4b5d75c3501416df34e9dd41a6eed4  s1250-swiss-nethttp
$ md5sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-nethttp
7950fc7d647fe3655f9afd1d0f6d27ed  s1250-swiss-nethttp

# receipt validation (exit 0)
$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/s1250-swiss-nethttp/receipt.json
{"counts":{"invalid":0,"receipts":1,"unreadable":0,"valid":1},"exit":0,...,"checks_performed":366,"findings":[],"status":"valid"}

# retained-log integrity (exit 0)
$ sha256sum <log>   # 6ece0aadad5aac290c61bbc961a8d9df84c32765d80ab844a4c29fdea0bfe3a7 = observation.log_sha256; log_bytes 1811252 matches file size

# step exits (exit 0)
$ cat carrier-run.exit compare.exit observation.exit   # 0 / 0 / 0

# ERROR-level component breakdown (exit 0)
$ grep " ERROR " <log> | sed -E 's/^[0-9-]+ [0-9:]+ ERROR +\(([A-Za-z]+)\).*/\1/' | sort | uniq -c
10240 GoFuncData      # "Failed to add source file mapping: new entry would overlap …"
    5 DWARFImportSummary  # log:351-355 "DWARF un-recoverable expressions"
    5 DWARFDataTypeImporter # log:173-177 "Bad value […] for array's size in DIE … forcing to 1"

# prediction blob identity (exit 0 ×3, all 16dc3c0b9788…)
$ git show eb6c2668e5cb…:…/s1250-swiss-nethttp.prediction.json | sha256sum
$ git show b2aad08ceeee…:…/s1250-swiss-nethttp.prediction.json | sha256sum
$ sha256sum .ufo/waves/round-18/predictions/s1250-swiss-nethttp.prediction.json

# producer tool hashes (exit 0; 7/7 MATCH: carrier-run.py, pins.py, log-extract.py, compare.py, receipt-validate.py, swiss-misread.py, selection.py)

# pins verification (exit 0)
$ # mid-1.json sha256 8f05d6f9eea5… / mid-2.json 20a6e5a2164d… = receipt map_sha256 pair; 152/152 pinned entries re-hashed OK
```

## Observations (no mismatch; recorded for calibration)

- **O1 [observation] `analyzer_errors_empty` is definition-scoped.** log-extract.py:244 collects ERROR records only from components whose name starts with `Golang` (GolangSymbolAnalyzer/GolangStringAnalyzer). The log carries 10250 ERROR-level lines (GoFuncData 10240, DWARF* 10) outside that definition, so the field is honest per the frozen contract but does not mean "error-free log". Reproduce: the component breakdown command above. The decision-rule table (frozen decision-rule.json, label `s1250-swiss-nethttp`: `diagnostic:false, h0:none, h1:none, route:info`) needs only "no failure" here — satisfied.
- **O2 [observation] Retained log is a polling copy.** receipt `log_capture_limit` discloses it; `retained_logs[0].last_copy_utc=16:30:34.935Z` vs `steps.analyze.ended_at_utc=16:30:35.937Z` — up to ~1s of trailing lines may be absent. All extracted events are timestamped ≤13:30:14 local (log:356-10611 window), inside the capture window; final retained line log:10651 is newline-terminated (`tail -c 1 | xxd` → `0a`). Low residual risk to the compared fields. [INFERENCE on impact; timestamps are observation]
- **O3 [observation] `snapshot_label` rule is non-discriminating** (request echo, compare.py:19); moot here since route=info and both GoApiSnapshot/GoRttiMapper labels are `1.25.0`.
- **O4 [observation] 4 WARN records, all GoTypeManager subtype lookups** (log:843 `net/http.Request`, log:6249-6251 sized-array types). Not covered by any predicted field; no bearing on route/fallback/reads.

## Verification gaps

- The ~1s tail window in O2 is inherent to the polling capture; not closable from retained artifacts alone.
- observation.json/compare.json are anchored by REV blob identity and tool-hash match, not by an in-receipt recorded digest (receipt steps cover analyze + inspect-go-binary only) — noted, not a defect.

Verdict: **HOLDS** — every frozen prediction field for `s1250-swiss-nethttp` re-derived independently from raw log lines and artifact hashes matches; receipt validation passes with `--require-mid-maps`.
