# DraftSourcesRows — round 17 draft report (advisory author seat)

**Axes:** calibration, depth. Source reading only. No `corpus/SOURCES.md` write, no knowledge/lesson edits, no REA/Ghidra analysis, no carrier execution.

**Deliverable:** `.ufo/waves/round-17/w1/draft-sources-rows.md` — candidate rows S024–S029 in contract-v1 11-column form (main table, all 13-field lines verified), plus a Gate table of 15 located quotes (≤25 words each) with URL, access date (2026-10-20), and location.

## Behavior

Opened and read this round (access 2026-10-20 UTC):
- Go 1.27.3 official tarball, sha256 `65efbc80…b40` matched against `go.dev/dl/?mode=json`; extracted to `~/.local/opt/go-1.27.3`.
- `go.dev/src/debug/buildinfo/buildinfo.go` (master view) and pinned `src/debug/buildinfo/buildinfo.go` in that tarball; line numbers agree at 58, 97, 224, 262.
- `go.dev/doc/devel/release` and `go.dev/doc/go1.27` (HTML snapshots, sha256 in draft).
- Linker suffix: `src/cmd/link/internal/ld/main.go:191-198`, `src/internal/buildcfg/exp.go:79-84, 157-161` (pinned tarball).
- `github.com/golang/go/issues/75953` (closed; Go1.26 milestone).
- Ghidra `GoRttiMapper.java:79` at tag `Ghidra_12.1.4_build` (`1.15-1.25`) and `master` (`1.15-1.26`); GP-6528 commit patch lines 150–151; releases feed (newest 12.1.4, 2026-09-21T17:38:59Z).
- Reopened (not new rows): installed `Base-src.zip` members `GoRttiMapper.java:79,170-171`, `GoBuildInfo.java:488-489`, `GoVer.java:62-65` (extracted under `/tmp/kr17-src`).

## Verification run (exercised)

- `go version <file>` (stdlib `debug/buildinfo` via go1.27.3; reads ELF/Mach-O bytes, does not execute): `/usr/bin/shfmt` → `go1.27.0-X:nodwarf5` (sha256 `58f765…459`, equals pilot pin); esbuild `…/@esbuild/linux-x64/bin/esbuild` → `go1.23.12` (sha256 `bab29b…014`, equals pilot pin). Carriers were not executed.
- Tiny `go/version` program on go1.27.3 (`GOTOOLCHAIN=local GOPROXY=off`): `go1.27.0` valid; `go1.27.0-X:nodwarf5` valid; `go1.27.3-X:nodwarf5` valid; `go1.27.0-X:nosizespecializedmalloc` valid; `go1.25.3 X:nodwarf5` **invalid**. Matches issue #75953's space-form defect and the linker's dash repair (main.go:193-196).
- `grep -i dwarf` on the go1.27 release-notes snapshot: zero matches.
- Release-history dates read from snapshot lines 474, 525-527, 750-751.

## Findings

1. **Observation:** Ghidra master (`GoRttiMapper.java:79`) declares `1.15-1.26`; the 12.1.4 tag and installed copy declare `1.15-1.25`. The GP-6528 commit (2026-03-03) is exactly that one-line range change plus a `go1.26.0.json` snapshot.
2. **Observation:** The newest Ghidra release in the feed is 12.1.4 (2026-09-21), and it still declares 1.15–1.25. No Ghidra release observed declares 1.26 or 1.27.
3. **Observation:** Installed `data/typeinfo/golang/` holds only `go1.25.0.json` among 1.25–1.27 files; installed `docs/ChangeHistory.md` has no 1.26/1.27 entry.
4. **Observation:** Go's own reader returns the version string raw, including the `X:` token (`buildinfo.go:97`); Ghidra strips the leading `go` (`GoBuildInfo.java:488-489`) and `GoVer.parse` drops everything after the first non `[.0-9]` char (`GoVer.java:64-65`), so `1.27.0-X:nodwarf5` normalizes to `1.27.0`.
5. **Consequence for C2 (inference):** all 1.27.x and 1.26.x carriers are outside Ghidra 12.1.4's declared range; in-range carriers must be ≤1.25.x. Pilot shfmt is out-of-range; pilot esbuild is in-range. This is consistent with claims.json C2 and is not an independent test of Ghidra's behavior.
6. **Inference:** S004 (commit) and S029 (release status) must stay separate in citing knowledge entries; master-only support must not be cited as release support.

## Out of scope / not done

- No row admitted, no `status` transitions, no `used-by` entries (L1 integrates).
- Did not reopen S003/S007 as new rows; cited only as existing anchors.
- No pilot log/receipt analysis; no REA `analyze`/`search`/`inspect-go-binary` run.

## Tool installs (per operator directive; recorded)

- Go toolchain **go1.27.3 linux/amd64** — channel: official `go.dev/dl` tarball, sha256 verified against `go.dev/dl/?mode=json`; location `~/.local/opt/go-1.27.3` (not on PATH, not in `~/.local/bin`); reason: read stdlib source and run the stdlib build-info reader and `go/version` for pinned-toolchain checks. No pacman operation performed.
- Scratch files in `/tmp` (`kr17-src`, `kr17-ghidra`, `kr17-gover`, `kr17-gocache`, the downloaded tarball was removed) — not committed, not in the repo.

## Limits

- `go.dev/src/...` URLs are a master view; the tarball is the pinned go1.27.3 tree. Line anchors agree at the cited lines, but live pages can change — the snapshot sha256s in the draft are the reproducibility handles.
- Release-history and release-notes anchors are snapshot line numbers, not stable URLs.
- The Ghidra releases feed is a live feed; L1 should recompute its sha256 before admission (the draft records the value read on 2026-10-20).
- The issue #75953 row is tier B (tracker discussion); its normative content is taken from S026 source.
- No validation that GP-6528's `go1.26.0.json` snapshot is correct; only that the range edit is present in the patch.
- `go version` reports the linker-written string; it does not prove which toolchain the carrier was built with beyond what the string records.

## Hand-off for L1 (checks the main agent should run)

- `awk` census from CORPUS.md:135-147 on the draft rows after admission (13-field lines; tier/kind/status enums; mined rows' `used-by` paths exist).
- Re-open Gate quotes once after admission if the snapshot files are unavailable (they are under `/tmp` only).
