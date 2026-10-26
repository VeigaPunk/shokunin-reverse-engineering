#!/usr/bin/env python3
"""mintable.py -- find smallest v4-grammar first-match tables scoring a tuple
universe (the round-42 C2 shortcut search).

Grammar (L1 decision from R42C2Grammar, 2026-10-26): the v4 table has a
13th column `failing handler` placed right after `handler`, a glob matched
against HF (handlers of extractor-failure gaps; if none carries a handler,
HF = F); `*` matches anything including an empty HF.  The `handler` cell
globs over F (any handler in F matches; `none` = F empty).  The
`dependencies` cell gains the contains form `name+` (D holds name), like gap
kinds.

Model: a table is an ordered list of rows; each row is a 13-cell v4-grammar
rule.  classify_table(t) is the pair of the first matching row, else
(unclassified, none).  A table scores a universe U iff classify_table(t) ==
expected(t) for every t in U.

Because a row carries exactly one (label, action) pair and a group is the set
of tuples sharing one expected pair, the minimum possible row count is the
number of non-unclassified groups.  The search finds, for the full universe
and for every one-class-deleted universe: (a) whether that minimum is
attainable, (b) a concrete minimal table, and (c) the ordering/cell choices
that make it work.
"""
import json
import os
import sys
from itertools import product

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v4eval import ACTION_BY_LABEL, NOMATCH_PAIR  # noqa: E402

KINDS = ("extractor-failure", "depth-limited", "unpublished-entry",
         "missing-extractor-dependency", "unknown-chunk-handler")
DEPS = ("sasquatch", "sasquatch-v4be")
SQUASHFS_PREFIX = "squashfs_"
HANDLER_PATTERNS = (
    "*", "none",
    "squashfs_*", "squashfs_v4_*", "squashfs_v4_be", "squashfs_v4_le",
    "squashfs_v[123]*", "squashfs_v3*", "squashfs_v3",
    "squashfs_v1*", "squashfs_v2*",
    "squashfs_v3_ddwrt", "squashfs_v3_broadcom",
)


def fnmatch_case(name, pat):
    import fnmatch
    return fnmatch.fnmatchcase(name, pat)


def f_of(h):
    return [n for n in h if n.startswith(SQUASHFS_PREFIX)]


def handler_matches(spec, f):
    if spec == "*":
        return True
    if spec == "none":
        return not f
    return any(fnmatch_case(v, spec) for v in f)


def failing_handler_matches(spec, hf):
    if spec == "*":
        return True
    return any(fnmatch_case(v, spec) for v in (hf or []))


def gap_matches(spec, g):
    if spec == "*":
        return True
    if spec == "none":
        return not g
    if spec.endswith("+"):
        body = spec[:-1]
        return set(body.split(",")) <= set(g)
    return set(spec.split("+")) == set(g)


def dep_matches(spec, d):
    if spec == "*":
        return True
    if spec == "none":
        return not d
    if spec.endswith("+"):
        body = spec[:-1]
        return set(body.split(",")) <= set(d)
    return set(spec.split("+")) == set(d)


def row_matches(row, f):
    if row["op"] != "*" and row["op"] != f["OP"]:
        return False
    if row["pr"] != "*" and row["pr"] != f["PR"]:
        return False
    if not handler_matches(row["handler"], f_of(f["H"])):
        return False
    if not failing_handler_matches(row["fh"], f["HF"]):
        return False
    if not gap_matches(row["gaps"], f["G"]):
        return False
    if not dep_matches(row["deps"], f["D"]):
        return False
    if row["be"] != "*" and row["be"] != f["BE"]:
        return False
    if row["sr"] != "*" and row["sr"] != f["SR"]:
        return False
    if row["files"] == "0" and f["P"] != 0:
        return False
    if row["files"] == ">0" and f["P"] <= 0:
        return False
    return True


def all_match(row, feats_list):
    return all(row_matches(row, f) for f in feats_list)


# ---------------------------------------------------------------------------
# candidate generation per group
# ---------------------------------------------------------------------------

def uniform(vals):
    s = set(vals)
    return next(iter(s)) if len(s) == 1 else None


def patterns_matching_all(patterns, vals_by_member, none_ok):
    out = set()
    for pat in patterns:
        if pat == "none":
            if none_ok and all(not v for v in vals_by_member):
                out.add(pat)
            continue
        if all(any(fnmatch_case(v, pat) for v in vals) for vals in vals_by_member):
            out.add(pat)
    return out


