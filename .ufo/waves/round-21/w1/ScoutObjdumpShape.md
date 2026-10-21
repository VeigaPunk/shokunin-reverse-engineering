# R20 objdump architecture Evidence record shape

## Findings

**Axes:** calibration (treat the witness as pathless, not subject-bound) and depth (inspect the retained record fields, not just operation tokens).

The retained R20 architecture output is one JSON Evidence record at `.ufo/waves/round-20/evidence/c2/objdump/architectures-json/stdout.json:1`. Its `subject` member is present and has JSON value `null`—it is not absent. The record has 16 top-level members:

- `evidence_id`: `ev_4d59366d3e60960da306e5b984acca68678ca83f20dd5d2ae40cb5f4851719b7`.
- `subject`: `null`.
- `provider`: `{id: "gnu.objdump", name: "GNU objdump", version: null}`.
- `analysis_profile`: `null`; `predicate_type`: `rea.reverse-engineering.command-observation`; `operation`: `inspect_with_objdump`.
- `parameters`: `{operation: "architectures", provider_executable: "objdump", command_arguments: ["-i"]}`. No artifact path is present.
- `raw_result` and `normalized_result`: each has the same eight members: `stdout` (string), `stderr` (empty string), `exit_code` (0), `signal` (`null`), `output_truncated` (`false`), `completion_status` (`complete`), `artifact_sha256_after` (`null`), `artifact_changed` (`null`). The two objects compare equal in the retained JSON. The stdout is 94 lines / 2,343 UTF-8 bytes; its first line says `BFD header file version (GNU Binutils) 2.47`. That output header does **not** change the separate `provider.version: null` field.
- `confidence`: `observed`; `authority`: `shipped-artifact`; `environment`: `null`.
- `limitations`: four strings, explicitly noting unavailable artifact identity, unreported objdump version, preserved nonzero exits, and independence from a selected artifact.
- `relationship_coverage`: `null`; `locations` and `evidence_links`: empty arrays.

The local stdout file is 6,179 bytes with SHA-256 `305f462825412b39476d80325eec055f92790fb42342666f82180abb5e2e785e`; the adjacent retained `receipt.json` binds that digest, byte count and Evidence ID at its `stdout.*` / `evidence_id` members. The retrospective coverage record binds the same ID and path at `.ufo/waves/round-20/verify/round20/measure.json:613-621`. This reports record/file identity, not cryptographic authentication of the Evidence ID.

The matching R20 knowledge entry states at `corpus/knowledge/2026-10-20-r20-objdump-architecture-list.md:9` (11-word located quote): “subject is null, provider is `gnu.objdump`, and provider version is null.” Its `:16-17` limits the result to one host's BFD inventory and does not establish general architecture coverage. The appended `:20-28` correction attributes pathlessness to construction and separates the objdump listing from the companion jq disassembly subject. The verifier lesson independently points to the `subject: null` boundary at `corpus/lessons/round-20-verifier-spotcheck.md:101`.

R21's frozen fixture contract directly preserves this boundary: `.ufo/waves/round-21/fixture-contract.json:14-15` requires the positive case to accept `inspect_with_objdump` plus `parameters.operation == "architectures"` with null subject under a pathless limit, while the wrong-parameter control must reject a `disassemble` record whose architecture mention is unrelated prose. The `--schema` argument-property observation in the knowledge entry is a CLI-argument schema fact, not a schema for this Evidence JSON object.

## Evidence status and limits

- **Observed:** the retained JSON's actual member names/values above; no path argument or selected artifact digest occurs in this record. The stdout itself reports a BFD target listing.
- **Inference, narrowly:** this witness is pathless because its parameters carry only `-i` and its record has null subject. This is consistent with the R20 knowledge entry's construction note; it is not a subject-bearing artifact observation.
- **Unresolved:** I did not inspect the installed package source or trace producer/caller definitions. No LSP device is mounted (`xd://lsp` returned “No such tool”), so any text search is only a locator, not semantic proof. The retained knowledge entry cites S048 for package-source anchors, but those anchors were not independently reopened here. No external URL was opened; no external quote/date applies.

## Scope and checks

Read-only research of the named R20 record, its retained receipt/output binding, the R20 knowledge/lesson references, and the frozen R21 fixture case. A local standard-library JSON parse was used only to enumerate fields and compare raw/normalized values; it did not invoke REA, objdump, or a live provider. The receipt was parsed for output identity; its environment metadata is omitted from this report. No tests, builds, lint, production edits, source-row writes, installs, or live configuration/HOME-file reads were performed.

No check is needed for this advisory report itself. If this evidence informs C1 implementation, parent should run the frozen C1 battery once after integration: `python3 -I -B .ufo/waves/round-21/battery.py --root <LANE> --rev <REV> --claim C1`, then the planned final suite; this scout ran neither.

Report: `.ufo/waves/round-21/w1/ScoutObjdumpShape.md`