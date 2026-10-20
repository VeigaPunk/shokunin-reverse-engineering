# EmulatorV2-2 — C3 implementation

Axes: **depth** (first-failure model), **calibration** (round-19 replay), **coverage** (eight carriers).

## Change and behavior

[OBS] Added `.ufo/waves/round-20/tools/swiss-misread-v2.py`, seeded from the unchanged r18 emulator; its r18 source and the baseline clone's r18 source both hashed to `14924bd6999b2cef4e1d217fa01d5fbb959ec8bb6e58b12959d4f4907f0e3b60`. Clone base observed with `rev-parse`: `14f0260ad319ecc26994381b2415d5a999003375`. The added file retains r18 JSON fields, applies `outCount & 0x7fff` in both func traversal paths (`:66-68`, `:945-952`, `:1054-1065`), and adds the per-hypothesis `first_failure` projection (`:1461-1476`, output `:1563-1567`). The projection normalizes `past_eof` to `eof`, records the failed read's index, the enclosing type VA, and `markup_walk`; it is null when silent. The walk continues past the emulator's synthetic `invalid_data` validation result rather than counting that as a read failure (`:1331-1347`). CLI accepts `--carrier`, optional `--label`, optional `--snapshot-dir`, and `--selftest` (`:1864-1895`). Stable selftest IDs `variadic_masked` and `first_failure_shape` were added while retaining the r18 cases (`:1788-1819`). The implementation follows the C3 contract at `.ufo/waves/round-20/contract.md:76-81` and the variadic mask shown by Ghidra `GoFuncType.java:79,86`.

[INFERENCE] `va` is the enclosing type address from the modeled markup failure, not an address asserted by the round-19 logs. `phase=markup_walk` follows the VA-sorted traversal in this emulator; these byte-only predictions are not themselves Ghidra observations.

## Round-19 retrospective predictions (final code)

[OBS] The retained replay summary reports `t1250-vet`'s H1 `Invalid index: 13902080` and no Go-analysis failure for the other seven labels (`corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:23-38,86-98`). Final v2 outputs (all carrier commands exit 0):

| Label | `first_failure` |
|---|---|
| t1250-go | `{"h0":null,"h1":null}` |
| t1250-gofmt | `{"h0":null,"h1":null}` |
| t1250-asm | `{"h0":null,"h1":null}` |
| t1250-cgo | `{"h0":null,"h1":null}` |
| t1250-compile | `{"h0":null,"h1":null}` |
| t1250-cover | `{"h0":null,"h1":null}` |
| t1250-preprofile | `{"h0":null,"h1":null}` |
| t1250-vet | `{"h0":null,"h1":{"index":13902080,"kind":"invalid_index","phase":"markup_walk","va":7599264}}` |

## Checks, commands, and delivery

[OBS] `python3 -I -B /tmp/kr20-EmulatorV2-2/.ufo/waves/round-20/tools/swiss-misread-v2.py --selftest` was run once in the clone; exact last line `SELFTEST: CLEAN cases=17`, exit 0. This was before the final `invalid_data`-skip adjustment at `:1335-1336`; no second selftest was run. The eight final byte-reading runs below exercised the adjusted file. No Go binary, REA, or Ghidra analysis was run.

[OBS] Shell commands and exits (the carrier command was run once per listed PATH/LABEL in each batch):
- `if test -e /tmp/kr20-EmulatorV2-2; then printf 'exists\n'; else printf 'absent\n'; fi` → 0 (`absent`).
- `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-EmulatorV2-2 && git -C /tmp/kr20-EmulatorV2-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-EmulatorV2-2 rev-parse HEAD` → 0 (`14f0260ad319ecc26994381b2415d5a999003375`).
- `mkdir -p /tmp/kr20-EmulatorV2-2/.ufo/waves/round-20/tools && cp /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/swiss-misread.py /tmp/kr20-EmulatorV2-2/.ufo/waves/round-20/tools/swiss-misread-v2.py` → 0.
- `sha256sum /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/swiss-misread.py /tmp/kr20-EmulatorV2-2/.ufo/waves/round-18/tools/swiss-misread.py /tmp/kr20-EmulatorV2-2/.ufo/waves/round-20/tools/swiss-misread-v2.py` → 0 (hashes above).
- `command -v jq && jq --version` → 0 (`jaq 3.1.1`).
- `python3 -I -B /tmp/kr20-EmulatorV2-2/.ufo/waves/round-20/tools/swiss-misread-v2.py --selftest; rc=$?; printf 'SELFTEST_EXIT=%s\n' "$rc"; exit "$rc"` → 0; exact last line: `SELFTEST: CLEAN cases=17`.

Each carrier invocation used this shell command, substituting PATH/LABEL below: `set -o pipefail; python3 -I -B /tmp/kr20-EmulatorV2-2/.ufo/waves/round-20/tools/swiss-misread-v2.py --carrier PATH --snapshot-dir /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang --label LABEL | jq -c '{label, first_failure}'; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"`. PATH/LABEL: `/home/vgpnk/.local/opt/go-1.25.0/bin/go` / `t1250-go`; `/home/vgpnk/.local/opt/go-1.25.0/bin/gofmt` / `t1250-gofmt`; `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/asm` / `t1250-asm`; `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cgo` / `t1250-cgo`; `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/compile` / `t1250-compile`; `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/cover` / `t1250-cover`; `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/preprofile` / `t1250-preprofile`; `/home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/vet` / `t1250-vet`. Both batches: exit 0 for all eight. The initial batch preceded the `invalid_data` skip; its go/gofmt/compile `invalid_data` records were superseded by the final batch/table.

- `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-EmulatorV2-2 add -A && git -C /tmp/kr20-EmulatorV2-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/EmulatorV2-2.patch && git -C /tmp/kr20-EmulatorV2-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375; rc=$?; printf 'EXIT=%s\n' "$rc"; exit "$rc"` → 0; stat `1 file changed, 1899 insertions(+)`.

Patch: `.ufo/waves/round-20/w1/patches/EmulatorV2-2.patch`. Report: `.ufo/waves/round-20/w1/EmulatorV2.md`. No tools were installed. LSP was unavailable in the mounted tool inventory; source was reviewed directly. No implementation blocker.