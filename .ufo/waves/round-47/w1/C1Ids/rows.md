# R47-C1 clause 4 — verification and ready-to-paste block-24 rows

Seat `C1Ids`, round 47 wave 1. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Freeze `5017e1f7299c3a812e87e7950148f54313dd279e`; base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`.
The lane tree was read-only for this seat; every fixture below is a one-commit repo under
`/fast/scratch/hyaku/kaidoku-r47/C1Ids/fx/` built from the lane's bytes at
`3186f69b49798f2cc05727bbfd1604505fcee03b`, with `git -C <fx> rev-parse --show-toplevel`
asserted equal to the fixture path before the first commit.

## 1. The clause, as frozen

Claims file, `plans/round-47-claims.md:74-75`:

> 4. Every row's trigger cell names exactly one `R46-CL<n>` id, and the multiset over the four
>    rows is exactly `{R46-CL2, R46-CL3, R46-CL4, R46-CL6}` (each once).

Counter, `tools/round-47/exact.py:217-233`:

```python
    # clause 4: routed-id cardinality -------------------------------------------------
    per_row = [ID.findall(r[0]) if r else [] for r in rows]
    counts = {}
    for ids in per_row:
        for i in ids:
            counts[i] = counts.get(i, 0) + 1
    receipt["routed_counts"] = counts
    if hard:
        multi = [n for n, ids in enumerate(per_row) if len(ids) != 1]
        if multi:
            failing.append(f"rows naming != 1 routed id: {multi}")
        if sorted(counts) != sorted(ROUTED) or set(counts.values()) != {1}:
            failing.append(f"routed cardinality {counts} != each of {ROUTED} exactly once")
    else:
        missing = [i for i in ROUTED if i not in counts]
        if missing:
            failing.append(f"routed ids not named by any row: {missing}")
```

with `ROUTED = ["R46-CL2", "R46-CL3", "R46-CL4", "R46-CL6"]` and `ID = re.compile(r"R46-CL\d+")`
at `tools/round-47/exact.py:34,43`. Two implementation facts the claim text does not state:

- the id scan is over cell 0 of each row (`r[0]`) only, so an id printed in the v2-hole or
  arm cell is invisible to clause 4 by design;
- `\d+` is greedy but not prefix-free in meaning: `R46-CL20` matches as `R46-CL20` (one id,
  outside `ROUTED`), so a suffix-collision like `R46-CL6` / `R46-CL66` resolves to the
  longest digits and fails the multiset rather than being silently folded together.

## 2. Frozen-state run (before any candidate)

```sh
HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/C1Ids python3 -I -B tools/round-47/exact.py \
  --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin \
  --freeze 5017e1f7299c3a812e87e7950148f54313dd279e \
  --rev 5017e1f7299c3a812e87e7950148f54313dd279e \
  --json-out .ufo/waves/round-47/w1/C1Ids/receipts/freeze-run.json
