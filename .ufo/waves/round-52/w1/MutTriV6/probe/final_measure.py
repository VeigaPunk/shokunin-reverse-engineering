"""Score the FOUR committed round-50 control surfaces with the v6 evaluator.

The committed receipts (.ufo/waves/round-50/c3/ctl-*.json) were produced with the
v5 evaluator.  The v6 evaluator changes the ddwrt route, so the numbers move.
"""
import sys, os, json
sys.path.insert(0,'/fast/scratch/hyaku/kaidoku-r52/w1-MutTriV6')
import proto_v6 as P
LANE='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
corpus=P.load_corpus(); fixtures=P.v6_fixtures()

def score_text(text):
    rules,info=P.v5.parse_skill(text)
    mism=[]
    for eid,_p,f in corpus:
        lab,act=P.v5.decision(P.v5.classify(rules,f))
        ev=P.evaluate_v6(f)[:2]
        if (lab,act)!=ev: mism.append(eid)
    return info, mism, P.audit_executability(rules,corpus)

SURFACES={
 'ctl-do-nothing':   LANE+'/.ufo/waves/round-50/c3/ctl-do-nothing.skill.md',
 'ctl-junk':         LANE+'/.ufo/waves/round-50/c3/ctl-junk.skill.md',
 'ctl-guard-deleted':LANE+'/.ufo/waves/round-50/w3/ExecTriageControls/ctl-guard-deleted.skill.md',
 'ctl-action-swapped':LANE+'/.ufo/waves/round-50/w3/ExecTriageControls/ctl-action-swapped.skill.md',
}
for name,path in SURFACES.items():
    if not os.path.exists(path):
        print('%-22s MISSING %s' % (name,path)); continue
    committed=json.load(open(LANE+'/.ufo/waves/round-50/c3/%s.json'%name))['pair_mismatch_count']
    try:
        info,m,a=score_text(open(path,encoding='utf-8').read())
    except Exception as e:
        print('%-22s committed(v5)=%-4s PARSE-REFUSED: %s' % (name,committed,e)); continue
    print('%-22s committed(v5)=%-4s under v6=%-4d audit=%-2d  rules=%d  %s' % (
        name,committed,len(m),len(a),info['rules'],
        [x['envelope'] for x in a]))
