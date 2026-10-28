#!/usr/bin/env python3
"""CritBattery receipt runner: every attacked command, with exit, stdout sha256 and UTC."""
import datetime
import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
OUT = os.path.join(LANE, ".ufo/waves/round-47/w1/CritBattery/receipts")
S = os.environ["HYAKU_SCRATCH"]
os.makedirs(OUT, exist_ok=True)
ENV = dict(os.environ, TMPDIR=S, HYAKU_SCRATCH=S)
PY = [sys.executable, "-I", "-B"]
rows = []


def run(name, argv, cwd=LANE, note=""):
    t = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    r = subprocess.run(argv, cwd=cwd, capture_output=True, text=True, env=ENV)
    sha = hashlib.sha256(r.stdout.encode()).hexdigest()
    payload = {"name": name, "argv": argv, "cwd": cwd, "exit": r.returncode,
               "utc": t, "stdout_sha256": sha, "note": note,
               "stdout_head": r.stdout.strip().splitlines()[:1],
               "stderr_head": r.stderr.strip().splitlines()[:2]}
    with open(os.path.join(OUT, name + ".stdout"), "w") as fh:
        fh.write(r.stdout)
    rows.append(payload)
    print(json.dumps(payload)[:400])
    return r


exact = [os.path.join(LANE, "tools/round-47/exact.py")]
record = [os.path.join(LANE, "tools/round-47/record.py")]

run("c1-declared-pair", PY + exact + ["--root", LANE, "--freeze", "f54b3b6d",
                                      "--rev", "a0753786"],
    note="the SCORECARD's declared freeze/rev pair")
run("c1-claims-freeze-at-declared-rev", PY + exact + [
    "--root", LANE, "--freeze", "5017e1f7", "--rev", "a0753786", "--no-battery"],
    note="the freeze the frozen claims file defines, at the declared measured revision")
run("c1-claims-freeze-rev-line", PY + exact + [
    "--root", LANE, "--freeze", "62e33f7d", "--rev", "a0753786", "--no-battery"],
    note="freeze re-derived by `git log -1 -- plans/round-47-claims.md`")
run("c1-freeze-blob-vs-landing", PY + [os.path.join(S, "t5017/tools/round-47/exact.py"),
                                       "--root", LANE, "--freeze", "e856beb5",
                                       "--rev", "e856beb5", "--no-battery"],
    note="exact.py@5017e1f7 (sha dcef54f1...) scoring the round's landing block")
run("c1-variants", PY + [os.path.join(S, "drv_c1.py"), "31b092d1", S],
    note="blobberish / one-cell substring / 4-row duplicate id / block asserts reversed order")
run("c1-denominator-coforgery", PY + [os.path.join(S, "drv_denominator.py"), "31b092d1"],
    note="fixture exact.py with flag-order-drift replaced by a second substring-arm")
run("c2-base-control", PY + record + ["--root", LANE, "--rev", "13a9e9e1", "--no-battery"],
    note="do-nothing control at the base")
run("c2-declared-rev", PY + record + ["--root", LANE, "--rev", "a0753786"],
    note="the declared measured revision")
run("c2-at-head", PY + record + ["--root", LANE, "--rev", "31b092d1"],
    note="HEAD at the time of this attack")
run("c2-attacks-31b092d1", PY + [os.path.join(S, "drv_c2c.py"), "31b092d1"],
    note="launderings: seats pair, window base/pathspec, false axes corrections, measured-at swap")
run("c2-attacks-1e2c3102", PY + [os.path.join(S, "drv_c2c.py"), "1e2c3102"],
    note="A4 card, where the round-45 seats atom is still inside the graded window")
run("c2-tampered-interpreter", PY + [os.path.join(S, "tpy/tools/round-47/record.py"),
                                     "--root", LANE, "--rev", "13a9e9e1"],
    note="a 3-line edit to the unpinned record.py against the base card")
run("c2-receipt-vs-row", PY + ["-c", (
    "import json,subprocess;"
    "card=subprocess.run(['git','-C',%r,'show','31b092d1:SCORECARD.md'],"
    "capture_output=True,text=True).stdout;"
    "d=json.load(open(%r));"
    "print(json.dumps({'row_atoms':'atoms 50' in card,'receipt_atoms':d['atoms'],"
    "'row_exempted':'exempted 2 <= 3' in card,'receipt_exempted':len(d['exempted']),"
    "'receipt_corrections':d['corrections'],'card_corrects_lines':card.count(chr(10)+'- corrects ')}))"
) % (LANE, os.path.join(LANE, ".ufo/waves/round-47/l1/scores/c2-at-A7.json"))],
    note="the landed after-cell against the receipt it cites")

with open(os.path.join(OUT, "manifest.jsonl"), "w") as fh:
    for r in rows:
        fh.write(json.dumps(r) + "\n")
print("MANIFEST", os.path.join(OUT, "manifest.jsonl"), len(rows))
