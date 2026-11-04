# Round 77 — declared claims (frozen; no amendments after this file's container commit)

Base `188562d43e3cc58b217ad7aa763fb296c5b8a0b7` (the round-76 lane tip: the round-76 verifier
spot-check lesson; lane tree clean and pushed at `local == remote == ahead=0`).
Two claims on two distinct axes, causally separable — each is scored by its own instrument, and
neither reads the other's result: C1 reads the record's annotation cells and the receipts they
name; C2 runs the prefile gate and the receipts that retain it. Both are capability acquisitions
in the AXES sense: the instrument runs, its output verifies, and its row enters the SCORECARD
capabilities table in the same round.

**Lowest-axis obligation.** The lane's three owned proxies (coverage/depth/calibration) sit at
10.0 behind different proxies; the stagnation nudge's waiver is *not* met (capability rows entered
in rounds 73–76, inside the 10-round window), so no waiver is claimed. **`lowest-axis:
calibration`** — R77-C1 works a tied-lowest axis.

**Population.** The round-76 non-author spot-check (`corpus/lessons/round-76-verifier-spotcheck.md`
§6) routed five defects to this round. Disposition:

- routed defect 5 (D24 checks that the path resolves, not the verdict beside it) → **R77-C1**;
- routed defects 3 (gate receipts carry no exit) and 4 (the prefile check retains no receipt) →
  **R77-C2**;
- routed defects 1 (the landing receipt cited as green in three files) and 2 (tip-receipt revision
  prose in the filed report) are record corrections, carried **unclaimed**, closed by an appended
  correction section and by the same edited cells R77-C1's instrument must pass — never by
  rewriting filed round reports.

## R77-C1 — calibration: a claimed verdict is re-derived from the receipt it names

**Type.** Capability acquisition. Round 76's D24 atom admits a row whose evidence cell carries a
false verdict beside a resolving path: the `## Capabilities` row `capability-row binding` said
`c1-at-landing.json (D24 true, mismatch_count 0)` while that receipt records `exit 1`,
`mismatch_count 1` and `D24_capability_rows false` (the two evidence paths it names first appear in
the commit it measures). D24 reads the path and never the annotation.

**Surface.** The record's annotation cells — frozen scope: the SCORECARD `## Capabilities` table's
data rows whose first-working-round numeral is `>= 73`, plus the PROVINCE `- **Core — ` bullets.
The instrument parses every parenthesised annotation with a closed, declared grammar (typed
`field literal`, `field N of M`, `N mismatches`, `N survivors`, `N|word atoms`, `pristine N`,
`validate defect-free`, atom-id shorthand) and re-derives each bound clause from the JSON receipt
the cell names at the measured revision. Unparsable clauses are reported as unbound, never
guessed; a field the receipt lacks is unbound, never a pass.

**Predicate (one sentence, frozen).** R77-C1 is verified iff
`python3 -I -B tools/round-77/verdict-bind.py --root . --rev <measured> --json-out <receipt>` exits
0 with `mismatch_count 0`, `population.bound_clauses >= 18`,
`population.in_scope_rows >= 11` and a defect-free `validate`, every bound clause re-derived from
the JSON receipt its cell names, while the same command at base `188562d4` exits 1 with
`mismatch_count 4` naming exactly the `capability-row binding` row and PROVINCE.md line 585
(`D24 true` vs `false`, `mismatch_count 0` vs `1`), and the selftest's 15 cases carry one red
fixture per failure shape plus their legitimate look-alikes.

**Counting command.** `mismatch_count` is the counter; the machine block below is the command the
prefile/plan-command gate executes.

<!-- counting-command: C1 -->
```sh
python3 -I -B tools/round-77/verdict-bind.py --root . --rev $REV --json-out $OUT
```
<!-- /counting-command -->

**Kill rule.** An annotation that passes because the grammar cannot see it (a negated cell, a
clause outside the group, a path from another cell); a bound clause whose receipt field is absent
and is treated as a pass; a `validate` defect; a target reached by an instrument whose
`bound_clauses` floor is met by prose; a `mismatch_count` that falls only because in-scope rows
were removed; an edited cell that keeps the false value; an evidence pointer that does not resolve
at the measured revision → not verified, reported, never narrowed.

