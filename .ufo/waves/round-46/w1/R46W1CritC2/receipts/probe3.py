#!/usr/bin/env python3
"""P1/P2: the frozen instrument's battery on an honest artefact, and clause 5 inside the census."""
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, os.path.join(S, "frozen"))
import gate      # noqa: E402
import registry  # noqa: E402

HEAD, TAIL, HOUSE, CENSUS = registry.HEAD, registry.TAIL, registry.HOUSE, registry.CENSUS
CLAIMS = "plans/round-46-claims.md"
TWO = ["tools/round-46/a.py", "tools/round-46/b.py"]


def row(p, purpose="gate", exits="0=met; 1=not met; 2=could-not-evaluate"):
    return f"| `{p}` | {purpose} | {exits} | `--selftest` | none | repo | kaidoku |"


def section(rows):
    body = "| " + " | ".join(HOUSE) + " |\n|" + "---|" * 7 + "\n" + "\n".join(rows) + "\n"
    return "\n### R\n\n" + HEAD + "\n\n" + body + "\n" + TAIL + "\n"


def fx(skill, census, present, named):
    d = tempfile.mkdtemp(dir=S, prefix="pr-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@h"), ("user.name", "fx")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    claims = ("# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
              "- `tools/round-46/`\n\n" + "\n".join(f"`{p}` computes the target." for p in named) + "\n")
    files = {"SKILL.md": skill, CENSUS: json.dumps({"paths": census}), CLAIMS: claims}
    for p in present:
        files[p] = "#!/usr/bin/env python3\n"
    for path, text in files.items():
        full = os.path.join(d, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fx"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return d, rev


def full(skill, census, present, named):
    d, rev = fx(skill, census, present, named)
    try:
        code, rec = registry.evaluate(d, rev, rev, "r46", "v2", with_battery=True)
        bat = rec.get("battery") or {}
        return {"exit": code, "failing": rec.get("failing"),
                "met_target": rec.get("met_target"), "scope_size": rec.get("scope_size"),
                "battery": {k: v for k, v in bat.items() if k != "fixtures"},
                "fixtures": [(f["name"], f.get("v1_exit"), f.get("v2_exit"))
                             for f in bat.get("fixtures", [])]}
    finally:
        shutil.rmtree(d, ignore_errors=True)


print(json.dumps({"P1_honest_full_at_frozen_bytes":
                  full(section([row(p) for p in TWO]), TWO, TWO, TWO)}, indent=1))
print(json.dumps({"P2_ghost_in_census_absent_at_rev":
                  full(section([row(p) for p in TWO] + [row("tools/round-46/ghost.py")]),
                       TWO + ["tools/round-46/ghost.py"], TWO, TWO)}, indent=1))
