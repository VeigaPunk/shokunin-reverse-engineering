#!/usr/bin/env python3
"""Outer CLI selftest for the round-34 legacy-gap repairs.

Runs, as separate processes under fixed time/memory/file-size bounds:

  A  wrapper_successor.py --selftest                      (green, 20 cases)
  B  wrapper_successor.py --input fixtures/wrapper/*.json  (good green; 6 red)
  C  four r32 C1 wrapper mutants applied to private copies  (each must be killed)
  D  quote_support_successor.py --selftest                 (green, 9 cases)
  E  quote case fixtures, good and tampered                (green / red)
  F  two quote-core mutants applied to private copies      (each must be killed)
  G  archived independent-pe/compare.py replayed on an isolated text/JSON
     fixture through replay/indep_pe_replay.py             (green / red)
  H  pe_own_compare.py                                     (NOT RUN: needs binary)

No file in the repository is modified; mutant copies live in a temporary
directory under this seat's own output directory and are deleted afterwards.
Nothing reads git, the network, carrier bytes, or /fast/scratch.

Exit: 0 every executed expectation met, 1 any mismatch, 2 harness unusable.
"""

import hashlib
import json
import os
import pathlib
import shutil
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
REPO = HERE.parents[4]
ARCHIVED_COMPARE = REPO / ".ufo/waves/round-32/independent-pe/compare.py"
PE_OWN_COMPARE = REPO / ".ufo/waves/round-32/final-c1-witness/pe_own_compare.py"
WRAPPER = HERE / "wrapper_successor.py"
QUOTE = HERE / "quote_support_successor.py"
REPLAY = HERE / "replay/indep_pe_replay.py"
BOUND = ["timeout", "--kill-after=5s", "120s",
         "prlimit", "--as=2147483648", "--fsize=4194304", "--",
         "python3", "-I", "-B"]

WRAPPER_MUTANTS = [
    ("C1-1", "    if claim_row not in text:", "    if not text:",
     "C1-1 kill: entry without the claim row"),
    ("C1-2", "    if strip_meta(committed) != strip_meta(live):",
     '    if committed.get("data") != (live or {}).get("data"):',
     "C1-2 kill: same data, committed top-level ok differs"),
    ("C1-3", "    if not isinstance(text, str) or eid not in text:",
     "    if not isinstance(text, str):",
     "C1-3 kill: live evidence_id omitted from the entry"),
    ("C1-4", "    if added > freeze_ct:", "    if added >= freeze_ct:",
     "C1-4 kill: first-added exactly at the freeze commit time"),
]

QUOTE_MUTANTS = [
    ("Q-1", "    if w > MAX_WORDS:", "    if w > MAX_WORDS + 1:",
     "contiguous 26-word run present in the bytes"),
    ("Q-2", "    if want_line is not None and ln != want_line:",
     "    if want_line is not None and ln is None:",
     "quote located later than the expected line"),
]

FIXTURE_EXPECT = [
    ("accept-good", 0, "failures=0"),
    ("bad-source", 1, "FAIL\tentry_cite"),
    ("bad-envelope-ok", 1, "FAIL\tenvelope_equal"),
    ("bad-envelope-extra", 1, "FAIL\tenvelope_equal"),
    ("bad-evidence", 1, "FAIL\tevidence_id"),
    ("bad-freeze-boundary", 1, "FAIL\tpost_freeze"),
    ("bad-committed-list", 1, "FAIL\tcommitted_json"),
]


def sha(path):
    return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()


