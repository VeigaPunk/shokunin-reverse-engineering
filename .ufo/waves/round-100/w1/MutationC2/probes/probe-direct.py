import importlib.util, sys
S = "/fast/scratch/hyaku/kaidoku-r100/MutationC2"
def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
base = load("base", S + "/orig.py")
muts = {i: load("m" + i, S + "/mut/%s.py" % i) for i in ["M05", "M06", "M09", "M11", "M19", "M22", "M23", "M10"]}
probes = [
  ("claim", "12 casesX"),          # M05: \b dropped
  ("claim", "two selftest cases=3 and 12 cases"),  # M06 last-match: both alternatives present
  ("claim", "15 cases at A, 16 from B"),           # selftest's own first-wins input
  ("claim", "15 cases then 16 cases"),             # two real matches
  ("claim", "3 cases at A, 9 cases at B"),
]
for kind, text in probes:
    print(kind, repr(text), "base=", base.parse_claim(text), *["%s=%s" % (i, m.parse_claim(text)) for i, m in muts.items() if i in ("M05", "M06")])
for text in ["ver1.45/45 cases", "x 45/45 cases", "45/45 cases"]:
    print("obs", repr(text), "base=", base.parse_observed(text, ""), "M09=", muts["M09"].parse_observed(text, ""))
for out, err in [("cases=2", "cases=9"), ("", "cases=9"), ("cases=4", "")]:
    print("obs-stream", repr(out), repr(err), "base=", base.parse_observed(out, err), "M11=", muts["M11"].parse_observed(out, err))
print("claim-cell M19 4-cell row:", muts["M19"].claim_cell(["`t.py`", "tool with cases=12", "0=ok", "green, exit 0"]), "| base:", base.claim_cell(["`t.py`", "tool with cases=12", "0=ok", "green, exit 0"]))
print("claim M19 parse:", base.parse_claim(base.claim_cell(["`t.py`", "tool with cases=12", "0=ok", "green, exit 0"])), muts["M19"].parse_claim(muts["M19"].claim_cell(["`t.py`", "tool with cases=12", "0=ok", "green, exit 0"])))
rtext = "x\n%s\n| `a.py` | g | 0=ok | `--selftest` 4 cases |\n| `a.py` | g | 0=ok | 9 cases |\n%s\n" % (base.START, base.END)
print("M22 dup rows: base dup=", base.registry_rows(rtext)[1], "M22 rows[a]=", muts["M22"].registry_rows(rtext)[0]["`a.py`".strip("`")] if False else muts["M22"].registry_rows(rtext)[0]["a.py"])
dbl = "x\n%s\n| `a.py` | g | 0=ok | 1 cases |\n%s\n%s\n| `b.py` | g | 0=ok | 2 cases |\n%s\n" % (base.START, base.END, base.START, base.END)
try:
    print("doubled: base", base.registry_rows(dbl)); 
except ValueError as e: print("doubled: base refuses:", e)
try:
    print("doubled: M23", muts["M23"].registry_rows(dbl))
except ValueError as e: print("doubled: M23 refuses:", e)
