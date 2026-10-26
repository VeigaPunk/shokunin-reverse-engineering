# R40W2C1Chain — vendor provenance chain + licence boundary

**Verdict: DEFECTS FOUND.** The provenance chain itself survives every attack I could mount (URLs live,
pins reproduce from two independent clients, committed oracles regenerate from freshly downloaded vendor
bytes, no firmware body is committed anywhere in history) — but the claim's licence sentence
"Vendor bytes are never committed" is **falsified at the landing revision**: four distinct AVM
firmware-package members (5 committed blobs) and two AVM download-page files, byte-identical to the live
vendor copies, sit in the tip tree; and one chain link the claim lists (`member_sha256`) is reported but
never compared by `fetch-vendor.py`.

What I attacked: the external half of R40-C1 — V1/V2 URL liveness and identity, the AVM download
directories, `tools/round-40/fetch-vendor.py` (self-test, real fetch, failure paths, tampered specs), an
independent rebuild of both carriers (curl + GNU tar instead of urllib + tarfile), the committed receipts
and oracles, and a whole-tree / whole-history scan of the lane at `4d62ee5a` for committed vendor bytes.
Lane HEAD when I started was `0b15c8b2` (`round-40: wave-2 spec, generator and validated dispatch` — one
commit past the assigned dispatch tip `4d62ee5a`); every tree claim below is read at `4d62ee5a`.

Scratch: `S=/fast/scratch/hyaku/kaidoku-r40/R40W2C1Chain` (removed at the end). Evidence copies:
`.ufo/waves/round-40/w2/artifacts/R40W2C1Chain/`.

---

## 1. What holds — the chain, re-derived from the wire

**H1. Both vendor URLs are live and self-consistent.** `curl -sS -I` (dumped verbatim in
`artifacts/R40W2C1Chain/http-headers.txt`):

| | V1 | V2 |
|---|---|---|
| URL | `…/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image` | `…/fritzbox-6820-lte/other/fritz.os/FRITZ.Box_6820v1_LTE-07.30.image` |
| status | `HTTP/2 200` | `HTTP/1.1 200 OK` |
| content-length | 39741440 | 28334080 |
| last-modified | `Mon, 04 Sep 2023 17:08:03 GMT` | `Thu, 07 Sep 2023 11:26:20 GMT` |
| etag | `"64f60ef3-25e6800"` | `"64f9b35c-1b05800"` |

**H2. The AVM download directories still list both images, at exactly those sizes and dates.** Listing
bodies fetched today: `…/fritzbox-6490-cable/other/fritz.os/` sha256
`063ec39af00bd45e668519cc2ce95debf41cf5d56ed9dcde37223b57f6d8f7bc` (lists `FRITZ.Box_6490_Cable-07.57.image … 04-Sep-2023 17:08 39741440`),
`…/fritzbox-6820-lte/other/fritz.os/` sha256
`07e2b9f2c18a8e854d890d0fbb53956457b50abd1d216af3343f9fd30ce4ab02` (lists
`FRITZ.Box_6820v1_LTE-07.30.image … 07-Sep-2023 11:26 28334080`). The 6490 listing is also byte-identical
to the wave-1 committed `.ufo/waves/round-40/w1/artifacts/R40SrcAvmVendor/listing.html`
(sha256 `063ec39a…f7bc`) — the directory listing has not moved since wave 1.

**H3. `fetch-vendor.py` self-test passes and a real fetch reproduces both carrier pins.**
`python3 -I -B tools/round-40/fetch-vendor.py --selftest` → `SELFTEST cases=8 pass=8 fail=0`, exit 0.
Real fetch (`--root … --rev 7fce3086… --cache "$S/cache"`) → exit 0, and per carrier:
V1 `image_sha256 f518ce6b…ede6d`, member `334e56df…f3d4` (5443592 B), carrier
`ac4098bd…8e95` (5442392 B); V2 `image_sha256 3948449d…9450`, member `cacc6461…4b19` (26013704 B),
carrier `5ccc7614…089b` (26013550 B). Both equal `carriers.json` (`artifacts/…/fetch-vendor-real-run.json`).

