# ExecReaBefore — report (round 87, R87-C1)

Evidence: `.ufo/waves/round-87/w1/ExecReaBefore/before.json` (per carrier × state {orig, packed, T1-zero, T2-foreign} plus `after` per tamper), `notes.md` (commands verbatim), `before_driver.py` (the driver that produced before.json).

- Before: all 8 tampered files make `upx -t/-l/-d` exit 2 (NotPackedException), yet the tampered jq/xxd/docker-init run with rc 0 and print the original version. REA counts are identical across packed, T1 and T2, and REA gives no packer signal. It sees 3 procedures for jq/xxd/dinit (stub only) and 98/184 for libz (partial, not stub-only).
- After (repair f4ebd152…): 8/8 with repair rc 0, `upx -t` rc 0, `upx -d` == pin, and REA procedure counts == declared (167/99/184/1268). Segment and string counts also match orig.
- Finding: jq/xxd have a 4th `UPX!` word, the loader immediate `cmp edx,'UPX!'` (jq @10971, xxd @16499). The repair leaves it tampered, so the repaired jq/xxd are not byte-identical to the intact packed file, but all arms still pass. This does not change the score. It qualifies what "recovered" means.
- Calibration: "REA sees only the stub" does not hold for libz.
- No installs, no production edits, no VCS mutation. Scratch removed.
