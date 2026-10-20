# NpmRegistrySource — REA npm registry record (round 19, w1)

Read-only seat. One question: what does the npm registry publish for `rea-agents`, and
what do the `6.5.0` (contract pin) and `6.7.0` (`latest`) records say? No package was
installed or executed; `npx` was queried (`--version`) but never invoked on `rea-agents`.

Labels: **[obs]** observed in tool output below; **[inf]** inference from those observations.

## 1. Access record

Three GETs, no credentials, no auth header. Second pass at 18:47:18Z is byte-identical to
the first pass for all three, so the hashes below are stable over a 10-minute window.

```
2026-10-20T18:47:18Z http=200 bytes=327312 sha256=bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450 https://registry.npmjs.org/rea-agents
2026-10-20T18:47:18Z http=200 bytes=22380  sha256=ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236 https://registry.npmjs.org/rea-agents/6.7.0
2026-10-20T18:47:18Z http=200 bytes=21678  sha256=52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde https://registry.npmjs.org/rea-agents/6.5.0
exit=0
```

First fetch of the packument was `2026-10-20T18:37:26Z` (`date -u`), same 327312 bytes and
same sha256 — **[obs]** the document did not change between 18:37:26Z and 18:47:18Z.

Response headers (`curl -sSI https://registry.npmjs.org/rea-agents/6.7.0`, exit 0):
`HTTP/2 200`, `content-type: application/json`, `cache-control: max-age=300`,
`cf-cache-status: DYNAMIC`, `server: cloudflare`. CORS `access-control-allow-origin: *`.

Caveat carried on every hash: the packument is a **mutable** document (it gains a version
on each publish); the two version documents are per-version and immutable in practice. A
later reader will not reproduce the packument hash after the next publish. **[inf]**

## 2. Registry facts **[obs]**

| field | value |
|---|---|
| `dist-tags.latest` | `6.7.0` |
| `time.created` | `2026-07-12T12:46:31.493Z` |
| `time["6.5.0"]` | `2026-10-14T12:56:14.513Z` |
| `time["6.7.0"]` | `2026-10-18T08:12:05.640Z` |
| `time.modified` | `2026-10-18T08:12:05.977Z` (same second as the 6.7.0 publish) |
| `repository.url` | `git+https://github.com/morluto/rea.git` |
| `homepage` | `https://github.com/morluto/rea#readme` |
| `bugs.url` | `https://github.com/morluto/rea/issues` |
| `license` | `MIT` |
| `maintainers` | `morluto` (sole) |
| versions published | 33 — `len(d["versions"])`; oldest `0.2.1`, newest `6.7.0` |

Per-version `dist` (read from the packument; re-read from `/rea-agents/<v>` with identical values):

| | 6.5.0 | 6.7.0 |
|---|---|---|
| `dist.integrity` | `sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==` | `sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==` |
| `dist.shasum` | `7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3` | `11f23ba377303a5c28b3162180cf2bf3f3643708` |
| `dist.tarball` | `https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz` | `https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz` |
| `dist.fileCount` | 1650 | 1775 |
| `dist.unpackedSize` | 25564765 | 28575703 |
| `engines.node` | `^22.19.0 \|\| ^24.11.0 \|\| >=26.0.0` | same |
| `bin` | `{"rea":"scripts/rea.mjs","rea-agents":"scripts/rea.mjs"}` | same |
| `dependencies` | 39 | 40 (`openpgp` added; nothing removed) |
| `optionalDependencies` | — | `frida@17.23.2` |
| `mcpName` | `io.github.morluto/rea` | same |

Also in the 6.7.0 record: `description` = "Reverse engineer anything from your terminal or
agent with one CLI and MCP server."; `allowScripts: {"frida@17.23.2": true}`;
`_npmUser` = `{"name":"GitHub Actions","email":"npm-oidc-no-reply@github.com",
"trustedPublisher":{"id":"github","oidcConfigId":"55284132-3079-4ea8-8df7-7f2d6893ac14"}}`;
`_resolved` = `/home/runner/work/rea/rea/.cache/verified-package/package.tgz`;
`_hasShrinkwrap: false`.

## 3. Independent integrity verification **[obs]**

Both tarballs were downloaded and hashed locally. The published `dist.integrity` and
`dist.shasum` both reproduce exactly, so the registry metadata matches the bytes served.

```
$ curl -sS -o .../rea-agents-6.7.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz
http=200 size=6276963   curl_exit=0
sha512-b64: yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==
sha1: 11f23ba377303a5c28b3162180cf2bf3f3643708
sha256: 20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90
exit=0

$ curl -sS -o .../rea-agents-6.5.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz
http=200 size=5634033   curl_exit=0
sha512-b64: C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==
sha1: 7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3
exit=0
```

