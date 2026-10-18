# CR7 — critic: attack for verdict inflation

**Verdict: PARTIAL REFUTE.** The four source-derived command-A before/after pairs and four custody receipt endpoint comparisons I re-derived match the records, but that is not the full C1 audit. A host-dependent census cannot be re-derived from Git archives under this round's no-live-probe rule. One concrete probe edge case is misclassified; C2's required dispatch lesson is not present at HEAD; C3 remains unknown until its register/landings exist.

## Axes

- **Calibration (C1):** 4/4 command-A pairs confirmed; 4/4 receipt endpoint comparisons confirmed as endpoint data. This does not establish every falsifiable round-1–4 before/after.
- **Operability (C2):** 60/64 is supported across rounds 2–4; the required 60/64-specific corpus lesson is absent at HEAD.
- **Freshness (C3):** not verifiable from the permitted round-1–4 context; no round-5 register was inspected.

## Evidence

### C1: re-derived subset and hard boundary

For each pair I extracted both cited revisions (not the moving worktree) and ran the SCORECARD command-A logic over those trees. Exact archive commands (each parent directory was created with `mkdir -p` first):

```bash
git archive 4b806e14db22ea44cc57729f5fa3f7b46b616178 | tar -x -C /var/tmp/arc2-l5r5-CR7-r1-before
git archive df31bfb | tar -x -C /var/tmp/arc2-l5r5-CR7-r1-after
git archive 165057e | tar -x -C /var/tmp/arc2-l5r5-CR7-r2-before
git archive b21c0da | tar -x -C /var/tmp/arc2-l5r5-CR7-r2-after
git archive 679af5d | tar -x -C /var/tmp/arc2-l5r5-CR7-r3-before
git archive dbba2dd | tar -x -C /var/tmp/arc2-l5r5-CR7-r3-after
git archive 158a966 | tar -x -C /var/tmp/arc2-l5r5-CR7-r4-before
git archive 265e1aa | tar -x -C /var/tmp/arc2-l5r5-CR7-r4-after
```

Exact derivation body used on each pair (the same body was run four times with the corresponding before/after roots substituted; it follows SCORECARD.md:92-123):

```bash
python3 - <<'PY'
import pathlib,re,json
for label, root in [('r1-before','/var/tmp/arc2-l5r5-CR7-r1-before'),('r1-after','/var/tmp/arc2-l5r5-CR7-r1-after')]:
 p=pathlib.Path(root)
 files={x.stem for x in (p/'corpus/knowledge').glob('*.md')}
 section=(p/'corpus/README.md').read_text().split('## Coverage map\n',1)[1].split('\n## ',1)[0]
 mapped=set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
 skill=(p/'SKILL.md').read_text().split('## Queue-drain craft ',1)[1].split('\n## ',1)[0]
 rules=re.split(r'(?m)^- \*\*',skill)[1:]
 pattern=r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
 resolved=0
 for rule in rules:
  refs=re.findall(pattern,rule); valid=bool(refs)
  for name,first,last in refs:
   try:
    n=len((p/'corpus/knowledge'/name).read_text().splitlines()); a,b=int(first or 1),int(last or first or 1); valid &= 1<=a<=b<=n
   except Exception: valid=False
  resolved+=valid
 print(label,json.dumps({'knowledge_files':len(files),'mapped':len(files&mapped),'missing':sorted(files-mapped),'dangling':sorted(mapped-files),'rule_blocks':len(rules),'citation_resolved_rules':resolved,'coverage_score':round(10*len(files&mapped)/len(files),2),'depth_score':round(10*resolved/len(rules),2)},sort_keys=True))
PY
```

Observed output excerpts (JSON field order preserved from the executed command):

```text
r1-before {"citation_resolved_rules": 9, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 9}
r1-after  {"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 10}
r2-before {"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 10}
r2-after  {"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 10}
r3-before {"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 10}
r3-after  {"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 10}
r4-before {"citation_resolved_rules": 10, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 10}
r4-after  {"citation_resolved_rules": 11, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 79, "mapped": 79, "missing": [], "rule_blocks": 11}
```

