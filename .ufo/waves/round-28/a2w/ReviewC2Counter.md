# ReviewC2Counter — R28-C2 counter correctness review

Reviewed tools/round-28/c2-filtered-flag.py (worktree sha256 4fdf7db8…, equal to the frozen
`instruments` hash in claims-c2.json) against claims-c2.json and filterResponse in the
Sourcify 4byte service at commit 189cd726f7ed8fb3d2f503402d5c133e0f50e1fd (clone at
/fast/scratch/hyaku/kaidoku-r28/src/sourcify, `git rev-parse HEAD` = 189cd726…, 18:27:57Z).

Tooling note: no `lsp` device exists in this seat's tool inventory, so caller/definition
checks are text reads plus direct execution (selftest, live count, independent recount);
no grep output is offered as semantic proof. No tools installed this round; pacman untouched.
Bounds: read-only on the lane (git show/log/rev-parse only); selftest wrote only under
TMPDIR in scratch. Lane untouched except this report file.

## Verdict

HOLDS. The counter's predicate is a faithful transcription of filterResponse for every case
the committed data can exercise, including the null result list, the absent canonical
`signature` field and hex-key case. Time and pin checks are correct and fail closed. No
entry kind escapes the count on the committed 230 responses. No defect found; three latent
divergences are recorded below as informational.

## Findings

1. Predicate fidelity — HOLDS (severity: none). Counter c2-filtered-flag.py:185-191
   (`c = canon.get("0x" + s)`; `pred = c is not None and it.get("name") != c.get("signature")`;
   `it.get("filtered") is not pred`) vs handlers.ts:44-48 (`expectedCanonical =
   canonicalSignatures[hash]`; `expectedCanonical !== undefined && … !== null`;
   `signatureItem.name !== expectedCanonical.signature`). Command: selftest, 18:27:40Z,
   `TMPDIR=…/ReviewC2Counter/tmp python3 -I -B tools/round-28/c2-filtered-flag.py --selftest`,
   exit 0: "selftest cases=17 failures=0". Observation.
2. Null result list — HOLDS (severity: none). handlers.ts:45 guards `!== null` and assigns
   nothing; counter c2-filtered-flag.py:177 `items = fn["0x" + s] or []` yields zero
   candidates, so no prediction and no mismatch — same observable outcome. Exercised:
   census (recount.py base) found 48 of the 230 committed responses carry a null list;
   both sides leave them with zero entries. Observation, 18:28:52Z.
3. Absent canonical `signature` field — HOLDS (severity: none; latent note at 10).
   The pinned canonical-signatures.json has 36 keys; 5 of them (`0x60806040`,
   `0x60a06040`, `0x60c06040`, `0x60e06040`, `0x61010060`) have only a `source` field, no
   `signature` (census output, 18:26Z: "missing signature field: ['0x60806040', …]").
   getCanonicalSignatures returns the JSON verbatim (signature-util.ts:11-15), so JS sees
   `expectedCanonical.signature === undefined` and `filtered = (name !== undefined)` = true
   for any string name. Counter: `c.get("signature")` is None and `str != None` is True —
   identical verdict. Unexercised by the data: those 5 selectors have 0 candidate items
   (recount.py: "candidate_items=0 predicted_true_among_them=0", exit 0, 18:28:03Z).
   Observation.
