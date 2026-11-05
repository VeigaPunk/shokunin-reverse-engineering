# ScoutSources — independent re-open of registry rows S322 / S323

Seat: ScoutSources (scout). Round 97, attempt 1, lane kaidoku. L = `867ed98d85f45a18265441c1760386ef353b3d43`,
B = `2a54af0785f75d50912e1136443c8e78e62adf27`. Scratch `/fast/scratch/hyaku/kaidoku-r97/ScoutSources` (clone at `$S/clone`, `--detach` L, read-only git only; removed on exit). No REA call was made. No tool was installed or upgraded (curl, python3, gawk, coreutils already present).

## Commands run (exact line, exit code, verdict)

Method: `curl` into `$S`; sha256 of the fetched bytes; strip tags (inline `<b>`/`<i>`/`<a>` removed
entirely, not replaced by a space), unescape entities, collapse whitespace; then test each quote. Section membership read from the man7 `<h2><a id="SECTION">` headings — "inside DESCRIPTION" is a section test, not a whole-page test.

| # | command | exit | verdict |
|---|---|---|---|
| 1 | `curl -sS -o $S/s322-fsync2-fetch.html -w 'S322 http=%{http_code} size=%{size_download}' https://man7.org/linux/man-pages/man2/fsync.2.html` | 0 | `S322 http=200 size=15152` |
| 2 | `curl -sS -o $S/s323-rename2-fetch.html -w 'S323 http=%{http_code} size=%{size_download}' https://man7.org/linux/man-pages/man2/rename.2.html` | 0 | `S323 http=200 size=23571` |
| 3 | `sha256sum $S/s322-fsync2-fetch.html $S/s323-rename2-fetch.html` | 0 | `f0a986d2…5d91f5` / `8772946a…e6e57` |
| 4 | `sha256sum <lane>/.ufo/waves/round-97/pre/s322-fsync2-fetch.html <lane>/.ufo/waves/round-97/pre/s323-rename2-fetch.html` | 0 | same two digests — **no difference** |
| 5 | `cmp $S/s322-fsync2-fetch.html <lane>/.ufo/waves/round-97/pre/s322-fsync2-fetch.html` | 0 | byte-identical |
| 6 | `cmp $S/s323-rename2-fetch.html <lane>/.ufo/waves/round-97/pre/s323-rename2-fetch.html` | 0 | byte-identical |
| 7 | quote/section test (script `check2.py`, sections from `<h2><a id=...>`) | 0 | see table below |
| 8 | `cd /home/vgpnk/Projects/shokunin && bash scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` | **0** | last line `kaidoku ok /home/.../kaidoku-shokunin/corpus/SOURCES.md`; 32 W04 warnings, **no E-code, no S322/S323 finding** |
| 9 | `git -C <lane> show 867ed98d…:corpus/SOURCES.md \| grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}'` | 0 | **228** |
| 10 | `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' <lane>/corpus/SOURCES.md` | 0 | **228** (worktree == L) |
| 11 | same count at base `git show 2a54af0…:corpus/SOURCES.md` | 0 | **226** → L adds exactly 2 rows (S322, S323) |
| 12 | `sha256sum -c <lane>/.ufo/waves/round-97/pins.sha256` | 0 | all pinned files OK; **but see F2** |
| 13 | `python3 tools/round-41/local-source-gate.py --root . --rev 867ed98d…` | 0 | `verdict FAIL (rows: S082, S302, S321)` — same set at base → **pre-existing debt** |

## Quote verification (the seat's core question)

| row | quote | verbatim after tag-strip + whitespace collapse | inside DESCRIPTION? |
|---|---|---|---|
| S322 | "Calling fsync() does not necessarily ensure that the entry in the directory containing the file has also reached disk." | **yes** | **yes** — `sections_containing_quote: ['DESCRIPTION']`, no other section contains it |
| S323 | "If newpath already exists, it will be atomically replaced" | **yes** | **yes** — `sections_containing_quote: ['DESCRIPTION']`, no other section contains it |

Discrimination control (the check is not vacuous): a paraphrase of the S322 quote, a wrong-word variant of the S323 quote, and the S323 quote tested against the fsync page all correctly returned **absent**; only the two exact quotes were present. Both pages carry the footer `Linux man-pages 6.19`. Neither quote is character-exact in the raw HTML (`Calling <b>fsync</b>() …`), so a raw-substring test would false-negative; the strip-tags reading is the one the rows' anchor cells describe.

## S323 row shape (the seat's second question)

`teaches` cell = `REJECTED: the page documents atomic replacement against a concurrent reader, not crash
durability of the rename; the durability clause for the directory entry comes from S322, not from this page; flip: a claim that needs rename atomicity against a concurrent reader, or a page that states a crash-durability guarantee for rename`

- starts with `REJECTED:` — **yes**; contains a `flip:` clause — **yes** (`flip: a claim that needs rename
  atomicity against a concurrent reader, or a page that states a crash-durability guarantee for rename`)
- `status` = `rejected`, `used-by` = `—`, `opened` = `2026-11-05`, `recheck` = `on-release`, `kind` = `docs`, `tier` = `A`; 13 fields, well-formed; census raises no E01/E07/E09/W02/W03 on it.
- The rejection reason is **substantiated by the page**: rename(2)'s DESCRIPTION contains no crash-durability statement at all. The only "crash" text on the page is in `BUGS` and concerns an NFS *server* failing mid-rename ("If the server does the rename operation and then crashes …"), which is not local crash durability of the rename. The row's anchor is scoped to DESCRIPTION, and the quoted sentence there is about a concurrent reader, exactly as the row says.
- Registry context: 25 rejected rows; 18 begin with `REJECTED:`, 13 carry a `flip:` clause (S323 is among both). S322 is `mined`, `teaches` = "a receipt writer must fsync the containing directory after `os.replace`, not only the file before it", `used-by` = `corpus/knowledge/2026-11-05-r97-receipt-byte-binding.md` (file exists; census E11 passes).

