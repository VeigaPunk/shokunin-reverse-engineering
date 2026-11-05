source: S110 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md — tag 26.6.4 (commit 1fcc7a0a584a70a96c31f5a276c20944d199a089), 235 lines, sha256 6544d60f22f7b521f8705b3bba5d47a50e428ccbd3359542708dbd009ccf3716, byte-identical to HEAD on 2026-10-26; line 49 "For SquashFS support, also install [sasquatch](https://github.com/onekey-sec/sasquatch):"
source: S111 — https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md — branch master, 30 lines, sha256 f09961ee6c2bf5ddadc0c7e52bdfb68e50c877cabec20ec0370f54c311e01fef; line 12 "Very beta."; line 17 build prerequisites; line 26 build.sh downloads squashfs-tools v4.3
verified-at: 2026-10-26 (both READMEs re-opened by the lane this round; access 2026-10-26T04:36:42Z, wave-1 seat `.ufo/waves/round-36/w1/R36ScribeAssimilationGate.md` §2.3)
recheck: 180d — `curl -fsSL https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md | sha256sum` → `6544d60f…3716`; a different digest means the tag moved and the entry is re-read

# On unblob's pip install route, SquashFS support is a declared dependency on an external sasquatch extractor

Assimilated in round 36 from the shokuknow `corpus-expansion-1` package (`merge/kaidoku/knowledge/corpus/knowledge/unblob-sasquatch-dependency.md`, staged 2026-10-23) and re-grounded by the lane: both sources re-opened on 2026-10-26, pinned by tag/commit and sha256, staged ids renumbered by document (staged S106 → S110, staged S107 → S111). Three corrections were applied before admission (round-36 lesson `## Gate`, decision 1): pins by document instead of a floating `HEAD`; inference labelled and the host-state sentence re-scoped; the unsupported "fork" provenance wording dropped.

**Claim (producer contract, pip route).** On its pip install route unblob's own README makes SquashFS
support conditional on an external extractor: "For SquashFS support, also install
[sasquatch](https://github.com/onekey-sec/sasquatch):" (S110, line 49), inside the block that line 43
opens with "Then install the required external extractor tools. On Ubuntu/Debian:". The step belongs to
the pip route only: the README's Docker route bundles every extractor (line 64) and its Kali route is a
single `apt install unblob` (lines 77-79). The README fetches sasquatch as a prebuilt `.deb` release asset
from onekey-sec's GitHub release (not a distribution package), so a packaged route exists beside a source
build. (Scope corrected in wave 2: `.ufo/waves/round-36/w2/R36W2ScoutS110.md` D1, D3.)

**What sasquatch says about itself (S111).** A patch set over the standard `unsquashfs` that targets
vendor-modified SquashFS (header mutations, changed LZMA options), self-described as "Very beta."
(line 12). Its source build needs a C/C++ compiler plus the liblzma, liblzo and zlib development
libraries (line 17), and `build.sh` downloads squashfs-tools **v4.3**, patches it and builds (line 26).
The packaged onekey-sec binary the lane installed reports `unsquashfs version 4.5.1 (2022/03/17)`
(`corpus/evidence/round-36/c1/K1/after-run.json`), so the two routes are built on different
squashfs-tools bases; this entry does not claim they behave identically.

**Consequences for the lane.**

1. Observed: the missing-dependency path is unblob's design. On this host REA `extract-firmware`
   reports it as `extraction_gaps[].kind = missing-extractor-dependency`, `dependencies = [sasquatch]`
   (`corpus/evidence/round-36/c1/K*/before.json`), and the gap disappears once a sasquatch binary is on
   `PATH` (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`).
2. [INFERENCE] The devttys0 sasquatch README (S111) says its LZMA handling "will attempt to automatically
   resolve" vendor changes by brute force (lines 6-8) and labels the tool "Very beta." (line 12); that label
   is devttys0's, not unblob's or onekey-sec's, and the lane runs the onekey-sec package. A failed or
   partial SquashFS extraction is therefore not by itself evidence that an image holds no SquashFS; read the
   chunk records and gaps first. (Attribution corrected in wave 2: `R36W2ScoutS110.md` D2, `R36W2ScoutS111.md` item 7.)
3. Host-state scope: the staged text's "sasquatch is absent on this host" was true at the package's
   2026-10-23 snapshot and is false from 2026-10-26 (`~/.local/bin/sasquatch`, sha256
   `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`, installed by the round-36 L1
   from the official `sasquatch_1.0_amd64.deb`; `unblob --show-external-dependencies` lists
   `sasquatch ✓`, `sasquatch-v4be ✓`).
4. The Frontier phrase "AUR-only" (`PROVINCE.md` `### Round-4 frontier (post-unlock)`) described one
   packaging route; S110 shows the producer-documented Debian-package route.

**Not claimed.** No statement about vendor-mangled or big-endian images, about the devttys0 build's
behaviour, or that the onekey-sec package is a fork of devttys0 (neither README says so).
