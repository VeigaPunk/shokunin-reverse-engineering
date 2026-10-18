# CR3 — attack C3: the README lessons-index row is cosmetic

**VERDICT: DROP the row. Do not re-point `corpus/README.md:177`. Do not score freshness improved on the row+re-point pair.** Adjudicate the carried debt NO-CHANGE-with-cause. The counting lesson is already the artifact; the gist row changes no gate the claim names, and the only live effect of the prescribed insert is a pointer break the re-point then undoes.

Axes: freshness delta (does any live stale statement clear?), pointer stability (`sc69-readme-177`), gate observability (command A / census v10 / citation-drift probe), stale-summary harm (a second gist of rules that already have a path cite).

## Evidence

HEAD `54bc9dd90b0aea67c345c1c6aa180e160164d151` (`arc2-loop1-round5: records`). No repo file edited by this seat.

**Observation — the lesson is already reachable without the row.** `git grep -n wave-dispatch-counting` hits `SCORECARD.md:979`, `LOG.md:1206`, `.ufo/reports/arc2-loop1-round5/kaidoku.md:45`. The file is `corpus/lessons/2026-10-18-wave-dispatch-counting.md` (59 lines; standing rules at `:19-37`). Round 5 already scored operability improved with the row deferred (`SCORECARD.md:1003`). The deferral names the hazard this attack repeats: inserting at `:165` shifts `corpus/README.md:177` (`SCORECARD.md:981-984`; `LOG.md:1207-1208`; report `:47-49`). Carried debt is the pair, not a missing rule (`SCORECARD.md:1017-1018`, `LOG.md:1216`).

**Observation — the index is a 3-column gist, not a resolvable citation.** `corpus/README.md:157` header is `| entry | round | gist |`. Last row is `:165`. `:166` is blank. `## Frontier` is `:167`. `:177` is the frontier bullet and contains `held, not frontier`. `corpus/README.md:9` ("A row is written when its file exists, never before") is a write-time anti-phantom rule for the index, not a freshness instrument. `SCORECARD.md:16-17` already records that a lesson-index row shifts later README lines — the insert is a known hazard class, not the freshness move.

**Observation — set-diff is not a standing gate, and the r14 token method is already dirty.**

```text
lesson_files 8
unmapped ['2026-10-18-wave-dispatch-counting']
dangling ['2026-10-13-r2-jq-shadow-verdict']
```

The dangling token is the knowledge cite inside the round-2 gist (`corpus/README.md:160`), not a missing file. r14's `## Lessons` 4/4 (`corpus/knowledge/2026-10-14-r14-02-final-sweep.md:22-24,48`) was a side count on a coverage-map repair, not a scored freshness observable. Command A does not use that method.

**Observation — the three gates the claim couples to the row do not read it, and two are already green without it.**

```text
python3 .ufo/gates/citation-drift/citation-drift-probe.py --root "$ROOT" --rev 54bc9dd --strict
CITATION_DRIFT_VERDICT: clean findings=0 exit=0
```

Probe table entry `sc69-readme-177` (`.ufo/gates/citation-drift/pointer-table.json:53-61`) is `extracted`: it reads the number out of `SCORECARD.md:69` and requires `held, not frontier` on that README line (`citation-drift-probe.py:203-249`). `git grep` of `Lessons|lessons` in the probe and `pointer-table.json`: no matches. Census SCOPE (`.ufo/gates/c1-census-v10.py:86-108`) is 20 ranges over `PROVINCE.md`, `SKILL.md`, `SCORECARD.md` only; `git grep README` in that file is empty. Command A (`SCORECARD.md:92-123`) splits `## Coverage map` through the next `## ` (headers: map `:11`, Knowledge `:70`, Lessons `:155`). At `54bc9dd`:

```text
{"citation_resolved_rules": 11, "counting_in_map": false, "coverage_score": 10.0,
 "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79,
 "missing": [], "rule_blocks": 11, "revision": "54bc9dd"}
```

Lessons are outside the denominator (same statement at `SCORECARD.md:998` / report `:69-70`). A missing gist row cannot fail these three gates. "Landed together with gates green" is a side-harm slogan, not a measurement of the row.

