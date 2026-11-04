# ScribeKnowledge — round-69 w1 scoped findings

Seat `ScribeKnowledge` (scribe, round 69 / w1 / attempt 1). Target repo path for the drafts:
`corpus/knowledge/2026-11-03-r69-packed-route-contract.md`, the PROVINCE `## Round-69 additions to
Core` block, and two `corpus/README.md` rows. Nothing tracked was edited; nothing was committed,
pushed, or run through `jj`. Scratch `/fast/scratch/hyaku/kaidoku-r69/ScribeKnowledge/` is removed
before this seat yields (receipts copied first).

## Drafted

| draft | bytes | sha256 | lands as |
|---|---|---|---|
| `.ufo/waves/round-69/w1/ScribeKnowledge/entry.md` | 25,860 | `fb939242815c8e238b94d45d076130237671ddfd747fb36bfd9eb96c0658ee62` | `corpus/knowledge/2026-11-03-r69-packed-route-contract.md` |
| `.ufo/waves/round-69/w1/ScribeKnowledge/province.md` | 4,184 | `e92ce87aa5235c057ada25115b81ff0bd618d56d16a017ffb2df3bd980db0bc0` | new `## Round-69 additions to Core` section in `PROVINCE.md` |
| `.ufo/waves/round-69/w1/ScribeKnowledge/readme-rows.md` | 2,950 | `ade03745cc1b0783594e1a525a939d79371f728d69f523b469c0572ced0ebd8f` | one `## Coverage map` row and one `## Knowledge` row (below the delimiter) in `corpus/README.md` |

`entry.md` opens with one `source:` line (S270, the `help.cpp`/`main.cpp` packer source, with
`doc/upx.1:164` as a secondary locator), then `verified-at:`, `recheck:`
and a predicate-shaped `status:` line; sections: the gate, the arm seam and the five mutations, the
typed contract, the three carriers, Limits, Evidence. There is **no** `## Corrections` section: no
prior entry states a fact this round contradicts. The round-68 entry's Frontier clause ("packed
libraries and static binaries") is superseded for exactly one carrier inside the new entry, not
rewritten.

Supporting artifacts staged in the same directory: `upx.1` (40,077 B, `09552b3c…`), `help.cpp`
(27,279 B, `0b893ca8…`), `main.cpp` (41,889 B, `a02c7cba…`), `upx-doc.txt` (37,208 B, `4dc547ed…`),
`SHA256SUMS` for the four, `check-receipt-exec3.json` (my `--check-receipt` run), and
`contract-probe-exec3.json` (my contract-probe run).

## Already-landed artifacts at this seat's read (reported, not edited)

The L1 (or another writer) landed round-69 corpus artifacts while this seat was drafting. They are not
my drafts and I did not touch them; the L1 must choose between them and the drafts above.

