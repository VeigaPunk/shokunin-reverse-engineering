# ReviewerC2 — round 81 C2

Axes: calibration + depth. Review recommendation only; no promotion/admission, runtime routing, or domain-coverage claim.

## Findings by severity

### P2 — frozen counter success is weaker than the frozen claim

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-81/record-integration.py:75-80` checks only pristine exit zero and presence of a summary. It does not require summary cases >=11, failures zero, preservation of the old nine names, a pristine passing clean case, or a duplicate integration case. Thus a shorter selftest can satisfy its killed predicate while violating C2. This is a static predicate finding, not an executed fabricated candidate. Keep the instrument immutable: final review must independently inspect pristine 11/0, all nine retained names, and the two integration rows. L1 explicitly confirmed this supplemental review duty.

The same counter reads its binder from the measured revision (`:63-65`), recording a hash but not comparing it with the frozen round-80 hash. Final review must require `a5755ba1884f0c8d695d16289edbf5dff420e72d7552d424c2cc2df7bb94a438`; a reported digest alone does not establish unchanged dependency bytes.

### Resolved P2 — direct selftest dependency initially broke standalone layout

Initial candidate loaded only sibling `pointer-bind.py`, absent the canonical round-81 directory. L1 accepted the finding and executor corrected candidate `:275-278` to prefer the counter-supplied sibling, falling back to canonical `../round-80/pointer-bind.py`. I inspected the corrected lines. Executor's `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/ExecRecord/canonical-selftest.json` records canonical no-sibling invocation exit 0; no reviewer execution. This finding is resolved in the final candidate, digest `6bffdbc1c2f027c7b70cadfb70aabdf5ec6a9e3a6067484886d3560fad3efe3c`.

## Candidate implementation inspection

Initial exact `diff -u` against `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-80/strictness-battery.py` showed only the 55-line integration insertion after the existing nine cases. Final dependency correction adds two further lines. Definitions, scoring, validation and non-selftest CLI were unchanged in the inspected diff. Integration references below describe initial reviewed locations; final insertion shifts subsequent locations by two lines.

- Old `FakeModule.battery` at old battery `:201-208` reads `PROVINCE.md` from the worktree and counts `OMP` text. Its nine passing cases cannot establish committed-record integration. Recorded red control `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/pre/c2-base.json` reports pristine 9/0 and commit-omission mutant 9/0, survivors 1. These are existing recorded results, not rerun results.
- Real binder `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-80/pointer-bind.py:240-244` calls `git_show(root, rev, PROVINCE)` then `parse_record`; `:265-272` calls actual `bind` and `declared_ok`. Candidate does not replace these functions.
- Candidate `:278-299` redirects only `read_lines` to controlled in-memory lines and supplies a fixture Ghidra input. All five declared input paths resolve through that replacement; unknown paths return None rather than falling through to config access. State is restored in `finally :321-326`. No actual client configs were read by this review.
- Candidate `:301-320` creates clean and duplicate committed fixtures via unchanged `make_fixture_repo`, poisons worktree PROVINCE after commit, and calls real `battery(repo, 'HEAD', None)`. Clean requires 5/5, zero mismatches/unparsed, no duplicates, ok true; duplicate requires 6/6 and exactly omp-pin duplicate with ok false. This distinguishes semantic duplicate refusal from malformed-input refusal.
- Sole commit expression remains at candidate `:111-113`. Omitting it leaves HEAD without a committed PROVINCE. Real binder then raises its Unevaluable; candidate catches that at `:316-319`, appends the named clean failure, and reaches summary emission at `:328-333` rather than crashing [INFERENCE pending bounded receipt].
- Fixture root is asserted with `--show-toplevel` before add/commit (`:103-113`); counter scratch is a TemporaryDirectory under explicit --work and isolated HOME/TMPDIR (`record-integration.py:32-36,66-73`). Candidate uses existing TMPDIR-based selftest work path; with counter-provided absolute scratch this remains inside the assigned fixture tree.

## Kill rule boundaries

Counter `:75-78` rejects absent named clean row, duplicate named clean rows, a wrong-case-only failure, exit other than 1, or absent summary. A normal uncaught exception before output therefore cannot count. It does not authenticate arbitrary printed summaries or rule out a crash *after* printed output; honest candidate source review remains necessary. No evidence that this candidate forges output or substitutes logic was found.

## Opened source: included proposition and rejected alternative

SOURCE reuse: existing S255 at `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md:172`; no new SOURCE row written. Reopened https://git-scm.com/docs/git-show, DESCRIPTION: “For plain blobs, it shows the plain contents.”

Included evidence proposition (not a promotion): committed-blob observation is the appropriate integration boundary because actual binder `git_show` requests `HEAD:PROVINCE.md`; candidate deliberately makes mutable worktree bytes disagree with that object.

Rejected alternative: accepting a green FakeModule/worktree-only selftest as committed-record evidence. Reason: neither its byte reader nor the recorded omission control depends on a commit. Flip condition: real git-reader battery on the committed clean fixture must produce the named failure when the sole commit expression is omitted, while pristine remains clean; include the duplicate committed case and unchanged dependency digest.

## Residual risk and verification gaps

- No reviewer build/test sweep, candidate execution, fixture git mutation, scratch creation, installs, production edits, or git-state writes occurred. No scratch exists to clean up.
- Opened executor's `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-81/w1/ExecRecord/counter.json`: scratch fixture revision `def872d219d2681f580ff5b90fe19228b6db8d54`, final candidate digest above, expected binder digest, all original nine names retained, pristine exit 0 / 11 cases / zero failures; mutant exit 1 / 11 cases / two failures, exactly one named clean failure reporting PROVINCE absent at HEAD, summary present and stderr empty, mutants 1/killed 1/survivors 0. These are read executor receipts, not reviewer runs or integrated production evidence. Executor cleanup receipt reports scratch removed. L1 still owns integrated verification against its measured commit once.
- LSP device unavailable: `read xd://lsp` returned “No such tool.” Caller/definition review used explicit source ranges and exact diff instead; text inspection is not presented as semantic-server proof.
- Runtime identity/rerouting/saturation/resume paths are not changed by this assigned battery diff; no claims about those unrelated contracts.

Self-check: accuracy 4/5 (runtime outcomes attributed to opened executor receipts, not independent runs); completeness 4/5 (integrated measured commit verification belongs to L1); clarity/actionability/conciseness 4/5 (explicit remaining counter clauses and resolved dependency finding).
