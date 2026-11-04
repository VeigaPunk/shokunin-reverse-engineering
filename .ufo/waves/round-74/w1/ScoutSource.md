# ScoutSource — r74/w1 independent source verification

Seat: ScoutSource (scout), lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Date: 2026-11-04 (bytes retained in the evidence dir; receipt written 07:40:13 UTC). Scope: the round's sourced row (S278,
`ptrace(2)` `PTRACE_MODE_READ_FSCREDS`) and the three questions the wave put to this seat.
One GET per URL, bytes retained under `.ufo/waves/round-74/w1/ScoutSource/`, digests in
`fetch-receipt.json`. No registry row, instrument or corpus file was edited; writes are
confined to this seat's evidence directory and this report.

Verdict summary: item 1 VERIFIED · item 2 CONFIRMED · item 3 CONFIRMED (the pages still
lack the phrase) with one label discrepancy · item 4 row parses (12 pipes, 11 cells),
quote 15 words, line anchors resolve, but there is no URL fragment anchor — and the frozen
audit's D11 token does not resolve on any live man7 page nor appear in the filed row.

## 1. `PTRACE_MODE_READ_FSCREDS` in `ptrace(2)` — VERIFIED

Observed. `GET https://man7.org/linux/man-pages/man2/ptrace.2.html` → HTTP 200,
**104 833 B**, sha256 `69cd309ece177d54086771701b2085e31cabd14a92484647392bcda468f7bd35`
(retained: `ScoutSource/ptrace.2.html`). Page footline: `Linux man-pages 6.19 2026-02-08`.

Located description, raw lines 1450–1451; term line `<b>PTRACE_MODE_READ_FSCREDS</b>` at
byte offset 83 606, definition at byte offset 83 649:

> `PTRACE_MODE_READ_FSCREDS`
> `Defined as PTRACE_MODE_READ | PTRACE_MODE_FSCREDS.`

Section anchor: the sentence sits in **NOTES → "Ptrace access mode checking"**
(`scout` heading at raw line 1404; the `NOTES` `<h2>` at raw line 1380 carries
`id="NOTES"`). The subsection itself has **no id attribute** — only the h2 anchors exist on
this page (`NAME`, `LIBRARY`, `SYNOPSIS`, `DESCRIPTION`, `RETURN_VALUE`, `ERRORS`,
`STANDARDS`, `HISTORY`, `NOTES`, `BUGS`, `SEE_ALSO`, `COLOPHON`), so the only resolvable
fragment for this text is `https://man7.org/linux/man-pages/man2/ptrace.2.html#NOTES`.
The composed macro's read half is defined at raw lines 1421–1425, which name the file
surface directly: `reading /proc/pid/auxv, /proc/pid/environ, or /proc/pid/stat` — i.e. an
environ read is a `PTRACE_MODE_READ`-class operation combined with the `FSCREDS` modifier.

One HTML caveat: the definition sentence contains a literal `|`, so it can be quoted in
prose but **cannot** be placed verbatim inside a registry cell without breaking the row's
pipe grammar (see item 4).

## 2. Does `proc_pid_environ(5)` state the same check? — CONFIRMED

Observed. `GET https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html` → HTTP 200,
**7 747 B**, sha256 `93394d9edb801ad44e342e8e8ab057bea619d995803221edaf008226b2062c46`
(retained: `ScoutSource/proc_pid_environ.5.html`). Sentence at raw line 90, byte offset
3 541; the rendered text of lines 90–91 (tags stripped) is exactly:

> "Permission to access this file is governed by a ptrace access mode PTRACE_MODE_READ_FSCREDS check; see ptrace(2)."

16 whitespace-separated words. The page thereby binds the generic macro from item 1 to this
specific file; the two pages agree, and neither contradicts the other.

## 3. Do the section-5 index and `proc(5)` still lack "complete command line"? — CONFIRMED

Observed, same fetch day:

