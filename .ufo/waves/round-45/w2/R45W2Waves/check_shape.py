#!/usr/bin/env python3
"""R45W2Waves: round-shape verifier for kaidoku-shokunin round 45.
Read-only: opens only committed wave artefacts + the fleet dispatcher. Writes one JSON receipt.
Exit: 0 all checks met, 1 any check failed, 2 unreadable input.
"""
import json,os,sys,hashlib,datetime
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
W=os.path.join(LANE,'.ufo/waves/round-45')
ATTACK={'reviewer','critic','mutation-tester','labrat'}
def load(p): return json.load(open(p))
def txt(p): return open(p,encoding='utf-8',errors='replace').read()
def main(outp):
    d1=load(f'{W}/w1-dispatch.json'); d2=load(f'{W}/w2-dispatch.json')
    s1=load(f'{W}/w1-spec.json');    s2=load(f'{W}/w2-spec.json')
    r1=load(f'{W}/r45-w1-results.json')
    g1=load(f'{W}/w1/swarm-registry.json'); g2=load(f'{W}/w2/swarm-registry.json')
    n1=[t['name'] for t in d1['taskCall']['tasks']]; n2=[t['name'] for t in d2['taskCall']['tasks']]
    p1=[i['name'] for i in s1['items']]; p2=[i['name'] for i in s2['items']]
    k1=list(g1['members']); k2=list(g2['members'])
    led=[x['name'] for x in r1['results']]
    prod=[x for x in r1['results'] if not x.get('note')]
    dead=[x for x in r1['results'] if x.get('note')]
    deadnote=dead[0]['note'] if dead else ''
    def hist(rs):
        h={}
        for r in rs: h[r]=h.get(r,0)+1
        return dict(sorted(h.items()))
    c=[]
    def chk(name,pred,detail):
        c.append({'check':name,'exit':0 if pred else 1,'detail':detail})
    rh=hist(t['agent'] for t in d1['taskCall']['tasks']); r2h=hist(t['agent'] for t in d2['taskCall']['tasks'])
    ph=hist(x['agent'] for x in prod)
    share=lambda h,tot: round(sum(v for k,v in h.items() if k in ATTACK)/tot,4)
    chk('w1_dispatch_total_in_32_64', 32<=len(n1)<=64, len(n1))
    chk('w2_dispatch_total_in_32_64', 32<=len(n2)<=64, len(n2))
    chk('round_total_in_64_128', 64<=len(n1)+len(n2)<=128, len(n1)+len(n2))
    chk('w1_spec_eq_dispatch_names', sorted(p1)==sorted(n1), len(p1))
    chk('w1_registry_eq_dispatch_names', sorted(k1)==sorted(n1), len(k1))
    chk('w2_spec_eq_dispatch_names', sorted(p2)==sorted(n2), len(p2))
    chk('w2_registry_eq_dispatch_names', sorted(k2)==sorted(n2), len(k2))
    chk('w1_ledger_names_eq_dispatch', sorted(led)==sorted(n1), len(led))
    chk('w1_produced_in_32_64', 32<=len(prod)<=64, {'produced':len(prod),'dispatched':len(n1)})
    md=[f for f in os.listdir(f'{W}/w1') if f.endswith('.md')]
    chk('w1_report_md_eq_produced', len(md)==len(prod), {'md':len(md),'produced':len(prod)})
    chk('w1_attack_share_ge_25', share(rh,len(n1))>=0.25, share(rh,len(n1)))
    chk('w1_produced_attack_share_ge_25', share(ph,len(prod))>=0.25, share(ph,len(prod)))
    chk('w2_attack_share_ge_25', share(r2h,len(n2))>=0.25, share(r2h,len(n2)))
    chk('w1_connector_le_2', rh.get('connector',0)<=2, rh.get('connector',0))
    chk('w2_connector_le_2', r2h.get('connector',0)<=2, r2h.get('connector',0))
    keys=sorted({k for x in r1['results'] for k in x})
    chk('ledger_seats_field_eq_produced', r1['seats']==len(prod), {'seats_field':r1['seats'],'produced':len(prod)})
    chk('ledger_has_status_field', 'status' in keys, keys)
    chk('ledger_has_id_field', 'id' in keys, keys)
    chk('w2_results_exists', os.path.exists(f'{W}/r45-w2-results.json'), False)
    ctx=d2['taskCall']['context']
    chk('w2_context_names_A3', 'f59565b7' in ctx, [l[:220] for l in ctx.split('\n') if 'amendment' in l][:1])
    n_a3=sum(1 for t in d2['taskCall']['tasks'] if 'f59565b7' in t['task'])
    n_any=sum(1 for t in d2['taskCall']['tasks'] if any(s in t['task'] for s in ('f59565b7','fedd11bf','1f4b27f8','e715263c')))
    chk('w2_prompts_all_pin_a_revision', n_any==len(n2), {'with_revision':n_any,'with_A3':n_a3,'total':len(n2)})
    DISP='/home/vgpnk/Projects/shokunin/scripts/hyaku/inline-dispatcher.py'
    dt=txt(DISP)
    chk('ledger_note_emitted_by_committed_dispatcher', deadnote in dt, {'note':deadnote})
    chk('dispatcher_emits_canonical_dead_note', 'orchestrator kernel restarted mid-wave' in dt, 'inline-dispatcher.py:295')
    chk('dispatcher_full_fill_before_marker', 'if len(mine) < len(tasks):' in dt, 'inline-dispatcher.py:262-265')
    m1=txt(f'{W}/w1.ready.dispatched'); m2=txt(f'{W}/w2.ready.dispatched').splitlines()
    chk('w1_marker_matches_writer_format', '\n' in m1.strip(), {'first_line':m1.strip()[:40]})
    chk('w2_marker_matches_writer_format', len(m2)>1 and m2[0].startswith('20'), {'first_line':m2[0][:40],'ids':len(m2)-1})
    r35=load(f'{LANE}/.ufo/waves/round-35/w1-results.json')
    n35={x.get('note') for x in r35['results']}
    chk('round35_dead_note_is_harness_string', any('orchestrator kernel restarted' in (x or '') for x in n35), sorted((x or '')[:60] for x in n35))
    chk('round45_note_absent_from_all_other_lane_ledgers', deadnote and all(deadnote not in txt(os.path.join(dp,f))
        for dp,_,fs in os.walk(f'{LANE}/.ufo/waves') for f in fs if f.endswith('-results.json') and 'round-45' not in dp), deadnote[:60])
    out={'utc':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
         'lane_root':LANE,'checks':c,
         'counts':{'w1_dispatch':len(n1),'w1_produced':len(prod),'w1_dead':len(dead),
                   'w2_dispatch':len(n2),'w2_produced':None},
         'hist':{'w1_dispatched':rh,'w1_produced':ph,'w2_dispatched':r2h},
         'attack_share':{'w1_dispatched':share(rh,len(n1)),'w1_produced':share(ph,len(prod)),'w2_dispatched':share(r2h,len(n2))},
         'dead':[{'name':x['name'],'agent':x['agent'],'output':x['output'],'note':x['note']} for x in dead],
         'ledger_keys':keys,'ledger_seats_field':r1['seats'],
         'provenance':{'dispatcher':DISP,'dispatcher_sha256':hashlib.sha256(dt.encode()).hexdigest(),
                       'ledger_note':deadnote,'round35_notes':sorted(x for x in n35 if x)}}
    body=json.dumps(out,indent=1,sort_keys=True)+'\n'
    open(outp,'w').write(body)
    print(body); print('sha256',hashlib.sha256(body.encode()).hexdigest())
    print('fails',sum(1 for x in c if x['exit']))
    return 1 if any(x['exit'] for x in c) else 0
if __name__=='__main__':
    sys.exit(main(sys.argv[1]))
