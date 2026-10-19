# SEAT VZ-2 | CHAIN c2 | ROLE convergence — seat report

Wave `arc3-loop1-round2`, chain c2, 2026-10-19. Repo HEAD `14b1682` (no seat
commits; parent integrates records). Deliverable written:
`claims/c2/verdict.md` — **VERIFIED**, pinned to `.ufo/gates/c1-census-v10.py`
final sha256 `d0772ce892223690d571448eeed81778d4a631b58a297d2633c31d241c8d97b5`
(610 L, mtime 09:18:14 −0300); before `6f1d19ff…` (490 L, HEAD blob
`8fee9422…`). The final hash was re-derived at write time and the target was
not edited after (last check 12:20Z+; poller + my own hashes agree).

## 1. Work performed (evidence pointers)

- **Poll protocol**: seats dir re-listed every 60 s, 20+ checks
  (`/var/tmp/vz2-poll.log`, kept because `/var/tmp` is not durable; my reads of
  every landed report are the real artifact). All 29 non-VZ-2 C2 reports landed
  and were read/digested before the verdict's final edit (EX-21/EX-22/SC-3/RV-9
  last; all corroborate, with three wording-level caveats reconciled in place:
  RV-9 whole-stdout byte-identity refuted (4-line delta, verdict line
  unchanged), EX-22 two doc-only receipt lags, EX-15 strict-reading refutation).
- **Independent harness** (own hand, never the real target for writes):
  `claims/c2/VZ-2/tools/battery.sh` (12-root injection battery + blind-instrument
  builder `tools/blind.py`), fixture recipes `tools/injections.md`.
- **Before-state** at `6f1d19ff…`: `claims/c2/VZ-2/before/` (12 outputs incl.
  `t0-baseline.json` counts) — reproduced the round-1 holes S1 (absent SKILL →
  silent PASS), S2 (0-byte SKILL → silent PASS), S3 (blind instrument → PASS
  `loci=0` G2 ok), plus per-file counts 162/6, 1417/9, 371/2.
- **After-state** at `82fb807e…`, `df9ffdf9…`, and **final `d0772ce8…`**:
  `claims/c2/VZ-2/after/`, `final/` (12+ outputs, `scope-diff.txt`,
  `records-sim.txt`, `records-sim-control.txt`, `canonical-head.txt`,
  `ordinary-full.txt`; landed copy preserved as
  `final/c1-census-v10-landed.py`, sha re-verified).
- **Certificates**: CR-5 `scope-diff.py` run by me on the v11 diff (0 flags);
  my records-commit union simulation with a live control; EX-16's stdout digest
  independently reproduced (`1db2ec31…`).
- **Reconciliation**: 29/29 C2 seat reports + their dispositions in
  `claims/c2/verdict.md` §"C2 seat reconciliation".

## 2. Proposed changes

- **None applied.** C2's real-path writer is EX-16 (landed; the diff is the
  patch). My pre-landing fallback `proposed-census-floor-and-unreadable.patch.md`
  (H1+H3 rebased onto the 490-line revision, sha `f4b9f84d…` as a scratch
  candidate) is **superseded** — EX-16's landing covers it and goes further
  (rows-beyond-EOF rule; per-file detection floor). Kept as evidence that the
  closure was independently designed and measured before the landing.
- Chain-text fixes I would *not* apply myself: EX-23's identity/usage nits,
  CR-2's message/label deltas, H5's missing mention in the landed still-named
  list — all named in `verdict.md` §"Named debt".

## 3. Before → after measurement (chain claim, commands + outputs)

Commands (from the repo; `<I>` = instrument path, before = HEAD blob copy):

```
$ python3 <I> --root /var/tmp/vz2/roots/<t> [--quiet|--json]      # battery
$ python3 .ufo/gates/c1-census-v10.py --root .                    # ordinary, live root
$ python3 .ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/scope-diff.py <before> <after>
```

