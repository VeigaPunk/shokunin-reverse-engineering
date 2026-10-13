<!-- corpus entry — kaidoku-shokunin round 3 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r3/14-mcp-session.md. -->

# 14 — Live MCP-session path: retained evidence, `inspect_analysis_view` paging, `record_pairs` verdict

Lane: kaidoku-shokunin, round 3. Date: 2026-10-13. Host: Linux x86_64.
Session: live `rea` MCP server (rea-agents 6.4.0, SDK 2.3.1, negotiated protocol
`2025-11-25`, client `rmcp` 3.1.0), served from
`~/.npm/_npx/dea9475797100b20/node_modules/rea-agents` — a *different* npx cache
root than the round-2 CLI runs (`af752b90495482d7`), same version.
Provider: Ghidra 12.1.4 (`~/.local/opt/ghidra_12.1.4_PUBLIC`) under
`rea-workflow` composed provider. Scratch: `/tmp/rea-mcp-r3/` (bundle exports
kept there for verification; session closed cleanly at end).

Round 2 established `record_pairs` exists only on the MCP `compare_bundles`
input, but exercised it via a direct `dist/domain` call — never the real MCP
tool. This lane ran the whole path inside the live session.

Targets: `/usr/bin/true` (sha256 `8bc9a73a…02d`, 43,320 B ELF PIE) and
`/usr/bin/false` (sha256 `193f3dd1…daed`, 43,320 B) — distinct coreutils
binaries, near-identical layout, real content delta.

## Run log (MCP tool calls, in order)

