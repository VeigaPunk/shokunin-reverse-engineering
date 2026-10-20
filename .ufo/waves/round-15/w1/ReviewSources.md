# Round 15 — ReviewSources (seat W1): S003/S007 used-by deltas and quotes

Seat: `KaidokuR15.ReviewSources` (leaf reviewer). Axes named: **depth** (C1 source-selection facts) and **calibration** (C2 correction of S003/S007 citations).
Access date for every reopened item below: **2026-10-20**. Registry row `opened` stays `2026-10-19` (CORPUS.md Rule 2: `opened` and `anchor` are immutable).

Scope honoured: `corpus/SOURCES.md` was read and **not modified** (git status shows it unchanged; sha256 at observation `25c19036312957087d384f8174c5e78e7f38d6decff5cf227b403b2c809e6cbb`). No new rows. No builds, tests, linters, census CLI, or gates were run. No tools installed or upgraded. Only reads, `sha256sum`, zip member reads, and line greps were used.

## 1. Observed state (read-only)

- **Installed sources match registry digests.**
  - S003 `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/lib/Base-src.zip` → `f00d29c20119562eca7efd2740e8c67257ebd63ea24a3dfbc4dbbb9187a8d804` (matches `corpus/SOURCES.md:9` and the entry).
  - S007 `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md` → `c6b25301cda77dca1683a2a1802d84256d35625cf8959cdced144579486f65c4` (matches `corpus/SOURCES.md:13`).
- **Current registry cells (unchanged, `corpus/SOURCES.md:9` and `:13`, `used-by` column):**
  `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md, corpus/lessons/round-14.md`
  Each listed path exists on disk. `corpus/lessons/round-14.md` cites both S003 (Gate row, ~line 18/34) and S007 (line 36), so the existing cells are consistent with citations.
- **Concurrent edits by other seats (observed during this read; not by W1):**
  - `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` changed mid-read: first read was tag `#664F` (106 lines); later read was tag `#C554` (117 lines). It now has a `## Round-15 advisory-pointer correction` section at `:108-117`.
  - `corpus/lessons/round-14.md` (159 lines) now has `## Round-15 correction — virtual-dispatch advisory` at `:144`, and `:157-158` names `corpus/lessons/round-15.md`, which **does not exist yet** (`ls`, 2026-10-20).
  - `corpus/QUALITY.md` is modified.
  - Ordering risk: any `used-by` path to `corpus/lessons/round-15.md` or the new round-15 knowledge entry must wait until that file exists (E11, CORPUS.md:46). L1 should re-hash `corpus/SOURCES.md` before and after integration.
- **Spot-check lessons cite S003/S007 by ID but are not in `used-by`.** `corpus/lessons/round-14-verifier-spotcheck.md:104,131-141` and `corpus/lessons/round-13-verifier-spotcheck.md:10` mention S003 (and S007 at `round-14-verifier-spotcheck.md:136,141`). Neither is listed. See §3, item N1.

## 2. Anchor verification of the round-14 entry (S003/S007 claims)

I opened the archive members and the installed ChangeHistory directly. Each row below is a claim in `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` (tag at observation `#C554` or `#664F`; claim text unchanged).

