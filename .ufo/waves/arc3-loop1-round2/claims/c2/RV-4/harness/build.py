#!/usr/bin/env python3
"""RV-4 mutation-test builder (scratch, /var/tmp).

Builds, from the frozen HEAD instrument (.ufo/gates/c1-census-v10.py, sha256
6f1d19ff...):
  work/instr-head.py      byte copy of HEAD
  work/instr-h3.py        HEAD + H3 positive-floor patch (CR-5 patch text, strict form)
  work/instr-h3-nog2.py   instr-h3.py with ONLY the H3 floor reverted (mutation)
  and needle/blindness fixtures derived from each:
  work/<name>-neut.py     PIN/VER/PTR neutered (CR-5's reproduction technique)
  work/<name>-gate.py     REA_GATE neutered (independent blindness channel)
  work/<name>-pinonly.py  only PIN neutered (partial-blindness probe)
"""
import hashlib
import os
import re

SRC = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py"
W = "/var/tmp/rv4-mutation/work"

FLOOR_HEAD = ('    g2_ok = len(out.get("current-ok", [])) > 0 or '
              '(not stale and not unatt and not undecl and not unres)\n')
FLOOR_H3 = '    g2_ok = len(out.get("current-ok", [])) > 0\n'
PRINT_HEAD = '    print("G2 positive-assertion guard: %s" % ("ok" if g2_ok else "SUSPECT"))\n'
PRINT_H3 = ('    print("G2 positive-assertion guard: %s (current-ok loci=%d, total loci=%d)" %\n'
            '          ("ok" if g2_ok else "SUSPECT", len(out.get("current-ok", [])),\n'
            '           sum(c["loci"] for c in counts.values())))\n')

NEEDLE_HEAD = {
    'PIN': 'PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
    'VER': 'VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
    'PTR': 'PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")',
}
NEEDLE_NEUT = {
    'PIN': 'PIN = re.compile(r"rea-agents@(ZZZ\\d+)", re.I)',
    'VER': 'VER = re.compile(r"(?<![\\d.])9\\.\\d+\\.\\d+")',
    'PTR': 'PTR = re.compile(r"((?:~|/)ZZZ\\.(?:json|toml|ya?ml)):(\\d+)")',
}
GATE_HEAD = ('REA_GATE = re.compile(r"rea-agents|\\brea\\b|config\\.toml|mcp_config\\.json|'
             'mcp\\.json|mcp_servers|devin|\\bomp\\b|kimi|npx", re.I)')
GATE_NEUT = 'REA_GATE = re.compile(r"ZZZ_never_matches_ZZZ")'


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def write(name, text):
    p = os.path.join(W, name)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(text)
    return p


def sub_once(text, old, new, label):
    n = text.count(old)
    assert n == 1, "%s: expected exactly 1 occurrence, found %d" % (label, n)
    return text.replace(old, new)


head = open(SRC, encoding='utf-8').read()
assert sha(SRC) == '6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b'
write('instr-head.py', head)

h3 = sub_once(head, FLOOR_HEAD, FLOOR_H3, 'H3 floor')
h3 = sub_once(h3, PRINT_HEAD, PRINT_H3, 'H3 diagnostic print')
write('instr-h3.py', h3)

# Mutation: revert ONLY the H3 floor boolean, keep the diagnostic print.
nog2 = sub_once(h3, FLOOR_H3, FLOOR_HEAD, 'revert H3 floor')
write('instr-h3-nog2.py', nog2)

variants = {'instr-head.py': head, 'instr-h3.py': h3, 'instr-h3-nog2.py': nog2}
for name, text in variants.items():
    stem = name[:-3]
    t = text
    for k in ('PIN', 'VER', 'PTR'):
        t = sub_once(t, NEEDLE_HEAD[k], NEEDLE_NEUT[k], '%s %s' % (name, k))
    write(stem + '-neut.py', t)

    write(stem + '-gate.py', sub_once(text, GATE_HEAD, GATE_NEUT, '%s gate' % name))

    write(stem + '-pinonly.py', sub_once(text, NEEDLE_HEAD['PIN'], NEEDLE_NEUT['PIN'],
                                         '%s pin-only' % name))

for f in sorted(os.listdir(W)):
    if f.endswith('.py'):
        print("%-24s %s" % (f, sha(os.path.join(W, f))))