**H4. Two independent clients, two independent toolchains, one carrier.** I re-downloaded both images with
`curl` and rebuilt the carriers with `tar -xf` + `head -c <length>` — no shared code with
`fetch-vendor.py` (urllib + `tarfile`). Image sizes/sha256 match H1 and the pins; member sha256 match; the
carved carriers are **byte-identical** to the cache `fetch-vendor.py` wrote (`cmp`, both carriers). So the
carve length (`bytes_used`, not the whole member) is load-bearing: pointing `length` at the whole member
(`5443592`) makes the run exit 1 `carrier_sha256`.

**H5. The carriers are the genuine AVM layout, parsed independently.** Both: magic `sqsh`, `s_major 4`,
`s_minor 0`, `block_size 65536`, `compression 4`, and `mkfs_time == bytes_used`
(V1 `5442392`, V2 `26013550`) — the AVM marker. Metadata-block headers are little-endian: at
`inode_table_start` (V1 `5421468`, V2 `26011444`) the u16 reads `1380`/`704` LE (both inside
`0 < len ≤ 8192`) and `25605`/`49154` BE (both outside) — I verified this with my own `struct` parse, not
through `sqfs-list.py`.

**H6. The committed oracles regenerate from freshly downloaded bytes.** `sqfs-list.py --layout avm
--files --nonregular` on my independently rebuilt carriers: exit 0 both; V1 697 file rows / 381 non-regular
rows, V2 8 / 95 — `diff` against the committed `corpus/evidence/round-40/c1/{V1,V2}/{oracle,nonregular}.tsv`
is **empty for all four**. A third, unrelated tool confirms the content: `sasquatch-v4be -d OUT` (no `-be`)
on the fresh carriers yields 697 files / 263 symlinks (V1) and 8 / 85 (V2), with **0** sha256+size
mismatches against `oracle.tsv` and **0** symlink-target mismatches against `nonregular.tsv`.

**H7. Receipt bindings recompute.** `sha256(committed after.json)` equals the `receipt.sha256` recorded in
`run.json` for both carriers (`98aaa5f9…7776` V1, `ab761fba…770b` V2); each receipt's `subject.digest.sha256`
equals its carrier pin; the single chunk is handler `squashfs_v4_be`; gap kinds are
`{depth-limited: 1, unpublished-entry: 263}` (V1) and `{…: 1, …: 85}` (V2), all unpublished entries
`symlink`. The tool identities in the receipts match the installed binaries by sha256:
`sasquatch-v4be` `fac88740…214c6` (= `~/.local/bin/sasquatch-v4be`, `unsquashfs version 4.5.1 (2022/03/17)`),
`unblob` shim `0ce7b624…1d09` (= `~/.local/bin/unblob`, 26.6.4, resolves to
`~/.local/share/uv/tools/unblob/bin/unblob`, the `command_env` the receipt records).

**H8. The pins never moved after the freeze.** `git log 7fce3086..4d62ee5a -- .ufo/waves/round-40/c1/carriers.json
.ufo/waves/round-40/c1/gap-rule.json tools/round-40/fetch-vendor.py` is empty.

**H9. Carrier selection is not cherry-picked.** V1's image holds two `filesystem` members — the LE
`./var/remote/var/tmp/x86/filesystem.image` (`hsqs` at 270848, 28200968 B) and the BE
`./var/remote/var/tmp/filesystem.image` (`sqsh` at 32026112, 5443592 B); the chosen one is the only BE body
at top level, and the LE one is the disclosed out-of-scope class. V2 has one member and a second `sqsh` at
relative 284724 inside it (the nested `filesystem_core`, disclosed as not claimed). Neither image has a
duplicate tar member name, so the name lookup in `carve()` cannot be shadowed.

## 2. What breaks

### D1 (main) — "Vendor bytes are never committed" is false at `4d62ee5a`

The claim (`plans/round-40-claims.md`, carriers bullet: *"Vendor bytes are never committed (the AVM licence
forbids redistribution…)"*) and the landed entry (`corpus/knowledge/2026-10-26-r40-avm-be-squashfs-core.md:43`,
*"Vendor bytes are not committed"*) are contradicted by committed AVM bytes:

| member of the `.image` | bytes | sha256 | committed at |
|---|---|---|---|
| `./var/info.txt` (the AVM licence notice itself) | 2807 | `b0360d88…e39b` | `w1/artifacts/R40SrcAvmVendor/image-members/info.txt` **and** `w1/artifacts/R40C1VendorV1/info.txt` |
| `./var/version` | 47 | — | `w1/artifacts/R40SrcAvmVendor/image-members/version` **and** `w1/artifacts/R40C1VendorV1/version` |
| `./var/content` | 346 | — | `w1/artifacts/R40SrcAvmVendor/image-members/content` |

