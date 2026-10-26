source: S112 — https://github.com/onekey-sec/unblob/blob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — tag 26.6.4 = commit 1fcc7a0a584a70a96c31f5a276c20944d199a089, 590 lines, sha256 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287: `SquashFSv4BEHandler` NAME `squashfs_v4_be`, pattern `73 71 73 68 [24] 00 04`, `EXTRACTOR = SquashFSExtractor(4, 0x73_71_73_68)`, `V4BE_EXECUTABLE = "sasquatch-v4be"`, `-be` appended only when `bytes_used != mkfs_time`; it does not establish REA behaviour or any carrier property
source: S113 — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs/squashfs_v4_be — the fixture bytes and expected `__output__` of K3 (`__input__/squashfs_v4.bin`, identical to `.4kpad.bin`, 4096 B sha256 9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0) and K4 (`__input__/squashfs_v4.nopad.bin`, 307 B sha256 a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed), stored as Git-LFS pointers; it does not establish extractor behaviour
source: S114 — https://github.com/Freetz-NG/freetz-ng/blob/master/docs/wiki/60_Development/squashfs4-be.en.md — the AVM-BE format note of which the committed `.ufo/waves/round-37/probes/avm.txt` is the body minus its H1 (upstream raw sha256 100948f38ea0ff7258eee00a420e67b090fd9a1e7e191361d03b9a9604875fc9; local copy sha256 c1c43f6f97d7477dcdab15203d11e43b49beb12e3a43a3b52bdd71b672a9a5d5): block-length field stays little-endian, `mkfs_time` equals `bytes_used`, XZ; it does not establish that any tool decodes AVM-BE and no carrier here is AVM-BE
source: S115 — 7-Zip 26.04 (x64) 2026-10-05, local tool — rejected as a big-endian SquashFS v4 reader (section "Gate-relevant quotes"); the rejection covers the listing path only
source: S116 — `tools/round-37/gen-squashfs.py` (lane own-work) — the generator that produced the K1/K2 synthetic standard-BE v4 gzip carriers; it does not make them independent of the lane
verified-at: 2026-10-26, access window 06:16:41Z–06:24:00Z; carrier pins recomputed from the committed bytes at base 77091b492cc53f8743bd0701b1e7d5e66123dd84 (four `sha256sum` runs agree with `.ufo/waves/round-38/c1/carriers.json`); receipt counts re-derived at 06:23Z from the wave-1 draft envelopes named below, which are **not yet committed**; the frozen C1 counter at freeze e059ca9391642d5b71b6662cabcbdce0d9308719 and at tip cb4326b2aa4c2024af0651fe6115b82d0c4de3df reports `carriers_matched 0`, `entry_present false`, `sourced false`
recheck: on-release of rea-agents or unblob, otherwise 180d — `S=$(mktemp -d /fast/scratch/hyaku/recheck-r38.XXXX) && REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob TMPDIR=$S bash tools/round-38/c1-run.sh after corpus/evidence/round-37/c1/K4/carrier.bin "$S/K4" >/dev/null && jq -c '.normalized_result|{files:(.files|length),gaps:(.extraction_gaps|length),handlers:[.chunks[].handler]}' "$S/K4/after.json"` → expect `{"files":4,"gaps":0,"handlers":["squashfs_v4_be"]}` on a host with `sasquatch-v4be` on `PATH`; `rm -rf "$S"` after

# Big-endian SquashFS v4: the `squashfs_v4_be` handler extracts through `sasquatch-v4be`, and gap-free depends on the link, not the endianness

## Question and novelty

The lane's Frontier note held that big-endian SquashFS v4 (`sasquatch-v4be`) was unmeasured
(`PROVINCE.md` bullet `sasquatch`, the round-36 Core row's "big-endian sibling, unmeasured",
`corpus/README.md` `## Frontier`). The round-36 entry measured only little-endian v4. This entry
records what REA `extract-firmware` (rea-agents 6.5.0, unblob 26.6.4) actually does with standard
big-endian v4: which handler it dispatches, which external binary performs the extraction, which
oracle rows are published, and where the "no extraction gap" statement stops being true.

Two premises from round 37 are corrected here, and one is refused:

