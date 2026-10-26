# R39Sentinel — round-start seam check (round 39, wave 1, pre-freeze)

**VERDICT: DEFECTS FOUND** — the five seam items are clean (no stray fleet-root writes, no secrets, no
config drift, no kaidoku leftovers), but the pre-freeze build has **two freeze-blocking tool-provenance
defects** (`tools/round-37/gen-squashfs.py` cannot reproduce the K5 carrier and cannot produce a usable
xz image), one vacuous peer 6.5-vs-6.7 comparison, and four low/ informational items.

Seat: `R39Sentinel` (leaf, sentinel remit: trust boundaries and failure modes from local evidence).
Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `a2f64e1d`, no VCS mutation, nothing
written outside `.ufo/waves/round-39/w1/artifacts/R39Sentinel/` and this report file.

---

## 1. Seam check — results

### (1) Fleet root untracked files naming kaidoku / round-38 / round-39 — ZERO

```
$ git -C /home/vgpnk/Projects/shokunin status --porcelain --untracked-files=all | wc -l
0
$ git -C /home/vgpnk/Projects/shokunin rev-parse --short HEAD
c2ac029a   (2026-10-26 13:03:18 -0300 "hyaku run 9: dispatcher saves .partial…")
$ git -C /home/vgpnk/Projects/shokunin status --ignored --porcelain | wc -l
120          # all ignored entries: .jj/ .tower/ .ufo/state/* — none created this wave, none named kaidoku
```
No untracked fleet-root file exists, so per the instruction there is nothing to list. Nothing touched.

### (2) Leftover scratch — one stale `/tmp` file, no stale kaidoku scratch

- `/fast/scratch/hyaku/kaidoku-r39/` — 16 seat dirs, all created 13:38–13:41 (this wave, live peers);
  `ls -d /fast/scratch/hyaku/kaidoku-r3*` returns **only** `kaidoku-r39`: no round-36/37/38 leftovers.
- Non-kaidoku siblings present in `/fast/scratch/hyaku` (other lanes, untouched): `kengaku-r40`,
  `mado-r44`, `souji-r31`, `souji-r33`, `tabi-r32`, `tameshi-r48`, `tsukuroi-r41`, `kasegi-r36` (empty).
- `/tmp/kaidoku-r39-census-start.txt` — 1205 B, mtime **2026-10-26 13:07:01** (L1 census, before
  wave-1 spawn at 13:38). First line: `kaidoku W04 S033 duplicate url
  github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes`; last line
  `kaidoku ok /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md`. Harmless (<50 MB, no
  secrets); it is not an evidence path. **Left in place** (not mine; owner = L1).
- `/tmp` total entries 237; the only kaidoku/squashfs-named one is the file above.

### (3) Lane status and ignored large files — expected only

```
$ git -C …/kaidoku-shokunin status --porcelain
?? .ufo/waves/round-39/
?? plans/round-39-claims.md
$ git -C …/kaidoku-shokunin status --ignored --porcelain
!! .jj/                                       25M
!! .ufo/waves/round-34/r34b/w1/CtlMultiset-files/__pycache__/   12K
!! .ufo/waves/round-39/w1/artifacts/R39C2TableDraft/__pycache__/  (new this wave)
!! tools/round-3{4,5,6,7,8}/__pycache__/       12K/36K/60K/new/84K
```
No ignored file >100 MB; the only large ignored tree is the jj store `.jj` (25 M). `.ufo` total 357 M
(tracked history). No untracked file outside `.ufo/waves/round-39/` and the claims draft.
Note: `tools/round-37/__pycache__/gen-squashfs.cpython-314.pyc` (16 317 B, 13:41) is **new this wave**
and is a *side effect of a seat importing the writer by path* (see F3) — the only lane write observed
outside a seat's own artifacts dir.

### (4) Secrets scan of `round-38/` — ZERO (two pattern-catalogue false positives)

Scope: 960 files / 8.3 MB, whole tree, plus keyword and entropy passes.

