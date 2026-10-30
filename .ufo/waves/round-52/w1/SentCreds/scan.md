# SentCreds — credential and vendor-bytes scan receipt

Round 52, attempt 1, wave 1 (`r52-w1`, build+attack). Seat: SentCreds, role: sentinel.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
Base scanned: `ab0eafedc41402b43b41a4362084119578dfe7ce` (claims draft); working tree at
`1842addcef3458515859b928b92d9bbd0a46c5d5`.
Scratch: `/fast/scratch/hyaku/kaidoku-r52/w1-SentCreds` (removed after receipts were copied here).

Tooling: **none installed.** All checks used the lane's own calibrated scanner
`tools/../.ufo/waves/round-50/w3/SentReceipts/credscan.py` (round-50 sentinel's instrument, read-only),
the lane's own `tools/round-50/fetch-vendor.py` (read-only source inspection), and stdlib
`hashlib`/`json`/`re`/`subprocess`/`base64` from the system Python 3.14. No pacman / `uv tool` /
`npx` / `~/.local/bin` transaction was performed, so the pacman guard was never engaged.

## Verdict

**PASS for the round-52 wave surface.** Zero live credential values in
`plans/round-52-claims.md`, zero in `.ufo/waves/round-52/` (304 files, 6.6 MB scanned at the first
pass; 387 files and `live_hits 0` on the final re-run), zero in
`corpus/evidence/round-50/c1/`. **No vendor firmware bytes** live in the lane tree — neither in the
working tree (48 313 files hashed) nor in **any** of the 38 560 blobs in the whole git object
database — and the largest files under `corpus/evidence/round-50/c1/` are JSON receipts, not
images.

One **carried** finding (not new, not a round-52 regression) is restated below with fresh
measurement: the open L0 "unredacted session cookies in pushed history" named at
`plans/round-52-claims.md:259` is still live in pushed history. The tips are clean; the blobs are
not. Round-52 adds **no new** exposure: the raw-cookie blob set is byte-identical to the round-51
measurement (same 3 blobs), and no round-52 commit introduces one.

---

## 1. Credential scan — round-52 surface

### 1a. Calibrated lane scanner (12 credential classes)

```
python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py plans/round-52-claims.md .ufo/waves/round-52/
```

Exit **1**, stdout sha256 `8a2c231524bb3a7c6d1c8b835386670da6fd1db79c692061191a41e8e2b906d1`,
stderr empty. Output: `files_scanned 304`, `bytes_scanned 6 600 009`, `live_hits 5`,
`placeholder_hits 0`, `synthetic_fixture_hits 0`.

**All 5 `live` hits are one scanner false positive, not a credential.** All five sit in a single
sibling-seat receipt —
`.ufo/waves/round-52/w1/SentSecrets/receipts/r51-credential-words-by-line.tsv` (at scan time blob
`5e0f4fe5f44739a759fea9371dae8f15475956b669997bc2d2dad41f218ddc78`) — and every one has class
`bearer` with a `value_len` of 40/40/40/52/57. That file is a **word index** listing which
round-51 files contain the *word* `bearer`. The scanner's `bearer` pattern is

```python
'bearer': re.compile(r'(?i)\bbearer\s+([A-Za-z0-9._~+/-]{12,})'),
```

and `\s` matches a **newline**, so the word `bearer` at the end of one TSV row is joined by `\s+`
to the start of the next row — a path such as `.ufo/waves/round-51/w1/SentCreds/scan.md` — which
satisfies the value charset and is then read as a "bearer token". Reproduced directly:

```
python3 -c "import re; pat=re.compile(r'(?i)\bbearer\s+([A-Za-z0-9._~+/-]{12,})');
            print(bool(pat.search('bearer\n.ufo/waves/round-51/x.json')))"
→ True
```

The five matched rows were exactly the five rows of that index whose `word` column was `bearer`
(lines 200, 219, 282, 294, 311). **No `Bearer <value>` token exists anywhere in the round-52
surface**: `grep -rc -iE "bearer [A-Za-z0-9._~+/-]{12,}" .ufo/waves/round-52/` returns no file
with a non-zero count.

> **State at yield (re-measured):** the sibling seat rewrote that index in the interim, changing
> its column order (blob now `f6bcbc6f31638ce37e58e2d22b06582c02b56f789b9f025f40f725893c89940b`),
> which incidentally removed the false positive. A **re-run of the same command over the surface as
> it now stands** returns **`live_hits 0`**, `placeholder_hits 6`, `files_scanned 387`, exit **0**.
> The scanner's newline-crossing behaviour is nevertheless a **latent defect of the round-50
> instrument**, demonstrated above: on the previous column layout the same pattern matches 1 time
> per occurrence, on the current layout 0 times. It is out of this seat's remediation scope and is
> reported to the L1 as a scanner-calibration note (see §5, F-4).

### 1b. Independent stdlib sweep (14 classes, cross-check)

A separate scanner written for this seat (classes: `set-cookie-header`, `cookie-header`,
`authorization-header`, `bearer-token`, `github-token`, `github-pat`, `aws-access-key`,
`slack-token`, `anthropic-key`, `private-key-block`, `op-vault-ref`, `jwt`,
`url-with-credentials`, `password-assignment`) was run over the round-52 surface
(claims file + `.ufo/waves/round-52/`, 269 files): **`hit_count 0`**. Over the whole lane working
tree (48 345 files) it produced 31 `(file, class)` pairs, every one explained in §1c.

### 1c. False positives, itemised with `file:line`

| `file:line` | Word | What it is |
|---|---|---|
| `plans/round-52-claims.md:259` | `session cookies` | The carried-L0 line naming the *open issue* ("unredacted session cookies in pushed history — `kaidoku \| round-50` stands"). A prose reference; no value, no header text. |
| `.ufo/waves/round-52/gen-w1.py:69` | `session cookies, tokens or Set-Cookie headers` | The wave-spec **instruction text** telling seats never to paste cookies into receipts. |
| `.ufo/waves/round-52/gen-w1.py:262` | `never save Set-Cookie` | The ExecCarrierProbe seat's instruction to strip headers. |
| `.ufo/waves/round-52/gen-w1.py:799,808,811` | `Set-Cookie, op:// refs, private keys` | This seat's own task string (embedded in the generator). |
| `.ufo/waves/round-52/w1-spec.json:5,60,285,290` | same four classes | The same task strings, JSON-escaped into the spec. |
| `.ufo/waves/round-52/w1-dispatch.json:485,540,765,770` | same four classes | The same task strings, JSON-escaped into the dispatch file. |
| `.ufo/waves/round-52/w1/ScoutQualRows/map.md:80` | `set-cookie`, `_gh_sess`, `_octo` | The **D6 carried-L0 row** naming the open issue and its path. Names only, no values. |
| `.ufo/waves/round-52/w1/ScribeSources/rows.md:59` | `Set-Cookie` | The SOURCES gate row recording `grep -ci set-cookie` → 0 on the fetched page. |
| `.ufo/waves/round-52/w1/ScribeSources/receipts/fetch-receipt.tsv:12` | `set_cookie_headers` | The receipt's own field `set_cookie_headers  0 (grep -ci set-cookie on the response headers: 0)`. A **count of zero**. |
| `.ufo/waves/round-52/w1/SentSecrets/receipts/receipts.json:69,82,95,108,117,121,130,251,264,277,303,312,316,325,329,338` | `op://`, `bearer`, `set-cookie` | The sibling sentinel's own scan receipts: the `argv` strings of its grep commands and the `stdout_head` of a grep over round-51 that lists *credential words*, not values. |

The whole-tree sweep's remaining pairs, all outside the round-52 surface and all benign:

| `file` | Class | What it is |
|---|---|---|
| `.ufo/waves/round-38/r38-w1-results.json`, `r38-w2-results.json`, `round-39/r39-w1-results.json`, `r39-w2-results.json`, `round-40/r40-w1/R40Sentinel.md`, `round-40/r40-w1/artifacts/R40CL6Receipts/*.json`, `round-40/r40-w1/artifacts/R40Sentinel/04-secrets.txt`, `round-39/w1/R39Sentinel.md`, `round-39/w2/artifacts/R39W2Sentinel/04-secrets.txt` | `op_ref`, `private_key` | Round-38/39/40 sentinel **scanner fixtures**: the two pattern strings (a vault-ref scheme reference and a PEM private-key header) used to prove the scanner fires. Values not reproduced here. Synthetic, carried, not new. |
| `.ufo/waves/round-49/w2/W2Sentinel/selftest.py` | `bearer`, `aws_key`, `anthropic`, `op_ref`, `private_key` | The round-49 scanner's own **synthetic self-test positives**. |
| `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr:15-17`, `.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr:15-17`, `.ufo/waves/round-49/w1/C1S138Reopen/receipts/top.hdr:15-17`, `.ufo/waves/round-49/w2/W2Sentinel/cookie-receipts-redacted-*.hdr.txt:15-17` | `set-cookie-raw` | **Redacted in the working tree** — every value is the literal `[redacted by L1 …]` / `[redacted by L1 round 50: …]` placeholder. The sweep's negative lookahead excludes `[redacted`; these rows matched only because the *placeholder text itself* begins `[redacted by L1…` after a `set-cookie: ` prefix — i.e. these are the redaction markers, not values. The **raw** values live only in history (§2). |
| `.ufo/waves/round-50/w3/SentReceipts/redirect-real.py:15`, `.ufo/waves/round-50/w3/SentReceipts/receipts/r11-redirect-policy.stdout:29` | `url-with-credentials` | `https://u:p@evil.example/x` — a **synthetic redirect-rejection fixture** proving the fetcher refuses a credential-bearing off-host URL. |
| `.ufo/waves/round-51/w1/SentCreds/scan.md:78` | `url-with-credentials` | `https://user:pass@host` — a round-51 doc example of the class. |

### 1d. Claim-specific secret check (round-52 claims + wave spec)

| Check | Result |
|---|---|
| URLs carrying credentials in `plans/round-52-claims.md` | **0** (the claims file contains no `http(s)://` URL at all). |
| URLs carrying credentials in `.ufo/waves/round-52/` | **0**. The only absolute URLs in the wave tree are `https://man7.org/linux/man-pages/man2/mknod.2.html` and `https://man7.org/linux/man-pages/man7/capabilities.7.html` (both credential-free). |
| URLs carrying credentials in `tools/round-50/carriers.json` (the four vendor URLs) | **0**. All four are `https://download.avm.de/fritzbox/….image`, no userinfo component, no query string. |
| `op://` vault refs (real, not the pattern string) | **0** in the round-52 surface. The 8 hits are the literal pattern `op://` inside the wave-spec task strings and a sibling's `grep` argv. |
| `BEGIN … PRIVATE KEY` blocks | **0**. |
| API-key-shaped literals (`ghp_`, `github_pat_`, `AKIA…`, `xox[baprs]-`, `sk-ant-`, JWT `eyJ…`) | **0** in the round-52 surface. |
| Long base64 payloads ≥120 chars that decode | **0** (every ≥120-char base64-ish run in the wave tree is a hex digest). |
| Files with NUL bytes (i.e. embedded binary) | **0**. |

---

## 2. Vendor firmware bytes — containment

### 2a. Content-hash scan against the 12 pinned vendor digests

The 12 digests taken from `tools/round-50/carriers.json` (4 × `external.image_sha256`,
4 × `external.member_sha256`, 4 × top-level carrier `sha256`) were used as an exact-match oracle.

| Scope | Command | Result |
|---|---|---|
| Lane working tree (all files, `.git`/`.jj` excluded) | stdlib `hashlib` walk, 48 313 files hashed | **0 hits** |
| **Every blob in the git object database** (all of history, not just the base tree) | `git cat-file --batch-all-objects` + sha256, 38 560 blobs hashed, 55 of them >1 MiB | **0 hits** |
| Base tree at `ab0eafedc` | `git ls-tree -r -l` + `git cat-file blob` + sha256, 44 919 blobs hashed | **0 hits** |

So the four carrier member images, the four vendor `.image` archives, and the four LE AVM members
are **absent from the entire repository, in every revision**. A size filter confirms the same from
the other direction: no blob in the tree has a size equal to any known vendor length
(32 010 240 / 32 256 000 / 39 741 440 / 35 911 680 image bytes; 28 368 210 / 28 607 082 /
28 200 029 / 23 861 507 member bytes).

### 2b. Magic-byte scan for SquashFS vendor images

`grep -rl --binary-files=text "hsqs"` over the whole lane tree returns only **text** files that
*mention* the magic string (`corpus/knowledge/*.md`, `corpus/lessons/*.md`) and the lane's own
**synthetic** SquashFS fixtures (`corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh`,
`k2-le-gzip.sqsh`, `corpus/evidence/round-{39,40,41}/c2/heldout/*/carrier.sqsh` — round-36's own
`carriers.json` labels K1 *"synthetic"*). None of them matches a vendor digest. The one committed
tar (`corpus/evidence/round-42/local-sources/S048/rea-agents-6.5.0-cited-members.tar`, 28 members)
was extracted to scratch and scanned: **no `hsqs` member**. No file >1 MiB in the base tree starts
with the SquashFS superblock.

### 2c. `corpus/evidence/round-50/c1/` — the largest files are receipts, not images

`git ls-tree -r -l ab0eafedc -- corpus/evidence/round-50/c1/` returns exactly **8** files, all
JSON text (`file -b` → `JSON text data` for all 8). **Files over 1 MiB: 4**, all `after.json`
receipts:

| Bytes | Path | Identity |
|---|---|---|
| 2 183 265 | `corpus/evidence/round-50/c1/c6490/after.json` | REA receipt (JSON) — the round-50 after-arm envelope |
| 2 114 315 | `corpus/evidence/round-50/c1/g7582/after.json` | REA receipt (JSON) |
| 2 111 348 | `corpus/evidence/round-50/c1/g7581/after.json` | REA receipt (JSON) |
| 1 862 743 | `corpus/evidence/round-50/c1/c6430/after.json` | REA receipt (JSON) |

The remaining four (`run.json`, 18.7 KB each) are below 1 MiB. **No image, no binary, no
firmware.** Their bulk is explained: `normalized_result.files[]` holds 3 955–4 709 entries per
carrier with `path`, `size`, `sha256`, `mime_type`, `analysis_depth`, `runtime_address`,
`original_file_range` — i.e. **metadata only**. The scan for embedded content confirms it: the
only payload-bearing field is `raw_result.execution.stdout.text` (2 033–2 141 chars); `stdout.bytes`
is an **integer** count (2 006–2 112), not a blob; `normalized_result.chunks[]` holds one entry per
carrier carrying `range`/`root_file_range` offsets and `length` (28 368 210 for g7581) — **offsets,
not bytes**. A regex sweep for base64-ish runs ≥200 chars inside the four receipts found **0**, and
no field named `content`/`data`/`body`/`hex`/`base64`/`payload`/`blob` exists in any of them.

### 2d. Lane tree >1 MiB — every large file identified (base tree, 57 files)

All 57 files over 1 MiB at `ab0eafedc` are JSON / ASCII text / patches / ELF fixtures / one
pycryptodome wheel / two REA-member tars — **no vendor image**. The largest are
`.ufo/waves/round-20/w1/patches/WasmCompareLeg-2.patch` (10 709 414 B, unified diff),
`.ufo/waves/round-20/w1/patches/WasmInspectLeg-2.patch` (8 703 728 B, unified diff), and
`.ufo/waves/arc3-loop1-round12/claims/c1/EX-7/evidence/function-copy.json` (6 212 446 B, JSON).
The binary files are `corpus/evidence/round-34/elf/e{05,10,11}.bin` (ELF 64-bit x86-64 objects,
1.1–2.9 MB, `file` confirms `ELF 64-bit LSB …`, **no** `fritz`/`AVM`/`FRITZ!` string, and no
vendor digest match), the `pycryptodome` wheel, and the two REA-cited-members tars.

### 2e. The round-52 wave tree holds no vendor bytes either

`.ufo/waves/round-52/` is 126 files; the `file -b` census is 81 JSON + 43 ASCII + 13 Python +
7 UTF-8 + 2 shell + 1 diff + 1 HTML + 22 empty — **zero binary files, zero NUL bytes**. The only
file over 1 MiB is `.ufo/waves/round-52/w1/RevClaimsFrozen/receipts.json` (4 277 651 B), a
`sibling seat's` receipt of `git show` / `git ls-tree` stdout. No `.bin`, `.image`, `.sqfs`, `.tar`,
`.zip` or archive of any kind exists under the wave tree.

The one carve-out worth naming: the wave tree's `hsqs` hits are the **strings** `hsqs` in the
counter/triage instrument sources and checklists (the SquashFS magic the instruments *test* for),
not SquashFS images.

### 2f. Fetcher containment (read-only source inspection)

`tools/round-50/fetch-vendor.py` (and the round-52 draft
`.ufo/waves/round-52/w1/ExecFetchVendor/fetch-vendor.py`) refuse to write vendor bytes into the
lane: the `--cache` / `--image-cache` arguments are rejected when
`(realpath(path) + os.sep).startswith(lane)`, where `lane` is the repository root
(`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/`). Verified: the guard resolves to the lane root
from both the round-50 and the round-52 file locations. The network guard is `ALLOWED_HOST =
'download.avm.de'`, enforced twice (initial request and redirect), and the fetcher writes **no
HTTP response headers** into any receipt — `rec` records only `id`, `pin`, `url`, `fetch`,
`image_sha256`, `member_sha256`, `member_detail`, `ok`, `link`, `detail`. `urllib`'s default
opener installs **no** `HTTPCookieProcessor` (verified by inspecting the handler list: no cookie
handler is present), so a `Set-Cookie` from the vendor cannot even be stored, let alone pasted into
a receipt.

The round-52 carrier cache path named in the claims
(`/fast/scratch/hyaku/kaidoku-r52/carrier-cache/`) does not exist yet, and the round-50 cache
(`/fast/scratch/hyaku/kaidoku-r50/carrier-cache/`) is gone (`ls` exit 2) — the round-50 carrier
bytes are genuinely not on this host.

---

## 3. Carried L0 — unredacted session cookies in pushed history (not new)

The open L0 named at `plans/round-52-claims.md:259` ("unredacted session cookies in pushed
history — `kaidoku | round-50` stands; not re-appended; no credential use this round") is
**still live**, and this seat re-measured it rather than restating it.

**The tips are clean.** At `origin/main` (`1842addc`) and at the working tree, all three
cookie-bearing headers carry the L1's redaction placeholders:

```
git show origin/main:.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr | grep -i set-cookie
→ 15:set-cookie: _gh_sess=[redacted by L1: session cookie value]; …
→ 16:set-cookie: _octo=[redacted by L1: session cookie value]; …
→ 17:set-cookie: logged_in=[redacted by L1: session cookie value]; …
```

**The blobs are not.** Scanning every blob in the object database for
`set-cookie: <name>=<value>` with a value ≥8 chars and excluding redaction markers yields
**7 raw hits across 4 blobs**, of which 3 are real cookie values:

| Blob | Path | Class | Value length | Introduced by (ancestor of `origin/main`) |
|---|---|---|---|---|
| `5f8478b4fc25c8b1c5718eeafba2591f62010a1f` | `.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr` | `_gh_sess` | 348 | `14936cb9` (round-49 wave-1) |
| `815e2951e830e2ffea5c0995444c19a47225879b` | `.ufo/waves/round-49/w1/C1S138Reopen/receipts/top.hdr` | `_gh_sess` | 364 | `14936cb9` (round-49 wave-1) |
| `ba6b0d6ec4d791ced391a08523bfd2e66ddbb2b6` | `.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr` | `_gh_sess` | 352 | `ef3edf4b` (round-45 wave-2) |
| `4bd24766f8d2b95a653971992bca20f0f25c38ba` | `.ufo/waves/round-49/w2/W2Jj.md` | — | 56 | **false positive**: the prose "Only `set-cookie` headers, see F3" — the regex captured a following prose run |

All three real blobs are **reachable from `origin/main`** (`git rev-list origin/main --objects`
lists each), i.e. they are in pushed history. The raw values are directly retrievable:

```
git show 14936cb9:.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr | grep set-cookie
→ set-cookie: _gh_sess=<348-char value>   (and _octo, logged_in=no)
git show 11ccdb72^:.ufo/waves/round-45/w2/R45W2S138Top/receipts/f1.hdr | grep set-cookie
→ set-cookie: _gh_sess=<352-char value>   (and _octo, logged_in=no)
```

Severity is **low** and unchanged: `logged_in=no` on every one, i.e. these are **anonymous**
server-issued GitHub session cookies, not user credentials (the round-49 wave-2 sentinel reached
the same judgement: *"These are server-issued anonymous session cookies, not user credentials"*).

**Round-52 adds no new exposure.** The raw-cookie blob set is the **same three blobs** the
round-51 seat measured; no commit in round-51 or round-52 introduces a new one; the round-52 wave
tree contains **no** copy of any of the three (checked by sha1 of every wave-tree file against the
three blob ids — no match); and the claims file itself already records the L0 as open and carried.
The remedy is an operator-side history rewrite (force-push), which the lane's rules forbid a seat
to perform and which the claims explicitly do not re-append. **No remediation is proposed by this
seat; this is a measurement, not a defect introduced this round.**

---

## 4. Command receipt

Every command below ran read-only against the lane or the git object database. UTC timestamps,
exit codes and stdout sha256 are in `scan-commands.tsv` (same directory). `sha256` values are of
**stdout**; the stderr hash is recorded on the `*.stderr` row of each pair.

| # | Command (cwd = lane) | Exit | stdout sha256 (prefix) | Result |
|---|---|---|---|---|
| A1 | `grep -n -iE 'set-cookie\|cookie:\|session[_-]?id\|bearer\|authorization:\|api[_-]?key\|private key\|op://\|ghp_\|github_pat_\|AKIA[0-9A-Z]{16}\|xox[baprs]-' plans/round-52-claims.md` | 1 | `e3b0c442…b855` (empty) | 0 matches — claims file clean |
| A2 | same grep over `.ufo/waves/round-52/` | 0 | `1eb1a19f…ffc2` | 32 hits, all prose/task-strings (§1c) |
| A3 | `grep -rn -E 'https?://[^/[:space:]@]+:[^/[:space:]@]+@' plans/round-52-claims.md .ufo/waves/round-52/ tools/round-50/carriers.json` | 1 | `e3b0c442…b855` (empty) | 0 credential-bearing URLs |
| A4 | `grep -rn -E 'BEGIN (RSA \|EC \|OPENSSH \|PGP \|DSA )?PRIVATE KEY' plans/round-52-claims.md .ufo/waves/round-52/` | 1 | `e3b0c442…b855` (empty) | 0 private-key blocks |
| A5 | `grep -rn 'op://' plans/round-52-claims.md .ufo/waves/round-52/` | 0 | `e83c9add…a2f1` | 8 hits, all the literal pattern in task strings / a sibling's argv |
| A6 | `git ls-tree -r -l ab0eafedc… -- corpus/evidence/round-50/c1/ \| awk '$4>1048576'` | 0 | `386b06d2…f4ae` | 4 files, all `after.json` receipts |
| A7 | `file -b corpus/evidence/round-50/c1/*/after.json corpus/evidence/round-50/c1/*/run.json` | 0 | `44009212…e4fe` | 8 × `JSON text data` |
| A8 | `git ls-tree -r -l ab0eafedc… \| awk '$4>1048576 {print $4"\t"$5}' \| sort -rn` | 0 | `94ebd500…eb0` | 57 files, none a vendor image |
| A9 | git object DB vs the 12 pinned vendor digests (python, `git cat-file --batch-all-objects`) | 0 | `cc937f81…7463c` | `blobs_hashed 38560 hits 0` |
| A10 | lane working tree vs the same 12 digests (python `hashlib` walk) | 0 | `7b978271…f07c0` | `files_hashed 48313 hits 0` |
| A11 | raw `set-cookie` values across all blobs (python, value ≥8 chars, redaction excluded) | 0 | `914f91b5…221b` | 7 raw hits / 4 blobs (3 real cookies + 1 prose FP) |
| A12 | `git show origin/main:.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr \| grep -c redacted` | 0 | `1121cfcc…302a2` | 3 → the tip is redacted |
| A13 | `grep -n 'is inside the lane' tools/round-50/fetch-vendor.py .ufo/waves/round-52/w1/ExecFetchVendor/fetch-vendor.py` | 0 | `96731970…5135` | the lane-write guard present in both |
| A14 | `ls /fast/scratch/hyaku/kaidoku-r50/carrier-cache/` | 2 | `e3b0c442…b855` (empty) | the round-50 carrier cache is gone |

Plus the calibrated lane scanner (§1a, exit 1, stdout sha256 `8a2c2315…906d1`) and the stdlib
sweeps (§1b).

### 4a. Self-scan of this seat's delivered artifacts

```
python3 .ufo/waves/round-50/w3/SentReceipts/credscan.py .ufo/waves/round-52/w1/SentCreds/ .ufo/waves/round-52/w1/SentCreds.md
```

The **first** run of this self-scan returned `live_hits 6` — this seat's own output was not clean,
and the fix is part of the receipt:

| Hit | Cause | Fix |
|---|---|---|
| `vendor-and-cookie-details.txt` ×4 (`set_cookie`, live) | The "proof: raw value retrievable from pushed history" block in that file **reproduced the leading characters of two real `_gh_sess`/`_octo` values** (14-char prefixes, printed by `git show … \| grep`). | The values were replaced by length-only classifications (`<REDACTED-BY-SENTCREDS: 348-char value>`); the proof now states *that* the values are retrievable without reproducing any of them. |
| `scan.md` ×1 (`op_ref`, live) | The §1c false-positive table quoted the two scanner-fixture pattern strings (a vault-ref scheme reference and a PEM private-key header) verbatim, in order to classify them. | Rewritten to describe the two fixtures by class without reproducing either literal. |

Re-run after the fix: **`live_hits 0`**, `placeholder_hits 6` (the six `set-cookie` rows whose
value is now an explicit redaction marker — correctly classed as placeholders, not values),
`files_scanned 8`, `bytes_scanned 39 849`, exit **0**. The same discipline the round-51 seat
applied: this seat's own output is held to the same bar as the surface it scanned.

## 5. Findings for the L1

| ID | Severity | Finding | Smallest remediation |
|---|---|---|---|
| **F-1** | **Info / PASS** | The round-52 surface (claims + wave tree) carries **no credential value** and **no vendor byte**. Both content-hash scans (working tree, whole object DB) return 0 hits against the 12 pinned digests. | None required. |
| **F-2** | **Info** | The largest files under `corpus/evidence/round-50/c1/` are the four `after.json` REA receipts (1.86–2.18 MB), JSON text, metadata-only — no image, no embedded content bytes. | None required. |
| **F-3** | **Low (carried, unchanged)** | The open L0 remains live: three raw anonymous GitHub `_gh_sess` values (348/364/352 chars) sit in pushed history, retrievable via `git show <old-commit>:<path>`. `logged_in=no` (anonymous, not user credentials). Round-52 adds **no** new exposure. | Operator-side history rewrite only — explicitly **not** in any seat's scope and **not** re-appended by the round-52 claims. Recorded, unchanged. |
| **F-4** | **Low (scanner defect, pre-existing, not round-52)** | The lane's calibrated scanner `.ufo/waves/round-50/w3/SentReceipts/credscan.py` reported `live_hits 5` on the round-52 surface at scan time. All five were false positives caused by its `bearer` pattern `(?i)\bbearer\s+([A-Za-z0-9._~+/-]{12,})` — `\s` matches a newline, so a TSV row ending in the *word* `bearer` is joined to the next row's path and read as a token. The surface as it now stands re-scans to `live_hits 0` because the sibling seat reordered that file's columns; **the defect remains latent** and will fire again on any file that ends a line with the word `bearer`. | Change `\s+` to `[ \t]+` in the `bearer` pattern (and audit the other classes for the same `\s+` shape), then re-run. Out of this seat's remediation scope — reported to the L1 for routing. |
| **F-5** | **Info** | The round-52 fetcher draft's network-guard selftests have **not** been run and the draft is self-declared a "reduced reconstruction" (`.ufo/waves/round-52/w1/ExecFetchVendor/deltas.md`). The **vendor-byte** containment it does carry is intact: the lane-write guard (`refusing: %s is inside the lane`) resolves correctly from `tools/round-52/`, the `ALLOWED_HOST` pin is enforced twice, and the fetcher records **no HTTP headers** in any receipt. | None for the credential/bytes surface; the selftest gap is `ExecFetchVendor`'s own open item and must not be closed by the L1 without the mutation evidence. |

## 6. Limits of this scan

- Pattern-class coverage only; there is **no entropy detector**, so a credential whose name is not
  in the class list would not be caught. Every hit in this round was nonetheless adjudicated by
  hand (file:line → what it actually is), so nothing is dismissed by pattern alone.
- The vendor-byte test is **exact-hash against 12 known digests** plus a `hsqs` magic sweep plus a
  size filter. A vendor image that was re-encoded, truncated or byte-modified after download would
  not be detected by the hash arm; the magic arm would catch it only if the SquashFS superblock
  survives.
- The git object scan covers the lane's own object database; it does not cover the **remote's**
  object store beyond what `origin/main`'s reachable set already contains (which was checked
  explicitly for the cookie blobs and the vendor digests).
- No REA run, no network fetch, no vendor download was performed by this seat (forbidden this
  wave). The carrier-URL check is a static read of `tools/round-50/carriers.json`.
