# R44MistakeHunt — mined mistake for the round-44 lesson

Seat role: critic. Axes exercised: falsifiability (the row must cite a reproducible red/green pair),
evidence integrity (receipts committed in-lane), scope discipline (one mistake, no widening).
Base observed: `f5fb8d590f0dd6afc0847e1a63e8a3953bef8717` (wave-1 spec commit on lane `main`;
round base `c29360e3…`). Read-only against the lane; only this file and
`w1/artifacts/R44MistakeHunt/` were written. Scratch: `/fast/scratch/hyaku/kaidoku-r44/probe-R44MistakeHunt/`.

## Verdict

Candidate (a) is REAL and verified: the L1's pre-freeze probe guessed the unblob fixture
API shape — `squashfs_v2.0_be.expected` — before reading the `__output__/` directory listing.
The guessed URL 404s (reproduced today); the correct listing returns 200 and shows the real
members are `<name>.bin_extract/` directories — there is no `.expected` file anywhere in the
fixture tree. Class: `stale-premise`, exactly as the draft names it (`plans/round-44-claims.md:198-203`).

Candidate (b) declined: round-43's lesson (`corpus/lessons/round-43.md`) already filed M43-1 and
M43-2; re-filing them would be a carried row, not a mined round-44 mistake. This seat's example
is the round's own probe error.

## Evidence (the red/green pair; reproduced 2026-10-28)

| probe | command | result | receipt artifact (sha256) |
|---|---|---|---|
| red — guessed URL | `curl -sS "https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/squashfs_v2/big_endian/__output__/squashfs_v2.0_be.expected"` | **HTTP 404**, body `404: Not Found` (14 B), wall 0.235 s | `artifacts/R44MistakeHunt/guessed-expected-404.body` sha256 `d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed` |
| green — correct listing (HTML tree) | `curl -sSL "https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs/squashfs_v2/big_endian/__output__"` | **HTTP 200**, 221 745 B, wall 0.078 s; page contains `squashfs_v2.0_be.bin_extract`, `squashfs_v2.1_be.bin_extract`; `grep -c 'squashfs_v2.0_be.expected'` = 0 | `artifacts/R44MistakeHunt/tree-200.html` sha256 `e3ea23b9c44e9c529d4733d53cb8f4227e689bd23e3169dfdccd3530e3132f46`; extract `member-names.txt` sha256 `9923279528c4b7a57d987dad103aa24d3db513594398be15b93fbb1ccc620176` |
| green — corroborating seat receipt | `api.github.com/.../contents/.../__output__?ref=26.6.4` | **HTTP 200** at 2026-10-28T11:10:40Z, body sha256 `ba7e3dc2…9e75be`, lists the same two `bin_extract` dirs | `w1/R44SrcOracle/listings/squashfs_v2__big_endian__output__.json` |
| second red arm | `curl -sSL "https://github.com/onekey-sec/unblob/raw/26.6.4/.../__output__/squashfs_v2.0_be.expected"` | **HTTP 404**, wall 0.427 s | (status-only probe) |
| control arm | contents-API call by this seat | **HTTP 403** — unauthenticated rate limit (`x-ratelimit-remaining: 0`), body receipt `artifacts/R44MistakeHunt/body-403.json` sha256 `2282f9baf641a8417b97a1785119fd62f08e3560b50fdecfae2019fff3ae259d`; the 200 above is the HTML listing, and R44SrcOracle's committed 200 covers the API form | — |

The guess assumed a per-fixture `.expected` file convention; unblob's integration tree in fact
keeps expected output as `__output__/<input>.bin_extract/` directories. `tools/round-42/fixtures.json`
confirmed nothing in the pinned fixture set uses a `.expected` member name.

## mistakes.md row (for the round-44 lesson, `## Mistakes`)

| id | class | evidence pointer | captured-by | fix (shown able to fail) |
|---|---|---|---|---|
| M44-1 (provisional; L1 assigns sequence) | stale-premise — pre-freeze probe fetched `squashfs_v2.0_be.expected` by guessing the fixture API shape (HTTP 404) before reading the `__output__/` directory listing, whose real members are `<name>.bin_extract/` dirs | `plans/round-44-claims.md:198-203` (draft anchor); reproduced red/green by R44MistakeHunt 2026-10-28: `w1/artifacts/R44MistakeHunt/guessed-expected-404.body` (404, sha256 `d5558cd4…3512ed`) vs `tree-200.html` + `member-names.txt` (200, sha256 `e3ea23b9…3d2f46`); corroborating committed 200 `w1/R44SrcOracle/listings/squashfs_v2__big_endian__output__.json`. NOTE: the originally cited receipt `.ufo/waves/round-44/l1/probe-fixture-404.txt` is absent (see below) | the frozen-URL convention: a URL is pinned only after a successful open, never guessed (enforced this round by R44SrcOracle opening listings first and pinning from 200 entries) | verify URL existence via the directory listing before pinning — red: `curl` of the guessed `.expected` URL → 404 (shown above, able to fail); green: `__output__/` listing open → 200 (shown above). Mechanical form (R44Debt D-27): the source gate refuses a URL cell lacking a committed 200 open receipt |

## Secondary finding — cited evidence path is absent (fixable defect, not a class change)

The draft cites `.ufo/waves/round-44/l1/probe-fixture-404.txt` as this mistake's red receipt;
`.ufo/waves/round-44/l1/` is empty (`find` and `git status` confirm; corroborated by
`w1/R44Debt.md` G9 / D-27 and the round-43-style ledger note at R44Debt `112`). The mistake
remains verifiable because this seat reproduced the 404 against the live URL, but the claims
file's evidence pointer currently resolves to nothing.

Smallest safe correction for the L1, choose one before freeze:
- commit the original probe receipt at the cited path (if it exists in L1 scratch), or
- repoint `plans/round-44-claims.md:200` to `w1/artifacts/R44MistakeHunt/guessed-expected-404.body`
  (this seat's reproduction, committed in-lane), recording the substitution in
  `## Changes from the draft`.

## Honesty notes

- This seat could not re-run the GitHub contents API (unauthenticated pool exhausted on this
  egress IP, `x-ratelimit-reset 1793188537`); the green arm therefore rests on the HTML tree
  page 200 plus the committed R44SrcOracle API 200, not a fresh API call by this seat.
- The 404 and 200 are against live upstream; a later unblob re-tagging could change them, but
  tag `26.6.4` is pinned and the receipts are committed, so the row's evidence is frozen-shape.
- No claim text, tool, or frozen path was touched by this seat.
