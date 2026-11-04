# R86-C1 attack — ReviewerC1 (read-only)

Counter: `tools/round-86/record-agreement.py` (sha256 `99cb8f27cdfdf3bd…`, identical to the frozen
`pre/c1-at-base.json` instrument pin; selftest `SELFTEST cases=11 failures=0`).
Commands run from the lane root with `python3 -I -B`. Fixtures are `--worktree` trees built from BASE
bytes (`git show 2cf0b7ff:<path>`, read-only) with one edit each; the default rule and the
`--control substring-only` rule were both scored. Receipts: `receipts/<fixture>.default.json` and
`receipts/<fixture>.control.json`. Fixture generator: `receipts/fixture-driver.py` (rebuilds the trees
under a scratch dir; the trees were deleted before yield).

Command template, per fixture `F`:
`python3 -I -B tools/round-86/record-agreement.py --root F --worktree F --json-out receipts/<name>.default.json`

## Re-derivation of BASE (not a fixture)

`python3 -I -B tools/round-86/record-agreement.py --root . --rev 2cf0b7ff93c698809bed321f7338276a22d6beb9 --json-out receipts/base-rev-2cf0b7ff.json`
→ exit **1**, `RECORD_AGREEMENT agreed=0/3 mismatches=['A1-s303-supersede-count', 'A2-docstring-status', 'A3-receipt-pointer']`. Matches the frozen BASE.

Each BASE mismatch, as a reader sees it at 2cf0b7ff:

| atom | mismatch | visible defect at BASE |
|---|---|---|
| A1 | no row opens `supersedes S303` | S303 (`corpus/SOURCES.md:219`) says "already holds this URL in five scopes (S083/S090/S092/S119/S123)"; the URL also sits in S079 (line 85) and S080 (line 86), so 7 other rows carry it, not 5. No superseding row exists. |
| A2 | `inconclusive` ≠ code `survived` | `tools/round-84/mutation-closure.py:8` says "an absent declared case is inconclusive, never a pass"; the code's `elif not case_present:` branch (line 202–204) assigns `"survived"`. The docstring also says "survived" for the same case at line 12. |
| A3 | "expected exactly one `| coverage |` row, found 23" | **Not the defect the plan names.** `SCORECARD.md` has 23 lines starting `| coverage |`; row 23 (the current one, last cell `85 (…)`) names receipts at rounds 84, 76, 75, 68, 67. The newest named receipt is round 84 < 85, and no `.ufo/waves/round-85/l1/scores/` file exists at BASE. |

## Fixtures

Columns: **fixture** (`receipts/<name>.default.json`), **command** (template above), **exit**,
**mismatches** (default rule), **target atom** (verdict of the atom under test), **verdict**
(accepted/refused by the counter), **right answer?** (what the frozen rule and the claim say).

