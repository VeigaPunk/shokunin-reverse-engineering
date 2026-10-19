# SEAT CU-1 — chain cross, role custody (arc3-loop1-round3)

Task (seat line): corroborate the round's custody state — recompute the 5 paths'
sha256+stat independently vs EX-29's pair; verify the solc-prefix reuse did not
touch any custody path; corroborate the compiler-check receipts.

Status at seat close (see §5 for the one open item): **PRE-side corroborated on
three independent sources; compiler receipts all re-derived; the POST pair had
not landed at last poll** (EX-29's post capture / C2's closing pair). All
artifacts under `.ufo/waves/arc3-loop1-round3/claims/cross/CU-1/`; scratch in
`/var/tmp/cu1-r3`; custody paths hash/stat-captured only (no content reads, no
writes); no git mutations.

## 1. Work performed (evidence pointers)

- Read `claims-frozen.md`, the r1 EVM entry (+ its recheck line), r2 c3 custody
  debt D1–D7, the r2 CU-1 seat report, and the custody-pair README.
- **Independent capture of the 5 custody paths** — three sha256 implementations
  (coreutils / `openssl dgst` / Python `hashlib`) + GNU `stat` lstat fields +
  epoch↔UTC/local renders: `capture.sh` → `capture-pre-indep.txt` (13:07:07Z).
- **My own grader** `grade-custody.py` (parses a v2 receipt; recomputes live;
  two modes): `grade-live` (16 fields × 5 paths vs live) and `diff` (receipt vs
  receipt, lists every moved field).
- **EX-29's pre-pair receipt corroborated**: `grade-live-vs-EX29-pre.txt`
  (80/80 cells MATCH), `diff-r2post-vs-r3pre.txt` (r2 post vs r3 pre), plus the
  tool's own `verify … --live` at two revision stamps
  (`tool-verify-live-EX29pre.txt`, `revstamped-checks-*.txt`).
- **Third source** — a fresh capture by the round's revised tool diffed against
  EX-29's receipt: `diff-EX29pre-vs-toolcapture.txt`, `cu1-mid1-capture.txt`
  (+ `.sha256`).
- **Independent write-guard / D3 attack battery** under a fake `HOME` so the
  "custody paths" resolve inside scratch (the real paths can never be at risk):
  `write-guard-attack.sh` → `write-guard-attack.out`, `write-guard-attack-rev2.out`.
- **Drift watcher** (30 × 60 s, read-only; log only): `watch.sh` →
  `watch-log.txt`, `poll-log.txt`.
- **Compiler-check receipts re-derived** (commands in §3c): `attest-rerun.txt`
  (EX-01's cache-attestation script re-run), `wasm-core-rerun.txt` (embedded-wasm
  capture re-run on prefix + ambient trees), `ex04-hash-rerun.txt`.
- **Cross-wave continuity table**: `continuity.py` → `continuity-table.txt`
  (9 captures parsed across the four receipt shapes) and peer sidecar
  re-derivation.
- Cross-wave receipt stability: r1 receipts' own bytes re-hashed (match r2 CU-1's
  claimed digests) and the r2 gate/receipt sidecars re-derived.
- Note on file names: some artifact names carry the tool revision observed at
  *creation* (`revstamped-battery-*.txt`, `revstamped-checks-*.txt`); the tool
  moved 7 times during this seat, so the **header line inside each file (REV=…)
  is authoritative**, not the file name.

## 2. Proposed changes

- **none** — the custody seat owns no repo target; C2's EX-21 target
  (`.ufo/gates/custody-pair/`) was under active revision during this seat's run
  (six revisions observed: `112d01dc` → `68e30768` → `d9be407d` → `08fb6833` →
  `ec2b2d48` → `57dffff1`), so patch text from here would race. Two measured
  notes for EX-21/parent instead (both revision-stamped, both §4):
  (N1) the landed README must document the `--require-paths` gate — at rev
  `ec2b2d48` `grep require-paths .ufo/gates/custody-pair/README.md` → 0 hits
  while the code implements it; (N2) all receipts/tool docs must self-pin the
  *final* revision's sha256 (rule #14), since the pre-pair receipt pins
  `112d01dc` and the tool has since moved.

## 3. Before → after measurement

### 3a. The pre-pair (task item 1) — three sources agree

