# ScoutMksquashfs — round 51, wave 1 (build) — the mksquashfs padding source (R51-C2 grounding)

**Verdict: the source opens, but the claims file's flag name is wrong and the premise it would support is false.**
The option is **`-nopad`** (one token). `-no-pad` does not exist: `mksquashfs: -no-pad is an invalid option`, exit 1.
And the padding state is **independent** of whether a reader accepts the body — so it cannot be the discriminator
R51-C2's failed-body route fix needs.

Deliverables (all under `.ufo/waves/round-51/w1/ScoutMksquashfs/`):
`receipts/fetch-receipt.json`, `receipts/probe-receipt.json`, `quotes.md`, `sources-row-fields.md`, `probe/` (3 scripts + 7 captured outputs).
Scratch `/fast/scratch/hyaku/kaidoku-r51/w1-ScoutMksquashfs` removed after copying.

---

## 1. The source (fetched, pinned)

`https://raw.githubusercontent.com/plougher/squashfs-tools/master/squashfs-tools/mksquashfs.c`
HTTP **200**, **266,790 B**, sha256 `205f58e6394844317b58266ca351966e222a2cc49657c7cc68365030d4a2bc5c`,
byte-identical across **3** fetches (04:57:26Z, 05:09:13Z), etag `f67f5d05…5fe5bd5502`,
upstream master HEAD `db038ef265ed00bb17aaf695a72f9b0c3489eb20` (`git ls-remote`, read-only).
No `Set-Cookie` header captured or stored. The fetched file is scratch-only and is **not** copied into the lane tree.

**Located (all quotes ≤25 words; full list in `quotes.md`):**

| ref | quote |
|---|---|
| `:205` | `int nopad = FALSE;` (comment at `:204`: "Will Mksquashfs pad the filesystem to a multiple of 4 Kbytes?") |
| `:8501-8502` | `} else if(strcmp(argv[i], "-nopad") == 0)` → `nopad = TRUE;` (sqfstar twin at `:7362-7363`) |
| `:571-573` | `/* If necessary: truncate output destination to filesystem end / pad to 4Kbyte multiple */` |
| `:577` | `int tail = end & (4096 - 1);` |
| `:588-590` | `if(!nopad && tail) { … write_destination(fd, get_dpos(), 4096 - tail, temp); }` |
| `:6262` | `block = nopad ? get_dpos() : (get_dpos() + 4095) & ~4095;` (streaming superblock offset) |

**What the padding actually is** — a **zero-fill of the output file's tail up to the next 4096-byte multiple**
(`4096 - tail` zero bytes written at `get_dpos()`), plus, in streaming mode only, a 4096-aligned superblock offset.
It is a **producer-side image-length** property, not a filesystem-content property.

**The rationale is NOT in the source.** Full-file grep of the fetched 266,790 B for `loopback`, `bootimage`,
`multiple of 4K`, `pad to a multiple` yields only `:204`, `:573` and the code sites. The "why" is in the **shipped man page**
of the installed tool: `/usr/share/doc/squashfs-tools/USAGE-MKSQUASHFS` (squashfs-tools 4.7.5-1, sha256 `b047ffbb…aa26b12e7f`)
`:1431` "The -nopad option informs Mksquashfs to not pad the filesystem to a 4K multiple." · `:1432-1433` "…to enable the output
filesystem file to be mounted by loopback, which requires files to be a 4K multiple." · `:1434-1435` "If the filesystem is being
written to a block device, or is to be stored in a bootimage, the extra pad bytes are not needed."

**The upstream usage string lives elsewhere in master**: `mksquashfs.c:77` `#include "mksquashfs_help.h"`.
The string itself, from the installed tool: `mksquashfs -help-option pad` → `-nopad			do not pad filesystem to a multiple of 4K` (exit 0).

---

## 2. The bounded probe (one input dir → two images)

