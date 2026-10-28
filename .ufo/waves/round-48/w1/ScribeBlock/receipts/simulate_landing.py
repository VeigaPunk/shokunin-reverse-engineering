#!/usr/bin/env python3
"""Simulate the round-48 C1 landing: insert block 25, repair the failing
verdict maps in their own rows, add the two missing registry rows, then score
genuine + the four forgeries. Repairs are row-scoped: the (old,new) pair is
applied only inside the registry row whose cell-0 path equals `path`."""
import json
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
sys.path.insert(0, LANE + "/tools/round-48")
sys.path.insert(0, LANE + "/tools/round-46")
import meanings  # noqa: E402

skill = open(LANE + "/SKILL.md").read()
block = open(LANE + "/.ufo/waves/round-48/w1/ScribeBlock/block.md").read()

# --- 1. insert the block as the last craft block (before next ## heading) ----
marker = "## Config custody for live-probe rounds (SOP)"
assert marker in skill, "craft-tail heading not found"
assert skill.count(meanings.MARKER) == 0, "marker already present"
sim = skill.replace(marker, block.rstrip("\n") + "\n\n" + marker, 1)

# --- 2. repair verdict maps, scoped to the named row's verdict cell ----------
# (path, segment-0 text, segment-1 text, segment-2 text): full honest map.
REPAIRS = {
 "tools/round-41/c1-extra.py":
   "0=met, all three bindings true, or a selftest in which every case passes; "
   "1=not met, a binding false, or at least one selftest case fails; "
   "2=unevaluable, from a non-commit --rev/--freeze/--base, carriers.json or "
   "the reader absent at --freeze, a missing --root/--rev/--freeze/--base, or "
   "a selftest whose tools dir lacks gen-squashfs.py and sqfs-list.py",
 "tools/round-41/c2-controls.py":
   "0=clean, no control reaches n/n so the kill rule does not fire; "
   "1=not met, a control reaches n/n so the kill rule fires, or an uncaught "
   "crash; 2=argparse usage error, nothing evaluated",
 "tools/round-41/fetch-vendor.py":
   "0=met, every external carrier materialised and every chain hash matched; "
   "1=not met, a chain link failed, so nothing was written for that carrier; "
   "2=usage refusal (no --cache, or neither --spec nor --root with --rev)",
 "tools/round-41/local-source-gate.py":
   "0=met, every out-of-lane row resolved; "
   "1=not met, at least one row unresolved (map-missing, no-copy-named, "
   "copy-digest-mismatch, row-pin-conflict, sidecar or kind finding); "
   "2=usage or parse error (root not a directory, unreadable --rev, malformed "
   "map, unknown map key, wrong table arity)",
 "tools/round-41/mk-l-carriers.py":
   "0=ok, both carriers built and, with --builds 2, each second build "
   "byte-identical to the first; "
   "1=no verdict: no explicit path returns it and only an uncaught exception "
   "does, e.g. a writer that exits 0 without writing the image raises "
   "FileNotFoundError at the sha256 read; "
   "2=usage or verification refusal before any build, argparse error, missing "
   "or non-empty outdir, or writer not found",
 "tools/round-42/c1-run.sh":
   "0=ok, the arm wrote its receipt and tables; "
   "1=no verdict: an unguarded command under set -e aborts with that command's "
   "status, which may be 1; "
   "2=usage or environment refusal (bad argv, missing python3 or jq, carrier "
   "not a regular file, OUTDIR outside the round-42 evidence root, SCRATCH "
   "without a /kaidoku-r42/ segment, plain sasquatch not resolvable)",
 "tools/round-42/c2-controls.py":
   "0=clean, no control reaches full score, the kill rule stays silent; "
   "1=not met, a control reaches full score so the kill rule fires, and by "
   "defect the same status also carries its own unevaluable SystemExit "
   "diagnostics (no DEV envelopes, failed feature extraction, failed "
   "evaluator); 2=argparse usage error or an unhandled IO failure",
 "tools/round-42/heldout-gen-v4.py":
   "0=met, the selected set was generated, or under --run --verify every "
   "envelope matched its declared tuple and the byte-identical regeneration "
   "passed; "
   "1=not met, an aggregate check failed (a REA run errored, or an envelope "
   "or regeneration mismatched) and also every refusal the script raises "
   "itself as SystemExit text, which Python exits as 1; "
   "2=unevaluable, argparse rejected the argv, so nothing was evaluated",
 "tools/round-42/indep-eval-v4.py":
   "0=wrote one record for the single envelope, or the batch payload emitted "
   "for a directory; "
   "1=not met, at least one selftest case failed; "
   "2=usage or I/O error (no envelope and no --envelopes, unreadable or "
   "non-object JSON, or a --envelopes path that is not a directory)",
 "tools/round-42/sqfs3-oracle.py":
   "0=ok, producers agree and oracle.tsv plus nonregular.tsv are written; "
   "1=not met, the inline selftest failed (never a verdict on an image); "
   "2=unevaluable: image unreadable, wrong magic or unsupported major, or a "
   "required producer missing or incomplete",
 "tools/round-42/unblob-logtee.sh":
   "0=ok, the wrapped unblob returned 0, log copied when C1_LOG_COPY names an "
   "existing destination; "
   "1=not met, the wrapped unblob's own non-zero code propagated unchanged "
   "and no verdict of its own is made; "
   "2=refusal before any run, C1_REAL_UNBLOB is not an absolute path",
 "tools/round-43/c1-counter.py":
   "0=met, met_target true, every held-out pair matched and every binding "
   "true; "
   "1=not met: at least one pair miss or one binding false, the receipt still "
   "written; "
   "2=could-not-evaluate: frozen_path_changed, freeze not an ancestor of rev, "
   "unknown revision, absent or unparsable manifest, or a frozen tool "
   "failing to run",
 "tools/round-43/c2-score-r43.py":
   "0=met, all 13 checks true; "
   "1=not met, at least one check false, including a gate or audit "
   "sub-receipt that could not be produced at all; "
   "2=could-not-evaluate: the clone cannot be made, or a usage/argument error",
 "tools/round-44/c1-run.sh":
   "0=clean, every carrier ran and produced a receipt; "
   "1=not met, at least one carrier failed, by REA exit, no receipt, or a pin "
   "mismatch; "
   "2=could not evaluate, usage, environment, missing sibling tool, or an "
   "occupied evidence dir",
 "tools/round-46/census.py":
   "0=ok, census computed and printed, and written when --out is given; "
   "1=no verdict: an unhandled exception such as an unwritable --out, a "
   "traceback and not a verdict; "
   "2=usage error from argparse (missing --root or an unknown flag)",
 "tools/round-46/gate.py":
   "0=clean, both arms agree that no frozen path changed in FREEZE..REV and "
   "the freeze is an ancestor of rev; "
   "1=no verdict: running gate.py as a program refuses with \"gate.py is a "
   "library\" and evaluates nothing, and no library entry point returns 1; "
   "2=could-not-evaluate, unknown or non-ancestor revision, absent claims "
   "file or Frozen paths section, failed git call, refused --json-out "
   "target, missing non-temporary scratch root, or any unhandled exception "
   "caught by main_guard",
}

