# ScoutS320 — independent non-author re-open of the S320 source and quote check

Seat: `ScoutS320` (scout). Lane: `kaidoku`, round 95, attempt 1.
Declaration commit read: `4bda1d1dd3788973f10e61212b70df18b3b14ea0` (base `b5331db1fb0ce0bf93695ce1730cf831effef6a9`).
Lane READ-ONLY for this seat: the only lane writes are inside
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ScoutS320/` plus this report file.
Scratch `/fast/scratch/hyaku/kaidoku-r95/ScoutS320` deleted before yield.

**Bottom line: the S320 source re-opens clean — no discrepancy.** Two independent fetches are HTTP 200,
76506 bytes, sha256 `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`, byte-identical to each
other and to both L1-committed fetch files; the frozen quote is exact (1 occurrence) after tag-strip + whitespace
normalisation; the page version string is `Linux man-pages 6.19` verbatim. Two caveats the L1 should carry into the
S320 row / knowledge entry (details in the seat file): the quote is **not** a raw contiguous byte substring, and the
`ERRORS` section qualifies the rule with `O_PATH`.

## The table (required)

| fetch index | HTTP status | bytes | sha256 | quote located | version string | discrepancy |
|---|---|---|---|---|---|---|
| 1 (this seat) | `200` | `76506` | `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789` | yes — 1 occurrence, normalised | `Linux man-pages 6.19` | none |
| 2 (this seat) | `200` | `76506` | `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789` | yes — 1 occurrence, normalised | `Linux man-pages 6.19` | none |
| L1 `l1/scores/s320-open2-fetch1.html` (reference) | committed file | `76506` | `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789` | yes — 1 occurrence | `Linux man-pages 6.19` | none — byte-identical to both this seat's fetches (`cmp` exit 0) |
| L1 `l1/scores/s320-open2-fetch2.html` (reference) | committed file | `76506` | `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789` | yes — 1 occurrence | `Linux man-pages 6.19` | none — byte-identical to both this seat's fetches (`cmp` exit 0) |

All four sha256 values above are the same string:
`d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`.

## Evidence (exact commands, exit codes)

```
SEAT=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/w1/ScoutS320
for i in 1 2; do
  code=$(curl -fsSL -w '%{http_code}' -o "$SEAT/s320-open2-fetch$i.html" https://man7.org/linux/man-pages/man2/open.2.html)
  rc=$?
  echo "fetch$i rc=$rc http=$code bytes=$(stat -c%s "$SEAT/s320-open2-fetch$i.html") sha256=$(sha256sum "$SEAT/s320-open2-fetch$i.html" | cut -d' ' -f1)"
done
```
→ `fetch1 rc=0 http=200 bytes=76506 sha256=d665489c…c789` ; `fetch2 rc=0 http=200 bytes=76506 sha256=d665489c…c789`

```
cmp "$SEAT/s320-open2-fetch1.html" .ufo/waves/round-95/l1/scores/s320-open2-fetch1.html   → IDENTICAL, exit 0
cmp "$SEAT/s320-open2-fetch2.html" .ufo/waves/round-95/l1/scores/s320-open2-fetch2.html   → IDENTICAL, exit 0
cmp "$SEAT/s320-open2-fetch1.html" "$SEAT/s320-open2-fetch2.html"                          → IDENTICAL, exit 0
sha256sum .ufo/waves/round-95/l1/scores/s320-open2-fetch1.html .ufo/waves/round-95/l1/scores/s320-open2-fetch2.html
```
→ both `d665489cadb85624d98fae03a8d8d06209030f32735cff8aeba949ad8491c789`, both 76506 B (the two L1 files are
committed at HEAD, `git ls-tree` confirms; `git status` clean for them).

Tag-strip + whitespace-normalise (`scan.py`, exit 0) →
`NORMALIZED_LEN 43529`, `NORMALIZED_SHA256 8d8501c9820149256a76d411c3a083f212a57304d53cdb6324ec8a21d62b1f6c`
(identical for both fetches), `QUOTE_EXACT_COUNT 1`, `VERSION_RAW 'Linux man-pages 6.19            2026-02-08'`.
Raw contiguous count of the frozen quote in the HTML: **0** (markup + line wrap).

## Findings for the L1

1. **Ordinal occurrence: 1st and only.** The whole-page count of `trailing component` is **1**, so unlike round 94's
   S319 (2 occurrences) there is no anchor ambiguity to disclaim.
2. **Enclosing section: `DESCRIPTION`** (nearest `<h2>`; the page uses `<pre>` + `<b>FLAG</b>` term labels, not
   `<dl>/<dt>/<dd>` — those tags occur 0 times on the page). **Heading context: the `O_NOFOLLOW` flag entry**
   (`<b>O_NOFOLLOW</b>` at raw offset 18584; the sentence at 18613; preceded by the `O_NOCTTY` entry).
3. **Version string verbatim: `Linux man-pages 6.19`** (footer `<span class="footline">`:
   `Linux man-pages 6.19            2026-02-08                        open(2)`; colophon: tarball
   `man-pages-6.19.tar.gz` fetched 2026-09-09).
4. **Quote length: 20 words / 112 chars** — inside the declared ≤25-word bound.
5. **Caveat to carry (observed):** the `ERRORS` section states `ELOOP path was a symbolic link, and flags
   specified O_NOFOLLOW but not O_PATH` — the `DESCRIPTION` rule is qualified by `O_PATH`; the knowledge entry
   should not state it as unconditional. The quote is also not a raw byte substring (exact only after
   tag-strip + whitespace normalisation).
6. **Registry fit (advisory):** `corpus/SOURCES.md` has no row for
   `https://man7.org/linux/man-pages/man2/open.2.html` (17 `man7.org` rows, none this URL); max existing id is
   `S319`, `grep -c -E '^\| S320 \|' corpus/SOURCES.md` → 0, so the `S320` id is free.

## Milestone addendum — R95-C1 / R95-C2 reproduction (scratch clone at 4bda1d1d)

Full detail: `.ufo/waves/round-95/w1/ScoutS320/repro-c1-c2.md` (receipts under `…/ScoutS320/repro/`).

- **C1 cmd 1 (forgery battery) → exit 0**, `forgeries refused 4 of 4; before admits True; honest accepted True`;
  each forgery carries exactly its intended reason (`label-not-frozen`, `label-not-recomputed`,
  `revision-not-bound`, `pins-not-bound`). My receipt is **byte-identical** to the L1's.
  **Operational caveat:** the honest triple `honest-pos.{json,stdout,rc}` is **untracked** (not in the declaration
  commit), so in a clean clone the honest leg finds nothing and the battery exits **1** (`honest accepted False`,
  reason `not-valid`). The honest v5 run must precede the battery, or the triple must be committed. Reproduced
  both ways.
- **C1 cmd 2 (honest v5) → exit 0**, stdout `selfverify ok=True reasons=0` + the frozen label line, stderr empty,
  receipt pins `6fc81208…` / `60026511…`, no temp file left behind.
- **C1 cmd 3 (probe) → exit 0**, `victim_intact true`, `receipt_valid true`, `verdict "hardened"`. Before-state
  reproduced: the same probe against the pinned **v4** writer exits 1 with `verdict "followed-symlink"`,
  `victim_intact false` — SentinelWrite F1 reproduces on this host.
- **Pins:** `sha256sum -c .ufo/waves/round-95/pins.sha256` → every file **OK**. Kill-rule diff clause clean:
  `git diff --stat 4bda1d1d HEAD -- tools/round-95 tools/round-94 tools/round-93` → empty.
- **Attacks on the strengthened instrument (extra, undeclared classes):** a **full-length but wrong** revision is
  refused with the typed reason `revision-not-bound`; a zeroed `counter_sha256` or `verdict_sha256` with
  `pins-not-bound`; a self-consistent re-authored triple filed under a forgery name is caught only by
  `predicted-mismatch`. **The declared named limit is confirmed real**: a wholly re-authored triple describing the
  honest world at the honest revision is **accepted** (`met true`, no reasons, exit 0) — catching it needs
  independent stdout/rc custody, exactly as the declaration states.
- **Host-level confirmation of the S320 ground:** `os.open(planted_symlink, O_WRONLY)` follows the link (the v4
  shape); `O_NOFOLLOW` fails with **errno 40 ELOOP**; `O_CREAT|O_EXCL` fails with **errno 17 EEXIST**;
  `tempfile.mkstemp` creates a fresh unique name and never touches the planted `<out>.tmp`.
- **C2 before-state at 4bda1d1d reproduced:** craft checker exit 1 `block 34 missing (craft has 33 blocks)`;
  depth-v2 exit 1 `blocks 33 resolved 33 expect 34`; depth-v3 exit 1 `required-shaped 0/0` — all matching the
  committed `pre/` receipts. The junk manifest at the declaration commit also exits 1 (block absent), i.e. it is
  **not yet discriminating**; it only becomes a real control once block 34 exists.
- **C2 reachability, measured in a scratch clone:** with a candidate block 34 (4×4 table, marker
  `receipt-world-binding v1`), candidate QUALITY rows 191/192 carrying the frozen atoms, and a stub knowledge
  file, the four frozen commands give **cmd1 exit 0 `ok`**, **cmd2 exit 0 `blocks 34 resolved 34`**, **cmd3 exit 0
  `required-shaped 1/1`**, **cmd4 exit 1 naming the three missing keyword atoms** (the right reason, not a
  missing block). Two landing requirements the depth counters impose: (1) block 34 must cite a
  `corpus/knowledge/…` file that **exists at the landing commit** (my first candidate failed with
  `unresolved: block 34 — absent:2026-11-05-r95-receipt-world-binding.md`, `blocks 34 resolved 33`), and (2) the
  block needs a decision table of ≥3 body rows × ≥4 cells (v2 also wants ≥25 words and ≥2 backtick spans).

## Files written

- `.ufo/waves/round-95/w1/ScoutS320.md` (this report)
- `.ufo/waves/round-95/w1/ScoutS320/s320-recheck.md` (the full table + detail)
- `.ufo/waves/round-95/w1/ScoutS320/s320-open2-fetch1.html`, `s320-open2-fetch2.html`
- `.ufo/waves/round-95/w1/ScoutS320/headers.txt`
- `.ufo/waves/round-95/w1/ScoutS320/scan.py`, `scan2.py`, `words.py`
- `.ufo/waves/round-95/w1/ScoutS320/scan-fetch1.txt`, `scan-fetch2.txt`, `scan2-fetch1.txt`
- `.ufo/waves/round-95/w1/ScoutS320/repro-c1-c2.md` (the R95-C1 / R95-C2 reproduction + attack detail)
- `.ufo/waves/round-95/w1/ScoutS320/repro/` — 17 receipts: `c1-forgery-repro.json`,
  `c1-forgery-repro.stdout`, `honest-pos.json`, `honest-pos.stdout`, `c1-symlink-v5-repro.json`,
  `c1-symlink-v4-repro.json`, `depth-v2-at-decl.txt`, `depth-v3-at-decl.txt`, `depth-v2-candidate.txt`,
  `depth-v3-candidate.txt`, `c2-block34-at-decl.txt`, `c2-after-candidate.txt`, `c2-junk-candidate.txt`,
  `named-limit-reauthored-triple.json`, `attack-consistent-wrong-rev.json`,
  `attack-bad-counter-pin.json`, `attack-reauthored-F3.json`

Scratch `/fast/scratch/hyaku/kaidoku-r95/ScoutS320` — including the `--shared` clone and its two scratch commits
— was deleted before yield. No lane file outside the seat directory and this report was created, edited or
deleted. No mutating git/jj command was run in the lane (`git rev-parse` / `git status` / `git ls-tree` /
`git cat-file` only); the only commits made were inside the scratch clone, after asserting
`git -C "$S/clone" rev-parse --show-toplevel` printed the clone path. No tool was installed or upgraded —
`curl`, `python3` (3.14.8), `sha256sum` were already present.
