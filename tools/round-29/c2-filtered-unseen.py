#!/usr/bin/env python3
"""Round 29 R29-C2 counter: the source-read `filtered` rule on selectors the lane never fetched.

Copied from tools/round-28/c2-filtered-flag.py with round-29 paths, pins and target, and three rule
changes: (1) routed defect 6 of the round-28 spot-check: the entry's source: line must cite the
claim's own SOURCES row CLAIM["row"]; (2) both branches must hold unseen data: predicted_true >= 1
and predicted_false >= 1 (QUALITY row 44); (3) selftest git runs without inherited GIT_DIR,
GIT_WORK_TREE or GIT_INDEX_FILE.

Rule under test, read from Sourcify's 4byte service source (services/4byte/src/api/handlers.ts,
function filterResponse; master 189cd726f7ed8fb3d2f503402d5c133e0f50e1fd and staging
0966a3bcf13a46b335dae390a0c95b3b0d980c69 serve identical bytes): a candidate is filtered exactly
when its selector is a key of services/4byte/src/utils/canonical-signatures.json and its name
differs from that key's `signature` (a key with no `signature` marks every candidate filtered).
Every other candidate is unfiltered.

Reads committed bytes at --rev only. Pinned inputs (exit 2 if absent or different): the frozen
selector list and the canonical-signatures.json copy taken from that commit.

Counts, at --rev:
  responses_complete  selectors in corpus/evidence/round-29/c2/selectors.tsv with one saved
                      openchain filter=false response: manifest entry with the frozen URL,
                      status 200, utc strictly after this counter's commit, sha256 equal to the
                      bytes; file first committed no earlier than this counter; body parses with
                      ok=true and holds the selector key (a null or empty list is a valid answer).
  entries             candidate entries over the complete responses.
  mismatches          entries whose `filtered` is not the boolean the rule predicts (a non-boolean
                      flag is a mismatch).
  predicted_true      entries the rule marks filtered; predicted_false the others.
  entry_ok            the knowledge entry opens with source:/verified-at:/recheck:, names
                      corpus/evidence/round-29/c2/, states "mismatches M of N entries" with the
                      recomputed values, and its source: line cites the claim's own row
                      CLAIM["row"], new since --base, status mined, opened 2026-10-22, listed in
                      corpus/lessons/round-29.md ## Gate.

Exit 0 only when responses_complete = 178/178, entries >= 1, mismatches = 0, predicted_true >= 1,
predicted_false >= 1 and entry_ok = 1. Exit 1 otherwise; exit 2 on a pin failure.

Usage: c2-filtered-unseen.py --root LANE --rev REV [--base BASE] | --selftest
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

COUNTER_PATH = "tools/round-29/c2-filtered-unseen.py"
EVDIR = "corpus/evidence/round-29/c2"
ENTRY = "corpus/knowledge/2026-10-22-r29-openchain-filtered-unseen.md"
SOURCES = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-29.md"
OPENED = "2026-10-22"
BASE = "bacbe9cc31d09b5e58e265b0138bd75d0cdb6b47"
CLAIM = {"row": "S087"}
URL = "https://api.openchain.xyz/signature-database/v1/lookup?function=0x%s&filter=false"
PINS = {
    EVDIR + "/selectors.tsv": "3a93f7837accb9acd66874707922317d9a8e0f8afb0c9cd87ee79f3d9fa15b5d",
    EVDIR + "/canonical-signatures.json": "5572beb596c9062be042b11be4a8cbd6a875be67a518dc0046b220433878b3e2",
}
TARGET = {"responses": 178}


class PinError(Exception):
    pass


def show(root, rev, path):
    proc = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)], capture_output=True)
    return proc.stdout if proc.returncode == 0 else None


def first_commit_time(root, rev, path):
    out = subprocess.run(["git", "-C", root, "log", "--diff-filter=A", "--format=%ct", rev, "--", path],
                         capture_output=True, text=True).stdout.split()
    return int(out[-1]) if out else None


def parse_utc(text):
    try:
        return int(datetime.strptime(text, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp())
    except (TypeError, ValueError):
        return None


def pinned(root, rev, path):
    raw = show(root, rev, path)
    if raw is None:
        raise PinError("pinned input absent: %s" % path)
    if hashlib.sha256(raw).hexdigest() != PINS[path]:
        raise PinError("pinned input differs from its pin: %s" % path)
    return raw


def sources_rows(text):
    rows = {}
    for line in text.split("\n"):
        m = re.match(r"^\| (S\d{3}) \|", line)
        if m:
            rows[m.group(1)] = [c.strip() for c in line.strip().strip("|").split("|")]
    return rows


def gate_ids(text):
    ids, inside = set(), False
    for line in text.split("\n"):
        if line.startswith("## "):
            inside = line.strip() == "## Gate"
            continue
        if inside:
            ids |= set(re.findall(r"\bS\d{3}\b", line))
    return ids


def check_entry(root, rev, base, mismatches, entries):
    raw = show(root, rev, ENTRY)
    if raw is None:
        return ["entry absent"]
    text = raw.decode("utf-8")
    lines = text.split("\n")
    why = []
    if not (len(lines) >= 3 and lines[0].startswith("source:") and lines[1].startswith("verified-at:")
            and lines[2].startswith("recheck:")):
        why.append("entry does not open with source:/verified-at:/recheck:")
    if EVDIR + "/" not in text:
        why.append("entry does not name %s/" % EVDIR)
    phrase = "mismatches %d of %d entries" % (mismatches, entries)
    if phrase not in text:
        why.append("entry does not state '%s'" % phrase)
    src, les = show(root, rev, SOURCES), show(root, rev, LESSON)
    bsrc = show(root, base, SOURCES) if base else None
    if src is None or les is None:
        return why + ["SOURCES.md or round-29 lesson absent"]
    rows = sources_rows(src.decode("utf-8"))
    brows = sources_rows(bsrc.decode("utf-8")) if bsrc else {}
    gates = gate_ids(les.decode("utf-8"))
    s = CLAIM["row"]
    if not (s in set(re.findall(r"\bS\d{3}\b", lines[0])) and s in rows and s not in brows and len(rows[s]) >= 11
            and rows[s][7] == "mined" and rows[s][8] == OPENED and s in gates):
        why.append("source: line does not cite the claim's row %s new since base, mined, opened %s and in ## Gate"
                   % (s, OPENED))
    return why


def count(root, rev, base):
    sels = [l.split("\t")[0] for l in pinned(root, rev, EVDIR + "/selectors.tsv").decode().split("\n")[1:] if l]
    canon = json.loads(pinned(root, rev, EVDIR + "/canonical-signatures.json"))
    ctime = first_commit_time(root, rev, COUNTER_PATH)
    mraw = show(root, rev, EVDIR + "/db/manifest.json")
    reasons = []
    try:
        manifest = {m["file"]: m for m in json.loads(mraw)} if mraw is not None else {}
    except (ValueError, KeyError, TypeError):
        manifest = {}
        reasons.append("manifest.json does not parse")
    complete = entries = mism = ptrue = 0
    for s in sels:
        fname = "openchain-%s.json" % s
        path = EVDIR + "/db/" + fname
        raw, m, why = show(root, rev, path), manifest.get(fname), []
        if raw is None or m is None:
            reasons.append("%s missing (file or manifest entry)" % fname)
            continue
        if m.get("url") != URL % s:
            why.append("url differs")
        if m.get("status") != 200:
            why.append("status %r" % m.get("status"))
        t = parse_utc(m.get("utc"))
        if t is None or ctime is None or t <= ctime:
            why.append("fetched before the counter commit")
        if hashlib.sha256(raw).hexdigest() != m.get("sha256"):
            why.append("sha256 differs from bytes")
        added = first_commit_time(root, rev, path)
        if added is None or ctime is None or added < ctime:
            why.append("first committed before the counter")
        try:
            body = json.loads(raw)
            fn = body["result"]["function"]
            if body.get("ok") is not True or ("0x" + s) not in fn:
                why.append("body lacks ok=true or the selector key")
                items = None
            else:
                items = fn["0x" + s] or []
        except (ValueError, KeyError, TypeError):
            why.append("body does not parse")
            items = None
        if why:
            reasons.append("%s: %s" % (fname, "; ".join(why)))
            continue
        complete += 1
        c = canon.get("0x" + s)
        for it in items:
            entries += 1
            pred = c is not None and it.get("name") != c.get("signature")
            ptrue += pred
            if it.get("filtered") is not pred:
                mism += 1
                reasons.append("mismatch 0x%s %r: filtered=%r, rule predicts %r" % (s, it.get("name"), it.get("filtered"), pred))
    ereasons = check_entry(root, rev, base, mism, entries)
    return {"responses_complete": complete, "responses_total": len(sels), "entries": entries, "mismatches": mism,
            "predicted_true": ptrue, "predicted_false": entries - ptrue, "entry_ok": int(not ereasons)}, reasons + ereasons


def main_count(root, rev, base, out=sys.stdout):
    try:
        c, reasons = count(root, rev, base)
    except PinError as e:
        print("PIN %s" % e, file=out)
        return 2
    for r in reasons:
        print("FAIL %s" % r, file=out)
    print("responses_complete=%d/%d entries=%d mismatches=%d predicted_true=%d predicted_false=%d entry_ok=%d" % (
        c["responses_complete"], c["responses_total"], c["entries"], c["mismatches"], c["predicted_true"],
        c["predicted_false"], c["entry_ok"]), file=out)
    full = (c["responses_complete"] == c["responses_total"] == TARGET["responses"] and c["entries"] >= 1
            and c["mismatches"] == 0 and c["predicted_true"] >= 1 and c["predicted_false"] >= 1
            and c["entry_ok"] == 1)
    return 0 if full else 1


# ---------------------------------------------------------------- selftest

def _git(repo, *args, when=None):
    env = dict(os.environ, GIT_AUTHOR_NAME="t", GIT_AUTHOR_EMAIL="t@t", GIT_COMMITTER_NAME="t", GIT_COMMITTER_EMAIL="t@t")
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        env.pop(k, None)
    if when:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = when
    return subprocess.run(["git", "-C", repo, *args], check=True, capture_output=True, text=True, env=env).stdout.strip()


def _w(repo, rel, data):
    p = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "wb") as f:
        f.write(data if isinstance(data, bytes) else data.encode("utf-8"))


def _commit(repo, when, msg):
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "--allow-empty", "-m", msg, when=when)
    return _git(repo, "rev-parse", "HEAD")


def _fixture(repo, counter_src, mutate=None):
    _git(repo, "init", "-q")
    hdr = "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n|---|---|---|---|---|---|---|---|---|---|---|\n"
    old = "| S001 | old | code | A | s | a | t | mined | 2026-10-21 | on-release | x |\n"
    _w(repo, SOURCES, "# SOURCES\n\n" + hdr + old)
    base = _commit(repo, "2026-10-22T10:00:00Z", "base")
    sel_tsv = "selector\tset\na9059cbb\tr25\n11111111\tr28\n22222222\tr28\n"
    canon = json.dumps({"0xa9059cbb": {"signature": "transfer(address,uint256)", "source": "standard:erc20"}})
    _w(repo, COUNTER_PATH, counter_src)
    _w(repo, EVDIR + "/selectors.tsv", sel_tsv)
    _w(repo, EVDIR + "/canonical-signatures.json", canon)
    PINS[EVDIR + "/selectors.tsv"] = hashlib.sha256(sel_tsv.encode()).hexdigest()
    PINS[EVDIR + "/canonical-signatures.json"] = hashlib.sha256(canon.encode()).hexdigest()
    _commit(repo, "2026-10-22T11:00:00Z", "counter")
    st = {"bodies": {
        "a9059cbb": {"ok": True, "result": {"event": {}, "function": {"0xa9059cbb": [
            {"name": "transfer(address,uint256)", "filtered": False, "hasVerifiedContract": True},
            {"name": "workMyDirefulOwner(uint256,uint256)", "filtered": True, "hasVerifiedContract": False}]}}},
        "11111111": {"ok": True, "result": {"event": {}, "function": {"0x11111111": [
            {"name": "f0(uint256)", "filtered": False, "hasVerifiedContract": False}]}}},
        "22222222": {"ok": True, "result": {"event": {}, "function": {"0x22222222": None}}}},
        "man": [], "entry": None, "cite": "S002", "gate": True, "status": "mined"}
    if mutate:
        mutate(st)
    man = []
    for s, b in st["bodies"].items():
        raw = json.dumps(b).encode()
        _w(repo, EVDIR + "/db/openchain-%s.json" % s, raw)
        man.append({"file": "openchain-%s.json" % s, "url": URL % s, "status": 200, "utc": "2026-10-22T11:30:00Z",
                    "sha256": hashlib.sha256(raw).hexdigest()})
    for f in st["man"]:
        f(man)
    _w(repo, EVDIR + "/db/manifest.json", json.dumps(man))
    entry = st["entry"] or "source: %s\nverified-at: x\nrecheck: y\n\n%s/ mismatches 0 of 3 entries\n" % (st["cite"], EVDIR)
    _w(repo, ENTRY, entry)
    _w(repo, SOURCES, "# SOURCES\n\n" + hdr + old + "| S002 | new | code | A | s | a | t | %s | 2026-10-22 | on-release | x |\n" % st["status"]
       + "| S003 | other | code | A | s | a | t | mined | 2026-10-22 | on-release | x |\n")
    _w(repo, LESSON, "# r29\n\n## Gate\n\n%s\n| S003 | admit |\n\n## Mistakes\n\nS002\n" % ("| S002 | admit |" if st["gate"] else "none"))
    return base, _commit(repo, "2026-10-22T12:00:00Z", "data")


def selftest():
    counter_src = open(os.path.abspath(__file__), "rb").read()
    saved_pins, saved_target, saved_claim = dict(PINS), dict(TARGET), CLAIM["row"]
    CLAIM["row"] = "S002"

    def no_false(st):
        st["bodies"]["a9059cbb"]["result"]["function"]["0xa9059cbb"].pop(0)
        st["bodies"]["11111111"]["result"]["function"]["0x11111111"].pop(0)
        st["entry"] = "source: S002\nverified-at: x\nrecheck: y\n%s/ mismatches 0 of 1 entries\n" % EVDIR

    def flag(sel, i, value):
        def f(st):
            st["bodies"][sel]["result"]["function"]["0x" + sel][i]["filtered"] = value
        return f

    cases = [
        ("green-both-branches", None, 0),
        ("red-flag-flipped-canonical-alternative", flag("a9059cbb", 1, False), 1),
        ("red-flag-flipped-canonical-name", flag("a9059cbb", 0, True), 1),
        ("red-flag-on-non-canonical", flag("11111111", 0, True), 1),
        ("red-flag-not-boolean", flag("11111111", 0, 0), 1),
        ("red-missing-response", lambda st: st["bodies"].pop("22222222"), 1),
        ("red-selector-key-absent", lambda st: st["bodies"]["22222222"]["result"].__setitem__("function", {}), 1),
        ("red-early-fetch", lambda st: st["man"].append(lambda m: m[0].__setitem__("utc", "2026-10-22T10:30:00Z")), 1),
        ("red-sha", lambda st: st["man"].append(lambda m: m[1].__setitem__("sha256", "0" * 64)), 1),
        ("red-url", lambda st: st["man"].append(lambda m: m[1].__setitem__("url", "https://example.org/")), 1),
        ("red-status", lambda st: st["man"].append(lambda m: m[2].__setitem__("status", 500)), 1),
        ("red-no-canonical-branch", lambda st: st["bodies"]["a9059cbb"]["result"]["function"]["0xa9059cbb"].pop(1), 1),
        ("red-entry-wrong-count", lambda st: st.__setitem__("entry", "source: S002\nverified-at: x\nrecheck: y\n%s/ mismatches 0 of 9 entries\n" % EVDIR), 1),
        ("red-entry-old-row", lambda st: st.__setitem__("cite", "S001"), 1),
        ("red-row-not-in-gate", lambda st: st.__setitem__("gate", False), 1),
        ("red-row-status", lambda st: st.__setitem__("status", "candidate"), 1),
        ("red-cites-other-new-row", lambda st: st.__setitem__("cite", "S003"), 1),
        ("red-no-false-branch", no_false, 1),
    ]
    fails = 0
    for name, mut, want in cases:
        PINS.clear(); PINS.update(saved_pins); TARGET.clear(); TARGET.update({"responses": 3})
        tmp = tempfile.mkdtemp(prefix="r29c2-st-")
        try:
            base, rev = _fixture(tmp, counter_src, mut)
            got = main_count(tmp, rev, base, out=open(os.devnull, "w"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        fails += got != want
        print("%s %s exit=%d want=%d" % ("ok" if got == want else "FAIL", name, got, want))
    PINS.clear(); PINS.update(saved_pins); TARGET.clear(); TARGET.update(saved_target)
    tmp = tempfile.mkdtemp(prefix="r29c2-st-")
    try:
        base, rev = _fixture(tmp, counter_src)
        PINS.clear(); PINS.update(saved_pins)
        got = main_count(tmp, rev, base, out=open(os.devnull, "w"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    fails += got != 2
    print("%s red-pin-refusal exit=%d want=2" % ("ok" if got == 2 else "FAIL", got))
    PINS.clear(); PINS.update(saved_pins); TARGET.clear(); TARGET.update(saved_target); CLAIM["row"] = saved_claim
    print("selftest cases=%d failures=%d" % (len(cases) + 1, fails))
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--base", default=BASE)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not (a.root and a.rev):
        ap.error("--root and --rev are required")
    return main_count(os.path.abspath(a.root), a.rev, a.base)


if __name__ == "__main__":
    sys.exit(main())
