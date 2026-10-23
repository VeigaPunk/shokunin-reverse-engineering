# R30-C2 — depth-axis fit and cheap-predictor attack

Seat: KaidokuR30.CriticAxisFitC2. Access date: 2026-10-23.

## Scoped verdict

**FIT as a proposed depth move; the four requested shallow predictors cannot reach 19/19 under the frozen P2 requirements. Attack verdict: holds, with the qualifications below.** This is an axis-fit review, not canonical adjudication, admission, or an empirical claim pass. Live P2 results remain **unknown**: this seat ran no REA command, counter, carrier, or mutant.

**Observation:** AXES defines depth as “Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources.” The frozen proposal names precisely those artifacts: a source-derived decision table, numerical limits, exact diagnostics, and source S090. This is depth, not additional container coverage. [E1; sources A–D]

**Inference:** the intended table is substantive if actually landed: a zlib-compressed payload is not the same condition as ELF's compressed-section flag; missing root is predicted acceptable while two roots are refused; and a package's kind and dependency index have specific validation rules. These distinctions are actionable, not an undifferentiated “malformed input” rule. The builder and prediction rows expose these distinctions before measurement. [E1; sources C–D]

## What the numbers mean

These are **paper expectations at P2's outcome/message-comparison layer**, not fabricated counter measurements. For the calculations, give the attacker all unrelated receipt/provenance prerequisites for free; it still misses the indicated cases. A standalone predictor is not a live REA invocation and supplies no qualifying committed evidence.

P2 does **not** count “refused” alone. For a frozen refusal, the exact nonempty frozen message must occur verbatim in stdout or stderr and the envelope must not be ok. For acceptance, an ok envelope, zero exit, correct operation and mutant SHA, nonempty oracle-equal package multiset, and correct section offset/size are required. The full target additionally requires committed receipts, entry_ok, and skill_ok. [sources B, D]

**Observation:** the frozen list has 19 rows: 16 refusals, 13 distinct refusal messages, and three acceptances: `g-relocated`, `g-recompressed`, `g-no-root`. Three messages occur twice; every other refusal message occurs once. [E1]

| Trivial predictor, explicitly defined | Expected matches out of 19 | Can meet 19/19? |
|---|---:|---|
| Always output only `refused`, without a frozen diagnostic | **0/19**. It gets 16 kinds right, but that is not P2. | No |
| Refuse every case with one ordinary generic message, e.g. `Invalid dependency metadata` | **0/19**. If generously upgraded to the best single exact error signature, **2/19**. A constant multi-signature blob is a stronger variant discussed below. | No |
| Refuse with a message copied from Rust command help: either its description or its path description | **0/19** | No |
| Refuse using the 18 lexically extracted Rust-looking strings in random order | **13/18 expected matches**, i.e. approximately **0.722/19**; not 13 successful cases. A raw, unfiltered random strings-line predictor is only **13/41181 ≈ 0.000316/19**. | No |

**Random-model definition:** the extracted catalog is deduplicated, with no interpretation of branch conditions. Uniform independent choices from its 18 entries give expectation 13/18. A uniformly shuffled catalog assigned to the first 18 frozen rows, followed by an empty diagnostic on the last row, has the same expectation: the final row is `r-index-outside`, which no literal catalog entry can match anyway. No random model can repair these predictors' three always-refused acceptance cases.

The literal catalog covers 13 refusal rows. It cannot spell the two `Dependency package 0 ...` cases or the `Dependency index 584 from package 0 ...` case: the bundle instead contains `${String(index)}` and `${String(outside)}` templates. The exact error text, not an approximate semantic resemblance, matters. [E1; source E, lines 5357 and 5408]

A still more charitable randomized baseline is handed all 16 fully instantiated frozen refusal messages, recognizes the `r-` labels, and merely shuffles the 16-message multiset over those rows. Its expected correct rows are

`(3 × 2² + 10 × 1²) / 16 = 22/16 = 11/8 = 1.375`,

again out of 19. Even its best permutation cannot match the three acceptances. This deliberately grants more information than plain strings extraction; it is not evidence of a successful predictor. [E1]

### Help limitation

REA `--help` was **not executed**. The concrete help-based predictor above uses the two statically registered strings:

- `Inspect an embedded cargo-auditable Rust dependency list without target execution`
- `Local ELF, PE or thin Mach-O image`

Neither contains any frozen refusal diagnostic. This proves 0 for that defined help-copying predictor, not a claim that this seat captured every byte of rendered global help. [E1; sources F and G]

