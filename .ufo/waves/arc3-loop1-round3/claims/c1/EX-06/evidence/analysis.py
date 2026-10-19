#!/usr/bin/env python3
# EX-06 (arc3-loop1-round3) — analysis of the carrier probe battery.
# Loads captured envelopes, strips per-request identity/path fields, deep-diffs.
# Run from repo root: python3 .ufo/waves/arc3-loop1-round3/claims/c1/EX-06/evidence/analysis.py
import json, hashlib
E = '.ufo/waves/arc3-loop1-round3/claims/c1/EX-06/evidence/'
R1 = '.ufo/waves/arc3-loop1-round1/claims/c1/'
X7 = '.ufo/waves/arc3-loop1-round3/claims/c1/EX-07/'

def load(f):
    d = json.load(open(f))
    if isinstance(d, dict) and 'ok' in d and 'data' in d and 'meta' in d:
        return d['data'], d
    return d, None

def norm(d):
    d = json.loads(json.dumps(d))
    d.pop('evidence_id', None)
    d.get('subject', {}).pop('local_path', None)
    d.get('normalized_result', {}).get('artifact', {}).pop('path', None)
    for k in ('stdout', 'stderr'):
        d.get('normalized_result', {}).get('diagnostics', {}).pop(k, None)
    d.get('parameters', {}).pop('path', None)
    for loc in d.get('locations', []) or []:
        if isinstance(loc, dict): loc.pop('path', None)
    return d

def diff(a, b, p=''):
    out = []
    if type(a) != type(b): return ['TYPE %s' % p]
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: out.append('ONLY-B %s/%s' % (p, k))
            elif k not in b: out.append('ONLY-A %s/%s' % (p, k))
            else: out += diff(a[k], b[k], p + '/' + k)
    elif isinstance(a, list):
        if len(a) != len(b): return ['LEN %s: %d vs %d' % (p, len(a), len(b))]
        for i, (x, y) in enumerate(zip(a, b)): out += diff(x, y, p + '/%d' % i)
    elif a != b: out.append('VAL %s: %r vs %r' % (p, a, b))
    return out

def sha(f): return hashlib.sha256(open(f, 'rb').read()).hexdigest()

legs = [('carrier-A hex-6.4.0', E+'probe-carrier-A-hex-6.4.0.json'),
        ('carrier-A hex-6.4.0-full', E+'probe-carrierA-hex-6.4.0-full.json'),
        ('carrier-A hex-6.4.0-rerun', E+'probe-carrierA-hex-6.4.0-rerun.json'),
        ('carrier-A hex-6.4.0-altpath', E+'probe-carrierA-hex-6.4.0-altpath.json'),
        ('carrier-A hex-6.7.0', E+'probe-carrierA-hex-6.7.0.json'),
        ('carrier-A hex-6.7.0-full', E+'probe-carrierA-hex-6.7.0-full.json'),
        ('carrier-A raw-6.4.0', E+'probe-carrierA-raw-6.4.0.json'),
        ('EX07 legA hex-6.4.0', X7+'legA-hex-6.4.0.json'),
        ('EX07 legA hex-6.7.0', X7+'legA-hex-6.7.0.json'),
        ('CR1 r1 out-A-hex', R1+'CR-1/evidence/out-A-hex.json'),
        ('EX03carrierA hex-6.4.0', E+'probe-EX03carrierA-hex-6.4.0.json'),
        ('EX03carrierA hex-6.4.0-full', E+'probe-EX03carrierA-hex-6.4.0-full.json'),
        ('EX03carrierA hex-6.7.0', E+'probe-EX03carrierA-hex-6.7.0.json'),
        ('EX03carrierA raw-6.4.0', E+'probe-EX03carrierA-raw-6.4.0.json'),
        ('EX07 legC hex-6.4.0', X7+'legC-hex-6.4.0.json'),
        ('EX07 legC hex-6.7.0', X7+'legC-hex-6.7.0.json'),
        ('EX07 legC raw-6.4.0', X7+'legC-raw-6.4.0.json')]

