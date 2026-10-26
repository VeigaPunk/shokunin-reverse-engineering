# R38CrossToolK2 — cross-tool oracle reproduction for C1 carrier K2 (REA-independent)

Seat: leaf executor. Scope: reproduce the C1 regular-file oracle for K2 with
`~/.local/bin/sasquatch-v4be -be` into fresh scratch, compare path+sha256 against the committed
`corpus/evidence/round-37/c1/K2/oracle.tsv`, and confirm 7-Zip refuses the BE image with the
error text recorded for the lesson Gate. K1/K3/K4 were run in the same batch (same command shape,
no extra setup) so the falsifier covers the whole frozen carrier set, not only K2.

No lane corpus file, frozen predicate, counter, carrier, oracle or registry was touched. Writes:
this report + artifacts under `.ufo/waves/round-38/w1/artifacts/R38CrossToolK2/`. Scratch
`/fast/scratch/hyaku/kaidoku-r38/R38CrossToolK2` removed (`ls` → No such file, exit 2).

**Verdict: cross-tool expectation CONFIRMED, not falsified.** 4/4 carriers open, 16/16 oracle
regular files reproduced with identical path suffix and sha256, 0 missing / 0 extra / 0 mismatched.
7-Zip 26.04 refuses all four BE images (exit 2). No new defect blocks C1.

## 1. Environment (all observed, not assumed)

| item | value | how |
|---|---|---|
| lane HEAD at run | `9c9d496b73cf066b02639dc54647934a0ba4297a` | `git rev-parse HEAD` |
| base (measured rev for the claim) | `77091b492cc53f8743bd0701b1e7d5e66123dd84` | claims doc; `git cat-file -t` → `commit` |
| freeze commit | `e059ca9391642d5b71b6662cabcbdce0d9308719` `kaidoku-shokunin <kaidoku@shokunin.local>` `2026-10-26T03:06:32-03:00` | `git cat-file -t` → `commit`, `git show -s` |
| control-receipts commit | `efd5c47a72a50b3a434783f82268fb4a96e636a1` `2026-10-26T03:09:14-03:00` | `git show -s` |
| extractor | `~/.local/bin/sasquatch-v4be` 436232 B; `-version` → `unsquashfs version 4.5.1 (2022/03/17)` | direct run, exit 0 |
| 7-Zip | `/usr/bin/7z`, `7-Zip 26.04 (x64)` | `7z i` |
| stock squashfs-tools | `/usr/bin/unsquashfs version 4.7.5 (2026/03/01)` | `unsquashfs -version` |
| generator | `tools/round-37/gen-squashfs.py`, python 3.14.8, zlib 1.3.2/1.3.2 | regen run |
| `diff` on PATH | `diff (pi-uu-diff) 0.8.0` (uutils) — GNU-only flags rejected | `diff --version`; see §7.3 |
| tools installed | none (no pacman/uv/npx installs this seat) | — |

## 2. Carrier bytes used (frozen pins, re-verified at base rev)

`sha256sum` on disk **and** `git show 77091b49:<path> | sha256sum` (identical for all eight):

| carrier | size | sha256 | frozen round-38 pin (`.ufo/waves/round-38/c1/carriers.json`) |
|---|---|---|---|
| K1 `carrier.sqsh` | 9780 | `1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e` | same |
| **K2 `carrier.sqsh`** | **1606** | **`403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154`** | same |
| K3 `carrier.bin` | 4096 | `9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0` | same |
| K4 `carrier.bin` | 307 | `a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed` | same |

Oracle files also byte-identical to base rev (`git show`): K1 `0c993e74…`, K2 `6567cc50…`,
K3 `638a6f75…`, K4 `638a6f75…`. K2 `src` regular files identical to base;
`src/var/lib/run-link` is git mode `120000` blob `034758ff…` whose content
`../../a/run.sh` equals `readlink` on disk (the earlier `sha256sum`-vs-`git show` difference on
that path is just symlink dereference, not drift).

## 3. Commands and results (scratch-only; every command named, every exit code recorded)

