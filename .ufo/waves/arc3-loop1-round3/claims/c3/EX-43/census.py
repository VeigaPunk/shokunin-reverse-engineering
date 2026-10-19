#!/usr/bin/env python3
"""EX-43 (c3, arc3-loop1-round3) before-state census + candidate-entry validation.

Read-only over the repo (no git objects written, no table edited): the real
pointer table is copied to scratch, candidate arc3-era entries are appended to
the COPY, a scratch expected.json is pinned to the copy's digest, and the probe
grades the copy against HEAD. Outputs land under claims/c3/EX-43/.
"""
import copy
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

REPO = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = "/var/tmp/ex43-scratch"
OUTDIR = os.path.join(REPO, ".ufo/waves/arc3-loop1-round3/claims/c3/EX-43")
TABLE = os.path.join(REPO, ".ufo/gates/citation-drift/pointer-table.json")
EXPECTED = os.path.join(REPO, ".ufo/gates/citation-drift/expected.json")
PROBE = os.path.join(REPO, ".ufo/gates/citation-drift/citation-drift-probe.py")
R1ENTRY = "corpus/knowledge/2026-10-19-arc3-r1-evm-real-solc.md"
R307 = "corpus/knowledge/2026-10-13-r3-evm-interface.md"
R307PAT = "2026-10-13-r3-evm-interface\\.md:(\\d+)-(\\d+)"

