# SourceRegistry — R23-C1 source IDs, status/used-by, `maximum57`, and sigrok/Dart URL collisions

Seat: `KaidokuR23.SourceRegistry` (scout, leaf). Author-side report, **not** outside verification
or admission. Lane HEAD read: `a3c92eb6bc70984e90ae5b895412de978840b2c5`
(`git rev-parse HEAD`, exit 0). No REA probe, no carrier/device/debugger execution, no install,
and no edit to `corpus/SOURCES.md`, the knowledge entry, or any production file. This seat wrote
only this report.

**Answer, with the two states separated because the table moved under this seat:**

- At **HEAD `a3c92eb`** the registry is **57 contiguous rows, `S001`–`S057`**; `maximum57` is that
  current highest allocated id, **not** a documented numeric cap. HEAD’s next free id would be
  `S058`.
- The **live working tree is uncommitted and now has 60 rows, `S058`–`S060` added** (three added
  lines; `git diff --stat corpus/SOURCES.md` → `3 +++`; `git status` → ` M corpus/SOURCES.md`).
  The live frontier is **`S060`**, so the next free id at this instant is **`S061`**, not `S058`.
- The live rows cite `corpus/lessons/round-23.md`, which **does not exist**: the read-only census
  validator now exits **1** with three `E11` findings. That is an integration gap, not a row-id
  question (details in §1/§2).
- **No sigrok/Dart candidate first-URL collides** with an existing registry URL, and the three
  new rows add no URL warning. The real collision risks are same-release content duplicates under
  *different* URLs (tarball vs raw file; code vs manual), which the validator cannot see because
  it compares only the **first** URL in the `source` cell.

---

## Findings

### 1. Registry state (observation, two states)

**HEAD state (committed):** parsed `HEAD:corpus/SOURCES.md` with Python (row regex
`^\| S\d{3} \|`, split on unescaped `|`, require 11 cells).

| Fact | At HEAD `a3c92eb` |
|---|---|
| Rows / ids | **57**, `S001`–`S057`, contiguous, no duplicate id, no malformed cell count |
| Rows outside `## Registry` | 0 (section-aware count: all rows under `Registry`) |
| Tier histogram | A **51**, B **5**, C **1** |
| Status histogram | `mined` **55**, `rejected` **2** (`S022`, `S028`); no `queued` |
| Tier × status | A: 53 mined / 1 rejected; B: 5 mined / 0 rejected; C: 0 mined / 1 rejected |
| Kind histogram | code 14, docs 20, paper 5, dataset 4, community 4, spec 3, tool 3, own-work 4 |
| `used-by` empty or `—` | 0 rows (no W03 “mined but unused” at HEAD) |
| `used-by` target exists at HEAD | **57/57 rows, all referenced paths exist** |
| `used-by` refs per row | 1→22 rows, 2→25, 3→5, 4→2, 5→1, 8→1, 12→1 (`S003` has 12) |
| `used-by` hygiene | no backticks, no embedded spaces, no duplicate refs, no `./` or trailing `/` |
| `used-by` refs to evidence trees | 0 rows at HEAD cite `.ufo/...`; refs are `corpus/knowledge/...` and `corpus/lessons/...` |

This agrees with the peer census (`w1/ReviewSourceCensus.md:5-9`: 57 rows, A/B/C 51/5/1,
mined/rejected 55/2). My recount is independent and adds the used-by existence/format checks.

**Live working-tree state (uncommitted; observed after the HEAD census):** `git status
--porcelain corpus/SOURCES.md` → ` M`; `git diff --stat` → 3 insertions; `grep -c '^| S'` → 60.
The three new rows are:

