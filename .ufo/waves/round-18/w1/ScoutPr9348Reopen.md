# R17-S032-DIGEST — PR #9348 re-open probe, and the S033 superseding row

Read-only seat. No REA, no Ghidra, no carrier execution, no `jj`/git write. Only this report was written.
Contract target: `.ufo/waves/round-18/contract.md:44-45` (`R17-S032-DIGEST`). Registry target: `corpus/SOURCES.md:38` (S032).

**Verdict (observation).** Four page fetches produced **four distinct sha256 at the same byte count** (403382). The API
JSON and the `.patch` are byte-stable across repeat fetches. The PR's stable identity is the **head sha
`a214355498e84aa86280be0c31c955aaf94f2d12`**, state `open`, `merged: false`, `updated_at 2026-08-31T11:56:44Z`.
**Inference:** S032's stored page digest `436c0f63…` cannot be reproduced by re-fetching, so S033 must ride the head sha,
not page bytes.

## 1. Commands and receipts (all observed)

### 1.1 Three page fetches (the assigned probe)

```
$ for i in 1 2 3; do
    f=/tmp/r18-pr9348-$i.html
    out=$(curl -sS -L --max-time 60 -A 'Mozilla/5.0 (X11; Linux x86_64)' \
          -w '%{http_code} %{size_download} %{time_total}' -o "$f" \
          https://github.com/NationalSecurityAgency/ghidra/pull/9348 2>&1)
    rc=$?; sum=$(sha256sum "$f" | cut -d' ' -f1)
    echo "fetch$i rc=$rc write=$out sha256=$sum"
  done
fetch1 rc=0 write=200 403382 1.012676 sha256=ef4733585f32735512124ba9ff87899e664aef567bf646d0bc054ebd4ba2956f
fetch2 rc=0 write=200 403382 0.091382 sha256=21b719b04cd4e1bb00bfea72038e04490a34c919cf5b3c65be1854a91d7e7d6d
fetch3 rc=0 write=200 403382 0.090599 sha256=ddc273352e207853122fc2052d588160214fe5638f84b29bdc02c99541166f96
```

**Observation:** 3/3 distinct digests, identical length. A fourth fetch minutes later gave a fourth digest and still
403382 bytes (`43a475111421530356fb0ba7598bf2676a1dd5e851b84d52b427c4da25827927`, `curl` rc=0, HTTP 200); `sha256sum`
over the four files reports **4** unique digests. Instability is not length drift.

**Observation:** none of the four matches S032's `436c0f63d2dc1e5d2946e4bbf15dfafb1f99fa2a3a60f0b42b00918bf7107cb8`
(`corpus/SOURCES.md:38`). The R17 rounding was not reproducible on 2026-10-20.

### 1.2 HTTP validators — none

```
$ curl -sS -I -L --max-time 30 -A 'Mozilla/5.0 (X11; Linux x86_64)' \
    https://github.com/NationalSecurityAgency/ghidra/pull/9348 | grep -icE '^(etag|last-modified)'
0
  (grep exit 1: no match; the block exit was 1)
```

**Observation:** the response carries `date` and a per-request `x-github-request-id` only — **no ETag, no
Last-Modified**. There is no server-offered stable validator for this page, so a byte digest is the only offered
identity and it is unstable by construction.

### 1.3 API JSON — first attempt blocked, then fetched

```
$ curl -sS -L --max-time 60 -H 'Accept: application/vnd.github+json' -A 'kaidoku-r18-scout' \
    -o /tmp/r18-pr9348.json https://api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348
rc=0  HTTP 403  280 bytes  sha256=2282f9baf641a8417b97a1785119fd62f08e3560b50fdecfae2019fff3ae259d
{"message":"API rate limit exceeded for 179.218.13.209. ...","documentation_url":"https://docs.github.com/rest/overview/resources-in-the-rest-api#rate-limiting"}
```

```
$ curl -sS --max-time 30 https://api.github.com/rate_limit | jq -c '.rate'
{"limit":60,"remaining":0,"reset":1792510140,"used":60}      # reset = 2026-10-20T15:29:00Z
```

After the reset (and one `sleep` to it):

```
$ curl -sS -L --max-time 60 -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' \
    -A 'kaidoku-r18-scout' -o /tmp/r18-pr9348-api3.json \
    https://api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348
rc=0  HTTP 200  23035 bytes  sha256=5ce7947f079258beff8a6f186891c6124142a393cd69e67626b97df4bc27b025
```

```
$ curl -sS ... -o /tmp/r18-pr9348-api4.json https://api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348
http=200 rc=0 bytes=23035
api3=5ce7947f079258beff8a6f186891c6124142a393cd69e67626b97df4bc27b025
api4=5ce7947f079258beff8a6f186891c6124142a393cd69e67626b97df4bc27b025
API_BYTES_IDENTICAL=yes
$ curl -sS https://api.github.com/rate_limit | jq -c '.rate'
{"limit":60,"remaining":58,"reset":1792513749,"used":2}
```

