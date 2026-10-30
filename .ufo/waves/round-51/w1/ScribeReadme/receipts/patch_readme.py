#!/usr/bin/env python3
"""Apply the R51-C1 corpus/README.md drafts to a scratch copy of the lane README and
check the shape of the result.  Read-only on the lane tree: the lane file is only read.

The checks mirror the frozen lane logic:
  * section()/cells()  -> tools/round-50/c1-counter.py:571-586
  * coverage_map_row   -> tools/round-50/c1-counter.py:2479-2482
  * map_token/b1()     -> tools/round-50/c2-record.py:490-517
  * unique_section()   -> tools/round-50/c2-record.py:337-339
"""
import difflib
import hashlib
import os
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r51/w1-ScribeReadme"
BASE_REL = "corpus/README.md"
STEM = "2026-10-30-r51-avm-le-squashfs-core"
ENTRY = "corpus/knowledge/%s.md" % STEM
FRONTIER_MARK = "Round-51 frontier note"
LE_AVM_RE = re.compile(r"\bLE[ _-]AVM\b|\bAVM[ _-]LE\b", re.IGNORECASE)


def section(text, heading):
    lines = text.splitlines()
    try:
        i = lines.index(heading)
    except ValueError:
        return None
    out = []
    for line in lines[i + 1:]:
        if line.startswith("## "):
            break
        out.append(line)
    return out


def cells(row):
    return [c.strip() for c in row.strip().strip("|").split("|")]


def map_token(stem):
    return re.compile(r"`(?:corpus/)?(?:knowledge/)?%s(?:\.md)?`" % re.escape(stem))


COVERAGE_ROW = (
    "| SquashFS LE AVM members (round 51) | `2026-10-30-r51-avm-le-squashfs-core` | "
    "**Core** — REA 6.5.0 `extract-firmware --max-depth 1` (unblob 26.6.4, `sasquatch` 4.5.1 on the "
    "child `PATH`) resolves the `squashfs_v4_le` handler on the four chain-pinned genuine "
    "AVM-marker little-endian members (FRITZ!Box 7581 07.18, 7582 07.18, 6490 Cable 07.57, 6430 "
    "Cable 07.30) and publishes every regular file of the independent `unsquashfs` 4.7.5 oracle at "
    "its exact path on all four (R51-C1 `carriers_matched 4`, `gaps_ok` true on every carrier, "
    "every binding true); the gap accounting is now the device-accounting law, re-frozen from the "
    "per-carrier-class derivation (`tools/round-51/gap-rule.json`, `tools/round-51/c1-counter.py` "
    "v2) — an unprivileged extraction creates no device nodes, fifos or sockets and emits no gap "
    "record for them, so a non-regular oracle entry carries no disposition at all — not the "
    "round-50 detail whitelist that generalised `247:0` from the Cable class; the carrier bytes are "
    "fetched through the pinned chain and never committed (AVM licence), so the durable evidence is "
    "the committed receipt set `corpus/evidence/round-51/c1/<id>/run.json` (`<id>` = `c6430`, "
    "`c6490`, `g7581`, `g7582`), the frozen oracle tables and the pin chain; the before/after "
    "scores are `.ufo/waves/round-51/l1/scores/c1-{before,after}.json`; LE AVM kernels, the "
    "~13k-file LE AVM rootfs under REA's 120 s limit and the other still-frontier SquashFS variants "
    "stay Frontier |"
)

KNOWLEDGE_ROW = (
    "| `2026-10-30-r51-avm-le-squashfs-core` | genuine AVM-marker LE SquashFS v4 (`hsqs`) through "
    "REA on four pinned vendor members — Core (R51-C1 under the re-frozen device-accounting rule: "
    "4 of 4 carriers, every oracle regular file published at its exact path) | S243, S244, S245, "
    "S249, <S??? round-51 device-node source row(s)>; receipts `corpus/evidence/round-51/c1/`; "
    "counter `tools/round-51/c1-counter.py` | 2026-10-30 |"
)

