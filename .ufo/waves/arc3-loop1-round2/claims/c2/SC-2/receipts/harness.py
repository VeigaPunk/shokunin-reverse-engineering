#!/usr/bin/env python3
"""SC-2 (scribe, c2, arc3-loop1-round2) injection-results ledger harness.

Runs a fixture x instrument matrix and emits one JSON summary per family so the
ledger table (.ufo/waves/arc3-loop1-round2/claims/c2/SC-2/injection-ledger.md)
is generated from measured runs, never from memory.

Usage:
  python3 harness.py build                      # build fixtures + instrument variants
  python3 harness.py run <family> <main.py>     # run matrix for one family
"""
import ast
import json
import os
import re
import shutil
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "/var/tmp/sc2-ledger"
FIX = os.path.join(BASE, "fixtures")
INST = os.path.join(BASE, "instruments")
RUNS = os.path.join(BASE, "runs")
SCOPED = ["PROVINCE.md", "SKILL.md", "SCORECARD.md"]

# fixture classes: "h1" (absent-file fail-open), "control" (already-FAIL at v10),
# "injection" (round-1 tamper classes), "blind" (H3), "residual" (H4), "anchor"
FIXTURES = [
    ("base-clean", "control", None),
    ("h1-missing-skill", "h1", "missing_skill"),
    ("h1-skill-as-dir", "h1", "skill_as_dir"),
    ("h1-skill-chmod000", "h1", "skill_chmod000"),
    ("h1-skill-symlink-loop", "h1", "skill_symlink_loop"),
    ("ctl-missing-province", "control", "missing_province"),
    ("ctl-missing-scorecard", "control", "missing_scorecard"),
    ("ctl-empty-dir", "control", "empty_dir"),
    ("inj-undeclared-append", "injection", "undeclared_append"),
    ("inj-marker-strip", "injection", "marker_strip"),
    ("inj-ptr-out-of-range", "injection", "ptr_out_of_range"),
    ("inj-false-current-pin", "injection", "false_current_pin"),
    ("inj-dated-shelter", "residual", "dated_shelter"),
    ("res-missing-root", "h1-residual", "missing_root"),
    ("res-empty-skill", "h1-residual", "empty_skill"),
    ("res-skill-decoy-historical", "h1-residual", "skill_decoy_historical"),
    ("res-h2-inline-marker", "h2-residual", "h2_inline_marker"),
    ("res-h5-eof-no-gate-token", "h5-residual", "h5_eof_no_gate_token"),
]

