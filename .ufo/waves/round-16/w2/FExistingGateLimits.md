# FExistingGateLimits — round 16, wave 2 (source-read attack)

Seat: `KaidokuR16.FExistingGateLimits` (leaf critic, no delegation).
Scope: C2 artifacts only — quote-fidelity supplemental baseline discoverability, unchanged script/baselines, manual-only rule — plus `controls.py` frozen-baseline logic and the red-before control.
Access date: 2026-10-20. Baseline revision: `6235498b4112350eebce0812a74af1781fc0ee88`.

## Method and limits

- Read: `corpus/QUALITY.md:9-28`, `SKILL.md:438-452`, `.ufo/waves/round-15/boundary-fixtures/{expected,raw-accepted,rendered-rejected}.json` and `raw-source.md`, `.ufo/waves/round-14/tools/quote-fidelity.py` (usage, `scan_headings`, `evaluate_frozen`, selftest case list), `.ufo/waves/round-16/controls.py`, `.ufo/waves/round-16/documentation-red.json`, `corpus/lessons/round-15-verifier-spotcheck.md:181-188`, `corpus/lessons/round-16.md`.
- Read-only git inspection only (`status --short`, `diff --stat`, `diff -U0` on two files, `log`, `rev-parse`). No selftest, no `--frozen` run, no `controls.py` run, no hashing, no build or lint.
- Consequently every pinned SHA-256 in `expected.json` is **unverified by this seat**. Nothing here is a gate result.
- Tools installed or updated: none.

## Verified no-finding (source-read)

1. **Supplemental discoverability is present.** `SKILL.md:450` (quote-fidelity row, pinned-values cell) names `.ufo/waves/round-15/boundary-fixtures/expected.json`. The file exists and is the frozen expectation for `raw-accepted.json` (exit 0) and `rendered-rejected.json` (exit 1, `quote_not_contiguous@raw-literal`). The `raw-source.md` source it pins is referenced by both manifests. This satisfies the route-2 request as written in `round-15-verifier-spotcheck.md:186`.
2. **Frozen coverage of the supplemental directory is complete for its current contents.** The `boundary-fixtures/` directory holds four files: `expected.json` (self-pin is impossible, as for every frozen expectation), two manifests (both pinned under `manifests`), and one source (pinned under `sources`). The `quote-fidelity.py:368-381` check that every manifest-referenced source is pinned passes on the file structure I read (`"path"`/`"sha256"` keys match the shape in the usage block, lines 47-54).
3. **QUALITY is append-only for this round.** `git diff -U0 -- corpus/QUALITY.md` shows one hunk, `@@ -27,0 +28 @@`: row 18 added. Rows 1-17 are byte-unchanged relative to HEAD.
4. **Frozen baselines and the quote script are unchanged in the worktree.** `git status --short` over `.ufo/waves/round-14`, `.ufo/waves/round-15`, `evidence/round-1-2026-10-15`, `corpus/lessons`, and `corpus/knowledge` shows no modified or untracked entries. `quote-fidelity.py` has no diff. The only `corpus/knowledge` edits are appends to the r14-02 and r15 knowledge files, and `LOG.md`; `git diff --stat` over those reports 83 insertions and 0 deletions.
5. **Row 17 citations resolve.** `corpus/lessons/round-15.md` exists and has `## Gate` and `## Mistakes` sections. `corpus/lessons/round-14-verifier-spotcheck.md:172` holds the routed manual-only item that row 17 cites.
6. **Row 18 citations resolve.** `round-15-verifier-spotcheck.md:181-188` contains the four routed duties. `documentation-red.json` exists. `corpus/lessons/round-16.md` exists (untracked; L1 integration only).

## Findings

Severity is calibration-weighted. None blocks the round-15 route itself.

### F1 — Medium-low (calibration): universal discoverability claim has one mechanical check on one path

- Claim: `corpus/QUALITY.md:28` (row 18): "Every supplemental frozen baseline is discoverable from its existing gate registry row."
- Enforcement: `documentation-red.json:6` runs one substring test, `'.ufo/waves/round-15/boundary-fixtures/expected.json' in row`. That test covers one path. Nothing enumerates supplemental frozen baselines. `controls.py:35-39` lists `FROZEN_PREFIXES` but reports only byte stability, never registry discoverability.
- Consequence: the universal "every" is backed by one substring. A later supplemental baseline with no registry row would not fail any artifact. For round 16 I found no counterexample among the baselines I read: round-15 `inventory.json` (go-snapshot-inventory row, `SKILL.md:487`), round-16 `selection-fixtures.json` / `negative-fixtures.json` (go-selection-preview row, `SKILL.md` round-16 section), and the round-14 and round-15 boundary expectations (`SKILL.md:450`). I did not mechanically enumerate every frozen-named file in the round-14/15 directories.
- Recommendation for L1: either narrow row 18 to the named route ("the round-15 boundary-fixtures baseline is discoverable from the quote-fidelity row"), or record the enumeration explicitly as bounded to the files listed above.

### F2 — Low (coverage): `frozen_report` cannot see files added under frozen prefixes

