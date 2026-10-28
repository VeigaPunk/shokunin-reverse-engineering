# CritC1Sizing — R47-C1 attack report (round 47, wave 1)

**Verdict (one line):** the target holds at `f7d6e58` — `failing == []`, exit 0, battery
`4/4/0/1/0` — but the predicate is **too weak in four measured ways** (exit column is a digit set,
not a meaning; the `v2 hole` column is unchecked prose; the `v3 arm` column is membership-only, so
four restatements or any permutation of the four tokens pass; a dead mutation is scored as a
discriminating forgery), and `mutations_sha256` proves only that the block was copied from the
cited bytes — it does not move when a mutation's behaviour is neutered, so it does not pin the
denominator R46-CL4 asked for. Each hole closes with one clause; the closes are demonstrated below.
The prompt's freeze value (`5017e1f`) does **not** measure the claim: with any freeze earlier
than A6 it exits 2 `frozen_path_changed` at the scored revision.

All measurements are read-only against the lane. Scratch: `/fast/scratch/hyaku/kaidoku-r47/CritC1Sizing`
(removed after capture). No installs. Fixture repos are one-commit repos under scratch; every git
call names `-C <fixture>` and `rev-parse --show-toplevel` was asserted equal to the fixture dir.

Pinned measurement revision: **`f7d6e58d6e7f4e664bf443137c55ee08821de244`**.
Instrument bytes: `tools/round-47/exact.py` sha256 `01a4bca7…bc5bcd5` (A6), `SKILL.md`
sha256 `894e2864…0ebffafd`. Receipts: `receipts/` (`MANIFEST.md` has every command, exit,
stdout sha256 and UTC).

## 1. Target measurement at the pinned tip

```sh
python3 -I -B tools/round-47/exact.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze f7d6e58d6e7f4e664bf443137c55ee08821de244 --rev f7d6e58d6e7f4e664bf443137c55ee08821de244 \
  --json-out .ufo/waves/round-47/w1/CritC1Sizing/receipts/final/c1-tip-full.json
```
→ **exit 0**, stdout sha256 `1fae3f70…8d4720`, `failing []`, `rows 4`, `refs 9`,
`arm_tokens ["symbol","once","digest","order"]`, `routed_counts` each 1,
`battery {forgeries_total 4, v2_green 4, v3_green 0, genuine_green 1, crash 0}`,
`interpreter_sha256 01a4bca7…` = `interpreter_sha256_expected`, `mutations_sha256 19a2166e…`
= expected, `gate_order_literal 1`, `gate_order_reversed 0`.

Before-state reproduced: `--freeze 5017e1f --rev 5017e1f` → **exit 1**, `rule_blocks 23`,
`block_present 0`, `marker_occurrences 0`, failing `["marker_occurrences 0 != 1",
"marker_block_count 0 != 1"]` (`receipts/final/c1-before-at-freeze.json`). Matches
`controls/ctl-c1-0-do-nothing.json`.

Selftest: `--selftest` → exit 0, `cases=16 failures=0`. (It still requires `--root --freeze --rev`
because argparse marks them required — a selftest that cannot be run bare.)

## 2. The freeze argument in the counting command is stale

`--freeze 5017e1f`, the value in this seat's prompt, exits 2 at the scored revision because the
amendment series commits to frozen paths; so does every freeze earlier than A6. Measured at `--rev f7d6e58` with `--no-battery`:

| `--freeze` | exit | receipt |
|---|---|---|
| `5017e1f` (prompt) | **2** `frozen_path_changed` | `c1-freeze-5017e1f7.json` |
| `9018c53` (A1) | **2** | `c1-freeze-9018c53b.json` |
| `e856beb` (landing) | **2** | `c1-freeze-e856beb5.json` |
| `07d2894` (A5) | **2** (A6 then touched `tools/round-47/exact.py`) | `c1-freeze-07d2894e.json` |
| `f54b3b6` (A6, last frozen-path commit) | **0** | `c1-freeze-f54b3b6d.json` |
| `a075378` (pin follows A6) | **0** | `c1-freeze-a0753786.json` |

So the only admissible freeze is ≥ A6. The claims file's own definition ("Nothing in this file or in
`tools/round-47/` changes after the freeze") is now true only relative to the sixth amendment; the
file discloses A1–A2 in text and A3–A6 only in commit subjects. Every re-freeze also makes the
freeze arm trivially satisfiable (`freeze == rev` ⇒ `history_touched` is empty by construction), so
the arm proves nothing at the revision that is actually scored.

## 3. Falsifying fixtures — each scores the target **met**

All fixtures copy the lane bytes at the pinned tip and mutate only the fixture's `SKILL.md` (or its
copy of `exact.py`), then run the frozen counter with `--root <fixture> --freeze <rev> --rev <rev>`.
Driver: `receipts/scripts/attacks.py`; receipts `receipts/attacks/*.json`.

