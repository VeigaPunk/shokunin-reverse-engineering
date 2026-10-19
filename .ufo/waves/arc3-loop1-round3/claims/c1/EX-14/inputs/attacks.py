#!/usr/bin/env python3
"""EX-14 attack battery for the arc3-loop1-round3 C1 projection.

Each attack builds a state in the /var/tmp/ex14-scratch clone, commits, and runs
command A verbatim. Expected outcomes are pre-registered in the dict; a mismatch
is printed as SURPRISE.

A1 token-only (no entry file)        -> dangling [stem], files 82
A2 entry-only (no token)             -> missing [stem], files 83, mapped 82
A3 stem mismatch token (entry ok)    -> missing [stem] AND dangling [wrong]
A4 row-insert form (191 lines)       -> command A still 83/83 (count blind);
                                        line-neutrality False (the harm the
                                        count cannot see)
"""
import json, pathlib, subprocess, sys

sys.path.insert(0, '/var/tmp/ex14')
import project  # noqa: E402

CLONE = project.CLONE
BASE = project.BASE
STEM = '2026-10-19-arc3-r3-evm-optimizer-shapes'
ENTRY = pathlib.Path('/var/tmp/ex14/entry-rev2.md')
NEWLINE = pathlib.Path('/var/tmp/ex14/new-line-primary.txt').read_text()

results = {}


def reset():
    project.git('reset', '--hard', BASE, '--quiet')
    project.git('clean', '-fdx', '--quiet')


def put_entry(stem=STEM):
    (CLONE / ('corpus/knowledge/' + stem + '.md')).write_text(ENTRY.read_text())


def put_line(new_line):
    p = CLONE / 'corpus/README.md'
    lines = p.read_text().splitlines(keepends=True)
    lines[37] = new_line if new_line.endswith('\n') else new_line + '\n'
    p.write_text(''.join(lines))


def commit(label):
    project.git('add', '-A')
    project.git('commit', '--quiet', '-m', f'attack {label} (scratch clone)')
    return project.git('rev-parse', 'HEAD').stdout.strip()


def inspect(label, rev):
    ca = project.command_a(rev)
    readme = (CLONE / 'corpus/README.md').read_text().splitlines(keepends=True)
    results[label] = {'command_a': ca, 'readme_lines': len(readme)}
    return results[label]


# A1 — token only
reset()
put_line(NEWLINE)
rev = commit('a1-token-only')
inspect('A1_token_only', rev)
assert results['A1_token_only']['command_a']['dangling'] == [STEM], results['A1_token_only']
assert results['A1_token_only']['command_a']['knowledge_files'] == 82

# A2 — entry only
reset()
put_entry()
rev = commit('a2-entry-only')
inspect('A2_entry_only', rev)
assert results['A2_entry_only']['command_a']['missing'] == [STEM], results['A2_entry_only']
assert results['A2_entry_only']['command_a']['mapped'] == 82

# A3 — stem mismatch
reset()
put_entry()
wrong = NEWLINE.replace(STEM, '2026-10-19-arc3-r3-evm-optimizer-shape')
assert wrong != NEWLINE
put_line(wrong)
rev = commit('a3-stem-mismatch')
inspect('A3_stem_mismatch', rev)
assert results['A3_stem_mismatch']['command_a']['missing'] == [STEM]
assert results['A3_stem_mismatch']['command_a']['dangling'] == ['2026-10-19-arc3-r3-evm-optimizer-shape']

# A4 — row insert instead of same-line edit
reset()
put_entry()
p = CLONE / 'corpus/README.md'
lines = p.read_text().splitlines(keepends=True)
lines.insert(38, '| EVM (r3 sub-leg) | `' + STEM + '` | held — row-insert attack form |\n')
p.write_text(''.join(lines))
rev = commit('a4-row-insert')
inspect('A4_row_insert', rev)
a4 = results['A4_row_insert']
a4['line_neutral_vs_base'] = a4['readme_lines'] == 190
a4['note'] = ('command A count is blind to the row insert; the line-count '
              'change (191) is what same-line discipline prevents — the r1 '
              'EX-13 measurement additionally showed probe findings on a row '
              'insert (5 citation_dead), not re-run here.')

print(json.dumps(results, indent=1, sort_keys=True))
ok = (results['A1_token_only']['command_a']['dangling'] == [STEM]
      and results['A2_entry_only']['command_a']['missing'] == [STEM]
      and results['A3_stem_mismatch']['command_a']['missing'] == [STEM]
      and results['A3_stem_mismatch']['command_a']['dangling'] != []
      and results['A4_row_insert']['line_neutral_vs_base'] is False)
print('ATTACKS_AS_PREREGISTERED:', ok)
sys.exit(0 if ok else 1)