# Round 70 — declared claims (frozen; no amendments after this file's container commit)

Base `5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d` (the carry-in commit that records the round-69
non-author closure before this declaration, the M69-7 ordering fix). Three claims on three
distinct axes, causally separable: each is scored by its own instrument and none reads another's
result. All three are capability acquisitions in the AXES sense — the instrument runs, its output
verifies, and its row enters the SCORECARD capabilities table in the same round. The stagnation
nudge is in play: every owned axis sits at 10.0 (saturation line 10.0, window 10; `SCORECARD.md`),
so the lowest-axis obligation is waived and this round is a capability/frontier move.

The instruments supersede the round-69 route (`tools/round-69/`, kept byte-identical at its own
round) under `tools/round-70/`: the route's scope is unchanged — detect a UPX-packed ELF, unpack
it with sha256 identity, recover the original's REA inventory — and round 70 closes the routed
round-69 defects M69-8 (counter shortcut), M69-9/S-1 (execute-before-hash seam), M69-10 (typed
preflight leaks) and M69-11 (/tmp HOME fallback, fixed-name scratch), and adds a fourth carrier
class: a statically linked executable.

## R70-C1 — calibration: the receipt readers are bound to their producers

**Type.** Capability acquisition (a provenance-bound receipt reader family) plus the repair of
the round-69 routed defect M69-8 (QUALITY #114 executed).

**Falsifiable before → after.** At the base the frozen round-69 readers accept fabricated
receipts: the wave's critic passed the C2 probe 6/6 and the C3 checker `met true` with invented
counts, a relabelled executable and a wrong ratio, and the round's own `c3-synthetic-met` control
passed the checker with no run at all. After the round the same forgery classes are rejected by
`tools/round-70/packed-elf.py --check-receipt` (each naming its clause) and by the hardened
`tools/round-70/contract-probe.py` receipt arms, while the genuine receipts still pass, and
`tools/round-70/mutation-check.py` enforces its target pin, its pristine floor and per-run
scratch dirs.

**Predicate (one sentence, frozen).** R70-C1 is verified iff the frozen forged-receipt battery,
run at the measured revision as `python3 -I -B tools/round-70/forged-receipts.py --root . --rev
<measured> --base-rev 5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d --tool
tools/round-70/packed-elf.py --base-tool tools/round-69/packed-elf.py --probe
tools/round-70/contract-probe.py --base-probe tools/round-69/contract-probe.py --base-probe-rev
5ee94c56ce7490938ee38c2e5c10930a1fd1330a --battery tools/round-70/mutation-check.py
--base-material .ufo/waves/round-69/l1/scores/c3-at-landing.json --landing-material
.ufo/waves/round-70/l1/scores/c3-at-landing.json --pkg <REA 6.5.0 root> --work <scratch>
--json-out <receipt>`, exits 0 with all ten forged shapes accepted by
tools/round-69/packed-elf.py --check-receipt at the base revision and rejected by
tools/round-70/packed-elf.py --check-receipt at the measured revision each naming its declared
clause (F1 rev, F2 instrument.sha256, F3 source, F4 before_ceiling_ratio, F5 orig_procedures, F6
packed, F7 carrier rows, F8 arm identity_ok missing, F9 unknown carrier id, F10 instrument
absent), the identity shapes (F1, F2, F3, F9, F10) also rejected by
tools/round-70/contract-probe.py with A5_carrier_record and A6_packer_pin false and accepted by
tools/round-69/contract-probe.py at revision 5ee94c56ce7490938ee38c2e5c10930a1fd1330a, the
genuine landing receipt accepted by both frozen readers, tools/round-70/mutation-check.py exiting
1 naming the target pin on a wrong --expect-target-sha256 and naming the pristine floor on
--min-pristine-cases 24, recording distinct work_dir values on two green runs, and --validate
rejecting a constant battery receipt with no mutant rows.

**Counting command.** The battery command above — exit 0 met, 1 the failing arms named, 2
could-not-evaluate; per-shape evidence in the receipt's `shapes` rows, the genuine arm in
`genuine`, the battery pins in `battery_arms`.

**Kill rule.** Any shape accepted by the frozen checker, any rejection whose `failing` does not
name the declared clause, a genuine receipt rejected, a wrong-pin or floor run exiting 0, equal
`work_dir` values, a constant receipt accepted by --validate, or a post-freeze instrument edit →
not verified, reported, never narrowed.

**Do-nothing control.** `controls.py` arm `c1-base-accepts-forged` (the base reader accepts a
wrong-rev shape cut from the round-69 receipt — acceptance is the base's status quo, never the
claim) and arm `c1-constant-battery` (a fabricated battery receipt with no mutant rows is
rejected by --validate); the battery's own `--selftest` wrong-world control shows the
base-acceptance assertion can fail (a 4-target receipt is rejected by the base reader for its
target clause).

## R70-C2 — operability: the packer seam is safe, typed and per-run

**Type.** Capability acquisition (the safe packer seam) plus the repair of the round-69 routed
defects M69-9/S-1, M69-10 and M69-11 (QUALITY #113 executed).

**Falsifiable before → after.** At the base the route executes the caller-supplied `--upx`
before hashing it (an impostor that prints the pinned version runs first), threads the module
constant through the carrier loop regardless of the validated path, inherits the caller's full
environment, turns an exec-format-less packer and a broken `node` into tracebacks or misleading
clauses, falls back to `/tmp` for HOME, and shares fixed-name scratch directories. After the
round the same seven scenarios are typed, ordered and isolated against
`tools/round-70/packed-elf.py`, and unchanged against `tools/round-69/packed-elf.py`.

**Predicate (one sentence, frozen).** R70-C2 is verified iff the frozen seam probe, run at the
measured revision as `python3 -I -B tools/round-70/seam-probe.py --root . --rev <measured> --tool
tools/round-70/packed-elf.py --battery tools/round-70/mutation-check.py --pkg <REA 6.5.0 root>
--work <scratch> --receipt .ufo/waves/round-70/l1/scores/c3-at-landing.json --expect-upx
<pinned-copy path> --json-out <receipt>`, reports `arms_passed 7` of `target 7` —
`A1_hash_before_exec`, `A2_threaded_path`, `A3_child_env_allowlist`, `A4_broken_node_typed`,
`A5_packer_exec_format`, `A6_home_no_tmp` and `A7_per_run_work` each true — while the same probe
against tools/round-69/packed-elf.py and tools/round-69/mutation-check.py at the base revision
`5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d` (with its own measured receipt and pinned-copy run)
reports `arms_passed 0` of 7 naming all seven arms.

**Counting command.** The seam-probe command above — exit 0 met, 1 each failed arm named with
its observation, 2 could-not-evaluate.

**Kill rule.** Any arm false; an A2 whose producer binding does not fail a forged receipt; a
base arm true; a post-freeze instrument edit → not verified, reported.

**Do-nothing control.** The base side of the same probe is the do-nothing control (0 of 7);
`controls.py` arms `c2-base-execformat-crash`, `c2-base-impostor-runs` (the defects are the
base's status quo) and `c2-new-refuses-unrun` (the claim's own property, positive control).

## R70-C3 — coverage: a statically linked executable joins the carriers

**Type.** Capability acquisition (a new carrier class in the route) — Frontier ground moved to
Core ("packed static binaries", named Frontier by the round-68 note).

**Falsifiable before → after.** At the base the route owns three carriers (two executables, one
shared object); PROVINCE's round-68 frontier note names packed static binaries as still Frontier,
and the base instrument's `CARRIERS` carries no static executable. After the round a fourth
pinned carrier of kind `static-exe` (`/usr/bin/docker-init`, sha256
`0bd49c8d4da5601ce955c24a515917c9a132404df633c1e2fa28855cc2e3e115`, measured 2026-11-04: 1268
procedures / 29 segments / 1111 strings original; 3 / 3 / 5 packed, ratio ceiling 10/1268 =
0.0079) is measured through the same route and the frozen checker binds it.

**Predicate (one sentence, frozen).** R70-C3 is verified iff the frozen receipt checker, run at
the measured revision as `python3 -I -B tools/round-70/packed-elf.py --check-receipt
.ufo/waves/round-70/l1/scores/c3-at-landing.json --root . --rev <measured>`, reports `met true`
with `target 4`, `carriers_matched 4`, `control_ok true`, `failing []`, every carrier's
`before_ceiling_ratio` at or below `0.75`, one carrier of kind `shared-object` (`libz`) and one
of kind `static-exe` (`dinit`), every carrier row bound to the frozen table and its declared
original procedure count, while the same checker over the round-69 receipt
`.ufo/waves/round-69/l1/scores/c3-at-landing.json` reports the producer-binding clause
(instrument.sha256 names tools/round-69/packed-elf.py bytes, not
tools/round-70/packed-elf.py) and `target 3 != 4`.

**Counting command.** The checker command above — exit 0 met, 1 each failing clause named, 2
unreadable or unresolvable revision.

**Kill rule.** A carrier arm false, a ceiling ratio above 0.75, no static-exe carrier, a
`target` other than 4, a receipt whose producer binding does not fail, or a post-freeze
instrument edit → not verified, reported.

**Do-nothing control.** `controls.py` arm `c3-base-three-carrier` (the base checker scores the
round-69 receipt met true at target 3 with no static kind — the world a do-nothing control
already holds) and arm `c3-new-rejects-old-receipt` (the frozen checker rejects the round-69
receipt on its producer binding — the binding is load-bearing).

## Repairs carried (not claims)

The round-69 non-author closure routed five defects; all five are closed or answered this round
under the round's LOG entry, never as claim input: R69-V1 (the carry-in commit precedes the
declaration — done, commit `5cc845ca`), R69-V2 (the lesson spot-check placeholder filled by an
appended erratum), R69-V3/M69-1 (the freeze container encoded as a top-level `instruments` map
with predicates in `claims`, audited by the round-29 gate before the freeze), R69-V4 (the
prefile receipt committed at the ticket tree before the report), and the standing duties re-run
(census start/end, registry-drift census, the halfway sweep, no `/tmp` fixtures).

## Frontier step (§2b)

`corpus/SOURCES.md` gains only rows opened this round (the lesson `## Gate` carries URL, access
date and a ≤25-word located quote). R70-C2's A3/A6 arms rest on the Python `subprocess`
environment-contract row opened this round (a new row: children inherit the parent environment
unless `env` is passed — the ground for the allowlist builder); at least one claim names it. One
mistake is mined into `corpus/lessons/round-70.md` `## Mistakes` (candidate recorded at design
time: the forged shapes must be cut from the base-world receipt — shapes cut from the round-70
four-carrier receipt would fail the base reader for the wrong reason, target 4 != 3, producing
a false before-arm; captured by the wrong-world control the battery's selftest now carries).
No `considerthese/` directory exists in this lane; `Assimilation: none` this round (the
`merge/kaidoku/` package themes do not serve these three claims; the frozen claims may not be
widened).