- `controls.py:197-203` builds `paths` only from `before.blobs`. A file added under `.ufo/waves/round-14/` or `.ufo/waves/round-15/` at AFTER is never reported. The per-path check (`controls.py:8-12`) is accurate as far as it goes, but the summary key `frozen_baselines` reads as directory-level.
- Current effect: none. `git status` shows no added or modified files under those directories.
- Fix: also list AFTER blobs under the same prefixes and report `added` paths, or report the key-set delta.

### F3 — Low (consistency): absent-at-before LOG.md aborts instead of reporting

- `prefix_report` (`controls.py:153-166`) calls `before.get(path)` at line 154 before any existence check. `Rev.get` (`controls.py:91-100`) runs `git show` and calls `fail()` on a missing path, producing exit 2 with no JSON. `unchanged_report` (lines 172-173) handles the identical case explicitly as `absent_at_before`.
- The docstring (`controls.py:16-17`) counts "missing structural anchor" as exit 2, so the abort can be defended. It is still inconsistent with the sibling helper and with `prefix_report`'s own `missing_at_after` branch.
- Current effect: none (`LOG.md` exists at HEAD).

### F4 — Low-medium (calibration): gate accepts rendered-derived section locators that the manual-only rule forbids for quotes

- `quote-fidelity.py:233` computes HTML heading selectors with `html.unescape(re.sub(r"<[^>]*>", "", ...))`, so entity-decoded, tag-stripped visible labels are valid `section` values (docstring `:26-29`).
- `corpus/QUALITY.md:26` (row 16) forbids "reuse a locator from a different rendering". Row 17 (`:27`) excludes "text obtained by rendering markup or character references" from machine grading. Row 17 does not say whether section locators fall under that exclusion. The gate therefore grades a rendered-form locator as clean without that being stated in any row.
- Selftest gap: the HTML section cases at `quote-fidelity.py:570-582` cover plain labels, attribute-stripped labels, and the literal element token. No case exercises an entity (for example `&amp;`) and no case rejects a rendered-form locator. The `html.unescape` branch is untested while the docstring documents it.
- Recommendation: decide whether section locators are inside #17's exclusion; if yes, add a selftest for entity labels and an explicit note in the SKILL row; if no, say so in #17.

### F5 — Low-medium (calibration): frozen "clean" for the rendered control can be misread as rejection capability

- `rendered-rejected.json` quotes `Use raw bytes.` against source `Use <em>raw</em> bytes.` (`raw-source.md:3`). Its pinned expectation is exit 1 (`expected.json:9-16`). `QUALITY.md:27` says the verdict on a rendered submission "is void for the manual-only claim".
- The round-15 frozen run will print `clean mode=frozen manifests=2 findings=0 exit=0` (`round-15-verifier-spotcheck.md:133`), which reads as a pass. That pass verifies only that the pinned control still produces the pinned exit 1.
- The SKILL row (`SKILL.md:450`) does say "Manual-only submissions are excluded by QUALITY #17 ... any machine verdict on such a claim is void", but in the same cell as the frozen-run pointer, so the caveat is not adjacent to the command.
- Recommendation: L1's closure text should state that the rendered control's pinned exit 1 is a limitation observation, not gate capability. Do not cite the frozen clean line as rendered-quote rejection evidence.

### F6 — Low (discoverability): supplemental frozen run has no literal invocation

- `SKILL.md:450` says the supplemental controls "run with the same script's `--frozen` flag". The primary command is literal; the supplemental one is not. A reader must compose `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --frozen .ufo/waves/round-15/boundary-fixtures/expected.json`.
- The route asked only for a reference, so this is below the bar of a defect. It does weaken reproducibility of the supplemental verdict relative to the primary one, and row 18's "discoverable" claim is satisfied only at path level.

### F7 — Low (marker weakness, adjacent to route 3): red-before "producing_command_retained" check is trivially satisfiable

- `documentation-red.json:6` evaluates `producing_command_retained` as `bool(co) and 'argv' in co`, where `co` is `controls.py`. `controls.py` itself calls `sys.argv` at lines 247-249 and 282-283, and the word "argv" appears throughout its docstring and invocation block. Any Python file that reads argv passes this check.
- The baseline result (`documentation-red.json:11`) is `false` only because `controls.py` is absent at `6235498`. Post-integration it will pass regardless of whether a command record is retained.
- The round-16 lesson already labels the red control marker-only (`corpus/lessons/round-16.md:61`), so this is a disclosed weakness. It still means QUALITY #18's "retains the producer" clause is backed by a presence test that cannot fail once the file exists.

## Residual risk and verification gaps (for L1, not run by this seat)

- Every SHA-256 pinned in `.ufo/waves/round-15/boundary-fixtures/expected.json` is unverified here. L1 must run `python3 -I .ufo/waves/round-14/tools/quote-fidelity.py --frozen .ufo/waves/round-15/boundary-fixtures/expected.json` once and compare to the expected `clean mode=frozen manifests=2 findings=0 exit=0`.
- The entity-decoding branch (F4) has no selftest coverage; a green selftest does not exercise it.
- `controls.py` has not been executed on the round-16 tree. F2/F3 are source-read observations only.
- The documentation red check was run once at baseline and returned 0/4 (`documentation-red.json:11`). The post-integration rerun is L1's.
