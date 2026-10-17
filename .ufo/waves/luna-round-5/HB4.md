## CLAIM
Cross-check every size figure in the current coverage-map rows (`corpus/README.md:13-61`) against source knowledge files, independent of Lane A H3; adjudicate debt #2 (r4u-01 hex→decimal size decimals).

## METHOD
Read-only reads at HEAD `cfc84c2` (tracked tree clean; `git status --porcelain` shows only untracked `.ufo/`). Mechanical token extraction: `sed -n '13,61p' corpus/README.md | grep -oE '([0-9][0-9,\.]*) ?(MB|KiB|KB|GiB|MiB)'` plus a hex scan. Arithmetic: `python3 -c "print(0x1c01dc8, 0x505b000)"` → `29367752 84258816`. No live probes. H3 read only after completing the primary-source pass.

## FINDINGS
- All ten byte-size tokens in coverage rows match sources: 91.6MB=r4-12:8,18 (91,662,336 B; truncation, not rounding); 24.9MB=r4-14:5 (24,944,200 B); 530KB=r4-07:128 (530,020 B); 41MB/68MB=r4-15:7,23 (41,154,494/68,429,868 B); 29MB=r5-01:3,12; 41-43MB=r4-10:19 (41,210,040→43,475,106 B); 1GiB/1.13-1.25GiB=r4u-05:12,116; 64MiB=r4-11:81; 32 MiB=r2-crash-inspect-probe:21-22.
- Non-byte counts also match: 715/579/1,046 (r4-15:30,70); 741/163 (r4-14:17,33); 120/130 (r3-apk-inventory:35-36); 196/0xfd1d (r4-11:53-66); 2,594/650 (r4u-04:71,77); 171 (r9-01:63-80); 13/8/104 (r12-01:50); 10 changed (r12-02:23); 18/8 (r2-provider-capability-matrix:26); ~26/~45/8 (r4-16:262-265); 56/156 (r4u-01:17); 94/10,766/900s (r5-01:3,26,64); 3/3 of 286 (r5-02:18,53); 19/19 (r8-02:125); 32 header bytes (r11-02:113); 0x117070 (r7-02:22-35).
- Debt #2 CONFIRMED, both parentheticals wrong at `r4u-01:41`: 0x1c01dc8=29,367,752 (file says 29,358,536=0x1bff9c8); 0x505b000=84,258,816 (file says 84,242,432=0x5057000). Direction for tu10x proven: r5-01:12,78 records the offset-64 carve as 29,367,752 B and the wave ran `--length 29367752` — hex side correct. For ga10x no second source cites either value; I infer hex-right from internal arithmetic (84,310,168−64−0x505b000 leaves a 51,288 B tail = 12×4,096 sigs + ~2,136 structural; 0x5057000 leaves an absurd 67,672 B). Already claimed at luna-round-4 C05.
- Map rows do not propagate the bad decimals (Firmware row:44 has no byte figures).
- Incidental, non-size: README:122 says r9-02's four statuses are unresolved/contradicted/verified/unsupported, but the schema union (r9-02:50-54) is verified/inferred/unresolved/contradicted and row 53 says "inferred not evidenced" — README-internal conflict for the r9-02 seats. README:105 "423-file" is pre-erratum wording (r4-06:327-331: 480 members vs relevant_files 423). README:15 "10 r2 doctor checks" vs r2-doctor-reverify-r2:16-17 (18 checks, 10 pass/8 fail).

## THREATS
Textual verification only; artifacts not re-probed (as instructed), so the ga10x direction is inference; "size figure" read as byte sizes plus entity counts, not process counts; H3 covered only the four MB labels and agrees.

## VERDICT
CLEAN for map-row size figures; debt #2 confirmed (both decimals misconverted; C05-known).
