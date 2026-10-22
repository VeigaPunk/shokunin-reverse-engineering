# Round 25 attempt 3, wave 1 — LessonGateDraft (S075–S077 Gate lines)

Scope: reopen the three source pages behind registry rows S075–S077 and draft one
Gate line each (row id, URL, access date, one located quote of at most 25 words,
section). Lane read-only; nothing in the lane was edited except this report file.

## Gate lines (drafted)

| row | URL | access date | located quote (≤25 words) | section |
|---|---|---|---|---|
| S075 | https://www.4byte.directory/docs/ | 2026-10-22 | "If the provided query is exactly 4 bytes long then results are filtered by exact match." | Signatures > Filtering on `hex_signature` |
| S076 | https://api.4byte.sourcify.dev/api-docs/swagger.json | 2026-10-22 | "Whether or not to filter out junk results" | `/signature-database/v1/lookup` > `filter` query parameter |
| S077 | https://raw.githubusercontent.com/cdump/evmole/master/agent/skills/evm-bytecode-analysis/references/interpretation.md | 2026-10-22 | "A selector is a four-byte dispatch value found by static bytecode analysis. It does not supply a verified function name." | Evidence and inference |

Word counts 16 / 8 / 20. Each quote is verbatim in the reopened page (whitespace
normalized for the Markdown-wrapped S077 passage).

## Commands and outcomes (all UTC 2026-10-22)

Plain HTTP fetch, one request per host, ≥1.2 s between hosts:

```
UTC 2026-10-22T10:43:40Z fetch https://www.4byte.directory/docs/
http=200 bytes=16524
65e0de89a7fc421e2fd96f9b70d1c6859731d1a8c211b860be8e9fe59d93f5c9
UTC 2026-10-22T10:43:42Z fetch https://api.4byte.sourcify.dev/api-docs/swagger.json
http=200 bytes=13346
896d6a30b58d501f508f8d311da0c81cdd6d006ed66f3e371142794101fcc00b
UTC 2026-10-22T10:43:44Z fetch https://raw.githubusercontent.com/cdump/evmole/master/agent/skills/evm-bytecode-analysis/references/interpretation.md
http=200 bytes=2209
fba49f8284e4b5efce67254034c58d1858b35c36ea51d0dc2baefa50c4ade955
```

Exit code 0 for every fetch. A second, independent fetch 1.2 s later of each URL
returned byte-identical digests. The S076 digest equals the digest already
recorded in row S076 (`896d6a30…cc00b`) and the lane's saved copy
`corpus/evidence/round-25/a3/sources/sourcify-4byte-swagger.json`
(`sha256sum` → `896d6a30b58d501f508f8d311da0c81cdd6d006ed66f3e371142794101fcc00b`).

Reopen check (quote present, ≤25 words, section found) —
`python3 -I -B /fast/scratch/hyaku/kaidoku-r25-a3/seats/LessonGateDraft/verify_gate.py`,
exit 0:

```
S075 quote_present=True words=16 within25=True section_found=True -> OK
S076 quote_present=True words=8 within25=True section_found=True -> OK
S077 quote_present=True words=20 within25=True section_found=True -> OK
```

## Verdicts

- **S075 holds.** The 4byte.directory API documentation is live (HTTP 200) and
  carries the quoted hex_signature rule verbatim. Observation: the page's
  `Signatures` section defines the `Signature` model (`id`, `text_signature`,
  `bytes_signature`, `hex_signature`), `Filtering on hex_signature` states the
  4-byte exact-match rule, and `Creating Signatures` documents POST
  `/api/v1/signatures/` — so the row's "signature model, hex_signature filter
  and public signature submission" scope is located on the page.
