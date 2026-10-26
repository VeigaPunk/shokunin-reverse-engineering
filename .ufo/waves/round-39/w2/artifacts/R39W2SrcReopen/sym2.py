import os, tempfile
from pathlib import Path
from unblob.extractor import fix_symlink
class TR:
    def __init__(s): s.reports=[]
    def add_report(s,r): s.reports.append(r)
d=Path(tempfile.mkdtemp(dir=os.environ['TMPDIR'])).resolve(); out=d/'out'; out.mkdir()
os.symlink('b',out/'a'); os.symlink('a',out/'b')
for n in 'ab':
    tr=TR(); fix_symlink(out/n,out,tr); print(n,os.path.lexists(out/n),[ (type(r).__name__, r.link, r.target) for r in tr.reports])
