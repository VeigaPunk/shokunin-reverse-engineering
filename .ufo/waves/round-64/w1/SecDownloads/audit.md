# SecDownloads — provenance and safety audit of the binaries R64-C1 consumes

Seat `SecDownloads`, round 64, wave w1. Scope: the inputs and binaries that
`tools/round-64/jsc-route-matrix.py` (sha256 `29efef4f…ba20deb`) loads or executes. Read-only
except own scratch (`/fast/scratch/hyaku/kaidoku-r64/SecDownloads`, deleted). No file in the
toolchain, lane, or fleet root was modified; no network fetch beyond the three named GitHub API
release records; no tool installed.

Instrument sha256 observed: `29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb`
(equal to frozen F1). Freeze commit `3fd8468c` is present and is the declaration commit
(`round-64: declaration - jsc route outcome matrix instrument, plan, carry-in and do-nothing
before-arm`); `a35e5141` is the operative freeze.

## Table

| # | check | command | observed | verdict |
|---|---|---|---|---|
| 1 | Electron 42.2.0 zip pin | `sha256sum /fast/scratch/hyaku/kaidoku-r64/lead/electron-v42.2.0-linux-x64.zip` | `9caeeb15dada37cb3a2d80bf0f5899d175db026a4def11560890bd2f19684909`; 119043564 B, mode 644, `vgpnk:vgpnk` | **match** (zip present locally under `/fast/scratch/hyaku/kaidoku-r64/lead`; nothing downloaded) |
| 2a | d8 14.8.178.14 tree | `ls -la`, `file`, `sha256sum`, `stat -c %a` | `d8` 49284864 B `bc70d3c0…835331`, `snapshot_blob.bin` 356296 B `b5c418dc…c17bf2bb`, `icudtl.dat` 10876464 B `c5da2fc3…85a46b6`; dir 755, d8 755 `-rwxr-xr-x`, data files 644 | **match**; ELF 64-bit LSB pie, x86-64, interpreter `/lib64/ld-linux-x86-64.so.2`, BuildID `834f9ae17276b0c0` |
| 2b | d8 14.8.178.1 tree | same | `d8` 49285616 B `4060ff2e…a1ae49b8`; snapshot 356296 B `601efdc6…fa73e24d`; icudtl `c5da2fc3…85a46b6`; 755/755/644/644 | **match**; ELF 64-bit pie x86-64, BuildID `8053f4736ea2eba1` |
| 2c | d8 14.7.173 tree | same | `d8` 49922216 B `c240ffae…62bcdcf2`; snapshot 351584 B `80590f45…98ea2720`; icudtl `c5da2fc3…85a46b6`; 755/755/644/644 | **match**; ELF 64-bit pie x86-64, BuildID `5c825e76f3b8922c` |
| 2d | no setuid/setgid in the toolchain root | `find /home/vgpnk/.local/share/kaidoku-jsc -maxdepth 2 \( -perm -4000 -o -perm -2000 \) -printf '%m %p\n'` | no output (exit 0); every path is 755 dir / 755 executable / 644 data | **pass** — no setuid, no setgid |
| 3a | View8 pin, committed object | `git -C …/jsc2js-src ls-tree 01fc264d… View8/view8.py` | `100644 blob bab4a42d8dcf3d22941b90b3ed079916463b0ae1	View8/view8.py` | **match** (HEAD is `01fc264d22055865a460b322399a15d84b71f5aa`, `git status --porcelain` empty) |
| 3b | View8 pin, bytes | `git -C … cat-file blob 01fc264d…:View8/view8.py \| sha256sum`; `sha256sum …/View8/view8.py` | `b3123e4a4651cbd7d810e14c6ac3ec45380e1b50580a4d194eb321e37171918c` from **both** the committed blob and the working tree (2634 B) | **match** to the required `b3123e4a…`; tree object `c125db10c7ce6f9cfc48a0cf80def3dc23b378bf` equals claims.json F6 |
| 4 | remote-script execution in round-64 tooling | `grep -rnE 'curl\|wget\|bash -c "\$\(\|eval \$\(\|sh -c\|subprocess\|os\.system\|Popen\|shell=True\|run\(' tools/round-64/` plus `grep -rn 'https\?://' tools/round-64/` | **5 hits, all in the instrument and all benign**: `import subprocess` (l.44), `subprocess.run([str(d8), "-e", "loadjsc('…')"])` (l.171), `subprocess.TimeoutExpired` (l.173), `subprocess.run([python, "view8.py", "--disassembled", …])` (l.204), `subprocess.run([node, "--check", …])` (l.211). Zero `curl`, zero `wget`, zero `sh -c`, zero `shell=True`, zero `eval $(`, zero URL in the whole directory (`grep` exit 1). | **pass** — no remote-script execution anywhere |
| 5 | instrument never runs a shell or a network command | read `tools/round-64/jsc-route-matrix.py:28-70,150-235,239-329`; `grep -nEi 'shell\|os\.system\|popen\|curl\|wget\|urllib\|httpx\|requests\|http' ` on it | only two prose matches ("the value a POSIX shell reports", lines 28/90). Every `subprocess.run` takes an **argv list** and no `shell=` argument. `loadjsc` is d8's own shell builtin, confirmed in all three binaries (`strings`: `loadjsc`, `_ZN2v85Shell7LoadJSCE…`) and at runtime (`typeof loadjsc` → `function`). | **pass** — argv-only, no shell, no network (see P5 for the one quoting gap) |
| 6 | release digest vs local tarball | `curl -fsS https://api.github.com/repos/xqy2006/jsc2js/releases/tags/<tag>` compared with `sha256sum /fast/scratch/hyaku/kaidoku-r64/lead/d8-<tag>-linux.tar.gz` | 14.8.178.14 API `sha256:9326e285…ee5f6` = local `9326e285…ee5f6`; 14.8.178.1 API `sha256:87a8afe9…b6ea3` = local `87a8afe9…b6ea3`; 14.7.173 API `sha256:fe518883…0738de` = local `fe518883…0738de`; API asset sizes 13796728 / 13797051 / 13962025 B match local tarballs | **match** for all three (tarballs are present locally, so comparison was possible) |
| 7 | tarball member ≡ installed file (derived) | `tar -xzOf <tgz> d8 \| sha256sum`; same for `snapshot_blob.bin` | every member hash equals the installed file hash for all three tags; `tar -tvzf` shows members `runner/runner` mode `-rw-r--r--`, dates 2026-08-11 | **pass** — installed trees are byte-identical to the API-attested tarballs |
| 8 | `icudtl.dat` provenance (derived) | `tar -tvzf` (members: only `d8` + `snapshot_blob.bin`); `unzip -l`/`unzip -p … icudtl.dat \| sha256sum` on the Electron zip | the d8 tarballs **do not ship** `icudtl.dat`; the installed `c5da2fc3…85a46b6` is byte-identical to `icudtl.dat` inside the pinned Electron 42.2.0 zip (`9caeeb15…`) | **attested** — the pin resolves to the Electron zip, as claims F6 states |
| 9 | probe→Electron chain (derived) | `unzip -p <zip> electron \| strings -a \| grep -m8 -E '14\.8\.178\.[0-9]+\|Chrome/\|Electron/'` | `14.8.178.14`, `14.8.178.14-electron.0`, `Chrome/148.0.7778.97 Electron/42.2.0` | **match** — the zip is the V8 build D1 is pinned to |
| 10 | probe/typora code-cache headers (derived) | `od -An -tx1 -N32` on both artifacts; `stat -c %s` | probe 472 B, first 8 B `c3 06 de c0 11 2c 84 76`; typora 388080 B, first 8 B `c3 06 de c0 11 2c 84 76` — **version hash and flag hash identical**, differing from byte 8 on | **confirms** the claims-file statement that the Typora cache's version and flag-hash words match the probe (so the 134 crash is not a header mismatch) |
| 11 | probe generator in tree | `sha256sum tools/round-64/mkcache.js`; `diff` vs the executed copy in `lead/` | `f052eafb5c6200c82a896cbfa72ba930bd232a5e0ed4d41637f9b4f93766ff11` (= claims F4), `diff` empty against `/fast/scratch/hyaku/kaidoku-r64/lead/mkcache.js`; generator uses only `vm` + `fs`, writes one absolute path, no network | **match** |
| 12 | freeze artifacts unedited | `git -C <lane> show 3fd8468c:plans/round-64-claims.md \| sha256sum` vs working tree; same for claims.json at `a35e5141` | `167861de…195ea8` = working tree; `473aff16…adf3fd` = working tree | **pass** — both frozen files are byte-identical to their freeze blobs |