```
$ grep -rIl -E 'sk-(ant|proj|live|test)|ghp_[A-Za-z0-9]{20,}|BEGIN [A-Z ]*PRIVATE KEY|op://[A-Za-z0-9]|AKIA[0-9A-Z]{16}|xox[bap]-' .
./r38-w2-results.json          ← 2 hits, both inside ONE quoted string
$ grep -o -E … r38-w2-results.json | sort -u
BEGIN PRIVATE KEY
op:///xox
```
Context (character-exact): `"3_secrets": "ZERO. sk-/ghp_/gho_/AKIA/BEGIN PRIVATE KEY/op:///xox[baprs]-/Bearer/password
over w1 (41 reports + all artifacts), w2, and every committed round-38 path …"` — i.e. the round-38
sentinel's own **list of patterns it searched for**. False positive, not credential material.

Broader passes, all negative for values:
- keyword grep (`token|password|secret|api[_-]key|Authorization`) → 11 files, every hit a scan
  description, a regex literal (`BEGIN [A-Z ]*PRIVATE KEY|authorization[: ]|api[_-]?key|secret[_-]?token|password\s*=`
  in `R38ReviewerEntryQuality/check-entry.py`), or a 429 body quoting `semanticscholar.org/product/api#api-key-form`.
- extended patterns `_authToken | //registry.npmjs.org/:_auth | BEGIN OPENSSH | ssh-rsa AAAA | glpat- | AIza…`
  → 0 hits.
- entropy pass (2872 base64-ish runs ≥40 chars): all accounted for — 93-char sha512 SRI values in
  `R38ExecMirrorGate/mirror-SOURCES.md`, base64 of the unblob log text
  (`U3F1YXNoRlMgdmVyc2lvbiBbMTAyNC4wXSAvIGlub2RlIGNvdW50…` = "SquashFS version [1024.0] / inode count…")
  in the AVM probe envelopes, and GitHub commit paths. No bearer/basic credential, no private key body.
- round-39 wave dir (`34 files`) and my scratch: same pattern set → 0 hits.
- permissions: no world-writable **regular** files in round-38 or round-39; dirs 755. `~/.tripo/config.json`
  is 600 (the mcp.json entry reads it through `!jq` at spawn, so the key is not stored in mcp.json).

### (5) `~/.omp/agent/mcp.json` / `config.yml` — unchanged through round 39

```
$ stat -c '%n %y %s' ~/.omp/agent/mcp.json ~/.omp/agent/config.yml
/home/vgpnk/.omp/agent/mcp.json   2026-10-25 02:32:37  2497
/home/vgpnk/.omp/agent/config.yml 2026-10-26 00:50:56 15135
```
Both predate the wave-1 spawn (13:38) and the round start (13:03); nothing changed during round 39, no
kaidoku/round-3x/rea reference in `config.yml`. Trust-boundary relevant: `mcpServers.rea` is
`npx -y rea-agents@6.7.0 mcp` but sits in `disabledServers: ["rea"]` — the MCP REA route (6.7.0) is
**not mounted** for this session (no `xd://mcp__rea_*` device exists), so the CLI-only rule and the
6.5.0 pin are structurally enforced. Ambient: two `npm exec rea-agents@6.7.0 mcp` processes are alive
from *other* project cwds (F7).

---

## 2. Findings

Severities: HIGH = breaks or falsifies a frozen claim's provenance; MED = a peer conclusion or a freeze
field is unsupportable as written; LOW = hygiene/precision; INFO = defended hazard.

### F1 — HIGH — the frozen K5 carrier is not reproducible from the lane's tools (UTF-8 `name_size`)

Exploit path (provenance, not privilege): the freeze records K5 `carrier.sqsh` (pin `5999eafc…`) as a
standard-BE v4 image built by `tools/round-37/gen-squashfs.py`; a later reader rebuilds K5 from the
committed tree with that tool and gets **different bytes that no extractor can read**, so the pin cannot
be derived from the frozen pipeline, and the discrepancy is invisible unless someone actually rebuilds.

