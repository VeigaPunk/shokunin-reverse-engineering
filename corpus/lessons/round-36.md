# Round 36 — fresh start: sasquatch recursion to Core, self-assessment drift repaired, counter blind spots named

Base `cab59f221fe19726b5692bfa4d9a9679e96b8a73`. Freeze `790561d4e3aca732a434081aa9573ec2fa5fd7d0`
(`plans/round-36-claims.md`, counters, selftests, carriers, oracle, before receipts); control receipts
`6a870b9290e9566468d7d9e6d1b8308daf025b12` (C1 ×3, C2 ×4, all exit 1); C1 after receipts
`3310d8fa27bfaa95ad858c4aaad6f6377f853982`; C2 landing `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`;
C1 + assimilation landing `ffc813417d3bceeeb7b028b12ce0be8a5dc33d95`. Fresh-start round after three
rejected closures (r33 unprovable, r34 and r35 honest stops); both claims were scored against
do-nothing and skip controls with the frozen counters before any claimed data existed.

## Mistakes

| id | class | evidence | captured-by | fix |
|---|---|---|---|---|
| M36-1 | stale packaging-route premise carried as prose for 32 rounds | `PROVINCE.md:149-150` "(AUR-only)" and `corpus/README.md` Frontier "sasquatch (AUR)" entered in round-4 commit `999ce123` and were byte-identical at base (`git log -S'AUR-only' -- PROVINCE.md` → that one commit). unblob's own README documents the Debian-package route (S110, line 49) and onekey-sec has shipped `.deb` assets since 2022-02-26 (wave-1 `R36ScoutPrebuiltInventory.md`) | none: no rule asked a Frontier route statement for a source; freshness sweeps read knowledge entries, not PROVINCE prose | Frontier notes added this round cite S110 by entry (`PROVINCE.md` round-36 Frontier note, README Frontier note). Shown able to fail only for the cited entry: `sources-census.sh validate` reports E11 if S110's used-by entry is absent (the scratch mirror without cited files failed E11 on S036/S081, `.ufo/waves/round-36/assimilation/validate-mirror.txt` history in this lesson's Gate). The general rule (route statements need a source) is not yet executable — open |
| M36-2 | present-tense scorecard count measured at a pinned revision and left behind | `SCORECARD.md:23` at base said `116/116 knowledge files mapped`; observed 122/122 | none before this round | R36-C2 counter O1. Shown able to fail: `.ufo/waves/round-36/controls/ctl-c2-0-do-nothing.json` (exit 1, stated [116,116] vs observed [122,122]); green after repair `.ufo/waves/round-36/c2/after-at-d2e46ef5.json` |
| M36-3 | counter keyed by unit name, so a duplicate row/box shadows the original | wave-1 `R36CriticC2Shortcut.md` class A1 (V2 fixture: three appended lines leave `116/116`, `receipts-B/`, `ScoutSkillPlacement.md` in place and score `met_target`); also A2 (other keys unvalidated), A3 (first match only), A4 (basename-suffix repair), A5 (population shrink), A6 (pointer count, not identity) | QUALITY #68 asks for predicate identity but no row asked the counter to enumerate every occurrence of a statement shape | QUALITY 77 (below). Not shown able to fail on the frozen counter (frozen, not edited); the round's C2 verdict is re-derived by a stricter non-counter check in wave 2 instead of being cited alone |
| M36-4 | receipt integrity read as provenance | wave-1 `R36CriticC1Shortcut.md` F1: an `after.json` fabricated from the oracle and re-hashed with REA's own 6.5.0 digest code scores `met_target` | QUALITY #67 (structure-blind replay) covers readers, not receipts | QUALITY 78 (below). The counter does reject edited-but-not-re-hashed envelopes (`controls/ctl-c1-2-forged-oracle-copy.json`, `after_evidence_id_ok false`, exit 1); provenance of the real receipts rests on four independent seat reproductions (`w1/R36ExecReproK{1,2,3,4}.md`) |
| M36-5 | report filed before the lane tip it describes (round 35) | fleet `33be25b8` (16:20:58 -03) precedes lane `3ca5a80f` (16:43:52); `.ufo/reports/round-35/kaidoku.md:56` says the wave had not settled | QUALITY 76 (seat accounting) — not the filing order | this round files only after `ls-remote` shows the final lane hash and after WAVE-DONE for every wave; the round-35 erratum is appended to `corpus/lessons/round-35.md` (R35-D5) |
| M36-6 | wave context dispatched without the literal `/fast/scratch` `find`/`du` restriction | `.ufo/waves/round-36/w1-spec.json` context: `grep -c 'find'` on the context → 0 (wave-1 `R36CriticRoutedCoverage.md`, R33-N1 recurrence) | QUALITY 60 | wave-2 context carries the sentence; red/green = `jq -r .context w1-spec.json | grep -c '/fast/scratch.*find\|find.*du'` vs the same on `w2-spec.json` |
| M36-7 | a frozen plan sentence pre-claimed hygiene not yet done | `plans/round-36-claims.md` "Routed defects … landed as appended corrections" while none had landed at the freeze (wave-1 `R36CriticRoutedCoverage.md:22-25`) | none | corrections appended this round (`corpus/lessons/round-34.md`, `corpus/lessons/round-35.md`, r34b entry trio); the plan sentence is left as written (frozen) and named here as a pre-claim |

## Gate

### Sources opened this round (2026-10-26)

- **S107 admit** — https://github.com/onekey-sec/sasquatch/releases/tag/sasquatch-v4.5.1-6, accessed 2026-10-26T04:26:58Z (wave-1 `R36ScoutSasquatchRelease.md`). Quote (9 words): "fix: remove unnecessary magic checks by @jstucke in #34". Deb digest `efbc92bd…ade95` equals the API digest; the installed binaries equal the deb members.
- **S108 admit** — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py, accessed 2026-10-26 (`R36ScoutUnblobHandler.md`); tag file sha256 `2d7b901b…599287` byte-identical to the installed handler. Quote (lines 58-62): `"-no-exit-code", "-f", "-d", "{outdir}", "{inpath}"`.
- **S109 admit** — https://github.com/neovim/neovim/releases/tag/v0.12.6, accessed 2026-10-26T04:27Z (`R36ScoutNeovimRelease.md`); API digests equal `carriers.json` K3/K4. Quote (3 words): "Download nvim-linux-x86_64.appimage".
- **S110 admit (assimilated, renumbered)** — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md, accessed 2026-10-26T04:36:42Z (`R36ScribeAssimilationGate.md` §2.3), sha256 `6544d60f…3716`. Quote (line 49): "For SquashFS support, also install [sasquatch](https://github.com/onekey-sec/sasquatch):".
- **S111 admit (assimilated, renumbered)** — https://raw.githubusercontent.com/devttys0/sasquatch/master/README.md, same access, sha256 `f09961ee…1fef`. Quote (line 12): "Very beta."
- **Rejected: AppImage Specification as authority for the offset rule** — https://github.com/AppImage/AppImageSpec (draft.md), accessed 2026-10-26 (`R36ScoutAppImageSpec.md` §2a). It says only that a type-2 image is an ELF "with a filesystem appended" and states no offset formula. Flip: an opened revision of the spec that defines the offset. The formula's real source, type2-runtime `runtime.c` `appimage_get_elf_size` ("The offset at which a filesystem image is expected = end of this ELF", line 527, commit `8f39b89e`), was located but not appended: no admitted entry cites it this round (the harness rule is recorded in SKILL as one operand of the runtime's rule).

No existing row's `status`, `recheck` or `used-by` cell changed this round; S106's used-by is unchanged (the r34b entry's appended trio cites it).

### Assimilation — theme sasquatch / unblob (`/home/vgpnk/Projects/shokuknow/merge/kaidoku`)

- **Id-collision check (scratch, before any append).** 0–3-space extractor: registry 106 ids, staged 132, `comm -12` → 1 collision `S106` (different documents: lane binutils readelf vs staged unblob README). Guard proof on a fixture with an indented `  | S002 |` row → `S002`. Evidence `.ufo/waves/round-36/assimilation/{reg-ids,staged-ids,collisions,id-guard-proof/}`.
- **Renumber map (by document).** staged S106 (unblob README) → lane **S110**; staged S107 (devttys0 sasquatch README) → lane **S111**. No other staged row is appended.
- **Append gate.** Scratch mirror (lane `corpus/` with S107–S111 and both new entries, plus `SKILL.md` and `tools/round-27/xpin-attribute.mjs` which S036/S081 cite) → `sources-census.sh validate --file` exit 0, the 9 pre-existing W04 only (`.ufo/waves/round-36/assimilation/validate-mirror.txt`). A first mirror of `corpus/` alone failed E11 on S036/S081 because those rows cite files outside `corpus/`; that is a mirror artefact, recorded so the next round copies the cited files first.
- **Decision 1 — ADMIT `unblob-sasquatch-dependency`** as `corpus/knowledge/2026-10-26-unblob-sasquatch-dependency.md`, with corrections c1 (pin by tag/commit/sha256 instead of `HEAD`), c2 (inference labelled; "sasquatch absent on this host" re-scoped to the 2026-10-23 snapshot), c3 ("fork" provenance wording dropped). PROVINCE scope: in (producer contract of the moved surface). Flip to refuse: either README digest changes, or a correction is reverted.
- **Decision 2 — REFUSE `sasquatch-prebuilt-package-inventory`** as staged: "each [release] carrying a Debian package per architecture" is false (`sasquatch-v1.0` is amd64-only) and the "release body shows 4.5.1 against 1.0" claim is not in the body (`R36ScoutPrebuiltInventory.md` claims 3 and 5). Flip: both corrected and re-opened.
- **Decision 3 — REFUSE `sasquatch-unblob-compatibility`** as staged: its evidence rows S184–S186 cite campaign-local `lanes/kaidoku/round8/work/*.tsv`, not lane-retained bytes (QUALITY #1), and the lane's own R36-C1 receipts supersede it. Flip: evidence imported into the lane and re-measured.
- **Decision 4 — REFUSE `sasquatch-unblob-compatibility-precondition`**: superseded premise (host-absence) — `R36ScribeAssimilationGate.md` decision 4.

### Quarantine slice (register `absent-defect-register.md`, kaidoku data rows: 5)

Re-checked live this round (`R36ScoutQuarantine.md`): S150 fabrication-class REFUSE (quoted heading absent; agrees with round 35); S113 locatable, but its "17 locales" count is false against live bytes (22 `hreflang` = 21 locales + x-default); S117 unverifiable (IEEE 202 empty body; not fabrication); S136 locatable own-work; S147 locatable local contract. None is cited by an admitted entry, so none is appended.

## Routed defects from r33–r35 closures

- Landed this round: r34 D-2 (31/32 seat accounting) and D-3 (r34b entry trio, appended) — `corpus/lessons/round-34.md` `## Corrections appended — round 36`, entry `## Provenance trio`; R35-D1..D5 — `corpus/lessons/round-35.md` `## Corrections appended — round 36`; r34 D-1 (start census in its own file before the first registry edit) — `.ufo/waves/round-36/census-start.txt` (106 rows, exit 0, 9 W04) committed in `790561d4`, the first SOURCES edit lands in `ffc81341`.
- r34 D-4 (eight-field registry rows): applied to the two round-36 counters (`SKILL.md` `### Round-36 instrument registry`); older five-column registries are not rewritten (history), stated reason.
- Stated reasons, not repaired: R33-2 (no depth claim this round; R33-C1 stays stopped), R33-3b/3d/3e and R33-4 (instrument limits of rounds 32–33; no round-36 claim depends on those instruments), R34-D5 (protocol lane).
- R35-D4 / `.jsc` frontier: still Frontier. An L1 pre-freeze probe (not a claim; scratch only, no committed receipt) saw the jsc2js patched d8 for V8 13.6.233.17 crash (SIGSEGV) on a node 24.21.0 code cache, and the 15.0.245.31 d8 crash while printing feedback metadata on an electron 43.7.11 cache — consistent with the jsc2js README's own warning that node-produced caches may not decompile. Recorded as a lead, not evidence.

## Criteria added (QUALITY 77–78)

See `corpus/QUALITY.md` rows 77 and 78.
