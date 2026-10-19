# CN-3 — arc3-loop1-round11 independent reconciliation

I re-derived the numeric controls and operational measurements below; peer artifacts were used to compare candidate choices and scope, not as evidence for my measurements. This seat writes only this verdict. Git history, corpus, coverage map, PROVINCE, SCORECARD, SKILL, LOG, gate source, and custody paths were not changed.

## Revision controls and gate identity

The frozen records revision is `e746ca79e2dbb3cb41436d612f448e81d2c6e585`; the comparison work revision is `9c1d1fef5595b55d65764626249f164e6816473a`. I re-ran Command A from `SCORECARD.md:88-124` against both immutable trees:

```json
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"e746ca79e2dbb3cb41436d612f448e81d2c6e585","rule_blocks":16}
{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"9c1d1fef5595b55d65764626249f164e6816473a","rule_blocks":16}
```

Neither revision contains a new C1 entry/token, so the expected 90/90 post-integration count remains **UNVERIFIABLE**.

I also ran `python3 .ufo/gates/c1-census-v10.py` at the worktree, whose gate source matches records HEAD. It returned `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`, with 14 G21 frontier rows asserted and `errors: []`; pointer assertions included `~/.kimi-code/config.toml:4126` as `current-ok (pins 6.7.0)` (`PROVINCE.md:18`).

The gate hash difference reported in peer evidence is revision-scoped, not unexplained drift: `git show HEAD:.ufo/gates/c1-census-v10.py` and the worktree both hash to `b325a6caddafb9e209f292dec873dec582a3f7a244d135e4f25205907cec9573`; the immutable `9c1d1fe` version hashes to `d6b4deaa5973d3a29260b0e325620d87a3cc59464771688f97cb1c62d138fc80`. `git diff 9c1d1fe e746ca79 -- .ufo/gates/c1-census-v10.py` shows one change at line 273: the last SCORECARD dated-scope range ends at line 1975 rather than 1924. That one-line scope extension explains the different whole-file hashes.

## C1 — one third-verb-family Evidence-ID Unknown

**REPRODUCED, narrowly — `inspect_artifact` behavior on the tested REA 6.7.0 calls. UNVERIFIABLE — corpus/map landing and the 90/90 after-state.**

All eight C1 reports are present. Their choices are alternatives for the single frozen Unknown (`claims-frozen.md:15-28`), not additive closures:

- `EX-2`, `EX-4`, `EX-5`, and `CR-2` choose `inspect_artifact`.
- `EX-1`, `EX-3`, and `CR-1` choose `inspect_go_binary`.
- `EX-6` proposes a separate Vyper Cancun blob-primitives case.

The convergence verdicts differ: VZ-1 prefers EX-5; VZ-3 and CN-1 prefer CR-2; VZ-4 and CN-4 prefer a Go-binary draft. CN-1 independently reproduced the same `/usr/bin/jq` repeat ID and nested inventory ID; its alternate-copy outer ID differs from mine because it used a different scratch path, consistent with the observed path sensitivity. For one C1 entry I recommend **CR-2 only**: `inspect_artifact` is the modal family among the eight reports, and CR-2 is directly aligned with my independent `/usr/bin/jq` measurement. The other drafts remain alternatives; do not co-land multiple entries or claim they close multiple Unknowns under this frozen C1.

I independently ran the cached REA 6.7.0 CLI's `inspect-artifact <path> --format json --full-output` twice on `/usr/bin/jq` and once on a byte-identical copy at `/var/tmp/kaidoku-arc3-r11-cr2-probe/copies/jq-copy`. The original was 30,800 bytes with SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`; the copy had the same size and digest. Recomputed IDs from the semantic projection matched the reported values:

```text
/usr/bin/jq repeat 1: ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca
/usr/bin/jq repeat 2: ev_f3b9e57f08ec6290e816552429d7e3ad1c45ef173561d6f85c9c7c0e4c06f7ca
same-byte copy:       ev_b3ebd1711ebc131bf0acc53e27b4a4d1e404a0c494d3baa0dc0ff76c5d61f88a
nested inventory ID:  ev_bd06f056ab62f7b324a05fa29829c230998a8bf5232ed843e4dafeee60f71435 (stable)
```

