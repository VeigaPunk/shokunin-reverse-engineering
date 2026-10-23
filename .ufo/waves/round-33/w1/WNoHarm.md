# WNoHarm — read-only compare base 428315a8 vs d7076120 (round 33 w1)

Seat: `KaidokuR33.WNoHarm` (LEAF, no subagents, no test/gate runs).
Assignment: compare `428315a8f5674b952def862910af6e07a6c2224b` → `d7076120e4f00c6d18aa77b8764d14861e820eb2` for existing owned knowledge, SKILL scope, SOURCE rows, SCORECARD, and original r32 instrument hashes; name any removed/false old fact, widened Core, unsupported source attribution, or promotion mark.

## Method

- `git diff --name-status` base→head: 77 files, **0 deletions**; 71 additions, 6 modified (`LOG.md`, `SCORECARD.md`, `SKILL.md`, `corpus/README.md`, `corpus/SOURCES.md`, `corpus/QUALITY.md`).
- `git ls-tree -r` of `tools/round-32/` at base vs head: **identical blob hashes** (7 files).
- Captured source files sha256 vs `source-pins.json` / `document-spec.json`: all 9 match.
- Upstream re-fetch at commit `0d261d1ca552c95a8f007e061c787ac7132fbcbc` (8 files): all sha256-identical to captures.
- Tag `llvmorg-23.1.3` deref via GitHub API: tag object `856f0005…` → commit `0d261d1c…` (tagger 2026-10-06). S101's commit pin is the tag's commit.
- Static replication of `measure_driver._section_bytes` normalization: SKILL `## CHPE structural profile — round 33` body equals `.ufo/waves/round-33/expected-skill-body.txt` (normalized hash `3750ce27…` both sides; text_file raw sha256 `49777892…` matches pin).

## Findings

