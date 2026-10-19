# Draft — `inspect_artifact` Evidence-ID domain (C1)

**Status:** draft for parent integration only. Proposed corpus destination: `corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md`. Proposed coverage-map token: `2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain`, appended to the **Evidence model** row. This seat did not edit `corpus/` or the map.

**Frozen claim:** C1 permits closing a third verb-family `ev_` ID-domain Unknown (`claims-frozen.md:18-25`). I selected the distinct `inspect_artifact` operation. This result is operation- and package-version-scoped; it is not a universal formula claim.

**Evidence:** full REA envelopes and source identities are under `claims/c1/EX-4/evidence/`. REA package version/root and source hashes, target identity, and retained-file hashes are in `evidence/identity.txt`.

**Recheck:** from the lane root, with scratch outside `/tmp`:

```bash
export TMPDIR=/var/tmp/kaidoku-arc3-r11-EX-4
node /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs inspect-artifact /usr/lib/signal-desktop/resources/app.asar --integrity-policy record-and-continue --format json --full-output
```

The same call was repeated at the same path and then run against a byte-identical copy at `/var/tmp/kaidoku-arc3-r11-EX-4/pathcopy/app.asar`, with its unpacked sidecar copied and checked by `diff -qr` (exit 0, no output). Recompute all three returned Evidence IDs with `node .ufo/waves/arc3-loop1-round11/claims/c1/EX-4/evidence/recompute-evidence-ids.mjs`.

## Result

`inspect_artifact`'s returned Evidence ID is `ev_` followed by lowercase SHA-256 over the installed package's canonical JSON semantic projection. The projection is defined at `dist/domain/evidence.js:159-183`; canonical hashing and recursively sorted object-key serialization are at `dist/domain/canonicalDigest.js:8-25,27-76`. The top-level `subject` projection includes `digest`, `format`, and `architecture`, but not its display `name` or `local_path`.

The `inspect_artifact` result has an important family-specific wrinkle: `dist/domain/artifactInspection.js:118-128` places the **complete nested `inventory_artifact` Evidence record** inside the parent result, and `:153-156` derives an `inspection_id` from that semantic result. `dist/application/DirectAnalysis.js:293-310` then uses this whole inspection result as the parent Evidence's `normalized_result`; `dist/artifacts/ArtifactProvider.js:230-255` shows how the nested inventory Evidence is made and returned. Consequently, the parent projection contains the nested Evidence's display `subject.local_path` (and the path-derived `inspection_id`) even though the parent's own top-level subject display fields are excluded.

## First-hand observations and verdicts

- **VERIFIED — target and package identity.** The target is `/usr/lib/signal-desktop/resources/app.asar`, SHA-256 `7cd804fa75f54da9890f65104092a36d120af42dd3b87e3843b9f2c4509fe0c4`, `38,465,187` bytes. The installed package reports version `6.7.0`; exact package/source hashes are in `evidence/identity.txt`.
- **VERIFIED — successful same-path result, with integrity caveat.** Default integrity policy first returned `artifact_integrity_mismatch` (`evidence/inspect-artifact-default-integrity-refusal.json`), so the successful calls explicitly used `record-and-continue`. Both returned `ok:true`, parent ID `ev_1bb34d565511c39b11c46492122ecceafb675b1c898059b579e46a1d557b367c`, and nested `inventory_artifact` ID `ev_fa8d54c1a61bcf5a73d2d0c223b6ef0442e7bc711873b2ff3f7e8dca16c871c4` (`evidence/inspect-artifact-signal-base.json` and `evidence/inspect-artifact-signal-repeat.json`). Each reported five retained observations, four integrity contradictions, one hypothesis, one unexplored branch, one next probe, zero omissions, and `complete-within-substeps`. The mismatched content is explicitly observed-untrusted; no integrity or safety endorsement is made.
- **REPRODUCED — same path.** The repeated call returned the same parent and nested IDs, and its `normalized_result` is JSON-identical to the first (`evidence/id-recompute-results.json`). `meta.duration` is outside the Evidence record and is not part of this comparison.
- **VERIFIED — path sensitivity in this parent-result class.** The same-byte copy has the same ASAR SHA-256 and the copied unpacked sidecar passed `diff -qr`; its nested inventory ID remains `ev_fa8d54c1a61bcf5a73d2d0c223b6ef0442e7bc711873b2ff3f7e8dca16c871c4`, but the parent ID changes to `ev_bece8b0735dbee3cdcac93cfcf88ff6e7dce6a8c7fcf26db78218de58cb34514` (`evidence/inspect-artifact-signal-pathcopy.json`). The independent recomputation matches each parent and nested ID. After normalizing only the nested `subject.local_path` and its derived `inspection_id`, the two parent semantic projections compare equal (`evidence/id-recompute-results.json`). This measures path sensitivity through the nested result, not through the parent's top-level subject projection.
- **VERIFIED — Command A pre-state.** Running the `SCORECARD.md:88-124` recipe against `e746ca7` returned `{"citation_resolved_rules":16,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":89,"mapped":89,"missing":[],"revision":"e746ca7","rule_blocks":16}`. At work revision `9c1d1fe` it independently returned the same counts (`evidence/command-A-e746ca7.json`, `evidence/command-A-9c1d1fe.json`).
- **UNVERIFIABLE — post-integration map count.** This is a draft only; no corpus entry or map token was landed, so no after-count is claimed. The parent integrator must co-land the entry and token and rerun Command A at the landing revision.

## Scope and limitations

This derives the `inspect_artifact` parent Evidence ID domain on cached `rea-agents@6.7.0`, for one Signal ASAR, one explicit integrity policy, a same-path repeat, and a same-byte alternate-path copy. The result does not establish behavior for other artifact formats, integrity policies, package releases, invocation shapes, or REA verb families. Inventory is complete only within its reported substep; the four integrity contradictions remain observed-untrusted. The target was statically inspected, not executed; no runtime, chain, or safety claim is made.
