# SourceGo1246 — go1.24.6 linux-amd64 carrier provenance (round 20, C3 scope)

Seat: KaidokuR20.SourceGo1246-2 (read-only leaf; no subagents; no Go binary executed; no REA/Ghidra run).
Scope: official archive identity for the go1.24.6 toolchain ELFs under `/home/vgpnk/.local/opt/go-1.24.6` (`bin/*`, `pkg/tool/linux_amd64/*`) only.

## Source opened (observed this run)

- URL: `https://go.dev/dl/?mode=json&include=all`
- Access date: 2026-10-20 17:46:57 -03:00 (`date -Iseconds`, command run at that time)
- Local copy: `/tmp/go-dl-r20.json`, 2256879 bytes, sha256 `6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950` (`sha256sum`).
- Release object `"version": "go1.24.6"` at line 19134, `"stable": true` at line 19135.
- Entry `go1.24.6.linux-amd64.tar.gz`: `filename` line 19264, `sha256` line 19268, `size` line 19269, `kind` line 19270 (`kind: "archive"`). Parsed with python `json` (list of 369 release objects); exactly one linux/amd64 archive entry exists for go1.24.6.
- Entry in the same release with sha256 `bb5bf69d…e065b` (size 76486559) is a different file; not used.

### Quote (contiguous, one line, section/line anchored)

- Section: release `go1.24.6` → file entry, line 19268:
  `"sha256": "bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712",`
- Companion quote, line 19264: `"filename": "go1.24.6.linux-amd64.tar.gz",`

## Cross-checks (observed)

| Check | Command / method | Result |
|---|---|---|
| Archive re-download | `curl -fsSL -o /tmp/go1.24.6.linux-amd64.tar.gz https://go.dev/dl/go1.24.6.linux-amd64.tar.gz` (17:47:10 -03) | 78583176 bytes; `sha256sum` `bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712` — equals JSON line 19268 and the round-19 record (`corpus/lessons/round-19.md:71-73`) |
| Installed tree vs archive | python `tarfile` streaming read of the tarball (no extraction, no execution), sha256 of each regular member vs the installed file at `/home/vgpnk/.local/opt/go-1.24.6/<member minus leading go/>` | 15735 members, 14175 regular; **14175 match, 0 mismatch, 0 missing** |
| C3 carrier ELFs in scope | magic check on `bin/*` and `pkg/tool/linux_amd64/*` | 20 files, all ELF; all inside the 14175 matched set. Key digests: `bin/go` `d8a308e5…b404` (14323704 B), `bin/gofmt` `349a5616…4863` (2926077 B), `pkg/tool/linux_amd64/compile` `09dfabe6…e367` (20979839 B), `link` `cba420d8…d2d6` (6230794 B), `asm` `6785f36b…ba68` (4650770 B) |
| Install record | `~/.local/opt/go-1.24.6/VERSION` = `go1.24.6`; `bin/go` birth 2026-10-20 12:14:45 -03, file mtime 2025-08-01 16:18:26 -03 (archive-preserved) | consistent with round-18 record (`round-19.md:69-73`) |
| Exec bits | `stat` on the 20 ELFs | all `0o644` (carrier-guard cleared; content unaffected) |

Note: the earlier `curl -sI` HEAD probe to the JSON URL returned HTTP 405; GET succeeded. Not material.

## Limits (labelled)

- Observation: the JSON and archive were fetched from go.dev over TLS; no detached signature or go.dev-published signing key was checked. Provenance is "same digest from the official endpoint, twice, plus byte-identity with the installed tree."
- Observation: go.dev's JSON is a mutable live document; this row pins the state observed 2026-10-20 17:46 -03, not a historical release record.
- Inference: because the installed tree matches the archive member-for-member, the C3 ELFs equal the official archive bytes; no claim is made about runtime behaviour or the Go 1.26/1.27 trains.
- Not done: no extraction into the install path, no execution, no REA/Ghidra run on these files.

## Tool installs / updates

None. Used only preinstalled `curl`, `sha256sum`, `stat`, and python3 stdlib (`json`, `tarfile`, `hashlib`).

## Scratch artifacts (outside the lane)

- `/tmp/go-dl-r20.json` (JSON copy)
- `/tmp/go1.24.6.linux-amd64.tar.gz` (archive copy, 78583176 B)

## Draft

Draft SOURCES.md row (11-column contract shape; id placeholder `S0NN`; tier A scoped to the C3 provenance question). Status `queued`, opened 2026-10-20, recheck `on-release`, used-by `—`.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S0NN | Go release list JSON, `https://go.dev/dl/?mode=json&include=all`, entry go1.24.6 linux-amd64 archive | dataset | A | The official go1.24.6 linux-amd64 archive digest and size, against which the installed go1.24.6 C3 carrier ELFs (`bin/*`, `pkg/tool/linux_amd64/*`) are matched; not the go1.25.0 or go1.27.3 trains and not runtime behaviour | Endpoint JSON sha256 `6b83804b8dd2d6052bb93cc03e4aba2ddee834f82c15f7bf8faacf5f91825950` (2256879 bytes); release `go1.24.6` `stable` true at line 19135; file `go1.24.6.linux-amd64.tar.gz` at line 19264, sha256 `bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712` at line 19268, size 78583176 at line 19269; fetched 2026-10-20 17:46 -03; `curl -fsSL https://go.dev/dl/go1.24.6.linux-amd64.tar.gz` re-hashed to the same sha256 and size | Gives an independent digest for the toolchain: 14175 regular members of the archive match the installed `/home/vgpnk/.local/opt/go-1.24.6` tree byte-for-byte, including `bin/go`, `bin/gofmt`, and the three `pkg/tool/linux_amd64` ELFs named in C3 scope (20 ELFs in total). | queued | 2026-10-20 | on-release | — |

Quote-table rows (for the SOURCES quote table, same shape as S038):

| ID | URL / location | Contiguous quote (≤25 words) |
|---|---|---|
| S0NN | https://go.dev/dl/?mode=json&include=all, go1.24.6 entry, `sha256` field (line 19268) | "sha256": "bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712", |
| S0NN | same entry, `filename` field (line 19264) | "filename": "go1.24.6.linux-amd64.tar.gz", |

## Verdict

ACCEPT for the stated scope (C3 go1.24.6 carrier provenance). Digest in the round-19 record matches the live go.dev entry and the re-downloaded archive; the installed tree matches the archive member-for-member. Row ready for L1 to assign the id.
