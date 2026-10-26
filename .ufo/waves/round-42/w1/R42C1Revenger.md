# R42C1Revenger — SquashFS v1–v3 through REA 6.5.0 / unblob 26.6.4: the v3 matcher rule and the predicted envelopes

**Verdict: DEFECTS FOUND** — the v3 counterpart of the round-41 extract-root rule is reconstructible and every
predicted envelope is measured (24 real REA runs, receipts in `artifacts/R42C1Revenger/receipts/`), but three draft
premises are falsified on real artefacts: **D1** a DD-WRT `tqsh` carrier cannot satisfy the draft's two-reader
oracle (neither `unsquashfs` 4.7.5 nor `7z` reads `tqsh`), **D2** the OpenWrt Kamikaze v3 images the draft names as
carriers are LZMA-compressed and `unsquashfs` 4.7.5 *fails* on them (7-Zip reads them), **D3** the round-41
`carve_ok`/`layout_ok` clauses are v4/AVM-shaped and reject three of the four measured v3 carrier shapes. Two draft
premises are **confirmed** by measurement: the dependency-missing label split (`sasquatch` vs `squashfs-v4be`,
draft step 3) and the need for a new legacy row (step 6).

Versions in play: rea-agents 6.5.0 (`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`), unblob
26.6.4 at commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`, sasquatch / sasquatch-v4be 4.5.1, `unsquashfs` 4.7.5,
`7z` 26.04. No packages installed or upgraded this seat (nothing was needed); nothing written outside this report and
`artifacts/R42C1Revenger/`.

---

## 1. The rule the exact-path matcher must use for v3

The round-41 counter selects the chunk root in exactly two places:

```
tools/round-41/c1-counter.py:287   HANDLER = 'squashfs_v4_be'
tools/round-41/c1-counter.py:288   SQUASHFS_PREFIX = 'squashfs_v4'      # derivation handlers
tools/round-41/c1-counter.py:863   if not (isinstance(h, str) and h.startswith(SQUASHFS_PREFIX)):  # in squashfs_roots()
tools/round-41/c1-counter.py:1603  d['handler_ok'] = HANDLER in chunk_handlers(env)
```

`derivations[].handler` is not REA's own vocabulary: it is unblob's `Handler.NAME`, carried through
`ChunkReport.handler_name` (`unblob/models.py:196-204`, `handler_name=self.handler.NAME`) into
`blobOrigins` and out as the edge's `handler` (`rea-agents dist/firmware/FirmwareReports.js:341-357`,
`handler: origin?.handler ?? null` at `:356`). The derivation set is REA's rendition of unblob's subtasks
(`FirmwareReports.js:341-360`), so the counter's root **is** an unblob extract directory and nothing else.

**Rule for round 42 (normative form):**

1. `HANDLER` in `handler_ok` becomes the **per-carrier frozen handler string** read from `carriers.json`
   (`handler: "squashfs_v3"` for a standard image, `"squashfs_v3_ddwrt"` etc. otherwise), tested by exact
   equality against `normalized_result.chunks[].handler`. Exact equality is required, not a prefix, because
   `squashfs_v3` is a *prefix* of `squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`
   (measured names, §2): a prefix test cannot distinguish "the frozen one" from a sibling and would let a
   carrier that unblob classified as `_ddwrt` score as a plain `squashfs_v3` carrier.
2. `SQUASHFS_PREFIX` in `squashfs_roots()` becomes the frozen **family set**
   `V3 = {'squashfs_v3', 'squashfs_v3_ddwrt', 'squashfs_v3_broadcom', 'squashfs_v3_nonstandard'}`
   with `h in V3` (segment-exact membership), used only for the *ambiguity count* and the root set. If the
   freeze prefers a regex it must be segment-bounded like `HANDLER_RE` (`c1-counter.py:314`,
   `(?<![A-Za-z0-9_-])…(?![A-Za-z0-9_-])`), never a bare `startswith`.
3. Everything downstream of the root is unchanged and stays valid: `rel()` is *whole-segment after the root*
   (`c1-counter.py:49-63`), `subject_root()` fails closed when more than one family root exists unless the
   freeze names it (`oracle_root`, `c1-counter.py:871-891`), and the `$output/` sigil is stripped exactly once
   from `child_path` (`FirmwareFiles.js:191-201`) while `files[].relative_path` stays bare
   (`FirmwareFiles.js:177`).
4. `carve_ok` and `layout_ok` must be re-specified (they are v4/AVM predicates today, see D3): v3 has no
   `mkfs_time`/`bytes_used` AVM marker and no metadata-header endianness rule; the v3 test is
   `s_major == 3` plus the magic the carrier pin claims, plus "the chunk covers the carrier or the carrier is a
   zero-padded whole" (§1.1, the measured shapes).

### 1.1 The four measured v3 extract-root shapes (this is what the matcher must survive)

| carrier shape | chunk range | derivation `child_path` (root) | receipt |
|---|---|---|---|
| zero-padded whole file (4096 B, `bytes_used` 258, zero tail) | `0..4096` | `$output/firmware.bin_extract` | `receipts/rea-v3le.json` |
| exact `bytes_used` carve (258 B) | `0..258` | `$output/firmware.bin_extract` | `rea-v3_exact.json` |
| non-zero trailing padding (`0xff`) | `0..258` + a `padding` chunk `258..4096` | `$output/firmware.bin_extract/0-258.squashfs_v3_extract` | `rea-v3_ffpad.json` |
| v3 chunk at a non-zero input offset (`'A'*4096 + image`) | `4096..8192` | `$output/firmware.bin_extract/4096-8192.squashfs_v3_extract` | `rea-v3_carved.json` |
| real nested rootfs (OpenWrt 7.09 `part2`, trailing 86016 B) | `0..1064960` inside `part2` | `…/part2_extract/0-1064960.squashfs_v3_extract` | `rea-kamikaze.json` (wave artifact, not copied) |

Consequences a v4-shaped counter gets wrong: with non-zero padding the root stops being
`firmware.bin_extract` **even though the chunk starts at offset 0**, and a `.padding` file is published into the
tree (`firmware.bin_extract/258-4096.padding`, P=3 instead of 2). Any rule that reconstructs the root from path
text or assumes "offset 0 ⇒ `firmware.bin_extract`" fails here; reading `derivations[]` (as round 41 already does)
is the only correct route.

---

## 2. Handler names actually emitted (measured, not inferred)

| input | emitted `chunks[].handler` = `derivations[].handler` | source of the name |
|---|---|---|
| standard v3 LE `hsqs`, BE `sqsh` | `squashfs_v3` | `unblob/handlers/filesystem/squashfs.py:245` |
| DD-WRT magic `tqsh` (BE) / `hsqt` (LE) | `squashfs_v3_ddwrt` | `:319` |
| Broadcom magic `qshs` (BE) / `shsq` (LE) | `squashfs_v3_broadcom` | `:364` |
| non-standard `zlqs` (LE) / `sqlz` (BE) | `squashfs_v3_nonstandard` | `:410` |
| v2 LE | `squashfs_v2` | `:159` (`squashfs_v2_nonstandard` at `:200`) |
| v1 LE | `squashfs_v1` | `:102` |
| trailing bytes that are not a chunk | `padding` (a chunk in H, no derivation) | `unblob/models.py:247` `handler_name="padding"` |
| no handler | `null` | `FirmwareReports.js:356` `origin?.handler ?? null` |

The four v3-variant fixtures shipped in the unblob tree are **byte-identical to the plain v3 fixtures**
(`sha256 4e9493d9…` for `squashfs_v3_be.bin` = `squashfs_v3_broadcom/…/squashfs_v3_be.bin`; `0161351c…` for the
LE pair): the integration fixtures exercise the magic via the shared image, and the variant handlers were therefore
tested here by patching only the 4 magic bytes of the BE and LE fixtures (rebuild commands in
`artifacts/R42C1Revenger/input-pins.tsv`). All four variant runs extracted correctly and named the variant handler.

---

## 3. The extractor argv (measured strings, from `diagnostics[].report.command`)

`SquashFSExtractor.extract` (`squashfs.py:32-66`) appends `-be` only for the BE branch, `-le` for LE, then always
`-no-exit-code -f -d {outdir} {inpath}`. Measured, verbatim:

```
sasquatch -le -no-exit-code -f -d <…>/firmware.bin_extract <…>/firmware.bin          # damaged v3 LE
sasquatch -be -no-exit-code -f -d <…>/firmware.bin_extract <…>/firmware.bin          # damaged v3 DD-WRT BE
sasquatch-v4be -be -no-exit-code -f -d <…>/firmware.bin_extract <…>/firmware.bin     # (round-41 v4 BE path, squashfs.py:40-50)
```

There is **no v3 `-be` → `sasquatch-v4be` remap**: the `sasquatch-v4be` branch is reachable only under
`match endian, self.version` = `(BIG, 4)` (`squashfs.py:39-50`), and every v1/v2/v3 handler carries an extractor
with `version` 3 or 2 (`squashfs.py:75`, `:204`, `:414`; v1 and v2 inherit `_SquashFSBase.EXTRACTOR`, `:75`).
A BE v3 chunk therefore yields `sasquatch -be …` and a **BE = `yes`** feature on a failure (measured:
`rea-v3_dmg_ddwrt_be2.json`), which matters for the C2 precedence (§7, D5).

Note the endian decision reads the magic at file position 0 of the carved chunk
(`squashfs.py:34` `get_endian(file, self.big_endian_magic)`, `file_utils.py:350-361`): it is a *magic comparison*,
never a heuristic, so `tqsh`/`qshs`/`zlqs` carriers get `-be`/`-le` from their own `BIG_ENDIAN_MAGIC`
(`squashfs.py:321`, `:366`, `:412`).

---

## 4. Dependency-missing: what the REA gap's `dependencies` list holds

**One name — the executable actually attempted — never both.** The handler-level
`SquashFSExtractor.get_dependencies()` returns `["sasquatch", "sasquatch-v4be"]` (`squashfs.py:68-69`), but that
method is consumed only by `unblob/dependencies.py:18-32` for the CLI's `--show-external-dependencies` display
(`cli.py:116`, `:181`). The report is minted inside `Command.extract`'s `FileNotFoundError` handler
(`extractors/command.py:69-77`) as `ExtractorDependencyNotFoundReport(dependencies=self.get_dependencies())`, and
`Command.get_dependencies()` returns `[self._executable]` (`extractors/command.py:101-102`).

Measured (child PATH stripped of `$HOME/.local/bin`, `REA_UNBLOB_COMMAND` absolute):

| input | `extraction_gaps[].kind` | `gaps[].dependencies` | other features |
|---|---|---|---|
| v3 standard LE | `missing-extractor-dependency` | `["sasquatch"]` | handler `squashfs_v3`, chunk `extraction_failed: true`, no derivation |
| v3 DD-WRT BE (`tqsh`) | `missing-extractor-dependency` | `["sasquatch"]` | handler `squashfs_v3_ddwrt` |
| v1 LE | `missing-extractor-dependency` | `["sasquatch"]` | handler `squashfs_v1` |
| v4 LE | `missing-extractor-dependency` | `["sasquatch"]` | handler `squashfs_v4_le` |
| v4 BE | `missing-extractor-dependency` | `["sasquatch-v4be"]` | handler `squashfs_v4_be` |

So the draft's rule-3 parenthetical is **confirmed**: every v1–v3 chunk and every v4 LE chunk resolves plain
`sasquatch`; only v4 BE resolves `sasquatch-v4be`. Two structural additions the rule text should carry:
(a) the dependency gap's `handler` is the chunk handler, `relative_path` is null, and the chunk stays in `chunks[]`
with `extraction_failed: true` — the chunk is visible, the *root is not* (no derivation, extract dir removed by
`processing.py:679` `delete_empty_extract_dir`);
(b) the report records **no argv**, so `BE` is `n/a` on this envelope (measured), never `no`.

---

## 5. Every place REA or unblob tests a handler name or the string `squashfs`

```
$ grep -rn -i squashfs <rea-agents dist>          → no matches at all
     (dist/ root; includes the bundles cli-runtime/cli.js and mcp/main-*.js)
