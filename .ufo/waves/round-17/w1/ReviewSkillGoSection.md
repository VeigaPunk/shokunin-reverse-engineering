# ReviewSkillGoSection — R17 SKILL.md Go sections: placement and qualification

Seat: `KaidokuR17.ReviewSkillGoSection-3` (leaf, author-side advisory). Date: 2026-10-20.
Scope: `SKILL.md:455-507` (r14/r15/r16 Go tables and registry rows) plus the text those rows
compress. Read-only. No REA `analyze`/`search`/`decompile`, no Ghidra, no headless, no carrier
execution, no installs. All observations below are from retained files or from the installed
Base source archive, read with `unzip -p` (no extraction).

Method: `SKILL.md` headings and rows (`grep -n`); pilot logs and hashes
(`.ufo/waves/round-17/pilot/`); installed data listing
(`.../Base/data/typeinfo/golang/`, 11 base JSONs go1.15.0–go1.25.0 + 123 patch diffs); S003 members
`rtti/GoRttiMapper.java`, `rtti/GoApiSnapshot.java`, `GoVer.java`, `GoBuildInfo.java`,
`analysis/GolangSymbolAnalyzer.java`, `analysis/GolangStringAnalyzer.java`; measured-lane drafts in
`w1/`. Labels: **O** = observed in a retained artifact, **I** = inference from source, **U** = unknown.

## 1. Where the section and rows go

**Append after `SKILL.md:507` (EOF).** The file's Go material is strictly round-ordered
(`:454` r14, `:472` r15, `:489` r16) and ends at the r16 registry row `:507`. Insertion inside any
existing block would break that order and rewrite rows whose argv/limits are round-scoped.

Do **not** add r17 rows to the top registry (`:438-450`): its prose at `:440-443` enumerates exactly
the r1-r14 four instruments, and `:452` closes the section. Adding rows there requires editing that
enumeration sentence, mixing round scopes, and makes the `controls.py`-style append check harder to
reason about. Do **not** append rows to the r15 (`:485-487`) or r16 (`:504-507`) tables for the same
reason; the new section should *refer* to them, not edit them.

Proposed shape at EOF (mirrors the existing three blocks):

1. Heading: `## Retained Go carrier diagnostics — round 17`.
2. 3-4 line preface: cite the admitted knowledge entry
   `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md` (the exact path `measure.py` keys on,
   `contract.md:117`), the REA pin `npx -y rea-agents@6.5.0` **CLI** (the OMP rea MCP entry is
   disabled by operator authorization), and S003's installed Ghidra 12.1.4 archive. Say the log is
   Ghidra-version-bound, not REA-version-bound.
3. `| Signal | Decision | Limit |` table (schema at `:461`, `:479`, `:497`).
4. `| Name | Kind / owner | Entry / status map | Self-invocation | Pinned values / write scope |`
   table (schema at `:445`, `:485`; r16 used "Fixture check" at `:504` — use
   "Self-invocation" only where a real `--selftest` exists).
5. Closing boundary paragraph in the register of `:468-470` and `:452`.

Registry rows belong to the **C2 toolchain only**: `carrier-run`, `log-extract`, `predict`,
`compare`, `receipt-validate`. The C1 instruments (`pins.py`, `retain.py`, `invocation-audit.py`,
`temporal-sweep.py`) are a different axis and do not belong in the Go section; if SKILL rows are
wanted for them, they need their own calibration section. `contract.md:118` says only "SKILL
registry rows for new tools" without naming them — pin the expected row names inside `measure.py`
too, or that check is self-referential and can pass on any row set.

Row text constraints, from C1b (`claims.json:12`): each entry cell's command must be an exercised
retained argv or carry the literal word `unexercised`. Do not copy r15's exit gloss "0 emitted,
nonzero could-not-evaluate" (`:487`): `carrier-run` exits **1 on pin drift** and `compare` exits
**1 on mismatch** (`contract.md:48-49`, `:75-78`). Do not present `carrier-run --search` as
exercised (the pilot never ran it), and do not advertise a `--selftest` that drives REA — the
contract's blanket selftest clause (`contract.md:7-9`) cannot be satisfied that way; state
"fixture-only, never REA" or "no selftest".