| source | time (UTC) | method | result |
|---|---|---|---|
| CU-1 independent capture | 13:07:07 | 3 × sha256 impls + GNU stat | `SHA256_AGREE=yes` on 5/5; inodes 11341318 / 11341316 / 37793921 / 25991953 / 40274 |
| EX-29 pre-pair receipt (`claims/c2/receipts/config-pre-pair-v2r3.txt`, tool `112d01dc`) | 13:06:57 | receipt | `grade-live-vs-EX29-pre.txt`: **80/80 field cells MATCH**; sha256 agrees hashlib == coreutils == receipt on 5/5 |
| CU-1 capture via current tool (rev-stamped), diffed against EX-29's receipt | 13:10/13:11 | receipt vs receipt | `DIFF: NO-MOVED-FIELDS` (16/16 × 5) |
| EX-29 revised-tool pre-pair (`config-pre-pair-v2r3-revised.txt`, tool `7cd19c3c`) | 13:15:44 | receipt | sidecar `553fe82d…` re-derived; `grade-live-vs-EX29-pre-revised.txt`: **80/80 MATCH**; `diff-EX29pre-vs-revised.txt` vs the 112d01dc receipt: NO-MOVED-FIELDS |

Tool-side verdicts at stamp revisions: `verify <EX-29 pre> --live` → `MATCH
paths=5/5 drift=0 exit=0` (run at `d9be407d` and again at `57dffff1`; the latter
also with `--require-paths 5`); `selftest` → `CLEAN cases=21 passed=21 failed=0
exit=0` at `57dffff1` (15/15 at `68e30768` earlier in the window; the C2 claim's
"15 → ≥17" floor is already exceeded, re-check at landing).

