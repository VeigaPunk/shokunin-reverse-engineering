# R45 W1 — S138 `opened`-cell repair: the row's own top URL, fetched

Seat `R45W1SrcS138Fix` (reviewer-shaped leaf, no dispatch). Lane `kaidoku`, round 45, wave 1.
Base `faa875bc0eb839d15b83c4afa6078819e5a7b381`; freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`
(`--is-ancestor` exit **0**; `git diff --stat <freeze> HEAD -- plans/round-45-claims.md tools/round-45/`
empty, so the frozen bytes hold at the revision I cite). Read-only on the lane tree: this report is the
only artifact, plus its sibling copy `../R45W1SrcS138Fix.md`.

Inputs read (bytes I actually read, hashed):

| input | sha256 | note |
|---|---|---|
| `corpus/SOURCES.md` | `70be416d0294871d969b587bd4eb2f4980bc46f1d8faa9636ecf0176edbc401a` | S138 = line 144, line sha256 `fbfb0186e09836b45d3baf9ea1a2358dfe78a4eb2536fa645c397a2056f8f2ba` |
| `corpus/lessons/round-44.md` | `d09e415ed983c7d7b72e6b54ef8a038b89a90308b8ae954227eb76c1b21d1cb0` | `## Gate` S138 row = line 27; routing item 4 |
| `corpus/lessons/round-45.md` | `f6bd9e17fed2008fce4163576e50fc2db96c7294c5be350f50665349d38a5131` | `## Mistakes` M45-2 = line 16; `### S138 correction (append-only)` = line 35 |
| `corpus/evidence/round-44/oracle/manifest.json` | `06a72dd5b660c79adae943917abf40c24ab16554ec6c2f14985958799a78f5fe` | prefix agrees with the round-44 Gate cell's `06a72dd5…f5fe` |

The S138 `opened` cell is `2026-10-28` (date-only). The *verbose* descendant credit is the round-44
Gate cell: `2026-10-28T11:10:29Z–11:12:37Z (contents API, 10 listings + 22 members, HTTP 200; …)`.
That distinction matters for (d) and for F3.

## 1. Receipts (every fetch, with status, bytes, hash, UTC)

Scratch `S=/fast/scratch/hyaku/kaidoku-r45/R45W1SrcS138Fix` (removed after the report was written).
No `/tmp` writes. No installs (pacman paused; nothing needed — `curl` + `python3` sufficed).

| # | command (abridged) | exit | HTTP | bytes | sha256 | UTC |
|---|---|---|---|---|---|---|
| R1 | `curl -sS -L -D top.hdr -o top.html -w '%{http_code}' https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs` | 0 | 200 | 238,102 | `e4b371824bf51cfda6fd2a51ccd48bf3fb127abcd7d3e4ab9a55e07d591a1294` | 2026-10-28T15:39:00Z |
| R2 | same URL again (`-o top2.html`, `%{url_effective}`=`…/squashfs`, `num_redirects=0`) | 0 | 200 | 238,102 | `1d98ac86c9d768e6db2be77fe6fb261d7581092f027a83afdd3768c50e792feb` | 2026-10-28T15:40:34Z |
| R3 | `curl -sS -L -H 'Accept: application/vnd.github+json' 'https://api.github.com/repos/onekey-sec/unblob/contents/tests/integration/filesystem/squashfs?ref=26.6.4'` | 0 | 200 | 11,007 | `be3180fc1c5221b7e91b3e442d10109348f3a50f6b7cbdfe7d915b6353542e00` | 2026-10-28T15:39:20Z |
| R4 | same contents-API URL again | 0 | 200 | 11,007 | `be3180fc1c5221b7e91b3e442d10109348f3a50f6b7cbdfe7d915b6353542e00` (byte-identical) | 2026-10-28T15:40:42Z |
| R5 | `curl -sS -o r5.json -w '%{http_code}' …/git/ref/tags/26.6.4` | 0 | 200 | body sha256 `4801191bdda9b8acd9b179b24671edb19e797ed29deff645f03ec2a6040f1873` | `refs/tags/26.6.4`, object `commit 1fcc7a0a584a70a96c31f5a276c20944d199a089` | 2026-10-28T15:42:24Z→15:42:25Z |
| R6 | `…/git/ref/heads/26.6.4`; `…/git/tags/26.6.4` | 0 | 404, 404 | `af34d7e1c24c2c3bd1da5d50fee4e8711a488d218f814c6c4f644603390fdf52`, `c7c41d0458f933eec45bb557b18124b4b12cde3d69b84a13eecb81cd3cb9348c` | `{"message": "Not Found", …}` (lightweight tag: no annotated-tag object, no branch) | 2026-10-28T15:42:25Z |
| R7 | `curl -sS -o r7.md -w '%{http_code} %{size_download}' https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md` | 0 | 200 | 7,580 | `6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716` (same as an earlier fetch); `grep -c -F '__output__'` = **0**, grep exit **1** (no match) | 2026-10-28T15:42:25Z |

