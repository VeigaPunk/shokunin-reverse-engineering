# C2 Harmony application-graph leg

**Axis:** coverage; this is a bounded author-side hold of `project-harmony-application-graph` on two synthetic HAP carriers, not a shipped HarmonyOS package or device result.

## Observations

- Stage carrier SHA-256 `21d46dbc88ba8f8c1306a70f727d8ee0383dc37c19430463dc7849f557c4a65f`: `inspect-artifact` exit 0; outer Evidence `ev_7c80b736aa635c44a0ea222bb6db2f1540d0f8bac65bd9c280c1efbc76fbe52e`, nested inventory Evidence `ev_ae4600c27ed4b6ed50dccafeb3983157577ab59835d2d0d21c9876e4ab25031b`, 4 nodes/4 occurrences and complete central-directory coverage. Projection exit 0; Evidence `ev_a437cf77ed5381ee7e71d36a87a7407bd5f38cb911a2432e8eb69ff554a74820`; hint `stage`, `complete-within-inventory`, `ark`; manifest `module.json`, bytecode `ets/modules.abc`, resource `resources.index`; 0 bridge candidates. Evidence anchors: `.ufo/waves/round-20/evidence/c2/harmony/stage-json/inventory-evidence.pretty.json:6,13-17,48-57,100-165` and `project-stage-json/projection-evidence.pretty.json:6,29-81`.
- FA carrier SHA-256 `9cb84d18fade6e7653d90a15d01d18179f9f47fb92187954dfbdf75bff6c2457`: `inspect-artifact` exit 0; outer Evidence `ev_9f377f35879ed711cb983a6bc0fe90b7baaa0dafe8eebac20145ff96ca512ba5`, nested inventory Evidence `ev_6fb3f68a68d59baedb0850eced6cc7217514f241ebec689934f3e47877d44fbe`, 4 nodes/4 occurrences and complete central-directory coverage. Projection exit 0; Evidence `ev_ac0c26dccd8db383f2ac848cab213e3a375e4b261072b57f52c037c45a32ab92`; hint `fa`, `complete-within-inventory`, `ark`; manifest `config.json`, bytecode `ets/modules.abc`, resource `resources.index`; 0 bridge candidates. Anchors: `.ufo/waves/round-20/evidence/c2/harmony/fa-json/inventory-evidence.pretty.json:6,13-17,48-57,100-165` and `project-fa-json/projection-evidence.pretty.json:6,29-81`.
- Each call has `argv`, cwd, empty `REA_*` set, UTC start/end, exit, stdout/stderr paths and SHA-256, plus carrier path/hash in its `receipt.json`; see `stage-json/receipt.json:2-20,34-38`, `fa-json/receipt.json:2-20,34-38`, `project-stage-json/receipt.json:2-25,33-45`, and `project-fa-json/receipt.json:2-25,33-45`. Schema calls exited 0; projection input shape (`inputJson`) and inspect path shape are at `schema-project/stdout.txt:1-8` and `schema-inspect/stdout.txt:1-18`, with receipts adjacent.
- Exact carrier archives and member-byte recipe are retained at `carriers/stage.hap`, `carriers/fa.hap`, and `carrier-recipe.json:1-53` (base64 member bytes, hashes/lengths, ZIP metadata and Python version). Stage's `module.json` bytes declare module `entry` and `EntryAbility`; the FA recipe carries `config.json` plus the same `resources.index` and placeholder `ets/modules.abc` bytes.

## Calibration and limits

- The first two projections exited 1 with `invalid_request`: the input reconstructed from the default presentation output carried `limitations[1]` instead of the required `limitations` array (`project-stage/stdout.txt:9-15`, `project-fa/stdout.txt:9-15`). Both exact payload snapshots and receipts are retained (`project-stage/receipt.json:20-24`, `project-fa/receipt.json:20-24`). Re-running inspections with `--json`, then passing the nested inventory Evidence unchanged, yielded the successful projections above.
- **Inference:** `stage`/`fa` is path-presence only (`module.json` versus `config.json`), not semantic manifest validation; installed source is `dist/domain/harmony/harmonyApplication.js:110-117` and the explanation is retained in `project-stage-json/projection-evidence.pretty.json:62-69`.
- **Unknown:** the `ets/modules.abc` payload is an invalid text placeholder, so the `ark` family hint is not verified bytecode. No manifest/resource semantics, signing state, actual package validity, runtime behavior, device install, N-API declaration/call, HSP, App Pack, or `.har` handling was established. Empty signing entries do not establish unsigned status; projection limitations are at `project-stage-json/projection-evidence.pretty.json:62-69` and `project-fa-json/projection-evidence.pretty.json:62-69`.
- **LSP unavailable:** no LSP device is exposed in this seat's tool inventory; source inspection used targeted grep/read. No tool was installed or updated.

