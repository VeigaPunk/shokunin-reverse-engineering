# ConnectorCross — round 68 wave 1 (connector seat): sibling-overlap scan

Lane `kaidoku-shokunin`, read-only on the lane and on the fleet. Measured at
`6ffa9ce1119ec01c953494d8f5b28e419efad646` (worktree carrying L1's uncommitted
`PROVINCE.md` / `SKILL.md` / `corpus/QUALITY.md` edits, none read as evidence). Base
`fcbe200f6739c38939e0dabf3f251de2cc6bd727`, freeze `1eaf596e5f241762349fbd102c9e09ec1df18e3f`,
both confirmed with `git cat-file -e`.

Deliverable: `.ufo/waves/round-68/w1/ConnectorCross/overlap.md` — 28-hit table, verdict per surface,
and every command run. This file carries the findings, the one proposal, and the risks.

Writes: only `.ufo/waves/round-68/w1/ConnectorCross/**`. No install, no package-manager transaction, no
fleet-repo write, no mutating `git`/`jj` verb. Scratch `/fast/scratch/hyaku/kaidoku-r68/ConnectorCross`
removed after its receipts were copied here. No sibling tool executed, no sibling file imported.

Fleet-root `merge/` and `considerthese/` **do not exist**; per-lane `considerthese/` were scanned
(hit 13).

---

## Verdict per surface (summary; hits and line numbers in `overlap.md` §1-2)

