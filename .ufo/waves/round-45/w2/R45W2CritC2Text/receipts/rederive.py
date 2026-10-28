#!/usr/bin/env python3
"""Re-derive the instrument set named by the two frozen claim files and diff it
against tools/round-45/registry-scope.json. Read-only."""
import json
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
TOOL = re.compile(r"tools/[A-Za-z0-9._/-]+\.(?:py|sh|mjs)")


def paths(rel):
    text = open(f"{LANE}/{rel}").read()
    return sorted(set(TOOL.findall(text)))


r44 = paths("plans/round-44-claims.md")
r45 = paths("plans/round-45-claims.md")
named = sorted(set(r44) | set(r45))
scope = json.load(open(f"{LANE}/tools/round-45/registry-scope.json"))["paths"]

print(json.dumps({
    "round-44-claims tool paths": r44,
    "round-45-claims tool paths": r45,
    "union_named": named,
    "scope": scope,
    "named_minus_scope": sorted(set(named) - set(scope)),
    "scope_minus_named": sorted(set(scope) - set(named)),
    "counts": {"named": len(named), "scope": len(scope)},
}, indent=1, sort_keys=True))