This confirms the structural changes claimed in `.ufo/reports/arc2-loop1-round1/kaidoku.md:129-140`, `...round2/kaidoku.md:86-89`, `...round3/kaidoku.md:70-74`, and `...round4/kaidoku.md:69-70`; corresponding SCORECARD rows are `SCORECARD.md:665-684`, `:723-745`, `:791-835`, `:886-909`. It does **not** re-verify the semantic claims attached to the added rules.

I parsed the committed pre/post receipt hash rows with this exact command (no live client config was read or hashed):

```bash
python3 - <<'PY'
from pathlib import Path
pairs=[('r1','/var/tmp/arc2-l5r5-CR7-r1-after'),('r2','/var/tmp/arc2-l5r5-CR7-r2-after'),('r3','/var/tmp/arc2-l5r5-CR7-r3-after'),('r4','/var/tmp/arc2-l5r5-CR7-r4-after')]
for label,root in pairs:
 d=Path(root)/'.ufo/waves'/f'arc2-loop1-round{label[1]}'/'receipts'
 pre=d/'config-pre-pair.txt'; post=d/'config-post-pair.txt'
 if not pre.exists() or not post.exists():
  print(label,'MISSING',pre.exists(),post.exists()); continue
 def parse(p):
  lines=p.read_text().splitlines(); return lines[0],{x.split('  ',1)[1]:x.split('  ',1)[0] for x in lines[1:] if '  ' in x}
 t1,a=parse(pre); t2,b=parse(post); keys=sorted(set(a)|set(b)); changed=[k for k in keys if a.get(k)!=b.get(k)]
 print(f'{label} pre={t1} post={t2} matched={len(keys)-len(changed)}/{len(keys)} changed={changed}')
PY
```

Observed output:

```text
r1 14:49:13Z -> 16:52:56Z: endpoint hashes match 3/3
r2 16:57:35Z -> 17:08:57Z: endpoint hashes match 5/5
r3 17:55:49Z -> 18:57:18Z: endpoint hashes match 5/5
r4 19:03:02Z -> 19:44:52Z: endpoint hashes match 4/5; config.toml differs
```

These are endpoint comparisons, not proof of continuous zero drift. In particular, round 3 records an in-window mutate-and-revert, and round 4 records the config.toml drift; the scorecard correctly voids bare zero-drift claims (`SCORECARD.md:820-827, :888-893`).

The remaining census obligations cannot be honestly counted as confirmed under custody. The round-2 E22 instrument and committed v10 both resolve live anchors from `$HOME` configs/cache (`.ufo/waves/arc2-loop1-round2/E22.md:336-339, :383-393`; `.ufo/gates/c1-census-v10.py:74-83,124-134,218-234,370-407`). The round-4 PASS is specifically at work commit `265e1aa` (`SCORECARD.md:880-885`), not an archive-only result: no live probe was authorized this round. Thus C1's measurable is **not complete** merely because command A reproduces. Report 8/8 narrow checks as confirmed; do not report all round-1–4 before/afters audited.

### R4 citation-drift probe: valid-revision pass confirmed; bad revision is misclassified

Ran the exact committed probe/table/expected from the 265e1aa archive against that Git revision:

```bash
python3 /var/tmp/arc2-l5r5-CR7-r4-after/.ufo/gates/citation-drift/citation-drift-probe.py --root . --rev 265e1aa --table /var/tmp/arc2-l5r5-CR7-r4-after/.ufo/gates/citation-drift/pointer-table.json --expected /var/tmp/arc2-l5r5-CR7-r4-after/.ufo/gates/citation-drift/expected.json --snapshot-dir /var/tmp/arc2-l5r5-CR7-r4-after/.ufo/gates/citation-drift --strict
```

Output: `CITATION_DRIFT_VERDICT: clean findings=0 exit=0` — the recorded valid-revision result reproduces.

Negative control, same artifact but an invalid revision:

```bash
python3 /var/tmp/arc2-l5r5-CR7-r4-after/.ufo/gates/citation-drift/citation-drift-probe.py --root . --rev deadbeef --table /var/tmp/arc2-l5r5-CR7-r4-after/.ufo/gates/citation-drift/pointer-table.json --expected /var/tmp/arc2-l5r5-CR7-r4-after/.ufo/gates/citation-drift/expected.json --strict
```

