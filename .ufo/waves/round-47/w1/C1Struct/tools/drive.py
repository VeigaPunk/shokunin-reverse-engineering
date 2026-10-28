#!/usr/bin/env python3
"""C1Struct: verify R47-C1 clauses 1-3 on the frozen counter, build candidate block 24.

Reads the lane read-only (git show), builds one-commit fixture repos under $S, and
scores candidates with the frozen exact.py `score`/`run_battery` functions.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
S = os.environ.get("HYAKU_SCRATCH") or "/fast/scratch/hyaku/kaidoku-r47/C1Struct"
W = os.path.join(LANE, ".ufo/waves/round-47/w1/C1Struct")
sys.path.insert(0, os.path.join(LANE, "tools/round-47"))
sys.path.insert(0, os.path.join(LANE, "tools/round-46"))
import exact  # noqa: E402
import gate  # noqa: E402

NEEDED = ["SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
          "tools/round-46/gate.py", "corpus/lessons/round-46.md",
          "corpus/lessons/round-45.md"]


def show(path):
    r = subprocess.run(["git", "-C", LANE, "show", f"{FREEZE}:{path}"],
                       capture_output=True, text=True)
    assert r.returncode == 0, path
    return r.stdout


def fixture_files(skill):
    out = {"SKILL.md": skill}
    for p in NEEDED[1:]:
        out[p] = show(p)
    return out


def insert_block(skill, block, extra_after=None):
    head, sep, tail = skill.partition("## Queue-drain craft ")
    assert sep, "craft heading"
    body, sep2, rest = tail.partition("\n## ")
    assert sep2, "next heading"
    out = head + sep + body.rstrip("\n") + "\n\n" + block.rstrip("\n") + "\n\n"
    if extra_after:
        out += extra_after.rstrip("\n") + "\n\n"
    return out + "## " + rest


def score_fixture(skill, profile="v3", battery=None):
    files = fixture_files(skill)
    d, rev = exact._repo(files, S, prefix="c1struct-")
    try:
        f = lambda p: gate.show(d, rev, p)  # noqa: E731
        bat = None
        code, rec = exact.score(files["SKILL.md"], f, profile, rev, battery=None)
        if battery == "run" and code == 0:
            bat = exact.run_battery(d, rev, S)
            code, rec = exact.score(files["SKILL.md"], f, profile, rev, battery=bat)
        return code, rec, bat
    finally:
        shutil.rmtree(d, ignore_errors=True)


MUT_DIGEST = exact.MUT_DIGEST
SELF_PIN = hashlib.sha256(show("tools/round-47/exact.py").encode()).hexdigest()

BLOCK_A = """- **24. An exactness matrix states one exact arm per routed defect.** <!-- exactness-table v3 --> The round-46 spot-check routed four instrument defects; this table names each hole and the arm that closes it.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| a loose cell | the check is a containment, so any word passes | arm one | 1 |
| a loose cell | the check is at-least-once, so a row may overclaim | arm two | 1 |
| a loose cell | the list is counted, never pinned | arm three | 2 |
| a loose cell | the flag order is a code detail no clause reads | arm four | 1 |
"""

BLOCK_B = """- **24. An exact binding is an equality over one token, one id, one digest and one flag order.** <!-- exactness-table v3 --> The round-46 non-author spot-check routed four instrument defects (R46-CL2, R46-CL3, R46-CL4, R46-CL6); each row states the loose binding that let the defect through, the exact arm that now fails it, and the exit the counter returns when the arm fires. Interpreter `tools/round-47/exact.py` `interpreter_sha256:{self_pin}`; the mutation list is pinned by `mutations_sha256:{mut}` over substring-arm, duplicate-routed-id, stale-mutations-digest, flag-order-drift in that order, so deleting a mutation changes the printed digest. All four forged fixtures exit 1 under v3 and 0 under the ported v2 profile, so the arms are measured, not asserted.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| R46-CL2 `blobberish` satisfies `blob` | the arm-vocabulary check is a lowercased substring test, so any word carrying the token passes | symbol | 1 |
| R46-CL3 a row claims a routed id it does not address | every id need only appear in some row, never exactly once | once | 1 |
| R46-CL4 a deleted mutation changes the denominator | the list is counted but never pinned, so a deletion fails no clause | digest | 1 |
| R46-CL6 one argument reorder blinds the merge arm | `git log --diff-merges=first-parent -m` prints a merge twice, and nothing reads the order | order | 1 |

  Refs: `corpus/lessons/round-46.md:57-59` (R46-CL2, the substring arm), `corpus/lessons/round-46.md:60-62` (R46-CL3, the at-least-once id), `corpus/lessons/round-46.md:63-64` (R46-CL4, the unpinned list), `corpus/lessons/round-46.md:65-70` (R46-CL6, the order-sensitive arm), `corpus/lessons/round-46.md:21` (M46-2, why the list needs a digest), `plans/round-47-claims.md:68-90` (the predicate these rows are scored by).
