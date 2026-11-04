# ScoutSource — r75/w1: the two source pages behind R75-C1's sourced claim

Seat: ScoutSource (scout, leaf). Lane `kaidoku-shokunin`. Scope: re-open
`proc_pid_cmdline(5)` and `environ(7)`, list every passage bearing on (a) argv as
process-controlled, (b) a zombie/empty read, (c) NUL separation, (d) the environment's
exec-boundary origin; say which round-75 claims each passage supports and does not; settle whether
the two `proc_pid_*` pages are one split family and whether S275's cell already says so; and give
the exact provenance trio a knowledge entry citing the cmdline page must carry.

Date 2026-11-04. One fresh GET per URL (HTTP 200), bytes retained under
`.ufo/waves/round-75/w1/ScoutSource/`, digests in `fetch-receipt.json`, machine-readable passages
in `passages.tsv`. No registry, instrument or corpus byte was edited by this seat.

**Verdict summary.** Item 1 VERIFIED · item 2 the pages support the *boundary* halves of R75-C1
and support none of its *predicate* halves · item 3 SAME FAMILY (man-pages 6.19 `proc(5)` split)
and S275's cell already names it · item 4 the trio must cite **S277**, not S283 (see §5) ·
drift NONE.

---

## 1. The passages (line spans in the retained snapshots; quotes ≤25 words)