| page | URL | bytes | sha256 | hits for "complete command line" (case-insensitive) |
|---|---|---|---|---|
| section-5 index | `…/man-pages/dir_section_5.html` | **39 543** | `1caa9e6d9b3700e20292bcee6a41b9f393af21d617af012ee06de96896fc1e74` | **0** |
| `proc(5)` | `…/man-pages/man5/proc.5.html` | **31 125** | `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97` | **0** |

Both are byte-identical to the round-73 retained copies (`sha256sum` of
`.ufo/waves/round-73/w1/ScoutSource/*.html`), so the round-73 rejection's premise still
holds at the byte level. The phrase occurs exactly once on the page that carries the
paragraph, `proc_pid_cmdline(5)` (7 918 B, sha256 `1fc68168…a91f15`, raw line 73) — not on
`proc(5)` and not on the index.

Label discrepancy (observed). The frozen audit's D11 constant is the literal string
`index.html#_section_5` (`tools/round-74/record-audit.py`, `R73_REJECTED_PAGES`), and
`pre/c2-at-base.json` reports `per_page["index.html#_section_5"]`. That identifier does not
resolve on the live site:

- `…/man-pages/index.html` → HTTP 200, **4 530 B**, sha256 `da70760de42638088cfb7d9b7e9848ccfe537f8ee8587df62438d01605f1bd25`;
  the page has **no anchors at all** (only `name="viewport"` etc.), so `#_section_5`
  resolves to nothing; 0 hits for the phrase.
- `…/man-pages/dir_all_by_section.html` → HTTP 200, 1 658 321 B, sha256
  `2d9f1ee5cf47d26dfa3631fb6dfd84b02633be6d7e9339a1442a329d97243c09`; **0** occurrences of
  `section_5`, 0 hits for the phrase (not retained, 1.6 MB).
- `dir_section_5.html` has **no anchors** (`id`/`name`/`href="#…"` all absent), so no
  fragment can resolve on it either.

[INFERENCE] `index.html#_section_5` is therefore a round-73 *label* for the section-5
index, not a URL that was opened. Round 73's own receipt records the opened URL as
`dir_section_5.html` (`ScoutSource/fetch-receipt.txt:22`); the label was carried into the
audit constant without a page behind it.

## 4. Would the drafted S278 row parse? — YES for shape, with a separate audit binding defect

Observed on the row as filed by ScribeRows, `corpus/SOURCES.md:195`:

- **Pipe count: 12** (leading and trailing included) → 11 cells.
  - Census parser (`scripts/sources-census.sh`, `gawk -F'|'`, contract "11 columns ⇒ NF=13")
    reports `NF=13`, so **no E01**.
  - Audit parser (`record-audit.py:split_row`, `strip("|").split("|")`) yields **11 cells**,
    so the row is in range for `row[7] == "rejected"` / `row[1]` reads. The audit would
    tolerate a missing trailing pipe; the census would not, so 12 is the safe count.
- **Quote word count: 15** (`source-evidence.json` also records 15; measured
  whitespace-separated). Under the ≤25-word cap. The quoted sentence is
  `Use the caller's filesystem UID and GID (see credentials(7)) or effective capabilities for LSM checks.`
  and it equals the **rendered** text of raw lines 1438–1439 after stripping the
  `credentials(7)` `<a>` tag; it is not a raw byte substring of the snapshot (the tag
  splits it), which is expected for an HTML render quoting task.
- **Anchor resolvability: line anchors resolve; no URL fragment exists.**
  - 1421–1425 → the `PTRACE_MODE_READ` bullet naming `/proc/pid/environ` ✔
  - 1437–1439 → `PTRACE_MODE_FSCREDS` and the quoted sentence ✔
  - 1450–1451 → `PTRACE_MODE_READ_FSCREDS` definition ✔
  - The anchor is prose + line numbers; `#NOTES` is the only resolvable fragment for that
    region (the subsection has no id). The row cites no fragment, so nothing dangles, but a
    reader cannot jump to the sentence by URL.
