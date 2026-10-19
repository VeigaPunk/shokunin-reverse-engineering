# CR-5 — verdict and convergence (arc3-loop1-round9)

Measured source revision: `947091d6b6f52684faf9ca53adf94ff8a0f6b006` (`git rev-parse HEAD`). The frozen contract is `.ufo/waves/arc3-loop1-round9/claims-frozen.md:14-56`. This artifact separates the measured subclaims from their integration conditions; it does not assign a scalar result.

## C1 — freshness

### Per-item verdicts

- **VERIFIED — current archive-file count.** Independent direct-child enumeration of `/var/cache/pacman/pkg/` found `archive_files=1350`, `matching_sidecars=1350`, `archives_without_sidecar=0`, `sidecars_without_archive=0`; arithmetic against the recorded `1556` is `delta_vs_recorded_1556=-206`. The command counted filenames only; it did not cryptographically verify every signature. The row under review is `PROVINCE.md:50`; the enclosing table is dated at `PROVINCE.md:40`.
- **UNVERIFIABLE — the historic 1,556 filesystem state.** `corpus/knowledge/2026-10-13-pacman-packages.md:21-25` records that count and its command at the time; the extant erratum calls it a dated snapshot and records the later 1,350/−206 result at `:73-83`. The old cache cannot be reconstructed from the current filesystem, so 1,556 is a recorded historical value, not a fresh measurement.
- **VERIFIED — installed `jq` identity for this recheck.** `pacman -Q jq` → `jq 1.8.2-1`; `pacman -Qkk jq` → `jq: 25 total files, 0 altered files`; installed `/usr/bin/jq` and the cached archive member both SHA-256 to `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`.
- **UNVERIFIABLE — current `available:true` REA-session status.** The 2026-10-13 host survey records the observation (`PROVINCE.md:40,50`); no current `binary_session {}` result was available to refresh it.
- **CORRECTED — proposal only, not landed.** The evidence supports a same-row replacement that dates the old snapshot, the historical availability observation, and the fresh `jq` check. This synthesized wording avoids implying current REA availability or whole-cache cryptographic signature validation:

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` recorded in the 2026-10-13 host survey; current-session status not re-probed); pacman `.pkg.tar.zst` cache: 1,556 archive files recorded 2026-10-13 (historical snapshot; re-read 2026-10-19: 1,350 archive files and 1,350 matching `.sig` sidecars, −206 vs recorded count; sidecar presence is not cryptographic verification; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` byte-identical to cached archive member (reverified 2026-10-19; SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`) |
```

This is one physical row, preserving the 162-line file length if applied. PL-2's proposal is a close integration candidate (`claims/c1/PL-2.md:20-34`); the alternatives likewise converge on dating both mutable values (`claims/c1/EX-3.md:19-30`, `claims/c1/RV-4.md:28-43`). No source edit was made here.

### Instrument condition — DISCREPANCY

Fresh `python3 .ufo/gates/c1-census-v10.py --quiet` on the measured HEAD returned:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1870 loci=11
SKILL.md       lines=413  loci=2
SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=17, SKILL.md=3; total loci=19; floor=1/file)
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
gate_exit=1
```

The failing locus is `SCORECARD.md` block `1833-1839`, line `1834`, pin `6.7.0` outside the gate's declared scope ending at line 1813 (`.ufo/gates/c1-census-v10.py:264-277`; `SCORECARD.md:1833-1839`). Multiple C1 scratch-after runs reproduce this same failure (`claims/c1/EX-3.md:46-48`, `claims/c1/PL-2.md:38-50`). The frozen requirement that the instrument still read PASS is therefore **DISCREPANCY / unmet**. A Province-row-only change does not clear the unrelated finding; do not report a whole-gate PASS.

## C2 — coverage

### Selected residual and independent re-derivation

I select the frozen Vyper candidate (c), narrowed to residual compiler-output byte behavior for the exact K8 source and Vyper build (`claims-frozen.md:30-42`). I recompiled `.ufo/waves/arc3-loop1-round9/claims/c2/CR-2/evidence/K8.vy` twice with each spelling, using the local Vyper executable `.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper` and `TMPDIR` under `/var/tmp`:

```text
source_sha256=62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d
compiler=0.4.3+commit.bff19ea2
bytecode=identical
bytecode_runtime=identical
abi=identical
method_identifiers=identical
settings=identical
runtime_decoded_bytes=617
runtime_sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
```

I then ran a separate 31-format matrix (124 successful compiles: each flag × two repeats × 31 `-f` formats) on EX-10's byte-identical K8 source. Exact summary from that run:

```text
formats_tested=31 compile_calls=124
raw_equal_count=28 raw_different=['ast', 'annotated_ast', 'archive']
canonical_or_payload_equal_count=31 content_different=[]
```

The comparison basis was canonical JSON for parseable JSON outputs, ZIP member payloads for `archive`, and raw bytes otherwise. Focused repeat checks show why the raw differences must not be overread:

```text
ast: raw_repeat_equal_noopt=False raw_repeat_equal_none=False cross_raw_equal=False normalized_content_equal=True normalized_repeat_equal=True
annotated_ast: raw_repeat_equal_noopt=False raw_repeat_equal_none=False cross_raw_equal=False normalized_content_equal=True normalized_repeat_equal=True
archive (fast four-call run): raw_repeat_equal_noopt=True raw_repeat_equal_none=True cross_raw_equal=True archive_timestamp_variance=False
archive (four calls separated by 2.1 s): raw_repeat_equal_noopt=False raw_repeat_equal_none=False cross_flag_raw_equal=False member_payloads_equal_across_all=True timestamps_equal_across_all=False
```

Thus the five common compiler outputs tested by CR-2/3/4 and EX-7/9 are correctly reported identical (`claims/c2/CR-2.md:7-9`, `CR-3.md:14-26`, `CR-4.md:9-12`, `EX-7.md:21-24`, `EX-9.md:7-11`). EX-10's wider matrix adds the residual: AST raw encodings differ despite canonical JSON equality; ZIP bytes may vary while archive members remain equal and timestamps vary. The measurements do not establish an option-specific semantic difference or attribute every changed ZIP byte exclusively to timestamps. EX-10's retained full results are `claims/c2/EX-10/evidence/measure.txt:3-18,34` and `compile/comparison.json:26-36,38-43,159-169,312-323`; its report states the same limits at `EX-10.md:7-10`.

### Candidate reconciliation

C2 seat reports now cover all twelve rostered seats (`CR-1`–`CR-4`, `EX-5`–`EX-12`). The candidates are distinct and several are independently well-supported: EX-5/EX-12 test other solc minor versions (`EX-5.md:3-11`, `EX-12.md:5-19`); EX-6/EX-8 test the r6 fallback gap (`EX-6.md:3-15`, `EX-8.md:3-14`); CR-1/EX-11 test other Evidence-ID operation domains (`CR-1.md:5-13`, `EX-11.md:3-19`); and CR-2/3/4/EX-7/9/10 test the Vyper boundary.

There is no unanimous verdict-seat candidate. CN-1, VZ-3, and CR-7 prefer EX-8; CN-4 prefers EX-6; CN-2 prefers EX-11; CN-3 prefers CR-1; VZ-1 and CR-8 prefer the narrower Vyper creation-bytecode result. CN-4 argues the Vyper issue may already be covered by R8's selected-output equivalence; CR-6 rejects treating the narrow result as a duplicate and recommends EX-10's broader residual-output comparison, as does VZ-4. VZ-2 instead prefers EX-5's solc 0.8.28 comparison. Other verdicts include CR-6's rationale that R8 does not report creation-bytecode comparison and EX-10's wider residual sweep (`claims/verdicts/CN-1.md:46-50`, `CN-2.md:62-79`, `CN-3.md:19-25`, `CN-4.md:38-83`, `VZ-1.md:44-68`, `VZ-2.md:90-94`, `VZ-3.md:46-48`, `VZ-4.md:59-83`, `CR-6.md:67-69`, `CR-7.md:40-62`, `CR-8.md:82-110`). Earlier missing-report counts in some verdicts are time-of-check snapshots; all twelve C2 seat reports were present at this verdict pass.

My selection is **EX-10's single residual-output entry/token**, because it directly tests the frozen candidate's “any residual byte-level distinction” and the 31-format census is broader than r8's runtime-focused comparison (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:7-17`). This is a bounded recommendation, not peer unanimity. Do not co-land the overlapping drafts or another candidate as part of this one C2 move.

