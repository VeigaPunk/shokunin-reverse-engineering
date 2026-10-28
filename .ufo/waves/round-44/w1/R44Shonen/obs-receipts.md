# R44Shonen observation receipts — round 44 wave 1 (pre-freeze)

Lane HEAD `f5fb8d590f0dd6afc0847e1a63e8a3953bef8717`. Base per claims `c29360e3`. Observations only; no claim score.

## v1-le--squashfs_v1.0_le
$ ['/usr/bin/unsquashfs', '-s', 'corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin']
exit 0 wall 0.001s stdout_sha256 eb50a21a0978be5ceae71818bfe69d355561ab7478b4baf5c213e77c54f5c8b4
Found a valid little endian SQUASHFS 1:0 superblock on corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1.0_le.bin.
Creation or last append time Mon Aug  5 04:18:51 2024
Filesystem size 176 bytes (0.17 Kbytes / 0.00 Mbytes)
Block size 32768
Filesystem is not exportable via NFS
Inodes are compressed
Data is compressed
Check data is not present in the filesystem
Duplicates are removed
Number of inodes 4
Number of uids 1
Number of gids 0

## v1-be--squashfs_v1.0_be
$ ['/usr/bin/unsquashfs', '-s', 'corpus/evidence/round-42/c2/fixtures/v1-be--squashfs_v1.0_be.bin']
exit 0 wall 0.001s stdout_sha256 8a1f5952abe9d3670f947641b3a50cafcbf6d9818c6e934961f8d1ffb2812162
Found a valid big endian SQUASHFS 1:0 superblock on corpus/evidence/round-42/c2/fixtures/v1-be--squashfs_v1.0_be.bin.
Creation or last append time Mon Aug  5 04:18:58 2024
Filesystem size 177 bytes (0.17 Kbytes / 0.00 Mbytes)
Block size 32768
Filesystem is not exportable via NFS
Inodes are compressed
Data is compressed
Check data is not present in the filesystem
Duplicates are removed
Number of inodes 4
Number of uids 1
Number of gids 0

## v2-le--squashfs_v2.0_le
$ ['/usr/bin/unsquashfs', '-s', 'corpus/evidence/round-42/c2/fixtures/v2-le--squashfs_v2.0_le.bin']
exit 0 wall 0.001s stdout_sha256 f4c8a99c53081b07aee8523e0360c0c616237a16cbaea29ef7ab1ccdc003715a
Found a valid little endian SQUASHFS 2:0 superblock on corpus/evidence/round-42/c2/fixtures/v2-le--squashfs_v2.0_le.bin.
Creation or last append time Thu Mar  9 14:05:52 2023
Filesystem size 196 bytes (0.19 Kbytes / 0.00 Mbytes)
Block size 65536
Filesystem is not exportable via NFS
Inodes are compressed
Data is compressed
Fragments are compressed
Always-use-fragments option is not specified
Check data is not present in the filesystem
Duplicates are removed
Number of fragments 1
Number of inodes 5
Number of uids 1
Number of gids 0

## v2-be--squashfs_v2.0_be
$ ['/usr/bin/unsquashfs', '-s', 'corpus/evidence/round-42/c2/fixtures/v2-be--squashfs_v2.0_be.bin']
exit 0 wall 0.001s stdout_sha256 e077bb2ab17d7368b5ba3dedffb5122142391c1b051e37716aa08937eb8e0496
Found a valid big endian SQUASHFS 2:0 superblock on corpus/evidence/round-42/c2/fixtures/v2-be--squashfs_v2.0_be.bin.
Creation or last append time Thu Mar  9 14:06:30 2023
Filesystem size 201 bytes (0.20 Kbytes / 0.00 Mbytes)
Block size 65536
Filesystem is not exportable via NFS
Inodes are compressed
Data is compressed
Fragments are compressed
Always-use-fragments option is not specified
Check data is not present in the filesystem
Duplicates are removed
Number of fragments 1
Number of inodes 5
Number of uids 1
Number of gids 0