```
S=/fast/scratch/hyaku/kaidoku-r38/R38CrossToolK2; mkdir -p "$S"; export TMPDIR="$S"
C=<lane>/corpus/evidence/round-37/c1
~/.local/bin/sasquatch-v4be -be -d "$S/out/$k" "$C/$k/carrier."*      # k=K1..K4   → rc=0 (all)
cd "$S/out/$k" && find . -type f -print0 | sort -z | while read -r -d '' f;
  do printf '%s\t%s\t%s\n' "${f#./}" "$(sha256sum "$f"|cut -d' ' -f1)" "$(stat -c%s "$f")"; done
sort "$C/$k/oracle.tsv" | diff -u - "$S/$k.extracted.tsv"            # → exit 0 (all four)
```

| carrier | sasquatch rc | oracle rows | matched (path+sha256+size) | missing | extra | `diff` exit |
|---|---|---|---|---|---|---|
| K1 | 0 | 5 | 5 | 0 | 0 | 0 |
| **K2** | **0** | **3** | **3** | **0** | **0** | **0** |
| K3 | 0 | 4 | 4 | 0 | 0 | 0 |
| K4 | 0 | 4 | 4 | 0 | 0 | 0 |
| total | 4/4 | 16 | **16/16** | 0 | 0 | 0 |

Strongest form of the result: my extraction listing is **byte-identical to the committed oracle
file itself**, not merely row-equal — `sha256sum` of each generated listing equals the committed
`oracle.tsv`:

* `K1.extracted.tsv` = `0c993e7421338a8c08e311914f71e0ebf9fda2849931b4f544e3774c78f13aab`
* `K2.extracted.tsv` = `6567cc50d9a1dea27609c0ae2b815229317e899eaba654edf6f0880e559cb921` (K2 oracle)
* `K3.extracted.tsv` = `K4.extracted.tsv` = `638a6f75579ae1ff508d3152723b1b9b279a90090e180cc63a2a6a758a477d23`

### K2 detail (the assigned carrier)

Extracted tree (`-d` is the tree root, no nested `squashfs-root/`):

```
d a   d a/b   d a/b/c   d var   d var/lib
f a/run.sh                       ca9988b8…602a4084   22
f space name.txt                 72d0bbc9…6c4c85d   21
f var/lib/data.bin               e96760a8…9f7d90d0  10240
l var/lib/run-link -> ../../a/run.sh          (symlink; not an oracle row — predicate scopes to regular files)
```

`sasquatch-v4be` stdout: `created 3 files / created 6 directories / created 1 symlink / created 0
devices / …`; stderr: `Reading a different endian SQUASHFS filesystem on …K2/carrier.sqsh` +
`Successfully decompressed with default gzip decompressor` (three blocks). Artifacts
`K2.stdout`, `K2.stderr`.

Second, oracle-independent leg: `diff -r <K2/src> <out/K2>` → **exit 0**, and a
name+type+symlink-target listing diff (`d/f/l %P [-> %l]`, sorted) → **exit 0** (`K2.src.names`
sha `e3f363e0…` == `K2.ext.names`). Same for K1 (`diff -r` exit 0; `K1.src.names` ==
`K1.ext.names` sha `9d378c52…`). So the BE extraction reproduces the committed source trees
exactly, including directory layout and symlink targets, not just the regular-file subset.

K1's `link-to-hello -> ../hello.txt` dangles identically in `src` and in the extract (agrees with
the round-37 lesson's observation).

### Frozen harness leg (same bytes, designated command)

`bash tools/round-38/c1-run.sh oracle "$C/K2/carrier.sqsh" "$S/harness-out/K2" "$S/harness-scratch"`
→ **exit 0**, stderr empty, TSV sha `6567cc50…` (== oracle file); `diff -u` vs sorted oracle
**exit 0**. The harness's `oracle` mode is functionally identical to my hand run, so the claim's
own cross-tool command produces the oracle on K2 at these bytes.

### Determinism

Second independent K2 extraction (fresh dest) → identical listing
(`diff -u K2.extracted.tsv K2.extracted2.tsv` **exit 0**), rc=0.

### Negative control: `-be` is required, and the failure is the endian probe

`~/.local/bin/sasquatch-v4be -d "$S/out-k2-noflag" K2/carrier.sqsh` (no `-be`) → **exit 1**,
no tree created:

```
SquashFS version [1024.0] / inode count [167772160] suggests a SquashFS image of a different endianess
read_id_table: failed to read id table block
FATAL ERROR: File system corruption detected
```

