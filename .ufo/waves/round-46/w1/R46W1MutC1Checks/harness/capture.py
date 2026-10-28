#!/usr/bin/env python3
"""Capture the probe matrix and the mutation matrix as citable receipts."""
import datetime
import hashlib
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kaidoku-r46/R46W1MutC1Checks"
REC = os.path.join(S, "receipts")
MUT = os.path.join(S, "mutants")

PAIRS = [
    ("p-g4-rows8-all-ids", ["head", "mutants/head-m4-rows-floor-8",
                            "base", "mutants/base-m4-rows-floor-8"]),
    ("p-g7-vocab-wrong-column", ["head", "mutants/head-m7-vocab-whole-row",
                                 "base", "mutants/base-m7-vocab-whole-row"]),
    ("p-g9-outside-allow", ["head", "mutants/head-m9-drop-allowlist",
                            "base", "mutants/base-m9-drop-allowlist"]),
    ("p-g10-refs3", ["head", "mutants/head-m10-drop-refs-min",
                     "base", "mutants/base-m10-drop-refs-min"]),
    ("p-g11-no-selector", ["head", "mutants/head-m11-no-line-selector",
                           "base", "mutants/base-m11-no-line-selector"]),
    ("p-g12-no-round45", ["head", "mutants/head-m12-must-cite-refs",
                          "base", "mutants/base-m12-must-cite-refs"]),
    ("p-h3-header-prefix", ["head", "mutants/head-m3-header-prefix",
                            "base", "mutants/base-m3-header-prefix"]),
    ("iso-ref-selector", ["head", "base"]),
    ("iso-ref-allow", ["head", "mutants/head-m9-drop-allowlist"]),
    ("p-arm-substring", ["head", "base"]),
    ("p-genuine", ["head", "base"]),
]


def utc():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main():
    env = dict(os.environ, TMPDIR=os.path.join(S, "tmpB"), HYAKU_SCRATCH=os.path.join(S, "scrB"))
    for k in ("TMPDIR", "HYAKU_SCRATCH"):
        os.makedirs(env[k], exist_ok=True)
    os.makedirs(os.path.join(S, "probe-root"), exist_ok=True)
    rows = []
    for probe, insts in PAIRS:
        for inst in insts:
            cmd = [sys.executable, os.path.join(S, "probe.py"), "--instrument",
                   os.path.join(S, inst), "--probe", probe]
            t = utc()
            r = subprocess.run(cmd, capture_output=True, text=True, env=env, cwd=S)
            try:
                d = json.loads(r.stdout)
            except Exception:  # noqa: BLE001
                d = {"exit": r.returncode, "stdout_head": (r.stdout + r.stderr)[:300]}
            rows.append({"utc": t, "cmd": " ".join(cmd), "probe": probe,
                         "instrument": inst, "harness_exit": r.returncode,
                         "result": d,
                         "stdout_sha256": hashlib.sha256(r.stdout.encode()).hexdigest()})
    with open(os.path.join(REC, "probes.jsonl"), "w") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

    # mutation matrix
    d = json.load(open(os.path.join(REC, "summary.json")))
    runs, meta = d["runs"], d["meta"]
    lines = ["# Mutation matrix — `tools/round-46/attest.py --selftest`",
             "",
             "Each run: `cd <dir> && TMPDIR=<dir>/tmp HYAKU_SCRATCH=<dir>/scr "
             "python3 -I -B attest.py --root /nonexistent --freeze deadbeef "
             "--rev deadbeef --selftest`.",
             "",
             "| version | mutant | one-change | exit | cases | failures | stdout sha256 | utc | verdict | cases that went red |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for ver in ("base", "head"):
        b = runs[f"{ver}-baseline"]
        lines.append(f"| {ver} | (baseline) | none | {b['exit']} | {b['cases']} | "
                     f"{b['failures']} | `{b['stdout_sha256']}` | {b['utc']} | BASELINE | — |")
        ok = {c["case"]: c["ok"] for c in b["case_rows"]}
        for mid in sorted({m["mutant"] for m in meta.values()}):
            r = runs[f"{ver}-{mid}"]
            flipped = [c["case"] for c in (r.get("case_rows") or [])
                       if ok.get(c["case"]) and not c["ok"]]
            verdict = "KILLED" if flipped else "SURVIVED"
            desc = meta[f"{ver}-{mid}"]["desc"].replace("|", "\\|")
            lines.append(f"| {ver} | {mid} | {desc} | {r['exit']} | {r.get('cases')} | "
                         f"{r.get('failures')} | `{r.get('stdout_sha256')}` | {r.get('utc')} | "
                         f"**{verdict}** | {', '.join(flipped) or '—'} |")
    open(os.path.join(REC, "mutation-matrix.md"), "w").write("\n".join(lines) + "\n")
    print("wrote", os.path.join(REC, "probes.jsonl"), "and mutation-matrix.md")
    print("probe rows:", len(rows))


if __name__ == "__main__":
    main()