| Row | First URL / identity | Kind/tier/status/opened | `used-by` (literal) | Observation |
|---|---|---|---|---|
| `S058` | `https://raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1` — sigrok-cli 0.7.2 manual | docs / A / mined / 2026-10-21 | `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md`, `corpus/lessons/round-23.md` | manual bytes sha256 `e3f06dfe…`; this is the document I had proposed as a manual row, now registered |
| `S059` | `…/sigrok-dumps/c8fad…/uart/hello_world/README` — dataset README | dataset / A / mined / 2026-10-21 | same two paths | README sha256 `7af1c784…`; the **README**, not the `.sr` fixture, is the registered source |
| `S060` | `.ufo/waves/round-23/evidence/c1/inventory.envelope.json`, `decode-uart-hi.envelope.json`, `decode-official-uart.envelope.json` — own-work envelopes | own-work / A / mined / 2026-10-21 | same two paths | no URL; the load-bearing Evidence family for the two new signal verbs |

Live-table histogram after the append: 60 rows, A 54 / B 5 / C 1, `mined` 58 / `rejected` 2;
all three new rows have 11 cells and no URL duplicate.

**Live validation defect (observation):** running the read-only census validator at this instant

`bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`
→ **exit 1**, stdout:

```
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
kaidoku	E11	S058 missing used-by corpus/lessons/round-23.md
kaidoku	E11	S059 missing used-by corpus/lessons/round-23.md
kaidoku	E11	S060 missing used-by corpus/lessons/round-23.md
```

`corpus/lessons/round-23.md` is absent (`ls` → no such file; `corpus/lessons/` ends at
`round-22.md`). The knowledge entry `corpus/knowledge/2026-10-21-r23-offline-signal-envelopes.md`
**exists but is untracked** (`??` in `git status`) and its first line cites
`S058`, `S059`, `S060` literally. So the row→entry linkage is shaped correctly, but the
row→lesson path fails `E11` until the lesson is created or removed from the three `used-by`
cells. The claim’s no-harm line “source census exit0” is therefore not met at this instant.
Do not treat this as a source-id defect: the IDs themselves are unique, contiguous and free of
URL collisions.

### 2. “maximum57” (observation + inference)

