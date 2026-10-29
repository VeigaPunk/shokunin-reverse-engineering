#!/usr/bin/env python3
# Probe 1 (unit): the round-41 counter's make_real_runner inherits PATH. A PATH-first `npx`
# shim answers the rerun; REA is never executed. The shim maps the carrier's sha256 to the
# committed round-49 receipt (v1le) and prints it as the rerun envelope.
# Probe 2 (marker): a lane-built standard LE carrier (round-36 K1, mkfs_time 0) with
# mkfs_time := bytes_used passes every superblock sub-clause of the AVM marker.
# Run: python3 rerun_binding_probe.py  -> $S/unit-and-marker.json
# Requires the shim dir from rigged_rerun_r49.py ($S/rigged/shimbin/npx) and its rec-v1le.json.
import os, subprocess, json, hashlib, shutil, importlib.util, struct
LANE = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin'
S = '/fast/scratch/hyaku/kaidoku-r50/C1ShortcutCritic'
RG = os.path.join(S, 'rigged'); shim = os.path.join(RG, 'shimbin')
out = {}
shutil.copy(os.path.join(LANE, 'tools/round-41/c1-counter.py'), os.path.join(S, 'r41counter.py'))
spec = importlib.util.spec_from_file_location('r41c', os.path.join(S, 'r41counter.py'))
r41 = importlib.util.module_from_spec(spec); spec.loader.exec_module(r41)
carrier = open(os.path.join(LANE, 'corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin'), 'rb').read()
csha = hashlib.sha256(carrier).hexdigest(); out['unit_carrier_sha256'] = csha
rec = os.path.join(RG, 'rec-v1le.json')
mp = os.path.join(S, 'unit-map.json'); json.dump({csha: rec}, open(mp, 'w'))
log = os.path.join(S, 'unit.argv.log')
if os.path.exists(log): os.remove(log)
os.environ['PATH'] = shim + ':' + os.environ['PATH']
os.environ['SHIM_MAP'] = mp; os.environ['SHIM_LOG'] = log
work = os.path.join(S, 'unit-work'); os.makedirs(work, exist_ok=True)
status, data = r41.make_real_runner(work, None, 120)(carrier, 'v1le', {'max_depth': 1})
out['runner_status'] = status
out['runner_data_is_committed_envelope'] = (data == json.load(open(rec))) if status == 'ok' else None
out['shim_invocations'] = open(log).read().splitlines()

def sb(b):
    magic, inodes, mkfs, bs, frag, comp, blog, flags, nid, maj, mnr = struct.unpack_from('<4sIIIIHHHHHH', b, 0)
    return dict(magic=magic.decode('latin1'), major=maj, minor=mnr, compression=comp,
                mkfs_time=mkfs, bytes_used=struct.unpack_from('<Q', b, 40)[0], size=len(b))

k1 = open(os.path.join(LANE, 'corpus/evidence/round-36/c1/fixtures/k1-le-xz.sqsh'), 'rb').read()
out['k1_sha256'] = hashlib.sha256(k1).hexdigest(); out['k1_superblock_before'] = sb(k1)
p = bytearray(k1); struct.pack_into('<I', p, 8, struct.unpack_from('<Q', k1, 40)[0] & 0xffffffff)
sbp = sb(bytes(p))
out['k1_patched_sha256'] = hashlib.sha256(bytes(p)).hexdigest(); out['k1_patched_superblock'] = sbp
out['k1_patched_marker_clause'] = (sbp['magic'] == 'hsqs' and sbp['major'] == 4 and sbp['minor'] == 0
                                   and sbp['mkfs_time'] == sbp['bytes_used'])
json.dump(out, open(os.path.join(S, 'unit-and-marker.json'), 'w'), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))
