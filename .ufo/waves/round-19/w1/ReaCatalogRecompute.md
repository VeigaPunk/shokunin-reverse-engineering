# ReaCatalogRecompute — REA catalog identity recompute (kaidoku round 19, wave 1)

Seat: `KaidokuR19.ReaCatalogRecompute` (executor, leaf). Clone `/tmp/kr19-ReaCatalogRecompute`,
created per contract `Writers`, detached at observed base `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`
(= baseline B; `git rev-parse HEAD`, exit 0). LANE `refs/heads/main` was observed at
`85589ac757f9ca3cb25efcd702d0963e25c9c4df`; all PROVINCE line anchors below are B-relative.

## Result (observation)

`PROVINCE.md:8-24` states the 6.7.0 and 6.5.0 catalog identities; both recompute **exactly** — no drift.

| version | `npx_cache_dir` | `cli_commands` | `mcp_tools` | `tools_sha256` |
|---|---|---|---|---|
| 6.7.0 | `/home/vgpnk/.npm/_npx/a1722018f28f9df2` | 153 | 207 | `af39310c9591bb981893ec0d2188b1bcf6e9cc8ba3ac513d5bbefc8ddcb85639` |
| 6.5.0 | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6` | 153 | 207 | `805433f17bb4f709558ff20c04f96fe561fca2938fd0f459b1f8cc0f6b438ded` |

Comparison anchors at B:
`PROVINCE.md:9-10` (6.5.0, 207/153, `805433f1…`), `:10-12` (6.7.0, 207/153, `af39310c…`,
"the package's compiled, recorded identity"), `:19-21` (cache dirs + full digests).
Evidence records: `.ufo/waves/round-19/evidence/rea-catalog.json:2-15` (6.7.0), `:16-29` (6.5.0).

## Method reproduced (observation)

Recorded method located by `git grep -n tools_sha256` (see log): the exact node argv is at
`.ufo/waves/arc2-loop1-round2/R3.md:166`; the same values were produced from each package's own
`createCatalogDigests()` at `E14.md:67-69`, with the digest projection and the 6.7.0 recorded-constant
caveat at `E14.md:71-75` (`R6.md:14,210`).

The tool (`.ufo/waves/round-19/tools/rea-catalog.py`) runs that argv — stored verbatim per record as
`method_argv` — importing four compiled modules (`PROBE`, `rea-catalog.py:52-70`):

1. `dist/catalogIdentity.js` → `CATALOG_IDENTITY.counts`, `createCatalogDigests()`,
   `CATALOG_IDENTITY.digests`;
2. `dist/cliCommandNames.js`, `dist/contracts/toolContracts.js`, `dist/contracts/promptContracts.js`
   → independent count derivations.

Key distinction: on 6.7.0 the default `CATALOG_IDENTITY.digests` getter returns the build-time
`RECORDED_CATALOG_DIGESTS` (`dist/recordedCatalogDigests.js:2`; selection at `dist/catalogIdentity.js:71-75`).
The probe therefore also calls `createCatalogDigests()` (`dist/catalogIdentity.js:51-66`), which recomputes
`af39310c…` from the compiled contracts; identity and recomputation agree, so the recorded constant is
verified rather than echoed. 6.5.0 ships no recorded file (`ls` exit 2) and computes both
(`dist/catalogIdentity.js:56-66`, `:69-84`).

Independent checks, all passing (no `FINDING:` lines):
`CLI_COMMAND_NAMES.length` = 153, `TOOL_CONTRACTS.length` = 207, `PROMPT_CONTRACTS.length` = 6
for both packages, equal to `CATALOG_IDENTITY.counts`; `node scripts/rea.mjs --version` printed
`6.7.0` and `6.5.0` from the respective caches; node `v24.21.0`.

## Command log (verbatim; observed exit)

```text
git grep -c tools_sha256 -- .ufo/waves/arc2-loop1-round2/R3.md .ufo/waves/arc2-loop1-round2/E14.md
                                                                            # exit 0 -> R3.md:2, E14.md:9
