#!/usr/bin/env python3
"""Print numbered lines of a vendor info file with tab characters escaped.

usage: excerpt.py <url-or-path> <line> [<line> ...]

Used by R41SrcAvm to quote the AVM info_en.txt / info_de.txt identity block
without committing the vendor file. Each output line is:
    L<lineno>\t<raw line with TAB rendered as \\t>
so a reader can check the quote and its line number against the fetched bytes
(sha256 recorded in avm-http-probe.tsv).
"""
import sys
import urllib.request

src = sys.argv[1]
want = [int(x) for x in sys.argv[2:]]
if src.startswith(("http://", "https://")):
    with urllib.request.urlopen(src, timeout=60) as r:
        data = r.read()
else:
    with open(src, "rb") as f:
        data = f.read()
# The vendor info files are ISO-8859-1, not UTF-8: `data.decode("utf-8")` raises
# on the first accented byte (5490 info_en.txt byte 17974, info_de.txt byte 44).
lines = data.decode("latin-1").split("\n")
for n in want:
    print("L%d\t%s" % (n, lines[n - 1].replace("\t", "\\t")))
