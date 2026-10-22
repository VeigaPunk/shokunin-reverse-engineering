# R26 w1 — Source row S079: rea-agents@6.5.0 Evidence-ID minting code

Seat: KaidokuR26.SourceRowEvidence. Date: 2026-10-22 (UTC). Lane read-only: no
lane file was edited; this report is the only file written in the lane.

## Status of the id

`grep -c "S079" corpus/SOURCES.md` → `0` (2026-10-22, run from
/home/vgpnk/Projects/shokunin/kaidoku-shokunin): S079 is unused. The registry's
last row is S078.

## What was opened (read-only, installed package)

Package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/`;
`package.json` line with `"version": "6.5.0"`.

| file (absolute) | role | sha256 (2026-10-22) |
|---|---|---|
| /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/evidence.js | mints the id (`semanticProjection`, `computeEvidenceId`, `createEvidence`) | f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff |
| /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/canonicalDigest.js | SHA-256 over canonical JSON | f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9 |
| /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/application/DirectAnalysis.js | generic CLI native-verb call site | 09d2b2225dd9817674f3a454d33447a6a917e82441f2081c6553511e2dc72617 |
| /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/application/binaryDiagnostics/BinaryLayoutService.js | `inspect_binary_layout` call site | b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4 |
| /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/analysisView/analysisView.js | projects an id into a view | 2685fc2c0f6dda136b9bc004ab3af30d4272b850b1a8d026ad14b2e22ef68363 |
| /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/analysisView/binaryLayoutView.js | projects parent id/digest | 5bd86489988b6cf4cb59bd6085805accdd83277870578426baebff687ff7b070 |

## The row (paste-ready, one table row)

| S079 | Installed `rea-agents@6.5.0` Evidence-ID minting and projection source — package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/` (`domain/evidence.js`, `domain/canonicalDigest.js`, `application/DirectAnalysis.js`, `application/binaryDiagnostics/BinaryLayoutService.js`, `domain/analysisView/analysisView.js`, `domain/analysisView/binaryLayoutView.js`) | code | A | How rea-agents@6.5.0 mints an `ev_` Evidence identifier and projects it into native-reader output: the hashed semantic projection and the call sites that feed it; not the per-verb identity outcomes this round measured | Package `6.5.0`; `domain/evidence.js:156-180` hashed field list, `:181-182` id rule, `:234-240` mint, sha256 `f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff`; `domain/canonicalDigest.js:8-25` sha256 `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9`; `application/DirectAnalysis.js:72-82` sha256 `09d2b2225dd9817674f3a454d33447a6a917e82441f2081c6553511e2dc72617`; `application/binaryDiagnostics/BinaryLayoutService.js:54-68` sha256 `b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4`; `domain/analysisView/analysisView.js:504,556` sha256 `2685fc2c0f6dda136b9bc004ab3af30d4272b850b1a8d026ad14b2e22ef68363`; `domain/analysisView/binaryLayoutView.js:71-73` sha256 `5bd86489988b6cf4cb59bd6085805accdd83277870578426baebff687ff7b070`; opened 2026-10-22 | An `ev_` identifier is `ev_` plus the SHA-256 of a canonical-JSON projection of the record's semantic fields: the subject contributes only digest, format and architecture, never its path, while parameters, results and locations are hashed, so any path carried in those fields changes the identifier. | mined | 2026-10-22 | on-release | corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md |

11 cells, no `|` inside any cell. `status` sits in column 9 (`mined`), `used-by`
in column 12, so the frozen census awk (NF=13) parses it.

## The lesson `## Gate` text (paste-ready)

For `corpus/lessons/round-26.md`, in the new-rows table:

| row | source and access date | sha256 of the bytes read | located quote (at most 25 words) | section |
|---|---|---|---|---|
| S079 | Installed `rea-agents@6.5.0` package source — `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/evidence.js`, with `dist/domain/canonicalDigest.js`, `dist/application/DirectAnalysis.js`, `dist/application/binaryDiagnostics/BinaryLayoutService.js`, `dist/domain/analysisView/analysisView.js`, `dist/domain/analysisView/binaryLayoutView.js`; opened 2026-10-22 | evidence.js `f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff`; canonicalDigest.js `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9`; DirectAnalysis.js `09d2b2225dd9817674f3a454d33447a6a917e82441f2081c6553511e2dc72617`; BinaryLayoutService.js `b7c249a7ba2bdc88287961c4259f0cb41d9e00b7270b56dac618dfc5e7cac2f4`; analysisView.js `2685fc2c0f6dda136b9bc004ab3af30d4272b850b1a8d026ad14b2e22ef68363`; binaryLayoutView.js `5bd86489988b6cf4cb59bd6085805accdd83277870578426baebff687ff7b070` | “const computeEvidenceId = (evidence) => `ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}`;” — `dist/domain/evidence.js:182`. Supporting: “digest: evidence.subject.digest, format: evidence.subject.format, architecture: evidence.subject.architecture” — `dist/domain/evidence.js:160-162` | Evidence-ID minting and projection; the id is a digest over the semantic projection, the subject's path is excluded from it, and parameters, results and locations are inside it |

