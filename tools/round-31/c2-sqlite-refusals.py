#!/usr/bin/env python3
"""R31-C2 counter: REA 6.5.0 `inspect-sqlite-database` refusal and edge signatures
predicted from the 6.5.0 code (S092) before any run, tested live on 23 requests.

Predicate P2-match (frozen in .ufo/waves/round-31/claims.json): a request matches when
its live REA 6.5.0 run agrees with its frozen prediction -- for a predicted refusal the
process exits 1, the envelope has ok=false, error.code equals the predicted code and
error.details.issues is exactly one issue equal to {path, reason, message} as predicted
(message with {P} replaced by the request path); for a predicted acceptance the run
exits 0 with an ok inspect_sqlite_database envelope whose subject sha256 is the
request file's sha256 and whose report equals the independent oracle (scope database)
or, for q-ok-rows, whose rows block selects Album with row_limit 3, 3 rows, columns
AlbumId, Title, ArtistId, each row present in the oracle's table; and the committed
envelope, first added after the freeze commit, equals the live envelope in every
field except meta (the full-envelope rule that repairs M30-3).

Modes: --build creates the mutants (outside the lane), --selftest runs offline cases,
default measures.  Prints `requests=N matches=M target=23 entry_ok=E skill_ok=S`.
"""

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import subprocess
import sys

TARGET = 23
REA = ["npx", "-y", "rea-agents@6.5.0"]
PKG_JSON = os.path.expanduser("~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/package.json")
CLAIM_ROW = "S092"
ENTRY = "corpus/knowledge/2026-10-23-r31-sqlite-refusals.md"
PRED = "corpus/evidence/round-31/c2/predictions.tsv"
CARRIERS = "corpus/evidence/round-31/c1/carriers.tsv"
CLAIMS = ".ufo/waves/round-31/claims.json"
ENV_DIR = "corpus/evidence/round-31/c2/envelopes"
HERE = os.path.dirname(os.path.abspath(__file__))
LABEL = "P2-match"
BUDGET = 268435456


