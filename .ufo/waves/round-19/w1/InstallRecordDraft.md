# InstallRecordDraft — round 19, R18-INSTALL-RECORD

Seat: `KaidokuR19.InstallRecordDraft` (leaf, read-only). Baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (`.ufo/waves/round-19/contract.md:4`). Nothing written in the lane except this report. No git write, no `jj`, no patch, no subagent. This seat installed or updated nothing (no install command was run).

Path roots: `fleet/` = `/home/vgpnk/Projects/shokunin`; `lane/` = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.

## Findings

Observations (O) and inferences (I) are labelled.

1. **O — the round-18 sha256 values are correct and complete now.** The fleet report gives them truncated (`fleet/.ufo/reports/round-18/kaidoku.md:90`). Full values from the go.dev JSON feed (fetched 2026-10-20) and from the retained tarballs both match them (commands 1 and 7). The truncated prefixes and suffixes agree with the full values.
2. **O — the round-18 record has no date.** `kaidoku.md:90` gives no install date. The install date is 2026-10-20 12:14 -0300 (commands 4, 5, 9). This is new information for the record.
3. **O — the install falls inside the round-18 mission.** The mission opened at 12:07:53 -0300 (`kaidoku.md:97`). The install (12:14:40 to 12:14:48) is before the W1 dispatch at 12:24 (`kaidoku.md:85`).
4. **O — directory mtimes are not install dates.** `~/.local/opt/go-1.24.6` has mtime 2025-08-01 and `go-1.25.0` has mtime 2025-08-08, both archive times (command 4). Birth times give the install date.
5. **O — round-17 date claim checked.** `corpus/lessons/round-17-verifier-spotcheck.md:92` says `go-1.27.3` mtime is 10:32:19. Its birth time is also 10:32:19.468 (command 10), so the claim holds for that directory. Its method (mtime) is weaker than birth time, and finding 4 shows mtime can be an archive time.
6. **O — no REA npx install is dated inside round 18.** The npx cache holds `rea-agents` `^6.5.0` (born 2026-10-16 12:49:41) and `^6.7.0` (born 2026-10-20 11:09:24) (command 11). The second predates the round-18 mission open (12:07:53). **I** — birth time of an npx cache dir is the first fetch; I do not attribute either entry to any seat. `kaidoku.md:90` lists no REA install, so the omission is consistent with these timestamps.
7. **O — the draft's parity claim is narrow.** Parity was checked on `bin/go` and on tar-entry counts only, not per file (command 8). The draft says so.
8. **O — copies in /tmp are not durable.** Retained tarballs live in `/tmp/kr18-dl/` (command 5). There are also duplicates at `/tmp/go1.25.0.linux-amd64.tar.gz` and `/tmp/kr19-SourcesRowsDraft-fetch/` with the same sha256 (command 6). `/tmp` is not a durable install record, so the draft cites `/tmp/kr18-dl` as the retained copy and marks it non-durable.
9. **O — placement deviation.** The Go trees are under `~/.local/opt` and are not on PATH (command 3). RULES names `~/.local/bin` as the official-release target (`/home/vgpnk/.omp/agent/RULES.md:7-9`). The lane contract already names the carriers under `~/.local/opt/go-1.25.0/bin` (`lane/.ufo/waves/round-19/contract.md:41-42`). The round-17 record flagged the same deviation (`lane/corpus/lessons/round-17-verifier-spotcheck.md:93`). The draft records it rather than hiding it.
10. **O — the round-18 spotcheck gap is confirmed as stated.** The gap is the missing install record in the round lesson (`lane/corpus/lessons/round-18-verifier-spotcheck.md:147`) and routed item 7 (`:199`). The draft closes it as a named correction.
11. **O — Ghidra and round-17 carriers are out of scope.** Not inspected by this seat.

## Commands (all read-only; exit codes pasted)

