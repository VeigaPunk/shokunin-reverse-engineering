# CriticC2Novelty — is a real-carrier log new depth, or a restatement of the r4-10/r14 predictions?

Seat: author-side advisory critic (`KaidokuR17.CriticC2Novelty-3`). Read-only, plus this file. No REA analyze/search/decompile, no Ghidra, no carrier execution. Installs: none.
Paths are relative to `kaidoku-shokunin/` unless they are absolute. W = `.ufo/waves/round-17`.

## Verdict (short)

As written, C2 is mostly a **confirmation re-run**. The pilot already shows the outcome the claim measures. Of the three fields `compare.py` compares, two cannot disagree with the source model except through a bug in the Python port. The third (`missing_bootstrap`) was predicted by r14 and has already been observed in the pilot. Both in-range carriers are `exact_diff`, so the r16 selector law reduces to identity on them.

C2 does become new depth if it records four things already present, or obtainable, in the logs: the **co-signature** that tells the missing-base path apart from the arch-exclusion path (N1), the **uncached retry** (N2), the **fallback line on a fallback carrier** (N3), and the **content binding of log to carrier** (P1). All four are source-checkable. Three of them are absent from the current contract.

## Counterexamples — where the claim is vacuous

**V1. `snapshot_label` echoes the request on every path, so a match cannot test selection.**
- Observation: `GoApiSnapshot.java:163` logs `Using Go API snapshot for %s` with `goVer`, the requested version, not the selected `patchVer`.
- Observation: `GoRttiMapper.java:178-180` logs `apiSnapshot.getVer()`. That value is the `goVer` passed into `read` (`GoApiSnapshot.java:111`) and stored at `:239`, again the request.
- Observation: contract `W/contract.md:71-72` defines the predicted label as "the normalized requested label (not selected file)".
- So the predicted value and the observed value are both copies of the input. A match says nothing about which base or diff Java chose, which is the r16 contribution named in `W/claims.json:21`.

**V2. `untested_version` is a range test on the same parsed number.**
- Observation: `GoRttiMapper.java:170-171` is `!SUPPORTED_VERSIONS.contains(goVer)`. `predict.py` reimplements `GoVer.parse` (`GoVer.java:62-81`, regex `[^.0-9].*$` at `:65`) and the range (`:79`).
- A mismatch can only come from a porting bug in `predict.py`. It cannot reveal anything about Ghidra.
- The one non-trivial input, the `-X:nodwarf5` suffix, is already observed. Pilot `shfmt-log/ghidra.log:83` logs `[1.27.0]`, and `pilot/README.txt:7` records `go1.27.0-X:nodwarf5`.

**V3. Both in-range carriers make the selector law look like identity.**
- Observation: the installed `patchverdiffs/` contains both `go1.23.12.json.diff` and `go1.20.12.json.diff`. The highest installed diff per minor is 1.20→14, 1.23→12, 1.24→6, and there are no 1.25 diffs.
- Observation: the sibling previews `W/w1/selection-1.23.12.json` and `W/w1/selection-1.20.12.json` both return `exact_diff`, with `selected_patch` equal to the request.
- A naive model ("always use the requested patch") predicts the same output. The r16 flagship contrasts (`corpus/knowledge/2026-10-20-r16-go-selection-preview.md:9,67-70`: request 1.24.5 against installed 6, and fallback 1.24.7→6) are never exercised.
- Observation: the "0 → ≥3 runs" count in `W/claims.json:22` measures repetitions, not discriminations.

**V4. The out-of-range run reproduces the pilot and r14's own table.**
- Observation: r14 already predicts both the `Untested` line and the `Missing Go bootstrap` line (`corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md:75,77`).
- Observation: the pilot already shows both, at `shfmt-log/ghidra.log:83-85`.
- Observation: the claim's own non-claim expects the failure (`W/claims.json:28`).
- Rerunning shfmt and admitting a knowledge entry on the count alone is the pattern the lane has refused before: "a re-run dressed as a move" (`SCORECARD.md:808-809`).

**V5. A go1.27 carrier cannot cite r4-10. Doing so would be false provenance.**
- Observation: r4-10's carrier was `op` 2.40.0-2, sha `8d029d2c…`, go1.26.8 (`corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:19`). That package is no longer in `/var/cache/pacman/pkg/`; only `1password-cli-2.41.0-1` is present.
- The r14 status "cause UNKNOWN" (`r14-go-version-diagnosis.md:86-89`) must stay. A go1.27.0 log, or even a log from the go1.26.8 `op` 2.41.0 (`/usr/bin/op`, sha `f4ac474f…`), is evidence about the go1.26/1.27 code path. It is not evidence about the deleted r4-10 session's log.

