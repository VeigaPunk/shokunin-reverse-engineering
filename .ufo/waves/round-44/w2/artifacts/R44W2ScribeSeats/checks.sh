#!/usr/bin/env bash
# R44W2ScribeSeats — role validity, host clock and wave-file presence.
set -u
W=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44
echo "host_local=$(date '+%Y-%m-%dT%H:%M:%S%z')"
echo "host_utc=$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
python3 - "$W" <<'PY'
import json,sys,os,datetime
W=sys.argv[1]
pol=json.load(open('/home/vgpnk/Projects/shokunin/scripts/hyaku/ufo-wave-policy.json'))
allowed=set(pol['nativeProfiles']['omp-native-v1']['proposalRoles'])
print('allowed_proposal_roles='+','.join(sorted(allowed)))
for w in ('w1-spec.json','w2-spec.json'):
    items=json.load(open(os.path.join(W,w)))['items']
    roles={i['role'] for i in items}
    print(f'{w}: seats={len(items)} roles_outside_policy={sorted(roles-allowed)}')
for f in ('w1.ready.dispatched','w2.ready.dispatched','w1-spec.json','w2-spec.json','w2-dispatch.json','r44-w1-results.json'):
    p=os.path.join(W,f)
    print(f'{f}: exists={os.path.exists(p)} bytes={os.path.getsize(p) if os.path.exists(p) else 0} mtime_local={datetime.datetime.fromtimestamp(os.path.getmtime(p)).isoformat() if os.path.exists(p) else "n/a"}')
print('r44-w2-results.json: exists=%s' % os.path.exists(os.path.join(W,'r44-w2-results.json')))
PY
