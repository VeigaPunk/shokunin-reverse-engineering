# R41S126Durable — round-40 closure D1: S126 pin, byte-exact copy, local-source gate

**DONE** — the S126 pin verifies (`f205807d…`, byte-identical copy prepared), and the gate that
finds this defect class is written, red at the base rev (19 rows, not 1) and green on a sandbox
clone that carries the copies plus the map. No lane file was written; nothing was extracted.

## 1. Item

Round-40 closure D1: `corpus/SOURCES.md` row S126 (at base `49096c7e6f226af0c750c4b003be58883cb6049f`)
names its source as `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv`,
a file in a *sibling project*. A fresh checkout of this lane therefore cannot resolve the row.
Work: (1) verify the digest, prepare a byte-exact copy; (2) write `local-source-gate.py`
(`--root LANE --rev REV`) that lists every SOURCES row whose URL cell is an out-of-lane local
absolute path and requires a named in-lane copy with a matching digest; show it red at the base
rev and green on a sandbox clone; selftest ≥ 6 cases.

## 2. Part A — the S126 pin and the copy

Verification (all commands run from `$S`, `TMPDIR=$S`):

```
$ sha256sum /home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/lead1-avm-image.tsv
f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0  …/lead1-avm-image.tsv
$ wc -c …/lead1-avm-image.tsv
1003 …/lead1-avm-image.tsv
```

That equals the digest pinned in the S126 URL cell **and** in the S126 anchor
(`sha256 f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0`). CONFIRMED, not
inferred: the source file on this host is the byte set the row pins.

Copy prepared (`cp --preserve=mode,timestamps`), then:

```
$ cmp <source> artifacts/R41S126Durable/s126/lead1-avm-image.tsv   -> exit 0 (no output)
$ cd s126 && sha256sum -c lead1-avm-image.tsv.sha256
lead1-avm-image.tsv: OK
```

The 1 003-byte TSV is 21 lines (`item<TAB>value`) and records `unblob_handler squashfs_v4_be`,
`unblob_command … sasquatch-v4be -no-exit-code -f -d {outdir} {inpath}`, and
`unblob_be_flag absent - the AVM branch passes no -be` — the exact claims the row is cited for.
I did **not** re-run unblob on the image (reserved-carrier bounds and not my job); the copy is a
byte copy, and I claim nothing new about its content.

The row cannot be re-read from the TSV alone: its anchor also names the 4 096-byte image
(`sha256 c7f74691…`) and `unblob.log` (`sha256 352e0d79…`), both in the same sibling directory.
I copied those two as well and checked them against the row's own pins:

```
c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32  avm-be.squashfs    (= anchor pin)
352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7  unblob.log         (= anchor pin)
$ sha256sum -c s126-anchor-bytes.sha256   -> 3× OK      $ cmp <src> <copy> ×3  -> identical
```

These are lane *own-work* bytes (a 4 096-byte image built from squashfs-tools 4.3 + Freetz
patches), not vendor firmware, so copying them into the lane does not touch the AVM licence rule.
Recommended landing `corpus/evidence/round-41/s126/` (L1 places it; I wrote only under my
artifacts dir).

## 3. Part B — `local-source-gate.py`

Stdlib-only (3.14.8 here), no network, honours `TMPDIR`, read-only git (`git -C ROOT show`).
Artifact: `local-source-gate.py` (32 444 B, sha256 `cafe232a…`).

### Convention (normative)

A sidecar map `corpus/evidence/local-sources.json` (override `--map`) binds each out-of-lane
absolute path to exactly one in-lane copy:

```json
{"version": 1,
 "sources": {"/abs/external/path": {
   "copy": "corpus/evidence/round-41/s126/lead1-avm-image.tsv",
   "sha256": "<64 hex>",
   "sha256_file": "…tsv.sha256",        // optional sha256sum-style sidecar
   "kind": "file" | "tree-archive",     // optional, descriptive
   "source_sha256": "<64 hex>",         // optional: digest of the external source at capture
   "note": "…", "rebuild": "…"}}}
```