FRONTIER_BULLET = (
    "- sasquatch — 2026-10-30 round 51 (Round-51 frontier note): LE AVM members (`hsqs`) moved "
    "Frontier → Core (`2026-10-30-r51-avm-le-squashfs-core`; REA 6.5.0 `extract-firmware "
    "--max-depth 1` publishes every regular file of the independent `unsquashfs` 4.7.5 oracle on "
    "all four chain-pinned vendor carriers — FRITZ!Box 7581/7582 07.18 and 6490/6430 Cable "
    "07.57/07.30 — and R51-C1 re-froze the gap accounting from the per-carrier-class derivation, "
    "the device-accounting law: an unprivileged extraction creates no device nodes, fifos or sockets "
    "and emits no gap record for them, so a non-regular oracle entry carries no disposition at all; "
    "the carrier bytes are fetched and never committed, AVM licence). This supersedes the LE-AVM "
    "clause of the round-49 line above and the LE-AVM clause of the round-50 frontier note below "
    "(2 of 4 under the round-50 detail whitelist `removed.silent.char-device: [\"247:0\"]`). "
    "Scope: four pinned carriers, one vendor, xz bodies, depth 1. Still frontier: the LE AVM rootfs "
    "of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590), AVM kernels, nested sub-images "
    "below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard` (and the "
    "DD-WRT no-pad/4k-pad v3 images), gzip v3 bodies, v4 Broadcom, v2.1 images."
)

FRONTIER_NOTE = (
    "Round-51 frontier note, 2026-10-30: LE AVM members (`hsqs`) moved Frontier → Core "
    "(`2026-10-30-r51-avm-le-squashfs-core`; REA published every oracle regular file on all four "
    "chain-pinned vendor carriers, and R51-C1 re-froze the gap accounting from the "
    "per-carrier-class derivation — the device-accounting law: an unprivileged extraction creates no "
    "device nodes, fifos or sockets and emits no gap record for them, so a non-regular oracle entry "
    "carries no disposition at all — so the counter matched 4 of 4 under the law-derived rule). This "
    "note supersedes the LE-AVM clause of the round-50 frontier note above (2 of 4 under the "
    "round-50 detail whitelist, which generalised `247:0` from the Cable-carrier class) and the "
    "LE-AVM clause of the round-40/41/44/49 notes' Still-Frontier lists, and nothing else. Still "
    "Frontier: LE AVM rootfs of ~13k files under REA's 120 s limit (FRITZ!Box 7530/7590), AVM "
    "kernels, nested sub-images below depth 1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, "
    "`squashfs_v3_nonstandard`, gzip v3 bodies, v4 Broadcom."
)