4. Case of hex keys — HOLDS (severity: none). Python dict.get and JS property access are
   both exact, case-sensitive string matches, so the counter models the code. All 230 TSV
   selectors, all 36 canonical keys and all body hash keys are lowercase `0x…` (census:
   "tsv rows 230 dups [] upper []", "canon all 0x+lower: True", "uppercase body hashes 0").
   A case mismatch would fail closed at c2-filtered-flag.py:174 ("body lacks ok=true or the
   selector key"), never silently pass. Observation, 18:26Z.
5. filter=false premise — HOLDS (severity: none). handlers.ts:223 calls
   `filterResponse(result, shouldFilter)` before the `if (shouldFilter)` removal loop
   (handlers.ts:54), so with `filter=false` the `filtered` flags are still computed and
   returned — the flag the claim tests is produced on exactly the pinned URL
   (c2-filtered-flag.py:37). mapLookupResult initializes `filtered: false`
   (handlers.ts:90), matching the counter's canonical-miss → false conjunct. Observation
   (code read of the cited commit).
6. Time checks — HOLDS (severity: none). c2-filtered-flag.py:162-166: manifest `utc` must
   parse as `%Y-%m-%dT%H:%M:%SZ` (else fail closed) and be strictly greater than the
   counter's own first-commit `%ct` (`t <= ctime` fails); the response file's first-add
   commit must not precede the counter commit (`added < ctime` fails; equality allowed,
   matching the freeze wording "before its own commit"). first_commit_time takes the oldest
   `%ct` line (out[-1] of newest-first git log), i.e. the true first commit. Freeze commit
   86fa8526 committed 2026-10-22T17:21:55Z (`git log -1 --format='%H %cI'`), manifest utcs
   17:22:05Z-17:25:57Z, data commit a2673116 — all after; live run shows 230/230 complete.
   Observation, 18:27:57Z.
7. Pin checks — HOLDS (severity: none). PINS (c2-filtered-flag.py:51-54) equal the
   `loaded_by_counter` hashes in claims-c2.json; `pinned()` (line 80) refuses an absent or
   hash-differing input with exit 2 (selftest "red-pin-refusal exit=2"). Measured
   (18:26Z): counter 4fdf7db8…, selectors.tsv ad1b5098…, canonical-signatures.json
   5572beb5… — all three match the frozen file; the scratch clone's
   utils/canonical-signatures.json is byte-identical to the pinned copy (same sha256).
   Observation.
8. Entry-kind escape — HOLDS on the committed data (severity: none; latent note at 11).
   The counter counts only `result.function["0x" + s]` (line 177). filterResponse also
   mutates `result.event` entries and would touch any extra `function` keys
   (handlers.ts:42-53). Census of all 230 committed responses: "event keys 0", "extra
   function keys beyond requested 0", 246 items total — nothing escapes. The lookup path
   only creates entries for requested hashes (handlers.ts:194-214), so this cannot arise
   under the pinned URL. Observation, 18:26Z.
9. Target arithmetic — HOLDS (severity: none). main_count exit rule (lines 208-210)
   matches the frozen target exactly: complete==total==230, entries>=1, mismatches==0,
   predicted_true>=1, entry_ok==1 → 0, else 1; PinError → 2. Live run at 18:27:57Z, exit 1:
   "FAIL entry absent / responses_complete=230/230 entries=246 mismatches=0
   predicted_true=59 entry_ok=0" — reproduces the L1 tally; the miss is only the not-yet-
   landed knowledge entry. Independent recount straight from the raw response bytes
   (recount.py, exit 0, 18:28:03Z): "selectors=230 malformed=[] entries=246 mismatches=0
   predicted_true=59". Observation.
10. Latent divergence, name:null — INFORMATIONAL (severity: low, not exercised). For an
    item with explicit JSON `"name": null` under a signature-less canonical key, JS computes
    `null !== undefined` → filtered=true, while the counter computes `None != None` → False.
    Counterexample shape: `{"0xaabbccdd": {"source": "x"}}` canonical + response item
    `{"name": null, "filtered": true}` would be counted a mismatch. Data: 0 null names and
    0 missing names in the 246 items (census 18:26Z); mapLookupResult always emits a string
    name, so it needs a null DB column. Inference from code plus data census.
11. Latent divergence, event/extra keys — INFORMATIONAL (severity: low, not reachable under
    the pinned URL). If a future response carried event entries or extra function keys, the
    counter would not count them while filterResponse would flag them. Today: zero such
    entries in all 230 responses (finding 8). Inference.
12. Selftest coverage gaps — INFORMATIONAL (severity: low). No selftest case pins the null
    list on a canonical selector, the absent-`signature` edge, or a name:null item; the
    fixture's null list sits on the non-canonical 22222222. The code paths are shared with
    covered cases and the live data exercises the null list 48 times, so the verdict is
    unaffected. Inference from the selftest case list (lines 265-281).

## Residual risk and verification gaps

- The counter verifies sha256 of response bytes against the manifest but cannot prove the
  manifest `utc` is the true fetch instant; that trust sits in the separately pinned
  producer collect-c2.py (claims-c2.json `producers_not_counters`). Unverified by design;
  the claim's `limits` states the one-fetch-instant assumption.
- The claim assumes api.openchain.xyz runs this Sourcify revision; that is unprovable from
  here and is acknowledged in the claim's `limits`. The 0-mismatch result on 246 entries is
  consistent with it, not proof of it.
- I did not audit collect-c2.py itself (out of scope; producer, not counter).
- entry_ok=0 is expected mid-round (knowledge entry not yet committed); the round must
  still land the entry, SOURCES row and Gate line for exit 0.

## Artifacts

- /fast/scratch/hyaku/kaidoku-r28/seats/a2w/ReviewC2Counter/recount.py sha256
  b87b9c541d216412ae09a797733f937aa613a3a7ca405d76df3534e82859d708 (independent recount;
  its run output is quoted in findings 3 and 9).
- tmp/ (selftest scratch) left empty; no other artifacts produced.
