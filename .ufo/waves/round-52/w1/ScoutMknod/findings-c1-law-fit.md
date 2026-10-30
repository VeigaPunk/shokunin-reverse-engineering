# ScoutMknod — findings on how the kernel-side ground fits the R52-C1 law

Scope: this seat was asked to open the man-page ground for R52-C1 and to say
whether a capabilities(7) row adds ground beyond mknod(2) alone. It also
checked the claim's own width statement against the committed oracle tables,
because the kernel ground and the corpus width have to agree for the law to
hold. Nothing here is a claim measurement; no carrier was fetched, no
extraction was run, no REA was invoked.

## 1. The kernel-side ground the claims draft names (S252) is present and correct

The claims draft's law says: "the kernel-side gate is CAP_MKNOD on device files
(S252, opened this round)". The page supports exactly that, in one sentence,
in `ERRORS`/`EPERM`:

> "mode requested creation of something other than a regular file, FIFO (named
> pipe), or UNIX domain socket, and the caller is not privileged (Linux: does
> not have the CAP_MKNOD capability)"

Read as a partition of `mode`, the privileged class is what remains after
removing regular file, FIFO and UNIX-domain socket — i.e. the device special
files (`S_IFCHR`, `S_IFBLK`; the page's own `EINVAL` entry enumerates the same
partition: "a regular file, device special file, FIFO or socket").

So the kernel side gives the law what it needs: **a device-only privilege
gate, with FIFO and socket creation explicitly outside it.** This is
independent corroboration of the round-51 closure's rejection (M51-3) of the
shared special-inode inference — the kernel's own documented partition is
per-kind, and it is device-only.

## 2. Two independent grounds now agree in kind, not merely in conclusion

