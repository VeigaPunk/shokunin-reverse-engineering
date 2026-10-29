# C2RowS147 — S147 tier correction row (`S152`), round 50 wave 1 (pre-freeze)

Base `7c678ae6d97aedb969fd253b52b3d2882ef1e186`. Lane tree untouched; all fixture commits were made in a scratch clone (`$S/clone`, toplevel asserted before commit, identity set in that clone only). Receipts: `.ufo/waves/round-50/w1/C2RowS147/receipts/` (`receipts.sha256`, `commands.txt`).

## Verdict

**S152 drafted and valid; not landed.** The draft row is at `.ufo/waves/round-50/w1/C2RowS147/S152-row.draft.md`.

- The SEP Popper page re-opened today is byte-identical to the committed snapshot (HTTP 200, 118,135 B, sha256 `2c2d48c6…ec207`).
- Tier **B** is supported by the CORPUS.md tier text, grounded in SEP's own bibliography and named-author byline (not in the A list, which is primary/official material).
- The S147 locator stands: both S147 quotes sit under h2 `2. Backdrop to Popper’s Thought`, before h2 `3. The Problem of Demarcation`.
- `sources-census.sh validate` on the registry with the S152 row exits **0** (0 E-codes; W04 rises 15→16, a warning for the same URL across scopes).
- Two freeze-relevant defects found (F1, F2 below). F1 is the important one: the frozen round-49 counter goes red as soon as round 50 appends any registry row.

## Draft row (S152)

Full text in `S152-row.draft.md`. Key cells:

| cell | value |
|---|---|
| source / URL | Stanford Encyclopedia of Philosophy, Karl Popper — `https://plato.stanford.edu/entries/popper/` (same as S147) |
| kind / tier / scope | `docs` / **B** / `Popper falsifiability criterion` |
| anchor | `Bibliography` (h2) › `Secondary Literature/Other Sources` (h3): "Ackermann, Robert, 1976, The Philosophy of Karl Popper, Amherst, MA: University of Massachusetts Press." (14 words); footer after `Related Entries`: "Copyright © 2026 by Stephen Thornton" (6 words); SEP `substantive revision Fri Jul 31, 2026`; re-opened 2026-10-28 HTTP 200, 118,135 B, sha256 `2c2d48c6…ec207`, snapshot `corpus/evidence/round-49/c2/popper.html` |
| teaches | opens `supersedes S147 —`; tier A→B per CORPUS tier B text; cite Popper's own works (`Primary Literature`, e.g. 1935 *Logik der Forschung*) for the criterion's wording |
| status / opened / recheck | `mined` / 2026-10-28 / `365d` |
| used-by | `corpus/lessons/round-49.md`, `corpus/lessons/round-49-verifier-spotcheck.md` |

`used-by` rationale (grep at base): `corpus/knowledge/` has 0 files citing S147 or the SEP URL. Of the lessons, round-49.md (Gate row) and round-49-verifier-spotcheck.md (closure that routed the tier defect) cite the row. The other eight lessons (round-35, -35-verifier-spotcheck, -36, -38, -40, -43, -44, -45) cite a *different* "S147": the round-5 staged HOST-CONTRACT quarantine candidate that was never a registry row (see F4). They are excluded.

Tier B reasoning (CORPUS.md:93–97): B = "strong secondary (expert write-up with reproducible detail, survey, textbook)". SEP is a named-author expert write-up with a bibliography (receipts `grounds.out`). A = "primary or authoritative for that scope (spec, official docs, source code, original paper, maintainer statement…)"; an encyclopedia entry is none of those. The primary source for the criterion is Popper's *Logik der Forschung* (listed under `Primary Literature`), which the lane has not opened.

## Findings

