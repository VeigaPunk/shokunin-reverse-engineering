#!/usr/bin/env python3
# W2C2Log: independent re-derivation of lesson atoms A3/A4/A5 (and A2 prose) from git objects
# at the round-48 base e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9. No import of tools/round-49.
import hashlib, json, os, re, subprocess, sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "e4f2cfa5ebff863a4d5d13c040cb0c41be6a40f9"
FLEET = "/home/vgpnk/Projects/shokunin"
FLEET_REPORT_COMMIT = "7b845bef80a797b7b90944c6ab2752dbbc9afaa9"
ENV = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1")

def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], env=ENV, capture_output=True, check=True).stdout

def show(repo, rev, path):
    return git(repo, "show", f"{rev}:{path}")

out = {"base": BASE}

# ---- A3: LOG.md line sets for the six commits
log = show(LANE, BASE, "LOG.md").decode("utf-8")
loglines = log.split("\n")
def named_lines(prefix):
    return [i + 1 for i, l in enumerate(loglines) if prefix.lower() in l.lower()]
a3 = {}
for h in ["2e785632", "33f65a91", "c093e798", "577a02a5", "8847042a", "7fe11332"]:
    full = git(LANE, "rev-parse", "--verify", "-q", h + "^{commit}").decode().strip()
    anc = subprocess.run(["git", "-C", LANE, "merge-base", "--is-ancestor", full, BASE], env=ENV).returncode == 0
    a3[h] = {"full": full, "ancestor_of_base": anc, "log_lines": named_lines(h)}
out["A3_log_lines"] = a3
out["A3_LOG_line_count"] = len(loglines) - 1
out["A3_LOG_line_3446_wave_sentence_has_73"] = "73 seats produced reports" in loglines[3445]

# ---- A4: seats and report artifacts
res = json.loads(show(LANE, BASE, ".ufo/waves/round-48/r48-w1-results.json"))
names = [r["name"] for r in res["results"]]
tree = git(LANE, "ls-tree", "-r", "--name-only", BASE, ".ufo/waves/round-48/w1/").decode().split("\n")
pre = ".ufo/waves/round-48/w1/"
rel = [p[len(pre):] for p in tree if p]
with_md, without = [], []
for n in names:
    c = [f for f in rel if f == n + ".md" or (f.startswith(n + "/") and f.endswith(".md"))]
    (with_md if c else without).append(n)
out["A4"] = {
    "seats_field": res["seats"], "results_len": len(names), "unique": len(set(names)) == len(names),
    "with_md_count": len(with_md), "without_md": without,
    "artifacts_of_without": {n: [f for f in rel if f == n or f.startswith(n + "/") or f.startswith(n + ".")] for n in without},
    "results_entries": {r["name"]: r["output"] for r in res["results"] if r["name"] in ("C1Meaning", "C1Battery", "ScribeReportNumbers")},
    "LOG_3446_names_no_report_seats": "no-report seats: C1Battery-2" in loglines[3445] and "ScribeReportNumbers" in loglines[3445],
}
# agent role mix from results
import collections
out["A4"]["role_mix"] = dict(collections.Counter(r["agent"] for r in res["results"]))

# ---- A5: digests of the two round-48 final receipts (raw, final-LF-stripped, all-LF-stripped)
def digests(path):
    b = show(LANE, BASE, path)
    final_lf = b[:-1] if b.endswith(b"\n") else b
    return {"bytes": len(b), "raw": hashlib.sha256(b).hexdigest(),
            "final_lf_stripped": hashlib.sha256(final_lf).hexdigest(),
            "all_lf_stripped": hashlib.sha256(b.replace(b"\n", b"")).hexdigest()}
out["A5"] = {
    "c1": digests(".ufo/waves/round-48/l1/scores/c1-final-33f65a91.json"),
    "c2": digests(".ufo/waves/round-48/l1/scores/c2-final-33f65a91.json"),
}

# ---- Fleet report (other repo, read-only): 73 claim, 7fe11332 citation, pointer lines
rep = git(FLEET, "show", f"{FLEET_REPORT_COMMIT}:.ufo/reports/round-48/kaidoku.md").decode("utf-8").split("\n")
out["fleet_report"] = {
    "73_claim": [i + 1 for i, l in enumerate(rep) if "73 seats produced reports" in l],
    "7fe11332_cite": [i + 1 for i, l in enumerate(rep) if "7fe11332" in l],
    "33f65a91_cites_LOG_3439": [i + 1 for i, l in enumerate(rep) if "33f65a91" in l and "LOG.md:3439" in l],
}

# ---- A2 (adjacent prose): shared prefix of the dead and actual hashes
dead, actual = "663f30ee7516942a0120e7de68fe88356e680822", "663f30ee751694fb0970e7de68fe88356e680822"
cp = 0
while cp < 40 and dead[cp] == actual[cp]:
    cp += 1
out["A2_prefix_len"] = cp
out["A2_positional_equal"] = sum(x == y for x, y in zip(dead, actual))

# ---- Closure wording (A3 attribution)
clo = show(LANE, BASE, "corpus/lessons/round-48-verifier-spotcheck.md").decode("utf-8").split("\n")
out["closure_pointer_lines"] = [l[:400] for l in clo if "LOG.md:3445" in l or "3442" in l]

print(json.dumps(out, indent=2, sort_keys=True))
