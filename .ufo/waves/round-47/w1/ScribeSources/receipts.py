#!/usr/bin/env python3
"""ScribeSources round-47 receipt driver: every check emits argv, exit, stdout sha256, UTC."""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone

S = os.path.dirname(os.path.abspath(__file__))
ROOT = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FREEZE = "5017e1f7299c3a812e87e7950148f54313dd279e"
OUT = os.path.join(S, "receipts.jsonl")
rows = []


def rec(label, argv, rc, out, extra=None):
    row = {
        "label": label,
        "argv": argv,
        "exit": rc,
        "stdout_sha256": hashlib.sha256(out.encode()).hexdigest(),
        "stdout_bytes": len(out.encode()),
        "utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }
    if extra:
        row.update(extra)
    rows.append(row)
    return row


def run(label, argv, cwd=S, extra=None, env=None):
    envcopy = dict(os.environ)
    if env:
        envcopy.update(env)
    p = subprocess.run(argv, capture_output=True, text=True, cwd=cwd, env=envcopy)
    out = p.stdout + p.stderr
    r = rec(label, argv, p.returncode, out, extra)
    print(label, "exit", p.returncode, r["stdout_sha256"][:16], "|", out.strip().splitlines()[:1])
    return out


def fetch(label, url, path):
    out = run(label, ["curl", "-sS", "-o", path, "-w", "http=%{http_code} bytes=%{size_download}",
                      url])
    meta = dict(kv.split("=") for kv in out.strip().split())
    digest = run(label + "-sha256", ["sha256sum", path], extra={"http": meta["http"],
                                                                "download_bytes": int(meta["bytes"])})
    return meta, digest.strip().split()[0]


def extract(label, path, *needles, window=1400):
    """Locate each needle in the stripped text of path; emit the surrounding text."""
    text = open(path, encoding="utf-8", errors="replace").read()
    stripped = re.sub(r"<[^>]+>", "", text)
    stripped = re.sub(r"\n{2,}", "\n", stripped)
    found = {}
    for n in needles:
        i = stripped.find(n)
        found[n] = re.sub(r"\s+", " ", stripped[i:i + window]) if i >= 0 else None
    payload = json.dumps({"needles": list(needles), "found": found}, sort_keys=True)
    rc = 0 if all(v is not None for v in found.values()) else 1
    rec(label, ["<python>", "extract", path, *needles], rc,
        payload, {"located": {k: v is not None for k, v in found.items()}})
    print(label, "exit", rc, {k: bool(v) for k, v in found.items()})
    return found


def main():
    # --- S143 candidate: the Python `re` page, /3/ alias ---
    meta_re, sha_re = fetch("R01-curl-re-3", "https://docs.python.org/3/library/re.html", "re.html")
    run("R02-re-anchor", ["grep", "-c", 'id="re.fullmatch"', "re.html"])
    q_re = extract("R03-re-fullmatch-text", "re.html", "re.fullmatch(pattern, string, flags=0)")
    run("R04-re-version", ["grep", "-o", r"Python 3\.1[0-9]", "re.html"])

    # --- version-pinned 3.14 pages ---
    meta_re314, sha_re314 = fetch("R05-curl-re-3.14", "https://docs.python.org/3.14/library/re.html",
                                  "p314-re.html")
    extract("R06-re314-fullmatch-text", "p314-re.html", "re.fullmatch(pattern, string, flags=0)")

    # --- S144 candidate: cmdline -I / -B ---
    meta_cli, sha_cli = fetch("R07-curl-cmdline-3", "https://docs.python.org/3/using/cmdline.html",
                              "cmdline.html")
    q_isolated = extract("R08-cmdline-I-text", "cmdline.html", "Run Python in isolated mode")
    extract("R09-cmdline-B-text", "cmdline.html", "won’t try to write .pyc files")
    meta_cli314, sha_cli314 = fetch("R10-curl-cmdline-3.14",
                                    "https://docs.python.org/3.14/using/cmdline.html",
                                    "p314-cmdline.html")
    extract("R11-cmdline314-I-text", "p314-cmdline.html", "Run Python in isolated mode")

    # --- S145 candidate: hashlib ---
    meta_hash, sha_hash = fetch("R12-curl-hashlib-3", "https://docs.python.org/3/library/hashlib.html",
                                "hashlib.html")
    extract("R13-hashlib-concat-text", "hashlib.html", "digest of the concatenation of the data fed")

    # --- reject candidate: regex HOWTO ---
    meta_howto, sha_howto = fetch("R14-curl-regex-howto", "https://docs.python.org/3/howto/regex.html",
                                  "regex.html")
    extract("R15-howto-abstract-text", "regex.html", "introductory tutorial to using regular expressions")

    # --- duplicate check: S142 / git-log --diff-merges ---
    meta_git, sha_git = fetch("R16-curl-git-log", "https://git-scm.com/docs/git-log", "gitlog.html")

    # --- live interpreter corroboration of -I ---
    run("R17-interp-version", ["python3", "-V"])
    run("R18-I-flags", ["python3", "-I", "-B", "-c",
                        "import sys;print('isolated',sys.flags.isolated,'nowrite',sys.flags."
                        "dont_write_bytecode,'safe_path',sys.flags.safe_path,'ignore_env',"
                        "sys.flags.ignore_environment,'no_user_site',sys.flags.no_user_site)"])
    run("R19-PYTHONPATH-with-I", ["python3", "-I", "-B", "-c",
                                  "import sys;print('/evil' in ' '.join(sys.path))"],
        extra={"env": {"PYTHONPATH": "/evil"}})
    run("R20-PYTHONPATH-without-I", ["python3", "-B", "-c",
                                     "import sys;print('/evil' in ' '.join(sys.path))"],
        extra={"env": {"PYTHONPATH": "/evil"}})

    # --- frozen-path state of the lane (read-only) ---
    run("R21-hash-object", ["git", "hash-object", "tools/round-47/record.py",
                            "tools/round-47/exact.py"], cwd=ROOT)
    run("R22-freeze-blobs", ["git", "rev-parse", f"{FREEZE}:tools/round-47/record.py",
                             f"{FREEZE}:tools/round-47/exact.py"], cwd=ROOT)
    run("R23-frozen-tree", ["git", "ls-tree", "-r", "--name-only", FREEZE, "--", "tools/round-47/"],
        cwd=ROOT)
    run("R24-status-round47", ["git", "status", "--porcelain", "tools/round-47/"], cwd=ROOT)
    run("R25-registry-max", ["grep", "-c", r"^| S14", "corpus/SOURCES.md"], cwd=ROOT)
    run("R26-registry-S143-at-freeze", ["git", "show", f"{FREEZE}:corpus/SOURCES.md"],
        cwd=ROOT, extra={"note": "counted by R27"})

    with open(OUT, "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    print("wrote", OUT, len(rows), "receipts")
    print("pins", json.dumps({
        "re-3": {"http": meta_re["http"], "bytes": int(meta_re["bytes"]), "sha256": sha_re},
        "re-3.14": {"http": meta_re314["http"], "bytes": int(meta_re314["bytes"]), "sha256": sha_re314},
        "cmdline-3": {"http": meta_cli["http"], "bytes": int(meta_cli["bytes"]), "sha256": sha_cli},
        "cmdline-3.14": {"http": meta_cli314["http"], "bytes": int(meta_cli314["bytes"]),
                         "sha256": sha_cli314},
        "hashlib-3": {"http": meta_hash["http"], "bytes": int(meta_hash["bytes"]), "sha256": sha_hash},
        "howto": {"http": meta_howto["http"], "bytes": int(meta_howto["bytes"]), "sha256": sha_howto},
        "git-log": {"http": meta_git["http"], "bytes": int(meta_git["bytes"]), "sha256": sha_git},
        "isolated_text": q_isolated.get("Run Python in isolated mode"),
    }, indent=1))


if __name__ == "__main__":
    sys.exit(main())
