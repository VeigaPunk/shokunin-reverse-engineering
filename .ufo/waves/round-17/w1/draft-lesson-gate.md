# Draft — `## Gate` for `corpus/lessons/round-17.md`

Author-side advisory draft by `KaidokuR17.DraftLessonGate-3` (leaf seat, not a non-author reviewer). Base: `b563c79`. L1 integrates; this file is not an admission. `[SLOT: …]` = filled only from retained final evidence; a slot left open means the candidate is not admitted. Pilot runs (`.ufo/waves/round-17/pilot/`, 10:17–10:19) predate `claims.json` (declared 10:25) and are not final evidence.

## Gate

### Candidate decisions — C1 (calibration: R16-PROVENANCE, R16-INVOCATION)

| Candidate | Author-side decision | Evidence and limits |
|---|---|---|
| C1.1 Named append-only R16-PROVENANCE correction at every temporal-stability site | **admit, conditional** on `[SLOT: S1]` committed at REV | Sites at `b563c79`: `corpus/lessons/round-16.md:154`; `.ufo/waves/round-16/verification.json:419` (boolean `pins_unchanged_during_run`); `LOG.md:2012` (“remain unchanged across execution”, missed by the sweep regex, see C1.3). Route text: `corpus/lessons/round-16-verifier-spotcheck.md:183`. Correction must be appended here, not edited into the old file: `contract.md:120-122` requires pre-existing `.ufo/waves/**` blobs and `LOG` prefix to stay byte-identical. Wording fixed by the route: “map matches committed source-revision blobs; temporal stability not evidenced.” |
| C1.2 Retroactively prove the round-16 pins were stable during the run | **reject** | No pre/post record exists. `verification.json:419` is a boolean with the map only at one instant (`round-16-verifier-spotcheck.md:183`). A later measurement cannot show stability in the past; only “not evidenced” survives. |
| C1.3 Count temporal-stability sites with the sweep regex and report `N→0` | **admit the metric only with the regex extended**; current regex undercounts | `contract.md:93` regex `(unchanged during|remained unchanged during|stable throughout|pins_unchanged_during_run)` returns 2 sites at `b563c79` (`round-16.md:154`, `verification.json:419`; the spot-check file at :183 is outside the sweep file set). It misses `LOG.md:2012` (“remain unchanged across execution”). Expected `N` is therefore ≥3, not 2. `[SLOT: S2 temporal-sweep output with the regex as run; state whether it was extended]`. `SCORECARD.md` at `b563c79` has no matching r16 pins statement under the wordings searched, so the route's “scorecard says” claim is not located (see report). |
| C1.4 Rewrite the old bytes (`round-16.md:154`, `verification.json:419`, `LOG.md:2012`) | **reject** | Append-only rule (`corpus/QUALITY.md` header lines 4-5; `contract.md:120-122`). A rewrite would also falsify the controls’ own byte-identity check. |
| C1.5 SKILL.md citation-drift row (`SKILL.md:448`): re-exercise its isolated absolute argv, retain receipt | **admit, conditional** on `[SLOT: S4]` | Row argv is relative and unisolated: `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev <REV> …` (no `-I`, no `--strict`). The exercised argv (`round-16/verification.json` entry `citation-strict`, lines 317-334 at `b563c79`) is `python3 -I /home/…/citation-drift-probe.py --root /home/… --rev 27b8fc13… --table … --expected … --strict`, exit 0, `findings=0`. The row itself says `--strict` restores the gate map (`SKILL.md:448`), so the advertised default is an unexercised variant. Admit as: row edited to the exercised argv (or explicitly labelled), plus a fresh `retain.py` receipt validated by `receipt-validate.py`. |
| C1.6 Blanket-label every `(probe|gate|tool) / kaidoku` row (`SKILL.md:447-450`) as “unexercised” to drive `M→0` | **reject for row 448; admit labelling only where the audit finds no exercised match** | Labelling 448 hides the defect the route asked to repair (`round-16-verifier-spotcheck.md:184`). Rows 447/449/450 may be labelled if `[SLOT: S3 invocation-audit classes]` shows no exercised match; the labelled-unexercised class is a legitimate outcome under QUALITY #18, but it must be reported as a label, not as a repair. |
| C1.7 New QUALITY row 19 for temporal-stability wording (draft text below) | **admit, conditional** on `[SLOT: S6 QUALITY row 19 presence 0→1]` | Current rows end at 18 (`corpus/QUALITY.md:26`). Row 19 covers a gap #18 does not: #18 requires argv/revision/stdout/exit and discoverable baselines, but no pre/post timestamped same-instrument records. Does not supersede #18. |
| C1.8 QUALITY row 19 restating the invocation rule | **reject** | #18 already requires that future recheck guidance “matches the exercised isolation flags and paths or explicitly names an unexercised variant” (`corpus/QUALITY.md:26`). R16-INVOCATION was a *miss in applying #18* (row 448 survived it), not a missing criterion. A second row would add count, not discrimination. LEARNING.md:19-21 adds a criterion only “when no criterion caught it”; here one did and was not enforced, so the fix is the audit gate (C1.5/C1.6), recorded under Mistakes. |

