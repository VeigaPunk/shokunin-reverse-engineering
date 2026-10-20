# ReopenS037 — SOURCES S037 re-opened against the live npm registry

Seat: `KaidokuR19.ReopenS037-3` (scout, leaf; no subagents, no REA/Ghidra, no carrier execution).
Assignment: reopen S037 (registry version, integrity, publish time, attestation if cited); compare the
registry row and the lesson quote; output exact URL / access date / quote.

Lane tip: `refs/heads/main` was `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` at first observation and
`279e8b19c51658bfd05b9e31a1c0894ab2e70537` at the end (`round-19: wave-two fixes …`, 2026-10-20
16:15:31 -0300) — main advanced under a sibling integration during this seat's work. Baseline
`8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` is an ancestor (`git merge-base --is-ancestor …` exit 0
against both tips). The working tree churned under sibling wave-2 seats throughout the run (transient
`M` states for `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-19.md`, the knowledge entry and
`wave2-registry.json`, plus untracked `runs/pass2/` and `w2/`). All row and lesson evidence below is
read from Git objects at `279e8b1` (and `8a8da7e` for the baseline): the lesson quote-presence check ran
against the worktree copy, whose sha256 at that moment (`c6583d44…f2c0`) equaled
`git show 279e8b1:corpus/lessons/round-19.md`, and the quotes and line anchors were re-read from that
Git object; sibling seats have since resumed editing both files, so the worktree is not the evidence
source. This seat made no git writes and touched no lane file except this report. Scratch:
`/tmp/kr19-w2-ReopenS037` (not in the lane).

## Verdict

**CLEAN re-open. No correction row and no append-only change is warranted.** The committed row
(`corpus/SOURCES.md:43`) and both lesson quotes (`corpus/lessons/round-19.md:40-41`) reproduce exactly
from the live registry on 2026-10-20. A 13-assertion machine check passed (`exit 0`). The publish
identity is additionally corroborated upstream: the attested commit is the live
`refs/heads/release/6.7.0` tip and the `rea-agents-6.7.0` tag target, and the attested GitHub Actions
run succeeded on that commit.

Axes: freshness — every cited value unchanged at re-fetch, including byte-identical responses;
calibration — the row's scope matches what the evidence can carry and lane usage stays inside
identity/provenance; depth — digest chain, DSSE subject, workflow, commit/tag/run, cert SAN and tlog
metadata cross-checked.

## Row as committed (observation)

`corpus/SOURCES.md:43`, 13 fields (`awk -F'|' … NF!=13` over the whole registry = 0):

| field | committed value |
|---|---|
| source | rea-agents 6.7.0 npm registry record — https://registry.npmjs.org/rea-agents/6.7.0 (tarball https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz; packument https://registry.npmjs.org/rea-agents) |
| kind | `dataset` |
| tier | `A` |
| scope | Publish identity and integrity of rea-agents@6.7.0 as served by the npm registry, with its SLSA provenance source commit; not the package's runtime behaviour |
| anchor | Version document `dist.integrity`, `dist.shasum`, `dist.attestations`; packument `time["6.7.0"]`, `dist-tags.latest`; attestation URL, predicate `https://slsa.dev/provenance/v1`, `resolvedDependencies[0].digest.gitCommit` `27dc42d10249f0410904a75c0997842eb03b931c`; fetched 2026-10-20 |
| teaches | Pins the 6.7.0 tarball by its sha512 and release-workflow commit, so a client pin can be checked against the registry's own digest before any package code runs. |
| status / opened / recheck | `mined` / `2026-10-20` / `on-release` |
| used-by | `corpus/lessons/round-19.md, corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` |

## Exact URL · access date · quote (observation)

Access date for all fetches: **2026-10-20**; first batch `date -u` = `2026-10-20T19:16:10Z`, second
batch = `2026-10-20T19:18:47Z` (w1 `SourcesRowsDraft` fetched the same day at 18:37:08Z; `NpmRegistrySource`
recorded a packument fetch at 18:47:18Z). The version document, packument and decoded DSSE payload are
single-line JSON (0 newlines), so the location is a JSON path plus a byte offset, not a line number.

