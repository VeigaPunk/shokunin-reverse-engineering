# CR-8 — round-9 independent reconciliation

Role: verdict/convergence (`CR-8`). Measured repository HEAD: `947091d6b6f52684faf9ca53adf94ff8a0f6b006` (`git rev-parse HEAD`). All live/custody reads were read-only. Compiler and gate fixtures used `/var/tmp`; no `/tmp`, Git mutation, source-file, gate, config, corpus, or peer-artifact writes were made. This file is the only deliverable from CR-8.

## Verdict summary

- **C1 freshness — DISCREPANCY / completion condition not met.** The unqualified archive count is stale against a fresh 1,350-file census, and the row-only patch text below preserves 162 lines. The required v10 census `PASS` is not observed: the current instrument exits 1 on an unrelated unscoped `SCORECARD.md:1834` locus. Perishable row values were censused; current `binary_session` availability remains unverified.
- **C2 coverage — REPRODUCED technically, but not landed.** I independently reproduced byte identity for Vyper K8 `--no-optimize` versus `-O none`, including creation bytecode. The frozen coverage move is **not yet verified**: Command A remains 87/87 at HEAD and the knowledge entry/map token are drafts, so 88/88 is not an observed after-state.
- **C3 calibration — REPRODUCED.** The live Kimi pin is the only `rea-agents@` match in the current config at line 4126; the gate grades the `PROVINCE.md:18` pointer `current-ok`. An isolated insertion before the pin makes the old physical-line pointer stale and re-anchoring restores `current-ok`. The whole-gate result is still FAIL on the separate SCORECARD locus; this does not negate the pointer-level result.

## C1 — row census, patch text, and gate result

First-hand source/cache census:

```text
git rev-parse HEAD
947091d6b6f52684faf9ca53adf94ff8a0f6b006

HEAD PROVINCE.md:50 contains: pacman `.pkg.tar.zst` corpus 1556 signed archives
live_archive_files=1350
live_signature_sidecars=1350
archives_without_matching_sidecar=0
orphan_sidecars=0
live_minus_row_snapshot=-206
row_is_unqualified=True
```

The source row itself is the current-file evidence for the stored `1556`; it is not a fresh cache count. The archive and sidecar census is first-hand. Matching `.sig` sidecars do not establish that every current signature cryptographically verifies.

I independently rechecked the other volatile row result:

```text
pacman -Q jq
jq 1.8.2-1
pacman -Qkk jq
jq: 25 total files, 0 altered files
sha256sum /usr/bin/jq
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
tar -xOf /var/cache/pacman/pkg/jq-1.8.2-1-x86_64.pkg.tar.zst usr/bin/jq | sha256sum
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  -
wc -l PROVINCE.md
162 PROVINCE.md
```

Whole-row census (`PROVINCE.md:50`):

- `1556 signed archives` — **CORRECTED** as a current count. It is the value printed by HEAD, not today's cache. The independently measured live count is 1,350, with 1,350 matching sidecars; difference from the value in the row is −206. The requested historical pointer is `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`.
- `available:true in live session` — **UNVERIFIABLE** as a current session state; no live `binary_session` probe was available. The adjacent table scope says each surface was verified on 2026-10-13 (`PROVINCE.md:40`); date it explicitly rather than implying current availability.
- Installed-`jq` byte equality — **VERIFIED as of 2026-10-19** by the package query, `pacman -Qkk`, and matching hashes above. This is another potentially perishable state result; date the recheck.
- `.MTREE per-file sha256`, `pacman -Qkk verify`, and `binary_session {}` identify a metadata property, procedure, and probe shape; they are not additional changing inventory counts.

Recommended same-line patch text (not applied):

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in the live session, observed 2026-10-13); pacman `.pkg.tar.zst` corpus 1,556 signed archives (2026-10-13 snapshot; live re-count 2026-10-19: 1,350 archives and 1,350 matching `.sig` sidecars; delta −206 vs the row snapshot; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq 1.8.2-1` byte-identical to its cached archive member (rechecked 2026-10-19; SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`) |
```

A scratch-only replacement test under `/var/tmp` returned `patch_occurrences=1 original_lines=162 patched_lines=162 same_line_count=True`. This patch preserves the historical count as dated, states the current path count without implying all signatures were cryptographically reverified, dates the availability observation, and dates the fresh `jq` equality check.

The live census command `python3 .ufo/gates/c1-census-v10.py` returned:

```text
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1870 loci=11
SKILL.md       lines=413  loci=2
-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
PROVINCE.md block 15-26 [scope CURRENT]
    :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
