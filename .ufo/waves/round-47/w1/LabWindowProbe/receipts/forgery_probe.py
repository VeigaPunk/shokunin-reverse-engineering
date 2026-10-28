import json, sys, os
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, os.path.join(LANE,"tools","round-47"))
sys.path.insert(0, os.path.join(LANE,"tools","round-46"))
import gate, record
REV=sys.argv[1]
tip=gate.resolve(LANE,REV)
card=gate.show(LANE,tip,"SCORECARD.md")
files=lambda p: gate.show(LANE,tip,p)
out={"rev":tip,"cases":[]}
def run(name, text, full=True):
    code,rec=record.evaluate_text(text,files,LANE,tip,battery=None)
    bat=None
    if full and code in (0,1):
        bat=record.run_battery(text,files,LANE,tip)
        code,rec=record.evaluate_text(text,files,LANE,tip,battery=bat)
    out["cases"].append({"case":name,"exit":code,"failing":rec.get("failing"),
        "mismatches":[m["atom"][:70] for m in rec.get("mismatches",[])],
        "corrections":rec.get("corrections"),"corrections_bad":rec.get("corrections_bad"),
        "exempted":len(rec.get("exempted",[])),
        "battery":{k:bat.get(k) for k in ("correction_forgeries","forgeries_green")} if bat else None})
CORR="- corrects window round-46: empty in %s -- tools/round-46 plans/round-46-claims.md"
run("control-as-landed", card)
for pair in ("58eb04b6..58eb04b6","332f4884..332f4884","0425224..58eb04b6"):
    text=card.replace("empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md",
                      CORR % pair)
    run("window-pair-"+pair, text)
text=card.replace("empty in 332f4884..58eb04b6 -- tools/round-46 plans/round-46-claims.md",
                  CORR % ("58eb04b6..58eb04b6")) .replace(
                  "empty in 58eb04b6..58eb04b6 -- tools/round-46 plans/round-46-claims.md",
                  "empty in 58eb04b6..58eb04b6 -- no/such/path")
run("window-pair-self+nonexistent-path", text)
run("window-correction-deleted", "\n".join(l for l in card.splitlines() if not l.startswith("- corrects window round-46")))
print(json.dumps(out, indent=1))
