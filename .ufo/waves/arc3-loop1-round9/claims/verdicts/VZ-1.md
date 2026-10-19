# VZ-1 — C1/C2/C3 convergence verdict

Wave: `arc3-loop1-round9` · frozen claims: `claims-frozen.md:14-56`  
Measured repository HEAD: `947091d6b6f52684faf9ca53adf94ff8a0f6b006`  
Scope: independent source rechecks and verdicts; source/custody paths remain read-only. The only file created for this seat is this verdict artifact.

## Verdicts

- **C1 — CORRECTED, with an independent gate DISCREPANCY.** I re-counted 1,350 package archives and 1,350 matching `.sig` sidecars (no missing/orphan names); the unqualified `1556` in `PROVINCE.md:50` is only a recorded 2026-10-13 snapshot. The proposed row replacement below dates every perishable observation and preserves 162 lines, but is not applied. Live `jq` byte identity is VERIFIED; present-session `available:true` is UNVERIFIABLE. The requested post-patch whole-gate PASS is DISCREPANCY: the same lone out-of-scope `SCORECARD.md:1834` finding remains.
- **C2 — REPRODUCED for the selected, bounded Vyper output boundary; post-landing count UNVERIFIABLE.** On the retained K8 source and Vyper 0.4.3 executable, `--no-optimize` and `-O none` outputs matched for all five tested formats, including creation bytecode. The proposed corpus entry/map token are not integrated; Command A remains 87/87, so the frozen 87→88 condition is not established.
- **C3 — REPRODUCED at pointer level; whole-gate DISCREPANCY.** The one live Kimi pin is at config line 4126, the gate grades `PROVINCE.md:18` `current-ok`, and a controlled insertion before the pin makes the old physical-line pointer stale until re-anchored. The overall gate still fails at the separate SCORECARD locus. The current receipt contains a generic perishability warning, but this round's controlled-mechanism result was not appended to a receipt or corpus entry; that landing requirement remains unmet.

## C1 — live census and full `PROVINCE.md:50` row

First-hand live commands and results:

```text
ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l       -> 1350
ls /var/cache/pacman/pkg/*.sig | wc -l               -> 1350
archives=1350 signatures=1350 missing_matching_signatures=0 orphan_signatures=0
pacman -Q jq                                        -> jq 1.8.2-1
pacman -Qkk jq                                      -> jq: 25 total files, 0 altered files
sha256sum /usr/bin/jq                               -> e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
archive usr/bin/jq member sha256                    -> e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
```

The independent pairing check establishes sidecar presence, not cryptographic validity of every signature. The recorded historical `1,556` is in `corpus/knowledge/2026-10-13-pacman-packages.md:21-25`; its erratum explicitly calls it a dated snapshot and records 1,350/−206 at `:73-83`. The current `1,350 − 1,556 = −206` arithmetic is correct, but the old filesystem state cannot be reconstructed from today's cache; I do not treat the historical total as a new measurement.

Whole-row census (`PROVINCE.md:50`, read with the table date at `:40`):

- Archive count `1556`: **CORRECTED** to “2026-10-13 snapshot”; current cache is 1,350. Sidecar counts match, but this check alone does not prove all signatures valid.
- `available:true` in a live session: **UNVERIFIABLE as current state**; the enclosing table says its host observations were verified 2026-10-13 (`PROVINCE.md:40`), and no live `binary_session {}` probe was available for this recheck.
- Installed `jq` identity: **VERIFIED for 2026-10-19** by package/version check, `pacman -Qkk`, and equal installed/archive-member SHA-256 values above. This state can change, so date it.
- `.MTREE` per-file sha256, `pacman -Qkk` verify, and the `binary_session {}` probe name are format/procedure/capability descriptions, not additional live inventory outcomes.

Proposed single-line replacement for `PROVINCE.md:50` (not applied; one physical line, so the 162-line count is preserved):

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` recorded in live session 2026-10-13; not re-probed 2026-10-19); pacman `.pkg.tar.zst` corpus 1,556 signed archives (2026-10-13 snapshot; live count 2026-10-19: 1,350 archives and 1,350 matching `.sig` sidecars, −206; sidecar pairing is not cryptographic verification; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq 1.8.2-1` byte-identical to its cached archive member (reverified 2026-10-19; SHA-256 `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806`) |
```

Gate evidence: `.ufo/gates/c1-census-v10.py` SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4` (716 lines). Running `python3 .ufo/gates/c1-census-v10.py` gives `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)`, exit 1. The sole blocker is `SCORECARD.md` block `1833-1839`, line `1834`, `6.7.0 -> AMBIGUOUS (no client token in clause)`. The declared SCORECARD scope ends at line 1813 (`.ufo/gates/c1-census-v10.py:276-277`), while the finding is at `SCORECARD.md:1833-1839`. The same-line candidate was tested on a `/var/tmp` copy: `PROVINCE_lines=162`; gate remained `FAIL`, exit 1, with that same sole undeclared SCORECARD finding. Therefore “instrument still reads PASS after” is **DISCREPANCY**, not a pass. The gate does not grade the archive count in row 50; this is a separate PROVINCE census correction.

