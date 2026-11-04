<!-- Candidate for PROVINCE.md: append after `## Round-84 additions to Core (verified 2026-11-04)`. -->

## Round-87 additions to Core (verified 2026-11-04)

- **Core — UPX-packed ELF whose `UPX!` magic words are tampered (magic-altered anti-UPX class):**
  `tools/round-87/upx-magic-repair.py` (sha256 `f4ebd152…9723`) restores the magic words from the
  packer's own structures — the PackHeader (its checksum excludes the magic), `l_info` cross-checked
  by version/format/`p_filesize`, and the end-of-chain `b_info` reached by walking the chain past the
  loader (S306, S307) — reading only `--in` and never running the packer. The frozen counter
  `tools/round-87/upx-tamper-battery.py` (sha256 `0f2d2bd8…4b0`) scores it on the four round-70
  carriers (`jq`, `xxd`, `libz.so.1.3.2`, `docker-init`) packed `upx --best` with UPX 5.2.0 and
  tampered T1-zero and T2-foreign: recovered `<MEASURED> of 8` (target 8; do-nothing 0/8,
  naive-global 4/8), each case requiring repair rc 0, changes only inside windows now reading
  `UPX!`, `upx -t` rc 0, `upx -d` to the pinned sha256 and REA 6.5.0 `analyze` to the declared
  procedure count (167/99/184/1268); controls N1 `<MEASURED>`/4, N2 `<MEASURED>`/4 recovered (0
  required), N3 `<MEASURED>`/4, exit `<MEASURED>`.
  Capability: `NotPackedException` on a section-less, running, high-entropy ELF is a symptom, not a
  verdict; repair the structure, test, then take the packed-ELF route.
  Receipts: `<MEASURED: .ufo/waves/round-87/l1/scores/c1-at-<rev>.json>`,
  `.ufo/waves/round-87/pre/c1-control-identity-at-base.json`,
  `.ufo/waves/round-87/pre/c1-control-naive-global-at-base.json`.
  Entry: `corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md`.
- **Round-87 frontier note, 2026-11-04:** the "anti-UPX stub whose magic … is altered" / "anti-UPX
  stubs" clause of the earlier notes and Core bullets (`PROVINCE.md` lines 466, 474, 537, 546, 556,
  617, 642 in the working tree read 2026-11-04 — round-68/69/70/72/73 notes and the round-76/78
  bullets) moves to Core for magic-only tampers of the four pinned carriers
  under UPX 5.2.0 `--best`, little-endian ELF x86-64 only. Still Frontier: an anti-UPX stub whose
  **entry** or loader code is altered, tampering of PackHeader/l_info/p_info/b_info fields other
  than the magic, any other packer or UPX version/mode, big-endian ELF, packed PE/Mach-O, any
  carrier outside the four, packed-byte equality of the repaired file (jq/xxd keep a 4-byte
  difference in the loader), repair provenance (the counter scores bytes; the no-pin rule is
  checked by review), and semantic equality of a recovered inventory.
