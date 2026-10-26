# R38W2AvmProbe — AVM marker on a standard-BE SquashFS v4 body (frontier evidence for round 39)

**Verdict: FALSIFIED** — for the discriminator reading: `bytes_used == mkfs_time` is a header-only,
body-blind marker, and the `-be` drop it triggers destroys extraction of a plain big-endian gzip
image. The branch's literal mechanics are **CONFIRMED**: unblob 26.6.4 read the marker, removed
`-be`, and `sasquatch-v4be` then failed (exit 1, 0 files); REA published **0 bytes** with
`extraction_gap.kind = extractor-failure` while reporting `ok: true`. No claim, counter, carrier,
oracle or control was touched; this is frontier recon, not R38 claim data.

Seat: `R38W2AvmProbe` (leaf executor). Lane HEAD while working `e265533ea3a7cd4d9a75a24ef737c2ff0e98e95f`.
Scratch `S=/fast/scratch/hyaku/kaidoku-r38/R38W2AvmProbe`, `TMPDIR=$S`, removed at the end; everything
cited below is copied byte-exact into
`.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/` (manifest in §10). No VCS mutation (read-only
`git rev-parse`/`status`/`show` only), no installs or upgrades, no subagents, no background jobs,
no `agent://all`. One stray `unblob.log` that an early probe wrote into the lane root (unblob logs to
its cwd) was deleted; nothing else in the lane was written except this report and the artifact dir.

## 1. Marker mechanics and the two carriers

