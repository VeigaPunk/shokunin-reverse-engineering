# RevIntent — does R47-C1 clause 7 protect R46-CL6's arm, or only its spelling?

Seat `RevIntent`, round 47 wave 1, lane `kaidoku-shokunin`.
Measured against the freeze `5017e1f7299c3a812e87e7950148f54313dd279e`; base
`13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`; git 2.56.0 (`receipts/01-git-version.out`).
The clause text read and attacked here is the **current** one at HEAD `09a9f912`
(`tools/round-47/exact.py` sha256 `01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5`),
i.e. after the disclosed amendment series A1–A6; `git diff 5017e1f HEAD -- tools/round-47/exact.py`
shows the amendments do not touch ORDER/REVERSED or the clause-7 block (A6 changed the
fixture file list only), so the verdict is stable across the series.
Read-only on the lane: no lane file was edited; every fixture lived under
`/fast/scratch/hyaku/kaidoku-r47/RevIntent/` and every fixture asserted
`git -C "$D" rev-parse --show-toplevel == $D` before its first commit.

**Verdict (one line).** Clause 7 protects the **spelling** of the arm —
`"-m", "--diff-merges=first-parent"` present once and its reverse absent, in `gate.py`'s
committed bytes at `--rev` — and it does protect that one thing correctly. It does not
protect the arm: two minimal forgeries keep the whole C1 counter green while the executed
history arm is reversed, and a third keeps it green while the arm returns nothing at all.
Separately, the lesson's stated *harm* ("restores the very blindness `R45-CL6` was about")
is falsified by measurement: reversal never narrows what the arm sees.

---

## 1. The question, made checkable

The seat brief asks whether R47-C1 clause 7 protects "the arm the lesson describes, or only
its spelling". That decomposes into four sub-questions, each answered below with a command:

| # | sub-question | answer |
|---|---|---|
| Q1 | What did R46-CL6 actually measure and prescribe? | §2 — three historical voices, one of which contradicts the other two |
| Q2 | What does the arm *do*, per git's own documentation and per measurement? | §3 — order selects the merge-diff **mode** |
| Q3 | What does clause 7 test? | §4 — a byte census over committed `gate.py` at `--rev` |
| Q4 | Can a gate whose arm is reversed / removed pass clause 7? | §5 — yes, both; receipts 06, 07, 10 |

## 2. Historical record: what R46-CL6 said, and in which voice

### 2.1 The measurement (wave-1 seat `R46W1ScribeSource`)

`.ufo/waves/round-46/w1/R46W1ScribeSource.md:87-93` — F4, verbatim:

> **F4 — the arm is order-sensitive and nothing pins the order.** Measured, same fixture:
> `-m` alone → merge emitted twice (per-parent `separate` output); `-m` then
> `--diff-merges=first-parent` → once; `--diff-merges=first-parent` then `-m` → twice again.
> `tools/round-46/gate.py:99` passes them in the working order (`-m` first), so the frozen arm
> is correct as written, but a reorder would silently **widen** the arm to per-parent diffs and
> still exit 0. `--diff-merges=first-parent` alone produces the same single entry (the `-m` is
> redundant for this arm, not harmful).

Its measured table (`.ufo/waves/round-46/w1/R46W1ScribeSource/row.md:99-109`) and the raw
probe (`.ufo/waves/round-46/w1/R46W1ScribeSource/receipts/arm_probe.out`) agree:

> | plain | `git log --name-status -1` | no file entry at all |
> | documented value | `--diff-merges=first-parent --name-status` | one entry, `M f.txt` |
> | `-m` only | `-m --name-status` | **two** entries (default `separate`), `M f.txt` twice |
> | reversed order | `--diff-merges=first-parent -m --name-status` | **two** entries — identical to `-m` only |
> | gate.py's order | `-m --diff-merges=first-parent --name-status -z` | one block, `M \0 f.txt \0` |

The seat's conclusion: *widen*. Its recommendation: "nothing in the frozen instrument or in
block 23's `merge` row records the ordering dependency" — routed for the L1.

### 2.2 The lesson (the routed defect the round-47 claim is built on)

`corpus/lessons/round-46.md:65-72`, verbatim:

> - **R46-CL6.** `gate.history_touched` passes `-m --diff-merges=first-parent`, and the arm is
>   **order-sensitive**: `git log --diff-merges=first-parent -m` prints a merge twice (one entry
>   per parent) because the later flag wins, which **restores the very blindness `R45-CL6` was
>   about**. The order is correct today and nothing in the code enforces it; one argument reorder
>   silently undoes the arm. Wave-1 seat `R46W1ScribeSource` measured this on a deterministic
>   merge fixture. **Round 47: assert the flag order in a selftest case.**

