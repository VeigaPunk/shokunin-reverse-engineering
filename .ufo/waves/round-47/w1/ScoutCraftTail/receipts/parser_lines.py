import sys
lines = sys.stdin.read().splitlines()
keys = ("CRAFT = ", "MARKER = ", "def craft_section", "def blocks_of", "block_is_last", "block.startswith")
for i, l in enumerate(lines, 1):
    if any(k in l for k in keys):
        print(f"{i}:{l}")