Plus two files from the AVM download page, **byte-identical to today's live copies**:
`w1/artifacts/R40SrcAvmVendor/info_de.txt` (111698 B, sha256 `3becce79…5a1e`) and `info_en.txt` (67591 B,
sha256 `6c601b34…70a7`).

What is *not* committed, and this is the part the claim really needs: **no firmware body and no extracted
filesystem file.** Evidence: every one of the 28119 blobs at `4d62ee5a` hashed (393,655,002 bytes) — zero
equal the V1/V2 carrier, image or member pins (the only pin hits are the two legitimately lane-built
carriers `corpus/evidence/round-40/c1/{L1,L2}/carrier.sqsh`); zero equal any of the 601 distinct V1/V2
extracted-file digests of size ≥ 16 B (the only digest collisions are zero-length and 1-byte vendor files,
i.e. sha256 of empty/one-byte content); zero start with the 16-byte V1 or V2 carrier prefix; the 385
committed blobs that start with `sqsh`/`hsqs` are all lane-built fixtures (largest 241390 B = L2's own
carrier). Whole-history check: `git cat-file --batch-all-objects` over 32518 objects shows **no object of
any type** whose size equals a vendor image, member or carrier — the bytes were never committed and later
removed either.

Calibration. Severity is real but narrow: the licensed software (the firmware bodies, the 697-file
squashfs contents) is genuinely absent, so no redistribution of the program occurred. What landed are the
package's own 47–346 B identity/law files (and the licence notice itself) plus AVM's public release notes.
The wave-1 report (`w1/R40SrcAvmVendor.md:30`) flagged exactly this and wrote *"the L1 may prefer to drop
`image-members/info.txt`"* — the tip instead keeps it **twice**. `[INFERENCE]` the L1 took the identity quote
as fair use and never revisited the wording. Either way the sentence as frozen is false, and the notice it
quotes forbids copying "in whole or in part", not just of the whole image.

**D1-b (same axis, not a byte issue).** The notice's other clause — *"shall not be modified, disassembled,
reverse engineered, decompiled or otherwise be opened in whole or in part"* — covers the C1 procedure
itself and the derived per-file inventory it publishes (697 paths + sha256 + sizes for V1). The claim
cites only the redistribution clause, which implies compliance is achieved by not committing bytes. It is
not: `[INFERENCE]` the honest framing is "we avoid redistributing the package and publish only derived
metadata; the vendor terms also purport to forbid the analysis", not "the licence is satisfied".

### D2 — `member_sha256` is a chain link the tool does not check

`carriers.json` pins `external.member_sha256` and `fetch-vendor.py` echoes it into `member_detail` and into
both `provenance.json` receipts, but `materialise()` only compares `image_sha256` and the carrier pin.
Tampered-spec matrix (`--spec` on a copy, cache dirs under scratch):

| mutation | exit | `link` | cache bytes written |
|---|---|---|---|
| V1 url → `…-99.99.image` | 1 | `url` (HTTP 404) | 0 |
| V2 carrier pin → `0*64` | 1 | `carrier_sha256` | 0 |
| **V1 `external.member_sha256` → `deadbeef*8`** | **0** | **None (ok)** | carrier written |
| V1 `external.length` → whole member | 1 | `carrier_sha256` | 0 |

Impact is nil for identity — a pinned image sha256 determines the member, so the carrier pin still binds —
but the claim text ("URL → image sha256 → tar member → carve length → carrier sha256") presents five
verified links and the tool verifies four. A one-line `member_sha256` comparison in `carve()`/`materialise()`
closes it; `selftest` already has the fixture for it (`member-absent` / `length-overrun` cases).

### N1 (nuance, not a defect) — `sasquatch-v4be` exits 2 on both carriers

Direct extraction returns exit 2 while logging `created 697 files / 263 symlinks / 0 devices`. Cause: the
char device cannot be created without privilege (`created 0 devices`), so the oracle's 1 char device per
carrier is never materialised and a naive rerun that treats sasquatch `exit != 0` as failure would report a
spurious failure. The claim's own receipts record REA's exit 0, not sasquatch's, so nothing scored is
wrong — but a future independent cross-check needs to expect this.

