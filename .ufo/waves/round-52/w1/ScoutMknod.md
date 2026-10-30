# ScoutMknod — round 52 wave 1 seat report

**Seat:** ScoutMknod (scout, leaf member — no subagents dispatched)
**Lane root:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
**Round base:** `c525de54a53eb3c4fee28ede2721da4527cf8ece`; claims draft `ab0eafedc41402b43b41a4362084119578dfe7ce`
**Scratch:** `/fast/scratch/hyaku/kaidoku-r52/w1-ScoutMknod` (removed after copying receipts into the seat dir)
**Verdict:** settled — the kernel-side ground the claims draft names (S252) exists and says what the claim says it says; a capabilities(7) row (S253) is admissible but narrower.

## 1. What was fetched (receipts in `ScoutMknod/receipts/`)

Both URLs named by the seat spec, fetched 2026-10-30, HTTP 200, each body re-fetched and confirmed byte-identical:

| page | bytes | body sha256 | page version |
|---|---|---|---|
| `https://man7.org/linux/man-pages/man2/mknod.2.html` | 16,407 | `f867026fdb9bd5659971c912b68d6745666211495aafefee9c0645b3923ba5f7` | man-pages 6.19, 2026-02-11; HTML rendering 2026-09-09 |
| `https://man7.org/linux/man-pages/man7/capabilities.7.html` | 83,601 | `79ca88f6d8984ca2858860e7267d7c4660f6555151cc1f570305a9c6dfccf714` | man-pages 6.19, 2026-02-08; HTML rendering 2026-09-09 |

Exact commands, curl exit codes, stdout sha256 and UTC times are in
`receipts/fetch-receipts.json`. No `Set-Cookie` header was present on either
response (grep count 0); no cookie or token was copied into any receipt. No
vendor bytes were downloaded; nothing was written under `corpus/`.

## 2. The three located quotes

**(1) The EPERM sentence about device files and CAP_MKNOD** — `ERRORS` → `EPERM`, mknod(2):

> "mode requested creation of something other than a regular file, FIFO (named pipe), or UNIX domain socket, and the caller is not privileged"  *(23 words)*
> "the caller is not privileged (Linux: does not have the CAP_MKNOD capability)"  *(12 words)*

**(2) Do FIFO and UNIX-domain socket creation need privileges per this page?**
**No.** The same `EPERM` entry exempts exactly those two kinds — the privileged
class is the device-special-file class and nothing else. Verbatim ERRORS text:

> "EPERM  *mode* requested creation of something other than a regular file, FIFO (named pipe), or UNIX domain socket, and the caller is not privileged (Linux: does not have the **CAP_MKNOD** capability); also returned if the filesystem containing *path* does not support the type of node requested."

**(3) The CAP_MKNOD definition line** — capabilities(7), `DESCRIPTION` → `Capabilities list`:

> "CAP_MKNOD (since Linux 2.4) Create special files using mknod(2)."  *(9 words)*

All ten quotes were matched verbatim against the tag-stripped fetched bodies
(`receipts/quote-check.json`, every `verbatim_present_in_page: true`); the
sixth corroborating quote is capabilities(7)'s fsuid rule, "CAP_MKNOD (since
Linux 2.6.30)", under `Effect of user ID changes on capabilities`.

## 3. Does capabilities(7) add ground beyond mknod(2) alone?

**Partly, and the added part is narrower.** It adds the capability's canonical
inventory entry and date, plus the availability rule mknod(2) does not state:
`CAP_MKNOD` (since Linux 2.6.30) is cleared from the effective set when the
filesystem UID goes 0 → nonzero. That is what makes "an unprivileged extraction
cannot create a device node" a statement about the *effective capability set*
rather than about uid 0 alone.

It does **not** add the per-kind split: its scope word is "special files",
broader than device nodes on that page's own taxonomy. Citing capabilities(7)
for a device-only rule would be an unsupported generalisation of the same
family as the round-51 rejection (M51-3). Recommendation in
`candidate-sources-rows.md`: admit S253 scoped to say it does not decide which
kinds are gated; every device-only citation points at S252 (+ S250 for the
extractor side). The claim does not depend on S253 — S252 alone suffices.

## 4. Two findings the L1 should carry into the freeze

**(a) The kernel side and the tool side now agree in kind.** The kernel's
partition is device-only; the lane's S250 (`unsquashfs.c` 4.7.5, re-read
first-hand this seat from the committed round-51 snapshot, body sha256
`6222d940c45537d597e2b36d1d46abbc90f0863e7106bab8fa7bdd97fd939341`) gates
`if(root_process)` (`:1287`) around the device `mknod` (`:1296`) with the FIFO
call (`:1328`) and the socket call (`:1349`) outside it. The round-51 closure
had only the tool side; the law's per-kind split now has an independent kernel
reader.

**(b) The fifo/socket clause must be a *width* statement, not a *privilege*
statement.** The kernel ground refutes "the extractor could not have made a
fifo/socket" as a reason. The corpus fact is that the four committed oracle
non-regular tables contain **no** fifo, socket or block-device row — verified:
kinds present across all four tables are only `char-device` (28 rows: 1, 1, 13,
13 for c6430, c6490, g7581, g7582), `dir` and `symlink`; rows with kind
`fifo`/`socket`/`block-device`/`device` = 0. So `allowed` for those kinds must
be justified by corpus width and fail closed on a future carrier that does
contain one, while the device clause may rest on the privilege reason.

**(c) Wording hazard, cheap to fix now.** mknod(2)'s `EPERM` has a second
cause: it is "also returned if the filesystem containing path does not support
the type of node requested". An EPERM is therefore not by itself evidence of an
unprivileged caller. Any `gap-rule.json` / counter clause that infers
"unprivileged" from a creation failure must not read the errno alone.

## 5. Candidate SOURCES rows (drafts; the L1 integrates or drops)

Full field-by-field draft with the validation receipts in
`candidate-sources-rows.md`. Both rows validated with the lane's own census
tool against a scratch clone of the claims-draft base: exit 0 with the
round-52 knowledge entry present; exit 1 with it removed (`E11` on S252/S253)
— so the landing must place `corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md`
in or before the freeze commit. Id space: the lane registry ends at S251; the
merge package's 132 staged rows span S106–S237 and contain no S252/S253, so
S252/S253 continue the lane's S-space with no collision. S252 is the id the
claims draft already names for mknod(2).

## 6. Not done, stated plainly

No carrier fetched; no vendor bytes downloaded; no REA run, no data run, no
extractor run; nothing written under `corpus/`, `tools/`, `plans/` or any lane
doc; no git or jj mutation in the lane or the fleet repo (the only clone is a
read-only `--shared` scratch clone used to validate the candidate rows). The
two man-page bodies are kept as wave evidence in this seat's own directory
(`ScoutMknod/receipts/bodies/`, sha256 as in the receipts) and are **not**
placed under `corpus/evidence/` — if the L1 wants a committed snapshot there
(S148 precedent), it should re-fetch and commit its own copy rather than
promote a seat's copy. `ScoutMknod/receipts/quote-check.py` re-checks all ten
quotes against those bodies (exit 0, `missing=0` as delivered).

**Tools installed/updated:** none. `/home/vgpnk/.omp/agent/RULES.md` was read;
no install was needed for this task.

**Seat directory:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScoutMknod/`
