# CriticSourcedClaim — does C2 rest on S024/S025/S026/S029, or are the rows decorative?

Seat: KaidokuR17.CriticSourcedClaim (w2 critic, author-side advisory). Target: the frontier-step
"sourced claim" requirement as C2 states it. Revision: lane HEAD `da64646adcb19c1ede7537b799b8c7d283fe43da`
(`git rev-parse HEAD` → `da64646a…`; `corpus/` is clean against HEAD). Axes: calibration, depth.
Read-only. No installs. Scratch files: `/tmp/kr17csc-bi-1.25.0.go` only.

## Verdict

**C2 still satisfies the protocol, but its "sourced" statement is miscalibrated.** PROTOCOL.md:141-142
asks for one claim "filed as *sourced* — its evidence citing an `S###` row". It does not ask for a new
row. C2's evidence really does rest on reopened S003 and S023: 9 Ghidra-source anchors in the entry body.
That meets the rule. But `claims.json` C2 `"sourced"` says the claim "rests on new SOURCES rows opened
this round (Go debug/buildinfo source/docs; Go release history)". The counterfactual shows otherwise.
Remove S024/S025/S026/S029 from the entry and no body claim loses an anchor. S025 has no load anywhere.
S026 and S029 have none in the entry. S024's only real use goes through a tool built from a different
Go revision. For the entry, these four rows are header-only citations. Severity overall: **medium
(calibration / false provenance), fixable, and not a frontier-step failure.**

## F1 · medium · calibration — the four new rows appear only in the entry header; the body anchors are all S003

Observation, `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md`:

```
$ sed -n '2,133p' $F | grep -o 'S0[0-9][0-9]' | sort | uniq -c
(empty: zero S### tokens outside the line-1 `source:` header)
$ sed -n '2,133p' $F | grep -oE '(GoRttiMapper|GoApiSnapshot|GoBuildInfo|GoVer|TransientProgramProperties)\.java:[0-9-]+|`:[0-9-]+`' | sort | uniq -c
      1 `:158-161`   1 `:162-164`   1 GoApiSnapshot.java:122-126   1 GoBuildInfo.java:488-489
      1 GoRttiMapper.java:170-172   1 GoRttiMapper.java:179-180   1 GoRttiMapper.java:79
      1 GoVer.java:62-81   1 TransientProgramProperties.java:107-110
```

That is 9 S003 anchors. Next, I grepped the entry for the content each new row teaches (`for p in
buildinfo buildinf 'X:' nodwarf experiment GOEXPERIMENT release master upstream 2026-08 2026-10-19
go.dev issue magic time-plausib dash '1\.26'`):

- `experiment`, `GOEXPERIMENT`, `dash`, `release` (outside line 1), `master`, `upstream`, `2026-08`,
  `go.dev` (outside line 1), `magic`, `time-plausib`: **0 hits** in lines 2–133.
- `X:`/`nodwarf`: only the raw strings in the table at `:51` and `:56`. The entry never interprets them.
- `1.26`: only carrier versions and the installed-base statement `:105` ("this installation"). It does
  not mention the upstream master range.

Per-row counterfactual (what the entry loses without the row):

| Row | `teaches` (SOURCES.md) | Body use in entry | Loss if removed |
|---|---|---|---|
| S024 (`SOURCES.md:30`) | reference decoder; version raw incl. `X:`; no magic = no record | `:79-80` magic string and "independent `tools/buildinfo-probe.py` … agrees" | Partial: the magic constant is also in S003 (`Base-src.zip:GoBuildInfo.java:50-53`, "Defined in Go's src/debug/buildinfo/buildinfo.go", `GO_BUILDINF_MAGIC = "\u00ff Go buildinf:"`). Only the probe's independence depends on S024, and see F2. |
| S025 (`:31`) | 1.27.x carriers are time-plausible; dates are lower bounds | none | **none**. I also found no "plausib" claim anywhere in `corpus/`, `SKILL.md`, or `LOG.md` that uses it. Its only appearance is the lesson quote table, `round-17.md:45-46`. |
| S026 (`:32`) | `X:<exp>` is a baseline-relative experiment list, not part of the release number | none. The `go1.27.0-X:nodwarf5 → 1.27.0` mapping comes from Ghidra's `GoVer.parse` regex (`predict.py:12-27` cites `GoVer.java:62-81`, S003) | none in the entry. It is used only by the lesson's S028 rejection rationale, `round-17.md:29`. |
| S029 (`:35`) | released line declares 1.15–1.25; 1.26 is master-only | none. `:31-33` and the table cite the installed `GoRttiMapper.java:79` (S003) | none in the entry. See F3 for the duplication. |

