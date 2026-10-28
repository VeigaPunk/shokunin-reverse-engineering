# R44C1Counter — R44-C1 counter port (round 44, wave 1)

Seat: `R44C1Counter` (executor, leaf). L1: `KaidokuR44`. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base `c29360e3ba5381a5ab69e372d0d9577970f85018`.

**Deliverable.** `tools/round-44/c1-counter.py` (installed at the L1's request; the canonical copy is
`.ufo/waves/round-44/w1/artifacts/R44C1Counter/c1-counter.py`, byte-identical).

| item | value |
|---|---|
| counter bytes / lines | 152655 B / 3374 lines |
| **counter sha256** | `9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993` |
| authored path | `.ufo/waves/round-44/w1/artifacts/R44C1Counter/c1-counter.py` |
| installed path | `tools/round-44/c1-counter.py` (`cp`, mode 755, same digest) |
| oracle merge snippet | `.ufo/waves/round-44/w1/artifacts/R44C1Counter/carriers.oracle-merge.json` |
| dev harness | `.ufo/waves/round-44/w1/artifacts/R44C1Counter/probe-real-carriers.py` |
| receipts | `.ufo/waves/round-44/w1/artifacts/R44C1Counter/receipts.json`, `receipts/*.json` |
| installs/updates | none |

Installed, **not committed, not pushed**; no check or test was run after the install (byte identity
verified with `sha256sum`, both digests equal). C1's after-side data procedure
(`tools/round-44/c1-run.sh`) was never run; `corpus/evidence/round-44/c1/` was never written.

## 1. Target set — exactly four ids

`EXPECTED_IDS = ('v1le','v1be','v2le','v2be')`, `TARGET = 4`, comparison case-insensitive.
`carriers_spec()` refuses a table that (a) does not declare exactly `target` carriers, (b) omits a
preregistered id, or (c) carries any id outside the four. A `v21le`/`v21be` entry therefore fails
`carriers_spec_ok` with the message that v2.1 stays unbound. The two v2.1 blobs the L1 committed
under `corpus/evidence/round-44/carriers/` are never read by the score path and are not claimed.

## 2. Functional deltas vs `git show c29360e3:tools/round-42/c1-counter.py`

Line/function census (measured): round-42 4949 lines / 78 functions → round-44 3374 lines / 87
functions; 69 function names carried, 23 bodies byte-identical, 9 dropped, 18 added. The dropped
ones are the round-42 published-carrier chain and its v3 fixtures; the added ones are the v1/v2
probe, the census/tree oracle and the dev arm.

### (1) v1/v2 superblock probe (`layout_probe`, replacing the v3 probe)

SquashFS v1/v2 share one 32-byte packed superblock, taken from unblob 26.6.4
`SquashFSv1Handler.C_DEFINITIONS` (S119) — the authority the seat assignment names:

```
magic 0:4 | inodes u32@4 | bytes_used u32@8 | uid_start u32@12 | guid_start u32@16
inode_table_start u32@20 | directory_table_start u32@24 | s_major u16@28 | s_minor u16@30
```

* endianness from the magic order (`hsqs` = le, `sqsh` = be); `zlqs`/`sqlz` (v2 nonstandard) are
  refused, so CTL-C1-4's shape reds.