```

exit **1**, `block_present 0`, `rule_blocks 23`, `marker_occurrences 0`, `failing` =
`["marker_occurrences 0 != 1", "marker_block_count 0 != 1"]`; stdout sha256
`88fafc603579d0e32679d6df708f92a471c2be5fbe154884937ac556054f28ba`, 2026-10-28T17:49Z.
Clause 4 is not reached: `score()` returns as soon as no marked block exists, so this two-line
`failing` list is **not** evidence that clauses 2–9 pass at the freeze — only that the
marker gate stopped first.

The committed tree has no block 24 at either the freeze or the revision I measured
(`git show 3186f69b:SKILL.md` carries 23 craft blocks and zero `exactness-table v3` markers;
the block landed later, at `e856beb5`); at measurement time it existed only in the worktree
(`git status --porcelain SKILL.md` = ` M SKILL.md`). Every clause below is therefore measured on
fixture repos, exactly as `exact.py`'s own battery does it. The tip now scores from freeze A4 —
`receipts/at-tip-a4-freeze.json`, exit 0, `routed_counts {CL2:1,CL3:1,CL4:1,CL6:1}`.

## 3. Clause 4 fires on its own defect class (and only there)

Three cardinality forgeries under `--profile v3`, all exit 1, all quoting clause 4:

| fixture | defect | clause-4 message |
|---|---|---|
| `dup-id` | row 2's trigger changed to `R46-CL2` | `routed cardinality {'R46-CL2': 2, 'R46-CL4': 1, 'R46-CL6': 1} != each of [...] exactly once` |
| `multi-id-cell` | one trigger cell names `R46-CL3` and `R46-CL2` | `rows naming != 1 routed id: [1]` + cardinality |
| `id-in-hole-cell` | row 2's id moved into its v2-hole cell | `rows naming != 1 routed id: [1]` + `{'R46-CL2': 1, 'R46-CL4': 1, 'R46-CL6': 1} != ...` |

`partial-header-digest-ref` keeps clause 4 green while breaking clauses 2, 6 and 8
(`header [...] != [...]`, `mutations_sha256 does not match`, `unresolved or unvalidated
citations: 1`). Its `failing` list contains no clause-4 message and `routed_counts` is
`{CL2:1, CL3:1, CL4:1, CL6:1}` — clause 4 is independent of the clauses that follow it.
The candidate that satisfies clause 4 in full reaches exit 0 with the battery green
(`forgeries_total 4`, `v2_green 4`, `v3_green 0`, `genuine_green 1`, `crash 0`).

## 4. Clause 4 does not close R46-CL3 (measured, three forgings)

`corpus/lessons/round-46.md:60-62` states the routed defect as: the id check requires every id
to appear in *some* row, not exactly once, "and a row may claim a group it does not really
address". Clause 4 closes the first half and leaves the second half open, because nothing
binds an id to the hole beside it. Three fixtures are **v3 exit 0, battery 4/4/0**:

| fixture | what it ships | why it is green |
|---|---|---|
| `permute-ids` | the `R46-CL2` and `R46-CL3` trigger ids swapped between rows; each row keeps the other row's hole | the multiset over trigger cells is unchanged — a permuted table is indistinguishable from the correct one |
| `copyrow` | rows 2–4 are row 1's hole and arm with ids `CL3/CL4/CL6` (arms `symbol`×4) | id membership and arm membership are both satisfiable without pairing |
| `one-hole-four-ids` | four distinct ids, four distinct arms `symbol/once/digest/order`, and **all four holes are R46-CL2's hole** | ids once each ✓, arms exact tokens ✓, pairing never read |

`one-hole-four-ids` is the decisive one: it is a table that describes one defect four times,
keeps every token the claim names, and scores `met_target: true`, exit 0. `dup-arm` (arms
`order`×4, correct ids) is also exit 0, and that is consistent with the frozen text — the
claims file requires each arm cell to be *one token of* the vocabulary, never a distinct one,
so the claims text and the code agree here; the table simply has no permutation constraint at
all. Consequence for the landing: a green block 24 is not evidence that block 24 says what it
claims, and the round's kill rule ("a block with the same routed id in two rows fails clause
4") is met literally while a strictly weaker table passes. The rows in §5 pair each id with
its own hole because that is the content the matrix is for, not because clause 4 checks it.

Not a clause-4 defect, recorded because it touches the same row: under `--profile v2` the
battery's `genuine_green` is computed with the **v3** scorer (`exact.py:346`), so a block
that is structurally legal in v2 but red in v3 exits 1 under `--profile v2` with
`battery genuine_green 0 != 1` — measured on `multi-id-cell` (receipt
`receipts/clause4-v2.json`). v2 is not a free pass.

## 5. Ready-to-paste rows

Drop-in replacement for the four body rows of block 24. Each trigger cell names exactly one
routed id; the multiset is `{CL2, CL3, CL4, CL6}` once each; each arm cell is exactly one
token; prose that used to sit in the arm cell moves into the v2-hole cell, because clause 5 is
an equality on that cell (`tools/round-47/exact.py:236-241`) and an arm cell reading
`symbol: the arm cell must equal …` fails it.

```markdown
| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` in the arm-vocabulary test | the v2 test asks whether any vocabulary token is a substring of the lowercased cell, so every superstring passes | symbol | 1 |
| R46-CL3 a row claims a routed id another row already addresses | the v2 test asks whether the id appears in some row, so one row can claim a group it does not address | once | 1 |
| R46-CL4 deleting a mutation changes the denominator the claim is judged on | the v2 counter compares `forgeries_total` with a number it computes itself and pins nothing, so a deleted mutation passes | digest | 1 |
| R46-CL6 one flag reorder prints a merge twice and blinds the history arm | the v2 profile reads no flag order, so `-m --diff-merges=first-parent` and its reverse print differently and no clause notices | order | 1 |
```

Measured in this exact form inside the full block of §6: exit **0**, `routed_counts`
`{"R46-CL2": 1, "R46-CL3": 1, "R46-CL4": 1, "R46-CL6": 1}`, `arm_tokens`
`["symbol","once","digest","order"]`, refs 6, unresolved `[]`, battery 4/4/0. The rows that
actually landed at `62e33f7d` (arm cells as single backticked tokens, prose dropped) also score
exit 0 — `receipts/at-tip-a4-freeze.json`; these four are the same tokens with the arm
explanation moved into the hole cell instead of deleted.

## 6. The whole block, measured green (appendix)

The worktree draft at `SKILL.md:632-641` is now **also** exit 0 (block sha256
`b9bb18e017f97e90474f37361799af9e7074f5b6edd496a7401a831f66c7c510`, measured
2026-10-28T17:53:13Z, receipt `receipts/clause4-v3.json` case `landed-worktree-draft`), so the
landing is not blocked on these rows. The block below is an
independent construction with the same score and with the arm explanation retained; block
sha256 `df731f78514cb5ac76557c0e349e3790359f4254c707503adf7b757e566a90e9`.