Those two numbers are exactly the little-endian misread of K2's superblock that I compute
independently below (`s_major` 4→1024, `inode_count` 10→167772160), which ties the failure to
endianness and not to an unrelated defect.

## 4. 7-Zip refusal (Gate material) — all four carriers

`7z l <carrier>` → **exit 2** for K1, K2, K3, K4. Text is identical in shape; K2 verbatim:

```
stdout:  7-Zip 26.04 (x64) : Copyright (c) 1999-2026 Igor Pavlov : 2026-10-05
         Scanning the drive for archives:
         1 file, 1606 bytes (2 KiB)
         Listing archive: <abs path>/K2/carrier.sqsh
         Errors: 1
stderr:  ERROR: <abs path>/K2/carrier.sqsh : Cannot open the file as archive
```

No listing lines are emitted (no archive is recognised), and `Errors: 1` is on stdout with the
`ERROR:` line on stderr — a checker that only reads stdout will see `Errors: 1` but not the
`says why` line. Artifacts `K2.7z.out`, `K2.7z.err`, plus `K1/K3/K4.7z.err`.

For contrast (same batch): stock `unsquashfs 4.7.5 -d … K2/carrier.sqsh` → **exit 1**,
`Reading a different endian SQUASHFS filesystem …` + `FATAL ERROR: Can't find a valid SQUASHFS
superblock` — reproducing the lesson's claim on the K2 carrier specifically.

## 5. Independent superblock decode (premise check: "standard BE v4", not a vendor variant)

Hand-unpacked the 96-byte v4 superblock big-endian (`artifacts/sb.py` → `superblock.json`):

| field | K1 | K2 | K3 | K4 |
|---|---|---|---|---|
| magic (bytes) | `sqsh` | `sqsh` | `sqsh` | `sqsh` |
| s_major.s_minor | 4.0 | 4.0 | 4.0 | 4.0 |
| compression | 1 (gzip) | 1 | 1 | 1 |
| block_size / block_log | 4096 / 12 | 4096 / 12 | 131072 / 17 | 131072 / 17 |
| inode_count | 11 | 10 | 5 | 5 |
| fragments | 0 | 0 | 1 | 1 |
| bytes_used / file size | 9780 / 9780 | 1606 / 1606 | 307 / 4096 | 307 / 307 |
| tail padding | 0 | 0 | 3789 | 0 |
| mkfs_time | 1700000000 | 1700000000 | 1646222857 | 1646222857 |
| table starts ascending | yes | yes | yes | yes |

Consequences, all consistent with the frozen spec:
- all four are **standard** BE v4 (`magic sqsh`, version 4.0, compressor gzip) — no AVM/vendor
  mangling in the carrier set, matching the claim's "standard BE v4" wording;
- K1/K2 `mkfs_time` 1700000000 and `fragments 0` are the generator's own constants
  (`MKFS_TIME = 1700000000`, docstring "no fragments"), and `file` prints the matching creation
  date `Tue Nov 14 22:13:20 2023`;
- K3 carries 3789 bytes of trailing zero padding (4kpad) and K4 none (nopad), exactly as their
  `kind` strings say; `sasquatch-v4be` ignores the padding and still matches 4/4;
- inode arithmetic accounts for every entry: K1 11 = 5 files + 5 dirs + 1 symlink, K2 10 = 3
  files + 6 dirs + 1 symlink, K3/K4 5 = 4 files + 1 dir. So the oracle deliberately covers the
  regular-file subset (5, 3, 4, 4) — the same scoping the counter's `matched()`/`oracle_files`
  uses.

## 6. Provenance: carriers regenerate byte-identically from their committed sources

```
python3 -B tools/round-37/gen-squashfs.py <lane>/corpus/evidence/round-37/c1/K{1,2}/src \
        $S/regen/K{1,2}.sqsh --endian be --comp gzip
```

| carrier | log | regenerated sha256 | `cmp` vs committed |
|---|---|---|---|
| K1 | `wrote …/K1.sqsh 9780 bytes, inodes 11` | `1cfb6c33…117e` | IDENTICAL |
| K2 | `wrote …/K2.sqsh 1606 bytes, inodes 10` | `403cb0a8…9154` | IDENTICAL |

Both runs exit 0 (python 3.14.8 / zlib 1.3.2). This closes the K1/K2 provenance loop from the
committed tree alone: frozen carrier bytes = deterministic output of the frozen generator on the
frozen source trees.

