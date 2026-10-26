# R39W2C2EntryReview — QUALITY review of `corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md`

**Verdict: DEFECTS FOUND (all minor)** — every substantive claim in the entry verified against its
five cited sources (line-exact), the committed round-38/39 envelopes, the committed held-out set and
the interpreter source; four minor defects remain (one false rider, two citation-precision gaps, one
uncited unlabeled inference), plus one row-13 conformity observation. Nothing falsifies the entry.

Seat `R39W2C2EntryReview`, leaf. Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Writes: this file and `w2/artifacts/R39W2C2EntryReview/sources/` only. No VCS mutation, no installs
(no tooling authorization entry needed), no REA run, no subagents. Scratch
`/fast/scratch/hyaku/kaidoku-r39/R39W2C2EntryReview` removed at the end; the six upstream files the
line audit quotes are preserved under the artifacts dir with sha256 below.

## 1. Provenance header — PASS

- Five `source:` lines (:3-7): S112, S118, S119, S120, S121 — all five rows exist in
  `corpus/SOURCES.md` (:118, :124, :125, :126, :127) with matching URLs and scope notes.
- `verified-at: 2026-10-26` (:8) present; the introducing commit is the freeze commit `8fcda41c`
  (committer time `2026-10-26T14:12:51-03:00`, `git log -1 --format='%h %cI %s' -- <entry>`) — same
  date, so the stamp does not postdate the commit. Date-only stamps are zoneless (QUALITY #23 does
  not check them; same form as the sibling C1 entry).
- `recheck: 180d` (:9) **re-run 2026-10-26**: `grep -c 'is_avm = header.bytes_used ==
  header.mkfs_time' ~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/
  filesystem/squashfs.py` → stdout `1`, exit 0 — reproduces. The installed file is byte-identical to
  the S112 tag blob (`cmp` tag-download vs installed file → exit 0; sha256 of the downloaded tag
  file `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`, the same value the
  round-38 probe and w1 `R39C2ReconMarker` recorded), so the recheck re-verifies S112's exact bytes.

## 2. Source-line citation audit — 12/12 exact

Downloaded each cited source at the pinned tag into scratch and numbered the lines (`awk 'NR>=a&&NR<=b'`):

| entry line | citation | checked lines | verdict |
|---|---|---|---|
| :3 | S112 `SquashFSExtractor` 24-70; AVM branch 44-50; `get_dependencies` 68-69 | class at 24, `case Endian.BIG, 4:` 40, header parse 44-46, `is_avm` 48, `if not is_avm` 49, `append("-be")` 50, `def get_dependencies` 68 + `return [self.EXECUTABLE, self.V4BE_EXECUTABLE]` 69 | exact |
| :4 | S118 `fix_symlink` 50-92 | `def fix_symlink` 50, loop-removal branch 58-65, absolute re-root 73-77, `safe = is_safe_path` 79, removal 81-87, rewrite 88-91, `return path` 92 | exact |
| :5 | S119 tarball | tarball sha256 recomputed `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699` = SOURCES pin; the three cited `dist/` files byte-equal (`cmp` exit 0) between tarball and the npx 6.5.0 install, so local grep line numbers are the tarball's | exact |
| :16 | `FirmwareReports.js:254-255` | 253 `for (const item of record.reports)`, 254 `if (!known.has(...))`, 255 `diagnostics.push(jsonValueSchema.parse({input_path, report: item}))` — the verbatim copy | exact |
| :17-18 | S120 `report.py:91-98`; `command.py:59-68` | `class ExtractCommandFailedReport` 91 with `command: str` 95; `if res.returncode != 0:` 59 → construct 60-65 → raise 68 | exact |
| :22-23 | `command.py:101-102` | `def get_dependencies` 101, `return [self._executable]` 102 | exact |
| :24 | S112 68-69 | see above | exact |
| :25 | `FirmwarePublication.js:241` | 241 `const dependencyChunkKeys = new Set(...)` under the "dependency row already covers" comment; the filter at 293 `!dependencyChunkKeys.has(...)` inside the generic `extractor-failure` emission | exact |
| :30 | S112 44-50 | see above | exact |
| :31 | S121 | `unsquashfs.c:4389` `strcmp(argv[i], "-be")`; FIX_BE branches 2263-2282 (the "different endianess" message at 2267-2268 is the exact string the entry quotes at :32-33); `debian/rules` 15-18 = install steps, 17 `CFLAGS=-DFIX_BE dh_auto_build`, 18 `cp … sasquatch-v4be` | exact |
| :42 | S118 79-91 | safe-check + remove/rewrite | exact |
| :43 | S118 73-77 | `target = Path(raw_target)` … `target = path.resolve()` | exact |
| :45 | S119 `FirmwarePublication.js:68-75,301-308` | 68 `for (const entry of context.entries)`, 69-76 non-file → `unpublished.push({relative_path, kind, link_target})`; 301-308 `...unpublished.map(... kind: "unpublished-entry" ...)` | exact |

