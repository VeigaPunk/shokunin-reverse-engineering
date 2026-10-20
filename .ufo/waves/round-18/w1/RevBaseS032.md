# RevBaseS032 — R17-S032-DIGEST: is the defect open at 9011581d?

Seat `KaidokuR18.RevBaseS032`. Read-only; only this file written. No installs or upgrades.
Lane HEAD = `9011581d84527ba34c675f9cf912e54d2e72d470` = `refs/heads/main` at audit time.

## Verdict

**Open at 9011581d**, with a wording defect in the routed remedy. The baseline row presents a
64-hex page digest as a checkable identity and does not qualify it; nine independent fetches of the
same URL produced nine distinct bodies, none matching the recorded digest. The lesson's *first*
remedy ("anchor the row on title and state") is already nominally present, so the operative red
condition is narrower than the lesson text suggests: the unqualified digest, not the absence of an
anchor. This is not "already-closed" (the digest is still presented as an identity) and not
"mis-stated" in its load-bearing claim (non-reproducibility is re-verified below).

Against `contract.md:44-45`, the closure test is **both too strong and too weak**: too strong
because it mandates a new row with both literal tokens and so rejects the lesson's digest-dropped
title/state anchor; too weak because the `fetch-time` token need not qualify a digest and the
correction need state nothing; and structurally unable to report an already-closed baseline, since
its red is guaranteed by the absent S033 row rather than by the S032 row's digest state. Details and
a replacement predicate are below.

## Observation 1 — baseline row and routed text (Git objects at REV)

```sh
$ git rev-parse refs/heads/main
9011581d84527ba34c675f9cf912e54d2e72d470        # exit 0
$ git rev-parse HEAD
9011581d84527ba34c675f9cf912e54d2e72d470        # exit 0
$ git status --porcelain=v1 --untracked-files=no
 M .ufo/waves/round-17/tools/compare.py         # exit 0; sibling in-flight edit, not mine, untouched
$ git show 9011581d:corpus/SOURCES.md | awk -F'|' 'NR==38{print NF-2}'
11                                               # exit 0
$ git show 9011581d:corpus/SOURCES.md | grep -c 'supersedes S0'
0                                                # exit 1 = no match
$ git show 9011581d:corpus/SOURCES.md | grep -c 'fetch-time'
0                                                # exit 1 = no match
```

The S032 row at `9011581d:corpus/SOURCES.md:38` (identical to the working-tree row) has 11 cells.
Its 6th cell (the `anchor` column, `CORPUS.md:86`) is, verbatim:

> `PR title and description, state OPEN, fetched 2026-10-20 (page sha256 `436c0f63d2dc1e5d2946e4bbf15dfafb1f99fa2a3a60f0b42b00918bf7107cb8`)`

So at baseline: one 64-hex digest, no `fetch-time` token anywhere in the registry, no superseding
row. `git log -S'436c0f63' -- corpus/SOURCES.md` returns only
`d0ab2992149a38794e5ef2474ba5d4ef5ee1e905` (2026-10-20 11:47:24 -0300, exit 0); the routing lesson
was committed at 9011581d (12:06:56 -0300), i.e. the verifier routed the defect *after* the row was
written, and the row was unchanged at the baseline.

The routed text is `corpus/lessons/round-17-verifier-spotcheck.md:147`:

> "S032's page sha256 `436c0f63…` cannot be reproduced: two fetches gave `028dbb7d…` and
> `f3841de0…`, because GitHub HTML is dynamic. Anchor the row on title and state, or qualify the
> digest as fetch-time only."

Observation: the title is in the row's `source` cell (`corpus/SOURCES.md:38`) and quoted again in the
r17 Gate at `corpus/lessons/round-17.md:61`; the state is in the anchor cell. The lesson's first
alternative is therefore already present in prose. The values `028dbb7d…` and `f3841de0…` appear
only at `round-17-verifier-spotcheck.md:147` and in the r18 draft
(`.ufo/waves/round-18/w1/DraftS033Row.md:32`); no retained fetch receipt or body carries them. The
`436c0f63…` value otherwise appears only at `corpus/SOURCES.md:38` and in the same draft. So the
verifier's fetches were not retained and the specific values are not independently checkable.
[INFERENCE] The row's digest is an unretained one-off body hash; its provenance (method, headers,
body) cannot be reconstructed.

## Observation 2 — re-fetch evidence

Shell, pure body (no `-w` trailer in the hash), 2026-10-20T15:28:15Z (`date -u`, exit 0):

```sh
$ U=https://github.com/NationalSecurityAgency/ghidra/pull/9348
$ for i in 1 2; do curl -sSL -o >(sha256sum >&2) -w 'http=%{http_code} bytes=%{size_download}\n' "$U"; echo "curl_exit=$?"; done
http=200 bytes=403382
08e2db7a5c4dc2026522f0c3a043636028e79f7b6d6d52d1ffd627edd4588cdc  -     # curl_exit=0
http=200 bytes=403377
787aac45c3d87f934b8adbc15e029af7282c59e276b8c5d55a5986dd9f9a3fb9  -     # curl_exit=0
$ for i in 1 2; do curl -sSL -o >(sha256sum >&2) -w 'http=%{http_code} bytes=%{size_download}\n' "$U.diff"; echo "curl_exit=$?"; done
http=200 bytes=4614
ae602a51fb870c3147572ed41c1cf5a7dbdda1d2d17faf6a75654af0c7b27156  -     # curl_exit=0
http=200 bytes=4614
ae602a51fb870c3147572ed41c1cf5a7dbdda1d2d17faf6a75654af0c7b27156  -     # curl_exit=0
```

