source: S038 (https://go.dev/dl/?mode=json&include=all, official go1.25.0 linux-amd64 archive sha256 2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613; carrier provenance only), S035 (Go internal/abi map layout), S023 (Ghidra installed Go data), S003 (Ghidra source); .ufo/waves/round-19/predictions/decision-rule.json and runs/ (observed outcome authority).
verified-at: 2026-10-20 — REA CLI explicitly pinned to rea-agents@6.5.0, Ghidra 12.1.4, eight sequential static-analysis sessions 18:57:51–19:07:07Z; producing revision a1140e76fffdc1be032d9d813dbb686157803bbc, also the pushed prediction freeze. Author-side, not outside verification.
recheck: read the retained .ufo/waves/round-19/evidence/receipt-validation/*.json (8 valid) and bound runs/*/logs/*/ghidra.log; re-hash logs against receipts. A live validation after tool edits is expected to flag receipt-validate.py's producer digest; reconstruct the a1140e7 producer bytes before replaying the validator. Never rewrite historical receipts to match a newer tool.

# Go 1.25.0 toolchain ELF replay: a held-out artifact confirms an H1-specific map-path index

## Question and boundary

Round 18 confirmed the Swiss/OldMapType mechanism on held-out Go 1.24.x artifacts; its Go 1.25 result rested on the aether calibration carrier plus source. Does a previously unrun official Go 1.25.0 toolchain executable produce a diagnostic map-path failure?

These are **toolchain ELFs**, not applications, and **artifact-held-out**, not version-held-out. Go 1.25.0 was already in round 18's synthetic cohort. The hypotheses remain byte-layout INFERENCE; a retained Ghidra log is an observation of the analyzer, not of target execution. No carrier was executed by the analysis runner. One install-record seat ran `bin/go version` outside the runner; disclosed in round-19 lesson Mistakes row 5, unused as outcome evidence.

## Inputs and freeze

- Installed root `/home/vgpnk/.local/opt/go-1.25.0`; official archive S038, 59659213 bytes. W1 `SourcesRowsDraft.md` re-downloaded it and matched all nine listed binary members to the installed bytes. Source metadata authenticates identity, not analyzer behavior.
- Exact per-carrier path/SHA-256: `.ufo/waves/round-19/predictions/carriers.tsv` (8 rows); static emulator output: `predictions/swiss-misread/*.json`. `link` excluded: no Go build info, emulator exit 2; its SHA-256 is retained in `decision-rule.json`.
- Unchanged round-18 `tools/swiss-misread.py`; producer digests in each run's `producer.json`. Predictions and rule committed and pushed as `a1140e76fffdc1be032d9d813dbb686157803bbc`, 15:57:47 -03; first run starts 15:57:51 -03 (`runs/run-log.txt`). Emulator prescan happened before freeze, not outcome observation.
- D = `{t1250-vet}` from H1 map-path failure true / H0 map-path failure false. The emulator's older `diagnostic:false` field includes a walk-only failure in its H0 kind; it cannot select D here (`w1/H0H1Semantics.md`). No emulator output was repaired after seeing logs.
- Frozen H1-only invalid indices for vet: `{13902080, 852107777}`; walk index shared by both hypotheses: `1801722468838924630`. Confirmation requires at least one H1-only index, no unpredicted index, and all seven non-D carriers silent. A shared-walk-only failure is non-discriminating, not confirmation.

## Observations (one pass)

| Label | Predicted H1 | carrier-run exit | compare exit | Retained outcome |
|---|---|---|---|---|
| t1250-go | silent | 0 | 0 | no Go analysis failure in retained log |
| t1250-gofmt | silent | 0 | 0 | same |
| t1250-asm | silent | 0 | 0 | same |
| t1250-cgo | silent | 0 | 0 | same |
| t1250-compile | silent | 0 | 0 | same |
| t1250-cover | silent | 0 | 0 | same |
| t1250-preprofile | silent | 0 | 0 | same |
| t1250-vet | invalid_index | 0 | **1** | Go analysis failure; `Invalid index: 13902080` |

Count command (from the lane): `find .ufo/waves/round-19/runs -name compare.json | wc -l` → 8. Individual exits and argv live in `runs/<label>/`; aggregate runner exit **1**, never presented as a clean full-match run. All snapshot-route fields match; vet's only compare mismatch is `extra.invalid_index_reads`: frozen full H1 list `[13902080, 852107777, 1801722468838924630]`, observed `[13902080]`.

The frozen rule's **mechanism verdict: confirmed**, because the observed index is H1-only and the seven non-D carriers are silent. The stronger **full-list prediction is falsified** (7/8 full compares match). The analyzer aborts before all candidate emulator reads are observed; that causal explanation is INFERENCE, not independently proven by the compare.

Vet's raw log `.ufo/waves/round-19/runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log`: line 186 Go analysis failure; line 229 `java.io.EOFException: Invalid index: 13902080`; line 243 `GoName.getPkgPath`. SHA-256 `a5de762231722468bcf265d5cd13ad9669f3a6d59a2746c73373e18a1a1a79c2`, 282 lines. This is an Invalid-index EOFException, not an EOF length-read pair.

## Byte-level connection (INFERENCE)

The frozen emulator's `per_type[144]` names `*types.valueMap`, descriptor address 7793536, slot size 40. H0 places uncommon data at 7793648 with pkg_path 17673 and no map-path failure; H1 places it at 7793624 (24 bytes early), reads pkg_path 40 and predicts Invalid index 13902080. The exact index now appears in the held-out analyzer log. The log does not name `*types.valueMap`; linking that descriptor identity to the stack remains byte-decode INFERENCE. This upgrades the Go 1.25 artifact-held-out half of the round-18 limit, not a claim that every Swiss map fails.

## Receipt binding and limitation of live rechecks

Eight retained receipt validations exit 0 under `--require-mid-maps` (`evidence/receipt-validation/`). They were performed after all runs using the corrected validator extracted to `/tmp`, with the producer's original receipt-validate.py bytes restored at its recorded path during validation. Applying the forward list-step fix changes that pinned producer file; validation against today's working-tree file then correctly reports a SHA-256/size mismatch. Retained validations prove consistency against the producer snapshot, not that historical pins equal future tool bytes, and not authenticity against someone rewriting and rehashing the whole chain.

## Decision table and limits

| Evidence | Admissible conclusion |
|---|---|
| vet H1-only index + seven silent controls, frozen rule | Go 1.25.0 artifact-held-out confirmation of this map-path index mechanism |
| vet compare exit 1 | Full predicted read-list did not match; never call this 8/8 exact prediction success |
| Silent carrier with a misread descriptor | No failure observed in retained prefix, not correct recovery or safety |
| Bound log + per-instant pin maps | Identical bytes at recorded instants only; no continuity claim |

One REA version, one Ghidra release, one pass, linux/amd64; no program-database inspection or recovery-quality judgment. No target behavior, no Go 1.26/1.27 generalization, no fix to REA/Ghidra. Provider logs remain outside REA's Evidence model; receipt linkage is the producer's assertion (see round-17/18 log-retention limits).
