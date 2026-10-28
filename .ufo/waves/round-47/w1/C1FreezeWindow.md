# C1FreezeWindow — scoped findings (round 47, wave 1)

Full detail, all receipts: `.ufo/waves/round-47/w1/C1FreezeWindow/report.md` and
`.../C1FreezeWindow/receipts/`. Read-only on the lane; no commit; no install.

## F-A (blocking for the landing citation) — the frozen window is not empty at the pinned freeze

`$F = 5017e1f7299c3a812e87e7950148f54313dd279e`, pathspec `tools/round-47 plans/round-47-claims.md`.

```sh
git -C <lane> log --name-status --format= -m --diff-merges=first-parent $F..$F    -- tools/round-47 plans/round-47-claims.md   # exit 0, 0 bytes
git -C <lane> log --name-status --format= -m --diff-merges=first-parent $F..<tip> -- tools/round-47 plans/round-47-claims.md
```

Ordering used: `-m` **before** `--diff-merges=first-parent` (matches `tools/round-46/gate.py:99`).

| tip | exit | bytes | names |
|---|---|---|---|
| `3186f69b` @17:48:33Z | 0 | 0 | — |
| `62e33f7d` @17:52:24Z | 0 | 108 | 2× `M plans/round-47-claims.md`, 2× `M tools/round-47/record.py` |
| `1e2c3102` @17:53:20Z | 0 | 162 | 2× claims, 4× `record.py` |

The commits are the disclosed amendments A1–A4 (`9018c53b`, `62e33f7d`, `2e4ae434`, `1e2c3102`).
Live consequence, the claims file's own counting command:

```
python3 -I -B tools/round-47/exact.py --root <lane> --freeze 5017e1f7… --rev 1e2c3102… --no-battery
→ exit 2, reason frozen_path_changed, restored ["tools/round-47/record.py"]
```

`--freeze <tip> --rev <tip>` → exit 0, `failing []` — but that window is `tip..tip`, i.e. empty by
construction. "Empty window" is a property of the `(--freeze, --rev)` pair the caller picks, not of
the tree. Pin `--freeze` as a literal; do not present a tip-pinned run as evidence of an unchanged
frozen set.

## F-B (blocking for a claim sentence) — `record.py` can never emit `frozen_path_changed`

`tools/round-47/record.py` has `--root --rev --no-battery --selftest --json-out` and no freeze
input; its receipt has no freeze key (`receipts/c2-at-tip.json`: exit 0, `mismatches []`,
`corrections 2`, `exempted 2`, at `1e2c3102`). The claims §Freeze sentence "a change makes **both**
counters exit 2 `frozen_path_changed`" is false for R47-C2 and, per F-A, false about the change
itself. Either the sentence is amended or the landing report must not cite it.

## F-C (blocking if the freeze is ever re-derived) — the stated freeze derivation self-heals

`git log --format=%H -1 -- plans/round-47-claims.md` returns the **last commit touching the file**,
so an edit to the claims file becomes the freeze and its own window reads empty. Observed live at
17:52:24Z (returned the tip `62e33f7d`, derived window 0 bytes). Fixture proof: `receipts/probe4.sh`
+ `receipts/clause7-and-freeze-derivation.json` — tamper `84b132ff…` rewrites `exact.py` **and**
appends to the claims file: derived window 0 bytes, `gate.freeze_state(derived)` exit 0,
`gate.freeze_state(pinned e0895467…)` exit 2 with `blob_changed` on both paths.
The pinned arm catches it; the file's own derivation cannot.

## F-D (frozen-clause falsification, R47-C1 clause 7) — bypassable and over-strict

Clause 7 is `exact.py:256-264`, `str.count` of two literals over `tools/round-46/gate.py` at
`--rev`. Counted with exact.py's own `ORDER`/`REVERSED` constants
(`receipts/gatem2.py`, `receipts/clause7-and-freeze-derivation.json`):

| gate.py text | ORDER | REVERSED | clause 7 | effective |
|---|---|---|---|---|
| frozen | 1 | 0 | green | first-parent |
| reversed | 0 | 1 | red | — |
| correct literal + trailing `"-m"` | 1 | 1 | red | separate |
| **correct literal + trailing `"--diff-merges=separate"`** | 1 | **0** | **GREEN** | **separate** |
| reformatted, correct order | 0 | 0 | **red** | first-parent |

- Bypass: `receipts/gate_forged_trailing_separate.py` (sha256 `75523f78…8e61`) keeps both counts
  green while git runs `separate`; on the merge fixture it makes `gate.freeze_state` exit 2
  `frozen_path_changed` on a tree whose frozen blob is net-identical. Clause 7 binds a source
  substring, not the effective option order.
- Over-strict: `receipts/gate_reformatted_correct_order.py` is behaviourally correct and fails.
- Scope: `tools/round-46/gate.py` is not in the round's frozen set (last touched `332f4884`,
  before the freeze), so an F1-style drift can be introduced at the landing revision with no
  freeze-window signal.

## F-E (R46-CL6 measured, fixture) — the reversed order over-reports, it does not miss

`receipts/probe2.sh`/`probe3.sh` build a two-parent merge where the merge resolves a frozen path to
the **side** bytes, so `blob@base == blob@tip` (`713f333f…`) while the second parent differs
(`998a6f80…`), and no plain commit in the window touches the path.

- `-m --diff-merges=first-parent`: 0 bytes, `gate.history_touched → []`, `freeze_state` exit 0.
- `--diff-merges=first-parent -m`: 28 bytes, `["tools/round-47/frozen.txt"]` → `blob_changed []` →
  `restored ["tools/round-47/frozen.txt"]` → `freeze_state` **exit 2**.

On the real lane this arm is inert: `git rev-list --merges $F..<tip>` = 0, so both orders agree
byte-for-byte (108/108 at `62e33f7d`). Today's empty window is no evidence about R46-CL6.

## Not run
`exact.py --no-battery` on both invocations (clause 9 battery **not run**), `--selftest` on either
counter, `record.py` clause-6 battery. No landing, no repair, no edits to `SKILL.md`,
`SCORECARD.md`, `plans/`, or `tools/`.