`mksquashfs`/`unsquashfs` 4.7.5 (2026/03/01), `sasquatch` at `/home/vgpnk/.local/bin/sasquatch`.
Input: `src/a.txt` + `src/sub/b.txt`, all mtimes pinned to `2020-01-01T00:00:00Z`. Script: `probe/probe_final.sh`.

| image | bytes | sha256 | `bytes_used` | `file_size mod 4096` | tail |
|---|---|---|---|---|---|
| `padded` (default) | **4096** | `3e775fb0402e80add75dc67d1203a6a78ddd094de2a41451967e330be6d7e648` | 281 | **0** | 3815 B |
| `nopad` (`-nopad`) | **281** | `f25daa73dee02a01c7894fff9d09e0bd3e64212b649634410d6f0e4830363e5e` | 281 | **281** | 0 |
| `padded2` (control) | 4096 | `3e775fb0…be6d7e648` (identical to `padded`) | 281 | 0 | 3815 B |

- **byte-length difference: 3815** (4096 − 281)
- the no-pad bytes are a **byte-exact prefix** of the padded bytes; the 3815-byte tail is **all zero** (`padded_tail_all_zero True`)
- `bytes_used` is **281 in both** — the pad does not change the filesystem's own length field
- both images extract to an **identical tree** (`TREES_IDENTICAL=yes`; `./a.txt` `5891b5b5…`, `./sub/b.txt` `e258d248…`)
- `unsquashfs -s` exit 0 and `sasquatch -d out` exit 0 on **both** (readers run in isolated cwds — the first attempt
  shared a cwd and produced a spurious rc=1 from a directory collision; corrected, re-run, and both reader logs are in `probe/`)
- **determinism control**: a third padded build 2 s later differs **only** in the superblock `mkfs_time` (offset 8..11:
  `1793336861` vs `1793336723`). An image sha256 is therefore **not** a stable identity across builds — pin the
  `bytes_used`/`file_size` pair, not the whole-file digest.

**The discriminator's observable, stated:** `file_size mod 4096` (and `file_size - bytes_used`),
both derivable from a superblock read plus a file length. On the lane's committed round-42 fixture family the same
image appears at **320 / 1024 / 4096 B** for every family (`squashfs_v3`, `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`,
`squashfs_v3_nonstandard`), so the observable is live on the real corpus — measured, all 24 variant files.

---

## 3. The finding that matters for R51-C2: pad state ≠ reader refusal

`probe/probe_magic.sh`, on the lane's **committed** ddwrt fixtures (read-only):

| fixture | bytes | `unsquashfs -s` | `sasquatch -be` |
|---|---|---|---|
| `squashfs_v3.be.nopad.bin` (320 B) | 320 | **exit 1** | exit 0 |
| `squashfs_v3.be.4kpad.bin` (4096 B) | 4096 | **exit 1** | exit 0 |
| `…nopad` + **one byte** patched `0x74`→`0x73` (magic `tqsh`→`sqsh`) | 320 | **exit 0** | exit 0 |
| `…4kpad` + the same one-byte magic patch | 4096 | **exit 0** | exit 0 |

**The 4096-byte padded image is refused exactly as the 320-byte no-pad one, and a one-byte magic patch makes both
readable.** Pad state and refusal are **independent**; the refusal cause is the **non-standard magic** (`tqsh`/`hsqt`
instead of `sqsh`/`hsqs`).

This is not a new discovery to the lane — its own round-42 reader oracle
(`.ufo/waves/round-42/w1/artifacts/R42C1ImgDdwrt/reader-oracle.txt`, 6× ) already records
"as published: unsquashfs -s rc=1" against "std-magic copy (sqsh): unsquashfs -s rc=0".