| Entry claim | Source anchor (S003 member `ghidra/app/util/bin/format/golang/rtti/…` unless noted) | Result |
|---|---|---|
| Declared range `1.15-1.25` | `GoRttiMapper.java:79` | Confirmed |
| Out-of-range logs and continues, no throw/return | `GoRttiMapper.java:170-172`; `:176` snapshot lookup follows | Confirmed |
| `getVer().isInvalid()` only logs on the success branch | `GoRttiMapper.java:178-181` | Confirmed (see §4, item L3) |
| Missing base file returns null, then EMPTY | `GoApiSnapshot.java:122-126` returns null on `jsonFile == null`; `:115` `return GoApiSnapshot.EMPTY;` | Confirmed |
| Patch-diff search does not fall back to an earlier minor | `GoApiSnapshot.java:148-166`; loop walks `prevPatch()` only, same major.minor | Confirmed |
| Bootstrap message only in IOException handler with invalid snapshot | `GoRttiMapper.java:353-365` (`:356` `if (apiSnapshot.isInvalid())`, `:358-360` message) | Confirmed |
| `DataTypeMapper` throw on missing structure | `DataTypeMapper.java:172-181` | Partly: the throw at `:180-181` applies to classes that are **not** `StructureReader`. A second throw at `:183-186` covers the StructureReader name-count case. Entry wording is broader than the cited range. Minor. |
| Catch and null return, analyzer false | `GoRttiMapper.java:114-125` (catch and `return null` at `:125`); `GolangSymbolAnalyzer.java:133-137` | Confirmed |
| Invalid snapshot = no applicable arch records | `GoApiSnapshot.java:205-239` (`:239` `new GoApiSnapshot(ver, results)`); `:503-505` `isInvalid()` = `arches.isEmpty()` | Confirmed |
| `super(program, null)` means no legacy GDT path | `GoRttiMapper.java:331` | Confirmed |
| `getType` override delegates to `goTypes.findDataType` | `GoRttiMapper.java:380-386` (`:382`) | Confirmed |
| `findTypeRec` snapshot dependence | `GoTypeManager.java:402` starts `findTypeRec`; entry cites `:405-455` (body). `:449` `else if ((typeDef = apiSnapshot.getTypeDef(typeName)) != null) {` | Confirmed; range `405-455` is the body, the method starts at `:402`. Minor. |
| S007 switch to JSON snapshots, `Ghidra 12.0 Change History` → `Improvements`, line 585 | `ChangeHistory.md:564` `# Ghidra 12.0 Change History (December 2025)`; `:582` `### Improvements`; `:585` bullet | Confirmed |

No S003/S007 claim in the entry was found to be false. The two minor range imprecisions above should be fixed only if the author reopens the entry; they do not change the decision table.

## 3. Proposed `used-by` deltas (proposal only; L1 applies)

Rule basis: CORPUS.md:107-108 (`used-by` = citing knowledge entries or lessons); Rule 2 (`used-by` changes in place, logged old→new in the round lesson); CORPUS.md:46 and scripts/sources-census.sh E11 (path must exist on disk before it is written).

**D0 — no change needed for round-14.** Current S003 and S007 cells are already correct (§1).

**D1 — conditional append, round-15 knowledge entry (custody-limited).** Only if the round-15 entry file exists and cites S003 for a **code-path** fact in `Base-src.zip` (for example `GoApiSnapshot.java` selection logic). Append after the existing three values; never replace. Check first with `grep -c 'S003' <entry>` ≥ 1. S003's pin (SOURCES.md:9, SHA-256 `f00d29c2…804`) covers `Base-src.zip` only. Do not stretch S003's `used-by` to cover facts from the installed typeinfo/golang data files that the inventory measures; those fall outside every registered row. Such facts must cite the committed inventory artifact and its digest, or L1 must open a new row for the data files (no row opened by this seat).

- S003 old: `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md, corpus/lessons/round-14.md`
- S003 new: `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md, corpus/lessons/round-14.md, <R15-ENTRY-PATH>`

**D2 — S007 append, conditional on citation.** Append `<R15-ENTRY-PATH>` to S007 only if the round-15 entry cites ChangeHistory. The natural anchor is `:585` (the JSON-snapshot switch) or `:564`/`:582`. If it cites only the S003 code path, do not append.

- S007 old: `corpus/lessons/round-13.md, corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md, corpus/lessons/round-14.md`
- S007 new: same as S003 new, only if D2 condition holds.

**D3 — round-15 lesson path, conditional.** Round-14 precedent lists `corpus/lessons/round-14.md` for S003 and S007 because its `## Gate` cites them. If `corpus/lessons/round-15.md` exists and its `## Gate` quotes S003/S007 (the reopened-source convention in SCORECARD/round-14 prompt), append `corpus/lessons/round-15.md` to both cells. Do not add it before the file exists. The round-14 entry at `corpus/lessons/round-14.md:157-158` already forward-references it, so the file must be created before D3 is applied.

**Unchanged in every case:** `opened` (2026-10-19), `anchor`, `teaches`, `scope`, `recheck` (`on-release`), `status` (`mined`). No new row.

**Log requirement:** the round-15 lesson must record each cell as old→new (Rule 2). Use the exact strings above.

