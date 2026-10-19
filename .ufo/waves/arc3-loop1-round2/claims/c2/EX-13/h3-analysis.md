# EX-13 (executor, chain c2) — H3 patch text vs current census: line-by-line analysis

Seat EX-13, arc3-loop1-round2, 2026-10-19. Chain c2 (claim: census fail-closures —
H1 absent-file guard + H3 blind-instrument floor). This seat wrote **no** target file;
all instrument variants and fixtures live under `/var/tmp` and are reproduced
here under `tools/` and `receipts/`.

> **Revision flux notice.** The target moved four times while this seat ran
> (R0 `6f1d19ff` pre-landing → R2 `59975ae0` 09:06:36 → R3 `82fb807e` 09:06:50 →
> R4 `df9ffdf9` 09:11:50 → R5 `a4c16763` 09:16, docstring/usage hygiene only,
> floor semantics unchanged — F4 re-confirmed PASS on R5's bytes at 09:16:38).
> §1–§6 below analyse the **patch texts vs R0/R3**.
> **R4 replaced the floor with EX-14's per-readable-file floor, which changes the
> verdict on this seat's fixtures** — see the companion file
> [`r4-recheck.md`](r4-recheck.md) for the re-measurement, the surviving residual
> (F4), and the measured variant-C prototype.

## 0. Pinned revisions (all hashed during this seat's run)

| id | sha256 | lines | mtime | what it is |
|---|---|---|---|---|
| R1 | `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48` | 456 | 07:06 | H3's declared before-state = `arc3-loop1-round1/claims/c3/CR-5/tools/census-before.py` (pre-EX-28) |
| R0 | `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b` | 490 | (git `14b1682`) | pre-landing HEAD; == committed blob; == `CR-5/tools/census-after.py` |
| R2 | `59975ae0f427e0e2a087aef3c622e7995a30fa3ca2e6c8cf2477957ba6401476` | 557 | 09:06:36 | EX-16's landing, revision 1 (observed, superseded 14 s later) |
| R3 | `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa` | 560 | 09:06:50 | EX-16's landing as analysed here; matches `claims/c2/EX-16/receipts/after/after-sha256.txt`; uncommitted (`git status` = ` M`) |

R1 → R0 delta (verified by `diff` and by an AST comparison with docstrings stripped):
docstring header + G18 docstring lines + the `("PROVINCE.md", 45, 62, …)` marker re-key
40→45 + the `assert_markers` G18 check. **`main()` is byte-identical**; the only
difference at the H3 anchors is a uniform **+57-line offset** (R1 `:396/:397/:424` →
R0 `:453/:454/:481`).

## 1. H3 patch text, element by element

Source: `.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/proposed-g2-positive-floor.patch.md`.

| # | element in the patch text | verdict at R0 (pre-landing HEAD) | at R3 (landed) |
|---|---|---|---|
| 1 | `before-state sha256 36e96cd5…` | **stale**: that is R1, not HEAD. HEAD is R0. Two revisions of drift | n/a — EX-16's own receipt (`claims/c2/EX-16/receipts/before/before-sha256.txt`) records the landing base R0 correctly |
| 2 | cause quote `g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)` | **byte-exact** at R0:453 (`unatt` is bound at R0:449 to `out["AMBIGUOUS"]` — quote is faithful) | replaced at R3:513 |
| 3 | hunk 1 (`-`/`+` on `g2_ok`) | content-applies; **conflicts in hunk context with H1's hunk 2** — see §3 | implemented as `g2_ok = n_current_ok > 0` |
| 4 | hunk 2 (G2 print line) | **byte-exact** at R0:481 | R3:548-549: `G2 positive-assertion guard: %s (current-ok loci=%d, total loci=%d, floor=1)` |
| 5 | "optional stronger form … redundant with the above" | **correct**: `current-ok > 0` ⇒ `total loci > 0`, so the optional conjunct adds nothing | the unconditional form was landed |
| 6 | evidence "current-ok dets: 29@b21c0da, 31@679af5d, 35@e87e507/6bc4c29; 10 loci at HEAD e845c2b" | **not reproducible.** CR-5's own receipt
(`.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/receipts/census-at-HEAD-cr5.out`) prints `-- CURRENT-OK (5) --`, and my runs give 3/5/5/5 blocks at those four revs (class split in §2). No artifact in the tree shows 29/31/35/10 | — (does not affect the fix: measured supply at HEAD is 5 blocks, still ≥ 1) |
| 7 | claim wording "zero loci in a non-empty scope" | the minimal form does **not** implement a non-emptiness condition | R3:513 is unconditional: at an empty root R3 declares `['UNREADABLE', 'BLIND-INSTRUMENT']` (receipt `landed-empty.out`) |
| 8 | "audit … with `scope-diff.py`" | the tool exists; I re-ran it independently on R0→R3 with **two** implementations (CR-5's round-1 tool and EX-16's copy): both print `rows before=20 after=20`, 0 added/removed/changed, `CREEP FLAGS: []`, exit 0 | same |

Discharge of the pre-landing "declared class" concern: at R3 a blind run's FAIL is now
*named* — `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` in text and
`declared_fail_classes` in `--json` (R3:517, 526). Good.

## 2. How the G2 positive floor interacts with CURRENT-only vs DATED row classes

**The mechanism.** `current-ok` is not a class-restricted disposition. Three channels
feed it (R3 line refs): (i) a client-named assertion whose value equals the live anchor
(R3:441); (ii) **G16's relabel** — any `historical` assert whose value is in
`live.values()` becomes `current-ok` (R3:449), which fires *inside DATED rows*; (iii)
G17 version-intrinsic cache matches (R3:432). EX-28's own docstring relies on (ii) as a
feature: "G16 keeps a live value inside them current-ok" for the capability rows
:619/:620. The floor (`len(current-ok blocks) > 0`) is therefore a **tree-level liveness
test whose supply is partly DATED-fed by design**.

**Measured supply at HEAD (R3, live root — `landed-live.out`):**
`current-ok` = 5 blocks / 11 asserts — **1 CURRENT-class block (PROVINCE.md 44-44) and
4 DATED-class blocks (SCORECARD.md 619, 687-702, 732-738, 748-767)**; assert split
**CURRENT 3 / DATED 8**. So 4 of the 5 blocks that satisfy the floor are DATED.

**Two consequences, each measured on a fixture (`tools/gen-fixtures.py`):**

- **F1 `root-current-silenced`** — every line of all six declared CURRENT rows
  (PROVINCE 8-13, 15-26, 44, 64-71; SKILL 10-16, 18-20; SCORECARD 56-60) replaced by
  filler, line counts preserved; DATED rows and markers byte-intact.
  Result at R3: `VERDICT: PASS` exit 0, `G2 … ok (current-ok loci=4, total loci=10,
  floor=1)`, `DECLARED FAIL CLASSES: []`, and the surviving 8 current-ok asserts are
  **all DATED**. → A wholly silent CURRENT surface is not a declared failure: the floor
  is satisfied by DATED content that has nothing to do with CURRENT reconciliation.
  (Same result pre-landing at R0 and with H1+H3 hand-merged: `receipts/h0-silenced.out`,
  `receipts/h3-silenced.out`, `receipts/h1h3-silenced.out`.)
- **F2 `root-all-silent2`** — *every* line inside *every* declared range replaced by
  filler, except the DATED marker lines. Result at R3: `VERDICT: PASS` exit 0,
  `current-ok loci=1, total loci=3`, `DECLARED FAIL CLASSES: []`, the one current-ok
  locus being `SCORECARD.md:619 [bare] None=6.5.0 -> current-ok (value equals a live
  anchor)`. → Even a fully silenced declared scope reads PASS because a preserved
  DATED marker line's own text supplies the floor.

**What the floor does close (measured, both directions):**
- R0 with all three needles neutered: `loci=0/0/0`, `G2 … ok`, `VERDICT: PASS` exit 0
  (`h0b-live.out`) — the H3 defect reproduces at HEAD, not only at R1.
- R3 with the same needles neutered: `VERDICT: FAIL` exit 1,
  `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` (`landedb-live.out`).
- R3 with `PIN` alone neutered: PASS (`landedpin-live.out`) — the per-needle residual
  EX-16 already names in its docstring.
- R3 with SKILL.md absent: FAIL exit 1, `UNREADABLE` declared, `SKILL.md lines=None`
  (`landed-skillGone.out`); R0 on the same root: PASS exit 0. H1 and H3 are
  **non-redundant**: H3 alone still PASSes the absent-CURRENT-file root.

**Block-granularity caveat (part of the same interaction).** The floor counts *block*
dispositions, and a block that mixes `current-ok` with `historical` is rolled up to
`info` — which is neither a failure class nor present in `--json`. So a CURRENT-ok
assert that shares a block with any historical assert is invisible to the floor *and*
to JSON-only auditors. A class-restricted subfloor therefore cannot be computed from
`--json` as it stands (recommendation O1).

## 3. Conflicts: this patch text vs the H1 patch text, and vs the landed revision

Loci in `main()` at R0: H3 touches `:453` and `:481`; H1 touches `:438-445`, `:454-455`
and inserts before `:480`. H3's hunk-1 context reaches `:454-456`; H1's hunk-2 changes
`:455`; H3's hunk-2 sits at `:481` while H1's hunk-3 inserts at `:480`.

Measured with real `diff -u` patches on scratch copies (`tools/patch-h3.diff`,
`tools/patch-h1.diff`, log in `receipts/patch-order.txt`):

| order | `patch -F0` (strict) | `patch` default fuzz |
|---|---|---|
| H3 then H1 | **rc=1**: H1 hunks #2 (at 453) and #3 (at 478) FAILED | rc=0, fuzz 2, result == hand-merge |
| H1 then H3 | **rc=1**: H3 hunks #1 (at 450) and #2 (at 478) FAILED | rc=0, fuzz 2, result == hand-merge |

Both fuzz-applied orders converge byte-identically to this seat's hand-merged
combination, sha256 `e07673ca939cf233…` (`tools/census-h1h3-combined.py`, 494 lines).
**Required adjustment:** the two patch texts must never be applied as independent
strict unified diffs; treat them as one hand-merged edit and verify the merged result
(the landed R3 is exactly that, plus the additions listed below).

R3 vs the hand-merge (diff): R3 = hand-merge **+** (a) G19 docstring **+** the
`max_end` truncation guard (`len(lines) < max_end` → UNREADABLE), (b) the `declared`
class list + `DECLARED FAIL CLASSES` print + `--json` keys `unreadable`,
`declared_fail_classes`, `g2_floor`, (c) the print-order swap (UNREADABLE moved after
SCOPE-ERRORS), (d) `lines=%-4s` formatting. No scope-table change — corroborated by the
two independent creep audits (§1 row 8).

## 4. Required adjustments (M) and optional hardening (O)

- **M1 (records wording).** The floor landed unconditionally, but the code comment
  (R3:512) and the frozen claim both say "in a non-empty scope". Measured: R3 declares
  `BLIND-INSTRUMENT` even when every scoped file is absent (`landed-empty.out`, where
  `declared == ['UNREADABLE', 'BLIND-INSTRUMENT']`). Either implement the qualifier or
  (cheaper) record the implemented semantics — an unconditional tree-level floor — in
  the SCORECARD/claim text.
- **M2 (name the residual).** EX-16's docstring names per-needle partial blindness as
  the remaining H4 residual. The sharper residual measured here is **class-conditioned
  silence**: CURRENT-only silence leaves `current-ok ≥ 1` (DATED-fed) and reads PASS
  with no declared class. The external certificate for any instrument touch should
  therefore include the **current-ok class split**, not only the locus-count +
  scope-diff audit (locus count alone cannot see F1: 17 → 10 loci, still PASS).
- **M3 (declared-class precision).** `declared` should not emit `BLIND-INSTRUMENT` when
  `unreadable` is non-empty — a could-not-evaluate root is not an instrument blindness
  (measured double-class on `landed-empty`). One-line guard in the `declared` expression.
- **M4 (replay note).** The H1 truncation guard makes the landed instrument refuse to
  grade any root whose files predate the current scope table: replaying the round-1
  roots gives `SCORECARD.md: 701 lines < declared max 855 (rows beyond EOF)` (b21c0da)
  and 766 < 855 (679af5d) → UNREADABLE → FAIL (`landed-b21c0da.out`, `landed-679af5d.out`),
  where R0 graded them (PASS/FAIL per their content). Historical replays must use the
  pinned pre-landing copy (`tools/census-before.py`, R0) or a scope table matching that
  revision; this should be said in the records so a future reader does not read the
  UNREADABLE as a regression.
- **O1 (optional, measured to hold at HEAD).** Class-restricted subfloor
  `#(current-ok asserts with scope == "CURRENT") ≥ 1`: 3 at HEAD, so it breaks no
  ordinary run, and it fails F1 (0). To be auditable it needs `info` blocks emitted in
  `--json` (today they are text-only) — a reporting change with no scope-creep signature.

## 5. Attacks / refutations attempted

| # | attack | expected if H3 were sufficient | measured | verdict |
|---|---|---|---|---|
| A1 | neuter all needles (round-1 CR-5 injection) on R3 | FAIL + declared class | FAIL exit 1, `BLIND-INSTRUMENT` | **H3 holds** at R0/R3 |
| A2 | same on R0 (baseline / defect reproduction at HEAD) | PASS (defect) | PASS exit 0, `loci=0` | defect reproduces at R0 |
| A3 | `PIN` only | (named residual) | PASS | EX-16's residual reproduced |
| A4 | SKILL.md absent (round-1 RV-11 A5) on R3 | H3 alone insufficient; H1 needed | H3-only: PASS; R3: FAIL + `UNREADABLE` | H1+H3 non-redundant |
| A5 | **F1 CURRENT rows silenced, DATED intact** | FAIL if the floor were a CURRENT-liveness test | **PASS exit 0, current-ok 4 all-DATED, no declared class** | **floor is DATED-satisfiable — residual (M2)** |
| A6 | **F2 all declared rows silenced, markers preserved** | FAIL (silent clean) | **PASS exit 0, current-ok=1 from SCORECARD:619 marker text** | residual sharper than named |
| A7 | strict patch-text application, both orders | — | rc=1 both ways; fuzz-2 converges to `e07673ca…` | patch texts not independently applicable (M-§3) |
| A8 | empty root | declared class on a non-empty scope only | FAIL, `['UNREADABLE','BLIND-INSTRUMENT']` | M1/M3 |
| A9 | scope creep (R0→R3) | 0 flags | 0 flags, 2 independent tools | no widening |

## 6. Residual named

The floor is a tree-level current-ok-existence test. It cannot distinguish a
reconciled CURRENT surface from a silent one, because DATED rows and DATED marker
lines supply `current-ok` by design (G16). The certificate for an instrument touch is
therefore the external triple — scope-diff (creep), locus-count invariance, **and the
current-ok class split**. This residual is not closed by H3 and is not claimed to be;
it is named here so the round's records do not over-read the floor.

## 7. Reproduction

`tools/` holds the pinned instruments (`census-landed.py` = R3, `census-h1h3-combined.py`
= the hand-merge, the H3-only and H1-only variants, landed+blinded, landed+PIN-blinded),
the two patch diffs, and the fixture/instrument generators. `receipts/` holds every
run output quoted above. Rebuild under `/var/tmp` (never `/tmp`):

```
python3 tools/gen-fixtures.py       # builds root-current-silenced, root-all-silent2, root-skill-absent, root-empty
python3 tools/run-matrix.py         # re-runs the full variant × root matrix into receipts/
```
