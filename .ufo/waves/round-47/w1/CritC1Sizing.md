# CritC1Sizing — scoped findings on R47-C1 (exactness table, block 24)

Seat: critic, C1 sizing. Lane `kaidoku`, round 47, wave 1. Read-only on the lane; scratch
`/fast/scratch/hyaku/kaidoku-r47/CritC1Sizing` (removed after capture). Pinned revision
**`f7d6e58d6e7f4e664bf443137c55ee08821de244`**; instrument `tools/round-47/exact.py` sha256
`01a4bca7…bc5bcd5`; `SKILL.md` sha256 `894e2864…0ebffafd`. Receipts:
`.ufo/waves/round-47/w1/CritC1Sizing/receipts/` (commands, exits, stdout sha256, UTC in
`MANIFEST.md`); narrative detail in `CritC1Sizing/report.md`.

**Verdict.** Predicate holds at the tip (exit 0, `failing []`, battery `4/4/0/1/0`) — but it is
**too weak in four ways** and its headline pin proves less than the claim says. F4 is a forgery of
the whole claim: a fully dead battery still scores met.

## F1 — the counter is red at the freeze the prompt names (blocking for any re-measure)

Counterexample: `--freeze 5017e1f --rev f7d6e58` → **exit 2** `frozen_path_changed`
(`receipts/final/c1-freeze-5017e1f7.json`, stdout sha `e4d02214…`). Same for A1 `9018c53`, the
landing `e856beb`, and A5 `07d2894`. Only `f54b3b6` (A6) and later exit 0
(`c1-freeze-f54b3b6d.json`, `c1-freeze-a0753786.json`). The claims file's freeze clause ("Nothing in
this file or in `tools/round-47/` changes after the freeze") is true only against the sixth
amendment; A3–A6 are disclosed in commit subjects, not in the claims text. With `freeze == rev`,
`history_touched` is empty by construction, so the freeze arm is dead at the revision actually
scored.
Smallest correction: state the freeze as `f54b3b6d` (A6) in the claims and the counting command, and
list A1–A6 in the claims text; do not claim a freeze arm at `freeze == rev`.

## F2 — `exit` is a digit set, not a meaning (the round's own HIGH defect, re-instantiated)

Block 24 routes R46-CL7 away ("a verdict map is a registry concern and this block does not reach
it") and then binds its own exit column as `{0,1,2}` membership. Fixture `exit-all-zero` (all four
exit cells `0`): **exit 0, `failing []`, battery `4/4/0/1/0`**
(`receipts/attacks/exit-all-zero.json`). A row that names an arm and says the arm returns clean is
met.
Smallest correction: for a row that names an arm, `exit ∈ {1,2}`; stronger, bind each row's exit to
the v3 exit of that defect's measured forgery (needs a `routed-id → mutation` map in the counter).

## F3 — the arm column has no bijection; the table is not a matrix

Fixtures (`receipts/attacks/`): `arm-all-order` (all four cells `order`) → **exit 0**;
`arm-permuted` (`CL2→order, CL3→digest, CL4→once, CL6→symbol`) → **exit 0**. With ids bijective and
arms membership-only, 24 × 4⁴ × 3⁴ = **497,664** tables pass clauses 2–5 for the same four ids.
`v2hole-junk` (every hole cell `x`) → **exit 0**: the `v2 hole` column asserts nothing.
Context: block 23 has 13 rows and a 9-forgery battery (`attest.py:254`); block 24 has 4 rows and 4
forgeries. The round's new instrument measures fewer forgeries than the one it succeeds; the four
rows are distinct holes in prose, but the counter verifies only their labels.
Smallest correction: `sorted(arm) == sorted(VOCAB)` (demonstrated: `arm-all-order` → exit 1, landed
block still met). That yields a bijection; the *pairing* residual needs a second authority and is a
tradeoff, not a bug — declare it instead of calling the table a matrix.

## F4 — a dead mutation is scored as a discriminating forgery (forgery of the whole claim)

