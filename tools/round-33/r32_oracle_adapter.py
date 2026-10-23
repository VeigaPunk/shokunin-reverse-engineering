#!/usr/bin/env python3
"""R33 baseline adapter around the frozen r32 oracle (scratch only; the oracle file is read, never edited).

  r32_oracle_adapter.py <path>      one JSON object {finding_id, ...facts}; exit 0
  r32_oracle_adapter.py --selftest  synthetic fixtures from chpe_profile's builder

finding_id: 'candidate' when r32 classify(path)["arm64x"] is true, 'not_candidate' when false,
'malformed' when classify raises. The oracle bytes must match ORACLE_SHA256 or the adapter refuses (exit 2).
They are executed from the verified bytes, so no bytecode is written and a later worktree edit cannot
change what runs.
"""

import hashlib
import json
import os
import subprocess
import sys
import shutil
import types

ORACLE_PATH = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-32/arm64x_oracle.py"
ORACLE_SHA256 = "17eea1f9768ec73e4e66712e7cf4221de83a1052cda40c5801d1e64a80936686"
SCHEMA = "r32-oracle-adapter/1"


def load_oracle():
    with open(ORACLE_PATH, "rb") as f:
        src = f.read()
    digest = hashlib.sha256(src).hexdigest()
    if digest != ORACLE_SHA256:
        raise RuntimeError("oracle sha256 %s != pinned %s" % (digest, ORACLE_SHA256))
    mod = types.ModuleType("r32_arm64x_oracle_pinned")
    mod.__file__ = ORACLE_PATH
    exec(compile(src, ORACLE_PATH, "exec"), mod.__dict__)
    return mod


def adapt(oracle, path):
    with open(path, "rb") as f:
        sha = hashlib.sha256(f.read()).hexdigest()
    try:
        c = oracle.classify(path)
    except Exception as e:  # the baseline's own failure is the old generic 'malformed'
        return {"schema": SCHEMA, "finding_id": "malformed", "oracle_sha256": ORACLE_SHA256,
                "facts": {"exception": "%s: %s" % (type(e).__name__, e)}, "input": {"sha256": sha}}
    pe = oracle.load(path)
    facts = {"machine": c["machine"], "metadata": {"code_map_count": len(c["code_map"]),
                                                   "code_map": c["code_map"]}}
    try:
        facts["ranges"] = [{"kind": r["type"], "rva": r["start"], "length": r["length"],
                            "section": next((s["name"] for s in pe.sections
                                             if s["va"] <= r["start"] < s["va"] + max(s["vsize"], s["rsize"])), None),
                            "file_offset": next((s["rptr"] + r["start"] - s["va"] for s in pe.sections
                                                 if s["va"] <= r["start"] < s["va"] + max(s["vsize"], s["rsize"])), None)}
                           for r in c["code_map"]]
    except Exception:
        facts.setdefault("ranges_error", "projection failed")
    return {"schema": SCHEMA, "finding_id": "candidate.structural" if c["arm64x"] else "not_candidate",
            "oracle_sha256": ORACLE_SHA256, "input": {"sha256": sha}, "facts": facts}


def selftest():
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import selftest_pegen as gp  # fixture recipe lives outside the parser by design
    import measure_driver as md
    L = gp.LAYOUTS[0]
    built = {c[0]: c[1] for c in gp.CASES}
    extra = gp.canonical(L)
    extra.set_map(gp.default_map(L) + [((L["hexp"] + 0x8) | 3, 4)])
    cases = [
        ("green_canonical", gp.canonical(L).build(), "candidate.structural"),
        ("pure_arm64_no_load_config", gp.canonical(L, chpe=False).build(), "not_candidate"),
        # r32 code_map() resolves CodeMap RVA 0 before reading the count, so zeroed metadata raises
        ("zeroed_metadata", built["zeroed_metadata"](L), "malformed"),
        ("ec_replaced_by_tag3", built["tag3"](L), "not_candidate"),
        ("garbage", b"\0" * 64, "malformed"),
        # baseline gaps the new profile closes: the r32 oracle still says candidate here
        ("range_overlap_forgery", built["range_overlap_forgery"](L), "candidate.structural"),
        ("extra_tag3_entry", extra.build(), "candidate.structural"),
        ("range_not_executable", built["range_not_executable"](L), "candidate.structural"),
        ("range_unmapped", built["range_unmapped"](L), "candidate.structural"),
        ("range_zero_tail", built["range_zero_tail"](L), "candidate.structural"),
    ]
    results, ok = [], True
    td = md._tmpdir("r33ad-")
    try:
        for name, b, want in cases:
            p = os.path.join(td, os.urandom(8).hex())
            with open(p, "wb") as f:
                f.write(b)
            r = subprocess.run([sys.executable, "-I", "-B", os.path.abspath(__file__), p], capture_output=True,
                               timeout=30)
            got = json.loads(r.stdout)["finding_id"]
            good = got == want and r.returncode == 0
            ok &= good
            results.append({"case": name, "want": want, "got": got, "exit": r.returncode, "pass": good})
        # common-fact projection matches the counter if expected_facts choose common decoded fields
        pos = gp.canonical(L).build()
        pp = os.path.join(td, os.urandom(8).hex())
        with open(pp, "wb") as f:
            f.write(pos)
        o = json.loads(subprocess.run([sys.executable, "-I", "-B", os.path.abspath(__file__), pp],
                                       capture_output=True, timeout=30).stdout)
        rows = [{"id": "pos", "path": pp, "sha256": hashlib.sha256(pos).hexdigest(),
                 "expected_finding_id": "candidate.structural",
                 "expected_facts": {"facts.machine": "0xaa64",
                                    "facts.metadata.code_map_count": 3,
                                    "facts.ranges": [{"kind": "ARM64", "rva": 4096, "length": 16,
                                                      "section": ".text"},
                                                     {"kind": "ARM64EC", "rva": 4352, "length": 24,
                                                      "section": ".text"},
                                                     {"kind": "AMD64", "rva": 8192, "length": 6,
                                                      "section": ".hexpthk"}]}}]
        mp = os.path.join(td, "manifest.json")
        mraw = json.dumps({"schema": md.MANIFEST_SCHEMA, "rows": rows}, sort_keys=True).encode()
        with open(mp, "wb") as f:
            f.write(mraw)
        code, out = md.run(os.path.abspath(__file__), mp, md.sha256(mraw))
        common_ok = code == 0 and out["matched"] == 1 and out["receipt"]["green"]
        ok &= common_ok
        results.append({"case": "common_positive_facts_match_counter", "pass": common_ok,
                        "exit": code, "matched": out["matched"]})
    finally:
        for root, dirs, _ in os.walk(td):
            for x in dirs:
                os.chmod(os.path.join(root, x), 0o755)
        shutil.rmtree(td, ignore_errors=True)
    print(json.dumps({"selftest": "r32_oracle_adapter", "pass": bool(ok), "results": results}, indent=1))
    return 0 if ok else 1


def main(argv):
    if argv == ["--selftest"]:
        return selftest()
    if len(argv) != 1 or argv[0].startswith("--"):
        sys.stderr.write("usage: r32_oracle_adapter.py <path> | --selftest\n")
        return 2
    try:
        oracle = load_oracle()
    except (OSError, RuntimeError) as e:
        print(json.dumps({"schema": SCHEMA, "finding_id": "error.oracle_pin", "reasons": [str(e)]}))
        return 2
    print(json.dumps(adapt(oracle, argv[0]), sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
