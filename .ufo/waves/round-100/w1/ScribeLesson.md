# ScribeLesson — round 100 wave 1 (L1 KaidokuR100, attempt 1)

Seat: scribe. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Scratch:
`/fast/scratch/hyaku/kaidoku-r100/ScribeLesson` (trap-deleted on exit). Deliverable (never
`corpus/`): `.ufo/waves/round-100/w1/ScribeLesson/lesson-draft-round-100.md` — the `## Mistakes`
rows for `corpus/lessons/round-100.md` (M100-a…M100-d), each with class · evidence pointer ·
captured-by · fix and an explicit "shown able to fail" statement.

## Behaviour

Drafted the three requested item groups plus the two round-99 closure defects, and reproduced the
frozen predicates, the seven-row provenance and the two regex defects by mutation. Nothing in
`corpus/` was touched; no git mutation in the lane or the fleet repo. Revision used: lane `main` at
`b0a7bb8ca` (past A2), frozen counters and controls at F `8e24c29a3`.

## Reproductions (clone at the named rev; `git rev-parse --show-toplevel` asserted before writes)

- C2 base control — `python3 -I -B tools/round-100/registry-selftest-truth.py --root . --rev 6371c88633f6ce6692eaeff17e256b80ad21ece0 --work $S/c2base --json-out $S/c2-base-repro.json` → `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 86 of 93; mismatches 7`, exit 1 — the seven named paths identical to the committed `pre/c2-do-nothing-at-base.json`.
- C2 at A2 — same command, `--rev cbd224ef9b9d2271f415d823bdc4d1e70a0d281c` → `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93; mismatches 0`, exit 0.
- C1 at A1 — `python3 -I -B tools/round-100/pe-upx-corrupt-battery.py --root . --repair tools/round-100/upx-pe-repair.py --rev a610671d7a01e1d762eb7103e6ee9f8a2be287ed --work $S/c1a1 --json-out $S/c1-a1-repro.json` → `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; corrupt 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; exec 1 of 1; effective 119 of 119`, exit 0.
- Counter selftest — `python3 -I -B tools/round-100/registry-selftest-truth.py --selftest` → `SELFTEST cases=22 failures=0`, exit 0.

## Evidence behind the drafted rows (full text in the draft)

**M100-a.** The frozen `CLAIM_RE`/`OBS_RE` (`tools/round-100/registry-selftest-truth.py:60-61`)
carry negative lookbehind; the pre-fix behaviour is reproduced by mutation, one guard at a time —
each kills exactly its own case, exit 1: number-guard of `CLAIM_RE` → `FAIL claim-date-not-count
got=28 want=12`; `cases`-guard of `CLAIM_RE` → `FAIL claim-flag-not-count got=38 want=None`;
`cases`-guard of `OBS_RE` → `FAIL obs-not-showcase got=4 want=None`; number-guard of `OBS_RE` →
`FAIL obs-date-not-count got=28 want=4`. End-to-end, the counter with the unguarded `CLAIM_RE` at
A2 gives `agree 92 of 93; mismatches 1` exit 1 — the false mismatch is the live row
`tools/round-46/gate.py` (claimed 28 vs counted 12), whose cell reads `green 2026-10-28 cases=12
failures=0`. The defective pre-freeze draft is **not** in the lane: `93a35286d`, `d34d53748`,
`e6e9f724c` and the freeze `8e24c29a3` all carry the same counter bytes (sha256 `496a4979…f1f4`).

**M100-b.** `git blame` / `git log -L` (read-only) give the writing rounds: 46 (`47b5e265`), 47
(`e856beb5`), 71 (`c46ea96b`, both rows), 76 (`821d9eb6`, both rows), 89 (`5a46542a`). The seven are
**three** defects; I measured each tool's printed count at the commit that wrote the row.
*Never true:* `round-71/packed-elf.py` printed `"cases": 32` and `round-71/seam-probe.py` printed
`"cases": 9` at `c46ea96b` while the rows said 31 and 7, and neither tool changed afterwards.
*True, then edited under the row:* `round-47/record.py` printed `cases=9` at `e856beb5` and 10
after four same-round commits; `round-76/record-audit.py` printed 17 at `821d9eb6` and 18 after
`a89089306`/`98407fadb`; `round-76/plan-command.py` printed 3 then 7;
`round-89/upx-field-value-repair.py` printed `SELFTEST cases=16` at `5a46542a` and 22 after
`7edab6ae5`/`bc0e0c20c`. *A cell holding two counts:* `round-46/attest.py` read `15 cases at the
3182047 and 50862e4a bytes, 16 from the F3 repair at 65678df0 onward`; the tool printed 16 at that
commit (18 after `332f48849`), but the first-match rule takes the stale 15. Shown able to fail: the
counter is red at base (mismatches 7, exit 1) and each forgery control stays red — F-drop `claimed
86 of 93; mismatches 7`, F-tool `agree 87 of 93; mismatches 7` (a tool edited to print the stale 16
is refused by the pin atom), F-dup `claimed 86 of 93; mismatches 7`. Per-row detail:
`registry-row-provenance.txt`. The defect was never in a committed revision of the counter.

