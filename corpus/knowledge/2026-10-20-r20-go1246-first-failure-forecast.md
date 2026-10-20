source: S047 (official go1.24.6 linux-amd64 archive: carrier provenance only), S035 (Go internal/abi map layout), S023 (Ghidra installed Go data), S003 (Ghidra source; `GoFuncType.java:65,79,86` variadic mask, `GolangSymbolAnalyzer` single try/catch — wave-1 `ScoutGhidraVariadic.md`); frozen predictions `.ufo/waves/round-20/predictions/` at freeze `808cbb31a1e24656da5ba4967497e602fbca7415`; runs `.ufo/waves/round-20/runs/` (observed outcome authority).
verified-at: 2026-10-20 — REA CLI pinned to rea-agents@6.5.0, Ghidra 12.1.4. Freeze committed 18:01:54 -03 and pushed by the lane helper before the runner started (`runs-start.txt`, first label start 18:02 -03); runs 18:02–18:17:55 -03 (`runs/run-log.txt`). One pass per artifact; author-side.
recheck: for each label, `python3 -I -B .ufo/waves/round-20/tools/compare-first-failure.py --prediction .ufo/waves/round-20/predictions/swiss-misread-v2/<label>.json --log <log_path from runs/<label>/comparison-log-binding.json> --extractor .ufo/waves/round-20/tools/first-failure-extract.py` (exit 0 = match); `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-20/runs/<label>/receipt.json`; `python3 -I -B .ufo/waves/round-20/measure.py <REV> --freeze 808cbb31a1e24656da5ba4967497e602fbca7415` field `c3`.

# Go 1.24.6 toolchain: a masked first-failure forecast matches 19/19 held-out Ghidra runs

## Question and boundary

Rounds 18-19 forecast the whole read list of Ghidra 12.1.4's Go RTTI markup walk; round 19 found that unmasked walk reads the
func-type variadic bit as 32771 parameters and that a multi-index forecast cannot match an analyzer that stops at its first
escaping IOException (`2026-10-20-r19-go125-toolchain-replay.md`). Does a forecast of only the **first** Go-analysis failure
(kind and index, or silence), with the variadic bit masked, predict held-out artifacts?

Carriers are the 20 official go1.24.6 toolchain ELFs under `/home/vgpnk/.local/opt/go-1.24.6` (`bin/*`, `pkg/tool/linux_amd64/*`;
S047: all 14175 archive members byte-identical to the install, wave-1 `SourceGo1246.md`, `ScoutGo1246Carriers.md`). They are
**artifact-held-out**: no REA analyze or Ghidra run had touched them (sha256/path sweep of the lane), although round 18 ran
`inspect-go-binary` (build metadata) on all 20. They are **not version-held-out**: Go 1.24.6 was in round 18's synthetic cohort.
They are toolchain ELFs, not applications. Byte-layout statements below are INFERENCE; a log line is an observation of the
analyzer, never of target execution. No carrier was executed: exec bits were cleared before wave 1 and checked before every
label (`evidence/carrier-guard/check-*.json`, 20/20 clean each time).

## Forecast and freeze

- `tools/swiss-misread-v2.py` = the round-18 emulator with `outCount & 0x7fff` in both func-type walk sites and a `first_failure`
  object per hypothesis (H1: Ghidra binds `internal/abi.OldMapType` for Swiss descriptors; H0: true layout). Retro check on the
  round-19 go1.25.0 bound logs: 8/8 (`evidence/retro-v2/retro-v2.csv`) — **not prediction evidence**, those outcomes were public.
- `link` excluded before freeze (v2 exit 2: first-hit build-info magic is a decoy; `predictions/decision-rule.json` `excluded`).
  19 labels frozen: D = 8 with an H1 first failure and silent H0 (addr2line, compile, go, nm, objdump, pprof, trace, vet); 11 silent.
- An all-silent baseline would score 11/19; every D forecast names an exact `Invalid index` value.

## Observations

| Label | Frozen H1 first failure | Observed first Go-analysis failure (log line) | REA analyze |
|---|---|---|---|
| t1246-addr2line | invalid_index 22078465 | invalid_index 22078465 (:112) | exit 0 |
| t1246-compile | invalid_index 36421889 | invalid_index 36421889 (:332) | exit 0 |
| t1246-go | invalid_index 35082496 | invalid_index 35082496 (:527) | exit 0 |
| t1246-nm | invalid_index 22070273 | invalid_index 22070273 (:121) | exit 0 |
| t1246-objdump | invalid_index 13816064 | invalid_index 13816064 (:122) | **exit 1** `execution_failure` |
| t1246-pprof | invalid_index 27091201 | invalid_index 27091201 (:381) | exit 0 |
| t1246-trace | invalid_index 25696001 | invalid_index 25696001 (:502) | exit 0 |
| t1246-vet | invalid_index 13791488 | invalid_index 13791488 (:187; cause `Invalid index: 13791488` :230) | exit 0 |
| asm, buildid, cgo, covdata, cover, doc, fix, gofmt, pack, preprofile, test2json (11) | silent | no Go-analysis failure up to each log's last line | exit 0 |

Per-label comparison records: `.ufo/waves/round-20/evidence/compare-rerun/<label>.json` (19 × exit 0, `match: true`); extractor
envelopes with `last_line` and separate `other_errors`: `evidence/extract/<label>.json`; all 19 receipts validate under
`--require-mid-maps` (`verify/receipt-validation/summary.txt`); every compared log's sha256 equals its binding record
(`runs/<label>/comparison-log-binding.json`, e.g. vet `657defd8485f7f97ca8ee7b560fbfef52708109489f3331439abb3eb76085b4e`).

Other errors are retained, not folded into the forecast: objdump's log records `VarnodeContext` address-space errors, then
`OutOfMemoryError: Java heap space` in X86Analyzer (:216) and an import failure (:411) **after** the Go failure at :122 — REA's
analyze returned `execution_failure`; pprof records four `VarnodeContext` errors (:490-494). No compile-style deferred RTTI NPE
recurred in these logs.

The in-run compare step was mis-wired (it passed `<label>.prediction.json`, whose `first_failure` is the H1 object itself, to a
comparator requiring `first_failure.h1`; all 19 exited 2, `runs/<label>/compare.json`). The comparison above was re-run after the
runs with the comparator and extractor bytes of the freeze commit on the frozen emulator outputs, after checking that each
emulator `first_failure.h1` equals the prediction file's `first_failure` (19/19; lesson round-20 Mistakes 6).

## Decision table and limits

| Evidence | Admissible conclusion |
|---|---|
| 8 D labels: exact predicted `Invalid index` is the first logged Go-analysis failure; 11 silent labels silent | On these go1.24.6 toolchain artifacts, the masked first-failure model of the OldMapType misread predicts Ghidra 12.1.4's first Go-analysis failure exactly (19/19) |
| objdump REA `execution_failure` | The heap OOM is a separate later failure; never call objdump a clean analyzer run |
| Silent label | No Go-analysis failure in the retained log prefix; not correct type recovery |
| Retro 8/8 on go1.25.0 | Consistency of v2 with public outcomes only |

One Ghidra release, one REA version, linux/amd64, one pass per artifact, toolchain ELFs from one Go release. Not examined:
other Go versions (1.25 artifacts only retro; 1.27 lacks a Ghidra snapshot), applications, program-database inspection,
recovery quality, the `phase`/`va` fields (emulator projections; the comparator compares kind and index only). No REA/Ghidra
repair is claimed.
