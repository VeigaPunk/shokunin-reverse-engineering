PARTIAL

# SimplifyR18Tools — YAGNI review of the round-18 tools at REV b2aad08 (wave 2, falsify)

Seat: KaidokuR18.SimplifyR18Tools (simplifier, author-side advisory, not an outside reviewer).
Scope: `.ufo/waves/round-18/{tools/*.py, measure.py, controls.py, verify.py, gen-predictions.py}` at
REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94` (BASE `9011581`). All 9 files on disk are byte-identical to their REV
blobs (9/9 sha256). All `path:line` anchors are at REV. Every edit was made in the mkdtemp clone
`T=/tmp/simplify-r18-WzmOx3/lane`. Its origin remote was removed before any write; `git remote` printed nothing. The
deletions are in scratch commit `S1=cfdb975` (patch `$T/../yagni-deletions.patch`). No REA or Ghidra runs. No carrier was
executed (the emulator only reads bytes). verify.py and gen-predictions.py were not run because both write the lane.

## Verdict
- **HOLDS (counting commands):** at REV, C1 `open_count` is 0 (6 at BASE) and C2 `live_count` is 0 (3 at BASE). C3
  counts 15 compare.json files, and all 15 carry `extra.*`. Controls report 15517/15517 frozen blobs unchanged. The REV
  emulator reproduces all 15 frozen outputs. jj-red-before holds 14/14 (§1).
- **BROKEN:** `tools/routed-defects.py --selftest` exits 1 at REV, with 7 of 17 cases failing. The b2aad08 amendment
  at routed-defects.py:282 requires two finding ids. The closed fixture still carries the stale placeholder
  `mid_map_mismatch` at routed-defects.py:914-916. contract.md:46-47 requires that closed case to pass (§2).
- **Deletions:** 14 deletions plus 1 stale-name fix, net −137 lines across 6 files. They preserve every counting
  command byte-for-byte (§3-4). Eight more deletions in swiss-misread.py (net −34) also preserve all 15 frozen outputs,
  but they are **BLOCKED**: all 15 receipts pin the emulator's bytes, so editing it makes receipt-validate fail (§5).
- **Load-bearing duplication:** the 7 duplicated git-wrapper helpers support C2. Consolidating them would blind
  head-rev-lint (§6).

## 1. Counting commands at REV (observation; cwd = lane, `python3 -I -B`)
| command | exit | result |
|---|---|---|
| `tools/routed-defects.py --root . --rev REV` / `--rev BASE` | 0 / 0 | open 0 (named 0, substance 0) / open 6 (6, 6) |
| `tools/routed-defects.py … --strict` REV / BASE | 0 / 1 | |
| `tools/head-rev-lint.py --root . --rev REV` / `--rev BASE` | 0 / 0 | live 0, fixture 15, annotated 6, files 39 / live 3, fixture 8, files 27 |
| `tools/head-rev-lint.py … --strict` REV / BASE | 0 / 1 | |
| `measure.py REV` | 0 | c1 0, c2 0, c3 15/15 with extra, could_not_evaluate false |
| `controls.py BASE REV` | 0 | frozen 15517/15517, QUALITY rows 20→21, rows_1_20_identical true |
| `tools/revpin.py --root .` | 0 | head_equals_source true, pushed true |
| `tools/swiss-misread.py --carrier <15 paths from predictions/carriers.tsv> --golang-root G` | 15× 0 | 15/15 parsed-equal to `predictions/swiss-misread/<label>.json`; aether eof `[[17645861, 111938854]]` |
| `tools/jj-red-before.py --root $T --out $T/../cmp/…` | 0 | 14/14 held, not_runnable [] |
| `--selftest`: head-rev-lint, revpin, swiss-misread, jj-red-before, measure, controls | 0 each | CLEAN 3, 11, 15, 5, 68, 23 |
| `tools/routed-defects.py --selftest` | **1** | see §2 |

## 2. BROKEN: routed-defects selftest (observation, with one inference)
- `python3 -I -B .ufo/waves/round-18/tools/routed-defects.py --selftest` → exit 1. Output:
  `FAILED closed-fixture-cli: … broken=['receipt-validate-mid-finding', 'producer-revs-are-ancestors']; closed-fixture-inprocess: open_count=1 …`
  The 5 token-only cases also fail with `extra_open=['R17-PINMAP']`.
- `git show eb6c266:…/routed-defects.py > x.py; python3 -I -B x.py --selftest` → exit 0, `CLEAN cases=17`.
  `git diff eb6c266 b2aad08 -- …/routed-defects.py` changes only the check at :277-288.
- A fix-only copy that replaces the stub at :914-916 with both amended ids → exit 0, `CLEAN cases=17`. The root cause
  is therefore the stale fixture name.
- **[INFERENCE]** verify.py:157-159 expects `selftest-routed-defects` to exit 0. A verify pass at REV would therefore
  list it in `unexpected_exits` and exit 1 (verify.py:295). The counting output does not depend on this fixture.

## 3. Deletion set (applied in S1; the evidence for each "dead" claim is an observation)
| ID | REV anchor | deletion | why it is weight |
|---|---|---|---|
| M1 | measure.py:38, :184-206, :214 | `run` fallback plus `inspect.signature` probing in `_invoke`; now calls `main(argv)` | both tools define `main(argv=None)` (routed-defects.py:1261, head-rev-lint.py:893); no stub uses `run` or a zero-argument main |
| M2 | measure.py:170-181 | last-line fallback in `_parse_json` | both tools emit one JSON document; the selftest stays CLEAN without it |
| M3 | measure.py:17-20, :125-127, :140-141, :145; selftest :579, :594, :601, :708, :719, :740, :749, :766 | sibling-import machinery: copy every `tools/*.py`, push `sys.path`, `STUB_REVPIN` | neither counted tool imports a sibling (stdlib-only imports at routed-defects.py:27-39 and head-rev-lint.py:68-76); only a stub exercised it; the module purge is kept |
| M4 | measure.py:271-373 | `_claim_c1` and `_claim_c2` share about 45 identical lines; replaced by `_claim_tool` plus two small adapters | keys, values and reason strings are unchanged |
| H1 | head-rev-lint.py:116-119, :527, :632 | `ANNOTATION_REASONS` | restates the vocabulary already in `ANNOTATION_RE` (:113-115); the output string is identical |
| H2 | head-rev-lint.py:356-357, :450 | `SiteScanner(lines)` / `self.lines` | stored but never read (`grep self.lines` finds only :357) |
| H3 | head-rev-lint.py:416-420 | second callee-name computation | duplicates :395-399 |
| R1 | routed-defects.py:294-310, :353-364 | relative-path and `lstrip("/")` arms of `_map_candidates` | every r18 receipt `map_path` is absolute and contains `.ufo/`; the only producer joins it under the W18-resolved `out_dir` (r17 carrier-run.py:501-502, run-carriers.sh:7); fixture :956 now uses the absolute form |
| R2 | routed-defects.py:379-382, :451-452 | `labels` branch of `_summary_labels` | summary.json keys are `receipts, remap, rev, validator_rev, validator_sha256`; the real data takes the receipts arm; fixture :944 dropped; mutation :1165 moved to `receipts[].label` and still kills |
| R3 | routed-defects.py:914-916 | **stale-name fix**, not a deletion | §2 |
| J1 | jj-red-before.py:186-193; fixture :752, :768-769 | JSON branch of `probe_resolved_rev` | fixture-only: the real probe prints only `CITATION_DRIFT_REV_*` lines (gates/citation-drift-probe.py:396-401); the stub now prints that same format |
| J2 | jj-red-before.py:275-276, :310-311 | duplicated jj identity `cfg` literal, now one `JJ_CFG` | the same literal appeared twice |
| K1 | controls.py:40, :600-606, :786 | hand-rolled `_rmtree` and the now-unused `os` import | duplicates `shutil.rmtree`, which every other tool uses |
| V1 | verify.py:64-80 | fallback in `run_labels` to runs/ directory names | carriers.tsv is tracked with 15 rows; the modified `run_labels()` returns the identical 15-label list (in-process, read-only call) |
| V2 | verify.py:193-195, :205-219, :229 | fresh `log-extract` fallback | a second observation authority; 15/15 runs carry a tracked observation.json, receipt and prediction |

Net change by file (`git diff --numstat b2aad08 S1`): measure −64, verify −26, routed-defects −20, head-rev-lint −10,
controls −9, jj-red-before −8.

## 4. Preservation proof (observation; "orig" is the REV bytes copied to `$T/../orig`, "mod" is S1)
```
{orig,mod}/routed-defects.py --root LANE --rev REV|BASE      # 0/0, stdout byte-identical (cmp), both revs
{orig,mod}/head-rev-lint.py  --root LANE --rev REV|BASE      # 0/0, byte-identical, both revs
… --strict (both tools)                                      # REV 0/0, BASE 1/1
{orig,mod}/measure.py --root $T REV|BASE|S1                  # 0/0 at each; JSON equal apart from argv; S1: c1 0, c2 0, c3 15/15
{orig,mod}/head-rev-lint.py --root $T --rev S1 --strict      # 0/0; live 0, fixture 15, annotated 6
controls.py BASE REV, lane copy vs scratch copy              # 0/0; JSON equal apart from invocation
mod swiss-misread.py on the 15 carriers                      # 15× exit 0; 15/15 parsed-equal to the frozen outputs
{orig,mod}/jj-red-before.py --root $T --out …                # 0/0; 14/14 held both; (name, held) lists identical
mod --selftest: routed-defects 0 (17), head-rev-lint 0 (3), jj-red-before 0 (5), swiss-misread 0 (15),
                measure 0 (67; the one removed case is b_no_revpin_leak), controls 0 (23)
```
J1 also improves selftest fidelity (observation). I mutated jj-red-before.py:199 from `_line("REV_RESOLVED")` to
`_line("REV_RESOLVED_MUTANT")`:
- REV selftest → exit 0, `CLEAN 5` (the mutant survives).
- Simplified selftest with the same mutant → exit 1 (`fixed-citation-drift` not held).
- Real run with the REV mutant → exit 1, 13/14 held.

So at REV the selftest never exercises the parse path that the real run uses.

## 5. Blocked by the pin: swiss-misread.py (observation)
These deletions are applied in S1, which still reproduces all 15 frozen outputs and keeps the selftest CLEAN at 15:
- :46 unused `import os`
- :488-490 `_read_section_u32`, which is never referenced
- `select_snapshot` (:245, :256-257, :261, :287-288, :292, :1285): parameters `goos`/`goarch` are unused, fields
  `requested`/`diff_patch` are never read, and field `base` duplicates `path`
- `--debug` (:1251, :1295-1296, :1576-1581, :1821, :1835): not in contract.md:110 and never passed by gen-predictions
- `results[h]["order"]` and `["marked"]` (:1333, :1336): never read
- `failure_kind`'s `walk` parameter (:1468, :1473-1474): always None
- `_build_elf64` parameters `sections`/`writable_data` (:1601, :1617-1622): never passed
- `_fixture` (:1673, :1743, :1757/1773/1783/1792): `huge_length` is always the default, and the returned
  `typelinks, tl_va` are always discarded

**Why these are blocked:** all 15 r18 receipts pin `tools/swiss-misread.py` at sha256 `14924bd6…`, which is the REV
blob and also `c3.emulator_sha256` (gen-predictions.py:70). receipt-validate re-hashes every pinned path
(receipt-validate.py:262-294 → :216-244). I tested a copy of the s1246-swiss-nethttp receipt under
`--require-mid-maps`:
- emulator pin path pointed at an *unmodified* copy → exit 1, findings `mid_map_compare_mismatch` only (an artifact of
  rewriting the path);
- pointed at the *edited* emulator → exit 1, adding `sha256_mismatch` and `size_mismatch`.

The frozen `binding_gate` (gen-predictions.py:83, decision-rule.json at eb6c266) requires receipt-validate to exit 0,
so an in-place edit would drop all 15 C3 labels. Ship these only in a new emulator file with a new freeze.

Output-changing, not applied: `predicted_failure_kind` and `predicted_invalid_index_reads` (:1521-1522) alias the
`_h1` fields and nothing consumes them (grep of round-18 `*.py`). `predicted_eof_reads` and `predicted_failure`
(:1519-1520) are contract-named (contract.md:116-118) and must stay.

**Calibration finding:** `_parse32` (:98-100, :133-156) parses ELF32, but module discovery hard-codes the 64-bit
layout: the `"<Q"` needle at :556, `"<QQ"` at :576, :586-587, kind at 0x17 (:516) and str at 0x28 (:520).
`python3 -I -B $T/../elf32_probe.py elf32.bin` builds a synthetic GOARCH=386 ELF32 with a correct 32-bit typelinks
slice. On it, `Elf` gives ptr_size 4 and buildinfo reads `go1.24.6` (inline), but `discover_modules` returns `[]` and
the CLI exits 2 with `no Go moduledata/typelinks found`. The `limits` line at :1494-1495, which appears in every frozen
output, nevertheless says 32-bit carriers "use the same JSON layout law". That overclaims. `_parse32` is dead weight,
and so is that text.

## 6. Kept: duplication that is load-bearing, and contract-named surfaces
- **Git wrappers (7 copies)** at routed-defects.py:72-118, head-rev-lint.py:153-184, revpin.py:71-90,
  measure.py:85-112, controls.py:80-97, jj-red-before.py:157-170 and verify.py:60-61, plus 4 spec-loader copies. Keep
  them. head-rev-lint resolves wrappers only within a file (LIMITS at head-rev-lint.py:134-135). In a fixture repo,
  the same `_git(".", "rev-parse", "HEAD")` call is a live site through an in-file wrapper but produces 0 sites through
  an imported one (exit 0, live 1). A shared helper module would hide HEAD sites from C2.
- revpin `--branch`, `--no-require-pushed`, `--no-require-head` (revpin.py:292-296) are contract-named
  (contract.md:57), even though only revpin's own selftest uses them.
- swiss-misread `--go-version` (contract.md:110); both `EXTRA_FIELDS` names in measure (contract.md:139-141);
  `ROUTED_SITES` (provenance).
- gen-predictions.py stays untouched as the producer of the freeze (historical provenance).

## 7. Candidates not applied (tradeoff named)
- **verify.py pins-CLI triple** (:150-152, :262-266): it re-pins a subset of the in-process pin set (`pin_paths`
  ⊇ tools, :105-114, :268). The CLI is already exercised by `selftest-w17-pins` (r17 pins.py:222-259). Cost of
  deletion: the tools-pre/post.json artifacts go away. [INFERENCE] no loss to any count; verify.py cannot be run here.
- **jj-red-before CLI options** `--branch`, `--baseline-rev`, `--cd-probe`, `--custody-pair`, `--revpin`
  (:1010-1022): not contract-named (contract.md:96-97 names only `--out`) and not used by verify.py:190-191. Keep
  `--root`: this review needed it to aim the probe at a scratch clone.
- **verify.py `skip()`** (:131-147): unreachable with REV's inputs, but deleting it turns a recorded skip into a
  traceback, which harms operability.
- **Duplicate revpin loader** in jj-red-before (:433-438, :673-678): merging saves about 2 lines net; not worth it.

## 8. Rejected scan hits and incidental observations
- My AST scan flagged `from __future__ import annotations` (routed-defects.py:27, jj-red-before.py:73, revpin.py:47)
  as unused imports. That is a false positive: these are compiler directives with no runtime weight on Python 3.14.8.
- `.ufo/waves/round-18/tools/__pycache__/` exists, holding routed-defects and swiss-misread .pyc files with mtimes
  13:46 and 13:57 -03:00. It predates this seat's scratch (14:02), and every run here used `-B`, so I did not create
  it. verify.py:269-271/:295 counts any `__pycache__` under `.ufo` without a before-snapshot. [INFERENCE] A verify
  pass run now would exit 1 regardless of its own hygiene.

## 9. Lane untouched (observation)
- HEAD is b2aad08.
- `git status --porcelain --untracked-files=no` is empty.
- The refs digest was `beab883eb9b46d39` both before and after the jj runs.
- All 9 target files are byte-identical to REV.
- This report is the only lane write. No tools were installed.