""".format(self_pin=SELF_PIN, mut=MUT_DIGEST)


def attack_marker_elsewhere(skill):
    return skill + "\nA later note quotes the block-24 marker <!-- exactness-table v3 --> in prose.\n"


def attack_not_last(skill):
    return insert_block(skill, BLOCK_B, extra_after="- **25. A later block.** tail text\n")


def attack_title_no_space(skill):
    return insert_block(skill, BLOCK_B.replace("24. An exact", "24.An exact", 1))


def attack_header_five(skill):
    return insert_block(skill, BLOCK_B.replace(
        "| trigger | v2 hole | v3 arm | exit |\n|---|---|---|---|",
        "| trigger | v2 hole | v3 arm | exit | note |\n|---|---|---|---|---|", 1))


def attack_pipe_in_cell(skill):
    return insert_block(skill, BLOCK_B.replace(
        "| the list is counted but never pinned, so a deletion fails no clause |",
        "| the list is counted|pinned, so a deletion fails no clause |", 1))


def attack_exit_outside(skill):
    return insert_block(skill, BLOCK_B.replace(
        "| order | 1 |", "| order | 3 |", 1))


def attack_second_table(skill):
    return insert_block(skill, BLOCK_B.rstrip("\n") +
                        "\n\n| a | b | c | d |\n|---|---|---|---|\n| e | f | g | h |\n")


def run(name, skill, profile="v3", battery=None):
    code, rec, bat = score_fixture(skill, profile=profile, battery=battery)
    row = {"case": name, "profile": profile, "exit": code,
           "failing": rec.get("failing", rec.get("reason")),
           "marker_occurrences": rec.get("marker_occurrences"),
           "block_present": rec.get("block_present"),
           "block_is_last": rec.get("block_is_last"),
           "block_title": rec.get("block_title"),
           "header": rec.get("header"), "rows": rec.get("rows"),
           "rule_blocks": rec.get("rule_blocks")}
    if bat:
        row["battery"] = {k: bat.get(k) for k in
                          ("forgeries_total", "v2_green", "v3_green",
                           "genuine_green", "crash", "genuine_exit")}
        row["fixtures"] = bat.get("fixtures")
    print(json.dumps(row))
    return row


base = show("SKILL.md")
out = {"mut_digest": MUT_DIGEST, "self_pin": SELF_PIN, "cases": []}
out["cases"].append(run("baseline-freeze-no-block", base))
out["cases"].append(run("candidate-A-clauses-1-3-only", insert_block(base, BLOCK_A)))
out["cases"].append(run("candidate-B-full", insert_block(base, BLOCK_B), battery="run"))
out["cases"].append(run("attack-marker-quoted-elsewhere", attack_marker_elsewhere(
    insert_block(base, BLOCK_B))))
out["cases"].append(run("attack-block-not-last", attack_not_last(base)))
out["cases"].append(run("attack-title-no-trailing-space", attack_title_no_space(base)))
out["cases"].append(run("attack-header-five-cells", attack_header_five(base)))
out["cases"].append(run("attack-pipe-inside-a-cell", attack_pipe_in_cell(base)))
out["cases"].append(run("attack-exit-cell-3", attack_exit_outside(base)))
out["cases"].append(run("attack-second-table-in-block", attack_second_table(base)))
with open(os.path.join(S, "driver-out.json"), "w") as fh:
    json.dump(out, fh, indent=1)
print("WROTE", os.path.join(S, "driver-out.json"))
