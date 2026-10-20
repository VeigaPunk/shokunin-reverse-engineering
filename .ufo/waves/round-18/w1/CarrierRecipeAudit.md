# CarrierRecipeAudit — round-18 wave-1

Seat: `KaidokuR18.CarrierRecipeAudit` (leaf, author-side advisory).
Scope: re-run `.ufo/waves/round-18/carriers/build.sh` twice into mkdtemp `OUT`, compare
against `/home/vgpnk/.local/share/kaidoku-r18/carriers/SHA256SUMS`, read build info with
`go version -m` and `buildinfo-probe.py`, write `evidence/carrier-buildinfo.json`.
QUALITY #12 anchor: `corpus/QUALITY.md:22`.

## Result: PASS — recipe is bit-reproducible

Both re-runs produced all 8 carriers byte-identical to the reference SHA256SUMS.
`sha256sum -c` printed `OK` for all 8 lines in each run (exit 0 both times).
Observation, not inference: the printed `<sha256>  <file>` lines from each run match
`SHA256SUMS` exactly, hash-for-hash and filename-for-filename.

Run outputs (identical across both runs):
```
93f3546cbb924aba632ed2b0bfebd9e0275dddb449bf65fdf3e64fa3d5d88031  s1246-noswiss-methods
e06aae7909c1dff17c1f51356f576995714fd96f98956c21a1a1cfee7b72549d  s1246-noswiss-nomethods
f8205baadc27fcf8f5a7f13bd5e68ce2522ec70a11cb768ee5b1f61c62aa48ac  s1246-swiss-methods
c0ca274873af987e67cb8b7d671935acb2837244ed5457b6eb82b35c5789a909  s1246-swiss-nomethods
450e3e5e1501813eddf068d49c65523830d1bd6209a0d5bde7aaed99b3b4ac23  s1250-noswiss-methods
e4e2f8ff8c47efb828be067217e0168020cc6ebab52c7d1f41fcc73f81ad0291  s1250-noswiss-nomethods
62e045851c08948dc27f2772c110834e06893708f65c61a8e7bd8c38932c40a5  s1250-swiss-methods
83c4f558d3224f5de6b3eab99a48cb6176ae790b03dd571265bed0f9e702a68b  s1250-swiss-nomethods
```

## Build-info findings

Evidence file written: `.ufo/waves/round-18/evidence/carrier-buildinfo.json`
(schema `{label: {sha256, go_version, GOEXPERIMENT, build_settings}}`).

- **GOEXPERIMENT confirmed**: all four `*-noswiss-*` carriers record
  `GOEXPERIMENT=noswissmap` as a build setting and `X:noswissmap` in the version
  string (`go1.24.6 X:noswissmap` / `go1.25.0 X:noswissmap`). The four `*-swiss-*`
  carriers have no GOEXPERIMENT key (encoded `null` in JSON — build.sh:16 sets the
  env var empty only for swiss... see note below).
- Both independent readers agree: `go version -m` (go1.27.3 toolchain at
  `/home/vgpnk/.local/opt/go-1.27.3/bin/go`) and the stdlib probe
  `.ufo/waves/round-17/tools/buildinfo-probe.py` report identical `go_version`
  strings and sha256 values for all 8 carriers. Probe locates the blob in the
  `.go.buildinfo` section, flags=2 (inline format), ptr_size=8, little-endian ELF.
- **1.24.6 vs 1.25.0 build-setting delta** (observation): the 1.25.0 carriers carry
  an extra `DefaultGODEBUG=containermaxprocs=0,decoratemappings=0,tlssha1=1,updatemaxprocs=0,x509sha256skid`
  setting absent from 1.24.6 carriers. Both sets share `-buildmode=exe`, `-compiler=gc`,
  `-trimpath=true`, `CGO_ENABLED=0`, `GOARCH=amd64`, `GOOS=linux`, `GOAMD64=v1`,
  matching build.sh:19-22.
- Module identity: `path\tkr18carrier`, `mod kr18carrier (devel)` — `-buildvcs=false`
  (build.sh:22) kept VCS stamps out, which the determinism result corroborates.

## Notes / minor observations (not defects)

- build.sh:16 sets `exp=""` for swiss and exports `GOEXPERIMENT=""` (build.sh:20);
  the toolchain omits an empty GOEXPERIMENT from the build stamp, so swiss carriers
  have no GOEXPERIMENT key at all. JSON encodes this as `null`, not `""` — readers
  should not expect an empty-string value.
- The recipe comment (build.sh:4) pins tarball sha256 prefixes for go1.24.6/go1.25.0;
  toolchains were already installed under `~/.local/opt/` and were not re-downloaded.
- No carrier was executed; all inspection was file-level.

## Tool selftest (required)

```
$ python3 /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools/buildinfo-probe.py --selftest
SELFTEST: CLEAN cases=11
EXIT=0
```
Last line: `SELFTEST: CLEAN cases=11` — exit code 0.

## Commands run (every command, with exit)

| # | Command | Exit |
|---|---------|------|
| 1 | `ls -la /home/vgpnk/.local/share/kaidoku-r18/carriers/` | 0 |
| 2 | `ls /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/carriers/` | 0 |
| 3 | `ls /home/vgpnk/.local/opt/` | 0 |
| 4 | `ls -R …/round-18/carriers/src` | 0 |
| 5 | `/home/vgpnk/.local/opt/go-1.27.3/bin/go version` | 0 |
| 6 | `python3 …/round-17/tools/buildinfo-probe.py --selftest` | 0 |
| 7 | `O1=$(mktemp -d /tmp/kr18-audit-1.XXXXXX) && OUT=$O1 bash …/carriers/build.sh` | 0 |
| 8 | `O2=$(mktemp -d /tmp/kr18-audit-2.XXXXXX) && OUT=$O2 bash …/carriers/build.sh` | 0 |
| 9 | `cd $O1 && sha256sum -c /home/vgpnk/.local/share/kaidoku-r18/carriers/SHA256SUMS` | 0 (8/8 OK) |
| 10 | `cd $O2 && sha256sum -c …/SHA256SUMS` | 0 (8/8 OK) |
| 11 | `for f in …/carriers/s1*; do go-1.27.3/bin/go version -m "$f"; done` | 0 |
| 12 | `python3 …/buildinfo-probe.py …/s1246-noswiss-methods` | 0 |
| 13 | `for f in …/carriers/s1*; do python3 …/buildinfo-probe.py "$f" | …; done` | 0 |
| 14 | `python3 -m json.tool …/evidence/carrier-buildinfo.json` | 0 |
| 15 | `sed -n '18,26p' …/corpus/QUALITY.md` | 0 |
| 16 | `rm -rf /tmp/kr18-audit-1.KAnXry /tmp/kr18-audit-2.BIFPNL` (cleanup) | 0 |

## Anchors

- Recipe: `.ufo/waves/round-18/carriers/build.sh:13-26` (loop), `:16` (exp selection),
  `:19-22` (hermetic env), `:26` (sha256 print).
- Reference: `/home/vgpnk/.local/share/kaidoku-r18/carriers/SHA256SUMS:1-8`.
- QUALITY #12: `corpus/QUALITY.md:22`.
- Probe: `.ufo/waves/round-17/tools/buildinfo-probe.py` (selftest at :501-608).

## Files written

- `.ufo/waves/round-18/evidence/carrier-buildinfo.json` (3687 B, valid JSON).
- This report.

## Installs

None. All tools pre-installed (go1.24.6/1.25.0/1.27.3 under `~/.local/opt/`, system python3).

## Risks / blockers

None. mkdtemp outputs removed after verification; reference carriers untouched.
