source: S038 (https://go.dev/dl/?mode=json&include=all, official go1.25.0 linux-amd64 archive sha256 2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613; carrier provenance only), S035 (Go internal/abi map layout), S023 (Ghidra installed Go data), S003 (Ghidra source); .ufo/waves/round-19/predictions/decision-rule.json and runs/ (observed outcome authority).
verified-at: 2026-10-20 — REA CLI pinned to rea-agents@6.5.0, Ghidra 12.1.4. Pass 1: 18:57:51–19:07:07Z, producer/prediction freeze a1140e76fffdc1be032d9d813dbb686157803bbc. Preserved pass 2: 19:22:08–19:31:01Z, producer 279e8b19c51658bfd05b9e31a1c0894ab2e70537, unchanged predictions. Two observations per artifact, not independent tool/model replication or proof of determinism; author-side.
recheck: `python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-19/runs/pass2/<label>/receipt.json` from the lane, plus `python3 -I -B .ufo/waves/round-19/measure.py <REV>` field `c3.bound_validated`. First-pass live validation is intentionally red on its old producer-file pin; do not rewrite those historical receipts. Final verification retains argv, tool digests, stdout/stderr and exits.

# Go 1.25.0 toolchain ELF replay: a held-out artifact confirms an H1-specific map-path index

## Question and boundary

Round 18 confirmed the Swiss/OldMapType mechanism on held-out Go 1.24.x artifacts; its Go 1.25 result rested on the aether calibration carrier plus source. Does a previously unrun official Go 1.25.0 toolchain executable produce a diagnostic map-path failure?

These are **toolchain ELFs**, not applications, and **artifact-held-out**, not version-held-out. Go 1.25.0 was already in round 18's synthetic cohort. The hypotheses remain byte-layout INFERENCE; a retained Ghidra log is an observation of the analyzer, not of target execution. No carrier was executed by the analysis runner. One install-record seat ran `bin/go version` outside the runner; disclosed in round-19 lesson Mistakes row 5, unused as outcome evidence.

## Inputs and freeze

- Installed root `/home/vgpnk/.local/opt/go-1.25.0`; official archive S038, 59659213 bytes. W1 `SourcesRowsDraft.md` re-downloaded it and matched all nine listed binary members to the installed bytes. Source metadata authenticates identity, not analyzer behavior.
- Exact per-carrier path/SHA-256: `.ufo/waves/round-19/predictions/carriers.tsv` (8 rows); static emulator output: `predictions/swiss-misread/*.json`. `link` excluded: no Go build info, emulator exit 2; its SHA-256 is retained in `decision-rule.json`.
- Unchanged round-18 `tools/swiss-misread.py`; producer digests in each `producer.json`. Freeze `a1140e76fffdc1be032d9d813dbb686157803bbc` has committer time 15:57:44 -03; the helper had completed remote verification by the L1's 15:57:47 clock read (not the exact push instant). First run starts 15:57:51 -03 (`runs/run-log.txt`). Emulator prescan was not outcome observation.
- D = `{t1250-vet}` from H1 map-path failure true / H0 map-path failure false. The emulator's older `diagnostic:false` field includes a walk-only failure in its H0 kind; it cannot select D here (`w1/H0H1Semantics.md`). No emulator output was repaired after seeing logs.
- Frozen H1-only indices: `{13902080,852107777}`; the frozen shared walk candidate `1801722468838924630` is now known to be an emulator variadic-count bug (below), not a valid H0 Ghidra read. The frozen membership rule still discriminates by the genuine H1-only value, without repairing any prediction after seeing logs.

## First-pass observations (preserved)

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

Count distinct labels in the final preserved pass with `python3 -I -B .ufo/waves/round-19/measure.py <REV>` (`c3.compare_jsons` and `c3.bound_validated`), not a recursive `find runs` that counts both passes (16 files). Both passes have carrier-run exits 0×8 and comparator exits 0×7 / 1×1 (vet); each aggregate runner exit is **1**. All snapshot-route fields match. Vet's compare mismatch is `extra.invalid_index_reads`: frozen `[13902080,852107777,1801722468838924630]`, observed `[13902080]`.

The frozen **map-path membership rule is confirmed**: vet's observed value is H1-only and the seven non-D logs lack the specific `Go analysis failure` signature. The full-list forecast is **falsified**, and comparator 7/8 is extractor-scoped, not seven wholly clean analyzer runs. The compile log has a separate deferred RTTI NPE the extractor omits. Source reading in w2 `KnowledgeMechanism` shows that the analyzer stops at its first IOException, so a multi-index exact-list forecast was not attainable; the enormous shared walk index is independently an emulator bug, not explained by early abort.

Vet's raw log `.ufo/waves/round-19/runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log`: line 186 Go analysis failure; line 229 `java.io.EOFException: Invalid index: 13902080`; line 243 `GoName.getPkgPath`. SHA-256 `a5de762231722468bcf265d5cd13ad9669f3a6d59a2746c73373e18a1a1a79c2`, 282 lines. This is an Invalid-index EOFException, not an EOF length-read pair.

## Byte-level connection (INFERENCE)

The frozen `per_type[144]` display name is `*types.valueMap`, descriptor 7793536 (0x76eb80), slot size 40. It is the map `go/types.valueMap` with ExtraStar display naming; a distinct pointer descriptor at 0x73f4a0 shares the name data. H0 uncommon data: 7793648 / pkg_path 17673 (`go/types`); H1: 7793624 (24 bytes early) / pkg_path 40 → Invalid index 13902080. W2 `KnowledgeMechanism.md` independently decoded these bytes and showed the index is not a unique type identifier: another map assigned slot size 40 yields the same index. The log does not identify the map; connecting descriptor identity to stack remains INFERENCE, not an observed type name.

## Receipt binding and limitation of live rechecks

Eight retained receipt validations exit 0 under `--require-mid-maps` (`evidence/receipt-validation/`). They were performed after all runs using the corrected validator extracted to `/tmp`, with the producer's original receipt-validate.py bytes restored at its recorded path during validation. Applying the forward list-step fix changes that pinned producer file; validation against today's working-tree file then correctly reports a SHA-256/size mismatch. Retained validations prove consistency against the producer snapshot, not that historical pins equal future tool bytes, and not authenticity against someone rewriting and rehashing the whole chain.

Vet's REA `analyze.json` is `binary_overview` Evidence
`ev_3dc824c4fb84650b4b9c53f911a1b59688ee481262251c140080d5b42fd96f64`,
subject SHA-256 `9b9d776e7569c910de714790a1b9bab1287b49fdc210973158f3076cee683bf7`,
absolute path `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/vet`.
That Evidence binds the inventory subject; the failure above is provider-log
evidence, not a field asserted by the overview Evidence.

## Decision table and limits

| Evidence | Admissible conclusion |
|---|---|
| vet H1-only index + seven silent controls, frozen rule | Go 1.25.0 artifact-held-out confirmation of this map-path index mechanism |
| vet compare exit 1 | Full predicted read-list did not match; never call this 8/8 exact prediction success |
| Silent carrier with a misread descriptor | No failure observed in retained prefix, not correct recovery or safety |
| Bound log + per-instant pin maps | Identical bytes at recorded instants only; no continuity claim |

One REA version and Ghidra release, linux/amd64, two preserved passes on the same bytes; no program-database inspection or recovery-quality judgment. No target behavior, Go 1.26/1.27 generalization, or REA/Ghidra repair. Provider logs remain outside REA's Evidence model; the receipt linkage is the producer's assertion.

### Wave-2 scope qualifications

- Vet's candidate H1 index 13902080 was already published in round-18
  `w2/KnowledgeEntryReview.md:84-100`. “Held out” means unseen Ghidra outcome,
  not novel emulator prediction or new Go-version coverage. The frozen
  metadata's “not in prediction sets” means not in the formal r17/r18 frozen
  carrier cohorts; it must not erase that earlier candidate exposure.
- “Silent” is the **extractor's specific Go-analysis-failure predicate**,
  bounded to the retained polling prefix, not absence of every analyzer
  warning/error. The first-pass compile log has a deferred RTTI propagation
  NullPointerException (`w2/BindingCompile.md`); silent carriers also show
  subtype/missing-type warnings (`w2/OutcomeGo.md`, `OutcomeCover.md`).
  These do not become correct recovery or a clean-analysis claim.
- First-pass live binding became red after the producer validator was fixed.
  A preserved second pass under `runs/pass2/` uses the final validator bytes,
  with exactly the same frozen predictions/rule; its final validation is
  reported separately. The first pass is not overwritten or re-labelled.

### Preserved second pass and model rejection

`runs/pass2/run-log.txt`: 16:22:08–16:31:01 -03, producer `279e8b1`,
same eight labels and frozen predictions. Vet again reports 13902080; raw log
`runs/pass2/t1250-vet/logs/rea-ghidra-PEkTou/ghidra.log` SHA-256
`621e0ef90478935a1f3a81c9bc318f675d93666b5f1649276f0a42446ff4296c`.
The first pass's binding conflict was not waived: final verification uses
pass 2 with current, matching validator bytes. Neither pass overwrites the other.

The frozen full walk reads an unmasked 0x8000 variadic output-count bit as
32771 parameters, reading garbage at parameter slot 7. Ghidra masks the bit
(`GoFuncType.java:79,86`) and handles failed parameter reads
(`GoTypeManager.java:639-646`). W2 `KnowledgeMechanism.md`'s post-outcome
masked experiment explains this mismatch but is not frozen prediction evidence.
No claim that the walk correctly models Ghidra survives this finding.

Compile's deferred RTTI propagation NullPointerException recurs at line 347
of `runs/pass2/t1250-compile/logs/rea-ghidra-07WMDZ/ghidra.log`, attributed to
`AnalysisTaskWrapper`, not the `Golang*` component filter the extractor uses.
Thus “no analyzer errors” as a whole-log statement is rejected even though
the existing compare reports 7/8. This anomaly is retained, not suppressed
by expanding the predicted success class.

### Delivered validation record

The post-integration execution at `b26a6c42207a859e70bd892c7e89a5befedf379b`
is retained in `2a6229f2fb415ba8efecbc2ae24e69ec89b64986`:
`verify/receipt-validate-t1250-*.stdout` all exit0 with no findings, and
`verify/measure-source.stdout` reports `run_tree: pass2`,
`bound_validated: 8`, `compare_jsons: 8`, `matched: 7`.
The verifier re-extracts all bound raw logs and applies the unchanged frozen
membership rule separately from compare success. Its additional-error record
explicitly retains compile's wrapper-attributed NPE. These are the current
delivered binding results, not the historical first-pass zero-exit substitution.
