#!/usr/bin/env python3
"""R46W1CritC2 part 2: the same attacks against the LANDED (HEAD) registry.py.

The freeze arm makes the frozen bytes score 2 at every post-freeze rev, so the
instrument the lane actually lands is the HEAD one.  This asks which holes survive.
"""
import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.environ["HYAKU_SCRATCH"]
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
spec = importlib.util.spec_from_file_location(
    "registry_head", os.path.join(LANE, "tools", "round-46", "registry.py"))
reg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reg)
gate = sys.modules["gate"]

HEAD, TAIL, HOUSE, CENSUS = reg.HEAD, reg.TAIL, reg.HOUSE, reg.CENSUS
CLAIMS = "plans/round-46-claims.md"
TWO = ["tools/round-46/a.py", "tools/round-46/b.py"]


def row(path, purpose="gate", exits="0=met; 1=not met; 2=could-not-evaluate",
        selftest="`--selftest`", pinned="none", scope="repo", owner="kaidoku"):
    return f"| `{path}` | {purpose} | {exits} | {selftest} | {pinned} | {scope} | {owner} |"


def section(rows, header=" | ".join(HOUSE), pre="", post=""):
    body = "| " + header + " |\n|" + "---|" * len(HOUSE) + "\n" + "\n".join(rows) + "\n"
    return pre + "\n### Round-46 instrument registry\n\n" + HEAD + "\n\n" + body + "\n" + TAIL + "\n" + post


def fixture(skill, census_paths, present, named):
    d = tempfile.mkdtemp(dir=S, prefix="fxh-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round46"), ("user.name", "round46 fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    claims = ("# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
              "- `tools/round-46/`\n\n" + "\n".join(f"`{p}` computes the target." for p in named) + "\n")
    files = {"SKILL.md": skill, CENSUS: json.dumps({"paths": census_paths}), CLAIMS: claims}
    for p in present:
        files[p] = "#!/usr/bin/env python3\n"
    for path, text in files.items():
        full = os.path.join(d, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(text)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return d, rev


CASES = []


def case(name, expected, skill, census_paths=None, present=None, named=None, full=False):
    census_paths = census_paths if census_paths is not None else TWO
    present = present if present is not None else census_paths
    named = named if named is not None else present
    d, rev = fixture(skill, census_paths, present, named)
    try:
        if full:
            code, rec = reg.evaluate(d, rev, rev, "r46", "v2", with_battery=True)
        else:
            files = lambda p: gate.show(d, rev, p)  # noqa: E731
            code, rec = reg.score(skill, files, "r46", "v2", rev)
        bat = rec.get("battery") or {}
        extra = {k: rec.get(k) for k in ("scope_size", "registry_rows", "unregistered",
                                        "thin", "absent_at_rev", "met_target") if k in rec}
        if bat:
            extra["battery"] = {k: v for k, v in bat.items() if k != "fixtures"}
    except Exception as exc:  # noqa: BLE001
        code, extra = "crash", {"err": f"{type(exc).__name__}: {exc}"}
        rec = {}
    finally:
        shutil.rmtree(d, ignore_errors=True)
    CASES.append({"attack": name, "expected": expected, "observed_exit": code,
                  "failing": rec.get("failing"), **extra})
    print(json.dumps(CASES[-1]))


green = section([row(p) for p in TWO])
case("HEAD baseline", 0, green)
case("HEAD lying-purpose", "1", section([row(TWO[0], purpose="prints the weather"), row(TWO[1])]))
case("HEAD empty-verdict", "1", section([row(p, exits="0=; 1=; 2=") for p in TWO]))
case("HEAD outer-fence", "1", "```markdown\n" + green + "```\n")
case("HEAD ghost-row-outside-census", "1 (R45-CL2)",
     section([row(p) for p in TWO] + [row("tools/round-46/ghost.py")]))
case("HEAD duplicate-fat-then-thin", "1 or 2",
     section([row(TWO[0]), row(TWO[0], exits="non-zero on failure"), row(TWO[1])]))
# the cheapest artefact: a hand-shrunk census + one row, full evaluation with battery
case("HEAD census-shrunk-to-one-row (full)", "1 (census != census.py)", section([row(TWO[0])]),
     census_paths=[TWO[0]], present=TWO, named=TWO, full=True)
# and the same shrink with a junk purpose and an empty verdict map
case("HEAD cheapest-junk-artefact (full)", "1",
     section([row(TWO[0], purpose="x", exits="0=; 1=; 2=")]),
     census_paths=[TWO[0]], present=TWO, named=TWO, full=True)

print(json.dumps({"cases": CASES}, indent=1))
