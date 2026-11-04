#!/usr/bin/env python3
"""Round-72 claims container generator (freeze). Writes .ufo/waves/round-72/claims.json."""

import hashlib
import json
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
BASE = "56241b1c8baff95862730c008f1ae5132b03388e"
DECL = "6316c1053f927a1a1cdc3e0960b70acab5f56381"
FIX1 = "17d8b5f785a449aed76f42e697071007ae9e226f"  # mutation-check: both selftest schemas
FIX2 = "306cbb3fb11661fba6f364f73ad0b1eeb24a959f"  # seam-probe: binding_verdict assignment form
FIX3 = "25ecc71116bad0673416ebfc128be5a16e03b7e2"  # controls: c3 checker at the declaration rev
FIX4 = "1563ea353ab32acc2141c82b89299580cb73f4c8"  # controls: caller-supplied pinned packer

C1 = ("R72-C1 is verified iff the frozen seam probe, run at the measured revision as "
      "`python3 -I -B tools/round-72/seam-probe.py --root . --rev <measured> --tool "
      "tools/round-72/packed-elf.py --battery tools/round-72/mutation-check.py --pkg <REA 6.5.0 "
      "root> --work <scratch> --receipt <route receipt> --expect-upx <pinned copy> "
      "--nonce-commitment <pre-committed commitment> --json-out <receipt>`, reports `arms_passed "
      "11` of `target 11` with `A11_checker_env` true — both shims' key sets exactly "
      "HOME/LANG/PATH/TMPDIR, the canary key absent, HOME and TMPDIR under the checker's run root, "
      "the checker's own `checker_child_env` recording at least two records whose child census "
      "contains `git` and `readelf` — while the same probe at the same revision against `--tool "
      "tools/round-71/packed-elf.py` reports 9 of 11 naming `A10_run_binding` and "
      "`A11_checker_env` false, the A11 observation showing the shim's canary present.")
C2 = ("R72-C2 is verified iff the frozen mutation battery, run at the measured revision as "
      "`python3 -I -B tools/round-72/mutation-check.py --root . --rev <measured> --tool "
      "tools/round-72/seam-probe.py --patch-set r72 --work <scratch> --json-out <receipt>`, exits "
      "0 with the single `A10_binding_force_true` mutant `killed`, its `failed` list naming "
      "`a10-binding-from-checker`, pristine selftest green, no wrong-case kill, and target pin "
      "matched — while the same battery with `--patch-set r71 --rev "
      "b827a8b5d54f2885ec9be7786389f356c59226ce --tool tools/round-71/seam-probe.py` reports "
      "`survivor_count 1` and survivors `[\"A10_binding_force_true\"]`; and the landing probe's A10 "
      "observation records `genuine_verdict {present true, nonce_ok true, binding_ok true}` with "
      "`wrong_nonce.nonce_ok false` and `broken_binding.binding_ok false` from the checker's JSON.")
C3 = ("R72-C3 is verified iff the frozen capsule audit, run at the measured revision as "
      "`python3 -I -B tools/round-72/capsule-audit.py --tamper-battery --capsule "
      ".ufo/waves/round-71/l1/scores/c1-env-at-landing.jsonl --audit "
      ".ufo/waves/round-71/l1/scores/c1-env-audit.json --work <scratch> --json-out <receipt>`, "
      "exits 0 with the genuine capsule accepted (`ok true`, 46 records, every clause true) and "
      "all seven tampered shapes (`log_sha256`, `records`, `keys`, `canary`, `home_under_run`, "
      "`tmpdir_under_run`, `children`) rejected each naming its declared clause — and the "
      "round-72 receipt checker on the filed lying receipt (`--check-receipt <lying receipt> "
      "--capsule <polluted capsule> --nonce-commitment <commitment>`) exits 1 with "
      "`receipt_capsule: canary` in `failing` and `clauses.receipt_capsule false`, while the "
      "round-71 checker accepts the same lying receipt shaped from its own genuine route receipt "
      "(`met true`, `failing []`).")

INSTRUMENTS = [
    "tools/round-72/packed-elf.py",
    "tools/round-72/seam-probe.py",
    "tools/round-72/mutation-check.py",
    "tools/round-72/capsule-audit.py",
    "tools/round-72/capsule_audit.py",
    "tools/round-72/controls.py",
]
LOADED_BY_COUNTER = [
    "tools/round-71/packed-elf.py",
    "tools/round-71/seam-probe.py",
    "tools/round-70/mutation-check.py",
    "tools/round-71/registry-census.py",
    "tools/round-70/packed-elf.py",
]


def blob(path: str) -> str:
    proc = subprocess.run(["git", "-C", LANE, "show", f"HEAD:{path}"],
                          capture_output=True)
    if proc.returncode != 0:
        raise SystemExit(f"git show HEAD:{path} failed")
    return hashlib.sha256(proc.stdout).hexdigest()


