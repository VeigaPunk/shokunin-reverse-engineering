# R26 w1 — evidence-id minting across rea-agents 6.5.0 / 6.7.0 (6.4.0 not on host)
Seat KaidokuR26.PinSourceDiff. Question: does evidence-id minting differ between the two installed
packages, and can the lane's 6.7.0 arc3 controls (r7, r10, r11, r12) transfer to 6.5.0? Times UTC,
2026-10-22. Read-only on the lane; base a0639d8e61e486e2a716ff94cddd89a73200a02c.
## Answer
**No — ids do not cross-transfer, and there are two independent causes.**
1. The hashed semantic projection changed: 6.5.0 omits `relationship_coverage` when it is null, 6.7.0
   always emits it. For null-coverage verbs this alone changes every id.
2. Per-verb evidence payloads also moved. `function` on `/usr/bin/jq` has non-null coverage, so rule
   (1) is inert there, yet the ids still differ: `analysis_profile.parameters` changed
   (`ghidra-function-boundary-limitations-v3` -> `v4`, `exact-address-incoming-v1` ->
   `exact-address-incoming-without-synthetic-entry-v2`).

So the 6.7.0 arc3 id strings cannot be carried into a 6.5.0 table; the round-26 C1 table must be
minted at 6.5.0 as the freeze says. The arc3 *verdict classes* (same-path repeat stable, path
sensitive) do transfer, because both differing inputs are constant across runs of one version, so
every equality/inequality relation among ids is preserved (observation for the four recomputed
entries; inference for untested verbs).

**6.4.0:** no copy exists on this host. `grep -rho "rea-agents-[0-9][0-9.]*\.tgz" ~/.npm/_cacache/index-v5/`
(6.4 pattern exit 1, 2026-10-22T12:09Z) returns only `rea-agents-6.5.0.tgz`; a walk of all 536
`~/.npm/_cacache/content-v2` files, reading `package/package.json` from every gzip member, printed
exactly one line: `rea-agents@6.5.0  ./sha512/0b/a0/46ec…`. The two `_npx` trees are 6.5.0 and 6.7.0
only; the pnpm store has none. The 6.4.0 path arc3 r7 recorded
(`/home/vgpnk/.npm/_npx/dea9475797100b20/node_modules/rea-agents`) is gone (`ls`: No such file or
directory), so 6.4.0 rests here only on r7's recorded ids and hash ledger.
## Files compared (sha256, both roots)
| file | 6.5.0 | 6.7.0 | |
|---|---|---|---|
| dist/domain/evidence.js | f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff | a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb | DIFF |
| dist/domain/relationshipCoverage.js | ccea848c90db5e4232409dbfc1e863f74ebeb5e10679467e57018156519ec7f8 | af589fd08faac1204361bf347e89ad6c0b1799c09c07c7897e4cadb977a6c399 | DIFF |
| dist/domain/binaryTargetTypes.js | 918849aaa36dd5cb3a9e666623d0449851930fb780c99e5e09c521fe8e33887b | 27ec1d8d5891ebed9017a0ea5a4b5ac84d4ee6568384b392cf19685b6e87f6b9 | DIFF |
| dist/contracts/analysisViewApiSurfaceExample.js | cb4ec89f27106078ced5d37ff22171feb4657a7cd7a06450fdd0d080a33946c2 | c6da7e38f4f1a9a068728d3e6f20a8c9a03984cce52f03c8f55e338655b1dd20 | DIFF |
| dist/contracts/analysisViewToolContracts.js | 56d855027367aa4d3bd0cbdeb573db2e768732d76aeff529d3ec483f13b9242c | 99db7ac98a72e6f2d95899fb2450d39e79307db36e9aa14764992a669175148f | DIFF |

SAME byte for byte in both trees (digest and hash plumbing): `canonicalDigest.js`
f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9, `canonicalJsonDigestSteps.js`
2d09327e55445a7c0d991b8e29c8a0bf8aa9a4955b5e4ec383b3d46ba6e0ddb6, `digests.js`
d3b4765597f6b2d7856d414bee84ffb172a7529095a5044d6119b03ba50748a5, `immutableJson.js`
1c919c359ae1a0bd21eef017cbe8c8f31950e41f889eb63f5add6afda31d3029, `evaluation/KnownAnswerEvaluation.js`
cd9d35a8a6fb076b0206228cd7f0f89301a07c9672b4f0dbab632277d7928abd; the bundled projection copies
`mcp/nativeValueTrace-*` and `cli-runtime/reconstructionObligationLedgerSchemas-*` show the same one-line change.
## The differing hunk that touches ids
`dist/domain/evidence.js`, `semanticProjection` (the hashing input of `computeEvidenceId`):

```
6.5.0 evidence.js:175-177      6.7.0 evidence.js:178
  ...(evidence.relationship_coverage === null    relationship_coverage: evidence.relationship_coverage,
      ? {}
      : { relationship_coverage: evidence.relationship_coverage }),
```

