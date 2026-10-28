
import hashlib, re, subprocess, sys
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
REV = "5017e1f7299c3a812e87e7950148f54313dd279e"
blob = subprocess.check_output(["git", "-C", ROOT, "show", f"{REV}:SKILL.md"])
text = blob.decode("utf-8")
lines = text.splitlines()
print(f"newline_terminated={text.endswith(chr(10))}")
print(f"splitlines={len(lines)}")
print(f"content_sha256={hashlib.sha256(blob).hexdigest()}")
print(f"blob_bytes={len(blob)}")
craft_idx = [i for i,l in enumerate(lines) if l.startswith("## Queue-drain craft")]
print(f"craft_heading_count={len(craft_idx)}")
for i in craft_idx:
    print(f"CRAFT_HEAD {i+1}|{lines[i]}")
# next ## after craft
if craft_idx:
    start = craft_idx[0]
    nxt = None
    for j in range(start+1, len(lines)):
        if lines[j].startswith("## "):
            nxt = j
            break
    print(f"NEXT_H2 {nxt+1}|{lines[nxt]}" if nxt is not None else "NEXT_H2 none")
else:
    nxt = None
# file-wide dash-bold
dash = [i for i,l in enumerate(lines) if re.match(r"^- \*\*", l)]
print(f"dash_bold_file={len(dash)}")
craft_dash = [i for i in dash if craft_idx and (nxt is None or craft_idx[0] < i < nxt)]
print(f"dash_bold_craft={len(craft_dash)}")
print("---CRAFT_BLOCKS---")
for n,i in enumerate(craft_dash, 1):
    end = (craft_dash[n] if n < len(craft_dash) else (nxt-1 if nxt is not None else len(lines)-1))
    prefix = lines[i][:60]
    print(f"BLOCK {n} start={i+1} end={end+1} chars60={prefix!r}")
print("---FILE_DASH_OUTSIDE_CRAFT---")
for i in dash:
    if i not in craft_dash:
        print(f"OUT {i+1}|{lines[i][:60]!r}")
print("---REGISTRY---")
for i,l in enumerate(lines):
    if "instrument-registry" in l or "exactness-table" in l:
        print(f"MARK {i+1}|{l!r}")
if craft_dash and nxt is not None:
    last = craft_dash[-1]
    print("---LAST_BLOCK_NEIGHBOURS---")
    for i in range(max(0, nxt-3), min(len(lines), nxt+2)):
        print(f"NEI {i+1}|{lines[i]!r}")
    print(f"INSERT_BEFORE_LINE={nxt+1}")
    print(f"LAST_BLOCK_RANGE={last+1}-{nxt}")  # inclusive end is line before heading = nxt (1-based nxt is heading, so end is nxt)
# 1-based heading line number is nxt+1; last included line of section is nxt (1-based) because heading is nxt+1
print("---EXACT_SPLIT---")
CRAFT = "## Queue-drain craft "
body = text.split(CRAFT, 1)[1].split("\n## ", 1)[0]
blocks = re.split(r"(?m)^- \*\*", body)[1:]
print(f"exact_py_rule_blocks={len(blocks)}")
print(f"last_block_startswith_23={blocks[-1].startswith('23. ')}")
print(f"last_block_title60={blocks[-1][:60]!r}")
print(f"marker_v3_count={text.count('<!-- exactness-table v3 -->')}")
