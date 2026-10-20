# SimplifyC1Tools — YAGNI review of the round-20 C1 tool plan

Written 2026-10-20T17:51:48-03:00 (clock at write time). Read-only: no lane file changed except this report.
No tool was executed, no fixture built, no install made.

## State (OBS)

- Baseline `14f0260` is a commit; `refs/heads/main` = `d1d981d`. The delta `14f0260..main` is 6 files only
  (`claims.json`, `contract.md`, `evidence/carrier-guard/manual-arm.json`, `evidence/d1-residue-before.txt`,
  `gen-wave1.py`, `wave1-spec.json`). Every tool file cited below is byte-identical at both revs.
- `.ufo/waves/round-20/tools/` and `/verify/` do not exist yet (exit 2 from `ls`). This review is against the
  written plan (`contract.md` §Interfaces, `wave1-spec.json` item prompts), not against built code.
- The counter that will judge closures (`W20/tools/routed-r19.py`) is also unbuilt. "Does not weaken" is therefore
  argued against its **written** substance spec at `wave1-spec.json:15`, not measured.

## Axes

- **calibration** — one authority per census claim; every extra recorder is a future divergence point.
- **coverage** — each routed item keeps a named check plus its attack fixture.
- **depth** — retained checks still recompute from the measured revision's bytes.

