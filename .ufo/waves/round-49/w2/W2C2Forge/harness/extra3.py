import sys, os, json, importlib.util, subprocess, re
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/W2C2Forge')
import forge as f
from forge import rd, wr, rep, line_rep, SRC, L, SC, R, C, ENV
spec = importlib.util.spec_from_file_location('c2f', f.CTR); c2 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c2)
def window26_after_heading():
    raw = subprocess.run(['git', '-C', C, 'show', R + ':corpus/evidence/round-49/c2/popper.html'], capture_output=True, env=ENV).stdout
    norm = c2.html_norm(raw)
    head = '2. Backdrop to Popper’s Thought'
    words_idx = [m.start() for m in re.finditer(r'\S+', norm)]
    toks = re.findall(r'\S+', norm)
    for i in range(len(toks) - 26):
        s = ' '.join(toks[i:i + 26])
        if '"' in s or any(ch in s for ch in '\x01\x02\x03'):
            continue
        pos = norm.find(s)
        if c2.section_of(norm, pos) == head:
            return s
    raise SystemExit('no window under heading')
def n34b():
    w = window26_after_heading()
    line_rep(SRC, r'^\| S147 \|', lambda l: re.sub(r'"[^"]+"\s*\(\d+ words\)', '"' + w + '" (26 words)', l, count=1))
def n44(): wr('corpus/lessons/round-48.md', rd('corpus/lessons/round-48.md') + '\nA later sentence the counter does not read.\n')
def n45(): line_rep(L, r'^- A1 ', lambda l: l.replace('declared=b6f7ca2a6391964dfdedd477cd560bd42159873a', 'declared=8847042a140b044dbf335210c965bf7b06b09b4f'))
EXTRA3_ = [('N34b', 'A6 S147 quote is a 26-word window after the heading (heading check passes)', 'red A6 (over 25)', n34b),
          ('N44', 'round-48 lesson gains one sentence at REV (header unchanged)', 'red A1 (not byte-identical)', n44),
          ('N45', 'A1 declared= names a commit but SCORECARD base freeze unchanged', 'red A1', n45)]
EXTRA3 = [('N34b', 'A6 S147 quote is a 26-word window under the Backdrop heading (heading check passes)', 'red A6 (over 25)', n34b), ('N44', 'round-48 lesson gains one sentence at REV (header unchanged)', 'red A1 (not byte-identical)', n44), ('N45', 'A1 declared= names a commit but SCORECARD base freeze unchanged', 'red A1', n45)]
if __name__ == '__main__':
    import json
    res = []
    for label, desc, expect, fn in EXTRA3:
        f.reset(); fn(); msg = f.commit('forgery ' + label)
        p = f.ctr('HEAD', f.F, False, tag=label)
        print(label, 'plain exit', p['exit'], 'mism', p['mismatches'], 'red', p['red'], '|', expect, '|', (p['why'].get(p['red'][0]) if p['red'] else ''))
        res.append(dict(label=label, desc=desc, expect=expect, commit=msg, plain=p))
    json.dump(res, open(os.path.join(f.OUT, 'results-extra3.json'), 'w'), indent=1, default=str)
