# LabOrderProbe — R47-C1 clause 7: what the flag order actually does

Seat: `LabOrderProbe` (leaf). Lane `kaidoku-shokunin`, round 47 wave 1, verification/drafting/attack
phase, **before any landing**. Everything below was measured on fixtures and on read-only git.
No file in the lane tree was written except this report and its receipt directory.
`git --version` 2.56.0, `python3` 3.14.8. No packages installed.

## Verdict

1. **The premise of clause 7 is TRUE and now measured.** On a deterministic two-parent merge the
   argument order is semantic, not cosmetic: git lets the *last* diff-merges selector win, so
   `-m --diff-merges=first-parent` shows the merge **once** (24 bytes) and
   `--diff-merges=first-parent -m` shows it **twice** (32 bytes). Different bytes, different
   touched set. Receipts in §1–§2.
2. **The clause as written is a literal test, not a semantic one.** Three one-line edits to
   `gate.py` keep `gate_order_literal 1 / gate_order_reversed 0` — i.e. clause 7 green — while the
   arm's behaviour changes. Two of them re-introduce the R46-CL6 defect class: a late `-m` makes the
   arm noisy (superset), and `--no-merges` makes it **blind** — the resolution-only path disappears
   and the output is byte-identical to the no-flag arm that R45-CL6 was about. All three variants
   exit **0** from `tools/round-47/exact.py`, including the full 4-forgery battery. §3.
3. **The frozen bytes are still correct today.** At the freeze and at HEAD, `gate.py` contains the
   forward literal exactly once, the reversed literal zero times, and no second `-m` / `--no-merges`
   (measured, §5). Nothing needs to change for R47-C1 to land.
4. **Blast radius, measured rather than assumed:** the drift cannot hide a changed frozen path,
   because `gate.freeze_state`'s `blob_changed` arm is history-independent; it can only make
   `touched` too large, which produces a **false exit 2** `frozen_path_changed` on any range that
   contains a merge. On the lane's own merge `7256d1da` the two orders differ 2 paths vs 642 paths
   (§4). So the residual hole is a false-*red* / completeness-oracle hole, not a false-green.
5. **Recommendation:** land block 24 as frozen; record §3 as the round's residual hole with these
   receipts, and make round 48's clause 7 a behavioural test (run the arm on a merge fixture and
   assert the resolution-only path is present and the second-parent-only path is absent) instead of
   a `str.count` over one spelling. §8.

---

## 1. The required probe — two-parent merge, flags run both ways

Fixture `m1` (deterministic; rebuilt fresh in `receipts.json`):

```
root:   a.txt=root, b.txt=root
side:   a.txt=one            (commit side1)
main:   b.txt=two            (commit side2)
merge:  --no-ff side         (commit merge1, parents [side2, side1])
range:  root..merge1         (3 commits: merge, side2, side1)
```

| order | argv (prefix `git -C <fx> log`) | exit | stdout bytes | stdout sha256 | status pairs |
|---|---|---|---|---|---|
| **forward** | `-m --diff-merges=first-parent --name-status -z --format= root..merge1` | 0 | **24** | `214044d1605f23b6ac5d95aff2916a07fabbb3d60ecf48ea88a1e8e61ae19fa7` | 3 |
| **swapped** | `--diff-merges=first-parent -m --name-status -z --format= root..merge1` | 0 | **32** | `1b351ed3570075e956b744f774149ae961781a25796367edf07a07270fcfdf91` | 4 |

Exact `-z` token streams (`(status, path)` pairs, newest commit first):

```
forward : (M,a.txt) (M,b.txt) (M,a.txt)            <- merge appears ONCE: only its first-parent diff
swapped : (M,a.txt) (M,b.txt) (M,b.txt) (M,a.txt)  <- merge appears TWICE: per-parent diffs
```

The merge commits itself are `972ff999..055a575c` in the recorded run; the two byte counts and both
sha256s reproduce on an independently created fixture (two separate `git init` repos, same content
hashes), so the numbers are content-determined, not run-determined. Reruns of the same command in the
same repo are byte-identical (verified twice).

**The fact clause 7 rests on:** the flag order decides whether a merge is emitted once or twice, and
the *later* selector wins. Equivalently: `--diff-merges=separate` (the long form of `-m`) placed after
`--diff-merges=first-parent` produces the swapped bytes exactly —
`-m --diff-merges=first-parent -m` and `--diff-merges=separate -m` both yield
`1b351ed3…` / 32 bytes, i.e. byte-identical to the swapped order.

Also on `m1`: `--no-merges` (with the forward pair intact) and no flags at all both give 16 bytes
(`6b916df95880825d…`) — the merge is dropped entirely. `m1` cannot show the consequence because both
side commits are in range; `m2` can.

## 2. The R45-CL6 case — a resolution-only edit