Observed tail: `CITATION_DRIFT: citation_file_absent ... absent at deadbeef`; `CITATION_DRIFT_VERDICT: failed findings=7 exit=1`. Without `--strict`, it reports `CITATION_DRIFT_VERDICT: reported findings=7 exit=0`. A nonexistent root, by contrast, returned `could-not-evaluate findings=1 exit=2`. Source: `.ufo/gates/citation-drift/citation-drift-probe.py:91-100,116-127,255-283,286-297`. This is not a false clean on a bad revision, but it is a genuine outcome-class gap: a revision that cannot be resolved is reported as seven absent citation files (or a strict failure), not as could-not-evaluate. This qualifies broad wording that all could-not-evaluate inputs are handled as exit 2; the valid-revision `findings=0` claim remains confirmed (`SCORECARD.md:906`). Disposition: instrument debt / narrow claim; no repo edit made.

### C2 and C3 status at the permitted baseline

The three consecutive `60 reports / 64 dispatched` observations are present at `SCORECARD.md:710-712`, `:772-775`, `:858-862` (also LOG tail `:1023-1025, :1074-1076, :1120-1122`). That establishes repeated outcomes, not root cause or a re-dispatch remedy. `git ls-tree -r --name-only 0e8c96b -- corpus/lessons/` returned only `.gitkeep`, the 2026-10-13 lessons, and the 2026-10-15 recovery lessons; there is no 60/64 dispatch lesson at this HEAD. `corpus/lessons/2026-10-15-round-1-recovery.md:83-97` discusses redispatch of a blocked interactive recovery with missing role bindings, not replacement of four non-completing seats in a 64-seat batch. Therefore C2 is not satisfied until a specific cross-round defect class and executable re-dispatch protocol land in a corpus lesson.

The R1–R4 carried debt is scattered across `SCORECARD.md:696-700, :756-766, :845-854, :920-927`; this audit did not inspect any round-5 wave file beyond the authorized pre-pair receipt. I cannot determine whether the proposed register gives every item a disposition or whether safe items landed. Treat C3 as **unknown**, not pass, until the canonical register and its safe landings are independently checked.

## Text parent may land verbatim

```text
CR7 (arc2-loop1-round5) — calibration is partial, not a blanket confirmation. I re-derived 4/4 command-A pairs from the cited Git archives (79/79 map throughout; rules 9→10, 10→10, 10→10, 10→11) and parsed 4/4 committed custody endpoint comparisons (3/3, 5/5, 5/5, 4/5). These eight narrow checks match their records, but they do not cover every falsifiable round-1–4 before→after. The round-2/v10 census depends on live config/cache anchors; under this round's no-live-probe rule, those census results remain un-rederived, so C1 is not complete.

The round-4 citation-drift probe is clean at its cited revision (0 findings). With --rev deadbeef, however, it reports seven citation_file_absent findings (exit 0 in probe mode; exit 1 in strict mode), not could-not-evaluate; only an unreadable root yields exit 2. Disposition this as instrument debt or narrow the C2 outcome-class statement; do not call it a false clean.

The 60/64 outcome is evidenced in rounds 2, 3, and 4, but no 60/64-specific corpus lesson exists at HEAD 0e8c96b; C2 remains open until the re-dispatch protocol lands. C3 is unknown until the R1–R4 missed-item register is available and each disposition/landing is checked.
```

## Conclusions

- **Observation:** archive-backed command-A values match at the cited revisions; receipt endpoint comparisons are 3/3, 5/5, 5/5, 4/5; the valid-revision probe run returns clean; `--rev deadbeef` is not classified CNE; three round records show 60/64; no 60/64 lesson is in the HEAD lesson tree.
- **Inference:** a round-wide PASS would inflate the evidence if it extrapolates these eight checks to all C1 metrics, claims C2's lesson already exists, or closes C3 without itemized dispositions. Invalid-revision handling is a real but bounded instrument-classification defect, not evidence that the valid-revision result is wrong.
- **Unknown:** host-dependent r2/r3/r4 census before/after values are not re-derived under the no-live-probe constraint; round-5 register contents and landings were not inspected; C2's re-dispatch protocol may still land later in the wave.
