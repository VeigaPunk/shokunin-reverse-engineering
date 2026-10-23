# RevCHPEExclusion — review of R34ParserBounds and retained bounded receipts

Seat: `KaidokuR34.RevCHPEExclusion` (reviewer, read-only prose; no execution).
Scope: review `prep/R34ParserBounds.md` + retained `prep/R34ParserBounds-files/` receipts.
No production reader, parser, or REA run was performed by this reviewer.

## Verdicts confirmed

### 1. Count survivor remains OPEN — confirmed
- Verdict in `results.json`: `count` = SURVIVED, `identical_stdout_all_phases: true`, `mutant_hash_matches_plan: true`.
- Count phases (pristine/mutated/restored) all exit 0; stdout byte-identical
  (21794 B, sha256 `bb11bba0de20f2aac16ee08f4dccaf583a87ea65b06494c494acd2110bb8f2bd`);
  selftest summary identical: pass=true, cases=107, failed=[], 45/45 finding IDs, vocabulary_ok=true.
- Retained mutant `count/chpe_profile.py.mutant:258` literally contains
  `if cm_count >= MAX_CODE_MAP_COUNT:` (`mutation.patch` matches; mutant digest `e2ae2ccbac...`
  matches plan). Count receipts record source_before/source_after equal to the mutant digest and
  source_final equal to pristine digest; restoration UTC 10:25:42.331388.
- No corpus case exercises equality: static AST inventory finds recipe literal only 2000
  (`selftest_pegen.py:279`), no 1024 literal (`inputs.json`). The `>`→`>=` change is therefore
  behaviorally invisible to the unchanged detector. The survivor stays open; recommendation
  (no successor patch without a discriminating input) was adopted verbatim in
  `corpus/lessons/round-34.md:33`.

### 2. Span now KILLED — confirmed (fresh bounded evidence)
- Metadata mutation (`need(..., CHPE_METADATA_SIZE, "metadata")` → `12`) at `metadata/chpe_profile.py.mutant:250`.
- Mutated run: exit 1, stdout 22613 B sha256 `f8c25e7a9078d1af4352f7ef719a24074ff9469db2c52b42b58ca082d9e511b3`;
  summary shows exactly **four structured mismatches** (L0+L1 metadata_zero_tail and metadata_cross_section:
  got `candidate.structural` exit 0 vs want `outside_profile.*` exit 11), 43/45 IDs produced,
  uncovered = those two IDs. Pristine and restored both pass (exit 0, stdout `bb11bba0...`).
- This is a real structured kill with passing baselines — distinct from round-33 `WMutMetadata.md`
  EAGAIN inconclusive (all phases failed to spawn child). The old record is untouched; the phrase
  "resolves the old EAGAIN inconclusive result" is accurate as new evidence, not a historical rewrite.

### 3. Tag only detector error — confirmed
- Tag mutation (`if tag not in TAGS:` → `if tag > 3:`) at `tag/chpe_profile.py.mutant:269`.
- Mutated run: exit 1 in 0.414s, stdout 0 B, stderr 1114 B sha256 `4420301c5f8de4ec6ef6346981897de56e793f32d7ae3456162d5be2d173c7e1`
  = parent `JSONDecodeError` at selftest line 328 (`json.loads(p.stdout)`). The child's captured
  stderr is hidden by the unchanged selftest; the underlying child case is not observed/asserted.
- Pristine and restored pass. Detection therefore rests **only** on the detector error/crash —
  a nonzero differential between two passing runs, not a structured finding-ID assertion.
  Matches the assignment's "tag only detector error".

## New claim independence — no dependence found
- Grep for `chpe|selftest_pegen|R33FixtureBuilder|U064N008Hf47eb933` returns zero matches in:
  `tools/round-34/` (counter/reader/integrity), frozen `expected.json`, knowledge entry
  `2026-10-23-r34-elf-version-needs.md`, and `prep/R34Expected-files/` (selection.json, checks.json,
  manifest, author_expected.py, challenge).
- `claims.json` instruments are only the four round-34 files with pinned digests; `held_exclusions`
  records `U064N008Hf47eb933` and `R33FixtureBuilder and derivatives`.
- `corpus/lessons/round-34.md:33` states none of these CHPE instruments is used for R34-C1
  admission; `R34LegacyGaps` evidence is likewise excluded from C1.

## Receipt/containment integrity
- Nine actual runs, one per phase, all under `prep/R34ParserBounds-files/`; argv identical across
  phases except private directory; bounded: timeout 30s + kill-after 2s, supervisor 35s,
  prlimit as=256MiB cpu=20 fsize≈1MiB nofile=128 core=0 (nproc=8192 is per-UID, documented);
  sequential probes, max 1 CLI child; TMPDIR per copy; LC_ALL=C.UTF-8; all process groups absent
  after cleanup (ESRCH); no external imports/fixture authoring (`run_probe.py` recorder).
- Source provenance: lane `chpe_profile.py` bytes verified by base-commit `git ls-tree`/`git show`
  before copying; lane before=after sha256 `b364de7034...`; sibling `selftest_pegen.py` sha256
  `aea5475c0ce...` unchanged everywhere; `restoration.json` confirms exact-byte equality of all
  private restored modules; `artifact-manifest.json` binds every retained file's bytes + digest.
- No tool install; Python 3.14.8, coreutils 9.12, util-linux 2.42.4 listed.

## Residual risk and verification gaps (low severity)
1. Count equality boundary remains untestable on the existing corpus; survivor is thereby
   permanently open until a discriminating input exists. No repair attempted — correct per scope.
2. Tag kill is crash-only; exact child failure unobserved. Any future tag-sensitivity claim would
   need a separately retained instrument exposing child stderr; not claimed here.
3. "Resolves the old EAGAIN inconclusive" wording could be misread as a historical repair; it is
   new evidence only. Old `WMutMetadata.md` remains intact.
4. R34ParserBounds executed only nine bounded CHPE selftest probes on private copies; no round-34
   ELF reader, REA/MCP, carrier execution, or fixture authoring occurred. Nothing in the reviewed
   record contradicts the wave's no-parser/no-REA constraint for production.

Recommendation: retain the disclosed survivor/open-span/tag-error-only posture; keep CHPE
instruments and held builder output excluded from R34-C1 admission. No action required in this
review's scope.
