# R46W1RegC — instrument-registry rows (round-46 C2 census, tag `reg-c`)

Seat: leaf executor, lane `kaidoku`, wave 1. Read-only on the lane tree; the only writes are
`.ufo/waves/round-46/w1/R46W1RegC/{rows.md,receipt.md,fixtures/*}` and this report. No tool
was installed (none was needed).

Freeze used for every source read: `31820472784284727546808acc31b3ea1e73919b`. Each
instrument was opened as a blob at that commit (`git show <freeze>:<path>`), its CLI surface
and every exit path read, and at least one claim per row exercised by a command actually run.
The complete command ledger — exact argv, exit code, stdout sha256, UTC — is
`w1/R46W1RegC/receipt.md`.

## The three rows (ready to paste, one line each)

```
| `tools/round-41/c1-run.sh` | probe — the round-41 C1 data procedure: arm after runs REA extract-firmware for one carrier into OUTDIR/after.json plus run.json, arm oracle builds the AVM-layout independent reader tables plus a sasquatch-v4be cross-check into oracle.tsv, nonregular.tsv and oracle-check.tsv; it scores nothing | 0=ok, the requested arm wrote its receipts; 1=no designed verdict, an unguarded command failure surfaces its own status under set -e; 2=usage or environment refusal (bad mode or arity, unreadable carrier, missing python3 or jq, a scratch without the /kaidoku-r41/ segment) | none — no --selftest in the script; the bad-argument probe exits 2 | none — the carrier sha256 and the tool versions are written into OUTDIR/run.json at run time | OUTDIR (after.json, run.json, oracle.tsv, nonregular.tsv, oracle-check.tsv, oracle-run.json) plus one scratch tree under HYAKU_SCRATCH, removed on exit | kaidoku |
| `tools/round-42/c2-controls.py` | probe — builds the round-42 C2 control documents plus the reference table from the lane SKILL.md and DEV envelopes, scores each with the draft-v4 interpreter against the precedence evaluator, and fires the C2 kill rule when any control reaches full score | 0=no control reaches full score, the kill rule stays silent; 1=a control reaches full score so the kill rule fires, and by defect the same status also carries its own unevaluable SystemExit diagnostics (no DEV envelopes, failed feature extraction, failed evaluator); 2=argparse usage error or an unhandled IO failure | none — no --selftest in the script; the bad-argument probe exits 2 | none — the DEV replicas are caller-supplied, the default interp and eval paths are absent at the freeze | --out document directory and --json-out only | kaidoku |
| `tools/round-44/c1-counter.py` | gate — R44-C1 coverage: re-derives the four frozen SquashFS v1 and v2 carriers (layout, carve, oracle census, gap rule), re-runs REA extract-firmware to compare the plus-extractor projection, and re-checks a receipt identity under --verify-receipt | 0=target met, every carrier clause and binding true; 1=not met, a named false clause or binding or a red selftest case; 2=could-not-evaluate, including frozen_path_changed, bad args, node or REA failure and rerun_disabled | python3 -I -B tools/round-44/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root> — 47 cases, green | tools/round-44/carriers.json, tools/round-42/fixtures.json and tools/round-42/prior-pins.json | --json-out plus a private --work scratch tree | kaidoku |
```

The same three lines are the whole of `w1/R46W1RegC/rows.md`. They are inside no fence
here for legibility only; `rows.md` holds them as plain lines.

## Where each exit meaning comes from (not guessed)

- `tools/round-41/c1-run.sh` — header line 69 `Exit: 0 ok, 2 usage/environment error, 3 tool
  failure`; `usage()` at 89–90 and `err()` at 93 both `exit 2`; `fail()` at 94 `exit 3`;
  `exit 0` at 434 (oracle arm) and 606 (after arm). Measured: a1/a2 exit 2.
- `tools/round-42/c2-controls.py` — docstring 35, `return 1 if full else 0` at 601,
  `SystemExit` string raises at 406 (feature extraction), 457 (no envelopes), 614
  (evaluator). Measured: a3 exit 2 (argparse), a4 and a5 exit 1 on unevaluable paths.
