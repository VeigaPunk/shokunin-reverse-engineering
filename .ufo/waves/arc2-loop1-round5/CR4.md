# CR4 — Does historical re-derivation test calibration?

**Verdict: PREMISE REFUTED AS NAMED — re-running measurements at cited commits tests operability/reproducibility, not calibration by itself.** Calibration is tested only when the rerun is checked against independent, historically pinned truth inputs (for example, the cited receipt contents), not merely against a rerun of the same measurement logic.

## Evidence

### Immutable-tree rerun

I re-ran command A from `SCORECARD.md:92-123` against the named commit objects. It reads each commit via `git show` / `git ls-tree`, not the moving worktree. Commands used the Python heredoc at `SCORECARD.md:93-123`, with `REV` as its argument, for these pairs:

```bash
python3 - "$REV" <<'PY'
import json, pathlib, re, subprocess, sys
rev = sys.argv[1]
def get(path):
    return subprocess.check_output(['git', 'show', f'{rev}:{path}'], text=True)
paths = subprocess.check_output(['git', 'ls-tree', '-r', '--name-only', rev,
                                 '--', 'corpus/knowledge'], text=True).splitlines()
files = {pathlib.PurePosixPath(p).stem for p in paths if p.endswith('.md')}
section = get('corpus/README.md').split('## Coverage map\n', 1)[1].split('\n## ', 1)[0]
mapped = set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', section))
craft = get('SKILL.md').split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0]
rules = re.split(r'(?m)^- \*\*', craft)[1:]
pattern = r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?'
resolved = 0
for rule in rules:
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(get('corpus/knowledge/' + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError:
            valid = False
    resolved += valid
print(json.dumps({'revision': rev, 'mapped': len(files & mapped),
 'knowledge_files': len(files), 'missing': sorted(files - mapped),
 'dangling': sorted(mapped - files), 'citation_resolved_rules': resolved,
 'rule_blocks': len(rules), 'coverage_score': round(10*len(files & mapped)/len(files), 2),
 'depth_score': round(10*resolved/len(rules), 2)}, sort_keys=True))
PY
```

I invoked that heredoc with `REV` set to `4b806e1`, `df31bfb`, `165057e`, `b21c0da`, `679af5d`, `dbba2dd`, `158a966`, and `265e1aa` (four pair batches).

Observed stdout excerpts (one JSON object per revision):

```text
4b806e1: 79/79 mapped, 9 rules, 9 resolved, coverage=10.0, depth=10.0
 df31bfb: 79/79 mapped, 10 rules, 10 resolved, coverage=10.0, depth=10.0
165057e: 79/79 mapped, 10 rules, 10 resolved, coverage=10.0, depth=10.0
 b21c0da: 79/79 mapped, 10 rules, 10 resolved, coverage=10.0, depth=10.0
679af5d: 79/79 mapped, 10 rules, 10 resolved, coverage=10.0, depth=10.0
 dbba2dd: 79/79 mapped, 10 rules, 10 resolved, coverage=10.0, depth=10.0
158a966: 79/79 mapped, 10 rules, 10 resolved, coverage=10.0, depth=10.0
265e1aa: 79/79 mapped, 11 rules, 11 resolved, coverage=10.0, depth=10.0
```

These reproduce the reported source-derived counts (e.g. `.ufo/reports/arc2-loop1-round1/kaidoku.md:129-140`; `.ufo/reports/arc2-loop1-round4/kaidoku.md:69-70`). They are valid rerun checks for coverage/depth. They do not independently establish that a factual statement about an external/live system was true.

### Why replay is not calibration

- The scorecard defines calibration as reconciliation to live receipts and explicitly limits the proxy to failure-selected completeness, not unbiased accuracy: `SCORECARD.md:21-25`. Command A instead counts map entries, source files, and citation-resolved rule blocks: `SCORECARD.md:88-123`.
- Round 2's calibration claim says its C1 census used anchors “re-derived live each run” and was “measured at the work tree,” with the executable named under `/tmp`: `.ufo/reports/arc2-loop1-round2/kaidoku.md:71-76`. The archived round-2 instrument code reads `CLIENTS` paths on the current host (`.ufo/waves/arc2-loop1-round2/E22.md:383-393`) and scans the current `~/.npm/_npx` cache (`:477-493`). It does not take historical client-config/cache inputs from the cited commit. Thus an archive-root replay combines historical repo text with present host state.
- The committed v10 instrument has the same boundary: `HOME`-derived client paths are fixed at `.ufo/gates/c1-census-v10.py:74-83`; `live_pins()` reads those current paths at `:124-135`; `cache_versions()` reads the present npx cache at `:218-234`. Its `--root` selects repo text only (`:370-386`). A successful replay therefore establishes that this version of the tool can run on that tree/environment, not that the historical external truth was reproduced.
- Round 4 reports its census as “at the work tree” and distinguishes v10 from v9's undeclared-count failure: `.ufo/reports/arc2-loop1-round4/kaidoku.md:75-78`. Replaying v10 at its cited commit is useful for repeatability; comparing its result to committed receipt bytes is the additional calibration check.

## Conclusions

- **Observation:** The command-A reruns above reproduce the cited source-derived values from the exact historical Git objects. The recipe is deterministic source measurement, not semantic truth measurement (`SCORECARD.md:88-123`).
- **Observation:** The R2/R4 C1 instruments obtain some comparison inputs from the current host, not the archived repo tree (`E22.md:383-393,477-493`; `c1-census-v10.py:74-83,124-135,218-234`).
- **Inference:** As written, “re-derive every measurement at its cited commit” primarily tests **operability / historical-measurement reproducibility**. It tests calibration only for the subset where the original truth inputs are independently pinned and the rerun is compared against them. A matching program output alone is not an independent truth check.
- **Unknown:** This seat did not replay every round-specific census, receipt comparison, or custody measurement; the outputs above are the direct source-metric reruns relevant to the premise, not a completion of the fleet's full C1 audit.

## Suggested text to land verbatim

```text
C1 — historical-measurement reproducibility (operability): rerun each versioned measurement against its cited commit tree and compare the output to the recorded before→after value; disposition mismatches. This establishes repeatability, not calibration by itself. Count a result as calibration only when the rerun also checks against independent, historically pinned truth inputs (such as the cited receipt contents), rather than current host state or the same claim being measured.
```