# ---------------------------------------------------------------- candidates
ENTRY_CANDIDATES = [
    {
        "id": "r1evm-cites-r307-erratum-offset",
        "kind": "extracted",
        "file": R1ENTRY,
        "line": 17,
        "pattern": R307PAT,
        "target": R307,
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "JUMPDEST dispatch-target position",
        "note": "the arc3-r1 entry's own citation of the r3-07 round-4 offset erratum; the named range must keep carrying the offset-semantics correction.",
    },
    {
        "id": "r1evm-cites-r307-stub-inference",
        "kind": "extracted",
        "file": R1ENTRY,
        "line": 18,
        "pattern": R307PAT,
        "target": R307,
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "inferred_state_mutability",
        "note": "the arc3-r1 entry's delta claim contrasts its real-carrier signal against the r3-07 stub lines; the named range must keep the stub-inference record.",
    },
    {
        "id": "r1evm-cites-quality-id-domain",
        "kind": "extracted",
        "file": R1ENTRY,
        "line": 21,
        "pattern": "QUALITY\\.md:(\\d+)-(\\d+)",
        "target": "corpus/QUALITY.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "full domain",
        "note": "the no-content-addressed-identity-claim observation cites the QUALITY rows on evidence-id domains; the named range must keep the domain rule.",
    },
    {
        "id": "r1evm-cites-quality-parsed-empty",
        "kind": "extracted",
        "file": R1ENTRY,
        "line": 24,
        "pattern": "QUALITY\\.md:(\\d+)",
        "target": "corpus/QUALITY.md",
        "target_group": 1,
        "must_match": "parsed-and-empty",
        "note": "the creation-code observation cites the parsed-and-empty quality row; the named line must keep the distinction.",
    },
    {
        "id": "r1evm-cites-r307-kind-hypothesis",
        "kind": "extracted",
        "file": R1ENTRY,
        "line": 25,
        "pattern": R307PAT,
        "target": R307,
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "richer bytecode",
        "note": "the entry's refuted-hypothesis record cites the r3-07 candidate-2 lines it refutes; the named range must keep the hypothesis text.",
    },
    {
        "id": "r1evm-cites-r307-positional-encoding",
        "kind": "extracted",
        "file": R1ENTRY,
        "line": 26,
        "pattern": R307PAT,
        "target": R307,
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "POSITIONAL arg",
        "note": "the input-shape-traps observation cites the r3-07 positional-encoding quirk; the named range must keep it.",
    },
    {
        "id": "readme38-arc3-r1-map-token",
        "kind": "anchor",
        "file": "corpus/README.md",
        "must_match": "2026-10-19-arc3-r1-evm-real-solc",
        "note": "arc3-r1's line-neutral map token in the knowledge map's EVM row; the token must keep naming the entry. Line deliberately unpinned (the map row is append-managed).",
    },
    {
        "id": "sc1435-shonen-refresh-record",
        "kind": "extracted",
        "file": "SCORECARD.md",
        "line": 1435,
        "pattern": "SHONEN\\.md:(\\d+)",
        "target": "SHONEN.md",
        "target_group": 1,
        "must_match": "14/14",
        "note": "the arc3-r2 SCORECARD record states the SHONEN.md:6 refresh (range 81-255, 14/14); the named line must keep resolving to the 14/14 assertion.",
    },
    {
        "id": "skill-rule14-cr2-stale-identity",
        "kind": "extracted",
        "file": "SKILL.md",
        "line": 246,
        "pattern": "arc3-loop1-round1/seats/CR-2\\.md:(\\d+)-(\\d+)",
        "target": ".ufo/waves/arc3-loop1-round1/seats/CR-2.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "stale against the",
        "note": "queue-drain rule #14's measured-origin citation (the stale self-identity finding); the named CR-2 range must keep the finding.",
    },
    {
        "id": "skill-rule14-verdict-d9",
        "kind": "extracted",
        "file": "SKILL.md",
        "line": 248,
        "pattern": "arc3-loop1-round1/claims/c1/verdict\\.md:(\\d+)-(\\d+)",
        "target": ".ufo/waves/arc3-loop1-round1/claims/c1/verdict.md",
        "target_group": 1,
        "target_group_end": 2,
        "must_match": "Three different applied identities",
        "note": "rule #14's chain-measurement citation (debt D9); the named verdict range must keep the three-identities record.",
    },
    {
        "id": "skill-rule14-r1evm-recheck-line",
        "kind": "extracted",
        "file": "SKILL.md",
        "line": 252,
        "pattern": "2026-10-19-arc3-r1-evm-real-solc\\.md:(\\d+)",
        "target": R1ENTRY,
        "target_group": 1,
        "must_match": "recheck:",
        "note": "rule #14's landed-entry citation: the entry's recheck line as the landing record; the named line must keep the recheck form.",
    },
    {
        "id": "skill-registry-row-citation-drift",
        "kind": "anchor",
        "file": "SKILL.md",
        "must_match": "\\| citation-drift \\| probe / kaidoku \\|",
        "note": "arc3-r1's registry row for the probe (the round that landed the frozen-run guard); the row must keep existing. Line deliberately unpinned (lane-appended file, rule #11 form).",
    },
    {
        "id": "skill-registry-row-custody-pair",
        "kind": "anchor",
        "file": "SKILL.md",
        "must_match": "\\| custody-pair \\| tool / kaidoku \\|",
        "note": "arc3-r2's registry row for the custody instrument; the row must keep existing. Line deliberately unpinned.",
    },
    {
        "id": "custody-readme-v1-stanza-example",
        "kind": "anchor",
        "file": ".ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair.txt",
        "must_match": "capture-utc: 2026-10-19T09:57:18Z",
        "note": "custody-pair README names this file as the in-tree stanza-v1 example; the example must keep existing with its capture stamp.",
    },
    {
        "id": "custody-readme-v1-sums-example",
        "kind": "anchor",
        "file": ".ufo/waves/arc3-loop1-round1/claims/c3/EX-26/custody-sha256.txt",
        "must_match": "16f496e6",
        "note": "README names this file as the in-tree sums-v1 example; the example must keep existing (its first custody digest pinned here).",
    },
    {
        "id": "custody-readme-v1-pipe-example",
        "kind": "anchor",
        "file": ".ufo/waves/arc3-loop1-round1/claims/cross/receipts/config-pre-pair-metadata.txt",
        "must_match": "format: path \\| inode \\| ctime",
        "note": "README names this file as the in-tree pipe-v1 example; the example must keep existing with its declared format line.",
    },
    {
        "id": "custody-receipt-v2-tool-self-pin",
        "kind": "anchor",
        "file": ".ufo/waves/arc3-loop1-round2/claims/c3/EX-31/capture-pre.txt",
        "must_match": "tool: custody-pair\\.py  sha256 112d01dc",
        "note": "the arc3-r2 custody convention: every v2 receipt self-pins the instrument's sha256; the round's landed receipt must keep carrying the self-pin.",
    },
]

QUOTED_CANDIDATE = {
    "id": "log1412-landing-identity-quoted",
    "file": "LOG.md",
    "line": 1412,
    "must_match": "dd986f56",
    "note": "queue-drain rule #14 cites LOG.md:1411-1412 as the landing-identity record; the digest itself wraps onto :1412 (measured: :1411 ends at '10,225 B, sha256'). Append-only LOG words must stay verbatim (quoted class), never repaired.",
}