- **Corrected — the dependency is named.** The BE handler depends on `sasquatch-v4be`, not on the
  LE `sasquatch`. A `missing-extractor-dependency` gap on the BE handler lists
  `dependencies: ["sasquatch-v4be"]` (observed below).
- **Refused — "no external extractor".** unblob 26.6.4 contains no in-process SquashFS reader; the
  handler always shells out to `sasquatch-v4be` for BE v4 (S112, and the observed argv below).
  Extraction is *driven* by unblob and *performed* by an external binary that REA does not install.
- **Reproduces, contrary to the round-37 reading** — the `missing-extractor-dependency` gap itself.
  It appears whenever `sasquatch-v4be` is not resolvable by the unblob subprocess. Round 37 read
  that gap as a property of big-endian images; it is a property of the environment.

## Carriers, pins and counts

Carrier set frozen before any round-38 after-run in `.ufo/waves/round-38/c1/carriers.json`; oracle
rows frozen at the same commit in `corpus/evidence/round-37/c1/K*/oracle.tsv`.

| carrier | kind (carriers.json) | size | carrier sha256 (recomputed) | oracle rows |
|---|---|---|---|---|
| K1 | synthetic standard-BE v4 gzip, tree 1 (S116) | 9780 B | `1cfb6c33f915aa64255465fba9f2074bb0f294a192f3e3058cb34bea8286117e` | 5 |
| K2 | synthetic standard-BE v4 gzip, tree 2, symlink + space in a name (S116) | 1606 B | `403cb0a827966bbe17a70e08af7d39b43260da8201d1b9001bbc4228cbc99154` | 3 |
| K3 | unblob 26.6.4 fixture `squashfs_v4_be` (4kpad) (S113) | 4096 B | `9c7c523c5d1d1cafc0b679af9092ce0289d9656f6a24bc3bd0009f95b69397c0` | 4 |
| K4 | unblob 26.6.4 fixture `squashfs_v4_be` (nopad) (S113) | 307 B | `a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed` | 4 |

Commands: `sha256sum corpus/evidence/round-37/c1/K*/carrier.*` → the four digests above;
`wc -l corpus/evidence/round-37/c1/K*/oracle.tsv` → `5 3 4 4 16 total`.

K1/K2's oracle is the committed pre-image source tree (`corpus/evidence/round-37/c1/K*/src`,
regular files + one symlink each), so their expected record is ground truth, not a second reader.
K3/K4's oracle is the unblob project's own `__output__/squashfs_v4{,.nopad}.bin_extract/apple{1..4}.txt`
(S113, 7 B each): independent of the REA run, **not** independent of unblob.

## What the four after-runs publish

`tools/round-38/c1-run.sh after CARRIER OUTDIR` runs
`npx -y rea-agents@6.5.0 extract-firmware --format json CARRIER OUTDIR` with
`REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` (unblob 26.6.4, executable sha256
`0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`).

| carrier | chunks[].handler | files published | oracle rows matched (path suffix + sha256) | `extraction_gaps` | `coverage` | `published_bytes` |
|---|---|---|---|---|---|---|
| K1 | `squashfs_v4_be` | 5 | 5/5 | 0 | `partial` | 9656 |
| K2 | `squashfs_v4_be` | 3 | 3/3 | **1** (`unpublished-entry`) | `partial` | 10283 |
| K3 | `squashfs_v4_be` | 4 | 4/4 | 0 | `complete` | 28 |
| K4 | `squashfs_v4_be` | 4 | 4/4 | 0 | `complete` | 28 |

Command (one per receipt):
`jq -c '.normalized_result|{files:(.files|length),bytes:.published_bytes,gaps:(.extraction_gaps|length),cov:.coverage,handlers:[.chunks[].handler]}' RECEIPT`
→ K1 `{"files":5,"bytes":9656,"gaps":0,"cov":"partial","handlers":["squashfs_v4_be"]}`;
K2 `{"files":3,"bytes":10283,"gaps":1,"cov":"partial",…}`;
K3 `{"files":4,"bytes":28,"gaps":0,"cov":"complete",…}`;
K4 `{"files":4,"bytes":28,"gaps":0,"cov":"complete",…}`.
Oracle matching re-implemented exactly as the frozen counter does it (`sha256` equal and path equal
or `/<oracle-rel>` suffix) → `5 3 4 4` hits out of `5 3 4 4`.

