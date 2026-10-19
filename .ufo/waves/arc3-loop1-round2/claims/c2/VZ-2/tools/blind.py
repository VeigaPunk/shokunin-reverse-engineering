import re, sys
src = open(sys.argv[1], encoding="utf-8").read()
for name in ("PIN", "VER", "PTR"):
    src, n = re.subn(r'(?m)^%s = re\.compile\(.*\)$' % name,
                     '%s = re.compile(r"(?!x)x")' % name, src)
    assert n == 1, (name, n)
open(sys.argv[2], "w", encoding="utf-8").write(src)
print("blind written:", sys.argv[2])