Evidence:
```
$ diff -u tools/round-37/gen-squashfs.py .ufo/…/R39C1CarrierK5/gen-squashfs.py
-  pack(e,'H',typ) + pack(e,'H', len(name) - 1)); tbl += entry + name.encode()
+  nb = name.encode(); … pack(e,'H', len(nb) - 1)); tbl += entry + nb
```
`name_size` was a **character** count while the bytes written are UTF-8, so any directory holding a
non-ASCII name is parsed past its end. Empirical, same tree (`R39C1CarrierK5/src`), same arguments
`--endian be --comp gzip`:
```
patched copy 5999eafc0fb6a8bc3cd8a363d14f4c3f0ffe00e947e155cf8f1bb3278d00b228  (== committed carrier)
stock        7bd4a42d90331dbdc02705bf89123fdb2d02f4028368c03ff8108212737c584d
$ sasquatch-v4be -be -ls <stock rebuild>     # exit 1
File system corrupted: invalid characters in name
FATAL ERROR: dir_scan: failed to read directory squashfs-root/usr/share/demo/assets/icons
$ sasquatch-v4be -be -ls <patched rebuild>   # exit 0, full listing
```
Scope of exposure measured: non-ASCII paths per carrier — K1 **0**, K2 **0**, K3 **0**, K4 **0**, K5 **1**
(`usr/share/demo/assets/icons/アイコン.txt`), K6 **0**. Round-37 pins are therefore unaffected (verified,
§3), and C2's held-out trees are currently ASCII-only (`ALPHABET = 'a-z0-9_-'`), so the bug does not bite
C2 today — it bites K5 and any future unicode carrier.

Impact: K5's provenance depends on a writer that exists only inside `.ufo/…/R39C1CarrierK5/` (not a tool
path); `carriers.json` saying "built by tools/round-37/gen-squashfs.py" is false. Also a latent trap for
C1 coverage: a unicode path is exactly the kind of name a real BE image carries.

Smallest remediation (L1, `tools/` is out of my write scope): apply the two-line `len(nb)` fix to
`tools/round-37/gen-squashfs.py` (ASCII output is unchanged — proven: K1/K2 still rebuild to their pins),
record `writer_sha256` per carrier in `.ufo/waves/round-39/c1/carriers.json`, and re-pin K5 from the
fixed tool. Alternatively drop the unicode file from K5 — loses real coverage.

*Peer confirmation (13:52, found independently and now on disk):*
`R39C1CarrierK5/tool-versions.txt` records `gen-squashfs stock sha256: 1c7c5e88…` / `gen-squashfs local
sha256: 833a40a9…` / `carrier sha256: 5999eafc…` — the same three numbers I measured, and the same
`7bd4a42d…` divergence for the stock rebuild. Its `oracle-from-image.tsv` / `symlinks-from-image.tsv` are
byte-identical to the frozen `oracle.tsv` (`651cb7e3…`) and `symlinks.tsv` (`9d7c1b6a…`), so the fixture's
oracle is now verified from both directions (tree-derived by the seat, image-derived by the seat, and
image-extracted independently by me). Remaining gap is unchanged and still L1's: the frozen *tool* must be
able to rebuild K5, not just the seat's artifact copy.

### F2 — HIGH — the stock writer's xz path produces an image no reader can decompress; K6's "xz" carrier exercises no xz

Evidence (compressible xz tree: 20 000×`A` + 16 000 B text, `--endian be --comp xz`):
```
$ sasquatch-v4be -be -d x_tz tz_stock.sqsh     # exit 1
Trying to decompress using default lzma decompressor… with xz… with zstd… lzma-adaptive… lzma-alt… lzma-ddwrt…
FATAL ERROR: writer: failed to read/uncompress file x_tz_stock/mixed.txt
[extracted] 0 mixed.txt   0 repeat.txt        (both files 0 bytes)
```
Two independent writer defects behind it, both visible in the source: `comp_bytes('xz')` uses
`lzma.FORMAT_RAW` (bare LZMA2, no `.xz` container) and the superblock writes `COMP['xz'] == 2`, which in
the SquashFS spec is **LZMA** (xz is 4). Same result with the K5-patched copy, so it is a stock defect,
not K5's.

K6 consequence: K6 (`carrier.sqsh` `df85c10b…`, superblock `comp_id 2`, 14 925 B) was built with
`--comp xz` and yet extracts cleanly with all 7 oracle rows matching — therefore **[INFERENCE]** every
one of its data blocks is stored uncompressed (its only >4 KiB file is `random.Random(39)` noise, which
xz cannot compress, so the writer's uncompressed flag is set), i.e. K6 decodes no xz block at all and its
"xz" description overstates what the carrier tests. Confirmed side-note: rebuilding K6's committed `src`
with the stock writer reproduces `df85c10b…` exactly.

Why it matters for the claims: R39-C1's predicate only needs file publication, so K6 passes — but the
freeze text should not call K6 an xz carrier, and R39-C2 must not assume "xz compresses" for its
`body-extractor-failure` class. C2's heldout-gen already replaces the encoder (`FORMAT_XZ`,
`CHECK_CRC32`); I verified that variant works: a `FORMAT_XZ` image with the same compressible tree
extracts fully with sasquatch (exit 0, 20 000/16 000 bytes). It still writes `comp_id 2`, though —
sasquatch survives only by brute-forcing decompressors; if unblob dispatches on the id, the xz arm's
label may differ from what sasquatch shows. **[INFERENCE]** — needs one dev-carrier REA run before the
freeze (not run here; my item forbids the held-out runs, not the dev ones, but that check belongs to the
C2 seat).