C2 names "Go release history" as a resting row (`claims.json` C2 `sourced`). It is the row with zero load.
w1 `ConnFleetCorpusRules.md:99` (D3) had already recorded "C2 is `sourced` only via those rows". The
integrated entry does not bear that out. The w1 draft `w1/draft-knowledge-r17.md:1` cited only
S003/S023 (+S004 as contrast). Integration added the four new IDs to the header without adding body text
that uses them.

Why the census missed it: CORPUS.md:103 defines `mined` as "cited by ≥1 path in `used-by`". The census
check at CORPUS.md:146-147 only tests that the `used-by` paths exist. A token in the `source:` header
meets both checks, so S024/S025/S026/S029 are `mined` with `used-by` = the entry (`SOURCES.md:30-35`
used-by column) without any body use. That is a fleet-level tradeoff in CORPUS.md, outside this lane's
write scope. Name it for the judge rather than fix it here.

Smallest fix (pick one per row; pre-falsify, so the L1 decides whether this is an in-round edit or an
appended correction under PROTOCOL.md:135-137):
1. Restate C2's sourcing in the round report and lesson Gate: "sourced via reopened S003 (9 body
   anchors) and S023; S024/S026/S029 are context rows; S025 has no load". Drop S025 (and S029 unless (2)
   applies) from the entry's `source:` header and from their `used-by`. If S025 has no other user,
   record it as `queued`, not `mined`, logged in the lesson (CORPUS.md:103,116).
