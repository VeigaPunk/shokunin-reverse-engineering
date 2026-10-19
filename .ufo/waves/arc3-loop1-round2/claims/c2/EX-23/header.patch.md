# v11 header/records PATCH TEXT — census fail-closures (H1+H3 closed), declared classes, H4 residual named

Seat **EX-23** · chain **c2** · role **executor** · 2026-10-19 · wave arc3-loop1-round2.
**Patch text only.** EX-23 does not write `.ufo/gates/c1-census-v10.py` (frozen rule:
C2's real-path write belongs to EX-16). No git mutation; scratch under `/var/tmp/ex23`.

Target: `.ufo/gates/c1-census-v10.py`.
- BEFORE bytes measured by this seat: **sha256 `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`, 490 lines**
  (byte copy kept: `receipts/before/c1-census-v10-6f1d19ff.py`).
- EX-16 landed its r9 revision **while this seat was measuring**; the landed bytes are now
  authoritative and already carry an H1/H3 stanza. Digest history + mid-write defect:
  `receipts/digests.txt`, `receipts/landed/X-midwrite-9373964c-typeerror.txt`.
  Landed/stable at **sha256 `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa`**.
- Consequence: my pre-landing draft implementation (`2ee0a1c9…`, `v11-draft.diff`) is
  **superseded** — EX-16's landed form is stronger (it also closes the rows-beyond-EOF /
  zero-byte / directory / EACCES legs). What survives as this seat's deliverable is the
  **header/records layer**: §1 hunks below are the remaining header deltas, anchored on the
  landed bytes; §2-§4 are the declared-class contract, the H4 residual record, and the
  before→after measurement.

---

## 1. Patch text (anchored on landed `82fb807e`; header/records layer only)

### Hunk A — revision identity in the landed stanza (landed `:47-48`)

```diff
 ARC3-LOOP1-ROUND2 r9 — H1+H3 FAIL-CLOSURES (2026-10-19, EX-16, C2's real-path
 write; instrument sha256 before this edit 6f1d19ff…). Two round-1 latent holes
+Revision under the frozen claim is v11; r9 is this landing's tag; the file path
+.ufo/gates/c1-census-v10.py stays frozen for arc3-loop1-round2 (v11 is a
+revision id, not a new file). Bound-invariance certificate: scope-diff.py on
+the v10 -> v11/r9 diff, rows before=20 after=20, 0 added / 0 removed / 0
+changed, CREEP FLAGS [] (EX-23 receipt
+claims/c2/EX-23/receipts/landed/scope-diff.txt).
```

### Hunk B — second-docstring identity line (landed `:84`)

```diff
-"""C1 stale-statement census instrument v9 (E22, arc2-loop1-round2) — FINAL.
+"""C1 stale-statement census instrument v11 (arc3-loop1-round2; r9 landing) —
+v10 + H1/H3 fail-closures (G19/G20; declared classes UNREADABLE,
+BLIND-INSTRUMENT); residual ledger H2/H4/H5/H6 named in the stanza above.
```

Rationale (measured, not stylistic): the landed file self-identifies as **v9** at `:84` and
its usage line names **`c1-census-v9.py`** — two revisions stale — while the frozen claim
calls the round's revision **v11** and the landed stanza calls it **r9**. Three names for
one revision is the identity-drift class rule #14 exists for; one line fixes it.

### Hunk C — usage line (landed `:174`)

```diff
-Usage: python3 c1-census-v9.py [--root DIR] [--json] [--quiet]
+Usage: python3 .ufo/gates/c1-census-v10.py [--root DIR] [--json] [--quiet]
+       (path frozen for arc3-loop1-round2; revision v11 / r9 landing)
```

### Hunk D — residual ledger completeness (landed `:74-76`)

