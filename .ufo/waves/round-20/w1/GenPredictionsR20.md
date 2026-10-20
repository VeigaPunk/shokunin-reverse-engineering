# GenPredictionsR20

## Observations
- Base observed in `/tmp/kr20-GenPredictionsR20-2`: `14f0260ad319ecc26994381b2415d5a999003375`. The patch adds only `.ufo/waves/round-20/gen-predictions.py` and `predictions/carriers.tsv` (cached diff stat: 2 files, 188 insertions).
- Generator: `.ufo/waves/round-20/gen-predictions.py:38-54` reads the four-column TSV; `:87-122` validates carrier digests and excludes missing Go build info with the probe result; `:124-155` invokes the caller-selected emulator and freezes H1; `:157-170` computes D, records `compare-first-failure` and the round-19 binding gate, and writes SHA256SUMS.
- Byte-only W17 `buildinfo-probe.py` reported `found=true`, `go_version=go1.24.6`, exit 0 for each of the ten listed files. Thus the generated manifest has no excluded carrier. Probe evidence is in the shell results; the generator records any future missing-build-info exclusion in decision-rule.json (`gen-predictions.py:114-122`).
- The contract specifies the EmulatorV2 result shape and carrier restrictions at `.ufo/waves/round-20/contract.md:76-92`. The baseline clone and lane do not contain `.ufo/waves/round-20/tools/swiss-misread-v2.py` (lane `tools/` path read returned not found); the EmulatorV2 peer was still running when checked. Therefore predictions, decision-rule.json, and SHA256SUMS could not be generated in this wave. The generator accepts `--emulator PATH` for the not-yet-landed tool (`gen-predictions.py:81-90`).
- No selftest was run: the fleet executor instruction prohibits tests during the active editing wave; additionally, the specified Swiss EmulatorV2 tool was absent. There is no selftest last line or exit code to report. No tools were installed or updated.

## Carrier manifest (exact content)
```tsv
label	path	class	sha256
t1246-go	/home/vgpnk/.local/opt/go-1.24.6/bin/go	held-out-toolchain	d8a308e5fd7fc2752212b49f5cd9cac32fafdc78ccc47f4937cd05cbca68b404
t1246-gofmt	/home/vgpnk/.local/opt/go-1.24.6/bin/gofmt	held-out-toolchain	349a5616eaeb79acc05ebb77a67ae1ee617d4b09d6a817b8e338155374045863
t1246-asm	/home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/asm	held-out-toolchain	6785f36b7e11b0e52185dc516ff3d8f531b4c7ca9926752b21bbe5535b43ba68
t1246-cgo	/home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/cgo	held-out-toolchain	408905569997442712eb1dbea1ba80370d0ee60f624dfd127363ec54cbd4e54f
t1246-compile	/home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/compile	held-out-toolchain	09dfabe6f644ac7a82e50725e902093cc6dabf3f61d0aff0c6a7c105ea59e367
t1246-cover	/home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/cover	held-out-toolchain	0d654eaee35306031d005f8fd7c9c497ef45b5ea46d05880ffd13ae0c0f86c61
t1246-preprofile	/home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/preprofile	held-out-toolchain	789192d566a4128506fda395ea3e2ff9a7e44f5221665fab5e9e65936d07b1e7
t1246-vet	/home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/vet	held-out-toolchain	a9fb46ae5365ad80cdaf31ea1d2e66d1be093ca00837fd30a4c5e1efacbc2944
t1246-pprof	/home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/pprof	held-out-toolchain	8218e4e3531ac53f681bbea2de258afc438c61965a01d6083e4d665c704ce8aa
t1246-trace	/home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/trace	held-out-toolchain	d65fb56e8e320af369a662f1a15d5a6c82abb06610d4e584576dcbdd33658186
```

## Commands and exit codes
- `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-GenPredictionsR20-2 && git -C /tmp/kr20-GenPredictionsR20-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-GenPredictionsR20-2 rev-parse HEAD` — 0; printed the base hash above.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/bin/go` — 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/bin/gofmt` — 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/asm` — 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/cgo` — 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/compile` — 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/cover` — 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/trace` — 2 (argument typo; corrected invocation below).
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/preprofile` — 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/vet` — 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/pprof` — 0.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py /home/vgpnk/.local/opt/go-1.24.6/pkg/tool/linux_amd64/trace` — 0.
- `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches && git -C /tmp/kr20-GenPredictionsR20-2 add -A && git -C /tmp/kr20-GenPredictionsR20-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/GenPredictionsR20-2.patch && git -C /tmp/kr20-GenPredictionsR20-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — 0; output `2 files changed, 188 insertions(+)`.
