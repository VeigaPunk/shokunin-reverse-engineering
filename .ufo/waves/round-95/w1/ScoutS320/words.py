import re, html
q = "If the trailing component (i.e., basename) of path is a symbolic link, then the open fails, with the error ELOOP"
print("WORDS", len(q.split()))
print("CHARS", len(q))
# also check case where path is italic -> after tag strip becomes "path"
