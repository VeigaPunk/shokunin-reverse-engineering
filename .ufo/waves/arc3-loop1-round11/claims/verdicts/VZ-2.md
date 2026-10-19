# VZ-2 — arc3-loop1-round11 independent reconciliation

Measured against `HEAD=e746ca79e2dbb3cb41436d612f448e81d2c6e585`; comparison work revision `9c1d1fef5595b55d65764626249f164e6816473a`. I re-derived the measurements below; peer artifacts were used to compare candidate choices and scopes, not as measurement evidence. This is a per-item verdict, not a scalar round result.

## C1 — coverage / one named corpus Unknown

**Candidate verdict: REPRODUCED, narrowly for CR-2's `inspect_artifact` Evidence-ID draft. Coverage after-state: UNVERIFIABLE.** The frozen claim requires one third-verb Evidence-ID family and one co-landed knowledge entry/map token (`claims-frozen.md:15-28`); the candidate drafts are alternatives, not additive closures.

I used the cached `rea-agents@6.7.0` CLI and ran `inspect-artifact <path> --format json --full-output` twice against `/usr/bin/jq`, then against a byte-identical copy created with `shutil.copy2` so its executable mode was preserved. The artifact was inspected statically, not executed. The source SHA-256 was `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`; size was 30,800 bytes and both original and copy had mode `0755`.

```text
/usr/bin/jq repeat 1: outer=ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca nested_inventory=ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435
/usr/bin/jq repeat 2: outer=ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca nested_inventory=ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435
same-byte, same-mode copy: outer=ev_72e0780302c6c0af91289dc7e3a2adcdceb2b762c685f1e48c7549599a41d4aa nested_inventory=ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435
independent outer and nested semantic-projection recomputations: all matched
```

This supports same-path repeatability and a path-sensitive outer ID for this invocation: the nested `inventory_artifact` ID remained stable while the outer `inspect_artifact` ID changed at the alternate path. The installed 6.7.0 implementation projects the outer Evidence at `dist/domain/evidence.js:159-183`, uses canonical SHA-256 at `dist/domain/canonicalDigest.js:8-25,27-76`, and embeds the nested inventory Evidence in the inspection result at `dist/domain/artifactInspection.js:111-156`. The observation is limited to this operation, ELF, package version, and successful call shape; it is not a universal REA ID formula. My earlier exploratory `copyfile` comparison was excluded because it did not preserve file metadata.

Peer recommendations differ: VZ-1 selected EX-5; VZ-3 and CN-1/CN-2/CN-3 selected CR-2; VZ-4 and CN-4 selected an `inspect_go_binary` draft. EX-6 is a separately valid Vyper hardfork alternative. I recommend **CR-2 as the sole C1 integration candidate** because this seat's controlled, metadata-preserving `inspect_artifact` rerun directly supports its bounded draft. The other candidates remain alternatives; do not co-land multiple C1 entries/tokens.

