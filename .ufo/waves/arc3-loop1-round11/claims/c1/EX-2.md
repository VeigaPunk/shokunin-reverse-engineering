<!-- DRAFT for parent integration only. Proposed destination: corpus/knowledge/2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain.md. Proposed coverage-map token: `2026-10-19-arc3-r11-inspect-artifact-evidence-id-domain`, appended to the Archives & packages row in `corpus/README.md`. No corpus or map edit was made by this seat. -->

# Draft — `inspect_artifact` Evidence-ID domain in REA 6.7.0

source: `.ufo/waves/arc3-loop1-round11/claims/c1/EX-2/evidence/` (`fixtures/{base.zip,copy.zip}`; `probe-{base1,base2,copy}.json`; `path-diff.txt`; `recompute-evidence-ids.py`; `id-recompute.json`; `fixture-sha256.txt`; `runtime-and-source-identity.txt`; `command-A-{head,work}.json`). The package source identity and hashes are recorded in `runtime-and-source-identity.txt`.

verified-at: 2026-10-19

recheck: from the lane root, run `TMPDIR=/var/tmp/kaidoku-ex2-r11 node /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs inspect-artifact "$PWD/.ufo/waves/arc3-loop1-round11/claims/c1/EX-2/evidence/fixtures/base.zip" --format json --full-output` twice at the same path, then repeat for `fixtures/copy.zip`; both carriers are byte-identical (SHA-256 `9a3b227621e9031246816e003ea720a247ac925188d503dea157682d140a331a`). Run `python3 .ufo/waves/arc3-loop1-round11/claims/c1/EX-2/evidence/recompute-evidence-ids.py` to independently recompute the outer and nested IDs and the identity controls. The CLI output was captured with its temporary directory under `/var/tmp`, not `/tmp`.

## Result

The C1 Unknown was the `ev_` Evidence-ID domain for a third verb family. This draft closes it narrowly for `inspect_artifact` in the cached `rea-agents@6.7.0` package on a one-member synthetic ZIP. It does not claim a universal formula for other operations or releases.

In this package, an Evidence ID is `ev_` plus lowercase SHA-256 of UTF-8 compact canonical JSON for a semantic projection. The projection uses `subject: null` or `{digest, format, architecture}` and then includes `provider`, `analysis_profile`, `predicate_type`, `operation`, `parameters`, `raw_result`, `normalized_result`, `confidence`, `authority`, `environment`, `limitations`, `relationship_coverage`, `locations`, and `evidence_links`; the Evidence ID itself is excluded. This is visible in the installed `dist/domain/evidence.js:159-183`; `dist/domain/canonicalDigest.js:8-25,63-75` defines the SHA-256 and canonical object-key ordering. Package/source hashes are pinned in the evidence directory.

For `inspect_artifact`, the outer record is path-sensitive in this measured case even though the top-level subject's display `name` and `local_path` are not hashed directly. Its `normalized_result` contains a path-varying `inspection_id` and the nested `inventory_artifact` Evidence's subject `name`/`local_path`; those fields are part of the outer semantic projection. The nested inventory Evidence ID itself stays stable because its own semantic projection excludes its subject display fields.

## First-hand observations

- `VERIFIED` — `inspect-artifact <fixture.zip> --format json --full-output` completed through REA 6.7.0's CLI (`node v26.12.0`); the outer operation is `inspect_artifact`, provider `rea-artifact-graph` v1, with one completed `inventory_artifact` substep. Full outputs: `probe-base1.json:1`, `probe-base2.json:1`, `probe-copy.json:1`. This is static inventory; the tool reports ZIP central-directory scope and no artifact execution.
- `REPRODUCED` — two calls at the same absolute `base.zip` path returned outer `ev_1bfefcf56e0a0b7176532511262d6cd25663fd53ef2292b0f7c9b6a3c8fcfc88`; the same bytes at `copy.zip` returned outer `ev_15da6d228d47e0d3df7b05047ee1092023467ed4118ffb79037fc67187f490ef`. Both fixture files independently hash to `9a3b227621e9031246816e003ea720a247ac925188d503dea157682d140a331a` (`fixture-sha256.txt:1-2`).
- `REPRODUCED` — independent `recompute-evidence-ids.py` matches all three outer IDs and all three nested `inventory_artifact` IDs. The nested ID is `ev_2c9b219a7cb9b7919500e2793bd93df9a3a309865976ad6e0303b6c152520f45` on both paths; a top-level-only subject name/path mutation preserves the outer ID; restoring the three path-varying output fields in the copy record reproduces the base outer ID (`id-recompute.json:1`). These controls distinguish the hashed nested result from the excluded top-level display fields.
- `VERIFIED` — the only observed record diffs are the outer ID, `normalized_result.inspection_id`, nested inventory Evidence subject name/path, and outer subject name/path (`path-diff.txt:1-6`). The inner Evidence ID remains unchanged. No path-only conclusion is generalized beyond this fixture and operation.
- `VERIFIED` — source-derived Command A at current HEAD `e746ca79e2dbb3cb41436d612f448e81d2c6e585` returned `knowledge_files:89`, `mapped:89`, `missing:[]`, `dangling:[]`; the work revision `9c1d1fe` independently returned the same values. Full JSON: `command-A-head.json:1` and `command-A-work.json:1`, using `SCORECARD.md:88-124`.
- `UNVERIFIABLE` — post-integration `90/90` Command A result. This seat only delivers the draft and proposed coverage-map token; it did not modify corpus files, so integration must rerun Command A at the landing revision.

## Scope and limitations

The target was a synthetic 155-byte ZIP containing one 35-byte text entry, not a production package. The input bytes and complete REA envelopes are retained in the evidence directory. The probe establishes the output/ID behavior for this exact fixture and REA 6.7.0 CLI route; it does not prove the live MCP tool is connected, generalize the hash formula to all verbs/releases, or inventory ZIP data outside the central directory. No runtime execution, network request, or package/configuration change was made.
