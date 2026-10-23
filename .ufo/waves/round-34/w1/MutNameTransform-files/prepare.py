#!/usr/bin/env python3
"""Create one bounded ASCII/NUL comparator fixture; never read ELF inputs."""
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
FREEZE = "54a87a51a865ab931fd355e767303337b05cccf4"
COUNTER = ROOT / "tools/round-34/version-needs-counter.py"


def store(name, data):
    if isinstance(data, str):
        data = data.encode("ascii")
    if len(data) > 65536:
        raise ValueError("fixture_write_bound")
    path = BASE / name
    if path.exists():
        raise ValueError("setup_already_exists:" + name)
    path.write_bytes(data)
    return {"path": name, "size": len(data), "sha256": hashlib.sha256(data).hexdigest()}


alphabet = sorted(b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_.-")
table = b"".join(b"p" + bytes([letter]) + b"\0" for letter in alphabet)
versions = [
    {"name": chr(letter), "flags": 0, "other": 2 + index, "hash": 0xF1230000 + index * 17}
    for index, letter in enumerate(alphabet)
]
needed = [
    {"file": "p" + chr(letter), "versions": versions if index == 0 else []}
    for index, letter in enumerate(alphabet)
]
expected = {"schema": 1, "needed": needed}
version_fields = ";".join(
    f"{index * 3 + 1},0,{version['other']},{version['hash']}"
    for index, version in enumerate(versions)
)
rows = [f"{index * 3}|" + (version_fields if index == 0 else "") for index in range(len(alphabet))]
header = b"\0".join([b"TEXT-R34-NUL-1", str(len(alphabet)).encode(), str(len(table)).encode(), *(row.encode() for row in rows)]) + b"\0\0"
data = header + table + b"TEXT-END\0"
if len(data) > 4096 or any(byte > 127 for byte in data):
    raise ValueError("text_fixture_bound")
records = [store("fixture.txt", data), store("expected.json", json.dumps(expected, sort_keys=True) + "\n")]
spec = {
    "target": 1,
    "documents_ok": True,
    "manifest": {
        "schema": 1,
        "carriers": [{
            "id": "nul-suffix-sort-hash",
            "path": "fixture.txt",
            "size": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "expected": expected,
            "string_table": {"offset": len(header), "size": len(table)},
        }],
    },
}
records.append(store("spec.json", json.dumps(spec, sort_keys=True) + "\n"))
reader = '''#!/usr/bin/env python3
"""Read only the supplied bounded ASCII/NUL text bytes, not an ELF parser."""
import json
from pathlib import Path
import sys

data = Path(sys.argv[1]).read_bytes()
assert len(data) <= 4096 and all(byte < 128 for byte in data)
header, payload = data.split(b"\\0\\0", 1)
fields = header.split(b"\\0")
assert fields[0] == b"TEXT-R34-NUL-1"
count, table_size = map(int, fields[1:3])
assert len(fields[3:]) == count and count <= 65
table = payload[:table_size]
assert payload[table_size:] == b"TEXT-END\\0"

def name(offset):
    assert 0 <= offset < len(table)
    return table[offset:table.index(0, offset)].decode("ascii")

needed = []
for row in fields[3:]:
    file_offset, encoded_versions = row.split(b"|", 1)
    versions = []
    for item in encoded_versions.split(b";") if encoded_versions else []:
        offset, flags, other, recorded_hash = map(int, item.split(b","))
        versions.append({"name": name(offset), "flags": flags, "other": other, "hash": recorded_hash})
    versions.sort(key=lambda value: (value["name"], value["other"]))
    needed.append({"file": name(int(file_offset)), "versions": versions})
needed.sort(key=lambda value: value["file"])
print(json.dumps({"schema": 1, "needed": needed}, sort_keys=True))
'''
records.append(store("byte_reader.py", reader))
replay = '''#!/usr/bin/env python3
"""Skip-work control: original content-hash lookup only, no name decoding."""
import hashlib
import json
from pathlib import Path
import sys

original = %r
expected = %r
observed_hash = hashlib.sha256(Path(sys.argv[1]).read_bytes()).hexdigest()
print(json.dumps(expected if observed_hash == original else {"schema": 1, "needed": []}, sort_keys=True))
''' % (hashlib.sha256(data).hexdigest(), expected)
records.append(store("original_hash_replay.py", replay))
records.append(store("counter.pristine.py", COUNTER.read_bytes()))
env = {key: value for key, value in os.environ.items() if not key.startswith(("GIT_", "PYTHON"))}
argv = ["git", "--no-replace-objects", "-C", str(ROOT), "rev-parse", "HEAD"]
started = datetime.now(timezone.utc).isoformat()
run = subprocess.run(argv, env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
if run.returncode or run.stdout.decode().strip() != FREEZE:
    raise ValueError("unexpected_sandbox_revision")
receipt = {
    "observed_utc": started,
    "argv": argv,
    "stdout": run.stdout.decode(),
    "stderr": run.stderr.decode(),
    "exit": run.returncode,
    "root": str(ROOT),
    "freeze_revision": FREEZE,
    "measured_revision": run.stdout.decode().strip(),
    "fixture": {"bytes": len(data), "table_offset": len(header), "table_size": len(table), "needed_records": len(needed), "versions": len(versions), "suffix_aliases": len(alphabet)},
    "files": records,
    "python_version": sys.version,
}
store("setup.json", json.dumps(receipt, sort_keys=True, indent=2) + "\n")
print(json.dumps(receipt, sort_keys=True))