1. `curl -sfL 'https://go.dev/dl/?mode=json&include=all' -o /tmp/kr19-goreleases.json` → exit 0. Python parse of `linux`/`amd64`/`archive`: `go1.25.0 go1.25.0.linux-amd64.tar.gz 2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613 59659213 True` and `go1.24.6 go1.24.6.linux-amd64.tar.gz bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712 78583176 True`. Python exit 0.
2. `~/.local/opt/go-{1.24.6,1.25.0}/bin/go version` → `go version go1.24.6 linux/amd64` and `go version go1.25.0 linux/amd64`, exit 0 each.
3. `command -v go` → no output, exit 1 (not on PATH).
4. `stat -c` on `~/.local/opt/go-1.24.6`, `go-1.25.0` → birth 2026-10-20 12:14:45.644 and 12:14:47.847 -0300; mtime 2025-08-01 16:18:26 and 2025-08-08 16:33:32 -0300.
5. `find ~ /tmp /var/cache -maxdepth 4 -name 'go1.2[45]*linux-amd64*'` → four matches listed below; exit 1 (permission errors suppressed by `2>/dev/null`, matches printed). Matches: `/tmp/kr18-dl/go1.24.6.linux-amd64.tar.gz`, `/tmp/kr18-dl/go1.25.0.linux-amd64.tar.gz`, `/tmp/go1.25.0.linux-amd64.tar.gz`, `/tmp/kr19-SourcesRowsDraft-fetch/go1.25.0.linux-amd64.tar.gz`.
6. `sha256sum` of the four files above → exit 0. The three go1.25.0 copies all give `2852af0c…b613`; `kr18-dl/go1.24.6` gives `bbca37cc…8712`.
7. `sha256sum` of the two `kr18-dl` tarballs vs live JSON → equal (same output as command 6).
8. `tar -xzOf /tmp/kr18-dl/go{1.24.6,1.25.0}.linux-amd64.tar.gz go/bin/go | sha256sum` vs `sha256sum ~/.local/opt/go-{…}/bin/go` → go1.24.6 `d8a308e5…b404` both, equal=yes; go1.25.0 `b93cdfdb…4bc25` both, equal=yes; exit 0. `tar -tzf | wc -l` vs `find ~/.local/opt/go-… | wc -l` → 15735 = 15735 and 16088 = 16088; exit 0.
9. `stat -c` on `/tmp/kr18-dl` and its tarballs → dir birth 2026-10-20 12:14:40.299; tarball mtimes 12:14:45.609 (1.24.6, 78583176 bytes) and 12:14:47.818 (1.25.0, 59659213 bytes), -0300; exit 0.
10. `stat -c` on `~/.local/opt/go-1.27.3` → birth 10:32:19.468, mtime 10:32:19.948, -0300; exit 0.
11. `stat -c %w` on the two `~/.npm/_npx/*/package.json` entries naming `rea-agents` → `ad9a3fdb…` born 2026-10-16 12:49:41, `a1722018…` born 2026-10-20 11:09:24; version strings `^6.5.0` and `^6.7.0`; exit 0.
12. `curl -sfL https://pypi.org/pypi/markdown-it-py/4.0.0/json` → version 4.0.0, files `markdown_it_py-4.0.0-py3-none-any.whl` and `markdown_it_py-4.0.0.tar.gz`; exit 0. Existence check only, no sha claimed in the draft.
13. `uv --version` → `uv 0.13.0`, exit 0 (context only; the draft does not claim uv was used at install time).

Throwaway files written: `/tmp/kr19-goreleases.json`, `/tmp/kr19-mdit.json` (outside the lane).

## Draft

The draft below is the text for `lane/corpus/lessons/round-19.md`. Root for relative citations: `fleet/` = `/home/vgpnk/Projects/shokunin`; `kaidoku-shokunin/` = lane.

### Correction to round 18: R18-INSTALL-RECORD (Go toolchain install record)