## Findings (undeclared dependencies in the executed chain)

All six assigned checks pass. The items below are **not pin mismatches** — every value in the
frozen `PINS` map was reproduced exactly. They are the parts of the executed chain that the
`PINS` map does not cover, so R64-C1's clause "every input and binary sha256 equal to its pin"
is true **over the declared pin set**, not over everything the run touches.

### P1 — `node` is executed but never pinned (medium)

The check stage runs `subprocess.run([args.node, "--check", str(out_js)])`, where `--node`
defaults to the literal `"node"` and resolves through `PATH`. Observed binary:
`/run/user/1000/fnm_multishells/1981588_1793727763382/bin/node`, `v24.21.0`, sha256
`7fde7b8afa198da66257f42ee2001d874c7355631e6d1579a5fb5ef1f246df4c`. That path is
session-scoped (`/run/user/1000/…`): after a new session the same receipt cannot be reproduced
even on an unchanged host, and the receipt JSON records only the label, never the node identity.
*Exploit path:* swap or upgrade node between the declaration run and the landing run; a
different parser verdict flips `node-pass`/`node-fail` with no pin check firing.
*Smallest remediation:* add `node` to `PINS` and check `args.node` the way `d8` is checked
(instrument is frozen → report to L1, do not edit).

### P2 — D2/D3 runtime files are unpinned (medium)

