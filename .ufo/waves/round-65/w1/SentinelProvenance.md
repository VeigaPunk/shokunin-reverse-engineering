# SentinelProvenance — provenance and safety audit of the R65-C1 closure (round 65, w1)

Seat: SentinelProvenance. Surface: the 30 closure entries the frozen `tools/round-65/jsc-closure-matrix.py`
(`sha256 79a4dca4…922c6`, re-hashed here — MATCH) pins, plus the pre-freeze cleanup and the "nothing ran
this round" clause. Read-only over the toolchain root; scratch
`/fast/scratch/hyaku/kaidoku-r65/SentinelProvenance` created and deleted; nothing written outside this
directory. Lane bounds respected: no subagent dispatch, no instrument run, no lane edit, no network.

Verdict line: **provenance-open: P1,P2,P3** (bytes stable and fully matched; origin of 9 binary entries and
the generation of the probe are not provable from bytes this host still holds). All 30 entries match; the
closure's *stability* claim is verified, its *origin* claim is not.

## 1. Independent closure recomputation (the primary check)

I parsed `CLOSURE` out of the frozen script with `ast.literal_eval` (no import, no execution) and re-hashed
every entry from disk, then the three aux pins. Result: **27/27 closure entries MATCH, 3/3 aux MATCH, 0
missing, 0 mismatch, 30 entries total** — equal to the instrument's own `entries` arithmetic
(`len(CLOSURE)+3`). `cache_entries()`-equivalent scan (`find … -name '__pycache__' -o -name '*.pyc'`) → **0**.

The frozen script hashes `d8`, `snapshot_blob.bin` and `icudtl.dat` for each build and self-reports the V8
version at run time; the three binaries self-report `V8 version 14.8.178.14`, `14.8.178.1`, `14.7.173`
(`d8 --version` writes nothing; run with `TMPDIR`/`HOME` in scratch), i.e. the version labels match the
directory names and the release tags. No binary contains a `jsc2js` marker string (`strings -a | grep -c
-i jsc2js` → 0 in all three), so "patched build" rests on the release index alone, not on an embedded mark.

## 2. Table