## Strongest local counterexamples and qualifications

### 1. One constant message can game the refusal-only subscore

**Observation:** the refusal branch checks substring presence, not equality to one diagnostic: source D, lines 200–207. [E1, E2]

**Inference / paper counterexample:** emit one constant non-ok diagnostic blob containing the entire strings catalog on every case. It covers **13/19** message checks without associating a single message with a condition. Instantiate the two templates using values already exposed in the builder, or concatenate the frozen refusal messages themselves, and the same constant blob covers **16/19**. Ordering is irrelevant to substring membership. The ordinary generic-message score of 0, or the best single-signature score of 2, must not be represented as a bound on arbitrary fixed strings.

**Impacted axes:** depth (specificity of demonstrated understanding), calibration (do not call these diagnostic associations). **The full frozen target still holds against this attack** because all three valid variants require successful, identity- and metadata-bound acceptance records. This is not an observed counterfeit live REA run or a demonstrated full-counter bypass.

**Smallest safe correction:** retain all 19 cases and the frozen target. Do not present a refusal-only subtotal as depth verification; require the actual condition-to-signature table in the deliverable. No amendment of P2 is proposed.

### 2. Counter success alone does not enforce the promised SKILL table

**Observation:** source D, lines 273–277, makes skill_ok depend only on a new line containing `inspect-rust-binary` and the knowledge-entry path. Lines 258–270 check an entry source line and an S090 source row. They do not inspect decision-table structure, numerical thresholds, or whether a reader can act on SKILL alone. This is a static source observation, not an exercised counter control. [E1, E2]

**Inference / paper counterexample:** otherwise qualifying evidence plus one new link line satisfies that SKILL gate while omitting the promised table. Thus a future green counter line is necessary under the frozen contract but is not, by itself, proof that the AXES depth artifact exists.

**Impacted axes:** depth and calibration. This is **fixable deliverable under-enforcement**, not a reason to relabel the proposed technical work as coverage and not a demonstrated acceptable tradeoff.

**Smallest safe correction:** the L1 must land/review the actual SKILL condition/threshold/signature/source table, including the positive exceptions, rather than treating skill_ok as a semantic documentation review. Preserve the frozen instrument and report any frozen-target miss honestly.

### 3. This is not a blind predictor benchmark

**Observation:** both the frozen TSV and the builder publish every expected kind/message; source D, lines 123–167, hardcodes them. Copying that answer key yields **19/19 agreement with the answer key**, without reading REA code. [E1; sources C–D]

**Inference:** the stronger unqualified claim “no trivial predictor can reproduce the predictions” would be false. Copying predictions is not a P2 match: P2 requires fresh live REA behavior and qualifying retained evidence. Its purpose is to test a frozen code-derived table against behavior, not to measure hidden-label prediction accuracy or prove which cognitive method authored the table. Authorship provenance is not independently established by these paper controls.

**Impacted axes:** calibration and depth attribution. **Smallest safe correction:** describe the result, if later achieved, as a frozen source-derived table corroborated by 19 live cases; do not call it blind prediction or proof that code reading was necessary. No change to claim identity, route, predicate, or target is warranted by this review.

## Evidence receipts

### E1 — passive extraction and arithmetic

Producing command:

```text
timeout 60 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/predictors.py
```

UTC start/end: `2026-10-23T02:44:21+00:00`. Exit: **0**. Exact stdout excerpts:

```text
  "rows": 19,
  "refused": 16,
  "distinct_frozen_refusal_messages": 13,
  "always_refused_full_message_matches": 0,
  "always_refused_kind_only_matches_not_P2": 16,
  "best_single_exact_message_matches": 2,
  "help_full_message_matches": 0,
  "strings_catalog_count": 18,
  "strings_catalog_random_expected_matches_fraction": "13/18",
  "raw_strings_line_count": 41181,
  "raw_strings_random_expected_matches_fraction": "13/41181",
  "generous_exact_frozen_multiset_shuffle_expected_matches": "11/8",
  "all_literal_errors_same_blob_matches": 13,
  "all_frozen_errors_same_blob_matches": 16,
static_analysis_exit=0
```

The script's only spawned inspection command was:

```text
timeout 20 strings -a -n 4 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/cli.js
```

