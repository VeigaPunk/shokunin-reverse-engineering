import PySquashfsImage as sq
p='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/evidence/round-42/c2/fixtures/v2ns-le--squashfs_v2.0_le.bin'
try:
    img = sq.SquashFsImage(open(p,'rb'))
    print('OPENED', img)
    try:
        for c in img.root.children:
            print('MEMBER', c.name)
    except Exception as e2:
        print('WALKFAIL:', type(e2).__name__, e2)
except Exception as e:
    print('REFUSED:', type(e).__name__, e)