| artifact | sha256 | provenance class | verified this round? |
|---|---|---|---|
| `d8-14.8.178.14/d8` | `bc70d3c057c5468611400a9b93a339ca2751c570d64337a2075b0d6bef835331` | official jsc2js release asset; tarball `d8-14.8.178.14-linux.tar.gz` `9326e285…ee5f6` recorded in round 64 (`.ufo/waves/round-64/w1/ScoutJscRoute/findings.md`, tracked blob `58564087…`) | hash MATCH; **origin unprovable** — tarball absent (see P1) |
| `d8-14.8.178.14/snapshot_blob.bin` | `b5c418dc0c6006d8dc6f4ac9981182eecf783cd892ae4c4b4ba16977c17bf2bb` | same tarball | hash MATCH; origin unprovable |
| `d8-14.8.178.14/icudtl.dat` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` | **not shipped by the d8 tarballs**; claimed from `electron-v42.2.0-linux-x64.zip` `9caeeb15…84909` (r64 claims F6, r64 `SecDownloads/audit.md` row 8) | hash MATCH; **claim unprovable and not corroborable** — see P2 |
| `d8-14.8.178.1/d8` | `4060ff2ea9e0955dd1dee27e3b77b3013140368d370833e4a99184a1f1ae49b8` | official release asset; tarball `87a8afe9…bb6ea3` (r64 scout) | hash MATCH; origin unprovable |
| `d8-14.8.178.1/snapshot_blob.bin` | `601efdc639d9f439cca3d1274e0917ab28ee09d6870787d6052d8949fa73e24d` | same tarball | hash MATCH; origin unprovable |
| `d8-14.8.178.1/icudtl.dat` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` | as above (byte-identical across all three builds) | hash MATCH; claim unprovable |
| `d8-14.7.173/d8` | `c240ffaef3b9022a44f36e35c124400c225906e5e9dd6f373b4323ba62bcdcf2` | official release asset; tarball `fe518883…0738de` (r64 scout) | hash MATCH; origin unprovable |
| `d8-14.7.173/snapshot_blob.bin` | `80590f459ddbac237de5f282196b2c551e24982f31150cb8998a3b4898ea2720` | same tarball | hash MATCH; origin unprovable |
| `d8-14.7.173/icudtl.dat` | `c5da2fc389d1bb0ecb13fe22a8e069b7abc491f8aa5d16eb65d4ff32c85a46b6` | as above | hash MATCH; claim unprovable |
| 12 × `jsc2js-src/View8/**` | e.g. `view8.py b3123e4a…971918c`, `translate.py 0e075893…ff9f78` | source at pinned commit; I hashed `git cat-file blob 01fc264d:<path>` for all 12 | **fully verified** — all 12 blob sha256 == CLOSURE; tree object `c125db10c7ce6f9cfc48a0cf80def3dc23b378bf` == r64 F6 |
| `venv/lib/…/parse/__init__.py` | `27ddec2f…6ba8c0` | PyPI wheel `parse-1.22.4-py2.py3-none-any.whl`, fetched by uv 2026-11-03 19:36:33 | hash MATCH; RECORD self-check 8/8 clean; wheel identity only in uv cache (P3) |
| `parse/__init__.pyi` | `0ada9b91…c0d4f00` | same wheel | hash MATCH |
| `parse-1.22.4.dist-info/METADATA` | `e4179e24374e7084ebe589092e44bf2c8aa03cfec9756a56fcaa98a056bb232c` | same wheel (`Version: 1.22.4`, `Metadata-Version: 2.4`) | hash MATCH |
| `parse-1.22.4.dist-info/RECORD` | `58aa77c758d4c307da016a6e4db5011d7069bfa1053c836235cce94e7b2bd8c6` | same wheel | hash MATCH; all 8 RECORD digests recomputed, 0 bad |
| `venv/pyvenv.cfg` | `87a6b46ee1f9261cabbe8efb4b60639c50dfc14d77157fd670390e411152f335` | uv 0.13.0-created venv, `include-system-site-packages = false`, base `/home/vgpnk/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu` | hash MATCH |
| `inputs/atom.compiled.dist.jsc` | `6a0cb7b32270498ed190c589ca29c990a0e4b5f06f0cd6a5516e19a715c2dfe9` | **re-derived this round** from live `/usr/share/typora/resources/app.asar` member `atom.compiled.dist.jsc` (typora 1.14.9-2, 390514 B asar) | **fully verified** — extracted bytes byte-equal, and the asar's own `integrity.hash` is `6a0cb7b3…c2dfe9` |
| `probe-electron.jsc` | `a86f6ea04b95c9796b87b24aa8a414aba97b4468a6c39bb2298310e28fd1d710` | generated locally by `tools/round-64/mkcache.js` `f052eafb…66ff11` (tracked, MATCH) under Electron 42.2.0 / v8 `14.8.178.14-electron.0` (r64 F4); the `.jsc` itself is git-tracked (472 B; `git cat-file blob HEAD:…` → sha256 `a86f6ea0…`, blob `c089eec9…`) | bytes MATCH and git-pinned; **generation not reproducible** — Electron 42.2.0 absent from host |
| node | `7fde7b8afa198da66257f42ee2001d874c7355631e6d1579a5fb5ef1f246df4c` | fnm-managed `v24.21.0`, `~/.local/share/fnm/node-versions/v24.21.0/installation/bin/node` (PATH reaches it via `/run/user/1000/fnm_multishells/…` → same file) | version + hash MATCH; no upstream digest held (P1 class) |
| venv interpreter | `aac3ade3f7d90fbf63e3ea0c46120a0cfbd159e1e503dde04721979507a1548b` | uv-managed CPython `3.15.0`, `~/.local/share/uv/python/cpython-3.15.0-linux-x86_64-gnu/bin/python3.15` | version + hash MATCH; no upstream digest held (P1 class) |

Auxiliary bytes examined (not closure members):

| artifact | sha256 | note |
|---|---|---|
| held `electron-v40.10.2-linux-x64.zip` | `0246201400600ac089c51a36f15a8045b5db723ba42b864f732a9b4e48731e97` | the **only** Electron zip on the host; not the `9caeeb15…` asset r64 cites |
| its `icudtl.dat` | `1cf67874b5a87a8363a86fb3f81e3cbbed54d389062dab8fb52308d5cf8c8612` | **differs** from the installed `c5da2fc3…` — icudtl is version-specific, so the held zip cannot corroborate the pin |
| `parse` wheel (from uv cache record) | `ae430a4477316eed4a9710f642b2db968ec89d5d82e6b0908b8169673b476847` | URL `https://files.pythonhosted.org/packages/8f/5f/fbe0…2833/parse-1.22.4-py2.py3-none-any.whl`, ETag `84e98b18…`; body not retained, digest not in any lane receipt |
| `tools/round-65/coverage-recipe.py` | `9434888e1bfa283f2980fb3c550b9e15409c88855ee94c944e8472fcf83995a6` | frozen bytes match the assignment pin |

## 3. Pre-freeze cleanup (item 3)