# charges that cannot become entries: adjudication candidates (NO-ENTRY + cause)
ADJUDICATIONS = [
    ("SCORECARD arc3-r1 section :1338-1400", "pin-free by design",
     "the section's own connector-injection record states it carries no bare version pin and no absolute path:line; measured zero path:line citations in the range -> NO-ENTRY (nothing to pin)."),
    ("SCORECARD:1415, :1494 `.ufo/waves/arc2-loop1-round10/C3.md`", "file-level mention of a pre-existing dirty path",
     "no line number, not a pointer to content; the path is named as a defect record -> NO-ENTRY."),
    (".ufo/waves/arc3-loop1-round2/claims/c3/EX-31/ (README:129 directory ref)", "directory reference",
     "a directory cannot carry a line pin; the load-bearing file inside it is covered by `custody-receipt-v2-tool-self-pin` -> NO-ENTRY."),
    ("identity records (8,316 B/`f95c5a05…`, 8,598 B/`d8d85949…`, 10,225 B/`dd986f56…`, SKILL.md 390 lines/`c134afcb…`)",
     "self-identity records bind a revision, not a live line",
     "rule #14 requires re-derivation after every revision; a static pin would manufacture a false-failure class -> NO-ENTRY (optional exact pins if the chain wants the words frozen instead)."),
    ("LOG.md internal arc3 citations (e.g. LOG.md:1449 custody receipt)", "append-only history",
     "the table's standing exempt clause: LOG line numbers describe past states by rule -> NO-ENTRY."),
]


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        h.update(fh.read())
    return h.hexdigest()


