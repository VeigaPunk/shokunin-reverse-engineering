# R45W2ReviewC2 — adversarial falsification of `tools/round-45/c2-counter.py`

Seat `R45W2ReviewC2`, wave 2 (falsify the landing). Lane `kaidoku-shokunin`, read-only on the
lane tree; every fixture and receipt written under
`/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewC2` and copied to
`.ufo/waves/round-45/w2/R45W2ReviewC2/evidence/`.

Revisions: freeze `f762b7273e3f6ca3c710bb37d5de92a4a4417aec`, landing
`e715263cb51b713c342ab992d527fe9d61d6f8ff`, A1 (measured)
`1f4b27f82353d6544dc0c8048b3cfdadd8525d12`, lane HEAD at review time
`a63d109faa050207d4c184471889049741c9ebbf`.

**Instrument under attack is the frozen one.** `tools/round-45/c2-counter.py` working-tree
sha256 `50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025` equals
`git show f762b727…:tools/round-45/c2-counter.py` sha256, and
`git diff --stat f762b727… -- tools/round-45 plans/round-45-claims.md` is empty. Every fixture
below runs a byte-identical copy (`c2-counter-frozen.py`) of that blob; nothing in
`tools/round-45/` or `plans/round-45-claims.md` was written.

## Verdict table

| # | Attack | Verdict | Live at A1/HEAD? |
|---|---|---|---|
| A1 | duplicate rows: `by_tool.setdefault` keeps the first | **falsified** — verdict flips on row order | no (no duplicate rows) |
| A2 | row inside an HTML comment or fenced block | **falsified** — invisible rows register | no (0 fenced, 0 commented) |
| A3 | first cell with text around the backticked path | **falsified** — `search`, not path equality | no (6/6 exact) |
| A4 | exit cell is digit-presence, not a verdict map | **falsified** — prose and decimals pass | **yes** (A1 row was wrong; A3 fixed it) |
| A5 | does `frozen_path_changed` cover `SKILL.md`? | **holds** — no, by design | — |
| A5′ | does the frozen arm see a merge that plants a frozen-dir file? | **falsified** — c2 exits 0 on the violation | no (no merges in range; disclosed R45-CL6) |
| A6 | `scope_size == 6` is list length, not distinct instruments | **falsified** (latent) | no (frozen scope is distinct) |
| A7 | scope path that does not exist at `--rev` | **holds-with-disclosed-limit** (R45-CL2) | no |
| A8 | the claims file's "Before" is reproducible from the round freeze | **falsified** — reason string differs | record, not score |

Nothing in A1–A5 changes the measured value of R45-C2: at landing, A1 and HEAD the counter
exits 0 with six exactly-named, unfenced, unique rows. The findings are about what the
instrument *would* certify, plus one live case where it certified a row that was wrong.

## Method (identical for every fixture)

```sh
S=/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewC2; export TMPDIR="$S"
git -C "$LANE" show f762b7273e3f6ca3c710bb37d5de92a4a4417aec:tools/round-45/c2-counter.py > "$S/c2-counter-frozen.py"
D=$(mktemp -d -p "$S/fx"); git -C "$D" init -q            # asserted: rev-parse --show-toplevel == $D
# fixture writes SKILL.md + tools/round-45/registry-scope.json + plans/round-45-claims.md,
# plus a stub for each scope path, then: git -C "$D" add -A && git -C "$D" commit -qm freeze
python3 -I -B "$S/c2-counter-frozen.py" --root "$D" --freeze "$(git -C "$D" rev-parse HEAD)" \
        --rev <same or post-freeze HEAD>
```

Every command, exit code, stdout sha256 and UTC is in `evidence/receipts.json` (31 receipts)
and every fixture's exact `SKILL.md` input is in `evidence/fixtures/<label>.SKILL.md`.
Baseline control `F0-green` exits 0 (`41db7a8581608ec8…`), so each red result below is a
property of the mutated input, not of the harness.

