import sys, os, json, subprocess, glob
sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r49/W2C2Forge')
import forge as f
from forge import g, wr, C, R, F, ENV, ctr, commit, OUT, S
src = subprocess.run(['git', '-C', C, 'show', F + ':tools/round-49/c2-mismatch.py'], capture_output=True, env=ENV).stdout.decode()
M = [
 ('M01', 'A2 dead-is-commit check', "if r.is_commit(dead):", "if False:"),
 ('M02', 'A2 real-is-ancestor check', "elif not r.ancestor(real, rev):", "elif False:"),
 ('M03', 'A2 8-hex prefix check', "if dead[:8] != real[:8] or dead == real:", "if False:"),
 ('M04', 'A2 dead quoted in closure', "if dead not in text(r.show(LANE_BASE, CLOSURE)):", "if False:"),
 ('M05', 'A3 stated vs derived line numbers', "if not got or sorted(want) != got:", "if False:"),
 ('M06', 'A3 key set equality', "if keys != sorted(LOG_KEYS):", "if False:"),
 ('M07', 'A3 unnamed set equality', "if un != sorted(UNNAMED):", "if False:"),
 ('M08', 'A3 unnamed-hash named-in-base', "        if base is not None and line_numbers(base, h):", "        if False:"),
 ('M09', 'A3 LOG append-only (startswith)', "if base is None or now is None or not now.startswith(base):", "if False:"),
 ('M10', 'A4 seats count', "    if d.get('seats') != str(len(names)):", "    if False:"),
 ('M11', 'A4 missing set', "if sorted(x for x in d.get('missing', '').split(',') if x) != sorted(missing):", "if False:"),
 ('M12', 'A5 stripped digest', "if d.get(k + '_stripped') != stripped:", "if False:"),
 ('M13', 'A5 report prefix', "if len(q) != 8 or stripped[:8] != q or raw[:8] == q:", "if False:"),
 ('M14', 'A5 report in closure', "if q and q not in closure:", "if False:"),
 ('M15', 'A6 snapshot pin', "if sha(b) not in HEX64.findall(c[5]):", "if False:"),
 ('M16', 'A6/A7 25-word limit', "if n > 25:", "if False:"),
 ('M17', 'A6/A7 stated word count', "if stated is None or stated != n:", "if False:"),
 ('M18', 'A6 locator heading', "if not head or head not in c[5]:", "if False:"),
 ('M19', 'A7 EX_USAGE 64 in snapshot', "if 'EX_USAGE 64' not in norm:", "if False:"),
 ('M20', 'A7 teaches (both regexes)', "if not re.search(r'EX_USAGE is 64\\b', c[6]) or re.search(r'EX_USAGE is (?!64\\b)\\S', c[6]):", "if False:"),
 ('M21', 'A7 teaches second-status regex only', "or re.search(r'EX_USAGE is (?!64\\b)\\S', c[6]):", "or False:"),
 ('M22', 'A8 round-48 late entry count', "if len(ent) != 1:", "if False:"),
 ('M23', 'A8 screened/identified relations', "if (inc, exc) != want[2:] or scr != inc + exc or idn < scr:", "if (inc, exc) != want[2:]:"),
 ('M24', 'A8 exclusion reason', "if want[3] > 0 and 'exclusion:' not in low:", "if False:"),
 ('M25', 'A8 rows B->A', "if (int(n.group(1)), int(n.group(2))) != want[:2]:", "if False:"),
 ('M26', 'A8 where-searched/stop tokens', "for token in ('where searched:', 'stop:'):", "for token in ():"),
 ('M27', 'A9 one-line exact', "if len(hits) != 1 or hits[0].strip() != want:", "if False:"),
 ('M28', 'A9 closure calibration row', "if not re.search(r'\\|\\s*calibration\\s*\\|\\s*harmed\\s*\\|', src):", "if False:"),
 ('M29', 'A1 stale = lesson header', "if d.get('stale') != stale:", "if False:"),
 ('M30', 'A1 LOG final-freeze text', "if declared_sc and ('final declared freeze `%s`' % declared_sc) not in text(r.show(LANE_BASE, 'LOG.md')):", "if False:"),
 ('M31', 'A1 round-48 lesson base-identity', "if les is None or base is None or sha(les) != sha(base):", "if False:"),
 ('M32', 'A1 closure names declared', "if declared_sc and declared_sc[:8] not in text(r.show(LANE_BASE, CLOSURE)):", "if False:"),
 ('M33', 'A1 declared == SCORECARD', "if d.get('declared') != declared_sc:", "if False:"),
 ('M34', 'A1 both hashes are commits', "if not (h and HEX40.fullmatch(h) and r.is_commit(h)):", "if False:"),
 ('M35', 'A6 registry rows append-only (S145/S146)', "if old not in rows or rows.get(old) != base_rows.get(old):", "if False:"),
 ('M36', 'A6/A7 duplicate registry ids', "if rid in rdup or old in rdup:", "if False:"),
 ('M37', 'A6/A7 used-by lesson', "if LESSON not in c[10] or r.show(rev, LESSON) is None:", "if False:"),
 ('M38', 'A6 lesson row= names row', "if d.get('row') != rid:", "if False:"),
 ('M39', 'quote presence in snapshot', "if qn not in norm:", "if False:"),
 ('M40', 'freeze: touched-path walk', "    if t:", "    if False:"),
 ('M41', 'battery: do-nothing red check', "if red != sorted(ATOM_IDS):", "if False:"),
 ('M42', 'battery: mutation ok predicate', "ok = red == [atom] and not noop", "ok = True"),
 ('M43', 'battery exit gate', "if b['failing']:", "if False:"),
 ('M44', 'do-nothing overlay is the genuine REV (control)', "dn = score(Overlay(r, rev, {x: r.show(freeze, x) for x in changed}), rev)", "dn = score(r, rev)"),
]
def mk(label, text):
    return text
if __name__ == '__main__':
    rows = []
    which = sys.argv[1:]
    for mid, desc, old, new in M:
        if which and mid not in which: continue
        n = src.count(old)
        if n != 1:
            print(mid, 'PATTERN COUNT', n); rows.append(dict(id=mid, desc=desc, error='pattern count %d' % n)); continue
        m = src.replace(old, new)
        mp = os.path.join(S, 'mut', mid + '.py'); open(mp, 'w').write(m)
        # freeze chain: X = FREEZE + mutant counter ; Y = X + landed tree from REV (same as the rest of the matrix)
        f.reset_to = None
        g('checkout', '-q', '-f', '--detach', F); g('clean', '-fdq')
        wr('tools/round-49/c2-mismatch.py', m)
        X = commit('mutant ' + mid)
        paths = [p for p in g('diff', '--name-only', F, R).stdout.decode().split('\n') if p and not p.startswith('tools/round-49') and not p.startswith('plans/')]
        g('checkout', '-q', R, '--', *paths)
        Y = commit('landed tree on mutant ' + mid)
        b = ctr('HEAD', X, True, ctrpath=mp, tag='mut-' + mid)
        survived = b['exit'] == 0
        rows.append(dict(id=mid, desc=desc, X=X, Y=Y, battery_run=b, survives_genuine_REV=survived))
        print(mid, 'exit', b['exit'], 'mism', b['mismatches'], 'bat', b['battery_failing'], 'reason', b['reason'], '| SURVIVES' if survived else '| killed', '|', desc)
    json.dump(rows, open(os.path.join(OUT, 'mutants-genuine.json'), 'w'), indent=1, default=str)
