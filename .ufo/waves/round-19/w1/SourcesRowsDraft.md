# SourcesRowsDraft — kaidoku round 19, seat KaidokuR19.SourcesRowsDraft

Role: leaf, read-only advisory draft. Lane files untouched; no subagents; no REA/Ghidra run; no carrier executed.
Access date for every fetch: 2026-10-20 (`date -u` → 2026-10-20T18:37:08Z).
Scratch: `/tmp/kr19-SourcesRowsDraft-fetch/` (not in lane).

## Behavior

Fetched both sources, verified their digests and cross-checks, drafted two SOURCES rows (S037 npm, S038 go.dev) and a Gate quote table. The two rows pass the CORPUS census checks when appended to a copy of `corpus/SOURCES.md` (see Checks). Nothing was written into the lane except this report.

## Gates

Census on a temp copy (`/tmp/kr19-SourcesRowsDraft-fetch/SOURCES.final.md` = lane `corpus/SOURCES.md` + the two draft rows), commands as in CORPUS.md §SOURCES census:

```
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' SOURCES.final.md          -> 38   (baseline 36, lane)
$ awk ... NF!=13 ... SOURCES.final.md                                         -> 0
$ awk ... uniq -d ... (dup ids)                                               -> (empty)
$ awk ... enum/tier-inflation ...                                             -> (empty)
$ awk ... mined rows with missing used-by paths ...                           -> (empty)
new-row field count (awk NF)                                                  -> 13, 13
tier histogram  A=33 B=4 C=1 ; status histogram  mined=34 queued=2 rejected=2
```

Lane census baseline (read-only, `awk ... NF!=13 corpus/SOURCES.md`) -> `malformed_baseline=0`.

## Observations (observation unless marked inference)

1. npm version doc (`curl -fsSL https://registry.npmjs.org/rea-agents/6.7.0`, body sha256 `ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236`; single-line JSON): `"version":"6.7.0"`, `dist.integrity` `sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==`, `dist.shasum` `11f23ba377303a5c28b3162180cf2bf3f3643708`, `dist.fileCount` 1775, `dist.unpackedSize` 28575703, `engines.node` `^22.19.0 || ^24.11.0 || >=26.0.0`, `_npmUser.trustedPublisher.id` `github`.
2. Tarball re-fetch (`curl -fsSL -o rea-agents-6.7.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz`, 6276963 bytes): `sha512sum` `ca1231da…e43a117`; base64 of that sha512 equals the registry `dist.integrity` (computed with node `crypto`); sha1 equals `dist.shasum` `11f23ba3…3643708`. Match on both.
3. Packument (`curl -fsSL https://registry.npmjs.org/rea-agents`, 327312 bytes, sha256 not recorded): `jq -c '."dist-tags"'` → `{"latest":"6.7.0"}`; `jq -c '.time["6.7.0"]'` → `"2026-10-18T08:12:05.640Z"`; 33 versions. `6.7.0` is the latest tag at fetch.
4. Provenance (`curl -fsSL https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.7.0`; predicate `https://slsa.dev/provenance/v1`; DSSE payload base64-decoded with `jq`): `subject[0].digest.sha512` equals the tarball sha512 above; `externalParameters.workflow` = `{"ref":"refs/heads/release/6.7.0","repository":"https://github.com/morluto/rea","path":".github/workflows/release.yml"}`; `resolvedDependencies[0]` = `{"uri":"git+https://github.com/morluto/rea@refs/heads/release/6.7.0","digest":{"gitCommit":"27dc42d10249f0410904a75c0997842eb03b931c"}}`; `runDetails.metadata.invocationId` `https://github.com/morluto/rea/actions/runs/39108764422/attempts/1`.
5. go.dev JSON (`curl -fsSL -o go-dl.json 'https://go.dev/dl/?mode=json&include=all'`, 2256879 bytes, sha256 `6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950`; time-varying, top entry is go1.27.3): `go-dl.json:14514` `"version": "go1.25.0",`; `:14515` `"stable": true,`; `:14644` `"filename": "go1.25.0.linux-amd64.tar.gz",`; `:14648` `"sha256": "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613",`; `:14649` `"size": 59659213,`.
6. Official archive (`curl -fsSL -o go1.25.0.linux-amd64.tar.gz https://go.dev/dl/go1.25.0.linux-amd64.tar.gz`): `sha256sum` → `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613`; `stat -c %s` → 59659213. Matches observation 5.
7. Carrier identity (no execution; `tar -xzf` of nine members only into `/tmp/kr19-SourcesRowsDraft-fetch/gotree`, then `sha256sum` on both trees): the nine carrier files under `/home/vgpnk/.local/opt/go-1.25.0` (`bin/go`, `bin/gofmt`, `pkg/tool/linux_amd64/{asm,cgo,compile,cover,link,preprofile,vet}`) hash identically to the same members from the official archive. `bin/go` `b93cdfdbc72f1afc3f21498c80bf3d155a44a9b95e2d690c940511051574bc25`; `pkg/tool/linux_amd64/vet` `9b9d776e7569c910de714790a1b9bab1287b49fdc210973158f3076cee683bf7`. Note: the label I printed in that command said "10 carriers"; the set is nine files (the diff printed nothing, and the nine-line listings are what match).
8. Freshness (`jq -r '[.[] | select(.stable==true)][0].version' go-dl.json` → `go1.27.3`; `jq -r '.[] | select(.version=="go1.25.14") | .version'` → `go1.25.14`): go1.25.0 is a pinned revision, not the current 1.25 point release nor the current stable train. Scope of S038 is kept to the 1.25.0 archive.
9. Lane registry (`corpus/SOURCES.md`): rows S001–S036 present, so S037 and S038 are the next unused ids (`grep -nE '^\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`).

