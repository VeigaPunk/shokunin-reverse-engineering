# CriticC3 — round 18, C3 (Swiss-map minimal pair) attack

Seat: author-side advisory critic. I was read-only on the lane and wrote only this file. Throwaway scratch lives outside the lane:
`/tmp/kr18c3/{scan.py,walk.py,*.json}` (byte scanners, stdlib only) and `/tmp/tmp.T82T0ZAJv2/` (unzipped Ghidra sources). The L1 may delete both.
I executed no carrier and ran no REA or Ghidra. I installed no tools.

## Headline (counterexample)

**The eight carriers as built cannot move aether off INFERENCE in either direction.** I emulated the carriers from their bytes and from Ghidra 12.1.4 source.
- Under H1 (Ghidra reads Swiss map types through `OldMapType`), every carrier is predicted to show no `Go analysis failure` and no EOF.
- Under H0 (no misread), the prediction is the same.
- No log-visible field separates the two hypotheses on any of the eight carriers.

An 8/8 `compare` match is therefore expected under both hypotheses. That result says nothing about the mechanism. With the current claim text (`claims.json:27`, "moves … to replayed-confirmed or replayed-refuted"), an 8/8 match would push the result toward a false "confirmed". A swiss-methods carrier that does not fail would push it toward a false "refuted".

## Evidence

### E1 — "methods" is the wrong factor. Methods are never read under the misread.
- **OBSERVATION (source).** The compiler gives a type an UncommonType whenever the type is named, with or without methods: `go-1.24.6/src/cmd/compile/internal/reflectdata/reflect.go:60-64` (`if t.Sym() == nil && len(methods(t)) == 0 { return 0 }`).
- **OBSERVATION (source).** Ghidra reads the uncommon block at the end of its own struct: `GoType.java:144-149` (`readStructure(GoUncommonType.class, context.getStructureEnd())`).
- **OBSERVATION (data).** That struct is `OldMapType`. The snapshot aliases are `go1.24.0.json` and `go1.25.0.json` `Types/runtime.maptype → internal/abi.OldMapType`. `GoMapType.java:32-34` binds `runtime.maptype` / `internal/abi.OldMapType` and has no Swiss binding.
- **OBSERVATION (source).** In both toolchains, `SwissMapType` places `SlotSize` at +0x58 and `ElemOff` at +0x60 (`go-1.24.6` and `go-1.25.0` `src/internal/abi/map_swiss.go:32-43`; `OldMapType` is at `map_noswiss.go:25-36`). Ghidra's misread uncommon block is therefore:
  - `PkgPath = low32(SlotSize)`
  - `Mcount = Xcount = 0`, the high half of `SlotSize`
  - `Moff = ElemOff`
- **OBSERVATION (bytes).** My scan agrees for every named Swiss map type. In the swiss-methods carriers, `main.Counts` has true `mcount=2`, but Ghidra reads `mcount=0, pkgpath=24` (output table below). On aether, `*dbus.sigSet` has 4 methods and `*http.Header` has 13, yet Ghidra reads `mcount=0` for both.
- **INFERENCE.** The trigger is (named Swiss map type) × (`SlotSize` = N) × (whatever bytes sit at `types+N`). Methods play no part. The round-17 seat already found this (`.ufo/waves/round-17/w2/CriticAetherUnknown.md:21,61-62,134,140-144`). Its replay recipe asked for a carrier whose `SlotSize` lands on a HAS_PKGPATH name. The round-18 recipe instead used `type Counts map[string]int` (`W18/carriers/src/methods/main.go:13`), which has `SlotSize` 24. That is the size r17 had already classified as **silent** (`CriticAetherUnknown.md:134`).

