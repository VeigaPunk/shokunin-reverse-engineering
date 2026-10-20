# CitationDriftBranchTip — round 18, wave 1 report

Scope: `citation-drift-probe.py` in-place fix for jj risk R2
(`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjAuditKaidoku.md:164-166,244`;
contract `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18/contract.md:73-77`).

File changed: `.ufo/gates/citation-drift/citation-drift-probe.py` (only file written
besides this report).

## Behavior change

- `--rev` omitted no longer defaults to the moving `HEAD`; it resolves the tip of
  `--branch` (new flag, default `main`, i.e. `refs/heads/main`) — `resolve_rev`
  at `citation-drift-probe.py:310`, argparse at `:575-580`.
- Literal `--rev HEAD` is accepted only when HEAD equals the branch tip; otherwise
  the run is could-not-evaluate with finding `head_not_branch_tip` (`:330-336`),
  exit 2. A missing `refs/heads/<branch>` is `branch_missing` (`:322-325`), also
  exit 2 — both ids added to the CNE set at `:93-94`.
- Explicit 40-hex (and any other) `--rev` passes through unchanged; `rev_ok` still
  grades an unresolvable rev `revision_unresolvable` (`:353-356`). `rev_resolved`
  records the normalized commit id when resolvable (`:340`).
- HEAD is resolved via `git rev-list --max-count=1 HEAD` (`head_commit`, `:299`),
  deliberately not `rev-parse …HEAD…`, so no `rev-parse-HEAD` live site appears
  under the C2 head-rev-lint site kinds (contract :64-66); the call carries the
  `# head-rev-lint: compare-only` marker per L1 note (`:304`).
- Report emits `CITATION_DRIFT_REV_REQUESTED`, `CITATION_DRIFT_REV_RESOLVED`,
  `CITATION_DRIFT_BRANCH` (`:394-400`), replacing the single `CITATION_DRIFT_REVISION`
  line. Docstring revision-pinning section added at `:42-49`.
- Selftest: two new cases appended after the expected.json table (`:497-502`):
  `detached_head_default` (green, exit 0 — omitted --rev resolves `main` tip even
  though HEAD is an unbookmarked commit) and `detached_head_rev_head` (red, exit 2
  `head_not_branch_tip`). Both cases run the real CLI via
  `subprocess.run([sys.executable, __file__, ...], strict argv)` — the argv
  surface (argparse → resolve_rev → run_check), not a direct run_check call
  (`:545-558`) — and share one `detached_head` fixture built by plain git under
  `tempfile.mkdtemp()`: commit on `main`, `checkout --detach`, delete `TARGET.md`,
  off-branch commit (`build_fixture` `:447-455`). Fixtures `git init -b main`
  (`:431`) so the branch pin has a target. All 13 pre-existing cases keep their
  exits and their direct `run_check` path.

## Verification (observed)

`--selftest` — last line and exit:
```
CITATION_DRIFT_SELFTEST: CLEAN cases=15 passed=15 failed=0 exit=0
EXIT=0
```

Registered strict argv (SKILL.md:448) with
`--rev 9011581d84527ba34c675f9cf912e54d2e72d470`:

- pre-change bytes (`git show B:…` → `/tmp/citation-drift-probe-pre.py`):
  `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`, EXIT=0
- post-change working-tree bytes:
  `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`, EXIT=0

Exit parity holds (0 == 0); output adds the three rev fields, findings unchanged.

Other commands run:
- `git --version` → `git version 2.56.0` (supports `init -b`, used by fixtures)
- `git -C <lane> show B:.ufo/gates/citation-drift/citation-drift-probe.py > /tmp/citation-drift-probe-pre.py` (read-only)
- `git -C <lane> rev-parse --verify refs/heads/main^{commit}` → `9011581d…` and
  `rev-list --max-count=1 HEAD` → `9011581d…` (lane HEAD currently equals tip)
- `grep -n` on the edited file for report anchors

## Risks / notes

- [INFERENCE] `rev_resolved` is the resolved SHA for default/HEAD/evaluated revs;
  for an unresolvable explicit rev it echoes the requested string — chosen so
  `revision_unresolvable` keeps its exact pre-change shape.
- `run_check` gained a `branch` kwarg (default `main`) — the only in-file callers
  (selftest, main) updated; no external callers exist in the lane.
- `report` signature dropped its `rev` param; only `main` calls it.
- No installs; git/python3 stdlib only.
