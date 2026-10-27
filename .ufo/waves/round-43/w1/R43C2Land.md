# R43C2Land — CONFIRMED (amended pack)

**Verdict: CONFIRMED** — the R43-C2 landing pack re-validates against the live host objects today with **zero unexplained drift**: all 17 copies hash to their recorded digests, all **41** row pins still resolve, every copy re-derives byte-identically from a substrate that is still reachable, and `local-source-gate.py` on a sandbox clone with the pack in place **exits 0** (`rows_failed []`, 134 rows). The L1's in-place amendment (§1.1) — the S048 archive extended from 23 to 28 members — is **verified byte-exactly reproducible** and raises anchor-slot coverage from **29/41 to 35/41** (§5). Three host objects the round-42 pack was cut from have moved; the copies are unaffected, but the *rebuild path* changed, and one silent-failure defect in the round-42 builder was measured and repaired (F6).

Everything below is measured, not inferred, except where marked `[INFERENCE]`. Scratch (`/fast/scratch/hyaku/kaidoku-r43/w1-R43C2Land`) has been removed; every cited byte lives in this seat's artifacts dir.

> **Two L1 directions honoured.** (1) *Paths:* the copies land at the **prepared round-42 paths** `corpus/evidence/round-42/local-sources/`, **not** `round-43` (IRC, round 43 wave 1) — the pack keeps them; `plans/round-43-claims.md` is the L1's to amend. (2) *Amendment:* the L1 rebuilt S048 to 28 members and updated the map's `note`/`rebuild` for S048/S035/S081. This report reflects the amended artefact: map `c544352220532d5f91be3677ef9a43684d02e984de8c82e76f05167975c8e0b7`, S048 tar `dca1b4edb39c8768c18aa1aeb21950f4b513ef1e24e1b9460a2f6f48d15bad92`, 28 members, 2 324 480 B.

---

## 1. The landing pack

`artifacts/R43C2Land/pack/` — the exact tree the L1 commits, at the lane-relative paths it will occupy.

```
pack/corpus/evidence/local-sources.json                          the map: 18 entries (17 new + S126 carried through)
pack/corpus/evidence/round-42/local-sources/…                    17 copies, 4 570 454 B total (incl. the map)
```

### 1.1 The L1's amendment, re-verified

| item | round-42 preparation | amended (L1) | verified today |
|---|---|---|---|
| S048 archive name | `rea-agents-6.5.0-dist-cited-members.tar` | `rea-agents-6.5.0-cited-members.tar` | ✅ present, old name gone |
| S048 members | 23 (dist-relative) | **28** = 27 dist-relative + `bridge/ghidra/ReaGhidraBridge.java` (package-relative) | ✅ member list read, 28 entries |
| S048 bytes | 2 048 000 | 2 324 480 | ✅ under the 5 MiB bound |
| S048 digest | `284a07dd0d2035ca…` | **`dca1b4edb39c8768c18aa1aeb21950f4b513ef1e24e1b9460a2f6f48d15bad92`** | ✅ map entry == file bytes |
| map digest | (round-42 map) | **`c544352220532d5f91be3677ef9a43684d02e984de8c82e76f05167975c8e0b7`** | ✅ |