**V6. REA's own evidence carries no Go diagnostic.**
- Observation: `pilot/shfmt.json` and `pilot/esb.json` have zero occurrences of `Untested`, `bootstrap`, `GoRttiMapper` or `snapshot`. The only visible signals are `procedure_count` (2581 and 8109) and `evidence_id`.
- So "REA evidence id" plus "log sha256" binds the log to a run only through timing and directory, unless P1 below is added.

## What counts as new depth (observable now or with one run)

**N1. Co-signature for missing base versus arch exclusion. This is the "discriminate" in the r14 plan (`SCORECARD.md:2230-2232`).**
- Background: r14 says the bootstrap message alone cannot tell an absent base file from a present file that has no applicable arch (`r14-go-version-diagnosis.md:51-54,77`). The sibling draft repeats that the pilot "cannot separate these two causes" (`W/w1/draft-knowledge-r17.md:117`). That statement is contradicted by source:
  - When a base resolves, `getApiSnapshotJsonFile` always calls `getPatchVerDiffFile` (`GoApiSnapshot.java:128`). That function always logs either `Falling back…` (WARN, `:159-160`) or `Using Go API snapshot for` (INFO, `:163`), including for patch 0, where the loop at `:153` is skipped and the `else` at `:162-163` runs.
  - `read` then returns a snapshot whose `ver` is valid (`:239`), so `GoRttiMapper.java:178-180` also logs `Using Go API snapshot for version`. An arch-excluded snapshot (`isInvalid()`, `:503-505`) therefore produces **≥2 snapshot lines before** the bootstrap WARN.
  - When the base is missing, `:124-125` returns null before `:128`. `EMPTY` carries `GoVer.INVALID` (`:242`), so `:178` suppresses the line. The result is **0 snapshot lines**.
- Observation from the pilot: `shfmt-log/ghidra.log:82-85` goes from `Reading Go binary info` straight to `Untested` and then `Missing Go bootstrap`, with no `GoApiSnapshot` line. That is the missing-base signature.
- Positive control: `esbuild-0.25.12-log/ghidra.log:63-64` shows both snapshot lines at INFO. This proves the log level records them.
- Scope: this upgrades r14's "INFERENCE FROM SOURCE … not observed execution" (`:45-50`) to an **observed sequence on one executing provider**.
- Limits:
  - It distinguishes "Java resolved no base" from "base resolved but arches empty". It does not distinguish "file absent" from "`getModuleDataFile` IOException" (`:175-176`).
  - It does not test downstream layout. Bootstrap aborts first, so layout stays "neither proved absent nor identified", as r14 states at `:89-90`.

**N2. A failed bootstrap is not cached; every Go analyzer retries it. No r14 or r16 text predicts this.**
- Observation: `TransientProgramProperties.java:107-110` (`ghidra/app/plugin/core/analysis/`) returns null without calling `addProperty` when the supplier returns null.
- Observation: `GolangStringAnalyzer.java:103-105` calls `getSharedGoBinary` again.
- Pilot: `shfmt-log/ghidra.log:82-85` (Symbol analyzer) and `:86-89` (String analyzer, 10 s later) show two full `Reading Go binary info` → `Untested` → `Missing bootstrap` cycles.
- This corrects the "ANALYSIS HALTED" framing (`.ufo/waves/round-14/w1/InstalledGoGate.md:88`) and resolves the sibling draft's UNKNOWN (`W/w1/draft-knowledge-r17.md:118`).
- Predicted count: one bootstrap attempt per Go analyzer that calls `getSharedGoBinary` while the result is null. `log-extract` should report this count, and a "1 failure" prediction would fail against it.

**N3. Fallback-branch carriers exercise the r16 law where it is not identity.**
- Host census: a stdlib read of the `\xff Go buildinf:` header over `/usr/bin`, `~/.local/bin` and `/usr/lib/docker/cli-plugins`. These are observations, not REA output.
- `/usr/bin/aether`: aether 4.32.0-2, sha `06c91f55df4117e5…`, `go1.25.14`.
  - It is in range, so no `Untested` line is expected.
  - The base `go1.25.0.json` exists and there are no 1.25 diffs. Source predicts `Falling back from 1.25.14 to 1.25.0 for Go API snapshot` (WARN, `GoApiSnapshot.java:159-160`), then `Using Go API snapshot for version 1.25.14` (`GoRttiMapper.java:180`).
  - This makes the r16 claim that the Java label is the request and not the selected bytes (`r16-go-selection-preview.md:24`) **directly falsifiable in one log**: the two lines name different versions.
  - Bootstrap success on a base-only snapshot for patch 14 is a genuinely open outcome. No source model fixes it.
