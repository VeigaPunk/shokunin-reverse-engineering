#!/usr/bin/env python3
"""CriticC1 diagnostic: per-tamper fault attribution.
For each carrier, each tamper kind, check upx -t after (a) no fix, (b) names-only fix
(f3), (c) magic-only fix (f4), (d) real candidate; and show the names of section
headers before/after so the reason is evidenced, not asserted."""
import importlib.util, json, os, struct, subprocess, sys

S = "/fast/scratch/hyaku/kaidoku-r98/CriticC1"
UPX = "/usr/bin/upx"
spec = importlib.util.spec_from_file_location("bat", S + "/clone/tools/round-98/pe-upx-tamper-battery.py")
bat = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bat)
D = os.path.join(S, "w", "diag")
os.makedirs(D, exist_ok=True)


def names(b):
    pe = struct.unpack_from("<I", b, 0x3C)[0]
    n = struct.unpack_from("<H", b, pe + 6)[0]
    st = pe + 24 + struct.unpack_from("<H", b, pe + 20)[0]
    return [bytes(b[st + 40 * k:st + 40 * k + 8]).rstrip(b"\0").decode("latin1") for k in range(n)]


def upxt(p):
    r = subprocess.run([UPX, "-t", "-q", p], capture_output=True, text=True)
    msg = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode, (msg[-1].split(": ")[-1] if msg else "")


def fix(cmd, src, dst):
    if os.path.exists(dst):
        os.unlink(dst)
    return subprocess.run([sys.executable, "-I", "-B", cmd, "--in", src, "--out", dst]).returncode


rows = []
for name, src, pin in bat.CARRIERS:
    pb = open(os.path.join(S, "w", "base", name + ".upx"), "rb").read()
    for kind in bat.TAMPERS:
        tp = os.path.join(D, "%s.%s.tam" % (name, kind))
        open(tp, "wb").write(bat.tamper(pb, kind))
        row = {"carrier": name, "kind": kind, "names_before": names(open(tp, "rb").read())}
        row["t_raw"] = upxt(tp)
        for label, cmd in (("names_only", S + "/f3_names_only.py"),
                           ("magic_only", S + "/f4_magic_only.py"),
                           ("real", S + "/clone/tools/round-98/upx-pe-repair.py")):
            out = os.path.join(D, "%s.%s.%s.out" % (name, kind, label))
            rc = fix(cmd, tp, out)
            if rc == 0:
                row[label] = {"rc": rc, "t": upxt(out), "names_after": names(open(out, "rb").read())}
            else:
                row[label] = {"rc": rc}
        rows.append(row)
json.dump(rows, open(S + "/out/diag_names.json", "w"), indent=1)
for r in rows:
    print(r["carrier"], r["kind"], "names", r["names_before"], "| raw t", r["t_raw"][0],
          "| names_only", r.get("names_only"), "| magic_only", r.get("magic_only", {}).get("t"),
          "| real", r.get("real", {}).get("t"))