Gate note to accompany the table:

> S079 is a new row; no older row's `status`, `recheck` or `used-by` cell changes.
> It grounds the identity mechanism of the installed 6.5.0 package, not the
> per-verb verdicts: the round-26 C1 table and its counter own those.

## Commands that produced the sha256 and the quote

Run 2026-10-22 from /home/vgpnk/Projects/shokunin/kaidoku-shokunin; exit 0.

```
sha256sum /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/evidence.js \
          /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/canonicalDigest.js \
          /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/application/DirectAnalysis.js \
          /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/application/binaryDiagnostics/BinaryLayoutService.js \
          /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/analysisView/analysisView.js \
          /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/analysisView/binaryLayoutView.js
```

```
grep -n "" .../dist/domain/evidence.js | sed -n '156,163p;181,182p;234,240p;281,282p'
grep -n "" .../dist/application/DirectAnalysis.js | sed -n '72,82p'
grep -n "" .../dist/application/binaryDiagnostics/BinaryLayoutService.js | sed -n '54,68p'
grep -n "" .../dist/domain/canonicalDigest.js | sed -n '2,8p'
grep -n "parentDigest" .../dist/domain/analysisView/analysisView.js
grep -n "" .../dist/domain/analysisView/binaryLayoutView.js | sed -n '71,73p'
grep -c "S079" corpus/SOURCES.md
```

Full receipt with the cited lines and every hash:
`/fast/scratch/hyaku/kaidoku-r26/seats/SourceRowEvidence/receipt.txt`,
sha256 `a19fda9736f8391a10200e8f48b9c3795fbe778b3b34ddae14362083852eb834`.

## Findings (labels per the evidence contract)

- observation — the id is `ev_` + SHA-256 of `semanticProjection(evidence)`
  hashed by `digestCanonicalValue` (canonical JSON, RFC 8785 key order):
  `dist/domain/evidence.js:156-182`, `dist/domain/canonicalDigest.js:8-25`.
- observation — the hashed field list is subject(digest, format, architecture),
  provider, analysis_profile, predicate_type, operation, parameters, raw_result,
  normalized_result, confidence, authority, environment, limitations,
  relationship_coverage, locations, evidence_links
  (`dist/domain/evidence.js:156-180`). The subject's `name` and `local_path` are
  not in it.
- observation — the subject's path can still reach the hash through other
  fields: `inspect_binary_layout` passes `parameters: input.data`,
  `result: value` (which carries `artifact.path`) and
  `locations: [{ kind: "artifact-path", path: value.artifact.path }]`
  (`dist/application/binaryDiagnostics/BinaryLayoutService.js:54-68`).
- observation — the generic CLI native path passes `parameters: arguments_`,
  `result`, `rawResult` and `locations`
  (`dist/application/DirectAnalysis.js:72-82`).
- observation — a minted id is re-checked on parse: `parseEvidence` rejects a
  record whose recomputed id differs (`dist/domain/evidence.js:133-142,183-193`).
- observation — views project the id as `parent_evidence_id` and
  `parent_digest` (`dist/domain/analysisView/analysisView.js:504,556`,
  `dist/domain/analysisView/binaryLayoutView.js:71-73`).
- inference — therefore two runs over byte-identical files at different paths
  need not share an id, and equal ids would be evidence that the path did not
  reach the hashed fields; whether it does for each of the eight frozen verbs is
  the C1 table's measurement, not this row's claim.
- unknown — whether any single verb's provider result embeds the path; that was
  not measured here.

## Out of scope / not done

- No REA run was performed: this seat's deliverable is a source row, and REA
  calls are bound to the C1 counter's argv and seat scratch.
- No lane file was edited (`corpus/SOURCES.md`, `corpus/`, `tools/` untouched).
- No git or jj write was performed; only read-only greps and `sha256sum`.
- No tool was installed or upgraded.

## Dependency for the L1 integrator

- `used-by` names `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`,
  which does not exist in the lane yet (checked 2026-10-22). The frozen census
  check "mined rows whose used-by paths do not exist" will flag S079 until the
  knowledge entry lands; the row is `mined` because that entry is the citing
  path this round produces.
