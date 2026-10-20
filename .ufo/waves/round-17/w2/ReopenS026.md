# W2 reopen S026 — Go linker build-version suffix

- Seat: KaidokuR17.ReopenS026 (leaf; read-only attack; no subagents).
- Lane revision under test: `da64646adcb19c1ede7537b799b8c7d283fe43da`. `corpus/SOURCES.md` and `corpus/lessons/round-17.md` are committed there; `git diff --stat da64646 -- corpus/SOURCES.md corpus/lessons/round-17.md` is empty (exit 0), so the working bytes are the reviewed bytes.
- Reopened 2026-10-20: the two registered go.dev `/src` URLs plus the installed go1.27.3 tree. No carrier executed; no REA `analyze`/`search`/`decompile`; no Ghidra/analyzeHeadless; no round-17 tool was run. The only network use was `curl` to reopen the two assigned URLs and `go.dev/dl/?mode=json`.
- Tool installs/updates: none.

## What I saw (verbatim)

Fetch and identity. The unversioned `go.dev/src` pages were fetched as text and compared byte-for-byte with the installed go1.27.3 GOROOT copies:

```
$ cd /tmp/s026
$ curl -sS -L -o main.go.txt 'https://go.dev/src/cmd/link/internal/ld/main.go?m=text' -o exp.go.txt 'https://go.dev/src/internal/buildcfg/exp.go?m=text'
$ sha256sum main.go.txt exp.go.txt /home/vgpnk/.local/opt/go-1.27.3/src/cmd/link/internal/ld/main.go /home/vgpnk/.local/opt/go-1.27.3/src/internal/buildcfg/exp.go
0fe8ad02e4b244bbaa82f14a86aaa005155e43c9ba7492c98c9e9650b86cd41e  main.go.txt
5825d40b47471bca28a00c0c19215930efef22b758120b6d972da1a955f21fa0  exp.go.txt
0fe8ad02e4b244bbaa82f14a86aaa005155e43c9ba7492c98c9e9650b86cd41e  /home/vgpnk/.local/opt/go-1.27.3/src/cmd/link/internal/ld/main.go
5825d40b47471bca28a00c0c19215930efef22b758120b6d972da1a955f21fa0  /home/vgpnk/.local/opt/go-1.27.3/src/internal/buildcfg/exp.go
$ diff -q main.go.txt /home/vgpnk/.local/opt/go-1.27.3/src/cmd/link/internal/ld/main.go; diff -q exp.go.txt /home/vgpnk/.local/opt/go-1.27.3/src/internal/buildcfg/exp.go
(no output, both exit 0)
```

Installed tree identity: `/home/vgpnk/.local/opt/go-1.27.3/VERSION` = `go1.27.3` / `time 2026-10-19T22:20:36Z`; `/home/vgpnk/.local/opt/go-1.27.3/bin/go version` = `go version go1.27.3 linux/amd64`. `https://go.dev/dl/?mode=json` lists `[('go1.27.3', True), ('go1.26.10', True)]` (go1.27.3 newest stable).

`cmd/link/internal/ld/main.go:191-199` (cited range 191-198; 199 shown because it is where `buildVersion` enters `runtime.buildVersion`):

```
191|\tbuildVersion := buildcfg.Version
192|\tif goexperiment := buildcfg.Experiment.String(); goexperiment != "" {
193|\t\tsep := " "
194|\t\tif !strings.Contains(buildVersion, "-") { // See go.dev/issue/75953.
195|\t\t\tsep = "-"
196|\t\t}
197|\t\tbuildVersion += sep + "X:" + goexperiment
198|\t}
199|\taddstrdata1(ctxt, "runtime.buildVersion="+buildVersion)
```

`internal/buildcfg/exp.go:79-89`:

```
79|\tdwarf5Supported := (goos != "darwin" && goos != "ios" && goos != "aix")
80|
81|\tbaseline := goexperiment.Flags{
82|\t\tRegabiWrappers:        regabiSupported,
83|\t\tRegabiArgs:            regabiSupported,
84|\t\tDwarf5:                dwarf5Supported,
85|\t\tRandomizedHeapBase64:  true,
86|\t\tGreenTeaGC:            true,
87|\t\tJSONv2:                true,
88|\t\tSizeSpecializedMalloc: true,
89|\t}
```

