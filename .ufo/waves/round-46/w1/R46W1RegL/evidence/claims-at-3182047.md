# Round 46 claims — freeze

Lane `kaidoku`, round 46, attempt 1. Base `5382acc85f9d8617fe242fc116819b8055dfc4c7`
(`git -C kaidoku-shokunin rev-parse main` at claim time).

**Freeze** = the commit that first contains this file and `tools/round-46/` (a directory
pathspec). Receipts under `.ufo/waves/round-46/controls/` are not frozen: a do-nothing
control can only be scored against a freeze that already exists. The report cites it as
`plans/round-46-claims.md@<freeze>`; `git log --format=%H -1 -- plans/round-46-claims.md`
re-derives it. Nothing in this file or in `tools/round-46/` changes after the freeze: a
change makes both counters exit 2 `frozen_path_changed`.

Owned axes are all tied at 10 (`SCORECARD.md` `## Owned axes`), none retired, and a
capability last entered in round 43 — so the stagnation nudge does not waive the
lowest-axis obligation. Two claims on two distinct tied-lowest axes; coverage gets no
claim (this round adds no domain surface).

| claim | axis | surface |
|---|---|---|
| R46-C1 | depth | `SKILL.md` `## Queue-drain craft` rule block 23 — the freeze-integrity **discrimination** matrix — and its interpreter `tools/round-46/attest.py` |
| R46-C2 | calibration | the `SKILL.md` instrument registry, widened to the census of instruments the round-41..46 claim files name, bound to presence at the measured revision |

**Causal separability.** C1's counter reads the craft section, this file's frozen paths and
`tools/round-46/attest.py`; it never reads a registry row. C2's counter reads the census,
the marker-bound registry section and the presence of each named tool; it never reads block
23. Either lands and scores without the other. They share `tools/round-46/gate.py`, which is
frozen infrastructure, not a claimed surface: a shared prerequisite, not a shared claim.

**Why this round exists.** Round 45 landed both artefacts and reported
`met (instrument non-discriminating)`: the frozen predicates were met, but wave 1 showed
that a 44-line forged C1 artefact and a six-fenced-row C2 artefact each scored
`met_target: true` (`corpus/lessons/round-45.md` R45-CL13, R45-CL14). A measure that a
forgery satisfies is not a measure. Round 46 replaces the measure with one that scores its
own forgeable copies red, and the forgeable copies are built by mutating the landed bytes:
the battery cannot drift from the artefact it defends.

## R46-C1 — depth: the freeze-integrity matrix and a check that scores its own forgeries red

**Prior state.** `## Queue-drain craft` holds 22 rule blocks; block 22 is the round-45
freeze-integrity table, and its interpreter's eleven selftest cases are arm-covering but the
bindings that make it evidence are weak in six named ways (`R45-CL13` a–f): no sha256 pin
on the interpreter (a 4-line stub printing the selftest banner passes), citations accepted
with no line selector and off-topic, header cells matched by substring, the marker counted
once per block rather than by occurrence, the block count inflated by a column-zero
`- **…**` line inside a body, and a malformed heading crashing to exit 1 with empty stdout
instead of exit 2.

**Landed surface.** One new rule block in `## Queue-drain craft`, title beginning `23. `,
marker `<!-- freeze-integrity-table v2 -->` occurring exactly once in `SKILL.md`, the block
being the **last** craft block. Its table's header cells are exactly
`trigger | v1 hole | v2 arm | exit`, at least thirteen rows, every row exactly four cells,
every exit cell exactly one of `0`, `1`, `2`; every row's trigger names a routed
`R45-CL<n>` id and the thirteen ids R45-CL2, CL6, CL7, CL9, CL13, CL14, CL15, CL18, CL19,
CL20, CL22, CL23, CL24 each appear in some row; every row's arm cell names a token from the
fixed vocabulary (`commit`, `blob`, `restored`, `dirty`, `pathspec`, `merge`, `marker`,
`header`, `rows`, `refs`, `pin`, `battery`, `output`, `presence`); at least six citations
carry a line selector and resolve, each inside `corpus/lessons/`, `corpus/knowledge/`,
`plans/` or `tools/round-46/`, with `corpus/lessons/round-45.md` among them; the block cites
`S142` and carries `sha256:<64 hex>` equal to the sha256 of `tools/round-46/attest.py` at the
measured revision.

**Predicate (each clause is computed by `tools/round-46/attest.py --profile v2`).**