`copy` is relative to the lane root, must stay inside it, and must name a **regular file**
(the byte-exact copy of a file, or an archive of a directory). Unknown entry keys are a hard
error, so a typo cannot silently disable a check.

### Rules, in order

1. map present → 2. entry present for the exact path → 3. `copy` inside the root (no absolute,
   no `..`) and not the external path itself → 4. copy exists and is a regular file →
5. `sha256(copy) == entry.sha256` → 6. if the **URL cell** pins a 64-hex digest, it must equal
   `entry.sha256` → 7. optional `sha256_file` sidecar must exist, parse, name the copy, and agree →
8. optional `source_sha256` must match the live source when that source is a regular file.

Step 6 is the anti-circularity rule: a digest written *in the same cell that names the path* is a
pin on those bytes, so the map cannot point at unrelated bytes. Digests elsewhere in the row
describe members or derived artefacts and are deliberately **not** consulted — S035 pins three
`.go` files, S082 pins pacman fields, S079/S090/S092 pin tarball/member digests; none of them can
bind a directory archive. Rule 6 binds exactly one row today: S126.

Path extraction: URLs are stripped first, then an absolute path token must start with `/` (not
`//`, not after `:`) and contain at least one `seg/` pair — so prose slashes such as
`` `operation`/provider.id`` in S123 are not paths. Row arity is validated (11 columns) and a
malformed table is exit 2, not a silent skip.

### Exit codes

`0` every row resolved · `1` at least one out-of-lane URL cell unresolved · `2` usage/parse error
(bad arity, unknown rev, malformed map, unknown entry key, non-directory root). Both exit-2 paths
are exercised (`evidence/gate-exit2-demo.txt`: `--rev deadbeef…` and `--root /nonexistent`).

### Advisory (never changes the exit status)

Each path record carries `source_present` (is the external path still on this host) and
`cell_url` (first public `http(s)` URL in the same cell). `cell_url` is cell-level, not a per-path
claim: row S035's cell cites the go1.25.0 tag while also naming the go-1.24.6 directory, so the
hint does not cover both.

### Scope limits (stated, not hidden)

* Only the URL cell (column 2) is gated. Four rows mention `/home/…` in other cells
  (`evidence/other-cell-paths.txt`: S038 col 6, S041 col 6, S080 col 5, S126 col 5); they are
  recorded but not gated, because the item scopes the gate to the URL cell.
* An in-lane path in the URL cell is not checked for existence — that is a different defect
  (untracked evidence), out of this item's scope.
* A directory source is carried as a deterministic tarball
  (`tar --sort=name --owner=0 --group=0 --numeric-owner --mtime=@0 … | gzip -n`), so the digest is
  of the archive, not a per-member manifest. Per-member digests would be a stronger convention;
  [INFERENCE] it is not needed for a fresh checkout to resolve the row, only for finer auditing.

## 4. Red at the base rev

```
$ python3 -I -B local-source-gate.py --root …/kaidoku-shokunin --rev 49096c7e6f226af0c750c4b003be58883cb6049f
… rows 126 total, 19 with an out-of-lane URL cell … verdict FAIL
exit=1
```

`evidence/gate-red-49096c7e.txt` (text), `…json`, `evidence/out-of-lane-summary.txt`,
`evidence/out-of-lane-rows.tsv`. Table sha256 `a61bb2486352ba452ac08c6002bae5b600ede3ae3d6afd64d38b21236ca49e5e`
(the base rev's `corpus/SOURCES.md`). The working-tree table is identical (`git diff --stat` at
base: empty), and the working-tree run agrees: `evidence/gate-red-worktree.txt`, exit 1, same 19.

**19 rows / 22 path tokens / 18 distinct paths** (Tshark cited twice, the 6.5.0 `dist/` tree four
times). Full list:

| host root | rows |
|---|---|
| `/home/vgpnk` installs | S001 S002 S003 S006 S007 S023 S035 S040 S048 S056 S066 S070 S079 S081 S083 S090 S092 S126 |
| `/var/lib` | S082 (3 paths) |
| `/home/vgpnk/Projects/shokuknow` (sibling project) | S126 |

Dispositions that matter for the fix's cost:

* **7 rows** carry a public URL in the same cell (S035, S079, S081, S082, S083, S090, S092) — the
  bytes are re-derivable from a published pin.
* **1 path token** is already gone from this host: S081's
  `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist` (`ls` → No such file or
  directory). That row's out-of-lane reference is now *dangling*, not merely out-of-lane.
* **S126 is the only row that is both out-of-lane and lane-authored** (`kind own-work`): its bytes
  exist nowhere but the sibling project. Every other row cites a host *installation* of a
  published artefact — the same npm package (pinned in S079/S080/S090/S092), the Ghidra 12.1.4
  release (S029), the Go toolchain archives (S038/S047), the Arch package (S082) — so those rows
  are un-resolvable-on-checkout but re-derivable. [INFERENCE] on the installed-REA-skill rows
  S001/S002: their text says "REA installed skill v42", which the package provides; I did not
  diff the installed skill against the npm tarball.

That is the calibration point for D1: the defect is a **class of 19**, but the *irrecoverable*
instance is exactly the one the closure names.

## 5. Green

Sandbox: `D=$(mktemp -d "$S/fx.XXXX")`, `git clone -q --shared …/kaidoku-shokunin "$D/lane"`,
`git -C "$D/lane" rev-parse --show-toplevel` verified equal to `"$D/lane"`, then
`git -C "$D/lane" checkout -q --detach 49096c7e…`. No git mutation beyond that checkout; the gate
reads the table through `--rev`.

**5.1 Full green** — `evidence/build-green-sandbox.py` consumes the gate's own red JSON and, for
each named path, copies the bytes (or the deterministic tarball) into
`$D/lane/corpus/evidence/local-sources/` and writes `corpus/evidence/local-sources.json`:

```
wrote …/corpus/evidence/local-sources.json with 18 entries       build_exit=0
$ local-source-gate.py --root "$D/lane" --rev 49096c7e…
… 19 rows … ok S126 [resolved/url-cell] <- corpus/evidence/local-sources/s126_lead1-avm-image.tsv_f90fb8c5  src[file]
verdict PASS (rows: none)                                        exit=0
```

`evidence/gate-green-sandbox.txt` / `.json`, `evidence/green-map.json` (the 18-entry map, 9 774 B),
`evidence/build-green-sandbox-manifest.tsv` (row, path, copy, digest, disposition). S081 is the
one rebuilt entry: its vanished directory is rebuilt from the published `rea-agents` 6.7.0
tarball, which S081 itself states is file-for-file identical to the installed tree.

**5.2 S126-only green** (the D1 fix as it would land this round) — second sandbox, only
`corpus/evidence/round-41/s126/{lead1-avm-image.tsv,…sha256}` plus the minimal map
`s126/local-sources.json`:

```
ok    S126 … [resolved/url-cell]  <- corpus/evidence/round-41/s126/lead1-avm-image.tsv  src[file]
verdict FAIL (rows: S001 … S092)   exit=1
```

`evidence/gate-green-s126-only.txt` / `.json`. S126 moves to resolved **through the digest the
row itself pins** (step 6), the sidecar checks, and the live-source check — and the gate still
reports the other 18, which is the honest outcome: D1's fix does not silently retire the class.

## 6. Selftest

`local-source-gate.py --selftest` → **23/23 cases, exit 0** (`evidence/selftest.txt`), fixtures in
`TMPDIR` and removed afterwards:

no-map-is-red · copy-and-map-is-green · digest-mismatch-is-red · copy-escape-is-red ·
absolute-copy-is-red · row-pin-conflict-is-red · row-pin-agrees-is-green ·
in-lane-and-url-ignored · prose-slash-ignored · half-mapped-row-is-red · sidecar-mismatch-is-red ·
sidecar-agrees-is-green · copy-must-be-a-file · malformed-map-is-exit2 · bad-arity-is-exit2 ·
cell-url-annotation · rev-fixture-green-on-disk · mutated-working-tree-is-red ·
rev-reads-committed-table · unknown-map-key-is-exit2 · source-digest-agrees-is-green ·
source-digest-mismatch-is-red · row-wide-digest-does-not-bind

The `rev-*` cases build a throwaway git fixture (`git -C <root> init/add/commit` with
`-c user.name=fx -c user.email=fx@fx`, toplevel asserted) and prove `--rev HEAD` reads the
committed table while the mutated working tree is red.

## 7. Cross-checks worth keeping

Two copies in the full-green map reproduce digests their own rows pin independently of the map:

* S003 `Base-src.zip` copy → `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804`
  = the `SHA-256` in the S003 anchor.
* S023 `go1.25.0.json` copy → `54d10162f4f55e5a94444f2602f12ef54561326370aa5868ffb325f0c3f16252`
  = the `SHA-256` in the S023 anchor.

Same for S126 (`f205807d…` = URL-cell pin). The map's digests are therefore not self-certified.

## 8. Risks / decisions for the L1

1. **What to land now.** `corpus/evidence/round-41/s126/` (TSV + sidecar + optional image/log) and
   the one-entry `corpus/evidence/local-sources.json` (`s126/local-sources.json`) are enough to
   close D1. The gate then reports S126 `resolved/url-cell` and 18 other rows red — visible, not
   hidden.
2. **Full migration is heavy.** Copies are 0.5–22 MB per path (rea-agents `dist/` 21.9 MB →
   archive, Ghidra `Base-src.zip` 7.1 MB, `go1.25.0.json` 9.6 MB, `extra.db` 8.5 MB): ~50 MB of
   in-lane evidence for rows that are re-derivable from public pins. [INFERENCE] a policy that
   accepts "public pin in the same cell" as resolution would cut the class to S126; that is a
   contract decision, and I did **not** encode it — the gate is strict by design.
3. **S081 is dangling even on this host.** Its cited npx cache directory no longer exists, so no
   copy can be verified against it; the row's claim now rests on the published 6.7.0 tarball.
   Worth a routed defect of its own next round.
4. **Optional row text.** `s126/SOURCES-row-s126-addendum.diff` adds the in-lane copy path to the
   S126 URL cell (2-line context hunk, `git apply --check` clean against the sandbox at base).
   Optional: the gate resolves the row through the map alone, so the table need not change.
5. **Map path convention** is `corpus/evidence/local-sources.json` + copies under
   `corpus/evidence/local-sources/`. If the L1 prefers a different home for the copies, only the
   map's `copy` values change.

## 9. Files, bounds, tooling

Lane files changed by me: **none** (verified: `git status --porcelain` shows only the pre-existing
untracked `.ufo/waves/round-41/`, `plans/round-41-claims.md`, `tools/round-41/`). No git/jj
mutation anywhere; read-only `git show/log/diff/status`, plus `git apply --check` and a sandbox
checkout/commit inside scratch fixtures whose toplevel I asserted. No REA, no unblob, no
extractor run at all; no reserved carrier touched; no vendor firmware bytes copied. Scratch
`/fast/scratch/hyaku/kaidoku-r41/R41S126Durable` removed after this report was written; the
sandboxes (and the ~50 MB of copies in them) lived there and are gone.

Artifacts (`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-41/w1/artifacts/R41S126Durable/`):