| # | sev | finding | command (abridged) | exit | evidence |
|---|---|---|---|---|---|
| 1 | — | Live SEP page re-opened | `curl -sS -D … -o popper.live.html -w 'http=%{http_code} bytes=%{size_download}' https://plato.stanford.edu/entries/popper/` | 0 | HTTP 200, 118135 B; response `Date: Wed, 28 Oct 2026 23:32:17 GMT` (UTC 2026-10-28T23:32:17Z); sha256 `2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207` = snapshot sha256 (`sha256sum corpus/evidence/round-49/c2/popper.html`) and `git show 7c678ae6:…popper.html` |
| 2 | — | S147 quotes located in snapshot (tags stripped, entities unescaped, typographic quotes normalised) | `python3 w/locate.py popper.html` (= `tools/round-50/sep-quote-locate.py`) | 0 | quote 1 (21 w) at 12276, quote 2 (9 w) at 12662; nearest preceding heading both `2. Backdrop to Popper’s Thought` (8896), next `3. The Problem of Demarcation` (13007). `locate.out` sha256 `b9a971aa…`. The S147 locator stands. |
| 3 | — | S152 quote located, Bibliography sub-heading | `python3 w/quotes2.py` | 0 | "Ackermann, Robert, 1976, …Massachusetts Press." (14 w) at 79996; preceding h3 `Secondary Literature/Other Sources` (79995), under h2 `Bibliography` (76117). "Copyright © 2026 by Stephen Thornton" (6 w) at 94184, after h2 `Related Entries` (93944). `quotes2.out` sha256 `9cea64ac…`. |
| 4 | — | Tier-B grounding apparatus present | `python3 w/grounds.py` | 0 | `First published Thu Nov 13, 1997; substantive revision Fri Jul 31, 2026`; h2 `Bibliography` with `Primary Literature` (`1935, Logik der Forschung, Vienna: Julius Springer Verlag.`), `Secondary Literature/Other Sources`; h2 `Academic Tools`, `Other Internet Resources`, `Related Entries`. `grounds.out` sha256 `d80c2e3b…`. |
| 5 | — | Registry validates at base | `sources-census.sh validate --root <lane> --file <lane>/corpus/SOURCES.md --today 2026-10-28` | 0 | 0 E-codes; 15 W04 (pre-existing). `val-base.out` sha256 `86296f51…`. Row count 149. |
| 6 | — | Registry validates with S152 appended (scratch clone, commit `132219ec`, 1 insertion) | same, `--root <clone>` | 0 | 0 E-codes; 16 W04 (new: S152 same URL across scopes — warning only). `val-clone.out` sha256 `20a13009…`. NF=13 on the S152 line (a first draft missed the closing `|` and returned E01 exit 1; fixed before this run). |
| 7 | — | Census shape | `sources-census.sh census --file …` (base / clone) | 0 / 0 | base rows 149, A138 B7 C4, mined 141, rejected 8; clone rows 150, A138 B8 C4, mined 142, rejected 8. S147 remains `tier A` (append-only), so the fleet histogram now counts one source as both A and B (F2). |
| 8 | — | Negative: S152 `used-by` naming a missing lesson | `…validate` on `variant-b.md` (scratch mutant) | 1 | `file E11 S152 missing used-by corpus/lessons/no-such-lesson.md`. E11 works. |
| 9 | — | Negative: tier C with `mined` | `variant-c.md` | 0 | W01 only (warning). Tier is not enum-policed against `mined`. |
| 10 | — | Negative: `supersedes` text removed | `variant-a.md` | 0 | exit 0. Scope cells differ (S147 vs `Popper falsifiability criterion`) so E04 is never reached: the `supersedes` mask is not what keeps the row clean (F3). |
| 11 | — | Census self-test | `sources-census.sh selftest` | 0 | `selftest.out` sha256 `6f61744e…` |
| 12 | **high (F1)** | Frozen round-49 counter (`tools/round-49/c2-mismatch.py`, freeze `decc5697` = "round-49: FREEZE") at base | `python3 -I -B tools/round-49/c2-mismatch.py --root <clone> --rev 7c678ae6 --freeze decc5697 --battery` | 0 | atoms 9, mismatches 0, battery clean. `c2-base.out` sha256 `44338e71…`. |
| 13 | **high (F1)** | Same counter at base + S152 row (`--rev 132219ec`) | same, `--rev 132219ec` | **1** | A8 red: `round 49: rows 146 -> 149, derived 146 -> 150`; `round 49: included/excluded 2/1 (screened 3, identified 3), derived 3/1`. With `--battery`: 1 mismatch; `failing` lists `genuine REV is not green` and every single-mutation overlay also shows `['A…', 'A8']` red (no noop). `c2-row.out` sha256 `f84e154e…`; no-battery `c2-row-nobat.out` sha256 `15ebc730…` (base `c2-base-nobat.out` `488524a4…`, exit 0). |
| 14 | — | Counter pinned to the wrong freeze (my first run) | `… --freeze b6f7ca2a…` | 2 | `counter_not_frozen`. `b6f7ca2a` is the round-48 A8 declared freeze; the round-49 counter's freeze is `decc5697`. Discarded; not a lane defect. |