Continuity (my grader `diff`, field-exact): r2 post (12:31:44Z) → r3 pre
(13:06:57Z) = `4/5 MATCH 16/16; config.toml MOVED=11/16` — SHA256
`8cbacd48…`→`bc66d543…`, INODE 34530637→37793921, MODE 600→644, MTIME/CTIME
`2026-10-18T23:20:43Z`→`2026-10-19T12:57:45Z` (`, `diff-r2post-vs-r3pre.txt`).
r1 v1 receipt (`config-pre-pair.txt`, 09:57:18Z) and r2 (`custody-sha256.txt`,
10:00:43Z) both carry the same 4 stable digests as the live tree now: 4/5
identical across ~3h10m; the one move is `config.toml`.

Cross-wave table (9 captures, all four receipt shapes parsed mechanically):
`continuity.py` → `continuity-table.txt` — every capture agrees on 4/5 paths
(one digest *and*, where carried, one inode each since 09:57Z); `config.toml`
is the only path with two distinct digests, and the second appears exactly at
the r3 pre capture. Reference receipts' own identity re-derived before use:
r2 `EX-31/capture-pre.txt 3f3db73e…` / `capture-post.txt c0674f99…`,
`c3/receipts/config-pre-pair-v2.txt fa9706c6…` — each equals its `.sha256`
sidecar. (The r1 `-metadata.txt` "ctime(UTC)" columns are again the local `-03`
renders — the known v1 label defect, epochs unaffected.)

### 3b. solc-prefix reuse did not touch any custody path (task item 2)

- Prefix tree is untouched since install: `package.json`/`package-lock.json`
  mtime+ctime `2026-10-19 06:57:25 -03` (= 09:57:25Z), `node_modules/` 06:57 —
  i.e. **before every round-3 write**, so the reuse read the tree, never wrote it.
- All five custody ctimes are ≤ `2026-10-19T12:57:45Z`, which is *before* round-3
  start (freeze dir 13:03Z; EX-29 pre-capture 13:06:57Z). ctime cannot be set
  backwards, so **no round-3 process (solc, npx probe, seat, or tool) wrote,
  chmod'd, renamed, or replaced any custody path**. Two captures 10 s apart plus
  the tool's live verify agree; the watcher log continues this across the window.
- r1's installer-seat pair (`EX-02/custody-pre-pair.txt` vs `-post-pair.txt`)
  is EMPTY-diff 5/5 per that receipt — the install itself did not touch custody
  either; that claim re-holds against the live tree for the 4 stable paths.
- The only custody move found this round is **pre-round and not solc-attributable**:
  `config.toml` at 12:57:45Z — after r2's last custody capture (12:31:44Z) and
  r2's landing writes (`LOG.md` 13:00:59Z, `SCORECARD.md`/r2 report 13:01:44Z),
  i.e. the kimi-code harness's own config at a wave boundary (its `file-history/`
  index moved 13:03Z). No content was read (custody rule); attribution is
  timing-based (see A6).
- Neighborhood check: the parent dirs of the 4 stable paths show no post-capture
  directory writes (`~/.config/devin` dir mtime 06:50 local, `~/.omp/agent`
  10:05 local = 13:05Z, both ≤ pre-capture; re-listed at close in §5).
- **Positive control for the whole method:** the directories the round's *actual*
  writers touched do move in stat terms — `~/.npm/_npx` dir mtime moved at
  13:06:01Z and again during the round (entries `9b980929…` 13:06, `ad9a3fdb…`
  13:09, `a1722018…` 13:13, `dea94757…` 13:15Z — the probe/`npx` runs). So a
  round-3 write *is* visible to this method where it happens; the custody paths'
  ctimes show none. (The npx cache is not a custody path — recorded, not a
  finding.)

### 3c. Compiler-check receipts (task item 3) — all re-derived

| receipt | claim | my re-derivation |
|---|---|---|
| r1 `EX-02/install-receipt.txt` | tarball sha256 `0e1a1ab6…575a51`, size 6476046, sha512 = registry integrity | npm-cache content file: sha256 **exact match**, size exact; base64 integrity decoded → `89e51874…` == the file's own sha512 (`sha512sum`) ✓ |
| same | prefix tree byte-identical to ambient install | `soljson.js 221d7a66…`, `solc.js 188c3fdc…` — identical in both trees ✓ |
| same | compiler string 0.8.37+commit.f401782d | `.bin/solcjs --version` → `0.8.37+commit.f401782d.Emscripten.clang`; `require(prefix/node_modules/solc).version()` → same ✓ |
| same | Smoke.bin 685 B `530efc7b…` | `sha256sum` exact, 1370 hex chars ✓ |
| `EX-04/evidence/toolchain.txt` | prefix `soljson.js 221d7a66…`; probe form `TMPDIR=/var/tmp/… npx -y rea-agents@6.4.0 …` | soljson hash matches my own; the disk-backed-TMPDIR probe form matches the r1 entry's recheck line ✓ |
| `EX-05/out/CarrierB.report.json` | compilerVersion `0.8.37+commit.f401782d.Emscripten.clang`; source `289bc599…`; solc-input `d48cd7aa…`; runtime `b9c70178…` (1469 B); creation `6794c3a2…` (1560 B); 4 output files' sha256s | every hash recomputed from the bytes: **all 8 exact** ✓ |
| `EX-10/planted-K.json` + opt200 runtime | K=13 planted selectors | recomputed independently with the prefix's `js-sha3` (not EX-10's keccak.py): **13/13 present**, 0 missing, 0 selector mismatches ✓ |
| `EX-01/compiler-check.txt` (the round's reuse-verification receipt) | prefix tree unchanged since install (`find -newermt '06:58'` → 0); `package.json b4205b08…`, `package-lock.json 9f6dcab2…`, `node_modules/solc/package.json b3a90035…`; whole tree 8/8 identical vs cache tarballs; embedded wasm core `df14c4e5…` (22,012,583 B) | I re-ran their own scripts from copies in `/var/tmp` with my scratch: `attest-prefix-vs-cache.py` → `identical=8 differ/missing=0 skipped=0` exit 0; `capture-embedded-wasm.js` → 22,012,583 B, sha256 **`df14c4e5…afca1e` exact**, `solidity_version()` = receipted string, and the ambient tree's core is **byte-identical** to the prefix's; three package hashes re-derived exact; `find -newermt` → 0 ✓ |
| `EX-04/evidence/compile-receipt.txt` (carrier-B compile legs) | opt200 runtime 1850 B `aaf85cea…`; noopt runtime 3872 B `679678e9…`; opt200 creation 2237 B `8466da5f…`; noopt creation 5276 B `45a6d3d7…`; abi `2be500d7…` both legs; source `carrierB.sol 14566042…` | every artifact hash + byte length recomputed from the files: **all exact** ✓ |

No receipt was found that misstates its own bytes; the round's reuse receipt
(EX-01) survived two independent re-runs of its own tooling. (Proof that C1's
"reuse, no install" claim is true of the *tree* as well: `find … -newermt`
0 files, tree hash-stable since 09:57:25Z.)

### 3d. Tool-level corroboration (C2's custody-safety claims, re-run by me)

At rev `ec2b2d48` (battery `write-guard-attack-rev2.out`), with fake `HOME`:
`capture --out <custody path>` → `USAGE` exit 2, target sha unchanged; VZ-4
replay `--paths X --out X` → `USAGE` exit 2, X unchanged; scoped-custody
variant → refused, unchanged; control capture → exit 0 with the scoped source
unchanged; 1-of-5 receipt `verify --live` → MATCH exit 0, and with
`--require-paths 5` → `USAGE: reference covers 1 of the required 5 paths`,
exit 2 (declared class). Tool identity stable across each run
(`TOOL-SHA-BEFORE == AFTER`).

## 4. Attacks / refutations attempted (with verdicts)

| # | attack / question | result | verdict |
|---|---|---|---|
| A1 | Is my "agreement" with EX-29 just the same tool twice? | my capture uses coreutils+openssl+hashlib and GNU stat; the grader is mine and parses the receipt text | **refuted** — independent agreement 80/80 |
| A2 | Could a round-3 process have written a custody path and hidden it (mtime restore)? | ctime cannot be backdated; all 5 ctimes ≤ 12:57:45Z < round start; two captures + tool verify + ongoing watcher | **refuted** |
| A3 | Did the solc-prefix reuse touch custody (npx/solc writing under `$HOME`)? | prefix tree mtimes = 09:57:25Z install; custody ctimes older; no custody-path writes in any capture | **refuted** |
| A4 | Does the write-guard still clobber (`--paths X --out X`, VZ-4)? | at `08fb6833` and `ec2b2d48`: refused, USAGE exit 2, file byte-unchanged (guard scope = CUSTODY_PATHS ∪ paths) | **closed** at those revisions |
| A5 | Is `--require-paths` actually reachable from the CLI (D3)? | at `08fb6833`: **not registered** → `unrecognized arguments`, exit 2, while the code path already existed (1-of-5 still read exit 0); at `ec2b2d48`+: registered and returns the declared `USAGE`/exit 2 | **mid-flight — must be re-checked at landing** (N1) |
| A6 | Is the `config.toml` move attributable to the round's tooling? | move at 12:57:45Z precedes round start 13:03Z and the pre-capture; r2 landing writes bracket it; no round-3 read/write can move ctime backwards | **not round-3**; writer = harness-level (timing only; no content read) |
| A7 | Is the standing "`/tmp` EDQUOT" premise still true? | `dd bs=1M count=50 of=/tmp/…` succeeded (50 MiB, 9 GB/s) at 13:08Z; only scratch discipline kept me off `/tmp` | **refuted — rule text is stale this round** |
| A8 | Do v1 receipts still verify (C2 clause)? | r1 stanza/pipe receipts' digests vs live: 4/5 match; `config.toml` CONTENT-DRIFT (the pre-round move) → the clause holds only with that drift recorded | **holds with the named drift** |
| A9 | Were the r1 cross receipts retro-edited since r2? | `config-pre-pair.txt b8ed1936…`, `-metadata.txt 85fa1860…` — both equal r2 CU-1's claimed digests | **refuted** (bytes stable) |

## 5. Blockers

1. **POST pair not landed at last poll** (13:11Z; EX-29's post capture absent from
   `claims/c2/receipts/`; `seats/` held EX-04, EX-22). My pre-side corroboration
   stands; the round's live pre/post MATCH 5/5 claim must be verified by the
   parent (or a later seat) against the landed post receipt with:
   `python3 .ufo/waves/arc3-loop1-round3/claims/cross/CU-1/grade-custody.py grade-live <post-receipt>`
   and `… grade-custody.py diff .ufo/waves/arc3-loop1-round3/claims/c2/receipts/config-pre-pair-v2r3.txt <post-receipt>`
   (expect `NO-MOVED-FIELDS` while no writer touches custody; `config.toml` moves
   only if the harness rewrites its own config again).
2. **The C2 target is a moving instrument** (six revisions during my run). Every
   check of mine above is revision-stamped; the landed revision must re-pass
   §3d and the selftest floor, and the README must document the flags (N1).
3. **`config.toml` carries a pre-round move** (12:57:45Z) that the round's
   "v1 receipts remain verifiable" and "MATCH 5/5" clauses must state as the
   round's baseline — do not compare r3 receipts against r1/r2 receipts without
   this one-path carve-out.
4. Watcher `watch-log.txt` runs 30 × 60 s from 13:09:56Z; it writes only this
   seat's artifact dir and stops by itself. If the wave runs past ~13:40Z the
   log will be short of the close — re-run `bash …/claims/cross/CU-1/watch.sh`
   or the one-shot `capture.sh post` as the authoritative post capture.