#!/usr/bin/env python3
"""Independent R84-C3 reproduction: nested LE SquashFS v4 chain through REA 6.5.0.

ExecNested seat, round-84 wave w1. Own runner -- shares no code with
tools/round-84/nested-sqfs.py (that is a frozen class-based counter; this is a
flat procedural driver with a named check list). Fixture recipe is the frozen
plan's: leaf(3 files) -> mid(leaf + 2 files) -> outer(mid + 1 file), built with
mksquashfs 4.7.5 (-noappend -comp gzip -b 4096 -repro-time 1760000000), oracle
from unsquashfs 4.7.5 per level, measured by `npx -y rea-agents@6.5.0
extract-firmware <outer> <absent outdir> --max-depth {3,4} --format json`.
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

REA_PIN = "rea-agents@6.5.0"
MID = "inner-b.sqfs_extract"
DEEP = MID + "/inner-c.sqfs_extract"
REPRO_TIME = "1760000000"


def sh(argv: list[str], env=None, timeout: int = 1800) -> subprocess.CompletedProcess:
    return subprocess.run([str(a) for a in argv], capture_output=True, text=True,
                          env=env, timeout=timeout)


def file_sha(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def make_image(src: Path, dest: Path) -> str:
    done = sh(["mksquashfs", src, dest, "-noappend", "-comp", "gzip", "-b", "4096",
               "-quiet", "-repro-time", REPRO_TIME])
    if done.returncode != 0:
        raise SystemExit(f"mksquashfs failed: {done.stderr[-500:]}")
    return file_sha(dest)


def squash_oracle(image: Path, dest: Path) -> dict[str, str]:
    done = sh(["unsquashfs", "-d", dest, image])
    if done.returncode != 0:
        raise SystemExit(f"unsquashfs failed: {done.stderr[-500:]}")
    listing: dict[str, str] = {}
    for path in sorted(dest.rglob("*")):
        if path.is_file() and not path.is_symlink():
            listing[path.relative_to(dest).as_posix()] = file_sha(path)
    return listing


def build_chain(root: Path) -> tuple[dict[str, str], dict[str, dict[str, str]]]:
    leaf, mid, outer = (root / name for name in ("leaf", "mid", "outer"))
    for directory in (leaf, mid, outer):
        directory.mkdir(parents=True)
    (leaf / "alpha.txt").write_text("leaf-alpha\n")
    (leaf / "beta.txt").write_text("leaf-beta\n")
    (leaf / "gamma.bin").write_text("".join(f"row-{n:03d}\n" for n in range(200)))
    leaf_image = root / "c.sqfs"
    pins = {"c": make_image(leaf, leaf_image)}
    shutil.copyfile(leaf_image, mid / "inner-c.sqfs")
    (mid / "one.txt").write_text("mid-one\n")
    (mid / "two.txt").write_text("mid-two\n")
    pins["b"] = make_image(mid, root / "b.sqfs")
    shutil.copyfile(root / "b.sqfs", outer / "inner-b.sqfs")
    (outer / "x.txt").write_text("outer-x\n")
    pins["a"] = make_image(outer, root / "a.sqfs")
    oracles = {"a": squash_oracle(root / "a.sqfs", root / "oracle-a"),
               "b": squash_oracle(root / "b.sqfs", root / "oracle-b"),
               "c": squash_oracle(root / "c.sqfs", root / "oracle-c")}
    return pins, oracles


def expected_map(oracles: dict[str, dict[str, str]]) -> dict[str, tuple[str, int]]:
    expected: dict[str, tuple[str, int]] = {}
    for name, sha in oracles["a"].items():
        expected[name] = (sha, 1)
    for name, sha in oracles["b"].items():
        expected[f"{MID}/{name}"] = (sha, 2)
    for name, sha in oracles["c"].items():
        expected[f"{DEEP}/{name}"] = (sha, 3)
    return expected


def parse_envelope(stdout: str):
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        pass
    start = stdout.find("{")
    if start < 0:
        return None
    try:
        value, _end = json.JSONDecoder().raw_decode(stdout[start:])
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def strip_extract_root(paths: list[str]) -> tuple[list[str], str | None]:
    if not paths:
        return [], None
    head = paths[0].split("/", 1)[0]
    if head.endswith("_extract") and all(p.split("/", 1)[0] == head for p in paths):
        return [p.split("/", 1)[1] for p in paths], head
    return paths, None


def observe(envelope, expected: dict[str, tuple[str, int]], depth: int) -> dict:
    norm = (envelope or {}).get("normalized_result") or {}
    files = norm.get("files") or []
    stripped, root = strip_extract_root([f.get("relative_path") for f in files])
    by_path = dict(zip(stripped, files))
    wanted_analysis = {}
    for path, (_sha, level) in expected.items():
        if level < depth:
            wanted_analysis[path] = level
        elif level == depth:
            # deepest level: analyzed only when the budget exceeds the chain
            wanted_analysis[path] = None if depth == 3 else depth
    got_analysis = {p: (by_path.get(p) or {}).get("analysis_depth") for p in expected}
    return {
        "depth": depth,
        "file_count": len(files),
        "extract_root": root,
        "published_paths": sorted(stripped),
        "sha_by_path": {p: (by_path.get(p) or {}).get("sha256") for p in expected},
        "coverage": norm.get("coverage"),
        "depth_limited_paths": norm.get("depth_limited_paths"),
        "extraction_gaps": norm.get("extraction_gaps"),
        "published_bytes": norm.get("published_bytes"),
        "engine": norm.get("engine"),
        "analysis_depth": got_analysis,
        "analysis_expected": wanted_analysis,
        "paths_match_oracle": set(stripped) == set(expected),
        "bytes_match_oracle": all(
            (by_path.get(p) or {}).get("sha256") == expected[p][0] for p in expected),
        "analysis_matches_claim": got_analysis == wanted_analysis,
    }


def main() -> int:
    scratch = Path(sys.argv[1]).resolve()
    json_out = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else None
    scratch.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, TMPDIR=str(scratch / "tmp"),
               PYTHONDONTWRITEBYTECODE="1")
    (scratch / "tmp").mkdir(exist_ok=True)

    toolchain = {
        "mksquashfs": sh(["mksquashfs", "-version"]).stdout.splitlines()[0],
        "unsquashfs": sh(["unsquashfs", "-version"]).stdout.splitlines()[0],
        "python": platform.python_version(),
        "node": sh(["node", "--version"]).stdout.strip(),
        "rea_version": sh(["npx", "-y", REA_PIN, "--version"]).stdout.strip(),
    }

    # two independent fixture builds for the reproducibility claim
    pins1, oracles1 = build_chain(scratch / "build-r1")
    pins2, oracles2 = build_chain(scratch / "build-r2")
    reproducible = pins1 == pins2 and oracles1 == oracles2
    expected = expected_map(oracles1)

    runs = {}
    envelopes_ok = True
    for depth in (3, 4):
        outdir = scratch / f"out-depth{depth}"
        assert not outdir.exists(), f"outdir must be absent: {outdir}"
        done = sh(["npx", "-y", REA_PIN, "extract-firmware",
                   scratch / "build-r1" / "a.sqfs", outdir,
                   "--max-depth", str(depth), "--format", "json"], env=env)
        envelope = parse_envelope(done.stdout)
        envelopes_ok = envelopes_ok and envelope is not None and done.returncode == 0
        runs[str(depth)] = {
            "exit": done.returncode,
            "stderr_tail": done.stderr[-2000:],
            "envelope": envelope,
            "observed": observe(envelope, expected, depth),
        }

    d3, d4 = runs["3"]["observed"], runs["4"]["observed"]
    eng3 = (runs["3"]["envelope"] or {}).get("normalized_result", {}).get("engine") or {}
    eng4 = (runs["4"]["envelope"] or {}).get("normalized_result", {}).get("engine") or {}
    one_limited = [p for p in (d3.get("depth_limited_paths") or [])
                   if str(p).endswith(DEEP)]
    gaps3 = d3.get("extraction_gaps") or []
    checks = [
        ("E1-runs-clean", "both REA runs exit 0 with a readable normalized envelope",
         envelopes_ok
         and all((r["envelope"] or {}).get("normalized_result") for r in runs.values())),
        ("E2-depth3-paths", "depth-3 published path set equals the unsquashfs oracle",
         d3["paths_match_oracle"]),
        ("E3-depth3-bytes", "depth-3 published bytes equal the oracle sha256 map",
         d3["bytes_match_oracle"]),
        ("E4-depth3-partial", "depth-3 coverage is partial", d3["coverage"] == "partial"),
        ("E5-depth3-one-depth-limited",
         f"depth-3 depth_limited_paths is exactly one entry ending in {DEEP}",
         len(d3.get("depth_limited_paths") or []) == 1 and len(one_limited) == 1),
        ("E6-depth3-single-gap",
         "depth-3 extraction_gaps is exactly one depth-limited gap at the deepest root",
         len(gaps3) == 1 and gaps3[0].get("kind") == "depth-limited"
         and str(gaps3[0].get("input_path", "")).endswith(DEEP)),
        ("E7-depth3-analysis-map",
         "depth-3 analysis_depth: levels 1,2 at their level, level 3 null",
         d3["analysis_matches_claim"]),
        ("E8-depth4-paths", "depth-4 published path set equals the oracle",
         d4["paths_match_oracle"]),
        ("E9-depth4-bytes", "depth-4 published bytes equal the oracle sha256 map",
         d4["bytes_match_oracle"]),
        ("E10-depth4-complete",
         "depth-4 coverage complete, no gaps, no depth-limited paths",
         d4["coverage"] == "complete" and (d4.get("extraction_gaps") or []) == []
         and (d4.get("depth_limited_paths") or []) == []),
        ("E11-depth4-analysis-map",
         "depth-4 analysis_depth: levels 1,2,3 all at their level",
         d4["analysis_matches_claim"]),
        ("E12-engine-identity",
         "engine block equal across runs: unblob 26.6.4, same executable_sha256, "
         "REA reports 6.5.0",
         eng3 and eng4
         and eng3.get("name") == eng4.get("name") == "unblob"
         and eng3.get("version") == eng4.get("version") == "26.6.4"
         and eng3.get("executable_sha256") == eng4.get("executable_sha256")
         and toolchain["rea_version"] == "6.5.0"),
        ("E13-nested-identity",
         "carriers match built image digests: inner-b.sqfs in outer oracle == pin b, "
         "inner-c.sqfs in mid oracle == pin c",
         oracles1["a"].get("inner-b.sqfs") == pins1["b"]
         and oracles1["b"].get("inner-c.sqfs") == pins1["c"]),
        ("E14-fixture-reproducible",
         "two independent builds give identical image digests and oracle listings",
         reproducible),
    ]
    control = {
        "rule": "published-file-count-equals-oracle-count-therefore-complete",
        "fires": d3["file_count"] == len(expected) and d3["coverage"] != "complete",
        "detail": "the depth-3 run publishes all eight oracle members yet REA still "
                  "reports partial; a count-only completeness oracle would misgrade "
                  "this run as complete",
    }
    met = all(ok for _id, _d, ok in checks) and control["fires"]
    published_set = set(d3["published_paths"])
    analyzed_set = {p for p, depth_value in d3["analysis_depth"].items()
                    if depth_value is not None}
    receipt = {
        "schema": "execnested-r84-c3-repro-v1",
        "rev": "043b89a25241710a68b45526c3287fb3c8d907c3",
        "seat": "ExecNested",
        "toolchain": toolchain,
        "fixture_pins": {"build-r1": pins1, "build-r2": pins2,
                         "reproducible": reproducible},
        "oracle_counts": {k: len(v) for k, v in oracles1.items()},
        "expected": {p: sha for p, (sha, _lvl) in sorted(expected.items())},
        "expected_levels": {p: lvl for p, (_sha, lvl) in sorted(expected.items())},
        "runs": {d: {"exit": r["exit"], "stderr_tail": r["stderr_tail"],
                     "observed": r["observed"]} for d, r in runs.items()},
        "engine_blocks": {"depth3": eng3, "depth4": eng4},
        "depth3_vs_depth4": {
            "files_differ": d3["published_paths"] != d4["published_paths"],
            "coverage_differ": d3["coverage"] != d4["coverage"],
            "analysis_depth_differ": d3["analysis_depth"] != d4["analysis_depth"],
            "analysis_depth_delta": {p: [d3["analysis_depth"].get(p),
                                         d4["analysis_depth"].get(p)]
                                     for p in sorted(expected)
                                     if d3["analysis_depth"].get(p)
                                     != d4["analysis_depth"].get(p)},
        },
        "depth3_published_vs_analyzed": {
            "published": sorted(published_set),
            "analyzed": sorted(analyzed_set),
            "published_not_analyzed": sorted(published_set - analyzed_set),
            "same_set": published_set == analyzed_set,
        },
        "checks": [{"id": cid, "desc": desc, "ok": ok} for cid, desc, ok in checks],
        "control": control,
        "met": met,
    }
    text = json.dumps(receipt, indent=1, sort_keys=True)
    print(text)
    print(f"REPRO checks={len(checks)} all_true={all(ok for _i, _d, ok in checks)} "
          f"control_fires={control['fires']} met={met}")
    if json_out:
        json_out.parent.mkdir(parents=True, exist_ok=True)
        json_out.write_text(text + "\n")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
