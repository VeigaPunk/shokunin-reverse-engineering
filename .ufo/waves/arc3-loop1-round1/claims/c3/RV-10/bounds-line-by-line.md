# RV-10 — census SCOPE bounds, line by line (v9 → v10@r4 → v10@r8/HEAD)

Seat RV-10, chain c3, wave arc3-loop1-round1, 2026-10-19. Read-only on the repo.
Question audited: **did any re-key relax a bound, and is the r4 open-ended-bound
laundering refusal still in force?**

Instrument versions (all sha256-verified, copies in `/var/tmp/rv10/`):

| version | provenance | sha256 | rows | max declared end |
|---|---|---|---|---|
| v9 | `.ufo/waves/arc2-loop1-round2/E22.md:264-692` (fenced block, never committed under `.ufo/gates/`) | `213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c` (429 L) | 18 | 701 |
| v10 @ `265e1aa` (r4 work) | `git show 265e1aa:.ufo/gates/c1-census-v10.py` | `fab61b07a561f66683178db961aca369668532dceef281c59aa5d37b9a5ba333` (433 L) | 20 | 854 (= EOF@265e1aa) |
| v10 @ `6bc4c29` (r8 work) = HEAD | `git show 6bc4c29:…` / `git show HEAD:…` (identical) | `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48` (433 L) | 20 | 855 (EOF@HEAD = 1336) |

Path history (`git log --oneline -- .ufo/gates/c1-census-v10.py`): exactly two
commits — `265e1aa` (created) and `6bc4c29` (re-keyed). No other edit ever.
The earlier `--follow` listing that showed `b21c0da` is a `--follow` artifact:
`git show b21c0da --name-only | grep -c c1-census-v10` = 0.

## 1. v9 → v10@r4 diff (complete)

`diff c1-census-v9.py v10-r4.py` is exactly three hunks:

- `0a1` — one provenance docstring line added:
  `"""C1 census v10 — v9 (sha256 213fe679…) re-keyed per arc2-loop1-round4 Z1 section 4d."""`
- `103a105,107` — two rows appended (fixed-bound, upper bound = the then-EOF 854):
  ```
      ("SCORECARD.md", 702, 767, "DATED", 703, r"arc2-loop1-round2"),
      ("SCORECARD.md", 768, 854, "DATED", 768, r"arc2-loop1-round3"),
  ```
- `112c116` — `RECEIPT` regex widened: `2026-10-18|receipt|SHA-256|re-grepped`
  → `2026-10-18|receipt|SHA-256|sha256|re-grepped` (adds the hyphenless
  lowercase form the round-2 battery block uses; Z1 §4d). Recognition-set
  widening, **not** a scope bound; the G11 receipt requirement is unchanged.

**All 18 pre-existing rows are byte-identical between v9 and v10@r4.** No
pre-existing bound moved. No row uses an open-ended or overshooting bound
(programmatic max-end check: v9 701, v10-r4 854; no end > 10**6 anywhere).

## 2. v10@r4 → v10@r8 diff (complete)

`git diff 265e1aa 6bc4c29 -- .ufo/gates/c1-census-v10.py` = exactly three rows
shifted +1 (start/end/marker each +1):

| row | @265e1aa | @6bc4c29 = HEAD | width |
|---|---|---|---|
| round-1 records | `635, 701, marker 635` | `636, 702, marker 636` | 67 (unchanged) |
| round-2 records | `702, 767, marker 703` | `703, 768, marker 704` | 66 (unchanged) |
| round-3 records | `768, 854, marker 768` | `769, 855, marker 769` | 87 (unchanged) |

**Semantic justification — content identity, measured** (range extracts hashed
with `sha256sum`; see `evidence/sha256-manifest.txt`):

| r4 range | r8 range | sha256 of both extracts | verdict |
|---|---|---|---|
| `SCORECARD.md` 635-701 @r4 | 636-702 @r8 | `fe4caac6ec500e834c932a71ff9e3b4ce9ed45912c79a8c58c17ed2b16beca24` | IDENTICAL |
| 702-767 @r4 | 703-768 @r8 | `1d2d60e7ddf4fa3b3c791f919ba57b372af06c8410f5dffb7fa436e4d0a6628b` | IDENTICAL |
| 768-854 @r4 | 769-855 @r8 | `068662cd77c51a9f2536a8823bb93bfd1e746b9c5600a90660cc06fea98eedb3` | IDENTICAL |

The +1 shift is fully explained by the r4→r8 `SCORECARD.md` diff, whose hunks
are `@@ -66,7 +66,7 @@` (line-neutral reword), `@@ -619,6 +619,7 @@` (the single
net +1 insertion — the capability row at `:622`), `@@ -852,3 +853,306 @@` (the
records appends at EOF). Every declared range covers the same content it
covered before; **no bound widened, none narrowed, no class flipped** (all
three stay DATED with their original markers).

Marker reality check at HEAD (each DATED row's marker sits on its declared line):
`:636` = round-1 header `… 2026-10-18`; `:704` = round-2 header; `:769` =
round-3 header. Census at HEAD: `SCOPE-ERRORS (marker assertions): []`.

## 3. Bound-vs-EOF posture (and the one deviation found)

- @`265e1aa`: last declared end 854 == file EOF 854 (fixed bound at EOF, as Z1
  §4d prescribed).
- @HEAD: last declared end 855 < EOF 1336. The rounds 4-10 records appends
  (SCORECARD 856-1336) live outside every declared row and carry **zero** gated
  loci (independently verified: EX-26 raw grep + classify() probe, CR-5
  independent checker, RV-11 ungated sweep; reproduced in this seat's fixtures
  A/D/F).
- **Deviation, named**: Z1 §4d's landing-order constraint ("the bound must be
  re-keyed to EOF in the same commit that appends the round-4 records") was
  not executed — `0e8c96b` (r4 records) did not touch the instrument. This is
  a deviation on the **strict** side: a bound below EOF can only turn future
  token-carrying text into UNDECLARED, never absorb it. Not a relaxation.
- **Documentation gap, named**: Z1 §4d's 3-line comment ("Fixed bound at the
  file's current EOF: an out-of-range append must read UNDECLARED … an
  open-ended tail was measured to launder a future stale append") was **not
  landed** — the two rows landed bare, the provenance line only cites "per Z1
  section 4d". Patch text to restore it: `proposed-fixed-bound-guard.patch.md`.

## 4. Non-bound edits in v10's lifetime (for completeness)

- `G16`'s `and not re.search(r"6\.4\.0", str(val))` exclusion: present in v9,
  unchanged by both re-keys → not a re-key relaxation (and its effect is
  conservative: it keeps 6.4.0 values historical rather than promoting them).
- No other line differs across v9 → v10@r4 → HEAD except those in §1/§2.

## 5. Verdict on this artifact's question

**The re-keys relaxed nothing.** v9→v10@r4 added two fixed-bound DATED rows
plus a receipt-recognition widening; v10@r4→v10@r8 shifted three rows +1 with
byte-identical range content (sha256-proven) for a single net +1 insertion.
No bound exceeds its file's EOF at landing, no open-ended bound exists in any
landed version, and the marker assertions pass at HEAD. The r4 refusal of the
open-ended form is preserved in the landed artifact; its re-measurement is in
`fixtures.md` (§2: the same stale append is UNDECLARED under the landed fixed
bound and laundered under both relaxed variants).
