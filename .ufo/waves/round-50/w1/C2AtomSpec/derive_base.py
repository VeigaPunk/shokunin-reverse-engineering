#!/usr/bin/env python3
"""C2AtomSpec: derive, read-only through git objects, the value the round-48/49 record states
and the value the committed bytes give for each R50-C2 atom B1..B11 at a base revision.
Usage: python3 -I -B derive_base.py --root LANE --rev REV   (stdout: JSON; exit 0 always)
Reads only `git show/ls-tree/cat-file/merge-base`; writes nothing."""
import argparse, hashlib, html, json, re, subprocess, sys

ap = argparse.ArgumentParser(); ap.add_argument('--root', required=True); ap.add_argument('--rev', required=True)
a = ap.parse_args(); L, REV = a.root, a.rev

def g(*args, check=True):
    p = subprocess.run(['git', '-C', L, '-c', 'core.quotePath=false', *args], capture_output=True)
    if check and p.returncode: raise RuntimeError(p.stderr.decode())
    return p
def show(path, rev=None):
    p = g('show', '%s:%s' % (rev or REV, path), check=False)
    return p.stdout if p.returncode == 0 else None
def txt(path, rev=None):
    b = show(path, rev); return b.decode() if b is not None else None
def ls(prefix, rev=None):
    return [x for x in g('ls-tree', '-r', '--name-only', rev or REV, '--', prefix).stdout.decode().split('\n') if x]
def sha(b): return hashlib.sha256(b).hexdigest()
def lines(path): return (txt(path) or '').split('\n')
def lno(path, pred): return [i + 1 for i, l in enumerate(lines(path)) if pred(l)]

out = {'rev': REV}
sc = lines('SCORECARD.md')

# ---- B1 coverage fraction
kn = [p for p in ls('corpus/knowledge') if p.endswith('.md')]
stems = {p.rsplit('/', 1)[1][:-3] for p in kn}
rd = txt('corpus/README.md'); sec = re.search(r'^## Coverage map\n(.*?)(?=^## )', rd, re.S | re.M).group(1)
mapped = stems & set(re.findall(r'2026-10-\d{2}-[a-z0-9-]+', sec))
row = [(i + 1, l) for i, l in enumerate(sc) if l.startswith('| coverage |')][0]
m = re.search(r'(\d+)/(\d+) knowledge files mapped', row[1])
out['B1'] = {'record': {'file_line': 'SCORECARD.md:%d' % row[0], 'stated': '%s/%s' % m.groups()},
             'derived': {'mapped': len(mapped), 'files': len(kn)}, 'missing': sorted(stems - mapped),
             'red': (int(m.group(1)), int(m.group(2))) != (len(mapped), len(kn))}

# ---- B2 calibration row cites round-48 verdict + round-49 c2-final
crow = [(i + 1, l) for i, l in enumerate(sc) if l.startswith('| calibration |')][0]
fin = json.loads(show('.ufo/waves/round-49/l1/scores/c2-final.json'))
ctl = json.loads(show('.ufo/waves/round-49/controls/ctl-c2-0-do-nothing.json'))
out['B2'] = {'record': {'file_line': 'SCORECARD.md:%d' % crow[0],
                        'has_rejected_harmed': 'rejected-harmed' in crow[1],
                        'has_c2_final': 'c2-final' in crow[1], 'has_round48_closure_path': 'round-48-verifier-spotcheck' in crow[1]},
             'derived': {'closure_admission': re.search(r'Admission: \*\*([a-z-]+)\*\*', txt('corpus/lessons/round-48-verifier-spotcheck.md')).group(1),
                         'c2_final': {k: fin.get(k) for k in ('rev', 'freeze', 'atoms_total', 'mismatches', 'exit_code')},
                         'c2_freeze_control': {k: ctl.get(k) for k in ('mismatches', 'exit_code')},
                         'c2_final_sha256': sha(show('.ufo/waves/round-49/l1/scores/c2-final.json'))},
             'red': not ('rejected-harmed' in crow[1] and 'c2-final' in crow[1])}

# ---- B3 seats settled
res = json.loads(show('.ufo/waves/round-48/r48-w1-results.json'))['results']
blocked, aborted = [], []
for r in res:
    j = json.loads(r['output'])
    if str(j.get('status', '')).strip().lower() == 'blocked': blocked.append(r['name'])
    if j.get('aborted') is True: aborted.append(r['name'])
