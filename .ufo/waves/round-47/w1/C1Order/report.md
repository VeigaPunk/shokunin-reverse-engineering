# C1Order — R47-C1 clause 7 (`order`): verified at the freeze, drafted, attacked, and one freeze-integrity blocker

Seat `C1Order`, wave `round-47/w1`. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Declared freeze `5017e1f7299c3a812e87e7950148f54313dd279e`; base `13a9e9e1`. Read-only on the lane
tree; every fixture is a throwaway repo under
`/fast/scratch/hyaku/kaidoku-r47/C1Order` (removed after the receipts below were copied).
No installs, no pacman, no git mutation anywhere.

## 1. The clause, quoted from both files

`plans/round-47-claims.md:80-82` (predicate 7, measured at the freeze):

> 7. `tools/round-46/gate.py` at the measured revision contains the literal
>    `"-m", "--diff-merges=first-parent"` exactly once and contains the reversed pair
>    `"--diff-merges=first-parent", "-m"` zero times.

`tools/round-47/exact.py:260-264` (the code that computes it, under `if hard:` i.e. `--profile v3`):

```python
            n_ok, n_bad = gtext.count(ORDER), gtext.count(REVERSED)
            receipt["gate_order_literal"] = n_ok
            receipt["gate_order_reversed"] = n_bad
            if n_ok != 1 or n_bad != 0:
                failing.append(f"gate.py flag order: {n_ok} correct, {n_bad} reversed")
```

