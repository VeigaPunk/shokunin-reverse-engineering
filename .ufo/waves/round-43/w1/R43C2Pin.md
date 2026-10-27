# R43C2Pin — independent fresh row-pin audit of the 18 host-local SOURCES rows

**Verdict: DEFECTS FOUND — 4 C2 blockers.** Every row's *host object* re-verifies today (no MATCH/DIFT
surprise among the 18 present path slots), but four structural defects break R43-C2 as written, and one
would let a do-nothing-plus-stub control reach the gate's green. Details below; every claim carries the
exact command and output.

Scope: fresh, independent audit of the 18 rows the round-41 gate reds at the base
(`6b9e64fe7e0de202d9383baad5792fbfe039a743`). I did **not** read the sibling seat `R43C2Land`'s
artifacts (`.ufo/waves/round-43/w1/artifacts/R43C2Land/`); every datum below was recomputed from the
base commit's `corpus/SOURCES.md`, the live host, and the published upstream tarballs. The round-42
seat `R42LocalSrc`'s artefacts were read only as *the prior round's claim under test*, and every one
of its numbers was independently recomputed.

Scratch: `/fast/scratch/hyaku/kaidoku-r43/w1-R43C2Pin` (removed at exit). Artefacts:
`.ufo/waves/round-43/w1/artifacts/R43C2Pin/`.

---

## 0. The audit's central finding, up front

**No row among the 18 pins a digest in its URL cell.** The gate's `row-pin: url-cell` rule reads the
URL cell (column 2) only:

```
tools/round-41/local-source-gate.py:341  row_pins_url = digests_in(URL.sub(" ", url_cell))
tools/round-41/local-source-gate.py:236  scope = "url-cell" if row_pins else "none"
tools/round-41/local-source-gate.py:238  if row_pins and want not in row_pins: fail("row-pin-conflict")
```

Recomputed with the gate's own functions over the base table
(`artifacts/R43C2Pin/row-pin-audit.json`, `artifacts/R43C2Pin/row-verdicts.tsv`):

| row | URL-cell 64-hex pins | notes |
|---|---|---|
| S001 S002 S003 S006 S007 S023 S035 S040 S048 S056 S066 S070 S079 S081 S082 S083 S090 S092 | **0 each** | every one of the 18 |

The gate itself confirms this at the base: all 18 fail with reason `no-copy-named` and **no** row
reports `row-pin-conflict`; the only row in the whole table that reports scope `url-cell` is S126
(`resolved/url-cell`). So the plan's phrase *"each row-pinned digest (where the URL cell pins one)
equals the entry or its source digest"* resolves to an **empty conjunction** for all 18 rows. The row
digests that do exist live in the **anchor** cell (column 6, 41 digest slots over 12 rows), which the
gate deliberately does not consult — by design, per its own comment at `local-source-gate.py:232-236`:

> "Digests elsewhere in the row describe members or derived artefacts (S035 pins member files, S082
> the pacman fields), so they cannot bind a directory archive and are not consulted here."

**Consequence (blocker B1).** The map's `sha256` for these 18 entries is bound to *nothing the row
says*. The plan's "row-pinned digest equals the entry or its source digest" clause is therefore
vacuous as written, and the prepared map satisfies it trivially while reproducing **29 of the 41**
anchor-cell digest slots as archived member bytes and **none** of the other 12. See §3.

---

## 1. Per-row table — host path existence and digest verdict

Method: parse the base table, extract each row's absolute host paths with the gate's own
`external_paths()`, recompute each present file's sha256, compare against every 64-hex digest in the
row (URL cell and anchor cell). Full machine-readable output:
`artifacts/R43C2Pin/row-pin-audit.json`, `artifacts/R43C2Pin/row-verdicts.tsv`.

**Verdict legend.** `MATCH` = host digest equals a digest written in the row. `DIFT` = host present,
digest differs. `ABSENT` = host path does not exist today.