Fixture `m2`: `c.txt` conflicts and the merge resolves it to a third value **and** adds
`resolved.txt`, which exists in neither parent. Range = `first_parent..merge` (merge + one side
commit).

| order | exit | bytes | sha256 (first 16) | pairs contributed by the merge | `resolved.txt` visible? |
|---|---|---|---|---|---|
| forward (`-m` first) | 0 | **31** | `3c0a6da3cb9183a1` | 2 (`M c.txt`, `A resolved.txt`) | **yes** |
| swapped (`-m` last) | 0 | **62** | `23b4515846cdd544` | 5 (both parents: adds `A a.txt`, repeats `M c.txt`, `A resolved.txt`) | yes |
| late `-m` (pair intact, extra `-m` after `--name-status`) | 0 | **62** | `23b4515846cdd544` | identical to swapped | yes |
| `--no-merges` (pair intact) | 0 | **8** | `cc7f540c75d26f2c` | 0 | **NO** |
| no flags at all | 0 | **8** | `cc7f540c75d26f2c` | 0 | **NO** |

`gate.history_touched` on the same range, three instrument variants:

```
frozen gate.py    -> ['c.txt', 'resolved.txt']              order_literal 1 / reversed 0
late -m           -> ['a.txt', 'c.txt', 'resolved.txt']     order_literal 1 / reversed 0
--no-merges       -> ['c.txt']                              order_literal 1 / reversed 0
swapped (battery) -> ['a.txt', 'c.txt', 'resolved.txt']     order_literal 0 / reversed 1
```

`--no-merges` reproduces `plain` exactly: the resolution edit and the resolution-only file are
invisible, which is precisely the R45-CL6 defect the clause exists to forbid.

## 3. Clause 7 falsification — three literal-clean, semantically different gate.py files

