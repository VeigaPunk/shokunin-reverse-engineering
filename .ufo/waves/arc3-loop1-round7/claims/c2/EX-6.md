# EX-6 — c2 chain (corpus Unknown characterization) — arc3-loop1-round7

Seat: EX-6 · chain c2 · 2026-10-19 · lane `kaidoku-shokunin`.

Target: C2, close one named corpus Unknown. Chosen candidate: bounded characterization of the `inspect_evm_interface` `ev_` ID domain, named open in r3/r4 and carried open in r6. Outcome: **REPRODUCED as a bounded path/canonicalization characterization**. The complete ID formula remains unknown; this is not presented as a universal formula derivation.

Deliverables: corpus knowledge-entry draft at `EX-6/entry-draft/2026-10-19-arc3-r7-evm-evidence-id-domain.md`, proposed map-token patch below, six full probe envelopes and matrix summary under `EX-6/evidence/`.

## First-hand re-derivation and item verdicts

| item | verdict | evidence |
|---|---|---|
| Frozen work revision | **REPRODUCED** | `git cat-file -t 2fba56f` → `commit`; `git log --oneline -3` → `ebdcc8e arc3-loop1-round6: records…`, `2fba56f arc3-loop1-round6: work…`, `c625d5d arc3-loop1-round5: records…`; matches the frozen HEAD/work identifiers. |
| Candidate Unknown remains open at work commit | **VERIFIED** | Read the work-commit corpus source: r3 `corpus/knowledge/2026-10-19-arc3-r3-evm-optimizer-shapes.md:33`, r4 `corpus/knowledge/2026-10-19-arc3-r4-evm-vyper-leg.md:28`, r6 `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`; each still names the full `ev_` ID domain as unknown. These lines identify the question; no prior-round ID value is used as evidence here. |
| Carrier bytes | **VERIFIED** | First-hand `sha256sum` of `.ufo/waves/arc3-loop1-round6/claims/c2/EX-7/out/viair-opt200/runtime.bin` and both `/var/tmp/kaidoku-ex6-arc3-r7/{A,B}/carrier.bin` copies: all `2ec3f557f6f2fb229dc49094981723c6efcce3df10f20363ec1732845c99581a`; `stat` → 1,517 bytes each. Source carrier was read-only. |
| Six REA invocations | **REPRODUCED** | Each `npx -y rea-agents@6.7.0 inspect-evm-interface <path> raw --format json` succeeded. Envelopes identify `evmole-interface`, `evmole@0.9.3`; all contain the same input/decoded SHA-256, 1,517 decoded bytes, 15 normalized functions, and canonical normalized-function-array SHA-256 `3394626e1e49bdb2714faf1fbc942f20dfcbd2a35547a2de18e3c2005adbe1ce`. Full evidence: `EX-6/evidence/{same-path-1,same-path-2,same-path-alt-tmpdir,relative-path-same-file,same-directory-renamed,alternate-path}.json:1`; compact exact matrix: `EX-6/evidence/matrix-summary.txt`. |
| Same-path repeatability | **REPRODUCED** | `same-path-1.json:1` and `same-path-2.json:1` both `ev_a84a565969defaa739ab2567e8da826a284b4a8c4ee1564ec472ab1703b6a09c`; complete envelope SHA-256 for both `9b333d1595188f96328dd0a0effaeeb3e17ea90419cce18dc13c1210c33dbc50`. |
| Path/TMPDIR boundary | **VERIFIED** | Changing only basename (`same-directory-renamed.json:1`) produced `ev_a19a232f0589027e2b528a7fc5ad68ad95034faee95e3ff7ec98281d130f4912`; changing only parent while keeping basename (`alternate-path.json:1`) produced `ev_4634efd77db0fc4d9df111ea38e333651a992c004ccb6a5b5f0361de43843b79`. Both retained identical decoded bytes/function payload. Same resolved absolute path through a relative argument, and same absolute path under a different `TMPDIR`, retained the first ID and byte-identical response envelope (`relative-path-same-file.json:1`, `same-path-alt-tmpdir.json:1`). |
| Complete Evidence-ID formula | **UNVERIFIABLE** | This bounded experiment does not derive the hash inputs or algorithm. Other verbs, versions, encodings, and parameter combinations remain outside its scope; the corpus draft explicitly preserves this residual Unknown. |
| Command A baseline at work commit | **REPRODUCED** | Ran the `SCORECARD.md:88-124` recipe at `REV=2fba56f` → `{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 85, "mapped": 85, "missing": [], "revision": "2fba56f", "rule_blocks": 15}`. |
| 85→86 overlay projection | **REPRODUCED (projection only)** | With the proposed new entry stem and its map token overlaid in memory on the same Command A source-derived sets → `{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 86, "mapped": 86, "missing": [], "revision": "2fba56f", "rule_blocks": 15}`. This is not a post-landing Command A run; the integrator must re-run after landing. |