def main():
    base_path = os.path.join(LANE, BASE_REL)
    base = open(base_path, encoding="utf-8").read()
    base_sha = hashlib.sha256(base.encode()).hexdigest()
    out = []
    out.append("lane README: %s" % base_path)
    out.append("base sha256: %s" % base_sha)
    out.append("base lines: %d" % len(base.splitlines()))
    lines = base.splitlines()

    # anchors (unique)
    r50_cov = [i for i, l in enumerate(lines) if l.startswith("| SquashFS LE AVM members (round 50) |")]
    r49_bul = [i for i, l in enumerate(lines)
               if l.startswith("- sasquatch — 2026-10-28 round 49:")]
    r50_note = [i for i, l in enumerate(lines) if l.startswith("Round-50 frontier note, 2026-10-29:")]
    r50_krow = [i for i, l in enumerate(lines)
                if l.startswith("| `2026-10-28-r50-avm-le-squashfs-core` |")]
    assert len(r50_cov) == 1, r50_cov
    assert len(r49_bul) == 1, r49_bul
    assert len(r50_note) == 1, r50_note
    assert len(r50_krow) == 1, r50_krow
    out.append("anchors: r50 coverage row L%d, r49 bullet L%d, r50 note L%d, r50 knowledge row L%d"
               % (r50_cov[0] + 1, r49_bul[0] + 1, r50_note[0] + 1, r50_krow[0] + 1))

    new = list(lines)
    # 1. coverage row after the round-50 coverage row
    new.insert(r50_cov[0] + 1, COVERAGE_ROW)
    # 2. knowledge-index row after the round-50 knowledge row
    idx = [i for i, l in enumerate(new) if l.startswith("| `2026-10-28-r50-avm-le-squashfs-core` |")][0]
    new.insert(idx + 1, KNOWLEDGE_ROW)
    # 3. new frontier bullet after the round-49 bullet
    idx = [i for i, l in enumerate(new) if l.startswith("- sasquatch — 2026-10-28 round 49:")][0]
    new.insert(idx + 1, FRONTIER_BULLET)
    # 4. new dated note after the round-50 note (end of file)
    idx = [i for i, l in enumerate(new) if l.startswith("Round-50 frontier note, 2026-10-29:")][0]
    new.insert(idx + 1, FRONTIER_NOTE)
    patched = "\n".join(new) + "\n"

    patched_path = os.path.join(SCRATCH, "README.patched.md")
    with open(patched_path, "w", encoding="utf-8") as fh:
        fh.write(patched)
    out.append("patched: %s (sha256 %s)" % (patched_path, hashlib.sha256(patched.encode()).hexdigest()))

    # ---- checks -------------------------------------------------------
    cm = section(patched, "## Coverage map")
    out.append("check coverage_map_row (counter 2479-2482): %s"
               % any(STEM in l for l in cm if l.lstrip().startswith("|")))
    row = [l for l in cm if STEM in l and l.lstrip().startswith("|")][0]
    c = cells(row)
    out.append("check coverage row cells: %d (want 3) -> %s" % (len(c), len(c) == 3))
    out.append("check coverage row cells (c2-record cells()): %d (want 3) -> %s"
               % (len(cells(row)), len(cells(row)) == 3))
    out.append("check no '|' inside any cell: %s"
               % all("|" not in x for x in c))
    krow = [l for l in section(patched, "## Knowledge") if STEM in l and l.lstrip().startswith("|")][0]
    kc = cells(krow)
    out.append("check knowledge row cells: %d (want 4) -> %s" % (len(kc), len(kc) == 4))
    out.append("check map_token match in ## Coverage map: %s"
               % bool(map_token(STEM).search("\n".join(cm))))
    # b1 simulation: every knowledge file mapped
    files = sorted(f for f in os.listdir(os.path.join(LANE, "corpus", "knowledge"))
                   if f.endswith(".md"))
    unmapped = [f for f in files
                if not map_token(f[:-3]).search("\n".join(cm))]
    out.append("check b1 mapping: %d knowledge files, unmapped %s" % (len(files), unmapped))
    out.append("check b1 mapping with the new entry present: %d files, unmapped %s"
               % (len(files) + 1, [f for f in unmapped + [STEM + ".md"]
                                  if not map_token(f[:-3]).search("\n".join(cm))]))
    for head in ("## Coverage map", "## Knowledge", "## Frontier"):
        n = sum(1 for l in patched.splitlines() if l.strip() == head)
        out.append("check unique_section %s: %d (want 1) -> %s" % (head, n, n == 1))
    fr = section(patched, "## Frontier")
    fr_bullets = [l for l in fr if l.startswith("- ")]
    out.append("check frontier last bullet is the r51 one: %s"
               % fr_bullets[-1].startswith("- sasquatch — 2026-10-30 round 51"))
    tail = fr_bullets[-1].split("Still frontier:", 1)[-1]
    out.append("check r51 bullet still-frontier list has no 'LE AVM members (`hsqs`)': %s"
               % ("LE AVM members (`hsqs`)" not in tail))
    out.append("check r51 bullet still-frontier list: %s" % tail.strip())
    hits = [l for l in patched.splitlines()
            if FRONTIER_MARK in l and STEM in l
            and LE_AVM_RE.search(l.replace(STEM, ""))]
    out.append("check frontier-note shape in README (mark+stem+LE-AVM token): %d line(s) -> %s"
               % (len(hits), bool(hits)))
    residue = [(i + 1, l[:90]) for i, l in enumerate(patched.splitlines())
               if "LE AVM members (`hsqs`)" in l and "2026-10-30" not in l and not l.startswith("- sasquatch — 2026-10-30")]
    out.append("residue: historical lines still naming 'LE AVM members (`hsqs`)': %s"
               % [n for n, _ in residue])
    diff = list(difflib.unified_diff(base.splitlines(), patched.splitlines(),
                                     fromfile="corpus/README.md (base)", tofile="corpus/README.md (patched)",
                                     lineterm="", n=0))
    out.append("diff hunks: %d, changed lines: +%d/-%d"
               % (sum(1 for d in diff if d.startswith("@@")),
                  sum(1 for d in diff if d.startswith("+") and not d.startswith("+++")),
                  sum(1 for d in diff if d.startswith("-") and not d.startswith("---"))))
    patch_path = os.path.join(SCRATCH, "readme-r51.patch")
    with open(patch_path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(diff) + "\n")
    out.append("patch file: %s" % patch_path)
    out.append("EXITS: all shape checks above are informational; the verdict is the reviewer's.")
    print("\n".join(out))


if __name__ == "__main__":
    main()