| # | MCP call | Result |
| - | -------- | ------ |
| 1 | `binary_session {}` | `open:false`, `analysis_provider_binding:null`, Ghidra candidate `available`, `server_identity` rea 6.4.0, catalog 127 CLI / 170 MCP / 6 prompts; `tool_availability` lists per-tool `available:false, reason:"target_required"` pre-open |
| 2 | `open_binary {path:/usr/bin/true}` | `format:elf, arch:x86_64`, sha256 matches `sha256sum` |
| 3 | `binary_overview {}` | `ev_982c6020…71a8`, provider `rea-workflow`; 206 procedures, 154 strings, 31 segments |
| 4 | `inspect_analysis_view` on ev_982c (view `summary`) | **FAIL** typed `unsupported_target`: parent op must be `inspect_binary_layout`, `analyze_javascript_application` or `analyze_function` — `binary_overview` records are not pageable |
| 5 | `inspect_binary_layout {path, detail:"summary"}` | **FAIL** `provider_unavailable` (retryable) — only candidate `pwntools-elf`, needs `REA_PWNTOOLS_PYTHON` (pwntools 4.15.0/pyelftools 0.33/Unicorn 2.1.2); corroborates r2 "doctor blind to aux providers" |
| 6 | `analyze_function {procedure:"entry"}` | `ev_5db3a3e0…a216`, provider `ghidra` direct; `entry` @ 0x102560, canonical `_start` (ENDBR64, XOR EBP, `__libc_start_main`, HLT) |
| 7 | `inspect_analysis_view` `{retained-evidence ev_5db3…, view:{native,assembly,off:0,lim:4}}` | `ev_7f15960c…421e`; `parameters.parent_evidence_id` set; `coverage:{status:"page",examined:4,total:13,next_offset:4}` — **retained-evidence paging works live** |
| 8 | same, `offset:4,limit:4` | `ev_53f8e30b…5bd4`; items continue contiguously (`MOV RDX,RSP` … `PUSH RSP`), `next_offset:8` |
| 9 | `export_evidence_bundle {/tmp/rea-mcp-r3/true-bundle.json}` | 50,829 B, **4 records** (overview + fn + 2 view pages) |
| 10 | `close_binary {}` → `open_binary {/usr/bin/false}` | clean close; false opened |
| 11 | `binary_overview {}` (false) | `ev_cfb0e80a…40fa`; 206 procedures, **156 strings** (vs 154) |
| 12 | `analyze_function entry` (false) | `ev_c00317c6…7fc6`; `entry` @ 0x102570 (+0x10 vs true), `FUN_00102480` body 227 B vs 218 B |
| 13 | `export_evidence_bundle` → `false-bundle.json` | 35,971 B, **2 records** — true's records evicted at the target switch |
| 14 | `compare_bundles {left:true-bundle, right:false-bundle}` (no pairs) | `status:unknown`, `unresolved:6`, all records `unresolved_branch` — CLI-equivalent ceiling reproduced **through the MCP tool** |
| 15 | `compare_bundles` + `record_pairs` [overview↔overview, fn↔fn] | paired records → `changed`/`observed_change` (`records_changed:2`) but `status:unknown` still — 2 unpaired view-records leave `unresolved:2` |
| 16 | `close` → `open(true)` → `binary_overview` + `analyze_function entry` | **identical ids** `ev_982c6020…` / `ev_5db3a3e0…` — content-addressed determinism holds across target close/reopen in-session |
| 17 | `export_evidence_bundle` → `true-bundle-paired.json` | 35,967 B, 2 records (exactly the pairable set) |
| 18 | `compare_bundles` + same `record_pairs` on paired bundles | **`status:"changed"`, `records_changed:2`, `unresolved:0`**, both `conclusion_kind:"observed_change"`, verdict `ev_367db735…ed7c` — round-2's MCP-only gap closed |
| 19 | `get_evidence_bundle {detail:"summary"}` | `total_retained_records:5` incl. **false's** records + verdict `ev_367d`; earlier verdicts (ev_7490…, ev_c6b9…) and first-window view pages absent — retention is an epoch, not a bag |
| 20 | `inspect_analysis_view` on ev_c00317c6 (false dossier) **while true is open** | works — pseudocode facet, `{unit:"utf16-code-units", total:280, next_offset:20}`; retained evidence outlives its own target's close |
| 21 | `export_evidence_bundle` → `late-bundle.json` | 82,239 B, **6 records** (verdict + both targets' records + cross-target view) |
| 22 | `close_binary {}` | clean drain/close |

## Candidate: `compare_bundles.record_pairs` produces `status:changed` through the real MCP tool — but only when *every* bundle member is paired

- claim: the MCP `compare_bundles` tool accepts
  `record_pairs:[{left_evidence_id,right_evidence_id}]` and reclassifies each
  pair `changed`/`observed_change`, exactly as round 2's domain call showed —
  now demonstrated on the live MCP surface. New refinement: **the bundle-level
  `status` folds in unpaired members.** Pairing 2 of 4 records left
  `unresolved:2` and the verdict stayed `unknown` (row 15); exporting a
  2-record bundle whose members were all paired gave `status:"changed"`,
  `unresolved:0` (row 18). To get `changed` on a real session bundle, either
  pair every record or keep exports tight (one record kind per target window).
- source: run log rows 14–18; verdict evidence `ev_367db735b7dd1f859ea36119a7c727cc34a5b8added883e8466f7c882492ed7c`; bundles `/tmp/rea-mcp-r3/{true-bundle-paired,false-bundle}.json`.
- verify: open `/usr/bin/true` via MCP, collect `binary_overview` +
  `analyze_function entry`, `export_evidence_bundle`; repeat for
  `/usr/bin/false`; call `compare_bundles` with the two op-matched pairs →
  `status:changed`, `unresolved:0`. Ids are deterministic: expect
  `ev_982c6020…`/`ev_5db3a3e0…` and `ev_cfb0e80a…`/`ev_c00317c6…` verbatim.
- verified-at: 2026-10-13
- suggested: admit — first live-MCP `status:changed`; refines r2's claim with
  the all-members-paired precondition (r2's domain call happened to pair all 4).

## Candidate: `inspect_analysis_view` retained-evidence paging works inside a live session — the capability the CLI cannot express

- claim: `inspect_analysis_view {source:{kind:"retained-evidence",
  evidence_id:<same-session id>}, view:{kind:"native",facet,offset,limit}}`
  pages an already-collected record without re-analysis: each call mints a new
  `rea.analysis-view` record carrying `parent_evidence_id`, `parent_digest`,
  `view_digest`, and `coverage:{status:"page",examined,total,next_offset,
  exhausted}`. Demonstrated on `assembly` (rows 7–8: 13 items, two contiguous
  pages) and `pseudocode` (row 20: 280 UTF-16 code units, paged by
  `utf16-code-units` unit). Parent-op gate is real: `binary_overview` records
  get typed `unsupported_target` (row 4); pageable parents are
  `inspect_binary_layout`, `analyze_javascript_application`,
  `analyze_function`.
- source: run log rows 4–8, 20; view records `ev_7f15960c…`, `ev_53f8e30b…`,
  `ev_b4d4b909…`.
- verify: in one MCP session, `open_binary` + `analyze_function {entry}` then
  call `inspect_analysis_view` with the returned id and varying `offset` —
  `coverage.next_offset` walks the facet; `parent_evidence_id` chains back.
- verified-at: 2026-10-13
- suggested: admit — plus record the parent-op gate and the
  `unsupported_target` code as taxonomy.

## Candidate: session retention is epoch-scoped and cross-target — `get_evidence_bundle` is the live discovery surface

- claim (partly inference): `export_evidence_bundle` and
  `get_evidence_bundle {detail:"summary"}` reflect the session's *current*
  retained set, not a cumulative log. Observed: exports wrote 4 → 2 → 2 → 6
  records (rows 9,13,17,21). `close_binary`+`open_binary` evicted the prior
  target's records — *unless* re-cited: false's two records survived the second
  switch because verdict `ev_367d`'s `evidence_links` reference them (row 19),
  and they remained pageable cross-target while `true` was open (row 20). The
  two earlier compare verdicts and first-window view records — uncited in the
  current epoch — were dropped. Re-collecting the same op on the same binary
  yields the identical content-addressed `ev_*` id (row 16), so eviction is
  cheap: re-observation is deterministic, not reconstructive.
- source: run log rows 9–21; summary payload lists `retention:"complete-record"`,
  `native_dossier.available`, per-record `analysis_profile_digest`.
- verify: repeat rows 10–21; check that an unpaired-member `compare_bundles`
  verdict (v1/v2 shape) disappears from `get_evidence_bundle` summary after the
  next target switch while a pair-cited record persists.
- verified-at: 2026-10-13
- suggested: admit the observed half (exports are current-retention snapshots;
  cited records survive target switch; uncited records evict; ids re-derive
  identically). The pinning mechanism is inference — flagged, testable.

## Candidate: `inspect_binary_layout` is `pwntools-elf`-gated and refuses closed with a named remediation when absent

- claim: MCP `inspect_binary_layout` selects only candidate `pwntools-elf`;
  without `REA_PWNTOOLS_PYTHON` it fails `provider_unavailable` (retryable)
  before touching the target — consistent with r2's "doctor is blind to aux
  providers" (doctor green while this verb is dead) and r2's crash-probe
  provisioning path (uv venv + pinned pwntools/pyelftools/Unicorn).
- source: run log row 5; error `details.rejections[0].reason` names the env key
  and exact version pins; r2 `06-crash-probe.md`, `11-caps-catalog.md`.
- verify: `inspect_binary_layout {path:/usr/bin/true}` with and without
  `REA_PWNTOOLS_PYTHON` exported.
- verified-at: 2026-10-13
- suggested: admit — corroborating instance on the MCP surface; the
  `detail:"summary"` + `parent_evidence_id` paging route for layout evidence
  remains untested until the provider is provisioned.

## Summary

**MCP session path: DEMONSTRATED end-to-end.** All four task goals held inside
one live `rea` MCP session: `binary_session` reports a healthy server
(rea-agents 6.4.0, Ghidra 12.1.4 candidate, `tool_availability` gating on
`target_required`); `open_binary`/`analyze` on `/usr/bin/true` produced
retained evidence; `inspect_analysis_view` paged that evidence by
`parent_evidence_id` across two facets and — newer — paged `/usr/bin/false`'s
dossier while `true` was the open target; and `compare_bundles` with
`record_pairs` returned **`status:"changed"` with `unresolved:0`** on two
analyzed artifacts, closing round 2's MCP-only gap. Two honest failure modes
also banked: `inspect_analysis_view` refuses `binary_overview` parents
(`unsupported_target`, non-retryable), and `inspect_binary_layout` is dead
without `REA_PWNTOOLS_PYTHON` (`provider_unavailable`, retryable). One
behavioral refinement and one new mechanism: `status:changed` requires every
bundle member paired (unpaired leftovers pin the verdict at `unknown`), and
session retention is epoch-scoped — records evict at target switch unless
re-cited, with content-addressed ids making re-collection byte-identical.

## Errata (round 4)

- **Evidence-id sensitivity refined (r4, three-lane corroboration):** evidence ids are
  `f(content, path, params)` — content-addressed AND path-sensitive. Same bytes at a
  different path mint a different id (independently confirmed by the revenger verifier:
  `ev_8efa2368…` vs `ev_50038b96…`; jadx verbs mint per-run ids via mkdtemp paths; apktool
  verb ids are deterministic on identical invocations; `trace-application-feature` re-mints
  the identical id on same-path re-run). Cite `subject.digest.sha256` for cross-path
  identity; "content-addressed" alone is incomplete.
