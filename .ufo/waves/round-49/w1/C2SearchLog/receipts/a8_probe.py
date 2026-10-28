import importlib.util, sys, json
D = '/fast/scratch/hyaku/kaidoku-r49/C2SearchLog/clone'
AF = '77580bf4503066fa093564641026e761bb4b34bb'
spec = importlib.util.spec_from_file_location('c2m', D + '/tools/round-49/c2-mismatch.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
r = m.Git(D)
reg = r.show(AF, 'corpus/SOURCES.md').decode()
R49 = '- 2026-10-28 round 49 — Question: do the S145/S146 locators and rationale survive a re-open? identified 2, screened 2, included 2, excluded 0; rows 146 → 148.'
R48 = '- 2026-10-28 round 48 (late entry, written in round 49) — Question: which source grounds the falsifiability criterion for a check, and does sysexits ground exit 2? identified 2, screened 2, included 1, excluded 1; rows 144 → 146.'
assert R49 in reg and R48 in reg, 'entries not found verbatim'
ROW149 = '| S149 | Padded test row — https://example.invalid/padded | docs | C | padding | x | REJECTED: padded; flip: none | rejected | 2026-10-28 | on-release | — |'
s148 = [l for l in reg.split('\n') if l.startswith('| S148 ')][0]
cases = {
 'T0_green_baseline': (reg, None),
 'T1_identified_999': (reg.replace('identified 2, screened 2, included 2, excluded 0; rows 146', 'identified 999, screened 2, included 2, excluded 0; rows 146'), None),
 'T2_included_excluded_swapped': (reg.replace('included 2, excluded 0; rows 146', 'included 1, excluded 1; rows 146'), None),
 'T3_round48_rows_wrong': (reg.replace('rows 144 → 146', 'rows 144 → 145'), None),
 'T4_padded_rejected_row': (reg.replace('identified 2, screened 2, included 2, excluded 0; rows 146 → 148.', 'identified 3, screened 3, included 2, excluded 1; rows 146 → 149.').replace(s148, s148 + '\n' + ROW149), None),
 'T5_S148_status_queued': (reg.replace(s148, s148.replace('| mined |', '| queued |')), None),
 'T6_round49_date_wrong': (reg.replace('- 2026-10-28 round 49', '- 2026-10-27 round 49'), None),
 'T7_identified_below_screened': (reg.replace('identified 2, screened 2, included 2', 'identified 1, screened 2, included 2'), None),
 'T8_semicolon_format': (reg.replace('identified 2, screened 2, included 2, excluded 0; rows 146 → 148', 'identified 2; screened 2; included 2; excluded 0; rows 146 → 148'), None),
}
out = {}
for k, (t, _) in cases.items():
    ov = {'corpus/SOURCES.md': t.encode()}
    got = m.score(m.Overlay(r, AF, ov), AF)
    out[k] = {'A8': got['A8'], 'other_red': sorted(a for a, v in got.items() if v and a != 'A8'), 'same_bytes_as_rev': t.encode() == r.show(AF, 'corpus/SOURCES.md')}
# T9: move round-49 entry out of Search log into Leads
t9 = reg.replace(R49 + '\n', '', 1).replace('## Leads (unopened)', '## Leads (unopened)\n\n' + R49, 1)
got = m.score(m.Overlay(r, AF, {'corpus/SOURCES.md': t9.encode()}), AF)
out['T9_entry_moved_to_leads'] = {'A8': got['A8'], 'other_red': sorted(a for a, v in got.items() if v and a != 'A8')}
# battery mutation inventory
muts = m.mutations(r, AF)
out['battery_mutation_labels'] = [(l, a) for l, a, _ in muts]
print(json.dumps(out, ensure_ascii=False, indent=1))
