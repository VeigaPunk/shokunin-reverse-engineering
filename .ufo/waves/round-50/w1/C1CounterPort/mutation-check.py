#!/usr/bin/env python3
"""Seat-local mutation check of the selftest (not a counter instrument).

Writes single-line mutants of the round-50 counter into a scratch directory, runs
`--selftest` on each (offline, ~2 min) and reports whether the selftest turns red.
A mutant that leaves the selftest green marks a clause the selftest does not
discriminate.

usage: python3 -I -B mutation-check.py COUNTER SCRATCH PKG65 [M1 M2 ...]
(requires SCRATCH/mut/tools/round-27/xpin-attribute.mjs, a copy of the lane's)
"""
import json, os, subprocess, sys

counter, scratch, pkg = sys.argv[1:4]
only = set(sys.argv[4:])
src = open(counter).read()
MUTANTS = {
    'M1-marker-not-required': ("    elif not d['marker']:\n        reason = 'AVM marker absent",
                               "    elif False:\n        reason = 'AVM marker absent"),
    'M2-compression-not-checked': ("    elif not d['compression_xz']:", "    elif False:"),
    'M3-magic-any': ("    if not d['le_magic']:\n        reason = 'magic",
                     "    if False:\n        reason = 'magic"),
    'M4-handler-prefix': ("    d['handler_ok'] = bool(d['squashfs_handlers']) and all(\n                    h == HANDLER for h in d['squashfs_handlers'])",
                          "    d['handler_ok'] = any(h.startswith('squashfs_v4') for h in d['squashfs_handlers'])"),
    'M5-extra-files-allowed': ("                                       and not extra)", "                                       and True)"),
    'M6-size-not-compared': ("if any(s == sha and z == want_size for s, z in idx.get(strip_rel(rel), [])):",
                             "if any(s == sha for s, z in idx.get(strip_rel(rel), [])):"),
    'M7-provenance-substring': ("    return output_directory.startswith(PROV_BASE)",
                                "    return PROV_SEGMENT in output_directory"),
    'M8-frontier-stem-token': ("and LE_AVM_RE.search(l.replace(STEM, ''))", "and LE_AVM_RE.search(l)"),
    'M9-params-not-bound': ("                                      and got_p == want_p)", "                                      and True)"),
    'M10-envelope-not-checked': ("d['evidence_envelope_ok'] = not ({'counter_sha256', 'exit_code'}\n                                                 & set(env))",
                                 "d['evidence_envelope_ok'] = True"),
    'M11-tables-order': ("    d['tables_sane'] = 0 < its < dts <= d['bytes_used']", "    d['tables_sane'] = True"),
    'M12-sasquatch-not-required': ("        if which_fixed('sasquatch') is None:", "        if False:"),
    'M13-drift-prefix': ("FROZEN_PREFIXES = ('tools/round-50/',)", "FROZEN_PREFIXES = ()"),
    # the two guards in diagnostic_rel are redundant with each other (under_root and
    # the segment-prefix test): disabling one is an equivalent mutant (measured: M14a
    # survives), disabling both is not
    'M14a-removal-root-one-guard': ("    if not under_root(link, trusted):\n        return None", "    if False:\n        return None"),
    'M14-removal-root-untrusted': ("    if not under_root(link, trusted):\n        return None\n    segs = [x for x in link.split('/') if x not in ('', '.')]\n    tsegs = [x for x in trusted.split('/') if x not in ('', '.')]\n    if segs[:len(tsegs)] != tsegs:\n        return None",
                                   "    segs = [x for x in link.split('/') if x not in ('', '.')]\n    tsegs = [x for x in trusted.split('/') if x not in ('', '.')]"),
    # round-50 additions from the wave-1 shortcut critique (S1, S3, S4, S5/S6, S11)
    'M15-adds-simplified-history': ("    p = git(root, 'log', '-m', '--full-history', '--diff-filter=A', '--format=%H',\n            rev, '--', path, check=False)",
                                    "    p = git(root, 'log', '--diff-filter=A', '--format=%H',\n            rev, '--', path, check=False)"),
    'M16-counter-not-frozen-off': ("    if frozen_counter is None or sha256_bytes(frozen_counter) != own_sha:", "    if False:"),
    'M17-oracle-rederive-always-ok': ("                d['oracle_rederived_ok'] = want_set == got_set\n", "                d['oracle_rederived_ok'] = True\n"),
    'M18-unblob-version-unbound': ("    if ver != UNBLOB_VERSION:", "    if False:"),
    'M19-sasquatch-ambient-path': ("    sas = which_fixed('sasquatch')\n    if sas is None:\n        raise RerunEnvError('missing-extractor-dependency: sasquatch is not '\n                            'on the fixed child PATH %r' % (FIXED_PATH,))\n    rec['sasquatch']",
                                   "    sas = shutil.which('sasquatch')\n    if sas is None:\n        raise RerunEnvError('missing-extractor-dependency: sasquatch is not '\n                            'on the fixed child PATH %r' % (FIXED_PATH,))\n    rec['sasquatch']"),
    'M20-projection-not-required': ("    if prof != DEFAULT_PROFILE:", "    if False:"),
    'M21-receipt-fresh-any': ("            d['receipt_fresh'] = bool(adds) and all(", "            d['receipt_fresh'] = bool(adds) and any("),
    'M22-runner-ambient-env': ("        env['PATH'] = FIXED_PATH\n        argv = [node, entry,", "        argv = [node, entry,"),
    'M23-rea-package-not-run': ("        argv = [node, entry, 'extract-firmware', '--format', 'json',", "        argv = ['npx', '-y', 'rea-agents@6.5.0', 'extract-firmware', '--format', 'json',"),
}
res = {}
for name, (old, new) in MUTANTS.items():
    if only and name.split('-')[0] not in only:
        continue
    n = src.count(old)
    if n != 1:
        res[name] = {'applied': False, 'occurrences': n}
        continue
    # the selftest locates tools/round-27/xpin-attribute.mjs relative to the counter:
    # mutants live in SCRATCH/mut/tools/ beside a copy of round-27/xpin-attribute.mjs
    d = os.path.join(scratch, 'mut', 'tools')
    os.makedirs(d, exist_ok=True)
    p = os.path.join(d, name.split('-')[0] + '.py')
    open(p, 'w').write(src.replace(old, new))
    work = os.path.join(scratch, 'mut', 'work-' + name.split('-')[0])
    os.makedirs(work, exist_ok=True)
    env = dict(os.environ, TMPDIR=scratch, HYAKU_SCRATCH='/fast/scratch/hyaku')
    r = subprocess.run([sys.executable, '-I', '-B', p, '--selftest', '--pkg65', pkg,
                        '--work', work], capture_output=True, text=True, env=env)
    fails = []
    try:
        doc = json.loads(r.stdout.strip().splitlines()[-1])
        fails = doc.get('failures') or []
    except Exception as e:  # noqa
        fails = ['unparseable: %s' % e]
    res[name] = {'applied': True, 'selftest_exit': r.returncode,
                 'killed': r.returncode != 0, 'failures': len(fails),
                 'first_failures': [f[:140] for f in fails[:3]]}
    print(name, json.dumps(res[name]), flush=True)
print(json.dumps(res, indent=1, sort_keys=True))
