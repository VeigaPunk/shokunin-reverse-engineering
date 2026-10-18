# CR2 — attack C2: `--rev` fix is not worth an operability claim

Seat: CR2 (critic). Window: arc2-loop1-round6. HEAD at run: `54bc9dd90b0aea67c345c1c6aa180e160164d151`. Scratch: none (probe reads Git objects; no fixture write). Custody not in scope (probe does not touch the five config paths). No repo edit except this report.

Axes used: (1) does the registered command's stated outcome change; (2) does `SKILL.md:348` actually require exit 2 for a dead rev; (3) blast radius (probe rc vs `--strict` rc vs `file_absent` vs registry digit); (4) any runnable caller.

## Verdict

**NOT WORTH A CLAIM. No-op on operability. Do not admit C2 on this fix.**

The patch is one predicate on one script, and it is real as a patch: `--rev deadbeef` today emits seven false `citation_file_absent` rows and exits 0. That is not an axis-move. The registered checklist already produces its stated outcome on every `<REV>` the entry names. Before and after on that observable are identical (`reported findings=0 exit=0`). A claim whose success condition is "all other behaviors byte-stable" has measured no improvement. Scoring operability `improved` would be a false admit (`AXES.md` working-the-axes: a claim verifies only as a falsifiable improvement; unchanged on the axis means the claim did not verify).

Keep the r5 sentence as **named instrument debt**, or discharge it with an append-only gloss correction. Do not spend the round's operability slot here. If a parent lands the preflight anyway, the axis verdict is **unchanged**, and the claim does not verify.

## Evidence

### Observation — this seat, cwd repo, 2026-10-18

```text
$ git rev-parse HEAD
54bc9dd90b0aea67c345c1c6aa180e160164d151

$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev deadbeef \
    --table .ufo/gates/citation-drift/pointer-table.json \
    --expected .ufo/gates/citation-drift/expected.json
CITATION_DRIFT_VERDICT: reported findings=7 exit=0
PROBE_RC=0
# seven rows, all citation_file_absent "absent at deadbeef"
# (SCORECARD.md, PROVINCE.md, round3 config-pre-pair.txt,
#  two corpus/knowledge files, SKILL.md, LOG.md)

$ python3 … --rev deadbeef --strict
CITATION_DRIFT_VERDICT: failed findings=7 exit=1
STRICT_RC=1

$ python3 … --rev HEAD
CITATION_DRIFT_VERDICT: reported findings=0 exit=0
HEAD_RC=0

$ git rev-parse --verify --quiet deadbeef ; echo VERIFY_SHORT=$?
VERIFY_SHORT=1
$ git rev-parse --verify --quiet 'deadbeef^{commit}' ; echo VERIFY_COMMIT=$?
VERIFY_COMMIT=1

$ ROOT=$(git rev-list --max-parents=0 HEAD | head -1) ; echo ROOT=$ROOT
ROOT=b3669e60f6dee601bab48cf152455cbf224e32d3
$ python3 … --rev "$ROOT" | tail -3
CITATION_DRIFT: citation_dead entry=skill-registry-row …
CITATION_DRIFT: citation_out_of_range entry=log1005-quoted-claim …
CITATION_DRIFT_VERDICT: reported findings=8 exit=0
ROOT_RC=0
```

A resolvable non-HEAD rev is graded and reported at rc 0. A dead rev is the same outer code. The difference is finding text, not a missing tool.

### Observation — contract text does not say what the claim says it says

- Registry row, verbatim map: "probe semantics: 0 reported (drift is reported, never failed) and 2 could-not-evaluate; `--strict` restores the gate map 0 clean / 1 failed / 2 could-not-evaluate". Self-invocation cell: "10 isolated-fixture cases". No sentence assigns an unresolvable `--rev` to exit 2. `SKILL.md:348`.
- Probe kind: "A tool that cannot fail is a probe, and is registered as one." `PROTOCOL.md:363-364` (fleet protocol, read-only). Exit 2 is a declared extra code for gates (`PROTOCOL.md:365-366`), not a rule that every bad input must be exit 2.
- Implemented CNE ids: `snapshot_tampered`, `snapshot_missing`, `pointer_table_unreadable`, `unpinned_legacy`, `root_unreadable`, `internal_error`. `citation_file_absent` is not in that set. `.ufo/gates/citation-drift/citation-drift-probe.py:69-78`.
- `root_ok` checks the work tree only (`:255-266`). `git_show` maps any nonzero `git show REV:path` to `"absent at %s"` (`:91-96`). `Tree.lines` files `citation_file_absent` (`:122-125`). Non-strict non-CNE returns 0 (`:77-78`).
- Selftest table has 10 cases and no absent-revision case. `.ufo/gates/citation-drift/expected.json:14-24`. `file_absent` expects exit 1 / `citation_file_absent` (`expected.json:18`) — that path must stay if anything is patched.
- r5 named the gap and called it debt, not a falsified measurement: `SCORECARD.md:965-966`, carried `:1017`. Same-round critic already said not a false-clean: `.ufo/waves/arc2-loop1-round5/CR7.md:115`.
- Caller sweep: no `*.py` / `*.sh` in this repo invokes `citation-drift-probe`. The entry is the registry command itself (`SKILL.md:348`). Recorded operational runs pass a real commit (`HEAD`, `265e1aa`, `0e8c96b`, `54bc9dd`).

