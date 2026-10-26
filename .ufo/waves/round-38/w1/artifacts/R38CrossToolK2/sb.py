import hashlib, json, struct, sys
C = '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-37/c1'
paths = {'K1': f'{C}/K1/carrier.sqsh', 'K2': f'{C}/K2/carrier.sqsh',
         'K3': f'{C}/K3/carrier.bin',  'K4': f'{C}/K4/carrier.bin'}
out = {}
for k, p in paths.items():
    raw = open(p, 'rb').read()
    sb = raw[:96]
    be = struct.unpack('>4sIIIIHHHHHHQQQQQQQQ', sb)
    le = struct.unpack('<4sIIIIHHHHHHQQQQQQQQ', sb)
    names = ['magic','inode_count','mkfs_time','block_size','fragments','compression',
             'block_log','flags','no_ids','s_major','s_minor','root_inode','bytes_used',
             'id_table_start','xattr_id_table_start','inode_table_start',
             'directory_table_start','fragment_table_start','lookup_table_start']
    d = dict(zip(names, be))
    out[k] = {
        'path': p, 'size': len(raw),
        'sha256': hashlib.sha256(raw).hexdigest(),
        'be': {n: (v.hex() if isinstance(v, bytes) else v) for n, v in zip(names, be)},
        'le_misread': {'magic': le[0].hex(), 's_major': le[9], 's_minor': le[10],
                       'inode_count': le[1]},
        'checks': {
            'magic_is_sqsh': be[0] == b'sqsh',
            'version_4_0': (be[9], be[10]) == (4, 0),
            'compressor_is_gzip(1)': be[5] == 1,
            'bytes_used_le_size': be[12] <= len(raw),
            'tail_padding': len(raw) - be[12],
            'table_starts_ascending': [be[15], be[16], be[13]] == sorted([be[15], be[16], be[13]]),
        },
    }
print(json.dumps(out, indent=1, sort_keys=True))
