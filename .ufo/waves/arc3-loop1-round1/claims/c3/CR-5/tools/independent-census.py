#!/usr/bin/env python3
"""CR-5 independent locus checker (critic instrument, NOT the census).

Re-derives, with a separate implementation, the coverage question the census
answers with its UNDECLARED class:
  - parse the SCOPE table out of a given census file (the table under test),
  - scan the three target files line-by-line for every PIN / bare-version /
    pointer needle occurrence (no REA_GATE gating -> strictly broader),
  - classify each occurrence line as inside a declared range (CURRENT/DATED)
    or OUT-OF-RANGE,
  - for DATED occurrences, report value vs live anchors (shelter surface).

Exit 0 iff no out-of-range occurrence. Usage:
  python3 independent-census.py <census.py> <root> [--json]
"""
import json, os, re, sys

PIN = re.compile(r"rea-agents@(\d+\.\d+\.\d+)")
VER = re.compile(r"(?<![\d.])6\.\d+\.\d+")
PTR = re.compile(r"((?:~|/)[\w./+-]+\.(?:json|toml|ya?ml)):(\d+)")
GATE = re.compile(r"rea-agents|\brea\b|config\.toml|mcp_config\.json|mcp\.json|"
                  r"mcp_servers|devin|\bomp\b|kimi|npx", re.I)
HOME = os.path.expanduser("~")
CLIENTS = {"devin": HOME + "/.config/devin/mcp_config.json",
           "omp": HOME + "/.omp/agent/mcp.json",
           "kimi": HOME + "/.kimi-code/config.toml"}


def parse_scope(census_path):
    txt = open(census_path, encoding="utf-8").read()
    m = re.search(r"SCOPE\s*=\s*\[(.*?)\n\]", txt, re.S)
    if not m:
        raise SystemExit("no SCOPE table found")
    rows = []
    for mm in re.finditer(r'\(\s*"([^"]+)",\s*(\d+),\s*(\d+),\s*"([A-Z]+)",\s*(None|\d+),\s*(None|r"[^"]*")\s*\)', m.group(1)):
        f, s, e, cls, ml, mr = mm.groups()
        rows.append((f, int(s), int(e), cls, None if ml == "None" else int(ml),
                     None if mr == "None" else mr[1:]))
    return rows


def live_anchors():
    out = {}
    for c, p in CLIENTS.items():
        try:
            txt = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            out[c] = None
            continue
        mm = re.search(r"rea-agents@(\d+\.\d+\.\d+)", txt)
        out[c] = mm.group(1) if mm else None
    return out


def scope_of(rows, f, line):
    for (rf, s, e, cls, ml, mr) in rows:
        if rf == f and s <= line <= e:
            return cls
    return None


def main():
    census_path, root = sys.argv[1], sys.argv[2]
    as_json = "--json" in sys.argv
    rows = parse_scope(census_path)
    live = live_anchors()
    live_vals = set(v for v in live.values() if v)
    files = sorted({r[0] for r in rows})
    out = {"scope_rows": len(rows), "live": live, "out_of_range": [],
           "dated_occurrences": [], "in_range_counts": {}, "files": {}}
    for f in files:
        try:
            lines = open(os.path.join(root, f), encoding="utf-8",
                         errors="replace").read().splitlines()
        except OSError:
            out["files"][f] = "unreadable"
            continue
        out["files"][f] = {"lines": len(lines)}
        counts = {}
        for i, ln in enumerate(lines, 1):
            occ = []
            for m in PIN.finditer(ln):
                occ.append(("pin", m.group(1)))
            spans = [(m.start(), m.end()) for m in PIN.finditer(ln)]
            for m in VER.finditer(ln):
                if any(s <= m.start() < e for s, e in spans):
                    continue
                occ.append(("bare", m.group(0)))
            if not occ:
                for m in PTR.finditer(ln):
                    occ.append(("ptr", m.group(0)))
            if not occ:
                continue
            cls = scope_of(rows, f, i)
            gated = bool(GATE.search(ln))
            for kind, val in occ:
                rec = {"file": f, "line": i, "kind": kind, "value": val,
                       "scope": cls, "rea_gate": gated}
                if cls is None:
                    out["out_of_range"].append(rec)
                else:
                    counts[cls] = counts.get(cls, 0) + 1
                    if cls == "DATED" and kind in ("pin", "bare"):
                        rec["equals_live"] = val in live_vals
                        out["dated_occurrences"].append(rec)
        out["in_range_counts"][f] = counts
    ok = not out["out_of_range"]
    out["verdict"] = "COVERAGE-OK" if ok else "OUT-OF-RANGE-FOUND"
    if as_json:
        print(json.dumps(out, indent=1))
    else:
        print("live anchors: %r" % live)
        print("scope rows: %d; files: %r" % (len(rows), {k: v for k, v in out["files"].items()}))
        print("in-range occurrence counts: %r" % out["in_range_counts"])
        print("OUT-OF-RANGE occurrences (%d):" % len(out["out_of_range"]))
        for r in out["out_of_range"]:
            print("  %s:%d [%s] %s=%s rea_gate=%s" %
                  (r["file"], r["line"], r["kind"], r["kind"], r["value"], r["rea_gate"]))
        print("DATED occurrences (%d, shelter surface):" % len(out["dated_occurrences"]))
        for r in out["dated_occurrences"]:
            print("  %s:%d [%s] %s equals_live=%s" %
                  (r["file"], r["line"], r["kind"], r["value"], r.get("equals_live")))
        print("VERDICT: %s" % out["verdict"])
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