#### Draft QUALITY row 19 (for L1; not written to `corpus/QUALITY.md` by this seat)

> 19 | A statement that a measured state (pins, producer or fixture hashes, frozen inputs) stayed unchanged *during* execution requires timestamped before-and-after records from the same instrument. A single post-run map compared with committed blobs supports only “map matches committed source-revision blobs; temporal stability not evidenced.” Matching boolean flags are not measurements. | `corpus/lessons/round-16-verifier-spotcheck.md:183`; `.ufo/waves/round-16/verification.json:419`; `corpus/lessons/round-16.md:154` | — (sharpens 18; does not supersede it) |

#### Draft correction text (for `corpus/lessons/round-17.md`; the sweep needs the repo-relative path and the token on one line)

> R16-PROVENANCE correction: `corpus/lessons/round-16.md:154` and `.ufo/waves/round-16/verification.json:419` (“pins_unchanged_during_run”) and `LOG.md:2012` (“remain unchanged across execution”) say pins/hashes were unchanged during execution. The retained evidence is one post-run map matching committed source-revision blobs; no before/after maps or timestamps were recorded. Correct wording: map matches committed source-revision blobs; temporal stability not evidenced. The old bytes are not rewritten.

#### Mistakes rows (handoff for the round lesson’s `## Mistakes`; not Gate)

| class | evidence | captured-by | fix |
|---|---|---|---|
| provenance / temporal wording | `round-16-verifier-spotcheck.md:183`; `round-16.md:154`; `verification.json:419`; `LOG.md:2012` | new QUALITY #19 (C1.7) | named correction (C1.1); pre/post pins tool with a red selftest case (`contract.md:17-20`) |
| invocation / registry variant | `round-16-verifier-spotcheck.md:184`; `SKILL.md:448` | QUALITY #18 existed but was not applied | row aligned to exercised argv (C1.5); `invocation-audit.py` counts (`contract.md:80-88`) |

### Candidate decisions — C2 (depth: Go carrier bootstrap diagnosis)

Carriers (inspect and hash read-only; no execution): `/usr/bin/shfmt` sha256 `58f765638eed5309573967726d9f9f54c8ba16cbcc65a6a5dfe0e5285aeab459`, owner `pacman -Qo`: shfmt 3.14.1-1, `rea inspect-go-binary` `go1.27.0-X:nodwarf5`, evidence `ev_f8ef12a805b6b28bee4beed4cde7440efe567e22133db2a1fb1776d867f4a42a`. esbuild 0.25.12 at `/home/vgpnk/Projects/kimi-code/node_modules/.pnpm/@esbuild+linux-x64@0.25.12/node_modules/@esbuild/linux-x64/bin/esbuild`, sha256 `bab29b2ca7a9e89b67cf720b77b2d743f9f31f5cf0d5bd74ee8c8de30ced7014`, `go1.23.12`, evidence `ev_0cabcc66620bf9f201e2b0aaba63d9bd1998b4e498ec823c01dc186a73041626`.

