#!/usr/bin/env python3
"""R38ReviewerEntryQuality — mechanical checks of the drafted C1 entry.

Checks (reported, never repaired):
  1. every S-id cited on a `source:` line exists in the append block or the registry;
  2. the counter's `sourced` binding is satisfiable: >=1 cited row opened 2026-10-26
     whose used-by contains the entry path;
  3. provenance trio (source:/verified-at:/recheck:) opens the entry, source first;
  4. quoted spans in the entry are <=25 words (heuristic: text inside "..." or > ...);
  5. crude credential-material scan (private keys, Authorization, api keys, tokens);
  6. observation/inference/unknown label presence.
"""
import re, sys

ENTRY_RE = re.compile(r'(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])')
ROW_RE = re.compile(r'^ {0,3}\|\s*(S\d{3,})\s*\|')


def cells(line):
    return [c.strip() for c in line.strip().strip('|').split('|')]


def load_rows(path):
    rows = {}
    if not path:
        return rows
    for line in open(path, encoding='utf-8', errors='replace'):
        m = ROW_RE.match(line)
        if not m:
            continue
        c = cells(line)
        if len(c) == 11:
            rows[c[0]] = {'opened': c[8], 'status': c[7], 'usedby': c[10], 'raw': line.rstrip('\n')}
    return rows


def quoted_spans(text):
    spans = []
    spans += re.findall(r'"([^"\n]{3,400})"', text)
    spans += re.findall(r'`([^`\n]{3,400})`', text)
    spans += re.findall(r'>\s*([^\n]{3,400})', text)
    return spans


def main():
    entry, block, registry = sys.argv[1], sys.argv[2], sys.argv[3]
    text = open(entry, encoding='utf-8', errors='replace').read()
    lines = text.splitlines()
    rows = load_rows(block)
    rows.update(load_rows(registry))  # registry must not shadow block ids; block wins only if absent
    block_rows = load_rows(block)
    reg_rows = load_rows(registry)

    src_ids = set()
    trio = []
    for i, l in enumerate(lines):
        if l.startswith('source:'):
            src_ids |= set(ENTRY_RE.findall(l))
            trio.append(('source', i + 1))
        elif l.startswith('verified-at:'):
            trio.append(('verified-at', i + 1))
        elif l.startswith('recheck:'):
            trio.append(('recheck', i + 1))

    print('== source: line ids:', sorted(src_ids))
    missing = sorted(i for i in src_ids if i not in rows)
    print('== cited ids absent from append block AND registry:', missing or 'NONE')
    ok = [i for i in src_ids if i in rows and rows[i]['opened'] == '2026-10-26'
          and 'corpus/knowledge/2026-10-26-r38-sasquatch-be-squashfs-recursion.md' in rows[i]['usedby']]
    print('== rows satisfying counter sourced binding:', sorted(ok) or 'NONE')
    for i in sorted(src_ids):
        if i in block_rows:
            r = block_rows[i]
            print(f'   {i}: block row status={r["status"]} opened={r["opened"]} usedby-ok={r["entry" if False else "usedby"].strip()[-60:]}')
        elif i in reg_rows:
            r = reg_rows[i]
            print(f'   {i}: REGISTRY row status={r["status"]} opened={r["opened"]} usedby={r["usedby"][:60]}')

    print('== provenance trio order:', trio[:6])
    long_quotes = [(w, s[:80]) for s in quoted_spans(text) for w in [len(s.split())] if w > 25]
    print('== quoted spans >25 words:', len(long_quotes))
    for w, s in long_quotes[:10]:
        print(f'   {w} words: {s}...')

    cred = re.findall(r'(?i)(BEGIN [A-Z ]*PRIVATE KEY|authorization[: ]|api[_-]?key|secret[_-]?token|password\s*=)', text)
    print('== credential-material hits:', cred or 'NONE')
    for lab in ('observation', 'inference', 'unknown', 'INFERENCE', 'OBSERVED', '[FACT]'):
        n = len(re.findall(lab, text, re.I))
        print(f'== label "{lab}": {n}')


if __name__ == '__main__':
    main()
