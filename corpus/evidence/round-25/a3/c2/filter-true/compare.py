#!/usr/bin/env python3
"""Round 25 attempt 3, seat C2FilterTrue: compare openchain filter=true with the
local filtered=false subset of the saved filter=false responses, and re-score the
openchain naming rules from the filter=true responses.

Reads the lane read-only. Writes only under this seat directory.

Usage: python3 -I -B compare.py
"""
import glob
import hashlib
import importlib.util
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
EVID = os.path.join(LANE, "corpus/evidence/round-25/a2/c2")
SEAT = "/fast/scratch/hyaku/kaidoku-r25-a3/seats/C2FilterTrue"
FT = os.path.join(SEAT, "filtertrue")
RESOLVER = os.path.join(LANE, "tools/round-25/a2/resolve-selectors.py")
TALLY = os.path.join(LANE, "tools/round-25/a3/tally-resolution.py")

# load the lane's tally module so rule semantics are identical to the committed count
spec = importlib.util.spec_from_file_location("lane_tally", TALLY)
lane_tally = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lane_tally)


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def load_manifest(d):
    with open(os.path.join(d, "manifest.json"), encoding="utf-8") as f:
        return json.load(f)


def oc_rows(path):
    """Candidate rows for one selector from a saved openchain response file.

    Returns (rows, key, raw_value) where raw_value is None when the server
    answered with a JSON null and [] when it answered with an empty array.
    """
    with open(path, encoding="utf-8") as f:
        body = json.load(f)
    fn = ((body.get("result") or {}).get("function") or {})
    sel = None
    for k in fn:
        sel = k
    raw = fn.get(sel) if sel else None
    rows = raw or []
    return rows, sel, raw


def carrier_dirs():
    out = []
    for d in sorted(glob.glob(os.path.join(EVID, "*", "db"))):
        if os.path.isdir(d):
            out.append((os.path.basename(os.path.dirname(d)), d))
    return out


def build_ft_dirs():
    """Per-carrier response dirs that hold only the filter=true openchain files."""
    made = []
    for name, dbdir in carrier_dirs():
        dst = os.path.join(SEAT, f"ft-{name}")
        os.makedirs(dst, exist_ok=True)
        for p in sorted(glob.glob(os.path.join(dbdir, "openchain-*.json"))):
            sel = os.path.basename(p)[len("openchain-"):-len(".json")]
            src = os.path.join(FT, f"openchain-{sel}.json")
            if not os.path.exists(src):
                continue
            with open(src, "rb") as f:
                data = f.read()
            with open(os.path.join(dst, os.path.basename(src)), "wb") as g:
                g.write(data)
        made.append((name, dst))
    return made


