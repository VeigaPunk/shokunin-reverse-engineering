#!/usr/bin/env python3
"""Generate kaidoku round-71's claims container from the plan and the committed pins.

The three predicate sentences are extracted from plans/round-71-claims.md
(whitespace-normalized) so the container and the plan cannot drift; the five
instrument pins are the blobs at --declaration.  Run from the lane root:

  python3 -I -B .ufo/waves/round-71/gen-claims.py --declaration <hash> --out .ufo/waves/round-71/claims.json
"""
import argparse
import hashlib
import json
import re
import subprocess
import sys

TOOLS = ["tools/round-71/packed-elf.py",
         "tools/round-71/seam-probe.py",
         "tools/round-71/forged-receipts.py",
         "tools/round-71/registry-census.py",
         "tools/round-71/controls.py"]
LOADED = ["tools/round-51/census3.py",
          "tools/round-69/packed-elf.py",
          "tools/round-69/contract-probe.py",
          "tools/round-70/packed-elf.py",
          "tools/round-70/contract-probe.py",
          "tools/round-70/mutation-check.py"]
PLAN = "plans/round-71-claims.md"


def blob(root: str, rev: str, path: str) -> bytes:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(f"cannot read {rev}:{path}")
    return proc.stdout


def predicate(plan_text: str, claim: str) -> str:
    anchor = f"**Predicate (one sentence, frozen).** {claim} is verified iff"
    start = plan_text.find(anchor)
    if start < 0:
        raise SystemExit(f"predicate anchor absent: {claim}")
    end = plan_text.find("\n\n**Counting command.**", start)
    if end < 0:
        raise SystemExit(f"predicate end absent: {claim}")
    sentence = plan_text[start:end].split("**", 2)[-1].strip()
    sentence = re.sub(r"\s+", " ", sentence)
    return sentence


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--declaration", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    plan_text = blob(args.root, args.declaration, PLAN).decode("utf-8")
    instruments = {path: hashlib.sha256(
        blob(args.root, args.declaration, path)).hexdigest() for path in TOOLS}
    claims = [predicate(plan_text, c) for c in ("R71-C1", "R71-C2", "R71-C3")]
    container = {
        "schema": 1,
        "round": "round-71",
        "base": "82c8e620c9222fb218aa0260570a3765da2afb44",
        "claim_row": "S273",
        "declaration_pointer": (
            f"plans/round-71-claims.md (no amendments). The five instruments were "
            f"committed BEFORE this claims file (QUALITY #33): declaration "
            f"{args.declaration} (tools/round-71/*, the plan, the census-start "
            f"receipt). The pre receipts in .ufo/waves/round-71/l1/pre/ "
            f"(c1-at-base.json, c2-do-nothing.json, c3-at-base.json, "
            f"controls-at-declaration.json, nonce-commitment.txt) were measured "
            f"at that declaration state and committed before an…"),
        "instruments": instruments,
        "loaded_by_counter": {path: hashlib.sha256(
            blob(args.root, args.declaration, path)).hexdigest() for path in LOADED},
        "claims": claims,
        "frozen_atoms": {
            "A0": ("base 82c8e620c9222fb218aa0260570a3765da2afb44 (the round-70 lane "
                   "tip); declaration " + args.declaration + " (the five tools, this "
                   "plan, the census-start receipt); the order is base, then "
                   "instruments+plan, then the pre receipts, then this container "
                   "(QUALITY #33/#38)."),
            "A1": ("instrument pins above are the frozen bytes (tools/round-71/*); no "
                   "post-freeze edit of any pinned path without an appended "
                   "instrument_supersessions entry and a re-taken before record."),
            "A2": ("R71-C1: the route is tools/round-71/packed-elf.py; every child "
                   "(packer, REA node, readelf, git) runs under build_child_env(run_root); "
                   "--child-env-log records each child's observed /proc/self/environ via "
                   "the launcher (its PYTHONCOERCECLOCALE marker popped before the "
                   "observation and the exec); --challenge/--nonce-commitment bind "
                   "run_nonce and run_binding = sha256(nonce:instrument.sha256:packed "
                   "pins). The landing nonce plaintext lives only in scratch; its "
                   "sha256 is committed at l1/pre/nonce-commitment.txt BEFORE the "
                   "landing run."),
            "A3": ("R71-C2: the six lying-field shapes are cut from "
                   ".ufo/waves/round-70/l1/scores/c3-at-landing.json and relabelled to "
                   "the round-70 FIRST-CUT world: first-cut-rev "
                   "4737a542ae3b1b910d8fe43efbd572bc578b07c6 (the first-cut blob of "
                   "tools/round-70/packed-elf.py is the instrument.sha256 in every "
                   "shape), superseded-rev "
                   "7c155617bb42dadf1725b88a06fe3f235c364f0a. Declared clauses: "
                   "unpacked_counts, packed_sha256, section_count, runs.pack.argv, "
                   "refusal, format. The ten base-world shapes keep the round-70 "
                   "material (.ufo/waves/round-69/l1/scores/c3-at-landing.json) and "
                   "readers; the two landing-world identity shapes keep their probe "
                   "arms."),
            "A4": ("R71-C3: grammar v2 = split on unescaped pipes, unescape '\\|', "
                   "owner = last cell, write scope = second-last, pinned = the joined "
                   "middle cells; the four round-69 eight-cell rows are read by the "
                   "join rule and never rewritten; the six round-70 rows gain the "
                   "owner cell they omitted, disclosed old->new in LOG.md. Base state: "
                   "6 nonconformant rows, defects ['pinned-empty'], exit 1; round-51 "
                   "census3 exits 2."),
            "A5": ("pins reused from round 70: packer upx 5.2.0 sha256 "
                   "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969; "
                   "REA package 6.5.0 package.json sha256 "
                   "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c; "
                   "the four carriers and DECLARED_ORIG/DECLARED_PACKED are the "
                   "round-70 tables."),
            "A6": ("pre receipts (before any claim data, at the declaration): "
                   "l1/pre/c1-at-base.json (the round-71 probe at 7c155617 against the "
                   "round-70 route: arms_passed 7 of 10, A8/A9/A10 false), "
                   "c2-do-nothing.json (the round-70 battery receipt: 10 base-world + "
                   "2 landing-world rows, 0 lying-field rows), c3-at-base.json (88 "
                   "rows, 6 nonconformant, exit 1), controls-at-declaration.json (6 of "
                   "6), nonce-commitment.txt (the landing nonce's sha256)."),
            "A7": ("controls: c1-base-world, c1-constant-probe, c2-do-nothing, "
                   "c2-constant-battery, c3-base-nonconformant, c3-junk-row - all six "
                   "show what they must at the declaration (A6's "
                   "controls-at-declaration.json)."),
            "A8": ("the measured revision is the landing commit that carries this "
                   "round's files; every after-receipt names it; the report cites the "
                   "jj helper's landed hash."),
            "A9": ("repaired SKILL.md rows: only the six round-70 rows change (the "
                   "owner cell appended); the four round-69 rows stay byte-identical; "
                   "the census records the multicell rows by name."),
            "A10": ("repairs carried, not claim input: R71-G1 (round-70 capability "
                    "rows), R71-G2 (census W04 erratum), R71-G3 (the ca9817cf->ca9817cd "
                    "erratum), R71-G4 (wave-settlement receipt), R71-G5 (SOURCES "
                    "search log + tempfile rejection row), and the standing duties "
                    "re-run this round."),
        },
        "repairs": ["R71-G1", "R71-G2", "R71-G3", "R71-G4", "R71-G5"],
        "frontier": {
            "sources": ("corpus/SOURCES.md: S273 (GFM 4.10 cell-count tolerance, tier A "
                        "spec, opened this round) and S274 (the tempfile page, REJECTED: "
                        "it does not ground distinctness); S273 grounds R71-C3's grammar "
                        "addendum via corpus/knowledge/2026-11-04-r71-registry-grammar.md."),
            "mistake": "corpus/lessons/round-71.md ## Mistakes",
            "considerthese": "absent in this lane",
            "assimilation": "none (the merge/kaidoku/ package does not serve these claims)",
        },
    }
    with open(args.out, "w", encoding="utf-8") as fh:
        json.dump(container, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({"out": args.out, "instruments": len(instruments),
                      "claims": len(claims)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
