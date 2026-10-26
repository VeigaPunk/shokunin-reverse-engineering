#!/usr/bin/env python3
import hashlib, json, os, shutil, struct, subprocess, sys, contextlib, io
sys.dont_write_bytecode = True
import importlib.util as _ilu
_spec = _ilu.spec_from_file_location('gen_squashfs', '/home/vgpnk/Projects/shokunin/kaidoku-shokunin/tools/round-41/gen-squashfs.py')
mod = _ilu.module_from_spec(_spec); _spec.loader.exec_module(mod); w = mod

S = '/fast/scratch/hyaku/kaidoku-r42/R42C2ReconCombo'
FIX = os.path.join(S, 'fixtures')
V3LE = open(os.path.join(FIX,'v3le.bin'),'rb').read()
V3BE = open(os.path.join(FIX,'v3be.bin'),'rb').read()
V3LE_DMG = V3LE[:96] + b'\x00'*(258-96) + V3LE[258:]
V3BE_DMG = V3BE[:96] + b'\x00'*(255-96) + V3BE[255:]

def sha(b): return hashlib.sha256(b).hexdigest()

def pattern(i, size=4096):
    head = f'combo-{i}:'.encode()
    return (head + bytes(range(48, 256)) * ((size // 208) + 1))[:size]

def mk_tree(root, files_links):
    if os.path.isdir(root): shutil.rmtree(root)
    os.makedirs(root, exist_ok=True)
    rec = {'files': [], 'links': []}
    for rel, kind, payload in files_links:
        p = os.path.join(root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if kind == 'file':
            with open(p,'wb') as f: f.write(payload)
            rec['files'].append((rel, sha(payload), len(payload)))
        elif kind == 'symlink':
            os.symlink(payload, p)
            rec['links'].append((rel, payload))
    return rec

def build_v4(mode, comp, tree, out):
    with contextlib.redirect_stdout(io.StringIO()):
        w.build_image(tree, out, mode, comp)
    b = open(out,'rb').read()
    assert b[:4] in (b'hsqs', b'sqsh')
    return b

def v4_zero_id(payload, endian):
    prefix = '>' if endian == 'be' else '<'
    id_table_start = struct.unpack(prefix + 'Q', payload[48:56])[0]
    id_meta_start = struct.unpack(prefix + 'Q', payload[id_table_start:id_table_start+8])[0]
    out = bytearray(payload)
    out[id_meta_start:id_table_start] = b'\x00' * (id_table_start - id_meta_start)
    return bytes(out)

def two_chunk(chunk1, chunk2):
    pad = (4096 - (len(chunk1) % 4096)) % 4096
    return chunk1 + b'\x00' * pad + chunk2

def write_carrier(name, body, meta):
    d = os.path.join(S, 'carriers', name)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'carrier.bin'), 'wb') as f:
        f.write(body)
    meta['sha256'] = sha(body)
    meta['size'] = len(body)
    with open(os.path.join(d, 'meta.json'), 'w') as f:
        json.dump(meta, f, indent=1, sort_keys=True)
    return meta

def main():
    os.makedirs(os.path.join(S,'carriers'), exist_ok=True)
    os.makedirs(os.path.join(S,'trees'), exist_ok=True)
    tr = os.path.join(S,'trees','v4le-intree')
    mk_tree(tr, [
        ('a.txt','file', pattern('v4le-intree-a')),
        ('link','symlink','a.txt'),
    ])
    v4le_intree = build_v4('le','gzip',tr, os.path.join(S,'trees','v4le-intree.sqsh'))

    tr = os.path.join(S,'trees','v4be-escaping')
    mk_tree(tr, [
        ('a.txt','file', pattern('v4be-escaping-a')),
        ('esc','symlink','../outside.txt'),
    ])
    v4be_escaping = build_v4('be','gzip',tr, os.path.join(S,'trees','v4be-escaping.sqsh'))

    tr = os.path.join(S,'trees','v4le-nested-v3')
    mk_tree(tr, [
        ('inner.sqsh','file', V3LE),
        ('a.txt','file', pattern('v4le-nested-a')),
    ])
    v4le_nested = build_v4('le','gzip',tr, os.path.join(S,'trees','v4le-nested-v3.sqsh'))

    tr = os.path.join(S,'trees','v4be-plain')
    mk_tree(tr, [
        ('a.txt','file', pattern('v4be-plain-a')),
    ])
    v4be_plain = build_v4('be','gzip',tr, os.path.join(S,'trees','v4be-plain.sqsh'))

    body = two_chunk(V3LE, v4le_intree)
    write_carrier('CB1', body, {
        'combo': 'legacy-twochunk-intree',
        'chunks': [
            {'offset':0, 'handler_expected':'squashfs_v3', 'role':'v3 LE clean fixture'},
            {'offset':4096, 'handler_expected':'squashfs_v4_le', 'role':'v4 LE in-tree symlink'},
        ],
        'max_depth': 3, 'arm': 'after',
    })

    write_carrier('CB2', v4le_nested, {
        'combo': 'legacy-nested-depth1',
        'chunks': [{'offset':0, 'handler_expected':'squashfs_v4_le', 'role':'v4 LE containing v3 fixture file'}],
        'max_depth': 1, 'arm': 'after',
    })
    write_carrier('CB3', v4le_nested, {
        'combo': 'legacy-nested-depth3',
        'chunks': [{'offset':0, 'handler_expected':'squashfs_v4_le', 'role':'v4 LE containing v3 fixture file'}],
        'max_depth': 3, 'arm': 'after',
    })

    write_carrier('CB4', V3BE, {
        'combo': 'legacy-depmiss-be',
        'chunks': [{'offset':0, 'handler_expected':'squashfs_v3', 'role':'v3 BE clean fixture'}],
        'max_depth': 3, 'arm': 'before',
    })

    body = two_chunk(V3LE, v4be_plain)
    write_carrier('CB5', body, {
        'combo': 'legacy-depmixed-v4be',
        'chunks': [
            {'offset':0, 'handler_expected':'squashfs_v3', 'role':'v3 LE clean fixture'},
            {'offset':4096, 'handler_expected':'squashfs_v4_be', 'role':'v4 BE plain'},
        ],
        'max_depth': 3, 'arm': 'before',
    })

    body = two_chunk(V3BE, v4be_escaping)
    write_carrier('CB6', body, {
        'combo': 'legacy-twochunk-escaping',
        'chunks': [
            {'offset':0, 'handler_expected':'squashfs_v3', 'role':'v3 BE clean fixture'},
            {'offset':4096, 'handler_expected':'squashfs_v4_be', 'role':'v4 BE escaping symlink'},
        ],
        'max_depth': 3, 'arm': 'after',
    })

    write_carrier('CB7', V3BE_DMG, {
        'combo': 'legacy-body-failure-be',
        'chunks': [{'offset':0, 'handler_expected':'squashfs_v3', 'role':'v3 BE metadata-zeroed'}],
        'max_depth': 3, 'arm': 'after',
    })
    write_carrier('CB8', V3LE_DMG, {
        'combo': 'legacy-body-failure-le',
        'chunks': [{'offset':0, 'handler_expected':'squashfs_v3', 'role':'v3 LE metadata-zeroed'}],
        'max_depth': 3, 'arm': 'after',
    })
    print('carriers written')

if __name__ == '__main__':
    main()