Suggested decision rows (each is supported below):

| Signal | Decision | Limit |
|---|---|---|
| `Untested Go version` + `Missing Go bootstrap type info` + **no** mapper snapshot label | Missing base JSON (`U`/`I`: `GoApiSnapshot.java:115,242`; label gate `GoRttiMapper.java:177-181`) | Session still exits 0; not Go recovery |
| `Using Go API snapshot for version X` (GoRttiMapper) | A base JSON existed; X is the **requested** version | Never the selected file; no bucket/byte identity |
| `Using Go API snapshot for X` (GoApiSnapshot, INFO) | Exact requested patch diff present (or patch 0) | Applied content unverified |
| `Falling back from X to Y` (GoApiSnapshot, WARN) | Requested patch diff absent; selected patch Y | Filename/digest must come from inventory, not the log |
| In-range base + diff | Names present but partial (4881 types, 19 missing on one carrier) | Not a recovery guarantee |

## 2. Existing text the observations qualify or contradict

Net result: **no existing row is contradicted outright.** `SKILL.md:463` is confirmed with a scope
fix (F4); `:464`, `:465`, `:466`, `:481` and the r14 paragraph `:468-470` are qualified (F3, F5, F6,
F8, F7); `:477` is confirmed but its caution is insufficient for the label fields (F1). `:483` and
`:500` receive no new claim. Details, with anchors and evidence class:

### F1 (high, calibration) — `SKILL.md:477`/`:481`: a label match cannot verify the selection branch; `compare.py` as specified can false-pass

- **O** esbuild: `GoApiSnapshot` INFO `pilot/esbuild-0.25.12-log/ghidra.log:63`, mapper INFO
  `:64`, `Go version` `:67`; shfmt: no snapshot label anywhere in `:82-89`.
- **I** (source): `GoApiSnapshot.getPatchVerDiffFile` logs INFO when the requested patch is the
  selected one (exact diff, or patch 0 where no diff search runs), and WARN `Falling back from X to Y`
  otherwise (`GoApiSnapshot.java:148-166`). But `read`
  stores the **requested** version (`:239`), so the mapper's `Using Go API snapshot for version X`
  (`GoRttiMapper.java:177-181`) prints the requested label for exact-diff, fallback, **and**
  base-only runs alike.
- Consequence: `compare.py` compares only `untested_version`, `snapshot_label`,
  `missing_bootstrap` (`contract.md:75-78`). For a requested patch with no exact diff, all three can
  match while the run silently contradicted a predicted `exact_diff` — the contradictory observable
  is the GoApiSnapshot branch line (INFO absent, WARN present), which no compared field currently
  carries. Concrete fallback carriers on this
  install: `go1.24.7` (diffs stop at `go1.24.6.json.diff`) and **any** `1.25.x` (123 diff files,
  **zero** for 1.25). None of the planned carriers exercises it: `go1.23.12` and `go1.20.12` both
  have exact diffs (`patchverdiffs/` listing), so the final runs inherit the blind spot.
- Required before the section lands: `predict.py` must predict the branch (INFO label vs WARN
  requested→selected patch vs none), `log-extract` must keep the two `Using Go API snapshot`
  spellings separate and add `snapshot_fallback`, and `compare.py` must include it. If L1 will not
  amend the contract, the SKILL table must at minimum state that a label match is **not**
  selection-branch verification and that fallback is unexercised.

### F2 (high, provenance) — the pilot JSONs are not `inspect-go-binary` and carry no Go version

- **O** `pilot/shfmt.json` and `pilot/esb.json`: `operation: binary_overview`; `normalized_result`
  keys are `document/image_base/segments/segment_count/procedure_count/string_count`; occurrences
  of `go_version`, `build_info`, `go1.`, `1.23`, `1.27` = **0**. Their evidence ids
  (`ev_2b29…`, `ev_391d…`) are `binary_overview` ids.
