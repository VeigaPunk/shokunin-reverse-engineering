# C1FreezeWindow — report (round 47, wave 1)

Seat: `C1FreezeWindow`, leaf executor. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (below: `$L`). Zero writes to the lane tree
outside `.ufo/waves/round-47/w1/C1FreezeWindow/`; no commits, no `git add`, no jj. Scratch root
`/fast/scratch/hyaku/kaidoku-r47/C1FreezeWindow` (`$S`), removed after these receipts were copied
here. No tool installs (nothing was needed; no pacman / uv / npx ran).

Frozen bytes were read, never modified: `tools/round-46/gate.py` sha256
`c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c`,
`tools/round-47/exact.py` sha256 `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`
(identical at `5017e1f7`, at every tip measured, and in the worktree). git 2.56.0.

---

## 1. The four window commands, exactly as run

`$F = 5017e1f7299c3a812e87e7950148f54313dd279e`, pathspec `tools/round-47 plans/round-47-claims.md`.

**Argument order used (both real-lane commands):** `--name-status --format= -m --diff-merges=first-parent`.
The relative order that matters is `-m` **before** `--diff-merges=first-parent`; that matches
`tools/round-46/gate.py:99` (`"log", "-m", "--diff-merges=first-parent", "--name-status", "-z", "--format="`).
The reversed form used in C3/C4 is `--name-status --format= --diff-merges=first-parent -m`.
Every command was the single-sourced trio `emit c1..c4` in `receipts/windows.sh`; outputs are
`receipts/win-c{1,2,3,4}-*.out`, log `receipts/windows.log`.

| # | window | flag order | exit | stdout bytes | stdout sha256 | UTC |
|---|---|---|---|---|---|---|
| C1 | `$F..$F` | `-m --diff-merges=first-parent` | 0 | **0** | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` | 2026-10-28T17:52:24Z |
| C2 | `$F..3186f69b` | `-m --diff-merges=first-parent` | 0 | **0** | `e3b0c442…b855` | 2026-10-28T17:48:33Z |
| C2 | `$F..62e33f7d` | `-m --diff-merges=first-parent` | 0 | **108** | `35eb003b4602eecd2b5627221c1db16e021de4def353a2df4c26c923f4a87865` | 2026-10-28T17:52:24Z |
| C2 | `$F..1e2c3102` | `-m --diff-merges=first-parent` | 0 | **162** | (see `receipts/snapshot-window.out`) | 2026-10-28T17:53:20Z |
| C3 | `$F..$F` | `--diff-merges=first-parent -m` | 0 | **0** | `e3b0c442…b855` | 2026-10-28T17:52:24Z |
| C4 | `$F..62e33f7d` | `--diff-merges=first-parent -m` | 0 | **108** | `35eb003b…7865` (byte-identical to C2) | 2026-10-28T17:52:24Z |

Nothing was written to stderr (`stderr_bytes=0` everywhere).

**Reading of C1/C3.** A range whose two endpoints are the same commit is empty for every
pathspec and every flag order — measured, 0 bytes, and it carries **zero tampering information**.
It is a spelling check on the pathspec, nothing more. The informative window is C2/C4 plus the
worktree-clean arm.

**Reading of C2.** The window was empty at tip `3186f69b` and **is no longer empty**. At
`62e33f7d` it prints, twice each:

```
M	plans/round-47-claims.md
M	tools/round-47/record.py
```

and at `1e2c3102` it is 162 bytes over 6 lines (`2× plans/round-47-claims.md`,
`4× tools/round-47/record.py`; `receipts/snapshot.log`). The commits are disclosed freeze
amendments A1–A4: `9018c53b`, `62e33f7d`, `2e4ae434`, `1e2c3102` — four of the six commits in the
window touch the round's own frozen paths. **The premise "the frozen window is empty for the
round's own paths at the current tip" is false as of 17:52:24Z**, and it stopped being true
between 17:48:33Z and 17:52:24Z while this seat was measuring.

**Reading of C3/C4.** On the real lane the two orders agree byte-for-byte, because
`git rev-list --merges $F..$T | wc -l` = 0 (**zero merges in the window**). The lane has 2 merges
in total, both before `$F`. So the real window does **not** exercise the flag-order arm at all:
its emptiness today is order-insensitive and therefore no evidence about R46-CL6.

## 2. R46-CL6, measured (not asserted): the order defect on a two-parent merge

Fixture recipe (deterministic construction, per-run SHAs): `receipts/probe2.sh` (fx2),
`receipts/probe3.sh` (fx3, adds a real `## Frozen paths (exact)` claims file so
`gate.freeze_state()` runs end to end), `receipts/probe4.sh` (fx4, the tamper case).
`git -C "$D" rev-parse --show-toplevel` was asserted equal to `$D` before the first commit in
each fixture; identity was set locally only.

