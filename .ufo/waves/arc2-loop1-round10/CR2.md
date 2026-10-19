# CR2 (critic) — attack on C2: is the probe-table extension scope creep, given the probe is advisory?

Seat CR2, wave arc2-loop1-round10. Snapshot 2026-10-19T00:58Z, HEAD `c561f00`, worktree clean except untracked `.ufo/waves/arc2-loop1-round10/`. Read-only throughout; my only write is this file. Scratch under `/var/tmp/arc2-l10r10-CR2-scratch/`. No live leg was signaled; both wave services were left untouched.

## 1. Verdict

**Not scope creep as an object; scope creep as a framing, and in two entry forms.**

- **In-scope.** The probe's declared contract is "pins every in-repo citation" (`SKILL.md:371`) and, in its own header, "every citation the lane relies on is listed as an entry" (`.ufo/gates/citation-drift/citation-drift-probe.py:3-8`). The extension is already carried as named debt in the ledger: `SCORECARD.md:1157` — "probe-table coverage of the new citations (gap analysis E41 — non-blocking, probe is advisory)". Extending the table is discharge of a recorded debt, not new scope.
- **But advisory means advisory.** Registry semantics are `0 reported` / `2 could-not-evaluate`, with `--strict` restoring `0 clean / 1 failed / 2 could-not-evaluate` (`SKILL.md:371`), and `SKILL.md:364` — "Neither validates REA correctness, outside review, canonical judgment, or fleet acceptance". **No table entry can block anything.** Round-10 text that says the extension "guards", "protects", or "verifies" the r7/r8 or SHONEN citations is verdict inflation. A green probe row is a report, not protection.
- **Creep form (a) — target-supplied masking.** An `extracted` entry declares its `target` in the table (`citation-drift-probe.py:203-249`); the on-page path token is not graded unless the entry's `pattern` contains it. Measured below: the same entry reports `citation_file_absent` (exit 1) with `target: "QUALITY.md"` and reports **nothing** (findings=0) with `target: "corpus/QUALITY.md"`. So an extension authored the second way **converts a live defect into a green row** — the probe would certify coverage of a citation that a reader still cannot resolve.
- **Creep form (b) — pins on changing-state tokens.** `SHONEN.md:6`'s `13/13` and `SKILL.md:81-243` are current-state claims, not citations. An `exact` pin on either passes today (measured: findings=0) but must be re-pinned every round the rules change — round 9's `ba06c4d` changed both in one commit, and round-9's CR2 caught the staleness by hand. Pinning them buys same-commit churn and zero drift detection.
- **`frozen-run re-verified` cannot be true as written.** The committed probe contains **zero** `frozen` references at every revision (`265e1aa`, `045c1b8`, HEAD); `expected.json`'s `frozen_run` block is unread metadata. The `--frozen` design in `.ufo/waves/arc2-loop1-round4/E9.md:132-135,198-209` was a seat proposal that never landed. My manual rerun at the pinned revision emits **6 findings in 3 classes** against the pinned `expected_findings: ["citation_dead"]`, and no table digest is pinned — so the leg is not reproducible from committed artifacts. Restate it as a manual rerun.
- **One limit the extension cannot buy.** A range `extracted` entry grades span **content**, not span **correctness**. Measured: `SHONEN.md:6`'s `81-243` passes with `must_match` anywhere inside 81..243 even though the craft section's last content line is `SKILL.md:239` and `SKILL.md:242` is the next section heading. The SHONEN range entry will not catch an endpoint overshoot; it catches only loss of content inside the span.

**Admissibility.** Land the extension as debt discharge, advisory wording intact, under three authoring constraints: (1) grade the path token **where it is written** — `target` = the token as written, or an `exact` companion pinning the token form; (2) no pins on count/range tokens — those stay SHONEN's same-commit refresh obligation; (3) each new entry must name what it would redden on, and frozen-target entries (`.ufo/waves/arc2-loop1-round{7,8}/**`, append-only knowledge records) take `quoted`/exempt classification rather than live rows. Coverage claims must count **live** entries, not rows.

## 2. Evidence

All commands from repo root; outputs verbatim except where elided.

**Baseline and custody (my scope does not touch custody; verified read-only as a courtesy).**

```
$ git log --oneline -1 ; git status --porcelain
c561f00 arc2-loop1-round9: records — SCORECARD round section …
?? .ufo/waves/arc2-loop1-round10/

$ awk 'NR>1{print $1"  "$2}' .ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt | sha256sum -c -
/home/vgpnk/.config/devin/mcp_config.json: OK
/home/vgpnk/.omp/agent/mcp.json: OK
/home/vgpnk/.kimi-code/config.toml: OK
/home/vgpnk/.bashrc: OK
/home/vgpnk/.profile: OK
--- row count: 5                                   → CUSTODY 5/5 MATCH
```