2. To make S026 genuinely load-bearing, add one body sentence:
   "`-X:nodwarf5` is the linker's baseline-relative GOEXPERIMENT suffix (S026 `main.go:191-198`,
   `exp.go:157-161`); Ghidra's `GoVer.parse` drops it (`GoVer.java:64-65`), so the requested version
   equals the release number." This is true at go1.27.3. I checked it locally: `sed -n 191,198p
   ~/.local/opt/go-1.27.3/src/cmd/link/internal/ld/main.go` shows `buildVersion += sep + "X:" +
   goexperiment` with `sep = "-"` when the version has no `-`.

## F2 · low · calibration/provenance — the only S024-dependent tool is built on go1.25.0, and on the no-build-info carrier it took a path S024's revision does not have

Observation:

```
$ sed -n 15,18p .ufo/waves/round-17/tools/buildinfo-probe.py
Source basis: Go `src/debug/buildinfo/buildinfo.go` at tag `go1.25.0`
(…fetched file sha256 332fff28ac2569b76dda2e9d4f25aacc112e12bd8888fca927db0c5156187f45, 599 lines)
```

S024 (`SOURCES.md:30`) pins **go1.27.3**. `SKILL.md:540` registers the probe as "Independent stdlib
reader per S024".

```
$ curl -sSfo /tmp/kr17csc-bi-1.25.0.go https://raw.githubusercontent.com/golang/go/go1.25.0/src/debug/buildinfo/buildinfo.go && sha256sum /tmp/kr17csc-bi-1.25.0.go
332fff28ac2569b76dda2e9d4f25aacc112e12bd8888fca927db0c5156187f45   (matches the probe docstring)
$ diff /tmp/kr17csc-bi-1.25.0.go ~/.local/opt/go-1.27.3/src/debug/buildinfo/buildinfo.go
70c70  (errors.As → errors.AsType; cosmetic)
461,465d460
< 	for _, p := range x.f.Progs {
< 		if p.Type == elf.PT_LOAD && p.Flags&(elf.PF_X|elf.PF_W) == elf.PF_W {
< 			return p.Vaddr, p.Memsz
544,551d538  (Mach-O first-writable-segment fallback removed)
```

go1.27.3's `elfExe.DataStart` no longer has the "first writable non-executable PT_LOAD" fallback. The
probe still has it (`buildinfo-probe.py:162-172`, "Mirror elfExe.DataStart (L455-466)"). On the carrier
behind entry `:78-83`, it takes exactly that path:

```
$ python3 -I -B tools/buildinfo-probe.py <pro-esbuild-0.27.7 carrier, sha256 c638273f…ba14b>
{'found': False, 'search_space': 'first writable non-executable PT_LOAD', 'go_version': None, 'magic_file_offsets': [], 'pointer_format': False}
$ readelf -SW <same> | grep -i 'go\.\|buildinfo'
  [ 7] .go.fipsinfo …          (no .go.buildinfo section)
```

The outcome does not change. `magic_file_offsets: []` is a whole-file scan, and the magic constant is
identical in both revisions (both at L58). S024's own revision also agrees:
`~/.local/opt/go-1.27.3/bin/go version -m <same>` → `…: not a Go executable` (exit 1). Control:
`shfmt` and `containerd-shim` decode through `.go.buildinfo section`, giving `go1.27.0-X:nodwarf5` and
`go1.27.2-X:nodwarf5`, so that path is the same at both revisions. Still, "per S024" is false provenance
for the probe's search-space semantics. The entry also states no retained probe output: `ls
runs/pro-esbuild-0.27.7/` has no probe JSON.

Smallest fix: change `SKILL.md:540` and the probe docstring to "per buildinfo.go go1.25.0 (sha
332fff…); go1.27.3 (S024) drops the ELF/Mach-O writable-segment fallback (diff 461-465, 544-551)".
Alternatively, cite the go1.27.3 `go version -m` result as the S024-revision cross-check for `:79-80`.
The second option is also the one change that makes S024 load-bearing at its pinned revision.

## F3 · low · depth — S029 duplicates S003 and S004; only its releases-feed fact is new

Observation:

```
$ unzip -p …/Base-src.zip ghidra/app/util/bin/format/golang/rtti/GoRttiMapper.java | sha256sum
2415ceba3ea5250774fff51d43f6b22656a83713372f090701a10e49ad581d95
```

This matches S029's tag-file digest (`SOURCES.md:35`), so the S029 tag half is byte-identical to the
installed S003 member. Line 79 is `GoVerRange.parse("1.15-1.25")` in both. The master half is quoted
(`round-17.md:52`) from `commit/385e8cd9….patch`, which is S004's commit (`SOURCES.md:10`). The only
content new to S029 is "newest release in the feed is 12.1.4, 2026-09-21; no 1.27 anywhere". The entry
does not use that fact; the lesson leads update `round-17.md:67` does. Two rows now ground the same tag
bytes, and two ground the same master commit: duplicate authorities.

Smallest fix: narrow S029's `scope`/`teaches` to the release-feed and tag-list status fact, citing
S003/S004 for the range strings, and set `used-by` to the lesson only.

## Strongest counterexamples I tested against my thesis (none overturn it)

- *"Header `source:` citation is the corpus convention for grounding."* QUALITY #1
  (`corpus/QUALITY.md:11`) asks for a resolvable source per claim. A header token supports no particular
  claim if no claim uses the row's content. The w1 draft shows the body was complete without the four
  rows.
- *"S026 grounds the out-of-range prediction for the `X:` carriers."* No. `predict.py:12-27,114`
  implements Ghidra's regex strip (S003). The prediction would be identical if Go defined the suffix
  differently.
- *"S024 grounds the no-build-info route."* Only partly. The REA `build_info: null` result and S003's
  magic constant carry the claim, and the probe follows a different Go revision (F2).

## Checked, no finding

- S024 anchors at go1.27.3: `:58` magic, `:97` `bi.GoVersion = vers`, `:200-202` flags, `:224-237`
  inline decode and `:262-268` framing are present in the local tree (`sha256 5e4064ef…c097`).
- S026 anchors `main.go:191-198` and `exp.go:79-84`/`:157-161` match the local go1.27.3 tree verbatim.
- C2 still meets PROTOCOL.md:141-142 through S003/S023. This is not a frontier-step failure; the
  defect is the stated reliance.

Impacted axes: calibration (C2 `sourced` statement, `used-by`/`mined` status, SKILL `per S024`); depth
(the new rows add no grounded claim to the entry).
