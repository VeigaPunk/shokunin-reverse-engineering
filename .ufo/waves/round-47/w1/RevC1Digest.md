# RevC1Digest — clause-6 attack on R47-C1's mutation digest

Seat: `RevC1Digest` (leaf, no subagent dispatch). Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on the lane tree; every write
under `S=/fast/scratch/hyaku/kaidoku-r47/RevC1Digest` (now deleted) and this report dir.
No tool was installed (`python3`, `git` only), so no install record.

Measured lane state during the seat: `HEAD` moved twice while I worked —
`3186f69b` (wave-1 spec) → `e856beb5` (landing) → `62e33f7d` (A2) → `2e4ae434` (A3) →
`1e2c3102` (A4) → `a631bba0` (still moving after my last measurement, 17:59Z). Every number below is pinned to a rev named in the receipt. The frozen
surfaces were never modified by me; `git status --porcelain -- tools/round-47/ plans/ is
empty at every point I read it.

## 0. Two facts that frame everything below

**Freeze re-derivation returns the tip, not the first freeze.**
`git log --format=%H -1 -- plans/round-47-claims.md tools/round-47/` at `1e2c3102` →
`1e2c3102952dc636650095643c1963c833859019` (i.e. `HEAD`, the A4 amendment commit). The
claim's own re-derivation rule is "the last commit that touched the frozen paths", and A1
redefined the freeze as "the commit that carries this paragraph" — so **every amendment moves
the declared freeze forward**, and any measurement with `--freeze <tip> --rev <tip>` is
zero-distance. The claims file still says at the same time: "Nothing in this file or in
`tools/round-47/` changes after the freeze: a change makes both counters exit 2
`frozen_path_changed`" (`plans/round-47-claims.md:10-11` at `1e2c3102`). Both statements cannot
hold: at the A1 freeze the counter *does* exit 2 (R7b below), so the "nothing changes" clause
is false for A2/A3/A4, and the "declared freeze" clause makes it unobservable.

**The first landing commit does not pass its own counter.** At `e856beb5` (the commit whose
message is `round-47: land craft block 24, the record corrections, the current axis heads and
S143`) the counter exits 1: the four arm cells read `symbol: …prose…`, `once: …`,
`digest: …`, `order: …` instead of the bare token, so clause 5 fires. A2 (`62e33f7d`) is the
commit that made the landed block green. Receipt `R11-landing-e856beb5.json`, exit 1,
`failing: ["arm cells not exact vocabulary tokens: [...4 verbose cells...]"]`. Consequence for
the L1: "re-measure at the landing revision" must name a commit; the claim's counting command
takes `--rev` and records no choice of revision.

## 1. Receipts (exact command, exit, stdout sha256, UTC)

Scratch root `S=/fast/scratch/hyaku/kaidoku-r47/RevC1Digest`. Counter executions were
`python3 -I -B <counter> --root <root> --freeze <F> --rev <R>`; fixtures were fresh
`git init` repos under `$S` whose toplevel was asserted equal to their path before the first
commit, carrying the lane's own bytes for `SKILL.md`, `plans/round-47-claims.md`,
`tools/round-47/exact.py`, `tools/round-46/gate.py`, `corpus/lessons/round-46.md`,
`corpus/lessons/round-45.md` at rev `1e2c3102` unless stated. Durable copies of every receipt
are in `receipts/` beside this file; the three drivers and the four counter variants are in
`attack/`.

| receipt | root | freeze..rev | exit | stdout sha256 (16) | UTC | battery |
|---|---|---|---|---|---|---|
| R1-fixture-honest | fixture | `bcfe7d39`..`bcfe7d39` | 0 | `4de0d20a4ff06d73` | 2026-10-28T17:53:41Z | 4/4/0/1/0 |
| R2-reorder-stale-pin | same fixture | `bcfe7d39`..`bcfe7d39` | **1** | `4dc601c8a420f431` | 17:53:42Z | **skipped** |
| R3-reorder-repinned | fixture | `f29de46d`..`f29de46d` | 0 | `256a62acd6b9ae7a` | 17:53:42Z | 4/4/0/1/0 |
| R4-body-swap | fixture | `…` | 0 | `72559d38935a0256` | 17:53:42Z | 4/4/0/1/0 |
| R5-noop-body | fixture | `…` | **0** | `e593f57df47d94e6` | 17:53:42Z | **4/4/0/1/0 with 3 real forgeries** |
| R6-executed-unpinned | fixture | `bcfe7d39`..`bcfe7d39` | **0** | `79bd4caed93e896c` | 17:53:43Z | 4/4/0/1/0 |
| R7-lane-freeze-eq-rev | lane | `1e2c3102`..`1e2c3102` | 0 | `98ef390e1c1a3eaa` | 17:54:18Z | 4/4/0/1/0 |
| R7b-lane-a1-freeze | lane | `9018c53b`..`1e2c3102` | **2** | `dbce9388c6838cb0` | 17:54:18Z | — |
| R8-amendment-freeze-old | fixture | `e1afc80e`..`22031ca3` | **2** | `a3b704c5848a3c11` | 17:54:18Z | — |
| R8b-amendment-freeze-tip | same fixture | `22031ca3`..`22031ca3` | **0** | `74e7e82821176f7f` | 17:54:18Z | **4/4/0/1/0 with 3 real forgeries** |
| R9-second-pin-ignored | fixture | `…` | **0** | `2c28088d98b1a120` | 17:54:59Z | 4/4/0/1/0 |
| R10-superstring-names | fixture | `…` | **0** | `2f53ae466b0187a8` | 17:54:59Z | 4/4/0/1/0 |
| R11-landing-e856beb5 | lane | `9018c53b`..`e856beb5` | **1** | `219d030bf624691f` | 17:56:30Z | skipped |
| R12-names-removed (control) | fixture | `…` | **1** | `f2b352626e0816a5` | 17:57:40Z | skipped |

R7b's `frozen_path_changed` is `["plans/round-47-claims.md", "tools/round-47/",
"tools/round-47/record.py"]`, `touched: ["plans/round-47-claims.md",
"tools/round-47/record.py"]`. R7's is `[]`, `touched: 0`, `freeze == rev == 1e2c3102`.

Digests, computed by hand and matched against the live counter:
`sha256("\n".join(names))` over `substring-arm, duplicate-routed-id, stale-mutations-digest,
flag-order-drift` = `19a2166e47c5…d5a112` (the block's pin at `1e2c3102`, and
`receipt.mutations_sha256_expected`); over the reversed order = `1d6a4cf8efb2…e48209`;
over the first three in order = `b7d3e477e2f6…1ac61a`; `sha256(tools/round-47/exact.py)` =
`dcef54f1b143…26412c` (the block's `interpreter_sha256`).

## 2. Findings

### F1 (HIGH) — a mutation that does nothing is scored as a passing forgery, so clause 9's denominator can be 4 while only 3 forgeries exist

`tools/round-47/exact.py:349-353` (in `run_battery`):

```python
if text == block and not overrides:
    out["fixtures"].append({"name": name, "error": "mutation was a no-op"})
    out["forgeries_total"] += 1
    out["v2_green"] += 1          # <-- a non-event counts as a measured pass
    continue