Changing only the top-level display fields preserved the outer ID; the path-bearing nested inventory result changed with the copy and the outer ID changed. The package semantic projection is at `dist/domain/evidence.js:159-183`; canonical digest code is at `dist/domain/canonicalDigest.js:8-25,60-76`. This reproduces the tested composition for this operation, artifact, package version, and successful call shape; it is not a universal rule for all REA IDs, verbs, versions, or failure records. The separate `inspect_go_binary` peer measurements on `/usr/bin/docker` are also reproducible but are evidence for a competing C1 choice, not another closure here.

**Disposition:** integrate one CR-2 corpus draft and its matching map token only if selected by the parent, then rerun Command A at that landing revision. Until then, retain 89/89 as the measured state and leave 90/90 **UNVERIFIABLE**.

## C2 — freshness receipt

**VERIFIED / REPRODUCED — Ghidra inventory; delta 0/0; NO-CHANGE.** This is the single C2 receipt I select. At `2026-10-19T19:23:17Z`, I read the installed `application.version` and independently counted immediate directories in `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features` and `.../Processors`:

```text
application.version=12.1.4
Features: count=34
Processors: count=39
```

Against `PROVINCE.md:46`, the deltas are `34−34=0` and `39−39=0`. This verifies the installed immediate-directory counts, not module loadability or REA-session availability. Retain the recorded values; no erratum is motivated.

I also re-counted the alternative receipts, but they are not extra C2 claims: `/var/cache/pacman/pkg` contained 1,350 `.pkg.tar.zst` files and 1,350 `.sig` sidecars, with zero missing/orphaned sidecars (delta `+0` to the current 1,350 and `−206` versus the dated 1,556 snapshot at `PROVINCE.md:50`). The ASAR count was 12 in the readable roots; a broader walk reported `find: ‘/opt/containerd’: Permission denied`, so it is not a host-wide completeness result.

## C3 — provider capability versus targetless readiness

**REPRODUCED at provider-capability scope; DISCREPANCY if the bare value is read as targetless per-tool readiness; UNVERIFIABLE for the active Kimi session.**

`rea` was absent from `PATH`; I used the cached `rea-agents@6.7.0` package at `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs`. `capabilities --format json` reported provider group `rea-artifact-graph`, operations `extract_artifact` and `inspect_artifact`, `available:true`, `reason:null`, `open:false`. In a separately launched local stdio server, I called `binary_session {}`; it reported package 6.7.0, 207 tools, `open:false`, and `cleanup_pending:false`. The group remained `available:true`, while both individual entries were `available:false`, `reason:"target_required"`, remediation `Call open_binary with a supported local target.` No target was opened and no artifact operation was called.

Thus the provider-level value recorded at `PROVINCE.md:50` is freshly reproduced. It does not establish that either operation is callable without a target. This matches the scope distinction in `PL-1.md:18-24` and `RV-6.md:17-21`; a targetless `available:true` per-tool reading would be misleading. `rea doctor --json` exited 1 and reported `live_server.state:"unknown"` and missing Kimi registration at `/home/vgpnk/.kimi-code/mcp.json`. The direct stdio call was not the attached Kimi session, so active-client availability remains **UNVERIFIABLE**; no registration/configuration was changed.

## Integration disposition

1. For C1, prefer one `inspect_artifact` draft (CR-2) and its matching token over the competing Go or Vyper choices; require Command A on the landing revision to show 90 files / 90 mapped and empty missing/dangling sets. That after-state has not been measured.
2. For C2, retain the Ghidra 34/39 values; the measured deltas are zero.
3. For C3, retain `available:true` only as a provider-capability result; record per-tool `target_required` in the targetless session and leave the active Kimi connection unknown.

No corpus, map, configuration, gate, custody path, peer verdict, or Git history was modified. Scratch was confined to `/var/tmp` as required.