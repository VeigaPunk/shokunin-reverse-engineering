"""F2: R45-CL18 is named by two rows, so the missing-routed-id mutation is vacuous.

The mention row precedes the real R45-CL18 row, and m_missing_id drops the FIRST
data line containing the id: the artefact stays complete and 13 rows remain.
Fail-closed if the battery reports it red anyway; a hole if v2 accepts it.
"""


def transform(skill):
    s = skill.index("- **23. ")
    e = skill.index("\n## ", s + 10)
    block = skill[s:e]
    lines = block.splitlines()
    inserted = False
    out = []
    for line in lines:
        t = line.strip()
        if (not inserted and t.startswith("|") and "trigger" not in t
                and not t.startswith("|---")):
            out.append("| R45-CL2 | a second row that mentions R45-CL18 in this cell | rows | 1 |")
            inserted = True
        out.append(line)
    assert inserted
    return skill[:s] + "\n".join(out) + "\n" + skill[e:]
