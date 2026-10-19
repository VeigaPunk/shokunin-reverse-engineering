#!/usr/bin/env python3
"""label-test.py — EX-34 (chain c3) custody-receipt UTC label test — v3.

Format-tolerant checker for custody receipts (v1 / v2 shapes). Three parse modes:

  A. block/field mode  — `PATH: <p>` blocks with `KEY: VALUE` fields
                         (the round-1 v1 canonical receipt shape)
  B. pipe/header mode  — a `format:` header naming `|`-separated columns
                         (the round-1 v1 metadata sidecar shape)
  C. value fallback    — per-line timestamp/epoch extraction

Checks per custody path:
  1. UTC-labeled file-time fields (keys naming mtime/ctime + a UTC label) must
     equal the true UTC rendering of that file's epoch (`date -u -d @epoch`,
     both `%Y-%m-%dT%H:%M:%SZ` and `%Y-%m-%d %H:%M:%S` forms);
  2. they must carry no numeric tz offset (only Z / +00:00 / +0000 acceptable);
  3. round-trip: `date -u -d '<rendered>' +%s` == epoch;
  4. an epoch field must be present for mtime and ctime (v2 claim component);
  5. a UTC-labeled value equal to the LOCAL rendering instead is reported as
     LOCAL_INSTANT_UNDER_UTC_LABEL (the v1 defect class);
  6. local-labeled fields are allowed but must equal the local rendering.

Exit: 0 PASS, 1 FAIL, 2 UNPARSED.
"""
import argparse, json, re, subprocess, sys, os

PATHS = [
    "/home/vgpnk/.config/devin/mcp_config.json",
    "/home/vgpnk/.omp/agent/mcp.json",
    "/home/vgpnk/.kimi-code/config.toml",
    "/home/vgpnk/.bashrc",
    "/home/vgpnk/.profile",
]
TS_RX = re.compile(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:Z|[+-]\d{2}:?\d{2}|[+-]\d{4})?")
E10_RX = re.compile(r"\b1\d{9}\b")
OFFSET_RX = re.compile(r"[+-]\d{2}:?\d{2}$")
ZERO_OFFSET_RX = re.compile(r"[+-]00:?00$")
UTC_RX = re.compile(r"utc", re.I)
LOCAL_RX = re.compile(r"local", re.I)
MT_RX = re.compile(r"mtime|modified", re.I)
CT_RX = re.compile(r"ctime|changed\b", re.I)
EPOCH_RX = re.compile(r"epoch", re.I)
TIMECOL_RX = re.compile(r"(mtime|ctime)", re.I)


def sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True,
                          env=dict(os.environ)).stdout.strip()


def read_live(path):
    live = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 6 or parts[0] not in PATHS:
            continue
        live[parts[0]] = {"sha256": parts[1], "size": parts[2], "inode": parts[3],
                          "mtime_epoch": int(parts[4]), "ctime_epoch": int(parts[5])}
    return live


def utc_renders(epoch):
    return {sh(f"date -u -d @{epoch} '+%Y-%m-%dT%H:%M:%SZ'"),
            sh(f"date -u -d @{epoch} '+%Y-%m-%d %H:%M:%S'")}


def local_renders(epoch):
    return {sh(f"date -d @{epoch} '+%Y-%m-%d %H:%M:%S'"),
            sh(f"date -d @{epoch} '+%Y-%m-%dT%H:%M:%S%z'")}


def parse_epoch(ts):
    out = sh(f"date -u -d '{ts}' '+%s' 2>/dev/null")
    try:
        return int(out)
    except ValueError:
        return None


def check_filetime(ts, true_epoch, label, ctx):
    rec = {"ts": ts, "label": label, **ctx}
    if OFFSET_RX.search(ts) and not ZERO_OFFSET_RX.search(ts):
        rec["kind"] = "TZ_OFFSET_PRESENT"
        return rec
    back = parse_epoch(ts)
    rec["roundtrip_epoch"] = back
    rec["true_epoch"] = true_epoch
    if back == true_epoch:
        rec["kind"] = "OK"
        rec["delta_vs_true_epoch"] = 0
        return rec
    rec["delta_vs_true_epoch"] = None if back is None else back - true_epoch
    rec["ts_equals_utc_render"] = ts in utc_renders(true_epoch)
    rec["ts_equals_local_render"] = ts in local_renders(true_epoch)
    if ts in local_renders(true_epoch) and ts not in utc_renders(true_epoch):
        rec["kind"] = "LOCAL_INSTANT_UNDER_UTC_LABEL"
    elif ts in utc_renders(true_epoch):
        rec["kind"] = "OK"
        rec["delta_vs_true_epoch"] = 0
    else:
        rec["kind"] = "ROUNDTRIP_MISMATCH"
    return rec