## Findings (4)

**F1 — medium — the round-97 knowledge entry misquotes the page it attributes the quote to.**
`corpus/knowledge/2026-11-05-r97-receipt-byte-binding.md:24-26` presents, inside one double-quoted string, "Calling fsync() does not necessarily ensure that the entry in the directory containing the file has also reached disk. **For that, fsync() on a file descriptor for the directory is also needed.**", and annotates it "(S322; located in the fetched copy.)". The page reads "For that **an explicit** fsync() on a file descriptor for the directory is also needed." — the word *an explicit* is dropped and `For that an` is rewritten as `For that,`. The quoted span is therefore not verbatim in `.ufo/waves/round-97/pre/s322-fsync2-fetch.html` (verified: the span with the page's exact wording is present, the span as written in the entry is not). The **S322 registry row's own located quote is verbatim** — it quotes only the first sentence — so the drift is in the knowledge entry, not in the row. Prior lane entries quoting man7 pages are verbatim (checked r73's proc_pid_cmdline quote and r95's O_NOFOLLOW/ELOOP quote against their pages), so this is new drift, not house style.

**F2 — medium — the S323 fetch copy landed without a pin line.**
`.ufo/waves/round-97/pre/s323-rename2-fetch.html` was added at L (`git log`: it appears in the landing commit only; the S322 copy arrived earlier, at the freeze commit `e859a88d…`), and `.ufo/waves/round-97/pins.sha256` is **byte-identical between the freeze and the landing** (`git diff e859a88d… 867ed98d… -- .ufo/waves/round-97/pins.sha256` is empty). Of the 17 files committed under `.ufo/waves/round-97/pre/` at L, 16 are pinned and **the S323 copy is the single unpinned one** — its sibling `s322-fsync2-fetch.html` is pinned at line 44 of the same manifest. The row's own text carries the digest (`sha256 8772946a…`), so the copy is bound by the row, but it is outside the round's pin manifest and outside every `sha256sum -c` the manifest expresses — the "pins name the bytes" doctrine the round lands in QUALITY 195, applied to the round's own evidence.

**F3 — low — no round-97 census before/after receipts are committed.**
The frozen claims file (unchanged F→L) states: "Census before/after via `scripts/sources-census.sh validate
--root /home/vgpnk/Projects/shokunin kaidoku` (exit 0 required at round end; start run recorded with W04
warnings unchanged)". I measured the exit-0 condition and the "W04 unchanged" condition (below), but no `census-before.txt` / `census-after.txt` exists anywhere under `.ufo/waves/round-97/`, while rounds 90–96 each committed a before/after pair.

**F4 — low — S323 landed outside the frozen claims' declared sources.**
`plans/round-97-claims.md` (frozen at F, verified unchanged at L) names S322 and only S322 in its "Sources and frontier" section ("S322 (`fsync(2)` … grounds the durability clause of C1's knowledge entry and block 36; the fetch bytes are `pre/s322-fsync2-fetch.html`"). `grep -c S323` on the claims file = **0**. The S323 row, its fetch copy, and the `corpus/README.md` line that names "S323 (rename(2), rejected)" are landing-side additions with no claim-side declaration. The registry row and its rejection reason are sound (verified above), so this is a traceability gap, not a row defect.

## Confirmed clean (no finding)

- **Both quotes verbatim, both inside DESCRIPTION**; no other section contains either. **Fetch sha256 == the
  lane's copies for both pages** (`f0a986d2…`, `8772946a…`), byte-identical to my fresh fetches — the pages did not change between the lane's fetch and this re-fetch; no difference.
- **`sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` exits 0**, last line
  `kaidoku ok …/kaidoku-shokunin/corpus/SOURCES.md`; 32 W04 warnings, zero E-codes.
- **W04 set unchanged across the round**: base-rev (226 rows) and landing-rev (228 rows) measurements differ
  only by the two new rows; the W04 finding lists are identical (`diff` of the two sets is empty), and my base-rev output is byte-identical to the lane's committed `.ufo/waves/round-96/census-after.txt` after normalising the lane label and file path — the claims' "W04 warnings unchanged" clause holds.
- **Row count**: 226 at base → 228 at L; worktree matches L at 228. The census's own counter reports
  `rows 228` (tier A 208 / B 11 / C 9; mined 203 / rejected 25) at L and `rows 226` at base.
- No E-code on S322/S323: each man7 URL appears once in the registry, so no E04/W04 arises.
- `sha256sum -c .ufo/waves/round-97/pins.sha256` → every pinned path present and matching (rc 0).
- `local-source-gate.py` FAIL set (S082, S302, S321) identical at base and at L → pre-existing debt.

## Not established / limits

- Verified the two rows' *text* against the served pages, not that the lane's original fetch was made on
  2026-11-05 by the lane — only that the bytes it kept are the bytes the server serves today.
- No REA call was made; no reverse-engineering capability was exercised.
- These are the seat's own measurements; they do not re-score or re-freeze R97-C1 or R97-C2. No file under
  `tools/round-97/`, `.ufo/waves/round-97/` (frozen), `corpus/`, `SKILL.md`, `plans/`, `LOG.md` or `SCORECARD.md` was edited by this seat.

Verdict: both rows re-open clean as to quote text, section placement, digests and census shape (4 findings,
none falsifying a row's stated value; F1 misquotes the fsync page in the knowledge entry, F2 leaves the S323 copy unpinned).
