#!/usr/bin/env python3
"""mk-matrix.py — assemble the round-40 marker-boundary master TSV from retained runs.

Inputs (all under one scratch/artifact root):
  probe-matrix.tsv   (probe_sqfs.py output)
  sq-matrix.tsv      (direct sasquatch runs)
  ub/<tag>/unblob.log + ub/<tag>/out/   (direct unblob runs)
  rea-<tag>/envelope.json               (REA extract-firmware envelopes)
usage: mk-matrix.py ROOT TAG[,TAG...] > master.tsv
TAG is the image stem: <stem>.sqsh / <stem>.squashfs
"""
import hashlib
import json
import os
import sys

ROOT = sys.argv[1]
STEMS = sys.argv[2].split(",")


def find_image(stem):
    for ext in (".sqsh", ".squashfs"):
        p = os.path.join(ROOT, stem + ext)
        if os.path.exists(p):
            return p
    return None


def probe_rows():
    rows = {}
    with open(os.path.join(ROOT, "probe-matrix.tsv")) as f:
        head = f.readline().rstrip("\n").split("\t")
        for line in f:
            v = line.rstrip("\n").split("\t")
            d = dict(zip(head, v))
            rows[os.path.basename(d["path"])] = d
    return rows


def sq_rows():
    rows = {}
    with open(os.path.join(ROOT, "sq-matrix.tsv")) as f:
        for line in f:
            img, _ts, mode, ex, fi, *_ = line.rstrip("\n").split("\t")
            rows.setdefault(img, {})[mode] = "%s/%s" % (fi.split("=")[1], ex.split("=")[1])
    return rows


def ub_row(stem):
    tag = os.path.join(ROOT, "ub", stem)
    log = os.path.join(tag, "unblob.log")
    if not os.path.exists(log):
        return None
    txt = open(log, errors="replace").read()
    handlers = sorted({seg.split("=")[1] for seg in txt.split() if seg.startswith("handler=")})
    cmd = ""
    for tok in txt.split("command='")[1:]:
        cmd = tok.split("'")[0]
        break
    nfiles = nlinks = 0
    for base, _dirs, files in os.walk(os.path.join(tag, "out")):
        for f in files:
            p = os.path.join(base, f)
            if os.path.islink(p):
                nlinks += 1
            elif os.path.isfile(p):
                nfiles += 1
    return dict(handler=",".join(handlers), argv=cmd.replace(ROOT + "/", ""),
                be_absent="0" if " -be " in " %s " % cmd else "1",
                files=nfiles, links=nlinks, failrep=txt.count("ExtractCommandFailedReport"))


def rea_row(stem):
    p = os.path.join(ROOT, "rea-" + stem, "envelope.json")
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    nr = (d.get("data") or {}).get("normalized_result") or {}
    return dict(ok=d.get("ok"),
                op=(d.get("data") or {}).get("operation"),
                prov="%s@%s" % ((d.get("data") or {}).get("provider", {}).get("id"),
                                (d.get("data") or {}).get("provider", {}).get("version")),
                cov=nr.get("coverage"), files=len(nr.get("files") or []),
                P=nr.get("published_bytes"),
                gaps=",".join(sorted({g.get("kind") for g in (nr.get("extraction_gaps") or [])})) or "-",
                chunk_failed=",".join(sorted({str(c.get("extraction_failed")) for c in (nr.get("chunks") or [])})),
                subject=(d.get("data") or {}).get("subject", {}).get("digest", {}).get("sha256"))


COLS = ["image", "sha256", "size", "magic", "comp", "marker", "blocklen", "multiblock",
        "ub_handler", "ub_argv", "ub_be_absent", "ub_files", "ub_links", "ub_failrep",
        "sq_noflag", "sq_flag", "rea_ok", "rea_cov", "rea_files", "rea_P", "rea_gaps",
        "rea_chunk_failed", "rea_subject_eq_pin"]

pr = probe_rows()
sq = sq_rows()
print("\t".join(COLS))
for stem in STEMS:
    img = find_image(stem)
    name = os.path.basename(img)
    p = pr.get(name, {})
    u = ub_row(stem) or {}
    r = rea_row(stem) or {}
    pin = hashlib.sha256(open(img, "rb").read()).hexdigest()
    s = sq.get(name, {})
    print("\t".join(str(v) for v in [
        name, pin, p.get("size"), p.get("magic"), p.get("comp"), p.get("marker"),
        p.get("layout"), p.get("multiblock"),
        u.get("handler"), u.get("argv"), u.get("be_absent"), u.get("files"), u.get("links"), u.get("failrep"),
        s.get("noflag") or s.get("-le"), s.get("-be") or s.get("-le"),
        r.get("ok"), r.get("cov"), r.get("files"), r.get("P"), r.get("gaps"),
        r.get("chunk_failed"), (r.get("subject") == pin) if r.get("subject") else None,
    ]))
