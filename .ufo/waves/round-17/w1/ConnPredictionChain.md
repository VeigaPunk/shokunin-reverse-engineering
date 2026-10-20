# Connector — one prediction→observation chain for the Go bootstrap diagnostic

Axes: **calibration**, **depth**. Read-only; this file is the only write. No REA
`analyze`/`search`/`decompile`, no Ghidra, no carrier execution. `rea inspect-go-binary`
(contract-permitted) was re-run on both pilot carriers to materialize the prediction input
that the pilot itself did not retain.

Evidence classes used below: **OBSERVED** = tool/file output; **SOURCE** = control-flow read
from the installed `Base-src.zip` (S003); **MODEL** = a Python/source-model computation, not
Java execution; **INFERRED** = reasoned from SOURCE + OBSERVED.

## 1. The chain, link by link

| # | Link | Prediction anchor (model) | Observation anchor | Status |
|---|---|---|---|---|
| L0 | Carrier + version input | `inspect-go-binary` `build_info.go_version` (`claims.json:21`) | shfmt `go1.27.0-X:nodwarf5`, esbuild `go1.23.12`; my runs, evidence `ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a` / `ev_0cabcc66620bf9f201e2b0aaba63d9bd1998b4e498ec823c01dc186a73041626`; hashes match `pilot/README.txt:7-8` | OBSERVED, independent route |
| L1 | Version normalization | `GoBuildInfo.java:488-489` strips `go`, `:237-239` → `GoVer.parse`; `GoVer.java:62-80` regex truncation, `:155-160` `M.m.p` | shfmt `shfmt-log/ghidra.log:83` `[1.27.0]`; esbuild `esbuild-0.25.12-log/ghidra.log:67` `1.23.12` | OBSERVED echo; the strip itself is SOURCE |
| L2 | Declared-range membership | `GoRttiMapper.java:79` `1.15-1.25`, `GoVerRange.java:83-86` inclusive; out-of-range is `Msg.error` only, no return (`GoRttiMapper.java:170-172`) | shfmt log:83 ERROR `Untested Go version`; esbuild log has no such line | OBSERVED match |
| L3a | Snapshot base/diff **status class** | r16 `selection.py` law: `missing_base` / `exact_diff` (`2026-10-20-r16-go-selection-preview.md:19,21,40`) | shfmt: **no** `GoApiSnapshot` line at all; esbuild log:63 INFO `Using Go API snapshot for 1.23.12`, no `Falling back` | OBSERVED at class level (see §2) |
| L3b | Selected file **bytes/digest** | r16 `base.path/sha256`, `diff.sha256`, `patch_applied:false` | no log line reports filename or digest | **MODEL only** (§3) |
| L4 | Bootstrap outcome | `GoApiSnapshot.java:122-126` null base → `:115` EMPTY → `:503-505` invalid → `GoRttiMapper.java:353,356-360` `BootstrapInfoException` → caught `:114-116` as WARN | shfmt log:84 exact WARN string | OBSERVED that the **invalid-snapshot branch was reached** (message text is branch-unique; the other branch at `:364-365` prints different text) |
| L5 | Analyzer consequence | `GolangSymbolAnalyzer.java:133-137` returns false; null result is not cached (`TransientProgramProperties.java:109-111`), so each Go analyzer re-runs the bootstrap | shfmt log:85 symbol error, log:89 string error, groups at 10:17:30 and 10:17:40; times `0.007`/`0.002` s (log:106-107) | OBSERVED, including the duplicate group |
| L6 | Post-bootstrap success path | **no prediction in r14/r15/r16** | esbuild log:65-85 (`Found 4881 Go types`, `Go missing type names: 19`, three subtype WARNs 68-70), times `15.728`/`3.158` s (log:103-104) | OBSERVED, **unpredicted** |

Reconstructed field values (MODEL; `predict.py` does not exist yet — `.ufo/waves/round-17/tools/` absent):

| Carrier | normalized | in range | r16 status | predicted untested/label/bootstrap | observed |
|---|---|---|---|---|---|
| shfmt | 1.27.0 | no | `missing_base` | `1.27.0` / null / true | `1.27.0` (log:83) / no snapshot line / true (log:84) |
| esbuild | 1.23.12 | yes | `exact_diff` (patch 12) | null / `1.23.12` / false | absent / `1.23.12` (log:63-64) / false |

`exact_diff` for esbuild is derived from installed files (`go1.23.0.json` base +
`go1.23.12.json.diff` present) under the r16 law; the log corroborates the branch, not the bytes.

## 2. New: the `GoApiSnapshot` line is an observation channel for r16's status

