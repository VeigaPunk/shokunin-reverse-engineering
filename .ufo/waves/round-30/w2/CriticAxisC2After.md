# CriticAxisC2After — post-data depth-axis fit, non-code predictor ceiling, and shared-message pairs

Seat: `KaidokuR30.CriticAxisC2After` (critic, wave 2). Access date: `2026-10-23`.
Target attacked: R30-C2 (`depth`) after data collection (`24da3459`) and the SKILL lead-line repair (`92b1dd2ddc119fda89a611ba515bdf6cfe906f76`).

## Verdict

- **Attack verdict: `holds` (with four bounded qualifications / fixable calibration disclosures below; no canonical-judge rejection required).**
- **1. Is R30-C2 a depth move after data?** **Yes (Observation + Inference).** Before data (`w1/CriticAxisFitC2.md`), `skill_ok` in `tools/round-30/c2-rust-refusals.py:273-277` was noted as under-enforcing `AXES.md:11` (“decision tables with real thresholds, named error signatures, cited sources”) because the counter checks only for a new `SKILL.md` line naming `inspect-rust-binary` and the entry path. At `92b1dd2d`, however, `SKILL.md:966-995` and `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` actually land the 19-row decision table with real numerical thresholds (`size > 0`, `SHF_COMPRESSED = 0x800`, `1 MiB = 1,048,576` B compressed section cap, `min(8 MiB, 64 × section bytes) = 896,576` B inflate bound, `nesting ≤ 32`, `format` non-negative integer, package count `584`), 13 distinct exact reader refusal messages across 16 refusal mutants, 3 positive boundary acceptances (`g-relocated`, `g-recompressed`, `g-no-root`), the outer envelope `error.code` split (`invalid_request` vs `unsupported_target` vs `resource_constraint`), and the caller rule to read `error.details.issues` because top-level `error.message` is generic on 13 of 16 refusals.
- **2. Could a predictor that never read the code (`S090`) have matched 19/19?** **No for genuine pre-run prediction (`≤ 12/19` under strict `S089` spec + `strings`, or `≤ 14/19` even if assisted by `g-`/`r-` mutant-ID prefixes); yes only via post-freeze answer-key copying or unpinned counter-substring gaming (Inference + Observation).** Seven frozen rows are code-reading traps where `S089` (`PARSING.md`, `cargo-auditable.schema.json`) and lexical `strings` extraction on `cli.js` either disagree with REA 6.5.0's implementation or expose decoy literals.
- **3. Do the three shared-message pairs weaken the 19/19?** **They narrow live branch discrimination from 16 refusal mutants to 13 distinct refusal messages (14 distinct outcome classes including acceptance), because each pair's two live envelopes are byte-identical modulo `<MUTANT_PATH>` and `<DURATION>`; however, they do NOT weaken the proof against non-code predictors — on the contrary, all three pairs contain decoy traps that defeat predictors that did not trace the code (Observation + Inference).**

---

## 1. Strongest counterexample: the `S089`-spec + `strings` non-code predictor (`12/19` strict, `14/19` prefix-assisted)

Wave 1 (`w1/CriticAxisFitC2.md`) showed that four trivial baselines fail `P2-match`:
- Always-refuse without message: `0/19`;
- Single generic refusal message (`CtlC2Sequence.md` control 4, `"Dependency section is not a complete zlib stream"`): `2/19` (`0/19` without committed envelopes);
- Command help strings: `0/19`;
- Uniformly shuffled 18-string lexical catalog from `strings -a -n 4 cli.js`: expected `13/18 ≈ 0.722/19` (or `11/8 = 1.375/19` when shuffling the 16 exact frozen refusal messages across the 16 refusal rows; `CtlC2Sequence.md` control 5 `rotated-messages` hit only the `3` adjacent duplicate-message rows).

After data, we test a much stronger counterexample: **an informed domain predictor that reads the mutant IDs, reads the official `cargo-auditable` specification (`S089`: `README.md`, `PARSING.md`, `cargo-auditable.schema.json`), and extracts the 18 literal diagnostic strings from `dist/cli-runtime/cli.js` via `strings`, but never reads the REA 6.5.0 JavaScript control flow (`S090`)**.

