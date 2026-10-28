#!/usr/bin/env python3
"""Behavioural probes for tools/round-47/record.py, one per guard the selftest cannot see.

Scratch-only. Builds a one-repo fixture (git init under $S/fixture-<tag>), then calls
the module's own `evaluate_text` with authored cards. Each probe prints the counter exit
and the failing lines, so a mutant guard's production consequence is observable.

Usage: probe.py <dir-containing-tools/round-47/record.py> <tag>
"""
import importlib.util
import json
import os
import subprocess
import sys

S = os.path.dirname(os.path.abspath(__file__))
HEAD = "# card\n\n## Owned axes\n\n| Axis | Baseline → current score, 0–10 | Observable | Evidence | Round |\n|---|---|---|---|---|\n"


def sh(*cmd, cwd=None):
    return subprocess.run(cmd, capture_output=True, text=True, cwd=cwd)


def fixture(tag):
    d = os.path.join(S, "fixture-" + tag)
    subprocess.run(["rm", "-rf", d], check=True)
    os.makedirs(d)
    sh("git", "-C", d, "init", "-q")
    assert sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.strip() == d, d
    sh("git", "-C", d, "config", "user.email", "st@r47")
    sh("git", "-C", d, "config", "user.name", "r47 probe")
    files = {
        ".ufo/waves/round-8/w1-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
        ".ufo/waves/round-8/w2-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
        ".ufo/waves/round-9/w1-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
        ".ufo/waves/round-9/w2-dispatch.json": json.dumps({"counts": {"spawn": 1}}),
        "tools/x/keep.md": "x\n",
        "corpus/knowledge/2026-10-01-x.md": "x\n",
        "corpus/README.md": "# readme\n\n## Coverage map\n\n- 2026-10-01-x — x\n\n"
                            "## Gaps\n\ntail\n",
    }
    for name, body in files.items():
        full = os.path.join(d, name)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(body)
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "commit", "-q", "-m", "base")
    base = sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()
    with open(os.path.join(d, "tools/x/keep.md"), "a") as fh:
        fh.write("y\n")
    sh("git", "-C", d, "add", "-A")
    sh("git", "-C", d, "commit", "-q", "-m", "tip")
    tip = sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()
    return d, base, tip


def card(tip, base, r8="", seats9="Waves: 1 + 1 = 2 seats",
         window=None, path=".ufo/waves/round-9/w1-dispatch.json",
         corrections=None, axes="| coverage | 9.72 → 10.0 | 1/1 knowledge files mapped | x | r1 |",
         only_round9=False):
    window = window or f"`git log {base[:8]}..{base[:8]} -- tools/x/` is empty"
    text = HEAD + axes + "\n\n"
    if not only_round9:
        text += "## Round 8\n\n" + (r8 or "An earlier round with no atoms.") + "\n\n"
    text += ("## Round 9\n\nBase `%s`. %s. %s. See `%s`.\n" % (tip[:8], seats9, window, path))
    if corrections is None:
        corrections = [
            "- corrects seats round-9: 2 waves, 2 seats total",
            f"- corrects window round-9: empty in {base[:8]}..{base[:8]} -- tools/x/",
            f"- corrects path {path}: landed",
        ]
    if corrections:
        text += "\n## Record corrections — round 47\n\n" + "\n".join(corrections) + "\n"
    return text


