# Development fixtures (unblob 26.6.4 test fixtures, MIT; never C1 carriers)

Base URL: https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/

| file | source path | sha256 |
|---|---|---|
| squashfs_v3_little_endian___input___squashfs_v3_le.bin | squashfs_v3/little_endian/__input__/squashfs_v3_le.bin | 0161351caec8e9da6e3e5ac7b046fd11d832efb18eb09e33011e6d19d50cd1f7 |
| squashfs_v3_big_endian___input___squashfs_v3_be.bin | squashfs_v3/big_endian/__input__/squashfs_v3_be.bin | 4e9493d9c6f868005dea8f11992129c3399e0bcb8f3a966c750cb925989ca97c |
| ddwrt-be.bin | squashfs_v3_ddwrt/big_endian/__input__/squashfs_v3.be.nopad.bin | daa8e72d355db1067a36bacd4b15853fb49ce7bb4fa6d6efafc0e7f09be8c9e1 (magic tqsh) |
| broadcom-le.bin | squashfs_v3_broadcom/little_endian/__input__/squashfs_v3_le.bin | 6baad4387dd51c8010de694420a35b6709706a268f7ba9e96e6417fb969f37d3 (magic shsq) |
| nonstd-le.bin | squashfs_v3_nonstandard/little_endian/__input__/squashfs_v3_le.bin | 3bce6ae378319fd2ac08c73ede9b3890a6d0f78c16392f09117cc3ffd70d1acb (magic zlqs) |

`truncated.bin` (8 B, magic only; F13 probe) is synthetic: `printf 'hsqs\x03\x00\x00\x00' > truncated.bin`.

The hsqs LE fixture and the ddwrt LE fixture served from the LFS path are byte-identical
(0161351c…); the real DD-WRT vendor magic is exercised by `ddwrt-be.bin` (tqsh, v3.1).
Nothing here is a C1 carrier.
