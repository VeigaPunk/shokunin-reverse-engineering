# SOURCES append rows — round 52, wave 1 (seat ScribeSources)

Draft for the L1 to land into `corpus/SOURCES.md`. **Not applied to the lane tree.**

One row: **S252** (man7 `mknod(2)`, the kernel-side CAP_MKNOD ground for the round-52
device-accounting law). `kind docs`, `tier A`, `status mined`, `opened 2026-10-30`,
`recheck on-release`.

## The row

Append as the last row of the `## Registry` table in `corpus/SOURCES.md` (immediately
after the `| S251 |` row at `corpus/SOURCES.md:164`; the table ends before `## Paths` at
`corpus/SOURCES.md:169`).

```markdown
| S252 | mknod(2) — Linux manual page — https://man7.org/linux/man-pages/man2/mknod.2.html | docs | A | the kernel-side privilege gate on Linux for creating a device node: the call fails with EPERM when the caller is unprivileged for lack of CAP_MKNOD; regular files, FIFOs and UNIX domain sockets are excluded from that requirement, so this row is not a claim about FIFO or socket creation, nor about symlink handling, nor about the absence of REA gap records, nor about any extractor's own mknod use, nor a measurement of this lane's host capabilities | `ERRORS` section, `EPERM` entry: "other than a regular file, FIFO (named pipe), or UNIX domain socket, and the caller is not privileged (Linux: does not have the CAP_MKNOD capability)"; Linux man-pages 6.19, 2026-02-11 (HTML rendering 2026-09-09); accessed 2026-10-30 HTTP 200, 16,407 bytes, sha256 `f867026fdb9bd5659971c912b68d6745666211495aafefee9c0645b3923ba5f7` | Device-node creation by an unprivileged caller is refused with EPERM for lack of CAP_MKNOD, so a device's absence from an extraction tree can be a privilege refusal rather than a reader gap | mined | 2026-10-30 | on-release | corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md |
```

Eleven columns; no `|` inside any cell; longest cell 379 chars (the `scope` cell), against
a registry whose own longest cell is ~1200. `opened` is `2026-10-30`, which is inside the
round-52 counter v2's `OPENED_DATES = ('2026-10-30',)`
(`.ufo/waves/round-52/w1/ExecCounterV2/c1-counter.py:394`), and `used-by` names the
round-52 entry path, so the counter's `sourced` binding (`c1-counter.py:2469`) can pass
without a change to the counter.

### Id space

The lane registry ends at **S251** (158 rows); `S252` is free and is the id the round-52
claims file reserves for this source (`plans/round-52-claims.md`, `## Frontier step`:
"C1's entry cites the round-52 SOURCES row S252"). The merge package
`/home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md` stages ids `S106`-`S237`
(132 rows) and contains **no** `S252` — no id collision with the package (checked by
grep over the whole merge tree, read-only).

## `## Gate` block fields

The lesson's `## Gate` record (integrated by the L1 into `corpus/lessons/round-52.md`):

| field | value |
|---|---|
| URL | https://man7.org/linux/man-pages/man2/mknod.2.html |
| access date | 2026-10-30 (HTTP 200, 16,407 bytes, sha256 `f867026fdb9bd5659971c912b68d6745666211495aafefee9c0645b3923ba5f7`) |
| located quote (25 words) | "other than a regular file, FIFO (named pipe), or UNIX domain socket, and the caller is not privileged (Linux: does not have the CAP_MKNOD capability)" |
| location of the quote | `ERRORS` section (`<h2 id="ERRORS">`, served HTML line 148), `EPERM` entry, served HTML lines 188-192; the `CAP_MKNOD` token itself is on line 191 |
| decision | **admit** (tier A, `mined`): the page documents the kernel-side privilege gate directly and distinguishes device creation from FIFO/socket creation, which is exactly the distinction the round-52 law rests on (S250 is the producer-side counterpart). |

The quote is 25 words (limit is 25) and was located mechanically, not by eye:
`python3 -I -B quote-check.py` -> `QUOTE_CHECK located=1 missing=0`, **exit 0**
(`quote-check.py`, run against the served bytes saved at `body/mknod.2.html`). The checker
was shown able to fail: with the body mutated `CAP_MKNOD` -> `CAP_MKNODX` it prints
`located_in_flattened_text=False` and exits **1**; restored, it exits **0** again with
the sha256 back at `f867026fdb9bd5659971c912b68d6745666211495aafefee9c0645b3923ba5f7`.
Three negative controls (a dropped "the", a claim that FIFOs are privileged, a
`not root` attribution) are asserted absent.

**The page did not move.** HTTP 200 on two independent fetches three minutes apart
(10:45:48Z and 10:48:47Z), byte-identical (`cmp -s` exit 0), same sha256. The served
page is the man-pages 6.19 rendering (`Linux man-pages 6.19  2026-02-11`, HTML rendered
2026-09-09). No `Set-Cookie` header was present in the response (`grep -ci set-cookie`
= 0), so no cookie or token was captured or stored.

## Census validation (offline, in scratch)

`sources-census.sh validate --file <mirror> --today 2026-10-30` over a scratch mirror of
the registry (`body/SOURCES.mirror-with-S252.md`, the lane's `corpus/SOURCES.md` plus this
one row), three arms:

| arm | registry | entry file | exit | findings | S252 finding |
|---|---|---|---|---|---|
| BASE | without S252 | placeholder present | 1 | 273 | (row absent) |
| WITH | with S252 | placeholder present | 1 | 273 | **none** |
| NEG | with S252 | **absent** | 1 | 274 | `E11 S252 missing used-by corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md` |

`WITH` minus `BASE` is empty — S252 introduces **no** new census finding, no W04
duplicate-URL warning (the man7 URL is new to the registry), and no E-code. The `NEG` arm
shows the row's used-by binding is **able to fail**: with the round-52 entry file absent
the census raises E11 on S252, so the row cannot pass vacuously. The pre-existing
273 findings are the lane's own long-standing E11 set (the mirror has no `corpus/lessons/`
or `corpus/knowledge/` tree, so every historical used-by path is dangling in the mirror) —
they are identical in all three arms and are **not** caused by this row.

The entry placeholder used above is a scratch stub, **not** the landed entry: the real
`corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md` does not exist in the lane yet
(`ls` at 2026-10-30T10:47Z: "No such file or directory"). It is the L1's landing
commit that must create it, together with this row, or E11 fires on the landed registry.

## `## Search log` entry

Append as the last bullet of the `## Search log` section in `corpus/SOURCES.md` (before
`## Leads (unopened)`):

```markdown
- 2026-10-30 round 52 wave 1 (C1 source open) — Question: does the kernel-side privilege gate for device-node creation come with a citable primary source that separates device creation from FIFO/socket creation? Where searched: the man7 `mknod(2)` page (https://man7.org/linux/man-pages/man2/mknod.2.html) fetched twice at 10:45:48Z and 10:48:47Z, HTTP 200 both times, 16,407 bytes each, byte-identical, sha256 `f867026fdb9bd5659971c912b68d6745666211495aafefee9c0645b3923ba5f7`; the served page is the man-pages 6.19 rendering (2026-02-11, HTML rendered 2026-09-09). Identified 1 source candidate, screened 1, included 1 (S252), excluded 0. The `ERRORS` > `EPERM` entry states the CAP_MKNOD gate and excludes regular files, FIFOs and UNIX domain sockets from that requirement, which grounds the round-52 law's device-only boundary (S250 is the producer-side counterpart); no fifo, socket or block-device row exists in any measured carrier, so the FIFO/socket half of the exclusion is documentation-ground only. Stop: the named source question is answered; no vendor carrier fetched, no extraction performed, no REA run. Census: `validate --file` over a scratch mirror exits 1 in every arm with the pre-existing lane E11 set unchanged; S252 adds no new finding and raises E11 when the round-52 entry file is absent.
```

## Scope limits carried by the row

- The row is **documentation of the kernel's documented error condition**, not a
  measurement of this lane's host. The sibling seat `LB4Mknod` probed the host and
  reported the three probes (mkfifo, char-device `os.mknod(0:0)`, AF_UNIX bind) all
  returning 0 in the initial context, i.e. the char-device call did **not** raise EPERM
  there and the unprivileged trial was never measured (`runuser` refused). That seat
  correctly states its own result is not evidence for S252's branch. The row's `scope`
  cell says so explicitly ("nor a measurement of this lane's host capabilities").
- The row documents the **kernel gate**, not the extractor's behaviour. S250 (the
  squashfs-tools 4.7.5 `root_process` gate) remains the producer-side half.
- **Per the `ConnSources` boundary: CAP_MKNOD ground alone cannot establish FIFO
  omission, symlink behaviour, or the absence of REA gap records.** The `scope` cell
  therefore excludes all four explicitly ("not a claim about FIFO or socket creation,
  nor about symlink handling, nor about the absence of REA gap records, nor about any
  extractor's own mknod use"). The extractor implementation and the envelope projection
  each need separate evidence; S252 is only the kernel-side permission requirement.
- Per the `ConnSources` boundary, CAP_MKNOD ground alone cannot establish FIFO
  omission, symlink behaviour, or the absence of REA gap records: the `scope` cell
  excludes all of those explicitly, plus any extractor's own `mknod` use. The extractor
  implementation (S250) and the envelope projection need separate evidence.
- The claim's device-law scope is "unprivileged device-node creation is CAP_MKNOD-gated
  on Linux". The page's EPERM text is broader than char/block devices in one direction
  (it also fires when the filesystem does not support the requested node type) and
  narrower in another (it excludes regular files, FIFOs and UNIX domain sockets). The
  row's `scope` cell states both directions so the row cannot be read as licensing a
  FIFO/socket inference.

## Out of scope for this seat

- No vendor firmware downloaded, no carrier fetched, no extraction, no REA invocation.
- No mutation of the lane tree: `corpus/SOURCES.md`, `corpus/lessons/`, `corpus/knowledge/`
  and `plans/` are untouched; the only writes are under
  `.ufo/waves/round-52/w1/ScribeSources/` and `.ufo/waves/round-52/w1/ScribeSources.md`.
- No git/jj mutating command was run in the lane or the fleet repo (only read-only
  `git log` / `ls-tree` reads).
- No tool was installed; no package manager was invoked.