w1 = ls('.ufo/waves/round-48/w1')
def has_report(seat):
    return any(p == '.ufo/waves/round-48/w1/%s.md' % seat or (p.startswith('.ufo/waves/round-48/w1/%s/' % seat) and p.endswith('.md')) for p in w1)
names = [r['name'] for r in res]
reports = [n for n in names if has_report(n)]
l3 = lno('SCORECARD.md', lambda l: 'all 75 seats settled' in l)
l3b = lno('LOG.md', lambda l: '0 dead seats' in l)
out['B3'] = {'record': {'SCORECARD': ['SCORECARD.md:%d' % x for x in l3], 'LOG': ['LOG.md:%d' % x for x in l3b]},
             'derived': {'results': len(res), 'blocked': blocked, 'aborted': aborted,
                         'completed': len(res) - len(blocked) - len(aborted), 'reports': len(reports),
                         'no_report': sorted(set(names) - set(reports))},
             'red': bool(l3) and (blocked != [] or aborted != [])}

# ---- B4 round-48 per-axis verdicts
clo = txt('corpus/lessons/round-48-verifier-spotcheck.md')
tv = clo.split('## Trend verdicts', 1)[1].split('\n## ', 1)[0]
cv = dict((k, v.strip()) for k, v in re.findall(r'^- \*\*(\w+)\s*[—:-]+\s*([^*]+?)\.?\*\*', tv, re.M))
r48 = txt('SCORECARD.md').split('## Round 48 ', 1)[1].split('\n## ', 1)[0]
tl = [l for l in r48.split('\n') if l.startswith('Learning trends:')]
rec = dict(re.findall(r'(expansion|quality|discernment) \*\*([^*]+)\*\*', tl[0])) if tl else {}
h48 = lno('SCORECARD.md', lambda l: l.startswith('## Round 48 '))[0]
l4 = [x for x in lno('SCORECARD.md', lambda l: l.startswith('Learning trends:') and 'improved on the instruments' in l) if x > h48]
out['B4'] = {'record': {'line': ['SCORECARD.md:%d' % x for x in l4], 'trends': rec},
             'derived': {'closure_trends': cv, 'closure_lines': lno('corpus/lessons/round-48-verifier-spotcheck.md', lambda l: l.startswith('- **') and ' — ' in l[:30])},
             'red': any(rec.get(k, '').split()[0] != cv.get(k, '').split()[0] for k in ('expansion', 'quality', 'discernment'))}

# ---- B5 final receipts named
tip, fin48 = '8847042a140b044dbf335210c965bf7b06b09b4f', '33f65a913cfd21a4491a4f8b7ccc8f00069f058d'
rc = {}
for k in ('c1', 'c2'):
    p = '.ufo/waves/round-48/l1/scores/%s-final-33f65a91.json' % k; b = show(p)
    rc[k] = {'path': p, 'sha256': sha(b), 'sha256_stripped': sha(b.rstrip(b'\n')), 'rev': json.loads(b).get('rev'), 'freeze': json.loads(b).get('freeze')}
out['B5'] = {'record': {'SCORECARD_hits_33f65a91_or_8847042a': len(lno('SCORECARD.md', lambda l: '33f65a91' in l or '8847042a' in l)),
                        'LOG_lines_33f65a91': lno('LOG.md', lambda l: '33f65a91' in l), 'LOG_lines_8847042a': lno('LOG.md', lambda l: '8847042a' in l)},
             'derived': {'receipts': rc, 'final_is_ancestor_of_tip': g('merge-base', '--is-ancestor', fin48, tip, check=False).returncode == 0,
                         'tip_is_ancestor_of_rev': g('merge-base', '--is-ancestor', tip, REV, check=False).returncode == 0},
             'red': len(lno('SCORECARD.md', lambda l: '33f65a91' in l or '8847042a' in l)) == 0}

# ---- registry rows
def reg_rows():
    t = txt('corpus/SOURCES.md'); rows = {}
    for i, l in enumerate(t.split('\n')):
        if re.match(r'^ {0,3}\|\s*S\d{3,}\s*\|', l):
            c = [x.strip() for x in l.strip().strip('|').split('|')]
            if len(c) == 11: rows[c[0]] = dict(zip(('id', 'source', 'kind', 'tier', 'scope', 'anchor', 'teaches', 'status', 'opened', 'recheck', 'used_by'), c), line=i + 1)
    return rows
