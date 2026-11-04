# ScribeKnowledge — round-84 knowledge entry draft (R84-C3, nested container chain)

Seat: `ScribeKnowledge` (scribe, round-84 wave `r84-w1`) · Lane `kaidoku-shokunin` · L1 `KaidokuR84`
Frozen plan: `plans/round-84-claims.md` · Declaration `e0de2088a7bddc16305357f90ac7e889fa0a0d11` ·
First container `a5663ddedd157bb9113928f5fe80509d6f3fc7a1` · Base `043b89a25241710a68b45526c3287fb3c8d907c3`
Milestone: claim metadata, mutation closure, nested container chain. Scope: **R84-C3 knowledge entry
draft only**. Leaf member — no subagent dispatch, no `task` spawns, no sibling-lane writes.

## Behavior — what this seat did

Drafted the round-84 knowledge entry `2026-11-04-r84-nested-container-chain.md` **into this seat's
wave directory only**. Nothing was written under `corpus/`, `PROVINCE.md`, `corpus/README.md`,
`corpus/SOURCES.md` or any production file; no predicate, counter, mutant table or fixture was
touched; no git/jj mutation, commit or push was performed. Only read-only git was used
(`git log`, `git ls-tree`, `git show <rev>:<path>`, `git status`, `git diff`).

- Draft: `.ufo/waves/round-84/w1/ScribeKnowledge/2026-11-04-r84-nested-container-chain.md`
  (11 551 B, sha256 `16d420c184675dd4d2c9ea127738c91fc3dadea81587de02a11261f8efdcc99f`).
- Candidate patch against the L1's working-tree copy of the same entry:
  `.ufo/waves/round-84/w1/ScribeKnowledge/knowledge-entry.patch` (unified diff, 18 115 B, sha256
  `07daaff302fc0b5d31b73300166211f317b4bde848f6212b0283943a2d993b8f`).
- Receipts (all copied out of scratch): `c3-scribe-receipt.json` (frozen blob run),
  `nested-selftest.json`, `analysis-depth-key-probe.json` (+ its `probe_key.py`),
  `probe-draft-S301.json`, `probe-draft-S302.json`, `probe-l1-s301.json`, `probe-l1-s302.json`,
  plus `receipts.sha256`.

## Gates exercised

| gate | command | outcome |
|---|---|---|
| R84-C3 counter, frozen blob at the first container | `git show a5663dde:tools/round-84/nested-sqfs.py > <scratch>/nested-sqfs-frozen.py` (sha256 `08353f36…`) then `python3 -I -B <scratch>/nested-sqfs-frozen.py --rev a5663ddedd157bb9113928f5fe80509d6f3fc7a1 --work <scratch> --json-out <receipt>` | exit 0, `met true`, `arms` A1–A9 all true, `control.fires true`, `instrument.sha256` `08353f36…` |
| R84-C3 counter selftest (frozen blob) | `python3 -I -B <scratch>/nested-sqfs-frozen.py --selftest --json-out <receipt>` | exit 0, `cases 7`, `failures []` |
| level-3 `analysis_depth` key presence (direct envelope probe) | own scratch probe: rebuild the same chain, run `npx -y rea-agents@6.5.0 extract-firmware … --max-depth 3 --format json`, read each file record | all 8 records **carry the key**; the three level-3 files have value `null` (not a dropped key) |
| house source grammar (round-83 frozen reader) | `python3 -I -B tools/round-83/source-bind.py --entry <draft> --sid S301` | rc 0, `cites true`, `status attributed` |
| same, S302 | `python3 -I -B tools/round-83/source-bind.py --entry <draft> --sid S302` | rc 0, `cites true`, `status attributed` |

The counter runs wrote only under `/fast/scratch/hyaku/kaidoku-r84/ScribeKnowledge/` and their own
`--work` trees; the scratch tree was removed after the receipts were copied into the wave dir.

## Content delivered in the draft

- **Opening `source:` field**, line 10 (within the first twelve lines), a single field whose value
  begins with the comma-separated leading list `S301, S302` followed by ` — `. S301 is the
  mksquashfs(1) `-repro-time` documentation, opened 2026-11-04, with the 24-word quote
  "build a reproducible filesystem image. This is equivalent to specifying -mkfs-time TIME and
  -inode-time TIME, which achieves reproducibility by setting all timestamps to TIME."
  (derived-text lines 168-174 of the retained 57 790 B snapshot,
  sha256 `3ea8c1a1b429a5da35c7ffa0719ee2dade48ab8566c099c02b2c25bbe2052765`). S302 is the
  provider's own `depth-limited` remedy text with its 18-word quote.
