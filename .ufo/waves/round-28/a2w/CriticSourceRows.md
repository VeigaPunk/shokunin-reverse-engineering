# CriticSourceRows: attack on planned SOURCES rows S084 to S087 (round 28, attempt 2)

Seat: KaidokuR28a2.CriticSourceRows (critic, leaf). Run 2026-10-22T18:22:56Z to 18:25:10Z.
Attacked: rows S084, S085, S086 as drafted in `corpus/SOURCES.md` (in the working copy at
dispatch, committed by the L1 in 9db24c9e during this run), the round-28 search log entry,
the round-28 lesson Gate rows 32-34, and planned row S087.
Contract read: `/home/vgpnk/Projects/shokunin/CORPUS.md` section "SOURCES.md" (rules 1-6, census).

## Verdicts

| row | verdict | reason |
|---|---|---|
| S084 | admit, with an anchor fix | The bytes, sha256, commit and line anchors hold. But the teaches clause "every other candidate keeps `filtered: false`" rests on `handlers.ts:90` (`mapLookupResult`) and `:262` (the search path), and the anchor does not cite either line. |
| S085 | admit as a separate row (do not merge) | It has its own URL, its own kind (`dataset`) and its own sha256, and its lane copy is the input frozen into the R28-C2 counter. It can also change without `handlers.ts` changing. The Gate quote is weak (see F3). |
| S086 | admit, with a version note and an attribution fix | The bytes and the `:74` and `:91` anchors hold. But the carrier was built with solc 0.8.37 and the row pins the docs at v0.8.30. The teaches cell also states REA's behaviour, which this source cannot support (see F4 and F5). |
| S087 | reject (write no row) | No row exists and the search log says "included 3 rows". A source that was not opened this round cannot be a row (rule 1). At most it is a bullet under `## Leads (unopened)`. |

No row duplicates an existing row. The census validator reports no W04 or E04 for S084-S086.

## Findings (all observations unless labelled)

F1 Primary bytes match the rows. Command: `curl -sS -o <f> https://raw.githubusercontent.com/argotorg/sourcify/189cd726.../<path>`
(HTTP 200 for both), `curl ... ethereum/solidity/v0.8.30/docs/using-the-compiler.rst` (200), then `sha256sum`.
Exit 0, at 18:23:34Z. handlers.ts `30981efb...5a38`, canonical-signatures.json `5572beb5...b3e2` (equal to the
lane copy), rst `76e5db1d...ae4fd`: all three equal the row anchors. JSON: a dict with 36 keys, all 10 characters
long (`0x` plus 8 hex digits); key `0xd55ec697` maps to `{'signature': 'upgrade()', 'source': 'generic:proxy'}`.

F2 Commit custody holds. `GET api.github.com/repos/argotorg/sourcify/compare/189cd726...master` (exit 0, at 18:23:34Z)
returned `compare identical ahead 0 behind 0`. `repos/ethereum/sourcify` returns 301 to repository id 183183290, and
`repos/argotorg/sourcify` is `183183290 argotorg/sourcify staging False` (at 18:23:59Z). So argotorg is the canonical,
non-fork home, and the commit is not a fork-network commit served through raw. Inference: the default branch is
`staging`, not `master`. That does not matter for the row, because its scope already excludes "which revision is deployed".

F3 Anchors versus teaches (S084, S085). `nl -ba handlers.ts` gives `39 function filterResponse(...)`, `47 signatureItem.filtered =`,
`48 signatureItem.name !== expectedCanonical.signature;` and `66 }`. Those are correct. `grep -n filtered handlers.ts`
gives `90: filtered: false,` (inside `mapLookupResult`, lines 87-93) and `262: filtered: false,`.
Counterexample: the anchored lines alone never assign `false` to a candidate whose selector is not a canonical key.
That half of the teaches is grounded only by `:90` and `:262`. The S085 Gate quote `"0xd55ec697": {` shows that a key
exists, but it grounds neither "36" nor the kept signature. JSON lines 2-3 are `"0xd55ec697": {` / `"signature": "upgrade()",`.
Fixable defect, not a tradeoff. Impacted axis: grounding (rule 1).

F4 Version mismatch (S086). Running `grep -rhoE 'solc...0\.[0-9]+\.[0-9]+'` over `.ufo/waves/arc3-loop1-round3/claims/c1/CR-1/` gives
`solc 0.8.37` (3 hits). The row pins tag `v0.8.30`. Command: `curl ... v0.8.37/docs/using-the-compiler.rst` (200, sha256
`bdacfc44631bf57be013041986133ee8e94c54aaae4fd599ecf8cdff277edcbb`, at 18:24:24Z), then `diff` of lines 68-92 between the
two tags, which printed `lines 68-92 identical`. So the claim holds at the compiler that built h09, but the row does not
show this. Fixable defect. Impacted axis: anchor and revision fidelity.

F5 Attribution (S086). The row's scope says "not REA's parser", yet its teaches cell says "REA 6.5.0 refuses such a carrier
as `invalid_format`". That sentence is grounded in the lane envelope, not in the Solidity docs. Running `grep -o` on
`corpus/evidence/round-28/c1/envelopes/h09.json` shows the top-level `"code":"invalid_request"` and the issue
`"reason":"invalid_format","message":"Hex carrier requires complete hexadecimal byte pairs..."`. Running `grep -o '__\$[0-9a-f]*\$__'`
on the carrier gives exactly one placeholder, `__$a2bad93077572174e8e5044433a5a7d5f3$__`, so "one placeholder" holds.
S077 already sets the pattern for this: "That REA's EVM provider is EVMole comes from REA's envelopes ... not from this page."
The cell also carries the lesson-local token `M28-1`. Fixable defect. Impacted axes: grounding and readability.