| bytes | sha256 | file |
|---|---|---|
| 32444 | `cafe232a196dd8446bd9b0420b32bf696cba427770eb79edda2be15a45a4ece7` | `local-source-gate.py` |
| 1264 | `f93c7ae0fb5f5b17b300c258015cb7fc29743c72b0ccd22f661d2db5b7fa6fb6` | `evidence/selftest.txt` |
| 3868 | `5c38454223890b2cadcea00620c4759fab1e64db1e97e38f0c76a8b64d32a3d0` | `evidence/gate-red-49096c7e.txt` |
| 9677 | `e822a2141a6f8f89045eb16adc43edb2461b3a61b2cc1a5c520aa9bea26716d1` | `evidence/gate-red-49096c7e.json` |
| 3875 | `1e386d883ddec647de8cb8f92a82debd48b20e3a0ed6f7fbccb081854618ff1e` | `evidence/gate-red-worktree.txt` |
| 4121 | `d5cca2f94ab25b66f8ea021465c761c4919fa5c6ef1c6d27be25d0c3f74246b5` | `evidence/gate-green-sandbox.txt` |
| 14577 | `51bf3c497617454a4cf06a4e0c8dbab614f4942518934354c5366cd9f36aad48` | `evidence/gate-green-sandbox.json` |
| 3955 | `961eb47974f50e8c6f391f491c70d7fe39821aba7f057064c55dfb02b0a31d9d` | `evidence/gate-green-s126-only.txt` |
| 9941 | `eb4f4220fd89ac73cb8399ad3c6c1caedf54debb5522886c3c01550b472c86d7` | `evidence/gate-green-s126-only.json` |
| 9774 | `27618485aea89ab16b61dd3377cd04dcfcbd65bfa444ffdc05e5446f61a9b8f5` | `evidence/green-map.json` |
| 7361 | `fffc064f7746b21535234453e4b1c05199c9b199bfdb5811aaab999c68af487a` | `evidence/build-green-sandbox.py` |
| 3779 | `4ef5bfc9602ad517b8d3e58ae394d45a39c8dffbe4061e7ba4d67c1a10f0aaf2` | `evidence/build-green-sandbox-manifest.tsv` |
| 2669 | `0a09eb34ee7bf8ab73eb0e1efa1da39631702be33df7205a3046bcdac0e9fd7b` | `evidence/out-of-lane-rows.tsv` |
| 533 | `b2651bb36e7446ce4f4887e35dd15acbf221a827a4ad62a7e9c87f85486bdca2` | `evidence/out-of-lane-summary.txt` |
| 435 | `7b00a3ae5a5eabaea0b3940f6cdce2c7a57da7e0241877c7e22d02345a32e7b9` | `evidence/other-cell-paths.txt` |
| 341 | `15326e53b562223f8cf1233fd9ae6a4060d45e9f190ac95c72449f1f69059457` | `evidence/gate-exit2-demo.txt` |
| 1003 | `f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0` | `s126/lead1-avm-image.tsv` |
| 86 | `9cd1382366c718f3c3ab9b3dfd1ac65bac4086277434984e9150b4c63947e63b` | `s126/lead1-avm-image.tsv.sha256` |
| 4096 | `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32` | `s126/avm-be.squashfs` |
| 2153 | `352e0d794143df9cc4fa6113d72ee5a620ea0aa201a930e00e91590518aed5d7` | `s126/unblob.log` |
| 245 | `8e41f8ee1437c6eb7dfc3e9aa4eb01c0343f80300e43277bff1594a35d5a3675` | `s126/s126-anchor-bytes.sha256` |
| 936 | `da01b075c0ee84f71bbec98a8191ff47fa549e900c55a2677a76cd50b7e2d172` | `s126/local-sources.json` |
| 6416 | `ff0abc3e2c9e0ab0bd5b7475069859210f3376aa08571e8a56c54df776b5c5b1` | `s126/SOURCES-row-s126-addendum.diff` |

Tooling: nothing installed or upgraded (no pacman, uv, npm or release-binary action; `python3` and
`git` were already present). No `~/.local/bin` write.