`fileCount` cross-check — **[obs]** archive entry count equals `dist.fileCount` for both:

```
$ tar -tzf rea-agents-6.5.0.tgz | wc -l   -> 1650   (dist.fileCount 1650)
$ tar -tzf rea-agents-6.7.0.tgz | wc -l   -> 1775   (dist.fileCount 1775)
exit=0
```

**Install hooks [obs]:** the packaged `package.json` (`tar -xzOf … package/package.json`)
declares `scripts.prepare = "node scripts/prepare.mjs"` and **no** `preinstall`, `install`,
or `postinstall` entry. So the tarball itself declares no install-time hook. Whether npm or
a transitive dependency still runs something under `npx -y` was **not tested** — see §7.

## 4. Provenance: `gitHead` drops out at 6.5.0 **[obs]**

`gitHead` is present for 30 of 33 versions and **absent** for exactly `3.0.0`, `6.5.0` and
`6.7.0` — so the drop is not purely the OIDC cutover:

```
versions without gitHead: ['3.0.0', '6.5.0', '6.7.0']   (30 of 33 carry it)
6.5.0 keys include gitHead: False
6.7.0 keys include gitHead: False
6.4.0 gitHead: a56f7bb668ab23fec8d33f7af353ac7ed2fe1895  npmUser: GitHub Actions  trusted: True
6.5.0 gitHead: None                                      npmUser: GitHub Actions  trusted: True
```

`6.4.0`'s `gitHead` equals the tag ref it publishes under, so commit binding used to be
free. From 6.5.0 the registry record no longer names a commit; it names an OIDC
trusted-publishing identity instead. **[obs]**

Commit binding is still recoverable by tag comparison, because upstream tags continue and
the tagged `package.json` is byte-identical to the tarball's:

```
$ git ls-remote --tags https://github.com/morluto/rea.git | tail -3
3b79af28e80785afce9f5998d8f03289402a1847  refs/tags/rea-agents-6.5.0
2c4338db1fdb7773e05376301c558cff2a0b4b80  refs/tags/rea-agents-6.6.0
27dc42d10249f0410904a75c0997842eb03b931c  refs/tags/rea-agents-6.7.0
exit=0   (39 tag refs total)

6.7.0: raw package.json @ tag  -> 3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570
       tarball package/package.json -> 3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570
6.5.0: raw package.json @ tag  -> a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
       tarball package/package.json -> a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c
```

So `6.7.0` = tag `rea-agents-6.7.0` (commit `27dc42d…`) at least at `package.json`
granularity, and `6.5.0` = tag `rea-agents-6.5.0` (commit `3b79af2…`). Equality of one file
is not equality of the whole tree; a full tree comparison was not run. **[inf]**

**`6.6.0` is tagged but not published [obs]:** `time` and `versions` contain no `6.6.0`
(`time keys minus versions keys: []`, `versions minus time: []`, `time has 6.6.0: False`),
while `refs/tags/rea-agents-6.6.0` exists. Published minor sequence is
`… 6.4.0 → 6.5.0 (skip 6.6.0) → 6.7.0`. **[inf]** A reader must not infer "next version
after 6.5.0 is 6.6.0" from the tag list, nor "6.6.0 was unpublished" from its absence —
the packument has no tombstone field, so absence proves only that the published record does
not contain it today.

## 5. Freshness exposure for this lane **[obs facts, inf consequence]**

- The round-19 contract pins the CLI at `npx -y rea-agents@6.5.0 <command>` —
  `.ufo/waves/round-19/contract.md:35`.
- `dist-tags.latest` is `6.7.0`, published `2026-10-18T08:12:05.640Z`, i.e.
  **58.4 h before** the 2026-10-20T18:37Z access; `6.5.0` is 91.3 h older than `6.7.0`.
- The lane's own CLI-surface catalog is one release further back:
  `corpus/knowledge/2026-10-13-rea-cli-surface.md:3` ("rea-agents@6.4.0") and `:10`
  (`rea@6.4.0` versions from `--version`).
- Between 6.5.0 and 6.7.0 the published dependency set gains `openpgp`, `fileCount` grows
  1650 → 1775 and `unpackedSize` 25564765 → 28575703; `bin` and `engines` are unchanged.

**[inf]** Any sentence in the corpus sourced to the 6.4.0 CLI surface (its command count,
global options, subcommand list) is two to three releases behind the artifact the contract
actually runs, and should be re-derived against 6.5.0 or re-labelled with the version it
describes before it grounds a round-19 claim. This report does not assert that 6.6.0/6.7.0
changed any command; that needs a `--help` run, which is outside this seat's question.

