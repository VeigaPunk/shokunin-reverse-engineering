import pathlib
import re
import subprocess

rev = "0436f4940283072db08e73c0117195847c50d31d"

def show(path):
    return subprocess.check_output(["git", "show", f"{rev}:{path}"], text=True)

paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", rev, "--", "corpus/knowledge"], text=True).splitlines()
files = {pathlib.PurePosixPath(path).stem for path in paths if path.endswith(".md")}
section = show("corpus/README.md").split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", section))
craft = show("SKILL.md").split("## Queue-drain craft ", 1)[1].split("\n## ", 1)[0]
rules = re.split(r"(?m)^- \*\*", craft)[1:]
pattern = r"corpus/knowledge/([a-z0-9-]+\.md)(?::(\d+)(?:-(\d+))?)?"

def resolved(rule):
    refs = re.findall(pattern, rule)
    valid = bool(refs)
    for name, first, last in refs:
        try:
            count = len(show("corpus/knowledge/" + name).splitlines())
            start, end = int(first or 1), int(last or first or 1)
            valid = valid and 1 <= start <= end <= count
        except subprocess.CalledProcessError:
            valid = False
    return bool(refs) and valid, refs

print(f"revision={rev} baseline_knowledge_files={len(files)} mapped={len(files & mapped)} missing={sorted(files - mapped)} dangling={sorted(mapped - files)} baseline_rule_blocks={len(rules)}")
for seat in ("EX-13", "EX-15"):
    text = pathlib.Path(f".ufo/waves/arc3-loop1-round12/claims/c2/{seat}.md").read_text()
    proposal = next(line for line in text.splitlines() if line.startswith("- **") and "Evidence-ID" in line or line.startswith("- **Measure `ev_`"))
    all_rules = rules + [proposal]
    count = sum(resolved(rule)[0] for rule in all_rules)
    ok, refs = resolved(proposal)
    refs_ok = all(
        pathlib.PurePosixPath(name).stem in files & mapped
        and 1 <= int(first or 1) <= int(last or first or 1) <= len(show("corpus/knowledge/" + name).splitlines())
        for name, first, last in refs
    )
    print(f"{seat}: projected_rule_blocks={len(all_rules)} citation_resolved_rules={count} proposal_refs={len(refs)} all_proposal_refs_in_bounds_and_mapped={refs_ok}")
