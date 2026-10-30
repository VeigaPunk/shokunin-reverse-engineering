# SentCreds — credential and vendor-bytes scan receipt

Round 51, attempt 1, wave 1 (build). Seat: SentCreds. Scope: credential classes + vendor-byte
containment over the round-51 claims file, the round-51 wave tree, the round-50 C1 evidence
receipts, and the lane tree at base `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.

Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Scratch: `/fast/scratch/hyaku/kaidoku-r51/w1-SentCreds` (removed after receipts were copied here).
Tooling: **none installed** — the lane's own calibrated scanner
`tools/round-50/w3/SentReceipts/credscan.py` (round-50 sentinel's instrument) was reused read-only,
plus stdlib `hashlib`/`json`/`re`/`subprocess` from the system Python. No pacman/`uv`/`npx`
transaction was performed, so the pacman guard was never engaged.

## Verdict

**PASS for the round-51 wave surface.** Zero live credential values in the round-51 claims file,
zero in `.ufo/waves/round-51/` (all 119 files), zero in `corpus/evidence/round-50/c1/`, zero in
`tools/round-51/`. **No vendor firmware bytes** live in the lane tree — neither the working tree
nor any blob in git history — and the largest files under `corpus/evidence/round-50/c1/` are JSON
receipts, not images.

One **carried** finding (not new, not a round-51 regression) is restated below with fresh
measurement: the open L0 "unredacted session cookies in pushed history" named at
`plans/round-51-claims.md:250` is still live in pushed history. The tips are clean; the blobs are
not.

## 1. Credential scan — round-51 surface

Calibrated scanner: `python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py` (patterns:
`set_cookie`, `cookie_hdr`, `authorization`, `x_api_key`, `github_token`, `github_pat`, `bearer`,
`op_ref`, `aws_key`, `sk_key`, `private_key`, `jwt`; live vs placeholder classed separately;
values never reproduced — only class + value length).

| # | Command (cwd = lane) | Exit | stdout sha256 | Result |
|---|---|---|---|---|
| 1 | `python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py plans/round-51-claims.md .ufo/waves/round-51/` | 0 | `7f049a101f64230e8b7de95a97e66ff9748bf5bead52b987d7520f95d28e958d` | `live_hits 0`, `placeholder_hits 0`, `synthetic_fixture_hits 0`; 119 files |
| 2 | `python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py corpus/evidence/round-50/c1/` | 0 | `53f4f5cdbb897b9bbaff1a025ab6c629c8ee93a702b06d60b0f902357460b97f` | `live_hits 0` |
| 3 | `python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py tools/round-51/` | 0 | `3b34eaf8f3a0ee827e8f6ac3084efa917382af7916e020a5ce0db0a91aa2753b` | `live_hits 0` (the untracked wave draft) |

All three at **2026-10-30T05:08:08Z–05:08:09Z**. Exact argv, exit code, stdout sha256, stdout and
stderr sha256 for every command in this receipt are in `final-receipts.json` (same directory).

**Final re-scan after both deliverables were written** (2026-10-30T05:10:13Z, exit 0, stdout
sha256 `a7b2609360441a1d…`, 141 files / 9 711 874 B):
`python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py plans/round-51-claims.md .ufo/waves/round-51/ tools/round-51/ corpus/evidence/round-50/c1/`
→ `live_hits 0`, `placeholder_hits 0`. The first draft of this receipt and of `SentCreds.md`
*quoted* the four synthetic literals of §3 (in order to classify them) and the scanner then
flagged those quotes as live-class hits; both files were rewritten to classify by class + value
length **without reproducing any literal**, and the re-scan above is the proof that the round-51
surface — this seat's own output included — is clean.

### 1a. False positives, itemised with `file:line`

Every credential-word hit inside the round-51 surface is a **word in prose or a path inside
vendor-derived metadata**, never a value. No value is reproduced here.

| `file:line` | Word | What it is |
|---|---|---|
| `plans/round-51-claims.md:250` | `session cookies` | The carried-L0 line naming the *open issue* ("unredacted session cookies in pushed history — `kaidoku \| round-50` stands"). No value; no `Set-Cookie` header text. |
| `plans/round-51-claims.md` (all) | — | A broad grep for `cookie\|token\|Set-Cookie\|op://\|secret\|password\|authoriz\|credential` returns exactly **one** line (`:250`). Nothing else. |
| `.ufo/waves/round-51/gen-w1.py:21` | `Set-Cookie`, `session cookies`, `tokens` | The wave contract's own prohibition text ("Never paste session cookies, tokens or `Set-Cookie` headers into any receipt"). Instruction, not data. |
| `.ufo/waves/round-51/gen-w1.py:138` | `session cookies`, `Set-Cookie`, `op://`, `private keys` | **This seat's own task text**, quoted into the generator. Instruction, not data. |
| `.ufo/waves/round-51/w1-spec.json:5`, `:175`; `w1-dispatch.json:289`, `:459` | same | The same contract text, embedded verbatim in the dispatch payload (the JSON escapes it as `\u2014`-style / `\n` strings). Instruction, not data. |
| `corpus/evidence/round-50/c1/{c6430,c6490,g7581,g7582}/after.json:1` (single-line JSON) | `cookie` ×10/carrier, `password`/`passwd` ×18/carrier | **Vendor firmware *file paths* inside the extraction manifest**: `usr/lua/webuicookie.lua`, `usr/www/avm/js/cookie.js`, `usr/www/avme/js/cookie.js`, `usr/www/myfritz/avm/js/cookie.js`, `usr/www/myfritz/avme/js/cookie.js`, `usr/www/avm/no_password.lua`, `usr/www/avm/sso_password.js`, `usr/www/avme/sso_password.js`, `usr/www/avm/js/password_checker.js`, `etc/fritzbox_resetpassword.html`, `sbin/smbpasswd`, `etc/passwd`, `usr/bin/passwd`. Path strings only — no credential bytes, no HTTP headers. |
| `.ufo/waves/round-51/w1/ExecCounterV2/c1-counter.py:583`, `:2446`, `:2447`, `:260`, `:2837`, `:2839`, `:4403`, `:4408`, `:4409`, `:4412` | `token` | A **lexical helper**: `def sid_tokens(text)` and the `token='LE AVM'` argument of the frontier-note builder. "token" = a lexeme, not a secret. |
| `.ufo/waves/round-51/w1/ExecTriV6/sqfs-triage-v6.py:98`, `:99`, `:118`, `:457`, `:460`, `:461`, `:462`, `:475`, `:489`, `:491`, `:494`, `:495`, `:497`, `:498`, `:530`, `:654`, `:665`, `:666`, `:687`, `:688`, `:813` | `token` | The triage **action-vocabulary tokenizer** (`action_re`, `token_re`, `command_tokens`). "token" = an action word. |
| `.ufo/waves/round-51/w1/ScribeScorecard/section.md:102`; `ScribeScorecard.md:155` | `cookie` | Prose reference to "the carried L0 cookie note". |
| `.ufo/waves/round-51/w1/ExecMisrootSweep.md:17` | — | "Filename classification … containing these tokens" — the sweep helper's prose. |