| surface | verdict | nearest precedent |
|---|---|---|
| (a) instrument-registry / inventory-conformance census | **duplicate class, distinct instance** — five lanes own the class (kama, mori, kotoba, tsukuroi, + chousa's repair history); three more own adjacent declared-vs-repo censuses (tameshi, souji, revenger) | `kama-shokunin/tools/gate-registry-check.py`, whose own round-28 → round-34 history is the same defect repaired twice |
| (b) packed-executable / UPX triage | **unowned** as an instrument, fleet-wide | `revenger-shokunin/corpus/knowledge/round-73-re-resource-atlas.md` (packer *knowledge*), `…/SOURCES.md:264` (dynamic unpacking **rejected** on charter grounds) |
| (c) sha256 identity, "the unpack restores the original" | **unowned as a rule**, composed from owned parts | `revenger…/round-64-firmware-region-byte-evidence.md` (inflate members, hash the derived bytes) + `kotoba…/check_substrate_pins.py:43-47` / `kama…/QUALITY.md:440` ("a digest says **which bytes run**, not which file") |

No contested ownership. Nothing absorbed, nothing edited.

---

## Evidence

### E1 — the class is owned; the population rule is not (observation)

All five sibling instruments of class (a) derive their population from the **tree layout** — one glob
(`gate-registry-check.py:79`) or an `ls-tree` over one directory (`check_gate_registry.py`). R68-C1
derives its population from `plans/round-N-claims.md` for the round's own N. Measured with
`w1/ConnectorCross/poprule.py` (a re-derivation that reproduces the claim's own `scope_size`):

```text
BASE   plan_keyed_scope=69   kama_layout_rule_matches=0   round67_in_scope=2  round67_matched_by_kama=[]
FREEZE plan_keyed_scope=71   kama_layout_rule_matches=0   round67_in_scope=2  round67_matched_by_kama=[]
```

kama's frozen population regex matches **0 of 71** paths at the freeze, **0 of the 2** round-67
instruments included — this lane keeps counters in the nested `tools/round-N/` layout and has no
`.ufo/waves/round-*/count-*.py` population at all. A lane importing that instrument verbatim scores
this inventory as empty and prints a clean green.

That the same class goes blind on a layout change is kama's own record: round 34 widened the glob
because "the round-33 counters live in `tools/` and were invisible to this gate"
(`kama-shokunin/SKILL.md:1362` region; the round-43 rows at `:1417` register sixteen counters the gate
had reported unregistered since round 35). Kaidoku's counters have already drifted into a nested
directory.

### E2 — independent re-derivation of one R68-C1 atom by a second code path (observation)

`python3 tools/round-68/registry-conformance.py --root <lane> --rev <base> --json-out …` →
exit 1, `mismatches 2`, `unregistered` = `["tools/round-67/avm-le-counter.py","tools/round-67/mutation-battery.py"]`,
`scope_size 69`, `registry_rows 73`, `thin []`, `duplicate_rows []`, `row_absent []`, `named_but_absent` 12,
`legacy_unregistered` 26. Receipt `w1/ConnectorCross/c1-at-base-independent.json`. It agrees with the
base receipt and with `poprule.py`'s independent `scope_size`. `registry_rows 77` at the measured
revision was **not** re-derived here.

### E3 — the one unguarded arm inside R68-C1's own instrument (observation)

`census()` guards the collapse direction: `"ok": mismatches == 0 and len(scope) > 0`
(`tools/round-68/registry-conformance.py:151`). So an empty population is never `ok`:

```text
pristine    {"mismatches": 0, "ok": false, "registry_rows": 2, "scope_size": 0}
```

No selftest case reaches that guard. The only fixture with `scope_size == 0` — `legacy-excluded` —
asserts `mismatches == 0`, the `legacy_unregistered` list and `scope_size == 0`, and never reads
`ok`; the `empty-registry` fixture keeps a non-empty scope by construction. A scratch **copy** of the
frozen instrument (sha verified `a300d831…` before and after the copy) with that guard replaced by
`and True`:

```text
selftest:  cases 11, failed [], ok true        <-- SURVIVES
census({}, <2-row registry>, …):
mut-okguard {"mismatches": 0, "ok": true, "registry_rows": 2, "scope_size": 0}
```

Control mutant on the same copy — `PLAN_RE` retargeted from `plans/` to `planz/`:

```text
failed ['clean', 'unregistered', 'legacy-excluded', 'named-but-absent', 'empty-registry'], ok false   <-- KILLED
```

So the harness is not blind in general; the scope-collapse guard is the specific thing it cannot see.
The mutant cannot flip R68-C1: the frozen predicate pins `scope_size 71` and `registry_rows 77`
independently of `ok`. The gap is in the instrument's standalone green, not in this round's claim.

Receipts: `w1/ConnectorCross/mutants/{okguard.diff, planre.diff, selftest-*.json, rc-*.py}`,
`w1/ConnectorCross/{collapse.py, collapse2.py, poprule.py, poprule.out, collapse2.out}`. The mutant
files are scratch derivatives of the frozen bytes, not the instrument; the frozen file was never
opened for writing (`sha256 a300d831…` unchanged).

### E4 — surface (b) has no route anywhere (observation)

`grep -rn -iE '\bupx\b' */SKILL.md */corpus/QUALITY.md` over all 20 sibling lanes → no hits. Outside
kaidoku the token occurs in two text surfaces: a past `pacman -S … upx …` line in a game-dev-3d report
(`reports/round-102/adversary/F6.md:54`) and a revenger source anchor quoting GoReSym's "malformed
unpacked binaries, such as from UPX" (`reports/round-73/scout-packs/ReFrameworkTargets.md:13`). Neither
is a route. The RE lane records ELF-layout routes as "blocked until caller-supplied"
(`corpus/knowledge/2026-10-12-rea-readiness-checklist.md:17`) and **rejected** dynamic unpacking —
`corpus/SOURCES.md:264`, mal_unpack, "live-malware execution is refused in this province";
`…/round-73-re-resource-atlas.md:324-333` carries the packer taxonomy as a *source ledger* with no
instrument and no capability claim. Host state, observed: `upx 5.2.0` at `/usr/bin/upx`, `binwalk` and
`unblob` present (the readiness checklist's K05 row is marked STALE for exactly this reason).

One review risk the precedent creates: atlas S348 says "a memory dump is a time-indexed observation,
**not 'the unpacked binary'**". Read out of context this looks like a counter-argument to R68-C2's
`identity` arm. It is not: `upx -d` is a deterministic inverse of a known transform whose output is
compared to a **pin of the original carrier**, so `identity_ok` is an equality with the carrier, not a
dump's agreement with a second measurement. One sentence in the R68-C2 receipt naming that distinction
de-fangs the reading.

### E5 — surface (c)'s rule is composed, not owned (observation)

Four identity relations are owned — receipt↔commit (`chousa tools/receipt-pin.py`), receipt↔fetched
bytes (`revenger corpus/audit_source_quotes.py`), file↔itself (`kama tools/gguf-identity.py`),
derived-copy↔authored oracle (`revenger round-64`, whose coverage-map explicitly excludes
`extract_firmware` and "any container format") — plus the doctrine that the pin must name the bytes
that run (`kama QUALITY.md:440` KQ85; `kotoba verifiers/check_substrate_pins.py:43-47`). None states
"the unpacked bytes' sha256 equals the original's pin". R68-C2's arm is the stronger composition: not
agreement between two measurements, but equality with the carrier.

---

## Affected axes

- **R68-C1 — calibration, capability acquisition.** E1 changes what the claim can honestly be said to
  acquire: not the census class (owned five times), but the plan-keyed population rule that finds an
  instrument the layout-keyed rules cannot see. E3 is a calibration *strength* measurement of the new
  instrument that no current artifact states.
- **R68-C2 — coverage, capability acquisition.** E4/E5 place the route as the fleet's first packed-ELF
  instrument, with the static-only boundary already set by revenger's charter and the S348 caution
  pre-answered by the pin-equality form.
- Neither surface is harmed: nothing here proposes a predicate, atom, tool, or route change.

---

## Proposed move (one, bounded)

**Guard the guard: make the scope-collapse arm visible, and register its survivor as a known gap.**

Two halves, both outside the frozen bytes:

1. **Now (report-level, no file edit).** Record in the R68-C1 receipt that the instrument's
   `len(scope) > 0` guard at `:151` is unguarded by the 11-case selftest, with the mutant and its
   predicted survival named — so the mutation battery's survivor, if it appears, is a *pre-classified*
   test gap rather than an unexplained instrument defect. Prediction, falsifiable in one run: the
   mutant `"ok": mismatches == 0 and True` survives all 11 cases (already observed here on a scratch
   copy) and turns `census({}, <populated registry>)` to `ok: true` with `scope_size 0`.
2. **Round 69 (12th case, no claim change this round).** Strengthen the scope-0 fixture to assert
   `not r["ok"]`, or add a named `scope-collapse` case, so `legacy-excluded` no longer passes on an
   assertion set that excludes the guard. This is kotoba's `QUALITY.md:46` (Q35) all-`probe` /
   `0 of 26` lesson adopted into this lane's own case inventory — a synthesis across lanes, not a new
   invention.

Why this and not something larger: the class, the empty-registry direction, the row-meaning grades and
the zero-population lesson are all owned elsewhere (hits 1-9, 13). The *only* thing round 68 has that
the fleet does not is the plan-keyed population rule (E1) and this instrument's specific guard
inventory (E3). The move touches exactly the second, is one assertion, and cannot harm coverage.

---

## Risks

1. **Class-repeat reading.** The strongest counter-argument to R68-C1 is that it is the fifth
   registry-conformance census (hits 1, 5, 7, 9) and kama's covers the same defect. E1 is the answer,
   and it must be *stated with the count* (`0 of 71`), not asserted: the class is owned, the population
   rule is not, and the population rule is what the round-67 defect was about.
2. **Cell-grammar false positives.** chousa's record (`considerthese/2026-10-25.md:28-34`) is the
   fleet's clearest case of this class producing mostly its own errors: "of round 47's 25 mismatches, 8
   were real self-assessment gaps and **10 were the counter's own escaped-pipe parsing bug**". Our
   census grades verdict cells with regexes (`VERDICT_RE`), the same surface that broke there.
   `thin []` at base is evidence against a grammar false positive, not proof; a seat that reports
   "mismatches 2" without naming both paths is reporting an unverified count.
3. **`ok: false` with `mismatches: 0` is a state the receipt vocabulary may not have.** E3's pristine
   line shows the instrument can print `mismatches 0` and still refuse. A re-derivation that reads only
   `mismatches` inherits the collapse green; the receipt must carry `ok` and `scope_size` together.
4. **Importing a sibling gate as a control.** The cheapest-looking control for next round is "run
   kama's registry gate here". E1 measures what that yields: population 0, green, no information. Any
   such import must be rejected on the measurement, and no sibling tool may be executed from this lane.
5. **S348 misreading** (E4) — one sentence in the R68-C2 receipt.
6. **`upx 5.2.0` and the REA package version are host state**, not lane state; the route's exit-2
   class already covers absent `upx`/`node`, but the pin is a sha of `/usr/bin/upx`, so a distro
   upgrade is a legitimately unevaluable run, not a red one.

---

## Verification (for the main agent; nothing here was verified by me except as noted)

- **Run:** `python3 .ufo/waves/round-68/w1/ConnectorCross/mutants/rc-mut-okguard.py --selftest` →
  expect `cases 11, failed [], ok true` (the survival). `…/rc-mut-planre.py --selftest` → expect the
  five-case kill list. `python3 …/collapse2.py` → expect the pristine `ok false` / mutant `ok true`
  pair. All three were run here; the copies differ from the frozen file only by
  `mutants/okguard.diff` and `mutants/planre.diff`.
- **Frozen bytes intact:** `sha256sum tools/round-68/registry-conformance.py` must still be
  `a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315`; the copy carried that sha
  before mutation.
- **Not run by me, unverified:** the measured-revision run (scope 71 / rows 77 / mismatches 0) —
  ExecRegistry; the C2 route — ExecPacked; the authoritative mutation battery — MutRegistry/MutPacked;
  the 12th case — round 69 by design (frozen this round).
- **Tooling record:** nothing installed or upgraded. `upx 5.2.0`, `binwalk`, `unblob` were already
  present; none was executed.

## L0 questions

None. Nothing in the scan needs a package that only `pacman` could install, and no `pacman`
transaction was run.
