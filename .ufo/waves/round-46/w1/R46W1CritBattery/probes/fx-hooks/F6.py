"""F6: an invalid artefact (eight data rows) used only to reach the no-op branch of
attest.run_battery directly; evaluate() must refuse to run the battery on it.
"""


def transform(skill):
    s = skill.index("- **23. ")
    e = skill.index("\n## ", s + 10)
    block = skill[s:e]
    out, k = [], 0
    for line in block.splitlines():
        t = line.strip()
        if t.startswith("|") and "trigger" not in t and not t.startswith("|---"):
            if k >= 8:
                k += 1
                continue
            k += 1
        out.append(line)
    return skill[:s] + "\n".join(out) + "\n" + skill[e:]