`precache-dirs.txt` (173 B, mtime 20:11:33) records exactly four directories:
`jsc2js-src/View8/{Parser,Simplify,Translate}/__pycache__` and
`venv/lib/python3.15/site-packages/parse/__pycache__`; the README states the removal command
(`find . -name '__pycache__' -type d -prune -exec rm -rf {} +`), the pre-removal `*.pyc` count `15` (the 15
filenames were printed but **not** retained — stated as a limit), and the post-removal count `0`.
Independent check now: `find /home/vgpnk/.local/share/kaidoku-jsc \( -name '__pycache__' -o -name '*.pyc' \) | wc -l`
→ **0**. Directory mtimes corroborate the cleanup: `View8/{Parser,Simplify,Translate}` and
`site-packages/parse` all carry mtime 20:11, the payload files carry 19:36 — i.e. only the `__pycache__`
removal touched those directories. Cleanup receipt and independent state agree.

## 4. Did anything download or install for this round? (item 4)

- `git -C <lane> log --oneline c99e907c…HEAD` → exactly two commits, both round-65: `4a699a3f` (declaration,
  20:24:25) and `922ed89f` (operative freeze, 20:24:54). Nothing after the freeze.
- Toolchain root: **0 files** newer than 2026-11-03 20:12 (`find … -newermt '2026-11-03 20:12' | wc -l` → 0).
  All 124 files with a 2026-11-03 mtime are 19:35–19:39 (materialization) or 20:11 (cache removal).
  Payload mtimes are preserved from the archives (`Aug 11 11:54` for d8/snapshot, `Jan 1 1980` for
  `icudtl.dat` — a tarball-normalized mtime), so the binaries were unpacked/copied, not rebuilt.
- `inputs/` mtimes: single file, `atom.compiled.dist.jsc` 19:39:26, 388080 B — before the freeze.
- **Correction to the clause as worded:** *something* did run during prep, before the freeze —
  (a) `jsc2js-src` is a fresh clone at 19:36:29 (`logs/HEAD`: `clone: from https://github.com/xqy2006/jsc2js`,
  identity `probe <probe@example.invalid>`, checked out at `01fc264d…`), and
  (b) uv fetched and installed `parse 1.22.4` at 19:36:33 (`~/.cache/uv/simple-v26/pypi/parse.rkyv`,
  `wheels-v7/pypi/parse/1.22.4-py2.py3-none-any.http`, `archive-v0/G_wqzaf5x7m2WqBN/`).
  Both are prep-time, pre-freeze, and both are the ordinary way that tree is built. What is true and
  checkable is narrower: **no download, install or rebuild happened after the freeze**, and no d8 asset was
  fetched this round (no tarball anywhere: `find /fast /home/vgpnk -maxdepth 6/7 -name 'd8-1*-linux.tar.gz'`
  and `-name 'electron-v42*'` → empty).
- Out-of-scope noise, recorded so nobody misreads it: `~/.cache/uv/interpreter-v4/…/d0222a08….msgpack`
  written 20:27:47 (after the freeze) and `markdown-it-py`/`mdurl` index entries at 20:18:56 — other seats'
  uv activity **outside** the audited root; no effect on the toolchain census.

## 5. Secrets and permissions (item 5)

No secret material found: `grep -rIl` for `ghp_…`, `AKIA…`, `BEGIN {RSA,OPENSSH,EC} PRIVATE KEY`,
`aws_secret_access_key` over the toolchain root and `.ufo/waves/round-65` → no files. No `.pem/.key/id_*/.netrc/.env`
by name. No setuid/setgid files; every file in the tree is owned by `vgpnk`; no `sitecustomize.py`,
`usercustomize.py` or `*.pth` in the venv; no `pip`/`uv` entry points in `venv/bin`; site-packages holds only
`parse` and `parse-1.22.4.dist-info`. One mode exception: `venv/.lock` is `0666` (P5). The cloned source repo
carries `build_versions_batch*.py` / `determine_versions.py` that would fetch from the network — they are
present but nothing in the closure executes them (the instrument runs `d8`, `view8.py` and a `parse` import).

## 6. Risk list