**`op://` refs, private keys, `AKIA*`, `ghp_*`, `github_pat_*`, JWTs: zero** in the round-51 surface.

### 1b. Round-51 census receipt — no embedded credentials

`grep -nEi 'set-cookie|cookie|authorization|bearer |api[_-]?key|passw|secret|token|op://|PRIVATE KEY|AKIA|ghp_|xox' .ufo/waves/round-51/l1/sources-census-start.txt`
→ **exit 1, 0 bytes out** (no match). The receipt is 24 lines: a header, 19 `W04` duplicate-URL
rows, and one `ok` row (`rows: 156`). Every URL in it is a **bare host + path with no scheme and no
userinfo** (`github.com/…`, `registry.npmjs.org/…`, `raw.githubusercontent.com/…`, `www.wireshark.org/…`).
No `https://user:pass@host` form appears anywhere.

The round-51 re-derived census draft `.ufo/waves/round-51/w1/ExecCensusDrift/census3.json` contains
**0 URL strings** at all (`grep -c http` → 0): 55 registry paths, provenance, counts, and the
13-path `registry_outside_census2` drift list. Nothing credential-shaped.

All seven round-51 JSON receipts were parsed for URL userinfo (`://[^/\s]*:[^/@\s]*@`): **0
credentialed URLs** in `census3.json`, `source-capture.json`, `input-receipt.json`, `inspection.json`,
`source-review.json`, `count-receipt.json`, `gap-rule-v2.json` (several contain **no** URLs at all).