* the handler family follows `s_major` (1 → `squashfs_v1`, 2 → `squashfs_v2`); v1 and v2 share the
  magic bytes, so a magic→variant table (round-42's `MAGIC_BY_VARIANT`) cannot express the
  discriminator and is gone.
* **there is no compression field in v1/v2.** The class is *observed* from the inode table's first
  metadata block: 2-byte header at `inode_table_start` (low 12 bits = stored length, `0x8000` =
  stored uncompressed), body classified (`78 xx` → `gzip`), and the frame is witnessed by
  `inode_table_start + 2 + length == directory_table_start`. The observed class is compared with the
  frozen `compression` value (normalised: `zlib(gzip)` and `gzip` name the same class; anything else,
  e.g. `uncompressed`/`zstd`, names no v1/v2 codec and is refused). `file(1)` is never consulted.
* the frozen table's `superblock_layout` block is **not used to parse**; it is cross-checked and any
  disagreement is recorded in `superblock_layout_notes` (advisory, because a wrong block cannot make
  the counter read the wrong offset). The amended block now agrees with the v1/v2 layout.
* `carve_ok` is unchanged in semantics (`chunk_end`: `bytes_used` or its 4096/1024 zero-padded
  rounding) and now reads `bytes_used` u32@8; all four carriers are exact 4096-byte carves whose
  tail is zero padding, so `chunk_end == size`.

Measured on the four real carriers (dev lane, real bytes, `receipts/dryrun-real.json`):

| id | magic | endian | major.minor | bytes_used | inode/dir table | meta hdr / len | chain | compression |
|---|---|---|---|---|---|---|---|---|
| v1le | `hsqs` | le | 1.0 | 176 | 71 / 128 | `3700` / 55 | lands | gzip |
| v1be | `sqsh` | be | 1.0 | 177 | 71 / 129 | `0038` / 56 | lands | gzip |
| v2le | `hsqs` | le | 2.0 | 196 | 88 / 136 | `2e00` / 46 | lands | gzip |
| v2be | `sqsh` | be | 2.0 | 201 | 88 / 138 | `0030` / 48 | lands | gzip |

### (2) Oracle binding — census + committed `__output__` tree, both frozen

`oracle.tsv`/`nonregular.tsv` and the v3 LZMA oracle path are gone. Per carrier the counter reads
from the frozen `carriers.json`:

```
carrier["oracle"]["members"]     [{path, sha256, size}]   # unsquashfs 4.7.5 census, rel paths
carrier["oracle"]["nonregular"]  [{path, kind[, detail]}] # empty on all four
carrier["oracle"]["output_tree"] {root, digest, digest_rule}
```

and then re-derives the second oracle from the committed S138 tree at the measured revision
(`git ls-tree -r` + `git show` per blob): every member must be a regular file, the member set must
equal the census rows exactly (path, sha256, size), and the tree digest over
`'<path>\t<sha256>\n'` sorted bytewise by path must equal the frozen digest. Neither oracle can be
edited alone (`tree_ok`). The oracle tool identity is bound by `oracle_tool_ok` (path resolves;
`sha256`/`version` checked when the table pins them).

`oracle_root` remains available for a multi-root receipt; the single-root rule is the stronger check
and none of the four carriers needs it.

### (3) Handler family binding — exact, per carrier

* `handler_ok` requires the list of squashfs-family chunk handlers to be **exactly** `[handler]`; a
  v3/v4 or `squashfs_v2_nonstandard` handler on a v1/v2 carrier fails (no prefix test, no default).
* the extract root is the `derivations[]` edge whose `handler` equals the carrier's handler
  (`squashfs_roots`/`subject_root`, segment-bounded); member edges (`handler: null`) are not
  candidates.
* `carriers_spec_ok` also refuses a handler that contradicts `s_major`.

### (4) Carrier custody — committed lane blobs

Round-42's published-carrier chain (external URL, `fetch-<id>.json`, toolchain pin,
`extract-env.json`, `--carrier-cache`) is dropped: these carriers are committed MIT unblob 26.6.4
fixtures (round-42 C2 held-out **inputs**, never a C1 carrier), so the bytes are read from
`git show REV:<path>` and the blob mode must be `100644` at the measured revision. Pins are checked
against those bytes (`carrier_pin_ok`, `carrier_size_ok`) and against the frozen prior-pins tables
(`carrier_fresh_ok`, no overlap measured: 18 prior pins, 0 hits).

### Kept verbatim (the contract's named invariants)

`under_root` / `extract_rel` / `same_rel` / `path_shape_*` / `subject_root` / `squashfs_roots` /
`strip_output` / `receipt_paths` / `diagnostic_rel` + `trusted_run_root` (segment-bounded extract
root, round-41 D5); `canonical` / `projection` / `projection_diff` / `make_real_runner` (the
counter-time REA rerun); `rea_package_problems` / `evidence_ids` (xpin evidence-id recompute);
`counter_identity` / `stamp_receipt` / `receipt_identity_ok` / `write_receipt` (`counter_sha256`
self-hash); `git` / `show` / `first_add` / `is_ancestor` / `prior_pins` / `disposition_check`.
Bodies byte-identical to round-42: `_readme`, `canonical`, `cells`, `chunk_failed`, `chunk_handlers`,
`diagnostic_typename`, `diagnostics`, `file_sha256`, `first_add`, `gaps`, `git`, `is_ancestor`,
`nonregular_published`, `path_shape_ok`, `projection_diff`, `published_rels`, `round_up`, `same_rel`,
`section`, `sha256_bytes`, `show`, `sid_tokens`, `stamp_receipt`. The rest of the same-named
functions differ only where the round constant, the table schema or the clause names required it.

### Freeze-integrity walk (claims' freeze rule, stricter than round-42's)

`frozen_drift` now walks `git log -m --diff-merges=first-parent --name-status FREEZE..REV`: M/D/R/T/U
are changes, A is a change when the path existed at FREEZE (a re-add is not a restore), rename
targets are changes, then every frozen regular-file blob that exists at both endpoints must be
byte-identical (`git rev-parse FREEZE:path` vs `REV:path`). Frozen set: the claims file, `tools/
round-44/*` and `corpus/evidence/round-44/oracle/*` (prefixes), the four carrier files, the table's
per-carrier `path` and `output_tree` roots, `tools/round-42/{fixtures,c1-counter,prior-pins,rea-pkg}`,
`tools/round-39/gen-squashfs.py`, `tools/round-27/xpin-attribute.mjs`. `carriers.json`,
`c1-run.sh`, the carrier blobs and the oracle tree all red as `frozen_path_changed` when edited after
the freeze (measured, `--selftest`).

