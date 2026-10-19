#!/usr/bin/env python3
"""VZ-4 roster census (arc3-loop1-round2).

Mechanically extracts the frozen roster from claims-frozen.md (the "Roster (64
seats, enumerated)" section), then compares against the seats/ dir and the
claims/<chain>/<seat>/ artifact dirs. Prints delivered/undelivered per chain.

Usage: python3 roster-census.py [--json]
"""
import json
import os
import re
import sys

W = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round2"
FROZEN = os.path.join(W, "claims-frozen.md")
SEATS = os.path.join(W, "seats")

CHAIN_PREFIX = {"c1": "C1 chain", "c2": "C2 chain", "c3": "C3 chain", "cross": "Cross"}


def parse_roster(path):
    """Parse roster lines like: 'C1 chain (12): PL-1, EX-01, ...' (continuation lines indented)."""
    text = open(path, encoding="utf-8").read()
    start = text.index("## Roster")
    # cut at the next '## ' after start, if any
    rest = text[start:]
    m = re.search(r"\n## ", rest)
    if m:
        rest = rest[: m.start()]
    chains = {}
    cur = None
    for line in rest.splitlines()[1:]:
        m = re.match(r"^(C1|C2|C3|Cross) chain \(", line) or re.match(r"^(Cross) \(", line)
        if m:
            cur = m.group(1)
            chains[cur] = []
            line = line.split(":", 1)[1]
        if cur is None:
            continue
        toks = [t.strip() for t in line.split(",")]
        for t in toks:
            t = re.sub(r"\(.*?\)|\.$", "", t).strip()
            if re.fullmatch(r"(?:PL|EX|SC|RV|CR|VZ|CN|CU)-\d+", t):
                chains[cur].append(t)
    return chains


def delivered_seats(seats_dir):
    if not os.path.isdir(seats_dir):
        return set(), set()
    names, empty = set(), []
    for f in sorted(os.listdir(seats_dir)):
        if not f.endswith(".md"):
            continue
        seat = f[:-3]
        names.add(seat)
        if os.path.getsize(os.path.join(seats_dir, f)) == 0:
            empty.append(seat)
    return names, set(empty)


def claim_dirs():
    out = {}
    root = os.path.join(W, "claims")
    if not os.path.isdir(root):
        return out
    for chain in sorted(os.listdir(root)):
        cdir = os.path.join(root, chain)
        if not os.path.isdir(cdir):
            continue
        for seat in sorted(os.listdir(cdir)):
            p = os.path.join(cdir, seat)
            if os.path.isdir(p):
                out.setdefault(seat, []).append(chain + "/" + seat)
    return out


def main():
    frozen = parse_roster(FROZEN)
    roster = [s for ch in frozen.values() for s in ch]
    roster_set = set(roster)
    seats, empties = delivered_seats(SEATS)
    cdirs = claim_dirs()

    result = {"roster_total": len(roster), "roster": frozen, "seats_dir": SEATS,
              "delivered": sorted(roster_set & seats), "undelivered": [],
              "strays": sorted(seats - roster_set), "empty_seat_files": sorted(empties),
              "claim_dirs": cdirs, "per_chain": {}}
    for ch, names in frozen.items():
        d = [n for n in names if n in seats]
        u = [n for n in names if n not in seats]
        result["per_chain"][ch] = {"roster": len(names), "delivered": len(d),
                                   "undelivered": u, "delivered_names": d}
        result["undelivered"].extend(u)

    if "--json" in sys.argv:
        print(json.dumps(result, indent=2))
        return
    print(f"roster_total={result['roster_total']} delivered={len(result['delivered'])} "
          f"undelivered={len(result['undelivered'])} seats_dir_present={os.path.isdir(SEATS)}")
    for ch in ("C1", "C2", "C3", "Cross"):
        pc = result["per_chain"][ch]
        print(f"  {ch:5s} {pc['delivered']:2d}/{pc['roster']:2d}  undelivered: "
              f"{' '.join(pc['undelivered']) if pc['undelivered'] else '-'}")
    if result["strays"]:
        print("  STRAYS (not in roster): " + " ".join(result["strays"]))
    if result["empty_seat_files"]:
        print("  EMPTY seat files: " + " ".join(result["empty_seat_files"]))
    print("  claim artifact dirs: " + (", ".join(sorted(cdirs)) if cdirs else "(none)"))


if __name__ == "__main__":
    main()
