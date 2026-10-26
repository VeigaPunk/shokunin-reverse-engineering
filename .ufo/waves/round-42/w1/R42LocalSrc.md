# R42LocalSrc — routed defect R41-CL3 (out-of-lane SOURCES rows)

**Verdict: DONE** — the 18 rows the round-41 `local-source-gate.py` reds at rev `c4a38ea` are resolvable from this lane: 17 in-lane copies (byte copies, one lossless `gzip -9 -n` copy, four deterministic member/`tree-archive` tars) plus the preserved S126 entry take the gate from **exit 1 (18 rows failed)** to **exit 0 (PASS)** inside a throwaway clone, on both the pinned rev and the current working tree. No host file drifted; all 41 digests the rows themselves pin still verify. Four findings routed forward (F1–F4), one of them against the gate's own vocabulary.

Everything below is measured, not inferred, except where marked `[INFERENCE]`. Scratch (`/fast/scratch/hyaku/kaidoku-r42/R42LocalSrc`) has been removed; every cited byte lives in this artifacts dir.

## 1. Baseline (the defect as it stands)

```
python3 -I -B tools/round-41/local-source-gate.py --root <lane> \
  --rev c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c
# exit 1
# rows 129 total, 19 with an out-of-lane URL cell
# verdict FAIL (rows: S001 S002 S003 S006 S007 S023 S035 S040 S048 S056 S066
#                    S070 S079 S081 S082 S083 S090 S092)
```

`--selftest`: **23/23 PASS** (exit 0), so the gate itself is healthy; 20 of the 21 out-of-lane path records were `no-copy-named`, S081's record also had `source_present=false`. S126 was already green (`[resolved/url-cell] src[file]`).

Receipt: `build/receipts/gate-baseline-host.json` (JSON, `exit: 1`, `rows_failed` length 18).

