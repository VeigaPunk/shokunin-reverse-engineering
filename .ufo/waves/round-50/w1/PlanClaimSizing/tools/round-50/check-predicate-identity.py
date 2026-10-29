#!/usr/bin/env python3
"""check-predicate-identity.py (PlanClaimSizing draft, wave 1; for the L1 to run at freeze).

Predicate identity (round-prompt section 9): the predicate sentence in the plan and the counter's
module docstring must be the same text. Whitespace, backticks and bold markers are normalised on
both sides; the plan body is the text after the `**Predicate <LABEL>**` / `**Predicate <LABEL>.**`
token up to the first bullet line (`- ...`) that follows it. Exit 0 = plan body is a substring of
the docstring; 1 = not; 2 = could not evaluate (label or docstring missing).

usage: check-predicate-identity.py --plan PLAN --label P50-C1 --counter COUNTER
"""
import argparse, ast, difflib, re, sys

def norm(s):
    s = s.replace('`', '').replace('**', '')
    return re.sub(r'\s+', ' ', s).strip()

def plan_body(text, label):
    m = re.search(r'\*\*Predicate ' + re.escape(label) + r'\*?\*?\.?\*?\*?', text)
    if not m:
        return None
    rest = text[m.end():]
    # the predicate sentence starts at its first 'At the measured revision' / 'At REV' phrase;
    # a parenthetical attribution before it is not part of the predicate
    k = re.search(r'At the measured revision|At REV,', rest)
    if k:
        rest = rest[k.start():]
    out = []
    for line in rest.split('\n'):
        if line.startswith('- ') and out:
            break
        out.append(line)
    return norm(' '.join(out))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--plan', required=True)
    ap.add_argument('--label', required=True)
    ap.add_argument('--counter', required=True)
    a = ap.parse_args()
    try:
        text = open(a.plan, encoding='utf-8').read()
        src = open(a.counter, encoding='utf-8').read()
    except OSError as e:
        print('could-not-evaluate:', e); return 2
    body = plan_body(text, a.label)
    doc = ast.get_docstring(ast.parse(src))
    if not body or not doc:
        print('could-not-evaluate: label or docstring missing'); return 2
    d = norm(doc)
    if body in d:
        print('identical:', a.label, 'len', len(body)); return 0
    # first divergence, for the report
    sm = difflib.SequenceMatcher(None, body, d, autojunk=False)
    blocks = [b for b in sm.get_matching_blocks() if b.size > 0]
    longest = max(blocks, key=lambda b: b.size) if blocks else None
    print('not-identical:', a.label, 'plan_len', len(body), 'longest_common_run', longest.size if longest else 0)
    return 1

if __name__ == '__main__':
    sys.exit(main())
