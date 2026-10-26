#!/usr/bin/env python3
"""R40 wave-2 seat R40W2DepthCount: run round-38 command_a (SCORECARD command A)
at N revisions, plus a faithful detail pass (per-rule citations, missing/dangling).

command_a is imported verbatim from tools/round-38/c2-counter.py (no copy) so the
numbers are the counter's own. The detail pass re-implements the same split rules
and adds the lists command_a only aggregates.
"""
import importlib.util, json, os, re, subprocess, sys

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
C38 = os.path.join(LANE, 'tools/round-38/c2-counter.py')

spec = importlib.util.spec_from_file_location('c2r38', C38)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

STEM = re.compile(r'2026-10-\d{2}-[a-z0-9-]+')
REF = re.compile(r'corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?')


def show(rev, path):
    p = subprocess.run(['git', '-C', LANE, 'show', f'{rev}:{path}'], capture_output=True)
    return p.stdout.decode() if p.returncode == 0 else None


def detail(rev):
    p = subprocess.run(['git', '-C', LANE, 'ls-tree', '-r', '--name-only', rev, '--', 'corpus/knowledge'],
                       capture_output=True, text=True)
    files = {os.path.splitext(os.path.basename(x))[0] for x in p.stdout.splitlines() if x.endswith('.md')}
    readme = show(rev, 'corpus/README.md') or ''
    has_cov = '## Coverage map\n' in readme
    sec = readme.split('## Coverage map\n', 1)[1].split('\n## ', 1)[0] if has_cov else ''
    mapped = set(STEM.findall(sec))
    skill = show(rev, 'SKILL.md') or ''
    has_craft = '## Queue-drain craft ' in skill
    craft = skill.split('## Queue-drain craft ', 1)[1].split('\n## ', 1)[0] if has_craft else ''
    blocks = re.split(r'(?m)^- \*\*', craft)[1:]
    rules = []
    for i, rule in enumerate(blocks, 1):
        title = rule.splitlines()[0].strip().rstrip('*').strip() if rule.splitlines() else ''
        refs = REF.findall(rule)
        good, bad = [], []
        for name, f, l in refs:
            t = show(rev, 'corpus/knowledge/' + name)
            if t is None:
                bad.append({'ref': 'corpus/knowledge/' + name, 'why': 'missing-file'})
                continue
            n = len(t.splitlines())
            s, e = int(f or 1), int(l or f or 1)
            if 1 <= s <= e <= n:
                good.append({'ref': f'corpus/knowledge/{name}:{s}-{e}', 'lines': n})
            else:
                bad.append({'ref': f'corpus/knowledge/{name}:{s}-{e}', 'why': f'range-outside({n})'})
        # other backticked tokens in the block that look like lane paths but are not corpus/knowledge refs
        others = sorted({t for t in re.findall(r'`([^`\s]+)`', rule)
                         if '/' in t and 'corpus/knowledge/' not in t and not t.startswith(('/', '~'))})[:6]
        rules.append({'n': i, 'title': title, 'refs': len(refs), 'resolved_refs': len(good),
                      'dangling': bad, 'resolved_rule': bool(refs) and not bad,
                      'zero_citation': not refs, 'other_tokens': others})
    return {
        'revision': rev,
        'knowledge_files': len(files),
        'coverage_map': {'section_present': has_cov, 'mapped': len(files & mapped),
                         'stems_in_map': len(mapped),
                         'missing': sorted(files - mapped),
                         'dangling': sorted(mapped - files)},
        'craft': {'section_present': has_craft, 'rule_blocks': len(blocks),
                  'resolved_rules': sum(1 for r in rules if r['resolved_rule']),
                  'zero_citation_rules': [r['n'] for r in rules if r['zero_citation']],
                  'unresolved_refs': [{'rule': r['n'], 'title': r['title'], **d} for r in rules for d in r['dangling']],
                  'rules': rules},
    }


def main():
    revs = sys.argv[1:]
    out = {'argv': ['depthcount.py'] + revs, 'lane': LANE, 'command_a_source': C38, 'revisions': {}}
    for rev in revs:
        a = mod.command_a(LANE, rev)
        d = detail(rev)
        out['revisions'][rev] = {'command_a': a, 'detail': d}
        print(json.dumps({'rev': rev[:8], 'command_a': a,
                          'mapped': d['coverage_map']['mapped'], 'total': d['knowledge_files'],
                          'missing_map': len(d['coverage_map']['missing']),
                          'dangling_map': len(d['coverage_map']['dangling']),
                          'zero_citation_rules': len(d['craft']['zero_citation_rules']),
                          'unresolved_refs': len(d['craft']['unresolved_refs'])}, sort_keys=True))
    json.dump(out, open(os.environ['OUT'], 'w'), indent=1, sort_keys=True)
    return 0


if __name__ == '__main__':
    sys.exit(main())
