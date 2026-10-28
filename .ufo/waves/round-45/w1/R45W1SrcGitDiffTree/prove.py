import hashlib, json, re, sys, datetime, pathlib
p = pathlib.Path(sys.argv[1])
raw = p.read_text(encoding='utf-8', errors='replace')
text = re.sub(r'<[^>]+>', '', raw)
text = re.sub(r'&lt;', '<', text); text = re.sub(r'&gt;', '>', text); text = re.sub(r'&amp;', '&', text)
norm = re.sub(r'\s+', ' ', text)
Q1 = "When --raw, --numstat, --name-only or --name-status has been given, do not munge pathnames and use NULs as output field terminators."
Q2 = "a tab or a NUL when -z option is used; only exists for C or R."
Q3 = "status, followed by optional \"score\" number."
Q4 = "an LF or a NUL when -z option is used, to terminate the record."
lines = raw.splitlines()
def line_of(s):
    return [i+1 for i, l in enumerate(lines) if s in l]
out = {
 "file": str(p), "bytes": len(raw.encode()), "sha256": hashlib.sha256(raw.encode()).hexdigest(),
 "utc": datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
 "checks": [],
}
for q in (Q1, Q2, Q3, Q4):
    hit = q in norm
    out["checks"].append({"quote": q, "words": len(q.split()), "present_in_normalized_text": hit,
                          "raw_html_lines_containing_fragment": line_of(q[:40]) if q[:40] in raw else line_of(q.split(' ')[0])[:1]})
ok = all(c["present_in_normalized_text"] for c in out["checks"])
out["all_present"] = ok
out["exit"] = 0 if ok else 1
print(json.dumps(out, indent=2))
sys.exit(out["exit"])
