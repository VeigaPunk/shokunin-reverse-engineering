#!/usr/bin/env python3
"""Independent re-read of round-43 C1 committed bytes (read-only on the lane)."""
import hashlib
import json
import subprocess
import sys
import os

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
REV = '77d196c66f4fea00d7d543728b190ebdfaf6d0f0'
FREEZE = 'f3f8db389416d094b1ddeb1215ddcf914bfc0d1c'
ANCHOR = 'd1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b'
MANIFEST = 'corpus/evidence/round-43/c1/heldout/manifest.json'


def git(*args, binary=True):
    p = subprocess.run(['git', '-C', LANE] + list(args), capture_output=True)
    return p.returncode, (p.stdout if binary else p.stdout.decode('utf-8', 'replace'))


def blob(rev, path):
    rc, out = git('cat-file', 'blob', '%s:%s' % (rev, path))
    return out if rc == 0 else None


def sha(b):
    return hashlib.sha256(b).hexdigest() if b is not None else None


def subset(d, keys):
    return {k: d.get(k) for k in keys}


DECL_ARGS = {'handler', 'operation', 'provider', 'parameters'}


def shape_of(data):
    """Independent re-implementation of the six-field observed tuple."""
    norm = data.get('normalized_result') or {}
    chunks = norm.get('chunks') or []
    gaps = norm.get('extraction_gaps') or []
    diags = [d.get('report') or {} for d in (norm.get('diagnostics') or [])]
    handlers = sorted({c.get('handler') for c in chunks if c.get('handler')})
    gap_kinds = sorted({g.get('kind') for g in gaps if g.get('kind')})
    deps = sorted({dep for g in gaps for dep in (g.get('dependencies') or [])})
    be = 'n/a'
    seen = False
    for d in diags:
        cmd = d.get('command')
        if not cmd:
            continue
        toks = cmd.split()
        if not toks:
            continue
        base = os.path.basename(toks[0])
        if base.startswith('sasquatch') or base.startswith('unsquashfs'):
            seen = True
            if '-be' in toks[1:]:
                be = 'yes'
                break
    if be != 'yes' and seen:
        be = 'no'
    sr = any(d.get('__typename__') == 'MaliciousSymlinkRemoved' for d in diags)
    files = len(norm.get('files') or [])
    return {'handler_set': handlers, 'gap_kinds': gap_kinds,
            'gap_dependencies': deps, 'be_argv': be,
            'symlink_removed': sr,
            'published': 'nonzero' if files else 'zero'}


