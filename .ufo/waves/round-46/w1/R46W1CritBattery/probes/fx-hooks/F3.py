"""F3: the citation paragraph is valid but is not a `Refs:` line.

Clause 5 does not require the name `Refs:`, so this artefact is v2-valid on the
clauses as written; m_self_refs then has nothing to rewrite and raises ValueError.
Shows whether the mutation set is total on the clause set it claims to test.
"""


def transform(skill):
    s = skill.index("- **23. ")
    e = skill.index("\n## ", s + 10)
    block = skill[s:e]
    assert "\n  Refs:" in block
    return skill[:s] + block.replace("\n  Refs:", "\n  Citations:", 1) + skill[e:]