### F1 (high, freeze-relevant) — round-49 counter reads the registry at REV, not at its own window

`tools/round-49/c2-mismatch.py` derives the round-49 registry counts from git at `REV` ("round 49: lane base -> REV"). Any round-50 commit that appends a row past `7c678ae6` makes its A8 atom red at that REV, while the counter's own bytes still equal the freeze (so `counter_not_frozen` does not fire). Round-49's record is green only at `7c678ae6` or an ancestor. Consequences for the plan:
- Any round-50 atom or receipt that re-runs the round-49 counter must pin `--rev` to the round-49 landing revision, not the round-50 tip. Round-50 C2 B-atoms that touch `tools/round-49/**` should say so explicitly.
- Do not "fix" this by editing `tools/round-49/` (byte-frozen). Report it as a disclosed limit of the round-49 counter.

### F2 (medium) — census tier histogram counts superseded rows

The append-only rule leaves S147 at `tier A`. The census has no supersedes resolution, so `tier.A` (138) includes S147 and `tier.B` (8) includes S152. Anyone reading the histogram as "the tiers of the sources we use" over-counts by one source. Recommend a disclosed limit in the lesson, or a census option that drops rows whose id is named in a `supersedes` target.

### F3 (low) — `supersedes` mask not exercised by the census for this row

Scopes differ, so E04 (duplicate URL+scope, no supersedes) never fires; the row is clean with or without the `supersedes` text (variant-a, exit 0). The S147/S152 pair is protected only by the reader. If the L1 wants E04 to actually guard the supersedes pairing, the S152 scope cell must equal S147's scope string exactly; the draft uses the spec's scope `Popper falsifiability criterion`. Decision for the L1.

### F4 (low, attribution) — id `S147` also names a pre-registry staged candidate

Lessons round-35 through round-45 cite `S147` for a staged HOST-CONTRACT (`~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md`) quarantine candidate that was never appended to the registry (`.ufo/waves/round-35/assimilation/quarantine-verdicts.md`). A naive `grep -l S147 corpus/lessons/*.md` returns 10 files, 8 of which are about that other artefact. Any round-50 mistake or census that greps S147 must filter by the registry row. Candidate for M50 `attribution`.

## Method notes
- Snapshot normalisation: tags stripped via `html.parser`, entities unescaped, `’`/`“”` mapped to ASCII, whitespace collapsed. My first locator had a heading-offset bug (length of a '\n'-joined string used against a ''-joined one); fixed before any result above was recorded (receipts are from the fixed script).
- No tools installed or upgraded. Used host `curl`, `python3`, `git`, `sources-census.sh`, `tools/round-49/c2-mismatch.py` (read/run only).
- Nothing committed to the lane; no lane file written. Scratch removed after receipts were copied.

## Not run
- No `--data-run`, no round-50 counter run (not in scope for this seat).
- No check that the entry commands of other rows run; no web-wide search for other SEP-Popper pages.