Two things moved between the seat and the lesson: "widen" became "restores the very blindness",
and "record the ordering dependency" became "assert the flag order in a selftest case".

### 2.3 The craft row that carried it forward

`SKILL.md:639` (block 23, the round-46 matrix):

> | R46-CL6 one flag reorder (`--diff-merges=first-parent -m`) prints a merge twice **and blinds the arm** | the argument order is a convention no clause reads | `order` | 1 |

### 2.4 The round-47 claim built on it

`plans/round-47-claims.md:59-60` repeats the lesson's framing ("order-sensitive and nothing
enforces the order"); `:72-73` states the gap the round closes ("the flag order that makes the
history arm see a merge resolution is a code detail no clause reads"); `:101-103` is the clause:

> 7. `tools/round-46/gate.py` at the measured revision contains the literal
>    `"-m", "--diff-merges=first-parent"` exactly once and contains the reversed pair
>    `"--diff-merges=first-parent", "-m"` zero times.

So the **intent reconstructed from history** is: *the history arm must select the
first-parent merge mode; that mode is selected by the order of two argv tokens; nothing
pinned the order; pin it so a reorder cannot silently change the arm.* The lesson's chosen
instrument was a selftest case; the claim's chosen instrument is clause 7.

## 3. What the arm is, and what the order actually selects

The frozen arm, `tools/round-46/gate.py` (identical bytes at base, freeze and worktree:
sha256 `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c`,
`receipts/02-gate-hashes.out`, `receipts/11-clause7-counts-real-bytes.out`):

```python
def history_touched(root, base, tip, paths):
    """Every path under `paths` that any commit in base..tip touched, merges included.

    `--diff-merges=first-parent` makes a merge show the diff it introduced on the
    first-parent side, which is exactly the resolution edit R45-CL6 could not see.
    """
    if not paths:
        return [], None
    r = git(root, "log", "-m", "--diff-merges=first-parent", "--name-status", "-z",
            "--format=", f"{base}..{tip}", "--", *paths, binary=True)
```

Git 2.56.0's own documentation (`receipts/03b-doc-m-clean.out`,
`receipts/04b-doc-diffmerges-clean.out`, rendered from `/usr/share/man/man1/git-log.1.gz`):

> **-m**
>   Show diffs for merge commits in the default format. This is similar to
>   `--diff-merges=on`, except -m will produce no output unless -p is given as well.

> **--diff-merges=<format>**
>   Specify diff format to be used for merge commits. …
>   **on, m** — Make diff output for merge commits to be shown in the default format. The
>   default format can be changed using `log.diffMerges` configuration variable, whose
>   default value is `separate`.
>   **first-parent, 1** — Show full diff with respect to first parent. This is the same
>   format as `--patch` produces for non-merge commits.
>   **separate** — Show full diff with respect to each of parents. Separate log entry and
>   diff is generated for each parent.

Therefore `-m` and `--diff-merges=…` write the *same* setting, and the last one on the
command line wins. `-m` first → mode `first-parent`; `-m` last → mode `on`, i.e.
`log.diffMerges`, default `separate` (two entries per merge).

Reproduced end-to-end on scratch fixture `fx-evil` (a merge whose resolution differs from
both parents; `receipts/05-raw-arm-table.out`, `receipts/06-probe1.out`):

```
gate order (-m --diff-merges=first-parent)   exit=0 tokens=4  sha256=fa3d14ebf94c1c22…
reversed   (--diff-merges=first-parent -m)   exit=0 tokens=6  sha256=33a406abc6cc8cfc…
fp only    (--diff-merges=first-parent)      exit=0 tokens=4  sha256=fa3d14ebf94c1c22…
```

`reversed` emits the merge twice; `fp only` is **byte-identical** to the frozen arm. Both
match the seat's 2026-10-28 measurement and the documented semantics. Q2 answered: the
order selects the mode; the frozen order selects `first-parent`.

## 4. What clause 7 actually tests

`tools/round-47/exact.py:38-39` and `:256-264` (HEAD):

```python
ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'
...
        gtext = files(GATE46)
        if gtext is None:
            failing.append("gate.py absent at rev")
        else:
            n_ok, n_bad = gtext.count(ORDER), gtext.count(REVERSED)
            receipt["gate_order_literal"] = n_ok
            receipt["gate_order_reversed"] = n_bad
            if n_ok != 1 or n_bad != 0:
                failing.append(f"gate.py flag order: {n_ok} correct, {n_bad} reversed")
```