def main():
    rc, text = git('show', '%s:%s' % (REV, MANIFEST), binary=False)
    assert rc == 0
    man = json.loads(text)
    print('manifest seed   :', man.get('seed'))
    print('manifest carriers:', len(man.get('carriers') or []))
    print('manifest keys   :', sorted(man))
    gen = man.get('generator') or {}
    tc = gen.get('tuple_check') or {}
    print('generator keys  :', sorted(gen))
    print('tuple_check keys:', sorted(tc) if isinstance(tc, dict) else type(tc))
    print('seed==freeze    :', str(man.get('seed', '')).lower() == FREEZE)

    bad = {'carrier_sha': [], 'envelope_digest': [], 'runjson_digest': [],
           'tuple': [], 'missing': [], 'op': []}
    tuples = {}
    for c in man['carriers']:
        cid = c['id']
        cpath = MANIFEST.rsplit('/',1)[0] + '/' + c['carrier']
        cbytes = blob(REV, cpath)
        if cbytes is None:
            bad['missing'].append((cid, 'carrier'))
            continue
        csha = sha(cbytes)
        if csha != str(c.get('sha256', '')).lower():
            bad['carrier_sha'].append((cid, csha, c.get('sha256')))
        epath = c.get('envelope') or (MANIFEST.rsplit('/',1)[0] + '/' + c['carrier'].rsplit('/', 1)[0] + '/envelope.json')
        ebytes = blob(REV, epath)
        if ebytes is None:
            bad['missing'].append((cid, 'envelope'))
            continue
        eo = json.loads(ebytes)
        data = eo.get('data', eo)
        subj = (((data.get('subject') or {}).get('digest') or {}).get('sha256'))
        if str(subj).lower() != csha:
            bad['envelope_digest'].append((cid, subj, csha))
        rp = epath.rsplit('/', 1)[0] + '/run.json'
        rb = blob(REV, rp)
        if rb is None:
            bad['missing'].append((cid, 'run.json'))
        else:
            rec = json.loads(rb)
            if str(rec.get('subject_sha256', '')).lower() != csha:
                bad['runjson_digest'].append((cid, rec.get('subject_sha256'), csha))
            if rec.get('digest_matches_carrier') is not True:
                bad['runjson_digest'].append((cid, 'flag-false'))
        obs = shape_of(data) if isinstance(data, dict) else None
        dec = c.get('declared_features')
        tuples[cid] = (obs, dec)
        if not isinstance(dec, dict):
            bad['tuple'].append((cid, 'declared-absent'))
            continue
        for k in ('handler_set', 'gap_kinds', 'gap_dependencies', 'be_argv',
                  'symlink_removed', 'published'):
            if obs.get(k) != dec.get(k):
                bad['tuple'].append((cid, k, dec.get(k), obs.get(k)))
        if data.get('operation') not in ('extract_firmware', 'inspect_firmware_regions'):
            bad['op'].append((cid, data.get('operation')))

    print('\n== per-carrier mismatches ==')
    for k, v in bad.items():
        print('%-18s %d %s' % (k, len(v), v[:6]))

    # manifest generator.tuple_check vs our own observation
    entries = tc.get('entries') if isinstance(tc, dict) else None
    if isinstance(entries, dict):
        n = 0
        for cid, rec in entries.items():
            n += 1
            obs, dec = tuples.get(cid, (None, None))
            ro = rec.get('observed')
            if ro != obs or rec.get('declared') != dec:
                print('  TUPLE-CHECK RECORD DISAGREES WITH BYTES', cid, ro, obs)
        print('tuple_check entries re-verified:', n)
    elif isinstance(entries, list):
        print('tuple_check entries is a list of', len(entries))
    print('all_equal field:', tc.get('all_equal') if isinstance(tc, dict) else None)

    # out-of-domain vacuity
    ood = [c['id'] for c in man['carriers'] if str(c.get('class')) == 'out-of-domain']
    print('\nout-of-domain carriers:', ood)
    for cid in ood:
        obs, dec = tuples[cid]
        print(' ', cid, 'declared', dec, 'observed', obs)

    # SKILL v4 table region, reproduced with the counter's rule_block semantics
    sys.path.insert(0, '/fast/scratch/hyaku/kaidoku-r43/w2/R43W2SentC1')
    skill_rev = blob(REV, 'SKILL.md')
    skill_fz = blob(FREEZE, 'SKILL.md')
    skill_an = blob(ANCHOR, 'SKILL.md')
    print('\nSKILL.md whole-blob equal freeze/rev:', sha(skill_fz) == sha(skill_rev),
          sha(skill_rev))
    print('SKILL.md bytes len rev:', len(skill_rev))

    print('\nfrozen blob equality freeze vs rev:')
    for p in ('SKILL.md', 'corpus/SOURCES.md', 'plans/round-43-claims.md',
              'tools/round-43/c1-counter.py', 'tools/round-43/heldout-gen-v4r43.py',
              'tools/round-42/sqfs-triage-v4.py', 'tools/round-42/indep-eval-v4.py',
              'tools/round-42/fixtures.json',
              '.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md',
              '.ufo/waves/round-42/controls/c2/CTL-C2-7b-lookup-fallback.md',
              '.ufo/waves/round-42/controls/c2/dev-scores-prefreeze.json',
              '.ufo/waves/round-42/controls/c2/c2-counter-at-freeze.json',
              'corpus/evidence/round-42/c2/dev/manifest.json',
              'corpus/evidence/round-42/c2/heldout/manifest.json',
              'corpus/evidence/round-42/c2/heldout/C02/envelope.json',
              'corpus/evidence/round-42/c2/heldout/C02/rea-full.json',
              '.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json',
              'tools/round-41/local-source-gate.py',
              'tools/round-39/gen-squashfs.py'):
        a, b = blob(FREEZE, p), blob(REV, p)
        print('  %-70s %s %s' % (p, 'EQUAL' if (a is not None and a == b) else
                                 ('A-ONLY' if b is None else 'DIFF'), sha(b)))
    rc, log = git('log', '--format=%H', '%s..%s' % (FREEZE, REV), '--', 'SKILL.md',
                  'tools/round-43', 'tools/round-42', binary=False)
    print('\ncommits in FREEZE..REV touching frozen tools/SKILL:', log.split() or 'none')


if __name__ == '__main__':
    main()
