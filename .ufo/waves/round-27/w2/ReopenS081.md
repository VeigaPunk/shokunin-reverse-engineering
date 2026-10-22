# W2 ReopenS081 — SOURCES row S081 and round-27 Gate lines re-opened

Seat KaidokuR27.ReopenS081, 2026-10-22. Item attacked: SOURCES row S081 (`corpus/SOURCES.md:87`)
and the five S081 rows of the `## Gate` table in `corpus/lessons/round-27.md:26-30` — i.e. the
claims that the installed rea-agents 6.7.0 tree is the registry's own published tarball, that the
Gate quotes sit verbatim at their stated lines, and that the row's 11-column shape and
status/opened/used-by cells are right. Verdict: **holds** (one cosmetic anchor-range nit,
disclosed below). No installs were performed (curl, openssl, jq, tar, awk, sha1sum/sha256sum,
diff, grep all pre-existing host binaries). All commands exit 0 unless stated.

## Checks (command → excerpt, exit, UTC, verdict)

1. Registry identity vs fetched tarball. `curl -fsS https://registry.npmjs.org/rea-agents/6.7.0 -o dl/registry-6.7.0.json && jq -c .dist` →
   `"shasum":"11f23ba377303a5c28b3162180cf2bf3f3643708","tarball":"https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz","fileCount":1775,"integrity":"sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw=="`.
   `curl -fsSL …/rea-agents-6.7.0.tgz -o dl/rea-agents-6.7.0.tgz && sha1sum … && sha256sum …` →
   `11f23ba377303a5c28b3162180cf2bf3f3643708` and `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90`, 6276963 bytes.
   Computed sha1 == registry dist.shasum. Exit 0, 15:38:17Z. Observation → **holds**.
2. sha512 integrity. `openssl dgst -sha512 -binary dl/rea-agents-6.7.0.tgz | openssl base64 -A` →
   `yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==` ==
   registry `dist.integrity` after the `sha512-` prefix. Exit 0, 15:39:07Z. Observation → **holds**.
   (First attempt used `-sha256` by my own error and mismatched; recomputed with `-sha512` before concluding.)
3. Tarball bytes vs installed tree. `tar -xzf dl/rea-agents-6.7.0.tgz -C unpack && diff -rq unpack/package /home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents; echo exit=$?` → no output, `diff_package_exit=0`; same for `unpack/package/dist` vs installed `dist/` (`diff_dist_exit=0`). 15:38:53Z.
   Reproduces S081's cell "`diff -rq` empty, exit 0" and the Gate's byte-identity basis. Observation → **holds**.
4. Re-hash of installed 6.7.0 files. `sha256sum …/rea-agents/dist/domain/evidence.js …/dist/domain/canonicalDigest.js …/rea-agents/package.json` →
   `a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb`, `f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9`, `3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570`; `jq -r .version package.json` → `6.7.0`. 15:39:07Z.
   All three equal the Gate's sha256 column (rows 1-4) and the S081 anchor. Observation → **holds**.
5. Gate quotes verbatim at stated lines (fixed-string grep, line numbers from the tool):
   - installed `dist/domain/evidence.js:178` = `    relationship_coverage: evidence.relationship_coverage,` — Gate quote is this line verbatim (leading indent stripped; contiguous). ✓
   - installed `dist/domain/evidence.js:183` = `const computeEvidenceId = (evidence) => `ev_${digestCanonicalValue(semanticProjection(evidence), "Evidence")}`;` — verbatim. ✓
   - tarball member `unpack/package/dist/domain/evidence.js:183` — same line, grep-pinned in the unpacked member. ✓
   - `dist/domain/canonicalDigest.js:8` = `export const digestCanonicalValue = (value, context = "Comparison") => {` — verbatim. ✓
   - `package.json:4` = `  "version": "6.7.0",` — verbatim. ✓
   All five quotes are ≤ 25 words. Greps run 15:39-15:40Z, exit 0 each. Observation → **holds**.
6. 11-column shape. `awk -F'|' 'NR==5{print NF-2} NR==87{print NF-2; …}'` → `header_columns=11`, `s081_columns=11`. 15:40:09Z. Observation → **holds**.
7. S081 tail cells (line 87): `status=[ mined ]`, `opened=[ 2026-10-22 ]`, `recheck=[ on-release ]`,
   `usedby=[ tools/round-27/xpin-attribute.mjs, corpus/lessons/round-27.md ]`. 15:40:09Z.
   Matches the lesson's row-change claim (`round-27.md:58-59`: status `mined`, used-by exactly those two), and both used-by files exist (glob). Observation → **holds**.
8. Anchor internals. semanticProjection opens at `evidence.js:159`, field list closes `});` at `:181`,
   `:178` relationship_coverage, `:183` id rule — the anchor's `:159-181` range is exact. Nit:
   anchor says `canonicalDigest.js:8-25` but the `digestCanonicalValue` construct closes at `:26`
   (`25| return hash.digest("hex"); *26|}; *27|const emitCanonical`); range 8-25 omits only the
   closing-brace line; the quoted line `:8` and sha256 are exact. 15:41:30Z. Observation → **holds** with cosmetic nit.
9. Teaches cell cross-pin claim. 6.5.0 `dist/domain/evidence.js:174-177` spreads
   `...(evidence.relationship_coverage === null ? {} : { relationship_coverage: … })` (key dropped
   when null) vs 6.7.0 `:178` unconditional `relationship_coverage: evidence.relationship_coverage,`
   — exactly what the teaches cell states. 15:41:30Z. Observation → **holds**.
10. Anchor citations. `corpus/lessons/round-26.md:37` contains "already row S037's family; no new
    row for it"; `round-26-verifier-spotcheck.md:165` is the sampled reject with the disagreement,
    `:197` the routed defect. 15:42:09Z. Observation → **holds**.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r27/seats/w2/ReopenS081/)

- `dl/rea-agents-6.7.0.tgz` — fetched registry tarball — sha256 `20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90`
- `dl/registry-6.7.0.json` — registry 6.7.0 version document — sha256 `ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236`
- `unpack/` — tarball unpacked, 1775 files (matches registry `fileCount` 1775) — per-file sha256 in `manifest-unpacked-sha256.txt`
- `manifest-unpacked-sha256.txt` — sha256 `b9e5d4e21422fffcd02230956b55fddf6c299c4156d7b8996136a41a24d429b2`

## Residual risk and gaps

- I did not re-run REA or the C2 tool; S081's remaining scope text (R27-C2 usage) is attested by
  the checker run recorded elsewhere, not re-exercised here.
- Registry identity rests on the registry's own document plus transport TLS; I did not verify npm
  signatures/attestations for 6.7.0 (out of item scope).
- The one defect-class finding is the `canonicalDigest.js:8-25` anchor range (true span 8-26):
  cosmetic, no quote or hash affected. Nothing else in S081 or its Gate rows failed.