def clean_env():
    return {k: v for k, v in os.environ.items()
            if k not in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE")}


def run(name, argv, cwd):
    started = time.time()
    proc = subprocess.run(argv, cwd=str(cwd), env=clean_env(), capture_output=True,
                          text=True, timeout=150)
    return {"name": name, "argv": [str(a) for a in argv], "exit": proc.returncode,
            "stdout": proc.stdout, "stderr": proc.stderr,
            "seconds": round(time.time() - started, 3),
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}


class Receipt:
    def __init__(self):
        self.records = []
        self.failures = 0
        (HERE / "receipts").mkdir(exist_ok=True)

    def add(self, rec, expect_exit, must_stdout=()):
        ok = rec["exit"] == expect_exit
        missing = [s for s in must_stdout if s not in rec["stdout"]]
        if missing:
            ok = False
        rec["expect_exit"] = expect_exit
        rec["must_stdout"] = list(must_stdout)
        rec["missing_stdout"] = missing
        rec["pass"] = ok
        self.failures += not ok
        text = ("# %s\nstart_utc=%s exit=%d expect_exit=%d pass=%s seconds=%s\n"
                "# argv: %s\n# must_stdout: %s missing=%s\n\n## stdout\n%s\n## stderr\n%s\n"
                % (rec["name"], rec["utc"], rec["exit"], expect_exit, ok, rec["seconds"],
                   json.dumps(rec["argv"]), json.dumps(list(must_stdout)),
                   json.dumps(missing), rec["stdout"], rec["stderr"]))
        safe = "".join(c if c.isalnum() or c in "-_." else "_" for c in rec["name"])
        (HERE / "receipts" / (safe + ".txt")).write_text(text)
        print("%s\t%s\texit=%s%s" % ("ok" if ok else "FAIL", rec["name"], rec["exit"],
                                     "" if not missing else "\tmissing=%s" % missing))
        self.records.append({k: rec[k] for k in
                             ("name", "argv", "exit", "expect_exit", "pass", "seconds", "utc",
                              "must_stdout", "missing_stdout")})
        return ok


def mutate_copy(source_text, old, new, path):
    if source_text.count(old) != 1:
        raise SystemExit("harness: clause %r occurs %d times, expected 1"
                         % (old, source_text.count(old)))
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(source_text.replace(old, new))
    return path


def prepare_indep_fixture(dest, tamper):
    src = HERE / "fixtures/indep-pe"
    prov = json.loads((src / "provenance.json").read_text())
    if prov.get("binary_content") is not False:
        raise SystemExit("harness: independent-pe fixture provenance does not declare text/JSON only")
    drift = [n for n, want in prov["fixture_sha256"].items() if sha(src / n) != want]
    if drift:
        raise SystemExit("harness: independent-pe fixture drift %s" % drift)
    dest.mkdir(parents=True, exist_ok=True)
    for item in src.iterdir():
        if item.is_file():
            shutil.copyfile(item, dest / item.name)
    if tamper:
        doc = json.loads((dest / "indep.json").read_text())
        sha_old = doc["results"][0]["sha256"]
        doc["results"][0]["sha256"] = sha_old[:-1] + ("0" if sha_old[-1] != "0" else "1")
        (dest / "indep.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n")
        return sha_old, doc["results"][0]["sha256"]
    return None, None


def main():
    tmp = HERE / "tmp" / ("run-%d" % os.getpid())
    if tmp.exists():
        shutil.rmtree(tmp)
    tmp.mkdir(parents=True)
    before = {p.name: sha(p) for p in (WRAPPER, QUOTE, REPLAY, ARCHIVED_COMPARE, PE_OWN_COMPARE)}
    r = Receipt()

    try:
        # A. wrapper successor selftest, in place
        r.add(run("A wrapper selftest", BOUND + [WRAPPER, "--selftest"], HERE), 0,
              ["selftest cases=20 failures=0"])

        # B. wrapper JSON fixtures through the outer CLI
        for name, code, needle in FIXTURE_EXPECT:
            r.add(run("B wrapper fixture %s" % name,
                      BOUND + [WRAPPER, "--input", HERE / "fixtures/wrapper" / (name + ".json")],
                      HERE), code, [needle])

        # C. r32 C1 wrapper mutants against private copies
        wrapper_src = WRAPPER.read_text()
        for mid, old, new, case in WRAPPER_MUTANTS:
            path = mutate_copy(wrapper_src, old, new, tmp / ("mut-" + mid) / WRAPPER.name)
            r.add(run("C mutant %s (%s)" % (mid, case),
                      BOUND + [path, "--selftest"], HERE), 1, ["FAIL\t" + case])

        # D. quote successor selftest
        r.add(run("D quote selftest", BOUND + [QUOTE, "--selftest"], HERE), 0,
              ["selftest cases=9 failures=0"])

        # E. quote case fixtures: green and tampered
        r.add(run("E quote cases green",
                  BOUND + [QUOTE, "--root", HERE / "fixtures/quote", "--cases",
                           HERE / "fixtures/quote/cases.json"], HERE), 0,
              ["support=7 informational=2 failures=0"])
        r.add(run("E quote cases tampered",
                  BOUND + [QUOTE, "--root", HERE / "fixtures/quote", "--cases",
                           HERE / "fixtures/quote/cases-tampered.json"], HERE), 1,
              ["failures=2"])

        # F. quote-core mutants
        quote_src = QUOTE.read_text()
        for mid, old, new, case in QUOTE_MUTANTS:
            path = mutate_copy(quote_src, old, new, tmp / ("mut-" + mid) / QUOTE.name)
            r.add(run("F mutant %s (%s)" % (mid, case),
                      BOUND + [path, "--selftest"], HERE), 1, ["FAIL\t" + case])

        # G. archived independent-pe comparator on an isolated text/JSON fixture
        version = subprocess.run(["llvm-readobj", "--version"], capture_output=True, text=True)
        version_line = version.stdout.splitlines()[1].strip() if len(version.stdout.splitlines()) > 1 else None
        if version.returncode != 0 or version_line is None:
            raise SystemExit("harness: llvm-readobj unavailable; replay would be could-not-evaluate")
        green = tmp / "indep-green"
        prepare_indep_fixture(green, tamper=False)
        r.add(run("G archived independent-pe green",
                  BOUND + [REPLAY, ARCHIVED_COMPARE, green, green / "carriers.tsv"], HERE), 0,
              ["checks=31 passed=31 failed=0"])
        red = tmp / "indep-red"
        old_sha, new_sha = prepare_indep_fixture(red, tamper=True)
        r.add(run("G archived independent-pe red (tampered sha256)",
                  BOUND + [REPLAY, ARCHIVED_COMPARE, red, red / "carriers.tsv"], HERE), 1,
              ["label_sha256"])

        # H. binary-dependent archived gate: recorded, never called
        not_run = {
            "name": "H pe_own_compare.py selftest",
            "status": "open-bounded-limit",
            "reason": ("own_parse requires the pinned carrier DLL bytes; no binary fixture may be "
                       "authored in this seat, and the committed captures alone do not reconstruct "
                       "the bytes (SKILL.md:1100). Not executed, not declared conformant."),
            "archived_sha256": sha(PE_OWN_COMPARE),
        }

        after = {p.name: sha(p) for p in (WRAPPER, QUOTE, REPLAY, ARCHIVED_COMPARE, PE_OWN_COMPARE)}
        changed = {k: [before[k], after[k]] for k in before if before[k] != after[k]}
        meta = {
            "schema": "r34-legacy-gaps-receipt-v1",
            "utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "bounds": {"wrapper": BOUND[:6], "timeout_s": 120, "as_bytes": 2147483648,
                       "fsize_bytes": 4194304, "llvm_readobj": version_line},
            "source_sha256_unchanged": not changed,
            "source_sha256": after,
            "changed_sources": changed,
            "archived_inputs": {"independent-pe/compare.py": sha(ARCHIVED_COMPARE),
                                "final-c1-witness/pe_own_compare.py": sha(PE_OWN_COMPARE)},
            "checks": r.records,
            "checks_run": len(r.records),
            "checks_failed": r.failures,
            "not_run": [not_run],
            "indep_red_sha": [old_sha, new_sha],
        }
        (HERE / "run-receipt.json").write_text(json.dumps(meta, indent=1, sort_keys=True) + "\n")
        print("checks=%d passed=%d failed=%d not_run=%d source_unchanged=%s"
              % (len(r.records), len(r.records) - r.failures, r.failures,
                 len(meta["not_run"]), not changed))
        return 0 if r.failures == 0 and not changed else 1
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
