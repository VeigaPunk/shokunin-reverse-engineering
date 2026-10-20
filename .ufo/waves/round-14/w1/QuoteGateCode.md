# QuoteGateCode — C2 quote-location gate implementation (round 14, w1)

Seat: `KaidokuR14.QuoteGateCode`, leaf executor. Access date: **2026-10-20** (UTC; fixtures re-checked after they landed).
Axes: **calibration** (does each exit/finding mean what C2 claims) and **coverage** (S017 splice, S018 mislocation, corrected contiguous cases, custody branches).

**Status: implemented, read back line by line, NOT executed.** No build, lint, formatter, smoke run, `--selftest`, manifest run, or frozen run was performed by this seat. Nothing below is an observed gate result; the design targets are derived from source bytes and the written code. L1 owns the single post-integration verification.

## Deliverable

| Item | Value |
|---|---|
| File | `.ufo/waves/round-14/tools/quote-fidelity.py` |
| SHA-256 | `0d939e231d73e02fab8898cd0f79f65ea2f6811e9300884c7e694992e19866d8` |
| Size / mode / lines | 35,910 bytes / 755 / 836 |
| Files under `round-14/tools/` | 1 (no `__pycache__`, no `.pyc`) |
| Imports | `argparse hashlib html json os re stat sys tempfile` (stdlib only); `subprocess` is imported inside the self-test observer only |
| Network / subprocess / eval / pickle | Normal modes: none. `--selftest` spawns this CLI with an argv list, no shell; it is the only subprocess path. |
| Normal-entry writes | none (stdout only); self-test writes only inside `TemporaryDirectory(dir=/var/tmp)` |

I wrote no fixtures, manifests, expected files, shared files, LOG, SCORECARD, corpus, SKILL, or fleet files. The fixture producer owns fixtures; it landed 7 manifests, 2 sources, and `expected.json` under `.ufo/waves/round-14/fixtures/`. I statically checked those bytes against the implemented schema, pins, selectors, and precedence (section below); this was not a gate run.

## Implemented interface

Mutually exclusive, one required: `--manifest PATH`, `--frozen EXPECTED`, `--selftest`.

Exit contract: **0** clean, **1** failed, **2** could-not-evaluate. Any CNE finding dominates; otherwise any finding is 1. A top-level `except Exception` prints `invalid_manifest ident=gate detail=internal:<Type>` and returns 2, so a crash cannot masquerade as exit 1. argparse usage errors already exit 2.

Output grammar (deterministic, no source text echoed):

```
QUOTE_FIDELITY: <finding> ident=<id> <detail>
QUOTE_FIDELITY_MANIFEST: <abs path>
QUOTE_FIDELITY_VERDICT: <label> quotes=<n> findings=<n> exit=<n>
QUOTE_FIDELITY_FROZEN: <abs path>
QUOTE_FIDELITY_PIN: manifest=<rel> expected=exit:<n>,ids:<list> actual=exit:<n>,ids:<list> <match|mismatch>
QUOTE_FIDELITY_VERDICT: <label> mode=frozen manifests=<n> findings=<n> exit=<n>
SELFTEST_CASE: <CLEAN|FAILED> case=<name> exit=<n> expected=<n> ids=<list>
QUOTE_FIDELITY_SELFTEST: <CLEAN|FAILED> cases=<n> passed=<n> failed=<n> exit=<n>
```

Stable per-instance ids are `<finding>@<ident>`, where ident is a quote id, source id, pinned relative path, `manifest`, `frozen`, or `gate`.

## Per-quote precedence (one finding maximum)

| # | Condition | Finding | Exit |
|---|---|---|---|
| 1 | `len(quote.split()) > 25` | `quote_too_long` | 1 (stops; no location check) |
| 2 | Quote is not a case-sensitive substring of the whole source | `quote_not_contiguous` | 1 |
| 3 | Declared selector matches more than one heading | `invalid_manifest` | 2 |
| 4 | Declared selector matches no heading | `quote_location_mismatch` | 1 |
| 5 | Quote not inside the matched heading body | `quote_location_mismatch` | 1 |
| 6 | Otherwise | pass | — |

