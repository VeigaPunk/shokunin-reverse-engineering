# frontier-repair-D — PROVINCE.md Round-4 frontier bullet R1: the RISC-V parse gate (1 hunk, line-neutral)

Authored by SEAT EX-11 (chain c2, executor), wave `arc3-loop1-round4`. **Patch text
only** — the parent applies it; seats never write PROVINCE.

Measured against revision `015e1bab914713568f339fd53999bc180459cc40` at write time:
`PROVINCE.md` sha256 `d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad`,
162 lines. Line-neutral (4 -> 4), needle-free.

## The staleness (measured this seat, live)

The bullet presents the RISC-V wall in the present tense: "`target_unavailable`
gate pinned (`binaryTarget.js:105` ELF e_machine allowlist), bypassed via e_machine
patch + language override". Three measurements show that is the **r5-01-pin**
state, not the live state:

| pin | `dist/domain/binaryTarget.js` | RISC-V handling | refusal class on an EM_RISCV ELF |
|---|---|---|---|
| r5-01's pin (3rd npx cache) | 237 lines, md5 `b7f89a09…` | `elfArchitecture()` has no case for 243 | `target_unavailable` / "unsupported ELF architecture" at `:105` — **as the bullet records** |
| mid pin (2nd cache) | 394 lines, md5 `0b036178…` | riscv case present | `capability_unavailable`; Ghidra lane asks for `EF_RISCV_FLOAT_ABI_DOUBLE` |
| live pin (Kimi's cache) | 379 lines, md5 `1ff13b45…` | `:118` branches on `architecture === "riscv"`; `elfFixedHeader.js:63` returns `"riscv"`; `binaryTargetTypes.js` lists it | provider-layer `architecture_unsupported` with a typed, specific reason — **not** a parse-gate `target_unavailable` |

End-to-end on the live pin, **no language override**: a RISC-V ET_EXEC carrying
the double-float ABI declaration analyzes successfully — RC=0,
`ev_a572363e36159f249fd24c18a5e7704d235576aa030b977056a3fa653fe09c97`,
`subject.architecture:"riscv"`, 31 segments, provider chain
`rea-workflow` → Ghidra 12.1.4 (`evidence/r1-live-pin-riscv-exec.json`). The same
file with the soft-float ABI is refused with the specific ABI reason, and a
RISC-V PIE is refused with "supports fixed-address ET_EXEC only" — both typed
rejections, both at the provider layer.

What this does **not** change: the r5-01 entry's own measurement was correct at
its pin, and the direct-`analyzeHeadless` leg (29 MB EXEC, 10,766 functions) is
independent of REA's pin and stays true. The repair therefore marks the parse
gate as superseded rather than deleting it, and keeps the entry citation.

**Needle note.** The repair must not name a pin version: the Frontier region is
UNDECLARED in the census scope table, and a bare `6.x.y` or a `rea-agents@x.y.z`
written there reads FAIL undeclared (EX-14 measured this on this very section).
The hunks therefore refer to "r5-01's pin" and "live pins" by role.

## Hunk
```diff
# file: PROVINCE.md
--- a/PROVINCE.md
+++ b/PROVINCE.md
@@ -135,4 +135,4 @@
-- **RISC-V analysis** — `target_unavailable` gate pinned (`binaryTarget.js:105`
-  ELF e_machine allowlist), bypassed via e_machine patch + language override
-  (r5-01: `corpus/knowledge/2026-10-13-r5-01-riscv-bypass.md`); full 29 MB EXEC
-  via direct `analyzeHeadless` (10,766 functions @900 s cap).
+- **RISC-V analysis** — r5-01's parse-gate refusal (`binaryTarget.js:105`
+  e_machine allowlist) is superseded: live pins carry a Ghidra RISC-V lane
+  (ET_EXEC + double-float ABI, no override needed); full 29 MB EXEC via direct
+  `analyzeHeadless` (10,766 functions @900 s cap) — r5-01 entry retained.
```

## Carrier caveat (honesty — the carrier is synthetic)

The admitted target is a **mislabeled carrier**: `jq`'s bytes with `e_machine`
patched to 243, `e_type` to ET_EXEC and the double-float ABI flag set
(`/var/tmp/ex11/jq-rv-dbl.bin`, sha256 `e6586a6db5e732afe9398a9a97f94fb6981afe703300bde05e67ebfe3a1b2cc7`;
recipe: `cp /usr/bin/jq <copy>`, `printf '\x02\x00' | dd of=<copy> bs=1 seek=16
conv=notrunc`, `printf '\xf3\x00' | dd of=<copy> bs=1 seek=18 conv=notrunc`,
`printf '\x04\x00\x00\x00' | dd of=<copy> bs=1 seek=48 conv=notrunc`). What the
run therefore proves is exactly one thing: **the parse gate no longer refuses
EM_RISCV on the live pin** — admission reaches the provider layer and succeeds
when the lane's two declared requirements are met. It does **not** prove that the
live pin analyzes real RISC-V code correctly (the bytes are x86-64), and the 31
segments are a projection of a fabricated carrier, not a RISC-V measurement. A
real-RISC-V end-to-end leg remains open; the r5-01 entry's direct-`analyzeHeadless`
leg on a genuine 29 MB RV64 EXEC is still the only real-code RISC-V evidence in
the corpus.

## Why this was not caught earlier

The r5-audit C1 pass that re-keyed this section tagged the bullets it touched but
left this one's present-tense wall wording standing, and the census gate cannot
see it (the Frontier block is UNDECLARED and needle-free, so the gate is inert
there — see `frontier-census.md`, attack #1). It was found by reading the live
caches' `binaryTarget.js` against the bullet's cited line.
