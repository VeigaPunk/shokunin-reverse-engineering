#!/usr/bin/env python3
"""R33 generic structural-match measurement driver (scratch only; not a semantic proof).

  measure_driver.py --classifier C --manifest M --manifest-sha256 H [--classifier-sha256 H]
                    [--document-spec D [--document-spec-sha256 H]]
                    [--repo R --rev REV] [--timeout S] [--order random|manifest]
  measure_driver.py --selftest

P33-structural-match: a fixture matches when its pinned bytes are decoded by the selected classifier and
its structural finding id equals the independently frozen expected id; when a row also carries
"expected_facts", every selected key in it must equal the classifier's parsed output with strict types.

Manifest (JSON): {"schema": "r33-structural-manifest/1",
                  "rows": [{"id", "path", "sha256", "expected_finding_id"[, "expected_facts"]}, ...]}
Without --repo, the classifier, manifest and row paths are absolute worktree paths. With --repo/--rev they
are repo-relative and read from Git objects of that revision (`git cat-file blob REV:PATH`), so worktree
edits cannot change what is measured.

Document spec (optional, JSON, frozen before data): {"schema": "r33-document-spec/1",
  "checks": [
    {"kind": "file_sha256",  "path": P, "sha256": H},
    {"kind": "file_quote",   "path": P, "line": N, "quote": S},        # quote must occur on line N (1-based)
    {"kind": "file_section", "path": P, "heading": H, "text_file": F,  # body EXCLUDES the heading line
                                "text_file_sha256": H},
    {"kind": "file_any_line","path": P, "lines": [S, ...]},
    {"kind": "file_exists",  "path": P}, ...]}
file_section compares the body after its heading to the approved text_file, applying the same
leading/trailing-blank-line and per-line right-whitespace normalization to both. The approved file
itself is pinned by sha256. file_sha256 pins whole-file bytes so a fabricated or off-topic file
cannot pass by carrying one quoted phrase. All reads use the same Source (worktree or Git rev).
No NLP: wording is reviewed separately.

For every row the driver checks the bytes against the row's sha256, writes them to a fresh random path
(random directory, random file name, no extension, read-only) under this seat's scratch tmp dir, and runs
`python3 -I -B CLASSIFIER PATH` with a minimal environment and an empty working directory. The classifier
receives nothing else: no row id, no expected id, no expected_facts, no original file name. Its stdout
must be one JSON object with a string `finding_id`; only that output object is compared. The classifier
itself is run from a pinned private copy of its bytes.

Receipt/exit contract (claim counter, not a probe): exit 0 only when every row was evaluated, matched and
fact-matched, and docs_ok is true when a document spec was supplied. Exit 1 when rows were evaluated but
some mismatched or a docs check failed. Exit 3 when some row could not be evaluated (pin mismatch,
fixture mutated, classifier error). Exit 2 on refusal (usage, manifest/spec digest or shape mismatch).
Classifier exits like 10/11/12 are normal observations, never driver errors.
"""

import argparse
import hashlib
import json
import os
import random
import resource
import secrets
import shutil
import signal
import subprocess
import sys
import tempfile
import time

LABEL = "P33-structural-match"
DEFINITION = ("A fixture matches when its pinned bytes are decoded by the selected classifier, its "
              "structural finding id equals the independently frozen expected id and its required facts "
              "equal the parsed output with exact recursive types; the target is met only when every "
              "frozen fixture matches and all supplied pinned-source, located-quote and approved-table "
              "checks pass.")
NOT_PROOF = ("driver output measures agreement of finding ids/facts only; it is not evidence that any "
             "fixture is a genuine hybrid or that the classifier is semantically correct")
SCHEMA = "r33-measure-driver/1"
MANIFEST_SCHEMA = "r33-structural-manifest/1"
DOC_SPEC_SCHEMA = "r33-document-spec/1"
ROW_KEYS = {"id", "path", "sha256", "expected_finding_id"}
ROW_OPT = {"expected_facts"}
CHECK_KINDS = ("file_sha256", "file_quote", "file_section", "file_any_line", "file_exists")
STDOUT_CAP = 1 << 20
MEM_CAP = 1 << 30
SCRATCH_TMP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tmp")


def _tmpdir(prefix=""):
    os.makedirs(SCRATCH_TMP, exist_ok=True)
    return tempfile.mkdtemp(prefix=prefix, dir=SCRATCH_TMP)


class Refuse(Exception):
    pass


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def git_env():
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


