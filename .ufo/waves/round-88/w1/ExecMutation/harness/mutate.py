#!/usr/bin/env python3
"""Round-88 mutation probe harness (seat ExecMutation).

For each declared mutant: copy the instrument into a depth-preserving mirror,
assert the anchor occurs exactly once, apply the single edit, byte-compile it,
run `--selftest`, and record rc / case count / failure names / whether the
declared case failed.  Killed == declared case present in the selftest and
failing.  A declared case that the instrument does not contain is recorded as
`absent` (survivor / coverage gap), never as a kill.
"""

import difflib
import hashlib
import json
import os
import shutil
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
SCRATCH = "/fast/scratch/hyaku/kaidoku-r88/ExecMutation"
MUT = os.path.join(SCRATCH, "mut")

REPAIR = "tools/round-88/upx-chain-repair.py"
BATTERY = "tools/round-88/upx-chain-battery.py"

# (id, file, anchor, replacement, declared_case, rationale)
MUTANTS = [
    # --- repair: chain-geometry law -------------------------------------
    ("R01", REPAIR,
     "            if not (0 < derived <= sz_unc0):\n",
     "            if not (0 < derived):\n",
     "derived-value",
     "drop the upper bound derived <= block0 sz_unc"),
    ("R02", REPAIR,
     "            try:\n"
     "                end, info = rep.find_sentinel(bytes(dd), b0, ph_off, ph[\"method\"])\n"
     "            except rep.Refused:\n"
     "                continue\n",
     "            end, info = ph_off, {\"resume\": None, \"blocks_first\": 0, \"blocks_resumed\": 0}\n",
     "chain-geometry-recovers",
     "drop the sentinel-reach test on candidates"),
    ("R03", REPAIR,
     "            if total > ph[\"u_len\"]:\n"
     "                fits = False\n"
     "            else:\n"
     "                fits = True\n",
     "            fits = True\n",
     "geometry-records-u_len",
     "drop the fits_u_len preference (always fits)"),
    ("R04", REPAIR,
     "            key = (fits, total, -derived)\n",
     "            key = (total, -derived)\n",
     "geometry-records-u_len",
     "prefer the largest accounted total regardless of u_len"),
    ("R05", REPAIR,
     "        if sz_cpr0 != 0 or sz_unc0 == 0:\n",
     "        if sz_unc0 == 0:\n",
     "szcpr-nonzero-not-derived",
     "accept a non-zero sz_cpr and derive over it"),
    ("R06", REPAIR,
     "        total += sz_unc\n",
     "        total += sz_cpr\n",
     "geometry-records-u_len",
     "account compressed length instead of uncompressed"),
    ("R07", REPAIR,
     "            if not (0 < sc <= su) or s1 + 12 + sc > ph_off \\\n"
     "                    or d[s1 + 8] not in (m0, ph[\"method\"]):\n",
     "            if not (0 < sc <= su) or s1 + 12 + sc > ph_off:\n",
     "chain-geometry-recovers",
     "drop the method gate on candidate b_info blocks"),
    ("R08", REPAIR,
     "    except (Refused, OSError) as exc:\n"
     "        print(f\"refused: {exc}\", file=sys.stderr)\n"
     "        return 2\n",
     "    except (Refused, OSError) as exc:\n"
     "        print(f\"refused: {exc}\", file=sys.stderr)\n"
     "        return 2\n"
     "    except Exception as exc:  # noqa: BLE001\n"
     "        print(f\"error: {exc}\", file=sys.stderr)\n"
     "        return 1\n",
     "exit-1-on-untyped-error",
     "exit 1 on an uncaught exception instead of 2"),
    # --- battery: scoring arms and fixtures -----------------------------
    ("B01", BATTERY,
     "        if a != b and not (lo <= i < hi):\n",
     "        if a != b and not (lo <= i < hi) and False:\n",
     "field-only-refuses-outside",
     "weaken field_only to a length-only check"),
    ("B02", BATTERY,
     "    if len(tampered) != len(out):\n",
     "    if len(tampered) != len(out) and False:\n",
     "field-only-refuses-length",
     "drop the length equality check in field_only"),
    ("B03", BATTERY,
     "    if name == \"identity\":\n        return data\n",
     "    if name == \"identity\":\n        return data + b\"\\0\"\n",
     "identity-builtin-noop",
     "identity control no longer byte-identical"),
    ("B04", BATTERY,
     "TARGET = len(CARRIERS)\n",
     "TARGET = 3\n",
     "target-is-four",
     "target lowered to 3 of 4"),
    ("B05", BATTERY,
     "            if r[\"rc\"] != 0 or not os.path.isfile(dst):\n",
     "            if (r[\"rc\"] not in (0, None)) or not os.path.isfile(dst):\n",
     "rc-none-not-refusal",
     "treat rc is None (child error) as success, not refusal"),
]

