import json,os,glob
L='/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
spec=[it['name'] for it in json.load(open(L+'/.ufo/waves/round-44/w1-spec.json'))['items']]
w1=L+'/.ufo/waves/round-44/w1'
md={os.path.basename(p)[:-3] for p in glob.glob(w1+'/*.md')}
print('snapshot', __import__('datetime').datetime.now().astimezone().isoformat(timespec='seconds'))
print('seats',len(spec),'with .md',len([s for s in spec if s in md]))
print('missing',sorted(s for s in spec if s not in md))
