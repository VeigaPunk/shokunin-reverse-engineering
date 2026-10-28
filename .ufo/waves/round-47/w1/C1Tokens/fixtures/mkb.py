import json, sys
exec(open('drive.py').read().split("out = []")[0])
variant = sys.argv[1]
if variant == "min":
    sys.stdout.write(skill_with(block(ROWS, PROSE_MIN)))
elif variant == "full":
    sys.stdout.write(skill_with(block(ROWS, PROSE_FULL)))
elif variant == "allorder":
    rows = [tuple(r[:2]) + ("order",) + tuple(r[3:]) for r in ROWS]
    sys.stdout.write(skill_with(block(rows, PROSE_FULL)))
elif variant == "block":
    sys.stdout.write(block(ROWS, PROSE_FULL))
