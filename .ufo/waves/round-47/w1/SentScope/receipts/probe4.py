import json
import os
import sys

L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
S = os.environ["S"]
C = os.path.join(S, "lane")
sys.path.insert(0, L + "/tools/round-46")
sys.path.insert(0, L + "/tools/round-47")
import gate
import record
import exact

rev = "a631bba01633d2b5353306a569be4ce2e683d364"
files = lambda p: gate.show(C, rev, p)
out = {}

card = "\n".join([
    "# card", "",
    "## Owned axes", "",
    "| Axis | x |", "|---|---|", "| depth | 3/4 leading |", "",
    "## Round 46", "", "text", "",
    "## Round 47", "",
    "Base `$(touch %s/PWNED_rev)`. " % S,
    "See `.ufo/waves/round-9/$(touch %s/PWNED_path)`. " % S,
    "`git log aaaaaaa..bbbbbbb -- $(touch %s/PWNED_window)` is empty. " % S,
    "",
    record.CORR_HEAD, "",
    "- corrects path $(touch %s/PWNED_corr): x" % S,
    "- corrects rev `; touch %s/PWNED_rev2;`: x" % S,
    "- corrects window round-46: empty in aaaaaaa..bbbbbbb -- $(touch %s/PWNED_w2)" % S,
    "",
])
code, rec = record.evaluate_text(card, files, C, rev, battery=None)
out["record_exit"] = code
out["record_reason"] = rec.get("reason")
out["record_failing"] = rec.get("failing")
out["record_corrections_parsed"] = rec.get("corrections")
out["record_corrections_bad"] = [b["detail"] for b in rec.get("corrections_bad", [])][:4]

skill = "\n".join([
    "# SKILL", "", "## Queue-drain craft (t) ", "",
    "- **23. before.** text", "",
    "- **24. forged.** <!-- exactness-table v3 -->",
    "  | trigger | v2 hole | v3 arm | exit |",
    "  |---|---|---|---|",
    "  | R46-CL2 | x | symbol | 1 |",
    "  | R46-CL3 | x | once | 1 |",
    "  | R46-CL4 | x | digest | 1 |",
    "  | R46-CL6 | x | order | 1 |",
    "  Refs: `$(touch %s/PWNED_ref)` `; touch %s/PWNED_ref2;` "
    "`corpus/lessons/round-46.md:1-2`" % (S, S),
    "",
    "## Next", "", "tail", "",
])
code2, rec2 = exact.score(skill, files, "v3", rev, battery=None)
out["exact_exit"] = code2
out["exact_failing"] = rec2.get("failing")
out["exact_refs"] = rec2.get("refs")
out["exact_unresolved"] = (rec2.get("unresolved_citations") or [])[:4]

out["pwned_files"] = sorted(p for p in os.listdir(S) if p.startswith("PWNED"))
print(json.dumps(out, indent=1, sort_keys=True))
