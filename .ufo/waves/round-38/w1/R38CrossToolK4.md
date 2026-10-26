# R38CrossToolK4 — cross-tool oracle reproduction for C1 carriers (independent of REA)

Role: leaf executor, round 38 wave 1. Scope: reproduce the R38-C1 oracle comparison with
`~/.local/bin/sasquatch-v4be -be` for **all four** frozen carriers (K1..K4; the seat text names
K4, and the oracle row set covers K1..K4), and confirm 7-Zip refuses each BE image with the
verbatim error text for the lesson `## Gate`. No claim predicate, counter, carrier or oracle was
changed. No REA run was made (this seat is the non-REA leg).

Lane HEAD at the time of work: `cb4326b2aa4c2024af0651fe6115b82d0c4de3df` (`git rev-parse HEAD`,
read-only). `git status --porcelain` before writing this report listed only the untracked wave
dirs `assimilation/`, `w1.ready`, `w1/` — no tracked-file modification by this seat.

## 1. Tool inventory (recorded per operator tooling directive)

| tool | version | channel | digest / note |
|---|---|---|---|
| `sasquatch-v4be` | `unsquashfs version 4.5.1 (2022/03/17)` (onekey-sec BE build) | pre-installed by L1 in `~/.local/bin` (official onekey-sec deb); not installed/upgraded by me | sha256 `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` |
| `sasquatch` (LE) | `4.5.1 (2022/03/17)` | same | negative control only |
| `unsquashfs` | `4.7.5 (2026/03/01)` | distro (`/usr/bin/unsquashfs`) | negative control only |
| `7z` | `7-Zip 26.04 (x64) 2026-10-05` | distro | refusal evidence |
| `unblob` | `26.6.4` | `~/.local/bin/unblob` (uv tool) | direct CLI run for handler-name corroboration (not REA) |
| `rea-agents` | `6.5.0` (package.json) | npx cache | read only, never invoked by this seat |

No installs, no upgrades, no pacman. All extraction, fixtures and unblob output lived in
`S=/fast/scratch/hyaku/kaidoku-r38/R38CrossToolK4` with `TMPDIR=$S`; `S` is removed
(`ls -d $S` → "No such file or directory"). Nothing cited below lives in scratch: every cited
listing was copied into
`.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/` before cleanup.

Carrier pins recomputed from committed bytes and matched against the frozen manifest
`.ufo/waves/round-38/c1/carriers.json` — all four agree:

```
1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e  K1/carrier.sqsh
403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154  K2/carrier.sqsh
9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0  K3/carrier.bin
a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed  K4/carrier.bin
```

`file(1)` on each: `Squashfs filesystem, big endian, version 4.0, zlib compressed` (K1 9780 B /
11 inodes; K2 1606 B / 10 inodes; K3/K4 307 B fs / 5 inodes, block size 131072). Byte check of
the BE v4 superblock at offset 0 for K3/K4: magic `73717368`, `s_major/s_minor` `0004/0000`,
block_size `00020000`, compression `0001`.

## 2. Result — cross-tool extraction matches every oracle

Command per carrier (`C=corpus/evidence/round-37/c1`):

```
~/.local/bin/sasquatch-v4be -be -d "$S/out/$k" "$C/$k/carrier.{sqsh,bin}"
cd "$S/out/$k" && find . -type f -printf '%P\0' | LC_ALL=C sort -z \
  | while IFS= read -r -d '' f; do printf '%s\t%s\t%s\n' "$f" "$(sha256sum -- "$f"|cut -d' ' -f1)" "$(stat -c%s -- "$f")"; done
diff -u "$C/$k/oracle.tsv" <listing>
```

| carrier | extractor exit | oracle rows | extracted rows | path+sha+size diff | symlinks | dir set | oracle vs source tree |
|---|---|---|---|---|---|---|---|
| K1 | 0 | 5 | 5 | **identical** | `link-to-hello -> ../hello.txt` identical | 4 = 4 identical | **identical** (`K1/oracle.tsv` == `K1/src`) |
| K2 | 0 | 3 | 3 | **identical** | `var/lib/run-link -> ../../a/run.sh` identical | 5 = 5 identical | **identical** (`K2/oracle.tsv` == `K2/src`) |
| K3 | 0 | 4 | 4 | **identical** | none in image | — | n/a (oracle = apple1..4) |
| K4 | 0 | 4 | 4 | **identical** | none in image | — | n/a (oracle = apple1..4) |

