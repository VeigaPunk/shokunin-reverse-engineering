# W2 KnowledgeMechanism: C3 vet identity and offset audit

Seat `KaidokuR19.KnowledgeMechanism-3` (reviewer, author-side, not an outside verifier). Scope: the
mechanism and identity claims in `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md`,
checked against frozen `per_type[144]`, the raw vet log, the carrier bytes and Ghidra 12.1.4 source.

**Revisions.** At dispatch `refs/heads/main` was `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`. My
clone is based there. During the review, main moved to `279e8b19c51658bfd05b9e31a1c0894ab2e70537`
(commit time 16:15:31 -03). I rechecked it at 16:38:34 -03. Between the two tips:

- `predictions/`, `runs/` and `round-18/tools/swiss-misread.py` have an empty diff.
- The entry gained lines 48-53, which add vet's `analyze.json` Evidence.

Entry line numbers below refer to `279e8b1`. Frozen artifacts refer to `a1140e7`; their blobs are
identical at `279e8b1`. LANE = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`; W19 =
`LANE/.ufo/waves/round-19`.

**Bottom line.**

- Every exact offset and value the entry quotes from `per_type[144]` reproduces from the carrier
  bytes with an independent decoder, and the frozen emulator output reproduces byte-for-byte.
- The entry correctly labels the descriptor identity as inference.
- Three explanations around that link are miscalibrated:
  - the abort story for the walk index;
  - the "stronger full-list prediction" framing;
  - an unpinned count command that already returns 16, not 8, in the working tree.
- The type label also needs precision.

## Findings by severity

### F1 (Medium, calibration/depth): the walk index 1801722468838924630 is an emulator artifact, not a read Ghidra skipped by aborting

Entry claims:

- `:19` calls it the "walk index shared by both hypotheses".
- `:36` says "the analyzer aborts before all candidate emulator reads are observed". It labels this
  as INFERENCE but offers it as the explanation for the full-list mismatch.

Observations (carrier bytes, frozen JSON, emulator instrumented in my clone, source unchanged):

- The frozen walk path is in `predictions/swiss-misread/t1250-vet.json:2690-2729`. The trace below
  maps it to addresses and names. The trace adds address wrappers only.
  - `*unitchecker.result` 0x73c1a0
  - → `unitchecker.result` 0x7874a0
  - → `*analysis.Analyzer` 0x75c460
  - → `analysis.Analyzer` 0x7a27e0
  - → `func(*analysis.Pass) (interface {}, error)` 0x759d80
  - → `*analysis.Pass` 0x76cf80
  - → method type `func(token.Pos, string, ...interface {})` 0x759140, with InCount=3 and
    OutCount=0x8000
- OutCount 0x8000 means the variadic bit is set and there are zero results. Param slots 0-2 are
  0x758500, 0x74ae40 and 0x744fe0. Slots 3-6 are 0. Slot 7 = 0x1901010a1afbe156 =
  **1801722468838924630**.
- The emulator counts `in_count + out_count` without a mask, at `.ufo/waves/round-18/tools/swiss-misread.py:939`
  and `:1047-1048`. That gives 32771 params, and it reads and marks slot 7 at `:946-948`.
- Ghidra masks the bit: `GoFuncType.java:79,86` (`outCount & 0x7fff`), giving a count of 3.
- Ghidra also resolves params through `getTypeUnchecked` (`GoFuncType.java:106-110`), which
  returns null on IOException (`GoTypeManager.java:639-646`).

Inference:

- Ghidra 12.1.4 never performs the read that yields 1801722468838924630, under either hypothesis.
  "Shared by both hypotheses" is true of the emulator only.
- An abort cannot explain the index's absence even inside the emulator's own ordering model. The
  walk failure's top-level type 0x73c1a0 sorts before valueMap's reacher 0x73f4a0 and before the map
  0x76eb80 (VA-sorted walk at `swiss-misread.py:1316-1329`), so it would have been the *first*
  failure, not a later one.

Mutation M1 (post-hoc diagnostic, built after seeing the log; **not a prediction**):

- The only change is masking `0x7FFF` at `:939` and `:1047-1048`. With it, vet's walk moves:
  - H1 first failure = `invalid_index 13902080` at `type@0x73f4a0 → elem`;
  - H0 walk = none;
  - H1 list = `[13902080, 852107777]`;
  - H0 list = `[]`.
- M1 survives the emulator's own `--selftest` (`SELFTEST: CLEAN cases=15`). No selftest fixture
  covers variadic function types.

Suggested correction: in `:19`, call 1801722468838924630 an emulator walk artifact (unmasked
variadic OutCount), not a shared-hypothesis read. In `:36`, keep the abort explanation only for
852107777. Callers repeating the "first of several candidate reads" framing: `SKILL.md:613-614`.

### F2 (Medium, calibration): a full-list match was unobservable by construction

Entry `:36` calls the full-list compare "the stronger full-list prediction … falsified". `SKILL.md:609`,
`SCORECARD.md:2495`, `LOG.md:2239` and `corpus/lessons/round-19.md:118-121` repeat that framing.

Observation:

- `GolangSymbolAnalyzer.java:144-184` wraps `recoverGhidraDataTypes`, `markupGoTypes` and all later
  Go markup in one `try`. At the first IOException it logs "Go analysis failure" (`:181-183`) and
  returns false.
- The vet log has exactly 1 `ERROR` line (`ghidra.log:186`) and exactly 1 `Invalid index` (`:229`).
  The untracked pass 2 shows the same.

Inference:

- One run can log at most one index. Any frozen expectation with two or more indices therefore
  makes compare exit 1 regardless of the mechanism. This is the case for
  `predictions/t1250-vet.prediction.json:48-51` and `compare.json:51-57`.
- The compare-1 result carries no information against H1; the decision-table row "vet compare
  exit 1" (`:60`) is a test-design limit, not evidence.
- Of the three listed indices:
  - 852107777 is consistent with abort order (inference). The pointer types `*types.opPredicates`
    0x73f5e0 and `*types.nodeSet` 0x75c160 sort after 0x73f4a0.
  - 1801722468838924630 is the F1 artifact.

### F3 (Medium, freshness): the count command already returns 16, and "one pass" is going stale

Entry `:34` says "Count command (from the lane): `find .ufo/waves/round-19/runs -name compare.json | wc -l` → 8".
`SCORECARD.md:2495` uses the same command.

Observation at 16:3x -03:

- In LANE it returns **16**. `git ls-tree` at main still counts 8.
- The cause is the untracked `W19/runs/pass2/`, a second full pass:
  - run log 16:22:08-16:31:01 -03;
  - producer `branch_tip` = `279e8b1`;
  - vet compare=1 and aggregate exit=1;
  - vet log `Invalid index: 13902080` at the same lines 186/229/243;
  - same MD5 at `:59`;
  - 7 controls with 0 Go analysis failures.
- The uncommitted `claims.json` working-tree diff adds an amendment key `"pass2"` that plans to keep
  this pass.

Consequences:

- The entry's "Observations (one pass)" (`:21`) and "one pass" (`:64`) become false once pass 2 is
  integrated.
- The count rule would double-count labels.

Pinned alternatives:

- `git ls-tree -r --name-only <rev> -- .ufo/waves/round-19/runs | grep -c '^\.ufo/waves/round-19/runs/t1250-[a-z]*/compare\.json$'`
  gives 8.
- `find .ufo/waves/round-19/runs -mindepth 2 -maxdepth 2 -name compare.json` is the working-tree
  form.

Pass 2 shows determinism: the same bytes, Ghidra, REA and frozen rule give the same result. It is
not independent replication.

### F4 (Low, calibration of identity wording): `*types.valueMap` labels two descriptors, and the log's top-level item is probably the pointer

Observation (bytes):

- Descriptor 7793536 (0x76eb80) has Kind 21 (map), TFlag 7 (Uncommon|ExtraStar|Named) and Str 47849,
  which decodes to `"*types.valueMap"`.
- Go-level, it is the named map `go/types.valueMap`: `map[any][]valueType`
  (`/home/vgpnk/.local/opt/go-1.25.0/src/go/types/stmt.go:230`).
- Its PtrToThis is 119968, giving the descriptor 0x73f4a0: Kind 22 (pointer), TFlag 8, and the
  **same** Str 47849. That is the literal Go type `*types.valueMap`.
- A discovery-independent scan of `[types, etypes)` finds only one single-object referrer of the map
  (ptr/slice/array/chan elem, or map key/elem/group): that pointer.

Observation (log):

- The stack has exactly three `StructureMappingInfo.lambda$createMarkupFuncFromGetter$4` frames
  (`ghidra.log:194,198,202`).
- It has one `FieldMappingInfo.lambda$makeMarkupReferenceFunc$6` frame (`:190`).
- It has no `MarkupSession.java:105` frame, so the getters returned single objects, not collections.

Inference, from source:

- `MarkupSession.java:336-341` runs field references before getter markups (`:348-350`), and
  `StructureMappingInfo.java:394-399` defines the getter frame.
- The name chain is one hop (F5). Therefore marking the map at top level would show only two getter
  frames.
- Three frames fit pointer `getElement` → map `getUncommonType` → uncommon `getPkgPath` →
  GoName field-reference `getPkgPath`. So `markupGoTypes` was most likely marking pointer 0x73f4a0,
  not the misread map.
- The M1 walk path `type@0x73f4a0 → elem` agrees.

Suggested wording for `:42`: "map descriptor `go/types.valueMap` (stored string `*types.valueMap`,
TFlagExtraStar)". This also strengthens `:42`'s own point that the log does not identify the type.

### F5 (Info, confirms the entry): the offset audit passes, but the index names a slot-size class, not a type

The table compares the frozen block `predictions/swiss-misread/t1250-vet.json:2404-2432` with my
independent decode `decode_vet.py`, which shares no emulator code and reads the ELF symtab plus raw
bytes.

| Entry `:42` claim | Frozen `per_type[144]` | Independent byte decode | Status |
|---|---|---|---|
| descriptor 7793536 | `addr` :2405 | 0x76eb80, Kind 21, Size 8, TFlag 7 | match |
| `*types.valueMap` | `name` :2429 | Str 47849, flags 0, len 15 | match (see F4) |
| slot size 40 | `slot_size` :2430 | Key `interface {}`, Elem `[]types.valueType`, Group `map.group[…]`; GroupSize 328, SlotSize 40, ElemOff 16, Flags 3 | match |
| H0 uncommon 7793648, pkg_path 17673 | :2410, :2413 | +112: PkgPath 17673 → name `go/types`; Mcount 0, Moff 16 | match; H0 name valid |
| H1 uncommon 7793624 (24 bytes early), pkg_path 40 | :2421, :2424 | +88: raw `28000000 00000000 10000000 00000000` (low 32 bits of SlotSize and ElemOff) | match |
| predicts Invalid index 13902080 | :2418, :2426 | see the chain below | match |
| `runtime.types` base | `module.types` 7479296 | `.symtab` `runtime.types` 0x722000, `runtime.etypes` 9695073 | match |

The H1 chain for 13902080 is one hop:

- GoName at `types+40` (0x722028) has flag 0x6E (HAS_TAG|HAS_PKGPATH|EMBEDDED plus junk bits), an
  empty name and tag `"u"`.
- Its pkgPath nameOff, read from `types+44..47`, is 0x00620100.
- 0x722000 + 0x620100 = 0xD42100 = 13902080. That is above the last PT_LOAD byte, 0xB6BD9F
  (11976095).
- `MemoryByteProvider.java:301-302` then raises "Invalid index".
- The bytes at `types+0..47` are packed one-letter name records (`_ v f p F R a w t m r N n u b`).
  The pseudo-name is assembled from the tail of `"n"` and the `"u"`/`"b"` records.

The sibling index also reproduces from bytes. `*types.opPredicates` and `*types.nodeSet` have slot
16. Their pkg_path 16 reads a GoName at `types+16` with flag 0x46, pkgPath nameOff 844628481, giving
852107777 (0x32CA2201). Both H0 names decode to `go/types`. So the frozen H1-only set
`{13902080, 852107777}` (`decision-rule.json:21`) reproduces.

Census (discovery-independent, 8-byte-aligned scan of the types region):

- 153 byte-plausible map descriptors, matching frozen `map_types` 153.
- 11 with uncommon, the same addresses as frozen.
- Slot histogram: 24×6, 16×2, 40×1, 32×1, 48×1.
- Exactly one uncommon slot-40 map, at 0x76eb80. `per_type` is address-sorted, and 0x76eb80 is index
  144.

Slot mutations (frozen emulator run on byte copies of vet; never executed; copies deleted after):

| Mutant | Edit | H1 failing `per_type` | Predicted H1 list |
|---|---|---|---|
| A | valueMap SlotSize 40→48 | opPredicates, nodeSet (852107777) | `[852107777, 1801722468838924630]`: 13902080 **killed** |
| B | objset 32→40 | valueMap **and** objset both 13902080, plus the two 852107777 | unchanged `[13902080, 852107777, 1801722468838924630]` |
| C | valueMap 40→48, objset 32→40 | objset 13902080, plus the two 852107777 | **identical** to the real carrier's list |

Conclusion:

- The index is a function of (types base, the bytes at `types+40..47`, H1, uncommon, SlotSize 40).
  It does not depend on which type that is.
- The log is therefore consistent with any slot-40 uncommon map. Identity rests only on the census
  uniqueness, which is a byte fact, not a log fact.
- The entry's "byte-decode INFERENCE" label (`:40-42`) is correct and should stay.

The raw-log boundary is a little wider than "analyzer failure", but stops short of identity. The log
shows:

1. a GolangSymbolAnalyzer failure inside `markupGoTypes` (`:186`, `:206`);
2. the failing read: `GoName.readStructure` reading its first byte at provider index 13902080
   (`:229-235`), reached from `GoName.getPkgPath → resolveNameOff` (`:241-243`) through a
   field-reference markup;
3. the call shape described in F4.

The log names no type, address, kind or +88 binding. grep counts for `valueMap`, `76eb80`,
`73f4a0`, `7793536`, `852107777` and `1801722468838924630` are all 0.

The log also binds itself to the carrier: `ghidra.log:59` records `MD5=26b91e58c33520c18d25f300ebb82f72`,
and `md5sum` of the vet carrier gives the same value. That is a log-internal identity check beyond
the producer receipts, but MD5 is weak against an adversary.

Freeze integrity:

- The prescan `evidence/prescan/kr19-sm-vet.json` (committed at `85589ac`, 15:28 -03) equals the
  frozen JSON semantically, including `per_type[144]`.
- The frozen JSON sha256 `3281d1ab…` equals the `predictions/SHA256SUMS` entry.
- No hindsight edit was found.

### F6 (Low, residual depth): the emulator's walk channel is unvalidated against the observed logs

Observation:

- In the frozen outputs the walk channel predicts a first failure in 6 of 8 carriers:
  - go: unmapped `func.param[5]`;
  - gofmt: `invalid_data`;
  - asm: unmapped `func.param[5]`;
  - compile: unmapped `func.param[5]`;
  - cover: unmapped `func.param[9]`;
  - vet: F1.
- No retained log shows any of these: Go analysis failure counts are 0 for the seven controls and 1
  for vet, with a different index.
- With M1, the asm and cover walks go silent and vet aligns. go, gofmt and compile keep
  `invalid_data` walk failures, which I did not root-cause.
- Ghidra discovered 112 unindexed types and found 3543 in total (`ghidra.log:183-184`). The emulator
  reports 0 unindexed and h1 3430 indexed.

This matters because `decision-rule.json:20` (`h0_consistent`) and entry `:19` use a channel with no
observed hit.

## Mutation and replay record (clone: `/tmp/kr19-w2-KnowledgeMechanism.QIqWTF/clone` at `d0690fd`)

| Test | Result | Kills or confirms |
|---|---|---|
| Frozen emulator replay on vet | identical except one trailing newline: 57552 bytes vs 57551; prefix cmp 0; semantic diff 0 | `per_type[144]` is still reproducible (freshness) |
| M1 variadic mask | vet walk H1 first = 13902080 at `type@0x73f4a0`; H0 none; walk index gone | F1 |
| M1 vs `--selftest` | CLEAN cases=15, a surviving mutant | F1 test gap |
| Slot mutants A/B/C | see the F5 table | identity via census only |

## Commands (exit codes as observed)

```
git -C LANE --no-optional-locks rev-parse refs/heads/main            # d0690fd44f46… (start), exit 0; 279e8b19c516… at 16:37:03 and 16:38:34 -03, exit 0
git -C LANE --no-optional-locks log --format='%H %ad %s' --date=iso d0690fd..refs/heads/main   # 279e8b1 16:15:31 -0300, exit 0
git -C LANE --no-optional-locks diff --stat d0690fd refs/heads/main -- .ufo/waves/round-19/predictions .ufo/waves/round-19/runs .ufo/waves/round-18/tools/swiss-misread.py   # empty, exit 0
T=$(mktemp -d /tmp/kr19-w2-KnowledgeMechanism.XXXXXX); git clone -q --no-hardlinks LANE $T/clone   # exit 0
git -C $T/clone checkout -q --detach d0690fd44f46d8a7fe9da5f01c6be723d12abd41; git -C $T/clone rev-parse HEAD   # exit 0; d0690fd…
git rev-parse {a1140e7,refs/heads/main}:.ufo/waves/round-19/predictions/swiss-misread/t1250-vet.json   # b25445c1a28e… both, exit 0
git show {8a8da7e,a1140e7,refs/heads/main}:.ufo/waves/round-18/tools/swiss-misread.py | sha256sum   # 14924bd6999b… x3 (= runs/t1250-vet/producer.json), exit 0
git show 279e8b1:.ufo/waves/round-19/runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log | sha256sum   # a5de76223172…, exit 0; | wc -l → 282
for pat in valueMap 76eb80 73f4a0 7793536 852107777 1801722468838924630 'Invalid index' 'Go analysis failure' 'lambda\$createMarkupFuncFromGetter' makeMarkupReferenceFunc 'MarkupSession.markup\(MarkupSession.java:105\)' ERROR; do git show 279e8b1:<log> | grep -cE "$pat"; done   # subset of the executed pattern loop: 0 0 0 0 0 0 1 1 3 1 0 1; loop exit 0; pass2 vet log: ERROR 1, Invalid index 1, getter frames 3
md5sum /home/vgpnk/.local/opt/go-1.25.0/pkg/tool/linux_amd64/vet   # 26b91e58c33520c18d25f300ebb82f72, exit 0 (= ghidra.log:59)
sha256sum …/vet   # 9b9d776e7569c910…, size 8082935, exit 0
python3 -I -B $T/decode_vet.py …/vet 7793536 > decode-valueMap.json   # exit 0 (F5 table); 7793792 / 7793920 runs exit 0
python3 -I -B $T/census_maps.py …/vet 7793536 7793792 7793920 > census-vet.json   # exit 0 (153 maps, 11 uncommon, one slot-40)
python3 -I -B $T/clone/.ufo/waves/round-18/tools/swiss-misread.py --carrier …/vet --golang-root /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang > repro-vet.json   # exit 0
cmp repro-vet.json frozen-vet.json   # exit 1 "EOF on frozen-vet.json after byte 57551"; head -c 57551 repro-vet.json | cmp - frozen-vet.json → exit 0; sorted-JSON diff → exit 0
python3 -I -B $T/trace_walk.py <clone emulator> …/vet <golang-root> > trace-walk.json   # exit 0 (F1 frames)
python3 -I -B $T/swiss-misread-m1.py --carrier <each of 8 carriers> --golang-root <golang-root>   # exit 0 x8
python3 -I -B $T/clone/.ufo/waves/round-18/tools/swiss-misread.py --selftest   # SELFTEST: CLEAN cases=15, exit 0
python3 -I -B $T/swiss-misread-m1.py --selftest                                 # SELFTEST: CLEAN cases=15, exit 0
python3 -I -B - (slot mutants A/B/C: frozen emulator on 0644 byte copies)       # emulator exit 0 x3; copies removed (rm exit 0)
cd LANE && find .ufo/waves/round-19/runs -name compare.json | wc -l            # 16, exit 0
git -C LANE --no-optional-locks ls-tree -r --name-only refs/heads/main -- .ufo/waves/round-19/runs | grep -c '/compare.json$'   # 8
git -C LANE --no-optional-locks status --porcelain=v1 --ignored -- .ufo/waves/round-19/runs   # ?? .ufo/waves/round-19/runs/pass2/, exit 0
cat LANE/.ufo/waves/round-19/runs/pass2/run-log.txt   # vet end 16:31:01 carrier-run=0 compare=1; aggregate exit=1; exit 0
unzip -p /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip <member> | cat -n | sed -n …   # exit 0; zip sha256 f00d29c20119…
```

Ghidra source anchors are Base-src.zip members:

- `rtti/GoName.java:88-102,122-125`
- `rtti/types/GoUncommonType.java:38-59`
- `rtti/types/GoType.java:72-75,143-150`
- `rtti/types/GoPointerType.java:32-47`
- `rtti/types/GoMapType.java:32-34`
- `rtti/types/GoFuncType.java:78-87,106-110`
- `rtti/GoTypeManager.java:147-155,263-269,639-646`
- `rtti/GoRttiMapper.java:1053-1075`
- `bin/MemoryByteProvider.java:252-255,289-302`
- `structmapping/MarkupSession.java:292-297,324,332-350`
- `structmapping/StructureMappingInfo.java:394-399`
- `structmapping/FieldMappingInfo.java:285-296`
- `structmapping/ReflectionHelper.java:320-331`
- `plugin/core/analysis/GolangSymbolAnalyzer.java:144-184`

The installed `typeinfo/golang/go1.25.0.json` aliases `runtime.maptype` to
`internal/abi.OldMapType` at `$GOROOT/runtime/map_noswiss.go:68:6`.

## Residual risk and verification gaps

- No Ghidra or REA run, per contract. The top-level-pointer inference in F4 rests on source reading
  and the census, which scans single-object referrers only in the types region.
- M1 is post-hoc. It tests the entry's explanation, and is not evidence for H1.
- I did not observe MemoryByteProvider's `maxOffset` for this program. "Invalid index" means
  `index > maxOffset`, which is consistent with the emulator's PT_LOAD maximum.
- Pass 2 and the `claims.json` amendment are untracked or uncommitted working-tree data observed
  around 16:30-16:38 -03, and may change.
- The census is a heuristic scan. It matched the frozen counts exactly, but it is not a proof of
  completeness.
- The remaining walk artifacts for go, gofmt and compile are not root-caused.
- Lane writes: this report only. No patch. No tools installed or updated.
- My scripts and outputs remain in `/tmp/kr19-w2-KnowledgeMechanism.QIqWTF/`; the mutant carrier
  copies were deleted.
