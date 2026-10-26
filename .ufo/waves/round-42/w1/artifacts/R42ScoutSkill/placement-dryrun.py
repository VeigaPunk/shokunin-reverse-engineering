#!/usr/bin/env python3
"""R42ScoutSkill placement dry run: sandbox clone of the lane at BASE, insert a block-21 skeleton
plus two stub knowledge entries and coverage-map rows, and run SCORECARD command A (cmdA-detail.py)
and the round-41 v3 interpreter / c2-counter rule_block on the result.  Honours --work (default $TMPDIR)."""
import argparse, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, tempfile

LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
BASE = 'c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c'
HERE = os.path.dirname(os.path.abspath(__file__))
ENT_A = '2026-10-26-r42-sqfs-triage-v4'
ENT_B = '2026-10-26-r42-squashfs-v3-core'

def sh(*a, cwd=None, check=True):
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True)
    if check and r.returncode:
        raise SystemExit('FAIL %s: %s' % (a, r.stderr))
    return r

def git(d, *a, check=True):
    return sh('git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx', *a, check=check)

def rows(n, label='clean'):
    return ('  | %s | `extract_firmware` | `unblob` | `squashfs_v[123]*` | `none` | `*` | `*` | `no` | `>0` | `none` | cause -> act | s |' % label)

def block21(cite, quote_marker_before=False):
    return '\n'.join([
        '- **SquashFS `extract-firmware` outcome triage v4 (round 42).** prose (%s).' % cite,
        '',
        '  <!-- sqfs-triage-table v4 -->',
        '  <!-- sqfs-triage-actions: none inspect-input install-extractor-be install-extractor-le wrap-extractor-be preserve-failure salvage-partial raise-depth audit-symlinks expect-link-absent count-gap confirm-empty cross-read-legacy -->',
        '  | label | operation | provider | handler | gap kinds | dependencies | -be in child argv | symlink removed | published files | action | cause | source |',
        '  | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |',
        '  | no-squashfs-chunk | `extract_firmware` | `unblob` | `none` | `*` | `*` | `*` | `*` | `*` | `inspect-input` | cause -> act | s |',
        rows(0), ''])

def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m