Supporting non-hashing changes in the same file: `relationship_coverage` schema `.default(null)`
(6.5.0:113) becomes plain `.nullable()` (6.7.0:116); the subject architecture enum excludes
`RAW_ONLY_ARCHITECTURES` (6502, m68k) at 6.7.0:60. `normalizeEvidenceObservation`, which always sets
`relationship_coverage` (null when unspecified) before the schema parse, is byte-identical in both.
`relationshipCoverage.js` differs only by swapping inline `z.tuple(...)` for `fixedTupleSchema([...])`;
the three coverage shapes and fields are unchanged, so it cannot move an id. `binaryTargetTypes.js`
only adds m68k/hexagon, so `x86_64` subjects are untouched. Contract example ids moved as a
*consequence* (`ev_9e218c18…` -> `ev_90073e94…`, plus `view_digest`), corroborating a re-mint.
Canonicalizer: `digestCanonicalValue` drops `undefined` members and emits `null` as `null`
(identical bytes), so the rule is exactly "key absent vs key null".
## Measured live (/usr/bin/jq, sha256 e8156675…7806, 30,800 B)
| verb | 6.5.0 id | 6.7.0 id | payload equal? |
|---|---|---|---|
| inspect-binary-layout | ev_294a449cecf2d7b6e72b63b8385b6dcacf589b58c55d9de3ce1b0a81760a71bd | ev_d1256a9649ddcb43a9251b202eb4dafb049ab50c11f92f907915899fa3d4cb2a | yes (coverage null) |
| function 0x103fa0 | ev_b2b7e9e4313ef4f23e003a3dc178fc8652eba209721c1f208955db1e4e0488b5 | ev_177586c695241d1e2552be2ca7def13c291756b00ae13c226875c6c615915be8 | no (analysis_profile) |

Commands (`<seat>` = /fast/scratch/hyaku/kaidoku-r26/seats/PinSourceDiff): `TMPDIR=<seat>/tmp npx -y
rea-agents@6.5.0 <verb> … --format json --full-output` -> `out/*-650.json` (exit 0, 12:14:23Z /
12:15:22Z); `TMPDIR=<seat>/tmp node /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/scripts/rea.mjs
<verb> …` -> `out/*-670.json` (exit 0, 12:14:30Z / 12:15:36Z). Excerpts: layout envelopes byte-identical
apart from the id (`"ev_294a449c…60a71bd"` vs `"ev_d1256a96…d4cb2a"`, both `"relationship_coverage":null`);
`function` walk `/analysis_profile/parameters/function_boundary_observations` `"…v3" -> "…v4"`.
## Can the arc3 6.7.0 controls transfer?
Recomputation (`<seat>/recompute-projection.py`, both projection rules, from the stored 6.7.0
envelopes; r10/r11/r12 exit 0, r7 exit 1 because its two 6.4.0 envelopes must miss the 6.7.0 rule; 12:14Z–12:16:55Z):

| entry | verb | 6.7.0 rule reproduces recorded id | 6.5.0 rule |
|---|---|---|---|
| r7 (probes/67-base1, 67-copyA) | inspect_evm_interface | yes, 2/2 | different id |
| r10 (probe-base1, probe-copyA) | inspect_rust_binary | yes, 2/2 | different id |
| r11 (inspect-artifact-base-1, -copy) | inspect_artifact | yes, 2/2 | different id |
| r12 (base-1, copy-a) | inspect_go_binary | yes, 2/2 | different id |

All eight recomputed envelopes carry `relationship_coverage: null`, so every recorded 6.7.0 id is one
rule-step away from its 6.5.0 value. Verdict: **the id values fail to transfer**; the stability and
path-sensitivity conclusions **hold** as relations, because the added key is constant per run set. A
control restated at 6.5.0 must re-derive its id by omitting the null key before hashing (the 6.5.0
branch of `recompute-projection.py`), never by copying the arc3 string.

**6.4.0 equivalence (inference with measurement support):** the 6.5.0 rule run over r7's two recorded
6.4.0 envelopes reproduces both recorded ids exactly (`64-base` -> `ev_36c9dd69…bdc`, `64-copyA` ->
`ev_e126868e…64f`) while the 6.7.0 rule misses both, so 6.4.0 and 6.5.0 share one id domain on that
verb and 6.7.0 is the outlier. r7's recorded 6.4.0 `evidence.js` sha256
`690dc0355ce8dd64417b8ebb1ebd4a06c6b5ece648eeb7caf6978638b880de39` differs from 6.5.0's `f992d93e…`,
so the files differ outside the hashed projection.
## Unknowns
- Payload drift was exercised live on 2 of the 8 round verbs (layout, function); which of the other six also moved their `analysis_profile` is unknown. MCP-side equivalence is inferred from the bundled copies, not from an MCP session. No 6.4.0 bytes were read this round; its statements rest on r7's recorded ids and hash ledger.
## Artifacts (sha256, under /fast/scratch/hyaku/kaidoku-r26/seats/PinSourceDiff)
```
65b6924…f1b0f recompute-projection.py   5d216ac…d1e666 evidence-js.diff
4edce78…0b75f hashes-650.txt (1574)     ab668eb…0b8d4 hashes-670.txt (1699)
f717812…3f67f out/layout-650.json       1d78b74…cd4aa out/layout-670.json
3bca4dc…a3630 out/function-650.json     9246dff…8cb6 out/function-670.json
a0ac833…e6e5fc out/recompute-live.txt   774e53e…5e24f out/recompute-r7.txt
b454234…f37286 out/recompute-r10.txt    96470c8…a091b out/recompute-r11.txt
92430c4…e2e2ff out/recompute-r12.txt
```
Full digests: `sha256sum <seat>/{recompute-projection.py,evidence-js.diff,hashes-650.txt,hashes-670.txt,out/*}` (exit 0, 2026-10-22T12:16Z). 6.5.0 custody: cached tarball `size=5634033`, sha512-b64
`C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`
equal to the `_cacache` index integrity for `rea-agents-6.5.0.tgz`; `package.json` 6.5.0
a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c, 6.7.0
3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570. No tools installed or upgraded.