I ran Command A from `SCORECARD.md:88-124` against both immutable revisions. Both results were pre-integration controls:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"e746ca79e2dbb3cb41436d612f448e81d2c6e585","rule_blocks":16}
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"9c1d1fef5595b55d65764626249f164e6816473a","rule_blocks":16}
```

No entry or token has been integrated. The required 90 knowledge files / 90 mapped post-state is **UNVERIFIABLE** until exactly one entry and its matching token land and Command A is rerun on that revision. CR-2's proposed entry is `2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md`; its matching token belongs in the Evidence model row of `corpus/README.md:41`.

### Gate revision identity

`python3 .ufo/gates/c1-census-v10.py --quiet` passed at current HEAD: 14 G21 frontier rows asserted, `errors: []`, and `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`. The gate SHA-256 at work revision `9c1d1fe...` is `d6b4deaa5973d3a29260b0e325620d87a3cc59464771688f97cb1c62d138fc80`; at current HEAD it is `b325a6caddafb9e209f292dec873dec582a3f7a244d135e4f25205907cec9573`. Read-only `git diff 9c1d1fe... e746ca7... -- .ufo/gates/c1-census-v10.py` shows one changed line: the SCORECARD scope end moves from line 1924 to 1975. Therefore `d6b4...` identifies the work-revision gate, not the current HEAD gate.

## C2 — freshness receipts

**REPRODUCED / NO-CHANGE for the three re-derived values, with their measurement boundaries.** The frozen C2 asks for a measured staleness receipt and disposition (`claims-frozen.md:30-41`). Ghidra alone is sufficient as the selected receipt; the additional pacman and ASAR measurements are corroborating candidates, not extra C2 closures.

- **Ghidra — REPRODUCED, delta 0/0.** Re-read `application.version` and counted immediate directories in the installed `Ghidra/Features` and `Ghidra/Processors` trees: version `12.1.4`, Features `34`, Processors `39`. These match `PROVINCE.md:46`; retain the values. This is an installed-directory count, not a module-loadability claim.
- **Pacman cache — REPRODUCED, current delta 0.** Read-only enumeration of `/var/cache/pacman/pkg` returned `archive_files=1350`, `signature_sidecars=1350`, `missing=0`, `orphan=0`, matching the current count at `PROVINCE.md:50`. The dated `1,556` value is the 2026-10-13 snapshot; `1350 - 1556 = -206` is only a comparison to that historical record, whose old directory state was not remeasured today. Filename pairing does not cryptographically validate signatures or packages.
- **ASAR — REPRODUCED, bounded.** Focused enumeration of regular `*.asar` files in `/usr/lib`, `/usr/share`, `$HOME/.config`, `$HOME/.local/opt`, and `/opt/1Password` returned `12`, matching `PROVINCE.md:49`. A wider `/opt` traversal could not read `/opt/containerd` (`drwx--x--x 1 root root 12 Oct 9 23:03`); do not claim host-wide inventory completeness.

No current count correction is indicated. No PROVINCE or corpus edit was made.

## C3 — `available:true` capability class

**REPRODUCED at provider-capability scope; DISCREPANCY if read as targetless tool readiness; active Kimi session UNVERIFIABLE.** A fresh REA 6.7.0 `capabilities --format json` call and an independently launched stdio MCP session both reported the `rea-artifact-graph` group containing `inspect_artifact` and `extract_artifact` as `available:true`. `tools/list` returned 207 tools including both operations. In `binary_session {}`, the session was `open:false`, `cleanup_pending:false`, and both per-tool entries were `available:false`, `reason:"target_required"`, with remediation `Call open_binary with a supported local target.` No target was opened and neither operation was invoked.

Thus `PROVINCE.md:50` is reproduced if `available:true` means shared provider capability; it is not evidence that either tool is callable in a targetless session. `rea doctor --client kimi --json` exited 1, reporting the Kimi registration missing/config-drift at `/home/vgpnk/.kimi-code/mcp.json` and `live_server.state:"unknown"`. This does not establish what the attached Kimi client can call. Keep that separate from the TOML pin recorded at `PROVINCE.md:18`; the two paths are not interchangeable. No REA/client setup or configuration was changed.

## Integration disposition and scope

1. Integrate only CR-2's bounded `inspect_artifact` entry and its matching Evidence model map token; rerun Command A on the landing revision. Until then, C1's coverage after-state is **UNVERIFIABLE**.
2. Retain the measured C2 values; preserve the ASAR root boundary and the dated status of the 1,556 pacman snapshot.
3. Preserve C3's provider-level `available:true`, qualify targetless per-tool readiness as `target_required`, and leave active-Kimi status **UNVERIFIABLE**.

Only this VZ-2 verdict artifact was written. No corpus, map, PROVINCE, SKILL, SCORECARD, LOG, gate source, custody path, or peer artifact was changed; Git history was not mutated. The pre-existing `.ufo/waves/arc2-loop1-round10/C3.md` modification was left untouched. Scratch used for the independent rerun was under `/var/tmp` and removed.
