PARTIAL — the successful WASM observations are supported, but the knowledge entry is not admissible unchanged under the strict QUALITY bar.

Axes: calibration (identity inference and source attribution), coverage (carrier path/scope disclosure), depth (replayability). This is a fixable evidence-presentation defect, not a reason to discard the observed inspections or comparisons.

## Observation and inference

**Observation:** I read the target entry and rubric from Git objects at S, not from the working tree. At S, the four inspection receipts record `exit_code: 0`, exact carrier paths/hashes, full Evidence IDs, and complete interface records (e.g. `wasm-inspect/evmole/receipt.json:18,33-46,62-70`; `wasm-inspect/zip-js/receipt.json:18,29-42,55-63`; `wasm-inspect/openjpeg/receipt.json:18,29-42,57-65`). The retained successful stdout records contain `operation` and the IDs. The real and synthetic compare stdout records likewise contain `operation: compare_wasm_interfaces`, exact IDs, and both input hashes; their receipts report exit 0 and empty stderr (e.g. `wasm-compare/compare-real-both.receipt.json:10-19,27-44`; `compare-real-both.stdout.txt:1`). The failure IDs `ev_b7b2…` and `ev_ac55…` are partial error Evidence, not successful holds; the entry correctly warns against counting an `ev_` ID alone (`knowledge/...wasm-interfaces.md:35`; `w1/WasmRefusalLeg.md`, Cases C/D).

**Observation:** the synthetic inputs are reproducible from retained WAT and byte-pinned WASM, with `wat2wasm` version/argv and hashes (`wasm-compare/synth/v1.wat:1-7`, `v2.wat:1-9`, `build-receipt.json:1-17`, `SHA256SUMS:1-4`). The entry also correctly says the real `qcms`/`openjpeg` comparison is cross-module, not a version-regression result (`knowledge/...wasm-interfaces.md:28-30`).

**Observation:** S040 is not the registered source for the Wasm CLI contracts. At S, `corpus/SOURCES.md:46` scopes S040 to HarmonyOS application inventory/projection and anchors `artifactCommands.js:145-159`; that installed-source range registers `inspect-artifact`, not `inspect-wasm-artifact`. The round-20 source notes likewise locate S040 at `harmonyApplication.js:111` (`corpus/lessons/round-20.md:43`), while the static-tool source sequence is S041–S045 (`corpus/SOURCES.md:64`). The underlying WABT gate is separately supported in the retained wave-1 source study `w1/RevWasmVerb.md`, and in the refusal receipts; the attribution to S040 is the error, not the observed refusals.

**Inference:** the line-18 parenthetical “content+params-keyed” is not established by the repeated evmole call. Both receipts have the same path, bytes and parameters and the same Evidence ID; that observation cannot distinguish an ID domain that includes path from one that does not. It is also placed under “What was exercised (observation)” rather than labeled inference (`knowledge/...wasm-interfaces.md:7-18`; same path/hash and repeat output digests at `wasm-inspect/evmole/receipt.json:3-10,16-26,33-45` and `evmole-repeat/receipt.json`).

**Observation:** compare receipts retain only each temporary request JSON’s `/tmp/kr20-wasm-compare-…/*.json` path, SHA-256 and size, not the request bytes (`wasm-compare/compare-real-both.receipt.json:2-9,28-32`; same shape in `compare-synth-both.receipt.json:2-9,28-32`). The S tree listing contains the receipts, stdout/stderr, evidence index and synth inputs, but no `real-both.json` or `synth-both.json`. Thus the entry’s instruction to “re-run the argv recorded” for compare (`knowledge/...wasm-interfaces.md:3`) is not verbatim replayable from S without reconstructing the input JSON; no reconstruction recipe is given. The wave-1 inspect/compare reports do record base B, so I do not count measured-revision omission as a defect (`w1/WasmInspectLeg.md:5`; `w1/WasmCompareLeg.md`, “Observed base”).

## QUALITY admission matrix (S: `corpus/QUALITY.md:11-35`)

