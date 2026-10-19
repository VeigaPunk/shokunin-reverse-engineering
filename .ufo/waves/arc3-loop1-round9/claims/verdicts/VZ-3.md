# VZ-3 — independent reconciliation verdict

**Date:** 2026-10-19  
**Frozen revision:** `947091d6b6f52684faf9ca53adf94ff8a0f6b006`  
**Scope:** reconcile C1–C3 using first-hand checks and peer submissions. Findings marked reproduced/verified describe evidence, not a claim that canonical edits were landed. This seat changed no source, corpus, gate, receipt, or other seat artifact.

## C1 — perishable pacman row

**Archive-count finding: CORRECTED (evidence and proposed wording; not landed).** `PROVINCE.md:40` dates Core-surface verification to 2026-10-13, while `PROVINCE.md:50` states `1556 signed archives` without a same-row date. The prior value is explicitly identified as a 2026-10-13 snapshot at `corpus/knowledge/2026-10-13-pacman-packages.md:75-83`. A fresh read-only cache inventory returned:

```text
archives=1350 signatures=1350 missing_sidecars=0 orphan_sidecars=0
wc -l < PROVINCE.md  ->  162
```

Thus the current cache contains 1,350 archive files and 1,350 filename-matched `.sig` sidecars, a delta of −206 from the dated snapshot. This is filename pairing, **not** cryptographic verification of every signature. Peer PL-1 independently reports the same count and delta (`claims/c1/PL-1.md:7-20`). Its perishable-row review also identifies `available:true` as a 2026-10-13 observation requiring that date in the row, and reports a fresh `jq` byte-identity recheck (`claims/c1/PL-1.md:22-35`). No live `binary_session {}` probe was available here, so current-session availability remains **UNVERIFIABLE**.