- 16/16 oracle rows match on relative path, sha256 **and** size; `diff` was bidirectional, so
  there is no extra regular file in any extraction and no missing one.
- The comparison is on exact relative paths, i.e. stricter than the predicate's "same
  relative-path suffix".
- Extractor self-report: K1 `created 5 files / 5 directories / 1 symlink`; K2 `3 files / 6
  directories / 1 symlink` (the sixth directory is the `-d` output root, not an image entry —
  `find -mindepth 1 -type d` on the extraction gives 5, equal to `K2/src`); K3/K4 `4 files / 1
  directory`.
- Lane harness agreement: `tools/round-38/c1-run.sh oracle <carrier> <out>` returns rc=0 and
  stdout byte-identical to each `oracle.tsv` (4/4), with empty stderr. Artifacts
  `harness-oracle-K{1..4}.tsv` + raw `sasquatch-v4be-K{1..4}.tsv` are the same bytes.

## 3. Negative controls — the `-be` path is load-bearing

| reader | K1 | K2 | K3 | K4 |
|---|---|---|---|---|
| `unsquashfs -l` 4.7.5 | rc=1 | rc=1 | rc=1 | rc=1 |
| `sasquatch` (LE 4.5.1) | rc=1 | rc=1 | rc=1 | rc=1 |
| `sasquatch-v4be` **without** `-be` | rc=1 | rc=1 | rc=1 | rc=1 |

`unsquashfs` 4.7.5: `Reading a different endian SQUASHFS filesystem on <carrier>` /
`FATAL ERROR: Can't find a valid SQUASHFS superblock on <carrier>`.
`sasquatch` LE and `sasquatch-v4be` sans `-be`: `SquashFS version [1024.0] / inode count
[184549376] suggests a SquashFS image of a different endianess` (K2 `167772160`; K3/K4
`83886080`), then `read_id_table: failed to read id table block` (v4be) or `Reading a different
endian SQUASHFS filesystem` (sasquatch). Full text in `artifacts/unsquashfs-refusal.txt`.

## 4. 7-Zip refusal — verbatim text for the `## Gate`

All four carriers, `7z l <carrier>`, exit code **2**, identical shape. Path varies only:

```
7-Zip 26.04 (x64) : Copyright (c) 1999-2026 Igor Pavlov : 2026-10-05
 64-bit locale=en_US.UTF-8 Threads:32 OPEN_MAX:524288, ASM

Scanning the drive for archives:
1 file, 9780 bytes (10 KiB)

Listing archive: <carrier>


ERROR: <carrier> : Cannot open the file as archive



Errors: 1
```

K1 9780 B / K2 1606 B / K3 4096 B / K4 307 B — `7z_exit=2` for each; the last error line is
`ERROR: <carrier> : Cannot open the file as archive`. Complete transcripts:
`artifacts/7z-refusal.txt` (`### exit_code=2` per carrier). This confirms the round-37
rejection candidate still holds on 7-Zip 26.04 for all four frozen carriers, not just K1.

## 5. Findings that bear on the C1 premise and on "cross-tool" independence

**(a) [FACT] unblob 26.6.4's `squashfs_v4_be` handler shells out to the external
`sasquatch-v4be` binary.** Source: installed package
`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`:
`:25 EXECUTABLE = "sasquatch"`, `:26 V4BE_EXECUTABLE = "sasquatch-v4be"`,
`:40-41 case Endian.BIG, 4: executable = self.V4BE_EXECUTABLE`,
`:69 return [self.EXECUTABLE, self.V4BE_EXECUTABLE]`; `unblob --show-external-dependencies` lists
`sasquatch` and `sasquatch-v4be`.

Direct unblob CLI runs (no REA) corroborate at the process level. `unblob -e out --report rep.json K3/carrier.bin`
(and K4), rc=0 both, report entry `handler_name=squashfs_v4_be`, `start_offset=0`,
`end_offset=4096` (K3, 4kpad) / `307` (K4, nopad); log line:

```
sasquatch-v4be -be -no-exit-code -f -d <out>/carrier.bin_extract <carrier>
```

and the extracted bytes equal `oracle.tsv` for both (4/4 each). Artifacts
`unblob-report-K{3,4}.json`, `unblob-command-K{3,4}.txt`.

