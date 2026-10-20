# Rizin PE leg — author findings

**Axes:** calibration (REA envelope vs Rizin result/exit), coverage (PE metadata, sections, invalid inputs, unknown command, chaining), depth (preflight error mapping and safe shell boundary).

## Observations

- **Carrier:** round-2 `cli-64.exe`, SHA-256 `bbb3de5707629e6a60a0c238cd477b28f07f0066982fda953fa6fcec39073a4a`, 14,336-byte PE32+. The original `uv/archive-v0/M1E0QXq07p7Gx3Fp` path was absent; an unblob setuptools copy with the exact historical digest was used. Host PATH resolves Rizin to `/usr/bin/rizin`, version 0.8.2; REA records provider version `null` (not a binary-hash binding). Evidence: `evidence/c2/rizin-pe/carrier-identity.md:3-33`, `01-iI/stdout.toon:1-12`.
- **`iI`:** exit 0, Evidence `ev_42df7881706281b45be31d097db03d0659f9f98701d7a42fff9cfddfff497a29`; stdout SHA-256 `141569ac43f05743bbaf360014d733049a73670b538c140ac6eb0256e528f0a4`. Rizin reports `bintype pe`, `class PE32+`, `bits 64`, `machine AMD 64`, `baddr 0x140000000`, `binsz 0x3800`, and separately `arch x86`. The REA envelope still says `format: unknown`, `architecture: null`; raw result is complete, exit 0, not truncated, `artifact_changed: false`. Evidence: `evidence/c2/rizin-pe/01-iI/receipt.json:2-13`, `01-iI/stdout.toon:21-29,39-42`.
- **`iS`:** exit 0, Evidence `ev_ca3b95815c78c0aa04e56dcbe9138ba960daf6a820f244a9824fa8e0dad08537`; stdout SHA-256 `34494e4a421fdffa0d180e67a2bacb3aeda6a039bf1e8fc4312bf6045729f2cb`. Six sections: `.text`, `.rdata`, `.data`, `.pdata`, `.rsrc`, `.reloc`; Evidence says complete, not truncated, artifact unchanged. Evidence: `evidence/c2/rizin-pe/02-iS/receipt.json:2-13`, `02-iS/stdout.toon:21-29`.
- **Nonexistent path and directory:** each command exits 1, emits no Evidence ID and the same generic `invalid_request` / `invalid_input` message; stdout SHA-256 `5bf61c0eb7f0c80c8fe8ddd47be9bf14cab6c2291968882a774aa8d1f60d0b08`. `--format json --full-output` retries also match each other: exit 1, no Evidence, same JSON error and 3 ms duration, stdout SHA-256 `eeb3530300fb12218d7671e3ba56c31fc508818b72ccbe675bdb4297cb4a1f24`. Receipts and outputs: `evidence/c2/rizin-pe/03-missing-path/{receipt.json:2-13,stdout.toon:1-6}`, `04-directory-path/{receipt.json:2-13,stdout.toon:1-6}`, `07-missing-json-full/{receipt.json:2-13,stdout.json:1}`, `08-directory-json-full/{receipt.json:2-13,stdout.json:1}`.
- **Unknown Rizin command:** `kr20_unknown_command` returns REA exit 0 with Evidence `ev_27ac86a5783d8c598fb3a043b82b01cef7154d493710a6bd1800c1815ec9c4e6`; Rizin's captured command-level stderr says the command does not exist and prints help for prefix `k`. The wrapper-level `stderr.txt` is empty; the observation is complete and the artifact is unchanged. Do not treat REA exit 0 as command success. Evidence: `evidence/c2/rizin-pe/05-unknown-command/receipt.json:2-13`, `05-unknown-command/stdout.toon:21-29`.
- **Chaining:** `iI; iS` ran both commands and returned exit 0, Evidence `ev_ee0f437c7ea9e580b80821569a8f7ae06d594543fc7ca2739f11fdfbdad1ce15`; stdout SHA-256 `82110b125a90d20282347f41195d46780915e77c9301f8bb42de7e83fdf8ebaa`, artifact unchanged. Evidence: `evidence/c2/rizin-pe/06-semicolon-chain/receipt.json:2-13`, `06-semicolon-chain/stdout.toon:18-38`.
- Five immediate replays of `iI`, `iS`, missing path, directory, and unknown command (receipts 09-13) have stdout SHA-256 values identical to their first receipts; successful repeats retain the same Evidence IDs. Example pair: `01-iI/receipt.json:11-13` and `09-rerun-iI/receipt.json:25-37`; remaining pairs are retained in matching `02/10`, `03/11`, `04/12`, and `05/13` directories. All 13 REA invocations have argv, cwd, `REA_*` environment snapshot (empty), UTC start/end, exit, output paths/hashes, and carrier path/SHA. Each output is below 8 MiB; no compression was needed.

## Safety and limitations

