#!/usr/bin/env python3
"""RV-11 rule-#11 conformance audit for the citation-drift pointer table.

Checks every entry of a pointer-table.json against SKILL.md:197-205 (rule #11:
citations into an operator-mutable file anchor by stanza key + receipt, never
by bare line number; a line number may appear only inside an append-only record
that names its capture stamp) and against the arc2-loop1-round4 no-laundering
precedent (a pinnable in-repo byte that re-states an unpinnable live value is a
laundered pin).

Usage: rule11-audit.py --root REPO --table TABLE.json [--expected EXPECTED.json] [--json OUT]
Exit: 0 always (audit is reported, never failed) -- the reviewer reads the rows.
"""
import argparse, json, os, re, sys

OM = {
    "config.toml": r"(?:~|/home/vgpnk)/\.kimi-code/config\.toml|\bconfig\.toml",
    "mcp_config.json": r"(?:~|/home/vgpnk)/\.config/devin/mcp_config\.json|\bmcp_config\.json",
    "omp mcp.json": r"(?:~|/home/vgpnk)/\.omp/agent/mcp\.json|\bmcp\.json",
    ".bashrc": r"(?:~|/home/vgpnk)/\.bashrc|\b\.bashrc",
    ".profile": r"(?:~|/home/vgpnk)/\.profile|\b\.profile",
}
OM_NAME = "|".join("(?:%s)" % v for v in OM.values())
OM_TOKEN = re.compile(r"(%s)\s*:(\d+)(?:\s*-\s*(\d+))?" % OM_NAME)
OM_BARE = re.compile(r"(%s)\b" % OM_NAME)
# content keys rule #11 names as the conforming anchor
CONTENT_KEY = re.compile(
    r"\[mcp_servers\.[a-z_]+\]|\bargs\b|rea-agents@\d|\bREA_[A-Z_]+\b|"
    r"GHIDRA_INSTALL_DIR|JAVA_HOME|startup_timeout_sec")
STAMP = re.compile(r"\b\d{2}:\d{2}(?::\d{2})?Z\b|\b\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z\b")
RECEIPT_PATH = re.compile(r"\.ufo/waves/[\w./-]*receipts/[\w./-]+|@[a-z0-9-]+")
LIVE_WORDS = re.compile(r"\blive\b|at HEAD|current\b|still reads|live file", re.I)
APPEND_ONLY_PREFIXES = (
    "corpus/knowledge/", "corpus/lessons/", ".ufo/waves/",
    "LOG.md", "corpus/README.md", "evidence/",
)
# strings that look like a laundered pin: the pinned byte IS a line number token
LAUNDER_VALUE = re.compile(r"^\s*:?\d{1,4}(-\d{1,4})?\s*$|^config\.toml:\d+$|^:\d+$")


def strings_of(entry):
    out = {}
    for k, v in entry.items():
        if isinstance(v, str):
            out[k] = v
        elif isinstance(v, int):
            out[k] = str(v)
    return out


def is_append_only(path):
    return any(path.startswith(p) for p in APPEND_ONLY_PREFIXES)