---

## A1 — duplicate rows: is the thin row ignored when the good row comes second?

**No. The first row wins, in either order, and the verdict is order-dependent.**

Fixture: the six good rows, except `tools/round-45/c2-counter.py` appears twice — once thin
(`0 met; non-zero otherwise`) and once good. Only the two lines' order differs.

| run | row order | exit | `thin` |
|---|---|---|---|
| `F1a-dup-thin-first` | thin, then good | **1** | `['tools/round-45/c2-counter.py']` |
| `F1b-dup-thin-second` | good, then thin | **0** | `[]` |

`registered` lists the path in both cases; only `thin` flips. Cause:
`by_tool.setdefault(row["tool"], row)` in `evaluate()` keeps the *first* parsed row, and
`parse_rows` returns document order. The claims file says "some `SKILL.md` registry row's first
cell is exactly that path" — an existential over rows. A good second row is discarded, so the
counter reports not-met where the claim's own wording is satisfied, and swapping two registry
lines changes the score. Fix: select by predicate rather than position — `hits = [r for r in
rows if r["tool"] == path]`, register if `hits`, and mark thin only if `all()` hits are thin;
or refuse duplicates with exit 2 `duplicate_row` so the ambiguity is named, never silently
resolved by line order.

Live impact: none. Audited at landing, A1 and HEAD — six scope rows, zero duplicate tools
(`evidence/real-audit.json` → `duplicate_tools: []`). Latent.

## A2 — does a row inside an HTML comment or a fenced block count?

**Yes, when the row occupies its own line; the parser has no comment or fence state.**

| run | fixture | exit | `unregistered` |
|---|---|---|---|
| `F2a-html-comment-only` | all six rows on their own lines inside `<!-- … -->` | **0** | `[]` |
| `F2b-fenced-only` | all six rows inside a triple-backtick fence | **0** | `[]` |
| `F2c-inline-comment` | the row shares the line with `<!--` | 1 | `['tools/round-45/c2-counter.py']` |

A `SKILL.md` whose entire registry is commented out or fenced off — nothing a reader sees as a
registry — scores exit 0 `met_target: true`. The failure is position-sensitive: `parse_rows`
only requires `line.strip().startswith("|")`, so a row that begins a line inside a multi-line
comment or a fence is a row, while the same row after `<!--` on the same line is not. Fix:
track fence toggles on ` ``` ` and an `inside_comment` flag that opens on `<!--` and closes on
`-->` in the line scan, and skip rows seen while either is active.

Live impact: none. `real-audit.json` shows `n_fenced: 0` at landing, A1 and HEAD, and the
registry rows sit in the visible table under `### Round-44/45 instrument registry` — lines
1630-1635 at the landing, 1636-1641 at A1, 1652-1657 at HEAD. Latent.

## A3 — does a first cell with text around the backticked path count?

**Yes. The claim's "exactly" is not implemented.**

`ROW_TOOL.search(cells[0])` locates a backticked `tools/…py|sh` anywhere in cell 0.

| run | first cell | exit | `unregistered` |
|---|---|---|---|
| `F3a-trailing-text` | `` `tools/round-45/c2-counter.py` (alias of the gate) `` | **0** | `[]` |
| `F3b-leading-text` | `` see `tools/round-45/c2-counter.py` `` | **0** | `[]` |
| `F3c-prefixed-path` | `` `vendor/tools/round-45/c2-counter.py` `` | 1 | `[…]` (correct: the backtick must precede `tools/`) |
| `F3d-two-path-scope-second` | `` `tools/round-40/other.py`, `tools/round-44/c2-counter.py` `` | 1 | `['tools/round-44/c2-counter.py']` |