R1 vs R2 is the load-bearing pair: **the HTML page hash is per-request and is not an identity.**
Same length (238,102), 667 differing bytes, first difference at offset 27,429 inside
`<meta name="fetch-nonce" content="v2:…">`, last at 175,633; the parsed directory list is identical
across both (`payload.codeViewTreeRoute.tree.items` equal, n=11). The contents-API body (R3/R4) is
byte-stable, so **that** is the citable identity for this endpoint.

## 2. (a) Does the page load, and what does it list

Loads: **HTTP 200**, no redirect (`num_redirects=0`), 238,102 bytes. Directory index, no README
rendered (the directory contains no file), no LFS pointers, **zero files**.

11 entries, all `directory` (contents API `type: "dir"`, `size: 0`; HTML `contentType: "directory"`):

```
squashfs_v1   squashfs_v2   squashfs_v2_nonstandard   squashfs_v3
squashfs_v3_adaptive   squashfs_v3_broadcom   squashfs_v3_ddwrt   squashfs_v3_nonstandard
squashfs_v4_be   squashfs_v4_broadcom   squashfs_v4_le
```

Located anchors in the saved page (byte offsets in R1's `top.html`):
`<title>` at 27,041 → `unblob/tests/integration/filesystem/squashfs at 26.6.4 · onekey-sec/unblob · GitHub`;
`Folders and files` at 200,867; `aria-label="squashfs_v1, (Directory)"` at 203,491;
`aria-label="squashfs_v2, (Directory)"` at 205,598.

## 3. (b) A located quote from the TOP page that supports the row's scope — verdict: **none**

What the top page can quote is only its own index:

> `unblob/tests/integration/filesystem/squashfs at 26.6.4 · onekey-sec/unblob · GitHub`
> — `<title>`, byte 27,041 of the 238,102-byte page (9 words)

That quote (with the two `(Directory)` rows above it) supports exactly two things: the path exists at
tag `26.6.4`, and it contains `squashfs_v1` and `squashfs_v2` subtrees. It does **not** support the row's
scope as written — "committed expected member trees for `squashfs_v1` and `squashfs_v2`, both byte
orders, as content-addressed member bytes (4 endian trees, 22 files)". Byte order, `__output__`,
endian-tree count, the 22-file count, LFS pointers and member hashes are all at depth ≥ 2 below this
page. The top page carries **no prose at all**, so no sentence can be mined for the scope predicate.

Check with `grep -c -F` on R1 (each = 0):
`squashfs_v2.0_be.bin_extract` 0 · `__output__` 0 · `little_endian` 0 · `NOT handler code` 0 ·
`LFS` 0 · `oid sha256` 0.

So: the row is *openable* and its subject is confirmed, but the top page is not the page that carries
the row's measured shape. Exit 1 on "top page supports the scope predicate"; exit 0 on "top page
confirms the subject".

## 4. (c) Does the row's stated quote live on the top page?

No — and the split is sharper than the routing note says. The round-44 Gate "located quote" is two
things, and **neither is top-page text**:

1. `listing member squashfs_v2.0_be.bin_extract under squashfs_v2/big_endian/__output__` — a
   **descendant listing**. It is present in
   `.ufo/waves/round-44/w1/R44SrcOracle/listings/squashfs_v2__big_endian__squashfs_v2.0_be.bin_extract.json`
   and in the manifest's `files[]`; absent from the top page (0 occurrences).
2. `"NOT handler code, NOT extractor behaviour, NOT a C1 carrier"` — the **lane's own manifest prose**,
   not source text at any depth. `manifest.source.grounds` reads verbatim:
   `"second oracle: unblob's expected member trees for squashfs_v1/v2; NOT handler code, NOT extractor behaviour, NOT a C1 carrier"`.

Bounded negative on "the top URL was never fetched in round 44": the manifest's 10 listings have
`repo_path` suffixes only
`/squashfs_v{1,2}/{little,big}_endian/__output__` and
`/squashfs_v{1,2}/{little,big}_endian/__output__/*.bin_extract`; `depths = [3, 4]`;
`repo_path == tests/integration/filesystem/squashfs` → `[]`; `api_url` equal to the contents root → `[]`;
all 10 `http_status == 200`; all 10 `replayed_from_saved_receipt == true` (so round 44 did not even
fetch its descendants live at replay time — the manifest `started_at == finished_at`). No intermediate
directory (`squashfs_v1`, `squashfs_v1/big_endian`) was listed either.

## 5. (d) The exact corrected `opened`-cell wording I would accept

The column cannot be edited (CORPUS rule 2: a row present at BASE may differ only in `status`,
`recheck`, `used-by` — `corpus/lessons/round-45.md:42` restates it). So the correction is the lesson's
append, and it must carry the values the cell *would* have had. **Accept this text verbatim**, replacing
the current `### S138 correction (append-only)` body (line 35 ff.):

> The `opened` cell is `2026-10-28`, and this fetch is what earns it — round 44's window did not.
> `https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs` was first
> opened at 2026-10-28T15:39:00Z: HTTP 200, 238,102 bytes, 11 entries, all directories (`squashfs_v1`,
> `squashfs_v2`, `squashfs_v2_nonstandard`, five `squashfs_v3*`, three `squashfs_v4_*`), no files and no
> README. Its reproducible identity is the contents-API body at
> `…/contents/tests/integration/filesystem/squashfs?ref=26.6.4`: HTTP 200, 11,007 bytes, sha256
> `be3180fc1c5221b7e91b3e442d10109348f3a50f6b7cbdfe7d915b6353542e00`, byte-identical on two fetches 82 s
> apart; the HTML page hash is per-request (nonce/request-id) and must not be cited as a page identity.
> `refs/tags/26.6.4` is a lightweight tag whose object is commit
> `1fcc7a0a584a70a96c31f5a276c20944d199a089` — the commit the row names. Round 44's
> 11:10:29Z–11:12:37Z window is 10 listings at or below `squashfs_v{1,2}/<endian>/__output__`, all
> replays of saved receipts; none is of this URL, of `squashfs_v1`, or of `squashfs_v2`. The top page
> carries no prose: the member name `squashfs_v2.0_be.bin_extract` is a descendant-listing entry and
> "NOT handler code, NOT extractor behaviour, NOT a C1 carrier" is this lane's own
> `manifest.source.grounds`, so neither is a page quote. The row stays `mined`; the scope's measured
> shape (4 endian trees, 22 files, 152 B, 7 distinct sha256) is evidenced by the descendant member set,
> not by this page. No column was edited (CORPUS rule 2).

Short form, if the Gate table gets an S138 row (same facts, one cell):

> 2026-10-28T15:39:00Z, HTTP 200, 238,102 bytes, **11 dirs / 0 files**, top URL fetched itself (receipt
> `w1/R45W1SrcS138Fix/report.md`); identity = contents-API body `?ref=26.6.4` 11,007 B sha256
> `be3180fc…3542e00` (stable ×2), **not** the per-request HTML hash; tag `26.6.4` → commit
> `1fcc7a0a…a089`; round-44's window covered `__output__` descendants only, all replayed.

What I would **not** accept: the current draft's `"true as of 2026-10-28 and false as of
2026-10-28T11:12Z"` (see F2), any wording that cites `e4b37182…` as a page identity (F1), and any
wording that treats the `__output__` filename or the manifest grounds sentence as page text (F4).

## 6. Findings

**F1 — MEDIUM, no current defect, guard for the landing.** A `github.com` HTML page hash is not a page
identity: R1 and R2 differ in 667 bytes (per-request `fetch-nonce`, `request-id`) with an identical
parsed listing. Cite the contents-API body hash (`be3180fc…`) or the parsed item list instead. The
round-45 Gate cells for S140/S141 quote *page* sha256s — those are `git-scm.com` static pages, so they
are unaffected; the guard applies the moment any cell quotes a GitHub HTML page.

**F2 — MEDIUM, the draft under-claims its own receipt.** `corpus/lessons/round-45.md:39-42` says "This
round fetches the top URL itself (receipt …), so the cell's claim is true as of 2026-10-28 and false as
of 2026-10-28T11:12Z". Two problems: (i) the SOURCES cell is date-only, so "false as of <instant>" is not
a property a date cell can have — the correct statement is that the day's only opens before 15:39Z were
descendants; (ii) as written the sentence asserts a fetch it does not characterise (no status, bytes,
entry count or identity), so it is a claim resting on a receipt that did not exist until this file was
written. The wording in §5 closes both.

**F3 — LOW/MEDIUM, locates the defect in the wrong cell.** M45-2 says "an S-row `opened` cell credited a
listing replay of descendant paths". The registry `opened` cell is `2026-10-28` and credits nothing; the
credit lives in the round-44 **Gate** cell (`10 listings + 22 members`). The lesson should name both
cells, because the repair differs: the registry cell is repairable only by a later fetch (done), the
Gate cell by an append. This is a calibration distinction, not pedantry — an auditor checking only the
registry would find no descendant language at all.

**F4 — LOW, the "located quote" is half lane prose.** The round-44 Gate quote pairs a real descendant
filename with a sentence from `manifest.source.grounds`. Any future row doing this should label the
provenance per fragment; otherwise a later reader inherits "source says" for lane-authored text.

**F5 — POSITIVE (record it so it is not re-derived).** The row's commit binding verifies: `refs/tags/26.6.4`
→ `1fcc7a0a584a70a96c31f5a276c20944d199a089`, exactly the row's stated commit; it is a lightweight tags
(`git/tags/26.6.4` → 404), which is why there is no tag object to fetch.

**F6 — LOW, scope-boundary note.** The top page lists `squashfs_v2_nonstandard` beside `squashfs_v2`
(and five v3 variants, three v4). The row's scope ("v1 and v2, both byte orders, 4 endian trees, 22
files") is unaffected — the manifest covers only `v1`/`v2` — but a reader given only the top page cannot
tell which of the 11 directories the 22-file count belongs to. Do not cite the top page as evidence for
the counts.

**F7 — instrument gap, confirmed (candidate fix, not implemented; I am read-only).**
`scripts/sources-census.sh:660-662` validates only that `opened` parses and is not in the future
(`E08 opened not a past/present ISO date`, `:27`). Nothing in the 806-line script compares the opened
endpoint to the row's `source` URL, so M45-2 is invisible to the census — matching the lesson's
`captured-by: none`. A cheap candidate arm (not proposed as a claim): a row whose `opened` names a host
must have a receipt file under the round containing that URL string; here it would have failed at round
44 and passes now.

## 7. Checks, with semantic exit codes

| check | result | exit |
|---|---|---|
| top URL loads | HTTP 200, no redirect | **0** |
| top page lists `squashfs_v1` and `squashfs_v2` | yes, 11 dirs | **0** |
| top page contains files / README / LFS pointers | none (0 files) | **0** |
| top page carries a quote supporting the row's scope predicate | absent | **1** |
| row's member name `squashfs_v2.0_be.bin_extract` on the top page | absent (0) | **1** |
| row commit == target of tag `26.6.4` | equal | **0** |
| HTML page sha256 reproducible on a second fetch | differs (667 bytes) | **1** |
| contents-API body sha256 reproducible on a second fetch | identical | **0** |
| round-44 receipts contain a fetch of the top URL | none (bounded to the manifest) | **1** |
| frozen paths unchanged freeze→HEAD | `git diff --stat` empty | **0** |
| `sources-census.sh` detects an unopened-endpoint credit | not implemented | **2** |

## 8. Residual risk and verification gaps

- The negative in §4 is bounded to `corpus/evidence/round-44/oracle/manifest.json` and
  `w1/R44SrcOracle/listings/`. A round-44 fetch outside those receipts would be unrecorded and
  unknowable from here — so the honest claim is "no receipt records it", not "nobody looked".
- I did not re-fetch the 10 descendant listings or the 22 member URLs, so I did **not** re-verify the
  LFS `oid sha256` ↔ served-bytes equality, the 152-byte total or the 7 distinct hashes; those rest on
  the round-44 manifest (whose internal `failures` is `[]` and whose counts are `listings 10,
  replayed 10, files 22, total_bytes 152, distinct_content_sha256 7, lfs_resolved 22,
  pointer_verified 22`).
- I did not list the intermediate directories (`squashfs_v1`, `squashfs_v1/big_endian`), so the endian
  directory *names* are known only from the descendant listing paths, not from a live listing of their
  parent.
- `README.md` at 26.6.4 does not mention `__output__` (R7, count 0). I did not run a repo-wide search
  for the convention, so I cannot say where, if anywhere, unblob documents it.
- No installs, no `pacman`, no git mutation: `git status --porcelain -- corpus/SOURCES.md` was empty
  after this seat's work; the only new paths are this directory and `../R45W1SrcS138Fix.md`. Scratch
  `$S` removed after the receipts above were transcribed.
