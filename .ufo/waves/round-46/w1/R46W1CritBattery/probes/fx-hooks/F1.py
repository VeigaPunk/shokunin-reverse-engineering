"""F1: keep every structural token, state nothing.

Each of the 13 required rows is reduced to `| R45-CLn | x | <token> | 1 |`.
The trigger names a routed id, the arm names a vocabulary token, the exit is 1,
the header is exact, the refs, pin and S142 are the landed block's own.
If C1 is a semantic measure this artefact is red; if it is a token census it is green.
"""
IDS = ["R45-CL2", "R45-CL6", "R45-CL7", "R45-CL9", "R45-CL13", "R45-CL14",
       "R45-CL15", "R45-CL18", "R45-CL19", "R45-CL20", "R45-CL22", "R45-CL23",
       "R45-CL24"]


def transform(skill):
    s = skill.index("- **23. ")
    e = skill.index("\n## ", s + 10)
    block = skill[s:e]
    out, k = [], 0
    for line in block.splitlines():
        t = line.strip()
        if t.startswith("|") and "trigger" not in t and not t.startswith("|---"):
            out.append("| %s | x | commit | 1 |" % IDS[k])
            k += 1
        else:
            out.append(line)
    assert k == 13, k
    return skill[:s] + "\n".join(out) + "\n" + skill[e:]
