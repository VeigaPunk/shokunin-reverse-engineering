# Captures REA 6.5.0 envelopes for the four scored carriers into scratch via the
# draft counter's own real runner (make_real_runner). Usage: capture.py <clone> <outdir>
import importlib.util, json, os, sys, time
clone, outdir = sys.argv[1], sys.argv[2]
os.environ.setdefault('HYAKU_SCRATCH', '/fast/scratch/hyaku')
spec = importlib.util.spec_from_file_location('c1c', os.path.join(clone, 'tools/round-49/c1-counter.py'))
c1c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c1c)
car = json.load(open(os.path.join(clone, 'tools/round-49/carriers.json')))
scored = car['carriers']
work = os.path.join(outdir, 'work'); os.makedirs(work, exist_ok=True)
run = c1c.make_real_runner(work, None, 900)
for c in scored:
    raw = open(os.path.join(clone, c['path']), 'rb').read()
    st, payload = run(raw, c['id'], {'max_depth': 3})
    d = os.path.join(outdir, c['id']); os.makedirs(d, exist_ok=True)
    json.dump(payload, open(os.path.join(d, 'after.json'), 'w'), indent=1, sort_keys=True)
    print(c['id'], st, payload.get('parameters', {}).get('output_directory') if isinstance(payload, dict) else type(payload), time.strftime('%H:%M:%S'))