**Observation (`E2`, exit 0, `2026-10-23T03:17:39Z`):** This strongest non-code predictor matches **12/19** strictly (or **14/19** if allowed to override `S089` using the `g-`/`r-` mutant-ID prefixes on `g-no-root` and `r-inflate-ratio`), failing **7 code-specific trap rows**:

| Mutant | True frozen & live outcome (`S090`) | Non-code `S089` + `strings` prediction | Why non-code prediction fails without reading `S090` |
|---|---|---|---|
| `g-no-root` | `ok` (`root_package_index: null`) | `refuse` (`PARSING.md:48-52`) | `PARSING.md:48-52` explicitly lists `1. Zero root packages` alongside `1. More than one root package` as an invalid state and requires “only one package with `root: true`.” `cargo-auditable.schema.json:62-65` makes `root` an optional boolean with no document-level cardinality check (which would allow both `0` and `2` roots). Only `RustAuditableReader.js:301-308` (`if (roots.length > 1) throw ... return roots[0] ?? null`) reveals REA's asymmetric rule (`0` accepted, `>1` refused). |
| `r-empty` | `refuse`: `Dependency section is not file-backed` | `refuse`: `Dependency section is empty` | `RustAuditableReader.js:52` contains the literal decoy string `"Dependency section is empty"`, which appears in `strings cli.js`. Without reading `GoBinaryContainer.js:80` (`file_backed: size > 0n`) and `RustBinaryImage.js:52-53` (`if (!section.file_backed)`), a non-code predictor maps `r-empty` (`sh_size = 0`) to `"Dependency section is empty"` and misses. |
| `r-trailing-bytes` | `refuse`: `Dependency section is not a complete zlib stream` | `refuse`: `Dependency section has bytes after the zlib stream` | `RustAuditableReader.js:87` contains the literal decoy string `"Dependency section has bytes after the zlib stream"`, which appears in `strings cli.js`. Only reading `RustAuditableReader.js:80-115,140-143` plus knowing Node `v24.21.0` sets `rejectsTrailingJunk() === true` (`ERR_TRAILING_JUNK_AFTER_STREAM_END`) shows that line 87 is bypassed and `inflateFailure` emits `"Dependency section is not a complete zlib stream"`. |
| `r-inflate-ratio` | `refuse`: `Inflated dependency JSON exceeds the size limit` | `ok` (under `PARSING.md:34`) | `PARSING.md:34` states “8 MiB should be more than enough to hold any legitimate audit data.” The mutant's uncompressed JSON is `3,201,452` B (`~3.05 MiB < 8 MiB`). Only `RustAuditableReader.js:9,79` reveals `RUST_INFLATE_RATIO = 64` (`min(8 MiB, 14009 × 64) = 896,576` B, matching `reported_limits.maximum_bytes: 896576` in `r-inflate-ratio.json`). |
| `r-extra-field` | `refuse`: `Dependency package 0 does not match the package schema` | `refuse`: `Dependency JSON does not match the package schema` | Upstream `cargo-auditable.schema.json:32-79` does not set `additionalProperties: false` on `Package`. Moreover, `strings cli.js` contains the whole literal `"Dependency JSON does not match the package schema"` (`RustAuditableReader.js:170`), whereas the per-package template at `:236` is split at `${String(index)}`. Only reading `parseDocument` (`:167-170`) shows `rejectMalformedPackages` runs before `documentSchema.safeParse` and interpolates index `0`. |
| `r-kind-dev` | `refuse`: `Dependency package 0 does not match the package schema` | `refuse`: `Dependency JSON does not match the package schema` | Same ordering and template trap as `r-extra-field`: `rejectMalformedPackages` (`:167,235-236,251-254`) preempts `documentSchema.safeParse` (`:168-170`) and interpolates package index `0`. |
| `r-index-outside` | `refuse`: `Dependency index 584 from package 0 is outside the package list` | `refuse`: uninstantiated fragment ` is outside the package list` | In `cli.js`, `rootIndex` (`RustAuditableReader.js:306`) is a two-parameter template (`Dependency index ${String(outside)} from package ${String(index)} is outside the package list`). Spelling the exact string requires knowing both the template wording and the carrier's package count `n = 584` plus edited package index `0`. |

---

## 2. Do the three shared-message pairs weaken the 19/19?

