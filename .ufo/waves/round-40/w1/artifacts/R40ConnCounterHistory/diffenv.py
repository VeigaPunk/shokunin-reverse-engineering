import json, sys
def walk(a, b, path=''):
    diffs = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: diffs.append((path + '.' + k, '<absent>', b[k]))
            elif k not in b: diffs.append((path + '.' + k, a[k], '<absent>'))
            else: diffs += walk(a[k], b[k], path + '.' + k)
    elif isinstance(a, list) and isinstance(b, list):
        if a != b:
            diffs.append((path, 'list len %d' % len(a), 'list len %d' % len(b)))
    elif a != b:
        diffs.append((path, a, b))
    return diffs
e1 = json.load(open(sys.argv[1])); e2 = json.load(open(sys.argv[2]))
for p, a, b in walk(e1, e2):
    s = json.dumps(a)
    print(p, '|', s[:150], '|', json.dumps(b)[:150])
