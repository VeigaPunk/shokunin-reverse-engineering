# ReviewManifestC2 — R28-C2 fetch manifest integrity (round 28, attempt 2)

Verdict: **holds**. Attacked: `corpus/evidence/round-28/c2/db/manifest.json` plus the 230 response
files beside it. No failure found in any of the six required checks.

## Ground checked before counting
- Frozen pins re-hashed 2026-10-22T18:24:55Z, command `sha256sum selectors.tsv collect-c2.py`,
  exit 0: selectors.tsv `ad1b50982922ed69…` equals the `loaded_by_counter` pin in frozen
  `.ufo/waves/round-28/claims-c2.json`; `tools/round-28/collect-c2.py` `0ea57ac5e66a9a53…` equals
  the `producers_not_counters` pin. Observation.
- The frozen URL pattern is the one built by the sha-pinned producer, collect-c2.py line
  `url = "https://api.openchain.xyz/signature-database/v1/lookup?function=0x%s&filter=false" % s`,
  one file `openchain-<selector>.json` per selectors.tsv row. Observation.
- Bytes reviewed are the committed bytes: `git diff HEAD --stat -- corpus/evidence/round-28/c2/db/`
  is empty (dirty_lines=0, exit 0, 18:25:11Z); `git show` sha256 of manifest.json is
  `bdfdea4f85605fb9…` at dispatch tip a2673116, at HEAD 9db24c9e, and in the working tree — all
  equal. The introducing commit a2673116 message says "230 responses + manifest, utc
  17:22:05Z-17:25:57Z, after freeze 86fa8526", matching what the file shows. Observation.

## Checks (command `python3 -I -B /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewManifestC2/verify_manifest.py`, exit 0, 2026-10-22T18:24:55Z)
1. Entry count: `entries=230 tsv_rows=230 tsv_sets=r25,r28-heldout` — 230/230 pass. Observation.
2. One per selector: exact bijection, `tsv=230 manifest_unique=230 missing=0 extra=0
   dupes_manifest=0 dupes_tsv=0`; every manifest file name is `openchain-<8 lower-hex>.json` and its
   embedded selector equals the one in its URL; selectors.tsv rows all valid 8-char lower hex under
   header `selector	set`; sets are r25 (43) and r28-heldout (187). 230/230 pass. Observation.
3. URL equals the frozen pattern: `url_ok=230 url_bad=0`, each URL byte-equal to
   `https://api.openchain.xyz/signature-database/v1/lookup?function=0x<its selector>&filter=false`.
   230/230 pass. Observation.
4. Status: `status200=230 status_bad=0`. 230/230 pass. Observation.
5. sha256 equals file bytes: each of the 230 db files re-hashed from disk; `sha_ok=230 sha_bad=0`.
   230/230 pass. Observation.
6. utc after freeze 2026-10-22T17:21:55Z: `utc_ok=230 utc_bad=0 min=2026-10-22T17:22:05Z
   max=2026-10-22T17:25:57Z` — 10 s margin at the head, 4 m 2 s span, one request per selector with
   the producer's 0.6 s sleep. 230/230 pass. Observation.

## Residual risk and gaps
- The producer stamps `utc` after writing each response file, so a stamp is fetch time plus write
  time; the earliest stamp is still 10 s after the freeze, so no fetch can precede the freeze.
  Inference from the pinned collector code, not a separate measurement.
- I did not re-fetch from api.openchain.xyz (one-fetch-instant limit, network budget), so status 200
  is the collector's recorded value; its integrity is anchored by the sha256 match to the committed
  bytes, not by a second fetch. Inference.
- Bodies are internally consistent manifest data; whether the served bytes are genuine openchain
  responses, and whether the deployed service ran the pinned Sourcify revision, is outside this
  item and already declared as a claim limit. Unknown, not attacked here.
- Spot anchor: committed blob `openchain-06fdde03.json` at HEAD hashes `e17c43577b042b8e…`, equal to
  manifest row 1's `sha256`. Observation.

## Artifacts
- `/fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewManifestC2/verify_manifest.py`
  sha256 `eb4fd94b127a0517307c54cca7b13f2090d5112a5cf75037d31b403a0c812796` — read-only checker,
  the only script run; its `tmp/` subdir stayed empty.
- Tooling installs: none; stock python3, jq, git, sha256sum only. No lane file touched besides this
  report; no network requests made.

Report: .ufo/waves/round-28/a2w/ReviewManifestC2.md
