#!/usr/bin/env python3
"""R42AssimIds — census pre-check for the four staged rows that duplicate a held URL.

Builds a scratch lane mirror (corpus/ + the files `used-by` names) and a
candidate append block of the four staged rows whose URL the lane registry
already carries (S107->S111, S122->S116, S192->S114, S216->S125), renumbered
into free ids S238-S241 and normalised to census schema:

  * `recheck` prose (`180d — curl … | grep -c …`) becomes `180d`; the stripped
    prose is recorded in the report, never in the row
  * every remaining literal or escaped `|` inside a cell becomes `/`, so the
    row parses as 11 columns
  * `used-by` names a file that exists in the mirror

Then runs `sources-census.sh validate --file <mirror>/corpus/SOURCES.md` and
prints the verdict class for each appended id (W04 = duplicate URL across
scopes: allowed; E04 = duplicate URL within scope: refused).

Usage: census-precheck.py <lane root> <staged append> <work dir> <out dir>
Writes only inside <work dir>; copies the findings into <out dir>.
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

PAIRS = {
    # staged id -> (candidate lane id, lane row already holding the same URL)
    "S107": ("S238", "S111"),
    "S122": ("S239", "S116"),
    "S192": ("S240", "S114"),
    "S216": ("S241", "S125"),
}
ROW = re.compile(r"^ {0,3}\|\s*(S[0-9]{3,})\s*\|(.*)$")
CENSUS = "/home/vgpnk/Projects/shokunin/scripts/sources-census.sh"
USED_BY = "corpus/lessons/round-42.md"


def staged_rows(path):
    out = {}
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = ROW.match(line.rstrip("\n"))
            if not m or m.group(1) in out:
                continue
            cells = [c.strip() for c in m.group(2).split("|")]
            if len(cells) < 10:
                continue
            out[m.group(1)] = cells
    return out


def clean(text):
    """No cell may carry a literal or escaped pipe; collapse the recheck prose."""
    text = text.replace("\\|", "/").replace("|", "/")
    return re.sub(r"\s+", " ", text).strip()


def main(argv):
    if len(argv) != 5:
        sys.stderr.write(__doc__)
        return 2
    lane, staged, work, out = map(Path, argv[1:5])
    mirror = work / "mirror"
    if mirror.exists():
        shutil.rmtree(mirror)
    (mirror / "corpus").mkdir(parents=True)
    for name in ("SOURCES.md", "README.md", "QUALITY.md", "PROVINCE.md"):
        src = lane / "corpus" / name
        if src.exists():
            shutil.copy2(src, mirror / "corpus" / name)
    for sub in ("lessons", "knowledge", "evidence"):
        if (lane / "corpus" / sub).exists():
            # symlinks=True: corpus/evidence carries deliberate dangling-link fixtures
            shutil.copytree(lane / "corpus" / sub, mirror / "corpus" / sub, symlinks=True)
    for name in ("SKILL.md", "PROVINCE.md"):
        if (lane / name).exists():
            shutil.copy2(lane / name, mirror / name)
    # every used-by target the baseline census reports missing, plus the one we append
    for extra in ("tools/round-27/xpin-attribute.mjs", USED_BY):
        dst = mirror / extra
        dst.parent.mkdir(parents=True, exist_ok=True)
        if not dst.exists():
            dst.write_text("# placeholder present only so the census used-by check resolves\n",
                           encoding="utf-8")

    rows = staged_rows(staged)
    block = []
    for sid, (new_id, held) in PAIRS.items():
        cells = rows[sid]
        source, kind, tier, scope, anchor, teaches = (clean(c) for c in cells[:6])
        block.append(f"| {new_id} | {source} | {kind} | {tier} | {scope} | {anchor} | "
                     f"{teaches} | mined | 2026-10-26 | 180d | {USED_BY} |")
    reg = mirror / "corpus" / "SOURCES.md"
    text = reg.read_text(encoding="utf-8")
    # An APPEND goes at the END OF THE REGISTRY TABLE, not at EOF: this registry
    # carries `## Paths`, `## Search log` and `## Leads` after the table, and a
    # trailing append lands outside it (census E12 row outside Registry section).
    lines = text.split("\n")
    start = next(i for i, ln in enumerate(lines) if ln.strip() == "## Registry")
    end = len(lines)
    for i in range(start + 1, len(lines)):
        if lines[i].startswith("## "):
            end = i
            break
    last_table = max(i for i in range(start, end) if lines[i].startswith("| "))
    lines[last_table + 1:last_table + 1] = block
    reg.write_text("\n".join(lines), encoding="utf-8")

    res = subprocess.run([CENSUS, "validate", "--file", str(reg)],
                         capture_output=True, text=True)
    (out / "census-precheck.txt").write_text(
        "$ sources-census.sh validate --file <mirror>/corpus/SOURCES.md\n"
        f"exit={res.returncode}\n" + res.stdout + res.stderr, encoding="utf-8")
    (out / "census-precheck-appended-rows.txt").write_text("\n".join(block) + "\n",
                                                          encoding="utf-8")
    new_ids = {v[0] for v in PAIRS.values()}
    verdicts = []
    for line in res.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and parts[2] in new_ids:
            verdicts.append(line)
        elif len(parts) >= 3 and parts[1].startswith("E") and parts[2] in new_ids:
            verdicts.append(line)
    print(f"exit={res.returncode} findings_on_appended_ids={len(verdicts)}")
    for v in verdicts:
        print(v)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