SOURCE, from `GoApiSnapshot.java:118-166`: `getPatchVerDiffFile` is called **only after**
`getApiSnapshotFile` returns a base (`:122-126`). It then logs unconditionally — INFO when
the selected patch equals the requested patch (`:162-164`), WARN `Falling back from %s to %s`
when lower (`:158-160`). The mapper's second line (`GoRttiMapper.java:178-181`) prints
`apiSnapshot.getVer()`, which is the **requested** version (`GoApiSnapshot.java:111,239`), so
it cannot distinguish fallback.

Therefore, with a present base:

| r16 status | predicted `(GoApiSnapshot)` line | predicted `(GoRttiMapper)` line |
|---|---|---|
| `missing_base` | none | none |
| `exact_diff` | INFO `Using Go API snapshot for <req>` | INFO `... version <req>` |
| `fallback_diff` | WARN `Falling back from <req> to <sel>` | INFO `... version <req>` |
| `base_only`, req patch 0 | INFO | INFO |
| `base_only`, req patch >0 | WARN `... to <minor>.0` | INFO |

This resolves r14's open discriminator (`2026-10-20-r14-go-version-diagnosis.md:77`, “distinguish
absent base file from OS/architecture exclusion”): a present-but-inapplicable base **must** emit
a `GoApiSnapshot` line before `read()` filters arches. shfmt emits none. Combined with the
absence of `Failed to read Go info` and `Error fetching Go API snapshot file`, and with
`getApiSnapshotFile`'s only failure mode on this path being a null return
(`GoApiSnapshot.java:168-177`), the shfmt run is an observation that the base **could not be
located**, not an arch-exclusion case. Residual: `Application.getModuleDataFile` resolution was
not traced; the pinned directory listing (11 bases, `go1.15.0`–`go1.25.0`) is the other half of
the inference.

The polling caveat (`pilot/README.txt:6`) does **not** explain the missing shfmt line: lines at
10:17:30 both before and after the expected position were copied, and the missing line would
have been written in that same second.

## 3. The link still only source-model

**L3b — selected snapshot identity.** No log line reports the selected filename, patch-diff
identity, or digest; the only version-shaped line prints the requested version (r15:21). So
r16's `base`/`diff` objects with their SHA-256 values remain a model, not an observation. The
pilot can corroborate *which branch* was taken (§2), never *which bytes* were read.

Secondary, narrower residuals:
- **Why** the snapshot was invalid (base absent vs module-data resolution) — INFERRED, not traced.
- **Post-hoc status of the comparison**: the pilot ran before any prediction tool existed
  (no `W17/tools/`, no prediction artifact for these carriers). These matches are a post-hoc
  model fit, not prospective prediction (§4, C3).

## 4. Calibration findings that change the round's plan

**C1 — `predict.py` will exit 2 on the flagship carrier if written to the contract literally.**
The contract says normalize as `GoVer.parse`. `GoVer.java:64-66` applies
`replaceAll("[^.0-9].*$","")`, which deletes a leading `go` and the whole string, yielding
INVALID. The prefix is stripped earlier at `GoBuildInfo.java:488-489`. Computed MODEL check:
raw `go1.27.0-X:nodwarf5` → `INVALID`; after the strip → `1.27.0`; `go1.23.12` → `INVALID`;
after strip → `1.23.12`. The tool must implement both steps, with the log echo (shfmt log:83) as
its acceptance check. Without this, shfmt produces no prediction at all. Separately, the
contract's reference to `GoVer.parse/fromVersionString` names a member that does not exist in
the installed `GoVer.java` (public normalizers there are `parse`, `parseWildcardPatch`,
`fromProgramProperties`); the prefix strip lives in `GoBuildInfo`, not in `GoVer`.

**C2 — range and base availability are perfectly confounded in this installation.**
Enumerating the installed directory: base minors = `{1.15…1.25}`, exactly
`SUPPORTED_VERSIONS = 1.15-1.25` (`GoRttiMapper.java:79`); for every minor 1–30,
`in_range == base_present` (no mismatch). So no carrier on this host can separate “out of range”
from “base absent”: the shfmt run cannot be evidence for the causal ordering in r14's rows 2–3,
only for the conjunction the source predicts. Presenting it as causal confirmation would
over-claim; the source read (`:170-172` has no return) remains the only separator.

**C3 — the pilot cannot supply a prospective prediction.**
All field matches in §1 are post-hoc. The round's falsifiable claim (`claims.json:21`) is only
satisfied as *prediction* if `predict.py` output is frozen (written before the analyze step) for
at least one **new** carrier. The pilot carriers may be reported, labelled post-hoc, as
reconstruction checks.

