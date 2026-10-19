# EX-12 (c2, executor) — line-by-line analysis: H1 patch text vs HEAD census (post-G18)

Wave: arc3-loop1-round2. Date: 2026-10-19. Seat task as frozen: line-by-line
analysis of the H1 patch text vs the current HEAD census (post-G18) — conflicts,
drift, required adjustments.

Sources analysed (read-only)
- Patch text: `.ufo/waves/arc3-loop1-round1/claims/c3/RV-11/proposed-missing-file-guard.patch.md`
- Target at HEAD: `.ufo/gates/c1-census-v10.py`, sha256 `6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b`, 490 lines
  (working tree == HEAD blob at capture; `git status --porcelain .ufo/gates/` listed no
  modification of the target at that moment). Frozen copy: `/var/tmp/ex12/census-head-6f1d19ff.py`.
- Drafting-era target: `git show e845c2b:.ufo/gates/c1-census-v10.py` =
  sha256 `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`, 433 lines —
  the sha the still-open H3 patch text pins as "before-state".

## 0. Summary of verdicts

| Item | Verdict |
|---|---|
| Hunk 1 text vs post-G18 HEAD | exact match at line 438 (offset +57); lands verbatim |
| Hunk 2 text vs post-G18 HEAD | context line byte-equal, but the fenced diff does **not** apply under a strict applier (fuzz=0): `patch` rejects it, `git apply` rejects the whole patch |
| Semantic conflict with G18 | none — edit surfaces are disjoint (G18 = docstring/SCOPE/`scope_of`/`assert_markers`; H1 = `main()` read loop + verdict expression) |
| Citation drift | 3 stale citations (pre-G18 anchors) — corrected numbers below |
| Behaviour claim (absent scoped file) | reproduces: PASS exit 0 → FAIL exit 1 with the UNREADABLE class (measured) |
| Required adjustments | 4 (text-report line placement, `--json` class, `None`-safe counts print, docstring verdict definition) |

## 1. Anchor drift (the patch was drafted against 36e96cd5…, HEAD is 6f1d19ff…)

EX-28's E22 edit (commit fbbbd45) inserted 44 docstring lines and re-keyed one
SCOPE row, so every file:line citation in the H1 patch text is stale:

| Citation in patch text | Text at that line at HEAD | Correct post-G18 anchor |
|---|---|---|
| `c1-census-v10.py:382-390` ("current code … `main()`") | 382-390 = docstring/`def assert_markers` region | read loop = **438-445** (the modified line is **438**, outside the cited range even pre-G18: pre-G18 it was 381) |
| `c1-census-v10.py:397-398` (verdict expression) | 397-398 = `assert_markers` loop | **454-455** |
| `(SKILL.md: c1-census-v10.py:94-95)` (its rows are CURRENT) | 94-95 = docstring | **147-148** (`("SKILL.md", 10, 16, "CURRENT", …)` / `("SKILL.md", 18, 20, "CURRENT", …)`) |
| H3 patch text: "before-state sha256 36e96cd5…" | — | now `6f1d19ff…` (adjacent finding, same class) |

