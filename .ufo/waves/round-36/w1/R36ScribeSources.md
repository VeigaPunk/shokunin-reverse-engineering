# R36ScribeSources — SOURCES.md rows drafted for round 36 (wave 1)

Seat: R36ScribeSources (scribe/sources). Leaf: no subagents, no background jobs.
Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, `git rev-parse --short HEAD` = `d2e46ef5`
(read-only). Only this report file was written.

## Behavior

Three registry rows drafted for append to `corpus/SOURCES.md`, in the frozen 11-column census
schema, at ids S107–S109 (lane registry held 106 rows at `d2e46ef5`; next unused ids are S107+).
Append position: immediately after the last registry row (`S106`, file line 112) and before the two
blank lines that precede `## Paths` (line 115). Each row is one line, cells contain no `|`
(`awk -F'|'` → `NF=13`, 11 cells, for all three), `status` = `mined`, `opened` = `2026-10-26`,
`recheck` = `on-release`, `used-by` = exactly
`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`.

### Rows to append (verbatim)

```text
| S107 | onekey-sec/sasquatch release sasquatch-v4.5.1-6 — https://github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6 | code | A | The sasquatch-v4.5.1-6 release as the maintainer's pinned distribution of the squashfs extractor: asset names, published sha256 digests and the tag changelog; not sasquatch's extraction behaviour and not any carrier result | Tag `sasquatch-v4.5.1-6`; body `Full Changelog: sasquatch-v4.5.1-5...sasquatch-v4.5.1-6`; asset `sasquatch_1.0_amd64.deb` sha256 `efbc92bd27594e01211e1b582f105a463a0017360a0746a93de3f283906ade95`; expanded-asset list sha256 `ab697cbc05de58e5970cf95863b5358aa6a5a8bb333cb958afdc2ea4d5cf56db` (two identical fetches, 2026-10-26) | The 4.5.1-6 tag ships prebuilt `sasquatch_1.0_*.deb` packages with published digests, so obtaining the extractor is a pinned-artifact step, not a build. | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
| S108 | unblob squashfs handler at tag 26.6.4 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | code | A | unblob 26.6.4's squashfs filesystem handler only: the executables it shells out to, the endian/AVM argument choice and the dependencies it declares; not sasquatch's own behaviour and not extraction output | Tag `26.6.4`; file sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`; `:25` `EXECUTABLE = "sasquatch"`, `:26` `V4BE_EXECUTABLE = "sasquatch-v4be"`, `:48` AVM test `header.bytes_used == header.mkfs_time`, `:54` `-le`, `:68-69` `get_dependencies` returns both; byte-identical to the installed unblob 26.6.4 site-packages copy | The 26.6.4 handler runs `sasquatch` (with `-le`, or `-be` and `sasquatch-v4be` for big-endian) and declares both as dependencies, so an absent binary is a missing-extractor gap rather than a silent skip. | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
| S109 | neovim v0.12.6 release — https://github.com/neovim/neovim/releases/tag/v0.12.6 | code | A | The v0.12.6 release's published Linux AppImage assets and their sha256 digests, plus its install section; not the AppImage internal layout and not any extraction result | Tag `v0.12.6`; body `Install` > `Linux (x86_64)` > `AppImage` `Download nvim-linux-x86_64.appimage`; asset digests `nvim-linux-x86_64.appimage` sha256 `b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb` and `nvim-linux-arm64.appimage` sha256 `8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2`; expanded-asset list sha256 `3ef86a0f14c7e5bc6bb81b426a51e9fcab79d005728d27fe5d611241326d068a` (two identical fetches, 2026-10-26) | The release publishes both Linux AppImage assets with sha256 digests, so a fetched carrier is bound to this published release by a maintainer digest, not a local hash alone. | mined | 2026-10-26 | on-release | corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md |
```

Row lengths: 952, 1029, 1004 characters = 954, 1031, 1006 bytes (each row holds one U+2014 em dash,
so bytes exceed characters by two per row).

## Gate record (SOURCES contract rule 1: URL, access date, ≤25-word quote + location)

All three sources were opened in this round, 2026-10-26, by `curl -sSL` into scratch.

- **S107** — `https://github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6`
  (HTTP 200, 195796 bytes) and its asset list
  `https://github.com/onekey-sec/sasquatch/releases/expanded_assets/sasquatch-v4.5.1-6`
  (HTTP 200, 28690 bytes).
  Quote (release body, under `What's Changed`, rendered-markdown div):
  "CI: fix build-nix by @qkaiser in #33 · unsquashfs: fix prototypes for C23 by @whispersofthedawn in #32" (16 words).
  Asset list carries `sasquatch_1.0_amd64.deb` with `sha256:efbc92bd…ade95` (also arm64 and armhf
  debs, dbgsym debs, and the `sasquatch-v4.5.1-6` source `.tar.gz`/`.zip`).