def candidate_cells(group_feats):
    ops = set()
    prs = set()
    handlers = set()
    fhs = set()
    gaps = {"*"}
    deps = {"*"}
    bes = {"*"}
    srs = {"*"}
    files = {"*"}

    ops.add("*")
    ops.add("extract_firmware")
    prs.add("*")
    prs.add("unblob")

    f_vals = [f_of(f["H"]) for f in group_feats]
    handlers |= patterns_matching_all(HANDLER_PATTERNS, f_vals,
                                     none_ok=True)
    hf_vals = [f["HF"] or [] for f in group_feats]
    fhs |= patterns_matching_all(HANDLER_PATTERNS, hf_vals,
                                 none_ok=False)
    fhs.add("*")

    K = set()
    for f in group_feats:
        K |= set(f["G"])
    K = sorted(K)
    if all(not f["G"] for f in group_feats):
        gaps.add("none")
    for r in range(1, min(4, len(K)) + 1):
        for comb in product(K, repeat=r):
            comb = tuple(sorted(set(comb)))
            if len(comb) != r:
                continue
            label = "+".join(comb)
            if all(set(f["G"]) == set(comb) for f in group_feats):
                gaps.add(label)
            if all(set(comb) <= set(f["G"]) for f in group_feats):
                gaps.add(label + "+")

    D = set()
    for f in group_feats:
        D |= set(f["D"])
    D = sorted(D)
    if all(not f["D"] for f in group_feats):
        deps.add("none")
    for r in range(1, min(3, len(D)) + 1):
        for comb in product(D, repeat=r):
            comb = tuple(sorted(set(comb)))
            if len(comb) != r:
                continue
            label = "+".join(comb)
            if all(set(f["D"]) == set(comb) for f in group_feats):
                deps.add(label)
            if all(set(comb) <= set(f["D"]) for f in group_feats):
                deps.add(label + "+")

    beu = uniform([f["BE"] for f in group_feats])
    if beu is not None:
        bes.add(beu)
    sru = uniform([f["SR"] for f in group_feats])
    if sru is not None:
        srs.add(sru)
    pu = uniform(["0" if f["P"] == 0 else ">0" for f in group_feats])
    if pu is not None:
        files.add(pu)

    return ops, prs, handlers, fhs, gaps, deps, bes, srs, files


def build_rows(group_feats, label, action):
    ops, prs, handlers, fhs, gaps, deps, bes, srs, files = candidate_cells(
        group_feats)
    rows = []
    for op, pr, h, fh, g, d, be, sr, fi in product(
            sorted(ops), sorted(prs), sorted(handlers), sorted(fhs),
            sorted(gaps), sorted(deps), sorted(bes), sorted(srs),
            sorted(files)):
        row = {"op": op, "pr": pr, "handler": h, "fh": fh, "gaps": g,
               "deps": d, "be": be, "sr": sr, "files": fi, "label": label,
               "action": action}
        if all_match(row, group_feats):
            rows.append(row)
    return rows



def load_universe(path):
    return json.load(open(path))["universe"]


def groups_of(members):
    g = {}
    for m in members:
        key = tuple(m["expected"])
        g.setdefault(key, []).append(m)
    return g


def group_touched(row, members_by_group):
    touched = set()
    for key, mems in members_by_group.items():
        if any(row_matches(row, m["features"]) for m in mems):
            touched.add(key)
    return touched


def norm_sr(v):
    return "yes" if v is True or v == "yes" else "no"


def prepare(members):
    """returns (groups dict, rows per group with touched sets)."""
    for m in members:
        m["features"]["SR"] = norm_sr(m["features"]["SR"])
    g = groups_of(members)
    rows = {}
    for key, mems in g.items():
        if key == NOMATCH_PAIR:
            rows[key] = []
            continue
        label, action = key
        pool = []
        for r in build_rows([m["features"] for m in mems], label, action):
            pool.append((r, group_touched(r, g)))
        rows[key] = pool
    return g, rows