Each context/removed line of both hunks was byte-compared against the post-G18
file: all equal (e.g. `ok = (not stale) … and (not scope_errors) \` is line 454
in both the pre-G18 397 and post-G18 454 slots).

## 2. Applicability, measured (not asserted)

Reconstructed verbatim from the md's two fenced `diff` blocks (extractor printed
the blocks; counts checked: block 1 = 8 old / 9 new, block 2 = 2 old / 2 new):

```
$ patch -p0 --fuzz=0 --dry-run demo.py < h1-verbatim.patch      # post-G18 HEAD
Hunk #1 succeeded at 438 (offset 57 lines).
Hunk #2 FAILED at 398.
1 out of 2 hunks FAILED                                           # exit 1
$ (cd gitapply && git apply --check -p1 g.patch)                  # git-style headers
error: patch failed: census-head-6f1d19ff.py:397
error: census-head-6f1d19ff.py: patch does not apply              # exit 1
$ patch -p0 demo2.py < h1-verbatim.patch                          # GNU default fuzz
Hunk #1 succeeded at 438 (offset 57 lines).
Hunk #2 succeeded at 455 with fuzz 1 (offset 57 lines).           # exit 0
```

Same fuzz=0 rejection reproduces against the pre-G18 revision the patch was
drafted against, so this is a defect of the patch text, not of HEAD.

Root cause isolated by substitution: hunk 2's only context line ends with a
backslash (`… and (not scope_errors) \`). Replacing that context line with a
non-backslash neighbour (`verdict = "PASS" if ok else "FAIL"`) makes the hunk
apply at fuzz=0 (`exit 0`). A one-line hunk without the backslash context also
applies at fuzz=0. Content after the default-fuzz apply was verified equal to a
hand-applied control (`sha256 2586b014…` for both).

### Half-application hazard (measured)

`patch` applies hunk 1 and leaves hunk 2 in `.rej` — exit 1, but the file is
already written. Reconstructed that state (hunk 1 only, control sha-verified
against HEAD except the hunk-1 lines):

```
$ python3 census-hunk1only.py --root fixtures/absent-skill --quiet
SKILL.md       lines=0    loci=0
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)    # exit 0
```

The file parses (`ast.parse` ok), the run does not warn, and the guard is inert:
`unreadable` is collected but never consulted. A half-landed patch would have
read as "the variable exists → the fix is in". Verification must therefore
reproduce the absent-file FAIL, not inspect the diff.

## 3. Conflicts with post-G18 HEAD

None. Edit surfaces are disjoint: EX-28's diff hunks are at (pre-G18) 1-48,
57-59, 109-115, 141, 253-254, 263-265 — docstring, SCOPE row, `scope_of`,
`assert_markers`; H1 touches only `main()`'s read loop (438/442-443) and the
verdict expression (455) plus a new print beside `SCOPE-ERRORS` (480). G18's
`marker line inside its own range` check adds a SCOPE-ERROR path that already
fails absent PROVINCE/SCORECARD runs; H1's term is additive on the same verdict
(`ok = … and (not unreadable)`), and exit stays 1 in both cases:

```
HEAD  on absent-province-md   exit=1   (G15 "marker uncheckable" ×3)
H1    on absent-province-md   exit=1
HEAD  on absent-scorecard-md  exit=1   (G15 ×10)
H1    on absent-scorecard-md  exit=1
```

Scope bounds are untouched by H1 — creep audit on both my variants, and on the
landed revision:

```
$ python3 …/c3/CR-5/tools/scope-diff.py census-head-6f1d19ff.py census-h1A.py
rows before=20 after=20 | ADDED (0) | REMOVED (0) | CHANGED (0) | CREEP FLAGS: []
$ python3 …/scope-diff.py census-head-6f1d19ff.py census-live-82fb807e.py
CREEP FLAGS: []            # same, for EX-16's landed revision
```

`citation-drift-probe.py` at HEAD: `findings=0 exit=0` (the probe's pointer
table does not pin the census file, so a rename/edit of the target does not
break it — checked `expected.json`: no `census`/`gates/c1` key).

## 4. Required adjustments (H1 as drafted is incomplete on these four)

1. **The text-report line is prose, not a hunk.** The md says "plus a line in
   the text report next to `SCOPE-ERRORS`, e.g. `print("UNREADABLE …")`" — the
   fenced diff has only 2 hunks. Landing must place it explicitly (I placed it
   directly after the scope-errors print; line 482 post-G18).
2. **`--json` must carry the class.** With only the md's hunks, the machine
   output has no cause: measured JSON keys of the patched variant =
   `[…, stale, undeclared, unresolved, verdict]` — no `unreadable`, while
   `verdict: FAIL`. "FAILs with a declared class" then holds for the human
   path only. Adding `"unreadable": unreadable` to the json dict fixes it
   (verified: key present, `['SKILL.md: FileNotFoundError']`).
3. **Counts print must tolerate the unevaluable file.** Declaring the class via
   `lines=None` (the natural way to stop printing the misleading `lines=0
   loci=0`) breaks `print("%-14s lines=%-4d loci=%s" …)`: measured crash —
   `TypeError: %d format: a real number is required, not NoneType` at
   `c1-census-v10.py:533` (intermediate revision, sha `65442158…`, 12:06Z).
   That crash exits 1, so an exit-code-only check reads "FAIL as claimed" while
   no class and no verdict line were emitted.
4. **Docstring self-description.** The verdict definition (post-G18 `:120-122`)
   enumerates the PASS terms; it must gain the unreadable term or the
   instrument's own description contradicts its behaviour. Adjacent, pre-existing
   self-reference drift worth fixing on the same touch (rule-#14 direction):
   `:47` says "instrument v9" and `:123` says `Usage: python3 c1-census-v9.py`
   inside a file named `c1-census-v10.py`.

## 5. Behaviour matrix (my fixtures; exit codes)

Fixtures: copies of the three scoped files from HEAD; only the named file is
altered. Scratch roots live in `/var/tmp/ex12/fixtures/`.

| fixture (SKILL.md) | HEAD 6f1d19ff | hunk-1-only (half-applied) | H1 as drafted (+fuzz collide) | landed 82fb807e |
|---|---|---|---|---|
| intact (control root) | 0 | 0 | 0 | 0 |
| absent | 0 (silent PASS) | 0 (inert) | 1 UNREADABLE | 1 UNREADABLE |
| 0-byte | 0 (silent PASS) | 0 | 0 (residual) | 1 UNREADABLE |
| blank-only (`\n`) | 0 | 0 | 0 (residual) | 1 UNREADABLE |
| directory in place | 0 (silent PASS)¹ | 0 (inert) | 1 UNREADABLE | 1 UNREADABLE |
| dangling symlink | 0 (silent PASS) | 0 | 1 UNREADABLE | 1 UNREADABLE |
| mode 000 (EACCES) | 0 (silent PASS) | 0 | 1 UNREADABLE | 1 UNREADABLE |
| 371 blank lines (padded) | 0 (silent PASS) | 0 | 0 (residual) | 0 (silent PASS) |

¹ directory-in-place: Python raises `IsADirectoryError` (an OSError), which the
HEAD `except OSError:` swallows exactly like an absent file, so `lines=0 loci=0`
and PASS — the H1-updated catches it. Raw captures: `evidence/out-*.txt`,
`evidence/fixture-matrix.txt`.

`--json` on the landed revision for the absent case: `verdict FAIL`, counts
`SKILL.md {lines: null, loci: null}`, `declared_fail_classes` present, exit 1.

Ordinary run at the repo root stays `PASS 0/0/0/0` at HEAD and on the landed
revision (`PROVINCE 162/6`, `SCORECARD 1417/9`, `SKILL 371/2`) — the H1/F1
claim's "ordinary runs at HEAD stay PASS" holds.

## 6. Residuals and attacks (verdicts)

- **F1, half-applied patch → inert guard.** Measured (section 2). Severity: the
  fix can be present-but-dead without any syntax or runtime signal.
- **F2, strict appliers reject the fenced diff.** Measured; cause isolated to the
  backslash-terminated context line. `git apply` is atomic, so an implementer
  using it would land *nothing* and might report "patch refused".
- **F3, `--json` without the class.** Measured on the (md-hunks-only) variant.
- **F4, counts print crash on the unevaluable file.** Measured on the
  intermediate in-flight revision `65442158…`; fixed by `%-4s` in `82fb807e…`.
- **F5, content-erased scoped file read silent PASS — CLOSED in the final landed
  revision.** At HEAD and on the intermediate landing `82fb807e…`, a scoped file
  padded to ≥ its declared max end (371 blank lines) has no "rows beyond EOF",
  yields `loci=0`, and the then tree-level floor was satisfied by the other
  files: `VERDICT: PASS`, `DECLARED FAIL CLASSES: []`, `SKILL.md lines=371
  loci=0`, exit 0. That is the per-file blindness residual: H1 closes
  *unreadable*, H3's variant A closes *whole-tree blindness*; neither sees a
  *per-file* erasure. Final revision `df9ffdf9…` (12:12:15Z, EX-16's receipt)
  closes it with EX-14's variant B — `h3_ok = all(floor[f] > 0 for f in files if
  filelines[f] is not None)` (`c1-census-v10.py:556`) — and my padded fixture now
  reads exit 1, `DECLARED FAIL CLASSES: ['BLIND-INSTRUMENT']` (re-measured).
  It was not a round-1 injection (checked the round-1 c3 artifacts and EX-17's
  before-* fixture names; no emptied/padded-file injection exists), so the frozen
  C2 claim was never violated. Residual still open in the landed revision (its
  own docstring names it): per-needle partial blindness — PIN alone neutered
  keeps every file's current-ok count above zero and still reads PASS.
- **F6, hand-built hunks carrying that context line** (informational, measured):
  the trigger is not the backslash character as such — a `diff -u`-generated hunk
  that carries the same line applies at fuzz=0 — but a hand-built hunk with that
  line as context is rejected even when byte-equal. Practical rule: generate
  hunks with `diff`, or keep them bare (rem/add only; the bare form applies at
  fuzz=0). `h1-reanchored-hunks.patch.md` ships the diff-generated form.

## 7. Status against the landed revisions (independent re-derivation)

Observed shas of the live target: `6f1d19ff…` (HEAD, 490 lines, 12:01Z) →
`2a89793a…` (12:06Z) → `65442158…` (556 lines, 12:06Z, crashed on its own fail
path, §4.3) → `82fb807e…` (560 lines, 12:07Z; receipt recorded 12:06:58Z) →
`df9ffdf9…` (601 lines, 12:12:15Z; receipt recorded 12:12:15Z, "r9 final").
The before-copy in EX-16's receipts still hashes `6f1d19ff…`.

My independent fixture runs of the last two revisions reproduce the claim:
absent / 0-byte / blank / directory / dangling / EACCES all → exit 1 with
`DECLARED FAIL CLASSES: ['UNREADABLE']`; `df9ffdf9…` additionally FAILs the
padded fixture as `BLIND-INSTRUMENT`; control root and repo root stay
`PASS 0/0/0/0` (`PROVINCE 162/6`, `SCORECARD 1417/9`, `SKILL 371/2`); creep
audit against HEAD: 0 flags for every revision I ran it on. All four required
adjustments of section 4 are present in the landing (text line `UNREADABLE
(could-not-evaluate)`, `--json` class + `declared_fail_classes`, `%-4s` counts,
docstring term), so sections 1-4 are for the record and for any re-apply, not an
open request. Every statement above is pinned to the sha cited; the target is a
moving file.

## 8. Repro commands (all scratch under /var/tmp/ex12)

```
bash /var/tmp/ex12/run-matrix.sh                     # baseline matrix + reconstruction
# anchors / strictness:
cp /workspace…/c1-census-v10.py demo.py; patch -p0 --fuzz=0 demo.py < /var/tmp/ex12/h1-verbatim.patch
(cd /var/tmp/ex12/gitapply && git apply --check -p1 g.patch)
# landed-revision check:
python3 /var/tmp/ex12/census-live-82fb807e.py --root /var/tmp/ex12/fixtures/absent-skill --quiet; echo $?
python3 /var/tmp/ex12/census-live-82fb807e.py --root /var/tmp/ex12/fixtures/padded-skill --quiet; echo $?
```