Suggested same-line replacement for `PROVINCE.md:50` (proposal only):

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in the 2026-10-13 live session); pacman `.pkg.tar.zst` cache: 1,350 archives with matching `.sig` sidecar filenames as of 2026-10-19; the prior 1,556 is the 2026-10-13 snapshot (live delta −206; see `corpus/knowledge/2026-10-13-pacman-packages.md:75-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` byte-identical to cached archive member (reverified 2026-10-19) |
```

The frozen requirement that the extended census still **PASS** is a **DISCREPANCY**. Fresh `python3 .ufo/gates/c1-census-v10.py` output:

```text
-- UNDECLARED (1) --
  SCORECARD.md block 1833-1839 [scope None]
      :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
exit=1
```

The declared SCORECARD census range ends at line 1813 (`.ufo/gates/c1-census-v10.py:276`), so a line-50-only correction cannot remove this separate finding. PL-1 likewise reports its scratch same-line patch left the gate FAIL (`claims/c1/PL-1.md:37-60`). No PROVINCE edit was made; the live row remains uncorrected.

## C2 — one corpus Unknown

**Bounded compiler finding: REPRODUCED.** I selected the frozen Vyper flag-boundary candidate for a separate first-hand re-derivation. Fresh Vyper 0.4.3 (`.ufo/waves/arc3-loop1-round4/tools/vyper-venv/bin/vyper`, SHA-256 `615f792c6bc1bdf87cbc4612420a331ec108246d9debadbb3f3b9efa8209dd10`) compiles the K8 source (SHA-256 `62549f79b9efb6677e5b24769296e812ec321914816cb5e78699091fdfe6ea7d`) identically with `--no-optimize` and `-O none`: `bytecode`, `bytecode_runtime`, `abi`, `method_identifiers`, and `settings` all compare byte-for-byte. The decoded runtime is 617 bytes, SHA-256 `1a7bf2cdc83e171f0a8485c894286ea59289de9bd45f1c124e1ed6888ef14ffc`. REA 6.7.0 on each fresh runtime returned 8 raw and 8 normalized rows with the same selector set (`2ae1431c, 364605a1, 9adbf691, 9b7c2962, bf3724af, cf35f823, d7531d91, d7b7913b`) and decoded-runtime digest. This closes only the byte-level distinction for this fixture/compiler/output set; REA rows are static inferences, not execution evidence. Peer CR-2/CR-3/CR-4 independently report this same bounded result (`claims/c2/CR-2.md:7-10`, `CR-3.md:12-26`, `CR-4.md:9-14`).

**Coverage landing: UNVERIFIABLE.** Fresh Command A at HEAD, using the recipe in `SCORECARD.md:88-124`, returned:

```json
{"citation_resolved_rules":15,"coverage_score":10.0,"dangling":[],"depth_score":10.0,"knowledge_files":87,"mapped":87,"missing":[],"revision":"947091d6b6f52684faf9ca53adf94ff8a0f6b006","rule_blocks":15}
```

No C2 draft or map token is in canonical `corpus/knowledge/` / `corpus/README.md`; therefore 87→88 and mapped 88 have not been measured. The current peer set proposes mutually exclusive candidates, not one shared closure: EX-5 (solc 0.8.28 viaIR), EX-6 and EX-8 (viaIR fallback interaction), CR-1 and EX-11 (different `ev_` verb families), plus several repeated Vyper-alias/offset drafts (CR-2/3/4, EX-7/9). Do not count these as multiple entries for this one frozen claim.

**Integration recommendation, not a landing:** choose EX-8's single draft `corpus/knowledge/2026-10-19-arc3-r9-viair-fallback-miss.md` and token `2026-10-19-arc3-r9-viair-fallback-miss`. It directly addresses the specifically named r6 unknown at `corpus/knowledge/2026-10-19-arc3-r6-viair-dispatch-shape.md:30`; its paired no-fallback/payable-fallback source measurements, REA selector checks, and byte-level branch walk are bounded and retained (`claims/c2/EX-8.md:3-19`; draft metadata and recheck at `claims/c2/EX-8/evidence/draft-corpus-entry.md:1-15`). EX-6 is a competing measurement of the same unknown and should not be added as a second closure for this claim. Regardless of selection, run Command A after integrating exactly one entry and its matching map token.

## C3 — pin-line drift

**Live pin and pointer: REPRODUCED.** A first-hand search of `~/.kimi-code/config.toml` found one `rea-agents@` occurrence, at line 4126: `args = [ "-y", "rea-agents@6.7.0", "mcp" ]`. The full `python3 .ufo/gates/c1-census-v10.py` output includes `:18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)`. The literal pointer is at `PROVINCE.md:18`; the gate dereferences that physical line at `.ufo/gates/c1-census-v10.py:466-482`. Gate `live_pins()` uses a first-match regex on the live file (`:324-334`); it does not enforce uniqueness.

**Drift behavior: REPRODUCED.** In isolated `/var/tmp` config fixtures, inserting one line before the pin moved it to 4127 while the pointer remained 4126; the pin still matched live 6.7.0 but the pointer became `STALE (line holds no rea-agents pin: '# isolated drift fixture')`. The shifted pointer worked at 4127. Thus the value is dynamically re-derived, but the recorded physical line does not follow edits. A second fixture changed the config pin to 6.7.1 at the old line: the pointer read `current-ok (pins 6.7.1)`, while the unchanged Province pin assertion was classified `historical (inline marker)` rather than stale (`claims/c3/SC-3.md:22-23,43-52`; marker and classification logic at `.ufo/gates/c1-census-v10.py:315,559-563`). This is a calibration caveat: same-line historical wording can mask a version mismatch.

**Aggregate gate status: DISCREPANCY.** The live pointer assertion is current-ok, but the full gate still fails on the unrelated undeclared SCORECARD locus recorded under C1. The requested canonical corpus/receipt characterization has not been landed by this seat; its landing remains **UNVERIFIABLE** pending authorized integration. The present evidence establishes behavior, not a completed canonical update.

## Reconciliation boundary

C1's live count and C3's pointer mechanics are reproduced. C1's frozen gate-PASS after-condition is a **DISCREPANCY**; C2's compiler result is reproduced while one-entry corpus/map integration and its 88/88 result remain unverified. C3's pointer current-ok and drift behavior reproduce, but its requested canonical characterization remains unlanded. This artifact is the only file written by VZ-3; all other evidence paths above are peer submissions or existing repository sources, explicitly identified as such.