## 7. Findings

### 7.1 (advisory, calibration) K2 is described as having a "unicode name"; no non-ASCII name exists

`.ufo/waves/round-38/c1/carriers.json` (frozen) `kind` for K2 reads
`"synthetic standard-BE v4 gzip (tree2, symlink + unicode name)"`; the round-37
`carriers.json` `note` says the same ("second tree with symlink + unicode name"). Observed:

* `find … | LC_ALL=C grep -P '[^\x20-\x7e]'` over `K2/src` names → no match (exit 1);
  over the extracted names → no match (exit 1);
* `find … -type f -printf '%P\0' | od -c` → `a/run.sh`, `var/lib/data.bin`,
  `space name.txt` — every byte ASCII (the distinguishing name contains a **space**, U+0020);
* `gen-squashfs.py` takes an arbitrary tree argument (`ap.add_argument('tree')`) and contains no
  unicode tree, so no unicode name was ever generated for tree2.

Effect on R38-C1: none. The frozen scored surface is `oracle.tsv` (3 rows) and the carrier sha256,
both matched; `kind` is free text. Flagged because a wave check that greps for a unicode filename
would be looking for an artifact that does not exist, and because the phrasing is inherited into
the round-38 freeze. Suggest (L1's call, not mine) rewording to "symlink + space in filename"
before any knowledge/README prose repeats it.

### 7.2 (advisory, reproducibility of the frozen controls) `gen-controls.py` changed after the freeze commit

`git diff e059ca93 -- tools/round-38/gen-controls.py` is **not** empty; the change is part of
`efd5c47a` (control receipts), i.e. it landed *with* the receipts rather than before them:

```diff
-            d, b, rv, c = c2_fixture(a.kind, a.kind.split('-')[1])
+            d, b, rv, c = c2_fixture(a.kind, {'c2-1': 'junk', 'c2-2': 'delete', 'c2-3': 'substitute'}[a.kind])
...
-    # control must NOT meet the target: exit 0 (or 2 unevaluable) is expected; exit 1 = control met target.
-    return 0 if res.get('exit') != 1 else 1
+    # control must NOT meet the target: counter exit != 0 is expected; exit 0 = control met target (kill condition).
+    ok = res.get('exit') != 0
+    print(json.dumps({'control': a.kind, 'counter_exit': res.get('exit'), 'kill': not ok}))
+    return 0 if ok else 1
```

Facts: (a) the receipts at `efd5c47a` were produced with the post-change generator and record
`argv` but not the generator bytes (`controls/ctl-c2-1-junk-count.json` shows `argv`, `exit: 1`,
`met_target: false`, `mismatches: 1`); (b) the freeze commit alone therefore does not regenerate
those receipts — `git show efd5c47a:tools/round-38/gen-controls.py` does; (c) the second hunk
**changes control semantics** after freeze: before, exit 2 ("unevaluable") counted as *not* meeting
the target; after, only exit 0 is "kill". C1/C2 *counters* themselves are untouched
(`c1-counter.py`, `c1-run.sh`, `c2-counter.py`, `carriers.json`, `plans/round-38-claims.md`
all hash-identical to the freeze commit: `a7a62b09…6db8`, `e2ec4938…0203`, `7f137b66…b0f7`,
`be404a9d…1be2`, `13ea8eba…9815`). Not my call — surfaced for the reviewers scoring CTL-C2-*
and for the L1's freeze-integrity ledger.

Note the control receipts were **not** re-run by me; I only read them. The `revision` field inside
them (`87dc8502…`, `9f5b5b6f…`) is the control fixture's synthetic rev, not a lane commit.

### 7.3 (environment note) `diff` on PATH is uutils, not GNU

`diff --version` → `diff (pi-uu-diff) 0.8.0`; GNU-only flags fail:
`diff -r --no-dereference a b` → `error: unexpected argument '--no-dereference' found`,
exit 2. Plain `-r`, `-u`, `--label` work. Any lane script, selftest or later wave step that
passes GNU-specific diff flags will fail for the wrong reason; my comparisons used only `-r`/`-u`
(plus an explicit `find`-based name/symlink diff to avoid dereference ambiguity).

### 7.4 (tooling record for the lesson Gate) sasquatch-v4be is a patched squashfs-tools 4.5.1

`~/.local/bin/sasquatch-v4be -version` self-identifies as `unsquashfs version 4.5.1
(2022/03/17)` while stock is 4.7.5. So the cross-tool leg is "patched squashfs-tools 4.5.1 vs
unblob 26.6.4": independent of unblob (which is what C1 claims through REA), but of the same
lineage as unsquashfs. Combined with §5 this is the honest description of the independence
strength behind the oracle.

Also recorded for the Gate (R37-CL3 wants the 7-Zip rejection filed): exact text and exit code in
§4, for **all four** carriers, not only K2.

## 8. Limits of this check (explicitly not claimed)

* Only regular files are compared, matching the predicate's "every regular file … same
  relative-path suffix, same sha256". Directory entries are compared only in the K1/K2
  `find`-listing diff; symlink rows are compared for K1/K2 via that listing, not for K3/K4 (those
  images contain none — `created 0 symlinks`).
* Metadata (mtimes, uids/gids, modes) is **not** compared, by either the frozen oracle or this
  check. `sasquatch-v4be` output beyond the oracle (padding write behaviour, xattrs) not probed.
* This is the REA-independent leg only: no `rea-agents extract-firmware` was run by this seat, so
  nothing here speaks to the `squashfs_v4_be` handler name, extraction gaps or evidence-id
  recomputation of the after-receipts. K3/K4 remain unblob's own fixture/oracle pair (see
  `R38ScoutUnblobFixtures` — "independent of the REA run, but not independent of unblob"), so the
  sasquatch leg is the only extractor-independent evidence in the set.
