# LabC1Meaning — R48-C1 meaning-classifier vs. tool code paths

Scope: the seeded hypothesis — *"the meaning classifier accepts a verdict cell whose
exit-0 segment names a success class but whose tool actually returns 2 for that
condition."* Three real registry rows read at source + driven live; whole-table
classifier sweep as background.

## Freeze identification note (for L1)

The tasking text declares freeze `dc73587a` (A1). The claims file is the rule: its own
derivation (`git log --format=%H -1 -- plans/round-48-claims.md`) and the A2 paragraph
("the declared freeze is the commit that carries this paragraph") both yield
**`ac02a79ff84133220d01ce3b59a4789b7004dbc5`** (A2). A1→A2 differs by exactly one
guard: `cls["0"] = "success" if SUCCESS.search(low["0"]) and not NOTMET.search(low["0"])`
→ `SUCCESS.search(low["0"])` (diff receipt: `tools/round-48/meanings.py` line 236,
2-line change plus the claims-file A2 paragraph). All work here pins the A2 bytes.
The declared-freeze hash in the tasking is stale by one commit; counters invoked with
`--freeze dc73587a` still score (frozen bytes are ancestors) but the A2 guard change
means the classifier under A1 and A2 disagree on any row whose exit-0 prose contains a
not-met token — e.g. `tools/round-47/exact.py` `0=met with failing empty`.

## How the classifier binds (frozen `meanings.py:214-247`)

`_segments` splits a verdict cell at `N=` marks; `meaning_classes` then assigns each
digit a class **purely by closed-token regex over the segment's own prose**:

- `cls["0"]="success"` iff `\b(met|clean|ok|green|pass|passed|verified|succeeded|wrote)\b` matches;
- `cls["1"]="not-met"` iff `(not met|violation|red|fail|failed|no verdict|refusal|refused|unresolved)` matches;
- `cls["2"]="unevaluable"` iff `(could-not-evaluate|unevaluable|could not evaluate|\busage\b|\berror\b|absent|unreadable|refus)` matches;
- plus BANANA placeholder guard and three-distinct-segment-text check.

Two structural facts, both verified by execution (receipt `CLASS`):
1. The class bound to digit N comes only from digit N's prose. **Nothing checks that
   the digit's claimed class matches the tool's code path, and nothing checks that the
   digit's real meaning is the digit's claimed class.** It is a token linter, not a
   semantic check; the residual hole is *honest* mis-binding, not `banana` forgery.
2. Class assignment is digit-positional: `refus` in segment 1 binds "not-met" via
   `refusal|refused` while `refus` in segment 2 binds "unevaluable". The same meaning
   token maps to different classes by position — so a row that truthfully says "exit 1
   is a refusal" is stamped `1=not-met`, and a row that lies the other way is stamped
   `2=unevaluable`.

## Classifier sweep over the current registry (worktree SKILL.md @ ac02a79f)

`meaning_classes()` over all 40 extracted rows: **24 pass, 16 fail**
(`classes.json`, `registry-rows.txt`). Failures are all vocabulary gaps — honest
success/refusal prose outside the token lists:

- 11 rows fail `exit 0 segment names no success meaning` for prose like
  `0=all three bindings true`, `0=the selected set was generated`, `0=every out-of-lane
  row resolved`, `0=the wrapped unblob returned 0` — no listed token.
- `tools/round-42/c1-run.sh` fails `exit 1 … no not-met meaning` (`1=no designed
  verdict, an unguarded command under set -e … may be 1` — `set -e` is `set-e`, `-\b`
  breaks the `red` token).
- `tools/round-42/heldout-gen-v4.py` fails `exit 2 … no unevaluable meaning`
  (`2=argparse rejected the argv` — no listed token).
- `tools/round-46/gate.py` fails `exit 1 … no not-met meaning` (`1=… refuses with
  "gate.py is a library"` — `refuses` matches neither `refusal|refused` nor `refus`).

Every one of these is an honest map rejected for vocabulary — the "repair" pressure is
toward token stuffing, the same degenerate class the A2 amendment was made to avoid.

## Hypothesis verdict

**Refined, not confirmed literally.** No OK row's exit-0 segment claims success while
the tool returns 2 for that condition (the 11 `0=` failures are all vocabulary, not
code-path mismatches). But the same defect class — *class label ≠ real code path* —
is confirmed live on digits 1 and 2, plus a digit outside the map entirely:

### Mismatch 1 — `tools/round-42/unblob-logtee.sh` (digit 2 mis-bound + unmapped code)

Registry cell: `2=refusal before any run, C1_REAL_UNBLOB is not an absolute path` →
classifier binds digit 2 to "unevaluable" (row currently fails on digit-0 vocabulary,
but the digit-2 binding itself is what the claim asserts).

Source (freeze bytes, copied to `unblob-logtee.sh` fixture): pre-run refusal exits 2,
then `"$real" "$@"; rc=$?; …; exit "$rc"` — **any** non-zero code the wrapped unblob
returns propagates unchanged.

| probe | command | rc | claimed meaning | actual meaning |
|---|---|---|---|---|
| A1 | `C1_REAL_UNBLOB=fake-unblob-2 unblob-logtee.sh --log /nonexistent/x.log input.sqfs` | **2** | "refusal before any run" | a run happened; the wrapped extractor failed with 2 |
| A2 | `C1_REAL_UNBLOB=fake-unblob-7 unblob-logtee.sh input.sqfs` | **7** | — | exit code entirely outside the 0/1/2 map |
| A3 | `C1_REAL_UNBLOB=relative/path unblob-logtee.sh input.sqfs` | 2 | "refusal before any run" | genuine refusal (the only case the cell describes) |

