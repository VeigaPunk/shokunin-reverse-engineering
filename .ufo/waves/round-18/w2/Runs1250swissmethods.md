# Runs1250swissmethods — wave-2 falsification re-derivation of `s1250-swiss-methods`

HOLDS

Lane REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (= HEAD, verified `git rev-parse HEAD` → exit 0). Freeze commit for predictions `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0`. Axes: (1) raw-log route extraction, (2) frozen-prediction agreement, (3) log/carrier binding, (4) receipt validity. Read-only seat; no tools installed (none needed); no REA analyze/search/decompile, no Ghidra run, no carrier execution; no lane edits.

## 1. Route extraction from raw log lines (observation)

Source: `.ufo/waves/round-18/runs/s1250-swiss-methods/logs/rea-ghidra-KX6ybk/ghidra.log` (6051 lines, 1017306 bytes).

- `ghidra.log:112` — `INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0` → route = **info** (exact/patch-0 path), label = **1.25.0**.
- `ghidra.log:113` — `INFO  (GoRttiMapper) Using Go API snapshot for version 1.25.0`.
- `grep -n -E "GoApiSnapshot|Using Go API snapshot|Go analysis failure|Invalid index|Unable to read past EOF|Untested Go version" ghidra.log` → exit 0, only lines 112–113. So: `Go analysis failure` = 0, `Invalid index:` = 0, `Unable to read past EOF:` = 0, `Untested Go version` = 0.
- Case-insensitive re-scan `grep -in "analysis failure\|past EOF\|invalid index"` → 0 hits.
- `grep -in "fallback"` → 0 hits (no fallback route line).
- All 3 WARN lines in the log are `(GoTypeManager) Failed to get subtype …` (`ghidra.log:3933-3935`) — not route/failure fields.

## 2. Frozen prediction agreement (observation)

`git show eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/predictions/s1250-swiss-methods.prediction.json` (exit 0). Byte-identity: working tree sha256 = `git show eb6c2668:…` sha256 = REV `predictions/SHA256SUMS` entry = `17d2a1c398debbdb4db1af7e6ad741da5d3b08e747726a51639a1443cf010599`; `diff` of eb6c2668 vs REV blob → identical. Receipt `pins_pre` records the same prediction sha256.

| Field | Predicted (frozen) | Observed (raw log / observation.json) | Verdict |
|---|---|---|---|
| snapshot_route | `info` | `info` (ghidra.log:112, GoApiSnapshot component) | HOLDS |
| snapshot_label | `1.25.0` | `1.25.0` (ghidra.log:112-113) | HOLDS |
| fallback_to | `null` | none (0 fallback lines; snapshot_fallbacks `[]`) | HOLDS |
| untested_version | `null` | none (0 `Untested Go version` lines) | HOLDS |
| missing_bootstrap | `false` | `false` (bootstrap_attempts 1; `Reading Go binary info` ghidra.log:111) | HOLDS |
| extra.analyzer_errors_empty | `true` | `analyzer_errors: []`, 0 failure lines | HOLDS |
| extra.eof_reads | `[]` | 0 `Unable to read past EOF:` lines | HOLDS |
| extra.invalid_index_reads | `[]` | 0 `Invalid index:` lines | HOLDS |
| carrier.sha256 | `62e045851c08…c40a5` | `sha256sum` of carrier = same; size 2270905 | HOLDS |
| in_declared_range / input / normalized | `true` / `go1.25.0` / `1.25.0` | consistent with info route at 1.25.0 | HOLDS |

`compare.json` (committed at REV, byte-identical to tree — `diff` vs `git show REV:…compare.json` → identical) reports `all_match: true` on the same 8 fields; my independent extraction from raw lines agrees with every observed value it records. `observation.json` also byte-identical at REV.

Mechanism note (inference, from frozen blob only): `predictions/swiss-misread/s1250-swiss-methods.json` (REV sha256 `2c2cc5bde667b6819ac10b8bc44219f92580b7bc6781011d29bceff1bf56a4d1`) has `predicted_failure_h1: false`, `predicted_eof_reads_h1: []`, `predicted_failure_kind_h1: "none"`, `diagnostic: false` — H1 predicts the `*main.Counts` uncommon misread (h1 addr 4920376/mcount 0/pkg_path 24 vs true 4920400/mcount 2/pkg_path 558) stays in bounds → silent, no log symptom. The observed empty failure set is therefore the exact H1 outcome for this non-D synthetic label, consistent with the frozen decision rule ("no non-D synthetic label shows a failure"). Not a mechanism verdict on its own (non-diagnostic by design).

## 3. Log binding and carrier identity (observation)