```

A no-op increments `forgeries_total` **and** `v2_green`, never touches `v3_green`, and so
leaves every clause-9 target (`forgeries_total == 4`, `v2_green == 4`, `v3_green == 0`,
`genuine_green == 1`, `crash == 0`) exactly where a real forgery would. Neither
`crash` nor `v3_green` can see it.

- Fixture: `$S/tmp.*` built by `attack/drv.py::build_fixture("noop", …)` — one commit, the
  lane's bytes at `1e2c3102` with `("duplicate-routed-id", lambda block, spec: (block, {}))`
  in `MUTATIONS`, the block's `interpreter_sha256` re-pointed to those bytes and
  `mutations_sha256` left at `19a2166e…` (names and order unchanged, so it is still *correct*).
- Command: `python3 -I -B $S/counters/noop.py --root <fixture> --freeze F --rev F`
- Exit **0**; receipt `R5-noop-body.json`; `battery.fixtures[1] == {"name":
  "duplicate-routed-id", "error": "mutation was a no-op"}` with no `v2_exit`/`v3_exit`, while
  `forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0`, `failing: []`.
- The same fixture two commits apart: `R8-amendment-freeze-old` (freeze at the honest commit)
  exits **2** `frozen_path_changed: ["tools/round-47/", "tools/round-47/exact.py"]`;
  `R8b-amendment-freeze-tip` (the amendment declared as its own freeze, exactly as A1 and A2
  did) exits **0** with the same fabricated battery. So the *only* thing standing between this
  and a green landing receipt is the freeze pin, which the claim lets the author move (F2).
- The lane already knows this failure mode from the other side: A2's own paragraph records
  that R47-C2's battery had a forgery that "was a no-op" and reported `forgeries_green 1`.
  `record.py` was fixed; `exact.py` still treats a no-op as a *pass*.

What the claim would have to say: clause 9 gains `battery.noop == 0`, the no-op branch stops
incrementing `v2_green` (or increments a `noop` counter and `forgeries_total` counts only
executed forgeries), and the kill rule names "a mutation whose body is a no-op keeps a green
receipt" as a defect rather than as a pass.

### F2 (HIGH) — the frozen-bytes guarantee is self-referential and vacuous at the declared freeze

- `R7b-lane-a1-freeze.json`: freeze `9018c53b` (the A1 freeze), rev `1e2c3102` → exit **2**
  `frozen_path_changed` naming `plans/round-47-claims.md` and `tools/round-47/record.py`.
  So the bytes did change after the stated freeze, three times (A2, A3, A4).
- `R7-lane-freeze-eq-rev.json`: freeze `1e2c3102`, rev `1e2c3102` → exit **0**, `touched: 0`,
  `frozen_path_changed: []`. The re-derived freeze is the measured revision, so the guard has
  nothing to compare and always passes.
- The claim has no clause reading `freeze`: R47-C1's nine clauses never mention it, the
  counting command leaves it to the operator, and the predicate text calls frozen paths
  "byte-frozen at `5017e1f`" while A1 re-declares the freeze. `git log -1 -- tools/round-47/
  plans/round-47-claims.md` now returns `1e2c3102` — the tip.
- Fixture demonstration that this is an exploit, not just bookkeeping: `R8`/`R8b` above; the
  counter is honest in both, and only the declared freeze decides the exit code.

What the claim would have to say: the freeze is a **fixed commit id** (or `git merge-base`
of the first containing commit, never a re-derivable "last commit"), the counting command
echoes it into the receipt, and clauses require `freeze != rev` plus `touch_count == 0`
already at the *first* declared freeze; amendments need their own bounded count
(`amendments <= N`) with the pre-amendment receipts retained. A receipt whose
`freeze == rev` should not be citable as freeze-integrity evidence.

### F3 (MEDIUM) — clause 6's "names all four mutation names" is a containment test, the exact defect R46-CL2 routed

`exact.py:254-257`: `unnamed = [n for n in names if n not in block]`. A block that mentions
each name only inside a longer token passes.

- Fixture `R10-superstring-names.json`: the lane's block at `1e2c3102` with every
  `` `substring-arm` ``-style backticked name rewritten to `` `not-substring-arm-honest` ``
  (and the three siblings); the pins are untouched.
- Command: `python3 -I -B $S/counters/orig.py --root <fixture> --freeze F --rev F`
- Exit **0**, battery 4/4/0/1/0, `failing: []`. The block no longer states a single bare
  mutation name, yet clause 6's name arm is satisfied. The control is
  `R12-names-removed.json` (the same fixture with `substring-arm` → `substring` everywhere):
  exit **1**, `mutation names not stated in the block: ['substring-arm']` — so the check is
  live, it is just a containment test.
- Note the block's own first row says the round's lesson is "an equality, not a containment";
  the names arm of the same clause still contains.

What the claim would have to say: clause 6's name arm is an equality over a token list —
`` `substring-arm` `` exactly once, no longer token, or "the four names occur, each as a
backticked whole token, exactly once, in the order the digest covers".

### F4 (MEDIUM) — the pin regexes read the *first* occurrence, so the block can display a false pin that no clause reads

`MUT_PIN`/`SELF_PIN` are `re.search`. A block carrying a second, different
`mutations_sha256:…` after the correct one keeps exit 0.

- Fixture `R9-second-pin-ignored.json`: the block line plus
  `A second, stale pin reads mutations_sha256:000…0.` appended inside the same block.
- Command: `python3 -I -B $S/counters/orig.py --root <fixture> --freeze F --rev F`
- Exit **0**, battery 4/4/0/1/0; the receipt's `mutations_sha256` is the correct first value
  and the `000…0` text is never looked at by any clause.

What the claim would have to say: each of `mutations_sha256` and `interpreter_sha256` occurs
**exactly once** in the block (a count, like the marker count), or the clause compares the
set of all matches.

### F5 (MEDIUM) — the digest binds the name sequence, not what a name denotes; a reorder is detectable only against a stale pin

Direct answers to the seat's questions, each with its receipt:

1. **Reorder + stale pin → detectable.** `MUTATIONS` reversed in a scratch copy of the counter
   (bytes `62903c75…`), block untouched: `R2-reorder-stale-pin.json`, exit **1**, single
   failing line `mutations_sha256 does not match the counter's own mutation list`
   (`mutations_sha256 19a2166e…` vs `mutations_sha256_expected 1d6a4cf8…`). Clause 6 is the
   only detector: the interpreter pin compares the fixture's file at rev (unchanged bytes), so
   it stays green.