- `corpus/knowledge/2026-11-03-r69-packed-route-contract.md` **already exists** (6,306 B, mtime
  2026-11-03 23:42, untracked at read) and is a different, shorter text. My `entry.md` is the superset
  alternative (per-number receipt paths, both patch sites for all five mutants, the six-arm table, the
  exact three-carrier counts, Limits incl. the counter scope); if the landed text is kept, it needs the
  S-row reconciliation and the count correction below (the wording note is optional).
  - **S-row conflict (correction; two staged artifacts disagree).** The landed entry reads `S270` as
    the code row (`src/help.cpp:460-469`, `src/main.cpp:1174`), and `corpus/lessons/round-69.md:19-20`
    records S270 = `help.cpp` + `main.cpp` (code) as **ADMIT**, calling `doc/upx.1` "not a row — a
    secondary locator". But `corpus/SOURCES.md:187` (staged, uncommitted) defines **S270** as the
    generated manual page `doc/upx.1` (40,077 B, `09552b3c…`, `--version` at line 164). The scout's
    correction to this seat names the two consistent fixes, both validator-clean: (A, recommended)
    replace the staged S270 row with `row.S270.md` — the code row, `doc/upx.1:164` as the anchor's
    secondary locator; or (B) append the code row as **S271** and re-point the entry. `grep -c '^|
    S271 ' corpus/SOURCES.md` = 0. `entry.md` now follows A (one `source:` line, S270 = code,
    `doc/upx.1:164` secondary); under B, lines 3-18 substitute S271 for S270 and prefix the manual
    locator with S270.
  - **Source-scope caution (scout).** The manual's internal-checksum sentence (`doc/upx.1:112-114`) is
    about the compressed and uncompressed *files*, not the packer binary; the packer-binary sha256 pin
    is route policy (`tools/round-69/packed-elf.py:64-65, 257-259`). `entry.md` says so explicitly and
    does not use the manual as evidence for the pin.
  - **Lesson quote nuance (scout).** `corpus/lessons/round-69.md:19` quotes `help.cpp:465` (the
    `UPX_VERSION_GIT_DESCRIBE` branch); on a non-git build the emitted line is `:469`
    (`UPX_VERSION_STRING`), with `:465`/`:467` as variants. `entry.md` cites 460/465/467/469, not 465
    alone. This seat did not edit the lesson.
  - **Count error (correction).** The landed carrier table records `xxd`'s packed stub as
    `3 / 3 / 3`; the measured receipt records `3 / 3 / 6`
    (`procedure_count 3`, `segment_count 3`, `string_count 6`) — see
    `.ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json` and, identically, the round-68 receipt
    `.ufo/waves/round-68/l1/pre/c2-dryrun-at-base.json`. The L1's own landing receipt
    `.ufo/waves/round-69/l1/scores/c3-at-landing.json` records `3 / 3 / 6` as well, so the landed
    table's `3 / 3 / 3` is contradicted by both the seat receipt and the score receipt. `entry.md`
    carries `3 / 3 / 6`.
  - **Wording.** The landed Limits say "default packing mode (`upx --best`)"; the instrument's
    `PACKING_MODE` is `upx --best` and the receipt's pack argv carries `--best`, so "default" is the
    brief's word, not a recorded mode.
  - The landed `verified-at:` is the bare date and the `recheck:` line names no receipt; `entry.md`
    names the base receipts, the seat receipts and the landed score paths, and gives each counter's
    command with its expected output.
- `PROVINCE.md` already carries a `## Round-69 additions to Core` block (lines 466-472, one row) and a
  round-69 frontier note; the frontier note cites `S270` for the route (the man-page row). `province.md`
  is the alternative three-row block, with the per-carrier ceilings and the probe receipts.
- `corpus/README.md` already carries the round-69 Knowledge row at line 120 (first data row, below the
  delimiter; the round-68 row moved to 121) and has **no round-69 Coverage-map row**
  (`grep -n 'round 69\|round-69' corpus/README.md` matches only :120). `readme-rows.md` supplies the
  missing coverage row and a corrected replacement knowledge row (source cell `S271, S270, S269`, no
  "default packing").

## What this seat verified (observation)

1. **Frozen bytes.** `sha256sum` over the four round-69 instruments equals the declared pins exactly
   (`4ac0d83b…` packed-elf, `51b64c56…` mutation-check, `e609d85d…` contract-probe, `1f8f78c1…`
   controls); `tools/round-68/packed-elf.py` is `48ef4c68…`. `python3 -I -B
   tools/round-69/packed-elf.py --selftest` → exit 0, `{"cases": 20, "failed": [], "ok": true}`.
2. **Revision facts.** `git log --diff-filter=A --format=%H -- .ufo/waves/round-69/claims.json` →
   `f15998102f1ce3569e61faa2ac6f286bc414538e`; the same query for
   `tools/round-69/packed-elf.py` → `616a5f2f7aabe46f51f2ea06102766f7ce0e3428`; the base
   `d7d9a62c…` is a commit; `git cat-file -e d7d9a62c:tools/round-69/packed-elf.py` exits 128;
   `git show d7d9a62c:tools/round-68/packed-elf.py | sha256sum` → `48ef4c68…`. Lane HEAD at read:
   `3f3d20fc…` (the wave-dispatch commit). `.ufo/waves/round-69/w1/ReviewerGates/freeze-integrity.json`
   records all four pins equal between freeze and working bytes, `freeze_to_main_rc 0`,
   `freeze_to_main_diff ""`.
