# C1MarkerCritic — R50-C1 AVM-marker clause attack (wave 1, pre-freeze)

## Verdict

**The AVM-marker clause does not separate "genuine" from "re-stamped standard LE" for REA, and as drafted it cannot be exercised alone by CTL-C1-4.** Measured: a standard LE xz image whose `mkfs_time` is patched to `bytes_used` produces the same REA projection as the unpatched image (files, sha256, sizes, gaps, chunk handler). The marker is read only on unblob's big-endian branch. What REA *does* see on genuine members is an **8-byte trailer past `round_up(bytes_used, 4096)`**, present on every AVM member probed (9 of 9, LE and BE), absent from re-stamped standard images, and it changes the gap and file set. The claim must be re-worded (provenance = sha256 pin, not marker) and the three carrier defects below must be folded in before the freeze.

## Answers to the three questions

**(1) What the clause proves / does not.** The plan's clause (`layout_ok`, draft counter line 97–98) proves that the pinned carrier bytes have `hsqs`, v4.0, comp 4 and `mkfs_time == bytes_used`. Given a frozen carrier pin (`carrier_pin_ok`), the marker is a constant of those bytes: it can fail only when the pin already fails, so it adds no independent evidence. It does not prove vendor origin: Freetz's AVM-LE definition (verified, see F6) is "the only difference of this format to the original LE format is that the value of the mkfs_time superblock field is equal to the bytes_used field". Unblob never reads it on LE (F3). Plan Disclosed limit (1) states the invisibility correctly but stops short of saying the marker is a re-stampable timestamp field.

**(2) Standard LE image with the marker patched.** Done in scratch (fixtures: r36 K1 `k1-le-xz.sqsh`, and a fresh `tools/round-41/gen-squashfs.py --endian le --comp xz` build of the r36 K1 source tree). Patch = 4 bytes at offset 8 (`mkfs_time := bytes_used`). `cmp -l` shows exactly the mkfs field differs (3 bytes; the 4th was already 0). unblob 26.6.4 and REA 6.5.0 both extract both forms with `squashfs_v4_le`, identical trees and identical REA projections (F1, F3b). So **a patched standard image is indistinguishable from an unpatched standard image to REA, and is indistinguishable from an AVM-LE member on the marker alone.** What then distinguishes "genuine" is: (a) provenance — the frozen sha256 pin of the vendor bytes, whose chain (download.avm.de URL → image sha → member sha → carrier sha) the counter does not re-verify at REV; and (b) the trailer (F5), a byte property a plain re-stamp does not reproduce (a determined re-stamper can append 8 bytes). The trailer is not a plain md5/sha1/sha256/crc32 of the filesystem (tested, no hit); its origin is not identified.

**(3) Proposed wording** — see section "Proposed wording" below (Disclosed limits (1) replacement, extra limit (6), Core row, Frontier retirement, CTL-C1-4 fix).

## Findings