def analyze_carrier(name, responses_dir, abi):
    p = subprocess.run([sys.executable, "-I", "-B", RESOLVER, "analyze",
                        "--envelope", os.path.join(EVID, name, "envelope.json"),
                        "--responses", responses_dir,
                        "--abi", os.path.join(LANE, abi)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise SystemExit(f"analyze failed for {name}: {p.stderr[-500:]}")
    return json.loads(p.stdout)


def ft_rule_outputs(row):
    """Rules 4 and 5 recomputed from a filter=true response.

    ft_sole            : the only candidate the filter=true response returned
    ft_sole_unfiltered : the only returned candidate whose filtered flag is false
    ft_sole_unfiltered_args_consistent :
        the only returned candidate whose filtered flag is false and whose
        parameter list matches REA's inference
    """
    oc = row["databases"].get("openchain")
    detail = oc["detail"] if oc else []
    out = {}
    out["ft_sole"] = detail[0]["text"] if len(detail) == 1 else None
    out["ft_first"] = detail[0]["text"] if detail else None
    u = [x["text"] for x in detail if x.get("filtered") is False]
    out["ft_sole_unfiltered"] = u[0] if len(u) == 1 else None
    ua = [x["text"] for x in detail if x.get("filtered") is False and x.get("label") == "consistent"]
    out["ft_sole_unfiltered_args_consistent"] = ua[0] if len(ua) == 1 else None
    return out


def score(rows, getter):
    res = {}
    for k in ("openchain_sole_unfiltered", "openchain_sole_unfiltered_args_consistent"):
        named = right = wrong = 0
        for r in rows:
            got = getter(r).get(k)
            if got is None:
                continue
            named += 1
            if got == r["abi_signature"]:
                right += 1
            else:
                wrong += 1
        res[k] = {"named": named, "right": right, "wrong": wrong, "no_name": len(rows) - named}
    for k in ("ft_sole", "ft_first", "ft_sole_unfiltered", "ft_sole_unfiltered_args_consistent"):
        named = right = wrong = 0
        for r in rows:
            got = getter(r).get(k)
            if got is None:
                continue
            named += 1
            if got == r["abi_signature"]:
                right += 1
            else:
                wrong += 1
        res[k] = {"named": named, "right": right, "wrong": wrong, "no_name": len(rows) - named}
    return res


def main():
    out = {"integrity": {}, "per_selector": [], "score": {}, "differences": {}}

    # 1. integrity of the lane's saved filter=false responses and of my filter=true files
    lane_bad = []
    for name, dbdir in carrier_dirs():
        for m in load_manifest(dbdir):
            if not m["file"].startswith("openchain-"):
                continue
            got = sha256(os.path.join(dbdir, m["file"]))
            if got != m["sha256"]:
                lane_bad.append({"carrier": name, "file": m["file"], "manifest": m["sha256"], "actual": got})
    out["integrity"]["lane_filterfalse_sha256_mismatch"] = lane_bad
    ft_bad = []
    for m in load_manifest(FT):
        got = sha256(os.path.join(FT, m["file"]))
        if got != m["sha256"]:
            ft_bad.append({"file": m["file"], "manifest": m["sha256"], "actual": got})
    out["integrity"]["filtertrue_sha256_mismatch"] = ft_bad
    out["integrity"]["filtertrue_requests"] = len(load_manifest(FT))

    # 2. per-selector set comparison (distinct selectors)
    sels = sorted(os.path.basename(p)[len("openchain-"):-len(".json")]
                  for p in glob.glob(os.path.join(FT, "openchain-*.json")))
    per_sel = []
    for sel in sels:
        # every lane copy of this selector's filter=false response
        copies = []
        for name, dbdir in carrier_dirs():
            p = os.path.join(dbdir, f"openchain-{sel}.json")
            if os.path.exists(p):
                rows, key, raw = oc_rows(p)
                copies.append({"carrier": name, "sha256": sha256(p),
                               "key": key,
                               "n": len(rows) if rows else 0,
                               "unfiltered": [r["name"] for r in (rows or []) if r.get("filtered") is False],
                               "unfiltered_verified": [r.get("hasVerifiedContract") for r in (rows or []) if r.get("filtered") is False],
                               "filtered": [r["name"] for r in (rows or []) if r.get("filtered") is not False]})
        ftpath = os.path.join(FT, f"openchain-{sel}.json")
        ftr, ftkey, ftraw = oc_rows(ftpath)
        ft_names = [r["name"] for r in (ftr or [])]
        ft_unf = [r["name"] for r in (ftr or []) if r.get("filtered") is False]
        unfiltered_sets = {tuple(c["unfiltered"]) for c in copies}
        same_set = (len(unfiltered_sets) == 1
                    and all(set(c["unfiltered"]) == set(ft_unf) for c in copies))
        same_order = all(tuple(c["unfiltered"]) == tuple(ft_unf) for c in copies)
        per_sel.append({"selector": sel,
                        "lane_copies": copies,
                        "lane_copy_count": len(copies),
                        "lane_copies_identical": len(unfiltered_sets) == 1,
                        "local_unfiltered": list(next(iter(unfiltered_sets))) if len(unfiltered_sets) == 1 else None,
                        "filtertrue_all": ft_names,
                        "filtertrue_unfiltered": ft_unf,
                        "filtertrue_key": ftkey,
                        "filtertrue_raw_is_null": ftraw is None,
                        "set_equal": same_set,
                        "order_equal": same_order,
                        "unfiltered_count_equal": all(len(c["unfiltered"]) == len(ft_names) for c in copies),
                        "counts_equal": all(c["n"] == len(ft_names) for c in copies)})
    out["per_selector"] = per_sel
    out["differences"] = {
        "selectors_compared": len(per_sel),
        "set_equal": sum(1 for s in per_sel if s["set_equal"]),
        "set_different": [s["selector"] for s in per_sel if not s["set_equal"]],
        "order_different": [s["selector"] for s in per_sel if not s["order_equal"]],
        "count_different": [s["selector"] for s in per_sel if not s["counts_equal"]],
        "unfiltered_count_different": [s["selector"] for s in per_sel if not s["unfiltered_count_equal"]],
        "junk_removed_total": sum(c["n"] - len(c["unfiltered"]) for s in per_sel for c in s["lane_copies"]),
        "unfiltered_without_verified_contract": sorted({
            s["selector"] for s in per_sel for c in s["lane_copies"]
            for v in c["unfiltered_verified"] if v is False}),
        "filtertrue_empty_array": sorted({
            s["selector"] for s in per_sel if s["filtertrue_all"] == []}),
        "filtertrue_null": sorted({
            s["selector"] for s in per_sel if s["filtertrue_all"] == [] and s["filtertrue_key"] is None}),
        "lane_copies_disagreeing": [s["selector"] for s in per_sel if not s["lane_copies_identical"]],
        "filtertrue_has_filtered_true": [s["selector"] for s in per_sel
                                          if any(x not in s["filtertrue_unfiltered"] for x in s["filtertrue_all"])],
    }

    # 3. rule scoring: lane filter=false baseline vs filter=true recomputation
    carriers = [ln.rstrip("\n").split("\t") for ln in
                open(os.path.join(EVID, "carriers.tsv"), encoding="utf-8") if ln.strip()]
    base_rows, ft_rows = [], []
    ft_dirs = build_ft_dirs()
    for name, _hex, abi in carriers:
        d = analyze_carrier(name, os.path.join(EVID, name, "db"), abi)
        for r in d["rows"]:
            r["carrier"] = name
        base_rows += d["rows"]
    ftdirmap = dict(ft_dirs)
    for name, _hex, abi in carriers:
        d = analyze_carrier(name, ftdirmap[name], abi)
        for r in d["rows"]:
            r["carrier"] = name
        ft_rows += d["rows"]

    def base_getter(r):
        o = lane_tally.rule_outputs(r)
        return o

    def ft_getter(r):
        o = dict(base_getter(r))
        o.update(ft_rule_outputs(r))
        return o

    def distinct(rows):
        # representative row per selector, chosen in carriers.tsv order so the
        # filter=false and filter=true runs pick the SAME carrier per selector
        d = {}
        for r in rows:
            d.setdefault(r["selector"], r)
        return list(d.values())

    out["score"] = {
        "per_carrier_rows_filterfalse": score(base_rows, base_getter),
        "per_carrier_rows_filtertrue": score(ft_rows, ft_getter),
        "distinct_selectors_filterfalse": score(distinct(base_rows), base_getter),
        "distinct_selectors_filtertrue": score(distinct(ft_rows), ft_getter),
        "rows_per_carrier": len(base_rows),
        "rows_filtertrue": len(ft_rows),
    }

    # 4. per-row diff of the two rule-4/5 answers
    diffs = []
    bmap = {(r["carrier"], r["selector"]): r for r in base_rows}
    for r in ft_rows:
        b = bmap.get((r["carrier"], r["selector"]))
        if not b:
            continue
        bo = lane_tally.rule_outputs(b)
        fo = ft_getter(r)
        for k in ("openchain_sole_unfiltered", "openchain_sole_unfiltered_args_consistent"):
            if bo.get(k) != fo.get(k):
                diffs.append({"carrier": r["carrier"], "selector": r["selector"], "rule": k,
                              "filterfalse": bo.get(k), "filtertrue": fo.get(k),
                              "abi": r["abi_signature"]})
    out["rule_row_differences"] = diffs

    # 5. rows where the filter=true response disagrees with the local subset
    ftmap = {}
    for name, dst in ft_dirs:
        for p in glob.glob(os.path.join(dst, "openchain-*.json")):
            sel = os.path.basename(p)[len("openchain-"):-len(".json")]
            rows, key, raw = oc_rows(p)
            ftmap[(name, sel)] = [r["name"] for r in (rows or [])]
    mis = []
    for r in base_rows:
        loc = [x["text"] for x in (r["databases"]["openchain"]["detail"] if r["databases"].get("openchain") else [])
               if x.get("filtered") is False]
        f = ftmap.get((r["carrier"], r["selector"]))
        if f is not None and sorted(f) != sorted(loc):
            mis.append({"carrier": r["carrier"], "selector": r["selector"], "local_unfiltered": loc, "filtertrue": f})
    out["row_level_set_mismatch"] = mis

    with open(os.path.join(SEAT, "compare.json"), "w", encoding="utf-8") as g:
        json.dump(out, g, indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "per_selector"}, indent=1)[:6000])
    return 0


if __name__ == "__main__":
    sys.exit(main())