sed -n '1,30p' PROVINCE.md > /dev/null; git rev-parse refs/heads/main       # exit 0 each -> 85589ac757f9…
sed -n '55,90p' .ufo/waves/arc2-loop1-round2/E14.md                         # exit 0
grep -rn "repro-digest\|createCatalogDigests\|recordedCatalogDigests" --include='*' -l . 2>/dev/null | grep -v interactive-sessions | head -30  # exit 0 (pipeline)
ls -d /home/vgpnk/.npm/_npx/*                                                # exit 0
for c in a1722018f28f9df2 ad9a3fdbcad992c6; do d=/home/vgpnk/.npm/_npx/$c/node_modules/rea-agents; node -e "const p=require('$d/package.json'); console.log(JSON.stringify({version:p.version,bin:p.bin}))"; echo "EXIT:$?"; done  # exit 0 each
cat .ufo/waves/round-19/claims.json                                          # exit 0
grep -rn "tools_sha256\|catalogIdentity\|CATALOG_IDENTITY" corpus/ | head -40  # exit 0 (pipeline)
sed -n '140,200p' .ufo/waves/round-19/gen-wave1.py                         # exit 0
cd /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents && grep -rln "CLI_COMMAND_NAMES" dist | head && grep -rn "export const CLI_COMMAND_NAMES\|export const TOOL_CONTRACTS\|export const PROMPT_CONTRACTS\|sortedToolContracts" dist | head -20  # exit 0
sed -n '40,95p' /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/catalogIdentity.js  # exit 0
sed -n '45,90p' /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/catalogIdentity.js  # exit 0
for c in a1722018f28f9df2 ad9a3fdbcad992c6; do d=/home/vgpnk/.npm/_npx/$c/node_modules/rea-agents; node --input-type=module -e "const m=await import('file://$d/dist/catalogIdentity.js'); console.log(JSON.stringify({counts:m.CATALOG_IDENTITY.counts,recomputed:m.createCatalogDigests(),identityDigests:m.CATALOG_IDENTITY.digests}))"; echo "EXIT:$?"; done  # exit 0 each
node --version                                                              # exit 0 -> v24.21.0
for c in a1722018f28f9df2 ad9a3fdbcad992c6; do d=/home/vgpnk/.npm/_npx/$c/node_modules/rea-agents; node --input-type=module -e "const d='$d'; const cli=await import('file://'+d+'/dist/cliCommandNames.js'); const tc=await import('file://'+d+'/dist/contracts/toolContracts.js'); const pc=await import('file://'+d+'/dist/contracts/promptContracts.js'); console.log(JSON.stringify({cli_commands:cli.CLI_COMMAND_NAMES.length,mcp_tools:tc.TOOL_CONTRACTS.length,mcp_prompts:pc.PROMPT_CONTRACTS.length}))"; echo "EXIT:$?"; done  # exit 0 each -> 153/207/6
for c in a1722018f28f9df2 ad9a3fdbcad992c6; do d=/home/vgpnk/.npm/_npx/$c/node_modules/rea-agents; echo "== $c"; timeout 30 node "$d/scripts/rea.mjs" --version 2>&1 | head -3; echo "EXIT:${PIPESTATUS[0]}"; done  # exit 0 each -> 6.7.0 / 6.5.0
for c in a1722018f28f9df2 ad9a3fdbcad992c6; do d=/home/vgpnk/.npm/_npx/$c/node_modules/rea-agents; echo "== $c"; sha256sum "$d/package.json" "$d/dist/catalogIdentity.js"; echo "EXIT:$?"; ls "$d/dist/recordedCatalogDigests.js"; done  # sha256sum exit 0 each; 6.5.0 ls exit 2
ls -d /home/vgpnk/.npm/_npx/dea9475797100b20                                # exit 2 (absent)
git show 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0:PROVINCE.md | sed -n '8,24p' | nl -ba -v8  # exit 0
rm -rf /tmp/kr19-KaidokuR19.ReaCatalogRecompute && git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr19-KaidokuR19.ReaCatalogRecompute && git -C /tmp/kr19-KaidokuR19.ReaCatalogRecompute checkout -q --detach 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 && git -C /tmp/kr19-KaidokuR19.ReaCatalogRecompute rev-parse HEAD  # exit 0 -> 8a8da7e19375…
rm -rf /tmp/kr19-ReaCatalogRecompute && mv /tmp/kr19-KaidokuR19.ReaCatalogRecompute /tmp/kr19-ReaCatalogRecompute && git -C /tmp/kr19-ReaCatalogRecompute rev-parse HEAD  # exit 0
python3 -I -B .ufo/waves/round-19/tools/rea-catalog.py --selftest           # exit 0
python3 -I -B .ufo/waves/round-19/tools/rea-catalog.py --out .ufo/waves/round-19/evidence/rea-catalog.json  # exit 0
sha256sum .ufo/waves/round-19/evidence/rea-catalog.json                     # exit 0 -> e18b82a2b9ac…
git add -A && git diff --cached --stat 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0  # exit 0
git diff --cached --binary B > LANE/.ufo/waves/round-19/w1/patches/ReaCatalogRecompute.patch  # exit 0
```

All commands above are verbatim (long `-e` scripts are single arguments). Earlier read-only inspections
used the `read`/`grep`/`glob` tools and short `sed`/`head`/`cat`/`find` calls whose content is cited
above; no exit-bearing command is omitted from this log.

## Selftest (exact)

```text
$ python3 -I -B .ufo/waves/round-19/tools/rea-catalog.py --selftest
SELFTEST: CLEAN cases=7
# exit 0
```

That is the whole output; the exact last line is `SELFTEST: CLEAN cases=7`, exit `0`.
Cases: clean (strict), identity-vs-recompute digest mismatch → `FINDING`+exit 1, counts mismatch →
exit 1, missing version → `REFUSED`+exit 2, duplicate cache → exit 2, bad npx root → exit 2,
`--out` bytes equal stdout. Hermetic stubs only, under `tempfile.mkdtemp()`.

## Files changed (patch)

```text
$ git -C /tmp/kr19-ReaCatalogRecompute diff --cached --stat 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
 .ufo/waves/round-19/evidence/rea-catalog.json |  30 ++
 .ufo/waves/round-19/tools/rea-catalog.py      | 414 ++++++++++++++++++++++++++
 2 files changed, 444 insertions(+)
# exit 0
```

Patch: `.ufo/waves/round-19/w1/patches/ReaCatalogRecompute.patch` (456 lines,
sha256 `0e90b94ec468bb68653078e6404492f7d6c3e9d3dea4ac315d7c370fb6e34816`).
Evidence sha256 `e18b82a2b9aca737fbcbb5ddeb96c4807ebca08c5c41c10df7b1d85e8d8e160a`.
No `__pycache__`/`.pyc` (runs use `-B`); no file outside the assignment in the patch.
Evidence shape: JSON array of two records, field order exactly
`version, npx_cache_dir, cli_commands, mcp_tools, tools_sha256, method_argv`
(`FIELDS`, `rea-catalog.py:41`); project by version with `{r["version"]: r for r in data}`.

## Freshness observations for C2 (observation, then labelled inference)

1. **Observation** — `PROVINCE.md:21-22` places 6.4.0 at `/home/vgpnk/.npm/_npx/dea9475797100b20`;
   that directory is absent (`ls -d`, exit 2). Remaining caches: `a1722018f28f9df2` (6.7.0),
   `ad9a3fdbcad992c6` (6.5.0), and `52027bd8fc0022aa` (npx `node@22`, no `rea-agents`).
   **Inference** — the 6.4.0 *digest* row is receipt-backed and historical, but its cache-location
   clause is not live-verifiable today; C2 may mark the path historical or drop it.
2. **Observation** — source custody hashes: 6.7.0 `package.json`
   `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570`, `dist/catalogIdentity.js`
   `892271aac6bdb735164afdd6a7235c7f5fb3f760c521c0d2beaa5784f29012da`; 6.5.0 `package.json`
   `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`, `dist/catalogIdentity.js`
   `023451dbce79652105d59d5b55da5fa3665c7d613021222d5689acc91b1a8e4e`.
   **Inference** — equal counts do not imply an equal catalog: 6.5.0→6.7.0 keeps 153/207/6 while
   `tools_sha256` changes (`E14.md:3`); do not infer digest stability from counts.
3. **Unknown (not probed)** — a live MCP `tools/list` census. This seat recomputes the compiled catalog
   identity (what PROVINCE's "catalog `tools_sha256`" names), not a running server's advertisement;
   round-18 E14's live census reported the same 153/207, so no contradiction is known.

## Risks / blockers / installs

- No blockers. No REA `analyze`/`search`/`decompile`, no Ghidra, no carrier execution, no MCP server
  started; the probe only imports the installed package's compiled JS modules at build-time-computed paths.
- No installs or upgrades (no pacman/uv/npm); existing npx caches were read in place, so `npx -y`
  resolution was deliberately avoided. Node v24.21.0 was already present.
- Residual risk: evidence values are bound to the installed artifact bytes hashed above; a cache
  replacement changes them even at the same version string.
