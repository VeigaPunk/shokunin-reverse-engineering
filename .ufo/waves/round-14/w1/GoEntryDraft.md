# Round 14 — GoEntryDraft (C1 candidate): Go RTTI bootstrap edge class

Seat: `KaidokuR14.GoEntryDraft` (leaf executor). Round 14, wave `kaidoku-r14-w1`.
Axes: C1 is **depth** per `.ufo/waves/round-14/claims-review.json` (reclassified from coverage without reducing scope); C2 calibration is untouched by this seat.
Writes: two files only — the candidate entry `.ufo/waves/round-14/w1/GoEntryDraft.candidate.md` and this report. No shared file, LOG, SCORECARD, corpus, registry, manifest, fleet file, or sibling file was written.
Tools installed/upgraded: **none**. No builds, tests, linters, formatters, smoke runs, REA calls, Ghidra analyses, or target executions were run. Network use was read-only: the pinned GitHub commit `385e8cd…` and one GoReSym README fetch (S005, later not cited); the C2 gate was not run (not this seat's artifact).

## Result

The candidate is a source-conditional diagnosis of one edge class: a Go binary whose Ghidra symbol recovery collapses because the **Go RTTI bootstrap never completes**. Its load-bearing claims:

- `OBSERVATION` — installed 12.1.4 declares `1.15-1.25` (`GoRttiMapper.java:79`) and, when a version is outside it, only logs `Untested Go version [%s]` (`:171`); control continues to the snapshot lookup at `:176`.
- `OBSERVATION` — the snapshot lookup keys on the base `major.minor`, has no cross-minor fallback, and returns `GoApiSnapshot.EMPTY` on a miss (`GoApiSnapshot.java:115,122-126,148-166`). Installed data has 11 base JSON snapshots (1.15.0–1.25.0), zero `1.26` files, 123 patch diffs, and zero 1.25 patch diffs.
- `OBSERVATION` — the shipped 9 `golang_*.gdt` archives are not a fallback: `GoRttiMapper` calls `super(program, null)` (`:331`), `archiveDTM` stays null, the archive branch is guarded (`DataTypeMapper.java:282-289`), and the 12.0 change record says JSON replaced gdt (`ChangeHistory.md:585`, under `:564`/`:582`). A source-tree sweep for `golang_` returns 0.
- `OBSERVATION` — with an invalid snapshot, `registerStructure` throws `Missing struct definition…` (`DataTypeMapper.java:172-181`), and `initStructMappings` converts it to `Missing Go bootstrap type info, unable to extract Go RTTI info.` only on the `apiSnapshot.isInvalid()` branch (`GoRttiMapper.java:356-359`); `getSharedGoBinary` then returns null and the analyzer aborts (`GolangSymbolAnalyzer.java:133-137`).
- `OBSERVATION` — `isInvalid()` is `arches.isEmpty()` (`GoApiSnapshot.java:503-505`) and `read` filters by exact GOOS/GOARCH names (`:205-239`), so the same message also covers an OS/arch-exclusion; the message alone is **not** version proof.
- `INFERENCE (conditional)` — for a `go1.26.x` build, the base-file miss is unconditional and version-driven, so the empty-snapshot→bootstrap path is source-determined on stock 12.1.4. This is **not** a causal proof of the retained op-pair collapse.
- `UNKNOWN` — the original cause of the r4-10 11,595-procedure outcome. Its log artifact is gone, the message is not version-unique, and no rerun exists.
- Boundary requested by L1: `inspect_go_binary` is a separate built-in target-free metadata parser (S001 `:167-169`), demonstrated on a go1.26.5 binary in `2026-10-16-l7-01-inspect-go-binary.md`; the Ghidra RTTI gate says nothing about that route.

The candidate carries an explicit new diagnostic question, an observation/inference/unknown label on every bullet, a six-row differential decision table with "what it does not establish", a bounded-scope section, and the `source:` / `verified-at:` / `recheck:` trio first.

## Sources opened (2026-10-20)

All quotes are verbatim contiguous substrings ≤25 words, except the S001 sentence whose source wraps a line (noted). Access date is 2026-10-20 for every row.

| id | source and location | quote | limitation |
|---|---|---|---|
| S001 | `/home/vgpnk/.agents/skills/reverse-engineer-anything/SKILL.md:167-169` (SHA-256 `c8639823…49da0`) | `This built-in target-free inspection requires no Go installation or disassembler.` (10 words; source breaks the sentence across lines 168–169, normalized to one space) | documents routing only; no execution |
| S003 | `Base-src.zip` (SHA-256 `f00d29c…8d804`), `GoRttiMapper.java:79` | `public static final GoVerRange SUPPORTED_VERSIONS = GoVerRange.parse("1.15-1.25");` (7 words) | shipped source archive; member SHA-256 `2415ceb…1d95` |
| S003 | same, `GoRttiMapper.java:170-171` | `Msg.error(GoRttiMapper.class, "Untested Go version [%s]".formatted(goVer));` (5 words) | log-only branch; no throw |
| S003 | same, `GoRttiMapper.java:331` | `super(program, null);` (2 words) | no GDT archive attached to the mapper |
| S003 | same, `GoRttiMapper.java:356-359` | `"Missing Go bootstrap type info, unable to extract Go RTTI info."` (11 words) | emitted only on the invalid-snapshot branch |
| S003 | same, `GoRttiMapper.java:363-365` | `Invalid Go bootstrap struct mapping info: %s` (6 words) | the distinct valid-snapshot failure message |
| S003 | same, `GoApiSnapshot.java:115` | `return GoApiSnapshot.EMPTY;` (3 words) | member SHA-256 `765d253…eb7d` |
| S003 | same, `GoApiSnapshot.java:242` | `public static final GoApiSnapshot EMPTY = new GoApiSnapshot(GoVer.INVALID, Map.of());` | EMPTY definition |
| S003 | same, `GoApiSnapshot.java:503-505` | `return arches.isEmpty();` (3 words) | invalid = no matched arch |
| S003 | same, `DataTypeMapper.java:172-181` | `Missing struct definition for class %s, structure name: [%s]` (9 words) | member SHA-256 `53ff4eb…6ff` |
| S003 | same, `DataTypeMapper.java:282-289` | `if (dataType == null && archiveDTM != null)` (8 words) | archive branch reachable only with an archive |
| S003 | same, `GolangSymbolAnalyzer.java:133-137` | `Go symbol analyzer error: unable to get GoRttiMapper` (7 words) | member SHA-256 `b9b7099…b80` |
| S004 | `https://github.com/NationalSecurityAgency/ghidra/commit/385e8cd923d09f10b1a7874108e71748875fa174` | `GP-6528 add support for golang 1.26` (commit title) | master history, not a release; 10 files; `go1.26.0.json` body not opened |
| S007 | `/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/docs/ChangeHistory.md:564,582,585` (SHA-256 `c6b2530…65c4`) | `Changed method of bootstrapping Go type info to use json Go snapshot files instead of gdt files.` (17 words) | installed release's own record; a short excerpt is not a full compatibility statement |
| — | `corpus/knowledge/2026-10-13-r4-10-real-version-pair.md:29,34,64-74` | retained record only (no re-quote of the mechanism sentence; paraphrased) | round-4 measurement, scratch deleted, not rerun |
| — | `.ufo/waves/round-14/w1/InstalledGoGate.md` §2–§4 | fleet K1 trace | concurrent author-side trace; credited, not independent admission |

Deliberately **not** cited in the entry: S005 (GoReSym) and S006 (BSim). Their scopes do not bear on the bootstrap edge class; the parent directed dropping them from the main diagnosis, and S006 is additionally scope-risky for a version-gate entry (ReviewRegistry F3).

## Exact counts and commands (all 2026-10-20)

- Base JSON snapshots: **11** — `ls /home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/Features/Base/data/typeinfo/golang/go*.json | wc -l`.
- Any `1.26` data file: **0** — `find …/typeinfo/golang -name '*1.26*' | wc -l`.
- Patch diffs: **123** — `ls …/typeinfo/golang/patchverdiffs | wc -l`.
- 1.25 patch diffs: **0** — `ls …/patchverdiffs | grep -c '^go1\.25'`.
- Legacy GDT archives: **9** — `ls …/typeinfo/golang/*.gdt | wc -l` (`golang_1.15_anybit_any` … `golang_1.23_anybit_any`).
- Source references to `golang_` in the full Base source extraction: **0** — `unzip -q <zip> -d <tmp> && grep -rn 'golang_' <tmp> | wc -l`.
- Upstream commit files: **10** — GitHub API `files` array; `go1.26.0.json` listed as added (no patch hunk shown).
- No package (`pacman`/`uv`/`npm`/`cargo`) was installed or upgraded.

## Quote-fidelity self-check (not the C2 gate)

I ran a local substring assertion over every quoted fragment against the actual source bytes (zip members, S007/S001 files, S004 API JSON): **14/14 citations resolve at their stated location** — 13 exact byte substrings plus the S001 sentence, which is exact after whitespace normalization because it wraps lines 168–169 (the candidate states this explicitly). This is a self-check of my own citations, not an execution of `quote-fidelity.py`, not a gate result, and not an admission.

## Calibration and depth notes

- The entry deliberately refuses two shortcuts: "range gate rejects 1.26" and "missing-bootstrap message proves the version caused the collapse". The first is contradicted by `:171`; the second by `isInvalid() == arches.isEmpty()` and the arch filter.
- It preserves the original cause as `UNKNOWN` and treats the source path as conditional, per L1's instruction and the missing log artifact.
- It distinguishes installed-source range (L2), installed data (L3), bootstrap mapping (L4), upstream commit (L5), and parser layout (L6), and states that L6 is not reached when L4 aborts.
- The old r4-10 entry is **not** rewritten; the candidate says L1 owns any append-only correction. Its operational pairing conclusion is preserved.

## Risks and handoff for L1

1. **Registration order**: the destination `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md` does not exist yet. Per `CORPUS.md:46` and ReviewRegistry F1/F2, write the file first, then README/used-by rows.
2. **Old-entry correction** is L1's append-only edit; do not rewrite r4-10. The new entry supersedes the unsourced mechanism attribution, not the measured symptom.
3. **Quote gate**: S003 quotes are Java inside a zip, so the C2 Markdown-section gate cannot express them (ReviewRegistry F4). The candidate's `recheck:` uses commands, not the gate. Do not claim the C2 gate covers S003.
4. **S004 is an API view**: `go1.26.0.json` content and any release containing GP-6528 remain unopened. Do not promote the commit to a host capability.
5. **S007 is a short excerpt** under the 12.0 release heading; it establishes the gdt→JSON switch, not a full per-version capability matrix.
6. **Fresh-import assumption** for the GDT conclusion is stated in the candidate; programs with pre-existing Go types are `UNKNOWN`.
7. **No blockers.** If L1 wants the entry to cite S005/S006 for registry row coverage, that is a deliberate scope decision I did not take; citing them for this edge class would be padding.
8. **Claim-source reconciliation (L1, required).** Frozen `claims.json` C1 lists sources `S003,S004,S005,S006`; the integrated artifact cites `S001,S003,S004,S007`. This is not drift: L1 steering after dispatch directed (a) dropping GoReSym/BSim as main-diagnosis padding, (b) opening/citing `ChangeHistory.md:585` (S007) for the 12.0 gdt→JSON switch, and (c) permitting S001 for the `inspect_go_binary` path boundary. S007 was not in the original claim list and S005/S006 are no longer cited. Registry `used-by` must follow the artifact, not the stale claim list; either `claims.json`/`claims-review.json` records the substituted source set or the claim note explains it in the round-14 lesson. `RegistryDeltaDraft` has independently verified the final token counts (`S001=1, S003=1, S004=1, S007=1, S005=0, S006=0`) and revised its delta accordingly.

## Not run (explicit)

No build, test, linter, formatter, smoke run, `sources-census.sh`, C2 gate, REA verb, Ghidra import, or target execution. The only network operations were read-only GitHub API/raw fetches for S004 (and earlier S005 while deciding scope; S005 is not cited in the final entry).
