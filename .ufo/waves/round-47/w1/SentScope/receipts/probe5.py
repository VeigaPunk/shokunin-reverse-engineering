import json, os, sys
L="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; S=os.environ["S"]; C=os.path.join(S,"lane")
sys.path.insert(0,L+"/tools/round-46"); sys.path.insert(0,L+"/tools/round-47")
import gate, record
rev="a631bba01633d2b5353306a569be4ce2e683d364"; files=lambda p: gate.show(C,rev,p); out={}
# 1. a `rev` correction whose key is an option-looking token
r=gate.git(C,"rev-parse","--verify","--quiet","--help^{commit}")
out["git_rev_parse_help_rc"]=r.returncode; out["git_rev_parse_help_out_head"]=(r.stdout or r.stderr)[:60]
entry={"class":"rev","key":"--help","statement":"x","text":"- corrects rev --help: x"}
out["corrects_rev_help"]=record.corrects(entry,files,C,rev,lambda n:({"x":0},None))
# 2. a window atom whose pathspec does not exist -> "is empty" is trivially true
atom={"class":"window","key":"46","line":"`git log 5017e1f..a631bba -- tools/round-47/does-not-exist/` is empty"}
ok,detail=record.derive(atom,files,C,rev,lambda n:(None,"x"))
out["bogus_pathspec_window"]={"ok":ok,"detail":detail}
atom2={"class":"window","key":"46","line":"`git log 5017e1f..a631bba -- prose words here` is empty"}
ok2,d2=record.derive(atom2,files,C,rev,lambda n:(None,"x"))
out["prose_pathspec_window"]={"ok":ok2,"detail":d2}
# 3. same window over the frozen path itself (what a real claim would say)
atom3={"class":"window","key":"46","line":"`git log 62e33f7..a631bba -- tools/round-47/` is empty"}
out["real_window"]=dict(zip(("ok","detail"),record.derive(atom3,files,C,rev,lambda n:(None,"x"))))
print(json.dumps(out,indent=1,sort_keys=True,default=str)[:2000])
