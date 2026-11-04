# ScoutSource — r73/w1 source reconnaissance

Seat: ScoutSource (scout). Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Date: 2026-11-04. Scope: the round's one sourced claim (`proc_pid_cmdline(5)` → S277) and
what the round-73 knowledge entry must cite. This seat wrote only under
`.ufo/waves/round-73/w1/ScoutSource*`; it appended no registry row and edited no instrument.
Facts below separate **observed** (tool output) from **[INFERENCE]** (reasoned from observed
bytes/code).

## 1. Fetch evidence — proc_pid_cmdline(5)

**Observed.** One body GET plus one HEAD, 2026-11-04:

| URL | HTTP | bytes | sha256 |
|---|---|---|---|
| `https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html` | 200 | 7 918 | `1fc6816805fa28c1fe015700e7c40efc21d9bbc032e02c35a447004075a91f15` |
| `https://man7.org/linux/man-pages/dir_section_5.html` | 200 | 39 543 | `1caa9e6d9b3700e20292bcee6a41b9f393af21d617af012ee06de96896fc1e74` |

Server: Apache/2.4.58 (Ubuntu); `Last-Modified: Mon, 02 Nov 2026 20:20:30 GMT` on both;
distinct ETags (`"1eee-65f50e092bf80"` / `"9a77-65f50e092bf80"`); HEAD `Content-Length`
equals the GET size on both. Footline: `Linux man-pages 6.19  2026-02-08`; HTML render
2026-09-09 (COLOPHON). No second body fetch, so cross-fetch byte stability is not measured.

**Located quote (the one quote; 17 words), DESCRIPTION `/proc/pid/cmdline`:**

> "This read-only file holds the complete command line for the process, unless the process is a zombie."

Location: snapshot `proc_pid_cmdline.5.html`, raw byte 2504 (0-based) to 2618 exclusive
(114 bytes), raw lines 73–75; no HTML tag inside the span; the raw bytes wrap once
(`\n` + 14 spaces) between "the" and "process", so the space-normalized sentence is not a
raw byte substring. The quote grounds the kernel exposing a per-process command-line record
that another process can read — the mechanism A12 uses to find a shim child.

Supporting location (paraphrase, not a second quote): the same paragraph continues at raw
byte 2986 with the argv layout — NUL-separated strings, a further NUL after the last one —
and closes near raw lines 95–96 by describing the file as the command line the process wants
the reader to see.

## 2. Does man-pages 6.19 split proc(5)? Yes.

**Observed.** The served `proc.5.html` is a 31 125-byte stub,
sha256 `b197c5fa64577269f992d50f60acfd5e0cc3df756644ddd8bd19a02591272a97` (byte-identical to
the round-72 retained copy): 0 occurrences of "complete command line"; its only cmdline
mentions are a cross-reference ("files such as /proc/pid/cmdline and /proc/pid/status") and
SEE ALSO links to `proc_cmdline(5)` and `proc_pid_cmdline(5)`.

**The page that carries the `/proc/pid/cmdline` paragraph:**
`proc_pid_cmdline(5)` — https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html.
The index lists `proc(5)`, `proc_cmdline(5)` and `proc_pid_cmdline(5)` as separate rows (one
`href` each to `proc.5.html`, `proc_cmdline.5.html`, `proc_pid_cmdline.5.html`).
`proc_pid(5)` (12 878 B, sha256 `1fd8ab…`) links `proc_pid_cmdline(5)`, and the cmdline
page's footer says "Pages that refer to this page: proc_pid(5)".

**Do not confuse the two `cmdline` pages.** `proc_cmdline(5)`
(https://man7.org/linux/man-pages/man5/proc_cmdline.5.html, 6 794 B,
sha256 `3f7f31a728fb358ffad603c697674433344151ba76b60c1c3aa7a573533aebdd`) documents
`/proc/cmdline - kernel boot arguments`, a different file. The S277 row cites the `proc_pid`
page only.

## 3. Registry state and next id

**Observed** (from the lane root, 2026-11-04):