### 1c. `tools/round-50/carriers.json` — the only vendor URL source

4 URLs, all `https://download.avm.de/fritzbox/…`. **0 credentialed URLs**; the host set is
`{download.avm.de}` alone. The `notes.http_etag` / `notes.http_last_modified` fields are response
*metadata* (an ETag and a date), not `Set-Cookie`.

## 2. Vendor-bytes containment

### 2a. `corpus/evidence/round-50/c1/` — files over 1 MiB

`find corpus/evidence/round-50/c1 -type f -size +1M -printf '%s\t%p\n'` → exit 0,
stdout sha256 `066594600569646cd6c9a98f098a1354e5f462b6a192c780d3b42c1432269259`:

```
2111348	corpus/evidence/round-50/c1/g7581/after.json
2114315	corpus/evidence/round-50/c1/g7582/after.json
2183265	corpus/evidence/round-50/c1/c6490/after.json
1862743	corpus/evidence/round-50/c1/c6430/after.json
```

**Four files, all `after.json`, all JSON text data** (`file` → `JSON text data`, stdout sha256
`1a84a5b33f24c935a352941828e6c4293a2c924438a9c12666c2119696af9d1b`). **No images, no binaries, no
firmware.** The eight files in the directory are exactly these four `after.json` plus four
`run.json` (18 683–18 716 B each, `JSON text data`, stdout sha256 `333fee26c837c5ae70452982f679147d1eab18cc44d700051e7ffa005f0a0fe1`).

Why the `after.json` files are large is worth stating plainly, because size alone would look
alarming: they are **extraction manifests, not payloads**. Per carrier, `after.json` holds ~4 556
`files[]` entries and ~637 `extraction_gaps[]` entries, each carrying a `relative_path`, `size`,
`sha256`, `mime_type` and (for gaps) a `handler`/`provider_id` — plus `raw_result.execution.stdout`
(2 112 B of tool chatter). The only `bytes`-named keys are **counts** (`stdout.bytes 2112`,
`stderr.bytes 0`, `published_bytes 108726608`, `max_output_bytes 536870912`); the only `sha256`
values are per-file digests. Measured: **0** base64 runs ≥300 chars, **0** raw-hex runs ≥200 chars
beyond the 64-char digests, **0** control bytes, and every file decodes as strict UTF-8 JSON.

`sha256sum` of all eight receipts (stdout sha256 `963ddb33213d1490037451a96bd53fcf290838152260943ba0bc16556f911b2e`):

```
30db72bdf2aa84e6d470b98acf5224c147eab5c070f845b38bc91b453f11c64c  corpus/evidence/round-50/c1/c6430/after.json
2c21f26464235334c330d42058c4b92485a688db65c05438b56c7690a0381aed  corpus/evidence/round-50/c1/c6490/after.json
ff481957b42cb418c2264771c60ebf5c4fda2db76f225d86606b2c0bf96c74a7  corpus/evidence/round-50/c1/g7581/after.json
f250f31585f6137755815062243a4fd5881affa794da583c5c64910e3dc19665  corpus/evidence/round-50/c1/g7582/after.json
cbf21bf830cd965cb48d58bfa7aa2113fba323bd864d3d815f1312e6ec92e65d  corpus/evidence/round-50/c1/c6430/run.json
c944f9783130e021890306d9ec41ecdbfa70ebc27de8f042b4fe609aaec5a775  corpus/evidence/round-50/c1/c6490/run.json
dbe0c9a649f80e673f062f04f7fb857e4db369a03d9a5fd245c119d44853874b  corpus/evidence/round-50/c1/g7581/run.json
90b32a9f56874a04eebb2c25f4d1f0783063f3033b370b76f1f81047fd1e494d  corpus/evidence/round-50/c1/g7582/run.json
```

### 2b. No AVM vendor bytes anywhere in the lane tree

The four carrier pins, the four vendor **image** pins and the four tar-**member** pins from
`tools/round-50/carriers.json` (12 sha256 values) were searched against **every** file ≥ 100 000 B
in the working tree (1 019 files hashed) and against **every blob > 1 MiB in the entire git
history** (48 900 objects enumerated; 55 blobs > 1 MiB; all 55 hashed):

> **AVM-pinned vendor bytes found: NONE** — in the working tree *and* in the full history.

