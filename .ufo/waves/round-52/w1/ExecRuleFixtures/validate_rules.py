#!/usr/bin/env python3
"""Read-only v1 grammar probe for the adjacent round-52 rule JSON files.

The R50 parser rejects the R52 claim label; normalize that field in memory only,
then invoke the actual v1 gap_rule_model for every other grammar clause.
"""
import importlib.util
import json
import pathlib
import sys

seat = pathlib.Path(__file__).resolve().parent
counter = pathlib.Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("r50_counter", counter)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
problems = []
for path in sorted(seat.glob("*.json")):
    if path.name == "M2-fourteenth.receipt.json":
        continue
    raw = path.read_bytes()
    try:
        doc = json.loads(raw)
    except Exception as exc:
        problems.append(f"{path.name}: JSON parse: {exc}")
        continue
    original_claim = doc.get("claim")
    if original_claim not in ("R50-C1", "R52-C1"):
        problems.append(f"{path.name}: unexpected claim {original_claim!r}")
        continue
    doc["claim"] = "R50-C1"
    model, errors = module.gap_rule_model(json.dumps(doc).encode())
    if errors:
        problems.append(f"{path.name}: {errors}")
    else:
        print(f"{path.name}: v1 grammar OK (claim normalized in-memory; {original_claim})")
if problems:
    print("\n".join(problems), file=sys.stderr)
    raise SystemExit(1)