`exact.py:367-371`: a no-op mutation does `forgeries_total += 1; v2_green += 1; continue` — it is never
scored under either profile, although the claims say each forgery is "scored … under both
profiles".
- `dead-one` (neuter `_m_substring_arm`, keep its name, re-pin the block's interpreter sha): **exit 0**.
- `dead-all` (neuter all four, names unchanged): **exit 0**, battery `4/4/0/1/0`, `failing []`
  (`receipts/attacks/dead-all.json`).
Smallest correction: `crash += 1` on a no-op (demonstrated: `dead-all` → exit 1 with
`battery crash 4 != 0`, landed block still met).

## F5 — `mutations_sha256` proves internal consistency only

The digest is `sha256("\n".join(names))`, and the names are bytes of the file that
`interpreter_sha256` already pins — so it is a pure function of the pinned bytes. It catches only an
authoring-time mismatch between the block's literal and the cited revision. It does **not** move on
a behaviour change (`dead-all` keeps `19a2166e…` while all four functions are dead), and a deletion
is caught by `forgeries_total == 4`, not by the digest — a count that four dead mutations satisfy.
Verified: names digest `19a2166e…d5a112` = block pin; the four function sources hash `e40a5ab1…b2cc88`.
Smallest correction: digest the mutation **sources**, not the names, so a behaviour edit must appear
in the graded `SKILL.md` diff; because the same actor can re-pin both literals in one amendment
series (A6 → `a075378` did, 25 s apart), the pin's value is exactly that visibility.

## F6 — executed ≠ graded for `tools/round-46/gate.py`

The claims call gate.py "frozen infrastructure"; it is not in `## Frozen paths (exact)` and `dirty()`
covers only the derived frozen set. The counter imports the **worktree** gate.py while clause 7
grades the **committed** literal.
Fixture `fx-gatesplit` (c1 freeze → c2 tamper `plans/round-47-claims.md` → c3 restore):
clean worktree → **2** `frozen_path_changed`; worktree `gate.py` with
`history_touched → [], None` (uncommitted; committed literal intact) → **0**; restored → **2**
(`receipts/gatesplit.json`). A tamper+restore of a frozen path scores clean by editing a file no
clause grades.
Smallest correction: include every imported module in the dirty/frozen guard, or grade the executed
source rather than `git show`.

## F7 — the cited v2 control does not contain `v2_green 4`

`controls/ctl-c1-1-v2-profile.json` has no `battery` key and no `v2_green`: it is a `--no-battery`
run of the genuine block under `--profile v2`. The claims cite it for "`v2_green 4` — the four holes
measured". The number is reachable: at the pinned tip, `--profile v2` with the battery gives
`v2_green 4, v3_green 0, genuine_green 1`, exit 0
(`receipts/final/c1-v2-profile-repro.json`). Stale control, not a false measurement; re-run it or
correct the sentence.

## Not a hole (checked, clause holds)

- `duplicate-routed-id` has teeth: a 4-row table with `CL2` twice fails on cardinality alone
  (`receipts/attacks/dup-id-isolating.json`, exit 1). But the *claimed* forgery inserts a 5th row,
  so it fails clause 3 as well — the claimed battery case does not isolate clause 4.
- Pins, header equality, marker cardinality, title numbering, and the flag-order literal all fail
  correctly in the selftest (`cases=16 failures=0`).
- `refs >= 3` is path matches, not selectored citations: `refs-minimal` (`refs 4` = one distinct
  selectored path cited twice + two SELF mentions) → exit 0. Minor; close by counting only
  selector-bearing, distinct citations.

## Measurement summary (all read-only)

| what | exit | receipt |
|---|---|---|
| C1 at tip `f7d6e58`, freeze = rev | **0**, `failing []`, battery `4/4/0/1/0` | `receipts/final/c1-tip-full.json` |
| do-nothing before (`5017e1f` = freeze = rev) | **1**, `rule_blocks 23`, `block_present 0` | `c1-before-at-freeze.json` |
| prompt freeze `5017e1f` at tip | **2** `frozen_path_changed` | `c1-freeze-5017e1f7.json` |
| freeze `f54b3b6d` (A6) at tip | **0** | `c1-freeze-f54b3b6d.json` |
| four falsifying blocks | **0** each | `receipts/attacks/` |
| dead-all | **0** | `receipts/attacks/dead-all.json` |
| gate.py executed≠graded | **0** vs **2** | `receipts/gatesplit.json` |
| four one-clause closes on copies | landed **0**, four attacks **1** | `receipts/fixdemo.json` |
| counter selftest | **0**, 16/16 | `receipts/selftest.out` |

Axes impacted: `depth` only (R47-C1). No coverage surface touched. The claim's depth credit is real
but narrower than "matrix": four exact bindings and four measured forgeries, with the denominator
open to a silent behaviour edit unless F4/F5 close. No installs; no lane writes outside this seat's
two named paths and its scratch.