Shape: base `B` = side tip, which already carries `tools/round-47/frozen.txt = SIDE`; second
parent `P2` (main) carries `V1`; the merge `M` resolves the path to the **side** bytes, i.e.
`blob@B == blob@M` (`713f333f…`) while `blob@P2 = 998a6f80…`. No plain commit in `B..M` touches
the path (`git log --name-status B..M -- …` is empty), so the only thing that can name it is the
merge-vs-second-parent diff.

fx2: `B=d351d7f8…`, `P2=40374b2a…`, `M=89f14452…`.
fx3: `B=94205f0a…`, `M=4f8cf079…`.

| run | argv tail | exit | bytes | sha256 | names |
|---|---|---|---|---|---|
| frozen order | `--name-status --format= -m --diff-merges=first-parent` | 0 | **0** | `e3b0c442…b855` | — |
| reversed order | `--name-status --format= --diff-merges=first-parent -m` | 0 | **28** | `b73e1327e459d3fad46581163d1a3bcf5d9c13cbede74c55752a7e1e34fcc728` | `M tools/round-47/frozen.txt` |
| correct literal + trailing `-m` | `… -m --diff-merges=first-parent -m` | 0 | 28 | `b73e1327…` | same |
| correct literal + trailing `--diff-merges=separate` | `… --diff-merges=separate` | 0 | 28 | `b73e1327…` | same |
| correct order, reformatted across lines | — | 0 | 0 | `e3b0c442…` | — |

Through `tools/round-46/gate.py` itself (module imported from the lane; `receipts/gatem.py`,
`receipts/gate-arms.json`), on the identical fixture:

| variant of gate.py | `history_touched` | `blob_changed` | `restored` | `freeze_state` |
|---|---|---|---|---|
| frozen (`-m` first) | `[]` | `[]` | `[]` | **exit 0** |
| reversed (`-m` last) | `["tools/round-47/frozen.txt"]` | `[]` | `["tools/round-47/frozen.txt"]` | **exit 2 `frozen_path_changed`** |
| forged: correct literal, trailing `-m` | `["tools/round-47/frozen.txt"]` | `[]` | same | exit 2 |
| forged: correct literal, trailing `--diff-merges=separate` | `["tools/round-47/frozen.txt"]` | `[]` | same | exit 2 |
| reformatted, correct order | `[]` | `[]` | `[]` | exit 0 |

So R46-CL6 is real and it is a **false-violation** direction, not a blind spot: the reversed order
never loses a path, it invents one, and `restored = touched − changed` then reports a frozen path
as tampered-and-restored on a tree whose frozen bytes are net-identical (`blob_changed == []`).
`git 2.56.0` implements this as last-`--diff-merges`-wins: `-m` after `--diff-merges=first-parent`
selects `separate`.

## 3. Falsification of R47-C1 clause 7 (frozen clause, reported not edited)

