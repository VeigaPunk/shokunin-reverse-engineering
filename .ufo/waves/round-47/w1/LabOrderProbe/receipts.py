#!/usr/bin/env python3
"""LabOrderProbe receipts — R47-C1 clause 7 (flag order) on deterministic merge fixtures.

Every measurement records: exact argv, cwd, exit code, stdout sha256, stdout bytes, UTC.
Fixtures are created fresh under this scratch root; git identity is fixture-local.
"""
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
import gate    # noqa: E402
import exact   # noqa: E402

ORDER = '"-m", "--diff-merges=first-parent"'
REVERSED = '"--diff-merges=first-parent", "-m"'
ENV = dict(os.environ, GIT_AUTHOR_NAME="fx", GIT_AUTHOR_EMAIL="fx@fx",
           GIT_COMMITTER_NAME="fx", GIT_COMMITTER_EMAIL="fx@fx", LC_ALL="C")
RECS = []


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def run(argv, cwd, label):
    r = subprocess.run(argv, cwd=cwd, env=ENV, capture_output=True)
    rec = {"id": label, "cmd": argv, "cwd": cwd, "exit": r.returncode,
           "stdout_bytes": len(r.stdout),
           "stdout_sha256": hashlib.sha256(r.stdout).hexdigest(),
           "stderr": r.stderr.decode("utf-8", "replace")[:400], "utc": utc()}
    RECS.append(rec)
    return rec, r.stdout