ROW = re.compile(r"(?m)^\|\s*`")
out_lines = []
changed = set()
for line in sim.splitlines():
    if ROW.match(line):
        cells = meanings._cells(line)
        if len(cells) == 7:
            path = cells[0].strip("` ")
            if path in REPAIRS:
                cells[2] = REPAIRS[path]
                line = "| " + " | ".join(cells) + " |"
                changed.add(path)
    out_lines.append(line)
missing_rep = set(REPAIRS) - changed
assert not missing_rep, f"repairs not applied: {missing_rep}"
sim = "\n".join(out_lines) + "\n"

# --- 3. append the two missing registry rows ---------------------------------
NEW = (
 "| `tools/round-48/meanings.py` | gate — R48-C1 depth: the verdict-meaning "
 "block in `## Queue-drain craft`, its pins and citations, and the registry "
 "verdict maps bound to meaning classes over the census | 0=met, every clause "
 "true at --rev; 1=not met, each false clause named in failing; "
 "2=could-not-evaluate, frozen_path_changed, a malformed craft or registry "
 "section, or a usage error | python3 -I -B tools/round-48/meanings.py "
 "--selftest (17 cases) | plans/round-48-claims.md and tools/round-48/ freeze, "
 "plus tools/round-48/census2.json | --json-out only; selftest fixtures under "
 "a scratch root | kaidoku |\n"
 "| `tools/round-48/record2.py` | gate — R48-C2 calibration: SCORECARD.md "
 "re-derived from committed bytes, a completeness floor, quoted-receipt "
 "binding, axes-correction parsing and the Owned-axes score cell | 0=met, "
 "every clause true at --rev; 1=not met, each false clause named in failing; "
 "2=could-not-evaluate, frozen_path_changed, an absent oracle or card, or a "
 "usage error | python3 -I -B tools/round-48/record2.py --selftest | "
 "plans/round-48-claims.md and tools/round-48/ freeze | --json-out only; "
 "selftest fixtures under a scratch root | kaidoku |\n")
close = "<!-- /instrument-registry -->"
assert sim.count(close) == 1
sim = sim.replace(close, NEW + close, 1)

# --- 4. score genuine + battery ----------------------------------------------
def files(p):
    try:
        return open(LANE + "/" + p).read()
    except OSError:
        return None

code, rec = meanings.score(sim, files, "v3", "SIM", battery=None)
print("GENUINE exit", code, "failing:", rec["failing"])
print("registry_rows", rec.get("registry_rows"), "census", rec.get("census_paths"),
      "rederived", rec.get("census_rederived_equal"),
      "meaning_failed", rec.get("meaning_rows_failed"))
out = {"forgeries_total": 0, "v2_green": 0, "v3_green": 0,
       "genuine_green": 1 if code == 0 else 0, "crash": 1 if code == 2 else 0}
for name, fn in meanings.MUTATIONS:
    text, _ = fn(sim, None)
    fx = lambda p: (text if p == "SKILL.md" else files(p))
    c2, _ = meanings.score(text, fx, "v2", "SIM", battery=None)
    c3, r3 = meanings.score(text, fx, "v3", "SIM", battery=None)
    out["forgeries_total"] += 1
    out["v2_green"] += c2 == 0
    out["v3_green"] += c3 == 0
    out["crash"] += c3 == 2
    print(f"  {name}: v2={c2} v3={c3} v3fail={r3.get('failing')}")
print("BATTERY", json.dumps(out))
want = {"forgeries_total": 4, "v2_green": 4, "v3_green": 0,
        "genuine_green": 1, "crash": 0}
print("BATTERY_MATCH", all(out[k] == want[k] for k in want))
with open("/fast/scratch/hyaku/kaidoku-r48/ScribeBlock/skill-landed.md", "w") as fh:
    fh.write(sim)
print("wrote simulated SKILL.md")
