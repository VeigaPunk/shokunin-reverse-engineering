# Envelope privacy review

## Scope and verdict

- Observation: scanned 55 JSON files present at the final inventory: the L1 probe, 24 `Run*/envelopes` results, 9 `ReplayA` results, and 21 `ReplayB` results (including ten failed-attempt receipts and one touch-test result). No REA calls, installs, or envelope edits were made.
- Verdict: **commit with a stated redaction**, not as is. Redact the scratch-path fields in successful alternate-copy envelopes and omit the ten provider-unavailable `ReplayB` attempt receipts. Keep originals private if provenance is needed.
- Observation: no secret values or usable network addresses were observed. The findings below are low-severity privacy and environment disclosures, not evidence of credential exposure.

## Finding 1 — alternate-copy envelopes expose private scratch paths

- Severity: Low. Observation: successful copy/alternate envelopes contain absolute paths below the private scratch tree. Run copies use `$.data.subject.local_path`; Replay A and Replay B alternates use the same field. The layout envelopes also repeat the path at `$.data.parameters.path`, `$.data.normalized_result.artifact.path`, and `$.data.locations[0].path`.
- Evidence command: timestamped `jq -c` selection over representative L1, Run, Replay A, and Replay B envelopes; exit 0 at `2026-10-22T12:21:07Z`. The all-file scan also found exactly three distinct scratch-path values, at `2026-10-22T12:22:12Z`, `jq_exit=0`.
- Exact output excerpt (scratch prefix redacted for this public report): `{"file":"ReplayB/envelopes/inspect-binary-layout-alt3.json","ok":true,"environment":null,"subject_path":"[redacted scratch path]","parameter_path":"[redacted scratch path]","artifact_path":"[redacted scratch path]"}`. The touch-test envelope has the same path-bearing JSON fields.
- Inference: the path values expose the carrier copy location and the Replay A / Replay B alternate locations.
- Exploit path: a public repository clone exposes contributors' scratch layout and seat-specific paths. Inference (impact): local workspace names and test organization become public; no account access follows from this alone.
- Smallest remediation: replace each absolute scratch prefix with a neutral stable placeholder while preserving the distinction between original and alternate inputs; cover the repeated layout fields too.

## Finding 2 — failed Replay B receipts disclose host and provider configuration

- Severity: Low. Observation: ten `*.attempt1.json` files are `ok:false`, `error.code="provider_unavailable"`. The diagnostics disclose the Java home/version and Hopper path, and name provider configuration variables as unset or required. No variable values or credentials were present.
- JSON paths: `$.error.details.rejections[0].diagnostics.java_home`, `.java_version`, and `.checks[0].detail`; `$.error.details.rejections[1].diagnostics.launcher_path`; `$.error.details.rejections[2].reason`; and, for layout attempts, `$.error.message` and `$.error.details.rejections[0].diagnostics.configuration_key`.
- Evidence command: timestamped `jq -c` selection of `instructions-base.attempt1.json` and `inspect-binary-layout-base.attempt1.json`; exit 0 at `2026-10-22T12:21:07Z`. Exact excerpts, with host paths redacted: `"java_version":"21.0.12.1","install_check":"GHIDRA_INSTALL_DIR is not set"`; `"launcher":"[redacted Hopper path]"`; `"configuration_key":"REA_PWNTOOLS_PYTHON"`; the other receipt contains `"Set REA_IDA_MCP_CONFIG"`.
- Exploit path: a public reader can fingerprint the host's JVM and infer which analysis integrations are absent. Inference (impact): modest environment disclosure; no token, credential, or live network endpoint was exposed.
- Smallest remediation: omit these failed provider-selection receipts from the public envelope set. If retained, remove `error.details.rejections` and provider-specific remediation text.

## Checks that held

- Observation: the recursive scalar scan across all 55 files returned `non_null_environments=[]`, `home_or_username=[]`, and `secret_markers=[]`. The only dotted-quad candidate was `21.0.12.1`, the JDK version in the failure diagnostic; no URL, IPv6 address, or network endpoint was found.
- Evidence command: timestamped `jq -sc` recursive marker summary over the 55 enumerated envelopes; exact output fields: `"files":55`, `"non_null_environments":[]`, `"home_or_username":[]`, and `"secret_markers":[]`; `jq_exit=0` at `2026-10-22T12:22:12Z`.
- Observation: successful subjects identify `jq` with SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`. The read-bytes envelope reports 64 requested and returned bytes for that subject at `0x103fa0`.
- Inference: the read-bytes sample is from the identified jq artifact; no content from another file was identified.
- Evidence command: timestamped `jq -c` selection of `RunReadBytesLayout/envelopes/read-bytes-base.json`; exit 0 at `2026-10-22T12:21:07Z`. Exact excerpt: `{"subject_sha256":"e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806","address":"0x103fa0","requested_bytes":64,"returned_bytes":64,"bytes_hex":"554889e541574989ff415641befcffffff41554589cd4154534883ec18448945c8ff15413f0000660f1f8400000000004c89ffff15af3f00004989c44889d348"}`.