- **Bounded class**: lane-built standard **little-endian** SquashFS **v4**, **gzip**, **three
  levels**, `mksquashfs 4.7.5 -noappend -comp gzip -b 4096 -repro-time 1760000000`, read through
  REA 6.5.0 `extract-firmware` on unblob 26.6.4. Fixture pins `a e82c5995…`, `b 7d2dd0e7…`,
  `c f68b42fa…`, with `b_is_oracle_member` / `c_is_oracle_member` true against the independent
  `unsquashfs 4.7.5` oracle.
- **Measured values**: 8/8 oracle members published at **both** depths with matching bytes and the
  full digest table (three container images + five regular files); depth 3 → `coverage partial`,
  exactly **one** `depth-limited` gap and one `depth_limited_paths` entry, both at the deepest
  extract root `…/inner-b.sqfs_extract/inner-c.sqfs_extract`, level-3 files `analysis_depth null`;
  depth 4 → `coverage complete`, no gap, level-3 files `analysis_depth 3`; engine identity equal
  across both runs (unblob 26.6.4, executable sha256 `0ce7b624…`, `worker_count 1`).
- **The reading that publication is not analysis**, with the file-count-only rule named as the
  counter's control that fires on exactly this case, and the provider's own remedy text.
- **Explicit not-covered list**: vendor/externally supplied images; compressors other than gzip;
  block sizes other than 4096; AVM/BE layouts; depth beyond three (chain depth > 3; extraction
  depths other than 3 and 4; provider ceiling `max_depth` 10); providers other than unblob 26.6.4;
  files beyond the provider's file/byte budget (staging entries default 10 000 / max 100 000;
  staging bytes default 256 MiB / max 512 MiB); chains with several containers per level and
  non-regular members.
- **`verified-at:` and `recheck:` fields**, both present, with the counting command, the selftest
  command and the source-side re-fetch instruction.

## Receipt provenance — what exists at the first container, and what is planned

Receipts that **exist at the first container** `a5663ddedd157bb9113928f5fe80509d6f3fc7a1` and are
cited as existing: `.ufo/waves/round-84/pre/c3-pilot.json` (sha256
`f45f018cdee6ce47daca6acbfb96674a9c0150fff834cc631fe6b25f5fb9cffa`; `met true`, A1–A9 true,
`control.fires true`, instrument sha256 `08353f36…`), and the claim container
`.ufo/waves/round-84/claims.json` (instrument pins). The mksquashfs snapshot
`.ufo/waves/round-84/l1/sources/mksquashfs.1.en.html` is present in the lane **working tree** but
uncommitted at that container.

Marked **planned, not present** in the draft: `.ufo/waves/round-84/l1/scores/c3-at-landing.json`
(the landing receipt the plan names; the path does not exist in the lane at this writing), and this
seat's own wave-local receipt `.ufo/waves/round-84/w1/ScribeKnowledge/c3-scribe-receipt.json`
(a wave artifact, not a first-container path).

## Findings (verbatim, for the canonical Rust judge)