| kind | kernel side (this seat, S252) | tool side (lane's S250, re-read first-hand) |
|---|---|---|
| char/block device | privileged — needs `CAP_MKNOD` | inside `if(root_process)` (`:1287`, `mknod` `:1296`, refusal `:1313-1318`) |
| FIFO | not privileged (exempt clause) | outside the gate (`:1328 mknod(pathname, S_IFIFO, 0)`) |
| UNIX-domain socket | not privileged (exempt clause) | outside the gate (`:1349 mknod(pathname, S_IFSOCK, 0)`) |

Re-read first-hand this seat from the committed round-51 snapshot
`.ufo/waves/round-51/w1/ScribeSources/body/unsquashfs-4.7.5.c` (sha256
`6222d940c45537d597e2b36d1d46abbc90f0863e7106bab8fa7bdd97fd939341`, identical
to the hash recorded in S250's row). All four cited line numbers confirmed.

The round-51 closure had only the tool side. The kernel side is now a second,
independent reader of the same per-kind split, which is what the law's
"per-carrier-class derivation … the generalisation to fifo/socket/block rests
on the source ground" sentence needs.

## 3. The corpus width statement checks out against the committed tables

The claim's F5 width statement says "no fifo, socket or block-device row exists
in any measured carrier". Verified against the four committed oracle
non-regular tables (`tools/round-50/oracle/<id>.nonregular.tsv`):

| carrier | char-device rows | fifo / socket / block rows | other kinds |
|---|---|---|---|
| c6430 | 1 | 0 | dir, symlink |
| c6490 | 1 | 0 | dir, symlink |
| g7581 | 13 | 0 | dir, symlink |
| g7582 | 13 | 0 | dir, symlink |

Across all four tables the only kinds present are `char-device`, `dir`,
`symlink`; the count of rows whose kind field is `fifo`, `socket`,
`block-device` or `device` is **0**. The Cable class carries exactly one
char-device and the FRITZ!Box class exactly thirteen, matching the claim's
class statement.

Two consequences the L1 should keep straight in the rule text:

* The "no fifo/socket/block row exists" fact is a **corpus** fact, not a
  privilege fact. The kernel ground says fifo/socket creation is *not*
  privileged; the corpus says the measured carriers contain no such rows. The
  rule's `allowed` lists for those kinds must therefore be justified by the
  corpus width (and fail-closed on a future carrier that does contain one),
  **not** by "the extractor could not have made it" — the kernel ground
  refutes that reason for fifo/socket. This is the exact trap M51-3 records.
* Conversely, for **char/block device**, the kernel ground *does* supply the
  reason: an unprivileged process cannot create the node. That is why the
  law's device clause can be a law while the fifo/socket clause must be a
  width statement.

## 4. One caveat the L1 should carry into the rule's own wording

mknod(2)'s `EPERM` entry carries a **second** cause: EPERM is "also returned
if the filesystem containing path does not support the type of node requested".
So an EPERM on `mknod` is not by itself evidence that the caller was
unprivileged; on a filesystem without device support even a privileged caller
gets it. Any clause in `tools/round-52/gap-rule.json` or the v2 counter that
infers "unprivileged" from a creation failure must not read the errno alone.
The lane's own extraction runs on ordinary filesystems, so this is a wording
hygiene point rather than an observed failure — but it is exactly the kind of
over-read that the law's `law_shape_ok` clause exists to prevent, and it is
cheapest to write the clause correctly now.

A related precision point: the page says EPERM is returned for creation of
"something other than a regular file, FIFO (named pipe), or UNIX domain
socket". `mknod(2)` can create a socket inode (`S_IFSOCK` is in the allowed
list) but *not* a bound UNIX-domain socket endpoint; `socket(2)` is the call
that creates a usable endpoint. The claim's law speaks of "socket" rows in the
oracle, i.e. inode kinds in the image, which is the `S_IFSOCK` case. The
distinction does not change the law but the rule's wording should say
"socket inode" rather than "UNIX domain socket" if it wants to be exact.

## 5. capabilities(7): admissible, but it cannot carry the per-kind split

Full argument in `candidate-sources-rows.md`. Short form: capabilities(7)
gives the capability's canonical inventory entry ("CAP_MKNOD (since Linux 2.4)
Create special files using mknod(2)") and — usefully — the availability rule
that mknod(2) does not state: `CAP_MKNOD` (since Linux 2.6.30) is cleared from
the effective set when the filesystem UID changes from 0 to nonzero. That is
what lets "an unprivileged extraction cannot create a device node" be a
statement about the effective capability set rather than about uid 0 alone.

But its scope word is "special files", which is broader than device nodes on
that page's own taxonomy, so it cannot decide which kinds are gated. Citing
S253 for a device-only rule would be an unsupported generalisation of the same
family as M51-3. Recommendation: admit S253 with a scope cell that says so, and
keep every device-only citation pointing at S252 (+ S250 for the extractor
side).

## 6. What was not done (stated for the record)

* No carrier was fetched; no vendor bytes were downloaded; nothing was written
  under `corpus/`.
* No REA run, no data run, no extractor run.
* No lane file was modified: `tools/`, `plans/`, `corpus/`, `SKILL.md`,
  `PROVINCE.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md` untouched. The two
  candidate SOURCES rows are **drafts** in this seat's directory; the L1
  integrates them (or not) into the freeze.
* No git mutation in the lane or the fleet repo; the only clone made was a
  `--shared` read-only scratch clone used to validate the candidate rows, and
  it lives in scratch.
* The `mknod(2)` and `capabilities(7)` bodies are kept as wave evidence in
  this seat's own directory (`ScoutMknod/receipts/bodies/`), not under
  `corpus/evidence/`. Both re-fetched byte-identically. If the L1 wants a
  committed snapshot there (the S148 precedent keeps one), it should re-fetch
  and commit its own copy rather than promote a seat's copy.
  `ScoutMknod/receipts/quote-check.py` re-checks all ten quotes against those
  bodies (exit 0, `missing=0`).