1. `marker_occurrences == 1`; `block_present == 1`; the marked block is the last craft block
   and its title starts with `23. `.
2. Header cells equal `["trigger", "v1 hole", "v2 arm", "exit"]` exactly.
3. `rows >= 13`; every row four cells; every exit cell in `{0,1,2}`.
4. The thirteen routed ids are all named; every arm cell is in the vocabulary.
5. `refs >= 6`, every reference carries a line selector (the pinned interpreter excepted —
   it is identified by its sha256), the path set is validated, and every reference resolves
   at `--rev`; `corpus/lessons/round-45.md` is cited.
6. The block cites `S142` and the sha256 pin matches the interpreter's bytes at `--rev`.
7. `battery.forgeries_total == 9`, `battery.v1_green == 9`, `battery.v2_green == 0`,
   `battery.genuine_green == 1`, `battery.v2_crash == 0`. The nine forgeries are this file's
   block 23 mutated one defect class at a time (`garbage-rows`, `thin-rows`, `lineless-refs`,
   `header-substring`, `two-markers`, `stub-pin`, `self-refs`, `missing-routed-id`,
   `no-vocab-arm`), each scored in a one-commit fixture repo.
8. `frozen_path_changed == []`, the frozen set derived from this file's `## Frozen paths`
   section, with the merge-aware history arm (`-m --diff-merges=first-parent`) and the
   independent blob arm.

**Target.** `failing == []`, counter exit 0.

**Counting command.**

```sh
python3 -I -B tools/round-46/attest.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze <FREEZE> --rev <REV> --json-out <OUT>
```

**Before — the do-nothing control and the discrimination gap.**

- `controls/ctl-c1-0-do-nothing.json`: at the freeze, exit 1 — `block_present 0`,
  `rows 0`, `marker_occurrences 0`. A do-nothing `SKILL.md` cannot reach the target.
- `controls/ctl-c1-1-v1-profile.json`: the nine forgery fixtures scored with
  `--profile v1` at the freeze, exit 0 with `forgeries_total 9`, `v1_green 9`. This is the
  round-45 clause set's hole, measured: every forgery the v2 check rejects is accepted by
  the check round 45 froze.
- Fidelity: `--spec r45 --profile v1` at `f59565b7`/`f762b727` reproduces the round-45
  receipt (`rule_blocks 22`, `block_present 1`, `rows 10`, `refs 8`, `unresolved []`,
  exit 0), so the v1 profile is a port and not a straw man (`controls/ctl-c1-fidelity.json`).

**Kill rule.** A copied block 22 relabelled `23. ` fails clause 1–4 (no routed ids, no
vocabulary). A 44-line artefact with garbage rows fails clause 4. A stub interpreter fails
clause 6. Two markers in one block fail clause 1. A line-less citation fails clause 5. A
`## Queue-drain craft` heading without its trailing space exits 2 (clause: malformed), never
1 with empty stdout.

## R46-C2 — calibration: the registry names the census instruments and proves each exists

**Prior state.** The registry section (`### Round-44/45 instrument registry`) carries six
rows — the instruments rounds 44 and 45 name. The lane's own claim files for rounds 41, 42
and 43 name 31 further instruments that compute their targets, and none has a row. The round
45 check also accepted a row naming a path that exists at no revision (`R45-CL2`), accepted
rows under any heading, in a fence or in an HTML comment, matched cell 0 by `re.search`,
never validated the header, and accepted any cell containing `0`, `1` and `2` (`R45-CL14`
a–d). That is a self-assessment whose gaps the lane's own record can expose: the calibration
axis measures exactly that mismatch.

**Scope.** `tools/round-46/census.json`, generated by `tools/round-46/census.py` and never
edited by hand: every path matching `tools/round-4[1-6]/**.{py,sh}` that is named in a
`plans/round-4[1-6]-claims.md` at `--rev`, restricted to paths that exist there. Named but
absent paths are reported in `named_but_absent` and do not enter the scope.

**Predicate (each clause is computed by `tools/round-46/registry.py --profile v2`).**

1. Exactly one `<!-- instrument-registry v2 -->` and one `<!-- /instrument-registry -->`,
   the close after the open. Rows register only between them, outside fenced blocks and
   outside HTML comments.
2. The section's header row equals the house schema exactly:
   `tool | gate or probe - purpose | verdict map (exit codes) | self-test command |
   pinned-value path | write scope | owner`.