### E2 — The emulator reproduces aether's EOF pair exactly, and predicts silence for the pair
- **OBSERVATION (aether).** `types = 0x954020`. There are 7 uncommon Swiss map types. The 3 with `SlotSize` 40 are `textproto.MIMEHeader`, `url.Values` and `http.Header`. For them:
  - the GoName at `types+0x28` has flags `0x6e` (HAS_TAG and HAS_PKGPATH);
  - its chained `pkgPath` is `0x780100`, so the name sits at `0x10d4120`;
  - that name's varint length is `111938854` and its data starts at `17645861`.

  This is exactly the r17 log pair (`.ufo/waves/round-17/runs/pro-aether/logs/rea-ghidra-J5bcRT/ghidra.log:177`). The other 4 types, with `SlotSize` 24 or 32, read harmless names (flags `0x1` or `0x0`).
- **OBSERVATION (pair).** Only the `*-methods` carriers have an uncommon map type: one, `main.Counts`. The `*-nomethods` carriers have 0, and so does notesmd-cli.

  | carrier | Ghidra uncommon read | name at `types+pkgpath` | outcome |
  |---|---|---|---|
  | s1246-swiss-methods | `pkgpath=24, mcount=0` | `0x495018`: flags `0x01`, len 116, in `.rodata` | no chain → no EOF |
  | s1250-swiss-methods | `pkgpath=24, mcount=0` | `0x49b018`: flags `0x01`, len 115 | no EOF |
  | s12x0-noswiss-methods | equals the true read (`pkgpath` 579/561 → "main", len 4) | — | no misread |
- **OBSERVATION (Ghidra discovery count).** My walk mirrors `GoTypeManager.java:96-145`: typelinks plus itabs, recursing as each `discoverGoTypes` does, without PtrToThis. On aether it gives **5927** indexed types, which equals the logged `Found 6115` minus `Discovered 188 unindexed` (`observation.json` go_lines 94-95).

  The H1 and H0 walks give identical counts on all 10 binaries. The method types are reachable some other way, so `Found N Go types` does not discriminate either.
- **INFERENCE (log-invisible discriminator).** Under H1, the swiss-methods `main.Counts` namespace becomes a 116- or 115-byte control-character string:
  - `GoType.java:187-188` takes it from `getPackagePathString()`;
  - `MarkupSession.java:221-225` creates the namespace unsanitized;
  - `SymbolUtilities.validateName` rejects control characters;
  - the resulting `InvalidInputException` is caught at `MarkupSession.java:234-235` and becomes a **Golang WARNING bookmark**, not a log line.

  I did not verify that `getOrCreateNameSpace` calls `validateName`. These are program-DB facts that the retained `ghidra.log` never sees.

### E3 — Calibration acceptance lets an overfit or trivial emulator pass
- The contract's acceptance (`contract.md:119-120`) needs only two things: aether `predicted_eof_reads` **contains** the pair, and notesmd-cli predicts `false`.
- notesmd-cli has **0** uncommon map types, so it never exercises the misread branch. Its "false" is vacuous.
- Two broken emulators pass both checks:
  - **(a)** "fail iff any named Swiss map type exists". It predicts failure on both swiss-methods carriers, which the bytes contradict (E2).
  - **(b)** a hard-coded pair.
- "contains" also allows spurious extra pairs. Ghidra aborts at the first throw (`GolangSymbolAnalyzer.java:181-183`), and the r17 log shows exactly one EOF line (`:177`).
- The swiss-methods carriers are the **first held-out case of "misread but silent"**. They test only the negative branch. They are worth keeping as calibration negatives, but they are not a replay.

### E4 — The noswiss control is valid for routing but non-diagnostic here
- **OBSERVATION.** `go version -m` reports `go1.2x.y X:noswissmap` and `build GOEXPERIMENT=noswissmap` for the noswiss carriers (commands below).
- **OBSERVATION (source).** `GoVer.java:63-65` strips `[^.0-9].*$` ("handle extra info … `1.22.8 X:rangefunc`"). Both siblings therefore select the same snapshot.
- **OBSERVATION (data).** `patchverdiffs` has `go1.24.6.json.diff`, so 1.24.6 has an exact patch, and 1.25.0 is a base. No 1.24.x or 1.25.x diff mentions maptype: the grep hits only 1.21.x and 1.23.x.
- So the controls differ in the true layout only. On the noswiss carriers the emulated Ghidra read equals the true read. That makes them valid "correct read" controls.
- **Confound (OBSERVATION).** The siblings are not byte-minimal:
  - type counts differ (761 vs 768, 792 vs 799);
  - the types base shifts (`0x494000` vs `0x495000`);
  - the head of the types region differs between versions: `types+0x28` is a HAS_PKGPATH name in s1246 but `flags 0x61`, no pkgpath, in s1250.

  Any EOF effect is a byte coincidence of each binary's layout, so the version factor is confounded with layout.
