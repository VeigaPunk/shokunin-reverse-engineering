# Sweep of a lesson's `## Mistakes` section at BASE (read-only: git show / cat-file / ls-tree).
# Usage: mistake-sweep.py <REV> <ROUND> [root]
# Checks per row: id; class in the CORPUS §5 vocabulary; captured-by cell names an existing QUALITY row
# (`QUALITY row N` or `row N`) or an existing file; evidence-pointer paths resolve at REV.
# Also counts M<round>-n bullets outside the table (prose mistakes the rule says must be rows).
# Exit 0 = every row captured by an existing criterion and every pointer resolves; 1 = a finding; 2 = could not evaluate.
import re, subprocess, sys
rev, rnd = sys.argv[1], sys.argv[2]
root = sys.argv[3] if len(sys.argv) > 3 else '.'
def git(*a):
    return subprocess.run(['git', '-C', root, *a], capture_output=True, text=True)
def show(path):
    r = git('show', f'{rev}:{path}')
    return r.stdout if r.returncode == 0 else None
def exists(path):
    return git('cat-file', '-e', f'{rev}:{path}').returncode == 0
VOCAB = {'vacuous','survivor','stale-premise','reference-drift','number-drift','scope','attribution','landing','provider'}
lesson = show(f'corpus/lessons/round-{rnd}.md')
quality = show('corpus/QUALITY.md')
if lesson is None or quality is None:
    print('could-not-evaluate: lesson or QUALITY absent at rev'); sys.exit(2)
qrows = set(int(m.group(1)) for m in re.finditer(r'^\| (\d+) ', quality, re.M))
sec = re.search(r'^## Mistakes\n(.*?)(?=^## |\Z)', lesson, re.S | re.M)
if not sec: print('no ## Mistakes section'); sys.exit(2)
rows = [l for l in sec.group(1).splitlines() if re.match(r'^\| M%s-\d+ ' % rnd, l)]
bad = 0
print(f'round={rnd} rev={rev[:12]} table_rows={len(rows)} QUALITY_rows={len(qrows)}')
for l in rows:
    cells = [c.strip() for c in l.strip().strip('|').split('|')]
    rid, cls, ptr, cap, fix = (cells + [''] * 5)[:5]
    issues = []
    cls_word = re.sub(r'[`*]', '', cls).split('—')[0].split(' ')[0].strip()
    if cls_word not in VOCAB: issues.append(f'class-not-in-CORPUS-vocab:{cls_word}')
    qs = [int(x) for x in re.findall(r'QUALITY row (\d+)|(?<![\w.])row (\d+)', cap) for x in x if x]
    qs = [int(x) for x in re.findall(r'(?:QUALITY )?row (\d+)', cap)]
    if not qs and 'none' in cap.lower(): issues.append('captured-by:none')
    for q in qs:
        if q not in qrows: issues.append(f'QUALITY-row-{q}-absent')
    paths = set(re.findall(r'`((?:corpus|tools|\.ufo|PROVINCE|SKILL|SCORECARD|LOG)[^`\s]*)`', ptr + ' ' + fix))
    paths |= set(re.findall(r'(?<![\w/])((?:corpus|tools)/[\w./-]+)', ptr))
    for p in sorted(paths):
        p2 = re.sub(r':[0-9][0-9,\-: ]*$', '', p)
        if not exists(p2): issues.append(f'pointer-absent:{p2}')
    for w in sorted(set(re.findall(r'\b(w[12]/[\w.-]+)', ptr))):
        cand = f'.ufo/waves/round-{rnd}/{w}'
        if not exists(cand): issues.append(f'pointer-absent:{cand}')
    status = 'OK' if not issues else 'FINDING'
    bad += bool(issues)
    print(f'{status}\t{rid}\tclass={cls_word}\tcaptured_by={cap[:70]!r}\tissues={issues}')
prose = [l[:40] for l in lesson.splitlines() if re.match(r'^\*\*M%s-\d+' % rnd, l)]
print(f'prose_mistake_bullets_outside_table={len(prose)} {prose}')
if prose: bad += 1
sys.exit(1 if bad else 0)