- **S108** — `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`
  (HTTP 200, 19842 bytes, 590 lines, sha256 `2d7b901b…99287`).
  Quote (`squashfs.py:25`, class `SquashFSExtractor`): `EXECUTABLE = "sasquatch"` (3 words).
  Cross-check: byte-identical to the installed copy
  `/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`
  (same sha256; `unblob --version` = `26.6.4`).
- **S109** — `https://github.com/neovim/neovim/releases/tag/v0.12.6`
  (HTTP 200, 207659 bytes) and
  `https://github.com/neovim/neovim/releases/expanded_assets/v0.12.6` (HTTP 200, 52427 bytes).
  Quote (release body, `Install` > `Linux (x86_64)` > `AppImage`): `Download nvim-linux-x86_64.appimage` (2 words).
  Asset list publishes `nvim-linux-x86_64.appimage` `sha256:b644d034…f29fb` and
  `nvim-linux-arm64.appimage` `sha256:8efcec73…e1c2`.

Capture stability (checked because a row anchor cites a digest): the two **tag** pages are
unstable across fetches — three fetches of the sasquatch tag page gave
`0a8dea31…`, `7497adc9…`, `95fa4e96…`; three of the neovim tag page gave
`52c6d865…`, `f5049858…`, `d6d3336c…` (per-response nonces). The two **expanded_assets** pages were
byte-identical on both fetches (`ab697cbc…f56db`, `3ef86a0f…068a`), so the rows anchor on the
asset-list capture and on per-asset digests, not on a tag-page hash.

## Validation evidence (scratch mirror, `sources-census.sh validate --file …`)

Scratch root `S=/fast/scratch/hyaku/kaidoku-r36/R36ScribeSources` (`export TMPDIR="$S"`), removed
before finishing; nothing below depends on scratch persisting.