`internal/buildcfg/exp.go:157-161`:

```
157|// String returns the canonical GOEXPERIMENT string to enable this experiment
158|// configuration. (Experiments in the same state as in the baseline are elided.)
159|func (exp *ExperimentFlags) String() string {
160|\treturn strings.Join(expList(&exp.Flags, &exp.baseline, false), ",")
161|}
```

Quote check, run on the fetched bytes (`python3 -B /tmp/s026/check-quotes.py`):

```
cmd/link/internal/ld/main.go:197 contains=True words=7 line='\t\tbuildVersion += sep + "X:" + goexperiment'
internal/buildcfg/exp.go:158 contains=True words=11 line='// configuration. (Experiments in the same state as in the baseline are elided.)'
```

Carrier-version spot check (reads the file; does not execute the carrier):

```
$ /home/vgpnk/.local/opt/go-1.27.3/bin/go version -m /usr/bin/shfmt | head -1
/usr/bin/shfmt: go1.27.0-X:nodwarf5
$ /home/vgpnk/.local/opt/go-1.27.3/bin/go version -m /usr/bin/containerd-shim-runc-v2 | head -1
/usr/bin/containerd-shim-runc-v2: go1.27.2-X:nodwarf5
```

## Row S026 (`corpus/SOURCES.md:32`) field by field

| field | row content | verdict |
|---|---|---|
| source / anchor | `https://go.dev/src/cmd/link/internal/ld/main.go` and `https://go.dev/src/internal/buildcfg/exp.go` (go1.27.3 release tree); `main.go:191-198` (`buildVersion += sep + "X:" + goexperiment`, dash when the version has no `-`, citing go.dev/issue/75953); `exp.go:79-84` baseline `Dwarf5`; `exp.go:157-161` `String()` elides baseline flags | **PASS.** All cited lines are present as quoted. 191-198 is the suffix-construction block; the injection into `runtime.buildVersion` is line 199, outside the range, but the row says "build version" (the variable assigned at 197), not `runtime.buildVersion`, so this is not an overclaim. `exp.go:79-84` spans the platform guard (79) through the baseline `Dwarf5` field (84); the baseline literal itself is 81-89, so the range is tight, not misleading. |
| kind / tier | `code` / `A` | **PASS.** Primary source at the exact release tree, same tier as the other `code` rows (S024, S029). |
| scope | "How a toolchain built with non-default GOEXPERIMENT writes `X:<exp>` into the build version, the separator it uses, and which flags are listed" | **PASS as a path description.** The separator branch and the baseline-relative listing are both shown by the cited lines (193-196, 157-161, 163-190). The only unhedged causal sentence is in `teaches`; see finding W2-S026-1. |
| teaches | "Explains `go1.27.0-X:nodwarf5` as a baseline-relative experiment list after a dash: the `X:` token marks a non-default toolchain build and is not part of the release number." | **One overreach (W2-S026-1).** "baseline-relative experiment list after a dash" and "not part of the release number" are correct (191 seeds from `buildcfg.Version`; 197 appends). "marks a non-default toolchain build" is not entailed by the token. |
| status | `mined` | **PASS.** Registry histogram at this revision: 28 `mined`, 2 `rejected`; S026 is one of the 28, and both `used-by` files cite it. |
| opened / recheck | `2026-10-20` / `on-release` | **PASS by content; date not independently reconstructible.** I can attest only that the quoted bytes are present on 2026-10-20. `on-release` fits an unversioned `/src` URL that tracks the latest release. |
| used-by | knowledge entry, `corpus/lessons/round-17.md` | **PASS.** S026 appears at knowledge line 1 and lessons lines 28, 29, 47, 48. |

## Lesson quotes (`corpus/lessons/round-17.md`, Gate → "Opened sources and located quotes")

- **Line 47:** `https://go.dev/src/cmd/link/internal/ld/main.go, line 197 (go1.27.3)` → `buildVersion += sep + "X:" + goexperiment`. Exact, one contiguous span of line 197, 7 words, location correct.
- **Line 48:** `https://go.dev/src/internal/buildcfg/exp.go, line 158 (go1.27.3)` → `(Experiments in the same state as in the baseline are elided.)`. Exact contiguous substring of line 158, 11 words, location correct.
- Both are under the table's own `≤25 words` header, neither splices wording across lines, and both are code quotes, i.e. the manual `QUALITY #1/#17` route the lesson itself declares (QUALITY #17 excludes code members from machine-gradeable submission). **PASS.**