**[obs]** Host node is `v24.21.0` (`node --version`, exit 0), inside
`^22.19.0 || ^24.11.0 || >=26.0.0`. So the engine gate is satisfied on this host for both
versions. **[inf]** The pin is loadable here; the registry record alone does not prove the
CLI works.

## 6. SOURCES row draft

Registry state at baseline: 36 rows, `S001`–`S036`, last row at `corpus/SOURCES.md:42`;
no existing row mentions `rea-agents` or `registry.npmjs`
(`grep -n 'rea-agents\|registry.npmjs' corpus/SOURCES.md` → no match, exit 0 via grep pair).
Next free id therefore `S037`. Shape and enums per `CORPUS.md:64` (§SOURCES.md), anchor rule
`:99`, row-is-a-claim rule `:112`. Both rows are `queued` / `used-by: —` because no round-19
lesson cites them yet. **The L1 renumbers if another seat took S037.**

Draft rows, validated with the contract's own census on a two-row file — rows=2,
`malformed: 0`, `tier A=2`, `status queued=2`, no enum violation, no duplicate id:

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S037 | REA CLI npm packument — https://registry.npmjs.org/rea-agents | tool | A | The registry's published release train, `latest` tag, and per-version dist integrity for the `rea-agents` package the contract invokes | Packument sha256 `bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450` fetched 2026-10-20; byte 30137 `description`; byte 85 `dist-tags`; `time` 6.7.0 2026-10-18T08:12:05.640Z and 6.5.0 2026-10-14T12:56:14.513Z | The registry's `latest` is 6.7.0 while the contract pins `@6.5.0`, so a pin and the live latest must be dated together. | queued | 2026-10-20 | on-release | — |
| S038 | REA 6.7.0 version document — https://registry.npmjs.org/rea-agents/6.7.0 | tool | A | The immutable per-version record: declared Node engine range, dist integrity and shasum, and OIDC trusted-publisher identity for 6.7.0 | Document sha256 `ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236` fetched 2026-10-20; byte 1023 `engines`; byte 269 `dist.integrity`; `dist.shasum` `11f23ba377303a5c28b3162180cf2bf3f3643708` | The engine range is recorded per version, so a run can check the host Node (v24.21.0 here) rather than assume the CLI loads. | queued | 2026-10-20 | on-release | — |

### Gate fragment for `corpus/lessons/round-19.md` `## Gate` (rule 1: URL, access date, ≤25-word located quote)

- **S037** — https://registry.npmjs.org/rea-agents, opened 2026-10-20, response
  sha256 `bfa6974e…6450`. Quote, 14 words, contiguous at packument byte 30137 (the
  `description` value): *Reverse engineer anything from your terminal or agent with one CLI
  and MCP server.* Machine-readable anchor for the row's actual claim: byte 85
  `"dist-tags":{"latest":"6.7.0"}`.
- **S038** — https://registry.npmjs.org/rea-agents/6.7.0, opened 2026-10-20, response
  sha256 `ae3429d5…c236`. Quote, 5 tokens, contiguous at byte 1023:
  `"engines":{"node":"^22.19.0 || ^24.11.0 || >=26.0.0"}`.

Both quotes are verbatim substrings of the fetched bytes — verified by
`raw.find(fragment) >= 0` on the saved response, not by eye.

## 7. Remaining unknowns

- **Not tested: any CLI behavior.** No `rea`/`rea-agents` command was run against either
  pinned version, so nothing here says 6.5.0 and 6.7.0 behave alike (`--help` deltas,
  command list, MCP surface).
- **Not verified: npm signature key.** `dist.signatures[*].keyid` is
  `SHA256:DhQ8wR5APBvFHLF/+Tc+AYvPOdTpcIDqOhxsBHRwC7U`; the key itself was not fetched from
  npm's `/-/npm/v1/keys`, so the signature chain is recorded, not validated. The sha512
  integrity *is* independently reproduced (§3).
- **Not tested: install-time script execution under `npx -y`.** Only observed that the
  published `package.json` declares no `preinstall`/`install`/`postinstall`.
- **Not established: full-tree equality** between the 6.7.0 tag and the published tarball;
  only `package.json` was compared byte-for-byte.
- **Unresolvable from the registry: why 6.6.0 was never published.** No tombstone exists.

## 8. Tooling

No installs or upgrades. Used `curl`, `python3 -I -B`, `openssl dgst`, `sha1sum`/`sha256sum`,
`tar`, `git ls-remote` (read-only), `npx --version` (11.19.0, query only). All work in `/tmp`;
the only file written outside `/tmp` is this report.
