# SC-6 — chain c3, scribe — E22 disposition record draft

Task (frozen): "E22 disposition record draft: the finding as recorded in SCORECARD
arc2-loop1-round3 carried debt → measured verdict at HEAD → re-keyed/retired rows
with causes → final verdict. Artifact `claims/c3/SC-6/e22-disposition.draft.md`."

Status: **COMPLETE**. Artifact delivered; no repo file outside this seat's two
allowed paths was written.

## 1. Work performed

- Read the frozen claims (`.ufo/waves/arc3-loop1-round1/claims-frozen.md`) and the
  C3 claim; confirmed SC-6 is a scribe seat (not EX-28) → no write to
  `.ufo/gates/c1-census-v10.py`.
- Located the finding verbatim: `SCORECARD.md:850-852` (round-3 carried debt:
  "E22 census scope-table drift (FAIL undeclared=2 at 766-line HEAD vs PASS at
  701-line `b21c0da` — re-key or retire next calibration round)"). Origin
  reproduced from round-3 seats: `.ufo/waves/arc2-loop1-round3/E5.md:14,48,126`
  (the FAIL block, two UNDECLARED blocks `731-737` + `747-766`),
  `.ufo/waves/arc2-loop1-round3/R8.md:227-233` (re-anchor duty + G11 trap).
- Instrument lineage established: v9 sha256
  `213fe679838ea217f4d34aa7d0e85bf73845a42ae49b68c9d8d52b4d38e6707c`
  (`.ufo/waves/arc2-loop1-round2/E22.md:698`, never committed under `.ufo/gates/`);
  v10 created `265e1aa` (433 lines), re-keyed `6bc4c29`; HEAD sha256
  `36e96cd59b622f7b9acd424156d02184fa690df61dd96242899ad9a3b4f52d48`.
- Row-level history extracted with `git show` (read-only) for `265e1aa` and
  `6bc4c29` and from the v9 text in E22.md; `git log --oneline --
  .ufo/gates/c1-census-v10.py` → only those two commits.
- Ran census v10 at HEAD (exit 0, PASS 0/0/0/0) and captured it verbatim:
  `claims/c3/SC-6/census-v10-at-head.txt` (91 lines, sha256 `3b677b8e…`).
- Cross-checked the tail region (`SCORECARD.md:856-1336`, outside the declared
  bound) with raw greps for `rea-agents@`, `6.x.y`, and PTR-shaped pointers.
- Ran four fixture attacks (A1-A4) against byte copies of the three scoped files,
  in `claims/c3/SC-6/fixture/` (since /tmp is unusable); captures kept.
- Audited the instrument's own `units()`/`REA_GATE` behavior on the round-2
  region via a read-only `importlib` load (this created, then I removed,
  `.ufo/gates/__pycache__/`).
- Polled `claims/c3/` and `seats/` during the run; read EX-26, EX-30 seat reports
  and RV-11's v9 re-runs; folded their evidence into the draft (four-way capture
  agreement; v9 stays red at HEAD by construction).
- Wrote `.ufo/waves/arc3-loop1-round1/claims/c3/SC-6/e22-disposition.draft.md`
  (13 KB) with the disposition record + two proposed patch texts.

## 2. Proposed changes

- `claims/c3/SC-6/e22-disposition.draft.md` §6 — **P1**: header stanza for
  `.ufo/gates/c1-census-v10.py` stating the E22 disposition (re-keyed, none
  retired, PASS 0/0/0/0 at HEAD, fixed-bound residual, fail-closed measured).
  **P2**: optional round-records SCORECARD sentence. Both are patch TEXT, not
  applied — EX-28/parent owns the real file.
- No other proposed changes.

## 3. Before→after measurement (chain c3 claim)

Command (at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`, 2026-10-19):

```
$ python3 .ufo/gates/c1-census-v10.py            # exit 0
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1336 loci=9
SKILL.md       lines=371  loci=2
SCOPE-ERRORS (marker assertions): []
G2 positive-assertion guard: ok
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
VERDICT: PASS  (stale=0 ambiguous=0 undeclared=0 unresolved=0)
```

- **Before (the finding, reproduced by RV-11 on the recovered v9):**
  `v9@b21c0da` PASS → `v9@679af5d` FAIL undeclared=2 → `v9@HEAD` FAIL
  undeclared=2 + `SCOPE-ERRORS ["SCORECARD.md:635 marker '2026-10-18' absent"]`.
- **After (HEAD, v10):** PASS 0/0/0/0, exit 0; the two formerly-undeclared
  blocks read `current-ok` (`block 732-738` via G16; `block 748-767` `:753
  kimi=6.7.0 matches live kimi`).
- **Agreement:** my capture is byte-identical (diff empty) to EX-26's and to
  EX-30's/RV-11's captures — four independent runs, one sha256 `3b677b8e…`.
- **Rows changed since the finding:** +2 DATED rows added at `265e1aa`
  (round-2 `:702-767`, round-3 `:768-854`, fixed-bound) + RECEIPT widening;
  three rows shifted +1 at `6bc4c29` (`:636-702`, `:703-768`, `:769-855`) for
  the `:622` capability-row insertion; **retired: none**.
- **Residual measured:** declared bound `:855` vs EOF `:1336` — tail holds zero
  loci at HEAD (raw greps + EX-26's independent grep, both empty).
- Final verdict recorded in the draft: **DISCHARGED by re-key**.

## 4. Attacks / refutations

| # | attack | result |
|---|---|---|
| A1 | inject `rea-agents@6.4.0` at SCORECARD EOF (fixture) | UNDECLARED 1, FAIL, exit 1 — caught (`fixture-tail-locus.txt`) |
| A2 | strip the date only from the round-3 header | PASS — **not caught; attack mis-designed** (that row's marker is the section name). Re-designed as A3; kept as evidence (`fixture-marker-strip.txt`) |
| A3 | strip the marker text fully at `:769` | SCOPE-ERRORS, FAIL, exit 1 — caught (`fixture-marker-strip2.txt`) |
| A4 | corrupt the r1 row's date marker at `:636` | SCOPE-ERRORS, FAIL, exit 1 — caught (`fixture-r1-date-strip.txt`) |
| A5 | silent-skip suspicion: `SCORECARD.md:753` "6.7.0" inside the round-2 row | refuted — the locus IS reported (`block 748-767`, `:753 kimi=6.7.0 -> current-ok`); my first read was a truncated `head -40` |
| A6 | reproduce the finding's before-state | reproduced (RV-11 v9@`679af5d` FAIL undeclared=2, matches E5.md:48) |

## 5. Blockers / notes

- **/tmp user quota exhausted** (`echo test > /tmp/x` → `write error: Disk quota
  exceeded`; python redirect to /tmp → exit 120, empty output). All scratch went
  to this seat's artifact dir instead; the wave rule "scratch under /tmp" is not
  executable on this host right now (matches the standing hazard at
  SCORECARD.md:991). Fixture copies removed after use.
- **Footprint note:** a read-only `importlib` audit created
  `.ufo/gates/__pycache__/c1-census-v10.cpython-314.pyc` (mtime 07:02); removed
  at 07:03. EX-30's T0 porcelain captured it in between. A fresh `__pycache__`
  appeared at 07:04:16 (another seat's module audit, not SC-6) and was left in
  place. No git mutations run by this seat.
- EX-28 (census writer) had not landed at last poll (07:03Z) — P1/P2 are
  proposals; the claim's terminal reading ("PASS at the records commit") is
  parent-owned and re-runnable with `python3 .ufo/gates/c1-census-v10.py`.
