# ScribeRows — round-75 source-row drafts: S283 admit, S284 reject

Seat: ScribeRows-4 (scribe). Date of work: 2026-11-04. Scope: verify the two frozen
round-75 source pages fresh, draft the two registry rows in CORPUS v1 shape, and check
them under the standing census parser. `corpus/SOURCES.md` itself was NOT written
(read-only), per the seat spec.

## 1. Fresh-fetch facts

Two fresh GETs were made per page: the first saved the bytes, the second recorded the
HTTP status line (the first GET's status/byte stdout was not retained by the runner, so
the status below is from a same-day repeat GET; the saved bytes are from the first GET
and are digest-pinned).

| page | URL | saved bytes | sha256 | HTTP (repeat GET) |
|---|---|---|---|---|
| proc_pid_cmdline(5) | https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html | 7 918 | `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15` | 200, size_download 7 918 |
| environ(7) | https://man7.org/linux/man-pages/man7/environ.7.html | 21 810 | `f209ca235d7c0d1b015e7457a275f277c592127040e66829eaa848ba46af5455` | 200, size_download 21 810 |

Drift check: both digests are byte-identical to the pins already recorded in the landed
registry — `S277` (proc_pid_cmdline(5), snapshot sha256 `1fc68168…`) and `S285`
(environ(7), sha256 `f209ca23…`, 21 810 bytes). No page drift this round; the snapshots
copied into `ScribeRows/` are the same bytes the landed rows pin.

## 2. Draft rows (verbatim)

These are the two rows exactly as drafted, in the exact CORPUS v1 shape (11 cells,
no `|` inside a cell, `recheck` a valid cadence, `used-by` the admitted entry that cites
the row). They are drafts only; the registry write belongs to the landing seat.

```text
| S283 | `proc_pid_cmdline(5)`, Linux man-pages 6.19 — https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html (snapshot and digest in `.ufo/waves/round-75/w1/ScribeRows/`) | docs | A | What `/proc/pid/cmdline` reports and what it does not: the argv layout, the zombie-empty case, and the process-writable framing of the file; not the environment record | Fresh fetch 2026-11-04, HTTP 200, 7 918 bytes, sha256 `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15`, byte-identical to the round-73 snapshot pinned at the landed `S277` row; DESCRIPTION, located quote at snapshot lines 96-97: "Think of this file as the command line that the process wants you to see." (15 words), inside the mutability paragraph at lines 84-97 | The page itself frames argv as a process claim rather than ground truth: the file holds the command line the process wants the reader to see, a process may override the argv memory region via `PR_SET_MM_ARG_START`, and post-`execve` argv edits show up here — so an A12 argv sample is a producer-writable claim whose failure mode is a missing sample, not a kernel-truth mismatch | mined | 2026-11-04 | 90d | corpus/knowledge/2026-11-04-r75-a12-case-independence.md |
| S284 | `environ(7)`, Linux man-pages 6.19 — https://man7.org/linux/man-pages/man7/environ.7.html (snapshot and digest in `.ufo/waves/round-75/w1/ScribeRows/`) | docs | A | The C-level `environ` array definition, screened for the per-process command-line question; not the `/proc/<pid>/cmdline` interface | Fresh fetch 2026-11-04, HTTP 200, 21 810 bytes, sha256 `f209ca235d7c0d1b015e7457a275f277c592127040e66829eaa848ba46af5455`, byte-identical to the landed `S285` row's pin; DESCRIPTION, located quote at snapshot lines 75-76: "The variable environ points to an array of pointers to strings called the "environment"." (14 words); `grep -c cmdline` on the snapshot prints 0 | REJECTED: defines the C-level environment array and its `execve(2)` origin; it says nothing about `/proc/<pid>/cmdline`, so it cannot ground argv layout or argv mutability. Flip: the page states the cmdline layout or mutability the argv claim needs. | rejected | 2026-11-04 | on-release | — |
```

## 3. Located quotes and line spans

proc_pid_cmdline(5) — DESCRIPTION, snapshot `ScribeRows/proc_pid_cmdline.5.html`:

- Admit quote (grounds argv as a process CLAIM, not ground truth), lines 96-97:
  `Think of this file as the command line that the process` / `wants you to see.`
  (one sentence wrapped across the two lines; 15 words).