### 1. No removed old facts (nothing deleted, verified)
All six modified tracked files are insertion-only (0 deletions; diff confirms). No existing knowledge file, SOURCES row, SKILL row, or SCORECARD line was removed or rewritten. `PROVINCE.md`, `MINT.md`, `SHONEN.md`, `AGENTS.md` untouched. S098/S099/S100 rows appear unchanged in the SOURCES diff (S100's CHPE-authority rejection is explicitly retained "not reversed" — S100 row still present with REJECTED status).

### 2. No widened Core; new knowledge on old covered ground
- `PROVINCE.md` unchanged: no Round-33 additions to Core; the only bounded-Core hybrid row remains round 32 ("ARM64X synthetic exported-leaf native-view import/overview… published hybrids, dual-view/EC recovery and internal-function analysis remain Frontier").
- `corpus/README.md` new row: "sourced detail on existing hybrid ground; original independent carrier claim stopped by a provider safety hold, no replacement measurement, no coverage widening" — matches my verification.
- `SKILL.md` "CHPE structural profile — round 33" decision table is explicitly framed: source facts (S101) vs "explicit local profile"/conservative exclusions, with repeated limits ("not a complete PE validator", "not proof of a genuine hybrid", "does not widen Core coverage", "Finite fixture agreement does not exclude arbitrary exact-hash lookup implementations"). No new REA verb, no new carrier class, no new capability row.

### 3. Source attribution supported (S101/S102)
- S101 URL/commit verified: raw file at `0d261d1c…` (== `llvmorg-23.1.3` tag commit). Content checks: `Object-COFF.h` `chpe_metadata` (734–760), `chpe_range_type`/`chpe_range_entry` with `TypeMask=3` and low-two-bit `getType` (762–773); `Chunks.h` execute-bit gate + machine→tag mapping (475–487); `Chunks.cpp` `ECCodeMapChunk::writeTo` computes `start = getRVA() & ~0xfff`, independent Length, `StartOffset = start | type` (944–956); `COFFObjectFile.cpp` reader `checkOffset(getRvaPtr(...))` across whole CHPE extents, `offsetof(...CHPEMetadataPointer)+sizeof(pointer)`, and `CodeMapCount`-bounded check (756–778). Emitter empty-range comment (MS link.exe) in `Writer.cpp:613-614`; empty-section behavior covered by `arm64ec-codemap.test`.
- Offsets 0xc8/0xd0: derived from captured 64-bit layout incl. `coff_load_config_code_integrity` (12 bytes) → CHPEMetadataPointer at 0xC8, pointer span through 0xD0. Verified by field-size walk. `chpe_metadata` = 23 × u32 = 92 data bytes (matches knowledge entry).
- S102 verified: `pe-format.md` lines 133–137 (0x3c → PE signature), 141 ("Windows loader limits the number of sections to 96"), 222–224 (SizeOfOptionalHeader and NumberOfRvaAndSizes bound probes). Digest `563f2dd9…` matches pin and capture.
- Quote positions: `Object-COFF.h:768` "The two low bits of StartOffset contain a range type." and `pe-format.md:133` "At location 0x3c, the stub has the file offset to the PE signature." both present on the pinned lines (document-spec `file_quote` passes).
- No claim in S101/S102 exceeds what the sources show (tag labels are not validation; S102 scoped to header boundaries). The knowledge entry's "0xc8/0xd0 derived from captured layout, not PE spec" is accurate (the spec capture contains no such offsets — consistent with the retained S100 rejection).

### 4. No promotion mark; scores unchanged
- `SCORECARD.md` round-33 section: owned proxies stay 10 → 10, delta 0; "no calibration gain or new capability row"; verdict "unprovable; honest stop"; before/after not evaluated; no substitute benchmark. It supersedes (additively) the round-32 "pending outside decision" sentence without deleting it.
- QUALITY 59–63 are new lessons (not score changes); LOG round-33 entry is an honest stop record.
- Knowledge file and README rows state "no admissible production carrier study" / "original claim stopped"; no "verified/held" upgrade for any capability.

### 5. Original r32 instrument hashes intact
- `tools/round-32/` blob hashes identical base→head (7 files).
- `r32_oracle_adapter.py` pins `ORACLE_SHA256 = 17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686`, which equals the live sha256 of `tools/round-32/arm64x_oracle.py`.
- SKILL round-32 registry rows unchanged (append-only round-33 section), and the five old wrapper mutants / secondary-gate selftest defects remain explicitly open (not silently repaired).

### 6. SKILL errata verified against archived tools
All registry-errata bullets in the new `## Round-33 instrument status…` section hold against the code:
- r31 C1: `--write-evidence` does not emit exit 3; prints receipt-shaped `target=` line; returns 0/1 (`c1-sqlite-positive.py:18,201,255-256`).
- r31 C2: needs separately built mutant/sibling tree under `/fast/scratch/hyaku/kaidoku-r31/`; missing inputs exit 2 (`c2-sqlite-refusals.py` return 2 paths).
- Calibration v1/v2/v3 read fleet pin via `--fleet` default `/home/vgpnk/Projects/shokunin` (`c2-capability-calibration.py:181`).
- `final-c1-witness/pe_own_compare.py` reads `${SCR}/carriers.tsv`, writes `compare-own.json` (live carrier bytes needed).
- `independent-pe/compare.py` hard-codes `BASE=/fast/scratch/…/A2PEIndependent`, has no argv parsing, invokes `llvm-readobj --version`; `secondary_evidence.py` reads `BASE/indep.json`, writes `secondary-evidence.json` (evidence producer, no selftest).
- `verify_quotes.py` pins absolute lane `SNAP`/`C1IN` paths; old `cited-runs-gate.py` `--selftest` builds a throw-away git repo and honors `--keep-selftest` (line 251).

### 7. Containment compliance at head
Excluded builder-dependent paths (`chpe_fixture_gen.py`, `chpe_predict.py`, `chpe_driver_manifest.py`, `frozen/`, `prefreeze-controls/`, `prep/R33FixtureBuilder.md`, `prep/R33ChpeParser.md`, `prep/builder-count-erratum.txt`) are absent from the d7076120 tree (git ls-tree grep). `safety-holds.json`/`quarantine-record.json` metadata was the only held-item reference used. The four retained instruments (`chpe_profile.py`, `measure_driver.py`, `r32_oracle_adapter.py`, `selftest_pegen.py`) are present, and their isolated selftests are instrument evidence only (not carrier measurement). `measure_driver.py` requires an admissible manifest (`--manifest-sha256` + `--classifier-sha256`) which does not exist; its docstring and SKILL row explicitly state "No admissible original R33-C1 input manifest or production receipt exists."

### 8. Minor notes (non-defect)
- `.ufo/waves/round-33/expected-skill-section.txt` is not referenced by `document-spec.json` or the driver (only `expected-skill-body.txt` is); harmless surplus.
- `expected-gate-notes.txt` is a substring of `corpus/lessons/round-33.md` (raw-substring true), so it is a section expectation, not a whole-file pin.
- SOURCES round-33 journal line ("Opened two primary source families… retained nine captures…") matches: 8 LLVM files + 1 served Markdown = 9, per `source-pins.json` (`jq '.files|length'` = 9).

## Residual risk / verification gaps

- **No execution**: per assignment, no test/gate runs were performed; all tool-behavior findings are static source reads. `measure_driver.py --selftest` behavior (STUBS) was reviewed in source only; nothing was executed.
- **Servability of `pe-format.md`**: the served Markdown is a live Microsoft Learn artifact; I verified stored digest/pin and line content locally, but cannot re-fetch a byte-identical copy (no network revalidation requested/needed).
- **`prep/R33FixtureDesign.md`** is committed and is not on the quarantine exclusion list; my scope does not require reading it and I did not. (It is a design/prep doc, not the held builder's code or output.)
- **Future drift**: upstream commit-pinned raw URLs are stable; the tag-name URL in S101 resolves to that commit today and is verified as of 2026-10-23.

## Conclusion

Within the assigned read-only compare, **no removed/false old fact, no widened Core, no unsupported source attribution, and no promotion mark** were found. New S101/S102 rows are supported by verified byte-identical captures, exact line anchors, a verified tag→commit deref, and internally consistent document-spec checks. The round-33 claim is honestly stopped (unprovable) with scores unchanged; r32 instruments and hashes are untouched. Residual gaps are limited to no-execution (per scope) and the unread design prep doc.
