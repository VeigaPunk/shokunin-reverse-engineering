## CLAIM
Adjudicate XA.md's four divergences from primary receipts: which seat is right.

## METHOD
Read XA, RV2/RV3/RV4/RV5/RV7, EX6/EX8/EX10, RE1, SC5, P0, and receipts leg-4/6/8/9/10. Read-only python3 sha256 recomputation of stdout blocks (raw and +LF); `stat` mtimes; `git status`. No probes, no MCP, no writes except this report.

## FINDINGS
- **L10 route — XA cites `RV2.md:6,10`; RV2 never mentions L10. Its description fits `RV4.md:6,10` exactly (Harmony fallback, `invalid_input`).** Canonical `leg-10.md:7` carries EX10's client id; `:9,16-17` are two `inspect_wasm_artifact` calls refused with structured `capability_unavailable`/`unsupported_provider`. Recorded hash `e4cf0833…` recomputes exactly. EX10 followed the frozen branch: `SC5.md:8` found `.wasm` carriers and `P0.md:9` selects the Wasm tool "if carriers exist"; RV4 searched only repo corpus + `/tmp` (`RV4.md:6`). Both routes are TYPED-REFUSAL — class agreement holds. EX10 is right for the canonical leg; `RV4.md:11`'s receipt claim holds for leg-9 only.
- **L6 receipt/provenance.** `leg-6.md:1` is RV3's receipt (`ev_e0eb446a…`, hash `9a1445b4…` recomputes). `EX6.md:15` predicted exactly this replacement (same evidence/hash) from a selected-table call. `RV3.md:5` admits one repeat to "repair receipt capture" but never discloses displacing EX6. EX6 right; RV3's account incomplete.
- **L6 hash.** The mismatch is `RE1.md:10,17`, not EX8 (EX8 is L8-only; its `22205280…` is L8 provider stdout, per `RV7.md:5`). RE1 cites `leg-6.md:12`/`:15-19`; current file holds `:13`/`:18-20` and recomputes cleanly. RE1.md mtime 18:27:31 precedes leg-6.md's final write 18:27:56, so RE1 audited an earlier version: right on its snapshot, stale against the current receipt.
- **L4 target.** Canonical `leg-4.md:12,39` = Signal `.node` (rust-auditable; hash `bc4902f7…` recomputes +LF). `RV2.md:9` replayed `/usr/bin/rg` — different target and evidence (`1c586f5a…`). RV2 itself reported no baseline receipt; mtime (18:21:55 < 18:25:16) confirms. RV2's statements are accurate but off-target; canonical L4 stands.

## THREATS
The wave dir is untracked (`git status`: `?? .ufo/waves/luna-round-6/`), so overwritten versions (EX6's receipt, RE1's snapshot) are unrecoverable; chronology rests on mtimes, not signed timestamps. EX6's `/tmp/luna-round-6-ex6-*` captures no longer exist. No probes re-run by this seat.

## VERDICT
FINDING: XA's L10 and L6-hash citations name the wrong seats (its line numbers match `RV4.md:6,10` and `RE1.md:10`); canonical L4/L6/L8/L10 receipts verify; RV3 displaced EX6's L6 transcript without disclosure.
