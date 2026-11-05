# SentinelScope scratch notes — evidence index (round 90)

Tool under audit: `tools/round-90/upx-break-repair.py`
sha256 aaf3536ea2226ac8ec498603d50b7b1b4a57c5572c7edef4fcf0e2a91d35590b (=== claims.json pin)
Counter: `tools/round-90/upx-later-block-battery.py`
sha256 84664f52afa0c03b38aca23552046fcf5e8e04056a597da7b2b06ef6d5eb8206 (=== pin)
Cheat control:  faafc982ca5c7fcf2e787a8f78f81c5eb687c74998d2552ddd8935d01759b826 (=== pin)
bwrap 0.13.1 (`bwrap --version`), python 3.14 (`/usr/lib/python3.14/tempfile.py` in traceback),
upx 5.2.0 pin cf2f6e7c… verified by the counter's preflight (not re-derived here).

Code anchors (line numbers at the pinned sha256):
- L86 `os.lstat(path)`; L89 `S_ISREG` check; L91 size cap 256 MiB — input guards.
- L100-113 `checked_target`: `..` (L104), immediate-parent `islink` (L108), parent isdir (L111).
- L115-125 `write_atomic`: `mkstemp(dir=os.path.dirname(full))` at L118 — **outside** any try;
  `except OSError` only wraps the fdopen/write/replace at L119-124.
- L415-438 `main`: the `try/except Refused` block covers only `read_input`+`repair`
  (L427-431); `write_atomic` for `--out` (L432) and `--info` (L434) are **outside** it.
- L62 `MAX_INPUT = 256 << 20`.
- derive_break: `for s in range(p + 13, ph_off - 12)` + per-survivor `bytearray(d)` copy and
  `chain_ok` -> `find_sentinel`, whose own scan is `for s in range(stop + 1, ph_off - 12)`.
- Counter L174-193 `invoke` (box = mkdtemp(dir=boxes); bwrap argv L181-183;
  `after = sorted(os.listdir(box))` L192), L264-290 run_root/boxes/decoy/blind_paths.
- Counter L265 comment: boxes is "outside run_root" -- i.e. deliberately not hidden.
