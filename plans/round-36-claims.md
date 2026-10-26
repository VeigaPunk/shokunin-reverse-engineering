# kaidoku round 36 — frozen claims (fresh-start round)

Base `cab59f221fe19726b5692bfa4d9a9679e96b8a73` (lane `main`, 2026-10-26). L1 `KaidokuR36` holds the
§3 planner seat. Fresh-start: the last three closures (r33, r34, r35) were rejected
(`corpus/lessons/round-3{3,4,5}-verifier-spotcheck.md`). Both claims below are scored only by the
counter, predicate and kill rule frozen in this file's commit; a do-nothing control is scored with
each frozen counter before any claimed data exists.

Owned axes coverage/depth/calibration are tied at 10 (`SCORECARD.md` `## Owned axes`); none is
retired. R36-C1 works coverage, so the lowest-axis rule is met.

## R36-C1 — coverage: sasquatch squashfs recursion moves from Frontier to Core

Surface moved: `PROVINCE.md` `### Round-4 frontier (post-unlock)` bullet **sasquatch** ("unblob's
squashfs recursion extractor (AUR-only); 7z fallback covers the carved-image path today") and
`corpus/README.md` Firmware row ("AppImage SquashFS carved but recursion blocked by missing
sasquatch"). REA `extract-firmware` (rea-agents 6.5.0, unblob 26.6.4) reports this exact gap as
`extraction_gaps[].kind = missing-extractor-dependency`, `dependencies = [sasquatch]`.

Command that shows it unmoved: the counter below at the base exits 1.

**Predicate P36-C1.** At the measured revision, for each of the four frozen carriers, the committed
REA extract-firmware receipt run with sasquatch on PATH publishes every regular file of the frozen
independent unsquashfs oracle (same relative path suffix, same sha256) with no sasquatch extraction
gap, the paired committed no-sasquatch receipt publishes none of them and names sasquatch as a
missing extractor dependency, both receipts recompute to their stored evidence id under the
rea-agents 6.5.0 rule, and PROVINCE.md holds a round-36 Core row naming sasquatch that cites the
round-36 knowledge entry, which cites a SOURCES.md row opened 2026-10-26 whose used-by lists that
entry.

- Carriers (frozen, `corpus/evidence/round-36/c1/carriers.json`): K1 synthetic LE v4 xz image; K2
  synthetic LE v4 gzip 4 KiB-block image with nested dirs and a symlink; K3 neovim v0.12.6
  `nvim-linux-x86_64.appimage` (sha256 `b644d034…f29fb`); K4 neovim v0.12.6
  `nvim-linux-arm64.appimage` (sha256 `8efcec73…e1c2`). K3/K4 digests equal GitHub's published
  release digests.
- Oracle (frozen before any sasquatch-enabled run): `/usr/bin/unsquashfs` 4.7.5 at the squashfs
  offset (0 for K1/K2; ELF end for K3/K4), regular files only — `corpus/evidence/round-36/c1/K*/oracle.tsv`.
- Before receipts (frozen with the claim; sasquatch absent from PATH): `K*/before.json`.
- Entry path `corpus/knowledge/2026-10-26-r36-sasquatch-squashfs-recursion.md`; Core heading
  `## Round-36 additions to Core`.
- **Target:** `carriers_matched == 4` and every binding true (`met_target`).
- **Counting command:**
  `python3 -I -B tools/round-36/c1-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --freeze <FREEZE> --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --json-out <RECEIPT>`
- Selftest: `python3 -I -B tools/round-36/c1-counter.py --selftest --pkg65 <same>` — 14 cases
  (1 green, 13 red: do-nothing, after:=before, forged oracle-copy envelope, before:=after, oracle or
  carriers changed after freeze, Core row outside the round-36 section, row without `sasquatch` in
  its first cell, row absent, `S1070` substring, source opened earlier, used-by lacking the entry,
  coverage map lacking the stem). Development inputs are a non-carrier probe image
  (`tools/round-36/selftest/dev-*`), never a carrier.
- Harness: `tools/round-36/c1-run.sh before|after|oracle CARRIER OUTDIR [SCRATCH]` (honours
  `$HYAKU_SCRATCH`, removes its scratch on exit).
- **Kill rule:** if any frozen control (CTL-C1-0 do-nothing at base, CTL-C1-1 no-sasquatch pipeline
  with all bindings present, CTL-C1-2 forged oracle-copy envelope) meets the target, C1 stops before
  any after-run. If the counter at the measured revision does not meet the target, C1 is an honest
  stop; the counter, predicate, carriers and oracle are never changed after this commit.
- Not claimed: big-endian / AVM SquashFS, vendor-mangled images, loader behaviour, anything about
  the extracted programs. 7z fallback is not re-tested.

Disclosed pre-freeze development probes (not carriers, never counted): one sasquatch-enabled REA run
on `tools/round-36/selftest/dev-le-xz.sqsh` (its receipts are the selftest fixtures) and one on a
scratch image holding `/usr/bin/true`, a `.gz` and a `.tar` (showed unblob keeps whole-file chunks
and publishes recursion output beside them). sasquatch for those probes ran from an unpacked copy
of the official `sasquatch_1.0_amd64.deb` in scratch.

## R36-C2 — calibration: self-assessment surfaces vs observed repo state

**Predicate P36-C2.** At the measured revision, the lane's current self-assessment surfaces — the
SCORECARD `## Owned axes` rows, the SCORECARD `## Capabilities` table rows and the SHONEN.md boxes —
carry zero mismatches with observed repo state: every backticked repo pointer in them resolves at
that revision (path exists, line range inside the file), the four stated counts equal the counts
the lane's command A / command B observe at that revision, and the three stated section ranges
equal the observed heading-to-last-non-blank-line ranges; with no unit removed, no fewer pointers
than at the base, and every pointer unresolved at the base repaired by a resolving pointer to the
same document.

- Before (base `cab59f22`): **3 mismatches** — unresolved `receipts-B/` (capability row "pre-registered
  two-lane live battery on REA 6.5.0"), unresolved `ScoutSkillPlacement.md` (SHONEN box 4), and the
  coverage row's `116/116 knowledge files mapped` against an observed 122/122.
- **Target:** `mismatches == 0` and `guards_ok` (`met_target`).
- **Counting command:**
  `python3 -I -B tools/round-36/c2-counter.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev <REV> --base cab59f221fe19726b5692bfa4d9a9679e96b8a73 --json-out <RECEIPT>`
- Selftest: `python3 -I -B tools/round-36/c2-counter.py --selftest` — 13 cases (1 green; red:
  do-nothing, junk count, deleted count, deleted pointer, substitution by another document, box
  removed, craft range off by one, Adjacent range wrong, range beyond file, new unresolved pointer,
  wrong calibration count, wrong SHONEN count).
- **Kill rule:** if a frozen control (CTL-C2-0 do-nothing, CTL-C2-1 junk counts, CTL-C2-2 delete the
  bad pointers, CTL-C2-3 substitute other resolving documents) meets the target, C2 stops before
  data. A miss at the measured revision is an honest stop; no counter change after this commit.
- Separability: C2 reads only SCORECARD/SHONEN/SKILL/PROVINCE/README/knowledge/result.json and is
  measured at its own landing commit before C1's entry lands, then again at the final tip (the
  coverage count it checks moves when C1 adds an entry; the row is re-stated then). C1 reads none
  of SCORECARD/SHONEN.

## Frontier step (§2b), assimilation, routed defects

- Census start captured before any registry edit: `.ufo/waves/round-36/census-start.txt` (exit 0,
  9 W04). End census is pasted in the report.
- Sourced claim: C1's entry cites rows opened 2026-10-26 (onekey-sec/sasquatch release, unblob
  `squashfs.py` handler, neovim release).
- Assimilation theme: `merge/kaidoku/` sasquatch/unblob entries (`unblob-sasquatch-dependency`,
  `sasquatch-prebuilt-package-inventory`, `sasquatch-unblob-compatibility`) — per-entry gate with ≥1
  admit and ≥1 reject; collision check per addendum §10 before any append.
- Routed defects still open from r34/r35 closures (D-2 seat accounting 31/32, D-3 entry trio for
  `2026-10-25-r34b-…`, R35-D1..D5) are hygiene, not claims, landed as appended corrections.
