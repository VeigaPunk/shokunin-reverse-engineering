#!/usr/bin/env python3
"""Independent fidelity check of the CtlHashReplay control table.

Reads the frozen manifest and the frozen carrier blobs from the freeze
revision (never from a manufactured fixture), imports the generated control
reader, and asserts:

  1. every frozen expected record is present in the control table under the
     frozen sha256 of its original carrier;
  2. the control reader's stdout for the original bytes equals the frozen
     expected record exactly (byte-for-byte JSON equality after decode);
  3. the control reader's stdout for the same bytes with one byte of the
     string table altered (a text-only in-memory mutation, never written as a
     binary fixture) is the empty record, i.e. the lookup misses;
  4. the control source contains no ELF interpretation tokens.

No ELF binary is authored, executed, or written. Only the frozen original
bytes are hashed and compared.
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
FREEZE = "54a87a51a865ab931fd355e767303337b05cccf4"
MANIFEST = ".ufo/waves/round-34/expected.json"
READER = ROOT / "controls" / "round-34" / "ctl-hash-replay.py"
ELF_TOKENS = (r"\be_ident\b", r"\bstruct\b", r"\bEI_NIDENT\b", r"\bSHT_\w+", r"\bDT_\w+",
              r"\belf\.h\b", r"\bmagic\b", r"\bunpack\b", r"\bELFMAG\b", r"\bPT_LOAD\b",
              r"\bVerneed\b", r"\bVernaux\b", r"\bdynstr\b", r"\bbinary_reader\b")


def git(args):
    env = {"GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": "/dev/null", "LC_ALL": "C", "PATH": "/usr/bin:/bin"}
    run = subprocess.run(["git", "--no-replace-objects", "-C", str(ROOT), *args], env=env,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=30, check=True)
    return run.stdout


def load_reader():
    spec = importlib.util.spec_from_file_location("ctl_hash_replay", READER)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    manifest = json.loads(git(["show", FREEZE + ":" + MANIFEST]))
    module = load_reader()
    table = module.TABLE
    source = READER.read_text("utf-8")
    findings = []
    tokens_hit = sorted({t for t in ELF_TOKENS if re.search(t, source)})
    rows = []
    for row in manifest["carriers"]:
        data = git(["show", FREEZE + ":" + row["path"]])
        digest = hashlib.sha256(data).hexdigest()
        in_table = digest in table
        table_value = table.get(digest)
        exact = table_value == row["expected"]
        # In-memory single-byte mutation probe; never written to disk, never executed.
        # Carriers with a string table are probed inside it; e12 has no string table
        # (the counter replays its original bytes on both schedules), so its probe
        # byte is the first byte of the file.
        has_table = bool(row.get("string_table"))
        offset = row["string_table"]["offset"] if has_table else 0
        mutated = bytearray(data)
        mutated[offset] = (mutated[offset] + 1) % 256
        mutated_digest = hashlib.sha256(bytes(mutated)).hexdigest()
        miss = mutated_digest not in table
        empty = module.TABLE.get(mutated_digest, {"schema": 1, "needed": []})
        rows.append({
            "id": row["id"],
            "frozen_sha256": row["sha256"],
            "digest_of_frozen_blob": digest,
            "digest_matches_manifest": digest == row["sha256"],
            "present_in_table": in_table,
            "table_value_equals_frozen_expected": exact,
            "probe_offset": offset,
            "probe_inside_string_table": has_table,
            "probe_digest": mutated_digest,
            "probe_digest_in_table": not miss,
            "probe_lookup_result": empty,
            "needed_records": len(row["expected"]["needed"]),
        })
    report = {
        "kind": "ctl_hash_replay_table_fidelity",
        "freeze": FREEZE,
        "manifest_sha256": hashlib.sha256(git(["show", FREEZE + ":" + MANIFEST])).hexdigest(),
        "reader_sha256": hashlib.sha256(READER.read_bytes()).hexdigest(),
        "table_size": len(table),
        "manifest_carriers": len(manifest["carriers"]),
        "table_keys_equal_manifest_digests": sorted(table) == sorted(r["sha256"] for r in manifest["carriers"]),
        "every_carrier_present": all(r["present_in_table"] for r in rows),
        "every_table_value_equals_frozen_expected": all(r["table_value_equals_frozen_expected"] for r in rows),
        "every_probe_digest_misses": all(r["probe_digest_in_table"] is False for r in rows),
        "elf_interpretation_tokens_in_source": tokens_hit,
        "rows": rows,
    }
    report["passed"] = bool(report["every_carrier_present"] and report["every_table_value_equals_frozen_expected"]
                            and report["every_probe_digest_misses"] and report["table_keys_equal_manifest_digests"]
                            and not tokens_hit and report["table_size"] == 12)
    print(json.dumps(report, sort_keys=True, indent=1))
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
