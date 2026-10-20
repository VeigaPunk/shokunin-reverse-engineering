# RealCarrierCensus — round 18 wave 1

Scope: find real (non-synthetic) Go 1.24.x/1.25.x ELF binaries on this host that are
not r17 carriers (`.ufo/waves/round-17/predictions/carriers.tsv`), over
`/usr/bin /usr/lib ~/.local/bin ~/go/bin ~/.cargo/bin /opt`, then rank ≤3 candidates
(<40 MB) by plausible named-map-type usage from `go version -m` deps only.
Artifact: `.ufo/waves/round-18/evidence/real-carrier-census.json`.

## Method (no carrier executed)

1. Filesystem walk: regular non-symlink files ≥4 KiB with `\x7fELF` magic and an
   mmap `find()` for the `\xff Go buildinf:` magic
   (`.ufo/waves/round-17/tools/buildinfo-probe.py` `MAGIC`, file line 28).
   Named roots scanned first (149,992 files, 61 magic hits), then widened to
   `/home /usr/local /var /tmp /root /etc /srv /mnt /media` (≈1.19 M more files,
   90 hits incl. already-seen) after the named roots yielded only r17 carriers.
2. Each hit decoded with the lane's own probe decoder (`elf_parse`,
   `elf_search_space`, `search_magic`, `decode_string` from
   `.ufo/waves/round-17/tools/buildinfo-probe.py`, probe() at lines 300–422),
   extended in-memory to keep the full modinfo (dep/build lines); `probe()`
   itself only exposes `modinfo_first_line` (line 326/417).
3. `carrier-census.py` run over all 35 non-synthetic 1.24/1.25 paths: sha256,
   size, ELF class, REA `inspect-go-binary` (6.5.0, read-only), `pacman -Qo`.
   Note: `go` is not installed on this host (`go version` → command not found),
   so "deps only" evidence comes from the decoded modinfo `dep`/`build` lines —
   byte-identical source to what `go version -m` prints.
4. `GOEXPERIMENT` taken from the `build GOEXPERIMENT=...` modinfo line;
   `go1.x.y X:<exp>` version-string suffixes recorded separately as
   `go_version_experiment_suffix` (toolchain-wide experiment tag, e.g.
   `noswissmap`, `nodwarf5`).

## Findings

Observation: within the six named roots exactly three Go 1.24.x/1.25.x ELFs
exist — `/usr/bin/aether`, `/usr/sbin/aether` (same sha256 `06c91f55…`, hardlinked
duplicate; pacman: `aether 4.32.0-2`), `~/.local/bin/notesmd-cli` (unowned) — and
all three are r17 carriers (carriers.tsv lines 4–5, 3). Every other Go binary in
those roots is go1.26.x–go1.27.2 (`-X:nodwarf5` toolchain builds): captree,
lazydocker, yay, git-lfs, op, cliamp, shfmt, gitleaks, runc, containerd(+shim,
stress), ctr, docker(+proxy,dockerd), fzf, gh, gum, lazygit, elephant, docker
cli-plugins, elephant `.so` providers, plus `~/.local/bin/gh` (go1.27.1) and
mason `shfmt_v3.13.1` (go1.26.1).

Observation: the wider scan adds, in the 1.24/1.25 window:
- `~/.kimi-webbridge/bin/kimi-webbridge` — go1.24.13, 10,031,288 B, real app
  (`mod dev.msh.team/harness/agent-extension`, vcs.revision d1b384e6), the only
  real non-carrier application found anywhere on the host.
- Two real upstream Go toolchain installs: `~/.local/opt/go-1.24.6/` (19 tools)
  and `~/.local/opt/go-1.25.0/` (9 tools), plus a mod-cache toolchain copy
  `~/go/pkg/mod/golang.org/toolchain@v0.0.1-go1.25.0.linux-amd64/bin/go`.
- Excluded as synthetic/cache: `~/.local/share/kaidoku-r18/carriers/s1246-*`,
  `s1250-*` (8 r18 carrier builds), `/tmp/kr18-b1|b2/*`, `/tmp/probe_*`,
  `/tmp/det_*`, `/tmp/r17-bix/esb-*`, `/tmp/abi-*` + `go-build` cache objects
  (`command-line-arguments`/`probe`/`nm`/`main` module paths), `/tmp/gore-v341/…`.
  `/etc/skel/.../shfmt_v3.14.1` is go1.27.1 (out of window anyway).

Observation: `/usr/lib/librz_bin.so.0.8.2` contains the buildinf magic as data
but no decodable blob (probe: no Go search-space magic) — a false-positive
string, not a Go binary.

## Ranked candidates (up to 3, <40 MB, deps-only plausibility)

