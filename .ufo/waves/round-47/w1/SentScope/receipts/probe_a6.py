"""Attack A6's new surface: `_fixture_files` now writes a file into the fixture repo for
every citation the landed block names. Does artefact content pick the write path?"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.environ["S"]
sys.path.insert(0, L + "/tools/round-46")
sys.path.insert(0, L + "/tools/round-47")
import gate
import exact

out = {}
D = os.path.join(S, "c-a6")
subprocess.run(["rm", "-rf", D])
subprocess.run(["git", "clone", "-q", "--no-hardlinks", L, D], check=True)
top = subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"],
                     capture_output=True, text=True).stdout.strip()
assert top == D, ("toplevel mismatch", top, D)
for k, v in (("user.email", "fx@r47"), ("user.name", "r47 fx")):
    subprocess.run(["git", "-C", D, "config", k, v], check=True)

skill_path = os.path.join(D, "SKILL.md")
skill = open(skill_path).read()
marker = exact.MARKER
block_start = skill.index(marker)
line_start = skill.rindex("\n- **", 0, block_start) + 1
line_end = skill.index("\n", skill.index("Refs:", block_start)) if "Refs:" in skill[block_start:] else None
escape = "tools/round-47/../../../../../../" + S.lstrip("/") + "/PWNED-outside.md"
crafted = skill[:line_end] + "\n  Extra refs: `" + escape + ":1-2`" + skill[line_end:]
open(skill_path, "w").write(crafted)
subprocess.run(["git", "-C", D, "add", "-A"], check=True)
subprocess.run(["git", "-C", D, "commit", "-q", "-m", "crafted citation"], check=True)
rev = subprocess.run(["git", "-C", D, "rev-parse", "HEAD"],
                     capture_output=True, text=True).stdout.strip()

files = lambda p: gate.show(D, rev, p)
bad, cited = exact.check_refs(gate.show(D, rev, "SKILL.md"), files, True)
out["check_refs_bad"] = bad
out["show_escape_path"] = gate.show(D, rev, escape)

scratch = tempfile.mkdtemp(dir=S, prefix="bat-")
try:
    bat = exact.run_battery(D, rev, scratch)
finally:
    shutil.rmtree(scratch, ignore_errors=True)
out["battery"] = {k: v for k, v in bat.items() if k != "fixtures"}
out["fixtures"] = [(f["name"], f.get("v3_exit"), f.get("error")) for f in bat.get("fixtures", [])]
out["PWNED_outside_exists"] = os.path.exists(os.path.join(S, "PWNED-outside.md"))
json.dump(out, open(os.path.join(S, "a6.json"), "w"), indent=1, sort_keys=True, default=str)
print(json.dumps({"PWNED_outside_exists": out["PWNED_outside_exists"], "show_escape_path": out["show_escape_path"], "escape_rejected": [b for b in out["check_refs_bad"] if "PWNED" in b], "battery": out["battery"], "fixtures": out["fixtures"]}, indent=1, default=str))