2. **The block's pin must move with the list.** `19a2166e…` → `1d6a4cf8…`. That is the whole
   order dependence of the claim: the pin value is computed over the ordered names.
3. **Reorder + re-pin → green, denominators unchanged.** `R3-reorder-repinned.json`, exit
   **0**, battery **4/4/0/1/0** — byte-identical denominators to the honest floor
   `R1-fixture-honest.json`. Per-forgery detail is unchanged too; `stale-mutations-digest` is
   still red for `mutations_sha256 does not match…` because it hashes `MUTATIONS[:3]`, which
   under any permutation is 3 of 4 distinct names and can never equal the 4-name digest
   (`orig[:3] = b7d3e477…`, `reversed[:3] = e6793438…`; all four 3-of-4 digests are distinct —
   printed in `attack/drv.py` header output). **No denominator moves under a reorder**, proved
   for all 24 permutations from the code, executed for the reversed one.
4. **A reorder alone is therefore not a forgery at all** — it is a rename of an unordered
   collection that the battery does not depend on. The claim depends on the order only because
   it writes the digest "in order"; a digest over `sorted(names)` would lose nothing.
5. **The real gap: the digest cannot see which body a name carries.** With the two function
   references swapped between `substring-arm` and `duplicate-routed-id` (names and order
   byte-identical, so `MUT_DIGEST` is unchanged and the block's pin is still *valid*),
   `R4-body-swap.json` exits **0**, battery 4/4/0/1/0, and the fixture list shows the lie:
   `{"name": "substring-arm", … "v3_failing": ["rows 5 != 4", "routed cardinality
   {'R46-CL2': 2, …}"]}` — the "substring-arm" forgery is red because a duplicate *row* was
   inserted, not because an arm cell contains `order-ish`. The only binder on bodies is
   `interpreter_sha256`, which is a whole-file hash the same author re-pins (F2), and the
   landed block's own earlier wording — "so any edit to the list breaks the block's pin"
   (present at `e856beb5`, removed by A2) — is exactly what this fixture falsifies: a body
   swap is an edit to the list and the pin does not break.

What the claim would have to say: the digest is defined as binding the **name sequence only**
(no consequence claims about semantics), and a second pin — `sha256` over
`[(name, inspect.getsource(fn)) for name, fn in MUTATIONS]`, or the four `fn.__qualname__`
values — binds each label to its body. Record the four `v3_failing` strings as the expected
failure *reason* per forgery, so a mislabelled forgery cannot pass as "red for some reason"
(the battery's own `fixtures` already carries them; nothing compares them).

### F6 (MEDIUM) — `interpreter_sha256` certifies the repo file, never the code that produced the receipt

Clause 8 compares the pin against `files(SELF)` at `--rev` (`exact.py:283-289`). The counting
command runs the *working-tree* file. Nothing in the receipt names the executed bytes.

- `R6-executed-unpinned.json`: executed `$S/counters/bodycam.py` (`f2d6c271…`) against a
  fixture whose `tools/round-47/exact.py` is the honest `dcef54f1…` and whose block pins
  `dcef54f1…`. Exit **0**; the receipt reports `interpreter_sha256: dcef54f1…` and
  `interpreter_sha256_expected: dcef54f1…`. The receipt's key set contains no field for the
  executed file (verified: the only sha-named keys are `interpreter_sha256`,
  `interpreter_sha256_expected`, `mutations_sha256`, `mutations_sha256_expected`).
- This is live in the lane today for the sibling counter: `git status --porcelain` showed
  ` M tools/round-47/record.py` at the start of the seat (`3186f69b`, 17:53Z), i.e. `record.py` executed from the
  working tree while its pin is read from git. For `exact.py` the same shape is available to
  any seat that edits its scratch copy and runs it with `--root` pointed at the lane.

What the claim would have to say: the counter hashes `__file__` at startup, emits
`interpreter_sha256_executed`, and clause 8 requires `interpreter_sha256_executed ==
interpreter_sha256`; alternatively the counting command materialises the file from `--rev`
(`git show "$REV:tools/round-47/exact.py"`) and runs that.

### F7 (LOW) — a structural failure erases the denominator instead of reporting it

When a v3 clause fails, `evaluate()` sets `receipt["battery"] = {"skipped": …}`
(`exact.py:400-402`) and clause 9's per-key comparison never runs. R2's receipt therefore has
`forgeries_total: null` — indistinguishable, for a census that greps receipts, from "battery
not requested". The claim's clause 9 reads as if the battery always reports five numbers.

What the claim would have to say: a `battery_measured` boolean (or `measured: false` plus a
reason) so a ratio over receipts cannot silently include skipped runs.

## 3. What is sound (checked, not assumed)

- The fixture floor is real: `R1` on a one-commit fixture carrying the lane's bytes at
  `1e2c3102` exits 0 with 4/4/0/1/0, and each forgery's `v3_failing` names its own defect
  (`arm cells not exact vocabulary tokens: ['order-ish' …]`; `rows 5 != 4` + cardinality;
  `mutations_sha256 does not match…`; `gate.py flag order: 0 correct, 1 reversed`). The four
  v2 exits are 0 for the same four, so "v2 green, v3 red" is measured, not asserted.
- Clause 6 does fire on a stale pin (R2) and the digest is genuinely order-sensitive
  (`19a2166e…` vs `1d6a4cf8…`), so the landed pin at `1e2c3102` is consistent with the
  landed `MUTATIONS` order and with `sha256(exact.py) = dcef54f1…`.
- `freeze_state`'s guard works when it is given a real freeze: R7b, R8 exit 2 with the exact
  changed paths. The defect is in what the claim calls "the freeze", not in `gate.py`.
- The landing is currently met in the only sense the counter can check: `1e2c3102` at
  `freeze == rev` exits 0, `met_target: true`, battery 4/4/0/1/0 (R7).

## 4. Verification gaps (not run)

- R47-C2 (`record.py`) was not measured by this seat — another seat owns it; I only cite A2's
  own admission about its no-op forgery, and the working-tree `M record.py` I observed.
- I did not run `exact.py --selftest` (the selftest is not part of the counting command and
  its cases are separate from the battery).
- The 24-permutation claim is proved from the code and executed only for the reversed
  permutation (R3).
- I did not attempt a real-lane amendment (read-only contract); R8/R8b reproduce the flow in a
  fixture with the lane's exact bytes.
- Clause 5's `v2` counterpart and clause 7's reversed-literal count were exercised only through
  the battery, not individually.

## 5. Residual risk

The receipts are pinned to `1e2c3102`; A3/A4 were landing while this seat ran, so a later
amendment can move the pin values (`19a2166e…`, `dcef54f1…`) again — which is exactly F2. The
findings that survive any re-pin are F1 (no-op accounting), F3 (containment), F4 (first-match
pin), F5.5 (names ≠ bodies) and F6 (executed-vs-pinned), because none of them depends on a
particular digest value.
