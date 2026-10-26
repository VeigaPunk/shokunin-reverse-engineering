#!/usr/bin/env python3
"""Dry-run driver for the round-42 C2 counter (QUALITY 84).

Builds a throwaway clone of the lane, commits a freeze-like commit that holds
the counter plus the STAND-IN drafts of the interpreter, evaluator and
generator (this seat's scaffolds; the owning seats' frozen tools replace them
byte for byte), generates the held-out and dev arms with the generator draft,
commits them, and runs the counter end to end at that revision.  The receipt it
writes is the dry-run evidence: every declared binding must appear.

Usage
  dryrun.py --lane LANE --artifacts ART [--scratch S]
Exit 0 when the counter ran and every binding was evaluated (met or not);
1 when a binding or a tool interface is missing; 2 on a fixture error.
Nothing in the lane is modified: the clone is the only tree written.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile

STALINKS = (
    ('c2-counter.py', 'c2-counter.py', 'tools/round-42/c2-counter.py'),
    ('standin-sqfs-triage-v4.py', 'sqfs-triage-v4.py',
     'tools/round-42/sqfs-triage-v4.py'),
    ('standin-indep-eval-v4.py', 'indep-eval-v4.py',
     'tools/round-42/indep-eval-v4.py'),
    ('standin-heldout-gen-v4.py', 'heldout-gen-v4.py',
     'tools/round-42/heldout-gen-v4.py'),
)
LOOKUP = '.ufo/waves/round-42/controls/c2/CTL-C2-7-lookup.md'
LOOKUP_7B = '.ufo/waves/round-42/controls/c2/CTL-C2-7b-lookup-fallback.md'
DEV_SEED_CMD = 'printf dev42 | sha256sum | cut -c1-40'


def run(cmd, cwd=None, env=None, check=True):
    pr = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if check and pr.returncode != 0:
        raise SystemExit('command failed (%d): %s\n%s\n%s'
                         % (pr.returncode, ' '.join(cmd), pr.stdout[-2000:],
                            pr.stderr[-2000:]))
    return pr


def git(d, *args, **kw):
    return run(['git', '-C', d, '-c', 'user.name=fx', '-c', 'user.email=fx@fx']
               + list(args), **kw)


def write(d, rel, data):
    p = os.path.join(d, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    mode = 'wb' if isinstance(data, bytes) else 'w'
    with open(p, mode) as fh:
        fh.write(data)


def insert_block(base_skill, block):
    """Insert the v4 marker..table lines at the end of `## Queue-drain craft`."""
    lines = base_skill.splitlines()
    start = next(i for i, l in enumerate(lines)
                 if l.lower().startswith('## queue-drain craft'))
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    blk = block.splitlines()
    mi = next(i for i, l in enumerate(blk)
              if l.strip().startswith('<!-- sqfs-triage-table v4 -->'))
    bullet = next((l for l in blk if l.startswith('- **')), '')
    out = lines[:end] + ['', bullet, ''] \
        + [l for l in blk[mi:] if not l.startswith('## ')] + [''] + lines[end:]
    return '\n'.join(out) + '\n'


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane', required=True)
    ap.add_argument('--artifacts', required=True)
    ap.add_argument('--scratch')
    ap.add_argument('--no-clean', action='store_true')
    a = ap.parse_args(argv)

    art = os.path.abspath(a.artifacts)
    lane = os.path.abspath(a.lane)
    sroot = a.scratch or os.environ.get('HYAKU_SCRATCH') or tempfile.gettempdir()
    os.makedirs(sroot, exist_ok=True)
    fx = tempfile.mkdtemp(prefix='dryrun.', dir=sroot)
    env = dict(os.environ)
    env['TMPDIR'] = os.path.join(fx, 'tmp')
    os.makedirs(env['TMPDIR'], exist_ok=True)
    try:
        clone = os.path.join(fx, 'lane')
        run(['git', 'clone', '-q', '--shared', lane, clone])
        top = run(['git', '-C', clone, 'rev-parse', '--show-toplevel'],
                  ).stdout.strip()
        if os.path.realpath(top) != os.path.realpath(clone):
            raise SystemExit('fixture toplevel mismatch: %r' % top)

        for src, dst, rel in STALINKS:
            with open(os.path.join(art, src), 'rb') as fh:
                write(clone, rel, fh.read())

        # control tables in the DRAFT v4 grammar (stand-in writer)
        for mode, rel in (('lookup', LOOKUP), ('lookup-fallback', LOOKUP_7B)):
            sub = os.path.join(fx, 'ctl-' + mode)
            os.makedirs(sub, exist_ok=True)
            out = os.path.join(fx, 'ctl-' + mode + '.md')
            run([sys.executable, '-I', '-B',
                 os.path.join(art, 'standin-controls.py'),
                 '--gen', os.path.join(art, 'standin-heldout-gen-v4.py'),
                 '--eval', os.path.join(art, 'standin-indep-eval-v4.py'),
                 '--seed', 'f' * 64, '--out', out, '--mode', mode,
                 '--work', sub], env=env)
            with open(out, 'rb') as fh:
                write(clone, rel, fh.read())

        # the claims draft, byte for byte
        with open(os.path.join(lane, 'plans/round-42-claims.md'), 'rb') as fh:
            write(clone, 'plans/round-42-claims.md', fh.read())

        # SKILL.md: the base bytes plus the stand-in block 21
        base = run(['git', '-C', clone, 'show',
                    'c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c:SKILL.md'],
                   cwd=clone).stdout
        with open(os.path.join(art, 'standin-skill-block21.md')) as fh:
            block = fh.read()
        write(clone, 'SKILL.md', insert_block(base, block))

        git(clone, 'add', '-A')
        git(clone, 'commit', '-qm', 'freeze-like: counter + stand-in drafts')
        freeze = git(clone, 'rev-parse', 'HEAD').stdout.strip()

        # held-out arm (seed = the freeze commit) and the dev arm
        held = os.path.join(clone, 'corpus/evidence/round-42/c2/heldout')
        dev = os.path.join(clone, 'corpus/evidence/round-42/c2/dev')
        gen = os.path.join(clone, 'tools/round-42/heldout-gen-v4.py')
        generated = {}
        generated['heldout'] = run([sys.executable, '-I', '-B', gen,
                                    '--seed', freeze, '--out', held],
                                   cwd=clone, env=env).stdout.strip()
        dev_seed = os.popen(DEV_SEED_CMD).read().strip()
        generated['dev'] = run([sys.executable, '-I', '-B', gen,
                                '--seed', dev_seed, '--out', dev, '--arm', 'dev'],
                               cwd=clone, env=env).stdout.strip()
        initial = {}
        generated['verify_initial'] = run(
            [sys.executable, '-I', '-B', gen, '--seed', freeze, '--out', held,
             '--verify'], cwd=clone, env=env, check=False).stdout.strip()
        generated['verify_dev'] = run(
            [sys.executable, '-I', '-B', gen, '--seed', dev_seed, '--out', dev,
             '--arm', 'dev', '--verify'], cwd=clone, env=env,
            check=False).stdout.strip()

        git(clone, 'add', '-A')
        git(clone, 'commit', '-qm', 'claim data: held-out + dev arms')
        rev = git(clone, 'rev-parse', 'HEAD').stdout.strip()

        receipt = os.path.join(art, 'dryrun-receipt.json')
        if os.path.exists(receipt):
            os.unlink(receipt)
        pr = run([sys.executable, '-I', '-B',
                  os.path.join(clone, 'tools/round-42/c2-counter.py'),
                  '--root', clone, '--rev', rev, '--freeze', freeze,
                  '--json-out', receipt], cwd=clone, env=env, check=False)
        if not os.path.exists(receipt):
            print(json.dumps({'dryrun': 'no receipt', 'exit': pr.returncode,
                              'stdout': pr.stdout, 'stderr': pr.stderr}))
            return 2
        with open(receipt) as fh:
            rec = json.load(fh)
        declared = set(rec.get('claim_bindings') or []) \
            | set(rec.get('instrument_bindings') or [])
        bindings = rec.get('bindings') or {}
        missing = sorted(declared - set(bindings))
        extra = sorted(set(bindings) - declared)
        undecided = sorted(k for k, v in bindings.items() if v not in (True, False))
        summary = {
            'dryrun': 'c2-counter r42 A1',
            'clone': clone,
            'freeze': freeze,
            'rev': rev,
            'counter_exit': pr.returncode,
            'receipt_exit_code': rec.get('exit_code'),
            'counter_sha256': rec.get('counter_sha256'),
            'counter_sha256_at_freeze': rec.get('counter_sha256_at_freeze'),
            'n': rec.get('n'),
            'matched': rec.get('matched'),
            'matched_classes': rec.get('matched_classes'),
            'matched_combos': rec.get('matched_combos'),
            'met_target': rec.get('met_target'),
            'bindings_evaluated': len(bindings),
            'bindings_declared': len(declared),
            'bindings_missing': missing,
            'bindings_extra': extra,
            'bindings_undecided': undecided,
            'bindings_false': rec.get('bindings_false'),
            'bindings': {k: bindings[k] for k in sorted(bindings)},
            'lookup': {k: (rec.get('lookup') or {}).get(k)
                       for k in ('n_combos', 'score', 'half', 'identical_to_freeze')},
            'lookup_7b': {k: (rec.get('lookup_7b') or {}).get(k)
                          for k in ('n_combos', 'score', 'below_half', 'binding')},
            'combo_unseen_majority': {k: (rec.get('combo_unseen_majority') or {}).get(k)
                                      for k in ('dev_named_tuples', 'n_combos',
                                                'need')} | {
                'unseen': len((rec.get('combo_unseen_majority') or {}).get('unseen') or [])},
            'real_receipts': {k: (rec.get('real_receipts') or {}).get(k)
                              for k in ('expected_label', 'missing',
                                        'interpreter_interface',
                                        'evaluator_interface')},
            'dev_envelopes': {k: (rec.get('dev_envelopes') or {}).get(k)
                              for k in ('dir', 'n', 'legacy_handler_seen',
                                        'interpreter_interface',
                                        'evaluator_interface')},
            'evaluator_interface': rec.get('evaluator_interface'),
            'interpreter_interface': rec.get('interpreter_interface'),
            'generated': generated,
        }
        print(json.dumps(summary, indent=1, sort_keys=True))
        ok = not missing and not extra and not undecided \
            and rec.get('met_target') is True and pr.returncode == 0
        return 0 if ok else 1
    finally:
        if not a.no_clean:
            shutil.rmtree(fx, ignore_errors=True)


if __name__ == '__main__':
    sys.exit(main())