### Probe commands

All scratch was under `/var/tmp/kaidoku-ex6-arc3-r7`; no `/tmp` scratch was used. The tested commands were:

```bash
TMPDIR=/var/tmp/kaidoku-ex6-arc3-r7/A/tmp npx -y rea-agents@6.7.0 inspect-evm-interface /var/tmp/kaidoku-ex6-arc3-r7/A/carrier.bin raw --format json
TMPDIR=/var/tmp/kaidoku-ex6-arc3-r7/A/tmp npx -y rea-agents@6.7.0 inspect-evm-interface /var/tmp/kaidoku-ex6-arc3-r7/A/carrier.bin raw --format json
TMPDIR=/var/tmp/kaidoku-ex6-arc3-r7/B/tmp npx -y rea-agents@6.7.0 inspect-evm-interface /var/tmp/kaidoku-ex6-arc3-r7/A/carrier.bin raw --format json
(cd /var/tmp/kaidoku-ex6-arc3-r7 && TMPDIR=/var/tmp/kaidoku-ex6-arc3-r7/B/tmp npx -y rea-agents@6.7.0 inspect-evm-interface A/carrier.bin raw --format json)
TMPDIR=/var/tmp/kaidoku-ex6-arc3-r7/A/tmp npx -y rea-agents@6.7.0 inspect-evm-interface /var/tmp/kaidoku-ex6-arc3-r7/A/renamed.bin raw --format json
TMPDIR=/var/tmp/kaidoku-ex6-arc3-r7/B/tmp npx -y rea-agents@6.7.0 inspect-evm-interface /var/tmp/kaidoku-ex6-arc3-r7/B/carrier.bin raw --format json
```

The full output JSON is retained in the evidence directory; each is 11,482 bytes. The envelope reports `confidence: inferred`, `authority: shipped-artifact`, and `runtime_execution: not-performed`. The result comparison concerns evidence identity and normalized output equality only, not runtime behavior or selector/signature truth.

## Landing moves for the parent

1. Copy `EX-6/entry-draft/2026-10-19-arc3-r7-evm-evidence-id-domain.md` to `corpus/knowledge/2026-10-19-arc3-r7-evm-evidence-id-domain.md`.
2. Append the new map token to the EVM row in `corpus/README.md:38`. Proposed patch:

```diff
-| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg`, `2026-10-19-arc3-r6-viair-dispatch-shape` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and from real solc-0.8.37-compiled runtime carriers (arc3-r1); positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-real-solc`, `2026-10-19-arc3-r3-evm-optimizer-shapes`, `2026-10-19-arc3-r4-evm-vyper-leg`, `2026-10-19-arc3-r6-viair-dispatch-shape`, `2026-10-19-arc3-r7-evm-evidence-id-domain` | held — EVMole selectors recovered from a synthetic dispatcher (r3-07) and real solc/Vyper runtime carriers (arc3-r1/r3/r4/r6); positional encoding quirk; arc3-r7 bounds `inspect_evm_interface` evidence-ID path/canonicalization behavior |
```

3. Run Command A on the landed work commit. The measured 86/86 above is only the explicit in-memory overlay projection, not a claim about an unmodified or not-yet-landed worktree.

## Scope and custody

Only this seat's files were written under `.ufo/waves/arc3-loop1-round7/claims/c2/EX-6.md` and `.ufo/waves/arc3-loop1-round7/claims/c2/EX-6/`. The carrier was read-only; scratch and `TMPDIR` were under `/var/tmp`; no source, corpus, map, gate, or git object was modified. The full ID formula remains the explicit residual; the entry's claim is bounded to this one verb/pin/carrier/request matrix.
