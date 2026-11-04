#!/usr/bin/env python3
"""Read-only recon: PROVINCE.md pointer cells under a strict exact-token rule."""
from __future__ import annotations
import hashlib, json, os, re, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "16dfa009bf143080dfcdfc5f9ec34bd359536d90"
OUT = os.path.join(LANE, ".ufo/waves/round-80/w1/ScoutRecord/probe.json")

RE_PIN = re.compile(r"(Devin|OMP|Kimi)\s+`rea-agents@([0-9][0-9.]*)`\s*\(`([^`]+)`\)")
RE_GHIDRA_PTR = re.compile(r"`([^`]*Ghidra/application\.properties):(\d+)`")
RE_GHIDRA_VALUE = re.compile(r"application\.version=([0-9][0-9.]*)")
RE_BASHRC_PTR = re.compile(r"`([^`]*\.bashrc):(\d+)(?:-(\d+))?`")
RE_POINTER = re.compile(r"^(?P<path>.+?):(?P<start>\d+)(?:-(?P<end>\d+))?$")
RE_TOKEN = re.compile(r"rea-agents@[0-9][0-9.]*")
CLASS = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._-")

BASHRC_TOKENS = ("GHIDRA_INSTALL_DIR=", "JAVA_HOME=")
DECLARED = {
    "devin-pin": "/home/vgpnk/.config/devin/mcp_config.json",
    "omp-pin": "/home/vgpnk/.omp/agent/mcp.json",
    "kimi-pin": "~/.kimi-code/config.toml",
    "ghidra-version": "<GHIDRA_INSTALL_DIR>/Ghidra/application.properties",
    "bashrc-exports": "/home/vgpnk/.bashrc",
}


def git_show(rev, path):
    p = subprocess.run(["git", "-C", LANE, "show", f"{rev}:{path}"], capture_output=True)
    if p.returncode != 0:
        raise SystemExit(f"git show failed: {p.stderr.decode()}")
    return p.stdout


def expand(path):
    return os.path.abspath(os.path.expanduser(path))


