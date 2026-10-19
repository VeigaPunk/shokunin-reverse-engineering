#!/usr/bin/env python3
"""EX-13 (c2) fixture + variant builder — deterministic, repo-READ-ONLY.

Writes only under --work (default /var/tmp/ex13-r2). Rebuilds:
  * instrument variants: R0 landing base, H3-only (CR-5 patch text), H1-only (RV-11
    patch text), the hand-merged H1+H3 combination, landed+blinded, landed+PIN-blinded
  * the two patch diffs used by the patch-order conflict test
  * fixture roots: root-current-silenced, root-all-silent2, root-skill-absent,
    root-empty, root-e845c2b (+ git-reconstructed b21c0da / 679af5d / e87e507 / 6bc4c29)
Usage: python3 gen-fixtures.py [--work DIR] [--repo DIR]
"""
import argparse, hashlib, os, re, shutil, subprocess, sys

REPO_DEFAULT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
H3_OLD = '    g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)'
H3_NEW = '    g2_ok = len(out.get("current-ok", [])) > 0'
H3_PRINT_OLD = '    print("G2 positive-assertion guard: %s" % ("ok" if g2_ok else "SUSPECT"))'
H3_PRINT_NEW = ('    print("G2 positive-assertion guard: %s (current-ok loci=%d, total loci=%d)" %\n'
                '          ("ok" if g2_ok else "SUSPECT", len(out.get("current-ok", [])),\n'
                '           sum(c["loci"] for c in counts.values())))')
H1_A_OLD = ('    out, counts, filelines = {}, {}, {}\n    for f in files:\n        try:\n'
            '            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()\n'
            '        except OSError:\n            counts[f] = {"lines": 0, "loci": 0}')
H1_A_NEW = ('    out, counts, filelines, unreadable = {}, {}, {}, []\n    for f in files:\n        try:\n'
            '            lines = open(os.path.join(args.root, f), encoding="utf-8", errors="replace").read().splitlines()\n'
            '        except OSError as ex:\n            unreadable.append("%s: %s" % (f, type(ex).__name__))\n'
            '            counts[f] = {"lines": 0, "loci": 0}')
H1_B_OLD = ('    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\\n'
            '         and (not g11) and g2_ok')
H1_B_NEW = ('    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\\n'
            '         and (not g11) and g2_ok and (not unreadable)')
H1_C_OLD = '    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)'
H1_C_NEW = '    print("UNREADABLE (could-not-evaluate): %r" % unreadable)\n' + H1_C_OLD

CURRENT_ROWS = {"PROVINCE.md": [(8, 13), (15, 26), (44, 44), (64, 71)],
                "SKILL.md": [(10, 16), (18, 20)],
                "SCORECARD.md": [(56, 60)]}
ALL_ROWS = {"PROVINCE.md": [(8,13),(15,26),(40,43),(44,44),(45,62),(64,71),(119,131)],
            "SKILL.md": [(10,16),(18,20)],
            "SCORECARD.md": [(56,60),(273,326),(417,466),(467,502),(503,533),(534,560),
                             (619,619),(620,620),(636,702),(703,768),(769,855)]}
MARKERS = {"PROVINCE.md": {40, 45, 119},
           "SCORECARD.md": {273, 417, 467, 503, 534, 619, 620, 636, 704, 769}}
HIST_REVS = ("b21c0da", "679af5d", "e87e507", "6bc4c29", "e845c2b")
NEEDLES = ("PIN", "VER", "PTR")


def blind(text, needles=NEEDLES):
    for n in needles:
        text = re.sub(r'^%s = re\.compile\(.*\)$' % n, '%s = re.compile(r"(?!x)x")' % n, text, flags=re.M)
    assert text.count('re.compile(r"(?!x)x")') == len(needles), "blinding anchors"
    return text


