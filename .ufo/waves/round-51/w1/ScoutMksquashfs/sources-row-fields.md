# SOURCES-row fields — the squashfs-tools padding source (round 51, R51-C2 grounding)

Proposed row **S250** (next free id: the registry's highest is S249; `grep -c '^| S[0-9]*' corpus/SOURCES.md` = 156 rows).
Fields are given in the registry's column order: `id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by`.

---

## S250 (proposed)

| field | value |
|---|---|
| **id** | S250 |
| **source** | squashfs-tools `mksquashfs.c`, upstream master — https://raw.githubusercontent.com/plougher/squashfs-tools/master/squashfs-tools/mksquashfs.c |
| **kind** | code |
| **tier** | A |
| **scope** | What mksquashfs's own source says about the output-padding option: its exact spelling, the flag variable, the two places the padding is written, and the tail arithmetic. NOT a claim about any carrier, NOT the rationale (the rationale is in the shipped man page, a different artifact at a different version), NOT a claim that any reader refuses or accepts a no-pad image. |
| **anchor** | `:205` `int nopad = FALSE;` (comment at `:204` "Will Mksquashfs pad the filesystem to a multiple of 4 Kbytes?"); option parse `:8501-8502` `strcmp(argv[i], "-nopad")` (and the sqfstar twin at `:7362-7363`); padding write `:588-590` `if(!nopad && tail) { … write_destination(fd, get_dpos(), 4096 - tail, temp); }` inside `prep_destination()`; tail arithmetic `:577` `int tail = end & (4096 - 1);`; streaming superblock offset `:6262` `block = nopad ? get_dpos() : (get_dpos() + 4095) & ~4095;`; upstream master HEAD `db038ef265ed00bb17aaf695a72f9b0c3489eb20`; file sha256 `205f58e6394844317b58266ca351966e222a2cc49657c7cc68365030d4a2bc5c` (266,790 B), byte-identical on 3 fetches, HTTP 200 2026-10-30 |
| **teaches** | The upstream option is **`-nopad`, one token** — `-no-pad` is not an option (measured: `mksquashfs: -no-pad is an invalid option`, exit 1). The padding it skips is a **zero-fill of the tail up to the next 4096-byte multiple** of the *output file* (`4096 - tail` zero bytes at `get_dpos()`), plus, in streaming mode only, a 4096-aligned superblock offset. It is a producer-side image-length property, not a filesystem-content property. On the lane's own committed fixture family the same image appears at 320 B (`nopad`), 1024 B (`1kpad`) and 4096 B (`4kpad`) bytes, so the pad state is observable as `file_size mod 4096` and as `file_size - bytes_used`. |
| **status** | mined |
| **opened** | 2026-10-30 |
| **recheck** | on-release |
| **used-by** | corpus/knowledge/2026-10-30-r51-… (the R51-C2 triage-v6 entry, stem to be fixed by the L1); `SKILL.md` rule block 27 (triage table v6) |

---

## Gate record (the `## Gate` shape the lane uses)

- **URL**: https://raw.githubusercontent.com/plougher/squashfs-tools/master/squashfs-tools/mksquashfs.c
- **Access date**: 2026-10-30 (UTC), HTTP 200
- **Bytes**: 266,790 · **sha256**: `205f58e6394844317b58266ca351966e222a2cc49657c7cc68365030d4a2bc5c` · **etag**: `f67f5d0593f9575daf92fd84707a99efc5e1ba0e4d90820ee801835fe5bd5502`
- **Located quotes** (all ≤25 words; full list in `quotes.md`):
  - `:205` — `int nopad = FALSE;`
  - `:588` — `if(!nopad && tail) {`
  - `:590` — `write_destination(fd, get_dpos(), 4096 - tail, temp);`
  - `:577` — `int tail = end & (4096 - 1);`
  - `:8501` — `} else if(strcmp(argv[i], "-nopad") == 0)`
- **Measured companion** (this seat's own probe, receipt `receipts/probe-receipt.json`): two tiny squashfs images from one input dir, `padded` 4096 B sha256 `3e775fb0…be6d7e648` vs `nopad` 281 B sha256 `f25daa73…0363e5e`; byte-length difference **3815**; the no-pad bytes are a byte-exact **prefix** of the padded bytes and the 3815-byte tail is **all zero**; `bytes_used` is **281 in both**; both images extract to an **identical tree**; a second padded build is byte-identical (a third, built 2 s later, differs **only** in the superblock `mkfs_time` at offset 8..11).
- **Flip condition**: if upstream renames or removes `-nopad`, or changes the padding from a 4096-byte multiple to another quantum, this row's anchor must be re-located and the discriminator's observable re-derived.

---

## Companion row candidate (NOT proposed as a separate registry row — a **rejection** to record)

The lane's round-51 claims file asks for "the squashfs-tools `-no-pad` / padding source row". **The name `-no-pad` does not exist upstream.** Two ways to record that, both honest:

1. **Preferred:** register the row as S250 above with the **measured** spelling `-nopad`, and amend the claims-file wording from "`-no-pad`" to "`-nopad`" in the freeze. The claims-file amendment belongs to the L1 (the `## Wave-1 amendment record`), not to this seat.
2. **Alternative:** register a second row for the *rejection* — "squashfs-tools `mksquashfs.c`, the `-no-pad` spelling — searched and absent" — with `status: rejected`, `scope: the hyphenated spelling does not exist; the option is `-nopad`` and `teaches: the corpus' "no-pad body" is a fixture-family name, not an upstream option name; a reader-facing rule must not cite `-no-pad``.

**Recommendation to the L1: option 1**, because the hyphenated spelling is a *prompt typo*, not a rejected source — recording it as a rejected row would misreport a typo as a screening decision. The one thing that must survive into the freeze is the exact spelling `-nopad`, because the R51-C2 audit's discriminator must not be written against a flag that does not exist.

---

## Secondary artifact — the rationale (a different artifact, different version)

The upstream master `mksquashfs.c` carries **no** "why" comment for the padding (full-file grep: only `:204`, `:573` and the code sites). The rationale lives in the **shipped man page** of the installed tool:

- `/usr/share/doc/squashfs-tools/USAGE-MKSQUASHFS`, sha256 `b047ffbb3d9bb5389212d32d03e99d2850e0a211833e128f759c62aa26b12e7f`, 1435 lines, squashfs-tools 4.7.5-1
- `:1431` "The -nopad option informs Mksquashfs to not pad the filesystem to a 4K multiple."
- `:1432-1433` "This is performed by default to enable the output filesystem file to be mounted / by loopback, which requires files to be a 4K multiple."
- `:1434-1435` "If the filesystem is being written to a block device, or is to be stored in a bootimage, the extra / pad bytes are not needed."

This is a **host-installed documentation file, not a fetched upstream source** — if the L1 wants it as a citable row it needs its own SOURCES entry (kind `docs`, tier B, `recheck: on-release`, and a `used-by` naming the R51-C2 entry). This seat does not propose it as S250's companion row because it was read from the host, not opened at a URL.

---

## What this row does NOT license (scope fences for the C2 rule draft)

1. It does **not** license a rule that says "a no-pad body is unreadable". Measured on the lane's committed ddwrt fixture family: `unsquashfs -s` refuses the **4096-byte 4kpad** image exactly as it refuses the 320-byte no-pad one (both exit 1), and a **one-byte** magic patch (`0x74`→`0x73`) makes **both** readable (exit 0). Pad state and reader refusal are **independent**.
2. It does **not** license reading a **body's** pad state out of the scored envelope. Measured on the 126-envelope round-42 corpus: the envelope's `locations[0].end` carries the **body length** (320 / 1024 / 4096 per variant), but the triage v5 feature tuple (`OP PV H F HF G D BE SR P commands`) does **not** carry it, and the failed body `dmg_Z3_v3ddwrt_inode_table` is a **320-byte** body with a `tqsh` magic whose refusal message is `read_inode: failed to read inode 144:128` — an **inode/metadata read** failure, not a pad failure.
3. It does **not** license "the pad is why the reader refuses". The refusal reason for the ddwrt family is the **non-standard magic** (`tqsh`/`hsqt` instead of `sqsh`/`hsqs`), as the lane's own round-42 reader oracle already recorded ("as published: unsquashfs -s rc=1"; "std-magic copy (sqsh): unsquashfs -s rc=0").
