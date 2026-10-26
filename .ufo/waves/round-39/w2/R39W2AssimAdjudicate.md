# R39W2AssimAdjudicate — AVM assimilation adjudication for round 40

**Verdict: DEFECTS FOUND** in both wave-1 seats' framing, and the round's deferral is resolvable
without new research: after re-grounding, **exactly one staged entry is admissible for round 40 —
`avm-firmware-image-unblob` (E4), rewritten**, because it is the only candidate whose evidence is a
real AVM image (the deferral's own flip condition) and every measurement in it reproduces byte-exactly
on a re-fetched, digest-pinned vendor image; `avm-image-extraction` (E3) is admissible on additions
alone but is **not** this round's admit; the other four stay refused.

Seat: critic/adjudicator (leaf). Wrote only this file and
`.ufo/waves/round-39/w2/artifacts/R39W2AssimAdjudicate/`. Scratch
`/fast/scratch/hyaku/kaidoku-r39/R39W2AssimAdjudicate` removed at exit. No tool installed or
upgraded; no pacman transaction; `sasquatch`, `sasquatch-v4be`, `unblob` untouched. `shokuknow` read
only (four 4096-byte lane images hashed in place and copied to scratch). Read-only git only, no VCS
mutation. No subagents, no background jobs.

Everything below is observed on this host this wave unless marked `[INFERENCE]`. Artifact paths are
relative to `.ufo/waves/round-39/w2/artifacts/R39W2AssimAdjudicate/` (abbrev `$ART`).

## Axes (Godspeed)

| axis | what this adjudication moves |
|---|---|
| **coverage** | which staged AVM entry may occupy the lane's Frontier note for AVM-BE, and with which source rows |
| **depth** | the statement the corpus should hold: *handler selection is marker-free; v4-BE extractor argv is marker-conditional; the marker is AVM's own format tag, and the only independent layout test is the metadata block-length endianness* |
| **calibration** | which of the two seats' corrections are defects of the entry and which are corrections of claims the entry never makes |

## 1. The pinned handler, re-read

Installed uv-tool copy, `sha256 2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`
(= lane row **S112**'s recorded blob at tag 26.6.4 = commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`;
also S108's scope row). `$ART/handler-lines-40-53.txt`:

```
40            case Endian.BIG, 4:
...
48                    is_avm = header.bytes_used == header.mkfs_time
49                    if not is_avm:
50                        commands_args.append("-be")
51            case Endian.BIG, _:
52                commands_args.append("-be")
53            case Endian.LITTLE, _:
```

Three arms, three different facts, and the whole w1 dispute turns on not collapsing them:

| arm | what the marker decides |
|---|---|
| **handler selection** (`SquashFSv4BEHandler` vs `SquashFSv4LEHandler`) | **nothing** — magic + endianness only |
| **(BIG, 4) extractor argv** | **everything** — `-be` appended **iff** `mkfs_time != bytes_used` |
| **(BIG, ≠4)** and **(LITTLE, any)** argv | **nothing** — unconditional |

So the entry's sentence is neither wholly true nor wholly false: its *selection* clause is confirmed by
the same lines that falsify its *invisibility* headline.

## 2. Sentence-by-sentence re-check of the disputed entry

| disputed text (staged `avm-firmware-image-unblob`) | verdict | evidence |
|---|---|---|
| `:16` "it never notices the AVM marker at all" | **FALSE** | lines 48-50; and the entry's *own* table at `:67` prints the BE argv without `-be` |
| `:75` "The AVM marker is **invisible to unblob**" | **FALSE for v4-BE**, **TRUE for v4-LE** | lines 48-50 vs line 53; measured: genuine AVM-LE → `sasquatch -le`, 4 files |
| `:75` "it selects a handler on the magic and the endianness, never on the marker" | **TRUE** | handler class by magic; endianness by `get_endian(file, self.big_endian_magic)` at the top of `extract` (lines 32-35); no marker test outside the (BIG,4) arm |
| `:75-77` "an AVM_LE image and a plain LE image of the same size and compression take the same path" | **TRUE** | LE arm is unconditional; r38/vendor LE runs both show `sasquatch -le` |
| `:77` "That is the opposite of round 12's expectation, which was that unblob would need a dedicated AVM branch" | **FALSE for BE** (`:77` "why round 13's synthetic image and this round's production image behave identically") | the branch exists — it is *why* the vendor BE argv lacks `-be`; the synthetic and production BE images behave **identically only because both carry the marker and both are AVM layout** |
| `:69` "9 877 files in all" | **TRUE as a whole-image total, misleading as the table's sum** | measured 6 912 + 2 942 = 9 854 ≠ 9 877; the 23-file remainder is outside both filesystem trees |
| `:56-59` "A 1970 date is the visible fingerprint of the AVM marker … the AVM marker shows up as a filesystem dated in 1970" | **TRUE** (correctly scoped to the *marker*) | r38 probe renders `created: Thu Jan 1 02:43:00 1970` on a marker-bearing **standard-BE** body; vendor members render 1970 |
| the "different endianess" stderr line | **not a claim of this entry** | the string appears nowhere in the entry; it lives only in the r38 probe artifacts and in `sasquatch-unblob-avm-branch.md` |

**Where each seat errs.**

- The critic's headline finding is sound but **overbroad**: "the shared mechanism sentence is
  falsified" is right only for the *invisibility* clause. Its selection clause is confirmed by the
  very lines cited, and the LE half is confirmed by measurement. Consequently the critic's conclusion
  ("only E3 survives") is not entailed by the handler — it is an editorial call, and the critic says so
  itself two paragraphs later ("Both paths land on the same corrected statement").
- The scout's **c2** (1970 date) and **c3** (stderr line) correct claims the entry never makes. The
  entry scopes the date to "the AVM marker" — exactly what the doctored probe demonstrates — so c2 is
  an *addition* ("the date identifies the field, not the layout"), not a correction; and c3 has no
  target in the entry at all (it is a design warning for the C2 table, and the landed table already
  does not key on stderr). Over-correction is itself a defect in an adjudication: it dilutes the one
  real reversal.
- The scout's **c1** is correct but **insufficient**: the entry needs row replacement (QUALITY #1) and
  a pin (QUALITY #8), not only a re-worded sentence.

## 3. Independent re-measurement (this wave)

**Vendor image** (`$ART/vendor-image.tsv`; `curl` at 17:35Z):
`39 741 440 B`, `sha256 f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d` — equal to
the campaign row's digest. Index page re-opened (`$ART/fetch-download.avm.de_…`, HTTP 200, 592 B,
`063ec39a…f6d8f7bc`), listing row 5: `FRITZ.Box_6490_Cable-07.57.image … 39741440`.

| member | bytes | superblock |
|---|---|---|
| `x86/filesystem.image` | 28 200 968 | `hsqs`, mkfs 28 200 029 == bytes_used 28 200 029 (marker **true**), comp 4, slack 939 |
| `filesystem.image` | 5 443 592 | `sqsh`, mkfs 5 442 392 == bytes_used 5 442 392 (marker **true**), comp 4, slack 1200 |
| `x86/kernel.image` | 3 552 264 | starts `81 12 ed fe` |
| `kernel.image` | 1 932 808 | starts `81 12 ed fe` |

**unblob 26.6.4 on the vendor image** (`$ART/unblob-vendor-squashfs-lines.log`,
`$ART/unblob-vendor-argv.txt`), exit 0:

```
Found valid chunk  chunk=0x0-0x1ae5000 handler=squashfs_v4_le
Found valid chunk  chunk=0x0-0x531000  handler=squashfs_v4_be
Running extract command  command='sasquatch-v4be -no-exit-code -f -d …0-5443584.squashfs_v4_be_extract …'
Running extract command  command='sasquatch   -le -no-exit-code -f -d …0-28200960.squashfs_v4_le_extract …'
```

Counts: total files **9 877**, symlinks **878**; LE dir **6 912** files / 615 links / **53** nested
extract dirs (own regular files **4 721**); BE dir **2 942** / 263 / **52** (own **711**).
Reconciliation: `9 877 = 6 912 + 2 942 + 23` files outside the two filesystem trees.

**Marker vs layout, four 4096-byte fixtures** (`$ART/marker-vs-layout-matrix.tsv`,
`$ART/carrier-fields.tsv`; unblob exit 0 in all four — it reports failure in the log and still exits 0):

| image | mkfs==bytes_used | metadata-length endianness | unblob argv | files |
|---|---|---|---|---|
| genuine AVM-BE (`c7f74691…`, round 11) | yes | **LE** (hdr `7400`: 116 vs 29 696) | no `-be` | **4** |
| same bytes, `mkfs_time := 0` (`c7eed042…`) | no | **LE** | **`-be`** | **0** |
| marker-only/doctored standard-BE (`7e86a1d1…`, round 9) | yes | **BE** (hdr `003a`: 14 848 vs 58) | no `-be` | **0** |
| genuine AVM-LE (`18d3ad05…`, round 13) | yes | LE | `-le` | 4 |

**REA control on the genuine AVM-BE** (`$ART/rea-avm-be-control.txt`; command per the wave rule,
`REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob npx -y rea-agents@6.5.0 extract-firmware --format json
--full-output`): `evidence_id ev_8a2c59ce…6379`, `ok true`, `coverage complete`,
`diagnostics []`, `unpublished []`, chunks `['squashfs_v4_be']`, 4 published files. **A genuine
AVM-layout image leaves no gap and no child-extractor `command` in `normalized_result`** — it is
envelope-identical to a clean standard-BE extraction.
`$ART/triage-control.txt` (`tools/round-39/sqfs-triage.py --skill SKILL.md`, exit 0):
genuine AVM-BE → `clean`; `H13` → `avm-marker-be-dropped`; `H15` → `body-extractor-failure`;
`K1` → `escaping-symlink-removed`.

**Round-39's own carriers** (`$ART/carrier-fields.tsv`): K1-K6 are all marker-**false** with
block-length endianness **BE** — the C1 claim "standard big-endian" is accurate and no C1 carrier
carries the marker (the critic's feed-forward item 1 is already satisfied). `H13`/`H14`
(`avm-marker-be-dropped`) are marker-**true** with block-length endianness **BE**, i.e. a doctored
marker on a standard body: the generator cannot write an AVM layout, so that class can only ever be
the forged direction.

## 4. Adjudication per entry

| entry | verdict for round 40 | why |
|---|---|---|
| **`avm-firmware-image-unblob`** (S216-S217-S218-S219-S220-S223) | **ADMISSIBLE — as a rewrite (c1-c7 below); this is the round-40 admit** | Only candidate built on a real AVM image = the round-39 deferral's own flip condition ("re-grounded on lane receipts against a real AVM image"). Every measurement reproduces byte-exactly on a re-fetched digest-pinned image (vendor sha, four members, both markers, both argvs, 6 912/2 942/9 877, slack 939/1200, kernel magic). The false element is confined to two sentences whose correct form the lane **already holds three times** (round-38 entry `:26-27`; `PROVINCE.md` round-39 Core row "(AVM marker excepted)"; `SKILL.md:339`), so the edit restores agreement instead of creating a fourth authority. Flip to refuse: vendor digest moves, or c1/c2 is reverted. |
| `avm-image-extraction` (S200-S201) | **admissible on additions alone — NOT this round's admit (second choice)** | Its claims survive; it already states the marker-conditional argv correctly ("**no `-be`**, exactly as its source says for the AVM case"). But it carries no vendor bytes, its carrier is a 4 096-byte synthetic image and its two rows are campaign-local; admitting it would not meet the deferral's flip condition. It also does not need a rebuild — QUALITY #12 is satisfied by retaining the 4 096 bytes (`c7f74691…`) plus the recipe. Flip: if the vendor image stops serving at its digest, admit E3 after that retention. |
| `sasquatch-unblob-avm-branch` (S189-S192) | **REFUSE** (stays) | Mechanism confirmed at 26.6.4, but its closing premise ("a real AVM image still needs a tool this host does not have") is falsified twice over — round 11 built one, round 14 downloaded one — and S189 is the unpinned `unblob/main` branch (QUALITY #8). Its content folds into the corrected E4 plus lane S112/S114. |
| `avm-image-build-blocker` (S197-S198-S199) | **REFUSE** (stays; convert to a reversal record) | Premise "the 4.3 tarball is not served from any reachable mirror" is false (SourceForge path HTTP 200, md5 `d92ab59a…` = Freetz's pin — the scout re-verified); and its supporting number `bytes_used 7 854 559 225 110 855 680` inside a 4 096-byte image (0x6D01000000000000) is a misparse presented as a measurement. QUALITY #35/#36 require it to become a reversal record, not a standing "gone" claim. |
| `avm-le-variant-reachability` (S206-S207) | **REFUSE** (stays; reversal record) | Headline "not reachable" is overturned by `avm-le-image-genuine-marker.md`; its surviving value (`AVM_LE`=2, `AVM_BE`=3; a patch *filename* is not a define) belongs in the admitted entry's citations of S206, not in a standing entry. |
| `avm-le-image-genuine-marker` (S212-S213-S214) | **REFUSE for round 40** | Its LE-scoped sentences are true (LE arm is marker-blind: line 53 + measured 4/4), but it carries no round-39/40 surface — the Core row is `squashfs_v4_be`, and the BE half is the falsified one. It is the entry E4 should be narrowed *toward*, not a second admit; its rows S212/S213 are campaign-local. |

## 5. Exact corrections for the admitted entry (E4)

Smallest safe edits; each one closes a specific falsified or ungrounded sentence.

- **c1 (headline, `:2-3` and `:16`).** Delete "— it never notices the AVM marker at all". Replace with:
  *"no handler is AVM-specific: both filesystems reach unblob's ordinary little-endian and big-endian
  v4 handlers; the BE handler does read the marker, but only to choose the extractor's argument list."*
- **c2 (`:75-77`, the mechanism paragraph).** Replace the paragraph with the three-arm statement:
  handler selection = magic + endianness only (no marker); **v4-BE extractor argv = marker-conditional**
  (`-be` iff `mkfs_time != bytes_used`, `squashfs.py:48-50`); **v4-LE argv = marker-blind** (`-le`
  unconditional, `:53`). Keep "no dedicated AVM handler is needed" — delete "That is the opposite of
  round 12's expectation" and the claim that the two production images behave identically *because* the
  marker is ignored; they behave identically because both carry the marker **and** are AVM layout.
- **c3 (the limit that makes the entry worth keeping).** Add: the marker is AVM's own format tag
  (S114 lines 13-14; the only LE field in AVM-BE is the block-length value, S114 lines 8-9), so it is
  authoritative for AVM-built images; it is only a *heuristic* for arbitrary bytes. Measured both
  failure directions on 4 096-byte fixtures: a doctored marker on a standard-BE body loses `-be`
  (0 files) and a genuine AVM-BE with a normalised timestamp gains `-be` (0 files), while the genuine
  AVM-BE with its marker extracts 4 files — and through REA reaches `coverage complete`,
  `diagnostics []`, i.e. **a working AVM-BE produces no gap at all**.
- **c4 (counts).** State 6 912 / 2 942 as *recursive published-file counts including unblob's nested
  extractions* (53 and 52 nested containers; own regular files 4 721 / 711; symlinks 615 / 263), and
  keep "9 877 in all" only as the whole-image total with the remainder named
  (`= 6 912 + 2 942 + 23`).
- **c5 (timestamps).** Quote the integers 28 200 029 and 5 442 392; the 1970 renderings are host-local
  (this host is UTC−03: 06:20:29 / 20:46:32 local = 09:20:29 / 23:46:32 UTC). The cheap test survives,
  re-scoped: *the marker shows up as a filesystem dated in 1970* identifies the **field**, not the
  layout.
- **c6 (provenance and pins).** Replace the campaign-local rows; pin the Freetz-NG document by commit
  or raw digest (master is a floating ref); label the S223 NMI/TI paragraph as one image, one product.
- **c7 (unlabelled inference in the table, `:67`).** The row reads `MIPS (AVM_BE)`; the measured tar
  member is `./var/remote/var/tmp/filesystem.image` and there is no MIPS directory (this wave's
  extraction: `x86/filesystem.image` and `filesystem.image`). `MIPS` is an inference from the campaign
  row naming (`mips_filesystem_*`, S218) and it contradicts the entry's own caveat that "which silicon
  actually boots these kernels is not established here" — label it inference or drop it (QUALITY #5).

Not corrections: the 1970-date sentence as written (true, correctly scoped); the stderr line (not in
the entry); "S192/S189 repin" (those are E1's rows; E4's handler row is **S112**, already pinned).

## 6. Staged source rows the admitted entry needs

Staged ids are renumbered by document; the lane registry holds S001-S122, so the **next free id is
S123**. Re-verified this wave (`$ART/fetch-*`):

| staged | document | lane action |
|---|---|---|
| S216 | `download.avm.de/…/fritz.os/` index page | **new row** — HTTP 200, 592 B, sha256 `063ec39af00bd45e668519cc2ce95debf41cf5d56ed9dcde37223b57f6d8f7bc`, listing row 5 |
| S217 | `…/info_en.txt` | **new row** — HTTP 200, 67 591 B, sha256 `6c601b342da91f7598dde1e7842ba92a61a1ec7f4b3d00564573fea3d11070a7`; `Product:`/`Version:`/`Release date:` lines |
| S220 | Freetz-NG `docs/make/README.md` line 674 | **new row, pinned** (master raw sha256 `8d1cae2fc1d9af038711fc130d26e525c5f24fbf9fb15250f4ea6b548ad862d6` today, or a commit sha); note the sentence describes **AVM-LE** |
| — | the vendor image itself | **new own-work row** — `FRITZ.Box_6490_Cable-07.57.image`, 39 741 440 B, sha256 `f518ce6baa05b30d84264d9349cca9bf0b9402986d4112bda8ad73a04f9ede6d`, URL + retrieval date (this is the QUALITY #4 identity the entry lacks) |
| S218 / S219 / S223 | campaign `lanes/kaidoku/round14/work/*.tsv` | **do not append.** Round-40 own-work rows must point at lane-retained receipts (superblock table, unblob argv/counts, triage control envelope `ev_8a2c59ce…`), measured from the digest-pinned image — a 6-second re-run on this host, so cost is not a ground for deferral |
| S192 / S189 | Freetz `AVM-BE-format.txt` / unblob handler | **no new row** — lane **S114** and **S112** already hold these documents at the needed scope (S114 may need its scope cell extended to the block-length bullet, lines 8-9) |

## 7. Landed round-39 artifacts: two precision items (not freeze violations)

1. `SKILL.md:339` (`avm-marker-be-dropped`) is **correct** on the mechanism and on the argv feature, but
   its cause clause — "so sasquatch-v4be read a standard-BE body with the wrong byte order" — states as
   fact what the marker alone cannot establish. Measured: a genuine AVM-BE also reaches this feature set
   when it fails for any other reason, and the class's held-out carriers (`H13`/`H14`) are all forged
   markers on standard-BE bodies. Smallest safe correction (round 40, as a wording tightening, not a
   predicate change): cause → *"the extractor used the AVM block-length layout on a body that does not
   match it (the metadata block-length endianness is the independent test)"*.
2. The counter has no **genuine-AVM-layout** class, so the label it can never be forced to produce is
   the one above. The control is cheap and already measured: `$ART/rea-avm-be-control.txt` (genuine
   AVM-BE → `clean`, `coverage complete`, `diagnostics []`). Adding it as a negative control in round 40
   costs one 4 096-byte carrier and one REA run.

## 8. Limits

- E4's other claims were checked against the vendor bytes only where cheap: the `bin/aicmd` ELF and
  `bin/ar7cfgchanged` shell-script examples were not re-typed; the "939 / 1 200 trailing slack" and
  "no TI checksum" claims are arithmetic from measured sizes (slack confirmed) — the TI-checksum
  absence was not re-derived here.
- The S223 NMI/TI paragraph was not re-measured; it is labelled one-image, campaign-local.
- The vendor BE member's metadata block-length endianness cannot be decided by the 2-byte plausibility
  test (its inode table spans several blocks); for the BE member that field is `[INFERENCE]` from the
  fixture measurements plus S114 lines 8-9.
- The AVM-LE half of the entry ("an AVM_LE image and a plain LE image take the same path") was checked
  on a genuine AVM-LE fixture (4/4) and against line 53; no vendor LE marker-blindness run was made
  beyond the vendor LE extraction itself.
- No REA run on the vendor image (only `unblob` directly); no REA run on K1-K6 or the held-out carriers
  this wave.

## 9. Housekeeping

- Tools: none installed or upgraded (RULES.md read; pacman paused; nothing needed). Versions used:
  `unblob 26.6.4`, `sasquatch-v4be` (unsquashfs 4.5.1), `python3` 3.14.8 (system), REA `6.5.0` via
  `npx -y rea-agents@6.5.0`.
- Retained: `handler-lines-40-53.txt`, `vendor-image.tsv`, `unblob-vendor-squashfs-lines.log`,
  `unblob-vendor-argv.txt`, `marker-vs-layout-matrix.tsv`, `carrier-fields.tsv`,
  `rea-avm-be-control.txt`, `triage-control.txt`, `fetch-*` (index page, `info_en.txt`, Freetz-NG
  README), `S114-AVM-BE-format.txt`. The 39.7 MB image and the extraction tree were scratch-local and
  are deleted with the scratch.
- Not done: no `git`, `jj`, or VCS operation of any kind; `shokuknow` untouched (hashes and copies out
  only); nothing written outside `$ART` and this report.
