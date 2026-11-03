# SecDownloads — provenance/safety audit of the R64-C1 binaries (w1 attack seat)

Claim under audit: **R64-C1** — "all 18 runs reproduce the frozen predicted label of their cell
(dump|view8|check), with every input and binary sha256 equal to its pin."
Surface: the inputs and binaries `tools/round-64/jsc-route-matrix.py` (sha256
`29efef4f…ba20deb`, frozen F1) loads or executes. Read-only; nothing in the toolchain, lane, or
fleet root was written, and the instrument/claims were not edited.

Full table (12 checks, commands, observed values) and finding detail:
`w1/SecDownloads/audit.md`.

## What I ran

`sha256sum`/`stat -c %a`/`file` on all three d8 trees, both artifacts, the Electron zip and the
three release tarballs; `tar -xzOf … | sha256sum` on every tarball member; `unzip -p` on the zip's
`electron`, `icudtl.dat` and member list; `git ls-tree`/`cat-file blob | sha256sum`/`rev-parse` on
the jsc2js tree; `curl -fsS` against the three GitHub release records (the only network);
`grep` over `tools/round-64/` and the instrument; `od -An -tx1 -N32` on both code caches; and
three `d8 -e 'print(typeof loadjsc, …)'` probes in own scratch. No tool installed; no git
mutation; no `pacman`.

## All six assigned checks reproduced

| # | assigned check | observed | verdict |
|---|---|---|---|
| 1 | Electron zip sha256 = `9caeeb15…f19684909` | `9caeeb15dada37cb3a2d80bf0f5899d175db026a4def11560890bd2f19684909`, 119043564 B, mode 644 — present at `/fast/scratch/hyaku/kaidoku-r64/lead/electron-v42.2.0-linux-x64.zip` | **match** (nothing downloaded) |
| 2 | d8 trees: listing, `file`, hashes, no setuid/setgid | `bc70d3c0…` / `4060ff2e…` / `c240ffae…` d8; snapshots `b5c418dc…`, `601efdc6…`, `80590f45…`; `icudtl.dat` `c5da2fc3…` in all three. Each d8: `ELF 64-bit LSB pie executable, x86-64 … not stripped`. Modes 755 dir / 755 d8 / 644 data; `find … -perm -4000 -o -perm -2000` → no output | **match, pass** |
| 3 | view8 tree + single pin `b3123e4a…` | `ls-tree` → blob `bab4a42d…`; committed blob sha256 **and** working-tree sha256 both `b3123e4a4651cbd7d810e14c6ac3ec45380e1b50580a4d194eb321e37171918c`; HEAD `01fc264d…`, `status --porcelain` empty, tree object `c125db10…` = claims F6 | **match** |
| 4 | remote-script execution grep | **zero** hits for `curl`/`wget` piped to a shell, `bash -c "$(curl`, `eval $(curl`; the only `subprocess` hits (5, all in the instrument) are argv-list calls. `grep -rn 'https\?://' tools/round-64/` → exit 1 (none) | **pass** |
| 5 | instrument never shells out with a network command | no `shell=`, no `os.system`/`popen`/`urllib`/`requests`/`socket`; all three `subprocess.run` sites pass lists. `loadjsc` is d8's builtin (`strings` → `loadjsc`, `v8::Shell::LoadJSC`; runtime `typeof loadjsc` → `function`) | **pass** (argv-only, local file read) |
| 6 | GitHub API `digest` vs local tarball | `9326e285…` = 14.8.178.14, `87a8afe9…` = 14.8.178.1, `fe518883…` = 14.7.173 — all three local tarballs byte-match the API digest, sizes match too | **match** |

Derived rows that close the chain (details in `audit.md`):

- Every tarball member hash equals the **installed** file hash for all three tags, so the
  installed trees are the API-attested releases.
- The d8 tarballs ship only `d8` + `snapshot_blob.bin`; the installed `icudtl.dat`
  (`c5da2fc3…`) is byte-identical to `icudtl.dat` inside the pinned Electron zip — the F6
  statement is accurate.
- The Electron zip's binary carries `14.8.178.14-electron.0`, `Chrome/148.0.7778.97`,
  `Electron/42.2.0`: the probe generator and D1 are the same V8 build.
- Probe (472 B) and Typora (388080 B) caches share their first 8 header bytes
  `c3 06 de c0 11 2c 84 76` (version hash + flag hash) and diverge from byte 8 — the claims
  file's "version and flag-hash words match the probe" is literally true.
- `plans/round-64-claims.md` at `3fd8468c` and `claims.json` at `a35e5141` are byte-identical to
  the working tree (`167861de…`, `473aff16…`); both freeze commits exist with the stated subjects.
- `tools/round-64/mkcache.js` is `f052eafb…` (= F4) and identical to the executed copy; it uses
  only `vm`/`fs`, no network.

## Findings (undeclared dependencies — not pin mismatches)

No pinned value diverged. These are the parts of the executed chain the frozen `PINS` map does
not cover, so the predicate holds over the **declared** pin set only. Severities are assigned for
provenance/safety impact on the claim, not as contract changes.

### P1 — `node` is executed but never pinned (medium)