Raw byte offsets are 0-based into the retained HTML, at the first line of the span. Tags inside a
span are counted in `passages.tsv`; a quote that spans a tag is not a contiguous raw byte string
before whitespace normalisation (same convention as round 73's row).

### `proc_pid_cmdline(5)` — 7 918 B, sha256 `1fc68168…a91f15`

| # | lines | byte | bearing | quote |
|---|---|---|---|---|
| C1 | 73–74 | 2 490 | (b) | "This read-only file holds the complete command line for the process, unless the process is a zombie." (17 w) |
| C2 | 73–76 | 2 490 | (b) | "In the latter case, there is nothing in this file: that is, a read on this file will return 0 characters." (21 w) |
| C3 | 78–80 | 2 825 | (c) | "For processes which are still running, the command-line arguments appear in this file in the same layout as they do in process memory" (23 w) |
| C4 | 80–82 | 2 899 | (c) | "If the process is well-behaved, it is a set of strings separated by null bytes ('\0'), with a further null byte after the last string." (25 w) |
| C5 | 84–86 | 3 096 | (a) | "processes have the freedom to override the memory region and break assumptions about the contents or format of the /proc/pid/cmdline file." (21 w; 4 tags inside) |
| C6 | 88–90 | 3 321 | (a) | "If, after an execve(2), the process modifies its argv strings, those changes will show up here." (16 w; 6 tags) |
| C7 | 92–94 | 3 567 | (a) | "a process may change the memory location that this file refers via prctl(2) operations such as PR_SET_MM_ARG_START." (17 w; 4 tags) |
| C8 | 96–97 | 3 781 | (a) | "Think of this file as the command line that the process wants you to see." (15 w) |

The page has **no permission paragraph**: `grep -c 'ptrace\|PTRACE'` on the snapshot → **0**. Its
SEE ALSO names only `proc(5)`.

### `environ(7)` — 21 810 B, sha256 `f209ca23…af5455`

| # | lines | byte | bearing | quote |
|---|---|---|---|---|
| E1 | 77–78 | 2 877 | (d) | "This array of strings is made available to the process by the execve(2) call when a new program is started." (20 w; 2 tags) |
| E2 | 78–80 | 2 944 | (d) | "When a child process is created via fork(2), it inherits a copy of its parent's environment." (16 w; 6 tags) |
| E3 | 85–86 | 3 449 | (c)* | "The name and the value may not contain an embedded null byte ('\0'), since this is assumed to terminate the string." (21 w) |
| E4 | 109–110 | 4 664 | (d) | "Arguments may also be placed in the environment at the point of an exec(3)." (14 w; 2 tags) |
| E5 | 113–115 | 5 056 | (d) limit | "This list is incomplete and includes only common variables seen by average users in their day-to-day routine." (17 w) |
| E6 | 220–221 | 11 383 | (d) mutability | "The prctl(2) PR_SET_MM_ENV_START and PR_SET_MM_ENV_END operations can be used to control the location of the process's environment." (17 w; 6 tags) |
| E7 | 226–228 | 11 895 | (d) limit | "Switching to the root user using su(1) may result in a mixed environment where LOGNAME and USER are retained from old user" (22 w; 8 tags) |
| E8 | 231–233 | 12 293 | (d) limit | "Many a system command has been tricked into mischief by a user who specified unusual values for IFS or LD_LIBRARY_PATH." (20 w; 4 tags) |
| E9 | 128–129 | 5 767 | (d) limit | "A user's login directory. Set at login time; see section NOTES below." (12 w; 2 tags) |

\* E3 is NUL-bearing but is about **C strings**, not the `/proc/<pid>/environ` byte layout. The
file-layout sentence ("entries are separated by null bytes, with a possible null byte after the
last entry") is on `proc_pid_environ(5)` (S275), not here.

`environ(7)` contains **no `/proc` interface at all**: `grep -c cmdline` → **0**; its single `/proc`
token is a SEE ALSO link to `proc_pid_environ(5)` at snapshot line 330.

---

## 2. Supported / not supported

The lane's own account of what it needs is `tools/round-75/seam-probe.py` (A12 wiring) and the
knowledge entry `corpus/knowledge/2026-11-04-r75-a12-case-independence.md`. Each row is a claim the
wave states or is tempted to state.

| claim | page verdict | grounding |
|---|---|---|
| argv **selection** is producer-writable: a process can rewrite its argv strings, relocate the region, and show a reader what it wants | **SUPPORTED** | C5, C6, C7, C8 |
| a **zero-length** `/proc/<pid>/cmdline` read is a legitimate state, so `[]` must be skipped rather than read as "clean" | **SUPPORTED** | C1, C2 |
| argv entries are NUL-separated with a trailing NUL | **SUPPORTED ONLY CONDITIONED** — the page says "if the process is well-behaved" and that processes may "break assumptions about the contents or format" (C4, C5). The unconditional split in `_proc_argv` (`tools/round-75/seam-probe.py:414-420`) is a convention, not a guarantee. | C3, C4 |
| the environment arrives across the **exec boundary** | **SUPPORTED for the C-level array** (E1, E2, E4). **NOT SUPPORTED for the `/proc/<pid>/environ` file** — that sentence is S275's. | E1, E2, E4 |
| `/proc/<pid>/cmdline` reads are gated by `PTRACE_MODE_READ_FSCREDS` | **NOT SUPPORTED by this page** (0 `ptrace` occurrences). The file-specific gate is S275's sentence; the macro definition is S278's. | C-page absence |
| `home_under`/`tmpdir_under` compared with `is True` (the round-74 survivor `d-home-under-truthy`, closed by `a12-genuine-field-identity`) | **NOT SUPPORTED** — no page says anything about value types, `bool` identity, or path containment under a work root. | — |
| one sample per shim name, or last/first wins (survivor `d-name-samples-last-wins`, closed by `a12-sample-name-merge`) | **NOT SUPPORTED** — neither page describes sampling, repeated launches, or merging. | — |
| `lie_clean` may use a key **superset** instead of the exact four (survivor `d-lie-clean-superset`, closed by `a12-lie-clean-keys-exact`) | **NOT SUPPORTED**, and E5 cuts the other way: the page declares its own variable list *incomplete*, so no page-derived allowlist is exhaustive. | E5 |
| a clean four-key set with no canary ⇒ a clean child (the `canary_present` field) | **NOT SUPPORTED** — E8 puts the documented risk in **values** (`IFS`, `LD_LIBRARY_PATH`), not in key-set membership; a key census cannot bound it. | E8, E5 |
| "the environment record is **not** [producer-writable]" (S277's registry cell, `corpus/SOURCES.md:194`) | **NOT SUPPORTED as written.** E4 says the environment is placed at `exec(3)`; E6 says `PR_SET_MM_ENV_START/END` can relocate it; A12's own forged sub-run passes a launcher-chosen environment (`tools/round-75/seam-probe.py`, `forged_subrun`: `f_env[canary] = "probe-canary-r73"`). What is supported is weaker and sufficient: the record reflects **what the process received at its last exec**, so a child cannot hide its received environment by writing a lying dump. | E4, E6 |
| "Producer-independent **by construction**" (`kernel_witness` docstring) — i.e. no wrapper can defeat the kernel witness | **NOT SUPPORTED.** C8 + E4: a wrapper that re-execs the child with a chosen argv **and** a chosen clean environment is indistinguishable in both files. The witness is independent of the child's *claims*, not of a launcher's choices. | C8, E4 |
| containment of `HOME` implies anything about identity or cleanliness | **NOT SUPPORTED** — E9 makes `HOME` a conventional login-time assignment, and E7 documents a *mixed* environment after `su(1)`, so `HOME`/`LOGNAME` agreement is not an invariant. | E7, E9 |

**The passage the lane must not use**: E8 (`BUGS`, "tricked into mischief … unusual values for IFS
or LD_LIBRARY_PATH"). It is the one passage that directly *limits* the A12 story — the page's own
security warning is about **values**, so a key-set/canary check is not a cleanliness proof, and any
entry that cites `environ(7)` for "the environment is a trustworthy record" would be reading the
page backwards.

---

## 3. Are `proc_pid_cmdline(5)` and S275's `proc_pid_environ(5)` the same split family?

**Yes — same family, and S275's cell already says so.** Measured:

| marker | `proc_pid_cmdline(5)` | `proc_pid_environ(5)` |
|---|---|---|
| path | `man5/proc_pid_cmdline.5.html` | `man5/proc_pid_environ.5.html` |
| footline | `Linux man-pages 6.19    2026-02-08    proc_pid_cmdline(5)` | `Linux man-pages 6.19    2026-02-08    proc_pid_environ(5)` |
| colophon | tarball `man-pages-6.19.tar.gz`, fetched `2026-09-09` | same tarball, same date |
| `proc(5)` split list | `proc_pid_cmdline(5)` at proc.5 snapshot line 381 | `proc_pid_environ(5)` at proc.5 snapshot line 386 |
| section-5 index | listed (`grep -c 'proc_pid_cmdline(5)'` → 1) | listed (`grep -c 'proc_pid_environ(5)'` → 1) |
| SEE ALSO | `proc(5)` only | `proc(5)` only |

**Registry cell.** `corpus/SOURCES.md:192` (S275) already contains the split: "`proc_pid_environ(5)`,
Linux man-pages 6.19 — https://man7.org/linux/man-pages/man5/proc_pid_environ.5.html **(the page
man-pages 6.19 splits out of proc(5)**; snapshot and sha256 in `.ufo/waves/round-72/w1/ScoutSource/`)";
S277's cell carries the same phrase for the cmdline page. So the split is registered, not new, and a
round-75 cmdline row could not have claimed it as new ground.

**`environ(7)` is *not* in the family**: man7, "Miscellaneous Information Manual", no `/proc`
interface (`grep -c cmdline` → 0), footline `environ(7)`. Sharing the 6.19 tarball is a release
fact, not a split fact.

---

## 4. Drift against the digests the lane already holds

| page | served now | prior lane digest | verdict |
|---|---|---|---|
| `proc_pid_cmdline(5)` | 7 918 B, `1fc68168…a91f15` | `.ufo/waves/round-73/w1/ScoutSource/proc_pid_cmdline.5.html`, same digest; `cmp` → **identical** | **no drift** |
| `environ(7)` | 21 810 B, `f209ca23…af5455` | none before round 75 (first open; row S285 carries this digest) | no inter-round test possible; intra-round match |
| `ptrace(2)` (r74) | 104 833 B, `69cd309e…7bd35` | same | **no drift** |
| `proc_pid_environ(5)` (r74) | 7 747 B, `93394d9e…062c46` | same | **no drift** |
| `proc(5)` (r74) | 31 125 B, `b197c5fa…272a97` | same | **no drift** |
| section-5 index (r74) | 39 543 B, `1caa9e6d…e1e74` | same | **no drift** |

Both pages carry `Last-Modified: Mon, 02 Nov 2026 20:20:30 GMT` with distinct ETags while the bytes
are unchanged — a re-render, not a content change. **No freshness defect.**

---

## 5. The provenance trio a knowledge entry citing this page must carry

`CORPUS.md:163-166` requires the three lines first, with `source:` naming the `S###` row, the URL and
an anchor; the lane's practice adds the located quote (≤25 words), the `opened` date and the
snapshot digest.

**Id first.** The frozen container said "S283 `proc_pid_cmdline(5)` admitted"
(`.ufo/waves/round-75/claims.json` at the freeze `ec149dc4`). That field was corrected under a
declared erratum at `1f2f7062` ("S284 `os.path.commonpath` admitted (mined); S285 `environ(7)`
rejected; S283 (`re.fullmatch`) withdrawn as a duplicate of S143"), the S283 row was deleted, and
the cmdline page is **S277** throughout — admitted in round 73 with this same URL and digest. A trio
citing S283 for this page would be a reference-drift defect (the id no longer exists); the trio below
therefore cites **S277**. Timeline and per-revision row table: `ScoutSource/registry-state.md`.

```
source: S277 — Linux man-pages 6.19, proc_pid_cmdline(5), "Think of this file as the command line that the process wants you to see." (first opened in round 73; re-opened 2026-11-04, https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html#DESCRIPTION, DESCRIPTION lines 96-97, 7 918 B, sha256 `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15`, snapshot `.ufo/waves/round-75/w1/ScoutSource/proc_pid_cmdline.5.html`).
verified-at: 2026-11-04 — fresh GET 2026-11-04T08:09:24Z, HTTP 200, byte-identical to `.ufo/waves/round-73/w1/ScoutSource/proc_pid_cmdline.5.html` (`cmp` exit 0); measured at <revision>; receipts `.ufo/waves/round-75/w1/ScoutSource/fetch-receipt.json`, `.ufo/waves/round-75/w1/ScoutSource/passages.tsv`.
recheck: `curl -sS https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html | sha256sum` must print `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15` (7 918 B, footline `Linux man-pages 6.19  2026-02-08`); then re-run the frozen R75-C1 battery command from `plans/round-75-claims.md` and read `survivor_count`, `sole_detector` and `target_pin` in the receipt.
```

Two content constraints that belong in the same entry, taken from §2: cite this page for the
**argv-as-claim boundary only** (C5–C8) and for the **zombie-empty read** (C1–C2); do not cite it for
read permissions (absent) or for anything about `/proc/<pid>/environ` (S275).

---

## 6. Adjacent defects observed (reported, not fixed)

Written as a timeline because the wave repaired part of it while this seat read. Pinned states:
`bfdf03dd` (rows added), `6864a780` (mid-wave read), `1f2f7062` (corrected ledger), `23893e23` and
`501b3c09` (the tips at this write; SOURCES.md unchanged between them).

1. **Id drift in the frozen field — CLOSED by the wave.** At `bfdf03dd` the tree bound S283
   `re.fullmatch`, S284 `commonpath`, S285 `environ(7)`, while `claims.json:57` still named S283 for
   the cmdline page. At `1f2f7062` the field was corrected under a declared `errata` entry and the
   S283 row was withdrawn as a duplicate of S143. No action left for this seat.
2. **Search-log ids — LIVE.** `corpus/SOURCES.md:230` (unchanged since `bfdf03dd`) still says
   "included 1 (**S283**), excluded 1 (**S284**)". At `23893e23` S283 does not exist and S284 is
   `os.path.commonpath`; the included page is S277, the excluded page S285. The sentence's substance
   matches this seat's independent open exactly (two GETs, 7 918 B and 21 810 B, `grep -c cmdline`
   → 0), so this is an id reference-drift, not a false search claim.
3. **Census end receipt and row count — CLOSED.** `l1/census-end.txt` cited by
   `corpus/lessons/round-75.md:37` was absent and the row count read 192 while the lesson claimed
   191, at `6864a780`; at `1f2f7062` the receipt landed (23 W04, `ok`) and the tree holds **191**
   rows, matching the lesson. The 24th W04 seen mid-wave was S283's `re.html` duplicate and went with
   the withdrawn row.
4. **Gate-table counts and one non-quote — LIVE, cosmetic.** The lesson counts S277's quote as 16
   words (whitespace split: **15**) and S284's as 13 (**12**); all rows stay inside the ≤25-word
   limit. Separately, the S143 row places the registry's own *anchor cell* ("Page fetched
   2026-10-28 (HTTP 200, 257,706 bytes, sha256 f169ed06…); anchor `re.fullmatch(...)`") in the
   "located quote" column — a registry cell, not a page excerpt, so that row carries no source quote.

Items 2 and 4 are outside this seat's assignment; they are recorded so the record audit and the
source-row owner can decide. Nothing here was edited.

---

## 7. Files and limits

| path | content |
|---|---|
| `ScoutSource/proc_pid_cmdline.5.html` | served bytes, 7 918 B, sha256 `1fc68168…a91f15` |
| `ScoutSource/environ.7.html` | served bytes, 21 810 B, sha256 `f209ca23…af5455` |
| `ScoutSource/fetch-receipt.json` | URLs, status, bytes, digests, headers, prior-digest and drift table, lane HEAD at record |
| `ScoutSource/passages.tsv` | 17 passages: page, line span, 0-based raw byte, tag count, word count, (a)/(b)/(c)/(d) code, quote, note |
| `ScoutSource/registry-state.md` | the S283/S284/S285/S277 id evidence, census arithmetic, commands |

Limits. (i) Two pages only — no other man7 or kernel source was opened, and no web-wide negative is
claimed. (ii) `environ(7)` had no earlier round digest, so its drift test is intra-round only.
(iii) The registry was being written by peer seats during this read (HEAD advanced `ec149dc4` →
`bfdf03dd` → `ad53c1e1` → `4e0329a4` → `6864a780` → `1f2f7062` → `23893e23` → `501b3c09`); every
registry statement is pinned to the revision named beside it, and the final binding is in
`ScoutSource/registry-state.md` §2. (iv) This seat ran no instrument and re-derived no claim; the A12 mapping
in §2 is a reading of `tools/round-75/seam-probe.py` against the page text, not an execution.
