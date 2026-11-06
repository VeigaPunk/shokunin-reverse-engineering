import os, sys
S = "/fast/scratch/hyaku/kaidoku-r100/MutationC2"
src = open(os.path.join(S, "orig.py"), encoding="utf-8").read()
M = [
 ("M01", "CLAIM_RE alt1: drop leading lookbehind", r'(?<![\w./-])(\d+)(?:/\d+)?\s+(?:selftest', r'(\d+)(?:/\d+)?\s+(?:selftest'),
 ("M02", "CLAIM_RE alt1: drop optional /N denominator", r'(\d+)(?:/\d+)?\s+', r'(\d+)\s+'),
 ("M03", "CLAIM_RE alt1: drop optional 'selftest' word", r'(?:selftest\s+)?cases', r'cases'),
 ("M04", "CLAIM_RE alt2: drop lookbehind on cases=N", r'|(?<![\w-])cases[=: ]+(\d+)")', r'|cases[=: ]+(\d+)")'),
 ("M05", "CLAIM_RE alt1: drop trailing \\b after cases", r'(?:selftest\s+)?cases\b|', r'(?:selftest\s+)?cases|'),
 ("M06", "parse_claim: last match instead of first", '    m = CLAIM_RE.search(cell)', '    ms = list(CLAIM_RE.finditer(cell))\n    m = ms[-1] if ms else None'),
 ("M07", "parse_claim: group(2) branch dropped", 'int(m.group(1) or m.group(2))', 'int(m.group(1))'),
 ("M08", "OBS_RE alt1: drop lookbehind (showcases)", r'OBS_RE = re.compile(r"(?<![\w-])cases', r'OBS_RE = re.compile(r"cases'),
 ("M09", "OBS_RE alt2: drop lookbehind on N/N cases", r'(?<![\w./-])(\d+)/\d+ cases', r'(\d+)/\d+ cases'),
 ("M10", "parse_observed: first match instead of last", 'g = ms[-1].groups()', 'g = ms[0].groups()'),
 ("M11", "parse_observed: stderr searched before stdout", 'for text in (stdout, stderr):', 'for text in (stderr, stdout):'),
 ("M12", "parse_observed: bool guard removed", 'if isinstance(c, bool):', 'if False:'),
 ("M13", "parse_observed: list branch off by one", 'return len(c)', 'return len(c) - 1'),
 ("M14", "parse_observed: JSON branch disabled", '    if isinstance(j, dict):', '    if isinstance(j, dict) and False:'),
 ("M15", "run_row ok: agree conjunct dropped", 'rec["counted"] is not None, rec["agree"]))', 'rec["counted"] is not None))'),
 ("M16", "run_row ok: pin_ok conjunct dropped", 'rec["ok"] = all((rec["row"], rec["pin_ok"],', 'rec["ok"] = all((rec["row"],'),
 ("M17", "run_row: duplicate-row gate dropped", 'rec["row"] = cells is not None and path not in dup', 'rec["row"] = cells is not None'),
 ("M18", "run_row: pin compares presence, not equality", 'rec["pin_ok"] = got == pins', 'rec["pin_ok"] = all(v is not None for v in got.values())'),
 ("M19", "claim_cell: 4-cell rows joined with preceding cells", 'return cells[3] if len(cells) >= 4 else', 'return cells[3] if len(cells) >= 5 else'),
 ("M20", "registry_rows: any pipe line taken as a row", 'if not line.startswith("| `"):', 'if not line.startswith("|"):'),
 ("M21", "registry_rows: duplicate detection removed", '            dup.add(path)', '            pass'),
 ("M22", "registry_rows: first-wins on duplicates (equivalent by gate)", '        rows[path] = cells', '        rows.setdefault(path, cells)'),
 ("M23", "registry_rows: doubled START marker tolerated", 'if text.count(START) != 1 or', 'if text.count(START) < 1 or'),
 ("M24", "main: met = label prefix only", 'met = label == TARGET', 'met = label.startswith("rows 93")'),
 ("M25", "label_of: mismatches = rows - agree", '    m = sum(not x["ok"] for x in recs)', '    m = r - a'),
 ("M26", "run_row: exit 1 counted green", 'rec["green"] = rc == 0', 'rec["green"] = rc in (0, 1)'),
 ("M27", "run_row: stderr dropped from counting", 'rec["counted"] = parse_observed(out, err)', 'rec["counted"] = parse_observed(out, "")'),
 ("M28", "label_of: counted = agree (label arithmetic)", '    k = sum(x["counted"] is not None for x in recs)', '    k = sum(x["agree"] for x in recs)'),
 ("M29", "label_of: green via rc (equivalent)", '    g = sum(x["green"] for x in recs)', '    g = sum(x["rc"] == 0 for x in recs)'),
 ("M30", "run_row ok: claimed-not-None conjunct dropped (equivalent)", 'rec["claimed"] is not None, rec["green"],', 'rec["green"],'),
 ("M31", "run_row ok: green conjunct dropped", 'rec["claimed"] is not None, rec["green"],', 'rec["claimed"] is not None,'),
 ("M32", "claim_cell: short-row text drops first cell (tool text)", 'return " | ".join(cells[1:])', 'return " | ".join(cells[2:])'),
]
os.makedirs(os.path.join(S, "mut"), exist_ok=True)
for mid, desc, old, new in M:
    n = src.count(old)
    if n != 1:
        print("SKIP %s count=%d %s" % (mid, n, desc)); continue
    out = src.replace(old, new, 1)
    if out == src:
        print("NOOP", mid); continue
    open(os.path.join(S, "mut", mid + ".py"), "w", encoding="utf-8").write(out)
    print("OK", mid, desc)
