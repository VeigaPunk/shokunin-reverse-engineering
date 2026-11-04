# ScribeEntry — round 87 (R87-C1) notes

Candidates (none written to a production path):
- `candidate/corpus/knowledge/2026-11-04-r87-upx-magic-tamper-repair.md` — knowledge entry (status/source/verified-at/recheck front matter in the r84 shape; class, three anchors, commands, measurement table, limits).
- `candidate/SKILL.md.decision-row.md` — (a) one row for `## Decision table (this host, r3-verified)`, (b) a standalone `### Round-87 UPX magic-tamper rule` block; L1 picks one.
- `candidate/PROVINCE.md.round-87-block.md` — `## Round-87 additions to Core (verified 2026-11-04)` with Core bullet + frontier note.
- `candidate/corpus/README.md.frontier-and-rows.md` — coverage-map row, `## Knowledge` row, Round-87 frontier note.

Placeholders the L1 fills: every `<MEASURED…>` (rev, receipt path, per-case table, recovered N of 8, N1/N2/N3 counts, exit); `<QUOTE…>` in both `source:` lines from ScribeSources' S306/S307 rows (ids are placeholders; reconcile).

Scribe observation (scratch run, not the scored run; scratch deleted):
command per carrier in `/fast/scratch/hyaku/kaidoku-r87/ScribeEntry/` (TMPDIR there):
`/usr/bin/upx --best -q -o <n>.p <copy of carrier>`; Python `d.replace(b"UPX!", b"\0"*4)` → `<n>.t1`;
`python3 -I -B tools/round-87/upx-magic-repair.py --in <n>.t1 --out <n>.r --json`; `cmp -l <n>.p <n>.r | wc -l`; `upx -t <n>.r`; `upx -d -q -o <n>.u <n>.r`; `cmp <n>.u <copy>`.

| carrier (source) | packed sha256 prefix | `UPX!` offsets in packed | repair anchors l_info / b_info_end / packheader | walk first/resume/resumed | repaired vs pristine packed (bytes) | upx -t | unpacked == original |
|---|---|---|---|---|---|---|---|
| jq (`/usr/bin/jq`) | e8b6c9e76b54 | 556, 10971, 13992, 14000 | 556 / 13992 / 14000 | 5 / 13228 / 4 | 4 | 0 | yes |
| xxd (`/usr/bin/tinyxxd`) | 1727faf91c38 | 556, 16499, 19513, 19524 | 556 / 19513 / 19524 | 5 / 18756 / 4 | 4 | 0 | yes |
| libz (`/usr/lib/libz.so.1.3.2`) | a9c544e6da4f | 9284, 63721, 65544 | 9284 / 63721 / 65544 | 3 / 62944 / 4 | 0 | 0 | yes |
| docker-init (`/usr/bin/docker-init`) | b67ce1bdda27 | 556, 357738, 357748 | 556 / 357738 / 357748 | 5 / 355828 / 4 | 0 | 0 | yes |

UPX banner `upx 5.2.0`. T1 only; no REA run; tampered `upx -t` printed `Tested 0 files.`
The non-anchor occurrences (jq 10971, xxd 16499) ground the "repaired packed ≠ pristine packed" limit; the claim that they are loader `cmp` immediates is carried as [inference] (not disassembled).

Tooling: nothing installed or updated.
