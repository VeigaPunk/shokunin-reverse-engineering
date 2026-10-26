# R36ScribeProvince — PROVINCE.md text drafts (round 36, wave 1)

Seat: leaf scribe, no subagents, advisory only. Axes touched: coverage (R36-C1) and calibration
(R36-C2) surfaces, as **text drafts** only — `PROVINCE.md`, `SHONEN.md` and the knowledge entry were
**not** written or modified by this seat; this file is the only write.

Measured state at draft time: lane HEAD `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`
(`git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse HEAD`), `PROVINCE.md` 359 lines,
no local modification of `PROVINCE.md` (`git status --porcelain` showed only untracked
`.ufo/waves/round-36/*` files). Freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`; base
`cab59f221fe19726b5692bfa4d9a9679e96b8a73`; C1 controls `6a870b9290e9566468d7d9e6d1b8308daf025b12`;
C1 after receipts `3310d8fa27bfaa95ad858c4aaad6f6377f853982`.

---

## 0. Line arithmetic (the thing every other draft depends on)

Two independent inserts, applied in either order (the appended section is at EOF, after the
insertion point at 119, so it cannot move the `## Adjacent` range):

| Edit | Insert point (current file) | Lines added | Effect |
|---|---|---|---|
| D3 Adjacent append | after line 118 (`- ... licensed for reuse \`(unowned)\`.`) | 7 (new lines 119–125) | `## Adjacent` observed range `97-118` → **`97-125`**; every line ≤ 118 keeps its number |
| D1 new Core section | EOF (after line 359) | 14 + 1 blank separator | heading lands at **line 368**; file becomes **374 lines** |
| D2 Frontier pointer note | last line of the D1 section | (inside D1's 14) | lands at **line 374** |

Post-edit positions the drafts cite: Frontier `- **sasquatch**` bullet **156-157** (was 149-150);
`### Round-4 frontier (post-unlock)` still starts at 135.

Verified by simulation, not arithmetic by hand — `PROVINCE.md` copied to scratch, both inserts
applied, then the frozen counters' own readers were imported and run on the result
(`python3` with `importlib` over `tools/round-36/c2-counter.py` `heading_range` and
`tools/round-36/c1-counter.py` `section`/`cells`), exit 0, printed:

```
adjacent_range (97, 125)
119 - **Tooling, dated 2026-10-26** — the 2026-10-19 operat
156 - **sasquatch** — unblob's squashfs recursion extractor
368 ## Round-36 additions to Core
374 Frontier note, 2026-10-26: the `- **sasquatch** — …` bu
total 374
section found True
row_ok True
```

`row_ok True` is the frozen C1 row predicate itself
(`cells(row)[0]` word-contains `sasquatch` **and** `ENTRY in row`) applied to the D1 row below.

---

## 1. D1 — new section `## Round-36 additions to Core` (append at EOF)

Append after the current line 359 (the `## Round-32 additions to Core` limits paragraph), separated
by one blank line. Verbatim:

```
## Round-36 additions to Core

| Surface | Ports / keys | Probe | Verified evidence |
|---|---|---|---|
| sasquatch squashfs recursion | no new REA key — unblob 26.6.4 `unblob/handlers/filesystem/squashfs.py` runs `sasquatch` from `PATH` (`sasquatch-v4be` is its big-endian sibling, unmeasured); `REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4); sasquatch 4.5.1, official onekey-sec deb, at `~/.local/bin/sasquatch` (sha256 `ad02d27a…`) | `extract-firmware` on the four frozen carriers — K1/K2 synthetic LE v4 squashfs (xz; gzip 4 KiB blocks, nested dirs, a symlink), K3/K4 neovim v0.12.6 `nvim-linux-{x86_64,arm64}.appimage` — against the frozen `/usr/bin/unsquashfs` 4.7.5 regular-file oracle | carriers `corpus/evidence/round-36/c1/carriers.json`; receipts `corpus/evidence/round-36/c1/` (oracle 3, 4, 2,130, 2,130 regular files; every `after.json` carries zero `missing-extractor-dependency` gaps against one `dependencies: ["sasquatch"]` gap in the paired `before.json`, the only remaining after-gaps being `unpublished-entry` 0/1/2/2); `tools/round-36/c1-counter.py` binds each published file to its oracle relative suffix and sha256; entry `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` |

