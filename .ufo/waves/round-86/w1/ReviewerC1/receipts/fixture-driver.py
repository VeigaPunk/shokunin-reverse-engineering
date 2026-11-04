import json, os, shutil, subprocess, sys
from pathlib import Path

LANE = Path("/home/vgpnk/Projects/shokunin/kaidoku-shokunin")
COUNTER = LANE / "tools/round-86/record-agreement.py"
BASE = "2cf0b7ff93c698809bed321f7338276a22d6beb9"
S = Path("/fast/scratch/hyaku/kaidoku-r86/ReviewerC1")
FX = S / "fx"
RCPT = LANE / ".ufo/waves/round-86/w1/ReviewerC1/receipts"
ENV = {"PATH": os.environ["PATH"], "HOME": os.environ["HOME"], "TMPDIR": str(S), "LANG": "C.UTF-8"}


def show(path):
    p = subprocess.run(["git", "-C", str(LANE), "show", f"{BASE}:{path}"], capture_output=True, text=True, check=True)
    return p.stdout


SRC = show("corpus/SOURCES.md")
CODE = show("tools/round-84/mutation-closure.py")
CARD = show("SCORECARD.md")
S303_LINE = next(l for l in SRC.splitlines() if l.startswith("| S303 "))
CARD_LINES = CARD.splitlines()
COV_IDX = [i for i, l in enumerate(CARD_LINES) if l.startswith("| coverage |")]
assert len(COV_IDX) == 23, len(COV_IDX)
ROW_HEAD = "| S305 | npm tarball rea-agents-6.5.0.tgz pack, supersession | code | A | scope | anchor | {t} | rejected | 2026-11-04 | on-release | corpus/lessons/round-86.md |"
URL = "https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz"
ROW_HEAD = ROW_HEAD.replace("npm tarball rea-agents-6.5.0.tgz pack, supersession", f"npm tarball {URL} supersession")


def src_with(new_lines_after_s303, row_mod=None):
    out = []
    for l in SRC.splitlines():
        out.append(l)
        if l == S303_LINE:
            out.extend(new_lines_after_s303)
    return "\n".join(out) + "\n"


def row(teaches):
    return ROW_HEAD.format(t=teaches)


RECEIPT_OK = lambda rev: json.dumps({"rev": rev, "ok": True}) + "\n"
CARD_ONE = lambda pointer, rnd: f"| coverage | 9.72 → 10.0 | evidence (`{pointer}`) | {rnd} (fixture) |\n"

fixtures = {}  # name -> (files, expectation note)

