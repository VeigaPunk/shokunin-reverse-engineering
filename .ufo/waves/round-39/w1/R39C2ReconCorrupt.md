# R39-C2ReconCorrupt — deterministic BE-body corruption for `body-extractor-failure`

VERDICT: **DONE** — one deterministic recipe (zero the v4 id metadata block, offsets derived from
`superblock.id_table_start`) makes unblob 26.6.4 report a valid `squashfs_v4_be` chunk, exec
`sasquatch-v4be -be -no-exit-code -f …`, and fail with exit 1 before publishing any file, on four
independent fresh trees (gzip) plus an xz image; features `H={squashfs_v4_be}`,
`G={extractor-failure}`, `D={}`, `BE=yes`, `SR=no`, `P=0` on every one of them.

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base
`a2f64e1da78afcf8cc39287106604dbcc270844c` (verified with read-only `git rev-parse HEAD`; the only
worktree additions are the untracked round-39 plan and wave dirs). Nothing frozen, nothing
committed, no file written outside
`.ufo/waves/round-39/w1/artifacts/R39C2ReconCorrupt/` and this report.

## 1. Recommended recipe

`artifacts/R39C2ReconCorrupt/corrupt.py` — dependency-free, guards the header, all offsets from
superblock fields, no tree-specific constants:

```python
SB_SIZE = 96
MAGIC_BE = b"sqsh"
ZERO_BYTES = 6            # u16 metadata header (0x8000|size) + the single u32 id

def corrupt(image_bytes: bytes) -> bytes:
    b = bytes(image_bytes)
    if len(b) < SB_SIZE:                       raise ValueError(...)
    if b[0:4] != MAGIC_BE:                     raise ValueError(...)
    if struct.unpack_from(">HH", b, 28) != (4, 0): raise ValueError(...)
    bytes_used, mkfs_time = _u64(b, 40), _u32(b, 8)
    if bytes_used == mkfs_time:                # unblob drops -be for AVM-shaped headers
        raise ValueError(...)
    id_table_start = _u64(b, 48)               # -> id lookup table (u64 block offsets)
    id_meta_start  = _u64(b, id_table_start)   # -> the id metadata block itself
    out = bytearray(b)                          # body-only edit: header untouched
    out[id_meta_start:id_meta_start + ZERO_BYTES] = b"\x00" * ZERO_BYTES
    return bytes(out)
```

Why it lands exactly on the target class:

- **Chunk survives.** unblob's `_SquashFSBase.calculate_chunk` uses only `bytes_used` and the
  trailing padding, both untouched (`unblob/handlers/filesystem/squashfs.py:77-97`).
- **`-be` survives.** `SquashFSExtractor.extract` appends `-be` for `Endian.BIG, 4` whenever
  `header.bytes_used != header.mkfs_time` (same file, lines 32-50). The zeroed bytes are outside
  the 96-byte superblock, so `mkfs_time=1700000000 != bytes_used` still holds.
- **sasquatch fails in `read_id_table`**, before it creates any file:
  `read_id_table: failed to read id table block` / `FATAL ERROR: File system corruption detected`,
  exit 1 (with `-no-exit-code` present — the failure is fatal, not a warning).

Idempotent (`corrupt(corrupt(x)) == corrupt(x)`), byte-identical to every tested v1 carrier
(sha256 comparison in §5). Deliberately **not** chosen: zeroing a data block (silently succeeds on
tree `ta`), rewriting a block length (SIGSEGV 139 plus partially written files), and the two
metadata-header variants that also work but need an inode-table walk (§3).

## 2. Exact outcome on the recommended corruption

Envelope `data.normalized_result` (paths verbatim; `ta-v1`, envelope
`envelopes/ta-v1-zero-id-table.envelope.json`):

