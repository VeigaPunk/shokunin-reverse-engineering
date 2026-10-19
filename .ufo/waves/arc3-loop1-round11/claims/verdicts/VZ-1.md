# VZ-1 — arc3-loop1-round11 reconciliation verdict

Independent reconciliation of the frozen C1–C3 claims (`claims-frozen.md:15-54`). I re-derived the measurements below from the current local tools and immutable Git objects; peer artifacts were used to inventory candidate choices and check whether the independent findings agreed, not as evidence for my numeric results. Scratch and `TMPDIR` were confined to `/var/tmp` and removed. Git was read-only. This verdict is the only VZ-1 artifact.

## Revision and source-derived baseline

- `HEAD`: `e746ca79e2dbb3cb41436d612f448e81d2c6e585`.
- Work revision: `9c1d1fef5595b55d65764626249f164e6816473a`.
- I ran Command A exactly as specified in `SCORECARD.md:88-124`, against each immutable revision. Exact output:

```json
{"citation_resolved_rules": 16, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 89, "mapped": 89, "missing": [], "revision": "e746ca79e2dbb3cb41436d612f448e81d2c6e585", "rule_blocks": 16}
{"citation_resolved_rules": 16, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 89, "mapped": 89, "missing": [], "revision": "9c1d1fe", "rule_blocks": 16}
```

These are the pre-integration results, not the frozen C1 after-state. No candidate entry or coverage-map token is in either source tree; the required 90/90 after-state remains **UNVERIFIABLE** until one chosen pair lands and Command A is rerun at that revision.

## C1 — coverage / one named corpus Unknown

**REPRODUCED — bounded `inspect_artifact` Evidence-ID behavior. RECOMMEND EX-5 as the single draft. UNVERIFIABLE — corpus/map landing and 89→90 after-state.**

The delivered C1 set includes EX-1, EX-2, EX-3, EX-4, EX-5, EX-6, CR-1, and CR-2. The proposals are alternatives, not additive closures: EX-1/EX-3/CR-1 investigate `inspect_go_binary`; EX-2/EX-4/EX-5/CR-2 investigate `inspect_artifact`; EX-6 investigates a distinct Vyper hardfork case. I recommend EX-5's draft (`claims/c1/EX-5.md`) for one tightly scoped corpus entry: it uses a shipped ELF target, has an ordinary successful inventory path, and I independently reran the operation and hash controls. EX-2 is a synthetic ZIP; EX-4 explicitly uses `record-and-continue` after an integrity refusal; CR-2 is a second `inspect_artifact` target and corroborating alternative. The Go and Vyper candidates remain valid alternatives, but I did not independently re-run them in this seat. Co-land only one entry and its map token.

### First-hand `inspect_artifact` measurement

I used the cached `rea-agents@6.7.0` CLI at `/home/vgpnk/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/scripts/rea.mjs` and ran `inspect-artifact <path> --format json --full-output` twice on `/usr/bin/rustc`, then on a byte-identical copy under a unique `/var/tmp/.../copy/rustc` path. The copy preserved the executable mode. The target was read statically; it was not run.

Exact selected output from the three calls and an independent SHA-256 recomputation of each semantic projection:

```text
target_bytes=5240 target_mode=755 target_sha256=c916a85b7d4f52d9650399eebd15c672377933e6c2d8e98215757ab0b9b37136
copy_bytes=5240 copy_mode=755 copy_sha256=c916a85b7d4f52d9650399eebd15c672377933e6c2d8e98215757ab0b9b37136
base1_outer=ev_af8a969b19de83e5b57b0830d70663408de3ea3c419dd6e708323f48ab44b5d2 outer_recomputed=ev_af8a969b19de83e5b57b0830d70663408de3ea3c419dd6e708323f48ab44b5d2 match=true
base1_nested=ev_e435a6805e64e8bb12c4c5f018b61f97babb5193deb11f41cbeb20ab2525abf1 nested_recomputed=ev_e435a6805e64e8bb12c4c5f018b61f97babb5193deb11f41cbeb20ab2525abf1 match=true
base2_outer=ev_af8a969b19de83e5b57b0830d70663408de3ea3c419dd6e708323f48ab44b5d2 outer_recomputed=ev_af8a969b19de83e5b57b0830d70663408de3ea3c419dd6e708323f48ab44b5d2 match=true
base2_nested=ev_e435a6805e64e8bb12c4c5f018b61f97babb5193deb11f41cbeb20ab2525abf1 nested_recomputed=ev_e435a6805e64e8bb12c4c5f018b61f97babb5193deb11f41cbeb20ab2525abf1 match=true
copy_outer=ev_72b5ff45b74cdd6f6a6562ebcd6a287948448270b4b0f444acfbc53ed22370be outer_recomputed=ev_72b5ff45b74cdd6f6a6562ebcd6a287948448270b4b0f444acfbc53ed22370be match=true
copy_nested=ev_e435a6805e64e8bb12c4c5f018b61f97babb5193deb11f41cbeb20ab2525abf1 nested_recomputed=ev_e435a6805e64e8bb12c4c5f018b61f97babb5193deb11f41cbeb20ab2525abf1 match=true
```

