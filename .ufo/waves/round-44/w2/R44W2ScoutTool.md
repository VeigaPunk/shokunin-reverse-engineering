# R44W2ScoutTool — round-44 tooling inventory

Seat `R44W2ScoutTool`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only inventory of what round 44 used or installed. This seat installed nothing and ran no pacman transaction (`-Q` / `-Qi` and `/var/log/pacman.log` reads only).

No numbered defect for the L1. Live binaries still match the frozen `tools/round-44/carriers.json` toolchain digests. The only package-manager installs recorded inside the round are two scratch-local probes (below); both scratch trees are gone.

## Axes

1. Named-tool presence, version, path, channel.
2. Whether any of those bytes were installed or upgraded during round 44.
3. Whether any pacman transaction happened (this seat, and the host log on the round's date).
4. Match against the frozen toolchain block, not a fresh pin.

## Tool / version / channel / reason

| tool | version | path | channel | why it is in this round | installed this round? |
|---|---|---|---|---|---|
| rea-agents | **6.5.0** | `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json` (`"version": "6.5.0"`) | npm npx cache (pre-existing). `package.json` mtime `2026-10-27 05:21:03.972295396 -0300`. Parent dir mtime `2026-10-28 11:18:44.189040438 -0300` (cache lookup during the round; children stay 2026-10-27) | `npx -y rea-agents@6.5.0 extract-firmware` is the C1 runner | **no** (cache not rewritten) |
| unblob | **26.6.4** | symlink `/home/vgpnk/.local/bin/unblob` → `/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob` (327 bytes, mtime `2026-10-25 18:10:59 -0300`) | `uv tool` (`uv tool list` → `unblob v26.6.4`; `uv-receipt.toml` requirement `name = "unblob"`, entrypoint into `~/.local/bin/unblob`) | REA extractor; S138 expectation trees. Not an independent oracle | **no** (mtime 2026-10-25) |
| unsquashfs | **4.7.5** (`unsquashfs version 4.7.5 (2026/03/01)`); package `squashfs-tools 4.7.5-1` | `/usr/bin/unsquashfs` | Arch official (`pacman`). Packager Christian Hesse. Install Date `Sat 24 Oct 2026 04:51:13 AM -03`. Log: `[2026-10-24T04:51:12-0300] Running 'pacman -S --noconfirm --needed squashfs-tools'` | independent oracle | **no** |
| 7z | **26.04** (`7-Zip 26.04 (x64) … 2026-10-05`); package **`7zip` 26.04-1**, which **Provides `p7zip`** | `/usr/bin/7z` (37-byte shell script: `exec /usr/lib/7zip/7z "$@"`) | Arch official. Packager George Rawlinson. Installed `2026-10-13` as `26.03-1` (`pacman -S … 7zip`), upgraded `[2026-10-20T09:16:29-0300] upgraded 7zip (26.03-1 -> 26.04-1)` | third producer, corroboration only | **no** |
| backhand (PATH name) | **absent** | `command -v backhand` → not found; `command -v backhand-cli` → not found | — | claims text: no v2ns profile | n/a |
| unsquashfs-backhand | **0.25.5** (`unsquashfs-backhand 0.25.5`) | `/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand` (also `add-backhand`, `replace-backhand`). mtime `2026-10-26 19:05:36 -0300`. sha256 `88cf3ba5db572a43ef70553416be104b1de70058cb63f1d6f532615cf007972f` | cargo registry: `.crates.toml` pins `backhand-cli 0.25.5`. **Not on PATH** | same crate the v2ns probe used; this opt tree predates the round | **no** (mtime 2026-10-26) |
| backhand-cli (round probe) | **0.25.5** (seat record, not re-executed) | was `/fast/scratch/hyaku/kaidoku-r44/probe-R44LabV2ns/backhand-root` — **path absent now** | `cargo install --root <that scratch>` | R44LabV2ns v2ns reader probe | **yes, scratch-only, wave 1** |
| PySquashfsImage | **0.9.0** (seat record) | was `probe-R44LabV2ns/venv` — **path absent now** | `pip` into that scratch venv | extra v2ns reader; refused (v4-only) | **yes, scratch-only, wave 1** |
| diffutils | **3.12-2** | pacman-owned `/usr/bin/cmp` family | Arch official, dependency (not explicit). Install Date `Sat 03 Oct 2026 05:42:01 PM -03`. Log `[2026-10-03T20:42:01+0000] installed diffutils (3.12-2)` | host of the `cmp -l` hazard (claims item 11) | **no** |
| sasquatch (used, not in the named query) | **4.5.1** (`unsquashfs version 4.5.1 (2022/03/17)`, `-version` exit 1) | `/home/vgpnk/.local/bin/sasquatch` and `sasquatch-v4be` (mtimes `2026-10-26 01:22`) | prior-round local binary (PROVINCE: round-36 onekey-sec deb). Not touched here | producer behind unblob, not the oracle | **no** |

`ls /home/vgpnk/.npm/_npx/*/node_modules/rea-agents/package.json` returns **one** file, the 6.5.0 cache above. The historical 6.7.0 cache `/home/vgpnk/.npm/_npx/a1722018f28f9df2` is absent.

`pacman -Q p7zip` does **not** fail and does **not** print a package named `p7zip`. It prints `7zip 26.04-1` and exits 0, because `7zip` provides `p7zip` (`pacman -Qi 7zip`).

## Frozen digest check (live == `carriers.json` `toolchain`)

| pin | frozen sha256 | live sha256 | match |
|---|---|---|---|
| `/usr/bin/unsquashfs` | `461e1fd9eac39c12e673042807459985636030d5557319343fc3a6ed4ba1677c` | same | yes |
| unsquashfs `-version` stdout | `6154c39eee941fa66ea0ee7942802a2607d6ee2e749051c956569d7e9f6d333a` | same | yes |
| `/usr/bin/7z` (the 37-byte wrapper) | `f802383f13b8331aabaf779def00a356c8d2b8148255170b75b03028f4d23ad4` | same | yes |
| `7z` no-arg stdout | `1fc75706498ddeea4ae822a1d9d6561bdca640cbbc06db4e3a5cb1e3f8a80c8d` | same | yes |
| unblob wrapper | `0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09` | same (`sha256sum` followed the symlink) | yes |
| unblob `--version` stdout | `47e584e899c6aef8a25c9f20db3a736da9f17cbd321bf6026be6c627dfec4582` (`26.6.4\n`) | same | yes |
| sasquatch / sasquatch-v4be | `ad02d27a…774754` / `fac88740…7214c6` | same | yes |

`/usr/bin/unsquashfs -version` exits **1** after printing the version line. That matches the frozen note; it is not a toolchain failure.

## Install / upgrade events in round-44 receipts

Prescribed command (the `head -40` the seat spec names):

```
grep -rn 'install\|pacman\|uv tool\|npm -g' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/ | head -40
```

Exit **0**, wall `0.000984` s, stdout sha256 `84b74c21704d897c8e6476c57e2867057a0ce2be6b68257652160966044f2bfe`, 8428 bytes, 40 lines. Copy: `.ufo/waves/round-44/w2/artifacts/R44W2ScoutTool/prescribed-grep-head40.txt`.

Those 40 lines are **not** an install log. Line 1 is a read-only `pacman -Q` inside `w1/artifacts/R44ConnSibling/overlap-receipts.py`. Lines 2–40 are the word "install" inside the saved Android docs mirror `w1/artifacts/R44Quarantine/s113-adb.html`. The real event is past `head -40`.

Narrower search of `l1/` and `w1/` (excluding `*.html` and `*.json`), pattern `cargo install|uv tool install|npm install -g|npm -g |pacman -S|pacman -Sy|pacman -U`, exit 0, wall `0.002780` s, stdout sha256 `40d9813722e165dad22f1b1fec4838ca1aa2a13ee943fd900b54315b875b102f` (2 lines). Copy: `package-install-events.txt`.

What that search actually finds:

1. **Not an event.** `w1/artifacts/R44C1Controls/controls/pos/tree/PROVINCE.md:125` quotes the standing rule that `pacman -Sy <pkg>` is never run.
2. **The only recorded package install.** `w1/R44LabV2ns.md:77` — `backhand-cli` 0.25.5 via `cargo install --root /fast/scratch/hyaku/kaidoku-r44/probe-R44LabV2ns/backhand-root`. Line 78 — `PySquashfsImage` 0.9.0 via `pip` into `probe-R44LabV2ns/venv`. Same fact is rolled up in `.ufo/waves/round-44/r44-w1-results.json` (the LabV2ns `installs` array: cargo channel, "pacman paused"). Probe stderr kept at `w1/R44LabV2ns/receipts/r3-backhand-l.err` (v4/AVM magic asserts; no v1/v2 profile).

No `uv tool install` and no `npm -g` / `npm install -g` in `l1/` or `w1/` markdown. "L1 installs" elsewhere in wave-1 means copying an authored script into `tools/round-44/`, not a package install.

The LabV2ns scratch root is **not on disk now** (`ls` → `No such file or directory`). The off-PATH `~/.local/opt/backhand-0.25.5-v3` tree is a different, older install (2026-10-26).

## Pacman transaction?

**No pacman transaction on 2026-10-28.** `rg -c '\[2026-10-28' /var/log/pacman.log` → no matches (`oct28_lines=0`).

This seat did not run `pacman -S`, `-Sy`, `-Syu`, `-U`, or `-R`.

The nearest earlier transaction is unrelated and the day before the round's source-open timestamps: `[2026-10-27T11:26:44-0300] Running 'pacman -S --needed --noconfirm poppler'`. Last ALPM transaction completed in the sampled tail is `2026-10-25T13:12:06-0300` (debug-package removals). None of diffutils, squashfs-tools, or 7zip moved on 2026-10-27 or 2026-10-28.

## This seat

No install, no upgrade, no PATH write, no `~/.local/bin` write. Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2ScoutTool/` was created for receipt capture, then removed (`SCRATCH_ABSENT` after `rm -rf`). The persistent shell does not fire an `EXIT` trap at the end of one command, so the removal was explicit, not the trap.

## Receipts (seat R44W2ScoutTool)

Stdout copies: `.ufo/waves/round-44/w2/artifacts/R44W2ScoutTool/receipts/`.

| command | exit | stdout sha256 | wall_s |
|---|---|---|---|
| `/usr/bin/unsquashfs -version` | 1 | `6154c39eee941fa66ea0ee7942802a2607d6ee2e749051c956569d7e9f6d333a` | 0.001168 |
| `/usr/bin/7z` | 0 | `1fc75706498ddeea4ae822a1d9d6561bdca640cbbc06db4e3a5cb1e3f8a80c8d` | 0.003379 |
| `/home/vgpnk/.local/bin/unblob --version` | 0 | `47e584e899c6aef8a25c9f20db3a736da9f17cbd321bf6026be6c627dfec4582` | 0.392387 |
| `pacman -Q diffutils squashfs-tools p7zip` | 0 | `22f758c5299907a9a821610a731b01b9f85a842d541727229d73fcfd2076203a` | 0.024643 |
| `bash -c 'command -v backhand; echo which_exit:$?'` | 0 (inner `command -v` status 1; stdout is `which_exit:1`) | `1a05af7042fb65866bbd304c0feecd7875dc09e15572261b1d58530f8c9f11e9` | 0.001860 |
| `/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand --version` | 0 | `478837d9dfe4fd652d6eb17d2820dd1753b8b0d9edc204e140f087c607993353` | 0.003755 |
| same binary `-V` | 0 | `478837d9dfe4fd652d6eb17d2820dd1753b8b0d9edc204e140f087c607993353` | 0.001932 |
| prescribed `grep … \| head -40` (see above) | 0 | `84b74c21704d897c8e6476c57e2867057a0ce2be6b68257652160966044f2bfe` | 0.000984 |

`pacman -Q` stdout is exactly:

```
diffutils 3.12-2
squashfs-tools 4.7.5-1
7zip 26.04-1
```

## Confidence and limits

- Live versions, pacman log, and frozen sha256 equality: measured, high.
- Wave-1 install record: measured from `R44LabV2ns.md` and the results rollup. The scratch binaries themselves were not re-run; the tree is gone.
- Concurrent wave-2 seats can still install after this read. This file does not claim their later actions.
- `r44-w1-results.json` "installed" hits are mostly "L1 copied a script into `tools/round-44/`". Those are not package installs.