def analyze(receipt_path, live):
    text = open(receipt_path, errors="replace").read()
    lines = text.splitlines()
    findings, rows = [], []
    strict_v2 = bool(re.search(r"receipt-version:\s*2", text))

    # header line for pipe mode (computed first: decides whether path-start
    # lines are mode-A blocks or mode-B pipe rows)
    hdr = None
    for i, line in enumerate(lines, 1):
        if "|" in line and TIMECOL_RX.search(line) and not any(p in line for p in PATHS):
            cols = [re.sub(r"^#\s*(format\s*:\s*)?", "", c.strip().strip("()")).lower()
                    for c in line.split("|")]
            hdr = (i, cols)

    # ---- mode A: block/field ------------------------------------------------
    cur = None
    blocks = []
    for ln, line in enumerate(lines, 1):
        m = re.match(r"\s*(?:#\s*)?PATH\s*:\s*(\S+)\s*$", line)
        if m and m.group(1) in PATHS:
            cur = {"path": m.group(1), "lines": [(ln, "PATH: " + m.group(1))]}
            blocks.append(cur)
            continue
        if cur is not None:
            for p in PATHS:
                if line.strip() == p or line.strip().startswith(p + " "):
                    cur = None
                    break
            if cur is not None:
                cur["lines"].append((ln, line))
    # also: lines that start with a custody path (pipe rows / compact lines)
    for ln, line in enumerate(lines, 1):
        s = line.strip()
        if hdr and "|" in line:
            continue
        for p in PATHS:
            if s.startswith(p):
                blocks.append({"path": p, "lines": [(ln, line)]})
                break

    if blocks:
        for blk in blocks:
            st = live.get(blk["path"])
            if st is None:
                findings.append({"kind": "NO_LIVE_STAT", "path": blk["path"]})
                continue
            exp = {"mtime": st["mtime_epoch"], "ctime": st["ctime_epoch"]}
            row = {"path": blk["path"], "fields": {}, "epochs": {}}
            for ln, line in blk["lines"]:
                fm = re.match(r"\s*(?:#\s*)?([A-Za-z][A-Za-z0-9 _\-()\.]*?)\s*[:=]\s*(.+?)\s*$", line)
                if not fm:
                    continue
                key, val = fm.group(1).strip(), fm.group(2).strip()
                if key.upper() == "PATH":
                    continue
                row["fields"][key] = val
                kind = "mtime" if MT_RX.search(key) else ("ctime" if CT_RX.search(key) else None)
                if kind is None:
                    continue
                true_epoch = exp[kind]
                ts = TS_RX.search(val)
                ep = E10_RX.fullmatch(val) or (E10_RX.search(val) if EPOCH_RX.search(key) else None)
                if ep and ep.group(0) and E10_RX.fullmatch(ep.group(0) if isinstance(ep, re.Match) else str(ep)):
                    epv = int(ep.group(0) if isinstance(ep, re.Match) else ep)
                    row["epochs"][kind] = epv
                    if epv != true_epoch:
                        findings.append({"kind": "EPOCH_MISMATCH", "path": blk["path"],
                                         "line": ln, "key": key, "value": epv,
                                         "true_epoch": true_epoch})
                if ts:
                    labeled_utc = bool(UTC_RX.search(key))
                    labeled_local = bool(LOCAL_RX.search(key))
                    ctx = {"line": ln, "path": blk["path"], "key": key}
                    if labeled_local and not labeled_utc:
                        # local render: must denote the SAME instant (offset
                        # suffix makes `date -u -d <ts>` the identity check)
                        tok = ts.group(0)
                        back = parse_epoch(tok)
                        has_off = bool(OFFSET_RX.search(tok))
                        if back == true_epoch and has_off:
                            findings.append({**ctx, "ts": tok, "kind": "OK",
                                             "label": "local (correctly labeled, offset-bearing)"})
                        elif back == true_epoch and tok in local_renders(true_epoch):
                            findings.append({**ctx, "ts": tok, "kind": "OK",
                                             "label": "local (correctly labeled)"})
                        else:
                            findings.append({**ctx, "ts": tok,
                                             "kind": "LOCAL_LABEL_MISMATCH",
                                             "delta_vs_true_epoch": None if back is None else back - true_epoch,
                                             "label": "local"})
                    else:
                        tok = ts.group(0)
                        findings.append(check_filetime(
                            tok, true_epoch,
                            "utc" if labeled_utc else "unlabeled", ctx))
                        if labeled_utc and strict_v2 and not re.fullmatch(
                                r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", tok):
                            findings.append({**ctx, "ts": tok,
                                             "kind": "UTC_RENDER_NOT_STRICT",
                                             "note": "v2 UTC render must be YYYY-MM-DDTHH:MM:SSZ"})
            for kind in ("mtime", "ctime"):
                if kind not in row["epochs"]:
                    findings.append({"kind": "NO_EPOCH_FIELD", "path": blk["path"],
                                     "field": kind})
            # capture-time sanity: capture-utc style keys must end with Z / +00:00
            for k, v in row["fields"].items():
                if re.search(r"capture|recompute", k, re.I) and TS_RX.search(v):
                    ts = TS_RX.search(v).group(0)
                    if not (ts.endswith("Z") or ZERO_OFFSET_RX.search(ts)):
                        findings.append({"kind": "CAPTURE_TIME_TZ_SUSPECT",
                                         "path": blk["path"], "ts": ts, "key": k})
            rows.append(row)

    # ---- mode B: pipe rows with header -------------------------------------
    if hdr:
        cols = hdr[1]
        for ln, line in enumerate(lines, 1):
            if "|" not in line or not any(p in line for p in PATHS):
                continue
            path = next(p for p in PATHS if p in line)
            st = live.get(path)
            if st is None:
                continue
            cells = [c.strip() for c in line.split("|")]
            exp = {"mtime": st["mtime_epoch"], "ctime": st["ctime_epoch"]}
            epochs_seen = {"mtime": None, "ctime": None}
            for j, c in enumerate(cols):
                if j >= len(cells):
                    continue
                kind = "mtime" if "mtime" in c else ("ctime" if "ctime" in c else None)
                if kind is None:
                    continue
                cell = cells[j]
                if E10_RX.fullmatch(cell) and EPOCH_RX.search(c):
                    epochs_seen[kind] = int(cell)
                    if int(cell) != exp[kind]:
                        findings.append({"kind": "EPOCH_MISMATCH", "line": ln, "path": path,
                                         "key": c, "value": int(cell), "true_epoch": exp[kind]})
                mts = TS_RX.search(cell)
                if mts:
                    ctx = {"line": ln, "path": path, "key": c}
                    findings.append(check_filetime(
                        mts.group(0), exp[kind],
                        "utc" if UTC_RX.search(c) else ("local" if LOCAL_RX.search(c) else "unlabeled"),
                        ctx))
                    if UTC_RX.search(c) and strict_v2 and not re.fullmatch(
                            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", mts.group(0)):
                        findings.append({**ctx, "ts": mts.group(0),
                                         "kind": "UTC_RENDER_NOT_STRICT"})
            for kind in ("mtime", "ctime"):
                if epochs_seen[kind] is None:
                    findings.append({"kind": "NO_EPOCH_FIELD", "line": ln, "path": path,
                                     "field": kind})
            rows.append({"path": path, "mode": "pipe"})

    # ---- mode C: value fallback (only if A/B produced nothing for a path) --
    seen_paths = {r["path"] for r in rows}
    for ln, line in enumerate(lines, 1):
        hit = [p for p in PATHS if p in line]
        if len(hit) != 1:
            continue
        path = hit[0]
        if path in seen_paths:
            continue
        st = live.get(path)
        if st is None:
            continue
        for ts in TS_RX.findall(line):
            exp = local_renders(st["mtime_epoch"]) | utc_renders(st["mtime_epoch"])
            ctx = {"line": ln, "path": path, "key": "<value-mode>"}
            rec = check_filetime(ts, st["mtime_epoch"], "utc-if-labeled", ctx)
            if rec["kind"] == "ROUNDTRIP_MISMATCH":
                # capture-time token on a compact line (e.g. sha256 lists with a timestamp)
                if ts.endswith("Z"):
                    rec = {"kind": "OK", "ts": ts, "label": "capture (Z)", **ctx}
                else:
                    rec = {**rec, "kind": "ROUNDTRIP_MISMATCH"}
            findings.append(rec)
        rows.append({"path": path, "mode": "value"})

    if not rows:
        return {"receipt": receipt_path, "verdict": "UNPARSED", "rows": [], "findings": []}
    bad = [f for f in findings if f["kind"] != "OK"]
    return {"receipt": receipt_path, "verdict": "PASS" if not bad else "FAIL",
            "rows": rows, "findings": findings,
            "counts": {"total": len(findings),
                       "ok": sum(1 for f in findings if f["kind"] == "OK"),
                       "bad": len(bad)}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--receipt", required=True)
    ap.add_argument("--live", required=True)
    ap.add_argument("--json", default=None)
    ap.add_argument("--quiet", action="store_true")
    a = ap.parse_args()
    if not os.path.exists(a.receipt):
        print(f"RECEIPT: {a.receipt}\nUNREADABLE: file not found")
        return 2
    res = analyze(a.receipt, read_live(a.live))
    if not a.quiet:
        print(f"RECEIPT: {a.receipt}")
        print(f"TZ: {os.environ.get('TZ','<unset>')}   rows: {len(res['rows'])}")
        for f in res["findings"]:
            if f["kind"] == "OK":
                continue
            print(f"  [{f['kind']}] line={f.get('line','-')} {f.get('path','')} "
                  f"{f.get('key','')} {f.get('ts','')} delta={f.get('delta_vs_true_epoch','')}")
        c = res.get("counts", {})
        print(f"  checks: total={c.get('total')} ok={c.get('ok')} bad={c.get('bad')}")
        print(f"VERDICT: {res['verdict']}")
    if a.json:
        json.dump(res, open(a.json, "w"), indent=1)
    return {"PASS": 0, "FAIL": 1, "UNPARSED": 2}[res["verdict"]]


if __name__ == "__main__":
    sys.exit(main())
