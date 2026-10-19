#!/usr/bin/env python3
"""EX-13 (c2) experiment runner — writes ONLY receipts next to this script.

Variants × roots matrix for the H1/H3 fail-closure analysis, plus the patch-order
conflict test. Deterministic; reads the pinned instruments in tools/ and the fixture
roots built by gen-fixtures.py; never writes any repo target.

Usage: python3 run-matrix.py [--work DIR] [--receipts DIR] [--repo DIR]
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_DEFAULT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
R0_SHA = "6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b"
R3_SHA = "82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/var/tmp/ex13-r2")
    ap.add_argument("--receipts", default=os.path.join(HERE, os.pardir, "receipts"))
    ap.add_argument("--repo", default=REPO_DEFAULT)
    a = ap.parse_args()
    W, OUT, R = a.work, os.path.abspath(a.receipts), a.repo
    os.makedirs(OUT, exist_ok=True)

    V = {"landed": os.path.join(HERE, "census-landed.py"),
         "landedb": os.path.join(W, "census-landed-blind.py"),
         "landedpin": os.path.join(W, "census-landed-pinblind.py"),
         "h0": os.path.join(W, "census-h0.py"),
         "h3": os.path.join(W, "census-h3.py"),
         "h1h3": os.path.join(W, "census-h1h3-combined.py"),
         "h0b": os.path.join(W, "census-h0-blind.py"),
         "h3b": os.path.join(W, "census-h3-blind.py")}
    assert sha(V["landed"]) == R3_SHA, "pinned R3 drift"
    assert sha(os.path.join(HERE, "census-before.py")) == R0_SHA, "pinned R0 drift"
    # landed needed in the work dir for the patch-order test copies
    if not os.path.exists(V["landedb"]):
        src = open(V["landed"], encoding="utf-8").read()
        for name, needles in (("census-landed-blind.py", ("PIN", "VER", "PTR")),
                              ("census-landed-pinblind.py", ("PIN",))):
            t = src
            for n in needles:
                t = re.sub(r'^%s = re\.compile\(.*\)$' % n, '%s = re.compile(r"(?!x)x")' % n, t, flags=re.M)
            open(os.path.join(W, name), "w").write(t)

    ROOT = {"live": R, "silenced": "%s/root-current-silenced" % W, "allsilent2": "%s/root-all-silent2" % W,
            "skillGone": "%s/root-skill-absent" % W, "empty": "%s/root-empty" % W,
            "e845c2b": "%s/root-e845c2b" % W, "b21c0da": "%s/root-b21c0da" % W,
            "679af5d": "%s/root-679af5d" % W, "e87e507": "%s/root-e87e507" % W,
            "6bc4c29": "%s/root-6bc4c29" % W}
    CASES = [("landed","live"),("landedb","live"),("landedpin","live"),
             ("landed","silenced"),("landed","allsilent2"),("landed","skillGone"),("landed","empty"),
             ("landed","e845c2b"),("landed","6bc4c29"),("landed","e87e507"),
             ("landed","b21c0da"),("landed","679af5d"),
             ("h0b","live"),("h3b","live"),
             ("h0","silenced"),("h3","silenced"),("h1h3","silenced"),
             ("h0","allsilent2"),("h3","allsilent2"),("h1h3","allsilent2"),
             ("h0","skillGone"),("h3","skillGone"),("h1h3","skillGone")]

    summary = []
    for v, r in CASES:
        tag = "%s-%s" % (v, r)
        p = subprocess.run([sys.executable, V[v], "--root", ROOT[r]], capture_output=True, text=True)
        open(os.path.join(OUT, tag + ".out"), "w").write(p.stdout + p.stderr)
        pj = subprocess.run([sys.executable, V[v], "--root", ROOT[r], "--json"], capture_output=True, text=True)
        d = json.loads(pj.stdout) if pj.stdout.strip().startswith("{") else {}
        g2 = next((l.strip() for l in p.stdout.splitlines() if "G2 positive" in l), "?")
        vd = next((l.strip() for l in p.stdout.splitlines() if l.startswith("VERDICT")), "?")
        cls = next((l.strip() for l in p.stdout.splitlines() if l.startswith("DECLARED FAIL")), "")
        unread = next((l.strip() for l in p.stdout.splitlines() if l.startswith("UNREADABLE")), "")
        scopes = {}
        for b in d.get("current_ok", []):
            for x in b["asserts"]:
                if x["disp"] == "current-ok":
                    scopes[x["scope"]] = scopes.get(x["scope"], 0) + 1
        summary.append("%-20s exit=%d %-40s %s | ck_blocks=%s scopes=%s | %s | %s" % (
            tag, p.returncode, vd, g2[:60], len(d.get("current_ok", [])) if d else "?",
            {k: scopes.get(k, 0) for k in ("CURRENT", "DATED", None)}, cls[:40], unread[:70]))
        print(summary[-1])
    open(os.path.join(OUT, "matrix-summary.txt"), "w").write("\n".join(summary) + "\n")

    # patch-order conflict test (strict -F0 and default fuzz)
    log = []
    for order, patches in (("h3-then-h1", ["patch-h3.diff", "patch-h1.diff"]),
                           ("h1-then-h3", ["patch-h1.diff", "patch-h3.diff"])):
        for fuzz in ("0", "2"):
            d = os.path.join(W, "ord-%s-f%s" % (order, fuzz))
            shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
            shutil.copy(V["h0"], os.path.join(d, "census-h0.py"))
            outs = []
            for pth in patches:
                r = subprocess.run(["patch", "-p0", "-F" + fuzz, "-i", os.path.join(W, pth), "census-h0.py"],
                                   cwd=d, capture_output=True, text=True)
                outs.append("%s rc=%d %s" % (pth, r.returncode,
                                             " ".join((r.stdout + r.stderr).split())[:120]))
                if r.returncode != 0:
                    break
            cur = open(os.path.join(d, "census-h0.py")).read()
            log.append("%-13s fuzz=%s  %s  result==hand-merge? %s" % (
                order, fuzz, " | ".join(outs), hashlib.sha256(cur.encode()).hexdigest() == hashlib.sha256(
                    open(V["h1h3"]).read().encode()).hexdigest()))
            print(log[-1])
    log.append("hand-merge sha256: " + hashlib.sha256(open(V["h1h3"]).read().encode()).hexdigest())
    open(os.path.join(OUT, "patch-order.txt"), "w").write("\n".join(log) + "\n")

    # input provenance
    prov = ["# EX-13 receipt provenance — generated by tools/run-matrix.py", ""]
    for f in ("PROVINCE.md", "SCORECARD.md", "SKILL.md"):
        p = os.path.join(R, f)
        prov.append("%s  %s  %d lines" % (sha(p), f, len(open(p, encoding="utf-8").read().splitlines())))
    for name, p in sorted(V.items()):
        prov.append("%s  %s" % (sha(p), os.path.relpath(p, os.path.dirname(HERE))))
    prov.append("%s  .ufo/gates/c1-census-v10.py (live target, read-only sample)" % sha(
        os.path.join(R, ".ufo/gates/c1-census-v10.py")))
    open(os.path.join(OUT, "inputs-sha256.txt"), "w").write("\n".join(prov) + "\n")


if __name__ == "__main__":
    sys.exit(main())