| URL | access (UTC) | exact contiguous quote | location / rendering |
|---|---|---|---|
| https://registry.npmjs.org/rea-agents/6.7.0 | 2026-10-20T19:16:10Z | `"integrity":"sha512-yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw=="` | `dist.integrity`, byte 269 of the 22,380-byte body; 1 occurrence; body sha256 `ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236` |
| https://registry.npmjs.org/rea-agents | 2026-10-20T19:16:10Z | `"2026-10-18T08:12:05.640Z"` | `.time["6.7.0"]`, byte 303528 of the 327,312-byte body; 1 occurrence; body sha256 `bfa6974e131d1bafa18cbfd5d2b590c9ae9ee9965916e0c45014f3e8fce36450` |
| https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.7.0 | 2026-10-20T19:16:10Z | `"gitCommit":"27dc42d10249f0410904a75c0997842eb03b931c"` | decoded SLSA payload `predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit`, byte 794 of the 1,033-byte payload; envelope 14,691 bytes, sha256 `438ef37ca9f9ace5cbc68cf859912d550381f5b27eea6afe8e979557339dcd8b`; payload sha256 `842a32884771c32035a1132153bdadbb69468960b19e01e9e58c4806a0ddd183` |
| https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz | 2026-10-20T19:16:10Z | `11f23ba377303a5c28b3162180cf2bf3f3643708  rea-agents-6.7.0.tgz` (command output, not page text) | `sha1sum`; sha512 hex `ca1231da2a096184f50bfb4e35f61e8ad0ba2e19ca98287e6704543a062e85273bdf794686492def7ce1ba0f5698b831a0c74abaa218182a017c3e1f5e43a117`; base64 `yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==`; 6,276,963 bytes |

Additional exact quotes (same fetch): `"version":"6.7.0"` (top-level); `"latest":"6.7.0"`
(`dist-tags`, 1 occurrence); `"uri":"git+https://github.com/morluto/rea@refs/heads/release/6.7.0"`
(payload byte 716); `"ref":"refs/heads/release/6.7.0"` (payload byte 442).

**Row and lesson comparison (observation):** both lesson quotes are exact substrings of the live bodies —
`corpus/lessons/round-19.md:40` (integrity) and `:41` (packument timestamp) — and the row's anchor names
the same fields with the same values. Nothing differs; nothing is stale.

## Field-level verification (observation)

`python3 -I -B verify_s037.py` → `S037: 13/13 checks pass`, `verify_exit=0`:

- version document `version` = `6.7.0`.
- `dist.integrity` = `sha512-` + base64(SHA-512 of the served tarball) — true.
- `dist.shasum` = SHA-1 hex `11f23ba377303a5c28b3162180cf2bf3f3643708` of the served tarball — true.
- packument `.time["6.7.0"]` = `2026-10-18T08:12:05.640Z`; `.dist-tags.latest` = `6.7.0`.
- SLSA attestation `subject[0].digest.sha512` = the tarball's SHA-512 hex — true.
- SLSA `resolvedDependencies[0].digest.gitCommit` = `27dc42d1…b931c`; workflow =
  `{ref: refs/heads/release/6.7.0, repository: https://github.com/morluto/rea, path: .github/workflows/release.yml}`.
- row anchor strings (integrity, shasum, commit, time, predicate) present in `corpus/SOURCES.md:43`.
- lesson quotes present in the fetched bodies (offset 270 for the text without the leading quote;
  packument timestamp at 303529 without the leading quote).

Additional live fields (not cited by the row, checked for drift against w1): `dist.fileCount` 1775,
`dist.unpackedSize` 28575703, `engines.node` `^22.19.0 || ^24.11.0 || >=26.0.0`,
`_npmUser` `GitHub Actions`, `trustedPublisher.id` `github` — all match w1 `SourcesRowDraft.md:29`
and `:31`. Tarball `package/package.json` inside the archive: `name` `rea-agents`, `version` `6.7.0`,
`bin` `scripts/rea.mjs` (`tar -xOf … | jq` exit 0) — the pinned digest covers the 6.7.0 payload.

Freshness check: 33 versions in the packument; the newest publish is 6.7.0
(`.time.modified` `2026-10-18T08:12:05.977Z`); `npm view rea-agents@6.7.0 version dist.integrity dist.shasum time --json`
(npm 11.19.0, exit 0) returns the same version, integrity, shasum and `time["6.7.0"]`.

## Provenance corroboration beyond the row's text (observation)

