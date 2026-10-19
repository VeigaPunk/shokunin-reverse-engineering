#!/usr/bin/env python3
"""RV-11 sabotage harness: mutate one detection mechanism per copy, run selftest.
Proves the selftest cases exercise the real detection paths (teeth check).
Usage: python3 apply-mutations.py <tool.py source> <outdir>"""
import pathlib, shutil, subprocess, sys
src = pathlib.Path(sys.argv[1]).read_text(); out = pathlib.Path(sys.argv[2])
variants = {
  "s1-neuter-rewrite": [
    ('    if diffs:\n        finding = "REWRITE-DRIFT"', '    if False and diffs:\n        finding = "REWRITE-DRIFT"'),
    ('        ctime = [k for k in ("ctime_ns", "ctime_epoch")\n                 if k in ref and k in cand and ref[k] != cand[k]]', '        ctime = []'),
  ],
  "s2-utc->localtime": [
    ('    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(epoch))', '    return time.strftime("%Y-%m-%dT%H:%M:%SZ", time.localtime(epoch))'),
  ],
  "s3-neuter-sha-compare": [
    ('    if "sha256" in ref and "sha256" in cand and ref["sha256"] != cand["sha256"]:', '    if False:'),
  ],
}
for tag, subs in variants.items():
    d = out/tag
    if d.exists(): shutil.rmtree(d)
    d.mkdir(parents=True)
    text = src
    for old, new in subs:
        assert old in text, (tag, old[:50]); text = text.replace(old, new, 1)
    (d/"custody-pair.py").write_text(text)
    r = subprocess.run([sys.executable, str(d/"custody-pair.py"), "selftest"], capture_output=True, text=True, cwd=str(d))
    print("%s: selftest exit=%d" % (tag, r.returncode))
    for l in r.stdout.splitlines():
        if "FAIL" in l or "SELFTEST:" in l: print("   ", l.strip())