# control-green probes: (id, file, anchor, replacement, expected, cmd)
CONTROL_PROBES = [
    ("G1", BATTERY,
     "    if name == \"identity\":\n        return data\n",
     "    if name == \"identity\":\n"
     "        if data[:4] == b\"\\x7fELF\" and b\"UPX!\" not in data:\n"
     "            raise _Refused(2, [\"refused: unpacked ELF\"])\n"
     "        return data\n",
     "identity", "identity builtin refuses an unpacked ELF (N1 green)"),
    ("G2", BATTERY,
     "            controls[\"N1-refuse-plain\"].append({\"carrier\": c[\"id\"], \"rc\": n1[\"rc\"],\n"
     "                                                \"refused\": n1[\"rc\"] != 0})\n",
     "            controls[\"N1-refuse-plain\"].append({\"carrier\": c[\"id\"], \"rc\": n1[\"rc\"],\n"
     "                                                \"refused\": True})\n",
     "identity", "N1 recorded true unconditionally (N1 green)"),
    ("G3", BATTERY,
     "    if name == \"naive-global\":\n",
     "    if name == \"naive-global\":\n"
     "        if data[:4] == b\"\\x7fELF\" and b\"UPX!\" not in data:\n"
     "            raise _Refused(2, [\"refused: unpacked ELF\"])\n",
     "naive-global", "naive-global builtin refuses an unpacked ELF (N1 green)"),
]


def mirror(mid, rel):
    base = os.path.join(MUT, mid)
    dst_dir = os.path.join(base, os.path.dirname(rel))
    os.makedirs(dst_dir, exist_ok=True)
    link = os.path.join(base, "tools", "round-87")
    if not os.path.exists(link):
        os.symlink(os.path.join(LANE, "tools", "round-87"), link)
    dst = os.path.join(base, rel)
    src = os.path.join(LANE, rel)
    with open(src, "r", encoding="utf-8") as fh:
        text = fh.read()
    return src, dst, text


def build(mid, rel, anchor, replacement):
    src, dst, text = mirror(mid, rel)
    n = text.count(anchor)
    if n != 1:
        raise SystemExit(f"{mid}: anchor matched {n} times (need exactly 1)")
    out = text.replace(anchor, replacement, 1)
    with open(dst, "w", encoding="utf-8") as fh:
        fh.write(out)
    r = subprocess.run([sys.executable, "-I", "-B", "-m", "py_compile", dst],
                       capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(f"{mid}: mutant does not compile: {r.stderr}")
    diff = "".join(difflib.unified_diff(
        text.splitlines(True), out.splitlines(True),
        fromfile=rel, tofile=f"mutant-{mid}/{rel}", n=2))
    return {"src": src, "dst": dst, "anchor_count": n, "diff": diff,
            "sha256": hashlib.sha256(out.encode()).hexdigest(),
            "src_sha256": hashlib.sha256(text.encode()).hexdigest()}


def run_selftest(path):
    r = subprocess.run([sys.executable, "-I", "-B", path, "--selftest"],
                       capture_output=True, text=True, timeout=600)
    line = (r.stdout + r.stderr).strip().splitlines()
    head = line[-1] if line else ""
    cases, fails = None, []
    for tok in head.split():
        if tok.startswith("cases="):
            cases = int(tok.split("=", 1)[1])
        elif tok.startswith("failures="):
            nf = int(tok.split("=", 1)[1])
    parts = head.split("failures=", 1)
    if len(parts) == 2:
        rest = parts[1].split(None, 1)
        if len(rest) == 2:
            fails = rest[1].split()
    return {"rc": r.returncode, "cases": cases, "failures": fails, "head": head}


def main():
    shutil.rmtree(MUT, ignore_errors=True)
    os.makedirs(MUT, exist_ok=True)
    base_repair = run_selftest(os.path.join(LANE, REPAIR))
    base_battery = run_selftest(os.path.join(LANE, BATTERY))
    base_cases = {"tools/round-88/upx-chain-repair.py":
                  {"intact-idempotent", "chain-geometry-recovers", "derived-value",
                   "geometry-records-u_len", "anchor-class-composed", "no-packheader",
                   "not-elf", "zero-length", "szcpr-nonzero-not-derived", "input-cap",
                   "upstream-pinned"},
                  "tools/round-88/upx-chain-battery.py":
                  {"field-only-accepts-window", "field-only-refuses-outside",
                   "field-only-refuses-length", "identity-builtin-noop",
                   "target-is-four", "class-name"}}
    rows = []
    for mid, rel, anchor, repl, declared, why in MUTANTS:
        rec = build(mid, rel, anchor, repl)
        st = run_selftest(rec["dst"])
        present = declared in base_cases[rel]
        killed = bool(present and declared in st["failures"])
        rows.append({
            "id": mid, "file": rel, "anchor": anchor, "replacement": repl,
            "declared_case": declared, "rationale": why,
            "anchor_count": rec["anchor_count"],
            "mutant_sha256": rec["sha256"], "source_sha256": rec["src_sha256"],
            "selftest_rc": st["rc"], "selftest_cases": st["cases"],
            "selftest_failures": st["failures"], "declared_case_present": present,
            "declared_case_failed": declared in st["failures"],
            "verdict": "killed" if killed else ("gap-absent-case" if not present else "survivor"),
            "diff": rec["diff"],
        })
    probes = []
    for mid, rel, anchor, repl, cmd, why in CONTROL_PROBES:
        rec = build(mid, rel, anchor, repl)
        probes.append({"id": mid, "file": rel, "anchor": anchor, "replacement": repl,
                       "repair_cmd": cmd, "rationale": why,
                       "anchor_count": rec["anchor_count"],
                       "mutant_path": rec["dst"],
                       "mutant_sha256": rec["sha256"]})
    out = {"base": {"repair": base_repair, "battery": base_battery},
           "rows": rows, "control_probes": probes}
    with open(os.path.join(SCRATCH, "mutants.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    print(json.dumps({"base": out["base"],
                      "rows": [{k: r[k] for k in ("id", "declared_case",
                                                  "declared_case_present",
                                                  "selftest_failures", "verdict")}
                               for r in rows]}, indent=1))


if __name__ == "__main__":
    main()