| fixture | exit | mismatches (default) | target atom | verdict | right answer? |
|---|---|---|---|---|---|
| `00-base-worktree` (BASE bytes; do-nothing control) | 1 | A1, A2, A3 | A1 F, A2 F, A3 F | refused ×3 | **yes** — same as `--rev` BASE |
| `01a-count7-ids-S001-S007` (superseding row, `count 7 (S001…S007)`) | 1 | A1, A2, A3 | A1 F | refused | **yes** — ids are not the URL rows |
| `01a-count6-correct-ids` (`count 6` with the 7 right ids) | 1 | A1, A2, A3 | A1 F | refused | **yes** — count mismatch |
| `01a-count7-with-S303-in-list` (`count 7 (…/S303)`) | 1 | A1, A2, A3 | A1 F | refused | **yes** — S303 is not a prior row |
| `01a-control-count7-correct-ids` (one added row, real ids) | 1 | A2, A3 | A1 **T** | accepted | **yes** — this is the claimed A1 work, done by one record edit |
| `01a-stale-earlier-wrong-row-plus-correct` (stale `count 3 (S083/S090/S119)` row above a correct row) | 1 | A2, A3 | A1 **T** | accepted | **no** — stale wrong count stays in the registry; only `sup[-1]` is read |
| `01d-indented3-correct` (correct row with 3-space indent) | 1 | A2, A3 | A1 **T** | accepted | yes (GFM allows ≤3 spaces) |
| `01d-wrapped-prose-row` (row inside a prose sentence) | 1 | A1, A2, A3 | A1 F | refused | yes — not a registry row |
| `01d-row-split-across-lines` (row wrapped mid-`ids`) | 1 | A1, A2, A3 | A1 F | refused | yes — the wrap truncates the id list |
| `01d-row-in-code-fence` (correct row inside a ``` fence) | 1 | A2, A3 | A1 **T** | accepted | **no** — a fenced example is not a registry row; the counter has no fence awareness |
| `02b-surviv-other-sentence` (extra "survivors…" sentence; absent-case sentence still says inconclusive) | 1 | A1, A2, A3 | A2 F | refused | yes |
| `02b-real-fix-survived` (absent-case sentence says "survivor") | 1 | A1, A3 | A2 **T** | accepted | yes — claimed A2 work, one record edit |
| `02b-split-sentence-verdict` ("an absent declared case is survived. Verdict on that case: inconclusive, never a pass") | 1 | A1, A3 | A2 **T** | accepted | **no** — the absent case gets two statuses; splitting on `.`/`:` hides the second |
| `02b-stem-substring-lint` ("an absent declared case is a survivability question, never a pass") | 1 | A1, A3 | A2 **T** | accepted | **no** — asserts no status; `"survi"` substring matches "survivability" |
| `02b-decoy-earlier-branch` (decoy `if not case_present:` → "inconclusive" inserted above the real `elif`) | 1 | A1, A3 | A2 **T** | accepted | **no** — hypothetical: BASE code has no earlier branch, but the counter takes the *first* `if not case_present:` in file order, so the real branch is not what it reads |
| `03c-receipt-rev-39hex` (round-86 receipt, rev 39 hex) | 1 | A1, A2, A3 | A3 F | refused | yes |
| `03c-receipt-rev-40hex-upper` (rev uppercase) | 1 | A1, A2, A3 | A3 F | refused | yes — regex is `[0-9a-f]{40}` |
| `03c-receipt-rev-40hex-lower-valid` (rev `b`×40) | 1 | A1, A2 | A3 **T** | accepted | yes by the frozen rule; weak: shape only |
| `03c-receipt-rev-zeros` (rev `0`×40) | 1 | A1, A2 | A3 **T** | accepted | **no** — rev is not checked against `--rev` or any commit |
| `03c-decoy-newest-round99-unrelated` (row names a valid round-86 receipt and an unrelated round-99 `ok:false` receipt) | 1 | A1, A2 | A3 **T** | accepted | **no** — `max(round)` picks the unrelated receipt; `ok` is never read |
| `03c-predates-round84` (round-85 row, round-84 receipt) | 1 | A1, A2, A3 | A3 F | refused | yes |
| `03e-two-coverage-rows` (two valid `| coverage |` rows) | 1 | A1, A2, A3 | A3 F | refused | right by the rule; the rule (exactly one row) is a card-layout property, not the claim |
| `03e-base-card-23-rows` (BASE SCORECARD) | 1 | A1, A2, A3 | A3 F | refused ("found 23") | right by the rule; **not** the defect the plan names (see BASE table) |
| `04-reach-row23-only-no-receipt` (row 23 repointed to a round-85 receipt that does not exist) | 1 | A1, A2, A3 | A3 F | refused | yes — a receipt file is required |
| `04-reach-minimal-no-history-touch` (row 23 repointed, receipt created, 22 history rows untouched) | 1 | A1, A2, A3 | A3 F | refused | yes by the rule; shows the 23-row card cannot pass A3 without history edits |
| `04-reach-delete-22-hist-rows` (22 history rows deleted, row 23 repointed, round-85 receipt `b`×40) | 1 | A1, A2 | A3 **T** | accepted | **no as a shortcut** — passes only by deleting history rows (not a record edit the claim names) |
| `04-reach-relabel-22-hist-rows` (22 history rows relabelled `coverage-hist`, row 23 repointed, round-85 receipt) | 1 | A1, A2 | A3 **T** | accepted | **no as a shortcut** — passes only by relabelling history rows |

Control arm (`--control substring-only`, receipts `*.control.json`): accepted **every** fixture,
including the BASE bytes (`mismatches []`, exit 0). That is the false green the plan requires
(`pre/c1-control-substring-at-base.json` reproduced). The control refuses nothing, so it is rejected as
a counter; it is not evidence against the default rule.

## Do-nothing control (plan item 3)

Is the target reachable by editing only the three records?

- **A1:** yes. One superseding row (`00`/`01a-control`) turns A1 green, and nothing else changes. This is the claimed work.
- **A2:** yes. One sentence edit (`02b-real-fix-survived`) turns A2 green. This is the claimed work.
- **A3:** no. The three-record edit cannot satisfy it. A3 needs (i) a round-85 `l1/scores/*.json` blob that does not exist at BASE (`04-reach-row23-only-no-receipt` refused), and (ii) the SCORECARD to carry exactly one `| coverage |` line, which means deleting or relabelling 22 history rows (`04-reach-minimal-no-history-touch` refused). Both (i) and (ii) pass the counter only with `04-reach-delete-…` / `04-reach-relabel-…`. (ii) is a history edit the claim does not name, so the "exactly one row" rule is mis-specified for a scorecard that accumulates rows. The counter also accepts a junk round-85 receipt (`03c-receipt-rev-zeros` pattern) without the coverage work.

So the do-nothing control holds (BASE 0/3 is not reachable from BASE by no-op), but the A3 target is reachable only by a shortcut the frozen rule permits.

## Lint vs re-derivation (plan item 4)

- **A1** is a re-derivation of the count and id set from the registry's `rea-agents-6.5.0.tgz` rows (`prior` is recomputed from the source column). Lint parts: `sup[-1]` only (earlier superseding rows unread); `count\s+(\d{1,3})` takes the first `count` integer and `int()` accepts `007`; the id list is every `S\d{3,}` after the count, anywhere in the cell; no fence/comment awareness; the row must match `^ {0,3}\|\s*S\d{3,}\s*\|`.
- **A2** is a re-derivation of the status (the code's `entry["status"]` in the first `if not case_present:` branch) plus a lint on the docstring: the sentence is found by `"absent declared case"` substring, split on `[.;:]`, and matched by `stem in sentence` (`"survi"`/`"incon"`) with a conflict list. The stem check is a substring lint, so "survivability" passes.
- **A3** is a **lint**, not a re-derivation. It derives nothing from the coverage figure or from the receipt's content: it checks exactly one row, a round integer, that a named receipt exists and parses, and that `rev` is 40 lowercase hex. It never reads `ok`, never compares `rev` to `--rev`, and picks the newest named receipt by round number.

## Where a wrong value still passes (plan item 4)

- A1: stale earlier superseding row (`01a-stale-…`); superseding row in a code fence (`01d-row-in-code-fence`); `count 007` formatting.
- A2: "Verdict on that case" split (`02b-split-sentence-verdict`); stem substring (`02b-stem-substring-lint`); first-branch read (`02b-decoy-earlier-branch`, hypothetical decoy).
- A3: rev not bound to `--rev` (`03c-receipt-rev-zeros`); unrelated newest receipt with `ok:false` (`03c-decoy-newest-round99-unrelated`); the exactly-one-row rule forces history edits (`04-reach-*`).

## Verdict on R86-C1

The counter is *failable* (refuses BASE, refuses the wrong-count, wrong-ids, 39-hex, uppercase-hex and predates fixtures) and the A1 and A2 targets are reachable by the claimed record edits. But A3 is not a re-derivation of the claimed record; its target is reachable through history edits or a junk receipt, and two wrong values pass on A2 and A1 by the splitter and fence paths above. Verdict: C1's counter can be fooled in ≥ 6 named ways; a clean "3/3 agreed" would not prove the records re-derive their bytes.

## Residual limits

- Fixtures ran in `--worktree` mode (disk reads, not `git show`). BASE parity was checked in `--rev` mode (`base-rev-2cf0b7ff.json`) and matched. No fixture exercised the `--rev` blob path, so "blob at --rev" is untested for fixtures.
- The decoy in `02b-decoy-earlier-branch` is synthetic; the real `tools/round-84/mutation-closure.py` has one `if not case_present` construct (`elif`, line 202). The decoy shows the counter's reading rule, not a present defect.
- The plan's BASE description of A3 ("names only a round-67 receipt") does not match the bytes: row 23 names rounds 84, 76, 75, 68 and 67 (max 84). The counter fails A3 on "found 23 rows", not on the receipt pointer. I cannot edit the frozen plan; flagged for L1.
- `--control substring-only` accepts every fixture, including BASE; it was scored as the cheap-rule control only.
- A3's `receipt_round` comparison uses the newest named path, so a row naming a higher-round receipt that is unrelated changes the verdict. Not exercised with a real coverage receipt.
- Scratch fixtures (`/fast/scratch/hyaku/kaidoku-r86/ReviewerC1/fx/`) were deleted at yield; `receipts/fixture-driver.py` regenerates them.
- No production file was edited; no VCS mutation; the counter was not modified.
