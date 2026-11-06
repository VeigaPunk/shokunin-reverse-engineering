# ScribeEntry — knowledge-entry draft for R100-C1 (round 100, attempt 1, wave 1)

Seat: ScribeEntry (scribe). Item: draft `corpus/knowledge/2026-11-05-r100-pe-upx-payload-checksum-refusal.md`
into the wave dir (not the lane corpus) plus a `corpus/README.md` coverage-map row draft.

## Deliverables (all under this seat's wave dir)

- `w1/ScribeEntry/2026-11-05-r100-pe-upx-payload-checksum-refusal.md` — the entry draft (source
  front matter S327/S324/S326, rule, measured table, population, limits, not-examined).
- `w1/ScribeEntry/README-coverage-map-row-draft.md` — proposed `## Coverage map` row, `## Knowledge`
  index row, `Round-100 frontier note`, plus one correction to the committed rows.
- `w1/ScribeEntry/receipts/` — every receipt cited below, copied out of the lane: the L1 C1 receipt
  at A1, the L1 C2 receipt at A2, `c1-controls-at-freeze.txt`, `adler-equality.txt`, this seat's
  reproductions (C1 at A1, C2 at A2, controls h4/h5 at F), the re-measured Adler-32 equality, and
  the probe transcript.

## Revisions and provenance cited

B0 `6371c88633f6ce6692eaeff17e256b80ad21ece0`; F `8e24c29a37ca81a0bd1ff5ec73c96a949885322e`;
CT `b3f41553e201e0e5ea76dd9e5b90285a97069a5b`; A1 `a610671d7a01e1d762eb7103e6ee9f8a2be287ed`;
A2 `cbd224ef9b9d2271f415d823bdc4d1e70a0d281c`. Lane `main` advanced to
`b0a7bb8ca5ef66d459d786b9d2705c7fd866d502` (C1 knowledge landing) while this seat worked, and the
lane working tree carries further uncommitted edits to the same entry and to `corpus/SOURCES.md`
(adding S328 and the ExecHeldOut citation). The lane copy was read at both states and diffed
against the draft here; this seat wrote nothing outside its own wave directory.
Host: `upx 5.2.0` (`/usr/bin/upx`, sha256 `cf2f6e7c…a8c969`), `/usr/bin/strace` (sha256
`28ed5493…796e2`). No tool was installed; pacman untouched; no PATH directory written.

## Commands run (every cited number comes from one of these)

1. `python3 -I -B tools/round-100/pe-upx-corrupt-battery.py --root <clone@A1> --repair
   tools/round-100/upx-pe-repair.py --rev a610671d7a01e1d762eb7103e6ee9f8a2be287ed --work
   $S/c1 --json-out $S/out/c1-repro-a1.json` → exit 0, label
   `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40;
   corrupt 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; exec 1 of 1; effective 119 of 119`,
   `met True`. The receipt's label, counts, `counter_sha256` (`8f148d33…3183`), `repair_sha256`
   (`15ada0b0…9a37`) and `rev` are identical to the L1 receipt at A1 (compared field by field).
2. `python3 -I -B tools/round-100/registry-selftest-truth.py --root <clone@A2> --rev
   cbd224ef9b9d2271f415d823bdc4d1e70a0d281c --work $S/c2 --json-out $S/out/c2-repro-a2.json` →
   exit 0, label `rows 93; claimed 93 of 93; green 93 of 93; counted 93 of 93; agree 93 of 93;
   mismatches 0` (identical to the L1 C2 receipt at A2).
3. The same C1 battery at F against two controls, read with `git show` at F:
   `tools/round-100/forgeries/h5-length-only.py` → exit 1, `corrupt 0 of 40`;
   `tools/round-100/forgeries/h4-oracle-alias.py` → exit 1, `corrupt 20 of 40; exec 0 of 1`.
   Both match the committed transcript `.ufo/waves/round-100/pre/c1-controls-at-freeze.txt`.
4. Adler-32 equality re-measured on all ten pinned packs (fresh `upx --best` packs, header located
   by the `UPX!` word): seed 1 equals the stored `c_adler` on 10 of 10, seed 0 on 0 of 10;
   `receipts/adler-equality-remeasured-by-scribeentry.txt`.