### Coverage landing — UNVERIFIABLE

My direct Command A run against immutable HEAD via the recipe at `SCORECARD.md:88-124` returned:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15}
```

No new C2 `2026-10-19-arc3-r9-*.md` knowledge file or matching selected token is present in canonical `corpus/knowledge/` / `corpus/README.md`; the exact EX-10 token search returned no match. Therefore the frozen `87 → 88`, mapped 88, empty missing/dangling after-state is **UNVERIFIABLE**, not an observed result. Before landing EX-10's proposed `corpus/knowledge/2026-10-19-arc3-r9-vyper-noopt-none-boundary.md` and token `2026-10-19-arc3-r9-vyper-noopt-none-boundary` (`claims/c2/EX-10/evidence/entry-draft.md:1-7`), the integrator should format its numeric claims to the corpus count contract (`CORPUS.md:33-40`); the draft currently has bare format/run/ratio counts (`entry-draft.md:13-15`). Rerun Command A at the integration revision.

## C3 — calibration

### Pointer and drift — REPRODUCED

A fresh filtered search of `/home/vgpnk/.kimi-code/config.toml` returned exactly:

```text
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

A read-only scan of `config.toml*` showed the same pin at backup lines 2915, 2932, 2940, 3227, 3298, 3298, and 3157, and current line 4126. The gate grades `PROVINCE.md:18` as `:18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)`; the same full run remains FAIL at `SCORECARD.md:1834`, not at the pointer. The gate uses a first-match version regex (`.ufo/gates/c1-census-v10.py:324-334`) and dereferences the specified physical line (`:466-482`).