A1 and A3 are indistinguishable by exit code yet carry opposite meanings under the
bound map. The class the digit claims is true of the tool — for one of its two
producers. Receipts `A1|A2|A3` in `rcpt-index.txt`; fixture `fake-unblob-*`.

### Mismatch 2 — `tools/round-45/c2-counter.py` (digit 1 mis-bound)

Registry cell: `1=not met (…), and also the exit of an uncaught OSError when
--json-out points into a missing directory, so an IO failure is not distinguishable
from a scored not-met` → classifier binds "not-met"; the row *discloses* the
mis-binding and the classifier stamps it anyway.

Source (`c2-counter-r45.py`, main() lines 260-262): `code, receipt = evaluate(...)`;
`open(args.json_out,"w")` is unguarded. Probe B:
`python3 c2-counter-r45.py --root <lane> --freeze ac02a79f --rev ac02a79f --json-out $SK/no-such-dir/out.json`
→ `FileNotFoundError` traceback, **rc=1**. Exit 1 = "not met" per the bound class;
this exit-1 evaluated nothing wrong — it crashed writing the receipt after a clean
evaluation. Receipt `B`.

### Mismatch 3 — `tools/round-42/prefile-gate.py` (digit 1 mis-bound, disclosed)

Registry cell: `1=GATE RED, at least one condition FAIL (a root that is not a
directory or not a work tree also exits 1, via SystemExit, although nothing was
evaluated)` → classifier binds "not-met"; row discloses the mis-binding.

Source lines 69-77: `not isdir(root)` / `rev-parse --show-toplevel` failure →
`raise SystemExit("…")` → rc 1 before any of conditions a–d ran. Probes D
(`--root <missing dir>` → rc=1), D2 (`--root` a non-repo → rc=1). Receipts `D`, `D2`.

### Mismatch 4 — `tools/round-46/gate.py` (digit 1 is pure refusal; repaired row will lie)

Registry cell: `1=not a verdict, running gate.py as a program refuses … and no library
entry point returns 1` → classifier currently *rejects* the row (`refuses` matches no
vocab). Source tail: `sys.exit("gate.py is a library; use attest.py or registry.py")`
→ Probe C rc=**1**. Any repair that passes the classifier must either write the not-met
vocabulary over an unevaluable refusal (dishonest, and the positional-token ambiguity
would then stamp it "not-met"), or move the text into the `2=` segment where it
doesn't occur. Receipt `C`.

### Mismatch 5 — `tools/round-42/c2-controls.py` (digit-1 carries SystemExit diagnostics)

Registry cell: `1=a control reaches full score so the kill rule fires, and by defect
the same status also carries its own unevaluable SystemExit diagnostics (no DEV
envelopes, failed feature extraction, failed evaluator)` → currently fails on digit-0
vocabulary; digit 1 contains "failed" so it would bind "not-met" — over disclosed
unevaluable SystemExits.

## Draft landing guidance (L1)

- The 16 failing rows need honest vocabulary repairs, not token stuffing. The four
  "by defect"/"not distinguishable"/"not a verdict" disclosures above are the rows
  where a passing repair **cannot** be honest under the current class grammar: the
  grammar assumes each digit carries exactly one class, and these tools genuinely
  overload a digit. Recommend the registry cell state the overload explicitly and
  L1 decide whether the claim wants a "mixed" meaning class or the cells keep the
  dominant class with the disclosure preserved.
- `unblob-logtee.sh` exit-7 (and any other wrapped code ≥3) is entirely unmapped by
  the `0=…;1=…;2=` grammar — a digit the claim's shape cannot name.
- Skill/registry landing must add rows for `tools/round-48/meanings.py` and
  `tools/round-48/record2.py` (census has 42 paths, worktree registry has 40 →
  `registry_missing` until landing; expected pre-landing).
- `gold-meaning`/`duplicate-meaning`/`swapped-meaning` forgeries are still caught by
  construction (BANANA tokens, distinct-segments, per-digit token presence). The
  residual unfalsified surface is *plausible* mis-binding: any prose that keeps a
  success token in seg 0, a not-met token in seg 1, an unevaluable token in seg 2,
  and three distinct segment texts passes — regardless of the tool's real exits.
  A stronger v3 would compile each tool's `sys.exit`/`return` paths or run the
  refusal probes above; that is a contract question for the round, not a repair.

## Not run

- `meanings.py --selftest`, `--profile v2`, and the live forgery battery on the real
  lane (sibling seats own the battery arms; not run here).
- `record2.py` and R48-C2 (other seats).
- No installs; python3 + git + bash only. No pacman transactions attempted.

## Files

`LabC1Meaning/` holds: `rcpt-index.txt` (probe receipts: name|rc|utc|sha256s),
`classes.json` (classifier verdict per row + segment excerpts), `registry-rows.txt`
(40 extracted rows), `classify.py` (frozen classifier driver), `unblob-logtee.sh`
(freeze bytes), `fake-unblob-{2,7}` (fixtures), `rcpt-*.err` (probe stderr).
Scratch `/fast/scratch/hyaku/kaidoku-r48/LabC1Meaning` removed after this copy.