| path | value |
|---|---|
| `normalized_result.chunks[0].handler` | `squashfs_v4_be` |
| `normalized_result.chunks[0].range` / `root_file_range` | `0..781` (= whole image) |
| `normalized_result.chunks[0].extraction_failed` | `true` |
| `normalized_result.extraction_gaps[0].kind` | `extractor-failure` |
| `normalized_result.extraction_gaps[0].dependencies` | `[]` |
| `normalized_result.extraction_gaps[0].handler` | `squashfs_v4_be` |
| `normalized_result.diagnostics[0].report.__typename__` | `ExtractCommandFailedReport` |
| `normalized_result.diagnostics[0].report.command` | `sasquatch-v4be -be -no-exit-code -f -d /tmp/rea-firmware-…/extracted/firmware.bin_extract /tmp/rea-firmware-…/firmware.bin` |
| `normalized_result.diagnostics[0].report.exit_code` | `1` |
| `normalized_result.diagnostics[0].report.stderr` | base64 of `Reading a different endian SQUASHFS filesystem on …\nread_id_table: failed to read id table block\nFATAL ERROR: File system corruption detected\n` |
| `normalized_result.files` / `.published_bytes` / `.coverage` | `[]` / `0` / `partial` |
| `normalized_result.unpublished_entries` | `[]` |
| `data.evidence_id` | `ev_5f0cf21de2ae41f76cb620348ac68fab33b93a45e2b5b5c19a32e0630c5c20da` (`ta-v1`) |
| top-level `ok` | `true`, `meta.command = extract-firmware`, REA exit 0 |

unblob's own log for the same carrier (`unblob-logs/ta-v1.unblob.log`) shows the two decisive
lines verbatim: `Running extract command command='sasquatch-v4be -be -no-exit-code -f -d …'` and
`Extract command failed … exit_code=0x1`.

## 3. Variant sweep (all five tried, three trees, plus xz and a symlink tree)

`REA` = rea-agents 6.5.0 `extract-firmware --format json --full-output`; all 25 runs exited 0 with
`ok:true`. `files` = files left on disk by the direct `sasquatch-v4be -be` probe.

Chunk found: **yes for all 15 corrupted variants on ta/tb/tc**, always one `squashfs_v4_be` chunk
covering `0..len(image)` (`unblob.log`: `Found valid chunk chunk=0x0-0x30d handler=squashfs_v4_be`),
so the handler column below is never empty. `chunks[].extraction_failed` is `true` for every
v1/v3/v4/v5 run and for `tb`/`tc` under v2, and `false` for `ta` under v2 — the only variant where
damage went unnoticed.

| variant | tree | direct exit | files | sasquatch stderr first line | fatal / failure line | REA features (H, G, D, BE, SR, P) |
|---|---|---|---|---|---|---|
| v1 zero id table | ta | 1 | 0 | `Reading a different endian SQUASHFS filesystem on img/ta-v1-zero-id-table.sqsh` | `read_id_table: failed to read id table block` + `FATAL ERROR: File system corruption detected` | H={squashfs_v4_be} G={extractor-failure} D={} BE=yes SR=no P=0 |
| v1 | tb | 1 | 0 | same text, `img/tb-…` | same | identical |
| v1 | tc | 1 | 0 | same text, `img/tc-…` | same | identical |
| v1 | td (symlinks) | 1 | 0 | same text, `img/td-be-gzip-v1.sqsh` | same | identical (SR stays `no`) |
| v1 | ta xz | 1 | 0 | same text, `img/ta-be-xz-v1.sqsh` | same | identical |
| v2 zero first data block | ta | **0** | 3 | same text | none — extraction **succeeds**, file content silently zeroed | H={squashfs_v4_be} G={} D={} BE=n/a SR=no P=3 |
| v2 | tb | 1 | 3 (0 bytes each) | same text | `FATAL ERROR: writer: failed to read/uncompress file …/root.cfg` | H={squashfs_v4_be} G={extractor-failure} D={} BE=yes SR=no **P=3** (all size 0) |
| v2 | tc | 1 | 3 (one 0-byte) | same text | `FATAL ERROR: writer: failed to read/uncompress file …/top.dat` | H={squashfs_v4_be} G={extractor-failure} D={} BE=yes SR=no **P=3** |
| v3 flip inode type | ta/tb/tc | 1 / 1 / 1 | 0 / 0 / 0 | same text | `FATAL ERROR: File system corrupted - invalid type in inode (type: 65282)` | H={squashfs_v4_be} G={extractor-failure} D={} BE=yes SR=no P=0 on all three |
| v4 zero directory table | ta/tb/tc | 1 / 1 / 1 | 0 / 0 / 0 | same text | `get_metadata: failed to read block` → `FATAL ERROR: dir_scan: failed to read directory …` | H={squashfs_v4_be} G={extractor-failure} D={} BE=yes SR=no P=0 on all three |
| v5 block length → 2 | ta/tb/tc | **139 (SIGSEGV)** | 3 / 3 / 3 | same text | none — process segfaults mid-write | H={squashfs_v4_be} G={extractor-failure} D={} BE=yes SR=no **P=3** (`published_bytes` 2648/0/35500) |

