#!/usr/bin/env python3
"""checks.py - run the draft v3 block against committed envelopes and precedence-derived
combinations. Seat R41C2TableDraft, round 41 wave 1.

Not a scorer and not the round-41 counter: it answers three pre-freeze questions cheaply.

  A. does the draft block parse and decide the committed round-40 held-out envelopes
     exactly as the round-40 manifest labels them (26/26)?  Expected pairs come from
     `manifest.json:label_actions`, i.e. the round-40 data, not from this draft.
  B. what does v3 do to the four round-40 C1 AVM carriers, which v2 refused as
     `unclassified`?  Expected pair derived by hand from precedence clause 7.
  C. does the table reproduce the precedence text on combined gap sets?  Each synthetic
     envelope is a committed envelope with gap kinds added or files removed; the expected
     pair is written here by clause number, NOT computed from the table.

Every read is from the lane (read-only); nothing is written outside this artifacts dir.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REFPARSE = os.path.join(HERE, "v3-refparse.py")
HELDOUT = os.path.join(LANE, "corpus/evidence/round-40/c2/heldout")
C1 = os.path.join(LANE, "corpus/evidence/round-40/c1")
FIXTURE = os.path.join(HERE, "fixture-SKILL.md")
FIXTURE_EXACT = os.path.join(HERE, "fixture-SKILL-exact-only.md")
ACTIVE = [FIXTURE]
TAG = [""]


def _wrap(path, block):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("## Queue-drain craft\n\n" + block + "\n\n## Next section\n")
    return path


def exact_only(block):
    """The v2 set grammar in v3 shape: every `kind+` cell becomes the exact `kind`."""
    out = []
    for line in block.splitlines():
        if line.strip().startswith("|") and "---" not in line:
            cells = line.split("|")
            for index in (5, 6):
                if index >= len(cells):
                    continue
                value = cells[index].strip().strip("`").strip()
                if value.endswith("+") and value != "*":
                    cells[index] = " `%s` " % value[:-1]
            line = "|".join(cells)
        out.append(line)
    return "\n".join(out) + "\n"


def build_fixture():
    with open(os.path.join(HERE, "block20.md"), "r", encoding="utf-8") as handle:
        block = handle.read()
    _wrap(FIXTURE, block)
    _wrap(FIXTURE_EXACT, exact_only(block))
    return FIXTURE


def run(envelopes, out_json=None):
    cmd = [sys.executable, "-I", "-B", REFPARSE, "--skill", ACTIVE[0], "--json"] + envelopes
    proc = subprocess.run(cmd, capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit("refparse failed (%d): %s" % (proc.returncode, proc.stderr.strip()))
    rows = json.loads(proc.stdout)
    if out_json:
        with open(out_json, "w", encoding="utf-8") as handle:
            json.dump(rows, handle, indent=1, sort_keys=True)
            handle.write("\n")
    return rows


def load(path):
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_lines(path, lines):
    with open(path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n")


def part_a():
    manifest = load(os.path.join(HELDOUT, "manifest.json"))
    expected = {}
    for carrier in manifest["carriers"]:
        cid = carrier["id"]
        label = carrier.get("label")
        if label is None:
            label = carrier["class"] if not isinstance(carrier.get("class"), dict) else None
        expected[cid] = label
    pairs = manifest["label_actions"]
    paths = []
    for cid in sorted(expected):
        paths.append(os.path.join(HELDOUT, cid, "envelope.json"))
    rows = run(paths, os.path.join(HERE, TAG[0] + "a-heldout-26.json"))
    lines = ["id\tclass\tlabel\taction\trow\texpected_label\texpected_action\tagree"]
    agree = 0
    miss = []
    for row in rows:
        cid = os.path.basename(os.path.dirname(row["path"]))
        want_label = expected[cid]
        want_action = pairs[want_label]
        ok = (row["label"], row["action"]) == (want_label, want_action)
        agree += 1 if ok else 0
        if not ok:
            miss.append((cid, want_label, want_action, row["label"], row["action"], row["row"]))
        lines.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            cid, want_label, row["label"], row["action"], row["row"], want_label, want_action,
            "yes" if ok else "NO"))
    write_lines(os.path.join(HERE, TAG[0] + "a-heldout-26.tsv"), lines)
    return agree, len(rows), miss


def part_b():
    paths = []
    ids = []
    for cid in ("V1", "V2", "L1", "L2"):
        path = os.path.join(C1, cid, "after.json")
        if os.path.exists(path):
            paths.append(path)
            ids.append(cid)
    rows = run(paths, os.path.join(HERE, TAG[0] + "b-c1-4.json"))
    lines = ["carrier\tgap_kinds\thandler\tpublished\tlabel\taction\trow\tclause7_expected"]
    agree = 0
    detail = []
    for cid, row in zip(ids, rows):
        feat = row["features"]
        ok = (row["label"], row["action"]) == ("depth-limited-nested", "raise-depth")
        agree += 1 if ok else 0
        detail.append((cid, feat["G"], feat["H"], feat["P"], row["label"], row["action"], row["row"], ok))
        lines.append("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            cid, "+".join(feat["G"]), "+".join(feat["H"]), feat["P"], row["label"],
            row["action"], row["row"], "yes" if ok else "NO"))
    write_lines(os.path.join(HERE, TAG[0] + "b-c1-4.tsv"), lines)
    return agree, len(rows), detail


def mutate(base_env, gaps=(), files=None, deps=()):
    """Copy a committed envelope and add gap kinds / reset the file count."""
    env = json.loads(json.dumps(base_env))
    data = env.get("data", env)
    result = data["normalized_result"]
    for kind in gaps:
        result["extraction_gaps"].append({
            "kind": kind, "input_path": "$output/synthetic", "relative_path": None,
            "handler": None, "provider_id": None, "range": None, "root_file_range": None,
            "dependencies": list(deps),
        })
    if files is not None:
        result["files"] = [{"path": "synthetic-%d" % i} for i in range(files)]
    return env


def part_c():
    cases = []

    def add(name, clause, env, want):
        cases.append((name, clause, env, want))

    h01 = load(os.path.join(HELDOUT, "H01/envelope.json"))   # clean, G={}, SR=no, P=5
    h07 = load(os.path.join(HELDOUT, "H07/envelope.json"))   # escaping, G={}, SR=yes, P=3
    h09 = load(os.path.join(HELDOUT, "H09/envelope.json"))   # in-tree, G={unpublished-entry}, SR=no
    h11 = load(os.path.join(HELDOUT, "H11/envelope.json"))   # mixed, G={unpublished-entry}, SR=yes
    h13 = load(os.path.join(HELDOUT, "H13/envelope.json"))   # dep be, deps=[sasquatch-v4be]
    h15 = load(os.path.join(HELDOUT, "H15/envelope.json"))   # dep le, deps=[sasquatch]
    h19 = load(os.path.join(HELDOUT, "H19/envelope.json"))   # body failure, P=0, BE=yes
    h23 = load(os.path.join(HELDOUT, "H23/envelope.json"))   # no chunk

    add("partial + mixed symlinks", 4, mutate(h11, gaps=("extractor-failure",)),
        ("partial-body-failure", "salvage-partial"))
    add("partial + in-tree link", 4, mutate(h09, gaps=("extractor-failure",)),
        ("partial-body-failure", "salvage-partial"))
    add("partial + escaping link", 4, mutate(h07, gaps=("extractor-failure",)),
        ("partial-body-failure", "salvage-partial"))
    add("depth + mixed symlinks", 7, mutate(h11, gaps=("depth-limited",)),
        ("depth-limited-nested", "raise-depth"))
    add("depth + in-tree link", 7, mutate(h09, gaps=("depth-limited",)),
        ("depth-limited-nested", "raise-depth"))
    add("depth alone on a clean tree", 7, mutate(h01, gaps=("depth-limited",)),
        ("depth-limited-nested", "raise-depth"))
    add("depth beside a dep gap", 3, mutate(h13, gaps=("depth-limited",)),
        ("dep-missing-be", "install-extractor-be"))
    add("partial above depth", 4, mutate(h11, gaps=("extractor-failure", "depth-limited")),
        ("partial-body-failure", "salvage-partial"))
    add("body above depth", 6, mutate(h11, gaps=("extractor-failure", "depth-limited"), files=0),
        ("body-extractor-failure", "preserve-failure"))
    add("body + in-tree link", 6, mutate(h19, gaps=("unpublished-entry",)),
        ("body-extractor-failure", "preserve-failure"))
    add("dep + partial", 3, mutate(h15, gaps=("extractor-failure",), files=2),
        ("dep-missing-le", "install-extractor-le"))
    add("dep(be) + mixed symlink gaps", 3,
        mutate(h11, gaps=("missing-extractor-dependency",), deps=("sasquatch-v4be",)),
        ("dep-missing-be", "install-extractor-be"))
    add("unnamed dep falls through to mixed", 8,
        mutate(h11, gaps=("missing-extractor-dependency",)),
        ("mixed-symlinks", "audit-symlinks"))
    add("no chunk above depth", 2, mutate(h23, gaps=("depth-limited",)),
        ("no-squashfs-chunk", "inspect-input"))
    add("mixed (row order)", 8, mutate(h01, gaps=("unpublished-entry",)),
        ("in-tree-symlink-metadata", "count-gap"))
    add("unknown kind stays unclassified", 12, mutate(h01, gaps=("unknown-chunk-handler",)),
        ("unclassified", "none"))
    add("two in-tree gap kinds", 12,
        mutate(h09, gaps=("unknown-chunk-handler",)), ("unclassified", "none"))

    # H01 has SR=no; add a removal report for the mixed case.
    mixed = mutate(h01, gaps=("unpublished-entry",))
    (mixed.get("data") or mixed)["normalized_result"]["diagnostics"].append(
        {"report": {"__typename__": "MaliciousSymlinkRemoved", "link": "x", "target": "y"}})
    add("mixed: in-tree gaps + removal report", 8, mixed,
        ("mixed-symlinks", "audit-symlinks"))

    paths = []
    for index, (_, _, env, _) in enumerate(cases):
        path = os.path.join(HERE, "c-envelope-%02d.json" % index)
        with open(path, "w", encoding="utf-8") as handle:
            json.dump(env, handle, indent=1, sort_keys=True)
            handle.write("\n")
        paths.append(path)
    rows = run(paths, os.path.join(HERE, TAG[0] + "c-combined.json"))
    lines = ["case\tclause\tgap_kinds\tsr\tpublished\tlabel\taction\trow\texpected\tagree"]
    agree = 0
    miss = []
    for (name, clause, _, want), row in zip(cases, rows):
        feat = row["features"]
        ok = (row["label"], row["action"]) == want
        agree += 1 if ok else 0
        if not ok:
            miss.append((name, clause, want, row["label"], row["action"], row["row"]))
        lines.append("%s\t%d\t%s\t%s\t%s\t%s\t%s\t%s\t%s/%s\t%s" % (
            name, clause, "+".join(sorted(feat["G"])), feat["SR"], feat["P"], row["label"],
            row["action"], row["row"], want[0], want[1], "yes" if ok else "NO"))
    write_lines(os.path.join(HERE, TAG[0] + "c-combined.tsv"), lines)
    return agree, len(rows), miss


def main():
    build_fixture()
    ACTIVE[0] = FIXTURE
    TAG[0] = ""
    a_ok, a_n, a_miss = part_a()
    b_ok, b_n, b_detail = part_b()
    c_ok, c_n, c_miss = part_c()
    print("A held-out 26 : %d/%d" % (a_ok, a_n))
    print("B C1 carriers : %d/%d -> %s" % (b_ok, b_n, ", ".join(
        "%s:%s/%s(row %s)" % (d[0], d[4], d[5], d[6]) for d in b_detail)))
    print("C combined    : %d/%d" % (c_ok, c_n))
    for miss in a_miss:
        print("  A MISS %s want=%s/%s got=%s/%s row=%s" % miss)
    for miss in c_miss:
        print("  C MISS %s clause=%d want=%s/%s got=%s/%s row=%s" % (
            miss[0], miss[1], miss[2][0], miss[2][1], miss[3], miss[4], miss[5]))
    total_ok = a_ok + b_ok + c_ok
    total_n = a_n + b_n + c_n
    print("TOTAL %d/%d" % (total_ok, total_n))

    # Negative control: the same block with every `kind+` rewritten to an exact `kind`.
    # This is the v2 grammar in v3 shape; it must NOT reach the target, or the contains
    # form would be decorative.
    ACTIVE[0] = FIXTURE_EXACT
    TAG[0] = "ctl-exact-"
    for path in (FIXTURE_EXACT,):
        pass
    ca_ok, ca_n, _ = part_a()
    cb_ok, cb_n, _ = part_b()
    cc_ok, cc_n, cc_miss = part_c()
    print("")
    print("CONTROL exact-only (v2 set grammar):A %d/%d  B %d/%d  C %d/%d" % (
        ca_ok, ca_n, cb_ok, cb_n, cc_ok, cc_n))
    for miss in cc_miss:
        print("  CTL C MISS %s clause=%d want=%s/%s got=%s/%s row=%s" % (
            miss[0], miss[1], miss[2][0], miss[2][1], miss[3], miss[4], miss[5]))
    control_ok = (ca_ok, cb_ok, cc_ok)
    target_ok = total_ok == total_n
    return 0 if (target_ok and control_ok[2] < cc_n) else 1


if __name__ == "__main__":
    sys.exit(main())
