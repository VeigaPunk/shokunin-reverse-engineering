# L1 in-memory check of the landed (7994eec7) needles against the text mutants of
# table1-rerun.md plus R12Reviewer's extras. The probe's `exact` kind is re.search on
# the pinned line (citation-drift-probe.py exact branch), so line delete/shift mutants
# are positional and needle-independent. Run from the lane root.
import json, re, subprocess
t = json.loads(subprocess.check_output(['git','show','6a35398:.ufo/gates/citation-drift/pointer-table.json']))
rows = {e['id']: e for e in t['entries'] if e['id'].startswith('pl4-')}
line = {k: subprocess.check_output(['git','show','6a35398:'+e['file']], text=True).splitlines()[e['line']-1] for k, e in rows.items()}
EVID = '`ev_ffd8f0b96a921dc2d42dbdc76546838494eebb0cdc02354d4d7570ef46acc052`'
M = {
 'r7': [('TMPDIR->/tmp','B','TMPDIR=/var/tmp/','TMPDIR=/tmp/'),('ev hex swap','B','ev_ffd8','ev_ffd9'),
        ('expected-id clause dropped','B',', expect '+EVID,''),('verb -legacy','B','inspect-evm-interface ','inspect-evm-interface-legacy '),
        ('verb -x','B','inspect-evm-interface ','inspect-evm-interface-x '),('fixture round7->round99','B','arc3-loop1-round7','arc3-loop1-round99'),
        ('fixture base->copyA','B','/fixtures/base/','/fixtures/copyA/'),('scratch dir -old','B','kaidoku-ex3-r7-recheck node','kaidoku-ex3-r7-recheck-old node'),
        ('trailing ws','H',None,'  '),('expect->yield','H','expect `','yield `'),('trailing note','H',None,' (note)'),
        ('disk-backed tail reworded','H','`TMPDIR` must be disk-backed here','scratch must be on disk')],
 'r10':[('mjs->py','B','recompute-ids.mjs','recompute-ids.py'),('script clause dropped','B','; then run `node .ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/recompute-ids.mjs`',''),
        ('rederive .txt->.md','B','rederive-commands.txt','rederive-commands.md'),('evidence/->evidence-old/','B','`evidence/','`evidence-old/'),
        ('round10->round99','B','arc3-loop1-round10','arc3-loop1-round99'),('claims/c1->c2','B','claims/c1/','claims/c2/'),
        ('trailing ws','H',None,'  '),('read-only->non-mutating','H','read-only','non-mutating'),('trailing note','H',None,' (note)'),
        ('; then run->; and then run','H','; then run','; and then run')],
 'r11':[('TMPDIR under /tmp','B','under `/var/tmp`','under `/tmp`'),('script clause dropped','B','Then run `python3 .ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence/recompute-ids.py`.',''),
        ('calls .txt->.md','B','calls.txt','calls.md'),('identity .txt->.md','B','identity.txt','identity.md'),
        ('/tmp tail dropped','B',' Do not use `/tmp` for scratch.',''),('round11->round99','B','arc3-loop1-round11','arc3-loop1-round99'),
        ('trailing ws','H',None,'  '),('byte-identical->identical','H','byte-identical copies','identical copies'),('trailing note','H',None,' (note)'),
        ('and run the four->then run the four','H','and run the four','then run the four')],
}
kb=hb=fa=sv=0
for r, muts in M.items():
    rid = f'pl4-{r}-recheck'; pat = rows[rid]['must_match']
    assert re.search(pat, line[rid]), rid
    for label, kind, old, new in muts:
        s = line[rid]
        if old is None: m = s + new
        else:
            assert old in s, (rid, label); m = s.replace(old, new, 1)
        killed = not re.search(pat, m)
        if kind=='B': kb+=1; sv += not killed
        else: hb+=1; fa += killed
        print(f"{rid} {kind} {label}: {'killed' if killed else 'survived'}")
print("positional mutants (line deleted / shifted, 2 per row) = 6, killed by construction")
print(f"breaking text mutants killed {kb-sv}/{kb}; harmless false alarms {fa}/{hb}")
