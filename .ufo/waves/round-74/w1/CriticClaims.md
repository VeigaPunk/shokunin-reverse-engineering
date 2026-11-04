# CriticClaims — independent attacks

Axes: operability (C1), calibration (C2), provenance/control validity. No admission or judgment is made here.

## Method and exact run

Frozen source read with `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show b3a7e28089582ce5fb002a1b88e5295caf696b9f:<path>`, not mutable worktree imports. Probe SHA256: `81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039`.

Executed from the lane:

```sh
S=/fast/scratch/hyaku/kaidoku-r74/CriticClaims
trap 'rm -rf -- "$S"' EXIT
TMPDIR="$S" python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-74/w1/CriticClaims/harness.py
```

Independent harness, not the lane battery: exact-once replacements, five subprocesses concurrently, each `/usr/bin/python3 -I -B "$S/<name>.py" --selftest`; classify only parseable 20-case results with rc 0/no failures as surviving, rc 1/named failures as killed. Raw commands, outputs and cosmetic fixtures are in `CriticClaims/results.json`; four unified patches are alongside it. Scratch deleted by the completed shell's EXIT trap. No installs or repository mutations.

## C1: four NEW defect classes

These four changes are absent from frozen `probe-mutation.py` R74 entries (lines 98–146). Pristine: rc 0, 20 cases, failures [].

| Mutation / mechanism | Observed verdict | Classification / smallest safe correction |
|---|---|---|
| `home-truthy-not-boolean`: remove `is True` from genuine `home_under` conjunct, accepting truthy non-booleans | **SURVIVED**, rc 0, 20, [] | Next-round type-contract debt, not a falsification of the explicitly enumerated ten-mutant predicate. Add a case with `home_under: "false"` or `1`. Current kernel producer emits bool, so external-input exploitability is not demonstrated. |
| `last-named-sample`: replace `_name_samples` setdefault with assignment, letting a later same-shim sample erase the first | **SURVIVED**, rc 0, 20, [] | Next-round witness-selection debt. Add two same-shim samples with conflicting canary/key status and require the declared selection policy. Whether first-sample-only itself suffices is separate; do not represent this as all-sample coverage. |
| `double-forged-producer`: execute forged producer twice in `assemble_arm` | **KILLED**, rc 1, failure `a12-arm-wiring` | Attack refuted by existing exact order assertion (lines 1409–1414). No correction needed. |
| `lie-clean-keys-unchecked`: remove forged shim allowlist equality, retaining absence-of-canary check | **SURVIVED**, rc 0, 20, [] | Next-round conjunct debt. Add forged shim with wrong keys but `canary_present: false` while genuine/kernel witnesses otherwise satisfy the arm. |

Three named survivors demonstrate premature saturation if zero survivors is generalized beyond the frozen ten classes. They do NOT erase the bounded six-survivor closure. No claim that the original six survive was established.

## C2: cosmetic true atoms without routed repair

Harness executes the frozen atom functions with `show` substituted by the explicitly recorded synthetic document, not a committed-revision audit. All four returned `ok: true`. These are parser counterexamples, **not** an assertion that a landing document contains these defects or that the complete audit reaches zero.

1. **D10, real semantic binding gap (calibration):** `## Search log\nround 73 round 74 Identified\n` passes. No question, location, counts, exclusion or stop rationale exists. Routed defect 3 explicitly requires those fields (`round-73-verifier-spotcheck.md:124`). Atom lines 373–375 merely search three tokens; evidence contains the same two booleans, so it does not bound the missing content. Smallest correction: separately bounded per-round notes and explicit required fields/counts.
2. **D12, real directional gap (calibration):** `census erratum W04: 24 is correct; 23 is incorrect.` under the round-74 heading passes. It reverses the actual correction. Routed defect 5 specifies measured 23, not 24 (spot-check:126). Evidence only records section/marker presence, so provides no protection. Smallest correction: parse distinct reported=24 and measured=23 fields, bind measurement to its census receipt.
3. **D9, partly bounded (calibration/provenance):** a used-by cell `NOT used by corpus/knowledge/2026-11-04-r73-kernel-witness-record.md` passes substring matching. The atom does enforce S275's registry row and used-by column and exposes the exact cell and expected path in evidence: a wrong-column or absent-path attack is refuted, and an independent reader can detect the negation. But `ok` alone does not. A positive exact path-list grammar is the smallest correction. Merely adding the correct positive path is the actual bookkeeping repair, not cosmetic; independent truth of the entry's citation is outside this atom.
4. **D11, real reason/flip gap (calibration):** four 11-cell rows with required page tokens and status `rejected`, but empty final three cells, pass. Atom promises reason+flip; routed defect 4 requires both (spot-check:125). Evidence is only counts per page, not reason/flip content, so does not bound it. Smallest correction: check nonempty reason and flip cells, with page identity not arbitrary URL substring.

These are defects in the asserted binding of atoms to routed repairs; whether the strictly frozen numerical C2 predicate alone is met remains a separate question for the canonical judge. Do not mutate the frozen instrument to hide them; disclose boundaries and carry stronger atoms into a subsequent declaration.

## Controls: can a battery bug satisfy `c1_no_declared_cases`?

**Yes at the control acceptance boundary; no actual battery bug was demonstrated.** Frozen controls lines 109–117 trust battery verdict labels, do not require `pristine_ok`, do not check six renamed failure names, and require only four killed rows, not their identities. Harness extracts and executes the actual AST `met` expression with the six expected wrong-case names, four arbitrary killed names, and `pristine_ok: false`: observed **true**. This is an executable adverse-input counterexample to the guard, not a complete forged control run.

A scorer bug that misroutes six declared failures to `killed_wrong_case` independent of case renaming produces the same accepted projection. The control cannot discriminate that bug from successful name binding. Its evidence block exposes pristine_ok but does not enforce it or expose the actual failed case lists. Thus this is a fixable control-validity defect / next-round debt, not proof the actual four-arm receipt is false.

Smallest correction: require pristine_ok; require exact mutant identities and complete row set; for each of six rows require rc 1 and its expected `x-<case>` failure present, original declared case absent, and contrast against an unrenamed positive arm. Re-derive labels from raw results rather than trusting the same classifier being tested. C1's main frozen predicate independently requires pristine green and declared failures, so this control weakness alone does not defeat it.

## Evidence limitations / self-check

Only scoped attack runs above were exercised; no full landing audit, canonical judgment or lane integration. Synthetic atom/control inputs are clearly distinguished from real committed records. Accuracy 4 (no full landing determination); completeness 4 (control adversarial expression tested, not a full faulty-battery execution); clarity 4 (fixtures and limits explicit, report necessarily longer); actionability 4 (minimal corrections specified, frozen instruments intentionally untouched); conciseness 4 (four required attacks plus three evidence surfaces). Overall 4.0. Highest-impact improvement belongs to a newly declared atom/control instrument, not retrospective freeze changes.
