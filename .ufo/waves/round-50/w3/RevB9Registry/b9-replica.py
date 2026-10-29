#!/usr/bin/env python3
"""RevB9Registry hand-replica of c2-record.py atom B9 against the lane at base
f890bbead20ca2c549487167f56876ae47f1e1a4. Read-only: reads lane objects via git.

Mirrors: vis(), cells(), registry_region(), census_paths(), meaning_classes(), b9().
"""
import subprocess, re, json, sys, hashlib

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'f890bbead20ca2c549487167f56876ae47f1e1a4'
COUNTER_BASE = '7c678ae6d97aedb969fd253b52b3d2882ef1e186'  # c2-record.py BASE constant
ATTEMPT1_LANDING = '11ccdb72'  # R50-C2 landing, added 12 registry rows
FREEZE_REC = '845e0586'
REG_OPEN = '<!-- instrument-registry v2 -->'
REG_CLOSE = '<!-- /instrument-registry -->'
CENSUS_BASE_PREFIX = 'tools/round-49'
CENSUS_REV_PREFIX = 'tools/round-50'

SEG = re.compile(r'(?<![0-9])([012])\s*=\s*')
SUCCESS = re.compile(r'\b(met|clean|ok|green|pass|passed|verified|succeeded|wrote)\b')
NOTMET = re.compile(r'(not met|violation|red|fail|failed|no verdict|refusal|refused|unresolved)')
UNEVAL = re.compile(r'(could-not-evaluate|unevaluable|could not evaluate|\busage\b|'
                    r'\berror\b|absent|unreadable|refus)')
NEGATED = re.compile(r'\bnot\s+met\b|\bno\s+verdict\b')
BANANA = re.compile(r'\b(banana|nope|whatever)\b')
FENCE_OPEN = re.compile(r'^ {0,3}(`{3,}|~{3,})')
INLINE_COMMENT = re.compile(r'<!--.*?-->')

def git(*args):
    p = subprocess.run(['git', '-c', 'core.quotePath=false', '-C', LANE] + list(args),
                       capture_output=True)
    if p.returncode != 0:
        raise RuntimeError('git %s -> %r' % (args, p.stderr[:200]))
    return p.stdout

def blob(rev, path):
    p = subprocess.run(['git', '-c', 'core.quotePath=false', '-C', LANE, 'cat-file', 'blob',
                        '%s:%s' % (rev, path)], capture_output=True)
    return p.stdout if p.returncode == 0 else None

def ls_tree(rev, prefix):
    out = git('ls-tree', '-r', '--name-only', rev, '--', prefix)
    return [l.decode('utf-8', 'surrogateescape') for l in out.split(b'\n') if l]

def vis(t, keep=()):
    out, fence, cm = [], None, False
    for ln in t.split('\n'):
        if cm:
            if '-->' in ln:
                cm = False
            out.append('')
            continue
        if fence:
            m = re.match(r'^ {0,3}(`+|~+)[ \t]*$', ln)
            if m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]:
                fence = None
            out.append('')
            continue
        if ln.strip() in keep:
            out.append(ln)
            continue
        m = FENCE_OPEN.match(ln)
        if m:
            fence = (m.group(1)[0], len(m.group(1)))
            out.append('')
            continue
        if re.match(r'^ {0,3}<!--', ln):
            if '-->' not in ln.split('<!--', 1)[1]:
                cm = True
            out.append('')
            continue
        if '<!--' in ln:
            ln = INLINE_COMMENT.sub('\x00', ln)
            if '<!--' in ln:
                ln = ln.split('<!--', 1)[0] + '\x00'
                cm = True
        out.append(ln)
    return '\n'.join(out)

def cells(line):
    c = [x.strip().replace('\x01', '|') for x in line.strip().replace('\\|', '\x01').split('|')]
    return c[1:-1] if len(c) >= 2 else c

def registry_region(t):
    v = vis(t, keep=(REG_OPEN, REG_CLOSE))
    lines = v.split('\n')
    o = [i for i, l in enumerate(lines) if l.strip() == REG_OPEN]
    cl = [i for i, l in enumerate(lines) if l.strip() == REG_CLOSE]
    if len(o) != 1 or len(cl) != 1 or o[0] >= cl[0]:
        return None, 'registry markers absent, doubled or reversed (%d/%d)' % (len(o), len(cl))
    rows = {}
    for l in lines[o[0] + 1:cl[0]]:
        if re.match(r'^ {0,3}\|\s*`', l):
            cs = cells(l)
            rows.setdefault(cs[0].strip('` ') if cs else '', []).append(cs)
    return rows, None

