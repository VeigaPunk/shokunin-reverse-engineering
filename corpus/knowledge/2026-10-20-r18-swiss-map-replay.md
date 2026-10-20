source: S034 (Go 1.24 notes, `GOEXPERIMENT=noswissmap` build-time opt-out, https://go.dev/doc/go1.24 `#runtime` lines 571-573), S035 (go1.24.6/go1.25.0 `internal/abi` `SwissMapType` 112 B / `OldMapType` 88 B and `Type.Uncommon()` placement, `map_swiss.go:32`, `map_noswiss.go:25`, `map_select_swiss.go:5,22`, `type.go:358-363`), S023 (installed `go1.25.0.json`: `runtime.maptype` aliases `internal/abi.OldMapType`; the same alias is in the installed `go1.24.0.json`, which has no row of its own), S003 (installed Ghidra 12.1.4 Base-src.zip: `GoMapType.java:32-34`, `GoType.java:137-149`, `GoName.java:79-126`, `GoRttiMapper.java:1053-1075`, `MemoryByteProvider.java:302,312`; used here beyond its registered scope, see SOURCES), S033 (PR #9348, https://github.com/NationalSecurityAgency/ghidra/pull/9348, head `a214355`, tier B lead) in `corpus/SOURCES.md`; retained runs `.ufo/waves/round-18/runs/<label>/`; predictions frozen at `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` (committed 16:23:55Z, pushed 16:23:57Z) before the first run step (16:24:07Z, calib-aether `inspect-go-binary`). Caveat (w2 `FreezeBeforeRun.md`): the wave-1 census had already run REA `inspect-go-binary` (build-info only) on kimi-webbridge, aether and notesmd-cli before the freeze; no `analyze` ran on any label before it
verified-at: 2026-10-20 — one pass of 15 REA 6.5.0 `analyze` sessions (Ghidra 12.1.4), 16:24–16:32 UTC, producing revision `eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0` (each run's `producer.json` records branch tip and tool digests); author-side, not outside verification.
recheck: read-only first — `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/runs/<label>/receipt.json` (exit 0 = recorded digests and log binding consistent, each retained mid-run map re-hashed and its verdict recomputed; the receipt's own `md5_pre`/`binding.*` and the REA version in the argv are not checked); print the retained mid-run keys with `jq -c '.steps.analyze.pin_checks|map(keys)' .ufo/waves/round-18/runs/<label>/receipt.json`; `grep -nE 'Go analysis failure|Invalid index|read past EOF' .ufo/waves/round-18/runs/<label>/logs/*/ghidra.log`; re-derive the prediction with `python3 -I -B .ufo/waves/round-18/tools/swiss-misread.py --carrier <path> --golang-root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang` and compare `predicted_failure_kind_h1` / `predicted_*_reads_h1` with `.ufo/waves/round-18/predictions/swiss-misread/<label>.json` (the frozen files lack the tool's trailing newline: compare parsed JSON, not bytes); a non-destructive rerun is `RUNS_DIR=/tmp/r18-recheck bash .ufo/waves/round-18/run-carriers.sh <label>`.

# Swiss-map misread replay: Ghidra 12.1.4 on Go 1.24 (held out) and 1.25 (calibration) named map types

## Question

Round 17 left the aether symbol-markup failure as an INFERENCE: Ghidra
12.1.4 reads Go 1.24/1.25 Swiss map type descriptors with the installed
`OldMapType` layout (`corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:145-164`,
`SKILL.md` round-17 table, last row). Does that mechanism predict, before the
run, which carriers fail and with which exact read, on carriers the
prediction was not calibrated on?

## Mechanism under test (H1) and its alternative (H0)

- **Source facts.** On amd64 `SwissMapType` is 112 bytes and `OldMapType` 88
  (S035); a map's uncommon block follows its own descriptor (`type.go:358-363`).
  The installed snapshots bind `runtime.maptype` to `internal/abi.OldMapType`
  (S023, both `go1.24.0.json` and `go1.25.0.json`), and `GoMapType` has no
  Swiss class (`GoMapType.java:32-34`). Layout is a per-binary build choice
  (S034): Swiss by default from Go 1.24, old under `GOEXPERIMENT=noswissmap`.
- **H1.** For a Swiss binary, Ghidra reads a named map type's
  `UncommonType` at descriptor+88, where the true descriptor holds `SlotSize`:
  `PkgPath` (a name offset) = low 32 bits of `SlotSize`, `Mcount` = 0. The
  name at `types+SlotSize` is then decoded with its own flags; if that record
  carries a pkgPath, Ghidra follows it (`GoName.java:79-126`) with no bounds
  check on the name offset (`GoRttiMapper.java:1053-1064`). Whether this
  aborts depends on the bytes found there, not on methods: an offset past
  the end of memory throws `Invalid index: N` (`MemoryByteProvider.java:302`),
  an overlong varint length throws `Unable to read past EOF: A, B` (`:312`).
  Other aborts are possible in principle (an overlong name or tag length, a
  read into uninitialized memory, a failed module-containment check; w2
  `EmulatorSourceCheck.md`), and otherwise the misread is silent.
- **H0.** Ghidra reads the true layout; no map-path failure.
- Every named type carries an uncommon block, with or without methods
  (round-18 w1 `CriticC3.md`, `RevNotesmdMaps.md`), so the round's first
  design (named map with methods vs none, slot 24) was predicted
  non-diagnostic before any run and was extended with four `nethttp`
  carriers (their named 40-byte-slot maps are `url.Values` and
  `textproto.MIMEHeader`; `http.Header` is not in their type tables, w2
  `S1250NethttpSilent.md`), the shapes present in aether, and one real carrier.

## Method

- **Carriers** (never executed; REA imports a copy): 12 deterministic
  synthetic builds `{go1.24.6, go1.25.0} × {swiss, noswissmap} × {methods,
  nomethods, nethttp}` from `.ufo/waves/round-18/carriers/build.sh` (official
  go.dev tarballs, sha256-checked; two rebuilds of the first 8 byte-identical,
  w1 `CarrierRecipeAudit.md`; all 12 rebuilt byte-identical, w2
  `CarrierRebuild.md`), sums in `.ufo/waves/round-18/carriers/SHA256SUMS`;
  calibration `/usr/bin/aether` (go1.25.14, sha256 `06c91f55df41…`) and
  `/home/vgpnk/.local/bin/notesmd-cli` (go1.25.8, `412dc532d278…`); real
  held-out `/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge` (go1.24.13,
  `71067480bd99c2ba0f6d76df50a17e4911917cec8878320c107105066f8ad35d`), the
  only non-r17 Go 1.24/1.25 *application* ELF found (w1
  `RealCarrierCensus.md`); the go1.24.6/go1.25.0 toolchain binaries under
  `~/.local/opt` were not used (w2 `KnowledgeEntryReview.md` F1: the emulator
  predicts diagnostic failures on 7 of them — unrun candidates, not evidence).
- **Prediction.** `.ufo/waves/round-18/tools/swiss-misread.py` emulates the
  reads from carrier bytes and the installed snapshot under H1 and H0
  (calibrated only on aether's logged pair). `.ufo/waves/round-18/gen-predictions.py`
  froze, per label, the route (round-17 `predict.py`) and the H1 outcome as
  `compare.py` extra expectations (`eof_reads`, `invalid_index_reads`,
  `analyzer_errors_empty` or `analyzer_errors_contain`), plus
  `predictions/decision-rule.json`: diagnostic set D = labels whose H1 and
  H0 failure kinds differ = {calib-aether (calibration only),
  s1246-swiss-nethttp, real-kimi-webbridge}; confirmed iff every held-out D
  label shows its exact H1 read, every noswiss sibling of a D label shows no
  failure, and no non-D synthetic label fails. The H1 outcome merges the
  per-map channel with the full-markup `walk` channel where it predicts a
  failure (`swiss-misread.py:1441-1456`); no frozen value depended on the walk.
- **Runs.** `.ufo/waves/round-18/run-carriers.sh` with the round-17 capture
  tools as amended this round (mid-run maps retained as `pins/mid-<n>.json`
  with `map_sha256`); every receipt passes `receipt-validate.py
  --require-mid-maps` (15/15 exit 0; the validator re-hashes the 22 mid-run
  maps and recomputes their verdicts against the pre map; it cannot
  recompute a map). Prediction files: `predictions/<label>.prediction.json`
  (compared fields) and `predictions/swiss-misread/<label>.json` (all
  `predicted_*_h1/h0` keys); `<GOLANG_DIR>` is
  `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang`.

## Observations (bound retained logs; Evidence IDs from each receipt)

| Label | Go / layout | Route logged | H1 predicted | Observed in `ghidra.log` | compare |
|---|---|---|---|---|---|
| calib-aether | 1.25.14 Swiss | WARN `Falling back from 1.25.14 to 1.25.0` | past_eof `[17645861, 111938854]` | `Go analysis failure` (l.97); `Unable to read past EOF: 17645861, 111938854` (l.177); `ev_247261e857d89e710977e8a40f118e797c6f4b70eed5ea4d617822910b5a4af4` | 0 |
| calib-notesmd-cli | 1.25.8 Swiss | fallback to 1.25.0 | none (0 named map types) | no failure | 0 |
| **s1246-swiss-nethttp** | 1.24.6 Swiss | INFO `Using Go API snapshot for 1.24.6` | invalid_index `[22386945]` | `Go analysis failure` (l.408); `Invalid index: 22386945` (l.451); `ev_fa79d26f6dc180710d10f7666f35a40a41aa7e1df92bb882ce10903a19045dd3` | 0 |
| s1246-noswiss-nethttp | 1.24.6 old | INFO 1.24.6 | none | no failure; `ev_dd15c14c42f4038aeb7e3b0a840c391e13fe19781c889861b618a7b762b14e5f` | 0 |
| s1250-swiss-nethttp | 1.25.0 Swiss | INFO 1.25.0 | none (name at types+40 has no pkgPath) | no failure; `ev_2b8b07d50c6639ef05a33a418b442022eefe02330359d848a1e9be16b834079b` | 0 |
| s1250-noswiss-nethttp | 1.25.0 old | INFO 1.25.0 | none | no failure | 0 |
| s12{46,50}-{swiss,noswiss}-{methods,nomethods} (8) | 1.24.6/1.25.0 | INFO exact | none (nomethods: no uncommon map type at all; swiss methods: `main.Counts` slot 24 lands on a pkgPath-free name) | no failure in any of 8 | 0 ×8 |
| **real-kimi-webbridge** | 1.24.13 Swiss | WARN `Falling back from 1.24.13 to 1.24.6` | invalid_index `[15606016]` | `Go analysis failure` (l.73); `Invalid index: 15606016` (l.206); `ev_3d0da5949267d6a1c3718d258d9d6bfa30d04ac865031bfd4eb24d5c320b4096` | 0 |

15/15 compare exit 0 against bytes frozen before the run
(`.ufo/waves/round-18/runs/*/compare.json`, `run-log.txt`). Under the frozen
rule the verdict is **confirmed**: both held-out D labels failed with their
exact predicted index, the noswiss sibling of the synthetic D label did not
fail, and none of the 11 non-D synthetic labels failed. Both held-out
confirmations are Go 1.24.x; for Go 1.25.x the only failing carrier is aether,
on which the emulator was calibrated, so the 1.25 half of the mechanism rests
on calibration plus source, not on a held-out run. The aether Evidence ID
equals the round-17 second-pass ID; both runs report `string_count` 29117,
while the round-17 first pass (29118) did not (w2 `ReplicateAetherId.md`).

## Decision table

| Signal | Decision | Limit |
|---|---|---|
| Go 1.24/1.25 Swiss carrier (no `X:noswissmap` in the build version), bootstrap OK, then `Go analysis failure` with `Invalid index: N` or `Unable to read past EOF: A, B` | Check named map types first: run `swiss-misread.py`; if H1 reproduces the exact read, attribute the abort to Ghidra's `OldMapType` binding (the exact read pins the 88-byte offset, w2 `EmulatorSourceCheck.md`), not the snapshot route | 3 carriers observed (1 calibrated, 2 held out, both Go 1.24.x), one Ghidra release, x86-64 ELF; no stack frame names `GoMapType` (the bad name is also reachable through struct/interface markup) |
| Same failure on a `noswissmap` carrier | Not this mechanism | 0 of 6 noswiss carriers failed |
| Swiss carrier, no failure | Not evidence of correct map layout: on amd64 the `PkgPath` misread aborts only when the bytes at `types+SlotSize` lead to an out-of-range read; `Mcount` reads 0, so map methods are dropped silently | Silent case is INFERENCE (no log line); program-database inspection was not run |
| The same source fails under one toolchain and not another (s1246 vs s1250 nethttp: go1.24.6 vs go1.25.0) | Expected: the outcome depends on name-table bytes at a small offset (one extra 3-byte name record shifts `types+40` from flags `0x6d` to `0x62`, w2 `S1250NethttpSilent.md`), not on the Go minor as such | One pair; do not generalize "1.25.0 is safe" |

## Inference (labelled)

- INFERENCE: the bad read is reachable from more than the map path. In aether
  the retained stack runs through struct/interface markup
  (`GoStructType.additionalMarkup:94` → `GoInterfaceType.additionalMarkup:77`,
  w1 `RevGhidraMapTypeRead.md`), while the same GoName at `0x954048` is the
  misread `PkgPath` of three 40-slot maps (w1 `RevAetherReplay.md`). The
  emulator reports both channels; the frozen prediction used the map path.
- INFERENCE: PR #9348 (S033, tier B, open) adds `SwissMapType` to
  `GoMapType`'s candidates; that it fixes these carriers is not tested here.

## Not examined

- Ghidra releases other than 12.1.4, Ghidra master, and REA versions other
  than 6.5.0; Go 1.26+ (no installed base); 32-bit and non-ELF carriers.
- The silent-misread program state (lost map methods, wrong type names) — no
  REA `search`/`decompile` or program export was run.
- Determinism: one pass only.
- The emulator's full-markup `walk` channel produces false positives
  (notesmd-cli, kimi-webbridge, aether under H0: an unmasked variadic bit in
  function out-counts, w2 `EmulatorIndependence.md` F1) and its gap scan
  misses `*struct {…}` names (0 vs Ghidra's logged unindexed counts, w2
  `Runs1246noswissnethttp.md` F1); neither changed a frozen per-map value.
- REA's `analyze` JSON shows no trace of the Go symbol-analysis abort on the
  three failing carriers; only the bound `ghidra.log` does (w2
  `ProvinceAccuracy.md`).