Patch: `.ufo/waves/round-20/w1/patches/KaidokuR20.HarmonyLeg-2.patch` (authored from baseline `14f0260ad319ecc26994381b2415d5a999003375`; source row ID `S040` is provisional because round-20 IDs are assigned at integration).

Patch stat from `git -C /tmp/kr20-KaidokuR20.HarmonyLeg-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375`:

```text
 .../evidence/c2/harmony/carrier-recipe.json        |  54 ++++++
 .../round-20/evidence/c2/harmony/carriers/fa.hap   | Bin 0 -> 604 bytes
 .../evidence/c2/harmony/carriers/stage.hap         | Bin 0 -> 548 bytes
 .../harmony/fa-json/inventory-evidence.pretty.json | 189 +++++++++++++++++++
 .../evidence/c2/harmony/fa-json/receipt.json       |  40 ++++
 .../evidence/c2/harmony/fa-json/stderr.txt         |   0
 .../evidence/c2/harmony/fa-json/stdout.txt         |   1 +
 .../round-20/evidence/c2/harmony/fa/receipt.json   |  33 ++++
 .../round-20/evidence/c2/harmony/fa/stderr.txt     |   0
 .../round-20/evidence/c2/harmony/fa/stdout.txt     | 205 +++++++++++++++++++++
 .../projection-evidence.pretty.json                | 106 +++++++++++
 .../c2/harmony/project-fa-json/receipt.json        |  46 +++++
 .../evidence/c2/harmony/project-fa-json/stderr.txt |   0
 .../evidence/c2/harmony/project-fa-json/stdout.txt |   1 +
 .../c2/harmony/project-fa/initial-input.json       |   1 +
 .../evidence/c2/harmony/project-fa/input.json      |   1 +
 .../evidence/c2/harmony/project-fa/receipt.json    |  39 ++++
 .../evidence/c2/harmony/project-fa/stderr.txt      |   0
 .../evidence/c2/harmony/project-fa/stdout.txt      |  15 ++
 .../projection-evidence.pretty.json                | 106 +++++++++++
 .../c2/harmony/project-stage-json/receipt.json     |  46 +++++
 .../c2/harmony/project-stage-json/stderr.txt       |   0
 .../c2/harmony/project-stage-json/stdout.txt       |   1 +
 .../c2/harmony/project-stage/initial-input.json    |   1 +
 .../evidence/c2/harmony/project-stage/input.json   |   1 +
 .../evidence/c2/harmony/project-stage/receipt.json |  39 ++++
 .../evidence/c2/harmony/project-stage/stderr.txt   |   0
 .../evidence/c2/harmony/project-stage/stdout.txt   |  15 ++
 .../c2/harmony/schema-inspect/receipt.json         |  27 +++
 .../evidence/c2/harmony/schema-inspect/stderr.txt  |   0
 .../evidence/c2/harmony/schema-inspect/stdout.txt  |  18 ++
 .../c2/harmony/schema-project/receipt.json         |  27 +++
 .../evidence/c2/harmony/schema-project/stderr.txt  |   0
 .../evidence/c2/harmony/schema-project/stdout.txt  |   8 +
 .../stage-json/inventory-evidence.pretty.json      | 189 +++++++++++++++++++
 .../evidence/c2/harmony/stage-json/receipt.json    |  40 ++++
 .../evidence/c2/harmony/stage-json/stderr.txt      |   0
 .../evidence/c2/harmony/stage-json/stdout.txt      |   1 +
 .../evidence/c2/harmony/stage/receipt.json         |  33 ++++
 .../round-20/evidence/c2/harmony/stage/stderr.txt  |   0
 .../round-20/evidence/c2/harmony/stage/stdout.txt  | 205 +++++++++++++++++++++
 corpus/README.md                                   |   3 +-
 corpus/SOURCES.md                                  |   3 +
 .../2026-10-20-r20-harmony-application-graph.md    |  28 +++
 44 files changed, 1521 insertions(+), 1 deletion(-)
```