- `tools/round-44/c1-counter.py` — docstring 213 `Exit: 0 target met, 1 target not met, 2
  unevaluable (bad args, git/node failure, frozen path changed, rerun environment error,
  --no-rerun)`; `res['exit_code'] = 0 if res['met_target'] else 1` at 2390. Measured: a6
  selftest exit 0, `cases 47 failures []`, stdout sha `fbe23fef…` — byte-identical to the
  round-45 registry receipt, so the command in cell 4 is reproducible across rounds.

## Findings the L1 must rule on

**F1 (P0, blocks every score): the seat's freeze is stale, and the frozen directory changed
after it.** Two commits after `3182047` touch `tools/round-46/`: `50862e4a` ("complete the
freeze … declared as the authoritative freeze because the first freeze commit did not carry
the final bytes" — `attest.py`, `gate.py`, `registry.py`) and `65678df0` (F3 — `attest.py`).
`plans/round-46-claims.md` is byte-identical at HEAD (`a09564e0…`), so no supersession is
recorded there. Running the counter from its own frozen bytes:

```
registry.py --root <lane> --freeze 3182047… --rev 6e018068… --no-battery
→ exit 2, reason frozen_path_changed,
  frozen_path_changed ["tools/round-46/", "tools/round-46/attest.py",
  "tools/round-46/gate.py", "tools/round-46/registry.py"], restored = the three files
```

That is clause 8 doing exactly what it was built to do, against this round's own history.
Consequence: with the claims file's definition of the freeze ("the commit that first contains
this file and `tools/round-46/`"), **no revision at or after `50862e4a` can be scored**, and
the last commit, `e3dfdbad` ("C1 met at 6e018068"), rests on a `FREEZE` value the claims file
does not authorise. Either the claims file must carry a declared freeze supersession (itself
an edit to a frozen path, needing the same disclosure machinery), or the wave's scores are
inadmissible. I did not choose between those; the differing value is reported as measured.

**F2 (P0 for landing C2): a copied legacy row and a placeholder row are both thin, and the
section is first-wins per path.** Reproduced over `SKILL.md` at the freeze with the v2 rule
(`EXITMAP = \b([012])\s*[=:]`): of the 38 census paths, 6 have a legacy row whose cell 0 is
exactly the backticked path, and **all 6 are thin** —
`tools/round-44/c1-counter.py`, `tools/round-44/c1-run.sh`, `tools/round-44/c2-counter.py`,
`tools/round-45/c1-counter.py`, `tools/round-45/c2-counter.py`,
`tools/round-45/frozen-path-preflight.py` — because they write `` `0` met `` and only a
digit followed by `=` or `:` binds. The legacy rows sit *outside* the markers, so they are
out of scope as long as they stay outside: the hazard is copying one into the new section,
which is the "reuse the six rows" shortcut. `registry.py` keeps the **first** row per path
(`by_path.setdefault`), so the measured outcomes are:

| section content | exit | `thin` |
|---|---|---|
| my three rows only | 0 | `[]` |
| the round-45 `tools/round-44/c1-counter.py` row only | 1 | `[tools/round-44/c1-counter.py]` |
| **old row first, mine appended** | **1** | `[tools/round-44/c1-counter.py]` |
| mine first, old row after | 0 | `[]` |

So if the section is built by copying a legacy row in and appending my row after it, the
section stays red — precisely the battery's `first-wins-shadow` forgery class. My
`tools/round-44/c1-counter.py` row is the replacement, not an addition. The same first-wins
rule governs `.ufo/waves/round-46/assemble-registry.py`: it builds `seen` in sorted seat order
and emits `seen.get(path)`, so the alphabetically-first seat wins a contested path and a
lower-quality duplicate silently shadows a better one. 32 of the 38 census paths had no row
of any kind at the freeze; the section needs all 38.

*Live check of the assembler's current draft* (read-only, 2026-10-28T16:57Z,
`.ufo/waves/round-46/l1/registry-section.md`): 38 rows, all 7 cells, **3 thin** — the
`UNREGISTERED | 0=` placeholders for `tools/round-41/sqfs-list.py`,
`tools/round-43/c1-counter.py` and `tools/round-46/registry.py`. A placeholder binds `0=`
only, so it counts as registered and still fails clause 4; at that moment the section scores
`thin 3`, not `unregistered`. Those three need real rows before the section can be green.

