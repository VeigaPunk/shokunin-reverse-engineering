# corpus/SOURCES.md rows for round 42 (R42-C1)

Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`, appends only.
Base `c4a38ea2` holds rows `S001`–`S129` (`grep -c '^| S' corpus/SOURCES.md` at base = 129; last row
`S129`, the binwalk v3 README). **Next free id is `S130`.**

Two bindings depend on this file, both in `tools/round-41/c1-extra.py` and its round-42 port:

- `sourced` (counter): the entry's `source:` lines must cite an id whose row has **11 cells**, `opened`
  = `2026-10-26`, and the entry path or stem somewhere in `used-by`.
- `sourced_new` (extra): at least one cited id must be **absent at the base commit** and present at the
  measured revision with the entry in `used-by`. `S112`, `S116`, `S118`, `S119`, `S121` are all present at
  the base, so they can never satisfy it; the new rows must.

**Invariant that survives any renumbering:** `opened` = `2026-10-26`, `used-by` contains
`corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md`, `status` = `mined`, 11 cells, one row per distinct
document. The ids below are the proposal; the L1 (or the source/id seat) may renumber them by append
order. If publisher rows land in a different order, adjust the entry's `source:` lines, not this invariant.

### Rows to append (11 cells each)

```markdown
| S130 | `<<L1:carrier-1-publisher>>` — `<<L1:carrier-1-publisher-url>>` (files `<<L1:carrier-1-published-files>>`) | dataset | A | The publisher's own published identity for carrier 1: product, release name, the image file name(s), the advertised size and any digest the publisher states; not the SquashFS layout of any member, not licence permission to redistribute or reverse engineer, not other releases of the same product | `<<L1:carrier-1-source-anchor>>` | Separates what the publisher claims about the artifact from what the lane measures on its bytes, so a carrier's identity does not rest on a lane inference | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md, corpus/lessons/round-42.md |
| S131 | `<<L1:carrier-2-publisher>>` — `<<L1:carrier-2-publisher-url>>` (files `<<L1:carrier-2-published-files>>`) | dataset | A | The publisher's own published identity for carrier 2 (same scope as S130, different document) | `<<L1:carrier-2-source-anchor>>` | Same as S130, for carrier 2 | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md, corpus/lessons/round-42.md |
| S132 | `<<L1:carrier-3-publisher>>` — `<<L1:carrier-3-publisher-url>>` (files `<<L1:carrier-3-published-files>>`) | dataset | A | The publisher's own published identity for carrier 3 (same scope as S130, different document) | `<<L1:carrier-3-source-anchor>>` | Same as S130, for carrier 3 | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md, corpus/lessons/round-42.md |
| S133 | `<<L1:carrier-4-publisher>>` — `<<L1:carrier-4-publisher-url>>` (files `<<L1:carrier-4-published-files>>`) | dataset | A | The publisher's own published identity for carrier 4 (same scope as S130, different document) | `<<L1:carrier-4-source-anchor>>` | Same as S130, for carrier 4 | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md, corpus/lessons/round-42.md |
| S134 | SquashFS v3 oracle premise on unblob 26.6.4's own v3 fixtures — own-work, `.ufo/waves/round-42/w1/artifacts/R42C1EntryDraft/dev-evidence/dev-input-evidence.txt` (sha256 `5cb5f9b9b480fa966874430569ea04bbdd4cda18136de07817fb72f11d77935d`) | own-work | A | What `unsquashfs` 4.7.5 and 7-Zip 26.04 publish from little- and big-endian SquashFS v3 fixture bodies (identical digests, 2 files each), the plain-`sasquatch` argv unblob 26.6.4 emits for each endianness, and that `unsquashfs` 4.7.5 refuses an LZMA-block v3 body (`gzip uncompress failed with error code -3`, exit 1) while 7-Zip extracts it; not a carrier result, not the producers' own behaviour beyond these fixtures, not a licence statement about the fixtures | fixture pins `squashfs_v3_le.bin` sha256 `0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7`, `squashfs_v3_be.bin` sha256 `4e9493d9c6f868005dea8f11992129c3399e0bcb8f3a966c750cb925989ca97c`, `squashfs_v3_le.lzma.bin` sha256 `2ac15e5c993f330854497b2fd032d2e87873a288fab6da2fe72106bb40b43124`, fetched from `https://media.githubusercontent.com/media/onekey-sec/unblob/refs/tags/26.6.4/tests/integration/filesystem/squashfs/…` on 2026-10-26 | Grounds the oracle pair's v3 leg before any carrier exists: two readers that are not sasquatch agree on gzip v3 in both endiannesses, and the pair has a measured hole on LZMA-block v3 — so a v3 carrier's oracle agreement is a per-carrier measurement, not a property of the format | mined | 2026-10-26 | 180d | corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md |
```

### Why S134 exists even though S130–S133 are also new

`S130`–`S133` are placeholders until the carrier seats pick publishers; `S134` is fully specified by this
seat's own dev-input read and is the row that makes `sourced_new` true regardless of how the publisher
rows are finally worded or ordered. Keep `S134` (or a same-scope row with `opened` = `2026-10-26` and the
entry in `used-by`).

### Collision handling

Other wave-1 seats (`R42Assim*`, `R42ConnSibling`, the C2 entry) also append rows. The registry has no
allocation lock; round-39/40/41 resolved collisions by **renumbering at append time by document order**
and never editing an existing cell. Consequences the L1 must honour:

1. Append order decides ids; the entry's `source:` ids are rewritten to the final numbers in the same
   commit that adds the rows (a dangling `S13x` in the entry is a `sourced` failure).
2. `S134`'s fixture pins and the own-work path must stay in the row; they are the only non-placeholder
   content in this block and the row's whole value.
3. The `used-by` cell is compared by **substring** against the entry path or stem (round-41 F3), so a
   renamed entry silently breaks the binding — rename the entry only together with every `used-by` cell.