- `git ls-remote https://github.com/morluto/rea 'refs/heads/release/*'` exit 0 →
  `27dc42d10249f0410904a75c0997842eb03b931c refs/heads/release/6.7.0`;
  `'refs/tags/*6.7.0*'` exit 0 → `27dc42d1… refs/tags/rea-agents-6.7.0`.
- GitHub commit API (`/repos/morluto/rea/commits/27dc42d1…`) HTTP 200, exit 0: committer date
  `2026-10-18T07:40:45Z`, message `chore(release/6.7.0): release rea-agents 6.7.0 (#4983)`.
- GitHub Actions run API (`/repos/morluto/rea/actions/runs/39108764422`) HTTP 200, exit 0:
  `name: Release`, `head_sha: 27dc42d1…`, `event: workflow_dispatch`, `status: completed`,
  `conclusion: success`, `created_at: 2026-10-18T07:43:55Z` — matches the attested
  `invocationId` `…/runs/39108764422/attempts/1`.
- Raw `package.json` at the attested commit (HTTP 200, exit 0): `name` `rea-agents`, `version` `6.7.0`.
- Attestation certificate (openssl exit 0): SAN
  `URI:https://github.com/morluto/rea/.github/workflows/release.yml@refs/heads/release/6.7.0`
  (same workflow/ref as the provenance), issuer `CN=sigstore-intermediate`, validity
  `2026-10-18T08:05:49Z`–`08:15:49Z`, which brackets the publish time `08:12:05.640Z`.
  One tlog entry: `logIndex` `3308597154`, `integratedTime` epoch `1792310749` =
  `2026-10-18T08:05:49Z`, log id `wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0=`.

[INFERENCE] These checks corroborate the publication identity the row claims; none of them says
anything about the package's runtime behaviour, and this seat did not install or execute the package.

## Integration and append-only state (observation)

- Registry census (frozen commands, `CORPUS.md:134-149`) run against the pinned blob
  `git show 279e8b1:corpus/SOURCES.md` (sha256 `d00aee27…fc5f`; the live worktree copy was clean
  against it when sampled): `rows=38`, `malformed=0`, tier `A=33 B=4 C=1`, status
  `mined=36 rejected=2`, no duplicate ids, no enum/tier violations, no missing `used-by` path;
  pipeline exit 0. S037 is 13 fields.
- Baseline `8a8da7e`: 36 rows and **no** S037 (`git show …:corpus/SOURCES.md | grep -c '^| S037 '` → 0,
  exit 1); at `279e8b1`: 38 rows, 1 S037 (exit 0). The row entered in
  `4f6c73f81ae8d31de18377d7ff57e4e10140ce48` (2026-10-20 15:57:44 -0300). The
  `corpus/SOURCES.md` +3 lines there are the S037 row, the S038 row and the round-19 search-log note
  (`corpus/SOURCES.md:71`); `corpus/lessons/round-19.md` gained 98 lines.
- Append-only comparison, w1 draft `SourcesRowsDraft.md:46` vs `corpus/SOURCES.md:43`: 9 of 11 fields
  identical; only field 7 `status` (`queued` → `mined`) and field 10 `used-by` (`—` → two paths)
  changed. The source, kind, tier, scope, anchor, teaches, opened and recheck cells are byte-identical.
- Both `used-by` paths exist and cite S037: `corpus/lessons/round-19.md` (14,215 bytes at `279e8b1`;
  lines 14, 28, 40, 41, 47, 94) and
  `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md` (14,533 bytes;
  line 71 says only "Package identity of rea-agents 6.7.0 is now also registered as S037").
- Lesson quote table header `corpus/lessons/round-19.md:36` carries the access date `2026-10-20`;
  `:40` and `:41` are the S037 quotes; `:47` records rows 36 → 38 and both rows `mined`; `:94` records
  the in-round `used-by` extension.
- Sibling wave-2 addendum: at first observation it was uncommitted worktree text; by the end main had
  advanced to `279e8b1` and now carries it at `corpus/lessons/round-19.md:128-134`
  (`git show 279e8b1:corpus/lessons/round-19.md | grep -c 'S037 version-document'` → 1, exit 0). It
  states the S037 version-document SHA-256 `ae3429d5…c236` — identical to this re-fetch. The only
  change between `d0690fd` and `279e8b1` in the two files is those 10 appended lines
  (`git diff --stat …` → `corpus/lessons/round-19.md | 10 ++++++++++`); the S037 row at
  `corpus/SOURCES.md:43` and the quotes at `:40-41` are unchanged, and the registry still has 38 rows.

