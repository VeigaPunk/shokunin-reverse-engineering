# `inspect_artifact` Evidence-ID domain in REA 6.7.0 — same-path repeat stable, same-name byte-identical input at a different path changes the outer ID

source: `.ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence/{inspect-artifact-base-1.json,inspect-artifact-base-2.json,inspect-artifact-copy.json,inspect-artifact-same-name-other-path.json,identity.txt,calls.txt,recompute-ids.py,recompute-ids-output.txt}`; package and algorithm source identities are recorded in `identity.txt`.

verified-at: 2026-10-19

recheck: use the pinned `rea-agents@6.7.0` cache path recorded in `identity.txt`, set `TMPDIR` to a directory under `/var/tmp`, and run the four exact calls in `calls.txt` after making byte-identical copies of `/usr/bin/jq` at the two recorded alternate paths. Then run `python3 .ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence/recompute-ids.py`. Do not use `/tmp` for scratch.

## Observation

The analyzed target was `/usr/bin/jq`, SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`, a 30,800-byte ELF. Both copies have the same measured SHA-256 and size; the controlled alternate at `/var/tmp/kaidoku-arc3-r11-cr2-probe/other-path/jq` retains the subject basename `jq`. Four successful REA CLI calls used the exact invocation `inspect-artifact <path> --format json --full-output` with REA 6.7.0; stdout envelopes are retained in `evidence/`.

Two calls on `/usr/bin/jq` returned the same outer `inspect_artifact` Evidence ID, `ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca`. The same-basename copy at the alternate path returned `ev_38cc43f4175331e53c7cd1bcefea9736028dc596bf84315d75b3a86505c9613c`; the copy with a different basename returned `ev_b3ebd1711ebc131bf0acc53e27b4a4d1e404a0c494d3baa0dc0ff76c5d61f88a`. The nested `inventory_artifact` Evidence ID is `ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435` for all four calls. The generated `inspection_id` is `ai_78cf490802e595884543670257cc4f4e11b4169f1fc14e2e53c755e4168883e2` at the original path and `ai_7c39b0eafa8f1b473a78c8a51436ed1d589452cded9a7cad05e088acdc301b5b` at the same-basename alternate path.

The returned root inventory is one ELF node and occurrence with zero edges, complete root coverage, and the limitation `Artifact has no child container entries.` The report notes that `open_binary` was not run. No target execution is claimed.

## Re-derived ID behavior

The independent script in the source bundle recomputed all four reported `ev_` digests exactly. A projection check that changes only the outer subject's display name and path preserves its ID. A second check changes only `normalized_result.substeps[0].evidence.subject.local_path` and changes the outer ID; the controlled same-basename copy gives the corresponding live observation while holding the name and bytes fixed. This is consistent with the package source: `evidence.js:159-183` projects the top-level subject to digest/format/architecture but includes `normalized_result`; `artifactInspection.js:111-155` retains the nested inventory Evidence inside `normalized_result` and hashes its semantic inspection object; `canonicalDigest.js:8-25,60-76` hashes canonical JSON with SHA-256. The observed path sensitivity is specific to this `inspect_artifact` wrapper's nested result on the measured target and call shape, not a universal rule for REA Evidence IDs.

## Limits

Only REA 6.7.0, `inspect_artifact`, this one ELF byte identity, a same-path repeat, and two alternate paths were measured. The result does not establish behavior for archive/container inputs, other verbs, other releases, other parameter values, error envelopes, or MCP-session evidence. No format-specific `open_binary` analysis, execution, network activity, or deployment claim was made. Command A's 90/90 post-integration result remains pending the co-landed corpus entry and map token.