def search_min(groups, rows, sort_key=None):
    """Return a min-size ordered table (list of (group, row)) or None.

    sort_key(order) scores a complete order (lower is better); among minimal
    row counts the lowest-cost order is returned.  Feasibility of a suffix
    depends only on the SET of placed groups (a row may touch any already
    placed group), so the DFS is memoized on the used-set.
    """
    if sort_key is None:
        sort_key = lambda o: 0
    all_keys = [k for k in groups if k != NOMATCH_PAIR]
    n = len(all_keys)

    def row_cost(r):
        return sum(1 for c in ("op", "pr", "handler", "fh", "gaps",
                               "deps", "be", "sr", "files")
                   if r[c] != "*")

    pools = {}
    for k in all_keys:
        best_row = {}
        for r, t in rows[k]:
            key = frozenset(t)
            cost = row_cost(r)
            if key not in best_row or cost < best_row[key][1]:
                best_row[key] = (r, cost, key)
        pools[k] = sorted(best_row.values(), key=lambda x: x[1])

    fail = set()
    best = [None]
    best_cost = [None]
    used = set()
    order = []

    def bt():
        if len(order) == n:
            cost = sort_key(list(order))
            if best[0] is None or cost < best_cost[0]:
                best[0] = list(order)
                best_cost[0] = cost
            return
        if best[0] is not None and len(order) + (n - len(used)) > len(best[0]):
            return
        key = frozenset(used)
        if key in fail:
            return
        # viable rows per unplaced group: touched subset of used | {group}
        best_k = None
        best_pool = None
        for k in all_keys:
            if k in used:
                continue
            viable = [e for e in pools[k] if all(u in used or u == k
                                                 for u in e[2])]
            if not viable:
                continue
            if best_k is None or len(viable) < len(best_pool):
                best_k = k
                best_pool = viable
        if best_k is None:
            # no group can be placed here: dead end
            fail.add(key)
            return
        for r, _, cost in best_pool:
            used.add(best_k)
            order.append((best_k, r))
            bt()
            order.pop()
            used.discard(best_k)
        fail.add(key)

    bt()
    return best[0] if best[0] else None


# ---------------------------------------------------------------------------
# table rendering
# ---------------------------------------------------------------------------

HEADER = ("label", "operation", "provider", "handler", "failing handler",
          "gap kinds", "dependencies", "-be in child argv",
          "symlink removed", "published files", "action", "cause", "source")


def render_table(order, title, vocab=None):
    lines = [title, ""]
    if vocab is None:
        vocab = sorted({r["action"] for _, r in order})
    lines.append("<!-- sqfs-triage-actions: %s -->" % " ".join(vocab))
    lines.append("")
    lines.append("| " + " | ".join(HEADER) + " |")
    lines.append("| " + " | ".join("---" for _ in HEADER) + " |")
    for i, (key, r) in enumerate(order, start=1):
        cause = "shortcut row %d -> %s" % (i, r["action"])
        cells = [r["label"], r["op"], r["pr"], r["handler"], r["fh"],
                 r["gaps"], r["deps"], r["be"], r["sr"], r["files"],
                 r["action"], cause, "R42C2Shortcuts analysis"]
        lines.append("| " + " | ".join("`%s`" % c for c in cells) + " |")
    lines.append("")
    return "\n".join(lines)


def main():
    universe_path = os.environ.get("UNIVERSE_PATH") or os.path.join(
        os.environ.get("TMPDIR") or HERE, "universe.json")
    members = load_universe(universe_path)
    g, rows = prepare(members)
    non_uncl = sorted(k for k in g if k != NOMATCH_PAIR)
    print("groups:", len(g), "non-unclassified:", len(non_uncl))
    for k in non_uncl:
        pool = rows[k]
        print(" ", k, "members=%d candidate-rows=%d" % (len(g[k]), len(pool))
              + (" (NO ROWS!)" if not pool else ""))
    best = search_min(g, rows)
    if best is None:
        print("NO minimal table found")
        return 1
    print("min rows:", len(best))
    for key, r in best:
        print(" ", key[0], "|", r["handler"], "|", r["fh"], "|",
              r["gaps"], "|", r["deps"], "|", r["be"], "|", r["sr"], "|",
              r["files"])
    out = os.environ.get("MINTABLE_OUT") or os.path.join(
        os.environ.get("TMPDIR") or HERE, "mintable.json")
    with open(out, "w") as fh:
        json.dump({"order": [[list(k), r] for k, r in best],
                   "groups": {str(k): len(v) for k, v in g.items()}},
                  fh, indent=1, sort_keys=True)
    print("wrote", out)


if __name__ == "__main__":
    sys.exit(main())
