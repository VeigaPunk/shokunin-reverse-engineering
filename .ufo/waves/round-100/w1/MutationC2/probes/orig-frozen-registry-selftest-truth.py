#!/usr/bin/env python3
"""registry-selftest-truth.py - round-100 frozen counter for R100-C2 (calibration).

Self-assessment surface: the self-test column (fourth cell) of the SKILL.md
instrument registry (`<!-- instrument-registry v2 -->` ... `<!-- /instrument-registry -->`).
Each row in the frozen population states how many cases its tool's self-test
runs ("N cases", "cases=N", "N/N cases").  The round-99 counter checked that
rows exist and carry a pinned sha256 (presence and shape); the round-99
closure and lesson (named limit 1, L1/L6) left the prose unchecked.  This
counter checks the stated count against the tool itself: it runs the
self-test the row documents, at the measured revision, and parses the count
the tool prints.

Population (frozen, POPULATION below): every registry row at the base
revision whose self-test cell states a case count and whose documented
self-test runs on this host with exit 0 and prints a parseable count.  Each
entry pins the tool's sha256 at the base revision and the argv of the
documented self-test (placeholders: {work} a per-row scratch dir, {pkg65} the
rea-agents 6.5.0 package root, {rev} the measured revision).  Rows excluded
at the freeze are listed in EXCLUDED with the reason; they are reported,
never scored.

Per row atoms:
  row       the registry has exactly one row whose first cell is the path;
  pin       sha256 of the tool at --rev equals the frozen pin (a tool edited
            to print the claimed number is not a correction of the claim);
  claimed   the self-test cell states a count (first match of CLAIM_RE);
  green     the documented self-test exits 0 (timeout 900 s);
  counted   the output carries a count (whole stdout as JSON with an integer
            `cases`, else a list `cases` -> its length, else the LAST match of
            OBS_RE over stdout then stderr);
  agree     claimed == counted.
A row is a mismatch unless all six atoms hold.

Label: `rows R; claimed C of R; green G of R; counted K of R; agree A of R;
mismatches M`.  Frozen predicate (R100-C2): the label equals TARGET and the
exit is 0.  Exit 1 otherwise; exit 2 could-not-evaluate (unknown revision,
clone failure, missing or doubled registry markers, no --work, bad argv).

The self-tests run in a `git clone --shared` of --root checked out at --rev
under --work (never in the lane checkout); HYAKU_SCRATCH and TMPDIR point
into --work.  The receipt is written through mkstemp in its own directory.
--selftest exercises the two parsers and the row extractor in memory.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

TOOL = "tools/round-100/registry-selftest-truth.py"
START = "<!-- instrument-registry v2 -->"
END = "<!-- /instrument-registry -->"
PKG65 = "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents"
CLAIM_RE = re.compile(r"(?<![\w./-])(\d+)(?:/\d+)?\s+(?:selftest\s+)?cases\b|(?<![\w-])cases[=: ]+(\d+)")
OBS_RE = re.compile(r"(?<![\w-])cases[\"'=: ]+(\d+)|(?<![\w./-])(\d+)/\d+ cases\b|(?<![\w./-])(\d+) cases\b")
S = "--selftest"

# path -> ({file: sha256 at base} for the row's tool and the script its
# documented self-test executes, argv after "python3 -I -B")
POPULATION = {}
EXCLUDED = {}    # path -> reason (none at the freeze: every claim-bearing row ran green and counted)


def _pop(path, pins, argv=None):
    POPULATION[path] = (dict(pins), list(argv) if argv else [path, S])


def sha_bytes(b):
    return hashlib.sha256(b).hexdigest()


def registry_rows(text):
    """Return ({path: [row cells]}, duplicates) or raise ValueError on markers."""
    if text.count(START) != 1 or text.count(END) != 1:
        raise ValueError("registry markers missing or doubled")
    body = text.split(START, 1)[1].split(END, 1)[0]
    rows, dup = {}, set()
    for line in body.splitlines():
        if not line.startswith("| `"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        path = cells[0].strip("`")
        if path in rows:
            dup.add(path)
        rows[path] = cells
    return rows, dup


def claim_cell(cells):
    """The self-test cell (fourth) of a full row; for a short row (fewer than
    four cells, e.g. the round-88/89 two-cell rows) the text after the path."""
    return cells[3] if len(cells) >= 4 else " | ".join(cells[1:])


def parse_claim(cell):
    m = CLAIM_RE.search(cell)
    if not m:
        return None
    return int(m.group(1) or m.group(2))


def parse_observed(stdout, stderr):
    try:
        j = json.loads(stdout)
    except ValueError:
        j = None
    if isinstance(j, dict):
        c = j.get("cases")
        if isinstance(c, bool):
            c = None
        if isinstance(c, int):
            return c
        if isinstance(c, list):
            return len(c)
    for text in (stdout, stderr):
        ms = list(OBS_RE.finditer(text))
        if ms:
            g = ms[-1].groups()
            return int(next(x for x in g if x is not None))
    return None


def run_row(clone, work, rev, path, pins, argv, rows, dup):
    rec = {"path": path, "pins": pins}
    cells = rows.get(path)
    rec["row"] = cells is not None and path not in dup
    got = {}
    for f in sorted(pins):
        try:
            with open(os.path.join(clone, f), "rb") as fh:
                got[f] = sha_bytes(fh.read())
        except OSError:
            got[f] = None
    rec["sha256_at_rev"] = got
    rec["pin_ok"] = got == pins
    rec["claimed"] = parse_claim(claim_cell(cells)) if rec["row"] else None
    seat = os.path.join(work, "rows", path.replace("/", "_"))
    os.makedirs(seat, exist_ok=True)
    full = [sys.executable, "-I", "-B"] + [a.format(work=seat, pkg65=PKG65, rev=rev) for a in argv]
    rec["argv"] = full[3:]
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "HOME": os.environ.get("HOME", "/"),
           "HYAKU_SCRATCH": seat, "TMPDIR": seat, "LANG": "C.UTF-8"}
    try:
        pr = subprocess.run(full, cwd=clone, capture_output=True, text=True, timeout=900, env=env)
        rc, out, err = pr.returncode, pr.stdout, pr.stderr
    except subprocess.TimeoutExpired:
        rc, out, err = -9, "", "timeout"
    rec["rc"] = rc
    rec["green"] = rc == 0
    rec["counted"] = parse_observed(out, err)
    rec["tail"] = (out + err)[-300:]
    rec["agree"] = rec["claimed"] is not None and rec["claimed"] == rec["counted"]
    rec["ok"] = all((rec["row"], rec["pin_ok"], rec["claimed"] is not None, rec["green"],
                     rec["counted"] is not None, rec["agree"]))
    return rec


def label_of(recs):
    r = len(recs)
    c = sum(x["claimed"] is not None for x in recs)
    g = sum(x["green"] for x in recs)
    k = sum(x["counted"] is not None for x in recs)
    a = sum(x["agree"] for x in recs)
    m = sum(not x["ok"] for x in recs)
    return "rows %d; claimed %d of %d; green %d of %d; counted %d of %d; agree %d of %d; mismatches %d" % (
        r, c, r, g, r, k, r, a, r, m)


def write_receipt(path, obj):
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".receipt-")
    try:
        with os.fdopen(fd, "w") as fh:
            json.dump(obj, fh, indent=1, sort_keys=True)
            fh.write("\n")
            fh.flush()
            os.fsync(fh.fileno())
        os.replace(tmp, path)
        tmp = None
    finally:
        if tmp is not None and os.path.exists(tmp):
            os.unlink(tmp)


def selftest():
    reg = "x\n%s\n| tool | a | b | self-test |\n|---|---|---|---|\n" % START
    reg += "| `tools/a.py` | g | 0=ok | `python3 a.py --selftest` - 12 cases, exit 0 |\n"
    reg += "| `tools/b.py` | g | 0=ok | none |\n"
    reg += "| `tools/a.py` | g | 0=ok | cases=3 |\n%s\n" % END
    rows, dup = registry_rows(reg)
    cases = [
        ("claim-n-cases", parse_claim("--selftest - 12 cases, exit 0"), 12),
        ("claim-slash", parse_claim("45/45 cases, 0 failures"), 45),
        ("claim-eq", parse_claim("green cases=12 failures=0"), 12),
        ("claim-selftest-word", parse_claim("`--selftest` 3 selftest cases"), 3),
        ("claim-absent", parse_claim("green, exit 0"), None),
        ("claim-first-wins", parse_claim("15 cases at A, 16 from B"), 15),
        ("claim-date-not-count", parse_claim("green 2026-10-28 cases=12 failures=0"), 12),
        ("claim-flag-not-count", parse_claim("--min-pristine-cases 38 --json-out x"), None),
        ("claim-short-row", parse_claim(claim_cell(["`t.py`", "tool; `--selftest` (11 cases)"])), 11),
        ("obs-date-not-count", parse_observed("run 2026-10-28 cases=4", ""), 4),
        ("obs-json-int", parse_observed('{"cases": 7, "ok": true}', ""), 7),
        ("obs-json-list", parse_observed('{"cases": [1, 2, 3]}', ""), 3),
        ("obs-json-bool-ignored", parse_observed('{"cases": true}', "x"), None),
        ("obs-last-line", parse_observed("cases=2\nSELFTEST cases=9 failures=0\n", ""), 9),
        ("obs-quoted-key", parse_observed('noise\n{"cases": 11, "failed": []}\n', ""), 11),
        ("obs-slash", parse_observed("45/45 cases; 0 failure(s)", ""), 45),
        ("obs-stderr", parse_observed("", "selftest: 23/23 cases"), 23),
        ("obs-none", parse_observed("ok true", ""), None),
        ("obs-not-showcase", parse_observed("showcases=4", ""), None),
        ("rows-dup", sorted(dup), ["tools/a.py"]),
        ("rows-count", sorted(rows), ["tools/a.py", "tools/b.py"]),
    ]
    try:
        registry_rows("no markers")
        bad = "accepted"
    except ValueError:
        bad = "refused"
    cases.append(("markers-missing", bad, "refused"))
    fails = [n for n, got, want in cases if got != want]
    for n, got, want in cases:
        print("%s %s got=%r want=%r" % ("PASS" if got == want else "FAIL", n, got, want))
    print("SELFTEST cases=%d failures=%d" % (len(cases), len(fails)))
    return 0 if not fails else 1


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--json-out")
    ap.add_argument("--jobs", type=int, default=8)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()
    if not (a.root and a.rev and a.work and a.json_out):
        print("usage: --root --rev --work --json-out are required", file=sys.stderr)
        return 2
    q = subprocess.run(["git", "-C", a.root, "rev-parse", "--verify", a.rev + "^{commit}"],
                       capture_output=True, text=True)
    if q.returncode != 0:
        print("could-not-evaluate: unknown revision %s" % a.rev, file=sys.stderr)
        return 2
    rev = q.stdout.strip()
    work = os.path.abspath(a.work)
    shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work)
    clone = os.path.join(work, "clone")
    c = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", os.path.abspath(a.root), clone],
                       capture_output=True, text=True)
    top = subprocess.run(["git", "-C", clone, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True).stdout.strip()
    if c.returncode != 0 or os.path.realpath(top) != os.path.realpath(clone):
        print("could-not-evaluate: clone failed %s" % c.stderr[-200:], file=sys.stderr)
        return 2
    co = subprocess.run(["git", "-C", clone, "checkout", "-q", "--detach", rev], capture_output=True, text=True)
    if co.returncode != 0:
        print("could-not-evaluate: checkout failed %s" % co.stderr[-200:], file=sys.stderr)
        return 2
    try:
        with open(os.path.join(clone, "SKILL.md"), encoding="utf-8") as fh:
            rows, dup = registry_rows(fh.read())
    except (OSError, ValueError) as e:
        print("could-not-evaluate: %s" % e, file=sys.stderr)
        return 2
    with concurrent.futures.ThreadPoolExecutor(max(1, a.jobs)) as ex:
        futs = [ex.submit(run_row, clone, work, rev, p, pin, av, rows, dup)
                for p, (pin, av) in sorted(POPULATION.items())]
        recs = [f.result() for f in futs]
    label = label_of(recs)
    met = label == TARGET
    with open(os.path.abspath(__file__), "rb") as fh:
        me = sha_bytes(fh.read())
    receipt = {"tool": TOOL, "rev": rev, "counter_sha256": me, "label": label, "target": TARGET,
               "met": met, "exit": 0 if met else 1, "excluded": EXCLUDED,
               "mismatches": [r["path"] for r in recs if not r["ok"]], "rows": recs}
    write_receipt(a.json_out, receipt)
    print(label)
    print("met %s" % met)
    return 0 if met else 1


# ---- frozen population: 93 claim-bearing registry rows at base 6371c88633f6ce6692eaeff17e256b80ad21ece0 ----
_pop("tools/round-41/c1-counter.py", {"tools/round-41/c1-counter.py": "bbabbfecb229e8992fb07149cad0cf9171a2bf31513bd5db77ddb3c4f8845cfc"},
     ["tools/round-41/c1-counter.py", "--selftest", "--pkg65", "{pkg65}"])
_pop("tools/round-41/c1-extra.py", {"tools/round-41/c1-extra.py": "531724e1c7215ed602a06648525cc375b4c9d86370f8e37ea59657a087ceacae"},
     ["tools/round-41/c1-extra.py", "--selftest", "--tools", "tools/round-41", "--work", "{work}"])
_pop("tools/round-41/c2-counter.py", {"tools/round-41/c2-counter.py": "c6c1ea64f07884a3b160a7e52268d295d54c8ef3bc2005704d5fae3398720af8"})
_pop("tools/round-41/fetch-vendor.py", {"tools/round-41/fetch-vendor.py": "1cb0a34688488160bc693369dadf21152050cdd6e1654f7d1f6c168bc8ea0e04"})
_pop("tools/round-41/indep-eval-v3.py", {"tools/round-41/indep-eval-v3.py": "26178d71c0f7634c3f1371ad5c4c7de3b59c49636cdf1b61bf8b2e461c75dce1"})
_pop("tools/round-41/local-source-gate.py", {"tools/round-41/local-source-gate.py": "cafe232a196dd8446bd9b0420b32bf696cba427770eb79edda2be15a45a4ece7"})
_pop("tools/round-41/sqfs-triage-v3.py", {"tools/round-41/sqfs-triage-v3.py": "6ad2b4e1638a2b5f883d7bed14f8863ad5396dbc1af64b7cd521720ea42b6aa4"})
_pop("tools/round-42/c1-counter.py", {"tools/round-42/c1-counter.py": "0f5052f99a976cfdd391d3e8330b644ca403b146095ca73e14f3859ab9d1483c"},
     ["tools/round-42/c1-counter.py", "--selftest", "--pkg65", "{pkg65}"])
_pop("tools/round-42/fetch-carrier.py", {"tools/round-42/fetch-carrier.py": "54b03b6df6b72b67af3aef93f013dd3df2d53a08650039a970908bf8b8b64498"})
_pop("tools/round-42/indep-eval-v4.py", {"tools/round-42/indep-eval-v4.py": "7a135dd36b3cab29d4dfa5b5d6dcf2199c026989549683933f4e6c1fa64dd301"})
_pop("tools/round-42/prefile-gate.py", {"tools/round-42/prefile-gate.py": "c3f8abf984fa4f2c247b3b3629721429fc212cb51fe80eeb7aaea0946a2688b6"},
     ["tools/round-42/prefile-gate.py", "--selftest", "--work", "{work}"])
_pop("tools/round-42/sqfs-triage-v4.py", {"tools/round-42/sqfs-triage-v4.py": "497bab6766a0b0c6d6f36cb58cadc531bddf9dd3231f6100bf46cf6ff552a2e9"})
_pop("tools/round-44/c1-counter.py", {"tools/round-44/c1-counter.py": "9f2cc140e1fa7875bcd9dc80ce2ff5a1006e8ee73c7e1207580f88a97ffea993"},
     ["tools/round-44/c1-counter.py", "--selftest", "--pkg65", "{pkg65}"])
_pop("tools/round-45/c1-counter.py", {"tools/round-45/c1-counter.py": "2cfc5a4853585879b0924f4c002ed4581dced02f061068d325c2cd3da130a509"})
_pop("tools/round-45/c2-counter.py", {"tools/round-45/c2-counter.py": "50212d0f456107edb6e36c48b51988ac24ec58b84b16197abe13572d2111b025"})
_pop("tools/round-45/frozen-path-preflight.py", {"tools/round-45/frozen-path-preflight.py": "633ebc058f0ea5a7c6dec4a9d6287e062eecf497fb6da674a3898c7c7130523b"})
_pop("tools/round-46/attest.py", {"tools/round-46/attest.py": "c405613170f0581661b9e2afb4bf278da8ac1f936eeb00eb4b456a9e70ad8e5c"},
     ["tools/round-46/attest.py", "--selftest", "--root", ".", "--freeze", "HEAD", "--rev", "HEAD"])
_pop("tools/round-46/gate.py", {"tools/round-46/gate.py": "c3ba6b93ef414e3795d2142d1d9a643a465a312593cdb9f3d8027553fd38897c", "tools/round-46/registry.py": "5e16e4af69ebf714f0ee48b5a714aa682592f0ce5e32cdeec699b963d3f2da73"},
     ["tools/round-46/registry.py", "--root", ".", "--freeze", "HEAD", "--rev", "HEAD", "--selftest"])
_pop("tools/round-47/exact.py", {"tools/round-47/exact.py": "01a4bca7a60bb598b57a0c99f41b912ff1967badaa002d289ea1fe450bc5bcd5"},
     ["tools/round-47/exact.py", "--selftest", "--root", ".", "--freeze", "HEAD", "--rev", "HEAD"])
_pop("tools/round-47/record.py", {"tools/round-47/record.py": "abf352573d156ed1388683c882e40cab9897f426b9448356993bf41bf37779e7"},
     ["tools/round-47/record.py", "--selftest", "--root", ".", "--rev", "HEAD"])
_pop("tools/round-48/meanings.py", {"tools/round-48/meanings.py": "f5e5c35c59c33d2b5abe884b83c9739c20f180f7c6863133a4d880711122cf97"})
_pop("tools/round-49/c1-counter.py", {"tools/round-49/c1-counter.py": "ac83715b199100774873389ea33fb4819231e1f963225416e86ad422f69d287f"},
     ["tools/round-49/c1-counter.py", "--selftest", "--pkg65", "{pkg65}"])
_pop("tools/round-49/c2-mismatch.py", {"tools/round-49/c2-mismatch.py": "9b80b3b0e3945563426510e72969a7b5fed3e66a47b567d3a8341fc1f5d8595d", "tools/round-50/selftest-r49-c2.py": "7d0523ab6b80c0b570f36e682eb0f446ffdd455d48e84d50399876b79a3e7fbc"},
     ["tools/round-50/selftest-r49-c2.py", "--lane", "."])
_pop("tools/round-50/c1-controls.py", {"tools/round-50/c1-controls.py": "bca264c1b385559290d649b7f7fbee4f7bbc343b4b280aa14ba0f6da557f5bfb"},
     ["tools/round-50/c1-controls.py", "selftest", "--work", "{work}"])
_pop("tools/round-50/c1-counter.py", {"tools/round-50/c1-counter.py": "9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813"},
     ["tools/round-50/c1-counter.py", "--selftest", "--pkg65", "{pkg65}"])
_pop("tools/round-50/c2-record.py", {"tools/round-50/c2-record.py": "4749bcd86c8f61bfb6994baeab3bd990b61ea0c369b87197351d0a4618e71285"},
     ["tools/round-50/c2-record.py", "--selftest", "--root", "."])
_pop("tools/round-50/fetch-vendor.py", {"tools/round-50/fetch-vendor.py": "c53221ea9e4ba586552a65cfa3be056a0ab8c792920a8361aca1e13addc3d8a8"})
_pop("tools/round-53/sqfs-triage-v6.py", {"tools/round-53/sqfs-triage-v6.py": "5902a00815d2a5db402f2b32bb5c3a555f2462c67e86e9ded96be3ca00bdaefa"})
_pop("tools/round-55/v6-block-digest.py", {"tools/round-55/v6-block-digest.py": "22785c1e47b61cc807f99f1ef3fecc5aa5203e90b8e4ba5bee7eedcc2a8f741c"})
_pop("tools/round-64/jsc-route-matrix.py", {"tools/round-64/jsc-route-matrix.py": "29efef4fb5492e7a4aa9cfb88ac2a7bf8b30c5462aafaf692c407ededba20deb"})
_pop("tools/round-65/coverage-recipe.py", {"tools/round-65/coverage-recipe.py": "9434888e1bfa283f2980fb3c550b9e15409c88855ee94c944e8472fcf83995a6"})
_pop("tools/round-65/jsc-closure-matrix.py", {"tools/round-65/jsc-closure-matrix.py": "79a4dca40d2b37dc8d88711e9a95ec25e7d2e099bfd3ed52bb38bab77ff922c6"})
_pop("tools/round-66/closure-boundary.py", {"tools/round-66/closure-boundary.py": "3c5cfb038d86cdde03fb659e1d42a44ffa5f42ccd019ab7ea9b52710d071045b"})
_pop("tools/round-66/coverage-selfcheck.py", {"tools/round-66/coverage-selfcheck.py": "1be9d046cea38a96a4b62d038f7dbc76e8ea611000af4aee3b91a6def86555aa"})
_pop("tools/round-67/avm-le-counter.py", {"tools/round-50/c1-counter.py": "9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813", "tools/round-67/avm-le-counter.py": "b5a660d2661713675f9f70cda296f4f3b72b73d7dd8b5dc22c2b1258b46f1323"},
     ["tools/round-50/c1-counter.py", "--selftest", "--pkg65", "{pkg65}"])
_pop("tools/round-67/mutation-battery.py", {"tools/round-67/mutation-battery.py": "ecf5598775edc33d359de152154f0dff00702b78d0bbd58d9fa5f4def8f5d766"})
_pop("tools/round-68/packed-elf.py", {"tools/round-68/packed-elf.py": "48ef4c688a14faf381abbd2cc2b29061035f38c97815e2365957843433e5276e"})
_pop("tools/round-68/registry-conformance.py", {"tools/round-68/registry-conformance.py": "a300d831c7ef1de47448c2feb8dcbd9ceaf597f7e5f4b996a8e4cc510c6e8315"})
_pop("tools/round-69/packed-elf.py", {"tools/round-69/packed-elf.py": "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc"})
_pop("tools/round-70/forged-receipts.py", {"tools/round-70/forged-receipts.py": "8aaac447a8cdd04a48a7b0bcaff03c0133aa24a18c1d3af79c464cfbdfd9d8c2"},
     ["tools/round-70/forged-receipts.py", "--selftest", "--root", ".", "--base-rev", "{rev}", "--base-tool", "tools/round-69/packed-elf.py", "--work", "{work}"])
_pop("tools/round-70/packed-elf.py", {"tools/round-70/packed-elf.py": "417b116803fbf78b44220d4a2caeb30d1261030353bc1b1c81d22c3b0146048a"})
_pop("tools/round-71/forged-receipts.py", {"tools/round-71/forged-receipts.py": "bd70af49ed4629ab965b83a814ec0a39ce5db4a86c2a76e42121bb9eabb2084a"},
     ["tools/round-71/forged-receipts.py", "--selftest", "--root", ".", "--base-rev", "{rev}", "--base-tool", "tools/round-69/packed-elf.py", "--work", "{work}"])
_pop("tools/round-71/packed-elf.py", {"tools/round-71/packed-elf.py": "d8bd30b8b95cb57524e1045e9786d4b14837fb27b0a9f6842b0bff81545d7d7a"})
_pop("tools/round-71/registry-census.py", {"tools/round-71/registry-census.py": "b85b4d7922ab571af04f633e415a4fe91859e440c9a609d4182a46aec61bb380"})
_pop("tools/round-71/seam-probe.py", {"tools/round-71/seam-probe.py": "22b840e1427b24618ac33075169d29780887d2cffb5b7b989af8cc4bb6ee0ce2"})
_pop("tools/round-72/capsule-audit.py", {"tools/round-72/capsule-audit.py": "d0fbc300c67f9b04915772765c750c40bd433243f8bb7b17b89266556b124219"})
_pop("tools/round-72/packed-elf.py", {"tools/round-72/packed-elf.py": "330ecf89debe550ca2e3799f0a1643728604d24d95924e6d8053433d6e32bab6"},
     ["tools/round-72/packed-elf.py", "--selftest", "--work", "{work}"])
_pop("tools/round-72/seam-probe.py", {"tools/round-72/seam-probe.py": "602b305d79222222c1f17c51cc10365246ecfc184cdd4afd8f773a0f5fd5f0e2"})
_pop("tools/round-74/freeze-pins.py", {"tools/round-74/freeze-pins.py": "29c75405ae7d853b0df7c2ead32b2d2b750be8e80777f6161ec738f8910f5e43"})
_pop("tools/round-74/probe-mutation.py", {"tools/round-74/probe-mutation.py": "156a92945f2acc257b025378e4de49064734a9652de19d6ed04b602161f0319b"})
_pop("tools/round-74/record-audit.py", {"tools/round-74/record-audit.py": "5bcd1462ee25c3ab3ef92f5ff22eda43bfc15dbbca15750f4c678eb9b1a32c5c"})
_pop("tools/round-74/seam-probe.py", {"tools/round-74/seam-probe.py": "81d6a43223c5504eb4ad7312563d7a9b1bd3f6288e39c196ee1d542a4c617039"})
_pop("tools/round-75/freeze-pins.py", {"tools/round-75/freeze-pins.py": "f80ad4079d0746a0f885f5236e23ca7bc48fb3af5f836ad3ec019b6f2720fc5a"})
_pop("tools/round-75/probe-mutation.py", {"tools/round-75/probe-mutation.py": "d7757ae29e184137668c047189aac131b5722641f04a95c063df7aa70de85203"})
_pop("tools/round-75/record-audit.py", {"tools/round-75/record-audit.py": "b81d037d00a3c5137acd73f03456448ae9ef42fc08708f6d892b890715f83d00"})
_pop("tools/round-75/seam-probe.py", {"tools/round-75/seam-probe.py": "1fc1c8fc6d08b8626ead431961f286753805a08893b73bdb2350261ad1ac410d"})
_pop("tools/round-76/plan-command.py", {"tools/round-76/plan-command.py": "c169d670013858c3af9789f2f7f47cc73d9360a09f1436daff7436bca26179e1"},
     ["tools/round-76/plan-command.py", "--root", ".", "--rev", "{rev}", "--work", "{work}", "--selftest"])
_pop("tools/round-76/record-audit.py", {"tools/round-76/record-audit.py": "805a8ba5ff6c83a374e88db589ff95b6f70b90fee1b102123b47ada22fe70f0e"})
_pop("tools/round-77/prefile-receipt.py", {"tools/round-77/prefile-receipt.py": "174eedb56369414f5e4310afa9fe5ee6400e5145e4801452c9d21a7abac2d3fd"})
_pop("tools/round-77/verdict-bind.py", {"tools/round-77/verdict-bind.py": "45280392ff6c59e4c96041544720f055952a11a088769e24cb04207db932a9e7"})
_pop("tools/round-78/surface-recheck.py", {"tools/round-78/surface-recheck.py": "e7ea1717176f3dce2660a10197056b359311c25c5f2490bf9bfbd256c6681a13"})
_pop("tools/round-79/gate-mutation.py", {"tools/round-79/gate-mutation.py": "ff74d63713524f37636257c53ccbe64a64e475b6e9cab7fd7ebcf26d85b3ed02"})
_pop("tools/round-79/pointer-bind.py", {"tools/round-79/pointer-bind.py": "40905d396245313bedb7d0ae25b63f322b39e8e877371630e84d7616f12cb877"})
_pop("tools/round-80/guard-battery.py", {"tools/round-80/guard-battery.py": "b9b3b10c41a329f18ff5b39a4f546875101285ee97d2385de6c36ac84c508272"})
_pop("tools/round-80/pointer-bind.py", {"tools/round-80/pointer-bind.py": "a5755ba1884f0c8d695d16289edbf5dff420e72d7552d424c2cc2df7bb94a438"})
_pop("tools/round-80/receipt-provenance.py", {"tools/round-80/receipt-provenance.py": "80f10a7351c6aaf25ec1cfaac4c2580e2894558c7a16a2661cb5be6ad0f2c64d"})
_pop("tools/round-80/strictness-battery.py", {"tools/round-80/strictness-battery.py": "f2aa8422f4d5ac93d1e3ed2823eb72869694b46682e90d8e1e908c0555da2a0a"})
_pop("tools/round-84/freeze-precheck.py", {"tools/round-84/freeze-precheck.py": "4aae3f26d2c8f5db27d4c91e8ec3facfd24202a937e2dbcbde9263125127380e"})
_pop("tools/round-84/mutation-closure.py", {"tools/round-84/mutation-closure.py": "4d73c89e45fd1657dfc56d30f0ab4e15f08e84093d080f81a6c87668f3cff5ed"})
_pop("tools/round-84/nested-sqfs.py", {"tools/round-84/nested-sqfs.py": "c79dc9b2e1fffcae9f1b8205e29064041c728130c8f9498034e1a7795bea0321"})
_pop("tools/round-85/predicate-bind.py", {"tools/round-85/predicate-bind.py": "a99f8f18c071d7496b07ea65795057484d10904e0501ad47ae6b9190dbfa9b12"})
_pop("tools/round-86/gate-registry.py", {"tools/round-86/gate-registry.py": "b87ffb1b95d02bac1f897a2899a58087462534aafba3515c3b9a6e1cc9bc81a5"})
_pop("tools/round-87/freeze-precheck.py", {"tools/round-87/freeze-precheck.py": "fd5247952d9a4a1cd6e5d2a567548a151a65c5841a47779a870d043b3af6890b"})
_pop("tools/round-87/registry-opened-check.py", {"tools/round-87/registry-opened-check.py": "c579d111a06c25fa3940fd2393db011a0ae1dd963f3257b86e1e71c9062fe670"})
_pop("tools/round-87/upx-magic-repair.py", {"tools/round-87/upx-magic-repair.py": "96da7d8e981b04f5a598dc7eb8ec3f05eeae4b1498f769c83e72c67f6babec24"})
_pop("tools/round-87/upx-tamper-battery.py", {"tools/round-87/upx-tamper-battery.py": "0f2d2bd80108ded5282dbb8cbf79044357538458143c97ee591cc78e8e5384b0"})
_pop("tools/round-88/upx-chain-repair.py", {"tools/round-88/upx-chain-repair.py": "59ee51b0e63d3e089c23cee066b637841133412cee50748d84d717d61f8a0b46"})
_pop("tools/round-89/depth-blocks-v2.py", {"tools/round-89/depth-blocks-v2.py": "359f15e1c87f5106aa3fcbef211568ab7a970564ea0d7ed877299ca706dcf18f"})
_pop("tools/round-89/upx-field-value-repair.py", {"tools/round-89/upx-field-value-repair.py": "41f29f211fcaef9cb57fb1a03858c590711dc9c3d7e0f28d36335178485b1d5d"})
_pop("tools/round-90/upx-break-repair.py", {"tools/round-90/upx-break-repair.py": "90dea08720a37e876e7f08eafe339a62c710baf402c1342924f9b41b44d5cd6a"})
_pop("tools/round-91/depth-blocks-v3.py", {"tools/round-91/depth-blocks-v3.py": "bcf6c4ea31047401d16ce47562e58bf1d76eec7b1c9da0ff5e222793aeeb052f"})
_pop("tools/round-91/record-cells.py", {"tools/round-91/record-cells.py": "87ff58444315a76b944f93e9f4b8f6df19d29d1730a55dfeae6f830a4b6b669b"})
_pop("tools/round-91/upx-stop-boundary-repair.py", {"tools/round-91/upx-stop-boundary-repair.py": "3779d35fc8f57bc9f573b87b5b4e566e159ac58737b3942be6b840f649e3f238"})
_pop("tools/round-92/upx-stop-boundary-search-repair.py", {"tools/round-92/upx-stop-boundary-search-repair.py": "ce1b1769d56c1d90fcf2ee0800ca508476b45eddc2e8a6d7e2f01aa8d12a70c1"})
_pop("tools/round-95/c1-agreement-v2.py", {"tools/round-95/c1-agreement-v2.py": "ca7d213a598fb79fd944886d480863d6464cb2217c8d2d4b9f11c7981c539291"},
     ["tools/round-95/c1-agreement-v2.py", "--selftest", "{work}"])
_pop("tools/round-95/c1-forgery-refusal.py", {"tools/round-95/c1-forgery-refusal.py": "8e43d7cff4d8f7eb9f4afe8e2ebdcfb3edfe6a53f019f21d0cd415457de0ff22"},
     ["tools/round-95/c1-forgery-refusal.py", "--selftest", "{work}"])
_pop("tools/round-95/stop-boundary-repair-battery-v5.py", {"tools/round-95/stop-boundary-repair-battery-v5.py": "6fc81208c9b151f35c9768bc1f481a1bdd0bcc0854d9732879e38e6b87194b7f"},
     ["tools/round-95/stop-boundary-repair-battery-v5.py", "--selftest", "--work", "{work}"])
_pop("tools/round-96/kill-rule-v2.py", {"tools/round-96/kill-rule-v2.py": "3b8c7583c9c9d6aa9e42a6a8e718d16bac4371a4fbdf7fd345f0190b1dc9bb5f"})
_pop("tools/round-96/stop-boundary-repair-battery-v6.py", {"tools/round-96/stop-boundary-repair-battery-v6.py": "7d7d559ac144eda6d163dd1d9ab26ed95ac089e18ccbb029bd91ae4277e46c06"})
_pop("tools/round-97/craft-citation-v2.py", {"tools/round-97/craft-citation-v2.py": "a50aa02d6f6b1ac1df0842d911df1977f8de6c43b969a4df194082dbe74fee7b"})
_pop("tools/round-97/stop-boundary-repair-battery-v7.py", {"tools/round-97/stop-boundary-repair-battery-v7.py": "2cd984f3a949520965487992c1c3917ff33a37bcf4221fe411fb990033ee8b58"})
_pop("tools/round-98/stop-boundary-repair-battery-v8.py", {"tools/round-98/stop-boundary-repair-battery-v8.py": "7a9837466d2d4eeb0a8096b71b8033c970ac2c43e00ec6f10cc8dd4f6de08a83"})
_pop("tools/round-99/self-assessment-audit.py", {"tools/round-99/self-assessment-audit.py": "e732465bde4d7c125b45fc60ead9343ee6d1c73378830e42e028ac2d0334eec0"})
TARGET = ("rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93; "
          "mismatches 0")

if __name__ == "__main__":
    sys.exit(main())