- `~/.local/bin/notesmd-cli` (`go1.25.8`) is not owned by any package (`pacman -Qo`), so its provenance is weaker.
- No go1.24.≥7 carrier was found.
- `/usr/bin/op` 1password-cli 2.41.0-1 (go1.26.8) is the closest same-version, same-product carrier to r4-10. It has a missing base with patch > 0, which tests that there is no cross-minor rescue. Cost is about 6 min, based on r4-10's `:28-29` timings. Per V5 it must not be cited as r4-10.

**N4. In-range post-bootstrap quantities that no source model predicts.**
- Observation: `esbuild-0.25.12-log/ghidra.log:65-66,72-73,80-85` reports 4881 types, 188 unindexed, 2248/2055 fixed signatures, 9908/9798/2 fixups, and `Go missing type names: 19`. The last is emitted at mapper `close()` (`GoRttiMapper.java:371-373`).
- These are depth only if tied to a question. For example: do missing type names appear with an *exact* diff, and how does the count compare with a base-only fallback carrier (N3)?
- Any cross-carrier comparison is confounded by program differences. Label it INFERENCE.

## Provenance and identity defect

**P1. The log-to-carrier binding is temporal only.**
- Contract `W/contract.md:36-38` attributes logs to a run by "NEW `/tmp/rea-ghidra-*` dirs" that appear during the Popen. Concurrent REA sessions on this host would be misattributed.
- The log carries content identity:
  - `IMPORTING: file:///tmp/rea-ghidra-…/target-<sha256[:12]>.bin` (`shfmt-log/ghidra.log:46`, `target-58f765638eed`, which matches the carrier sha `58f76563…`).
  - `…?MD5=<md5>` (`:64`, `caacf2c8df03f63b98119ef107020070`; `md5sum /usr/bin/shfmt` gives the same value).
- Without this check, "retained log sha256 + REA evidence id" can pair a carrier with another session's log.

## Smallest safe corrections (advisory to L1)

1. `log-extract.py`: add `fallback: [{from,to}]` from `Falling back from X to Y for Go API snapshot`, plus `bootstrap_attempts` (the count of `Reading Go binary info`), `snapshot_line_count_before_bootstrap`, and `import_target_sha12` / `import_md5`.
2. `compare.py`: add `selected_patch` (r16 `selected_patch` against observed `fallback.to` patch, or the request if no fallback line) and `invalid_snapshot_path ∈ {missing_base, arch_excluded}` (N1 rule). Mark `snapshot_label` and `untested_version` as `non_discriminating: true` in output so a green table is not read as testing selection.
3. `receipt-validate.py`: fail if `import_target_sha12 != carrier.sha256[:12]` or `import_md5 != md5(carrier)`.
4. Carrier set: keep shfmt (N1, N2). Add **`/usr/bin/aether` go1.25.14** as the fallback-branch carrier (N3). Use at most one exact-diff esbuild run (N4 positive control, not three). Use `/usr/bin/op` go1.26.8 only with the V5 disclaimer.
5. Knowledge entry:
   - State N1/N2 as new observations with source anchors.
   - Strike "pilot cannot separate" (`draft-knowledge-r17.md:117`) in favour of the N1 rule with its limits.
   - Resolve `:118` through `TransientProgramProperties.java:107-110`.
   - Keep r4-10's cause UNKNOWN.
   - Do not count runs as the depth unit.

## Axes impacted

- **Depth:** the claim improves only through N1–N3. Without them, at best the run count changes.
- **Calibration:** at risk from V1, V2 (non-discriminating matches presented as confirmations), V5 (false provenance to r4-10) and P1 (log misattribution).

## Searched

- `W/claims.json`, `W/contract.md`, all `W/pilot/*` (`sha256sum -c SHA256SUMS`: all OK), `W/w1/selection-*.json`, `W/w1/draft-knowledge-r17.md`.
- Committed r4-10, r14, and r16 Go entries; `SCORECARD.md` (808-809, 2222-2234, 2345-2348); `corpus/lessons/round-15.md:10`; lane grep for `Untested Go version|Missing Go bootstrap`.
- `Base-src.zip` members `GoApiSnapshot.java` (95-250, 495-510), `GoRttiMapper.java` (95-200, 325-380), `GoVer.java` (20-140), `TransientProgramProperties.java`, `GolangStringAnalyzer.java`.
- Installed `typeinfo/golang` and `patchverdiffs` listing; host Go-carrier buildinfo census (read-only byte scan); `pacman -Qo` and `ls /var/cache/pacman/pkg`, both read-only.
- Not done: no REA analyze or search, no Ghidra run, no `inspect-go-binary` on the new candidates (the census versions come from my stdlib buildinfo read and are not REA output).
