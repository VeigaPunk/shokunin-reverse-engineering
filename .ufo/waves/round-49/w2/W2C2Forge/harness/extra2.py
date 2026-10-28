import sys, os, json, importlib.util, subprocess
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/W2C2Forge')
import forge as f
from forge import rd, wr, rep, line_rep, SRC, L, SC, R, C, ENV
spec = importlib.util.spec_from_file_location('c2f', f.CTR); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
def window26():
    raw = subprocess.run(['git', '-C', C, 'show', R + ':corpus/evidence/round-49/c2/popper.html'], capture_output=True, env=ENV).stdout
    norm = c2.html_norm(raw)
    words = norm.split(' ')
    for i in range(200, len(words) - 26):
        w = words[i:i + 26]
        s = ' '.join(w)
        if '"' in s or '\x01' in s or '\x02' in s or '\x03' in s or len(s) > 200:
            continue
        return s
    raise SystemExit('no window')
def n29(): line_rep(L, r'^- A1 ', lambda l: l.replace('stale=0f06251bf6a3a6964c715f67243d4df12e854258', 'stale=8847042a140b044dbf335210c965bf7b06b09b4f'))
def n31(): line_rep(L, r'^- A4 ', lambda l: l.replace('seats=75', 'seats=74'))
def n32(): line_rep(L, r'^- A4 ', lambda l: l.replace('missing=C1Battery,C1Meaning,ScribeReportNumbers', 'missing=C1Battery,C1Meaning'))
def n33(): line_rep(L, r'^- A5 ', lambda l: l.replace('report_c1=3cc2d72d', 'report_c1=6320c5d2'))
def n34():
    w = window26()
    line_rep(SRC, r'^\| S147 \|', lambda l: __import__('re').sub(r'"[^"]+"\s*\(\d+ words\)', '"' + w + '" (26 words)', l, count=1))
def n35(): line_rep(SRC, r'^\| S147 \|', lambda l: l.replace('2. Backdrop to Popper’s Thought', '3. The Problem of Demarcation', 1))
def n36(): line_rep(SRC, r'^\| S148 \|', lambda l: l.replace('(a command used incorrectly);', '(a command used incorrectly); EX_USAGE is 2 on other hosts;', 1))
def n37():
    t = rd(SRC).split('\n'); i = [k for k, l in enumerate(t) if l.startswith('- 2026-10-28 round 48 (late entry')][0]
    t.insert(i + 1, t[i]); wr(SRC, '\n'.join(t))
def n39(): line_rep(SRC, r'^- 2026-10-28 round 49 ', lambda l: l.replace('Stop:', 'Halt:'))
def n40(): rep(SC, '- A9 verdict=rejected-harmed', '- A9 verdict=admitted')
def n43(): line_rep(L, r'^- A2 ', lambda l: l.replace('actual=663f30ee751694fb0970e7de68fe88356e680822', 'actual=663f30ee7516942a0120e7de68fe88356e680822'))
EXTRA2 = [('N29', 'A1 stale= names a commit that is not the lesson header', 'red A1', n29),
          ('N31', 'A4 seats=74', 'red A4', n31),
          ('N32', 'A4 missing list drops one seat', 'red A4', n32),
          ('N33', 'A5 report_c1 = raw digest prefix', 'red A5', n33),
          ('N34', 'A6 S147 quote is a 26-word window of the snapshot (counted as 26)', 'red A6 (over 25 words)', n34),
          ('N35', 'A6 S147 anchor names a different heading', 'red A6', n35),
          ('N36', 'A7 S148 teaches adds a second status "EX_USAGE is 2" (no double space)', 'red A7', n36),
          ('N37', 'A8 round-48 late entry duplicated', 'red A8', n37),
          ('N39', 'A8 round-49 entry: Stop: renamed Halt:', 'red A8', n39),
          ('N40', 'A9 SCORECARD verdict changed to admitted', 'red A9', n40),
          ('N43', 'A2 actual == dead (same hash)', 'red A2', n43)]
if __name__ == '__main__':
    import datetime
    res = []
    for label, desc, expect, fn in EXTRA2:
        f.reset()
        try:
            fn(); msg = f.commit('forgery ' + label)
        except AssertionError as e:
            print(label, 'EDIT-ERROR', e); continue
        p = f.ctr('HEAD', f.F, False, tag=label)
        b = f.ctr('HEAD', f.F, True, tag=label) if p['exit'] == 0 else None
        print(label, 'plain exit', p['exit'], 'mism', p['mismatches'], 'red', p['red'], '| bat', (b or {}).get('exit'), (b or {}).get('battery_failing'), '|', expect, '|', p['why'].get(p['red'][0]) if p['red'] else '')
        res.append(dict(label=label, desc=desc, expect=expect, commit=msg, plain=p, battery=b))
    json.dump(res, open(os.path.join(f.OUT, 'results-extra2.json'), 'w'), indent=1, default=str)
