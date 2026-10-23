#!/usr/bin/env python3
"""Archive only this seat's bounded receipts, without invoking any reader."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
ROOT = BASE.parents[4]
DEST = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-34/w1/MutNameTransform-files")
COUNTER = ROOT / "tools/round-34/version-needs-counter.py"
original = (BASE / "counter.pristine.py").read_bytes()
current = COUNTER.read_bytes()
restored_snapshot = (BASE / "counter.restored.snapshot.py").read_bytes()
assert current == original == restored_snapshot, "restoration_not_exact"
assert hashlib.sha256(current).hexdigest() == "d7f0a8cf3ca08562437d40711d15e7ad4f6fa44edb4e8934c36f4673e4e7c45e"
files = ["prepare.py", "detector.py", "archive.py", "mutation.patch", "fixture.txt", "expected.json", "spec.json", "byte_reader.py", "original_hash_replay.py", "counter.pristine.py", "setup.json"]
for phase in ("pristine", "mutated", "restored"):
    files += [phase + ".json", "counter." + phase + ".snapshot.py"]
    for label in ("byte", "replay"):
        files += [phase + "." + label + suffix for suffix in (".stdout.json", ".stderr.txt", ".schedule1.txt")]
contents = {name: (BASE / name).read_bytes() for name in files}
assert all(len(data) <= 524288 for data in contents.values())
assert sum(map(len, contents.values())) <= 1048576
DEST.mkdir(parents=True, exist_ok=True)
assert not any((DEST / name).exists() for name in [*files, "archive-receipt.json"]), "archive_destination_already_exists"
records = []
for name, data in contents.items():
    path = DEST / name
    path.write_bytes(data)
    archived = path.read_bytes()
    assert archived == data
    records.append({"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "exact_archived_bytes": True})
receipt = {
    "observed_utc": datetime.now(timezone.utc).isoformat(),
    "argv": sys.orig_argv,
    "source": str(BASE),
    "destination": str(DEST),
    "measured_revision": "54a87a51a865ab931fd355e767303337b05cccf4",
    "restoration": {"working_counter": str(COUNTER), "pristine_equals_restored_snapshot_equals_working_bytes": True, "bytes": len(current), "sha256": hashlib.sha256(current).hexdigest()},
    "files": records,
    "outer_commands": [
        "timeout --signal=TERM --kill-after=2s 20s prlimit --as=536870912 --nproc=4096 --cpu=10 python3 -I -B .ufo/waves/round-34/w1/MutNameTransform-files/prepare.py",
        *["timeout --signal=TERM --kill-after=2s 70s prlimit --as=536870912 --nproc=4096 --cpu=25 python3 -I -B .ufo/waves/round-34/w1/MutNameTransform-files/detector.py " + phase for phase in ("pristine", "mutated", "restored")],
        "timeout --signal=TERM --kill-after=2s 15s prlimit --as=536870912 --nproc=4096 --cpu=10 python3 -I -B .ufo/waves/round-34/w1/MutNameTransform-files/archive.py",
    ],
    "detector_outer_exit_codes": {"pristine": 0, "mutated": 1, "restored": 0},
    "no_installs_or_updates": True,
}
encoded = (json.dumps(receipt, sort_keys=True, indent=2) + "\n").encode("ascii")
assert len(encoded) <= 65536
(BASE / "archive-receipt.json").write_bytes(encoded)
(DEST / "archive-receipt.json").write_bytes(encoded)
print(json.dumps({"destination": str(DEST), "files": len(records), "archived_bytes": sum(map(len, contents.values())), "restoration": receipt["restoration"], "observed_utc": receipt["observed_utc"]}, sort_keys=True))
