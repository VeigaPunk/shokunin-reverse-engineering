# R46W1RegH — instrument-registry rows for the round-46 C2 census (tag `reg-h`)

Seat `R46W1RegH`, leaf. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Read-only on the lane
tree; scratch `$S=/fast/scratch/hyaku/kaidoku-r46/R46W1RegH` (removed at exit). No git mutation, no
commit/push, nothing written outside
`.ufo/waves/round-46/w1/R46W1RegH/` and `$S`. No install was needed (`python3 3.14`, `git` only).

Deliverable: `.ufo/waves/round-46/w1/R46W1RegH/rows.md`, exactly three rows, sha256
`3e5ef55944333b954fddadd7a5e75777f9100516e7d3b8d73364a7957904c92c`.
Receipts: `.ufo/waves/round-46/w1/R46W1RegH/receipt.md` (argv, exit code, stdout sha256, UTC per command).

All three instruments are in the frozen census (`tools/round-46/census.json`, 38 paths) — verified by
reading the census at the freeze — so these rows are clause-3 work, not extra.

## The three rows (verbatim copy of rows.md; paste from the file, not from this block)

```
| `tools/round-41/heldout-gen-v3.py` | probe — seeded held-out SquashFS carrier generator, table-v3 classes, two replicates per class, with the label fixed by class before any REA run and an optional --run/--verify dev proof | 0=carriers written and, with --verify, every envelope reached its declared tuple (also the determinism selftest's 12 checks all pass); 1=a red outcome — a REA run error, a --verify miss, a failed selftest check, or a guard refusal (seed not at least 16 hex, missing --out, an existing manifest.json, --verify without --run); 2=argparse usage error only (missing --seed, unknown flag, a --actions-set value outside the choices) | `python3 -I -B tools/round-41/heldout-gen-v3.py --seed <freeze-hex> --selftest --scratch <scratch>` — 12 checks, green 2026-10-28 | none fixed — the caller's --seed selects the bytes, the optional --actions-file pin is checked against the class tokens, and the emitted manifest.json records the seed and every carrier sha256 | `--out` only, plus `--scratch` for trees and REA output dirs | kaidoku |
| `tools/round-42/prefile-gate.py` | gate — pre-file check that every wave is settled, the round scopes are clean, the lane root has no stray .err, and every w*/<Name>.md citation in the lesson resolves in HEAD | 0=GATE GREEN, all four conditions a to d pass; 1=GATE RED, at least one condition FAIL (a root that is not a directory or not a work tree also exits 1, via SystemExit, although nothing was evaluated); 2=argparse usage error (no --root/--round and no --selftest, unknown flag) | `python3 -I -B tools/round-42/prefile-gate.py --selftest --work <existing dir>` — 12 cases, green 2026-10-28 | none — it reads HEAD of the caller's --root and pins no file of its own | none at all, read-only; selftest fixtures go under --work or TMPDIR | kaidoku |
| `tools/round-45/frozen-path-preflight.py` | gate — freeze integrity before a commit counts as landed, with arms commit, blob, restored, dirty (--check-dirty) and pathspec (--require-pathspec) | 0=clean, no frozen path touched in FREEZE..REV, every frozen blob identical, nothing restored and the worktree clean under the pathspec; 1=violation, verdict frozen_path_changed with the offending commits and paths listed; 2=could-not-evaluate — usage, unknown or non-ancestor revision, a frozen directory left uncovered under --require-pathspec, or a failing git call | `python3 -I -B tools/round-45/frozen-path-preflight.py --selftest` — 11 cases, green 2026-10-28 | none built in — the caller supplies --freeze, --freeze-path and --pathspec; plans/round-45-claims.md names the round-45 set | `--json-out` only; selftest fixtures under $HYAKU_SCRATCH or $TMPDIR | kaidoku |
```

Grammar, checked with the frozen counter's own parser (`registry.EXITMAP`, `registry.rows_in_section`):
three lines, 7 cells each, cell 0 exactly the backticked path with nothing else, cell 3 binds `0=`,
`1=` and `2=`, no literal `|` inside a cell. Then end-to-end: a scratch fixture repo carrying these
rows inside a `<!-- instrument-registry v2 -->` … `<!-- /instrument-registry -->` section, with a
census of exactly these three paths, scored by the frozen `tools/round-46/registry.py --spec r46
--profile v2` → exit 0, `met_target true`, `registered` = 3, `unregistered []`, `thin []`,
`absent_at_rev []`, header equal to the house schema. Negative control: the same fixture with row 1's
verdict map degraded to `0 rows, 1 column, 2 bytes` → exit 1, `thin` names that path. So the rows
satisfy clauses 2–5 and the check that says so is discriminating.