**Observation (`E1`, exit 0, `2026-10-23T03:14:07Z`):** The 19 frozen rows in `predictions.tsv` comprise 3 acceptances and 16 refusals, but only **13 distinct refusal messages** (14 distinct predicted outcomes in total). Three refusal messages are shared across two mutants each:

1. **`r-empty` and `r-nobits` → `"Dependency section is not file-backed"`**
   - *Upstream branches:* `r-empty` sets `sh_size = 0`, hitting `declaredFileRange` (`GoBinaryContainer.js:80`, `file_backed: size > 0n`). `r-nobits` sets `sh_type = 8` (`SHT_NOBITS`), hitting `elfImageSection` (`GoElfImage.js:186`, `type === SHT_NOBITS ? { ...declared, file_backed: false } : declared`).
   - *Shared throw site:* Both collapse to `section.file_backed === false` and hit the same throw at `RustBinaryImage.js:52-53`.
   - *Live envelope comparison (`E1`):* `r-empty.json` and `r-nobits.json` are **byte-for-byte identical** after replacing `/fast/scratch/hyaku/kaidoku-r30/mutants/<id>` and `meta.duration` (`263ms` vs `230ms`).
2. **`r-not-zlib` and `r-trailing-bytes` → `"Dependency section is not a complete zlib stream"`**
   - *Upstream branches:* `r-not-zlib` feeds 9,870 non-zlib bytes (`inflateSync` throws `Z_DATA_ERROR`, matched by `code.startsWith("Z_")` at `RustAuditableReader.js:141`). `r-trailing-bytes` appends 4 bytes to the valid 9,870-byte stream (`inflateSync` with `rejectGarbageAfterEnd: true` on Node `v24.21.0` throws `ERR_TRAILING_JUNK_AFTER_STREAM_END`, matched at `RustAuditableReader.js:140`).
   - *Shared throw site:* Both branches of the disjunction in `inflateFailure` (`RustAuditableReader.js:140-143`) return the same `RustAuditableFormatFailure("malformed", "Dependency section is not a complete zlib stream")`, and `RustBinaryProvider.js` drops `cause.code` when building the CLI envelope.
   - *Live envelope comparison (`E1`):* `r-not-zlib.json` and `r-trailing-bytes.json` are **byte-for-byte identical** modulo `<MUTANT_PATH>` and `meta.duration` (`259ms` vs `180ms`).
3. **`r-extra-field` and `r-kind-dev` → `"Dependency package 0 does not match the package schema"`**
   - *Upstream branches:* `r-extra-field` adds `features: []` to package `0` (`packageRecord` returns `false` at `RustAuditableReader.js:243-245`, `!PACKAGE_FIELDS.has(key)`). `r-kind-dev` sets `kind: "dev"` on package `0` (`packageRecord` returns `false` at `RustAuditableReader.js:251-254`).
   - *Shared throw site:* Both return `false` to `rejectMalformedPackages` (`RustAuditableReader.js:235-236`) on package index `0`, throwing the identical string. (Had one mutant targeted package `1` instead of package `0`, the interpolated index would at least have distinguished them.)
   - *Live envelope comparison (`E1`):* `r-extra-field.json` and `r-kind-dev.json` are **byte-for-byte identical** modulo `<MUTANT_PATH>` and `meta.duration` (`181ms` vs `182ms`).

### Two-sided evaluation of how the shared pairs affect R30-C2

- **Where they weaken 19/19 (live branch-isolation power — Inference):**
  - Because `judge()` (`c2-rust-refusals.py:200-207`) and the live CLI envelopes cannot distinguish the two members of each pair, a live `19/19` score proves **13 distinct refusal throw signatures and 3 distinct positive envelopes (16 distinct output signatures across 19 inputs)**, not 16 distinct refusal throw sites.
  - Specifically, from the live REA envelope alone, `P2-match` on `r-nobits` cannot prove `SHT_NOBITS` was the operative cause rather than `size === 0`; `P2-match` on `r-trailing-bytes` cannot prove `ERR_TRAILING_JUNK_AFTER_STREAM_END` fired rather than `Z_DATA_ERROR`; and `P2-match` on `r-kind-dev` cannot prove the `kind` check fired rather than another `packageRecord` clause on package 0. Distinguishing the two branches inside each pair relies on the deterministic mutant builder (`c2-rust-refusals.py:129-160`) and the Wave 1 header/Node inspections (`w1/RevPredRefuseA.md`, `w1/RevPredRefuseB.md`).
  - Both `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md:50` and `w1/RevSelftestLookalikes.md:215-220` explicitly disclose this limitation.
