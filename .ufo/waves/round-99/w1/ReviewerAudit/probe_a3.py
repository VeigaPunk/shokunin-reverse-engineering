import importlib.util, os
CLONE = "/fast/scratch/hyaku/kaidoku-r99/ReviewerAudit/clone"
spec = importlib.util.spec_from_file_location("saa", os.path.join(CLONE, "tools/round-99/self-assessment-audit.py"))
saa = importlib.util.module_from_spec(spec); spec.loader.exec_module(saa)
cs = saa.load_cs()

stems = ["2026-01-01-a", "2026-01-02-b"]
state = "held — a state cell that is long enough to pass the forty char floor"
sc = ("## Owned axes\n\n| Axis | s | o | e | r |\n|---|---|---|---|---|\n"
      "| coverage | 1 → 10.0 | 2/2 knowledge files mapped | x | 99 |\n\nBaseline source revision: x\n")
sha = "a" * 64
skill = saa.REG_HEAD + "\n\n" + (
    "| `tools/round-99/t.py` | counter — R99 thing | 0=met; 1=not met; 2=usage | "
    "`--selftest` cases 3 | sha256 %s | none |\n" % sha)
tools = {"tools/round-99/t.py": sha}

# Case 1: filler-only row (20 x's) where a real description should be.
readme_filler = ("x\n## Coverage map\n\n| section | entries | state |\n|---|---|---|\n"
                 "| A | `2026-01-01-a` | %s |\n| B | `2026-01-02-b` | xxxxxxxxxxxxxxxxxxxx |\n\n## Knowledge\n" % state)
sec = cs.map_section(readme_filler)
r = saa.score(cs, stems, readme_filler, sc, skill, tools)
rec = cs.recipe_stem(stems, sec)
print("CASE1 filler-only row: mismatches=%d label=%s" % (r["mismatches"], r["label"]))
print("  r66 recipe sees it as mapped: %s/%s" % (rec["mapped"], rec["knowledge_files"]))

# Case 2: placeholder repeated ('TBD TBD ...') same question.
readme_tbd = readme_filler.replace("xxxxxxxxxxxxxxxxxxxx", "TBD TBD TBD TBD TBD TBD TBD")
r2 = saa.score(cs, stems, readme_tbd, sc, skill, tools)
print("CASE2 TBD-pad row: mismatches=%d" % r2["mismatches"])

# Case 3: stem cited in the 4th cell of an otherwise unrelated row.
readme_cell4 = ("x\n## Coverage map\n\n| section | entries | state | notes |\n|---|---|---|---|\n"
                "| A | `2026-01-01-a` | %s | filler |\n"
                "| B | rows of the other table | %s | `2026-01-02-b` |\n\n## Knowledge\n" % (state, state))
r3 = saa.score(cs, stems, readme_cell4, sc, skill, tools)
print("CASE3 stem-in-4th-cell: mismatches=%d label=%s" % (r3["mismatches"], r3["label"]))

# Case 4: row cites the entry with a corpus/ prefix (reader would call it mapped).
readme_prefix = ("x\n## Coverage map\n\n| section | entries | state |\n|---|---|---|\n"
                 "| A | `2026-01-01-a` | %s |\n| B | `corpus/knowledge/2026-01-02-b.md` | %s |\n\n## Knowledge\n" % (state, state))
sec4 = cs.map_section(readme_prefix)
r4 = saa.score(cs, stems, readme_prefix, sc, skill, tools)
rec4 = cs.recipe_stem(stems, sec4)
print("CASE4 corpus/-prefixed backtick: mismatches=%d label=%s; recipe mapped=%s/%s"
      % (r4["mismatches"], r4["label"], rec4["mapped"], rec4["knowledge_files"]))
