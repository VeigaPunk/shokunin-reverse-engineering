# R42Assim — per-candidate verdicts

Scope: the four named candidates plus every staged entry naming SquashFS v3, DD-WRT or OpenWrt.
`grep -ril -e squashfs -e dd-wrt -e openwrt -e tqsh -e kamikaze` over
`merge/kaidoku/knowledge/` returns **10** files — `avm-firmware-image-unblob`, `avm-image-build-blocker`,
`avm-image-extraction`, `avm-le-image-genuine-marker`, `avm-le-variant-reachability`,
`sasquatch-prebuilt-package-inventory`, `sasquatch-unblob-avm-branch`, `sasquatch-unblob-compatibility`,
`unblob-format-matrix`, `unblob-sasquatch-dependency`.

Per-term counts over the staged knowledge files (`grep -ril`, 2026-10-26): `SquashFS v3` 0,
`squashfs-3` 0, `squashfs_v3` 0, `DD-WRT` 0, `tqsh` 0, `Kamikaze` 0, `OpenWrt` 1
(`avm-image-build-blocker.md:31`, a distfiles list), `v3` 2 (`firmware-region-vocabulary.md` — binwalk
v3; `unblob-format-matrix.md:24-25` — "SquashFS (v2-non-standard), (v3-non-standard), (v3-Broadcom),
(v3-DDWRT) …"). So the **only** staged entry naming SquashFS v3 or DDWRT is `unblob-format-matrix`,
which the lane **already admitted** in round 38 (`corpus/knowledge/2026-10-26-unblob-format-matrix.md:21-22`
lists all ten SquashFS sections, `v3`, `v3-Broadcom`, `v3-DDWRT`, `v3-non-standard` among them). The
package therefore supplies **no new v3 extraction material** for R42-C1 — only the handler-name
inventory, which is held.

| # | entry | verdict | reason (one line) | flip condition |
|---|---|---|---|---|
| 1 | `sasquatch-prebuilt-package-inventory.md` | **ADMIT (re-grounded)** — draft `drafts/entry-A-sasquatch-release-matrix.md` | r36's two falsified sentences are both corrected on live bytes today (the arch matrix starts at v1.0.1, v1.0 is amd64-only; no body states a version pair), and the asset citation moves from the page to the API | a refetch shows a ninth release, a changed asset set, or a release body that states a package/upstream version pair |
| 2 | `avm-le-image-genuine-marker.md` | **ADMIT-AFTER-REWRITE** — draft `drafts/entry-B-avm-le-marker-le-squashfs.md` | r40's three corrections are now written against re-read bytes, plus two the staged text needed (the lane does not hold the image; the "patched" reader's message is mislabelled); central claim reproduces | the retained image loses the marker (`mkfs_time != bytes_used`) or the little-endian arm starts testing it |
| 3 | `avm-le-variant-reachability.md` | **REJECT** | headline falsified by retained bytes: a clean plain-Freetz build needing no option patch already sets 361 == 361 and is byte-identical to the option build; third refusal of this entry (r39, r40, here) and it still carries no reversal pointer | a rewrite that keeps only the surviving define-value fact (`#define AVM_LE 2`, `#define AVM_BE 3`) with a reversal line naming `avm-le-image-genuine-marker` |
| 4 | `sasquatch-unblob-compatibility.md` | **REJECT** | cites a movable `unblob/main` file, rests on a campaign-local TSV that contradicts its own "exercised" sentence, and every observation it makes is held in-lane with receipts | an entry re-grounded on S108 + S110 + the r36/r38/r39 receipts stating a fact the lane does not already hold |

Not re-adjudicated this wave (held status, re-checked only for overlap): `unblob-sasquatch-dependency`
(admitted r36), `unblob-format-matrix` (admitted r38), `sasquatch-unblob-compatibility-precondition`
and `sasquatch-unblob-avm-branch` (refused r36/r38, refusals stand), `avm-firmware-image-unblob`,
`avm-image-build-blocker`, `avm-image-extraction`, `avm-image-extraction`→`2026-10-26-r40-avm-be-squashfs-core`
(rejected/admitted in r39/r40 with standing reasons).

