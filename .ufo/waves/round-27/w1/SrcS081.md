# Round 27 — SrcS081: S081 SOURCES row for the installed rea-agents 6.7.0 evidence-ID projection

Seat: SrcS081 (scribe). Lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin, base cd32264f7ee356a9c0f48bd8e3fcdac222db22a0.
Read-only on the lane; the only file written inside the lane is this report. Scratch work lives under /fast/scratch/hyaku/kaidoku-r27/seats/SrcS081/.
This seat answers routed defect 1 of corpus/lessons/round-26-verifier-spotcheck.md:197: the 6.7.0 installed-package code read for the pin diff
had no SOURCES row, because the round-26 Gate rejected it as "already row S037's family" (corpus/lessons/round-26.md:37). It opens that code and
the npm 6.7.0 tarball, records digests, shows the installed tree is byte-identical to the tarball, and drafts the S081 row, the Gate lines, the
search-log sentence and the family decision. It edits no lane file; the L1 integrates and commits.

## Commands, exit codes, UTC times

| # | command | exit | UTC | observed |
|---|---|---|---|---|
| 1 | `sha256sum dist/domain/evidence.js dist/domain/canonicalDigest.js package.json` in /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents | 0 | 2026-10-22T14:54:35Z | three digests, below |
| 2 | `curl -fsSL -o rea-agents-6.7.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz` | 0 | 2026-10-22T14:54:47Z | 6276963 bytes |
| 3 | `sha256sum` and `sha1sum rea-agents-6.7.0.tgz` | 0 | 2026-10-22T14:54:47Z | sha256 `20958a66…1f90`, sha1 `11f23ba3…3708` |
| 4 | `tar -xzf rea-agents-6.7.0.tgz -C unpack` | 0 | 2026-10-22T14:54:47Z | `unpack/package/` with `dist/`, `package.json` |
| 5 | `curl -fsSL -o registry-6.7.0.json https://registry.npmjs.org/rea-agents/6.7.0` | 0 | 2026-10-22T14:54:47Z | version document, sha256 `ae3429d5…c236` |
| 6 | `diff -rq unpack/package/dist /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist` | 0 | 2026-10-22T14:55:38Z | no output: the two trees are identical |
| 7 | `diff -q unpack/package/package.json /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json` | 0 | 2026-10-22T14:55:38Z | no output: identical |
| 8 | `grep -n "relationship_coverage: evidence.relationship_coverage" …/dist/domain/evidence.js`; `grep -n "const computeEvidenceId" …/dist/domain/evidence.js` | 0 | 2026-10-22T14:55:38Z | lines 178 and 183 |
| 9 | `grep -n "export const digestCanonicalValue" …/dist/domain/canonicalDigest.js`; `grep -n '"version"' …/package.json` | 0 | 2026-10-22T14:55:38Z | lines 8 and 4 |
| 10 | `grep -rn "relationship_coverage" /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/ \| wc -l` (and the 6.5.0 tree) | 0 | 2026-10-22T14:55:48Z | 74 hits in 25 files (6.5.0 tree: 73 hits) |
| 11 | `git show cd32264f…:corpus/SOURCES.md \| grep -cE '^\| S[0-9]{3} \|'`; `… \| grep -c S081` | 0 | 2026-10-22T14:55:20Z | 80 rows, 0 hits for S081 |

## Digests and quote line numbers

| file | sha256 | quote used, line |
|---|---|---|
| installed 6.7.0 `dist/domain/evidence.js` | `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb` | `relationship_coverage: evidence.relationship_coverage,` at `:178`; id rule at `:183` |
| tarball member `package/dist/domain/evidence.js` | `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb` | id rule at `:183` |
| installed 6.7.0 `dist/domain/canonicalDigest.js` | `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9` | `export const digestCanonicalValue = (value, context = "Comparison") => {` at `:8` |
| tarball member `package/dist/domain/canonicalDigest.js` | `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9` | same bytes as the installed copy |
| installed 6.7.0 `package.json` | `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570` | `"version": "6.7.0",` at `:4` |
| tarball member `package/package.json` | `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570` | same bytes as the installed copy |
| npm tarball `rea-agents-6.7.0.tgz` | `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90` (sha1 `11f23ba377303a5c28b3162180cf2bf3f3643708`) | id rule in member `:183` |
| npm registry version document `registry-6.7.0.json` | `ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236` | `"shasum":"11f23ba377303a5c28b3162180cf2bf3f3643708"`, `"integrity":"sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw=="` |

