#!/usr/bin/env python3
"""Build receipt.tsv from the captured stdout files (sha256 + UTC mtime + command)."""
import hashlib
import os
import datetime

S = os.path.dirname(os.path.abspath(__file__))
L = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
FZ = "31820472784284727546808acc31b3ea1e73919b"
F3 = "65678df0f1666e83cdeea7233bfb31ffe73ec709"
F4 = "0425224756791b414454df28a9abf93dcdf154ce"
R45F = "f762b7273e3f6ca3c710bb37d5de92a4a4417aec"
R45R = "f59565b782c18b0eb691bec12f52d2f80d9f5032"
FIX = None
try:
    import json
    FIX = json.load(open(os.path.join(S, "fixture.json")))["rev"]
except Exception:
    pass

CMDS = {
 "attest-selftest.stdout": ("0", f"python3 -I -B $S/frozen/attest.py --root {L} --freeze {FZ} --rev {FZ} --selftest"),
 "registry-selftest.stdout": ("0", f"python3 -I -B $S/frozen/registry.py --root {L} --freeze {FZ} --rev {FZ} --selftest"),
 "attest-fidelity-frozen.stdout": ("0", f"python3 -I -B $S/frozen/attest.py --root {L} --spec r45 --profile v1 --no-battery --freeze {R45F} --rev {R45R}"),
 "registry-fidelity-frozen.stdout": ("0", f"python3 -I -B $S/frozen/registry.py --root {L} --spec r45 --profile v1 --no-battery --freeze {R45F} --rev {R45R}"),
 "r45-c1.stdout": ("0", f"python3 -I -B $S/r45/c1-counter.py --root {L} --freeze {R45F} --rev {R45R}"),
 "r45-c2.stdout": ("0", f"python3 -I -B $S/r45/c2-counter.py --root {L} --freeze {R45F} --rev {R45R}"),
 "attest-head-vs-3182047.stdout": ("2", f"python3 -I -B $S/frozen/attest.py --root {L} --freeze {FZ} --rev HEAD   # HEAD resolved e3dfdbad"),
 "registry-head-vs-3182047.stdout": ("2", f"python3 -I -B $S/frozen/registry.py --root {L} --freeze {FZ} --rev HEAD   # HEAD resolved e3dfdbad"),
 "latest-attest-freeze318.stdout": ("2", f"python3 -I -B $S/headlatest/attest.py --root {L} --freeze {FZ} --rev HEAD   # HEAD resolved 49e6cac4"),
 "latest-registry-freeze318.stdout": ("2", f"python3 -I -B $S/headlatest/registry.py --root {L} --freeze {FZ} --rev HEAD   # HEAD resolved 49e6cac4"),
 "attest-r46-head.stdout": ("0", f"python3 -I -B $S/head/attest.py --root {L} --freeze {F3} --rev HEAD   # HEAD resolved 7bf33e31"),
 "registry-r46-head.stdout": ("1", f"python3 -I -B $S/head/registry.py --root {L} --freeze {F3} --rev HEAD   # HEAD resolved 17a72375, registry not yet landed"),
 "attest-donothing-frozen.stdout": ("2", f"python3 -I -B $S/frozen/attest.py --root {L} --freeze {FZ} --rev {FZ}   # default battery"),
 "attest-donothing-frozen-nb.stdout": ("1", f"python3 -I -B $S/frozen/attest.py --root {L} --freeze {FZ} --rev {FZ} --no-battery"),
 "registry-donothing-frozen.stdout": ("1", f"python3 -I -B $S/frozen/registry.py --root {L} --freeze {FZ} --rev {FZ}   # default battery: traceback"),
 "registry-donothing-frozen-nb.stdout": ("1", f"python3 -I -B $S/frozen/registry.py --root {L} --freeze {FZ} --rev {FZ} --no-battery"),
 "attest-frozen-at-head.stdout": ("1", f"python3 -I -B $S/frozen/attest.py --root {L} --freeze {F3} --rev HEAD   # NameError: REF"),
 "battery-probe.stdout": ("0", "python3 -B $S/probe_battery.py   # frozen bytes, attest.REF rebound in memory; printed receipt exit 1"),
 "registry-draft-frozen.stdout": ("1", f"python3 -I -B $S/frozen/registry.py --root $FIXTURE --freeze $FIXTURE_REV --rev $FIXTURE_REV   # frozen bytes, L1 draft section"),
 "registry-draft-head.stdout": ("1", f"python3 -I -B $S/head/registry.py --root $FIXTURE --freeze $FIXTURE_REV --rev $FIXTURE_REV   # pre-F4 bytes, L1 draft section"),
 "latest-registry-fixture.stdout": ("0", f"python3 -I -B $S/headlatest/registry.py --root $FIXTURE --freeze $FIXTURE_REV --rev $FIXTURE_REV   # F4 bytes, L1 draft section"),
 "v1-gap.stdout": ("0", "python3 -B $S/probe_v1_gap.py   # per-mutation v1/v2 exits, frozen registry"),
 "gate-probe.stdout": ("0", "python3 -B $S/probe_gate.py   # frozen gate.freeze_state, four fixture repos"),
 "gate-probe-latest.stdout": ("0", "python3 -B $S/probe_gate_latest.py   # HEAD gate.freeze_state"),
 "attest-probe.stdout": ("0", "python3 -B $S/probe_attest.py   # frozen attest.score, synthetic SKILL"),
 "attest-probe-latest.stdout": ("0", "python3 -B $S/probe_attest_latest.py   # HEAD attest.score"),
 "latest-attest-green.stdout": ("0", f"python3 -I -B $S/headlatest/attest.py --root {L} --freeze {F4} --rev HEAD   # HEAD resolved 49e6cac4"),
 "latest-registry-green.stdout": ("0", f"python3 -I -B $S/headlatest/registry.py --root {L} --freeze {F4} --rev HEAD   # HEAD resolved 49e6cac4"),
 "latest-attest-selftest.stdout": ("0", f"python3 -I -B $S/headlatest/attest.py --root {L} --freeze {FZ} --rev {FZ} --selftest"),
 "latest-registry-selftest.stdout": ("0", f"python3 -I -B $S/headlatest/registry.py --root {L} --freeze {FZ} --rev {FZ} --selftest"),
 "latest-attest-v1.stdout": ("0", f"python3 -I -B $S/headlatest/attest.py --root {L} --freeze {F4} --rev HEAD --profile v1   # reconstructs the absent ctl-c1-1-v1-profile"),
 "head-attest-freeze318.stdout": ("2", f"python3 -I -B $S/head/attest.py --root {L} --freeze {FZ} --rev HEAD   # HEAD resolved 49e6cac4; pre-F4 attest bytes (same as F3)"),
 "head-registry-freeze318.stdout": ("2", f"python3 -I -B $S/head/registry.py --root {L} --freeze {FZ} --rev HEAD   # HEAD resolved 49e6cac4; pre-F4 registry bytes"),
 "head-attest-v1.stdout": ("2", f"python3 -I -B $S/head/attest.py --root {L} --freeze {F3} --rev HEAD --profile v1   # HEAD resolved 49e6cac4; frozen_path_changed by F4"),
}