- **Robustness (OBSERVATION).** The contract derives the "true kind" from the `GOEXPERIMENT` build setting. A byte witness agrees with it and does not depend on build metadata:
  - `map.group[` appears in swiss carriers and aether (14 hits) and in no noswiss carrier;
  - `map.bucket[` appears only in noswiss carriers.

### E5 — Real-world generality
- The carriers are tiny: about 760–800 types, 11–12 maps, at most 1 named map. aether has 5927 types, 152 maps and 7 named maps.
- Real binaries that import `net/http` or `net/url` carry `http.Header` and `url.Values`, both `map[string][]string` with `SlotSize` 40. Each such binary is its own coin flip on what lies at `types+0x28`.
- **Feasibility (OBSERVATION).** I swept `SlotSize` 8..128 on the current swiss carriers:
  - s1246: every HAS_PKGPATH chain (N = 40, 80, 96, 104, 112, 120) points to **unmapped** memory;
  - s1250: N = 16 is unmapped and N = 40 is silent;
  - none reaches a mapped overrun like aether's.
- **INFERENCE.** An unmapped chain raises an exception class I have not established; it is not necessarily `Unable to read past EOF`. The emulator must report it as `unknown`, not as a prediction.

## Impacted axes
- **depth:** the claim as worded (`claims.json:26-27`) overstates what the pair can show.
- **calibration:** the acceptance in E3 admits overfit emulators, and the confirm/refute dichotomy has no "unresolved" state.
- **operability:** without a frozen verdict rule, a throughput metric ("0 → 8 compared, match or not") can be read as a mechanism verdict.

## Pre-registered decision rule (freeze with the predictions)

Freeze, per carrier and in Git before any run, a per-type record for every uncommon map type: type VA, `SlotSize`, the Ghidra-read uncommon tuple, and a chain class. The chain class is one of:
- `silent` (no HAS_PKGPATH);
- `eof(A,B)` (the chained name is mapped and its data overruns);
- `unknown` (the chain is unmapped or unreadable);
- `n/a` (noswiss).

Also freeze two carrier-level predictions, `H1_outcome` and `H0_outcome` (H0 means no map-path failure). The diagnostic set is **D = {carriers where H1_outcome ≠ H0_outcome on a log field}**.

**G0 — calibration gate.** If any check fails, C3 is `unresolved (tool)` and no mechanism verdict is given.
1. aether: exactly 7 uncommon maps (3 `eof`, 4 `silent`), and `predicted_eof_reads == [[17645861, 111938854]]` by exact equality.
2. notesmd-cli: `uncommon_map_types == 0`, recorded as a vacuous negative.
3. aether indexed-type count: 5927.

**G1 — binding gate.** The carrier is unobserved, and not counted, unless all of these hold:
- the log sha is bound to its run;
- the carrier sha equals SHA256SUMS;
- the prediction commit is an ancestor of the run.

**Per carrier:** `match` iff the observed analyzer errors, the `eof_reads` list and the route lines equal the frozen H1 prediction exactly. Report the per-carrier match/mismatch count separately as a **throughput/calibration** number. It is never a mechanism verdict.

**Verdict:**
- **replayed-confirmed:** |D| ≥ 1, AND every D carrier shows its exact H1 EOF pair, AND every non-D carrier matches, AND each D carrier's noswiss sibling shows no map-path failure.
- **replayed-refuted:** any D carrier shows its H0 outcome; OR any noswiss carrier fails through a map-type GoName chain; OR any swiss carrier fails with an EOF pair the emulator did not predict.
- **unresolved:** everything else, including **|D| = 0**, any D carrier classed `unknown`, or a G0/G1 failure. On the current eight carriers the verdict is fixed in advance: **unresolved — non-diagnostic** even at 8/8 match. aether stays INFERENCE, now with the static chain replication of E2.