class Source:
    def __init__(self, repo=None, rev=None):
        self.repo, self.rev, self.commit = repo, rev, None
        if repo is not None:
            p = subprocess.run(["git", "-C", repo, "rev-parse", "--verify", "%s^{commit}" % rev],
                               capture_output=True, env=git_env(), timeout=60)
            if p.returncode:
                raise Refuse("cannot resolve rev %r in %s: %s" % (rev, repo, p.stderr.decode().strip()))
            self.commit = p.stdout.decode().strip()

    def read(self, path):
        if self.repo is None:
            if not os.path.isabs(path):
                raise Refuse("worktree mode requires absolute paths: %r" % path)
            with open(path, "rb") as f:
                return f.read()
        if os.path.isabs(path):
            raise Refuse("git mode requires repo-relative paths: %r" % path)
        p = subprocess.run(["git", "-C", self.repo, "cat-file", "blob", "%s:%s" % (self.commit, path)],
                           capture_output=True, env=git_env(), timeout=60)
        if p.returncode:
            raise FileNotFoundError("%s:%s" % (self.commit, path))
        return p.stdout

    def describe(self):
        if self.repo is None:
            return {"mode": "worktree"}
        return {"mode": "git", "repo": self.repo, "rev": self.rev, "commit": self.commit}


def load_manifest(raw, want_sha):
    got = sha256(raw)
    if got != want_sha:
        raise Refuse("manifest sha256 %s != --manifest-sha256 %s" % (got, want_sha))
    try:
        m = json.loads(raw)
    except ValueError as e:
        raise Refuse("manifest is not JSON: %s" % e)
    if not isinstance(m, dict) or m.get("schema") != MANIFEST_SCHEMA or not isinstance(m.get("rows"), list):
        raise Refuse("manifest must be {schema: %s, rows: [...]}" % MANIFEST_SCHEMA)
    ids, by_sha = set(), {}
    for r in m["rows"]:
        keys = set(r) if isinstance(r, dict) else set()
        if not ROW_KEYS <= keys <= ROW_KEYS | ROW_OPT:
            raise Refuse("row keys must cover %s and may add %s: %r" % (sorted(ROW_KEYS), sorted(ROW_OPT), r))
        if not all(isinstance(r[k], str) and r[k] for k in ROW_KEYS):
            raise Refuse("row %r: id/path/sha256/expected_finding_id must be non-empty strings" % r)
        if "expected_facts" in r and not isinstance(r["expected_facts"], dict):
            raise Refuse("row %r: expected_facts must be an object" % r)
        if r["id"] in ids:
            raise Refuse("duplicate row id %r" % r["id"])
        ids.add(r["id"])
        prev = by_sha.setdefault(r["sha256"].lower(), (r["expected_finding_id"], r.get("expected_facts")))
        if prev != (r["expected_finding_id"], r.get("expected_facts")):
            raise Refuse("conflicting expectations for sha256 %s" % r["sha256"])
    if not m["rows"]:
        raise Refuse("manifest has no rows")
    return m["rows"], got


def _strict_eq(a, b):
    return type(a) is type(b) and a == b


def _walk(val, want, path):
    """want must subset-match val with exact types. Dict expected_facts recurse; dotted keys walk dicts."""
    if isinstance(want, dict):
        if not isinstance(val, dict):
            return ["%s: expected object, got %r" % (path, val)]
        bad = []
        for k, w in want.items():
            if k not in val:
                bad.append("%s.%s: missing" % (path, k))
            else:
                bad += _walk(val[k], w, "%s.%s" % (path, k))
        return bad
    if isinstance(want, list):
        if not isinstance(val, list) or len(val) != len(want):
            return ["%s: expected list of %d elements, got %r" % (path, len(want), val)]
        bad = []
        for i, w in enumerate(want):
            bad += _walk(val[i], w, "%s[%d]" % (path, i))
        return bad
    return [] if _strict_eq(val, want) else ["%s: expected %r (type %s), got %r (type %s)" % (
        path, want, type(want).__name__, val, type(val).__name__)]


def facts_mismatches(output, expected_facts):
    """Compare expected_facts against the classifier output. Dotted path segments walk dict keys."""
    bad = []
    for key, want in expected_facts.items():
        node = output
        ok = True
        for seg in key.split("."):
            if isinstance(node, dict) and seg in node:
                node = node[seg]
            else:
                ok = False
                bad.append("%s: path missing" % key)
                break
        if ok:
            bad += _walk(node, want, key)
    return bad


def _norm_body(body):
    lines = [ln.rstrip() for ln in body.split(b"\n")]
    while lines and not lines[0]:
        lines.pop(0)
    while lines and not lines[-1]:
        lines.pop()
    return b"\n".join(lines) + b"\n" if lines else b""


def _section_bytes(text, heading):
    """Markdown section body from just after `heading` to the next same-or-shallower heading,
    normalized by _norm_body (leading/trailing blank lines and per-line right whitespace removed)."""
    lines = text.split(b"\n")
    depth = start = None
    for i, ln in enumerate(lines):
        if ln.rstrip() == heading.rstrip():
            stripped = ln.lstrip(b"#")
            depth = len(ln) - len(stripped) or 1
            start = i + 1
            break
    if start is None:
        return None
    end = len(lines)
    for j in range(start, len(lines)):
        ln = lines[j]
        stripped = ln.lstrip(b"#")
        lead = len(ln) - len(stripped)
        if lead and lead <= depth and stripped.startswith(b" "):
            end = j
            break
    return _norm_body(b"\n".join(lines[start:end]))