def audit_entry(entry, expected):
    eid = entry.get("id", "<unnamed>")
    kind = entry.get("kind")
    f = entry.get("file", "")
    tgt = entry.get("target", "")
    strs = strings_of(entry)
    blob = " | ".join(strs.values())
    # de-escape: a token hidden behind regex escaping (`config\.toml:1287`)
    # is the same token for rule #11's purposes
    blob = re.sub(r"\\(.)", r"\1", blob)

    tok_hits = OM_TOKEN.findall(blob)          # (om-name, lo, hi)
    bare_hits = OM_BARE.findall(blob)
    key_hits = CONTENT_KEY.findall(blob)
    stamp_named = bool(STAMP.search(blob))
    receipt_named = bool(RECEIPT_PATH.search(blob))
    live_claim = bool(LIVE_WORDS.search(blob))

    om_file = bool(OM_BARE.search(f)) or bool(OM_BARE.search(tgt))
    snap_target = tgt.startswith("@") or f.startswith("@")
    snap_pinned = None
    if snap_target:
        slug = (tgt if tgt.startswith("@") else f)[1:]
        snap_pinned = slug in (expected.get("snapshots") or {})

    findings = []
    # T1: a live operator-mutable file graded by line number (the probe resolves
    # in-repo paths only; an OM path grades as citation_file_absent -- but the
    # TABLE may still carry the intent, which is the rule-#11 question).
    if om_file and kind != "anchor":
        findings.append("OM_GRADED_BY_LINE")
    if snap_target and snap_pinned is False:
        findings.append("SNAPSHOT_UNPINNED")
    # T2: bare line-number tokens into an operator-mutable file anywhere in the
    # entry's strings. Conforming ONLY inside an append-only record that names
    # its capture stamp (rule #11's sole exception).
    if tok_hits:
        # rule #11's sole exception: a line number inside an append-only record
        # that names its capture stamp. The table encodes this as kind=quoted
        # (the probe grades the words, never a live value); a record-quoted row
        # is conforming, an `exact` row asserting the same token is not.
        exception = is_append_only(f) and (stamp_named or receipt_named)
        record_quoted = (kind == "quoted") and is_append_only(f) and not live_claim
        if not (exception or record_quoted):
            findings.append("OM_LINE_TOKEN")
    # T3: laundering (r4 precedent) -- a pinnable in-repo pinned VALUE that is
    # itself a line number into an OM file, i.e. the covered byte re-states an
    # unpinnable live value.
    mm = re.sub(r"\\\\(.)", r"\1", (strs.get("must_match", "") or "")
                + " " + (strs.get("pattern", "") or "")).strip().strip("^$")
    if kind in ("exact", "quoted", "extracted") and not om_file:
        if LAUNDER_VALUE.match(mm) or (tok_hits and live_claim):
            findings.append("LAUNDERED_PIN")
    # T4: config-class entries must carry the content key half of rule #11.
    # config_class = the entry grades an OM file or names one in its strings;
    # a receipt filename that merely contains "config" is not the class.
    config_class = om_file or bool(tok_hits) or bool(bare_hits)
    if config_class and not key_hits and not snap_target:
        if not ((kind == "quoted") and is_append_only(f)):
            findings.append("NO_CONTENT_KEY")
    return {
        "id": eid, "kind": kind, "file": f, "target": tgt,
        "om_tokens": ["%s:%s%s" % (a, b, ("-%s" % c) if c else "") for a, b, c in tok_hits],
        "bare_om_names": sorted(set(bare_hits)),
        "content_keys": sorted(set(key_hits)),
        "stamp_named": stamp_named, "receipt_named": receipt_named,
        "live_claim": live_claim, "append_only_target": is_append_only(f),
        "om_file": om_file, "snap_pinned": snap_pinned,
        "verdict": "CONFORM" if not findings else "VIOLATION:" + ",".join(findings),
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--table", required=True)
    ap.add_argument("--expected", default=None)
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    table = json.load(open(os.path.join(a.root, a.table) if not os.path.isabs(a.table) else a.table))
    exp = {}
    if a.expected:
        p = a.expected if os.path.isabs(a.expected) else os.path.join(a.root, a.expected)
        if os.path.isfile(p):
            exp = json.load(open(p))
    rows = []
    for e in table.get("entries", []):
        rows.append(audit_entry(e, exp))
    for e in table.get("quoted", []):
        r = audit_entry(dict(e, kind="quoted"), exp)
        r["array"] = "quoted"
        rows.append(r)
    for e in table.get("exempt", []):
        r = {"id": e.get("id", "<exempt>"), "kind": "exempt", "file": e.get("file", ""),
             "target": e.get("target", ""), "om_tokens": [], "bare_om_names": [],
             "content_keys": [], "stamp_named": False, "receipt_named": False,
             "live_claim": False, "append_only_target": False, "om_file": False,
             "snap_pinned": None, "array": "exempt",
             "verdict": "UNENFORCED:the probe never grades the exempt array"}
        rows.append(r)
    viol = [r for r in rows if r["verdict"] != "CONFORM"]
    out = {"table": a.table, "entries": len(rows),
           "conform": len(rows) - len(viol), "violations": len(viol), "rows": rows}
    if a.json:
        json.dump(out, open(a.json, "w"), indent=1)
    print("entries=%d conform=%d violations=%d" % (out["entries"], out["conform"], out["violations"]))
    for r in rows:
        mark = "OK " if r["verdict"] == "CONFORM" else ">> "
        print("%s%-28s %-9s %s%s" % (mark, r["id"], r["kind"], r["verdict"],
                                     ("  tokens=%s" % r["om_tokens"]) if r["om_tokens"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())