3. **Base receipts** (read, not re-run): `c1-at-base.json` — r68 patch set, five survivors, each
   `applied true`, `cases 13`, `failed []`, `verdict survived`; `pristine.cases 13`, `ok true`.
   `c2-at-base.json` — `arms_passed 0` of 6, all six named, with A1/A2 Python tracebacks (rc 1) and
   A3/A4 argparse `unrecognized arguments: --upx`. `c3-at-base.json` — exit 1, `target 2`,
   `carriers_matched 2`, `kinds [null]`, no shared-object carrier, both ratio clauses `None > 0.75`.
   `controls-at-base.json` — seven arms, `ok true`.
4. **Three-carrier receipt** (seat receipt, read): `.ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json`
   — closure `{carriers_matched 3, target 3, control_ok true, met_target true}`, `failing []`,
   `rev 3f3d20fc…`, instrument `{sha256 4ac0d83b…, rev 616a5f2f…}`; counts jq 167/30/190 → 3/3/3 →
   167/30/190, xxd 99/29/103 → 3/3/6 → 99/29/103, libz 184/29/199 → 98/6/136 → 184/29/199; ratios
   0.0599 / 0.101 / 0.6522; `kinds [executable, executable, shared-object]`; `jq` refusal packed rc 1
   `invalid_request` vs unpacked rc 0 with 4,841 bytes; control `list_rc 2`/`decompress_rc 2` on all
   three.
5. **My own counters over that receipt.**
   `python3 -I -B tools/round-69/packed-elf.py --check-receipt .ufo/waves/round-69/w1/ExecC3/c3-at-landing-exec3.json`
   → exit 0, `met true`, `target 3`, `carriers_matched 3`, `failing []`, `kinds ["executable",
   "shared-object"]` (`.ufo/waves/round-69/w1/ScribeKnowledge/check-receipt-exec3.json`).
   `python3 -I -B tools/round-69/contract-probe.py --root <LANE> --rev f1599810… --tool
   tools/round-69/packed-elf.py --pkg <REA> --work <SCRATCH> --receipt <that receipt> --json-out …` →
   exit 0, `arms_passed 6` of `target 6`, `failed []`, `instrument_sha256 4ac0d83b…`
   (`.ufo/waves/round-69/w1/ScribeKnowledge/contract-probe-exec3.json`).
6. **Host pins re-derived.** `/usr/lib/libz.so.1.3.2` = `6c78c5e5…`; `/usr/bin/jq` = `e8156675…`;
   `/usr/bin/xxd` = `7b1e5d0c…` and `readlink -f` → `/usr/bin/tinyxxd`; `/usr/bin/upx` = `cf2f6e7c…`,
   `upx --version` first line `upx 5.2.0` (second line `UCL data compression library 1.03`);
   `readelf -h /usr/lib/libz.so.1.3.2` → `ELF64`, `2's complement, little endian`, `DYN (Shared object
   file)`, `Advanced Micro Devices X86-64`; REA `package.json` = `a5003023…`, version `6.5.0`.
7. **Sources opened** (fetched this seat, digests equal the declared ones): `doc/upx.1` (40,077 B,
   `09552b3c…`; `--version` at line 164; internal-checksum sentence at lines 112-114), `src/help.cpp`
   (27,279 B, `0b893ca8…`; `void show_version(bool one_line) {` at line 460, banner `fprintf`s at
   465/467/469), `src/main.cpp` (41,889 B, `a02c7cba…`; `{"version", 0, N, 'V' + 256}` at line 834,
   `strcmp(argv[i], "--version")` at line 1174), `doc/upx-doc.txt` (37,208 B, `4dc547ed…`; line 99).

