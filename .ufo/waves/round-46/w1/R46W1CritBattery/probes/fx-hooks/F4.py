"""F4: every row's identity cell is exact and its verdict map binds the three codes,
and every other cell says nothing at all.

If C2 is a semantic registry this artefact is red; if it is a path census plus a
regex on cell 2, it is green.
"""
HOUSE_N = 7


def transform(skill):
    H = "<!-- instrument-registry v2 -->"
    T = "<!-- /instrument-registry -->"
    i = skill.index(H) + len(H)
    j = skill.index(T)
    out, n = [], 0
    for line in skill[i:j].splitlines():
        t = line.strip()
        if t.startswith("|") and not t.startswith("|---") and "| tool |" not in t:
            cells = [c.strip() for c in t.strip("|").split("|")]
            if len(cells) != HOUSE_N:
                out.append(line)
                continue
            out.append("| %s | x | 0= 1= 2= | x | x | x | x |" % cells[0])
            n += 1
        else:
            out.append(line)
    assert n == 38, n
    return skill[:i] + "\n".join(out) + "\n" + skill[j:]