## 3. Envelope, held-out and interpreter audit — PASS

- `corpus/evidence/round-38/c1/K1/before.json` (cited :26): `G=[missing-extractor-dependency]`,
  `D=[sasquatch-v4be]`, files 0 — matches the BE dependency claim exactly.
- `.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json` (cited :37): `G=[extractor-failure]`,
  files 0, command `sasquatch-v4be -no-exit-code -f …` (no `-be`), `exit_code 1`, stderr exactly
  `SquashFS version [1024.0] / inode count [184549376] suggests a SquashFS image of a different
  endianess\nread_id_table: …` (also in the probe's `summary.json`) — matches :32-33 verbatim.
- Committed held-out set `corpus/evidence/round-39/c2/heldout/` (manifest 20 carriers, 10 classes × 2):
  H01 clean → no commands, 7 files, complete; H05 escaping → no commands; H07 in-tree →
  `unpublished-entry`; H09 dep-missing-be → `sasquatch-v4be`, no command (BE `n/a`); H13 avm →
  command without `-be`; H15 body → command with `-be`; **H19/H20 (`version-minor-mismatch`,
  `s_minor` 5) → `G=[extractor-failure]`, files 0, command `sasquatch-v4be -be …`** (confirms
  :33-34 on committed data); H17/H18 no-squashfs-chunk → no chunk, no gap, 0 files,
  `coverage complete` (confirms :51-53). Every checked `run.json` has `exit_code 0`.
- Interpreter `tools/round-39/sqfs-triage.py` vs the Features paragraph (:11-16): `features()`
  returns exactly H (handlers `startswith('squashfs')`, :384-386), G, D (union over gaps), BE
  (`'n/a'` when no sasquatch command; standalone `-be` token via `shlex` tokens, :325-340 —
  `-no-exit-code` never counts), SR (`MaliciousSymlinkRemoved` in `diagnostics` or `raw_result`),
  P (`len(files)`) — six fields, as claimed. The tool references no knowledge entry (no
  `knowledge`/date string in its source) — "the interpreter reads the table, never this entry"
  (:56-57) is true; it parses the marker `<!-- sqfs-triage-table v1 -->` inside the craft section.
- SKILL.md table (marker at `SKILL.md:333`, 8 rows = the title's "eight labels"): escaping row
  (gaps `*`, SR `yes`) precedes the in-tree row, so a mixed image first-matches
  `escaping-symlink-removed` (:47-48 ✓); body row handler cell is `squashfs_v4_be`, so LE body
  damage matches nothing → `unclassified` ("little-endian body damage (no row)", :59 ✓); no row
  matches `unknown-chunk-handler`/`encrypted-chunk`/`depth-limited` gaps (:58-59 ✓). The block
  cites this entry at `…sqfs-outcome-triage.md:11-28`, `:29-40`, `:41-54` — "This entry backs the
  round-39 triage table" (:55) is literally true.

## 4. Wave-2 addendum (:61-74) — every citation resolves

The addendum (appended after the score) is fully traceable: `w2/R39W2C2Shortcut.md` carries the
16/20 ablation ceiling and the 8-row/7-non-`*`-cell floor (:4-6, :17-18, :80-84) and the no-leak
result (:19); `w2/R39W2C2AxisFit.md` carries the 0%-scored cause column and the non-firmware
mislabel (:7-8, :143-146, :215-221); `w2/R39W2C2TableReview.md` carries D3 (row-6 loop omission,
S118:58-65), D4a (row-7 `special` entries — verified live: `firmwareAnalysis.js` `unpublished_entries`
kind enum `["symlink","special"]` at :136-140) and D5a/b (row-4 wrapper untested `[INFERENCE]`,
`w1/R39C2TableDraft.md:143-146`). K5/K6 mixed-symlink envelopes verified:
K5 `after.json` = 2 `unpublished-entry` + 1 `MaliciousSymlinkRemoved` + 10 files; K6 = 1 + 2 + 8.
"Corrections for the next table version, not edits to the frozen one" — honest framing.

## 5. Findings

**F1 — minor — :14-15 (false rider on a correct definition).** "(`n/a` when no command is
recorded, which is every successful run)". A successful REA run can record a command: committed
held-out H15/H19/H20 all have `run.json.exit_code 0` **and** a recorded `sasquatch-v4be -be …`
command (their chunk failed); w1 `R39C2ReconDep` states all 23 dev runs were `ok:true`, including
chunk-failing xz runs with recorded commands. The command exists only on
`ExtractCommandFailedReport` (S120 `report.py:91-98`, `command.py:59-68`), so the true rider is
"which is every run with no failed chunk". The operational definition in the same sentence ("when
no command is recorded") is correct; drop or fix the "every successful run" clause.

**F2 — minor — :50-52 (citation does not cover one of three listed causes).** "A truncated image, a
`bytes_used` beyond the file **or an `s_major` other than 4** … (`.ufo/waves/round-39/w1/
R39C2ReconTruncate.md`)" — that report never built an `s_major ≠ 4` carrier (its §5 names
`bytes_used > file_size` as the deciding invariant; all its carriers keep `s_major = 4`). The
`s_major` evidence is `w1/R39C2HeldoutGen.md` §4 opt-in (op H01/H02, `s_major` 4→9 → no chunk, no
gap, no file, `complete`). Add that citation beside ReconTruncate.

**F3 — minor — :33-39 (claims exceed the cited section).** The `s_minor` sentence claims "with zero
files, but the recorded argv carries `-be`", citing `R39C2HeldoutGen.md` section 4 — that section's
opt-in table records only the gap kind and the stderr line for op H03/H04, neither file count nor
argv. Both details are true (verified on committed held-out H19/H20 envelopes above, and the w1
`opt-in-run/` envelopes hold them); cite those instead of, or beside, section 4.

**F4 — minor — :35-37 (uncited, unlabeled inference + superlative).** "REA's `extract-firmware` has
no unblob-flag passthrough, so the **only** fix for the marker case is a `PATH` wrapper named
`sasquatch-v4be` that appends `-be`." Neither clause carries a citation or an `[INFERENCE]` label.
The w1 basis is explicitly hedged: `w1/R39C2TableDraft.md:145-146` "[INFERENCE] — I did not build or
test one. `npx rea-agents@6.5.0 extract-firmware --help` confirms there is no unblob-flag
passthrough"; source support exists at `dist/firmware/FirmwareCommand.js:17-33` (REA resolves only
an absolute binary path via `REA_UNBLOB_COMMAND` and spawns it with fixed arguments — no flag
channel); the entry's own addendum (:71-72) already flags the wrapper mechanism as untested
(`w2/R39W2C2TableReview.md` D5a/b). Within `extract-firmware`'s argv the wrapper is the mechanism
(unblob hardcodes the executable name, S112 :25-26,:41), but "the only fix" is a superlative —
input-side normalization (clearing the marker before the run) is an alternative outside that
framing. Label the sentence `[INFERENCE]`, cite TableDraft:145-146 or `FirmwareCommand.js:17-33`,
and align its hedge with the addendum.