- **Observation:** no numeric source cap exists in the validator
  (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh`) or in the corpus docs I read
  (`corpus/SOURCES.md`, `corpus/QUALITY.md`, `SKILL.md`). The id grammar is `S[0-9]{3,}`
  (`sources-census.sh:624-627`), so ids may exceed three digits. `maximum57` is the
  **HEAD frontier** (`S057`), not a ceiling; the live frontier is now `S060`.
- **Observation — row shape:** exactly 11 cells (`NF==13` after the pipe split,
  `sources-census.sh:623`), unique id (`E03`), rows inside `## Registry` (`E12`), status
  `queued|mined|rejected` (`:628`), tier `A|B|C` (`:632`), `used-by` paths must exist
  (`E11`, `usedby_findings` at `:538-570`).
- **Observation — counter eligibility:** the R23 counter reads rows at the tested Git revision
  and admits a row only when `int(id) >= 51`, `tier in (A,B)`, `status == "mined"`,
  `opened == "2026-10-21"`, and the knowledge-entry path appears literally in the row’s
  `used-by` list (`.ufo/waves/round-22/tools/count-c1.py:121-141`). The claim is stricter:
  “cites opened/mined **S058+** with exact used-by” (`claims.json:28`), so new entries should
  cite `S061` or later now (any of the live `S058`–`S060` also satisfies the claim wording).
- **Inference:** because the counter reads a Git revision, the untracked rows/entry are
  invisible to a counter run at `a3c92eb`; rows, knowledge entry, lesson (or trimmed used-by),
  and evidence must be committed together before counting. A row whose `used-by` names an
  uncommitted path fails `E11`; an entry citing a row whose `used-by` does not name that entry
  fails counter eligibility even if the row validates.
- **Observation — insertion:** new rows append after `S060` (working-tree line 67), before the
  blank line and `## Paths`; plain comma-separated repo-relative `used-by` paths, no backticks.

### 3. URL collision machinery and the current duplicate set (observation)

- 50 URL occurrences at HEAD; 47 distinct after normalization (strip scheme/fragment/trailing
  slash, lowercase host). Existing normalized duplicates:
  - `github.com/NationalSecurityAgency/ghidra/pull/9348` — `S032`/`S033`
  - `go.dev/dl?mode=json&include=all` — `S038`/`S047`
  - `developer.android.com/ndk/guides/abis` — `S052`/`S054`
- **Observation (validator source):** `sources-census.sh:600-651` extracts only the **first**
  URL from the `source` cell. `W04` fires when that URL appeared in a different scope; `E04`
  fires for the same URL **within the same scope** and a non-rejected row whose `teaches` text
  lacks `supersedes S###`. A duplicate document cited under a different URL (release tarball vs
  raw blob, code vs manual) produces **no warning**. Collision control for sigrok/Dart must
  therefore be document-identity control, not validator output.
- The current `S047` W04 line carries a trailing backtick/comma artifact from the cell text
  (`go.dev/dl/?mode=json&include=all`,`); both `S038` and `S047` name the same release-index
  document, which is the intended duplicate. It is a validator URL-extraction artifact, not a
  second document.
- The three live rows (`S058`–`S060`) add **no** W04/E04: `S058`’s raw-manpage URL and `S059`’s
  README URL are each unique, and `S060` has no URL.

### 4. Sigrok candidate documents: identities, live rows, and collisions (observation)

All candidate first URLs were checked against the registry’s normalized URL set (HEAD + live
rows). “Content collision” is my manual identity comparison.

| # | Document identity | Status at this observation | First URL | URL state | Content-collision note |
|---|---|---|---|---|---|
| D1 | libsigrokdecode **0.5.3** UART decoder, release tarball, extracted `decoders/uart/pd.py` | proposed (`UartSemantics.md:246`) | `https://sigrok.org/download/source/libsigrokdecode/libsigrokdecode-0.5.3.tar.gz` | free | `pd.py` byte-identical to raw tag URL (sha256 `51a29d0e…`); **one row**, not two |
| D2 | sigrok-cli **0.7.2** release code (`decode.c`, `show.c`, `parsers.c`, `options.c`, `main.c`) | proposed (`UartSemantics.md:247`; partly `SignalRawFormat.md:137`) | `https://sigrok.org/download/source/sigrok-cli/sigrok-cli-0.7.2.tar.gz` | free | **S058 already owns the same release’s manual**; D2 must exclude `doc/sigrok-cli.1` and stay code-scoped |
| D3 | sigrok-cli **0.7.2** manual `doc/sigrok-cli.1` | **registered as `S058` (live, uncommitted)** | raw manpage URL | free | byte-identical to the tarball copy; page says `March 28, 2019` and **no version string**; no `--dont-scan` text |
| D4 | libsigrok **0.5.2** binary input `src/input/binary.c` (+ output writers) | proposed (`SignalRawFormat.md:137`; `SourceSigrokRaw` pending) | `https://github.com/sigrokproject/libsigrok/tree/libsigrok-0.5.2` | free | `SignalRawFormat`’s draft also cites sigrok-cli `parsers.c`/`input.c`/manual, overlapping D2/`S058` |
| D5 | sigrok wiki `File_format:Binary` (docs) | proposed (`SignalRawFormat.md:131`) | `https://sigrok.org/wiki/File_format:Binary` | free | only the two options/defaults; not packing/bit order (those are D4) |
| D6 | sigrok-dumps **0.1.0** README (dataset) | **registered as `S059` (live, uncommitted)** | `…/sigrok-dumps/c8fad…/uart/hello_world/README` | free | the `.sr` fixture itself is a separate document; no row for it yet |
| D6b | sigrok-dumps fixture `hello_world_8n1_9600.sr` | retained in evidence, no row | `…/c8fad…/uart/hello_world/8n1/hello_world_8n1_9600.sr` | free | optional dataset row if a knowledge entry cites the fixture rather than the README |
| D7 | sigrok wiki `Sigrok-cli` page (R22 candidate) | unregistered | `https://sigrok.org/wiki/Sigrok-cli` | free | if reopened, it is a superseding row or explicit exclusion, not a new document |
| D8 | Round-23 own-work signal evidence family | **registered as `S060` (live, uncommitted)** | no URL (evidence paths) | free | load-bearing for the new `inspect-signal-decoders` / `decode-signal-recording` witnesses |
| D9 | sigrok-cli 0.7.2 x86_64 AppImage tool pin | proposed (`CoverageMap.md:220`, which suggested `S059` — **now taken by D6**) | host path, no URL | free | optional; fold digest into `S060` if no separate version claim is made |

Exact observations behind the table:

- **Tag/commit pins:** `sigrok-cli-0.7.2` tag object `2f342b4d…`, peeled commit
  `b584f959edb788f1731d5a304badf241ac21bf65`; `libsigrokdecode-0.5.3` tag object `1577c435…`,
  peeled `97991a3919da6a07c4c87308ae66fb441bd512e3`; `libsigrok-0.5.2` tag object
  `48ceaf1b…`, peeled `a6b07d7e28fe445afccf36922ef7d20e63e54fe6` (`git ls-remote --tags`,
  exits 0).
- **Release artifacts (fetched, sha256):** `sigrok-cli-0.7.2.tar.gz` 230,354 B sha256
  `71d0443f36897bf565732dec206830dbea0f2789b6601cf10536b286d1140ab8`;
  `libsigrokdecode-0.5.3.tar.gz` 892,783 B sha256
  `c50814aa6743cd8c4e88c84a0cdd8889d883c3be122289be90c63d7d67883fc0`.
  Extracted `doc/sigrok-cli.1` sha256 `e3f06dfe…` and `decoders/uart/pd.py` sha256
  `51a29d0e…`, both identical to the raw tag URLs. The registered `S058` anchor already names
  the retained copy `.ufo/waves/round-23/evidence/sources/sigrok-cli.1`, sha256 `e3f06dfe…`.
- **`S058` limits:** the manual does **not** contain `--dont-scan` (grep: 0 hits); that flag is
  in `options.c:29,149` of the same release. The manual’s
  `-I binary:numchannels=4:samplerate=1mhz` example (lines 141-145) is *plain decimal* on the
  0.7.2 code path (`strtoul(...,10)`), so `1mhz` → 1 Hz — a **code-row** fact, not a manual-row
  fact. The live `S058` scope says “decimal samplerate … explicit in the exercised calls”; keep
  that claim tied to the code/REA call, not to the manual text.
- **D4 anchors (my read):** `src/input/binary.c` 4,394 B sha256
  `fa037abe4beaf00ff35470f4a78989c2237663edad79b9fd53af6375e72dd9d1`; options table
  `:157-161` (`numchannels`, `samplerate`), defaults `:33-34`, `unitsize` `:64`, module
  descriptor `:174-178`.
- **D5:** live page HTTP 200, 13,661 B HTML, `wgRevisionId` 13665, last edit 2018-09-17; raw
  wikitext 335 B sha256 `2d81a085ad13ac0bf859629728549130fc7d8fa401c7950d5a8281757be222c4`.
- **D6/D6b:** fixture 58,381 B sha256
  `01b72610cdc4510dd46c8ce82b163947adbbab5b9883aea164c00e15af900b61`; tag
  `sigrok-dumps-0.1.0` peeled `c8fad0528648ba58ceddbda9e34e4dfcd293a6b0` (2012-05-18).
  `6bf0de22955f18e91eb9c2089cb31b7c9252ed47` is a **2015-12-25** commit; README sha256
  `7af1c784…` is identical at both, but `c8fad` is the tag and the live `S059` correctly uses it.
- **D2 vs `S058`:** `UartSemantics.md:247` lists `doc/sigrok-cli.1` among the code row’s files.
  With `S058` registered as the manual row, that would claim the same document twice under
  different first URLs (no validator warning, but duplicate source identity). Remove the manual
  from D2’s source/anchor, or merge D2 into `S058` and drop the separate code row.
- **D4 vs D2:** `SignalRawFormat.md:137` combines libsigrok and sigrok-cli in one code row whose
  scope includes `-I` key=value conversion. That duplicates D2’s `parsers.c`/`options.c`
  content unless the row is split (libsigrok mapping vs CLI argument conversion) or its scope is
  narrowed.
- **D7:** R22’s wiki draft was never assigned an id; `corpus/SOURCES.md` contains no `sigrok`
  string at HEAD. The live `S058` is a *different authority* (version-pinned tag) from that
  unregistered wiki draft, not a duplicate row.

### 5. Dart candidate documents: identities and collisions (observation)

REA 6.5.0 looks up exactly four names in the **dynamic** symbol table:
`_kDartVmSnapshotData`, `_kDartVmSnapshotInstructions`, `_kDartIsolateSnapshotData`,
`_kDartIsolateSnapshotInstructions` (`dist/cli-runtime/cli.js:19742-19745`). `readElfSymbols`
iterates `SHT_DYNSYM` only; when section headers are absent it reconstructs the dynamic table
from `PT_DYNAMIC` — it never reads `SHT_SYMTAB` (`cli.js:18926-19010`; peer `SchemaDart.md:80-91`
and `DartSaberRefusal.md:48-51` independently state the same from `DartElf.js`, which has
`SHT_SYMTAB` count 0).

| # | Document identity | First URL | URL state | What it actually declares |
|---|---|---|---|---|
| E1 | Dart SDK `runtime/include/dart_api.h` @ commit `0edc81df4fa2060ca4ca80bf2f91c4b5a2616004` (stable 3.13.6) | `https://raw.githubusercontent.com/dart-lang/sdk/0edc81df…/runtime/include/dart_api.h` | free | `kSnapshotBuildIdCSymbol`/`Data`/`Text`/`Bss`; non-Apple values `_kDartSnapshotBuildId`, `_kDartSnapshotData`, `_kDartSnapshotText`, `_kDartSnapshotBss` at `:4028-4031`; AsmSymbol forms `:4033-4036`. **Does not declare the four VM/isolate names.** |
| E1′ | Same file @ `main` `2752d562ce0230b3fda87f10d8070150d32397db` | `https://raw.githubusercontent.com/dart-lang/sdk/2752d562…/runtime/include/dart_api.h` | free | same macro set, shifted to `:4090-4104`; second anchor, not a second row |
| E2 | Flutter engine (archived mirror) `runtime/dart_snapshot.cc` @ `ae5c3603d013477d37ae301993fc0967d4ad7ed2` | `https://raw.githubusercontent.com/flutter/engine/ae5c3603…/runtime/dart_snapshot.cc` | free | declares the **legacy** four: `kDartVmSnapshotData`, `kDartVmSnapshotInstructions`, `kDartIsolateSnapshotData`, `kDartIsolateSnapshotInstructions` at `:18-22` (engine constants omit the leading `_`) |
| E3 | Flutter monorepo `engine/src/flutter/runtime/dart_snapshot.cc` @ `14d4db86a25f5c0d56bc67ed9deaba4dde2bdfbb` | `https://raw.githubusercontent.com/flutter/flutter/14d4db86…/engine/src/flutter/runtime/dart_snapshot.cc` | free | maps **both** VM and isolate roles to `kDartSnapshotData`/`kDartSnapshotText` at `:18-21`; the modern name set |
| E4 | Dart SDK `runtime/vm/snapshot.cc` (any revision checked) | n/a | free | **contains none of the four names**; see below — do not cite it as their declaration |

Observations:

- **E1 hash/anchors:** fetched at the pinned commit, 153,740 B sha256
  `d5009bb2dfa76dcdf3ed3c5bd427a74c4c820cea29f393a5909efa377291f713` (matches the peer’s
  `d5009bb2…`). `tools/VERSION` at that commit reads `CHANNEL stable`, `MAJOR 3`, `MINOR 13`,
  `PATCH 6`.
- **E2:** 10,827 B sha256
  `cfe68fef2c719490630765978fe6e5856649f7a8e28b503c0e479327b9ff76e1`; commit date
  2025-02-25, subject `Prepare for archive (#57288)` (shallow `git fetch` + `git log -1`).
- **E3:** 10,946 B sha256
  `a4f15bb6a84fff05e5cf2f739e18a8ce6f2f50fed12cad8289994dc5d82db3d0`; `flutter/flutter`
  `refs/heads/master` = `14d4db86…`.
- **E4:** Dart SDK `runtime/vm/snapshot.cc` fetched at tags `2.19.6`, `3.5.0`, `3.9.0`, `main`
  (`2752d562…`) and `0edc81df…`: 0 hits for `kDartVmSnapshotData`, `kDartIsolateSnapshotData`,
  or `kVMDataSymbol`. A row attributing the four lookup names to this file would be false.
- **Carrier cross-check (independent byte scan, not execution):** `/tmp/kd22probe/saber.apk`
  libapp member `lib/x86_64/libapp.so` 16,778,120 B sha256
  `b54b19d243b6db78e27f9147b56dc0aa17ef6119fa905c2e2f7c72eb2f198feb`; byte offsets
  `_kDartSnapshotData` 508, `_kDartSnapshotText` 489, `_kDartSnapshotBuildId` 527; all four
  legacy names `-1` (absent). This matches peer `DartSaberRefusal.md:71-76,91-93`.
- **Collision risk:** `SourceDartSnapshots` (“Dart VM snapshot symbols source”) and
  `DartSymbolSource` (“Dart SDK snapshot symbol declaration source”) target overlapping
  material. If both cite E1 or both cite E2, they are **one document, one row**; the second seat
  contributes anchors/used-by, not a duplicate row. The honest split is E1 (SDK exported names,
  matching the carrier) and E2/E3 (engine role-to-name mapping, explaining REA’s legacy lookup
  names). Those are distinct claims and should not be merged into one `teaches` sentence.
- **Carrier ownership:** `S055` already owns the Saber probe with fixed used-by
  (`corpus/knowledge/2026-10-21-r22-flutter-positive-dart-refusal.md`,
  `corpus/lessons/round-22.md`). A new round-23 knowledge entry cannot rely on `S055` for source
  eligibility (its used-by does not name the new entry and the row must not be edited under
  no-harm). If a new Dart entry cites the carrier, it needs a new `S061+` row whose used-by names
  that entry — or it must cite E1 as the source and the retained S055 envelope as evidence
  without claiming S055 as its new source row.

### 6. Proposed next ids (proposal only — no edit made)

The live frontier is `S060`; the ids below start at `S061`. `S058`–`S060` are **already taken**
by the live working-tree rows (manual, dataset README, own-work envelopes), so the earlier
`CoverageMap` proposal to use `S059` for the AppImage collides with the live dataset row and must
not be followed.

| Id | Document | Tier/kind | First URL (must be the unique discriminator) | Conditions / notes |
|---|---|---|---|---|
| `S061` | libsigrokdecode 0.5.3 UART decoder (D1) | A / code | `https://sigrok.org/download/source/libsigrokdecode/libsigrokdecode-0.5.3.tar.gz` | One row; cite raw tag `pd.py` only as byte-identical corroboration (second URL is allowed after the first) |
| `S062` | sigrok-cli 0.7.2 code (D2) | A / code | `https://sigrok.org/download/source/sigrok-cli/sigrok-cli-0.7.2.tar.gz` | Scope = `options.c`/`decode.c`/`show.c`/`parsers.c`; **exclude** `doc/sigrok-cli.1` because `S058` already owns it |
| `S063` | libsigrok 0.5.2 binary input module (D4) | A / code | `https://github.com/sigrokproject/libsigrok/tree/libsigrok-0.5.2` | Scope = `binary.c` sizing/bit mapping + output writers; do not duplicate `S062`’s CLI parsers |
| `S064` | sigrok wiki `File_format:Binary` (D5) | A / docs | `https://sigrok.org/wiki/File_format:Binary` | Optional docs row; distinct document from `S063`; only two options/defaults |
| `S065` | sigrok-dumps 0.1.0 `.sr` fixture (D6b) | A / dataset | `https://raw.githubusercontent.com/sigrokproject/sigrok-dumps/c8fad…/uart/hello_world/8n1/hello_world_8n1_9600.sr` | Only if a knowledge entry uses the fixture itself; `S059` already owns the README; no acquisition claim |
| `S066` | Dart SDK `runtime/include/dart_api.h` (E1) | A / code | `https://raw.githubusercontent.com/dart-lang/sdk/0edc81df…/runtime/include/dart_api.h` | The carrier-matching exported-name row; scope explicitly says “not the four legacy VM/isolate names” |
| `S067` | Flutter engine `DartSnapshot` symbol declarations, legacy + modern (E2/E3) | A / code | `https://raw.githubusercontent.com/flutter/engine/ae5c3603…/runtime/dart_snapshot.cc` | One version-difference row; second URL = monorepo `14d4db86…`; scope = engine constants, not Dart SDK and not carrier exports |
| `S068` | sigrok-cli 0.7.2 AppImage tool pin (D9) | A / tool | host path, no URL | Optional, only if the entry makes a producer-build claim beyond `S060`; do **not** reuse `S059` |

Dedupe rules if L1 prefers fewer rows:

- **One sigrok-cli row instead of `S058`+`S062`:** the manual is already `S058`; adding `S062`
  for code is the code/docs split used by `S043`/`S044`. If L1 prefers one row, fold the code
  anchors into `S058` and drop `S062` — do not keep two rows whose scopes both name the manual.
- **One raw-input row instead of `S063`+`S064`:** keep `S063` (code) and cite the wiki page only
  inside its anchors; the wiki’s two-option claim is already in the manual/source.
- **Dart:** if only one Dart row is admitted, `S066` (SDK `dart_api.h`) is the one matching
  Saber’s dynsym and the `.dynsym`-only lookup; `S067` is needed only to explain REA 6.5.0’s
  legacy names. Do **not** create a row from E4.
- **Rejected/exclusion candidates:** E4 (`runtime/vm/snapshot.cc` as declaration source), D7
  (unversioned wiki `Sigrok-cli` page as a new 0.7.2 row), and any second row for the same
  tarball/raw bytes. If recorded, mark `rejected` with a flip condition; a rejected row cannot
  satisfy the claim (`status` must be `mined`).

### 7. Commands and exits (observation)

| Command (cwd) | Exit | Observed |
|---|---|---|
| `git rev-parse HEAD` (`kaidoku-shokunin`) | 0 | `a3c92eb6bc70984e90ae5b895412de978840b2c5` |
| `git status --porcelain corpus/SOURCES.md` | 0 | ` M corpus/SOURCES.md` (live drift) |
| `git diff --stat corpus/SOURCES.md` | 0 | `1 file changed, 3 insertions(+)` |
| `git show HEAD:corpus/SOURCES.md \| grep -c '^| S'` | 0 | `57` (HEAD); working tree now `60` |
| Python census over HEAD/working tree | 0 | 57/60 rows, contiguous, 11 cells, histograms in §1 |
| Python URL census | 0 | 50 HEAD occurrences / 47 distinct; 3 duplicate pairs in §3 |
| Python candidate-vs-registry URL check | 0 | all candidate first URLs free (HEAD + live rows); no candidate-vs-candidate first-URL duplicate among distinct documents |
| `bash scripts/sources-census.sh validate --root … kaidoku` | **1** | 3 W04 + 3 `E11` (`S058`–`S060` missing `corpus/lessons/round-23.md`) |
| `git ls-remote --tags` for sigrok-cli / libsigrokdecode / libsigrok | 0 | tag→commit pairs in §4 |
| `curl -sS -L` raw tag/commit files (manpage, `pd.py`, `binary.c`, Dart/Flutter files) | 0 | HTTP 200; sha256s in §4/§5; tarball copies byte-identical |
| `curl` `sigrok.org/gitweb/…;a=blob_plain` | 0 | body `Sorry, disabled because of misbehaving AI crawlers.` — official gitweb is not a usable automated citation route |
| `curl` `https://sigrok.org/wiki/File_format:Binary` (+ `action=raw`) | 0 | 200; rev 13665; raw sha256 `2d81a085…` |
| Shallow `git fetch` of `flutter/engine` `ae5c3603…` + `git log -1` | 0 | `2025-02-25 … Prepare for archive (#57288)` |
| `pacman -Si libsigrok libsigrokdecode sigrok-cli` (read-only) | 0 | `0.5.2-26`, `0.5.3-10`, `0.7.2-3`; no transaction |
| Independent byte scan of `/tmp/kd22probe/saber.apk` libapp member | 0 | sha256 `b54b19d2…`; modern names present, legacy four absent |

No REA command was run by this seat; no target/device/debugger/Frida execution occurred.

---

## Produced files

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/SourceRegistry.md` —
  this report. Its SHA-256 is computed after the write and reported in the seat’s final message
  (a file cannot embed its own hash without changing it).

## Installs

None. No package manager, `uv`, `npx`, or config change. `pacman -Si` was a read-only sync-DB
query; host pacman transactions remain paused and untouched.

## Open risks

1. **Live table is uncommitted and currently fails census.** `S058`–`S060` exist only in the
   working tree and cite a missing `corpus/lessons/round-23.md`; the validator exits 1. Rows,
   knowledge entry, lesson (or trimmed used-by), and evidence must land together. I did not edit
   them.
2. **The frontier moved during this seat.** HEAD is 57 rows (`S057`); the live tree is 60
   (`S060`). Any later seat that assumed `S058` is free would collide; use the live max at edit
   time.
3. **Validator blind spot for content duplicates.** Only the first URL is compared, so a tarball
   row and a raw-file row for the same bytes would both pass. The document-identity dedupe in §4
   is manual, not machine-enforced.
4. **`S058` scope overreach risk.** Its `teaches` says “decimal samplerate … explicit in the
   exercised calls”; the manual text does not state the decimal rule (the code path does). Keep
   that claim attributed to `S062`/REA calls if the manual row is reviewed for relevance.
5. **Dart declarations are not carrier evidence.** E1/E2/E3 declare symbol names; only the
   retained Saber parse shows which names the APK actually exports. No source row should be
   written as “this APK exports …” on the strength of E1/E2/E3.
6. **`0edc81df…` provenance.** The peer read that revision from another seat’s scratch clone; I
   re-fetched the public raw file at the same commit and matched sha256 `d5009bb2…`, but I did
   not verify the clone’s fetch history or branch. The commit itself is publicly reachable.
7. **Archived engine mirror.** `flutter/engine` `main` is the archival commit (2025-02-25); the
   current source lives in `flutter/flutter/engine/src/flutter/...`. A row citing only the mirror
   must say so.
8. **Official gitweb is blocked for automated clients** (“misbehaving AI crawlers”); GitHub raw at
   the same tag/commit is the reproducible citation route. This is a channel substitution, not an
   identity change (byte-identical tarball copies observed where checked).
9. **AppImage row is host-local.** Its path is not reproducible off this host; only the SHA-256
   and version banner make it citable. If admitted without a digest-pinned public URL, say so in
   `anchor`.
10. **No LSP.** `read xd://lsp` is unavailable in this session (the device list has no LSP
    route), so this report’s text searches are literal locators only, never semantic proof. This
    seat did not present grep output as definition/reference evidence.
11. **No numeric cap was found**, but absence of a cap in the files I read is not proof that no
    other fleet rule caps the registry; the claim’s own `S058+` wording is the operative bound.
