# Proposed SOURCES row — ScoutSource (round 67, w1)

Status: **proposal only.** Registry last id is S267 (`grep -o '^| S[0-9]*' corpus/SOURCES.md | tail -5` →
S263…S267), so S268 is the next free id; renumber at append time if another seat lands first.
The row is written against the **substitute** locator, because the assigned
`docs.kernel.org` page does not contain the quote (see `gate.md` §1 — rejection).

## Paste-ready row (registry column order)

```
| S268 | squashfs-tools-ng SquashFS format documentation, `doc/format.adoc` at commit e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90 — https://raw.githubusercontent.com/AgentD/squashfs-tools-ng/e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90/doc/format.adoc | docs | A | The SquashFS v4 on-disk layout of device special file inodes (basic and extended): what a device entry stores and the Linux major/minor encoding of its device number; not any carrier, not extraction outcomes, not the mknod privilege gate (S250) | `=== Device Special Files` (heading, fetched-bytes line 730), line 732; companion major/minor lines 742-746; type codes `Basic Character Device` 5 / `Extended Character Device` 12 at `=== Common Inode Header` lines 549, 556; commit e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90, sha256 08c38b69a9fda3d1a7ce9784132a75cb8c8d65f290e2747af74ab58ae50c82eb, 41,981 B, HTTP 200 2026-11-03 | A SquashFS character- or block-device entry is a device special file inode that stores only a hard-link counter and a device number, so it carries no file payload for a regular-file extractor to reproduce. | queued | 2026-11-03 | 180d | corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md |
```

## Cells, field by field

| field | value | basis |
|---|---|---|
| id | `S268` (next free; last registered S267) | `grep -o '^\| S[0-9]*' corpus/SOURCES.md \| tail -5` |
| source | squashfs-tools-ng SquashFS format documentation, `doc/format.adoc` at commit `e3dcf177…` — pinned raw URL | fetched HTTP 200, 41 981 B, sha256 `08c38b69…`; pinned bytes `cmp`-identical to `master` bytes |
| kind | `docs` | it is a format description, not code and not a dataset |
| tier | `A` | primary/authoritative for the format it describes: the producing implementation's own on-disk specification; the quoted sentence states the device-inode field set directly. If the lane reads tier A as kernel/vendor-only, demote to B rather than widen the scope |
| scope | device special file inode layout (basic + extended), device-number major/minor encoding, type codes | lines 730–747 and 549/556; nothing about carriers or extraction |
| anchor | `=== Device Special Files`, line 730; quote line 732; companions 742–746; type codes 549/556; commit + sha256 + size + access | contiguity proved: quote occurs exactly once, byte offset 28 445 |
| teaches | one sentence, 34 words, grounded in 732–733 | see below |
| status | `queued` | row proposed, not yet relied on by a published entry |
| opened | `2026-11-03` | lane-local date; HTTP `Date` was `2026-11-04T00:55:58Z` |
| recheck | `180d` | seat spec |
| used-by | `corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md` | planned entry path; file does not exist yet (`ls` → No such file or directory) |

## Quote discipline

Submitted quote, verbatim, 13 words, fetched-bytes line 732:

> Basic device special files only store a hard-link counter and a device number.

- Byte string `Basic device special files only store a hard-link counter and a device number.`
  occurs **1×** in the pinned file (byte offset 28 445, line 732).
- Heading containing it: `=== Device Special Files` (line 730), i.e. the nearest preceding heading —
  matches QUALITY #91(i).
- It is single-line plain prose (AsciiDoc paragraph), no markup inside the quote, so it is not
  caught by the QUALITY #17 rendered-markup exclusion.

## Rejected locator (do not append)

`https://docs.kernel.org/filesystems/squashfs.html` — HTTP 200, 26 045 B, sha256 `10767bbf…`, but
**0** occurrences of `Basic device inode`, `Extended device inode`, `major`, `minor`, `Basic`,
`Extended`. Its only device sentences (raw bytes 264–266, 412–414) are rendered HTML, state no
major/minor and no payload rule, and would force either an over-wide `teaches` or a paraphrase.
Registering it would put a row on the registry whose anchor cannot carry its own claim.

## Duplicate check

- `grep -c 'kernel\.org' corpus/SOURCES.md` → `0`: the assigned page is not any existing row.
- `grep -n 'format.adoc\|Device Special Files\|special files\|docs.kernel.org' corpus/SOURCES.md`
  → no match: the proposed locator is not an existing row.
- No row in the registry cites `squashfs-tools-ng` / `tools-ng` / `AgentD`.
- Adjacent but distinct: S250 (device-creation privilege refusal in `unsquashfs.c` — extractor
  behaviour), S108/S112/S245 (unblob handler argv), S114/S124 (AVM-BE marker and reader patch).
  Different locators, different scopes; none states the device-inode field set.
- `CORPUS.md` `### Rules` item 2 is **Append-only**, not a duplicate rule: adding one new row is the
  sanctioned move; there is no row here to supersede.

## Risks the L1 should weigh

1. **Locator substitution is the point of this seat.** If the round insists the class rule's source
   be the kernel docs page, the rule has no quotable grounding and the C1 prose must be reworded —
   the honest wording would be "SquashFS distinguishes device inodes from regular-file inodes"
   (kernel page, rendered HTML) rather than anything about major/minor or payload absence.
2. **Tier call.** `A` rests on "producing implementation's own format spec". A reviewer who reserves
   A for kernel/vendor texts should record the demotion explicitly rather than silently editing it.
3. **Branch drift.** Only the commit-pinned URL is safe; `master` currently matches, but the row's
   URL must stay the `e3dcf177…` form.
