"""F5: the citation paragraph is a `Refs:` line whose content is exactly what
m_self_refs writes, and corpus/lessons/round-45.md is cited on a SEPARATE line.

m_self_refs rewrites only `Refs:` lines, so the separate citation survives, the
artefact stays valid, and the "self-refs" forgery is not a forgery at all.
"""


def transform(skill):
    s = skill.index("- **23. ")
    e = skill.index("\n## ", s + 10)
    block = skill[s:e]
    selfrefs = "  Refs: " + ", ".join(
        "plans/round-46-claims.md:%d" % k for k in range(1, 7))
    out = []
    for line in block.splitlines():
        if line.strip().startswith("Refs:"):
            out.append(selfrefs)
            out.append("  Also `corpus/lessons/round-45.md:142-176` for the routed defects.")
        else:
            out.append(line)
    return skill[:s] + "\n".join(out) + "\n" + skill[e:]
