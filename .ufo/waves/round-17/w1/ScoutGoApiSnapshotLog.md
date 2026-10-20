# Scout: `Using Go API snapshot for %s` label semantics

scope: read-only source/data inspection plus two already-retained pilot logs. No REA
analyze/search/decompile, no Ghidra, no carrier execution, no installs. Source extracted to
`/tmp/basesrc_all` from
`/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip`.
Member line numbers below are archive-absolute; the r16 quote at `GoApiSnapshot.java:122`
reproduces exactly in this extraction, so the numbering matches the cited member.

## Answer

**The logged label is the requested `GoVer`, not the selected base or diff file version.**

Anchor: `Base-src.zip!ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:163`

```java
Msg.info(GoApiSnapshot.class, "Using Go API snapshot for %s".formatted(goVer));
```

`goVer` there is the parameter of `getPatchVerDiffFile(GoVer goVer)` (line 148), forwarded
unchanged from `getApiSnapshotJsonFile`'s `getPatchVerDiffFile(goVer)` at line 128, which in
turn received the `get(...)` parameter (line 102) that `GoRttiMapper` built from
`buildInfo.getGoVer()` (`GoRttiMapper.java:165,176`). The mutable selection variable is the
local `patchVer` (line 151); `baseVer` exists only as `goVer.withPatch(0)` (line 122). Neither
is ever formatted into this message.

The message never carries file identity: the base name is constructed as
`go<M.m.0>.json` (122, 168-171), the selected diff as
`patchverdiffs/go<M.m.p>.json.diff` (152-153, 168-171), and neither path, name, nor digest is
logged. What the line does attest is only the branch it sits in.

## Branch table (source-anchored; INFERENCE where no log was retained)

`getPatchVerDiffFile` (148-166):

- exact diff found for the requested patch: `patchVer == goVer` -> **INFO 163**
  (`... for <requested>`).
- no diff found and requested patch > 0: loop walks down (152-156), `patchVer != goVer` ->
  **WARN 159-160** `Falling back from <requested> to <selected> for Go API snapshot`.
- requested patch == 0: the loop never executes (condition `patchVer.getPatch() > 0`),
  `patchDiffFile` stays null (130-131) and the raw base provider is returned -> **INFO 163**
  even though no diff was ever consulted (`... for <M.m.0>`).

Consequences, in order of calibration value:

1. **The same info string covers an unpatched resource file and an in-memory base+diff
   composition.** For `1.23.0` it is the former; for `1.24.6` with a diff installed it is the
   latter. Nothing in the message distinguishes them.
2. **On fallback the info line is absent and the warn is the only accurate record.** The
   object is still seeded with the requested version: `read(is, archSearchOrder, goVer)`
   (line 111) -> constructor `this.ver = ver` (494-495) -> `getVer()` (499-501). So
   `GoRttiMapper.java:178-180` then logs `Using Go API snapshot for version <requested>` in
   *every* non-missing-base case, including fallback, where the bytes are base.0 + an older
   diff. That line is a request echo, not artifact evidence.
3. **Arch-bucket selection is entirely unlogged.** Order is built at 108-109; `read` keeps
   only those buckets (205-240); `GoApiSnapshot.isInvalid()` is `arches.isEmpty()` (503) and
   feeds the bootstrap branch (`GoRttiMapper.java:356-361`). A valid label therefore does not
   prove the carrier's `os/arch` bucket was retained — only that `getVer()` is valid, which
   the mapper's guard tests separately (178).
4. **The info precedes patch application.** It is emitted at line 128, before the derived
   provider is even constructed (133-145). A diff that fails to parse/apply throws an
   `IOException` from the provider read inside `get` (105-107); the mapper catches only
   `CancelledException` (183-185). No line reports "exact diff present but apply failed".
5. **Label format is numeric-only.** `GoBuildInfo.java:488-489` strips the leading `go`;
   `GoVer.parse` cuts at the first non-`[.0-9]` character (`GoVer.java:62-65`);
   `toString` prints `M.m.p` or `M.m` (`GoVer.java:154-160`). A log grep for `go1.23.12` will
   not match the label; `1.22.8 X:rangefunc` collapses to `1.22.8`; a `devel` string is
   invalid and becomes `BootstrapInfoException` with the raw string (`GoRttiMapper.java:166-168`).

## Observed pilot confirmation

Pilot log SHA-256 values match `pilot/SHA256SUMS` (checked this round):
`shfmt-log/ghidra.log` = `aaf677ed...b5255`, `esbuild-0.25.12-log/ghidra.log` =
`f6b61152...d89a7`.

esbuild, go1.23.12 (OBSERVED), `pilot/esbuild-0.25.12-log/ghidra.log`:

- `:62` INFO (GoRttiMapper) `Reading Go binary info: target-bab29b2ca7a9.bin`
- `:63` INFO (**GoApiSnapshot**) `Using Go API snapshot for 1.23.12`
- `:64` INFO (**GoRttiMapper**) `Using Go API snapshot for version 1.23.12`
- `:67` INFO (GolangSymbolAnalyzer) `Go version 1.23.12`
- no `Falling back` line; one `Reading Go binary info`.

`w1/selection-1.23.12.json` (r16 model, `status: exact_diff`) names base
`go1.23.0.json` (sha256 `3b1d79...`) and diff `patchverdiffs/go1.23.12.json.diff`
(`e1fdbc...`). So the observed label equals the request and equals the diff-embedded version,
while the base file version is `1.23.0` and appears nowhere in the log.

