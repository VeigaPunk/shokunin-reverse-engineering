# ExecC1Base — independent R72-C1 BEFORE measurement

Axes: direct observation, baseline reproducibility, producer-binding separation, secret minimization.

## Result

The round-71 checker accepted the genuine round-71 receipt (exit **0**, `met: true`, `failing: []`, carriers 4/4), while every observed checker child inherited the caller environment. This independently reproduces the BEFORE defect; no lane probe was imported or run.

Invocation: `/usr/bin/python3 -I -B tools/round-71/packed-elf.py --root . --rev b827a8b5d54f2885ec9be7786389f356c59226ce --pkg /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --work /fast/scratch/hyaku/kaidoku-r72/ExecC1Base/r71/work --check-receipt .ufo/waves/round-71/w1/ExecC1/c1-route.json --nonce-commitment 20256a954f2613bef25019a6b8c260883cb5f852a624e3af7a5335005326822e`.

Cwd: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Shim directory first on PATH; shims execute `/usr/bin/git` and `/usr/bin/readelf` after observing their own `/proc/self/environ`.

## Verbatim permitted fields, each shim record

All five records have exactly **275 keys**. First 20 sorted keys (truncated, not an allowlist):

`AGENT`, `ALACRITTY_LOG`, `ALACRITTY_SOCKET`, `ALACRITTY_WINDOW_ID`, `AWS_PAGER`, `BACKGROUND`, `BAT_PAGER`, `BAT_THEME`, `BINARYEN_ROOT`, `BORDER_BACKGROUND`, `BORDER_FOREGROUND`, `CARGO_TERM_PROGRESS_WHEN`, `CI`, `CLAUDECODE`, `CLOUDSDK_CORE_DISABLE_PROMPTS`, `COLORTERM`, `COMPOSER_NO_INTERACTION`, `CUDA_PATH`, `DBUS_SESSION_BUS_ADDRESS`, `DEBIAN_FRONTEND`.

| Record | Child / operation | Canary present | HOME | TMPDIR |
|---|---|---|---|---|
| 1 | git show round-71 instrument | true | `/home/vgpnk` | `/fast/scratch/hyaku/kaidoku-r72/ExecC1Base/caller-tmp` |
| 2 | readelf -h /usr/bin/jq | true | `/home/vgpnk` | `/fast/scratch/hyaku/kaidoku-r72/ExecC1Base/caller-tmp` |
| 3 | readelf -h /usr/bin/xxd | true | `/home/vgpnk` | `/fast/scratch/hyaku/kaidoku-r72/ExecC1Base/caller-tmp` |
| 4 | readelf -h /usr/lib/libz.so.1.3.2 | true | `/home/vgpnk` | `/fast/scratch/hyaku/kaidoku-r72/ExecC1Base/caller-tmp` |
| 5 | readelf -h /usr/bin/docker-init | true | `/home/vgpnk` | `/fast/scratch/hyaku/kaidoku-r72/ExecC1Base/caller-tmp` |

Canary value in each: `ExecC1Base-r72-before`. Both HOME and TMPDIR are outside the round-71 `--work` root. Full key sets, argv and permitted values are retained in `ExecC1Base/r71.shim.jsonl`; all other values, including credentials/session material, are not decoded or logged.

## Separate control: producer binding, NOT C1 landing evidence

Ran the round-72 checker against the **same unchanged round-71 receipt**, with `--rev 34fe7aa70b627d92e2d27dbce308d9f5bebda63d` and work `.../ExecC1Base/r72/work`. The operative freeze is necessary: the round-71 revision has no round-72 instrument blob.

Exit **1**, `met: false`; the complete failure list consists of:

- `instrument.path tools/round-71/packed-elf.py != tools/round-72/packed-elf.py`
- `instrument.sha256 5cf95aaa0892c4e4f1b82edb60590b57e6667467ed607b15989bb867e7d8efe0 != blob at 34fe7aa70b627d92e2d27dbce308d9f5bebda63d (973d504b415c58c1cc84896057322ce99c2db2762551de3b13f0c87f17ffefe7)`
- `rev b827a8b5d54f2885ec9be7786389f356c59226ce != 34fe7aa70b627d92e2d27dbce308d9f5bebda63d`

Five shim records in this control contain exactly `HOME, LANG, PATH, TMPDIR`, no canary; HOME/TMPDIR lie inside its work root. These observations are retained for transparency only, **not scored as R72-C1 evidence**. No claim about the round-72 landing receipt is made.

## Evidence and limits

Exclusive evidence directory: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-72/w1/ExecC1Base/`:

- `harness.py`: independent reproducible driver (no probe dependency).
- `r71.stdout.json`, `r71.stderr.txt`, `r71.shim.jsonl`, `r71.result.json`.
- `r72.stdout.json`, `r72.stderr.txt`, `r72.shim.jsonl`, `r72.result.json`.
- `summary.json`: invocation, hashes, verdicts and per-record summaries.
- `Report.md`: report locator and result.

The first harness invocation used a Linux-incompatible multi-flag shebang and observed no children (both checkers exit 2). Corrected the shim shebang to the single `-I` argument; the retained receipts are the subsequent successful measurements above. No lane source changed. No tools installed or updated. No build/lint/formatter/suite run. LSP is unavailable in this seat's exposed tools; no symbol edit/refactor was needed. A scratch UPX copy and its SHA-256 are recorded by the harness; checker mode does not execute UPX. Scratch captures were copied into the lane before `finally: shutil.rmtree(S)` removed the sole scratch root.

Risks: host key inventory is ambient and may change on reproduction; non-permitted environment values are deliberately absent. This is a BEFORE measurement and cross-producer control, not proof of all route children or all three round-72 claims.

Self-evaluation (evidence-bound): accuracy 4/5 (direct shim observations; initial harness error disclosed); completeness 4/5 (requested observations and producer rejection retained; sensitive values intentionally excluded); clarity 4/5 (control clearly separated, long ambient key inventory retained once); actionability 5/5 (driver, argv, raw permitted observations and verdicts retained); conciseness 4/5 (per-record table needed for independent evidence). Overall 4.2/5. Improvement: compare parent-owned C1 landing evidence separately rather than treating this rejection control as acceptance. The user should agree that the scoped baseline deliverable is complete.