The 6.7.0 `canonicalDigest.js` digest equals the 6.5.0 file digest recorded in S079 (`f46d6bd4…81d9`); observation, both files hash to it. The
6.7.0 projection object opens at `dist/domain/evidence.js:159`, its last field `evidence_links` is at `:180`; the 6.5.0 counterpart opens at
`:156` and projects `relationship_coverage` only when it is not null (`:175-177`).

## Drafts (verbatim)

### 1. S081 row

| S081 | Evidence-ID minting and projection source in the rea-agents 6.7.0 package tarball https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz (members `package/dist/...`), read from the installed copy at `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/`, whose `dist/` tree is file-for-file identical to that tarball (`diff -rq` empty, exit 0) — package root `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/` (`domain/evidence.js`, `domain/canonicalDigest.js`) and `package.json` | code | A | How rea-agents@6.7.0 mints an `ev_` Evidence identifier and projects it into native-reader output: the hashed semantic projection and the id rule that R27-C2 compares across the 6.5.0 and 6.7.0 pins; not the per-verb identity outcomes this round measured | Package `6.7.0`; `domain/evidence.js:159-181` hashed field list, `:178` always-projected `relationship_coverage`, `:183` id rule, sha256 `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb`; `domain/canonicalDigest.js:8-25` sha256 `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9`; `package.json:4` sha256 `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570`; tarball sha256 `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90`, sha1 `11f23ba377303a5c28b3162180cf2bf3f3643708`; opened 2026-10-22; supersedes the round-26 rejection of this source at `corpus/lessons/round-26.md:37`, reported at `corpus/lessons/round-26-verifier-spotcheck.md:165` and `:197` | At 6.7.0 the hashed semantic projection always includes `relationship_coverage`, so one saved envelope can carry an identifier the 6.5.0 rule (S079, whose projection adds that field only when it is not null) would not produce; the subject still contributes only digest, format and architecture, never its path, so the two pins are separable by the stored id. | mined | 2026-10-22 | on-release | tools/round-27/xpin-attribute.mjs, corpus/lessons/round-27.md |

Shape check with the checker's own parser (`re.match(r"^\| (S\d{3}) \|", line)` then split on `|`): 11 cells; cell 1 contains
`a1722018f28f9df2`; cell 7 `mined`; cell 8 `2026-10-22`; no cell holds a pipe. Observation from that run, exit 0.

### 2. Gate lines for corpus/lessons/round-27.md

| row | source and access date | sha256 of the bytes read | located quote (at most 25 words) | section |
|---|---|---|---|---|
| S081 | Installed `rea-agents@6.7.0` package source — `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js`; opened 2026-10-22 | `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb` | `relationship_coverage: evidence.relationship_coverage,` | `dist/domain/evidence.js:178` |
| S081 | Installed `rea-agents@6.7.0` package source — `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js`; opened 2026-10-22 | `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb` | `const computeEvidenceId = (evidence) => \`ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}\`;` | `dist/domain/evidence.js:183` |
| S081 | Installed `rea-agents@6.7.0` package source — `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/canonicalDigest.js`; opened 2026-10-22 | `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9` | `export const digestCanonicalValue = (value, context = "Comparison") => {` | `dist/domain/canonicalDigest.js:8` |
| S081 | Installed `rea-agents@6.7.0` package source — `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/package.json`; opened 2026-10-22 | `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570` | `"version": "6.7.0",` | `package.json:4` |
| S081 | npm registry tarball `https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz`, member `package/dist/domain/evidence.js` unpacked under the seat directory; opened 2026-10-22 | tarball `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90` (sha1 `11f23ba377303a5c28b3162180cf2bf3f3643708`) | `const computeEvidenceId = (evidence) => \`ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}\`;` | `package/dist/domain/evidence.js:183` |

Each quote is contiguous in its file and under 25 words (3, 10, 9, 3, 10 words).

### 3. Search-log sentence