def cmdA(d, rev):
    r = sh(sys.executable, os.path.join(HERE, 'cmdA-detail.py'), rev, cwd=d)
    j = json.loads(r.stdout.splitlines()[0])
    return {k: j[k] for k in ('rule_blocks', 'citation_resolved_rules', 'knowledge_files', 'mapped', 'missing', 'dangling')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--work', default=os.environ.get('TMPDIR'))
    a = ap.parse_args()
    if not a.work: raise SystemExit('--work or TMPDIR required')
    d = tempfile.mkdtemp(prefix='fx.', dir=a.work); lane = os.path.join(d, 'lane')
    sh('git', 'clone', '-q', '--shared', LANE, lane)
    top = git(lane, 'rev-parse', '--show-toplevel').stdout.strip()
    assert top == lane, (top, lane)
    git(lane, 'checkout', '-q', '--detach', BASE)
    skill0 = open(os.path.join(lane, 'SKILL.md')).read().split('\n')
    # lines are 1-based in the report: block 20 = 387..449, v3 marker 434, craft ends before 454 heading
    assert skill0[386].startswith('- **SquashFS `extract-firmware` outcome triage v3'), skill0[386][:60]
    assert skill0[433].strip() == '<!-- sqfs-triage-table v3 -->'
    assert skill0[448].lstrip().startswith('| clean-empty')
    assert skill0[453].startswith('## Config custody')
    rd0 = open(os.path.join(lane, 'corpus/README.md')).read().split('\n')
    assert rd0[98].startswith('| SquashFS `extract-firmware` outcome triage v3 (round 41)')
    c2 = load(os.path.join(lane, 'tools/round-41/c2-counter.py'), 'c2c')
    v3src = open(os.path.join(lane, 'tools/round-41/sqfs-triage-v3.py')).read()
    v4src = v3src.replace("MARKER = '<!-- sqfs-triage-table v3 -->'", "MARKER = '<!-- sqfs-triage-table v4 -->'") \
                 .replace("REFUSED_MARKERS = ('<!-- sqfs-triage-table v2 -->', '<!-- sqfs-triage-table v1 -->')",
                          "REFUSED_MARKERS = ('<!-- sqfs-triage-table v3 -->', '<!-- sqfs-triage-table v2 -->')")
    assert v4src != v3src
    v4py = os.path.join(d, 'v4-as-v3.py'); open(v4py, 'w').write(v4src)
    out = {'base': BASE, 'variants': {}}

    def variant(name, skill_lines, entries=(ENT_A, ENT_B), map_rows=(ENT_A, ENT_B), entry_len=40):
        git(lane, 'checkout', '-q', '--detach', BASE)
        open(os.path.join(lane, 'SKILL.md'), 'w').write('\n'.join(skill_lines))
        for e in entries:
            open(os.path.join(lane, 'corpus/knowledge', e + '.md'), 'w').write(
                '\n'.join('line %d' % i for i in range(1, entry_len + 1)) + '\n')
        rd = list(rd0)
        rd[99:99] = ['| row for round 42 (%s) | `%s` | held |' % (e, e) for e in map_rows]
        open(os.path.join(lane, 'corpus/README.md'), 'w').write('\n'.join(rd))
        git(lane, 'add', '-A'); git(lane, 'commit', '-q', '-m', name)
        rev = git(lane, 'rev-parse', 'HEAD').stdout.strip()
        res = {'cmdA': cmdA(lane, rev)}
        blob = sh('git', '-C', lane, 'show', '%s:SKILL.md' % rev).stdout
        v3_before = c2.rule_block('\n'.join(skill0), c2.MARKER_V3)
        v3_after = c2.rule_block(blob, c2.MARKER_V3)
        res['v3_region_bytes_equal_base'] = (v3_before == v3_after)
        res['v3_region_sha'] = hashlib.sha256((v3_after or '').encode()).hexdigest()[:12]
        lines = blob.split('\n')
        res['block21_start_line'] = next((i + 1 for i, l in enumerate(lines) if l.startswith('- **SquashFS `extract-firmware` outcome triage v4')), None)
        res['v4_marker_lines'] = [i + 1 for i, l in enumerate(lines) if '<!-- sqfs-triage-table v4 -->' in l]
        res['config_custody_line'] = next(i + 1 for i, l in enumerate(lines) if l.startswith('## Config custody'))
        sk = os.path.join(d, 'SKILL-%s.md' % name); open(sk, 'w').write(blob)
        r = sh(sys.executable, '-I', '-B', v4py, '--skill', sk, '--table-only', check=False)
        txt = r.stdout.splitlines()
        res['v4_reader'] = {'exit': r.returncode,
                            'info': next((l for l in txt if l.startswith('marker line')), None),
                            'stderr': r.stderr.strip()[:160]}
        r3 = sh(sys.executable, '-I', '-B', os.path.join(lane, 'tools/round-41/sqfs-triage-v3.py'), '--skill', sk, '--table-only', check=False)
        res['v3_reader_exit'] = r3.returncode
        res['v3_reader_tail'] = r3.stdout.strip().splitlines()[-1][:100] if r3.stdout.strip() else r3.stderr[:100]
        out['variants'][name] = res
        return blob

    cite_ok = 'corpus/knowledge/%s.md:12-30' % ENT_A
    ins = lambda blk, at=449: skill0[:at] + [''] + blk.split('\n')[:-1] + skill0[at:]
    # V1 placement: after line 449, one blank line between, before the blank run + ## Config custody
    variant('V1-good', ins(block21(cite_ok)))
    variant('V2-range-past-eof', ins(block21('corpus/knowledge/%s.md:12-300' % ENT_A)))
    variant('V3-no-prefix-cite', ins(block21('knowledge %s.md :12-30' % ENT_A)))
    variant('V4-entry-uncommitted', ins(block21(cite_ok)), entries=(ENT_B,))
    variant('V5-no-map-row', ins(block21(cite_ok)), map_rows=())
    variant('V6-after-next-heading', skill0[:453] + ['## Config custody x'] + [''] + block21(cite_ok).split('\n')[:-1] + skill0[454:])
    variant('V7-indented-bullet', ins(block21(cite_ok).replace('- **SquashFS', '  - **SquashFS', 1)))
    variant('V8-no-bold-bullet', ins(block21(cite_ok).replace('- **SquashFS', '- SquashFS', 1).replace(' (round 42).**', ' (round 42).')))
    # supersession sentence placements inside block 20
    sup_quote = ['  Superseded for v1-v3 chunks by table v4 (`<!-- sqfs-triage-table v4 -->`, rule block 21 below).']
    sup_plain = ['  Superseded for v1-v3 chunks by table v4 (rule block 21 below, `corpus/knowledge/%s.md:12-30`).' % ENT_A]
    b = ins(block21(cite_ok))
    variant('V9-sentence-quotes-v4-marker-before-v3-marker', b[:414] + sup_quote + b[414:])
    variant('V10-sentence-plain-before-v3-marker', b[:414] + sup_plain + b[414:])
    variant('V11-sentence-after-v3-table', b[:449] + sup_plain + b[449:])
    assert skill0[413].endswith('stale second text behind.'), skill0[413][-60:]
    app = list(b); app[413] = app[413] + ' Superseded for v1-v3 chunks by table v4 (rule block 21 below).'
    variant('V12-sentence-appended-to-line-414-no-shift', app)
    json.dump(out, open(os.path.join(HERE, 'placement-dryrun.json'), 'w'), indent=1, sort_keys=True)
    print(json.dumps(out, indent=1, sort_keys=True))
    shutil.rmtree(d, ignore_errors=True)

main()
