#!/usr/bin/env python3
"""C1Refs — clause-8 (and clause-9) probes against the FROZEN counter tools/round-47/exact.py.

Three verdicts per case:
  lane   : score() with files read from the lane at REV (the real artefact verdict)
  fixture: score() with files from a one-commit fixture repo holding only the files the
           battery copies (`_fixture_files`) — this is what the battery itself scores
  battery: run_battery() on that fixture repo, then score() with battery=
Nothing in the lane tree is written; every fixture lives under $HYAKU_SCRATCH.
"""
import json
import os
import shutil
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "5017e1f7299c3a812e87e7950148f54313dd279e"
SCRATCH = os.environ["HYAKU_SCRATCH"]
sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import exact  # noqa: E402
import gate   # noqa: E402

CAND = """- **24. An instrument's binding is an equality, not a containment, and its denominator is pinned.** <!-- exactness-table v3 --> Block 23 stated what makes a freeze claim checkable; this one states what makes a *check* exact — each row is a defect the round-46 non-author spot-check routed (`corpus/lessons/round-46.md:57-66`), the loose binding that let a forgery pass it, and the clause of `tools/round-47/exact.py` that now fails the forgery. Interpreter pin: `tools/round-47/exact.py` `interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c`; the counter's own mutation list is pinned as `mutations_sha256:19a2166e47c5231997063a7bc21a7224dda1aa0773bab9c6ffa80ea453d5a112` over `substring-arm`, `duplicate-routed-id`, `stale-mutations-digest`, `flag-order-drift`. Source S143.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` in the arm-vocabulary test | containment over a lowercased cell, so any superstring passes while nothing is measured | symbol | 1 |
| R46-CL3 a row claims a routed id another row already addresses | the id check asks whether the id appears in some row, never whether it appears once | once | 1 |
| R46-CL4 deleting a mutation changes the denominator the claim is judged on | the count is compared with a number the code computes and nothing pins the list | digest | 1 |
| R46-CL6 one flag reorder (`--diff-merges=first-parent -m`) prints a merge twice and blinds the arm | the argument order is a convention no clause reads | order | 1 |

  Refs: `corpus/lessons/round-46.md:57-66` (the four routed instrument defects this matrix closes), `corpus/lessons/round-46.md:21` (M46-2: a denominator the code computes is not a pinned denominator), `corpus/lessons/round-46.md:60-62` (R46-CL3), `corpus/lessons/round-46.md:63-64` (R46-CL4), `corpus/lessons/round-46.md:65-70` (R46-CL6), `plans/round-47-claims.md:70-89` (the nine clauses this block is scored by), `plans/round-47-claims.md:83-84` (clause 8). S143 grounds the equality.
"""
BODY = CAND[4:]          # block body as the parser sees it (leading "- **" is the delimiter)

FILES = [exact.CLAIMS, exact.SELF, exact.GATE46, exact.MUST_CITE, "corpus/lessons/round-45.md"]


def wt_skill():
    with open(os.path.join(LANE, "SKILL.md")) as fh:
        return fh.read()


def rev_files():
    out = {p: gate.show(LANE, REV, p) for p in FILES}
    return {k: v for k, v in out.items() if v is not None}


def block_of(skill):
    blocks = exact.blocks_of(skill)
    marked = [b for b in blocks if exact.MARKER in b]
    return blocks, (marked[0] if len(marked) == 1 else None)


def probe(name, block_body, base="wt"):
    """`block_body` is the marked block as the parser sees it (no leading '- **')."""
    files = rev_files()
    if base == "wt":
        skill = wt_skill()
        blocks, cur = block_of(skill)
        if cur is None:
            return {"case": name, "error": "working tree has no single marked block"}
        if block_body is not None:
            skill = skill.replace(cur, block_body, 1)
    else:
        skill = gate.show(LANE, REV, "SKILL.md")
        blocks, _ = block_of(skill)
        skill = skill.replace(blocks[-1], blocks[-1] + "- **" + block_body, 1)
    lane_at = lambda p: gate.show(LANE, REV, p)  # noqa: E731
    lane_code, lane_rec = exact.score(skill, lane_at, "v3", REV, battery=None)

    files["SKILL.md"] = skill
    d, rev = exact._repo(files, SCRATCH, prefix="c1refs-")
    out = {"case": name, "base": base, "lane_exit": lane_code,
           "lane_failing": lane_rec.get("failing", lane_rec.get("reason")),
           "lane_refs": lane_rec.get("refs"), "lane_cited": lane_rec.get("cited"),
           "lane_unresolved": lane_rec.get("unresolved_citations"),
           "lane_pins": [lane_rec.get("mutations_sha256") == lane_rec.get("mutations_sha256_expected"),
                         lane_rec.get("interpreter_sha256") == lane_rec.get("interpreter_sha256_expected")],
           "gate_order": [lane_rec.get("gate_order_literal"), lane_rec.get("gate_order_reversed")]}
    try:
        fx_at = lambda p: gate.show(d, rev, p)  # noqa: E731
        fx_code, fx_rec = exact.score(skill, fx_at, "v3", rev, battery=None)
        bat = exact.run_battery(d, rev, SCRATCH)
        full_code, full_rec = exact.score(skill, fx_at, "v3", rev, battery=bat)
        out.update({"fixture_exit": fx_code,
                    "fixture_failing": fx_rec.get("failing", fx_rec.get("reason")),
                    "fixture_unresolved": fx_rec.get("unresolved_citations"),
                    "battery_exit": full_code,
                    "battery_failing": full_rec.get("failing"),
                    "battery": {k: bat.get(k) for k in ("forgeries_total", "v2_green",
                                                        "v3_green", "genuine_green",
                                                        "crash", "genuine_exit", "error")}})
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return out