The frozen claim (§ R45-C2 clause 2) and `SKILL.md:1645-1646` (HEAD) both state the rule as
"its first cell is that **exact** backticked path". F3a/F3b violate that rule and still score met; F3d
shows the mirror defect — a cell that names two instruments registers only the first, so a row
that does name the scope path is unregistered. The predicate is being read as "cell 0 contains
a backticked path" on the happy path and as "cell 0 is the path" only by accident. Fix:
`ROW_TOOL.fullmatch(cells[0])` (the regex already anchors `tools/` and the extension), and
leave the two-path cell unregistered as F3d does.

Live impact: none. Audit: six scope-naming rows, `n_not_exactly_a_path: 0`, at landing, A1 and
HEAD — the real score does not lean on the loose match. Latent.

## A4 — is the exit cell satisfiable by `0 rows, 1 column, 2 bytes`?

**Yes. `exits_ok` asks for three digits as words anywhere in the cell, not for a verdict map.**

| run | exit cell | exit | `thin` |
|---|---|---|---|
| `F4a-prose-units` | `0 rows, 1 column, 2 bytes` | **0** | `[]` |
| `F4b-decimal-prose` | `0.5 of a row, 1.5 columns, 2.5 bytes` | **0** | `[]` |
| `F4c-control-missing-2` | `` `0` met; `1` not met `` | 1 | `[…]` |
| `F4d-control-bare-nonzero` | `` `0` met; non-zero otherwise `` | 1 | `[…]` |

Both controls are caught, so the clause does what its kill rule says. But `\b0\b`, `\b1\b`,
`\b2\b` accept any three numbers in any units, in any order, with no relation to exit codes:
the cell is scored as a digit triple. `thin` therefore certifies "the string mentions 0, 1 and
2", not "the row maps 0/1/2 to meanings".