**Consequence for the C2 draft:** the failed body `dmg_Z3_v3ddwrt_inode_table` (320 B, sha256 `839c17a8…`) has its
sasquatch stderr *"Non-standard SquashFS Magic: 'tqsh'"* → *"get_metadata: failed to read block"* →
*"FATAL ERROR: read_inode: failed to read inode 144:128"* (decoded from the committed envelope's base64 field). That is an
**inode/metadata read** failure, not a pad failure. A `legacy-body-unreadable` rule keyed on the pad state would be
keyed on the wrong cause.

**Two further scope facts the C2 drafter needs:**
1. The scored envelope **does** expose the body length — `locations[0].end` = 320 / 1024 / 4096 per variant (measured on
   all 14 ddwrt envelopes) — but the triage v5 feature tuple (`OP PV H F HF G D BE SR P commands`) does **not** carry it.
   So a body-variant feature is *addable* to the tuple, contradicting v5's "the scored features do not expose a body variant"
   only if "scored features" means the tuple; it remains true of the tuple as written.
2. The triage v5 premise "a reader is only trusted for the BODY VARIANT it was measured on" needs the **cause** to be
   separated from the **variant**: on this corpus all three ddwrt pad variants behave identically per reader, so
   variant-keyed reader trust buys nothing here.

---

## 4. SOURCES-row fields

`sources-row-fields.md` carries the full row for **S250** (next free id; registry max is S249, 156 rows) in the registry's
column order, plus the Gate record (URL, access date, bytes, sha256, ≤25-word quotes, flip condition), the recommended
disposition of the `-no-pad` name, and the secondary man-page artifact.

**Recommendation to the L1:** register **S250** as `mksquashfs.c` / code / tier A with the **measured** spelling `-nopad`,
and amend the claims-file wording from "`-no-pad`" to "`-nopad`" in the freeze's `## Wave-1 amendment record`.
Do **not** record the hyphenated spelling as a *rejected source* — it is a prompt typo, not a screening decision.

---

## 5. Open gaps (stated, not papered over)

- The **rationale quote** comes from the **host-installed** man page (4.7.5-1), not from a fetched upstream URL; upstream
  master carries no rationale comment at all. If the L1 wants it citable, it needs its own SOURCES row and its own access.
- The upstream master **usage string** was not fetched from `mksquashfs_help.h` (out of my task's named URL scope); the
  string quoted is from the installed 4.7.5 binary's `-help-option`.
- The failed body `Z3_v3ddwrt_inode_table.bin` (sha256 `839c17a8…`) is **not** present in the lane tree. Measured:
  a whole-file sha256 sweep over every lane file ≤1 MB found no match, and a bounded **320-byte carve** sweep over the
  **whole lane tree** (44,830 files, 911,215,363 B read) found no match either — 470 magic-anchored windows hashed, no hit.
  The carve sweep is **positive-control proven**: the same script, pointed at a synthetic file with a planted
  `tqsh`-magic 320-byte window, reports `MATCHES: … offset=500`. The round-42 scratch
  `/fast/scratch/hyaku/kaidoku-r42` no longer exists, so the body is gone.
  Its behaviour was therefore read from the committed envelope's base64 stderr, and the **magic-vs-pad** experiment was
  run on the committed *fixture family* (same 320-byte size, same `tqsh` magic, sha256 `daa8e72d…`), not on the failed
  body itself. That substitution is the one inference in this report.
  (A first carve sweep, hashing every 320-byte window of every file, was killed at the 400 s bound with no output —
  inconclusive; the magic-anchored rewrite above is the one that completed.)
- Not run: any REA invocation, any `--data-run`, any write into `corpus/evidence/`, any lane-tree instrument.
  The lane tree was not modified; `git -C /home/vgpnk/Projects/shokunin status --porcelain` is clean.

## 6. Tooling

No install was needed. `mksquashfs`/`unsquashfs` 4.7.5 and `sasquatch` were already present
(`pacman -Q squashfs-tools` → `squashfs-tools 4.7.5-1`; `sasquatch` at `/home/vgpnk/.local/bin/sasquatch`).
No pacman transaction was run; the pacman guard was honoured.
