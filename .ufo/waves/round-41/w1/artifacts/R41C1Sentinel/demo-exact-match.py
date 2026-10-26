def extract_rel(path):
    if not isinstance(path, str): return None
    p = path
    while p.startswith('$output/'): p = p[len('$output/'):]
    parts = [x for x in p.split('/') if x not in ('', '.')]
    if parts and parts[0].endswith('_extract'): parts = parts[1:]
    return '/'.join(parts)

def same_rel(candidate, rel):
    return bool(rel) and bool(candidate) and extract_rel(candidate) == rel

cases = [
 ('R40-CL1 direction A: regular usr/bin/busy vs symlink bin/busy',
  'firmware.bin_extract/usr/bin/busy', 'bin/busy', False),
 ('R40-CL1 direction B: regular bin/busy vs symlink usr/bin/busy',
  'firmware.bin_extract/bin/busy', 'usr/bin/busy', False),
 ('exact hit', 'firmware.bin_extract/bin/busy', 'bin/busy', True),
 ('$output prefix', '$output/firmware.bin_extract/bin/busy', 'bin/busy', True),
 ('absolute outdir', '/abs/out/firmware.bin_extract/etc/version', 'etc/version', True),
 ('nested extract keeps inner root', 'a_extract/b_extract/x', 'x', False),
 ('dot-dot cannot climb out', 'firmware.bin_extract/../bin/busy', 'bin/busy', False),
 ('no _extract root at all', 'bin/busy', 'bin/busy', True),
 ('empty oracle row', 'firmware.bin_extract/bin/busy', '', False),
 ('None candidate', None, 'bin/busy', False),
 ('prefix-suffix confusion', 'firmware.bin_extract/usr/libbin/busy', 'bin/busy', False),
]
bad=0
for name, cand, rel, want in cases:
    got = same_rel(cand, rel)
    ok = got == want
    bad += not ok
    print('%s %-58s got=%-5s want=%-5s' % ('PASS' if ok else 'FAIL', name, got, want))
print('cases=%d fail=%d' % (len(cases), bad))
