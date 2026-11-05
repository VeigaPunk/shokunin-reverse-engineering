import json, os, shutil, sys
SRC, F = sys.argv[1], sys.argv[2]
def load(case):
    d = os.path.join(F, case); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for n in ("pos","F1","F2","F3"):
        for e in ("json","stdout","stderr","rc"):
            shutil.copy(os.path.join(SRC, f"c1-v4-{n}.{e}"), os.path.join(d, f"c1-v4-{n}.{e}"))
    return d
def rj(d, n): return json.load(open(os.path.join(d, f"c1-v4-{n}.json")))
def wj(d, n, r): json.dump(r, open(os.path.join(d, f"c1-v4-{n}.json"), "w"), indent=1, sort_keys=True)
def ws(d, n, s): open(os.path.join(d, f"c1-v4-{n}.stdout"), "w").write(s)
def wrc(d, n, s): open(os.path.join(d, f"c1-v4-{n}.rc"), "w").write(s)
def stdout_with(line_old, line_new, d, n):
    t = open(os.path.join(d, f"c1-v4-{n}.stdout")).read(); ws(d, n, t.replace(line_old, line_new))
cases = {}
# A: receipt label only (stdout untouched) for F1
d = load("A_receipt_label_only_F1"); r = rj(d,"F1"); r["label"] = "repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2"; wj(d,"F1",r); cases["A_receipt_label_only_F1"]=d
# B: stdout label only for F1
d = load("B_stdout_label_only_F1"); stdout_with("repaired 10 of 12", "repaired 12 of 12", d, "F1"); cases["B_stdout_label_only_F1"]=d
# C: receipt met_target True only for F1
d = load("C_receipt_met_only_F1"); r = rj(d,"F1"); r["met_target"] = True; wj(d,"F1",r); cases["C_receipt_met_only_F1"]=d
# D: met flipped True in receipt AND stdout for F1 (exit still 1)
d = load("D_met_both_F1"); r = rj(d,"F1"); r["met_target"] = True; wj(d,"F1",r); stdout_with("met False exit 1","met True exit 1", d, "F1"); cases["D_met_both_F1"]=d
# E: exit flipped to 0 in receipt+stdout+rc for F1 (met False)
d = load("E_exit_all_F1"); r = rj(d,"F1"); r["exit"]=0; wj(d,"F1",r); stdout_with("met False exit 1","met False exit 0", d, "F1"); wrc(d,"F1","0\n"); cases["E_exit_all_F1"]=d
# F: rc file only changed for F1
d = load("F_rc_only_F1"); wrc(d,"F1","0\n"); cases["F_rc_only_F1"]=d
# G: F3 receipt truncated
d = load("G_truncated_F3"); t=open(os.path.join(d,"c1-v4-F3.json")).read(); open(os.path.join(d,"c1-v4-F3.json"),"w").write(t[:700]); cases["G_truncated_F3"]=d
# H: label rewritten consistently to frozen label for F1 (receipt + stdout), met False exit 1
d = load("H_label_rewritten_both_F1"); r = rj(d,"F1"); r["label"]="repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2"; wj(d,"F1",r)
ws(d,"F1","repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met False exit 1"); cases["H_label_rewritten_both_F1"]=d
# J: pos receipt+stdout say met True exit 0 but label reports 0 of 12 (verdict-label contradiction)
d = load("J_pos_label_contradicts_met"); r = rj(d,"pos"); r["label"]="repaired 0 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 0 of 12; fresh-roundtrip 0 of 2"; wj(d,"pos",r)
ws(d,"pos","repaired 0 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 0 of 12; fresh-roundtrip 0 of 2 met True exit 0"); cases["J_pos_label_contradicts_met"]=d
# K: receipt 'expect' rewritten (frozen label not checked by agreement counter)
d = load("K_expect_rewritten_F1"); r = rj(d,"F1"); r["expect"]="anything"; wj(d,"F1",r); cases["K_expect_rewritten_F1"]=d
# control: untouched copy
d = load("00_control_unaltered"); cases["00_control_unaltered"]=d
for k, d in sorted(cases.items()):
    print(k, json.dumps(d))
