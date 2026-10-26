# R36W2ExecCommandA — command A at base, C1 landing and tip

Seat: `R36W2ExecCommandA`, leaf, round 36 wave 2. Task: run the lane's `SCORECARD.md`
`## Measurement recipes` **recipe A** (python heredoc over immutable git objects) at
`cab59f221fe19726b5692bfa4d9a9679e96b8a73`, `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95` and
`01a44dbf45913a1bdcabbbfb85b7bb9d232cb930`; compare with the stated owned-axes numbers
(coverage 124/124, depth 17/17) and with the knowledge-file count of **every**
`corpus/knowledge/*.md` (not only date-prefixed stems); report any knowledge file outside
command A's stem pattern.

Lane HEAD when measured: `01a44dbf45913a1bdcabbbfb85b7bb9d232cb930` (2026-10-26T05:01Z), worktree
clean apart from pre-existing untracked `.ufo/waves/round-36/w2*` artefacts. No VCS mutation, no
lane write except this report. No tool installed or upgraded (nothing was needed).

## 1. Command run (recipe A, verbatim from `SCORECARD.md:86-124`)

```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
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

## 2. Output at the three assigned revisions (exit 0 each)

```
=== cab59f221fe19726b5692bfa4d9a9679e96b8a73
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 122, "mapped": 122, "missing": [], "revision": "cab59f221fe19726b5692bfa4d9a9679e96b8a73", "rule_blocks": 17}
=== ffc813417d3bceeeb7b028b12ce0be8a5dc33d95
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 124, "mapped": 124, "missing": [], "revision": "ffc813417d3bceeeb7b028b12ce0be8a5dc33d95", "rule_blocks": 17}
=== 01a44dbf45913a1bdcabbbfb85b7bb9d232cb930
{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 124, "mapped": 124, "missing": [], "revision": "01a44dbf45913a1bdcabbbfb85b7bb9d232cb930", "rule_blocks": 17}
```

Re-run of the tip invocation with exit code captured: `exit=0`,
`{"citation_resolved_rules": 17, "coverage_score": 10.0, "dangling": [], "depth_score": 10.0, "knowledge_files": 124, "mapped": 124, "missing": [], "revision": "01a44dbf45913a1bdcabbbfb85b7bb9d232cb930", "rule_blocks": 17}`.

## 3. Comparison with the stated owned-axes numbers — all reproduce, no disagreement

| Statement (source at tip) | Command A observation | Verdict |
|---|---|---|
| coverage `SCORECARD.md:23` "124/124 knowledge files mapped after the round-36 landing" | `mapped 124 / knowledge_files 124`, `missing []`, `dangling []`, `coverage_score 10.0` at `ffc81341` **and** `01a44dbf` | **matches** |
| coverage `SCORECARD.md:23` "122/122 at `cab59f221…`" | 122/122, `missing []` at base | **matches** |
| coverage `SCORECARD.md:23` "two entries added" | `git diff --stat cab59f22..ffc81341 -- corpus/knowledge` → exactly `2026-10-26-r36-sasquatch-squashfs-recursion.md` (215+) and `2026-10-26-unblob-sasquatch-dependency.md` (41+), `2 files changed, 256 insertions(+)`; nothing else added, nothing removed (`ffc81341..01a44dbf` touches no knowledge file except a 6-line append to the existing `2026-10-25-r34b-…`) | **matches** |
| coverage history "116/116 at `c369242f…` (round 31)" | at `c369242fee9f559f895e3f7956b1242076c7b1be`: `mapped 116`, `knowledge_files 116` | **matches** |
| coverage history "109/109 at `ebe2cb4a`" | at `ebe2cb4aff1aea6f45e8bb5583662717ea61c0bb`: 109/109 | **matches** |
| coverage history "108/108 after the round-25 entry" | at `08c7a7299ed61c3fdc30ddb0adfe4e812d5eac76` (commit that added `2026-10-22-r25-evm-selector-name-resolution.md`): 108/108 | **matches** |
| coverage history "107/107 at `7ef837a4…`" | 107/107 | **matches** |
| coverage history "78/78 at `3395b6d` (luna-round-7)" | 78/78, `rule_blocks 9` (pre-growth) | **matches** |
| depth `SCORECARD.md:24` "17/17 queue-drain rule blocks have resolvable file/range citations at `c369242f…`" | at `c369242f`: `citation_resolved_rules 17`, `rule_blocks 17`; same 17/17 at base, `ffc81341` and tip | **matches** |
| depth row craft range "`SKILL.md:81-314` (heading line 81, last non-blank line 314)" | observed heading line 81, next `## ` heading line 319, last non-blank line of the section 314 — identical at `c369242f` and at tip (`SKILL.md` grew 1005 → 1297 lines below the section) | **matches** |
| round-36 section "finite map proxy 122/122 → 124/124, two entries added and mapped" | 122/122 → 124/124 | **matches** |

