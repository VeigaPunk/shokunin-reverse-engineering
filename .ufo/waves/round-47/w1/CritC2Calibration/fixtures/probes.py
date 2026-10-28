#!/usr/bin/env python3
"""CritC2Calibration probes — regenerates the census, timeline, ledger, open-defect and
pinning receipts for one revision. Read-only: `git show`/`ls-tree`/`cat-file`/`status` and a
read-only import of the frozen counter. Nothing under the lane is written except --out-dir.

  python3 -I -B .ufo/waves/round-47/w1/CritC2Calibration/fixtures/probes.py \
      --lane /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> \
      --out-dir .ufo/waves/round-47/w1/CritC2Calibration/receipts
"""
import argparse
import datetime
import json
import os
import subprocess
import sys


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", required=True)
    ap.add_argument("--rev", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--timeline", type=int, default=8)
    a = ap.parse_args()
    rev = git(a.lane, "rev-parse", a.rev).stdout.strip()
    sys.path.insert(0, os.path.join(a.lane, "tools", "round-47"))
    import record  # noqa: E402

    def show(p, r=None):
        r = r or rev
        q = git(a.lane, "show", f"{r}:{p}")
        return q.stdout if q.returncode == 0 else None

    def emit(name, payload):
        path = os.path.join(a.out_dir, name)
        with open(path, "w") as fh:
            json.dump(payload, fh, indent=1, sort_keys=True)
        print(name, payload.get("atoms", ""), payload.get("utc", ""))

    card = show("SCORECARD.md")
    cache = {}

    def spawns(rnd):
        if rnd not in cache:
            cache[rnd] = record.dispatch_counts(show, str(rnd))
        return cache[rnd]

    # ---- census: every atom, its kind, its verdict -------------------------------
    secs = record.sections(card)
    atoms = []
    for rnd, text in secs:
        atoms += record.collect(text, rnd, show, a.lane, rev)
    atoms += record.collect_axes(card)
    corr, _ = record.corrections(card)
    rows = []
    for atom in atoms:
        cls = atom["class"]
        ok, detail = record.derive(atom, show, a.lane, rev, spawns)
        exempt = (not ok) and any(
            c["class"] == cls and (str(c["key"]) == str(atom["key"]) or cls == "window")
            for c in corr)
        rows.append({"class": cls, "key": str(atom["key"]),
                     "kind": "token" if cls in ("path", "rev") else "content",
                     "atom": atom["atom"][:110], "derive_ok": ok,
                     "derived": detail, "exempted": bool(exempt)})
    content = [r for r in rows if r["kind"] == "content"]
    emit("c2-atom-census.json", {
        "rev": rev, "utc": now(), "sections": [r for r, _ in secs],
        "atoms": len(rows), "token_atoms": sum(1 for r in rows if r["kind"] == "token"),
        "content_atoms": len(content), "content_detail": content,
        "corrections_counted": [c["text"][:130] for c in corr],
        "correction_lines_in_card": [l for l in
                                     card.split(record.CORR_HEAD)[1].split("\n## ")[0].splitlines()
                                     if l.strip().startswith("- corrects")]})

    # ---- timeline: atoms/sections per landing commit -----------------------------
    log = git(a.lane, "log", "--format=%h %H %s", f"-{a.timeline}", rev, "--",
              "SCORECARD.md", "tools/round-47/record.py").stdout.splitlines()
    tl = []
    for line in log:
        h, full, subj = line.split(" ", 2)
        c = git(a.lane, "show", f"{full}:SCORECARD.md").stdout
        f = lambda p, r=full: (git(a.lane, "show", f"{r}:{p}").stdout
                               if git(a.lane, "cat-file", "-e", f"{r}:{p}").returncode == 0
                               else None)
        code, rec = record.evaluate_text(c, f, a.lane, full, battery=None)
        tl.append({"commit": h, "subject": subj[:70], "exit": code,
                   "sections": rec.get("sections"), "atoms": rec.get("atoms"),
                   "exempted": len(rec.get("exempted", [])),
                   "corrections": rec.get("corrections"),
                   "mismatches": len(rec.get("mismatches", []))})
    emit("c2-timeline.json", {"head": rev, "utc": now(), "rows": tl})

    # ---- the round-47 ledger row vs the receipt it cites -------------------------
    sec = card.split("## Round 47", 1)[1] if "## Round 47" in card else ""
    row = next((l for l in sec.splitlines() if l.startswith("| R47-C2 |")), "")
    cells = [c.strip() for c in row.split("|") if c.strip()]
    cited = [t for t in row.split() if "l1/scores/" in t]
    cited = [c.strip("()`") for c in cited]
    def receipt_of(name):
        body = show(".ufo/waves/round-47/l1/scores/" + name)
        if body is None:
            return None
        d = json.loads(body)
        return {"file": name, "rev": d.get("rev"), "atoms": d.get("atoms"),
                "exempted": len(d.get("exempted", [])), "corrections": d.get("corrections"),
                "mismatches": len(d.get("mismatches", [])), "sections": d.get("sections"),
                "met_target": d.get("met_target"), "failing": d.get("failing")}
    calib = next((l for l in card.splitlines() if l.startswith("| calibration |")), "")
    emit("ledger-vs-receipt.json", {
        "axis_row_calibration": {
            "atoms_claim": __import__("re").findall(r"re-derives (\d+) atoms", calib),
            "exempted_claim": __import__("re").findall(r"`exempted (\d+) <= (\d+)`", calib),
            "cites": [t.strip("()`") for t in calib.split() if "l1/scores/" in t]},
        "utc": now(), "head": rev, "row_found": bool(row),
        "row_atoms_claim": __import__("re").findall(r"`atoms (\d+)`", row),
        "row_exempted_claim": __import__("re").findall(r"`exempted (\d+) <= (\d+)`", row),
        "row_measured_at": cells[-1] if cells else None,
        "row_cites": cited,
        "cited_receipt": receipt_of(cited[0].split("/")[-1]) if cited else None,
        "receipts": [receipt_of(n) for n in
                     ("c2-at-A4.json", "c2-at-A7.json", "c2-at-R4.json")]})

    # ---- routed record defects: the surfaces no class reads ----------------------
    probes = {"measured_rev": rev, "utc": now(), "probes": {}}

    def probe(name, *args, note=""):
        r = git(a.lane, *args)
        probes["probes"][name] = {"cmd": "git -C <lane> " + " ".join(args),
                                  "exit": r.returncode,
                                  "lines": [l[:220] for l in r.stdout.splitlines()][:40],
                                  "note": note}

    tree = git(a.lane, "ls-tree", "-r", "--name-only", rev, ".ufo/waves/round-46").stdout.split()
    probes["probes"]["round46_markers"] = {
        "cmd": "git -C <lane> ls-tree -r --name-only <rev> .ufo/waves/round-46",
        "tree_entries": len(tree), "ready": [p for p in tree if ".ready" in p],
        "results_json": [p for p in tree if p.endswith("-results.json")],
        "note": "wave 2 never dispatched; LOG.md cites {w1,w2}-results.json"}
    tree45 = git(a.lane, "ls-tree", "-r", "--name-only", rev, ".ufo/waves/round-45").stdout.split()
    probes["probes"]["round45_markers"] = {
        "cmd": "git -C <lane> ls-tree -r --name-only <rev> .ufo/waves/round-45",
        "ready": [p for p in tree45 if ".ready" in p],
        "note": "a dispatched wave pair carries both .ready markers"}
    probe("w2_dispatch_provenance", "log", "--format=%H %ci %s", "--",
          ".ufo/waves/round-46/w2-dispatch.json")
    probe("log_round46_waves",
          "grep", "-n", "-E", "wave 2 = 40 seats|Round total 80|w1,w2\\}-results", "--", "LOG.md")
    for p in ("ctl-c1-1-v1-profile.json", "ctl-c2-1-v1-profile.json", "ctl-c2-2-ghost-tool.json"):
        probe("v7_rc_" + p, "cat-file", "-e",
              f"{rev}:.ufo/waves/round-46/controls/{p}", note="R46-V7 cited receipt")
    probe("v7_rc_l1_scores_c1_v1_gap", "cat-file", "-e",
          f"{rev}:.ufo/waves/round-46/l1/scores/c1-v1-gap.json", note="R46-V7 cited receipt")
    for axis in ("coverage", "depth", "calibration"):
        row = next((l for l in card.splitlines() if l.startswith(f"| {axis} |")), None)
        probes["probes"]["axis_row_" + axis] = {"head": row[:220] if row else None,
                                                "is_atom": axis in ("coverage", "depth")}
    st = git(a.lane, "status", "--porcelain")
    probes["probes"]["worktree_porcelain"] = {
        "cmd": "git -C <lane> status --porcelain", "exit": st.returncode,
        "n": len([l for l in st.stdout.splitlines() if l]),
        "note": "R46-V5 surface; record.py reads git show only"}
    emit("record-open-defects.json", probes)

    # ---- pinning: what the C2 receipt cannot show -------------------------------
    src = show("tools/round-47/record.py") or ""
    live_keys = None
    rec_path = os.path.join(a.out_dir, "c2-at-live.json")
    if os.path.exists(rec_path):
        live_keys = sorted(json.load(open(rec_path)))
    lines = [f"# pinning probes — lane {rev} at {now()}", "",
             "## occurrences in tools/round-47/record.py",
             f"freeze: {src.count('freeze')}", f"sha256: {src.count('sha256')}",
             "", "## byte history of record.py after the claims file was last amended",
             git(a.lane, "log", "--format=%h %s", "62e33f7d.." + rev, "--",
                 "tools/round-47/", "plans/round-47-claims.md").stdout.strip(),
             "", "## receipt keys of a C2 run (no freeze/pin field)",
             json.dumps(live_keys)]
    with open(os.path.join(a.out_dir, "tool-pinning.txt"), "w") as fh:
        fh.write("\n".join(lines) + "\n")
    print("tool-pinning.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
