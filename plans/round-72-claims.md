# Round 72 — declared claims (frozen; no amendments after this file's container commit)

Base `56241b1c8baff95862730c008f1ae5132b03388e` (the round-71 lane tip: the report, the close
commit and the non-author spot-check lesson; the lane tree is clean and pushed). Three claims on
three distinct axes, causally separable — each is scored by its own instrument and none reads
another's result. All three are capability acquisitions in the AXES sense: the instrument runs, its
output verifies, and its row enters the SCORECARD capabilities table in the same round. The
stagnation nudge is in play: every owned axis sits at 10.0 (saturation line 10.0, window 10;
`SCORECARD.md`), so the lowest-axis obligation is waived and this round is a capability/frontier
move.

The round-71 non-author closure routed five defects (`.ufo/reports/round-71/kaidoku.md` §Routed
defects). This round's work is the lane's own queue from that report:
- routed defect 5 / the round-71 report's planned item (a): A10's binding verdict is bound to the
  checker's JSON, not a probe-side boolean → **R72-C2**;
- planned item (b): checker-mode children (`readelf`/`git`) inherit the caller environment →
  **R72-C1** (the round-71 frontier note's "checker-mode child environments" line);
- planned item (c): the raw-witness capsule audit as a checked instrument → **R72-C3**.
Routed defects 1–4 are record repairs carried below (report role count, the `c2-do-nothing`
citation, the container's supersession sha, the S274 column contract), not claims — bookkeeping
alone earns no claim slot.

## R72-C1 — coverage: the checker-mode children join the observed-environment class (Frontier → Core)

**Type.** Capability acquisition. The round-71 frontier note (`corpus/README.md`, `PROVINCE.md`
`## Round-71 additions to Core`) leaves "checker-mode child environments" Frontier; this round
moves it to Core for the measured route.

**Falsifiable before → after.** At the base the route's `--check-receipt` spawns `git` (the tool
blob) and `readelf` (each existing carrier's format) through `subprocess.run(...)`/`run(...)` with
no `env=`, so both inherit the caller's whole environment and no checker-mode child is recorded;
the round-71 probe has ten arms and none observes the checker path. After the round
`tools/round-72/packed-elf.py` runs every checker-mode child under `build_child_env()`, records
them into `--child-env-log`, and the checker JSON carries `checker_child_env`; the probe's new
A11 measures it two ways (a `git` and a `readelf` shim that dump their exact `/proc/self/environ`
bytes, and the checker's own capture log) with an exported canary in the caller's environment.

**Predicate (one sentence, frozen).** R72-C1 is verified iff the frozen seam probe, run at the
measured revision as `python3 -I -B tools/round-72/seam-probe.py --root . --rev <measured> --tool
tools/round-72/packed-elf.py --battery tools/round-72/mutation-check.py --pkg <REA 6.5.0 root>
--work <scratch> --receipt <route receipt> --expect-upx <pinned copy> --nonce-commitment
<pre-committed commitment> --json-out <receipt>`, reports `arms_passed 11` of `target 11` with
`A11_checker_env` true — both shims' key sets exactly HOME/LANG/PATH/TMPDIR, the canary key
absent, HOME and TMPDIR under the checker's run root, the checker's own `checker_child_env`
recording at least two records whose child census contains `git` and `readelf` — while the same
probe at the same revision against `--tool tools/round-71/packed-elf.py` reports 9 of 11 naming
`A10_run_binding` and `A11_checker_env` false, the A11 observation showing the shim's canary
present.

**Counting command.** The probe command above — exit 0 met, 1 each failed arm named with its
observation, 2 could-not-evaluate (unknown revision, missing host tool, bad argv).

**Kill rule.** Any arm false; a shim whose key set differs from the allowlist or that carries the
canary; a checker log missing the `git`/`readelf` classes; a base arm true; a post-freeze
instrument edit → not verified, reported, never narrowed.

**Do-nothing control.** `tools/round-72/controls.py` arm `c1_base_world` (the round-71 route at the
same revision: 9 of 11, A10/A11 false) and arm `c1_constant_probe` (an all-true arms receipt with
empty observations is rejected by `--validate`).

## R72-C2 — calibration: the A10 verdict is the checker's clause, and the self-mutant dies

**Type.** Capability acquisition (checker-emitted clauses + a selftest case that binds them) and
the repair of the round-71 wave's survivor i (MutReaders: `probe:471 binding_ok=True` survived
the probe's own test because the verdict was re-derived from the receipt's fields).

**Falsifiable before → after.** At the base the round-71 probe computes `binding_ok =
receipt["run_binding"] == want_binding`; the frozen battery's patch set `r71` applies
`binding_ok = True` and the probe's `--selftest` stays green (survivor count 1). After the round
the probe's verdict is `binding_verdict(checker JSON)` reading `clauses.run_nonce` /
`clauses.run_binding` (absent clauses fail closed), its `--selftest` carries
`a10-binding-from-checker` over a false-clause fixture, and the battery's `r72` patch set kills the
same mutation (`killed`, its failure naming that case).

**Predicate (one sentence, frozen).** R72-C2 is verified iff the frozen mutation battery, run at
the measured revision as `python3 -I -B tools/round-72/mutation-check.py --root . --rev <measured>
--tool tools/round-72/seam-probe.py --patch-set r72 --work <scratch> --json-out <receipt>`, exits 0
with the single `A10_binding_force_true` mutant `killed`, its `failed` list naming
`a10-binding-from-checker`, pristine selftest green, no wrong-case kill, and target pin matched —
while the same battery with `--patch-set r71 --rev b827a8b5d54f2885ec9be7786389f356c59226ce
--tool tools/round-71/seam-probe.py` reports `survivor_count 1` and survivors
`["A10_binding_force_true"]`; and the landing probe's A10 observation records
`genuine_verdict {present true, nonce_ok true, binding_ok true}` with `wrong_nonce.nonce_ok false`
and `broken_binding.binding_ok false` from the checker's JSON.

**Counting command.** The battery command above — exit 0 met, 1 each survivor/wrong-case kill
named, 2 could-not-evaluate (unknown revision, patch site absent or ambiguous, pristine not green,
bad argv).

**Kill rule.** A survivor; a kill via a case other than `a10-binding-from-checker`; a pristine
selftest not green; a target-pin mismatch; a post-freeze instrument edit → not verified, reported.

**Do-nothing control.** `tools/round-72/controls.py` arm `c2_base_survivor` (patch set `r71`:
survivor 1) and arm `c2_constant_survivors` (a mutation receipt claiming no survivors while a row
reads `survived` is rejected by `--validate`).

## R72-C3 — operability: the raw-witness capsule audit, and a lying summary cannot pass

**Type.** Capability acquisition (a standalone capsule reader composed into the receipt checker).

**Falsifiable before → after.** At the base the round-71 checker never reads the capsule behind a
receipt: a receipt whose `child_env_observed` claims `canary_present false` over a capsule that
carries a canary record is accepted (rc 0, `met true`, `failing []`, no clause object) — the
`c3_base_accepts` control. After the round `tools/round-72/capsule-audit.py` re-derives seven
clauses from the capsule bytes (digest, record count, exact key sets, canary, HOME, TMPDIR, child
census), rejects the seven tampered shapes cut from the committed 46-record round-71 capsule each
naming its clause, and `--check-receipt` audits a resolvable capsule (`--capsule`, or the
receipt's own `child_env_observed.log` under `--root`), so the round-72 lying receipt fails with
`receipt_capsule: canary`.

**Predicate (one sentence, frozen).** R72-C3 is verified iff the frozen capsule audit, run at the
measured revision as `python3 -I -B tools/round-72/capsule-audit.py --tamper-battery --capsule
.ufo/waves/round-71/l1/scores/c1-env-at-landing.jsonl --audit
.ufo/waves/round-71/l1/scores/c1-env-audit.json --work <scratch> --json-out <receipt>`, exits 0
with the genuine capsule accepted (`ok true`, 46 records, every clause true) and all seven
tampered shapes (`log_sha256`, `records`, `keys`, `canary`, `home_under_run`, `tmpdir_under_run`,
`children`) rejected each naming its declared clause — and the round-72 receipt checker on the
filed lying receipt (`--check-receipt <lying receipt> --capsule <polluted capsule>
--nonce-commitment <commitment>`) exits 1 with `receipt_capsule: canary` in `failing` and
`clauses.receipt_capsule false`, while the round-71 checker accepts the same lying receipt shaped
from its own genuine route receipt (`met true`, `failing []`).

**Counting command.** The audit command above — exit 0 met, 1 a shape accepted or a clause
unnamed, 2 could-not-evaluate (unreadable capsule or summary, no run root, bad argv).

**Kill rule.** The genuine capsule rejected; any shape accepted; any declared clause missing from
its shape's `failures`; the lying receipt accepted by the round-72 checker; a post-freeze
instrument edit → not verified, reported.

**Do-nothing control.** `tools/round-72/controls.py` arm `c3_base_accepts` (the round-71 checker
accepts the lying receipt; the audit rejects the same pair naming `canary`).

## Sourced claim

R72-C1 rests on a `corpus/SOURCES.md` row opened this round: the Linux `proc(5)` page's
`/proc/pid/environ` paragraph, which states that the file holds the initial environment set at
exec as NUL-separated `name=value` strings — the ground for measuring a child's environment at the
exec boundary from its own bytes rather than trusting a summary. Its row id, access date, located
quote and snapshot digest land in the round lesson `## Gate`; the knowledge entry
`corpus/knowledge/2026-11-04-r72-checker-env-capsule.md` cites it, and the container names
`claim_row: "S275"` (the next id after the registry's S274; confirmed against the duplicate-id
check before the append, and the append re-checks it).

## Frontier step (§2b)

`corpus/SOURCES.md` gains only rows opened this round; the census start/end receipts are committed
under `.ufo/waves/round-72/l1/`. One mistake is mined into `corpus/lessons/round-72.md
## Mistakes` — the round-71 instrument recorded every ROUTE child but no CHECKER child while its
docstring claimed "every child" (QUALITY row 121's clause extended to the mode), captured by the
new A11. No `considerthese/` directory exists in this lane; `Assimilation: none` (the
`merge/kaidoku/` package does not serve these claims).

## Repairs carried (not claims)

R72-G1 the round-71 report's role-count defect is corrected in this round's report (not by
rewriting it); R72-G2 the `c2-do-nothing` citation is corrected by citing the landing control
receipt; R72-G3 each round-72 `instrument_supersessions` entry, when one is needed, carries the
replacement sha256 (the round-71 container's entries carried none); R72-G4 the S274 column
contract is repaired as a new SOURCES row under rule 2 (reason in `teaches`, never an in-place
rewrite); R72-G5 the standing duties (sources census start/end, registry census, receipt audit,
no-`/tmp` scan) re-run; R72-G6 the wave-settlement receipt is written for this wave.

## Freeze mechanics

Instruments are committed before this plan's container (QUALITY #33): the declaration commit
carries `tools/round-72/{packed-elf,seam-probe,mutation-check,capsule-audit,capsule_audit,controls}.py`,
this plan, the pre-committed nonce commitment and the census-start receipt. The pre receipts
(`l1/pre/c1-at-base.json`, `c2-at-base.json`, `c3-at-base.json`, `controls-at-declaration.json`)
are measured at that state and committed before the container; the freeze commit is the first
commit adding `.ufo/waves/round-72/claims.json`, which pins the six instruments by sha256 and
holds the three predicate sentences byte-identical to this file.
