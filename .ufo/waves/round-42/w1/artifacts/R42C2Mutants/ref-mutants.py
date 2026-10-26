#!/usr/bin/env python3
"""R42C2Mutants -- A1 new-mutant sweep over the precedence-derived ref harness.

For each NM-I* mutant (one exact-string edit of art/ref-v4.py):
  - the pristine ref must pass its own selftest (baseline), and
  - the mutant must fail the selftest with the expected killing case among the
    failures.  That pair is the evidence that the case belongs in the v4
    interpreter/evaluator selftest.
"""
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
REF = os.path.join(HERE, 'ref-v4.py')
MUT = os.path.join(ROOT, 'muts')
OUT = os.path.join(ROOT, 'out')

S2 = ("    if not F and 'depth-limited' in G:\n"
      "        return ('container-depth-limited', 'raise-depth')                   # 2\n"
      "    if not F:\n"
      "        return ('no-squashfs-chunk', 'inspect-input')                       # 3\n")

MUTANTS = {
    'NM-I1-container-after-nochunk': [(
        S2,
        "    if not F:\n"
        "        return ('no-squashfs-chunk', 'inspect-input')                       # 3\n"
        "    if not F and 'depth-limited' in G:\n"
        "        return ('container-depth-limited', 'raise-depth')                   # 2\n")],
    'NM-I2-container-or': [(
        "    if not F and 'depth-limited' in G:",
        "    if not F or 'depth-limited' in G:")],
    'NM-I3-container-tar-guard': [(
        "    if not F and 'depth-limited' in G:",
        "    if not F and 'depth-limited' in G \\\n"
        "            and all(h.split('_')[0] == 'tar' for h in f['H']):")],
    'NM-I4-hf-to-f': [(
        "            and 'squashfs_v4_be' in HF:",
        "            and 'squashfs_v4_be' in F:")],
    'NM-I5-legacy-exact-names': [(
        "LEGACY_PATTERNS = ('squashfs_v1*', 'squashfs_v2*', 'squashfs_v3*')",
        "LEGACY_PATTERNS = ('squashfs_v1', 'squashfs_v2', 'squashfs_v3')")],
    'NM-I6-legacy-too-wide': [(
        "LEGACY_PATTERNS = ('squashfs_v1*', 'squashfs_v2*', 'squashfs_v3*')",
        "LEGACY_PATTERNS = ('squashfs_v*',)")],
    'NM-I7-residue-after-depth': [(
        "    if 'unknown-chunk-handler' in G:\n"
        "        return ('unknown-residue', 'isolate-residue')                       # 9\n"
        "    if 'depth-limited' in G:\n"
        "        return ('depth-limited', 'raise-depth')                             # 10\n",
        "    if 'depth-limited' in G:\n"
        "        return ('depth-limited', 'raise-depth')                             # 10\n"
        "    if 'unknown-chunk-handler' in G:\n"
        "        return ('unknown-residue', 'isolate-residue')                       # 9\n")],
    'NM-I8-h-chunks-only': [(
        "    for g in gaps:\n"
        "        h = g.get('handler')\n"
        "        if isinstance(h, str):\n"
        "            H.append(h)\n",
        "")],
    'NM-I9-deps-exact-set': [(
        "        if 'sasquatch-v4be' in D:\n"
        "            return ('dep-missing-be', 'install-extractor-be')               # 4\n"
        "        if 'sasquatch' in D:\n"
        "            return ('dep-missing-le', 'install-extractor-le')               # 4",
        "        if D == {'sasquatch-v4be'}:\n"
        "            return ('dep-missing-be', 'install-extractor-be')               # 4\n"
        "        if D == {'sasquatch'}:\n"
        "            return ('dep-missing-le', 'install-extractor-le')               # 4")],
    'NM-I10-container-h-empty': [(
        "    if not F and 'depth-limited' in G:",
        "    if not f['H'] and 'depth-limited' in G:")],
    'NM-I11-glob-args-swapped': [(
        "any(fnmatch.fnmatchcase(h, p) for p in LEGACY_PATTERNS)",
        "any(fnmatch.fnmatchcase(p, h) for p in LEGACY_PATTERNS)")],
    # survivor-analog mutants: the round-41 survivors re-expressed on the A1
    # ref so each survivor's killing case is verified by execution
    'NM-I12-sr-stdout-fallback': [(
        "    SR = any(isinstance(holder, dict) and holder.get('__typename__') == SYMLINK_TYPENAME\n"
        "             for dg in diags if isinstance(dg, dict)\n"
        "             for holder in (dg, dg.get('report') if isinstance(dg.get('report'), dict) else None))\n",
        "    SR = any(isinstance(holder, dict) and holder.get('__typename__') == SYMLINK_TYPENAME\n"
        "             for dg in diags if isinstance(dg, dict)\n"
        "             for holder in (dg, dg.get('report') if isinstance(dg.get('report'), dict) else None))\n"
        "    SR = SR or (SYMLINK_TYPENAME in json.dumps(d.get('raw_result') or {}))\n")],
    'NM-I13-sr-diag-holder-only': [(
        "             for holder in (dg, dg.get('report') if isinstance(dg.get('report'), dict) else None))",
        "             for holder in (dg.get('report') if isinstance(dg.get('report'), dict) else None,))")],
    'NM-I14-p-collapse': [(
        "    P = len(nr['files']) if isinstance(nr.get('files'), list) else 0",
        "    P = 1 if isinstance(nr.get('files'), list) and nr['files'] else 0")],
    'NM-I15-dep-after-partial': [(
        "    if 'missing-extractor-dependency' in G:\n"
        "        if 'sasquatch-v4be' in D:\n"
        "            return ('dep-missing-be', 'install-extractor-be')               # 4\n"
        "        if 'sasquatch' in D:\n"
        "            return ('dep-missing-le', 'install-extractor-le')               # 4\n"
        "    if 'extractor-failure' in G and f['P'] > 0:\n"
        "        return ('partial-body-failure', 'salvage-partial')                  # 5\n",
        "    if 'extractor-failure' in G and f['P'] > 0:\n"
        "        return ('partial-body-failure', 'salvage-partial')                  # 5\n"
        "    if 'missing-extractor-dependency' in G:\n"
        "        if 'sasquatch-v4be' in D:\n"
        "            return ('dep-missing-be', 'install-extractor-be')               # 4\n"
        "        if 'sasquatch' in D:\n"
        "            return ('dep-missing-le', 'install-extractor-le')               # 4\n")],
    'NM-I16-sr-key-type': [(
        "    SR = any(isinstance(holder, dict) and holder.get('__typename__') == SYMLINK_TYPENAME",
        "    SR = any(isinstance(holder, dict) and holder.get('type') == SYMLINK_TYPENAME")],
    'NM-I17-be-substring': [(
        "        BE = 'yes' if any('-be' in c.split() for c in cmds) else 'no'",
        "        BE = 'yes' if any('-be' in c for c in cmds) else 'no'")],
    'NM-I18-na-to-no': [(
        "    else:\n        BE = 'n/a'",
        "    else:\n        BE = 'no'")],
    'NM-I19-p-absent-one': [(
        "    P = len(nr['files']) if isinstance(nr.get('files'), list) else 0",
        "    P = len(nr['files']) if isinstance(nr.get('files'), list) else 1")],
    'NM-I20-f-prefix-dropped': [(
        "    F = sorted({h for h in H if h.startswith('squashfs_')})",
        "    F = sorted(set(H))")],
}

