# AttackSourceRows — advisory review

**Axes:** depth, calibration. Source/data reading only; no admission or runtime verdict.

## Exact missing evidence

At this review snapshot, `corpus/SOURCES.md:29-30` ends the registry with **S023**, the existing Go 1.25 base JSON row. The bounded search of `.ufo/waves/round-16/w1` for `S024|S025|new row|Opened sources|located quote|source row` returned no matches. Thus no proposed new row and matching round-16 author-opening/located-quote record were available to inspect. This is an explicit evidence gap, **not an observed false or nonconforming new row**.

S023 is already round-15 work: `corpus/lessons/round-15.md:33,43`. Reopening it or S003 cannot itself establish a new source acquisition. C1 (`.ufo/waves/round-16/claims.json:6`) does not require a new row.

## Strongest concrete counterexample

S023's frozen anchor is `go1.25.0.json`, `all.Types.runtime.moduledata.Fields[1]`; reading that object yields `Name: pcHeader`, `DataType: *runtime.pcHeader`. It does **not** establish Go 1.24 patch contents or that a selected patch was applied.

The separately opened installed file `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/patchverdiffs/go1.24.6.json.diff:1-3` changes `crypto/tls.buildRetryConfigList.Position` from `$GOROOT/crypto/tls/ech.go:621:6` to `$GOROOT/crypto/tls/ech.go:641:6`. S003's `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java:119-165`, methods `getApiSnapshotJsonFile` and `getPatchVerDiffFile`, separately defines selection and explicitly invokes `jpa.apply(jsonPatch, monitor)`.

**Conditional falsifier:** a row/quote supporting only S023's generic pointer cannot substantiate those patch-content or applied-snapshot claims. Selecting or hashing the diff is not applying it. No available candidate was observed making that overclaim.

## Smallest safe correction

- Reuse **S003** for selector source law and **S023** only within its existing installed-base scope. Preserve their identity and frozen `source/kind/tier/scope/anchor/teaches/opened` cells. Existing-row `used-by` additions should name already-created citing files and receive old→new lesson entries.
- If a new patch-data row is wanted, append the next unused ID only after its author opens the exact source. Record its path, access date and contiguous located quote in round-16 `## Gate`; for this diff, line 1 supplies `@ ["all","Funcs","crypto/tls.buildRetryConfigList","Position"]`. This review's opening is not proof of a different author's opening. Scope tier A to the installed bytes, not compiled execution or target applicability.
- A genuinely incorrect frozen statement needs a new row beginning `supersedes S0NN —`, not an in-place scope/anchor/teaches repair. No new-row quota justifies duplicate authority or expansion credit.

These are fixable provenance issues, not a required depth/calibration tradeoff. Rule anchors: canonical `skills/shokunin/protocol/CORPUS.md:99-118` (located anchors, author opening, quote, immutable cells), `:123-125` (rows are not expansion); prior local practice `corpus/lessons/round-15.md:25-44`.

**Limits:** prospective review of the available snapshot, not an immutable before/after comparison. No builds, tests, checks, target/provider execution, installs or protected-file edits performed. Only this report was written.
