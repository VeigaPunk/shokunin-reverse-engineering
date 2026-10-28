import sys, importlib.util, json
sys.dont_write_bytecode = True
DRAFT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c2-mismatch.py'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
E = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
spec = importlib.util.spec_from_file_location('c2m', DRAFT)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
g = m.Git(LANE)
def lesson(lines):
    body = '## Corrections to round 48\n\n' + '\n'.join(lines) + '\n'
    return {m.LESSON: body.encode()}
def run(label, lines, atoms=('A3', 'A4')):
    ov = m.Overlay(g, E, lesson(lines))
    sc = m.score(ov, E)
    out = {k: sc[k] for k in atoms}
    print(json.dumps({'case': label, 'lines': lines, **out}, ensure_ascii=False))
A3 = '- A3 '
run('F0 honest A3 (full sets)', [
  '- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a'])
run('F1 A3 states only 33f65a91 (per-hash completeness)', [
  '- A3 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a'])
run('F2 A3 uses closure phrasing for 2e785632 (3445 only)', [
  '- A3 log_2e785632=3445 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a'])
run('F3 A3 keys by full 40-hex of 33f65a91 (LOG uses 8-hex)', [
  '- A3 log_33f65a913cfd21a4491a4f8b7ccc8f00069f058d=3440,3441,3444 unnamed=577a02a5,8847042a'])
run('F4 duplicate A3 lines: first wrong, second honest', [
  '- A3 log_2e785632=3442,3443,3444 unnamed=577a02a5,8847042a',
  '- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a'])
run('F5 A3 lists 0f06251b as unnamed (it is at 3439)', [
  '- A3 log_33f65a91=3440,3441,3444 unnamed=0f06251b,577a02a5'])
run('F6 A3 lists 663f30ee (named at 3449) as unnamed', [
  '- A3 log_33f65a91=3440,3441,3444 unnamed=663f30ee,577a02a5'])
run('F7 A3 no unnamed key', [
  '- A3 log_33f65a91=3440,3441,3444'])
run('F8 A4 honest', [
  '- A4 seats=75 reports=72 missing=C1Meaning,C1Battery,ScribeReportNumbers'], atoms=('A4',))
run('F9 A4 LOG-style accounting (73; C1Battery-2)', [
  '- A4 seats=75 reports=73 missing=C1Battery-2,ScribeReportNumbers'], atoms=('A4',))
run('F10 A4 reordered missing list', [
  '- A4 seats=75 reports=72 missing=ScribeReportNumbers,C1Meaning,C1Battery'], atoms=('A4',))
run('F11 A4 duplicate line: first wrong, second honest (last wins)', [
  '- A4 seats=75 reports=73 missing=C1Battery-2,ScribeReportNumbers',
  '- A4 seats=75 reports=72 missing=C1Meaning,C1Battery,ScribeReportNumbers'], atoms=('A4',))
# mutation arms for A3/A4 against the honest overlay: each must flip exactly its own atom
honest = m.Overlay(g, E, lesson([
  '- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 unnamed=577a02a5,8847042a',
  '- A4 seats=75 reports=72 missing=C1Meaning,C1Battery,ScribeReportNumbers']))
muts = m.mutations(honest, E)
print(json.dumps({'mutation_labels': [l for l, a, o in muts]}, ensure_ascii=False))
base = m.score(honest, E)
print(json.dumps({'honest_A3': base['A3'], 'honest_A4': base['A4']}, ensure_ascii=False))
for label, atom, over in muts:
    if atom not in ('A3', 'A4'): continue
    got = m.score(m.Overlay(honest, E, over), E)
    print(json.dumps({'mut': label, 'atom': atom, 'A3_red': got['A3'], 'A4_red': got['A4']}, ensure_ascii=False))