Byte arithmetic checks the published set: K1 9656 = 18 + 9000 + 609 + 0 + 29; K2 10283 = 22 + 21 +
10240; K3 = K4 = 28 = 4 × 7.

Every chunk record for all four carriers is the whole file (`root_file_range {offset: 0, length:
<carrier size>}`, `extraction_failed: false`), i.e. the carrier is the payload and no carve precedes
recursion. Members are published under `firmware.bin_extract/…` with the in-image relative path as
suffix — hence the predicate's suffix rule rather than path equality.

**The four-of-four "no gap" statement is false as written: K2 carries one gap.** It is
`kind: "unpublished-entry"`, `relative_path: "firmware.bin_extract/var/lib/run-link"`, a
`symlink` with `link_target: "../../a/run.sh"`, `dependencies: []`, continuation id
`602c674b7f83f4acd6bf01c5655a5dd669f206d33ee3bc9b8bc2c0ba9f08cfca`. Command:
`jq -r '.normalized_result.unpublished_entries[]?|"\(.kind) \(.relative_path) -> \(.link_target)"' RECEIPT`.

## Gap-free depends on the link target, not on the endianness

K1 has the same shape of content as K2 — one symlink — but **zero** gaps and zero
`unpublished_entries`. Its symlink is `link-to-hello -> ../hello.txt`, whose resolved target lies
outside the image root; REA drops it and records a diagnostic instead:

```json
{"input_path": "$input", "report": {"__typename__": "MaliciousSymlinkRemoved", "severity": "WARNING",
 "link": "…/firmware.bin_extract/link-to-hello", "target": "…/extracted/hello.txt"}}
```

K2's `var/lib/run-link -> ../../a/run.sh` resolves inside the image and is retained as metadata,
which under the handler's publish policy costs one `unpublished-entry` gap. Consequences:

- A BE v4 image with an escaping symlink can be gap-free and still `coverage: "partial"` (K1);
  coverage is not a function of the gap list alone.
- A BE v4 image with a normal in-tree symlink cannot be gap-free (K2), exactly as the round-36
  entry found for LE v4. **Symlink policy is endian-independent**; only regular files are compared
  by the frozen oracle in either round.

## The extractor is a declared dependency, and REA installs nothing

Observed on the K3/K4 runs (`.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/unblob-command-K{3,4}.txt`):

```
sasquatch-v4be -be -no-exit-code -f -d <outdir>/carrier.bin_extract <carrier>
```

This is the argv S112 builds for `Endian.BIG, 4` when `not is_avm` (L40-50) plus the tail
`-no-exit-code -f -d {outdir} {inpath}` (L58-62). `get_dependencies()` returns
`["sasquatch", "sasquatch-v4be"]` for the squashfs handlers (L68-69), and
`Command.extract` turns `FileNotFoundError` into an `ExtractorDependencyNotFoundReport`
(`extractors/command.py` L69-77, as read by the wave-1 scout; S112/S108).

The same carrier with the binary absent produces the round-37 gap verbatim:

| field | value |
|---|---|
| `kind` | `missing-extractor-dependency` |
| `handler` | `squashfs_v4_be` |
| `dependencies` | `["sasquatch-v4be"]` |
| `root_file_range` | `{offset: 0, length: 4096}` |
| files published | 0 |
| `coverage` | `partial` |
| continuation id | `4ca863d04cc06d61e7be38d0811847a15f55c70f028fdf45e8fefdf75957a07a` |

So the "missing extractor" record is a statement about the host, not about the image, and it names
the BE binary specifically. With `sasquatch-v4be` installed the same input publishes 4/4 with zero
gaps; REA itself installs nothing, and its own continuation says so (quote in the Gate section).

## Cross-tool agreement: same binary, different driver

`tools/round-38/c1-run.sh oracle` runs `sasquatch-v4be -be -d OUT CARRIER` directly
(`unsquashfs version 4.5.1 (2022/03/17)`, sha256
`fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6`, the official onekey-sec deb
member). Regular-file sets match the REA receipts exactly:

