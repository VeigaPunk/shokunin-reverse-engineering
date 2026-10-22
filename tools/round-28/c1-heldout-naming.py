#!/usr/bin/env python3
"""Round 28 R28-C1 counter: held-out test of the round-25 EVM selector naming rule.

Reads committed bytes at --rev only (git show); never touches the network or REA.
Every file the counter loads is pinned below by sha256 (routed defect 4 of the round-27
spot-check): the round-25 resolver it imports, and the frozen carrier and selector lists.

Counts, at --rev:
  runs_ok        carriers in corpus/evidence/round-28/c1/carriers.tsv with exactly one valid
                 call record in runs.tsv: exit 0, frozen argv, package version 6.5.0 and the
                 frozen package.json sha256, utc_start strictly after the counter's own commit,
                 envelope file first committed no earlier than the counter, envelope sha256 equal
                 to its bytes, operation inspect_evm_interface, provider evmole@0.9.3, subject
                 digest and local path equal to the carrier's runtime file.
  rows_complete  held-out selectors in heldout.tsv whose carrier run is valid and whose saved
                 lookups are complete: 4byte.directory pages p0.. and one openchain filter=false
                 response, each with a manifest entry (frozen URL, status 200, utc after the
                 counter commit, sha256 equal to the bytes), first committed no earlier than the
                 counter. Byte-identical response bodies for different selectors are legitimate
                 (an empty result is the same bytes for every unknown selector) and are never
                 refused: responses are keyed by their manifest entry, not by their bytes.
  tally_equal    1 when corpus/evidence/round-28/c1/tally.json equals the tally this counter
                 recomputes from the committed envelopes and responses.
  entry_ok       1 when the knowledge entry exists, opens with source:/verified-at:/recheck:,
                 names tally.json, states the primary rule's triple exactly as
                 "named N, right R, wrong W" with the recomputed values, and its source: line
                 cites an S### row that is new since --base, status mined, opened 2026-10-22 and
                 listed in corpus/lessons/round-28.md ## Gate.

Exit 0 only when runs_ok = 61/61, rows_complete = 187/187, tally_equal = 1 and entry_ok = 1.
Exit 1 otherwise; exit 2 when a pinned input is absent or differs from its pin.

Usage: c1-heldout-naming.py --root LANE --rev REV [--base BASE]
       c1-heldout-naming.py --root LANE --emit-tally   (recompute from the working tree; L1 use)
       c1-heldout-naming.py --selftest
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

LANE_ABS = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER_PATH = "tools/round-28/c1-heldout-naming.py"
RESOLVER = "tools/round-25/a2/resolve-selectors.py"
EVDIR = "corpus/evidence/round-28/c1"
ENTRY = "corpus/knowledge/2026-10-22-r28-evm-heldout-selector-naming.md"
SOURCES = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-28.md"
OPENED = "2026-10-22"
BASE = "935c36608008f79e3dea4f1ed191df3c89e3b848"
PKG_VERSION = "6.5.0"
PKG_JSON_SHA = "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c"
ARGV = "npx -y rea-agents@6.5.0 inspect-evm-interface %s/%s hex --format json"
RUNS_HEADER = ["carrier", "utc_start", "exit", "argv", "pkg_version", "pkg_json_sha256", "envelope", "envelope_sha256"]
PINS = {
    RESOLVER: "4be915668ea20a643d04c9b8ae3c83bc9f5fd1b4d8821e06cabdccce36b3c23d",
    EVDIR + "/carriers.tsv": "4392b5c377cc2e343d385ba3b93206a0bb67df972bdc3814780819f1d4c5e71f",
    EVDIR + "/heldout.tsv": "423654f9d71feb417725a1e5a290b1e028ee53ad628141281a8c08391dab6cef",
}
TARGET = {"runs": 61, "rows": 187}
PRIMARY = "openchain_sole_unfiltered_args_consistent"
RULES = {
    "fourbyte_first": "first 4byte.directory result (API default order)",
    "fourbyte_sole_args_consistent": "the only 4byte candidate whose keccak and parameter list match REA",
    "openchain_first": "first openchain result (filter=false response order)",
    "openchain_sole_unfiltered": "the only openchain candidate with filtered=false",
    "openchain_sole_unfiltered_args_consistent": "the only openchain candidate with filtered=false whose parameter list matches REA",
}


class PinError(Exception):
    pass


def show(root, rev, path):
    if rev is None:
        p = os.path.join(root, path)
        return open(p, "rb").read() if os.path.exists(p) else None
    proc = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)], capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def ls(root, rev, path):
    if rev is None:
        d = os.path.join(root, path)
        return sorted(os.listdir(d)) if os.path.isdir(d) else []
    proc = subprocess.run(["git", "-C", root, "ls-tree", "--name-only", "%s:%s" % (rev, path)], capture_output=True, text=True)
    return sorted(proc.stdout.split()) if proc.returncode == 0 else []


def first_commit_time(root, rev, path):
    if rev is None:
        return None
    out = subprocess.run(["git", "-C", root, "log", "--diff-filter=A", "--format=%ct", rev, "--", path],
                         capture_output=True, text=True).stdout.split()
    return int(out[-1]) if out else None


def parse_utc(text):
    try:
        return int(datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())
    except (TypeError, ValueError):
        return None


def pinned(root, rev, path):
    raw = show(root, rev, path)
    if raw is None:
        raise PinError("pinned input absent: %s" % path)
    if hashlib.sha256(raw).hexdigest() != PINS[path]:
        raise PinError("pinned input differs from its pin: %s" % path)
    return raw


def load_resolver(root, rev):
    src = pinned(root, rev, RESOLVER)
    ns = {"__name__": "resolver"}
    exec(compile(src, RESOLVER, "exec"), ns)
    return ns


def tsv(raw, header):
    lines = [l for l in raw.decode("utf-8").split("\n") if l]
    if not lines or lines[0].split("\t") != header:
        return None
    return [dict(zip(header, l.split("\t"))) for l in lines[1:]]


def rule_outputs(row):
    """Same rule definitions as tools/round-25/a3/tally-resolution.py (round 25), unchanged."""
    out = {}
    fb = row["databases"].get("4byte")
    oc = row["databases"].get("openchain")
    fbd = fb["detail"] if fb else []
    ocd = oc["detail"] if oc else []
    out["fourbyte_first"] = fbd[0]["text"] if fbd else None
    c = [x["text"] for x in fbd if x["label"] == "consistent"]
    out["fourbyte_sole_args_consistent"] = c[0] if len(c) == 1 else None
    out["openchain_first"] = ocd[0]["text"] if ocd else None
    u = [x for x in ocd if x.get("filtered") is False]
    out["openchain_sole_unfiltered"] = u[0]["text"] if len(u) == 1 else None
    ua = [x["text"] for x in u if x["label"] == "consistent"]
    out["openchain_sole_unfiltered_args_consistent"] = ua[0] if len(ua) == 1 else None
    return out


def check_runs(root, rev, carriers, counter_time):
    raw = show(root, rev, EVDIR + "/runs.tsv")
    runs = tsv(raw, RUNS_HEADER) if raw is not None else None
    ok, envs, reasons = {}, {}, []
    if runs is None:
        return ok, envs, ["runs.tsv absent or header differs"]
    by = {}
    for r in runs:
        by.setdefault(r["carrier"], []).append(r)
    for c in carriers:
        name = c["carrier"]
        rs_ = by.get(name, [])
        if len(rs_) != 1:
            reasons.append("%s: %d call records (need exactly 1)" % (name, len(rs_)))
            continue
        r = rs_[0]
        why = []
        if r["exit"] != "0":
            why.append("exit %s" % r["exit"])
        if r["argv"] != ARGV % (LANE_ABS, c["runtime"]):
            why.append("argv differs")
        if r["pkg_version"] != PKG_VERSION or r["pkg_json_sha256"] != PKG_JSON_SHA:
            why.append("package pin differs")
        t = parse_utc(r["utc_start"])
        if t is None or counter_time is None or t <= counter_time:
            why.append("utc_start %s not after counter commit" % r["utc_start"])
        epath = EVDIR + "/envelopes/" + r["envelope"]
        eraw = show(root, rev, epath)
        if eraw is None or "/" in r["envelope"]:
            why.append("envelope absent")
        else:
            if hashlib.sha256(eraw).hexdigest() != r["envelope_sha256"]:
                why.append("envelope sha256 differs from bytes")
            added = first_commit_time(root, rev, epath)
            if rev is not None and (added is None or counter_time is None or added < counter_time):
                why.append("envelope first committed before the counter")
            try:
                env = json.loads(eraw)
                if env.get("operation") != "inspect_evm_interface":
                    why.append("operation differs")
                if (env.get("provider") or {}).get("version") != "evmole@0.9.3":
                    why.append("provider version differs")
                subj = env.get("subject") or {}
                if (subj.get("digest") or {}).get("sha256") != c["runtime_sha256"]:
                    why.append("subject digest is not the carrier")
                if subj.get("local_path") != "%s/%s" % (LANE_ABS, c["runtime"]):
                    why.append("subject path is not the carrier")
                fns = env["normalized_result"]["functions"]
            except (ValueError, KeyError, TypeError, AttributeError):
                why.append("envelope does not parse as an REA EVM envelope")
                fns = None
        if why:
            reasons.append("%s: %s" % (name, "; ".join(why)))
            continue
        ok[name] = True
        envs[name] = {fn["selector"].lower().removeprefix("0x"): fn.get("inferred_arguments") for fn in fns}
    return ok, envs, reasons


def check_lookups(root, rev, sel, manifest, counter_time):
    why = []
    files = []
    page = 0
    names = set(ls(root, rev, EVDIR + "/db"))
    while "4byte-%s-p%d.json" % (sel, page) in names:
        files.append(("4byte-%s-p%d.json" % (sel, page), None))
        page += 1
    if page == 0:
        why.append("no 4byte page")
    files.append(("openchain-%s.json" % sel,
                  "https://api.openchain.xyz/signature-database/v1/lookup?function=0x%s&filter=false" % sel))
    for i, (fname, url) in enumerate(files):
        if url is None and i == 0:
            url = "https://www.4byte.directory/api/v1/signatures/?hex_signature=0x%s" % sel
        m = manifest.get(fname)
        raw = show(root, rev, EVDIR + "/db/" + fname)
        if m is None or raw is None:
            why.append("%s missing (file or manifest entry)" % fname)
            continue
        if url is not None and m.get("url") != url:
            why.append("%s url differs" % fname)
        if m.get("status") != 200:
            why.append("%s status %r" % (fname, m.get("status")))
        t = parse_utc(m.get("utc"))
        if t is None or counter_time is None or t <= counter_time:
            why.append("%s fetched before the counter commit" % fname)
        if hashlib.sha256(raw).hexdigest() != m.get("sha256"):
            why.append("%s sha256 differs from bytes" % fname)
        added = first_commit_time(root, rev, EVDIR + "/db/" + fname)
        if rev is not None and (added is None or counter_time is None or added < counter_time):
            why.append("%s first committed before the counter" % fname)
    return why


def recompute(root, rev, rs, heldout, envs):
    tmp = tempfile.mkdtemp(prefix="r28c1-")
    try:
        for fname in ls(root, rev, EVDIR + "/db"):
            if fname.endswith(".json") and fname != "manifest.json":
                with open(os.path.join(tmp, fname), "wb") as f:
                    f.write(show(root, rev, EVDIR + "/db/" + fname))
        rows = []
        for h in heldout:
            sel, truth = h["selector"], h["abi_signature"]
            fns = envs.get(h["carrier"], {})
            recovered = sel in fns
            inferred = fns.get(sel)
            fb, oc = rs["_load_candidates"](tmp, sel)
            row = {"selector": sel, "abi_signature": truth, "carrier": h["carrier"], "recovered_by_rea": recovered,
                   "inferred_arguments": inferred, "databases": {}}
            for db, cands in (("4byte", fb), ("openchain", oc)):
                if cands is None:
                    row["databases"][db] = None
                    continue
                for cand in cands:
                    cand["label"] = rs["_label"](cand["text"], sel, inferred)
                row["databases"][db] = {"candidates": len(cands),
                                        "truth_present": truth in [x["text"] for x in cands],
                                        "detail": cands}
            outs = rule_outputs(row) if recovered else {k: None for k in RULES}
            row["rule_outputs"] = outs
            rows.append(row)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    t = {"selector_rows": len(rows), "recovered_by_rea": sum(r["recovered_by_rea"] for r in rows),
         "args_match_abi": sum(1 for r in rows if r["recovered_by_rea"] and r["inferred_arguments"] is not None
                               and r["inferred_arguments"].replace(" ", "") == rs["params_of"](r["abi_signature"])),
         "no_candidate_in_either_database": sum(1 for r in rows if not any(
             r["databases"].get(db) and r["databases"][db]["candidates"] for db in ("4byte", "openchain"))),
         "truth_in_some_database": sum(1 for r in rows if any(
             r["databases"].get(db) and r["databases"][db]["truth_present"] for db in ("4byte", "openchain"))),
         "primary_rule": PRIMARY, "rules": {}}
    for k, desc in RULES.items():
        named = sum(1 for r in rows if r["rule_outputs"][k] is not None)
        right = sum(1 for r in rows if r["rule_outputs"][k] is not None and r["rule_outputs"][k] == r["abi_signature"])
        t["rules"][k] = {"rule": desc, "named": named, "right": right, "wrong": named - right, "no_name": len(rows) - named}
    wrong = [{"selector": r["selector"], "carrier": r["carrier"], "rule": k, "returned": v, "abi": r["abi_signature"]}
             for r in rows for k, v in r["rule_outputs"].items() if v is not None and v != r["abi_signature"]]
    return {"tally": t, "wrong_names": wrong,
            "rows": [{k: r[k] for k in ("selector", "abi_signature", "carrier", "recovered_by_rea", "inferred_arguments", "rule_outputs")}
                     for r in rows]}


def sources_rows(text):
    rows = {}
    for line in text.split("\n"):
        m = re.match(r"^\| (S\d{3}) \|", line)
        if m:
            rows[m.group(1)] = [c.strip() for c in line.strip().strip("|").split("|")]
    return rows


def gate_ids(text):
    ids, inside = set(), False
    for line in text.split("\n"):
        if line.startswith("## "):
            inside = line.strip() == "## Gate"
            continue
        if inside:
            ids |= set(re.findall(r"\bS\d{3}\b", line))
    return ids


def check_entry(root, rev, base, tally):
    raw = show(root, rev, ENTRY)
    if raw is None:
        return ["entry absent"]
    text = raw.decode("utf-8")
    lines = text.split("\n")
    why = []
    if not (len(lines) >= 3 and lines[0].startswith("source:") and lines[1].startswith("verified-at:")
            and lines[2].startswith("recheck:")):
        why.append("entry does not open with source:/verified-at:/recheck:")
    if EVDIR + "/tally.json" not in text:
        why.append("entry does not name tally.json")
    p = tally["rules"][PRIMARY]
    triple = "named %d, right %d, wrong %d" % (p["named"], p["right"], p["wrong"])
    if triple not in text:
        why.append("entry does not state the primary triple '%s'" % triple)
    src = show(root, rev, SOURCES)
    les = show(root, rev, LESSON)
    bsrc = show(root, base, SOURCES) if base else None
    if src is None or les is None:
        return why + ["SOURCES.md or round-28 lesson absent"]
    rows = sources_rows(src.decode("utf-8"))
    brows = sources_rows(bsrc.decode("utf-8")) if bsrc else {}
    gates = gate_ids(les.decode("utf-8"))
    good = [s for s in sorted(set(re.findall(r"\bS\d{3}\b", lines[0])))
            if s in rows and s not in brows and len(rows[s]) >= 11 and rows[s][7] == "mined"
            and rows[s][8] == OPENED and s in gates]
    if not good:
        why.append("source: line names no S### new since base, mined, opened %s and in ## Gate" % OPENED)
    return why


def count(root, rev, base):
    rs = load_resolver(root, rev)
    carriers = tsv(pinned(root, rev, EVDIR + "/carriers.tsv"),
                   ["carrier", "runtime", "abi", "runtime_sha256", "abi_sha256"])
    heldout = tsv(pinned(root, rev, EVDIR + "/heldout.tsv"), ["selector", "abi_signature", "carrier"])
    counter_time = first_commit_time(root, rev, COUNTER_PATH) if rev is not None else 0
    ok, envs, reasons = check_runs(root, rev, carriers, counter_time)
    mraw = show(root, rev, EVDIR + "/db/manifest.json")
    try:
        manifest = {m["file"]: m for m in json.loads(mraw)} if mraw is not None else {}
    except (ValueError, KeyError, TypeError):
        manifest = {}
        reasons.append("manifest.json does not parse")
    complete = 0
    for h in heldout:
        why = [] if ok.get(h["carrier"]) else ["carrier %s run not valid" % h["carrier"]]
        why += check_lookups(root, rev, h["selector"], manifest, counter_time)
        if why:
            reasons.append("row %s: %s" % (h["selector"], "; ".join(why)))
        else:
            complete += 1
    result = recompute(root, rev, rs, heldout, envs)
    committed = show(root, rev, EVDIR + "/tally.json")
    tally_equal = 0
    try:
        tally_equal = int(committed is not None and json.loads(committed) == result)
    except ValueError:
        pass
    if not tally_equal:
        reasons.append("tally.json absent or differs from the recompute")
    ereasons = check_entry(root, rev, base, result["tally"])
    reasons += ereasons
    return {"runs_ok": len(ok), "runs_total": len(carriers), "rows_complete": complete, "rows_total": len(heldout),
            "tally_equal": tally_equal, "entry_ok": int(not ereasons)}, reasons, result


def main_count(root, rev, base, out=sys.stdout):
    try:
        c, reasons, result = count(root, rev, base)
    except PinError as e:
        print("PIN %s" % e, file=out)
        return 2
    for r in reasons:
        print("FAIL %s" % r, file=out)
    p = result["tally"]["rules"][PRIMARY]
    print("primary rule %s: named %d, right %d, wrong %d, no_name %d" % (PRIMARY, p["named"], p["right"], p["wrong"], p["no_name"]), file=out)
    print("runs_ok=%d/%d rows_complete=%d/%d tally_equal=%d entry_ok=%d" % (
        c["runs_ok"], c["runs_total"], c["rows_complete"], c["rows_total"], c["tally_equal"], c["entry_ok"]), file=out)
    full = (c["runs_ok"] == c["runs_total"] == TARGET["runs"] and c["rows_complete"] == c["rows_total"] == TARGET["rows"]
            and c["tally_equal"] == 1 and c["entry_ok"] == 1)
    return 0 if full else 1


# ---------------------------------------------------------------- selftest

def _git(repo, *args, when=None):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    if when:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True, env=env).stdout.strip()


def _w(repo, rel, data):
    p = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def _commit(repo, when, msg):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "--allow-empty", "-m", msg, when=when)
    return _git(repo, "rev-parse", "HEAD")


def _fixture(repo, resolver_src, counter_src, mutate=None):
    """Two carriers, three held-out selectors; returns (base, rev)."""
    global TARGET
    _git(repo, "init", "-q")
    src_hdr = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
    old = "| S001 | old | code | A | s | a | t | mined | 2026-10-21 | on-release | x |\n"
    _w(repo, SOURCES, "# SOURCES\n\n" + src_hdr + old)
    base = _commit(repo, "2026-10-22T10:00:00Z", "base")
    _w(repo, RESOLVER, resolver_src)
    _w(repo, COUNTER_PATH, counter_src)
    rt = {"k1": "6080604052", "k2": "6080604053"}
    sha = {k: hashlib.sha256(v.encode()).hexdigest() for k, v in rt.items()}
    for k, v in rt.items():
        _w(repo, "carriers/%s.runtime.hex" % k, v)
    car = "carrier\truntime\tabi\truntime_sha256\tabi_sha256\n" + "".join(
        "%s\tcarriers/%s.runtime.hex\tcarriers/%s.abi.json\t%s\tx\n" % (k, k, k, sha[k]) for k in rt)
    ns = {"__name__": "resolver"}
    exec(compile(resolver_src, RESOLVER, "exec"), ns)
    s1, s2, s3 = ns["selector_of"]("ping()"), ns["selector_of"]("pong(uint256)"), ns["selector_of"]("zip(address)")
    # s3's ABI truth is planted as zap(address): the database's keccak-correct zip(address) must count wrong
    sels = [(s1, "ping()", "k1"), (s2, "pong(uint256)", "k1"), (s3, "zap(address)", "k2")]
    held = "selector\tabi_signature\tcarrier\n" + "".join("%s\t%s\t%s\n" % s for s in sels)
    _w(repo, EVDIR + "/carriers.tsv", car)
    _w(repo, EVDIR + "/heldout.tsv", held)
    PINS[EVDIR + "/carriers.tsv"] = hashlib.sha256(car.encode()).hexdigest()
    PINS[EVDIR + "/heldout.tsv"] = hashlib.sha256(held.encode()).hexdigest()
    _commit(repo, "2026-10-22T11:00:00Z", "counter")
    state = {"runs": {}, "env": {}, "db": {}, "manifest": [], "entry": None, "sources": SOURCES, "gate": True}
    fns = {"k1": [("0x" + s1, ""), ("0x" + s2, "uint256")], "k2": [("0x" + s3, "address")]}
    for i, k in enumerate(rt):
        env = {"evidence_id": "ev_%d" % i, "operation": "inspect_evm_interface",
               "provider": {"version": "evmole@0.9.3"},
               "subject": {"digest": {"sha256": sha[k]}, "local_path": "%s/carriers/%s.runtime.hex" % (LANE_ABS, k)},
               "normalized_result": {"functions": [{"selector": s, "inferred_arguments": a} for s, a in fns[k]]}}
        state["env"][k] = json.dumps(env).encode()
        state["runs"][k] = {"carrier": k, "utc_start": "2026-10-22T11:30:0%dZ" % i, "exit": "0",
                            "argv": ARGV % (LANE_ABS, "carriers/%s.runtime.hex" % k), "pkg_version": PKG_VERSION,
                            "pkg_json_sha256": PKG_JSON_SHA, "envelope": "%s.json" % k}
    empty4 = b'{"count":0,"next":null,"previous":null,"results":[]}'
    answers = {s1: ("ping()", False), s2: ("pong(uint256)", False), s3: ("zip(address)", False)}
    for s, _t, _c in sels:
        state["db"]["4byte-%s-p0.json" % s] = empty4  # byte-identical bodies across selectors: legitimate
        name, filt = answers[s]
        state["db"]["openchain-%s.json" % s] = json.dumps(
            {"ok": True, "result": {"function": {"0x" + s: [{"name": name, "filtered": filt}]}}}).encode()
    if mutate:
        mutate(state)
    for k, env in state["env"].items():
        _w(repo, EVDIR + "/envelopes/%s.json" % k, env)
    runs = "\t".join(RUNS_HEADER) + "\n"
    for k, r in state["runs"].items():
        r = dict(r)
        r.setdefault("envelope_sha256", hashlib.sha256(state["env"].get(k, b"")).hexdigest())
        runs += "\t".join(r[h] for h in RUNS_HEADER) + "\n"
    _w(repo, EVDIR + "/runs.tsv", runs)
    man = []
    for fname, body in state["db"].items():
        s = fname.split("-")[1].split(".")[0]
        url = ("https://api.openchain.xyz/signature-database/v1/lookup?function=0x%s&filter=false" % s
               if fname.startswith("openchain") else "https://www.4byte.directory/api/v1/signatures/?hex_signature=0x%s" % s)
        man.append({"file": fname, "url": url, "status": 200, "utc": "2026-10-22T11:40:00Z",
                    "sha256": hashlib.sha256(body).hexdigest()})
        _w(repo, EVDIR + "/db/" + fname, body)
    for m in state["manifest"]:
        m(man)
    _w(repo, EVDIR + "/db/manifest.json", json.dumps(man, indent=1))
    # tally from the working tree, then entry and source row
    saved = dict(TARGET)
    rs = load_resolver(repo, None)
    _ok, envs, _r = check_runs(repo, None, tsv(car.encode(), ["carrier", "runtime", "abi", "runtime_sha256", "abi_sha256"]), 0)
    result = recompute(repo, None, rs, tsv(held.encode(), ["selector", "abi_signature", "carrier"]), envs)
    if state.get("tally_mut"):
        state["tally_mut"](result)
    _w(repo, EVDIR + "/tally.json", json.dumps(result, indent=1))
    TARGET.update(saved)
    p = result["tally"]["rules"][PRIMARY]
    triple = "named %d, right %d, wrong %d" % (p["named"], p["right"], p["wrong"])
    sid = state.get("cite", "S002")
    entry = state["entry"] or ("source: %s\nverified-at: x\nrecheck: y\n\nprimary %s; %s/tally.json\n" % (sid, triple, EVDIR))
    _w(repo, ENTRY, entry)
    _w(repo, SOURCES, "# SOURCES\n\n" + src_hdr + old + "| S002 | new | code | A | s | a | t | %s | 2026-10-22 | on-release | x |\n"
       % state.get("status", "mined"))
    _w(repo, LESSON, "# r28\n\n## Gate\n\n%s\n\n## Mistakes\n\nS002 elsewhere\n" % ("| S002 | admit |" if state["gate"] else "none"))
    rev = _commit(repo, "2026-10-22T12:00:00Z", "data")
    return base, rev


def selftest():
    here = os.path.abspath(__file__)
    root = os.path.dirname(os.path.dirname(os.path.dirname(here)))
    resolver_src = open(os.path.join(root, RESOLVER), "rb").read()
    counter_src = open(here, "rb").read()
    saved_pins, saved_target = dict(PINS), dict(TARGET)

    def run_field(k, field, value):
        def f(st):
            st["runs"][k][field] = value
        return f

    def env_edit(k, fn):
        def f(st):
            d = json.loads(st["env"][k])
            fn(d)
            st["env"][k] = json.dumps(d).encode()
        return f

    cases = [
        ("green-identical-4byte-bodies-across-selectors", None, 0),
        ("red-early-run", run_field("k1", "utc_start", "2026-10-22T10:59:59Z"), 1),
        ("red-pkg-sha", run_field("k1", "pkg_json_sha256", "0" * 64), 1),
        ("red-pkg-version", run_field("k2", "pkg_version", "6.7.0"), 1),
        ("red-argv", run_field("k2", "argv", "npx -y rea-agents@6.7.0 inspect-evm-interface x hex --format json"), 1),
        ("red-exit", run_field("k1", "exit", "1"), 1),
        ("red-envelope-of-other-carrier", lambda st: st["env"].__setitem__("k2", st["env"]["k1"]), 1),
        ("red-provider", env_edit("k1", lambda d: d["provider"].__setitem__("version", "evmole@0.9.4")), 1),
        ("red-envelope-sha", run_field("k1", "envelope_sha256", "f" * 64), 1),
        ("red-missing-openchain", lambda st: st["db"].pop(sorted(k for k in st["db"] if k.startswith("openchain"))[-1]), 1),
        ("red-lookup-status", lambda st: st["manifest"].append(lambda man: man[0].__setitem__("status", 404)), 1),
        ("red-lookup-early", lambda st: st["manifest"].append(lambda man: man[1].__setitem__("utc", "2026-10-22T10:00:00Z")), 1),
        ("red-lookup-sha", lambda st: st["manifest"].append(lambda man: man[1].__setitem__("sha256", "0" * 64)), 1),
        ("red-lookup-url", lambda st: st["manifest"].append(lambda man: man[1].__setitem__("url", "https://example.org/x")), 1),
        ("red-tally-edited", lambda st: st.__setitem__("tally_mut", lambda r: r["tally"]["rules"][PRIMARY].__setitem__("wrong", 0)), 1),
        ("red-entry-wrong-triple", lambda st: st.__setitem__("entry", "source: S002\nverified-at: x\nrecheck: y\n%s/tally.json named 9, right 9, wrong 0\n" % EVDIR), 1),
        ("red-entry-old-row", lambda st: st.__setitem__("cite", "S001"), 1),
        ("red-row-not-in-gate", lambda st: st.__setitem__("gate", False), 1),
        ("red-row-status", lambda st: st.__setitem__("status", "candidate"), 1),
    ]
    fails = 0
    for name, mutate, want in cases:
        PINS.clear(); PINS.update(saved_pins); TARGET.clear(); TARGET.update({"runs": 2, "rows": 3})
        tmp = tempfile.mkdtemp(prefix="r28c1-st-")
        try:
            base, rev = _fixture(tmp, resolver_src, counter_src, mutate)
            PINS[RESOLVER] = hashlib.sha256(resolver_src).hexdigest()
            buf = _Buf()
            got = main_count(tmp, rev, base, out=buf)
            if name.startswith("green"):
                fx = buf.text
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        status = "ok" if got == want else "FAIL"
        fails += got != want
        print("%s %s exit=%d want=%d" % (status, name, got, want))
    # the wrong count is real on the green fixture: bbbb0001 is named zip(address), ABI says zap(address)
    if "wrong 1" not in fx:
        print("FAIL green fixture did not count the planted wrong name")
        fails += 1
    # pin refusal: the shipped pins must refuse a tampered carrier list
    PINS.clear(); PINS.update(saved_pins); TARGET.clear(); TARGET.update(saved_target)
    tmp = tempfile.mkdtemp(prefix="r28c1-st-")
    try:
        base, rev = _fixture(tmp, resolver_src, counter_src)
        PINS.clear(); PINS.update(saved_pins)
        got = main_count(tmp, rev, base, out=_Buf())
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    print("%s red-pin-refusal exit=%d want=2" % ("ok" if got == 2 else "FAIL", got))
    fails += got != 2
    PINS.clear(); PINS.update(saved_pins); TARGET.clear(); TARGET.update(saved_target)
    print("selftest cases=%d failures=%d" % (len(cases) + 2, fails))
    return 0 if fails == 0 else 1


class _Buf:
    def __init__(self):
        self.text = ""

    def write(self, s):
        self.text += s

    def flush(self):
        pass


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--emit-tally", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.emit_tally:
        root = os.path.abspath(a.root)
        rs = load_resolver(root, None)
        carriers = tsv(pinned(root, None, EVDIR + "/carriers.tsv"), ["carrier", "runtime", "abi", "runtime_sha256", "abi_sha256"])
        heldout = tsv(pinned(root, None, EVDIR + "/heldout.tsv"), ["selector", "abi_signature", "carrier"])
        _ok, envs, reasons = check_runs(root, None, carriers, 0)
        for r in reasons:
            print("FAIL %s" % r, file=sys.stderr)
        print(json.dumps(recompute(root, None, rs, heldout, envs), indent=1))
        return 0
    if not (a.root and a.rev):
        ap.error("--root and --rev are required")
    return main_count(os.path.abspath(a.root), a.rev, a.base)


if __name__ == "__main__":
    sys.exit(main())
