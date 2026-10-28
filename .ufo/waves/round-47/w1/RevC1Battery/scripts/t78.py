import json, sys
sys.path.insert(0, "/fast/scratch/hyaku/kaidoku-r47/RevC1Battery")
import attack as A
base = A.show(A.FREEZE, A.SELF)
t7 = base.replace('def _m_flag_order(block, spec):\n    return block, {GATE46: ("gate_order_swapped", None)}',
                  'def _m_flag_order(block, spec):\n    raise RuntimeError("boom")')
assert t7 != base
t8 = base.replace('def _m_substring_arm(block, spec):\n    rows = [r[:2] + ["order-ish"] + r[3:] for r in _rows(block)]\n    return rewrite_rows(block, rows), {}',
                  'def _m_substring_arm(block, spec):\n    return block + "\\n  Note: cosmetic only.\\n", {}')
assert t8 != base
out = {}
for tag, src in (("T7-mutation-raises", t7), ("T8-cosmetic-change", t8)):
    lane, f1, f2 = A.build_lane(tag, src)
    rec = A.counter(tag, lane, f1, f2)
    s = A.summary(rec); out[tag] = s
    print(tag, "exit=%s" % s["exit"], "failing=%s" % (s["failing"] or s["reason"]), s["battery"], flush=True)
json.dump(out, open("runs/summary-T78.json", "w"), indent=1)
