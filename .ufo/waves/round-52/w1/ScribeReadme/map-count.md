# R52-C1 — the coverage-map count arithmetic the `SCORECARD.md` head must carry

Seat `ScribeReadme`, kaidoku round 52 wave 1 (build). Draft only.

## The number

| quantity | value | how measured |
|---|---|---|
| knowledge `.md` files at the round-start base `c525de54a53eb3c4fee28ede2721da4527cf8ece` | **141** | `git ls-tree -r --name-only <rev> -- corpus/knowledge` → 142 entries, 141 of them `.md` (the 142nd is `corpus/knowledge/.gitkeep`) |
| of those, mapped in `corpus/README.md` `## Coverage map` at the base | **141** | command A below: `mapped: 141`, `missing: []`, `dangling: []` |
| after the round-52 entry lands (`corpus/knowledge/2026-10-30-r52-avm-le-squashfs-core.md`) | **142** | 141 + 1 |
| therefore the `SCORECARD.md` `## Owned axes` coverage row must read | **`142/142 knowledge files mapped`** | atom **B1** (`tools/round-50/c2-record.py:496-517`) derives the number from `git ls-tree -r --name-only <rev> -- corpus/knowledge` and requires the row to state `N/N` with the *same* N |

**Arithmetic: 141 → 142 with this entry.** The current `SCORECARD.md` coverage head says
"Round-51 index integrity: 141/141 knowledge files mapped" (measured at `SCORECARD.md:23`); after the
round-52 entry lands the head must read **142/142**.

**The map's 142nd file is this entry** — the round-52 entry is the 142nd `.md` file of
`corpus/knowledge/` (sorted, it sorts last: `2026-10-30-r52-avm-le-squashfs-core.md` follows
`2026-10-30-r51-avm-le-squashfs-core.md`).

## The counting command (claims' command A semantics)

This is the `SCORECARD.md` "Measurement recipes → A — source-derived controls" block, run from the
lane repo with `REV` set to the landing revision. It reads immutable git objects, never the moving
worktree.

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

**Semantics that the arithmetic depends on** (measured, not inferred):

* `knowledge_files` = the **`.md` stems** under `corpus/knowledge/` at `REV`
  (`git ls-tree -r --name-only REV -- corpus/knowledge`, `.md` filter; `corpus/knowledge/.gitkeep`
  is not counted);
* `mapped` = the set of tokens matching `2026-10-\d{2}-[a-z0-9-]+` found **inside the
  `## Coverage map` section only** — the section runs from the literal `## Coverage map\n` to the
  next `\n## `, so the `## Knowledge` table and the `## Frontier` section are **not** counted;
* `missing` = files with no token in the coverage-map section, `dangling` = tokens with no file;
* `coverage_score` = `round(10 * mapped / knowledge_files, 2)` → **10.0** at 142/142 (the numeric
  coverage score does not move; the head's *count* moves 141 → 142).

## Measured runs

| run | rev | result |
|---|---|---|
| command A at the round-start base | `c525de54a53eb3c4fee28ede2721da4527cf8ece` | `knowledge_files: 141`, `mapped: 141`, `missing: []`, `dangling: []`, `coverage_score: 10.0`, `citation_resolved_rules: 26`, `rule_blocks: 26`, `depth_score: 10.0` |
| command A at the claims draft | `ab0eafedc41402b43b41a4362084119578dfe7ce` | identical README blob (`b8a266ea…`), so identical counts |
| patched-clone simulation (base + the new coverage row + the new entry file) | scratch clone of the base | `knowledge_files: 142`, `mapped: 142`, `missing: []`, `dangling: []`, `coverage_score: 10.0` — see `receipts/check.log` and `receipts/README.patched.md` |

## The two failure modes this binding must catch (and why the row placement matters)

1. **Entry lands, row does not** → `mapped: 141`, `knowledge_files: 142`, `missing:
   ['2026-10-30-r52-avm-le-squashfs-core']`, `coverage_score: 9.93`; atom **B1** fails
   ("knowledge files not mapped in README Coverage map"). The coverage row and the entry must land in
   the **same commit**.
2. **Row lands, entry does not** → `dangling: ['2026-10-30-r52-avm-le-squashfs-core']` — a token in
   the coverage map with no file. Same-commit landing prevents this too.

## Cross-seat dependencies (flagged, not owned)

* `ScribeScorecard` owns the `SCORECARD.md` head edit: the coverage row must read
  **142/142 knowledge files mapped** and the row's own wording must carry the literal
  `(\d+)/(\d+) knowledge files mapped` phrase, because atom B1 parses exactly that shape
  (`tools/round-50/c2-record.py:503-508`).
* `ScribeEntryC1` owns the entry file: its stem must be exactly
  `2026-10-30-r52-avm-le-squashfs-core` (the claims' constant) so the coverage row's token matches
  the file stem.
* `ScribeSources` owns the `S252` SOURCES row: the count arithmetic above is independent of it, but
  the *citation* in the coverage/Knowledge rows is not — see `coverage-map-row.md` §3.