- **Where they strengthen 19/19 (anti-guessing / code-reading proof — Inference):**
  - The three shared-message pairs are **not** redundant padding for a predictor: each pair tests a many-to-one mapping in the code where a naive predictor expects a distinct message (`"Dependency section is empty"` for `r-empty`, `"Dependency section has bytes after the zlib stream"` for `r-trailing-bytes`, and `"Dependency JSON does not match the package schema"` for `r-extra-field`/`r-kind-dev`). Predicting that these three pairs *share* messages rather than emitting the decoy literals in `RustAuditableReader.js:52,87,170` is stronger evidence of code reading than 1-to-1 literal matching.

---

## 3. Post-data instrument and documentation findings (fixable defects vs acceptable scope)

### Finding F1 — Substring matching in `judge()` plus `--rev` prediction pinning makes `freeze-gate` load-bearing (calibration / counter design)

- **Observation (`E1`, `E2`):** In the 16 committed refusal envelopes (`corpus/evidence/round-30/c2/envelopes/r-*.json`), 13 of 16 have `"error.code": "invalid_request"` with the generic top-level `"error.message": "Analysis input is invalid. Check the arguments and try again."` and carry the specific reader diagnostic only inside `error.details.issues[0].message`. Moreover, 15 of 16 contain `"Selected artifact /fast/scratch/hyaku/kaidoku-r30/mutants/"`, and 16 of 16 contain `"inspect_rust_binary"`.
- **Counterexample / Inference:** `judge()` (`tools/round-30/c2-rust-refusals.py:205`) checks `message not in out_text and message not in err_text` across the entire raw JSON stdout string, and `measure()` (`:325-328`) checks only that working-tree `predictions.tsv` equals `<rev>:corpus/evidence/round-30/c2/predictions.tsv` (confirmed live in `w1/CtlC2Sequence.md:505-507`, where controls 3–5 edited `predictions.tsv` in a sandbox commit and were measured rather than `exit 2` PIN-rejected). Consequently, if `predictions.tsv` were not externally pinned to its freeze digest `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` by `claims.json` and `prefreeze-gate.py`, a predictor that never read the code could set `message` to `"Analysis input is invalid. Check the arguments and try again."` (matching 13/16 refusals), `"Selected artifact /fast/scratch/hyaku/kaidoku-r30/mutants/"` (matching 15/16), or `"inspect_rust_binary"` (matching 16/16).
- **Impacted axes:** `calibration`, `depth`.
- **Smallest safe correction:** Fixable / already mitigated by the external freeze pin (`claims.json:54`, `prefreeze-gate.py`). Do not claim `c2-rust-refusals.py` alone enforces prediction immutability or exact-field equality; `freeze-gate.py` / `prefreeze-gate.py` + the frozen `predictions.tsv` SHA-256 (`6852df3a…`) are part of the verification chain.

### Finding F2 — Committed-envelope check for refusals verifies only `ok: false` parity (`CtlC2Sequence.md` control 7)

- **Observation (`w1/CtlC2Sequence.md:415-461, 509-542`, `tools/round-30/c2-rust-refusals.py:246-255`):** Refusal envelopes have no `evidence_id`. In `committed_agrees()`, when `l_ok` is `False`, the counter checks only `c_ok != l_ok` and `added > freeze_ct`. In `CtlC2Sequence` control 7 (`predictions-copied-as-observations`), 16 fabricated refusal JSON files (`{"ok":false,"error":{"message":"..."}}`) matched `16/19` (`P2-match`), while the 3 positive rows (`g-relocated`, `g-recompressed`, `g-no-root`) failed with `committed evidence_id differs`. Furthermore, after `git revert` restored the working tree (`CtlC2Sequence.md:515-542`), `show(root, rev, rel)` returned `None` (`c_ok = False`) while `first_add` still saw the reverted add commit in history, so even absent committed refusal files satisfied `committed_agrees` (`matches=16`).
- **Impacted axes:** `calibration`.
- **Smallest safe correction:** This is already disclosed in `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md:51`. Keep the disclosure that the live REA re-run and the 3 positive `evidence_id` checks are the authority preventing a fabricated pass.