A second same-mode copy comparison showed the only changed `data` paths were `evidence_id`, `subject.local_path`, `normalized_result.inspection_id`, and `normalized_result.substeps[0].evidence.subject.local_path`; the nested inventory Evidence ID stayed fixed. Thus the outer ID changes with the path-bearing nested result on this invocation shape, while same-path calls reproduce. The installed package's semantic projection is at `/home/vgpnk/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/dist/domain/evidence.js:159-183`; canonical SHA-256 serialization is at `/home/vgpnk/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/dist/domain/canonicalDigest.js:8-25,27-76`. This establishes the behavior for this operation, package version, ELF, and call shape only—not a universal REA ID formula.

**Disposition:** use one bounded EX-5 corpus draft plus one matching map token, then rerun Command A at the landing revision. Do not report 90/90 before that check.

## C2 — freshness / PROVINCE inventory receipt

**VERIFIED — Ghidra module counts; delta 0/0; NO-CHANGE.**

I independently enumerated immediate child directories in the installed Ghidra `Features` and `Processors` trees and read `application.version`. `PROVINCE.md:46` records 34 feature directories and 39 processor modules. Exact measured output:

```text
install=/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC
application.version=12.1.4
Features: count=34
Processors: count=39
```

Measured deltas are `34 − 34 = 0` features and `39 − 39 = 0` processors. The count receipts in EX-11, EX-12, SC-1, and SC-2 agree with this independent enumeration. Disposition: retain the PROVINCE values; no erratum is indicated. This counts immediate directories in this installation; it does not prove each module loads or is available through a particular REA session. I did not independently re-count the alternate pacman/ASAR candidates; EX-10 itself bounds its ASAR result to readable roots and leaves the denied subtree unresolved (`claims/c2/EX-10.md:7-9,39-42`).

## C3 — calibration / `available:true` session-scoped class

**REPRODUCED at provider-capability scope; DISCREPANCY at targetless tool-readiness scope; UNVERIFIABLE for the attached Codex server.**

The active seat did not expose REA MCP tools, so I launched the cached REA 6.7.0 stdio server directly and called `binary_session` with `{}`. The returned session had `open:false`; no target was opened and neither artifact operation was invoked. Selected exact response values:

```json
{
  "server": {"name": "rea", "version": "6.7.0"},
  "open": false,
  "capability_groups": [{
    "provider": "rea-artifact-graph",
    "operations": ["extract_artifact", "inspect_artifact"],
    "available": true,
    "reason": null
  }],
  "tool_availability": [
    {"surface": "artifact-provider", "names": ["extract_artifact"], "available": false, "reason": "target_required", "remediation": "Call open_binary with a supported local target."},
    {"surface": "artifact-provider", "names": ["inspect_artifact"], "available": false, "reason": "target_required", "remediation": "Call open_binary with a supported local target."}
  ]
}
```

This independently reproduces `available:true` for the shared provider capability group, consistent with the provider-capability method recorded at `PROVINCE.md:50`. It does **not** mean either exact operation is callable in this targetless session: both per-tool entries are false until a supported target is opened. PL-1 and RV-6 correctly separate these two scopes (`claims/c3/PL-1.md:18-24`; `claims/c3/RV-6.md:17-21`); provider-only CLI capability results do not settle targetless per-tool readiness.

I also ran `node /home/vgpnk/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/scripts/rea.mjs doctor --client codex --json`. It exited 1; the exact relevant fields were `registration:codex ok:false classification:config_drift detail:/home/vgpnk/.codex/config.toml` and `live_server.state:unknown`. Doctor therefore did not identify the attached server or establish its operation-level availability. No REA/client setup, registration edit, restart, artifact open, or extraction was performed. A `binary_session {}` from the actually attached client remains necessary to settle that separate scope.

## Integration disposition

- **C1:** recommend one EX-5 `inspect_artifact` entry and its single map token; Command A must show 90 knowledge files / 90 mapped with empty missing/dangling sets at the landing revision.
- **C2:** retain the current 34/39 Ghidra inventory values; measured deltas are zero.
- **C3:** preserve the provider-level `available:true` result but qualify its scope; the targetless tool gates are `target_required`, and the attached server remains unknown.

No corpus, map, PROVINCE, SKILL, SCORECARD, LOG, gate source, custody path, or peer artifact was changed by VZ-1. No Git mutation was performed.