def probes(tip, base):
    p = lambda s: f"`{s}`"  # noqa: E731
    out = []
    out.append(("P0-valid-control", card(tip, base), "green card must exit 0"))
    # P1: no atom of class `rev` at all (class-coverage clause)
    c = card(tip, base).replace(f"Base `{tip[:8]}`. ", "")
    out.append(("P1-missing-rev-class", c, "card has zero rev atoms"))
    # P5: four false seats atoms, each exempted by a correction that re-derives as true
    r8 = "Waves: 1 + 1 = 3 seats. Wave 1: 1 seats; wave 2: 9 seats."
    s9 = "Waves: 1 + 1 = 3 seats. Wave 1: 1 seats; wave 2: 9 seats."
    c = card(tip, base, r8=r8, seats9=s9, corrections=[
        "- corrects seats round-8: 2 waves, 2 seats total",
        "- corrects seats round-9: 2 waves, 2 seats total"])
    out.append(("P5-four-exemptions", c, "4 true corrections exempt 4 atoms > EXEMPT_MAX"))
    # P6: real battery over a card whose corrections have no seats-total and no window pair
    c = card(tip, base, corrections=[
        "- corrects path .ufo/waves/round-9/w1-dispatch.json: landed",
        "- corrects path .ufo/waves/round-9/w2-dispatch.json: landed"]).replace(
        "See `.ufo/waves/round-9/w1-dispatch.json`.",
        "See `.ufo/waves/round-9/w1-dispatch.json` and "
        "`.ufo/waves/round-9/w2-dispatch.json`.")
    out.append(("P6-battery-two-noop-forgeries", c, "real run_battery: forgeries_green=2"))
    # P6c: synthetic battery dial (correction_forgeries unreachable != 3 from run_battery)
    out.append(("P6c-battery-dial-synthetic", card(tip, base),
                "SYNTHETIC battery {'correction_forgeries': 2, 'forgeries_green': 0}"))
    # P7: exemption naming an atom the card does not contain, correction itself re-derives true
    c = card(tip, base, corrections=[
        "- corrects seats round-9: 2 waves, 2 seats total",
        f"- corrects window round-9: empty in {base[:8]}..{base[:8]} -- tools/x/",
        f"- corrects rev {base}: landed"])
    out.append(("P7-ghost-atom-existing-rev", c, "rev correction resolves, no rev atom in card"))
    # P8: one `## Round N` section only
    out.append(("P8-single-round-section", card(tip, base, only_round9=True),
                "sections != 2 (clause 5)"))
    # P9: a false `axes` correction line; CORR does not parse class `axes` at all
    c = card(tip, base, corrections=[
        "- corrects seats round-9: 2 waves, 2 seats total",
        f"- corrects window round-9: empty in {base[:8]}..{base[:8]} -- tools/x/",
        "- corrects axes coverage: 99/99"])
    out.append(("P9-false-axes-correction", c, "axes correction states 99/99, derived 1/1"))
    out.append(("P9b-true-axes-correction", card(tip, base, corrections=[
        "- corrects seats round-9: 2 waves, 2 seats total",
        f"- corrects window round-9: empty in {base[:8]}..{base[:8]} -- tools/x/",
        "- corrects axes coverage: 1/1"]), "axes correction states 1/1"))
    # P10: an exemption whose own correction is false
    c = card(tip, base, seats9="Waves: 1 + 1 = 3 seats", corrections=[
        "- corrects seats round-9: 2 waves, 9 seats total",
        f"- corrects window round-9: empty in {base[:8]}..{base[:8]} -- tools/x/"])
    out.append(("P10-false-correction-exempts", c, "false seats correction exempts a false atom"))
    # P11: two corrections that correct nothing -- both atoms already verify
    out.append(("P11-vacuous-corrections", card(tip, base, corrections=[
        "- corrects path .ufo/waves/round-9/w1-dispatch.json: landed",
        "- corrects path .ufo/waves/round-9/w2-dispatch.json: landed"]).replace(
        "See `.ufo/waves/round-9/w1-dispatch.json`.",
        "See `.ufo/waves/round-9/w1-dispatch.json` and "
        "`.ufo/waves/round-9/w2-dispatch.json`."),
        "two re-deriving corrections over atoms that were never wrong"))
    return out


def main():
    d, base, tip = fixture(os.path.basename(os.path.dirname(os.path.dirname(
        os.path.abspath(sys.argv[1])))))
    path = os.path.join(sys.argv[1], "tools/round-47/record.py")
    spec = importlib.util.spec_from_file_location("rec_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    files = lambda p: mod.gate.show(d, tip, p)  # noqa: E731
    res = []
    for name, text, why in probes(tip, base):
        battery = None
        if name.startswith("P6-"):
            battery = mod.run_battery(text, files, d, tip)
        elif name == "P6c-battery-dial-synthetic":
            battery = {"correction_forgeries": 2, "forgeries_green": 0, "fixtures": "SYNTHETIC"}
        code, rec = mod.evaluate_text(text, files, d, tip, battery=battery)
        res.append({"probe": name, "why": why, "exit": code,
                    "failing": rec.get("failing", rec.get("reason")),
                    "mismatches": [m["key"] for m in rec.get("mismatches", [])],
                    "exempted": [e["key"] for e in rec.get("exempted", [])],
                    "corrections": rec.get("corrections"),
                    "battery": rec.get("battery") if isinstance(rec.get("battery"), dict)
                    and "fixtures" not in str(rec.get("battery")) else str(rec.get("battery"))[:60]})
    print(json.dumps({"module": path, "base": base, "tip": tip, "probes": res}, indent=1))


if __name__ == "__main__":
    main()
