## CLAIM
Confirm that the round-6 dispatch brief's frozen predictions match the predictions the PS seats scored against.

## METHOD
Dispatch record lives in the parent session log `agents/main/wire.jsonl` (session 5dcc2935). Quoted the lane-A brief's frozen block at `main/wire.jsonl:2685,2782`; verified it verbatim in the PS3/PS4 seat prompts (`agents/agent-446/wire.jsonl`, `agent-447/wire.jsonl`). Read the four in-repo PS reports. No probe executed; no prediction rewritten.

## FINDINGS
Brief (lane A, `:2685/2782`), verbatim: "PREDICTIONS WERE FROZEN BY THE PARENT BEFORE THIS DISPATCH … L1 `npx -y rea-agents@6.5.0 --version` → 6.5.0 exit 0 (exact). L2 MCP tools/list on 6.5.0 → 207 tools (exact). L3 inspect_go_binary on a real Go ELF → RESULT class. L4 inspect_rust_binary on a real Rust ELF → RESULT class. L5 inspect_electron_fuses on an Electron binary → RESULT class. L6 inspect_sqlite_database on a real SQLite db → RESULT class. L7 search_bytes ELF magic on a small ELF → RESULT class (hit with offset). L8 inspect_with_objdump on /usr/bin/jq → RESULT class. L9 identify_flutter_build on /usr/bin/jq (non-flutter) → TYPED-REFUSAL class. L10 compare_wasm_interfaces if wasm carriers exist, else project_harmony_application_graph on non-harmony input → TYPED-REFUSAL class."

Cowitnesses: plan (`:2684`) "Prediction: … L9-L10 TYPED-REFUSAL-class"; lane-B brief (`:3063`) "L9-L10 TYPED-REFUSAL class".

Scored against: `PS1.md:8-12` "PREDICTED: exact `6.5.0`" / "exactly 207 tools" / "RESULT class" — match. `PS2.md:5` "L6–L8 RESULT; L9–L10 TYPED-REFUSAL" — match. `PS3.md:10-18` L1 "Exact `6.5.0`, exit 0", L2 "Exactly 207 tools", L3–L8 "RESULT", L9 "TYPED-REFUSAL" — match; `PS3.md:19` L10 row: "RESULT if WASM branch; otherwise TYPED-REFUSAL". `PS4.md:8`: "L10 RESULT if wasm carriers exist, otherwise TYPED-REFUSAL", presented as all ten predictions.

"RESULT if WASM branch" appears in no dispatch text; all three sources freeze L10 as TYPED-REFUSAL class. Material outcome: leg 10 took the wasm path and returned structured `capability_unavailable` (`receipts/leg-10.md:16-17`, TYPED-REFUSAL class), so PS3's restated register would score a mismatch, the brief's register a match; `PS3.md:19` leaves L10 unscored ("No receipt"). Benign: PS1 omits "exit 0" (L1); PS3 omits "(hit with offset)" (L7).

## THREATS
Only session dispatch records carry the brief; no standalone signed prereg artifact. Both report authors (agent-446=PS3, agent-447=PS4) received "→ TYPED-REFUSAL class" yet wrote "RESULT if WASM branch"; no in-band text supports RESULT. If the final tally adopts PS3.md's table, the L10 register changes.

## VERDICT
FINDING: PS3/PS4 restate L10's wasm branch as "RESULT" — absent from both lane briefs and the parent plan, which freeze TYPED-REFUSAL class for L10.
