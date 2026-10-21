#!/usr/bin/env python3
"""Read-only inspection of committed candidate bytes (OriginalPublic lane, R23-C1 source review).

Inputs (paths only; no producer, no sigrok, no network):
  argv[1] = hello_world_8n1_9600.sr  (bytes extracted with git show at 2838351450ff1ee4baa620c962a1153450d53311)
  argv[2] = decode-official-uart.envelope.json (same commit)

Independently decodes channel TX (= sigrok session 'probe1', bit 0) as 8N1 at 9600 baud,
reproduces the envelope annotation text, and reports framing, window and gap facts.
"""
import hashlib
import io
import json
import math
import re
import sys
import zipfile
from collections import Counter

sr_path, env_path = sys.argv[1], sys.argv[2]
sr_raw = open(sr_path, 'rb').read()
env_raw = open(env_path, 'rb').read()
out = {'sr_sha256': hashlib.sha256(sr_raw).hexdigest(), 'sr_bytes': len(sr_raw),
       'envelope_sha256': hashlib.sha256(env_raw).hexdigest()}

z = zipfile.ZipFile(io.BytesIO(sr_raw))
meta = z.read('metadata').decode()
logic = z.read('logic-1')
N = len(logic)
rate = 625000.0
bw = rate / 9600.0
out['metadata'] = meta.strip().splitlines()
out['logic_samples'] = N

# channel activity: which bit of each sample toggles
active = {}
for b in range(8):
    s = logic.translate(bytes(((i >> b) & 1) + 48 for i in range(256)))
    active[b] = len(re.findall(rb'0+|1+', s))
out['runs_per_bit'] = active

lvl = bytes(x & 1 for x in logic)           # bit 0 == probe1 == TX
ascii0 = logic.translate(bytes(((i & 1) + 48) for i in range(256)))
falls = [m.start() + 1 for m in re.finditer(rb'10', ascii0)]

frames = []
last_end = -1.0
for s0 in falls:
    if s0 < last_end:
        continue
    bits = []
    for k in range(10):
        p = math.ceil(s0 + (bw - 1) / 2 + k * bw)   # decoder sample point convention (uart pd.py get_sample_point)
        bits.append(None if p >= N else int(lvl[p]))
    val = sum((bits[k + 1] << k) for k in range(8) if bits[k + 1] is not None)
    frames.append({'s0': s0, 'byte': val, 'start': bits[0], 'stop': bits[9]})
    last_end = s0 + 9.5 * bw
out['frames'] = len(frames)
out['frame_error_frames'] = [
    {'index': i, 'byte': '%02X' % f['byte'], 's0': f['s0'], 'stop_value': f['stop']}
    for i, f in enumerate(frames) if f['stop'] == 0]
out['incomplete_last_frame'] = {
    'byte': '%02X' % frames[-1]['byte'], 's0': frames[-1]['s0'],
    'stop_sample': math.ceil(frames[-1]['s0'] + (bw - 1) / 2 + 9 * bw), 'recording_end': N}

# reproduce annotation text (decoder convention: ann_start = ceil(sp_bit0) - floor(bw/2); ann_end = ceil(sp_bit7) + ceil(bw/2))
env = json.loads(env_raw)
at = env['data']['normalized_result']['annotations_text']
lines = [l for l in at.split('\n') if l]
pat = re.compile(r'^(\d+)-(\d+) uart-1: ([0-9A-F]{2})$')
parsed = [pat.match(l) for l in lines]
out['annotation_lines'] = len(lines)
out['annotation_lines_all_rx_data_form'] = all(parsed)
mism = 0
for f, m in zip(frames, parsed):
    s0 = f['s0']
    ss = math.ceil(s0 + (bw - 1) / 2 + bw) - math.floor(bw / 2)
    es = math.ceil(s0 + (bw - 1) / 2 + 8 * bw) + math.ceil(bw / 2)
    if (ss, es, f['byte']) != (int(m.group(1)), int(m.group(2)), int(m.group(3), 16)):
        mism += 1
out['annotation_reproduction_mismatches'] = mism

# leading group and timing
def max_resid(s0):
    lo, hi = max(0, int(s0) - 2), min(N - 1, int(s0 + 10 * bw) + 2)
    seg = lvl[lo:hi + 1]
    worst, prev = 0.0, seg[0]
    for j in range(1, len(seg)):
        if seg[j] != prev:
            k = (lo + j - s0) / bw
            worst = max(worst, abs(k - round(k)) * bw)
            prev = seg[j]
    return worst
out['leading8_max_edge_residual_samples'] = round(max(max_resid(f['s0']) for f in frames[:8]), 2)
out['stream_max_edge_residual_samples'] = round(max(max_resid(f['s0']) for f in frames[:-1]), 2)
gaps = [round((frames[i + 1]['s0'] - frames[i]['s0']) / bw) for i in range(len(frames) - 1)]
out['gap_bit_times_counter'] = dict(Counter(gaps))
out['non10_gap_indices'] = [i for i, g in enumerate(gaps) if g != 10]
out['leading8'] = ['%02X%s' % (f['byte'], '(FE)' if f['stop'] == 0 else '') for f in frames[:8]]

# stream after leading group + CRLF
tail = bytes(f['byte'] for f in frames[8:])
pat_b = b'Hello World!\r\n'
reps = len(tail) // len(pat_b)
out['tail_full_repeats'] = reps
out['tail_exact_repeats'] = all(tail[i * 14:(i + 1) * 14] == pat_b for i in range(reps))
out['tail_remainder'] = tail[reps * 14:].decode()

print(json.dumps(out, indent=1, sort_keys=True))