1. **The L1's working-tree entry `corpus/knowledge/2026-11-04-r84-nested-container-chain.md` has
   two line-start `source:` fields (lines 11 and 12).** Under the frozen round-83 house grammar
   (`tools/round-83/source-bind.py`, "exactly one line-start `source:` field within the first
   twelve lines"), a duplicate field is unbound: running the frozen reader against that file gives
   rc 1, `cites false`, `status not-attributed` for **both** S301 and S302 (receipts
   `probe-l1-s301.json`, `probe-l1-s302.json`). The same reader gives rc 0 / `cites true` for both
   ids against this seat's draft, which uses one comma-separated leading list (`S301, S302`).
   I did not modify the L1's file; the diff is offered as `knowledge-entry.patch`.
2. **The counter's `--rev` argument is a caller-supplied label**, recorded in the receipt's `rev`
   field; it does not check out a revision. What binds the measurement is `instrument.sha256`
   (equal to the digest frozen in `.ufo/waves/round-84/claims.json`), the `chain.pins` and the
   `expected` oracle digests. The draft says so explicitly.
3. **The L1's PROVINCE addition and the plan disagree on the depth ceiling wording** — the plan's
   frontier note says "chains deeper than four"; the class measured here is a three-level chain
   and the provider's own schema caps `max_depth` at 10. The draft's not-covered bullet names
   chain depth > 3 and extraction depths other than 3 and 4, and quotes the provider ceiling, so
   the entry does not inherit either number silently.
4. **`corpus/SOURCES.md` in the working tree already carries rows S301/S302/S303** (S301 and S302
   `mined`, S303 `rejected`), and S301/S302 `used-by` already names
   `corpus/knowledge/2026-11-04-r84-nested-container-chain.md`. That row set was written by
   another seat; this seat only read it. The registry census at round start was 205 rows
   (A187/B10/C8, mined 184/rejected 21) per `.ufo/waves/round-84/l1/sources/round-84-sources.json`.
5. **The working tree's `tools/round-84/nested-sqfs.py` drifted from the frozen pin during this
   seat's work.** At the first container the blob is sha256 `08353f36…`; the working-tree file was
   observed at `e0364dde…` and later `938801ba…` (another seat's edits — a `deepest-unanalyzed`
   arm that now requires the `analysis_depth` key to be *present*, plus a selftest case). My first
   counter run therefore recorded `instrument.sha256` `e0364dde…`, which is **not** the frozen pin.
   I discarded that receipt and re-ran the counter from `git show
   a5663dde:tools/round-84/nested-sqfs.py` (a scratch copy, byte-identical to the frozen pin
   `08353f36…`); the retained receipt `.ufo/waves/round-84/w1/ScribeKnowledge/c3-scribe-receipt.json`
   carries `instrument.sha256` `08353f36…`, equal to `.ufo/waves/round-84/claims.json`. Both runs
   agree on all nine arms and the control. I edited no counter byte.
6. **The frozen counter's level-3 arm reads "value is null", which also accepts a dropped key.**
   The `analysis_depth` key-presence probe above shows the key is genuinely present with value
   `null` on all three level-3 files, so the entry's claim is sound on its own evidence; the
   frozen arm alone would not have distinguished the two. The draft says so, and marks the probe
   as a wave-local observation rather than a first-container receipt.
7. **No `considerthese` directory exists in this lane** (`find . -maxdepth 3 -type d -name
   considerthese` → no output).

## Out of scope (not done by this seat, deliberately)

- No write into `corpus/` — the entry draft stays in the wave directory; L1 integrates.
- No edit to `PROVINCE.md`, `corpus/README.md`, `corpus/SOURCES.md`, `SKILL.md` or the three
  round-84 tools; no edit to `plans/round-84-claims.md`, `mutants.json`, `claims.json`.
- No C1/C2 predicate work, no mutation testing, no registry rows, no lesson file, no freeze-ledger
  row, no source census: those belong to the other seats and to L1.
- No tooling was installed or upgraded, so there is no tool/version/channel/reason record beyond
  the pre-existing toolchain the receipts name (mksquashfs and unsquashfs 4.7.5, Python 3.14.8,
  node/npx with `rea-agents@6.5.0` from the npx cache, unblob 26.6.4 at
  `~/.local/share/uv/tools/unblob/bin/unblob`). No pacman, no PATH-directory writes, no host
  service touched.

## Artifact paths

- `.ufo/waves/round-84/w1/ScribeKnowledge/2026-11-04-r84-nested-container-chain.md` — the draft entry.
- `.ufo/waves/round-84/w1/ScribeKnowledge/knowledge-entry.patch` — diff against the L1's copy.
- `.ufo/waves/round-84/w1/ScribeKnowledge/c3-scribe-receipt.json` — this seat's independent R84-C3
  run, executed from the first-container blob (`instrument.sha256` `08353f36…`).
- `.ufo/waves/round-84/w1/ScribeKnowledge/nested-selftest.json` — counter selftest (7 cases, 0 failures).
- `.ufo/waves/round-84/w1/ScribeKnowledge/analysis-depth-key-probe.json` and `probe_key.py` — the
  level-3 `analysis_depth` key-presence probe (all eight records carry the key; three are `null`).
- `.ufo/waves/round-84/w1/ScribeKnowledge/probe-draft-S301.json`, `probe-draft-S302.json` — frozen
  source reader against this draft (both `cites true`).
- `.ufo/waves/round-84/w1/ScribeKnowledge/probe-l1-s301.json`, `probe-l1-s302.json` — the same
  reader against the L1's working-tree entry (both `cites false`; finding 1).
- `.ufo/waves/round-84/w1/ScribeKnowledge/receipts.sha256` — digests of the above.
- Scratch `/fast/scratch/hyaku/kaidoku-r84/ScribeKnowledge/` — removed before this report.