### Finding F3 — Unexercised reader refusal signatures in `RustAuditableReader.js` and `RustBinaryImage.js`

- **Observation (`RustAuditableReader.js:51-52, 85-87, 168-170, 200-204`; `RustBinaryImage.js:94-98`):** Across `RustBinaryImage.js` and `RustAuditableReader.js`, there are 18 static/template refusal throw sites for `inspect_rust_binary` (excluding container-shared `GoBinaryContainer`/`GoElfImage` structural throws):
  - **13 distinct refusal messages** are exercised live by the 16 refusal mutants.
  - **5 refusal messages in those two files are not exercised live:**
    1. `"Dependency section is empty"` (`RustAuditableReader.js:52`) — unreachable via ELF section header `sh_size = 0` because container `file_backed` fires first (disclosed in entry line 45);
    2. `"Dependency section has bytes after the zlib stream"` (`RustAuditableReader.js:87`) — unreachable on Node `v24.21.0` where `rejectsTrailingJunk()` is `true`;
    3. `"Dependency JSON does not match the package schema"` (`RustAuditableReader.js:170`) — reached only when top-level `documentSchema.safeParse(value)` fails after `documentVersionSchema` and `rejectMalformedPackages` pass (e.g., missing/non-array `packages` or an extra top-level key alongside `format` and `packages`);
    4. `"Dependency graph exceeds the complete report byte budget before expansion"` (`RustAuditableReader.js:204`, `8 MiB` report budget) — disclosed as code-read only in entry line 49 and `SKILL.md:994`;
    5. `"Read-only data contains more than 64 distinct rustc commit paths."` (`RustBinaryImage.js:98`, `MAX_RUSTC_HASHES = 64`).
  - Additionally, for `"Inflated dependency JSON exceeds the size limit"` (`RustAuditableReader.js:79,139`), `r-inflate-ratio` exercises the `64 × compressed_bytes` (`896,576` B) arm of `Math.min(RUST_UNCOMPRESSED_BYTES, bytes.length * RUST_INFLATE_RATIO)`, leaving the `8 MiB` (`RUST_UNCOMPRESSED_BYTES`) arm code-read only.
- **Impacted axes:** `depth`, `calibration`.
- **Smallest safe correction:** Fixable documentation precision (optional in entry/SKILL limits): note that top-level `documentSchema` failures (`RustAuditableReader.js:170`, `"Dependency JSON does not match the package schema"`) and the `8 MiB` uncompressed arm of `Math.min` are code-read only alongside the `256 MiB` input cap and `8 MiB` report budget. This does not invalidate `R30-C2` (`19/19` frozen predictions hold live).

---

## Evidence receipts

### E1 — Post-data envelope and shared-pair audit

Producing command:
```sh
timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/audit_c2_after.py
```
UTC: `2026-10-23T03:14:07Z`. Exit code: **0**. Exact stdout excerpt:
```json
{
  "utc": "2026-10-23T03:14:07Z",
  "total_predictions": 19,
  "accept_count": 3,
  "refuse_count": 16,
  "distinct_refusal_messages": 13,
  "shared_message_pairs": {
    "Dependency section is not file-backed": [
      "r-empty",
      "r-nobits"
    ],
    "Dependency section is not a complete zlib stream": [
      "r-not-zlib",
      "r-trailing-bytes"
    ],
    "Dependency package 0 does not match the package schema": [
      "r-extra-field",
      "r-kind-dev"
    ]
  },
  "pair_identical_modulo_path_duration": {
    "r-empty vs r-nobits": true,
    "r-not-zlib vs r-trailing-bytes": true,
    "r-extra-field vs r-kind-dev": true
  }
}
```

### E2 — Non-code (`S089` + `strings`) predictor evaluation and C2 `--selftest`