### N2 (documentation gap) — V2's directory count is missing from the carriers bullet

The claim gives V1 as "697 regular files, 263 symlinks, 117 directories, 1 character device" and V2 as
"8 regular files …, 85 symlinks, 1 device". `nonregular.tsv` for V2 also carries **9 directories** (95 rows
= 85 + 9 + 1). Harmless for scoring (the gap rule requires no gap for directories) but the two carriers are
described to different precision.

## 3. Effect on the verdicts under attack

- **R40-C1 = NOT MET** is unaffected and remains honest: my findings attack (i) a descriptive sentence in
  the carriers bullet that no counter binding reads, and (ii) an unverified tool link that cannot change a
  pin outcome. Neither produces a fifth carrier match nor makes the 3/4 score admissible.
- The demotion in `PROVINCE.md` (line 386 `## Round-40 measured, not promoted (R40-C1 honest stop)`, frontier
  note at line 394 naming the entry stem) and the `corpus/README.md` mappings (lines 96, 208, 250) are
  consistent with the L1's account: no `## Round-40 additions to Core` row exists, so the predicate's
  promotion clause is genuinely unmet.
- **Any re-freeze of R40-C1 must correct the licence sentence** (name the four committed members and the two
  download-page files, or delete them and say "no firmware body, no extracted filesystem file and no vendor
  image is committed") and should bind `member_sha256`. As written, the sentence is a falsifiable statement
  the landing already fails — the cheapest fix is deleting the four members and both copies of the licence
  notice from the tree, since `provenance.json` already carries the digests that identify them.

## 4. Reproduction

```bash
S=/fast/scratch/hyaku/kaidoku-r40/R40W2C1Chain; mkdir -p "$S"; export TMPDIR="$S"
cd "$S"
# H1/H2
curl -sSI https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image
curl -sS  https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/ -o d1.html && sha256sum d1.html
# H3
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-40/fetch-vendor.py --selftest
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-40/fetch-vendor.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 7fce308631a8b457d6b7c5a4b39a923c4e9a49de --cache "$S/cache"
# H4 (independent carve) / H5 / H6
curl -sS -o img/6490.image <V1 url>; tar -xf img/6490.image -C m './var/remote/var/tmp/filesystem.image'
head -c 5442392 m/var/remote/var/tmp/filesystem.image | sha256sum     # ac4098bd…8e95
python3 -I -B <lane>/tools/round-40/sqfs-list.py --layout avm --files F.tsv --nonregular N.tsv m/V1.carrier
diff -q F.tsv <lane>/corpus/evidence/round-40/c1/V1/oracle.tsv
~/.local/bin/sasquatch-v4be -d x m/V1.carrier    # exit 2, 697 files, 0 devices
# D1 (whole-tree and whole-history sweep)
#   git ls-tree -r -l 4d62ee5a | 28119 blobs, sha256 each  -> artifacts/…/blob-scan.json
#   git cat-file --batch-all-objects --batch-check        -> no vendor-sized object
```

The sweep and comparison programs are the same ones whose outputs I serialised into
`artifacts/R40W2C1Chain/{vendor-chain,blob-scan,licence-boundary,repro}.json`; each records the numbers
quoted above. No vendor bytes are copied into the lane: only hashes, sizes, headers and my own derived
tables.

## 5. Limits

- I verified *today's* vendor bytes, not the bytes the L1 downloaded at 16:16 UTC: the URLs are pinned by
  sha256 and both clients agree, but a mid-round swap to different bytes with the same sha256 is out of
  reach (collision assumption).
- The sweep proves absence of vendor-sized *git objects*; a vendor body re-encoded (compressed, base64,
  chunked) inside a text file would evade the size sweep, and my content checks against it are the
  exact-digest intersections, the 16-byte prefix scan and the `sqsh`/`hsqs` magic scan only. A body stored
  under a non-squashfs transform would not be caught.
- "Which process wrote the committed receipt" stays unproven, as the claim discloses; I only showed the
  receipt is *reproducible* from fresh vendor bytes and internally bound (H6, H7).
- `[INFERENCE]` judgements are marked inline: the fair-use reading of the licence-notice quote, and the
  severity split between "wording false" and "firmware leaked".
- No tool was installed, upgraded or moved: `curl`, GNU `tar`, `python3`, `sasquatch-v4be` 4.5.1,
  `unblob` 26.6.4 were already present and used as-is.
