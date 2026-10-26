import os, sys, json
sys.path.insert(0, '/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages')
from pathlib import Path
from unblob.file_utils import is_safe_path

for root in sys.argv[1:]:
    outdir = Path(root).resolve()
    print('==', root, 'outdir', outdir)
    rows = []
    for dirpath, dnames, fnames in os.walk(root):
        for n in sorted(dnames + fnames):
            p = Path(dirpath) / n
            if not p.is_symlink():
                continue
            raw = os.readlink(p)
            if not raw:
                cls, note = 'escaping', 'empty target -> removed silently'
            else:
                t = Path(raw)
                if t.is_absolute():
                    t = Path(t.as_posix().lstrip('/'))
                else:
                    t = p.resolve()
                safe = is_safe_path(outdir, t)
                cls = 'in-tree' if safe else 'escaping'
                note = 'target resolves to %s ; is_safe_path=%s' % (t, safe)
            rel = p.relative_to(root).as_posix()
            rows.append((rel, raw, cls))
            print('  %-22s -> %-22s %-9s %s' % (rel, raw, cls, note))
    print('  classes:', {c: sum(1 for r in rows if r[2]==c) for c in ('in-tree','escaping')})