def mkrepo(name):
    d = tempfile.mkdtemp(dir=S, prefix=name + ".")
    subprocess.run(["git", "-C", d, "init", "-q", "-b", "main"], env=ENV, check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    return d


def commit(d, msg):
    subprocess.run(["git", "-C", d, "add", "-A"], env=ENV, check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", msg], env=ENV, check=True)
    return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()


def w(d, p, text):
    full = os.path.join(d, p)
    os.makedirs(os.path.dirname(full) or d, exist_ok=True)
    with open(full, "w") as fh:
        fh.write(text)


def pairs(out):
    toks = out.decode("utf-8", "surrogateescape").split("\0")
    got, i = [], 0
    while i < len(toks):
        if gate.STATUS.match(toks[i].strip()) and i + 1 < len(toks):
            got.append((toks[i], toks[i + 1]))
            i += 2
            continue
        i += 1
    return got


def orders(d, a, b, label, extra=()):
    """Run the flag orders over a..b; return {tag: (rec, pairs)}."""
    out = {}
    for tag, flags in (("forward", ["-m", "--diff-merges=first-parent"]),
                       ("reversed", ["--diff-merges=first-parent", "-m"]),
                       ("late_m", ["-m", "--diff-merges=first-parent", "--name-status",
                                   "-m", "-z"]),
                       ("no_merges", ["-m", "--diff-merges=first-parent", "--no-merges"]),
                       ("plain", [])):
        # late_m already carries --name-status -z; normalise the rest here
        argv = ["git", "-C", d, "log", *flags]
        if tag != "late_m":
            argv += ["--name-status", "-z"]
        argv += ["--format=", f"{a}..{b}", *extra]
        rec, raw = run(argv, d, f"{label}/{tag}")
        rec["pairs"] = pairs(raw)
        rec["distinct_paths"] = sorted({p for _, p in rec["pairs"]})
        out[tag] = rec
    return out


# --- M1/M2/M3: the two-parent merge with disjoint side edits ----------------------
d1 = mkrepo("m1")
w(d1, "a.txt", "root\n"); w(d1, "b.txt", "root\n")
r1 = commit(d1, "root")
subprocess.run(["git", "-C", d1, "checkout", "-q", "-b", "side"], env=ENV, check=True)
w(d1, "a.txt", "one\n"); s1 = commit(d1, "side1")
subprocess.run(["git", "-C", d1, "checkout", "-q", "main"], env=ENV, check=True)
w(d1, "b.txt", "two\n"); m1 = commit(d1, "side2")
subprocess.run(["git", "-C", d1, "merge", "-q", "--no-ff", "side", "-m", "merge1"],
               env=ENV, check=True)
b1 = subprocess.run(["git", "-C", d1, "rev-parse", "HEAD"],
                    capture_output=True, text=True).stdout.strip()
f1 = orders(d1, r1, b1, "M1-disjoint")

# --- M4: resolution-only edit (the R45-CL6 case) ---------------------------------
d2 = mkrepo("m2")
w(d2, "c.txt", "orig\n"); r2 = commit(d2, "root")
subprocess.run(["git", "-C", d2, "checkout", "-q", "-b", "side"], env=ENV, check=True)
w(d2, "c.txt", "side\n"); commit(d2, "side-c")
subprocess.run(["git", "-C", d2, "checkout", "-q", "main"], env=ENV, check=True)
w(d2, "a.txt", "a\n"); p2 = commit(d2, "main-a")
subprocess.run(["git", "-C", d2, "merge", "-q", "--no-ff", "side", "-m", "merged"],
               env=ENV, capture_output=True)
w(d2, "c.txt", "resolved\n")
w(d2, "resolved.txt", "only the resolution\n")
subprocess.run(["git", "-C", d2, "add", "-A"], env=ENV, check=True)
subprocess.run(["git", "-C", d2, "commit", "-q", "--amend", "--no-edit"], env=ENV,
               check=True)
b2 = subprocess.run(["git", "-C", d2, "rev-parse", "HEAD"],
                    capture_output=True, text=True).stdout.strip()
f2 = orders(d2, p2, b2, "M4-resolution-only")

# the instruments themselves, on the same ranges
inst = {}
GATE_SRC = open(os.path.join(LANE, "tools", "round-46", "gate.py")).read()
variants = {
    "frozen": GATE_SRC,
    "late_m": GATE_SRC.replace('"--diff-merges=first-parent", "--name-status", "-z",',
                               '"--diff-merges=first-parent", "--name-status", "-m", "-z",', 1),
    "no_merges": GATE_SRC.replace('"--diff-merges=first-parent", "--name-status", "-z",',
                                  '"--diff-merges=first-parent", "--name-status", '
                                  '"--no-merges", "-z",', 1),
    "swapped": GATE_SRC.replace(ORDER, REVERSED, 1),
}
for tag, src in variants.items():
    p = os.path.join(S, "gate_%s.py" % tag)
    open(p, "w").write(src)
    spec = importlib.util.spec_from_file_location("g_" + tag, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    inst[tag] = {
        "order_literal": src.count(ORDER), "reversed_literal": src.count(REVERSED),
        "touched_m1": mod.history_touched(d1, r1, b1, ["."])[0],
        "touched_m2": mod.history_touched(d2, p2, b2, ["."])[0],
    }

# --- M7: counter verdict, clause 7 isolated and end-to-end with the battery ------
def counter_case(tag, src, with_battery):
    files = {"SKILL.md": exact.skill_text(exact.good_block()),
             "plans/round-47-claims.md": exact.CLAIMS_BODY,
             "corpus/lessons/round-46.md": "lesson line\n" * 240,
             "tools/round-47/exact.py": open(os.path.join(LANE, "tools", "round-47",
                                                          "exact.py")).read(),
             "tools/round-46/gate.py": src}
    scratch_root, err = gate.scratch("kaidoku-r47-orderprobe-")
    if err:
        raise RuntimeError(err)
    d = None
    try:
        d, rev = exact._repo(files, scratch_root, prefix="fo-")
        code, rec = exact.evaluate(d, rev, rev, "v3", with_battery)
        keep = {k: rec.get(k) for k in ("failing", "gate_order_literal",
                                        "gate_order_reversed", "met_target", "reason")}
        if with_battery:
            b = rec.get("battery") or {}
            keep["battery"] = {k: b.get(k) for k in
                               ("forgeries_total", "v2_green", "v3_green",
                                "genuine_green", "crash")}
        rec_out = {"id": "M7-%s-battery%s" % (tag, "on" if with_battery else "off"),
                   "cmd": ["python3", "-I", "-B", "tools/round-47/exact.py",
                           "--root", d, "--freeze", rev, "--rev", rev,
                           "--profile", "v3"] + ([] if with_battery else ["--no-battery"]),
                   "cwd": d, "exit": code,
                   "stdout_sha256": None, "stdout_bytes": None,
                   "json_sha256": hashlib.sha256(
                       json.dumps(rec, sort_keys=True).encode()).hexdigest(),
                   "utc": utc(), "receipt": keep}
        RECS.append(rec_out)
        return code, keep
    finally:
        if d:
            shutil.rmtree(d, ignore_errors=True)
        shutil.rmtree(scratch_root, ignore_errors=True)


cnt = {}
for tag in ("frozen", "late_m", "no_merges", "swapped"):
    cnt[tag] = {"nobattery": counter_case(tag, variants[tag], False)}
cnt["frozen"]["battery"] = counter_case("frozen", variants["frozen"], True)
cnt["no_merges"]["battery"] = counter_case("no_merges", variants["no_merges"], True)

# --- M8: what the freeze arm does with a frozen path that was changed then restored
d3 = mkrepo("m3")
w(d3, "plans/round-47-claims.md",
  "# claims\n\n## Frozen paths (exact)\n\n- `tools/frozen.txt`\n\n## After\n")
w(d3, "tools/frozen.txt", "v1\n")
fz = commit(d3, "freeze")
w(d3, "tools/frozen.txt", "v2\n"); commit(d3, "change")
w(d3, "tools/frozen.txt", "v1\n"); back = commit(d3, "restore")
freeze_rc = {}
for tag in ("frozen", "no_merges"):
    p = os.path.join(S, "gate_%s.py" % tag)
    spec = importlib.util.spec_from_file_location("gf_" + tag, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    code, rc = mod.freeze_state(d3, fz, back)
    freeze_rc[tag] = {"exit": code, "changed": rc.get("blob_changed"),
                      "touched": rc.get("touched"), "restored": rc.get("restored"),
                      "verdict": rc.get("frozen_path_changed"), "reason": rc.get("reason")}

out = {
    "utc": utc(),
    "git": subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip(),
    "python": sys.version.split()[0],
    "fixtures": {"m1": d1, "m1_range": [r1, b1], "m2": d2, "m2_range": [p2, b2],
                 "m3": d3},
    "M1_disjoint": f1, "M4_resolution_only": f2, "instruments": inst,
    "counter": cnt, "freeze_restore": freeze_rc,
    "receipts": RECS,
}
dest = sys.argv[1] if len(sys.argv) > 1 else os.path.join(S, "receipts.json")
with open(dest, "w") as fh:
    json.dump(out, fh, indent=1)
print(json.dumps({k: out[k] for k in ("fixtures", "instruments", "freeze_restore")},
                 indent=1))
print("counter:", json.dumps({k: {kk: vv[0] for kk, vv in v.items()} for k, v in
                              cnt.items()}, indent=1))
print("wrote", dest, hashlib.sha256(open(dest, "rb").read()).hexdigest())