- **O** `pilot/README.txt:7-8` asserts the versions; `:3` abbreviates the esbuild path.
- **O** the draft entry's inspect id `ev_f8ef…` (`w1/draft-knowledge-r17.md:17`) traces to
  `w1/ScoutGoReleaseHistory.md:18` — a scout's live inspect run, not a pilot artifact.
- The new section must cite the **final** receipt's `inspect-go.json` and analyze `evidence_id`
  (`contract.md:31-49`), not the pilot JSONs, for carrier identity. The pilot supports only the two
  log observations, the exit codes, and the README/SHA256SUMS pins.

### F3 (medium, calibration) — `SKILL.md:464`: the bootstrap message cannot separate the two causes; the label gate can

- **I** `GoApiSnapshot.isInvalid()` returns `arches.isEmpty()` (`:503-505`); `GoRttiMapper:355-365`
  selects `Missing Go bootstrap type info` for **any** invalid snapshot. So the shfmt WARN
  (`shfmt-log/ghidra.log:84`) is not by itself proof of missing base, and the r14
  zero-applicable-bucket hypothetical stays unestablished.
- **I** the log-side discriminator is the mapper's valid-version gate: a present base yields
  `new GoApiSnapshot(requestedVer, results)` (`:239`, valid even with zero buckets) and therefore
  the `Using Go API snapshot for version X` line; a missing base returns EMPTY/INVALID
  (`:115`,`:242`) and logs no line. shfmt has no label ⇒ missing base, corroborated by the installed
  listing (bases end at `go1.25.0.json`; no 1.26/1.27 base).
- Add the row from §1; keep the 1.27 carrier from being read as evidence for the hypothetical.

### F4 (medium, calibration) — `SKILL.md:463` is confirmed but must be scoped to the session

- **O** shfmt: `:83` ERROR Untested, `:84` WARN Missing, `:85` symbol-analyzer error, `:87-89` the
  same route for the string analyzer, `:119` `Analysis succeeded`, exit 0 (`pilot/shfmt.exit`).
  Go auto-analysis costs ~0.002/0.007 s (`:106-107`).
- So "logs and continues; it does not refuse analysis" is true of the **Ghidra session**, not of Go
  analysis: both Go analyzers return false. Exit 0 + `Analysis succeeded` is not recovery.
- The duplicate lines are **per-analyzer retries**, not repeated runs: `GolangSymbolAnalyzer:133-137`
  and `GolangStringAnalyzer:103-105` each call `getSharedGoBinary`, and the failed instance is not
  reused (`Reading Go binary info` appears twice, `:82`,`:86`). `log-extract` must use set
  semantics; `analyzer_errors` on shfmt are exactly the two `unable to get GoRttiMapper` messages,
  not the expected `Untested` line (note `Golang*` vs `Go*` filter ambiguity, `contract.md:55-56`).

### F5 (medium, calibration) — `SKILL.md:465`: the 1.27 failure cannot discriminate GP-6528

- **I/O** S004 is a bundle — range plus snapshot JSON, moduledata/pcHeader/map handling
  (`corpus/lessons/round-14-verifier-spotcheck.md:104`). The install has **no** 1.26/1.27 base JSON
  at all, so a range-only host patch would still fail. The observed shfmt failure is fully explained
  by absent base data and is not evidence for or against the upstream support change. Say this or the
  1.27 carrier reads as an upstream-support result.

### F6 (medium, calibration) — `SKILL.md:466`: "names absent" is conditional, and in-range recovery is partial

- **O** esbuild: `Found 4881 Go types` `:66`; `Fixed 2248 … runtime snapshot` `:72`;
  `Fixed 2055 … method info` `:73`; `Go strings found: 6264` `:83`; `Go missing type names: 19`
  `:85`; three `Failed to get subtype` WARNs `:68-70`.