def check_document_spec(raw, want_sha, src):
    got = sha256(raw)
    if want_sha and got != want_sha:
        raise Refuse("document-spec sha256 %s != --document-spec-sha256 %s" % (got, want_sha))
    try:
        spec = json.loads(raw)
    except ValueError as e:
        raise Refuse("document spec is not JSON: %s" % e)
    if not isinstance(spec, dict) or spec.get("schema") != DOC_SPEC_SCHEMA or not isinstance(spec.get("checks"), list):
        raise Refuse("document spec must be {schema: %s, checks: [...]}" % DOC_SPEC_SCHEMA)
    results = []
    for c in spec["checks"]:
        kind = c.get("kind") if isinstance(c, dict) else None
        if kind not in CHECK_KINDS:
            raise Refuse("unsupported document check: %r" % c)
        res = {"kind": kind, "path": c.get("path"), "ok": False, "detail": None}
        results.append(res)
        try:
            data = src.read(c["path"])
        except (OSError, Refuse) as e:
            res["detail"] = "unreadable: %s" % e
            continue
        if kind == "file_exists":
            res["ok"] = True
        elif kind == "file_sha256":
            h = c.get("sha256")
            if not isinstance(h, str) or not h:
                raise Refuse("file_sha256 needs sha256")
            got_h = sha256(data)
            res["ok"] = got_h == h.lower()
            res["detail"] = None if res["ok"] else "file sha256 %s != %s" % (got_h, h)
        elif kind == "file_quote":
            q, line = c.get("quote"), c.get("line")
            if not isinstance(q, str) or not q or not isinstance(line, int) or line < 1:
                raise Refuse("file_quote needs non-empty quote and 1-based line int")
            lines = data.split(b"\n")
            if line > len(lines):
                res["detail"] = "file has %d lines" % len(lines)
            else:
                res["ok"] = q.encode() in lines[line - 1]
                res["detail"] = None if res["ok"] else "quote not on line %d" % line
        elif kind == "file_any_line":
            want = c.get("lines")
            if not isinstance(want, list) or not want or not all(isinstance(x, str) and x for x in want):
                raise Refuse("file_any_line needs non-empty string list")
            present = set(data.split(b"\n"))
            missing = [x for x in want if x.encode() not in present]
            res["ok"] = not missing
            res["detail"] = None if res["ok"] else "missing lines %r" % missing
        else:  # file_section
            heading, tf, tfh = c.get("heading"), c.get("text_file"), c.get("text_file_sha256")
            if not isinstance(heading, str) or not heading or not isinstance(tf, str) or not tf \
                    or not isinstance(tfh, str) or not tfh:
                raise Refuse("file_section needs heading, text_file and text_file_sha256")
            got_body = _section_bytes(data, heading.encode())
            try:
                approved = src.read(tf)
            except (OSError, Refuse) as e:
                res["detail"] = "text_file unreadable: %s" % e
                continue
            if sha256(approved) != tfh.lower():
                res["detail"] = "text_file sha256 mismatch"
                continue
            approved_norm = _norm_body(approved)
            res["ok"] = got_body is not None and got_body == approved_norm
            res["detail"] = None if res["ok"] else ("no such heading" if got_body is None
                                                    else "section bytes differ")
    return {"sha256": got, "docs_ok": all(r["ok"] for r in results), "checks": results}