- **[INFERENCE, source-backed]** Missing and non-regular paths fail REA's pre-run digest gate, which maps digest failures to generic `AnalysisInputError`; the returned error omits the original filesystem errno. Source notes: `evidence/c2/rizin-pe/rea-cli-source-notes.md:5-8,14`.
- **[OBSERVATION]** The Rizin Handbook says `!<command>` executes through `system(3)` and `;` separates commands; REA's own contract warns that commands/plugins can execute code or mutate/access external resources. `!echo` was **not run** because no REA refusal guarantee was documented. Evidence/source notes: `evidence/c2/rizin-pe/rea-cli-source-notes.md:9-11`; mined source row `corpus/SOURCES.md:46`.
- One PE and one local Rizin host version; the REA envelope does not identify the provider version or bind the provider executable by digest. Rizin command/plugin external inputs are outside the Evidence boundary. No target execution or file-writing Rizin command was used. The candidate coverage entry is `corpus/knowledge/2026-10-20-rizin-pe-command-observation.md:1-2,46`; proposed source row S040 is integration-assigned.

## Delivery

- Clone base observed: `14f0260ad319ecc26994381b2415d5a999003375`.
- Patch: `.ufo/waves/round-20/w1/patches/KaidokuR20.RizinPeLeg-2.patch`.
- `git -C /tmp/kr20-KaidokuR20.RizinPeLeg-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375`:

```text
 .../evidence/c2/rizin-pe/01-iI/receipt.json        | 14 +++++++
 .../round-20/evidence/c2/rizin-pe/01-iI/stderr.txt |  0
 .../evidence/c2/rizin-pe/01-iI/stdout.toon         | 46 ++++++++++++++++++++++
 .../evidence/c2/rizin-pe/02-iS/receipt.json        | 14 +++++++
 .../round-20/evidence/c2/rizin-pe/02-iS/stderr.txt |  0
 .../evidence/c2/rizin-pe/02-iS/stdout.toon         | 46 ++++++++++++++++++++++
 .../c2/rizin-pe/03-missing-path/receipt.json       | 14 +++++++
 .../c2/rizin-pe/03-missing-path/stderr.txt         |  0
 .../c2/rizin-pe/03-missing-path/stdout.toon        |  6 +++
 .../c2/rizin-pe/04-directory-path/receipt.json     | 14 +++++++
 .../c2/rizin-pe/04-directory-path/stderr.txt       |  0
 .../c2/rizin-pe/04-directory-path/stdout.toon      |  6 +++
 .../c2/rizin-pe/05-unknown-command/receipt.json    | 14 +++++++
 .../c2/rizin-pe/05-unknown-command/stderr.txt      |  0
 .../c2/rizin-pe/05-unknown-command/stdout.toon     | 46 ++++++++++++++++++++++
 .../c2/rizin-pe/06-semicolon-chain/receipt.json    | 14 +++++++
 .../c2/rizin-pe/06-semicolon-chain/stderr.txt      |  0
 .../c2/rizin-pe/06-semicolon-chain/stdout.toon     | 46 ++++++++++++++++++++++
 .../c2/rizin-pe/07-missing-json-full/receipt.json  | 14 +++++++
 .../c2/rizin-pe/07-missing-json-full/stderr.txt    |  0
 .../c2/rizin-pe/07-missing-json-full/stdout.json   |  1 +
 .../rizin-pe/08-directory-json-full/receipt.json   | 14 +++++++
 .../c2/rizin-pe/08-directory-json-full/stderr.txt  |  0
 .../c2/rizin-pe/08-directory-json-full/stdout.json |  1 +
 .../evidence/c2/rizin-pe/09-rerun-iI/receipt.json  | 39 ++++++++++++++++++
 .../evidence/c2/rizin-pe/09-rerun-iI/stderr.txt    |  0
 .../evidence/c2/rizin-pe/09-rerun-iI/stdout.toon   | 46 ++++++++++++++++++++++
 .../evidence/c2/rizin-pe/10-rerun-iS/receipt.json  | 39 ++++++++++++++++++
 .../evidence/c2/rizin-pe/10-rerun-iS/stderr.txt    |  0
 .../evidence/c2/rizin-pe/10-rerun-iS/stdout.toon   | 46 ++++++++++++++++++++++
 .../c2/rizin-pe/11-rerun-missing/receipt.json      | 37 +++++++++++++++++
 .../c2/rizin-pe/11-rerun-missing/stderr.txt        |  0
 .../c2/rizin-pe/11-rerun-missing/stdout.toon       |  6 +++
 .../c2/rizin-pe/12-rerun-directory/receipt.json    | 37 +++++++++++++++++
 .../c2/rizin-pe/12-rerun-directory/stderr.txt      |  0
 .../c2/rizin-pe/12-rerun-directory/stdout.toon     |  6 +++
 .../c2/rizin-pe/13-rerun-unknown/receipt.json      | 39 ++++++++++++++++++
 .../c2/rizin-pe/13-rerun-unknown/stderr.txt        |  0
 .../c2/rizin-pe/13-rerun-unknown/stdout.toon       | 46 ++++++++++++++++++++++
 .../evidence/c2/rizin-pe/carrier-identity.md       | 33 ++++++++++++++++
 .../evidence/c2/rizin-pe/rea-cli-source-notes.md   | 14 +++++++
 corpus/SOURCES.md                                  |  5 +++
 .../2026-10-20-rizin-pe-command-observation.md     | 46 ++++++++++++++++++++++
 43 files changed, 749 insertions(+)
```