Depth did not move this round and is not claimed to; 17/17 is a carry (the round-36 section says
"17/17 unchanged"), consistent with `rule_blocks 17` at base and tip.

## 4. Denominator: every `corpus/knowledge/*.md`, not only date-prefixed stems

Command A's `files` is built from **all** `.md` paths under `corpus/knowledge`
(`endswith('.md')`, `PurePosixPath(...).stem`) — the stem is not filtered for a date before being
counted, so the denominator is every `.md` file and a non-date stem can only surface as `missing`.

Independent enumeration at tip (`git ls-tree -r --name-only 01a44dbf -- corpus/knowledge`):

- 125 tracked paths, of which **124 are `.md`** and one is `corpus/knowledge/.gitkeep` (correctly
  excluded by the `endswith('.md')` filter — no file is hidden by that filter).
- **No nested directories**: every `.md` is a direct child of `corpus/knowledge` (124 paths,
  124 matching `corpus/knowledge/[^/]*$`).
- **No duplicate stems** (`… | sed 's|.*/||; s|\.md$||' | sort | uniq -d` → empty).
- **Every stem matches `^2026-10-[0-9]{2}-[a-z0-9-]+$`** — `grep -Ev` returns zero lines at
  `cab59f22` (122 files), `ffc81341` (124) and `01a44dbf` (124). **No knowledge file lies outside
  command A's stem pattern**, so command A's denominator equals the true knowledge-file population
  at all three revisions, and `knowledge_files` (124) equals the on-disk count (124) exactly.
- Worktree at tip: `ls corpus/knowledge | grep -c '\.md$'` → 124; only `.gitkeep` is non-`.md`.

## 5. Duplicate map tokens (occurrence count > distinct count) — no effect on the verdict

The coverage-map section holds **128 token occurrences** for **124 distinct stems** at `ffc81341`
and tip (126 occurrences / 122 distinct at base). The four extra occurrences:

| stem | occurrences (section line within `## Coverage map`, cell index) |
|---|---|
| `2026-10-18-arc2-r7-pe-wall` | line 11, cell 0 (section cell) + line 11, cell 1 twice (state-cell citations `:13-19`, `:23-37`) |
| `2026-10-19-arc3-r7-evm-evidence-id-domain` | line 27 cell 1 (EVM row) + line 30 cell 1 (Evidence model row) |
| `2026-10-19-arc3-r10-rust-evidence-id-domain` | line 30 cell 1 + line 52 cell 0 (`knowledge/…` row) |

The metric is set-based (`len(files & mapped)`), so duplicates cannot inflate or deflate it; they
are recorded because QUALITY 77 warns that first-match/occurrence-blind matching hides duplicates.

## 6. Stricter non-counter re-derivation of the same 124/124 (by row, not by token presence)

Command A counts a stem **anywhere** in the coverage-map section, including the prose/state
column. I re-derived the mapping with a stricter rule — a stem counts only if it appears in the
row's section cell (0) or entries cell (1):

| revision | `.md` files | distinct tokens | tokens reachable only via prose cells |
|---|---|---|---|
| `cab59f22` | 122 | 122 | **none** |
| `ffc81341` | 124 | 124 | **none** |
| `01a44dbf` | 124 | 124 | **none** |

So the tip's 124/124 survives the stricter reading: every one of the 124 files is named in a
mapping cell of the table, not merely mentioned in a state note.

## 7. Detector-failure and blind-spot probes (scratch fixtures, not lane bytes)

Fixture repo `$S/fx` = `git clone --depth 1 file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin`
under `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ExecCommandA`; `git -C "$S/fx" rev-parse
--show-toplevel` = `$S/fx` before the first fixture commit; every mutation committed in the
fixture; scratch removed on exit. Command A was run at each fixture `HEAD` with the verbatim
recipe.

