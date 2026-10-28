#!/usr/bin/env python3
"""Recount round-49 wave-1 seats from the committed dispatch, registry, and spec."""
import collections
import hashlib
import json
import subprocess

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "decc5697bfd4ec1e9de4a762ad199d9bd9c4230d"
LAND = "29883d4ec35a31a8393c4ffb220888c44c0bb022"
EVID = "14936cb9df3897f89f8bc1eef3fe269f7d7df313"
PATHS = {
    "dispatch": ".ufo/waves/round-49/w1-dispatch.json",
    "registry": ".ufo/waves/round-49/w1/swarm-registry.json",
    "spec": ".ufo/waves/round-49/w1-spec.json",
}
QUOTED = (
    ("executor", 10),
    ("reviewer", 9),
    ("scout", 9),
    ("scribe", 6),
    ("critic", 5),
    ("mutation-tester", 4),
    ("connector", 2),
    ("revenger", 1),
    ("sentinel", 1),
    ("simplifier", 1),
)
ATTACK = {"reviewer", "critic", "mutation-tester"}


def git(*args):
    p = subprocess.run(["git", "-C", LANE, *args], capture_output=True)
    if p.returncode != 0:
        raise SystemExit("git %s -> %s %s" % (" ".join(args), p.returncode, p.stderr.decode()[:200]))
    return p.stdout


def show(rev, path):
    return git("show", "%s:%s" % (rev, path))


def roles_dispatch(doc):
    return doc["counts"], {n: m["role"] for n, m in doc["registry"]["members"].items()}


def roles_registry(doc):
    return {n: m["role"] for n, m in doc["members"].items()}


def roles_spec(doc):
    return {i["name"]: i["role"] for i in doc["items"]}


def hist(roles):
    return collections.Counter(roles.values())


def main():
    loaded = {}
    for key, rel in PATHS.items():
        blobs = {rev: show(rev, rel) for rev in (EVID, FREEZE, LAND)}
        wt = open(LANE + "/" + rel, "rb").read()
        same = len({hashlib.sha256(b).hexdigest() for b in list(blobs.values()) + [wt]}) == 1
        print("%s bytes=%d sha256=%s identical_evidence_freeze_land_worktree=%s" % (
            key, len(wt), hashlib.sha256(wt).hexdigest(), same))
        loaded[key] = json.loads(wt.decode())
    counts, d_roles = roles_dispatch(loaded["dispatch"])
    r_roles = roles_registry(loaded["registry"])
    s_roles = roles_spec(loaded["spec"])
    print("dispatch.counts %s" % json.dumps(counts, sort_keys=True))
    print("n dispatch=%d registry=%d spec=%d" % (len(d_roles), len(r_roles), len(s_roles)))
    print("name_sets_equal %s" % (set(d_roles) == set(r_roles) == set(s_roles)))
    print("roles_equal %s" % (d_roles == r_roles == s_roles))
    h = hist(d_roles)
    print("role_hist %s" % " ".join("%s=%d" % (k, h[k]) for k, _ in QUOTED))
    print("quoted_match %s" % all(h[k] == n for k, n in QUOTED))
    print("unexpected_roles %s" % sorted(set(h) - {k for k, _ in QUOTED}))
    attack = sum(h[k] for k in ATTACK)
    print("attack %d/%d" % (attack, len(d_roles)))
    names = set(d_roles)
    for rev in (EVID, FREEZE, LAND):
        files = git("ls-tree", "-r", "--name-only", rev, "--", ".ufo/waves/round-49/w1").decode().splitlines()
        top = set()
        for p in files:
            rel = p.split(".ufo/waves/round-49/w1/", 1)[1]
            if "/" not in rel and rel.endswith(".md"):
                top.add(rel[:-3])
        missing = sorted(names - top)
        extra = sorted(top - names)
        print("reports %s top_md=%d missing=%s extra=%s" % (rev[:12], len(top), ",".join(missing), ",".join(extra)))


if __name__ == "__main__":
    main()
