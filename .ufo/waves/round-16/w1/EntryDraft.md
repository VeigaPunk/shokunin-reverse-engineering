# EntryDraft — round-16 w1 report

## Behavior

Drafted the selection-preview knowledge entry as a candidate only: `.ufo/waves/round-16/w1/EntryDraft.candidate.md`. It covers provenance trio (`source:`, `verified-at:`, `recheck:`), source-law anchors, the selection algorithm, status labels with what each does not establish, boundary cases, exact model command form, and limits. No corpus, README, SOURCES, LOG, SCORECARD, or SKILL file was edited. Nothing was committed.

## Gates

- No `selection.py`, `selfcheck.py`, build, test, lint, or smoke run. The recheck command in the draft is the contract form and is marked not run.
- No JSON patch applied. No Ghidra or Java execution. No target or carrier touched.
- `sha256sum`, `stat`, and `jq -c keys` were read-only fact reads.

## Touched surfaces

- Written: `.ufo/waves/round-16/w1/EntryDraft.candidate.md` (new), this report.
- Read only: `Base-src.zip` member `GoApiSnapshot.java` (numbered with `unzip -p | cat -n`), `GoVer.java`, installed `typeinfo/golang` bases and diffs, `corpus/knowledge/2026-10-20-r14-go-version-diagnosis.md`, `corpus/knowledge/2026-10-20-r15-go-snapshot-inventory.md`, `corpus/SOURCES.md`, `corpus/lessons/round-15-verifier-spotcheck.md:181-188`, `.ufo/waves/round-16/wave1-spec.json`, `.ufo/waves/round-16/claims.json`.

## Findings

1. **Line anchors verified against the numbered member.** `get` `:102-116` (search order `:108-109`, EMPTY `:115`); `getApiSnapshotJsonFile` `:118-146` (base `:122`, null base `:124-125`, base-only `:128-131`, patched branch `:133-145`); `getPatchVerDiffFile` `:148-166` (walk `:153-156`, warn `:158-161`, info `:162-164`); `read` `:205-240` (requested `ver` `:239`); `EMPTY` `:242`; `isInvalid` `:503-505`. The r14 and r15 anchors I checked (`:111`, `:115`, `:122-126`, `:148-166`, `:239`, `:503-505`) match the shipped member.
2. **Source archive digest matches the round-14 pin** (`f00d29c2…d804`). The data files and diffs were hashed in this seat (table in the candidate).
3. **Data facts agree with the round-15 inventory.** 11 bases (1.15.0–1.25.0), 123 diffs, per-minor histogram identical, no 1.25 diffs, 1.24.7 falls back to 6. Every base has the linux-amd64, linux, unix, amd64, all, windows-amd64, and windows keys (jq read). Full key lists were read only for 1.15.0 and 1.24.0.
4. **Calibration points the draft records:**
   - A missing base returns before the diff walk, so diffs never rescue it (`:124-125`).
   - `EMPTY` has version INVALID, so the requested label is lost on that path (`:242`).
   - The `Falling back` warning fires when no diff is selected (`:158-161`), including `base_only` for 1.25.x.
   - Source `GoVer.parse` accepts `1.24`, `1.24.-1` (→1.24.0), and `1.24.7-rc1`. The strict preview rejects them, so it is not equivalent to Ghidra there.
   - `getFuncdef` and `getTypeDef` dereference bucket fields without null checks (`:516`, `:526`). Marked [INFERENCE FROM SOURCE].
5. **Not established by this seat:** patched bucket content (JsonPatch/JsonPatchApplier not opened), any `selection.py` output, and the emitted form of the `""` placeholder in `arch_search_order`. The draft marks each of these as unpinned.

## Out-of-scope items

- Routed round-15 items 2–4 (baseline discoverability, command provenance, SHONEN wording) are not addressed here. Item 1 (`-I`) is reflected in the recheck form, and the append-only correction belongs to CorrectionDraft.
- No coverage, patch-engine, or target capability claim. No numeric score.

## Artifact paths

- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/w1/EntryDraft.candidate.md`
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/w1/EntryDraft.md`

## Tool installs or updates

None. `jq` (`/home/vgpnk/.local/bin/jq`, jaq 3.1.1 reported by `jq --version`) was already present and used read-only.

## Checks for L1 after integration

- Once `.ufo/waves/round-16/selection.py` exists, run the draft's recheck command, then compare its output against the source-derived expectation. Do not quote output before the run is recorded.
- Confirm the `""` placeholder form in `arch_search_order` and update Limit 11.
- Re-hash `Base-src.zip`, `go1.24.0.json`, and `go1.24.6.json.diff` against the table before integrating.
- Confirm no sibling seat (CorrectionDraft, RegistryDraft, LessonDraft, CraftDraft) reuses a different recheck form.
