# R42Assim — assimilation review (read-only package `merge/kaidoku`), round 42 wave 1

**Verdict: DONE — 2 admit (one after rewrite), 2 reject; 5 defects routed; the staged entry's own
`recheck:` command reproduced.** No campaign tool was run, nothing was written to
`/home/vgpnk/Projects/shokuknow`, no file outside this seat's report and artifacts directory was
touched, and nothing in the lane tree changed (this seat's writes are `R42Assim.md` and
`artifacts/R42Assim/` only).

Seat: `R42Assim`, scribe/assimilation. Leaf: no subagents, no background jobs, no `agent://all`.
Base read: `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c`. Host tools used read-only: `curl`,
`sha256sum`, `unsquashfs` 4.7.5, `~/.local/bin/sasquatch-v4be` (one refusal run), `python3`.
**No tool installed or upgraded**; no pacman transaction; no REA call; no unblob run.

## Axes

| axis | what this seat moves |
|---|---|
| **coverage** | two package entries become landable: the sasquatch release matrix (v3-capable extractor's published packages) and the AVM_LE marker ground that `PROVINCE.md:408` still lists Frontier. The v3/DDWRT material in the package turns out to be **already held**. |
| **depth** | the discriminating mechanism for the AVM_LE route: Freetz patch **550** hard-wires the marker, patch **613** only makes it optional — so the entry's headline "reachable" is true for a reason its own text gets backwards. Plus the exit-code rule (WARNING→0) that makes every "success" sentence on this surface need a file count. |
| **calibration** | one prior refusal (r36 D2) discharged on live bytes rather than waived; one deferral (r40) satisfied in substance with its unmet scheduling clause **quoted rather than ignored**; one entry refused for the third time with the surviving fact named so it can be salvaged. |

## Candidate review

Full text: `artifacts/R42Assim/verdicts.md`. Sources: `artifacts/R42Assim/sources-reopened.md`.

| entry | verdict | one-line reason | flip |
|---|---|---|---|
| `sasquatch-prebuilt-package-inventory` | **ADMIT**, re-grounded → `drafts/entry-A-sasquatch-release-matrix.md` | both r36 falsifications corrected on today's bytes; asset citation moved from the page to the API | refetch shows a ninth release / changed assets / a body stating a version pair |
| `avm-le-image-genuine-marker` | **ADMIT-AFTER-REWRITE** → `drafts/entry-B-avm-le-marker-le-squashfs.md` | r40's three corrections written against re-read bytes, plus two more (lane holds no image; "patched" reader mislabelled) | the retained image loses the marker, or the LE arm starts testing it |
| `avm-le-variant-reachability` | **REJECT** | headline falsified by two byte-identical retained images; third refusal with no reversal pointer | a rewrite to the surviving define-value fact with a reversal line |
| `sasquatch-unblob-compatibility` | **REJECT** | movable `unblob/main` cite; its own cited TSV contradicts "exercised"; content superseded by three held entries | re-grounding on S108 + S110 + lane receipts stating something not already held |

## PROVINCE scope check (`git show c4a38ea2:PROVINCE.md`)

| entry | in scope? | the line that decides it |
|---|---|---|
| sasquatch release matrix | **yes** | `PROVINCE.md:132` firmware/extract row; `:156-157` the `sasquatch` Frontier bullet the row refers to; `:122` records the round-36 install (official onekey-sec deb) as an allowed host change |
| AVM_LE marker | **yes, as Frontier ground** | `PROVINCE.md:408` — "Still Frontier: **LE AVM members (`hsqs`)** …"; the adjacent AVM-BE ground is Core since round 41 (`:400-408`) |
| `avm-le-variant-reachability` | in scope but wrong | same bullet; the entry's claim that the route is closed by an option build contradicts `:400` (marker = trigger, layout = LE block length) |
| `sasquatch-unblob-compatibility` | in scope but not needed | `:372`/`:382` already hold the handler/argv facts as Core rows; nothing here is a new surface |

Nothing in the four candidates touches malware triage, non-REA dynamic analysis, engine installs or
quality/safety verdicts — the Adjacent refusals are not engaged.

## QUALITY bar — the rows that actually bite

- **#1 resolvable source.** Candidate 1's asset facts are not on the page it cited (`grep -c` → 0) —
  that is the #1 failure and is repaired by citing the REST endpoint (new row S130). Candidate 4's
  evidence is campaign-local (`lanes/kaidoku/round8/work/lead3-sasquatch-compat.tsv`) **and**
  self-contradictory. Candidate 2's TSVs are campaign-local too, but their bytes are now imported
  with the draft (`artifacts/R42Assim/imported/`), which is the only way a host-local file meets #1.
- **#4 stable identity.** Candidate 1 pins the newest release's six `.deb`s by sha256 (API `digest`);
  the seven older releases expose **no** digest, so they are size-pinned only and the draft says so.
  Candidate 2's artifact identity is the image sha256 `18d3ad05…` (4096 B) — and the draft now states
  that the lane holds **no** copy, which the staged text asserted falsely.
- **#5/#7 labels.** The `is_avm` branch is labelled observed (source bytes); the claim that a BE
  carrier would behave the same is not made. The one place I infer is marked below.
- **#12/#18 producer bytes.** The image recipe is retained as patch text + scripts; the squashfs-tools
  4.3 tree itself is **not** retained (re-fetch by md5 `d92ab59a…`), so re-runs are recipe-level, not
  byte-level — stated in the draft.
- **#21 retention statement.** The staged "what the lane keeps is the 4096-byte image" is a retention
  claim with no recheck command and no held blob — false at the base (`git ls-tree -r c4a38ea2 --
  corpus/evidence | grep -i avm` finds only the **AVM-BE** image at `round-41/s126/`).

## Overlap with held entries (`corpus/README.md` `## Coverage map`, base)

| held entry | what it already says | consequence |
|---|---|---|
| `2026-10-26-unblob-sasquatch-dependency` | SquashFS support is a declared external dependency; Debian-package route exists; host-state correction | candidate 1's "AUR was never the only route" half is **not news** — draft re-titles to the matrix |
| `2026-10-26-unblob-format-matrix` | ten SquashFS sections incl. `v3`, `v3-Broadcom`, `v3-DDWRT`, `v3-non-standard` | **the package's only v3/DDWRT material is this entry, and it is held** (r38). R42-C1 can cite it; assimilation adds nothing |
| `2026-10-26-r36-sasquatch-squashfs-recursion` | LE v4 4/4, dependency gap before, symlinks unpublished | candidate 4's LE half is superseded |
| `2026-10-26-r38-…` / `2026-10-26-r39-be-squashfs-v4-core` | BE v4 measured / Core | candidate 4's BE half is superseded |
| `2026-10-26-r41-avm-be-squashfs-core` | AVM-BE Core, `-be` dropped when the marker holds | candidate 2's BE arm statement must point here, not at a denial |

Round-36/38 refusals I checked for reversal: `sasquatch-unblob-compatibility-precondition` (refused,
stands — host-absence premise), `sasquatch-unblob-avm-branch` (refused on the unpinned `unblob/main`;
still refused). Neither flips this wave.

## Evidence — commands actually run (exact; exit 0 unless stated)

```
date -u +%FT%TZ                                                  # 2026-10-26T21:51:26Z … 21:54:49Z
curl -s 'https://api.github.com/repos/onekey-sec/sasquatch/releases?per_page=100' -o rel.json
  → HTTP 200, 87700 B; 8 releases; asset counts [6,6,6,6,6,6,6,2]
curl -s -o sasq-releases.html https://github.com/onekey-sec/sasquatch/releases
  → HTTP 200, 349266 B; 8 tags in the page; grep -c 'sasquatch_1.0_amd64.deb' → 0
curl -fsSL 'https://api.github.com/repos/onekey-sec/sasquatch/releases' | grep -c 'sasquatch-v4.5.1-6' → 12
  (the staged entry's own recheck; reproduces)
curl … freetz-ng/86c23d96…/613-avm_format_as_option.patch → HTTP 200, 1601 B, sha256 9af3b3de…
curl … freetz-ng/master/…/613-avm_format_as_option.patch    → HTTP 404
curl … freetz/master/…/101-TARGET_FORMAT__AVM_BE_AVM_LE_symbols_only.patch → 200, 1153 B, e28b3341…
     `grep -c 'AVM_BE_AVM_LE'` on its body → 0;  `#define AVM_LE 2` / `#define AVM_BE 3` at body lines 7-8
curl … freetz/master/…/550-mkfs_time__AVM_BE_AVM_LE.patch → 200, 1080 B, 603c36c9…; cmp vs campaign copy → identical
curl … github.com/api/repos/Freetz-NG/freetz-ng/commits?path=…/613-…patch → 2 commits:
     86c23d96d765 2020-07-19 "squashfs4: enable timestamp at superblock"; 761e1923f9d4 2020-07-20 "Revert …"
curl … unblob/main/…/squashfs.py and …/26.6.4/…/squashfs.py → both 19842 B, both sha256 2d7b901b… (== installed)
curl … unblob/26.6.4/python/unblob/cli.py → 20221 B, fc775f1a… (== installed); `(Severity.WARNING, 0)` at :467
unsquashfs -s <three 4096-byte images>   → marker images: "Creation or last append time Wed Dec 31
     21:06:01 1969" + "Filesystem size 361 bytes"; the standard-time image: "Sat Oct 24 16:51:00 2026"
unsquashfs -lls <avm-le-genuine>         → 4 regular files; -d extract → 4 files, apple1.txt = "apple"
$HOME/.local/bin/sasquatch-v4be -be -no-exit-code -f -d <out> avm-le-genuine.squashfs
     → exit 1; "Reading a different endian SQUASHFS filesystem …" ; "FATAL ERROR: Block size too small.
       File system is corrupt."; 0 files written
sha256sum ~/.local/bin/sasquatch → ad02d27a3d8424b2f67ae88d479dba57334974527943e5f1e305423c4c774754
sha256sum avm-le-genuine.squashfs avm-le-plain550.squashfs → both 18d3ad0563cce852a438fe414d881909a6097fc30a38ca523372931cfcafaee4
git show c4a38ea2:corpus/SOURCES.md | grep -oE '^\| S[0-9]+ ' | wc -l → 129 (S001–S129)
     staged ids 132 (S106–S237); comm -12 → 24 collisions S106–S129; first free id S130
```

Only the `sasquatch-v4be` command above is a non-zero exit; it is the refusal the entry claims and
was run on a **lane-built 4096-byte development image**, not on any C1 candidate or anything carved
from one. No REA/unblob invocation of any kind this seat.

## Defects routed (for the L1 and for the round lesson)

| id | defect | standing |
|---|---|---|
| R42-AS1 | Staged `sasquatch-prebuilt-package-inventory:4` cites the rendered releases page for its asset list; the page bytes carry **no** asset filename (`grep -c` → 0). | repaired in draft A (S130 API row + S131 page row) |
| R42-AS2 | r36 D2 has stood for six rounds on a **true** observation read as a **false** universal: the arch matrix exists, it just starts at `sasquatch-v1.0.1`; `sasquatch-v1.0` is amd64-only. Likewise "the body shows 4.5.1 against 1.0" is simply not there, while "unsquashfs: fix prototypes for C23" **is**. | repaired in draft A; the refusal's flip is discharged |
| R42-AS3 | Staged `avm-le-image-genuine-marker:52-53` says the upstream commit "introduced" the patch: that commit was **reverted the next day** (`761e1923f9d4`, 2020-07-20) and the file is **404 on `master` today** — so the pin is load-bearing, not decorative. | stated in draft B; S134's anchor carries the 404 |
| R42-AS4 | The staged entry attributes the "mkfs_time == bytes_used" message to `upstream_unsquashfs_stat`; that wording is added by Freetz patch **550**'s unsquashfs hunk. Stock 4.7.5 prints the 1969 timestamp instead. | relabelled `patched_unsquashfs_stat` in draft B |
| R42-AS5 | Staged `avm-le-image-genuine-marker:59` "what the lane keeps is the 4096-byte image" — the lane holds no **AVM_LE** blob at the base: `git ls-tree -r -l c4a38ea2 -- corpus/evidence \| grep -i avm` returns only the **AVM-BE** image at `round-41/s126/` (4096 B), and the ~100 other `.sqsh` blobs are round-36/37/39/40/41 carriers. | imported with the draft; landing path proposed (`corpus/evidence/round-42/s132/`) |

Additional note for the round's own prose, not a package defect: **the package holds no SquashFS v3
extraction material.** Its only v3 text is `unblob-format-matrix`, already held (r38) and useful for
R42-C1 as a handler-name inventory (`v3`, `v3-Broadcom`, `v3-DDWRT`, `v3-non-standard`).

## Artifacts (all under `.ufo/waves/round-42/w1/artifacts/R42Assim/`, 50 files, 629542 B)

| path | what |
|---|---|
| `verdicts.md` | per-candidate verdicts with the prior decision quoted, defects, reason, flip |
| `sources-reopened.md` | every cited source re-opened today: access time, HTTP status, bytes, sha256, ≤25-word located quote |
| `drafts/entry-A-sasquatch-release-matrix.md` | admitted entry A, lane frontmatter, re-grounded |
| `drafts/entry-B-avm-le-marker-le-squashfs.md` | admitted entry B after rewrite, with the five corrections and the evidence-landing proposal |
| `drafts/sources-rows.md` | 7 proposed SOURCES rows in the 11-column schema (S130–S136; held S108 reused, not re-appended) |
| `id-collision.txt` | 24 staged/lane id collisions; first free id S130; the guard command |
| `imported/` | the three 4096-byte images, both own-work TSVs, `613.patch`, the 23-patch Freetz set, `build-avmle*.sh`, `build-avmle.log` — all lane-built or patch text, no third-party firmware |
| `receipts/` | `rel.json`, `sasq-releases.html`, `p613.patch`, `p550.patch`, `p101.patch`, `main-squashfs.py`, `2664-cli.py`, `handler-argv.txt`, `severity-exit.txt`, `unsquashfs-superblocks.txt`, `v4be-refusal.txt` |
| `sha256-manifest.txt` | sha256 of every file above |

## Limits and markers

- `[INFERENCE]` — that the option build produces a marker image **because** patch 550's unconditional
  write is present and patch 613 merely guards it: the patch bytes and the three images are observed;
  the causal sentence is my reading of them. The alternative reading (the plain build was really the
  option build) is excluded by `build-avmle2.sh`, which re-uses one tree and prints arm labels C/D/E,
  but that is a script label, not a fresh re-run.
- The squashfs-tools 4.3 tree is gone from the campaign directory, so **I did not re-run either
  build**; the images are the retained artifacts. Recipe-level reproducibility only.
- `patches/101-…` and `patches/550-…` were verified byte-identical to their upstream fetches **today**;
  `master` can move, so the imported bytes are the pin.
- Campaign TSVs are host-local own-work files: I read them, hashed them and imported their bytes;
  their readings are dated 2026-10-24 and I did not re-measure them except where noted (superblocks,
  BE refusal, file list).
- Not adjudicated: the other six staged squashfs/AVM entries (their r39/r40 decisions stand) and the
  `queued`/pointer tables in `MERGE-REPORT.md`.
- Scratch `/fast/scratch/hyaku/kaidoku-r42/R42Assim` (fetches, extraction, `.deb`-free) removed
  before yield; every quoted byte lives in `artifacts/R42Assim/`.