def rewrite(f, rows, keep_markers):
    src = open(f, encoding="utf-8", errors="replace").read().splitlines()
    for (a, b) in rows:
        for i in range(a - 1, min(b, len(src))):
            if keep_markers and (i + 1) in MARKERS.get(os.path.basename(f), set()):
                continue
            src[i] = "neutral filler line"
    return "\n".join(src) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/var/tmp/ex13-r2")
    ap.add_argument("--repo", default=REPO_DEFAULT)
    a = ap.parse_args()
    W, R = a.work, a.repo
    os.makedirs(W, exist_ok=True)

    # R0 = pinned pre-landing base; prefer this directory's frozen copy (the live
    # target moved to R3 mid-wave, so it can no longer reproduce these patch anchors).
    pinned = os.path.join(os.path.dirname(os.path.abspath(__file__)), "census-before.py")
    src_path = pinned if os.path.exists(pinned) else os.path.join(R, ".ufo/gates/c1-census-v10.py")
    r0 = open(src_path, encoding="utf-8").read()
    if os.path.exists(pinned):
        assert hashlib.sha256(r0.encode()).hexdigest() == \
            "6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b", "pinned R0 drift"
    h3 = r0.replace(H3_OLD, H3_NEW).replace(H3_PRINT_OLD, H3_PRINT_NEW)
    assert h3 != r0, "H3 anchors missing (target already moved from R0)"
    h1 = r0.replace(H1_A_OLD, H1_A_NEW).replace(H1_B_OLD, H1_B_NEW).replace(H1_C_OLD, H1_C_NEW)
    assert h1 != r0, "H1 anchors missing"
    h1h3 = h1.replace(H3_OLD, H3_NEW).replace(H3_PRINT_OLD, H3_PRINT_NEW)
    variants = {"census-h0.py": r0, "census-h3.py": h3, "census-h1.py": h1, "census-h1h3-combined.py": h1h3,
                "census-h0-blind.py": blind(r0), "census-h3-blind.py": blind(h3)}
    for name, text in variants.items():
        open(os.path.join(W, name), "w", encoding="utf-8").write(text)

    # patch diffs for the order-conflict test (relative names: patch -p0 targets census-h0.py)
    for tag, other in (("patch-h3.diff", "census-h3.py"), ("patch-h1.diff", "census-h1.py")):
        with open(os.path.join(W, tag), "w") as fh:
            subprocess.run(["diff", "-u", "census-h0.py", other], cwd=W, stdout=fh)

    # fixtures
    for name, rows, keep in (("root-current-silenced", CURRENT_ROWS, False),
                             ("root-all-silent2", ALL_ROWS, True)):
        d = os.path.join(W, name); os.makedirs(d, exist_ok=True)
        for f, rw in rows.items():
            open(os.path.join(d, f), "w", encoding="utf-8").write(rewrite(os.path.join(R, f), rw, keep))
    d = os.path.join(W, "root-skill-absent"); os.makedirs(d, exist_ok=True)
    for f in ("PROVINCE.md", "SCORECARD.md"):
        shutil.copy(os.path.join(R, f), os.path.join(d, f))
    os.makedirs(os.path.join(W, "root-empty"), exist_ok=True)

    # historical roots from git (read-only)
    for rev in HIST_REVS:
        d = os.path.join(W, "root-" + rev); os.makedirs(d, exist_ok=True)
        for f in ("PROVINCE.md", "SCORECARD.md", "SKILL.md"):
            p = subprocess.run(["git", "show", "%s:%s" % (rev, f)], cwd=R, capture_output=True, text=True)
            if p.returncode == 0:
                open(os.path.join(d, f), "w", encoding="utf-8").write(p.stdout)

    print("work dir: %s" % W)
    for name in sorted(os.listdir(W)):
        p = os.path.join(W, name)
        if os.path.isfile(p):
            print("  %-26s %s" % (name, hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]))
        else:
            print("  %-26s <dir>" % name)


if __name__ == "__main__":
    sys.exit(main())
