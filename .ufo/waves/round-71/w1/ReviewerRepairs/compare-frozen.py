import hashlib, json, re, subprocess
R = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
B = "82c8e620c9222fb218aa0260570a3765da2afb44"
F = "b827a8b5d54f2885ec9be7786389f356c59226ce"
def git(*args):
    return subprocess.check_output(["git", "-C", R, *args])
def blob(path, rev=F):
    return git("show", rev + ":" + path)
plan = blob("plans/round-71-claims.md").decode()
container = json.loads(blob(".ufo/waves/round-71/claims.json"))
predicates = re.findall(r"\*\*Predicate \(one sentence, frozen\)\.\*\*\s*(.*?)(?=\n\n)", plan, re.S)
norm = lambda text: " ".join(text.split())
assert len(predicates) == len(container["claims"]) == 3
print("normalized_predicate_equal", [norm(p) == norm(c) for p, c in zip(predicates, container["claims"])])
for group in ("instruments", "loaded_by_counter"):
    for path, expected in container[group].items():
        actual = hashlib.sha256(blob(path)).hexdigest()
        print(group, path, actual, actual == expected)
old = blob("SKILL.md", B).decode()
new = blob("SKILL.md").decode()
print("SKILL_whole_blob_equal", old == new)
for line in old.splitlines():
    if line.startswith("|") and "round-69/" in line and len(re.split(r"(?<!\\)\|", line.strip()[1:-1])) == 8:
        print("round69_eight_cell_row_equal", line.split("|")[1].strip(), line in new.splitlines())
