# R39AssimAvmCritic — independent attack on the staged AVM assimilation entries

**Verdict: DEFECTS FOUND** — the staged AVM set's shared mechanism sentence ("the AVM marker is
invisible to unblob") is falsified by the pinned 26.6.4 handler and by the lane's own retained
bytes; three entries carry standing claims that later lane bytes overturn with no reversal
pointer; exactly one entry (`avm-image-extraction.md`) survives the QUALITY bar after re-grounding,
and it needs four small additions, not a rewrite.

Seat: critic (leaf). Lane corpus untouched; nothing written outside
`.ufo/waves/round-39/w1/R39AssimAvmCritic.md` and
`.ufo/waves/round-39/w1/artifacts/R39AssimAvmCritic/`. Scratch
`/fast/scratch/hyaku/kaidoku-r39/R39AssimAvmCritic` removed at exit. No tool installed; no pacman
transaction; `sasquatch`, `sasquatch-v4be`, `unblob` untouched. No REA call was made (bounds: no
REA on K5/K6 or held-out carriers; none was needed — the attack is on unblob/sasquatch behaviour).
Shokuknow read-only: the four lane images were hashed in place and **copied** into scratch; nothing
was written under `/home/vgpnk/Projects/shokuknow`. Read-only git only.

## Axes named (Godspeed)

| axis | what moves here |
|---|---|
| **depth** | a discriminating rule the corpus does not hold: `mkfs_time == bytes_used` is a *timestamp proxy*, the **metadata block-length endianness** is the format test. Two-direction misprediction measured. |
| **coverage** | which staged entry R39-C1 may cite for `squashfs_v4_be` in the Core row: one entry (E3) is admissible after re-grounding; four are not. |
| **calibration** | do the entries' own conclusions survive their own bytes: yes for E3/E6, no for E1/E2/E4/E5. |

## The strongest counterexample

`knowledge/corpus/knowledge/avm-firmware-image-unblob.md:75-77`

> "**The AVM marker is invisible to unblob**: it selects a handler on the magic and the endianness,
> never on the marker, so an AVM_LE image and a plain LE image of the same size and compression take
> the same path."

and its headline at `:16`, "it never notices the AVM marker at all".

