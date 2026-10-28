# W2Sentinel — round 49 wave 2: sensitive-content and write-scope sweep

Lane `main`, landing revision `29883d4ec35a31a8393c4ffb220888c44c0bb022`, base `e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9`.
Run 2026-10-28T22:49Z. All reads were git objects at the landing revision (`git show`, `git cat-file`, `git diff`), never the worktree. No counter was run (not in this seat's attack). No tool was installed. No mutating git. Nothing under the lane tree was written.

## Verdict

**NOT CLEAN on sensitive content; write-scope CLEAN.**

- One credential-class finding (F1): GitHub session cookies (`_gh_sess`, `_octo`, `logged_in`) are committed unredacted in two wave-1 receipts. `logged_in=no`, so the session is unauthenticated, but it is session-token material and the rule forbids it in the record. The lane's own `C1S139Reopen.md:36` says set-cookie headers were dropped from its receipts; the two receipts that carry them were not redacted.
- Everything else scanned is clean of credential material: no tokens, keys, `op://` refs, `Authorization`, bearer strings, session-keyed assignments, env dumps, symlinks or gitlinks, in all 2231 added or modified paths, the three HTML snapshots, and the REA receipts.
- One file is over 1 MiB (F2, no secret inside). One compressed receipt expands 36x (F3, no secret inside).
- Operator and fleet-private paths and public upstream identifiers are present (F4–F8). Under the contract "home paths are acceptable" these are info or low; F4 is the one a reviewer should remove.
- The contract's "CORPUS.md rule 6" does not resolve anywhere in the lane (F13).

## Scope and method

- Diff scope: `git diff --name-only E R` = 2231 paths (2176 A 100644, 49 A 100755, 6 M 100644; `git diff --numstat` 512683 insertions, 2 deletions).
- Blob scan: every added or modified blob at R (2231 blobs, 0 unreadable, `.gz` decompressed before scanning) through 21 credential and privacy classes (`scan.py`, sha256 below). Plus a scan of the added diff lines only (512593 lines), so pre-existing text is not attributed to the round.
- Calibration: `selftest.py` gives 11 of 12 synthetic positives on the first pass; the JWT fixture was malformed. Re-tested with a well-formed JWT (`jwt-selftest`: positive True, clean-text negative False). A clean synthetic negative produced 0 hits. Limits: regex keyword and prefix classes only, no entropy detector; a credential with an unlisted name would not be caught (F1 was found by the `set-cookie:` pattern, not a generic key rule).

## Findings table

Each row: file:line, class, command and exit code, sha256, verdict. Command notation: `S`=scratch `/fast/scratch/hyaku/kaidoku-r49/W2Sentinel`, `L`=lane, `E`=base, `R`=landing revision. All git calls use `GIT_NO_REPLACE_OBJECTS=1`.

| # | Severity | Location (file:line) | Class | Command → exit | Evidence (sha256 / size / count) | Verdict |
|---|---|---|---|---|---|---|
| F1 | **Must fix** (credential class; impact low, `logged_in=no`) | `.ufo/waves/round-49/w1/C1CarrierPins/receipts/tree.hdr:15,16,17`; `.ufo/waves/round-49/w1/C1S138Reopen/receipts/top.hdr:15,16,17` | session cookie (`_gh_sess`, 348 and 364 chars), `_octo` (27 chars), `logged_in=no` | `git show R:<path> \| grep -nE set-cookie` → exit 0, matches at 15–17 in each file (values redacted in `cookie-receipts-redacted-*.hdr.txt`); scanner `cookie-header` class → 6 hits in 2 files, all F1 | blob `5f8478b4fc25c8b1c5718eeafba2591f62010a1f` (tree.hdr) sha256 `bee3ed2a38e68e970e3d4b97851ed5f94ae1b7c86ce217aba48e02ed484b956d`; blob `815e2951e830e2ffea5c0995444c19a47225879b` (top.hdr) sha256 `7a63a11df61469932adf4639c4328c2f987905429d33dc3ac42713c41e7f0ad9` | **FAIL.** Session-id material committed; the lane's redaction claim (`C1S139Reopen.md:36`, "set-cookie dropped") is true only for S139 receipts. No landed doc cites either receipt's sha256 (`git grep` for `bee3ed2a`, `7a63a11d`, `tree.hdr`, `top.hdr` over `corpus PROVINCE.md LOG.md SCORECARD.md tools/round-49 plans` → no match), so the fix touches only non-frozen wave-1 receipts. |
| F2 | Low (size) | `.ufo/waves/round-49/w1/C2CounterMut/results-raw.json` | file over 1 MiB | `git cat-file -s R:<path>` → 1720798; size pass over 2231 blobs → 1 file over 1,048,576 | sha256 `cf571bba26dc04e0ed86c58f2d894b54937e07e431667e0e05245a3dc411dd67`; scanner → 0 credential hits | Over the threshold; no secret. L1 decision (keep, or compress/trim if the 1 MiB rule applies). |
| F3 | Low (size, expansion) | `.ufo/waves/round-49/w1/C1RunReview/logs/strace-f-dev-run.txt.gz` | compressed log, 36x expansion | `git cat-file -s` → 697043 (blob `ec27715cf1b174176d2380bd9ed3a952757f3238`, sha256 `5ec57e107dbeb810106d79c55a7dcee08e99b38e0a364e89d7e62501e556664a`); `gzip -dc` → 25376186 bytes, 421812 lines (`strace.txt` sha256 `971c768f10202ddc3a33a4f60e010ee6f161e7e2ec9e1c1365fd66a384ddd759`) | Content clean. No `NAME=` env tokens (0), no `execve(` lines (0), no `_authToken`/`password`/`ghp_`/`npm_` fragments (0). `.npmrc` opened 4x → ENOENT. `.config/git/config` opened 10x, no `[user]`/`email` payload reads. 104 hits are `user@1000.service` (systemd unit, benign). Size only. |
| F4 | Low (operator-private sibling repo path, landed text) | `corpus/lessons/round-49.md:28` | `/home/vgpnk/Projects/shokuknow/merge/kaidoku/` | `git show R:corpus/lessons/round-49.md \| grep -n shokuknow` → 0 (line 28) | Only landed-text instance of a sibling fleet repo path in this round's additions. Other copies sit in the frozen `tools/round-49/control-fixtures/pos/**` and `.ufo/waves/round-49/**` | Remove or make repo-relative (non-frozen text). Low. |
| F5 | Info (operator tool path, frozen control copy) | `tools/round-49/control-fixtures/pos/PROVINCE.md:509567` (diff line; a copy of the landed PROVINCE text) | `/home/vgpnk/.config/devin/mcp_config.json:7` | `git show R:tools/round-49/control-fixtures/pos/PROVINCE.md \| grep -n .config/devin` → 1 | Landed `PROVINCE.md` at R: 0 hits for `.config` (checked). Only the frozen fixture copy carries it | Acceptable per contract (path, not secret). Frozen; report only. |
| F6 | Info (public upstream identifiers, landed snapshot) | `corpus/evidence/round-49/c2/sysexits.html:263` (`sc_project=7422636`), `:265` (`sc_security="9b6714ff"`), `:268` (`statcounter.com/counter/counter.js`), `:273` (`c.statcounter.com/7422636/0/9b6714ff/1/`), `:285` (`_gaq.push(['_setAccount','UA-9830363-8'])`), `:209` (`man-pages@man7.org`) | third-party analytics tags and an upstream contact, inside a page snapshot | `git show R:<path> \| grep -nE 'sc_security\|sc_project\|UA-\|statcounter'` → exit 0, matches at 263–285 | sha256 `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340` (sysexits.html, 12725 B) | Public identifiers of the upstream site (man7.org), not operator credentials. Policy call: a snapshot that keeps third-party tracker scripts is not secret-bearing; strip if the corpus wants only content. |
| F7 | Info (synthetic and upstream addresses) | `tools/round-49/c1-controls.py:218,1319` `controls@r49.invalid`; `corpus/SOURCES.md:88` `xyproto@archlinux.org` (pre-existing line, outside the round's hunks, which start at 144); `corpus/evidence/round-49/c2/sysexits.html:209` `man-pages@man7.org`; wave-1 `C1S139Reopen/tagobj.body:1`, `C1ScribeSources/receipts/s139-tag-object.json:7` (squashfs-tools maintainer, tag tagger) | e-mail addresses | `git show R:<p> \| grep -noE '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[a-z]{2,}'` | ~155 scanner hits in 47 files; landed-path distinct: 4 | Synthetic `.invalid` addresses, or public upstream metadata. No private personal address in landed text. |
| F8 | Info (scanner false positives and public IPs) | `.ufo/waves/round-49/w1/C1S139Reopen/page.body:292,3828`; `…/tagpage.body:305,783`; `C1ScribeSources/receipts/squashfs-tools-releases-page.html:305,783`; `…/unblob-squashfs-tree.html:342,525` (`10.669.606.225`) | private-IP regex | scanner `ipv4-private` → 8 hits in 4 files | — | False positives: `669` is not a valid octet. No RFC1918 address in the added set. Public CDN addresses `104.16.x.34` appear in wave receipts (benign). |
| F9 | Info (UUIDs) | `.ufo/waves/round-49/w1/` (248 UUIDs in 5 files: `C1S139Reopen/page.body` 193, `C1S139Reopen/tagpage.body` 24, `C1ScribeSources/receipts/squashfs-tools-releases-page.html` 24, `unblob-squashfs-tree.html` 5, `C1RunReview/strace-outside-writes.txt` 2) | UUID-shaped tokens | added-lines scan, 4 sampled contexts | — | Sampled: npm cache temp names (`~/.npm/_cacache/tmp/<uuid>`) and upstream page content. Not session credentials. Not exhaustively classified. |
| F10 | Info (write-scope, positive) | `git diff --numstat E R -- LOG.md PROVINCE.md SCORECARD.md corpus/QUALITY.md corpus/README.md corpus/SOURCES.md` | modified existing files | `diff` exit 0 | LOG.md +6/−0; PROVINCE.md +8/−0; SCORECARD.md +6/−0; corpus/QUALITY.md +1/−0; corpus/README.md +3/−0; corpus/SOURCES.md +8/−2 (hunk `@@ -144,2 +144,2 @@` replaces rows S138/S139 — the planned `used-by` update) | Clean. All 2231 paths fall under the allowed set (`.ufo/waves/round-49/`, `corpus/evidence/round-49/`, `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md`, `corpus/lessons/round-49.md`, `plans/round-49-claims.md`, `tools/round-49/`, the six modified files). 0 added files outside it. `.ufo/state*`, `.ufo/watchdog.log`, `.scratch/`: 0 paths. |
| F11 | Info (modes, links) | `git diff --raw -z --no-renames E R` | symlinks (mode 120000), gitlinks (160000), exec bits | `diff --raw` exit 0 | 0 symlinks, 0 gitlinks; 49 new 100755 files: 6 in `tools/round-49/` (`c1-controls.py`, `c1-counter.py`, `c1-oracle.py`, `c1-run.py`, `c1-run.sh`, `c2-mismatch.py`), 43 under `.ufo/waves/round-49/` | Clean. Exec bits are scripts, expected. |
| F12 | Info (REA receipts, clean) | `corpus/evidence/round-49/c1/{v1be,v1le,v2be,v2le}/{run,extract-env,provenance,envelope,after}.json`, `manifest.json` | env dumps, `PATH`, home paths | JSON key walk over each file (keys matching env/token/secret/key/cookie/auth/session/password/home/user) → only `unblob_command_env` (a path string), `environment: null`, `authority`, `extract_env` (a filename) | `extract-env.json` keys: `carrier, log_tee, notes, npx, path, sasquatch, sasquatch-v4be, schema, seat, unblob, unblob_log`. `path` is an allowlisted PATH (`/usr/local/bin:…/home/vgpnk/.local/bin:…`). `run.json` `command`/`argv` contain the lane path and `/fast/scratch/hyaku/…` | Clean. Home paths acceptable per contract. No secret in any REA receipt. |
| F13 | Process (reference does not resolve) | contract "CORPUS.md rule 6" | rule citation | `git ls-tree -r --name-only R \| grep -i corpus.md` → none in `corpus/` or top level; `git log --all --oneline -- CORPUS.md` → empty; `git grep -n 'rule 6' R -- '*.md'` → no CORPUS rule | — | The cited file does not exist in the lane. The fleet root was not consulted (out of bounds for this seat). I applied the contract's stated test (credential, private path, symlink, >1 MiB, secrets in snapshots and receipts) directly. L1 should cite the real rule or drop the reference. |

## Snapshot and receipt checks (contract items)

- HTML snapshots (`popper.html` 118135 B sha256 `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207`; `sysexits.html` 12725 B sha256 `d9db4b96fded98e35ec7d9e98f4c229ac57b8083593b57e2381c047aee20b340`; `freebsd-sysexits.html` 59251 B sha256 `1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf`): grep for `csrf|nonce|integrity|token|session|cookie|authorization|bearer|api_key|secret|password|jwt|signature|x-amz|cf_clearance` → only public words; hidden inputs are `sitesearch`, `DB`, `ka`, `kt` (search UI, benign). Only F6 identifiers. Clean.
- REA receipts: F12. Clean.
- Symlinks and gitlinks: F11. None.
- Files over 1 MiB: F2 (1 file). F3 is 25 MB expanded, 697 KB stored.
- Secret-class classes over all 2231 blobs (`scan-summary.json`, `hit-counts.txt`): private-key-block 0, aws-access-key 0, github-token 0, npm-token 0, npmrc-authtoken 0, anthropic/openai key 0, slack 0, google api key 0, jwt 0, 1password `op://` 0, authorization-header 0, bearer-literal 0, cookie-header 6 (F1 only), session-id-assign 0, generic-secret-assign 0, env-token-var 0. Distinct classes with hits: email 155, operator-home-path 29002, ipv4-private 8 (false positive), hex-40/64 30103 (sha256s, benign).

## Commands and exit codes (full list in `W2Sentinel/commands.txt`)

| command | exit |
|---|---|
| `git -C $L diff --name-only $E $R` | 0 (2231 paths) |
| `git -C $L diff --raw -z --no-renames $E $R` | 0 |
| `git -C $L diff --numstat -z $E $R` | 0 |
| `git -C $L diff --no-color --no-ext-diff -U0 --no-renames $E $R > added.diff` | 0 (28880208 B, sha256 `f0dbbae17811faddc110e8df1ebf4c1b2e9afb7d47c86ef9b48c50a5baa0bb7f`; 512593 added lines) |
| `python3 -I -B scan.py` | 0 (2231 blobs, 0 unreadable) |
| `python3 -I -B selftest.py` | 0 (11/12 positive first pass; JWT fixture re-tested positive, negative False; clean negative 0 hits) |
| `git -C $L show $R:<path> \| sha256sum` (receipts, snapshots, results-raw, strace.gz) | 0 |
| `git -C $L log --all --oneline -- CORPUS.md` | 0, empty |
| `/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` | 0 (/fast/scratch/hyaku 42% used, 472.1G free) |

## Artifacts (`.ufo/waves/round-49/w2/W2Sentinel/`)

- `commands.txt` — exact commands and their results.
- `scan.py` (sha256 `c1f3f8535cc8ae4a1d861bde479b67327c6d77c3aa7d91e8e47d860ab9c6d8b5`) — the blob scanner.
- `selftest.py` (sha256 `109df34a63c1675ef157427b30d3cd1d52fc421a4a4d02170867817585195ea2`).
- `scan-summary.json` (sha256 `9e0eb98643cb10564125f33b57e009e866e2d2ba5ff98ee5e64d0d49c1ea449b`) and `hit-counts.txt`.
- `rows.tsv` (sha256 `7ceb2d8c101c3558e24bac98847937f16cd50dde33880b6cf3300c03622c65e2`) — mode, status, blob sha, path for all 2231 paths.
- `cookie-and-ipv4-hits.tsv` — the scanner rows for F1 and F8.
- `cookie-receipts-redacted-tree.hdr.txt` and `cookie-receipts-redacted-top.hdr.txt` — copies of the two receipts with the cookie values replaced by `<REDACTED>`.
- `sha256-artifacts-scratch.txt` — scratch hashes (scan-hits.tsv `8cca2fb528d55190f413453c96306ed219e8d10520a5d3b4098bf4069c8609cf`, added.diff, added-lines.tsv `67d81f85c84b4c3530f0c02ca5cdc8ff72ff4576c9051cf9ae64fd7f256eed3f`, strace.txt).

Not copied (size): the full scan-hits (6.3 MB), the added-line table, and the 25 MB strace text. Their sha256s are recorded above and in `sha256-artifacts-scratch.txt`.

## Recommendations for L1 (non-frozen text only; the frozen tree is untouched by this report)

1. **F1 (must):** remove or redact the three `set-cookie:` lines at `tree.hdr:15-17` and `top.hdr:15-17` (`_gh_sess`, `_octo`, `logged_in`), keeping the status if needed. Nothing landed cites those receipts' hashes. The unredacted blobs stay reachable in history; whether to rewrite history is an operator decision (this seat did no mutating git).
2. **F1 (claim):** make `C1S139Reopen.md:36` true for every receipt in the wave, or qualify it.
3. **F4:** remove the `/home/vgpnk/Projects/shokuknow/...` path at `corpus/lessons/round-49.md:28`.
4. **F2:** decide whether the 1 MiB threshold applies to `results-raw.json`.
5. **F13:** cite the real rule for "CORPUS.md rule 6", or drop it.
6. Informational only: F5–F9, F11, F12 need no action.

No counters were re-measured in this seat. The write-scope findings (F10–F11) and the receipt checks (F12) are independent of the two counters' verdicts.
