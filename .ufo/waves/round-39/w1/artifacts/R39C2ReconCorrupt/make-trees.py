#!/usr/bin/env python3
"""Rebuild the four dev trees used by the R39-C2 corruption recon (deterministic).

usage: python3 make-trees.py <root>   -> <root>/{ta,tb,tc,td}
Then:  python3 tools/round-37/gen-squashfs.py <root>/ta out/ta-be-gzip.sqsh --endian be --comp gzip
"""
import os
import sys


def mk(root, name, files, dirs=()):
    base = os.path.join(root, name)
    for d in dirs:
        os.makedirs(os.path.join(base, d), exist_ok=True)
    for rel, data in files.items():
        path = os.path.join(base, rel)
        os.makedirs(os.path.dirname(path) or base, exist_ok=True)
        with open(path, "wb") as f:
            f.write(data)
    return base


def main(root):
    mk(root, "ta", {
        "etc/config.txt": b"alpha=1\nbeta=2\n" * 40,
        "bin/tool": bytes(range(256)) * 8,
        "readme": b"fresh tree A for round-39 c2 recon\n",
    }, dirs=["etc", "bin"])
    mk(root, "tb", {
        "usr/share/data.bin": bytes((i * 7) % 251 for i in range(9000)),
        "usr/lib/notice.txt": b"notice\n" * 300,
        "root.cfg": b"B\n" * 10,
    }, dirs=["usr", "usr/share", "usr/lib"])
    mk(root, "tc", {
        "opt/app/lib/mod.py": b'print("hello")\n' * 500,
        "opt/app/etc/a.conf": b"k=v\n" * 7000,
        "top.dat": bytes(range(256)) * 40,
    }, dirs=["opt", "opt/app", "opt/app/lib", "opt/app/etc"])
    td = mk(root, "td", {"etc/main.conf": b"key=value\n" * 30}, dirs=["etc", "var"])
    os.symlink("../etc/main.conf", os.path.join(td, "var", "notice-link"))
    os.symlink("../../../../etc/shadow", os.path.join(td, "var", "escape-link"))


if __name__ == "__main__":
    main(sys.argv[1])