Clause 7 is `exact.py:256-264`: `n_ok = gtext.count(ORDER)`, `n_bad = gtext.count(REVERSED)`,
require `n_ok == 1 and n_bad == 0`, over `GATE46 = "tools/round-46/gate.py"` at `--rev`, with
`ORDER = '"-m", "--diff-merges=first-parent"'` and
`REVERSED = '"--diff-merges=first-parent", "-m"'`. Measured with exact.py's **own constants**
(`receipts/gatem2.py`, `receipts/clause7-and-freeze-derivation.json`):

| gate.py text | `count(ORDER)` | `count(REVERSED)` | clause 7 | effective `--diff-merges` | text sha256 |
|---|---|---|---|---|---|
| frozen file | 1 | 0 | **green** | first-parent | `c3ba6b93…897c` |
| reversed | 0 | 1 | red (correct) | first-parent (order-ignored semantics) | `e2d3472f…5869` |
| **forged: correct literal + trailing `"-m"`** | 1 | 1 | red | separate | `ffb4e00f…4170` |
| **forged: correct literal + trailing `"--diff-merges=separate"`** | 1 | 0 | **GREEN** | **separate** | `75523f78…8e61` |
| **reformatted, correct order** | 0 | 0 | **red** | first-parent | `1d2ebac5…e646` |

Two defects, opposite directions, both reproducible from `receipts/gate_forged_trailing_separate.py`
and `receipts/gate_reformatted_correct_order.py`:

- **F1 (bypass).** Append `"--diff-merges=separate"` after the pinned pair — a one-token edit that
  leaves `count(ORDER)==1` and `count(REVERSED)==0` — and clause 7 stays green while git runs the
  hole back. Reproduce: `python3 -I -B /fast/…/gatem2.py` against fx2/fx3, or diff
  `receipts/gate_forged_trailing_separate.py` against `tools/round-46/gate.py`. Consequence: the
  v3 arm binds a **source substring**, not the effective option order, so the R46-CL6 defect it
  claims to close is still reachable inside a gate.py that passes clause 7.
- **F2 (over-strict).** Wrap that call across lines with the same, correct flag order and clause 7
  goes red (`0/0`) while behaviour is correct. So the clause also rejects a semantically identical
  file, i.e. it grades formatting. Both F1 and F2 come from the same choice: `str.count` on a
  literal that spans the argument list.
- **F3 (scope).** Clause 7's subject, `tools/round-46/gate.py`, is **not** in the round's frozen
  set (`plans/round-47-claims.md` `## Frozen paths (exact)` names only `plans/round-47-claims.md`
  and `tools/round-47/`). Last touch: `332f4884`, before `$F`, so today it is clean — but a
  post-freeze edit that keeps both counts green (F1) is caught by neither the freeze window nor
  clause 7.

Clause-7 residue to record in the landing evidence: the arm is satisfiable by a forged gate.py
(F1) and unsatisfiable by a reformatted honest one (F2). It cannot be made exact by pinning a
sha256 either — gate.py is shared frozen infrastructure from round 46 and a hash pin would break
on any later round.

## 4. The frozen window and the claims file's own freeze derivation (seat headline)

Live, `--freeze` pinned at `$F`, `--rev` at the tip, using the claims file's own counting command
(`receipts/c1-at-tip-pinned-freeze.json`, battery not run):

```
python3 -I -B tools/round-47/exact.py --root $L --freeze 5017e1f7… --rev 1e2c3102… --no-battery
exit 2   reason=frozen_path_changed
  frozen_path_changed = ["plans/round-47-claims.md", "tools/round-47/", "tools/round-47/record.py"]
  touched             = ["plans/round-47-claims.md", "tools/round-47/record.py"]
  restored            = ["tools/round-47/record.py"]
```

Same counter, freeze moved to the tip (`receipts/c1-at-tip-seriehead-freeze.json`):
`exit 0`, `failing []`, `rule_blocks 24`, `marker_occurrences 1` (battery not run). The window is
then `tip..tip` — **empty by construction**, which is C1's degenerate case measured on the real
lane. Between those two invocations nothing about the bytes changed; only the call-site pin did.
So "the frozen window is empty" is not a property of the tree, it is a property of the pair
`(--freeze, --rev)` the caller chooses, and `exact.py` accepts any pair.

