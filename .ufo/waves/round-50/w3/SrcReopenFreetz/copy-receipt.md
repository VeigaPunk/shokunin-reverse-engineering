# Copy receipt — S243 source re-open (Freetz 101 patch), seat SrcReopenFreetz, 2026-10-29

- URL: `https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch`
- Fetch UTC time: 2026-10-29T20:32:26Z
- Command (run from `/fast/scratch/hyaku`):
  `curl -sS -o /fast/scratch/hyaku/kaidoku-r50/w3-SrcReopenFreetz/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch -w 'http_code=%{http_code} size_download=%{size_download}\n' https://raw.githubusercontent.com/Freetz/freetz/master/tools/make/squashfs4-host-be/patches/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch; echo curl_exit=$?; sha256sum <out>; stat -c 'bytes=%s' <out>; date -u '+utc=%Y-%m-%dT%H:%M:%SZ'`
- curl exit: 0; `http_code=200 size_download=1153`
- Bytes: 1153; lines: 27 (`wc -l` exit 0)
- sha256: `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707`
- Byte-identity vs attempt-1 lane snapshot: `cmp <scratch fetch> .ufo/waves/round-50/w1/C1SrcFreetz/sources/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch` → exit 0 (identical; both sha256 `e28b3341…c707`)
- Seat-dir copy: `.ufo/waves/round-50/w3/SrcReopenFreetz/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch` (cp exit 0; sha256 of copy identical; 1153 B)
- Attempt-1 record comparison: 1,153 B, sha256 `e28b3341021c4c62560f48807de5c949b7bd55b127c687399a9afc289e84c707`, opened 2026-10-28T23:31:54Z — MATCH, byte-unchanged
- No cookies, tokens, or Set-Cookie headers involved (anonymous raw.githubusercontent.com GET; `-sS`, no saved headers).