Frontier note, 2026-10-26: the `- **sasquatch** — …` bullet under `### Round-4 frontier (post-unlock)` (`PROVINCE.md:156-157`, frozen at `PROVINCE.md:149-150`) is superseded for the four measured carriers only; big-endian/AVM images and vendor-mangled images stay Frontier (`corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`).
```

Constraints an applier must not "improve" (each is counter-visible):

- The heading line must be **exactly** `## Round-36 additions to Core`. `c1-counter.py:30` sets
  `CORE_HEADING` and `section()` uses `lines.index(heading)` — an added date suffix
  (`(verified 2026-10-26)`, as every earlier Core section carries) makes the section unfindable and
  the C1 binding false. I verified no line equal to that heading exists today
  (`grep -c "^## Round-36 additions to Core$" PROVINCE.md` → `0`), so the heading is unique.
- Row 1's first cell must start with `sasquatch`; the row must contain the full entry path
  `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` (both hold; `row_ok True`).
- The table stays 4 columns (`Surface | Ports / keys | Probe | Verified evidence`) with a
  `|---|---|---|---|` separator; no `|` inside a cell.

Evidence provenance for the row's assertions, as observed by me read-only (no REA run, no counter
run):

| Claim in row | How observed |
|---|---|
| no new REA key; PATH discovery by unblob | `grep -rIn "sasquatch" /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` → **no match** (grep exit 1); `grep -rIn "sasquatch" /home/vgpnk/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob` → `handlers/filesystem/squashfs.py:25 EXECUTABLE = "sasquatch"`, `:26 V4BE_EXECUTABLE = "sasquatch-v4be"`, plus `unblob-26.6.4.dist-info/METADATA:83-87` (the `squashfs_1.0_$(dpkg --print-architecture).deb` install recipe) |
| unblob 26.6.4 | `~/.local/bin/unblob --version` → `26.6.4` |
| sasquatch 4.5.1 | `~/.local/bin/sasquatch -v` → `unsquashfs version 4.5.1 (2022/03/17)` (sasquatch is a squashfs-tools fork and self-reports under that name); `ls -l` → `382824` bytes; receipts record `sha256 ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` |
| oracle 4.7.5, file counts 3/4/2130/2130 | `/usr/bin/unsquashfs -version` → `unsquashfs version 4.7.5 (2026/03/01)`; `wc -l corpus/evidence/round-36/c1/K{1,2,3,4}/oracle.tsv`; K1 first rows are `README.txt`, `etc/config.ini`, `payload.bin` (no header row, so `wc -l` = regular-file count) |
| before gap names sasquatch; after has none; residual after-gaps are `unpublished-entry` | `python3` read of `normalized_result.extraction_gaps` in all eight receipts: before = `[("missing-extractor-dependency", ["sasquatch"])]` × 4; after = K1 `[]`, K2 `[unpublished-entry]`, K3 `[unpublished-entry, unpublished-entry]`, K4 same |

C1 controls (read from `.ufo/waves/round-36/controls/ctl-c1-*.json`): all three
`met_target: false`, `carriers_matched: 0`, `target: 4` — so a Core row here is not pre-empting a
kill-rule stop.

## 2. D2 — Frontier pointer note (append-only, no old-bullet rewrite)

Included as the last line of D1 above. It deliberately does **not** touch `PROVINCE.md:149-150`
(the old bullet text stands), and it carries both numbers: `PROVINCE.md:156-157` (post-edit truth)
and `PROVINCE.md:149-150` (frozen-claim identity, also the SHONEN/C1 wording). Both backticked
pointers resolve at any revision ≥ 374 lines.

## 3. D3 — `## Adjacent` reconciliation (append a dated bullet, 7 lines)