## Findings

### W2-S026-1 — LOW (calibration) — `corpus/SOURCES.md:32` states a hedged inference as a definition

Row sentence: "the `X:` token marks a non-default toolchain build and is not part of the release number."

Source facts (observation): `buildcfg.Experiment` is initialized from `envOr("GOEXPERIMENT", defaultGOEXPERIMENT)` (`exp.go:31-32`; `envOr` is `internal/buildcfg/cfg.go:52`), and `main.go:192` prints `buildcfg.Experiment.String()`. `GOEXPERIMENT` is a user-settable build-time variable (`cmd/go/internal/help/helpdoc.go:736-741`: "Comma-separated list of toolchain experiments to enable or disable"; `cmd/go/internal/cfg/cfg.go:289-290`: `RawGOEXPERIMENT = envOr("GOEXPERIMENT", buildcfg.DefaultGOEXPERIMENT)`). The official go1.27.3 tree embeds an empty default (`internal/buildcfg/zbootstrap.go:15` sets `defaultGOEXPERIMENT` to the empty string), so a stock toolchain plus `GOEXPERIMENT=nodwarf5` produces the same token as a toolchain built with that non-default embedded default.

Inference: the token proves the link-time experiment configuration differed from the platform baseline; it does not distinguish "the toolchain was built with non-default GOEXPERIMENT" from "the build set GOEXPERIMENT". The w1 census kept that distinction: `CarrierCensusTool.md:51-54` says "consistent with `GOEXPERIMENT=nodwarf5` toolchain builds" and labels "suffix→experiment mapping is inference". The w1 draft row (`w1/draft-sources-rows.md:19`) already states the unhedged form ("an `X:` token marks a non-default toolchain build"), and the integrated row carries it forward.

Impact and blast radius: a future analyst meets `X:nodwarf5` on some other binary and the row invites a toolchain-build attribution that the token alone cannot support. It does **not** affect the observed carriers (both readings remain live), the anchor, the tier, the status, or the lesson quotes.

Smallest fix (one clause): replace "marks a non-default toolchain build" with "records a non-default experiment configuration at link time (embedded toolchain default or a `GOEXPERIMENT` override)".

No other findings.

## Bounded no-finding (checked clean)

- Anchor line numbers and text: `main.go:191-198`, `exp.go:79-84`, `exp.go:157-161` — present exactly as claimed; `exp.go:176` (`strings.ToLower`) plus 182-187 (`"no"+name` for a disabled flag) make `nodwarf5` producible, and `internal/goexperiment/flags.go:103-104` declares `Dwarf5`.
- Quote exactness, contiguity, word bounds and locations: both pass (output above).
- Tier `A`, status `mined`, recheck `on-release`: consistent with the registry's other `code` rows and its 28/2 status split.
- `used-by` claims: real citations in both named files (knowledge line 1; lessons 28, 29, 47, 48).
- Example string: `go1.27.0-X:nodwarf5` is an observed carrier string (`/usr/bin/shfmt`), not an invented one.
- Committed state: `git diff --stat da64646 -- corpus/SOURCES.md corpus/lessons/round-17.md` empty; `git show da64646:corpus/SOURCES.md` line 32 matches the working row.

## Limits

- The go.dev `/src` HTML exposes no version marker to grep (only code text); "go1.27.3 release tree" is corroborated by byte identity with the installed 1.27.3 tarball and by `dl?mode=json` listing 1.27.3 as newest stable, not by a version string printed on the page. [INFERENCE: the unversioned `/src` page serves the latest release.]
- The historical act of opening by the w1 seat on 2026-10-20 is not independently reconstructible; only present-day content was verified.
- The carriers' own build path (distro toolchain default vs a build-time `GOEXPERIMENT`) is not established here; W2-S026-1 is about the registry sentence, not a carrier claim.
- Not checked (outside this assignment): S024/S025/S027/S028/S029/S030 rows and their quotes; the round-17 tools' behavior.
