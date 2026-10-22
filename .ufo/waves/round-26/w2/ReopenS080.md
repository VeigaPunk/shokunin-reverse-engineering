# R26 w2 — ReopenS080: SOURCES row S080 and its lesson Gate lines

Seat: KaidokuR26.ReopenS080. UTC 2026-10-22, fetches at 13:00:08Z–13:09:25Z. Lane commit judged:
`003de8cc38a86a914c0348ded674091d47d71fc1` (working tree `git rev-parse HEAD`, exit 0). Scratch:
`/fast/scratch/hyaku/kaidoku-r26/seats/w2/ReopenS080/`. Lane touched only by this report file.

## Verdict

Substance **holds**: all three sha256 pins in the S080 Gate rows reproduce byte-exactly on a fresh
plain-HTTP refetch, every quoted value is present, and the installed npx package matches
`dist.integrity` through four independent checks. One defect, minor, on form: all four S080
"located quote" cells in `corpus/lessons/round-26.md` are written with a space after the JSON
colon (`"integrity": "…"`), but the registry serves compact JSON (`"integrity":"…"`), so as
written the quotes are not contiguous in the pinned bytes — against the Gate's own "Each quote is
contiguous" rule and the round-19 S037 precedent. No live drift in any artifact.

## Per-quote verdicts (all commands 2026-10-22, exit 0)

Fetch command for each: `curl -sS --fail -o <file> <url>`; excerpt form `exit=0 http=200 bytes=<n> sha256=<h>`.

1. Version document https://registry.npmjs.org/rea-agents/6.5.0 — observation —
   `ts=2026-10-22T13:00:08Z exit=0 http=200 bytes=21678 sha256=52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde`
   → Gate sha256 cell **verified**, byte-identical to wave-1's 12:12Z fetch. `dist.integrity`
   quote: space-form count **0**, compact count **1** (`grep -c -F '"integrity": "sha512-C6BG'` vs
   `grep -o -F '"integrity":"sha512-C6BG'` on vdoc.json). `dist.shasum` quote: space-form **0**,
   compact **1**. Values true; form not contiguous. **Verdict: holds on value, fails lane
   contiguous-quote form.**
2. Packument https://registry.npmjs.org/rea-agents — observation —
   `ts=2026-10-22T13:00:08Z exit=0 http=200 bytes=327312 sha256=bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450`
   → Gate sha256 cell **verified**. `time["6.5.0"]` quote `"6.5.0": "2026-10-14T12:56:14.513Z"`:
   space-form **0**, compact **1**. `jq -r '.["dist-tags"].latest'` → `6.7.0`;
   `.time.modified` `2026-10-18T08:12:05.977Z`; `.versions["6.5.0"].dist.integrity` equals the
   same sha512. **Verdict: holds on value, fails form.**
3. Attestation https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.5.0 — observation —
   `ts=2026-10-22T13:00:08Z exit=0 http=200 bytes=14481 sha256=af5a2c203702c99a70713075860cdf87ef108383cc74d3e020a235ad2d7bdf0b`
   → Gate sha256 cell **verified**. Bundle holds 2 attestations; the SLSA one decodes to payload
   sha256 `6001416ab8008690e984ab77e56ff4c00b6e0b9f13d0e4347738af19a10d096a`, byte-identical to
   wave-1's decoded payload. `gitCommit` sits at exactly
   `predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit` = `3b79af28e80785afce9f5998d8f03289402a1847`
   (Gate section label **verified**); quote is compact-form in the payload, space-form absent.
   **Verdict: holds on value, fails form.**
4. Tarball https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — observation —
   `ts=2026-10-22T13:00:08Z exit=0 http=200 bytes=5634033`; sha1 `7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3`
   and sha512-base64 `C6BG7LyrAdR74mSjertM6PrxJkcNZ2bfQNOJornPo9erDEp2tyPRVYPnV5Yodr+1RqewCQla68WulXlVnveD+A==`
   — exactly `dist.shasum` and `dist.integrity` (via `openssl dgst -sha512 -binary | openssl base64 -A`).

## Does the installed package match dist.integrity? Yes (all observations, 2026-10-22)

- Fresh tarball sha1 == `dist.shasum`, sha512-b64 == `dist.integrity` (finding 4).
- npx cache: `/home/vgpnk/.npm/_cacache/content-v2/sha512/0b/a0/46ec…f8` exists, 5,634,033 B;
  `cacache sha512 == dist.integrity: True`; its sha1 `7ea5e6f6…ab3` == `dist.shasum`
  (verify_attest.py run at 13:08:02Z, exit 0).
- npx lock `…/ad9a3fdbcad992c6/node_modules/.package-lock.json` →
  `version=6.5.0 resolved=https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz integrity=sha512-C6BG7Lyr…A==` (exit 0).