Consequences for the frozen wording (reported, **not repaired**):
1. The claim text "run with stock unblob 26.6.4; **no external extractor dependency**" and the
   `Not claimed` sentence "the `squashfs_v4_be` handler publishing all oracle files without any
   external extractor" are too strong as written: stock unblob names and drives the BE handler but
   *cannot* extract without `sasquatch-v4be` on `PATH`. The accurate statement is that the BE leg
   needs only unblob **plus** its documented `sasquatch-v4be` dependency (no bespoke lane code).
   `[INFERENCE]` This also explains why the round-37 "missing-extractor-dependency" before-arm did
   not reproduce: `sasquatch-v4be` was already installed in `~/.local/bin` when that probe ran.
2. `tools/round-38/c1-run.sh`'s header comment "with stock unblob (no external extractor needed
   for standard BE v4), ... never runs sasquatch" is factually wrong at the subprocess level:
   the `after` leg reaches `sasquatch-v4be` through the handler. Flagging only — the harness
   behaviour itself is correct.
3. **Independence caveat for this seat's evidence:** because unblob delegates to the same
   executable, my `sasquatch-v4be -be` run is *not* an independent decoder relative to the
   REA→unblob path; it exercises the same binary and the same flag. What this seat verifies
   independently is (i) the binary reproduces the committed oracle byte-for-byte, (ii) the
   carriers are genuine standard BE v4 (superblock decode, `file(1)`, LE readers refuse), (iii)
   the oracle for K1/K2 is reproduced from an independent generator source tree. The K3/K4 oracle
   itself originates from unblob's own test `__output__` (same lineage), so for K3/K4 the oracle
   is expected-output evidence, not a second decoder. Any claim text implying two *distinct*
   decoders agree should be corrected; "extractor binary and committed oracle agree" is what is
   shown.

**(b) [FACT] The frozen K3/K4 carriers are standard BE v4, not AVM-BE.** unblob's AVM branch is
`:48 is_avm = header.bytes_used == header.mkfs_time` (`:49 if not is_avm: append "-be"`). For both
frozen carriers `bytes_used = 0x0000000000000133 (307)` and `mkfs_time = 0x621f5e09
(1646359049)`, so `is_avm` is false and the plain `-be` path is taken — consistent with the log
line above and with the claim's AVM exclusion. This is direct byte evidence that K3/K4 do not
exercise the AVM-BE branch.

**(c) [FACT] K3/K4 provenance is byte-identical to the round-37 probe carriers.**
`cmp K3/carrier.bin .ufo/waves/round-37/probes/be-squashfs_v4.bin` and `cmp K4/carrier.bin
.../be-squashfs_v4.nopad.bin` both equal; sha256 `9c7c…97c0` / `a29d…56ed` match both locations.
Padding layout confirmed: K3 = 307-byte filesystem + zero padding to 4096 (K4 is exactly 307).

## 6. Artifacts (all under `.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/`)

```
oracle-compare.tsv        per-carrier matrix (rows, path+sha diff, oracle-vs-src)
sasquatch-v4be-K{1..4}.tsv  raw extractor listings (rel path, sha256, size)
harness-oracle-K{1..4}.tsv  c1-run.sh oracle-mode output (byte-identical to the above)
7z-refusal.txt            full 7-Zip transcript per carrier + exit codes
unsquashfs-refusal.txt    4.7.5 refusal per carrier
carrier-pins.txt          recomputed carrier sha256
unblob-report-K{3,4}.json unblob CLI report (handler squashfs_v4_be, chunk bounds)
unblob-command-K{3,4}.txt the exact sasquatch-v4be argv unblob issued
tool-versions.txt         versions + sasquatch-v4be digest
```

## 7. Verdict for this seat

- Oracle reproduction: **pass** — 4/4 carriers, 16/16 regular files identical to the committed
  oracles on path, sha256 and size; 0 missing, 0 extra; symlinks and directory sets identical for
  K1/K2 where the oracle is the source tree.
- No carrier failed to open with `sasquatch-v4be -be`, so nothing here falsifies the cross-tool
  expectation.
- 7-Zip refusal: **reproduced on all four** carriers, exit 2, text recorded in §4 for the Gate.
- Two premise corrections routed to the L1 (§5a): the "no external extractor dependency" wording,
  and the harness header comment; plus the independence caveat (same executable on both legs).
- Blockers: none. Files written: this report and the artifact directory only. Scratch removed;
  no VCS mutation; no REA invocation; no frozen input touched.
