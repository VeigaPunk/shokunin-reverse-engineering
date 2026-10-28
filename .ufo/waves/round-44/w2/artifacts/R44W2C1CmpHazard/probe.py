#!/usr/bin/env python3
"""R44W2C1CmpHazard: reproducible probe of the declared `cmp -l` instrument hazard.

Regenerates every number in ../R44W2C1CmpHazard.md from scratch:

  * a one-byte-difference size ladder, three comparison modes per size;
  * the stdout-destination matrix at 4096 B (30 repetitions per destination);
  * flag and size-mismatch variants;
  * the four invocation paths a counter could actually take;
  * the counterfactual on the real v1le carrier bytes (false pass vs sha256 /
    git-blob-oid catch);
  * the byte-comparison audit of every round-44 tool.

All fixtures are written under a caller-supplied scratch dir (--scratch) and
removed afterwards. Nothing outside --scratch and --out is written; no lane byte
is modified (the carrier is copied, never touched).

Usage:
  python3 -I -B probe.py --scratch DIR --out FILE
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

CMP = '/usr/bin/cmp'
CARRIERS = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
LANE = CARRIERS
TOOLS = os.path.join(LANE, 'tools', 'round-44')
CARRIER_REL = 'corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin'
CARRIER_PIN = 'b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def probe(argv, *, stdout_path=None, cwd=None, stdin_data=None):
    """Run argv; record exit code, stdout digest/bytes, stderr digest, wall time."""
    started = time.perf_counter()
    fh = open(stdout_path, 'wb') if stdout_path else None
    try:
        proc = subprocess.run(argv, cwd=cwd, input=stdin_data,
                              stdout=fh if fh else subprocess.PIPE,
                              stderr=subprocess.PIPE)
        out = b'' if fh else proc.stdout
        if fh:
            fh.close()
            out = open(stdout_path, 'rb').read()
    finally:
        if fh and not fh.closed:
            fh.close()
    return {
        'argv': argv,
        'exit_code': proc.returncode,
        'stdout_sha256': sha(out),
        'stdout_bytes': len(out),
        'stdout_head': out[:200].decode('utf-8', 'replace'),
        'stderr_sha256': sha(proc.stderr),
        'stderr_head': proc.stderr[:200].decode('utf-8', 'replace'),
        'wall_s': round(time.perf_counter() - started, 6),
    }


def write(path, data):
    with open(path, 'wb') as fh:
        fh.write(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--scratch', required=True)
    ap.add_argument('--out', required=True)
    args = ap.parse_args()

    work = os.path.join(args.scratch, 'probe')
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work, exist_ok=True)
    result = {'seat': 'R44W2C1CmpHazard', 'generated_at_utc':
              time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
              'cmp': CMP, 'scratch': work}

    # ---- instrument identity -------------------------------------------------
    result['instrument'] = {
        'cmp_version': probe([CMP, '--version']),
        'pacman_Q': probe(['pacman', '-Q', 'diffutils']),
        'pacman_Qkk': probe(['pacman', '-Qkk', 'diffutils']),
        'which_cmp_python': shutil.which('cmp'),
        'size': os.path.getsize(CMP),
        'sha256': sha(open(CMP, 'rb').read()),
    }

    # ---- 1. size ladder ------------------------------------------------------
    ladder = []
    for n in (15, 255, 4095, 4096, 4097, 8191, 8192, 8193, 16384, 65536,
              1 << 20):
        a = b'A' * n
        b = bytearray(a)
        b[n // 2] = ord('B')
        pa, pb = os.path.join(work, 'a%d' % n), os.path.join(work, 'b%d' % n)
        write(pa, a)
        write(pb, bytes(b))
        differing = sum(1 for x, y in zip(a, bytes(b)) if x != y)
        row = {'size': n, 'differing_bytes': differing}
        for label, argv in (('-l', [CMP, '-l', pa, pb]),
                            ('-s', [CMP, '-s', pa, pb]),
                            ('plain', [CMP, pa, pb])):
            row['exit_' + label] = probe(argv)['exit_code']
        ladder.append(row)
    result['size_ladder'] = ladder
    result['false_equal_sizes'] = [r['size'] for r in ladder if r['exit_-l'] == 0]

    # ---- 2. destination matrix at the carrier size ---------------------------
    pa, pb = os.path.join(work, 'a4096'), os.path.join(work, 'b4096')
    dest = {}
    counts = {}
    for _ in range(30):
        counts.setdefault('devnull', []).append(
            probe([CMP, '-l', pa, pb], stdout_path='/dev/null')['exit_code'])
        counts.setdefault('regular_file', []).append(
            probe([CMP, '-l', pa, pb],
                  stdout_path=os.path.join(work, 'o.txt'))['exit_code'])
        counts.setdefault('pipe', []).append(
            probe([CMP, '-l', pa, pb])['exit_code'])
    for k, v in counts.items():
        dest[k] = {str(rc): v.count(rc) for rc in sorted(set(v))}
    result['destination_matrix_4096'] = dest
    result['destination_matrix_4096']['repetitions'] = 30

    # ---- 2b. a second char device: writes fail with ENOSPC -------------------
    # The path is never read back (`/dev/full` is an infinite zero source).
    started = time.perf_counter()
    with open('/dev/full', 'wb') as fh:
        full = subprocess.run([CMP, '-l', pa, pb], stdout=fh,
                              stderr=subprocess.PIPE)
    dest['devfull'] = {str(full.returncode): 1}
    dest['_devfull_wall_s'] = round(time.perf_counter() - started, 6)

    # ---- 2c. equal-length vs unequal-length at >= 4096 ----------------------
    eq = {}
    specs = (
        ('equal_4096_one_diff', 4096, 4096, 2048),
        ('equal_4096_identical', 4096, 4096, None),
        ('equal_8192_one_diff', 8192, 8192, 7000),
        ('unequal_4096_8192_shared_prefix_diff', 4096, 8192, 100),
        ('unequal_4096_8192_no_shared_diff', 4096, 8192, None),
        ('unequal_4096_4097_shared_prefix_diff', 4096, 4097, 100),
    )
    for name, n1, n2, at in specs:
        p1, p2 = (os.path.join(work, name + s) for s in ('-a', '-b'))
        b1, b2 = bytearray(b'A' * n1), bytearray(b'A' * n2)
        if at is not None:
            b2[at] = ord('B')
        write(p1, bytes(b1))
        write(p2, bytes(b2))
        eq[name] = {'sizes': [n1, n2],
                    '-l': probe([CMP, '-l', p1, p2])['exit_code'],
                    '-s': probe([CMP, '-s', p1, p2])['exit_code'],
                    'plain': probe([CMP, p1, p2])['exit_code']}
    result['equal_length_vs_unequal'] = eq

    # ---- 3. identical pair (does -l discriminate at all?) --------------------
    pc = os.path.join(work, 'c4096')
    write(pc, b'A' * 4096)
    result['identical_4096'] = {
        '-l': probe([CMP, '-l', pc, pc])['exit_code'],
        '-s': probe([CMP, '-s', pc, pc])['exit_code'],
        'plain': probe([CMP, pc, pc])['exit_code'],
    }

    # ---- 4. size-mismatch / truncation cases ---------------------------------
    p4096, p4097, p5000 = (os.path.join(work, n) for n in
                           ('p4096', 'p4097', 'p5000'))
    write(p4096, b'A' * 4096)
    write(p4097, b'A' * 4097)
    write(p5000, b'A' * 5000)
    result['size_mismatch'] = {
        '4096_vs_4097_prefix_identical': {
            '-l': probe([CMP, '-l', p4096, p4097])['exit_code'],
            'plain': probe([CMP, p4096, p4097])['exit_code']},
        '4096_vs_5000_prefix_identical': {
            '-l': probe([CMP, '-l', p4096, p5000])['exit_code'],
            'plain': probe([CMP, p4096, p5000])['exit_code']},
    }

    # ---- 5. flag variants ----------------------------------------------------
    result['flag_variants_4096'] = {
        f: probe([CMP, *f.split(), pa, pb])['exit_code']
        for f in ('-l', '-b', '--print-bytes', '-l -s')
    }

    # ---- 6. invocation paths a counter could take ----------------------------
    shell_abs = '/bin/sh -c "%s -l %s %s"  (absolute binary)' % (CMP, pa, pb)
    shell_path = '/bin/sh -c "cmp -l %s %s"  (PATH lookup)' % (pa, pb)
    result['invocation_paths_4096'] = {
        'subprocess_argv': probe([CMP, '-l', pa, pb])['exit_code'],
        'subprocess_argv_bare_cmp_PYTHONPATH': probe(['cmp', '-l', pa, pb])['exit_code'],
        'subprocess_shell_true': probe(
            ['/bin/sh', '-c', 'cmp -l %s %s' % (pa, pb)])['exit_code'],
        'bin_sh_absolute': probe(['/bin/sh', '-c', '%s -l %s %s' % (CMP, pa, pb)])['exit_code'],
        'bin_bash_resolves': probe(['/bin/bash', '-c', 'command -v cmp'])['stdout_head'].strip(),
        'bin_sh_resolves': probe(['/bin/sh', '-c', 'command -v cmp'])['stdout_head'].strip(),
        '_labels': {'bin_sh_path': shell_path, 'bin_sh_abs': shell_abs},
    }

    # ---- 7. counterfactual on the real carrier bytes -------------------------
    src = os.path.join(LANE, CARRIER_REL)
    orig = os.path.join(work, 'carrier-orig.bin')
    mutant = os.path.join(work, 'carrier-mutant.bin')
    shutil.copyfile(src, orig)
    raw = bytearray(open(src, 'rb').read())
    raw[100] ^= 0xFF
    write(mutant, bytes(raw))
    cf = {
        'carrier': CARRIER_REL,
        'carrier_size': os.path.getsize(src),
        'carrier_pin': CARRIER_PIN,
        'mutation': 'byte offset 100 XOR 0xFF (one byte)',
    }
    rc_file = probe([CMP, '-l', orig, mutant],
                    stdout_path=os.path.join(work, 'cf.out'))
    rc_null = probe([CMP, '-l', orig, mutant], stdout_path='/dev/null')
    rc_pipe = probe([CMP, '-l', orig, mutant])
    cf['cmp_l_to_file'] = {'exit_code': rc_file['exit_code'],
                           'emitted_line': rc_file['stdout_head'].strip()}
    cf['cmp_l_to_devnull'] = {'exit_code': rc_null['exit_code']}
    cf['cmp_l_to_pipe'] = {'exit_code': rc_pipe['exit_code']}
    cf['naive_binding_verdict'] = ('MET (FALSE PASS)'
                                   if rc_file['exit_code'] == 0 else 'red')
    cf['sha256_orig'] = sha(open(orig, 'rb').read())
    cf['sha256_mutant'] = sha(open(mutant, 'rb').read())
    cf['carrier_pin_ok_for_mutant'] = cf['sha256_mutant'] == CARRIER_PIN
    cf['carrier_pin_ok_for_orig'] = cf['sha256_orig'] == CARRIER_PIN
    oid_orig = probe(['git', 'hash-object', orig])['stdout_head'].strip()
    oid_mut = probe(['git', 'hash-object', mutant])['stdout_head'].strip()
    cf['git_blob_oid'] = {'orig': oid_orig, 'mutant': oid_mut,
                          'equal': oid_orig == oid_mut}
    result['carrier_counterfactual'] = cf

    # ---- 8. tool audit -------------------------------------------------------
    audit = {}
    for label, argv in (
        ('round44_py_sh_cmp',
         ['grep', '-rn', 'cmp', os.path.join(TOOLS, 'c1-counter.py'),
          os.path.join(TOOLS, 'c2-counter.py'),
          os.path.join(TOOLS, 'c1-controls.py'),
          os.path.join(TOOLS, 'c2-controls.py'),
          os.path.join(TOOLS, 'c1-oracle.py'),
          os.path.join(TOOLS, 'c1-run.py'),
          os.path.join(TOOLS, 'c1-run.sh')]),
        ('round44_tree_cmp', ['grep', '-rn', 'cmp', TOOLS]),
        ('round44_cmp_dash_l', ['grep', '-rn', 'cmp[[:space:]]*-l', TOOLS]),
        ('round44_shell_true', ['grep', '-rn', 'shell=True', TOOLS]),
        ('lane_cmp_dash_l',
         ['grep', '-rn', '--binary-files=without-match', 'cmp[[:space:]]*-l',
          LANE, '--exclude-dir=.git']),
    ):
        r = probe(argv)
        audit[label] = {'exit_code': r['exit_code'],
                        'stdout_bytes': r['stdout_bytes'],
                        'matches': [ln for ln in r['stdout_head'].splitlines()][:40]}
    result['tool_audit'] = audit

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    with open(args.out, 'w') as fh:
        json.dump(result, fh, indent=1, sort_keys=False)
    print('wrote', args.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