- `tar -xzf` then `diff -r` extracted `package/` vs installed
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`: `diff -r exit=0 diff_lines=0`,
  1650 files each side, 25,564,765 bytes each side — equal to `dist.fileCount` 1650 and
  `dist.unpackedSize` 25564765 from the version document.

## The one defect (minor, actionable)

`corpus/lessons/round-26.md` Gate rows for S080 (lines 28–31) and the SOURCES S080 anchor cell
quote registry JSON with a space after the colon. The pinned bytes (sha256 verified above) contain
only the compact form; `grep -c -F '"integrity": "…"'` → 0. The lane's own standard is exact
contiguity: the round-14 quote-fidelity gate applies "no whitespace, tag or punctuation
normalization" and exits 1 when the quote is absent; and round-19.md:42 quotes the same registry's
`"integrity":"sha512-yhIx…"` in compact form. So all four S080 Gate quote cells, taken literally,
would fail that gate even though every value is true and every sha256 matches. Suggested repair
(for the L1, one commit with the round-26 section): rewrite the four quotes in compact form, or
quote bare values as round-19 does for `.time["6.7.0"]`.

## Extra checks the lane did not claim (observations)

- The npm-publish attestation (bundle entry 0, subject `pkg:npm/rea-agents@6.5.0`) carries a DSSE
  PAE signature that verifies: `openssl dsse PAE verify exit: 0 | Verified OK` under registry key
  `SHA256:DhQ8wR5APBvFHLF/+Tc+AYvPOdTpcIDqOhxsBHRwC7U` fetched from
  https://registry.npmjs.org/-/npm/v1/keys (`bytes=580 sha256=faf23d8753d5bb79…`, 13:04:09Z).
- Both attestations' subject `sha512` hex `0ba046ec…f8` equals `dist.integrity` base64-decoded,
  binding attestation → tarball → installed tree into one chain (verify_attest.py, exit 0, 13:08:02Z).

## Residual risk and gaps

- unknown — the SLSA provenance attestation (bundle entry 1) has an empty signature `keyid` and its
  96-char signature did not verify under either published registry key (tried 2 keys, exit 1). The
  Gate does not claim its verification; the gitCommit quote stands on fetched bytes. Likely cause:
  the keys endpoint publishes registry document-signing keys, not provenance-signing keys.
- unknown — whether GitHub `morluto/rea` at commit `3b79af28…` builds the published tarball
  byte-identically; not opened (wave-1 also left this open).
- The compressed tarball bytes are not pinned anywhere in the lane (sha256 `531717a0…` recorded
  here only); drift in tarball serving would surface only via the digest checks above, which all
  pass today.

## Drift

None observed between wave-1's fetches (12:12Z, 12:16:28Z) and this seat's refetch (13:00:08Z):
version document, packument, attestation, decoded SLSA payload, and tarball all byte-identical;
`dist-tags.latest` still 6.7.0.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/w2/ReopenS080/, sha256)

| file | sha256 |
|---|---|
| fetch/vdoc.json | 52184d3129b17c15a223736c48a3235038f26aa8aaa959f30a4b0931453b5cde |
| fetch/packument.json | bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450 |
| fetch/attest.json | af5a2c203702c99a70713075860cdf87ef108383cc74d3e020a235ad2d7bdf0b |
| fetch/rea-agents-6.5.0.tgz | 531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699 |
| fetch/npmkeys.json | faf23d8753d5bb79df250f10391ac89b63ecf7743e48487a544a99c847f9c8df |
| fetch/att0.payload.bin (npm publish payload) | a5561b57330a1d43f16927157de1c2f93615170eeccad9f6e661242b2703c165 |
| fetch/att1.payload.bin (SLSA payload) | 6001416ab8008690e984ab77e56ff4c00b6e0b9f13d0e4347738af19a10d096a |
| fetch/att0.sig.bin | db14efe8d9bf7d7bdc6f2c3768f8a7946a2dad1853313bc7ad8c0b94ac6d6f4e |
| fetch/att1.sig.bin | 473c39070271cadd269c558cb0b14f30c57898d7fd5db1be3ecc878a770c21f0 |
| fetch/treediff.txt (empty, diff clean) | e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855 |
| verify_attest.py | 3c476ee5d67afd3fe9a90f18f04dee9887b0957b2c79bf75618bf2bb529c73de |
| fetch/x/package/ (extracted tarball) | directory, re-extractable from the tgz above |

## Bounds and tooling

No lane file edited except this report; no git/jj write anywhere (only `git rev-parse HEAD`
read-only in the lane); no REA call needed (plain HTTP and hashing only); no tool installed or
upgraded. Access dates 2026-10-22; all sources opened by plain `curl` HTTP fetch.