Stability verdict: **v1** is the only variant that (a) is bit-for-bit tree-independent in outcome,
(b) leaves zero files, (c) needs no inode/dir parsing. v3 and v4 are equally stable on the envelope
features but each needs one more parser step (inode-table payload / `directory_table_start`) and
carry tree-shape-dependent error text; they are valid fallbacks if the freeze prefers a different
`corrupt()` body. v2 and v5 are rejected: partial publishing makes `P` unreliable, and v2 even
succeeds silently on one tree.

## 4. Class separation measured this wave (feeds the triage table)

Every row is an REA envelope in `envelopes/`, features computed by `envelope_features.py`
(H = squashfs handlers, G = gap kinds, D = gap dependencies, BE = `-be` token in a recorded
sasquatch command, SR = `MaliciousSymlinkRemoved`, P = `len(normalized_result.files)`):

| class | carrier | H | G | D | BE | SR | P | notes |
|---|---|---|---|---|---|---|---|---|
| clean | `ta/tb/tc-clean` | `{squashfs_v4_be}` | `none` | `{}` | n/a | no | 3 | `coverage=complete`, `published_bytes` 2683/11120/45740 |
| in-tree symlink only | `te-clean` | `{squashfs_v4_be}` | `{unpublished-entry}` | `{}` | n/a | no | 1 | `unpublished_entries[].kind=symlink` |
| escaping symlink only | `tf-clean` | `{squashfs_v4_be}` | `none` | `{}` | n/a | **yes** | 1 | `MaliciousSymlinkRemoved` |
| in-tree + escaping | `td-clean` | `{squashfs_v4_be}` | `{unpublished-entry}` | `{}` | n/a | **yes** | 1 | both signals at once |
| **body damage** | `ta/tb/tc/td-v1`, `ta-xz-v1` | `{squashfs_v4_be}` | `{extractor-failure}` | `{}` | **yes** | no | 0 | this seat's target |
| AVM marker (round-38 probe, re-read only) | `…/round-38/w2/…/rea-k1-avm.json` | `{squashfs_v4_be}` | `{extractor-failure}` | `{}` | **no** | no | 0 | same G, distinguished only by `-be` |
| missing BE dependency (control) | `ta-clean-nodep` | `{squashfs_v4_be}` | `{missing-extractor-dependency}` | `{sasquatch-v4be}` | n/a | no | 0 | `ExtractorDependencyNotFoundReport`, no `command` recorded |

Consequences worth freezing into the interpreter grammar:

1. `BE` is the *only* discriminator between `body-extractor-failure` and `avm-marker-be-dropped`;
   `G`, `D`, `SR`, `P` are identical. Measured, not inferred.
2. `BE` is `n/a` (not `no`) whenever extraction never ran: clean runs and the dep-missing control.
   A row that writes `no` for the AVM class and `*` elsewhere is fine, but a row that writes
   `-be in child argv = *` for `body-extractor-failure` swallows the AVM class.
3. `dependencies` for the dep-missing classes is a singleton from the *resolved executable*
   (`unblob/extractors/command.py:68-71` FileNotFoundError branch → `Command.get_dependencies()`,
   `command.py:100-101`, `return [self._executable]`), so `sasquatch-v4be` for BE and `sasquatch`
   for LE. Handler cell separates them anyway.
4. `P` must not be `0` in the failure rows unless the frozen generator is guaranteed to use v1:
   v2/v5 produce `extractor-failure` with `P=3` (v2 even with `published_bytes=0`). Recommended
   cells: `published files = *` for both failure rows; `>0` for the three symlink/clean rows.
