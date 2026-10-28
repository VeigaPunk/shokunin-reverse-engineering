import os, sys, shutil
argv = sys.argv[1:]
fixture, outdir = argv[-2], argv[-1]
cid = {'v1-le--squashfs_v1.0_le.bin': 'v1le', 'v1-be--squashfs_v1.0_be.bin': 'v1be',
       'v2-le--squashfs_v2.0_le.bin': 'v2le', 'v2-be--squashfs_v2.0_be.bin': 'v2be'}[os.path.basename(fixture)]
src = '/fast/scratch/hyaku/kaidoku-r49/C1RunMut/evid-base/' + cid
os.makedirs(outdir, exist_ok=True)
shutil.copytree(src + '/firmware.bin_extract', os.path.join(outdir, 'firmware.bin_extract'), symlinks=True)
sys.stdout.buffer.write(open(src + '/stdout.log', 'rb').read())
