# RevC1Before — R47-C1 attack report

Seat `RevC1Before`, round 47 wave 1. Read-only on the lane: every lane byte was read through
`git show`; every mutation happened in a `git clone --shared` fixture under
`/fast/scratch/hyaku/kaidoku-r47/RevC1Before/`, one commit per variant, `--root` always the
fixture, `--freeze` always a commit that fixture contains.

**The lane moved while this seat ran.** Twelve round-47 commits landed after the freeze
(`5017e1f7`): `9018c53b` A1 → `e856beb5` first landing → `62e33f7d` A2 → `2e4ae434` A3 →
`1e2c3102` A4 → `caafeffa` record → `07d2894e` A5 → `a631bba0` A5 record → `04469ee8` →
`f54b3b6d` A6 → `a0753786` → `31b092d1` A7. Every figure below names the revision it was
measured at. Current tip at the last measurement:
`31b092d17e77f5064c919383a9bc1e6cbfd2d1ff`.

---

## 0. Verdict

| # | finding | severity | receipt |
|---|---|---|---|
| F1 | **The block need not be in `## Queue-drain craft` at all.** Any earlier text containing the literal `## Queue-drain craft ` (an `### …` heading, a fenced quote, a prose mention) hijacks the parse; the real H2 section — 23 rules, no marker — is never read, and the counter exits 0 with the full battery green | **claim-fatal (green forgery)** | `fixtures/P1-decoy-h3-real-section-absent.json` |
| F2 | **No declared freeze scores the landing.** The claims file declares A1 (`9018c53b`) as "the commit that carries this paragraph"; at HEAD that freeze exits 2 `frozen_path_changed` because `tools/round-47/exact.py` changed at A6 (`f54b3b6d`). The only freeze that scores (exit 0) is `f54b3b6d`, which **no document names** — not the claims file (0 occurrences of `A6` or `f54b3b6d`), only a commit message | **claim-fatal (identity)** | `at-HEAD-A1-freeze.json` (2), `at-HEAD-A6-freeze.json` (0), `at-HEAD-prompt-freeze.json` (2) |
| F3 | **The denominator is pinned to itself.** Remove a mutation from `MUTATIONS`, change `("forgeries_total", 4)`→`3` and `("v2_green", 4)`→`3` in the same file, re-pin `mutations_sha256`/`interpreter_sha256` in the block, and name that commit the freeze: exit 0 with `battery.forgeries_total 3`. Re-run under the real freeze: exit 2. This is R46-CL4 one level up | **high (green forgery)** | `fixtures/P8-reduced-denominator.json` (0, 3 forgeries), `fixtures/P8b-reduced-denominator-A6-freeze.json` (2) |
| F4 | **The executed core is outside the frozen set.** `tools/round-46/gate.py` is what `exact.py` imports and runs, but round 47's `## Frozen paths` lists only the claims file and `tools/round-47/`; `dirty()` also does not cover it. A one-line uncommitted edit to `gate.py` (`freeze_state` → `return 0, receipt`) turns a true `frozen_path_changed` exit 2 into exit 0, and a dirty frozen tool into exit 0. The tampered run's receipt is **byte-identical** to a clean one | **high (green forgery)** | `fixtures/P7-frozen-path-changed.json` (2) → `fixtures/P7b-gate-tamper.json` (0); `15e-…` (2) → `15f-…` (0) |
| F5 | **A contentless matrix is met.** With every `v2 hole` cell replaced by `-`, the block still exits 0 with the battery green: the clause binds ids, arm tokens and exit digits, never the hole the row is supposed to state — the R46-CL7 species inside the fix for R46-CL7 | medium (green forgery) | `fixtures/P2-empty-hole-cells.json` (0) |
| F6 | **Two rule-24 blocks are met.** A phantom `- **24. …` bullet inside rule 23's body leaves 25 blocks, two titled `24. `, and the counter green — `block_is_last` only binds the marker's block, never the title's uniqueness | medium (green forgery) | `fixtures/P4-two-blocks-titled-24.json` (0, `rule_blocks 25`) |
| F7 | **Citation cardinality is token cardinality.** `refs >= 3` counts `HARD_REF` matches; three selector-bearing tokens spread over two documents pass, and `tools/round-47/exact.py` is exempt from the selector requirement (the landed block mentions it 4× bare). Breadth of citation is not measured | low | `fixtures/P3-three-citations-two-documents.json` (0, `refs 6`, 3 documents) |
| F8 | **`restored` mislabels children of a changed directory** (`tools/round-47/exact.py`, `record.py` are reported "restored" while `tools/round-47/` is in `frozen_path_changed`): the comparison is string equality between the dir entry and the child path | low (diagnostics) | `at-HEAD-A1-freeze.json` `restored` |
| F9 | **`--selftest` is unreachable as documented.** `--root/--freeze/--rev` are `required=True`, so `exact.py --selftest` exits 2 on argparse; with dummy required args it runs 16 cases, 0 failures. No case puts prose in an arm cell, which is why the instrument was green while the first landing (`e856beb5`) was red on clause 5 | low (instrument) | `selftest.stdout.txt` (exit 2), `selftest-with-required-args.stdout.txt` (exit 0, 16/0) |
| F10 | **`ctl-c1-2` is described by a mechanism it does not demonstrate.** The receipt says `battery.skipped: artefact fails a structural clause first`; the claims file says "the battery cannot even be built (`marker blocks 0`)". The `battery: cannot build a battery: marker blocks N` branch is unreachable, because `evaluate()` runs the battery only when `code == 0`, and `code == 0` requires exactly one marked block | low (before-cell) | `ctl-c1-0-do-nothing.json`, lane `controls/ctl-c1-2-…json` |