- 2026-10-22 round 27 — Question: which installed code decides the evidence-ID projection at the 6.7.0 pin, and is the installed copy the registry's own published tarball. Where searched: the installed rea-agents 6.7.0 package tree `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/`, the npm registry tarball `https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz` unpacked into the seat directory, and the npm registry version document `https://registry.npmjs.org/rea-agents/6.7.0`. Identified 3 candidate sources (installed code tree, registry tarball, registry version document), screened 3, included 1 (S081, which covers the installed tree and its byte-identical tarball as one family), excluded 1 (the registry version document, already row S037's dataset family). Consumer-code search run for the exclusion: `grep -rn "relationship_coverage" /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/` returned 74 hits in 25 files (the 6.5.0 tree returned 73), so the projection rule lives in the installed package code, not in the registry record.

### 4. Family decision

S081 is a code row for the 6.7.0 package's own code; S037 is a dataset row for the npm registry's publish record of the same version, and S037's scope cell says "not the package's runtime behaviour". The round-26 Gate rejected the 6.7.0 installed code because it "is already row S037's family" (`corpus/lessons/round-26.md:37`); the outside spot-check disagreed (`corpus/lessons/round-26-verifier-spotcheck.md:165`, routed defect 1 at `:197`), because the round-26 Gate's own split is installed package = one family, registry = another. S081 is therefore the 6.7.0 analogue of S079, the 6.5.0 code row: same role, same kind (code), same tier (A), one row per installed pin. The two code rows differ in a measured way, which is why one row per pin is needed: at 6.5.0 the projection adds `relationship_coverage` only when it is not null (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/evidence.js:175-177`), while at 6.7.0 it always adds it (`/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/evidence.js:178`), so a stored `ev_` identifier is separable by pin. The registry record cannot supply that rule: it carries publish identity only. QUALITY row 36 (`corpus/QUALITY.md:46`) is satisfied in both directions: the reversing lesson (round 27) must name the rejected decision by path and line and name S081, and S081's anchor cell above names the rejected decision by path and line.

## Findings

1. Observation: the 6.7.0 installed `dist/` is byte-identical to the npm 6.7.0 tarball, so the installed copy is the registry's published
   artefact and one code row can cite both.
2. Observation: the 6.7.0 projection always includes `relationship_coverage` (`:178`), while the 6.5.0 projection adds that field only when
   it is not null (`:175-177`). This code difference is what the R27-C2 attribution tool measures, so it belongs in a code row.
3. Inference from 1 and 2: a saved envelope's stored `ev_` id is separable by pin, so S081 is the source that licenses the R27-C2
   attribution claim.
4. Observation: S081 does not exist at the lane base (80 rows, ids up to S080), so it is a new row and the C2 checker's "new since the base"
   clause applies.
5. Unknown: whether the L1 also cites S081 in the round-27 SCORECARD and LOG rows that QUALITY row 36 asks for when an outside spot-check
   disagrees with a lane decision. This seat does not own those files.

## Out of scope and not done

- No lane file was edited: SOURCES.md, corpus/lessons/round-27.md, SCORECARD.md, LOG.md, tools/ and .ufo/waves/round-27/claims.json are
  untouched. Only this report was written inside the lane.
- No REA call was made and no MCP device was used; this seat reads package code and the npm registry only, so the carrier and REA CLI
  restrictions do not apply.
- No git or jj write was performed; the only git use was a read-only `git show` of a blob.
- The 6.7.0 attribution tool `tools/round-27/xpin-attribute.mjs` did not exist in the lane when this seat ran (path not found); the row names
  it in `used-by` because the frozen R27-C2 claim and the checker require that naming, not because this seat observed the tool run.
- No tool was installed or upgraded; `curl`, `tar`, `diff`, `sha256sum`, `sha1sum`, `grep` and `python3` were already present and sufficient.

## Artifacts

| path | sha256 |
|---|---|
| /fast/scratch/hyaku/kaidoku-r27/seats/SrcS081/draft.md | `0906101c88b7635e7773e4424fc993c900d55fcbfd18b603b2733b24baa3a7b8` |
| /fast/scratch/hyaku/kaidoku-r27/seats/SrcS081/rea-agents-6.7.0.tgz | `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90` |
| /fast/scratch/hyaku/kaidoku-r27/seats/SrcS081/registry-6.7.0.json | `ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236` |
| /fast/scratch/hyaku/kaidoku-r27/seats/SrcS081/unpack/package/ | unpacked tarball tree, diffed against the installed `dist/` (exit 0) |