### Deliberate scope guards

* `scratch_root()` = `--work` > `$HYAKU_SCRATCH` > `/fast/scratch/hyaku`, never `gettempdir()`;
  children get `TMPDIR` inside the private work dir (R44-SCR-TMP).
* zero-gap rule: `GAP_RULE['structural'] = {'depth-limited': 0, 'unknown-chunk-handler': 0}`. The
  wave-1 amendment freezes `gaps == []` (R44C1Controls measured zero gaps at REA's default depth 3
  on all four carriers); the draft's one-`depth-limited` allowance is therefore zero — stricter, and
  a `missing-extractor-dependency` gap (CTL-C1-3's shape) reds.
* `--no-rerun` exits 2; it is not a mode of the predicate.
* `--json-out` is stamped with `counter` + `counter_sha256`; `--verify-receipt` re-checks it. The
  committed REA receipt must not carry those keys (`evidence_envelope_ok`).

## 3. Measured receipts

`receipts.json` (same directory) carries, per invocation: seat, exact command, exit code, stdout
sha256 and bytes, wall time. Summary:

| receipt | command (abridged) | exit | wall | stdout sha256 |
|---|---|---|---|---|
| `selftest` | `c1-counter.py --selftest --work …` | **0** | 12.18 s | `6a221fd607468227…` |
| `dryrun-real-lane` | `--root <dev lane> --rev HEAD --freeze HEAD --pkg65 … --json-out receipts/dryrun-real.json` | 1 | 0.19 s | `5d431ae89142e96d…` |
| `dev-arm-positive` | `--dev-arm --run-rea --root <dev lane> --rev HEAD --pkg65 … --json-out receipts/devarm-rea.json` | **0** | 14.3 s | `ad30ecb6b10c9a29…` |
| `verify-receipt` | `--verify-receipt receipts/dryrun-real.json` | 0 | 0.09 s | `92cbb3ac798809f8…` |

### Selftest — 47 cases, 1 green, 46 red/unevaluable, 0 failures

Offline and deterministic (in-process `measure()` over a git fixture lane, simulated REA runner).
The three mandated cases plus the do-nothing lane:

* **correct map on a dev-arm-shaped receipt** → exit 0 (green).
* **v3 receipt fed to a v1 carrier** → exit 1, `v1le:handler_ok` (and `oracle_hits_ok`, `tree_ok`);
  also `squashfs_v2` on a v1 carrier → `handler_ok`.
* **fabricated oracle-only envelope** (files copied from the oracle, projection ≠ a real run) →
  exit 1, `v1be:projection_ok`; re-minted evidence id does not help.
* **do-nothing lane** (frozen table, no receipts) → exit 1, `receipt_present`.

Other red arms (all measured): `zlqs` magic, truncated superblock, `bytes_used` beyond file,
`s_major`≠handler, uncompressed metadata block, metadata length that misses the directory table,
BE magic on an LE carrier, sloppy carve, flipped census sha, extra published file, symlink row
published as a regular file, tree digest mismatch, `depth-limited` gap, `missing-extractor-
dependency` gap, `..` provenance, foreign `/kaidoku-r42/` provenance, trailing slash,
`x_extract2` prefix collision, receipt added at the freeze, score receipt relabelled as evidence,
stale evidence id, subject pin of another carrier, v2.1 id in the table, a dropped carrier, handler
vs `s_major`, all-LE coverage, five freeze-drift arms (carriers table, carrier bytes, oracle tree,
touch-then-restore), and every documentation binding (PROVINCE section/row/citation, frontier note,
entry, S138/S139 sourcing, coverage map). Probe tables (segment-bounded prefixes ×6, receipt
identity ×5) are asserted too.

### Dry run on REAL carrier bytes (no REA, no receipts)

A freeze-shaped scratch lane was built from the lane's real bytes
(`probe-real-carriers.py` → `/fast/scratch/hyaku/kaidoku-r44/probe-R44C1Counter/lane`, 23 files,
rev `8ded618c…`): the four carrier blobs, the committed S138 trees, a merged `carriers.json` for
exactly the four ids, the frozen tool pins and doc fixtures. The counter scored it at
`freeze == rev`: **all four carriers pass** `carrier_present/pin/size/fresh`, `layout_ok`,
`carve_ok`, `oracle_ok`, `tree_ok`; zero `carriers_spec_problems`, zero failing bindings, exit 1
only because no after-receipts exist (the do-nothing shape). This is the frozen-data half of the
predicate measured on the real bytes.

### Positive dev arm (R44RevKill K3)

`--dev-arm --run-rea` ran REA 6.5.0 `extract-firmware --format json --full-output` on the four real
carrier bytes into scratch (never `c1-run.sh`, never `corpus/evidence/round-44/c1`) and scored the
produced envelopes: **4/4 `dev_matched`, exit 0**, `gaps_ok` on all four with zero gaps, `oracle_hits
== oracle_files` (3/3/4/4), `tree_ok`, `evidence_id_ok` (real `ev_…` recomputed through xpin). This
is the positive control that a counter which always exits 1 cannot pass. `--arm-dir DIR` scores
already captured envelopes (`<id>/after.json`) instead of running REA.

## 4. What the frozen table must contain (state after the L1's merge)

The counter needs, per carrier, the census rows and the committed-tree binding (produced by
R44C1Oracle; merge snippet in `carriers.oracle-merge.json`, digest `4e57ca11…`):

```json
"oracle": {
  "tool": "/usr/bin/unsquashfs", "version": "4.7.5",
  "members": [{"path": "apple.txt", "sha256": "…", "size": 6}, …],
  "nonregular": [],
  "output_tree": {"root": "corpus/evidence/round-44/oracle/…_extract",
                  "digest": "…", "digest_rule": "sha256 over the concatenation of '<path>\\t<sha256>\\n' lines of `members`, sorted bytewise by path"}
}
```

Re-checked against `tools/round-44/carriers.json` after the L1's 09:06 merge (table sha256
`f29bc7b5f520065024f1f78e1da81902dea22c4470d133c84a2fe69e679c4f3d`):

