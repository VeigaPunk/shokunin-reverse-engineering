#!/usr/bin/env python3
"""C1Tokens driver: clause-5 fixture, candidate block 24, arm-cell attack matrix."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
S = os.environ["HYAKU_SCRATCH"]

sys.path.insert(0, os.path.join(LANE, "tools", "round-47"))
sys.path.insert(0, os.path.join(LANE, "tools", "round-46"))
import exact  # noqa: E402
import gate  # noqa: E402

MUT_DIGEST = hashlib.sha256("\n".join(n for n, _ in exact.MUTATIONS).encode()).hexdigest()
SELF_SHA = hashlib.sha256(open(os.path.join(LANE, "tools/round-47/exact.py"), "rb").read()).hexdigest()


def show(path):
    r = subprocess.run(["git", "-C", LANE, "show", f"{FREEZE}:{path}"],
                       capture_output=True, text=True)
    assert r.returncode == 0, (path, r.stderr)
    return r.stdout


BASE_FILES = {}
for p in ("SKILL.md", "plans/round-47-claims.md", "tools/round-47/exact.py",
          "tools/round-46/gate.py", "corpus/lessons/round-46.md",
          "corpus/lessons/round-45.md"):
    BASE_FILES[p] = show(p)

ROWS = [
    ("R46-CL2 — a cell passes because some vocabulary token is a substring of it",
     "the arm check is `token in cell.lower()`, so `blobberish` scores where `symbol` was meant (`corpus/lessons/round-46.md:57-59`)",
     "symbol", "1"),
    ("R46-CL3 — an id is satisfied by appearing in some row, not in its own row",
     "the routed-id check asks at-least-once, so a row may claim a group it does not address (`corpus/lessons/round-46.md:60-62`)",
     "once", "1"),
    ("R46-CL4 — the mutation list carries no digest",
     "`forgeries_total` is checked while a deletion silently changes the denominator (`corpus/lessons/round-46.md:63-64`)",
     "digest", "1"),
    ("R46-CL6 — the history arm's flag order is unenforced",
     "`-m` after `--diff-merges=first-parent` prints a merge twice and restores the blindness (`corpus/lessons/round-46.md:65-69`)",
     "order", "1"),
]

PROSE_FULL = (
    "- **24. An exact binding is an equality, not a containment.** "
    "<!-- exactness-table v3 --> Block 23 stated the arms; this block states the four ways "
    "its own clause text was satisfiable without the property it named, one row per defect "
    "the round-46 spot-check routed (`corpus/lessons/round-46.md:51-69`). Each v3-arm cell "
    "is a binding, not a vocabulary hit: the cell is stripped of backticks and spaces and "
    "then compared for equality, so `order-ish` fails `order` and `blobberish` fails "
    "`symbol` (`plans/round-47-claims.md:76-77`). The interpreter is pinned twice — by its "
    "own bytes and by a digest over its mutation list in the counter's order "
    "(substring-arm, duplicate-routed-id, stale-mutations-digest, flag-order-drift) — so "
    "deleting a mutation moves the printed digest instead of shrinking the denominator the "
    "claim is judged on. `tools/round-47/exact.py` interpreter_sha256:%s "
    "mutations_sha256:%s." % (SELF_SHA, MUT_DIGEST)
)
PROSE_MIN = (
    "- **24. An exact binding is an equality, not a containment.** "
    "<!-- exactness-table v3 --> Minimal clause-5 candidate: header, four rows, exact arm tokens."
)


def block(rows, prose):
    out = prose + "\n\n  | trigger | v2 hole | v3 arm | exit |\n  | --- | --- | --- | --- |\n"
    for r in rows:
        out += "  | " + " | ".join(r) + " |\n"
    return out + "\n"


def skill_with(blk):
    text = BASE_FILES["SKILL.md"]
    assert text.count(MARKER_SEP) == 1
    return text.replace(MARKER_SEP, blk + MARKER_SEP, 1)


MARKER_SEP = "\n## Config custody for live-probe rounds (SOP)"


def fixture(files, prefix):
    d = tempfile.mkdtemp(dir=S, prefix=prefix)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    for k, v in (("user.email", "fx@round47"), ("user.name", "r47 fixture")):
        subprocess.run(["git", "-C", d, "config", k, v], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    assert top == d, (top, d)
    for p, t in files.items():
        full = os.path.join(d, p)
        os.makedirs(os.path.dirname(full) or d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(t)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "commit", "-q", "-m", "fixture"], check=True)
    rev = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                         capture_output=True, text=True).stdout.strip()
    return d, rev


def run(skill, label, battery=False):
    files = dict(BASE_FILES)
    files["SKILL.md"] = skill
    d, rev = fixture(files, "fx-")
    try:
        f = lambda p: gate.show(d, rev, p)  # noqa: E731
        c3, r3 = exact.score(skill, f, "v3", rev, battery=None)
        c2, r2 = exact.score(skill, f, "v2", rev, battery=None)
        bat = None
        if battery:
            sr, err = gate.scratch("b-")
            assert not err, err
            try:
                bat = exact.run_battery(d, rev, sr)
            finally:
                shutil.rmtree(sr, ignore_errors=True)
            if "error" not in bat:
                c3, r3 = exact.score(skill, f, "v3", rev, battery=bat)
    finally:
        shutil.rmtree(d, ignore_errors=True)
    return {"label": label, "v3_exit": c3, "v2_exit": c2,
            "v3_failing": r3.get("failing", r3.get("reason")),
            "v2_failing": r2.get("failing", r2.get("reason")),
            "v3_arms": r3.get("arm_tokens"), "v3_routed": r3.get("routed_counts"),
            "v3_refs": r3.get("refs"), "v3_cited": r3.get("cited"),
            "v3_mut_pin": r3.get("mutations_sha256"),
            "v3_mut_expected": r3.get("mutations_sha256_expected"),
            "v3_self_pin": r3.get("interpreter_sha256"),
            "v3_self_expected": r3.get("interpreter_sha256_expected"),
            "battery": bat}


out = []
out.append({"digests": {"mutations_sha256": MUT_DIGEST,
                        "interpreter_sha256": SELF_SHA,
                        "mut_digest_over_three": hashlib.sha256(
                            "\n".join(n for n, _ in exact.MUTATIONS[:3]).encode()).hexdigest()}})
out.append(run(skill_with(block(ROWS, PROSE_MIN)), "A: clause-5-only block"))
out.append(run(skill_with(block(ROWS, PROSE_FULL)), "B: full block + battery", battery=True))

# attack matrix: arm-cell variants against the full block
VARIANTS = [
    ("exact tokens (control)", ["symbol", "once", "digest", "order"]),
    ("backticked", ["`symbol`", "`once`", "`digest`", "`order`"]),
    ("padded spaces", ["  symbol  ", "once ", " digest", "order  "]),
    ("suffix -ish", ["symbol-ish", "once-ish", "digest-ish", "order-ish"]),
    ("prefix contains token", ["symbolmap", "onceover", "digested", "orderly"]),
    ("prose phrase", ["the symbol arm", "exactly once", "a digest pin", "flag order"]),
    ("empty cell", ["", "once", "digest", "order"]),
    ("capitalised", ["Symbol", "Once", "Digest", "Order"]),
    ("all four = order", ["order", "order", "order", "order"]),
    ("all four = symbol", ["symbol", "symbol", "symbol", "symbol"]),
    ("tab suffix", ["symbol\t", "once", "digest", "order"]),
    ("newline-ish zero width", ["symbol\u200b", "once", "digest", "order"]),
]
for label, arms in VARIANTS:
    rows = [tuple(r[:2]) + (a,) + tuple(r[3:]) for r, a in zip(ROWS, arms)]
    out.append(run(skill_with(block(rows, PROSE_FULL)), "attack: " + label))

print(json.dumps(out, indent=1))