The five added members are exactly the anchor-pinned files that were missing: `domain/pcap/pcapAnalysis.js` (S066's 2nd pin), `pcap/PcapProvider.js` and `pcap/PcapNativeBound.js` (S070's 2nd/3rd pins), `ghidra/GhidraTargetSnapshot.js` and `bridge/ghidra/ReaGhidraBridge.java` (S083's 2nd/3rd pins). **All 28 members were checked twice** — against the row-pinned npm tarball `package/dist/…` and against the live installed pipe (`…/rea-agents/dist/…`, with `bridge/` at the package root) — **28/28 identical on both substrates**, and each carries its row's pinned digest:

```
bridge/ghidra/ReaGhidraBridge.java                db16aed4d16ab94d   (S083 pin)  tgz=True live=True
domain/pcap/pcapAnalysis.js                       7651b4c5582b6251   (S066 pin)  tgz=True live=True
ghidra/GhidraTargetSnapshot.js                    a27e410752f5474b   (S083 pin)  tgz=True live=True
pcap/PcapNativeBound.js                           24811182c301a73e   (S070 pin)  tgz=True live=True
pcap/PcapProvider.js                              16a4d813665208bd   (S070 pin)  tgz=true live=True
members 28 ok 28 bad 0 skip 0
```

The amended tar **reproduces byte-exactly** from the npm tarball with the deterministic recipe (§6): `r43-reverify.py` reports `npm tarball, 28 cited members; rebuilt dca1b4edb39c8768 vs copy dca1b4edb39c8768`, and two independent rebuilds of the whole pack into fresh directories are `diff -r`-identical to each other and to the pack.

### 1.2 Pack manifest (path, bytes, sha256)

Full receipt: `receipts/pack-manifest.tsv` (18 entries, 0 findings).

| copy (lane-relative) | bytes | sha256 | kind |
|---|---|---|---|
| `…/round-41/s126/lead1-avm-image.tsv` *(already in lane)* | 1 003 | `f205807de8016ead8732d77f14acf5e99e6527e02d6281566f6070b7c8539eb0` | file |
| `…/round-42/local-sources/S001/SKILL.md` | 23 437 | `056dee0476d1cac5bd325e30fc697b98f25ed17c60b0ec7e76b4bae536c03692` | file |
| `…/S002/native-and-artifacts.md` | 18 911 | `18b8828aec6476be03ca92bdb9506c47cc9ef8c1415c37d33e4af2f8c55cf8f9` | file |
| `…/S003/Base-src-go-rtti-members.tar` | 61 440 | `ba1f1209766abada1a4c4ae6262904f23f13efc0bfc2f99ea9f1a7eab31e6c94` | tree-archive |
| `…/S006/BSimTutorial_Intro.md` | 4 664 | `a23562a3175409a66e12e5ba47bd19e218cd7868b03bc3210c4ae7e0d296c33e` | file |
| `…/S007/ChangeHistory.md` | 491 055 | `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4` | file |
| `…/S023/go1.25.0.json.gz` | 719 095 | `ad405f00949215aa32de7314ae7fc3fc60303c599c62841afb943dc9a9cb7e05` | file (gzip) |
| `…/S035/internal-abi-go1.24.6.tar` | 81 920 | `8530a509c4d28765b68292bb5c3fda670fb53e8a8700dce90b0a567bf21a11d1` | tree-archive |
| `…/S035/internal-abi-go1.25.0.tar` | 81 920 | `069d0c887b475efa4a4d98acc7803e2f56cdfd4812244457803d2c2a00fc0df3` | tree-archive |
| `…/S040/artifactCommands.js` | 7 042 | `c4d56e038151ce3fa700692fb0701f3651c05add34e6e7cb1d2eef8b9b4f6aaa` | file |
| **`…/S048/rea-agents-6.5.0-cited-members.tar`** *(amended)* | **2 324 480** | **`dca1b4edb39c8768c18aa1aeb21950f4b513ef1e24e1b9460a2f6f48d15bad92`** | tree-archive (28) |
| `…/S056/cliCommandNames.js` | 10 543 | `41963156f6330ecf7b8d8b62e00da6a563ad5312fca82afac38f51c996255dd3` | file |
| `…/S066/TsharkCaptureProvider.js` | 21 208 | `fdc1fc13d2468fa0bcaf1e1bf585c80dc9840f059f78a623d7be420f76d30549` | file |
| `…/S081/rea-agents-6.7.0-dist-cited-members.tar` | 51 200 | `11c07d925277ee136d430fe1e329151d39b63192ee866c2e54e64430dc89f42d` | tree-archive |
| `…/S082/desc` | 402 | `a2d70e537e159315625038c38cc2d54830617431db384b2b5caf0d9da8cd5456` | file |
| `…/S082/extra-db-tinyxxd-1.3.17-1-desc.tar` | 10 240 | `4c1d650f1528d17c0c9fd3000f5df257923e799e24dddd38c75edbe22e68bb31` | tree-archive |
| `…/S082/mtree` | 529 | `a5e4c9e67d9c608f0b7c8603cd68ebab5d9d97f4cddfbf85c2b4ced0365fea58` | file (gzip) |
| `…/S083/binary-BVOr2mgE.js` | 649 535 | `64c07dae6fe8b79a2015550cd8de208bc41f7b325dddd7262031ef76820c00df` | file |

**Firmware scan.** `pack-manifest.py` inspects the outer magic of every copy and the first bytes of every archive member against a squashfs/cramfs/jffs2/ubifs/ubi/dtb/gzip/bzip2/xz/lz4/zstd/7z/png/jpeg/zip/tar list. **No third-party firmware image is among the copies**; the only recognised magics are the two intended gzip encodings (S023's payload and S082's `mtree`, which the row itself calls "gzip"). No copy exceeds the 5 MiB bound (largest: the amended S048 at 2 324 480 B).

**Map.** 18 entries: 17 new plus the round-41 S126 entry carried through untouched (`sha256_file` sidecar and `source_sha256` unchanged). `corpus/SOURCES.md` needs **no** edit — the rows keep their host paths; the map carries the resolution.

---

## 2. Re-verification against the live host objects (the plan's re-verification clause)

`build/r43-reverify.py` — **133 checks, 0 failures** (`receipts/reverify.tsv`).

### 2.1 Pass A — pack self-consistency

For each of the 17 copies: present, sha256 equal to the map entry, size within the 5 MiB bound. 17/17 OK — including the amended S048 (`map dca1b4edb39c8768 == actual dca1b4edb39c8768`).

### 2.2 Pass B — re-derivation from a *reachable* substrate

The plan asks that each source file's digest be recomputed on the host. Three host objects are gone (§3), so for those the re-derivation runs against the substrate **the row itself pins**. Every re-derived artefact was compared **byte-for-byte** with the copy:

| copy | substrate used today | re-derived == copy |
|---|---|---|
| S001, S002 | live host file (REA skill install) | ✅ |
| S003 | live host zip (`Base-src.zip`), 2 cited members | ✅ `ba1f1209…` |
| S006, S007 | live host file (Ghidra docs) | ✅ |
| S023 | live host file, re-encoded `gzip -9 -n` | ✅ `ad405f00…` |
| S035 (1.25.0) | **Go 1.25.0 source tarball**, `internal/abi` tree | ✅ `069d0c88…` |
| S035 (1.24.6) | **Go 1.24.6 source tarball**, `internal/abi` tree | ✅ `8530a509…` |
| S040 | **npm tarball** member `package/dist/cli/artifactCommands.js` | ✅ `c4d56e03…` |
| **S048 (amended)** | **npm tarball**, the 28 cited members (27 under `package/dist/`, 1 under `package/`) | ✅ **`dca1b4ed…`** |
| S056 | **npm tarball** member `package/dist/cliCommandNames.js` | ✅ `41963156…` |
| S066 | **npm tarball** member `package/dist/captures/TsharkCaptureProvider.js` | ✅ `fdc1fc13…` |
| S081 | **npm tarball** `rea-agents-6.7.0.tgz`, the 3 cited members | ✅ `11c07d92…` |
| S082 `desc`, `mtree` | live host file (pacman local db) | ✅ |
| S082 extra.db tar | live pacman db member `tinyxxd-1.3.17-1/desc` | ✅ `4c1d650f…` |
| S083 | **npm tarball** member `package/dist/cli-runtime/binary-BVOr2mgE.js` | ✅ `64c07dae…` |

**17/17 re-derive byte-identically.** Tarball digests were verified before use:

```
rea-agents-6.5.0.tgz  531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699  (S090/S092 pin)
rea-agents-6.7.0.tgz  20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90  (S081 pin)
go1.25.0.src.tar.gz   4bd01e91297207bfa450ea40d4d5a93b1b531a5e438473b2a06e18e077227225  (go.dev ?mode=json&include=all)
go1.24.6.src.tar.gz   e1cb5582aab588668bc04c07de18688070f6b8c9b2aaf361f821e19bd47cfdbd  (go.dev ?mode=json&include=all)
```

**The shared-dist-dir cross-check (S048/S070/S079/S090/S092 and, after the amendment, S066/S083).** The REA 6.5.0 npx pipe was absent when this seat started and was re-installed during the round. All 28 amended members are byte-identical to the tarball's, 28/28, so the archive holds the same bytes whether one reads the pipe or the tarball. Every row sharing that host path now has its cited member inside the one archive — the F5 defect from round 42 is closed.

### 2.3 Pass C — the row pins (41 digests, zero drift)

The round-42 audit claimed **41** pinned digests over the 18 rows and zero drift. Re-run: **41 distinct (row, digest) pins, all 41 audited, all 41 MATCH**. Each was resolved against the live object or the row-pinned upstream substrate — never against a transcribed constant:

| row | pins | result |
|---|---|---|
| S003 | 1 (container `f00d29c2…`) | MATCH (`src[file]` at the gate) |
| S023 | 1 (`54d10162…`, decoded gzip) | MATCH |
| S035 | 3 (`map_swiss.go` `0e2fedbe…`, `map_noswiss.go` `03db5a82…`, `map_select_swiss.go` `c16b55b8…`) | MATCH in **both** 1.25.0 and 1.24.6 — the "byte-identical" claim holds |
| S056 | 1 (`41963156…`) | MATCH |
| S066 | 2 (`fdc1fc13…`, `pcapAnalysis.js` `7651b4c5…`) | MATCH |
| S070 | 3 (`fdc1fc13…`, `PcapProvider.js` `16a4d813…`, `PcapNativeBound.js` `24811182…`) | MATCH |
| S079 | 6 | MATCH |
| S081 | 4 (`20958a66…` tarball + 3 members) | MATCH |
| S082 | 2 (`/usr/bin/tinyxxd` `7b1e5d0c…` from the mtree; `%SHA256SUM%` `3f84d7de…` from the db member) | MATCH |
| S083 | 3 (`64c07dae…`, `GhidraTargetSnapshot.js` `a27e4107…`, `ReaGhidraBridge.java` `db16aed4…`) | MATCH |
| S090 | 5 (`531717a0…` tarball + 4 members) | MATCH |
| S092 | 10 (same tarball pin + 9 sqlite/artifact readers) | MATCH |
| S001 S002 S006 S007 S040 S048 | 0 | rows pin no digest |

The S035 pins were checked against both toolchain versions (6 checks for 3 row pins); that is what makes the row's cross-version byte-identity assertion a measurement rather than a claim.

---

## 3. Drift since round 42

Receipt: `receipts/drift.tsv`. **Zero unexplained drift**; one deliberate supersession; three host objects moved.

### 3.1 Pack bytes

Every copy except the amended S048 is byte-identical to its round-42 recorded digest. S048 was **superseded on purpose** by the L1 (23 → 28 members, `284a07dd…` → `dca1b4ed…`) and the drift audit reports it as `SUPERSEDED`, not as drift:

```
COPY  …/S048/rea-agents-6.5.0-dist-cited-members.tar  present  SUPERSEDED by …/rea-agents-6.5.0-cited-members.tar  SUPERSEDED
MAP   …/S048/rea-agents-6.5.0-cited-members.tar       284a07dd0d2035ca  dca1b4edb39c8768  DRIFT  SUPERSEDED
drift findings: 0
```

### 3.2 Host objects that moved (the copies are unaffected; the *rebuild path* changed)

| host path | round 42 | today | consequence |
|---|---|---|---|
| `/home/vgpnk/.local/opt/go-1.25.0/src/internal/abi` | present | **ABSENT** | S035's 1.25.0 copy can no longer be re-cut from the host dir; it re-derives from the official go1.25.0 source tarball (identical bytes). The host now carries only `go1.27.3`, which has no `src/internal/abi`. |
| `/home/vgpnk/.local/opt/go-1.24.6/src/internal/abi` | present | **ABSENT** | as above, from go1.24.6. |
| `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist` | absent (already at round 42) | still **ABSENT** | unchanged: S081 resolves from the 6.7.0 tarball. The amended map's S081 `rebuild` now says so explicitly. |
| `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist` | present | **re-installed during the round** (content byte-identical, 28/28 members match the tarball) | none — but its presence is **not stable**, so the tarball is the durable substrate. |

Nothing else moved: the Ghidra install, the REA skill install, the pacman local records and `extra.db`, and the S126 shokuknow file all hash exactly as at round 42 — including the three `source_sha256`-pinned containers (`f00d29c2…`, `54d10162…`, `0b07b403…`).

### 3.3 Rebuild pointers

The amended map now carries substrate-specific rebuild text for S035 (upstream Go tags, with a fetch manifest at `R43RevLocalsrc/receipts/go-upstream-sha256.tsv`) and S081 (curl + pinned digest), which is correct. Nine entries still say `python3 build-copies.py --out <lane> --tarball-dir <dir>`; that script reads the **host paths**, three of which no longer exist, and it silently writes empty archives when a host directory is absent (F6). `build/build-copies-r43.py` in this seat's artifacts is the re-grounded replacement: it rebuilds **all 17** copies from the row-pinned substrates, refuses a missing tarball (exit 1), refuses an empty archive, and reproduces all 17 recorded digests **exactly**, including the amended `dca1b4ed…` (§6). **Recommendation:** point those nine `rebuild` fields at it.

---

## 4. Sandbox gate receipt

`build/sandbox-gate.sh` — two `git clone --shared` clones in scratch, each `git -C … rev-parse --show-toplevel` asserted equal to the clone dir before anything touches it, copies laid down with `cp -a`, **no commit, no checkout, no stash**. Gate = the lane's own `tools/round-41/local-source-gate.py`.

| step | what | exit | receipt |
|---|---|---|---|
| A | gate, **pristine** clone, `--rev 6b9e64fe…` (do-nothing control) | **1** | `gate-pristine.json` — `rows_failed` = the 18 rows |
| B | gate, clone **+ pack**, `--rev 6b9e64fe…` | **0** | `gate-with-copies.json` — `rows_failed []`, `rows_total` 134, `rows_checked` 19 |
| C | gate, clone **+ pack**, working tree | **0** | `gate-with-copies.txt` — `verdict PASS (rows: none)` |
| D | gate `--selftest` | **0** | `gate-selftest.txt` — 23/23 cases |
| E | control: one byte appended to S056's copy | **1** | `gate-corrupt.json` — `S056 copy-digest-mismatch` |
| F | control: S007's map entry dropped | **1** | `gate-dropped-entry.json` — `S007 no-copy-named` |
| G | control: S056's map digest zeroed | **1** | `gate-bad-digest.json` — `S056 copy-digest-mismatch` |
| H | restored clone | **0** | `gate-restored.json` — `rows_failed []` |

Per-row verdicts at step B: every one of S001 S002 S003 S006 S007 S023 S035(×2) S040 S048 S056 S066 S070 S079 S081 S082(×3) S083 S090 S092 reads `[resolved/none]`; S126 reads `[resolved/url-cell] src[file]`. The three `source_sha256` hosts (S003, S023, S082/extra.db) read `src[file]` — the gate re-verified the live container on that run. `table_sha256` = `8c6c53143741b03a4261049b50844d2179be3b139f0f2769c7e2acc147bf2ed5` (= the base `corpus/SOURCES.md`): the registry table is untouched.

**The exact landing recipe, run end-to-end in a fresh sandbox clone:**

```
cp -a artifacts/R43C2Land/pack/corpus/evidence/round-42           corpus/evidence/
cp -a artifacts/R43C2Land/pack/corpus/evidence/local-sources.json corpus/evidence/local-sources.json
python3 -I -B tools/round-41/local-source-gate.py --root . --rev 6b9e64fe7e0de202d9383baad5792fbfe039a743
# -> rows 134 total, 19 with an out-of-lane URL cell, verdict PASS (rows: none), exit 0
```

**Gate tool identity.** Byte-identical to the base commit's copy: sha256 `cafe232a196dd8446bd9b0420b32bf696cba427770eb79edda2be15a45a4ece7`, `cmp` exit 0; last touched by `d764389e` (round-41 freeze). P43-C2's "gate tool byte-identical to the round-41 committed bytes" holds.

---

## 5. Coverage: which anchor-cell digests the pack actually carries

The gate reads only the URL cell, and **none of the 18 rows pins a digest there** — so a green gate does not by itself show that the landing carries the bytes the rows pin (the sibling seat's blocker B1). `build/anchor-coverage.py` measures the useful question mechanically: it hashes every byte copy, every archive member and every gzip payload in the pack, then checks all **41** anchor-cell digest slots against that set. Receipt: `receipts/anchor-coverage.tsv`.

| | round-42 pack | **amended pack** |
|---|---|---|
| anchor slots carried as bytes | 29 of 41 | **35 of 41** |

Per row: S023 1/1 · S035 3/3 · S056 1/1 · S066 2/2 · S070 3/3 · S079 6/6 · S081 3/4 · S082 0/2 · S083 3/3 · S090 4/5 · S092 9/10 · S003 0/1.

**The 6 remaining slots are structurally out of reach, not defects:**

| slot | why it cannot be an in-lane copy |
|---|---|
| S003 `f00d29c2…` | digest of the **container** `Base-src.zip` (7 481 132 B) — over the 5 MiB copy bound; pinned via `source_sha256`, which the gate re-verifies live on every run |
| S081 `20958a66…` | digest of `rea-agents-6.7.0.tgz` itself (6 276 963 B) — over the bound; it is the rebuild substrate |
| S090, S092 `531717a0…` | digest of `rea-agents-6.5.0.tgz` itself (5 634 033 B) — over the bound; the rebuild substrate |
| S082 `7b1e5d0c…` | the `sha256digest` of `/usr/bin/tinyxxd` recorded in the mtree — the **binary** is not one of the row's URL-cell host paths, so no copy names it |
| S082 `3f84d7de…` | the `%SHA256SUM%` **package field** of `tinyxxd-1.3.17-1-x86_64.pkg.tar.zst` — a string inside a pacman record, not file bytes anywhere in the pack |

One is cheaply closable if the L1 wants 36/41: copy `/usr/bin/tinyxxd` (38 928 B, sha256 `7b1e5d0c970afe68…`, well under the bound) into `…/S082/tinyxxd` and add its map entry. I did **not** do this — the L1 owns the pack's shape after the amendment, and the amendment is verified as delivered.

---

## 5b. Tool provenance, and the `rebuild`-path variant map

**Provenance receipt: `receipts/tools-provenance.tsv`** — sha256 + bytes for every artefact this seat authored, plus the 17 copies. The L1 can cite artifact path + hash directly:

| artefact | bytes | sha256 |
|---|---|---|
| `build/build-copies-r43.py` | 20 291 | `4314309508511fc45abb0022459d0ea143c510ae6cadd04a47a4b7809898a9c0` |
| `build/r43-reverify.py` | 26 025 | `b1a0c3f43760701d46c6b48430e90cc877fe3e25a08d596ac88bff57abe4b70c` |
| `build/anchor-coverage.py` | 4 305 | `c5403043ff3543ff01390e122df8bbe7e5d6834e9fa745ab8cbf3a6c43e997f5` |
| `build/drift-audit.py` | 7 784 | `8ccbce8a828b73790b0d21be5fcc1fd9bc0d7c1af2a98343b3ba3e86877c8d66` |
| `build/pack-manifest.py` | 4 583 | `8abdadb586f67ca60fe2f311d80674c7178710952b9c5d8a48d86155222e377a` |
| `build/sandbox-gate.sh` | 3 915 | `c62252a151189fe793197f727ed4bb4c730282ae675e1a166be5d49dbf595d7d` |
| `build/calibration-probes.sh` | 4 847 | `e8c9280f16e30a7d021293e31cc47e0c4f36015e89de74ed687676bd68e1cfc9` |
| `build/validate-proposal.sh` | 7 472 | `5033c1affcacb05f4c36c4554c72c154b3d89c730b4c7d39c7f384bf61d4a7b4` |
| `proposal/gate-extension-F4.patch` | 5 091 | `7edbd33af285e9136470161c051068f866e089b19d97f8a46693d38a9a7cbfbf` |
| `pack/corpus/evidence/local-sources.json` | 12 833 | `c544352220532d5f91be3677ef9a43684d02e984de8c82e76f05167975c8e0b7` |
| `pack-rebuild-path/corpus/evidence/local-sources.json` | 12 533 | `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e` |

**Two fixes made for the L1's `tools/round-43/` plan.**

1. **The builder now emits the installed path.** `build-copies-r43.py` writes its own `rebuild` field as `python3 tools/round-43/build-copies-r43.py --out <lane> --tarball-dir <dir>`, so a regenerated map is correct by construction and the 17 fields need no hand edit. (Earlier it wrote the bare `build-copies-r43.py`; that is changed.)
2. **The builder no longer clobbers hand-edited notes.** It preserves an existing entry's `note` and only fills one in when absent — so rebuilding on top of the L1's amended map keeps the S035/S048/S081 note rewording instead of reverting it. Verified: rebuilding from the amended map changes **only** the `rebuild` field (17 entries) and nothing else — `copy`, `kind`, `sha256`, `sha256_file`, `source_sha256`, `note` all differ in **0** entries.

3. **The builder now refuses to write a partial map.** A run into a directory with no map used to write a 17-entry map and silently **drop the S126 entry**, which the base commit's map carries (the sibling seat measured the same hazard at its B4 against the round-42 script). It now requires either an existing map or `--base-map <lane>/corpus/evidence/local-sources.json`, and re-checks after merging that no base entry vanished:

```
$ build-copies-r43.py --out <empty dir> --tarball-dir <scratch>
refusing to write a partial map: …/local-sources.json does not exist and no --base-map was
given, so entries this script does not build (row S126) would be dropped.
Pass --base-map <lane>/corpus/evidence/local-sources.json.        [exit 1]
$ build-copies-r43.py --out <dir with the amended map>            [exit 0, 18 entries]
$ build-copies-r43.py --out <dir> --base-map <amended map>        [exit 0, 18 entries]
```

Both seeding routes produce the **same bytes** as `pack-rebuild-path/corpus/evidence/local-sources.json` (`diff` clean), with the 17 copies identical to the pack.

**Variant map (optional, ready to take):** `pack-rebuild-path/corpus/evidence/local-sources.json`, sha256 `3158cdc982fc07d263198ab0eaeee2adb9ca9d8cf4ebb662ea640c1c0491148e`, 18 entries. It is the amended map with **only** the `rebuild` fields rewritten to the `tools/round-43/` path; every digest and note is the L1's. Gate-checked in a sandbox clone with the pack's copies: **exit 0, `rows_failed []`, `rows_total` 134** (`receipts/variant-gate.json`). Taking that file, or regenerating it after installing the script, gives identical bytes (verified both ways).

## 6. Determinism of the rebuild

```
build-copies-r43.py --out <fresh dir 1> --tarball-dir <scratch>
build-copies-r43.py --out <fresh dir 2> --tarball-dir <scratch>
diff -r run1/corpus run2/corpus                                  -> RUNS-IDENTICAL
diff -r run1/corpus/evidence/round-42 pack/corpus/evidence/round-42 -> PACK-IDENTICAL
```

All 17 copy digests are reproduced exactly, including the amended S048 (`dca1b4ed…`, 28 members). The rebuild refuses a missing tarball (`missing …/go1.25.0.src.tar.gz`, exit 1) and refuses an empty archive (`refusing to build an empty archive: no members`).

---

## 7. Findings routed forward

**F6 (new, correctness) — the round-42 builder silently writes an EMPTY archive and exits 0.** Measured: with the Go toolchains gone, `R42LocalSrc/build/build-copies.py` ran to **exit 0** and produced two 10 240-byte tars with **zero members**, digest `84ff9269…` instead of `069d0c88…`/`8530a509…`. Its `tar_dir()` walks a missing directory, gets an empty file list, and emits a valid-looking empty tar; nothing checks the member count. A rebuild on today's host would have silently replaced S035's copies with empty archives. `build-copies-r43.py` refuses both cases. **Recommendation:** point the remaining `build-copies.py` rebuild fields at it (the sibling seat independently reached the same conclusion at its B4).

**F4 (round-42 finding, CONFIRMED as a hard blocker) — the gate's map vocabulary cannot express what the copies are.** Measured on this pack: an entry with `"encoding": "gzip"` → exit **2** (`map …: entry for '…/go1.25.0.json' has unknown key(s) encoding (allowed: copy, kind, note, rebuild, sha256, sha256_file, source_sha256)`); `"kind": "compressed"` → exit **1** (`S023 map-kind-invalid compressed`). A green row tells a machine reviewer nothing about whether the copy is source bytes, a reversible encoding, or a member excerpt — and 3 of the 17 copies are of the latter two kinds. **A tested patch is delivered** in `proposal/gate-extension-F4.patch`; `build/validate-proposal.sh` applies it **inside a sandbox clone only** (the lane's gate is sha256-verified unchanged before and after). Acceptance, all measured on the amended pack:

```
selftest 23/23 (exit 0);  pack still green (exit 0, rows_failed [])
kind=compressed without encoding   -> exit 1  (map-kind-encoding-mismatch)
kind=compressed with encoding=gzip -> exit 0
encoding=brotli                    -> exit 1  (map-encoding-invalid)
members=[…DoesNotExist.java]       -> exit 1  (map-member-absent)
lane gate sha256 before == after   -> UNCHANGED (cafe232a…)
```

**It must NOT be applied this round:** P43-C2 freezes the gate tool to its round-41 bytes, and this seat did not touch it.

**F7 (round-42 §7 risk, CONFIRMED) — `source_sha256` turns a host drift into a hard gate red.** Perturbing `extra.db`'s recorded `source_sha256` → exit **1** (`S082 source-digest-mismatch expected 1111111111 actual 0b07b4031088`); dropping the field entirely → **exit 0**, `rows_failed []`. The field is doing real work (it is how the gate proves the copy still corresponds to the live container) but it is a host-coupled trip-wire: `extra.db` changes on the next `pacman -Sy`, and two Ghidra paths move on the next Ghidra upgrade. **L1 decision:** keep it and record the trip-wire in the freeze note, or drop it and accept a weaker binding. The landing is unaffected either way.

**F5 (round-42 finding) — CLOSED by the L1's amendment.** The shared-dist archive now holds 28 members covering every anchor-pinned member of the seven rows that share that host path; the 5 previously-orphaned pins (`pcapAnalysis.js`, `PcapProvider.js`, `PcapNativeBound.js`, `GhidraTargetSnapshot.js`, `ReaGhidraBridge.java`) are present and carry their row digests.

**F8 (observation) — the REA 6.5.0 npx pipe is not a stable substrate.** Absent at round start, re-installed mid-round; content byte-identical either way. The tarball is the durable substrate and the amended S048 note should keep saying so.

**F1/F2/F3 (round-42 row-quality items, unchanged).** S081 is pipe-absent; S082 names two different `desc` records (installed 402 B vs repo member 1 246 B); S083's `bridge/ghidra/ReaGhidraBridge.java` is package-relative, not `dist/`-relative. All re-verified today. The amendment's S048 note now states the `bridge/` exception explicitly, which resolves the practical half of F3. These remain `corpus/SOURCES.md` row-quality items, not gate blockers.

---

## 8. Limits and disclosed risks

* Three host objects moved, so for those the copies' **provenance today** is the row-pinned upstream tarball rather than the host install the URL cell names. The bytes are identical and the rows pin those tarballs themselves, so the claim is not weakened — but S035 is now a *fourth* row whose URL cell names an absent host path (after S081). A row-quality pass may want it noted; it does not affect the gate.
* The Go tree re-derivation uses the **official Go source tarballs**, whose digests were confirmed against `https://go.dev/dl/?mode=json&include=all` and whose `internal/abi` member lists equal the archived lists (28 = 28 for both versions, `diff` empty). The three pinned files were additionally fetched from the row's own upstream pointer (`raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/`) and matched.
* The npm tarballs were downloaded this round; digests were checked against the row pins **before** use, and every re-derived member was compared against the live pipe where the pipe exists (28/28).
* The amended S048's 27 dist-relative members and 1 package-relative `bridge/` member use different tarball prefixes; both the verifier and the builder handle the split explicitly, so a future member added under `bridge/` cannot silently resolve against the wrong prefix.
* This seat ran **no** REA, unblob, sasquatch or extractor, and touched no firmware image.
* `[INFERENCE]` The claim's predicate names the copies under `corpus/evidence/round-43/local-sources/`; both L1 directions (IRC correction, then the amendment notification) keep them at the prepared round-42 paths, and this pack follows them. If the plan is amended the other way, the map's 17 `copy` fields must be rewritten in step — a mechanical edit; digests are unaffected.

## 9. Tools used (nothing installed, upgraded or moved)

`python3` 3.14.8 · `git` 2.56.0 · GNU `tar` 1.35 · `gzip` 1.15 · `curl` 8.23.0 · `sha256sum` (coreutils). No pacman transaction, nothing written into any PATH directory, `~/.local/bin` untouched, no git mutation in the lane (clones only, `rev-parse --show-toplevel` asserted before every use).

## 10. Artifacts

```
build/r43-reverify.py       pack self-consistency + substrate re-derivation + the 41-pin audit (133 checks, 0 failures)
build/build-copies-r43.py   re-grounded builder: rebuilds all 17 copies (incl. the amended 28-member S048) from the row-pinned substrates; refuses a missing tarball and an empty archive
build/anchor-coverage.py    which of the 41 anchor-cell digests the pack actually carries (35/41)
build/drift-audit.py        copy / host / map drift classes vs the round-42 recorded digests (supersession aware)
build/pack-manifest.py      landing manifest + firmware-magic scan
build/sandbox-gate.sh       the gate receipt (A…H): do-nothing control + three red controls
build/calibration-probes.sh P1/P1b (F4), P2/P2b (source_sha256 trip-wire), P3 (gate byte identity), P4 (map entries)
build/validate-proposal.sh  applies the F4 patch in a sandbox clone and checks its acceptance criteria
pack/corpus/evidence/local-sources.json                    the map to land (18 entries, sha256 c5443522…)
pack/corpus/evidence/round-42/local-sources/…              the 17 copies to land (S048 = rea-agents-6.5.0-cited-members.tar, dca1b4ed…, 28 members)
pack-rebuild-path/corpus/evidence/local-sources.json       the optional variant map: amended map + `rebuild` fields pointing at tools/round-43/ (sha256 3158cdc9…), gate-green
proposal/gate-extension-F4.patch                           the tested F4 extension (NOT to be applied to the frozen gate this round)
receipts/tools-provenance.tsv  sha256 + bytes for every artefact this seat authored, and the 17 copies (regenerated after the final edits — cite this file, not an earlier hash)
receipts/variant-map-sha256.txt / variant-gate.json        the variant map's digest and its green sandbox gate run
receipts/reverify.tsv          133 checks, 0 failures
receipts/anchor-coverage.tsv   35 of 41 anchor slots carried; the 6 uncovered named with reasons
receipts/pack-manifest.tsv     18 entries, 0 findings
receipts/drift.tsv             0 unexplained; 1 SUPERSEDED (S048); 3 host objects MOVED
receipts/gate-with-copies.json exit 0, rows_failed []
receipts/gate-pristine.json    do-nothing control: exit 1, 18 rows failed
receipts/gate-corrupt.json / gate-dropped-entry.json / gate-bad-digest.json   three red controls
receipts/gate-restored.json    exit 0 again
receipts/gate-selftest.txt     23/23
receipts/gate-tool-sha256.txt  gate byte identity at the base commit
receipts/p1-encoding-keys.err / p1b-new-kind.json / p2-source-drift.json / p2b-no-source.json   F4 + F7 probes
receipts/proposal-*.json / proposal-selftest.txt   the F4 extension's acceptance run
receipts/sandbox-gate.log / calibration-probes.log / validate-proposal.log   raw run logs
```

### Recommended next steps for the L1

1. **Land the amended pack as-is.** It is green, its 28-member S048 is byte-exactly reproducible, and it carries 35 of 41 anchor slots.
2. **Install `build/build-copies-r43.py` at `tools/round-43/` and point the nine remaining `build-copies.py` rebuild fields at it** — the round-42 builder now writes empty S035 archives and exits 0 (F6). The script already emits that path in its own `rebuild` field and preserves the amended notes, so either take `pack-rebuild-path/corpus/evidence/local-sources.json` (sha256 `3158cdc9…`, gate-green) or regenerate it after the install — both give the same bytes.
3. *Optional, if 36/41 is wanted:* copy `/usr/bin/tinyxxd` (38 928 B, `7b1e5d0c…`) into `…/S082/tinyxxd` and add its map entry (§5). Not done here — the pack's shape is the L1's after the amendment.
4. The F4 gate extension is ready but must wait for a round in which the gate tool is not frozen.
