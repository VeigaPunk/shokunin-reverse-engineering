import json, os, re, sys
ROOT="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(ROOT,"tools/round-47")); sys.path.insert(0, os.path.join(ROOT,"tools/round-46"))
import gate, record
REV=sys.argv[1]; tip=gate.resolve(ROOT,REV)
card0=gate.show(ROOT,tip,"SCORECARD.md"); assert card0
emit=lambda p: gate.show(ROOT,tip,p)
def run(name, card):
    code,rec=record.evaluate_text(card, emit, ROOT, tip, battery=None)
    print(json.dumps({"name":name,"exit":code,"failing":rec.get("failing"),
                      "axes_atoms":rec["atoms_by_class"]["axes"],
                      "mismatch_keys":[m["key"] for m in rec.get("mismatches",[])]}))
run("E10-control", card0)
# delete the coverage fraction entirely -> the atom vanishes, class still covered by depth
c=card0.replace("138/138 knowledge files mapped","all knowledge files mapped",1)
assert c!=card0; run("E10-coverage-fraction-deleted", c)
# delete the depth fraction too -> both atoms vanish -> only then red
c2=c.replace("24/24 queue-drain rule blocks","all queue-drain rule blocks",1)
assert c2!=c; run("E11-both-fractions-deleted", c2)
# relabel the coverage row (case change) -> silent drop
c3=re.sub(r"(?m)^\| coverage \|", "| Coverage |", card0, count=1)
assert c3!=card0; run("E12-row-relabelled-Coverage", c3)
# duplicate the coverage row with the true fraction but a false observable
c4=card0.replace("| coverage | 9.72 → 10.0 | 138/138 knowledge files mapped",
                 "| coverage | 9.72 → 10.0 | 0/0 knowledge files mapped",1)
assert c4!=card0; run("E13-observable-false-zero", c4)
# score arithmetic: current 138/138 => 10.0 but card claims 8.40
c5=card0.replace("| coverage | 9.72 → 10.0 |","| coverage | 9.72 → 8.40 |",1)
run("E14-score-below-derived", c5)