CMDS.update({
 "final-attest-green.stdout": ("0", f"python3 -I -B $S/headlatest/attest.py --root {L} --freeze {F4} --rev HEAD   # HEAD resolved 21b55a8f"),
 "final-registry-green.stdout": ("0", f"python3 -I -B $S/headlatest/registry.py --root {L} --freeze {F4} --rev HEAD   # HEAD resolved 21b55a8f"),
 "final-attest-freeze318.stdout": ("2", f"python3 -I -B $S/headlatest/attest.py --root {L} --freeze {FZ} --rev HEAD   # HEAD resolved 21b55a8f"),
 "final-registry-freeze318.stdout": ("2", f"python3 -I -B $S/headlatest/registry.py --root {L} --freeze {FZ} --rev HEAD   # HEAD resolved 21b55a8f"),
})

rows = []
for name in sorted(os.listdir(S)):
    if not name.endswith(".stdout"):
        continue
    path = os.path.join(S, name)
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    mtime = datetime.datetime.fromtimestamp(os.path.getmtime(path),
                                            datetime.timezone.utc)
    rc, cmd = CMDS.get(name, ("?", "UNRECORDED"))
    if "$FIXTURE" in cmd:
        cmd = cmd.replace("$FIXTURE_REV", FIX or "?").replace(
            "$FIXTURE", os.path.join(S, "fixture-reg"))
    rows.append((mtime.strftime("%Y-%m-%dT%H:%M:%SZ"), cmd, rc, sha, name))

print("utc\tcommand\texit\tstdout_sha256\treceipt_file")
for r in sorted(rows):
    print("\t".join(r))