| clause | before `6f1d19ff` | after `d0772ce8` (final) |
|---|---|---|
| ordinary run PASS 0/0/0/0 | PASS, counts 6/9/2 loci | PASS, counts identical, floor line `current-ok loci per file: PROVINCE.md=17, SCORECARD.md=14, SKILL.md=3; total loci=17; floor=1/file`; stdout sha `1db2ec31e8f8896031f1f80a2d90f7e2801af645c4f685d2c55100534d1b7cc0` (`final/ordinary-full.txt`) |
| absent scoped file | SKILL: **PASS exit 0** `lines=0 loci=0` | `FAIL exit 1`, `UNREADABLE (could-not-evaluate): ['SKILL.md: FileNotFoundError']`, `DECLARED FAIL CLASSES: ['UNREADABLE']` (`final/t1`) |
| zero-byte / truncated / dir / EACCES / absent-SCORECARD / all-absent | PASS silent (dir, perm) / FAIL anonymous (SCORECARD, all) | all `FAIL` `['UNREADABLE']` with typed causes (`final/t2, t9, t10, t11, t12`) |
| floor vs blind instrument | **PASS exit 0**, `loci=0`, `G2 … ok` | `FAIL exit 1`, `G2 … SUSPECT ('…=0…')`, `['BLIND-INSTRUMENT']` (`final/t5`) |
| creep audit | — | `rows before=20 after=20 / ADDED 0 / REMOVED 0 / CHANGED 0 / CREEP FLAGS: []` (`final/scope-diff.txt`) |
| records-commit union (C1+C2+C3 literal sections appended) | — | PASS 0/0/0/0, 0 loci added; planted control → `FAIL undeclared=1` (`final/records-sim*.txt`) |

The earlier intermediate revisions were measured too: `82fb807e…` passed this
battery, but `c95a5cf3…` (block-unit floor) false-FAILed the ordinary run —
found by EX-14/CR-2/PL-2/RV-6, fixed in `df9ffdf9…`, and the final revision is
behaviour-identical to `df9ffdf9` (same stdout sha). Details in `verdict.md`.

## 4. Attacks / refutations attempted (verdicts)

| # | attack | verdict |
|---|---|---|
| A1 | Is the closure vacuous? (injection flips vs clean control) | **no** — clean stays PASS with floor met, every injection flips, classes in text + JSON |
| A2 | Emptied-but-present scoped file (my t2) | pre-landing silent PASS; post-landing FAIL — closed by the rows-beyond-EOF leg (not by the floor alone) |
| A3 | directory / EACCES / dangling variants of the H1 class | pre-landing silent PASS; post-landing declared FAIL (typed cause each) |
| A4 | Does the H1 guard false-fire on a legitimate rename? | **no** (CR-2 A1–A4 reproduced by them; my t0 control agrees) |
| A5 | Self-certification (H4): instrument widening itself | **not closed by construction** — external differ flags it (EX-23 A4, EX-16 receipt; residual named in the claim) |
| A6 | Pointer shadowing (SCORECARD.md:291 → config.toml:1478) | **confirmed stale** (live :1478 = `capabilities = [...]`) and **never evaluated** (pointer checks skipped when a block carries a version); named debt, out of the two closures' scope (EX-19 measured the path, I the live content) |
| A7 | Trace the mid-wave defect to its authors | block-unit floor false FAIL at `c95a5cf3` — reproduced via receipts; closed at `df9ffdf9`; no verifier was misled in the record |
| A8 | Does my own scorecard of seats hold? | yes — re-derived the dispositions after the last four reports landed; three wording caveats reconciled in place rather than smoothed over |

## 5. Blockers

- **None standing.** Two caveats for the parent:
  1. **Records commit**: my PASS at the simulated records tree is a pre-flight;
     re-run `python3 .ufo/gates/c1-census-v10.py --root .` after the SCORECARD +
     LOG append; keep appended text locus-free in the census unit or re-key in
     the same commit (standing rule). The C3 draft's pasteable section is
     locus-free; its *notes* block is not (append the literal section only).
  2. **Churn**: nine observed revisions in ~15 minutes; any seat receipt pinned
     to `82fb807e`/`df9ffdf9`/`a4c16763` describes superseded bytes (doc-only
     difference at the end). If the parent lands a further *code* revision, my
     battery (`tools/battery.sh`), the creep audit and the records sim must be
     re-run — the verdict is only as durable as the hash it names.
- No custody path touched (their bytes are C3's to capture); no git mutations;
  scratch under `/var/tmp` and `/dev/shm` only (never `/tmp`).