| row | out-of-lane path(s) named in URL cell | host state today | row digest → verdict |
|---|---|---|---|
| S001 | `~/.agents/skills/reverse-engineer-anything/SKILL.md` | FILE 23 437 B | **pins nothing** (no digest anywhere in row) — file digest `056dee04…c03692` |
| S002 | `…/references/native-and-artifacts.md` | FILE 18 911 B | **pins nothing** — file digest `18b8828a…5cf8f9` |
| S003 | `…/ghidra_12.1.4_PUBLIC/…/lib/Base-src.zip` | FILE 7 481 132 B | `f00d29c2…a8d804` → **MATCH** (container digest) |
| S006 | `…/docs/GhidraClass/BSim/BSimTutorial_Intro.md` | FILE 4 664 B | **pins nothing** — digest `a23562a3…c296c33e` |
| S007 | `…/docs/ChangeHistory.md` | FILE 491 055 B | **pins nothing** — digest `c6b25301…86f65c4` |
| S023 | `…/data/typeinfo/golang/go1.25.0.json` | FILE 10 081 618 B | `54d10162…c3f16252` → **MATCH** |
| S035 | `~/.local/opt/go-1.25.0/src/internal/abi` | **ABSENT** (dir) | pins 3 member digests → see §2.2 (all **MATCH** upstream) |
| S035 | `~/.local/opt/go-1.24.6/src/internal/abi` | **ABSENT** (dir) | same 3 pins → **MATCH** upstream |
| S040 | `…/rea-agents/dist/cli/artifactCommands.js` | FILE 7 042 B | **pins nothing** (line anchors only) — digest `c4d56e03…4f6aaa` |
| S048 | `…/rea-agents/dist` (dir) | DIR present (1 574 files, 22 972 248 B) | **pins nothing** (line anchors only) |
| S056 | `…/rea-agents/dist/cliCommandNames.js` | FILE 10 543 B | `41963156…96255dd3` → **MATCH** |
| S066 | `…/dist/captures/TsharkCaptureProvider.js` | FILE 21 208 B | `fdc1fc13…76d30549` → **MATCH**; second pin `7651b4c5…597c641` (pcapAnalysis.js) → not a copy member, see §3 |
| S070 | `…/dist/captures/TsharkCaptureProvider.js` | FILE 21 208 B | `fdc1fc13…` → **MATCH**; pins `16a4d813…8ed64d4` (PcapProvider.js) and `24811182…38cd2` (PcapNativeBound.js) → §3 |
| S079 | `…/rea-agents/dist` (dir) | DIR present | 6 member pins → **all MATCH** in the 6.5.0 tarball (§2.1) |
| S081 | `~/.npm/_npx/a1722018f28f9df2/…/dist` (dir) | **ABSENT** | 3 member pins + tarball `20958a66…f51f90` → **MATCH** in the published 6.7.0 tarball (§2.1) |
| S082 | `/var/lib/pacman/local/tinyxxd-1.3.17-1/desc` | FILE 402 B | pins 2 member digests → §2.3, **MATCH** (textual) |
| S082 | `/var/lib/pacman/local/tinyxxd-1.3.17-1/mtree` | FILE 529 B (gzip) | same 2 pins → §2.3, **MATCH** |
| S082 | `/var/lib/pacman/sync/extra.db` | FILE 8 881 002 B | same 2 pins → §2.3, **MATCH** |
| S083 | `…/dist/cli-runtime/binary-BVOr2mgE.js` | FILE 649 535 B | `64c07dae…c00df` → **MATCH**; pins `a27e4107…f03f52b` (GhidraTargetSnapshot.js) and `db16aed4…c0a105` (ReaGhidraBridge.java) → §3 |
| S090 | `…/rea-agents/dist` (dir) | DIR present | tarball `531717a0…8e699` → **MATCH**; 4 member pins → **all MATCH** (§2.1) |
| S092 | `…/rea-agents/dist` (dir) | DIR present | tarball `531717a0…` → **MATCH**; 10 member pins → **all MATCH** (§2.1) |

**Count:** 18 rows, **21** out-of-lane path slots, **17** distinct paths.
Present today: **18** path slots (14 files + 4 directory slots naming the same 6.5.0 `dist/` tree).
Absent today: **3** path slots on **2** rows — **S035** (both Go trees) and **S081** (the 6.7.0 npx
pipe). No `DIFT`: every host object that exists hashes exactly to the digest its row names.

### 1.1 Does every out-of-lane path still exist on the host?

**No — 2 of 18 rows have an out-of-lane path that no longer exists**, and both are handled differently
by the prepared map:

```
$ ls -d /home/vgpnk/.local/opt/go-1.2*
ls: cannot access '/home/vgpnk/.local/opt/go-1.2*': No such file or directory
$ ls -d /home/vgpnk/.npm/_npx/a1722018f28f9df2
ls: cannot access '/home/vgpnk/.npm/_npx/a1722018f28f9df2': No such file or directory
```

The only Go tree on the host is `go1.27.3` (`/home/vgpnk/.local/opt/go1.27.3/go`, a *different*
version, whose `src/internal/abi` is 27 files and lacks `map_swiss.go`/`map_noswiss.go` entirely —
see §2.2). The `a1722018f28f9df2` npx cache is gone; the surviving `ad9a3fdbcad992c6` npx cache holds
6.5.0 only.

### 1.2 The 6.5.0 npx path is volatile — it vanished and returned *during this audit*

Observed live, same host, same wave:

```
05:20  $ ls -la /home/vgpnk/.npm/_npx
       a3ecabc7dc353655  ba38acecdf97096f  db2207bf930d61c8      <- ad9a3fdbcad992c6 GONE
05:21  $ ls -la /home/vgpnk/.npm/_npx
       a3ecabc7dc353655  ad9a3fdbcad992c6  ba38acecdf97096f  db2207bf930d61c8   <- BACK
       $ stat -c '%n %y' .../ad9a3fdbcad992c6
       .../ad9a3fdbcad992c6 2026-10-27 05:21:00.830803489 -0300
```

The directory reappeared with mtime equal to the moment of observation, i.e. an `npx` cache
rehydration by a concurrent process (the host runs `npx -y rea-agents@6.5.0` for REA). Its content is
correct — §2.1 proves the rehydrated `dist/` tree is byte-identical to the published tarball — but the
**path's existence is not stable**, and the gate's `source_present` advisory for the seven rows that
name it (S040, S048, S056, S066, S070, S079, S083, S090, S092) is correspondingly unstable. This is
the mechanism behind the plan's own disclosed limit ("host paths that drift later re-red the row in
the gate's advisory output"), observed live rather than inferred.

---

## 2. Container verification — container digest **and** cited member digests

### 2.1 npm tarballs (S079, S081, S090, S092, and the 6.5.0 `dist/` tree)

Both published tarballs were fetched fresh and hashed:

```
$ curl -sS -o rea-agents-6.5.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz
531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699  rea-agents-6.5.0.tgz
7ea5e6f669bc18c45dbf5dba653edaa1ada07ab3                          rea-agents-6.5.0.tgz   (sha1)

$ curl -sS -o rea-agents-6.7.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz
20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90  rea-agents-6.7.0.tgz
11f23ba377303a5c28b3162180cf2bf3f3643708                          rea-agents-6.7.0.tgz   (sha1)
```

Both match the rows' pins exactly (S090/S092 pin the 6.5.0 tarball `531717a0…`; S081 pins the 6.7.0
tarball `20958a66…` **and** its sha1 `11f23ba3…`, both confirmed). The 6.5.0 sha1 `7ea5e6f6…` also
matches S080's `dist.shasum`.

Member digests, recomputed from the extracted tarballs and cross-checked against the live npx tree:

```
6.5.0 tarball members (all MATCH):  rust/RustAuditableReader.js 1f3748c9…  rust/RustBinaryImage.js 08adaa59…
  go/GoElfImage.js ee88b9cd…  cli-runtime/cli.js 168cd322…  domain/evidence.js f992d93e…
  domain/canonicalDigest.js f46d6bd4…  application/DirectAnalysis.js 09d2b222…
  application/binaryDiagnostics/BinaryLayoutService.js b7c249a7…  domain/analysisView/analysisView.js 2685fc2c…
  domain/analysisView/binaryLayoutView.js 5bd86489…  sqlite/SqliteDatabase*.js 5a908695… edfcd90f…
  92df76ff… 018756d9… c8af51f8… ebb39f58… 6e49c2ab…  c7a0eff5…  artifacts/readStableArtifact.js 06a23746…
6.7.0 tarball members (all MATCH):  dist/domain/evidence.js a3fb9f02…  dist/domain/canonicalDigest.js f46d6bd4…
  package.json 3f6c47fb…
```

The live npx `dist/` tree was compared file-for-file against the tarball's `package/dist` subtree:

```
tarball dist files: 1574   npx dist files: 1574
only_in_tarball: 0   only_in_npx: 0   content_differing: 0     -> IDENTICAL
package.json: a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c  (both)
```