**Answer in one line (OBS):** exactly one of the five planned C1 files — `final-census.py` — can be dropped
(its single census command merges into `verify.py`); no other file-level merge survives the controls; two
internal scope cuts are safe (`--allow`/`quoted:` in D2; the second command and 2 extra keys in D5's record).

## Verdict by interface item

| Item | Contract | Planned artifact | Verdict |
|---|---|---|---|
| D1 | `contract.md:38` | in-place patch `custody-pair.py` | **keep** — refusal + cleanup is the substance; no new file |
| D2 | `contract.md:41` | new `evidence-timestamps.py` | **keep tool, trim flags** (F2) |
| D3 | `contract.md:46` | new `carrier-guard.py` | **keep** (F3a) |
| D4 | `contract.md:53` | in-place patch `c1-census-v10.py` | **keep** |
| D5 | `contract.md:55` | new `final-census.py` (invented by task) | **merge into `verify.py` / drop the file** (F1) |
| D6a | `contract.md:56` | in-place patch `head-rev-lint.py` | **keep** |
| D6b | `contract.md:58` | new `revexec.py` | **keep** (F3b) |
| D6c–D6e | `contract.md:62-68` | in-place patches | **keep** |
| D6f | `contract.md:70` | in-place patch `jj-red-before.py` | **keep** |
| C2 | `contract.md:71` | new `verb-coverage.py` | **keep** (F3c) |
| C3 | `contract.md:76-82` | three tools | **out of scope** — `SimplifyC3Pipeline` owns that pipeline |

Plan shape: 5 new C1 files → **4** after F1; 7 in-place patches; no other file-level YAGNI move survives contact
with the controls.

## F1 — D5 producer: the only file-level deletion (OBS unless marked INF)

The contract fixes a **record**, not a tool: `contract.md:55` defines
`W20/verify/final-census.json` `{rev, argv, exit, stdout_path, stdout_sha256}` (5 keys). The task prompt invents a
tool with a wider job: `wave1-spec.json:70` asks for `final-census.py` that runs **two** commands
(`c1-census-v10.py --root LANE` **and** `sources-census.sh validate`) and records **7** keys
(`+ worktree_clean, + taken_at_utc`) as one singular `{argv, exit, stdout_path}`.

Every field and both commands already exist in the round-20 verifier this wave is also building — `VerifyR20`
is instructed to follow `W19/verify.py` as its pattern (`wave1-spec.json:150`):

- `W19/verify.py:207-233` — `Pass.run` records `{argv, exit, expected_exit, stdout_path, stdout_sha256,
  stderr_path, stderr_sha256}`; `:238-267` is the same for skipped rows; `:274, :301, :303` selftest the
  stdout-sha shape.
- `W19/verify.py:633` runs `c1-census-v10 --root LANE`; `:634-637` runs `sources-census census` and
  `sources-census validate` — the exact two commands.
- `W19/verify.py:757` records `source_revision`; `:764` records `worktree_dirty_tracked_at_start`.
- A produced artifact confirms the shape: `W19/verification.json:1856` (`source_revision: b26a6c4…`),
  `:1976` (`worktree_dirty_tracked_at_start: []`), `:1335` (`c1-census-v10` row with argv/exit/stdout_path/
  stdout_sha256), `:1377` (`sources-census` row, same shape).
- `SKILL.md:600` already registers `round19-verify` (gate/kaidoku) with its write scope; no new registry row is
  needed, only a write-scope addition.
- No spec item other than the recorder's own prompt calls `final-census.py`; the only other mentions are the
  record (`RoutedR19Tool`), the D5 prose (`ReviewVerifyScratch`) and the registry list (`ReviewSkillRegistry`,
  `wave1-spec.json:320`).

**Recommendation.** Add a narrow `verify.py --final-census OUT_DIR` mode; delete `W20/tools/final-census.py`
from the plan. The mode must, or D5's tree-delta check fails:

1. write **only** `final-census.json` and its census stdout — no `verification.json` rewrite, no `.stderr`
   sibling (D5 permits exactly the record + one stdout file);
2. emit exactly the contract's 5 keys — drop `worktree_clean`/`taken_at_utc` from the record; keep the dirty
   refusal as exit 2 behaviour (`wave1-spec.json:70`), not as a field;
3. run **one** command: the census gate. `sources-census validate` is already a separate recorded row
   (`W19/verify.py:636-637`); a singular record cannot represent two commands without an ambiguous `exit`.

**Cheaper variant (acceptable).** Drop the producer entirely and have the L1 write the 5-key record from the
census run with three shell commands. It costs reproducibility but not evidence: `routed-r19` D4 re-runs
`c1-census-v10` at REV from REV bytes over a `git archive REV` export (`wave1-spec.json:15`), so the record's
`exit` is never the counter's only source. That run uses the same gate bytes, so the *strength* of the census
still rests on `CensusRekey`'s anti-vacuity fixture, not on which file produced the record.

**Why this weakens no substance check.** D5's check (record consistency + tree delta) is unchanged; D4 still
recomputes the census at REV; no counter calls `final-census.py`; the record's key set is the contract's.
**Cost/tradeoff.** `SKILL.md:600` write scope must add `W20/verify/final-census.json` + stdout; a single mutant
in `verify.py` would now cover both records. That is not a new evidential loss: D4 executes the gate bytes at
REV independently of either recorder, and the gate's own strength is never attested by the recorder in either
design. [INF] the merged mode is ~35–45 lines incl. one selftest case; the planned tool (two command runners,
7-key record, mkdtemp repo fixture) would be ~100–140 lines.

## F2 — drop `--allow` and the `quoted:` heuristic from `evidence-timestamps.py`

- The contract CLI is `[--strict] [--selftest]` only (`contract.md:41`); `--allow` is not part of the fixed
  interface.
- `wave1-spec.json:25` self-cancels: “Ignore timestamps inside lines that are explicit quotations … only if marked
  `quoted:`? — no: report every finding; offer `--allow FILE:LINE` exemptions recorded in output.”
- No caller passes `--allow` (grep of all 100 prompts: only this prompt contains the token).
- An allowlist is a second place a finding can disappear; D2's defect is a wrong timestamp, and its fix is
  correct text, so the exemption surface has no legitimate use this round. Report every finding; drop both the
  flag and the quotation heuristic.

The tool itself is **not** redundant: no existing checker compares line timestamps with the introducing commit
(grep `future` across `W17`–`W19` Python finds only `from __future__`), and `routed-r19` D2 executes the file by
name.

## F3 — candidates examined and rejected

- **a) `carrier-guard.py` → `carrier-census.py`.** `carrier-census.py:7,26,85,171-176` records sha256/size/ELF only;
  `grep -c 'st_mode\|mode'` = 0. It has no mode/ctime transition and no state machine, so `arm/check/disarm` and
  the `exec_refused` fixture have no home there. Also, `controls-r20`'s edit list (`wave1-spec.json:145`) does
  **not** include `carrier-census.py`; merging would either violate the no-harm control or widen it. Keep.