**Probe state at HEAD: advisory, clean, extension not landed.**

```
$ python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest --expected .ufo/gates/citation-drift/expected.json | tail -2
CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0

$ … --root . --rev HEAD --table …/pointer-table.json --expected …/expected.json --strict | tail -1
CITATION_DRIFT_VERDICT: clean findings=0 exit=0

$ python3 -c "import json;t=json.load(open('.ufo/gates/citation-drift/pointer-table.json'));print('entries',len(t['entries']),'quoted',len(t['quoted']),'exempt',len(t['exempt']))"
entries 13 quoted 4 exempt 3

$ grep -n "r7\|r8\|SHONEN\|shonen" .ufo/gates/citation-drift/pointer-table.json   → no matches
```

So the table carries **no** r7, r8, or SHONEN entry at HEAD: C2's extension is prospective at this cut. Selftest reproduces 11/11 (C2's first half holds).

**The frozen-run leg is unenforced and does not reproduce its pinned set.**

```
$ grep -n "frozen" .ufo/gates/citation-drift/citation-drift-probe.py   → rc=1, no matches
$ for r in 265e1aa 045c1b8 HEAD; do echo "$r frozen refs: $(git show $r:.ufo/gates/citation-drift/citation-drift-probe.py | grep -ci frozen)"; done
265e1aa frozen refs: 0
045c1b8 frozen refs: 0
HEAD frozen refs: 0

$ … --root . --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f --table …/pointer-table.json --expected …/expected.json --strict
CITATION_DRIFT: citation_dead          entry=sc59-stanza-key-anchor      SCORECARD.md:59 lacks '\[mcp_servers\.rea\]'
CITATION_DRIFT: citation_dead          entry=prov18-stamp-named          PROVINCE.md:18 lacks '17:55:49Z receipt'
CITATION_DRIFT: citation_file_absent   entry=.ufo/waves/arc2-loop1-round3/receipts/config-pre-pair.txt absent at 679af5d…
CITATION_DRIFT: citation_dead          entry=sc698-sc2-refuted-record    SCORECARD.md:699 lacks 'SC2-refuted'
CITATION_DRIFT: citation_out_of_range  entry=mcpreg-errata-anchor-form   corpus/knowledge/2026-10-13-mcp-registrations.md:96 beyond EOF (88 lines)
CITATION_DRIFT: citation_out_of_range  entry=r416-errata-durable-anchor  corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md:946 beyond EOF (936 lines)
CITATION_DRIFT_VERDICT: failed findings=6 exit=1
```

Pinned expectation is `expected.json` `frozen_run: {revision: 679af5d…, verdict: "failed", expected_findings: ["citation_dead"]}`. The *verdict* reproduces (failed / exit 1 under `--strict`); the *finding set* does not (`citation_dead` + `citation_file_absent` + `citation_out_of_range`, 6 rows). Nothing pins the table's digest, so the leg cannot be reproduced from committed artifacts alone. Round 9's C2 report cited `reported findings=0 exit=0` as the probe evidence — that is the HEAD leg, not the frozen leg.

**Measured entry forms (scratch table `/var/tmp/arc2-l10r10-CR2-scratch/t-faithful.json`, probe run against HEAD).**

```
{"entries":[
 {"id":"r7-quality-pathfaithful","kind":"extracted","file":"corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md","line":7,
  "pattern":"`QUALITY\\.md:([0-9]+)`","target":"QUALITY.md","target_group":1,"must_match":"content\\+params-keyed"},
 {"id":"r7-quality-targetfixed","kind":"extracted","file":"corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md","line":7,
  "pattern":"`QUALITY\\.md:([0-9]+)`","target":"corpus/QUALITY.md","target_group":1,"must_match":"content\\+params-keyed"},
 {"id":"shonen-craft-range-exact","kind":"extracted","file":"SHONEN.md","line":6,
  "pattern":"`SKILL\\.md:([0-9]+)-([0-9]+)`","target":"SKILL.md","target_group":1,"target_group_end":2,
  "must_match":"registry-validated analyzers disabled"},
 {"id":"shonen-craft-range-window","kind":"extracted","file":"SHONEN.md","line":6,
  "pattern":"`SKILL\\.md:([0-9]+)-([0-9]+)`","target":"SKILL.md","target_group":1,"target_group_end":2,
  "window":4,"must_match":"kernel-OOM-killed"}]}

$ … --root . --rev HEAD --table /var/tmp/arc2-l10r10-CR2-scratch/t-faithful.json --expected …/expected.json --strict
CITATION_DRIFT: citation_file_absent entry=QUALITY.md absent at HEAD
CITATION_DRIFT: citation_file_absent entry=r7-quality-pathfaithful QUALITY.md (cited by corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:7): absent at HEAD
CITATION_DRIFT_VERDICT: failed findings=2 exit=1
```

