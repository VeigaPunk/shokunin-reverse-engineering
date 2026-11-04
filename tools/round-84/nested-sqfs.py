#!/usr/bin/env python3
"""Round-84 nested SquashFS container-chain counter (frontier edge class).

Measures one edge class the lane's PROVINCE lists as Frontier — nested sub-images below
depth 1 — on a lane-built, reproducible three-level chain of standard little-endian
SquashFS v4 images (mksquashfs 4.7.5, gzip, `-repro-time` for image identity), through
REA 6.5.0 `extract-firmware` (unblob 26.6.4 provider).

Measured surface (one value per arm, re-derivable by this command):
  A1  --max-depth 3 publishes exactly the oracle member set (8/8 paths)
  A2  every published file's sha256 equals the oracle's bytes
  A3  --max-depth 3 reports coverage "partial" and exactly one depth-limited path, the
      deepest extract root
  A4  at --max-depth 3 the deepest level's files carry analysis_depth null (published,
      not analyzed) while levels 1-2 carry their own depth
  A5  --max-depth 4 publishes exactly the same oracle member set (8/8 paths)
  A6  every published file's sha256 equals the oracle's bytes
  A7  --max-depth 4 reports coverage "complete", no depth-limited path and no gap
  A8  the deepest level's files carry analysis_depth 3
  A9  engine identity is equal across the two runs (unblob id/version/executable sha256)
control  the cheap rule "published file count equals the oracle count, therefore complete"
         labels the depth-3 run complete although REA reports partial: the counter's target
         is failable, not satisfied by the file list alone.

Exit: 0 when every arm holds and the control fires; 1 otherwise; 2 when the toolchain or an
envelope cannot be read. `--selftest` exercises the scorer on synthetic envelopes only.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCHEMA = "kaidoku-r84-nested-sqfs-v1"
REA_PIN = "6.5.0"
REPRO_TIME = "1760000000"
DEEPEST_ROOT = "inner-b.sqfs_extract/inner-c.sqfs_extract"
EXPECTED_LEVEL = {}


def sha256_bytes(body: bytes) -> str:
    return hashlib.sha256(body).hexdigest()


def sha256_file(path: str) -> str:
    return sha256_bytes(Path(path).read_bytes())


def run(argv: list[str], cwd: str | None = None, env: dict | None = None,
        timeout: int = 300) -> dict:
    try:
        done = subprocess.run(argv, cwd=cwd, env=env, capture_output=True,
                              text=True, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"argv": argv, "exit": 127, "stdout": "", "stderr": str(error)}
    return {"argv": argv, "exit": done.returncode, "stdout": done.stdout,
            "stderr": done.stderr}


def mksquashfs(src: str, image: str) -> None:
    result = run(["mksquashfs", src, image, "-noappend", "-comp", "gzip", "-b", "4096",
                  "-quiet", "-repro-time", REPRO_TIME])
    if result["exit"] != 0:
        raise RuntimeError(f"mksquashfs failed: {result['stderr'][-400:]}")


def unsquash_oracle(image: str, dest: str) -> dict:
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    result = run(["unsquashfs", "-d", dest, image])
    if result["exit"] != 0:
        raise RuntimeError(f"unsquashfs failed: {result['stderr'][-400:]}")
    members: dict[str, str] = {}
    for current, _dirs, files in os.walk(dest):
        for name in files:
            path = os.path.join(current, name)
            if os.path.islink(path) or not os.path.isfile(path):
                continue
            members[os.path.relpath(path, dest)] = sha256_file(path)
    return members


def build_chain(work: str) -> dict:
    build = os.path.join(work, "build")
    leaf, mid, outer = (os.path.join(build, name) for name in ("leaf", "mid", "outer"))
    for directory in (leaf, mid, outer):
        os.makedirs(directory)
    Path(leaf, "alpha.txt").write_text("leaf-alpha\n")
    Path(leaf, "beta.txt").write_text("leaf-beta\n")
    Path(leaf, "gamma.bin").write_text("".join(f"row-{n:03d}\n" for n in range(200)))
    images = {"c": os.path.join(work, "c.sqfs"), "b": os.path.join(work, "b.sqfs"),
              "a": os.path.join(work, "a.sqfs")}
    mksquashfs(leaf, images["c"])
    shutil.copyfile(images["c"], os.path.join(mid, "inner-c.sqfs"))
    Path(mid, "one.txt").write_text("mid-one\n")
    Path(mid, "two.txt").write_text("mid-two\n")
    mksquashfs(mid, images["b"])
    shutil.copyfile(images["b"], os.path.join(outer, "inner-b.sqfs"))
    Path(outer, "x.txt").write_text("outer-x\n")
    mksquashfs(outer, images["a"])
    oracle = {
        "a": unsquash_oracle(images["a"], os.path.join(work, "oracle", "a")),
        "b": unsquash_oracle(images["b"], os.path.join(work, "oracle", "b")),
        "c": unsquash_oracle(images["c"], os.path.join(work, "oracle", "c")),
    }
    pins = {name: sha256_file(path) for name, path in images.items()}
    return {"images": images, "oracle": oracle, "pins": pins, "build": build}


def expected_map(chain: dict) -> dict:
    """Expected published path -> (sha256, level), from the independent unsquashfs oracle."""
    expected: dict[str, tuple[str, int]] = {}
    for name, digest in chain["oracle"]["a"].items():
        expected[name] = (digest, 1)
    for name, digest in chain["oracle"]["b"].items():
        expected[f"inner-b.sqfs_extract/{name}"] = (digest, 2)
    for name, digest in chain["oracle"]["c"].items():
        expected[f"{DEEPEST_ROOT}/{name}"] = (digest, 3)
    return expected


def rea_extract(image: str, outdir: str, depth: int, env: dict) -> dict:
    argv = ["npx", "-y", f"rea-agents@{REA_PIN}", "extract-firmware", image, outdir,
            "--max-depth", str(depth), "--format", "json"]
    return run(argv, env=env, timeout=600)


def envelope(result: dict) -> dict | None:
    text = result.get("stdout") or ""
    start = text.find("{")
    if start < 0:
        return None
    try:
        value, _end = json.JSONDecoder().raw_decode(text[start:])
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def strip_root(paths: list[str]) -> tuple[list[str], str | None]:
    """Strip the single shared `<name>_extract/` root the provider prepends."""
    if not paths:
        return [], None
    first = paths[0].split("/", 1)
    if len(first) == 2 and first[0].endswith("_extract") and all(
            p.startswith(first[0] + "/") for p in paths):
        return [p.split("/", 1)[1] for p in paths], first[0]
    return paths, None


def score_envelope(env: dict | None, expected: dict, depth: int) -> dict:
    """Score one envelope. `expected` maps path -> (sha256, level)."""
    arms: dict[str, bool] = {}
    observed: dict = {"depth": depth}
    if env is None:
        return {"depth": depth, "arms": {"envelope-readable": False},
                "observed": observed}
    if "code" in env and "normalized_result" not in env:
        observed.update({"error": env.get("message"), "code": env.get("code")})
        return {"depth": depth, "arms": {"envelope-readable": True,
                                         "no-error-envelope": False},
                "observed": observed}
    norm = env.get("normalized_result") or {}
    files = norm.get("files") or []
    paths = [f.get("relative_path") for f in files if isinstance(f, dict)]
    stripped, root = strip_root(paths)
    by_path = {rel: f for rel, f in zip(stripped, files)}
    observed.update({"files": len(files), "root": root,
                     "coverage": norm.get("coverage"),
                     "depth_limited_paths": norm.get("depth_limited_paths"),
                     "extraction_gaps": norm.get("extraction_gaps"),
                     "published_bytes": norm.get("published_bytes"),
                     "engine": norm.get("engine")})
    expected_paths = set(expected)
    arms["path-set-equal"] = set(stripped) == expected_paths
    arms["bytes-equal"] = all(
        by_path[p].get("sha256") == expected[p][0] for p in expected_paths & set(stripped)
    ) and expected_paths <= set(stripped)
    arms["coverage-partial"] = norm.get("coverage") == "partial"
    arms["coverage-complete"] = norm.get("coverage") == "complete"
    gaps = norm.get("extraction_gaps") or []
    arms["single-depth-gap"] = (len(gaps) == 1
                                and gaps[0].get("kind") == "depth-limited"
                                and str(gaps[0].get("input_path", "")).endswith(DEEPEST_ROOT))
    arms["no-gap"] = gaps == []
    limited = norm.get("depth_limited_paths") or []
    arms["depth-limited-paths"] = (len(limited) == 1
                                   and str(limited[0]).endswith(DEEPEST_ROOT))
    arms["no-depth-limited-paths"] = limited == []
    analyzed = {p: by_path[p].get("analysis_depth") for p in expected_paths if p in by_path}
    arms["analyzed-through-budget"] = all(
        analyzed[p] == expected[p][1] for p in analyzed if expected[p][1] <= depth - 1)
    arms["deepest-unanalyzed"] = all(
        analyzed[p] is None for p in analyzed if expected[p][1] == depth)
    arms["deepest-analyzed"] = all(
        analyzed[p] == expected[p][1] for p in analyzed if expected[p][1] == depth)
    observed["analysis_depth"] = analyzed
    return {"depth": depth, "arms": arms, "observed": observed}


def score(chain: dict, expected: dict, runs: dict, rea_version: dict) -> dict:
    depth3 = score_envelope(runs["3"]["envelope"], expected, 3)
    depth4 = score_envelope(runs["4"]["envelope"], expected, 4)
    arms = {
        "A1-depth3-paths": depth3["arms"].get("path-set-equal", False),
        "A2-depth3-bytes": depth3["arms"].get("bytes-equal", False),
        "A3-depth3-partial": depth3["arms"].get("coverage-partial", False)
        and depth3["arms"].get("depth-limited-paths", False)
        and depth3["arms"].get("single-depth-gap", False),
        "A4-depth3-deepest-unanalyzed": depth3["arms"].get("deepest-unanalyzed", False)
        and depth3["arms"].get("analyzed-through-budget", False),
        "A5-depth4-paths": depth4["arms"].get("path-set-equal", False),
        "A6-depth4-bytes": depth4["arms"].get("bytes-equal", False),
        "A7-depth4-complete": depth4["arms"].get("coverage-complete", False)
        and depth4["arms"].get("no-gap", False)
        and depth4["arms"].get("no-depth-limited-paths", False),
        "A8-depth4-deepest-analyzed": depth4["arms"].get("deepest-analyzed", False)
        and depth4["arms"].get("analyzed-through-budget", False),
    }
    engines = [depth3["observed"].get("engine"), depth4["observed"].get("engine")]
    arms["A9-engine-identity-equal"] = bool(
        engines[0] and engines[1]
        and engines[0].get("executable_sha256") == engines[1].get("executable_sha256")
        and engines[0].get("version") == engines[1].get("version") == "26.6.4"
        and engines[0].get("name") == "unblob" and rea_version.get("stdout", "").strip()
        == REA_PIN)
    control = {
        "rule": "published-file-count-equals-oracle-count-therefore-complete",
        "fires": depth3["observed"].get("files") == len(expected)
        and depth3["observed"].get("coverage") != "complete",
        "detail": "the depth-3 run publishes all eight members yet REA reports partial; a "
                  "file-count-only reading calls it complete",
    }
    return {"schema": SCHEMA, "expected": {p: v[0] for p, v in expected.items()},
            "expected_levels": {p: v[1] for p, v in expected.items()},
            "fixture_pins": chain["pins"], "depths": {"3": depth3, "4": depth4},
            "arms": arms, "control": control,
            "met": all(arms.values()) and control["fires"]}


# --------------------------------------------------------------------------
# selftest: synthetic envelopes; no REA run, no fixture build
# --------------------------------------------------------------------------

def synthetic_envelope(expected: dict, depth: int, coverage: str,
                       limited: list[str], analyzed_depth: int | None,
                       override_sha: str | None = None) -> dict:
    files = []
    for path, (digest, level) in sorted(expected.items()):
        files.append({"relative_path": f"firmware.bin_extract/{path}",
                      "sha256": override_sha if (override_sha and level == 3) else digest,
                      "analysis_depth": (analyzed_depth if level == depth
                                          else level)})
    gaps = []
    if limited:
        gaps = [{"kind": "depth-limited",
                 "input_path": f"$output/firmware.bin_extract/{limited[0]}"}]
    return {"provider": {"id": "unblob", "name": "Unblob", "version": "26.6.4"},
            "normalized_result": {"coverage": coverage, "files": files,
                                  "depth_limited_paths": [f"$output/firmware.bin_extract/{p}"
                                                          for p in limited],
                                  "extraction_gaps": gaps,
                                  "published_bytes": 100,
                                  "engine": {"name": "unblob", "version": "26.6.4",
                                             "executable_sha256": "a" * 64}}}


def selftest(json_out: str | None) -> int:
    expected = {"x.txt": ("1" * 64, 1), "inner-b.sqfs": ("2" * 64, 1),
                "inner-b.sqfs_extract/one.txt": ("3" * 64, 2),
                "inner-b.sqfs_extract/inner-c.sqfs": ("4" * 64, 2),
                f"{DEEPEST_ROOT}/alpha.txt": ("5" * 64, 3)}
    cases: dict[str, bool] = {}

    def check(name: str, cond: bool) -> None:
        cases[name] = bool(cond)

    partial = score_envelope(
        synthetic_envelope(expected, 3, "partial", [DEEPEST_ROOT], None), expected, 3)
    complete = score_envelope(
        synthetic_envelope(expected, 4, "complete", [], 3), expected, 4)
    wrong_root = score_envelope(
        synthetic_envelope(expected, 3, "partial", ["inner-b.sqfs_extract"], None),
        expected, 3)
    bad_bytes = score_envelope(
        synthetic_envelope(expected, 4, "complete", [], 3, override_sha="9" * 64),
        expected, 4)
    error = score_envelope({"code": "invalid_request", "message": "no"}, expected, 3)

    check("partial-clean", partial["arms"]["path-set-equal"]
          and partial["arms"]["bytes-equal"] and partial["arms"]["coverage-partial"]
          and partial["arms"]["single-depth-gap"] and partial["arms"]["deepest-unanalyzed"])
    check("complete-clean", complete["arms"]["path-set-equal"]
          and complete["arms"]["bytes-equal"] and complete["arms"]["coverage-complete"]
          and complete["arms"]["no-gap"] and complete["arms"]["deepest-analyzed"])
    check("wrong-root-fails", wrong_root["arms"]["single-depth-gap"] is False)
    check("bad-bytes-fails", bad_bytes["arms"]["bytes-equal"] is False)
    check("error-envelope-fails", error["arms"]["envelope-readable"] and not error["arms"].get("no-error-envelope", True))
    control = {"fires": partial["observed"]["files"] == len(expected)
               and partial["observed"]["coverage"] != "complete"}
    check("junk-control-fires", control["fires"] is True)
    check("strip-root", strip_root(["firmware.bin_extract/x", "firmware.bin_extract/y"])
          == (["x", "y"], "firmware.bin_extract"))

    failures = sorted(name for name, ok in cases.items() if not ok)
    summary = {"schema": SCHEMA + "-selftest", "cases": len(cases),
               "case_names": sorted(cases), "failures": failures, "control": control}
    text = json.dumps(summary, indent=1, sort_keys=True)
    if json_out:
        Path(json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(json_out).write_text(text + "\n")
    print(text)
    print(f"SELFTEST cases={len(cases)} failures={len(failures)}")
    return 0 if not failures else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--rev")
    ap.add_argument("--work")
    ap.add_argument("--artifact-work", help="kept after the run (default: removed)")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json-out")
    args = ap.parse_args()
    if args.selftest:
        return selftest(args.json_out)
    if not args.work:
        ap.error("--work is required")

    work = os.path.abspath(args.work)
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(work, "tmp")
    os.makedirs(env["TMPDIR"], exist_ok=True)
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    toolchain = {
        "mksquashfs": run(["mksquashfs", "-version"])["stdout"].splitlines()[0]
        if run(["mksquashfs", "-version"])["stdout"] else None,
        "unsquashfs": run(["unsquashfs", "-version"])["stdout"].splitlines()[0]
        if run(["unsquashfs", "-version"])["stdout"] else None,
        "rea_version": run(["npx", "-y", f"rea-agents@{REA_PIN}", "--version"], env=env),
        "python": sys.version.split()[0],
    }
    receipt: dict = {"schema": SCHEMA, "rev": args.rev,
                     "instrument": {"path": "tools/round-84/nested-sqfs.py",
                                    "sha256": sha256_file(__file__)},
                     "toolchain": {k: (v.get("stdout", "").strip() if isinstance(v, dict) else v)
                                   for k, v in toolchain.items()}}
    try:
        chain = build_chain(work)
        expected = expected_map(chain)
        receipt["chain"] = {"images": {k: os.path.basename(v)
                                       for k, v in chain["images"].items()},
                            "pins": chain["pins"],
                            "oracle_counts": {k: len(v) for k, v in chain["oracle"].items()},
                            "nested_identity": {
                                "b_is_oracle_member": chain["oracle"]["a"].get("inner-b.sqfs")
                                == chain["pins"]["b"],
                                "c_is_oracle_member": chain["oracle"]["b"].get("inner-c.sqfs")
                                == chain["pins"]["c"]}}
        runs = {}
        for depth in (3, 4):
            outdir = os.path.join(work, f"out-depth{depth}")
            result = rea_extract(chain["images"]["a"], outdir, depth, env)
            runs[str(depth)] = {"exit": result["exit"],
                                "stderr": result["stderr"][-2000:],
                                "envelope": envelope(result)}
        receipt.update(score(chain, expected, runs, toolchain["rea_version"]))
        receipt["runs"] = {depth: {"exit": r["exit"], "stderr": r["stderr"]}
                           for depth, r in runs.items()}
    except Exception as error:  # noqa: BLE001 - the receipt records the failure
        receipt.update({"unevaluable": f"{type(error).__name__}: {error}", "met": False})
    finally:
        if not args.artifact_work:
            shutil.rmtree(work, ignore_errors=True)
    text = json.dumps(receipt, indent=1, sort_keys=True)
    if args.json_out:
        Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
        Path(args.json_out).write_text(text + "\n")
    print(json.dumps({"arms": receipt.get("arms"), "control": receipt.get("control"),
                      "met": receipt.get("met"), "unevaluable": receipt.get("unevaluable")},
                     sort_keys=True))
    return 0 if receipt.get("met") else 1


if __name__ == "__main__":
    sys.exit(main())