Installs/updates this round: none. Used pre-existing `curl`, `jq`, `node`, `npm`, `sha256sum`, `sha512sum`, `tar`, `stat`, `awk`.

## Draft

Rows (verbatim; insert after S036 in `corpus/SOURCES.md` Registry table):

```
| S037 | rea-agents 6.7.0 npm registry record — https://registry.npmjs.org/rea-agents/6.7.0 (tarball https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz; packument https://registry.npmjs.org/rea-agents) | dataset | A | Publish identity and integrity of rea-agents@6.7.0 as served by the npm registry, with its SLSA provenance source commit; not the package's runtime behaviour | Version document `dist.integrity`, `dist.shasum`, `dist.attestations`; packument `time["6.7.0"]`, `dist-tags.latest`; attestation `https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.7.0`, predicate `https://slsa.dev/provenance/v1`, `resolvedDependencies[0].digest.gitCommit` `27dc42d10249f0410904a75c0997842eb03b931c`; fetched 2026-10-20 | Pins the 6.7.0 tarball by its sha512 and release-workflow commit, so a client pin can be checked against the registry's own digest before any package code runs. | queued | 2026-10-20 | on-release | — |
| S038 | Go release list JSON, `https://go.dev/dl/?mode=json&include=all`, entry go1.25.0 linux-amd64 archive | dataset | A | The official go1.25.0 linux-amd64 archive digest and size, against which the installed 1.25.0 carrier binaries are matched; not the Go 1.26 or 1.27 release train | Endpoint JSON, version `go1.25.0` with `stable` true, file `go1.25.0.linux-amd64.tar.gz` sha256 `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613` size 59659213; fetched 2026-10-20; `curl -fsSL https://go.dev/dl/go1.25.0.linux-amd64.tar.gz` re-hashed to the same sha256 | Gives an independent digest for the toolchain: nine carrier binaries under `/home/vgpnk/.local/opt/go-1.25.0` hash identically to the same members extracted from that archive. | queued | 2026-10-20 | 180d | — |
```

Status and used-by note: both rows are `queued` with used-by `—`. A `mined` status needs a used-by path that exists (CORPUS census, `mined rows whose used-by paths do not exist`). L1 flips to `mined` with the knowledge paths when C2/C3 entries land, and logs old→new in the round lesson `## Gate`.

Gate quote table (URL · access date · ≤25-word contiguous quote · location):

| URL | access date | quote | location |
|---|---|---|---|
| https://registry.npmjs.org/rea-agents/6.7.0 | 2026-10-20 | `"integrity":"sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw=="` | version document, `dist.integrity` (single-line JSON; body sha256 ae3429d5…) |
| https://registry.npmjs.org/rea-agents/6.7.0 | 2026-10-20 | `"version":"6.7.0"` | version document, top-level `version` |
| https://registry.npmjs.org/rea-agents | 2026-10-20 | `"2026-10-18T08:12:05.640Z"` | packument, `.time["6.7.0"]` |
| https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.7.0 | 2026-10-20 | `"uri":"git+https://github.com/morluto/rea@refs/heads/release/6.7.0"` | decoded DSSE payload, `predicate.buildDefinition.resolvedDependencies[0]` |
| https://go.dev/dl/?mode=json&include=all | 2026-10-20 | `"filename": "go1.25.0.linux-amd64.tar.gz",` | go-dl.json:14644 |
| https://go.dev/dl/?mode=json&include=all | 2026-10-20 | `"sha256": "2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613",` | go-dl.json:14648 |
| https://go.dev/dl/?mode=json&include=all | 2026-10-20 | `"stable": true,` | go-dl.json:14515 (entry `"version": "go1.25.0",` at :14514) |
| https://go.dev/dl/go1.25.0.linux-amd64.tar.gz | 2026-10-20 | `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613  go1.25.0.linux-amd64.tar.gz` (command output, not page text) | `sha256sum` of the downloaded archive; `stat -c %s` = 59659213 |

Suggested Search log note (L1 to add; rule 5):

> 2026-10-20 round 19, SourcesRowsDraft (w1). Question: what do the registry and go.dev pin for rea-agents@6.7.0 and go1.25.0 linux-amd64. Where searched: `registry.npmjs.org/rea-agents/6.7.0`, the packument, the npm attestation endpoint and tarball; `go.dev/dl/?mode=json&include=all` and `go.dev/dl/go1.25.0.linux-amd64.tar.gz`. Identified 4 sources; screened 4; included 2 (S037, S038); excluded 2 (the packument as a standalone row, folded into S037's anchor; the attestation endpoint, folded into S037). Stop: one fetch per URL plus digest cross-checks.

## Findings / limits

- Calibration of the rows: S037 and S038 are tier A for their narrow scopes (registry publish identity; official archive digest). Neither row says anything about `rea-agents` behaviour or Go 1.26/1.27 support.
- `dist-tags.latest` is `6.7.0` and may move on the next release, so S037 recheck is `on-release`. S038's archive is immutable, but the listing is re-generated, so I used `180d`.
- The go-dl.json snapshot is time-varying (top stable entry go1.27.3 at fetch time). Only the go1.25.0 entry is cited.
- No check of the client pins (C2) or the carrier run (C3). Those belong to other seats.

## Integration notes for L1

- Insert the two rows after S036; the census above (38 rows, 0 malformed, no duplicate ids) is what the lane should see after integration. I did not run the census in the lane.
- `claims.json` C2 cites "npm registry metadata for rea-agents" and C3 cites "go.dev/dl JSON go1.25.0 linux-amd64 archive sha256": S037 and S038 map to those.
- Carrier provenance (observation 7) is an observed match, not a run; C3 execution remains L1's.
