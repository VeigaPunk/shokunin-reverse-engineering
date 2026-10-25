#!/usr/bin/env python3
"""ExecRedReproduce: P34-mini-records-fresh counter (candidate fix for the gap).

Same predicate shape and the same reader contract as tools/round-34/mini-fix/
mini-counter.py, but the green surface is GENERATED PER RUN from a fresh seed
instead of being eight committed fixtures. Names, record counts, flags and values
are drawn at run time; expected records are computed from the generation, not read
from a public file, and the fixtures are written to opaque temporary paths.

Consequence: no memorised table can be keyed on the content, because the content
has never been published. Only record-array traversal recovers the association.

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

PREDICATE = "P34-mini-records-fresh: eight synthetic record-chain fixtures generated per run from a fresh seed decode to exactly their generated name/flags/value records on opaque paths; the association is unpublished, so only record-array traversal recovers it."
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


def generate(rng, index):
    """Fresh fixture: random name pool, random flags/values."""
    count = rng.randint(2, 6)
    names = []
    while len(names) < count:
        stem = "".join(rng.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(rng.randint(3, 12)))
        candidate = "lib" + stem + ".so." + str(rng.randint(1, 9))
        if candidate not in names:
            names.append(candidate)
    rng.shuffle(names)
    records = [(name, rng.randint(0, 3), rng.choice([0, rng.randint(0, 0xFFFFFFFF)])) for name in names]
    pool = bytearray()
    offsets = {}
    for name, _flags, _value in records:
        offsets[name] = len(pool)
        pool += name.encode("ascii") + b"\x00"
    records_off = 16
    names_off = records_off + 8 * len(records)
    if names_off + len(pool) > SIZE:
        raise Unevaluable("fixture_too_large")
    out = bytearray(SIZE)
    out[0:4] = MAGIC
    struct.pack_into("<HHI", out, 4, 1, len(records), records_off)
    struct.pack_into("<I", out, 12, names_off)
    for position, (name, flags, value) in enumerate(records):
        struct.pack_into("<HHI", out, records_off + 8 * position, offsets[name], flags, value)
    out[names_off:names_off + len(pool)] = pool
    expected = [{"name": name, "flags": flags, "value": value} for name, flags, value in
                sorted(records, key=lambda row: (row[0], row[1], row[2]))]
    return bytes(out), expected, "gen-" + str(index)


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


def score(reader, seed):
    if not reader.is_file():
        raise Unevaluable("reader_absent")
    rng = random.Random(seed)
    rows = []
    with tempfile.TemporaryDirectory(prefix="kaidoku-r34-fresh-") as work:
        for index in range(TARGET):
            data, expected, label = generate(rng, index)
            target = Path(work) / ("opaque-" + hashlib.sha256(data).hexdigest()[:20] + ".data")
            target.write_bytes(data)
            run = subprocess.run([sys.executable, "-I", "-B", str(reader), str(target)],
                                 capture_output=True, text=True, timeout=60,
                                 env={"PATH": "/usr/bin:/bin", "HOME": str(work)})
            observed = None
            if run.returncode == 0:
                try:
                    observed = canonical(json.loads(run.stdout))
                except (ValueError, TypeError):
                    observed = None
            rows.append({"fixture": label, "ok": observed == expected, "exit": run.returncode,
                         "input_size": len(data), "records": len(expected)})
    matched = sum(1 for row in rows if row["ok"])
    return {"predicate": PREDICATE, "target": TARGET, "matched": matched,
            "met_target": matched == TARGET, "rows": rows, "seed": str(seed),
            "finding": "records_match" if matched == TARGET else "records_mismatch"}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--control-reader", required=True)
    parser.add_argument("--seed", default=None)
    args = parser.parse_args()
    seed = args.seed if args.seed is not None else os.urandom(16).hex()
    try:
        result = score(Path(args.control_reader), seed)
    except Exception as error:  # noqa: BLE001 - typed refusal, printed
        print(json.dumps({"predicate": PREDICATE, "met_target": False,
                          "finding": "unevaluable:" + type(error).__name__ + ":" + str(error)},
                         sort_keys=True))
        return 3
    print(json.dumps(result, sort_keys=True))
    return 0 if result["met_target"] else 1


if __name__ == "__main__":
    sys.exit(main())