shfmt, go1.27.0 (OBSERVED), `pilot/shfmt-log/ghidra.log`:

- `:83` ERROR (GoRttiMapper) `Untested Go version [1.27.0]`
- `:84` WARN (GoRttiMapper) `Missing Go bootstrap type info, unable to extract Go RTTI info.`
- `:85` ERROR (GolangSymbolAnalyzer) `Go symbol analyzer error: unable to get GoRttiMapper`
- `:86-89` second identical block for the string analyzer
- **no** `Using Go API snapshot` line of either form.

This is exactly the `missing_base` path: no `go1.27.0.json` -> `getApiSnapshotJsonFile`
returns null (124-126) -> `EMPTY` (242, ver `INVALID`) -> mapper guard `!getVer().isInvalid()`
suppresses 180. The duplicate block is `GoRttiMapper.java:114-116` catching the
`BootstrapInfoException` thrown by `init()` (356-361) and logging its message per analyzer;
the second `Reading Go binary info` at `:86` is the observed evidence that no mapper instance
was cached after the failure (supplier returns null, 125).

The WARN at `:84` carries **no version**, and that is source-correct: the literal at
`GoRttiMapper.java:359` has no format specifier while `.formatted(goVer)` is applied at
360. The only version on that failing path is the preceding `Untested Go version [...]`
ERROR (171). A log consumer cannot recover the requested version from the bootstrap-missing
line.

## Relation to r16 reject at `corpus/lessons/round-16.md:21`

CONFIRMED, with a refinement the reject wording does not yet distinguish:

- Object label is request-side in all cases (111 -> 494-495 -> 499), so "the label is not
  file identity" holds.
- In the **exact_diff** branch the label numerically coincides with the selected diff's
  embedded version, because the diff name is derived from `patchVer` (152-153) and the info
  branch implies `patchVer == goVer` (158). The coincidence is branch-conditional, not an
  authentication: no base name, bucket set, or apply outcome is carried.
- In the **fallback_diff** branch the last surviving "Using ..." text (180) is *wrong about
  content* by construction, and the warn (159-160) is the only accurate record. Any
  prediction table that compares a single label to `selection.json` will pass fallback cases
  incorrectly.

## Round-17 contract calibration (`contract.md`, `log-extract.py` section)

Observed spec gaps, suggested for L1 integration (I did not edit the contract):

1. `snapshot_labels` drawn from both message forms yields `["1.23.12","1.23.12"]` on
   exact_diff: one request echo counted twice, never two artifact confirmations. The
   `for version X` form should be labelled request-echo, not evidence of loaded bytes.
2. The fallback warn (`Falling back from X to Y`) is outside `snapshot_labels` and has no
   field at all. Proposed `fallbacks: [{requested, selected}]`; `snapshot_loaded` should be
   withheld or annotated when a fallback exists, since the bytes target Y while every label
   reads X.
3. `classification: snapshot_loaded` is derivable without any proof that the carrier's
   bucket matched (503 vs 178).
4. `missing_bootstrap` detection on the literal `Missing Go bootstrap type info` is correct
   (359, observed at shfmt `:84`), but it cannot yield a version; only `go_version_logged`
   (`GolangSymbolAnalyzer.java:139`) and `untested_versions` (`GoRttiMapper.java:171`) can.
5. `GoApiSnapshot.java:139` monitor text `Patching Go API snapshot <baseVer> -> <goVer>`
   always names the *requested* target, so on a fallback-to-older-diff it mislabels the
   applied data. It was not present in either pilot log (`grep 'Patching Go API snapshot'`
   returns nothing), consistent with TaskMonitor text not reaching `ghidra.log`; treat it as
   unusable for artifact attribution unless a run shows otherwise.

## Predictions for the C2 carriers (INFERENCE, pending L1 runs)

| carrier | r16 status (`w1/selection-*.json`) | predicted Msg signature |
|---|---|---|
| esbuild go1.23.12 | exact_diff | OBSERVED above: 163, 180, analyzer 139; no warn |
| esbuild go1.20.12 | exact_diff (base `go1.20.0.json`, diff `go1.20.12` present) | same two-line label pair with `1.20.12` + `Go version 1.20.12` |
| shfmt go1.27.0 | missing_base | OBSERVED above: `Untested Go version [1.27.0]` + version-less bootstrap warn, no labels |
| hypothetical go1.25.1+ | base_only, patch>0, no 1.25 diffs installed (max installed diff is `go1.24.6`) | warn `Falling back from 1.25.1 to 1.25.0`, then mapper 180 with `1.25.1`; no 163 |
| hypothetical go1.24.7 | fallback_diff (diffs stop at `go1.24.6`) | warn `from 1.24.7 to 1.24.6`; mapper 180 `1.24.7`; monitor text (if ever captured) would claim `1.24.0 -> 1.24.7` while applying the `1.24.6` diff |

`w1/selection.py` status `base_only` conflates patch==0 (info 163) with patch>0-no-diff
(warn 159), so a log prediction keyed on status alone is ambiguous; request patch must be
included.

## Remaining unknowns

- No retained fallback_diff or patch==0 log: those two branches are source-derived only.
- `Base-src.zip` member was not authenticated against the shipped `Base.jar`/compiled classes;
  no class-file comparison attempted, so compiled behavior is inferred from source and the
  two pilot logs.
- Whether `TaskMonitor` text can ever reach a retained log is unresolved; not observed here.
- Lazy vs eager evaluation of the derived `ByteProvider` producer was not inspected
  (`FileSystemService` detail); the ordering claim ("info before construction/apply") does not
  depend on it.