- An in-range carrier with base+diff yields names **present**; the row's left-hand condition is now
  predictable from the new evidence. The new section must not upgrade this to "in-range works":
  19 missing type names remain unexplained. The subtype WARNs stay `U`.

### F7 (medium, calibration) — `SKILL.md:468-470` is round-scoped and needs a named correction

- The old op-pair's cause remains unknown, but the stated **reason** ("its analyzer log was not
  retained") is no longer a standing limitation: `pilot/README.txt:4-6` shows 1 s polling retained
  the log, and R17 adds provider execution. The section should carry, verbatim or near:
  *"Round-14's 'adds no new provider execution' and 'log was not retained' are round-scoped. Round 17
  adds retained analyze runs; the old op-pair cause remains unknown because no pre-existing log
  exists, not because retention is impossible."*
- Do not claim the old cause is now explained.

### F8 (low-medium, calibration) — `SKILL.md:481` asks for a filename/digest the log cannot give

- The WARN names versions only; the filename/digest must come from
  `selection.py`/inventory. Record the WARN as the branch observation, the inventory identity as the
  byte evidence. Also: the fallback state is unexercised by the pilot and by the planned carriers;
  `go1.24.7` or any `1.25.x` is the cheap probe if C2 wants that row actually tested.

### F9 (low, operability) — pin the REA version and the CLI route

- `SKILL.md:12` still shows 6.4.0 as historical; `:19-20` lists 6.5.0 (Devin/OMP) and 6.7.0
  (Kimi). The pilot used 6.5.0. The new row must write `npx -y rea-agents@6.5.0` and say CLI, so a
  reader does not take the disabled MCP route or a different bridge/runtime-root lifecycle. Go
  message wording is bound to Ghidra 12.1.4.

### F10 (low) — `fromVersionString` does not exist; use the two real anchors

- `contract.md:63-64` says "normalize exactly as Ghidra's `GoVer.parse`/`fromVersionString`". No
  `fromVersionString` exists in `GoVer.java`. The actual law: `GoBuildInfo.java:488-489` strips a
  leading `go`; `GoVer.java:62-70` truncates at the first non-`[.0-9]` and splits; missing patch → 0.
  Observed cross-check: `go1.27.0-X:nodwarf5` → log `[1.27.0]` (`shfmt:83`);
  `go1.23.12` → `1.23.12` (`esbuild:67`). Cite these two anchors in the SKILL row rather than the
  nonexistent method.

## 3. Residual risk and verification gaps

- The pilot is not a receipt: no pre/post pins, no analyze stdout/evidence id, no inspect-go JSON, and
  both logs end mid-lifecycle at the bridge script with no terminal close line (`shfmt` ends 10:17:56,
  `esbuild` 10:19:53). Absence of a line near either tail is not evidence of absence; the new section
  must keep the `log_capture_limit` sentence.
- The "base present, zero applicable buckets" branch is unobserved on this host and cannot be
  produced without altering installed data; keep it as a prediction, as r14:464 already does.
- `predict.py`, `log-extract.py`, `compare.py`, `receipt-validate.py` do not exist in `w1` yet; F1's
  false-pass is a defect in the **specified** comparison, derived from source and the two pilot
  labels — not from running those tools.
- I did not run REA, Ghidra, or any carrier. No tool installs or upgrades were needed.

## 4. Bounded no-finding statements

- Searched `SKILL.md` for an existing "retained carrier"/"carrier diagnostics"/`ghidra.log` section or
  row: none; the file ends at `:507`.
- Searched the lane for an admitted real-carrier observation: none — `SKILL.md:468-470` states the
  opposite (no retained log), so the new section is genuinely new text, not a duplicate.
- `SKILL.md:483` and `:500` are not contradicted by the pilot; F3/F8 only bound what the logs can add
  to them. `SKILL.md:499` (1.24.5 exact patch) is untouched and unexercised by the pilot.