R = reg_rows()
def supers(n): return [k for k, v in R.items() if re.search(r'supersedes %s\b' % n, v['teaches'])]
def html_norm(b, anchors=False):
    t = b.decode('utf-8', 'replace'); t = re.sub(r'(?is)<script.*?</script>|<style.*?</style>', ' ', t)
    t = re.sub(r'(?is)<h([23])[^>]*>(.*?)</h\1>', lambda m: ' \x01' + re.sub(r'(?s)<[^>]*>', '', m.group(2)) + '\x02 ', t)
    if anchors: t = re.sub(r'(?is)<a id="([A-Za-z_ ]+)" href="#end"><b>.*?</b></a>', lambda m: ' \x01' + m.group(1) + '\x02 ', t)
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'(?s)<[^>]*>', '', t)))
def where(norm, q):
    idx = [m.start() for m in re.finditer(re.escape(q), norm)]
    best = None
    for mm in re.finditer('\x01(.*?)\x02', norm):
        if idx and mm.start() < idx[0]: best = mm.group(1).strip()
    return len(idx), best

# ---- B6 S149
fb = show('corpus/evidence/round-49/c2/freebsd-sysexits.html'); nfb = html_norm(fb, anchors=True)
n, sect = where(nfb, 'EX_USAGE (64) The command was used incorrectly')
hist = re.search(r'HISTORY\x02 (.{0,80})', nfb)
s149 = R['S149']
out['B6'] = {'record': {'row': 'corpus/SOURCES.md:%d' % s149['line'], 'status': s149['status'], 'tier': s149['tier'],
                        'anchor_names_DESCRIPTION': 'DESCRIPTION' in s149['anchor'], 'teaches_inverted_provenance': 'second mirror' in s149['teaches'],
                        'rows_superseding_S149': supers('S149')},
             'derived': {'snapshot_sha256': sha(fb), 'quote_hits': n, 'quote_section': sect, 'history_text': hist.group(1) if hist else None,
                         'linux_snapshot_history': re.search(r'HISTORY top\x02 (.{0,70})', html_norm(show('corpus/evidence/round-49/c2/sysexits.html'))).group(1)},
             'red': 'DESCRIPTION' in s149['anchor'] and sect == 'ERRORS' and not supers('S149')}

# ---- B7 S147
po = show('corpus/evidence/round-49/c2/popper.html'); npo = html_norm(po)
q1 = 'falsifiability as his criterion for demarcating science from non-science: if a theory is incompatible with possible empirical observations it is scientific'
q2 = 'it is consistent with all possible observations, is unscientific'
n1, s1 = where(npo, q1); n2, s2 = where(npo, q2)
s147 = R['S147']; ct = txt('corpus/lessons/round-49-verifier-spotcheck.md')
out['B7'] = {'record': {'row': 'corpus/SOURCES.md:%d' % s147['line'], 'kind': s147['kind'], 'tier': s147['tier'], 'rows_superseding_S147': supers('S147')},
             'derived': {'snapshot_sha256': sha(po), 'q1': [n1, s1], 'q2': [n2, s2], 'q1_words': len(q1.split()), 'q2_words': len(q2.split()),
                         'closure_says_B': 'puts at **B**' in ct and 'disagree tier A' in ct, 'closure_line': lno('corpus/lessons/round-49-verifier-spotcheck.md', lambda l: l.startswith('| S147 '))},
             'red': s147['tier'] == 'A' and not supers('S147')}

# ---- B8 S138
mf = json.loads(show('corpus/evidence/round-44/oracle/manifest.json'))
lst = [p for p in ls('.ufo/waves/round-44/w1/R44SrcOracle/listings') if 'bin_extract' in p]
tot = sum(sum(1 for e in json.loads(show(p))['entries'] if e['type'] == 'file') for p in lst)
tree = [p for p in ls('corpus/evidence/round-44/oracle') if not p.endswith('manifest.json')]
okhash = sum(sha(show(f['local_path'])) == f['sha256'] for f in mf['files'])
s138 = R['S138']
out['B8'] = {'record': {'row': 'corpus/SOURCES.md:%d' % s138['line'], 'status': s138['status'], 'says_22': '22 files' in s138['teaches'] or '22 members' in s138['anchor'],
                        'rows_superseding_S138': supers('S138'), 'anchor_quote': re.findall(r'"[^"]+"', s138['anchor'])[:1]},
             'derived': {'manifest_files': len(mf['files']), 'distinct_sha256': len({f['sha256'] for f in mf['files']}), 'bytes': sum(f['bytes'] for f in mf['files']),
                         'tree_files': len(tree), 'extract_listings': len(lst), 'listing_file_entries': tot, 'local_sha_matches': okhash,
                         'manifest_sha256': sha(show('corpus/evidence/round-44/oracle/manifest.json'))},
             'red': not supers('S138')}