**M100-c.** At `b0a7bb8ca` the round-99 lesson `## Gate` table has 4 lines (header, separator,
S326, S324) and **no** rejection, and `corpus/SOURCES.md` `## Search log` has **no** round-99 or
round-100 note (`grep -cE "round 99|round 100"` → 0; newest note is round 76). The drafted rejection
survives only at `.ufo/waves/round-99/w1/ScoutSources/draft-s327-candidate-rejection.md` (tracked in
the lane). Shown able to fail: **not by a committed gate** — the search-log atoms bind rounds
48/73/74/75 only (`tools/round-49/c2-mismatch.py:52`, `tools/round-74/record-audit.py:372-379`,
`tools/round-76/record-audit.py:655-666`); a D10-shaped probe of the same shape
(`probe/searchlog_probe.py`) returns `absent` rc=1 for `round 99`/`round 100` on the current corpus
and `present` rc=0 on a copy with the note appended — verifiable, but only by a probe.

**M100-d.** The round-99 report §Sources says the end census has "only the W04 warnings that were
already there"; measured, round-99 `pre/census-start.txt` has 32 W04 lines and `l1/census-end.txt`
has 33, the added line being `S326 duplicate url …/src/packer.cpp across scopes` (same URL as S310,
new scope). The QUALITY-187 sweep `.ufo/waves/round-92/w1/ScribeQuality/sweep-w04.sh` exits 2
`nothing checked` on both the round-99 report and the round-99 lesson (neither states a number),
and does fail when a number is written (`DISAGREE: report 33 != receipt 34` rc=1; `agree: report 34
== receipt 34` rc=0). **The same shape recurs now**: round-100 `pre/census-start.txt` has 33 W04
lines, the current census has 34, the added line being `S327 duplicate url …/src/packhead.cpp across
scopes` (same URL as S308) — so the round-100 end-census figure is 34. The S326/S310 scope split is
deliberate (S310's scope excludes the checksum comparison S308; S326's is the overlay check), so the
W04 is expected and the *figure* was the defect.

## Gates and touched surfaces

Both frozen predicates reproduced at the cited revisions: R100-C1 met at A1 (full label, exit 0);
R100-C2 met at A2 (`agree 93 of 93; mismatches 0`, exit 0) and red at B0 (mismatches 7, exit 1). No
claim was re-frozen, re-pinned or re-scored. Only `.ufo/waves/round-100/w1/ScribeLesson.md` (this
file) and `.ufo/waves/round-100/w1/ScribeLesson/` (draft + 8 receipts/probes + 4 mutant selftest
logs + provenance table) were touched; `corpus/` untouched; no git mutation in the lane or the
fleet repo; no commit, no push. Tooling: none installed or upgraded (no pacman, no `uv tool`, no
network fetch).

## Findings (4)

1. **M100-a** — pre-freeze regex read a date's day number (`2026-10-28 cases=12` → 28) and a flag's
   argument (`--min-pristine-cases 38` → a 38-case claim) as case counts; same class observed-side
   (`showcases=4`). Fix = four negative lookbehinds, each pinned by one selftest case; **shown able
   to fail** by four single-guard mutations and end-to-end (unguarded `CLAIM_RE` at A2 → `mismatches
   1` on the live row `tools/round-46/gate.py`).
2. **M100-b** — the seven stale counts are three defects (two never true, four drifted after a
   same-round tool edit, one cell with two counts), written by rounds 46, 47, 71, 76, 89. Fix = the
   seven rows corrected at A2 plus the counter; **shown able to fail** (base control and all three
   forgery controls exit 1).
3. **M100-c** — the round-99 S327-candidate rejection and the round-99/100 search-log note are still
   unregistered at `b0a7bb8ca`; fix = append both; **not shown able to fail** by any committed gate
   (no instrument binds rounds 99/100) — a D10-shaped probe is rc=1 today.
4. **M100-d** — the round-99 "only the warnings that were already there" census claim is false
   (32 → 33 W04) and the QUALITY-187 sweep cannot see it (no number stated → exit 2); the same shape
   recurs this round (33 → 34, the new S327/S308 W04), so the round-100 end-census figure must be
   **34**.

## Out of scope (stated so the record is complete)

- `corpus/lessons/round-100.md` does not exist in the lane; I drafted its `## Mistakes` rows into my
  wave directory only, and did not write the corpus file.
- The lane's own S327-candidate rejection text was not re-derived (I read the round-99 draft) and no
  new source search was run — the lesson draft records the closure defect, not a new row.
- The round-99/100 lesson `## Gate` and `## Search log` appends are left to the integrator; I did not
  re-score either claim or re-derive the C1 controls (another seat owns the attack).

## Artifacts

- Report: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-100/w1/ScribeLesson.md`
- Draft: `…/w1/ScribeLesson/lesson-draft-round-100.md`; receipts: `…/w1/ScribeLesson/{c1-a1-repro,
  c2-base-repro,c2-a2-repro,c2-naive-claim-re-at-a2}.json`, `census-now.txt`,
  `registry-row-provenance.txt`, `probe/searchlog_probe.py`, `selftest-mutant{A,B,D,E}-*.txt` and
  `w04-sweep-demo-33-vs-34.md`, all under the seat's wave directory.
