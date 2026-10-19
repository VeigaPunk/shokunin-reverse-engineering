#!/usr/bin/env python3
"""RV-6 (arc3-loop1-round2) independent census SCOPE creep audit.

Independent of CR-5's round-1 differ (`scope-diff.py`, regex block capture) and
of EX-21's auditor (`scope-audit.py`, line-regex rows): this tool extracts the
`SCOPE` literal via the module AST (`ast.literal_eval` on the assignment), so a
row written in a form a line regex would skip fails loudly instead.

Flag set is restricted to rules that can actually fire (regression found this
round: CR-5's `changed`-loop "DATED end widened" / "DATED start moved earlier"
branches are unreachable — such rows differ in key, so they land in
added/removed, never in `changed`):
  - open-ended bound (end >= 9000)
  - bound reaches the target file's live EOF (end >= its line count)
  - wide added DATED row (>150 lines)
  - widen-by-add/remove (an added row covers a removed row and extends it)
  - coverage loss (a removed row with no same-file, same-width replacement)
  - class flip CURRENT->DATED (and the merge-risk DATED->CURRENT)

Usage:
  scope-creep-audit.py <before.py> <after.py> --root <repo> --expect-rows 20
Exit 0 = no creep flags AND row count unchanged AND (file,start,end) key set
unchanged (marker-only edits at a fixed key are range-neutral re-keys).
Exit 1 = anything else (flags and/or structural change) — printed, never
silent.
"""
import ast, hashlib, json, sys, os


def load_rows(path):
    src = open(path, encoding="utf-8").read()
    tree = ast.parse(src)
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
                getattr(t, "id", None) == "SCOPE" for t in node.targets):
            return src, [tuple(r) for r in ast.literal_eval(node.value)]
    raise SystemExit("NO-SCOPE-ASSIGNMENT: %s" % path)


def line_count(root, fname):
    try:
        with open(os.path.join(root, fname), encoding="utf-8",
                  errors="replace") as fh:
            return len(fh.read().splitlines())
    except OSError:
        return None


def key(r):
    return (r[0], r[1], r[2])


def main():
    args = sys.argv[1:]
    opts = {"--root": ".", "--expect-rows": "20"}
    pos = []
    i = 0
    while i < len(args):
        if args[i] in opts:
            opts[args[i]] = args[i + 1]
            i += 2
        else:
            pos.append(args[i])
            i += 1
    before_p, after_p = pos[0], pos[1]
    expect = int(opts["--expect-rows"])
    root = opts["--root"]

    bsrc, before = load_rows(before_p)
    _, after = load_rows(after_p)
    bset = {key(r): r for r in before}
    aset = {key(r): r for r in after}
    added = [r for k, r in aset.items() if k not in bset]
    removed = [r for k, r in bset.items() if k not in aset]
    changed = [(bset[k], aset[k]) for k in sorted(bset.keys() & aset.keys())
               if bset[k] != aset[k]]

    flags = []
    for (f, s, e, cls, ml, mr) in added:
        n = line_count(root, f)
        if e >= 9000:
            flags.append("CREEP open-ended bound: %s %d-%d %s" % (f, s, e, cls))
        if n is not None and e >= n:
            flags.append("CREEP bound reaches file EOF: %s %d-%d %s (lines=%d)"
                         % (f, s, e, cls, n))
        if cls == "DATED" and (e - s) > 150:
            flags.append("CREEP wide added DATED row: %s %d-%d (%d lines)"
                         % (f, s, e, e - s + 1))
    for (f, s, e, cls, ml, mr) in added:
        for (f2, s2, e2, cls2, ml2, mr2) in removed:
            if f == f2 and s <= s2 and e >= e2 and (s < s2 or e > e2):
                flags.append("CREEP widen-by-add/remove: %s %d-%d %s replaced %d-%d %s"
                             % (f, s, e, cls, s2, e2, cls2))
    for (f2, s2, e2, cls2, ml2, mr2) in removed:
        if not any(a[0] == f2 and (a[2] - a[1]) == (e2 - s2) for a in added):
            flags.append("CREEP row removed (coverage loss): %s %d-%d %s"
                         % (f2, s2, e2, cls2))
    for (b, a) in changed:
        if b[3] == "CURRENT" and a[3] == "DATED":
            flags.append("CREEP class flip CURRENT->DATED: %s %d-%d -> %d-%d"
                         % (b[0], b[1], b[2], a[1], a[2]))
        if b[3] == "DATED" and a[3] == "CURRENT":
            flags.append("CREEP class flip DATED->CURRENT (merge risk): %s %d-%d"
                         % (a[0], a[1], a[2]))

    print("INSTRUMENT before_sha256=%s after_sha256=%s"
          % (hashlib.sha256(bsrc.encode()).hexdigest()[:16],
             hashlib.sha256(open(after_p, 'rb').read()).hexdigest()[:16]))
    print("SCOPE-ROWS before=%d after=%d expected=%d rows_unchanged=%s"
          % (len(before), len(after), expect,
             "YES" if len(before) == len(after) == expect else "NO"))
    print("CANON before_ordered_sha256=%s after_ordered_sha256=%s"
          % (hashlib.sha256(json.dumps(before).encode()).hexdigest()[:16],
             hashlib.sha256(json.dumps(after).encode()).hexdigest()[:16]))
    print("KEYSET identical=%s added_keys=%d removed_keys=%d changed_rows=%d"
          % ("YES" if set(bset) == set(aset) else "NO", len(added), len(removed),
             len(changed)))
    for r in added:
        print("  + %s %d-%d %s marker_line=%s marker=%r" % r)
    for r in removed:
        print("  - %s %d-%d %s marker_line=%s marker=%r" % r)
    for (b, a) in changed:
        print("  ~ %s %d-%d %s -> %d-%d %s (marker %s->%s)"
              % (b[0], b[1], b[2], b[3], a[1], a[2], a[3], b[4], a[4]))
    print("CREEP FLAGS (%d): %r" % (len(flags), flags))
    clean = (not flags and len(before) == len(after) == expect
             and set(bset) == set(aset))
    print("AUDIT: %s" % ("clean" if clean else "dirty"))
    return 0 if clean else 1


if __name__ == "__main__":
    sys.exit(main())
