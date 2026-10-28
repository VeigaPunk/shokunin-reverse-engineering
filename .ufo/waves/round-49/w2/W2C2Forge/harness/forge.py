import hashlib, json, os, re, subprocess, sys, time, datetime
S = '/fast/scratch/hyaku/kaidoku-r49/W2C2Forge'
C = os.path.join(S, 'c0')
R = '29883d4ec35a31a8393c4ffb220888c44c0bb022'
F = 'decc5697bfd4ec1e9de4a762ad199d9bd9c4230d'
B = 'e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'
CTR = os.path.join(S, 'c2-frozen.py')
OUT = os.path.join(S, 'out'); os.makedirs(OUT, exist_ok=True)
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS='1', TMPDIR=S, HYAKU_SCRATCH='/fast/scratch/hyaku')
L = 'corpus/lessons/round-49.md'; SC = 'SCORECARD.md'; SRC = 'corpus/SOURCES.md'
SNAP = 'corpus/evidence/round-49/c2/popper.html'
RC1 = '.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json'
def g(*a, inp=None):
    p = subprocess.run(['git', '-C', C] + list(a), capture_output=True, input=inp, env=ENV)
    return p
def rd(p):
    return open(os.path.join(C, p), 'rb').read().decode('utf-8')
def wr(p, t):
    full = os.path.join(C, p); os.makedirs(os.path.dirname(full), exist_ok=True)
    open(full, 'wb').write(t.encode('utf-8') if isinstance(t, str) else t)
def rep(p, old, new, count=1):
    t = rd(p); n = t.count(old)
    assert n >= 1, ('NOOP', p, old[:60])
    wr(p, t.replace(old, new, count))
def line_rep(p, pat, fn):
    t = rd(p); ls = t.split('\n'); hits = [i for i, l in enumerate(ls) if re.search(pat, l)]
    assert len(hits) >= 1, ('NOLINE', p, pat)
    i = hits[0]; ls[i] = fn(ls[i]); wr(p, '\n'.join(ls))
def sha(b): return hashlib.sha256(b).hexdigest()
def ctr(rev, freeze, battery, ctrpath=CTR, tag=''):
    name = os.path.join(OUT, tag + ('-bat' if battery else '-plain') + '.json')
    cmd = ['python3', '-I', '-B', ctrpath, '--root', C, '--rev', rev, '--freeze', freeze, '--json-out', name]
    if battery: cmd.append('--battery')
    p = subprocess.run(cmd, capture_output=True, env=ENV)
    try:
        d = json.load(open(name))
    except Exception:
        d = {}
    red = sorted(k for k, v in d.get('atoms', {}).items() if not v['ok'])
    bf = d.get('battery', {}).get('failing') if battery else None
    return dict(exit=p.returncode, mismatches=d.get('mismatches'), reason=d.get('reason'), red=red,
                battery_failing=bf, counter_sha=d.get('counter_sha256'),
                stdout_sha=sha(open(name, 'rb').read()) if os.path.exists(name) else None,
                stderr=p.stderr.decode()[-300:], why={k: v['why'] for k, v in d.get('atoms', {}).items() if not v['ok']})
def reset():
    assert g('rev-parse', '--show-toplevel').stdout.decode().strip() == C
    g('checkout', '-q', '-f', '--detach', R); g('clean', '-fdq')
    assert g('rev-parse', 'HEAD').stdout.decode().strip() == R
def commit(msg):
    g('add', '-A', '-f'); p = g('commit', '-q', '-m', msg)
    assert p.returncode == 0, p.stderr
    return g('rev-parse', 'HEAD').stdout.decode().strip()
A3_OLD = 'log_2e785632=3440,3441,3445 log_33f65a91=3440,3441,3444 log_c093e798=3440,3441,3445'
A1_OLD = 'declared=b6f7ca2a6391964dfdedd477cd560bd42159873a stale=0f06251bf6a3a6964c715f67243d4df12e854258'
A4_OLD = 'seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers'
S148 = lambda l: l
def s_line(prefix_re):
    return prefix_re
def edit_s147(fn):
    line_rep(SRC, r'^\| S147 \|', fn)