**F3 (P1): the claims' satisfiability preflight does not run as written.** The claims say
"`registry.py --selftest` prints `cases=11 failures=0`" and "`attest.py --selftest` prints
`cases=15 failures=0`". Both literal commands exit **2**: `--root`, `--freeze` and `--rev`
are `required=True` in both parsers and `--selftest` is just another flag, so the selftest
branch is unreachable without dummy required arguments. Supplying them, from the freeze
blobs: registry **cases=12 failures=0** (not 11), attest **cases=15 failures=0** (count
right). From the F3 blob: attest **cases=16 failures=0**, registry **cases=12**. So the
preflight sentence is wrong in its command form and in the registry case count. The
instruments themselves are green; the *record* of them is not accurate — the calibration
axis is exactly that mismatch.

**F4 (P1, C2 instrument): `c2-controls.py` conflates a violation with could-not-evaluate.**
Its designed triple is 0 = no control at full score, 1 = kill rule fires, 2 = usage/IO.
Measured, exit 1 also carries `no envelopes under […]` (a4) and `evaluator failed … (exit 2)`
(a5), both of which are unevaluable. A red result of this tool cannot be told apart from a
broken setup. My row states this defect rather than hiding it; the L1 may prefer the row to
carry only the designed meaning, in which case F4 stays a separate routed finding.

**F5 (P2): `c1-run.sh` exits 3, outside the 0/1/2 verdict map.** Tool failure is exit 3
(`fail()`, line 94; line 604), and there is no designed exit 1. The row binds 1 to "no
designed verdict" and keeps 3 out of the row, per the seat rule; the row's cell 6 also names
the six files it writes.

**F6 (P2): the claim's "Before" describes the round-45 counter, not this predicate.** The
claims' R46-C2 Before says "the round-45 counter reports `scope_size 6`". The round-46
predicate's own before-state, measured with the frozen `registry.py` at the freeze
(`--freeze = --rev = 3182047`), is exit **1** with
`failing ["markers: 0 open, 0 close", "header != house schema (7 cells)",
"unregistered: 38 of 38"]` and `scope_size 38`. The census existed at the freeze (38 paths,
`named_but_absent []`), so "the census does not exist yet" is stale too. This is a stronger
before than the claim states, not a weaker one.

**F7 (method note): the lane is live and a working-tree run is not a revision result.** HEAD
advanced under this seat (`c0ca539` → … → `6e018068` → `e3dfdbad`) and the worktree was dirty
at 16:54:2x. One run of the lane's `attest.py` at that moment returned
`cases=16 failures=1` (`green-with-battery: battery v1_green 5 != 9`); the identical bytes
(sha `e6c44d2d…`, the F3 blob) run five times afterwards returned `failures=0`
byte-identically. The red is recorded as a dirty-tree artifact, attributable to no commit.
Every number in this report comes from a blob or from a copy of one.

## Coverage and what is not claimed

- Verified by command: the row format against the frozen parser (7 cells, exact backticked
  cell 0, `{0,1,2}` bound via the frozen regex, no stray backticks), and all three rows
  registering green in a fixture lane scored by the frozen `registry.py` itself.
- Read from source, **not exercised**: exit 0 of `c1-run.sh` (needs REA, unblob, a carrier)
  and exit 0 of `c2-controls.py` (needs DEV envelopes and replicas that do not exist at the
  freeze). Both are marked as source-derived, not passed.
- Not run: any score of the real `SKILL.md` (no registry section is landed — 0 markers at
  HEAD — so the only meaningful real-tree measurement at this moment is F6's exit 1).
- Three rows are three of 38 census paths; I make no claim about the other 35 beyond F2's
  count.

## Suggested next commands for the L1 (not run here)

1. Decide F1 before anything else; if a freeze supersession is declared, record it in the
   claims file and cite the new commit everywhere.
2. Land the registry section with my `tools/round-44/c1-counter.py` row **replacing** the
   round-45 one, and rewrite the other five verdict cells into the `0=…; 1=…; 2=…` form.
3. `python3 -I -B tools/round-46/registry.py --root <lane> --freeze <FREEZE> --rev <REV>
   --json-out <OUT inside the lane>` and expect `unregistered []`, `thin []`,
   `absent_at_rev []` only when all 38 rows are present.
