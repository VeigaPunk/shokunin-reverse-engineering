source: `.ufo/waves/arc3-loop1-round12/claims/c1/CR-3.md`; complete first-hand probe envelopes and re-derivation output under `.ufo/waves/arc3-loop1-round12/claims/c1/CR-3/evidence/`; pinned package-source identities in `evidence/identity.txt`.
verified-at: 2026-10-19
recheck: `bash .ufo/waves/arc3-loop1-round12/claims/c1/CR-3/evidence/recheck.sh` — creates same-byte copies of `/usr/bin/jq` under `/var/tmp`, runs four `inspect-artifact` calls with `rea-agents@6.7.0`, then recomputes both parent and nested IDs from the package's `digestCanonicalValue`; expect the nested `inventory_artifact` projection to match and hash to one ID across all four runs while the parent `inspect_artifact` projection changes across paths. The script verifies pinned source hashes and does not execute the target. It never uses `/tmp`.

# `inventory_artifact` Evidence ID is path-stable for one bare ELF in REA 6.7.0

This draft narrows the C1 candidate in `.ufo/waves/arc3-loop1-round12/claims-frozen.md:22-23`: for the internal `inventory_artifact` Evidence emitted as `inspect_artifact`'s substep, does the selected absolute target path affect the `ev_` ID when it is absent from that operation's semantic projection? The result is bounded to `rea-agents@6.7.0`, the exact `/usr/bin/jq` ELF bytes below, `integrity_policy: "fail"`, and a root-only inventory. `inventory_artifact` is an internal provider operation, not a separately exposed CLI command (`dist/contracts/artifactToolContracts.js:77-80`); the public recheck therefore invokes its enclosing `inspect-artifact` command.

## Re-derived observations

The pinned target `/usr/bin/jq` is SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` (30,800 bytes). Two copies under different paths have that same digest. Four successful `inspect-artifact <path> --format json --full-output` calls yielded:

- `/usr/bin/jq` twice: outer `inspect_artifact` ID `ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca`; nested `inventory_artifact` ID `ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435`.
- `/var/tmp/kaidoku-cr3-r12/alternate/jq` (same basename): outer ID `ev_11da29de7efeb77a1b272846b96cf9262e0cb9508fdb48bdfde5f0b09ee3928a`; nested ID remains `ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435`.
- `/var/tmp/kaidoku-cr3-r12/renamed/jq-copy` (different basename): outer ID `ev_c2cc7d48b96283023e5b58ec105dbc889d36d1f5c9e40a40d9920f20958b3ac6`; nested ID remains `ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435`.

All four full envelopes are retained in `evidence/{base-1,base-2,alt-same-name,alt-different-name}.json`. `evidence/rederive.mjs` independently reconstructs the semantic projection for both operations and recalculates the `ev_` IDs with the pinned package's canonical-digest implementation. All eight recomputations match their emitted IDs. Across the four nested inventory records, the computed projection objects are structurally equal; across the parent records they are not.

## Identity rule and path boundary

In the installed `dist/domain/evidence.js:159-183`, an Evidence ID is `ev_` plus lowercase SHA-256 over the canonical JSON semantic projection. The projection excludes the ID and projects `subject` to only `{digest, format, architecture}`; it includes `provider`, `analysis_profile`, `predicate_type`, `operation`, `parameters`, `raw_result`, `normalized_result`, `confidence`, `authority`, `environment`, `limitations`, `relationship_coverage`, `locations`, and `evidence_links`. `dist/domain/canonicalDigest.js:8-25,60-76` emits compact canonical JSON with sorted keys and hashes its UTF-8 bytes. The source files' SHA-256 identities are in `evidence/source-files.sha256`.

`dist/artifacts/ArtifactProvider.js:219-243` builds the nested `inventory_artifact` record with parameters containing only `integrity_policy`, a subject derived from the selected path and inventory manifest, and `locations: []`. The Evidence subject still displays `name` and `local_path`, but those display fields are omitted by the semantic projection. In these root-only single-file outputs, the inventory's only path-like value is the stable logical path `"."`; no selected absolute path occurs in the nested projection (`evidence/rederive-output.txt`). Thus the nested ID is path-stable in this measured case.

This does not make the enclosing `inspect_artifact` ID path-stable: `dist/domain/artifactInspection.js:111-128` embeds the complete nested Evidence, including its display subject, in the parent's `normalized_result`, and `evidence.js:173` hashes that result. The parent ID changed across the alternate paths while its nested inventory ID did not. This is a per-projection result, not a universal rule for Evidence IDs.

## Scope and limits

Only REA 6.7.0, `inspect_artifact`'s internal `inventory_artifact` substep, this one 30,800-byte ELF, and a root-only inventory were measured. The operation's result contains one occurrence with logical path `"."`; archive/container member paths may be semantic content and are not tested. No other artifact type, package version, request option, failure envelope, or MCP-session call is covered. REA statically parsed the artifact; no target execution, network access, or chain of custody claim is made.
