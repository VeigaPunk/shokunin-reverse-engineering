# CR6 — critic: separability attack (arc2-loop1-round10)

Seat CR6. Read-only on the lane repo except this report. No git mutation of the lane
repo, no config edit, no signal to `arc2-r10-big` / `arc2-r10-mid` (watch-only; never
signaled). Scratch: `/var/tmp/arc2-l10r10-CR6-sim` (a local `git clone` of this repo;
synthetic commits only, source repo never written) and `/var/tmp/arc2-l10r10-CR6-tmp`
(`TMPDIR` for the gate's fixtures). HEAD at measurement: `c561f00`.

Axes: (a) causal separability — can each claim be verified without the other having
landed; (b) line-shift / needle harm from C1's edit into C2's target pointers;
(c) round-baseline integrity (command A `13/13`, `10.0/10.0`) under C1's edit.

## 1. Verdict

**NOT SEPARABLE — as evidence surfaces.** The two claims are cleanly separable as
*write surfaces* (C1 writes `corpus/knowledge/`, C2 writes `.ufo/gates/`; no file
overlap, no shared receipt path), and the stated split is accurate at that level. But
they are **not** separable as *evidence surfaces*, and the coupling runs one way, C1 →
C2:

1. **C2's instrument is a dependency tracker over C1's edit target.** The pointer table
   is a list of citations, and the r7/r8 pointers C2 proposes to add read *out of* the
   two files C1's disposition exists to rewrite. Demonstrated: a candidate extension
   table is clean at HEAD (0 findings), then **4 of 6 entries go `citation_dead`** after
   a simulated C1 landing — including the two entries that pin the literal words
   "id stability across a rerun is UNKNOWN/unknown", which C1 deletes by construction.
2. **C2's own two legs interfere.** The frozen-run is pinned at rev `679af5d7`, where
   the r7/r6 knowledge files *and the pointer table itself* do not exist. Any entry C2
   adds for r7/r8 citations is unresolvable at that rev by construction, so the
   extension changes the frozen-run's observed finding set away from the committed
   expectation.
3. **C1 moves the round baseline.** Command A's `depth_score` bounds-checks SKILL.md
   rule-block citations *into `corpus/knowledge/*`* against those files' line counts at
   the same rev. A one-line shrink of `r7-pe-wall.md` drops `13/13 → 12/13` and
   `10.0 → 9.23` (measured). C1's edit is only baseline-neutral if it does not shrink
   those files.

**Consequence for the wave.** C1 and C2 cannot be independently verified at one cut.
The only sound ordering is **C1 lands first, then C2 re-pins and re-verifies against
post-C1 content, then command A is re-run on the landed tree.** If C2 lands first, its
gate is red at HEAD the moment C1 lands — the round's freshness verdict would be
falsified by the round's own calibration work. One sub-leg is genuinely independent:
`SHONEN.md` carries **no** r7/r8 citations (grep below), so C2's "SHONEN pointers" leg
(its `SKILL.md:81-243` / `PROVINCE.md:88-116` range assertions) is C1-independent and
may be verified alone.

Custody: pre-pair re-verified 5/5 at this cut (§2.0). This seat wrote no custody path.

## 2. Evidence

### 2.0 Custody
- `R=.ufo/waves/arc2-loop1-round10/receipts/config-pre-pair.txt; wc -l <$R; grep -cE '^[0-9a-f]{64}  /' $R; grep -cE '^[0-9]{4}-...Z$' $R; tail -n +2 $R | sha256sum -c -`
  → `6`, `5`, `1`; all five paths `OK` (`.../mcp_config.json: OK`, `.../mcp.json: OK`,
  `.../config.toml: OK`, `.../.bashrc: OK`, `.../.profile: OK`).
  **5/5 MATCH** at `config-pre-pair.txt:1-6`. Point-in-time pre-pair, not post-pair.

### 2.1 Gate baseline reproduced (read-only)
- `python3 .ufo/gates/citation-drift/citation-drift-probe.py --selftest`
  → `CITATION_DRIFT_SELFTEST: CLEAN cases=11 passed=11 failed=0 exit=0`. Matches the 11
  committed cases at `expected.json:1` (`selftest` array).
- `python3 .ufo/gates/citation-drift/citation-drift-probe.py`
  → `CITATION_DRIFT_VERDICT: reported findings=0 exit=0` (default `--rev HEAD`,
  `citation-drift-probe.py:445`). The committed table is clean at HEAD.
- `python3 .ufo/gates/citation-drift/citation-drift-probe.py --rev 679af5d749f2fd48b9d543e3c99d348d5458f90f --strict`
  → `failed findings=6 exit=1`; the observed **set** is
  `{citation_dead, citation_file_absent, citation_out_of_range}`, while
  `expected.json:1` records `"expected_findings": ["citation_dead"]` (single id) and
  `"verdict": "failed"`. Verdict reproduces; the committed finding *set* is narrower
  than the observation. Relevant because C2's claim is to re-verify this frozen-run.

### 2.2 The frozen rev predates the whole r7/r8 apparatus
- `for f in <each>; do git cat-file -e 679af5d7:$f; done` →
  `ABSENT@679af5d7: corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`,
  `ABSENT@679af5d7: corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md`,
  `ABSENT@679af5d7: .ufo/gates/citation-drift/pointer-table.json`,
  `ABSENT@679af5d7: .ufo/waves/arc2-loop1-round8/receipts/r8-ctl-envelope.json`.
- `git log --diff-filter=A -- corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md` → `8cc81a8`
  (round 7). `...-r6-pe-midrung.md` → `596df1c` (round 6). `679af5d7` is round 2 and is
  26 commits behind HEAD (`git rev-list --count 679af5d7..HEAD` → `26`).
- The gate resolves repo targets as Git objects at `--rev` (`citation-drift-probe.py:91`
  `git_show`), never the worktree; an absent target is `citation_file_absent`
  (`:124`, `:168`), which is a **failure** id, not could-not-evaluate
  (`verdict()` returns `FAILED` for it). So extending the table to r7/r8 citations
  *necessarily* adds failure ids to the frozen-run measurement.

### 2.3 The coupling, demonstrated end-to-end
Scratch clone (`git clone -q <repo> /var/tmp/arc2-l10r10-CR6-sim/repo`; source untouched),
candidate C2-extension table `/var/tmp/arc2-l10r10-CR6-sim/ext-table.json` with six
entries mirroring the pointers C2 proposes to pin:

| entry | citing pointer | target |
|---|---|---|
| `sim-r7-11-to-r6-19` | `r7-pe-wall.md:11` | `r6-pe-midrung.md:19` |
| `sim-readme22-to-r7-13-19` | `corpus/README.md:22` | `r7-pe-wall.md:13-19` |
| `sim-readme175-to-r7-13-37` | `corpus/README.md:175` | `r7-pe-wall.md:13-37` |
| `sim-skill226-to-r6-13` | `SKILL.md:226` | `r6-pe-midrung.md:13` |
| `sim-r7-7-unknown-needle` | `r7-pe-wall.md:7` | needle `id stability across a rerun is UNKNOWN` |
| `sim-r6-7-unknown-needle` | `r6-pe-midrung.md:7` | needle `id stability across a rerun is unknown` |

- **(A) pre-C1:** `python3 .ufo/gates/citation-drift/citation-drift-probe.py --root .
  --table /var/tmp/arc2-l10r10-CR6-sim/ext-table.json --strict`
  → `CITATION_DRIFT_VERDICT: clean findings=0 exit=0`. The extension C2 proposes is
  achievable at HEAD.
- **(B) after a simulated C1 landing** (close "rerun id-stability" in both entries: reword
  `r7:7` and `r7:19` in place; reword `r6:7` as a two-physical-line wrap, so `r6` grows
  21 → 22 lines; drop the closed unknown from `r6:21`):
  → `failed findings=4 exit=1`:
  - `citation_dead sim-r7-11-to-r6-19 corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:11 cites corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:19-19, which lacks 'Scale-ladder placement' (holds '')`
  - `citation_dead sim-skill226-to-r6-13 SKILL.md:226 cites corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:13-13, which lacks 'Run envelope' (holds '')`
  - `citation_dead sim-r7-7-unknown-needle corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:7 lacks 'id stability across a rerun is UNKNOWN'`
  - `citation_dead sim-r6-7-unknown-needle corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md:7 lacks 'id stability across a rerun is unknown'`

  The two `holds ''` lines are the sharpest part: the pointer `r6-midrung.md:19` still
  *resolves* — it just now lands on a blank line. A reader (and a naive gate) sees a
  well-formed `path:line` that silently points at nothing. This is exactly the defect
  class rule #11 names, re-created by C1's edit inside C2's table.
- **(C) one wrapped line added in the `r7` body before `:11`** (a realistic C1 reword that
  carries a receipt sentence):
  → `citation_dead sim-r7-11-to-r6-19 ... states no resolvable pointer (pattern
  '2026-10-18-arc2-r6-pe-midrung\\.md:(\\d+)' absent)`. The citing line itself moved off
  `:11`, so the entry dies a second, independent way. (`r7` 37 → 39 lines.)
- **(D) the extension table against the frozen rev:**
  `... --table .../ext-table.json --rev 679af5d7... --strict`
  → `failed findings=5 exit=1`, including
  `citation_file_absent entry=corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md absent at 679af5d7...`
  and `citation_file_absent entry=corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md absent ...`.
  So C2's extension and C2's frozen-run re-verification cannot both be asserted against
  the current committed expectation.

### 2.4 C1 moves the round baseline (command A)
Command A is the fenced python at `SCORECARD.md:92-124` (contract at `:98-124`); it
bounds-checks each SKILL.md rule-block citation `corpus/knowledge/<name>.md:<a>-<b>`
with `1 <= start <= end <= len(file)`. Extracted verbatim to
`/var/tmp/arc2-l10r10-CR6-sim/cmdA.sh` and run against the clone:

- `REV=c561f00 bash .../cmdA.sh` →
  `{"citation_resolved_rules": 13, "coverage_score": 10.0, "depth_score": 10.0,
  "knowledge_files": 81, "mapped": 81, "missing": [], "rule_blocks": 13}` — the seat's
  stated baseline `81/81, 13/13, 10.0/10.0` reproduces exactly.
- post-C1-sim commit where the files **grew** (`r7` 37→39, `r6` 21→22) → identical
  `13/13, 10.0/10.0`. Growth is baseline-neutral.
- post-C1-sim commit where `r7` **shrank** by one line (37→36; the `:19` "two honest
  unknowns" sentence deleted) →
  `{"citation_resolved_rules": 12, "coverage_score": 10.0, "depth_score": 9.23, ...}`.
  The breaking citation is `SKILL.md:239` → `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md:23-37`
  (verified: `git show HEAD:SKILL.md | sed -n '237,239p'`), whose end `37` now exceeds the
  36-line file. **A one-line shrink of C1's target drops the round's baseline.**

### 2.5 The independent sub-leg
- `grep -n "r7-pe-wall\|r6-pe-midrung\|pointer-table\|citation-drift\|id-stability\|ev_a4aa9b0d\|ev_8b688ce7" SHONEN.md`
  → **no output**. `SHONEN.md` cites no r7/r8 knowledge file and no gate artifact; its
  pointers are `SKILL.md:81-243` (`SHONEN.md:6`) and `PROVINCE.md:88-116` (`:16`), i.e.
  files C1 does not write. C2's SHONEN leg is separable from C1; only its r7/r8-citation
  leg is coupled.
- `grep -n "corpus/knowledge\|SCORECARD.md\|SKILL.md\|PROVINCE.md" .ufo/gates/c1-census-v10.py`
  → the census `SCOPE` (`:86-108`) declares ranges only in `PROVINCE.md`, `SKILL.md`,
  `SCORECARD.md` — **not** `corpus/knowledge/`. So C1's knowledge edits do not trip the
  census's UNDECLARED-locus rule; that particular coupling is absent. (The census is a
  different instrument from command A; recorded to close the question, not as a finding.)

## 3. Verbatim-landable text

A sequencing constraint for the wave (parent to place in the round's integration notes
or the round report; it asserts no new fact, only the measured dependency):

```markdown
- **C1/C2 ordering (CR6).** The r7/r8-citation leg of C2's probe extension reads out of
  the two knowledge entries C1 rewrites (`corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`,
  `...-r6-pe-midrung.md`), and the probe resolves targets at a pinned `--rev`. Land C1
  first, then re-pin and re-verify C2's extension against post-C1 content, then re-run
  command A on the landed tree. A simulated C1 landing turned 4 of 6 candidate extension
  entries `citation_dead`, and a one-line shrink of `r7-pe-wall.md` moved command A to
  `12/13, 9.23`. C2's SHONEN leg is independent of C1.
```

An amendment for the gate's frozen expectation, if C2's extension lands (drafted; the
parent decides whether to take it — it is a content change to a committed instrument):

```json
"frozen_run": {
  "revision": "679af5d749f2fd48b9d543e3c99d348d5458f90f",
  "note": "the revision the committed verdict was measured against; a run over a different revision is a different measurement. Measured finding set at this rev is {citation_dead, citation_file_absent, citation_out_of_range}; entries added for post-round-2 targets (r7/r8 knowledge files) are absent here by construction and read citation_file_absent.",
  "verdict": "failed",
  "expected_findings": ["citation_dead", "citation_file_absent", "citation_out_of_range"]
}
```

## 4. Observation / inference / unknown

- **Observation:** custody 5/5 at this cut; selftest 11/11; committed table clean at HEAD;
  committed table at `679af5d7` yields verdict `failed` with finding set
  `{citation_dead, citation_file_absent, citation_out_of_range}` against a committed
  `expected_findings` of `["citation_dead"]`; r7/r6 knowledge files, the pointer table,
  and the r8 receipt are all absent at `679af5d7`; command A reproduces `81/81, 13/13,
  10.0/10.0` at `c561f00`; `SHONEN.md` cites no r7/r8 artifact; the census `SCOPE`
  excludes `corpus/knowledge/`.
- **Inference:** the claims are separable in write surface but coupled in evidence. C2's
  instrument measures citations *into* C1's edit target, so C2's verdict is only
  well-defined relative to a fixed C1 content — i.e. C2 is a *downstream* claim, not a
  sibling. Command A's `depth_score` is likewise a function of C1's edit through the
  line-count bounds check, in the shrink direction only.
- **Unknown:** whether C2's actual extension entries will pin the same pointers I
  mirrored (my six are a reconstruction from the r7/r8 citation set at HEAD, not C2's
  landed table); whether C1 will land by reword-in-place (line-neutral, needle-breaking)
  or by append (line-neutral, needle-preserving in the errata but not in the body);
  whether C2 defines its frozen-run re-verification as verdict-only (survives the
  extension) or as an exact finding set (does not); whether C1's closure will grow or
  shrink the two entries — growth is command-A-neutral, a one-line shrink is not; and
  the live legs' outcomes, which this seat did not read (watch-only, no signal).
- **Scope:** textual + offline-simulation review only; no live-service inspection, no
  signal to either running leg; the only repo write is this report.
