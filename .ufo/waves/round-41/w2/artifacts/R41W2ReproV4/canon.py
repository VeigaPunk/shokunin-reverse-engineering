#!/usr/bin/env python3
"""Path-normalised structural diff between V4 after-receipts.

Absolute scratch paths (subject.local_path, parameters.path, output_directory,
files[].path, diagnostic links, evidence_id) are receipt-specific; everything
else should be identical if both receipts came from the same bytes and
toolchain. Reports every JSON path that differs after normalisation.
"""
import json
import sys

PATH_KEYS = {"local_path", "path", "output_directory", "link", "evidence_id",
             "executable_path"}


def norm(obj, env, tag):
    """Replace receipt-specific strings with placeholders, in place."""
    nr = env.get("normalized_result") or {}
    od = (env.get("parameters") or {}).get("output_directory") or ""
    local = ((env.get("subject") or {}).get("local_path")) or ""
    subs = [s for s in (od, local) if s]
    # rea staging dir: <scratch>/rea-firmware-XXXXXX/extracted/<cr>/...
    import re
    rea = re.compile(r"/[^/]*/rea-firmware-[A-Za-z0-9]+/extracted")

    def walk(x, p):
        if isinstance(x, dict):
            out = {}
            for k, v in x.items():
                if k in PATH_KEYS and isinstance(v, str):
                    out[k] = "<" + k + ">"
                elif k == "duration" or k == "start_utc" or k == "end_utc":
                    out[k] = "<" + k + ">"
                else:
                    out[k] = walk(v, p + "/" + k)
            return out
        if isinstance(x, list):
            return [walk(v, p + "/[]") for v in x]
        if isinstance(x, str):
            s = x
            for sub in subs:
                s = s.replace(sub, "<receipt-root>")
            s = rea.sub("/<scratch>/rea-firmware-XXXXXX/extracted", s)
            if s.startswith("/fast/scratch/hyaku/kaidoku-r41/"):
                s = "<scratch>/" + s.split("/fast/scratch/hyaku/kaidoku-r41/", 1)[1]
            return s
        return x

    return walk(obj, "")


def diff(a, b, p="", out=None):
    if out is None:
        out = []
    if type(a) is not type(b):
        out.append((p, "type " + type(a).__name__ + " vs " + type(b).__name__))
        return out
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                out.append((p + "/" + k, "only in b"))
            elif k not in b:
                out.append((p + "/" + k, "only in a"))
            else:
                diff(a[k], b[k], p + "/" + k, out)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            out.append((p, "len %d vs %d" % (len(a), len(b))))
        for i, (x, y) in enumerate(zip(a, b)):
            diff(x, y, p + "[%d]" % i, out)
        return out
    if a != b:
        out.append((p, repr(a)[:120] + " vs " + repr(b)[:120]))
    return out


def main():
    a = json.load(open(sys.argv[1]))
    b = json.load(open(sys.argv[2]))
    na = norm(a, a, "a")
    nb = norm(b, b, "b")
    d = diff(na, nb)
    print("differences:", len(d))
    for p, why in d[:40]:
        print(" ", p, "->", why)


if __name__ == "__main__":
    main()