`--node` defaults to the literal `"node"` and resolves via `PATH`; the check stage runs it on the
reconstructed file. Observed: `/run/user/1000/fnm_multishells/1981588_1793727763382/bin/node`,
`v24.21.0`, sha256 `7fde7b8afa198da66257f42ee2001d874c7355631e6d1579a5fb5ef1f246df4c` — a
session-scoped path, and the receipt records only the label, never the node identity.
*Exploit path:* swapping/upgrading node flips `node-pass`/`node-fail` with no pin firing and no
trace in the receipt. *Smallest remediation:* pin `node` and check `args.node` like `d8`.

### P2 — D2/D3 runtime files unpinned (medium)

`check_pins` covers `D1`'s `snapshot_blob.bin` + `icudtl.dat` only; D2/D3 are checked on the
executable alone although both start from their own snapshots
(`601efdc6…`, `80590f45…`) and the shared `icudtl.dat`.
*Exploit path:* replace `d8-14.8.178.1/snapshot_blob.bin` so that build aborts on the probe —
pins stay green and the cell reads as an agent-level mismatch instead of a tampered input.
Disk state today is correct (installed = tarball member). *Remediation:* pin the two snapshots.

### P3 — View8's dependency surface unpinned (medium)

Only `View8/view8.py` is pinned. The `--disassembled` route imports
`Parser/sfi_file_parser.py` (`7ce34163…`), `Parser/shared_function_info.py` (`b5c79cdd…`),
`Translate/translate.py` (`0e075893…`), `Translate/translate_table.py` (`717e2a67…`),
`Translate/jump_blocks.py` (`ab0acbff…`), `Simplify/simplify.py` (`9603ff0f…`),
`Simplify/function_context_stack.py` (`51b6f4f5…`), `Simplify/global_scope_replace.py`
(`0f217057…`), plus PyPI `parse` 1.22.4 and `import ast`. Two bytecode generations
(`cpython-314`, `cpython-315`) exist in the tree, so at least two interpreters ran this chain and
neither version is pinned. *Exploit path:* edit an unpinned module to change the pseudo-code
emitted; `view8-ok`/`node-pass` flip while `view8.py`'s pin stays valid.
*Remediation:* pin the imported modules and the `parse` distribution.

### P4 — the View8 step writes into the pinned toolchain tree (low)

Launched with `cwd=view8_dir` and no `-B`, CPython writes `View8/{Parser,Simplify,Translate}/__pycache__`
(14 `.pyc`, mtime 2026-11-03 19:36). `git status --porcelain` stays empty (gitignored), so no pin
fails, but the run mutates a tree the seat rules say never to write. Upstream also has two
content-reachable writes relative to that cwd: `Simplify/simplify.py:6` writes
`debug_0x708001a5f95.log` when an SFI name contains that address (not triggered by either pinned
artifact; gated at lines 460/479), and `Parser/parse_v8cache.py` spawns `VersionDetector.exe` —
that module is a separate entry point, **not** imported by `view8.py`, so the instrument's route
never reaches it. The pre-freeze log proves the relative-path hazard is real: `Exporting to file
../../probe-view8.js.` resolved outside `View8`.
*Exploit path:* an artifact whose SFI name carries the debug address writes a log file inside the
pinned tree — artifact-controlled, not operator-only. *Remediation:* run with `-B` and a cwd
inside the cell.

### P5 — `loadjsc('{artifact}')` builds JS from an unescaped path (low)

`run_cell` interpolates the path into a single-quoted JS literal with no escaping. Confirmed d8
capabilities: `read`, `load`, `loadjsc` are functions, `os.system` is `undefined` — so the
primitive is file read / JS execution, not a shell. Reachable only via operator-supplied
`--probe`/`--typora` (their contents are pinned, so the artifact itself is not the vector).
*Remediation:* interpolate `json.dumps(str(artifact))` (one line; the instrument is frozen, so
reported, not applied).

## Verdict

The six assigned checks all reproduce exactly, every pinned sha256 matches, no toolchain file is
setuid/setgid, and the round-64 tooling contains no remote-script execution, no shell invocation
and no network command. No finding falsifies R64-C1 as frozen; the five items are pin-set scope
gaps. Audit line: `provenance-open: P1,P2,P3,P4,P5`.

## Evidence pointers

- Table + per-row commands/observed values: `w1/SecDownloads/audit.md`
- Instrument sha256 observed (unchanged): `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb`
- Freeze blobs: `plans/round-64-claims.md`@`3fd8468c` → `167861dea70702d29c3683620d41efad70c142372c44ab0961c24d73ce195ea8`;
  `.ufo/waves/round-64/claims.json`@`a35e5141` → `473aff163e1afec1d7ee58f5e529aebcde0fd2813d224c232254dd3a0fadf3fd`
- Electron zip `9caeeb15…`, V8 string `14.8.178.14-electron.0`; tarball digests `9326e285…`,
  `87a8afe9…`, `fe518883…`; installed d8 `bc70d3c0…`, `4060ff2e…`, `c240ffae…`
- `__pycache__` observation: `/home/vgpnk/.local/share/kaidoku-jsc/jsc2js-src/View8/*/__pycache__`, mtime 2026-11-03 19:36
- Scratch `/fast/scratch/hyaku/kaidoku-r64/SecDownloads` deleted before yield; no other writes; no tool installed; no git mutation.

Report: .ufo/waves/round-64/w1/SecDownloads.md
