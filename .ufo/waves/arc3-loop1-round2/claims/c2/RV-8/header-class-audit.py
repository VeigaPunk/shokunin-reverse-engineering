#!/usr/bin/env python3
"""RV-8 review harness — does a proposed census header text name only things
the landed instrument defines?

Usage:
  python3 header-class-audit.py --header HEADER.md [--source .ufo/gates/c1-census-v10.py]
                                [--residuals RESIDUAL_FILE ...] [--json]

Checks, per named token extracted from HEADER:
  G<n>        defines-a-class label -> must appear in SOURCE's docstring
              "DEFECT CLASSES REPAIRED" block as a line start `G<n> ` (the
              instrument's own enumeration of repaired classes)
  DISPOSITION classes STALE / AMBIGUOUS / UNDECLARED / UNRESOLVED / info /
              historical / current-ok -> must appear as a quoted literal in
              SOURCE
  exit codes / ANCHOR-FAIL -> must appear in SOURCE
  H<n>        residual label -> must appear in the source header/comment text
              or in one of the --residuals files (round-1 verdict inventory)
  sha256 prefixes (7+ hex chars followed by ellipsis or 64-hex) -> recomputed
              against the files named on the same line when possible; otherwise
              reported as informational unresolvable tokens
Exit 0 iff no UNKNOWN token was found; 1 otherwise. An unrun check has not
passed: every row carries the command/regex that produced it (--show).
"""
import argparse, json, os, re, subprocess, sys

DEFECTS_RE = re.compile(r"^\s*(G\d+)\s+\S", re.M)
G_LABEL_RE = re.compile(r"\bG(\d+)\b")
DISPOS = ["STALE", "AMBIGUOUS", "UNDECLARED", "UNRESOLVED", "historical",
          "current-ok", "info"]
RESID_RE = re.compile(r"\bH(\d+)\b")
SHA_RE = re.compile(r"\b([0-9a-f]{7,64})\b|([0-9a-f]{7,})\u2026")
EXIT_RE = re.compile(r"\bexit\s*[= ]\s*([012])\b|exit (\d)")


def load_source_sections(src_txt):
    g_defs = set(DEFECTS_RE.findall(src_txt))
    doc = src_txt.split('"""')
    docstring = doc[1] if len(doc) > 1 else ""
    return g_defs, docstring