F6 W04 and duplicate URLs. In `scripts/sources-census.sh:600-660`, `url_of` takes the first `https?://` URL in the source
cell, strips the scheme, any fragment and a trailing slash, and lowercases the host. W04 fires when that URL was already seen
under a different scope. Command: `bash scripts/sources-census.sh validate /home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
exit 0, at 18:24:24Z. Output: W04 only for S033, S047, S054, S062, S069 and S083 (all older), then `ok`. The census reports
`rows 86`, `tier.A 80`, `missing 0`. S084 and S085 have different first URLs (different file paths), so splitting them
cannot trigger W04. Merging them would also not trigger it, but would bury S085's own sha256 inside S084's anchor.
Prior-row overlap: S076 (an OpenAPI page at `api.4byte.sourcify.dev`) and S078 (a blog at `docs.sourcify.dev`) have other
URLs and scopes, and S021 (the ABI spec at `docs.soliditylang.org`) is another page. Inference: S084 narrows S076's
"drops junk" but does not contradict it, so no `supersedes` row is needed. The search log already says S076 stays.

F7 Tiers. Code at a pinned commit of the maintainer's repository is A for "what the code does at that commit". The
maintainer's own data file at the same commit is A for its contents. Official Solidity docs are A for the placeholder form.
No tier inflation, and no row has kind `community`. Tradeoff note, not a defect: the recheck value `on-release` for a pinned
commit only ever triggers on a list change. S076 uses `90d` for the same live service, and S085's scope is explicitly "not
the deployed list".

F8 Merge versus separate (S085), strongest counterexample. The lane does bundle files in one row: S070, S079 and S083 each
list several files of one package. Against merging here: those bundles share one kind and one teaches, while S079 and S080
were split when kind and teaches differed. S085 differs from S084 in kind (`dataset` versus `code`), in teaches (list
membership versus rule) and in its separate frozen lane copy (C2 freeze 86fa8526). Verdict: separate is correct, and
merging would be allowed but would be a loss.

## Smallest safe corrections (for the L1; append-only, so each is a new row or a logged change)

1. S084 anchor: add `:87-93` (`mapLookupResult` sets `filtered: false`) and `:262`. Because the anchor cannot change in
   place, either write the fix as a correction row whose teaches opens `supersedes S084 —`, or (cheaper) have the R28-C2
   entry and the Gate cite `handlers.ts:90` alongside S084.
2. S085 Gate quote: replace or extend the quote with lines 2-3, `"0xd55ec697": {` / `"signature": "upgrade()",`. This is
   lesson text, not a row edit.
3. S086: note in the lesson Gate (or in a correction row) that the carrier was built with solc 0.8.37 and that lines 68-92 are
   identical at tag v0.8.37 (sha256 above). Attribute the REA sentence to
   `corpus/evidence/round-28/c1/envelopes/h09.json` (`reason` `invalid_format`) in the knowledge entry, not to S086, and
   spell out `M28-1` as "round-28 mistake M28-1".
4. S087: write no row. Add a Leads bullet only if the L1 wants the 4byte.directory server ordering kept as an open question.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r28/seats/a2w/CriticSourceRows/src/, accessed 2026-10-22)

| file | sha256 | source |
|---|---|---|
| handlers.ts | 30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38 | raw.githubusercontent.com/argotorg/sourcify/189cd726.../services/4byte/src/api/handlers.ts |
| canonical-signatures.json | 5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2 | same commit, services/4byte/src/utils/canonical-signatures.json |
| using-the-compiler.rst | 76e5db1df6cb67b189c0e8e0b27ed9546a03e5655ffdb400653d62196baac4ae | raw.githubusercontent.com/ethereum/solidity/v0.8.30/docs/using-the-compiler.rst |
| using-the-compiler-v0.8.37.rst | bdacfc44631bf57be013041986133ee8e94c54aaae4fd599ecf8cdff277edcbb | same path at tag v0.8.37 |
| compare.json | f7f54ac639cfb6aa37d9aa1913aa4af78ef2f1637e310f914352547a6ab5b4d3 | api.github.com/repos/argotorg/sourcify/compare/189cd726...master |
| repo-argot.json | 804969c01fed2499ab325186fdab166e46c7a27263733fabb98c71d43c4977e1 | api.github.com/repos/argotorg/sourcify |
| repo-eth.json | c1bb621eb3cd85bc18ebc5fa6ecaa7b913f11fb9b13151a0c76669e4557004df | api.github.com/repos/ethereum/sourcify (301 body) |

Located quotes: handlers.ts `:47-48` `signatureItem.filtered = signatureItem.name !== expectedCanonical.signature;`;
handlers.ts `:90` `filtered: false,`; rst v0.8.30 `:75` `The placeholder is a 34 character prefix of the hex encoding of
the keccak256 hash of the fully qualified library name.`

No 4byte.directory or openchain requests, no REA runs, and no tool installs or updates. No lane file was written other than this report.
