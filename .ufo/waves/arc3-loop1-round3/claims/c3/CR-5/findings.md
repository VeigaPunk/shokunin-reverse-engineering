# CR-5 findings — attack memo on the C3 landing + the arc3-era citation census

Seat CR-5 (chain c3, critic) · wave `arc3-loop1-round3` · 2026-10-19 · repo
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` · HEAD `c07af80fcf3a60f9c6a0ca09b6e23fb5794d3311`.
Object under attack: the landed artifact pair
`.ufo/gates/citation-drift/pointer-table.json` (sha256 `bfc42f1b…`, 57 entries)
+ `expected.json` (pin `bfc42f1b…`), and the census-bearing artifacts
`claims/c3/EX-41/{02-census.txt,03-census-dispositions.md}` and
`claims/c3/EX-43/{before.md,census.out,candidate-entries.json}`.
All mutations ran in scratch clones under `/var/tmp/cr5-r3/scratch/` (never `/tmp`);
the repo, the table pair and the custody paths were read-only for this seat.

## 0. My independent census, against theirs

Mechanical census (census-cr5.py): added lines of the four arc3 r1/r2 commits
(`fbbbd45`,`14b1682`,`28aa7a9`,`c07af80`) in 10 durable-surface files → **15
citation-bearing added lines**. Compared row-by-row with EX-41's 18-row census
(`attacks/…`, `census/census-cr5.txt` vs EX-41 `02-census.txt`):

- 15/15 of my rows appear in EX-41's census with the same citing line and target;
- EX-41's extra 3 rows are `.ufo/gates/c1-census-v10.py`'s own SCORECARD
  citations (`:850-852`, `:856-1336`, `:908`), which my file list omitted;
  their three landed needles verify at HEAD (probe findings=0);
- no row in my reading is missing from theirs; no row in theirs contradicts mine.

Verdict: **their census is not under-scoped against my reading.** (The roster's
census seat EX-42 delivered nothing — §4 scorecard.)

## 1. Attack: scope creep (pinning what the r4 precedent forbids)

| probe | measurement | verdict |
|---|---|---|
| operator-mutable pins (rule #11 / r4 prune precedent) | zero entries or quoted rows name `config.toml`/`mcp_config`/`.bashrc`/`.profile`/`/home/vgpnk/.` | clean |
| census scope rows widened? | `git status` this round: census instrument unmodified; C3 touched only its two gate files | clean |
| dated records graded as live pointers? | `sc-arc3r2-cites-shonen` grades a dated record but with a tolerant pattern (`SKILL\.md:81-\d+` + `\(craft section`); the SHONEN:6 legit-refresh simulation (81-256, 15/15) fires **nothing** | clean |
| old entries rewritten? | `entries[0:31]`, `quoted`, `exempt[0:3]` objects byte-equal to pre-landing (my diff re-run) | clean |
| **line-pinned section keys** | the two new `sc-arc3r{1,2}-section-key` needles are `exact` at `SCORECARD.md:1338/:1419` — line numbers into an append-managed file, the class the table's own `skill-registry-row` note calls out; simulated head rewrite (+1 line at `:13`) fires **13** findings, 2 of them these (anchor-form variant fires 11) | **flag (form, not scope)** |

## 2. Attack: NO-ENTRY laundering (adjudications used to dodge conforming work)

Re-test method: each adjudicated token was attacked with my own conforming-needle
attempt (16 candidates, `attacks/cr5-candidates.json`, **findings=0 at HEAD**).

| adjudicated token (exempt row) | re-test | verdict |
|---|---|---|
| round-report pin `SKILL.md:371` | pinning it live fires `citation_dead` ("holds `## Refuses`") — measured; the words ARE pinnable (`exact`) but the pointer is measured stale, and a live pin would grade a record's revision | NO-ENTRY valid (r4 «declared baseline / drop with the adjudication named») |
| round-report pin `corpus/README.md:38` | still accurate at HEAD; also covered indirectly by `readme38-arc3r1-token` | NO-ENTRY valid |
| five operator paths | unresolvable as Git objects; rule #11 forbids | NO-ENTRY valid |
| count tokens (`82/82`,`13/13`,`15/15`,`31 entries`,`10.0/10.0`) | no drift class; a pin would fire on every legitimate round (measured: the SHONEN count refresh) | NO-ENTRY valid |
| wave-internal citations (class) | r10 precedent; wave targets are graded where durable surfaces cite them (`skill-rule14-cr2-identity`, `-verdict-identities`) | NO-ENTRY valid |
| `LOG.md`/report rosters without numbers | no stated number ⇒ no drift class; `LOG.md` exempt clause pre-existing | NO-ENTRY valid |
| r1-entry `:5/:11-16/:33` rosters **and** the `:7` recheck line | `:7` is graded for content by `skill-rule14-entry-recheck`; rosters carry no numbers | covered/adjudicated |

Also verified: `exempt` is documentation only — the probe never reads it
(`grep -n exempt citation-drift-probe.py` → no match), so exempt-widening cannot
mechanically hide findings; the 5 added rows are the census's NO-ENTRY ledger.

Verdict: **no laundering found**; every NO-ENTRY group is either non-conforming by
construction or has a measured cause.

## 3. Attack: entry count inflation (needles nobody needs)

- **Non-vacuity battery** (nonvacuity-cr5.py): for each of the 26 added entries a
  mutation was constructed that removes the graded content; **26/26 fire**
  (25 with a single-site mutation; `custody-readme-v2-fieldset` needs both
  occurrences of `MTIME_UTC_RENDER` replaced — precision note, not a dead needle).
  No dead needles.
- **Duplication**: zero added entries duplicate an existing `(file,line,target,must_match)`;
  no added citation line collides with an existing entry's.
- **Scale**: +26 entries vs the r10 precedent's +18 (13→31); heaviest cluster is
  7 needles on `custody-pair/README.md` + its three named example receipts (the r7
  entry holds 7 needles on one file) — inside precedent.
- **Weakest by value, still live**: the three v1-shape example anchors (they guard
  frozen wave receipts named only by the README's table). They earned their keep
  this round: the custody README was rewritten by C2 while this table pins four of
  its sentences — my work-commit emulation (C2's README/py + this table pair)
  yields `reported findings=0 exit=0`.

Verdict: **no inflation above precedent; no dead weight measured.**

## 4. Scorecard for the seats I was asked to check

- **EX-42 (census seat): delivered nothing** — `claims/c3/EX-42/` empty at my last
  poll (10:15, and again ~10:20). The census function was instead delivered by
  EX-41 (implementer, 18 rows) and EX-43 (before-state, 17+1 candidates); both
  were checked against my independent reading (§0).
- **EX-41 (implementer of C3's real target): claims re-measured independently.**
  31→57 entries; prior-31 objects unmodified; expected.json pin == table sha
  (`bfc42f1b…`); probe HEAD default/strict `findings=0`; selftest 13/13; my
  emulated work commit and emulated records commit (CN-2 merged SCORECARD/LOG
  drafts appended) both `findings=0`.
- **EX-43 (before-state): census claims re-measured.** SCORECARD `:1338-1417`
  is pin-free (my regex: zero `path:line` tokens); its candidate objects pass at
  HEAD through my harness (`findings=0`); its blindness proof reproduced with a
  *different* mutation pair (`QUALITY.md:24-25→:23-24` on the entry, `SHONEN.md:6→:7`
  on SCORECARD:1435): real 31-entry table blind, extensions catch.

## 5. Residual risk the parent should re-measure at landing

1. The table pins four sentences of `custody-pair/README.md`, which C2 rewrites
   this round: coupling verified green *now* (work-commit emulation) — re-run the
   probe after the final C2 revision lands in the same work commit.
2. `sc-arc3r{1,2}-section-key` `exact` line pins (see §1 flag); covered by the
   proposed patch text `proposed-section-key-anchor-form.patch.md`.
3. `census-cites-*` needles pin line numbers inside `c1-census-v10.py`; if a later
   round edits that instrument's header comments, these fire — intended, but the
   editing chain should know.