- **Why the draft does not quote the READ_FSCREDS definition itself:** that sentence,
  `Defined as PTRACE_MODE_READ | PTRACE_MODE_FSCREDS.`, contains a literal `|`. Quoting it in
  a cell would raise the row to 13 pipes → 12 cells for the audit and `NF=14` for the census
  (`E01 fields=12`). The filed 15-word FSCREDS sentence is the only ≤25-word, pipe-free,
  verbatim locatable sentence in the same paragraph region. [INFERENCE] This is the correct
  trade-off, not an evasion: the READ half is named by the row's anchor range and by the
  scope cell.

Parser run (read-only, no registry edit): `sources-census.sh validate --root
/home/vgpnk/Projects/shokunin --file …/kaidoku-shokunin/corpus/SOURCES.md --today 2026-11-04`
→ no `E01` for S278; the only S278 line is
`E11 S278 missing used-by corpus/knowledge/2026-11-04-r74-probe-mutation-closure.md`
(that knowledge file does not exist yet at scan time — a pre-landing state, cleared when
ScribeKnowledge's entry lands).

### Routed blocker for R74-C2 as frozen (reported, not edited)

The frozen audit's D11 requires each of four literals in the **source cell** (`row[1]`) of a
`rejected` row. Re-derived over the current registry's 15 rejected rows:

| token | rejected rows whose source cell contains it |
|---|---|
| `proc.5.html` | 1 (S279) |
| `proc_cmdline.5.html` | 1 (S280) |
| `proc_pid.5.html` | 1 (S281) |
| `index.html#_section_5` | **0** |

S282's source cell names only `https://man7.org/linux/man-pages/dir_section_5.html`. Unless
S282's source cell also carries the literal `index.html#_section_5` (recorded as the round-73
label, not as the opened page), D11 stays false at the landing revision and R74-C2's
`mismatch_count` cannot be 0 — the freeze-pinned atom would be red for a reason that is a
label mismatch, not missing evidence. Exact requirement: the substring must appear in the
source cell of a row whose status cell is `rejected`; it must not be introduced into any
non-rejected row's source cell, and it must not displace the actually opened
`dir_section_5.html` URL.

## Observed vs inference

Observed: every HTTP status, byte count, sha256, hit count, cell/pipe/word count, line
number and parser output above, each from `fetch-receipt.json` or the retained bytes.
[INFERENCE]: that `index.html#_section_5` is a label rather than an opened URL (round-73's
receipt names `dir_section_5.html`), and that the FSCREDS-sentence quote was chosen to avoid
the pipe in the READ_FSCREDS definition (supported by the row's own text and the grammar).

## Post-report re-check (S282 correction)

Observed after ScribeRows corrected S282: its source cell now names
`https://man7.org/linux/man-pages/dir_section_5.html` and adds the literal
`index.html#_section_5` explicitly as the round-73 label, "not an opened URL"; the row keeps
12 pipes / 11 cells / status `rejected`. Re-deriving the frozen D11 match over the 15
rejected rows gives `proc.5.html` 1, `proc_cmdline.5.html` 1, `proc_pid.5.html` 1,
`index.html#_section_5` **1** (S282) — the routed blocker above is closed, and the row now
keeps both the actually opened URL and the audit's label without claiming the label resolves.
`sources-census.sh validate --file …/corpus/SOURCES.md --today 2026-11-04` exits **0**, with
no E01/E11 on S278–S282 (`corpus/knowledge/2026-11-04-r74-probe-mutation-closure.md` now
exists, 10 616 B).

## Remaining unknowns

- No second body fetch was made, so byte stability across fetches on 2026-11-04 is not
  measured here; the three named pages match the round-73 copies byte-for-byte, which is the
  only cross-day stability signal available.
- The label's provenance is [INFERENCE] in the narrow sense that no round-73 document spells
  it out: it follows from the audit constant plus round-73's receipt naming the opened URL.
  S282's wording records it as a label, which is the correct claim.