**Do-nothing controls (scored before data).**
- `ctl-no-binding`: the instrument copy with `parse_clause` forced to return `None` — 0 bound,
  0 defects at base: the target's `bound_clauses >= 18` floor is what this control cannot reach.
- `ctl-all-false`: the instrument copy with `bind` forced to return `False` — every clause a
  defect at both arms, so the landing target is unreachable by blanket failure.
- `ctl-pointer-only`: round 76's own `tools/round-76/record-audit.py --rev 188562d4` — the D24
  atom is true and the audit reports 0 mismatches while the false annotation stands: the prior
  green record is exactly the defect.

## R77-C2 — operability: the prefile gate retains a receipt that binds its exit and revision

**Type.** Capability acquisition. The round-29 prefile gate prints PASS/FAIL and exits 0/1, but
round 76's filing retained no output (routed defect 4) and its `gate-at-tip.txt` carried a
disclosures block without the wrapper's exit (routed defect 3): a verdict the next reader cannot
re-check.

**Surface.** The filing gate invocation and the evidence it leaves: `tools/round-77/prefile-receipt.py`
runs `tools/round-29/prefile-check.sh` as a child under a four-key environment (PATH, HOME,
TMPDIR, LANG) inside a private work root and writes a receipt binding argv, revision, exit, the
`prefile: ` verdict line and the stdout digest; `--check-receipt` re-derives every clause from the
receipt bytes alone.

**Predicate (one sentence, frozen).** R77-C2 is verified iff
`python3 -I -B tools/round-77/prefile-receipt.py --root . --rev <measured> --work <scratch>
--battery --json-out <receipt>` exits 0 with `arms_ok 6`, `arms_total 6`, `ok true` and a
defect-free `validate`, each arm carrying its expected observation (clone-run a clean clone run
whose receipt passes `--check-receipt`; record-receipt the filing receipt at exit 0; gate-exits
every gate receipt in the newest round dir carrying its exit; red-no-exit, red-verdict and red-rev
each refused), while the same command at base `188562d4` exits 1 with `arms_ok 4` (the filing
receipt absent and three round-76 gate receipts without exit), and the selftest's 13 cases carry
both red fixtures and their legitimate look-alikes.

**Counting command.** `arms_ok` is the counter; the machine block below is the command the
prefile/plan-command gate executes.

<!-- counting-command: C2 -->
```sh
python3 -I -B tools/round-77/prefile-receipt.py --root . --rev $REV --work $WORK --battery --json-out $OUT
```
<!-- /counting-command -->

**Kill rule.** An arm met for a reason other than its expected observation; a receipt accepted
whose `exit` is not an integer or whose digest does not cover its stdout; a `passed` that does not
follow from `exit` and the verdict line; a `gate-exits` arm that passes with an empty gate set; a
red fixture that is accepted; a filing receipt whose rev is not the filing revision → not
verified, reported, never narrowed.

**Do-nothing controls (scored before data).**
- `ctl-gate-alone`: run `prefile-check.sh` on a clean clone at base exactly as round 76 ran it —
  it prints PASS and exits 0, and the battery's `record-receipt` arm stays unmet because no receipt
  was retained: the prior practice reaches 4 of 6 arms, never the target.
- `ctl-forged-arms`: a battery receipt with `arms_ok` set to the arm count while an arm row says
  `met false` — `battery_defects` refuses it (selftest `red-battery-ok`).

## Causal separability

C1's counter reads SCORECARD/PROVINCE annotation cells and their receipts; C2's counter runs the
prefile gate and reads prefile/gate receipts. Neither counter reads the other's value, and each
lands without the other: C1 passes with round-76's gate receipts unchanged (C1's scope is the
annotation cells, not `gate-*.txt`), and C2 passes with the false annotation in place (its arms
read the filing receipt and the gate receipts' exit keys, not the annotation cells).

## Instruments (pinned at the freeze commit)

| path | role |
|---|---|
| `tools/round-77/verdict-bind.py` | C1 counter, 15-case selftest, frozen `PREDICATE` |
| `tools/round-77/prefile-receipt.py` | C2 counter + `--check-receipt` + `--filing`, 13-case selftest, frozen `PREDICATE` |

Both were committed (with this plan and the census-start receipt) **before** any claim data in
`.ufo/waves/round-77/pre/`; the freeze commit is the first commit adding `.ufo/waves/round-77/claims.json`.