`files` is `lambda p: gate.show(root, rev, p)` (`exact.py:406`) — the **committed** blob at
`--rev`, not the bytes that execute. The test is a substring census over the whole file: no
AST, no function identity, no execution, no config read. It cannot distinguish the call
argument of `history_touched` from a comment, a docstring, a dead copy or a variable name.

Scope check (`receipts/09-frozen-set.out`): round-47's frozen set at the freeze is
`[('plans/round-47-claims.md', False), ('tools/round-47', True)]` — **`tools/round-46/gate.py`
is not frozen by round 47**, so round-47's `freeze_state` never asks whether the executing
gate is dirty. Q3 answered: a byte census over committed bytes.

## 5. Does the census protect the arm? Measured, five ways

Harness: the real frozen `exact.py` `score(profile="v3")` and the real `gate.history_touched`,
run over one-commit fixture repos built by `exact._repo` with a genuine block
(`exact.skill_text(exact.good_block())`). Variants differ only in `tools/round-46/gate.py`.
Receipts `06-probe1.out`, `07-probe2.out`, `probe.json`, `probe2.json`, `fuzz.json`.

### 5.1 Two forgeries pass the whole counter with a reversed arm

```
genuine              exit=0 literal=1 reversed=0 failing=[]
reversed             exit=1 literal=0 reversed=1 failing=['gate.py flag order: 0 correct, 1 reversed']
forge_comment_var    exit=0 literal=1 reversed=0 failing=[]      # arm reversed, counter green
forge_slice          exit=0 literal=1 reversed=0 failing=[]      # arm reversed, counter green
```

* `forge_comment_var` — the pinned adjacency lives in a **comment**; the executable call
  passes the mode through a module name, in reversed order:
  `# pinned order (R46-CL6): "-m", "--diff-merges=first-parent"` … `"log", MERGE_MODE, "-m", …`.
* `forge_slice` — the pair is stored once and applied reversed at the call:
  `MERGE_ARGS = ("-m", "--diff-merges=first-parent")` … `"log", *MERGE_ARGS[::-1], …`.

The arm really changed (fixture `fx-oldbranch`, where the merge's second parent forked before
the freeze):

```
genuine              touched=['other.txt']
reversed             touched=['frozen.txt', 'other.txt']
forge_comment_var    touched=['frozen.txt', 'other.txt']
forge_slice          touched=['frozen.txt', 'other.txt']
```

In `gate.freeze_state` this is a verdict flip: on a history where no commit in `base..tip`
touches `frozen.txt`, the frozen arm returns `0` and the forged arms return `2
frozen_path_changed`. Clause 7 stays green for both forgeries.

### 5.2 A gate whose arm has disappeared passes the whole counter

`arm_disabled` — the identical bytes plus `return [], None` after the call:

```
arm_disabled   freeze_state exit=0 reason=None  touched=[]   literal=1 reversed=0
               exact.py exit=0 failing=[]
```

On fixture `fx-restore-merge` (tamper of a frozen path, then the **merge resolution restores
it**, so the blob arm is clean at both ends and only the history arm can witness it —
`trees identical at both ends for frozen.txt: True`):

```
genuine        freeze_state exit=2 reason=frozen_path_changed touched=['frozen.txt']
reversed       freeze_state exit=2 reason=frozen_path_changed touched=['frozen.txt']
forge_slice    freeze_state exit=2 reason=frozen_path_changed touched=['frozen.txt']
arm_disabled   freeze_state exit=0 reason=None                touched=[]
```

This is the exact R45-CL6 class the arm exists for. Clause 7 cannot see its removal.

### 5.3 Worktree drift is invisible to round 47

`receipts/10-worktree-dirty-gate.out`: committed `gate.py` correct, worktree copy reversed
(the bytes that would execute), round-47 claims:

```
freeze_state_exit: 0      frozen_derived: ["tools/round-47/", "plans/round-47-claims.md"]
dirty_frozen_paths: []    dirty gate.py when asked directly: ["tools/round-46/gate.py"]
exact_exit: 0             clause7_counts: [1, 0]
```