Smallest remediation: in the frozen writer set `COMP = {'gzip': 1, 'xz': 4}` and emit `FORMAT_XZ`; if
that is too large a change at freeze time, keep K6 gzip and state the xz limitation in the SKILL craft
row instead of shipping a mislabelled carrier.

*Peer follow-up (13:47, `R39C2HeldoutGen`, peer-reported, unverified by me):* confirms `COMP xz->2` is a
real defect, is patching `module.COMP` alongside `comp_bytes` and re-running its dev pipeline so frozen
images declare `comp_id 4`; it withdrew the mid-edit caveat (build_tree complete, 16 carriers verified
against sasquatch) and will put `sys.dont_write_bytecode = True` before the loader call and a
`block_encoder` marker in the manifest. Consequence to check after the patch: with `comp_id 4` the xz
carriers' bytes change, so every xz-arm label must be re-measured (sasquatch brute-forced the decompressor;
unblob may dispatch on the id) — a carrier that sasquatch reads can still be a `body-extractor-failure`
envelope, and the triage table must reflect what the extractor actually did.

*Second follow-up (13:49, peer-reported, unverified by me):* the peer states the final dev run regenerates
all 16 carriers with `comp_id 4` (checked per superblock, `file` now says xz rather than LZMA) and re-runs
REA on every carrier, so xz-arm labels are re-measured rather than inherited; it will state the
comp_id/unblob asymmetry explicitly if the xz arms come back with their intended classes. I cannot verify
that from here (my seat runs no REA and must not touch held-out generation); what an auditor should check
at the freeze is the manifest's per-carrier `comp_id` + `block_encoder` + writer hash, not the narrative.

### F3 — MEDIUM — heldout-gen's writer identity is not the code that produced the bytes (and it writes into `tools/`)

- `heldout-gen.py` (snapshot 13:44, 22 142 B) loads `tools/round-37/gen-squashfs.py` by path and
  monkeypatches `module.comp_bytes`; `writer_sha256(path)` hashes the **stock file**, so the manifest's
  writer fingerprint does not identify the encoder that actually ran. Freeze consequence: an auditor
  cannot reconstruct held-out bytes from "writer sha256" alone; record the patch (comp_bytes replacement,
  `FORMAT_XZ/CRC32` vs `FORMAT_RAW`) and both hashes, or better, freeze the encoder into the tool file.
- Loading the writer by path wrote `tools/round-37/__pycache__/gen-squashfs.cpython-314.pyc` (13:41) —
  a seat-side write into the lane's `tools/` tree (gitignored, no tracked change, current version not a
  shadow risk). Smallest fix: `sys.dont_write_bytecode = True` at the top of the script, so a run without
  `-B` cannot do it.
- Snapshot caveat, not counted as a defect: at 13:44 `build_tree()` still contained `for kind in
  rng_kinds:` before `rng_kinds()` is defined and never created the `symlinks` list, i.e. the file was
  mid-edit; I assume the peer finished it.

### F4 — LOW — a peer passes the 6.5.0 root as `--pkg67`; the vacuity is declared, so no conclusion is affected

Captured process at 13:41 (peer scratch, gone by 13:43):
```
node …/tools/round-27/xpin-attribute.mjs --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents \
                                         --pkg67 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents k1.json
```
Both pins are the same root, and that root is **6.5.0**:
```
6.5.0  ~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json
6.4.0  ~/.npm/_npx/dea9475797100b20/node_modules/rea-agents/package.json
(5 other _npx/*/node_modules/rea-agents dirs have no package.json; a grep for "6.7.0" under ~/.npm/_npx finds nothing)
```
`xpin-attribute.mjs` imports `digestCanonicalValue` and the `semanticProjection` source from each root, so
the second column is the 6.5.0 rule computed twice. **Verified resolution (peer claim checked against its
artifacts, 13:55):** the vacuity is disclosed in the evidence header itself —
`evidence/xpin-verdicts.txt:2` reads `# columns: path, stored id, id@6.5.0, id@6.7.0-root(=6.5.0), verdict`
— and the seat's report cites only the 6.5.0 rule (`xpin-attribute.mjs (6.5.0 rule)`), with no
6.5.0-vs-6.7.0 divergence anywhere in `R39C1Controls.md` or its evidence. Downgraded from MEDIUM to LOW on
that evidence: nothing downstream is misled today.

