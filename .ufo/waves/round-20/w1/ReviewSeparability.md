# Round-20 claim separability review — C1/C2/C3 (seat ReviewSeparability-2)

Axes: C1 calibration, C2 coverage, C3 depth (claims.json:11,21,33). Question: can each claim be
verified with the others reverted, and what shared files/tools couple them?

Method: read-only census of claims, contract, spec prompts, and baseline/HEAD tool sources. No
tool was installed or upgraded. Timestamp of report: 2026-10-20 (clock at write). Base observed:
lane HEAD `d1d981d2cc041dda4656c5b01d2c8445d8d17124` (1 commit past B=14f0260: the declaration
commit; `git log --oneline 14f0260..HEAD` exit 0). Round-20 tools do not exist in the tree yet
(`glob .ufo/waves/round-20/**/*.py` → only gen-wave1.py): all claims-verifier behavior below is
read from the binding interfaces (contract.md §Interfaces) and the round-19 patterns, i.e.
observation of plan text + [INFERENCE] where marked.

Commands run (all exit 0 unless noted): `git --no-optional-locks rev-parse HEAD`; `git status
--porcelain=v1 | head`; `git log --oneline 14f0260..HEAD`; `jq` extractions of
wave1-spec.json items; `wc -l SCORECARD.md SKILL.md PROVINCE.md corpus/QUALITY.md` (SOURCES.md
at lane root: exit 2, no such file — the registry is corpus/SOURCES.md);
`grep -n` anchors cited below; `ls` of the npx cache path and `node --version` (v24.21.0);
`ls -la /home/vgpnk/.local/opt/go-1.24.6/bin/go` (`-rw-r--r--`, exec bit cleared).

## Verification chains (observed from claims.json + contract.md)