**Observation — the prescribed insert moves the only live pin; the re-point only puts it back.** Live `corpus/README.md:177` cites outside `.ufo/waves` and `.ufo/reports`: `SCORECARD.md:69` (the probe pin) and `SCORECARD.md:982` (the round-5 deferral record). `:742` and `:1018` and `LOG.md:1216` are dated/append-only records of the number, not live pointers. In-memory replay of the extracted check (citing line kept as `:69`; not a git commit, so not a probe invocation):

```text
HEAD PASS cited 177 holds - Runtime-obs depth — …
INSERT_after_165_no_repoint citation_dead cited 177 holds - PE reserve: ARM64X hybrids; …
INSERT_plus_repoint_178 PASS holds - Runtime-obs depth — …
OVERWRITE_166_keep_177 PASS
OVERWRITE_166_plus_claim_repoint_178 citation_dead holds - Blocked-on-operator: IDA …
```

Insert after `:165` makes the file 187→188 and moves the phrase to `:178`. Same-commit re-point of `:69` restores `findings=0`. Net probe delta of the pair: zero. Consuming blank `:166` (the only line-neutral slot) keeps `:177` and makes the claim's prescribed `:177`→`:178` re-point a new `citation_dead`. C1's specified form is a line-neutral map-token append inside `## Coverage map` (`:11-69`), which cannot move `:177`. There is no free ride. The re-point exists only because the row creates the staleness.

**Inference — scoring the pair as freshness-improved is a false delta.** Freshness in this window is disposition of live stale statements (r5: register adjudicated / closed / named, zero unsafe edits — `SCORECARD.md:985-992,1004`). The row clears no stale statement. It manufactures one, then patches it. The gist cannot carry the four standing rules (`corpus/lessons/2026-10-18-wave-dispatch-counting.md:21-37`); a short cell is a duplicate pointer, a long cell is a second summary of the class `SCORECARD.md:68` exists to discharge. r5 paid a pre-commit revert to avoid exactly this (`SCORECARD.md:983-984`). Repeating it spends the freshness slot on bookkeeping.

**Inference — the honest freshness close is a NO-CHANGE disposition, not an insert.** That removes the item from carried debt without moving `:177`, without touching command A's 79/79, and without giving the probe a new way to go red. The 1 unmapped lesson file remains a named nit under `corpus/README.md:9`. It is not this claim's observable. Dropping harms no scored axis (coverage/depth unchanged by construction; operability already improved on the file; calibration's frozen `rubric.json:61` cites `corpus/README.md:157-165` and does not require the new row).

**Unknown —** whether a parent still wants index parity as an unscored chore in a later round. That choice is outside this attack. If it is taken, it must not be scored as freshness, and it must not ship the claim's re-point against a line-neutral overwrite. Census v10 was not executed here (no config read); invisibility of the row follows from SCOPE, not from a live PASS/FAIL.

## Verbatim-landable

Parent lands. This seat does not edit SCORECARD, README, or LOG.

```markdown
- C3 freshness (fleet) — README lessons-index row DROPPED. Not landed. `corpus/README.md:177` not re-pointed. The counting lesson remains the artifact (`corpus/lessons/2026-10-18-wave-dispatch-counting.md`, already cited at SCORECARD.md:979 and LOG.md:1206). A `## Lessons` gist row is not read by command A (map section `:11-69` only; 79/79, 11/11 at `54bc9dd`), census v10 (SCOPE has no README range), or the citation-drift probe (no lessons entry; `sc69-readme-177` findings=0 at `54bc9dd`). Inserting a row after `:165` moves `:177` off `held, not frontier`; the re-point only restores the same findings=0. That pair is not a freshness delta. Carried debt "README lessons-index row + :177 re-point" adjudicated NO-CHANGE-with-cause. `corpus/README.md:9` stays a write-time anti-phantom rule; the one unmapped lesson file is a named bookkeeping nit, outside the denominator, not an axis move.
```

Labels: command outputs, line resolves, and gate source ranges are observation. "False freshness delta" and "NO-CHANGE is the close" are inference. A future unscored index chore, and the live census verdict, are unknown.
