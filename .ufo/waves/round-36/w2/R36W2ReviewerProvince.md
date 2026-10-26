# R36W2ReviewerProvince — PROVINCE.md diff review, base `cab59f22` → tip `01a44dbf`

Wave-2 falsification seat (leaf, no subagents). Scope: the PROVINCE.md hunk of the round-36 landing —
the `## Round-36 additions to Core` row, the Frontier note, the dated Adjacent tooling bullet — plus the
effect of the 7 inserted Adjacent lines on every earlier `PROVINCE.md:` pointer in `SKILL.md`,
`SCORECARD.md`, `SHONEN.md`, `corpus/README.md`.

Worktree state during review: HEAD `6f2ba761` (one commit past tip);
`git diff --name-only 01a44dbf 6f2ba761` lists only `.ufo/waves/round-36/w1-results.json`,
`w1/R36ReviewerQualityBar.md`, `w2-dispatch.json`, `w2-gen.py`, `w2-spec.json`, `w2.ready` — PROVINCE.md
and the three other checked files are byte-identical to tip, so worktree reads are tip reads. All git
use was read-only (`show`, `diff`, `log -S`, `rev-parse`, `status`); no lane file was modified; the
frozen counters were run with `--json-out` into my scratch only.

**Verdict: no disagreement found on any of the three review questions.** Every checked value in the
Core row reproduces from the committed receipts; both Frontier-note pointers are exact at their named
revisions; the Adjacent bullet is a faithful paraphrase of `/home/vgpnk/.omp/agent/RULES.md` and does
not widen the analysis province. Two minor observations (O1, O2) and one pre-existing staleness family
(O3, explicitly **not** caused by this round's insertion) are recorded below. Nothing to repair.

## 0. The diff itself

`git diff cab59f221fe19726b5692bfa4d9a9679e96b8a73 01a44dbf45913a1bdcabbbfb85b7bb9d232cb930 -- PROVINCE.md`
→ `1 file changed, 15 insertions(+), 0 deletions(-)`:

- **7 lines at tip :119-125** — the dated Adjacent tooling bullet, inserted after the safety-refusal
  bullet (:116-118) and before the blanks + `### Round-4 additions to Core (verified 2026-10-13)`
  (base :121 → tip :128). Zero deletions, so every line ≤ 118 is byte-identical base↔tip and every
  pointer to lines ≤ 118 is mechanically unaffected.
- **8 lines at the tail** — blank :367, `## Round-36 additions to Core` :368, blank :369, table header
  :370, separator :371, the sasquatch row :372, blank :373, the Frontier note :374 (last line of the
  374-line file).

The Frontier note's own arithmetic claim ("7-line Adjacent addition") matches the diff exactly.

## 1. `## Round-36 additions to Core` row (:368 heading, :372 row) — every value checked

| Row value | Check | Result |
|---|---|---|
| Surface: sasquatch squashfs recursion | row first cell contains `sasquatch` (counter red-case requirement) | ✅ |
| "no new REA key — unblob 26.6.4 `unblob/handlers/filesystem/squashfs.py` runs `sasquatch` from `PATH`" | `~/.local/bin/unblob --version` → `26.6.4`; installed handler `~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/handlers/filesystem/squashfs.py` sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` = S108's recorded tag-26.6.4 digest (byte-identical); handler `:25` `EXECUTABLE = "sasquatch"`, `:37-41` selects it for the LE path, `:68-69` `get_dependencies()` returns `[sasquatch, sasquatch-v4be]`; empirically: before-run (sasquatch stripped from PATH) gaps, after-run (on PATH) publishes — PATH-run confirmed | ✅ |
| "`sasquatch-v4be` is its big-endian sibling, unmeasured" | handler `:26` `V4BE_EXECUTABLE = "sasquatch-v4be"`, `:41` BE switch, `:50/:52` `-be`; entry `## What this is not claimed to show` states no BE/AVM carrier was run | ✅ |
| "`REA_UNBLOB_COMMAND=~/.local/bin/unblob` (26.6.4)" | version check above; key pre-existing in the `.bashrc:63-69` inventory (PROVINCE.md:26) | ✅ |
| "sasquatch 4.5.1, official onekey-sec deb, at `~/.local/bin/sasquatch` (sha256 `ad02d27a…`)" | `sha256sum ~/.local/bin/sasquatch` → `ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754` (prefix matches); `~/.local/bin/sasquatch -v` → `unsquashfs version 4.5.1 (2022/03/17)`; provenance in the entry `## Install provenance`: release `sasquatch-v4.5.1-6` (S107), asset `sasquatch_1.0_amd64.deb` 187244 B sha256 `efbc92bd…ade95`, members byte-identical, installed without dpkg (`ar x` + `tar -xJf`) | ✅ |
| Probe: `extract-firmware` on the four frozen carriers, K1/K2 synthetic LE v4 (xz; gzip 4 KiB blocks, nested dirs, a symlink), K3/K4 neovim v0.12.6 `nvim-linux-{x86_64,arm64}.appimage` | `corpus/evidence/round-36/c1/carriers.json` matches cell-for-cell: K1 `bare squashfs v4 LE, xz, 128 KiB blocks, synthetic`, K2 `…gzip, 4 KiB blocks, nested dirs + symlink, synthetic`, K3/K4 URLs + sha256 `b644d034…f29fb` / `8efcec73…e1c2` (equal to the claims file's digests) | ✅ |
| "against the frozen `/usr/bin/unsquashfs` 4.7.5 regular-file oracle" | `/usr/bin/unsquashfs -version` → `unsquashfs version 4.7.5 (2026/03/01)`; `K1/oracle-run.json` records `"unsquashfs": "unsquashfs version 4.7.5 (2026/03/01)"`, `regular_files: 3`, `squashfs_offset: 0`; oracle.tsv rows are regular files only (K2's 4 rows exclude its symlink, which surfaces only as unpublished-entry metadata) | ✅ |
| "oracle 3, 4, 2,130, 2,130 regular files" | `wc -l` on `K*/oracle.tsv` → 3 / 4 / 2130 / 2130 (no header row; K1 line 1 is data: `README.txt <sha> 59`) | ✅ |
| "all published after, none before" | `jq '.normalized_result.files\|length'` → before 0/0/2/2, after 3/4/2147/2147; K3/K4 before paths are only `firmware.bin_extract/0-<elf_end>.elf64_extract/carved.elf` and `firmware.bin_extract/<start>-<end>.squashfs_v4_le` (the carve; zero oracle members) | ✅ |
| "every `after.json` carries zero `missing-extractor-dependency` gaps against one `dependencies: ["sasquatch"]` gap in the paired `before.json`" | jq over all 8 receipts: before gaps = exactly one per carrier, `{"k":"missing-extractor-dependency","d":["sasquatch"]}` ×4; after gaps contain no `missing-extractor-dependency` | ✅ |
| "the only remaining after-gaps being `unpublished-entry` 0/1/2/2 for symlinks" | after gap kinds: K1 `[]`, K2 `[unpublished-entry]`, K3/K4 `[unpublished-entry ×2]` — no other kind; `unpublished_entries` all `kind:"symlink"` (K2 `../usr/share/doc/NOTICE`; K3/K4 `.DirIcon` and `nvim.png` → `usr/share/icons/hicolor/128x128/apps/nvim.png`) | ✅ |
| "`tools/round-36/c1-counter.py`" | exists; **I reran the frozen counter at the tip**: exit 0, `{"bindings": {…all seven true…}, "carriers_matched": 4, "carriers_unchanged": true, "met_target": true, "revision": "01a44dbf45913a1bdcabbbfb85b7bb9d232cb930"}`; selftest `{"selftest": "c1-counter", "cases": 14, "green_ok": 1, "red_ok": 13, "failures": []}` exit 0; committed receipt `.ufo/waves/round-36/after/c1-at-ffc81341.json` independently shows `met_target: true` at `ffc81341` | ✅ |
| "entry `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`" | exists (215 lines); cites S107/S108/S109 in its Sources table; `corpus/SOURCES.md:113-115` rows S107-S109 all `mined 2026-10-26` with used-by = that entry (counter bindings `entry_present`/`sourced`/`opened_source_rows` true) | ✅ |

Note for a future reader: S108 shows the handler's `get_dependencies()` returns **both** extractor
names, while the measured before-gap names only `["sasquatch"]`. Both facts are recorded as measured
(receipts) and as source-read (S108); the row claims neither contradicts the other, and none of its
values depends on resolving that unblob-internal detail.

Calibration corroboration (adjacent surface, not my primary scope): I also ran the frozen C2 counter at
the tip — exit 0, `{"assertion_mismatches": [], "guards_ok": true, "met_target": true, "mismatches": 0,
"revision": "01a44dbf…"}`. The committed C2 receipts cover `d2e46ef5` (`.ufo/waves/round-36/c2/after-at-d2e46ef5.json`)
and `ffc81341` (`.ufo/waves/round-36/after/c2-at-ffc81341.json`); no receipt at `01a44dbf` was committed,
so my run supplies the tip leg. Per lesson M36-3 the counter has named blind spots (unit-name keying,
first-match), so this is corroboration only — the authoritative stricter re-derivation belongs to the
wave-2 C2 seats.

## 2. Frontier note (:374) — pointer anchors

- **Tip `01a44dbf`:** `### Round-4 frontier (post-unlock)` at :142; the `- **sasquatch** — unblob's
  squashfs recursion extractor (AUR-only); 7z fallback / covers the carved-image path today.` bullet at
  **:156-157** ✅ (lines 142-149 and 150-162 are bullet lines only — no intervening heading).
- **Base `cab59f22`:** same heading at :135; the same bullet at **:149-150** ✅.
- Shift arithmetic: everything below :118 moves exactly +7 (135→142, 149→156, 150→157, 121→128) —
  consistent with the 7-line insertion and nothing else. The note's parenthetical is exact at both
  revisions.
- Content claims of the note: "(AUR-only) was wrong as a route statement" — grounded by the assimilated
  entry `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md` (S110: unblob README tag 26.6.4
  line 43 "Then install the required external extractor tools. On Ubuntu/Debian:" + line 49 "For
  SquashFS support, also install [sasquatch](…)"); "Big-endian/AVM and vendor-mangled images stay
  Frontier" — matches the entry's `## What this is not claimed to show`. "as measured above" is
  literally true: the Core row is :372, the note :374.

## 3. Dated Adjacent tooling bullet (:119-125) vs `/home/vgpnk/.omp/agent/RULES.md`

RULES.md (read in full) is headed `# Tooling directive — operator, 2026-10-19 (always on, every agent)`
and says agents "installs or updates any tool that helps its task or is a strict upgrade, with full
privilege, without asking first", with a channel order (pacman → uv tool → official release binary into
`~/.local/bin` → cargo/npm), "Official sources only", and "Record every install or update — tool,
version, channel, reason — in your report or handoff."

- The bullet's paraphrase — "lets an agent install or upgrade the tooling its task needs through
  official channels only, with tool, version, channel and reason recorded" — is **faithful**; it omits
  the channel *order* and the pacman update-safety gate, which do not distort the operative claim.
- The round-36 exercise it cites is real and correctly characterized: sasquatch 4.5.1 from the official
  onekey-sec release deb into `~/.local/bin` = RULES channel 3 ("official release binary into
  `~/.local/bin`"; pacman has no sasquatch package on this Arch host, uv tool N/A for a C binary).
  Recorded with tool/version/channel/reason in the entry's Install provenance, lesson S107, and commit
  `3310d8fa`'s message. ✅
- The client list in the bullet (`claude_code`/`codex`/`grok_build`/`opencode`/`pi`) matches the
  installer bullet :111-112 exactly. ✅
- **Does it widen the lane's province?** `[INFERENCE]` — it does **not** widen the analysis domain: it
  adds no Core surface, and it explicitly keeps `rea setup` runs and client-config edits
  **operator-owned** (:123-125), i.e. it narrows nothing and claims no new capability. What it does
  record is an operator-granted widening of *install permission* — from :110-115's blanket "it never
  runs the installer" to "may install task-needed tooling per the 2026-10-19 directive" — which is a
  fleet-wide grant (RULES.md applies to every agent/lane), dated, exercised once, with the install
  recorded. The capability itself (SquashFS recursion) is claimed in the Core row through the counter,
  i.e. the lane's normal evidence-gated growth, not through this bullet.

## 4. Earlier `PROVINCE.md:` pointers in the four files — effect of the 7 inserted lines

All 25 `PROVINCE.md:` matches enumerated (`grep -n 'PROVINCE.md:' SKILL.md SCORECARD.md SHONEN.md
corpus/README.md`). **None is invalidated by the insertion.**

| Pointer | Classification | Status at tip |
|---|---|---|
| SKILL.md:205 → `PROVINCE.md:18` | current-intent, < 116 | ✅ :18 carries the Kimi `config.toml:4126` pin it cites |
| SKILL.md:343 → `PROVINCE.md:15-26` | current-intent, < 116 | ✅ drift-prone + provider-key block spans 15-26 |
| SKILL.md:357 → `PROVINCE.md:108-113` | pre-round-30 token (landed `58116aa`, arc2-loop1-round1) | stale-by-2 (installer bullet now 110-115) — **pre-existing**, < 119, unaffected by this insertion; see O3 |
| SCORECARD.md:45 → `:23-26,68-73,144-153` | C5 row, baseline-anchored per SCORECARD.md:16-17 ("Line citations to pre-existing lane files refer to the baseline revision unless explicitly marked current") | ✅ verified at the card's baseline `66455858`: 23-26 = r5-audit C8 apktool note, 68-73 = r5-audit C1 pruned-bullets note, 144-153 = Signal/Cross-version bullets with r5-audit C1 notes |
| SCORECARD.md:79 → `:107-109` | baseline-anchored (adjudicated at :680 and :3118) | ✅ in its own frame |
| SCORECARD.md:593 → `:48`, :664 → `:114-116`, :666, :680, :705 → `:10,:18`, :749 → `:10,:18,:44`, :788 → `:18`, :1777 → `:18`, :1795/:1818/:1887/:1917 → `:50`, :3093 → `:24`, :3120/:3134 → `:45` | historical round records or < 116 | ✅ unaffected; :24 verified (v42 at tip :24) |
| SCORECARD.md:3118 → `107-109`/`114-116`; :3119 → `91-93,139-144,84-86,149-150,87-88,145-146,103-104` | round-3-era errata (a4f674b3 frame) | ✅ in their own frame (at a4f674b3, :149-150 was the adb bullet; at base it is sasquatch — different revisions, no conflict) |
| SHONEN.md:12 → `:97-125`, `:116-118`, `:119-125`, `:8-14`, `:24` | **refreshed this round** (`ffc81341`) | ✅ verified at tip: `## Adjacent` heading :97, section ends :125 (tooling bullet's last line); safety refusal :116-118; tooling bullet :119-125; "range was 97-118 before round 36" ✅ (base :97 heading, section ends :118); `:8-14`/`:24` pre-existing and < 116 |
| corpus/README.md:111, :202 → `:114-116` | pre-round-30 tokens (landed `b3cd790c`, arc2-loop1-round2); rows untouched by the round-36 diff (`git diff cab59f22 01a44dbf -- corpus/README.md` contains no `114-116`/Safety-verdict change) | stale-by-2 (refusal block now 116-118) — **pre-existing**, < 119, unaffected by this insertion; see O3 |

## Observations (minor, no defect)

- **O1 — note placement.** The PROVINCE Frontier note sits at file end (:374), ~215 lines below the
  bullet (:156-157) it supersedes, with no marker at the bullet itself; the parallel README note
  (`corpus/README.md:233`) sits directly under its bullet (:232). A reader scanning the Frontier
  bullet sees "(AUR-only)" with no local pointer to the supersession. The note is dated and grep-findable,
  so this is discoverability asymmetry, not an error.
- **O2 — implicit reconciliation.** :110-115 ("it never runs the installer") and :119-125 ("lets an
  agent install…") coexist without an explicit precedence sentence; SHONEN.md:12 characterizes the new
  bullet as "reconciling" the two. The dated bullet's scoping (official channels, recorded, rea
  setup/client-configs operator-owned) makes the precedence recoverable, but the file states it only
  implicitly.
- **O3 — pre-existing stale-by-2 pointer family (out of this round's causal scope).**
  `SKILL.md:357` (`:108-113`), `corpus/README.md:111` and `:202` (`:114-116`) are pre-round-30 tokens
  (landing commits `58116aa1`, `b3cd790c`) from when the Adjacent block sat two lines higher; the +2
  drift from Frontier additions `2832c5b3`/`2f18996d` is documented in SHONEN.md:12's own history
  clause, but these three tokens were never refreshed. They were already stale at base `cab59f22`, are
  untouched by the round-36 diff, and sit entirely below :119 — the 7 inserted lines did not move them.
  (`SCORECARD.md:664`'s `:114-116` is the same era but is baseline-anchored by the card convention, so
  it is not stale in its own frame.) Recorded here because the sweep surfaced them; repairing them is
  outside this seat's bounds.

## Residual risk / verification gaps

- The Core row's per-file member parity ("all published after") rests on the frozen counter plus four
  wave-1 seat reproductions; my own checks verified the receipt-level gap/file counts and reran the
  counter, but I did not independently re-extract any carrier (out of a reviewer seat's remit and
  unnecessary — the receipts are committed and the counter recomputes their evidence ids).
- The Frontier note's self-referential line pointers (:156-157 / :149-150) are fresh drift debt: any
  future insertion above :156 invalidates them. They are dated 2026-10-26, so re-derivable; the lane's
  own history (round-30 +2 drift, O3) shows this debt class is real.
- K4's oracle rests on unsquashfs alone (no qemu-aarch64 for the runtime cross-check) — stated in the
  entry itself; not a PROVINCE-row defect.

## Tooling record

No tool installed or updated. Used pre-existing host tools only: git (read-only), jq, python3
(`-I -B`, lane's frozen counters, receipts written to scratch only), sha256sum, coreutils.

## Scratch

`/fast/scratch/hyaku/kaidoku-r36/R36W2ReviewerProvince` (counter receipts `c1-at-tip.json`,
`c2-at-tip.json`, quoted verbatim above) removed after this report; nothing cited lives only there.