- **b) `revexec.py` → `routed-r19.py` or `verify.py`.** `revexec` is the shared sandbox primitive; `routed-r19`'s
  own D6b self-check requires REV tools execute *only through* it (`wave1-spec.json:15`), and `measure`/`verify`
  need it too. Folding it into a caller would create a second sandbox authority. Keep. [INF] the three
  `write_outside_refused`/`net_refused`/`runs_ok` cases are the only evidence of the sandbox, so they must attach
  to the standalone file.
- **c) `verb-coverage.py` → `rea-catalog.py`.** `rea-catalog.py:62` emits `cli_commands: CLI_COMMAND_NAMES.length`
  only — no names — and it is a round-19 file outside the controls edit list. Duplicating the ~15-line node
  import is cheaper than mutating an immutable prior-round tool. Keep.
- **d) `routed-r19.py` → `controls-r20.py`.** `routed-r19` is the published C1 counting command
  (`claims.json:17`) and the only D1–D6 substance oracle; `controls-r20` runs a different `BASE SOURCE` contract
  (`wave1-spec.json:145`). Merging would change a published counting command. Keep two.
- **e) In-place patches (D1, D4, D6a, D6c–D6f).** They add zero files and their edits are already on the controls'
  named edit list (`wave1-spec.json:145`). No YAGNI action.

## Preserved contract

Interfaces `contract.md:38-70` are unchanged by F1/F2 **except** the D5 *producer*, which the contract never
fixed (only the record shape at `:55`). The record keeps its 5 keys; `routed-r19`'s D1–D6 checks, `measure.py`'s
`c3.first_failure_bound` (`claims.json:38`) and `verify.py`'s recording contract are untouched. C3's three fixed
CLIs (`contract.md:76-82`) are left to `SimplifyC3Pipeline`.

## Evidence (commands, exits)

1. `git rev-parse refs/heads/main` → `d1d981d2…` (0); `git cat-file -t 14f0260…` → `commit` (0);
   `git diff --stat 14f0260 refs/heads/main` → 6 files (0).
2. `ls .ufo/waves/round-20/tools .ufo/waves/round-20/verify/` → both “No such file” (2).
3. `grep -n "def \|census\|sha256\|stdout_path\|argv" .ufo/waves/round-19/verify.py` → :207 `def run`,
   :226-233 record fields, :633 census row, :634-640 census rows (0);
   `grep -n '"source_revision"\|"worktree_dirty_tracked_at_start"\|"commands": p.commands\|"baseline_revision"'
   .ufo/waves/round-19/verify.py` → :757, :764, :773, :756 (0).
4. `python3 -` (stdin script reading `W19/verification.json`) → `source_revision b26a6c4…`, dirty `[]`, and both
   census rows with argv/exit/expected_exit/stdout_path/stdout_sha256 (0); `grep -n` on the same file →
   :1335, :1377, :1500, :1526, :1856, :1976 (0).
5. `grep -n "future" W19/*.py W18/*.py W17/tools/*.py` → only `from __future__ import annotations` (0).
6. `grep -c 'st_mode\|mode' .ufo/waves/round-17/tools/carrier-census.py` → `0` (1: no match).
7. `grep -n '"name": "FinalCensusRecorder"\|"name": "ReviewSkillRegistry"'
   .ufo/waves/round-20/wave1-spec.json` → item :68, item :318 (0); their prompt lines are :70 and :320.
8. `wc -l W19/verify.py c1-census-v10.py carrier-census.py rea-catalog.py` → 820 / 742 / 329 / 420 (0).

## Limits

- Read-only review; nothing was run end-to-end, so the merged-mode line counts are [INF], not measured.
- `routed-r19.py` does not exist yet; “no weakening” is an argument against its written spec, not a test result.
- `refs/heads/main` moved past the declared baseline; anchors for `contract.md`/`wave1-spec.json` are at `d1d981d`,
  tool-file anchors at `14f0260` (the 6-file delta proves those bytes are identical).
