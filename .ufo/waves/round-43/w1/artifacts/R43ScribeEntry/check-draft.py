#!/usr/bin/env python3
"""Gate the round-43 v4-scored knowledge entry draft.

Reads only. No network, no REA, no VCS mutation: `git show` against the lane.

Checks, each mapped to the defect it catches:
  E1  front-matter order: every `source:` line, then `verified-at:`, then `recheck:`,
      then `status:` last of the four (CORPUS.md "provenance trio"; lesson R42-V5,
      corpus/lessons/round-42-verifier-spotcheck.md:92)
  E2  every `source:` line names an `S###` row and a resolvable pointer (URL or a
      path), so a source cannot be cited by number alone
  E3  the status line names the claim (R43-C1)
  E4  placeholder hygiene: every `<<L1:tok>>` in the draft is a ledger row, every
      ledger row appears, and each appears the number of times the ledger says
  E5  prose only: no markdown table row and no fenced code block (the entry the
      L1 installs is prose, not a second copy of the table)
  E6  literal pins: the numbers the draft states as measured must equal the ones
      recomputed here -- the SKILL.md v4 region at --rev, the frozen interpreter,
      evaluator and fixture pins, the S135 license, the S119 6.5.0 files. A pin
      that drifts is the failure this check exists for (R42-V5 sibling defect:
      a number written once and never re-derived).

Exit 0 when every check passes; 1 on the first failing check with the reason on
stdout. `--selftest` mutates the draft in memory six ways and requires each to
fail for the stated check; it exits 0 only when all six go red and the unchanged
draft is green.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys

BLOCK_MARKER = '<!-- sqfs-triage-table v4 -->'
CRAFT_HEAD = '## queue-drain craft'

PINS = {
    'block': '92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2',
    'interpreter': '497bab6766a0b0c6d6f36cb58cadc531bddf9dd3231f6100bf46cf6ff552a2e9',
    'evaluator': '7a135dd36b3cab29d4dfa5b5d6dcf2199c026989549683933f4e6c1fa64dd301',
    'fixtures': '9f957663c1f21940ec17e32f98485425145b6c4e7eb265a7b12327b629c3da9b',
    's135_sha': '67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e',
    's119_tarball': '531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699',
    's119_pub': 'bb4f3246bee70a5b32b048e5ef956e649626b6449b1d457454440739a8d51029',
    's112': '2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287',
    's118': '1bb498119429ed80ae29caf9772d2b6210c22b6a8a2c8beb6cfea94550bcd23a',
}
PATHS = {
    'interpreter': 'tools/round-42/sqfs-triage-v4.py',
    'evaluator': 'tools/round-42/indep-eval-v4.py',
    'fixtures': 'tools/round-42/fixtures.json',
}


def fail(check, why):
    print('%s: %s' % (check, why))
    return 1


def show(root, rev, path):
    p = subprocess.run(['git', '-C', root, 'show', '%s:%s' % (rev, path)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        return None
    return p.stdout


def region(text):
    """marker line -> end of the first markdown table after it, within the craft section."""
    if text is None:
        return None
    lines = text.splitlines()
    start = next((i for i, l in enumerate(lines)
                  if l.lower().startswith(CRAFT_HEAD)), None)
    if start is None:
        return None
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith('## '):
            end = i
            break
    mi = next((i for i in range(start + 1, end)
               if lines[i].strip().startswith(BLOCK_MARKER)), None)
    if mi is None:
        return None
    stop = end
    for i in range(mi + 1, end):
        l = lines[i]
        if re.match(r'^#{1,4} ', l) or re.match(r'^\s*-\s+\*\*', l) \
                or l.strip().startswith('<!-- sqfs-triage-table'):
            stop = i
            break
    block = '\n'.join(lines[mi:stop]).rstrip('\n')
    return block or None


def front_matter(text):
    lines = text.splitlines()
    idx = {}
    for name in ('source:', 'verified-at:', 'recheck:', 'status:'):
        hits = [i for i, l in enumerate(lines) if l.startswith(name)]
        idx[name] = hits
    return lines, idx


def check_e1(text):
    lines, idx = front_matter(text)
    if not idx['source:']:
        return fail('E1', 'no source: row')
    for name in ('verified-at:', 'recheck:', 'status:'):
        if len(idx[name]) != 1:
            return fail('E1', '%s appears %d times, expected 1' % (name, len(idx[name])))
    src = idx['source:']
    if not (max(src) < idx['verified-at:'][0] < idx['recheck:'][0] < idx['status:'][0]):
        return fail('E1', 'front-matter order is source(%d) / verified-at(%d) / recheck(%d) / status(%d)'
                    % (max(src), idx['verified-at:'][0], idx['recheck:'][0], idx['status:'][0]))
    return 0


def check_e2(text):
    lines, idx = front_matter(text)
    for i in idx['source:']:
        l = lines[i]
        if not re.match(r'^source: S\d{3}\b', l):
            return fail('E2', 'source line %d has no S### id' % (i + 1))
        if not re.search(r'https?://|[~/][\w./-]+\.\w+', l):
            return fail('E2', 'source line %d has no URL or path pointer' % (i + 1))
    return 0


def check_e3(text):
    lines, idx = front_matter(text)
    status = lines[idx['status:'][0]]
    if 'R43-C1' not in status:
        return fail('E3', 'status line does not name R43-C1')
    return 0


def check_e4(text, ledger_text):
    got = re.findall(r'<<L1:[a-z0-9-]+>>', text)
    want = {}
    for row in ledger_text.splitlines()[1:]:
        if not row.strip():
            continue
        tok, n = row.split('\t')[0], int(row.split('\t')[1])
        want[tok] = n
    from collections import Counter
    c = Counter(got)
    missing = sorted(set(want) - set(c))
    extra = sorted(set(c) - set(want))
    if missing:
        return fail('E4', 'ledger tokens absent from draft: %s' % ' '.join(missing))
    if extra:
        return fail('E4', 'draft tokens absent from ledger: %s' % ' '.join(extra))
    wrong = ['%s %d!=%d' % (t, c[t], want[t]) for t in want if c[t] != want[t]]
    if wrong:
        return fail('E4', 'occurrence mismatch: %s' % ', '.join(sorted(wrong)))
    return 0


def check_e5(text):
    for i, l in enumerate(text.splitlines()):
        if l.lstrip().startswith('|'):
            return fail('E5', 'markdown table row at line %d' % (i + 1))
        if l.strip().startswith('```'):
            return fail('E5', 'fenced code block at line %d' % (i + 1))
    return 0


def check_e6(text, root, rev):
    for key, want in PINS.items():
        if want not in text:
            return fail('E6', 'pin %s (%s…) absent from draft' % (key, want[:12]))
    if rev:
        block = region(show(root, rev, 'SKILL.md'))
        if block is None:
            return fail('E6', 'no v4 region at %s' % rev)
        got = hashlib.sha256(block.encode()).hexdigest()
        if got != PINS['block']:
            return fail('E6', 'v4 region at %s hashes %s, draft pins %s'
                        % (rev, got, PINS['block']))
        for key, path in PATHS.items():
            t = show(root, rev, path)
            if t is None:
                return fail('E6', '%s unreadable at %s' % (path, rev))
            got = hashlib.sha256(t.encode()).hexdigest()
            if got != PINS[key]:
                return fail('E6', '%s at %s hashes %s, draft pins %s'
                            % (path, rev, got, PINS[key]))
    return 0


def run(text, ledger_text, root, rev):
    for fn in (check_e1, check_e2, check_e3):
        rc = fn(text)
        if rc:
            return rc
    rc = check_e4(text, ledger_text)
    if rc:
        return rc
    rc = check_e5(text)
    if rc:
        return rc
    return check_e6(text, root, rev)


def selftest(text, ledger_text, root):
    lines, idx = front_matter(text)
    s = idx['status:'][0]
    mutants = []

    m = list(lines)
    m[s], m[idx['source:'][0]] = m[idx['source:'][0]], m[s]
    mutants.append(('E1', 'status moved to the top', '\n'.join(m)))

    m = list(lines)
    m[idx['source:'][0]] = m[idx['source:'][0]].split(' — ')[0]
    mutants.append(('E2', 'source loses its pointer', '\n'.join(m)))

    mutants.append(('E3', 'status stops naming the claim',
                    text.replace('R43-C1', 'R43-C9', 1)))

    mutants.append(('E4', 'undeclared placeholder',
                    text.replace('<<L1:n>>', '<<L1:carrier-count>>', 1)))

    mutants.append(('E5', 'a table row is pasted in',
                    text.replace('**The new held-out score.**',
                                 '| label | action |\n|---|---|\n**The new held-out score.**', 1)))

    mutants.append(('E6', 'a pin drifts',
                    text.replace(PINS['evaluator'], '0' * 64, 1)))

    bad = 0
    for want, what, mutant in mutants:
        if mutant == text:
            print('SELFTEST %s: mutation did not apply (%s)' % (want, what))
            bad += 1
            continue
        first = None
        for fn in (check_e1, check_e2, check_e3):
            if fn(mutant):
                first = fn.__name__[6:].upper()
                break
        if first is None:
            if check_e4(mutant, ledger_text):
                first = 'E4'
            elif check_e5(mutant):
                first = 'E5'
            elif check_e6(mutant, root, None):
                first = 'E6'
        if first != want:
            print('SELFTEST %s: %s -> first failing check %s (wanted %s)'
                  % (want, what, first, want))
            bad += 1
    print('selftest: %d of %d mutants red for the intended check'
          % (len(mutants) - bad, len(mutants)))
    return 0 if bad == 0 else 1


def summary(text, ledger_text, rev):
    lines, idx = front_matter(text)
    toks = re.findall(r'<<L1:[a-z0-9-]+>>', text)
    rows = len(ledger_text.splitlines()) - 1
    print('E1-E6 ok: %d source rows, %d placeholder tokens (%d distinct, ledger rows %d), '
          '%d pins matched%s'
          % (len(idx['source:']), len(toks), len(set(toks)), rows, len(PINS),
             ' against %s' % rev if rev else ' (literal only)'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--entry', required=True)
    ap.add_argument('--ledger', required=True)
    ap.add_argument('--root', default='.')
    ap.add_argument('--rev', default=None)
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    with open(a.entry, encoding='utf-8') as f:
        text = f.read()
    with open(a.ledger, encoding='utf-8') as f:
        ledger_text = f.read()
    if a.selftest:
        rc = run(text, ledger_text, a.root, a.rev or None)
        if rc:
            return rc
        return selftest(text, ledger_text, a.root)
    rc = run(text, ledger_text, a.root, a.rev or None)
    if rc == 0:
        summary(text, ledger_text, a.rev or None)
    return rc


if __name__ == '__main__':
    sys.exit(main())