def load_oracle():
    spec = importlib.util.spec_from_file_location("sqlite_oracle", os.path.join(HERE, "sqlite_oracle.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def git(root, *args):
    return subprocess.run(["git", "-C", root] + list(args), capture_output=True, text=True)


def show(root, rev, rel):
    p = git(root, "show", rev + ":" + rel)
    return p.stdout if p.returncode == 0 else None


def parse_tsv(text):
    lines = text.splitlines()
    head = lines[0].split("\t")
    return [dict(zip(head, ln.split("\t"))) for ln in lines[1:] if ln]


def carrier_sha(root, rev):
    text = show(root, rev, CARRIERS)
    if text is None:
        return None
    return {r["path"]: r["sha256"] for r in parse_tsv(text)}


def base_of(path):
    return "/fast/scratch/hyaku/kaidoku-r31/carriers/chinook.sqlite"


def build(root, rev):
    rows = parse_tsv(show(root, rev, PRED) or open(os.path.join(root, PRED)).read())
    base = base_of(None)
    data = open(base, "rb").read()
    for r in rows:
        kind, path = r["build"], r["path"]
        if kind == "none":
            continue
        d = os.path.dirname(path)
        if kind == "enotdir":
            d = os.path.dirname(d)
        if os.path.lexists(d):
            continue
        os.makedirs(d)
        if kind == "absent":
            continue
        if kind == "enotdir":
            open(os.path.join(d, "file"), "wb").write(b"not a directory\n")
            continue
        if kind == "directory":
            os.makedirs(path)
            continue
        if kind == "db-symlink":
            os.symlink(base, path)
            continue
        if kind == "zero-magic":
            open(path, "wb").write(b"\x00" * 16 + data[16:])
            continue
        if kind == "pagesize-768":
            open(path, "wb").write(data[:16] + b"\x03\x00" + data[18:])
            continue
        if kind == "sparse-268435457":
            with open(path, "wb") as f:
                f.write(data[:4096])
                f.truncate(BUDGET + 1)
            continue
        shutil.copyfile(base, path)
        j = path + "-journal"
        if kind == "journal-hot":
            open(j, "wb").write(bytes([0xD9, 0xD5, 0x05, 0xF9, 0x20, 0xA1, 0x63, 0xD7]) + b"\x00" * 20)
        elif kind == "journal-short":
            open(j, "wb").write(b"\x00" * 10)
        elif kind == "journal-empty":
            open(j, "wb").close()
        elif kind == "journal-zero28":
            open(j, "wb").write(b"\x00" * 28)
        elif kind == "journal-symlink":
            os.symlink(base, j)
        elif kind == "wal-sparse":
            with open(path + "-wal", "wb") as f:
                f.truncate(BUDGET + 1 - len(data))
        else:
            raise SystemExit("unknown build kind %s" % kind)
    print("built under /fast/scratch/hyaku/kaidoku-r31/mutants")
    return 0


def run_rea(path, args):
    start = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    argv = REA + ["inspect-sqlite-database", path] + args + ["--format", "json", "--full-output"]
    p = subprocess.run(argv, capture_output=True, timeout=300, cwd="/tmp")
    end = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    return argv, p.returncode, p.stdout, p.stderr, start, end


def strip_meta(env):
    if not isinstance(env, dict):
        return env
    return {k: v for k, v in env.items() if k != "meta"}


def judge(row, env, code, oracle, file_sha):
    """Return (verdict, reason) for the live half of P2."""
    path = row["path"]
    if not isinstance(env, dict):
        return "P2-miss", "no JSON envelope (exit %s)" % code
    if row["outcome"] == "refuse":
        if code != int(row["exit"]):
            return "P2-miss", "exit %s != %s" % (code, row["exit"])
        if env.get("ok") is not False:
            return "P2-miss", "envelope ok, refusal predicted"
        err = env.get("error") or {}
        if err.get("code") != row["code"]:
            return "P2-miss", "code %r != %r" % (err.get("code"), row["code"])
        issues = (err.get("details") or {}).get("issues")
        want = {"path": json.loads(row["issue_path"]), "reason": row["issue_reason"],
                "message": row["message"].replace("{P}", path)}
        if issues != [want]:
            return "P2-miss", "issues %s != [%s]" % (json.dumps(issues)[:300], json.dumps(want))
        return LABEL, "refused %s %s" % (row["code"], row["issue_reason"])
    if code != 0 or env.get("ok") is not True:
        return "P2-miss", "accept predicted, exit %s ok %r" % (code, env.get("ok"))
    data = env.get("data") or {}
    if data.get("operation") != "inspect_sqlite_database":
        return "P2-miss", "operation %r" % data.get("operation")
    if ((data.get("subject") or {}).get("digest") or {}).get("sha256") != file_sha:
        return "P2-miss", "subject sha256 differs from the request file"
    nr = data.get("normalized_result") or {}
    if row["id"] == "q-ok-rows":
        rows = nr.get("rows") or {}
        if rows.get("table") != "Album" or rows.get("row_limit") != 3 or rows.get("returned_rows") != 3:
            return "P2-miss", "rows block %s" % json.dumps({k: rows.get(k) for k in ("table", "row_limit", "returned_rows")})
        if rows.get("columns") != ["AlbumId", "Title", "ArtistId"]:
            return "P2-miss", "columns %r" % rows.get("columns")
        want_rows = oracle["album_rows"]
        for vals in rows.get("values") or []:
            try:
                got = (int(vals[0]["value"]), vals[1]["value"], int(vals[2]["value"]))
            except (KeyError, IndexError, TypeError, ValueError):
                return "P2-miss", "row shape"
            if got not in want_rows:
                return "P2-miss", "row %r not in the oracle's Album table" % (got,)
        album = [t for t in oracle["report"]["schema"]["tables"] if t["name"] == "Album"]
        if (nr.get("schema") or {}).get("tables") != album:
            return "P2-miss", "selected-table schema differs from the oracle"
        return LABEL, "accepted, 3 Album rows"
    exp = dict(oracle["report"])
    if load_oracle().comparable(nr) != exp:
        return "P2-miss", "report differs from the oracle"
    return LABEL, "accepted, report equals oracle"


def oracle_for(row, oracle_mod):
    if row["outcome"] != "accept":
        return None
    import sqlite3
    rep = oracle_mod.expected_report(row["path"])
    out = {"report": rep}
    if row["id"] == "q-ok-rows":
        con = sqlite3.connect("file:%s?mode=ro&immutable=1" % row["path"], uri=True)
        out["album_rows"] = set(tuple(r) for r in con.execute("SELECT AlbumId, Title, ArtistId FROM Album"))
        con.close()
        rep = dict(rep)
        rep["schema"] = dict(rep["schema"])
        out["report"] = rep
    return out


def file_sha(path):
    if os.path.isfile(path) and not os.path.islink(path):
        h = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    return None


def first_added(root, rel, rev):
    p = git(root, "log", rev, "--diff-filter=A", "--format=%ct", "--", rel)
    t = [int(x) for x in p.stdout.split()]
    return min(t) if t else None


def committed_check(root, rev, rid, live, freeze_ct, entry_text):
    rel = ENV_DIR + "/" + rid + ".json"
    text = show(root, rev, rel)
    if text is None:
        return False, "committed envelope absent"
    added = first_added(root, rel, rev)
    if freeze_ct is None or added is None or added <= freeze_ct:
        return False, "committed envelope not added after the freeze"
    try:
        committed = json.loads(text)
    except ValueError:
        return False, "committed envelope is not JSON"
    if strip_meta(committed) != strip_meta(live):
        return False, "committed envelope differs from the live envelope (full comparison)"
    if rid not in entry_text:
        return False, "entry does not name %s" % rid
    return True, "ok"


def entry_ok(root, rev):
    text = show(root, rev, ENTRY)
    if text is None:
        return False, "entry absent"
    if CLAIM_ROW not in text:
        return False, "entry does not cite %s" % CLAIM_ROW
    return True, "ok"


def skill_ok(root, rev, rows):
    """SKILL.md holds a table row per request id naming its predicted code and message."""
    text = show(root, rev, "SKILL.md") or ""
    table = [ln for ln in text.splitlines() if ln.startswith("|")]
    missing = []
    for r in rows:
        want = r["code"] if r["outcome"] == "refuse" else "accept"
        msg = r["message"].split("{P}")[0].rstrip(": ") if r["outcome"] == "refuse" else ""
        hit = [ln for ln in table if ("`%s`" % r["id"]) in ln and want in ln and msg in ln]
        if not hit:
            missing.append(r["id"])
    if "inspect-sqlite-database" not in text or ENTRY not in text:
        return False, "SKILL names neither the verb nor the entry"
    if missing:
        return False, "no SKILL table row for %s" % ",".join(missing[:5])
    return True, "ok"


def measure(root, rev, write):
    pred_text = show(root, rev, PRED)
    if pred_text is None:
        print("PIN predictions absent at %s" % rev)
        return 2
    if pred_text != open(os.path.join(root, PRED)).read():
        print("PIN predictions in the tree differ from %s" % rev)
        return 2
    rows = parse_tsv(pred_text)
    if len(rows) != TARGET:
        print("PIN %d predictions, frozen %d" % (len(rows), TARGET))
        return 2
    shas = carrier_sha(root, rev)
    if shas is None:
        print("PIN carrier list absent at %s" % rev)
        return 2
    base = base_of(None)
    if file_sha(base) != shas.get(base):
        print("PIN base carrier absent or altered: %s" % base)
        return 2
    if json.load(open(PKG_JSON))["version"] != "6.5.0":
        print("PIN package version")
        return 2
    pkg_sha = hashlib.sha256(open(PKG_JSON, "rb").read()).hexdigest()
    claims = show(root, rev, CLAIMS)
    pins = json.loads(claims).get("mutant_sha256", {}) if claims else {}
    sib_pins = json.loads(claims).get("mutant_sibling_sha256", {}) if claims else {}
    for r in rows:
        if r["build"] in ("zero-magic", "pagesize-768", "journal-hot", "journal-short", "journal-empty",
                          "journal-zero28", "journal-symlink", "wal-sparse", "sparse-268435457"):
            if not os.path.lexists(r["path"]) or file_sha(r["path"]) != pins.get(r["id"]):
                print("PIN mutant %s absent or altered" % r["id"])
                return 2
            for suffix in ("-journal", "-wal"):
                sib = r["path"] + suffix
                key = r["id"] + suffix
                if key in sib_pins and (file_sha(sib) if not os.path.islink(sib) else "symlink:" + os.readlink(sib)) != sib_pins[key]:
                    print("PIN mutant sibling %s absent or altered" % key)
                    return 2
        if r["build"] == "none" and file_sha(r["path"]) != shas.get(r["path"]):
            print("PIN carrier for %s absent or altered" % r["id"])
            return 2
        state = {"absent": lambda p: not os.path.lexists(p) and os.path.isdir(os.path.dirname(p)),
                 "enotdir": lambda p: os.path.isfile(os.path.dirname(p)),
                 "directory": os.path.isdir,
                 "db-symlink": lambda p: os.path.islink(p) and os.readlink(p) == base}.get(r["build"])
        if state is not None and not state(r["path"]):
            print("PIN mutant %s not in its built state" % r["id"])
            return 2
    oracle_mod = load_oracle()
    p = git(root, "log", rev, "--diff-filter=A", "--format=%ct", "--", CLAIMS)
    times = [int(x) for x in p.stdout.split()]
    freeze_ct = min(times) if times else None
    entry_text = show(root, rev, ENTRY) or ""
    matches = 0
    runs = []
    for r in rows:
        oracle = oracle_for(r, oracle_mod)
        argv, code, out, err, start, end = run_rea(r["path"], json.loads(r["args"]))
        try:
            env = json.loads(out)
        except ValueError:
            env = None
        verdict, reason = judge(r, env, code, oracle, file_sha(r["path"]))
        if verdict == LABEL and not write:
            ok, why = committed_check(root, rev, r["id"], env, freeze_ct, entry_text)
            if not ok:
                verdict, reason = "P2-miss", why
        matches += verdict == LABEL
        print("%s\t%s\t%s" % (r["id"], verdict, reason))
        runs.append((r["id"], start, end, code, " ".join(argv), "6.5.0", pkg_sha, verdict, reason))
        if write:
            d = os.path.join(root, ENV_DIR)
            os.makedirs(d, exist_ok=True)
            open(os.path.join(d, r["id"] + ".json"), "wb").write(out)
            open(os.path.join(d, r["id"] + ".stderr"), "wb").write(err)
    if write:
        with open(os.path.join(root, os.path.dirname(ENV_DIR), "runs.tsv"), "w") as f:
            f.write("id\tutc_start\tutc_end\texit\targv\tpkg_version\tpkg_json_sha256\tverdict\treason\n")
            for row in runs:
                f.write("\t".join(str(x) for x in row) + "\n")
    e_ok, e_why = entry_ok(root, rev)
    s_ok, s_why = skill_ok(root, rev, rows)
    print("requests=%d matches=%d target=%d entry_ok=%d (%s) skill_ok=%d (%s)" % (
        len(rows), matches, TARGET, e_ok, e_why, s_ok, s_why))
    return 0 if matches == TARGET and e_ok and s_ok else 1


def selftest():
    fails = 0
    row = {"id": "x", "path": "/p/db", "outcome": "refuse", "exit": "1", "code": "invalid_request",
           "issue_path": '["path"]', "issue_reason": "invalid_value", "message": "gone: {P}"}
    good = {"ok": False, "error": {"code": "invalid_request", "details": {"issues": [
        {"path": ["path"], "reason": "invalid_value", "message": "gone: /p/db"}]}}}
    cases = [
        ("refusal exact", row, good, 1, LABEL),
        ("refusal wrong exit", row, good, 0, "P2-miss"),
        ("refusal wrong code", row, {"ok": False, "error": {"code": "x", "details": good["error"]["details"]}}, 1, "P2-miss"),
        ("refusal wrong message", row, json.loads(json.dumps(good).replace("gone: /p/db", "gone: /q")), 1, "P2-miss"),
        ("refusal wrong reason", row, json.loads(json.dumps(good).replace("invalid_value", "invalid_format")), 1, "P2-miss"),
        ("refusal extra issue", row, {"ok": False, "error": {"code": "invalid_request", "details": {"issues": good["error"]["details"]["issues"] * 2}}}, 1, "P2-miss"),
        ("refusal but ok", row, {"ok": True, "data": {}}, 1, "P2-miss"),
        ("no envelope", row, None, 1, "P2-miss"),
        ("accept but refused", dict(row, outcome="accept", id="m"), good, 1, "P2-miss"),
    ]
    for name, r, env, code, want in cases:
        got, why = judge(r, env, code, None, None)
        ok = got == want
        fails += not ok
        print("%s\t%s\t%s" % ("ok" if ok else "FAIL", name, why))
    a = {"ok": True, "data": {"x": 1}, "meta": {"duration": "1ms"}}
    b = {"ok": True, "data": {"x": 1}, "meta": {"duration": "9ms"}}
    c = {"ok": True, "data": {"x": 2}, "meta": {"duration": "1ms"}}
    for name, x, y, want in [("meta ignored", a, b, True), ("data compared", a, c, False),
                             ("error compared", good, json.loads(json.dumps(good).replace("invalid_request", "y")), False)]:
        ok = (strip_meta(x) == strip_meta(y)) == want
        fails += not ok
        print("%s\t%s" % ("ok" if ok else "FAIL", name))
    print("selftest cases=%d failures=%d" % (len(cases) + 3, fails))
    return 0 if fails == 0 else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=os.getcwd())
    ap.add_argument("--rev", default="main")
    ap.add_argument("--write-evidence", action="store_true")
    ap.add_argument("--build", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    for k in ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE"):
        os.environ.pop(k, None)
    if a.selftest:
        sys.exit(selftest())
    if a.build:
        sys.exit(build(a.root, a.rev))
    sys.exit(measure(os.path.abspath(a.root), a.rev, a.write_evidence))


if __name__ == "__main__":
    main()
