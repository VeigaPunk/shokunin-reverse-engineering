import sys, pathlib
src, dst = sys.argv[1], sys.argv[2]
t = pathlib.Path(src).read_text()
i = t.index("PATH:")
head, stanza = t[:i], t[i:]
body = head + stanza * 5
pathlib.Path(dst).write_text(body)
print("built %s: PATH-stanzas=%d" % (dst, body.count("PATH:")))