| carrier | direct `sasquatch-v4be -be` rows | REA receipt rows | path+sha diff | oracle vs source tree |
|---|---|---|---|---|
| K1 | 5 | 5 | identical | identical |
| K2 | 3 | 3 | identical | identical |
| K3 | 4 | 4 | identical | — |
| K4 | 4 | 4 | identical | — |

Command: `wc -l sasquatch-v4be-K*.tsv harness-oracle-K*.tsv` → `5 3 4 4` each, and the comparison
table above is `.ufo/waves/round-38/w1/artifacts/R38CrossToolK4/oracle-compare.tsv`.

**Read this as driver parity, not as two-implementation agreement.** The binary the direct leg runs
is the binary the handler invokes; a disagreement would indicate an argv or output-directory bug,
not an image ambiguity. The independent anchors are elsewhere: K1/K2 against the committed source
trees (byte-identical, symlink included in the listing), K3/K4 against the project's own
`__output__`.

## Other readers refuse big-endian v4

Sweep over all four carriers (`R38CrossToolK4/7z-refusal.txt`, `unsquashfs-refusal.txt`):

| reader | version | exit | output |
|---|---|---|---|
| `/usr/bin/unsquashfs` | 4.7.5 (2026/03/01) | 1 on 4/4 | `Reading a different endian SQUASHFS filesystem` + `FATAL ERROR: Can't find a valid SQUASHFS superblock` |
| `7z` | 26.04 (x64) 2026-10-05 | 2 on 4/4 | `ERROR: … : Cannot open the file as archive`, `Errors: 1` |

Neither refusal distinguishes standard BE v4 from AVM-BE; both are simply out of scope for those
readers. This is why the sasquatch build matters at all on a Linux host.

## AVM-BE stays Frontier

- No carrier in the lane is AVM-BE; all four are standard BE v4. Observed on the two fixture
  carriers (big-endian superblock parse): `magic sqsh`, version 4.0, compressor gzip (id 1),
  `mkfs_time 1646222857`, `bytes_used 307` — `mkfs_time != bytes_used`, so the handler's AVM test
  is false and `-be` is passed. The inode-table metadata header at offset 121 reads big-endian
  (`00 3a` = 58), whereas AVM-BE keeps the block length little-endian. [source: wave-1 scout
  `.ufo/waves/round-38/w1/R38ScoutFreetzAvm.md`; the parse itself was not re-run here]
- The AVM route (S114): block-length field little-endian, `mkfs_time == bytes_used`, XZ — and
  S112 omits `-be` when the AVM test holds. That is a *source-level route*, never measured.
- Therefore the frontier note's "big-endian/AVM stays Frontier" is correct for AVM and
  vendor-mangled images, and wrong only for standard BE v4, which the four carriers represent.

## Gate-relevant quotes (each ≤25 words)

Source quotes:

> `EXECUTABLE = "sasquatch"` / `V4BE_EXECUTABLE = "sasquatch-v4be"` — S112, L24-26

> `case Endian.BIG, 4:` / `executable = self.V4BE_EXECUTABLE` — S112, L40-41

> `is_avm = header.bytes_used == header.mkfs_time` / `if not is_avm:` / `commands_args.append("-be")` — S112, L48-50

> `REA installs nothing. Add the named dependency to your own environment and rerun extract_firmware on the same immutable input` — REA continuation `4ca863d0…`, observed in the K3 missing-dependency envelope

> `the only data field stored in the little-endian format is the block length value at the beginning of each block` — S114 (AVM-BE block length)

> `super-block field 'mkfs_time' contains (instead of the filesystem creation time) the same value as the super-block field 'bytes_used'` — S114 (AVM-BE marker)

> `oid sha256:a29ddc15f5a6abcabf28b7161837eb56b34111e48420e7392e648f2fdfe956ed / size 307` — S113, K4 `__input__` LFS pointer

Tool-output quotes (not sources):

> `ERROR: … : Cannot open the file as archive` — 7-Zip 26.04, 4/4 carriers; basis of the S115 rejection (flip: a 7-Zip release that lists `sqsh`/BE v4)

> `FATAL ERROR: Can't find a valid SQUASHFS superblock` — unsquashfs 4.7.5, 4/4 carriers

## What this is not claimed to show

