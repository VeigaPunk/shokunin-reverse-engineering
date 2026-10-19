#!/usr/bin/env python3
"""CR-5 per-entry non-vacuity battery.

For each entry added by arc3-loop1-round3, construct ONE mutation that removes
the content the entry claims to grade, run the probe in a scratch clone, and
record whether that entry fires. An entry that cannot be made to fire is a dead
needle (count inflation); an entry that fires is live.

Mutations run only in the scratch clone (/var/tmp/cr5-r3/scratch/teeth).
"""
import json
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
CLONE = "/var/tmp/cr5-r3/scratch/teeth"
TABLE = "/var/tmp/cr5-r3/attacks/landed-table.json"
EXPECTED = "/var/tmp/cr5-r3/attacks/landed-expected.json"
PROBE = REPO + "/.ufo/gates/citation-drift/citation-drift-probe.py"
BASE = "c07af80"


def sh(*a, **kw):
    return subprocess.run(a, capture_output=True, text=True, **kw)


def mutate_and_run(entry):
    """Apply one mutation for `entry` in the clone and return True if it fires."""
    sh("git", "-C", CLONE, "reset", "-q", "--hard", BASE)
    target = entry["file"]
    line = entry.get("line")
    kind = entry["kind"]
    path = CLONE + "/" + target
    try:
        text = open(path).read()
    except OSError:
        return None, "citing file missing"
    lines = text.split("\n")
    if line is None:
        # anchor: replace the matched phrase with a token that cannot match
        m = re.search(entry["must_match"], text, re.M)
        if not m:
            return None, "anchor phrase absent at HEAD"
        text = text[:m.start()] + "MUTATED-CONTENT" + text[m.end():]
        open(path, "w").write(text)
        how = "anchor phrase replaced"
    elif kind == "extracted":
        if not (1 <= line <= len(lines)):
            return None, "line out of range"
        m = re.search(entry["pattern"], lines[line - 1])
        if not m:
            return None, "pattern absent at HEAD"
        lo = int(m.group(entry.get("target_group", 1)))
        new = str(lo + 500)
        s, e = m.span(entry.get("target_group", 1))
        lines[line - 1] = lines[line - 1][:s] + new + lines[line - 1][e:]
        open(path, "w").write("\n".join(lines))
        how = "stated number re-pointed +500"
    else:
        if not (1 <= line <= len(lines)):
            return None, "line out of range"
        lines[line - 1] = "MUTATED-CONTENT"
        open(path, "w").write("\n".join(lines))
        how = "pinned line content erased"
    sh("git", "-C", CLONE, "-c", "user.email=e@x", "-c", "user.name=e",
       "commit", "-qam", "teeth: " + entry["id"])
    rev = sh("git", "-C", CLONE, "rev-parse", "HEAD").stdout.strip()
    # pin the scratch expected to the landed table
    out = sh("python3", PROBE, "--root", CLONE, "--rev", rev,
             "--table", TABLE, "--expected", EXPECTED)
    fired = ("entry=" + entry["id"] + " ") in out.stdout
    fired_ids = set(re.findall(r"entry=(\S+)", out.stdout))
    return fired, "%s; other entries fired: %d" % (how, len(fired_ids) - (1 if fired else 0))


def main():
    old = json.loads(sh("git", "-C", REPO, "show",
                        "HEAD:.ufo/gates/citation-drift/pointer-table.json").stdout)
    new = json.load(open(REPO + "/.ufo/gates/citation-drift/pointer-table.json"))
    om = {e["id"] for e in old["entries"] + old["quoted"]}
    added = [e for e in new["entries"] if e["id"] not in om]
    live = dead = skipped = 0
    rows = []
    for e in added:
        fired, how = mutate_and_run(e)
        if fired is None:
            skipped += 1
            rows.append((e["id"], "SKIP", how))
            continue
        live += fired
        dead += (not fired)
        rows.append((e["id"], "FIRES" if fired else "DEAD", how))
    sh("git", "-C", CLONE, "reset", "-q", "--hard", BASE)
    with open("/var/tmp/cr5-r3/attacks/receipts/nonvacuity-cr5.txt", "w") as f:
        for i, (eid, verdict, how) in enumerate(rows):
            f.write("%-38s %-6s %s\n" % (eid, verdict, how))
        f.write("\nlive=%d dead=%d skipped=%d of %d added entries\n"
                % (live, dead, skipped, len(added)))
    print("live=%d dead=%d skipped=%d of %d" % (live, dead, skipped, len(added)))
    for eid, verdict, how in rows:
        if verdict != "FIRES":
            print("  %-38s %-6s %s" % (eid, verdict, how))


if __name__ == "__main__":
    sys.exit(main())