**This one is live.** At A1 the row for `tools/round-44/c1-run.sh` read "…one REA
`extract-firmware` run per carrier **plus the independent oracle arm**" with `0` = "every
carrier produced a receipt" — no oracle arm exists in that script and the `--dry-run` path
was undeclared. `c2-counter.py` at A1: exit 0, `thin: []`, i.e. it certified that row.
Amendment A3 (`f59565b7`) rewrote exactly that row ("it does not run the oracle
(`c1-oracle.py` is the counter's)", `0` now covers `--dry-run`); c2 at HEAD: exit 0,
`thin: []` again. The counter's number did not move across a substantive correction to one of
its six rows — the receipt cannot distinguish an accurate row from an inaccurate one
(`evidence/a1-to-a3-row-diff.txt`, `real-audit.json` → `a1_a3_c1_run_sh_row_correction`).
`SKILL.md:1657` (HEAD) describes the row it wants as "a registry row with a real exit map";
the instrument checks "contains 0, 1, 2".

Fix, in increasing strength: require each code to be followed by a non-empty meaning (e.g.
`` `0`\s+\w ``, `` `1`\s+\w ``, `` `2`\s+\w ``), reject cells containing fewer than three
backticked codes, and — if the calibration axis is to be honest — treat an exit-map/gate
mismatch as out of scope in the claim text rather than implied by "real exit map".

## A5 — does `frozen_path_changed` cover an edit to `SKILL.md`?

**No, and that is correct.** `FROZEN = [CLAIMS, "tools/round-45"]`; `SKILL.md` is the graded
surface, not an instrument (claims § "Frozen paths").

| run | post-freeze commit touches | exit | `frozen_path_changed` |
|---|---|---|---|
| `F5a-skill-post-freeze` | `SKILL.md` | **0** | `[]` |
| `F5b-scope-json-post-freeze` | `tools/round-45/registry-scope.json` | 2 | `['tools/round-45/registry-scope.json']` |
| `F5c-new-file-in-frozen-dir` | new `tools/round-45/sub/new.py` | 2 | `['tools/round-45/sub/new.py']` |
| `F5e-claims-post-freeze` | `plans/round-45-claims.md` | 2 | `['plans/round-45-claims.md']` |
| `F5f-rename-out` | `tools/round-45/c2-counter.py` → `tools/moved-away.py` | 2 | `['tools/round-45/c2-counter.py']` |
| `F5d-sibling-dir` | new `tools/round-45-extra/x.py` | **0** | `[]` (no over-block) |

The arm is correct in both directions: it names the offending path, it catches additions,
rewrites and moves-out, and the `tools/round-45` pathspec does not swallow the sibling
directory `tools/round-45-extra/`. Real timeline agrees: `git log --name-only
f762b727..1f4b27f8 -- plans/round-45-claims.md tools/round-45` is empty (A1 touched only
`SKILL.md`; the landing touched `SKILL.md`, `corpus/SOURCES.md`, `corpus/lessons/round-45.md`),
so evaluation at the landing and at A1 is admissible. `F5a` also fixes the boundary the claim
needs: post-freeze `SKILL.md` edits are exactly what the graded surface is for.

### A5′ — the same arm, against a merge commit (extra probe)

Block 22 (`SKILL.md:566-567` at HEAD, amended by A3 `f59565b7`) states a blind spot for both
round-45 counters ("a plain `git log --name-only` scan misses it … HIGH, routed R45-CL6"). It does, and here is
the reproduction:

```
freeze ── feat (SKILL.md edit) ─┐
        └ main (unrelated) ────┴─ merge --no-ff --no-commit, then plant
                                    tools/round-45/sub/planted.py and commit the merge
```

| probe | output |
|---|---|
| `git log --name-only --format=%H fz..rev -- plans/round-45-claims.md tools/round-45` (what c2 reads) | `d7b909bf…` — **no file names at all** |
| `git diff --name-only fz..rev -- …` | `tools/round-45/sub/planted.py` |
| `git log -m --first-parent --name-only …` (the preflight's form) | `tools/round-45/sub/planted.py` |
| `c2-counter.py` (`F8`, exit **0**) | `met_target: true`, `frozen_path_changed: []` |

A file materialised inside the frozen directory by a merge commit scores as clean. This is the
disclosed R45-CL6 blindness, not a new hole, and it is latent for this round:
`git rev-list --merges f762b727..a63d109` and `..1f4b27f8` are both empty. It does bound the
claim: "a score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen
path" holds only for linear history; the preflight form (`-m --first-parent`) is the one that
closes it, and c2's own arm is weaker than the gate it defers to.

## A6 — `scope_size == 6` counts entries, not instruments

| run | scope | exit | `scope_size` |
|---|---|---|---|
| `F6-scope-duplicate-path` | five instruments plus a duplicate of the fifth | **0** | 6 |

Six list entries, five distinct instruments, `met_target: true`. The clause is a length check
(`len(scope) != 6`). Fix: compare `len(set(scope))` as well, or reject a scope with duplicates
as exit 2. Latent: the frozen `tools/round-45/registry-scope.json` lists six distinct paths
(verified by reading it at `f762b727`), and the scope file itself is frozen, so no post-freeze
edit can inject a duplicate without tripping `frozen_path_changed` (F5b).

## A7 — a scope path that does not exist at `--rev`

`F7-ghost-instrument`: scope names `tools/round-45/ghost.py`, which no commit contains, and a
row names it → exit 0. This is the limitation `SKILL.md:1659-1660` (HEAD) already states ("checks that
a row names the path, not that the tool exists at `--rev` (routed R45-CL2)"). Confirmed, not
new, latent for the same reason as A6 (the scope file is frozen and every path exists at
`f762b727`). Recorded because a row+vanish pair would otherwise pass silently.

## A8 — the claims file's "Before" for R45-C2 does not reproduce from the round freeze

Claims § R45-C2 "Before": *"At the base the counter exits 2 `scope file absent at rev`"*, with
receipt `controls/ctl-c2-0-base-unevaluable.json` = `{counter, reason: "scope file absent at
rev", verdict: could_not_evaluate}` — three keys, no `freeze`, no `rev`, no argv.

| run | argv | exit | `reason` |
|---|---|---|---|
| `R4-real-base-canonical-freeze` | `--freeze f762b727… --rev 149133d4…` | 2 | **`freeze is not an ancestor of rev`** |
| `R5-real-base-as-freeze` | `--freeze 149133d4… --rev 149133d4…` | 2 | `scope file absent at rev` |
| `R6-real-base-freeze-to-freeze-commit` | `--freeze 149133d4… --rev f762b727…` | 2 | `frozen_path_changed` (5 paths) |

The stored reason is producible only by passing the base as the **freeze** — the opposite
polarity from the counting command the claim template gives (`--freeze <FREEZE> --rev <REV>`).
With the round's own freeze the base yields a different reason string. The receipt cannot
arbitrate because it records neither revision. Verdict on the *record*: the "Before" sentence is
not reproducible as written; the conclusion it supports (the base is not a measurable before)
still holds, because both invocations are exit 2 and a 2 is never a claim. Fix: pass
`--freeze`/`--rev` into the receipt (they are already computed in `evaluate()` — the
`could_not_evaluate` wrapper in `main()` drops them for every code-2 path) and re-issue the
control receipt with both.

Note also from R6: `FREEZE..REV` excludes the freeze commit itself, so the commit that first
adds `tools/round-45/` does not trip its own arm. That is the intended range semantics; it
means the freeze constant is load-bearing, which is why A8 matters. The stated re-derivation
(`git log --format=%H -1 -- plans/round-45-claims.md`) does return `f762b727…`, so the freeze
constant itself is sound.

---

## What still stands

* `c2-counter.py` at landing `e715263c`, A1 `1f4b27f8` and HEAD `a63d109f`: exit **0**,
  `scope_size 6`, `registry_rows 45`, six registered, `unregistered []`, `thin []`,
  `met_target true` (`R0`, `R1`, `R2`; stdout `a292755a…`, `2b401a9a…`, `7af2ede0…`).
* No finding above is exploited by the landed `SKILL.md`: six scope-naming rows under
  `### Round-44/45 instrument registry`, all `cell0` exactly `` `path` ``, none fenced,
  none nested in a comment, no duplicate tools, at all three revisions.
* The do-nothing control reproduces exactly: `freeze..freeze` → exit 1,
  `unregistered` = the six scope paths, `registered []`, `thin []`, `scope_size 6` (`R3`),
  identical in content to `controls/ctl-c2-0-do-nothing.json`.
* `frozen_path_changed` is correct for linear history (A5 table), including the no-over-block
  case, and the real freeze..A1 and freeze..landing ranges are clean.
* The instrument's own `--selftest` is green: exit 0, `cases=7 failures=0` (`R7`).

## Residual risk and verification gaps

* **Selftest coverage is the gap that matters.** Seven green cases coexist with four
  falsified predicate clauses (A1–A4), the duplicate-scope case (A6) and the merge case (A5′).
  None of the seven fixtures exercises: a duplicated row, a row inside a comment or fence,
  a non-exact first cell, a non-verbatim exit cell, a duplicate scope entry, or a merge
  commit. A green `--selftest` here is not evidence about any of them, yet `SKILL.md:1657`
  (HEAD) records this instrument's evidence as exactly `--selftest` — 7 cases, green at the
  freeze.
* **A4 is not latent**: the counter certified a row at the measured revision that A3 had to
  correct, and no result of `c2-counter.py` changed. Any future claim that rests on
  `thin == []` inherits that blind spot; calibration scoring should cite the row text, not
  the `thin` flag.
* **Not run** (say so rather than imply coverage):
  * a merge that *reverts* a frozen path to its freeze bytes while a parent changed it — the
    path is still named by the parent commit, so I expect `frozen_path_changed` to fire; not
    executed, so not claimed;
  * a frozen-directory rename (`git mv tools/round-45 tools/round-45-new`) — only the
    single-file rename `F5f` was executed;
  * shallow clones or `--depth` fetches, where `git log` range walks can silently truncate;
    c2 has no shallow guard;
  * `parse_rows` against a registry table whose exit column is not column 3 — `cells[2]` is
    hardcoded, and the round-40 table happens to share that layout; not exercised with a
    reordered table.
* **Not attacked by this seat** (owned elsewhere): block 22's own text and the
  `frozen-path-preflight.py` arms (R45-C1), the six rows' factual accuracy beyond the A1
  `c1-run.sh` correction (A3 fixed that one; A1's other five rows were not re-read against
  source by me), and the SOURCES/LOG/SCORECARD records.

## Receipts

All in `evidence/receipts.json` (label, exact argv, exit, stdout sha256, UTC, and the parsed
JSON receipt). Fixture inputs: `evidence/fixtures/*.SKILL.md`. Real-tree audit:
`evidence/real-audit.json`. A1→A3 row correction: `evidence/a1-to-a3-row-diff.txt`.

| label | exit | stdout sha256 (16) |
|---|---|---|
| R0-real-landing | 0 | `a292755ac912dd24` |
| R1-real-A1 | 0 | `2b401a9ae5a6e562` |
| R2-real-HEAD | 0 | `7af2ede0f4dd70b9` |
| R3-real-do-nothing | 1 | `d6e202aac80ee78d` |
| R4-real-base-canonical-freeze | 2 | `c1b9db741fabb5e7` |
| R5-real-base-as-freeze | 2 | `ab4227f82c5ece64` |
| R6-real-base-freeze-to-freeze-commit | 2 | `77d1aec0760f4fd5` |
| F0-green | 0 | `41db7a8581608ec8` |
| F1a-dup-thin-first | 1 | `8f328e2ec94c8f45` |
| F1b-dup-thin-second | 0 | `64812c83ccf589c7` |
| F2a-html-comment-only | 0 | `3af36eba607a36d7` |
| F2b-fenced-only | 0 | `25a311e1ab11e2d3` |
| F2c-inline-comment | 1 | `b62e50c1f3e58fc1` |
| F3a-trailing-text | 0 | `57e9b39c7887a485` |
| F3b-leading-text | 0 | `3570e35f18516723` |
| F3c-prefixed-path | 1 | `6334954043fd1336` |
| F3d-two-path-scope-second | 1 | `d6e7219d19e0ba09` |
| F4a-prose-units | 0 | `a2f233426a6cc609` |
| F4b-decimal-prose | 0 | `ef3b167189d7deba` |
| F4c-control-missing-2 | 1 | `beedc788beef151c` |
| F4d-control-bare-nonzero | 1 | `9fcb5bb721ffbe0c` |
| F5a-skill-post-freeze | 0 | `ad592a49990cdccd` |
| F5b-scope-json-post-freeze | 2 | `0b283d791222802a` |
| F5c-new-file-in-frozen-dir | 2 | `979debe334e5e602` |
| F5d-sibling-dir | 0 | `7d3bc22e205e1f52` |
| F5e-claims-post-freeze | 2 | `b4865ea34b4af8cf` |
| F5f-rename-out | 2 | `411fcf21ab239e1b` |
| F6-scope-duplicate-path | 0 | `28749e611ee5a504` |
| F7-ghost-instrument | 0 | `91d2c210fb4592f9` |
| F8-merge-commit-plants-frozen-file | 0 | `90873ef249e9b14a` |
| R7-selftest | 0 | `aea7e363e5661efc` |

No tool installs were needed (python3 3.14, git; nothing added to `PATH`). Scratch
`/fast/scratch/hyaku/kaidoku-r45/R45W2ReviewC2` removed after the evidence copy.