Provenance is not "read once": the three files' content sha256 is identical at `31820472…`, at
`50862e4a…` and at the HEAD of the verification (`e3dfdbad…`, and unchanged at `7bf33e31…`) — the
rows cannot be stale against a later HEAD.

## Exit-code audit (requested: anything outside {0,1,2}?)

None of the three takes a code outside {0,1,2}. Two of them **overload 1 with could-not-evaluate**,
which is why the rows say so in words:

- `prefile-gate.py`: `_norm_root` raises `SystemExit("…")` for a `--root` that is not a directory or
  not a work tree → exit **1** with empty stdout (measured: `pg-nongit`). Only argparse errors are 2.
- `heldout-gen-v3.py`: every `raise SystemExit("…")` guard (bad seed, missing `--out`, an existing
  `manifest.json`, `--verify` without `--run`) → exit **1** (measured: `hg-badseed`, `hg-verify-norun`).
  Only argparse errors are 2 (measured: `hg-noseed`). `--verify` on a real set exits 1 for a miss and
  the selftest exits 1 for a failed check, so 1 is genuinely overloaded.
- `frozen-path-preflight.py`: clean 0 / violation 1 / could-not-evaluate 2 with no overload — the
  explicit `return 2` paths are usage, unknown revision, non-ancestor, `pathspec_required`, `git log
  failed`, `git status failed`, `ls-tree failed`.

One self-test command cell carries a precondition found by measurement: `prefile-gate.py --selftest
--work <dir>` calls `tempfile.mkdtemp(dir=work_root)` without creating `work_root`, so a missing
`--work` parent exits **1** with a `FileNotFoundError` traceback (measured: `pg-selftest-missing-work`),
not a selftest failure and not 2. Hence "existing dir" in the row. The preflight selftest, by
contrast, `makedirs` its scratch root.

## Findings against the frozen instruments (reported, not fixed)

These are outside my row mandate but came out of probing with the exact commands below; each is
read-only and re-runnable. They matter because they decide whether a C1/C2 score at HEAD is
admissible.

**F1 — the brief's freeze hash is stale, and so is the "authoritative" second freeze.** The lane moved
while this wave ran: `HEAD` was `50862e4a` when I started, `e3dfdbad` at 16:55Z, `7bf33e31` at
16:57:57Z. `tools/round-46/attest.py` has three different byte strings across the commits in play:
`31820472` → sha256 `dd1e7df1682c5b63ed9f5f75a3aff26c7914e6d41885e5e2da717aa91165d0fb`,
`50862e4a` → `eba599582bb32eab3c47d7c15cbd53852e257070ae756136e3cee059e37311fd`,
`65678df0`/`6e018068`/HEAD → `e6c44d2d57dbbc65ed8d14b642a6101eea264b05faf68c25606525b8fe532346`.
Measured with the frozen counter:

- `python3 -I -B tools/round-46/registry.py --root <lane> --freeze 31820472… --rev 50862e4a… --spec r46 --profile v2 --no-battery`
  → **exit 2**, `reason frozen_path_changed`, `touched` = `attest.py`, `gate.py`, `registry.py`.
- same with `--freeze 50862e4a… --rev HEAD` → **exit 2**, `touched` = `attest.py` (commit `65678df0`).
- same with `--freeze 65678df0… --rev HEAD` → no frozen-path touch (`frozen_path_changed []`); the
  score then proceeds and exits 1 on the registry predicates.

So: (a) the claims file's own definition of the freeze ("the commit that first contains this file and
`tools/round-46/`") yields `31820472`, where the interpreter is not the final bytes; (b) the
"authoritative" `50862e4a` was superseded by `65678df0`, which is where `attest.py`'s final blob
(`936910fe60b259472be2791b826ea7444b793114`) first appears; (c) any score at HEAD must cite
`65678df0` or later, or the counter exits 2. The C1 score receipted at `6e018068` is only admissible
under a freeze of `65678df0`. `65678df0..HEAD` touches no frozen path (`git diff --name-status` over
`plans/round-46-claims.md tools/round-46/` is empty), and `6e018068..HEAD` likewise.

**F2 — `restored` does not mean tamper-then-restored.** `gate.freeze_state` computes
`restored = [p for p in touched if p not in changed]`, but `changed` is computed over the *entries* in
the claims file (`tools/round-46/` as a directory + the claims file), never over individual files under
a frozen directory. Two controlled fixtures differing only in final bytes
(`$S/restored_semantics.py`, receipt `restored-semantics`) both exit 2 and both report
`restored: ["frozen/same.txt"]`; in one the final bytes are `tampered`, in the other `same`. The exit
code is right in both, but the receipt field cannot be read as evidence of restoration — which is
exactly the reading the claims file's Freeze-integrity paragraph invites. Routed as a finding only.