EXPECTED_KILLER = {
    'NM-I1-container-after-nochunk': 's2-container-trx',
    'NM-I2-container-or': 's10-depth',
    'NM-I3-container-tar-guard': 's2-container-trx',
    'NM-I4-hf-to-f': 's6c-hf-trx',
    'NM-I5-legacy-exact-names': 's7-legacy-ddwrt',
    'NM-I6-legacy-too-wide': 's8-v4le-body',
    'NM-I7-residue-after-depth': 's9-residue-plus-depth',
    'NM-I8-h-chunks-only': 's7c-legacy-gap-handler',
    'NM-I9-deps-exact-set': 's4c-dep-membership-le',
    'NM-I10-container-h-empty': 's2-container-trx',
    'NM-I11-glob-args-swapped': 's7-legacy-ddwrt',
    'NM-I12-sr-stdout-fallback': 's12c-stdout-only-sr',
    'NM-I13-sr-diag-holder-only': 's12b-diag-level-holder',
    'NM-I14-p-collapse': 'f-p-counts-every-file',
    'NM-I15-dep-after-partial': 's4e-dep-plus-partial',
    'NM-I16-sr-key-type': 's11-mixed',
    'NM-I17-be-substring': 'f-be-token-not-substring',
    'NM-I18-na-to-no': 's6d-no-argv-avm-blocked',
    'NM-I19-p-absent-one': 'f-p-absent-is-zero',
    'NM-I20-f-prefix-dropped': 's3-no-squashfs',
}


def run(path):
    p = subprocess.run([sys.executable, '-I', '-B', path, '--selftest'],
                       capture_output=True, text=True, timeout=60)
    fails = [l.split()[1].rstrip(':') for l in p.stdout.splitlines()
             if l.startswith('FAIL ')]
    return p.returncode, fails, p.stdout


def main():
    os.makedirs(MUT, exist_ok=True)
    src = open(REF, encoding='utf-8').read()
    rc, fails, out = run(REF)
    pristine_ok = rc == 0 and not fails
    print('pristine: exit=%d %s' % (rc, out.strip().splitlines()[-1] if out else ''))
    rows = [{'probe': 'pristine', 'exit': rc, 'failures': fails, 'ok': pristine_ok}]
    for mid, patches in sorted(MUTANTS.items()):
        msrc = src
        for old, new in patches:
            n = msrc.count(old)
            assert n == 1, '%s anchor x%d for %r' % (mid, n, old[:60])
            msrc = msrc.replace(old, new)
        mp = os.path.join(MUT, 'refv4-%s.py' % mid)
        with open(mp, 'w', encoding='utf-8') as fh:
            fh.write(msrc)
        rc, fails, out = run(mp)
        killed = rc != 0 and EXPECTED_KILLER[mid] in fails
        rows.append({'probe': mid, 'exit': rc, 'failures': fails,
                     'expected_killer': EXPECTED_KILLER[mid], 'killed': killed})
        print('%-30s exit=%d killers=%s expected=%s killed=%s'
              % (mid, rc, fails, EXPECTED_KILLER[mid], killed))
        sys.stdout.flush()
    with open(os.path.join(OUT, 'ref-mutants.json'), 'w') as fh:
        json.dump(rows, fh, indent=1, sort_keys=True)
    print('DONE pristine_ok=%s all_killed=%s'
          % (pristine_ok, all(r.get('killed') for r in rows[1:])))


if __name__ == '__main__':
    main()