## Calibration findings

1. **Tier A is justified for the declared scope.** `CORPUS.md:93-95` puts A at "primary or
   authoritative for that scope"; the registry is the authoritative publication record, and the SLSA
   record is the maintainer workflow's own statement. The row limits that authority explicitly
   ("not the package's runtime behaviour"). Observation, not inference: the scope sentence is present.
2. **No overreach observed in lane usage.** `claims.json:41` scopes S037 to "publish/integrity
   identity … the published version identity only"; the knowledge entry cites identity only; the
   client-pin statements at `SKILL.md:19-20` rest on the configs, not on S037. The row's `teaches`
   ("a client pin can be checked against the registry's own digest") is an inference about npm's use
   of `dist.integrity`, not a measured client behaviour — but it is stated as a capability of the
   digest, which the evidence supports.
3. **Minor ambiguity at `corpus/lessons/round-19.md:28`** [INFERENCE]: the parenthetical
   "(integrity, publish time, sha256 and size reproduced)" reads over the S037/S038 pair. S037's record
   has no `sha256` or `size` field, and the row does not cite one (the tarball's SHA-1/SHA-512 are its
   digests; SHA-256 and 59,659,213 bytes belong to S038's archive). The statement is not false about
   S037 when read over both rows, but a reader could mis-attribute `sha256` to S037.
4. **Shorthand at `corpus/lessons/round-19.md:14`** ("C2 freshness (sourced: S037)") omits the
   identity-only scope carried by `claims.json:41`. [INFERENCE] Not a defect; the amendment and row
   scope both state the limit.
5. **Anchor path precision.** The row cites `resolvedDependencies[0].digest.gitCommit`; the exact
   decoded path is `predicate.buildDefinition.resolvedDependencies[0].digest.gitCommit`. The
   attestation endpoint serves two attestations (npm publish `…/specs/publish/v0.1` and SLSA v1); the
   row names the SLSA one and does not claim the endpoint has only one. Both are consistent with the
   evidence.
6. **Optional hardening, not a defect.** The anchor fixes fields, fetch date and commit but no
   rendering digest. The version document is immutable in practice, yet the anchor also cites the
   mutable `dist-tags.latest`. The wave-2 worktree addendum supplies the version-document SHA-256
   (`ae3429d5…`); the packument SHA-256 `bfa6974e…` is already recorded at
   `.ufo/waves/round-19/w1/NpmRegistrySource.md:15` and reproduced here, so recheck can compare bytes.
   `on-release` remains the right cadence because `latest` moves on release.
7. **No ID collision.** `NpmRegistrySource.md:185` drafted a different, packument-only S037 (`kind tool`);
   it was not integrated. The registry has exactly one S037 (census duplicate check empty), so the
   packument is an anchor of the integrated row, as the search-log note `corpus/SOURCES.md:71` says.

## Limits and unresolved

- **No cryptographic verification of the attestation.** The DSSE signature, Fulcio chain and Rekor
  inclusion proof were not verified: `command -v cosign` exit 1, no verification tool installed (not
  essential to this question). The cert SAN, validity window, subject digest and tlog metadata were
  checked structurally only. [INFERENCE] The digest equality between DSSE subject and served tarball is
  observed; the signature's validity is not asserted.
- **Single registry source.** No independent mirror or registry-operator transparency was consulted;
  `time` and `integrity` are registry-asserted. Mitigation: the tarball bytes were re-hashed locally and
  match both digests, and the publish identity is corroborated by the upstream tag/commit/run.
- **Immutability is observed only inside today's window** (w1 18:37Z, this seat 19:16Z and 19:18Z with
  cache-busting query strings): version document, packument, attestation envelope and tarball were
  byte-identical across those fetches. No claim is made about registry retention policy.
- **Packument rendering depends on the client's Accept header** (npm's abbreviated document vs the
  full JSON fetched here). The cited `.time` and `dist-tags` values also appear through npm 11.19.0
  (`npm view` exit 0), so the quote is not an artifact of one rendering.
- **Client pin reality is outside S037.** Whether Devin/OMP configs actually pin 6.7.0 is C2's live
  probe, not this row; S037 grounds only that 6.7.0 is the published version with this identity.