Producing command:
```sh
timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/noncode_predictors_after.py && timeout 60 python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py --selftest > /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/c2-selftest.stdout.txt && date -u +%Y-%m-%dT%H:%M:%SZ
```
UTC: `2026-10-23T03:17:39Z`. Exit code: **0**. Exact stdout excerpt:
```json
{
  "utc": "2026-10-23T03:17:39Z",
  "strict_spec_plus_strings_exact_matches_of_19": 12,
  "prefix_assisted_spec_plus_strings_exact_matches_of_19": 14,
  "live_envelope_substring_hits_on_16_refusals": {
    "Analysis input is invalid. Check the arguments and try again.": {
      "hit_count_of_16": 13,
      "missed_ids": [
        "r-compressed-flag",
        "r-over-1mib",
        "r-inflate-ratio"
      ]
    },
    "Selected artifact /fast/scratch/hyaku/kaidoku-r30/mutants/": {
      "hit_count_of_16": 15,
      "missed_ids": [
        "r-compressed-flag"
      ]
    },
    "inspect_rust_binary": {
      "hit_count_of_16": 16,
      "missed_ids": []
    },
    "Dependency": {
      "hit_count_of_16": 13,
      "missed_ids": [
        "r-compressed-flag",
        "r-two-sections",
        "r-inflate-ratio"
      ]
    }
  }
}
```
`c2-selftest.stdout.txt` last line: `selftest cases=16 failures=0` (exit **0**).

### E3 — Artifact and source digest verification

Producing command:
```sh
timeout 20 sha256sum /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/audit_c2_after.py /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/audit_c2_after.json /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/noncode_predictors_after.py /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/noncode_predictors_after.json /fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/c2-selftest.stdout.txt /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/PARSING.md /fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/cargo-auditable.schema.json && date -u +%Y-%m-%dT%H:%M:%SZ
```
UTC: `2026-10-23T03:18:13Z`. Exit code: **0**.

---

## Opened primary-source ledger

All sources were opened by ordinary local file reads on **2026-10-23** (no browser, captcha, or access-control bypass). Every quote is at most 25 contiguous words with its line number.

| URL | Access date | SHA-256 | Located quote (≤25 words) |
|---|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/AXES.md` | 2026-10-23 | `04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993` | line 11: `Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json` | 2026-10-23 | `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a` | line 29: `for a predicted refusal, the envelope is not ok and the frozen message appears verbatim in the run's stdout or stderr;` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv` | 2026-10-23 | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | line 5: `r-empty	refuse	Dependency section is not file-backed` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/runs.tsv` | 2026-10-23 | `d686623aeb147916bb1396dd8320281729a141c95559da60dddfd8cb11718262` | line 2: `g-relocated	2026-10-23T03:00:36+00:00	2026-10-23T03:00:40+00:00	0` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` | 2026-10-23 | `bb0518484e01386116d00fa9415fb129368ca0ef6bc68ba8acf2e11c1f6be4a3` | line 50: `Several mutants share a message (r-empty/r-nobits; r-not-zlib/r-trailing-bytes; r-extra-field/r-kind-dev), so a match does not prove which branch fired` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/SKILL.md` | 2026-10-23 | `7cbc725b8f7907e90e7bd23a639309d81f20c464bbd45c97b7f9679d3b3635b4` | line 968: `Read error.details.issues as well as error.message: for invalid_request refusals the message field is generic.` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md` | 2026-10-23 | `f81ff4e109174beba9e636490384c6f49ffbaf25b31cddd400d5ff32fb29722c` | line 96: `The inspect_rust_binary reader's Rust dependency-section gates, input/section/inflate/output/nesting limits, schema/root/index checks and refusal messages; not observed REA outcomes` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py` | 2026-10-23 | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` | line 205: `if not message or (message not in out_text and message not in err_text):` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/CriticAxisFitC2.md` | 2026-10-23 | `281d6fab30705401fdc67b80da0c77c4ffb1405660604d0c75a6720ff1b34d13` | line 7: `FIT as a proposed depth move; the four requested shallow predictors cannot reach 19/19 under the frozen P2 requirements.` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/CtlC2Sequence.md` | 2026-10-23 | `de1148a5b01cb11ecc5c7a94ec075fd76037b71d44d3902dad7d6ecd5bd0d94e` | line 5: `Observation — attack verdict: holds for these seven controls. None met the frozen target.` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/RevSelftestLookalikes.md` | 2026-10-23 | `ccba50bcaf1f4bde5e9dab3e8b321248f300f61d0e4a8082d44becc30c50314c` | line 215: `predictions.tsv reuses identical frozen messages across mutants built through different code paths` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/RevPredRefuseA.md` | 2026-10-23 | `31cc15916f104432138a1239744e56387610ec210a2ec4434db9793a83f3635f` | line 94: `None. All eight predictions agree: message text verbatim, failure class` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/RevPredRefuseB.md` | 2026-10-23 | `272e5d21761aefe26e03d921f864c4cb2f7d7ee5c4e10061348df82fd6fc7d34` | line 11: `## Verdict: all 11 predictions AGREE with the code` |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/after/c2-rust-refusals-at-92b1dd2d.txt` | 2026-10-23 | `2a1251738e041caf52154b63ee6a82318737c36a67b50fcbbdf380fb154622b6` | line 21: `mutants=19 matches=19 target=19 entry_ok=1 (ok) skill_ok=1 (ok)` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustAuditableReader.js` | 2026-10-23 | `1f3748c9ed6d04721a9bef364195e5d9b3d86794088c8594a366a9fb97fd6505` | line 79: `const maximum = Math.min(RUST_UNCOMPRESSED_BYTES, bytes.length * RUST_INFLATE_RATIO);` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/rust/RustBinaryImage.js` | 2026-10-23 | `08adaa596386428c84c2a8faa5d9e7b80199c14e5650ebd9fca41acd236ea681` | line 53: `throw new RustAuditableFormatFailure("malformed", "Dependency section is not file-backed");` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/go/GoElfImage.js` | 2026-10-23 | `ee88b9cd54763d7106068d4ba4055eac8f6c57218bc34aaed5dc9eecaa483204` | line 186: `const range = type === SHT_NOBITS ? { ...declared, file_backed: false } : declared;` |
| `file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/go/GoBinaryContainer.js` | 2026-10-23 | `2db56f9285c349dff9c9ac807a2e2bd1ddc468acd18f17f2e22456b3e52788b2` | line 80: `file_backed: size > 0n,` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/PARSING.md` | 2026-10-23 | `39e35b885ce178d748a0ca301951734489fe6dc64ea60add426e8ebde008de7e` | line 48: `1. Zero root packages` |
| `file:///fast/scratch/hyaku/kaidoku-r30/seats/w1/SrcCargoAuditable/cargo-auditable.schema.json` | 2026-10-23 | `c6ac9399d04d50d758b5c7f7bc7f03e89cf8af2d880856964a2ac52f6606ea15` | line 63: `"description": "Whether this is the root package in the dependency tree. There should only be one root package.` |

