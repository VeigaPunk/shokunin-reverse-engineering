# ScribeEntryC1 — round 50 attempt 2, wave 3 (build): the R50-C1 knowledge entry draft

**Verdict: the C1 entry draft is delivered and paste-ready (87 lines, six `<FILLED AT LANDING>` slots, every
claim labelled per QUALITY 5, a "not examined" section per QUALITY 7). Two landing defects in the L1's own
wave-1 landing scripts would turn four of the frozen counter's nine documentation bindings red unless they
are corrected first; one premise in my task text is factually wrong and is corrected in the draft.**

Seat: `ScribeEntryC1`. Lane HEAD at read time `6f4aba635fc47b5823ed42afe9c8b5dc3e28127f`
("round-50: attempt-2 claims corrected — entry stem pinned to the frozen counter constants").
Read-only seat: nothing in the lane tree was written, no REA run, no download, no git mutation.
Scratch `/fast/scratch/hyaku/kaidoku-r50/w3-ScribeEntryC1` removed at yield; receipts copied first.

## Findings

| # | finding | command (abridged) | exit | stdout sha256 | action for the L1 |
|---|---|---|---|---|---|
| F1 | **Entry stem: three different stems live in the tree; the frozen counter's wins.** `tools/round-50/c1-counter.py:377-378` pins `ENTRY`/`STEM` = `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`; `.ufo/waves/round-50/l1/land_c1.py:11-12` and `land_sources.py:11-12` still use the attempt-1 stem `2026-10-28-r50-le-avm-members-core`; the first draft of `plans/round-50-attempt2-claims.md` (and my task text) named `2026-10-29-r50-le-avm-hsqs-core`. The claims file was already corrected by commit `6f4aba63` before any data. With the stale stems the counter's `entry_present`, `province_core_row`, `frontier_note` and `coverage_map_row` bindings are all red. | `grep -n "^ENTRY = \|^STEM = " tools/round-50/c1-counter.py .ufo/waves/round-50/l1/land_c1.py .ufo/waves/round-50/l1/land_sources.py`; `git show 6f4aba63 -- plans/round-50-attempt2-claims.md` | 0 | `75c4a616777c3315b045ed91744283403390abf9a6a3507937bf7f9f8549cdea` (counter constants), `4a19c3a0ac222833d10ecc04803d55f646133379d3e5ede20fe5b8fabfe96768` (land_c1.py stem), `0cad4e4175880ab8457e56f0e739a4aca2bb14396e1bd5e0086a504bdb7c213c` (land_sources.py stem) | land the entry at the counter's stem; update `land_c1.py`/`land_sources.py` to the same string. Details and the nine bindings: `.ufo/waves/round-50/w3/ScribeEntryC1/stem-binding.md` |
| F2 | **`land_sources.py` deliberately drops the four C1 source rows.** The script builds S243/S244/S245/S249 with `used-by` = the stale stem and then filters them out: `S = {k: S[k] for k in ('S246', 'S247', 'S248')}` — comment "honest stop: C1 rows S243-S245/S249 are not landed (no entry cites them)". Now that the entry cites all four, that filter must go and the `used-by` cell must name the counter's stem, or the counter's `sourced` binding stays red (it requires the row's `opened` in `2026-10-28`/`2026-10-29` **and** `ENTRY`/`STEM` inside `used-by`). | `grep -n "S = {k: S\[k\] for k in" .ufo/waves/round-50/l1/land_sources.py` | 0 | `0cad4e4175880ab8457e56f0e739a4aca2bb14396e1bd5e0086a504bdb7c213c` | drop the filter; set `used-by` = `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`; keep the `used-by` cell free of backticks (the census rule the script itself applies) |
| F3 | **Correction to my task text: the cable images' big-endian ARM `sqsh` sibling is a separate tar member, not a second chunk.** `./var/remote/var/tmp/filesystem.image` (BE `sqsh`, `bytes_used` 5 442 392 / 5 981 012) is a different member of the image tar and is never fed to REA. The *second chunk with `unknown-chunk-handler`* that REA reports on an **uncarved** member is the 8-byte AVM trailer of the LE member itself (bytes `23de53c4` + 4, after the 4096-padded filesystem); the carve to `bytes_used` removes it, and on the carved carrier the chunk list is one `squashfs_v4_le` chunk with no such gap (the frozen gap rule allows `unknown-chunk-handler: 0`). The draft states both facts separately. | `cat .ufo/waves/round-50/l1/dev-arm-timeouts.txt`; `python3 -c "import json;print(json.load(open('tools/round-50/carriers.json'))['carriers'][2]['notes'])"`; wave-1 `w1/C1DevArmB.md` F3, `w1/C1RevLayout.md` F10/F15 | 0 | `e747627643b1ade85dccab68b3d0dd6d4e32acde6482566b8dcaa7e7e524e382` (timeouts receipt), `239d16236988ccfa5dd6b70e15f8f98445c8f4c89f0865b446c21b946be4f7bb` (carriers.json sha256 `0d7a6336fcebdbbf272134dda12519b1dd7554a01e8b60a6860f05dd4ec29ff3`) | none; the draft's wording is the corrected one |
| F4 | **The draft exists and is self-consistent**: 87 lines (< 220), 6 `<FILLED AT LANDING>` placeholders (`carriers_matched`, published regular files, gaps, `MaliciousSymlinkRemoved`, evidence ids), 20 labelled claim lines, `source:` lines only for S243/S244/S245/S249 (the four ids the attempt-2 claims pin), `verified-at: <REV>`, `recheck: on-refetch` naming the fetch-vendor chain command, the four-carrier pin table from `carriers.json`, the census (70 model directories, 28 LE `hsqs` marker rows in 16 models), the marker-is-a-constant-of-the-bytes clause, the carrier-swap history (7530/7590), the Still-Frontier list and limits 1-7 restated. | `wc -l`; `grep -c "FILLED AT LANDING"`; `grep -c "observation\]\|inference\]\|unknown\]"` on `.ufo/waves/round-50/w3/ScribeEntryC1/entry-draft.md` | 0 | draft file sha256 `3eff0a832ac7bae773b2c722ad71ee52479ffa34c375a1f7f241673d4792b018` (lane-side commands in `receipts.tsv`) | land it as `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` |
| F5 | **Oracle row counts (committed at the freeze) are the numbers the results table must reproduce**: regular files 4 556 (g7581), 4 564 (g7582), 4 709 (c6490), 3 955 (c6430); non-regular entries 1 001 / 1 001 / 914 / 824. These agree with the wave-1 measurements (MarkerCritic F11: "6490: 4710 files (4709 regular + 1 `.unknown`)" — the extra file appears only on the uncarved member). The counter asserts `files == oracle` per carrier, so the L1's four `published regular files` cells must equal these four numbers. | `for i in g7581 g7582 c6490 c6430; do awk 'NF' tools/round-50/oracle/$i.oracle.tsv \| wc -l; …` | 0 | `eefccac263221727f98991dfd58d88249f443e302d2e23783ec6b03115d02542` | use them as the cross-check when filling the placeholders; a mismatch is a real miss, not a typo |
| F6 | **The carrier-swap numbers in the draft come from the measured receipts, not from the plan's prose.** 7530: 13 366 regular files, 172 089 104 published bytes, 15 150 inodes; 7590: 13 358 files, 189 853 649 bytes; REA's fixed 120 s `provider_timeout` fired on 3 of 3 attempts each at host load 42.5-54 (`rea_attempts=3`, `duration_ms` 371 525 / 369 533, `exit=1`), while the same bytes ran in 29-63 s at a lower load. The plan's "~13.4k regular files (172/190 MB published)" is the rounded form of these. | `cat .ufo/waves/round-50/l1/dev-arm-timeouts.txt`; `w1/C1DevArmA.md` run table | 0 | `e747627643b1ade85dccab68b3d0dd6d4e32acde6482566b8dcaa7e7e524e382` | keep the Frontier wording "LE AVM rootfs of ~13k files under REA's 120 s limit" exactly as the claims text has it |
| F7 | **The marker clause needed one honest demotion that the plan text does not carry**: the marker is re-stampable (stock `mksquashfs -no-xattrs -mkfs-time <bytes_used>` passes every superblock clause) and unblob 26.6.4 reads it only in its BE branch, so it adds no evidence of origin beyond the carrier pin. The draft states this as the attempt-1 amendment, labels the "genuine = provenance, not marker" reading, and cites the Freetz patch 101 row as the reason no registry text describes an LE AVM layout. | `grep -n "is_avm" tools/round-50/../round-50/c1-counter.py` (docstring), `w1/C1MarkerCritic.md` F1-F3b, `w1/C1RevLayout.md` F9 | 0 | `75c4a616777c3315b045ed91744283403390abf9a6a3507937bf7f9f8549cdea` | none; this is the clause the w4 falsify wave should attack first |
| F8 | **One corroborating source is not in the registry and is therefore cited as prose only**: the Freetz wiki page `https://www.freetz.mhampicke.de/trunk/make/squashfs4-le/Config.in` ("The only difference of this format to the original LE format is that the value of the mkfs_time superblock field is equal to the bytes_used field", read 2026-10-28 by `w1/C1MarkerCritic.md` F6). The four pinned ids are S243 (patch 101), S244 (index), S245 (unblob LE), S249 (licence); adding a fifth row would touch the registry beyond the claim's pin and would need the round's id allocation. | `grep -n "freetz.mhampicke.de" .ufo/waves/round-50/w1/C1MarkerCritic.md` | 0 | `090176fc4fa3aec10a07f9d0f66de38fcf1ba74cf13fd564ce89f3999f25ecca` (seat report sha256) | either register it as a new row (then move it into a `source:` line) or leave it as prose; the draft currently leaves it as prose and says so |
| F9 | **Frozen bytes verified unchanged** between the freeze `435d41fd…` and the attempt-1 tip `8ccc05e6…` for `tools/round-50/`, `plans/round-50-claims.md`, `tools/round-41/sqfs-list.py`, `tools/round-27/xpin-attribute.mjs` (empty diff, exit 0), so the counter, carriers, oracle and gap tables the draft cites are the scoring bytes. | `git diff --stat 435d41fd… 8ccc05e6… -- tools/round-50/ plans/round-50-claims.md tools/round-41/sqfs-list.py tools/round-27/xpin-attribute.mjs` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (sha256 of empty stdout) | none; the L1 re-runs this before the data run |
| F10 | **The sibling registry patch applies cleanly to the live registry** (checked by this seat, read-only): `corpus/SOURCES.md` at HEAD is byte-identical to the rows seat's base copy (both sha256 `2204e6a6475177616caa92446c68ec35c3e6cdcd8f5194e945b7b201d8f189c4`; `diff` exit 0), and it already carries the attempt-1 C2 rows S246-S248 at lines 156-158, so no rebase and no duplicate rows. The patched file adds exactly S243, S244, S245, S249 (rows 152 → 156, 0 removed) plus one search-log bullet; each of the four rows has 11 cells, `status mined`, `opened 2026-10-28`, and `used-by` = the plain path `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (no backticks), with the pipe count per row matching the lane's 12-pipe convention. | `sha256sum corpus/SOURCES.md`; `diff .ufo/waves/round-50/w3/ScribeRowsSources/artifacts/SOURCES.base.md corpus/SOURCES.md`; python row/column parse of `SOURCES.patched.md` | 0 / 0 / 0 | base+patched sha256 as in the rows seat's report; `2204e6a6…` for both the live file and the base copy | the L1 can apply the patched registry as-is (entry + rows in one commit) |


- `ScribeRowsSources` (the four SOURCES rows) independently reached the same two blocking findings
  (F1 stem, F2 the `land_sources.py:130` filter) and shipped a ready-to-apply registry patch computed
  against the counter's stem: `.ufo/waves/round-50/w3/ScribeRowsSources/artifacts/SOURCES.patched.md`
  (sha256 `a8fc2772aafc10269497ef66a19ddfce0983e227f0499053b0f64989af7daabc`; base
  `2204e6a6475177616caa92446c68ec35c3e6cdcd8f5194e945b7b201d8f189c4`; +4 rows +1 search-log bullet,
  0 changed, 0 removed). Its `used-by` cells carry the plain path
  `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (no backticks), `opened 2026-10-28`.
- `ScribeReadmeMap` (the `corpus/README.md` rows) is on the same stem; `verified-at:` in my draft is the
  placeholder `<REV>` (the attempt-2 data commit), not a literal date, so the Knowledge index row should
  use the data commit's `%cI` for the same value.
- Verification I ran for the rows seat: applying the counter's own tokenizer (`SID_RE`,
  `tools/round-50/c1-counter.py:430`; `sid_tokens` :589) to this seat's draft yields
  `src_ids = {S243, S244, S245, S249}` and those four are the only S-ids anywhere in the file, so the
  `sourced` binding (c1-counter.py:2468-2476) needs exactly those four rows and no stray id.
- The complete C1 landing therefore is: the two L1 scripts patched to
  `STEM = '2026-10-28-r50-avm-le-squashfs-core'` (and the `land_sources.py:130` filter dropped), then
  the entry draft and the four registry rows landed in **one** commit (the rows seat measured the
  registry census exiting 1 with exactly four E11 lines when the entry path is absent).
- One point of calibration agreed with the rows seat: the uncatalogued Freetz wiki page that describes
  an LE AVM layout stays prose in my draft, with an explicit "the lane holds no `corpus/SOURCES.md` row
  for it" note; it is not minted as S250 and not moved onto a `source:` line, because admitting it as
  `mined` would make the registry assert an LE AVM layout that R50-C1 deliberately does not claim. That
  page was not fetched in this wave — the draft attributes it to the wave-1 seat that read it
  (`w1/C1MarkerCritic.md` F6, 2026-10-28), and this seat makes no claim about its bytes.

## Addendum — the landing outcome (added after the L1's landing and the falsify wave)

Round 50 has since landed, so this seat's draft was integrated and then corrected by the falsify wave;
the addendum records the measured outcome for the audit trail (read-only, no claim of authorship of the
landed text).

- [observation] The entry landed at `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`
  (sha256 `3b5f3119390361fc7a154022575b0716972c1fd7d8ca481f55abb16890f15b0d`), i.e. at the stem this
  seat's F1 pointed at.
- [observation] The frozen counter at the landing scored **`carriers_matched 2` of `target 4`,
  `met_target` false, `failing` = `g7581:gaps_ok`, `g7581:projection_ok`, `g7582:gaps_ok`,
  `frozen_path_changed []`** (receipt `.ufo/waves/round-50/l1/scores/c1-after-attempt2.json`, sha256
  `e1e0ac176a9ccd71876bfe3ce2032eb94067c29c86922ee56d7db211b7c62816`): the extraction half held on all
  four carriers (published regular files == the frozen oracle counts 4 556 / 4 564 / 4 709 / 3 955), and
  the frozen gap rule failed on the two FRITZ!Box carriers, whose oracle tables carry 13 `char-device`
  entries each against the one (`247:0`, `dev/led`) the rule admits silently.
- [observation] **The documentation bindings this seat's draft controls are all true**: `entry_present`
  true, `sourced` true with `entry_source_ids` = `['S243','S244','S245','S249']` and
  `opened_source_rows` = the same four, `coverage_map_row` true, `frontier_note` true,
  `carriers_spec_ok` true, `gap_rule_ok` true, `frozen_tables_valid` true. The two false ones
  (`province_core_section`, `province_core_row`) are false because nothing was promoted to Core — the
  correct outcome for a miss.
- [observation] The falsify wave then amended this draft's text in the landed entry, among other things:
  the marker clause is now scoped to the round-50 experiment actually run (a 4-byte `mkfs_time` patch on
  standard-LE fixtures; no stock `mksquashfs` invocation), the census is stated as a re-count of
  retained listing metadata rather than a superblock re-read, and the S244 listing bodies are cited at
  their real committed path (`.ufo/waves/round-50/w3/ScribeLessonGate/receipts/`, not the never-committed
  `corpus/evidence/round-50/c1/index/`). Those corrections are the falsify wave's, not this seat's, and
  this seat's draft text remains in its seat directory as the pre-landing version.

## Deliverables (all under this seat's directory)

| path | what |
|---|---|
| `.ufo/waves/round-50/w3/ScribeEntryC1/entry-draft.md` | the entry draft, paste-ready as `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md` (sha256 `3eff0a832ac7bae773b2c722ad71ee52479ffa34c375a1f7f241673d4792b018`) |
| `.ufo/waves/round-50/w3/ScribeEntryC1/stem-binding.md` | which stem is authoritative, the nine counter bindings it drives, and the two stale L1 landing scripts (sha256 `1a50c8a52a685daab1ca76011b260fa3e44072f5f7b6d8151efdc6e431736185`) |
| `.ufo/waves/round-50/w3/ScribeEntryC1/carriers-pins.tsv` | the four carrier chains, machine-readable, derived from `tools/round-50/carriers.json` (sha256 `c1792fa0c5392760f45374de0e761a813bb3088af61f81a1a3e0022fad2d9433`) |
| `.ufo/waves/round-50/w3/ScribeEntryC1/receipts.tsv` | every command run by this seat: UTC instant, exit code, stdout sha256, description, argv (sha256 `2dffc153608d4faa7673d9bbf9b7f63f2da0c7e775849577bb0d6941d6ede227`) |

## Not run / out of scope

- No REA run of any kind (this wave is build-only; the L1 runs the REA-dependent controls and the data
  run). No `npx rea-agents`, no `rea-agents` package invocation, no counter run, no `--data-run`.
- No vendor image or member downloaded; no fetch, no carrier cache, no scratch copy of vendor bytes.
- No lane write outside this seat's directory; no commit, push, stage, stash or any other mutating
  git/jj command; no fixture repo was created; the lane's `tools/`, `plans/`, `corpus/`, `SKILL.md`,
  `PROVINCE.md`, `LOG.md`, `SCORECARD.md`, `SHONEN.md` and the fleet repo are untouched.
- Not examined (QUALITY 7, also in the draft): the other 12 census models' LE members; LE AVM bodies
  with compression other than xz; xattr-bearing LE bodies; AVM kernel images; nested sub-images below
  depth 1; the cable images' BE ARM member; the census's 20 zero-length and 4 version-0.0 rows; the
  content of the 8-byte AVM trailer; the git history of the Freetz `AVM_LE` build branch.
- Tools installed or upgraded: **none**. No `pacman`, no `uv tool`, no `~/.local/bin` change
  (the operator's tooling directive was not needed for a read-and-draft seat).

## Tooling note

`/home/vgpnk/Projects/shokunin/scripts/hyaku/disk-guard.sh status` exit 0 at
`2026-10-29T20:35:31Z` (stdout sha256 `ef1d6b4798b1ca7e7771ad19890cae2ba31ad0cbaf0f8eeb288ad5d84b043f46`);
the pass was light (hashes and greps only), so no further disk action was taken.