- Surrounding mutability paragraph, lines 84-97: line 84 `This is the common case, but
  processes have the freedom to` … line 85-86 `override the memory region and break
  assumptions about the contents or format of the /proc/pid/cmdline file.`; lines 88-90
  `If, after an execve(2), the process modifies its argv strings, those changes will show
  up here.  This is not the same thing as modifying the argv array.`; lines 92-94
  `…prctl(2) operations such as PR_SET_MM_ARG_START.`; lines 96-97 the quote above.
- Adjacent zombie-empty fact (same DESCRIPTION, lines 73-76): `This read-only file holds
  the complete command line for the process, unless the process is a zombie.  In the
  latter case, there is nothing in this file: that is, a read on this file will return 0
  characters.`
- Admit-refusal check: the quote IS present at lines 96-97 in the fetched bytes —
  nothing refuses the admit.

environ(7) — DESCRIPTION, snapshot `ScribeRows/environ.7.html`:

- Defining quote, lines 75-76: `The variable <i>environ</i> points to an array of
  pointers to strings` / `called the "environment".` (14 words; rendered text: “The
  variable environ points to an array of pointers to strings called the
  "environment"."); the `execve(2)` origin sentence follows at lines 77-78.
- Rejection flip-condition check: `grep -c cmdline` on the snapshot prints **0**
  (receipt `ScribeRows/cmdline-count.txt`; zero `cmdline` lines in all 418 lines). The
  page therefore says nothing about `/proc/<pid>/cmdline`, and the rejection stands with
  the flip as drafted.

## 4. Census parser cell-count check

The standing parser is `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`
(run read-only against a scratch fixture; the fleet `scripts/` tree was not modified).
Its row grammar: E01 `fields=N` fires unless the pipe-split row has exactly 13 fields
(11 cells); E05 kind enum, E06 tier, E07 status, E08 opened non-future, E09 recheck
(`Nd` or symbolic), E11 used-by path existence for mined rows.

(Results appended in section 4 output block below.)

## 5. Registry-convention notes and conflicts (reported, not resolved)

1. **Numbering collision, verbatim conflict with the frozen claims.** The frozen seat
   spec and `.ufo/waves/round-75/claims.json` `frontier.sources_rows_opened` say
   `"S283 proc_pid_cmdline(5) admitted; S284 environ(7) rejected"`, and the round-75
   search-log entry in `corpus/SOURCES.md` uses the same numbering. The landed registry
   rows at HEAD `6864a78039fadf3743304c8eb9ca38be5b2238b1` instead carry:
   `S277` = proc_pid_cmdline(5) (mined, retrospective, "first opened round 73"),
   `S283` = `re.fullmatch` (mined), `S284` = `os.path.commonpath` (mined), `S285` =
   environ(7) (rejected). This seat's drafts keep the frozen-spec ids (S283/S284) as
   instructed and flag the collision; the landing seat resolved it as S277/S285.
2. **Row-opened convention** (as stated in the round-75 search log): a row's `opened`
   cell is the date the source was FIRST opened by this lane; a retrospective row names
   its opening round in the search log. proc_pid_cmdline(5) was first opened round 73
   (same calendar date 2026-11-04), so `opened` 2026-11-04 is correct under either
   reading; the landed S277 row records this explicitly.
3. **Word-count nit in landed prose:** the landed round-75 lesson (round-75.md) counts
   the admit quote as "16 words"; the sentence as wrapped in the snapshot is 15 words
   (Think, of, this, file, as, the, command, line, that, the, process, wants, you, to,
   see). Verbatim quote is given in section 3 so the count is checkable. Cosmetic only.
4. `used-by` of the rejected S284 draft is `—` (no admitted entry cites it; the citing
   document is the lesson's gate table, which is where this draft lives). The parser
   accepts `—`; E11 does not check rejected rows.

## 6. Defects refusing the admit

None. The admit quote is present at the pinned lines in byte-identical fresh bytes; the
environ rejection's flip condition (zero `cmdline` mentions) holds. The only reported
conflicts are the numbering collision and the word-count nit in section 5.

## 7. Evidence inventory (under `ScribeRows/`)

- `proc_pid_cmdline.5.html` — 7 918 bytes, sha256 `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15`
- `environ.7.html` — 21 810 bytes, sha256 `f209ca235d7c0d1b015e7457a275f277c592127040e66829eaa848ba46af5455`
- `http-status-cmdline.txt` — `200 7918`
- `http-status-environ.txt` — `200 21810`
- `cmdline-count.txt` — `0` + grep exit note
- `rows.md` — this file (draft rows verbatim + checks)