Method: the frozen counter, unmodified, scored against a fixture repo holding a synthetic but
structurally green block 24 (`exact.skill_text(exact.good_block())`, the counter's own generator) and
one of five `tools/round-46/gate.py` variants. Command form (CLI receipts in `receipts2.json`):

```sh
python3 -I -B tools/round-47/exact.py --root <fx> --freeze <rev> --rev <rev> --profile v3
```

| gate.py variant | clause 7 fields | exit | stdout bytes | stdout sha256 | battery |
|---|---|---|---|---|---|
| frozen bytes | `1 / 0` | **0** | 2435 | `b24a3e394a222d5b6478132c768658d1419dea7192886fe506c78c2e5c620b9e` | 4 / 4 / 0 / 1 / 0 |
| late `-m` after `--name-status` | `1 / 0` | **0** | 2435 | `06e9d26f28c6787c0f02b63c657d8b1d85626e38c64a1a3c8b35a52747c8ee03` | 4 / 4 / 0 / 1 / 0 |
| `--no-merges` after the pair | `1 / 0` | **0** | 2435 | `7120707abc54033ec497eefa1f6a4ad916160ce918450bcfc6da2337f07b909c` | 4 / 4 / 0 / 1 / 0 |
| reversed pair (the battery's forgery) | `0 / 1` | **1** | — | `failing: gate.py flag order: 0 correct, 1 reversed` | not built |
| forward pair split across a line break | `0 / 0` | **1** | 1411 | `34d12c2fa8035501afcf15c1d3a2caef722ac5539d1100c1ad39f9a733e9290a` | skipped |

Two distinct defects, both in clause 7's instrument:

**(a) False green — the clause binds a literal, the semantics are free.** `exact.py:38-39` defines

```python
ORDER    = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'
```

and scores `gtext.count(ORDER) == 1 and gtext.count(REVERSED) == 0` over the whole file text. A second
`-m` or a `--no-merges` placed anywhere else in the same arg list keeps that count intact and is
invisible to the clause. The `--no-merges` variant is the sharp case: **clause 7 green, clause 9
battery green (4/4/0/1/0), and the arm that clause 7 supposedly pins no longer sees a merge
resolution at all** (`m2`: `['c.txt']` instead of `['c.txt','resolved.txt']`). The round's fourth
forgery, `flag-order-drift`, only ever exercises `body.replace(ORDER, REVERSED, 1)`
(`exact.py:379`), so clause 9's discrimination over the flag-order class is exactly one spelling
wide.

**(b) False red — correct code, different formatting.** Reformatting the call to
`"-m",\n "--diff-merges=first-parent"` leaves the semantics *correct* and clause 7 red with
`gate.py flag order: 0 correct, 0 reversed` (exit 1). `gate.py` is frozen and spelled one way, so this
bites only a re-land or a reformat, but it is the same containment-vs-equality class the block's own
row 1 is about, applied to the clause that is supposed to be the exact one.

The claim's kill rule — "A fixture whose `gate.py` carries the reversed flag pair fails clause 7" — is
**true as stated**, verified. It is just not a statement about the arm's behaviour.

## 4. Real repo: the same order delta, on the lane's own merge

Read-only, range `9e9d6b1e..7256d1da` (3 commits: merge `7256d1da` of `9e9d6b1e`+`a46b1e70`, merge
`a46b1e70`, linear `35573514`). Receipt `realrepo.json`.

| order | exit | stdout bytes | stdout sha256 | pairs | distinct paths |
|---|---|---|---|---|---|
| forward | 0 | **63** | `43c0983aa6b06efd7770eef9563472be6a67be643a99b99fb1ef64f1d59d0e09` | 6 | **2** (`LOG.md`, `README.md`) |
| swapped | 0 | **25523** | `60c07b83c41ca52843ea8443961bebb7af1be3a45059106b8e3233077f00459b` | 647 | **642** |
| `--no-merges` | 0 | 21 | `3c30bea402cfb1e6f0f1afb14acbabfe10a69bd7b2103d7940d88c3a9c84a428` | 2 | 2 |

Per-commit decomposition of the 647: merge vs first parent = 2 paths, merge vs second parent = **641**
paths, plus 2+2 from the two non-merge commits — so the merge contributes 2 pairs forward and 643
swapped. 640 paths appear only under the swapped order; 0 appear only under the forward order.

## 5. The frozen bytes are clean (nothing to fix for landing)

| measurement | value |
|---|---|
| `gate.py` at freeze `5017e1f` | `order 1`, `reversed 0`, `bare "-m" 1`, `--no-merges 0` |
| `gate.py` at HEAD `f7d6e58d` | `order 1`, `reversed 0`, `bare "-m" 1`, `--no-merges 0` |
| `git diff 5017e1f HEAD -- tools/round-46/gate.py` | empty (identical) |
| `git log --format=%H -1 -- plans/round-47-claims.md` | `62e33f7d` (A2) — series: `5017e1f7` → `9018c53b` (A1) → `62e33f7d` (A2), as declared |

So clause 7 is green at the freeze and at HEAD for the real instrument. The L1 must still pass
`--freeze` explicitly: the freeze the claims file declares (the A1 paragraph, and after A2 the
`record.py`-scoring commit) is *not* the commit named in the wave prompt (`5017e1f`), and
`git log -1 -- plans/round-47-claims.md` re-derives `62e33f7d`. `gate.py` is identical across all
three, so this does not move clause 7 — but the two counters' `frozen_path_changed` arms read the
claims file, so the `--freeze` argument is load-bearing for them.

## 6. Calibration of the blast radius (measured, not argued)

- `gate.freeze_state` sets `frozen_path_changed = sorted(set(blob_changed) | set(touched))`
  (`gate.py:181`). `touched` is the arm clause 7 governs; `blob_changed` is a direct blob
  comparison and history-independent. Therefore **no flag-order drift can hide a changed frozen
  path**: the blob arm catches the change regardless of which diffs `git log` emitted. The sharp §3
  case is a *completeness* failure of `touched`, and it can only reach the verdict as inflation.
- Structural argument for why the blind arm is not a free pass (an argument, not a measurement): in
  `freeze..rev` both parents of an in-range merge are themselves in range, so a path the merge's
  first-parent diff shows was touched by the second parent's commits and is reported anyway; the
  paths a merge-only view contributes that `--no-merges` drops are exactly those whose frozen bytes
  the merge left equal to the freeze (any real change is in `blob_changed`). Net effect of the blind
  arm on this verdict: it can turn an exit 2 into an exit 0 **only** for a touch that restored the
  frozen bytes, and **only** when the range starts at the merge's first parent — the corner §3's
  `m2` was built to expose (`resolved.txt` appears in the merge diff and in no in-range commit).
- Inflation is real and measurable: on the lane's own merge (still inside the lane's history) the
  swapped order reports 642 paths where the forward order reports 2. A landing range that contains
  that merge and a such-drifted `gate.py` would exit 2 `frozen_path_changed` for 640 paths nobody
  touched in range. Not a security loss, a scoring loss.
- **Separate finding, offered for the L1's reconciliation (not a clause-7 defect):** the freeze arm
  grades *touch*, not *change*. Fixture: frozen path changed in one commit and restored to its frozen
  bytes in the next → `blob_changed []`, `restored ['tools/frozen.txt']`, and still
  **exit 2 `frozen_path_changed`** (`receipts2.json` → `freeze_arm`, both gate variants). `restored`
  is computed and never used in the verdict. Consequence for this round: if any landing range touches
  a frozen path and restores it — or contains a merge that the arm reports as touching one — the
  counter exits 2 and the claim cannot be scored. Sequence the landing accordingly, or decide
  explicitly that touch-is-fail is the intent (it is at least consistent with "frozen means
  read-only").

## 7. Receipts

All receipts live next to this report in `.ufo/waves/round-47/w1/LabOrderProbe/`; each JSON entry
carries `cmd`, `cwd`, `exit`, `stdout_bytes`, `stdout_sha256`, `utc`.

| file | sha256 | contents |
|---|---|---|
| `receipts.json` | `98bf7d1bc6042b2640bfb128641269f472b3a4cedd083e732d80d5f6a3141bd1` | m1/m2 five-order runs, four instrument variants, in-process counter verdicts, freeze-restore arm |
| `receipts2.json` | `675f8741525b9e60352bc61ac4600a229eee476092036d3951c87290a0606c84` | CLI counter runs (real stdout sha256) for frozen / late-`-m` / `--no-merges`, plus the restore fixture |
| `realrepo.json` | `2d40d64f793c765f5a27c34cc3a2712b48c6a77855fa8f3ccc2d4d95eaa7fe73` | lane merge `7256d1da` under three orders, per-command receipts |
| `linebroken.json` | `e6fdba2b463c21034fbc45a76cd3420f38791ce373b3896f574c5b8c2902e9b1` | the formatting false-red (exit 1, `0 correct, 0 reversed`) |
| `probe_flagorder.out` | `59152dea996b72fcd98b37c80d98be09f3ba8f2a6d106c62b4c565b96c057d07` | first-pass 5-variant isolation run (superseded by `receipts.json`, kept for the two mispredictions) |
| `receipts.py` | `1939206ea5f246345bb88914929663bda6dc6a741672c94a928ef72e3ddd1463` | driver for `receipts.json` |
| `receipts2.py` | `f9d7d133c5e8376995464da25d4eee49eb93ca7c7f8eb2deef3104a1dc9871aa` | driver for `receipts2.json` |
| `probe_flagorder.py` | `be02fd5b9c993b0411a3ccbaa938887c49407eda1d6341c5921dcbfb1b8d0629` | first-pass driver |

Two of the first-pass predictions were wrong and are reported as measured: appending `-m` *immediately*
after the pair does **not** forge clause 7 (the resulting text contains the reversed literal, so
`reversed 1` → red), and injecting `--diff-merges=separate` *before* `-m` is semantically identical to
the frozen arm (green is correct). The surviving forgeries are the two placements in §3.

Fixture rebuild (all fixtures were deleted with the scratch root per the wave contract; the byte
counts and sha256s are content-determined and reproduce):

```sh
D=$(mktemp -d -p "$S") && git -C "$D" init -q -b main
# m1: a.txt/b.txt=root; branch side sets a.txt=one; main sets b.txt=two; merge --no-ff side
# m2: c.txt=orig; side c.txt=side; main adds a.txt; merge --no-ff side -> resolve c.txt=resolved,
#     add resolved.txt, git commit --amend --no-edit
# m3: e.g. as in receipts.py (freeze fixture for the restore arm)
```

## 8. What I recommend the L1 do

1. **Land block 24 unchanged.** Clause 7 is satisfiable and true on the frozen instrument; nothing in
   §3 blocks the landing.
2. **Record §3 as the round's residual hole**, with `receipts2.json` as the fixture receipt: the
   round-47 report should say plainly that clause 7 pins the spelling of the arm, not its behaviour,
   and that `--no-merges` (or a late `-m`) passes clauses 7 and 9 while returning the pre-round-46
   view of merges.
3. **Round 48, if this axis is claimed again:** replace the `str.count` pair with a behavioural test —
   build a two-commit merge fixture whose resolution adds a path neither parent has, call
   `gate.history_touched` at `--rev`, and require the resolution-only path present **and** a
   second-parent-only path absent. That is one fixture and three assertions, and it is satisfied only
   by the arm that actually implements first-parent semantics. Cheap version if only the clause text
   may change: require exactly one `diff-merges` selector in the arg list, resolved as "last wins",
   and forbid `--no-merges`/`-c`/`--cc` in the same call.
4. **Reconcile `--freeze`** with the amendment series before scoring (§5): the prompt's `5017e1f` is
   the first freeze, `62e33f7d` is the declared one, and the frozen-path arm reads the claims file.

## Not run / out of scope

- Clause 6 (`mutations_sha256`) and the other three block-24 rows: other seats' axes, not measured here.
- `tools/round-47/record.py` (R47-C2): not executed by this seat.
- The merge-only restore arm (§6 second bullet): argued structurally, **not measured**. The linear
  change-then-restore is measured: exit 2 `frozen_path_changed` with `blob_changed []`.
- No landing was measured; no block-24 bytes exist yet, so every counter verdict above is on the
  counter's own structurally green generator block, which is the correct pre-landing target.