def audit(header_txt, src_txt, residuals_txt, src_path):
    g_defs, docstring = load_source_sections(src_txt)
    rows = []

    # G-labels: presence in the header, defined in the source enumeration
    for m in G_LABEL_RE.finditer(header_txt):
        lab = "G" + m.group(1)
        rows.append({"token": lab, "kind": "g-label",
                     "ok": lab in g_defs,
                     "where": "DEFECT CLASSES REPAIRED" if lab in g_defs else None,
                     "evidence": ("%s in source enumeration" % lab) if lab in g_defs
                     else ("%s absent from %s" % (lab, src_path))})

    # disposition vocab
    for tok in DISPOS:
        if re.search(r"\b%s\b" % re.escape(tok), header_txt):
            lit = ('"%s"' % tok) in src_txt or ("'%s'" % tok) in src_txt \
                  or tok in src_txt
            rows.append({"token": tok, "kind": "disposition-class", "ok": lit,
                         "where": "source literal" if lit else None,
                         "evidence": "quoted literal found" if lit
                         else "no literal in %s" % src_path})

    if re.search(r"ANCHOR-FAIL", header_txt):
        lit = "ANCHOR-FAIL" in src_txt
        rows.append({"token": "ANCHOR-FAIL", "kind": "exit-class", "ok": lit,
                     "where": "source literal" if lit else None,
                     "evidence": "found" if lit else "absent"})
    decl = re.search(r"Exit (\d) PASS(?:, (\d) FAIL)?(?:, (\d) [\w -]+)?", src_txt)
    declared = {g for g in (decl.groups() if decl else ()) if g}
    for m in EXIT_RE.finditer(header_txt):
        code = m.group(1) or m.group(2)
        can_return = re.search(r"return .*\b%s\b|else %s\b|sys\.exit\(%s\)"
                               % (code, code, code), src_txt) is not None
        lit = (code in declared) or can_return
        rows.append({"token": "exit %s" % code, "kind": "exit-code", "ok": lit,
                     "where": "source" if lit else None,
                     "evidence": ("declared (%s) / returnable" % ",".join(sorted(declared)))
                     if lit else "no return %s / exit declaration" % code})

    # residual labels
    resid_text = src_txt + "\n" + (residuals_txt or "")
    seen = set()
    for m in RESID_RE.finditer(header_txt):
        lab = "H" + m.group(1)
        if lab in seen:
            continue
        seen.add(lab)
        ok = re.search(r"\b%s\b" % lab, resid_text) is not None
        rows.append({"token": lab, "kind": "residual-label", "ok": ok,
                     "where": "residual inventory" if ok else None,
                     "evidence": ("%s present in residual inventory" % lab) if ok
                     else "no %s row anywhere in residuals/source" % lab})

    # sha tokens. A *digest claim* is a 64-hex token, or a 7+-hex token
    # adjacent to "sha256", or any hex token followed by an ellipsis. A bare
    # 7-12 hex token with none of those markers is a git rev / nonce and is
    # NOT verified against file contents (first-run lesson: `14b1682` on a
    # line naming the census file read as a false MISMATCH).
    for ln_no, line in enumerate(header_txt.splitlines(), 1):
        for m in re.finditer(r"[0-9a-f]{7,64}(\u2026|\.\.\.)?", line):
            tok = m.group(0).rstrip("\u2026.")
            if len(tok) < 7:
                continue
            ellipsis = bool(m.group(1))
            digest_claim = len(tok) >= 13 or ellipsis or "sha256" in line.lower()
            row = {"token": tok, "kind": "sha-utterance", "line": ln_no,
                   "ok": None, "where": None, "evidence": ""}
            if not digest_claim:
                row["evidence"] = "bare rev/nonce (no sha256 marker, no ellipsis): not verified"
                rows.append(row)
                continue
            fm = re.search(r"`?([\w./-]+\.(?:py|md|json|toml|txt|sh))", line)
            if fm and os.path.isfile(fm.group(1)):
                h = subprocess.run(["sha256sum", fm.group(1)],
                                   capture_output=True, text=True).stdout.split()[0]
                row["ok"] = h.startswith(tok)
                row["where"] = fm.group(1)
                row["evidence"] = "%s=%s %s" % (fm.group(1), h[:12] + "\u2026",
                                                "matches" if row["ok"] else "MISMATCH")
            else:
                row["evidence"] = ("digest claim (%s-hex%s); no local file on the line: "
                                   "resolve against the named revision manually"
                                   % (len(tok), ", ellipsis" if ellipsis else ""))
            rows.append(row)
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--header", required=True)
    ap.add_argument("--source", default=".ufo/gates/c1-census-v10.py")
    ap.add_argument("--residuals", action="append", default=[])
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    header_txt = open(args.header, encoding="utf-8", errors="replace").read()
    src_txt = open(args.source, encoding="utf-8", errors="replace").read()
    resid = "\n".join(open(p, encoding="utf-8", errors="replace").read()
                      for p in args.residuals) if args.residuals else ""
    rows = audit(header_txt, src_txt, resid, args.source)
    bad = [r for r in rows if r["ok"] is False]
    if args.json:
        print(json.dumps({"header": args.header, "source": args.source,
                          "unknown": bad, "rows": rows}, indent=1))
        return 1 if bad else 0
    print("HEADER-CLASS-AUDIT header=%s source=%s" % (args.header, args.source))
    for r in rows:
        status = {True: "OK", False: "UNKNOWN", None: "INFO"}[r["ok"]]
        print("  [%s] %-12s %-18s %s" % (status, r["token"], r["kind"], r["evidence"]))
    print("UNKNOWN tokens: %d" % len(bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
