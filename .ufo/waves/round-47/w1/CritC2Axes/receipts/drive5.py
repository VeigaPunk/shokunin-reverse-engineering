import json, os, sys
ROOT="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.abspath("toolsC/round-47")); sys.path.insert(0, os.path.abspath("toolsC/round-46"))
import gate, record
assert record.__file__.startswith(os.path.abspath("toolsC")), record.__file__
REV=sys.argv[1]; tip=gate.resolve(ROOT,REV)
card0=gate.show(ROOT,tip,"SCORECARD.md"); readme0=gate.show(ROOT,tip,"corpus/README.md")
emit=lambda p: gate.show(ROOT,tip,p)
def run(name, card, over=None):
    over=over or {}
    files=lambda p: over[p] if p in over else emit(p)
    code,rec=record.evaluate_text(card, files, ROOT, tip, battery=None)
    print(json.dumps({"name":name,"exit":code,"failing":rec.get("failing"),
                      "axes":[ (m["key"],m["derived"]) for m in rec.get("mismatches",[]) if m["class"]=="axes"]}))
run("C1-real-card", card0)
run("C2-row-relabelled", card0.replace("| coverage |","| Coverage |",1))
run("C3-both-relabelled", card0.replace("| coverage |","| Coverage |",1).replace("| depth |","| Depth |",1))
ghost=readme0.replace("## Coverage map\n","## Coverage map\n\n- `2026-10-27-r47-ghost-entry` ghost entry\n",1)
assert ghost!=readme0
run("C4-dangling-token", card0, {"corpus/README.md": ghost})
run("C5-score-forged", card0.replace("| coverage | 9.72 → 10.0 |","| coverage | 3.14 → 4.20 |",1))