# ---- B9 registry census
sk = txt('SKILL.md'); o, c = '<!-- instrument-registry v2 -->', '<!-- /instrument-registry -->'
body = sk.split(o, 1)[1].split(c, 1)[0]
cell0 = {}
for l in body.split('\n'):
    if l.startswith('|'):
        cs = [x.strip() for x in l.strip().strip('|').split('|')]
        mm = re.fullmatch(r'`(tools/[^`]+)`', cs[0])
        if mm: cell0.setdefault(mm.group(1), []).append(cs)
r49 = [p for p in ls('tools/round-49') if p.endswith(('.py', '.sh'))]
allp = [p for n in range(41, 50) for p in ls('tools/round-%d' % n) if p.endswith(('.py', '.sh'))]
loc = lno('SKILL.md', lambda l: l.startswith('## Local round-evidence gate registry'))
out['B9'] = {'record': {'marker_block_rows': len(cell0), 'local_registry_heading_line': loc, 'markers': [sk.count(o), sk.count(c)]},
             'derived': {'round49_py_sh': r49, 'round49_missing_row': [p for p in r49 if p not in cell0], 'round41_49_missing_row': [p for p in allp if p not in cell0]},
             'red': any(p not in cell0 for p in r49)}

# ---- B10 selftest
cm = txt('tools/round-49/c2-mismatch.py')
out['B10'] = {'record': {'selftest_script_at_rev': show('tools/round-50/selftest-r49-c2.py') is not None, 'c2_mismatch_has_--selftest': '--selftest' in cm,
                         'registry_row_for_c2_mismatch': 'tools/round-49/c2-mismatch.py' in cell0},
              'derived': {'c2_mismatch_sha256': sha(cm.encode()), 'argparse_flags': re.findall(r"add_argument\('(--[a-z0-9-]+)'", cm)},
              'red': show('tools/round-50/selftest-r49-c2.py') is None}

# ---- B11 guard (declared freeze) and the red replacement (round-49 trend line vs closure)
les = txt('corpus/lessons/round-49.md'); fr = txt('.ufo/waves/round-49/l1/FREEZE').strip()
h = lambda t: sorted(set(re.findall(r'Declared freeze:?\*{0,2}\s*`([0-9a-f]{40})`', t)))
decl = {'lesson': h(les), 'scorecard_r49': h(txt('SCORECARD.md').split('## Round 49 ', 1)[1].split('\n## ', 1)[0]), 'FREEZE_file': fr,
        'LOG_round49': sorted(set(re.findall(r'\*\*Freeze:\*\* `([0-9a-f]{40})`', txt('LOG.md').split('round 49 (KaidokuR49)', 1)[1])))}
agree = all(v == [fr] or v == fr for v in decl.values())
c49 = txt('corpus/lessons/round-49-verifier-spotcheck.md').split('## Trend verdicts', 1)[1].split('\n## ', 1)[0]
cv49 = dict((k, v.strip()) for k, v in re.findall(r'^- \*\*(\w+)\s*[:—-]+\s*([^*]+?)\.?\*\*', c49, re.M))
r49s = txt('SCORECARD.md').split('## Round 49 ', 1)[1].split('\n## ', 1)[0]
tl49 = [l for l in r49s.split('\n') if l.startswith('Learning trends:')][0]
rec49 = dict(re.findall(r'(expansion|quality|discernment) \*\*([^*]+)\*\*', tl49))
out['B11_guard_declared_freeze'] = {'declared': decl, 'agree': agree, 'red': not agree,
    'seats': {'lesson_says': '48 + 40 = 88', 'results_json': [len(json.loads(show('.ufo/waves/round-49/r49-w1-results.json'))['results']), len(json.loads(show('.ufo/waves/round-49/r49-w2-results.json'))['results'])]}}
out['B11_replacement_r49_trends'] = {'record': {'line': 'SCORECARD.md:%d' % lno('SCORECARD.md', lambda l: l == tl49)[0], 'trends': rec49, 'says_spotcheck_pending': 'spot-check is pending' in tl49},
    'derived': {'closure_trends': cv49}, 'red': any(rec49[k].split()[0] != cv49[k].split()[0] for k in ('expansion', 'quality', 'discernment'))}
print(json.dumps(out, indent=1, sort_keys=True, ensure_ascii=False))
