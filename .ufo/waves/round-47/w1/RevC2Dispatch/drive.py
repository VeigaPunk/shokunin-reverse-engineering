#!/usr/bin/env python3
"""RevC2Dispatch: seats-derivation attack fixtures for round-47 record.py (frozen)."""
import hashlib, json, os, shutil, subprocess, sys, datetime

S = "/fast/scratch/hyaku/kaidoku-r47/RevC2Dispatch"
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
COUNTER = os.path.join(LANE, "tools/round-47/record.py")
FX = os.path.join(S, "fx")
ENV = dict(os.environ,
           GIT_AUTHOR_NAME="r47 fixt", GIT_AUTHOR_EMAIL="f@r47",
           GIT_COMMITTER_NAME="r47 fixt", GIT_COMMITTER_EMAIL="f@r47",
           GIT_AUTHOR_DATE="2026-10-28T00:00:00Z",
           GIT_COMMITTER_DATE="2026-10-28T00:00:00Z",
           TMPDIR=S, HYAKU_SCRATCH=S)

BASE_FILES = {
    "corpus/README.md": "# readme\n\n## Coverage map\n\n- 2026-10-01-x \u2014 x\n\n## Gaps\n\ntail\n",
    "corpus/knowledge/2026-10-01-x.md": "x\n",
    "tools/x/keep.md": "x\n",
    "SKILL.md": "# s\n\n## Queue-drain craft rules\n\n- **rule one** cites `corpus/knowledge/2026-10-01-x.md:1`.\n",
    ".ufo/waves/round-9/w1-spec.json": "{}\n",
    ".ufo/waves/round-9/w1-dispatch.json": json.dumps({"counts": {"spawn": 40, "resume": 0, "total": 40}}) + "\n",
    ".ufo/waves/round-9/w2-dispatch.json": json.dumps({"counts": {"spawn": 32, "resume": 0, "total": 32}}) + "\n",
    ".ufo/waves/round-9/r9-w1-results.json": json.dumps({"lane": "kaidoku", "round": 9, "wave": "r9-w1", "seats": 40}) + "\n",
    ".ufo/waves/round-9/r9-w2-results.json": json.dumps({"lane": "kaidoku", "round": 9, "wave": "r9-w2", "seats": 32}) + "\n",
    ".ufo/waves/round-8/w1-dispatch.json": json.dumps({"counts": {"spawn": 1}}) + "\n",
}


def card(rev, seats="Waves: 40 + 32 = 72 seats", seats_corr="2 waves, 72 seats total",
         seats_key="9", window=None, sections=2, path=".ufo/waves/round-9/w1-spec.json",
         axes_depth=True):
    window = window or "`git log {r}..{r} -- tools/x/` is empty".format(r=rev)
    depth = ("| depth | 20 \u2192 20 | 1/1 rules resolved | x | r1 |\n" if axes_depth else "")
    seat_line = (seats + ". ") if seats else ""
    text = ("# card\n\n## Owned axes\n\n"
            "| Axis | Baseline \u2192 current score, 0\u201310 | Observable | Evidence | Round |\n"
            "|---|---|---|---|---|\n"
            "| coverage | 9.72 \u2192 10.0 | 1/1 knowledge files mapped | x | r1 |\n"
            + depth +
            "\n## Round 8\n\nAn earlier round with no atoms.\n\n")
    if sections == 2:
        text += ("## Round 9\n\nBase `%s`. %s%s. See `%s`.\n\n" % (rev, seat_line, window, path))
    else:
        text += ("## Round 9\n\nBase `%s`. %s%s. See `%s`.\n\n" % (rev, seat_line, window, path))
        text = text.replace("## Round 8\n\nAn earlier round with no atoms.\n\n", "")
    text += ("## Record corrections \u2014 round 47\n\n"
             "- corrects seats round-%s: %s\n" % (seats_key, seats_corr)
             + "- corrects window round-9: empty in %s..%s -- tools/x/\n" % (rev, rev)
             + "- corrects path %s: landed\n" % path)
    return text


def sh(*args, cwd=None):
    return subprocess.run(args, cwd=cwd, env=ENV, capture_output=True, text=True)


