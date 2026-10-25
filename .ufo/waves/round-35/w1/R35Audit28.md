# R35Audit28 — Retry S117 DOI and classify access

- Seat: R35Audit28 (scribe, leaf member — no subagent dispatch)
- Date: 2026-10-25
- Item: retry S117 DOI (`https://doi.org/10.1109/SP46214.2022.9833799`) and classify access
- Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only; report only write)
- Milestone: build evidence and first falsifications

## 0. Target row (source fleet)

Row `S117` (kaidoku, round 1) is defined in the source fleet's proposal
`lanes/kaidoku/SOURCES-PROPOSED.md` (Gate — S117):

- URL: `https://doi.org/10.1109/SP46214.2022.9833799` (IEEE S&P 2022 SoK,
  *SoK: Demystifying Binary Lifters Through the Lens of Downstream Applications*,
  Liu/Yuan/Wang/Bao, pp. 1100–1119)
- Scope: abstract + publisher metadata only (body retrieval non-deterministic; see
  `REJECTIONS.md` / `CANNOT-ANSWER.md` §6)
- Quote to verify (Abstract): `four popular static and dynamic LLVM IR lifters that were developed by the industry or academia from a total of 252,063 executables`
- Register class: `unreachable` ("the cited source could not be fetched, so no quote was checked")
- Round-35 quarantine verdict (`.ufo/waves/round-35/assimilation/quarantine-verdicts.md`):
  `unverifiable` (unreachable, not fabrication) — "no quote checkable"

## 1. Retry evidence (all fetches 2026-10-25, read-only)

### 1.1 DOI resolution (with redirects)

```
$ curl -sS -o /dev/null -w 'status=%{http_code} type=%{content_type} size=%{size_download} redirects=%{num_redirects} url_final=%{url_effective}\n' \
    --max-time 60 -L -A 'Mozilla/5.0 ... Chrome/120.0' 'https://doi.org/10.1109/SP46214.2022.9833799'
status=202 type=text/html; charset=UTF-8 size=0 redirects=1 url_final=https://ieeexplore.ieee.org/document/9833799/
```

First hop (no follow):

```
$ curl -sS -o /dev/null -w 'first_status=%{http_code} redirect=%{redirect_url}\n' --max-time 40 'https://doi.org/10.1109/SP46214.2022.9833799'
first_status=302 redirect=https://ieeexplore.ieee.org/document/9833799/
```

Full chain:

```
HTTP/2 302
location: https://ieeexplore.ieee.org/document/9833799/
HTTP/2 202
final_status=202 final_url=https://ieeexplore.ieee.org/document/9833799/
```

### 1.2 Direct IEEE Xplore document page

```
$ curl -sS -o /tmp/r35_s117_ieee.html -w 'ieee status=%{http_code} type=%{content_type} size=%{size_download}\n' \
    --max-time 60 -A 'Mozilla/5.0 ... Chrome/120.0' 'https://ieeexplore.ieee.org/document/9833799/'
ieee status=202 type=text/html; charset=UTF-8 size=0
$ wc -c /tmp/r35_s117_ieee.html
0 /tmp/r35_s117_ieee.html
```

Result: identical to the quarantine's earlier attempt — **HTTP 202 with empty body**
(0 bytes) from ieeexplore, both via DOI and direct. The publisher wall is reproducible.

### 1.3 Metadata / open-access routes

| Route | Outcome |
|---|---|
| CrossRef `api.crossref.org/works/10.1109/SP46214.2022.9833799` | 200; title/venue/pages/published, license = IEEE STM ASF policy links (10.15223/policy-009/001); **no abstract** in record |
| Semantic Scholar graph API `.../paper/DOI:10.1109/SP46214.2022.9833799?fields=title,abstract,openAccessPdf,externalIds,url` | 200 (after one 429 rate-limit, retried ~8 s later); full abstract (2,313 chars); `openAccessPdf.status = CLOSED` (no OA PDF); externalIds: DBLP `conf/sp/LiuYWB22`, CorpusId 251144563 |
| arXiv `export.arxiv.org/api/query?search_query=all:"Demystifying Binary Lifters"` | 200, **0 entries** — no preprint copy |
| Unpaywall `api.unpaywall.org/v2/<doi>?email=…` | 422 — rejects placeholder email (API requires a real address); skipped; not needed for classification |

## 2. Quote checkability (falsification)

The row's gate quote was checked verbatim against the Semantic Scholar abstract
(publicly retrievable, no key):

```
$ python3 - <<'EOF'
import json, re
d = json.load(open('/tmp/r35_s117_s2.json'))
abs_ = d.get('abstract') or ''
q = 'four popular static and dynamic LLVM IR lifters that were developed by the industry or academia from a total of 252,063 executables'
print('quote_verbatim_present:', q in abs_)
EOF
quote_verbatim_present: True
```

- Abstract length: 2,313 chars (matches the wave-1 record's "2,523-character abstract" order of magnitude; exact length varies by API rendering).
- `openAccessPdf.status = CLOSED` — full text remains closed.

## 3. Access classification (verdict)

1. **Canonical URL (DOI/publisher):** `unreachable` — 302 → ieeexplore → HTTP 202 empty body (0 bytes). Reproducible today; unchanged from the quarantine's earlier attempt.
2. **Row-scoped content (abstract):** **verifiable-now** — the abstract is publicly retrievable via the Semantic Scholar graph API (200, stable), and the gate quote is present verbatim. This is the same channel the row's own `recheck` already uses (S2 API, measured `grep -c 'Binary Lifters'` → 1 on 2026-10-23).
3. **Full text (body):** closed access — no OA PDF (S2 CLOSED), no arXiv record, CrossRef license is IEEE STM (not free). Body quotes stay uncheckable without a subscriber copy (consistent with `CANNOT-ANSWER.md` §6).

Therefore: the quarantine line's premise "no quote checkable" is **falsified**; the recommended verdict for S117 moves from `unverifiable` → **verifiable-now (abstract channel), body closed** — the canonical DOI endpoint itself remains walled.

## 4. Touched surfaces

- Reads (read-only): lane `plans/round-35-claims.md`, `.ufo/waves/round-35/claims-canonical.json`, `.ufo/waves/round-35/assimilation/quarantine-verdicts.md`; source fleet `lanes/kaidoku/SOURCES-PROPOSED.md` (Gate S117), `REJECTIONS.md`, `CANNOT-ANSWER.md`, `SEARCH-LOG.md`, `KNOWLEDGE-PROPOSED.md`; shokuknow `.ufo/waves/corpus-expansion-1/absent-defect-register.md`.
- Private captures (only): `/tmp/r35_s117_ieee.html`, `/tmp/r35_s117_crossref.json`, `/tmp/r35_s117_s2.json` (0-byte IEEE page; JSON metadata).
- Writes: this report only (`.ufo/waves/round-35/w1/R35Audit28.md`). No lane production files, no VCS mutation.

## 5. Out-of-scope

- No lane writes beyond the report trailer; no corpus/counter/claim edits.
- No PDF/body retrieval attempted (closed); no subscriber/library route exists here.
- Unpaywall not usable (requires a real email); S2 singly rate-limited but succeeded on retry.

## 6. Limits / caveats

- S2 API is rate-limited (one 429 observed); retry with backoff if reused.
- Content-type/size of the 202: `text/html` but 0 bytes — no challenge page captured.
- The classification is advisory evidence; no predicate/scope altered.