- Session path: `ghidra.log:2` `Using log file: /tmp/kr17-rea-am0np5dt/rea-ghidra-KX6ybk/ghidra.log`; retained copy lives at `logs/rea-ghidra-KX6ybk/` (same session id); receipt `bound_sessions = ['/tmp/kr17-rea-am0np5dt/rea-ghidra-KX6ybk']`, `unbound_sessions = []`. HOLDS.
- target-<sha12>: `ghidra.log:46` `IMPORTING: file:///tmp/kr17-rea-am0np5dt/rea-ghidra-KX6ybk/target-62e045851c08.bin`; `62e045851c08` = first 12 hex of the carrier sha256; also at `ghidra.log:65,105,111,6045,6051`. HOLDS.
- MD5: `ghidra.log:65` `Loading file:///tmp/…target-62e045851c08.bin?MD5=690d46d7ee923b9ffefa92be991bb502...`; independent `md5sum` of the carrier = `690d46d7ee923b9ffefa92be991bb502` = receipt `carrier.md5_pre`. HOLDS.
- Carrier sha256: `sha256sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-methods` → `62e045851c08948dc27f2772c110834e06893708f65c61a8e7bd8c38932c40a5` = prediction = receipt `sha256_pre`=`sha256_post`; size 2270905 matches receipt pins and misread blob. HOLDS.
- Log identity: `sha256sum` retained ghidra.log = `3cfd8ca4b08a91b5776327134bb4b85322140538b056050206b71e17702d13df` = observation.json `log_sha256` = receipt `steps.analyze.retained_logs[0].files["ghidra.log"].sha256` = `git show REV:…ghidra.log | sha256sum`. script.log sha256 `1d3a6ea1590b6f430a9a7b74899aee9b3a9b52a77589a287b4daf09ffdcb0a75` matches receipt. HOLDS.
- Producer: `producer.json` `branch: main`, `branch_tip: eb6c2668…` (the freeze commit) at `recorded_at_utc 2026-10-20T16:28:12Z`; analyze argv `npx -y rea-agents@6.5.0 analyze <carrier> --format json` (REA CLI only). HOLDS.
- Exits: `carrier-run.exit` 0, `compare.exit` 0, `observation.exit` 0; `analyze.stderr`/`carrier-run.stderr`/`inspect-go.stderr` empty (0 bytes). HOLDS.

## 4. Receipt validity (observation)

`python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/s1250-swiss-methods/receipt.json` → **exit 0**; `valid: 1, invalid: 0, unreadable: 0`, `checks_performed: 360`, `findings: []`, `require_mid_maps: true`, `pins_available: true`. Mid-run pin map committed at REV: `pins/mid-1.json` sha256 `8b3dfccba7aaeb495dc2be1d0baf644632d40ba14c9968a1820af087de6c1c68` = receipt `steps.analyze.pin_checks[0].map_sha256` (152 entries, `equal: true`, `changed/missing: []`). HOLDS.

## Commands (paste, with exit codes)

```
$ grep -n -E "GoApiSnapshot|Using Go API snapshot|Go analysis failure|Invalid index|Unable to read past EOF|Untested Go version" <run>/logs/rea-ghidra-KX6ybk/ghidra.log
112:2026-10-20 13:28:16 INFO  (GoApiSnapshot) Using Go API snapshot for 1.25.0
113:2026-10-20 13:28:16 INFO  (GoRttiMapper) Using Go API snapshot for version 1.25.0
# exit 0 (only matches shown; failure/EOF/index/untested patterns: 0 hits)

$ grep -in "analysis failure\|past EOF\|invalid index" <run>/logs/rea-ghidra-KX6ybk/ghidra.log
# exit 1 (no matches)

$ sha256sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-methods
62e045851c08948dc27f2772c110834e06893708f65c61a8e7bd8c38932c40a5  …  # exit 0
$ md5sum /home/vgpnk/.local/share/kaidoku-r18/carriers/s1250-swiss-methods
690d46d7ee923b9ffefa92be991bb502  …  # exit 0

$ git show eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0:.ufo/waves/round-18/predictions/s1250-swiss-methods.prediction.json | sha256sum
17d2a1c398debbdb4db1af7e6ad741da5d3b08e747726a51639a1443cf010599  -  # exit 0 (== tree == REV SHA256SUMS == receipt pins_pre)

$ git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/runs/s1250-swiss-methods/logs/rea-ghidra-KX6ybk/ghidra.log | sha256sum
3cfd8ca4b08a91b5776327134bb4b85322140538b056050206b71e17702d13df  -  # exit 0 (== retained file == observation.json == receipt)

$ python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/s1250-swiss-methods/receipt.json
{"counts":{"invalid":0,"receipts":1,"unreadable":0,"valid":1},"exit":0,…,"require_mid_maps":true,…}  # exit 0
```

(`<run>` = `.ufo/waves/round-18/runs/s1250-swiss-methods`.)

## Residual risk and verification gaps

- Receipt-declared limitation (observation, `receipt.json` `log_capture_limit`): the retained log is a polling copy; lines written after the final poll before REA deleted its runtime root could be missing. Mitigated but not eliminated by the four-way sha256 equality above; a post-poll trailing failure line would be invisible. No counter-evidence found.
- The 3 `GoTypeManager` subtype WARNs (ghidra.log:3933-3935) are outside the compared field set; they are not route/failure/EOF/index lines (observation). No claim about them is made by the prediction.
- I did not re-run REA/Ghidra or re-derive the emulator law (contract forbids; frozen blobs taken as given). Route/field verdicts rest solely on the retained raw log, which is byte-identical at REV.
- `snapshot_label` is non-discriminating per compare.json rules (request echo); the independent raw-log extraction removes reliance on that rule for this label.

Per-field verdicts: all HOLDS. Overall: **HOLDS**.
