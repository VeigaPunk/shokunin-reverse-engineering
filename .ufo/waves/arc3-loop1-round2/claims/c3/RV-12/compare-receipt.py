#!/usr/bin/env python3
"""RV-12 independent receipt comparator.

Parses any custody receipt (v1 sha256-list form, v1 block form, or v2 field form)
and compares it against a baseline capture produced by capture-5path.sh.

Checks, per path:
  - sha256 equal to baseline
  - mtime_epoch equal (if the receipt carries an epoch)
  - any time rendered under a *_UTC label equals the epoch-derived UTC rendering
  - inode/ctime present (v2 requirement; reported, not fatal for v1)
Exit 0 iff no FAIL among sha256/epoch/label checks.
"""
import re, subprocess, sys, datetime

SHA = re.compile(r'\b([0-9a-f]{64})\b')
EPOCH = re.compile(r'\b(1[0-9]{9})\b')
UTCSTAMP = re.compile(r'(\d{4}-\d{2}-\d{2})[T ](\d{2}:\d{2}:\d{2})Z?')

def load_baseline(path):
    base = {}
    for line in open(path):
        if '|' not in line or line.startswith('#'):
            continue
        parts = [p.strip() for p in line.split('|')]
        if len(parts) < 6 or not parts[0].startswith('/'):
            continue
        base[parts[0]] = {
            'sha256': parts[1], 'size': parts[2], 'inode': parts[3],
            'mtime_epoch': parts[4], 'ctime_epoch': parts[5],
        }
    return base

def load_receipt(path):
    """Return {filepath: {'sha256':..., 'mtimes':[(epoch, rendered_or_None, utc_labeled_bool)], 'inode':.., 'ctime':..}}"""
    found = {}
    cur = None
    def slot(p):
        return found.setdefault(p, {'sha256': None, 'mtime_epochs': [], 'ctime_epochs': [],
                                    'utc_renders': [], 'inode': None, 'ctime_renders': []})
    for raw in open(path, errors='replace'):
        line = raw.rstrip('\n')
        # path detection: absolute path token, or sticky from a previous PATH: line
        m = re.search(r'(/home/[^\s|,]+|/root/[^\s|,]+)', line)
        p = m.group(1) if m else None
        # compact sha256sum line
        m2 = re.match(r'^([0-9a-f]{64})\s+(/\S+)$', line.strip())
        if m2:
            s = slot(m2.group(2)); s['sha256'] = m2.group(1); cur = m2.group(2); continue
        mp = re.match(r'^\s*(?:PATH|path|FILE|file)\s*[:=]\s*(\S+)', line)
        if mp:
            cur = mp.group(1)
            p = cur
        if p is None:
            if cur is None:
                continue
            p = cur  # attribute path-less field lines to the current path block
        s = slot(p)
        h = SHA.search(line)
        if h and 'SHA256' in line.upper() or (h and line.strip().startswith(h.group(1))):
            s['sha256'] = h.group(1)
        up = line.upper()
        if 'INODE' in up or re.search(r'\|\s*\d+\s*\|', line):
            for cand in re.findall(r'\|\s*(\d{4,})\s*\|', line):
                s['inode'] = cand
        if 'MTIME' in up and 'UTC' in up and 'LOCAL' not in up:
            for e in EPOCH.findall(line):
                s['mtime_epochs'].append(e)
            for t in UTCSTAMP.finditer(line):
                s['utc_renders'].append((t.group(1), t.group(2)))
        if 'CTIME' in up and 'UTC' in up and 'LOCAL' not in up:
            for e in EPOCH.findall(line):
                s['ctime_epochs'].append(e)
            for t in UTCSTAMP.finditer(line):
                s['ctime_renders'].append((t.group(1), t.group(2)))
    return found

def epoch_to_utc(e):
    return datetime.datetime.fromtimestamp(int(e), datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

def epoch_to_local(e):
    return datetime.datetime.fromtimestamp(int(e)).strftime('%Y-%m-%d %H:%M:%S')

def label_check(p, b, r, fails, oks):
    """Any time rendered on a line labelled *UTC* must equal the epoch-derived UTC."""
    for (d, t) in r['utc_renders']:
        rendered = f'{d} {t}'
        exp_utc = epoch_to_utc(b['mtime_epoch'])
        exp_loc = epoch_to_local(b['mtime_epoch'])
        if rendered == exp_utc:
            oks.append(f'utc-label ok {p.split("/")[-1]} :: {rendered}')
        elif rendered == exp_loc:
            fails.append(f'UTC-LABEL-DEFECT {p}: {rendered} is the LOCAL (-0300) rendering '
                         f'of epoch {b["mtime_epoch"]}; true UTC is {exp_utc}')
        else:
            fails.append(f'UTC-LABEL-UNMATCHED {p}: rendered={rendered} '
                         f'epoch-utc={exp_utc} epoch-local={exp_loc}')

def main(baseline_path, receipt_path):
    base = load_baseline(baseline_path)
    rec = load_receipt(receipt_path)
    fails, warns, oks = [], [], []
    for p, b in base.items():
        r = rec.get(p)
        if r is None:
            warns.append(f'MISSING-IN-RECEIPT {p}')
            continue
        if r['sha256'] is None:
            warns.append(f'NO-SHA-IN-RECEIPT {p}')
        elif r['sha256'] != b['sha256']:
            fails.append(f'SHA-DRIFT {p}: receipt={r["sha256"][:12]}… baseline={b["sha256"][:12]}…')
        else:
            oks.append(f'sha256 ok {p.split("/")[-1]}')
        for e in r['mtime_epochs']:
            if e != b['mtime_epoch']:
                fails.append(f'MTIME-EPOCH-DRIFT {p}: receipt={e} baseline={b["mtime_epoch"]}')
        label_check(p, b, r, fails, oks)
    # v2 fields
    inode_ct = sum(1 for p in rec if rec[p]['inode'])
    print(f'baseline paths: {len(base)}  receipt paths: {len(rec)}  inode-carrying rows: {inode_ct}')
    for o in oks: print('OK   ' + o)
    for w in warns: print('WARN ' + w)
    for f in fails: print('FAIL ' + f)
    print(f'VERDICT: {"PASS" if not fails else "FAIL"} ({len(oks)} ok, {len(warns)} warn, {len(fails)} fail)')
    return 1 if fails else 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1], sys.argv[2]))