Residual risk, not a defect: the duplication is a property of the *invocation*, not the tool, so the same
pattern reused without the header line would silently produce a vacuous "6.7.0" column. **Resolved by the
peer (13:58, verified in its artifacts):** `_harness/apply_control.py:202-204` and
`_harness/fabricate_receipts.py:363-370` now print a startup note that xpin runs with
`--pkg67 = --pkg65` (no 6.7.0 root on this host) and a warning when `--pkg65`'s package.json version is not
6.5.0, and `README.md:24-25` records the same. My suggested `pkg65 != pkg67` assertion would have disabled
the harness (the tool requires both flags), so the disclosure-plus-version-check form is the correct reuse
guard; F4 is closed on that basis. Related ambient observation: the two live `npm exec rea-agents@6.7.0
mcp` processes (F7) suggest no 6.7.0 install has completed on this host.

### F5 — LOW — the frozen round-38 `carriers.json` mis-describes K2

`.ufo/waves/round-38/c1/carriers.json` says K2 is `synthetic standard-BE v4 gzip (tree2, symlink + unicode
name)`, but the frozen K2 tree contains **no** non-ASCII path: `oracle.tsv` has exactly `a/run.sh`,
`space name.txt`, `var/lib/data.bin`; `find K2 -print | LC_ALL=C grep -c '[^ -~]'` → 0; sasquatch lists
the same plus `a/b/c`, `var/lib/run-link` (symlink). K2's pin `403cb0a8…` rebuilds exactly from
`K2/src` with the stock writer. Impact: a reader who trusts the description would think K2 covers unicode
names (it does not — that gap is exactly why K5's tree breaks the stock writer). Remediation: correct the
note in the round-39 carrier record (round-38 is history; do not rewrite it).

### F6 — LOW — K6 ships no pin file while K5 does

`R39C1CarrierK5/build.sh` ends with `sha256sum carrier.sqsh | tee carrier.sqsh.sha256`; K6's ends with
`sha256sum "$OUT"` (stdout only). K6's `carrier.sqsh` `df85c10b…` therefore exists only in the seat's
report. Remediation: record it in `.ufo/waves/round-39/c1/carriers.json` at freeze (it must be there
anyway), optionally have K6's build.sh emit the `.sha256` like K5.

### F7 — LOW — two stale out-of-lane REA 6.7.0 MCP processes; one `/tmp` leftover

```
2244623  npm exec rea-agents@6.7.0 mcp   started 13:02:37  cwd /home/vgpnk/Projects
2282871  npm exec rea-agents@6.7.0 mcp   started 13:02:39  cwd /home/vgpnk/Projects/stakezico
         (both: REA_UNBLOB_COMMAND=/home/vgpnk/.local/bin/unblob, REA_PWNTOOLS_PYTHON=…/kaidoku-pwnenv/bin/python)
```
Alive ≥39 min at observation, neither owned by a kaidoku seat, no resolved 6.7.0 package on disk — most
likely stuck npm deliveries. No kaidoku evidence is touched by them, and kaidoku's `rea` MCP is disabled;
reporting because a stalled `npm exec` holds npm cache/install locks that a seat's `npx -y
rea-agents@6.5.0` could block on, and because a 6.7.0 MCP route existing anywhere invites a
version-mismatched run. Remediation: none available to me (not mine to kill, processes belong to other
cwd sessions); the operator should reap them if they persist.

### F8 — INFO — escaping-symlink fixtures resolve to host paths; guards verified

K5/K6 fixtures carry real escapes (`usr/share/demo/escape -> ../../../../etc/shadow`,
`data/escape-deep -> ../../../../etc/passwd`, root-level `outside -> ../outside`). POSIX resolution
re-checked by hand against the frozen `symlinks.tsv` classification: all three escape; `a/b/link-in ->
../../etc/config.ini` and `usr/share/demo/link-blob -> ../opt/blob.bin` / `link-notes -> notes.txt`
resolve in-tree and match oracle rows. A build step that followed those links (`cp -L`, `tar -h`,
`os.stat`, `getsize`, `os.walk(followlinks=True)`) would pull host `/etc/passwd` content into an oracle.
Current state is correct: the stock writer uses `os.walk(followlinks=False)` + `islink`/`readlink` only;
both oracle writers skip symlinks with `islink`; K6's build.sh additionally refuses an absolute target or
a symlink that resolves to a host *directory*. Confirmed clean: K6 `oracle.tsv` has 7 rows, exactly its 7
regular files, no `passwd`/`shadow` row. Residual gap: the guard does not cover an escape that resolves
to a host *file* — a one-line assertion (`assert all(rel in oracle_rows for ...)`, plus
`os.path.realpath(p).startswith(os.path.realpath(tree))` for every in-tree link) would close it without
touching the fixtures.

*Corroboration for the draft symlink rule (artifact content, not my run):*
`R39C1CarrierK5/dev-probe-unblob-traversal.log` holds
`2026-10-26 16:45.07 [error] Path traversal attempt through symlink, removing pid=998273 target=etc/shadow`
— unblob 26.6.4 detects the escape at extraction time and removes the link instead of reading it, which is
the escaping half of the draft rule (`MaliciousSymlinkRemoved`, no gap) observed rather than asserted. It
also shows what the guard is protecting: without it, an in-tree path would reach the host `/etc/shadow`.

### F9 — MEDIUM — P39-C2 does not pin the image writer it loads by path, so the F1/F2 fixes break its own byte-identity clause

The draft predicate says the held-out set is "generated by the frozen `tools/round-39/heldout-gen.py` with
seed = the freeze commit hash, every carrier regenerates byte-identically from that seed". But
`heldout-gen.py` does not own its writer: `default_writer_path()` resolves to
`tools/round-37/gen-squashfs.py`, the module is loaded from there at run time, and only `comp_bytes` is
monkeypatched. `tools/round-37/gen-squashfs.py` is named nowhere in the predicate, in `manifest.json`'s
identity fields as drafted, or in the C2 kill rule.

Failure path: the freeze integrates F1 (ASCII-neutral `name_size` fix — harmless) together with F2
(`COMP = {'gzip': 1, 'xz': 4}` *plus* `FORMAT_XZ`). Held-out-gen patches `comp_bytes` but not `COMP`, so
after such a change the same seed yields xz carriers whose superblocks differ from the ones recorded at
freeze: the predicate's own "regenerates byte-identically" clause fails and an honest C2 run is scored as a
miss. The reverse order is equally bad — freeze the current writer, patch it afterwards, and the frozen
record matches no run of the tool as it then exists. F1+F2 are exactly the two fixes I am asking L1 to make,
so this collision is not hypothetical.

Smallest remediation: pin the emitter, not only the generator — `manifest.generator.sha256`
(heldout-gen.py) **+** `writer.sha256` (the round-37 file as loaded) **+** a `block_encoder` marker naming
the correction; the peer proposed the same at 13:49 (peer-reported) and flagged it as L1's wording change
because seats cannot edit the claims file. A simpler alternative: copy the ~150-line writer into
`tools/round-39/` so held-out generation has no out-of-tree dependency at all.

---

## 3. Independent verification I ran (not delegated, not re-run from a report)

| Check | Result |
|---|---|
| generator determinism, 2 runs/mode 1 s apart (be/le/avm × gzip/xz) | identical bytes in all 5 modes (`generator-forensics.txt`) |
| K1 rebuild from committed `src`, stock writer | `1cfb6c33…` == pin ✓ |
| K2 rebuild from committed `src`, stock writer | `403cb0a8…` == pin ✓ |
| K5 extract (`sasquatch-v4be -be -d`), compare to `oracle.tsv` | 10/10 rows sha256+size, 0 extra regular files, 0 unexpected links ✓ |
| K5 oracle/symlink tables cross-derived from the built image (seat's `*-from-image.tsv`) | byte-identical to frozen `oracle.tsv` `651cb7e3…` and `symlinks.tsv` `9d7c1b6a…` ✓ |
| unblob 26.6.4 escape handling (seat's dev probe log) | `Path traversal attempt through symlink, removing … target=etc/shadow` — escaping link removed, not read ✓ |
| K6 extract, compare to `oracle.tsv` | 7/7 rows sha256+size ✓ |
| K6 rebuild from committed `src`, stock writer | `df85c10b…` == committed carrier ✓ |
| stock xz writer, compressible blocks | **unreadable** (F2) |
| `FORMAT_XZ` writer (heldout-gen's encoder), same tree | extracts cleanly, 20 000/16 000 B ✓ (still `comp_id 2`) |
| generator sources of nondeterminism (`getmtime`, `random`, `urandom`, `uuid`, `time()`) | none; `MKFS_TIME = 1700000000`, `UID = 1000`, sorted walk ✓ — so C2's "byte-identical from seed" is supportable **[INFERENCE, code-level]** |

---

## 4. Artifacts (all under `.ufo/waves/round-39/w1/artifacts/R39Sentinel/`)

| file | sha256 |
|---|---|
| `gen-squashfs-canonical-vs-K5copy.diff` | `ed6e362763a19737a68edbff054bd29df5eaa06f811d6c6452b0df3b2eeabd18` |
| `generator-forensics.txt` | `81c6c3c8bb64aca0a7646a346d065309898a9d799cd655a0bf4950ae1b1c0e39` |
| `hashes.txt` | `1f4e1af9b983546b367ef1b759d486ada7216fe028ed6e9501b103d5b9198150` |
| `sasquatch-canonical-build.err` (stock writer vs unicode tree) | `2de2c94c08e2ebbf26a9bb4fabbaf069e1c64680aae3dea750e937f8d677ed66` |
| `sasquatch-patched-build.err` (clean) | `bd5511b028eb4d0cc4d54a949bcbc7c8fa76ae3d3318833e6d34373995aa6ad2` |
| `sasquatch-stock-xz-extract.log` (FATAL) | `021749dfd5d736eb0ffc3a491836a26abe0f4edd5c0b860a594cd1587c2a1207` |
| `sasquatch-heldoutstyle-xz-extract.log` (clean) | `a1a654ebd6524e863dc460291e1dd3a3f3a998457436e4b5462d8701bf220d93` |
| `sasquatch-xz-block-forensics.txt` | `de0c2c0488d70a8754c24f1bee0da072092748982636193e18c1b7f1032082c9` |
| `sasquatch-K2.err` (K2 lists clean) | `86bc8173d57b8c31ae75009fcc49154bf789ebf519e53b1050a4451e8fc6b0b1` |
| `seam-commands.txt` (seam items 1/3/5 raw output) | `8cd7278a3f9fa90e71d2623a28e30797987a2b13008c98f3d7e2d09c36999212` |

Peer messages sent (coordination only): `KaidokuR39` (F1/F2 + remediation), `R39C1CarrierK5` (F1),
`R39C2HeldoutGen` (F2 comp_id + F3), `R39C1Controls` (F4).

## 5. Tooling record and bounds compliance

- **No tool installed, upgraded, moved or removed.** Used only what exists: `python3` 3.14,
  `sasquatch-v4be`/`sasquatch` 4.5.1 in `~/.local/bin` (read-only use), `git` (read-only verbs only),
  `df`, `lsof`, `pgrep`. No pacman, no `npx` run by me, **no REA invocation at all** (held-out and
  development both untouched — my item needs neither).
- No VCS mutation (no add/commit/checkout/reset/stash/pull/push, no jj), no writes outside
  `.ufo/waves/round-39/w1/artifacts/R39Sentinel/` + this report; scratch `/fast/scratch/hyaku/kaidoku-r39/R39Sentinel`
  created and **removed** at the end; nothing cited as evidence is left in scratch or `/tmp`.
- Read-only reads of `corpus/`, `tools/`, `plans/`, `.ufo/waves/round-38/`, `~/.npm`, `~/.omp/agent`
  did not modify them (K5/K6 carriers, oracles and both writers were copied into scratch before any
  rebuild).
- Out of scope, not judged here: the symlink rule itself (R39C1SymlinkK1K4 / R39SrcUnblobSymlink), the
  round-38 counter's logic (R39MutR38Counter), SKILL table content (R39C2 seats).

Report: .ufo/waves/round-39/w1/R39Sentinel.md