1. **`/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge`** — go1.24.13, 10.0 MB,
   32 dep lines. INFERENCE: deps `github.com/coder/websocket v1.8.14` (WebSocket
   over net/http), `github.com/Shopify/sarama v1.34.1` (Kafka client),
   `golang.org/x/net v0.30.0` make `net/http` import near-certain →
   `http.Header` (`map[string][]string` with methods) and `url.Values`.
   Weakest point: outside the six named roots (under `~/.kimi-webbridge/bin`);
   included as the only real non-carrier app on the host.
2. **`~/.local/opt/go-1.24.6/pkg/tool/linux_amd64/pprof`** — go1.24.6, 14.0 MB.
   Real upstream toolchain binary. Stdlib-only modinfo → zero dep lines, so the
   deps-only rule yields no positive evidence; pprof's HTTP UI makes
   `http.Header` probable by role. Flagged as weakest evidence tier.
3. **`~/.local/opt/go-1.24.6/pkg/tool/linux_amd64/link`** — go1.24.6, 6.2 MB.
   Same toolchain; internally uses named map types (symbol tables) but nothing
   in deps supports it. Third only because the frontier is empty — every other
   1.24/1.25 ELF on the host is an r17 carrier, synthetic r18 build, or
   go-build cache object.

No in-scope (named-roots) non-carrier candidate exists; `dockerd` (91 MB) and
`frida_binding.node` (112 MB) exceed 40 MB and are go1.27.x anyway.

## Commands run (all read-only; no carrier executed)

- `cat .ufo/waves/round-17/tools/carrier-census.py | head -50` — exit 0
- `ls` of r17 tools/, r17 predictions/, r18 dirs — exit 0
- `python3 .ufo/waves/round-17/tools/carrier-census.py --help` — exit 0
- `python3 .ufo/waves/round-17/tools/buildinfo-probe.py --help` — exit 0
- `cat .ufo/waves/round-17/predictions/carriers.tsv` — exit 0
- `cat ~/.omp/agent/RULES.md | head -60` — exit 0
- `python3 .ufo/waves/round-17/tools/carrier-census.py --selftest` — exit 0;
  last line: `SELFTEST: CLEAN cases=10`
- `python3 .ufo/waves/round-17/tools/buildinfo-probe.py --selftest` — exit 0;
  last line: `SELFTEST: CLEAN cases=11`
- `which go; go version` — exit 127 (`go` not installed)
- `find` counts over scope dirs — exit 0 (142,639 files /usr/lib; 3,353 /usr/bin;
  613 /opt; 34 ~/.local/bin; 0 ~/go/bin; 0 ~/.cargo/bin)
- `du -sh` scope dirs — exit 0/1 (du ok, trailing pipeline exit 1)
- `df -h /home /usr /var; ls /usr/local/bin …` — exit 0
- `python3 .ufo/waves/round-17/tools/carrier-census.py --out
  .ufo/waves/round-18/evidence/real-carrier-census.raw.json <35 paths>` —
  exit 0; stdout tail shows `counts: total 35, elf 34, go_version_found 34,
  pacman_owned 2, errors 1` (the one error: a nonexistent
  `…/toolchain@…/pkg/tool/linux_amd64/pprof` path I passed — that file does not
  exist in the mod-cache copy; recorded as per-carrier error, not hidden).
- `python3 -c` summarizer over the raw census — exit 0
- `python3 -m json.tool` validation of the final JSON — exit 0 (`JSON_VALID`)
- In-process Python scans/decodes via eval (filesystem walk + buildinfo decode +
  JSON assembly); no files written outside the lane evidence/report paths.

## Tool installs

None. `npx -y rea-agents@6.5.0` was already cached (invoked only inside
`carrier-census.py`'s read-only `inspect-go-binary` call).

## Risks / blockers

- The JSON lists 35 census-run entries (r17 carriers + the only real app +
  toolchain binaries). The 1.24/1.25 synthetic r18 builds under
  `~/.local/share/kaidoku-r18/carriers/` and `/tmp/kr18-*` were decoded in the
  scan but intentionally not run through carrier-census to avoid npx noise;
  their versions/sizes/modinfo are in this report's findings and re-derivable.
- `~/go/bin` and `~/.cargo/bin` are empty (observation); `~/go/pkg/mod` toolchain
  copies were covered by the wider scan.
- Rank-2/3 plausibility is low-evidence by construction: toolchain binaries are
  stdlib-only, so `go version -m` deps cannot support the map-type hypothesis;
  kimi-webbridge is the single defensible pick.
- One census per-carrier error (`unreadable` pprof path) is recorded in the raw
  JSON, not hidden — exit stayed 0 per tool contract (per-carrier errors are
  data).
