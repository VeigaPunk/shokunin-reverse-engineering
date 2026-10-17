# VB6 — verify r5-02 ~283 wording (2nd opinion) + adjudicate counting sections :18-19, :53-70

## CLAIM

Debt item (6) is real: `corpus/knowledge/2026-10-13-r5-02-call-targets-jq.md:153` says "sweeping the remaining ~283 call sites", but the sweepable remainder is **281 call sites** (284 census calls − 3 probed). 283 = 286 − 3 counts all remaining GOT-indirect sites incl. the 2 jmp sites that :154-155 itself excludes as unprobed/out-of-op-scope. Counting sections :18-19 and :53-70 independently adjudicated: :18-19 exact; :53-70 static half exact, output half unverifiable offline.

## METHOD

No Lane A outputs read. Primary sources only: read the file; re-derived counts locally from `objdump -d /usr/bin/jq` + `readelf -r` (binary sha256 `e8156675…84f7806` == pin at :11-12; /tmp scratch gone; no REA runs, no network).

## FINDINGS

- :18-19 census reproduced exactly: 286 `*0x…(%rip)` lines = 284 call + 2 jmp; also 1 `call *%reg` + 2 `jmp *%reg` exist (register-indirect, correctly excluded); all 286 slot targets inside .got [0x7d80,0x8000); `objdump -d` disassembles only .init/.text/.fini; no .plt (`objdump -h`). Claim holds.
- :53-70: the three probed sites exist verbatim as calls — `0x206a`→slot 0x7fb8 `setlocale@GLIBC_2.2.5`, `0x207b`→0x7f78 `jv_array`, `0x20a3`→0x7ea8 `jq_init` (readelf -r GLOB_DAT rows confirm). Their "1 target each" outputs (0x109110/0x1091e0/0x109220) rest on deleted /tmp/r5-ct-*.json; not re-runnable offline — unverifiable here; internally consistent (targets past last file vaddr 0x8038, bss end).
- Arithmetic: 284−3 = **281** remaining calls; 286−3 = 283 = remaining sites incl. 2 jmp → the word/value mismatch is exactly the 2 jmp sites. The "~" is also unjustified (counts are exact, deterministic).
- Minor: ≥6 GOT-indirect call sites sit in .text 0x206a-0x20c1 (also 0x2075, 0x208f, 0x20c1); :59-60 "Three call sites inside main" should be read as "the three probed sites" — one-clause clarification if the line is ever touched.

## THREATS

- Resolver outputs and ev_ hashes cannot be re-verified offline (scratch gone, live probes banned); accepted as recorded, flagged.
- Counts used this host's binutils on the byte-identical binary; a different objdump version could shift line forms.
- Ghidra's exact main extent (procedure 0x102020 → objdump 0x2020 via +0x100000) is not locally checkable; the :59-60 note rests on position in .text.

## VERDICT

FINDING: ~283 wording confirmed imprecise — errata should pin "remaining **281** call sites" (283 only if restated as all remaining GOT-indirect sites incl. the 2 unprobed jmp); census :18-19 and probe section :53-70 otherwise verify.