**F3 — `--selftest` on both counters is unreachable as the claims file spells it.** The claims
§Satisfiability preflight says "`attest.py --selftest` prints `cases=15 failures=0` … and
`registry.py --selftest` prints `cases=11 failures=0`". Measured:

- `python3 -I -B tools/round-46/registry.py --selftest` → **exit 2**, empty stdout, stderr
  `registry.py: error: the following arguments are required: --root, --freeze, --rev`.
- same plus `--root /nonexistent --freeze x --rev x` → **exit 0**, `REGISTRY_SELFTEST: cases=12 failures=0`.
  **12, not 11.**
- `python3 -I -B tools/round-46/attest.py --selftest` → **exit 2** for the same reason.

`--root/--freeze/--rev` are `required=True` in argparse, so the `--selftest` branch is never reached
without dummy values; the claims' own preflight number (11) is also one behind the instrument (12),
consistent with `65678df0` "a battery selftest case".

**F4 — `--json-out` to a non-existent parent crashes instead of exiting 2.** `registry.py … --json-out
$F/receipts/reg.json` where `$F/receipts` does not exist → `FileNotFoundError` traceback out of
`gate.emit`, **exit 1**, empty structured output. `gate.py`'s docstring promises "An unhandled exception
is a defect, never a verdict: every entry point catches it and returns 2"; `main_guard` wraps
`evaluate`, not `emit`. This is the `R45-CL13(f)` class one layer out.

## Paste notes for the L1 (things that would silently fail the C2 predicate)

0. **State measured at the end of this wave.** At `781e19ae` (2026-10-28T16:59:30Z) the section is
   landed with the house header and **38 rows**, and my three rows appear verbatim (`heldout-gen-v3.py`,
   `prefile-gate.py`, `frozen-path-preflight.py`). Scoring it with the frozen counter and
   `--no-battery` at `--freeze 65678df0 --rev 781e19ae` → **exit 0**, `scope_size 38`,
   `registered 38`, `unregistered []`, `thin []`, `absent_at_rev []`, `failing []`. The battery was
   **not run** by me (`--no-battery`), so clause 6 is untested in this receipt; and the score is
   admissible only under a freeze of `65678df0` or later (F1). Sequence: the section did not exist at
   `7bf33e31` (`grep -c 'instrument-registry v2' SKILL.md` → 0 at 16:57:57Z) and appeared by
   `781e19ae`.
1. Rows register **only** between `<!-- instrument-registry v2 -->` and `<!-- /instrument-registry -->`,
   exactly one of each, close after open. A row pasted under the existing `### Round-44/45 instrument
   registry` heading does not count. The `<!-- freeze-integrity-table v2 -->` marker for C1 is a
   different marker and does not open the registry section.
2. The header row inside the section must equal exactly
   `tool | gate or probe - purpose | verdict map (exit codes) | self-test command | pinned-value path | write scope | owner`
   (clause 2). Cell 3 style must be `0=…; 1=…; 2=…` — the round-45 rows use `` `0` met; `` which the
   v2 `EXITMAP` does **not** accept. Rows carried over verbatim from the round-44/45 section would be
   thin.
3. `registry.score` keeps the **first** row per cell-0 path (`by_path.setdefault`). `frozen-path-preflight.py`
   already has a row in the older round-44/45 section; that one is outside the markers so it cannot
   shadow, but no v2-section row may precede these three for the same paths.
4. My rows cover 3 of the 38 census paths; clause 3 fails until the other 35 have rows. Nothing in my
   rows substitutes for theirs.

## Risks / limits

- The lane moved three times during the wave (`50862e4a` → `e3dfdbad` → `7bf33e31`); every number above
  states the revision it was measured at. My three instruments are byte-identical at all of them, so the
  rows are unaffected — but a re-freeze changes which `--freeze` argument is admissible (F1).
- `heldout-gen-v3.py --selftest` requires the round-39 writer at `tools/round-39/gen-squashfs.py`; it
  resolves relative to the script, so the command in the row works from any cwd, but a lane that moves
  that writer breaks the cell's self-test.
- `prefile-gate.py` needs its `--work` parent to exist (measured); the row says "existing dir" for that
  reason.
- Scratch `$S` was removed after copying `rows.md`, `receipt.md` and the receipt files into this seat's
  directory; nothing under `/tmp` was used, and nothing outside this seat's directory was written.

## Cleanup

Removed `/fast/scratch/hyaku/kaidoku-r46/R46W1RegH` (fixture repos `fx-mine`, `fx-prose`,
`fx-tamper-kept`, `fx-tamper-restored`, `pg/`, `hg/`, `hgv/`, `notgit/`, `tmp.*`, and the runner) after
copying hashes and JSON receipts into `receipt.md`. Lane tree unchanged: only
`.ufo/waves/round-46/w1/R46W1RegH/rows.md`, `receipt.md` and this report were created.
