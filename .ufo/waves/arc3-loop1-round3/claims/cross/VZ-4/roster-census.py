#!/usr/bin/env python3
"""VZ-4 roster census — parse the frozen roster mechanically and count delivered seat reports.

Roster source: .ufo/waves/arc3-loop1-round3/claims-frozen.md (the `## Roster` section).
Count is against THIS wave's frozen roster artifact (r5 counting lesson).
Mechanical: chain headers define blocks; seat names are `[A-Z]{2}-\d+` tokens in each block.
"""
import pathlib, re, sys

WAVE = pathlib.Path(__file__).resolve().parents[3]  # .ufo/waves/arc3-loop1-round3
FROZEN = WAVE / 'claims-frozen.md'
SEATS = WAVE / 'seats'

text = FROZEN.read_text()
roster_sec = text.split('## Roster (64 seats, enumerated)', 1)[1]

chained, cur = {}, None
for line in roster_sec.splitlines():
    if re.match(r'^(Cross|[Cc]\d) ?chain \(\d+\)', line) or re.match(r'^Cross \(\d+\)', line):
        cur = line.split(':')[0].strip()
        chained[cur] = []
    elif line.startswith('Counts:') or line.startswith('Assertions') or line.startswith('## '):
        cur = None
    if cur is not None:
        chained[cur] += re.findall(r'\b([A-Z]{2}-\d+)\b', line)

all_seats = []
for head in chained:
    seen, uniq = set(), []
    for s in chained[head]:
        if s not in seen:
            seen.add(s); uniq.append(s)
    chained[head] = uniq
    all_seats += uniq

out = []
for head in chained:
    out.append(f'  {head}: {len(chained[head])} :: {", ".join(chained[head])}')
out.append(f'TOTAL roster seats: {len(all_seats)} unique={len(set(all_seats))}')
assert len(all_seats) == 64, f'roster parse broke: {len(all_seats)} != 64'
assert len(set(all_seats)) == 64, 'duplicate seat names in roster'

delivered = {p.stem for p in SEATS.glob('*.md')} if SEATS.exists() else set()
zero_byte = [p.name for p in SEATS.glob('*.md') if p.stat().st_size == 0] if SEATS.exists() else []
stray = sorted(delivered - set(all_seats))
missing_files = [s for s in all_seats if s not in delivered]
out.append(f'DELIVERED: {len(delivered & set(all_seats))}/{len(all_seats)}')
out.append(f'UNDELIVERED ({len(missing_files)}): {", ".join(missing_files) if missing_files else "none"}')
out.append(f'STRAY seat files (not on roster): {stray if stray else "none"}')
out.append(f'ZERO-BYTE seat reports: {zero_byte if zero_byte else "none"}')
for head in chained:
    u = [s for s in chained[head] if s not in delivered]
    out.append(f'  {head}: {len(chained[head])-len(u)}/{len(chained[head])}' + (f' undelivered: {", ".join(u)}' if u else ' COMPLETE'))
print('\n'.join(out))