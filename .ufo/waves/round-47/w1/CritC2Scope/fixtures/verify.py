#!/usr/bin/env python3
"""CritC2Scope consolidated matrix: scope sizes, dodge fixtures, corrections reach.

Usage: verify.py <REV> [<BASE_REV>]
Every case goes through record.evaluate_text (the counter's own entry point) with the
same `files`/root the CLI uses, so nothing here is a re-implementation.
"""
import hashlib
import json
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-47")
sys.path.insert(0, LANE + "/tools/round-46")
import record  # noqa: E402

REV = sys.argv[1]
BASE = sys.argv[2] if len(sys.argv) > 2 else "13a9e9e1"


def files(rev):
    def f(path):
        r = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"],
                           capture_output=True, text=True)
        return None if r.returncode != 0 else r.stdout
    return f


out = {"rev": REV, "counter_sha256": hashlib.sha256(
    open(LANE + "/tools/round-47/record.py", "rb").read()).hexdigest()}

for tag, rev in (("rev", REV), ("base", BASE)):
    F = files(rev)
    CARD = F("SCORECARD.md")
    secs = record.sections(CARD)
    heads = [(m.start(), m.group(1)) for m in re.finditer(r"(?m)^## (\S+)", CARD)]
    round_heads = [(m.start(), m.group(1)) for m in
                   re.finditer(r"(?m)^## Round (\d+)", CARD)]
    in_scope_lines = 0
    for pos, rnd in round_heads[-2:]:
        end = CARD.find("\n## ", pos + 1)
        in_scope_lines += CARD[:end if end >= 0 else len(CARD)].count("\n") - \
            CARD[:pos].count("\n")
    axes_body = CARD.split("## Owned axes", 1)[1].split("\n## ", 1)[0]
    total_lines = CARD.count("\n")
    atoms = []
    for rnd, text in secs:
        atoms.extend(record.collect(text, rnd, F, LANE, rev))
    all_atoms = 0
    outside = 0
    for pos, rnd in round_heads:
        end = CARD.find("\n## ", pos + 1)
        n = len(record.collect(CARD[pos:end if end >= 0 else len(CARD)], rnd, F, LANE, rev))
        all_atoms += n
        if rnd not in [r for r, _ in secs]:
            outside += n
    # atoms in round-like sections whose heading does not match ^## Round \d+
    other_round_atoms = 0
    for i, (pos, title) in enumerate([(m.start(), m.group(1)) for m in
                                      re.finditer(r"(?m)^## (.+)$", CARD)]):
        nxt = [p for p, _ in [(m.start(), m.group(1)) for m in
                              re.finditer(r"(?m)^## (.+)$", CARD)] if p > pos]
        end = min(nxt) if nxt else len(CARD)
        if re.match(r"(luna-|arc[23]-|Post-review)", title):
            other_round_atoms += len(record.collect(CARD[pos:end], "0", F, LANE, rev))
    out[tag] = {
        "total_lines": total_lines,
        "level2_sections": len(heads),
        "round_matching_headings": len(round_heads),
        "round_like_non_matching_sections":
            sum(1 for _, t in [(m.start(), m.group(1)) for m in
                               re.finditer(r"(?m)^## (.+)$", CARD)]
                if re.match(r"(luna-|arc[23]-|Post-review)", t)),
        "sections_in_scope": [r for r, _ in secs],
        "in_scope_section_lines": in_scope_lines,
        "owned_axes_body_lines": axes_body.count("\n"),
        "in_scope_lines": in_scope_lines + axes_body.count("\n"),
        "in_scope_line_fraction": round((in_scope_lines + axes_body.count("\n"))
                                       / total_lines, 4),
        "atoms_section_scope": len(atoms),
        "atoms_all_round_matching": all_atoms,
        "atoms_round_matching_outside_scope": outside,
        "atoms_round_like_non_matching": other_round_atoms,
        "collectible_atoms_card_wide": all_atoms + other_round_atoms,
        "in_scope_share_of_collectible": round(
            (len(atoms) + 2) / (all_atoms + other_round_atoms), 4),
        "corrects_lines": sum(1 for l in CARD.splitlines()
                              if l.strip().startswith("- corrects")),
        "corrects_parsed": len(record.corrections(CARD)[0]),
    }