## superblock decode (unblob v1/v2 C_DEFINITIONS offsets)
$ ['python3', '-I', '-B', '-c', '\nimport struct,sys,json\nout={}\nfor f,e in [("v1-le--squashfs_v1.0_le","<"),("v1-be--squashfs_v1.0_be",">"),("v2-le--squashfs_v2.0_le","<"),("v2-be--squashfs_v2.0_be",">")]:\n    b=open("corpus/evidence/round-42/c2/fixtures/%s.bin"%f,"rb").read()\n    out[f]={"magic":b[:4].decode("latin-1"),"inodes@4":struct.unpack(e+"I",b[4:8])[0],\n            "bytes_used@8":struct.unpack(e+"I",b[8:12])[0],\n            "inode_table_start@20":struct.unpack(e+"I",b[20:24])[0],\n            "s_major@28":struct.unpack(e+"H",b[28:30])[0],"s_minor@30":struct.unpack(e+"H",b[30:32])[0],\n            "file_size":len(b)}\nprint(json.dumps(out,indent=1))\n']...
exit 0 wall 0.016s stdout_sha256 7fbd78de7d61579bba012513ddfe4fde84cbb5a5695073666d311f3242e79e2b
{
 "v1-le--squashfs_v1.0_le": {
  "magic": "hsqs",
  "inodes@4": 4,
  "bytes_used@8": 176,
  "inode_table_start@20": 71,
  "s_major@28": 1,
  "s_minor@30": 0,
  "file_size": 4096
 },
 "v1-be--squashfs_v1.0_be": {
  "magic": "sqsh",
  "inodes@4": 4,
  "bytes_used@8": 177,
  "inode_table_start@20": 71,
  "s_major@28": 1,
  "s_minor@30": 0,
  "file_size": 4096
 },
 "v2-le--squashfs_v2.0_le": {
  "magic": "hsqs",
  "inodes@4": 5,
  "bytes_used@8": 196,
  "inode_table_start@20": 88,
  "s_major@28": 2,
  "s_minor@30": 0,
  "file_size": 4096
 },
 "v2-be--squashfs_v2.0_be": {
  "magic": "sqsh",
  "inodes@4": 5,
  "bytes_used@8": 201,
  "inode_table_start@20": 88,
  "s_major@28": 2,
  "s_minor@30": 0,
  "file_size": 4096
 }
}

## carrier pins vs carriers.json
$ ['python3', '-I', '-B', '-c', '\nimport json,hashlib\nd=json.load(open("tools/round-44/carriers.json"))\nfor c in d["carriers"]:\n    h=hashlib.sha256(open(c["path"],"rb").read()).hexdigest()\n    print(c["id"], c["handler"], c["endian"], "declared_compression="+c["compression"],\n          "pin_match="+str(h==c["sha256"]).lower(), h)\n']...
exit 0 wall 0.018s stdout_sha256 d46013df19ed04b2092495a269811ba60d2a156a3f41b5acba6c891831e17218
v1le squashfs_v1 le declared_compression=gzip pin_match=true b45925fa779eae0293635ce0e6dc8760308f25227dd88645d677ba3ffce23e71
v1be squashfs_v1 be declared_compression=gzip pin_match=true 529e10775cc152e6c5df0c6c63316811004cc73ce99f03989c86ffd396d631e6
v2le squashfs_v2 le declared_compression=gzip pin_match=true 7c62dbe388b972119f5d17a12836a016737d58276184f4caa2a90dafd924f124
v2be squashfs_v2 be declared_compression=gzip pin_match=true 79c0f3886291f4abcc656acd49932446cf16afaa67e6ffb0c5258e3c2e2dfcc0


## v2ns refusal (retained Frontier verification)
- v2ns-le--squashfs_v2.0_le unsquashfs: exit 1 wall 0.001s stdout_sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  $( /usr/bin/unsquashfs -s corpus/evidence/round-42/c2/fixtures/v2ns-le--squashfs_v2.0_le.bin )
  stderr_first: FATAL ERROR: Can't find a valid SQUASHFS superblock on corpus/evidence/round-42/c2/fixtures/v2ns-le--squashfs_v2.0_le.bi
- v2ns-le--squashfs_v2.0_le 7z: exit 2 wall 0.002s stdout_sha256 4326f46701576d235d30e66c6110c817dca8fec351321ce46f31159ebb7e3fad
  $( 7z l corpus/evidence/round-42/c2/fixtures/v2ns-le--squashfs_v2.0_le.bin )
  stderr_first: ERROR: corpus/evidence/round-42/c2/fixtures/v2ns-le--squashfs_v2.0_le.bin : Cannot open the file as archive
