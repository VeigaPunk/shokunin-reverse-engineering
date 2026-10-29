#!/usr/bin/env python3
"""s153-verify.py — re-open check for the S153 correction row (draft, seat C2RowS149).

Checks, against a committed FreeBSD sysexits(3) snapshot (default: the round-49 snapshot):
  1. snapshot bytes: size 59,251 and sha256 1fc793a2...5dbf;
  2. each quote is verbatim in the tag-stripped, whitespace-collapsed body, is <= 25 words,
     and lies entirely inside the section whose heading the row names (section = last
     `<a id="HEADING">` anchor before the quote's first character in the raw HTML);
  3. the quote's section is NOT `DESCRIPTION` (S149's cited anchor) — the S149 locator defect;
  4. the S153 row (in --sources): 13 pipe-fields, id S153, status rejected, tier C, kind docs,
     teaches opens `supersedes S149 —` and contains `REJECTED:` and `flip:`, anchor cell names
     each quoted heading and contains each quote verbatim, URL equals S149's URL.
Exit: 0 all hold · 1 any check fails · 2 cannot evaluate (missing file/row).
Output: TSV `check<TAB>result<TAB>detail`. Stdlib only.
"""
import argparse, hashlib, re, sys

SNAP_SHA = "1fc793a298a937d7a22b8724fdd8e26cdb5f1c155a70c0c403f00d26a7b45dbf"
SNAP_BYTES = 59251
URL = "https://man.freebsd.org/cgi/man.cgi?query=sysexits&sektion=3"
QUOTES = [
    ("ERRORS", "EX_USAGE (64) The command was used incorrectly"),
    ("HISTORY", "The sysexits file first appeared in 4BSD."),
]


def normalise(raw):
    """Return (text, idx): text with tags dropped and whitespace collapsed to single spaces;
    idx[i] = offset in raw of text[i]."""
    out, idx = [], []
    i, n = 0, len(raw)
    in_tag = False
    last_space = True
    while i < n:
        c = raw[i]
        if c == "<":
            in_tag = True
        elif c == ">" and in_tag:
            in_tag = False
        elif not in_tag:
            if c.isspace():
                if not last_space:
                    out.append(" "); idx.append(i); last_space = True
            else:
                out.append(c); idx.append(i); last_space = False
        i += 1
    return "".join(out), idx


def sections(raw):
    """List of (raw_offset, heading) for every `<a id="HEADING">` anchor, in order."""
    return [(m.start(), m.group(1)) for m in re.finditer(r'<a id="([A-Z_][A-Z_0-9 ]*)"', raw)]


def section_of(secs, offset):
    name = None
    for pos, h in secs:
        if pos <= offset:
            name = h
        else:
            break
    return name


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--sources", required=True)
    ap.add_argument("--id", default="S153")
    a = ap.parse_args()
    rows = []  # (check, result, detail)
    fails = 0

    def rec(check, ok, detail):
        nonlocal fails
        if not ok:
            fails += 1
        rows.append((check, "pass" if ok else "FAIL", detail))

    try:
        data = open(a.snapshot, "rb").read()
    except OSError as e:
        print(f"snapshot\tcannot-evaluate\t{e}"); return 2
    sha = hashlib.sha256(data).hexdigest()
    rec("snapshot.sha256", sha == SNAP_SHA, sha)
    rec("snapshot.bytes", len(data) == SNAP_BYTES, str(len(data)))
    raw = data.decode("utf-8", errors="replace")
    text, idx = normalise(raw)
    secs = sections(raw)
    rec("snapshot.sections", len(secs) > 0, ",".join(h for _, h in secs))

    for want_sec, quote in QUOTES:
        words = len(quote.split())
        rec(f"quote.{want_sec}.words<=25", words <= 25, str(words))
        pos = text.find(quote)
        if pos < 0:
            rec(f"quote.{want_sec}.verbatim", False, "not found in normalised body")
            continue
        rec(f"quote.{want_sec}.verbatim", True, f"text offset {pos}")
        raw_start = idx[pos]
        raw_end = idx[pos + len(quote) - 1]
        s1 = section_of(secs, raw_start)
        s2 = section_of(secs, raw_end)
        rec(f"quote.{want_sec}.section", s1 == want_sec and s2 == want_sec, f"start={s1} end={s2}")

    # S149's cited anchor is DESCRIPTION: the quotes must not sit there
    desc_hits = [q for _, q in QUOTES if section_of(secs, idx[text.find(q)] if text.find(q) >= 0 else 0) == "DESCRIPTION"]
    rec("quote.not-in-DESCRIPTION", not desc_hits, ";".join(desc_hits) or "none")

    try:
        src = open(a.sources, encoding="utf-8").read().splitlines()
    except OSError as e:
        print(f"sources\tcannot-evaluate\t{e}"); return 2
    cand = [l for l in src if re.match(rf"^\| {re.escape(a.id)} \|", l)]
    s149 = [l for l in src if re.match(r"^\| S149 \|", l)]
    if len(cand) != 1 or len(s149) != 1:
        print(f"row\tcannot-evaluate\t{a.id} rows={len(cand)} S149 rows={len(s149)}"); return 2
    row = cand[0]
    cells = [c.strip() for c in row.strip().strip("|").split("|")]
    rec("row.fields==11", len(cells) == 11, str(len(cells)))
    if len(cells) == 11:
        sid, source, kind, tier, scope, anchor, teaches, status, opened, recheck, usedby = cells
        rec("row.kind-docs", kind == "docs", kind)
        rec("row.tier-C", tier == "C", tier)
        rec("row.status-rejected", status == "rejected", status)
        rec("row.url", URL in source, "present" if URL in source else "absent")
        rec("row.teaches-supersedes-S149", teaches.startswith("supersedes S149 \u2014"), teaches[:40])
        rec("row.teaches-REJECTED", "REJECTED:" in teaches, "REJECTED:" in teaches and "yes" or "no")
        rec("row.teaches-flip", "flip:" in teaches, "flip:" in teaches and "yes" or "no")
        for want_sec, quote in QUOTES:
            rec(f"row.anchor.{want_sec}", f"`{want_sec}`" in anchor and f"\"{quote}\"" in anchor,
                f"heading and quote in anchor")
        rec("row.anchor.sha256", SNAP_SHA in anchor, "sha256 cited" if SNAP_SHA in anchor else "missing")
    rec("row.s149-url-equal", URL in s149[0], "S149 row carries the same URL")

    print("check\tresult\tdetail")
    for c, r, d in rows:
        print(f"{c}\t{r}\t{d}")
    print(f"summary\t{'ok' if fails == 0 else 'fail'}\tfailed={fails}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