FRONTIER register (G21): 14 rows asserted, errors: []
G2 positive-assertion guard: ok
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
CENSUS_EXIT=1
```

Therefore C1's required instrument `PASS` is **not established**; the instrument has an undeclared current SCORECARD locus beyond the scope it declares (ending at line 1813). The proposed PROVINCE-row-only patch cannot cure that locus. I did not change the SCORECARD or the gate, both outside the seat write scope.

Peer reconciliation: the C1 artifacts `PL-2.md`, `EX-4.md`, `EX-1.md`, `RV-2.md`, `RV-3.md`, and `PL-4.md` independently report the same live count and the same gate failure. Their patch variants differ in how explicitly they date the other volatile row values; the recommendation above dates both `available:true` and the rechecked `jq` result.

## C2 — independent byte-boundary re-derivation and landing state

I selected the K8 optimizer spelling boundary for an independent re-run. Source SHA-256: `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`. The local compiler reported `0.4.3+commit.bff19ea2`; cached REA CLI reported `6.7.0`.

Under fresh `/var/tmp` scratch, I separately compiled `bytecode`, `bytecode_runtime`, `abi`, `method_identifiers`, and `settings` using `--no-optimize` and `-O none`. Every cross-form comparison passed:

```text
bytecode byte-identical: PASS
bytecode_runtime byte-identical: PASS
abi byte-identical: PASS
method_identifiers byte-identical: PASS
settings byte-identical: PASS
noopt: runtime_bytes=617 runtime_sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
none: runtime_bytes=617 runtime_sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
noopt: rea_functions=8 selectors=0x2ae1431c,0x364605a1,0x9adbf691,0x9b7c2962,0xbf3724af,0xcf35f823,0xd7531d91,0xd7b7913b decoded_sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
none: rea_functions=8 selectors=0x2ae1431c,0x364605a1,0x9adbf691,0x9b7c2962,0xbf3724af,0xcf35f823,0xd7531d91,0xd7b7913b decoded_sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
provider=evmole-interface/evmole@0.9.3 confidence=inferred
rea_functions_equal=True decoded_sha_equal=True
```

This **REPRODUCES** the bounded compiler-output equivalence on this source and compiler. The R8 knowledge entry describes the runtime comparison; creation-bytecode equality is the additional residual worth recording here. Do not generalize this one synthetic fixture to other source shapes or Vyper releases. REA function data is inferred, not contract-execution evidence.

The immutable Command A recipe at `SCORECARD.md:88-124`, run at this HEAD, returned:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 87, "mapped": 87, "missing": [], "revision": "947091d6b6f52684faf9ca53adf94ff8a0f6b006", "rule_blocks": 15}
```

At reconciliation time, the corpus and map remain untouched; no after-landing `88` measurement exists. Multiple C2 seats have drafted competing valid targets (among them the K8 boundary, solc-viaIR version/fallback questions, and SQLite/Go Evidence-ID domains), with differing proposed filenames/tokens. CR-8's technical re-run supports the K8 boundary, but the integrator must select **one** named Unknown, one canonical entry filename, and its matching map token; do not land every competing draft. The frozen C2 coverage claim remains **UNVERIFIED / incomplete** until that entry and token land and Command A observes 88 knowledge files, 88 mapped, `missing=[]`, `dangling=[]`.

## C3 — live pin, gate classification, and drift class

A targeted read-only search (`Grep` for `rea-agents@` in `/home/vgpnk/.kimi-code/config.toml`) returned exactly one match:

```text
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

A read-only search over `config.toml*` returned one identical pin match in each listed file, at these physical lines:

```text
config.toml:4126
config.toml.20261018-085645.bak:2915
config.toml.20261018-114557.bak:2932
config.toml.20261018-143236.bak:2940
config.toml.20261018-145016.bak:3227
config.toml.20261018-150133.bak:3298
config.toml.20261018-161746.bak:3298
config.toml.20261018-201656.bak:3157
```

The snapshot lines vary while the matched pin text stays `rea-agents@6.7.0`; this establishes a mutable physical-line locator, not version movement or the exact cause of each historical edit. I did not edit or inspect unrelated contents of the custody config.

The gate's targeted output and aggregate result were:

```text
:18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
:1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
```

For a controlled behavior check, I imported `ptr_check()` from `.ufo/gates/c1-census-v10.py` and used only a synthetic `config.toml` under `/var/tmp`:

```json
{"baseline_line_2": ["ok", "pins 6.7.0"], "fixture_only": true, "insert_after_line_3": ["ok", "pins 6.7.0"], "insert_before_old_line_2": ["stale", "line holds no rea-agents pin: '[mcp_servers.rea]'"], "insert_before_rekeyed_line_3": ["ok", "pins 6.7.0"], "live_anchors": {"devin": "6.5.0", "kimi": "6.7.0", "omp": "6.5.0"}}
```

**REPRODUCED:** the line pointer is version-checked but positional. Inserting before the pin makes the old line stale; re-anchoring to the new line restores `ok`; inserting after it leaves the line valid. The live file's one-match status is an observation of this capture, not a uniqueness invariant; `live_pins()` uses a first-match regex (`.ufo/gates/c1-census-v10.py:324-334`), while `ptr_check()` dereferences the literal line (`:466-482`).

C3 is **REPRODUCED** for live uniqueness, current pointer disposition, and the line-sensitive drift class. The global census FAIL is a separate discrepancy, not a failed pointer check. This agrees with the C3 artifacts reviewed, including `SC-1.md`, `SC-3.md`, `RV-7.md`, `RV-8.md`, `EX-13.md`, `EX-15.md`, and `EX-16.md`; those also distinguish the assertion-level `current-ok` result from aggregate FAIL.

## Reconciliation boundary

At the final artifact inventory check, no sibling verdict files were present under `claims/verdicts/*.md`; this is CR-8's independent reconciliation, not a claim of agreement with unlanded VZ/CN/CR-5..7 artifacts. All findings above are supported by CR-8's own measurements or are explicitly identified as peer-state context. No source or custody write was made.