Using the actual `ptr_check()` with a minimal config under `/var/tmp`, I observed:

```text
before_line2=('ok', 'pins 6.7.0')
after_insert_old_line2=('stale', "line holds no rea-agents pin: '# inserted before pin'")
after_insert_reanchored_line3=('ok', 'pins 6.7.0')
```

The line pointer is positional and must be re-anchored after preceding edits; it does not follow the stanza. The current config has one match, but that is a present-state observation, not a uniqueness invariant. The available snapshots verify line movement but do not contain the cited `:3546` occurrence; `.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt:9` records that it now holds a Copilot block, but the exact intermediate pin position is **UNVERIFIABLE** from the inspected snapshot set. Do not assert the whole `2940 → 3227 → 3298 → 3546 → 4126` history as independently reconstructed.

### Aggregate gate and durable destination

The targeted pin assertion is **VERIFIED / REPRODUCED `current-ok`**; the whole census is **DISCREPANCY / FAIL** for the separate undeclared SCORECARD locus. This distinction is consistent across SC-1/2/3 and the other C3 reports.

The frozen claim asks to land the drift characterization as a corpus erratum or measured note on the receipt (`claims-frozen.md:48-56`). The existing receipt already says the pointer class is perishable (`.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt:8-10`), and the round-9 seat reports contain detailed measured notes, but no new corpus entry or receipt update is present. The exact canonical landing condition is **UNVERIFIABLE / pending authorized integration**; no receipt, corpus, gate, Province, or live config file was changed here.

## Scope and final evidence boundary

At the final inventory pass, delivered verdict peers were `CN-1`–`CN-4`, `VZ-1`–`VZ-4`, and `CR-6`–`CR-8`. Their differing C2 recommendations, including VZ-2's preference for EX-5, are recorded above, not collapsed into a consensus. C1 and C3 evidence agrees on the live measurements and the separation between a targeted `current-ok` assertion and the globally failing gate.

Before this write, `git status --short` showed the pre-existing `M .ufo/waves/arc2-loop1-round10/C3.md` and the existing untracked `.ufo/waves/arc3-loop1-round9/` tree. No Git mutation was made. The only file written for this seat is `.ufo/waves/arc3-loop1-round9/claims/verdicts/CR-5.md`; all test scratch was under `/var/tmp` and removed.
