#!/usr/bin/env python3
"""R43LabTuple probe: run observed_features() from the base-committed
tools/round-42/heldout-gen-v4.py against the committed round-42 C02 run.json
record. Read-only: the module is imported from a `git show` copy in scratch;
no lane writes, no REA run."""
import importlib.util
import json
import sys

GEN = "/fast/scratch/hyaku/kaidoku-r43/w1-R43LabTuple/heldout-gen-v4.py"
RUN = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
       "corpus/evidence/round-42/c2/heldout/C02/run.json")
MANIFEST = ("/home/vgpnk/Projects/shokunin/kaidoku-shokunin/"
            "corpus/evidence/round-42/c2/heldout/manifest.json")

spec = importlib.util.spec_from_file_location("heldout_gen_v4", GEN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

record = json.load(open(RUN))
manifest = json.load(open(MANIFEST))
entry = [c for c in manifest["carriers"] if c["id"] == "C02"][0]

observed = mod.observed_features(record)
expected = mod.expected_for(entry)
diff = mod.feature_diff(expected, observed)

six = ("handler_set", "gap_kinds", "gap_dependencies", "symlink_removed",
       "published", "be_argv")

print("== module ==", GEN)
print("module file:", mod.__file__)
print("observed_features is:", mod.observed_features.__code__.co_filename,
      "line", mod.observed_features.__code__.co_firstlineno)
print()
print("== observed six-field tuple (observed_features on C02 run.json record) ==")
print(json.dumps({k: observed[k] for k in six}, indent=2, sort_keys=True))
print()
print("== declared six-field tuple (manifest declared_features) ==")
print(json.dumps({k: entry["declared_features"][k] for k in six},
                 indent=2, sort_keys=True))
print()
print("== extras ==")
print("declared_extras:", json.dumps(entry["declared_extras"], sort_keys=True))
print("observed extras: extraction_failed=%r max_depth=%r"
      % (observed["extraction_failed"], observed["max_depth"]))
print()
print("== feature_diff(expected_for(entry), observed) ==")
for line in diff:
    print(" ", line)
print()
print("diff field count:", len(diff))
gap_want = set(entry["declared_features"]["gap_kinds"])
gap_got = set(observed["gap_kinds"])
print("gap_kinds declared-only:", sorted(gap_want - gap_got))
print("gap_kinds observed-only:", sorted(gap_got - gap_want))
sys.exit(0)