- **Not that stock unblob needs no external extractor.** The opposite: the handler always runs
  `sasquatch-v4be` for BE v4. "Stock unblob" means unblob's *own* handler and argv, not an
  in-process reader.
- **Not four-of-four gap-free.** K2 keeps one `unpublished-entry` gap for its in-tree symlink.
- **Not a claim that the frozen C1 target is met.** With these receipts the frozen counter's
  `after_gaps_empty` binding fails on K2, so `carriers_matched` cannot exceed 3. The frozen
  predicate and carrier set are reported, not changed, from this seat.
- **Not an independent-implementation cross-check.** The `sasquatch-v4be` oracle leg runs the same
  binary the handler runs.
- **Not AVM-BE, not vendor-mangled images** (Broadcom `qshs` and the other non-standard handlers in
  S112 are unexercised), **not other unblob/rea-agents versions**, **not non-v4 SquashFS**.
- **Not member semantics.** Regular files only; modes, uid/gid, mtime, xattrs and symlink targets
  are not compared; nothing was executed, and `max_depth: 3` with empty `depth_limited_paths` on
  all four receipts means no recursion limit was hit.
- **Not committed evidence yet.** The receipts named here are wave-1 draft envelopes under
  `.ufo/waves/round-38/w1/artifacts/`; the claim receipts land at
  `corpus/evidence/round-38/c1/K*/after.json`. Numbers above are re-derived from the drafts at
  2026-10-26T06:23Z.

## Sources

| id | source | what it grounds here | what it does not |
|---|---|---|---|
| S112 | unblob `squashfs.py` at tag `26.6.4` | BE v4 handler name/pattern, `EXTRACTOR`, `V4BE_EXECUTABLE`, the `-be`/AVM argv rule, `get_dependencies()` | REA's envelope shape, any carrier, any gap record |
| S113 | unblob `squashfs_v4_be` integration fixtures at `26.6.4` | K3/K4 carrier bytes and the `__output__` expectations, the LFS-pointer storage rule | extractor behaviour, oracle independence from unblob |
| S114 | Freetz-NG SquashFS 4 (BE) note | the AVM-BE format properties behind the Frontier reject, and that `avm.txt` is that page's body | any measurement, any AVM carrier |
| S115 | 7-Zip 26.04 | the refusal being a property of this reader version (rejected row, flip stated) | anything about SquashFS correctness |
| S116 | `tools/round-37/gen-squashfs.py` | K1/K2 carrier provenance and that they are lane-authored | independence of the K1/K2 oracle (that comes from the committed `src` trees) |
| S107, S108, S110, S111 | sasquatch release, unblob handler at the old path, unblob README, devttys0 README | sasquatch binary provenance and digests; the "install sasquatch" producer statement; that the devttys0 README says nothing about big-endian | — (all four already mined by the round-36 entries) |

## Receipts (draft, wave 1)

| carrier | draft envelope | stored evidence id |
|---|---|---|
| K1 | `.ufo/waves/round-38/w1/artifacts/R38ExecProvincePatch/after-K1.json` | `ev_eccca7337fd7dfe589a…` |
| K2 | `.ufo/waves/round-38/w1/artifacts/R38ExecAfterK2/after.json` | `ev_4d478254a54b7c732ae…` |
| K3 | `.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/diagnostic-after-with-declared-extractor.json` (4/4, 0 gaps); `.ufo/waves/round-38/w1/artifacts/R38ExecAfterK3/after.json` (0 files, 1 `missing-extractor-dependency`) | `ev_096b500d37e879c18ac…`; `ev_bb5d941f43f9362d9f7…` |
| K4 | `.ufo/waves/round-38/w1/artifacts/R38ExecAfterK4/after.json` | `ev_3d1197d1126eaa4660a…` |

Limit worth knowing when reading these ids: three runs over the same K4 subject
(`a29ddc15…56ed`) stored `ev_3d1197d1…`, `ev_de83842f…`, `ev_b62e21b8…` under `xpin-attribute.mjs`
(`id = 'ev_' + digestCanonicalValue(semanticProjection(evidence), 'Evidence')`), so the id
identifies the whole evidence record — including `parameters.output_directory` — not the subject
digest alone. The frozen counter only requires per-envelope recompute equality, which holds.
