# R17 w1 — DraftKnowledgeEntry report (author-side advisory, leaf)

## Behavior
Drafted `.ufo/waves/round-17/w1/draft-knowledge-r17.md` as the future `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`. It opens with the `source:` / `verified-at:` / `recheck:` trio. Pilot facts appear only as PILOT. Every unmeasured value is an explicit `<FINAL:...>` slot. The draft includes a prediction-vs-observation table skeleton, observation/inference/unknown labels (QUALITY #5), and a NOT-examined section (QUALITY #7).

## Gates
- Trio rule: `/home/vgpnk/Projects/shokunin/CORPUS.md:163-170` (the file is at the workspace root, not under `kaidoku-shokunin/`). It requires the trio first and `S###` citations for external sources. The draft's `source:` cites S003, S023 (scope-limited) and S004 (contrast, with URL).
- Pilot integrity: `sha256sum -c pilot/SHA256SUMS` returned OK for all six files. Both carrier SHA-256 values match the pilot README.
- Anchor check: I reopened S003 members from `Base-src.zip` (`GoRttiMapper.java:79,114-125,170-172,331,351-367`; `GoApiSnapshot.java:115,118-128,148-166,205-240,503-505`; `GoVer.java:65,67-68,149`; `GoVerRange.java:83-86`; `GoBuildInfo.java:488-489`; `GolangSymbolAnalyzer.java:133-139`; `DataTypeMapper.java:172-181`). All cited anchors match the text. The r14 anchors match too.
- Pilot log lines: `shfmt-log/ghidra.log:82-89` and `esbuild-0.25.12-log/ghidra.log:62-85` were read directly and match the draft's quotes.

## Findings (with anchors)
1. **Version normalization trap (INFERENCE, regex re-evaluated).** `GoVer.java:65` applied to the literal `go1.27.0-X:nodwarf5` yields `""` and therefore `INVALID`. The `go` strip at `GoBuildInfo.java:488-489` must run first. A predictor that skips it will misclassify every real carrier. The FINAL predictor must strip `go` before calling the `GoVer.java:65` rule.
2. **Source-model predictions** (SOURCE-MODEL, run 2026-10-20 with `round-16/selection.py`):
   - shfmt `1.27.0` → `missing_base`, base null (no `go1.26.0.json` or `go1.27.0.json` installed; installed bases span go1.15–go1.25).
   - esbuild `1.23.12` → `exact_diff`, base `go1.23.0.json` SHA-256 `3b1d795f…692`, diff `go1.23.12.json.diff` SHA-256 `e1fdbc7e…c53`, patch 12.
3. **PILOT vs source route.** The shfmt log matches the bootstrap route: `ghidra.log:83` Untested `[1.27.0]`, `:84` Missing bootstrap WARN, `:85` `unable to get GoRttiMapper`, repeated for `GolangStringAnalyzer` at `:86-89`. The esbuild log matches the snapshot route: `:63-64` Using snapshot `1.23.12`, `:67` Go version. Hand-read agreement only; `compare.py` is not run.
4. **Unpredicted observations, reported not scored.** esbuild `:68-70` three `GoTypeManager` "Failed to get subtype" WARNs (cause UNKNOWN); `:65-66` 188 unindexed / 4881 types; `:85` 19 missing type names. Both carriers' `binary_overview` counts (`pilot/shfmt.json`: 2581/7813; `pilot/esb.json`: 8109/17573) are Ghidra default-analysis output and are not Go-recovery evidence.
5. **Log binding.** Logs name the target only by hash prefix (`target-58f765638eed.bin`, `target-bab29b2ca7a9.bin`); identity runs through the SHA-256 pin. Pilot pins were not recorded (`pilot/README.txt`). `REA no-return fix` lines appear in both `script.log` files; their effect on Go analysis is UNKNOWN.
6. **Second-pass duplication (UNKNOWN).** The shfmt Go failure repeats under two analyzers. The cause was not read (`getSharedGoBinary` not opened).
7. **Pins and versions.** Provider identities recorded: `rea-agents@6.5.0`, `rea-workflow` v1 over Ghidra 12.1.4; `go-build-info` v1 for inspect output. JDK not examined.

## Carriers identified (this draft, read-only)
- `/usr/bin/shfmt` SHA-256 `58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459`, 3601168 bytes, `go1.27.0-X:nodwarf5` (`inspect-go-binary` evidence `ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a`).
- esbuild 0.25.12 at the pnpm path in `draft-knowledge-r17.md` SHA-256 `bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014`, 10358936 bytes, `go1.23.12` (evidence `ev_0cabcc66620bf9f201e2b0aaba63d9bd1998b4e498ec823c01dc186a73041626`). The path is a mutable pnpm directory under another project.

## Commands run (no analyze/search/decompile/Ghidra headless; no carrier execution)
- `sha256sum -c` on pilot SHA256SUMS; `sha256sum` on both carriers, Base-src.zip, `go1.23.0.json`, `go1.25.0.json`.
- Python `zipfile` read-only over Base-src.zip members (no extraction to disk).
- `python3 -I .ufo/waves/round-16/selection.py --root …/data/typeinfo/golang --request {1.27.0,1.23.12} --goos linux --goarch amd64` (stdout only).
- `npx -y rea-agents@6.5.0 inspect-go-binary <carrier> --format json` ×2 (allowed by contract).
- One regex re-evaluation in Python for `GoVer.java:65`.
- `pacman -Q unzip` (read-only query; not used for installs).

## Tool/install record
- No tools installed or upgraded by this seat. `npx` may have populated its cache on first `rea-agents@6.5.0` fetch; that is the only package-manager side effect.

## Out-of-scope items
- No `analyze`, `search`, `decompile` or Ghidra headless run (contract).
- No edits to LOG, SCORECARD, QUALITY, SKILL, SHONEN, SOURCES, PROVINCE, README, knowledge or lessons; no commit or push.
- No predictor, compare or log-extract tool written (executor scope).
- No S### rows were added; a new Go `debug/buildinfo` row is referenced in the claims but not present in SOURCES, so the draft cites none for it.

## Limits
- Every PILOT number is pre-final; the logs are 1-second poll copies and may miss tail lines.
- Source reading is of S003, not of loaded classes; the Python `selection.py` is a source model, not Java/Gson.
- `missing_bootstrap` has two possible causes (missing base vs. no applicable records); the pilot cannot separate them, and the shfmt base is absent.
- No go1.20.12 carrier, no non-linux selection, no upstream release check.

## Artifact paths
- Draft: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/w1/draft-knowledge-r17.md`
- Report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/w1/DraftKnowledgeEntry.md`

## Checks for the main agent after FINAL
- Fill every `<FINAL:...>` slot from receipts; run `receipt-validate.py` and `compare.py` on the retained prediction/observation JSON.
- Confirm the predictor strips the `go` prefix before `GoVer.java:65` (see Finding 1); a `go1.27.0-X:nodwarf5` input must yield `1.27.0`, not INVALID.
- Confirm the `verified-at:` and `recheck:` placeholders are replaced with real dates and argv.
