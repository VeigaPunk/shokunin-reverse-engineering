import sys, importlib.util, json
sys.dont_write_bytecode = True
DRAFT = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c2-mismatch.py'
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
E = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
spec = importlib.util.spec_from_file_location('c2m', DRAFT)
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
g = m.Git(LANE)
def run(label, lines):
    body = '## Corrections to round 48\n\n' + '\n'.join(lines) + '\n'
    sc = m.score(m.Overlay(g, E, {m.LESSON: body.encode()}), E)
    print(json.dumps({'case': label, 'A3': sc['A3']}, ensure_ascii=False))
run('R1 A3 extended: all four LOG-named hashes the fleet report cites', [
  '- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 log_c093e798=3440,3441,3445 log_7fe11332=none unnamed=7fe11332,577a02a5,8847042a'])
run('R2 A3 R1 but 7fe11332 wrongly absent from unnamed', [
  '- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 log_c093e798=3440,3441,3445 log_7fe11332=none unnamed=577a02a5,8847042a'])
run('R3 A3 R1 but c093e798 stated as the fleet cite 3440,3441 (omits 3445)', [
  '- A3 log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 log_c093e798=3440,3441 log_7fe11332=none unnamed=7fe11332,577a02a5,8847042a'])