| Row | Judgment | Reason |
|---|---|---|
| 1 | ADMIT, with correction | Paths, Evidence IDs and S041/S042 are resolvable; S040 resolves but its registered scope is unrelated to Wasm (see row 8). |
| 2 | ADMIT | Counts, hashes and success/error states make the observations falsifiable. |
| 3 | ADMIT | Specific to Wasm interface inspection and comparison. |
| 4 | REJECT as written | The table uses `~` and `…` in carrier paths, and the zxing comparison says only “two package releases” (`knowledge/...wasm-interfaces.md:13-16,26`). Receipts contain the full absolute paths and hashes, so this is not evidence of a wrong carrier; the entry must surface those paths rather than require a lookup. Synthetic rows also omit the two fixture hashes in the entry (they are recoverable from `SHA256SUMS`). |
| 5 | PARTIAL | Observation/inference headings and runtime limits are generally disciplined, but the ID-domain phrase at line 18 is an inference presented as observation; the generalized gate wording at line 34 should distinguish tested refusal cases from source-derived rule. |
| 6 | PARTIAL | All successful inspection and comparison claims have full Evidence IDs. The two invalid-input IDs at line 35 are abbreviated and their exact call/receipt filenames are not cited there; cite the full IDs or exact refusal receipts. |
| 7 | PARTIAL | It names >8 MiB, unrepresented non-function imports, partial-state paths and MCP summary as unexamined (`:44-45`), and limits version-regression coverage (`:28-30`). It does not explicitly bound other unvisited host modules/providers; state that the inspected set is four selected modules and name the remaining coverage boundary. |
| 8 | PARTIAL | REA/WABT versions and source type are pinned (`:2,9,34`), but S040 is not a Wasm CLI source as registered at `SOURCES.md:46`; replace that attribution with the exact Wasm source anchors in `w1/RevWasmVerb.md`/`w1/ScoutWasmSchema.md`. |
| 9 | ADMIT | No runtime behavior is inferred; static literal association, no execution, and ABI/runtime limits are explicit (`:36,41-45`). |
| 10 | ADMIT | The held claims use successful runs on real modules and retained synthetic fixtures; receipts show exit 0 and WABT 1.0.42. |
| 11 | ADMIT | The zero-import zip.js result is paired with a valid, complete 9-section parse and zero interface issues (`zip-js/receipt.json:42-58`), not an excluded member. |
| 12 | ADMIT | WAT recipes, output bytes, checksums and compiler receipt are retained (`synth/v1.wat`, `v2.wat`, `build-receipt.json`, `SHA256SUMS`). |
| 13 | N/A | No minified-file occurrence count is claimed. |
| 14 | REJECT for the parenthetical | Same-path/same-content/same-parameter repetition does not establish the full Evidence-ID domain or whether path is part of it; the subject SHA is retained, but no cross-path identity experiment is cited. |
| 15 | REJECT for the parenthetical | It gives no corpus citation for an ID domain per verb family; S040 is not such a citation. Replace with the bounded repeat observation and say the ID domain was not tested. |
| 16 | N/A | No research Gate quotation appears. |
| 17 | N/A | No research Gate quotation appears. |
| 18 | REJECT as recheck guidance | Compare’s prescribed receipt argv points to an unretained temporary JSON input; only its path/hash/size survive. Retain that input or add a complete reconstruction recipe and recheck command. |
| 19 | PARTIAL | The repeated-call statement is supportable as equality of two retained output hashes/IDs, not temporal continuity; both receipts record the same second-resolution interval. Keep it explicitly limited to the two recorded calls. |
| 20 | N/A | No provider-log observation is claimed. |
| 21 | PARTIAL | The statement that receipts retain argv/env/times/hashes is factually borne out by the JSON, but the stated recheck does not print the retained keys at S as row 21 requires. Add a key-printing recheck or remove the retention-compliance assertion. No comparator verdict is misdescribed as its input object. |
| 22 | N/A | No wave seat-status count is claimed. |
| 23 | PARTIAL / not established by this entry | Zoned run times are retained and precede S’s committer time, but this entry cites no strict `evidence-timestamps.py` result. Do not treat this file as proof of the round-wide check. |
| 24 | N/A | “No target execution” describes the observed WASM analysis limitation, not an enforced no-execution contract. |
| 25 | ADMIT for the successful holds | Retained successful stdout bytes carry the verb operation and full `ev_` ID, with exit-0 receipts and empty stderr. Compare has `subject:null`, but the entry states it consumes two inspect Evidence records and the outputs bind both carrier hashes; it is not a carrierless architecture-list result. Exit-1 partial error IDs are explicitly excluded from a held result. |

## Smallest safe correction

Expand every abbreviated carrier path and include the synth fixture hashes in the entry; correct the S040 citation and label the gate as tested behavior versus source-derived inference; remove the unsupported Evidence-ID-domain parenthetical unless it is independently sourced; replace the compare recheck with retained request JSON or a full deterministic rebuild recipe; and add the missing receipt-key check and unvisited-module scope. No re-analysis is needed to preserve the already-supported findings.

## Read-only command record

All commands below were read-only; no REA CLI invocation, analysis, install, or test was run by this seat.

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:corpus/knowledge/2026-10-20-r20-wasm-interfaces.md` — exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:corpus/QUALITY.md` — exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin ls-tree -r --name-only 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-20/evidence/c2/wasm-compare` — exit 0; no temporary compare request JSON appears in the tree.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/evidence/c2/wasm-inspect/evmole/stdout.json.xz | xz -dc | jq -e '.operation == "inspect_wasm_artifact" and .evidence_id == "ev_16a0be885adf3dee8f857604b91d409f4113a97e198b5875e0416f678e356d89" and .subject.digest.sha256 == "542b24e22eab36910fe2e797b329ab24b5423c0577fa85e49a97d9edf068b884"'` — exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9:.ufo/waves/round-20/evidence/c2/wasm-compare/compare-real-both.stdout.txt | jq -e '.operation == "compare_wasm_interfaces" and .evidence_id == "ev_38716779400ae692129c94bd6d0af9627a4f511cc401977979429e4874eeaaf7" and .normalized_result.left.artifact.sha256 == "6017eca5939cde1836e88e6d8cd27ae039246f206515ea4487bdfd0e3fb16e26" and .normalized_result.right.artifact.sha256 == "67b8e2b162da472e98cb48d3d32e3e38fff481b9b32ff4818e78bb248af88ab2"'` — exit 0.
- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin merge-base --is-ancestor 14f0260ad319ecc26994381b2415d5a999003375 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9` and the same command with freeze `808cbb31a1e24656da5ba4967497e602fbca7415` — exit 0 for both.