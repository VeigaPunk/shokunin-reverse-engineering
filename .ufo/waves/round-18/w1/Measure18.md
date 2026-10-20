# Measure18 — round-18 `measure.py`

Author-side advisory seat. Wrote exactly two files: `.ufo/waves/round-18/measure.py` and this
report. No other lane file touched; no jj or git write, no REA/Ghidra, no carrier executed;
no installs were needed (Python 3.14.8, git 2.56.0 already present).

Axes this move improves: **calibration** (each number names the artifact it came from and the
exact reason it is missing), **operability** (one command, pure JSON on stdout, named exit-2
reasons, cwd-independent), **depth** (C3 census plus per-label `all_match`).

## Deliverable

- `.ufo/waves/round-18/measure.py`: 914 lines, mode 755,
  sha256 `cf584a3eb024ff08409766e3d51267d86883eb527700a5d03e954175d972e6c6`.
- Usage: `python3 -I -B .ufo/waves/round-18/measure.py <revision>`; `--selftest`;
  optional `--root DIR` (default: `parents[3]` of the file, i.e. the lane root).

### What it measures (contract `.ufo/waves/round-18/contract.md:139-141`)

| claim | source read at REV | fields emitted |
|---|---|---|
| C1 | `.ufo/waves/round-18/tools/routed-defects.py` | `c1.open_count`, `c1.defects`, `c1.open_ids` |
| C2 | `.ufo/waves/round-18/tools/head-rev-lint.py` | `c2.live_count`, `c2.files_scanned`, `c2.fixture_count` |
| C3 | `.ufo/waves/round-18/runs/*/compare.json` | `c3.compare_jsons`, `c3.compare_jsons_with_extra`, `c3_all_match_by_label` |

The tree comes from one `git ls-tree -r` at the resolved commit; every blob from
`git show REV:path` (`measure.py:452-466`). The two tools are copied out of REV into
`tempfile.mkdtemp()` **together with every other `tools/*.py` blob**, then loaded with
`importlib.util.spec_from_file_location` only when present in that REV's tree
(`measure.py:115-135`, `measure.py:239-253`). Mirroring the sibling modules is what makes a
`head-rev-lint.py` that does `import revpin` load; `sys.path` and `sys.modules` are restored
and purged afterwards (`measure.py:137-151`). Temp root is removed in a `finally`
(`measure.py:463`).

### Named could-not-evaluate reasons (no guessing)

`tool_absent_at_rev`, `tool_blob_unreadable`, `tool_import_error: <Exc>: <msg>` (import-time
`SystemExit` included), `tool_has_no_callable_main`, `tool_raised: <Exc>: <msg>`,
`tool_output_not_json_object`, `tool_output_missing_open_count`,
`tool_output_missing_live_count`, `tool_exit_2` (and `tool_exit_<n>`),
`tool_rev_mismatch`, `compare_json_unparseable` / `compare_json_unreadable`.
The tool's own exit code and stderr tail are retained (`tool_exit`, `tool_stderr`,
`tool_output`), so a peer tool that fails at delivery is diagnosable from measure's output
alone.

## Decisions (all reversible, each with an anchor)

1. **Exit 0 whenever a report is emitted**, including claims that are
   `could-not-evaluate`; the top-level boolean `could_not_evaluate` carries that outcome
   (`measure.py:25-29`, `measure.py:482-484`, `measure.py:909-910`). Exit 2 is reserved for
   the measurement being impossible (`revision_unresolvable`, `revision_unreadable`,
   `lane_unresolvable`, `usage`). Observation: round-17's verifier expects exit 0 from
   measure at *both* the baseline and the source revision
   (`.ufo/waves/round-17/verify.py:178-179`). Inference: round-18's verify will mirror
   that. If the L1 instead wants exit 2 on any `could-not-evaluate`, the change is one line
   at `measure.py:910`.
2. **C3 counts only `fields[]` entries** whose `field` is exactly `extra.eof_reads` or
   `extra.analyzer_errors_empty` (`measure.py:61`, `measure.py:376-389`). That is the shape
   round-17's compare emits for extras (`.ufo/waves/round-17/tools/compare.py:176-199`), and
   the in-flight `CompareEofFields` edit of that tool emits exactly
   `fields.append({"field": "extra.analyzer_errors_empty", ...})` and
   `fields.append({"field": "extra.eof_reads", ...})` in the worktree
   (`.ufo/waves/round-17/tools/compare.py:203,209`, observation of uncommitted work; the REV
   pin will be whatever the L1 commits). A different producer shape is left uncounted rather
   than inferred, so a mismatch shows up as a low count instead of a silent false positive.
   `all_match` is copied per label, never re-derived (`measure.py:392-450`).