def edit_s148(fn):
    line_rep(SRC, r'^\| S148 \|', fn)
def edit_s149(fn):
    line_rep(SRC, r'^\| S149 \|', fn)
def edit_r49(fn):
    line_rep(SRC, r'^- 2026-10-28 round 49 ', fn)
def edit_r48(fn):
    line_rep(SRC, r'^- 2026-10-28 round 48 \(late entry', fn)
def stub_w1():
    for s in ('C1Battery', 'C1Meaning', 'ScribeReportNumbers'):
        wr('.ufo/waves/round-48/w1/%s.md' % s, '')
def w_pin_popper_fab():
    t = open(os.path.join(C, SNAP), 'rb').read()
    nt = t + b'\n<p>Fabricated paragraph asserting a new reading.</p>\n'
    wr(SNAP, nt)
    newsha = sha(nt)
    edit_s147(lambda l: l.replace('2c2d48c6891418c46c372a780ce2e76c00bcc9716bb7603f169976d61b6ec207', newsha))
    return newsha

def forgeries():
    # each: label, description, expected-by-analysis, function applying edits (returns commit msg)
    out = []
    def add(label, desc, expect, fn):
        out.append((label, desc, expect, fn))
    # ---- wave-1 re-run
    add('W01', 'three zero-byte .md stubs under round-48 w1; record unchanged', 'green (record unchanged; base-bound)', stub_w1)
    def w02():
        stub_w1(); line_rep(L, r'^- A4 ', lambda l: '- A4 seats=75 reports=75 missing=')
    add('W02', 'stubs + lesson A4 restated reports=75 missing=', 'red A4', w02)
    def w03():
        import json as j
        d = j.loads(subprocess.run(['git', '-C', C, 'show', R + ':.ufo/waves/round-48/r48-w1-results.json'], capture_output=True, env=ENV).stdout)
        d['results'] = d['results'][:-3]
        wr('.ufo/waves/round-48/r48-w1-results.json', j.dumps(d, indent=1))
        line_rep(L, r'^- A4 ', lambda l: '- A4 seats=72 reports=72 missing=')
    add('W03', 'results.json at REV drops 3 seats; A4 restated seats=72', 'red A4 (base results)', w03)
    def w04():
        rep(SC, '**Declared freeze:** `b6f7ca2a6391964dfdedd477cd560bd42159873a`', '**Declared freeze:** `8847042a140b044dbf335210c965bf7b06b09b4f`')
        line_rep(L, r'^- A1 ', lambda l: l.replace('declared=b6f7ca2a6391964dfdedd477cd560bd42159873a', 'declared=8847042a140b044dbf335210c965bf7b06b09b4f'))
    add('W04', 'SCORECARD round-48 declared freeze re-pointed at REV; A1 restated', 'red A1 (base SCORECARD)', w04)
    def w05():
        t = open(os.path.join(C, RC1), 'rb').read()
        nt = t[:-1] + b' \n'
        wr(RC1, nt)
        raw, strp = sha(nt), sha(nt[:-1])
        line_rep(L, r'^- A5 ', lambda l: re.sub(r'c1_raw=\w+', 'c1_raw=' + raw, re.sub(r'c1_stripped=\w+', 'c1_stripped=' + strp, re.sub(r'report_c1=\w+', 'report_c1=' + strp[:8], l))))
    add('W05', 'round-48 c1 receipt rewritten at REV; A5 digests restated', 'red A5 (base receipt)', w05)
    add('W06', 'A3 drops log_33f65a91 pointer', 'red A3', lambda: rep(L, ' log_33f65a91=3440,3441,3444', ''))
    def w07():
        newsha = w_pin_popper_fab()
    add('W07', 'popper.html self-authored (fabricated paragraph) + S147 pin re-written', 'green (disclosed: snapshot self-attested)', w07)
    add('W08', 'round-49 search log identified 3 -> 300', 'green (disclosed: identified asserted)', lambda: edit_r49(lambda l: l.replace('Identified 3, screened 3', 'Identified 300, screened 3')))
    add('W09', 'round-48 closure rewritten at REV (Admission flipped)', 'green (counter reads closure at base; by design)', lambda: rep('corpus/lessons/round-48-verifier-spotcheck.md', 'Admission: **rejected-harmed**', 'Admission: **admitted**'))
    add('W10', 'duplicate A4 line inserted above the real one', 'red (duplicate atom line)', lambda: line_rep(L, r'^- A4 ', lambda l: '- A4 seats=75 reports=75 missing=\n' + l))
    add('W11', 'A2 dead hash replaced by 663f30ee + 32 zeros', 'red A2', lambda: rep(L, 'dead=663f30ee7516942a0120e7de68fe88356e680822', 'dead=663f30ee' + '0' * 32))
    add('W12', 'A3 unnamed list drops 8847042a', 'red A3', lambda: rep(L, 'unnamed=577a02a5,8847042a,7fe11332', 'unnamed=577a02a5,7fe11332'))
    add('W13', 'S148 teaches inverted to EX_USAGE is 2', 'red A7', lambda: edit_s148(lambda l: l.replace('EX_USAGE is 64', 'EX_USAGE is 2')))
    add('W15', 'round-49 lesson header Declared freeze -> 0f06251b (round-48 header defect recurring)', 'green (no atom reads the round-49 header)',
        lambda: rep(L, 'Declared freeze `decc5697bfd4ec1e9de4a762ad199d9bd9c4230d`', 'Declared freeze `0f06251bf6a3a6964c715f67243d4df12e854258`'))
    add('W16', 'prose line in round-49 lesson restating 0f06251b', 'green (prose not judged)', lambda: rep(L, '## Mistakes', '## Mistakes\n\nThe round-48 declared freeze is 0f06251b (A4).\n'))
    # ---- new forgeries
    add('N01', 'A3 duplicate key within one line: wrong log_2e785632 first, correct last', 'green (last-wins hides the first token)',
        lambda: rep(L, A3_OLD, 'log_2e785632=9999 ' + A3_OLD))
    add('N02', 'A4 duplicate key within one line: seats=9 first, seats=75 last', 'green (last-wins)',
        lambda: rep(L, A4_OLD, 'seats=9 ' + A4_OLD))
    add('N03', 'A1 duplicate key within one line: wrong declared first, correct last', 'green (last-wins)',
        lambda: rep(L, A1_OLD, 'declared=8847042a140b044dbf335210c965bf7b06b09b4f ' + A1_OLD))
    add('N04', 'A9 SCORECARD line with duplicate verdict key', 'red (exact-line compare)',
        lambda: rep(SC, '- A9 verdict=rejected-harmed source=', '- A9 verdict=rejected-harmed verdict=admitted source='))
    def n05():
        edit_r48(lambda l: l)
        t = rd(SRC); lines = t.split('\n')
        i = [k for k, l in enumerate(lines) if l.startswith('- 2026-10-28 round 48 (late entry')][0]
        lines.insert(i + 1, '- 2026-10-28 round 48 — Question: restated. Where searched: restated. Identified 9, screened 9, included 9, excluded 0; rows 1 -> 2. Stop: restated.')
        wr(SRC, '\n'.join(lines))
    add('N05', 'second round-48 search-log entry without the late marker, contradicting the first', 'green (only late-marked entries are counted)', n05)
    add('N06', 'S148 teaches adds "EX_USAGE  is 2" (double space)', 'green (regex needs single space)', lambda: edit_s148(lambda l: l.replace('(a command used incorrectly);', '(a command used incorrectly); EX_USAGE  is 2 on other hosts;', 1)))
    add('N07', 'S148 teaches adds "EX_USAGE: 2"', 'green (regex only matches "is")', lambda: edit_s148(lambda l: l.replace('(a command used incorrectly);', '(a command used incorrectly); EX_USAGE: 2 on other hosts;', 1)))
    add('N08', 'S148 teaches adds "EX_USAGE means 2"', 'green (regex only matches "is")', lambda: edit_s148(lambda l: l.replace('(a command used incorrectly);', '(a command used incorrectly); EX_USAGE means 2 elsewhere;', 1)))
    add('N09', 'round-49 search log appends a contradicting restatement after the first numbers', 'green (first match wins)',
        lambda: edit_r49(lambda l: l + ' Restated: identified 1, screened 1, included 1, excluded 0; rows 1 -> 2.'))
    add('N10', 'A3 pointer list with a non-numeric token', 'green (isdigit filter drops it silently)',
        lambda: rep(L, 'log_c093e798=3440,3441,3445 ', 'log_c093e798=3440,3441,3445,xyz '))
    add('N11', 'round-49 entry: Exclusion: token removed (excluded 1)', 'red (exclusion: required when excluded > 0)', lambda: edit_r49(lambda l: l.replace('Exclusion:', 'Excluded:')))
    add('N12', 'round-49 entry: where searched token removed', 'red', lambda: edit_r49(lambda l: l.replace('Where searched:', 'Where looked:')))
    add('N13', 'S147 used-by lesson path removed', 'red (used-by must list the lesson)', lambda: edit_s147(lambda l: l.replace('corpus/lessons/round-49.md', 'corpus/lessons/round-XX.md')))
    add('N14', 'S149 status flipped to mined; round-49 counts restated to 3/0 (teaches still says REJECTED)', 'green (status cell is the derivation input; prose not judged)',
        lambda: (edit_s149(lambda l: l.replace('| rejected |', '| mined |')), edit_r49(lambda l: l.replace('included 2, excluded 1', 'included 3, excluded 0'))))
    add('N15', 'popper.html edited, S147 pin NOT updated', 'red A6 (pin)', lambda: wr(SNAP, open(os.path.join(C, SNAP), 'rb').read() + b'\n<p>x</p>\n'))
    add('N16', 'A2 actual replaced by base commit (same prefix absent)', 'red A2', lambda: rep(L, 'actual=663f30ee751694fb0970e7de68fe88356e680822', 'actual=e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9'))
    add('N17', 'S147 stated word count wrong (21 -> 20)', 'red A6', lambda: edit_s147(lambda l: l.replace('(21 words)', '(20 words)', 1)))
    add('N18', 'A9 SCORECARD line without calibration=harmed', 'red A9', lambda: rep(SC, ' calibration=harmed\n', '\n'))
    add('N19', 'round-48 late entry: included 1 excluded 1 restated as 2/0', 'red A8', lambda: edit_r48(lambda l: l.replace('included 1, excluded 1', 'included 2, excluded 0')))
    add('N20', 'round-49 entry identified 3 -> 2 (below screened)', 'red A8', lambda: edit_r49(lambda l: l.replace('Identified 3,', 'Identified 2,')))
    add('N21', 'round-48 late entry: rows 144 -> 146 restated 144 -> 147', 'red A8', lambda: edit_r48(lambda l: l.replace('rows 144 → 146', 'rows 144 → 147')))
    add('N22', 'round-48 late marker removed from its only entry', 'red A8', lambda: edit_r48(lambda l: l.replace('late entry', 'last entry')))
    return out

if __name__ == '__main__':
    sel = sys.argv[1:]
    res = []
    for label, desc, expect, fn in forgeries():
        if sel and label not in sel:
            continue
        reset()
        t0 = time.time()
        try:
            fn()
            msg = commit('forgery ' + label)
        except AssertionError as e:
            res.append(dict(label=label, error=str(e))); print(label, 'EDIT-ERROR', e); continue
        p = ctr('HEAD', F, False, tag=label)
        b = ctr('HEAD', F, True, tag=label) if p['exit'] == 0 else None
        row = dict(label=label, desc=desc, expect=expect, commit=msg, plain=p, battery=b, utc=datetime.datetime.utcnow().isoformat() + 'Z')
        res.append(row)
        print(label, 'plain exit', p['exit'], 'mism', p['mismatches'], 'red', p['red'], '| bat', (b or {}).get('exit'), (b or {}).get('battery_failing'), '|', expect)
    json.dump(res, open(os.path.join(OUT, 'results-%s.json' % ('-'.join(sel) or 'all')), 'w'), indent=1, default=str)
