# R36W2ConnFrontierNext — round-37 frontier step: ranked next-3 moves

Seat: R36W2ConnFrontierNext (connector, leaf). Date: 2026-10-26.
Milestone context: falsify wave-1 / L1 landing; this seat's scoped slice is the §2b frontier step
for round 37. Inputs read: `plans/round-36-claims.md` (frozen R36-C1/R36-C2), `corpus/lessons/round-36.md`,
`PROVINCE.md` Frontier lists (`## Frontier`, `### Round-4 frontier (post-unlock)` bullets, round-36 Core
addition + Frontier note at `PROVINCE.md:368-374`), `corpus/README.md:233`, S108 = unblob 26.6.4
`unblob/handlers/filesystem/squashfs.py` (installed at
`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`),
and the round-36 lesson's R35-D4 / `.jsc` lead block.

All probes below ran in seat scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ConnFrontierNext` (removed at
exit). No lane, fleet, or shokuknow writes. No installs/upgrades performed by this seat (pacman untouched,
host-wide pause respected); every tool used pre-existed on the host: `sasquatch` 4.5.1 and `sasquatch-v4be`
(onekey-sec deb, landed round 36, `~/.local/bin`), `/usr/bin/unsquashfs` 4.7.5, `/usr/bin/mksquashfs`
4.7.5, `7z` 26.04, `node` v24.21.0, `curl`, kernel `squashfs.ko.zst` (loop-mount via passwordless sudo).
Read-only git only; no VCS mutation.

---

## TL;DR ranking

1. **AVM-BE SquashFS v4 recursion on a real carrier (FRITZ!Box 7490, sasquatch-v4be)** — all three seat
   criteria directly evidenced on this host today, including the do-nothing control and the end-to-end
   after-run; it is the exact "Not claimed: big-endian / AVM SquashFS …" clause of R36-C1.
2. **Dispose the `.jsc` lead with the exact-version jsc2js d8 14.8.178.14 against typora's cache** — the
   round-35 prep captures missed the 13.x/14.x release pages; the exact-match d8 exists and is downloadable;
   the lead's crashes were on 13.6/15.0, so 14.8 is genuinely open.
3. **Synthetic plain-BE v4 / AVM-quirk carriers built with freetz `squashfs4-be-host` tools** — completes
   S108 branch coverage (the `is_avm` no-`-be` path and non-AVM BE v3/v4) with a construction-level
   independent oracle; feasible but flagged build friction (`xz` headers absent, pacman paused).

---

## Move 1 — AVM-BE SquashFS v4 recursion, real carrier (highest)

Move: promote "big-endian/AVM" from Frontier to measured Core the same way R36-C1 did for LE: a frozen real
carrier, a paired no-sasquatch before-receipt and sasquatch-enabled after-receipt from REA 6.5.0
`extract-firmware`, scored against an independent extractor. Target surface named in
`PROVINCE.md:374` ("Big-endian/AVM and vendor-mangled images stay Frontier") and `corpus/README.md:233
("Still frontier: big-endian/AVM (`sasquatch-v4be`)")`. (a) Do-nothing cannot reach it: with `sasquatch`
hidden (`env -i PATH=/usr/bin:/bin`), REA 6.5.0 on the carrier published **11 files / 73,093,847 bytes —
zero files of the filesystem** — and reported
`extraction_gaps[0] = {"kind":"missing-extractor-dependency","handler":"squashfs_v4_be","dependencies":["sasquatch-v4be"],"range":{"offset":0,"length":35012608}}`
(receipt bytes copied below); the BE chunk was carved but not extracted. With `~/.local/bin` on PATH the
same command published **10,028 files / 226,964,316 bytes** including the nested
`filesystem_core.squashfs_extract/**` tree — after-run shape mirrors R36-C1's before/after design exactly.
(b) Independent expected record: partial today — three would-be oracles were tested and **failed on
AVM-BE**: kernel loop-mount (`mount: fsconfig() failed: Can't find a SQUASHFS superblock on loop0`, exit
32; note the kernel DOES work as an oracle for LE, proven by mounting a scratch LE image and reading file
contents), 7z 26.04 (sees only the bare XZ stream at offset 96, "There are data after the end of archive"),
and regular `sasquatch -be` ("Block size and block_log do not match. File system is corrupt"). The workable
independent lineage is freetz/PeterPawn `unsquashfs4-avm-be`, a different implementation from onekey-sec's
sasquatch-v4be; build feasibility on this host: `gcc (GCC) 16.2.1` and `make` present, `zlib.h`/`lzo`
headers present, but `xz.h` absent and pacman is paused — needs an official xz source drop into scratch
(friction, not a blocker). (c) Feasibility: proven end-to-end in 19.5s — carrier
`https://download.avm.de/fritzbox/fritzbox-7490/deutschland/fritz.os/FRITZ.Box_7490-07.62.image`
(38,092,800 bytes, sha256 `2ab05656563abe7fabdbbf62b3305123098b798e6f79c678f00baefc553f8ee9`, HTTP 200,
`Last-Modified: Wed, 15 Dec 2025`); inner `./var/tmp/filesystem.image` sha256
`58d73b2f490a0fd22b49154382d7d572…` (35,012,616 bytes, BE magic `73 71 73 68` at offset 0); `sasquatch-v4be`
extracted it standalone (10 dirs / 86 symlinks / nested core present); unblob 26.6.4 routed it to handler
`squashfs_v4_be` (staged dir `0-35012608.squashfs_v4_be_extract/`). One nuance the round must record
explicitly: unblob's `is_avm` check (`header.bytes_used == header.mkfs_time`, S108 handler lines 47-52) is
**False** on this image (parsed BE: `mkfs_time=0x69`, `bytes_used=0x2163042`), so sasquatch-v4be ran the
`-be` path; the no-flag AVM branch still needs a quirk-true carrier (see Move 3).

## Move 2 — Dispose the `.jsc` lead: jsc2js exact-version d8 14.8.178.14 vs typora's cache

Move: the round-36 lesson records an L1 pre-freeze probe where jsc2js patched d8 crashed (SIGSEGV on the
node 24.21.0 / V8 13.6.233.17 cache; crash printing feedback metadata on the electron 43.7.11 / V8
15.0.245.31 cache) and stores it as "a lead, not evidence". Round 37 can settle the lead on its real target:
run the jsc2js patched d8 **14.8.178.14** — the exact V8 version of typora's `atom.compiled.dist.jsc`,
pinned three independent ways in `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` (`/usr/share/typora/version`
= 42.2.0; the `Typora` ELF string `14.8.178.14`; `jscd info` brute left-fold `v8: 14.8.178.14`; electron
42.2.0 `process.versions` v8 `14.8.178.14-electron.0`) — with `loadjsc()` on the cache, then View8
reconstruction. (a) Do-nothing cannot reach it: no held tool decompiles a V8 14.8 cache (jscd v0.1.0
hard-refuses ≥14.8, tables stop at 14.6; REA `unsupported_target`; host node 24 rejects
`0xC0DE06C3` — all recorded r4-07). (b) Independent expected record: structural, not source-level — the
original webpack source is unavailable (typora is closed-source), so the check is against the lane-held
r4-07 Ignition disassembly (530KB, 116-block band) from `ELECTRON_RUN_AS_NODE=1 electron@42.2.0
--print-bytecode`, plus the cache header's recorded `version_hash 0x76842c11` / `source_hash 0x00039fde`;
a full source diff is impossible and must not be claimed. (c) Feasibility: correction to round-35 prep —
the captured release pages (page 1 = newest 15.x, page 7 = oldest 9-12.x) **missed the middle pages**;
live GitHub API scan of all 7 pages shows `13.6.233.17` (page 6) and a full 14.8 line including the exact
`14.8.178.14` (page 5), with asset `d8-14.8.178.14-linux.tar.gz` (13,796,728 bytes, download URL resolves
302 → release-assets). Host node v24.21.0 and typora's tree (`/usr/share/typora`, `Typora` ELF present)
are on-host. Risk stated plainly: the lead's crashes may still reproduce on 14.8 (jsc2js's own README warns
node-produced caches may not decompile; typora's cache is electron-produced with `--no-lazy` — a different
feature mix), in which case the honest stop is a recorded crash receipt for the exact version, which still
disposes the lead. [INFERENCE] the 13.6/15.0 crashes are feature-specific rather than version-universal;
that is the hypothesis this move tests.

## Move 3 — Synthetic BE carriers via freetz squashfs4-be-host (completes S108 branch coverage)

Move: build freetz-ng's `squashfs4-be-host` (PeterPawn lineage) in scratch to (i) synthesize plain
(non-AVM) BE v4 and AVM-quirk (`mkfs_time == bytes_used`) images, and (ii) stand up `unsquashfs4-avm-be`
as the independent oracle Move 1 lacks. S108's handler has BE branches none of the R36 carriers exercised:
`Endian.BIG, version 4` with `is_avm=True` (no `-be` flag), v1/v2/v3 BE (`sasquatch -be`), and the
vendor-mangled v3/v4 magics (`ddwrt_be`, `broadcom_be`, v4 `broadcom_be`). (a) Do-nothing cannot reach it:
upstream `mksquashfs` 4.7.5 has no endianness option (`-help-all` grep for endian/byte-order/swap is
empty), so BE images cannot be built by any held tool — a do-nothing control cannot even produce a carrier.
(b) Independent expected record: strong by construction — the synthetic source tree is the expected record
file-for-file, and for plain-BE v4 the kernel mount (proven on LE; expected to accept plain BE, [INFERENCE]
— the kernel's refusal was specifically on the AVM-BE layout) or freetz's own reader give a second lineage;
for the AVM-quirk image, freetz's reader is the oracle while sasquatch-v4be's no-flag path is the target.
(c) Feasibility: medium — `gcc 16.2.1`, `make`, `zlib.h`, `lzo/*` headers present; `xz.h` absent and pacman
is paused host-wide, so the xz/lzma dependency needs an official xz source release built in scratch
(allowed channel per `/home/vgpnk/.omp/agent/RULES.md`; no host service touched). Note the freetz
`AVM-BE-format.txt` (the very document S108 line 47 cites) confirms the quirk list this move would pin:
BE structures, XZ compression, LE block-length fields, `mkfs_time` := `bytes_used`. A v3-BE real-carrier
alternative exists (freetz identifies 7390 as BE v3), but this probe's 7390-06.88 download yielded **no**
standard squashfs superblock (BE or LE) — its tar `./var/tmp/filesystem.image` is 0 bytes and the full
17,725,440-byte image scan found no sane superblock, so a v3-BE real carrier needs a different
model/release and is higher-effort than the synthetic route.

---

## Evidence appendix (commands and outputs, copied before scratch removal)

- Tool inventory (no installs by this seat):
  `ls ~/.local/bin/sasquatch*` → `sasquatch`, `sasquatch-v4be` (both `-v` → "unsquashfs version 4.5.1");
  `mksquashfs -version` → 4.7.5; `7z` → 26.04; `node --version` → v24.21.0; `gcc --version` → 16.2.1;
  `/usr/bin/unsquashfs -h` has no `-be`/`-le` flag (grep exit 1) while `sasquatch -h` lists both.
- BE recognition probe (crafted 4,096-byte BE superblock, magic `73 71 73 68`):
  `/usr/bin/unsquashfs -s` → "Reading a different endian SQUASHFS filesystem … FATAL ERROR: Can't find a
  valid SQUASHFS superblock"; `sasquatch -s` and `sasquatch-v4be -s` both accept BE superblocks.
- LE kernel-oracle proof: `mksquashfs le-src le-test.sqsh` → `sudo mount -o loop,ro le-test.sqsh /mnt`
  (exit 0) → `cat /mnt/a.txt` → "hello"; `7z l` reports `Type = SquashFS`, `File System = SquashFS 4.0`,
  `Big-endian = -`.
- AVM-BE carrier: `curl -sI
  https://download.avm.de/fritzbox/fritzbox-7490/deutschland/fritz.os/FRITZ.Box_7490-07.62.image` → 200,
  `Content-Length: 41850840` (actual download 38,092,800 bytes — server omits chunked tail accounting;
  sha256 `2ab05656…` recorded above); `tar -tf` lists `./var/tmp/filesystem.image`;
  `od` head of filesystem.image → `73 71 73 68 00 00 00 69 02 16 30 42 …`; XZ stream magic at offset 96.
- AVM-BE oracle failures: kernel mount exit 32 ("Can't find a SQUASHFS superblock on loop0"); `7z l`
  → `Type = xz`, "There are data after the end of archive", `Offset = 96`, `Physical Size = 278964`;
  `sasquatch -be -d … filesystem.image` → "Block size and block_log do not match. File system is
  corrupt."; `sasquatch-v4be -d fs7490-be …` exit 0 → "created 10 directories / 86 symlinks", entries
  incl. `filesystem_core.squashfs` (magic `73 71 73 68`, sha256 `d0cae51a17e48c7517fa82e12d02274e…`).
- REA after-run: `PATH=$HOME/.local/bin:$PATH REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y
  rea-agents@6.5.0 extract-firmware fritz7490.image out7490 --max-output-files 100000
  --max-output-bytes 536870912 --format json` → exit 0, `evidence_id
  ev_b47413813259754b3fd1ec1e87259efb12659d24b48c524ce8f23a6d4cea2950`, engine unblob 26.6.4,
  `published_bytes 226964316`, 10,028 files, staged dir `0-35012608.squashfs_v4_be_extract/`, nested
  `filesystem_core.squashfs_extract/bin/{aicmd,allcfgconv,ar7cfgchanged,…}` present,
  `depth_limited_paths` = the nested core (default `--max-depth 3`), gaps = trailing 8-byte
  `unknown-chunk-handler` + `unpublished-entry` symlink-policy removals only, **no
  missing-extractor-dependency**. (Default budgets 10,000/268435456 are exceeded by this carrier — a
  round-37 claim must freeze non-default budgets.)
- REA control-run (do-nothing): `env -i PATH=/usr/bin:/bin REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob …`
  → exit 0, 11 files / 73,093,847 bytes: only tar members + carved `0-35012608.squashfs_v4_be` (35,012,608
  bytes) + `35012608-35012616.unknown`; gap
  `{"kind":"missing-extractor-dependency","handler":"squashfs_v4_be","dependencies":["sasquatch-v4be"]}`.
- `.jsc` facts: GitHub API `repos/xqy2006/jsc2js/releases` pages 1-7 scanned; 13.x/14.x live on pages 5-6;
  `releases/tags/14.8.178.14` → assets `d8-14.8.178.14-linux.tar.gz` (13,796,728) and
  `d8-14.8.178.14-windows.zip`; asset HEAD → 302 to release-assets. Round-35 prep captures
  (`.ufo/waves/round-35/prep/jsc-sources/releases-page{1,7}.json`, 177 tags: majors 9/11/12/15 only) are
  demonstrably incomplete for the 13/14 line. `corpus/knowledge/2026-10-13-r4-07-jsc-bytecode.md` pins
  typora cache to V8 `14.8.178.14-electron.0`, magic `0xC0DE06C3`, hashes `0x76842c11`/`0x00039fde`.
- BE build facts: `mksquashfs -help-all | grep -i "endian|byte.order|swap"` → empty; `ls /usr/include`
  → `zlib.h`, `lzo/` present, `xz.h` absent; `squashfs.ko.zst` present under
  `/lib/modules/$(uname -r)/kernel/fs/squashfs/`; `sudo -n modprobe squashfs` exit 0.
- 7390 negative result: `FRITZ.Box_Fon_WLAN_7390-06.88.image` (17,725,440 bytes, sha256
  `35cf96b6d9417c46bdf227a7b2beb0d9…`) tar lists `./var/tmp/filesystem.image` **0 bytes**; scans of the
  whole image and `plugins.update` found `sqsh` magic hits (kernel.image@0x15a500, plugins@0x400/0x52a00/
  0x53c00) all with insane superblock fields — no usable BE v3 carrier in that release.

## Disagreements / corrections to prior records (evidence-backed)

1. Round-35 prep capture gap (feeds R35-D4): the staged claim package's release inventory omits the 13.x
   and 14.x jsc2js releases; "no matching d8" was never stated in the lane, but any round-37 scoping off
   those captures alone would wrongly exclude the exact typora version. Corrected by live API scan above.
2. The round-36 lesson's `.jsc` lead is version-specific (13.6/15.0) and must not be generalized to
   "jsc2js d8 crashes on code caches"; the 14.8 case is untested, and the exact-version binary exists.
3. R36-C1's PROVINCE Core row says "`sasquatch-v4be` is its big-endian sibling, unmeasured" — this seat
   measured it on one real carrier in scratch (not a claim; no committed receipt). The `is_avm` branch
   remains unmeasured on both sides (False on 7490; no quirk-true carrier tested).
4. Kernel squashfs mount is a valid LE oracle but NOT a BE/AVM-BE oracle (mount exit 32); stating it as a
   general BE oracle would be wrong.

## Risks / second-order effects

- Move 1: 10000/268MB default budgets are exceeded → frozen claim must pin budgets or use a smaller
  carrier; the 8-byte trailing `unknown-chunk-handler` gap must be scoped out of the predicate (same class
  as R36-C1's trailing/padding handling); AVM firmware bytes are shipped-artifact authority — fine per
  QUALITY; the freetz build needed for (b) pulls a second extractor into the lane's trusted set (record
  tool/version/channel/reason per the 2026-10-19 directive; freetz-ng source via official GitHub release/
  tag only, pacman untouched).
- Move 2: d8 crash on 14.8 is a live possibility (two prior crashes are recorded); a crash is an honest
  stop, not a lane repair; View8 output is "semantic approximation" — any source-recovery claim must stay
  structural. Downloading a 13.8MB release binary from GitHub is an official-channel install → record it.
- Move 3: freetz build friction (xz headers) plus freetz images need lzma/xz; synthetic carriers must be
  byte-frozen with the full regenerating recipe (QUALITY #12).
- Cross-move: Moves 1 and 3 both append to the same PROVINCE/README Frontier lines — L1 should sequence
  them as one BE claim family or two separable claims; Move 2 touches the `.jsc` Frontier bullet and the
  SHONEN/SCORECARD `.jsc` rows (C2's counter reads those; restating counts after any landing is required).

## Verification statement

Everything above was exercised on-host today except where marked [INFERENCE] (kernel acceptance of plain
BE v4; version-specificity of the d8 crashes; freetz build success modulo xz headers). No frozen
predicate, counter, carrier, oracle, or lane file was touched. Nothing here lands data; it ranks moves and
copies the evidence into this report. Scratch removed after writing.