def refs_of(body):
    return body[body.index("  Refs: "):]


def with_refs(body, refs):
    return body[:body.index("  Refs: ")] + refs


CASES = [
    ("A-working-tree-block", "wt"),
    ("B-candidate", "rev"),
    ("C-candidate-plus-knowledge-cite", "rev"),
    ("D-vacuous-three-repeats", "rev"),
    ("E-directory-citation", "rev"),
    ("F-gate46-path-cited", "rev"),
    ("G-selector-zero", "rev"),
    ("H-selector-past-eof", "rev"),
    ("I-swapped-pin", "rev"),
    ("J-no-lesson-cite", "rev"),
    ("K-arm-cell-colon-annotated", "rev"),
    ("L-unquoted-citation", "rev"),
    ("J2-lesson-absent-entirely", "rev"),
    ("M-one-selector-dropped", "rev"),
    ("O-floor-three-refs", "rev"),
    ("P-self-padded-floor", "rev"),
    ("R-refs-floor-two", "rev"),
    ("P2-self-padded-two-selected", "rev"),
]


def build(name, body):
    if name.startswith("C"):
        return with_refs(body, refs_of(body).rstrip("\n") +
                         ", `corpus/knowledge/2026-10-25-r34b-pre-freeze-shortcut-replay-gate-stop.md:40-66`"
                         " (QUALITY row 77a: the depth proxy counts a knowledge citation).\n")
    if name.startswith("D"):
        return with_refs(body, "  Refs: `corpus/lessons/round-46.md:57`, `corpus/lessons/round-46.md:57`, "
                               "`corpus/lessons/round-46.md:57`.\n")
    if name.startswith("E"):
        return with_refs(body, "  Refs: `corpus/lessons/round-46.md:1`, `plans/round-47-claims.md:1`, "
                               "`plans/:1`, `tools/round-47/:1-2`.\n")
    if name.startswith("F"):
        return with_refs(body, refs_of(body).rstrip("\n") + ", `tools/round-46/gate.py:99` (the argv literal).\n")
    if name.startswith("G"):
        return with_refs(body, refs_of(body).replace("round-46.md:57-66", "round-46.md:0-66"))
    if name.startswith("H"):
        return with_refs(body, refs_of(body).replace("round-46.md:57-66", "round-46.md:57-103"))
    if name.startswith("I"):
        return body.replace(
            "interpreter_sha256:dcef54f1b14326c33b89a4c55e766832c2a938241968c1d3db1389f9b26c412c",
            "interpreter_sha256:" + "0" * 64)
    if name == "J-no-lesson-cite":
        return with_refs(body, "  Refs: `plans/round-47-claims.md:70-89`, `plans/round-47-claims.md:83-84`.\n")
    if name.startswith("K"):
        return body.replace("| symbol |", "| `symbol` (the equality) |") \
                   .replace("| once |", "| once (the equality) |") \
                   .replace("| digest |", "| digest (the equality) |") \
                   .replace("| order |", "| order (the equality) |")
    if name.startswith("J2"):
        body = body.replace("corpus/lessons/round-46.md", "corpus/lessons/round-45.md")
        return body
    if name.startswith("M"):
        return with_refs(body, refs_of(body).replace("`plans/round-47-claims.md:70-89`",
                                                     "`plans/round-47-claims.md`"))
    if name.startswith("O"):
        return with_refs(body, "  Refs: `corpus/lessons/round-46.md:57`, "
                               "`plans/round-47-claims.md:1`.\n")
    if name == "P-self-padded-floor":
        return with_refs(body, "  Refs: `tools/round-47/exact.py`, "
                               "`corpus/lessons/round-46.md:57`, "
                               "`plans/round-47-claims.md:1`; the interpreter is "
                               "`tools/round-47/exact.py`.\n")
    if name.startswith("P2"):
        body = body.replace("(`corpus/lessons/round-46.md:57-66`)", "(the routed defects)")
        return with_refs(body, "  Refs: `tools/round-47/exact.py`, "
                               "`corpus/lessons/round-46.md:57`, "
                               "`plans/round-47-claims.md:1`.\n")
    if name.startswith("R"):
        body = body.replace("`tools/round-47/exact.py` ", "")
        return with_refs(body, "  Refs: `corpus/lessons/round-46.md:57`.\n")
    if name.startswith("L"):
        return with_refs(body, refs_of(body).replace("`corpus/lessons/round-46.md:60-62`",
                                                     "corpus/lessons/round-46.md:60-62"))
    return body


def main(names=None):
    out = []
    for name, base in CASES:
        if names and name not in names:
            continue
        try:
            body = None if base == "wt" else build(name, BODY)
            out.append(probe(name, body, base=base))
        except Exception as exc:  # noqa: BLE001
            out.append({"case": name, "crash": f"{type(exc).__name__}: {exc}"})
    print(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    main(sys.argv[1:] or None)