Manifest/digest failures abort before any quote is graded. This makes the round-13 defects map as C2 claims: the S017 splice is absent everywhere → `quote_not_contiguous`; S018 under `Decompiled output` is present elsewhere → `quote_location_mismatch`; a missing section is a location error, not exit 2.

## Section and quote grammar

- **Markdown ATX**: line starts at column 0 with 1–6 `#`, one or more spaces/tabs, then text. Selector is the literal line with trailing whitespace/CR removed, including `#` (e.g. `## Usage`). Exact equality, so `## Usage` does **not** match `## Basic Usage`.
- **HTML h1..h6**: a single line `<hN attrs>inner</hN>` (case-insensitive; attributes may not contain `>`). Two exact selectors per heading: (a) visible label — inline tags removed, entities unescaped, whitespace collapsed (`Introduction`); (b) literal trimmed element line including attributes (`<h1 class="wp-block-heading">Introduction</h1>`). This accepts both the label form I sent the fixture producer and the literal-token form in ReviewS017's red table.
- **Body**: text after the heading line to the next heading (Markdown or HTML) with level `<=` the declared level, or EOF. Deeper headings stay inside; parent scopes are accepted by design (L1 kept same/higher hierarchy).
- **Fences**: ATX-looking lines inside ``` or ~~~ fences are ignored. HTML `<pre>` blocks are not special-cased (documented limit).
- **Quote match**: raw, case-sensitive `in` on the body. No whitespace, tag, entity, case, or punctuation normalization. A visible sentence interrupted by inline tags is unsupported and must not be quoted (L1 steer; AttackQuoteGate A1 accepted as a stated limitation, not rendered-text normalization).

## Manifest validation and custody

- Manifest opened once with `O_RDONLY|O_NONBLOCK`; `fstat` must be a regular file (a FIFO or device is rejected before any read); strict UTF-8; parsed with `object_pairs_hook` rejecting duplicate JSON keys at any depth.
- `sources` non-empty object; `quotes` non-empty array (anti-vacuity); non-empty string fields; duplicate quote ids rejected; unknown source references rejected.
- Digests are 64 hex chars; source paths non-empty, relative, and `realpath`-confined with `commonpath` under the manifest directory (absolute paths, `..` escapes, and symlinks resolving outside are `invalid_manifest`).
- Every declared source (including one no quote uses) is read once, hashed over the exact bytes, and compared **before any quote is graded**. Mismatch → `source_tampered` (2). Only then strict UTF-8 decode; failure → `invalid_manifest` (2). Missing/unreadable/non-regular → `invalid_manifest` (2).
- No second read: hash and decode use the same byte buffer.

## `--frozen` (parent-directed gate standard)

```json
{"manifests":[{"path":"REL","sha256":"HEX64","exit":0,"findings":["quote_not_contiguous@Q-ID"]}],
 "sources":[{"path":"REL","sha256":"HEX64"}]}