---

## 1. `sasquatch-prebuilt-package-inventory` — ADMIT, corrected

**Prior decision, quoted.** `corpus/lessons/round-36.md:42`: "REFUSE `sasquatch-prebuilt-package-inventory`
as staged: 'each [release] carrying a Debian package per architecture' is false (`sasquatch-v1.0` is
amd64-only) and the 'release body shows 4.5.1 against 1.0' claim is not in the body … Flip: both
corrected and re-opened."

**Defects in the staged text.**
- `:10-11` "each carrying a Debian package per architecture" — false as a universal: the oldest
  release `sasquatch-v1.0` carries 2 assets, both amd64.
- `:13-14` "The release body shows the packaged upstream version (`4.5.1`) against the package version
  (`1.0`)" — false: the 645-byte body of `sasquatch-v4.5.1-6` lists three change lines, new
  contributors and a changelog link; `sasquatch-v1.0`'s body is empty.
- `:4` the source is the **rendered page**, which in bytes carries no asset filename
  (`grep -c 'sasquatch_1.0_amd64.deb'` → 0); the assets are the REST endpoint's fields.
- `:14` "records the build fixes it carries ('unsquashfs: fix prototypes for C23')" — **holds**
  (body line 2). `:6` recheck (`grep -c … -> 12`) — **reproduces** (`12`, 2026-10-26T21:53:35Z).

**Why admit.** The surviving claim is domain-specific, falsifiable, re-countable, and new to the
lane's knowledge files: 8 releases, seven with the three-arch matrix and one without, the matrix's
start tag, and the fact that the API's `digest` field exists only for the newest release. Held row
S107 records the newest tag's six assets and holds the `usr/bin/sasquatch` member digest
(`ad02d27a…`), which I re-hashed on the installed binary today — so the entry can bind the published
package to the running tool. Held entry `2026-10-26-unblob-sasquatch-dependency` records the
Debian-package *route*; it does not record the arch matrix, so this is not a duplicate.

**Overlap disclosure.** The staged headline's second half ("the AUR was never the only route") is
**already held** (`unblob-sasquatch-dependency:43` point 4). The draft therefore re-titles the entry
to its surviving claim (the matrix and its start tag) and does not restate the route fact as news.

## 2. `avm-le-image-genuine-marker` — ADMIT after rewrite

**Prior decision, quoted.** `.ufo/waves/round-40/w1/R40AssimReject.md` verdicts table: "ADMIT-AFTER-REWRITE
… `:30` generalises the LE observation, `:55-56` denies a mechanism that exists, and it records
success without the exit-code caveat"; `corpus/lessons/round-40.md:81`: "deferred (LE scope;
admissible in an LE-AVM round after its `:30`/`:55-56` corrections)".

**What I re-verified today (all receipts in `receipts/`, commands in `sources-reopened.md`).**
- `avm-le-genuine.squashfs` and `avm-le-plain550.squashfs` are **byte-identical**, sha256
  `18d3ad05…`, 4096 B; `unsquashfs -s` reports `Filesystem size 361 bytes` and a creation time that
  is exactly epoch + 361 s. `avm-le-standard-time.squashfs` (`6d787405…`) keeps a real 2026-10-24
  timestamp.
- The marker's producer is Freetz patch **550**, not the option patch **613**: 550 writes
  `sBlk->mkfs_time = (int) sBlk->bytes_used;` under the `TARGET_FORMAT` test with no other
  condition; 613 wraps that assignment in `if (!use_standard_mkfs_time)`, default `TRUE`. The
  campaign's own copies of both patches are byte-identical to the upstream fetches.
- The handler reads the marker only inside `case Endian.BIG, 4:`; the little-endian arm appends
  `-le` without parsing.
- `sasquatch-v4be -be` on the marker image: exit 1, "FATAL ERROR: Block size too small.  File system
  is corrupt.", 0 files (my run).