* Cross-tool agreement is agreement on *these four* images, both of which are ≤ 9 KB trees with
  gzip compression; nothing is claimed about xz/lzo/zstd BE images, fragment-heavy images, or
  AVM-BE (which stays Frontier).

## 9. Artifacts

`.ufo/waves/round-38/w1/artifacts/R38CrossToolK2/` (sha256 of each, `sha256sum *`):

```
3e2807ef…b3ee4  K1.7z.err            9d378c52…b167  K1.ext.names / K1.src.names (identical)
0c993e74…3aab  K1.extracted.tsv     8743e849…2251  K1.regen.log
df3daaf8…1c76  K1.stderr            2a328a74…87cc  K2.7z.err
4201d6bb…be25a K2.7z.out            e3f363e0…71f7  K2.ext.names / K2.src.names (identical)
6567cc50…69121 K2.extracted.tsv = K2.harness.tsv = K2.oracle.sorted.tsv (identical bytes)
6d5c9b0f…f75d  K2.regen.log         e3b0c442…f855  K2.src-vs-extract.diff (empty)
b4bdf54a…5b56  K2.stderr            60a10a52…16b2  K2.stdout
bd14b4b3…eea   K2.unsquashfs.out    8a2a93e1…03b   k2.second.out   (determinism run)
ebd24707…814d  k2.noflag.out       2793b893…382   k2.nodest.out
70a6f9b8…6c8d  K3.7z.err            638a6f75…7d23  K3.extracted.tsv
3220598c…8e2c  K3.stderr            0db92483…88da  K4.7z.err
638a6f75…7d23  K4.extracted.tsv     3a6726d2…343   K4.stderr
cba0b50d…482a  sb.py               d102e4f0…28f7  superblock.json
```

Scratch-only notes that are not evidence: `sasquatch-v4be -d` requires the destination's parent
to exist (`FATAL ERROR: dir_scan: failed to make directory …, because No such file or directory`,
exit 1 — `k2.nodest.out`); the frozen harness avoids this with `mkdir -p "$OUT"`. Any hand-run
copy of the lesson's `-d out` command must `mkdir -p` first.

## 10. Transfer to L1 (advisory, one line each)

1. C1's cross-tool leg holds on all four carriers at the frozen bytes: publishable as
   "sasquatch-v4be -be reproduces the committed oracle byte-for-byte (4/4, 16/16 files)".
2. Gate entry for 7-Zip rejection can cite 7-Zip 26.04, exit 2, `Cannot open the file as
   archive`, 4/4 carriers.
3. Fix the "unicode name" wording for K2 (§7.1) before it propagates into PROVINCE/knowledge prose.
4. `gen-controls.py` moved after the freeze commit (§7.2) — score CTL-C2-* from `efd5c47a`.