| fixture | exit | what the counter accepted |
|---|---|---|
| `ctrl-genuine` | 0 | control: the landed block, battery 4/4/0/1/0 |
| `exit-all-zero` (all four exit cells → `0`) | **0** | a row that names an arm but claims the arm returns **clean** is met; the exit column is a digit set, never a meaning |
| `v2hole-junk` (every `v2 hole` cell → `x`) | **0** | the `v2 hole` column asserts nothing |
| `arm-all-order` (all four arm cells → `order`) | **0** | four restatements of one token are a “matrix” |
| `arm-permuted` (`CL2/CL3/CL4/CL6 → order, digest, once, symbol`) | **0** | the row↔arm pairing is unverified; all 24 permutations pass (23 are the wrong pairing) |
| `refs-minimal` (`refs 4` = the same selectored citation twice + two SELF mentions; one distinct selectored path) | **0** | “at least three citations carry a line selector” is implemented as “three path matches”, SELF exempt and duplicates counted |
| `dup-id-isolating` (4 rows, `CL2` duplicated) | **1** | *not* a hole: clause 4 fails on cardinality alone — the claimed `duplicate-routed-id` forgery is merely non-isolating (it inserts a 5th row, so clause 3 also fires) |
| `dead-one` (one mutation function neutered, name kept, interpreter pin re-pinned) | **0** | a no-op is scored `v2_green += 1` and never run under v3 |
| `dead-all` (all four neutered, name list unchanged) | **0** | battery `4/4/0/1/0` with **zero** discriminating power |

`dead-all` is the headline: `_m_substring_arm/_m_duplicate_id/_m_stale_digest/_m_flag_order` each
`return block, {}`; the four names still exist, so `MUT_DIGEST` is unchanged
(`19a2166e…`), the block's `mutations_sha256` still matches, the block's `interpreter_sha256` is
updated to the edited file's sha, and `run_battery`'s no-op branch
(`exact.py:367-371`) does `forgeries_total += 1; v2_green += 1; continue` — it never scores the case
under either profile. The claims file says each forgery "is scored in a one-commit fixture repo under
both profiles"; for a no-op, that statement is false.

## 4. Is `rows == 4` a matrix, or four restatements?

- **Against block 23:** 13 rows, 52 cells, 13 distinct routed ids covering R45-CL13a–f/CL14a–f
  groups plus 7 singletons, exits `{1:9, 2:3, 0:1}`, scored by a **9**-forgery battery
  (`tools/round-46/attest.py:254`). Block 24: 4 rows, 16 cells, 4 ids, exits `{1:4}`, scored by a
  **4**-forgery battery. The round's new instrument therefore measures *fewer* forgeries than the
  one it succeeds; the advance is exactness per binding, not attack surface.
- **The four rows are genuinely distinct holes** in prose (containment, at-least-once, unpinned
  denominator, unread flag order) — not restatements. But the counter checks only two of four
  columns: ids (injective) and arm tokens (set membership). The `v2 hole` text is free and the exit
  is a digit set. With 24 id orders × 4⁴ arm assignments × 3⁴ exit assignments, **497,664** distinct
  tables satisfy clauses 2–5 against the same four ids. `arm-all-order` is one of them.
- **A matrix needs two constrained axes.** One line makes the second axis injective:
  `sorted(arm) != sorted(VOCAB)` → red. That closes restatement, not the wrong-pairing residual
  (`arm-permuted` still passes a bijection). Closing the pairing needs a second authority — either a
  `routed-id → arm` map in the counter (the block then echoes the counter) or a
  `routed-id → mutation name` map so each row's exit cell must equal that forgery's measured v3
  exit. Both are tradeoffs for the canonical judge; the block's own claim is per-row (“the clause …
  that now fails the forgery”), which is prose-verified, so the residual can be declared rather than
  duplicated. What is **not** acceptable is claiming “matrix” while any permutation passes.

## 5. `mutations_sha256` — what the pin actually proves

`MUT_DIGEST = sha256("\n".join(names))` over the counter's own `MUTATIONS` names; the same file's
bytes are pinned by `interpreter_sha256`. Since the names are a subset of the pinned bytes, the
digest is a deterministic function of bytes the block already pins. Verified:

```
names digest        19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112
block pin           19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112
four function sources (sha256)  e40a5ab1…b2cc88   <- what a behaviour pin would cover
```

- It catches an **authoring-time** mismatch: a digest transcribed from a different revision of
  `exact.py` than the interpreter pin names. That is all.