- v2ns-be--squashfs_v2.0_be unsquashfs: exit 1 wall 0.001s stdout_sha256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
  $( /usr/bin/unsquashfs -s corpus/evidence/round-42/c2/fixtures/v2ns-be--squashfs_v2.0_be.bin )
  stderr_first: FATAL ERROR: Can't find a valid SQUASHFS superblock on corpus/evidence/round-42/c2/fixtures/v2ns-be--squashfs_v2.0_be.bi
- v2ns-be--squashfs_v2.0_be 7z: exit 2 wall 0.003s stdout_sha256 160b059c55372630b6db33f69581e8dfe2e2c220ce118f680bdc0a82fb1bd9b8
  $( 7z l corpus/evidence/round-42/c2/fixtures/v2ns-be--squashfs_v2.0_be.bin )
  stderr_first: ERROR: corpus/evidence/round-42/c2/fixtures/v2ns-be--squashfs_v2.0_be.bin : Cannot open the file as archive
- 7z identity: exit 0 stdout_sha256 1fc75706498ddeea4ae822a1d9d6561bdca640cbbc06db4e3a5cb1e3f8a80c8d
  first lines: 7-Zip 26.04 (x64) : Copyright (c) 1999-2026 Igor Pavlov : 2026-10-05


## carriers.json at HEAD (post-advance) — 6 carriers, v2.1 added
carriers.json sha256 = 2f61554e8d7ba631998982d6df79ed5cd6b1ff5ee2c32f946ccc62926e532278
carrier ids: ['v1le', 'v1be', 'v2le', 'v2be', 'v21le', 'v21be']  (draft froze 4; frozen file has 6)
- v1le squashfs_v1 le pin_match=True comp_declared=gzip regular_files=3 expected_regular=3 unsquashfs_s_exit=0 lls_exit=0 verdict=Found a valid little endian SQUASHFS 1:0 superblock on corpus/evidence/round-42/c2/fixtures/v1-le--squashfs_v1
- v1be squashfs_v1 be pin_match=True comp_declared=gzip regular_files=3 expected_regular=3 unsquashfs_s_exit=0 lls_exit=0 verdict=Found a valid big endian SQUASHFS 1:0 superblock on corpus/evidence/round-42/c2/fixtures/v1-be--squashfs_v1.0_
- v2le squashfs_v2 le pin_match=True comp_declared=gzip regular_files=4 expected_regular=4 unsquashfs_s_exit=0 lls_exit=0 verdict=Found a valid little endian SQUASHFS 2:0 superblock on corpus/evidence/round-42/c2/fixtures/v2-le--squashfs_v2
- v2be squashfs_v2 be pin_match=True comp_declared=gzip regular_files=4 expected_regular=4 unsquashfs_s_exit=0 lls_exit=0 verdict=Found a valid big endian SQUASHFS 2:0 superblock on corpus/evidence/round-42/c2/fixtures/v2-be--squashfs_v2.0_
- v21le squashfs_v2 le pin_match=True comp_declared=gzip regular_files=4 expected_regular=4 unsquashfs_s_exit=0 lls_exit=0 verdict=Found a valid little endian SQUASHFS 2:1 superblock on corpus/evidence/round-44/carriers/squashfs_v2.1_le.bin.
- v21be squashfs_v2 be pin_match=True comp_declared=gzip regular_files=4 expected_regular=4 unsquashfs_s_exit=0 lls_exit=0 verdict=Found a valid big endian SQUASHFS 2:1 superblock on corpus/evidence/round-44/carriers/squashfs_v2.1_be.bin.; I


## mined-mistake red receipt (observed at 08:16, 9a8de923053978342fdba6ce047e1cca4eda9dd2)
- path `.ufo/waves/round-44/l1/probe-fixture-404.txt`
- size 14 bytes, mtime 2026-10-28T11:16:47Z
- sha256 d5558cd419c8d46bdc958064cb97f963d1ea793866414c025906ec15033512ed
- content (repr) b'404: Not Found'
- attributes recorded: none (no URL, status line, timestamp or command in the file)