**N1 — spot-check lessons (decision for L1, not a proposed edit).** `corpus/lessons/round-14-verifier-spotcheck.md` cites S003 and S007 by ID and quotes the S007 line. Round-13 precedent: `corpus/lessons/round-13-verifier-spotcheck.md` cites S003 and is not in its `used-by`. Literal CORPUS.md:107-108 wording would list it; precedent would not. **Recommendation: leave unlisted** and state the convention in the round-15 lesson, so the rule is applied consistently. Adding it is a defensible alternative if L1 prefers the literal reading; it should not be done silently.

## 4. Proposed quotes for reopened S003/S007 (exact, located)

Each quote is a verbatim substring of the stated line (checked by substring match against the archive member or the installed file). Counts in the Words column are approximate whitespace tokens; every quote is far below the 25-word limit (CORPUS.md Rule 1). Quote location format: `<member or file>:<line>`.

**S003** (`Base-src.zip`; member prefix `ghidra/app/util/bin/format/golang/rtti/` unless stated)

| # | Location | Quote | Words | Use |
|---|---|---|---|---|
| Q1 | `GoRttiMapper.java:79` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` | 8 | installed declared range |
| Q2 | `GoRttiMapper.java:171` | `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));` (branch `:170-172`, no throw/return) | 5 | range is advisory |
| Q3 | `GoRttiMapper.java:359` | `"Missing Go bootstrap type info, unable to extract Go RTTI info."` (within `:356-360`, guarded by `apiSnapshot.isInvalid()` at `:356`) | 11 | bootstrap message is conditional |
| Q4 | `GoApiSnapshot.java:115` | `return GoApiSnapshot.EMPTY;` | 3 | missing base yields EMPTY |
| Q5 | `GoApiSnapshot.java:124` | `if (jsonFile == null) {` (returns null at `:125`) | 5 | base-missing short-circuits before patch-diff lookup |
| Q6 | `GoApiSnapshot.java:128` | `File patchDiffFile = getPatchVerDiffFile(goVer);` | 4 | patch-diff consulted only after base exists |
| Q7 | `GoApiSnapshot.java:149` | `// returns the closest patch file that is present, or null if patch-ver-num is already 0` | 16 | single closest diff file (not a chain) |
| Q8 | `GoApiSnapshot.java:160` | `"Falling back from %s to %s for Go API snapshot".formatted(goVer, patchVer));` | 11 | fallback is logged (warn) |
| Q9 | `GoApiSnapshot.java:504` | `return arches.isEmpty();` (with `:503` `public boolean isInvalid() {`) | 3 | "invalid" = no applicable arch records |
| Q10 | `GoApiSnapshot.java:242` | `public static final GoApiSnapshot EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of());` | 11 | EMPTY has invalid version |
| Q11 | `GoRttiMapper.java:331` | `super(program, null);` | 3 | no legacy GDT archive on this path |
| Q12 | `GoRttiMapper.java:382` | `DataType result = goTypes.findDataType(name);` (in `getType` override `:380-386`) | 4 | type lookup goes to snapshot-backed manager |

**S007** (`docs/ChangeHistory.md`)

| # | Location | Quote | Words | Use |
|---|---|---|---|---|
| Q13 | `ChangeHistory.md:585` (section `# Ghidra 12.0 Change History (December 2025)` `:564` → `### Improvements` `:582`) | `Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files.` | 17 | JSON snapshot switch (already in the lesson; re-verified exact) |
| Q14 | `ChangeHistory.md:585` (same section) | `Added support for Golang 1.24 and 1.25.` | 7 | installed history's own Go-version support statement |
| Q15 | `ChangeHistory.md:1` | `# Ghidra 12.1.4 Change History (September 2026)` | 7 | installed file identity (matches S007 row header) |

**Limit on Q13/Q14:** these lines sit in the **12.0** section of the installed 12.1.4 file. The S007 row describes the file as the 12.1.4 history. Any lesson citing Q13/Q14 must name the `Ghidra 12.0 Change History` section, or the version attribution is wrong.

## 5. Source-selection facts for the round-15 C1 inventory decision record (depth)

These are observed from source. Runtime consequences are labeled.

- **F1 (observed).** A missing base file at `goVer.withPatch(0)` returns null before any patch-diff lookup (`GoApiSnapshot.java:122-126`). `get` then returns EMPTY (`:115`). A present patch-diff for the requested patch therefore cannot rescue a missing base file.
- **F2 (observed).** `getPatchVerDiffFile` returns **one** diff file: the closest patch that has a diff, searched downward via `prevPatch()` (`:148-166`). `getApiSnapshotJsonFile` applies that single `JsonPatch` to the base JSON and names the result `go%s.json` with the requested `goVer` (`:128-145`).
  - [INFERENCE] Whether diff files are cumulative (a patch-N diff applies cleanly to base alone) is not established by this code. The round-15 decision record must not assume a chain.
- **F3 (observed).** When no diff is found for a patch>0 request, the code falls back to base and logs `Falling back … for Go API snapshot` (`:158-161`). When patch==0, it logs `Using Go API snapshot for %s` (`:163`). The fallback is observable in logs; the base-missing case is silent in this function.
- **F4 (observed).** `read()` returns `new GoApiSnapshot(ver, results)` with `ver` = the requested `goVer` (`:239`), even when `results` is empty. `isInvalid()` is `arches.isEmpty()` (`:503-505`). So a present file with no applicable OS/arch records has a **valid** `getVer()` and an **invalid** `isInvalid()`.
- **L3 (observed + consequence [INFERENCE]).** `GoRttiMapper.java:178-180` logs `Using Go API snapshot for version …` whenever `getVer()` is valid. By F4, that message is emitted even when `isInvalid()` is true and the later bootstrap failure will fire at `:356`. Log text alone does not prove an applicable snapshot was used.
- **Javadoc vs code (observed).** The `get` Javadoc (`GoApiSnapshot.java:89-101`) says earlier patch revs are tried. The code requires a base file first (`:122-126`). The Javadoc is incomplete on the base-missing case; the code is authoritative.

These facts support the C1 "missing base / patch-diff / OS-arch applicability" discrimination. They do not establish the historical 1password run's cause (the entry already says UNKNOWN).

## 6. Limits

- Archive reading only. The S003 archive is not authenticated against any compiled provider classes; no Ghidra execution was done.
- The S007 quotes come from the installed copy. No upstream check was made.
- The S003 row anchor reads `GoApiSnapshot.java:get` (a method name, not a line). It is immutable under Rule 2; do not rewrite. The entry's line citations are the usable anchors.
- `corpus/lessons/round-15.md` and the round-15 knowledge entry do not exist at observation. D1–D3 are conditional on their existence and citations; they cannot be fully verified now.
- Working tree was changing during this read (§1). Findings are tied to the observed tags and hashes above.
- This report does not check the `[INFERENCE]` items, the S004 and S005 rows, or the C2 quote-gate behaviour (out of seat scope).

## 7. Proposed L1 checks (named, NOT run by this seat)

1. `sha256sum` of the S003 zip and S007 file; compare with `f00d29c2…804` and `c6b25301…5c4`.
2. Before editing: `sha256sum corpus/SOURCES.md` (baseline `25c19036…6cbb`); after editing: `git diff -- corpus/SOURCES.md` must show only `used-by` cells changed on S003/S007 (plus any other row L1 intentionally changes, logged).
3. `ls corpus/knowledge/<R15-ENTRY-PATH>` and `ls corpus/lessons/round-15.md` must succeed before the corresponding `used-by` append (E11 order).
4. `grep -cF 'S003' <R15-ENTRY-PATH>` and `grep -cF 'S007' <R15-ENTRY-PATH>` ≥ 1 for each row whose cell changes (no false citation).
5. For each quote Q1–Q15: `grep -cF` the exact string against the extracted member or `docs/ChangeHistory.md`, and confirm word count ≤25.
6. `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` → expect `kaidoku ok`, exit 0, with rows still 22 and tiers A20/B1/C1 and statuses mined21/rejected1.
7. Confirm the round-15 lesson `## Gate` records each S003/S007 old→new `used-by` string exactly as in §3.

## 8. Tooling

No installs, upgrades, or `pacman`/`uv`/`cargo`/`npm` use. Reads only: `sha256sum`, `git status`, `python3` zip member reads, `grep`/`sed` line reads.
