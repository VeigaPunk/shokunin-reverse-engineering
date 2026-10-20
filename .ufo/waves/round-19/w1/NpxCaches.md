# W1 scout — npx cache inventory vs PROVINCE.md:19-23 (read-only)

Seat: KaidokuR19.NpxCaches. Base: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`. No lane file touched except this report; no REA/`npx -y` invocation, no carrier execution, no client-config read. Host: linux x64, node v24.21.0 (fnm).

## Observation — inventory of `~/.npm/_npx/*`

| cache dir | rea-agents package.json | version | dir exists | npx spec recorded in dir `package.json` |
|---|---|---|---|---|
| `~/.npm/_npx/52027bd8fc0022aa` | **absent** (only `node_modules/node`, `node-bin-setup`) | — (node 22.23.3) | yes | `{"node":"^22.23.3"}` |
| `~/.npm/_npx/a1722018f28f9df2` | `node_modules/rea-agents/package.json` | **6.7.0** | yes | `{"rea-agents":"^6.7.0"}` |
| `~/.npm/_npx/ad9a3fdbcad992c6` | `node_modules/rea-agents/package.json` | **6.5.0** | yes | `{"rea-agents":"^6.5.0"}` |
| `~/.npm/_npx/dea9475797100b20` | **dir missing** | — | **no** | — |

Exact `~/.npm/_npx/*/node_modules/rea-agents/package.json` files found (2): the a172/ (6.7.0) and ad9a/ (6.5.0) paths above. There is no third REA cache. `find ~/.npm/_npx -type d -name rea-agents` returns exactly those two (exit 0).

Per-file identity:

- `a1722018f28f9df2/node_modules/rea-agents/package.json` — version 6.7.0, size 24696 B, sha256 `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570`, mtime `2026-10-20 11:09:23 -0300`; lock resolves `https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz`, integrity `sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==`.
- `ad9a3fdbcad992c6/node_modules/rea-agents/package.json` — version 6.5.0, size 23946 B, sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`, mtime `2026-10-16 12:49:41 -0300`; lock resolves `rea-agents-6.5.0.tgz`, integrity `sha512-C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`.

Command (exit 0), run once:

```
$ for f in ~/.npm/_npx/*/node_modules/rea-agents/package.json; do ... json version ...; done
/home/vgpnk/.npm/_npx/52027bd8fc0022aa  -> FileNotFoundError (no rea-agents)   EXIT aggregate 0
/home/vgpnk/.npm/_npx/a1722018f28f9df2  -> 6.7.0
/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6  -> 6.5.0
```

## Observation — versions PROVINCE.md names vs dirs today

- `PROVINCE.md:19` — 6.7.0 at `/home/vgpnk/.npm/_npx/a1722018f28f9df2`: **dir exists, version matches.**
- `PROVINCE.md:20-21` — 6.5.0 at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6`: **dir exists, version matches.**
- `PROVINCE.md:21-23` — 6.4.0 at `/home/vgpnk/.npm/_npx/dea9475797100b20`: **dir does not exist.** (`[ -d ]` check: EXISTS a172, EXISTS ad9a, MISSING dea, EXISTS 52027; exit 0.)
- `PROVINCE.md:12` — “both versions have separate npx cache installs”: **stale for the 6.4.0 clause at observation time**; only 6.5.0 and 6.7.0 have cache installs now.
- `~/.npm/_cacache` index has exactly three `rea-agents` keys: the registry packument and the **6.5.0 and 6.7.0 tarballs only** (no 6.4.0 tgz). So the 6.4.0 identity is not locally re-derivable without a network refetch.
- Baseline already documents the dir as present: `git grep dea9475797100b20 8a8da7e` → `.ufo/waves/arc2-loop1-round1/SC1.md:7` (“6.4.0 (`dea9475797100b20`) both present”), `:17`, `:25`; derivation of its `{127,170,6}` / `25802f6d…` at `.ufo/waves/arc2-loop1-round2/C1.md:174-180`. Drift therefore happened between the 2026-10-18 arc2 evidence and 2026-10-20.

## Observation — catalog identities recomputed from the cached packages

Channel: direct ESM import of each cached `dist/catalogIdentity.js` (`CATALOG_IDENTITY`), node v24.21.0, no server/MCP/session, no `npx`, no network. Exit 0 for both.

```
a1722018f28f9df2  {"counts":{"cli_commands":153,"mcp_tools":207,"mcp_prompts":6},
                   "digests":{"tools_sha256":"af39310c9591bb981893ec0d2188b1bcf6e9cc8ba3ac513d5bbefc8ddcb85639",
                              "prompts_sha256":"7152916ab48bd2a9677a5ad9cdbde0a51dc53c113934952ad096e93f5f18aa7e",
                              "combined_sha256":"96d8f6e6ea1b1ba13557216624a3461c738729d53c79b4b0100d1f3a3a32441c"}}
