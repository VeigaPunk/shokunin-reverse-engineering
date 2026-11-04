# ScoutSource — round 67, w1

**Question:** does the C1 class rule ("a char-device entry is a device-node inode, not a file
payload, so a regular-file extractor cannot reproduce it") have a primary source, and is a new
`corpus/SOURCES.md` row justified?

## Headline (observed)

The assigned locator **cannot carry the quote**. `https://docs.kernel.org/filesystems/squashfs.html`
served HTTP 200 at 26 045 B, sha256 `10767bbf8b5c49e81d7aafadd84b6e06602c19641d7f7ae9b0a0258d81733685`
(2026-11-04T00:55:58Z), and contains **zero** occurrences of `Basic device inode`,
`Extended device inode`, `major`, `minor` or `Basic`. Its `extended` occurrences (2 lines) are about
regular-file and directory inodes only; its section list has no device-inode subsection. The page
cannot ground major/minor or payload absence. Per the seat rule, that is a **rejection, not a
paraphrase**.

The wording the seat expected is squashfs-tools-ng's format description, whose real heading is
`=== Device Special Files` — not "Basic device inode". Found and pinned:

- `doc/format.adoc` at commit `e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90` (2024-03-23),
  HTTP 200, 41 981 B, sha256 `08c38b69a9fda3d1a7ce9784132a75cb8c8d65f290e2747af74ab58ae50c82eb`;
  pinned bytes `cmp`-identical to `master` bytes, so neither is a stale rendering.
- Heading at fetched-bytes line **730**; quote at line **732**, 13 words, occurring **exactly once**
  (byte offset 28 445):

  > Basic device special files only store a hard-link counter and a device number.

- Same section, lines 733 and 742–746, state the layout is "identical for both character and block
  devices" and give the Linux `major = (dev & 0xFFF00) >> 8` / `minor = (dev & 0x000FF) | ((dev >> 12) & 0xFFF00)`
  extraction. Type codes `Basic Character Device` 5 and `Extended Character Device` 12 sit at
  `=== Common Inode Header` lines 549/556, distinct from `Basic File` 2.

Together: the entry is a device special file inode storing a link count and a device number — no
block list, no payload — which is exactly the class rule. Classified **[INFERENCE]-free** for the
layout statement; the step from "entry type has no payload field" to "a regular-file extractor
cannot reproduce it" is an inference the rule already makes explicitly.

## Registry (observed)

- `grep -c 'kernel\.org' corpus/SOURCES.md` → **0**. No kernel.org row exists, so the assigned page
  is neither registered nor a near duplicate.
- `grep -n 'format.adoc\|Device Special Files\|special files\|docs.kernel.org' corpus/SOURCES.md`
  → no match. No `squashfs-tools-ng` / `tools-ng` / `AgentD` row either.
- Last registered id: **S267** (`grep -o '^| S[0-9]*' … | tail -5`). Next free: S268.
- Nearest rows and why they are not duplicates: **S250** (device-creation privilege refusal in
  `unsquashfs.c` — extractor behaviour), **S108/S112/S245** (unblob handler argv), **S114/S124**
  (AVM-BE marker and reader patch). None states the device-inode field set.
- `CORPUS.md` `### Rules` item 2 is **Append-only**, not a duplicate rule; with no row to supersede,
  one new row is the sanctioned move.

## Proposed row (proposal, not appended)

`S268`, `docs`, tier `A`, scope = SquashFS v4 device special file inode layout (basic + extended)
and its major/minor encoding; anchor = `=== Device Special Files` line 730 / quote line 732 /
companions 742–746 / type codes 549, 556 / commit + sha256 + size + access; teaches = "A SquashFS
character- or block-device entry is a device special file inode that stores only a hard-link
counter and a device number, so it carries no file payload for a regular-file extractor to
reproduce."; status `queued`, opened `2026-11-03`, recheck `180d`, used-by
`corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md` (the entry file does not exist yet).
Full paste-ready line and per-cell basis: `row.md`. Evidence: `gate.md`, `fetch.json`.

## What this changes for R67-C1 prose

- Cite the class rule to `doc/format.adoc` §Device Special Files, **not** to the kernel docs page.
  A C1 sentence that attributes major/minor or "no payload" to kernel.org would be unsupported by
  the bytes that page serves.
- The kernel page is usable only for the weaker, rendered-HTML statement that SquashFS defines
  different inodes per file type including device — manual-gradeable at best (QUALITY #17), and not
  worth a row while the format.adoc row covers the rule.
- Tier `A` rests on "producing implementation's own format spec". A reviewer who reserves A for
  kernel/vendor texts should record a demotion explicitly rather than editing the row silently.

## Remaining unknowns

- **No carrier evidence here.** Nothing in this seat shows that the twelve round-50 `char-device`
  entries are type-5/type-12 device inodes; that is the L1 data run's and REA's gap records' job.
  The row binds the format rule only.
- `format.adoc` is a second implementation's spec, not `fs/squashfs/squashfs_fs.h`. It states the
  layout directly; it does not prove kernel conformance, and this seat did not open the kernel
  header.
- Branch drift: only the `e3dcf177…` URL is safe; `master` matches today but may not later.

## Housekeeping

Fetched bodies were first written to `/fast/scratch/hyaku/kaidoku-r67/ScoutSource` (now deleted);
the two bodies that the gate needs are retained beside it as `fetched-squashfs-docs.html` and
`fetched-format.adoc` so every probe re-runs offline. No tool installs. No writes outside
`.ufo/waves/round-67/w1/ScoutSource/`. Frozen inputs read only.