The round-46 residual (R46-CL10: "the executing bytes are not pinned, only the examined
ones") reappears through round-47's different frozen set. Low severity — the lane's counters
execute from the worktree only under an operator's hand — but it is the same class.

### 5.4 Two behaviour-preserving spellings are scored red

```
fp_only   (drop the redundant `-m`)  exit=1 failing=['gate.py flag order: 0 correct, 0 reversed']
fp_one    (--diff-merges=1)          exit=1 failing=['gate.py flag order: 0 correct, 0 reversed']
doc_quoted (arm correct, docstring quotes the pair) exit=1 failing=['gate.py flag order: 2 correct, 0 reversed']
```

`fp_only` is **byte-identical in output** to the frozen arm (`sha256 fa3d14eb…`, §3) and the
seat recorded the `-m` as redundant; `--diff-merges=1` is the same documented value (one
shared `<dd>` in git-log(1); also `.ufo/waves/round-46/w1/R46W1ScribeSource.md` F6). A gate
cleaned either way fails C1. And `doc_quoted` shows the census is also breakable by prose:
quoting the pair once in the module docstring of a **correct** file yields `literal=2` and
exit 1. The verdict is a function of bytes and prose, in both directions — not of behaviour.

### 5.5 The claimed harm is in the wrong direction

The lesson and block 23 say a reversal *blinds*. Measured:

* On `fx-restore-merge` — the resolution edit the arm exists to see — genuine and reversed
  **both** report `frozen.txt` (§5.2). No blindness.
* Reversal can only add the second-parent diff, which `separate` always includes alongside
  the first-parent one, so the touched set is a **superset**: 24/24 randomly generated merge
  fixtures produced identical touched sets (`fuzz.json`: `{'equal': 24, 'reversed_wider': 0,
  'reversed_narrower': 0}`); the only strict difference observed was `fx-oldbranch`, where
  reversal **added** a path (§5.1) — a false positive, i.e. a wider arm, exactly as the seat
  wrote.
* `log.diffMerges=combined` does not change this on the fixture tested (`probe.out`), because
  the merge's first-parent diff is not the only witness in any of these shapes.

[INFERENCE] The superset argument is structural (`separate` = diff vs each parent ⊇ diff vs
first parent), and was not tested on octopus merges or with rename detection. The claim
"reversal never narrows" is therefore high-confidence, not proved for every repository
shape. The claim "reversal blinds on the gate's actual command" is falsified on both
handcrafted shapes and all 24 fuzz fixtures.

## 6. Answer to the seat question

**Clause 7 protects the spelling of the arm, not the arm.**

What it does protect, correctly: the one failure mode the seat actually measured — a
*committed, literal* swap of the two argv tokens in the call — turns C1 red (verified:
`reversed` exit 1). Since that swap is what selects `separate` over `first-parent`, clause 7
does bind the mode-selection mechanism at the source-text level.

What it cannot protect:

1. the same reversal expressed through indirection (name, slice, helper) — counter green;
2. removal or short-circuit of the arm — counter green, and the gate silently passes the
   tamper+restore class the arm was built for;
3. the executing bytes when the worktree copy differs (gate.py is outside round-47's frozen
   set);
4. behaviour-preserving rewrites — it *rejects* them, so green is not evidence of a working
   arm any more than red is evidence of a broken one.

And the harm it is justified by is mis-stated: reversal widens or equals, never blinds. The
lesson's own remedy ("assert the flag order in a selftest case") was not implemented by
clause 7; clause 7 is a source census, and a census cannot be a selftest.

## 7. For the L1 (nothing here asks for a change to frozen bytes)

1. **Block 24's R46-CL6 row should not repeat "blinds".** The measured effect is: the
   reversed pair selects `separate` (`-m` = `--diff-merges=on`, default format
   `log.diffMerges=separate`), so the merge is emitted once per parent. Write the hole as
   "one argument reorder selects per-parent diffs (duplicate merge entries; wider touched
   set)" — that is what receipts 05/06/07 and the round-46 seat's own table support. Keeping
   "blinds" in the landed block would put a falsified mechanism claim into a verified
   surface.
2. **If the intent is to protect the arm rather than its spelling**, the clause that does it
   is behavioural and cheap: build a fixture merge where a frozen path is tampered and then
   restored *inside the resolution*, run `gate.history_touched` from the measured `gate.py`,
   and require the path to be returned (genuine → `['frozen.txt']`; `arm_disabled` → `[]`;
   `forge_slice` → detects). Recipe and fixtures: `probe2.py` §build, receipt
   `07-probe2.out`. This alone would kill §5.2 and §5.1.
