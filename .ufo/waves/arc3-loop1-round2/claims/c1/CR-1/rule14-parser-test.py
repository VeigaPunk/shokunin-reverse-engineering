#!/usr/bin/env python3
"""CR-1 r2 probe: replay command A's rule-parsing block (SCORECARD.md:104-122)
against scratch SKILL.md variants carrying candidate rule-#14 bullets.

Knowledge files are read as immutable Git objects at HEAD (the experiment does
not touch them). SKILL.md is read from HEAD for the baseline and from the
assembled scratch variant for each candidate. Writes only under /var/tmp.
"""
import hashlib
import json
import pathlib
import re
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "HEAD"
OUT = pathlib.Path("/var/tmp/cr1-r2/variants")
OUT.mkdir(parents=True, exist_ok=True)

T1 = (
    "- **An artifact that records its own byte-identity must re-derive that identity "
    "after every revision; a stale self-identity voids the verification block, not the "
    "work.** The arc3-loop1-round1 entry patch churned mid-wave: its recorded identity "
    "(8,316 B, `f95c5a05…`) stopped describing the artifact it produced — an independent "
    "re-apply read 8,598 B, `d8d85949…` (`.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/"
    "entry-file-identity.txt`; VZ-1 debt D9, `.ufo/waves/arc3-loop1-round1/claims/c1/"
    "VZ-1/verdict.md:149-166`), and the landed bytes were re-derived at landing "
    "(10,225 B, `dd986f56…`, `.ufo/waves/arc3-loop1-round1/claims/cross/wave-summary.md:50`). "
    "Re-derive before citing; the integrator records the fresh identity at landing."
)
T2 = (
    T1
    + " The re-derivation discipline's analogue in the evidence-id family is recorded "
    "where an id held across a day and re-derives byte-exact "
    "(`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11`)."
)
T3 = (
    "- **Cite the source you measured, not the one you remember.** "
    "(`corpus/knowledge/2026-10-13-r3-evm-interface.md:23-25`)"
)
# The actual drafted candidate as landed by seat EX-05 (read from the wave tree).
T4 = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round2/"
    "claims/c1/EX-05/fallback-rule14-candidate.txt"
).read_text().rstrip("\n")
# CR-1 corrected form: incident receipts present, corpus anchor path-only and
# framed as the landing instance (not as defect evidence).
T5 = (
    "- **An artifact that records its own byte-identity re-derives that identity "
    "after every revision.** A verification block that states its subject's size, "
    "hash, or line count holds only against the subject's current bytes: the "
    "identity is re-derived after each revision, a stale self-identity voids the "
    "verification block rather than the work, and the integrator records the fresh "
    "identity at landing. The round-1 entry patch churned mid-wave: its recorded "
    "identity (8,316 B, `f95c5a05…`) stopped describing the artifact it produced — "
    "an independent re-apply read 8,598 B, `d8d85949…` "
    "(`.ufo/waves/arc3-loop1-round1/claims/c1/CR-2/entry-file-identity.txt`; three "
    "applied identities within 20 minutes, `.ufo/waves/arc3-loop1-round1/claims/c1/"
    "VZ-1/verdict.md` debt D9) — and the landed bytes were re-derived at landing "
    "(10,225 B, `dd986f56…`; landing record, SCORECARD.md round-1 section, stamped "
    "2026-10-19). The landing instance is the EVM entry itself: "
    "`corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md`."
)


def git_show(path):
    return subprocess.check_output(["git", "show", f"{REV}:{path}"], text=True, cwd=REPO)


KNOWLEDGE_LEN = {}


def knowledge_len(name):
    if name not in KNOWLEDGE_LEN:
        KNOWLEDGE_LEN[name] = len(git_show("corpus/knowledge/" + name).splitlines())
    return KNOWLEDGE_LEN[name]


def parse(skill_text):
    """Verbatim command-A rule block, applied to a supplied SKILL.md text."""
    craft = skill_text.split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
    rules = re.split(r"(?m)^- \*\*", craft)[1:]
    pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"
    resolved = 0
    detail = []
    for rule in rules:
        refs = re.findall(pattern, rule)
        valid = bool(refs)
        for name, first, last in refs:
            try:
                count = knowledge_len(name)
                start, end = int(first or 1), int(last or first or 1)
                valid = valid and 1 <= start <= end <= count
            except subprocess.CalledProcessError:
                valid = False
        resolved += valid
        detail.append(
            {
                "resolved": bool(valid),
                "refs": refs,
                "head": rule.splitlines()[0][:80],
                "sha256": hashlib.sha256(rule.encode()).hexdigest(),
            }
        )
    return rules, resolved, detail


def assemble(base, candidate):
    """Insertion form B: append after the section's existing trailing blank line,
    so every prior rule block's split segment (including rule 13's tail) is
    byte-identical to the base."""
    idx = base.index("## Queue-drain craft ")
    tail = base[idx:].split("\n## ", 1)
    section = tail[0]  # keeps its trailing blank line(s)
    rest = "\n## " + tail[1]
    return base[:idx] + section + candidate + "\n" + rest


base_text = git_show("SKILL.md")
rules0, resolved0, detail0 = parse(base_text)
print(f"BASE HEAD: rules={len(rules0)} resolved={resolved0}")
json.dump(
    {"rule_blocks": detail0, "count": len(rules0), "resolved": resolved0},
    open(OUT / "rule-blocks-before.json", "w"),
    indent=1,
)

results = {"base": {"count": len(rules0), "resolved": resolved0}}
for name, cand in (("T1", T1), ("T2", T2), ("T3", T3), ("T4-EX05-actual", T4), ("T5-CR1-corrected", T5)):
    variant = assemble(base_text, cand)
    (OUT / f"{name}.SKILL.md").write_text(variant)
    rules, resolved, detail = parse(variant)
    results[name] = {
        "count": len(rules),
        "resolved": resolved,
        "new_rule_resolved": detail[-1]["resolved"],
        "new_rule_refs": detail[-1]["refs"],
        "depth_score": round(10 * resolved / len(rules), 2),
    }
    print(
        f"{name}: rules={len(rules)} resolved={resolved} "
        f"new_rule_resolved={detail[-1]['resolved']} depth={round(10*resolved/len(rules),2)}"
    )
    # prior 13 blocks must be byte-identical across variants
    same = [d["sha256"] for d in detail[:-1]] == [d["sha256"] for d in detail0]
    print(f"   prior-13 byte-identical: {same}")
    results[name]["prior13_byte_identical"] = same

json.dump(results, open(OUT / "rule14-parser-results.json", "w"), indent=1)
print("written:", OUT / "rule14-parser-results.json")