`corpus/SOURCES.md` is identical at rev `c4a38ea` and at lane HEAD `fdabdfa4` (both sha256 `3cf6cf99de275e68dcd06d5c297c5f22e36749657f1a8d8128df2755ead18727`, = the gate's `table_sha256`), so the fix is not revision-dependent.

## 2. What each row gets

Copies are staged in this artifacts dir under the exact lane paths they would take; `<A>` = `.ufo/waves/round-42/w1/artifacts/R42LocalSrc`, `<L>` = the lane root. "copy sha256" is the digest that goes into the map (16 hex shown; full values in §4 and `build/copies.tsv`).

| row | host path named by the URL cell | host bytes | host sha256 | disposition | copy under `corpus/evidence/round-42/local-sources/` | copy bytes | copy sha256 |
|---|---|---|---|---|---|---|---|
| S001 | `~/.agents/skills/reverse-engineer-anything/SKILL.md` | 23 437 | `056dee0476d1cac5…` | byte copy | `S001/SKILL.md` | 23 437 | `056dee0476d1cac5…` |
| S002 | `…/references/native-and-artifacts.md` | 18 911 | `18b8828aec6476be…` | byte copy | `S002/native-and-artifacts.md` | 18 911 | `18b8828aec6476be…` |
| S003 | `ghidra_12.1.4_PUBLIC/…/Base-src.zip` | 7 481 132 | `f00d29c20119562e…` | **member extract** tar (2 cited `.java`) | `S003/Base-src-go-rtti-members.tar` | 61 440 | `ba1f1209766abada…` |
| S006 | `…/docs/GhidraClass/BSim/BSimTutorial_Intro.md` | 4 664 | `a23562a3175409a6…` | byte copy | `S006/BSimTutorial_Intro.md` | 4 664 | `a23562a3175409a6…` |
| S007 | `…/docs/ChangeHistory.md` | 491 055 | `c6b25301cda77dca…` | byte copy | `S007/ChangeHistory.md` | 491 055 | `c6b25301cda77dca…` |
| S023 | `…/typeinfo/golang/go1.25.0.json` | 10 081 618 | `54d10162f4f55e5a…` | **`gzip -9 -n`** (lossless) | `S023/go1.25.0.json.gz` | 719 095 | `ad405f00949215aa…` |
| S035 | `go-1.25.0/src/internal/abi/` | 51 856 / 28 files | — | directory tar | `S035/internal-abi-go1.25.0.tar` | 81 920 | `069d0c887b475efa…` |
| S035 | `go-1.24.6/src/internal/abi/` | 50 614 / 28 files | — | directory tar | `S035/internal-abi-go1.24.6.tar` | 81 920 | `8530a509c4d28765…` |
| S040 | `…/dist/cli/artifactCommands.js` | 7 042 | `c4d56e038151ce3f…` | byte copy | `S040/artifactCommands.js` | 7 042 | `c4d56e038151ce3f…` |
| S048 | `…/rea-agents/dist/` (6.5.0) | 22 972 248 / 1 574 files | — | **cited-member** tar (23) | `S048/rea-agents-6.5.0-dist-cited-members.tar` | 2 048 000 | `284a07dd0d2035ca…` |
| S056 | `…/dist/cliCommandNames.js` | 10 543 | `41963156f6330ecf…` | byte copy | `S056/cliCommandNames.js` | 10 543 | `41963156f6330ecf…` |
| S066 + S070 | `…/dist/captures/TsharkCaptureProvider.js` (same path string) | 21 208 | `fdc1fc13d2468fa0…` | byte copy (one entry greens both) | `S066/TsharkCaptureProvider.js` | 21 208 | `fdc1fc13d2468fa0…` |
| S081 | `…/a1722018f28f9df2/…/rea-agents/dist/` | **absent** | — | **tarball-sourced** tar (3) | `S081/rea-agents-6.7.0-dist-cited-members.tar` | 51 200 | `11c07d925277ee13…` |
| S082 | `/var/lib/pacman/local/tinyxxd-1.3.17-1/desc` | 402 | `a2d70e537e159315…` | byte copy | `S082/desc` | 402 | `a2d70e537e159315…` |
| S082 | `…/tinyxxd-1.3.17-1/mtree` | 529 | `a5e4c9e67d9c608f…` | byte copy | `S082/mtree` | 529 | `a5e4c9e67d9c608f…` |
| S082 | `/var/lib/pacman/sync/extra.db` | 8 881 002 | `0b07b40310883996…` | **member extract** tar (1) | `S082/extra-db-tinyxxd-1.3.17-1-desc.tar` | 10 240 | `4c1d650f1528d17c…` |
| S083 | `…/dist/cli-runtime/binary-BVOr2mgE.js` | 649 535 | `64c07dae6fe8b79a…` | byte copy | `S083/binary-BVOr2mgE.js` | 649 535 | `64c07dae6fe8b79a…` |

17 copies totalling 4 281 141 bytes (plus the 11 741-byte map and 139 200 bytes of scripts/receipts; 4 432 082 bytes in this artifacts dir); nothing was copied whole above the 5 MiB bound, and no third-party firmware is involved.

Why the escapes are honest rather than a green wash:
* **S003 / S082 extra.db** are *containers*; the row's own scope is a named member. The tar holds the exact member bytes at their in-container paths (`ghidra/app/util/bin/format/golang/rtti/{GoRttiMapper,GoApiSnapshot}.java`; `tinyxxd-1.3.17-1/desc`), and `source_sha256` pins the container so the gate re-verifies the host container on every run (receipt shows `src[file]`).
* **S023** is not an excerpt: `gzip -dc` reproduces the 10 081 618 source bytes exactly (sha256 `54d10162…` = the row's pin = the map's `source_sha256`). The size bound forces the encoding, not the content.
* **S048/S079/S090/S092** share one host path (the dist dir) and therefore one map key. The tar is deliberately the *union* of every member the four rows cite (23 files, including `cli-runtime/cli.js` 1 813 387 B), so one green does not hide a missing row-specific member.
* **S081**: the installed pipe is gone; the bytes come from the published tarball the row itself pins. Every member digest equals the row's own pin, and the tarball digest equals the row's tarball pin.

## 3. Row-pin audit — 41 pinned digests, zero drift

Every 64-hex digest in the 18 rows was recomputed against the live host object (files, archive members, downloaded tarballs):

| row | pinned digests | result |
|---|---|---|
| S003 | 1 (container `f00d29c2…`) | MATCH — gate re-verifies it as `src[file]` |
| S023 | 1 (`54d10162…`) | MATCH (decoded copy; gate `src[file]`) |
| S035 | 3 (`map_swiss.go 0e2fedbe…`, `map_noswiss.go 03db5a82…`, `map_select_swiss.go c16b55b8…`) | MATCH in 1.25.0 **and** 1.24.6 — the row's "byte-identical" claim holds |
| S056 | 1 (`41963156…`) | MATCH |
| S066 | 2 (`TsharkCaptureProvider.js fdc1fc13…`, `domain/pcap/pcapAnalysis.js 7651b4c5…`) | MATCH |
| S070 | 3 (`fdc1fc13…`, `pcap/PcapProvider.js 16a4d813…`, `pcap/PcapNativeBound.js 24811182…`) | MATCH |
| S079 | 6 (`domain/evidence.js f992d93e…`, `canonicalDigest.js f46d6bd4…`, `DirectAnalysis.js 09d2b222…`, `BinaryLayoutService.js b7c249a7…`, `analysisView.js 2685fc2c…`, `binaryLayoutView.js 5bd86489…`) | MATCH |
| S081 | 4 (`evidence.js a3fb9f02…`, `canonicalDigest.js f46d6bd4…`, `package.json 3f6c47fb…`, tarball `20958a66…`) | MATCH from `rea-agents-6.7.0.tgz` (6 276 963 B downloaded, digest verified) |
| S082 | 2 (`/usr/bin/tinyxxd 7b1e5d0c…`, sync `%SHA256SUM% 3f84d7de…`) | MATCH |
| S083 | 3 (`binary-BVOr2mgE.js 64c07dae…`, `GhidraTargetSnapshot.js a27e4107…`, `ReaGhidraBridge.java db16aed4…`) | MATCH — but see F3 for where the `.java` actually lives |
| S090 | 5 (tarball `531717a0…`, `rust/RustAuditableReader.js 1f3748c9…`, `rust/RustBinaryImage.js 08adaa59…`, `go/GoElfImage.js ee88b9cd…`, `cli-runtime/cli.js 168cd322…`) | MATCH (`rea-agents-6.5.0.tgz` 5 634 033 B downloaded, digest verified) |
| S092 | 10 (same tarball pin + 9 sqlite/artifact readers) | MATCH, all nine |
| S001 S002 S006 S007 S040 S048 | 0 | — (rows pin no digest) |

Installed 6.5.0 `dist/` is file-for-file identical to the tarball's `dist/`: `diff -rq` over 1 574 files, empty, exit 0 — the cross-check S090/S092 assert still holds today.

## 4. Sandbox gate run (the evidence that the defect closes)

`build/sandbox-gate.sh <A> <S> <receipts>`: two `git clone --shared` clones of the lane in scratch, `rev-parse --show-toplevel` asserted equal to each clone dir before anything touches it, copies laid down with `cp -a <A>/corpus/. <clone>/corpus/`, no commit, no checkout, no stash. Working tree of the clone = lane HEAD `fdabdfa4`.

| step | command shape | exit |
|---|---|---|
| A | gate, pristine clone, `--rev c4a38ea` (negative control) | **1** (18 rows: same list as §1) |
| B | gate, clone + copies, `--rev c4a38ea --json` | **0** — `rows_failed []`, 129 rows / 19 checked |
| C | gate, clone + copies, working tree | **0** — `verdict PASS (rows: none)` |
| D | `verify-copies.py --root <clone> --tarball rea6.7.0.tgz` | **0** — 67 checks, 0 failures |
| E | control: append `x` to `S056/cliCommandNames.js`, re-run gate | **1** — `S056 copy-digest-mismatch expected 41963156f633 actual 3702dd46ba0f` |
| F | control: drop the S007 entry from the map, re-run gate | **1** — `S007 no-copy-named` |
| G | restore and re-run | **0** |

Per-row verdicts at step B (from `build/receipts/gate-with-copies.txt`): every one of S001 S002 S003 S006 S007 S023 S035(×2) S040 S048 S056 S066 S070 S079 S081 S082(×3) S083 S090 S092 reads `[resolved/none]`, S126 still reads `[resolved/url-cell] src[file]`; S003, S023 and S082/extra.db show `src[file]` (host container re-verified).

`verify-copies.py` (step D) does three things the gate cannot: (a) re-hashes each copy against the map; (b) byte-compares every `file` copy with the host source (`cmp`-equivalent, `byte-identical` lines) and decodes the gzip copy; (c) opens every archive and compares each member **against the host source member** — not against a transcribed constant — including `S048` vs the installed dist (23 members), `S035` vs both toolchain dirs (28 members each, plus the 3 pinned files cross-version), `S003` vs the zip (2 members), `S081` vs `rea-agents-6.7.0.tgz` (3 members), `S082` vs `tar -xOf /var/lib/pacman/sync/extra.db tinyxxd-1.3.17-1/desc` (1 member). 67/67 OK.

Determinism: a second `build-copies.py` run into a fresh dir reproduced **all 17 copy digests** byte-for-byte and all 17 map entries (compared as JSON values), so the L1 can rebuild the tree from the script alone.

## 5. Findings (routed, not fixed here)

**F1 — S081 is a pipe-absent row, not a copy-missing row.** `/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist` no longer exists (18 rows red, this is the only `source_present=false`). It is resolvable only through the published tarball, whose digest the row already pins. Recommendation for `corpus/SOURCES.md`: say "read from `rea-agents@6.7.0` tarball member `package/dist/...`; local pipe absent since <date>" so the next gate run does not re-diagnose it. The copy's note carries the `curl` + pin-check + rebuild sequence.

**F2 — S082 names two different `desc` records.** The installed `/var/lib/pacman/local/tinyxxd-1.3.17-1/desc` (402 B, `a2d70e53…`, keys `%INSTALLDATE% %VALIDATION% %SIZE% %XDATA%`) is **not** the repository member `tinyxxd-1.3.17-1/desc` of `extra.db` (1 246 B, `a8a2df3f…`, keys `%FILENAME% %CSIZE% %ISIZE% %PGPSIG%`). Both are now retained under `S082/`; the row's wording ("local `desc` … and … member `desc` of extra.db") is correct but easy to read as one object. Recommendation: name both digests in the row's teaches cell.

**F3 — S083's `bridge/ghidra/ReaGhidraBridge.java` is package-relative, not `dist/`-relative.** The installed package root `…/node_modules/rea-agents/` holds `bridge/` *next to* `dist/`, and `dist/bridge/` does not exist (`ls` → ENOENT; `find` over the 1 574 dist files finds no `.java` at all). The file lives at `package/bridge/ghidra/ReaGhidraBridge.java` inside `rea-agents-6.5.0.tgz`, digest `db16aed4…` = the row's pin. The row is right about the bytes and loose about the base path; a fresh reader following the row's URL cell literally (which ends in `dist/`) lands on a missing file. Recommendation: prefix that token with the package root (or `tarball:`) and keep the bridge path out of the dist-relative list.

**F4 — the gate's map vocabulary cannot express what these copies are.** `kind` is `{file, tree-archive}` and the allowed keys are `{copy, sha256, sha256_file, kind, note, source_sha256, rebuild}`. A `gzip`-encoded copy (S023) and a member excerpt (S003, S082) are both masquerading as `file` / `tree-archive`, with the real semantics only in prose `note`. A green row therefore does not tell a machine reviewer whether the copy is the source bytes, a reversible encoding, or a named member. Routed to round 43: extend the map with `encoding: gzip` and `members: [<in-container paths>]` (and validate them in the gate) — or at minimum admit `kind: compressed|member-excerpt` so the distinction is machine-visible. This is a *calibration* defect, not a correctness defect: nothing here is fabricated, but the record is weaker than the evidence.

**F5 (observation, not a defect) — one map entry can green several rows.** S048/S079/S090/S092 name the same directory path; the gate's row verdicts are therefore not independent verifications. The union archive deliberately covers all four rows' cited members; any future row that cites a new member of that tree must extend `REA65_MEMBERS` in `build-copies.py` and re-run it, or its green inherits from a copy that does not contain its file `[INFERENCE: the gate performs no "row cited member present in copy" check; that is exactly why `verify-copies.py` re-derives expected members from the host]`.

## 6. Integration recipe for the L1

```
A=.ufo/waves/round-42/w1/artifacts/R42LocalSrc
cp -a "$A/corpus/evidence/round-42" corpus/evidence/            # 17 copies
cp -a "$A/corpus/evidence/local-sources.json" corpus/evidence/local-sources.json
python3 -I -B tools/round-41/local-source-gate.py --root . \
  --rev c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c                # expect exit 0
python3 -I -B "$A/build/verify-copies.py" --root .               # expect 0 failures
```

The map is the round-41 map plus 17 entries; the pre-existing S126 entry (with its `sha256_file` sidecar) is carried through untouched, and §4 step F shows the entry set is load-bearing rather than decorative. Nothing outside `corpus/evidence/round-42/local-sources/` and `corpus/evidence/local-sources.json` needs to change; no `SOURCES.md` edit is required for the gate to pass (F1–F3 are row-quality improvements, not gate blockers).

## 7. Limits and risks

* `source_sha256` on S003/S023 turns the gate **red if those host files ever drift** — intentional (drift means the row's own pin is stale), but it means the gate now watches two host paths that Ghidra upgrades move. Say so in the freeze note or drop the field to make the gate host-independent.
* The S023 copy is gzip-encoded; the recorded digest is authoritative, and decompression was verified, but a reviewer who `sha256sum`s the `.gz` and compares it to the row's pin will see a mismatch. The `note` says this in words; F4 is the machine-readable fix.
* The S081 copy can only be rebuilt with network access to the npm registry; the tarball digest is pinned, so the rebuild either matches or fails loudly.
* The S048 archive is a curated member list. It is complete for the four rows as they read today; it is not the whole package, and `rebuild` does not re-derive the member list from SOURCES.md.
* Tar determinism is a property of `build-copies.py` (sorted names, `mtime` 0, `uid/gid` 0, GNU format, no pax headers), verified by a second run — not of GNU tar's defaults, so hand-rebuilding with `tar` will produce a different digest.
* No tools were installed, upgraded or moved (pacman untouched; nothing written into any PATH dir). Tools used, for the record: python3 3.14.8, git 2.56.0, GNU tar 1.35, gzip 1.15, curl 8.23.0.

## 8. Artifacts

```
build/build-copies.py        builder (stdlib; TMPDIR-honouring; writes copies + map + manifest)
build/verify-copies.py       independent checker (map digests, byte-identity vs host, archive members vs host, gz decode)
build/sandbox-gate.sh        clone → copy → gate → 3 controls → verify, all receipts
build/copies.tsv             per-copy manifest: host path/size/sha256, disposition, copy path/bytes/sha256
build/verification.tsv       artifacts-only verify run (66/67 OK; the one FAIL is S126, whose round-41 copy is already in the lane and was verified in-clone instead)
build/receipts/              gate-baseline-host.json (exit 1) · gate-pristine.json (A, exit 1) ·
                             gate-with-copies.{json,txt} (B/C, exit 0) · verify-clone.tsv (D, 67/67) ·
                             gate-corrupt.json (E, exit 1) · gate-dropped-entry.json (F, exit 1) ·
                             gate-restored.json (G, exit 0)
corpus/evidence/local-sources.json           the updated map (18 entries: 17 new + S126)
corpus/evidence/round-42/local-sources/…     the 17 copies listed in §2
```