D = {}
print('== legs ==')
for tag, f in legs:
    d, w = load(f); D[tag] = d
    nr = d['normalized_result']
    fns = [(x['selector'], x['bytecode_offset']) for x in nr['functions']]
    print('%-26s ev=%-14s wrapper=%-5s fns=%-2d bytecode_sha=%s artifact=%sB/%s' % (
        tag, d['evidence_id'][:14], bool(w), len(fns), nr['bytecode']['sha256'][:12],
        nr['artifact']['bytes'], nr['artifact']['encoding']))
print()

print('== planted-K checks (pre-probe records: EX-03/planted-selectors.txt, r1 CR-1 record) ==')
pk_hex = [l.split()[0].lower() for l in open('.ufo/waves/arc3-loop1-round3/claims/c1/EX-03/planted-selectors.txt') if l.startswith('0x')]
planted_control = ['0x095ea7b3', '0x70a08231', '0xa9059cbb']
for tag in ('carrier-A hex-6.4.0', 'carrier-A hex-6.7.0', 'carrier-A raw-6.4.0', 'EX03carrierA hex-6.4.0', 'EX03carrierA hex-6.7.0', 'EX03carrierA raw-6.4.0'):
    got = ['0x' + x['selector'].replace('0x', '') for x in D[tag]['normalized_result']['functions']]
    planted = set(pk_hex) if tag.startswith('EX03') else set(planted_control)
    gs = set(g.lower() for g in got)
    print('%-26s K_planted=%d missing=%s extra=%s' % (tag, len(planted), sorted(planted - gs), sorted(gs - planted)))
print()

print('== normalized diffs vs carrier-A hex-6.4.0 (evidence_id/paths/diagnostics stripped) ==')
base = norm(D['carrier-A hex-6.4.0'])
for tag, _ in legs:
    if tag == 'carrier-A hex-6.4.0' or tag.startswith('EX03') or tag.startswith('EX07 legC'): continue
    dd = diff(base, norm(D[tag]))
    print('%-26s diffs=%-2d %s' % (tag, len(dd), dd[:4]))
print()
print('== EX03 carrierA cross-seat diffs (vs my EX-03 legs) ==')
for mine, theirs in (('EX03carrierA hex-6.4.0', 'EX07 legC hex-6.4.0'),
                     ('EX03carrierA hex-6.7.0', 'EX07 legC hex-6.7.0'),
                     ('EX03carrierA raw-6.4.0', 'EX07 legC raw-6.4.0')):
    dd = diff(norm(D[mine]), norm(D[theirs]))
    print('%-26s vs %-22s diffs=%d %s' % (mine, theirs, len(dd), dd[:3]))
print()

print('== identity checks ==')
print('carrier-A hex-6.4.0 vs rerun raw bytes:', 'IDENTICAL' if sha(E+'probe-carrier-A-hex-6.4.0.json') == sha(E+'probe-carrierA-hex-6.4.0-rerun.json') else 'DIFFER')
print('ids (same path):', D['carrier-A hex-6.4.0']['evidence_id'][:24], '| rerun', D['carrier-A hex-6.4.0-rerun']['evidence_id'][:24], '| full-output', D['carrier-A hex-6.4.0-full']['evidence_id'][:24])
print('id (alt path):   ', D['carrier-A hex-6.4.0-altpath']['evidence_id'][:24])
print('id (6.7.0 pin):  ', D['carrier-A hex-6.7.0']['evidence_id'][:24])
print('id (raw form):   ', D['carrier-A raw-6.4.0']['evidence_id'][:24])
print('id (EX07 CR-1 path replay):', load(X7+'idpath-cr1path-6.4.0.json')[0]['evidence_id'][:24], '== CR-1 r1 id:', load(R1+'CR-1/evidence/out-A-hex.json')[0]['evidence_id'][:24])
print()

print('== id-vs-bytes-at-same-path test ==')
a = load(E+'idtest-bytes-a.json')[0]; b = load(E+'idtest-bytes-b.json')[0]
print('id-a:', a['evidence_id']); print('id-b:', b['evidence_id'])
print('file digest a/b:', a['subject']['digest']['sha256'][:16], b['subject']['digest']['sha256'][:16])
print('decoded bytecode sha a==b:', a['normalized_result']['bytecode']['sha256'] == b['normalized_result']['bytecode']['sha256'])
print()