3. **The tool's echoed `rev` must equal the resolved commit** when present; otherwise
   `tool_rev_mismatch` (`measure.py:293-298`, `measure.py:349-354`). A count computed at a
   different commit is not a count at REV.
4. **In-process execution must not disturb measure's own streams.** Module *import* is
   redirected exactly like the CLI call (`measure.py:243-250`); without this a tool with a
   module-level `print` contaminated measure's JSON stdout — observed as a real defect in my
   first draft, fixed, and now pinned by red case K (`measure.py:864-874`). An import-time
   `SystemExit` is caught and reported rather than aborting the measurement
   (`measure.py:245-250`, red case J at `measure.py:849-861`).

## Evidence

### Selftest (`--selftest`, fixtures under `mkdtemp`, removed)

Exact last line and exit:

```
SELFTEST: CLEAN cases=68
exit=0
```

68 assertions across 11 fixture repositories: absent tools (A), both tools + sibling
`revpin` + two runs (B), non-JSON output (C), JSON then exit 2 (D), no `main`/`run` (E),
unparseable `compare.json` (F), unresolvable revision (G), later-commit tool must not leak
into an earlier REV (H), wrong-`rev` echo (I), import-time `SystemExit` (J), chatty import
must not reach measure's stdout (K).

Mutation checks that the suite can fail for the named reason (copies under `/tmp`, lane
untouched):

| mutation | observed |
|---|---|
| `found.add(item["field"])` → `pass` | `SELFTEST: FAILED cases=54 failures=['b_c3_extra', 'b_label_extra', 'b_label_extra_name', 'b_field_counts']`, exit 1 |
| `if rel not in paths:` → `if False:` | `SELFTEST: FAILED cases=54 failures=['a_c1_reason', 'a_c2_reason', 'h_first_absent', 'h_first_stable']`, exit 1 |
| delete the import-time redirect | `SELFTEST: FAILED cases=68 failures=['k_stdout_clean']`, exit 1 |
| first attempt: sed the literal `tool_output_not_json` | exit 0 — discarded: sed also rewrote the assertion. Lesson: mutate logic, not shared literals. |

### Baseline run (final bytes), exit 0, stderr 0 bytes

`python3 -I -B .ufo/waves/round-18/measure.py 9011581d84527ba34c675f9cf912e54d2e72d470`

```json
{
  "argv": [
    ".ufo/waves/round-18/measure.py",
    "9011581d84527ba34c675f9cf912e54d2e72d470"
  ],
  "c1": {
    "defects": null,
    "open_count": null,
    "open_ids": null,
    "reason": "tool_absent_at_rev",
    "status": "could-not-evaluate",
    "tool_exit": null,
    "tool_path": ".ufo/waves/round-18/tools/routed-defects.py",
    "tool_rev": null,
    "tool_stderr": null
  },
  "c1_open_count": null,
  "c2": {
    "files_scanned": null,
    "fixture_count": null,
    "live_count": null,
    "reason": "tool_absent_at_rev",
    "status": "could-not-evaluate",
    "tool_exit": null,
    "tool_path": ".ufo/waves/round-18/tools/head-rev-lint.py",
    "tool_rev": null,
    "tool_stderr": null
  },
  "c2_live_count": null,
  "c3": {
    "compare_jsons": 0,
    "compare_jsons_with_extra": 0,
    "extra_field_counts": {
      "extra.analyzer_errors_empty": 0,
      "extra.eof_reads": 0
    },
    "labels": {},
    "reason": null,
    "status": "evaluated",
    "unparseable": []
  },
  "c3_all_match_by_label": {},
  "c3_compare_jsons": 0,
  "c3_compare_jsons_with_extra": 0,
  "could_not_evaluate": true,
  "lane": "/home/vgpnk/Projects/shokunin/kaidoku-shokunin",
  "limits": [
    "C1/C2 copy the tools' own contract JSON at the measured revision; measure.py re-runs no defect check and no lint rule.",
    "C3 counts compare.json `fields[]` entries whose `field` is exactly one of the two names; it re-derives no all_match and re-reads no run log.",
    "C3 all_match is the value the artifact itself records, copied, not verified.",
    "C1/C2 require the tool's echoed `rev` to equal the resolved commit when it is present; a mismatch is could-not-evaluate because the count would not be at REV.",
    "A count of 0 is a measured zero (no matching artifact at that revision), not an error.",
    "Tools are imported from a temporary copy of the revision's bytes and run in-process against the resolved commit; the worktree is never read and no carrier binary is executed.",
    "Import-time and call-time Python stdout/stderr are captured; a tool that writes straight to the process file descriptors (an uncaptured child) is outside that capture."
  ],
  "revision": "9011581d84527ba34c675f9cf912e54d2e72d470",
  "revision_requested": "9011581d84527ba34c675f9cf912e54d2e72d470",
  "round": ".ufo/waves/round-18"
}
```