Earlier in the same audit, via Python 3 stdlib `urllib` (HTTP 200 each; no shell exit code):

| fetch | UA | bytes | sha256 |
|---|---|---|---|
| 1 | Chrome 140 | 403377 | `31d385c1ae3f4f7001f05ef48d22f6cf24d4bf52221fc93f462a9cf2b51397d1` |
| 2 | Chrome 140 | 403377 | `f7394aacb06e93d61d9d9806a81d6dcb07286c6519b2e34f68980f895388b3b8` |
| 3 | Chrome 140 | 403382 | `754f96e9748d05f6d3c882e639380c7de282962ab2612670adc4d77d34c264dd` |
| 4 | Python-urllib/3.13 | 403382 | `03d30e94f3508626134155711cc68b51305b33a574a3e518e9a10718f3d979ba` |
| 5 | curl/8.17.0 | 403382 | `a8a907612f10abae4e3d7ddba6d8b472b387fcc861ed0ff9b56d526f8990e84d` |
| 6, 7 | Chrome 140 | 403382 / 403386 | `32bf973bec64638c…` / `3db5960c4eedae8d…` (16-hex prefixes) |
| 8, 9 | shell curl | 403382 / 403377 | 08e2db7a… / 787aac45… (above) |

Observation: 9 fetches, 9 distinct hashes, 0 equal to `436c0f63…`, `028dbb7d…` or `f3841de0…`.
Fetches 1 and 2 were separated by a 2 s sleep (durations 1.04 s and 0.10 s) and returned the same
`Date` header and identical length; they differ at offset 42513, in `<meta name="request-id" …>` and
`<meta name="html-safe-nonce" …>`. Fetches 6/7
differed in 15,083 byte runs and by 4 bytes of length. The body also embeds
`nonce="v2:2df1d85b-…"` and `data-pjax-transient` request tokens. The response carries
`cache-control: no-cache` and no `ETag`. [INFERENCE] The instability is per-response channel/nonce
material, not a slow content update: the two shell fetches (8/9), issued back-to-back with no sleep
(whole four-fetch block under 1.5 s), already differ, so no plain body hash of this page can be
stable by construction.

By contrast, `.diff` (4614 bytes, `ae602a51…`) and `.patch` (9115 bytes, `ae5dc2e3…`, urllib twice,
HTTP 200) are byte-stable across fetches; `.commits` and `.files` are not (they differ between two
fetches). The PR's machine-readable identity inside the fetched HTML is stable: the embedded JSON
carries `"state":"OPEN"`, `"mergedTime":null`, `"title":"Golang: recover symbols from stripped Go
1.24/1.25 (swiss-map) binaries"`, `"headSha":"a214355498e84aa86280be0c31c955aaf94f2d12"`. The REST
API was attempted once and returned HTTP 403 rate-limit (matching the r17 scout's experience,
`.ufo/waves/round-17/w2/ScoutGhidraEOFIssue.md:155`), so state was read from the HTML embed instead.

## Why the verdict is "open"

- The anchor cell asserts `page sha256 436c0f63…` as an identity, with no statement that it is a
  fetch-time artefact and no retained method/body. Nothing in the registry can be checked against
  it: 0/9 fetches reproduce it, and none can.
- "Already-closed" fails: the digest is neither removed nor qualified; the row still reads as
  content-addressed.
- "Mis-stated" fails in the load-bearing claim: repeated fetches really do differ (0/9 equal), so
  the routing's causal claim is re-observed. The wording is imprecise only in offering an
  alternative that the baseline row already nominally satisfies; the digest is the operative defect.
- The row's state clause is still true (`"state":"OPEN"` at 15:25Z), so a title/state/head anchor is
  available and stable; only the page digest is unusable.

## Minimal objective test

Any test that requires reproducing the digest is unsatisfiable by construction (Observation 2), and
the contract's tool may read Git objects only (`contract.md:26` "reads Git objects at REV only").
The test must therefore be a presentation test on the effective row, offline:

```
effective(REV) := the row at REV whose teaches cell starts with `supersedes S032 —`
                  (highest id if several), else the S032 row
a              := that row's anchor cell (6th cell)
closed(REV)    := a contains no token matching (?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])
                  OR a contains "fetch-time" (case-insensitive)
```

Evaluation:

| state | predicate | why |
|---|---|---|
| baseline 9011581d (S032) | **open** | one 64-hex digest in `a`, no `fetch-time` |
| hypothetical: S032 anchor qualified in place | closed | qualifier present (but `controls.py` forbids this form) |
| hypothetical: digest dropped, title/state/head anchor only | closed | no 64-hex token |
| draft S033 (`.ufo/waves/round-18/w1/DraftS033Row.md:10`, not integrated) | closed | digest + literal `fetch-time only` |