**F6 — observation (QUALITY #13 conformity), :9.** The recheck records an occurrence count via
`grep -c`. Row 13's letter prescribes `grep -o … | wc -l` for occurrence counts ("never
`grep -c`"). Here the target is a normal multi-line source file, the count 1 is a true
matching-line count, the command reproduces (re-run: stdout `1`, exit 0), and the sibling round-39
C1 entry uses the same form — noted for the record, not charged as a defect of this entry alone.

(No F5: the symlink-loop gap I initially flagged at :46-47 is already disclosed by the entry's own
addendum at :69-71, citing S118:58-65 and `w2/R39W2C2TableReview.md` D3 — verified correct.)

## 6. Limits paragraph — honest

"Development evidence only … held-out set generated after the freeze" ✓; the not-covered list
matches the frozen table (no rows for `unknown-chunk-handler`/`encrypted-chunk`/`depth-limited` →
`unclassified`; body row BE-only → LE body damage `unclassified`; AVM-BE/XZ/vendor images and
extracted programs out of scope) ✓; QUALITY #11's parsed-empty-vs-excluded discipline is present
(:52-53 "An empty envelope of this shape is not an empty filesystem", mirrored in the table's
no-squashfs-chunk cause) ✓. No overclaim found beyond F1-F4.

## 7. Residual risk and verification gaps

- `unblob` 26.6.4 also ships a third v4 handler, `squashfs_v4_broadcom` (`squashfs.py:548-551`),
  which inherits the same extractor; "Both v4 handlers" (:20) undercounts the family and the Limits
  paragraph does not name it (a Broadcom-image envelope would match no row → `unclassified`;
  `w2/R39W2C2TableReview.md:280-281` records the same). Unexercised by any cited evidence.
- :13-14 names `diagnostics[].report.command` for BE; the interpreter also accepts the
  `raw_result` mirror (`extractor_commands` walks both). A harmless superset; a nit.
- S119 was verified via the npx-resolved install plus tarball sha256 equality (pin match, three
  cited files byte-equal); I did not line-grep the tarball directly, but byte equality makes that
  moot.
- S118/S120/S121 re-downloads hash to the values SOURCES/w1 recorded (`extractor.py`
  `1bb49811…`, `report.py` `2329783f…`, `unsquashfs.c` `ece42b66…`) — sources stable since the
  round read them.

## 8. Verification log (key commands)

- Recheck rerun: `grep -c 'is_avm = header.bytes_used == header.mkfs_time' ~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py` → `1`, exit 0; `cmp` tag vs installed → 0.
- `git -C <lane> log --format='%h %cI %s' -1 -- corpus/knowledge/2026-10-26-r39-sqfs-outcome-triage.md` → `8fcda41c 2026-10-26T14:12:51-03:00 round-39: freeze …`.
- `curl` the five pinned sources at their tags into scratch; numbered with `awk 'NR>=a&&NR<=b {printf "%d|%s\n", NR, $0}'`; sha256 in `w2/artifacts/R39W2C2EntryReview/sources/` (`sq.py 2d7b901b…`, `ex.py 1bb49811…`, `rep.py 2329783f…`, `cmd.py 8ae7d2a3…`, `unsq.c ece42b66…`, `rules b49d25e9…`).
- `curl -o rea.tgz https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz && sha256sum rea.tgz` → `531717a0…` (= S119 pin); `tar xzf` the three cited `dist/` members; `cmp` vs `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/...` → all equal.
- `jq` feature probes over `corpus/evidence/round-38/c1/K1/before.json`, `.ufo/waves/round-38/w2/artifacts/R38W2AvmProbe/rea-k1-avm.json`, `corpus/evidence/round-39/c2/heldout/H{01,05,07,09,13,15,17,18,19,20}/envelope.json` (+ `run.json` exit codes) and `corpus/evidence/round-39/c1/K{5,6}/after.json` — outputs quoted in §3/§4.

No tool was installed or upgraded (host pacman pause respected; nothing needed).
