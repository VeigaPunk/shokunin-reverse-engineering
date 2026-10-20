# Round-18 routed-defects format-only review

## Scope and evidence

**Observation:** `.ufo/waves/round-18/tools/routed-defects.py` is unchanged from the round-19 baseline `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (diff command below, exit 0). This is a review of its baseline behavior, not a newly introduced change.

**LSP:** no LSP device is mounted (`read xd://lsp` returned `No such tool`), so status/references/definition/diagnostics were unavailable. Literal grep was used only to locate candidate checks; conclusions below are from the cited source and selftest, not grep as semantic proof.

**Commands exercised:**

- `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 -- .ufo/waves/round-18/tools/routed-defects.py; rc=$?; printf 'exit_code=%s\n' "$rc"; exit "$rc"` — exit **0**.
- `python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/tools/routed-defects.py --selftest; rc=$?; printf 'exit_code=%s\n' "$rc"; exit "$rc"` — `SELFTEST: CLEAN cases=17`; exit **0**. The selftest's temporary repository is removed by the tool (`:1011-1012,1290-1291`). No tools were installed.

## Findings by severity

### High — `validator-sha256-pinned` is not pinned

**Observation:** `.ufo/waves/round-18/tools/routed-defects.py:463-467` accepts any string of 64 hexadecimal characters. This check does not hash or compare the `receipt-validate.py` blob at the evaluated revision. The previous spotcheck explicitly identified the missing comparison with the validator blob hash (`corpus/lessons/round-18-verifier-spotcheck.md:194`).

**Fabrication passes: yes, including full defect closure.** The closed fixture supplies `"f" * 64` (`routed-defects.py:978-984`), and the selftest asserts all defects/check sets close (`:1089-1104`). The successful selftest confirms that an arbitrary well-shaped value passes the validator pin check when the fixture's other internally-consistent artifacts are present. This is an unbound identity claim, not a SHA-256 pin.

### Moderate — S032 digest/anchor checks accept fabricated hashes

- **`s033-anchor-commit`** (`routed-defects.py:780-786`) passes if the selected anchor cell contains *any* 40-hex token; it does not resolve that token as a Git commit. **Fabrication passes: yes.** The closed fixture uses `H1` (`"a" * 40`) in the S033 anchor (`:972-974`), and the full closed-fixture assertion passes (`:1097-1104`).
- **`s032-digests-evidence`** (`:753-763,795-813`) recursively gathers 64-hex strings from arbitrary JSON values and requires only two distinct strings. It does not bind either digest to page bytes or another retained source. **Fabrication passes: yes.** The fixture uses `"1" * 64` and `"2" * 64` (`:986-987`) and still closes the check set (`:1097-1104`).
- **`superseding-row`** (`:741-750,775-793`) checks row width and marker phrases (`11` cells, a `supersedes S032 —` prefix, and `fetch-time` in the anchor cell), not the source's provenance. **Fabrication passes: yes.** The fixture supplies such a row with the fake `H1` anchor (`:972-974`). The check is a lexical row-shape predicate, not evidence that S033's page digest was actually captured.

### Moderate — code-marker checks do not establish behavior

**Observation:** `carrier-run-map-code` tests only for `map_sha256` in tokenized non-comment code (`routed-defects.py:260-270`); `receipt-validate-mid-finding` tests only for two finding-id strings in tokenized code (`:272-288`). Neither executes or evaluates the implementation.

**Fabrication passes: yes.** The fixture's `carrier-run.py` merely assigns `digest` to `map_sha256` (`:945-948`), and its validator defines a tuple of finding strings and returns that tuple (`:949-952`); the complete selftest still passes. Thus dead, incomplete, or behaviorless code carrying the expected tokens satisfies these two checks. The separate retained-map check does hash stored map bytes (`:349-364`), but it does not prove the validator executes the advertised comparisons.

### Low — other shape/pattern-only predicates

| Check and lines | What it accepts | Fabrication result |
|---|---|---|
| `validate16-summary`, `routed-defects.py:405-434` | A JSON object with the expected `rev`, eight receipt entries, and integer `exit` fields. | **Yes, for this check.** A fabricated summary can satisfy the schema. Other checks later compare labels/run directories and retained stdout hashes (`:448-485`), so this schema check alone is not enough to close the defect. |
| Producer `*-names-producing-revs`, `:518-528` | A line with the defect token and any two distinct 40-hex strings. | **Yes, for the named checks only.** The selftest's `H1`/`H2` fabricated pair is exercised at `:1209-1233`; its assertion confirms the defect remains open because exact pinned-revision text and ancestry are checked separately (`:541-553,1278-1282`). |
| `log-fraction-true`, `:44,619-636` | The number of lines matching `^== \S+ start\b`, then a matching fraction in `LOG.md`; it does not validate that each line represents an actual process start. | **Yes, in a fabricated history.** The selftest synthesizes the seven start lines (`:848-850`) and accepts the derived 7/8 fixture. In the lane the tool reads the run log from its fixed `RUNLOG_REV`; the parser itself remains pattern/count-only. |
| `skill-scope-*` and citation-drift row checks, `:655-677,701-718,719-733` | Presence of `Pinned values:`, `Write scope:` plus three words, existing backticked paths, a second cell beginning `gate`, and `--strict` somewhere in the third cell. It does not validate the asserted pinned values or execute the registered command. | **Yes.** The fixture uses `Pinned values: none` and placeholder scope prose, plus `c --strict` (`:953-965`), and passes the closed-fixture test. In particular, `Pinned values: none` satisfies the purported pinned-values clause. |
| Generic `_line_with` / named checks, `:8-11,132-139` and call sites such as `:204-209,240-245,435-438` | Same-line substring presence. The module documents these as token/naming checks, separate from substantive checks. | **Yes, by design:** fabricated prose containing the expected tokens passes the named check. These checks must not be treated as independent evidence of the named claim, and their pass alone cannot close a defect. |

## Checks not classified as format-only

Several similarly hash-shaped parsers do bind the value to bytes: `r18-receipt-pinmaps` compares the map blob's SHA-256 with `map_sha256` (`routed-defects.py:349-364`); `summary-stdout-bound` hashes retained stdout (`:471-485`); and `sums-covers-carriers.tsv` compares the recorded digest with the actual `carriers.tsv` blob (`:563-585`). A fabricated *wrong* digest fails those comparisons. This contrast is why `validator-sha256-pinned` and the S032 digest checks are material gaps.