The predicate is decidable from `git show REV:corpus/SOURCES.md` alone, needs no network, and does
not prescribe the remediation form. It can also return "already closed" at a baseline where the
digest was already qualified or removed — which the contract's check cannot.

Residual gap in the minimal test: a superseding row that carries no digest and no explanation
(e.g. anchor "accessed 2026-10-20") passes, while the historical S032 row still shows the digest.
That is acceptable under append-only history only if the ledger is meant to supersede silently; if
the correction must be self-explaining, add one objective clause: the effective row's `teaches`,
after the prefix, contains one of `digest`, `sha256`, or `reproduc`. The draft passes that clause
("S032 keyed the page on a sha256 that does not reproduce").

## Comparison with the contract definition

`contract.md:44-45` requires: "an 11-column registry row whose teaches cell starts with
`supersedes S032 —` and whose anchor cell contains `fetch-time`".

**Too strong (form-locked).** It mandates a new row and both literal tokens, so it rejects a valid
closure by the lesson's first remedy: an anchor on title + `state OPEN` + `head a214355…` with the
digest dropped has no `fetch-time` and fails. It also rejects an in-place qualification of the S032
anchor, although the defect text offers exactly that remedy. That form is separately forbidden by
`contract.md:142-144` ("SOURCES S001–S032 identical except status/recheck/used-by") and by
`CORPUS.md:116-118` (append-only; corrections are new rows), so the append-only form is defensible
as lane policy — but the check should then say it tests the ledger form, not the defect state. It
also *requires keeping a volatile page digest* as the only qualifying evidence, whereas
`CORPUS.md:99-100` asks the anchor for an exact section plus revision (version/commit/date); the
stable revision here is the head commit `a214355…`, and `.diff` is the stable byte object. The
definition rewards the weaker anchor.

**Too weak (token presence, not property).** The `fetch-time` token is not tied to a digest. A row
with `teaches` = "supersedes S032 — " (nothing after the prefix) and `anchor` = "accessed
2026-10-20; fetch-time not recorded" passes while S032's unqualified digest remains the only digest
in the registry and no correction is stated. It also does not check the S032 row's `status`/`used-by`
pointer (the only in-place fields `CORPUS.md:116-118` allows), so a reader at line 38 sees no route
to the correction. Matching is unspecified for case and for the em dash, so `Fetch-time` or a
hyphen could fail a literal implementation (the draft uses lowercase, so it passes either way).

**It cannot falsify the baseline premise.** Its red state at 9011581d is guaranteed by the absence
of the S033 row, not by the S032 row's digest state. Had the digest been qualified (or reproducible)
at baseline, the check would still be red; had a row with the two tokens been added for an unrelated
reason, it would go green without touching the digest. This contradicts the stronger reading of
`claims.json:13` ("each check is a revision-scoped Git-object test whose red state is the baseline"):
for this one defect the red is fix-absence, not defect-state. Most other checks are tied to a
concrete correction artifact (the restored `SHA256SUMS` match, the retained receipt summary, the two
producing revisions), so their green cannot be reached vacuously; S032's can be, which makes it the
weakest of the six.

**Recommendation.** Keep the append-only part of the contract check (11 cells + `supersedes S032 —`,
which matches `CORPUS.md:117-118`) and replace the `anchor contains fetch-time` clause with the
predicate above applied to the effective row: `closed = form_check ∧ no_unqualified_64hex_or_fetch_time_qualified`.
That makes the check test the defect it names, remains satisfiable, and still fails a fabricated row
that records no digest disposition. State case-insensitive matching for `fetch-time`.

## Residual risk and verification gaps

- The exact provenance of `436c0f63…` is unretained; I cannot prove which byte stream it hashed.
  No tested representation matches it (page ×9, `.diff`, `.patch`), and no page body can reproduce
  by construction, so the row's digest is unverifiable regardless of provenance.
- `routed-defects.py` did not exist at audit time (`.ufo/waves/round-18/tools/` contained only
  `revpin.py`), so this compares the contract text, not its implementation. When it lands, verify
  cell counting, exact prefix matching on `teaches`, and case handling of `fetch-time`.
- The draft S033 was evaluated as text at `.ufo/waves/round-18/w1/DraftS033Row.md:10`, not from
  `SOURCES.md`; it is not integrated.
- The REST API check was rate-limited (HTTP 403); PR state came from the HTML embed, which is
  page-declared content and treated as untrusted data.
- No LSP server applies (no code symbol/callsite question; the artifact is Markdown registry data);
  text searches were used as literal checks, not semantic proof. I did not run REA, Ghidra, or any
  carrier, and did not verify the PR's mechanism claim (out of scope).

## Tooling record

No installs or updates. Existing tools only: `git` (read-only: `rev-parse`, `status`, `show`,
`log -S`), `curl` 8.x, Python 3 stdlib (`urllib`, `hashlib`, `re`), `awk`, `grep`. One tracked file
(`.ufo/waves/round-17/tools/compare.py`) was modified in the lane by another seat; I did not touch it.
