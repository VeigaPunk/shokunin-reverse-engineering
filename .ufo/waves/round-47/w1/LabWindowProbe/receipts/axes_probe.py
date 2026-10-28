import json,sys,os
LANE="/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0,os.path.join(LANE,"tools","round-47")); sys.path.insert(0,os.path.join(LANE,"tools","round-46"))
import gate, record
REV=sys.argv[1]; tip=gate.resolve(LANE,REV)
card=gate.show(LANE,tip,"SCORECARD.md"); files=lambda p: gate.show(LANE,tip,p)
# what the counter parses as corrections
corr,_=record.corrections(card)
out={"rev":tip,"card_correct_lines":[l.strip() for l in card.splitlines() if l.strip().startswith("- corrects ")],
     "parsed_corrections":[{"class":c["class"],"key":c["key"]} for c in corr]}
def run(name,text):
    code,rec=record.evaluate_text(text,files,LANE,tip,battery=None)
    bat=record.run_battery(text,files,LANE,tip) if code in (0,1) else None
    code,rec=record.evaluate_text(text,files,LANE,tip,battery=bat) if bat else (code,rec)
    out.setdefault("cases",[]).append({"case":name,"exit":code,"failing":rec.get("failing"),
        "corrections_bad":rec.get("corrections_bad"),"corrections":rec.get("corrections")})
run("control",card)
# a false axes correction: rendered text, parsed nowhere
bad=card.replace("- corrects axes coverage: 138/138","- corrects axes coverage: 1/1")
run("axes-correction-false-1/1",bad)
ghost=card.replace("- corrects axes coverage: 138/138","- corrects axes does-not-exist: 1/1")
run("axes-correction-nonexistent-axis",ghost)
print(json.dumps(out,indent=1))
