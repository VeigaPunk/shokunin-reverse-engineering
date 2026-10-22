# C2 — openchain lookup is now served by Sourcify (S076)

Seat KaidokuR25a3.C2SourcifyService. Round 25 attempt 3, wave 1. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, read-only except this report. Live HTTP (curl) only, no browser, no bot challenge. Seat artifacts under `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2SourcifyService/`.

## Verdict — both halves hold

1. **Identical results: holds.** For all 10 selectors, `api.openchain.xyz` and `api.4byte.sourcify.dev` return **byte-for-byte identical** bodies (same sha256, same `ETag`, same `content-length`); headers are identical apart from the volatile `date`, `x-cloud-trace-context`, `alt-svc`.
2. **Migration claim is sourced — but not by S076 as anchored.** The takeover is stated by Sourcify itself in two primary places (A, B below). **S076 does not carry that statement**: `api.4byte.sourcify.dev/api-docs/swagger.json` asserts *compatibility* ("This API maintains compatibility with openchain.xyz behavior"), not the takeover. The entry sentence "The openchain lookup, now served by Sourcify (S076)" attributes the migration to a source that does not state it. The claim is true; the citation needs a second source.

## Primary statements of the migration (opened 2026-10-22)

**A. Sourcify blog — "Sourcify 2025 Recap"**, section `4byte.sourcify.dev`, `https://docs.sourcify.dev/blog/recap-2025/` (`datePublished` `2025-12-17T00:00:00.000Z`):

> "We took over the most popular 4byte signature service openchain.xyz's database and API."

and later in the same section:

> "We implemented the exact openchain API and now Sourcify serves all signature requests to openchain.xyz as well."

**B. Live site banner** at `https://4byte.sourcify.dev/` (the page `https://openchain.xyz/` 301-redirects to), site-wide top banner:

> "Sourcify is taking over openchain.xyz API. Please switch to api.4byte.sourcify.dev (same API)."

**C. Secondary, same publisher** — "Spam or Legit? Analyzing 4byte Selector Collisions", `https://docs.sourcify.dev/blog/signatures-analysis/` (`datePublished` `2025-10-30`), first paragraph:

> "Recently Sourcify took over openchain.xyz's 4byte signature APIs as well as the domain itself, maintained by @samczsun."

## Observation: the openchain host now serves the Sourcify API itself

`https://api.openchain.xyz/api-docs/swagger.json` → HTTP 200, sha256 `896d6a30b58d501f508f8d311da0c81cdd6d006ed66f3e371142794101fcc00b` — **identical bytes** to `https://api.4byte.sourcify.dev/api-docs/swagger.json` and to the lane's saved `corpus/evidence/round-25/a3/sources/sourcify-4byte-swagger.json` (same sha256). Its `info.title` is "Sourcify Ethereum Function, Event, and Error Signatures API", `info.contact.name` "Sourcify".

Infrastructure (observation): `api.openchain.xyz`, `api.4byte.sourcify.dev`, `openchain.xyz`, `4byte.sourcify.dev` all resolve to the single A record `34.54.86.181`; each returns `server: Google Frontend`, `x-powered-by: Express`, `via: 1.1 google`; TLS issuer Google Trust Services WR3 for all four, distinct per-host CNs.

## Measurement: 10 selectors, both hosts

Command (per selector, per host; `sleep 1.2` between requests to a host; no `-L`, so a redirect would surface as a `Location` header, not be followed):

```
curl -sS -o <body> -D <headers> -w '%{http_code}' -H 'accept: application/json' \
  -H 'user-agent: kaidoku-r25-a3-C2SourcifyService/1.0' --max-time 30 \
  "https://<host>/signature-database/v1/lookup?function=0x<sel>&filter=false"
```