| Candidate | Author-side decision | Evidence and limits |
|---|---|---|
| C2.1 Pin both carriers by path + SHA-256 | **admit, conditional** on `[SLOT: S8 pins pre/post equal]` | Hashes above match `sha256sum` and the pilot `README.txt` ids. The esbuild path is inside a sibling lane’s `node_modules`; if pnpm replaces it, `carrier-run.py` must exit 2 (could-not-evaluate), never substitute a different binary. |
| C2.2 Pilot logs as prediction-vs-observation evidence | **reject** | They predate `claims.json` declared_at 10:25 (`claims.json:5`) and pilot `README.txt` records no pins. Usable as a parse rehearsal only. |
| C2.3 Predictions as pre-registration | **admit, conditional** on `[SLOT: S7 predictions.json sha256 and mtime before the first final analyze]` | Source-model predictions (INFERENCE until frozen): **shfmt** normalized `1.27.0`; out of `GoRttiMapper.java:79` range `1.15-1.25` (`GoVerRange.java:83-87`; patch-tolerant `GoVer.java:143-149`); selection `missing_base` because `typeinfo/golang/` holds `go1.15.0`–`go1.25.0` JSON only; expected `untested_version "1.27.0"`, `snapshot_label null`, `missing_bootstrap true`. **esbuild** normalized `1.23.12`; in range; selection `exact_diff` (`patchverdiffs/go1.23.12.json.diff` present); expected `untested_version null`, `snapshot_label "1.23.12"`, `missing_bootstrap false`. |
| C2.4 `missing_bootstrap` = “true iff selection status is `missing_base`” | **admit as a source-model claim with stated limit** | Path: `GoRttiMapper.java:356` (`if (apiSnapshot.isInvalid())` inside the `IOException` catch of `initStructMappings`) → `:359` message. The equivalence to `missing_base` is inferred from that branch; other causes of the same IOException are not excluded. Report it as inference. |
| C2.5 `untested_version` field | **admit** | `GoRttiMapper.java:170-171` logs `Msg.error` on out-of-range. Level is ERROR, so `log-extract` must parse `[1.27.0]` from a GoRttiMapper line; `compare.py` (`contract.md:77-78`) checks list membership only, not level. |
| C2.6 `snapshot_label` as a discriminator of the selected file | **reject as a discriminator in its current form** | `GoApiSnapshot.java:205` `read(…, GoVer ver)` and `:239` `new GoApiSnapshot(ver, results)` store the **requested** version. `GoRttiMapper.java:179-180` logs `getVer()`, i.e. the requested label. On fallback the only signal is `GoApiSnapshot.java:159-160` WARN `Falling back from %s to %s`, which `log-extract` (`contract.md:53-54`) does not extract. A fallback run would still match the predicted requested label, so the field cannot falsify fallback. Admit only with a separate `Falling back` field (L1 decides the schema change). |
| C2.7 Selector depth claim from these two carriers | **admit, limited** | Reaches 2 of 4 statuses: `missing_base` (shfmt) and `exact_diff` (esbuild 1.23.12). `base_only` and `fallback_diff` are **not** exercised; the claimed in-range `go1.20.12` carrier also has its own diff (`go1.20.12.json.diff`), so it is `exact_diff` too. No text may say the fallback branch is verified. |
| C2.8 Log-capture capability row (“retained REA Ghidra-session log”) | **reject now; conditional admit** on `[SLOT: S8 completeness check]` | Pilot copies were polled at 1 s. shfmt `ghidra.log` ends at line 125 at the `ReaGhidraBridge` post-script stage; esbuild at line 123 at the same stage (`pilot/*/ghidra.log`). All Go diagnostic lines precede `REPORT: Analysis succeeded` (shfmt line 119; esbuild line 118), so the Go fields were captured in the pilot, but post-script output is missing. A “capture runs and receipt validates” test alone would admit this. Admission must add a completeness check (the `Analysis succeeded` or failure line present) and state the post-script tail limit (`contract.md:46-47`). |
| C2.9 Knowledge entry `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` with prediction-vs-observation table | **defer** | Admit only from `compare.py` output on the final receipts (`[SLOT: S9]`); the table must not be filled from pilot logs. |
| C2.10 Claim that shfmt Go RTTI or 1.27 symbols were recovered | **reject** | Pilot shfmt shows `Untested Go version [1.27.0]` (`pilot/shfmt-log/ghidra.log:83`) and `Missing Go bootstrap type info` (`:84`), with `unable to get GoRttiMapper` (`:85`). Claims non-claim (`claims.json:28`) already excludes this. |