def _limits():
    resource.setrlimit(resource.RLIMIT_AS, (MEM_CAP, MEM_CAP))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def invoke(classifier_path, fixture_path, timeout):
    work = _tmpdir("w")
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"), "LC_ALL": "C", "PYTHONHASHSEED": "0"}
    try:
        p = subprocess.Popen([sys.executable, "-I", "-B", classifier_path, fixture_path], cwd=work, env=env,
                             stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             start_new_session=True, preexec_fn=_limits)
        try:
            out, err = p.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid, signal.SIGKILL)
            p.communicate()
            return None, None, "classifier_timeout"
        finally:
            try:
                os.killpg(p.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if len(out) > STDOUT_CAP:
        return p.returncode, None, "classifier_output_too_large"
    try:
        obj = json.loads(out)
    except ValueError:
        return p.returncode, None, "classifier_output_invalid"
    if not isinstance(obj, dict) or not isinstance(obj.get("finding_id"), str) or not obj["finding_id"]:
        return p.returncode, None, "classifier_output_invalid"
    return p.returncode, obj, None


def run(classifier, manifest, manifest_sha256, classifier_sha256=None, repo=None, rev=None, timeout=30.0,
        order="random", document_spec=None, document_spec_sha256=None):
    t0 = time.time()
    src = Source(repo, rev)
    try:
        raw_manifest = src.read(manifest)
        cls_bytes = src.read(classifier)
        raw_docs = src.read(document_spec) if document_spec else None
    except OSError as e:
        raise Refuse("cannot read input: %s" % e)
    rows, msha = load_manifest(raw_manifest, manifest_sha256.lower())
    docs = check_document_spec(raw_docs, document_spec_sha256 and document_spec_sha256.lower(), src) \
        if raw_docs is not None else None
    csha = sha256(cls_bytes)
    if classifier_sha256 and csha != classifier_sha256.lower():
        raise Refuse("classifier sha256 %s != --classifier-sha256 %s" % (csha, classifier_sha256))
    results = [None] * len(rows)
    idx = list(range(len(rows)))
    if order == "random":
        random.SystemRandom().shuffle(idx)
    priv = _tmpdir("r33m-")
    try:
        cpath = os.path.join(priv, "c" + secrets.token_hex(12) + ".py")
        with open(cpath, "wb") as f:
            f.write(cls_bytes)
        os.chmod(cpath, 0o444)
        for i in idx:
            r = rows[i]
            res = {"id": r["id"], "sha256": r["sha256"].lower(), "expected_finding_id": r["expected_finding_id"],
                   "observed_finding_id": None, "match": False, "facts_matched": None,
                   "facts_mismatches": None, "classifier_exit": None, "error": None, "output": None}
            results[i] = res
            try:
                b = src.read(r["path"])
            except (OSError, Refuse) as e:
                res["error"] = "fixture_unreadable"
                res["detail"] = str(e)
                continue
            res["bytes"] = len(b)
            if sha256(b) != res["sha256"]:
                res["error"] = "pin_mismatch"
                res["observed_sha256"] = sha256(b)
                continue
            d = os.path.join(priv, secrets.token_hex(8))
            os.mkdir(d)
            fpath = os.path.join(d, secrets.token_hex(16))
            with open(fpath, "wb") as f:
                f.write(b)
            os.chmod(fpath, 0o444)
            os.chmod(d, 0o555)
            code, obj, err = invoke(cpath, fpath, timeout)
            os.chmod(d, 0o755)
            try:
                with open(fpath, "rb") as f:
                    after = f.read()
            except OSError:
                after = None
            res["classifier_exit"] = code
            if after is None or sha256(after) != res["sha256"]:
                res["error"] = "fixture_mutated"
            elif err:
                res["error"] = err
            else:
                res["observed_finding_id"] = obj["finding_id"]
                res["output"] = obj
                res["match"] = obj["finding_id"] == r["expected_finding_id"]
                if "expected_facts" in r:
                    bad = facts_mismatches(obj, r["expected_facts"])
                    res["facts_matched"] = not bad
                    res["facts_mismatches"] = bad or None
            shutil.rmtree(d, ignore_errors=True)
    finally:
        for root, dirs, _ in os.walk(priv):
            for x in dirs:
                os.chmod(os.path.join(root, x), 0o755)
        shutil.rmtree(priv, ignore_errors=True)
    evaluated = [r for r in results if not r["error"]]
    matched = sum(1 for r in evaluated if r["match"])
    facts_failed = sum(1 for r in evaluated if r["facts_matched"] is False)
    errors = sum(1 for r in results if r["error"])
    docs_ok = None if docs is None else docs["docs_ok"]
    all_green = (errors == 0 and matched == len(evaluated) == len(results) and facts_failed == 0
                 and docs_ok is not False)
    code = 0 if all_green else (3 if errors else 1)
    out = {"schema": SCHEMA, "label": LABEL, "definition": DEFINITION, "not_a_semantic_proof": NOT_PROOF,
           "source": src.describe(), "manifest": {"path": manifest, "sha256": msha},
           "classifier": {"path": classifier, "sha256": csha},
           "document_spec": docs, "docs_ok": docs_ok, "order": order, "rows": results,
           "total": len(results), "evaluated": len(evaluated), "matched": matched,
           "mismatched": len(evaluated) - matched, "facts_failed": facts_failed, "errors": errors,
           "receipt": {"all_matched": errors == 0 and matched == len(evaluated) == len(results),
                       "all_facts_matched": facts_failed == 0, "docs_ok": docs_ok, "green": all_green},
           "run": {"utc_start": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t0)),
                   "duration_seconds": round(time.time() - t0, 3)}}
    return code, out


# ---------------------------------------------------------------- selftest (generic stub classifiers)

