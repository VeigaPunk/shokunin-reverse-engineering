# ScoutMknod — located quotes (mknod(2), capabilities(7))

Second independent reader of the kernel-side device-accounting ground for R52-C1.
The L1 opens mknod(2) independently; this seat is the second reader and adds
capabilities(7).

Fetch receipts: `receipts/fetch-receipts.json`. Machine-checked quote table:
`receipts/quote-check.json` (every quote below was matched **verbatim** against
the tag-stripped fetched body; `verbatim_present_in_page: true` for all ten).

Both pages fetched 2026-10-30, HTTP 200, from man7.org; each body was re-fetched
and is byte-identical on the second fetch (same sha256).

---

## 1. mknod(2) — https://man7.org/linux/man-pages/man2/mknod.2.html

Body: 16,407 bytes, sha256 `f867026fdb9bd5659971c912b68d6745666211495aafefee9c0645b3923ba5f7`.
Page version: Linux man-pages 6.19, 2026-02-11; HTML rendering created 2026-09-09.

### (1) The EPERM sentence about device files and CAP_MKNOD

Location: `ERRORS` → `EPERM` entry (HTML anchor `#ERRORS`).

> "mode requested creation of something other than a regular file, FIFO (named
> pipe), or UNIX domain socket, and the caller is not privileged"  *(23 words)*

> "the caller is not privileged (Linux: does not have the CAP_MKNOD capability)"
> *(12 words)*

Both halves are in the same `EPERM` entry; together they state the whole
operative point: the privilege gate applies to node kinds **other than** regular
file / FIFO / UNIX-domain socket — i.e. to device special files — and the
capability that carries it is `CAP_MKNOD`.

Supporting scope sentences from the same entry and from `DESCRIPTION`:

| id | location | quote | words |
|---|---|---|---|
| Q3 | `ERRORS` → `EINVAL` | "mode requested creation of something other than a regular file, device special file, FIFO or socket" | 16 |
| Q4 | `DESCRIPTION` | "The file type must be one of S_IFREG, S_IFCHR, S_IFBLK, S_IFIFO, or S_IFSOCK" | 13 |
| Q5 | `ERRORS` → `EPERM` | "also returned if the filesystem containing path does not support the type of node requested" | 15 |
| Q8 | `DESCRIPTION` | "If the file type is S_IFCHR or S_IFBLK, then dev specifies the major and minor numbers of the newly created device special file" | 23 |
| Q9 | `DESCRIPTION` | "The system call mknod() creates a filesystem node (file, device special file, or named pipe) named path, with attributes specified by mode and dev." | 24 |
| Q10 | `VERSIONS` | "Under Linux, mknod() cannot be used to create directories." | 9 |

### (2) Do FIFO and UNIX-domain socket creation need privileges per this page?

**No — this page says the opposite of a privilege requirement for them.** The
`ERRORS`/`EPERM` entry exempts exactly those two kinds: EPERM is returned
"mode requested creation of something other than a regular file, FIFO (named
pipe), or UNIX domain socket, and the caller is not privileged". The privileged
class is therefore the device-special-file class (`S_IFCHR`, `S_IFBLK` — Q4, Q8)
and nothing else. The relevant ERRORS text verbatim:

> "EPERM  *mode* requested creation of something other than a regular
> file, FIFO (named pipe), or UNIX domain socket, and the
> caller is not privileged (Linux: does not have the
> **CAP_MKNOD** capability); also returned if the filesystem
> containing *path* does not support the type of node
> requested."

Raw HTML (mknod.html, `EPERM` entry, tags as served):

```
       <b>EPERM  </b><i>mode</i> requested creation of something other than a regular
              file, FIFO (named pipe), or UNIX domain socket, and the
              caller is not privileged (Linux: does not have the
              <b>CAP_MKNOD </b>capability); also returned if the filesystem
              containing <i>path</i> does not support the type of node
              requested.
```

Two corollaries the L1 should note:

* `EINVAL` (Q3) enumerates the creatable kinds as "a regular file, device
  special file, FIFO or socket" — the same partition as the EPERM sentence, so
  the page's own kind taxonomy puts FIFO and socket **outside** the privileged
  class.
* `VERSIONS` records that POSIX.1-2001 treats FIFO creation as the only
  portable use of `mknod()` and points at `mkfifo(3)` for it — i.e. FIFO
  creation is an ordinary, unprivileged operation, not a privileged one.
* The page also warns that EPERM is returned "if the filesystem containing
  path does not support the type of node requested" (Q5): a device node on an
  unsupported filesystem fails for a second, non-privilege reason. Any rule
  clause that reasons about "the extractor could not have created it" must not
  read EPERM as proof of an unprivileged process.

### (3) Cross-check against the lane's existing source ground