**C4 — the three contract fields are not equally evidential.**
`untested_version` is near-tautological: the log prints the same build-info version that the
prediction parsed (both derive from the same bytes). `snapshot_label` and `missing_bootstrap`
carry the selection law. A 3/3 table should not read as three independent confirmations; the
report should state that one field tests normalization and two test the selection outcome.

**C5 — the planned carrier trio repeats a status class.**
`claims.json:21` plans 1.27.x, 1.23.12, 1.20.12. Installed data: `go1.20.12.json.diff` exists,
so 1.20.12 is also `exact_diff`; 1.23.12 is `exact_diff`. Two of three carriers exercise the same
branch (`base_only` and `fallback_diff` unexercised). A carrier choice that adds a branch,
derived only from the installed listing:
- `base_only` + WARN-to-`.0`: any Go 1.25.x build with patch > 0 (no diffs in the 1.25 minor);
- `fallback_diff` + WARN-to-k: patch above the installed max for the minor — 1.20.15+ (max 14),
  1.22.13+ (max 12), 1.23.13+ (max 12), 1.24.7+ (max 6).
This is a selection criterion for L1/Scout, not a new run.

## 5. Second-order effects on the round's tools and entry

- `log-extract.py`: add a field for the `GoApiSnapshot` line class (`info`/`fallback`/`none`) and
  the fallback `from`/`to`. Today `snapshot_labels` merges both patterns and cannot express the
  branch, so the §2 channel is invisible to `compare.py`.
- `predict.py`: emit the predicted line class alongside the three fields; keep the contract's
  three required fields unchanged so `compare.py`'s exit semantics stay intact.
- `compare.py`: if the fourth field is added, weight/report the selection-dependent fields
  separately; a mismatch on `snapshot_label`/line class is the informative one.
- Knowledge entry: record (i) the base/range confound (C2), (ii) branch-reached vs cause,
  (iii) the unpredicted esbuild type-resolution band (L6: 19 missing type names, three subtype
  warnings), (iv) post-hoc vs prospective labelling for each carrier row.
- Provenance: the pilot has no pre/post pins (`README.txt:6`); the final runs' `pins.py`/
  `retain.py` receipts are what make these logs admissible, and the analyze JSONs already carry
  `binary_overview` evidence ids (`shfmt.json` `ev_2b29…`, `esb.json` `ev_391d…`) that the
  pilot's provenance didn't use.

Cross-seat overlap, checked at write time (so L1 does not double-count): `RevGoVerNormalize.md`
independently derives the `go`-prefix strip (corroborates C1; the additive parts here are the
`predict.py` exit-2 consequence and the absent `fromVersionString` member);
`ScoutGoApiSnapshotLog.md` and `ConnRequestedLabel.md` independently establish that the logged
label is the requested version (corroborates L3b; additive here is the line-class→r16-status
mapping and the "a present base always logs before arch filtering" discriminator).

## 6. Risks

- Adding a comparison field mid-round could disturb the sole-integrator contract; mitigate by
  keeping it outside the three-field gate (table-only) unless L1 adopts it explicitly.
- The §2 channel depends on log level; a future REA/Ghidra config that filters INFO would erase
  the `missing_base` signal. Pin the log config (`Using log config file` line, shfmt log:1).
- A 1.25.x / 1.24.7+ carrier may not exist on the host; choosing carriers is Scout/L1 work, and
  a missing candidate must not be replaced by a second `exact_diff` carrier and reported as
  branch coverage.

## 7. Verification performed

- `sha256sum` on both carriers → match `pilot/README.txt:7-8`.
- `npx -y rea-agents@6.5.0 inspect-go-binary <carrier> --format json` for both (contract-allowed;
  no Ghidra, no analyze) → evidence ids above; `confidence: observed`, `authority:
  shipped-artifact`. Not retained in the lane; no install was performed and none is needed
  (npx cache at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6`).
- Python enumeration of `typeinfo/golang/` bases and `patchverdiffs/` maxima (C2/C5), and a
  Python reproduction of the `GoVer` regex (C1). These are my computations, not tool runs.
- Read-only extraction/grep of `Base-src.zip` members (`GoVer`, `GoVerRange`, `GoBuildInfo`,
  `GoRttiMapper`, `GoApiSnapshot`, `GoTypeManager`, `GolangSymbolAnalyzer`,
  `TransientProgramProperties`).
- Grep of both pilot `ghidra.log` files for the branch strings in §2.
