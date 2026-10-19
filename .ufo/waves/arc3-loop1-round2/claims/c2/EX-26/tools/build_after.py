#!/usr/bin/env python3
"""EX-26: build the guarded 'after' census from the HEAD instrument.

Applies the round-1 patch texts (NOT applied there):
  H1  .ufo/waves/arc3-loop1-round1/claims/c3/RV-11/proposed-missing-file-guard.patch.md
  H3  .ufo/waves/arc3-loop1-round1/claims/c3/CR-5/proposed-g2-positive-floor.patch.md
Each replacement is asserted to hit exactly once, so the reconstruction is
verifiable; the resulting file's sha256 and a unified diff are written next to it.
"""
import hashlib
import sys
import difflib

SRC = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/gates/c1-census-v10.py"
BASE = "/var/tmp/ex26"
BEFORE = BASE + "/before.py"
AFTER = BASE + "/after.py"

src = open(SRC, encoding="utf-8").read()
print("source sha256:", hashlib.sha256(src.encode()).hexdigest())

edits = [
    # H1.1 -- collect unreadable scoped files
    (
        "    out, counts, filelines = {}, {}, {}\n",
        "    out, counts, filelines, unreadable = {}, {}, {}, []\n",
    ),
    # H1.2 -- record the could-not-evaluate class
    (
        "        except OSError:\n"
        "            counts[f] = {\"lines\": 0, \"loci\": 0}\n",
        "        except OSError as ex:\n"
        "            unreadable.append(\"%s: %s\" % (f, type(ex).__name__))\n"
        "            counts[f] = {\"lines\": 0, \"loci\": 0}\n",
    ),
    # H1.3 -- the verdict term
    (
        "         and (not g11) and g2_ok\n",
        "         and (not g11) and g2_ok and (not unreadable)\n",
    ),
    # H1.4 -- report line next to SCOPE-ERRORS
    (
        "    print(\"\\nSCOPE-ERRORS (marker assertions): %r\" % scope_errors)\n",
        "    print(\"\\nSCOPE-ERRORS (marker assertions): %r\" % scope_errors)\n"
        "    print(\"UNREADABLE (could-not-evaluate): %r\" % unreadable)\n",
    ),
    # H3.1 -- positive floor: at least one current-ok locus
    (
        "    g2_ok = len(out.get(\"current-ok\", [])) > 0"
        " or (not stale and not unatt and not undecl and not unres)\n",
        "    g2_ok = len(out.get(\"current-ok\", [])) > 0\n",
    ),
    # H3.2 -- self-documenting G2 line
    (
        "    print(\"G2 positive-assertion guard: %s\" % (\"ok\" if g2_ok else \"SUSPECT\"))\n",
        "    print(\"G2 positive-assertion guard: %s (current-ok loci=%d, total loci=%d)\" %\n"
        "          (\"ok\" if g2_ok else \"SUSPECT\", len(out.get(\"current-ok\", [])),\n"
        "           sum(c[\"loci\"] for c in counts.values())))\n",
    ),
]

out = src
for i, (old, new) in enumerate(edits, 1):
    n = out.count(old)
    print("edit %d occurrences=%d" % (i, n))
    if n != 1:
        sys.exit("ABORT: edit %d matched %d times (need exactly 1)" % (i, n))
    out = out.replace(old, new)

open(BEFORE, "w", encoding="utf-8").write(src)
open(AFTER, "w", encoding="utf-8").write(out)
print("before sha256:", hashlib.sha256(src.encode()).hexdigest())
print("after  sha256:", hashlib.sha256(out.encode()).hexdigest())
print("before lines:", src.count("\n"), "after lines:", out.count("\n"))

diff = difflib.unified_diff(src.splitlines(True), out.splitlines(True),
                            "head/.ufo/gates/c1-census-v10.py (before)",
                            "after.py (H1+H3 guards applied)",
                            n=3)
open(BASE + "/guards.diff", "w", encoding="utf-8").write("".join(diff))
print("wrote", BEFORE, AFTER, BASE + "/guards.diff")