## Sibling state, quoted where it matters (reported, not resolved here)

- **S-row id shuffle.** `corpus/SOURCES.md:187` now carries **S270** = the generated man page
  `doc/upx.1` (40,077 B, `09552b3c…`, `--version` at line 164). The scout's earlier message called S270
  the `help.cpp`/`main.cpp` code row; the row it actually drafted in its directory is
  `.ufo/waves/round-69/w1/ScoutSource/row.S271.md` — **S271**, code kind, tag object `bc521d8d…` →
  commit `034b6d0d…`, `help.cpp` `0b893ca8…` and `main.cpp` `a02c7cba…`. `grep -c '^| S271 ' corpus/SOURCES.md`
  = 0 at this seat's read. **Landing dependency:** if S271 is not appended, `entry.md`'s first
  `source:` line dangles. Entry cites S271 (code) and S270 (man page); S269 (byte identity) is cited
  only in Limits.
- **ExecC1** (independent applier): "**Verdict: the R69-C1 predicate sentence holds at the freeze**,
  for both the constant-`True` mutants [and the behavioural family]" —
  `.ufo/waves/round-69/w1/ExecC1/rederive.md`; its receipts `battery-r69.json` (`survivors []`,
  `pristine.cases 20`) and `battery-r68.json` (five survivors, `pristine.cases 13`) agree.
- **ExecC2** (independent contract harness; it did not run the frozen probe): the six arms are all
  typed on its own fixtures and the before side is 0/6, all six named; it reports contract-shape leaks
  **outside** the six arms — U1 `upx-enoexec` rc 1 `OSError: Exec format error`, U2 `upx-unreadable`
  rc 1 `PermissionError`, U11 `node` with a bad shebang rc 1, U9 a bogus `--rev` accepted into the
  receipt, U8 a missing `--root` giving a free-form `git … failed: rc=128` with no class token
  (`.ufo/waves/round-69/w1/ExecC2/rederive.md`, `arm-receipt.json`). Its own words: "No clause of
  R69-C2's kill rule fires on the honest evidence … The gaps I did find (F1–F8 in `ExecC2.md`) are
  outside the six named arms: they are contract-shape leaks and evidentiary boundaries, not predicate
  falsifiers." `ExecC2.md` was not present at this seat's read; only `rederive.md` was. `entry.md`
  records the U1/U2/U9 shape in `## Limits`, not as a claim clause.
- **ReviewerGates** (`.ufo/waves/round-69/w1/ReviewerGates/attacks.json`) ran the frozen battery at
  the freeze: `battery-r69` rc 0, `survivors []`, five kills each naming its declared case,
  `pristine.cases 20`; `battery-r68` rc 0, five survivors, `pristine.cases 13`. Its counter attacks on
  `--check-receipt` are **reported verbatim for the canonical judge**: `missing-identity-arm` rc 0,
  `met true`; `one-carrier-no-arms` rc 0, `met true`; `nan-ratio` rc 0, `met true`;
  `boundary-075` rc 0, `met true`; `boundary-over075` rc 1 (`0.7501 > 0.75`); `explicit-false-arm`
  rc 1 (`jq:identity_ok false`). Its validator probes: `mutation-invented-kills` rc 0 (`mutants 1`,
  `defects []`) and `probe-invented-arms` rc 0 (`arms 6`, `defects []`) — i.e. both `--validate`
  paths accept a receipt row the attacker invented. Its `foreign-probe` is 6/6 against a receipt whose
  carrier `name` fields read `wrong-name` (A5 checks presence and re-derives pin/format/mode, not the
  name value). `entry.md`'s counter-scope Limits bullet records the `arms`-map and identity-field
  gaps without treating synthetic receipts as evidence.
