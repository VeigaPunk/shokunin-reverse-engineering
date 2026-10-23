#!/usr/bin/env python3
"""Round-31 independent oracle for REA `inspect-sqlite-database --schema-scope database`.

Two readers, neither of them REA code:

* `read_schema_rows(path)` parses the SQLite file format directly in Python
  (header, table b-tree pages of page 1, overflow chains, record format) and
  returns every sqlite_schema row (rowid, type, name, tbl_name, rootpage, sql)
  in b-tree key order, plus the header text encoding.  No SQLite library code.
* The system libsqlite3 (Python stdlib `sqlite3`, a different build from the
  SQLite that node bundles for REA) supplies `PRAGMA table_list` (kind, ncol,
  without_rowid, strict) and `PRAGMA table_xinfo` (columns), opened read-only
  and immutable so the file is never written.

`expected_report(path)` combines them into the shape of REA's
`normalized_result` for scope `database`, minus `engine.version`,
`limitations` and `rows` (which the counters drop from REA's side as well).
The library's own sqlite_schema rows must equal the byte parser's rows, or
the oracle raises.
"""

import hashlib
import os
import sqlite3
import struct

ENCODINGS = {1: "UTF-8", 2: "UTF-16le", 3: "UTF-16be"}
PY_CODEC = {"UTF-8": "utf-8", "UTF-16le": "utf-16-le", "UTF-16be": "utf-16-be"}


class OracleError(Exception):
    pass


def _varint(b, i):
    v = 0
    for k in range(8):
        c = b[i + k]
        v = (v << 7) | (c & 0x7F)
        if c < 0x80:
            return v, i + k + 1
    return (v << 8) | b[i + 8], i + 9


_INT_SIZES = {1: 1, 2: 2, 3: 3, 4: 4, 5: 6, 6: 8}


def _record(payload, codec):
    hs, i = _varint(payload, 0)
    types = []
    while i < hs:
        t, i = _varint(payload, i)
        types.append(t)
    pos = hs
    out = []
    for t in types:
        if t == 0:
            out.append(None)
        elif t in _INT_SIZES:
            n = _INT_SIZES[t]
            out.append(int.from_bytes(payload[pos:pos + n], "big", signed=True))
            pos += n
        elif t == 7:
            out.append(struct.unpack(">d", payload[pos:pos + 8])[0])
            pos += 8
        elif t == 8:
            out.append(0)
        elif t == 9:
            out.append(1)
        elif t >= 12 and t % 2 == 0:
            n = (t - 12) // 2
            out.append(bytes(payload[pos:pos + n]))
            pos += n
        elif t >= 13:
            n = (t - 13) // 2
            out.append(bytes(payload[pos:pos + n]).decode(codec))
            pos += n
        else:
            raise OracleError("reserved serial type %d" % t)
    return out


def read_header(data):
    if data[:16] != b"SQLite format 3\x00":
        raise OracleError("not a SQLite 3 file")
    ps = int.from_bytes(data[16:18], "big")
    ps = 65536 if ps == 1 else ps
    if ps < 512 or ps & (ps - 1):
        raise OracleError("invalid page size %d" % ps)
    enc = ENCODINGS.get(int.from_bytes(data[56:60], "big"))
    if enc is None:
        raise OracleError("invalid text encoding")
    return ps, ps - data[20], enc


