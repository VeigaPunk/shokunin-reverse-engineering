#!/usr/bin/env python3
"""Forgery F2 (round-93 control; mirrors the round-92 CHEAT-D over five
carriers): the round-92 repair's own window search with its packer verdict
(`upx_green`) replaced by membership against the five public carriers' packed
images, built fresh once per process. On any carrier outside the table the
verdict is never green, so the repair refuses - the round-93 fresh-pack
held-out arm must hold it under repaired."""
import importlib.util, os, shutil, subprocess, sys, tempfile
ROOT = "/fast/scratch/hyaku/kaidoku-r93/MutCounter/clone"
CARRIERS = ['/usr/bin/jq', '/usr/bin/xxd', '/usr/lib/libz.so.1.3.2', '/usr/bin/docker-init', '/usr/bin/xz']
spec = importlib.util.spec_from_file_location("cand", os.path.join(ROOT, "tools/round-92/upx-stop-boundary-search-repair.py"))
cand = importlib.util.module_from_spec(spec); spec.loader.exec_module(cand)

def build_images():
    cache = os.path.join(os.environ.get("TMPDIR") or tempfile.gettempdir(), "f2-table5-cache")
    os.makedirs(cache, exist_ok=True)
    images = []
    for i, c in enumerate(CARRIERS):
        p = os.path.join(cache, f"{i}.bin")
        if not os.path.isfile(p):
            box = tempfile.mkdtemp(prefix="f2-", dir=cache)
            inp, outp = os.path.join(box, "in"), os.path.join(box, "p")
            shutil.copyfile(c, inp); os.chmod(inp, 0o755)
            subprocess.run(["/usr/bin/upx", "--best", "-q", "-o", outp, inp], capture_output=True, check=True)
            shutil.move(outp, p); shutil.rmtree(box, ignore_errors=True)
        images.append(open(p, "rb").read())
    return images

IMAGES = build_images()
cand.upx_green = lambda data: any(data == P for P in IMAGES)
sys.exit(cand.main(sys.argv[1:]))