- **ExecC3** (`.ufo/waves/round-69/w1/ExecC3/verify.md`): no mismatch between the route receipt and
  its own derivation; two structural notes, both **not** mismatches — (a) `before_ceiling_ratio` is
  ceiling/original (120/184), not packed/original (98/184 = 0.5326); (b) `section_count` records the
  packed file's count, not the original's. Its generalisation probe: `/usr/lib/liblzma.so.5.8.4`
  `6e4dae5b…`, 417/29/227 → 175/6/177 → 417/29/227, ratio 175/417 = 0.4197, byte-identical unpack; the
  same constant ceiling 120 would be false for it. Both notes are now in `entry.md` (`## Limits` and
  the ratio paragraph).

## Not verified by this seat (unknown)

- **The L1's landing receipts appeared at 23:46 and were read.** `.ufo/waves/round-69/l1/scores/`
  holds `c1-at-landing.json` (rev `5ee94c56…`, `survivors []`, five kills naming their declared cases,
  `pristine.cases 20`), `c1-before-recheck.json` (five survivors, `pristine.cases 13`),
  `c2-at-landing.json` (`arms_passed 6`, `failed []`, `instrument_sha256 4ac0d83b…`, scored against
  `c3-at-landing.json`), `c3-at-landing.json` (`target 3`, `carriers_matched 3`, `control_ok true`,
  `met_target true`, `failing []`), `c3-check-at-landing.json` (`met true`, `kinds ["executable",
  "shared-object"]`) and `provenance-at-landing.json` (`met true`). Every value equals the drafts'
  tables, so the drafts now cite them in `verified-at:`/Evidence. What remains open is only the
  landing **choice** (the landed entry/rows above vs these drafts) and the S270/S271 reconciliation.
  My own auxiliary runs were at the operative freeze `f1599810` (C2 probe, and ReviewerGates' C1
  battery), and ExecC3's route receipt is at `3f3d20fc…`; the drafts name the landing receipts for the
  scored values and the seat receipts as corroboration.
- I did **not** run the mutation battery myself (I read two independent runs: ReviewerGates' and
  ExecC1's), and I did **not** re-run the route over the carriers (I read ExecC3's receipt and
  re-derived the host pins, libz's `readelf -h` and all four source digests myself). No count of mine
  is presented as a route measurement.
- The `format` values for `jq`/`xxd` in `entry.md` come from ExecC3's receipt (and reproduce the
  round-68 receipt); I re-derived only libz's `readelf -h` header.
- Whether the round-68 knowledge entry's own R68-V1 correction block lands this round is outside this
  seat (ExecLedger).

## Conflict with the seat brief (verbatim)

The brief asks Limits to name "default packing mode". The frozen instrument records
`PACKING_MODE = "upx --best"` (`tools/round-69/packed-elf.py:66`), every carrier's `packing_mode` in
both the round-69 receipt and the round-68 receipt reads `upx --best`, and both recorded pack argvs
carry `--best`. `entry.md` states `upx --best` and says no other mode was measured. This is a wording
mismatch in the brief, not an instrument or receipt discrepancy.

## Out of scope / not done

- No tracked lane file was created or edited; no `corpus/`, `PROVINCE.md`, or `README.md` edit; no
  SOURCES row authored (the scout's S270-replacement / S271-append decision is the dependency); no
  commit, push, or `jj` command; no
  subagent dispatch; no mutation of any frozen instrument or carrier.
- No claim was narrowed, widened, or re-frozen; the drafts restate the predicates verbatim in
  `status:`.

## Tools installed

None. No package manager transaction was run (pacman is paused host-wide); no tool beyond the
pre-installed `python3`, `curl`, `sha256sum`, `readelf`, `git`, `/usr/bin/upx` 5.2.0 and `node` was
needed.

## Scratch

`/fast/scratch/hyaku/kaidoku-r69/ScribeKnowledge/` held the four source fetches and the two counter
runs; the sources and both receipts were copied into the wave directory first, and the scratch tree is
removed before this seat yields.