* exactly **4** carriers — `v1le`, `v1be`, `v2le`, `v2be`; the v2.1 pair is gone from the table
  (recorded only as `scope.exploratory_ids`, which the counter does not read), so the earlier
  "carriers has 6 entries, want 4" blocker is **closed**;
* `carriers_spec()` → `problems []`, `notes []`; each carrier's `oracle_rows()` → 3/3/4/4 regular
  rows, 0 non-regular rows; each `output_tree_binding()` → no problems;
* the four `oracle.output_tree` blocks carry `digest` but **not** `digest_rule` (they were written
  before R44C1Oracle added the literal). The counter tolerates that: the digest is pinned
  behaviourally (the counter re-derives it from the committed blobs with its own declared rule and
  requires equality), so a table built with a different rule cannot pass. If the L1 re-runs the
  merge with the updated oracle tool the literal appears and the token check binds it textually.

The score path now needs only the L1's after-receipts; nothing in the frozen table blocks the claim.

## 5. Risks and limits

1. **`--max-depth` replay.** The rerun replays the receipt's recorded `parameters.max_depth`, so a
   receipt written at REA's default (3) is replayed at 3 and a receipt at depth 1 at 1. The dev arm
   confirms depth 3 ⇒ zero gaps on all four carriers, so the frozen zero-gap rule and the rerun
   agree as long as `c1-run.sh` does **not** pass `--max-depth 1` (R44C1Controls measured the same).
2. **Provenance segment.** `run_provenance_ok` requires `/kaidoku-r44/` in
   `parameters.output_directory`. `c1-run.sh` must extract under a scratch path carrying that
   segment (round-42 used `/kaidoku-r42/`); a receipt from another round fails.
3. **Oracle-tool dependency.** `oracle_tool_ok` resolves the frozen `oracle.tool`
   (`/usr/bin/unsquashfs`) and checks `sha256`/`version` only when the table pins them; a host
   without squashfs-tools fails that binding rather than scoring silently.
4. **Compression is observed, not read from a field.** The v1/v2 superblock has no compression id;
   the class comes from the inode-table metadata block body plus the chain witness. A metadata block
   stored uncompressed (flag `0x8000`) leaves the class undetermined and reds — none of the four
   carriers does that.
5. **Oracle independence.** The S138 `__output__` trees are unblob's own expectation (sasquatch
   lineage); the independent producer is the frozen unsquashfs census. The counter cross-checks the
   two but cannot prove the census came from unsquashfs — that is the freeze's custody claim, and
   `oracle_tool_ok` only binds the tool identity.
6. **Target spelling.** A frozen id set with different names (e.g. `V1LE`) passes (case-insensitive);
   a different *set* does not. If the L1 renames beyond case, the counter must be updated before the
   freeze.
7. **Not run:** `tools/round-44/c1-run.sh` (L1's data procedure) and any write under
   `corpus/evidence/round-44/c1/`. The claim's score is the L1's to take after the freeze.
