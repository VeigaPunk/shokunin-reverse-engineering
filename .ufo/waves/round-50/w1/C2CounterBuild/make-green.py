#!/usr/bin/env python3
"""Seat harness (not a lane instrument): in a scratch `git clone --shared` of the lane build
the FREEZE commit F (draft counter + draft selftest + expected + plan) on top of BASE and the
GREEN commit G (the correction text every atom needs, appended in the clone only).  Prints
{"freeze": F, "green": G, "base": BASE} on stdout.

Usage: make-green.py --clone DIR   (DIR must be a clone whose `git rev-parse --show-toplevel`
equals DIR; its identity is set here, in that clone only)
"""
import argparse
import importlib.util
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOLS = os.path.join(HERE, 'tools', 'round-50')


def load(path):
    spec = importlib.util.spec_from_file_location('c2rec', path)
    m = importlib.util.module_from_spec(spec)
    sys.dont_write_bytecode = True
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--clone', required=True)
    ap.add_argument('--plan', default='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-50/draft/plans/round-50-claims.md')
    a = ap.parse_args()
    m = load(os.path.join(TOOLS, 'c2-record.py'))
    d = os.path.realpath(a.clone)
    top = subprocess.run(['git', '-C', d, 'rev-parse', '--show-toplevel'], capture_output=True, text=True).stdout.strip()
    if os.path.realpath(top) != d:
        print('toplevel %s != %s' % (top, d), file=sys.stderr)
        return 2
    fx = m.Fx.__new__(m.Fx)
    fx.dir = d
    fx.git('config', 'user.name', 'c2counterbuild')
    fx.git('config', 'user.email', 'c2counterbuild@invalid')
    fx.git('config', 'commit.gpgsign', 'false')
    fx.git('checkout', '-q', '--detach', m.BASE)
    own = open(os.path.join(TOOLS, 'c2-record.py'), 'rb').read()
    st = open(os.path.join(TOOLS, 'selftest-r49-c2.py'), 'rb').read()
    ex = open(os.path.join(TOOLS, 'selftest-r49-c2.expected.json'), 'rb').read()
    F = fx.commit({m.SELF: own, m.SELFTEST_PATH: st, m.SELFTEST_EXPECTED: ex,
                   'plans/round-50-claims.md': open(a.plan, 'rb').read(),
                   'tools/round-50/control-fixtures/x.txt': b'x\n'}, 'GREEN-fixture FREEZE')
    ov = m.finish_green(m.build_green(m.Git(d)), st, ex, 3)
    G = fx.commit(ov, 'GREEN-fixture REV')
    print(json.dumps({'freeze': F, 'green': G, 'base': m.BASE}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