Read-out: the **path-faithful** entry catches the live defect; the **target-fixed** entry is silent (masking, creep form (a)); both SHONEN range entries pass (span-content grading, so the `81-243` overshoot is invisible). Second scratch table `t-mask.json` (exact pins on `13/13` and on `` `SKILL.md:81-243` ``, plus a table-supplied cross-entry pointer to `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:19`) → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`.

**The live defect inside the r7/r8 citations.**

```
$ sed -n 7p corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md | cut -c1-160
recheck: a re-run needs the identical request bytes (`QUALITY.md:25`, analyze ids are content+params-keyed). …
$ sed -n 7p corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md | grep -o "QUALITY.md:25"
QUALITY.md:25
$ ls QUALITY.md
ls: cannot access 'QUALITY.md': No such file or directory
$ sed -n 25p corpus/QUALITY.md | cut -c1-120
| 15 | Evidence-id identity claims state the id's domain per verb family with its corpus citation — never a universal formula; recorded: revenger-verifier ids a…
```

The token is bare (`QUALITY.md`, no `corpus/` prefix), the root path does not exist, and the **line number is right** — `corpus/QUALITY.md:25` is criterion 15, the family-scoped evidence-id rule the sentence invokes. So this is a path-token defect, not number drift: precisely the class the probe reports when the entry grades the token where it is written. Both the r6 and the r7 entries carry it.

**The SHONEN range endpoint.**

```
$ grep -n "^## " SKILL.md | sed -n 1,3p
81:## Queue-drain craft (rounds 5-12, distilled in round 13)
242:## Config custody for live-probe rounds (SOP)
$ sed -n 239p SKILL.md
  kernel-OOM-killed (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`).
$ sed -n 243p SKILL.md | cat -A
$
$ sed -n 6p SHONEN.md | cut -c1-130
  asserted: `SKILL.md:81-243` (craft section; rules #11-13 added arc2 rounds 4/7/9); 13/13 rule blocks have resolvable citations, …
```

`SHONEN.md:6`'s range names the craft section but its endpoint `:243` is a blank line inside the config-custody section; the section's last content line is `:239` and the next heading is `:242`. The count `13/13` and the range both reproduce at HEAD by the lane's own counter:

```
$ REV=HEAD bash -c "$(sed -n '93,123p' SCORECARD.md)"
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0,
 "knowledge_files": 81, "mapped": 81, "missing": [], "revision": "HEAD", "rule_blocks": 13}
```

So SHONEN's *claims* are true at HEAD; what an `exact` pin on them would do is redden on the next legitimate change (the round-9 precedent: `git show ba06c4d -- SHONEN.md` changed `81-237`→`81-243` and `12/12`→`13/13` in the same commit that added rule #13).

**Precedent for the classification discipline.** Round-8's gap analysis (`.ufo/waves/arc2-loop1-round8/E4.md:21-25`) already sorted a citation sweep into *live/probe-tracked* (`SCORECARD.md:69,72`), *live/not-tracked* (`SCORECARD.md:23`'s `corpus/README.md:11-67` range — "already one line short at HEAD"), and *dated/append-only — NO action*. That is the standard the round-10 extension should apply; the ledger's own advisory caveat sits beside it at `SCORECARD.md:1157`.

**Recorded, not absorbed (C3-adjacent, not my axis).** Both live legs are still running at my close; I observed nothing about them and signal nothing. My claims are text/instrument-only.

## 3. Verbatim-landable text

Draft round-10 record line (use in the SCORECARD round section and/or the round report; advisory wording preserved, detection claim stated per entry class):

```markdown
- C2 freshness (fleet) — probe-table extension (debt discharge, `SCORECARD.md:1157`;
  the probe is advisory: `SKILL.md:371` reports, never fails; `--strict` restores
  0/1/2; `SKILL.md:364` disclaims correctness/acceptance judgment). Entries added
  for LIVE in-repo citations only, each naming what it reddens on: the r7/r6
  `recheck:` token is graded where written — `QUALITY.md:25` as written does not
  resolve (root `QUALITY.md` absent; the target is `corpus/QUALITY.md:25`,
  criterion 15, number correct) → `citation_file_absent` unless the entries
  re-anchor by append-only errata; frozen wave artifacts and append-only records
  are classified `quoted`/exempt, never live rows. Coverage counts LIVE entries,
  not rows: 13 → ⟨N⟩ entries, of which ⟨L⟩ live. Count/range tokens in `SHONEN.md:6`
  are NOT pinned (changing-state claims; same-commit refresh obligation, round-9
  precedent `ba06c4d`). Selftest re-run: 11/11. Frozen leg: manual rerun at the
  pinned revision `679af5d` — verdict `failed`/exit 1 reproduces; the pinned
  `expected_findings ["citation_dead"]` does NOT (6 findings, 3 classes), and the
  `frozen_run` block is unread by the probe (zero `frozen` refs at `265e1aa`,
  `045c1b8`, HEAD) — recorded as named debt, not as a re-verified leg.
```