```markdown
- **24. An instrument's binding is an equality, not a containment, and its denominator is pinned.** <!-- exactness-table v3 --> Block 23 stated what makes a freeze claim checkable; this one states what makes a *check* exact — one row per defect the round-46 non-author spot-check routed (`corpus/lessons/round-46.md:57-70`), the v2 binding that let a forgery pass it, and the v3 arm that fails the forgery. Interpreter pin: `tools/round-47/exact.py` `interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`; the counter's own mutation list is pinned as `mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` over `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift`.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` in the arm-vocabulary test | the v2 test asks whether any vocabulary token is a substring of the lowercased cell, so every superstring passes | symbol | 1 |
| R46-CL3 a row claims a routed id another row already addresses | the v2 test asks whether the id appears in some row, so one row can claim a group it does not address | once | 1 |
| R46-CL4 deleting a mutation changes the denominator the claim is judged on | the v2 counter compares `forgeries_total` with a number it computes itself and pins nothing, so a deleted mutation passes | digest | 1 |
| R46-CL6 one flag reorder prints a merge twice and blinds the history arm | the v2 profile reads no flag order, so `-m --diff-merges=first-parent` and its reverse print differently and no clause notices | order | 1 |

  Refs: `corpus/lessons/round-46.md:57-70` (the four routed instrument defects this matrix closes), `corpus/lessons/round-46.md:65-70` (R46-CL6: the flag order is a convention no clause reads), `corpus/lessons/round-46.md:27-31` (S142 grounds `-m --diff-merges=first-parent`), `plans/round-47-claims.md:74-75` (the routed-id cardinality clause this table must satisfy).
```

## 7. Citation selectors actually resolved

| selector | file length at rev | resolves | content at the cited lines |
|---|---|---|---|
| `corpus/lessons/round-46.md:57-70` | 102 | yes | `R46-CL2` (57), `R46-CL3` (60), `R46-CL4` (63), `R46-CL6` (65) |
| `corpus/lessons/round-46.md:65-70` | 102 | yes | the R46-CL6 flag-order paragraph |
| `corpus/lessons/round-46.md:27-31` | 102 | yes | the S142 row (29) and the sentence that names `--diff-merges=first-parent` (31-32) |
| `plans/round-47-claims.md:74-75` | 190 | yes | clause 4, quoted in §1 |
| `tools/round-46/gate.py:99` | 247 | **no — refused** | the `-m, --diff-merges=first-parent` literal, but `ALLOW` (`exact.py:36`) is `corpus/lessons/`, `corpus/knowledge/`, `plans/`, `tools/round-47/`, so clause 8 fails with `outside the validated path set` (`cite-gate46`, exit 1, stdout sha256 `4b3764e7f7d71546ec10696348470eb9e865adb7a7db365af5930bcc4eb256ad`) |

The last row is a design consequence worth stating before landing: clause 7 *reads*
`tools/round-46/gate.py` while clause 8 refuses to let the block cite it, so the order arm's
evidence can only be pointed at by naming the literal (`-m --diff-merges=first-parent`) or by
citing `corpus/lessons/round-46.md:27-31`, which is what the block above does.

## 8. Pins and digests computed here

| value | bytes hashed | sha256 |
|---|---|---|
| `interpreter_sha256` | `tools/round-47/exact.py` at freeze/rev (identical) | `dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c` |
| `mutations_sha256` | `"\n".join` over `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift` | `19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` |
| (not a pin) `tools/round-46/gate.py` | worktree bytes at rev | `c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c` |
| (not a pin) `SKILL.md` worktree after the mid-wave edit | 303,655 bytes | `bf94d1b53a255d2e7bf50b0516ff679b3cd1e63e4e9b573d9fac5b54c3a3fae8` |

Both pins the counter compares (`mutations_sha256_expected`, `interpreter_sha256_expected`)
were read back from a receipt as equal to these values, not asserted.

## 9. Reproduction

```sh
export HYAKU_SCRATCH=/fast/scratch/hyaku/kaidoku-r47/C1Ids TMPDIR=/fast/scratch/hyaku/kaidoku-r47/C1Ids
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-47/w1/C1Ids/receipts/drive.py
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-47/w1/C1Ids/receipts/drive-v2.py
```

`drive.py` rebuilds each fixture from `git show 3186f69b:…`, inserts the case's block before
`## Config custody for live-probe rounds (SOP)`, commits once, and scores `freeze == rev` with
`--profile v3`. Receipts: `receipts/clause4-v3.json`, `receipts/clause4-v2.json`. The fixture
trees themselves were removed with the scratch root after the receipts above were copied out.