### 1.4 `.patch` — a second stable carrier

```
$ curl -sS -L --max-time 60 -o /tmp/r18-pr9348.patch  https://github.com/NationalSecurityAgency/ghidra/pull/9348.patch
HTTP:200 bytes:9115   rc=0
$ curl -sS -L --max-time 60 -o /tmp/r18-pr9348-2.patch https://github.com/NationalSecurityAgency/ghidra/pull/9348.patch
HTTP:200 bytes:9115   rc=0
ae5dc2e3e28f3f64feb32ba7df9659626a5173328b83a6b5e3914fcfa3b70a11  r18-pr9348.patch
ae5dc2e3e28f3f64feb32ba7df9659626a5173328b83a6b5e3914fcfa3b70a11  r18-pr9348-2.patch
PATCH_BYTES_IDENTICAL=yes
```

**Observation:** the patch lists three commits, head last: `1aa79ff…` → `a94872c…` → `a2143554…`
(`[PATCH 1/3] Golang: don't let one bad type abort all type markup`, `[PATCH 2/3] …reject out-of-bounds rtti name
offsets…`, `[PATCH 3/3] Golang: resolve stripped 1.24/1.25 maps as SwissMapType`). The head sha agrees with the API
field and with the page's embedded `"headSha"`.

## 2. API record (observed fields, `api3.json`)

| field | value |
|---|---|
| `title` | `Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries` |
| `state` | `open` |
| `merged` | `false` |
| `draft` | `false` |
| `merged_at` | `null` |
| `head.sha` | `a214355498e84aa86280be0c31c955aaf94f2d12` |
| `updated_at` | `2026-08-31T11:56:44Z` |
| `created_at` | `2026-07-05T12:12:29Z` |
| `closed_at` | `null` |
| `commits` | `3` |
| `head.ref` / `head.repo` | `fix/golang-stripped-type-markup-master` / `kubrickfr/ghidra` |
| `base.ref` / `base.sha` | `master` / `b070495c0bdfe96b12469550a9bc76131f6c4dd7` |
| `user.login` | `kubrickfr` |
| `comments` / `review_comments` / `changed_files` | `7` / `0` / `3` |
| `body` | 3696 chars, sha256 `b61c3faeff1c20f8394a2eaae4b1f6a4828e47736f57edf7034ec48a4b75e0f5` |

**Calibration trap (observed):** `merge_commit_sha` is **non-null** (`b25164e7173a8539810025a944ba328ba37b41d1`)
while `merged` is `false` and `merged_at` is `null`. Any check that infers merge from a non-null `merge_commit_sha` is
wrong for this PR; **`merged`/`merged_at` are the authority** (inference: that sha is GitHub's ephemeral test-merge
commit, not a landed merge).

**Corroboration (observation):** the page's last `<relative-time datetime="2026-08-31T11:56:44Z">` equals
`updated_at`; the page's embedded JSON also carries `"state":"OPEN"`, `"mergedTime":null`, `"mergeCommitSha":null`,
`"headSha":"a2143554…"`, `"commitsCount":3` — the API and the page agree on PR facts while disagreeing on digest.

## 3. Instability anatomy (depth)

Normalization ladder applied to all four saved pages; digest is sha256 of the transformed bytes:

| layer | normalization | fetches 1–3 | fetch 4 | residual |
|---|---|---|---|---|
| N0 | none | 3 distinct | distinct | — |
| N1 | 5 meta tokens + `authenticity_token` | equal (`e84007e8…`) | `7ab107ae…` | `fetch-nonce`, DOM ids, channel tokens |
| N2 | + `fetch-nonce`, `data-nonce`, `(icon-button\|tooltip\|label)-<hex>` ids, `aliveChannel`/`markAsReadChannel`/`data-channel` | equal (`9fd89164…`) | `761afb50…` | 8 lines |
| N3 | + channel-token shape `[A-Za-z0-9+/]{20,}={0,2}--[0-9a-f]{40,}` + `partial_last_updated` | equal (`b78a09be…`) | `cf7cbefb…` | 2 lines |

**Observation (N3 residual, byte-identical structure):** the only remaining difference is the repository's own
**open pull-request counter**, `"count":542` → `543` in `react-partial.embeddedData` and the same `542` → `543` in the
rendered nav `CounterLabel`. Someone opened a PR in `NationalSecurityAgency/ghidra` between fetches.

**Observation:** the per-request tokens are signed channel blobs whose decoded payload is
`{"c":"<channel>","t":<unix epoch>}` plus `--<hmac>`; the epoch advanced `1792509898` → `1792510186` (fetch 1 vs 4).
`<meta name="fetch-nonce" content="v2:<uuid>">`, 20 lines carrying `authenticity_token`, and generated element ids
(`icon-button-<uuid>`, `tooltip-<uuid>`, `label-<hex>`) are minted per request.