```

- Paths are relative to the expected file and use the same confinement; duplicate pinned paths are `invalid_manifest`.
- Preflight hashes **every** pinned manifest and source before any evaluation. Missing, unreadable, or mismatched bytes → `snapshot_tampered`, exit 2, nothing graded.
- Inventory coverage: every source a pinned manifest references must itself be pinned in `sources`, matched by resolved path. A gap is `invalid_manifest` ident `frozen`, exit 2, before any verdict comparison. A structurally invalid pinned manifest is skipped here because it has no valid inventory; it still fails closed at its own pinned `invalid_manifest` verdict.
- Each manifest then runs; observed exit **and** the sorted `<finding>@<quote-id>` list must equal the pin exactly. Any difference → `expected_verdict_mismatch`, exit 1. Pinning exit alone is not supported, per AttackQuoteGate A7.1.
- A pinned could-not-evaluate manifest that reproduces its ids counts as a reproduced pin (overall exit 0); the base-mode manifest run still exits 2.
- Frozen-only ids: `snapshot_tampered` (2), `expected_verdict_mismatch` (1). Base mode uses the five original ids.

## Self-test inventory (28 cases, isolated, NOT run)

Scratch: `tempfile.TemporaryDirectory(dir=SELFTEST_ROOT, prefix=...)`, where `SELFTEST_ROOT = /var/tmp` unless `QUOTE_FIDELITY_SELFTEST_DIR` is set; cleanup by context manager. No repository writes, no network, no imports from the lane. Every case launches **this CLI** as `[sys.executable, "-I", <script>, "--manifest"|"--frozen", <path>]` and asserts the real return code plus the parsed stable `class@id` lines; no helper return values are checked.

| Case | Exit | Exact expected ids |
|---|---|---|
| markdown_clean | 0 | — |
| html_label_clean | 0 | — |
| html_attributes_clean | 0 | — |
| html_element_token_clean | 0 | — |
| fenced_pseudo_heading_ignored | 0 | — |
| word_limit_boundary (25 words) | 0 | — |
| splice_absent_everywhere | 1 | `quote_not_contiguous@q-splice` |
| quote_elsewhere | 1 | `quote_location_mismatch@q-loc` |
| section_absent | 1 | `quote_location_mismatch@q-sec` |
| heading_exact_not_substring | 1 | `quote_location_mismatch@q-exact` |
| quote_too_long (26 words) | 1 | `quote_too_long@q-long` |
| duplicate_heading | 2 | `invalid_manifest@q-dup` |
| source_tampered_precedes_quotes | 2 | `source_tampered@S1` |
| invalid_json | 2 | `invalid_manifest@manifest` |
| duplicate_quote_id | 2 | `invalid_manifest@manifest` |
| duplicate_source_key | 2 | `invalid_manifest@manifest` |
| source_missing | 2 | `invalid_manifest@S1` |
| source_not_utf8 | 2 | `invalid_manifest@S1` |
| source_not_regular (FIFO) | 2 | `invalid_manifest@S1` |
| path_escape | 2 | `invalid_manifest@manifest` |
| absolute_path | 2 | `invalid_manifest@manifest` |
| empty_quotes | 2 | `invalid_manifest@manifest` |
| frozen_reproduces_clean | 0 | — |
| frozen_verdict_mismatch | 1 | `expected_verdict_mismatch@manifest.json` |
| frozen_source_tampered | 2 | `snapshot_tampered@src/doc.md` |
| frozen_input_missing | 2 | `snapshot_tampered@absent.json` |
| frozen_missing_source_pin | 2 | `invalid_manifest@frozen` |
| frozen_invalid | 2 | `invalid_manifest@frozen` |

The `source_tampered_precedes_quotes` case also carries a spliced quote that must never be graded, pinning digest-before-quote precedence. The `fenced_pseudo_heading_ignored` case fails as `quote_location_mismatch` if a `# pseudo heading` line ends the span. The `heading_exact_not_substring` case uses `## Basic Usage` against selector `## Usage`. `frozen_missing_source_pin` omits the referenced source from `sources` and must fail before any verdict comparison.

## Landed fixtures — static compatibility check (NOT a gate run)

The fixture producer landed 7 manifests, 2 source excerpts, and `expected.json` under `.ufo/waves/round-14/fixtures/`. I re-read the JSON and bytes; I did **not** execute the gate against them.