`check_pins` verifies `D1`'s `snapshot_blob.bin` (`D1-snapshot`) and `icudtl.dat`
(`D1-icudtl`), but for `D2`/`D3` it checks only the `d8` executable. The other two builds also
start from their own `snapshot_blob.bin` (`601efdc6…fa73e24d`, `80590f45…98ea2720`) and the
shared `icudtl.dat`. *Exploit path:* replace `d8-14.8.178.1/snapshot_blob.bin` with a blob that
aborts on the probe cache; `PINS` still match, the cell flips to a mismatch, and the run looks
like an agent-level failure rather than a tampered input. Today the installed copies equal the
API-attested tarball members, so nothing is wrong on disk.
*Smallest remediation:* pin the two remaining snapshots (the values are recorded above).

### P3 — View8's real dependency surface is unpinned (medium)

Only `View8/view8.py` is pinned. The `--disassembled` route resolves
`Parser/sfi_file_parser.py` → `Parser/shared_function_info.py` → `Translate/translate.py` →
`Translate/translate_table.py` → `Translate/jump_blocks.py` → `Simplify/simplify.py` →
`Simplify/function_context_stack.py`, plus the PyPI `parse` 1.22.4 package and `import ast`;
none of those bytes or the interpreter version is pinned. Observed sibling hashes (all
attributable to `01fc264d` via the clean `git status` and tree object `c125db10…`, but not
checked by the instrument): `parse_v8cache.py` `98ffc4b5…`, `sfi_file_parser.py` `7ce34163…`,
`shared_function_info.py` `b5c79cdd…`, `function_context_stack.py` `51b6f4f5…`, `simplify.py`
`9603ff0f…`, `jump_blocks.py` `ab0acbff…`, `translate.py` `0e075893…`, `translate_table.py`
`717e2a67…`, `global_scope_replace.py` `0f217057…`. Two byte-compiled generations exist in the
tree (`cpython-314` and `cpython-315`), so at least two interpreters have executed this chain.
*Exploit path:* edit `Simplify/simplify.py` (unpinned) to emit different pseudo-code; the View8
label and the `node --check` verdict change, the pin check stays green, and the recorded
`view8_out_bytes` changes without an explanation.
*Smallest remediation:* pin the eight imported modules and the venv's `parse` distribution.

### P4 — the View8 step writes into the pinned toolchain tree (low)

`view8.py` is launched with `cwd=view8_dir` and no `-B`/`PYTHONDONTWRITEBYTECODE`, so CPython
writes bytecode next to the sources. Observed: `View8/{Parser,Simplify,Translate}/__pycache__`
with 14 `.pyc` files, mtime 2026-11-03 19:36. `git -C jsc2js-src status --porcelain` is empty
because bytecode is gitignored, so no pin fails — but the run mutates a tree the seat rules say
must never be written to. The same upstream tree also carries two latent write paths relative to
that cwd: `Simplify/simplify.py:6` opens `debug_<TARGET_DEBUG_ADDR>.log` for write/append when an
SFI name contains the literal `0x708001a5f95` (searched line 460/479; not triggered by either
pinned artifact, whose SFIs are `0x311d0101e1fd` / `0x3810101e1fd`), and `Parser/parse_v8cache.py`
spawns `VersionDetector.exe` via `subprocess.run` — it is a separate entry point, **not** imported
by `view8.py`, so the instrument's route never reaches it. The pre-freeze probe log shows the
relative-output behaviour is real: `Exporting to file ../../probe-view8.js.` resolved two levels
above `View8` because the caller passed a relative path.
*Exploit path:* craft an artifact whose SFI name contains the debug address; the View8 step then
creates/appends `debug_0x708001a5f95.log` inside the pinned `View8` directory (content-controlled
write into the trust root, not an operator-only path). *Smallest remediation:* run the view8 step
with `-B` and, belt-and-braces, a cwd inside the cell directory.

### P5 — `loadjsc('{artifact}')` interpolates an unescaped path (low)

`run_cell` builds the d8 program as `f"loadjsc('{artifact}')"` with no escaping. A path
containing `'`, `\` or a newline breaks out of the string literal and injects JavaScript into the
pinned d8. Verified d8 capabilities: `read`, `load`, `loadjsc` are `function`; `os.system` is
`undefined`, so the primitive is file read/execute-JS, not shell. Reachable only through the
operator-supplied `--probe`/`--typora` paths (their *contents* are pinned, so the artifact is not
the vector). *Impact if an untrusted manifest ever supplies the path:* local file read and
arbitrary JS in the auditing binary. *Smallest remediation:* interpolate `json.dumps(str(artifact))`.

## Verdict

Every one of the six assigned checks reproduced exactly, and the derived rows close the
probe→Electron, tarball→installed and icudtl→zip chains. No pinned binary is setuid/setgid; no
remote-script execution or shell exists anywhere in the round-64 tooling; the instrument invokes
no network command. The five findings are undeclared dependencies in the executed chain, not pin
mismatches, and none of them changes a frozen predicted label by itself.

provenance-open: P1,P2,P3,P4,P5