- Stock `unsquashfs` lists 4 files; `apple1.txt` reads `apple`.

**Corrections applied in the draft.**
1. `:30` "invisible to it" → scoped to the little-endian arm, with the big-endian arm named.
2. `:55-56` "does not say unblob *recognises* the AVM marker" → replaced by the two-arm statement.
3. Exit-code caveat added (WARNING→0), with the file count named as the witness.
4. "what the lane keeps is the 4096-byte image" → false: the lane holds no AVM_LE image; bytes are
   imported with the draft, plus a proposed `corpus/evidence/round-42/s132/` landing on the
   `round-41/s126/` precedent.
5. TSV row `upstream_unsquashfs_stat` → `patched_unsquashfs_stat`; the stock reader's rendering is
   given beside the patched string.

**Scheduling clause, recorded rather than assumed.** r40's deferral also required "an LE-AVM round".
Round 42 works the **little-endian v3** arm, not AVM_LE, so that clause is **not literally met**. The
draft is complete and verified either way; landing it now is the L1's call, and if it is held, the
hold is a scheduling decision, not a doubt about the content.

## 3. `avm-le-variant-reachability` — REJECT

**Reason.** Two of its three load-bearing sentences are falsified by retained bytes:
- `:23-24` "`mkfs_time` … does **not** equal its `bytes_used` … so it is not an AVM image" — true of
  the round-12 run only because that run used the stale binary (S133: the binary hash is unchanged
  across the define change).
- `:30-33` "What would close the variant … The `AVM_FORMAT_AS_OPTION` build …" — falsified:
  `avm-le-plain550.squashfs` came from the plain recipe, with no `-no-mkfs-time` and no option
  build, and is byte-identical to the option build's marker image.

Third refusal in a row (r39, r40, wave 1 here) and the entry still carries no reversal pointer to
the sibling that overturns it. Its **one surviving fact** — patch 101 defines `AVM_LE 2` and
`AVM_BE 3`, and `AVM_BE_AVM_LE` occurs in no patch body — is real (I re-fetched the patch: 1153 B,
sha256 `e28b3341…`, identical to the campaign's local copy) and belongs in the rewritten sibling,
which cites it through S135's sibling fact anyway.

**Flip.** A rewrite titled to the define-value fact, carrying the reversal line and no reachability
claim.

## 4. `sasquatch-unblob-compatibility` — REJECT

**Reason, three separable grounds.**
1. **Movable reference.** `:4` cites `unblob/main`. Today `main` and tag `26.6.4` are the same bytes
   (both sha256 `2d7b901b…`), which is exactly why the citation looks safe and is not: round 38
   refused `sasquatch-unblob-avm-branch` for the same class of reference.
2. **The evidence contradicts its own sentence.** `:33-34` says the `sasquatch-v4be` branch is
   "exercised, not assumed", while the TSV it cites (`lanes/kaidoku/round8/work/lead3-sasquatch-compat.tsv`,
   2175 B, sha256 `83953548…`) holds the row `be_image_built … so the sasquatch-v4be branch was NOT
   exercised`. The TSV's reconciliation row (`be_fixture_source`) is not cited, and the entry's
   `recheck:` greps `unsquashfs version 4.5.1` — it attests the version row and never the big-endian
   claim.
3. **Superseded content.** Every observation it makes is held, with in-lane receipts: LE extraction
   4/4 and the missing-dependency gap (`2026-10-26-r36-sasquatch-squashfs-recursion`), BE v4
   (`2026-10-26-r38-…`, `2026-10-26-r39-be-squashfs-v4-core`), the declared-dependency contract and
   the host-state correction (`2026-10-26-unblob-sasquatch-dependency` points 1 and 3). Round 36's
   stated flip ("evidence imported into the lane and re-measured") has fired in substance, and what
   it produces is the lane's own entries, not this one.

**Flip.** An entry re-grounded on S108 + S110 + the lane receipts that states a fact the lane does
not already hold — and then it is a different entry.
