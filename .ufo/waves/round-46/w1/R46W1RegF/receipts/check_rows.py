"""Validate rows.md with the FROZEN round-46 C2 scorer's own code path."""
import json
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-46")
import registry  # noqa: E402

ROWS = sys.argv[1]
raw = [l.rstrip("\n") for l in open(ROWS) if l.strip()]
rows = []
for line in raw:
    cells = [c.strip() for c in line.strip().strip("|").split("|")]
    rows.append(cells)

paths = [c[0].strip("`") for c in rows]
census = {"paths": paths}
HEAD = ("| tool | gate or probe - purpose | verdict map (exit codes) | "
        "self-test command | pinned-value path | write scope | owner |")
SEP = "|---|---|---|---|---|---|---|"


def build(body):
    lines = [HEAD, SEP] + ["| " + " | ".join(c) + " |" for c in body]
    return ("# SKILL\n\n<!-- instrument-registry v2 -->\n"
            + "\n".join(lines)
            + "\n<!-- /instrument-registry -->\n")


def files_for(cen):
    return lambda p: (json.dumps(cen).encode()
                      if p == "tools/round-46/census.json" else b"x")


def run(label, body, cen):
    code, rec = registry.score(build(body), files_for(cen), "r46", "v2",
                               "probe-rev")
    print(json.dumps({"case": label, "exit": code,
                      "unregistered": rec.get("unregistered"),
                      "thin": rec.get("thin"),
                      "absent_at_rev": rec.get("absent_at_rev"),
                      "registry_rows": rec.get("registry_rows"),
                      "header_ok": rec.get("header") == registry.HOUSE,
                      "failing": rec.get("failing")}, sort_keys=True))
    return code


# Structural checks that the counter itself does not perform.
for cells in rows:
    print(json.dumps({"cells": len(cells), "cell0": cells[0],
                      "backticked_ok": cells[0].startswith("`")
                      and cells[0].endswith("`"),
                      "stray_backticks": sum(c.count("`") for c in cells[1:]),
                      "exit_keys": sorted(set(registry.EXITMAP.findall(
                          cells[2]) if len(cells) > 2 else []))},
                     sort_keys=True))

green = run("as-written", rows, census)

thin = [c[:] for c in rows]
thin[0][2] = "0 rows, 1 column, 2 bytes"
run("mutant-thin-verdict-map", thin, census)

sub = [c[:] for c in rows]
sub[0][0] = "see " + sub[0][0] + " (wrapper)"
run("mutant-cell0-substring", sub, census)

missing = [c[:] for c in rows if c[0].strip("`") != "tools/round-45/c1-counter.py"]
run("mutant-row-absent", missing, census)

print("GREEN_EXIT", green)