*(All 19 committed envelope JSON and `.stderr` SHA-256 digests are recorded in `/fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/audit_c2_after.json`; notable pair digests: `r-empty.json` `7ee87d4570b4ce8fc9f8bd5a480a7a8858b1f4c158be75b450b6aa1542396003`, `r-nobits.json` `42667a42c5742ca81c2df6f4074d60fa7b8ef65a5064b4b605c4e2445779209f`, `r-not-zlib.json` `0651cf13972c3c835390427b35714fb4e7c33de7785966c81d483ff2b8fd77bc`, `r-trailing-bytes.json` `458c3ec5f2c0bf4e3a76fc0fb414d987e305fb83b64234aa15780286333ff46f`, `r-extra-field.json` `0d63474d6658ef5a89811b3bc5be98a5dc0877ecdb8b9756fd0b0141763d4a5a`, `r-kind-dev.json` `6715c10c216e9ebaa87e7f93a326f377b45a730c18da518116ec2aa0497ac411`.)*

---

## Scratch artifacts

All scratch files written by this seat live under `/fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/`:

- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/audit_c2_after.py` — `768408b7990b64d80311436bc280cd68388844281e3660a7c496021e4fbdc141`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/audit_c2_after.json` — `5a966da20c61236662fb9a58dd5196d28da74b30dd76429b2a42b651686e7801`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/noncode_predictors_after.py` — `df1c823aad90982215c7483bda9f7df7d3fec984fddefa04ecf5a416b40db918`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/noncode_predictors_after.json` — `2116da536ff1d3040bdf2cee7b4b6c29716102efe8ee8dc12c11bdf272d3c248`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w2/CriticAxisC2After/c2-selftest.stdout.txt` — `fa6330a447c67b5b31285e56adb811ed5a833ae42941bc2278cafd7b10d16573`

Tool installs/updates: **none**. No REA CLI or MCP call was run; no carrier or mutant was executed or modified; no Git/jj write was performed; no child process remains running.

Report: .ufo/waves/round-30/w2/CriticAxisC2After.md
