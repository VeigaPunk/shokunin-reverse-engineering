#!/usr/bin/env python3
"""Round-47 C2 vacuity attacker: build one mutated SCORECARD.md per attack.

Each attack starts from the byte-exact SCORECARD.md at base 13a9e9e1 (card-base.md)
and applies explicit, asserted textual mutations. No frozen byte is touched: the
source is a scratch copy inside a throwaway clone.
"""
import sys

ROOT = "/fast/scratch/hyaku/kaidoku-r47/C2Vacuity"
BASE = open(ROOT + "/card-base.md").read()
CORR_HEAD = "## Record corrections — round 47"

EMPTY_WIN = "31820472..31820472 -- tools/round-46 plans/round-46-claims.md"
ATOM_WIN = "0425224..<tip> -- tools/round-46 plans/round-46-claims.md"


def sub(text, old, new, count=1):
    assert text.count(old) == count, (old, text.count(old))
    return text.replace(old, new)


def seats(text, a, b):
    return sub(text, f"Wave 1: 40 seats; wave 2: 32 seats",
               f"Wave 1: {a} seats; wave 2: {b} seats")


def window(text, win):
    return sub(text, ATOM_WIN, win)


def axes_fixed(text):
    text = sub(text, "| coverage | 9.72 → 10.0 | 133/133", "| coverage | 9.72 → 10.0 | 138/138")
    text = sub(text, "| depth | 10 → 10 | 20/20", "| depth | 10 → 10 | 23/23")
    return text


def add_side_rev(text, sha8):
    """Cite a revision that exists but is not an ancestor of the measured rev."""
    anchor = "The arm's correctness depends on the two flags' order (R46-CL6)"
    return sub(text, anchor, f"An auxiliary sweep ran at `{sha8}` on a side branch.\n" + anchor)


def corr(text, lines):
    return text.rstrip("\n") + "\n\n" + CORR_HEAD + "\n\n" + "\n".join(lines) + "\n"


def atoms_of(card):
    sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-47")
    sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-46")
    import record
    out = []
    for rnd, txt in record.sections(card):
        out.extend(record.collect(txt, rnd, lambda p: None, "/", "HEAD"))
    out.extend(record.collect_axes(card))
    return out


def build(name, side_sha8=None):
    t = BASE
    if name == "A1-exempt-every-atom":
        # the maximal vacuity attempt: one correction per atom, record untouched
        lines = []
        for a in atoms_of(t):
            c, k = a["class"], str(a["key"])
            if c == "seats":
                lines.append(f"- corrects seats round-{k}: 2 waves, 76 seats total")
            elif c == "window":
                lines.append(f"- corrects window round-{k}: empty in {EMPTY_WIN}")
            elif c == "path":
                lines.append(f"- corrects path {k}: present")
            elif c == "rev":
                lines.append(f"- corrects rev {k}: resolves")
            elif c == "axes":
                # the claim's clause-3 axes form (CORR cannot parse it)
                lines.append(f"- corrects axes {k}: 138/138")
        return corr(t, lines)

    if name == "A2-ghost-atom":
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        "- corrects path does/not/exist/at/any/revision.md: never"])

    if name == "A3-seats-total-contradicted":
        return corr(t, ["- corrects seats round-45: 2 waves, 75 seats total",
                        f"- corrects window round-46: empty in {EMPTY_WIN}"])

    if name == "A4-window-not-empty":
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        "- corrects window round-46: empty in "
                        "31820472..13a9e9e1 -- tools/round-46 plans/round-46-claims.md"])

    if name == "A5-window-other-pair":
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        "- corrects window round-46: empty in "
                        "13a9e9e1..13a9e9e1 -- corpus/knowledge/"])

    if name == "A6-false-split-exempt":
        t = seats(t, 36, 40)          # swapped split: total 76 right, waves wrong
        t = axes_fixed(t)
        t = window(t, EMPTY_WIN)
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        f"- corrects window round-46: empty in {EMPTY_WIN}"])

    if name == "A7-nonancestor-rev-exempt":
        assert side_sha8, "A7 needs a side-branch sha"
        t = seats(t, 36, 40)
        t = axes_fixed(t)
        t = window(t, EMPTY_WIN)
        t = add_side_rev(t, side_sha8)
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        f"- corrects window round-46: empty in {EMPTY_WIN}",
                        f"- corrects rev {side_sha8}: measured on a side branch"])

    if name == "A8-duplicate-corrections":
        t = seats(t, 40, 36)          # record made true by hand
        t = axes_fixed(t)
        t = window(t, EMPTY_WIN)
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        "- corrects seats round-45: 2 waves, 76 seats total"])

    if name == "A9-short-key":
        t = seats(t, 40, 36)
        t = axes_fixed(t)
        t = window(t, EMPTY_WIN)
        return corr(t, ["- corrects seats 45: 2 waves, 76 seats total",
                        f"- corrects window round-46: empty in {EMPTY_WIN}"])

    if name == "A10-honest-landing":
        t = seats(t, 40, 36)
        t = axes_fixed(t)
        t = window(t, EMPTY_WIN)
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        f"- corrects window round-46: empty in {EMPTY_WIN}"])

    if name == "A11-exempt-cap":
        assert side_sha8, "A11 needs a side-branch sha"
        t = seats(t, 36, 40)
        t = axes_fixed(t)
        t = window(t, EMPTY_WIN)
        for _ in range(3):
            t = add_side_rev(t, side_sha8)
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        f"- corrects window round-46: empty in {EMPTY_WIN}",
                        "- corrects rev %s: measured on a side branch" % side_sha8])

    if name == "A12-axes-correction-dropped":
        t = axes_fixed(t)
        t = seats(t, 40, 36)
        t = window(t, EMPTY_WIN)
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        f"- corrects window round-46: empty in {EMPTY_WIN}",
                        "- corrects axes coverage: 138/138",
                        "- corrects axes depth: 23/23"])


    if name == "A1b-exempt-all-true":
        lines = []
        for a in atoms_of(t):
            c, k = a["class"], str(a["key"])
            if c == "seats":
                total = {"45": 76, "46": 80}.get(k, 0)
                lines.append(f"- corrects seats round-{k}: 2 waves, {total} seats total")
            elif c == "window":
                lines.append(f"- corrects window round-{k}: empty in {EMPTY_WIN}")
            elif c == "path":
                lines.append(f"- corrects path {k}: present")
            elif c == "rev":
                lines.append(f"- corrects rev {k}: resolves")
            elif c == "axes":
                lines.append(f"- corrects axes {k}: 138/138")
        return corr(t, lines)

    if name == "A13-window-unrelated-pair":
        t = seats(t, 36, 40)
        t = axes_fixed(t)
        # the record's window claim keeps its <tip> placeholder
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        "- corrects window round-46: empty in "
                        "13a9e9e1..13a9e9e1 -- corpus/knowledge/"])

    if name == "A14-decorative-historical":
        t = seats(t, 40, 36)
        t = axes_fixed(t)
        t = window(t, EMPTY_WIN)
        return corr(t, ["- corrects seats round-45: 2 waves, 76 seats total",
                        f"- corrects window round-46: empty in {EMPTY_WIN}",
                        "- corrects seats round-40: 2 waves, 80 seats total"])

    raise SystemExit("unknown attack " + name)


if __name__ == "__main__":
    name = sys.argv[1]
    side = sys.argv[2] if len(sys.argv) > 2 else None
    sys.stdout.write(build(name, side))
