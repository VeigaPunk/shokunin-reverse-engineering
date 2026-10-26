import json,sys
n=sys.argv[1]
r=json.load(open(f'r_{n}/rep.json'))
def walk(o,d=0):
    if isinstance(o,dict):
        t=o.get('__typename__')
        if t and t not in('StatReport','FileMagicReport','HashReport','RandomnessReport'):
            print(' '*d,t,{k:(v if not isinstance(v,(list,dict)) else '..') for k,v in o.items() if k not in('__typename__','id','path')})
        for v in o.values(): walk(v,d+1)
    elif isinstance(o,list):
        for v in o: walk(v,d)
walk(r)