The before-state itself is honest — see §1. The current landing *is* green under the A6 freeze —
see §2. What fails is the instrument's ability to distinguish the landed block from the five
forgeries in §3, and the record's ability to name the freeze it was scored at.

---

## 1. The do-nothing control, and why `block_present 0` is the right reason

Commands (lane root, canonical form from the claims file's counting command):

```sh
python3 -I -B tools/round-47/exact.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze 5017e1f7299c3a812e87e7950148f54313dd279e \
  --rev    5017e1f7299c3a812e87e7950148f54313dd279e \
  --json-out .ufo/waves/round-47/w1/RevC1Before/ctl-c1-0-do-nothing.json
```

exit **1**; `rule_blocks 23`, `marker_occurrences 0`, `block_present 0`,
`failing ["marker_occurrences 0 != 1", "marker_block_count 0 != 1"]`,
`frozen_path_changed []`, `dirty []`. Receipt `ctl-c1-0-do-nothing.json`
(sha256 `88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba`).

Four independent checks that this is *absence*, not a parser accident
(`fixtures/attack.py` step 0, output in the run log):

1. **The section parses.** `craft_section()` finds the H2, `blocks_of()` returns 23 blocks, the
   last is `23. Freeze-integrity evidence…` — so the block walk ran to the end of the section
   and found no 24. A parse failure would have raised `Malformed`, and `score()` returns **2**,
   not 1 (`exact.py` `score()` → `except Malformed`).
2. **The marker is absent document-wide**, not just in the section: `skill.count(MARKER) == 0`
   over all of `SKILL.md@5017e1f`.
3. **The first `## Queue-drain craft ` occurrence is the real H2**, at line 81
   (`## Queue-drain craft (rounds 5-12, distilled in round 13)`). No decoy precedes it at the
   freeze, so the 23 blocks are the live section's.
4. **The same harness on the same base produces 24 and exit 0** once a block is inserted
   (`fixtures/02-arms-exact-token.json`, now superseded by `P0-baseline-head-block.json`), so
   the parser is not failing on this file shape.

At the declared A1 freeze the identical numbers hold, exit 1, `rule_blocks 23`,
`block_present 0` — `fixtures/ctl-c1-0-do-nothing-at-A1.json`.

Two bookkeeping notes for the report's Before cell:

* the lane's retained `controls/ctl-c1-0-do-nothing.json` **omits** the `battery` key — it was
  produced with `--no-battery`, which the claims' counting command does not pass; my receipt at
  the same rev differs from it by exactly that key (`battery.skipped`). Either state the command
  with `--no-battery` or retain the keyed receipt;
* `--json-out` is refused outside the lane root (`out_path`), which the claims' command template
  (`--json-out <OUT>`) does not say. My first attempt exited 2
  `--json-out outside the lane root`.

---

## 2. The landing, measured

| freeze | rev | exit | why |
|---|---|---|---|
| `5017e1f7` (prompt) | `e856beb5` (first landing) | **2** | `frozen_path_changed: [plans/round-47-claims.md, tools/round-47/, tools/round-47/record.py]` — A1 edited two frozen paths |
| `9018c53b` (A1, declared) | `e856beb5` | **1** | clause 5: `arm cells not exact vocabulary tokens` — the landed cells read `symbol: the arm cell must equal …` |
| `9018c53b` (A1, declared) | `31b092d1` (HEAD) | **2** | `frozen_path_changed` — A6 edited `tools/round-47/exact.py` (sha `dcef54f1…` → `01a4bca7…`) |
| `5017e1f7` (prompt) | `31b092d1` (HEAD) | **2** | same, plus `plans/round-47-claims.md` |
| `f54b3b6d` (A6, undeclared) | `31b092d1` (HEAD) | **0** | `failing []`, `rule_blocks 24`, `rows 4`, `refs 9`, `cited` 4 documents, `unresolved_citations []`, both pins equal to the bytes at rev, `gate_order_literal 1 / reversed 0`, battery `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0` |

Receipts: `at-landing-e856beb5.json`, `at-landing-A1-freeze.json`, `at-HEAD-prompt-freeze.json`,
`at-HEAD-A1-freeze.json`, `at-HEAD-A6-freeze.json`.

The A7 record row is therefore **true at HEAD** (`refs 9`, exit 0, battery 4/4/0/1/0 — compare
`.ufo/waves/round-47/l1/scores/c1-at-A7.json`, rev `a0753786`). The first landing commit
`e856beb5` was red for 48 seconds and A2 (`62e33f7d`) repaired it — **do not cite an
`e856beb5` receipt as the target**; `fixtures/01-genuine-as-landed.json` preserves that state.

Under `--profile v2` the *as-landed* `e856beb5` block passes every structural v2 clause (the
prose cells contain the tokens) and exits 1 only through the battery's embedded v3
`genuine_green` check — the landed artefact was itself an instance of the v2 hole
(`at-landing-v2-profile.json`).

---

## 3. Green forgeries — each passes `failing == []` at exit 0

All fixtures: clone of the lane, `git -C "$D" checkout -q f54b3b6d…`, then one commit per
variant; `SKILL.md` taken from HEAD (`31b092d1`) so the pins are the live ones. Command shape:

```sh
python3 -I -B "$D/tools/round-47/exact.py" --root "$D" \
  --freeze f54b3b6de9085d3db449ed5d0916296cb29c1f6d --rev "$(git -C "$D" rev-parse HEAD)" \
  --json-out "$D/_fx/<name>.json"
```

Recipe retained byte-for-byte at `fixtures/attack5.py`
(sha256 `114d1f2cc8e893b8…`); receipts `fixtures/P*.json`; run log `fixtures/attack5-summary.json`.

### F1 — the block need not be in the craft section (`P1`)

`P1-decoy-h3-real-section-absent.json`: exit **0**; `rule_blocks 1`, `block_present 1`,
`block_is_last true`, battery `4/4/0/1/0`. The document under measurement has

* `### Queue-drain craft notes` **before** the real H2, holding the block, and
* the real `## Queue-drain craft (rounds 5-12, distilled in round 13)` with its **23 rules and no
  marker**.

`craft_section()` is `skill.split("## Queue-drain craft ", 1)[1]…` — a plain substring split, so
`### ` (index 1 of the H3 prefix), a fenced quotation, or any prose containing the heading text
takes over, and the section that ends at the next `\n## ` is the decoy's one-line body. The real
craft section is never parsed: a landing could delete rules 1–23 and this counter would still
report `met_target true`.

Cost of the same fragility in the other direction: quoting the heading earlier while landing the
block correctly reads as `block_present 0` (exit 1). Measured at `aad12c5ee779`
(`fixtures/05-fenced-quote-earlier-genuine-at-end.json`, `rule_blocks 1`, green — the block was
inserted into the quoted section, which is the same defect).

*What the claim would have to say:* clause 1 as an anchored H2 match —
`re.search(r"(?m)^## Queue-drain craft ", skill)` must match **exactly once**, the marker block
must lie inside that match's span, and the section must contain exactly 24 blocks whose last is
the marked one. Today `block_is_last` is true inside a one-block decoy.

### F2 — no declared freeze scores the landing

`at-HEAD-A1-freeze.json`: exit **2**, `reason frozen_path_changed`,
`frozen_path_changed [plans/round-47-claims.md, tools/round-47/, tools/round-47/exact.py,
tools/round-47/record.py]`, `touched [plans/round-47-claims.md, tools/round-47/exact.py,
tools/round-47/record.py]`.

The claims file declares exactly two amendments. A1: "the **declared freeze is the commit that
carries this paragraph**, i.e. the first commit whose `tools/round-47/record.py` scores the
landing's own corrections section" — a property, not a hash. A2: "Every clause, threshold and
kill rule is byte-identical to A1". There is no A3–A6 paragraph: `grep -c A6` and
`grep -c f54b3b6d` over `plans/round-47-claims.md@31b092d1` both return 0, while
`tools/round-47/exact.py` changed between A1 and A6.

So the round's rule (lines 10–11: "Nothing in this file or in `tools/round-47/` changes after the
freeze: a change makes both counters exit 2 `frozen_path_changed`") is falsified by A6, and the
only freeze under which the claim scores is an undeclared commit. `--freeze` is a caller
argument that `evaluate()` never cross-checks against anything.

*What the claim would have to say:* one literal `freeze=<40 hex>` inside `plans/round-47-claims.md`,
unchanged after the freeze, plus a clause that fails when `--freeze` differs from that literal.
Any further freeze amendment then must be a new claims file with its own literal and the whole
series disclosed — which is what A1's paragraph asks for but cannot enforce.

### F3 — the denominator is pinned to itself (`P8`)

`fixtures/P8-reduced-denominator.json`: exit **0**; battery
`forgeries_total 3 / v2_green 3 / v3_green 0 / genuine_green 1 / crash 0`;
`mutations_sha256 == mutations_sha256_expected == b7d3e477…` (sha256 over the three remaining
names), `interpreter_sha256` = sha of the edited file, freeze = the commit that carries the edit.
`fixtures/P8b-reduced-denominator-A6-freeze.json`: the same landing under `f54b3b6d` → exit **2**
`frozen_path_changed`.

The edit was three textual changes in one file — drop `("flag-order-drift", _m_flag_order)` from
`MUTATIONS`, `("forgeries_total", 4)`→`3`, `("v2_green", 4)`→`3` — plus the two pins in the block.
Every clause of the predicate is satisfied: the block still *names* `flag-order-drift` in prose,
so clause 6's "the block names all four mutation names" reads true while the list holds three.

The A6 commit is not the same act, but the counter cannot tell them apart: it edited the frozen
interpreter and the re-pin followed in `a0753786`. A6's own rule ("a change makes both counters
exit 2") is the only thing that distinguishes a clause change from a denominator change, and it
is enforced only by the caller's `--freeze`.

*What the claim would have to say:* an external anchor for the denominator. Either block 24 pins
the frozen **claims** bytes (`claims_sha256:<64 hex>`) and the counter compares the claims file's
stated `forgeries_total`/mutation names against the module, or `record.py`/`exact.py` read those
constants from `plans/round-47-claims.md@freeze` instead of from their own source. Without an
anchor outside `tools/round-47/`, the digest is a checksum of the thing it is supposed to bound.

### F4 — the executed core is not frozen (`P7 → P7b`)

`fixtures/P7-frozen-path-changed.json`: exit **2** (a committed post-freeze edit of
`plans/round-47-claims.md` inside the fixture).
`fixtures/P7b-gate-tamper.json`: same rev, same commit, **uncommitted** edit to
`$D/tools/round-46/gate.py` replacing

```
    if receipt["frozen_path_changed"]:
        receipt["reason"] = "frozen_path_changed"
        return 2, receipt
```
with `    return 0, receipt` → exit **0**, `failing []`, battery `4/4/0/1/0`,
`frozen_path_changed []`. The `ORDER`/`REVERSED` literals are untouched, so clause 7 stays green.

The dirty arm is removable the same way: `fixtures/15e-dirty-frozen-pristine-gate.json` (an
uncommitted append to `tools/round-47/record.py`) → exit 2 `frozen_worktree_dirty`,
`dirty ["tools/round-47/record.py"]`; `fixtures/15f-dirty-frozen-neutered-dirty-arm.json` (same
dirty tree + `dirty()` → `return []`) → exit **0**, byte-identical receipt to the clean baseline
`fixtures/15d-baseline-clean.json` (both `08fe83249826…`; the un-tampered dirty run `15e-…`
keeps `2e00aead66a5…`).

Why this is not covered: `## Frozen paths (exact)` lists `plans/round-47-claims.md` and
`tools/round-47/`; `freeze_state` derives its set from that section only, and `exact.py` imports
`gate` from `../round-46/`, i.e. the executing copy. `gate.py`'s own docstring names this class —
"The counters grade committed bytes, but they EXECUTE from the worktree: an uncommitted change to
a frozen tool is a different instrument (F3)" — and round 47's frozen set omits the file both
counters execute.

*What the claim would have to say:* add `tools/round-46/gate.py` to the frozen paths (and to block
24's pins, `gate_sha256:<64 hex>`), or vendor the freeze/dirty logic into `tools/round-47/`. Until
then, "same identity" holds only for bytes the set names.

### F5 — a contentless matrix is met (`P2`)

`fixtures/P2-empty-hole-cells.json`: exit **0**, battery `4/4/0/1/0`, with all four rows reading
`| R46-CL2 | - | symbol | 1 |` etc. Clause 4 binds which id each row names, clause 5 the arm
token, clause 3 the exit digit; nothing binds the `v2 hole` cell to the defect, nothing binds the
exit code to the arm (all four could say `0`), and nothing binds a row to
`corpus/lessons/round-46.md`'s own ledger text. This is R46-CL7's "binds the digits, not their
meanings" one column over.

*What the claim would have to say:* per-row, require a citation of the form
`corpus/lessons/round-46.md:<line>` whose line is the routed id's own ledger bullet (the counter
can resolve the selector and `grep -n` the id at that line), and bind the exit cell per arm
(`symbol/once/digest/order → 1`), not to `{0,1,2}`.

### F6 — two rule-24 blocks (`P4`)

`fixtures/P4-two-blocks-titled-24.json`: exit **0**, `rule_blocks 25`, one block titled
`24. Phantom rule.` inserted inside rule 23's body and the marker block still last. `block_is_last`
is an identity check against the marker's own block; nothing requires the title `24. ` to be
unique, so a reader sees two rule 24s and the counter sees one.

*What the claim would have to say:* exactly one block whose title starts `24. `.

---

## 4. Traps — a correct landing goes red

These are not defects in the artefact; they are the boundaries a landing must respect, measured
so the next drafter is not surprised.

| trap | receipt | exit |
|---|---|---|
| any craft block after block 24 (`- **25. …`) | `fixtures/P5-later-rule.json` | 1 `marker block is not the last craft block` |
| a column-zero `- **…` line **inside** block 24's body | `fixtures/12-inner-bold-in-body.json` | 1 (same) |
| the same inside a fenced code block in the body | `fixtures/13-inner-fenced-bold.json` | 1 — the split is `(?m)^- \*\*`, fence-unaware |
| the marker quoted anywhere else (even in a fence) | `fixtures/P6-marker-quoted-elsewhere.json` | 1 `marker_occurrences 2 != 1` |
| two routed ids in one trigger cell | `fixtures/19-trigger-names-two-ids.json` | 1 |
| an exit cell outside `{0,1,2}` | `fixtures/20-exit-cell-3.json` | 1 |
| a citation path with `..` (`corpus/lessons/../../SCORECARD.md:1-5`) | `fixtures/09-traversal-ref.json` | 1 — the `ALLOW` prefix test accepts it, `cited` includes it, and only git's refusal of `..` in `rev:path` makes it red: the path set is validated by string prefix, not by resolution |
| the H2 heading without its trailing space (`## Queue-drain craft`) | `fixtures/03-heading-no-trailing-space.json` | **2** `craft heading lacks its trailing space` — a landing typo is "could-not-evaluate", never red |

---

## 5. Instrument notes (no landing change)

* `--selftest` cannot run alone: `--root/--freeze/--rev` are `required=True` and argparse
  validates before `args.selftest` (`selftest.stdout.txt`, exit 2 usage). With the three dummy
  required args: `EXACT_SELFTEST: cases=16 failures=0`
  (`selftest-with-required-args.stdout.txt`, sha256 `0249b80f5808…`). The selftest's green block
  uses bare tokens, so it could not have caught the `e856beb5` defect (F1 in §2): add a red case
  whose arm cell is ``symbol: prose``.
* Determinism: two runs of the same rev produce byte-identical receipts
  (`fixtures/17-det-a.json` == `fixtures/17-det-b.json`, sha256 `defa7b901e3d…`; also
  `15d-baseline-clean.json` == `15f-dirty-frozen-neutered-dirty-arm.json`, sha256
  `08fe83249826…`, while the un-tampered dirty run `15e-…` is `2e00aead66a5…`). The battery's
  `fixtures[].v2_exit/v3_exit` are stable; no wall-clock leaks into the receipt.
* `marker_occurrences` is counted over the whole `SKILL.md` while `blocks_of` is scoped to one
  substring section — the two halves of clause 1 disagree about what "the document" is (F1).
* `tools/round-47/__pycache__/` exists on disk, ignored by `.gitignore:1`, which is why the
  `dirty` arm does not fire on every run. `-B` (as the claims command has it) is load-bearing; if
  `__pycache__/` were ever un-ignored, every run would exit 2 `frozen_worktree_dirty`.
* Causal separability holds as claimed for C1: `grep -c SCORECARD tools/round-47/exact.py` → 0.

---

## 6. Punch list for the L1

1. **Name the freeze with a literal.** `plans/round-47-claims.md` must carry
   `freeze=<40 hex>` (A6 = `f54b3b6de9085d3db449ed5d0916296cb29c1f6d`) and state that A1–A6 are a
   six-commit series, or the claim has no freeze it can be scored at (F2). The prompt's
   `5017e1f` and the file's A1 `9018c53b` both exit 2 at HEAD.
2. **Anchor clause 1 to the H2** (`(?m)^## Queue-drain craft ` exactly once; block inside that
   span; 24 blocks; unique `24. ` title) — F1/F6.
3. **Freeze or pin `tools/round-46/gate.py`** — F4; a one-line worktree edit currently flips the
   verdict with a byte-identical receipt.
4. **Give the denominator an external anchor** (claims-file mutation names / `forgeries_total`,
   or a `claims_sha256` pin in the block) — F3; today the digest checksums the object it bounds.
5. **Bind the `v2 hole` column and the exit column to the routed defect's ledger line** — F5.
6. Before cells: say the battery is **never attempted** at the freeze (`battery.skipped`), not
   that it cannot be built (`ctl-c1-2`), and state the counting command with `--no-battery` if the
   retained control omits the key; note `--json-out` must live under `--root` (§1, F10).
7. Do not cite an `e856beb5` receipt as the target: it is red on clause 5
   (`fixtures/01-genuine-as-landed.json`); A2 repaired it and A7 re-pinned the interpreter.

---

## 7. Residual risk / not run

* **Not run:** `tools/round-47/record.py` and every R47-C2 figure (out of seat).
* **Not run:** the owned-axes command A overlays (`coverage`/`depth` heads) — C2's surface.
* **Not run:** hostile-fixture sweeps beyond §3–§4 (path encodings, CRLF, non-UTF-8 bytes in
  `SKILL.md`). `show()` decodes with the default codec, so a non-UTF-8 `SKILL.md` would raise
  inside `evaluate` and exit 2 `unhandled …` (`main_guard`) — could-not-evaluate, never a pass,
  so not chased further. Round 46's `R46W1MutC1Checks` battery covered that family against
  `attest.py`, not against this counter.
* **Not run:** profile `v2` on the HEAD block (only on `e856beb5`, `at-landing-v2-profile.json`).
  The battery's own `v2_green 4` covers the four forgeries at HEAD.
* Fixture repos lived under `/fast/scratch/hyaku/kaidoku-r47/RevC1Before/` and were removed; the
  recipes (`fixtures/attack.py`, `attack2.py`, `attack3.py`, `attack4.py`, `attack5.py`) rebuild
  them from `git clone --shared` in one command, and every receipt keeps the fixture `rev` it was
  measured at.

## 8. Sources

* `plans/round-47-claims.md@5017e1f` (the freeze text this seat attacked) and `@31b092d1`
  (`grep -n "amendment"` → A1 line 23, A2 line 35; `grep -c A6` → 0).
* `tools/round-47/exact.py@5017e1f` sha256 `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`;
  `@31b092d1` sha256 `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bcb5cd5`.
* `tools/round-46/gate.py@HEAD` `freeze_state`/`dirty`/`show`/`out_path`/`scratch`.
* `SKILL.md@5017e1f` craft section (line 81 H2, 23 blocks) and `@31b092d1` block 24
  (`refs 9`, `cited` 4 documents).
* `.ufo/waves/round-47/l1/scores/c1-at-A7.json` (rev `a0753786`, `refs 9`, battery 4/4/0/1/0) —
  reproduced at HEAD.
* Receipts and recipes: this directory; per-file sha256 in `receipt-index.json`.

## 9. Tooling

No installs. `python3` 3.14 (system), `git` as present; all work under `uv`-free system tooling.
Scratch root `/fast/scratch/hyaku/kaidoku-r47/RevC1Before` with `TMPDIR`/`HYAKU_SCRATCH` set to it
(`gate.scratch` refuses `/tmp`); removed after the receipts were copied here.
