import json
p='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-44/w1.ready.dispatched'
lines=open(p).read().splitlines()
m=json.loads(lines[1])
print('dispatch stamp', lines[0])
print('seat count', len(m))
print('renamed (spec id -> dispatched id):', [(k,v) for k,v in m.items() if k!=v])
