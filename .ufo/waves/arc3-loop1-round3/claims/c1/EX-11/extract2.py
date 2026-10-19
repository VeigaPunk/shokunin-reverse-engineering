import sys, json, hashlib, itertools, re

def envelope(b):
    if b.startswith(b'{"ok":true,"data":'):
        body = b[len(b'{"ok":true,"data":'):]
        i = body.rfind(b',"meta":')
        assert i != -1
        return body[:i]
    return b.rstrip(b'\n')

files = sys.argv[1:]
rows = []
for f in files:
    b = open(f,'rb').read()
    env = envelope(b)
    d = json.loads(env)
    rows.append(dict(name=f.split('/')[-1], stdout=len(b), envlen=len(env),
                     envsha=hashlib.sha256(env).hexdigest(), id=d.get("evidence_id"), d=d))
for r in rows:
    print(f"{r['name']}  stdout={r['stdout']}  env={r['envlen']}  env_sha256={r['envsha']}")
    print(f"    id={r['id']} prov={r['d']['provider']['version']} path={r['d']['parameters']['path']}")
print("\npairwise envelope cmp:")
for (a,b) in itertools.combinations(rows,2):
    print(f"  {a['name']} vs {b['name']}: {'IDENTICAL' if a['envsha']==b['envsha'] else 'DIFFER'}")
print("\nfunction payload check:")
for r in rows:
    nf = r['d']['normalized_result']['functions']
    print(f"  {r['name']}: n={len(nf)} sels={sorted(x['selector'] for x in nf)} bsha={r['d']['normalized_result']['bytecode']['sha256'][:16]}")