ad9a3fdbcad992c6  {"counts":{"cli_commands":153,"mcp_tools":207,"mcp_prompts":6},
                   "digests":{"tools_sha256":"805433f17bb4f709558ff20c04f96fe561fca2938fd0f459b1f8cc0f6b438ded",
                              "prompts_sha256":"7152916ab48bd2a9677a5ad9cdbde0a51dc53c113934952ad096e93f5f18aa7e",
                              "combined_sha256":"405725e736ec8dc8483435b970acbf20f9f26b9f1fd25203b992f5ab4cd2a4f4"}}
```

Both match `PROVINCE.md:19-21` byte-for-byte on tools digest and on “153 CLI / 207 MCP” (`mcp_prompts=6` is not stated in PROVINCE). The two 6.5.0/6.7.0 packages share `prompts_sha256` but differ in `combined_sha256` (the combined digest also covers CLI names); PROVINCE states neither combined value, so no claim conflict.

Calibration note for any probe built on grep: `tools_sha256` is **runtime-computed** in 6.5.0/6.4.0 (`dist/catalogIdentity.js:905-907` in the 6.5.0 tree; lazy getter exposed at `:69`, `:86`). Only 6.7.0 ships a recorded constant, `dist/recordedCatalogDigests.js:2` (`af39310c…`). A grep for `805433f1…` inside the 6.5.0 tree returns **no matches** (exit 0 from the grep wrapper, empty result) — that is absence of a stored constant, **not** a digest mismatch; the computed digest matches. A static-file check is therefore valid for 6.7.0 alone.

## Registry corroboration (read-only HTTP GET, curl exit 0)

`curl -fsS https://registry.npmjs.org/rea-agents` → 33 versions, dist-tags `latest=6.7.0`; published: 6.4.0 `2026-10-11T04:02:45.490Z` (integrity `sha512-Vj1zWfSl…`), 6.5.0 `2026-10-14T12:56:14.513Z`, 6.7.0 `2026-10-18T08:12:05.640Z`. The 6.4.0 version is still published, so re-deriving its identity later is possible; its local cache install is gone.

## Inference / limits

- **Inference:** the a172/ and ad9a/ dirs correspond to the `rea-agents@6.7.0` / `6.5.0` specs — the association comes from each dir's top-level `package.json` dependency range plus the lockfile `resolved` URL, not from recomputing npm's `_npx` dir hash.
- **Inference:** the `2026-10-20 15:38:33` mtime on both surviving REA cache dirs is npx bookkeeping from today's cache lookups; the same pattern was recorded for `2026-10-18 11:55:56` at `.ufo/waves/arc2-loop1-round1/R3.md:35`. No file inside either package changed (package.json mtimes stay 10-20 11:09 / 10-16 12:49).
- **Inference:** `dea9475797100b20` was removed by cache cleanup/garbage collection, not by an operator-visible uninstall; no local record of the event exists.
- **Unknown (unresolved):** exact removal time and cause of `dea9475797100b20`. The dir is absent, so no stat/atime is available, and nothing under `~/.npm` retains a 6.4.0 record.
- **Unknown (out of seat scope):** whether any client config still pins 6.4.0; client configs were not read here (C2 owns pin reads).
- **Consequence for C2 (advisory, not a design):** PROVINCE's 6.4.0 sentence needs a “cache install no longer present at 2026-10-20” rewrite or an explicit historical marker rather than another unconditional “at `<path>`”; the 6.7.0/6.5.0 rows are confirmed correct as stated. If a probe checks cache identity, compare computed `CATALOG_IDENTITY.digests.tools_sha256`, not a grep.

## Commands pasted with exits

1. `ls -la ~/.npm/_npx/` → exit 0 (3 dirs: 52027…, a172…, ad9a…).
2. per-dir `package.json` + `.package-lock.json` parse (python3) → exit 0; versions/specs/integrities as tabled.
3. `[ -d ]` existence loop over the four hashes → exit 0; dea9475797100b20 MISSING.
4. `find ~/.npm/_npx -type d -name rea-agents` → exit 0; two hits.
5. `npm cache ls 'rea-agents'` → exit 0; packument + 6.5.0 + 6.7.0 tgz keys only.
6. `node --input-type=module` import of both `dist/catalogIdentity.js` → exit 0 each; identities above.
7. `curl https://registry.npmjs.org/rea-agents` → exit 0; publish times above.
8. `git --no-optional-locks grep -n <hash> 8a8da7e` → exit 0; baseline references as cited.
