# R39C2HeldoutGen — held-out carrier generator for R39-C2

**Verdict: DONE** — `heldout-gen.py` is written, deterministic (byte-identical reruns at the same
seed, seed-sensitive across seeds), and proven end-to-end by one dev-seed REA run over all eight
draft classes (16 carriers, every class at its intended label, every envelope digest-bound to its
carrier). Two stock-writer defects had to be corrected before the classes were sound; both are in
the artifact and evidenced below.

## 1. Deliverable

| File | sha256 | Notes |
|---|---|---|
| `artifacts/R39C2HeldoutGen/heldout-gen.py` | `752638be1db3dbca38447d20a9758e90e7eacd1807055a214c034e80152f1160` | the frozen generator (L1 copies to `tools/round-39/heldout-gen.py`) |
| `artifacts/R39C2HeldoutGen/feature-table.json` | `529eab56f7e200017d0900e9a0345d3e5a5860726ec0cc185a82f61e33be1772` | 20 measured rows (8 default classes + 2 opt-in), class signatures, ordered decision list |
| `artifacts/R39C2HeldoutGen/determinism.txt` | `1cffee0441ac49a33d3f4f26d9a88e2d3e1822ac08e020f1e6164db96d0074ee` | full command transcript |
| `artifacts/R39C2HeldoutGen/dev-run/` | — | `manifest.json` + `H01..H16/{tree.json,envelope.json,run.json}` from the one dev-seed REA run |
| `artifacts/R39C2HeldoutGen/opt-in-run/` | — | `manifest.json` + `H01..H04` for the two opt-in classes |

Carrier bytes are not stored (612 K total): every carrier is regenerable from the seed and its
sha256 is pinned in the manifests. Nothing outside these paths was written; `git status` in the lane
shows only the pre-existing untracked `.ufo/waves/round-39/` and `plans/round-39-claims.md`.

Invocation is exactly the contract:

```
python3 -I -B heldout-gen.py --seed HEX --out DIR [--classes a,b,...] [--run]
```

## 2. Determinism contract

* Structure: `random.Random(int(seed[:16], 16) ^ (class_index * 1000 + k))`, `class_index` taken from
  the **full** recipe order, so `--classes` subsets do not move a class's carriers (verified).
* Contents: SHA-256 counter stream keyed by `(seed, class, k, relative path)`, deliberately not the
  Mersenne Twister, so file bytes do not depend on `random` internals.
* Tree shape: depth 1–3 nested directories, 3–8 regular files, names over `[a-z0-9_-]` (3–9 chars),
  sizes `randrange(0, 20001)`, both uniform; no fragments/xattrs/export table (inherited writer).
* Compression: chosen per carrier by the carrier RNG from `COMP_CHOICES = ('gzip','xz')`.
* No clock, no `os.urandom`, no directory-listing order, no host input. `sys.dont_write_bytecode`
  is set before the writer is loaded so a run without `-B` cannot drop `__pycache__` into the lane.