SquashFS v4 superblock, big-endian, 96 bytes (offsets documented in `make-avm-copy.py`; widths match
unblob's `squashfs4_super_block_t`, handler lines 468-492 of the pinned file):

| field | offset | width | K1 value |
|---|---|---|---|
| magic `sqsh` | 0 | 4 | `73717368` |
| inodes | 4 | 4 | 11 |
| **mkfs_time** | **8** | **u32** | `0x6553f100` = 1700000000 |
| block_size | 12 | 4 | 4096 |
| compression | 20 | 2 | 1 (gzip) |
| **bytes_used** | **40** | **u64** | `0x2634` = 9780 |

Copy made per the assignment: `python3 make-avm-copy.py K1/carrier.sqsh k1-avm.sqsh` sets
`mkfs_time := bytes_used` (big-endian u32 at offset 8), nothing else.

| carrier | bytes | sha256 | differs from parent |
|---|---|---|---|
| `k1-orig.sqsh` (byte copy of committed K1) | 9780 | `1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e` | — (matches `carriers.json` and `K1/after.json` subject digest) |
| `k1-avm.sqsh` | 9780 | `91be6f2897a8c859d27747153a7823e15c3703714ea493957087bf9884461df1` | offsets **8, 9, 10, 11** only |
| `k4-avm.bin` (K4 fixture, second family) | 307 | `59a8708d08089f225ed577cf27576f45f85f9513127cc081748fcf86f2f7fb66` | offsets 8-11 only; `mkfs_time` 1646222857 → 307 |

Post-patch parse: `mkfs_time=9780 bytes_used=9780 equal=True` (K4: 307/307/True).
Because `mkfs_time` is u32 and `bytes_used` u64 (handler lines 473 and 483), the marker is reachable
only when `bytes_used < 2**32`, i.e. never for images ≥ 4 GiB — struct-width reading, `[INFERENCE]`
beyond the two images measured. The generator already emits this carrier:
`tools/round-37/gen-squashfs.py <tree> out --endian avm` (line 173 `mkfs = bytes_used if e == 'avm'`)
produced **byte-identical** output (`sha256 91be6f28…`), and `--endian be` reproduces K1 byte-identical
(`1cfb6c33…`, `cmp` rc 0) — so the generator is deterministic and its `avm` mode is *marker-only*:
magic `sqsh`, everything big-endian (block lengths BE, not the LE block length S114 describes),
compression gzip (not XZ). See §6.

## 2. unblob drops `-be` — measured, and the consequence

`unblob 26.6.4`, PATH containing `~/.local/bin`, cwd `$S`:

```
unblob -v -e $S/unblob-k1-avm/out input/k1-avm.sqsh     # exit 0
unblob -v -e $S/unblob-k1-orig/out input/k1-orig.sqsh   # exit 0 (control)
```

Verbose log, AVM-marked (`unblob-k1-avm.log` lines 6-9):

```
Found valid chunk   chunk=0x0-0x2634 handler=squashfs_v4_be
Running extract command  command='sasquatch-v4be -no-exit-code -f -d …/k1-avm.sqsh_extract …/k1-avm.sqsh'
Extract command failed   __typename__=ExtractCommandFailedReport … exit_code=0x1 severity=WARNING stderr='U3F1…'
```

Control (`unblob-k1-orig.log` lines 6-9): same chunk `0x0-0x2634`, command
`'sasquatch-v4be -be -no-exit-code …'` (**`-be` present**), then
`Path traversal attempt through symlink, removing target=hello.txt`. Extraction dirs afterwards:
AVM-marked **empty**; control 5 regular files + 4 subdirectories.

So: the marker alone decides `-be`; the chunk offset/length are unchanged (`0x0-0x2634` both),
i.e. the marker does not alter carving, only the extractor argv. `-be` is appended at
`python/unblob/handlers/filesystem/squashfs.py:48-50` (`is_avm = header.bytes_used == header.mkfs_time`
/ `if not is_avm:` / `commands_args.append("-be")`). Installed copy sha256
`2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` = the S112 pin (590 lines), so the
S112 "lines ~45-50" locator is exact at 48-50. This is the landed entry's sentence confirmed literally.

## 3. What `sasquatch-v4be` does without `-be` on a standard-BE body

Same binary, direct argv, six cells (`sasquatch-*.{exit,stderr,stdout}.txt` artifacts):

| input | flag | exit | files | stderr (first line) |
|---|---|---|---|---|
| k1-orig | *none* | 1 | 0 | `SquashFS version [1024.0] / inode count [184549376] suggests a SquashFS image of a different endianess` |
| k1-orig | `-be` | 0 | 5 | `Reading a different endian SQUASHFS filesystem on …` (success) |
| k1-avm | *none* | 1 | 0 | identical to k1-orig without `-be` |
| k1-avm | `-be` | 0 | **5** | success, same 5 files |
| k4-avm | *none* | 1 | 0 | `… inode count [83886080] … different endianess` |
| k4-avm | `-be` | 0 | 4 | success (K4 oracle = 4 regular files) |

Reading: without `-be` it reads the header little-endian, prints the nonsensical 1024.0/184549376
values, then `read_id_table: failed to read id table block` and `FATAL ERROR: File system corruption
detected`, exit 1, publishes nothing. Forcing `-be` on the AVM-marked copy still extracts all 5 files,
which independently proves the patched bytes left the **body standard-BE gzip** — the failure is the
missing flag, not image damage. The effect is not K1-specific (K4 reproduces it at 307 B / 128 KiB
blocksize).

## 4. REA `extract-firmware` envelopes

```
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware input/k1-avm.sqsh  rea/k1-avm.out  --format json --full-output
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
  npx -y rea-agents@6.5.0 extract-firmware input/k1-orig.sqsh rea/k1-orig.out --format json --full-output
```

Both npx calls exit 0. Envelope fields that matter (`rea-k1-avm.json`, `rea-k1-orig.json`):

| field | AVM-marked | control |
|---|---|---|
| `ok` | true | true |
| `evidence_id` | `ev_b035737ad1a58ae428db9843f8f3ed0f8db197f9d2e29e01ec6fa72a73348afe` | `ev_90a0a2eb8ac50934963d866add7940e77828400571d6aa57c0d01950f7014a74` |
| `normalized_result.coverage` | partial | partial |
| chunk handler | `squashfs_v4_be` `0x0-0x2634` | `squashfs_v4_be` `0x0-0x2634` |
| `chunks[0].extraction_failed` | **true** | false |
| `extraction_gaps` | 1 × `extractor-failure` | none |
| gap continuation id | `7bca61a18c2e24f811bce926abefe387b4e009310796c1962f95828397e96f76` | — |
| `published_bytes` | **0** | 9656 |
| `normalized_result.files` | **empty list `[]`** | 5 (`bin/run`, `docs/deep/nested/file.dat`, `docs/readme.md`, `empty`, `hello.txt`) |
| diagnostics | `ExtractCommandFailedReport` (WARNING, exit_code 1) | `MaliciousSymlinkRemoved` (WARNING) |
| child command | `sasquatch-v4be -no-exit-code -f -d …` | `sasquatch-v4be -be -no-exit-code -f -d …` |

The control reproduces the committed K1 `after.json` on the two scoring quantities (`published_bytes`
9656, gap count 0), so the receipt shape is calibrated. The AVM child stderr decodes to exactly the
three lines in §3. REA's own `FileMagicReport` on the AVM input reads
`… created: Thu Jan  1 02:43:00 1970` — the marker is visible in `file(1)` output as a 1970 creation
date (a second, library-independent observable for round 39).

REA exposes no extractor-flag passthrough: `extract-firmware --help` lists only offset/length/depth/
budget options and `REA_UNBLOB_COMMAND` selects the unblob *binary* (`dist/firmware/FirmwareCommand.js`);
the observed child args are exactly the 13 fixed ones (`--process-num 1 --depth 3
--randomness-depth 0 --report … --log … --extract-dir … <input>`). Forcing `-be` therefore requires a PATH-level
extractor substitution or patching unblob — no REA knob exists.

## 5. Gap kinds are distinguishable — do not count them as one

Committed receipts and this probe give three different `extraction_gaps[].kind` values for the same
handler on BE v4 inputs:

| receipt | gap kind | cause |
|---|---|---|
| `corpus/evidence/round-38/c1/K1/before.json` | `missing-extractor-dependency` | `sasquatch-v4be` off the child PATH |
| `…/K2/after.json` | `unpublished-entry` (`…/var/lib/run-link`) | in-tree symlink kept as metadata |
| this probe (`k1-avm`) | `extractor-failure` (exit 1) | marker forced the no-`-be` argv |

A counter keyed on "gap count" cannot tell a PATH fault from a marker fault from a symlink; any
round-39 predicate that needs that distinction must read `kind` (and `chunks[].extraction_failed`).
The `dependencies` field separates the two failure kinds on its own: `["sasquatch-v4be"]` in the
before-arm gap, `[]` in this probe's `extractor-failure` gap.
`ok: true`, `exit 0` and `coverage: partial` held on the 0-byte AVM run, so none of the three is a
success signal.

## 6. Boundary of this probe (what it does NOT show)

- The marked carrier is **standard BE gzip with a marker**, not AVM-BE. S114 (`.ufo/waves/round-37/
  probes/avm.txt`) describes AVM-BE as XZ hardcoded, block length LE, `mkfs_time == bytes_used`;
  `gen-squashfs.py --endian avm` writes big-endian block lengths and defaults to gzip, so its `avm`
  mode is a marker-only fixture and cannot stand in for a real AVM image.
- No real AVM-BE carrier exists in the lane (round-38's own note says AVM was not measured). What
  unblob/sasquatch-v4be do to a genuine AVM body (LE block lengths + XZ, no `-be`) was **not**
  measured here; S114 says plain `-be` cannot decode it — that remains `[INFERENCE]` for our stack.
- The ≥ 4 GiB unreachability of the marker follows from u32/u64 widths, not from a 4 GiB image.
- The first-freeze `c1-counter.py` and the R38 predicates were read only as context; nothing here
  scores or judges R38-C1/C2.

## 7. Round-39 advisory (frontier only — no claim text proposed)

1. A carrier built with `gen-squashfs.py --endian avm` is a false-AVM marker fixture. Any round-39
   claim of the form "REA extracts AVM-BE" is unmeetable with it, measured: 0 files, 0 bytes,
   `extractor-failure`.
2. It is nevertheless a *good* behavioral carrier for the branch itself: the `-be` drop is observable
   directly (verbose log argv, REA diagnostics `command`), and the negative outcome is stable
   (K1 and K4 both reproduce it).
3. True AVM coverage still needs an image with LE block lengths + XZ. The lane has none and the
   generator cannot make one; without a real sample, round 39 can claim marker-branch behaviour but
   not AVM capability.
4. If round 39 wants to state the consequence for standard-BE images, the measured sentence is:
   a standard-BE v4 image whose `mkfs_time` equals `bytes_used` is misclassified, `-be` is dropped,
   and extraction yields 0 files with `extractor-failure` (K1 + K4 evidence).
5. Worth flagging to the scribe (advisory, corpus untouched): S112's `is_avm` sentence is correct as
   written; the body-blind consequence is the natural round-39 delta. Collision arithmetic is
   `[INFERENCE]`: `mkfs_time` is a Unix timestamp (~1.7e9 s for 2023-2026 builds) and `bytes_used`
   for a ~1.7 GB standard-BE image lies in the same range, so a chance equality is possible in
   principle; no collision was observed or searched for.

## 8. Tooling and limits

| tool | version | channel / digest |
|---|---|---|
| `unblob` | 26.6.4 | uv tool `~/.local/share/uv/tools/unblob` (`~/.local/bin/unblob` is a symlink to it); launcher sha256 `0ce7b624…`; handler sha256 `2d7b901b…` (= S112 pin) |
| `rea-agents` | 6.5.0 | `npx -y`; run as `extract-firmware … --format json --full-output` |
| `sasquatch-v4be` | unsquashfs 4.5.1 (2022/03/17) | pre-installed `~/.local/bin` by the L1 (not by this seat); sha256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` |
| `sasquatch` (LE) | 4.5.1 | sha256 `ad02d27a…`; not used in this probe |
| python3 | 3.14.8 | stdlib `struct` parse/patch only |

No installs or upgrades were made (pacman untouched, guard respected). Limits: Linux-only host; the
`REA_UNBLOB_COMMAND` staging dirs under `/tmp` were transient (REA deletes them) so the child
`stderr`/argv are cited from the committed envelopes, not from `/tmp`.

**Operational anomaly (observed twice, cause unspecified).** Invoking `sasquatch-v4be` **without**
`-be` directly from a non-interactive bash loop terminated the invoking shell: the run left its
`stderr` file behind but the following `echo $? > exit.txt` never ran, the loop stopped, and the
harness reported the whole command exited 1 with no output. The same failure wrapped in `( … )`
returned normally (`subshell rc=1`, shell survived), and the exit-0 `-be` runs never showed it. The
matrix in §3 was produced with the subshell wrapper and per-cell exit files. Round-39 runners that
expect a failing `sasquatch-v4be` should isolate it and record status to a file rather than trusting
`$?` in the same shell. `[INFERENCE]` this is signal/process-group behaviour of the onekey-sec 4.5.1
build; it was not diagnosed further.

## 9. Files written in the lane

- this report (`.ufo/waves/round-38/w2/R38W2AvmProbe.md`)
- `.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/` (§10)

Nothing else. `corpus/`, `PROVINCE.md`, `SCORECARD.md`, `SHONEN.md`, `LOG.md`, `tools/` untouched;
scratch `S` removed; the one stray lane-root `unblob.log` created by an early probe was deleted.

## 10. Artifact manifest (`sha256`)

```
91be6f2897a8c859d27747153a7823e15c3703714ea493957087bf9884461df1  k1-avm.sqsh
59a8708d08089f225ed577cf27576f45f85f9513127cc081748fcf86f2f7fb66  k4-avm.bin
93db89e39d0533346918ce4b0a0fbf442bc1fece77efd0e6610309d195fdb7f3  make-avm-copy.py
051fcca41df2e4141abf867a12e9a152e5f09da0fcc6f55c896862706d97cdf3  probe.sh
d1a2b501083db331367e65636507c57dc30317dfb47dfa10af2971af15ac11ff  summary.json
feb59a14e9a622f3432981cee7d25e85172324c341f6931b00fc23f3aa1537ca  rea-k1-avm.json
7433e31b1a11f0fe206228e61084346b69c70f280044b93f0c4a3daeb4414b8e  rea-k1-orig.json
594a5c69d816e5e7a2b8a5059a8fad56009aaa49addacd4a6944f9578f6a9c7e  rea-k1-avm.unblob-stdout.txt
e3c30a927c536586ac1ec707ac096ba48ac2a943e4d48801ef2bd2ce5185907d  rea-k1-orig.unblob-stdout.txt
e7a85494d16e44bf962dde4b6830f241d3059226a70daa8ccc11675f6f1293f9  unblob-k1-avm.log
288deafa0d4a94352e6d149ed2f3514d5397ddc32d2142354452ebc954a05b8c  unblob-k1-orig.log
27e5413e751d070a121ca6e02283b67ebdaee1b02a38eb5b350d6b771606827b  unblob-k4-avm.log
4355a46b19d348dc2f57c046f8ef63d4538ebb936000f3c9ee954a27460dd865  sasquatch-{k1-orig,k1-avm,k4-avm}-noflag.exit.txt
9a271f2a916b0b6ee6cecb2426f0b3206ef074578be55d9bc94f6f3fe3ab86aa  sasquatch-{k1-orig,k1-avm,k4-avm}-beflag.exit.txt
0397f828d787f784d16bcf247bd3d4aa4e7f4a2a5dc4e8915e8ed6353b6f9458  sasquatch-k1-orig-noflag.stderr.txt
0397f828d787f784d16bcf247bd3d4aa4e7f4a2a5dc4e8915e8ed6353b6f9458  sasquatch-k1-avm-noflag.stderr.txt
ced7bbbcb9c1129a195e7cc804c7683866586fca5b603130de2660c1ed4c1189  sasquatch-k4-avm-noflag.stderr.txt
0bb1d91f77a56c563f822eb194888ea62b05f3816e7b9807b442f9e1e14e4e2a  sasquatch-k1-orig-beflag.stderr.txt
f2ae526743b582bebd11d10c5b5391936ce83f6efc73a65bea99a19c02baede0  sasquatch-k1-avm-beflag.stderr.txt
b6feff522e14c1deb90aa9854b230d69ab819f1f9e4364125385a9311486c8e2  sasquatch-k4-avm-beflag.stderr.txt
1273387a9c064f29a45e2082f3f8db59f5f508459968d2e5796fead9cb4b1565  sasquatch-{k1-orig,k1-avm}-beflag.stdout.txt
a8386373a3372494a4ee94b96f90a15f3dfff6c6bdb34d08ba5751e0ad542095  sasquatch-k4-avm-beflag.stdout.txt
e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855  sasquatch-*-noflag.stdout.txt (empty)
```

Reproduce: `probe.sh` (reads `LANE`, uses a fresh `mktemp -d` scratch; the only tool assumptions are
those in §8). Artifacts are evidence for this report only; none of them is a scoring receipt.

Report: `.ufo/waves/round-38/w2/R38W2AvmProbe.md`
