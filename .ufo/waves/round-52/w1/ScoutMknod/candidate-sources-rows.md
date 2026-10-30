# Candidate SOURCES rows — round 52 (draft for the L1's freeze)

Both rows were validated with the lane's own census tool against a scratch
clone of the claims-draft base (`ab0eafedc41402b43b41a4362084119578dfe7ce`),
with the round-52 knowledge entry present as a placeholder file:

```
bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root <scratch> <scratch-clone>
→ clone  ok  <scratch>/clone/corpus/SOURCES.md
   exit 0
```

Negative control (the same two rows with the knowledge entry removed):

```
→ clone  E11  S252 missing used-by corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md
→ clone  E11  S253 missing used-by corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md
   exit 1
```

So both rows are structurally valid, and their `used-by` target must exist on
disk before the census can pass — the L1's landing bindings already require
`corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md`, so the landing order
must place that file in or before the freeze commit.

**Id space.** The lane registry ends at S251 (`corpus/SOURCES.md`, 158 rows).
The merge package's 132 staged rows span S106–S237 and contain no S252/S253, so
S252/S253 continue the lane's S-space with no collision. The claims draft
already names "the round-52 SOURCES row S252 (man7 `mknod(2)`, opened this round
by the L1 and a scout)" — this seat's independent read confirms that id and
supplies the located quote; S253 is the free id for capabilities(7).

---

## S252 — mknod(2) (the row the claims draft already names)

```
| S252 | mknod(2), Linux man-pages 6.19 — https://man7.org/linux/man-pages/man2/mknod.2.html | docs | A | the kernel's device-node creation privilege gate only; not FIFO/socket creation, not the extractor's gap records, not an LE-carrier measurement | `ERRORS` → `EPERM`: "mode requested creation of something other than a regular file, FIFO (named pipe), or UNIX domain socket, and the caller is not privileged" (23 words); man-pages 6.19, 2026-02-11; HTML rendering 2026-09-09; fetched 2026-10-30 HTTP 200, 16,407 bytes, sha256 `f867026fdb9bd5659971c912b68d6745666211495aafefee9c0645b3923ba5f7` | Grounding for a device-only privilege gate: the kernel refuses device-node creation without CAP_MKNOD, and the same sentence exempts regular files, FIFOs and UNIX domain sockets from that gate | mined | 2026-10-30 | on-release | corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md |
```

Field notes for the L1:
- **kind** `docs`, **tier** `A`: the kernel's own documented syscall contract
  (same shape as S148, the lane's existing man-pages row).
- **scope** must say "device-node creation privilege gate only" — this page does
  not decide which kinds the extractor materialises, does not speak to REA gap
  records, and does not measure any carrier.
- **teaches** should carry the exemption explicitly, because the exemption is
  the load-bearing half: the privileged class is the device-special-file class
  and nothing else.
- **recheck** `on-release`: man-pages is a moving release stream; the page
  version (6.19) and the HTML rendering date (2026-09-09) are both recorded so
  a future re-open can detect drift.
- No `Set-Cookie` header was present on either fetch; no cookie or token was
  copied into any receipt.

## S253 — capabilities(7) (candidate; admissible, but narrower than S252)

```
| S253 | capabilities(7), Linux man-pages 6.19 — https://man7.org/linux/man-pages/man7/capabilities.7.html | docs | A | the kernel capability set's own definition and availability rule for CAP_MKNOD only; not which file kinds the gate covers, not FIFO/socket creation, not the extractor's gap records | `DESCRIPTION` → `Capabilities list`: "CAP_MKNOD (since Linux 2.4) Create special files using mknod(2)." (9 words); man-pages 6.19, 2026-02-08; HTML rendering 2026-09-09; fetched 2026-10-30 HTTP 200, 83,601 bytes, sha256 `79ca88f6d8984ca2858860e7267d7c4660f6555151cc1f570305a9c6dfccf714` | Names the capability the device gate depends on and dates it, but its scope word "special files" is broader than device nodes and cannot itself carry a device-only rule | mined | 2026-10-30 | on-release | corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md |
```

Field notes for the L1:
- **scope** must be worded to say this row does **not** decide which file kinds
  the gate covers. That is the whole risk in admitting it: capabilities(7)'s
  one-line scope is "special files", which on that page's taxonomy is broader
  than device nodes. If the row's scope cell left that open, a later reader
  could cite S253 for a device-only rule it cannot support — the same
  unsupported generalisation the round-51 closure rejected (M51-3).
- **What it genuinely adds beyond mknod(2) alone:** (a) the capability's
  canonical inventory entry and its date ("since Linux 2.4"); (b) the
  availability rule — "If the filesystem user ID is changed from 0 to nonzero
  … CAP_MKNOD (since Linux 2.6.30)" is cleared from the effective set — which
  mknod(2) does not state and which is what makes "an unprivileged extraction
  cannot create a device node" a statement about the effective capability set
  rather than about uid 0 alone.
- **Where it is weaker:** it cannot carry the per-kind split. The device-only
  scope must be cited to **S252** (mknod(2) `ERRORS`/`EPERM`) and **S250**
  (unsquashfs 4.7.5 branch placement), never to S253.
- **Recommendation:** admit S253 as a second independent reader of the
  capability, scoped as above. If the L1 prefers a single row for the kernel
  side, S252 alone is sufficient for the law's device-only scope and S253 may be
  dropped — the claim does not depend on it. If S253 is admitted, the landing
  bindings' "the round-52 SOURCES row(s) opened this round" wording covers it;
  no binding text needs to change.

---

## Where the two rows may be cited

| rule clause / binding | citable row | not citable from |
|---|---|---|
| "the kernel-side gate is CAP_MKNOD on device files" | S252 (`ERRORS`/`EPERM`), with S250 for the extractor-side branch placement | S253 alone |
| "FIFO and UNIX-domain socket creation are not privileged" | S252 `ERRORS`/`EPERM` (the exemption clause), S250 `:1328`/`:1349` | S253 |
| "the capability is absent from an unprivileged process" | S252, strengthened by S253's fsuid rule | — |
| "the extractor creates no device nodes" | S250 (branch placement) + the law's own derivation; S252 bounds the privilege claim | S252 or S253 alone (neither observes the extractor) |

Note the last row: neither man page observes the extractor or any carrier. The
law's device-accounting statement needs the source ground (S250, S252) plus the
measured corpus; no man page can carry the measurement.
