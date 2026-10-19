#!/usr/bin/env python3
import hashlib
import importlib.util
from pathlib import Path
import re
import tempfile

repo = Path.cwd()
gate_path = repo / ".ufo/gates/c1-census-v10.py"
spec = importlib.util.spec_from_file_location("census_gate", gate_path)
gate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(gate)
source = Path.home() / ".kimi-code/config.toml"
raw = source.read_bytes()
lines = raw.splitlines(keepends=True)
locations = [(i + 1, line) for i, line in enumerate(lines) if re.search(rb"rea-agents@", line)]
occurrence_count = raw.count(b"rea-agents@")
if occurrence_count != 1 or len(locations) != 1:
    raise SystemExit(f"expected one Kimi pin occurrence; measured {occurrence_count}")
line_number, pin_line = locations[0]
print(f"source_occurrences={occurrence_count} source_pin_line={line_number} source_pin={pin_line.decode().rstrip()}")
print(f"source_pin_sha256_no_eol={hashlib.sha256(pin_line.rstrip(b'\r\n')).hexdigest()}")
print(f"source_pin_sha256_with_eol={hashlib.sha256(pin_line).hexdigest()}")

with tempfile.TemporaryDirectory(prefix="kaidoku-r9-sc2-", dir="/var/tmp") as temp:
    root = Path(temp)
    baseline = root / "baseline/.kimi-code/config.toml"
    shifted = root / "shifted/.kimi-code/config.toml"
    baseline.parent.mkdir(parents=True)
    shifted.parent.mkdir(parents=True)
    baseline.write_bytes(raw)
    eol = b"\r\n" if lines[line_number - 1].endswith(b"\r\n") else b"\n"
    shifted.write_bytes(b"".join(lines[:line_number - 1] + [b"# SC-2 hypothetical one-line config edit" + eol] + lines[line_number - 1:]))
    gate.CLIENTS["kimi"] = str(baseline)
    live = gate.live_pins()
    print(f"baseline live_kimi={live['kimi']} ptr_check@{line_number}={gate.ptr_check(str(baseline), line_number, live)}")
    gate.CLIENTS["kimi"] = str(shifted)
    shifted_live = gate.live_pins()
    shifted_raw = shifted.read_bytes()
    new_locations = [(i + 1, line) for i, line in enumerate(shifted_raw.splitlines()) if re.search(rb"rea-agents@", line)]
    shifted_occurrences = shifted_raw.count(b"rea-agents@")
    if shifted_occurrences != 1 or len(new_locations) != 1:
        raise SystemExit(f"expected one shifted Kimi pin occurrence; measured {shifted_occurrences}")
    shifted_line = new_locations[0][0]
    print(f"one-line-insertion occurrences={shifted_occurrences} new_pin_line={shifted_line} new_live_kimi={shifted_live['kimi']}")
    print(f"old_pointer@{line_number}={gate.ptr_check(str(shifted), line_number, shifted_live)}")
    print(f"reanchored_pointer@{shifted_line}={gate.ptr_check(str(shifted), shifted_line, shifted_live)}")
