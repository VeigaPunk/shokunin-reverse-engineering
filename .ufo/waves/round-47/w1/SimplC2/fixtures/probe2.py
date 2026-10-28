#!/usr/bin/env python3
"""SimplC2 probe 2: parser domain, dead locals, kill-rule count."""
import ast
import importlib.util
import json
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.path.dirname(os.path.abspath(__file__))
FREEZE = "07d2894eabe88c326e9036262f20ad02662c860d"
BASE = "13a9e9e1f7ca3b95f2cc11f24f69d0d92a21a8a5"


def load(name):
    path = os.path.join(S, "mut", name, "record.py")
    spec = importlib.util.spec_from_file_location("rec_" + name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["rec_" + name] = mod
    spec.loader.exec_module(mod)
    return mod


def show(rev, path):
    r = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def files_at(rev):
    return lambda p: show(rev, p)


def unused_locals(path):
    tree = ast.parse(open(path).read())
    out = []
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.Module)):
            continue
        assigned, loaded = {}, set()
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name):
                if isinstance(sub.ctx, ast.Store):
                    assigned.setdefault(sub.id, sub.lineno)
                else:
                    loaded.add(sub.id)
            elif isinstance(sub, ast.arg):
                assigned.setdefault(sub.arg, sub.lineno)
        for name, line in assigned.items():
            if name not in loaded and not name.startswith("_"):
                out.append((getattr(node, "name", "<module>"), name, line))
    return out


def main():
    rec = load("base")
    res = {}

    # 1. the parser's output domain on the landing card's own corrections section
    card = show(FREEZE, "SCORECARD.md")
    corr, body = rec.corrections(card)
    res["landing_corrections_parsed"] = [(c["class"], c["key"]) for c in corr]
    res["landing_correction_lines_in_card"] = [
        l for l in card.splitlines() if l.strip().startswith("- corrects ")]
    res["CORR_regex_hits_axes_line"] = [
        bool(rec.CORR.match(l.strip())) for l in res["landing_correction_lines_in_card"]]

    # 2. kill rule: delete the corrections section from the landing card
    stripped = card[:card.index(rec.CORR_HEAD)].rstrip() + "\n"
    code, r = rec.evaluate_text(stripped, files_at(FREEZE), LANE, FREEZE, battery=None)
    res["kill_rule_delete_corrections"] = {
        "exit": code, "failing": r["failing"],
        "mismatches": [m["class"] + ":" + str(m["key"]) for m in r["mismatches"]],
        "corrections": r["corrections"]}

    # 3. dead locals in the module
    res["unused_locals"] = unused_locals(os.path.join(S, "mut", "base", "record.py"))

    # 4. is the `corrects` axes branch dead only because of the regex? widen it.
    src = open(os.path.join(S, "mut", "base", "record.py")).read()
    widened = src.replace('(seats|window|path|rev)', '(seats|window|path|rev|axes)')
    assert widened != src
    os.makedirs(os.path.join(S, "mut", "wide"), exist_ok=True)
    open(os.path.join(S, "mut", "wide", "record.py"), "w").write(widened)
    wide = load("wide")
    code, r = wide.evaluate_text(card, files_at(FREEZE), LANE, FREEZE, battery=None)
    res["regex_widened_to_axes"] = {
        "exit": code, "corrections": r["corrections"],
        "corrections_bad": r["corrections_bad"],
        "exempted": [e["class"] + ":" + str(e["key"]) for e in r["exempted"]],
        "mismatches": [m["class"] + ":" + str(m["key"]) for m in r["mismatches"]]}

    code, r = wide.evaluate_text(card, files_at(BASE), LANE, BASE, battery=None)
    res["regex_widened_at_base"] = {
        "exit": code, "corrections": r["corrections"],
        "mismatches": [m["class"] + ":" + str(m["key"]) for m in r["mismatches"]],
        "failing": r["failing"]}

    # 5. a false axes correction becomes red only under the widened regex
    bad = card.replace("138/138", "199/199", 1)
    code, r = wide.evaluate_text(bad, files_at(FREEZE), LANE, FREEZE, battery=None)
    res["widened_with_false_axes_correction"] = {
        "exit": code, "corrections_bad": r["corrections_bad"], "failing": r["failing"]}

    out = os.path.join(S, "receipts", "probe2.json")
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1)[:2600])


if __name__ == "__main__":
    main()