# ---- base parity (do-nothing control)
fixtures["00-base-worktree"] = ({"corpus/SOURCES.md": SRC, "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "BASE bytes; expect 0/3, mismatches x3")

# ---- (a) superseding row, count 7 with ids not the URL rows
fixtures["01a-count7-ids-S001-S007"] = ({"corpus/SOURCES.md": src_with([row("supersedes S303 — count 7 (S001/S002/S003/S004/S005/S006/S007) corrected prior-row count")]), "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "refuse A1")
fixtures["01a-control-count7-correct-ids"] = ({"corpus/SOURCES.md": src_with([row("supersedes S303 — count 7 (S079/S080/S083/S090/S092/S119/S123) corrected prior-row count")]), "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "accept A1 (the real work)")
fixtures["01a-count6-correct-ids"] = ({"corpus/SOURCES.md": src_with([row("supersedes S303 — count 6 (S079/S080/S083/S090/S092/S119/S123)")]), "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "refuse A1")
fixtures["01a-stale-earlier-wrong-row-plus-correct"] = ({"corpus/SOURCES.md": src_with([row("supersedes S303 — count 3 (S083/S090/S119) corrected prior-row count"), row("supersedes S303 — count 7 (S079/S080/S083/S090/S092/S119/S123) corrected prior-row count")]), "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "accept A1 wrongly: only the newest supersession row is read; the stale wrong count stays")
fixtures["01a-count7-with-S303-in-list"] = ({"corpus/SOURCES.md": src_with([row("supersedes S303 — count 7 (S079/S080/S083/S090/S092/S119/S123/S303)")]), "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "refuse A1")
fixtures["01d-indented3-correct"] = ({"corpus/SOURCES.md": src_with(["   " + row("supersedes S303 — count 7 (S079/S080/S083/S090/S092/S119/S123)")]), "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "accept A1 (GFM allows <=3 spaces)")
fixtures["01d-wrapped-prose-row"] = ({"corpus/SOURCES.md": src_with(["Round 86 records the supersession in prose: " + row("supersedes S303 — count 7 (S079/S080/S083/S090/S092/S119/S123)")]), "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "refuse A1 (not a registry row)")
fixtures["01d-row-split-across-lines"] = ({"corpus/SOURCES.md": src_with([ROW_HEAD.split("supersedes")[0] + "supersedes S303 — count 7 (S079/S080/S083/S090/S092/", "S119/S123) corrected | rejected | 2026-11-04 | on-release | corpus/lessons/round-86.md |"]), "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "refuse A1 (wrapped row)")
fixtures["01d-row-in-code-fence"] = ({"corpus/SOURCES.md": src_with(["```", row("supersedes S303 — count 7 (S079/S080/S083/S090/S092/S119/S123)"), "```"]), "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}, "refuse A1 (row is not a registry row); counter may accept")

# ---- (b) docstring
fixtures["02b-surviv-other-sentence"] = ({"corpus/SOURCES.md": SRC, "tools/round-84/mutation-closure.py": CODE.replace("present in the target's own output;", "present in the target's own output; survivors are listed in the receipt;", 1), "SCORECARD.md": CARD}, "refuse A2 (absent-case sentence still says inconclusive)")
fixtures["02b-split-sentence-verdict"] = ({"corpus/SOURCES.md": SRC, "tools/round-84/mutation-closure.py": CODE.replace("an absent declared case is inconclusive, never a pass", "an absent declared case is survived. Verdict on that case: inconclusive, never a pass", 1), "SCORECARD.md": CARD}, "refuse A2 (two statuses for the absent case); counter may accept")
fixtures["02b-stem-substring-lint"] = ({"corpus/SOURCES.md": SRC, "tools/round-84/mutation-closure.py": CODE.replace("an absent declared case is inconclusive, never a pass", "an absent declared case is a survivability question, never a pass", 1), "SCORECARD.md": CARD}, "refuse A2 (asserts no status); counter may accept on 'survi' substring")
fixtures["02b-decoy-earlier-branch"] = ({"corpus/SOURCES.md": SRC, "tools/round-84/mutation-closure.py": CODE.replace("\nimport argparse", "\nif not case_present:\n    entry = {}\n    entry[\"status\"] = \"inconclusive\"\n\nimport argparse", 1), "SCORECARD.md": CARD}, "refuse A2 (code's real branch survived); counter may read decoy")
fixtures["02b-real-fix-survived"] = ({"corpus/SOURCES.md": SRC, "tools/round-84/mutation-closure.py": CODE.replace("an absent declared case is inconclusive, never a pass", "an absent declared case is a survivor, never a pass", 1), "SCORECARD.md": CARD}, "accept A2 (the real work)")

# ---- (c) receipt pointer; card with exactly one coverage row
def card_pointing(pointer, rnd="86"):
    return CARD_ONE(pointer, rnd)

R86 = ".ufo/waves/round-86/l1/scores/c.json"
fixtures["03c-receipt-rev-39hex"] = ({"SCORECARD.md": card_pointing(R86), R86: RECEIPT_OK("a" * 39)}, "refuse A3")
fixtures["03c-receipt-rev-40hex-upper"] = ({"SCORECARD.md": card_pointing(R86), R86: RECEIPT_OK("A" * 40)}, "refuse A3")
fixtures["03c-receipt-rev-40hex-lower-valid"] = ({"SCORECARD.md": card_pointing(R86), R86: RECEIPT_OK("b" * 40)}, "accept A3 (receipt shape only)")
fixtures["03c-receipt-rev-zeros"] = ({"SCORECARD.md": card_pointing(R86), R86: RECEIPT_OK("0" * 40)}, "accept A3 wrongly: rev is not the measured revision or any commit")
fixtures["03c-decoy-newest-round99-unrelated"] = ({"SCORECARD.md": CARD_ONE(R86 + "` and `.ufo/waves/round-99/l1/scores/unrelated.json", "86") , R86: RECEIPT_OK("b" * 40), ".ufo/waves/round-99/l1/scores/unrelated.json": json.dumps({"rev": "c" * 40, "ok": False}) + "\n"}, "accept A3 wrongly: newest named receipt is unrelated and ok:false")
fixtures["03c-predates-round84"] = ({"SCORECARD.md": card_pointing(".ufo/waves/round-84/l1/scores/x.json", "85"), ".ufo/waves/round-84/l1/scores/x.json": RECEIPT_OK("b" * 40)}, "refuse A3 (predates)")
fixtures["03e-two-coverage-rows"] = ({"SCORECARD.md": card_pointing(R86) + card_pointing(R86, "86"), R86: RECEIPT_OK("b" * 40)}, "refuse A3 (two rows)")
fixtures["03e-base-card-23-rows"] = ({"SCORECARD.md": CARD}, "refuse A3 (found 23) -- BASE reason")

# reachability: what does A3 need?
base_minus_hist = [l for i, l in enumerate(CARD_LINES) if i not in COV_IDX or i == 22]
ptr85 = ".ufo/waves/round-85/l1/scores/coverage-r85.json"
row23 = CARD_LINES[22].replace(".ufo/waves/round-84/l1/scores/coverage-selfcheck.json", ptr85)
row23 = row23.replace(".ufo/waves/round-76/l1/scores/coverage-selfcheck-at-record.json", ".ufo/waves/round-76/l1/scores/coverage-selfcheck-at-record.json")
card_delete_hist = "\n".join([l if i != 22 else row23 for i, l in enumerate(CARD_LINES) if i not in COV_IDX or i == 22]) + "\n"
card_relabel_hist = "\n".join([l if i == 22 and False else (row23 if i == 22 else (l.replace("| coverage |", "| coverage-hist |", 1) if i in COV_IDX else l)) for i, l in enumerate(CARD_LINES)]) + "\n"
fixtures["04-reach-row23-only-no-receipt"] = ({"corpus/SOURCES.md": SRC, "SCORECARD.md": "\n".join([row23 if i == 22 else l for i, l in enumerate(CARD_LINES)]) + "\n"}, "refuse A3: names round-85 receipt that does not exist at BASE")
fixtures["04-reach-delete-22-hist-rows"] = ({"SCORECARD.md": card_delete_hist, ptr85: RECEIPT_OK("b" * 40)}, "accept A3: requires deleting 22 history rows (not a record edit)")
fixtures["04-reach-relabel-22-hist-rows"] = ({"SCORECARD.md": card_relabel_hist, ptr85: RECEIPT_OK("b" * 40)}, "accept A3: requires relabelling 22 history rows (also not a record edit)")
fixtures["04-reach-minimal-no-history-touch"] = ({"SCORECARD.md": "\n".join([row23 if i == 22 else l for i, l in enumerate(CARD_LINES)]) + "\n", ptr85: RECEIPT_OK("b" * 40)}, "refuse A3: 23 rows still, the A3 rule cannot pass without history edits")

results = []
if FX.exists():
    shutil.rmtree(FX)
for name, (files, note) in fixtures.items():
    d = FX / name
    for rel, text in files.items():
        p = d / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    # ensure the non-SOURCES fixtures still satisfy A1/A2 inputs by copying BASE where absent
    for rel, text in {"corpus/SOURCES.md": SRC, "tools/round-84/mutation-closure.py": CODE, "SCORECARD.md": CARD}.items():
        if not (d / rel).exists():
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            (d / rel).write_text(text)
    for mode in ("default", "control"):
        out = RCPT / f"{name}.{mode}.json"
        cmd = ["python3", "-I", "-B", str(COUNTER), "--root", str(d), "--worktree", str(d), "--json-out", str(out)]
        if mode == "control":
            cmd += ["--control", "substring-only"]
        p = subprocess.run(cmd, capture_output=True, text=True, env=ENV, cwd=str(S))
        line = [l for l in p.stdout.splitlines() if l.startswith(("RECORD_AGREEMENT", "CONTROL"))]
        mism = None
        if out.exists():
            mism = json.loads(out.read_text())["mismatches"]
        results.append({"fixture": name, "mode": mode, "exit": p.returncode, "mismatches": mism,
                        "summary": line[-1] if line else p.stderr.strip()[-200:], "expect": note,
                        "path": str(d)})
(S / "results.json").write_text(json.dumps(results, indent=1))
for r in results:
    print(f"{r['fixture']:<42} {r['mode']:<8} exit={r['exit']} mism={r['mismatches']} | {r['expect']}")