Supplementary check: every SquashFS-magic file in `corpus/` was parsed for the **AVM marker**
(`mkfs_time == bytes_used`, the property that distinguishes AVM-written images — see
`tools/round-41/sqfs-list.py:263`). Every lane-tree SquashFS is a **non-marker** fixture
(`mkfs_time` 0 / 1700000000 / 177 / …, `bytes_used` different or 0). No AVM-marked image is
committed anywhere. The largest lane-tree binaries are unrelated: `corpus/evidence/round-34/elf/e10.bin`
(2 939 928 B, `ELF 64-bit LSB shared object, x86-64` — a Linux shared object, not firmware) and
`corpus/evidence/round-42/local-sources/S048/rea-agents-6.5.0-cited-members.tar` (2 324 480 B, the
npm package tarball — not vendor firmware).

So the round-50 receipts are **metadata about vendor bytes** (paths, sizes, digests), never the
bytes themselves — the AVM licence containment holds.

### 2c. The round-51 fetcher draft does not capture response headers

`.ufo/waves/round-51/w1/ExecFetchSelftest/fetch-vendor.py` (the repaired round-51 copy) has header
handling **byte-identical** to `tools/round-50/fetch-vendor.py`: the only `hdrs` occurrences are the
`urllib` `redirect_request(self, req, fp, code, msg, hdrs, newurl)` signature and the
`urllib.error.HTTPError(..., hdrs, fp)` raise — no `getheaders()`, no `Set-Cookie` read, no header
dump into any receipt. Its receipts carry the URL, hashes and byte counts only. The guard itself
(`ALLOWED_HOST = 'download.avm.de'`, https-scheme check on both the initial URL and every redirect)
is intact at lines 61, 102 and 112.

### 2d. The data-run harness copies only TSVs into the lane

`tools/round-51/c1-run.sh` (the untracked wave draft) writes into
`corpus/evidence/round-51/c1/<id>/` only `after.json`, `run.json` and four **text TSVs**
(`oracle.tsv`, `nonregular.tsv`, `oracle-unsquashfs.tsv`, `oracle-check.tsv` — lines 616–619). No
firmware image is ever copied into the lane. The extraction tree and the carrier cache stay under
`/fast/scratch/hyaku/kaidoku-r51/`.

## 3. Whole-lane-tree sweep (context, not a round-51 defect)

A full-tree sweep (47 715 files, 735 608 832 B) with the same 12 patterns found **9 live-class hits,
all outside the round-51 surface, all in old rounds and all synthetic**:

| `file` | class | value_len | what it is |
|---|---|---|---|
| `.ufo/waves/round-49/w2/W2Sentinel/selftest.py` | `bearer` / `op_ref` / `aws_key` / `sk_key` / `private_key` | 16 / 21 / 20 / 37 / 35 | The round-49 sentinel's **own scanner self-test fixtures** — synthetic literals such as a fake AWS access-key id and a fake OpenSSH private-key header, each assigned to a synthetic label. Already whitelisted by the round-50 scanner as `KNOWN_SCANNER_FIXTURES`. |
| `.ufo/waves/arc3-loop1-round3/claims/c2/EX-31/evidence/independent/secret-echo-finding.txt` | `sk_key` | 49 | A synthetic placeholder whose own text says it is a demo value, not a real one ("SYNTHETIC", "not-a-re[al]"). |
| `.ufo/waves/round-20/w1/ScoutSlugEscape.md` | `sk_key` | 30 | A **fictional** hex token (the file is a report *about* a secret-file-detection rule; the literal is a made-up example assigned to a `SECRET_TOKEN=` key). |
| `.ufo/waves/round-20/w1/patches/WasmCompareLeg-2.patch` | `sk_key` | 27 | A random base64 run inside a 10.7 MB binary patch. **Coincidental substring**, not a key. |

Per this receipt's own discipline (values are never reproduced), none of the four literals is quoted
here; only the class and the value length are given.

15 placeholder-class hits, all `[redacted …]` / `<redacted>` redaction markers.

### Carried L0 (restated, freshly measured — NOT a round-51 regression)

`plans/round-51-claims.md:250` carries the open L0 "unredacted session cookies in pushed history —
`kaidoku | round-50` stands; not re-appended". Re-measured against `origin/main`:

* **Tip tree: clean.** All 15 `set-cookie:` lines in the 64 `.hdr*` files at `HEAD` are
  placeholders — 9-char `[redacted…]` or 10-char `<redacted>` shapes. Zero live values.
