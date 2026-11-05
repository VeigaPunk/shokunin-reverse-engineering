import importlib.util, json, os, shutil, sys, tempfile

CLONE = "/fast/scratch/hyaku/kaidoku-r95/SentinelWrite/clone"
S = "/fast/scratch/hyaku/kaidoku-r95/SentinelWrite"
spec = importlib.util.spec_from_file_location("v5", os.path.join(CLONE, "tools/round-95/stop-boundary-repair-battery-v5.py"))
v5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(v5)

base = os.path.join(S, "exp")
shutil.rmtree(base, ignore_errors=True)
os.makedirs(base)
rec = {"label": "x", "met_target": False, "exit": 1, "counts": {}, "revision": "b" * 40}


def show(tag, **kw):
    print(tag, json.dumps(kw, sort_keys=True))


# (b) pre-created receipt path is a symlink to a victim
d = os.path.join(base, "b")
os.makedirs(d)
victim = os.path.join(d, "victim.txt")
open(victim, "wb").write(b"VICTIM-B\n")
target = os.path.join(d, "receipt.json")
os.symlink(victim, target)
v5.write_receipt(target, {"k": 1})
show("B", victim_unchanged=open(victim, "rb").read() == b"VICTIM-B\n",
     target_is_symlink=os.path.islink(target), target_is_regular=os.path.isfile(target) and not os.path.islink(target),
     target_json=json.load(open(target)), leftovers=[n for n in os.listdir(d) if n.endswith(".tmp")])

# (b2) pre-created receipt path is a dangling symlink to a non-existent target outside dir
d2 = os.path.join(base, "b2")
os.makedirs(d2)
outside = os.path.join(base, "outside-not-created.json")
t2 = os.path.join(d2, "receipt.json")
os.symlink(outside, t2)
v5.write_receipt(t2, {"k": 2})
show("B2-dangling", outside_created=os.path.exists(outside), target_is_symlink=os.path.islink(t2))

# (c) O_EXCL: force mkstemp to collide with a planted symlink at the chosen name
d3 = os.path.join(base, "c")
os.makedirs(d3)
victim3 = os.path.join(d3, "victim3.txt")
open(victim3, "wb").write(b"VICTIM-C\n")
fixed = "FIXEDNAME"
orig_next = v5.tempfile._RandomNameSequence.__next__
v5.tempfile._RandomNameSequence.__next__ = lambda self: fixed
os.symlink(victim3, os.path.join(d3, "receipt.json." + fixed + ".tmp"))
err = None
try:
    v5.write_receipt(os.path.join(d3, "receipt.json"), {"k": 3})
except Exception as e:
    err = type(e).__name__
finally:
    v5.tempfile._RandomNameSequence.__next__ = orig_next
show("C-excl", error=err, victim_unchanged=open(victim3, "rb").read() == b"VICTIM-C\n",
     receipt_exists=os.path.exists(os.path.join(d3, "receipt.json")))

# (c2) mkstemp mode and name shape from the real writer
d4 = os.path.join(base, "c2")
os.makedirs(d4)
p4 = os.path.join(d4, "receipt.json")
v5.write_receipt(p4, {"k": 4})
st = os.stat(p4)
names = [n for n in os.listdir(d4)]
show("C2-mode", mode_octal=oct(st.st_mode & 0o777), names=names)

# (a) receipt parent directory is a symlink to another directory (user-named path)
real = os.path.join(base, "realdir")
os.makedirs(real)
link = os.path.join(base, "linkdir")
os.symlink(real, link)
v5.write_receipt(os.path.join(link, "receipt.json"), {"k": 5})
show("A-parent-symlink", landed_in_real=os.listdir(real), link_dir_is_link=os.path.islink(link))

# (d-fail) failing serialization leaves no target and no temp
d5 = os.path.join(base, "d5")
os.makedirs(d5)
try:
    v5.write_receipt(os.path.join(d5, "r.json"), {"x": object()})
    e5 = None
except TypeError as e:
    e5 = "TypeError"
show("D-fail-closed", error=e5, names=os.listdir(d5))
