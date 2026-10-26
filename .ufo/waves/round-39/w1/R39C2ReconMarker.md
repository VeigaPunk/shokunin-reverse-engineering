# R39C2ReconMarker — the AVM-marker `-be` drop on standard-BE SquashFS v4 (C2 recon, pre-freeze)

Verdict: **CONFIRMED** — the AVM marker (`mkfs_time == bytes_used`) makes unblob 26.6.4 drop `-be`
from the child `sasquatch-v4be` argv, and the drop is invariant across compression (gzip/xz), tree
shape and symlink content: 6/6 AVM runs give the same six features. Collateral (and freeze-relevant)
findings: a **successful** run records no child argv at all (so the grammar's BE feature is `n/a`
there), an **absolute** symlink target is never "escaping" (it is re-rooted and kept), and the
round-37 generator's **xz** bodies fail extraction for a second, endian-independent reason.

Scope: development carriers I authored in scratch from five fresh trees + the round-38 probe
envelopes. No K5/K6 carrier was built, no REA run touched a K5/K6 or held-out input, nothing in
`corpus/`, `tools/`, `plans/` or `SKILL.md` was written. No tools installed or upgraded. No VCS
mutation.

## 1. Mechanism (source-cited, installed artefacts only)

`unblob` 26.6.4, handler `unblob/handlers/filesystem/squashfs.py`
(sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` — identical to the
round-38 probe's `handler_sha256`), `SquashFSExtractor.extract`, lines 32-56 (AVM branch 44-50):

```python
case Endian.BIG, 4:
    executable = self.V4BE_EXECUTABLE          # "sasquatch-v4be"
    ...parse HEADER_STRUCT with Endian.BIG...
    is_avm = header.bytes_used == header.mkfs_time     # line 48
    if not is_avm:
        commands_args.append("-be")                    # line 50
case Endian.BIG, _:  commands_args.append("-be")
case Endian.LITTLE, _: commands_args.append("-le")
```

So for a big-endian v4 image the flag is emitted **only when the marker is absent**. When
`mkfs_time == bytes_used` unblob drops `-be`, and `sasquatch-v4be` *without* `-be` reads the
superblock as little-endian and aborts (exit 1). The AVM marker is therefore not a
"vendor quirk that still extracts": for this toolchain it is a **guaranteed extraction failure on an
undamaged body**, and the failure text gives no hint about the flag:

```
SquashFS version [1024.0] / inode count [150994944] suggests a SquashFS image of a different endianess
read_id_table: failed to read id table block
FATAL ERROR: File system corruption detected
```

Observed argv (unblob `-v` log, `logs/ub-*.log`; same strings in the REA envelopes):

| carrier | child argv (first tokens) | exit |
|---|---|---|
| `carrier-TC-avm-gzip.bin` | `sasquatch-v4be -no-exit-code -f -d …` | 1 |
| `carrier-TC-avm-xz.bin` | `sasquatch-v4be -no-exit-code -f -d …` | 1 |
| `carrier-TC-be-gzip.bin` (no marker) | `sasquatch-v4be -be -no-exit-code -f -d …` | 0 |

Direct matrix (`sasquatch-matrix.json`, 21 carriers × {no flag, `-be`}, each call in its own session
because a failing `sasquatch-v4be` can take the calling shell down): **every** BE/AVM carrier fails
with no flag (`files=0`, exit 1) and succeeds with `-be` — *except* multi-block xz bodies, see §6.

The marker is reproducible from `tools/round-37/gen-squashfs.py --endian avm`, which writes
`mkfs = bytes_used` (`gen-squashfs.py:172-173`, superblock field at offset 8, u32 truncation of the
u64 `bytes_used` at offset 40), so the drop only exists while `bytes_used < 2**32` (4 GiB).

## 2. Feature table — every run, from the REA envelope

21 `extract-firmware` runs (`rea-agents` 6.5.0, `--format json --full-output`, unblob 26.6.4,
`sasquatch-v4be`/`sasquatch` 4.5.1). `ok=true` for all 21; every `subject.digest.sha256` equals the
carrier file's sha256 (checked in `manifest.json`). Columns are the P39-C2 grammar's features:
H = chunk handlers starting `squashfs`; G = gap kinds; D = gap dependencies; unpub =
`unpublished_entries[].kind`; BE / SR / P as defined in the claim.

| run | carrier sha256[:12] | H | chunk failed | G | D | unpub | BE | SR | P | bytes | coverage |
|---|---|---|---|---|---|---|---|---|---|---|---|
| E-be-gzip | 79b2a4842d37 | squashfs_v4_be | False | unpublished-entry | none | symlink | n/a | **yes** | 2 | 17 | partial |
| TA-avm-gzip | e8e3ffa8d972 | squashfs_v4_be | True | extractor-failure | none | none | **no** | no | 0 | 0 | partial |
| TA-avm-xz | eb0d9f6b5075 | squashfs_v4_be | True | extractor-failure | none | none | **no** | no | 0 | 0 | partial |
| TA-be-gzip | 046118726196 | squashfs_v4_be | False | unpublished-entry | none | symlink | n/a | no | 5 | 9067 | partial |
| TA-be-midcorrupt | 229c41dd4805 | squashfs_v4_be | True | extractor-failure,unpublished-entry | none | symlink | **yes** | no | 5 | 19 | partial |
| TA-be-xz | d6a5af153649 | squashfs_v4_be | True | extractor-failure,unpublished-entry | none | symlink | **yes** | no | 5 | 19 | partial |
| TA-le-xz | 46ac4b5f3c74 | squashfs_v4_le | True | extractor-failure,unpublished-entry | none | symlink | no | no | 5 | 19 | partial |
| TC-avm-gzip | e3b6e2868b68 | squashfs_v4_be | True | extractor-failure | none | none | **no** | no | 0 | 0 | partial |
| TC-avm-xz | b15bf84f207d | squashfs_v4_be | True | extractor-failure | none | none | **no** | no | 0 | 0 | partial |
| TC-be-gzip | b56a4a085ee8 | squashfs_v4_be | False | unpublished-entry | none | symlink | n/a | no | 4 | 46 | partial |
| TC-be-nosasq | b56a4a085ee8 | squashfs_v4_be | True | missing-extractor-dependency | sasquatch-v4be | none | n/a | no | 0 | 0 | partial |
| TC-be-xz | aae5a9040ef5 | squashfs_v4_be | False | unpublished-entry | none | symlink | n/a | no | 4 | 46 | partial |
| TT-avm-gzip | 54a37d8225c2 | squashfs_v4_be | True | extractor-failure | none | none | **no** | no | 0 | 0 | partial |
| TT-avm-xz | e9b41ffa9676 | squashfs_v4_be | True | extractor-failure | none | none | **no** | no | 0 | 0 | partial |
| TT-be-gzip | 83168771066c | squashfs_v4_be | False | none | none | none | n/a | no | 2 | 11 | **complete** |
| TT-be-inodecorrupt | 66447d027979 | squashfs_v4_be | True | extractor-failure | none | none | **yes** | no | **0** | 0 | partial |
| TT-be-trunc | 6fb99a9bfc2d | **none** | — | none | none | none | n/a | no | 0 | 0 | **complete** |
| TT-be-xz | 2a3a33558e01 | squashfs_v4_be | False | none | none | none | n/a | no | 2 | 11 | complete |
| TT-le-avmmark | 359779efe0bf | squashfs_v4_le | False | none | none | none | n/a | no | 2 | 11 | complete |
| TT-le-gzip | d1b61a15cd34 | squashfs_v4_le | False | none | none | none | n/a | no | 2 | 11 | complete |
| TT-le-nosasq | d1b61a15cd34 | squashfs_v4_le | True | missing-extractor-dependency | sasquatch | none | n/a | no | 0 | 0 | partial |

Trees (authored, deterministic): **TA** files incl. a 9000-byte multi-block file + in-tree link +
in-tree dir link + absolute `/etc/passwd` link; **TB** files only, no symlinks; **TC** single-block
files + the three TA-style links; **TT** single-block files, no symlinks; **TE** in-tree link +
relative escaping link `../outside.txt` + self-loop `loop -> loop`. Payload-damage variants:
`TT-be-trunc` (last 40 bytes cut), `TT-be-inodecorrupt` (inode-table metadata header XORed),
`TA-be-midcorrupt` (60 data-area bytes XORed). `TT-le-avmmark` is a LE image with
`mkfs_time := bytes_used` patched in.

## 3. Where the child argv is recorded — and where it is not

Both arms, exact JSON paths:

- `data.normalized_result.diagnostics[i].report.command` — a **string**, present only on failure,
  with `report.__typename__ == "ExtractCommandFailedReport"` (BE) or the LE equivalent.
  Verified on every failing run in the table.
- Rich-REA mirror of the same thing: `data.raw_result.report[i].reports[j].extraction_reports[k].command`
  (same string, same typenames). Nothing else in the envelope names `sasquatch`.

**A successful extraction records no child argv at all.** Mechanical proof: a recursive walk of
every string in all 21 envelopes finds `sasquatch` in exactly the two paths above and only for the
runs whose chunk failed. The successful BE runs (`TA-be-gzip`, `TC-be-gzip`, `TC-be-xz`,
`TT-be-gzip`, `TT-be-xz`, `E-be-gzip`) contain **zero** `sasquatch` strings:
`data.normalized_result.diagnostics` is `[]`, `data.raw_result.execution.command` is
`/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob` with `args` naming only unblob flags, and
`data.raw_result.version_execution` is the `unblob --version` probe. Therefore, under the frozen
grammar, **a successful BE run scores BE = `n/a` — the grammar cannot see that `-be` was passed**.
The BE feature is a *failure-only* feature; it exists precisely to separate
`avm-marker-be-dropped` (BE=`no`) from `body-extractor-failure` on an intact-superblock BE body
(BE=`yes`), and it is useless for any success class.

Round-38 confirmation (`feat-round38.json`, computed with the same extractor from the probe
envelopes): `rea-k1-avm.json` → H={squashfs_v4_be}, G={extractor-failure}, D=∅, BE=`no`, SR=`no`,
P=0, bytes=0, coverage=partial; `rea-k1-orig.json` → H={squashfs_v4_be}, G=∅, BE=`n/a`, SR=`yes`,
P=5, bytes=9656. Identical shape to my 6 AVM runs and to my `E-be-gzip` (SR=yes) run.

## 4. Does an AVM-marked image whose tree holds a symlink change anything?

**No.** `TC-avm-{gzip,xz}` (in-tree link, in-tree dir link, absolute `/etc/passwd` link) and
`TT-avm-{gzip,xz}` (no symlinks) are feature-identical: H={squashfs_v4_be}, chunk
`extraction_failed=true`, G={extractor-failure}, D=∅, `unpublished_entries=[]`, BE=`no`, SR=`no`,
P=0, published_bytes=0. `TA-avm-{gzip,xz}` (multi-block body + links) is identical again. The
extractor dies before writing a single entry, so no symlink is ever materialised, kept or removed —
the REA output directory stays empty (`rea/TC-avm-gzip/` contains no files). Symlinks and the AVM
drop are orthogonal: a symlink-bearing AVM carrier collapses into the plain AVM signature.

## 5. Consequences for the triage table (what the freeze must encode)

Empirical facts the table has to survive:

1. **`no-squashfs-chunk` is real and distinct** — `TT-be-trunc` (last 40 bytes cut): H=∅, G=∅, P=0,
   BE=`n/a`, coverage=**complete**. unblob's `calculate_chunk` seeks to `bytes_used` for the padding
   check, so a short body is not even detected as a chunk. Note the trap: `coverage=complete` with
   P=0 looks "clean" to any rule that keys on coverage.
2. **`avm-marker-be-dropped` ≡ `body-extractor-failure` on every cell except BE.** `TT-be-inodecorrupt`
   (BE body, superblock intact, inode table damaged) gives H={squashfs_v4_be}, G={extractor-failure},
   D=∅, SR=no, **P=0**, and differs from all six AVM runs only in `-be in child argv` (`yes` vs `no`).
   The BE cell is therefore load-bearing, and the `published files` cell for `body-extractor-failure`
   MUST be `*` (not `>0`): a metadata-level failure publishes nothing.
3. **Exact-set gap matching splits labels into rows.** With `a+b` meaning set equality, one class can
   need several rows: `body-extractor-failure` on a link-free tree is G=`extractor-failure`
   (`TT-be-inodecorrupt`) but on a link-bearing tree is G=`extractor-failure+unpublished-entry`
   (`TA-be-midcorrupt`, `TA-be-xz`). Same for `in-tree-symlink-metadata` vs `clean`.
4. **BE must be `n/a` in every success row and in every dependency row.** `TC-be-nosasq` /
   `TT-le-nosasq` record no argv at all (diagnostic typename `ExtractorDependencyNotFoundReport`,
   no `command` field) → BE=`n/a` even though these are BE/LE runs. Writing BE=`yes` in a
   `dep-missing-be` row would make the row unable to match.
5. **BE=`no` does not mean "big endian body"**: the LE failure `TA-le-xz` records
   `sasquatch -le -no-exit-code -f …` → BE=`no`, H={squashfs_v4_le}. Endianness is carried by H;
   BE=`no` only means "a sasquatch-named command exists and none had `-be`".
6. **`dep-missing-be` / `dep-missing-le` are environment classes, not carrier classes.** They were
   produced by removing `$HOME/.local/bin` from the child PATH with `REA_UNBLOB_COMMAND` kept
   absolute; the carrier bytes are the ordinary `TC-be-gzip` / `TT-le-gzip` images (same sha256 as
   the passing runs). The held-out manifest must record the PATH mode per envelope, and the
   counters must replay that mode, or the class is unreachable. D populates exactly as
   `sasquatch-v4be` (BE) / `sasquatch` (LE); gap kind is `missing-extractor-dependency`.
7. **`escaping-symlink-removed` needs a *relative* escaping target or a loop** (see §6). SR is `yes`
   only for `E-be-gzip` (relative `../outside.txt` + self-loop) and for round-38's K1
   (`../hello.txt`); the absolute-target links produced SR=`no`.
8. Available-but-unused separators (the grammar does not read them): the decoded
   `report.stderr` endianness banner and `report.exit_code` (always 1 on the AVM drop).

## 6. Symlink rule: the draft's "escaping" needs sharpening (affects C1's oracle too)

unblob 26.6.4 `unblob/extractor.py:50-93` `fix_symlink` + `file_utils.py:34-39` `is_safe_path`:

```python
raw_target = os.readlink(path)
target = Path(raw_target)
if target.is_absolute():
    target = Path(target.as_posix().lstrip("/"))      # re-rooted under outdir
else:
    target = path.resolve()                            # resolve() FOLLOWS the link
if not is_safe_path(outdir, target):                   # relative_to() -> ValueError
    ... MaliciousSymlinkRemoved(link=..., target=target.as_posix()); path.unlink()
else: rewrite to os.path.relpath(outdir/target, path.parent)
```

- An **absolute** target is re-rooted (`/etc/passwd` → `<outdir>/etc/passwd`) and is therefore
  *never* escaping: it is rewritten, kept as metadata, and reported as one
  `unpublished-entry` gap (`TC-be-gzip` shows `link_target: "etc/passwd"`, SR=`no`).
- Only a **relative** target whose `path.resolve()` leaves the extraction root (`../outside.txt` at
  the root), or a symlink loop (`path.resolve()` raises → "Symlink loop identified"), is removed
  with `MaliciousSymlinkRemoved`; a removed link yields **no** gap (round-38 `k1-orig`: gaps 0,
  one MaliciousSymlinkRemoved).
- The reported `target` for relative links is the *resolved link path*, not the literal target —
  which is why round-38's diagnostic shows an absolute `/tmp/rea-firmware-…/extracted/hello.txt`
  for a `../hello.txt` link.

For C1: if a frozen K5/K6 `symlinks.tsv` marks an **absolute** link (`/etc/…`) as `escaping`, the
oracle is wrong — it will be kept as an in-tree `unpublished-entry`. Freeze `escaping` only for
relative `../`-style targets (or loops). For C2: the `escaping-symlink-removed` held-out carriers
must use relative escaping links; an absolute-target carrier lands in
`in-tree-symlink-metadata` and would silently mislabel.

## 7. Tooling defect found: `gen-squashfs.py --comp xz` breaks multi-block bodies

Endian-independent, reproducible, and it contaminates any "clean" expectation for xz:

| carrier | `-be` | result |
|---|---|---|
| `TT-*-xz` (all files < 4096) | passed | exit 0, files correct (`files=2`) |
| `TC-*-xz` (all files < 4096) | passed | exit 0, 6 extracted entries = 4 regular files + 2 links (REA publishes 4, 46 bytes) |
| `TA-be-xz` / `TA-avm-xz` / `TB-*-xz` (a file ≥ 4096) | passed | **exit 1** `FATAL ERROR: writer: failed to read/uncompress file …/file.dat` |
| `TA-le-xz` (`sasquatch -le`, no BE involved) | n/a | **exit 1**, same fatal error |

The extracted bytes are wrong too: in `TA-be-xz` most files come out 0 bytes
(`file.dat` 0 vs 9000 in the tree, `readme.md` 0, `hello.txt` 0) while `bin/run` is correct — so the
REA envelope reports `published_bytes=19` for a 9 KB tree. The compression path is
`gen-squashfs.py:22-29` (raw LZMA2, `dict_size=block_size`); a multi-block file makes sasquatch
re-run its decompressor ladder (xz → zstd → lzma-adaptive → …) and then abort.

Second generator defect, found while checking why a three-symlink tree produced two gaps: a
**symlink to a directory is dropped at build time**. `build_image`'s `os.walk` loop
(`gen-squashfs.py:61-74`) records only `fnames`, and a symlink-to-dir is reported by `os.walk` in
`dirnames` without being descended into, so it is never written. Proof on `carrier-TC-be-gzip.bin`
(tree had `link-in`, `dir-in -> docs`, `link-out`): `sasquatch-v4be -lls -be` lists only
`link-in -> hello.txt` and `link-out -> /etc/passwd` — `dir-in` is absent from the **image**, not
just from the extraction. (The `link-out` listing also shows the target still absolute in the image,
which is why §6's `lstrip("/")` happens in unblob's `fix_symlink`, not in sasquatch.)

Consequence for the freeze: any held-out `clean` / `in-tree-symlink-metadata` /
`escaping-symlink-removed` carrier built with `--comp xz` **and any file ≥ block_size** will emit
`extractor-failure` and land in `body-extractor-failure`. Either fix the generator's LZMA2 chunking
or keep held-out xz carriers single-block-per-file. The AVM classes are unaffected (they fail
earlier), but their xz variants are not a clean contrast for anything else. Likewise, a frozen tree
that holds a symlink **to a directory** loses that entry inside the carrier, so it can neither
publish nor gap: the generator must not be trusted to materialise such a link, and any oracle or
held-out tree naming one is describing a path the image does not contain.

## 8. Risks / blockers for the freeze

- BE feature is failure-only (§3): a triage table cannot distinguish a successful BE from a
  successful LE run. If any held-out class expects BE=`yes`/`no` on success, it is unsatisfiable.
- `avm-marker-be-dropped` and `body-extractor-failure` are separable **only** by the BE cell and only
  when the body failure is on an intact-superblock BE image. If a held-out `avm` carrier is also
  truncated, the features collapse to `no-squashfs-chunk` and the AVM label becomes unreachable —
  keep the two damages disjoint in `heldout-gen.py`.
- The drop is bounded by `bytes_used < 2**32`; a >4 GiB dev/held-out carrier would not reproduce it.
- xz generator defect and the directory-symlink drop (§7) plus the absolute-symlink mislabel (§6) are
  the ways a frozen class definition or oracle can become unreachable or wrong without anyone
  noticing.
- `sasquatch-v4be` can kill the calling process group on failure (exit 1 is not enough isolation);
  scripts must launch it with `start_new_session=True`/`setsid`.
- Nothing here is a C1 result: I state the symlink mechanics from unblob source plus my carriers;
  K5/K6 pins, oracle bytes and receipts remain untouched and unmeasured.

## 9. Evidence index (all under `.ufo/waves/round-39/w1/artifacts/R39C2ReconMarker/`)

- `envelopes/rea-*.json` — 21 full CLI envelopes `{ok,data,meta}` (uncompressed, ≤ 25 KB each).
- `manifest.json` — per run: envelope, carrier path, carrier sha256 == `subject.digest.sha256`,
  `evidence_id`, unblob version + executable sha256, CLI duration.
- `features.py` — the grammar feature extractor used for every row of §2 (accepts bare `data` or a
  full CLI envelope). `feat-*.json` — its output for this matrix and for the round-38 probe.
- `carriers/*.bin` — all 25 development carriers (21 pristine + 4 damaged/patched variants); the
  five trees are recreated verbatim by `repro.sh`.
- `sasquatch-matrix.json` — 50 direct invocations: 25 carriers × {no endian flag, correct endian
  flag}, each call in its own session.
- `logs/ub-*.log` — unblob `-v` logs holding the exact child argv for the AVM and BE cases.
- `repro.sh` — trees, carriers, payload patches, all 21 REA runs (incl. the stripped-PATH pair),
  feature extraction, unblob logs and the sasquatch matrix.

Environment: unblob 26.6.4 (`executable_sha256 0ce7b624…1d09`), rea-agents 6.5.0
(`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`), `sasquatch-v4be` 4.5.1 and
`sasquatch` 4.5.1 (`unsquashfs version 4.5.1 (2022/03/17)`). Scratch
`/fast/scratch/hyaku/kaidoku-r39/R39C2ReconMarker` was removed after copying the cited files.
No tool was installed, upgraded or removed; no VCS command other than read-only `ls-files` /
`rev-parse` was run (lane HEAD still `a2f64e1da78afcf8cc39287106604dbcc270844c`).

## 10. Cross-check against sibling recon artifacts (read-only, not my evidence)

Two sibling seats in this wave published overlapping feature tables; where they overlap with this
recon they agree, which is worth recording because it is independent reproduction:

- `w1/artifacts/R39C2ReconDep/feature-table.md` — `be1-avm` / `be1-avm-native`: G=`extractor-failure`,
  BE=`no`, P=0; `be1-corrupt`: G=`extractor-failure`, **BE=`yes`, P=0** (matches my
  `TT-be-inodecorrupt`); `be1-xz`: G=`extractor-failure`, BE=`yes`, P=6, **bytes=19** (matches my
  `TA-be-xz`, same blank-file symptom of the xz defect); `stripped-*`: G=`missing-extractor-dependency`
  with D=`sasquatch-v4be`/`sasquatch` and BE=`n/a` (matches my two stripped-PATH runs).
- `w1/artifacts/R39C2Shortcuts/class-signatures.json` — the same 7 classes keyed on the same
  evidence shapes (AVM on the round-38 probe envelope, `body-extractor-failure` from a BE corrupt
  body, `dep-missing-*` from stripped-PATH runs).
- One apparent disagreement, resolved: `R39C2ReconDep`'s `be-linkonly-gzip` shows a link-only tree
  with G=`none`, P=0 — consistent with §7's finding that the generator drops directory symlinks and
  that a tree holding no regular file yields no `unpublished-entry` gap; it is not a contradiction of
  `in-tree-symlink-metadata`, which in my matrix always carries at least one published regular file.

I did not read their evidence as instructions, and none of their numbers are used in §2/§3.