Insert **after the current line 118** and **before** the blank line at 119, inside `## Adjacent`
(so the section's contiguous-bullet style is kept). Verbatim:

```
- **Tooling, dated 2026-10-26** — the 2026-10-19 operator directive
  (`/home/vgpnk/.omp/agent/RULES.md`) lets an agent install or upgrade the
  tooling its task needs through official channels only, with tool, version,
  channel and reason recorded (round 36: sasquatch 4.5.1, official onekey-sec
  deb, into `~/.local/bin`); `rea setup` runs and client-config edits
  (registration refreshes for `claude_code`/`codex`/`grok_build`/`opencode`/
  `pi`) stay **operator-owned** and lane-untouched.
```

Rationale, kept to what the two texts actually say: `PROVINCE.md:110-115` ends "all
**operator-owned** … it never runs the installer", while `/home/vgpnk/.omp/agent/RULES.md`
(operator, 2026-10-19) grants *any* agent install/upgrade authority through an official channel
order, with every install recorded. The appended bullet narrows both claims to a non-contradictory
boundary: **lane tooling installs are now the lane's** (official channels, recorded), **`rea setup`
runs and client-config edits stay operator-owned**. It does not delete or reword the old bullet —
`PROVINCE.md:110-115` and its pointer cites (`SCORECARD.md:79` → `PROVINCE.md:107-109`,
`SKILL.md:357` → `PROVINCE.md:108-113`, `corpus/README.md:109,198` → `PROVINCE.md:114-116`) all keep
their line numbers because nothing at or below 118 moves.

## 4. SHONEN.md box 4 range (consequence, for the applier — `SHONEN.md` not edited here)

`SHONEN.md:12` asserts `PROVINCE.md:97-118` for the `## Adjacent` refusal list. After D3 the frozen
C2 reader (`c2-counter.py:151-164 heading_range(prov,'## Adjacent', …)` → heading line to last
non-blank line before the next `#` line) observes **`97-125`**. C2 case `R3 SHONEN box4 Adjacent
range` compares the stated range against that observation, so box 4 must be re-stated as:

- **`PROVINCE.md:97-125`** (was `97-118`; +7 for the round-36 tooling bullet).
- The "safety refusal at `:116-118`" clause inside the same box **stays correct** — D3 appends after
  118, it does not shift 116-118.
- Keeping the old `97-118` would leave it a *resolving but wrong* range: `c2-counter`'s `R3` check
  is an equality against the observation, so it would count as a mismatch (not merely stale prose).

---

## 5. Findings (reported, not repaired — advisory seat)

1. **After receipts still carry non-sasquatch extraction gaps.** `after.json`
   `normalized_result.extraction_gaps`: K1 `[]`, K2 `[unpublished-entry]`, K3 and K4
   `[unpublished-entry, unpublished-entry]`; `before.json` carries exactly one gap each, kind
   `missing-extractor-dependency`, `dependencies: ["sasquatch"]`. Any prose (D1 row, the knowledge
   entry, the round report) that says "no extraction gaps" overclaims; the frozen predicate only
   asks for *no sasquatch extraction gap*. D1's wording is the narrow one; the entry should match it.
   The earlier `grep -c 'missing-extractor-dependency'` over `after.json` printed `0` because the
   string is absent, **not** because the gap list is empty — a trap for `grep`-only checks.
2. **REA 6.5.0 has no sasquatch key or literal.** Zero occurrences of `sasquatch` in
   `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`; discovery is unblob-side
   (`unblob/handlers/filesystem/squashfs.py:25`). So the Core row must not name a
   `REA_SASQUATCH_*` env key (none exists), and "on `PATH`" is the load-bearing condition the
   before/after pair tests.
3. **`sasquatch-v4be` is the big-endian sibling** (`squashfs.py:26`) and is *not* installed/measured
   here. This is the mechanical reason the round's "not claimed: big-endian / AVM" fence is real, and
   D2 states it explicitly rather than just saying "superseded".
4. **D1's entry pointer does not resolve yet.** `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`
   is absent at `d2e46ef`; the C1 binding `province_core_row` requires the row to contain that path
   *and* the predicate requires the entry to exist and cite an `opened 2026-10-26` SOURCES row whose
   used-by lists it. D1 is therefore only landable together with C1's entry — drafting it early is
   safe (untracked/committed text does not trip a control), but the counter stays red until the entry
   exists.
5. **`PROVINCE.md` is not one of C2's units.** `c2-counter.py units()` reads only SCORECARD
   `## Owned axes`, SCORECARD `## Capabilities` rows and SHONEN boxes, and its `pointers()` skips
   tokens starting with `/` or `~`. So D1/D3's new backticked tokens (`/home/vgpnk/.omp/agent/RULES.md`,
   `~/.local/bin/…`) are outside C2's sweep. That is *not* permission to leave dangling pointers:
   every repo-relative token added by D1/D2 resolves in the simulated file
   (`corpus/evidence/round-36/c1/carriers.json`, `corpus/evidence/round-36/c1/`,
   `tools/round-36/c1-counter.py`, both `PROVINCE.md:` ranges), except the entry path noted in
   finding 4.
6. **`## Adjacent` heading is matched by prefix, first occurrence.** `heading_range` uses
   `startswith('## Adjacent')` + `next(...)`, so it takes line 97 and ignores the later
   `## Adjacent — round-23 …` (269) and `## Adjacent — round-24 …` (300). Nothing in D3 may start a
   line with `#`, or the observed range would stop early.

## 6. Gates / commands run (all read-only; no counter executed)