Draft entry pair for `QUALITY.md:25` (both forms; land the first, or the second only alongside the first):

```json
{"id": "r7-recheck-quality-token", "kind": "extracted",
 "file": "corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md", "line": 7,
 "pattern": "`QUALITY\\.md:([0-9]+)`", "target": "QUALITY.md", "target_group": 1,
 "must_match": "content\\+params-keyed",
 "note": "grades the path token WHERE WRITTEN: a bare root QUALITY.md reports citation_file_absent. Do NOT substitute target corpus/QUALITY.md — that masks the defect (measured: findings=0)."},
{"id": "r7-recheck-quality-line", "kind": "extracted",
 "file": "corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md", "line": 7,
 "pattern": "corpus/QUALITY\\.md:([0-9]+)", "target": "corpus/QUALITY.md", "target_group": 1,
 "must_match": "per verb family with its corpus citation",
 "note": "the post-errata form: valid only once the append-only errata re-anchors the token to corpus/QUALITY.md; until then this entry reddens (pattern absent)."}
```

Append-only repair text (knowledge entries are records; never rewrite the `recheck:` line in place):

```markdown
Errata (arc2-loop1-round10): the `recheck:` token `QUALITY.md:25` above is a
bare path token and does not resolve from the repo root; the target is
`corpus/QUALITY.md:25` (criterion 15, the family-scoped evidence-id rule the
sentence invokes — the line number was correct, the path was not). The original
token is left verbatim as the record of the pre-errata form.
```

Advisory-boundary sentence for the round report's capability note:

```markdown
The probe is advisory by construction: it reports drift (exit 0) and reserves
exit 2 for could-not-evaluate; `--strict` restores the 0/1/2 gate map but is not
part of the registry entry. Extending the table therefore adds REPORTING
coverage only — it cannot block a round, and a clean probe row is not evidence
that the covered citations are correct, only that the declared targets still
hold the claimed content at the pinned revision.
```

## 4. Labels

- **Observation** — Probe is advisory per registry semantics and the SKILL.md limits sentence; the table holds 13 entries / 4 quoted / 3 exempt and no r7, r8 or SHONEN entry at HEAD; selftest 11/11 at HEAD; the probe has zero `frozen` references at `265e1aa`, `045c1b8` and HEAD, while `expected.json` still carries a `frozen_run` block; my rerun at `679af5d` yields 6 findings in 3 classes vs the pinned `["citation_dead"]`; root `QUALITY.md` is absent and `corpus/QUALITY.md:25` is criterion 15; the r6 and r7 knowledge entries both write the bare token `QUALITY.md:25`; `SKILL.md:239` is the craft section's last content line, `:242` the next heading, `:243` blank, while `SHONEN.md:6` states `81-243`; command A at HEAD is 81/81, 13/13, 10.0/10.0; custody pre-pair re-hashes 5/5; `SCORECARD.md:1157` records the extension as non-blocking debt and names the probe advisory; the two live legs were not observed and not signaled.
- **Inference** — The extension is in-scope debt discharge rather than new scope, because the probe's contract is "every in-repo citation" and the ledger already carries the gap; the masking form (target supplied by the table) is the one way the extension can *reduce* effective freshness by turning a live defect into a green row; range entries grade span content, so a SHONEN range entry cannot detect an endpoint overshoot; pinning count/range tokens converts intended evolution into reported drift; `SHONEN.md:6`'s `81-243` overshooting the craft section by four lines is an authoring artifact, not a claim of protection.
- **Unknown** — Whether C2's round-10 landing actually extends the table, and with which entry forms (nothing landed at my cut); whether the parent judges the r6/r7 `recheck:` token a live pointer or a dated form (it decides defect-vs-record classification, and the repair is append-only either way); whether any r7/r8 citation outside `QUALITY.md:25` and the cross-entry `…r6-pe-midrung.md:19` pointer is intended; the final count of live entries; both live legs' outcomes (out of my scope; C1 owns id stability, C3 the lane census).
- **Scope** — Text and instrument review only; the probe was run read-only over Git objects; no repo file was modified except this report; no service was signaled or killed; scratch confined to `/var/tmp/arc2-l10r10-CR2-scratch/`.
