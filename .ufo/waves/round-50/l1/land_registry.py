#!/usr/bin/env python3
"""L1 landing step 2 (round 50): SKILL.md instrument-registry rows for tools/round-49 (six) and
tools/round-50 (six) paths, inserted before the marker closer. Refuses to run twice."""
import re

L = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
sk = open(L + '/SKILL.md', encoding='utf8').read()
CLOSE = '<!-- /instrument-registry -->'
assert sk.count(CLOSE) == 1 and '`tools/round-50/c1-counter.py`' not in sk
OK = lambda s: s

def row(path, purpose, verdict, selftest, pinned, scope):
    return '| `%s` | %s | %s | %s | %s | %s | kaidoku |' % (path, purpose, verdict, selftest, pinned, scope)

V_GATE = ('0=met, every clause true at --rev (and, where a battery exists, a clean battery); 1=not met, a named clause or binding false; '
          '2=could-not-evaluate, bad arguments, unknown revision, frozen_path_changed, counter_not_frozen, a rerun environment error or a refusal')
V_PROBE = ('0=ok, the run completed and every arm agreed; 1=failed, a clause, an oracle comparison or a run did not hold; '
           '2=could-not-evaluate, usage error, missing fixture or tool, or an environment refusal')
rows = [
    row('tools/round-49/c1-counter.py',
        'gate — R49-C1 coverage: SquashFS v1/v2 through REA extract-firmware on four carriers (receipts, oracle, gap rule, rerun projection, documentation bindings), run as `python3 -I -B tools/round-49/c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 PKG`',
        V_GATE, 'python3 -I -B tools/round-49/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root> (52 cases per the round-49 wave-2 seat W2C1Selftest)',
        'tools/round-49/carriers.json and the freeze pins', '--json-out and a private scratch under $HYAKU_SCRATCH/kaidoku-r49/counter'),
    row('tools/round-49/c1-controls.py',
        'probe — R49-C1 counterfactual control driver: plants control trees in shared-clone sandboxes and scores the frozen counter, run as `python3 -I -B tools/round-49/c1-controls.py`',
        V_PROBE, 'python3 -I -B tools/round-49/c1-controls.py --selftest (stub counter, driver machinery only)',
        'tools/round-49/control-fixtures/**', '--out and --json-out; sandbox clones under --work; never the lane'),
    row('tools/round-49/c1-oracle.py',
        'probe — R49-C1 frozen oracle builder: unsquashfs 4.7.5 census, per-file sha256 and the unblob __output__ second reading per carrier, run as `python3 -I -B tools/round-49/c1-oracle.py`',
        V_PROBE, 'python3 -I -B tools/round-49/c1-oracle.py --selftest',
        'tools/round-49/carriers.json (per-carrier oracle block)', '--work, --json-out and --receipt only'),
    row('tools/round-49/c1-run.py',
        'probe — R49-C1 after-freeze data runner: REA extract-firmware per carrier into corpus/evidence/round-49/c1/<id>/, run as `python3 -I -B tools/round-49/c1-run.py --dry-run` (a dry run writes nothing)',
        V_PROBE, 'none — no --selftest flag exists; --dry-run is the only no-write mode',
        'tools/round-49/carriers.json', 'the round-49 evidence root only under --data-run; scratch $HYAKU_SCRATCH/kaidoku-r49'),
    row('tools/round-49/c1-run.sh',
        'probe — wrapper around c1-run.py that pins the child PATH and scratch base, run as `bash tools/round-49/c1-run.sh --dry-run`',
        V_PROBE, 'none — no self-test; the wrapper passes --help and --dry-run to c1-run.py',
        'tools/round-49/carriers.json', 'as c1-run.py'),
    row('tools/round-49/c2-mismatch.py',
        'gate — R49-C2 calibration: nine round-48 atoms A1..A9 re-derived from committed bytes, run as `python3 -I -B tools/round-49/c2-mismatch.py --root LANE --rev REV --freeze FREEZE --battery`',
        V_GATE, 'none — the file has no --selftest flag; the hermetic self-test is python3 -I -B tools/round-50/selftest-r49-c2.py --lane . (40 cases)',
        'none — the pinned values are the LANE_BASE, R48_BASE and R48_TIP constants in the source', '--json-out only'),
    row('tools/round-50/c1-counter.py',
        'gate — R50-C1 coverage: genuine AVM-marker little-endian SquashFS v4 (hsqs) members of four FRITZ!OS images through REA extract-firmware (receipts, oracle re-derivation, gap/removal rule, parameters, rerun projection on the pinned REA package, documentation bindings), run as `python3 -I -B tools/round-50/c1-counter.py --root LANE --rev REV --freeze FREEZE --pkg65 PKG --carrier-cache CACHE`',
        V_GATE, 'python3 -I -B tools/round-50/c1-counter.py --selftest --pkg65 <rea-agents 6.5.0 root> — 169 cases, exit 0 on 2026-10-28',
        'tools/round-50/carriers.json, gap-rule.json and oracle/** frozen at the freeze', '--json-out and a private scratch under $HYAKU_SCRATCH/kaidoku-r50/counter'),
    row('tools/round-50/c1-run.sh',
        'probe — R50-C1 run harness: arm `after` runs REA extract-firmware on a carved carrier and writes the receipt, arm `oracle` derives the oracle with three readers, run as `bash tools/round-50/c1-run.sh after --id ID --carrier FILE --data-run`',
        V_PROBE, 'none — no self-test; the oracle arm cross-checks three independent readers and exits 3 on disagreement',
        'tools/round-50/carriers.json', 'corpus/evidence/round-50/c1/<id>/ only under --data-run; scratch $HYAKU_SCRATCH/kaidoku-r50'),
    row('tools/round-50/c1-controls.py',
        'probe — R50-C1 control driver: gen builds and score plants the committed control fixtures (do-nothing, round-41 BE receipts, oracle forgery, sasquatch absent, standard LE carrier, positive) and scores the frozen counter, run as `python3 -I -B tools/round-50/c1-controls.py score --lane LANE --freeze FREEZE`',
        V_PROBE, 'python3 -I -B tools/round-50/c1-controls.py selftest --work DIR (positional spelling, no --selftest flag; 20 cases, exit 0 on 2026-10-28)',
        'tools/round-50/control-fixtures/** (manifest sha256 per file)', '--out and --json-out; sandbox clones under --work; never the lane'),
    row('tools/round-50/fetch-vendor.py',
        'probe — R50-C1 carrier custody: materialises the chain-pinned vendor carriers (image sha256, tar member, carve to bytes_used, carrier sha256) from download.avm.de only, run as `python3 -I -B tools/round-50/fetch-vendor.py --spec FILE --cache DIR`',
        V_PROBE, 'python3 -I -B tools/round-50/fetch-vendor.py --selftest — 16 cases, exit 0 on 2026-10-28',
        'tools/round-50/carriers.json', '--cache and --image-cache outside the lane only; refuses a lane-resident directory'),
    row('tools/round-50/c2-record.py',
        'gate — R50-C2 calibration: eleven round-48/49 record atoms B1..B11 re-derived from committed bytes with a single-mutation battery, run as `python3 -I -B tools/round-50/c2-record.py --root LANE --rev REV --freeze FREEZE --battery`',
        V_GATE, 'python3 -I -B tools/round-50/c2-record.py --selftest --root . — 29 cases, exit 0 on 2026-10-28',
        'none — the pinned values are the BASE and R48_TIP constants in the source', '--json-out and a scratch under --work or TMPDIR only'),
    row('tools/round-50/selftest-r49-c2.py',
        'gate — hermetic self-test of the frozen round-49 counter c2-mismatch.py over fixture clones of the real history (40 cases), run as `python3 -I -B tools/round-50/selftest-r49-c2.py --lane LANE`',
        V_GATE, 'none — this file is the self-test; --mutant-counter PATH judges a mutant counter and exits 1 when it is caught',
        'tools/round-50/selftest-r49-c2.expected.json (hand-written expected values, counter sha256 pinned)', '--work and --json-out outside the lane only'),
]
for r in rows:
    assert r.count('|') == 8, r.count('|')
sk = sk.replace(CLOSE, '\n'.join(rows) + '\n' + CLOSE, 1)
open(L + '/SKILL.md', 'w', encoding='utf8').write(sk)
print('registry rows added', len(rows))