5. A body-corrupted carrier may legitimately contain symlinks; `td-v1` shows `SR=no`, `P=0`, i.e.
   extraction failure preempts symlink sanitisation, so `symlink removed = *` is safe for the
   body row and `no` is also observed-true for a symlink-free tree.

A concrete row block that matches every envelope above (first-match order; the L1 owns the final
table and its `cause -> action`/`source` text):

```
| label | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | cause -> action | source |
| dep-missing-be | squashfs_v4_be | missing-extractor-dependency | sasquatch-v4be | * | * | * | … | … |
| escaping-symlink-removed | squashfs_v4_be | none | * | * | yes | >0 | … | … |
| in-tree-symlink-metadata | squashfs_v4_be | unpublished-entry | * | * | * | >0 | … | … |
| body-extractor-failure | squashfs_v4_be | extractor-failure | none | yes | * | * | … | … |
| avm-marker-be-dropped | squashfs_v4_be | extractor-failure | none | no | * | * | … | … |
| clean-be-extracted | squashfs_v4_be | none | * | n/a | no | >0 | … | … |
```
(`clean-be-extracted` last: it is the only remaining `G=none, SR=no` shape. `dep-missing-le` would
be `handler=squashfs_v4_le, dependencies=sasquatch`; out of this seat's item.)

## 5. Verification actually run

- `corrupt()` output reproduced the scratch-built v1 carriers byte-for-byte for
  `ta/tb/tc/td` gzip and `ta` xz (sha256 equality, §build.md), and is idempotent.
- Guards exercised: `hsqs` (LE) input → `ValueError: not a standard big-endian SquashFS image`;
  `--endian avm` image (`bytes_used == mkfs_time`) → `ValueError: AVM-shaped header …: unblob
  drops -be`; short input → `ValueError: shorter than a SquashFS v4 superblock`.
- 25 REA runs, all exit 0 with `ok:true`: 15 corrupted runs (5 variants × ta/tb/tc), 2 extra
  corrupted (td-v1 on the symlink tree, ta-xz-v1 on an xz image), 6 clean basis runs (ta/tb/tc/td/
  te/tf), 1 dep-missing control, 1 `ta-v1` rerun in a second outdir. The rerun reproduces the same
  feature vector with a different `evidence_id` (outdir/`local_path` differ), so features are
  repeatable and evidence ids are not.
- 20 direct `sasquatch-v4be -be -no-exit-code -f -d …` probes with recorded exit codes and stderr
  (`sasquatch-stderr/`).
- `python3 file` on the clean images: `Squashfs filesystem, big endian, version 4.0, zlib
  compressed, 781/1433/1820 bytes … blocksize: 4096 bytes`.

Nothing was installed or upgraded (unblob 26.6.4, rea-agents 6.5.0, sasquatch-v4be 4.5.1 already
present; pacman untouched). Scratch `/fast/scratch/hyaku/kaidoku-r39/R39C2ReconCorrupt` was
removed after the artifacts were copied; no scratch or `/tmp` path is cited as evidence except
inside saved envelope `subject.local_path` fields, which are REA's own record and not durable.

## 6. Risks / limits (read with the freeze)

1. The recipe assumes the v4 id lookup table is a `u64` array whose first entry points at the id
   metadata block — true for every image `tools/round-37/gen-squashfs.py` writes (`no_ids = 1`).
   With `no_ids > 1` the first entry is still the first id block, but that shape was not built or
   tested; the function raises rather than guessing when the geometry does not resolve.
2. Only gzip and xz compression shapes were exercised (the generator's whole range). A compressed
   id metadata block is not producible with this generator; zeroing its 2-byte header would still
   break it, but that is [INFERENCE], not measured.
3. v1 zeroes 6 bytes; 2 would likely suffice. 6 is what was measured on all carriers.
4. `body-extractor-failure` carriers must be built from images whose header keeps
   `bytes_used != mkfs_time`; `corrupt()` refuses AVM-shaped headers for exactly that reason, so a
   held-out generator cannot silently drift into the AVM class.
5. Held-out discipline respected: no K5/K6 carrier was built or run, and every carrier here comes
   from trees authored in scratch this wave.
6. The direct-probe stderr first line is identical for all variants (sasquatch's banner); the
   discriminating line is the second/third, which is why the table records both.