The installed handler reads the marker and changes the command line with it —
`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`
(sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`), lines 41-52:

```python
        match endian, self.version:
            case Endian.BIG, 4:
                executable = self.V4BE_EXECUTABLE
                ...
                    is_avm = header.bytes_used == header.mkfs_time        # :48
                    if not is_avm:                                        # :49
                        commands_args.append("-be")                       # :50
```

The entry contradicts **itself**: its own table at `:67` prints the BE member's argv as
`sasquatch-v4be -no-exit-code -f -d {outdir} {inpath}` — the missing `-be` *is* the marker being
noticed. So the observation rows reproduce and the causal sentence beside them is false.

Reproduced on AVM's own firmware (sha256 `f518ce6b…`, see E4), unblob 26.6.4:

```
Running extract command  command='sasquatch-v4be -no-exit-code -f -d 0-5443584.squashfs_v4_be_extract …'
Running extract command  command='sasquatch -le -no-exit-code -f -d 0-28200960.squashfs_v4_le_extract …'
```

Smallest safe correction (E4): distinguish **handler selection** (marker-independent: magic +
endianness only) from **extractor-argument selection** (marker-dependent on the BE-v4 path). Then
the LE/BE pairing sentence at `:75-77` is right for LE and wrong as written for BE.

### The counterexample the corpus cannot state today

Eleven images, one classifier (`artifacts/probe-marker-vs-format.py`, output `artifacts/matrix.tsv`,
`python3 -I -B … `, exit 0). `marker` = `mkfs_time == bytes_used`; `len` = the 2-byte metadata block
header at `inode_table_start` decoded both ways, `0x8000` masked.

| image | magic | comp | marker | hdr | len LE / BE | length endianness | unblob 26.6.4 argv | measured outcome |
|---|---|---|---|---|---|---|---|---|
| round11 `avm-be.squashfs` (**genuine AVM-BE**) | `sqsh` | 4 xz | **yes** | `7400` | 116 / 29696 | **LE** | no `-be` | 4 files ✓ |
| round13 `avm-le-genuine.squashfs` | `hsqs` | 4 xz | yes | `7000` | 112 / 28672 | LE | `-le` | 4 files ✓ |
| round9 `sqimg-avm-probe.bin` (marker-only) | `sqsh` | 1 gzip | yes | `003a` | 14848 / **58** | **BE** | no `-be` | **0 files, exit 1** |
| round12 `avm-le.squashfs` (stale build) | `hsqs` | 4 | no | `7400` | 116 | LE | `-le` | 4 files ✓ |
| round37 K1 `carrier.sqsh` | `sqsh` | 1 | no | `817c` | 31873 / **380** | BE | `-be` | 5 files ✓ |
| round37 K4 `carrier.bin` | `sqsh` | 1 | no | `003a` | 14848 / **58** | BE | `-be` | 4 files ✓ |
| **fresh** `carrier-be.sqsh` (`--endian be`) | `sqsh` | 1 | no | `8137` | 14209 / **311** | BE | `-be` | 3 files ✓ |
| **fresh** `carrier-avm.sqsh` (`--endian avm`) | `sqsh` | 1 | **yes** | `8137` | 14209 / **311** | **BE** | no `-be` | **0 files, exit 1** |
| **fresh** `avm-be-markerstripped.sqsh` | `sqsh` | 4 | **no** | `7400` | 116 / 29696 | **LE** | **`-be`** | **0 files, exit 1** |
| AVM 07.57 BE member | `sqsh` | 4 xz | yes | `6405` | 1380 / 25605 | LE (plausibility) | no `-be` | 2942 files ✓ |
| AVM 07.57 LE member | `hsqs` | 4 xz | yes | `7c07` | 1916 / 31751 | LE | `-le` | 6912 files ✓ |

Direct `sasquatch-v4be` matrix (no unblob), `artifacts/sasquatch-matrix.txt`:

```
avm-be.squashfs        noflag exit=0 files=4      -be exit=1 files=0
sqimg-avm-probe.bin    noflag exit=1 files=0      -be exit=0 files=4
carrier-avm.sqsh       noflag exit=1 files=0      -be exit=0 files=3
```

So the marker mispredicts **in both directions**: a marker-true standard-BE body loses its `-be`
and the extractor dies loudly; a genuine AVM-BE with the timestamp normalised is given `-be` and
dies equally loudly, while `sasquatch-v4be` **without** `-be` still extracts it (exit 0, 4 files).
The load-bearing difference is the block-length endianness, exactly Freetz's own bullet
(S114 lane / S192 merged: "the only data field stored in the little-endian format is the block
length value at the beginning of each block"), byte-confirmed here for the first time on a
retained genuine image.

For the two 4096-byte fixtures the test is exact (`len + inode_table + 2 == dir_table`):
`121+2+116 = 239` = `dir_table` on the genuine AVM-BE, while the BE reading gives `29819`;
`121+2+58 = 181` on the marker-only probe, while the LE reading gives `14971`. On the real
firmware members the inode table spans more than one metadata block, so that identity no longer
holds and only plausibility separates them (1380 vs 25605) — the classifier states which signal it
used, and this is the limit of the cheap test.

**Round-39 consequence (C1).** `tools/round-37/gen-squashfs.py --endian avm` is **byte-identical**
to `--endian be` with bytes 8..12 overwritten by `bytes_used`:

```
gen-squashfs.py tree carrier-be.sqsh  --endian be   -> sha256 103649e6cd3f088b88404c9b23fc80da9c5ef901cffb562a83cf627cf3a9b16b
gen-squashfs.py tree carrier-avm.sqsh --endian avm  -> sha256 762c06a68db24b316387f20ed9ea3bc8304f19eb5977109f49b6e9c6219ff001
carrier-be patched at 8..12 to bytes_used           -> sha256 762c06a68db24b316387f20ed9ea3bc8304f19eb5977109f49b6e9c6219ff001  (0 differing bytes)
```

The generator's `avm` mode is the doctored-marker transform, not the AVM layout (it cannot write
LE block lengths). K5/K6 must therefore be built `--endian be` (or from vendor bytes); using
`--endian avm` would put a marker-only carrier into a standard-BE claim and would teach the
equivalence the corpus is wrong about.

## Per-entry verdicts

Every `source:` id resolves: `SOURCES.append.md` holds 132 rows, S106–S237, including S189–S223, and
each AVM entry appears in the `used-by` cells of its own rows (6 / 3 / 2 / 3 / 2 occurrences
respectively; spot-checked: S200/S201 → `avm-image-extraction.md`, S206/S207 →
`avm-le-variant-reachability.md`, S216–S223 → `avm-firmware-image-unblob.md`). The `own-work`
rows name `lanes/kaidoku/roundNN/work/*.tsv`, and those ten files exist on this host under
`/home/vgpnk/Projects/shokuknow/lanes/kaidoku/` (read-only). What the rows do **not** carry is a
digest for the retained image, so QUALITY #4 fails at row level for all four image-bearing entries;
the sha256s below close that gap.

### E1 `sasquatch-unblob-avm-branch.md` — mechanism CONFIRMED, standing conclusion FALSIFIED

- Weakest claim: `:2` / `:14` "a real AVM image still needs a tool this host does not have", with
  `:39` "**What is still open.** A real AVM image."
- Test: the lane holds one — `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs`,
  4096 B, sha256 `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32`. unblob 26.6.4 →
  handler `squashfs_v4_be`, argv without `-be`, 4 files (`apple`/`banana`/`cherry`/`date`).
- Falsified. The branch-logic half holds exactly at 26.6.4 (`:48-49` above), so the entry's *core
  mechanism* is confirmed; only its open lead is stale by two rounds.
- Second defect: `S189` names `unblob/main`, an unpinned branch (QUALITY #8). The decision lines are
  byte-equal at 26.6.4, so nothing is wrong today — but the row should be re-pinned to the tag with
  the installed digest `2d7b901b…`.
- Smallest correction: append one sentence — "closed in round 11: … `avm-be.squashfs`, sha256
  `c7f74691…`, extracts 4 files through the no-`-be` argv" — and re-pin S189.

### E2 `avm-image-build-blocker.md` — FALSIFIED (stale standing claim), and one bad number

- Weakest claim: `:2` "A real AVM image is one release away", `:14` / `:39` "it is gone", on twelve
  404s.
- Test: the next round's own row records the working path —
  `round11/work/lead1-avm-image.tsv: source_tarball_url https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz`,
  `source_tarball_md5 d92ab59aabf5173f2a59089531e30dbf` (Freetz's pin) — and the image built from it
  is retained and extracts (E3).
- Falsified. QUALITY #35/#36: the reversal is recorded only as prose inside a *different* entry that
  never names this file, so the rejected decision is not locatable from the admitting row and the
  admitting row is not locatable from this one. This entry must become a reversal record, not remain
  a standing "gone" claim.
- Independent defect (`:43-44`): it presents `mkfs_time 4 036 090 986` against
  `bytes_used 7 854 559 225 110 855 680` as a superblock reading. That `bytes_used` is 7.85 EiB
  (`0x6d01000000000000`) inside a 4096-byte image — a misparse read as a measurement. The entry's
  inference (the marker is a creation property, not a compression property) is right; the supporting
  field is not. Label it a misread or drop it.

### E3 `avm-image-extraction.md` — CONFIRMED (the survivor)

- Weakest claim: `:10` "The answer is **yes**" — a real AVM-BE builds and extracts.
- Test: re-ran unblob 26.6.4 on the retained bytes (sha256 `c7f74691…`) from scratch:
  `Found valid chunk chunk=0x0-0x1000 handler=squashfs_v4_be`;
  `Running extract command command='sasquatch-v4be -no-exit-code -f -d …'`; extracted 4 files,
  contents `apple` / `banana` / `cherry` / `date`. The entry's argv and file list reproduce exactly.
- Confirmed. Residual gaps against the bar: no image digest/path (#4), no tool pins (#8), no
  statement of what was not examined (#7), and its generalisation caveat omits the only failure
  direction that matters (marker without the layout).
- Smallest correction (this is the one entry to re-ground, not rewrite): add (a) absolute path +
  sha256 `c7f74691…`; (b) `unblob 26.6.4` (handler sha256 `2d7b901b…`) + `sasquatch-v4be 4.5.1` +
  the verbatim argv; (c) one sentence: the `-be`-dropping branch keys on `mkfs_time == bytes_used`
  and therefore also fires on a standard-BE body with a normalised timestamp, where extraction
  fails (measured: `carrier-avm.sqsh`, 0 files, exit 1); (d) keep "one directory, four files".

### E4 `avm-firmware-image-unblob.md` — headline FALSIFIED, measurements reproduce

- Weakest claim: `:16` and `:75-77`, the "invisible to unblob" pair — see the counterexample above.
- Reproduction of the rest, from a fresh 39.7 MB download of
  `https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image`
  (HTTP 200, 39 741 440 B, sha256 `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`
  — **equal** to the row's recorded digest):
  - BE member `sqsh`, mkfs 5 442 392 == bytes_used 5 442 392, comp 4 (xz);
  - LE member `hsqs`, mkfs 28 200 029 == bytes_used 28 200 029, comp 4 (xz);
  - unblob: outer `tar`, then `squashfs_v4_be` **without** `-be` and `squashfs_v4_le` with `-le`;
  - whole-image `find -type f` count = **9877**, exactly the recorded total.
- The sentence at `:69` "9 877 files in all" attaches the whole-image total to the two filesystems.
  It reconciles exactly — 6 912 + 2 942 + 2 carved squashfs images + 21 outer/member artifacts
  (kernel images, `initramfs`, `var/*`, `filesystem.image` members) = 9 877 — but as written it
  imputes the outer set to the trees. My recursive walk inside each `…_extract` directory gives
  6 913 / 2 943 (each includes its own carved image): consistent, and the +1 each is explained by
  the carve, not a discrepancy.
- Verdict: measurements confirmed; the causal sentence falsified and self-contradicted. Salvageable
  by the handler-vs-argv narrowing; the 1970-date fingerprint at `:71-73` is a genuinely good cheap
  test and survives.

### E5 `avm-le-variant-reachability.md` — FALSIFIED (superseded without a pointer)

- Weakest claim: `:2` "The second AVM variant is **not reachable** as an AVM image through the recipe
  the lane holds".
- Test: `round13/work/avm-le-genuine.squashfs`, 4096 B, sha256
  `18d3ad0563cce852a438fe414d881909a6097fc30a38ca523372931cfcafaee4` — `hsqs`, mkfs 361 ==
  bytes_used 361, comp 4; unblob → `squashfs_v4_le`, `-le`, 4 files.
- Falsified. The entry's body already names the closing route (`AVM_FORMAT_AS_OPTION`), and its
  surviving value is the filename-vs-define correction (`AVM_BE_AVM_LE` is a patch filename, not a
  define value; `AVM_LE`=2, `AVM_BE`=3) — confirmed by S206. Its sibling
  `avm-le-image-genuine-marker.md` overturns it in prose without naming this path: a reversal with no
  two-way pointer (QUALITY #35/#36).
- Smallest correction: append a reversal line naming this file as the rejected decision, with the
  flip evidence (round13 image + sha256) and the flip condition already met.

### E6 `avm-le-image-genuine-marker.md` — CONFIRMED (scope: LE only)

- Weakest claim: `:30` "the marker is invisible to it [unblob]".
- Test: true in scope — the LE branch of the handler appends `-le` unconditionally and never reads
  the marker; measured `squashfs_v4_le` / `sasquatch -le` on the genuine LE image, 4 files. Its own
  limit sentence — "it does not say unblob *recognises* the AVM marker" — is the correct formulation
  and is the one E4 contradicts.
- Confirmed. Needs only the digest/path/pin additions (and to be the entry E4 is narrowed toward).

## Which entry would survive the QUALITY bar after re-grounding

**`avm-image-extraction.md` (E3), and only it.** Score against the admission rows:

| # | E3 today | after the four additions |
|---|---|---|
| 1 resolvable source | row resolves (S200/S201 → existing TSV) | unchanged |
| 2 falsifiable | yes ("builds and extracts") | yes |
| 3 domain-specific | yes | yes |
| 4 absolute path + stable identity | **fails** (relative path, no digest) | path + `c7f74691…` |
| 5 observation/inference labels | mixed | one limit sentence added |
| 7 names what was not examined | **fails** | "one directory, four files; no vendor firmware" |
| 8 versions pinned | **fails** | unblob 26.6.4 + sasquatch-v4be 4.5.1 |
| 12 byte-exactness | recipe + tarball md5 retained; image built, not re-synthesised | unchanged, stated as such |
| 35/36 reversal traceability | n/a | n/a |

E4 after the narrowing would also be admissible, but it is a retraction of its own headline — that is
a rewrite, not a re-grounding. E1 needs a retraction plus a re-pin. E2 and E5 are reversal records.
E6 is already admissible modulo the digest, but it carries no round-39 surface: R39-C1's Core row is
about `squashfs_v4_be`, which E6 does not address.

If the L1 prefers E4 as the citation (it is the richest entry, and its measurement rows reproduce
exactly on the sha-pinned 07.57 image), it survives only as a **rewrite whose headline and causal
sentence are retracted**; E3 is the only entry that survives with additions alone. Both paths land on
the same corrected statement, so the choice is editorial, not factual.

## Feed-forward to the freeze

1. **R39-C1**: all six carriers are standard BE v4; none may carry the marker. K5/K6 built with
   `--endian be` (or vendor fixtures). Add one line to the claims' carrier note: `gen-squashfs.py
   --endian avm` is the marker transform on a standard-BE body (byte-identical, sha256 `762c06a6…`)
   and is therefore barred from C1 carriers. The Core row may cite E3 only after the four additions.
2. **R39-C2**: the class `avm-marker-be-dropped` is correctly named. Define it as
   `marker == yes ∧ metadata length endianness == BE`, and key the table row on the block-length
   field, not on `mkfs_time == bytes_used` — otherwise the table mislabels a genuine AVM-BE (which
   unblob extracts fine) as broken and a marker-only image as AVM. Two extra rows earn their keep:
   `avm-layout-be-flag-passed` (genuine layout, timestamp normalised → 0 files, exit 1) and
   `ok:true-with-zero-output` (unblob exits 0 on `ExtractCommandFailedReport`; REA reports
   `ok: true`, `published_bytes: 0`, `coverage: partial`). A counter-class control must assert that
   the retained genuine AVM-BE is **not** labelled `avm-marker-be-dropped`.
   **Do not key on the stderr sentence** "suggests a SquashFS image of a different endianess": on the
   genuine AVM-BE it is printed by a run that succeeds (`sasquatch-v4be` noflag: exit 0, 4 files,
   first stderr line is that sentence) and by one that fails (`carrier-avm.sqsh` noflag: exit 1,
   0 files, same sentence). Only exit code plus extracted-entry count separates them.
3. **Held-out generation**: `heldout-gen.py` can generate the marker class but cannot generate a
   genuine AVM-BE (no LE-block-length writer on this host). The class list as drafted is therefore
   right; do not rename `avm-marker-be-dropped` to anything implying a real AVM image.

## Evidence (commands, outputs, exit codes)

```
# handler bytes (pinned)
sha256sum .../site-packages/unblob/handlers/filesystem/squashfs.py
  -> 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287
grep -n "is_avm\|mkfs_time\|bytes_used" <same>   -> 48: is_avm = header.bytes_used == header.mkfs_time ; 49: if not is_avm
unblob --version -> 26.6.4 ; sasquatch-v4be -version -> unsquashfs version 4.5.1 (2022/03/17); python3 -V -> 3.14.8

# fresh carriers (scratch tree: bin/run, etc/a.txt, docs/deep/blob.bin, symlink docs/deep/link-ok)
python3 tools/round-37/gen-squashfs.py tree carrier-be.sqsh  --endian be  --comp gzip   # 5610 B
python3 tools/round-37/gen-squashfs.py tree carrier-avm.sqsh --endian avm --comp gzip   # 5610 B
# marker-patch identity
python3 (patch be[8:12] := bytes_used)  -> sha256 762c06a6… == carrier-avm.sqsh, 0 differing bytes

# unblob direct, cwd = scratch (unblob writes unblob.log into cwd)
unblob -v -e ub-carrier-be  carrier-be.sqsh    # exit 0; argv 'sasquatch-v4be -be …'; 3 files
unblob -v -e ub-carrier-avm carrier-avm.sqsh   # exit 0; argv 'sasquatch-v4be …' (no -be); ExtractCommandFailedReport exit_code=1; 0 files
unblob -v -e u2-avm-be avm-be.squashfs         # exit 0; squashfs_v4_be; no -be; 4 files
unblob -v -e u2-avm-le-genuine avm-le-genuine.squashfs  # exit 0; squashfs_v4_le; -le; 4 files
unblob -v -e u2-sqimg-avm-probe sqimg-avm-probe.bin    # exit 0; no -be; ExtractCommandFailedReport; 0 files
unblob -v -e u3 avm-be-markerstripped.sqsh     # exit 0; -be chosen; ExtractCommandFailedReport; 0 files;
                                               # same bytes with sasquatch-v4be noflag: exit 0, 4 files

# vendor firmware (sha-pinned, re-run to reconcile E4's counts)
curl -sS -m 200 -o fw.image https://download.avm.de/fritzbox/fritzbox-6490-cable/other/fritz.os/FRITZ.Box_6490_Cable-07.57.image
  -> http=200 bytes=39741440  sha256 f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d
unblob -v -e fw-out fw.image   # exit 0; tar -> elfs -> squashfs_v4_be (no -be) + squashfs_v4_le (-le) + nested tar/cpio/gzip
find fw-out/fw.image_extract -type f | wc -l   -> 9877
```

Limits: `sasquatch`/`sasquatch-v4be` 4.5.1 layout detection was not re-derived from source (only
exercised); the Freetz 4.3 toolchain was not rebuilt (the retained images stand in); the
`--endian avm` identity is proven for `tools/round-37/gen-squashfs.py` at the round-37 revision
only; the firmware re-run used the recorded URL and pin, not a second mirror; no REA call, so no
envelope-level claim is made here beyond re-reading the committed round-38 receipts.

## Artifacts (this seat's directory)

`probe-marker-vs-format.py` (classifier, exit 0/1, states which signal it used) · `matrix.tsv`
(11 images) · `sasquatch-matrix.txt` · `carrier-be.sqsh`, `carrier-avm.sqsh`,
`avm-be-markerstripped.sqsh` (fresh bytes, cited above) · `unblob-u2-avm-be.log`,
`unblob-u2-avm-le-genuine.log`, `unblob-u2-sqimg-avm-probe.log`, `unblob-ub-carrier-be.log`,
`unblob-ub-carrier-avm.log`, `unblob-u3.log` · `avm-firmware-squashfs-argv.txt` (extractor argv on
AVM's own firmware). The 4.2 MB verbose firmware log was not retained (size); its two squashfs
extractor lines are in `avm-firmware-squashfs-argv.txt`.