3. **If clause 7 stays as is**, treat it as a mode pin, and add `tools/round-46/gate.py` to
   the round's frozen paths (or pin its sha256 in the block) so §5.3 closes as well; and
   expect the two false reds of §5.4 when anyone cleans the arm.
4. Clause 7's two literals are fine as written — they fire exactly on the committed swap and
   nowhere else in the frozen bytes (`receipts/11-clause7-counts-real-bytes.out`: order 1,
   reversed 0 at base, freeze and worktree).

## 8. Confidence

| finding | confidence | basis |
|---|---|---|
| order selects the merge-diff mode; last flag wins; frozen order = `first-parent` | high | docs quoted + 5-arm reproduction + seat's 2026-10-28 probe |
| clause 7 is a substring census over committed bytes at `--rev` | high | source read, `exact.py:256-264`, `:406` |
| two forgeries and the disabled arm pass the full counter | high | `exact.score` exit 0 in receipts 06/07 |
| reversal never narrows the touched set | high, not proved | structural argument + 24/24 fuzz; no octopus/rename test [INFERENCE] |
| "blinds the arm" in the lesson/block 23 is unsupported | high for the tested shapes | §5.2, §5.5 |
| worktree drift escapes round-47 scope | high | receipt 10 |
| gap 1 (indirection) is exploitable in a landing, not only in a fixture | medium | requires a landing that edits `gate.py`; no such landing exists at the freeze (bytes unchanged base→freeze) [INFERENCE] |

## 9. Receipts

All under `.ufo/waves/round-47/w1/RevIntent/`; `receipts.json` carries the exact command,
UTC, exit, stdout sha256. `04-*`/`03-*` are the raw troff renders; `03b-*`/`04b-*` are the
same pages rendered by `man` for quotation.

| receipt | exit | stdout sha256 (first 16) | UTC | bytes |
|---|---|---|---|---|
| 01-git-version | 0 | c9e40977101870d1 | 2026-10-28T18:00:52Z | 19 |
| 02-gate-hashes | 0 | e0578242f405591c | 2026-10-28T18:00:52Z | 316 |
| 03-doc-m-sentence | 0 | e20994b1663ac031 | 2026-10-28T18:01:04Z | 163 |
| 04-doc-diffmerges | 0 | 99a4369b6d65301a | 2026-10-28T18:01:04Z | 862 |
| 05-raw-arm-table | 0 | 3c2a85e051687254 | 2026-10-28T18:00:52Z | 857 |
| 06-probe1 | 0 | 744ff009db5f25e5 | 2026-10-28T18:00:52Z | 2410 |
| 07-probe2 | 0 | 8065c4083f615d63 | 2026-10-28T18:00:52Z | 1057 |
| 08-exact-selftest | 0 | 0249b80f58085f0d | 2026-10-28T18:00:53Z | 2840 |
| 09-frozen-set | 0 | 5d8dd1edfa43c9c7 | 2026-10-28T18:00:53Z | 72 |
| 10-worktree-dirty-gate | 0 | face97008c666a32 | 2026-10-28T18:01:44Z | 274 |

Supporting files copied with the receipts: `probe.py`, `probe2.py`, `probe.json`,
`probe2.json`, `fuzz.json`, `probe.out`, `probe2.out`, `11-clause7-counts-real-bytes.out`.
`exact.py --selftest` is 16/16 green (`receipts/08-exact-selftest.out`); its only order case
is the text case `red-flag-order-swapped`, and no case exercises the arm's behaviour — which
is why the four gaps above are invisible to the counter.

**Not run, so not passed:** no count of the counter at the landing revision (none existed
during this wave); no octopus-merge or rename-detection shape; no `log.diffMerges` sweep
beyond `combined` on one fixture; no `attest.py`/`registry.py` run (not this seat's surface).

## 10. Touched surfaces

- `.ufo/waves/round-47/w1/RevIntent.md` (this report) and `.ufo/waves/round-47/w1/RevIntent/`
  (receipts, probes, JSON).
- Scratch `/fast/scratch/hyaku/kaidoku-r47/RevIntent/` (removed after the receipts above were
  copied out; nothing under `/tmp` was used).
- No edit to `SKILL.md`, `plans/`, `tools/`, `corpus/`, `LOG.md`, `SCORECARD.md`, `.ufo/state/`,
  `.ufo/watchdog.log`, `.scratch/`, the fleet repo or any sibling lane. Git use was read-only
  (`show`, `rev-parse`, `log`, `rev-list`, `merge-base`, `diff-tree`), except inside scratch
  fixtures whose toplevel was asserted before the first commit. No tool installed.
