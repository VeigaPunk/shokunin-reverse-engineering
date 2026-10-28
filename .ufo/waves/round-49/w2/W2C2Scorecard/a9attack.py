import sys, re, json
sys.dont_write_bytecode = True
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/W2C2Scorecard')
import importlib.util
spec = importlib.util.spec_from_file_location('c2', '/fast/scratch/hyaku/kaidoku-r49/W2C2Scorecard/c2-mismatch.py')
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
ROOT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
g = c2.Git(ROOT)
sc = g.show(REV, 'SCORECARD.md').decode()
A9 = '- A9 verdict=rejected-harmed source=corpus/lessons/round-48-verifier-spotcheck.md calibration=harmed'
assert sc.count(A9) == 1
cases = {}
cases['base_landing'] = sc
cases['delete_A9'] = sc.replace(A9 + '\n', '')
cases['A9_calibration_improved'] = sc.replace(A9, A9.replace('calibration=harmed', 'calibration=improved'))
cases['A9_verdict_admitted'] = sc.replace(A9, A9.replace('verdict=rejected-harmed', 'verdict=admitted'))
cases['A9_trailing_text'] = sc.replace(A9, A9 + ' (see lesson)')
cases['A9_in_html_comment'] = sc.replace(A9, '<!--\n' + A9 + '\n-->')
cases['A9_in_code_fence'] = sc.replace(A9, '```\n' + A9 + '\n```')
cases['A9_moved_to_round48_section'] = sc.replace(A9 + '\n', '').replace('## Owned axes', A9 + '\n\n## Owned axes')
cases['duplicate_correction_heading'] = sc.replace('## Owned axes', '## Record corrections \u2014 round 49 (draft)\n\n' + A9 + '\n\n## Owned axes')
cases['A9_nbsp_dash'] = sc.replace(A9, A9.replace('- A9 ', '-\u00a0A9 '))
out = {}
for name, txt in cases.items():
    over = {'SCORECARD.md': txt.encode()}
    got = c2.score(c2.Overlay(g, REV, over), REV)
    out[name] = {'red': sorted(k for k, v in got.items() if v), 'A9_why': got['A9']}
print(json.dumps(out, indent=1, ensure_ascii=False))