## Smallest safe corrections (L1-owned; ordered by cost)
1. **Reword C3.** Replace "method-carrying map types misread their uncommon/method data" with "named Swiss map types misread their UncommonType (`PkgPath` = `SlotSize`, `Mcount` = 0)". Add the `unresolved` state to `claims.json:27`.
2. **Tighten acceptance.** In `contract.md:119-120`, use exact equality instead of "contains"; require per-type records and the aether 3/4 split; add the swiss-methods carriers as held-out silent negatives; emit `unknown` for unmapped chains.
3. **Make D non-empty** with a pre-registered selection rule. Two options:
   - (a) The L1 builds `type V map[string]T` variants that sweep `SlotSize`. Before any run, the emulator selects, by a frozen rule, the first variant whose chain is `eof(A,B)`, plus its noswiss sibling. Feasibility is not guaranteed (E5).
   - (b) Use the real-world census: any 1.24/1.25 host binary with `http.Header` or `url.Values` that the emulator classes `eof`.
   If neither yields a D carrier, freeze C3's depth delta as "static replication plus calibration negatives", not replay.
4. **Optionally, a program-DB observable.** Golang WARNING bookmarks or missing `main.Counts___map_type_methods` labels would discriminate on the current pair (E2, INFERENCE). This needs an REA query beyond the retained log, run in the L1's single analysis pass.
5. **Add the byte-level layout witness** to the swiss-misread `true_kind` (E4).

## Commands (exit codes as observed)
- `cd …/round-18/carriers && cat -n build.sh src/*/go.mod src/*/main.go; ls …/kaidoku-r18/carriers; cat SHA256SUMS` → exit 0
- `cd ~/.local/share/kaidoku-r18/carriers && sha256sum -c SHA256SUMS` → 8× OK, exit 0
- `for f in carriers/s1* /usr/bin/aether ~/.local/bin/notesmd-cli; do ~/.local/opt/go-1.27.3/bin/go version -m $f | grep …; done` → each exit 0 (reads files only)
- `sha256sum /usr/bin/aether ~/.local/bin/notesmd-cli` → `06c91f55…006e`, `412dc532…802d`, exit 0. `grep -c` of each digest in its r17 `receipt.json` → 4 and 4.
- `unzip -q Base-src.zip 'ghidra/app/util/bin/format/golang/*' …` and `sed`/`grep` reads of `GoType`, `GoMapType`, `GoName`, `GoUncommonType`, `GoTypeManager`, `GoVer`, `MarkupSession`, `GolangSymbolAnalyzer`; `SymbolUtilities` from `SoftwareModeling-src.zip` → exit 0
- `python3 (snapshot JSON walk)` → `runtime.maptype → internal/abi.OldMapType` in go1.24.0.json and go1.25.0.json, exit 0
- `python3 -I -B /tmp/kr18c3/scan.py /usr/bin/aether swiss` → exit 0 (7 uncommon maps)
- `python3 -I -B /tmp/kr18c3/scan.py <each carrier> swiss|old` → 8× exit 0; notesmd → exit 0 (0 uncommon)
- slot sweep (`python3 -I -B -` heredoc reusing scan.py, with the tag varint fixed) → exit 0; aether N=40 → chain `0x780100` → len `111938854`, data `17645861`
- `python3 -I -B /tmp/kr18c3/walk.py <10 binaries>` → 10× exit 0; aether H1 = H0 = 5927
- `ls patchverdiffs | grep -E "go1\.2[45]\."` → go1.24.1–1.24.6 only, exit 0; `grep -l -i maptype patchverdiffs/*` → 1.21.x and 1.23.x only
- `grep -c -a 'map.group\['` / `'map.bucket\['` → swiss 1/0, noswiss 0/1, aether 14/0