def ghidra_dir():
    env = os.environ.get("GHIDRA_INSTALL_DIR")
    if env:
        return env
    with open("/home/vgpnk/.bashrc", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = re.search(r"""export\s+GHIDRA_INSTALL_DIR=["']?([^"'\s]+)""", line)
            if m:
                return os.path.expandvars(os.path.expanduser(m.group(1)))
    return ""


def read_lines(path):
    try:
        with open(expand(path), encoding="utf-8", errors="replace") as fh:
            return fh.readlines()
    except OSError:
        return None


def whole_token_occurrences(line, token):
    """Return list of {start,end,left,right,whole} for every occurrence of token."""
    hits, start = [], 0
    while True:
        idx = line.find(token, start)
        if idx < 0:
            break
        end = idx + len(token)
        left = line[idx - 1] if idx > 0 else None
        right = line[end] if end < len(line) else None
        whole = (left is None or left not in CLASS) and (right is None or right not in CLASS)
        hits.append({"start": idx, "end": end,
                     "left": left, "right": right, "whole": whole})
        start = idx + 1
    return hits


def line_sha(lines):
    return hashlib.sha256("".join(lines).encode("utf-8")).hexdigest()


def main():
    text = git_show(BASE, "PROVINCE.md").decode("utf-8")
    prov_lines = text.splitlines(keepends=True)

    # ---- five cells exactly as the round-79 parser extracts them -------------
    pins = {}
    for name, pin, pointer in RE_PIN.findall(text):
        pins[name] = (pin, pointer)  # last-wins, mirrors round 79
    cells = []
    for client, cid in (("Devin", "devin-pin"), ("OMP", "omp-pin"), ("Kimi", "kimi-pin")):
        pin, pointer = pins[client]
        m = RE_PIN.search(text)
        # find the specific match for this client (last one, matching round-79 last-wins)
        mm = [m for m in RE_PIN.finditer(text) if m.group(1) == client][-1]
        cells.append({"id": cid, "client": client,
                      "cell_text": f"{client} `rea-agents@{pin}` (`{pointer}`)",
                      "pointer": pointer, "tokens": [f"rea-agents@{pin}"],
                      "match_start_line": text[:mm.start()].count("\n") + 1,
                      "match_span_lines": [text[:mm.start()].count("\n") + 1,
                                           text[:mm.end()].count("\n") + 1],
                      "record_line": next(i + 1 for i, ln in enumerate(prov_lines)
                                          if f"`rea-agents@{pin}` (`{pointer}`)" in ln)})
    gp = RE_GHIDRA_PTR.search(text)
    gv = RE_GHIDRA_VALUE.search(text)
    gd = ghidra_dir()
    gpointer = f"{gp.group(1)}:{gp.group(2)}"
    cells.append({"id": "ghidra-version", "client": "Ghidra",
                  "cell_text": f"`application.version={gv.group(1)}` (`{gpointer}`)",
                  "pointer": gpointer,
                  "tokens": [f"application.version={gv.group(1)}"],
                  "record_line": next(i + 1 for i, ln in enumerate(prov_lines)
                                      if gpointer.rsplit(":", 1)[0] in ln and f"application.version={gv.group(1)}" in ln)})
    bp = RE_BASHRC_PTR.search(text)
    bpointer = f"{bp.group(1)}:{bp.group(2)}" + (f"-{bp.group(3)}" if bp.group(3) else "")
    cells.append({"id": "bashrc-exports", "client": "bashrc",
                  "cell_text": f"`{bpointer}`",
                  "pointer": bpointer, "tokens": list(BASHRC_TOKENS),
                  "record_line": next(i + 1 for i, ln in enumerate(prov_lines)
                                      if bp.group(0) in ln)})

    # ---- bind each cell against its live pointed lines ----------------------
    for cell in cells:
        pointer = cell["pointer"]
        m = RE_POINTER.match(pointer)
        p = m.group("path")
        if p.startswith("<GHIDRA_INSTALL_DIR>"):
            p = p.replace("<GHIDRA_INSTALL_DIR>", gd)
        start, end = int(m.group("start")), int(m.group("end") or m.group("start"))
        lines = read_lines(p)
        pointed = lines[start - 1:end]
        cell["live_path"] = expand(p)
        cell["line_start"], cell["line_end"] = start, end
        cell["pointed_lines"] = [ln.rstrip("\n") for ln in pointed]
        cell["line_sha256"] = line_sha(pointed)
        cell["line_sha256_rstrip"] = hashlib.sha256(
            "".join(ln.rstrip("\n") for ln in pointed).encode("utf-8")).hexdigest()
        toks = []
        for token in cell["tokens"]:
            occurrences = []
            per_line = []
            for off, ln in enumerate(pointed):
                hits = whole_token_occurrences(ln, token)
                occurrences.extend(hits)
                per_line.append({"line": start + off,
                                 "hits": len(hits),
                                 "whole_hits": sum(1 for h in hits if h["whole"])})
            toks.append({"token": token, "occurrences": occurrences,
                         "per_line": per_line,
                         "whole_token": bool(occurrences) and all(h["whole"] for h in occurrences)})
        cell["tokens_detail"] = toks
        cell["whole_token"] = all(t["whole_token"] for t in toks)
        cell["bind_would_match"] = all(t["whole_token"] for t in toks)

    # ---- every other rea-agents@ occurrence in PROVINCE.md ------------------
    cell_lines = {c["record_line"] for c in cells if c["client"] != "Ghidra"
                  and c["client"] != "bashrc"}
    others = []
    for idx, ln in enumerate(prov_lines, 1):
        for tok in RE_TOKEN.findall(ln):
            if idx in cell_lines and idx in (16, 17, 18):
                kind = "pointer cell"
            else:
                kind = "other"
            hits = whole_token_occurrences(ln, tok)
            others.append({"line": idx, "token": tok, "kind": kind,
                           "whole_occurrences": [h for h in hits if h["whole"]],
                           "all_whole": all(h["whole"] for h in hits),
                           "context": ln.strip()[:200]})
    # RE_PIN matches: which record lines actually parse as client cells
    pin_matches = []
    for m in RE_PIN.finditer(text):
        line_no = text[:m.start()].count("\n") + 1
        pin_matches.append({"line": line_no, "match": m.group(0)})

    # ---- file lengths ------------------------------------------------------
    files = {
        "devin": "/home/vgpnk/.config/devin/mcp_config.json",
        "omp": "/home/vgpnk/.omp/agent/mcp.json",
        "kimi": "/home/vgpnk/.kimi-code/config.toml",
        "bashrc": "/home/vgpnk/.bashrc",
        "ghidra_properties": "/home/vgpnk/.local/opt/ghidra_12.1.4_PUBLIC/Ghidra/application.properties",
    }
    file_lengths = {}
    for name, path in files.items():
        data = open(path, "rb").read()
        with open(path, encoding="utf-8", errors="replace") as fh:
            n = sum(1 for _ in fh)
        file_lengths[name] = {"path": path, "bytes": len(data), "lines_wc_l": n,
                              "sha256": hashlib.sha256(data).hexdigest()}

    receipt = {
        "schema": "kaidoku-r80-scoutrecord-v1",
        "round": 80,
        "base": BASE,
        "lane": LANE,
        "declaration_guard": subprocess.run(
            ["git", "-C", LANE, "log", "-1", "--format=%H", "--", "plans/round-80-claims.md"],
            capture_output=True, text=True).stdout.strip(),
        "province_lines": len(prov_lines),
        "ghidra_install_dir": gd,
        "cells": cells,
        "pin_matches": pin_matches,
        "rea_agents_occurrences": others,
        "file_lengths": file_lengths,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2)
        fh.write("\n")
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
