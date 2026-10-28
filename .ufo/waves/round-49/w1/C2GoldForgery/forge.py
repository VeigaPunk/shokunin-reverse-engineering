import hashlib, json, os, re, subprocess, sys
S = '/fast/scratch/hyaku/kaidoku-r49/C2GoldForgery'
D = S + '/c0'
CTR = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-49/draft/tools/round-49/c2-mismatch.py'
AFTER = open(S + '/after_rev').read().strip()
FZ = open(S + '/freeze_rev').read().strip()
def g(*a, inp=None):
    return subprocess.run(['git', '-C', D] + list(a), capture_output=True, input=inp)
def cur(p):
    return g('show', AFTER + ':' + p).stdout
def sha(b): return hashlib.sha256(b).hexdigest()
def rep(b, a, c, n=1):
    t = b.decode('utf-8')
    assert t.count(a) >= 1, ('missing', a[:70])
    return t.replace(a, c, n).encode('utf-8')
LES = 'corpus/lessons/round-49.md'
SRC = 'corpus/SOURCES.md'
SC = 'SCORECARD.md'
CLOSE = 'corpus/lessons/round-48-verifier-spotcheck.md'
W1 = '.ufo/waves/round-48/w1'
RES = '.ufo/waves/round-48/r48-w1-results.json'
RC1 = '.ufo/waves/round-48/l1/scores/c1-final-33f65a91.json'
SNAP_P = 'corpus/evidence/round-49/c2/popper.html'
SNAP_S = 'corpus/evidence/round-49/c2/sysexits.html'
forg = {}
# F01 A4 stub seat reports (empty files) + restated counts
forg['F01-A4-empty-stub-reports'] = {
    W1 + '/C1Meaning.md': b'', W1 + '/C1Battery.md': b'', W1 + '/ScribeReportNumbers.md': b'',
    LES: rep(cur(LES), 'reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers', 'reports=75 missing=')}
# F02 A4 results.json edited at REV (three failed seats dropped from the registry)
def f02():
    j = json.loads(cur(RES)); j['results'] = [x for x in j['results'] if x['name'] not in ('C1Meaning', 'C1Battery', 'ScribeReportNumbers')]
    return json.dumps(j, indent=2).encode() + b'\n'
forg['F02-A4-results-json-edited'] = {RES: f02(),
    LES: rep(cur(LES), 'seats=75 reports=72 missing=C1Battery,C1Meaning,ScribeReportNumbers', 'seats=72 reports=72 missing=')}
# F03 A1 SCORECARD declared freeze re-pointed at a different commit; correction re-derived
forg['F03-A1-scorecard-redeclared'] = {
    SC: rep(cur(SC), '**Declared freeze:** `b6f7ca2a6391964dfdedd477cd560bd42159873a`', '**Declared freeze:** `8847042a140b044dbf335210c965bf7b06b09b4f`'),
    LES: rep(cur(LES), 'declared=b6f7ca2a6391964dfdedd477cd560bd42159873a', 'declared=8847042a140b044dbf335210c965bf7b06b09b4f')}
# F04 A5 round-48 receipt bytes edited at REV (whitespace-only), digests re-derived
def f04():
    b = cur(RC1); nb = b.replace(b'\n', b' \n', 1)
    return nb
nb = f04(); c1raw = sha(nb); c1s = sha(nb[:-1] if nb.endswith(b'\n') else nb)
les04 = cur(LES).decode().replace('c1_raw=6320c5d240e4822d1612c2cb929b383ca6f628953f032c7c92253e53d8ced86e', 'c1_raw=' + c1raw)
les04 = les04.replace('c1_stripped=3cc2d72d8f6564545a7d9f32c86a4d3a81bf5367f8b55bdb15075e60401e8f77', 'c1_stripped=' + c1s).replace('report_c1=3cc2d72d', 'report_c1=' + c1s[:8])
forg['F04-A5-round48-receipt-edited'] = {RC1: nb, LES: les04.encode()}
# F05 A3 omit the log_33f65a91 pointer (the one the closure called wrong)
forg['F05-A3-omit-pointer'] = {LES: rep(cur(LES), ' log_33f65a91=3440,3441,3444', '')}
# F06 A6 fabricated snapshot + fabricated quote in row, snapshot re-pinned
qf = 'falsifiability is the criterion that the 2026 review board certified for all empirical sciences'
snap6 = ('<html><body><h2>2. Backdrop to Popper\u2019s Thought</h2><p>' + qf + '</p></body></html>').encode('utf-8')
def line_sub(text, prefix, a, c):
    out, hit = [], 0
    for l in text.split('\n'):
        if l.lstrip().startswith(prefix):
            hit += 1; l = l.replace(a, c)
        out.append(l)
    assert hit == 1, (prefix, hit)
    return '\n'.join(out)
