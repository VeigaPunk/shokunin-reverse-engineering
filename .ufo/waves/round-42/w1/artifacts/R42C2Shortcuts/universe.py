#!/usr/bin/env python3
"""universe.py -- build the A1 R42-C2 shortcut-analysis tuple universe.

Universe U = (1) the 52 committed round-41 held-out envelopes (tuples from
the frozen round-41 independent evaluator output, re-labelled by the A1 v4
transcription), (2) predicted legacy-family tuples built from the amended
draft (plans/round-42-claims.md `## R42-C2`) and unblob 26.6.4 handler
names, (3) predicted new named classes (container-depth-limited,
unknown-residue), (4) a widened combo factor space: every factor draw the A1
combo design can produce (>= 2 decision factors per draw).

Each universe member records: id, class, feature tuple (OP, PR, H, HF, G, D,
BE, SR, P), and the A1-expected (label, action, step) pair.
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from v4eval import classify  # noqa: E402

LEGACY_HANDLERS = [
    "squashfs_v1", "squashfs_v2", "squashfs_v3",
    "squashfs_v3_ddwrt", "squashfs_v3_broadcom",
]

CONTAINER_HANDLERS = ["trx_v1", "tar", "ubi"]


def tp(op, pr, h, g, d, be, sr, p, hf=None):
    if hf is None:
        # HF = handlers of the extractor-failure gaps; with no failure gap the
        # envelope carries none (observed on real REA envelopes)
        hf = list(h) if "extractor-failure" in g else []
    return {
        "OP": op, "PR": pr, "H": sorted(h), "HF": sorted(hf),
        "G": sorted(g), "D": sorted(d), "BE": be, "SR": sr, "P": p,
    }
    out = []
    for hand in LEGACY_HANDLERS:
        out.append(("legacy-clean[%s]" % hand, "legacy-clean",
                    tp("extract_firmware", "unblob", [hand], [], [], "n/a",
                       "no", 7)))
        out.append(("legacy-dep-missing[%s]" % hand, "legacy-dep-missing",
                    tp("extract_firmware", "unblob", [hand],
                       ["missing-extractor-dependency"], ["sasquatch"],
                       "n/a", "no", 0)))
        out.append(("legacy-zero-file[%s]" % hand, "legacy-zero-file",
                    tp("extract_firmware", "unblob", [hand], [], [], "n/a",
                       "no", 0)))
        for be, tag in (("yes", "be"), ("no", "le")):
            out.append(("legacy-partial[%s][%s]" % (hand, tag),
                        "legacy-partial",
                        tp("extract_firmware", "unblob", [hand],
                           ["extractor-failure"], [], be, "no", 5)))
            out.append(("legacy-body-failure[%s][%s]" % (hand, tag),
                        "legacy-body-failure",
                        tp("extract_firmware", "unblob", [hand],
                           ["extractor-failure"], [], be, "no", 0)))
    return out

def legacy_tuples():
    out = []
    for hand in LEGACY_HANDLERS:
        out.append(("legacy-clean[%s]" % hand, "legacy-clean",
                    tp("extract_firmware", "unblob", [hand], [], [], "n/a",
                       "no", 7)))
        out.append(("legacy-dep-missing[%s]" % hand, "legacy-dep-missing",
                    tp("extract_firmware", "unblob", [hand],
                       ["missing-extractor-dependency"], ["sasquatch"],
                       "n/a", "no", 0)))
        out.append(("legacy-zero-file[%s]" % hand, "legacy-zero-file",
                    tp("extract_firmware", "unblob", [hand], [], [], "n/a",
                       "no", 0)))
        for be, tag in (("yes", "be"), ("no", "le")):
            out.append(("legacy-partial[%s][%s]" % (hand, tag),
                        "legacy-partial",
                        tp("extract_firmware", "unblob", [hand],
                           ["extractor-failure"], [], be, "no", 5)))
            out.append(("legacy-body-failure[%s][%s]" % (hand, tag),
                        "legacy-body-failure",
                        tp("extract_firmware", "unblob", [hand],
                           ["extractor-failure"], [], be, "no", 0)))
    return out


def named_a1_tuples():
    out = []
    # container-depth-limited: a SquashFS chunk sits below the depth budget
    # inside a container: no squashfs handler at this depth, G has depth-limited
    for ch in CONTAINER_HANDLERS:
        for p, tag in ((0, "p0"), (3, "p3")):
            out.append(("container-depth-limited[%s][%s]" % (ch, tag),
                        "container-depth-limited",
                        tp("extract_firmware", "unblob", [ch],
                           ["depth-limited"], [], "n/a", "no", p)))
    # unknown-residue: unclaimed bytes beside a SquashFS chunk
    for fam in ("squashfs_v4_le", "squashfs_v3"):
        for extra in (["unknown-chunk-handler"],
                      ["unknown-chunk-handler", "depth-limited"]):
            out.append(("unknown-residue[%s][%s]"
                        % (fam, "+".join(extra)), "unknown-residue",
                        tp("extract_firmware", "unblob", [fam], extra, [],
                           "n/a", "no", 2)))
    return out


def combo_tuples():
    """Widened combo factor space (A1): >= 2 decision factors per draw.

    Factors: handler family, in-tree links, escaping links, damage (none /
    partial P>0 / zero-file P=0), dependency unreachable (single or both
    names), residue (unknown-chunk-handler), container wrap, max-depth,
    second v4 chunk (multi-H).
    """
    out = []
    fams = {"v4": ("squashfs_v4_le", "squashfs_v4_be"),
            "v3": ("squashfs_v3", "squashfs_v3"),
            "v1": ("squashfs_v1", "squashfs_v1")}
    seq = 0
    for fam, (le_h, be_h) in fams.items():
        for endian in ("le", "be"):
            h = le_h if endian == "le" else be_h
            for in_tree in (0, 1):
                for escaping in (0, 1):
                    for damage in ("none", "partial", "zeroid"):
                        for dep in ("none", "missing-le", "missing-be",
                                    "both"):
                            for residue in (0, 1):
                                for container in (0, 1):
                                    for depth in (1, 3):
                                        for second in (0, 1):
                                            if container and second:
                                                continue
                                            # dependency-realistic draws: v4
                                            # BE resolves sasquatch-v4be, v4
                                            # LE and every v1-v3 chunk resolve
                                            # plain sasquatch; 'both' is the
                                            # F1 probe (v4 BE only)
                                            if fam == "v4" and endian == "be":
                                                deps_ok = ("none", "missing-be",
                                                            "both")
                                            else:
                                                deps_ok = ("none",
                                                            "missing-le")
                                            if dep not in deps_ok:
                                                continue
                                            active = sum([
                                                damage != "none",
                                                dep != "none",
                                                residue == 1,
                                                container == 1,
                                                in_tree == 1,
                                                escaping == 1,
                                                depth == 1,
                                                second == 1,
                                                fam != "v4",
                                            ])
                                            if active < 2:
                                                continue
                                            gaps = set()
                                            deps = set()
                                            p = 5
                                            be = "n/a"
                                            handlers = [h]
                                            if second:
                                                handlers.append(
                                                    le_h if endian == "le"
                                                    else be_h)
                                            if container:
                                                # container wrap: replace the
                                                # squashfs handler with a
                                                # container handler at depth 1
                                                handlers = ["trx_v1"]
                                            if damage == "partial":
                                                gaps.add("extractor-failure")
                                                p = 5
                                                be = ("yes" if endian
                                                      == "be" else "no")
                                            elif damage == "zeroid":
                                                gaps.add("extractor-failure")
                                                p = 0
                                                be = ("yes" if endian
                                                      == "be" else "no")
                                            if dep != "none":
                                                gaps.add(
                                                    "missing-extractor-dependency")
                                                p = 0
                                                be = "n/a"
                                                if dep in ("missing-le",
                                                           "both"):
                                                    deps.add("sasquatch")
                                                if dep in ("missing-be",
                                                           "both"):
                                                    deps.add(
                                                        "sasquatch-v4be")
                                            if in_tree:
                                                gaps.add("unpublished-entry")
                                            if residue:
                                                gaps.add(
                                                    "unknown-chunk-handler")
                                            if depth == 1 and not container:
                                                gaps.add("depth-limited")
                                            elif container:
                                                gaps.add("depth-limited")
                                            feats = tp(
                                                "extract_firmware",
                                                "unblob", handlers, gaps,
                                                deps, be,
                                                "yes" if escaping else "no",
                                                p)
                                            seq += 1
                                            label = (
                                                "comboA1[%s/%s/in%d/es%d/"
                                                "dmg%s/dep%s/res%d/ctr%d/"
                                                "dp%d/2nd%d]"
                                                % (fam, endian, in_tree,
                                                   escaping, damage, dep,
                                                   residue, container, depth,
                                                   second))
                                            out.append((label, "combo",
                                                        feats))
    return out


def real_52():
    pairs = json.load(open(os.path.join(HERE, "heldout-v3-pairs.json")))
    out = []
    for cid, rec in sorted(pairs["labels"].items()):
        f = rec["features"]
        feats = tp(f["OP"], f["PR"], f["H"], f["G"], f["D"], f["BE"],
                   f["SR"], f["P"], f["HF"])
        out.append(("real:%s" % cid, "real-heldout", feats))
    return out

def dev_real():
    """The committed round-42 dev-arm envelopes (R42C2Gen artifacts):
    real feature tuples extracted from the actual envelope JSON blobs."""
    import gzip
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "E", "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
             "tools/round-41/indep-eval-v3.py")
    E = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(E)
    gen = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/" \
          "round-42/w1/artifacts/R42C2Gen/dev42-runs"
    out = []
    for d in sorted(os.listdir(gen)):
        p = os.path.join(gen, d, "envelope.json.gz")
        if not os.path.isfile(p):
            continue
        with gzip.open(p, "rt", encoding="utf-8") as fh:
            doc = json.load(fh)
        f = E.features(doc)
        feats = tp(f["OP"], f["PR"], f["H"], f["G"], f["D"], f["BE"],
                   f["SR"], f["P"], f["HF"])
        out.append(("dev:%s" % d, "dev-real", feats))
    return out


def main():
    members = []
    for cid, cls, feats in (real_52() + legacy_tuples()
                            + named_a1_tuples() + combo_tuples()
                            + dev_real()):
        pair, step = classify(feats)
        members.append({
            "id": cid, "class": cls, "features": feats,
            "expected": list(pair), "step": step,
        })
    out = os.environ.get("UNIVERSE_OUT") or os.path.join(
        os.environ.get("TMPDIR") or HERE, "universe-a1.json")
    with open(out, "w") as fh:
        json.dump({"universe": members, "amendment": "A1",
                   "note": "real-heldout: committed round-41 envelopes; "
                           "legacy-*/container-depth-limited/unknown-residue: "
                           "predicted named classes; combo: A1 widened factor "
                           "space (>=2 decision factors)"},
                  fh, indent=1, sort_keys=True)
    print("wrote %s (%d tuples)" % (out, len(members)))


if __name__ == "__main__":
    main()
