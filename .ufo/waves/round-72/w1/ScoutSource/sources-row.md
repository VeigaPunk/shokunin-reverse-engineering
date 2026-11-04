# sources-row — S275 (ScoutSource, r72/w1)

State: **ready to append, not appended.** This seat wrote no registry byte. `corpus/SOURCES.md`
belongs to whichever seat owns the registry; the row below is the exact 11-cell line and the
insertion point is the line after the current last registry row (`corpus/SOURCES.md:191`, S274).

## The row (one line, verbatim)

| S275 | `proc_pid_environ(5)`, Linux man-pages 6.19 — https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html (the page man-pages 6.19 splits out of proc(5); snapshot and sha256 in `.ufo/waves/round-72/w1/ScoutSource/`) | docs | A | What `/proc/pid/environ` reports: the initial environment installed by `execve(2)`, entries NUL-separated with an optional trailing NUL, later modifications explicitly not reflected, `PR_SET_MM_ENV_START` able to move the reported block, and a `PTRACE_MODE_READ_FSCREDS` read check; not any carrier's environment, not a probe result, not a statement about `os.environ` after interpreter start | man-pages 6.19, page dated 2026-02-08; fetched 2026-11-04, HTTP 200, 7 747 bytes, sha256 `93394d9edb801ad44e342e8e8ab057bea619d995803221edaf008226b2062c46`; DESCRIPTION paragraph snapshot bytes 2465-3712, lines 72-91; quoted sentence begins at byte 2511 (0-based), line 73; the split stub `proc.5.html` (31 125 B, sha256 `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97`) carries only a SEE ALSO link to this page | Grounds a child-environment measurement as the exec-boundary snapshot: "This file contains the initial environment that was set when the currently executing program was started via execve(2)." (18 words) The same paragraph adds that entries are NUL-separated with a possible trailing NUL and that later putenv(3) changes are not reflected — so a raw capsule read at a shim's exec boundary measures what execve installed, while a later in-process `os.environ` view measures neither the same bytes nor the same source. | mined | 2026-11-04 | 180d | `.ufo/waves/round-72/w1/ScoutSource.md` |

## Checks on this exact line

- **11 cells.** `awk -F'|'` on the row gives NF-2 = 11 (leading and trailing empty fields).
- **No pipe inside any cell.** No literal `|` and no escaped `\|`: cell count equals 11, so a
  split on `|` recovers the 11 values with nothing to escape. The only separators are the 12 pipes.
- **Id is free.** Census `grep -oE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md`:
  181 rows, max id S274, and `grep -c 'S275\|S276'` = 0 over the whole file — S275 is the next
  free id (S276 stays free if another seat needs it).
- **URL is new.** `grep -n 'proc_pid_environ' corpus/SOURCES.md` (all lines, no indent filter)
  and `grep -n 'man5/proc.5.html'` both exit 1. The three existing `man7.org` rows (S146, S148,
  S252) are different pages; same host is not a duplicate.
- **Quote is 18 whitespace-separated words** (limit 25): verified by `split()` on the sentence.
- **Quote locator.** The sentence is not a contiguous byte string in the snapshot: it spans
  lines 73-75 and carries one HTML anchor (`<a href="../man2/execve.2.html">execve(2)</a>`,
  starts byte 2680). Raw span is bytes 2511-2693 (0-based, 183 bytes); in the tag-stripped
  render the sentence starts at offset 840 of the plain text. A byte-substring search for the
  rendered sentence therefore finds nothing in the raw snapshot — the anchor is the seam.
- **Status/date/recheck** follow the registry's current style: `mined`, `2026-11-04`, `180d`
  (same cadence as the other man-page rows, S252).

## Not claimed

- Not appended here, and not claimed to be appended by anyone else in this wave.
- The `used-by` cell cites this seat's report; the r72 knowledge entry being drafted by another
  seat may add itself to that cell when it lands.