So S079/S090/S092's "compared with the installed copy" claim and S079's "file-for-file identical to
the tarball" claim are **CONFIRMED** today, and the rehydrated npx tree is a faithful stand-in for the
published tarball.

### 2.2 S035 — Go `internal/abi` (both host trees ABSENT)

The row pins three member digests and claims the 1.25.0 and 1.24.6 copies are byte-identical. The
host trees are gone, so I verified against upstream
`https://raw.githubusercontent.com/golang/go/{go1.25.0,go1.24.6}/src/internal/abi/<file>`:

```
map_swiss.go       go1.25.0 0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383  MATCH
                   go1.24.6 0e2fedbedf244b5fe360a3c6e5ca71502ea6ee7a4043bd83b96a13d1af76c383  MATCH
map_noswiss.go     go1.25.0 03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291  MATCH
                   go1.24.6 03db5a82addb4c8cb471aa93b0b75c3eee8ecf39326ee646f398a9b2e25a7291  MATCH
map_select_swiss.go go1.25.0 c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718  MATCH
                   go1.24.6 c16b55b87bb7b5873fea4b9468ee60cb24d9b33240c5e58f7ede6584af799718  MATCH
```

The row's byte-identity claim is **CONFIRMED** for the three pinned files (and, in fact, for 22 of the
28 files in the tree — `escape.go`, `iface.go`, `switch.go`, `symtab.go`, `type.go` differ between the
two versions; the round-42 tar preserves that difference correctly). The upstream tree is 26 files at
the API level; the prepared tars carry 28 (they additionally hold `testdata/x.go` and `testdata/x.s`,
which the GitHub contents API does not list). Re-fetching all 28 members of each prepared tar from
upstream and comparing digests: **0 mismatches for both versions** (`artifacts/R43C2Pin/member-recheck.json`,
and the upstream re-fetch in §5).

### 2.3 S082 — pacman `desc` / `mtree` / `extra.db`