## C2 — one selected Vyper residual

I select only the residual creation-bytecode/output-form boundary between Vyper `--no-optimize` and `-O none`, not another solc Unknown. The R8 entry (`corpus/knowledge/2026-10-19-arc3-r8-vyper-optimizer-dispatch-shapes.md:7-15`) documents runtime dispatch, selectors, ABI/method identifiers/settings, but does not settle creation-bytecode equality.

Fresh compile evidence in `.ufo/waves/arc3-loop1-round9/claims/c2/CR-2/evidence/rederive.txt:1-20,22-52,54-60` records source SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`, compiler SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`, version `0.4.3+commit.bff19ea2`, and pairwise byte-identical results:

```text
bytecode=IDENTICAL
bytecode_runtime=IDENTICAL
abi=IDENTICAL
method_identifiers=IDENTICAL
settings=IDENTICAL
bytecode_decoded_bytes=687 sha256=b09398d8eb89f1ec1a73de9cbec27a54ce79d185094a4253a384cfffe62e2598
bytecode_runtime_decoded_bytes=617 sha256=1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc
```

The REA cross-check in `rederive.txt:62-82` reports `evmole-interface`, `evmole@0.9.3`, eight selectors/functions for each runtime, and matching decoded-runtime SHA. **REPRODUCED** is limited to this K8 source and this compiler executable; it does not establish equivalence across sources, versions, or deployment/runtime behavior.

Integration verdict: **UNVERIFIABLE / not achieved.** The draft at `claims/c2/CR-2/entry-draft.md:1-14` is explicitly marked for parent integration, has no `recheck:` field, and its proposed map token is absent from `corpus/README.md` (coverage map). Command A from `SCORECARD.md:88-124`, rerun at HEAD `947091d6b6f52684faf9ca53adf94ff8a0f6b006`, returns:

```json
{"citation_resolved_rules": 15, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 87, "mapped": 87, "missing": [], "revision": "947091d6b6f52684faf9ca53adf94ff8a0f6b006", "rule_blocks": 15}
```

This matches `claims/c2/CR-2/evidence/command-a-before.json`; it is a **before** count only. No 88th knowledge entry/map token is landed, so the frozen after-count cannot be claimed.

## C3 — pin-line drift re-derivation

A direct search of `/home/vgpnk/.kimi-code/config.toml` found exactly one `rea-agents@` match:

```text
/home/vgpnk/.kimi-code/config.toml:4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
```

The saved config snapshots were independently scanned; the same pin text occurred at current line 4126 and backup lines 2915, 2932, 2940, 3227, 3298, 3298, and 3157. This confirms a mutable physical line coordinate, not the cause of any particular historical edit. Current gate output confirms `PROVINCE.md:18` pointer `~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)`. Gate logic at `.ufo/gates/c1-census-v10.py:466-482` dereferences the exact physical line and marks it stale if that line has no pin; it checks the extracted version against the live anchor. The current pin-level disposition is **REPRODUCED**.

Controlled fixture, kept under `/var/tmp` with no live config edit:

```text
anchors={'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
baseline line1=('ok', 'pins 6.7.0')
after insertion old line1=('stale', "line holds no rea-agents pin: '# inserted before pin'")
after insertion rekeyed line2=('ok', 'pins 6.7.0')
```

Thus an insertion before the pin shifts the line number and leaves the old pointer stale until re-anchored; the pin/version itself need not change. The exact edit causes behind the archived snapshot offsets remain unproven.

The same gate run exits 1 / **DISCREPANCY** at `SCORECARD.md:1834` as described above, despite the pointer being `current-ok`. `.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt:8-10` already says the line pointer is perishable and must be re-derived; however, no receipt or corpus file was changed in this seat, and no new receipt/corpus landing of this round's controlled insertion result is present. The new mechanism is described in the peer claim at `claims/c3/EX-15.md:87-89`, but the frozen durable-landing condition (`claims-frozen.md:48-52`) remains outstanding.
