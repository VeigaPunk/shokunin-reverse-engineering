#!/usr/bin/env python3
"""Classify a SquashFS v4 image by LAYOUT, not by the AVM marker.
Reads: magic, superblock (big- or little-endian by magic), marker, and the first
2-byte metadata block-length header at inode_table_start decoded both ways.
The layout discriminator is the identity len + inode_table_start + 2 == directory_table_start,
which holds only in the block-length header's true byte order. Exit 0 on a decisive
class, 1 when undecidable (two metadata blocks with no identity fit).
"""
import sys, struct

def be(b,o,n): return int.from_bytes(b[o:o+n],'big')
def le(b,o,n): return int.from_bytes(b[o:o+n],'little')

def classify(path):
    b=open(path,'rb').read()
    magic=b[:4]
    if magic==b'sqsh': sb_ord='big'
    elif magic==b'hsqs': sb_ord='little'
    else: return {'image':path,'error':'not squashfs v4','magic':magic.hex()}
    rd=(lambda o,n: be(b,o,n)) if sb_ord=='big' else (lambda o,n: le(b,o,n))
    if rd(28,2)!=4: return {'image':path,'error':'not v4','version':rd(28,2)}
    mkfs=rd(8,4); used=rd(40,8); its=rd(64,8); dts=rd(72,8)
    hdr=b[its:its+2] if its+2<=len(b) else b''
    len_le=le(hdr,0,2)&0x7fff if len(hdr)==2 else None
    len_be=be(hdr,0,2)&0x7fff if len(hdr)==2 else None
    fits=[('LE',len_le),('BE',len_be)]
    ok=[name for name,v in fits if v is not None and its+2+v==dts]
    return {'image':path.split('/')[-1],'bytes':len(b),'magic':magic.decode(),
            'superblock_fields':sb_ord,'compression':rd(20,2),'marker':mkfs==used,
            'mkfs_time':mkfs,'bytes_used':used,'inode_table_start':its,'dir_table_start':dts,
            'meta_hdr':hdr.hex(),'len_le':len_le,'len_be':len_be,'identity_fit':ok,
            'layout':'AVM-BE (BE superblock, LE block lengths)' if ok==['LE'] and sb_ord=='big'
                     else 'standard BE (BE block lengths)' if ok==['BE'] and sb_ord=='big'
                     else 'LE' if sb_ord=='little' else 'ambiguous'}

if __name__=='__main__':
    rc=0
    for p in sys.argv[1:]:
        r=classify(p)
        for k,v in r.items(): print(f'{k}\t{v}')
        print()
        if r.get('layout')=='ambiguous' or 'error' in r: rc=1
    sys.exit(rc)