INSTRUMENT_CASES = [
    ("blind-all-needles", "blind", "blind"),
    ("blind-pin-only", "blind-partial", "pinblind"),
    ("blind-rea-gate", "blind", "blindgate"),
    ("widened-scope", "residual", "widened"),
]


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def build_fixtures():
    if os.path.exists(FIX):
        shutil.rmtree(FIX)
    for name, cls, mut in FIXTURES:
        d = os.path.join(FIX, name)
        os.makedirs(d)
        for f in SCOPED:
            shutil.copy2(os.path.join(REPO, f), os.path.join(d, f))
        if mut is None:
            continue
        if mut == "missing_skill":
            os.remove(os.path.join(d, "SKILL.md"))
        elif mut == "missing_province":
            os.remove(os.path.join(d, "PROVINCE.md"))
        elif mut == "missing_scorecard":
            os.remove(os.path.join(d, "SCORECARD.md"))
        elif mut == "empty_dir":
            for f in SCOPED:
                os.remove(os.path.join(d, f))
        elif mut == "skill_as_dir":
            os.remove(os.path.join(d, "SKILL.md"))
            os.makedirs(os.path.join(d, "SKILL.md"))
        elif mut == "skill_chmod000":
            os.chmod(os.path.join(d, "SKILL.md"), 0o000)
        elif mut == "skill_symlink_loop":
            os.remove(os.path.join(d, "SKILL.md"))
            os.symlink("SKILL.md", os.path.join(d, "SKILL.md"))
        elif mut == "undeclared_append":
            with open(os.path.join(d, "SCORECARD.md"), "a") as fh:
                fh.write("\nThe kimi client remains pinned to rea-agents@6.3.0 for the current round.\n")
        elif mut == "marker_strip":
            p = os.path.join(d, "PROVINCE.md")
            txt = open(p, encoding="utf-8").read()
            old = "verified on this host 2026-10-13"
            assert old in txt
            open(p, "w", encoding="utf-8").write(txt.replace(old, "verified on this host [marker removed]", 1))
        elif mut == "ptr_out_of_range":
            with open(os.path.join(d, "SCORECARD.md"), "a") as fh:
                fh.write("\nSee ~/.kimi-code/config.toml:9999 for the pointer class check.\n")
        elif mut == "false_current_pin":
            p = os.path.join(d, "SKILL.md")
            txt = open(p, encoding="utf-8").read()
            old = "rea-agents@6.5.0"
            assert old in txt, "SKILL.md has no @6.5.0 pin"
            open(p, "w", encoding="utf-8").write(txt.replace(old, "rea-agents@6.3.0", 1))
        elif mut == "dated_shelter":
            p = os.path.join(d, "SCORECARD.md")
            lines = open(p, encoding="utf-8").read().splitlines()
            lines.insert(800, "Current status: kimi runs rea-agents@6.3.0 as of this round.")
            open(p, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        elif mut == "missing_root":
            open(os.path.join(d, ".rootless"), "w").write("\n")
        elif mut == "empty_skill":
            open(os.path.join(d, "SKILL.md"), "w").close()
        elif mut == "skill_decoy_historical":
            open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8").write(
                "SKILL.md (historical stub): superseded by the round-2 instrument; "
                "last noted rea-agents@6.3.0 here.\n")
        elif mut == "h2_inline_marker":
            p2 = os.path.join(d, "PROVINCE.md")
            lines = open(p2, encoding="utf-8").read().splitlines()
            assert "rea-agents@6.5.0" in lines[16], lines[16]
            lines[16] = lines[16].replace("rea-agents@6.5.0", "rea-agents@6.3.0 (historical)")
            open(p2, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        elif mut == "h5_eof_no_gate_token":
            with open(os.path.join(d, "PROVINCE.md"), "a") as fh:
                fh.write("\nThe build shipped 6.7.0 last week.\n")
        else:
            raise SystemExit("unknown mutation " + mut)


def edit(path, old, new, count=1):
    txt = open(path, encoding="utf-8").read()
    assert old in txt, "needle not found in %s: %r" % (path, old[:60])
    open(path, "w", encoding="utf-8").write(txt.replace(old, new, count))


def build_variants(tag, main):
    out = {}
    v11 = os.path.join(INST, tag + "-main.py")
    shutil.copy2(main, v11)
    out["main"] = v11
    # H1 + H3 candidate edits (patch texts from round 1: RV-11 H1, CR-5 H3)
    if tag == "cand":
        edit(v11, "    out, counts, filelines = {}, {}, {}",
             "    out, counts, filelines, unreadable = {}, {}, {}, []")
        edit(v11, "        except OSError:\n            counts[f] = {\"lines\": 0, \"loci\": 0}",
             "        except OSError as ex:\n            unreadable.append(\"%s: %s\" % (f, type(ex).__name__))\n"
             "            counts[f] = {\"lines\": 0, \"loci\": 0}")
        edit(v11, "and (not g11) and g2_ok",
             "and (not g11) and g2_ok and (not unreadable)")
        edit(v11, '    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)',
             '    print("\\nSCOPE-ERRORS (marker assertions): %r" % scope_errors)\n'
             '    print("UNREADABLE (could-not-evaluate): %r" % unreadable)')
        edit(v11, '    g2_ok = len(out.get("current-ok", [])) > 0 or (not stale and not unatt and not undecl and not unres)',
             '    g2_ok = len(out.get("current-ok", [])) > 0')
    # blindness variants: neuter the three needles, or the gate regex
    for var in ("blind", "pinblind", "blindgate"):
        p = os.path.join(INST, tag + "-" + var + ".py")
        shutil.copy2(v11, p)
        if var == "blind":
            edit(p, 'PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
                 'PIN = re.compile(r"rea-agents@(ZZZ\\d+)", re.I)')
            edit(p, 'VER = re.compile(r"(?<![\\d.])6\\.\\d+\\.\\d+")',
                 'VER = re.compile(r"(?<![\\d.])9\\.\\d+\\.\\d+")')
            edit(p, 'PTR = re.compile(r"((?:~|/)[\\w./+-]+\\.(?:json|toml|ya?ml)):(\\d+)")',
                 'PTR = re.compile(r"((?:~|/)ZZZ\\.(?:json|toml|ya?ml)):(\\d+)")')
        elif var == "pinblind":
            edit(p, 'PIN = re.compile(r"rea-agents@(\\d+\\.\\d+\\.\\d+)", re.I)',
                 'PIN = re.compile(r"rea-agents@(ZZZ\\d+)", re.I)')
        else:
            edit(p, 'REA_GATE = re.compile(r"rea-agents|\\brea\\b|config\\.toml|mcp_config\\.json|mcp\\.json|mcp_servers|devin|\\bomp\\b|kimi|npx", re.I)',
                 'REA_GATE = re.compile(r"ZZZ_never_matches", re.I)')
        out[var] = p
    # widened-scope variant (H4 residual, round-1 CR-5 form): extend the last
    # declared DATED row's END so the appended records read historical.
    p = os.path.join(INST, tag + "-widened.py")
    shutil.copy2(v11, p)
    n = len(open(os.path.join(REPO, "SCORECARD.md"), encoding="utf-8").read().splitlines())
    edit(p, '    ("SCORECARD.md", 769, 855, "DATED", 769, r"arc2-loop1-round3"),',
         '    ("SCORECARD.md", 769, %d, "DATED", 769, r"arc2-loop1-round3"),' % n)
    out["widened"] = p
    return out


def parse(out, rc):
    rec = {"exit": rc}
    m = re.search(r"VERDICT: (\w+)\s+\(stale=(\d+) ambiguous=(\d+) undeclared=(\d+) unresolved=(\d+)\)", out)
    if m:
        rec["verdict"] = m.group(1)
        rec["counts"] = {"stale": int(m.group(2)), "ambiguous": int(m.group(3)),
                         "undeclared": int(m.group(4)), "unresolved": int(m.group(5))}
    m = re.search(r"SCOPE-ERRORS \(marker assertions\): (\[.*?\])\s*$", out, re.M)
    if m:
        rec["scope_errors"] = ast.literal_eval(m.group(1))
    m = re.search(r"UNREADABLE \(could-not-evaluate\): (\[.*?\])\s*$", out, re.M)
    if m:
        rec["unreadable"] = ast.literal_eval(m.group(1))
    m = re.search(r"G2 positive-assertion guard: (\w+)", out)
    if m:
        rec["g2"] = m.group(1)
    if "ANCHOR-FAIL" in out:
        rec["verdict"] = "ANCHOR-FAIL"
    if "Traceback (most recent call last)" in out:
        rec["crash"] = True
        rec["verdict"] = "CRASH"
        m = re.search(r"(\w+Error): (.*)", out)
        rec["crash_error"] = "%s: %s" % (m.group(1), m.group(2)) if m else "unknown"
    rec["tail"] = [l for l in out.splitlines() if l.strip()][-6:]
    return rec


def run_one(family, name, instrument, root, env_extra=None, cls="?", use_json=False):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    if os.path.exists(os.path.join(root, ".rootless")):
        root = os.path.join(root, "does-not-exist")
    cmd = [sys.executable, instrument, "--root", root]
    if use_json:
        cmd.append("--json")
    sha_before = sh(["sha256sum", instrument]).stdout.split()[0]
    p = sh(cmd, env=env)
    sha_after = sh(["sha256sum", instrument]).stdout.split()[0]
    out = p.stdout + p.stderr
    d = os.path.join(RUNS, family)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name + ".out"), "w") as fh:
        fh.write(out + "\nEXIT=%d\nINSTRUMENT=%s\nROOT=%s\n" % (p.returncode, instrument, root))
    rec = parse(out, p.returncode)
    if use_json:
        try:
            j = json.loads(p.stdout)
            rec["verdict"] = j["verdict"]
            rec["counts"] = {k: j["counts"][k]["loci"] for k in j["counts"]}
            rec["unreadable"] = j.get("unreadable", [])
            rec["declared_fail_classes"] = j.get("declared_fail_classes", [])
            rec["g2_ok"] = j.get("g2_ok")
            rec["json_keys"] = sorted(j.keys())
        except Exception as ex:
            rec["json_error"] = str(ex)
    rec["fixture"] = name
    rec["class"] = cls
    rec["instrument"] = instrument
    rec["mode"] = "json" if use_json else "text"
    rec["instrument_sha256"] = sha_before
    rec["instrument_sha256_after_run"] = sha_after
    rec["instrument_stable"] = (sha_before == sha_after)
    print("[%s] %-24s exit=%d %s" % (family, name, p.returncode,
          rec.get("verdict", "?") + (" unreadable=%d" % len(rec["unreadable"]) if rec.get("unreadable") else "")))
    return rec


