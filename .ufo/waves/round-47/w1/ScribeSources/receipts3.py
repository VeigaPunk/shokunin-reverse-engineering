#!/usr/bin/env python3
"""ScribeSources round-47 receipt pass 3: does the C1 counter's freeze gate make the
*first* declared freeze unscoreable once the sibling frozen file changed?"""
import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone

S = os.path.dirname(os.path.abspath(__file__))
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
rows = []


def run(label, argv, cwd):
    env = dict(os.environ)
    env["TMPDIR"] = S
    p = subprocess.run(argv, capture_output=True, text=True, cwd=cwd, env=env)
    out = p.stdout + p.stderr
    row = {"label": label, "argv": argv, "exit": p.returncode,
           "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
           "stdout_bytes": len(out.encode()),
           "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
    try:
        doc = json.loads(p.stdout)
        row["reason"] = doc.get("reason")
        row["frozen_path_changed"] = doc.get("frozen_path_changed")
        row["dirty"] = doc.get("dirty")
        row["failing"] = doc.get("failing")
    except Exception:
        row["stdout_head"] = out[:400]
    rows.append(row)
    print(label, "exit", p.returncode, json.dumps({k: row.get(k) for k in
                                                   ("reason", "frozen_path_changed", "failing")})[:220])
    return row


head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                      text=True).stdout.strip()
print("HEAD", head, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
for freeze, label in (("5017e1f7299c3a812e87e7950148f54313dd279e", "T01-first-freeze"),
                      ("9018c53b" , "T02-A1"),
                      ("1e2c3102952dc636650095643c1963c833859019", "T03-A4")):
    run(f"{label}-vs-HEAD", ["python3", "-I", "-B", "tools/round-47/exact.py",
                             "--root", ROOT, "--freeze", freeze, "--rev", head,
                             "--no-battery"], ROOT)
with open(os.path.join(S, "receipts3.jsonl"), "w", encoding="utf-8") as fh:
    for r in rows:
        fh.write(json.dumps(r, sort_keys=True) + "\n")
print("wrote receipts3.jsonl", len(rows))
