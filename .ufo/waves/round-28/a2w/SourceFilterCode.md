# R28-C2 source row — Sourcify 4byte filterResponse (S084)

Seat KaidokuR28a2.SourceFilterCode, written 2026-10-22T18:27Z. Read only on the lane; nothing
written there except this report. No openchain or 4byte.directory lookup was made; none was in my
item.

## Verdict

The rule frozen in claims-c2.json is the complete rule in the code: **holds**. In services/4byte/src
at commit 189cd726 the only place that gives `filtered` a computed or true value is handlers.ts:47-48,
and its condition is exactly "the selector is a key of the canonical list and the candidate's name
differs from that key's signature". No counterexample exists in the source; the notes below are
precision, not exceptions on this claim's data.

## Source record (opened 2026-10-22)

- URL: https://raw.githubusercontent.com/argotorg/sourcify/189cd726f7ed8fb3d2f503402d5c133e0f50e1fd/services/4byte/src/api/handlers.ts
- Opened by plain `curl 8.23.0` GET (no browser, no challenge) at 2026-10-22T18:23:18Z: `http=200
  bytes=14637`, 471 lines, sha256 `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38`.
- Cross check 2026-10-22T18:25:20Z: `git cat-file blob 189cd726…:services/4byte/src/api/handlers.ts |
  sha256sum` in the L1 sparse checkout (HEAD is exactly that commit) returned the same sha256, exit 0,
  so the served bytes are the committed blob, not a moving branch.
- The pinned list corpus/evidence/round-28/c2/canonical-signatures.json hashes
  `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2`, equal to the commit's
  services/4byte/src/utils/canonical-signatures.json (both hashed 2026-10-22T18:23Z).
- Located quote, lines 47-48, copied from the served bytes; the statement spans a line break and the
  indentation is the file's, no words changed (5 words):
  `          signatureItem.filtered =`
  `            signatureItem.name !== expectedCanonical.signature;`
- `function filterResponse(response: SignatureResult, shouldFilter: boolean) {` is line 39 and the
  closing brace is line 66. Range **:39-66**.

## Every assignment to `filtered` in services/4byte/src at that commit

From `grep -n filtered` over the served bytes (5 hits) and
`git grep -c -E '\.filtered|filtered:' 189cd726 -- 'services/*/src/**'` (only
services/4byte/src/api/handlers.ts:5 and services/4byte/src/openapi.yaml:9; no other service in the
repository carries the token), both 2026-10-22T18:25:20Z, exit 0.

- api/handlers.ts:20 — declaration `filtered: boolean;` in `SignatureItem`; type, not assignment.
- api/handlers.ts:47-48 — the computed assignment; the only producer of a true value.
- api/handlers.ts:61 — read only, the predicate `!signatureItem.filtered` of the `shouldFilter` drop.
- api/handlers.ts:90 — `filtered: false` initializer in `mapLookupResult`.
- api/handlers.ts:262 — `filtered: false` initializer in `searchSignatures`.
- api/openapi.yaml:76, 80, 85, 89, 155, 158, 163, 469, 484 — specification examples, not code.
- test/integration/4bytes-api.spec.ts:195 — assertion `{ name: collusionSignature, filtered: true, … }`;
  a test expectation, not production code.
`filterResponse` has two callers: handlers.ts:223 (`lookupSignatures`) and handlers.ts:279
(`searchSignatures`). None other exists in the service.

## Why the rule is complete (observation, from the served bytes)

`filterResponse` walks `function` then `event`; for each hash whose key is in the canonical map and
whose entry is not null it sets every candidate's flag to `name !== expectedCanonical.signature`
(:44-49). The `shouldFilter` block (:54-65) only removes the marked candidates and never writes the
flag. Every candidate is built with `filtered: false` (:90 lookups, :262 search), so an unmarked
candidate keeps false. That is the frozen rule in both directions.
## Precision notes (no prediction changes on the 230 selectors)

1. The assignment is guarded by `expectedCanonical !== undefined && response[type][hash] !== null`
   (:45). A null entry holds no candidates, so the guard cannot be observed in a response.
2. Five of the 36 canonical keys carry no `signature` field and are marked `source: system:magic`:
   0x60806040, 0x60a06040, 0x60c06040, 0x60e06040, 0x61010060. For these the comparison is
   `name !== undefined`, so every candidate is marked. None of the 230 selectors is one of the five
   (awk over selectors.tsv, 2026-10-22T18:24Z, 0 each), and the counter's `c.get("signature")` gives
   None, so counter and code agree here regardless.
3. `searchSignatures` pushes one candidate object into both `function[hash4]` and `event[hash32]`
   (:261-272). If both hashes are canonical, the later `event` pass overwrites what the `function`
   pass set. Still only :47 assigns, so it is not a second rule, but the search endpoint's final flag
   depends on the last matching pass. The lookup path R28-C2 tests builds a fresh object per hash, so
   it has no aliasing.
4. The canonical lookup is exact string matching on the requested hash; handlers.ts has no
   `toLowerCase` and all 36 keys are lowercase 10-character strings, so an uppercase query would
   silently miss. The claim's selectors are lowercase, so this is moot for R28-C2.
5. `sanitizeFilter` (:105-110) defaults to true when `filter` is absent, so the flags are visible only
   with `filter=false`, which the claim's URL sends.

## Lane row

S084 already exists in corpus/SOURCES.md at HEAD `9db24c9e` (the working tree also holds another
seat's uncommitted search-log lines; I did not touch it). Its fields match all of the above: URL with
the commit, sha256 `30981efb…c5a38`, `filterResponse` `:39-66`, assignment `:47-48`, and the rule
sentence. No correction is required. If note 2 is to be reflected, the minimal addition to the anchor
column is "5 of the 36 keys (`system:magic`) carry no `signature`, so every candidate for them is
marked"; optional, and it changes no prediction.
## Evidence, artifacts, tooling, unknowns

Artifacts under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/SourceFilterCode/, sha256 from `sha256sum`
2026-10-22T18:25:20Z:

- `raw/handlers.ts` — served bytes, `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38`
- `raw/handlers.headers` — HTTP/2 200 headers, `5caa30c17a325e25b1f612b0590a20a8feaca45b6518287f588e09c7e9999349`
- `evidence.log` — timestamped commands, outputs and exit codes behind every line above

No installs or upgrades. Used `curl 8.23.0`, `git 2.56.0` (read-only cat-file, grep and rev-parse in
the L1 checkout), `python3 3.14.8`.

Unknowns: which revision answers api.openchain.xyz in production (not shown by this code, not tested
here); result ordering and `hasVerifiedContract` (outside this row's scope).