def git_show(path):
    r = subprocess.run(["git", "-C", REPO, "show", "HEAD:" + path],
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return r.stdout.split("\n")


def simulate(entry):
    """Manual resolution sim: returns a 'resolved' line or a FAIL reason."""
    citing = git_show(entry["file"])
    if citing is None:
        return "FAIL citing file absent at HEAD"
    kind = entry.get("kind", "quoted")
    if kind == "anchor":
        hits = [i + 1 for i, l in enumerate(citing)
                if re.search(entry["must_match"], l)]
        return "hit at %s" % (hits if hits else "NONE -> FAIL")
    ln = entry["line"]
    if not (1 <= ln <= len(citing)):
        return "FAIL line %d beyond EOF (%d)" % (ln, len(citing))
    line = citing[ln - 1]
    if kind == "quoted":
        ok = re.search(entry["must_match"], line)
        return "quoted-word %s at :%d" % ("OK" if ok else "MISSING -> FAIL", ln)
    if kind == "exact":
        ok = re.search(entry["must_match"], line)
        return "exact %s at :%d" % ("OK" if ok else "MISSING -> FAIL", ln)
    m = re.search(entry["pattern"], line)
    if not m:
        return "FAIL pattern absent at :%d" % ln
    lo = int(m.group(entry.get("target_group", 1)))
    hi = int(m.group(entry.get("target_group_end", entry.get("target_group", 1))) or lo)
    cited = git_show(entry["target"])
    if cited is None:
        return "FAIL target %s absent at HEAD" % entry["target"]
    if not (1 <= lo <= hi <= len(cited)):
        return "FAIL %s:%d-%d beyond EOF (%d)" % (entry["target"], lo, hi, len(cited))
    blob = "\n".join(cited[lo - 1:hi])
    ok = re.search(entry["must_match"], blob, re.M)
    return "states %s:%d-%d; needle %s; hit=%r" % (
        entry["target"], lo, hi, "OK" if ok else "MISSING -> FAIL",
        (re.search(entry["must_match"], blob, re.M).group(0) if ok else None))


def run_probe(table, expected, strict):
    args = [sys.executable, PROBE, "--root", REPO, "--rev", "HEAD",
            "--table", table, "--expected", expected]
    if strict:
        args.append("--strict")
    env = dict(os.environ, TMPDIR=SCRATCH)
    r = subprocess.run(args, capture_output=True, text=True, env=env)
    return r.returncode, r.stdout + r.stderr


def main():
    os.makedirs(SCRATCH, exist_ok=True)
    os.makedirs(OUTDIR, exist_ok=True)
    log = []

    def emit(s):
        print(s)
        log.append(s)

    head = subprocess.run(["git", "-C", REPO, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    emit("== EX-43 before-state census ==")
    emit("repo HEAD: %s" % head)
    emit("probe: %s" % os.path.relpath(PROBE, REPO))

    table_bytes = open(TABLE, "rb").read()
    table_sha = hashlib.sha256(table_bytes).hexdigest()
    table = json.loads(table_bytes)
    emit("pointer-table.json: %d bytes, sha256 %s" % (len(table_bytes), table_sha))
    emit("counts: entries=%d quoted=%d exempt=%d" %
         (len(table["entries"]), len(table["quoted"]), len(table["exempt"])))

    blob = json.dumps(table)
    arc3_hits = [e["id"] for e in table["entries"] + table["quoted"]
                 if "arc3" in json.dumps(e)]
    emit("table entries/quoted mentioning 'arc3': %d %s" % (len(arc3_hits), arc3_hits))

    # needle-target file set of the existing table (for overlap analysis)
    def target_files(entries):
        out = set()
        for e in entries:
            out.add(e.get("target") or e["file"])
        return out
    old_targets = target_files(table["entries"])
    new_targets = target_files(ENTRY_CANDIDATES)
    emit("existing table targets %d files; candidate targets %d files; overlap: %s"
         % (len(old_targets), len(new_targets), sorted(old_targets & new_targets)))

    emit("")
    emit("-- candidate resolution sim (git objects at HEAD) --")
    bad = 0
    for e in ENTRY_CANDIDATES:
        r = simulate(e)
        if "FAIL" in r:
            bad += 1
        emit("  %-42s %s" % (e["id"], r))
    r = simulate(QUOTED_CANDIDATE)
    if "FAIL" in r:
        bad += 1
    emit("  %-42s %s" % (QUOTED_CANDIDATE["id"], r))
    emit("sim FAIL count: %d" % bad)

    # ---------------------------------------------------------- scratch table
    ext = copy.deepcopy(table)
    ext["entries"].extend(ENTRY_CANDIDATES)
    ext["quoted"].append(QUOTED_CANDIDATE)
    ext_path = os.path.join(SCRATCH, "table-ext.json")
    with open(ext_path, "w") as fh:
        json.dump(ext, fh, indent=2)
        fh.write("\n")
    ext_sha = sha256_file(ext_path)
    expected = json.load(open(EXPECTED))
    exp_ext = copy.deepcopy(expected)
    exp_ext["pointer_table"]["sha256"] = ext_sha
    exp_path = os.path.join(SCRATCH, "expected-ext.json")
    with open(exp_path, "w") as fh:
        json.dump(exp_ext, fh, indent=2)
        fh.write("\n")
    emit("")
    emit("-- scratch extension --")
    emit("table-ext.json sha256 %s (%d entries, %d quoted)"
         % (ext_sha, len(ext["entries"]), len(ext["quoted"])))
    rc, out = run_probe(ext_path, exp_path, strict=True)
    emit("probe --strict on extension: rc=%d" % rc)
    emit(out.rstrip())
    emit("")

    # ------------------------------------------------------------------ teeth
    teeth = copy.deepcopy(ext)
    teeth["entries"][31 + 7]["must_match"] = "15/15"  # sc1435 candidate
    teeth_path = os.path.join(SCRATCH, "table-ext-teeth.json")
    with open(teeth_path, "w") as fh:
        json.dump(teeth, fh, indent=2)
        fh.write("\n")
    exp_teeth = copy.deepcopy(exp_ext)
    exp_teeth["pointer_table"]["sha256"] = sha256_file(teeth_path)
    teeth_exp = os.path.join(SCRATCH, "expected-ext-teeth.json")
    with open(teeth_exp, "w") as fh:
        json.dump(exp_teeth, fh, indent=2)
        fh.write("\n")
    rc2, out2 = run_probe(teeth_path, teeth_exp, strict=True)
    emit("-- teeth control (sc1435 needle 14/14 -> 15/15) --")
    emit("probe --strict rc=%d" % rc2)
    emit(out2.rstrip())
    emit("")

    # --------------------------------------------------------- adjudications
    emit("-- adjudication candidates (NO-ENTRY + cause) --")
    for token, cause, note in ADJUDICATIONS:
        emit("  * %s | %s | %s" % (token, cause, note))

    with open(os.path.join(OUTDIR, "census.out"), "w") as fh:
        fh.write("\n".join(log) + "\n")
    with open(os.path.join(OUTDIR, "candidate-entries.json"), "w") as fh:
        json.dump({"entry_candidates": ENTRY_CANDIDATES,
                   "quoted_candidate": QUOTED_CANDIDATE,
                   "scratch_validation": {
                       "table_ext_sha256": ext_sha,
                       "probe_strict_rc": rc,
                       "teeth_rc": rc2},
                   "adjudication_candidates": [
                       {"token": t, "cause": c, "note": n} for t, c, n in ADJUDICATIONS
                   ]}, fh, indent=2)
        fh.write("\n")
    return 0 if (bad == 0 and rc == 0 and rc2 == 1) else 1


if __name__ == "__main__":
    sys.exit(main())