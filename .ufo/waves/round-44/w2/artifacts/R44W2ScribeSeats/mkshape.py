import json,sys,os
A=sys.argv[1]
v=json.load(open(os.path.join(A,'verify.json')))
def mix(w): return v[w]['spec']['roles']
r1,r2=mix('w1'),mix('w2')
round_mix={k:r1.get(k,0)+r2.get(k,0) for k in sorted(set(r1)|set(r2))}
shape={
 "seat":"R44W2ScribeSeats","round":44,
 "as_of_utc":v['as_of_utc'],
 "shape":"two v1 waves (both dispatches under policy v1: waveMinLanes 32 / waveMaxLanes 64)",
 "waves":[{"wave":"r44-w1","seats":v['w1']['spec']['count'],"roles":r1,
           "dispatched_local":v['w1']['dispatched']['timestamp_line'],
           "dead_seats":[],"reports_landed":v['w1']['results']['reports_present']},
          {"wave":"r44-w2","seats":v['w2']['spec']['count'],"roles":r2,
           "dispatched_local":v['w2']['dispatched']['timestamp_line'],
           "dead_seats":"not determinable (in flight; r44-w2-results.json absent)",
           "reports_landed":0}],
 "round_total":v['bands']['round_total'],
 "round_mix":round_mix,
 "attack_share":{k:v['attack_share'][k] for k in
   ('narrow_role_set','wide_role_set','w1_narrow','w2_narrow','round_narrow','w1_wide','w2_wide','round_wide')},
 "residual_call":v['residual'],
 "bands":{k:v['bands'][k] for k in ('w1_in_v1_band','w2_in_v1_band','round_total_within_32_128','both_waves_one_taskcall')},
}
sys.stdout.write(json.dumps(shape,indent=1,sort_keys=True)+"\n")