- **Attestation certificate subject is empty**; the identity is in the SAN URI. Observed, not treated
  as a defect. [INFERENCE] Sigstore keyless certificates commonly carry identity in the SAN; this
  report did not verify that convention against Sigstore documentation.

## Commands and exit codes (condensed; scratch = `/tmp/kr19-w2-ReopenS037`)

```
$ date -u +%Y-%m-%dT%H:%M:%SZ
2026-10-20T19:16:10Z                                              # exit 0

$ curl -fsSL -o s037-version.json -w 'version_http %{http_code} bytes %{size_download}\n' \
    https://registry.npmjs.org/rea-agents/6.7.0
version_http 200 bytes 22380 ; curl_exit=0
$ sha256sum s037-version.json
ae3429d52774e39bda4f8c9ba9aa141b26901ec65f82a394e540ed9cc479c236  s037-version.json   # exit 0

$ curl -fsSL -o s037-packument.json https://registry.npmjs.org/rea-agents
packument_http 200 bytes 327312 ; curl_exit=0
$ jq -c '."dist-tags"' s037-packument.json   -> {"latest":"6.7.0"}   # exit 0
$ jq -c '.time["6.7.0"]' s037-packument.json -> "2026-10-18T08:12:05.640Z"

$ curl -fsSL -o s037-attestation.json 'https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.7.0'
attest_http 200 bytes 14691 ; curl_exit=0 ; sha256 438ef37ca9f9ace5cbc68cf859912d550381f5b27eea6afe8e979557339dcd8b
$ jq -r '.attestations[].predicateType' s037-attestation.json
https://github.com/npm/attestation/tree/main/specs/publish/v0.1
https://slsa.dev/provenance/v1                                   # jq exit 0

$ curl -fsSL -o rea-agents-6.7.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz
tgz_http 200 bytes 6276963 ; curl_exit=0
$ sha1sum rea-agents-6.7.0.tgz   -> 11f23ba377303a5c28b3162180cf2bf3f3643708   # exit 0
$ sha512sum rea-agents-6.7.0.tgz -> ca1231da2a096184f50bfb4e35f61e8ad0ba2e19ca98287e6704543a062e8527
                                    3bdf794686492def7ce1ba0f5698b831a0c74abaa218182a017c3e1f5e43a117
$ node -e '…createHash("sha512")…base64…'
b64sha512=yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==
                                                                 # node_exit=0; equals dist.integrity payload

$ npm view rea-agents@6.7.0 version dist.integrity dist.shasum time --json
version 6.7.0; integrity/shasum as above; time["6.7.0"] 2026-10-18T08:12:05.640Z   # exit 0

$ python3 -I -B verify_s037.py
S037: 13/13 checks pass ; verify_exit=0

$ curl -fsSL -o s037-version-2.json 'https://registry.npmjs.org/rea-agents/6.7.0?cachebust=kr19'
$ cmp -s s037-version.json s037-version-2.json ; byte_identical_exit=0
$ curl … 'https://registry.npmjs.org/rea-agents?cachebust=kr19' ; cmp packuments ; byte_identical_exit=0
$ curl … 'https://registry.npmjs.org/-/npm/v1/attestations/rea-agents@6.7.0?cachebust=kr19' ;
  cmp attestations ; attest_identical_exit=0
$ curl … 'https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz?cachebust=kr19' ;
  cmp tarballs ; tgz_identical_exit=0

$ git ls-remote https://github.com/morluto/rea 'refs/heads/release/*'
27dc42d10249f0410904a75c0997842eb03b931c  refs/heads/release/6.7.0            # exit 0
$ git ls-remote https://github.com/morluto/rea 'refs/tags/*6.7.0*'
27dc42d10249f0410904a75c0997842eb03b931c  refs/tags/rea-agents-6.7.0           # exit 0

$ curl -fsSL https://api.github.com/repos/morluto/rea/commits/27dc42d10249f0410904a75c0997842eb03b931c
commit_api_http 200 ; commit_curl_exit=0
  .sha=27dc42d1… ; .commit.committer.date=2026-10-18T07:40:45Z ;
  .commit.message[0]=chore(release/6.7.0): release rea-agents 6.7.0 (#4983)
$ curl -fsSL https://api.github.com/repos/morluto/rea/actions/runs/39108764422
run_api_http 200 ; run_curl_exit=0
  id=39108764422 ; name=Release ; head_sha=27dc42d1… ; event=workflow_dispatch ;
  status=completed ; conclusion=success ; created_at=2026-10-18T07:43:55Z
$ curl -fsSL https://raw.githubusercontent.com/morluto/rea/27dc42d1…/package.json
raw_http 200 ; raw_exit=0 -> {name: rea-agents, version: 6.7.0}

$ jq -r '.attestations[1].bundle.verificationMaterial.certificate.rawBytes' s037-attestation.json \
    | base64 -d | openssl x509 -noout -subject -nameopt RFC2253 -dates
subject= ; notBefore=Oct 18 08:05:49 2026 GMT ; notAfter=Oct 18 08:15:49 2026 GMT   # cert_exit=0
… -ext subjectAltName ->
  URI:https://github.com/morluto/rea/.github/workflows/release.yml@refs/heads/release/6.7.0
$ jq -c '.attestations[1].bundle.verificationMaterial.tlogEntries[] | {logIndex, integratedTime}'
{"logIndex":"3308597154","integratedTime":"1792310749"} ; timestampVerificationData rfc3161Timestamps []

$ date -u -d @1792310749 +%Y-%m-%dT%H:%M:%SZ
2026-10-18T08:05:49Z                                              # exit 0

$ git rev-parse refs/heads/main
d0690fd44f46d8a7fe9da5f01c6be723d12abd41        # first observation
279e8b19c51658bfd05b9e31a1c0894ab2e70537        # end observation (sibling wave-2 integration, 16:15:31 -0300)
$ git diff --stat d0690fd 279e8b1 -- corpus/SOURCES.md corpus/lessons/round-19.md
 corpus/lessons/round-19.md | 10 ++++++++++
$ git diff d0690fd 279e8b1 -- corpus/SOURCES.md | grep -E '^[+-].*S037'
(empty)                                                            # rowdiff_grep_exit=0; row unchanged
$ git show 279e8b1:corpus/lessons/round-19.md | grep -c 'S037 version-document'   -> 1   (exit 0)

# lane registry (read-only; frozen census commands CORPUS.md:134-149), against the pinned blob
$ git show 279e8b1:corpus/SOURCES.md > /tmp/kr19-w2-ReopenS037/SOURCES.279e8b1.md
$ S=/tmp/kr19-w2-ReopenS037/SOURCES.279e8b1.md
$ sha256sum "$S" -> d00aee278ef6f2de3b8fac440af307fad322008885af0fc37c84bdcdf556fc5f
$ grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' "$S"                        -> 38
$ awk … NF!=13 … "$S"                                                            -> 0
$ awk … tier histogram … "$S"   -> A=33 B=4 C=1
$ awk … status histogram … "$S" -> mined=36 rejected=2
$ awk … uniq -d … "$S"                                                           -> (empty)
$ awk … enum/tier-inflation … "$S"                                               -> (empty)
$ awk … missing used-by paths … "$S"                                             -> (empty; run from lane root)
$ git show 8a8da7e…:corpus/SOURCES.md | grep -c '^| S037 '                       -> 0   (exit 1)
$ git show 279e8b1:corpus/SOURCES.md | grep -c '^| S037 '                        -> 1   (exit 0)
$ git merge-base --is-ancestor 8a8da7e… 279e8b1                                  -> ancestor_exit=0
$ python3 -I -B quote check (lesson :40/:41 substrings)                          -> true/true (exit 0)
```

Tools used (no installs, no updates): curl 8.23.0 (OpenSSL 3.6.5), `jq` binary = jaq 3.1.1,
git 2.56.0, node v24.21.0, npm 11.19.0, OpenSSL 3.6.5, Python 3.14.8 on Linux 7.2.11-arch1-1 x86_64.
No REA/Ghidra call, no carrier execution, no package installation or `npx` execution of the package.

## Bottom line

S037 is a correctly tiered, correctly scoped identity/provenance row. Its version, integrity, publish
time and SLSA attestation all reproduce exactly from the live registry on the same access date the row
and lesson record, and the attested commit is independently bound to the live release branch, tag,
successful Actions run and release-tree `package.json`. The only reader-facing ambiguity is the joint
S037/S038 parenthetical at `corpus/lessons/round-19.md:28`; the remaining calibration notes (shorthand
at `:14`, anchor-path abbreviation, optional rendering digest) are hardening, not corrections, and no
registry correction is required.
