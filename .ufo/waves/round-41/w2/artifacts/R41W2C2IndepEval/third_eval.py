#!/usr/bin/env python3
"""Third independent evaluator for R41-C2, written ONLY from the frozen
`**Label precedence (frozen ...)**` text in plans/round-41-claims.md
(lines 109-132 of the frozen file). It does not read the SKILL table,
the frozen interpreter (sqfs-triage-v3.py) or the frozen evaluator
(indep-eval-v3.py).

Usage:
  python3 third_eval.py <envelope.json ...> [--json-out out.json]

Prints per-envelope features + decision to stdout (JSON lines); with
--json-out also writes a single JSON object.
"""

import json
import sys

# --- feature extraction (only from the envelope bytes) ---------------------

def features(env):
    nr = env.get("normalized_result") or {}
    op = env.get("operation")
    pr = (env.get("provider") or {}).get("id")

    chunks = nr.get("chunks") or []
    gaps = nr.get("extraction_gaps") or []
    diags = nr.get("diagnostics") or []

    # H = handler names in chunks[].handler ∪ extraction_gaps[].handler (nulls dropped)
    H = set()
    for c in chunks:
        h = c.get("handler")
        if h:
            H.add(h)
    for g in gaps:
        h = g.get("handler")
        if h:
            H.add(h)

    # G = set of extraction_gaps[].kind
    G = set()
    for g in gaps:
        k = g.get("kind")
        if k:
            G.add(k)

    # D = union of gaps' dependencies, compared by exact name
    D = set()
    for g in gaps:
        for dep in (g.get("dependencies") or []):
            D.add(dep)

    # BE = yes if any recorded child argv in diagnostics[].report.command carries
    # the token "-be"; no if argvs are recorded and none carries it; n/a if none recorded.
    cmds = []
    for d in diags:
        rep = d.get("report") or {}
        if isinstance(rep.get("command"), str):
            cmds.append(rep["command"])
    if not cmds:
        be = "n/a"
    elif any("-be" in cmd.split() for cmd in cmds):
        be = "yes"
    else:
        be = "no"

    # SR = yes iff a MaliciousSymlinkRemoved producer report is in diagnostics
    sr = any((d.get("report") or {}).get("__typename__") == "MaliciousSymlinkRemoved"
             for d in diags)

    # P = number of files (absent reads 0)
    P = len(nr.get("files") or [])

    return {
        "op": op, "pr": pr,
        "H": sorted(H), "G": sorted(G), "D": sorted(D),
        "BE": be, "SR": sr, "P": P,
    }


# --- precedence steps (verbatim from the frozen text) ----------------------

def decide(fx):
    op, pr = fx["op"], fx["pr"]
    H, G, D = set(fx["H"]), set(fx["G"]), set(fx["D"])
    be, sr, P = fx["BE"], fx["SR"], fx["P"]

    # 1. OP ≠ extract_firmware or PR ≠ unblob (exact, case-sensitive) → unclassified/none
    if op != "extract_firmware" or pr != "unblob":
        return 1, "unclassified", "none"

    # 2. no squashfs_v4_* handler in H → no-squashfs-chunk/inspect-input
    if not any(h.startswith("squashfs_v4_") for h in H):
        return 2, "no-squashfs-chunk", "inspect-input"

    # 3. missing-extractor-dependency ∈ G…
    if "missing-extractor-dependency" in G:
        if "sasquatch-v4be" in D:
            return 3, "dep-missing-be", "install-extractor-be"
        if "sasquatch" in D:
            return 3, "dep-missing-le", "install-extractor-le"
        # a dependency gap naming neither continues at step 4

    # 4. extractor-failure ∈ G and P > 0 → partial-body-failure/salvage-partial
    if "extractor-failure" in G and P > 0:
        return 4, "partial-body-failure", "salvage-partial"

    # 5. extractor-failure ∈ G, P = 0, BE = no, failing chunk's handler (else H)
    #    is squashfs_v4_be → avm-marker-be-dropped/wrap-extractor-be
    if "extractor-failure" in G and P == 0 and be == "no" \
            and "squashfs_v4_be" in H:
        return 5, "avm-marker-be-dropped", "wrap-extractor-be"

    # 6. extractor-failure ∈ G, P = 0 → body-extractor-failure/preserve-failure
    if "extractor-failure" in G and P == 0:
        return 6, "body-extractor-failure", "preserve-failure"

    # 7. depth-limited ∈ G → depth-limited/raise-depth
    if "depth-limited" in G:
        return 7, "depth-limited", "raise-depth"

    # 8. SR = yes and unpublished-entry ∈ G → mixed-symlinks/audit-symlinks
    if sr and "unpublished-entry" in G:
        return 8, "mixed-symlinks", "audit-symlinks"

    # 9. SR = yes and G = ∅ → escaping-symlink-removed/expect-link-absent
    if sr and not G:
        return 9, "escaping-symlink-removed", "expect-link-absent"

    # 10. G = {unpublished-entry} exactly → in-tree-symlink-metadata/count-gap
    if G == {"unpublished-entry"}:
        return 10, "in-tree-symlink-metadata", "count-gap"

    # 11. G = ∅: P > 0 → clean/none; P = 0 → clean-empty/confirm-empty
    if not G:
        if P > 0:
            return 11, "clean", "none"
        return 11, "clean-empty", "confirm-empty"

    # 12. anything else → unclassified/none
    return 12, "unclassified", "none"


def evaluate(env):
    fx = features(env)
    step, label, action = decide(fx)
    return {"features": fx, "step": step, "label": label, "action": action}


def main(argv):
    out_path = None
    paths = []
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--json-out":
            i += 1
            out_path = argv[i]
        else:
            paths.append(a)
        i += 1

    results = []
    for p in paths:
        with open(p, "r", encoding="utf-8") as fh:
            env = json.load(fh)
        ev = evaluate(env)
        ev["input"] = p
        results.append(ev)
        print(json.dumps(ev, sort_keys=True))
    if out_path:
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