Exit: **0**, within the same UTC second. Full stdout/stderr retained below. It imported/executed neither REA nor the counter. It read the TSV, performed lexical string extraction, calculated expectations, and hashed the eight sources. For static source findings, the producing read operations were `functions.read` on sources A–G with the located ranges stated here; structured reads succeeded and have no process exit code. Source identity is independently recorded by E1/E2.

### E2 — source and artifact identity

Producing command:

```text
timeout 10 date -u +%Y-%m-%dT%H:%M:%SZ && timeout 20 sha256sum /fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/predictors.py /fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/analysis.json /fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/strings.stdout.txt /fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/strings.stderr.txt /fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/strings-catalog.json
```

UTC output: `2026-10-23T02:45:22Z`. Exit: **0**. Exact checksum output is reproduced by the artifact list below. Source hashes were also independently produced by `timeout 20 sha256sum` over sources A–D and G, then E/F/H, during the review; E1's JSON preserves all eight.

## Opened primary-source ledger

All sources were ordinary local file reads; access date **2026-10-23**. No HTTP fetch, access-control bypass, browser, or REA runtime was used. Each quote below is at most 25 contiguous words. Governing skill/operator instructions are not technical evidence sources.

| ID | URL | SHA-256 | Located quote |
|---|---|---|---|
| A | file:///home/vgpnk/Projects/shokunin/AXES.md | `04ea5c9e89c91cef645536ab56863ebb014dce617e7083e54968092968a7d993` | line 11: `Verifiable technical detail — decision tables with real thresholds, named error signatures, cited sources` |
| B | file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/claims.json | `65d94d3fbdf7469f8e100c87c96b1eaa6b93382e20521b0606be54b3db1e989a` | line 29: `the envelope is not ok and the frozen message appears verbatim in the run's stdout or stderr` |
| C | file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-30/c2/predictions.tsv | `6852df3ab8d5c98551f8768125fd3cb63d361e58868ff797ceb423c2f6c87315` | line 11: `Dependency section exceeds the 1 MiB compressed limit` |
| D | file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-30/c2-rust-refusals.py | `1c357fca7b00a8aa1a524d17b7cda50526a3aa49af87f07bb94a51f678857a6b` | line 276: `"inspect-rust-binary" in l and ENTRY in l` |
| E | file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli-runtime/cli.js | `168cd322a29c9baed02d7e44ab5ae9b2634b3f5b872ff5fcfa3bd20b718e2204` | line 5357: `Dependency package ${String(index)} does not match the package schema` |
| F | file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/cli/rustCommands.js | `feca585495e89647b64b08f361b24e9cc1f786da7077e20b9794708de148b766` | line 12: `Inspect an embedded cargo-auditable Rust dependency list without target execution` |
| G | file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json | `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c` | line 4: `"version": "6.5.0",` |
| H | file:///home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/scripts/rea.mjs | `526105418604cc6e5a202a6275b700814e27450bfaffd45e7510530ba669de8d` | line 44: `"dist/cli-runtime/cli.js",` |

Additional located source facts: E lines 5182–5186 declare the 1 MiB compressed cap, ratio 64, 8 MiB uncompressed cap, and depth 32; line 5240 uses the minimum of the uncompressed cap and 64 times compressed length. The proposal's quoted limits are genuine static implementation details; the 19 cases alone do not establish every exact boundary. C line 4 and D lines 125–128 predict acceptance after removing all roots. D lines 348–357 mandate the actual REA invocation before comparison; this review did not execute them.

## Scratch artifacts

All generated non-report files are confined to the assigned seat directory:

- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/predictors.py` — `5296706a39ad49bb49495debbd6e12a8b231393d70fdb390a0fb7191e63546f1`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/analysis.json` — `9f5393d7f4709523e2f0c617867419c1acb37ab663a247267f7ce018e10b4db7`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/strings.stdout.txt` — `d925be525c7004a588c3abd0058a1bd8dfd7b232a2a4e4df613304ea83c37c6f`
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/strings.stderr.txt` — `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty)
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/CriticAxisFitC2/strings-catalog.json` — `91cdf9318c1ade83dbe7a1f6dcf6bdc01e127c787c139add26af52bb76cf0491`

Tool installs/updates: **none**. Existing GNU strings reports GNU Binutils 2.47 (`timeout 10 strings --version`, exit 0, observed by `2026-10-23T02:43:08Z`). No agents spawned, lane/index changes, Git/JJ writes, or shared-mutant writes. All commands were bounded and completed; no started process remains.

Report: .ufo/waves/round-30/w1/CriticAxisFitC2.md