The row pins two digests: `7b1e5d0c…` (the installed `/usr/bin/tinyxxd` binary) and `3f84d7de…`
(the sync DB's `%SHA256SUM%` for the `.pkg.tar.zst`).

```
$ sha256sum /usr/bin/tinyxxd
7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65   MATCH
$ zcat /var/lib/pacman/local/tinyxxd-1.3.17-1/mtree | grep 7b1e5d0c
./usr/bin/tinyxxd time=1790704346.0 size=38928 sha256digest=7b1e5d0c…   MATCH
$ tar -xzf /var/lib/pacman/sync/extra.db tinyxxd-1.3.17-1/desc   # member extracted
a8a2df3fb47706ab42be91d0161fb571ae3dde63ab73dc626205721692435941  tinyxxd-1.3.17-1/desc
$ grep -A1 '%SHA256SUM%' tinyxxd-1.3.17-1/desc
3f84d7de243de1391f97cfbc90adf01bb5b784fccb249372b67accf4e65607ce   MATCH
```

Both pins **MATCH**. Note the two `desc` records are genuinely different records (the installed one
has `%INSTALLDATE%`/`%VALIDATION%`/`%SIZE%`/`%XDATA%`; the repo member has `%FILENAME%`/`%CSIZE%`/
`%PGPSIG%`/`%SHA256SUM%`) — `diff` confirms, and the round-42 note documents this. The row's anchor
quotes `%VERSION% 1.3.17-1`, `%BUILDDATE% 1790704346`, `%PACKAGER%`, `%URL%` from the *installed*
record: all present and correct today.

### 2.4 S003 — Ghidra `Base-src.zip`

Container digest **MATCH** (`f00d29c2…a8d804`, 7 481 132 B, 3 865 members). The row's two cited
members are present at their in-zip paths:

```
ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java  765d25365a8c379c929097a6602df5fa75049f871eb0f610d5376d630d95eb7d
ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java    2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95
```

The row pins the *container* digest, not the member digests, so the member digests are my own
addition (the round-42 seat archived the same two members and its `verification.tsv` records the same
two values — independently confirmed).

---

## 3. The C2 blockers the plan must route around

### B1 — the "row-pinned digest" clause is vacuous, and 12 of 41 anchor-digest slots are reproduced by no in-lane copy

The 18 rows carry **41 anchor-cell digest slots** (38 distinct digests; 6 rows — S001, S002, S006,
S007, S040, S048 — pin nothing at all). This is the set the plan means by "where the row pins one".
The prepared copies reproduce **29** of the 41 slots as archived member bytes. **12 are not reproduced
by any in-lane copy** (`artifacts/R43C2Pin/copy-anchor-coverage.json`):

| row | unreproduced anchor digest | what it is | why |
|---|---|---|---|
| S003 | `f00d29c2…a8d804` | the 7.1 MiB zip container | not copied (over bound); pinned via `source_sha256` instead |
| S023 | `54d10162…c16252` | the 10 MiB json | gzip-encoded in the copy; pinned via `source_sha256` |
| S066 | `7651b4c5…597c641` | `domain/pcap/pcapAnalysis.js` | **not in the 23-member tar** |
| S070 | `16a4d813…8ed64d4` | `pcap/PcapProvider.js` | **not in the 23-member tar** |
| S070 | `24811182…38cd2` | `pcap/PcapNativeBound.js` | **not in the 23-member tar** |
| S081 | `20958a66…f51f90` | the 6.7.0 tarball | not copied; the 3 cited members are |
| S082 | `7b1e5d0c…03ae65` | installed `/usr/bin/tinyxxd` binary | the mtree copy carries the digest *as text*, not the bytes |
| S082 | `3f84d7de…607ce` | `.pkg.tar.zst` `%SHA256SUM%` | present as text inside the copied `desc` member |
| S083 | `a27e4107…f03f52b` | `ghidra/GhidraTargetSnapshot.js` | **not in the 23-member tar** |
| S083 | `db16aed4…c0a105` | `bridge/ghidra/ReaGhidraBridge.java` | **not in the 23-member tar** (and not under `dist/` at all) |
| S090 | `531717a0…8e699` | the 6.5.0 tarball | not copied |
| S092 | `531717a0…8e699` | the 6.5.0 tarball | not copied |

Seven of these are benign-by-design (container/tarball digests pinned via `source_sha256`, or values
that live as *text* inside a copied member). **Five are genuine gaps**: the members
`domain/pcap/pcapAnalysis.js`, `pcap/PcapProvider.js`, `pcap/PcapNativeBound.js`,
`ghidra/GhidraTargetSnapshot.js` and `bridge/ghidra/ReaGhidraBridge.java` are named with digests by
rows S066, S070 and S083, and **no in-lane copy contains their bytes**. The round-42 seat's own
`verification.tsv` never mentions them (`grep -E 'pcapAnalysis|PcapProvider|PcapNativeBound|GhidraTargetSnapshot|ReaGhidraBridge' verification.tsv` → no match), i.e. the gap was inherited silently.

All five are present in the published 6.5.0 tarball with exactly the digests the rows pin (verified
against `rea-agents-6.5.0.tgz`):
`domain/pcap/pcapAnalysis.js 7651b4c5…`, `pcap/PcapProvider.js 16a4d813…`,
`pcap/PcapNativeBound.js 24811182…`, `ghidra/GhidraTargetSnapshot.js a27e4107…`,
`bridge/ghidra/ReaGhidraBridge.java db16aed4…` — all **MATCH**.

**Route-around:** extend the S048 member list from 23 to 28 members (adding those five, with
`bridge/ghidra/ReaGhidraBridge.java` stored at its package-relative path). Cost measured: the
28-member deterministic tar is **2 324 480 B** — still under the 5 MiB bound (the 23-member one is
2 048 000 B). The gate and the map need no change; only `build-copies.py`'s `REA65_MEMBERS` list and
the map digest.

### B2 — the prepared map does not satisfy its own stated invariant, and the gate cannot see it

`P43-C2` says: *"each row-pinned digest (where the URL cell pins one) equals the entry or its source
digest"*. Since **no** URL cell pins a digest (§0), the predicate as written has 18 vacuous
instances and asserts nothing. The gate's `row-pin-conflict` branch is therefore dead for this claim,
and the gate's only content binding is *map digest == copy digest* — i.e. the map and the copy can
collude freely (see B3). The prepared map's `note` fields assert the stronger property
("sha256 of the copy equals the digest recorded in the row's anchor/teaches cell where the row pins
one") — for S066/S070/S083 that claim is **false** of the copies they ship.

**Route-around:** restate the predicate as "the copy reproduces every anchor-cell digest the row
names, either as archived member bytes or as a `source_sha256` on the host container" and land a
counter that checks it — the gate cannot be its own check for this claim.

### B3 — the gate greens on a stub: a do-nothing-plus-stub control reaches exit 0

The round-38 lesson named in the plan's CTL-C2-1 ("a counter must not green on a stub at the old
path") is **not** enforced by `local-source-gate.py`, because of §0: with zero URL-cell pins, the
gate only compares the map's `sha256` against the copy's own bytes. Both directions of the trivial
fix — replacing a copy with a stub *and* updating the map to match — leave the gate green.

Proven in a sandbox clone (`git clone -q --shared <lane> "$D/lane"`, `git rev-parse --show-toplevel`
asserted == `$D/lane` before any write; no commit made):

```
CONTROL A: S001 copy replaced by 11 bytes of stub, map sha256 updated to the stub digest
CONTROL B: S003 member tar replaced by a 1-member tar of "fake java", map sha256 updated
CONTROL C: S035 copy replaced by the EMPTY tar that build-copies.py emits today
  -> local-source-gate.py --rev 6b9e64fe...  =>  verdict PASS (rows: none)   EXIT=0
```

Receipts: `artifacts/R43C2Pin/receipts/gate-stub-green.json` (A+B), `artifacts/R43C2Pin/receipts/gate-empty-tree-stub-green.json` (C).
The pristine prepared copies also green (`artifacts/R43C2Pin/receipts/gate-prepared-green.json`, exit 0,
`rows_failed []`) — so the gate distinguishes *nothing* between the honest copies and the stubs.

**Route-around:** the C2 counter must carry a content binding the gate lacks — e.g. for each of the
18 rows, assert that the copy's bytes (or its archived members) reproduce the anchor-cell digest(s)
the row names, and that a stub control of the same shape reds. As things stand, C2's stated kill rule
("a control reaching exit 0 stops C2") is satisfied by a stub, i.e. the claim as specified is
satisfiable by work that does not preserve any cited byte.

### B4 — re-running the round-42 build script today silently produces an **empty** S035 copy

`build-copies.py` is the tool that produced the prepared copies. It is the obvious rebuild command
recorded in every map entry's `rebuild` field. Re-run today, unchanged, it emits a **0-member tar**
for both S035 entries, because `tar_dir()` on a non-existent directory yields an empty tar rather
than failing:

```
$ python3 -I -B .../R42LocalSrc/build/build-copies.py --out $S/repro/out --tarball-dir $S/repro
S035  tree  dir-tree:0  False  ...  10240  .../S035/internal-abi-go1.25.0.tar  84ff9269…  tree-archive
S035  tree  dir-tree:0  False  ...  10240  .../S035/internal-abi-go1.24.6.tar  84ff9269…  tree-archive
map entries: 17
```

Both new digests differ from the prepared ones (`069d0c88…`, `8530a509…`) — so a naive rebuild
would **change the S035 map digests** and silently drop all three pinned Go members, while still
greening the gate (control C above). The prepared 28-member tars are good; the *rebuild command
recorded in the map* is not reproducible on this host today.

**Route-around:** either (a) re-source S035 from the upstream Go trees (`raw.githubusercontent.com`,
verified identical — §2.2) and make the build script fail loudly on an absent source directory
rather than emitting an empty tar, or (b) land the prepared tar bytes and change the `rebuild` field
to name the upstream tarball fetch instead of the vanished host path. Also note the script prints
`map entries: 17` — it writes a 17-entry map and the S126 entry is only preserved if the pre-existing
map is read first (`--out` pointing at a lane that already has `corpus/evidence/local-sources.json`);
running it against an empty output directory drops S126.

---

## 4. What is confirmed (so the L1 does not have to redo it)

- The gate tool is byte-identical at the base and on disk:
  `cafe232a196dd8446bd9b0420b32bf696cba427770eb79edda2be15a45a4ece7`
  (`git show 6b9e64f:tools/round-41/local-source-gate.py | sha256sum` == `sha256sum` of the file);
  its last commit is `d764389e` (round-41).
- The gate at the base exits **1** with exactly the 18 rows failed
  (`artifacts/R43C2Pin/receipts/gate-base.txt`); `rows_total` 134, `rows_checked` 19 (the 19th is S126, which
  resolves).
- The prepared map + prepared copies make the gate exit **0** today in a fresh clone
  (`artifacts/R43C2Pin/receipts/gate-prepared-green.json`): all 18 rows `resolved`, `rows_failed []`.
- The lane's current committed map holds **only** the S126 entry, and S126's copy
  (`corpus/evidence/round-41/s126/lead1-avm-image.tsv`, `f205807d…c8539eb0`) and its sidecar are
  committed at the base — so a landing that replaces the map must re-add S126 (the prepared map does:
  18 keys = 17 new + S126).
- No prepared copy exceeds the 5 MiB bound (largest: S048 tar 2 048 000 B; S083 file 649 535 B).
- No third-party firmware image is among the copies; the only network artefacts are the two npm
  tarballs (MIT/Apache npm packages), cited by URL + sha256, never copied into the lane.

---

## 5. Exact commands used (reproducible)

```
# base table
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show \
    6b9e64fe7e0de202d9383baad5792fbfe039a743:corpus/SOURCES.md

# gate at base (exit 1, 18 rows)
python3 -I -B tools/round-41/local-source-gate.py --root <LANE> \
    --rev 6b9e64fe7e0de202d9383baad5792fbfe039a743

# host digests
sha256sum <each present out-of-lane file>
sha256sum /usr/bin/tinyxxd
zcat /var/lib/pacman/local/tinyxxd-1.3.17-1/mtree
tar -xzf /var/lib/pacman/sync/extra.db tinyxxd-1.3.17-1/desc

# published tarballs
curl -sS -o rea-agents-6.5.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz
curl -sS -o rea-agents-6.7.0.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz
sha256sum rea-agents-6.{5,7}.0.tgz ; sha1sum rea-agents-6.{5,7}.0.tgz
tar -xzf rea-agents-6.5.0.tgz -C x650 ; (cd x650 && find package/dist -type f | sort | xargs sha256sum) > m650.txt

# upstream Go members (S035)
curl -sS https://raw.githubusercontent.com/golang/go/go1.25.0/src/internal/abi/<file>
curl -sS https://raw.githubusercontent.com/golang/go/go1.24.6/src/internal/abi/<file>

# prepared-copy rebuild attempt (produces the empty S035 tar)
python3 -I -B .../R42LocalSrc/build/build-copies.py --out $S/repro/out --tarball-dir $S/repro

# sandbox clone controls (no commit made)
D=$(mktemp -d "$S/fx.XXXX"); git clone -q --shared <LANE> "$D/lane"
git -C "$D/lane" rev-parse --show-toplevel   # asserted == "$D/lane"
```

Scratch was removed on exit (`trap 'rm -rf -- "$S"' EXIT`).

---

## 6. Recommendation to the L1 (routing, not implementation)

1. Land the 17 prepared copies as-is (they are correct and the gate greens), **but** re-state
   `P43-C2`'s pin clause against the **anchor** cell and extend the S048 member list 23 → 28 to
   close B1/B2 (the extra tar is 2 324 480 B, still under the 5 MiB bound).
2. Add a content-binding counter for C2 that a stub control reds (B3), rather than relying on
   `local-source-gate.py` alone; the gate's `row-pin-conflict` branch is dead for these rows and will
   stay dead unless the URL cells are changed — which the plan forbids ("the `corpus/SOURCES.md` table
   itself is byte-identical to the base").
3. Fix or re-point S035's rebuild (B4): make the build fail loudly on an absent source, and re-source
   from the upstream Go trees rather than the vanished `/home/vgpnk/.local/opt/go-1.25.0` path.
4. Record in the plan's disclosed limits that 2 of 18 rows' host paths are absent today (S035 ×2, S081
   ×1 path) and that the 6.5.0 npx path is volatile — observed live at 05:20/05:21, not inferred.

## 7. Scope note

This seat audited rows only. It did not touch `corpus/`, `tools/`, `plans/`, `SKILL.md`, `PROVINCE.md`,
`SCORECARD.md`, `SHONEN.md` or `LOG.md`, did not read `R43C2Land`'s artefacts, and made no VCS mutation
in the lane or the fleet (the sandbox clones were read-only working copies; no commit, no `git add`).
No tool was installed or upgraded this wave.