**Inference (firm):** no page-level content digest can be stable. Even after removing every per-request artifact, the
page embeds **repository-wide mutable counters**, so the noise floor is real repo state. The R17 practice of recording
a page sha256 as the anchor is unfixable by more regex; the anchor has to move to the head sha (and optionally the API
JSON digest, which was byte-identical on two fetches).

## 4. Operability prescription

For `W18/tools/routed-defects.py` and any later recheck of S032/S033:

1. **Identity = `head.sha`**, not page bytes. Recheck succeeds when the API's `head.sha` still equals
   `a214355498e84aa86280be0c31c955aaf94f2d12`; report `state`, `merged`, `updated_at` alongside.
2. **Artifact digest = API JSON** (`23035` bytes, `5ce7947f…` at this fetch) or the `.patch` (`9115` bytes, `ae5dc2e3…`).
   Both were byte-identical on repeat; either is a legitimate content carrier.
3. **Page digest may be recorded only as `fetch-time only`**, with the fetch instant, never as the row's anchor.
   A normalizing digest is *not* a fix: the N3 residual is repo state.
4. **Quota discipline:** unauthenticated GitHub REST is 60/h **per egress IP** (`179.218.13.209` was exhausted by
   earlier traffic at 15:25Z, reset 15:29:00Z). Sibling seats share this budget; prefer the two non-API carriers
   (`.patch`, page) for repeat checks. `curl -6` failed (`rc=6`, `Could not resolve host`), so there is no IPv6
   side-channel.

## 5. S033 draft row (11 columns, ready for L1 to append at `corpus/SOURCES.md` after line 38)

```
| S033 | Ghidra pull request #9348, swiss-map Go 1.24/1.25 recovery — https://github.com/NationalSecurityAgency/ghidra/pull/9348 (REST `https://api.github.com/repos/NationalSecurityAgency/ghidra/pulls/9348`; `…/pull/9348.patch`) | community | B | Candidate mechanism for the aether symbol-markup EOF, re-pinned on the REST record and the PR head rather than on rendered-page bytes | REST 2026-10-20T15:29:08Z, 23035 bytes, sha256 `5ce7947f079258beff8a6f186891c6124142a393cd69e67626b97df4bc27b025` (byte-identical on a second fetch): title `Golang: recover symbols from stripped Go 1.24/1.25 (swiss-map) binaries`, state `open`, merged `false`, head sha `a214355498e84aa86280be0c31c955aaf94f2d12`, updated_at `2026-08-31T11:56:44Z`; rendered-page sha256 is fetch-time only — 4 fetches, 403382 bytes each, 4 distinct digests (`ef473358…`, `21b719b0…`, `ddc27335…`, `43a47511…`), and the page serves no ETag or Last-Modified | supersedes S032 — the mechanism stands but the page digest it recorded (`436c0f63…`) is not reproducible, because the rendered page re-signs channel tokens with a per-request epoch (`{"c":…,"t":<unix>}`), mints `fetch-nonce`/CSRF/DOM-id UUIDs, and embeds a repo-wide open-PR counter (observed 542 then 543), so identity must ride the head sha. Body quote (17 words, body line 13): "…a default-built 1.24/1.25 binary emits the 112-byte `SwissMapType` layout, so the struct is under-read by 24 bytes". | mined | 2026-10-20 | 90d | corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md, corpus/lessons/round-17.md |
```

Row self-check (run against the block above, observed):

- 11 pipe-separated cells, matching `corpus/SOURCES.md:5` header and S032's own width (11).
- teaches cell starts with `supersedes S032 —` (U+2014 em dash, no space before it) — satisfies
  `contract.md:44-45`.
- anchor cell contains the literal `fetch-time only`, the API title, `state open`, `merged false`, and the head sha —
  satisfies the same check and gives the reader the stable identity first.
- quote is a contiguous substring of the PR body as returned by the API (`body` line 13, verified with a literal
  containment test), 17 words ≤ 25, no `|` characters so the table stays parseable.

**L1 decisions left open (not taken here):** whether to also re-status S032 (the observed status vocabulary is only
`mined` (30 rows) and `rejected` (2 rows); there is no `superseded` token, so S032 likely stays `mined` and S033 carries
the supersession), and whether `used-by` should point at `corpus/lessons/round-18.md` instead of the R17 pair.

## 6. Limits and remaining unknowns

- **One API sample pair, not a time series.** The API JSON was identical on two fetches seconds apart; stability across
  hours/days is unproven. `updated_at` is the API's own field, so it is the right thing to compare, not bytes.
- **Page sampling window ≈ 4 minutes.** The 542→543 counter change is observed, not explained; it is consistent with an
  unrelated PR being opened upstream (inference).
- **Comments were not independently paged.** The rendered page showed 6 comment bodies; `comments: 7` counts issue
  comments (the PR description is not one), so the two numbers are not the same quantity (inference).
- **No tool installed or upgraded** during this seat (nothing was needed; `curl`, `python3`, `jq`, `sha256sum`, `cmp`
  were already present).