def read_schema_rows(path):
    data = open(path, "rb").read()
    ps, usable, enc = read_header(data)
    codec = PY_CODEC[enc]
    rows = []
    seen = set()

    def page(n):
        if n < 1 or n * ps > len(data) or n in seen:
            raise OracleError("bad page %d" % n)
        return data[(n - 1) * ps:n * ps]

    def walk(n):
        p = page(n)
        seen.add(n)
        off = 100 if n == 1 else 0
        kind = p[off]
        ncell = int.from_bytes(p[off + 3:off + 5], "big")
        hdr = 12 if kind in (2, 5) else 8
        ptrs = [int.from_bytes(p[off + hdr + 2 * k:off + hdr + 2 * k + 2], "big") for k in range(ncell)]
        if kind == 5:
            for c in ptrs:
                walk(int.from_bytes(p[c:c + 4], "big"))
            walk(int.from_bytes(p[off + 8:off + 12], "big"))
        elif kind == 13:
            for c in ptrs:
                size, i = _varint(p, c)
                rowid, i = _varint(p, i)
                x = usable - 35
                if size <= x:
                    payload = p[i:i + size]
                else:
                    m = ((usable - 12) * 32 // 255) - 23
                    k = m + ((size - m) % (usable - 4))
                    local = k if k <= x else m
                    payload = bytearray(p[i:i + local])
                    ov = int.from_bytes(p[i + local:i + local + 4], "big")
                    while len(payload) < size:
                        if not ov:
                            raise OracleError("overflow chain ends early")
                        op = data[(ov - 1) * ps:ov * ps]
                        payload += op[4:4 + min(usable - 4, size - len(payload))]
                        ov = int.from_bytes(op[0:4], "big")
                rec = _record(payload, codec)
                if len(rec) != 5:
                    raise OracleError("sqlite_schema record has %d fields" % len(rec))
                rows.append((rowid,) + tuple(rec))
        else:
            raise OracleError("page %d is not a table b-tree page (type %d)" % (n, kind))

    walk(1)
    return enc, rows


def _fold(name):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in name)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def expected_report(path):
    enc, rows = read_schema_rows(path)
    con = sqlite3.connect("file:%s?mode=ro&immutable=1" % path, uri=True)
    try:
        lib_rows = [tuple(r) for r in con.execute(
            "SELECT rowid, type, name, tbl_name, rootpage, sql FROM main.sqlite_schema")]
        if sorted(lib_rows) != sorted(rows):
            raise OracleError("byte parser and libsqlite3 disagree on sqlite_schema")
        listed = {}
        for schema, name, typ, ncol, wr, strict in con.execute("PRAGMA main.table_list"):
            if schema == "main":
                listed[name] = (typ, ncol, wr, strict)
        unresolved = [n for n, v in listed.items() if v[0] == "virtual" and v[1] == 0]
        tables, indexes, views, triggers = [], [], [], []
        for _rowid, typ, name, tbl, root, sql in rows:
            if typ == "table":
                lt = listed.get(name)
                if lt is None or lt[0] == "view":
                    raise OracleError("table %s missing from table_list" % name)
                parent = None
                if lt[0] == "table":
                    parent = next((u for u in unresolved if _fold(name).startswith(_fold(u + "_"))), None)
                virtual = lt[0] == "virtual"
                cols = []
                if not virtual:
                    for cid, cname, ctype, notnull, dflt, pk, hidden in con.execute(
                            "PRAGMA main.table_xinfo(\"%s\")" % name.replace('"', '""')):
                        cols.append({"cid": cid, "name": cname, "declared_type": ctype,
                                     "not_null": notnull != 0, "default_sql": dflt,
                                     "primary_key_position": pk, "hidden": hidden})
                tables.append({
                    "name": name, "sql": sql, "root_page": root,
                    "kind": lt[0] if parent is None else "unknown",
                    "without_rowid": lt[2] != 0, "strict": lt[3] != 0,
                    "column_count": None if (virtual and lt[1] == 0) else lt[1],
                    "columns_completeness": "unsupported" if virtual else "complete",
                    "columns": cols,
                })
            elif typ == "index":
                indexes.append({"name": name, "table": tbl, "sql": sql, "root_page": root})
            elif typ == "view":
                views.append({"name": name, "sql": sql})
            else:
                folded = {_fold(n): n for n in listed}
                target = tbl if tbl in listed else folded.get(_fold(tbl), tbl)
                triggers.append({"name": name, "table": target, "sql": sql})
    finally:
        con.close()
    wal = path + "-wal"
    return {
        "artifact": {"path": path, "sha256": sha256_file(path), "bytes": os.path.getsize(path)},
        "wal": None if not os.path.lexists(wal) else "present",
        "engine": {"name": "SQLite"},
        "database_encoding": enc,
        "schema": {"scope": "database", "completeness": "complete", "tables": tables,
                   "indexes": indexes, "views": views, "triggers": triggers},
        "rows": None,
    }


def comparable(normalized_result):
    """REA's normalized_result reduced to the oracle's fields (drops engine.version, limitations)."""
    r = dict(normalized_result)
    r.pop("limitations", None)
    eng = dict(r.get("engine") or {})
    eng.pop("version", None)
    r["engine"] = eng
    return r


if __name__ == "__main__":
    import json
    import sys
    for p in sys.argv[1:]:
        rep = expected_report(os.path.abspath(p))
        s = rep["schema"]
        print(json.dumps({"path": p, "encoding": rep["database_encoding"], "tables": len(s["tables"]),
                          "indexes": len(s["indexes"]), "views": len(s["views"]),
                          "triggers": len(s["triggers"]),
                          "columns": sum(len(t["columns"]) for t in s["tables"])}))