| # | Finding | Command (abridged; full argv in receipts.json) | Exit | Evidence (sha256 / value) |
|---|---|---|---|---|
| F1 | Standard LE and stamped LE give identical REA projection | `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output --max-depth 1 <img> <out>` on `std-r36.sqsh`, `stamp-r36.sqsh`, `gen-le-xz.sqsh`, `gen-stamp.sqsh` | 0,0,0,0 | std `93802938…a589` (= r36 K1 carrier pin), stamp `f24359bf…a832`; 3 files, 70086 B published (= r36 K1 receipt `published_bytes`), chunk `squashfs_v4_le` 0..73728, gaps `depth-limited` only; files/sha/gaps equal across pairs; evidence ids differ (not analysed further) |
| F2 | Marker patch is the only byte difference std→stamp | `cmp -l std-r36.sqsh stamp-r36.sqsh` | 0 (3 lines) | 3 differing bytes at offsets 8–10 (`mkfs_time` 0x011352 vs 0) |
| F3 | unblob reads the marker only on BE | `sha256sum …/handlers/filesystem/squashfs.py` (unblob 26.6.4, uv tool); source lines 39–54 | 0 | `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` = S108 value; `is_avm = header.bytes_used == header.mkfs_time` only in `case Endian.BIG, 4`; LE branch `commands_args.append("-le")` unconditionally; `calculate_chunk` uses `bytes_used` only |
| F3b | unblob direct run on both LE forms | `unblob -e <dir> -f <img>` | 0,0 | both log `SQUASHFS_V4_LE`; extracted content hashes identical (only the directory-name prefix differs) |
| F4 | CTL-C1-4 "red on marker alone" is not achievable as written | reading draft counter `C1CounterPort/tools/round-50/c1-counter.py` CLAUSES tuple (line 321–323), `carrier_pin_ok` (line 90), `subject_pin_ok` (line 119) | — | a planted standard carrier with genuine receipts fails `carrier_pin_ok` and `subject_pin_ok` as well; only a control whose own carriers.json pins the planted bytes (and re-issued receipts) isolates `layout_ok` |
| F5 | Every AVM member probed carries an 8-byte non-zero trailer at `round_up(bytes_used,4096)` | `marker-probe.py` on 9 members (table below); `tail_nonzero == 8` every case | 0 for probes | 9 of 9 AVM members, LE and BE; `23de53c4e5960d62` (7530). Re-stamped std image: no trailer. Appending the same 8 bytes to std-r36 and stamp-r36 (`*-trl`): both give `unknown-chunk-handler` gap + `73728-73736.unknown` file, regardless of marker (exit 0, 0). So the REA-visible genuine signal is the trailer, not the marker |
| F6 | Freetz AVM-LE definition (source for "what the marker is") | read `https://www.freetz.mhampicke.de/trunk/make/squashfs4-le/Config.in` | — | "AVM-LE is the format used by AVM to pack the filesystem of some cable boxes, e.g. 6490, 6590 (x86 core only). … The only difference of this format to the original LE format is that the value of the mkfs_time superblock field is equal to the bytes_used field." Non-cable 7530/7520/7590/6850 members also carry the marker (F7), which this note does not list — the documented scope is narrower than the observed one |
| F7 | Carrier probe (scratch copies; member bytes not kept) | `marker-probe.py <scratch> <image> [member]` (draft, `tools/round-50/marker-probe.py` in seat dir) | 0 | table below |
| F8 | **Cable carrier member path in the plan is wrong**: `./var/tmp/filesystem.image` is absent from the 6490/6430/6590 cable tars; the LE x86-core member is `./var/remote/var/tmp/x86/filesystem.image` (sizes 28200968 / 23863304 / 27750408 = the plan's "28 MB"/"23.9 MB"). The 5.4 MB `./var/remote/var/tmp/filesystem.image` at that cable path is **BE** (`sqsh`, AVM-BE) and would fail the LE clause. The L1 scan (`l1/scan-output.txt`) reports the x86 sizes, so the scan read the right member under the wrong name | `tarfile.getmember('./var/tmp/filesystem.image')` on FRITZ.Box_6490/6430/6590 | 2 (MISSING) | 6490 image `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`, 6430 image `52e3687d7363301453aa4fe0c712126874c90d3c138dee0792213dab11f5d815` (from `C1CarrierAdversary/img/SHA256SUMS`, not re-downloaded); x86 member sha 6490 `7ea4c628def17c25dc05f6103f8563884022dd1a5baf0c4fba38a85b546a0419`, 6430 `25194a87e54f98d868c614cef4ef8509c3e8f34bd6498bc03cdc3e7dcdd4934c`, 6590 `57552a6dd81b6a43032b761bfbd10090442dbbcce88609bdb731af1242932786` |
| F9 | **a7530 fails under the plan's frozen REA argv** (default `--max-output-files` 10000) | `extract-firmware --max-depth 1 g7530.sqsh <out>` | 1 (`ok:false`, `unreadable_output`, `Staging entry budget exceeded (10000)`) | 7530 member has 15150 inodes. Re-run with `--max-output-files 100000`: rc 0, 13367 published files (13366 regular + 1 `.unknown`). Unsquashfs 4.7.5 oracle: 13366 regular files, 857 symlinks. The 13366 REA regular files: **0 sha/size mismatches** against the oracle. Extra: `firmware.bin_extract/34004992-34005000.unknown`, outside the chunk root `0-34004992.squashfs_v4_le_extract/`. Gap `unknown-chunk-handler` (not in the round-41 structural allowance `{'depth-limited': 1}`) |
| F10 | Trimmed 7530 (carve to `bytes_used`) removes the residue | `head -c 34003969` then REA with `--max-output-files 100000` | 0 | 13366 files = oracle count; no `unknown` gap or file; diagnostics only `MaliciousSymlinkRemoved`. (Trimmed sha projection not separately compared to the oracle; the untrimmed run matched it 0 mismatches.) |
| F11 | Cable x86-core LE members extract with default budget, but residue again | REA default argv on `c6490x86.sqsh` (28200968 B) and `c6430x86.sqsh` (23863304 B) | 0, 0 | 6490: 4710 files (4709 regular + `28200960-28200968.unknown`), chunk `squashfs_v4_le` 0..28200960, unsquashfs oracle 4709 regular, 0 mismatches. 6430: 3956 files (3955 regular + `23863296-23863304.unknown`), oracle 3955 regular, 0 mismatches. Oracle `unsquashfs -o 0` exited **2** for both (device-node creation, unprivileged; files written; not inspected further) |
| F12 | Budget risk for the other planned carriers, inferred | inode counts from probe (7520 15150, 7590 15151, 6850 11198 entries ≥ 10000) | not run | inferred to fail under default argv like 7530; **not run**. 6490/6430/6590 x86 members (5624/4780/5627) are under the budget (6490 and 6430 ran under it, F11) |
| F13 | Oracle exit code | `unsquashfs -no-progress -o 0 -d <dir> g7530.sqsh` | 0 | regular 13366, symlink 857, dirs 926 |
| F14 | Round-36 calibration reproduced | REA on r36 K1 fixture (max-depth 1) | 0 | 3 files, 70086 B, matches `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` K1 row (published 70086) |

### Carrier probe (scratch copies; the superblock fields the marker clause reads)

| image | member | magic | inodes | bytes_used | mkfs==bu | tail non-zero after bu | tail offset from round_up(bu,4096) |
|---|---|---|---|---|---|---|---|
| 7530 | ./var/tmp/filesystem.image (34005000 B) | hsqs | 15150 | 34003969 | yes | 8 | at round_up (1023 B after bu) |
| 7590 | ./var/tmp/filesystem.image (35835912 B) | hsqs | 15151 | 35834769 | yes | 8 | at round_up (1135 B after bu) |
| 7520 | ./var/tmp/filesystem.image (34013192 B) | hsqs | 15150 | 34009089 | yes | 8 | at round_up (4095 B after bu) |
| 6850 | ./var/tmp/filesystem.image (32526344 B) | hsqs | 11198 | 32525731 | yes | 8 | at round_up (605 B after bu) |
| 6490-cable | ./var/remote/var/tmp/x86/filesystem.image (28200968 B) | hsqs | 5624 | 28200029 | yes | 8 | at round_up (last 8 bytes; tail 939 = 931 + 8) |
| 6430-cable | ./var/remote/var/tmp/x86/filesystem.image (23863304 B) | hsqs | 4780 | 23861507 | yes | 8 | at round_up (tail 1797 = 1789 + 8) |
| 6590-cable | ./var/remote/var/tmp/x86/filesystem.image (27750408 B) | hsqs | 5627 | 27748075 | yes | 8 | at round_up (tail 2333 = 2325 + 8) |
| 6490-cable | ./var/remote/var/tmp/filesystem.image (5443592 B) | **sqsh (BE)** | 1079 | 5442392 | yes | 8 | at round_up (not an LE carrier) |
| 6430-cable | ./var/remote/var/tmp/filesystem.image (5984264 B) | **sqsh (BE)** | 1098 | 5981012 | yes | 8 | at round_up (not an LE carrier) |

Member shas (scratch, not committed): 7530 `df6c22ddd009870404375aff606853c9d5171580437b6aae193114d2040c6e56`, 7590 `05ba6ac992f77076cd72d97ed98ab7612f3cc6969f6bbf736515537a9373c3dc`, 7520 `6e2f4a0b420378764ea5461fd83b1620caf54c3bc7eed3824a9a3a433f8629a2`, 6850 `3fc0825b533bbe7adb817cdc62230cd52473f325b50ecffab7a73fab327102c8`. Image sha 7530 `b17fe5cd0bd3faa713dd92513cb3a65c23e61f5f23366c343b78674955d35e9c` = plan value (downloaded, `curl` exit 0, HTTP 200). The 7590 image sha in `SHA256SUMS` is `267ef427337d2141736ad6ed5d9389722a6a1234dd590bb7d4ebf11a00616c0d`; not re-downloaded.

## Proposed wording (for the L1 to fold in; the plan is not edited here)

**Disclosed limits (1) — replace:**
> (1) The AVM marker (`mkfs_time == bytes_used`) is, per Freetz's AVM-LE definition (`make/squashfs4-le/Config.in`), the only superblock difference between AVM-LE and standard LE. unblob 26.6.4 reads it only on its big-endian branch (`squashfs.py:47-54`); on LE it passes `-le` for every image. REA's projection of a standard LE image re-stamped to the marker equals the unstamped image's (round-50 scratch receipts `rea-std-r36`, `rea-stamp-r36`). The claim is therefore "REA publishes every oracle file of these four vendor-pinned LE members", never "REA or unblob recognises AVM" and never "the marker proves vendor origin". "Genuine" means the carrier bytes equal the frozen vendor-download pin; the marker is a descriptive check on those bytes.

**Disclosed limits (6) — add:**
> (6) Each AVM member probed carries an 8-byte non-zero trailer at `round_up(bytes_used, 4096)` (9 of 9 AVM members, LE and BE; not a plain md5/sha1/sha256/crc32 of the filesystem; origin not identified). REA reports it as an `unknown-chunk-handler` gap and a `<start>-<end>.unknown` file outside the chunk root, with or without the marker. The carrier is trimmed to `bytes_used` (carve recorded in the pin chain) — or the gap rule admits this residue; the choice is frozen before the data run.

**Core row (`## Round-50 additions to Core`) — suggested:**
> `squashfs_v4_le` — little-endian SquashFS v4 (xz) members of four vendor-pinned FRITZ!OS images (7530, 7590, 6490-cable x86 core, 6430-cable x86 core) with the `mkfs_time == bytes_used` superblock stamp; no new REA key (unblob 26.6.4 takes the `-le` path for stamped and unstamped images alike); measured with `extract-firmware --max-depth 1` against an unsquashfs 4.7.5 oracle. Not: AVM recognition by REA or unblob; every LE AVM image; BE/AVM-BE members (`sqsh`); trailer-free re-stamps.

**Frontier:** retire "LE AVM members (`hsqs`)" as the open clause; the residual frontier becomes "AVM trailer semantics (8-byte tail after `bytes_used`, unidentified)" and "AVM-LE members of model lines other than these four".

**CTL-C1-4 — fix:** "red on the AVM-marker/superblock clause alone" is achievable only if the control's own `carriers.json` pins the planted bytes and its receipts are re-issued for those bytes; otherwise the red comes from `carrier_pin_ok` and `subject_pin_ok`. State it as "red on `layout_ok`, with the pin clauses re-pinned in the control fixture".

**Carrier table — fix before freeze (C1CarrierSelect / L1):**
1. c6490 and c6430 members: `./var/remote/var/tmp/x86/filesystem.image` (not `./var/tmp/filesystem.image`, which is absent at that path in the cable tars; the `./var/remote/var/tmp/filesystem.image` member there is BE).
2. a7530 and a7590 (and 7520, 6850 by inference): default argv exceeds the staging budget (10000). Either freeze `--max-output-files 100000` in the counter argv and in `c1-run.sh` (argv change, pre-freeze), or record a negative. 7530 with the flag works (F9).
3. Residue (F5, F9, F11): decide trim-to-`bytes_used` with the carve in the chain (F10: clean, 13366 = oracle count) versus a gap-rule allowance `unknown-chunk-handler: 1` plus an extra-file rule for `<start>-<end>.unknown` outside the chunk root. round-41 `carve_ok` (external carrier: frozen carve length == `bytes_used`) favours the trim.

## Not run

- REA on the a7590, 7520, 6850 members (budget inference only, F12).
- Trimmed-7530 sha-by-sha oracle comparison (count only, F10).
- Re-download of the 6490, 6430, 6590 or 7590 images (used the copies in other seats' scratch; hashes from `SHA256SUMS` where listed).
- Identity of the 8-byte trailer (hash candidates md5/sha1/sha256/blake2b-8/crc32 tested; none matched).
- The counter itself (draft `C1CounterPort` not run; no `--data-run`).

## Tools

No tools installed or updated (no pacman, no uv/npm installs; used existing unblob 26.6.4, rea-agents@6.5.0 via npx cache, unsquashfs 4.7.5, python3 stdlib). Web search used once for Freetz context; the verified source is the Config.in read above.

## Receipts

- `.ufo/waves/round-50/w1/C1MarkerCritic/receipts.json` (sha256 `738aa232c806b844fa63057a3de0a1470813197f77015503f1dacd51f6c234fe`): REA runs (argv class, exit, stdout sha256, input sha256, projection), oracle counts, carrier probe.
- `.ufo/waves/round-50/w1/C1MarkerCritic/tools/round-50/marker-probe.py` (draft probe; exit 0 on probed members, 2 on missing member; tested on the 6490 image).
- REA stdout sha256 (scratch, not kept): std-r36 `e9ef32ad227e88dcf8ee684ea119da5ac43fb3ef79ead734da218bd2458ab95a` (ok); g7530 default `a20983e7db1c4eb33cf8571aa1f8726144f29f10e1b3f237c9279984b67de729` (ok:false); g7530-mof `0d7d95c4e519edcaace4a3b91856669a4012f5f0bba7e065d44ea7f285dfe401`.

Scratch `/fast/scratch/hyaku/kaidoku-r50/C1MarkerCritic` removed after the receipts were written. No vendor bytes were copied into the lane tree.
