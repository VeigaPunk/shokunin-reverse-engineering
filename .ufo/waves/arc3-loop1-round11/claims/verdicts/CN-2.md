# CN-2 — arc3-loop1-round11 per-item convergence verdict

This reconciles the frozen C1–C3 claims (`claims-frozen.md:15-54`) against the delivered seat reports and independent checks. These are per-axis findings, not a scalar or an overall pass. I wrote only this CN-2 artifact; no corpus, map, PROVINCE, SCORECARD, LOG, gate, or Git mutation was made.

## Revision and source-derived baseline

`git rev-parse HEAD` returned `e746ca79e2dbb3cb41436d612f448e81d2c6e585`; resolving the named work revision returned `9c1d1fef5595b55d65764626249f164e6816473a`. I ran SCORECARD Command A unchanged (`SCORECARD.md:88-124`) against both immutable revisions:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"HEAD","rule_blocks":16}
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"9c1d1fef5595b55d65764626249f164e6816473a","rule_blocks":16}
```

These are pre-integration controls. Neither revision measures the required 90/90 after-state.

## C1 — one third-verb Evidence-ID domain

**Candidate observation: REPRODUCED, narrowly. Frozen coverage closure: NOT YET VERIFIED.** The eight C1 reports select `inspect_artifact` four times (EX-2, EX-4, EX-5, CR-2), `inspect_go_binary` three times (EX-1, EX-3, CR-1), and a Vyper Cancun variant once (EX-6). This is a plurality for `inspect_artifact`, not an absolute majority. The Go reports reuse `/usr/bin/docker`; the `inspect_artifact` reports cover ZIP, ASAR, and ELF targets. See `c1/EX-2.md:13-26`, `c1/EX-4.md:5-7,20-31`, `c1/EX-5.md:13-26`, `c1/CR-2.md:5-16`; compare `c1/EX-1.md:26-48`, `c1/EX-3.md:13-24`, `c1/CR-1.md:11-23`, and `c1/EX-6.md:3-17`.

I made an independent static REA 6.7.0 check with `inspect-artifact /usr/bin/jq --format json --full-output`, repeated at the same path and then against a byte-identical copy at `/var/tmp/kaidoku-arc3-r11-cn2-artifact/copy/jq` (all REA `TMPDIR` state was under `/var/tmp`). `sha256sum` returned `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` for both files; `cmp` exited 0.

```text
base-1: ok=true, operation=inspect_artifact, evidence_id=ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca
base-2: ok=true, operation=inspect_artifact, evidence_id=ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca
copy:   ok=true, operation=inspect_artifact, evidence_id=ev_2808287566546efb8b2657a01fd45e60008c8b5b675c2baa984bc4bcb849ae10
nested inventory_artifact id, all three: ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435
```

I reconstructed the package's semantic projection (`rea-agents@6.7.0/dist/domain/evidence.js:159-183`) and canonical SHA-256 (`dist/domain/canonicalDigest.js:8-25,60-76`) independently; the recomputed IDs matched all three returned IDs. The base-to-copy result diff includes `normalized_result.inspection_id` and `normalized_result.substeps[0].evidence.subject.local_path`; the outer display `subject.local_path` changes too but is excluded from the top-level projection. This corroborates the nested-result/path mechanism described in `c1/EX-4.md:20-30`, `c1/EX-5.md:17-19`, and `c1/CR-2.md:12-13,38-40`. This is a bounded result for one successful operation, target class, and REA version—not a universal formula for every verb, format, version, or error envelope. EX-4's successful ASAR run required `--integrity-policy record-and-continue` after a default-policy integrity refusal; retain that limitation (`c1/EX-4.md:26-35`). EX-6's separate Vyper result also remains bounded and explicitly does not close the broader Unknown (`c1/EX-6.md:3,11-17`).

**Convergence recommendation:** select one `inspect_artifact` entry/token, not four duplicate entries. The four drafts agree on the proposed basename/token `2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain`, but split 2–2 on the map row (Archives & packages versus Evidence model). I recommend the **Evidence model** row (`corpus/README.md:41`): the finding is about the semantic Evidence-ID projection, and the observed targets are not all archives. This row choice is a verifier's semantic adjudication, not a peer majority. Parent integration should preserve the different target and integrity limitations and avoid generalizing beyond `inspect_artifact`.

**Landing status: UNVERIFIABLE / open.** All C1 reports leave the proposed knowledge entry and map token as drafts. Command A currently measures 89 files / 89 mapped at both revisions, with no missing or dangling tokens; no 90/90 result exists in this worktree. C1 is not closed until one entry and its token co-land and Command A is rerun at that landing revision (`claims-frozen.md:23-28`).

## C2 — freshness receipt

**VERIFIED — no-change disposition.** Four of eight C2 reports select Ghidra, three select the pacman cache, and one selects the ASAR inventory. I independently enumerated immediate directories in `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/{Features,Processors}` and read `Ghidra/application.properties`:

```text
application.version=12.1.4
Features: count=34
Processors: count=39
```

Against `PROVINCE.md:46`, the feature delta is `34 - 34 = 0` and processor delta is `39 - 39 = 0`. **Disposition: retain the recorded counts; no erratum is indicated.** This confirms an install directory inventory, not that every module loads or is available in an REA session. The four Ghidra receipts independently agree (`c2/EX-11.md:3-5,41-44`, `c2/EX-12.md:7-11`, `c2/SC-1.md:31-36`, `c2/SC-2.md:8-11`). The alternate receipts are bounded and do not conflict: pacman re-counts 1,350 archives with 0 missing/orphan sidecars (EX-7..EX-9), while EX-10 re-counts 12 ASAR files in its readable roots but leaves host-wide completeness unresolved due to `/opt/containerd` permission denial (`c2/EX-7.md:31-41`, `c2/EX-8.md:12-23`, `c2/EX-9.md:8-10`, `c2/EX-10.md:7-9,39-42`). The selected Ghidra observation satisfies the frozen measured-delta/disposition requirement (`claims-frozen.md:30-41`).

## C3 — `available:true` capability re-probe

**REPRODUCED at provider-capability scope; DISCREPANCY if read as targetless tool readiness; active Kimi session UNVERIFIABLE.** I launched the cached REA 6.7.0 stdio server under `/var/tmp`, initialized MCP `2025-03-26`, and called `binary_session` with `{}`. The response identified REA 6.7.0 and `open:false`:

```text
provider rea-artifact-graph, operations [extract_artifact, inspect_artifact]: available=true, reason=null
extract_artifact tool_availability: available=false, reason=target_required
inspect_artifact tool_availability: available=false, reason=target_required
```

Thus the provider-level `available:true` recorded at `PROVINCE.md:50` reproduces; in the same empty-target session, neither exact tool is ready to run until `open_binary` selects a supported target. No target was opened or extracted. This matches the direct session reports PL-1 and RV-6 (`c3/PL-1.md:7-10,18-24`, `c3/RV-6.md:7-21`); PL-2/RV-4/RV-5 reproduce the provider capability via CLI, while RV-1..RV-3 cannot determine live availability from doctor-only results (`c3/PL-2.md:7-23`, `c3/RV-1.md:5-22`, `c3/RV-2.md:7-34`, `c3/RV-3.md:8-39`, `c3/RV-4.md:7-31`, `c3/RV-5.md:11-27`).

The local stdio probe is not the attached Kimi agent session. My separate `rea doctor --client kimi --json` exited 1; `registration:kimi` was `config_drift` at `/home/vgpnk/.kimi-code/mcp.json`, and `identity.live_server.state` was `unknown`. This establishes neither `available:true` nor `available:false` for the currently attached Kimi session. No configuration change was made. The frozen C3 capability class is reproduced, but active-client readiness remains unresolved (`claims-frozen.md:43-54`).

## Scope

No corpus integration, map change, PROVINCE/SCORECARD/LOG edit, gate change, or Git mutation was performed. This verdict records bounded measurements and dispositions only; it is not a claim that all three axes are closed.
