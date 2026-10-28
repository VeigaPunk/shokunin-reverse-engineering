#!/usr/bin/env python3
"""R46W1CritC2: attack the FROZEN (3182047) registry.py predicate in fixture repos.

Every case builds a fresh git fixture under HYAKU_SCRATCH, scores it with the frozen
module's own `score()` (clauses 1-5) or `evaluate()` (with the battery), and prints
{attack, expected, observed, exit, failing}.
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

S = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, os.path.join(S, "frozen"))
import gate      # noqa: E402  (frozen bytes)
import registry  # noqa: E402  (frozen bytes)

HEAD = registry.HEAD
TAIL = registry.TAIL
HOUSE = registry.HOUSE
CENSUS = registry.CENSUS
CLAIMS = "plans/round-46-claims.md"
TWO = ["tools/round-46/a.py", "tools/round-46/b.py"]


def row(path, purpose="gate", exits="0=met; 1=not met; 2=could-not-evaluate",
        selftest="`--selftest`", pinned="none", scope="repo", owner="kaidoku"):
    return f"| `{path}` | {purpose} | {exits} | {selftest} | {pinned} | {scope} | {owner} |"


def section(rows, header=" | ".join(HOUSE), pre="", post=""):
    body = "| " + header + " |\n|" + "---|" * len(HOUSE) + "\n" + "\n".join(rows) + "\n"
    return pre + "\n### Round-46 instrument registry\n\n" + HEAD + "\n\n" + body + "\n" + TAIL + "\n" + post


def census_doc(paths):
    return json.dumps({"paths": paths})


def fixture(skill, paths, present=None, claims_tools=None):
    d = tempfile.mkdtemp(dir=S, prefix="fx-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round46"), ("user.name", "round46 fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    files = {"SKILL.md": skill, CENSUS: census_doc(paths),
             CLAIMS: "# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n"
                     "- `tools/round-46/`\n"}
    present = paths if present is None else present
    for p in present:
        files[p] = "#!/usr/bin/env python3\nprint('tool')\n"
    # the census generator's own input: the claims files name these tools
    named = claims_tools if claims_tools is not None else present
    body = "# claims\n\n## Frozen paths (exact)\n\n- `plans/round-46-claims.md`\n- `tools/round-46/`\n\n"
    body += "\n".join(f"`{p}` computes the target." for p in named) + "\n"
    files[CLAIMS] = body
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


def structural(skill, paths, present=None):
    d, rev = fixture(skill, paths, present)
    try:
        files = lambda p: gate.show(d, rev, p)  # noqa: E731
        code, rec = registry.score(skill, files, "r46", "v2", rev)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return code, rec


def full_eval(skill, paths, present=None, claims_tools=None):
    d, rev = fixture(skill, paths, present, claims_tools)
    try:
        code, rec = registry.evaluate(d, rev, rev, "r46", "v2", with_battery=True)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return code, rec


CASES = []


def case(name, expected, skill, paths=None, present=None, claims_tools=None,
         runner="structural"):
    paths = paths if paths is not None else TWO
    try:
        if runner == "structural":
            code, rec = structural(skill, paths, present)
        else:
            code, rec = full_eval(skill, paths, present, claims_tools)
        failing = rec.get("failing") or rec.get("reason")
        extra = {k: rec.get(k) for k in ("scope_size", "registry_rows", "unregistered",
                                        "thin", "absent_at_rev") if k in rec}
        bat = rec.get("battery") or {}
        if bat:
            extra["battery"] = {k: v for k, v in bat.items() if k != "fixtures"}
    except Exception as exc:  # noqa: BLE001
        code, failing, extra = "crash", f"{type(exc).__name__}: {exc}", {}
    CASES.append({"attack": name, "expected": expected, "observed_exit": code,
                  "observed_failing": failing, **extra})
    print(json.dumps(CASES[-1]))


green = section([row(p) for p in TWO])

# 0. sanity: the plain artefact is green
case("baseline-two-honest-rows", 0, green)

# 1. exact cell 0, lying purpose (R45-CL14 at column 1)
case("lying-purpose-cell", "1 (row must describe the tool it names)",
     section([row(TWO[0], purpose="prints the weather forecast; computes nothing"),
              row(TWO[1])]))

# 2. verdict map forms
case("empty-verdict-bindings", "1 (0=;1=;2= binds no meaning)",
     section([row(p, exits="0=; 1=; 2=") for p in TWO]))
case("verdict-garbage-suffix", "1 (a cell with trailing garbage binds nothing)",
     section([row(p, exits="0=met; 1=not met; 2=could-not-evaluate; 999=padding !!garbage")
              for p in TWO]))
case("verdict-colon-space", "1", section([row(p, exits="0: 1: 2:") for p in TWO]))
case("verdict-digits-in-prose", 1, section([row(p, exits="0 rows, 1 column, 2 bytes")
                                            for p in TWO]))

# 3a. escaped pipe in a rendered cell smuggles the digits into the parsed verdict column
smuggle = ("| `" + TWO[0] + "` | see x\\|0=a; 1=b; 2=c | non-zero on failure | "
           "`--selftest` | none | repo | kaidoku |")
case("escaped-pipe-smuggles-verdict", "1 (the rendered verdict cell is prose)",
     section([smuggle, row(TWO[1])]))

# 3b. unclosed fence / comment after a complete table
case("unclosed-fence-after-rows", "2 malformed (C1 precedent) or 1",
     section([row(p) for p in TWO], post="```\n"))
case("unclosed-html-comment-after-rows", "2 malformed or 1",
     section([row(p) for p in TWO], post="<!-- trailing prose never closed\n"))

# 3c. the whole marked section inside an outer fence / comment (rendered as a code sample)
case("section-inside-outer-fence", "1 (rows inside a fenced block register nothing)",
     "```markdown\n" + green + "```\n")
case("section-inside-outer-comment", "1 (rows inside an HTML comment register nothing)",
     "<!--\n" + green + "-->\n")

# 4. duplicate registration: first wins
case("duplicate-fat-then-thin", "1 or 2 (ambiguous registration)",
     section([row(TWO[0]), row(TWO[0], exits="non-zero on failure"), row(TWO[1])]))
case("duplicate-thin-then-fat", 1,
     section([row(TWO[0], exits="non-zero on failure"), row(TWO[0]), row(TWO[1])]))

# 5. ghost rows
case("ghost-row-outside-census", "1 (R45-CL2: a row whose tool does not exist)",
     section([row(p) for p in TWO] + [row("tools/round-46/ghost.py")]))
case("ghost-row-listed-in-census", 1,
     section([row(p) for p in TWO] + [row("tools/round-46/ghost.py")]),
     paths=TWO + ["tools/round-46/ghost.py"])

# 6. duplicate census path
case("duplicate-census-path", 0,
     section([row(p) for p in TWO]), paths=TWO + [TWO[0]])

# 7. the census is trusted data: shrink it below what census.py derives
case("census-shrunk-below-derivation", "1 (census must equal census.py at --rev)",
     section([row(TWO[0])]), paths=[TWO[0]], present=TWO,
     claims_tools=TWO, runner="full")

print(json.dumps({"cases": CASES}, indent=1))