Selectors `6e8efde2, 2e1a7d4d, a9059cbb, 23b872dd, 095ea7b3, 70a08231, 0c751377, 3efdef66, dd62ed3e, 8456cb59` (all from the lane's 43-selector carrier set). Fetch window 2026-10-22T10:43:02Z–10:43:32Z, all HTTP 200, exit 0.

| selector | body sha256 (identical on both hosts) | status openchain/sourcify |
|---|---|---|
| 6e8efde2 | `677680a0cde168a16e1c8444a56cb6052c3fd6ac629830c6162598dbfe6def20` | 200 / 200 |
| 2e1a7d4d | `48d08290066ee1625bfb138d0b64fc5167d6681432525eb8789fb5c5e11b3077` | 200 / 200 |
| a9059cbb | `f20961e3557f0e70c853a732542cd8cc3d79735c2c0fb7b15032fac7b302bd43` | 200 / 200 |
| 23b872dd | `f76eb47b8828a38231579f690e717f6e59b5b8e4ebaa8c7170bc7cd806a8f1be` | 200 / 200 |
| 095ea7b3 | `9fef7b82b077949b31f9c3fb3c265f620a5dfe89be54326378cc6e6ab80447ff` | 200 / 200 |
| 70a08231 | `319d450f3fa1eb43df936ec0ac21a57226667ca4b0b3892e9e6562aaef2b31e` | 200 / 200 |
| 0c751377 | `8a5a16c2f0482cda907655ed69cba4270814c937019aa326ebf60ab1b2a7f83d` | 200 / 200 |
| 3efdef66 | `8a928f77f539f91950d409b0979fdd1af20401c7e40b70e076d5eeb8b9122b57` | 200 / 200 |
| dd62ed3e | `1804e7ca3b3e93f80f12adaa531d3ea2f156d71f5f5c4c8358508185a15f6b48` | 200 / 200 |
| 8456cb59 | `e4053aa94d146c787ac35e84a140c4bc382a13f89eb31c5af3961662259587ea` | 200 / 200 |

**Zero redirects on the API path:** no `Location` header on any of the 20 lookups; `num_redirects=0`, first hop 200. The bare domain does redirect: `curl -sS -L -o /dev/null -w '%{url_effective} %{http_code} %{num_redirects}' https://openchain.xyz/` → `final=https://4byte.sourcify.dev/ code=200 redirects=1`, first hop `HTTP/2 301`, `location: https://4byte.sourcify.dev/`.

**Headers** (openchain vs sourcify, 10/10 pairs): after dropping `date`, `x-cloud-trace-context`, `alt-svc`, the header sets are **identical** for every selector — `x-powered-by: Express`, `access-control-allow-origin: *`, `cache-control: public, max-age=60, s-maxage=3600`, `content-type: application/json; charset=utf-8`, same `etag` (e.g. `W/"89-zikREXutGXX/J+C4JllDg40ezGU"` for `6e8efde2`, `W/"7c-X0ejQZDz9a1yE3xFPaKWMQOVrNk"` for `8456cb59`), same `content-length`, `server: Google Frontend`, `via: 1.1 google`. Identical ETag on both hostnames is direct evidence of one origin serving both.

**Scope beyond the 10 selectors** (extra probes, byte-identical across hosts): `GET /signature-database/v1/stats` sha `dce6ba0d027a931f1814f7320200998409ab3431817595d7f43cfb46f579f74c`; `GET .../lookup?function=0xa9059cbb&filter=true` sha `1874fa3d62048d9229251610c80821f45ae1578d356b532a85e3b965682a83dd`; `GET .../lookup?event=0xddf252ad…` sha `22606285d25b78fb…`; `GET .../lookup?error=0x08c379a0` sha `dede645a4953c13e…` (both `{"ok":true,"result":{"function":{},"event":{}}}`). Both hosts 404 on `/v1/graphql` and `/v1/blockchain/1`; `api.openchain.xyz/` root 404s — the migration covers the 4byte signature service, not the whole openchain API surface. **Unknown:** whether other non-4byte openchain endpoints now answer elsewhere.

**Cross-check against the lane's a2 snapshot.** For all 10 selectors the fresh `api.openchain.xyz` body sha256 equals the sha256 recorded in `corpus/evidence/round-25/a2/c2/*/db/manifest.json` for the a2 openchain entry (e.g. `a9059cbb`: a2 `f20961e3…` at 2026-10-22T08:30:37Z = fresh 10:43:08Z). The a2 evidence is stable over the ~2 h window and remains valid: the a2 "openchain" lookups are byte-identical to what Sourcify's host returns.

## Risks / scoping notes for the entry

- S076 supports *compatibility*, not *migration*. Recommend adding a source row for the Sourcify 2025 Recap post (or the live banner) and citing it for the takeover sentence, keeping S076 for the `filter` and `filtered`/`hasVerifiedContract` flags as it is used.
- The entry's "openchain responses were requested with `filter=false`" stays accurate — those requests hit `api.openchain.xyz`, which now answers from Sourcify's backend, so the saved a2 evidence equals a Sourcify-host request.
- The entry's "Limits" bullet "Both databases take public submissions, so a later lookup can add a colliding or junk entry" is **strengthened**: the two hosts are one database, so 4byte.directory and openchain/Sourcify are not independent witnesses. The "two databases" framing in the entry's measured procedure (4byte.directory vs openchain) still holds — 4byte.directory is a separate service — but openchain and Sourcify are the same one.
- **Unknown / could-not-evaluate:** the exact cutover date. The earliest Sourcify statement opened is dated 2025-10-30 ("Recently Sourcify took over…"); no dated cutover announcement was found in the pages opened. `blog.sourcify.dev` does not resolve on this host (DNS failure), so no standalone Sourcify blog domain was opened; the blog is served under `docs.sourcify.dev/blog/`.

## Seat artifacts (sha256)

All under `/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2SourcifyService/`. `ARTIFACT_SHA256SUMS.txt` enumerates all 66 files with their sha256. Selected:

| file | sha256 |
|---|---|
| `manifest.json` (20 fetches: url, status, utc, body sha, headers sha, server, location) | `8b7fe35456571ed5083c273fc7f79fa9282c0d6a40251c57e15d1b7f9cc72f50` |
| `extras.json` (11 extra-endpoint bodies) | `1ac7d44b50fb41fec452033e3b2b7a436b0688a4c3e11429f867cece3e64b88e` |
| `fetch.sh` (fetch script) | `b016fd505c12582500ff62e81a878ce00ebf7781b73d15b01ae121f1ad3cfb64` |
| `sel10.txt` (the 10 selectors) | `8362988ade01b8b8f0a036b3a39b4be16c6fae5c6d5b87ff3487f1587814814c` |
| `raw/openchain-*.json` + `raw/sourcify-*.json` (20 bodies) | per-selector sha256 in the table above |
| `raw/openchain-*.headers.txt` + `raw/sourcify-*.headers.txt` (20 header sets) | per-fetch `headers_sha256` in `manifest.json` |
| `pages/docs.sourcify.dev_blog_recap-2025_.html` (statement A) | `9b5c4f9eeee7232f0c7365a71ff095c4b77f8083f0d81586205be6aa45da8b21` |
| `pages/docs.sourcify.dev_blog_signatures-analysis_.html` (statement C) | `f2efd1c72cf130e81052c38d1b67782728c92ad62b7f8f6948d68579463d2cfd` |
| `pages/openchain.xyz_.html` (banner B, after the 301) | `1b39296a333952b097a08e9b623a972a6c053415c52ac061b72065d8b3f44f4f` |
| `pages/swagger.json` (the S076 document) | `896d6a30b58d501f508f8d311da0c81cdd6d006ed66f3e371142794101fcc00b` |
| `pages/docs.sourcify.dev_docs_api_.html` (Sourcify API docs page) | `a5e796d72c7439d8310e6d34fcf6c7a0bc71c05a68bf9bde265cb1f65c8afa48` |

## Commands, exits and times (2026-10-22)

- 20 lookups (10 selectors × 2 hosts): exit 0, HTTP 200, 10:43:02Z–10:43:32Z.
- `curl -sS -L -w` on `https://openchain.xyz/`: exit 0, 1 redirect, final 200 (10:44Z).
- `getent hosts` / `socket.getaddrinfo` for the four hostnames → `34.54.86.181` (10:47Z).
- `openssl s_client` cert subject/issuer for the four hostnames: exit 0 each (10:48Z).
- Page fetches (10:44Z–10:48Z): `docs.sourcify.dev/docs/api/` 200; `/blog/` 200; `/blog/recap-2025/` 200; `/blog/signatures-analysis/` 200; `/blog/roadmap-2025/` 200; `/docs/repository/signature-database/` 200; `sourcify.dev/blog` 404; `blog.sourcify.dev/` exit 6 (DNS: could not resolve host); `www.openchain.xyz/` exit 6 (DNS); `docs.sourcify.dev/docs/signatures-database/` 404 and `/docs/api/api/` 404 (same 404 body, sha `30bd0f73…`).
- Extra endpoint probes (10:45Z–10:52Z): all exit 0, HTTP 200 except the two 404s noted.

## Tools

No tool installed or upgraded. `curl 8.23.0` (system, OpenSSL 3.6.5), `python3 3.14.8`, `openssl` (system) sufficed; the REA CLI was not needed since this card asks only about the two lookup hosts and the migration statement. Total HTTP requests from this seat ≈ 50, to `api.openchain.xyz`, `api.4byte.sourcify.dev`, `openchain.xyz`, `4byte.sourcify.dev`, `docs.sourcify.dev`, `sourcify.dev` — under the 120 per-seat cap, with ≥1.2 s spacing between requests to a host. No lane file was written except this report; no git/jj write command was run.

Report: .ufo/waves/round-25/a3/w1/C2SourcifyService.md