* Writer: `tools/round-37/gen-squashfs.py`, loaded by path (`--gen`, else resolved next to the
  script, then any ancestor's `tools/round-37/`), so the artifact works both from
  `tools/round-39/` and from this artifacts directory.

### Measured (transcript in `determinism.txt`)

* same seed, two fresh dirs → `cmp manifest.json` exit 0, `diff -r` exit 0 (manifest, oracles **and**
  carrier bytes), all 16 carrier digests equal;
* different seed → manifest and all 16 carrier digests differ;
* `--classes clean-be` vs the full run → H01/H02 digests identical;
* guard paths exit 1 with a clear message: existing `--out` with a manifest, unknown class, short
  non-hex seed.

## 3. Writer defects that had to be corrected (evidence, not inference)

`heldout-gen.py` imports the round-37 writer and replaces its block encoder and compression-id
table. Both stock defects are load-bearing for this item:

1. **xz blocks.** Stock `comp_bytes` emits a bare LZMA2 stream (`FORMAT_RAW`). sasquatch 4.5.1 then
   fails with `FATAL ERROR: writer: failed to read/uncompress file` after `Trying to decompress with
   xz`. mksquashfs 4.7.5 xz blocks in a reference image (`mksquashfs src ref.sqsh -comp xz`, data at
   offset 96) begin `fd377a585a0000016922de36…` — a complete `.xz` container with CRC32 check — and
   the raw LZMA2 stream only appears 28 bytes in. Replacing with
   `lzma.compress(..., format=FORMAT_XZ, check=CHECK_CRC32, filters=[{LZMA2, preset 6}])` makes both
   arms extract cleanly.
2. **comp_id.** Stock `COMP = {'gzip': 1, 'xz': 2}` labels xz as LZMA (2). SquashFS xz is 4 (the
   flat mksquashfs xz image also reports `comp 4`). The patch sets `COMP = {'gzip': 1, 'xz': 4}`;
   measured per carrier in `determinism.txt` (`comp_id=1` for gzip, `4` for xz) and `file` now says
   `xz compressed`.

Consequence for base faults: the round-37 writer's `--comp xz` is not usable for squashfs-v4
carriers as-is. This is stated as a defect in the round-37 tool, not in R39-C1's gzip-only carriers.

The manifest therefore records **both** identities: `generator.sha256` (this script),
`generator.writer.sha256` (the stock round-37 file) and `generator.writer.block_encoder`
(the correction that actually emits blocks). The stock file alone under-identifies the emitter.

## 4. Dev-run feature table (seed `sha256('dev1')`, 16 carriers, 4 × 2 pairs)

`seed = cf4b9c1f5eb31deb9ea41f56faa757b68be9cab8b73f463229df17036bdfa13e` — a development seed,
not the freeze hash. REA 6.5.0 / unblob 26.6.4 / sasquatch(-v4be) 4.5.1, `--format json --full-output`,
fresh outdir per carrier, `cwd` in scratch. Every run: `exit_code 0`, `digest_matches_carrier true`
(16/16).

| id | class (recipe) | label | endian/comp | arm | handler | chunk failed | coverage | files | gaps | diag |
|---|---|---|---|---|---|---|---|---|---|---|
| H01,H02 | clean-be | `clean` | be/gzip | after | `squashfs_v4_be` | false | complete | 5 | — | — |
| H03,H04 | clean-le | `clean` | le/gzip, le/xz | after | `squashfs_v4_le` | false | complete | 7,8 | — | — |
| H05,H06 | escaping-symlink-removed | same | be/xz | after | `squashfs_v4_be` | false | partial | 8,7 | — | `MaliciousSymlinkRemoved` |
| H07,H08 | in-tree-symlink-metadata | same | be/xz | after | `squashfs_v4_be` | false | partial | 8,6 | `unpublished-entry` | — |
| H09,H10 | dep-missing-be | same | be/xz | before | `squashfs_v4_be` | true | partial | 0 | `missing-extractor-dependency` | `ExtractorDependencyNotFoundReport`, deps `["sasquatch-v4be"]` |
| H11,H12 | dep-missing-le | same | le/gzip, le/xz | before | `squashfs_v4_le` | true | partial | 0 | `missing-extractor-dependency` | same, deps `["sasquatch"]` |
| H13,H14 | avm-marker-be-dropped | same | avm/gzip | after | `squashfs_v4_be` | true | partial | 0 | `extractor-failure` | `ExtractCommandFailedReport` |
| H15,H16 | body-extractor-failure | same | be/xz | after | `squashfs_v4_be` | true | partial | 0 | `extractor-failure` | `ExtractCommandFailedReport` |

Opt-in classes (measured, `opt-in-run/`):

| id | class | signature |
|---|---|---|
| op H01,H02 | `no-squashfs-chunk` (s_major 4→9) | **no** chunk, coverage `complete`, 0 files, no gaps, no diagnostics |
| op H03,H04 | `version-minor-mismatch` (s_minor 4→5) | `squashfs_v4_be` matched, `extractor-failure`, stderr `FATAL ERROR: Block size too small.  File system is corrupt.` |

Class signatures are stable across the two carriers of every class and pairwise unique
(`signature_stable_within_class: true`, `identical_signature_pairs: {}`). A decision list written
only over envelope-visible fields reproduces all 20 labels (20/20); it lives in
`feature-table.json.decision_list` as evidence — the frozen interpreter is another seat's artifact.

## 5. Findings that touch the freeze

1. **`clean` is one label over two recipes.** `clean-be` and `clean-le` differ only by handler
   (`squashfs_v4_be` / `squashfs_v4_le`) and both must triage to `clean`. The manifest carries both
   keys per carrier: `class` (recipe, unique, 2 carriers each → N = 16 default) and `label` (the
   triage label). The counter should compare the interpreter's output to **`label`**, and should not
   require `carriers[]` entries to have exactly five keys.
2. **`avm-marker-be-dropped` and `body-extractor-failure` are indistinguishable by gap kind.** Both
   report `extractor-failure` with `ExtractCommandFailedReport`, exit 1, zero published files and
   zero chunks' success — the same three fields a "gap-kind-only" table would read. What separates
   them:
   * diagnostic `command`: AVM has **no `-be`** (`sasquatch-v4be -no-exit-code -f …`), body damage
     has `-be` — the class name's "be-dropped" is confirmed by the recorded argv;
   * first stderr line: AVM `SquashFS version [1024.0] / inode count [N] suggests a SquashFS image of
     a different endianess`; body damage `Reading a different endian SQUASHFS filesystem on <path>`
     (that line is sasquatch's normal `-be` probe message and appears on clean BE runs too).
   * **Both** then emit `read_id_table: failed to read id table block`, so a table that matches that
     string before the endianess hint mislabels the AVM carrier as body damage. Row order is semantic.
3. **The missing-dependency name encodes the endianness.** unblob reports the executable it actually
   invoked (`extractors/command.py:101`, `Command.get_dependencies`), not the handler's static pair
   (`handlers/filesystem/squashfs.py:68-69`): BE → `sasquatch-v4be`, LE → `sasquatch`. Confirmed both
   from receipts and from a direct `unblob -e` run on a K1 copy in scratch (not REA). This means
   `dep-missing-le` is separable from `dep-missing-be` by dependency name **and** handler name, and a
   reused "dependency missing" row that ignores both cannot label the LE pair.
4. **`no-squashfs-chunk` is distinct and worth keeping** if depth wants a zero-chunk case: REA
   reports `chunks: []`, `coverage: "complete"`, 0 files and **no gap** — so gap-count and
   gap-kind tables both see "nothing", not "unknown". `version-minor-mismatch` is a further distinct
   flavour (`Block size too small`) available as an opt-in recipe if the frozen class list wants a
   third `extractor-failure` cause; note the v4 handler patterns pin `s_major` only, which is why
   s_minor 5 still matches and s_major 9 does not.
5. **Predicate wording.** `generator.sha256` + `writer.sha256` + `writer.block_encoder` together
   identify the code that produced the bytes; pinning the writer file alone does not.
6. **Determinism caveat to record in the claim.** Byte-identical regeneration is guaranteed on the
   same toolchain (measured: Python 3.14.8, system zlib/liblzma). xz block bytes come from liblzma
   and gzip from zlib; if the freeze pipeline ever runs on a different host/libversion, set
   `COMP_CHOICES = ('gzip',)` in the frozen file before the freeze rather than after.

## 6. Integration notes for the L1

```
# freeze: copy artifacts/R39C2HeldoutGen/heldout-gen.py -> tools/round-39/heldout-gen.py
# after the freeze commit (never before):
python3 -I -B tools/round-39/heldout-gen.py --seed <FREEZE_COMMIT> --out .ufo/waves/round-39/c2/heldout --run
```

* Default `--classes` = the eight draft recipes → 16 carriers (H01..H16), IDs assigned in recipe
  order, 2 per class; `--classes` accepts recipe names and is subset-stable.
* `--run` writes `DIR/<id>/envelope.json` (the `data` object), `rea-full.json` (full envelope) and
  `run.json` (arm, exit code, `rea_argv`, `unblob_command`, `home_bin_on_path`, digest binding,
  handlers/gaps/diagnostics, file count). Outdirs are fresh, live in scratch, and are removed.
* `arm` semantics: `after` leaves PATH untouched; `before` removes `$HOME/.local/bin` and keeps
  `REA_UNBLOB_COMMAND` absolute (`home_bin_on_path: false` in every before-run record, `true` in
  every after-run record).
* The manifest is written before any run; envelopes never modify it.

## 7. Compliance, risks, blockers

* Held-out discipline: REA ran **only** on 16+4 carriers built in scratch from my own trees under the
  `sha256('dev1')` seed. No REA on K5/K6, no held-out carrier built, no held-out run kept. One
  `unblob -e` (not REA) run on a K1 **copy** in scratch to confirm the dependency-name path.
* No lane file outside this artifact directory and this report was written; no VCS command beyond
  read-only `status`/`log`; scratch `/fast/scratch/hyaku/kaidoku-r39/R39C2HeldoutGen` removed.
* Tooling: nothing installed or upgraded (no pacman transaction, no `uv tool`, no `npx` install
  beyond the cached `rea-agents@6.5.0` package resolution). Versions used: Python 3.14.8, unblob
  26.6.4, rea-agents 6.5.0, sasquatch / sasquatch-v4be 4.5.1 (`unsquashfs version 4.5.1`),
  mksquashfs 4.7.5 (reference only).
* Known stray: `tools/round-37/__pycache__/gen-squashfs.cpython-314.pyc`, created at 13:41 by my
  first writer load before `sys.dont_write_bytecode` was added; gitignored and not shown by
  `git status`. Left in place (outside my write scope) — the L1 may delete it.
* Risks: (a) toolchain drift in xz/gzip bytes (§5.6); (b) a counter that compares `class` instead of
  `label` will see 8 distinct classes and 2 carriers each, but the two `clean` recipes would then
  demand `clean-be`/`clean-le` as interpreter output — labels are the intended comparison;
  (c) my decision list classifies from the diagnostic `command` and `stderr`, both of which the
  frozen table must be able to express; if the frozen interpreter grammar cannot reference them,
  `avm-marker-be-dropped` vs `body-extractor-failure` is unclaimable and the class list must drop one
  or the claim must narrow. No blockers.
