# SentCreds — credential and vendor-bytes scan (round 52, wave 1)

Seat: SentCreds. Role: sentinel. Wave: `r52-w1` (build+attack, 64 seats).
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base `ab0eafedc41402b43b41a4362084119578dfe7ce`,
working tree `1842addcef3458515859b928b92d9bbd0a46c5d5`.
Full receipt: `.ufo/waves/round-52/w1/SentCreds/scan.md`.

## Verdict

**PASS.** The round-52 surface carries **no credential value** and **no vendor firmware byte**.
Zero hits against the 12 pinned vendor digests (4 vendor `.image` archives + 4 LE AVM members +
4 carrier pins from `tools/round-50/carriers.json`) across the lane working tree (48 313 files
hashed) **and** across every one of the 38 560 blobs in the git object database — the vendor bytes
are absent from the repository in *every* revision, not merely at the base.

## The three asked-for results

1. **Credentials in `plans/round-52-claims.md` and `.ufo/waves/round-52/`** — none. The lane's
   calibrated scanner (`credscan.py`, 12 classes) reported `live_hits 5` at the first pass, but
   **all five were one false positive**: the sibling seat's `r51-credential-words-by-line.tsv` was a
   word index whose `word` column contained `bearer`, and the scanner's pattern
   `(?i)\bbearer\s+([A-Za-z0-9._~+/-]{12,})` lets `\s` cross a **newline**, joining that word to the
   next row's path. Reproduced directly. No `Bearer <value>` exists anywhere in the surface
   (`grep -rc` over the wave tree: every file 0). The sibling has since reordered that file's
   columns, and a **final re-run over the surface as it now stands returns `live_hits 0`**
   (387 files, exit 0). A second, independent 14-class stdlib sweep returns `hit_count 0` over 269
   files. Every pattern hit in the wave tree was adjudicated by hand at `file:line`
   (scan.md §1c): all are prose, task strings, scanner fixtures, or the L1's own redaction markers.
   No `op://` refs, no private-key blocks, no URL with credentials, no token-shaped literal.
2. **Vendor bytes in the lane tree** — none. The largest files under
   `corpus/evidence/round-50/c1/` are the four `after.json` **REA receipts** (1.86 / 2.11 / 2.11 /
   2.18 MB), all `file -b` = `JSON text data`; the other four are `run.json` at 18.7 KB. Their bulk
   is metadata (`files[]` carries `path`/`size`/`sha256`/`runtime_address`, 3 955–4 709 rows each);
   the only payload field is `raw_result.execution.stdout.text` (2 033–2 141 chars) and
   `stdout.bytes` is an **integer** count. `chunks[]` holds offsets (`length 28368210`), not bytes.
   A ≥200-char base64 sweep inside the four receipts: 0. Every lane file over 1 MiB (57 of them at
   the base) was identified individually — JSON receipts, ASCII logs, unified-diff patches, ELF
   x86-64 fixtures, one pycryptodome wheel, two REA-member tars; **no image, no SquashFS
   superblock, no vendor digest match**. The wave tree is text-only (0 binary files, 0 NUL bytes).
3. **Accidental secrets in the round-52 claims and wave spec** — none. The claims file contains no
   URL at all; the wave tree's only absolute URLs are two credential-free `man7.org` man pages; the
   four vendor URLs in `tools/round-50/carriers.json` carry no userinfo and no query string.

## Carried L0, re-measured (not new, not a round-52 regression)

The open L0 at `plans/round-52-claims.md:259` is **still live**: three raw anonymous GitHub
`_gh_sess` values (348 / 364 / 352 chars) sit in pushed history at
`.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr`,
`.ufo/waves/round-49/w1/C1S138Reopen/receipts/top.hdr` and
`.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr`, retrievable via
`git show 14936cb9:<path>` / `git show 11ccdb72^:<path>` and reachable from `origin/main`. The
**tips are clean** (L1-redacted placeholders). Severity **low**: `logged_in=no` on every one —
server-issued anonymous session cookies, not user credentials. **Round-52 adds no new exposure**:
the raw-blob set is identical to the round-51 measurement, no round-51/52 commit introduces one,
and the wave tree holds no copy of any of the three. Remediation is an operator-side history
rewrite, which no seat may perform and which the round-52 claims explicitly do not re-append.

## The one actionable item for the L1

**F-4 — scanner defect (pre-existing, in the round-50 instrument, not round-52).**
`.ufo/waves/round-50/w3/SentReceipts/credscan.py`'s `bearer` pattern
`(?i)\bbearer\s+([A-Za-z0-9._~+/-]{12,})` matches across newlines and manufactures false
`live` hits from any file that has the word `bearer` at the end of a line. It reported
`live_hits 5` on a surface that is in fact clean — a scanner that cries wolf on a clean wave is a
false-red generator. The sibling seat's later rewrite of that file happened to remove the
symptom (the surface now re-scans to `live_hits 0`), but **the defect is latent** and will fire
again on the next file with that shape. Smallest remediation: `[ \t]+` instead of `\s+` in the
`bearer` pattern (and an audit of the sibling classes for the same shape), then re-run.
**Routing:** this is the round-50 instrument, outside this seat's write scope — reported, not
patched.

Also noted (no action for the credential/bytes surface): the round-52 fetcher draft's
network-guard selftests are **not yet run** and the draft is self-declared a "reduced
reconstruction" (`ExecFetchVendor/deltas.md`). Its vendor-byte containment is intact — the
lane-write guard (`refusing: %s is inside the lane`) resolves to the lane root from
`tools/round-52/`, `ALLOWED_HOST = download.avm.de` is enforced on both the initial request and
the redirect, urllib installs **no** cookie handler, and the fetcher records **no** HTTP headers
in any receipt.

## Evidence

`scan.md` (full receipt, with the per-command table, false-positive adjudication and limits),
`scan-commands.tsv` (14 command pairs: UTC time, exit code, stdout sha256, stderr sha256),
`lane-credscan-r52.json` (the calibrated scanner's raw output), `stdlib-cred-scan.json` (the
independent 14-class sweep: `hit_count 0`), `vendor-and-cookie-details.txt`,
`A2-pattern-hits-fileline.tsv`, `selfscan-final.json`.

**Self-scan of this seat's own output:** the first run of the calibrated scanner over my delivered
artifacts returned `live_hits 6` — my own receipt had reproduced 14-char prefixes of two real
`_gh_sess`/`_octo` values in the "raw value is retrievable" proof block, and the false-positive
table had quoted the two scanner-fixture pattern strings verbatim. Both were rewritten to classify
by class + value length without reproducing any literal. The re-run
(`selfscan-final.json`, sha256 `2461b666…a7ef`) returns **`live_hits 0`**, `placeholder_hits 6`,
exit 0. This seat's output is held to the same bar as the surface it scanned.

No REA run, no network fetch, no vendor download, no git mutation. No tool was installed, so the
pacman guard was never engaged.
