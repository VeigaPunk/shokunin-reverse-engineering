#!/usr/bin/env python3
"""Read-only tar member lister for remote AVM images via HTTP Range reads.

Walks 512-byte ustar/GNU headers with Range requests and never downloads
member data. Writes TSV rows (url, index, typeflag, name, size, data_offset)
to stdout. No request or response headers are stored; only the Content-Range
total length of the first response is printed to stderr.
"""
import sys
import urllib.request
import urllib.error


def get(url, start, end):
    req = urllib.request.Request(url)
    req.add_header("Range", "bytes=%d-%d" % (start, end))
    with urllib.request.urlopen(req, timeout=60) as r:
        cr = r.headers.get("Content-Range", "")
        return r.status, r.read(), cr


def octal(b):
    s = b.split(b"\0")[0].strip()
    return int(s or b"0", 8)


def walk(url, max_members=400):
    off = 0
    rows = []
    long_name = None
    total = None
    for _ in range(max_members):
        try:
            status, hd, cr = get(url, off, off + 511)
        except urllib.error.HTTPError as e:
            return rows, "HTTP %d at offset %d" % (e.code, off), total
        if total is None and "/" in cr:
            total = cr.rsplit("/", 1)[1]
        if len(hd) < 512 or hd == b"\0" * 512:
            return rows, "end-of-archive at %d" % off, total
        typeflag = chr(hd[156]) if hd[156] else "0"
        size = octal(hd[124:136])
        name = hd[0:100].split(b"\0")[0].decode("utf-8", "replace")
        prefix = hd[345:500].split(b"\0")[0].decode("utf-8", "replace")
        if prefix and hd[257:262] == b"ustar":
            name = prefix + "/" + name
        data_off = off + 512
        if typeflag == "L":
            # GNU long name: data block holds the real name of the next entry.
            _, data, _ = get(url, data_off, data_off + size - 1)
            long_name = data.split(b"\0")[0].decode("utf-8", "replace")
        else:
            if long_name is not None:
                name, long_name = long_name, None
            rows.append((url, len(rows), typeflag, name, size, data_off))
        off = data_off + ((size + 511) // 512) * 512
    return rows, "max_members reached", total


def main(urls):
    print("url\tindex\ttypeflag\tname\tsize\tdata_offset")
    for url in urls:
        rows, stop, total = walk(url)
        sys.stderr.write("%s total=%s members=%d stop=%s\n" % (url, total, len(rows), stop))
        for r in rows:
            print("\t".join(str(x) for x in r))


if __name__ == "__main__":
    main(sys.argv[1:])
