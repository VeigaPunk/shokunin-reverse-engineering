# ScoutQualRows — QUALITY coverage map for the round-51 routed defects (r52-w1)

Seat: ScoutQualRows (scout). Read-only seat; no lane file outside
`.ufo/waves/round-52/w1/ScoutQualRows/` was written, no git mutation, no REA run, no download.
Full deliverable: `.ufo/waves/round-52/w1/ScoutQualRows/map.md` (with receipts).

**Verdict.** Two of the six round-51 routed defects are already criterion'd and need no new row
(D1 round-shape → QUALITY **#76**, **#98**; D2 per-seat results fields → **#22**, **#76**). Three are
**uncriterion'd** and their r52 lesson rows must cite the observed failure *before* any QUALITY row 99+ is
added (D3 dispatch interpolation; D4 misroot prevention; D5 census W04 hygiene) — and two of those three
(**D4 misroot**, **D5 census W04**) are **not seeded** in the r52 lesson draft the `ScribeLesson` seat is
building, so the L1 must require them. The sixth (**D6 carried credential L0**) is already governed by fleet
`CORPUS.md` (`:49` "No credential material, ever"; rule 6 `:129`) and is an operator-owned purge; **no new
QUALITY row is advised** for it.

**Three findings that matter most.**

1. **QUALITY numbering has a live collision, and the next free number is 99.** The file holds **98 distinct
   criterion numbers** (last = **98**) across **91 admission-table rows** (1–74, 77–93) and **7 bullet-only
   rows** (75, 76, 94–98) — 107 numbered entries in all. Numbers **77, 78 and 79 each carry two different
   texts**: the table row (round-36/round-38, `corpus/QUALITY.md:85-87`) and the appended bullet
   (round-46/47/48, `:145-149`). The collision is already cited bare in the corpus —
   `corpus/lessons/round-51.md:74` (M51-8) says "QUALITY 77 and command A" and is ambiguous between them.
   New rows must start at **99** and must not reuse 75/76/77/78/79 or 94–98; when a round-52 lesson row cites
   a criterion number it should say "table row N" / "bullet row N" for those three.
2. **The 19 census W04 warnings are mostly a warning-level artifact, not 19 wrong rows.** I re-implemented the
   census rule (`scripts/sources-census.sh:645`) over `corpus/SOURCES.md` (158 rows) and reproduced exactly
   **19** W04s (matching the committed r51 receipt "156 rows, 19 W04 warnings"; a live census run also prints 19
   and `ok`, exit 0 — `census-w04.txt`). Of those, **7 are explained by a `supersedes S0NN` relation** (the
   CORPUS rule-2 shape: S033→S032, S054→S052, S062→S058, S069→S065, S246→S147, S247→S149, S248→S138) and
   **12 are not** (S047, S083, S090, S092, S102, S112, S117, S119, S123, S138, S142, S245). For those 12 I
   verified **0** shared `scope` pairs, **0** shared `teaches` pairs and **0** census `E04` (same URL + same
   scope) hits — they are distinct scopes over one shared URL (e.g. six `rea-agents-6.5.0.tgz` rows each
   teaching a different reader). So the honest r52 disposition is an audit result, not 19 appended
   superseding rows; `plans/round-52-claims.md` §Routed-defect-repairs 6's "correction set" should not be
   manufactured. (Inference, from my own re-derivation over committed bytes — not a lane-gate run.)
3. **Two routed defects have no criterion and no seeded lesson row, and one of them recurred.** D4 misroot
   prevention has **zero** QUALITY coverage (`misroot`/`fleet root`/`stray` → 0 hits) and its evidence is the
   recurrence: r50 **M50-9** (fleet stray, "no preventive fleet-root control exists or was tested") then r51
   **M51-1** (same class again). The r52 repair is a *read-only* sweep helper — a detector; the closure leaves
   prevention operator-side, so any new criterion must claim detection-and-containment only. D3 interpolation
   is likewise uncriterion'd (row #76 covers only the directive prefix; `interpolat`/`unresolved {` → 0 hits),
   though the r52 generator already carries the obligation and `w1/ExecWaveCheck/check-dispatch.py` reports
   `dispatch placeholder check: clean` (receipt exit 0, stdout sha256 `d610c20f…`, 2026-10-30T10:47:22Z) with
   0 `{IDENT}` markers in `w1-spec.json`/`w1-dispatch.json` — but those are the *spec* files, not the rendered
   per-seat prompts, and the checker's regex `\{[A-Z_0-9]{2,}\}` misses lowercase/mixed-case placeholders, so
   "the delivered prompts are placeholder-free" is **not** established by what I read.

Also worth the L1's attention: D2's fix is in place mechanically (per-seat `status.json`; 38 of 48 seat dirs
carry one at read time, 10 do not), but `git ls-files .ufo/waves/round-52` = 5 — the wave tree is untracked, and
QUALITY #22/#76 require the per-seat record to be **retained** (and the totals in the same commit as any stop).
Land the wave dir or a derived per-seat ledger before filing, or the #22 test is unmet at filing.

**One thing the L1 must see that is not mine.** During this seat's read pass the tracked lane file
`.ufo/waves/round-50/w3/ScribeEntryC1.md` was modified (mtime 07:53:57, `git status --porcelain` → ` M …`,
`git diff --stat` → 30 insertions, an "Addendum — the landing outcome"). It is **not** my write: I touched only
`.ufo/waves/round-52/w1/ScoutQualRows/` and my report file. The round-52 seat that owns this material is
`ScribeEntryC1`, whose seat dir is `.ufo/waves/round-52/w1/ScribeEntryC1/` — the edited path is under the
**round-50** wave tree, i.e. a committed file outside the seat's own directory (the wave contract says write ONLY
inside `<YourSeatName>/`), and a moved round-50 baseline for anything that pins those bytes. I did not modify,
stage or revert it; the diff is preserved in the working tree for the L1's judgement. Detail in `map.md` §5.

**Report path:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScoutQualRows.md`
**Deliverable:** `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-52/w1/ScoutQualRows/map.md`
