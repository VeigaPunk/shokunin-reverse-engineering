import os, tempfile, json
from pathlib import Path
from unblob.extractor import fix_symlink
from unblob.file_utils import is_safe_path
from unblob.models import TaskResult, Task
import inspect
print(inspect.signature(TaskResult.__init__) if hasattr(TaskResult,'__init__') else '')
class TR:
    def __init__(s): s.reports=[]
    def add_report(s,r): s.reports.append(r)
def run(name, target, mk=None):
    d=Path(tempfile.mkdtemp(dir=os.environ['TMPDIR'])).resolve()
    out=d/'out'; out.mkdir(); (out/'sub').mkdir(); (out/'sub'/'f').write_text('x')
    l=out/'sub'/'lnk'
    os.symlink(target,l)
    tr=TR()
    try: fix_symlink(l,out,tr); 
    except Exception as e: print(name,'EXC',repr(e)); return
    exists=os.path.islink(l)
    print(f"{name:28} target={target!r:22} kept={exists} link->{os.readlink(l) if exists else None} reports={[type(r).__name__ for r in tr.reports]}")
run('relative-in-tree','f')
run('relative-escape','../../../etc/passwd')
run('abs-in-root','/sub/f')
run('abs-outside(/etc)','/etc/passwd')
run('abs-dotdot','/../../etc/passwd')
run('abs-dotdot-in','/sub/../sub/f')
run('self-loop','lnk')
run('empty-target','')
