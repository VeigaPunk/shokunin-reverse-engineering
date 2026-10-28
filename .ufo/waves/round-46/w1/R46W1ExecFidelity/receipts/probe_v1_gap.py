#!/usr/bin/env python3
"""Why do two of the seven C2 forgeries fail the v1 profile?  Score each mutation
under both profiles with the FROZEN registry and print the v1 failing list."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "frozen"))
import registry  # noqa: E402

fixture = json.load(open(os.path.join(HERE, "fixture.json")))["fixture"]
rev = json.load(open(os.path.join(HERE, "fixture.json")))["rev"]


def show(path):
    import subprocess
    r = subprocess.run(["git", "-C", fixture, "show", f"{rev}:{path}"],
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


skill = show("SKILL.md")
files = lambda p: show(p)  # noqa: E731
spec = registry.SPECS["r46"]
mid, err = registry.split_section(skill, spec)
print(json.dumps({"section_error": err, "rows_in_section": len(registry.rows_in_section(mid))}))
for name, kind, fn in registry.MUTATIONS:
    try:
        text = fn(skill, spec) if name != "fenced" else skill.replace(
            registry.split_section(skill, spec)[0],
            registry.m_fenced(registry.split_section(skill, spec)[0]), 1)
    except (ValueError, TypeError) as exc:
        print(json.dumps({"name": name, "error": str(exc)}))
        continue
    c1, r1 = registry.score(text, files, "r46", "v1", rev)
    c2, r2 = registry.score(text, files, "r46", "v2", rev)
    print(json.dumps({"name": name, "v1": c1, "v1_failing": r1.get("failing"),
                      "v1_rows": r1.get("registry_rows"),
                      "v2": c2, "v2_failing": r2.get("failing")}))