### Inference — steelman the no-op (this is the attack)

1. **The observable does not move.** Operability's signal is a checklist item that runs and produces the stated outcome (`AXES.md` six-axes table). The stated outcome of `--rev <REV>` on a real revision is already `reported findings=0 exit=0` at `54bc9dd`. The claim's own clause "all other behaviors byte-stable" is an admission that the fleet surface does not change.
2. **Dead rev is already inside the declared exit set.** Probe exits are {0, 2}. Observed dead-rev exit is 0, with findings printed. "Registry requires exit 2" is a gloss at `SCORECARD.md:965-966`, restated by this round's brief, not a sentence in `SKILL.md:348`. Matching a gloss is not repairing a broken command.
3. **Not a false-clean.** `findings=7` is on the verdict line. An rc-only consumer already cannot tell HEAD-clean (`findings=0`) from a real historical grade (`b3669e60`, `findings=8`, rc 0). That conflation is the probe contract (`PROTOCOL.md:363-364`: a probe cannot fail on the graded surface). Fixing only `deadbeef` does not fix rc-only consumption.
4. **No caller, so no runnable gap.** Zero in-repo scripts. Auditors invented the input as a negative control. A claim that defines an input the registry does not name, then "improves" that input, is circular.
5. **The claim is not one behavior.** Probe dead-rev is rc 0; `--strict` dead-rev is rc 1. Putting a new id in the CNE tuple (the only way both maps yield exit 2) changes strict 1→2 as well. "Instead of reporting findings at rc 0" plus "all other behaviors byte-stable" cannot both hold. A probe-only special case would leave `--strict` at `failed/1`, which is the map the claim cites as the thing being repaired.
6. **Selftest +1 is not one tool.** `SKILL.md:348` pins "10 isolated-fixture cases". Gaining the case without editing that digit leaves a false registry count (freshness/calibration harm — a round may not harm an axis). Editing the digit is a second artifact. Either the claim harms a sibling statement or it is not "one behavior on one tool."
7. **Cheaper faithful move already exists.** r5 dispositioned this as instrument debt and said not to call it a false-clean. An append-only correction that the registry map does not assign unresolvable `--rev` to exit 2 discharges the gloss. The code patch does not discharge the real probe-exempt debt (frozen-run table digest, `SCORECARD.md:924-925`).

### Unknown

- Whether any out-of-repo wrapper keys only on rc. None is in this repo. Not assumed.
- Full finding-id histogram at `b3669e60` (this seat kept the tail only). Not needed: the verdict line `findings=8 exit=0` is enough to show a resolvable rev is graded.

## If a patch lands anyway (harm bound, not a recommendation)

Only a preflight `git rev-parse --verify --quiet <rev>^{commit}` before the table loop, one new CNE id, return without grading. Do not treat nonzero `git show` as CNE — that collapses `file_absent` (selftest exit 1, `expected.json:18`) and would harm the tool. Do not retarget `entry["rev"]` (`citation-drift-probe.py:220-222`); that is a different mechanism and unused by the committed table. Update the self-invocation digit in the same landing or do not add the case. Score the axis **unchanged**. Do not enter a capability row (the probe already entered at arc2-loop1-round4, `SCORECARD.md:917-918`).

## Verbatim-landable

```markdown
C2 operability — NOT VERIFIED, axis unchanged (CR2). The `--rev` preflight is one predicate on one script and is not an axis-move. At `54bc9dd` the registered command `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root . --rev HEAD --table .ufo/gates/citation-drift/pointer-table.json --expected .ufo/gates/citation-drift/expected.json` already returns `reported findings=0 exit=0`. `--rev deadbeef` returns `reported findings=7 exit=0` (seven `citation_file_absent`); `--strict` on that rev returns `failed findings=7 exit=1`. That exit 0 is inside the registry's probe set {0 reported, 2 could-not-evaluate} (`SKILL.md:348`); the row never says an unresolvable `--rev` is exit 2. `SCORECARD.md:965-966` is a gloss, not a contract sentence. No in-repo `*.py`/`*.sh` calls the probe. A resolvable root commit `b3669e60` grades at `findings=8 exit=0`, so rc 0 is the probe contract, not a missed CNE. Adding a selftest case without changing the "10 isolated-fixture cases" cell harms the registry row; changing the cell means the claim is not one tool. Disposition: keep named instrument debt (carried `SCORECARD.md:1017`); do not score operability improved; do not admit the round on this claim. A later patch, if any, is `git rev-parse --verify <rev>^{commit}` only — never "any git-show failure is CNE" — and still does not move the axis.
```

Labels: command blocks and path:line quotes above are **observation**. The no-op steelman and the "do not admit" verdict are **inference**. Out-of-repo rc-only wrappers are **unknown**.