STUBS = {
    "honest": "import json,sys\nb=open(sys.argv[1],'rb').read()\n"
              "print(json.dumps({'finding_id': b.split(b'\\n',1)[0].split(b'=',1)[1].decode()}))\n",
    "factful": "import json,sys\nb=open(sys.argv[1],'rb').read()\n"
               "f=b.split(b'\\n',1)[0].split(b'=',1)[1].decode()\nn=b.count(b'x')\n"
               "print(json.dumps({'finding_id': f, 'facts': {'count': n, 'kinds': ['A','EC'], "
               "'flag': True, 'depth': {'len': n}}}))\n",
    "filename": "import json,os,sys\nn=os.path.basename(sys.argv[1])\n"
                "print(json.dumps({'finding_id': n.rsplit('.bin',1)[0]}))\n",
    "id_probe": "import json,os,sys\nv=[a for a in sys.argv[2:]]+[os.environ.get(k,'') for k in "
                "('R33_ID','FIXTURE_ID','EXPECTED','ID')]\n"
                "print(json.dumps({'finding_id': next((x for x in v if x), 'unknown')}))\n",
    "constant": "import json\nprint(json.dumps({'finding_id': 'not_candidate.x'}))\n",
    "denial": "import json\nprint(json.dumps({'finding_id': 'not_candidate.no_load_config'}))\n",
    "wordbag": "import hashlib,json,sys\nV=['candidate.structural','not_candidate.x','outside_profile.y',"
               "'malformed.z']\np=hashlib.md5(sys.argv[1].encode()).digest()[0]%4\n"
               "print(json.dumps({'finding_id': V[p]}))\n",
    "mutator": "import json,os,sys\np=sys.argv[1]\n"
               "try:\n os.chmod(os.path.dirname(p),0o755); os.chmod(p,0o644); open(p,'ab').write(b'x')\n"
               "except OSError: pass\nprint(json.dumps({'finding_id': 'candidate.structural'}))\n",
    "crash": "import sys\nsys.exit(1)\n",
}
FIND = ["candidate.structural", "not_candidate.x", "outside_profile.y", "malformed.z"]


def _fixture(fid, salt):
    return ("FINDING=%s\n" % fid).encode() + hashlib.sha256(salt.encode()).digest() * 4


def _write(path, b):
    with open(path, "wb") as f:
        f.write(b)


def _manifest(td, rows, name="m.json"):
    p = os.path.join(td, name)
    raw = json.dumps({"schema": MANIFEST_SCHEMA, "rows": rows}, sort_keys=True).encode()
    _write(p, raw)
    return p, sha256(raw)


def _set(td, tag, salt, names=None, ids=None, facts=None):
    os.makedirs(os.path.join(td, tag), exist_ok=True)
    rows = []
    for k, fid in enumerate(FIND):
        b = _fixture(fid, salt + fid)
        nm = (names[k] if names else fid) + ".bin"
        p = os.path.join(td, tag, nm)
        _write(p, b)
        row = {"id": ids[k] if ids else "row-%d" % k, "path": p, "sha256": sha256(b),
               "expected_finding_id": fid}
        if facts:
            row["expected_facts"] = facts[k]
        rows.append(row)
    return rows


