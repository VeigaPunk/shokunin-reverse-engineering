# CR-2 seat report — arc3-loop1-round2, chain c2, role critic

Seat CR-2 | chain c2 | critic | 2026-10-19 | repo HEAD `14b1682`
Task: attack H1 — could the absent-file guard fire on a legitimate scoped-file
rename (a future round moves a file)? Is the failure class actionable?

## 1. Work performed (evidence pointers)

- Read `claims-frozen.md` (C2 §36-50), the round-1 H1 patch text
  (`.ufo/waves/arc3-loop1-round1/claims/c3/RV-11/proposed-missing-file-guard.patch.md`),
  the census instrument, and the round-1 `CR-5` scope-diff tool.
- Built a 15-root attack matrix on scratch copies (`/var/tmp/cr2/`), run against
  **pristine v10** (`6f1d19ff…`, extracted via `git show HEAD:` — the live path
  is EX-16's write), the **H1 patch text applied verbatim**, the **landed**
  revisions, and a **CR-2 fix candidate**. All outputs:
  `claims/c2/CR-2/evidence/` (64 receipts, incl. `matrix2-summary.txt`,
  `final-capture.txt`, `df9ffdf9__*.txt`, `landed_hist_*.txt`).
- Instrument identity timeline observed (sha per revision):
  `6f1d19ff` (HEAD) → `2a89793a` → `82fb807e` → `09e270c2` → `c95a5cf3` →
  `df9ffdf9` (09:11:50, 31207 B). Every number below is bound to a sha.
- Patch text delivered: `claims/c2/CR-2/proposed-h1-critic-deltas.patch.md`.

## 2. Proposed changes (patch-text paths)

`claims/c2/CR-2/proposed-h1-critic-deltas.patch.md` — §3 (still open at
`df9ffdf9`): name the action in both UNREADABLE message constructors; state both
subclasses in the printed class label (`unreadable-or-rows-beyond-EOF`); relabel
the G2 line's per-file figures as current-ok **assertions**. Token
`UNREADABLE` unchanged in `--json`/`declared_fail_classes`. Cosmetic/operability
severity; the round's closures are unaffected by accepting or refusing it.

No change proposed for the H3 floor: its false-FAIL episode (§4, A6) was closed
by the implementers at `df9ffdf9` before this report was written.

## 3. Before→after measurement (chain c2 claim, at my own hand)

Instruments distinguished by sha; roots are one-mutation copies of the tree.

```
ROOT          INSTRUMENT                                  RESULT
full          pristine-v10 6f1d19ff                       PASS exit 0
full          H1-draft (round-1 patch verbatim)           PASS exit 0
full          landed 82fb807e / df9ffdf9                  PASS exit 0

absent SKILL  pristine-v10 6f1d19ff                       PASS exit 0   <- the debt (silent)
absent SKILL  H1-draft                                    FAIL exit 1  UNREADABLE ['SKILL.md: FileNotFoundError']
absent SKILL  landed df9ffdf9                             FAIL exit 1  same class
zero-byte SKILL  pristine-v10 / H1-draft                  PASS exit 0   <- H1-draft alone still blind
zero-byte SKILL  landed df9ffdf9                          FAIL exit 1  '0 lines < declared max 20 (rows beyond EOF)'
truncated 1-line SKILL  H1-draft                          PASS exit 0   <- still blind
truncated 1-line SKILL  landed df9ffdf9                   FAIL exit 1  '1 lines < declared max 20'
absent PROVINCE/SCORECARD  pristine-v10                   FAIL exit 1   (marker assertions already fired)
live repo root  pristine-v10 / landed df9ffdf9            PASS exit 0   0/0/0/0
```

Scope surface: round-1 `scope-diff.py` over `6f1d19ff → 82fb807e` and (CR-5 tool)
over pristine → landed: 20 rows both sides, ADDED 0 / REMOVED 0 / CHANGED 0,
`CREEP FLAGS: []` (`evidence/scopediff-landed.txt`).

Chain-claim note: the ordinary-run-at-HEAD invariant (PASS 0/0/0/0) held at
`6f1d19ff`, `82fb807e` and `df9ffdf9`, but **not** at `09e270c2`/`c95a5cf3`
(§4 A6) — the frozen claim's invariant is violated at any revision whose G2
floor counts block records instead of assertions.

## 4. Attacks/refutations attempted, with verdicts

| # | Attack | Verdict | Receipt |
|---|---|---|---|
| A1 | The seat's own question: coherent rename (file moved + SCOPE re-keyed in the same edit) | **REFUTED the false-fire hypothesis** — PASS exit 0 at `82fb807e` and `df9ffdf9` | `evidence/landedrekey__rename_rekey.txt`, `df9ffdf9__rename-rekeyed-COHERENT.txt` |
| A2 | Incoherent rename (moved, table stale) | FAIL `FileNotFoundError` — intended catch, not a false fire | `evidence/df9ffdf9__rename-norekey.txt` |
| A3 | Move kept reachable by in-place symlink | PASS (shim tolerated); broken symlink → FAIL `FileNotFoundError` | `evidence/landed__symlink_skill.txt`, `landed__brokensym_skill.txt` |
| A4 | Move of an *unscoped* file in the same root | PASS — guard reach is exactly the declared set | `evidence/landed__undeclared_move.txt` |
| A5 | One-`touch` bypass: zero-byte scoped file under the H1 patch text | **CONFIRMED** (draft alone PASSes; closed by the landed rows-beyond-EOF rule) | `evidence/draft__empty_skill.txt` |
| A6 | Per-file G2 floor (variant B) against the ordinary run | **CONFIRMED as a false FAIL** at `c95a5cf3`: FAIL exit 1 `BLIND-INSTRUMENT` (SKILL.md 0 current-ok blocks; its lone locus is inline-historical). Closed at `df9ffdf9`; CR-2's alternative (per-file *locus* floor + tree-level current-ok floor) measured and not needed | `evidence/floorfix__live_c95a5cf3_.txt`, `landed3__live-repo.txt`, `floorfix__FIX_live-repo.txt`, `df9ffdf9__skl-blank-400.txt`, `df9ffdf9__blind-all.txt` |
| A7 | Stale line anchors in the round-1 H1 patch text (`:382-390`/`:397-398` vs real `:438-445`/`:454-455` at `6f1d19ff`) | CONFIRMED (artifact defect; content-application meant no harm landed) | `evidence/v10-pristine-anchors.txt`; `final-capture.txt` |
| A8 | Historical-replication false fire (guard firing on old trees) | REFUTED — all 8 commits and all 7 round-1 tree copies carry the three scoped files, non-zero; H1 changes no historical verdict | `evidence/landed_hist_*.txt` |
| A9 | `lines=None` counts crashing the text report (`%-4d` vs `None`) | REFUTED — landed uses `%-4s`; prints `lines=None loci=None` | `evidence/landed3__live-repo.txt` |
| A10 | Label fidelity: readable file reported under `UNREADABLE` | CONFIRMED (open) | `evidence/landed_hist_hist-tree-679af5d.txt` |
| A11 | Remedy presence in the fail-class messages | CONFIRMED absent (open) — both constructors name file + cause only | `final-capture.txt:19,21` |

Answer to the seat question, plainly: **no**, the guard does not fire on a
legitimate rename — it fires on a *stale scope table*, and it stays silent for
symlink-shimmed moves and for moves of unscoped files. Its failure class is
diagnosable (names the file and the errno/EOF cause, `--json` carries the class
and the declared-fail-class list) but **not yet prescriptive**: no message tells
the operator to re-key the rows or restore the file, and its label misdescribes
the rows-beyond-EOF subclass. Both gaps have patch text in §2.

## 5. Blockers

- None for this seat. Coordination note for the integrator: the target changed
  six times inside ~11 minutes; receipts landed earlier in this wave (e.g. RV-8
  records `6f1d19ff…`, EX-16's own before/ receipts) describe superseded
  revisions, and the round's post-commit identity must be re-derived at landing
  (C1 rule #14). My §3 numbers are reproducible against `6f1d19ff` (git blob)
  and `df9ffdf9`; scratch scripts are under `/var/tmp/cr2/` (`run_matrix.sh`,
  `run2.sh`, `run3.sh`, `run4.sh`, `mk_v11.py`) and the receipts are preserved
  in `evidence/` because `/var/tmp` is not durable.
- No custody path was written (hash/stat capture only); no git mutation; `/tmp`
  untouched; this seat wrote only its seat report and `claims/c2/CR-2/`.