5. Probes on a `t32.exe` pack (distlib, sha256 `6b4195e6…9415b`), transcript
   `receipts/probe-transcript.txt`: corrupted payload → round-100 candidate rc 2
   `refused: checksum: adler32 of compressed data 5819af6c != c_adler 8091af36`, no `--out`, while
   `upx -t` says `Exception: checksum error` rc 1; the round-99 candidate on the same bytes answers
   `ok intact` rc 0 and its output is byte-identical to the corrupted input (sha256 equal), and
   `upx -t` of that output still fails rc 1; forged `c_adler` (payload flipped and `c_adler` plus
   the header checksum byte rewritten) → candidate `ok intact` rc 0 while `upx -t` refuses rc 1;
   tampered magic+names plus a flipped payload byte → `refused: checksum` rc 2, no `--out`;
   compressed data cut one byte past EOF → round-100 refuses `truncated: compressed data ends at
   36040 > file 36039 bytes` rc 2 where the round-99 candidate answers `ok intact` rc 0.

## Findings (7)

- F1 [correctness, lane copy] The lane entry's class paragraph and the committed README rows say
  the corrupt arm "fails `upx -t` with `Exception: checksum error`" for the whole arm. The L1
  receipt's 40 corrupt cells split 20/20: the `corrupt-intact-*` cells carry `checksum error`, the
  `corrupt-both-*` cells (same payload flip plus the round-98 magic/name tamper) carry
  `CantUnpackException: file is modified/hacked/protected` — the anti-unpack gate (S324) refuses
  before the compressed data is checksummed. The refusal is the packer's own in both halves and the
  arm is effective 40 of 40; only the message differs. Correction drafted in both files.
- F2 [resolved in the lane working tree, still open at `b0a7bb8c`] The entry committed at
  `b0a7bb8c` cites `corpus/lessons/round-100.md` for the held-out run; that file does not exist at
  that revision. The lane working tree has since replaced that citation with
  `.ufo/waves/round-100/w1/ExecHeldOut.md` (nine held-out files, 54 payload flips, 54 of 54 refused
  `checksum`) — the dangling citation is closed there, and the draft uses the same retained path.
- F3 [corpus-quality gap, lane copy] The lane entry has no carrier identity table (QUALITY row 4:
  absolute path plus sha256) and no "not examined" section (QUALITY row 7); it names the carriers
  only as a prose list inside one Limits bullet. The draft adds both, with the ten carriers' paths
  and digests re-hashed by this seat (10 of 10 equal to the battery's pins).
- F4 [resolved in the lane working tree] The seed-1 claim now rests on the round-100 registry row
  **S328** (`src/check/dt_check.cpp`, `upx_adler32(d,4) == 0x09f003f7` and seed 0 `0x09ec03f6`),
  added to `corpus/SOURCES.md` and cited by the entry after `b0a7bb8c`; Python reproduces both
  values exactly (re-measured by this seat, `receipts/s328-zlib-crosscheck.txt`). The draft cites
  S328 and keeps the independent 10-of-10 pack measurement.
- F5 [citation precision, lane copy] The lane entry's S324 line quotes only line 3053; the read of
  exactly `c_len` bytes is line 3054 (`fi->readx(ibuf, ibufgood = ph.c_len);`). The draft cites
  3053-3054.
- F6 [reproduction, no defect] C1 at A1 and C2 at A2 both reproduce with byte-identical labels,
  counts and instrument digests; the h4 and h5 controls re-scored at F both exit 1 as the committed
  transcript records. The C1 `exec` cell records 154 candidate invocations and 0 violations.
- F7 [limits confirmed] The two documented blind spots hold under the probes: a forged `c_adler`
  (with the header checksum byte rewritten) passes the rule — the candidate answers `ok intact`
  rc 0 while `upx -t` refuses rc 1 — and the `u_adler` test that would catch it needs the codec.
  The new compressed-data `truncated` refusal is reachable independently of the round-99
  aligned-end rule (round-99 answers `ok intact` rc 0 on the same bytes).

## Out of scope (not done by this seat)

- The lane corpus was not edited: the entry and the README rows at `b0a7bb8c` were read only, and
  the draft lives in this wave dir. Whether to fold F1-F5 into the lane copy is the integrator's
  call.
- `corpus/lessons/round-100.md` (ScribeLesson's item) was not written; no lesson text was edited.
- No claim was re-frozen, re-pinned or re-scored; the frozen predicate and receipts are cited as
  they stand. No git or jj mutation was made in the lane or the fleet repo (read-only git only);
  scratch was created under `$HYAKU_SCRATCH/kaidoku-r100/ScribeEntry` and deleted on exit.

Report: .ufo/waves/round-100/w1/ScribeEntry.md