### Opened sources and located anchors (author-side re-open, 2026-10-20)

| ID | Location | Observation |
|---|---|---|
| S003 | `Base-src.zip`, sha256 `f00d29c2…d804` (matches `SOURCES.md:9`) | `GoRttiMapper.java:79` `SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25")`; `:170-171` untested-version `Msg.error`; `:179-180` `Using Go API snapshot for version %s` with `getVer()`; `:356-359` bootstrap branch; `GoApiSnapshot.java:118-122` `baseVer = goVer.withPatch(0)`; `:159-163` fallback WARN vs exact INFO; `:205` and `:239` requested-version storage; `GoVer.java:65` suffix strip |
| S023 | `typeinfo/golang/` listing (`SOURCES.md:29`) | JSON bases `go1.15.0`–`go1.25.0`; `patchverdiffs/` includes `go1.20.12.json.diff`, `go1.23.12.json.diff`; no `go1.26`/`go1.27` base |

### Spot-check (non-author, LEARNING.md:42-45)

`[SLOT: non-author spot-check: ≥1 admit and ≥1 reject from this Gate, re-open each source, agree/disagree with reason]`. Suggested sample for the reviewer, not a result: admit C1.1 and C2.3; reject C1.6 (row 448) and C2.6.

### Final evidence slots (fill only from retained artifacts)

| Slot | Required artifact | State |
|---|---|---|
| S1 | correction text committed at REV in `corpus/lessons/round-17.md` | open |
| S2 | `temporal-sweep.py --root … --rev <REV>` output, regex as run, N/corrected/unqualified | open |
| S3 | `invocation-audit.py --root … --rev <REV>` output, rows 447–450 classes | open |
| S4 | `retain.py` receipt for the 448 argv, `receipt-validate.py` exit 0 | open |
| S5 | `pins.py` selftest red case exit 1 on mutated pin | open |
| S6 | `measure.py` QUALITY row 19 presence 0→1 | open |
| S7 | `predictions.json` sha256 and mtime before the first final analyze | open |
| S8 | `W/runs/<label>/receipt.json` for shfmt and esbuild: evidence_id, pins pre/post equal, log sha256, polls, completeness marker | open |
| S9 | `compare.py` output per carrier; `log-extract.py` output | open |
| S10 | `controls.py` output (byte-identical pre-existing blobs, prefixes) | open |
| S11 | knowledge entry and capability row | deferred until S8–S9 |

## Integration notes for L1

- LOG.md:2012 correction must be appended by L1 (this seat may not edit LOG).
- `temporal-sweep.py` regex (`contract.md:93`) needs `remain(s|ed)? unchanged across` or equivalent before the `N` in S2 is reported as complete.
- `log-extract.py` needs a `Falling back from` field before C2.6 can be admitted.