# --- fixtures at REV -----------------------------------------------------------------
F = files(REV)
CARD = F("SCORECARD.md")
secs = dict((r, t) for r, t in record.sections(CARD))
newest, prev = [r for r, _ in record.sections(CARD)][-1], [r for r, _ in record.sections(CARD)][-2]
T_PREV, T_NEW = secs[prev], secs[newest]
cases = {}


def run(name, card, battery=False):
    code, rec = record.evaluate_text(card, F, LANE, REV,
                                     battery=record.run_battery(card, F, LANE, REV)
                                     if battery else None)
    cases[name] = {
        "exit": code,
        "sections": rec.get("sections"),
        "atoms": rec.get("atoms"),
        "mismatches": [m["atom"][:70] for m in rec.get("mismatches", [])],
        "exempted": len(rec.get("exempted", [])),
        "corrections": rec.get("corrections"),
        "failing": rec.get("failing") or rec.get("reason"),
        "receipt_sha256": hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest(),
    }
    return code, rec


# find a rev atom in the older in-scope section to corrupt
m = re.search(r"`([0-9a-f]{7,40})`", T_PREV)
if not m:
    raise SystemExit("no rev atom in the older in-scope section")
corrupt = "`deadbee" + m.group(1)[7:] + "`"
T_BAD = T_PREV.replace(m.group(0), corrupt, 1)
CARD_BAD = CARD.replace(T_PREV, T_BAD, 1)
assert CARD_BAD != CARD

run("A0_clean", CARD, battery=True)
run("A1_corrupt_older_section_rev", CARD_BAD)
run("A2_corrupt_plus_bare_duplicate_heading",
    CARD_BAD + f"\n## Round {prev} — duplicate heading\n")          # one line, no body
run("A3_corrupt_plus_fenced_heading",
    CARD_BAD + "\n```markdown\n## Round 99 — example\n```\n")        # not a document section
run("A4_corrupt_plus_self_excluded_heading",
    CARD_BAD + f"\n## r{int(newest) + 1} — record, measured at `{corrupt.strip('`')}`\n\n"
              f"Waves: 900 + 900 = 1800 seats\n")
run("A5_corrupt_plus_new_round_section",
    CARD_BAD + f"\n## Round {int(newest) + 1} — record, measured at `{corrupt.strip('`')}`\n\n"
              f"Waves: 900 + 900 = 1800 seats\n")
run("A6_two_empty_new_sections",
    CARD + f"\n## Round {int(newest) + 1} — nothing\n\n-\n"
           f"\n## Round {int(newest) + 2} — nothing\n\n-\n")
# corrections reach: a false axes head with an axes correction line
if "| coverage |" in CARD and re.search(r"\| coverage \|[^\n]*?(\d+)/(\d+)", CARD):
    mm = re.search(r"\| coverage \|([^\n]*)", CARD)
    frac = re.search(r"\d+/\d+", mm.group(1))
    a, b = frac.group(0).split("/")
    bogus = f"{int(a) - 1}/{b}"
    reg = CARD.replace(frac.group(0), bogus, 1)
    run("B0_coverage_head_regressed", reg)
    run("B1_coverage_regressed_with_axes_correction",
        reg + f"\n- corrects axes coverage: {bogus}\n")
run("C0_axes_correction_lines_deleted",
    "\n".join(l for l in CARD.splitlines()
              if not l.strip().startswith("- corrects axes")) + "\n")

out["cases"] = cases
print(json.dumps(out, indent=1))