This is an append-only named correction of round 18. It closes routed item 7, "R18-INSTALL-RECORD", at `kaidoku-shokunin/corpus/lessons/round-18-verifier-spotcheck.md:199`, which states that the Go installs were recorded only in the fleet report. The original statement is `fleet/.ufo/reports/round-18/kaidoku.md:90`, which gives the sha256 values truncated and no date. Round 18 text is not changed.

Installed on the host, both `linux/amd64`, official go.dev tarballs:

- **Go go1.24.6.** Channel: `go1.24.6.linux-amd64.tar.gz` from `https://go.dev/dl/?mode=json&include=all`, size 78583176 bytes (command 1). Full sha256 `bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712` (command 1; equal to the retained copy, command 6). Install path `/home/vgpnk/.local/opt/go-1.24.6`. Version check: `go version` → `go1.24.6 linux/amd64` (command 2).
- **Go go1.25.0.** Channel: `go1.25.0.linux-amd64.tar.gz` from the same feed, size 59659213 bytes (command 1). Full sha256 `2852af0cb20a13139b3448992e69b868e50ed0f8a1e5940ee1de9e19a123b613` (command 1; equal to the retained copies, command 6). Install path `/home/vgpnk/.local/opt/go-1.25.0`. Version check: `go version` → `go1.25.0 linux/amd64` (command 2).

Date: 2026-10-20 12:14 -0300. The retained tarball mtimes are 12:14:45.609 (go1.24.6) and 12:14:47.818 (go1.25.0) (command 9). The install directories were born at 12:14:45.644 and 12:14:47.847 (command 4). The directory mtimes (2025-08-01 and 2025-08-08) are archive timestamps, not the install date (command 4).

Reason: build deterministic Swiss/noswiss synthetic carriers and read `internal/abi` source (`fleet/.ufo/reports/round-18/kaidoku.md:90`). The lane's round-19 carriers are later named under `/home/vgpnk/.local/opt/go-1.25.0/bin` (`kaidoku-shokunin/.ufo/waves/round-19/contract.md:41-42`).

Channel and placement: pacman was not used because all pacman transactions were paused (`fleet/.ufo/reports/round-18/kaidoku.md:90`; the pause is also stated in the round-19 dispatch host-safety block, which this seat did not re-verify). The trees sit under `~/.local/opt`, not `~/.local/bin` as the channel order names (`/home/vgpnk/.omp/agent/RULES.md:7-9`), and are not on PATH (`command -v go` → exit 1, command 3). This placement deviation was already flagged for round 17 (`kaidoku-shokunin/corpus/lessons/round-17-verifier-spotcheck.md:93`).

Verification: each installed `bin/go` is byte-identical in sha256 to `go/bin/go` inside its tarball, and the installed tree entry counts equal the tar entry counts (15735 and 16088) (command 8). This is a spot check of `bin/go` and entry counts, not a per-file comparison.

Retained copies: `/tmp/kr18-dl/` (not a durable location). Duplicates at `/tmp/go1.25.0.linux-amd64.tar.gz` and `/tmp/kr19-SourcesRowsDraft-fetch/` have the same go1.25.0 sha256 (command 6).

Other installs: none global. The round-18 report records one ephemeral environment, `uv run --with markdown-it-py==4.0.0`, with "nothing global" (`fleet/.ufo/reports/round-18/kaidoku.md:90`). No artifact or sha256 was recorded for it; PyPI lists markdown-it-py 4.0.0 (command 12). [INFERENCE: the ephemeral environment left no retained artifact; the uv cache was not searched.]

Limits: the install date comes from kernel birth times and file mtimes, not a log. The pacman pause is reported, not re-observed. The full tree was not compared file by file.

## Limits

- Parity is a spot check (command 8), not a full tree hash.
- `/tmp` copies are not durable; the draft says so.
- The pacman pause was not re-observed in this round.
- No outside check of the round-18 install claims was performed beyond the commands above.