- C1: routed-r19.py --strict (claims.json:17) executes REV's own D1–D6 tool bytes; plus
  c1-census-v10.py --root LANE — a LIVE-tree reading (claims.json:18 "census exit != 0 at the
  delivered tip"). Contract interface rows: D3 contract.md:46, D6d contract.md:65.
- C2: verb-coverage.py --root LANE --rev REV (claims.json:28); knowledge entries + ev_ ids +
  evidence under .ufo/waves/round-20/evidence/c2/ at REV (contract.md:71-75).
- C3: measure.py <REV> field c3.first_failure_bound (claims.json:38); receipt gate
  `receipt-validate --require-mid-maps` (claims.json:39); carriers contract.md:88-90.

## Revert test — verdict per claim

- C2 with C1+C3 reverted: YES, fully separable. verb-coverage reads only C2-authored files
  (entries, evidence/c2/, README map) plus the host npx cache. No C1/C3 artifact in its input
  set. [INFERENCE from contract.md:71-75 + claims.json:28-30; tool not yet landed]
- C3 with C1+C2 reverted: YES with two named caveats.
  (a) measure.py embeds the C1/C2 counters (spec items[MeasureR20]: fields c1 via routed-r19,
  c2 via verb-coverage). The round-19 pattern tolerates absent tools: "Anything absent or
  unusable at <revision> prints `null` plus a named reason (`tool_absent_at_rev`, …); the run
  never crashes on it" and "Exit 0 after the report is emitted"
  (round-19/measure.py:31-38, :325, :458). [INFERENCE] Provided the r20 port keeps that
  tolerance, c3.first_failure_bound stays computable when W20/tools/{routed-r19,verb-coverage}.py
  are absent. This tolerance is a separability requirement, not decoration.
  (b) The receipt gate degrades gracefully: `--require-mid-maps` already exists at B
  (round-17/tools/receipt-validate.py:6,:33-39,:1142), so with the C1/D6d edit reverted the gate
  still runs — but analyze-step identification falls back to the decoy-permissive rule
  (`step`/`name` "analyze" or any argv `analyze` token, receipt-validate.py:37-39), i.e. the
  receipt-authenticity STRENGTH of C3's evidence depends on C1 landing. C3 is verifiable either
  way; its meaning differs.
- C1 with C2+C3 reverted: YES with two named caveats.
  (a) routed-r19's D3 substance consumes a C3 artifact when present: the arm/check record's
  "carrier set equals predictions/carriers.tsv (if that file exists at REV)" (spec
  items[RoutedR19Tool]). With C3 reverted the conjunct self-skips, so D3 still closes; with C3
  present a later carriers.tsv change invalidates C1's D3 record.
  (b) The tip-census half of C1 (claims.json:18) is a claim about the FULL tip, so it is not
  verifiable in a C2/C3-free tree by construction — it quantifies over whatever landed.

## Shared-file / shared-tool couplings (the answer to the assignment's question)

1. `.ufo/waves/round-17/tools/receipt-validate.py` — edited IN PLACE by C1/D6d
   (contract.md:65; ControlsR20 lists it among allowed in-place edits), and consumed by C3
   measurement (claims.json:39) and re-validation of retained r18/r19 receipts (spec
   items[ArgvDecoy]). Direction: C1→C3. Keeps separable: (i) the D6d patch must be proven
   against every receipt class C3 counts — ArgvDecoy's assignment already mandates re-running
   `--require-mid-maps` over r18/r19 receipts with exits 0; extend the same proof to the
   round-20 receipts once they exist, BEFORE the freeze/measure step; (ii) C3 run receipts must
   be born compatible (REA argv `analyze` immediately after the `rea-agents@6.5.0` token), which
   holds if the L1 integrates D6d before running carriers (runs are post-integration anyway).
2. Root docs ↔ census tip PASS — the widest cross-claim coupling. Census SCOPE is exactly
   PROVINCE.md / SKILL.md / SCORECARD.md (c1-census-v10.py:254-276; the read loop is keyed on
   SCOPE's file set, :268-270 comment "Register files must also appear in SCOPE"). SCORECARD.md
   is 2567 lines; declared DATED bounds end at :2122 (c1-census-v10.py:276), and the standing
   records-commit rule says text appended past the declared bound must be locus-free — no
   `rea-agents@x.y.z`, no bare `6.x.y`, no `~`/absolute `path:line` — or the bound must be
   re-keyed in the same commit (c1-census-v10.py:42-46). C2's record rows will naturally cite
   `rea-agents@6.5.0` and evidence paths; C3's rows cite tools/predictions. If those land in
   SCORECARD.md tail (or PROVINCE frontier bullets change — FRONTIER register :281-303, "any
   frontier edit re-keys the register in the same commit"), the live census at the tip FAILs and
   C1 is falsified (claims.json:18) by C2/C3 text, not by any C1 defect. Keeps separable: the L1
   integrates every records-commit together with the same-commit SCOPE/FRONTIER re-key (the
   rule's own remedy), or keeps tail records locus-free; CensusRekey's round-17 declarations
   (spec items[CensusRekey]: SCORECARD 2380-2382, SKILL 511-519) are necessary but not
   sufficient for the tail the round itself appends.
3. `predictions/carriers.tsv` (C3, GenPredictionsR20) ← read by C1's counter: routed-r19 D3
   compares the carrier-guard check record's carrier set against it at REV (spec
   items[RoutedR19Tool], clause "(if that file exists at REV)"). Direction: C3→C1. Keeps
   separable: freeze carriers.tsv BEFORE taking the carrier-guard arm/check records that
   routed-r19 will match; any manifest change re-runs arm+check before integration.
4. carrier-guard state — C1's D3 evidence (arm.json + exit-0 check records,
   contract.md:46-49; already armed at .ufo/waves/round-20/evidence/carrier-guard/, committed in
   d1d981d) is also C3's run gate: run-carriers.sh runs `carrier-guard.py check` before each
   label and aborts on exit 1 (spec items[RunnerR20]). Shared host state: Go carrier exec bits
   are cleared on disk (observed `-rw-r--r--` on go-1.24.6/bin/go). Keeps separable: C1's D3
   records and C3's pre-label checks read the same arm record; do not disarm between the C1
   demonstration and the C3 run window, and end every window in the armed+checked state.
5. measure.py aggregation — C3's declared counting command (claims.json:38) internally computes
   c1 and c2 too (spec items[MeasureR20]). This is aggregation, not dependence, ONLY if the
   per-claim fields are computed independently and absent-sibling counters yield
   `tool_absent_at_rev` nulls (round-19/measure.py:325,:458 pattern). Keeps separable: MeasureR20
   must not let a routed-r19/verb-coverage failure (nonzero exit, non-JSON) abort the c3 field;
   the pattern already contracts for this (round-19/measure.py:31-38).
6. evidence-timestamps wide sweep — VerifyR20 runs evidence-timestamps over ALL of
   .ufo/waves/round-20 at SOURCE expecting 0 findings (spec items[VerifyR20]), while C1's own
   counter (routed-r19 D2) only exercises the r19 fixture (spec items[RoutedR19Tool]). Every
   C2/C3-authored timestamp (receipts' started/ended_at_utc, evidence taken_at_utc) therefore
   feeds a round-level red that is easy to misattribute to C1. Keeps separable: authoring rule
   only — timestamps taken from the clock at write time, before the commit that introduces the
   line (contract.md:31-32); no cross-claim code dependence.
7. final-census.json ordering — D5 requires the recorded rev's tree to differ from REV only in
   that record + its stdout file (spec items[RoutedR19Tool] D5 clause), and FinalCensusRecorder
   refuses a dirty worktree (spec items[FinalCensusRecorder]). So the D5 record must be the LAST
   lane write before verification — an integration-order coupling among all three claims, owned
   by the L1.
8. Shared host state (not git-revertible): the npx cache path
   ~/.npm/_npx/ad9a3fdbcad992c6/.../cliCommandNames.js is C2's command catalog source
   (contract.md:71-72) and the same rea-agents@6.5.0 install runs C3's carriers; node v24.21.0
   observed present. Cache eviction or a version bump changes both claims at once — record the
   package version in each claim's evidence (C2 already does: package_version field,
   spec items[VerbCoverageTool]).

## Residual risk and verification gaps

- None of the round-20 tools exist at HEAD yet, so every "keeps separable" clause above is a
  plan-level obligation; the two that can silently break the revert property are (5) measure.py
  crash-tolerance and (2) SCORECARD tail re-key discipline. Both are checkable at integration:
  run `measure.py <REV>` in a tree with W20/tools/{routed-r19,verb-coverage}.py deleted (expect
  c3 still emitted, c1/c2 null with `tool_absent_at_rev`), and run the census at the tip before
  declaring C1 closed.
- The D6d strictness vs round-20 receipt shapes is unmeasurable until both ArgvDecoy's patch
  and RunnerR20's receipts exist; the ArgvDecoy assignment covers r18/r19 only
  (spec items[ArgvDecoy]) — r20 receipts are the gap named in coupling 1(ii).
- [INFERENCE] labels above mark plan-derived statements; all path:line and exit-code statements
  are observations from the commands listed.
