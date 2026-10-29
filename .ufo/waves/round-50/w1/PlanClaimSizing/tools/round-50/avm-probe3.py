#!/usr/bin/env python3
"""PlanClaimSizing probe (draft, wave 1): HTTP HEAD of the four frozen carrier URLs,
directory-index count of model dirs, and Range-only superblock reads for three models.
Prints one JSON object; header values kept only for Content-Length/Last-Modified/ETag/Content-Range.
No cookies or Set-Cookie are read or stored."""
import json, re, struct, sys, time, urllib.request, urllib.error
B = 'https://download.avm.de/fritzbox/'
KEEP = ('content-length', 'last-modified', 'etag', 'content-range', 'accept-ranges')
def req(url, method='GET', rng=None):
    r = urllib.request.Request(url, method=method, headers={'User-Agent': 'hyaku-r50-planclaimsizing/1'})
    if rng: r.add_header('Range', 'bytes=%d-%d' % rng)
    try:
        with urllib.request.urlopen(r, timeout=60) as resp:
            body = b'' if method == 'HEAD' else resp.read()
            hdrs = {k.lower(): v for k, v in resp.headers.items() if k.lower() in KEEP}
            return resp.status, hdrs, body
    except urllib.error.HTTPError as e:
        return e.code, {}, b''
def head(url):
    st, h, _ = req(url, 'HEAD'); return {'url': url, 'status': st, 'headers': h}
CARRIERS = {
 'a7530': 'fritzbox-7530/deutschland/fritz.os/FRITZ.Box_7530-08.25.image',
 'a7590': 'fritzbox-7590/deutschland/fritz.os/FRITZ.Box_7590-08.25.image',
 'c6490': 'fritzbox-6490-cable/deutschland/fritz.os/FRITZ.Box_6490_Cable-07.57.image',
 'c6430': 'fritzbox-6430-cable/deutschland/fritz.os/FRITZ.Box_6430_Cable-07.30.image',
}
def superblock(url):
    off = 0
    names = []
    for _ in range(60):
        st, _, hd = req(url, 'GET', (off, off + 511))
        if st not in (200, 206) or len(hd) < 512: return {'error': 'header-read', 'status': st, 'names': names}
        name = hd[:100].split(b'\0')[0].decode(errors='replace')
        size = int(hd[124:136].split(b'\0')[0].strip() or b'0', 8)
        names.append((name, size))
        if name.endswith('filesystem.image'):
            st2, _, d = req(url, 'GET', (off + 512, off + 512 + 47))
            e = '<' if d[:4] == b'hsqs' else '>'
            return {'member': name, 'member_offset': off + 512, 'member_size': size,
                    'magic': d[:4].decode(errors='replace'), 'endian': 'LE' if e == '<' else 'BE',
                    'major_minor': list(struct.unpack(e + 'HH', d[28:32])),
                    'compression_id': struct.unpack(e + 'H', d[20:22])[0],
                    'mkfs_time': struct.unpack(e + 'I', d[8:12])[0],
                    'bytes_used': struct.unpack(e + 'Q', d[40:48])[0],
                    'avm_marker_mkfs_eq_bytes_used': struct.unpack(e + 'I', d[8:12])[0] == struct.unpack(e + 'Q', d[40:48])[0],
                    'superblock_status': st2}
        off += 512 + ((size + 511) // 512) * 512
    return {'error': 'no-filesystem-member-within-60-headers', 'names': names[:10]}
out = {'utc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'carriers_head': {}, 'index': {}, 'models': {}}
for k, p in CARRIERS.items():
    out['carriers_head'][k] = head(B + p)
st, _, body = req(B, 'GET')
models = sorted(set(re.findall(r'href="(fritzbox-[^"/]+)/"', body.decode(errors='replace'))))
out['index'] = {'status': st, 'count_unique_model_dirs': len(models), 'sample_first5': models[:5], 'sample_last5': models[-5:]}
for m in sys.argv[1:]:
    loc = B + m + '/deutschland/fritz.os/'
    st, _, lb = req(loc, 'GET')
    imgs = re.findall(r'href="([^"]+\.image)"', lb.decode(errors='replace'))
    chosen = imgs[-1] if imgs else None
    rec = {'listing_status': st, 'image_files': imgs, 'scan_py_choice_last': chosen}
    if chosen:
        u = loc + chosen
        rec['head'] = head(u)
        rec['superblock'] = superblock(u)
    out['models'][m] = rec
print(json.dumps(out, indent=1, sort_keys=True))
