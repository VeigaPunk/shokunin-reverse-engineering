# Gate — ScoutSource (round 67, w1)

Class rule under test: a SquashFS char-device entry is a device-node inode, not a file payload,
so a regular-file extractor cannot reproduce it.

## 1. Assigned locator — opened, quote absent

- URL: `https://docs.kernel.org/filesystems/squashfs.html`
- Access: 2026-11-03 (local) / `2026-11-04T00:55:58Z` (HTTP `Date` header); one fetch.
- Result: HTTP **200**, **26 045 B**, sha256
  `10767bbf8b5c49e81d7aafadd84b6e06602c19641d7f7ae9b0a0258d81733685`,
  `text/html; charset=utf-8`, `Last-Modified: Sun, 01 Nov 2026 22:46:23 GMT`.
- Title: "Squashfs 4.0 Filesystem — The Linux Kernel documentation" (page label `7.4.0-rc1`).
- Fallback `https://www.kernel.org/doc/html/latest/filesystems/squashfs.html` was **not** used:
  the assigned URL served 200, so the 404 branch never triggered.

**Quote: REJECTED.** The expected inode-type text does not exist in the fetched bytes.

Probes over the 26 045 fetched bytes (all case-insensitive):

| probe | occurrences |
|---|---|
| `Basic device inode` | 0 |
| `Extended device inode` | 0 |
| `major` (any case, any line) | 0 |
| `minor` (any case, any line) | 0 |
| `Basic` (any case) | 0 |
| `Extended` (any case) | 2 |
| `device` (any case) | 6 lines / 7 occurrences |

No section heading in the page introduces a device-inode layout. The page's section list jumps
`3.2 Inodes`, `3.3 Directories`, `3.4 File data`, `3.5 Fragment lookup table` — there is no
device-inode subsection. The two `extended` occurrences are not about devices: raw bytes
415–418 say "two types of regular file inode and directory inode are defined: … and extended
types where extra information has to be stored", so on this page "extended" is a regular-file and
directory notion only. Maximum contiguous device statement is one sentence spread over raw
bytes lines 412–414:

```
412	To maximise compression there are different inodes for each file type
413	(regular file, directory, device, etc.), the inode contents and length
414	varying with the type.
```

and a size remark over lines 264–266:

```
264	compressed inode is on average 8 bytes in length (the exact length varies on
265	file type, i.e. regular file, directory, symbolic link, and block/char device
266	inodes have different sizes).
```

Both are rendered-HTML prose (QUALITY #17 excludes text obtained by rendering markup from
machine-gradeable use), and neither states major/minor, `rdev`, or payload absence. Per the seat
rule, an unfindable quote is a rejection, not a paraphrase — so **this URL is rejected as the row
locator for the class rule**.

## 2. Substitute locator — text found, contiguous, pinned

The wording the seat expected ("Basic device inode" / "Extended device inode", major/minor) is the
squashfs-tools-ng format description, whose real heading is `=== Device Special Files`.

- Document: squashfs-tools-ng `doc/format.adoc`
- URL (pinned): `https://raw.githubusercontent.com/AgentD/squashfs-tools-ng/e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90/doc/format.adoc`
- Access: 2026-11-03 (local) / `2026-11-04T00:55:58Z` (HTTP `Date`).
- Result: HTTP **200**, **41 981 B**, sha256
  `08c38b69a9fda3d1a7ce9784132a75cb8c8d65f290e2747af74ab58ae50c82eb`, `text/plain; charset=utf-8`.
- Commit pin `e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90` (2024-03-23T23:00:58Z, "fixed fragment
  table size typo") is the last commit touching the file; bytes fetched at the pin are
  `cmp`-identical to the bytes fetched at `master` (same sha256), so neither is a stale rendering
  of the other.
- Locator (heading that structurally contains the quote): `=== Device Special Files`, fetched-bytes
  **line 730**.

**Quote (13 words, verbatim, fetched-bytes line 732):**

> Basic device special files only store a hard-link counter and a device number.

Contiguity proof: the byte string occurs **exactly once** in the 41 981 fetched bytes, at byte
offset 28 445, line 732 (`python3` `bytes.find` + count over the pinned file).

Companion text in the same section (supporting material, **not** the submitted quote):

```
732	Basic device special files only store a hard-link counter and a device number.
733	The layout is identical for both character and block devices:
...
742	                        On Linux, this consists of major and minor device
743	                        numbers that can be extracted as follows:
745	                          major = (dev & 0xFFF00) >> 8.
746	                          minor = (dev & 0x000FF) | ((dev >> 12) & 0xFFF00)
```

Type-code grounding, heading `=== Common Inode Header` (line 531), table lines 549 and 556:
`!  5 ! Basic Character Device` and `! 12 ! Extended Character Device`, distinct from
`!  2 ! Basic File` (line 546).

Lines 732–733 together establish the class rule: the entry is a *device special file* inode whose
stored fields are a link count and a device number (character and block identical) — there is no
block list and no data payload, unlike a regular file inode.

## 3. Registry check — no duplicate

- `grep -c 'kernel\.org' corpus/SOURCES.md` → **0**. No row anywhere in the registry cites any
  kernel.org locator, so the assigned page is not an existing row (nor a near duplicate of one).
- `grep -n 'format.adoc\|Device Special Files\|special files\|docs.kernel.org' corpus/SOURCES.md`
  → **no match**. The substitute locator is also not registered.
- No row cites `squashfs-tools-ng`, `tools-ng` or `AgentD`.
- Nearest adjacent rows, and why they are not duplicates:
  - **S250** — squashfs-tools 4.7.5 `unsquashfs.c`, char/block-device *privilege refusal*
    (`mknod`, `root_process`). Different locator, different object: extractor behaviour as an
    unprivileged user. S250 explains why a device node fails to be created; the proposed row
    explains why no payload exists to create. Neither implies the other.
  - **S108 / S112 / S245** — unblob 26.6.4 SquashFS handler argv and dependencies.
  - **S114 / S124** — AVM-BE marker and reader patch.
  None describes the on-disk device-inode layout or its `rdev` major/minor encoding.
- Rule label note: `CORPUS.md` `### Rules` item 2 is **Append-only** ("Only `status`, `recheck`
  and `used-by` change in place … A correction is a new row whose `teaches` opens
  `supersedes S0NN —`"), not a duplicate rule. Dedupe is not triggered here because no row exists
  to supersede; the append-only rule is satisfied by adding one new row.

## 4. Verdict

- Assigned locator: **rejected** (quote absent; probes recorded above). Do not register it for this
  class rule, and do not let a paraphrase of it stand in for a quote.
- Proposed row locator: **`doc/format.adoc` at `e3dcf177…`, §Device Special Files, line 732** —
  accepted on contiguity (1 occurrence) and heading containment, with the commit pin making it
  re-openable byte-for-byte.
- Residual limit: this is a second implementation's format description, not the kernel's own
  header. It states the layout directly; it does not by itself prove any carrier contains such an
  entry, and it says nothing about extraction outcomes. Class-rule support only.

## 5. Retained bodies

Both fetched bodies are kept beside this file so every probe above is re-runnable offline:

- `fetched-squashfs-docs.html` — 26 045 B, sha256 `10767bbf…33685` (assigned URL).
- `fetched-format.adoc` — 41 981 B, sha256 `08c38b69…c82eb` (pinned substitute; quote at line 732,
  1 occurrence).