with `ORDER = '"-m", "--diff-merges=first-parent"'`, `REVERSED =
'"--diff-merges=first-parent", "-m"'` (`exact.py:38-39`) and `GATE46 = "tools/round-46/gate.py"`
read through `gate.show(root, rev, path)` — i.e. the committed bytes at `--rev`, counted as a
substring over the whole file. The clause is skipped entirely under `--profile v2` (the round-46
hole the block's row measures).

## 2. At the freeze: block 24 absent, clause 7 already green

```
$ cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
$ HYAKU_SCRATCH=… TMPDIR=… python3 -I -B tools/round-47/exact.py \
    --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
    --freeze 5017e1f7299c3a812e87e7950148f54313dd279e \
    --rev    5017e1f7299c3a812e87e7950148f54313dd279e \
    --json-out .ufo/waves/round-47/w1/C1Order/receipt-freeze.json
exit 1 · stdout sha256 88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba
{"block_present": 0, "rule_blocks": 23, "marker_occurrences": 0,
 "failing": ["marker_occurrences 0 != 1", "marker_block_count 0 != 1"],
 "battery": {"skipped": "artefact fails a structural clause first"}}
```

So at the freeze the counter is red only on the marker clauses, and clause 7 **cannot fail**
because it is evaluated after the marker gate… but it is also already satisfied by the frozen
`tools/round-46/gate.py`:

```
$ git show 5017e1f:tools/round-46/gate.py | python3 -c 'import sys;t=sys.stdin.read();
  print(t.count("\"-m\", \"--diff-merges=first-parent\""),
        t.count("\"--diff-merges=first-parent\", \"-m\""))'
1 0
$ git show 5017e1f:tools/round-46/gate.py | sha256sum
c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c
```

`gate.py` is unchanged at `62e33f7d`, `2e4ae434` and `1e2c3102` (same sha256), and the ordered
literal sits on the live call at `gate.py:99`.

## 3. Candidate block 24, and the row this seat owns

`receipts/candidate-SKILL.md` = the freeze `SKILL.md` with a four-row block 24 inserted before
`## Config custody for live-probe rounds (SOP)`. Fixture repo committed from the freeze bytes of
`SKILL.md`, `plans/round-47-claims.md`, `tools/round-47/exact.py`, `tools/round-46/gate.py`,
`corpus/lessons/round-46.md`, `corpus/lessons/round-45.md`; `git -C "$D" rev-parse --show-toplevel`
asserted equal to `$D` before the first commit; counter run with `--freeze HEAD --rev HEAD`.

| variant | change to the candidate | profile | exit | failing |
|---|---|---|---|---|
| `v1-candidate-gate-clean` | none | v3 | **0** | `[]` |
| `v2-gate-order-swapped` | `gate.py` ORDER→REVERSED once | v3 | **1** | `["gate.py flag order: 0 correct, 1 reversed"]` |
| `v3-forged-order-in-comment-argv-reversed` | see §4 F1 | v3 | **0** | `[]` |
| `v4-cites-the-measured-file` | block cites `tools/round-46/gate.py:99` | v3 | **1** | `["unresolved or unvalidated citations: 1"]` |
| `v5-arm-substring-v3` | `order` → `order-ish` | v3 | **1** | `["arm cells not exact vocabulary tokens: ['symbol','once','digest','order-ish']"]` |
| `v6-worktree-draft` | the lane's own uncommitted block-24 revision | v3 | **0** | `[]` |

`v1` battery: `forgeries_total 4`, `v2_green 4`, `v3_green 0`, `genuine_green 1`, `crash 0`;
per-forgery exits `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`,
`flag-order-drift` → `v2_exit 0 / v3_exit 1` each. `receipts/variants.json`.
`v6` (the lane's in-flight draft, copied out read-only) is also `exit 0` with `refs 8`,
`unresolved []`, the same battery counts, and a matching interpreter pin (`receipts/v6.json`).

The paste-ready row, its Refs selectors and the pin values are in `rows.md`. Row verdict on the
clause's own terms: **clause 7 met by the drafted row** (arm token `order`, one routed id
`R46-CL6`, exit `1`), and the instrument red case for it is measured (`v2-gate-order-swapped`).

## 4. Attack on the clause — five findings

### F1 (clause is forgeable by a comment) — HIGH

The clause counts two substrings anywhere in the file. `receipts/forged-gate-comment-order.py`
keeps the ordered literal in a **docstring** and reverses the **live argv** under a different
spacing:

```python
    r = git(root, "log", "--diff-merges=first-parent","-m", "--name-status", "-z",
```

`count(ORDER) == 1`, `count(REVERSED) == 0` → variant `v3` scores **exit 0** with the battery
green, i.e. the block and the counter both call it clean while the gate is in the exact state
clause 7 exists to forbid. The forged module was then executed on the case-D fixture:

```
forged history_touched(['frozen.txt']) -> (['frozen.txt'], None)      # false touch
forged freeze_state exit 2 reason frozen_path_changed touched ['frozen.txt']
```

Repair shape (not this seat's to land): count the two tokens **on the live `git(` call line**
(the line containing `"log"`), or pin `gate.py`'s sha256 the way clause 8 pins the interpreter,
or both.

### F2 (the clause's stated consequence is inverted) — HIGH

`corpus/lessons/round-46.md:65-70` says the reorder "prints a merge twice (one entry per parent)
… which restores the very blindness `R45-CL6` was about". Measured on purpose-built conflict
merges (`receipts/order-semantics.json`, `order-semantics-C.json`, `order-semantics-D.json`):

- "prints a merge twice" — **true**. Case A, range base..tip: gate order 3 log entries, reversed
  order 4 (merge commit `95c0972` twice).
- "blinds the arm" — **false**. `-m` means `--diff-merges=separate`, which is a **superset** of
  `first-parent`; `history_touched` dedupes into a set, so the reversed order can only add paths.
  Case A/B: `touched` identical under both orders.
- What it actually does — **over-reports**. Case D (side branch predates the base and never
  touches `frozen.txt`; the base commit is the one that changed it; range `base..tip` therefore
  contains only side's commit and the merge): gate order → `exit 0`, `touched []`,
  `frozen_path_changed []`; reversed order → `exit 2`, `reason frozen_path_changed`,
  `touched ['frozen.txt']`, `restored ['frozen.txt']` — a frozen path the merge never touched,
  reported as touched *and* as restored.

So the order is load-bearing on the verdict (good: the clause pins something real) but the
defect class it belongs to is `false-positive attribution`, not blindness. The landed row's text
("prints a merge twice and blinds the arm", `SKILL.md` block 24 at `e856beb5`) is a record
defect of exactly the kind R46-V1..V3 routed; `rows.md` carries a corrected row that scores
identically.

### F3 (the block cannot cite the file the clause measures) — MEDIUM

Clause 8's validated path set is `corpus/lessons/`, `corpus/knowledge/`, `plans/`,
`tools/round-47/`. A block that carries the one pointer a reader needs —
`tools/round-46/gate.py:99` — fails clause 8: variant `v4` → exit 1,
`unresolved_citations: ["tools/round-46/gate.py: outside the validated path set"]`. The rule
block is therefore forced to describe the arm in prose with no resolving citation, which is the
`R45-CL9` "a citation resolves but names nothing" defect from the other side.

### F4 (clause 7 is green before the block exists, and pins only two substrings) — MEDIUM

Measured above: `tools/round-46/gate.py` is already `1/0` at the freeze, so clause 7 contributes
nothing to the landing predicate — it can only fail if `tools/round-46/gate.py` is edited, and
`gate.py` is round-46 frozen infrastructure outside this round's claimed surface. Nothing pins
`gate.py`'s bytes: any other rewrite of `history_touched` (dropping `-m`, dropping
`--name-status`, changing the range) leaves both counts intact and clause 7 green.

### F5 (the documented selftest flag is unreachable as documented) — LOW

`main()` declares `--root/--freeze/--rev` as `required=True` before testing `args.selftest`, so
`python3 -I -B tools/round-47/exact.py --selftest` exits 2 with
`error: the following arguments are required: --root, --freeze, --rev`. With three dummy
revisions the selftest does run: `EXACT_SELFTEST: cases=16 failures=0` (including
`red-flag-order-swapped`). No claim clause depends on `--selftest`, so this is a usability
defect, not a scoring one.

## 5. Freeze integrity: the declared freeze is no longer the freeze — BLOCKER

This is the round-46 `M46-3 freeze-moved` class, one round later, and it is the finding the L1
has to reconcile before the landing can be scored.

- `git log --format=%H -1 -- plans/round-47-claims.md` → **`62e33f7d`**, not the declared
  `5017e1f`. Six commits sit between them: `3186f69b` (wave-1 spec/dispatch/freeze controls),
  `9018c53b` (A1, *freeze amendment*: claims file), `e856beb5` (land block 24 + corrections),
  `62e33f7d` (A2: claims file **and** `tools/round-47/record.py`), `2e4ae434` (A3: `record.py`),
  `1e2c3102` (A4: `record.py`, 14 insertions).
- The claims file itself changed after the declared freeze: 190 lines at `5017e1f`, 211 at
  `62e33f7d`; sha256 `c8615eb8…` → `2b5d1bef…`.
- `tools/round-47/record.py` changed **three times** after the declared freeze
  (`af666ce2…` → `c704c3d4…`). `tools/round-47/exact.py` did **not** change
  (`dcef54f1…` at `5017e1f`, `62e33f7d` and `1e2c3102`), so C1's interpreter pin survives.
- Measured consequence (`receipts/cli-matrix.json`, all receipts kept):

| case | freeze | rev | exit | output |
|---|---|---|---|---|
| `freeze-self` | `5017e1f` | `5017e1f` | 1 | `block_present 0`, marker clauses only |
| `declared-freeze-at-2e4ae434` | `5017e1f` | `2e4ae434` | **2** | `frozen_path_changed: [plans/round-47-claims.md, tools/round-47/, tools/round-47/record.py]` |
| `declared-freeze-at-1e2c3102` | `5017e1f` | `1e2c3102` | **2** | same |
| `derived-freeze-self` | `62e33f7d` | `62e33f7d` | **0** | `failing []`, battery 4/4/0/1/0, `gate_order_literal 1`, `gate_order_reversed 0` |
| `derived-freeze-at-1e2c3102` | `62e33f7d` | `1e2c3102` | **2** | `frozen_path_changed: [tools/round-47/, tools/round-47/record.py]` |
| `pre-landing-rev-not-ancestor` | `62e33f7d` | `e856beb5` | **2** | `freeze is not an ancestor of rev` (A2 is a *child* of the landing) |

Consequences for the C1 claim as frozen:

1. With the declared freeze `5017e1f`, **no** rev at or after `9018c53b` can be scored: the
   counter returns 2 `frozen_path_changed`, so `failing == []` is unreachable and the target
   cannot be met at the landing revision. `controls/ctl-*` receipts taken at the freeze do not
   cover this.
2. Even the derived freeze `62e33f7d` is only scoreable **at itself**; the next commit touching
   `tools/round-47/` (A3, A4 already did) re-breaks it. Today the only green configuration is
   `--freeze 62e33f7d --rev 62e33f7d`.
3. The claims file's two definitions disagree once amended — "the commit that **first** contains
   this file" is `5017e1f`, while its own re-derivation command returns `62e33f7d`; the clause set
   it publishes (nine C1 clauses, C2's set) is the `62e33f7d` text, not the `5017e1f` text that
   the wave froze. C2 shares the substrate: its interpreter `record.py` is the frozen file that
   moved three times, so the same 2 `frozen_path_changed` applies to `record.py` runs.

What the L1 must decide (not this seat's call): declare `62e33f7d` the freeze and stop editing
`tools/round-47/`, or re-freeze once more *after* the last instrument edit and take the landing
receipt at that immediate rev. Either way the `--freeze`/`--rev` pair in the round report must be
the pair that is actually green, and the fact that A1/A2 edited a frozen path after the declared
freeze has to be stated in the report rather than absorbed (`corpus/lessons/round-46.md` M46-3,
`M46-1`).

## 6. Evidence (commands, exits, stdout sha256, UTC)

All under `python3 -I -B`, `HYAKU_SCRATCH=TMPDIR=/fast/scratch/hyaku/kaidoku-r47/C1Order`,
cwd = lane root or the fixture dir. Stdout hashes are of the counter's printed receipt.

| # | command (abridged) | exit | stdout sha256 | UTC | receipt |
|---|---|---|---|---|---|
| 1 | `exact.py --freeze 5017e1f --rev 5017e1f` | 1 | `88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba` | 17:54:17Z | `cli-freeze-self.json` |
| 2 | `exact.py --freeze 5017e1f --rev 2e4ae434` | 2 | `3381e86a327cdd04e967a720dcf7477d1ec848047eca6a42a0cfc73c1d29e265` | 17:54:17Z | `cli-freeze-moved-at-2e4ae434.json` |
| 3 | `exact.py --freeze 5017e1f --rev 1e2c3102` | 2 | `706cf11c4b17acb95c78afc1ac690addc3de81a0d479685ba4f11cd66625790f` | 17:54:17Z | `cli-declared-freeze-at-1e2c3102.json` |
| 4 | `exact.py --freeze 62e33f7d --rev 62e33f7d` | 0 | `d220eacf6418a23b4e6f2196c1901a396184ad25a04b0182fa571a35b22a765e` | 17:54:17Z | `cli-derived-freeze-self.json` |
| 5 | `exact.py --freeze 62e33f7d --rev 1e2c3102` | 2 | `98a15294e14bb03410a39fde64c0af80c1bc08e68a3bc19904f718d5e6e1dd01` | 17:54:17Z | `cli-derived-freeze-at-1e2c3102.json` |
| 6 | `exact.py --freeze 62e33f7d --rev e856beb5` | 2 | `92c356bff54e4b6374466cdfa6acc505b46ae6ff29e4a33cdbb3fd3fac1c9476` | 17:54:17Z | `cli-pre-landing-rev-not-ancestor.json` |
| 7 | `exact.py --freeze HEAD --rev HEAD` on 6 fixtures (`build.py`) | 0/1/0/1/1 | per-variant in `receipts/variants.json` | 17:50:30Z | `variants.json` |
| 8 | same on the worktree draft (`v6`) | 0 | `ffd10dc43727bdf61b698b3e3d4271fc619d2b73a3237753ecbddfb926d292d3` | 17:52:51Z | `v6.json` |
| 9 | `exact.py --root . --freeze 5017e1f --rev 5017e1f --selftest` | 0 | `EXACT_SELFTEST: cases=16 failures=0` | 17:47Z | — |
| 10 | `semantic.py`, `semantic_c.py`, `semantic_d.py` on merge fixtures | 0 | `order-semantics*.json` | 17:49-17:53Z | retained |

Fixture toplevel was asserted (`git -C "$D" rev-parse --show-toplevel` == `$D`) before the
first commit in every fixture; identity was configured per fixture (`c1order@round47`).

## 7. Not run, and limits

- Not run: `tools/round-47/record.py` (C2's counter) — another seat's surface; it is cited here
  only as the frozen file that moved (§5).
- Not run: the v2-profile control on the real landed block (`--profile v2 --rev 62e33f7d`); the
  claim says it is produced post-landing, and the battery's own `v2_green 4` covers the same
  hole from inside `run_battery`.
- No claim about `git log` semantics beyond the three measured fixtures; the superset argument
  in F2 is stated as reasoning on top of those measurements, not as a measurement itself.
- `--rev e856beb5` (the landing commit) cannot be scored under any freeze: it precedes the A2
  amendment, so `62e33f7d` is its *child*, and `5017e1f` sees A1's claims edit. Recorded as
  receipt 6, not as a failure of the block.
- The lane moved twice while this seat worked (`2e4ae434` → `1e2c3102` during the run); every
  revision above is pinned by full or 8-char hash, all measurements are deterministic (two runs
  of receipt 1 produced byte-identical JSON, sha256 `88fafc60…`).

## 8. Files written

- `.ufo/waves/round-47/w1/C1Order/rows.md` — paste-ready row, Refs selectors, pins.
- `.ufo/waves/round-47/w1/C1Order/report.md` (this file) and `…/C1Order.md` (same bytes).
- `.ufo/waves/round-47/w1/C1Order/receipts/` — `candidate-SKILL.md`,
  `forged-gate-comment-order.py`, `variants.json`, `v6.json`, `cli-matrix.json`,
  `order-semantics{,-C,-D}.json`, the four driver scripts, `MANIFEST.sha256`.
- `.ufo/waves/round-47/w1/C1Order/cli-*.json`, `receipt-*.json` — the six counter receipts.
- Installs: none.