- It cannot catch a changed mutation that the interpreter pin misses (impossible: the names live in
  the file), and it does not move on a **behaviour** change (names unchanged) — `dead-all` proves it
  scores met after every mutation is neutered and the interpreter pin is re-pinned, exactly the
  A6 → `a075378` two-commit pattern (25 s apart).
- A *deletion* of a mutation is caught by `forgeries_total == 4`, not by the digest — and that
  denominator is satisfied by four dead mutations. So the pin is not the R46-CL4 denominator pin.

Smallest non-redundant close: digest the mutation **sources**, not the names, so any behaviour edit
moves the literal the block carries. Because `SKILL.md` is graded, a behaviour change then has to
appear in the graded diff instead of only inside a file the same actor re-pins.

## 6. Executed ≠ graded for `tools/round-46/gate.py`

The claims file calls gate.py “frozen infrastructure”; it is not in `## Frozen paths (exact)`, and
`dirty()` only covers the derived frozen set. The counter executes the **worktree** `gate.py` (via
`sys.path` import) while clause 7 grades the **committed** literal (`git show rev:…gate.py`).

Fixture `fx-gatesplit`: c1 base → c2 tamper `plans/round-47-claims.md` → c3 restore (rev).

| run | exit | reason |
|---|---|---|
| lane counter, clean worktree | **2** | `frozen_path_changed` (touched = restored = claims) |
| fixture counter, worktree `gate.py` with `history_touched → [], None` (uncommitted) | **0** | `touched 0`, `restored []`, clause 7 still sees the committed literal |
| fixture counter, worktree gate restored | **2** | `frozen_path_changed` |

Smallest safe correction: add every imported module (`tools/round-46/gate.py`) to the dirty/frozen
guard, or grade the executed bytes (`inspect.getsource` / read the resolved module file) instead of
`git show`.

## 7. The cited v2 control does not contain the number it is cited for

`controls/ctl-c1-1-v2-profile.json` (cited by the claims for “`v2_green 4` — the four holes
measured”) has **no `battery` key** and no `v2_green`; it is a `--no-battery` run of the *genuine*
block under `--profile v2` (`met_target true`, `failing []`). The number is producible — at the
pinned tip, `--profile v2` with the battery gives `v2_green 4, v3_green 0, genuine_green 1`
(`receipts/final/c1-v2-profile-repro.json`, exit 0) — but the receipt on file does not show it. This
is a stale control, not a false measurement; re-run it or correct the claims text.

## 8. Smallest safe corrections (demonstrated on copies, not the frozen file)

`receipts/scripts/fixdemo.py` applies four one-clause edits to a copy of `exact.py` per fixture and
re-scores the same attacks; the landed block still scores met under all four.

| case | landed | with the clauses |
|---|---|---|
| genuine block | 0 | **0** |
| `exit-all-zero` | 0 | **1** `exit cells outside {0,1,2}: 4` (exit `{1,2}` for a row that names an arm) |
| `arm-all-order` | 0 | **1** `arm cells are not the four tokens once each` |
| `refs-minimal` | 0 | **1** `selectored citations 2 < 3` |
| `dead-all` | 0 | **1** `battery v2_green 0 != 4`, `battery crash 4 != 0` |
| `arm-permuted` | 0 | **0** — residual, see §4 |

The `dead-all` close is the no-op branch: `crash += 1` instead of `v2_green += 1`. That is one line
and turns a dead forgery into a counter defect rather than a pass.

## 9. What I did not run

- Did not run `--profile v2` on each forgery individually (the battery already reports `v2_exit 0`
  for all four; `c1-v2-profile-repro` reproduces `v2_green 4`).
- Did not re-derive C2 or the record; that is another seat.
- Did not test the `git merge --squash` blind spot (R46-CL1, declared unclosed).
- Did not modify any lane file; the frozen counter and block are untouched. All writes are under
  `.ufo/waves/round-47/w1/CritC1Sizing/`. During capture the lane worktree carried uncommitted
  changes to `SCORECARD.md` and `corpus/lessons/round-47.md` (not mine; C1 reads neither); the
  frozen paths were clean at every run, so no receipt is `frozen_worktree_dirty`.

## 10. What the claim buys (one paragraph)

Four exact bindings replace four loose ones — arm tokens by equality instead of substring, routed
ids exactly once instead of at-least-once, a mutation-list literal beside the interpreter pin, and a
flag-order literal clause — and each is demonstrated by a forgery that the weakened (v2) profile
accepts. That is a real, if narrow, depth step: the four routed *instrument* defects now have
mechanical kill cases. It does not buy a matrix (one injective column), an exit that means anything,
a denominator that survives a silent behaviour edit, or a freeze arm that is live at the scored
revision. The cheapest honest framing for the landing is “four exact bindings, four measured
forgeries”, not “exactness matrix”, unless the arm-bijection and no-op clauses land first.
