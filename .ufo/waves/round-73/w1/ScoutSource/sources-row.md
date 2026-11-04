# sources-row — S277 (ScoutSource, r73/w1)

State: **ready to append, not appended.** This seat wrote no registry byte. The row below is
the exact 11-cell line; the insertion point is `corpus/SOURCES.md:194`, between the current
last registry row (S276, line 193) and the blank line before `## Paths` (line 195).
`claims.json` already declares `claim_row: "S277"`, so the id is allocated by the container,
not chosen by this seat.

## The row (one line, verbatim)

| S277 | `proc_pid_cmdline(5)`, Linux man-pages 6.19 — https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html (the page man-pages 6.19 splits out of proc(5) for `/proc/pid/cmdline`; snapshot and sha256 in `.ufo/waves/round-73/w1/ScoutSource/`) | docs | A | What `/proc/pid/cmdline` reports: each process's complete command line as NUL-separated argv with a trailing NUL after the last string for a well-behaved process, empty for a zombie, mutable by the process via argv rewrite or `PR_SET_MM_ARG_START`; not `/proc/cmdline` (kernel boot arguments), not a probe result, and not proof that a kernel-side observer selected the intended process | man-pages 6.19, page dated 2026-02-08; fetched 2026-11-04, HTTP 200, 7 918 bytes, sha256 `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15`; DESCRIPTION `/proc/pid/cmdline`, snapshot bytes 2504-2618, lines 73-75; the split stub `proc.5.html` (31 125 B, sha256 `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97`) carries no paragraph, only SEE ALSO links | Grounds a kernel-side observer's child lookup: "This read-only file holds the complete command line for the process, unless the process is a zombie." (17 words) The file exposes argv to another process, so `tools/round-73/seam-probe.py` lists `/proc`, reads `/proc/<pid>/cmdline`, splits on NUL and selects the shim by argv path before sampling `/proc/<pid>/environ`; argv is self-declared and mutable, so this grounds selection, not authenticated identity or the environment bytes. | mined | 2026-11-04 | 180d | corpus/knowledge/2026-11-04-r73-kernel-witness-record.md, .ufo/waves/round-73/w1/ScoutSource.md |

## Checks on this exact line

- **11 cells / NF=13.** `awk -F'|'` on the row: 13 fields, so 11 values between the leading and
  trailing empty fields. No literal `|` inside any cell, so a split on `|` recovers the values.
- **Id is free.** Census (frozen command in CORPUS.md):
  `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` → `183`;
  max id S276; `grep -c 'S277' corpus/SOURCES.md` → `0`; duplicate-id and malformed-row
  censuses print nothing. Next unused id = **S277** under the registry's id rule
  (`S` + 3 or more digits, the next unused, never reused).
- **Append-only.** CORPUS.md SOURCES rule 2: only `status`, `recheck` and `used-by` change in
  place, each logged old→new in the round lesson. The row itself is a new line, appended.
- **URL is new.** `grep -c 'proc_pid_cmdline' corpus/SOURCES.md` → `0`. The only man7.org
  section-5 page in the registry is S275 (`proc_pid_environ.5.html`), a different page.
  `grep -oE 'https://man7.org/linux/man-pages/man5/proc[^ )|]*'` returns only S275's URL.
- **Quote is 17 words** (`split()` on the sentence; limit 25). Location: raw byte 2504
  (0-based), lines 73-75, 114 raw bytes, no tags inside; raw wrap is newline + 14 spaces, so
  the sentence is not a contiguous raw byte string before whitespace normalization.
- **Anchor carries revision + bytes.** man-pages 6.19, page dated 2026-02-08; man7 HTML render
  2026-09-09 (COLOPHON); fetched 2026-11-04 with HTTP 200 and the sha256 above.
- **Split premise.** serviced `proc.5.html` is a 31 125-byte stub (sha256 identical to the
  round-72 retained copy) with 0 occurrences of "complete command line"; the paragraph is on
  `proc_pid_cmdline(5)`. `proc_cmdline(5)` is `/proc/cmdline - kernel boot arguments` and is
  NOT the cited page.
- **Status/date/recheck** follow the neighbouring man-page row (S275): `mined`, `2026-11-04`,
  `180d` (page is a released man-pages edition; recheck on man-pages release).

## Append sequencing (for the registry owner)

- `mined` requires at least one `used-by` path that exists at census time
  (CORPUS.md census: "mined rows whose used-by paths do not exist — must print nothing").
  This seat's `.ufo/waves/round-73/w1/ScoutSource.md` exists once this report lands; the
  knowledge entry `corpus/knowledge/2026-11-04-r73-kernel-witness-record.md` lands with the
  scribe. Append after both exist, or append with `queued` / `—` and update to `mined` when
  the entry lands (status/used-by in-place change is allowed and must be logged old→new).
- Round-end census target: 184 rows (183 at start, +1), exit 0, per
  `plans/round-73-claims.md` Frontier step.
