# ReopenS087 — re-open SOURCES row S087

Seat: `KaidokuR29.ReopenS087`. Scope: `corpus/SOURCES.md` row S087 (`:93`) and the Gate
row in `corpus/lessons/round-29.md` (`:28-34`, gate note `:36-38`). Read-only on the
lane; all fetched bytes under `/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReopenS087/`.
All times UTC 2026-10-22.

## Verdict: admit

Every checkable cell of row S087 and the lesson Gate row re-verifies against freshly
served bytes and a live `git ls-remote`. No finding.

## Re-fetch evidence

Command (20:21:51Z):
`curl -sSL -o handlers.ts https://raw.githubusercontent.com/argotorg/sourcify/0966a3bcf13a46b335dae390a0c95b3b0d980c69/services/4byte/src/api/handlers.ts` → HTTP 200, 14637 B.
`curl -sSL -o canonical-signatures.json .../services/4byte/src/utils/canonical-signatures.json` (same commit) → HTTP 200, 3857 B.

sha256 of served bytes:
- `handlers.ts` `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38` — equals the row's recorded hash. (observation)
- `canonical-signatures.json` `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2` — equals the row's recorded hash and the lane pin
  `corpus/evidence/round-29/c2/canonical-signatures.json` (same sha256, 20:22Z). (observation)

`git ls-remote https://github.com/argotorg/sourcify.git HEAD refs/heads/master refs/heads/staging` (20:21:51Z, exit 0):
```
0966a3bcf13a46b335dae390a0c95b3b0d980c69	HEAD
189cd726f7ed8fb3d2f503402d5c133e0f50e1fd	refs/heads/master
0966a3bcf13a46b335dae390a0c95b3b0d980c69	refs/heads/staging
```
Matches the row's cell verbatim: HEAD = staging = `0966a3bc` (the S087 commit),
master = `189cd726` (the S084 commit). The row's "newest branch head" framing still
holds: HEAD resolves to the staging tip the URL pins. (observation)

## Located quote

`handlers.ts:47-48` in the served bytes (exactly as the row and the Gate table record):

```
          signatureItem.filtered =
            signatureItem.name !== expectedCanonical.signature;
```

Two contiguous served lines, inside `filterResponse`, which spans `:39-66` in the
served bytes (`function filterResponse(...)` opens at `:39`, closing `}` at `:66`).
Both locator cells confirmed. (observation)

## Cell-by-cell

- Source cell: URL commit `0966a3bc` is current HEAD/staging; ls-remote parenthetical
  accurate; the second file exists at the same commit and is fetched above. (observation)
- Type `code`, confidence `A`: consistent with row conventions. (observation)
- Teaches cell: "whether the newest branch head … still sets `filtered` the way S084
  records, and with the same canonical list" — supported: staging bytes byte-identical
  to master bytes (below), which S084/S085 already record. Exclusions (deployed
  revision, result order, `hasVerifiedContract`) are untouched by the row. (observation)
- Identity cell: "(byte-identical to S084)" / "(identical to S085)" — verified by
  fetching the `189cd726` copies (20:22:42Z): `handlers-master.ts` sha256
  `30981efbc7bc…` and `canonical-master.json` sha256 `5572beb596…`; `cmp -s` reports
  byte-identical for both pairs. S084 row (`:90`) records the same handlers.ts hash.
  (observation)
- "36 keys, 5 of them `system:magic` with no `signature`" — verified: 36 top-level
  keys; exactly 5 (`0x60806040`, `0x60a06040`, `0x60c06040`, `0x60e06040`,
  `0x61010060`) carry only `{"source":"system:magic"}` and no `signature`. (observation)
- Observation cell: "A key with no `signature` makes `name !== undefined` true, so
  every candidate under a `system:magic` key is marked filtered" — consistent with
  the served code at `:47-48` (`expectedCanonical.signature` is `undefined` for those
  keys). (inference from code semantics, grounded in served lines)
- `mined`, `2026-10-22`, `on-release`, knowledge path
  `corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md` — file exists and its
  Rule section cites `handlers.ts:39-66` at both commits, matching. (observation)

## Lesson Gate row (`corpus/lessons/round-29.md`)

- Gate table S087 row (`:34`): URL, access timestamp 19:52Z, both sha256s, located
  quote and `:47-48`/`:39-66` locators — all re-verified above. Quote is 2 contiguous
  lines, within the 25-word cap. (observation)
- Gate note (`:36-38`): "6 of the 31 kept signatures do not hash to their key."
  Independently recomputed over the served `canonical-signatures.json` with
  keccak-256 (pycryptodome, scratch venv): 31 keys carry a `signature`; exactly 6
  signatures do not hash to their key — `0x0d0f30c6`→`token1()`,
  `0x1a686502`→`uniswapV3SwapCallback(int256,int256,bytes)`,
  `0x89035730`→`flash(address,uint256,uint256,bytes)`,
  `0xc45a0155`→`mint(address,int24,int24,uint128,bytes)`,
  `0xfc6f7865`→`uniswapV3MintCallback(uint256,uint256,bytes)`,
  `0x8abf6077`→`proxyOwner()`. Matches the note and the knowledge entry's list.
  The note's claim that the row's teaches cell does not state the 6-of-31 is true.
  (observation)
- Preamble claims the L1 used plain `curl`/`git ls-remote` and that no existing row
  changed; consistent with the SOURCES.md search-log entry at `:167` (5 files
  screened, 2 rows included, 3 master copies excluded). (observation)

## Tooling installs

`pycryptodome` into scratch venv `.venv` via `uv venv` + `uv pip` (channel allowed by
the contract; pacman paused host-wide). Reason: keccak-256 to recompute selector keys
for the 6-of-31 gate-note check. No other installs; `curl`, `git`, `sha256sum`, `cmp`
pre-existing.

## Scratch artifacts (`/fast/scratch/hyaku/kaidoku-r29/seats/w1/ReopenS087/`)

- `handlers.ts` — `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38` (served, staging commit)
- `canonical-signatures.json` — `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2` (served, staging commit)
- `handlers-master.ts` — `30981efbc7bc1b541954eb75767c8154562f4f77a9bfc1ad22cf19c8996c5a38` (served, master commit; byte-identical)
- `canonical-master.json` — `5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2` (served, master commit; byte-identical)
- `.venv/` — pycryptodome install (tooling, not evidence)

## Residual risk / gaps

- Deployment: which revision the live service actually runs remains out of scope (the
  row disclaims it); nothing here bears on it. (unknown, out of scope)
- `git ls-remote` is a point-in-time read; the row's 19:52Z snapshot and this 20:21Z
  re-check agree. (observation)
- No network lookups to 4byte.directory or api.openchain.xyz were needed or made;
  none requested by the item. (observation)