```
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md   → 183
grep -E   '^\| S[0-9]{3}' corpus/SOURCES.md | tail -1                   → S276, line 193
grep -c   'S277' corpus/SOURCES.md                                      → 0
malformed-row census (NF!=13)                                           → 0
duplicate-id census                                                     → no output
grep -c   'proc_pid_cmdline' corpus/SOURCES.md                          → 0
grep -oE 'https://man7.org/linux/man-pages/man5/proc[^ )|]*' corpus/SOURCES.md
                                                                        → only S275's proc_pid_environ.5.html
```

Highest id: **S276**. The candidate URL is **not present in any S-row**; the only man7
section-5 source is S275 (the `environ` split page). Under the registry id rule
(`S` + 3 or more digits, the next unused, never reused) the exact next id is **S277**;
`claims.json` already declares `claim_row: "S277"`, so the allocation is the container's.
Under SOURCES rule 2 (append-only) the row is appended at `corpus/SOURCES.md:194`, after
S276; this seat drafted it at `.../ScoutSource/sources-row.md` but did not write it.

## 4. What the round-73 knowledge entry must cite

Target: `corpus/knowledge/2026-11-04-r73-kernel-witness-record.md` — **absent** at scan time
(`ls` → "No such file or directory").

**Required `source:` row.** CORPUS.md's provenance-trio rule: a new entry opens with
`source:`, `verified-at:`, `recheck:` first; when the source is external, `source:` cites the
`S###` row in `corpus/SOURCES.md` alongside the URL and anchor. The r70/r71 entries show the
accepted form (trio at file lines 1–3, before the title); the r72 entry's trio sits at lines
66–68, which is exactly routed defect D5 the round repairs. So the r73 entry must open:

```
source: S277 — `proc_pid_cmdline(5)`, Linux man-pages 6.19,
https://man7.org/linux/man-pages/man5/proc_pid_cmdline.5.html, DESCRIPTION `/proc/pid/cmdline`
(snapshot bytes 2504-2618, lines 73-75; fetched 2026-11-04, HTTP 200, 7 918 bytes, sha256
1fc68168…); own-work evidence: tools/round-73/seam-probe.py and the round-73 receipts pinned by
.ufo/waves/round-73/claims.json at the declaration.
verified-at: <landing revision> — <the C1/C2/C3 landing receipts>.
recheck: <the frozen claim commands / selftest invocations>.
```

It must also carry the `probe arms` scope honestly: S277 grounds **A12's process selection**
(`/proc/<pid>/cmdline`, NUL-split argv, shim-path prefix), while S275 grounds the **environment
bytes** (`/proc/<pid>/environ`). The source row's scope cell and the entry's limits must say
the page documents a mutable, self-declared argv, not authenticated identity.

**Does any existing entry already claim the kernel-witness surface? No — observed:**

- `grep -rn 'A12' corpus/` → no knowledge or lesson hit (only a CLI `-A12` help example and
  binary noise in an unrelated squashfs carrier).
- `grep -rniE 'kernel[ _-](side|witness|sample)|/proc/%d|proc/self/cmdline|proc_pid_cmdline'
  corpus/knowledge corpus/lessons` → 0 hits.
- The r72 entry explicitly bounds it out: "a hostile replacement wrapper that forges both
  witnesses is outside this class" (`corpus/knowledge/2026-11-04-r72-checker-env-capsule.md:48`);
  `corpus/lessons/round-72.md:45` calls it a class boundary.
- `corpus/README.md:335` lists "a producer-independent (hostile-wrapper) child census" as
  still Frontier.

So the r73 entry is the first claim on this surface at base, and it must not cite the r72
entry as already holding it.

## 5. Consumer trace — how the page is used, and its honest limit

**Observed** in `tools/round-73/seam-probe.py` (frozen at `da6c17c1`; worktree diff empty):

- `_proc_argv()` (`:407-412`) opens `/proc/%d/cmdline`, splits the bytes on `\x00`, drops
  empties — the NUL layout the page documents at raw bytes 2986–3054.