def main() -> int:
    instruments = {p: blob(p) for p in INSTRUMENTS}
    loaded = {p: blob(p) for p in LOADED_BY_COUNTER}
    container = {
        "schema": "1",
        "round": "round-72",
        "base": BASE,
        "claim_row": "S275",
        "claims": [C1, C2, C3],
        "declaration_pointer": (
            "plans/round-72-claims.md (no predicate amendments). The six instruments were "
            f"committed BEFORE this claims file (QUALITY #33): declaration {DECL} (tools/round-72/*, "
            "the plan, the nonce commitment, the census-start receipt), with two pre-freeze "
            f"declaration fixes whose bytes are the operative pin state: {FIX1} (the mutation "
            "battery reads both selftest schemas), {FIX2} (binding_verdict uses the assignment "
            f"form the frozen mutant patches), {FIX3} and {FIX4} (the controls' two arm fixes). "
            "Predicates byte-unchanged. "
            "The pre receipts in .ufo/waves/round-72/l1/pre/ (route-at-declaration.json, "
            "route-r71-at-declaration.json, env-at-declaration.jsonl, c1-at-base.json, "
            "c2-at-base.json, c2-mutant-test.json, c3-at-base.json, controls-at-declaration.json, "
            "nonce-commitment.txt) were measured at that state and committed before this file."),
        "errata": [
            {"fields": ["plans/round-72-claims.md Sourced claim", "claim_row"],
             "text": ("the plan's first draft named claim_row S276; the registry's highest id is "
                      "S274, so the row this round opens is S275. The plan was amended pre-freeze "
                      "(the predicate sentences unchanged) and this container names S275. The "
                      "append re-checks the duplicate-id guard before landing the row.")},
            {"fields": ["frozen_atoms.A0"],
             "text": (f"the declaration commit {DECL} carries the instruments; four pre-freeze fixes "
                      f"({FIX1}, {FIX2}, {FIX3}, {FIX4}) changed tools/round-72/mutation-check.py, "
                      "tools/round-72/seam-probe.py and tools/round-72/controls.py before any claim "
                      "data (a selftest-schema read, the mutant patch site, and the two control "
                      "arms' argv/rev). The pre receipts were measured against the fixed bytes; the "
                      "pins below are those bytes.")},
        ],
        "frontier": {
            "assimilation": "none (the merge/kaidoku/ package does not serve these claims)",
            "considerthese": "absent in this lane",
            "mistake": "corpus/lessons/round-72.md ## Mistakes",
            "sources": ("corpus/SOURCES.md: S275 (the Linux proc(5) /proc/pid/environ paragraph, "
                        "tier A, opened this round; grounds the exec-boundary measurement of a "
                        "child's environment) — cited by "
                        "corpus/knowledge/2026-11-04-r72-checker-env-capsule.md."),
        },
        "frozen_atoms": {
            "A0": (f"base {BASE} (the round-71 lane tip: report, close, non-author spot-check); "
                   f"declaration {DECL} (the six round-72 instruments, this plan, the nonce "
                   f"commitment, the census-start receipt); pre-freeze declaration fixes {FIX1}, "
                   f"{FIX2}, {FIX3}, {FIX4} (bytes unchanged after them); the order is base, instruments+plan, the "
                   "pre receipts, this container (QUALITY #33)."),
            "A1": ("the instrument pins below are the frozen bytes (tools/round-72/*); no "
                   "post-freeze edit of a pinned path without an appended instrument_supersessions "
                   "entry carrying the replacement sha256 and the reason, and a re-taken before "
                   "record (the round-71 container's missing-sha defect, R72-G3)."),
            "A2": ("R72-C1: tools/round-72/packed-elf.py `--check-receipt` runs its git (tool blob) "
                   "and readelf (carrier format) children under build_child_env(check_root), "
                   "records them into `--child-env-log`, and emits `checker_child_env`; the probe's "
                   "A11 runs the checker with a git and a readelf shim first on PATH that dump "
                   "`/proc/self/environ` bytes, an exported canary in the caller environment, and "
                   "requires both shims allowlisted + canary-free + HOME/TMPDIR under --work, plus "
                   "the checker's own log to contain git and readelf. Base world: the round-71 "
                   "route at the same rev, 9 of 11, A10/A11 false."),
            "A3": ("R72-C2: `binding_verdict(checker)` reads `clauses.run_nonce` / "
                   "`clauses.run_binding` from the checker's JSON; absent clauses are fail-closed "
                   "(present false). The frozen mutant `binding_ok = clauses.get(\"run_binding\") is "
                   "True and present` -> `binding_ok = True` is killed by the selftest case "
                   "`a10-binding-from-checker`; on the round-71 probe the same mutant (its own "
                   "line) survives. Nothing else in the probe re-derives a binding verdict."),
            "A4": ("R72-C3: the capsule audit's seven clauses (log_sha256, records, keys, canary, "
                   "home_under_run, tmpdir_under_run, children); a summary that claims no digest "
                   "leaves log_sha256 not-evaluated (None, recorded, never green by omission); the "
                   "seven tampered shapes are cut from the committed 46-record capsule "
                   ".ufo/waves/round-71/l1/scores/c1-env-at-landing.jsonl with the committed "
                   "summary c1-env-audit.json as the claim; every shape must fail naming its "
                   "declared clause. The base world: the round-71 checker accepts a lying receipt "
                   "(no clause object, `met true`)."),
            "A5": ("pins reused from rounds 70-71: packer upx 5.2.0 sha256 "
                   "cf2f6e7c6846a7c9a2224bc2bcc2dd79db6847d2cc73092d7356ce5c9aa8c969; REA package "
                   "6.5.0 package.json sha256 "
                   "a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c; the four "
                   "carriers, DECLARED_ORIG and DECLARED_PACKED are the round-70 tables."),
            "A6": ("pre receipts (before any claim data): l1/pre/route-at-declaration.json (the "
                   "round-72 route at the declaration, pinned-copy argv, 4 carriers, met_target "
                   "true, 46 observed children) + env-at-declaration.jsonl; "
                   "l1/pre/route-r71-at-declaration.json (the round-71 route at the same rev for "
                   "the base arm); c1-at-base.json (the round-72 probe against the round-71 route: "
                   "9 of 11, A10/A11 false, shim canary present); c2-at-base.json (patch set r71: "
                   "survivor 1); c2-mutant-test.json (patch set r72 against the fixed probe: killed "
                   "naming a10-binding-from-checker); c3-at-base.json (the round-71 checker accepts "
                   "the lying receipt; the audit rejects it naming canary); "
                   "controls-at-declaration.json; nonce-commitment.txt."),
            "A7": ("the nonce plaintext lives only in scratch; its sha256 "
                   "(2532bd5bd8bbf48b5576821b29f35d90b55ab136a9e7179eff989cf961b84fd5) is "
                   "committed at l1/pre/nonce-commitment.txt BEFORE the route runs; both route "
                   "receipts carry run_nonce and run_binding = "
                   "sha256(nonce:instrument.sha256:packed pins). The nonce is reused across the "
                   "two declaration runs because both are genuine runs of the same pre-committed "
                   "challenge; the receipts are distinguished by their instrument path and "
                   "packed pins, not by the nonce."),
            "A8": ("landing receipts: l1/scores/c1-at-landing.json (the probe at the landing rev), "
                   "c2-at-landing.json (the r72 mutant), c3-at-landing.json (the audit battery), "
                   "c3-lying-check.json (the round-72 checker on the lying receipt), "
                   "controls-at-landing.json, gate-at-freeze.json / gate-at-landing.json / "
                   "gate-at-record.json, registry-conformance-at-record.json."),
            "A9": ("frontier step: SOURCES.md gains S275 only if ScoutSource's live fetch and "
                   "locate succeed (a failed fetch is a rejected row with its reason, never an "
                   "admitted one); the lesson's ## Gate records URL, access date and the <=25-word "
                   "quote; the knowledge entry carries the provenance trio; no considerthese/ "
                   "directory exists; assimilation none."),
            "A10": ("repairs carried, not claim input: R72-G1 (the round-71 role-count defect is "
                    "corrected in this round's report, not by rewriting that one), R72-G2 (the "
                    "c2-do-nothing citation names the landing control receipt), R72-G3 (any "
                    "round-72 supersession entry carries the replacement sha256), R72-G4 (the S274 "
                    "column contract is repaired as a new row under SOURCES rule 2), R72-G5 (the "
                    "standing duties), R72-G6 (the wave-settlement receipt)."),
            "A11": ("wave: one v1 wave r72-w1, 16 seats (5 executor, 3 scribe, 2 reviewer, 2 "
                    "mutation-tester, 1 critic, 1 sentinel, 1 scout, 1 connector); attack roles "
                    "(reviewer/critic/mutation-tester) 5 of 16 = 31%; the L1 holds the planner "
                    "seat; no residual call; dead seats reported from the results file."),
        },
        "instruments": instruments,
        "loaded_by_counter": loaded,
        "repairs": ["R72-G1", "R72-G2", "R72-G3", "R72-G4", "R72-G5", "R72-G6"],
    }
    out = os.path.join(LANE, ".ufo/waves/round-72/claims.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(container, fh, indent=1)
        fh.write("\n")
    print(out)
    print(json.dumps({"instruments": len(instruments), "loaded": len(loaded)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
