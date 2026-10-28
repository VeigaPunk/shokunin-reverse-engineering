# RevC1Order — round 47 C1, clause 7 (`flag-order` over `tools/round-46/gate.py`)

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Base `13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5`,
freeze `5017e1f7299c3a812e87e7950148f54313dd279e` (`git log --format=%H -1 -- plans/round-47-claims.md`
re-derives it). Nothing in the lane tree was written outside this report file and
`.ufo/waves/round-47/w1/RevC1Order/`. Every verdict below is from an executed fixture; the probe
sources and every forged `gate.py` are in `receipts/` and re-run the same way.

Environment: Python 3.14.8, git 2.56.0, ruff 0.17.2 (`~/.local/bin/ruff`, already installed —
nothing was installed or upgraded for this seat).

## Verdict

Clause 7 is a **substring count over the whole file** —
`n_ok, n_bad = gtext.count(ORDER), gtext.count(REVERSED)` at `tools/round-47/exact.py:260`, with
`ORDER`/`REVERSED` as literal source text at `tools/round-47/exact.py:38-39`. It is therefore an
assertion about layout, not about the argv the arm executes.

Measured, with a genuine block-24 (the counter's own `good_block()`) in a one-commit fixture repo:

- **3 file shapes score green while the merge arm is dead or reversed** — two of them with the
  merge-resolution tamper invisible (`history_touched` returns `[]` where it must return the path).
- **4 file shapes score red while being behaviourally identical to the frozen bytes** — including a
  plain `ruff format --line-length 80`.
- The **whole frozen counter**, battery included, returns `exit 0`, `met_target true`,
  `forgeries_total 4 / v2_green 4 / v3_green 0 / genuine_green 1 / crash 0` on a `gate.py` whose
  `-m --diff-merges=first-parent` pair is present, in order, in the live call — and **inert**.

The premise the clause encodes (`plans/round-47-claims.md:59`, "the arm is order-sensitive") is not
the failure mode: reordering the pair never removed a path from `touched` in any shape measured;
what blunts the arm is the pair's **absence** or its **position after `--`** (F6).

## Findings

### F1 — HIGH — green with the literal in a comment and no flags in the live call

- Fixture `receipts/variants/forgery-A-comment-only-literal-flags-dropped.py`,
  sha256 `b8ad7ba7ce30450fcdeb3f217e30aa44710796e03e8e4df9f61e7d9d467fbc4e` (byte-identical to the
  variant scored as `comment-only-literal-flags-dropped`; the probe recreates the repo each run).
- Command `python3 -B probe_clause7_forgery.py $S` → probe exit **0**; inside the receipt the
  counter's v3 verdict is **exit 0**, `gate_order_literal 1`, `gate_order_reversed 0`, `failing []`.
  Receipt `receipts/p3-clause7-forgery.json`.
- The diff that matters: a two-line comment `# ... "-m", "--diff-merges=first-parent"; the order /
  # is load-bearing` and a live call `git(root, "log", "--name-status", "-z", ...)` that passes
  **neither** flag.
- Behaviour on the tamper repo (only the merge commit writes `f.txt`; neither parent does):
  `history_touched(base, tip, ["f.txt"]) == []`, `err None`. Ground truth in the same receipt:
  `git log --name-status -z --format= <base>..<tip>` = `M z.txt`, `M y.txt` — the merge diff is
  absent without the flags. This is precisely the R45-CL6/R46-CL6 defect restored, scored green.
- What the claim would have to say: the pair must occur **in the argv that is executed**, not
  anywhere in the file — a comment or a dead list must not satisfy it.

### F2 — HIGH — green with the pair in order in the live call, but after `--`

- Fixture `receipts/variants/forgery-B-flags-after-pathspec.py`, sha256
  `00d817655956a98be0513f1d02702bd120c53cf2d41fd34c35a74a6866078eb7`.
- End-to-end, `python3 -B probe_e2e_forgery.py $S` exit **0**; for this fixture the frozen counter
  `exact.evaluate(..., with_battery=True)` returns **exit 0**, `met_target true`,
  `failing []`, `frozen_path_changed []`, `gate_order_literal 1`, `gate_order_reversed 0`,
  battery `4/4/0/1/0` with `flag-order-drift` red as designed. Receipt
  `receipts/p6-e2e-counter-forgery.json` (`forged-flags-after-pathspec`).
- The call is `git(root, "log", "--name-status", "-z", "--format=", ..., "--", *paths,
  "-m", "--diff-merges=first-parent", binary=True)`. `--` ends option parsing, so both flags become
  pathspecs; git exits 0 and the merge diff is suppressed. `touched` on the tamper repo: `[]`
  (`receipts/p5-kwarg-equivalence.json`, `flags-after-pathspec` → `all: [y.txt, z.txt]`,
  `f.txt: []`).
- So the clause does not bind order in any meaningful sense: the literal is present once, in the
  right relative order, in the executed call, and the arm is dead.
- What the claim would have to say: the pair must appear in the call's argv **before** the `--`
  separator, i.e. in the options slice, not the pathspec slice.

### F3 — HIGH (precision) — red on behaviourally identical bytes

Four rewrites that change nothing except layout or where the flag list is assembled:

| rewrite | literal fwd/rev | v3 exit | behaviour |
|---|---|---|---|
| line break inside the call | 0/0 | 1 | identical |
| double space between the tokens | 0/0 | 1 | identical |
| single-quoted tokens | 0/0 | 1 | identical |
| helper kwarg inserting the pair after `log` (`p3` row `kwarg-helper-correct-argv`) | 0/0 | 1 | **identical, proven** |

- Receipts `receipts/p1-clause7-matrix.json` (rows `v1-wrapped-forward-same-order`,
  `v2-double-space-forward-same-order`, `v3-single-quotes-forward-same-order`: all exit 1, failing
  `gate.py flag order: 0 correct, 0 reversed`) and `receipts/p5-kwarg-equivalence.json`
  (`agree: {"kwarg-helper-correct-argv": true}` — the same `touched` sets as the frozen bytes:
  `[f.txt, y.txt, z.txt]`; the counter's verdict on that same file is exit 1,
  `receipts/p3-clause7-forgery.json`).
- Calibration note, because it changes how the row reads: `p1`'s
  `v4-helper-kwarg-order-built-at-runtime` is a **different** helper that appends the pair after
  `*args`, i.e. after `--`, so its flags are inert and it is behaviourally wrong — clause 7 rejects
  it for the right outcome but the wrong reason (the literal is absent, not the argv wrong). The
  equivalent-argv helper is the `p3`/`p5` one above, and that is the over-rejection evidence.
- A real formatter does it too: `ruff format --line-length 80 gate.py` exits 0, "1 file
  reformatted", forward literal `1 → 0`, `clause7_would_reject: true`
  (`receipts/p7-formatter-80col.json`; `gate.py:99` is 83 columns, so an 80-column formatter splits
  the call one-argument-per-line).
- Consequence for the claim: `failing == []` is unsatisfiable for any correctly-ordered `gate.py`
  that a formatter has touched, so the Target is a property of a formatting accident, not of the
  arm.
- What the claim would have to say: token equality after `ast` parsing (string-literal argv in
  order), or a behavioural check (F-recommendation below), or an explicit statement that the
  measured bytes are the frozen round-46 blob and no other gate.py satisfies the predicate.

### F4 — MEDIUM — the diagnostics cannot separate F3 from a reversal; and the byte it binds is outside the freeze

- A wrapped **correct** call and a wrapped **reversed** call produce the *same* receipt
  (`0 correct, 0 reversed`) and the *same* failing string (`p1` rows `v1` vs `v6`). Only a reversal
  written adjacently on one line is detected (`v5`: `0 correct, 1 reversed`, exit 1). That adjacent
  one-line swap is exactly what the battery builds (`exact.py:88-89` → `body.replace(ORDER,
  REVERSED, 1)`), so `battery.v3_green == 0` for `flag-order-drift` is tautological for the class it
  is meant to demonstrate.
- Post-freeze flip: freeze at F, reformat only `tools/round-46/gate.py` at R
  (`probe_postfreeze_flip.py`, receipt `receipts/p4-post-freeze-flip.json`): counter **exit 0 at F,
  exit 1 at R**, `frozen_path_changed []`, `touched 0`, `frozen_bytes_moved []`,
  `frozen_derived [tools/round-47/, plans/round-47-claims.md]`. `gate.py` is in round-46's
  *directory* freeze and its blob is identical at base, freeze and tip
  (`dac075f1e040518ed4a3d14a6b446a83feca9717`), so clause 7 is a constant over immutable bytes that a
  later commit outside round-47's freeze can still flip to red without any frozen-path alarm.
- What the claim would have to say: either add `tools/round-46/gate.py` to the round-47 frozen
  paths, or state the clause over the pinned blob (`dac075f1…`) rather than over whatever bytes sit
  at `--rev`.

### F5 — LOW — `--selftest` is unreachable from its own flag

`python3 tools/round-47/exact.py --selftest` → **exit 2**, empty stdout, argparse
`the following arguments are required: --root, --freeze, --rev` (`exact.py:429-431`). With dummies
(`--root /nonexistent --freeze x --rev y --selftest`) it runs: **exit 0**,
`EXACT_SELFTEST: cases=16 failures=0` (receipts `p0a-bare-selftest.json` (expected 2),
`p0b-selftest-with-dummy-required.json`). So the 16-case red battery — including
`red-flag-order-swapped` — is not reproducible from the documented flag surface; a reader running
the obvious command reads it as could-not-evaluate. The counter is otherwise sound against its own
cases, which is why the attacks above are not artefacts of a broken import.

### F6 — LOW (premise) — "order-sensitive" is not the arm's failure mode

`probe_order_semantics.py` (receipt `receipts/p2-flag-order-semantics.json`), three merge shapes,
`f.txt` scope: raw `git log` bytes differ between the two orders in 2 of 3 shapes
(`f_scope_raw_identical` false for `third-state` and `first-parent-version`), but the **parsed
`touched` set is identical in all three**, and also identical in the isolated shape where only the
merge writes the path (`p3` rows `original` and `comment-only-literal-reversed-across-lines` both
`[f.txt]`). `-m` (separate) is a superset of `--diff-merges=first-parent` for this parser, so a
reversal can add the second-parent diff, never remove a path. The claim's kill rule ("A fixture
whose `gate.py` carries the reversed flag pair fails clause 7") is true as a statement about the
literal and false as a statement about the arm.

Caveat: four shapes, one git version (2.56.0); octopus merges and `--first-parent` interaction were
not measured.

## The exact rewrites tried, and the exit

Every row: genuine block 24, one-commit fixture repo, `exact.score(..., profile="v3")`
(`receipts/p1-clause7-matrix.json`, `receipts/p3-clause7-forgery.json`). The `v2` profile exits 0 on
every scored variant (10/10 in `p1`, 7/7 in `p3`) — the ported round-46 semantics have no flag
clause, so all twelve differences below are v3-only.

| # | `tools/round-46/gate.py` rewrite | fwd/rev | v3 exit | arm behaviour |
|---|---|---|---|---|
| 1 | frozen bytes | 1/0 | **0** | correct |
| 2 | `git(root, "log", "-m",` / newline / `"--diff-merges=first-parent", ...)` | 0/0 | **1** | identical (correct) |
| 3 | `"-m",  "--diff-merges=first-parent"` (double space) | 0/0 | **1** | identical |
| 4 | `'-m', '--diff-merges=first-parent'` (single quotes) | 0/0 | **1** | identical |
| 5 | helper kwarg inserts the pair after `log` (`p3` `kwarg-helper-correct-argv`) | 0/0 | **1** | identical (proven, `p5`) |
| 6 | `"--diff-merges=first-parent", "-m"` on one line | 0/1 | **1** | identical |
| 7 | reversed, split across lines | 0/0 | **1** (same message as #2) | identical |
| 8 | comment carries the literal, live call reversed across lines | 1/0 | **0** | identical |
| 9 | comment carries the literal, live call passes neither flag | 1/0 | **0** | **tamper missed** |
| 10 | live pair in order, after `--` | 1/0 | **0** | **tamper missed** |
| 11 | literal in a docstring **and** in code | 2/0 | **1** | identical |
| 12 | comment + reversed adjacent on one line | 1/1 | **1** | identical |

Direct answers to the two questions posed:

- **Does the literal check survive a reformatted `gate.py` that keeps the order?** No. Line break
  inside the tuple, double space, single quotes and a kwarg-assembled argv each exit 1 (rows 2–5),
  and `ruff format --line-length 80` alone converts row 1 into row 2 (`p7`). It is equally broken by
  *documenting* the pair (row 11, exit 1).
- **Does it catch the reversed pair written across lines?** Not as a reversal detector. Row 7 and
  row 2 produce the identical receipt (`0 correct, 0 reversed`) and the identical failing string;
  the clause fires only because the forward literal disappeared, and it goes green again as soon as
  any comment restores that literal (rows 8–10).

## What clause 7 would have to say

The round wants "a flag-order clause over `tools/round-46/gate.py`". Keeping that shape, the
predicate has to be one of:

1. **Behavioural (recommended).** One-commit fixture repo whose `base..tip` contains a merge that
   writes a path neither parent writes; require
   `gate.history_touched(base, tip, [path]) == [path]` with `err is None`. Reformat-proof, position-
   sensitive, comment-proof; it fails rows 9 and 10 and passes rows 2–5 and 11. This is the property
   the round actually protects.
2. **Syntactic, done properly.** `ast.parse` `gate.py`, locate the `git(...)` call inside
   `history_touched`, take the positional string-literal prefix (stopping at `--` or the first
   non-literal), and require that slice to contain `-m` immediately followed by
   `--diff-merges=first-parent`. Rejects row 10 (position) and row 9 (absence), accepts 2–5 and 11,
   still accepts row 8's reversal only if it also checks the slice order across lines — which a token
   scan does.
3. **Byte pin.** State the clause over the round-46 frozen blob
   `dac075f1e040518ed4a3d14a6b446a83feca9717` and delete the literal count, so the verdict cannot be
   flipped by formatting or by a third-party commit (F4). Add the behavioural case from (1) if the
   clause must say something about the arm rather than about the file.

Whichever is chosen, the battery's `flag-order-drift` forgery must also include at least one of
row 9 / row 10, otherwise `battery.v3_green == 0` continues to be guaranteed by construction.

## Receipts and reproduction

All probes are in `receipts/probes/`; they take one argument, the scratch root, and import the
frozen counter read-only from the lane. Receiver-side command:

```sh
S=/fast/scratch/hyaku/kaidoku-r47/RevC1Order          # or any non-/tmp root
mkdir -p "$S"; export TMPDIR="$S" HYAKU_SCRATCH="$S"
cd .ufo/waves/round-47/w1/RevC1Order/receipts/probes
python3 -B run_receipts.py "$S" "$PWD/../rerun"
```

Receipt `receipts/receipts.jsonl` — one row per probe with the exact command, exit code, expected
exit, stdout sha256, stderr sha256 and UTC window (`2026-10-28T17:58:2xZ`):

| probe | exit (expect) | stdout sha256 | receipt |
|---|---|---|---|
| p0a-bare-selftest | 2 (2) | `e3b0c442…` (empty) | `p0a-bare-selftest.json` |
| p0b-selftest-with-dummy-required | 0 | `0249b80f5808…` | `p0b-selftest-with-dummy-required.json` |
| p1-clause7-matrix | 0 | `7e743c4353c4…` | `p1-clause7-matrix.json` |
| p2-flag-order-semantics | 0 | `622f0e5d53f0…` | `p2-flag-order-semantics.json` |
| p3-clause7-forgery | 0 | `8c3277391459…` | `p3-clause7-forgery.json` |
| p4-post-freeze-flip | 0 | `153dac3043c7…` | `p4-post-freeze-flip.json` |
| p5-kwarg-equivalence | 0 | `372c5f8d2fb6…` | `p5-kwarg-equivalence.json` |
| p6-e2e-counter-forgery | 0 | `da48261c0af9…` | `p6-e2e-counter-forgery.json` |
| p7-formatter-80col | 0 | `326a52532461…` | `p7-formatter-80col.json` |

Forged `gate.py` bytes, kept verbatim: `receipts/variants/forgery-A-comment-only-literal-flags-dropped.py`
(`b8ad7ba7…`), `receipts/variants/forgery-B-flags-after-pathspec.py` (`00d81765…`); the frozen
original for comparison is `receipts/variants/original.py`
(`c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c`).

## Residual risk and verification gaps

- **No landed block 24 exists at this revision**, so every "v3 exit" above is the counter's verdict
  on the counter's own `good_block()` in a fixture repo. Rows 1–12 are properties of clause 7, not
  of the draft the L1 lands. When the block lands, re-run row 1 and rows 9/10 against the landed
  bytes; the clause-7 verdict should be identical because clause 7 never reads `SKILL.md`.
- **Fixture commit ids differ per run** (fresh repos), so receipt JSON is not byte-reproducible: `p2`'s
  stdout sha changed between two runs at identical byte length while every verdict field was
  identical. Cite verdict fields, not hashes, for those probes.
- **Not measured**: octopus merges, `--first-parent` interaction with `-m`, git versions other than
  2.56.0; whether `-m` and `--diff-merges` order changes anything for a parser other than
  `gate.history_touched`'s.
- **Not measured / not available**: no `lsp` device exists in this seat's tool surface, so
  definition/reference checks on `exact.py` were done by import-and-execute of the frozen module
  (which is stronger for this question: every verdict is the real `score()`), not by a language
  server.
- The predicate I did not attack: clauses 1–6, 8, 9 of C1 and the whole of C2 are other seats'
  scope; where my receipts touch them (block structure, digest, refs) it is only to isolate
  clause 7.
