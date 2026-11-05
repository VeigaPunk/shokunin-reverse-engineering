#!/usr/bin/env python3
"""In-process sweep of repair() for exception types that escape the CLI's
`except (Refuse, struct.error)` clause. 20000 mutants across the three packs."""
import collections
import importlib.util
import json
import random
import struct
import time

TOOL = "/fast/scratch/hyaku/kaidoku-r99/SentinelInputs/clone/tools/round-99/upx-pe-repair.py"
PACKS = ["/fast/scratch/hyaku/kaidoku-r99/SentinelInputs/packs/%s.upx" % n
         for n in ("t32", "w64", "freeglut32dll")]
spec = importlib.util.spec_from_file_location("upxrepair", TOOL)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

rng = random.Random(0xC0FFEE)
escaped = collections.Counter()
examples = {}
outcomes = collections.Counter()
worst = (0.0, None)
N = 20000
for it in range(N):
    data = bytearray(open(PACKS[it % 3], "rb").read())
    mode = it % 4
    if mode == 0:  # uniform flips anywhere
        for _ in range(rng.randint(1, 16)):
            data[rng.randrange(len(data))] = rng.randrange(256)
    elif mode == 1:  # flips in first 1 KiB (headers)
        for _ in range(rng.randint(1, 8)):
            data[rng.randrange(min(1024, len(data)))] = rng.randrange(256)
    elif mode == 2:  # random 32-bit field write at random offset in header area
        off = rng.randrange(0, min(1024, len(data) - 4))
        struct.pack_into("<I", data, off, rng.choice([0, 1, 0xFFFF, 0xFFFFFFFF, rng.randrange(1 << 32)]))
    else:  # random truncation plus flips
        data = data[:rng.randrange(0, len(data))]
        if data:
            data[rng.randrange(len(data))] = rng.randrange(256)
    t0 = time.perf_counter()
    try:
        m.repair(bytes(data))
        outcomes["ok"] += 1
    except (m.Refuse, struct.error) as e:
        outcomes["refuse:" + (str(e).split(":")[0] or type(e).__name__)] += 1
    except Exception as e:  # escapes CLI handler
        key = type(e).__name__ + ": " + str(e)[:60]
        escaped[key] += 1
        examples.setdefault(key, {"iter": it, "mode": mode, "len": len(data)})
    dt = time.perf_counter() - t0
    if dt > worst[0]:
        worst = (dt, it)
print(json.dumps({"iterations": N, "outcomes": outcomes.most_common(), "escaped": escaped.most_common(),
                  "examples": examples, "worst_repair_secs": round(worst[0], 5), "worst_iter": worst[1]},
                 indent=1))