- `kernel_witness()` (`:431-458`) enumerates `/proc`, skips PIDs already seen, keeps a process
  when any argv element startswith the shim directory prefix, then reads `_proc_environ(pid)`.
- `_name_samples()` (`:544-557`) keys each sample by the basename of the matched argv path
  (`git` / `readelf`).
- The receipt's `channels` block (`:638-641`) has exactly three keys — `keys_exact`, `canary`,
  `checker_summary` — all naming `child dump + kernel /proc/<pid>/environ`; it does **not**
  name `/proc/pid/cmdline` or S277.

**[INFERENCE] Limit the entry must state.** A12's *environment sample* is kernel-side, but its
*selection* reads `/proc/<pid>/cmdline`, and the cited page says a process may override that
memory region, break assumptions about its contents/format, and move it with
`PR_SET_MM_ARG_START`. Therefore a hostile wrapper that rewrites its argv, or execs the real
shim outside the watched prefix, can evade selection even though the environ it would have
exposed is kernel-recorded. The producer-independence claim covers the sampled environment
bytes, not process identity; the page itself calls the file what the process wants seen.

## 6. Evidence gap found — the plan's "C1 receipt's channels block" pointer

`plans/round-73-claims.md` Frontier step says the new row "is cited by the round-73 knowledge
entry and the C1 receipt's `channels` block."

**Observed.** The instrument frozen at the declaration emits a channels block with exactly
`keys_exact`, `canary`, `checker_summary` (`git show da6c17c1:tools/round-73/seam-probe.py`
lines 638-641; `git diff da6c17c1 -- tools/round-73/seam-probe.py` empty). The only C1
receipt present, `.ufo/waves/round-73/pre/c1-at-base.json`, repeats those three keys
(`:324`) and cites `/proc/<pid>/environ`, not the cmdline page. The receipt does carry A12
`observed.genuine/forged.kernel[*].argv` arrays, which show cmdline was read, but no field
names `/proc/pid/cmdline` or S277.

**Consequence.** The knowledge entry can cite S277 (first half of the sentence). The second
half cannot be satisfied by the frozen instrument's `channels` block without a post-freeze
instrument edit, which the claim's kill rule forbids ("a post-freeze instrument edit → not
verified"). Options for Main/L1: (a) file a pre-landing erratum correcting the frontier-step
sentence to the receipt's `observed.A12_kernel_witness` argv evidence plus the instrument
source line, or (b) disclose in the landing report that the pointer is prose, not a receipt
field. This seat did not edit the plan or instrument.

## 7. Gaps / not claimed

- One body fetch per URL: no cross-fetch byte-stability measurement; HEAD sizes agree.
- man7 may re-render the page; the sha256 pins this 2026-09-09 render of man-pages 6.19.
- S277 is drafted, not appended; the target knowledge entry is absent. `ScribeKnowledge-12`
  was messaged with the opened status, quote, hash and id so the entry does not assume an
  append that has not happened.
- The `source:` row's `mined` status needs an existing `used-by` path at census time; see the
  append-sequencing note in `sources-row.md`.
- Not claimed: that a kernel-side observer cannot be defeated by argv rewriting; that
  `/proc/<pid>/cmdline` bytes are immutable; that the page documents `environ` (S275 does).

## Files

- `.ufo/waves/round-73/w1/ScoutSource/fetch-receipt.txt` — HTTP/HEAD evidence and quote locator.
- `.ufo/waves/round-73/w1/ScoutSource/sources-row.md` — exact S277 row and shape checks.
- `.ufo/waves/round-73/w1/ScoutSource/proc_pid_cmdline.5.html`, `dir_section_5.html`,
  `proc.5.html`, `proc_pid.5.html`, `proc_cmdline.5.html` — retained snapshots (sha256 above).
- `.ufo/waves/round-73/w1/ScoutSource.md` — this report.

Report: .ufo/waves/round-73/w1/ScoutSource.md