| # | fixture mutation | command A output | reading |
|---|---|---|---|
| fx1 | add `corpus/knowledge/notes.md` (non-date stem) | `knowledge_files 125, mapped 124, missing ["notes"], coverage_score 9.92` | the denominator counts non-date `.md` files and the mapping fails loudly — the observable is **not** stem-pattern-blind |
| fx2 | add `corpus/knowledge/2026-10-26-unmapped-entry.md` | `125 / 124`, `missing ["2026-10-26-unmapped-entry"]`, `9.92` | an unmapped date-prefixed entry fails |
| fx3 | copy `2026-10-13-asar-surface.md` to `corpus/knowledge/sub/2026-10-13-asar-surface.md` (125 `.md` on disk) | `knowledge_files 124, mapped 124, missing [], coverage_score 10.0` | **blind spot (latent)**: stems are a `set`, so a duplicate stem in a nested directory is collapsed and 125 files score 124/124. Not active — the lane has no nested directory and no duplicate stem (§4) |
| fx4 | move `2026-10-13-ghidra-install` from the Provider-readiness entries cell into the state cell prose | `124 / 124`, `missing []`, `10.0`; stricter cell check reports `['2026-10-13-ghidra-install']` as prose-only | **blind spot (latent)**: token presence anywhere in the section counts as mapped. Not active — §6 shows zero prose-only stems at all three revisions |
| fx5 | append `- **bad-ref probe.**` citing `…r36-sasquatch-squashfs-recursion.md:9999` and `- **no-ref probe.**` citing nothing | `rule_blocks 19, citation_resolved_rules 17, depth_score 8.95` | depth detector rejects both an out-of-range range and a ref-less block (score falls below 10) |
| fx6 | add `corpus/knowledge/2026-11-02-nov-entry.md` **and** a coverage-map row naming it | `knowledge_files 125, mapped 124, missing ["2026-11-02-nov-entry"]`, `9.92` | the `mapped` regex is month-pinned (`2026-10-\d{2}`), so any entry dated outside October 2026 can never be mapped. Brittle **loudly** (coverage drops), never a silent pass; no such file exists at the measured revisions |

## 8. Agreement with the round-36 recount instrument the coverage row cites

`SCORECARD.md:23` says the round-36 count was taken "with the command-A observable in
`tools/round-36/c2-counter.py`". `tools/round-36/c2-counter.py:118-140` (`command_a`) implements
the same algorithm as recipe A: same `git ls-tree -r --name-only <rev> -- corpus/knowledge`
population, same `2026-10-\d{2}-[a-z0-9-]+` token set, same `## Queue-drain craft ` split and
`^- \*\*` rule split, same citation regex and `1 <= start <= end <= count` test. The only
difference is stem extraction (`os.path.splitext(os.path.basename(x))[0]` vs
`PurePosixPath(...).stem`), which is identical for a flat directory and equally collapses nested
duplicate stems — so the counter's O1 cannot disagree with recipe A on this tree.

## 9. Findings

- **No disagreement with any stated owned-axes number.** Coverage 124/124 and depth 17/17 reproduce
  at `ffc81341` and `01a44dbf`; base is 122/122; every historical figure in the coverage row
  (116, 109, 108, 107, 78) and the depth row's `SKILL.md:81-314` range reproduce exactly.
- **No knowledge file outside command A's stem pattern** at any of the three revisions; the
  denominator is the complete `.md` population (124), with `.gitkeep` the only excluded path.
- Limitations of the frozen observable, **all latent at the tip and none changing the verdict**:
  duplicate-stem collapse (fx3), prose-cell token counting (fx4), month-pinned date regex (fx6),
  and the set-based counting that hides the four duplicate token occurrences (§5). These are
  properties of recipe A / `c2-counter.command_a`, not of the round-36 work; fixing them is a
  round-37 instrument decision (the QUALITY 77/78 successor), not this wave.
- [INFERENCE] The 10.0 `coverage_score`/`depth_score` are saturated finite proxies; a pass here
  demonstrates index integrity only, as the coverage row itself states.

## 10. Evidence inventory (all reproduced in this report; no /tmp or scratch paths cited)

- Recipe A outputs: §2 (three revisions) and §3 (seven historical revisions).
- File-population enumeration: §4 (ls-tree counts, stem-pattern `grep -Ev`, duplicate-stem
  `uniq -d`, on-disk count).
- Stricter mapping re-derivation: §6.
- Fixture probe matrix: §7 (six fixtures, each with the command-A JSON line it produced).
- Instrument equivalence: §8 (`tools/round-36/c2-counter.py:118-140`).

Scratch `S=/fast/scratch/hyaku/kaidoku-r36/R36W2ExecCommandA` removed (`rm -rf`; `ls -d` → absent).
Lane HEAD unchanged at `01a44dbf…`; `git status --porcelain` shows no tracked modification.
