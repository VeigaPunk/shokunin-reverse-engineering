# W2C1Rea — toolchain identity vs host

**Verdict: no drift of a recorded hash.** At `29883d4ec35a31a8393c4ffb220888c44c0bb022`, all four carriers (`v1le`, `v1be`, `v2le`, `v2be`) store the same unblob, sasquatch, sasquatch-v4be, and npx identities in `extract-env.json` and the same unblob, sasquatch, and `rea` blocks in `run.json`. Those sha256 values match the live files. `npx -y rea-agents@6.5.0 --version` prints `6.5.0`. The entry's sasquatch 4.5.1 sentence and hash are supported. Two gaps are not hash drift: the child PATH's `node` is `/usr/bin/node` v26.12.0 while the recorded npx file lives under the v24.21.0 tree, and the entry's `counter-fixed-path` line range does not reproduce its own stdout hash.

Read from git objects at `29883d4e` (`GIT_NO_REPLACE_OBJECTS=1`). Worktree not used. No tools installed. Disk guard before the pass: `/fast/scratch/hyaku` 37% used, 513.8G free (status header; the consumer listing was still running when the header was captured).

## Findings

| id | attack | result |
|---|---|---|
| F1 | recorded npx path vs the node that PATH actually runs | **Gap, not a changed hash.** `extract-env.json` `path` is `/usr/local/bin:/usr/bin:/bin:/home/vgpnk/.local/bin:/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/bin`. On that PATH, `command -v node` is `/usr/bin/node` **v26.12.0** (`6dcdb9bbe2bf22bd053ba06d5ba7b8a2d92b2d3d8c714f3b2670be3d2728c9c8`). The recorded npx file is `/home/vgpnk/.local/share/fnm/node-versions/v24.21.0/installation/lib/node_modules/npm/bin/npx-cli.js`, shebang `#!/usr/bin/env node`, so the data-run interpreter is the v26 binary. The v24.21.0 `node` is a different file (`7fde7b8afa198da66257f42ee2001d874c7355631e6d1579a5fb5ef1f246df4c`). `extract-env.json` does not record `node` (`c1-run.py` `tool_pins` looks it up and `env_doc` drops it). `/usr/bin/node` mtime is before the data run (2026-10-28T22:12:58Z), so this is the run's PATH, not a later swap. The entry does not claim a node version. |
| F2 | entry `counter-fixed-path` line range vs receipt hash | **Citation does not reproduce.** Entry row and `receipts.tsv` say `sed -n 266,272p` of the counter, exit 0, stdout sha256 `c5bbef8c01c96553bc9821bdfd39d42eac674e0d91c0396d37f2e84fb36342b8`. At `29883d4e`, lines 266–272 are `PROV_BASE` through `REQUIRED_SIDS` and hash to `64ee0893115fbb0b3d2debe441f307d3b594c86962d05e1fe14631a2e48cd0b8`. Lines 274–280 hash to `c5bbef8c…` and are the `FIXED_PATH` assignment, which does include `~/.local/bin`. The prose sentence is true; the printed line numbers are not. Same mismatch at wave-1 `14936cb9`. |
| F3 | `unblob.version` is null | **Not drift.** All four receipts have `version: null` and `version_line: "26.6.4"`. `c1-run.py` keeps a version only when the line matches `[Vv]ersion ([0-9]…)`; `unblob --version` prints `26.6.4` with no word "version". Live stdout sha256 `47e584e899c6aef8a25c9f20db3a736da9f17cbd321bf6026be6c627dfec4582` equals `tools/round-49/carriers.json` `toolchain.unblob.version_argv_stdout_sha256`. The hashed file is a 327-byte trampoline (`import unblob.cli`); that size and sha256 match `carriers.json`. Installed `unblob-26.6.4.dist-info` METADATA says `Version: 26.6.4` (METADATA sha256 `11d8c59f95620d7cb913653837e916443fe57000460b64fb4d646e32ce3bbb48`, not in the receipt). The entry's "unblob 26.6.4" sentences are the upstream tag (S112, S138); the installed `--version` agrees. |

`sasquatch-where` (`sasquatch --version`) prints the usage text, not `unsquashfs version 4.5.1`. The version line is in `sasquatch-version` and in `run.json`. Both scribe stdout hashes reproduce (below). The entry cites the pair for one sentence; the version half is the `-v` receipt.

## Recorded vs live

Identical on v1le, v1be, v2le, v2be. Runs 2026-10-28T22:12:58Z–22:13:06Z, each `exit_code` 0. Unblob logs: `sasquatch -le` on v1le/v2le and `sasquatch -be` on v1be/v2be, same tail `-no-exit-code -f -d`. No carrier invokes `sasquatch-v4be`. That matches the entry's "endianness is the only argv difference" and `carriers.json` ("not used by the v1/v2 carriers").