3. For each census path, a row whose **cell 0 is exactly** the backticked path. `unregistered == []`.
4. That row's verdict-map cell enumerates `0=`, `1=`, `2=` (`thin == []`); a cell that merely
   mentions the digits is thin.
5. Every registered path exists at `--rev` — `absent_at_rev == []` (`R45-CL2`).
6. `battery.forgeries_total == 7`, `battery.v1_green == 7`, `battery.v2_green == 0`,
   `battery.genuine_green == 1`: seven forgery classes (fenced rows, rows moved outside the
   section, a cell-0 substring, a prose verdict-map cell, rows inside an HTML comment, a
   fenced good row shadowing a thin honest row, a non-house header), each built by mutating
   the landed section.
7. `frozen_path_changed == []`, frozen set derived from this file, merge-aware history arm.

**Target.** `unregistered == []`, `thin == []`, `absent_at_rev == []`, exit 0.

**Counting command.**

```sh
python3 -I -B tools/round-46/registry.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze <FREEZE> --rev <REV> --json-out <OUT>
```

**Before.** At the freeze the round-45 counter reports `scope_size 6`, `registered` = six,
`unregistered []` — i.e. 6 of the census's instruments named, and the census does not exist
yet. The v1 clause set scores all seven forgery classes green
(`controls/ctl-c2-1-v1-profile.json`), and would score a row naming a non-existent path green
(`controls/ctl-c2-2-ghost-tool.json`); both are the `R45-CL2`/`R45-CL14` holes, measured. The
fidelity receipt (`controls/ctl-c2-fidelity.json`, `--spec r45 --profile v1`) reproduces the
round-45 verdict on the round-45 artefact.

**Kill rule.** Appending N rows with correct first cells but paths that do not exist fails
clause 5 — row count cannot substitute for presence. Rows in a fence fail clause 1. A header
with three cells fails clause 2. `0 of 1, 2` in the verdict-map cell fails clause 4. A row
naming a suffix of a scope path fails clause 3 (exact equality).

## Frozen paths (exact)

- `plans/round-46-claims.md`
- `tools/round-46/` — a **directory** freeze: both counters derive this list from this
  section and use it for the history arm, the blob arm and the dirty scope, so the pathspec
  boundary of `R45-CL18` cannot exist here.

`SKILL.md` is the graded surface and is **not** frozen. `corpus/SOURCES.md`,
`corpus/lessons/round-46.md`, `LOG.md` and `SCORECARD.md` are record, not instrument.

## Freeze-integrity rule (both claims)

A score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path. The
history arm is `git log -m --diff-merges=first-parent --name-status -z` (`R45-CL6`: a merge's
own resolution edit is now visible), an independent blob arm compares `freeze:path` with
`rev:path`, and `restored` names a path the history arm saw and the blob arm finds clean. A
later restore does not un-block. A touch makes the counter exit 2 `frozen_path_changed` and
print no `met_target`. **Inherent limit, stated not claimed (`R45-CL19`):** a tamper+restore
committed and folded away with `git merge --squash` leaves nothing in the surviving history
for either arm to read; no table row claims otherwise.

## Satisfiability preflight (before any seat scores)

Every predicate clause is a value the claim's own instrument computes, and each was exercised
before this freeze: `attest.py --selftest` prints `cases=15 failures=0` with one red case per
clause (including the malformed-heading exit 2 and the frozen-touch exit 2), and
`registry.py --selftest` prints `cases=11 failures=0`. The control receipts under
`.ufo/waves/round-46/controls/` score the do-nothing freeze and the v1 profiles. No clause
asks for a value the instrument cannot derive; provenance is exact path equality plus a
sha256 pin, never "names a path".

## Sources

R46-C1 and R46-C2 cite one row opened this round, with its located quote in
`corpus/lessons/round-46.md` `## Gate`:

- **S142** `https://git-scm.com/docs/git-log` — `--diff-merges=first-parent` is the option
  that shows a merge's first-parent diff, which is the arm `R45-CL6` needed.

Existing rows `S140` (git-status porcelain) and `S141` (git-diff-tree `-z` name-status) stay
cited by block 22 and are unchanged.

## Round shape

Two v1 waves under `/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json`
(band 32–64 each): wave 1 verifies the frozen instruments, drafts the landing evidence, opens
the round's sources and attacks both predicates before data; wave 2 falsifies the landing
after data. Seat counts, role mix and dead seats come from
`.ufo/waves/round-46/<wave>-results.json` and are reported from there.