* **History: not clean.** Three blobs carrying **live** `_gh_sess` / `_octo` values remain reachable
  from `origin/main` (`git rev-list origin/main --objects`):

  | blob | path | live value lengths |
  |---|---|---|
  | `ba6b0d6ec4d791ced391a08523bfd2e66ddbb2b6` | `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr` | `_gh_sess` 352, `_octo` 26, `logged_in` 2 |
  | `5f8478b4fc25c8b1c5718eeafba2591f62010a1f` | `.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr` | `_gh_sess` 348, `_octo` 27, `logged_in` 2 |
  | `815e2951e830e2ffea5c0995444c19a47225879b` | `.ufo/waves/round-49/w1/C1S138Reopen/receipts/top.hdr` | `_gh_sess` 364, `_octo` 27, `logged_in` 2 |

  The redacted successor blobs (`f89013cd…`, `54e21756…`) sit at the tip; the live ones remain in
  the object store and are reachable from the pushed ref. This is the finding the round-50
  sentinel already recorded (`.ufo/waves/round-50/w1/C1SentinelFetch.md:30` S2/S3,
  `.ufo/waves/round-50/w3/SentReceipts.md:64-65`) and the round-50 closure left it open by
  decision; **this wave adds nothing to it and re-appends nothing.** Impact is low
  (`logged_in=no` ⇒ anonymous GitHub session cookies), and remediation requires either a
  history rewrite + force-push or an operator-authorised rotation, both outside a wave seat's
  remit.

  A full-history scan of the 156 `hdr`/`cookie`/`sess`-named paths found 28 live header hits, all
  from these three blobs plus their round-49 re-captures; every other hit is a placeholder.

## 4. Lane hygiene observed (reported, not touched)

`git status --porcelain` (exit 0, stdout sha256 `c0b654f50dd7144133ca8cbf4bd9be3cc9f74716a288e179fcd68f21b71e4e09`)
at 2026-10-30T05:08:09Z shows three untracked entries:

```
?? .ufo/waves/round-51/w1.ready.dispatched
?? .ufo/waves/round-51/w1/
?? tools/round-51/
```

The third is a **wave-1 draft (`tools/round-51/c1-run.sh`, 46 142 B, mtime 2026-10-30 01:58)
sitting in the lane's `tools/`** instead of under a seat directory — the wave contract puts drafts
under `.ufo/waves/round-51/w1/<seat>/`. `ScribeReadme.md:80-85` already reported this. I did not
touch it (read-only listing only). It is credential-clean (§1, command 3) and vendor-byte-clean
(§2d), so it is a **hygiene** issue, not a containment issue; the L1 should decide whether it is
moved into its owning seat's directory before the freeze so the freeze remains the single commit
that adds the round-51 instruments.

`git rev-parse HEAD` → `39f41d4f15a87689a41c16c5c17ed885fbfb7da3`; the base under test is
`f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.

## 5. Limits of this scan (stated, not hidden)

* No live REA run, no `--data-run`, no vendor download was performed by this seat (wave contract:
  the L1 alone runs REA after the freeze). The receipts examined are the **committed round-50**
  ones, not fresh data.
* The credential scan is **pattern-based**; a secret that matches none of the 12 classes, or that is
  split across lines/encodings, would not be found. The whole-tree sweep was the mitigation, and
  its 9 hits were each manually classified above.
* The vendor-byte check is **pin-based** (12 sha256 from `carriers.json`) plus a SquashFS
  marker check. It proves the *four pinned AVM images* are absent; a re-encoded or differently
  carved vendor image would not be caught by the pin check — the marker check covers the AVM-image
  class, but a non-SquashFS vendor payload would not be covered by either.
* No file in `.git/` internals beyond the object database was inspected for content.
* The tree changed under the scan (siblings kept writing): the counts above are as of the stated
  UTC stamps. The round-51 surface was re-scanned at 05:08:08Z, after the last sibling write
  observed at that moment.

## 6. Files

* `final-receipts.json` — exact argv, exit code, stdout/stderr sha256, stdout byte count and UTC
  stamp for all 11 commands in this receipt.
* `whole-tree-credscan.json` — the whole-lane-tree sweep result (47 715 files; 9 live-class hits,
  15 placeholders; each hit classified in §3).
