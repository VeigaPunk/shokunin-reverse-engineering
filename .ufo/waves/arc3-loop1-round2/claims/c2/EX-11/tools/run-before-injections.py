#!/usr/bin/env python3
"""EX-11 before-state harness (arc3-loop1-round2, chain c2).

Runs four injection classes against the PRE-EDIT census v10 on /var/tmp copies:
  A  absent SKILL.md           (H1 class)
  B  absent PROVINCE.md        (H1 control: DATED rows present)
  C  neutered needles          (H3 class: PIN/VER/PTR never match)
  D  weakened regex            (partial narrowing variants w1/w2/w3)
Plus c0 baseline. Every run is on a /var/tmp/ex11/cases/<case>/root copy; the
repo tree is never a --root. Verbatim stdout+stderr+exit per case is written to
/var/tmp/ex11/outs/<case>.out and a header line to stdout.

Usage: python3 run-before-injections.py [--work /var/tmp/ex11] [--repo REPO]
"""
import argparse, hashlib, os, re, shutil, subprocess, sys

FILES = ["PROVINCE.md", "SKILL.md", "SCORECARD.md"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def write_out(work, case, out, rc, extra=""):
    p = os.path.join(work, "outs", case + ".out")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(out + "\nEXIT=%d\n" % rc)
        if extra:
            fh.write(extra)
    return p


def run_census(work, casedir, census, root, home=None):
    env = dict(os.environ)
    if home:
        env["HOME"] = home
    return subprocess.run([sys.executable, census, "--root", root],
                          capture_output=True, text=True, env=env)


def edit(path, old, new):
    txt = open(path, encoding="utf-8").read()
    assert old in txt, "needle %r not found in %s" % (old[:50], path)
    open(path, "w", encoding="utf-8").write(txt.replace(old, new, 1))


def variant_census(work, name, census_src, subs):
    dst = os.path.join(work, "instruments", name + ".py")
    txt = open(census_src, encoding="utf-8").read()
    for old, new in subs:
        assert old in txt, "substitution anchor missing: %r" % old[:60]
        txt = txt.replace(old, new, 1)
    open(dst, "w", encoding="utf-8").write(txt)
    return dst


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", default="/var/tmp/ex11")
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
    ap.add_argument("--census-src",
                    default="/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/claims/c3/CR-5/tools/census-after.py",
                    help="pristine PRE-EDIT census source (round-1 tree copy)")
    ap.add_argument("--expect-sha", default="6f1d19ff4b0878adfcdf0e38523aa79db461e74942eaafc018036a504163cc8b")
    args = ap.parse_args()
    W, R = args.work, args.repo
    assert not W.startswith("/tmp/"), "scratch under /tmp is forbidden"
    for d in ("outs", "instruments", "cases"):
        os.makedirs(os.path.join(W, d), exist_ok=True)

    census_gate = os.path.join(R, ".ufo/gates/c1-census-v10.py")
    if sha(args.census_src) != args.expect_sha:
        print("ABORT: census-src sha256 %s != expected %s" % (sha(args.census_src), args.expect_sha))
        return 3
    census_pre = os.path.join(W, "instruments", "census-pre.py")
    shutil.copy2(args.census_src, census_pre)
    root_before = os.path.join(W, "root-before")
    shutil.rmtree(root_before, ignore_errors=True)
    os.makedirs(root_before)
    for f in FILES:
        shutil.copy2(os.path.join(R, f), os.path.join(root_before, f))

    print("== before-state identity ==")
    print("census-pre.py sha256 %s  (repo:%s sha256 %s)" %
          (sha(census_pre), census_gate, sha(census_gate)))
    for f in FILES:
        print("  %-13s sha256 %s lines=%d" %
              (f, sha(os.path.join(root_before, f)),
               len(open(os.path.join(root_before, f)).read().splitlines())))

    cases = []

    def case(name, mutate=None, census=None, home=None):
        casedir = os.path.join(W, "cases", name)
        shutil.rmtree(casedir, ignore_errors=True)
        shutil.copytree(root_before, os.path.join(casedir, "root"))
        root = os.path.join(casedir, "root")
        if mutate:
            mutate(root)
        p = run_census(W, casedir, census or census_pre, root, home=home)
        out = p.stdout + p.stderr
        write_out(W, name, out, p.returncode)
        tail = [l for l in out.splitlines()
                if l.startswith(("VERDICT", "SCOPE-ERRORS", "ANCHOR-FAIL", "UNREADABLE", "G2 ")) or l.startswith("SKILL")]
        print("[%s] exit=%d  %s" % (name, p.returncode, " | ".join(tail)))
        cases.append(name)
        return out, p.returncode

    print("\n== injection classes ==")
    case("c0-baseline")
    case("cA-absent-skill", lambda root: os.remove(os.path.join(root, "SKILL.md")))
    case("cA2-empty-skill", lambda root: open(os.path.join(root, "SKILL.md"), "w").close())
    case("cB-absent-province", lambda root: os.remove(os.path.join(root, "PROVINCE.md")))
    case("cB2-absent-scorecard", lambda root: os.remove(os.path.join(root, "SCORECARD.md")))

    neutered = variant_census(W, "census-neutered", census_pre, [
        ("PIN = re.compile(r\"rea-agents@(\\d+\\.\\d+\\.\\d+)\", re.I)", "PIN = re.compile(r\"never-match-A\")"),
        ("VER = re.compile(r\"(?<![\\d.])6\\.\\d+\\.\\d+\")", "VER = re.compile(r\"never-match-B\")"),
        ("PTR = re.compile(r\"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)\")", "PTR = re.compile(r\"never-match-C\")"),
    ])
    print("   neutered instrument sha256 %s" % sha(neutered))
    case("cC-neutered-needles", census=neutered)

    def plant_false_pin(root):
        edit(os.path.join(root, "SKILL.md"), "rea-agents@6.5.0", "rea-agents@6.3.0")
    case("cD0-plant-false-pin-control", plant_false_pin)
    weak_nogroup = variant_census(W, "census-weak-pin-nogroup", census_pre, [
        ("PIN = re.compile(r\"rea-agents@(\\d+\\.\\d+\\.\\d+)\", re.I)",
         "PIN = re.compile(r\"rea-agents@6\\.5\\.\\d+\", re.I)"),
    ])
    print("   weak-pin-nogroup instrument sha256 %s" % sha(weak_nogroup))
    case("cD1a-weak-nogroup-plant", plant_false_pin, census=weak_nogroup)
    case("cD2a-weak-nogroup-noplant", census=weak_nogroup)
    weak_pin = variant_census(W, "census-weak-pin", census_pre, [
        ("PIN = re.compile(r\"rea-agents@(\\d+\\.\\d+\\.\\d+)\", re.I)",
         "PIN = re.compile(r\"rea-agents@(6\\.5\\.\\d+)\", re.I)"),
    ])
    print("   weak-pin instrument sha256 %s" % sha(weak_pin))
    case("cD1b-weak-pin-plant", plant_false_pin, census=weak_pin)
    case("cD2b-weak-pin-noplant", census=weak_pin)
    weak_gate = variant_census(W, "census-weak-gate", census_pre, [
        ("REA_GATE = re.compile(r\"rea-agents|\\brea\\b|config\\.toml|mcp_config\\.json|mcp\\.json|mcp_servers|devin|\\bomp\\b|kimi|npx\", re.I)",
         "REA_GATE = re.compile(r\"rea-agents\", re.I)"),
    ])
    print("   weak-gate instrument sha256 %s" % sha(weak_gate))
    def append_ptr(root):
        with open(os.path.join(root, "SCORECARD.md"), "a") as fh:
            fh.write("\nSee ~/.kimi-code/config.toml:9999 for the pointer class check.\n")

    case("cD3-weak-gate-ptr-append", append_ptr, census=weak_gate)
    case("cD4-stock-ptr-append-control", append_ptr)

    def append_stale(root):
        with open(os.path.join(root, "SCORECARD.md"), "a") as fh:
            fh.write("\nThe kimi client remains pinned to rea-agents@6.3.0 for the current round.\n")

    case("cD5-stock-stale-append-control", append_stale)
    case("cD6-weak-gate-stale-append", append_stale, census=weak_gate)

    weak_pinver = variant_census(W, "census-weak-pinver", census_pre, [
        ("PIN = re.compile(r\"rea-agents@(\\d+\\.\\d+\\.\\d+)\", re.I)",
         "PIN = re.compile(r\"rea-agents@(6\\.5\\.\\d+)\", re.I)"),
        ("VER = re.compile(r\"(?<![\\d.])6\\.\\d+\\.\\d+\")",
         "VER = re.compile(r\"(?<![\\d.])6\\.5\\.\\d+\")"),
    ])
    print("   weak-pinver instrument sha256 %s" % sha(weak_pinver))
    case("cD7-weak-pinver-plant", plant_false_pin, census=weak_pinver)
    case("cD8-weak-pinver-noplant", census=weak_pinver)

    # -- projection: hand-applied H1 + H3 patch texts (round-1 c3 drafts) ----
    projected = variant_census(W, "census-projected-h1h3", census_pre, [
        ("    out, counts, filelines = {}, {}, {}",
         "    out, counts, filelines, unreadable = {}, {}, {}, []"),
        ("        except OSError:\n            counts[f] = {\"lines\": 0, \"loci\": 0}\n            filelines[f] = None\n            continue",
         "        except OSError as ex:\n            unreadable.append(\"%s: %s\" % (f, type(ex).__name__))\n            counts[f] = {\"lines\": 0, \"loci\": 0}\n            filelines[f] = None\n            continue"),
        ("    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\\n         and (not g11) and g2_ok",
         "    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\\n         and (not g11) and g2_ok and (not unreadable)"),
        ("    g2_ok = len(out.get(\"current-ok\", [])) > 0 or (not stale and not unatt and not undecl and not unres)",
         "    g2_ok = len(out.get(\"current-ok\", [])) > 0"),
        ("    print(\"\\nSCOPE-ERRORS (marker assertions): %r\" % scope_errors)",
         "    print(\"\\nSCOPE-ERRORS (marker assertions): %r\" % scope_errors)\n    print(\"UNREADABLE (could-not-evaluate): %r\" % unreadable)"),
    ])
    print("   projected H1+H3 instrument sha256 %s" % sha(projected))
    case("cP0-projected-baseline", census=projected)
    case("cP1-projected-absent-skill", lambda root: os.remove(os.path.join(root, "SKILL.md")), census=projected)
    proj_neutered = variant_census(W, "census-projected-neutered", projected, [
        ("PIN = re.compile(r\"rea-agents@(\\d+\\.\\d+\\.\\d+)\", re.I)", "PIN = re.compile(r\"never-match-A\")"),
        ("VER = re.compile(r\"(?<![\\d.])6\\.\\d+\\.\\d+\")", "VER = re.compile(r\"never-match-B\")"),
        ("PTR = re.compile(r\"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)\")", "PTR = re.compile(r\"never-match-C\")"),
    ])
    proj_weakgate = variant_census(W, "census-projected-weak-gate", projected, [
        ("REA_GATE = re.compile(r\"rea-agents|\\brea\\b|config\\.toml|mcp_config\\.json|mcp\\.json|mcp_servers|devin|\\bomp\\b|kimi|npx\", re.I)",
         "REA_GATE = re.compile(r\"rea-agents\", re.I)"),
    ])
    proj_weakpinver = variant_census(W, "census-projected-weak-pinver", projected, [
        ("PIN = re.compile(r\"rea-agents@(\\d+\\.\\d+\\.\\d+)\", re.I)",
         "PIN = re.compile(r\"rea-agents@(6\\.5\\.\\d+)\", re.I)"),
        ("VER = re.compile(r\"(?<![\\d.])6\\.\\d+\\.\\d+\")",
         "VER = re.compile(r\"(?<![\\d.])6\\.5\\.\\d+\")"),
    ])
    for nm, inst in (("projected-neutered", proj_neutered), ("projected-weak-gate", proj_weakgate),
                     ("projected-weak-pinver", proj_weakpinver)):
        print("   %s instrument sha256 %s" % (nm, sha(inst)))
    case("cP2-projected-neutered", census=proj_neutered)
    case("cP3-projected-weak-gate-ptr", append_ptr, census=proj_weakgate)
    case("cP4-projected-weak-pinver-plant", plant_false_pin, census=proj_weakpinver)

    h1only = variant_census(W, "census-h1-only", census_pre, [
        ("    out, counts, filelines = {}, {}, {}",
         "    out, counts, filelines, unreadable = {}, {}, {}, []"),
        ("        except OSError:\n            counts[f] = {\"lines\": 0, \"loci\": 0}\n            filelines[f] = None\n            continue",
         "        except OSError as ex:\n            unreadable.append(\"%s: %s\" % (f, type(ex).__name__))\n            counts[f] = {\"lines\": 0, \"loci\": 0}\n            filelines[f] = None\n            continue"),
        ("    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\\n         and (not g11) and g2_ok",
         "    ok = (not stale) and (not unatt) and (not undecl) and (not unres) and (not scope_errors) \\\n         and (not g11) and g2_ok and (not unreadable)"),
    ])
    h3only = variant_census(W, "census-h3-only", census_pre, [
        ("    g2_ok = len(out.get(\"current-ok\", [])) > 0 or (not stale and not unatt and not undecl and not unres)",
         "    g2_ok = len(out.get(\"current-ok\", [])) > 0"),
    ])
    print("   h1-only instrument sha256 %s ; h3-only instrument sha256 %s" % (sha(h1only), sha(h3only)))
    case("cP5-h1only-absent-skill", lambda root: os.remove(os.path.join(root, "SKILL.md")), census=h1only)
    case("cP6-h3only-absent-skill", lambda root: os.remove(os.path.join(root, "SKILL.md")), census=h3only)
    case("cP7-h1only-neutered", census=variant_census(W, "census-h1only-neutered", h1only, [
        ("PIN = re.compile(r\"rea-agents@(\\d+\\.\\d+\\.\\d+)\", re.I)", "PIN = re.compile(r\"never-match-A\")"),
        ("VER = re.compile(r\"(?<![\\d.])6\\.\\d+\\.\\d+\")", "VER = re.compile(r\"never-match-B\")"),
        ("PTR = re.compile(r\"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)\")", "PTR = re.compile(r\"never-match-C\")"),
    ]))
    case("cP8-h3only-neutered", census=variant_census(W, "census-h3only-neutered", h3only, [
        ("PIN = re.compile(r\"rea-agents@(\\d+\\.\\d+\\.\\d+)\", re.I)", "PIN = re.compile(r\"never-match-A\")"),
        ("VER = re.compile(r\"(?<![\\d.])6\\.\\d+\\.\\d+\")", "VER = re.compile(r\"never-match-B\")"),
        ("PTR = re.compile(r\"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)\")", "PTR = re.compile(r\"never-match-C\")"),
    ]))
    case("cP9-projected-empty-skill", lambda root: open(os.path.join(root, "SKILL.md"), "w").close(), census=projected)

    s = open(os.path.join(W, "summary.txt"), "w", encoding="utf-8")
    s.write("census-pre.py sha256 %s (source: %s)\n" % (sha(census_pre), args.census_src))
    for f in FILES:
        s.write("%s sha256 %s\n" % (f, sha(os.path.join(root_before, f))))
    s.write("cases: %s\n" % " ".join(cases))
    s.close()
    print("\nwrote summary to %s" % os.path.join(W, "summary.txt"))


if __name__ == "__main__":
    sys.exit(main())