print('== traps / controls ==')
t = json.load(open(E+'trap-hex-declared-on-bin.json'))
print('hex-on-bin: code=%s issues=%s' % (t.get('code'), t.get('details', {}).get('issues')))
t2 = load(E+'trap-raw-declared-on-hex.json')[0]
print('raw-on-hex: id=%s bytecode_sha=%s bytes=%s fns=%d' % (t2['evidence_id'][:14], t2['normalized_result']['bytecode']['sha256'][:12], t2['normalized_result']['bytecode']['bytes'], len(t2['normalized_result']['functions'])))
t3 = load(E+'trap-tmp-default-edquot.json')[0]
print('TMPDIR=/tmp carrier-A: exit 0; id==baseline:', t3['evidence_id'] == D['carrier-A hex-6.4.0']['evidence_id'])
try:
    t4 = load(E+'trap-tmp-edquot-rv2token-6.4.0.json')[0]
    print('TMPDIR=/tmp Rv2Token: exit 0 envelope; id=', t4['evidence_id'][:14], '(EDQUOT did NOT reproduce)')
except Exception as ex:
    print('TMPDIR=/tmp Rv2Token: parse fail:', ex)
print()

print('== r1 recheck line ==')
print('byte-identical to r1 artifact:', sha(E+'recheck-rv2token-hex-6.4.0.json') == sha(R1+'RV-2/probe-runtime-hex-6.4.0.json'))
r = load(E+'recheck-rv2token-hex-6.4.0.json')[0]
print('id re-derived:', r['evidence_id'], '(r1 file: same bytes)')
print()

print('== planted-K independent disasm (planted-K.json / planted-K-ex03carrierA.json) ==')
pk = json.load(open(E+'planted-K.json'))
print('carrier-A:', pk['push4_sites'], 'decoys_present:', pk['decoys_present'])
pk2 = json.load(open(E+'planted-K-ex03carrierA.json'))
print('EX03 carrierA: push4 sites:', [(s['pc'], s['imm']) for s in pk2['push4_sites']])
print()
print('== PL-1 carrier A (OptVault) legs (third reading) ==')
pl = [('PL1OptVault hex-6.4.0', E+'probe-PL1OptVault-hex-6.4.0.json'),
      ('PL1OptVault hex-6.4.0-full', E+'probe-PL1OptVault-hex-6.4.0-full.json'),
      ('PL1OptVault hex-6.7.0', E+'probe-PL1OptVault-hex-6.7.0.json'),
      ('PL1OptVault raw-6.4.0', E+'probe-PL1OptVault-raw-6.4.0.json')]
plplanted = {'0x16c38b3c', '0x2e1a7d4d', '0x5c975abb', '0x75807250', '0xd0e30db0'}
Dp = {}
for tag, f in pl:
    d, w = load(f); Dp[tag] = d
    got = set('0x' + x['selector'].replace('0x', '').lower() for x in d['normalized_result']['functions'])
    print('%-26s ev=%-14s fns=%d missing=%s extra=%s bytecode_sha=%s' % (
        tag, d['evidence_id'][:14], len(got), sorted(plplanted - got), sorted(got - plplanted),
        d['normalized_result']['bytecode']['sha256'][:12]))
print()
print('== PL1 OptVault cross-seat diffs (mine vs PL-1 prototype envelopes) ==')
for mine, theirs in (('PL1OptVault hex-6.4.0', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/OptVault-6.4.0-hex.json'),
                     ('PL1OptVault raw-6.4.0', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/OptVault-6.4.0-raw.json'),
                     ('PL1OptVault hex-6.7.0', '.ufo/waves/arc3-loop1-round3/claims/c1/PL-1/evidence/OptVault-6.7.0-hex.json')):
    try:
        dd = diff(norm(Dp[mine]), norm(load(theirs)[0]))
        print('%-26s vs %-24s diffs=%d %s' % (mine, theirs.split('/')[-1], len(dd), dd[:3]))
    except Exception as ex:
        print('%-26s vs %-24s FAILED: %s' % (mine, theirs.split('/')[-1], ex))
pk3 = json.load(open(E+'planted-K-pl1OptVault.json'))
print()
print('OptVault disasm:', pk3['prologue'], [(s['pc'], s['imm']) for s in pk3['push4_sites']])