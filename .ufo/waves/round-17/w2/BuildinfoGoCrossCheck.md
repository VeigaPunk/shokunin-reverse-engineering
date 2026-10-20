# W2-FALSIFY: buildinfo-probe.py vs official Go toolchain reader

Seat: KaidokuR17.BuildinfoGoCrossCheck · rev da64646adcb19c1ede7537b799b8c7d283fe43da
Oracle: `/home/vgpnk/.local/opt/go-1.27.3/bin/go` (`go version go1.27.3 linux/amd64`), source `…/src/debug/buildinfo/buildinfo.go` read directly.
Subject: `.ufo/waves/round-17/tools/buildinfo-probe.py` (read-only; never edited).
Artifact: `.ufo/waves/round-17/w2/buildinfo-crosscheck.json` (full per-carrier record).

## Carrier sweep — observation

For all 8 rows of `predictions/carriers.tsv` I ran `go version -m <path>` and
`python3 -B -I tools/buildinfo-probe.py <path>` and compared against
`predictions/<label>.inspect-go.json` (`normalized_result.build_info`).

- **go_version: 8/8 three-way agreement.** go1.27.0-X:nodwarf5 (shfmt), go1.23.12 (esbuild-0.25.12),
  go1.25.8 (notesmd-cli), go1.25.14 (aether), go1.20.12 (esbuild-0.21.5),
  go1.27.2-X:nodwarf5 (containerd-shim-runc-v2), go1.26.8 (op); esbuild-0.27.7 has no build
  info per all three sources (`go version -m` exit 1 "not a Go executable", probe `found:false`,
  REA `build_info:null`, probe `magic_file_offsets:[]`).
- **module first line (`path\t…`): 7/7 agreement** on every Go carrier (all three sources).
- **header_offset: 7/7 agreement** between probe and REA records.
- **sha256: 8/8 carriers' current bytes equal the sha256 recorded in inspect-go.json** —
  no carrier drift since predictions were frozen.
- On this corpus the probe is a faithful reimplementation; no disagreement to report.

## Defects found attacking the tool — source-level divergence, one proven live

### BIX-1 (observed divergence): PT_LOAD fallback does not exist in `debug/buildinfo`

`tools/buildinfo-probe.py:162-172` (`elf_search_space`) claims to mirror `elfExe.DataStart`
"L455-466" and adds a fallback to "the first PT_LOAD that is writable and not executable"
when `.go.buildinfo` is absent. In installed Go 1.27.3, `buildinfo.go:455-462` is:

```go
func (x *elfExe) DataStart() (uint64, uint64) {
	for _, s := range x.f.Sections {
		if s.Name == ".go.buildinfo" { return s.Addr, s.Size }
	}
	return 0, 0
}
```

No PT_LOAD fallback exists (removed upstream in Go 1.17-era rework); `dataSize==0` →
`errNotGoExe` (L170-172). The probe's cited line numbers describe a different file
revision, and the fallback means the probe accepts files the toolchain rejects.

Demonstration (scratch under /tmp, no carrier mutated):

```
cp <esbuild-0.21.5 carrier> /tmp/r17-bix/esb-renamed
objcopy --rename-section .go.buildinfo=.notgobuildinf /tmp/r17-bix/esb-renamed
go version -m /tmp/r17-bix/esb-renamed
  → "could not read Go build info …: not a Go executable" (exit 1)
python3 buildinfo-probe.py /tmp/r17-bix/esb-renamed
  → found:true, search_space:"first writable non-executable PT_LOAD",
    go_version:"go1.20.12", modinfo_first_line:"path\tgithub.com/evanw/esbuild/cmd/esbuild"
```

Impact: on any stripped/damaged-name ELF whose blob bytes still sit inside a writable
PT_LOAD, the probe reports Go build info that `go version -m` — and therefore any
calibration that treats the toolchain as ground truth — calls "not a Go executable".
If the probe is meant to predict REA/Ghidra behavior this is a false-positive axis;
if it is meant to be maximally independent, the limitation string should say it
*intentionally exceeds* `DataStart`, not that it "mirrors" it.

### BIX-2 (minor): Plan 9 claimed sniffed, never sniffed

Docstring/`limitations` (tools/buildinfo-probe.py:302-303) say "PE/Mach-O/XCOFF/Plan 9
are sniffed"; `sniff_format` (L275-286) has no Plan 9 a.out magic check
(`hasPlan9Magic` at buildinfo.go:273-282 covers magics 0x0177/0x8070/0x8071 etc.).
A Plan 9 input yields `"unrecognized"`, not a named format. Label bug only.

### BIX-3 (semantic, no output divergence): misaligned-magic tail handling

At buildinfo.go:392-399 Go returns `errNotGoExe` when the next aligned offset exceeds
the final (partial) chunk buffer; probe lines 230-232 instead set `data_offset` past
the buffer end and continue. Both conclude not-found, so no carrier-visible difference.

### BIX-4 (latent): 1 MiB `MAX_STRING` cap stricter than toolchain

`MAX_STRING = 1<<20` (tools/buildinfo-probe.py:55, enforced L263-264) makes the probe
reject inline version/modinfo strings >1 MiB as `NotGo`. Go's `decodeString` reads via
`saferio.ReadDataAt` (buildinfo.go:290, 420) whose bound is 1<<23-ish (≈10 MiB with
saferio's default cap), so a huge-but-valid modinfo would diverge. Unobserved; all
carriers' modinfo ≤ 4418 bytes.

### Verified-non-defects

- Flags 0x1/0x2 masks, ptr-size/flags offsets 14/15/16, inline decode order, empty-vers
  reject, modinfo 16-byte sentinel framing strip (mod[16:len-16] with `mod[-17]=='\n'`),
  and `DataReader` PT_LOAD vaddr/filesz mapping all match buildinfo.go L181-318 and
  L445-453 line-for-line.
- Whole-file `magic_file_offsets` scan is extra diagnostics, not a decode input.

## Bounded residual

Non-ELF formats (PE/Mach-O/XCOFF) are out of corpus; probe selftest was not run
(contract allows one run for the owning executor only; I am not it). No installs
made. Scratch confined to /tmp/r17-bix.

Report: .ufo/waves/round-17/w2/BuildinfoGoCrossCheck.md
