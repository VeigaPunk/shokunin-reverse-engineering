# Provenance — R42SrcUnblob live opens (2026-10-26, UTC)

All fetches used `curl -sS` (raw.githubusercontent.com / media.githubusercontent.com) and
`urllib` (api.github.com). Timezone UTC. Each sha256 below is of the bytes actually received.

| # | URL | HTTP | bytes | sha256 | opened |
|---|---|---|---|---|---|
| D1 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py | 200 | 19842 | 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287 | 21:50:35Z (recheck 21:51:10Z, 200, 19842, same sha256) |
| D2 | https://api.github.com/repos/onekey-sec/unblob/git/trees/1fcc7a0a584a70a96c31f5a276c20944d199a089?recursive=1 | 200 | 1522052 | adb692a25b66718f9ed1dc237d87d72b4b6440a9a2f2ddbbb49e925df38b3ef2 | 21:50:43Z |
| D3 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/LICENSE | 200 | 1068 | 67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e | 21:50:35Z (recheck 21:51:10Z, 200, 1068, same sha256) |
| D4 | https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/.gitattributes | 200 | 158 | df86e28e5e3b04895438ccba79200a462d2e67daefd9042b5477d42b5b2ccede | 21:50:5xZ (recheck 21:51:10Z, 200, 158) |
| D5 | 58 x https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/tests/integration/filesystem/squashfs/.../__input__/*.bin | 200 each | 128-129 each | see fixtures-58.tsv `pointer_sha256` | 21:51:15Z-21:51:32Z |
| D6 | same 58 paths under https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/... | 200 each | 307-4096 each (total 161486) | see fixtures-58.tsv `actual_sha256`; every payload sha256 equals the pointer's LFS `oid` | 21:51:37Z-21:51:42Z |

D2 returned `"truncated": false`, so the 380 entries under `tests/integration/filesystem/squashfs`
are the complete subtree at that commit; 58 of them are `__input__` blobs.

Installed-copy identity check: the unblob 26.6.4 handler installed at
`/home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py`
hashes to the same 2d7b901b... bytes as D1, so the tag document read here is the code that runs locally.

Rebuild of D1, D3, D4 (any seat):

    curl -sS -o squashfs.py https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py
    sha256sum squashfs.py    # 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287
    curl -sS -o LICENSE https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/LICENSE
    sha256sum LICENSE        # 67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e
    curl -sS -o .gitattributes https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/.gitattributes
    sha256sum .gitattributes # df86e28e5e3b04895438ccba79200a462d2e67daefd9042b5477d42b5b2ccede

Rebuild of any fixture payload (path from fixtures-58.tsv, oid from the same row):

    curl -sSL -o fx.bin "https://media.githubusercontent.com/media/onekey-sec/unblob/26.6.4/<path>"
    sha256sum fx.bin   # must equal the row's lfs_oid

No tool was installed or upgraded for this seat; no REA, unblob, sasquatch or reader was run on a
published C1 candidate. Scratch root `/fast/scratch/hyaku/kaidoku-r42/R42SrcUnblob` was removed
after the artifacts below were copied into the lane.