- **P1 — origin of the nine binary entries is unprovable (medium).** The closure pins sha256 of 3 `d8`, 3
  `snapshot_blob.bin` and 3 `icudtl.dat`; the tarballs they came from are gone from the host (toolchain tree,
  `~/.cache`, `/fast/scratch`, btrfs `/home/.snapshots` is empty). The only link to upstream is the round-64
  scout record (tarball digests `9326e285…`, `87a8afe9…`, `fe518883…`, then checked against the GitHub API and
  against lead-scratch copies that no longer exist) plus the binaries' self-reported V8 version. Consequence
  for the claim: R65-C1's clause (i) proves the tree is **unchanged since the freeze**, not that it is
  **what upstream published**. A substitution performed before the freeze would be pinned as truth. Smallest
  remediation: record the three tarball digests and the Electron zip digest in the claims container as
  *recorded-not-reverified* evidence, or re-fetch and hash the assets once (network-authorized) and keep the
  digests in `l1/`. Neither is done here.
- **P2 — `icudtl.dat` claim is unprovable and cannot be corroborated by proxy (medium).** r64 F6 says the
  installed `c5da2fc3…` comes from `electron-v42.2.0-linux-x64.zip` (`9caeeb15…`). That zip is absent; the only
  Electron zip on the host (`electron-v40.10.2`, `02462014…`) ships a **different** `icudtl.dat`
  (`1cf67874…`). So the file is version-specific and the held archive cannot stand in. Three closure entries
  depend on a source the host cannot show. Smallest remediation: state the icudtl pin as *attested in round
  64, not re-verifiable*, and either retain the Electron zip or re-derive it.
- **P3 — the one third-party Python dependency was fetched from PyPI during prep and its wheel digest is not
  in any lane receipt (low-medium).** uv's cache holds URL + wheel sha256 (`ae430a44…`) and an ETag, but no
  wheel body, and the closure pins post-install bytes only — so it pins *what was installed at 19:36:33*, not
  *what PyPI published*. Mitigations already present: version pinned, `RECORD` self-check 8/8 clean, no `.pth`
  or site hooks. Smallest remediation: copy the wheel digest and URL into the round receipt.
- **P4 — the prep README overclaims what the census proves (low).** "the census proves the run writes
  nothing" is true only for regular files **under the toolchain root**, minus `jsc2js-src/.git/`
  (`CENSUS_EXCLUDE`). `SUBPROCESS_ENV` is `{"PYTHONDONTWRITEBYTECODE": "1"}` and the child env is
  `dict(os.environ)`, so `HOME`, `TMPDIR` and the excluded `.git/` are outside what before/after can see.
  The predicate itself is unaffected (it says "census equals census"); only the receipt's wording is wider
  than the mechanism. Smallest remediation: reword to "the census proves no regular file under the root
  (excluding `jsc2js-src/.git/`) changed".
- **P5 — `venv/.lock` is world-writable (0666) inside a tree described as read-only (low).** It is not a
  closure member and not read by the instrument, so it cannot move a pinned hash; noted because a writable
  inode inside a "read-only" root is the kind of thing a later seat assumes away.
- **P6 — the source repo's index was refreshed during prep (low, hygiene).** `jsc2js-src/.git/index` mtime
  19:43:16, seven minutes after the 19:36:29 clone, i.e. a `git status`-class operation ran there even though
  the round rule forbids it (the rule's stated reason is exactly index refresh). It cannot affect the census
  (`.git/` excluded) and no tracked content moved — `rev-parse HEAD` is still `01fc264d…` and the 12 View8
  blobs match — but the rule and the observed mtime disagree.
- **P7 — no secret exposure found (informational).** No credentials, keys or tokens in the tree, the wave dir
  or the venv; nothing was printed that would need redaction.

## 7. What I ran (one line each, read-only)

`sha256sum` over 3×{d8,snapshot,icudtl}, node, interpreter, `pyvenv.cfg`, `parse` METADATA/RECORD, both
frozen tools, `mkcache.js`, `atom.compiled.dist.jsc`, `probe-electron.jsc`; `ast.literal_eval` recomputation of
all 30 pins; `d8 --version` ×3 (env-scrubbed, cwd=scratch); `strings -a | grep -c -i jsc2js` ×3; asar member
extraction from `/usr/share/typora/resources/app.asar` with the asar integrity field read back; `git cat-file
blob 01fc264d:<path> | sha256sum` ×12 and `rev-parse 01fc264d:View8`; `find` for `__pycache__`/`*.pyc`
(0), for tarballs (0), for secrets (0), for setuid/world-writable (only `venv/.lock`), for post-20:12 mtimes
(0); `git -C <lane> log c99e907c..HEAD` (2 commits); `ls -lt --full-time` on `inputs/`, the tree root and
`jsc2js-src/.git/`; `findmnt`/`df -T` (btrfs `/home`, xfs `/fast`; `/home/.snapshots` empty);
`~/.cache/uv` mtime scan; `python` RECORD verification (8 files, 0 bad).
No instrument run, no lane write, no network, no git/jj mutation, no pacman.
