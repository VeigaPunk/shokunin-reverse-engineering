import json, hashlib, pathlib, subprocess, sys
clone = pathlib.Path("/var/tmp/ex46/clone")
tbl = clone / ".ufo/gates/citation-drift/pointer-table.json"
exp = clone / ".ufo/gates/citation-drift/expected.json"
t = json.loads(tbl.read_text())
print("SIM: entries before =", len(t["entries"]))
sim = [
 {"id": "arc3r1-evm-recheck-line", "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md", "line": 7,
  "must_match": "recheck: `mkdir -p /var/tmp/cr2-recheck",
  "note": "SIM: arc3-era citation class (r1 EVM entry recheck line)"},
 {"id": "arc3r1-evm-unknowns-line", "kind": "exact",
  "file": "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md", "line": 29,
  "must_match": "Unknowns:",
  "note": "SIM: arc3-era citation class (r1 EVM entry Unknowns line)"},
 {"id": "sc-arc3-r1-c3-row", "kind": "exact",
  "file": "SCORECARD.md", "line": 881, "must_match": "census v10",
  "note": "SIM: arc3-era SCORECARD section needle"},
]
t["entries"] = t["entries"] + sim
tbl.write_text(json.dumps(t, indent=1, ensure_ascii=False) + "\n")
new_sha = hashlib.sha256(tbl.read_bytes()).hexdigest()
e = json.loads(exp.read_text())
old_pin = e["pointer_table"]["sha256"]
e["pointer_table"]["sha256"] = new_sha
exp.write_text(json.dumps(e, indent=1, ensure_ascii=False) + "\n")
print("SIM: entries after  =", len(t["entries"]))
print("SIM: old pin =", old_pin)
print("SIM: new pin =", new_sha)