Four mirrors were built: **A** = literal assignment (copy of `corpus/` + the three rows);
**B** = full lane (`tar` without `.git`/`.jj`) + the three rows; **C** = B plus a one-line stub file
at `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` (stub text: "Scratch
validation stub only — not the round-36 knowledge entry and not evidence of entry content");
**D** = full lane, no rows (clean baseline).

### A. Literal assignment mirror (corpus copy + rows) — `validate`, exit **1**

```text
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file "$S/mirror/corpus/SOURCES.md"
file	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
file	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
file	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
file	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
file	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
file	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
file	E11	S036 missing used-by SKILL.md
file	E11	S081 missing used-by tools/round-27/xpin-attribute.mjs
file	E11	S107 missing used-by corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md
file	E11	S108 missing used-by corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md
file	E11	S109 missing used-by corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md
EXIT=1
```

The two `S036`/`S081` `E11` lines are a property of a corpus-only mirror, not of the registry:
`SKILL.md` and `tools/round-27/xpin-attribute.mjs` live outside `corpus/`, and validate resolves
`used-by` against the mirror root derived from `--file` (`realpath(dirname(file)/..)`). Both resolve
in the full-lane mirror (B), where only the three new rows report.

### B. Full-lane mirror + rows, no knowledge entry — `validate`, exit **1**

```text
file	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
file	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
file	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
file	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
file	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
file	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
file	E11	S107 missing used-by corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md
file	E11	S108 missing used-by corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md
file	E11	S109 missing used-by corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md
EXIT=1
```

### C. Full-lane mirror + rows + stub at the used-by path — `validate`, exit **0**

```text
file	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
file	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
file	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
file	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
file	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
file	W04	S083 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S090 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S092 duplicate url registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz across scopes
file	W04	S102 duplicate url learn.microsoft.com/en-us/windows/win32/debug/pe-format across scopes
file	ok	/fast/scratch/hyaku/kaidoku-r36/R36ScribeSources/full/corpus/SOURCES.md
EXIT=0
```

### D. Clean full-lane baseline, no rows — `validate`, exit **0**

Identical finding set to C (9× `W04` + `ok`); `diff base2.out C.out` differs only in the printed
`--file` path. Baseline `W04` count 9 matches the round-36 plan's census start ("exit 0, 9 W04"),
so the draft introduces no new warning class.

### Frozen manual census (`CORPUS.md` v1 commands), before → after

```text
lane file (106 rows)          mirror + rows (109 rows)
rows 106                      rows 109
malformed 0                   malformed 0
tier A=100 B=5 C=1            tier A=103 B=5 C=1
status mined=102 rejected=4   status mined=105 rejected=4
dups (none)                   dups (none)
enum-violations (none)        enum-violations (none)
```

Per-row shape on the mirror: `S107 cells=11 pipes=12`, `S108 cells=11 pipes=12`,
`S109 cells=11 pipes=12` (no `|` inside any cell).

### C1-counter SOURCES binding, replayed against the drafted rows

`tools/round-36/c1-counter.py` was imported read-only (`importlib`, no execution of `main`) and its
own `cells()`/`OPENED`/`ENTRY` constants applied to the mirror rows. For S107, S108 and S109:
`cells 11`, `opened 2026-10-26`, `opened_ok True`, `used_by_exact True`, `status mined`, `kind code`,
`tier A`. Its `sid_tokens()` on a `source: S107, S108, S109 — <entry>` line returns
`['S107','S108','S109']`, so an entry whose `source:` cites these ids satisfies
`c[0] in src_ids and c[8] == OPENED and ENTRY in used`. S107's source cell also carries
`sasquatch` as a standalone token, which is what the counter's PROVINCE sibling check looks for on
its own file.

## Cross-checks (independent of the rows)

- K4's frozen carrier sha256 (`8efcec73cea1cebcd3a19da0bc782c0c6d95da7ae6006902a9d93b5ac9efe1c2`)
  and K3's (`b644d034746aed32f4e918be9fc6147408ce4ecd360fedd7130da543c35f29fb`) both appear
  verbatim in the v0.12.6 asset list page, i.e. the release publishes the digests
  `corpus/evidence/round-36/c1/carriers.json` froze. S109's `teaches` rests on that observed match.
- Installed `unblob` 26.6.4 handler is byte-identical to the tag-26.6.4 raw file (sha256 above), so
  the row's "declared dependency" reading applies to the binary the round actually runs.
- `/home/vgpnk/.local/bin/sasquatch` (sha256
  `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754`) self-reports
  `unsquashfs version 4.5.1 (2022/03/17)` on `sasquatch -version`, consistent with tag
  `sasquatch-v4.5.1-6`. [INFERENCE] Its bytes were not compared against
  `sasquatch_1.0_amd64.deb` here, so this is version-string agreement, not deb-to-binary provenance.

## Findings

1. **The three rows cannot validate clean before the knowledge entry lands.** `validate`'s `E11`
   resolves `used-by` on disk, so appending these rows first makes `SOURCES.md` exit 1 with exactly
   three `E11` lines (B above); with the entry path present the file validates `ok`, exit 0, with an
   unchanged finding set (C). Sequencing for L1: append rows and the entry in the same commit, or
   accept a transient `E11`.
2. **Tag-page hashes are not citation-grade.** Both GitHub tag pages returned three distinct page
   hashes across three fetches, while `releases/expanded_assets/<tag>` was byte-stable. Anchors
   therefore cite per-asset digests and the stable asset-list capture. Anyone re-fetching a tag page
   to "verify" a cited hash will see a mismatch that is not a source change.
3. **`kind` choice.** All three rows are `code` tier `A`: each names a specific revision of a
   source/artifact producer (release tag, tagged handler file, release assets), matching the lane's
   precedent for revision-pinned source rows (S004, S029). `community` never applies; no rejection
   needed, so no `REJECTED:` row this round.
4. **No registry collisions.** `E04` (duplicate URL+scope) did not fire for any new row, and the
   existing 9 `W04` same-URL-different-scope warnings are pre-existing and unchanged.

## Limits / out of scope

- Not written: `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`, the
  `PROVINCE.md` `## Round-36 additions to Core` row, and the `corpus/README.md` coverage-map row.
  At `d2e46ef5` all three are absent (`git cat-file -e HEAD:corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`
  → `fatal: path … does not exist in 'HEAD'`, rc 128; `grep -c` of the stem in `corpus/README.md` → 0;
  no `## Round-36 additions to Core` heading in `PROVINCE.md`). C1's `sourced` binding therefore
  becomes reachable only after the entry cites these ids.
- `c1-counter.py` / `c2-counter.py` were not run (no measured revision, and the SOURCES-side
  binding replay above is the only part in this seat's scope). No extraction was run; no carrier
  was fetched or hashed by this seat. `sasquatch`/`unblob`/`unsquashfs` were inspected only.
- The three rows are a draft: `corpus/SOURCES.md` in the lane is unmodified
  (`git status --porcelain -- corpus/SOURCES.md` → empty, exit 0), no VCS mutation was performed,
  and no other lane path was written.
- Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ScribeSources` (mirrors, page captures, row file) was
  deleted at exit; every digest and line number quoted above is reproduced in this report, and
  nothing cited depends on those paths.

## Tooling

No tools were installed or upgraded this round (`sasquatch` 4.5.1, `unblob` 26.6.4,
`unsquashfs` 4.7.5 were already present; pacman untouched). `curl`, `awk`, `sha256sum`, `git`
read-only and `python3 -I -B` were used.

Artifact: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-36/w1/R36ScribeSources.md`.