- **S076 holds.** The OpenAPI file is live (HTTP 200), `info.version` is
  `1.0.0`, the `filter` parameter of `/signature-database/v1/lookup` carries the
  quoted description, and `components.schemas.SignatureResponse` gives each
  match `name`, `filtered` and `hasVerifiedContract`. The "linked from" clause
  also holds: https://docs.sourcify.dev/docs/api/ (opened 2026-10-22T10:45:21Z,
  HTTP 200, sha256 `a5e796d72c7439d8310e6d34fcf6c7a0bc71c05a68bf9bde265cb1f65c8afa48`)
  links "OpenAPI JSON spec for 4byte (Signature) Service API Documentation" to
  exactly that URL (2 occurrences).
- **S077 holds.** The EVMole interpretation reference is live (HTTP 200) and the
  `Evidence and inference` section carries the quoted passage. The same section
  adds "Argument types are likely ABI types inferred from calldata use" and
  "Never resolve selectors to names without a separately authorized signature
  source", which is the support the row and the knowledge entry rely on.
- **Consistency with the landed lesson holds.** `corpus/lessons/round-25.md`
  (attempt 3 `### Gate`) already carries the same three quotes for S075–S077;
  my independent reopen reproduces them exactly, so the lesson's Gate table needs
  no change from this seat.

## Findings (for the L1; both are wording, not substance)

1. **S075's "no result order" clause is silence, not a stated rule.**
   Observation: the reopened page contains zero occurrences of "order", "sort",
   "rank" or "priority" (case-insensitive, over the whole 16 524-byte HTML; the
   only `ord` hits are inside the word "record"). The page documents pagination
   but never a result order. Row S075's bounded-support cell says "the
   documentation states no result order", and the knowledge entry says "Its
   documentation states no result order." Read literally, that asserts the page
   makes a statement it never makes; the supportable wording is that the
   documentation is silent on order, so a first result carries no ranking
   guarantee. Verdict: **fails as literally worded**, holds as an inference.
   The lesson's own Gate quote for S075 is unaffected, since it quotes the
   filter rule instead.
2. **S077's cell attributes REA to EVMole's own document.**
   Observation: `interpretation.md` never mentions REA. The claim "REA's EVM
   provider is EVMole" is supported instead by the lane's REA replay envelopes
   (`corpus/evidence/round-25/a3/c2/rea-replay/*.json` contain `evmole@0.9.3`
   and `evmole-interface`). Verdict: the row's source supports EVMole's own
   wording; the REA attribution needs the envelope citation beside it.

Neither finding changes a Gate line, and neither is a lane edit — the L1 owns
the wording.

## Out of scope

No REA run, no lookup, no tally, no lane file edited, no commit, no jj command.
The C1/C2 claims, the resolver, the tally and the other wave-1 members'
surfaces were not touched. No tooling was installed or upgraded (no pacman, uv,
npm or cargo action), so there is nothing to record on that axis.

## Artifacts (all outside the lane)

| path | sha256 |
|---|---|
| `/fast/scratch/hyaku/kaidoku-r25-a3/seats/LessonGateDraft/verify_gate.py` | `b8975fb0c56855639b4af06fc3b5dce0b9a817b978b011210493e7a09a78be99` |
| `.../raw/4byte-docs.html` | `65e0de89a7fc421e2fd96f9b70d1c6859731d1a8c211b860be8e9fe59d93f5c9` |
| `.../raw/sourcify-swagger.json` | `896d6a30b58d501f508f8d311da0c81cdd6d006ed66f3e371142794101fcc00b` |
| `.../raw/evmole-interpretation.md` | `fba49f8284e4b5efce67254034c58d1858b35c36ea51d0dc2baefa50c4ade955` |
| `.../raw/sourcify-api-docs.html` | `a5e796d72c7439d8310e6d34fcf6c7a0bc71c05a68bf9bde265cb1f65c8afa48` |

`...` = `/fast/scratch/hyaku/kaidoku-r25-a3/seats/LessonGateDraft`.

Report: .ufo/waves/round-25/a3/w1/LessonGateDraft.md