The lane already holds S250 (squashfs-tools 4.7.5 `unsquashfs.c`), which the
round-51 lesson recorded as: char/block-device creation is inside
`if(root_process)` (`:1287`, `mknod` at `:1296`, refusal at `:1313-1318`), while
the FIFO call (`:1328 mknod(pathname, S_IFIFO, 0)`) and the socket call
(`:1349 mknod(pathname, S_IFSOCK, 0)`) sit **outside** that gate. Re-read
first-hand this seat from the committed snapshot
`.ufo/waves/round-51/w1/ScribeSources/body/unsquashfs-4.7.5.c`
(sha256 `6222d940c45537d597e2b36d1d46abbc90f0863e7106bab8fa7bdd97fd939341`,
identical to the S250 row's recorded body hash). Line numbers confirmed:
`if(root_process)` at `:866`, `:1256`, `:1287`; `mknod(pathname, chrdev ? S_IFCHR :`
at `:1296`; `mknod(pathname, S_IFIFO, 0)` at `:1328`;
`mknod(pathname, S_IFSOCK, 0)` at `:1349`.

**The two independent grounds agree in kind, not only in conclusion.** The
kernel side (mknod(2)) says the privilege gate covers device special files and
exempts FIFO and UNIX-domain socket; the tool side (S250) says the extractor
gates exactly the device branch and not the FIFO/socket branches. This is the
kernel-side half of the round-52 law's per-kind split that the round-51
closure had only from the tool side.

---

## 2. capabilities(7) — https://man7.org/linux/man-pages/man7/capabilities.7.html

Body: 83,601 bytes, sha256 `79ca88f6d8984ca2858860e7267d7c4660f6555151cc1f570305a9c6dfccf714`.
Page version: Linux man-pages 6.19, 2026-02-08; HTML rendering created 2026-09-09.

### The CAP_MKNOD definition line

Location: `DESCRIPTION` → `Capabilities list` (the list of capabilities
implemented on Linux; HTML `<b>CAP_MKNOD </b>(since Linux 2.4)` at raw line 188).

> "CAP_MKNOD (since Linux 2.4) Create special files using mknod(2)."
> *(9 words)*

Raw HTML as served:

```
       <b>CAP_MKNOD </b>(since Linux 2.4)
              Create special files using <a href="../man2/mknod.2.html">mknod(2)</a>.
```

A second CAP_MKNOD occurrence exists at raw line 983, under
`DESCRIPTION` → `Effect of user ID changes on capabilities`:

> "CAP_MKNOD (since Linux 2.6.30)"  *(4 words)*

in the sentence: "If the filesystem user ID is changed from 0 to nonzero (see
setfsuid(2)), then the following capabilities are cleared from the effective
set: CAP_CHOWN, CAP_DAC_OVERRIDE, CAP_DAC_READ_SEARCH, CAP_FOWNER, CAP_FSETID,
CAP_LINUX_IMMUTABLE (since Linux 2.6.30), CAP_MAC_OVERRIDE, and CAP_MKNOD (since
Linux 2.6.30)."

### Does capabilities(7) add ground beyond mknod(2) alone?

**Partly, and the part it adds is narrower than mknod(2)'s.**

*What it adds.* capabilities(7) is the kernel's own canonical inventory of the
capability, and it states the capability's *scope* in one line: "Create special
files using mknod(2)". It also dates the capability (since Linux 2.4) and it is
the page that says the capability is dropped from the effective set when the
filesystem UID changes from 0 to nonzero (since Linux 2.6.30) — a fact about
*when* the gate is unavailable that mknod(2) does not state. For a rule that
must claim "an unprivileged extraction cannot create a device node", the second
fact is the one that closes the reasoning: CAP_MKNOD is not merely absent from
a non-root process by default, it is actively cleared from the effective set on
a filesystem-UID transition.

*What it does not add, and where it is weaker.* capabilities(7) says "special
files", which on this page's own taxonomy is **broader** than device nodes —
the same page's DESCRIPTION preamble treats privileged/unprivileged as a
binary and the capability list is not per-file-kind. It therefore cannot carry
the device-only scope by itself: quoting capabilities(7) alone as the ground
for "only device nodes are gated" would be an unsupported generalisation, and
would re-create exactly the inference the round-51 closure rejected (M51-3:
"the inference that all special kinds disappear because unprivileged mknod is
impossible"). The device-only scope comes from **mknod(2)**'s EPERM sentence
and from S250, not from capabilities(7).

*Conclusion for the registry.* capabilities(7) is admissible as a **second,
independent source for the capability's identity and its availability rule**,
provided its row's scope cell says plainly that it does not decide which file
kinds are gated. It is **not** a substitute for mknod(2) and must not be cited
as the law's device-only ground. Candidate id **S253** is free in the lane's
S-space (the lane registry ends at S251; the merge package's 132 staged rows
span S106–S237 and contain no S252/S253), so S252/S253 are the correct
continuation ids for the two rows this round opens.