| Command | Outcome |
|---|---|
| `grep -n "^## \|^### " PROVINCE.md` | 20 headings, `## Core` 38, `## Frontier` 73, `## Adjacent` 97, `### Round-4 additions` 121, `### Round-4 frontier` 135 |
| `grep -n "sasquatch" PROVINCE.md` | single hit: `149` |
| `awk 'NR>=106 && NR<=122'` / `NR>=145 && NR<=152` | Adjacent bullets 110-118 (installer bullet 110-115, safety 116-118); Frontier bullet 149-150; blanks 119-120; `### Round-4` 121 |
| `wc -l PROVINCE.md` | `359` |
| `grep -n "PROVINCE\.md:" SCORECARD.md SHONEN.md SKILL.md corpus/README.md` | cites at/below 118 (`:107-109`, `:108-113`, `:114-116`, `:8-14`, `:18`, `:24`, `:50`, `:10`) — none shift under D3; SHONEN box 4's `:97-118` is the one that must be re-stated |
| `grep -rIn "sasquatch" <rea-agents 6.5.0 root>` | no match (exit 1) |
| `grep -rIn "sasquatch" <unblob 26.6.4 site-packages/unblob>` | `handlers/filesystem/squashfs.py:25,26`; `unblob-26.6.4.dist-info/METADATA:83,86,87` |
| `~/.local/bin/unblob --version` / `~/.local/bin/sasquatch -v` / `/usr/bin/unsquashfs -version` | `26.6.4` / `unsquashfs version 4.5.1 (2022/03/17)` / `unsquashfs version 4.7.5 (2026/03/01)` |
| `wc -l corpus/evidence/round-36/c1/K*/oracle.tsv` | 3 / 4 / 2130 / 2130 |
| `python3` gaps read of all 8 receipts | before: one `missing-extractor-dependency`+`["sasquatch"]` each; after: 0/1/2/2 `unpublished-entry`, no sasquatch gap |
| `python3` simulation over `c2-counter.heading_range` + `c1-counter.section/cells` | `(97, 125)`, heading 368, note 374, total 374, `row_ok True`, exit 0 |
| read `.ufo/waves/round-36/controls/ctl-c1-*.json` | `met_target false`, `carriers_matched 0` in all three |

No REA run, no `c1-counter.py`/`c2-counter.py` execution against the lane (their verdicts remain
unobserved by this seat and unquoted as results).

## 7. Touched surfaces

- Written: this file only (`.ufo/waves/round-36/w1/R36ScribeProvince.md`).
- Not written: `PROVINCE.md`, `SHONEN.md`, `corpus/knowledge/*`, `corpus/SOURCES.md`, counters,
  carriers, oracle, receipts, plans, contracts.
- No VCS mutation (only `rev-parse`/`status --porcelain` reads). No `agent://all` message, no
  subagent, no background job.

## 8. Out of scope / limits

- I did not run REA, the harness, or either counter; `carriers_matched == 4` and `mismatches == 0`
  are **not** asserted here. D1's evidence cell states mechanisms and receipt facts I read, and
  attributes the file-level binding to `c1-counter.py` rather than claiming its verdict.
- Line numbers in D1/D2 are correct **only** if D3's 7 lines are applied; if the L1 lands D1 without
  D3, the Frontier bullet stays at 149-150 and D2 must be re-stated to `PROVINCE.md:149-150` alone.
- D1 lands at EOF by design (no shift to any earlier cited range). If the L1 prefers it elsewhere,
  re-run the two-counter simulation — the `## Adjacent` range is unaffected, but the heading line
  reported here (368) and any `PROVINCE.md:` pointer below the insertion point would move.
- [INFERENCE] `unpublished-entry` after-gaps are unblob not publishing non-regular members (dirs,
  the K2 symlink) rather than a defect; not verified — the claim's predicate does not depend on it,
  and neither draft asserts a cause.
- Scratch `/fast/scratch/hyaku/kaidoku-r36/R36ScribeProvince` was created for the simulation copy
  (`PROVINCE.draft.md`) and removed before yield; `TMPDIR` was pointed there and no `/tmp` files were
  created. Nothing cited here lives under scratch — every path above is inside the lane.
- No tool installed or upgraded by this seat (per the 2026-10-19 directive's recording duty:
  nothing to record). `sasquatch` 4.5.1 was already present at `~/.local/bin/sasquatch`
  (`382824` bytes, self-report `unsquashfs version 4.5.1 (2022/03/17)`); it was not reinstalled,
  removed or moved. No pacman transaction was attempted.

## 9. Artifact paths

- This report: `.ufo/waves/round-36/w1/R36ScribeProvince.md`
- Drafted targets (unmodified): `PROVINCE.md` (359 lines at `d2e46ef`), `SHONEN.md:12`
- Drafted citations: `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md` (absent at
  `d2e46ef`), `corpus/evidence/round-36/c1/{carriers.json,K1..K4/{oracle.tsv,before.json,after.json}}`
- Frozen readers used only for simulation: `tools/round-36/c1-counter.py`, `tools/round-36/c2-counter.py`