| identity | recorded | live check | match |
|---|---|---|---|
| unblob sha256 | `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` path `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob` | `sha256sum` of that path, exit 0, 2026-10-28T22:38:30Z, stdout sha `26e6866549a17c2d31bfed2285e6f516c5e1c318a8fb4e1ca91f556ac96675ca` (combined with the three paths below) | yes |
| unblob version | `version_line` `26.6.4`, `version` null | `unblob --version` exit 0, 2026-10-28T22:38:29Z, stdout `26.6.4\n`, stdout sha `47e584e899c6aef8a25c9f20db3a736da9f17cbd321bf6026be6c627dfec4582`, stderr empty | version line yes; structured version absent |
| sasquatch sha256 | `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` path `/home/vgpnk/.local/bin/sasquatch` size 382824 | same `sha256sum` | yes |
| sasquatch version | `4.5.1`, line `unsquashfs version 4.5.1 (2022/03/17)` | `sasquatch -v` exit **1**, 2026-10-28T22:38:30Z, stdout sha `26fdf569252636dd41476f4e867597f280ac7a4ac7a1ff8575111be3d5a8ab60`. `sasquatch -version` same stdout sha, exit 1, 2026-10-28T22:41:48Z. `carriers.json` already records exit 1 and that stdout sha | version text yes; bare `-v` is exit 1, as the frozen carriers file says |
| sasquatch-v4be sha256 | `fac88740f49b3460db6a67be93aa21e7390e2845b1e2f348265a95419b7214c6` | same `sha256sum`; `-version` exit 1, stdout sha `26fdf569…` (same banner), 2026-10-28T22:41:48Z | yes; not the binary the four logs ran |
| npx sha256 | `237adf8f3747cad8b9b62fcfd0d9c8d509a64e550337707f55100afcb79e8900` path the v24.21.0 `npx-cli.js` | same `sha256sum`. `readlink -f $(command -v npx)` in this shell is that file | file yes |
| rea-agents pin | `run.json` `rea.pin` `rea-agents@6.5.0`, `package_root` `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` | `npx -y rea-agents@6.5.0 --version` exit 0, 2026-10-28T22:40:33Z, stdout `6.5.0\n`, stdout sha `3eb8e06ca1e02f0a30b0e3eebd289494b35d4fd1466ed907b9148e03b2459b00`. Same pin under the recorded PATH: exit 0, 2026-10-28T22:42:38Z, stdout node path + npx path + `v26.12.0` + `6.5.0`, stdout sha `eda1522e7859aeceb05ae10ef3123b51dc47ae76ad334a8c4160b14b75a0d574` | version yes |
| rea-pkg.json | `package_json_sha256` `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`; `package_lock_sha256` `d42d56f0f4f8baf3ecc24f2bd24f9f09e3c99b83592ef85201f74df255e0c6ca`; version `6.5.0` | `sha256sum` of `package.json` exit 0, 2026-10-28T22:38:30Z, that hash. Cache-root `package-lock.json` (the file `c1-counter.py` `rea_package_problems` selects: `dirname(dirname(package_root))/package-lock.json`) is `d42d56f0…`. `package.json` `name`/`version` print `rea-agents 6.5.0`, stdout sha `9e681be12a221796bc47f74df982ae2ec767e65db9055552708115bb65731515`, which equals scribe receipt `rea-pkg` | yes |
| prior-pins.json | `kaidoku-r42-prior-pins-v1`: sha256 union of round 38–41 carrier pins. No unblob, sasquatch, npx, or rea-agents field | read at `29883d4e` | cannot confirm toolchain; nothing in it disagrees |

`node_modules/.package-lock.json` hashes to `ecfdcb0e225989eaaf89aeea5c008a0a5669b9f4d81f87a0b4bf0a928b6391a4`, which is not the frozen lock pin. The counter does not read that file.

## Entry sentences the receipts support

`corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md` line 27: sasquatch resolves to `/home/vgpnk/.local/bin/sasquatch`, reports `unsquashfs version 4.5.1 (2022/03/17)`, sha256 `ad02d27a…`. Supported by all four `run.json`/`extract-env.json` blocks and by the live binary. `FIXED_PATH` in `tools/round-49/c1-counter.py` lines 276–279 includes `~/.local/bin`. Recorded `child_path` is that PATH with `$HOME` expanded, and `sasquatch` is not present earlier on it (`/usr/local/bin`, `/usr/bin`, `/bin` have no `sasquatch`).

Scribe receipts re-run against the live binary, stdout sha256 unchanged:

| receipt | command | exit | stdout sha256 | utc |
|---|---|---|---|---|
| `sasquatch-version` | `sasquatch -v 2>&1 \| head -1; sha256sum $(command -v sasquatch) \| cut -c1-64` | 0 | `923b821159b4a32d623d02f3b401ddfbdd72e7396f80e5e52645afc6520d6085` | 2026-10-28T22:40:33Z |
| `sasquatch-where` | `command -v sasquatch; command -v sasquatch-v4be; sasquatch --version 2>&1 \| head -2; true` | 0 | `58c6c99c0adfb032bdb0582beaf782693ff35496b325ff2fac58eaaf9e52fc8f` | 2026-10-28T22:40:33Z |
| `rea-pkg` | `cat …/rea-agents/package.json \| python3 -c '…print(d["name"],d["version"])'` | 0 | `9e681be12a221796bc47f74df982ae2ec767e65db9055552708115bb65731515` | 2026-10-28T22:40:33Z |

The entry table abridges `sasquatch-version` to `` `sasquatch -v`; `sha256sum $(command -v sasquatch)` `` and labels the column abridged. The compound still exits 0 because `sha256sum` is last; bare `sasquatch -v` exits 1. The full tsv command is what the hash belongs to.

The entry does not state an installed unblob binary version apart from the 26.6.4 source tag. It does not state a node version. `rea-agents 6.5.0` appears as the recheck `--pkg65` placeholder (line 9); the data-run pin is in `run.json`, and the live package matches `tools/round-42/rea-pkg.json`.

## Limits (not scored as drift)

- The unblob sha256 pins the 327-byte launcher, not `site-packages`. Today `unblob --version` and METADATA both say 26.6.4, and the launcher hash matches the receipt.
- `extract-env.json` records `log_tee.sha256` `28956884f690402e7d1ab17cfd542e66114d7c503914adcb42b52c23111883b6` for a scratch `unblob-tee.sh` that is not in the commit. The note says the tee exec'd `$HOME/.local/bin/unblob`. The side-measured unblob hash matches the live trampoline; the tee bytes were not re-hashed.
- `prior-pins.json` is not a toolchain pin.

Receipts copied under `.ufo/waves/round-49/w2/W2C1Rea/`.
