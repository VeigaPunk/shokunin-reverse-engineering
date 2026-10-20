# CraftDraft report — round 16 w1 (Go selection-preview rows)

Draft written to `.ufo/waves/round-16/w1/CraftDraft.candidate.md`. No existing doc edited. No checks, builds, tests, or CLI runs executed. Installs/updates: none.

## Scope and behavior

- Drafted: (A) one new row plus a four-status table for `SKILL.md` "Installed Go snapshot selection — round 15" (after `SKILL.md:483`); (B) a conditional held-map row for `corpus/README.md` after `:35`.
- Not drafted: coverage expansion, patch engine, target capability, numeric score, or `held` state.
- Placement note: the top-level `README.md` has no coverage map (only a "What's here" list). The held-Go map is `corpus/README.md` coverage map.
- Gate condition on (B): `corpus/README.md:9` says a row is written only when its file exists. The row is held back until `corpus/knowledge/2026-10-20-r16-go-selection-preview.md` (or its L1-chosen name) lands.

## Source anchors (S003, `Base-src.zip` member `ghidra/app/util/bin/format/golang/rtti/GoApiSnapshot.java`, read directly)

| Rule | Anchor | Observed |
|---|---|---|
| Arch search order | `:108-109` | `[goOS-goArch, goOS, unix-if-unix, goArch, all]` |
| Base missing → EMPTY | `:122-126`, `:115` | base `go{M}.{m}.0.json` null → no diff consulted |
| Diff search loop | `:153-156` | `p` down to `1`; patch 0 is never a diff |
| Fallback warning / exact info | `:158-164` | warn if selected ≠ requested; info otherwise |
| Diff apply path (not used here) | `:128-145` | applies selected diff to base; preview does not |
| Version label at read | `:111`, `:239` | label = requested `goVer` regardless of byte source |
| Bucket keep / order | `:229-237` | key presence only; empty-string entry skipped |
| Legacy filename fallback (off get path) | `:183-192` | `getApiFile` `go%d.%d.json`; must not be used |
| `isInvalid` | `:503-505` | `arches.isEmpty()` |
| Consumer version log | `GoRttiMapper.java:170-181` | "Untested" error at `:170-171`; "Using" info at `:178-180` checks `getVer().isInvalid()` only |

## Installed-data facts (retained inventory, `.ufo/waves/round-15/inventory.json` selection entries; directory listing re-read)

- `go1.26.0.json`: absent. `1.26.8` → `missing_base`.
- `go1.25.0.json`: present; no `go1.25.*.json.diff`. `1.25.7` → `base_only`.
- `go1.24.0.json`: present, SHA-256 `aab28c8f7fcf36224f01b883b1f3f13208412d22e4eb0d87d090a258e124c571`, 10,039,962 B. `patchverdiffs/` has `go1.24.1`–`go1.24.6` `.json.diff`; `go1.24.7` absent. `1.24.7` → `fallback_diff`, `selected_patch: 6`; `1.24.6` → `exact_diff`.
- Linux/amd64 bucket keys on the 1.24 and 1.25 bases include `linux-amd64`, `linux`, `unix`, `amd64`, `all` (inventory `os_arch_map_keys`, not the 10 MB JSON re-parsed here).

## Findings

1. The round-15 SKILL table and entry match the source on the points they cite (base-first lookup, nearest-lower diff, requested label versus fallback bytes, `isInvalid` at `:503-505`). No contradiction found.
2. Two source facts the existing text does not state:
   - `GoRttiMapper` logs "Using Go API snapshot" when `getVer()` is non-INVALID, even if the bucket map is empty (`GoRttiMapper.java:178-180`, `:503-505`). Version-only check; not a bucket check.
   - `getApiFile` (`:183-192`) has a `go%d.%d.json` filename fallback that `get` does not use. A preview must not borrow it. The shared contract already forbids it.
3. Missing base wins over any diff: a present diff cannot rescue a missing base. Preview status must read `missing_base` in that case (synthetic boundary case).
4. Requested patch 0 is `base_only` with no fallback label (exact base). Requested patch `p>0` with no diff in the minor is `base_only` with a fallback label (warning at `:158-160`).

## Interpretation to confirm (L1 / SelectorModel)

- Shared contract: "Base-only matching is unpatched preview and must be labelled so when diff selected." I read this as: when `selected_diff` is non-null, `base_matching_buckets` is an unpatched-base preview and must be labelled. Reason: patch application could change top-level keys. This is not observed; the preview never applies a diff. The alternative reading (a `base_only` status cannot coexist with a selected diff) is consistent with the status table and does not change the rows.
- `arch_search_order` for non-unix OS keeps the `""` entry or omits it. The draft says it is skipped at match time; the output shape is for the SelectorModel seat.
- `--request` accepts `M.m.p` only. `GoVer.parse` would default a missing patch to 0 (`GoVer.java`, `parse(s,0)`); whether the CLI should mirror that is a SelectorModel decision.

## Limits and calibration

- Source read directly (archive member, anchors above). Installed-data facts are from the retained round-15 inventory, cross-checked against the current directory listing and `patchverdiffs` glob. The 10 MB base JSON was not re-parsed by me; key presence for linux/amd64 is from the inventory.
- Boundary cases for the 1.25 bucket count and the synthetic `windows-amd64`-only case are source-model reasoning, not observed. Marked `[INFERENCE]` where relevant.
- No `selection.py`, fixture, or runner was inspected or run. No claim that they exist or pass.
- No held capability: QUALITY.md #10 requires a carrier run this round; none was run. The draft labels the row `source-model only — not held`.
- No numeric score is offered. Depth/calibration verdicts belong to L1.

## Artifacts

- Candidate draft: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/w1/CraftDraft.candidate.md`
- Report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-16/w1/CraftDraft.md`
- Scratch files created during reading were removed (`/tmp/r16w1_*`).

## Checks L1 should run after integration

- Only if the selection CLI lands: run its fixture runner once against the boundary cases in the candidate (`missing_base`, `base_only` at 1.25.7 and 1.24.0, `exact_diff` at 1.24.6, `fallback_diff` at 1.24.7, synthetic missing-base-with-diff, synthetic non-matching-bucket).
- Confirm the SKILL row count and table shape render after insertion.
- Confirm the corpus row is added only if its knowledge file exists (`corpus/README.md:9`).
