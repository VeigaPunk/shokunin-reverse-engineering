import json, os, sys
ROOT="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(ROOT,"tools/round-47")); sys.path.insert(0, os.path.join(ROOT,"tools/round-46"))
import gate, record
assert record.__file__.startswith(os.path.join(ROOT,"tools")), record.__file__
REV=sys.argv[1]; tip=gate.resolve(ROOT,REV)
card0=gate.show(ROOT,tip,"SCORECARD.md"); emit=lambda p: gate.show(ROOT,tip,p)
def run(name, card):
    code,rec=record.evaluate_text(card, emit, ROOT, tip, battery=None)
    print(json.dumps({"name":name,"exit":code,"failing":rec.get("failing")}))
# E15: keep the fraction, replace its subject entirely -> atom still met
c=card0.replace("138/138 knowledge files mapped at the round-47 landing",
                "138/138 bytes of the moon accounted for at the round-47 landing",1)
assert c!=card0; run("E15-subject-replaced", c)
# E16: keep both fraction and text but claim the axis regressed in the score cell
c2=card0.replace("| coverage | 9.72 → 10.0 |","| coverage | 10.0 → 9.72 |",1)
run("E16-score-reversed", c2)
