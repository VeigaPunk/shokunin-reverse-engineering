#!/usr/bin/env python3
"""Generate rows.md from the byte-identical verified candidate block."""
import hashlib
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r47/C1Tokens"
L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = os.path.join(L, ".ufo/waves/round-47/w1/C1Tokens/rows.md")
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"

raw = subprocess.run([sys.executable, "-I", "-B", os.path.join(S, "mkb.py"), "block"],
                     capture_output=True, text=True, check=True).stdout
blk = raw.rstrip("\n") + "\n"          # canonical bytes: fence text + one newline
bhash = hashlib.sha256(blk.encode()).hexdigest()

CITED = ["corpus/lessons/round-46.md", "plans/round-47-claims.md", "tools/round-47/exact.py"]
SEL = {"corpus/lessons/round-46.md": ["51-69", "57-59", "60-62", "63-64", "65-69"],
       "plans/round-47-claims.md": ["76-77"],
       "tools/round-47/exact.py": ["none: SELF is exempt from the selector rule "
                                   "(tools/round-47/exact.py:149-150)"]}


def show(path):
    return subprocess.run(["git", "-C", L, "show", f"{FREEZE}:{path}"],
                          capture_output=True, text=True, check=True).stdout


def sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


doc = []
doc.append("# C1Tokens — block-24 table rows governed by R47-C1 clause 5\n")
doc.append("Seat `C1Tokens`, round 47 wave 1. Frozen surface "
           "`plans/round-47-claims.md@%s` — clause 5 at `plans/round-47-claims.md:76-77` — "
           "and `tools/round-47/exact.py@%s`.\n" % (FREEZE, FREEZE))
doc.append("Clause 5 is computed by `tools/round-47/exact.py:235-243`:\n")
doc.append("```python\n"
           "arm = [r[2].strip(\"` \") if len(r) > 2 else \"\" for r in rows]\n"
           "receipt[\"arm_tokens\"] = arm\n"
           "if hard:\n"
           "    if any(a not in VOCAB for a in arm):\n"
           "        failing.append(f\"arm cells not exact vocabulary tokens: {arm}\")\n"
           "else:\n"
           "    if any(not any(t in a.lower() for t in VOCAB) for a in arm):\n"
           "        failing.append(\"arm cells outside the vocabulary\")\n"
           "```\n")
doc.append("`VOCAB = (\"symbol\", \"once\", \"digest\", \"order\")` "
           "(`tools/round-47/exact.py:35`). `hard` is `profile == \"v3\"`. The v3 test is "
           "tuple membership of the whole stripped cell, so it is an equality on that cell "
           "and never a containment test on a substring.\n")

doc.append("## The rows this seat drafts (v3-arm cells)\n")
doc.append("| routed id | v3 arm cell (paste verbatim) | why that token is the binding |")
doc.append("| --- | --- | --- |")
for rid, cell, why in [
    ("R46-CL2", "`symbol`",
     "the cell is stripped and then compared for equality, so `blobberish`, `order-ish`, "
     "`symbolmap` and `the symbol arm` all fail under v3 while the v2 profile passes them"),
    ("R46-CL3", "`once`",
     "one routed id per trigger cell, each of the four exactly once — the arm token names "
     "that cardinality binding"),
    ("R46-CL4", "`digest`",
     "`mutations_sha256` pins the counter's own list in order, so a deleted mutation moves "
     "the digest instead of shrinking the denominator"),
    ("R46-CL6", "`order`",
     "the flag-order clause over the round-46 history arm: the literal pair once, the "
     "reversed pair zero times"),
]:
    doc.append(f"| {rid} | {cell} | {why} |")
doc.append("")
doc.append("These four cells are the ones clause 5 governs. They are the only cells of the "
           "block clause 5 reads (`r[2]`, the third column). Everything else in the block "
           "below is drafted to the other clauses and verified together with these.\n")

doc.append("## Ready-to-paste block 24\n")
doc.append("Insert as the **last** craft block: immediately after block 23 "
           "(`SKILL.md:612-631`) and before the `## Config custody for live-probe rounds "
           "(SOP)` heading (`SKILL.md:632`). Canonical bytes = the fenced text below plus "
           "exactly one trailing newline, **%d bytes**, sha256 `%s`.\n" % (len(blk), bhash))
doc.append("```markdown")
doc.append(blk.rstrip("\n"))
doc.append("```\n")
doc.append("Verified: `/fast/scratch/hyaku/kaidoku-r47/C1Tokens/receipt-cli-full.json` is "
           "the counter run over a one-commit fixture whose `SKILL.md` is the freeze's "
           "`SKILL.md` with exactly these bytes inserted at that point — exit 0, "
           "`failing: []`.\n")

doc.append("## Citation selectors, measured at %s\n" % FREEZE)
doc.append("| citation as pasted | selector | resolves at rev | file sha256 at freeze | lines |")
doc.append("| --- | --- | --- | --- | --- |")
for p in CITED:
    body = show(p)
    h, n = sha(body), len(body.splitlines())
    for s in SEL[p]:
        shown = f"`{p}:{s}`" if s[0].isdigit() else f"`{p}` — {s}"
        doc.append(f"| {shown} | `{s}` | {'yes' if s[0].isdigit() else 'exempt'} | `{h}` | {n} |")
doc.append("")
gate_h = sha(show("tools/round-46/gate.py"))
doc.append("`tools/round-46/gate.py` (sha256 `%s`, 247 lines) is read by clause 7 and is "
           "**never named in the block**: `tools/round-46/` lies outside `ALLOW` "
           "(`tools/round-47/exact.py:36`), so one path token naming it would fail clause 8 "
           "with `outside the validated path set`. The block says \"the history arm's flag "
           "order\" in prose and lets the counter read that file itself.\n" % gate_h)
doc.append("Every other mention of a cited path in the block carries its selector; a bare "
           "`corpus/lessons/round-46.md` in the prose would fail clause 8 with "
           "`no line selector` under v3 (`tools/round-47/exact.py:151-153`).\n")

doc.append("## sha256 values the block must carry\n")
doc.append("| pin | value | derivation |")
doc.append("| --- | --- | --- |")
mut = sha("\n".join(["substring-arm", "duplicate-routed-id", "stale-mutations-digest",
                     "flag-order-drift"]))
selfh = sha(show("tools/round-47/exact.py"))
doc.append(f"| `mutations_sha256` | `{mut}` | sha256 over `\"\\n\".join(name for name, _ in "
           "MUTATIONS)`, counter order |")
doc.append(f"| `interpreter_sha256` | `{selfh}` | sha256 of `tools/round-47/exact.py` bytes "
           f"at {FREEZE[:12]} |")
doc.append(f"| block sha256 | `{bhash}` | the fenced text plus one newline ({len(blk)} bytes) |")
doc.append("")
doc.append("The block states all four mutation names because clause 6 requires them named "
           "(`tools/round-47/exact.py:252-255`); the digest alone is not enough.\n")

with open(OUT, "w") as fh:
    fh.write("\n".join(doc) + "\n")
print(json.dumps({"rows_md": OUT, "block_sha256": bhash, "block_bytes": len(blk),
                  "mutations_sha256": mut, "interpreter_sha256": selfh}))
