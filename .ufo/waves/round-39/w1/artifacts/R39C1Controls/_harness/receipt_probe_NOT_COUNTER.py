#!/usr/bin/env python3
"""REFERENCE RECEIPT PROBE - not the R39-C1 counter and never frozen.

This is the cheapest possible receipt-only implementation of the drafted
P39-C1 predicate, used by the control harness to demonstrate *which* control a
receipt-only counter accepts.  It deliberately has no live REA run, so CTL-C1-3
passes it.  The real round-39 counter belongs to L1 and must add whatever
binding the control report requires.

Usage: receipt_probe_NOT_COUNTER.py --root LANE --rev REV --freeze FREEZE \
         --pkg65 <REA650_PKG_ROOT> [--json-out PATH]
Exit 0 target met, 1 not met, 2 unevaluable.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

CARRIERS = ".ufo/waves/round-39/c1/carriers.json"
ENTRY = "corpus/knowledge/2026-10-26-r39-sasquatch-be-squashfs-promotion.md"
STEM = "2026-10-26-r39-sasquatch-be-squashfs-promotion"
CORE = "## Round-39 additions to Core"
HANDLER = "squashfs_v4_be"
XPIN = "tools/round-27/xpin-attribute.mjs"
OPENED = "2026-10-26"
TARGET = 6
PREFIX = "firmware.bin_extract"


class Unevaluable(Exception):
    pass


def git(root, *args, check=True):
    p = subprocess.run(["git", "-C", root, *args], capture_output=True)
    if check and p.returncode != 0:
        raise Unevaluable("git " + " ".join(args) + ": " + p.stderr.decode(errors="replace").strip())
    return p


def show(root, rev, path):
    p = git(root, "show", "%s:%s" % (rev, path), check=False)
    return p.stdout if p.returncode == 0 else None


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def section(text, heading):
    lines = text.splitlines()
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    out = []
    for line in lines[i + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return out


def tsv(raw):
    rows = []
    for line in (raw or b"").decode().splitlines():
        if not line.strip():
            continue
        rows.append(line.split("\t"))
    return rows


def evidence_ids(root, freeze, pkg65, envs, work):
    raw = show(root, freeze, XPIN)
    if raw is None:
        raise Unevaluable("xpin absent at freeze")
    tool = os.path.join(work, "xpin.mjs")
    open(tool, "wb").write(raw)
    order = sorted(envs)
    paths = []
    for name in order:
        p = os.path.join(work, name.replace("/", "_") + ".json")
        json.dump({"data": envs[name]}, open(p, "w"))
        paths.append(p)
    r = subprocess.run(["node", tool, "--pkg65", pkg65, "--pkg67", pkg65] + paths,
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise Unevaluable("xpin: " + r.stderr.strip())
    out = {}
    for name, line in zip(order, r.stdout.splitlines()):
        f = line.split("\t")
        out[name] = (f[1], f[2])
    return out


def first_add(root, path):
    p = git(root, "log", "--diff-filter=A", "--format=%H", "--", path, check=False)
    if p.returncode != 0:
        return None
    lines = [l for l in p.stdout.decode().splitlines() if l.strip()]
    return lines[-1] if lines else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--freeze", required=True)
    ap.add_argument("--pkg65", required=True)
    ap.add_argument("--json-out")
    a = ap.parse_args(argv)
    res = {"revision": a.rev, "freeze": a.freeze, "predicate": "P39-C1-refprobe",
           "target": TARGET}
    root = a.root
    git(root, "cat-file", "-e", a.rev + "^{commit}")
    git(root, "cat-file", "-e", a.freeze + "^{commit}")
    frozen_raw = show(root, a.freeze, CARRIERS)
    if frozen_raw is None:
        res["unevaluable"] = "carriers.json absent at freeze"
        print(json.dumps(res))
        return 2
    res["carriers_unchanged"] = show(root, a.rev, CARRIERS) == frozen_raw
    spec = json.loads(frozen_raw)
    work = tempfile.mkdtemp(prefix="probe.")
    envs = {}
    per = {}
    try:
        for c in spec["carriers"]:
            k = c["id"]
            d = {"id": k}
            o_f = show(root, a.freeze, c["oracle"])
            s_f = show(root, a.freeze, c["symlinks"]) if c.get("symlinks") else b""
            d["oracle_frozen"] = o_f is not None and o_f == show(root, a.rev, c["oracle"])
            d["symlinks_frozen"] = (show(root, a.rev, c["symlinks"]) if c.get("symlinks") else b"") == s_f
            oracle = [(r[0], r[1]) for r in tsv(o_f) if len(r) >= 2]
            links = [(r[0], r[1], r[2]) for r in tsv(s_f) if len(r) >= 3]
            d["oracle_files"] = len(oracle)
            raw = show(root, a.rev, "corpus/evidence/round-39/c1/%s/after.json" % k)
            try:
                env = json.loads(raw) if raw else None
            except json.JSONDecodeError:
                env = None
            d["after_present"] = isinstance(env, dict)
            if isinstance(env, dict):
                envs[k] = env
                nr = env.get("normalized_result") or {}
                d["after_subject_ok"] = ((env.get("subject") or {}).get("digest") or {}).get("sha256") == c["sha256"]
                chunks = [x for x in (nr.get("chunks") or []) if isinstance(x, dict)]
                d["after_handler_ok"] = any(x.get("handler") == HANDLER for x in chunks)
                d["after_no_failed_chunk"] = not any(x.get("extraction_failed") for x in chunks)
                files = [(f.get("relative_path") or "", f.get("sha256") or "")
                         for f in (nr.get("files") or [])]
                d["after_oracle_hits"] = sum(
                    1 for rel, sha in oracle
                    if any(sha == fs and (fp == rel or fp.endswith("/" + rel)) for fp, fs in files))
                actual = sorted((g.get("kind"), g.get("relative_path"))
                                for g in (nr.get("extraction_gaps") or []))
                expect = sorted(("unpublished-entry", PREFIX + "/" + r)
                                for r, t, kind in links if kind == "in-tree")
                d["gaps_expected"] = len(expect)
                d["gaps_actual"] = len(actual)
                d["after_gaps_exact"] = actual == expect
                add = first_add(root, "corpus/evidence/round-39/c1/%s/after.json" % k)
                d["first_add"] = add
                d["first_add_strict_descendant"] = bool(add) and add != a.freeze and (
                    git(root, "merge-base", "--is-ancestor", a.freeze, add, check=False).returncode == 0)
            per[k] = d
        ev = evidence_ids(root, a.freeze, a.pkg65, envs, work) if envs else {}
        n = 0
        for k, d in per.items():
            if k in envs:
                d["after_evidence_id_ok"] = (k in ev and ev[k][0] == ev[k][1]
                                             and ev[k][0].startswith("ev_"))
            ok = (d.get("oracle_frozen") and d.get("symlinks_frozen") and d["oracle_files"] > 0
                  and d.get("after_present") and d.get("after_subject_ok")
                  and d.get("after_handler_ok") and d.get("after_no_failed_chunk")
                  and d.get("after_gaps_exact")
                  and d.get("after_evidence_id_ok")
                  and d.get("first_add_strict_descendant")
                  and d.get("after_oracle_hits") == d["oracle_files"])
            d["matched"] = bool(ok)
            n += bool(ok)
        res["carrier_ids"] = [c["id"] for c in spec["carriers"]]
        res["carriers"] = per
        res["carriers_matched"] = n
    finally:
        shutil.rmtree(work, ignore_errors=True)

    b = {}
    prov = show(root, a.rev, "PROVINCE.md")
    sec = section(prov.decode(), CORE) if prov else None
    b["province_core_section"] = sec is not None
    rows = [l for l in (sec or []) if l.lstrip().startswith("|")]
    b["province_core_row"] = any(
        re.search(r"(?<![A-Za-z0-9-])squashfs_v4_be(?![A-Za-z0-9])", cells(r)[0])
        and ENTRY in r for r in rows)
    b["frontier_note"] = bool(prov) and any(
        "big-endian" in l and "superseded" in l for l in prov.decode().splitlines())
    ent = show(root, a.rev, ENTRY)
    b["entry_present"] = ent is not None
    src_ids = set()
    if ent:
        for line in ent.decode().splitlines():
            if line.startswith("source:"):
                src_ids |= set(re.findall(r"(?<![0-9A-Za-z])(S\d{3,})(?![0-9A-Za-z])", line))
    b["entry_source_ids"] = sorted(src_ids)
    reg = show(root, a.rev, "corpus/SOURCES.md")
    ok_ids = []
    if reg:
        for line in reg.decode().splitlines():
            if not re.match(r"^ {0,3}\|\s*S\d{3,}\s*\|", line):
                continue
            c = cells(line)
            if len(c) != 11:
                continue
            used = [u.strip() for u in c[10].split(",")]
            if c[0] in src_ids and c[8] == OPENED and ENTRY in used:
                ok_ids.append(c[0])
    b["opened_source_rows"] = sorted(ok_ids)
    b["sourced"] = bool(ok_ids)
    readme = show(root, a.rev, "corpus/README.md")
    cm = section(readme.decode(), "## Coverage map") if readme else None
    b["coverage_map_row"] = bool(cm) and any(
        STEM in l for l in cm if l.lstrip().startswith("|"))
    res["bindings"] = b
    bind_ok = all(b[x] for x in ("province_core_section", "province_core_row",
                                 "frontier_note", "entry_present", "sourced",
                                 "coverage_map_row"))
    res["met_target"] = bool(res["carriers_unchanged"] and res["carriers_matched"] == TARGET
                             and bind_ok)
    print(json.dumps({k: res.get(k) for k in
                      ("revision", "carriers_matched", "carriers_unchanged",
                       "bindings", "met_target")}, sort_keys=True))
    if a.json_out:
        json.dump(res, open(a.json_out, "w"), indent=1, sort_keys=True)
    return 0 if res["met_target"] else 1


if __name__ == "__main__":
    sys.exit(main())
