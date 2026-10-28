#!/usr/bin/env python3
"""ScribeReport ingest: spec roster -> seat reports -> results.json, with pointer audit.

Read-only on the lane. Emits JSON summary + markdown table into scratch.
"""
import json, os, re, sys, glob

ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
WAVE = os.path.join(ROOT, ".ufo/waves/round-47")
W1 = os.path.join(WAVE, "w1")

def rel(p):
    return os.path.relpath(p, ROOT)

def load_spec():
    s = json.load(open(os.path.join(WAVE, "w1-spec.json")))
    out = {}
    for it in s["items"]:
        p = it["prompt"]
        body = p.split("Act directly via tool calls.\n\n", 1)
        body = body[1] if len(body) > 1 else p
        body = body.split("Lane bounds:")[0]
        head = " ".join(body.split())
        out[it["name"]] = {
            "role": it["role"],
            "headline": head[:400],
            "prompt_bytes": len(it["prompt"]),
        }
    return out

def find_results():
    for name in ("r47-w1-results.json", "w1-results.json"):
        p = os.path.join(WAVE, name)
        if os.path.exists(p):
            return p
    return None

def load_results(p):
    d = json.load(open(p))
    seats = {}
    for r in d.get("results", []):
        name = r.get("name")
        out = r.get("output")
        parsed, err = None, None
        if isinstance(out, str):
            try:
                parsed = json.loads(out)
            except Exception as e:
                err = f"output not JSON: {e}"
        elif isinstance(out, dict):
            parsed = out
        seats[name] = {
            "agent": r.get("agent"),
            "parsed": parsed,
            "parse_error": err,
            "raw_len": len(out) if isinstance(out, str) else None,
            "raw": out if not parsed else None,
        }
    return d, seats

# --- path extraction -------------------------------------------------------
PATH_RE = re.compile(r"\.ufo/waves/round-47/[A-Za-z0-9_./-]+")

def paths_in(text):
    return sorted(set(m.rstrip(".,;:)`'\"") for m in PATH_RE.findall(text)))

def audit_paths(texts):
    """Return (existing, missing) for every cited .ufo path."""
    seen = []
    for t in texts:
        if not isinstance(t, str):
            continue
        for p in paths_in(t):
            if p not in seen:
                seen.append(p)
    ok, bad = [], []
    for p in seen:
        full = os.path.join(ROOT, p)
        (ok if os.path.exists(full) else bad).append(p)
    return ok, bad

def report_files(name):
    d = os.path.join(W1, name)
    if not os.path.isdir(d):
        return []
    return sorted(os.path.basename(p) for p in glob.glob(os.path.join(d, "*")))

def main():
    spec = load_spec()
    res_p = find_results()
    results, seats = (None, {})
    if res_p:
        results, seats = load_results(res_p)

    rows = []
    for name in spec:
        rd = os.path.join(W1, name, "report.md")
        has_report = os.path.exists(rd)
        rep_text = open(rd, encoding="utf-8", errors="replace").read() if has_report else ""
        files = report_files(name)
        st = seats.get(name, {})
        texts = [rep_text]
        if st.get("parsed"):
            texts.append(json.dumps(st["parsed"]))
        elif st.get("raw"):
            texts.append(st["raw"])
        ok, bad = audit_paths(texts)
        rows.append({
            "seat": name,
            "role": spec[name]["role"],
            "headline": spec[name]["headline"],
            "report": has_report,
            "report_bytes": len(rep_text),
            "artifacts": files,
            "in_results": name in seats if results else None,
            "parse_error": st.get("parse_error"),
            "paths_ok": len(ok),
            "paths_bad": bad,
            "parsed": st.get("parsed"),
            "report_text": rep_text,
        })

    summary = {
        "results_file": rel(res_p) if res_p else None,
        "n_spec": len(spec),
        "n_reports": sum(1 for r in rows if r["report"]),
        "n_artifacts": sum(1 for r in rows if r["artifacts"]),
        "n_in_results": sum(1 for r in rows if r["in_results"]) if results else 0,
        "n_bad_pointers": sum(1 for r in rows if r["paths_bad"]),
        "rows": rows,
    }
    out = os.path.join("/fast/scratch/hyaku/kaidoku-r47/ScribeReport", "ingest.json")
    json.dump(summary, open(out, "w"), indent=1)
    print(json.dumps({k: v for k, v in summary.items() if k != "rows"}, indent=1))
    print("seats with reports:", summary["n_reports"], "/", summary["n_spec"])
    missing = [r["seat"] for r in rows if not r["report"]]
    print("no report.md yet:", len(missing))
    if missing:
        print("  " + " ".join(missing))
    bad = [(r["seat"], r["paths_bad"]) for r in rows if r["paths_bad"]]
    if bad:
        print("BAD POINTERS:")
        for s, b in bad:
            print(f"  {s}: {b}")

if __name__ == "__main__":
    main()
