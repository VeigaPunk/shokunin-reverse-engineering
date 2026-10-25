#!/usr/bin/env python3
"""P34-mini-records counter: the replay gate's green surface.

For every fixture the counter writes a permuted copy (name pool reordered, each
record's name_off rewritten; total size, record order and value bytes unchanged)
under an opaque temporary path, runs the reader under test on it, and compares
the decoded records with the fixture's expected records. Only a reader that
walks the record array can associate a name with its record.

Never executes fixtures; static bytes only.
"""
import argparse
import hashlib
import json
import os
import random
import struct
import subprocess
import sys
import tempfile
from pathlib import Path

PREDICATE = "P34-mini-records: eight equal-size synthetic record-chain fixtures decode to exactly their expected name/flags/value records on opaque permuted copies; only record-array traversal associates a name with its record."
HERE = Path(__file__).resolve().parent
TARGET = 8
SIZE = 512
MAGIC = b"MREC"


class Unevaluable(Exception):
    pass


def decode_fixture(data):
    if len(data) != SIZE or data[0:4] != MAGIC:
        raise Unevaluable("fixture_shape")
    version, count, records_off = struct.unpack_from("<HHI", data, 4)
    names_off = struct.unpack_from("<I", data, 12)[0]
    if version != 1 or count == 0 or records_off < 16:
        raise Unevaluable("fixture_header")
    records = []
    for index in range(count):
        base = records_off + 8 * index
        if base + 8 > names_off:
            raise Unevaluable("fixture_records_overflow")
        name_off, flags, value = struct.unpack_from("<HHI", data, base)
        records.append((name_off, flags, value))
    return records, names_off


def name_at(data, names_off, name_off):
    start = names_off + name_off
    end = data.index(b"\x00", start)
    return data[start:end].decode("ascii")


def permute(data, rng):
    """Reorder the name pool; rewrite name_off per record. Decoded output unchanged."""
    records, names_off = decode_fixture(data)
    pool = data[names_off:]
    strings = []
    offset_to_index = {}
    cursor = 0
    while cursor < len(pool):
        end = pool.index(b"\x00", cursor)
        offset_to_index[cursor] = len(strings)
        strings.append(bytes(pool[cursor:end]))
        cursor = end + 1
    order = list(range(len(strings)))
    rng.shuffle(order)
    new_pool = bytearray()
    new_offset = {}
    for index in order:
        new_offset[index] = len(new_pool)
        new_pool += strings[index] + b"\x00"
    if len(new_pool) != len(pool):
        raise Unevaluable("permute_size")
    out = bytearray(data[:names_off]) + new_pool
    for index, (name_off, _flags, _value) in enumerate(records):
        base = 16 + 8 * index
        struct.pack_into("<H", out, base, new_offset[offset_to_index[name_off]])
    return bytes(out)


def canonical(value):
    if not isinstance(value, dict) or set(value) != {"schema", "records"} or value["schema"] != 1:
        return None
    if not isinstance(value["records"], list):
        return None
    rows = []
    for record in value["records"]:
        if not isinstance(record, dict) or set(record) != {"name", "flags", "value"}:
            return None
        if not isinstance(record["name"], str) or not isinstance(record["flags"], int) or not isinstance(record["value"], int):
            return None
        rows.append({"name": record["name"], "flags": record["flags"], "value": record["value"]})
    return sorted(rows, key=lambda row: (row["name"], row["flags"], row["value"]))


def score(root, reader, seed):
    base = Path(root)
    expected_path = base / "tools/round-34/mini-fix/expected.json"
    fixtures_dir = base / "tools/round-34/mini-fix/fixtures"
    if not reader.is_file():
        raise Unevaluable("reader_absent")
    expected = json.loads(expected_path.read_text())["fixtures"]
    rng = random.Random(seed)
    rows = []
    with tempfile.TemporaryDirectory(prefix="kaidoku-r34-mini-") as work:
        for name in sorted(expected):
            source = fixtures_dir / name
            data = source.read_bytes()
            transformed = permute(data, rng)
            target = Path(work) / ("opaque-" + hashlib.sha256(transformed).hexdigest()[:20] + ".data")
            target.write_bytes(transformed)
            run = subprocess.run([sys.executable, "-I", "-B", str(reader), str(target)],
                                 capture_output=True, text=True, timeout=60,
                                 env={"PATH": "/usr/bin:/bin", "HOME": str(work)})
            observed = None
            if run.returncode == 0:
                try:
                    observed = canonical(json.loads(run.stdout))
                except (ValueError, TypeError):
                    observed = None
            want = expected[name]
            rows.append({"fixture": name, "ok": observed == want, "exit": run.returncode,
                         "transformed_sha256": hashlib.sha256(transformed).hexdigest(),
                         "input_size": len(transformed)})
    matched = sum(1 for row in rows if row["ok"])
    return {"predicate": PREDICATE, "target": TARGET, "matched": matched,
            "met_target": matched == TARGET, "rows": rows,
            "finding": "records_match" if matched == TARGET else "records_mismatch"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--control-reader", required=True)
    parser.add_argument("--seed", default="kaidoku-r34-mini-v1")
    parser.add_argument("--selftest", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        result = score(args.root, Path(args.root) / "tools/round-34/mini-fix/readers/structural.py", args.seed)
        print(json.dumps({"selftest": "structural_reader_meets_target", "matched": result["matched"],
                          "target": result["target"]}, sort_keys=True))
        return 0 if result["met_target"] else 1
    try:
        result = score(args.root, Path(args.control_reader), args.seed)
    except Exception as error:  # noqa: BLE001 - typed refusal, printed
        print(json.dumps({"predicate": PREDICATE, "met_target": False, "finding": "unevaluable:" + type(error).__name__ + ":" + str(error)}, sort_keys=True))
        return 3
    print(json.dumps(result, sort_keys=True))
    return 0 if result["met_target"] else 1


if __name__ == "__main__":
    sys.exit(main())