def selftest():
    checks = []

    def check(name, cond, **info):
        checks.append(dict(case=name, ok=bool(cond), **info))

    td = _tmpdir("r33ds-")
    try:
        stub = {}
        for k, src in STUBS.items():
            stub[k] = os.path.join(td, "stub_%s.py" % k)
            _write(stub[k], src.encode())
        a_rows = _set(td, "A", "setA")
        ma, ha = _manifest(td, a_rows, "a.json")

        code, out = run(stub["honest"], ma, ha)
        check("green_honest_content_classifier", code == 0 and out["matched"] == 4 and out["errors"] == 0,
              matched=out["matched"])
        code2, out2 = run(stub["honest"], ma, ha)
        strip = lambda o: [(r["id"], r["observed_finding_id"], r["match"]) for r in o["rows"]]
        check("deterministic_rows", strip(out) == strip(out2))
        code, outm = run(stub["constant"], ma, ha)
        check("evaluated_mismatch_exit_1", code == 1 and outm["evaluated"] == 4 and outm["matched"] == 1,
              matched=outm["matched"])

        code, out = run(stub["filename"], ma, ha)
        check("red_filename_label_shortcut_fails", code == 1 and out["matched"] == 0, matched=out["matched"])
        code, out = run(stub["id_probe"], ma, ha)
        check("red_id_or_expected_probe_fails", code == 1 and out["matched"] == 0
              and all(r["observed_finding_id"] == "unknown" for r in out["rows"]), matched=out["matched"])
        code, out = run(stub["constant"], ma, ha)
        check("all_same_baseline_scores_only_its_class", out["matched"] == 1 and out["matched"] < out["total"],
              matched=out["matched"])
        code, out = run(stub["denial"], ma, ha)
        check("denial_stub_scores_only_denials", out["matched"] == 0 and code == 1, matched=out["matched"])
        code, out = run(stub["wordbag"], ma, ha)
        check("wordbag_stub_below_total", code == 1 and out["matched"] < out["total"],
              matched=out["matched"])

        table = {r["sha256"]: r["expected_finding_id"] for r in a_rows}
        stub["hash"] = os.path.join(td, "stub_hash.py")
        _write(stub["hash"], ("import hashlib,json,sys\nT=%r\nh=hashlib.sha256(open(sys.argv[1],'rb').read())"
                              ".hexdigest()\nprint(json.dumps({'finding_id': T.get(h,'unknown')}))\n" % table).encode())
        code, out = run(stub["hash"], ma, ha)
        check("hash_lookup_passes_seen_bytes_disclosed_limit", out["matched"] == 4 and code == 0,
              matched=out["matched"])
        b_rows = _set(td, "B", "setB-unseen")
        mb, hb = _manifest(td, b_rows, "b.json")
        code, out = run(stub["hash"], mb, hb)
        check("red_hash_lookup_fails_unseen_equivalents", code == 1 and out["matched"] == 0,
              matched=out["matched"])
        code, outb = run(stub["honest"], mb, hb)
        check("green_honest_on_unseen_equivalents", code == 0 and outb["matched"] == 4,
              matched=outb["matched"])

        perm = [2, 3, 0, 1]
        r_rows = _set(td, "R", "setA", names=[FIND[p] for p in perm], ids=["zz-%d" % (9 - k) for k in range(4)])
        mr, hr = _manifest(td, r_rows, "r.json")
        code, outr = run(stub["honest"], mr, hr)
        code0, out0 = run(stub["honest"], ma, ha)
        by_sha = lambda o: sorted((r["sha256"], r["observed_finding_id"], r["match"]) for r in o["rows"])
        check("label_renaming_invariant", code == 0 and by_sha(outr) == by_sha(out0)
              and outr["matched"] == out0["matched"] == 4)
        code, outf = run(stub["filename"], mr, hr)
        check("red_filename_after_renaming_still_fails", outf["matched"] == 0, matched=outf["matched"])

        # expected_facts: strict subset equality on classifier output
        counts = [open(r["path"], "rb").read().count(b"x") for r in a_rows]
        fact_rows = [dict(r, expected_facts={"facts.count": c, "facts.flag": True,
                                             "facts.depth.len": c})
                     for r, c in zip(a_rows, counts)]
        mf, hf = _manifest(td, fact_rows, "facts.json")
        code, out = run(stub["factful"], mf, hf)
        check("green_expected_facts_subset", code == 0 and out["matched"] == 4
              and all(r["facts_matched"] for r in out["rows"]))
        code, out = run(stub["honest"], mf, hf)
        check("red_facts_missing_on_no_reader", code == 1 and out["matched"] == 4
              and not any(r["facts_matched"] for r in out["rows"]))
        typed = [dict(fact_rows[0], expected_facts={"facts.flag": 1})]
        mt, ht = _manifest(td, typed, "typed.json")
        code, out = run(stub["factful"], mt, ht)
        check("red_bool_vs_int_type", code == 1 and out["rows"][0]["facts_matched"] is False)
        wrong = [dict(fact_rows[0], expected_facts={"facts.count": counts[0] + 1})]
        boollist = [dict(fact_rows[0], expected_facts={"facts.kinds": ["A", 1]})]
        ml, hl = _manifest(td, boollist, "boollist.json")
        code, out = run(stub["factful"], ml, hl)
        check("red_bool_inside_facts_list", code == 1 and out["rows"][0]["facts_matched"] is False)

        mw, hw = _manifest(td, wrong, "wrong.json")
        code, out = run(stub["factful"], mw, hw)
        check("red_wrong_fact_value", code == 1 and out["rows"][0]["facts_matched"] is False)

        bad = [dict(r) for r in a_rows]
        bad[1]["sha256"] = "0" * 64
        mp, hp = _manifest(td, bad, "pin.json")
        code, out = run(stub["honest"], mp, hp)
        check("pin_mismatch_is_error_exit_3", code == 3 and out["rows"][1]["error"] == "pin_mismatch"
              and out["matched"] == 3, matched=out["matched"])

        try:
            run(stub["honest"], ma, "f" * 64)
            check("manifest_digest_mismatch_refused", False)
        except Refuse:
            check("manifest_digest_mismatch_refused", True)
        try:
            run(stub["honest"], ma, ha, classifier_sha256="e" * 64)
            check("classifier_digest_mismatch_refused", False)
        except Refuse:
            check("classifier_digest_mismatch_refused", True)
        conflict = [dict(a_rows[0]), dict(a_rows[0], id="dup-sha", expected_finding_id="malformed.z")]
        mc, hc = _manifest(td, conflict, "conflict.json")
        try:
            run(stub["honest"], mc, hc)
            check("conflicting_expected_ids_refused", False)
        except Refuse:
            check("conflicting_expected_ids_refused", True)
        dup = [dict(a_rows[0]), dict(a_rows[1], id=a_rows[0]["id"])]
        md, hd = _manifest(td, dup, "dup.json")
        try:
            run(stub["honest"], md, hd)
            check("duplicate_row_id_refused", False)
        except Refuse:
            check("duplicate_row_id_refused", True)
        extra = [dict(a_rows[0], hint="candidate.structural")]
        me, he = _manifest(td, extra, "extra.json")
        try:
            run(stub["honest"], me, he)
            check("extra_row_key_refused", False)
        except Refuse:
            check("extra_row_key_refused", True)

        code, out = run(stub["mutator"], ma, ha)
        check("fixture_mutation_detected", code == 3 and all(r["error"] == "fixture_mutated" for r in out["rows"]))
        code, out = run(stub["crash"], ma, ha)
        check("classifier_crash_is_error", code == 3 and all(r["error"] == "classifier_output_invalid"
                                                             for r in out["rows"]))

        # document spec: sha-pinned file, line-pinned quote, byte-exact section text with pinned text_file
        docs = os.path.join(td, "docs")
        os.makedirs(docs)
        skill = (b"# Lane\n\n## PE ARM64X structural profile\n\nThis is the approved section body.\n"
                 b"It has two lines.\n\n## Next\nrest.\n")
        _write(os.path.join(docs, "SKILL.md"), skill)
        approved = b"This is the approved section body.\nIt has two lines.\n"
        _write(os.path.join(docs, "approved.txt"), approved)
        _write(os.path.join(docs, "SOURCES.md"), b"| S101 | Arm64X | u |\n")
        spec = {"schema": DOC_SPEC_SCHEMA,
                "checks": [{"kind": "file_sha256", "path": os.path.join(docs, "SKILL.md"),
                            "sha256": sha256(skill)},
                           {"kind": "file_quote", "path": os.path.join(docs, "SKILL.md"),
                            "line": 5, "quote": "This is the approved section body."},
                           {"kind": "file_section", "path": os.path.join(docs, "SKILL.md"),
                            "heading": "## PE ARM64X structural profile",
                            "text_file": os.path.join(docs, "approved.txt"),
                            "text_file_sha256": sha256(approved)},
                           {"kind": "file_any_line", "path": os.path.join(docs, "SOURCES.md"),
                            "lines": ["| S101 | Arm64X | u |"]}]}
        sp = os.path.join(td, "spec.json")
        sraw = json.dumps(spec, sort_keys=True).encode()
        _write(sp, sraw)
        code, out = run(stub["honest"], ma, ha, document_spec=sp, document_spec_sha256=sha256(sraw))
        check("green_docspec_docs_ok", code == 0 and out["docs_ok"] is True and out["receipt"]["green"])
        blank_approved = b"\n" + approved + b"\n"
        _write(os.path.join(docs, "approved.txt"), blank_approved)
        blank_checks = [dict(c, text_file_sha256=sha256(blank_approved))
                        if c["kind"] == "file_section" else c for c in spec["checks"]]
        blank_raw = json.dumps(dict(spec, checks=blank_checks), sort_keys=True).encode()
        blank_path = os.path.join(td, "spec-blank-margins.json")
        _write(blank_path, blank_raw)
        code, out = run(stub["honest"], ma, ha, document_spec=blank_path,
                        document_spec_sha256=sha256(blank_raw))
        check("green_docspec_blank_margins", code == 0 and out["docs_ok"] is True)
        _write(os.path.join(docs, "approved.txt"), approved)
        fab = skill.replace(b"approved section body", b"denied section body")
        _write(os.path.join(docs, "SKILL.md"), fab)
        code, out = run(stub["honest"], ma, ha, document_spec=sp, document_spec_sha256=sha256(sraw))
        check("red_denial_bag_docs_fail", code == 1 and out["docs_ok"] is False
              and not out["receipt"]["green"])
        _write(os.path.join(docs, "SKILL.md"), skill)
        # quote on the wrong line fails even though the phrase exists in the file
        spec2 = dict(spec, checks=[{"kind": "file_quote", "path": os.path.join(docs, "SKILL.md"),
                                    "line": 3, "quote": "This is the approved section body."}])
        sp2 = os.path.join(td, "spec2.json")
        sraw2 = json.dumps(spec2, sort_keys=True).encode()
        _write(sp2, sraw2)
        code, out = run(stub["honest"], ma, ha, document_spec=sp2, document_spec_sha256=sha256(sraw2))
        check("red_quote_wrong_line", code == 1 and out["docs_ok"] is False)
        spec3 = dict(spec, checks=[{"kind": "file_sha256", "path": os.path.join(docs, "SKILL.md"),
                                    "sha256": "0" * 64}])
        sp3 = os.path.join(td, "spec3.json")
        sraw3 = json.dumps(spec3, sort_keys=True).encode()
        _write(sp3, sraw3)
        code, out = run(stub["honest"], ma, ha, document_spec=sp3, document_spec_sha256=sha256(sraw3))
        check("red_file_sha256_fabricated", code == 1 and out["docs_ok"] is False)

        p = subprocess.run([sys.executable, "-I", "-B", os.path.abspath(__file__), "--classifier", stub["honest"],
                            "--manifest", ma, "--manifest-sha256", "f" * 64], capture_output=True, timeout=60)
        check("cli_refusal_exit_2", p.returncode == 2, exit=p.returncode)
        p = subprocess.run([sys.executable, "-I", "-B", os.path.abspath(__file__), "--classifier", stub["honest"],
                            "--manifest", ma, "--manifest-sha256", ha], capture_output=True, timeout=60)
        check("cli_green_exit_0", p.returncode == 0 and json.loads(p.stdout)["matched"] == 4, exit=p.returncode)

        if shutil.which("git"):
            repo = os.path.join(td, "repo")
            os.makedirs(os.path.join(repo, "fx"))
            g = lambda *a: subprocess.run(["git", "-C", repo, "-c", "user.name=selftest", "-c",
                                           "user.email=selftest@invalid", "-c", "commit.gpgsign=false"] + list(a),
                                          capture_output=True, env=git_env(), timeout=60, check=True)
            g("init", "-q")
            rel_rows = []
            for k, fid in enumerate(FIND):
                b = _fixture(fid, "git" + fid)
                _write(os.path.join(repo, "fx", "%02d.bin" % k), b)
                rel_rows.append({"id": "g%d" % k, "path": "fx/%02d.bin" % k, "sha256": sha256(b),
                                 "expected_finding_id": fid})
            raw = json.dumps({"schema": MANIFEST_SCHEMA, "rows": rel_rows}, sort_keys=True).encode()
            _write(os.path.join(repo, "manifest.json"), raw)
            shutil.copy(stub["honest"], os.path.join(repo, "cls.py"))
            g("add", "-A")
            g("commit", "-q", "-m", "pinned")
            _write(os.path.join(repo, "fx", "00.bin"), _fixture(FIND[0], "tampered"))
            _write(os.path.join(repo, "cls.py"), STUBS["constant"].encode())
            code, outg = run("cls.py", "manifest.json", sha256(raw), repo=repo, rev="HEAD")
            check("git_rev_reads_committed_bytes", code == 0 and outg["matched"] == 4
                  and outg["classifier"]["sha256"] == sha256(STUBS["honest"].encode()), matched=outg["matched"])
            wt = [dict(r, path=os.path.join(repo, r["path"])) for r in rel_rows]
            mw, hw = _manifest(td, wt, "wt.json")
            code, outw = run(stub["honest"], mw, hw)
            check("worktree_tamper_is_pin_mismatch", code == 3 and outw["rows"][0]["error"] == "pin_mismatch")
            try:
                run("cls.py", "manifest.json", sha256(raw), repo=repo, rev="no-such-rev")
                check("git_bad_rev_refused", False)
            except Refuse:
                check("git_bad_rev_refused", True)
        else:
            check("git_available", False)
    finally:
        for root, dirs, _ in os.walk(td):
            for x in dirs:
                os.chmod(os.path.join(root, x), 0o755)
        shutil.rmtree(td, ignore_errors=True)
    ok = all(c["ok"] for c in checks)
    print(json.dumps({"selftest": "measure_driver", "pass": ok, "checks": checks}, indent=1))
    return 0 if ok else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--classifier", required=True)
    ap.add_argument("--manifest", required=True)
    ap.add_argument("--manifest-sha256", required=True)
    ap.add_argument("--classifier-sha256")
    ap.add_argument("--document-spec")
    ap.add_argument("--document-spec-sha256")
    ap.add_argument("--repo")
    ap.add_argument("--rev")
    ap.add_argument("--timeout", type=float, default=30.0)
    ap.add_argument("--order", choices=("random", "manifest"), default="random")
    try:
        a = ap.parse_args(argv)
    except SystemExit:
        return 2
    if (a.repo is None) != (a.rev is None):
        sys.stderr.write("--repo and --rev go together\n")
        return 2
    try:
        code, out = run(a.classifier, a.manifest, a.manifest_sha256, a.classifier_sha256, a.repo, a.rev,
                        a.timeout, a.order, a.document_spec, a.document_spec_sha256)
    except Refuse as e:
        print(json.dumps({"schema": SCHEMA, "refused": str(e)}))
        return 2
    print(json.dumps(out, sort_keys=True))
    return code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