`record.py` (R47-C2's counter) has **no freeze notion at all**: `grep add_argument` shows
`--root --rev --no-battery --selftest --json-out`; its receipt carries no freeze key
(`receipts/c2-at-tip.json`, exit 0, `mismatches []`, `corrections 2`, `exempted 2`, at
`1e2c3102`). The claims file's §Freeze sentence — "Nothing in this file or in `tools/round-47/`
changes after the freeze: a change makes **both** counters exit 2 `frozen_path_changed`" — is
therefore false in two ways at once: the change did happen (A1–A4, measured in §1), and one of
the two counters could never emit that verdict.

**Self-healing derivation, observed live.** The claims file re-derives its own freeze as
`git log --format=%H -1 -- plans/round-47-claims.md`. That command returns the **last commit that
touched the file**, so a commit that edits the claims file becomes the freeze. At 17:52:24Z it
returned `62e33f7d` — the tip — and the derived window `62e33f7d..62e33f7d` was 0 bytes while
`exact.py` differed from `$F`'s in nothing and `record.py` differed in everything. At 17:53:20Z it
returned `62e33f7d` with tip `1e2c3102` (54 bytes). Fixture proof of the general case
(`receipts/probe4.sh` + `receipts/clause7-and-freeze-derivation.json`): freeze `e0895467…`, one
tamper commit `84b132ff…` rewriting `tools/round-47/exact.py` **and** appending to the claims file
— derived freeze `== 84b132ff…`, derived window **0 bytes**, `gate.freeze_state(pinned)` exit 2
with `blob_changed ["plans/round-47-claims.md", "tools/round-47/"]`, `gate.freeze_state(derived)`
**exit 0**. The pinned arm sees it; the file's stated derivation cannot.

Consequence for landing: the freeze sha must be pinned as a literal in the report and in the
`--freeze` of every C1 measurement; it must never be re-derived from the claims file, and the
§Freeze sentence must stop promising immutability that four committed amendments already broke
(A1's own paragraph calls the freeze "a series of two" while §Freeze still says it does not
change). Which revision is the operative series head (`62e33f7d` per A2's "the measured revision
is taken after A2", or later) is the L1's call, not mine; what is measured is that `5017e1f7` is
no longer an admissible `--freeze` for a target-scoring run.

## 5. What I did not run

- `exact.py` with the forgery battery (`--no-battery` on both invocations): clause 9
  (`forgeries_total/v2_green/v3_green/genuine_green/crash`) is **not run** by this seat.
- `exact.py --selftest`, `record.py --selftest`: not run.
- `record.py` battery (clause 6, `correction_forgeries`): not present in the receipt I produced
  for the non-battery run — not run.
- No landing, no repair, no `SKILL.md`/`SCORECARD.md` edit, no commit.

## 6. Files and reproduction

Receipts in `receipts/`: `windows.sh`, `windows.log`, `win-c1..c4-*.out`,
`probe2.sh`, `probe3.sh`, `probe4.sh`, their `*.log`, `fx2-*.out`, `gatem.py`, `gatem2.py`,
`gate-arms.json`, `clause7-and-freeze-derivation.json`, the four forged/reformatted gate texts,
`real-lane.log`, `snapshot.log`, `snapshot-window.out`, `c1-at-tip-pinned-freeze.json`,
`c1-at-tip-seriehead-freeze.json`, `c2-at-tip.json` (+`.stdout`).

To re-measure the flag-order defect: run `receipts/probe3.sh`, then `receipts/gatem.py` and
`receipts/gatem2.py` with `HYAKU_SCRATCH` set to a non-`/tmp` root. The fixture dirs named in the
receipts lived under `/fast/scratch/hyaku/kaidoku-r47/C1FreezeWindow/merge-fx{2,3,4}` and were
removed as the contract requires; the scripts rebuild them, and the SHAs cited above are this
run's.
