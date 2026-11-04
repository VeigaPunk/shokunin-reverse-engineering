import json, os, shutil, subprocess, sys
from pathlib import Path
work = "/fast/scratch/hyaku/kaidoku-r84/ScribeKnowledge/keyprobe"
shutil.rmtree(work, ignore_errors=True)
os.makedirs(work)
build = os.path.join(work, "build")
leaf, mid, outer = (os.path.join(build, n) for n in ("leaf","mid","outer"))
for d in (leaf, mid, outer): os.makedirs(d)
Path(leaf,"alpha.txt").write_text("leaf-alpha\n")
Path(leaf,"beta.txt").write_text("leaf-beta\n")
Path(leaf,"gamma.bin").write_text("".join(f"row-{n:03d}\n" for n in range(200)))
def mks(src, img):
    r = subprocess.run(["mksquashfs", src, img, "-noappend", "-comp", "gzip", "-b","4096","-quiet","-repro-time","1760000000"], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-400:]
images = {k: os.path.join(work, k+".sqfs") for k in "cab"}
mks(leaf, images["c"]); shutil.copyfile(images["c"], os.path.join(mid,"inner-c.sqfs"))
Path(mid,"one.txt").write_text("mid-one\n"); Path(mid,"two.txt").write_text("mid-two\n")
mks(mid, images["b"]); shutil.copyfile(images["b"], os.path.join(outer,"inner-b.sqfs"))
Path(outer,"x.txt").write_text("outer-x\n"); mks(outer, images["a"])
env = dict(os.environ); env["TMPDIR"] = os.path.join(work,"tmp"); os.makedirs(env["TMPDIR"])
out = os.path.join(work,"out3")
r = subprocess.run(["npx","-y","rea-agents@6.5.0","extract-firmware",images["a"],out,"--max-depth","3","--format","json"], env=env, capture_output=True, text=True, timeout=600)
text = r.stdout
start = text.find("{")
env_obj, _ = json.JSONDecoder().raw_decode(text[start:])
norm = env_obj.get("normalized_result")
files = norm.get("files") or []
out_rows = []
for f in files:
    rel = f.get("relative_path")
    out_rows.append({"relative_path": rel, "has_analysis_depth": "analysis_depth" in f,
                     "analysis_depth": f.get("analysis_depth"), "sha256": (f.get("sha256") or "")[:16]})
res = {"exit": r.returncode, "coverage": norm.get("coverage"),
       "depth_limited_paths": norm.get("depth_limited_paths"),
       "files": out_rows}
print(json.dumps(res, indent=1))