**Reading of the nulls (calibration, not a defect).** At `9011581` the whole
`.ufo/waves/round-18/` tree is untracked — `git ls-tree -r --name-only 9011581 --
.ufo/waves/round-18/` is empty, exit 0 — so both tools are absent *at that REV* and the
contract's rule (`.ufo/waves/round-18/contract.md:139-141` plus the "only when present at
REV" clause) makes `could-not-evaluate` correct. The C1/C2 "before" numbers (6 and 3) are
obtained by pointing the *delivered* tools at `--rev 9011581`; measure at the delivered
revision gives the "after" numbers. Case H proves measure reports a real count at a revision
where the tool exists and stays absent for an earlier revision in the same repository.

### Other commands (exact exits)

| exit | command (read-only unless noted) |
|---|---|
| 0 | `git rev-parse --verify refs/heads/main^{commit}` → `9011581d84527ba34c675f9cf912e54d2e72d470` |
| 0 | `git ls-tree -r --name-only 9011581 .ufo/waves/round-18/` → empty |
| 0 | `git ls-tree -r --name-only 9011581 .ufo/waves/round-18/runs/` → empty |
| 0 | `git ls-tree -r --name-only 9011581 .ufo/waves/round-18/measure.py` → empty |
| 0 | `ls .ufo/waves/round-18/`, `ls .ufo/waves/round-17/tools/`, `ls .ufo/waves/round-17/runs/` |
| 0 | `grep -n 'all_match\|extra_expectations' .ufo/waves/round-17/tools/compare.py` |
| 0 | `grep -rn 'measure.py' .ufo/waves/round-17/verify.py` (lines 178-179: expected exit 0) |
| 0 | `sed -n '1,3p' .ufo/waves/round-18/w1/DraftPinmapCorrection.md` (report style) |
| 0 | inline `python3 -I -c` test: `spec_from_file_location` on a `*-*.py` name + sibling import |
| 0 | `python3 -I -B -c 'import ast; ast.parse(open(...).read())'` → `ast_ok` |
| 0 | baseline run above (stdout pure JSON, stderr 0 bytes) |
| 0 | same run from `cwd=/tmp` → resolved lane correct (`cwd_independent`) |
| 2 | `measure.py` with no revision → `usage: measure.py <revision> \| --selftest` |
| 2 | `measure.py deadbeef…` → `revision_unresolvable` |
| 2 | `measure.py --root /tmp 9011581…` → `revision_unresolvable` (not a git repository) |
| 0 | `measure.py --help` |
| 0 | `git status --porcelain --untracked-files=all -- .ufo/waves/round-18/` (other seats' untracked files only) |
| 0 | post-run check: `leftovers=0` for `/tmp/measure18-tools-*` and `/tmp/measure-r18-selftest-*` |

## Risks / blockers

- **Integration shape of the two C1/C2 tools (inference, main residual risk).** They do not
  exist at any committed revision yet, so measure has only been exercised against
  contract-shaped stubs. measure accepts `main(argv=None)` or `run(argv=None)` (also a
  zero-argument `main()` reading `sys.argv`), invoked with `--root <abs lane> --rev
  <resolved sha>`, expecting one JSON object on stdout. Any other interface yields a named
  reason, never a fabricated count.
- **Producer shape of C3 (reduced risk).** The in-flight compare edit emits the two field
  names in `fields[]` exactly as measure expects (observed in the worktree, see decision 2).
  If a later edit switches to another shape, the count stays 0 by design and is visible as
  such; measure does not guess.
- **Sibling imports are mirrored only from `tools/*.py`.** If `head-rev-lint.py` imports a
  module stored outside `.ufo/waves/round-18/tools/`, the load fails as `tool_import_error`
  rather than importing lane code. The contract places `revpin.py` in `tools/`, so this is
  expected clean.
- **fd-level writes.** A tool that lets a child process write to fd 1/2 bypasses Python
  redirection; documented in `limits` (`measure.py:74-75`). The contract tools capture their
  `git` calls, so this is not expected.
- **Exit-code policy** (decision 1) must match the round-18 `verify.py` (`W18/verify.py`,
  owned elsewhere). If verify requires exit 2 for `could-not-evaluate`, change
  `measure.py:910`.
- Not measured by design: whether the C1/C2 tools' checks are themselves correct, whether a
  run's `all_match: true` is truthful, or any semantic carrier outcome. Those stay with the
  tools and the retained logs.