```diff
-   - Still named, NOT closed here (no silent widening): H2 same-line inline-
-     marker excusal; t5 DATED-shelter for historical-looking non-live values;
-     H4 self-certification (covered externally, see above).
+   - Still named, NOT closed here (no silent widening): H2 same-line inline-
+     marker excusal; t5 DATED-shelter for historical-looking non-live values;
+     H4 self-certification (covered externally, see above); H5 unit boundary
+     (a version statement with no rea/kimi/devin/omp token is not a locus in
+     this unit -- stated boundary, v10 and v11 alike); H6 fixed-bound rationale
+     comment at the SCOPE rows remains unlanded (optional mechanical guard).
+   - H7 (EX-23 pre-landing finding: a zero-byte scoped file still read silent
+     PASS) is CLOSED BY THIS LANDING's rows-beyond-EOF leg
+     (`len(lines) < declared max end`), measured: SKILL.md 0 lines ->
+     UNREADABLE ['SKILL.md: 0 lines < declared max 20 (rows beyond EOF)'],
+     FAIL exit 1 (EX-23 receipt claims/c2/EX-23/receipts/landed/C-zerobyte.txt).
+     Recorded as closed; it must not be carried forward as open debt.
```

Nothing else in the header needs changing. Full drafted stanza (my pre-landing form,
superseded) is in `header-only.diff` / `v11-draft.diff` for reference only.

---

## 2. Declared classes (binding on the landed revision; tokens as landed)

| Class token (as landed) | Trigger | Verdict | Text report | `--json` |
|---|---|---|---|---|
| `UNREADABLE` (could-not-evaluate) | scoped file raises `OSError` (absent, zero-byte, truncated, directory, EACCES) **or** holds fewer lines than its declared max end | FAIL, whatever the row classes | `UNREADABLE (could-not-evaluate): [...]`; counts read `lines=None loci=None` | `unreadable`, `declared_fail_classes` |
| `BLIND-INSTRUMENT` | G2 positive floor: `current-ok` loci `< 1` (tree level) | FAIL | `G2 positive-assertion guard: SUSPECT (current-ok loci=N, total loci=M, floor=1)` + `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` | `g2_ok`, `g2_floor`, `declared_fail_classes` |
| unchanged | `STALE`, `AMBIGUOUS`, `UNDECLARED`, `UNRESOLVED`, `SCOPE-ERRORS`, `G11`, `G7` (warn) | FAIL / warn as before | as before | as before |

Class-name reconciliation: my pre-landing draft used the token `BLIND` and a separate
`total_loci == 0` conjunct; the landed form uses **`BLIND-INSTRUMENT`** with the floor on
`current-ok >= 1`. The landed token is the binding one — the neutered-needles injection
drives `current-ok` to 0, so the literal claim ("zero loci in a non-empty scope") is
covered. The already-landed verdict line (`and g2_ok and (not unreadable)`) has no
`blind` variable; the class is carried by `declared` (text) and `declared_fail_classes`
(JSON), which is what an auditor reads.

---

## 3. H4 self-certification residual — staying named, and certified externally