$ grep -rn "handler_name *==\|NAME *==\|\.NAME)" <unblob>/*.py   → no matches
```

REA is handler-agnostic; it only compares against `null`:

* `firmware/FirmwareReports.js:421` — `chunks.some((c) => c.handler === null || c.encrypted === true)` → `coverage: "partial"`.
* `firmware/FirmwareReports.js:356` — `handler: origin?.handler ?? null` (the value the counter reads).
* `firmware/FirmwarePublication.js:286` — `chunkGaps("unknown-chunk-handler", (chunk) => chunk.handler === null)`.
* `firmware/FirmwarePublication.js:289-292` — `chunk.handler !== null && chunk.encrypted !== true && !dependencyChunkKeys.has(...)` → the `extractor-failure` gap.
* `firmware/FirmwarePublication.js:171` and `:229` — handler copied into the gap row, never tested.

unblob emits the name from the class attribute and never tests it: `models.py:202`, `:247` (`"padding"`),
`:267` (multi-file); `cli.py:500-502` uses it for a byte-distribution table only. The only `squashfs`-specific logic
in the whole package is `handlers/filesystem/squashfs.py` itself (patterns = `HexString` blocks, endianness =
`BIG_ENDIAN_MAGIC`, extractor argv). **Consequence:** nothing downstream can re-label a chunk, so the counter's
handler test and the oracle's handler expectation can disagree only through unblob's own pattern/validation — exactly
the failure mode a mis-patched magic produces (measured: `sqlz` BE pattern needs bytes `00 03` at 0x1c; a LE image
with only the magic patched matches *no* handler and yields an empty envelope with no gap at all — `G = ∅`,
`H = ∅`, `coverage: complete`).

---

## 6. Predicted and measured envelope features (H, G, D, BE, SR, P)

Definitions are the round-41 frozen text (`plans/round-41-claims.md:109-115`); `F` (`squashfs_` prefix of H) is the
round-42 addition. Every row below is a real receipt in `artifacts/R42C1Revenger/receipts/`, re-derived by
`artifacts/R42C1Revenger/features.py` into `features-table.json`.

### 6.1 Clean v3 run — measured, at two depths

| run | H | G | D | BE | SR | P | draft label |
|---|---|---|---|---|---|---|---|
| `--max-depth 1`, whole-file chunk | `{squashfs_v3}` | `{depth-limited}` | ∅ | `n/a` | `no` | 2 | step 8 → (`depth-limited`,`raise-depth`) |
| default depth 3, same bytes | `{squashfs_v3}` | ∅ | ∅ | `n/a` | `no` | 2 | step 12 → (`clean`,`none`) |
| real rootfs, `--max-depth 1` (OpenWrt 7.09 carve, 163 symlinks) | `{squashfs_v3}` | `{depth-limited, unpublished-entry}` | ∅ | `n/a` | `no` | 156 | step 9 is false (SR=no) → step 8 |

Prediction rule (what a *predicted* clean v3 run must satisfy): `H` holds exactly the frozen v3 handler, `G ⊆
{depth-limited, unpublished-entry}` and is empty at `max_depth ≥ 2`, `D = ∅`, `BE = n/a` (no argv is recorded on a
successful extraction), `SR = no` unless the image holds a symlink that escapes the extract root, `P` = the number
of regular files sasquatch wrote.

### 6.2 Dependency-missing v3 run — measured

`H = {squashfs_v3}` (or the variant name), `G = {missing-extractor-dependency}`, `D = {sasquatch}`, `BE = n/a`,
`SR = no`, `P = 0`, `coverage = partial`, no derivation edge. Draft step 3 → (`dep-missing-le`,
`install-extractor-le`). **Draft label confirmed.**

### 6.3 Damaged v3 run — measured (three damage sites)

`H = {squashfs_v3}` (gap handler is the chunk handler), `G = {extractor-failure}`, `D = ∅`,
`BE = no` for LE / **`yes` for BE**, `SR = no`, `P = 0`, `coverage = partial`, no derivation edge, and one
`ExtractCommandFailedReport` diagnostic carrying `command`, `exit_code: 1` and the sasquatch stderr.

Damage sites that produce it (all measured): inode-table metadata block zeroed (`[132:188)`), directory table zeroed
(`[188:246)`), fragment table zeroed (`[246:258)`), and a partial inode block (`[170:188)`). The failing chunk's
`squashfs_v3` extraction reports `stderr: get_metadata: failed to read block / FATAL ERROR: read_inode: failed to
read inode 132:64`, `exit_code: 1`. **`-no-exit-code` does not suppress this**: `sasquatch -no-exit-code -f -d …`
returns 1 on the same image outside unblob too. So a damaged v3 chunk is an `extractor-failure` envelope, not a
silent partial one.

A partial-body case (`P > 0` with `extractor-failure`, draft step 4) was **not** producible on these images:
sasquatch aborts before writing any file on every damaged variant, and unblob deletes the then-empty extract
directory (`processing.py:679`), so no derivation edge survives. `[INFERENCE]` a large real rootfs damaged late
will leave already-written files in place and yield `P > 0`; the draft's step 4 is untested by this seat.
Draft step 6 → (`legacy-body-failure`,`cross-read-legacy`) for every measured damage row; see D5 for the BE
interaction.

---

## 7. Divergences and defects against the draft

**D1 — a DD-WRT `tqsh` carrier cannot satisfy the draft's oracle.** `unsquashfs -lls` and `7z l` on a `tqsh`
image both refuse it (`FATAL ERROR: Can't find a valid SQUASHFS superblock`; 7-Zip `Cannot open the file as
archive`, rc 2), while sasquatch extracts both files. Same for `hsqt` (DD-WRT LE), `zlqs`/`sqlz`
(standard-nonstandard). Measured, `unsquashfs` 4.7.5 / `7z` 26.04:

| magic | unsquashfs 4.7.5 | 7-Zip 26.04 |
|---|---|---|
| `hsqs` / `sqsh` (standard, gzip) | reads (rc 0) | reads (rc 0) |
| `qshs` / `shsq` (Broadcom) | **fails** (rc 1) | reads (rc 0) |
| `tqsh` / `hsqt` (DD-WRT) | **fails** (rc 1) | **fails** (rc 2) |
| `zlqs` / `sqlz` (non-standard) | **fails** (rc 1) | **fails** (rc 2) |

The draft's own carrier example ("DD-WRT v24 `tqsh`") therefore has *no* non-sasquatch oracle on PATH. Either the
carrier set must be restricted to standard-magic v3, or the oracle must be `7z` (kind-aware via `7z l -slt`,
`Mode = lrwxrwxrwx` vs `-rwxr-xr-x`, measured) plus a lane stdlib v3 reader for the `tqsh`/`zlqs` family.

**D2 — the OpenWrt Kamikaze v3 images the draft names are LZMA-patched and `unsquashfs` 4.7.5 fails on them.**
Both `openwrt-wrt54g-2.6-squashfs.bin` (7.09, `sha256 3cdbe426…`) and `openwrt-brcm47xx-squashfs.trx` (8.09,
`sha256 6117a6b1…`) hold a standard `hsqs` v3.0 rootfs whose metadata blocks are **not gzip**: the first metadata
block header at `inode_table_start` decodes as a sane length (`a1 07` = 1953) and the following bytes are not
`1f 8b`. `unsquashfs` 4.7.5 dies with `gzip uncompress failed with error code -3` /
`read_fragment_table: failed to read fragment table block` / `FATAL ERROR: File system corruption detected` (rc 1)
even on the full tail; 7-Zip reads the same image and extracts all 156 regular files **byte-identically** to
sasquatch (0 differing hashes; its 80 extra files are symlink placeholders, skippable via `Mode`). sasquatch 4.5.1
extracts 156 files / 44 dirs / 163 symlinks, matching REA's `P = 156` and 163 `unpublished-entry` gaps exactly.

So the draft's premise "`unsquashfs` 4.7.5 (reads v1–v3 gzip)" is true only for **gzip** v3, and the two carriers
the draft names (DD-WRT, OpenWrt Kamikaze) are precisely the two shapes the oracle pair cannot both read. Carrier
selection must be oracle-validated before the freeze (the draft says so) — but the draft's examples must not be
copied into `carriers.json` without that check.

**D3 — `carve_ok` / `layout_ok` are v4/AVM predicates and reject three of the four measured v3 shapes.**
`c1-counter.py:109-115` requires "for a committed carrier the file size equals `bytes_used`" and
`layout_probe()` (`:682`, doc at `:97-104`) requires the AVM marker `mkfs_time == bytes_used` plus a little-endian
metadata-block header. Measured v3: a zero-padded 4096-byte carrier has chunk `0..4096` and `bytes_used` 258; a
`0xff`-padded carrier has chunk `0..258` **plus a published `.padding` file**; an exact carve has
`0..bytes_used`. v3 has no `mkfs_time`-vs-`bytes_used` field pair at all (`squashfs.py:284-315`:
`bytes_used_2`, `mkfs_time`, 64-bit `bytes_used`), so `layout_ok` must be replaced by
`s_major == 3` + the carrier's expected magic + `0 < bytes_used <= file size`, and `carve_ok` by
"`range.offset == 0` and (`range.length == file size` or `range.length == bytes_used` and the tail is zero padding
or published as `padding`)". Without that, every padded published v3 image fails before the oracle is consulted.

**D4 — the draft's rule-3 reason is wrong even though the conclusion is right.** `get_dependencies()` returning
both executables (`squashfs.py:68-69`) never reaches a report; the report carries the single attempted executable
via `Command.get_dependencies()` (`extractors/command.py:101-102`). The freeze should cite the `Command` path,
because a future unblob that reports handler-level dependencies would otherwise silently change the label split.

**D5 — C2's new step 6 must not require `BE = no`.** The handler condition in step 5 already protects the AVM
label, but a BE v3 body failure measures `BE = yes` (argv `sasquatch -be …`). If step 6 is written as
"`extractor-failure` ∈ G, P = 0, failing handler a v1–v3 handler" it fires correctly; if it inherits step 5's
`BE = no` it silently falls through to step 7 (`body-extractor-failure`) for every BE DD-WRT/Broadcom/AVM-adjacent
v3 image. The draft's step 6 text (as written) is correct — this is a hazard for the implementer, not an error in
the text.

**D6 — H carries a `padding` chunk.** Any carrier with trailing bytes publishes `padding` into `chunks[]`
(`models.py:247`), so H can be `{padding, squashfs_v3}` (measured twice). The round-42 `F` set is filtered by the
`squashfs_` prefix, so C2 is safe; a v4-style `handler_ok` written as "H contains only squashfs handlers" would not
be.

**D7 — a mis-patched magic is reported as *nothing*, not as an unknown chunk.** An image whose magic matches no
handler pattern yields `chunks: []`, `gaps: []`, `coverage: "complete"`, `files: []` — i.e. draft step 12 would
label it (`clean-empty`,`confirm-empty`) rather than (`no-squashfs-chunk`,`inspect-input`), because unblob emitted
no unknown-chunk report for a file it never matched. The `no-squashfs-chunk` label is only reachable when unblob
carved *some* other chunk, or when an `unknown-chunk-handler`/`padding` chunk exists. This is a genuine gap in the
draft's precedence text for C2's held-out set: a "wrong magic" fixture must not be generated as a bare image, or
step 2 can never fire.

---

## 8. Confidence

| claim | confidence | basis |
|---|---|---|
| emitted handler names per v3 variant | high | 24 receipts in `receipts/`; 9 clean runs name v1, v2, v3 and the three v3 variants |
| argv shape and the absent v3→v4be remap | high | verbatim `command` strings from two failing runs (LE, BE) |
| dependency list holds one name | high | 5 PATH-stripped runs; `command.py:69-77`, `:101-102` |
| root shapes (whole / carve at 0 / carve at N / nested) | high | 5 receipts with distinct shapes |
| clean / dep-missing / damaged feature tuples | high | 23 of the 24 receipts, table regenerated by `features.py` |
| partial-body (`P>0` + `extractor-failure`) tuple | low | **not observed**; sasquatch aborted with zero files on every damage site tried `[INFERENCE]` |
| v3 chunk with an escaping symlink → `SR = yes` | low | mechanism measured on a v4 fixture only (`bad_symlink.squashfs`: absolute link rewritten to a relative in-tree target, `SR = no`, one `unpublished-entry`); no v3 image with an escaping link was available `[INFERENCE]` from `extractor.py:50-93` |

What would raise the low-confidence rows: a v3 image with an absolute symlink to a path outside the root (SR=yes
path), and a large v3 rootfs truncated inside a data block after several files are already written (partial-body
path).

---

## 9. Artifacts and reproduction

All under `.ufo/waves/round-42/w1/artifacts/R42C1Revenger/`:

* `features.py` — derives (OP, PR, H, G, D, BE, SR, P, F) plus `v3_roots`/`v3_carve` from an REA receipt. This is
  the prototype of the v3 matcher rule in §1; it is the only place a prefix is used, and only for `F`.
* `features-table.json` — 24 rows, machine-derived from the receipts (no hand-typed tuple).
* `receipts/` — 24 real REA 6.5.0 receipts (388 KB total), including the depth-1 and depth-3 clean pair, all four
  variant handlers, the three damage sites, all five dependency-stripped runs, the carved/non-zero-pad shapes, the
  v4 symlink probe, and the real OpenWrt 7.09 carve (`rea-kamikaze1.json`, P=156, 163 symlinks).
* `input-pins.tsv` — bytes + sha256 + exact URL for every input, and the rebuild command for every derived input.

Run shape (every run in this seat):

```
cd "$S"   # S=/fast/scratch/hyaku/kaidoku-r42/R42C1Revenger, TMPDIR=$S
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware \
    --format json --full-output [--max-depth 1] <input> <fresh outdir>
```

Dependency-missing runs replaced the child PATH with `PATH=<node dir>:/usr/local/bin:/usr/bin:/bin` (no
`$HOME/.local/bin`), `REA_UNBLOB_COMMAND` absolute. Oracle probes: `unsquashfs -s|-lls|-no-progress -d`,
`7z l|-slt|x -snl`. Scratch (`/fast/scratch/hyaku/kaidoku-r42/R42C1Revenger`) held every third-party image and was
removed after the run; no firmware bytes entered the lane, only receipts and hashes. No VCS mutation; no write
outside this report and the artifacts directory; no tool installed.