def census_paths(rev_r49, rev_r50):
    def pick(rev, prefix):
        return [p for p in ls_tree(rev, prefix)
                if p.endswith(('.py', '.sh')) and '/control-fixtures/' not in p + '/']
    return pick(rev_r49, CENSUS_BASE_PREFIX) + pick(rev_r50, CENSUS_REV_PREFIX)

def meaning_classes(cell):
    text_ = cell.strip()
    marks = list(SEG.finditer(text_))
    if [m.group(1) for m in marks] != ['0', '1', '2']:
        return 'verdict map does not parse as 0=;1=;2='
    segs = {}
    for i, m in enumerate(marks):
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text_)
        segs[m.group(1)] = text_[m.end():end].strip().rstrip(';').strip().lower()
    if BANANA.search(' '.join(segs.values())):
        return 'placeholder text in the verdict map'
    if not (SUCCESS.search(segs['0']) and not NEGATED.search(segs['0'])):
        return 'exit 0 segment names no success meaning'
    if not NOTMET.search(segs['1']):
        return 'exit 1 segment names no not-met meaning'
    if not UNEVAL.search(segs['2']):
        return 'exit 2 segment names no unevaluable meaning'
    if len(set(segs.values())) != 3:
        return 'verdict segments are not three distinct meanings'
    return None

def b9(rows, paths):
    out = []
    for p in paths:
        got = rows.get(p, [])
        if not got:
            out.append((p, 'no registry row'))
            continue
        if len(got) > 1:
            out.append((p, '%d registry rows, want 1' % len(got)))
            continue
        cs = got[0]
        if len(cs) != 7:
            out.append((p, 'row has %d cells, want 7' % len(cs)))
            continue
        if not re.match(r'(?i)(gate|probe)\b', cs[1]):
            out.append((p, 'kind cell does not open gate|probe: %r' % cs[1][:60]))
        entry = r'(?:python3?|bash|sh|node)\s+(?:-\S+\s+)*(?:\./)?' + re.escape(p) + r'(?![\w./\-])'
        if not any(re.search(entry, x) for x in cs[1:5]):
            out.append((p, 'no entry command naming the path'))
        why = meaning_classes(cs[2])
        if why:
            out.append((p, 'verdict map: %s' % why))
        st = cs[3]
        if not (re.match(r'(?:python3?|bash|sh)\s+(?:-\S+\s+)*(?:\./)?' + re.escape(p) +
                         r'\b.*--selftest', st)
                or re.match(r'none\s*[\u2014\-:;,]\s*\S+(?:\s+\S+){2,}', st)):
            out.append((p, 'self-test cell mismatch: %r' % st[:80]))
        pin = cs[4]
        if not (re.match(r'none\s*[\u2014\-:;,]\s*\S+(?:\s+\S+){1,}', pin)
                or re.search(r'[\w.\-]+/[\w./\-]*|\b[\w\-]+\.(?:json|tsv|md|py|sh|txt|html)\b', pin)):
            out.append((p, 'pinned-value cell names no path and is not `none — <reason>`: %r' % pin[:80]))
    return out

def main():
    sk = blob(BASE, 'SKILL.md').decode('utf-8', 'replace')
    rows, bad = registry_region(sk)
    print('registry_region problem:', bad)
    print('total rows keyed:', len(rows))

    # census at my base (both prefixes from f890bbe)
    paths = census_paths(BASE, BASE)
    print('census paths (%d):' % len(paths))
    for p in paths:
        print('  ', p)

    # also census exactly as the atom would see it with its own constants
    paths_counter = census_paths(COUNTER_BASE, BASE)
    print('census per counter constants (%d):' % len(paths_counter))
    for p in paths_counter:
        print('  ', p)
    if set(paths_counter) - set(paths):
        print('DIFF counter-minus-base:', sorted(set(paths_counter) - set(paths)))
    if set(paths) - set(paths_counter):
        print('DIFF base-minus-counter:', sorted(set(paths) - set(paths_counter)))

    findings = b9(rows, paths_counter)
    print('\nB9 findings (%d):' % len(findings))
    for p, f in findings:
        print('  %s: %s' % (p, f))

    json.dump({'paths': paths_counter, 'findings': findings,
               'row_keys': sorted(rows)},
              open('/fast/scratch/hyaku/kaidoku-r50/w3-RevB9Registry/b9-replica.json', 'w'), indent=1)
    return 0 if not findings else 1

if __name__ == '__main__':
    sys.exit(main())