def build(name):
    d = os.path.join(FX, name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    assert sh("git", "-C", d, "init", "-q").returncode == 0
    top = sh("git", "-C", d, "rev-parse", "--show-toplevel").stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)
    for path, body in BASE_FILES.items():
        full = os.path.join(d, path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w") as fh:
            fh.write(body)
    sh("git", "-C", d, "add", "-A")
    assert sh("git", "-C", d, "commit", "-q", "-m", "base").returncode == 0
    base = sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()
    return d, base


def commit_card_quiet(d, text, msg):
    """Card-only commit: base..tip over `tools/x/` stays EMPTY (honest window claim)."""
    with open(os.path.join(d, "SCORECARD.md"), "w") as fh:
        fh.write(text)
    sh("git", "-C", d, "add", "-A")
    r = sh("git", "-C", d, "commit", "-q", "-m", msg)
    assert r.returncode == 0, r.stderr
    return sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()


def commit_card(d, text, msg):
    with open(os.path.join(d, "SCORECARD.md"), "w") as fh:
        fh.write(text)
    # make base..tip over `tools/x/` non-empty, so the battery's non-empty-window
    # forgery is genuinely false (the selftest does the same)
    with open(os.path.join(d, "tools/x/keep.md"), "a") as fh:
        fh.write(msg + "\n")
    sh("git", "-C", d, "add", "-A")
    r = sh("git", "-C", d, "commit", "-q", "-m", msg)
    assert r.returncode == 0, r.stderr
    return sh("git", "-C", d, "rev-parse", "HEAD").stdout.strip()


def run(d, name, outdir):
    os.makedirs(os.path.join(d, "receipts"), exist_ok=True)
    outrel = os.path.join(d, "receipts", "%s.json" % name)
    cmd = [sys.executable, "-I", "-B", COUNTER, "--root", d, "--rev", "HEAD",
           "--json-out", outrel]
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    r = subprocess.run(cmd, env=ENV, capture_output=True, text=True)
    sha = hashlib.sha256(r.stdout.encode()).hexdigest()
    rec = json.load(open(os.path.join(d, outrel)))
    shutil.copy(os.path.join(d, outrel), os.path.join(outdir, name + ".json"))
    return {"name": name, "fixture": d, "cmd": " ".join(cmd), "utc": t,
            "exit": r.returncode, "stdout_sha256": sha,
            "failing": rec.get("failing"), "reason": rec.get("reason"),
            "met_target": rec.get("met_target"), "atoms_by_class": rec.get("atoms_by_class"),
            "seats_mismatches": [m for m in (rec.get("mismatches") or []) if m["class"] == "seats"],
            "all_mismatch_classes": sorted({m["class"] for m in (rec.get("mismatches") or [])}),
            "corrections_bad": rec.get("corrections_bad"),
            "has_failing_key": "failing" in rec, "has_met_target_key": "met_target" in rec}


def scen(name, mutate, out):
    d, base = build(name)
    rev8 = base[:8]
    mutate(d, rev8)
    return run(d, name, out)


def main():
    out = os.path.join(S, "receipts")
    os.makedirs(out, exist_ok=True)
    receipts = []

    def green(d, rev):
        commit_card(d, card(rev), "card green")

    receipts.append(scen("s0-green-baseline", green, out))

    def no_dispatch(d, rev):
        sh("git", "-C", d, "rm", "-q", ".ufo/waves/round-9/w1-dispatch.json",
           ".ufo/waves/round-9/w2-dispatch.json")
        sh("git", "-C", d, "commit", "-q", "-m", "rm dispatch")
        commit_card(d, card(rev), "card")
    receipts.append(scen("sA-no-dispatch-file", no_dispatch, out))

    def spawn_absent(d, rev):
        p = os.path.join(d, ".ufo/waves/round-9/w2-dispatch.json")
        open(p, "w").write(json.dumps({"counts": {"resume": 0, "total": 32}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "no spawn")
        commit_card(d, card(rev), "card")
    receipts.append(scen("sB-spawn-absent", spawn_absent, out))

    def spawn_string(d, rev):
        p = os.path.join(d, ".ufo/waves/round-9/w2-dispatch.json")
        open(p, "w").write(json.dumps({"counts": {"spawn": "32", "total": 32}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "str spawn")
        commit_card(d, card(rev), "card")
    receipts.append(scen("sB2-spawn-string-accepted", spawn_string, out))

    def spawn_float(d, rev):
        p = os.path.join(d, ".ufo/waves/round-9/w2-dispatch.json")
        open(p, "w").write(json.dumps({"counts": {"spawn": 32.9, "total": 32.9}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "float spawn")
        commit_card(d, card(rev), "card")
    receipts.append(scen("sB3-spawn-float-truncated", spawn_float, out))

    def gap_adapted(d, rev):
        sh("git", "-C", d, "rm", "-q", ".ufo/waves/round-9/w2-dispatch.json")
        open(os.path.join(d, ".ufo/waves/round-9/w3-dispatch.json"), "w").write(
            json.dumps({"counts": {"spawn": 32, "resume": 0, "total": 32}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "w1+w3")
        commit_card(d, card(rev, seats="Waves: 40 + 0 = 40 seats",
                            seats_corr="1 waves, 40 seats total"), "card")
    receipts.append(scen("sC-gap-w1-w3-adapted-claim", gap_adapted, out))

    def gap_honest(d, rev):
        sh("git", "-C", d, "rm", "-q", ".ufo/waves/round-9/w2-dispatch.json")
        open(os.path.join(d, ".ufo/waves/round-9/w3-dispatch.json"), "w").write(
            json.dumps({"counts": {"spawn": 32, "resume": 0, "total": 32}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "w1+w3")
        commit_card(d, card(rev), "card")
    receipts.append(scen("sC2-gap-honest-total", gap_honest, out))

    def glob_divergence(d, rev):
        os.rename(os.path.join(d, ".ufo/waves/round-9/w2-dispatch.json"),
                  os.path.join(d, ".ufo/waves/round-9/wave-2-dispatch.json"))
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "glob name")
        commit_card(d, card(rev, seats="Waves: 40 + 0 = 40 seats",
                            seats_corr="1 waves, 40 seats total"), "card")
    receipts.append(scen("sC3-glob-name-divergence", glob_divergence, out))

    def results_contradict(d, rev):
        open(os.path.join(d, ".ufo/waves/round-9/r9-w2-results.json"), "w").write(
            json.dumps({"lane": "kaidoku", "round": 9, "wave": "r9-w2", "seats": 36}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "results 36")
        commit_card(d, card(rev), "card")
    receipts.append(scen("sD-results-contradict-dispatch", results_contradict, out))

    def results_garbage(d, rev):
        open(os.path.join(d, ".ufo/waves/round-9/r9-w1-results.json"), "w").write("{not json")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "results junk")
        commit_card(d, card(rev), "card")
    receipts.append(scen("sD2-results-unreadable", results_garbage, out))

    def silence(d, rev):
        # move the seats claim to round 8 (1 dispatched seat); round 9 keeps 72 dispatched seats
        # and no seat sentence at all.
        text = card(rev, seats=None, seats_corr="1 waves, 1 seats total", seats_key="8")
        text = text.replace("## Round 8\n\nAn earlier round with no atoms.\n\n",
                            "## Round 8\n\nWaves: 1 + 0 = 1 seats.\n\n")
        commit_card(d, text, "card silent on round 9")
    receipts.append(scen("sE-silence-round-with-none", silence, out))

    def one_section(d, rev):
        commit_card(d, card(rev, sections=1), "card one round section")
    receipts.append(scen("sF-exit2-one-round-section", one_section, out))

    def launder_sum(d, rev):
        commit_card(d, card(rev, seats="Waves: 40 + 0 = 72 seats"), "card laundered sum")
    receipts.append(scen("sG-launder-false-split-sum", launder_sum, out))

    def launder_pair(d, rev):
        commit_card(d, card(rev, seats="Wave 1: 40 seats; wave 2: 0 seats"), "card laundered pair")
    receipts.append(scen("sG2-launder-false-split-pair", launder_pair, out))

    def three_waves_honest(d, rev):
        open(os.path.join(d, ".ufo/waves/round-9/w3-dispatch.json"), "w").write(
            json.dumps({"counts": {"spawn": 32}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "w3")
        commit_card(d, card(rev), "card three waves honest")
    receipts.append(scen("sH1-three-waves-honest-sum", three_waves_honest, out))

    def three_waves_false(d, rev):
        open(os.path.join(d, ".ufo/waves/round-9/w3-dispatch.json"), "w").write(
            json.dumps({"counts": {"spawn": 32}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "w3")
        commit_card(d, card(rev, seats="Waves: 40 + 32 = 104 seats",
                            seats_corr="3 waves, 104 seats total"), "card three waves false sum")
    receipts.append(scen("sH2-three-waves-arith-false", three_waves_false, out))

    def bool_spawn(d, rev):
        open(os.path.join(d, ".ufo/waves/round-9/w2-dispatch.json"), "w").write(
            json.dumps({"counts": {"spawn": True, "total": 1}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "bool")
        commit_card(d, card(rev, seats="Waves: 40 + 1 = 41 seats",
                            seats_corr="2 waves, 41 seats total"), "card bool spawn")
    receipts.append(scen("sB4-spawn-bool-accepted", bool_spawn, out))

    def resume_wave(d, rev):
        open(os.path.join(d, ".ufo/waves/round-9/w2-dispatch.json"), "w").write(
            json.dumps({"counts": {"spawn": 0, "resume": 32, "total": 32}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "resume wave")
        commit_card(d, card(rev, seats="Waves: 40 + 0 = 40 seats",
                            seats_corr="2 waves, 40 seats total"), "card resume wave")
    receipts.append(scen("sJ-resume-wave-zero-spawn", resume_wave, out))

    def honest_card_battery(d, rev):
        # an honest card: the round's `empty in base..base -- tools/x/` claim is true, and the
        # card commit does not touch tools/x, so the battery's non-empty-window forgery
        # (`base..tip`) stays TRUE and scores green.
        commit_card_quiet(d, card(rev), "card honest, tools/x untouched")
    receipts.append(scen("sK-battery-window-fragility", honest_card_battery, out))

    def historical_ghost(d, rev):
        # a round-3 correction with no round-3 atom in the card: predicate 3 calls this a
        # defect; A3 carves it out as "historical" evidence.
        os.makedirs(os.path.join(d, ".ufo/waves/round-3"), exist_ok=True)
        open(os.path.join(d, ".ufo/waves/round-3/w1-dispatch.json"), "w").write(
            json.dumps({"counts": {"spawn": 2}}) + "\n")
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "round-3 dispatch")
        text = card(rev).replace(
            "- corrects path .ufo/waves/round-9/w1-spec.json: landed\n",
            "- corrects path .ufo/waves/round-9/w1-spec.json: landed\n"
            "- corrects seats round-3: 1 waves, 2 seats total\n")
        commit_card(d, text, "card historical ghost")
    receipts.append(scen("sL-historical-ghost-correction", historical_ghost, out))

    def inf_spawn(d, rev):
        # int(float("inf")) raises OverflowError, which dispatch_counts does not catch
        open(os.path.join(d, ".ufo/waves/round-9/w2-dispatch.json"), "w").write(
            '{"counts": {"spawn": Infinity, "total": 32}}\n')
        sh("git", "-C", d, "add", "-A"); sh("git", "-C", d, "commit", "-q", "-m", "inf spawn")
        commit_card(d, card(rev), "card inf spawn")
    receipts.append(scen("sI-inf-spawn", inf_spawn, out))

    with open(os.path.join(S, "receipts", "index.json"), "w") as fh:
        json.dump(receipts, fh, indent=1)
    for r in receipts:
        print("%-34s exit=%d failing=%s reason=%s seats_mm=%s" %
              (r["name"], r["exit"], r["failing"], r["reason"],
               [m["derived"] for m in r["seats_mismatches"]]))


if __name__ == "__main__":
    main()
