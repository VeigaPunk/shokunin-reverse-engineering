#!/usr/bin/env python3
"""RV-4 prose-patch applier — wave arc3-loop1-round4, chain c2, seat RV-4.

The round-3/round-4 patch texts are prose `.patch.md` files whose change is
carried in a fenced code block as `-` / `+` hunk lines (see
`arc3-loop1-round3/claims/c2/EX-24/proposed-coverage-count.patch.md`).  This
applier reads such a file and applies each hunk to a target tree by CONTENT
match, so it does not depend on the patch author's line numbers.

Usage:
    prose-apply.py <PATCH.md> <TREE-DIR>

A fenced block is treated as a hunk when it contains at least one line starting
with `-` and at least one starting with `+`.  Consecutive `-` lines form the
search text; the following `+` lines form the replacement.  A leading
`# file: <path>` (or `# <path>`) comment inside the block, or a
`` `path` `` mention on the line introducing the fence, sets the target file;
absent both, the file named in the patch's first `# ...` heading is used.

Exit 0 when every hunk applied; 1 when a hunk failed; 2 on usage error.
Prints a per-hunk report to stdout (the caller tees it to its run log).
"""
import os
import re
import sys


FENCE = re.compile(r"^```")
PATH_HINT = re.compile(r"`([A-Za-z0-9_./-]+\.(?:md|py|sh|json|toml|txt))`")


def read(path):
    with open(path, encoding="utf-8", errors="replace") as fh:
        return fh.read()


def hunks(text):
    """Yield (target_hint, minus_lines, plus_lines) for every hunk.

    A fenced block may carry one bare `-`/`+` group or a unified diff with
    several `@@` sections; each `@@` section is yielded separately so a
    multi-hunk patch applies section by section.  Within a section, consecutive
    `-` lines form the search text and the following `+` lines the replacement.
    """
    lines = text.splitlines()
    i, cur_file = 0, None
    while i < len(lines):
        line = lines[i]
        m = PATH_HINT.search(line)
        if m:
            cur_file = m.group(1)
        if FENCE.match(line):
            body, j = [], i + 1
            while j < len(lines) and not FENCE.match(lines[j]):
                body.append(lines[j])
                j += 1
            hint = cur_file
            for b in body[:3]:
                if b.startswith("# file:"):
                    hint = b.split(":", 1)[1].strip()
                elif b.startswith("# ") and "/" in b:
                    hint = b[2:].strip().split()[0].rstrip(":")
            # split the block into @@-delimited sections (or one implicit section)
            sections, cur = [], None
            for b in body:
                if b.startswith("@@"):
                    if cur:
                        sections.append(cur)
                    cur = []
                elif b.startswith("---") or b.startswith("+++"):
                    continue
                elif cur is not None:
                    cur.append(b)
            if cur:
                sections.append(cur)
            if not sections:
                sections = [body]
            for sec in sections:
                minus, plus, mode = [], [], None
                for b in sec:
                    if b.startswith("-"):
                        minus.append(b[1:]); mode = "-"
                    elif b.startswith("+"):
                        plus.append(b[1:]); mode = "+"
                    elif mode == "-":
                        minus.append(b)          # context line inside the search
                if minus and plus:
                    yield hint, minus, plus
            i = j + 1
            continue
        i += 1


def apply_hunk(tree, hint, minus, plus):
    if not hint:
        return "no target file named in the patch"
    path = os.path.join(tree, hint)
    if not os.path.isfile(path):
        return "target %r not present in the scratch tree" % hint
    src = read(path)
    search = "\n".join(minus)
    if search not in src:
        return "search text not found verbatim in %s" % hint
    if src.count(search) != 1:
        return "search text is ambiguous in %s (%d occurrences)" % (hint, src.count(search))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(src.replace(search, "\n".join(plus), 1))
    return None


def main(argv):
    if len(argv) != 3:
        print("usage: prose-apply.py <PATCH.md> <TREE-DIR>", file=sys.stderr)
        return 2
    patch, tree = argv[1], argv[2]
    text = read(patch)
    print("patch   : %s" % patch)
    print("tree    : %s" % tree)
    n_ok = n_fail = 0
    for idx, (hint, minus, plus) in enumerate(hunks(text), 1):
        err = apply_hunk(tree, hint, minus, plus)
        if err:
            n_fail += 1
            print("  hunk %d [%s]: FAILED — %s" % (idx, hint or "?", err))
        else:
            n_ok += 1
            print("  hunk %d [%s]: applied (%d - / %d +)"
                  % (idx, hint, len(minus), len(plus)))
    print("hunks: applied=%d failed=%d" % (n_ok, n_fail))
    if n_ok == 0 and n_fail == 0:
        print("no fenced -/+ hunk found in this patch text")
        return 1
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