Named in the landed stanza (landed `:71-73`: "that residual is H4/self-certification: only
the external locus-count + scope-diff audit sees it, and that audit remains the certificate
for any instrument touch"). Measured by this seat on the landed bytes:

- **Injection (own widening):** `SCORECARD.md 769-855 DATED` → `769-1200 DATED` (swallows
  345 lines of record tail). The instrument's verdict on its own widening:
  `VERDICT: PASS (stale=0 …)`, **exit 0** — self-certification cannot see it
  (`receipts/landed/K-widen-census.txt`).
- **Certificate (external):** `scope-diff.py landed vs widened` → `ADDED 1 / REMOVED 1`,
  `CREEP FLAGS: ['CREEP wide added DATED row: SCORECARD.md 769-1200 (432 lines)',
  'CREEP widen-by-add/remove: … replaced 769-855 DATED']`, **exit 1**
  (`receipts/landed/scope-diff.txt`).
- **Certificate on the actual v11/r9 diff:** `scope-diff.py v10(6f1d19ff) vs landed(82fb807e)`
  → rows `before=20 after=20`, 0 added / 0 removed / 0 changed, `CREEP FLAGS: []`, exit 0 —
  the chain's certificate that the round's fail-closures moved no scope bound.
- **Locus-count invariance** (second half of the certificate): PROVINCE 6 / SCORECARD 9 /
  SKILL 2 blocks; current-ok 5 blocks, total loci 17 — identical before and after.

---

## 4. Before → after measurement (chain C2 claim, commands + outputs)

Scratch copies only; the real target was read/copied, never written by this seat.

| # | Injection / run | BEFORE v10 `6f1d19ff` | AFTER landed `82fb807e` |
|---|---|---|---|
| A | ordinary run at repo root | PASS `stale=0 ambiguous=0 undeclared=0 unresolved=0`, exit 0; counts 6/9/2 | PASS same 0/0/0/0, exit 0; counts 6/9/2; `UNREADABLE []`, `BLIND…` absent, `DECLARED FAIL CLASSES: []` |
| B | H1 — `SKILL.md` absent | **PASS exit 0**, `lines=0 loci=0`, `G2 … ok` | **FAIL exit 1**, `UNREADABLE ['SKILL.md: FileNotFoundError']`, `DECLARED FAIL CLASSES: ['UNREADABLE']` |
| C | H1b — `SKILL.md` zero-byte (EX-23 finding) | **PASS exit 0** | **FAIL exit 1**, `['SKILL.md: 0 lines < declared max 20 (rows beyond EOF)']` |
| D | H1c — `SCORECARD.md` truncated to 500 lines | PASS would be silent (rows 636-855 beyond EOF) | **FAIL exit 1**, UNREADABLE + 10 SCOPE-ERRORs |
| E | B via `--json` | PASS, no such field | FAIL; `unreadable`, `declared_fail_classes: ['UNREADABLE']`; process exit 1 |
| F | H3 — `PIN`+`VER`+`PTR` neutered (blind) | **PASS exit 0**, `loci=0`, `G2 … ok` | **FAIL exit 1**, `G2 … SUSPECT (current-ok loci=0, total loci=0, floor=1)`, `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` |
| G | `SKILL.md` is-a-directory | silent PASS class (counts 0) | **FAIL exit 1**, `['SKILL.md: IsADirectoryError']` |
| H | `SKILL.md` chmod 000 (EACCES) | silent PASS class | **FAIL exit 1**, `['SKILL.md: PermissionError']` |
| I | scope bounds (creep audit) | 20 rows | 20 rows; 0 added/removed/changed; `CREEP FLAGS: []` |

Every command and verbatim output cited above is stored under
`receipts/before/` (BEFORE) and `receipts/landed/` (AFTER); the pre-landing draft runs
(same injections against `2ee0a1c9`) are under `receipts/draft/`.

**Mid-write defect caught (evidence, not blame):** revision `9373964c` (09:06:16) set
`counts[f] = {"lines": None, "loci": None}` for unreadable files but kept
`print("%-14s lines=%-4d loci=%s")` — the H1 injection died with
`TypeError: %d format: a real number is required, not NoneType` before printing any declared
class (`receipts/landed/X-midwrite-9373964c-typeerror.txt`). Fixed in `82fb807e`. Any receipt
against this target must name the digest it measured: the target moved five times in ~2
minutes (`receipts/digests.txt`).

---

## 5. Attacks attempted (with verdicts)

1. **Silent-PASS replay of round-1 holes** (H1 absent, H3 blind): both reproduce on v10 and
   both read declared FAIL on landed bytes → closure confirmed (B, F).
2. **Adjacent unreadable shapes** (zero-byte, truncated, directory, EACCES): v10 silent-PASS
   class → all declared FAIL on landed (C, D, G, H). No counterexample found.
3. **Partial blindness** — `VER` needle alone neutered: loci 17→8, current-ok 5→4, and the
   run reads **FAIL stale=1** (caught by an incidental stale, not by the floor);
   `PIN` alone neutered: loci/verdict unchanged (VER covers the same text at this tree).
   Verdict: per-needle narrowing is **not** generally self-detected — it remains the named
   H4 residual; a narrowing that happens to keep the verdict is invisible except by the
   day-over-day locus-count audit (J, `receipts/landed/J-verneuter.txt`).
4. **Self-certification attack** (widen own SCOPE bound): instrument still PASS exit 0 →
   residual confirmed real; external differ catches it (K, §3). No refutation.
5. **Format-consumer attack**: does any script parse the census stdout lines?
   `grep -rn "positive-assertion guard\|SCOPE-ERRORS"` over `*.py/*.sh/*.md` finds only the
   instrument itself and prose — the added report lines and `lines=None` counts break no
   machine consumer in-repo. Exit-code contract kept: 0 PASS / 1 FAIL / 2 ANCHOR-FAIL
   (anchor-fail re-measured: `HOME=/nonexistent` → `ANCHOR-FAIL`, exit 2).
6. **Claim about my own patch**: the header hunks are inert — applying the full header
   stanza alone to v10 produced **byte-identical** census output to v10 on the ordinary run
   (`receipts/draft/after-ordinary.txt` vs `receipts/before/ordinary-pass.txt`; diff empty),
   so the closure lives in the implementation hunks, not in the prose. The patch text
   cannot make a claim true by itself.

---

## 6. Parent application notes

1. Apply hunks A-D to the landed bytes at the records commit (or land one revision id and
   record the reconciliation). A-D touch only the two docstrings; the shebang stays where
   the landed file puts it.
2. If EX-16 lands a further revision, re-derive its digest first (rule #14) and re-run
   scope-diff before sealing; my receipts name `82fb807e` and are void for other digests.
3. H7 is closed by the landed rows-beyond-EOF leg — record it as closed, do not carry it.
4. The H4 residual is deliberately *not* closed by any header text; the certificate is the
   external differ, and this seat's run of it on the landed diff is the chain's evidence.

---

## 7. ADDENDUM — the target moved twice after §3-§5; final measured digest `df9ffdf9`

Timeline (`receipts/digests.txt`): `6f1d19ff` (v10, 490 L) → `82fb807e` (r9, tree-level
floor, HEAD PASS) → `076bd621` → `c95a5cf3` (per-file **block**-level floor, **HEAD FAIL**)
→ **`df9ffdf9`** (601 L; per-file **det**-level floor, HEAD PASS; frozen for this addendum,
byte copy `receipts/landed/final-df9ffdf9.py`).

**Regression found, evidenced, and fixed within the wave.** `076bd621`/`c95a5cf3` replaced
the tree floor with `floor[rec["file"]] += 1` over `out["current-ok"]` **blocks**. At HEAD,
SKILL.md has **0** current-ok *blocks* — its 3 live-matching dets sit inside an
`info`-aggregate block (`SKILL.md:18-20`) — so `h3_ok=False` and the ordinary HEAD run read
`VERDICT: FAIL`, `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']`
(`receipts/landed/L2-newest-ordinary-FAIL.txt`), contradicting the frozen claim's "ordinary
runs at HEAD stay PASS 0/0/0/0".

EX-23's measured fix — count per-file current-ok **dets** across all blocks — restores the
claim and keeps EX-14's per-file-collapse detection:

| run | block floor (`c95a5cf3`) | det floor (EX-23 variant a) | tree floor (`82fb807e`) |
|---|---|---|---|
| ordinary HEAD | FAIL (false BLIND) | **PASS**, `PROVINCE=17 SCORECARD=14 SKILL=3` | PASS |
| `SKILL.md` absent | FAIL UNREADABLE | FAIL UNREADABLE | FAIL UNREADABLE |
| `SKILL.md` blanked (371 empty lines) | FAIL BLIND | **FAIL BLIND** | PASS (silent!) |
| all needles neutered | FAIL BLIND | FAIL BLIND | FAIL BLIND |

Receipts `M1`–`M5` (incl. `M5` showing the tree floor passes the collapse silently — the det
floor dominates it). `df9ffdf9` now implements the det-level floor; final battery
`N1`–`N4`: ordinary `PASS 0/0/0/0` exit 0; absent → `UNREADABLE` FAIL; collapse → `BLIND`
FAIL; blind-all → `BLIND` FAIL; `scope-diff.py v10→df9ffdf9` rows 20/20, 0 flags, exit 0;
counts 6/9/2.

Hunk applicability on `df9ffdf9`: A, B, C anchor exactly once each; **D's anchor now matches
2 sites** (the residual bullet was duplicated in the grown stanza) — apply D with surrounding
context or by hand-merge. `v11` still appears 0 times in the file: the identity drift (§1
hunks B/C) is unchanged and still worth landing at the records commit.
