import json, os, sys
ROOT="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.abspath("toolsB/round-47")); sys.path.insert(0, os.path.abspath("toolsB/round-46"))
import gate, record
assert record.__file__.startswith(os.path.abspath("toolsB")), record.__file__
REV=sys.argv[1]; tip=gate.resolve(ROOT,REV)
card0=gate.show(ROOT,tip,"SCORECARD.md"); emit=lambda p: gate.show(ROOT,tip,p)
def run(name, card):
    code,rec=record.evaluate_text(card, emit, ROOT, tip, battery=None)
    print(json.dumps({"name":name,"exit":code,"failing":rec.get("failing"),
                      "corr":rec.get("corrections"),
                      "axes":[ (m["key"],m["derived"]) for m in rec.get("mismatches",[]) if m["class"]=="axes"]}))
run("B1-real-card", card0)
run("B2-score-3.14-4.20", card0.replace("| coverage | 9.72 → 10.0 |","| coverage | 3.14 → 4.20 |",1))
run("B3-depth-0.00-1.00", card0.replace("| depth | 10 → 10 |","| depth | 0.00 → 1.00 |",1))
run("B4-out-of-range", card0.replace("| coverage | 9.72 → 10.0 |","| coverage | 42.0 → 99.9 |",1))
run("B5-current-below", card0.replace("| coverage | 9.72 → 10.0 |","| coverage | 9.72 → 8.40 |",1))
run("B6-baseline-wrong", card0.replace("| coverage | 9.72 → 10.0 |","| coverage | 9.70 → 10.0 |",1))
run("B7-fraction-in-score-column", card0.replace("| coverage | 9.72 → 10.0 | 138/138 knowledge files mapped","| coverage | 138/138 | 0/138 knowledge files mapped",1))
run("B8-fraction-137", card0.replace("138/138 knowledge files mapped","137/138 knowledge files mapped",1))
run("B9-row-relabelled", card0.replace("| coverage |","| Coverage |",1))
