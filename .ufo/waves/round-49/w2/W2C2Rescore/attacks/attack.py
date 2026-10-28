import sys, importlib.util, json
D = '/fast/scratch/hyaku/kaidoku-r49/W2C2Rescore/clone.m6J4'
R = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
F = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('c2', D + '/tools/round-49/c2-mismatch.py')
c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
g = c2.Git(D)
def sha(b): return c2.sha(b)
def t(p): return c2.text(g.show(R, p))
def run(label, over, expect):
    o = c2.Overlay(g, R, over)
    got = c2.score(o, R)
    red = sorted(k for k, v in got.items() if v)
    verdict = 'RED' if red else 'GREEN'
    print(json.dumps({'label': label, 'expect': expect, 'red': red, 'verdict': verdict,
                      'why': {k: v for k, v in got.items() if v}}, ensure_ascii=False))
    return red
sx = t('corpus/SOURCES.md')
base_sec = 'corpus/SOURCES.md'
# baseline: genuine REV
run('genuine REV', {}, 'green')
# X1 A7: second EX_USAGE status without the word "is"
s148 = [l for l in sx.split('\n') if l.startswith('| S148 |')][0]
x1 = s148.replace('defines EX_USAGE is 64 (a command used incorrectly)', 'defines EX_USAGE is 64 (a command used incorrectly); an older mirror prints EX_USAGE=2', 1)
assert x1 != s148
run('X1 A7 teaches adds EX_USAGE=2 (no "is")', {base_sec: sx.replace(s148, x1, 1).encode()}, 'red A7 (plan: no other status)')
x1b = s148.replace('defines EX_USAGE is 64 (a command used incorrectly)', 'defines EX_USAGE is 64 (a command used incorrectly); EX_USAGE was 2 in 1994', 1)
run('X1b A7 teaches adds "EX_USAGE was 2"', {base_sec: sx.replace(s148, x1b, 1).encode()}, 'red A7')
# X2 A8: unmarked second round-48 entry
lines = sx.split('\n')
i48 = [i for i, l in enumerate(lines) if l.startswith('- 2026-10-28 round 48 (late entry')][0]
dup48 = '- 2026-10-28 round 48 — Question: duplicate round-48 entry without the late marker. Where searched: none. Identified 2, screened 2, included 1, excluded 1; rows 144 → 146. Exclusion: S146. Stop: duplicate.'
l2 = lines[:i48+1] + [dup48] + lines[i48+1:]
run('X2 A8 unmarked duplicate round-48 entry', {base_sec: '\n'.join(l2).encode()}, 'red A8 (plan: exactly one round-48 entry)')
# X3 A8: duplicate round-49 entry (same date/tag)
i49 = [i for i, l in enumerate(lines) if l.startswith('- 2026-10-28 round 49 ')][0]
dup49 = lines[i49] + ' (copy)'
l3 = lines[:i49+1] + [dup49] + lines[i49+1:]
run('X3 A8 duplicate round-49 entry', {base_sec: '\n'.join(l3).encode()}, 'red A8')
# X4 A8: inflated identified count (asserted by lane, disclosed)
e49 = lines[i49]
x4 = e49.replace('Identified 3, screened 3', 'Identified 300, screened 3', 1)
assert x4 != e49
run('X4 A8 identified 3->300', {base_sec: sx.replace(e49, x4, 1).encode()}, 'green (disclosed: identified not derivable)')
# X5 A8: round-48 late entry with inflated included but consistent screened==included+excluded
e48 = lines[i48]
x5 = e48.replace('Identified 2, screened 2, included 1, excluded 1', 'Identified 2, screened 2, included 1, excluded 1', 1)
# X6 A8: second round-49 entry dated differently (tag matching is by date prefix)
dup49b = '- 2026-10-29 round 49 — Question: second entry with a different date. Identified 1, screened 1, included 0, excluded 1; rows 149 → 149. Exclusion: none applies. Stop: duplicate.'
l6 = lines[:i49+1] + [dup49b] + lines[i49+1:]
run('X6 A8 extra round-49 entry dated 10-29', {base_sec: '\n'.join(l6).encode()}, 'expected: not counted (date-prefix match)')
# X7 A6: heading membership test -- anchor text merely contains the heading
s147 = [l for l in sx.split('\n') if l.startswith('| S147 |')][0]
pop = g.show(R, 'corpus/evidence/round-49/c2/popper.html')
norm = c2.html_norm(pop)
print('X7 snapshot heading check: s147 anchor contains section3 heading:', '3. The Problem of Demarcation' in s147)
# X8 A7 snapshot forgery with re-pinned sha (disclosed limit: snapshot not bound to live page)
sy = g.show(R, 'corpus/evidence/round-49/c2/sysexits.html')
sy2 = sy.replace(b'EX_USAGE', b'EX_USAGE')  # no-op placeholder for identical bytes check
print('X8 sysexits snapshot sha', sha(sy))