s147 = cur(SRC).decode()
q1 = 'falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific'
s147 = line_sub(s147, '| S147 ', q1, qf)
s147 = line_sub(s147, '| S147 ', '(21 words)', '(%d words)' % len(qf.split()))
s147 = line_sub(s147, '| S147 ', sha(cur(SNAP_P)), sha(snap6))
row6b = s147
forg['F06-A6-fabricated-snapshot-repinned'] = {SNAP_P: snap6, SRC: row6b.encode()}
# F07 A8 identified inflated (identified/screened not re-derived from anything)
forg['F07-A8-identified-inflated'] = {SRC: rep(rep(cur(SRC), 'identified 2, screened 2, included 2, excluded 0; rows 146', 'identified 400, screened 2, included 2, excluded 0; rows 146'), 'identified 2, screened 2, included 1, excluded 1; rows 144', 'identified 999, screened 2, included 1, excluded 1; rows 144')}
# F08 A9 source closure admission flipped; SCORECARD verdict string survives as substring
cl = cur(CLOSE).decode()
cl = cl.replace('Admission: **rejected-harmed**.', 'Admission: **admitted**.').replace('**Rejected-harmed** because', '**Admitted** because')
cl += '\nSuperseded draft admission wording, kept for the record: rejected-harmed.\n'
forg['F08-A9-closure-verdict-flipped'] = {CLOSE: cl.encode()}
# F09 A4 duplicate (shadowed) line: false line first, correct line later wins in dict
forg['F09-duplicate-lesson-line'] = {LES: rep(cur(LES), '- A4 seats=75 reports=72', '- A4 seats=75 reports=75 missing=\n- A4 seats=75 reports=72')}
# F10 A2 dead hash arbitrary non-commit with the 8-hex prefix
forg['F10-A2-dead-hash-arbitrary'] = {LES: rep(cur(LES), 'dead=663f30ee7516942a0120e7de68fe88356e680822', 'dead=663f30ee' + '0' * 32)}
# F11 A3 unnamed list truncated (completeness not checked)
forg['F11-A3-unnamed-truncated'] = {LES: rep(cur(LES), 'unnamed=577a02a5,8847042a', 'unnamed=577a02a5')}
# F12 A7 teaches inverts the convention; snapshot unchanged; token check passes
forg['F12-A7-teaches-inverted'] = {SRC: rep(cur(SRC), 'EX_USAGE is 64, not 2', 'EX_USAGE is 2, not 64')}
# F13 A6 snapshot "heading" forged only (section name is a free token in the pinned snapshot)
cur_pop = cur(SNAP_P)
forg['F13-A6-pinned-snapshot-edited-bytes-only'] = {SNAP_P: cur_pop.replace(b'empirical', b'empirica1')}
# F15/F16 (lesson-level)
forg['F15-round49-header-stale-freeze'] = {LES: ('# Round 49 - lessons (dev fixture)\n\nDeclared freeze `0f06251bf6a3a6964c715f67243d4df12e854258` (series A1-A4).\n' + cur(LES).decode().split('\n', 2)[2]).encode()}
forg['F16-lesson-prose-contradicts-A-lines'] = {LES: cur(LES).decode().replace('- A6 row=S147', '- A6 row=S147\n\nThe round-48 declared freeze is 0f06251b (A4); the correction above is not a rewrite.').encode()}
if __name__ == '__main__':
    only = sys.argv[1:]
    res = {}
    for label, edits in forg.items():
        if only and not any(label.startswith(o) for o in only):
            continue
        g('checkout', '-q', '-f', '--detach', AFTER); g('clean', '-fdq')
        assert g('rev-parse', '--show-toplevel').stdout.decode().strip() == D
        for p, b in edits.items():
            fp = D + '/' + p
            if b is None:
                os.remove(fp); continue
            os.makedirs(os.path.dirname(fp), exist_ok=True); open(fp, 'wb').write(b)
        g('add', '-A'); cp = g('commit', '-q', '-m', 'forgery ' + label)
        assert cp.returncode == 0, cp.stderr
        rev = g('rev-parse', 'HEAD').stdout.decode().strip()
        out = S + '/out-' + label + '.json'
        p1 = subprocess.run(['python3', '-I', '-B', CTR, '--root', D, '--rev', rev, '--freeze', FZ, '--json-out', out + '.plain'], capture_output=True, text=True)
        p2 = subprocess.run(['python3', '-I', '-B', CTR, '--root', D, '--rev', rev, '--freeze', FZ, '--battery', '--json-out', out], capture_output=True, text=True)
        d = json.load(open(out))
        pl = json.load(open(out + '.plain'))
        red = [k for k, v in pl.get('atoms', {}).items() if not v['ok']]
        res[label] = dict(rev=rev, plain_exit=p1.returncode, plain_mismatches=pl.get('mismatches'), plain_red=red,
                          battery_exit=p2.returncode, battery_failing=d.get('battery', {}).get('failing'),
                          json_sha256=sha(open(out, 'rb').read()))
        print(label, json.dumps(res[label]))
    json.dump(res, open(S + '/forgery-results-' + ('_'.join(o.split('-')[0] for o in only) or 'all') + '.json', 'w'), indent=1)