| Check | Result |
|---|---|
| `expected.json` shape | `manifests[]` (7) with `path/sha256/exit/findings`; `sources[]` (2) with `path/sha256`; all paths relative |
| Manifest shape | `sources` map (1 entry each; 2 in `manifest-corrected.json`), `quotes` array (1–2), all fields non-empty, quote ids unique per file |
| Digest pins | All 7 manifest SHA-256 and both source SHA-256 recomputed with `sha256sum`; every value equals its `expected.json` pin |
| Source pins | Both source digests equal the pinned values in `expected.json`; every manifest-referenced source is present in `expected.json.sources`, satisfying the new inventory-coverage rule |
| Selectors | Visible labels only: `Command-Line Arguments`, `Deterministic Function Names and Mapping CSV`, `Introduction`, `Decompiled output`; each occurs exactly once per excerpt |
| S017 placement | Corrected sentence at line 23 inside `Command-Line Arguments` (h3 line 3; next h3 line 49); absent from the `Deterministic…` body (h3 line 64; next h3 line 91); splice absent from the whole excerpt |
| S018 placement | Quote at line 3 inside `Introduction` (h1 line 1; next h1 line 5); absent from `Decompiled output` (h1 line 11; next h1 line 17) |
| Heading skeleton | HTML h1–h3 only; no ATX lines, no ```/~~~ fences, no duplicate labels; S018 keeps every intermediate h1 with labelled elision comments |
| Expected verdicts | Pins 1/1/0/1/1/0/0 with IDs `quote_not_contiguous@S017-Q1` (twice), `quote_location_mismatch@S017-Q1`, `quote_location_mismatch@S018-Q1`, and clean pairs; consistent with the implemented precedence on the checked bytes |

Limit: this table proves the frozen inputs are admissible and byte-consistent with their pins. It is not a gate verdict and does not show the gate executes correctly; L1's `--frozen` run is the first execution.

## Evidence opened

All opens 2026-10-20 (UTC). Quotes are contiguous and ≤25 whitespace words.

| Source and location | Quote | Note |
|---|---|---|
| `corpus/lessons/round-13-verifier-spotcheck.md:13` (sha256 `1f64a497e2252339652cbabdae669a3dc44c1a0e84992d01272baf932e168bbd`) | “Review found S017's spliced quotation and S018's mislocated exact quote.” | The two defects C2 must catch. |
| `corpus/lessons/round-13.md:63` (sha256 `b2ae45a87e574a25a0ba1505014b9909d3b3dd1a3741db01e20a9a260994ffb3`) | “These append-only corrections supersede the S017 quote and S018 location printed in the original Gate table.” | Correction semantics; rows 65–66 give the corrected S017 and S018 locations. |
| `corpus/lessons/round-13.md:65` | “Replace address-derived function identifiers with deterministic names based on parse order.” | Corrected S017 sentence; location `Usage` → `Command-Line Arguments` → `--normalize` row. |
| `w1/ReviewS017-source/View8-README-ef39099b4f5076042173f9113382ebeb0630a56d.md` (opened while present; **removed by its author before this report**) | “Replace address-derived function identifiers with deterministic names based on parse order.” | Raw line 40; line 18 `<h2>Usage</h2>`, line 20 `<h3>Command-Line Arguments</h3>`, next h3 line 66 `Basic Usage`, line 81 `Deterministic Function Names and Mapping CSV`, line 82 tag-interrupted sentence. Peer-reported sha256 `191621cd…1619b`; I did not re-hash it before removal. |
| `w1/s018-raw.html` (opened while present; **removed by its author before this report**) | “The goal is not perfect source recovery — V8 compilation is lossy, and the output of decompilation remains pseudocode.” | Raw line 489 inside h1 `Introduction` (line 469); next h1 `Distributed payloads` line 497; wrong anchor `Decompiled output` line 625. Peer-reported sha256 `31b82315…74dd5e`; not re-hashed by me. |
| `.ufo/waves/round-14/spec.json` `context` “Gate interface” | “0 clean,1 failed (quote_not_contiguous,quote_location_mismatch,quote_too_long),2 could-not-evaluate (source_tampered,invalid_manifest)” | Base exit/ID contract. |
| `.ufo/waves/round-14/claims.json` C2 (sha256 `d10234d3e81ad48375d22caf22d46f3d6a9893cf718d8682a3a78052a1be7350`) | “quote-location fidelity gate plus grounded QUALITY criterion rejecting S017 splice and S018 mislocation while admitting corrected contiguous located quotes” | C2 observable and stated local-excerpt limit. |
| `corpus/SOURCES.md:23` (S017 row) | “README-stated V8 disassembler versions, normalization behavior, and serialized-input warning” | Registry anchor; does not name the corrected quote's section. |
| `w1/ReviewQuoteContract.md` proposed correction 1 | “Not a byte substring of the whole source → quote_not_contiguous.” | Precedence adopted; duplicate-heading and missing-section rules adopted. |
| `w1/AttackQuoteGate.md` A7.1 | “Pin the full sorted list of (quote id, finding id) plus exit, per frozen manifest.” | Frozen format pins pairs, not exit alone. |
| `w1/GateInputSafety.md` F5 | “Open each input exactly once in "rb".” | Single-read nonblocking hash/decode and regular-file check adopted. |
| `.ufo/waves/round-14/dispatch.json` QuoteSourceFixtures target | “Create source files + manifests red-before (original S017 splice and S018 wrong heading if opened), corrected manifest and expected.json” | Fixture producer's owned scope. |

Also read: `w1/ReviewS017.md`, `w1/ReviewS018.md`, and `/home/vgpnk/.omp/agent/RULES.md` (tooling policy). No REA diagnostics, target execution, network fetches, or client edits were performed by this seat.

## Limitations

- **Not executed.** The gate, `--selftest`, and frozen mode were not run; no exit code or finding line is observed. Syntax rests on line-by-line read-back. L1 must run `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --selftest` and the frozen inputs once.
- **Raw-bytes matching only.** A verbatim visible sentence interrupted by inline markup (e.g. `Use <code>--normalize</code> to …`) is unsupported; the fixture producer must quote raw-contiguous text. This is the L1-accepted limitation and avoids silent normalization ambiguity.
- **HTML headings must be single-line** and may not carry `>` inside attributes; multi-line elements are not parsed. Backtick/tilde fences are handled; `<pre>`-embedded pseudo-headings are not.
- **Coarse parent scopes.** Same/higher-level hierarchy means a quote in a descendant subsection passes when the manifest names the ancestor; this was L1's explicit choice. Keeping every intermediate heading in excerpts is a fixture rule the gate cannot enforce.
- **Duplicate-heading precedence.** Whole-source absence is checked first, so a quote absent everywhere reports `quote_not_contiguous` even if its named heading is duplicated. A present quote naming a duplicated selector reports `invalid_manifest` (2).
- **Self-consistency, not authenticity.** `source_tampered` means excerpt bytes differ from the manifest pin; a coordinated excerpt+manifest rewrite passes. The independent anchor is the frozen digest pin plus L1's registration. The gate proves local quote-location consistency only, not semantic truth, live-page fidelity, or held REA behavior.
- **Frozen inventory is now covered, not closed.** Every source a pinned manifest references must itself be pinned in `expected.json.sources` (fail-closed, `invalid_manifest@frozen`); extra unreferenced pins are allowed, and the gate does not prove the fixture producer listed every file they intended.
- **Anti-vacuity rule.** Empty `sources` or `quotes` is `invalid_manifest`; this is an interface decision beyond the original four quote IDs, chosen so a manifest that grades nothing cannot report clean.
- **Extra frozen ids.** `snapshot_tampered` and `expected_verdict_mismatch` are parent-directed additions for `--frozen`; base mode remains the five original ids.
- **Word count** is `str.split()`, so the standalone em dash in the S018 quote counts as a token (19 words). No punctuation stripping is applied anywhere.
- The two capture files cited above were present during this session and removed by their author before report writing; their line citations are from my live open, and their hashes are peer-reported, not re-derived by me at report time.

## Risks and integration checklist for L1

1. Run `--selftest`; design target is `QUOTE_FIDELITY_SELFTEST: CLEAN cases=28 passed=28 failed=0 exit=0` (unobserved). It launches the CLI 28 times, including malformed/unreadable inputs that must exit 2 and a FIFO source that must not block.
2. Run the S017 red-before manifest (splice under `Deterministic Function Names and Mapping CSV`): design target exit 1, `quote_not_contiguous@<id>`.
3. Run the S017 corrected manifest under `Command-Line Arguments` (label or literal `<h3>…</h3>` token): design target exit 0.
4. Run the S018 corrected manifest under `Introduction`: exit 0; the same quote under `Decompiled output`: exit 1, `quote_location_mismatch`.
5. Run `--frozen` with `expected.json` pinned over gate inputs; expect 0 on reproduction, 1 on pin drift, 2 on byte drift. Pin the gate script digest externally; the gate cannot self-authenticate.
6. Do not treat a green `--selftest` as C2 evidence; only the frozen S017/S018 run with digest-pinned inputs supports the observable.
7. `--selftest` needs `/var/tmp` writable (or `QUOTE_FIDELITY_SELFTEST_DIR`); failure exits 2 via the catch-all, never 1.

**Blockers:** none for this seat. The landed fixtures are statically admissible under the frozen schema and pins; the remaining unobserved step is L1's single execution of `--selftest` and the frozen run. No scope widening was taken.

## Tool installs / updates

None. No package manager, `uv`, binary download, or upgrade was used or needed.
