# CraftDraft candidate — Go selection-preview decision rows (round 16, w1)

Draft for L1 integration. Not applied to `SKILL.md` or `corpus/README.md`.
Evidence class: source model plus retained installed-data inventory. No held capability, no coverage expansion, no patch engine, no target run.
Authority: `S003` = `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java` in `Base-src.zip` (line anchors below are from that member); data = installed `typeinfo/golang` directory as retained in `.ufo/waves/round-15/inventory.json`.

---

## A. SKILL.md — add to "Installed Go snapshot selection — round 15" (after the table row ending at `SKILL.md:483`)

Add this row to the existing `Signal | Decision | Limit` table:

| Requested Go `M.m.p` needs the installed base/diff that would be selected | Run the read-only selection preview (once its CLI lands; until then, the manual lookup in the status table below). Retain `status`, base path, size, SHA-256, `selected_diff`, `selected_patch`, `arch_search_order`, `base_matching_buckets`, `patch_applied:false` | `evidence_class: source_model`. Preview selects bytes; it does not apply a diff, run Ghidra, or recover any target. Not a held capability (QUALITY.md #10) |

Then add this status table directly after it:

| Preview status | Source rule (`S003`) | Decision | Forbidden shortcut |
|---|---|---|---|
| `missing_base` | Base `go{M}.{m}.0.json` absent from the resource directory: `getApiSnapshotJsonFile` returns null (`:122-126`); `get` returns EMPTY (`:115`) | Record `base: null`, `selected_diff: null`, `selected_patch: null`; stop | A present patch diff cannot rescue a missing base; no fallback to the preceding minor (`getPatchVerDiffFile` is never reached) |
| `base_only` | Base present and no diff chosen: requested patch 0 (exact base, info `:162-164`), or no `go{M}.{m}.{q}.json.diff` for any `q` in `1..p` (warning `:158-160`; base bytes returned `:129-130`) | Use base bytes. For `p>0`, label as base-fallback with `selected_diff: null`; for `p=0`, exact base with no fallback label | The base file's identity is its SHA-256, not the requested label |
| `exact_diff` | `go{M}.{m}.{p}.json.diff` present with `p>0` (loop exits on first hit, `:153-156`) | `selected_diff` = that file, `selected_patch` = `p`; selection only, `patch_applied: false` | Selection is not patch validity or patched-result correctness |
| `fallback_diff` | `p>0`, exact diff absent, nearest lower `q` in `1..p-1` present (`:153-160`) | `selected_patch` = `q`; keep the fallback warning text; label as fallback | The requested label `p` does not name the bytes; `q` names the diff identity |

Search and applicability rules to keep with the table:

- Arch search order is `[goOS-goArch, goOS, "unix" if goOS is unix-like, goArch, "all"]` (`:108-109`). Linux/amd64 = `linux-amd64, linux, unix, amd64, all`. The empty entry for non-unix OS is skipped at match time (`:229-231`).
- Matching is top-level key presence (`:233-237`). An empty object under a present key still counts as present.
- `isInvalid()` is `arches.isEmpty()` after filtering to the search order (`:503-505`). Non-invalid version labels do not imply non-empty buckets; see the boundary cases.
- Diff search covers `q` from `p` down to `1` only; patch 0 is the base, never a diff (`:153`).
- Do not use `getApiFile` (`:183-192`): it has a `go%d.%d.json` filename fallback that is not on the `get` path.
- When `selected_diff` is non-null, `base_matching_buckets` is reported as an unpatched base preview. Diff application may change the top-level key set; this preview does not check that. [INFERENCE — not observed]

Boundary cases to keep as evidence rows (source-model, installed-data-observed where noted):

- `1.26.8` → `missing_base`. Observed: no `go1.26.0.json` in the installed directory; `inventory.json` selection entry `requested: 1.26.8`, `base_present: false`.
- `1.25.7` → `base_only`, base `go1.25.0.json`. Observed: no `go1.25.*.json.diff` in `patchverdiffs/`; `all` bucket present.
- `1.24.7` → `fallback_diff`, `selected_patch: 6`, base `go1.24.0.json` (SHA-256 `aab28c8f…`, 10,039,962 B). Observed: diffs 1.24.1 through 1.24.6 present, `go1.24.7.json.diff` absent.
- `1.24.6` → `exact_diff`, `selected_patch: 6`. Observed: `go1.24.6.json.diff` present.
- `1.24.0` → `base_only`, exact base, no fallback label. [INFERENCE from `:158-164` branch; not separately observed]
- Synthetic temp tree only: diff `go1.27.3.json.diff` present but base `go1.27.0.json` absent → `missing_base`, diff not consulted.
- Synthetic temp tree only: base with only `windows-amd64` key, request linux/amd64 → `base_matching_buckets: []`, `isInvalid()` true (`:503-505`). `GoRttiMapper.java:178-180` still logs "Using Go API snapshot" because the check is version-only, not bucket-based. Source-model reading.

---

## B. corpus/README.md — held-Go coverage map addition (CONDITIONAL)

Placement: corpus coverage map, directly after row at `corpus/README.md:35` (`2026-10-20-r15-go-snapshot-inventory`). The top-level `README.md` has no coverage map (only a "What's here" list), so this addition belongs in `corpus/README.md`.

Do not add this row until its knowledge file exists: `corpus/README.md:9` states "A row is written when its file exists, never before." Once the file exists, add:

| `knowledge/2026-10-20-r16-go-selection-preview` | source-model Go selection preview: requested `M.m.p` → base file identity and nearest-lower diff choice, with fallback labels and bucket applicability; boundary cases for missing base, base-only, exact diff, fallback diff | source-model only — **not held**: no carrier run this round (QUALITY.md #10), no patch application, no target, no provider execution, no coverage expansion | `S003` `GoApiSnapshot.java:105-166,183-192,229-239,503-505`; `GoRttiMapper.java:170-181`; `.ufo/waves/round-15/inventory.json` selection entries; selection fixtures and runner output at the paths L1 records |

Do not use the state word `held` for this row; the coverage map reserves it for carrier-run capability claims.

---

## C. Not in this draft

- No change to existing SKILL/corpus text beyond the two insertions above.
- No claim that `selection.py`, its fixtures, or its runner exist or pass. Those belong to the SelectorModel seat and L1 verification.
- No claim about the historical `op` cause, a Ghidra provider outcome, or patch correctness.
