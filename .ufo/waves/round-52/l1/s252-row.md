# S252 row fields (L1-opened 2026-10-30; lands at the freeze with the entry)

- URL: https://man7.org/linux/man-pages/man2/mknod.2.html
- access: 2026-10-30T10:45:07Z, HTTP 200, 16407 bytes, sha256 f867026fdb9bd5659971c912b68d6745666211495aafefee9c0645b3923ba5f7
- located quote (24 words, ERRORS -> EPERM entry): "mode requested creation of something other than a regular file, FIFO (named pipe), or UNIX domain socket, and the caller is not privileged"
- continuation (not part of the 25-word quote): "(Linux: does not have the CAP_MKNOD capability)"
- teaches: mknod(2) permits unprivileged creation only of regular files, FIFOs and UNIX-domain sockets; device nodes require CAP_MKNOD.

## Registry row (11 columns, lands at the freeze)

| S252 | mknod(2) — Linux man-pages — https://man7.org/linux/man-pages/man2/mknod.2.html | docs | A | unprivileged device-node creation is CAP_MKNOD-gated on Linux; FIFO/socket creation is not | ERRORS, EPERM entry (page sha256 f867026f…, accessed 2026-10-30) | mknod(2) permits unprivileged creation only of regular files, FIFOs and UNIX-domain sockets; devices need CAP_MKNOD | mined | 2026-10-30 | 180d | corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md |

## Gate fields (for corpus/lessons/round-52.md ## Gate)

- URL + access date + 24-word located quote + location (above); opened independently by the L1
  (this file) and second-read by ScoutMknod in the wave (its fetch receipt lives in its seat dir).
- Purpose: R52-C1's kernel-side ground for the device-accounting law — S250 showed the
  unsquashfs branch structure (char/block mknod inside `if(root_process)`, FIFO/socket calls
  outside); S252 supplies why the kernel gate exists (CAP_MKNOD) and that FIFO/socket creation
  is not the privileged case.
