#!/usr/bin/env python3
"""Generate the round-78 attack fixtures under .ufo/waves/round-78/attacks/.

Nine trees, one per attack class declared in tools/round-78/attack-gate.py
ATTACKS.  Each tree is a minimal record: PROVINCE.md carries the single
`- **Core — ` bullet whose parenthesised verdict the class attacks, plus the
receipt the cell names.  Receipts that must authenticate write `@HEAD@` where
their 40-hex rev goes; the gate materialises the tree as a two-commit repo and
substitutes the first commit's hash (the commit that carries the instrument
blob the receipt pins), so a receipt's provenance resolves by construction.

    python3 .ufo/waves/round-78/attacks/gen-fixtures.py

Writes only inside the lane.  Never run it from a seat.
"""

from __future__ import annotations

import hashlib
import json
import pathlib

LANE = pathlib.Path(__file__).resolve().parents[4]
OUT = LANE / ".ufo/waves/round-78/attacks"
SCORES = ".ufo/waves/round-78/l1/scores"

FIXTURE_INSTRUMENT = (
    "# fixture instrument: the blob a fixture receipt pins\n"
    "PREDICATE = 'fixture'\n")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def receipt(rev: str, instrument_sha: str, **extra) -> dict:
    out = {"schema": "kaidoku-r78-fixture-receipt-v1",
           "rev": rev,
           "instrument": {"path": "tools/round-78/fixture-instrument.py",
                          "sha256": instrument_sha}}
    out.update(extra)
    return out


def filing_receipt(rev: str, exit_code: int, token: str, argv_path: str) -> dict:
    stdout = f"prefile: tree clean\nprefile: {token}\n"
    return {"schema": "kaidoku-r77-prefile-receipt-v1",
            "lane": "/fixture", "rev": rev,
            "argv": ["bash", argv_path, "/fixture"],
            "exit": exit_code, "passed": exit_code == 0 and token == "PASS",
            "prefile_line": f"prefile: {token}", "stdout": stdout,
            "stdout_sha256": sha256_bytes(stdout.encode()),
            "stdout_lines": 2, "stderr_tail": "",
            "env_keys": ["HOME", "LANG", "PATH", "TMPDIR"]}


def province(bullet: str) -> str:
    return ("# kaidoku-shokunin — fixture province\n\n"
            "## Core\n\n" + bullet + "\n")


def scorecard() -> str:
    return ("# fixture scorecard\n\n## Capabilities\n\n"
            "| Capability | What it can now do | Evidence pointer | First-working round |\n"
            "|---|---|---|---|\n")


def tree(name: str, bullet: str, receipts: dict[str, object]) -> dict:
    files = {
        "SCORECARD.md": scorecard(),
        "PROVINCE.md": province(bullet),
        "tools/round-78/fixture-instrument.py": FIXTURE_INSTRUMENT,
    }
    for path, payload in receipts.items():
        files[path] = (payload if isinstance(payload, str)
                       else json.dumps(payload, indent=1, sort_keys=True) + "\n")
    return {"name": name, "files": files}


def main() -> int:
    instrument_sha = sha256_bytes(FIXTURE_INSTRUMENT.encode())
    gate = "tools/round-29/prefile-check.sh"
    good_filing = filing_receipt("@HEAD@", 0, "PASS", gate)
    fail_filing = filing_receipt("@HEAD@", 1, "FAIL", gate)
    stale_filing = filing_receipt("0" * 40, 0, "PASS", gate)
    stale_gate = filing_receipt("0" * 40, 0, "PASS", gate)

    green = receipt("@HEAD@", instrument_sha,
                    atoms=[{"id": "D24_capability_rows", "ok": True}],
                    mismatch_count=0)
    nested = receipt("@HEAD@", instrument_sha, mismatch_count=0,
                     atoms=[{"id": "D24_capability_rows", "ok": True}],
                     arms=[{"arm": "a12", "observed": {"verdict":
                                                      {"forged_detected": False}}}])
    dropped = receipt("@HEAD@", instrument_sha, mismatch_count=0)

    # a1: a hand-authored green receipt with no rev and no instrument pin.
    forged = {"atoms": [{"id": "D24_capability_rows", "ok": True}],
              "mismatch_count": 0}
    fixtures = [
        tree("a1-forged-receipt",
             "- **Core — forged receipt:** `.ufo/waves/round-78/l1/scores/"
             "green-forged.json` records the verdict (D24 true, mismatch_count 0).",
             {f"{SCORES}/green-forged.json": forged}),
        tree("a2-repunctuated",
             "- **Core — repunctuated:** `.ufo/waves/round-78/l1/scores/"
             "green-authed.json` records the verdict (D24: true, mismatch 0, "
             "D24 true).",
             {f"{SCORES}/green-authed.json": green}),
        tree("a3-near-miss",
             "- **Core — near miss:** `.ufo/waves/round-78/l1/scores/"
             "green-authed.json` records the verdict (mismatch 0, D24 true).",
             {f"{SCORES}/green-authed.json": green}),
        tree("a4-negated",
             "- **Core — negated:** `.ufo/waves/round-78/l1/scores/"
             "green-authed.json` records the verdict (the receipt does not record "
             "D24 false, D24 true).",
             {f"{SCORES}/green-authed.json": green}),
        tree("a5-nested-field",
             "- **Core — nested:** `.ufo/waves/round-78/l1/scores/"
             "nested.json` records the verdict (forged_detected true, D24 true).",
             {f"{SCORES}/nested.json": nested}),
        tree("a6-dropped-defect",
             "- **Core — dropped defect:** `.ufo/waves/round-78/l1/scores/"
             "dropped.json` records the verdict (D24 true, mismatch_count 0).",
             {f"{SCORES}/dropped.json": dropped}),
        tree("b1-fail-run",
             "- **Core — failing run:** `.ufo/waves/round-78/l1/scores/"
             "prefile-at-filing.json` records a run (exit 1).",
             {f"{SCORES}/prefile-at-filing.json": fail_filing,
              ".ufo/waves/round-77/l1/scores/prefile-at-filing.json": fail_filing}),
        tree("b2-stale-filing",
             "- **Core — stale filing:** `.ufo/waves/round-78/l1/scores/"
             "prefile-at-filing.json` records a run (exit 0).",
             {f"{SCORES}/prefile-at-filing.json": stale_filing,
              ".ufo/waves/round-77/l1/scores/prefile-at-filing.json": stale_filing}),
        tree("b3-one-key-gate",
             "- **Core — one key gate:** `.ufo/waves/round-78/l1/scores/"
             "gate-at-tip.json` records a run (exit 0).",
             {f"{SCORES}/prefile-at-filing.json": good_filing,
              ".ufo/waves/round-77/l1/scores/prefile-at-filing.json": good_filing,
              f"{SCORES}/gate-at-tip.json": {"exit": 0}}),
        tree("b4-stale-gate-rev",
             "- **Core — stale gate rev:** `.ufo/waves/round-78/l1/scores/"
             "gate-at-tip.json` records a run (exit 0).",
             {f"{SCORES}/prefile-at-filing.json": good_filing,
              ".ufo/waves/round-77/l1/scores/prefile-at-filing.json": good_filing,
              f"{SCORES}/gate-at-tip.json": stale_gate}),
    ]
    written = []
    for fixture in fixtures:
        root = OUT / fixture["name"]
        for relative, payload in fixture["files"].items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(payload)
            written.append(str(path.relative_to(LANE)))
    print(json.dumps({"fixtures": len(fixtures), "files": len(written),
                      "root": str(OUT)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