def main():
    mode = sys.argv[1]
    if mode == "build":
        os.makedirs(INST, exist_ok=True)
        build_fixtures()
        printed = {}
        for tag, src in (("before", os.path.join(REPO, ".ufo/gates/c1-census-v10.py")),
                         ("after", os.path.join(INST, "after-main.py"))):
            if tag == "after" and not os.path.exists(src):
                print("after-main.py not staged yet; variant build deferred")
                continue
            variants = build_variants(tag, src)
            printed[tag] = {k: (v, sh(["sha256sum", v]).stdout.split()[0]) for k, v in variants.items()}
        for tag, v in printed.items():
            for k, (path, digest) in sorted(v.items()):
                print("%-7s %-8s %s %s" % (tag, k, digest[:16], path))
        return
    if mode == "run":
        family, mainp = sys.argv[2], sys.argv[3]
        use_json = "--json" in sys.argv
        tag = "main" if not use_json else "main"
        variants = build_variants(family.replace("-json", ""), mainp)
        rows = []
        for name, cls, mut in FIXTURES:
            rows.append(run_one(family, name, variants[tag], os.path.join(FIX, name), cls=cls, use_json=use_json))
        for name, cls, var in INSTRUMENT_CASES:
            rows.append(run_one(family, name, variants[var], os.path.join(FIX, "base-clean"), cls=cls, use_json=use_json))
        rows.append(run_one(family, "anchor-fail-empty-home", variants[tag],
                            os.path.join(FIX, "base-clean"), env_extra={"HOME": os.path.join(BASE, "emptyhome")},
                            cls="anchor", use_json=use_json))
        os.makedirs(RUNS, exist_ok=True)
        with open(os.path.join(RUNS, family + ".json"), "w") as fh:
            json.dump({"family": family, "main": mainp,
                       "main_sha256": sh(["sha256sum", mainp]).stdout.split()[0],
                       "rows": rows}, fh, indent=1)
        print("family %s -> %s/%s.json" % (family, RUNS, family))
        return
    raise SystemExit(__doc__)


if __name__ == "__main__":
    main()
