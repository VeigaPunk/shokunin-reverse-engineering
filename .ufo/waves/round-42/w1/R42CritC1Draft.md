# R42CritC1Draft — attack of the DRAFT R42-C1 (SquashFS v3 through REA, Frontier → Core)

VERDICT: DEFECTS FOUND — the coverage premise (a) is confirmed unmoved, but the draft
predicate as written cannot survive its own oracle gate on the real v3 flavor, would
emit a forbidden gap on full-file carriers, and does not bind the two-reader oracle or
the fabrication control tightly enough. Concrete text changes in §6.

All probes ran 2026-10-26 in scratch `S=/fast/scratch/hyaku/kaidoku-r42/R42CritC1Draft`
(removed on exit). Artifacts: `.ufo/waves/round-42/w1/artifacts/R42CritC1Draft/`
(`probe-log.txt`, `reader-matrix.txt`, `dev-full-after.json`, `dev-trunc-after.json`,
`unsquashfs-err.txt`, `7z-listing.txt`). No REA/unblob run touched any candidate
published carrier; the only third-party image exercised is the designated development
OpenWrt Kamikaze 7.09 rootfs and the MIT unblob fixtures.

---

## 1. (a) Is SquashFS v3 through REA really ground the lane does not hold? CONFIRMED unmoved

Sweep at base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (read-only git grep over
`tools/ plans/ .ufo/ SKILL.md PROVINCE.md SCORECARD.md corpus/` for `squashfs_v3|squashfs-v3|v1–v3|v1-v3|s_major`):
- No receipt, after.json, handler string, run log or score names `squashfs_v3` or any
  v1–v3 handler. Corpus hits are only (i) the producer-statement knowledge entry
  `2026-10-26-unblob-format-matrix.md` (ten SquashFS sections, "coverage claim only,
  never an extraction outcome", and the vendor-mangled v3 variants explicitly "still
  unmeasured lane Frontier") and (ii) byte copies of unblob's `squashfs.py` handler
  source in wave artifacts (r38–r40).
- Round-41's carrier named "V3" (FRITZ!Box 5490) is **not** a SquashFS v3 run: its
  receipt names handler `squashfs_v4_be`, magic `sqsh` v4.0
  (`R41W2ReproV3.md` clause table). The lane's only measured SquashFS runs are v4.

Conclusion: a Core row for v3 through REA is a coverage move under prompt §9
("name the surface the round changes … the command that would show it unmoved" —
the draft's counter-exit-1 at freeze does that). No re-score concern.

## 2. (b) Can the kill-rule controls reach 4/4 under P42-C1?

- **CTL-C1-0 (do-nothing): no.** No receipts exist at the freeze; `carriers_matched`
  0, exit 1 — same shape as round-41's scored CTL-C1-0 (`ctl-c1-0-do-nothing.json`,
  `carriers_matched 0, exit_code 1`). Unobjectionable.
- **CTL-C1-1 (round-41 receipts relabelled): no, provided the port keeps the round-41
  clause set.** Each relabelled receipt fails at least: `handler_ok` (names
  `squashfs_v4_be`, not a `squashfs_v3*` handler), `subject_pin_ok` (round-41 subject
  digests cannot equal round-42 pins), `oracle_hits_ok`/`gaps_ok` (round-41 oracle and
  non-regular tables don't match v3 carriers), and `run_provenance_ok` (output dirs
  carry `/kaidoku-r41/`, not `/kaidoku-r42/`). Round-41's identical relabel test
  (S2 in `R41W2C1Fabricate.md`) scored 0/4 with exactly these failures. Keep the
  `carrier_fresh_ok`/`prior_pins` mechanism in the port so a rename is still
  distinguishable.
- **CTL-C1-2 (oracle-only fabricated receipt): HIGH RISK of meeting the target — this
  is the defect.** Round-41's fabrication attack (`R41W2C1Fabricate.md` S1) showed the
  full frozen counter, *including* the counter-time REA rerun projection, accepted
  oracle-only fabrications for V3/L3/L4 (3/4 carriers `matched: true`); only V4
  refused because its `MaliciousSymlinkRemoved` set is extractor-determined. A v3
  carrier built on the empirical profile below (all symlinks kept, 0 removals, fixed
  derivations, pinned engine, `published_bytes` ≡ Σ oracle sizes, coverage forced by
  depth-1 replay) is fully oracle-closed: every `plus-extractor` field is derivable
  from the frozen tables + pinned toolchain. So CTL-C1-2 could plausibly score 4/4,
  which under prompt §9 means "the counter or target is wrong — fix it before data".
  The draft's kill rule therefore does **not** currently guarantee the claim is
  unreachable by its own control set. Minimal fixes in §6 (5)(6).

## 3. (c) Two-reader oracle: independence and the disagreement case

Independence is real (unsquashfs 4.7.5 vs 7-Zip 26.04, separate codebases). But the
pair fails on the dominant real v3 flavor:

- **unsquashfs 4.7.5 reads v1–v3 gzip only.** On LZMA-compressed v3 it errors:
  `gzip uncompress failed with error code -3 … FATAL ERROR: File system corruption
  detected` (fixtures `v3_le.lzma.bin`/`v3_be.lzma.bin` and the real image below).
- **7-Zip 26.04 reads v3 gzip and LZMA, BE and LE, but its listing carries no entry-kind
  discrimination**: symlinks appear as `.....` (regular-file) rows with size = target
  length; no `l`/`c`/`b` attribute letters. It alone cannot produce the non-regular
  table the gap rule consumes.
- **Observed disagreement on the reference development carrier**: OpenWrt Kamikaze
  7.09 `openwrt-atheros-2.6-root.squashfs` (md5 `d0a4cbd0c81f158aa852ae57360d410f` =
  archive `md5sums`; sha256 `70d7c4c7ce6794a627bdfb38a1efae45363888a194caef260f389be5241aff58`;
  BE SquashFS 3:0, 7z `Method = LZMA Spec`, fs 995971 B, physical 999424 B, 180224 B
  zero tail). `unsquashfs -lls` fails; 7z lists it fully.
- Therefore the draft's gate "must agree file-for-file before a carrier freezes" can
  only be satisfied on **gzip v3** carriers. All named examples (DD-WRT `tqsh`
  = v3-DDWRT magic `74 71 73 68`, OpenWrt Kamikaze 7.09/8.09 rootfs) are LZMA-class
  v3, so with this exact reader pair the real-world carrier universe is effectively
  the gzip v3 subset, which we did not verify publicly available in four fresh
  published instances. This is a feasibility gate the freeze must close, not a
  stylistic detail.

## 4. (d) What a real v3 rootfs does to the gap rule

Measured on the Kamikaze 7.09 rootfs through REA 6.5.0 (`--max-depth 1`, unblob
26.6.4, sasquatch 4.5.1):

- Truncated-to-fs receipt (`dev-trunc-after.json`): chunks `['squashfs_v3']`, 147
  published regular files, gaps = 1 `depth-limited` + **162** `unpublished-entry`
  (the 162 symlinks), 0 `MaliciousSymlinkRemoved`, 0 `unknown-chunk-handler`;
  `published_bytes 2914612`; coverage partial. Extraction tree: 44 dirs (many empty),
  0 char/block devices materialised, 0 hardlink-inode duplicates.
- Full-file receipt (`dev-full-after.json`): adds 1 `unknown-chunk-handler` gap
  (range 999424/180224 — the zero tail) and one extra published file
  `firmware.bin_extract/999424-1179648.unknown`; 148 files.

Changes the v3 port needs:
1. **Carrier extent vs `bytes_used`.** unblob's v3 chunk ends at the padded boundary
   (1024/4096), not at `bytes_used` (995971 → 999424). A pin/carve defined as
   `bytes_used` is shorter than the extracted chunk; a full published file carries
   trailing material. The round-41 `carve_ok` semantics ("frozen length ==
   `bytes_used`") does not transfer verbatim; freeze the carved length as the
   unblob-computed chunk end (999424 here) or explicitly allow the padded end.
2. **`unknown-chunk-handler` is unavoidable on full-file carriers.** The predicate
   forbids it ("no `unknown-chunk-handler`"), so as written the claim cannot pass on
   a published file with any non-fs residue (kernel/loader/padding). Either carriers
   are carved fs extents (documented carve + fetch chain, exactly as round-41's V4
   nested member) with the forged gap rule intact, or the gap rule gains an explicit
   single `unknown-chunk-handler` allowance for container residue — the carve route
   is the smaller change and matches round-41 precedent.
3. **Extra published regular files are unconstrained.** `oracle_hits_ok` is
   one-directional (every oracle row must be published); nothing forbids publishing a
   non-oracle regular path (the `.unknown` slice above is exactly that). Tighten with
   a published ⊆ oracle binding for regular files, or a v3-tail carve guarantees it
   away.
4. **Kinds.** Real v3 rootfs rows observed: symlink (all kept → `unpublished-entry`,
   no removals), dir (invisible), device nodes (invisible in extraction; oracle row
   kinds from the reader that reports them), empty dirs (invisible). Hard links, if a
   carrier has them, are two regular oracle rows (both must publish) — no new
   non-regular kind; `.` entries do not occur in SquashFS listings, no change.
5. **`depth-limited` placement**: on the v3 extract root
   (`firmware.bin_extract/0-999424.squashfs_v3_extract`) — same structural gap
   semantics as round-41.

## 5. (e) Missing kill rules / bindings

1. **Oracle provenance is unbound.** The predicate freezes oracle/non-regular tables
   but does not freeze the writer and the two-reader agreement witness. A table could
   be hand-built; the counter cannot detect it. Freeze `tools/round-42/oracle-*.py`
   plus a per-carrier `reader-agreement.json` (both readers' raw listings + equality
   verdict), mirroring round-41's `oracle-run.json`.
2. **Expected handler naming.** "a `squashfs_v3*` handler (the one frozen per
   carrier)" is a glob over a family that includes vendor variants
   (`squashfs_v3_ddwrt`, `_broadcom`, `_nonstandard`) and the nonexistent
   `squashfs_v3_adaptive` (a fixture folder name; the installed 26.6.4 handler source
   defines no adaptive class — plain `squashfs_v3` handles gzip *and* LZMA via
   `sasquatch -be|-le`, verified). Freeze an exact allowed handler set per carrier
   and define in the plan that LZMA v3 lands on `squashfs_v3`.
3. **`layout_ok` has no v3 probe yet.** The round-41 probe is AVM-v4-specific
   (marker, LE metadata block lengths). The port needs a v3 superblock probe (major
   3 at the v3 struct offsets, magic `sqsh`/`hsqs`, and a compression/flags read);
   the predicate's "magic/major/compression" wording must be resolved to that probe.
4. **Reservation safety of control evaluation.** The counter's rerun runs REA on
   carrier *; if CTL evaluation invoked it, a control run would violate the reserved-
   carriers binding. State in the plan that control scoring short-circuits before any
   rerun (no receipt → no rerun → no REA on any published image).
5. **Fabrication control must be scored before data.** Add CTL-C1-3 = the
   oracle-closed fabricated receipt (R41W2C1Fabricate S1 style) and require it *not*
   met with the frozen counter; if it is met, the projection/claim is wrong (prompt
   §9). Because v3 carve carriers are oracle-closed, pair this with either (a) a
   stronger per-carrier extractor-determined projection component, or (b) an explicit
   disclosure in the claim prose that oracle-only fabrication is indistinguishable for
   these carriers (the R41W2C1Fabricate §4 options), or (c) deliberately choosing
   carriers that exercise extractor-determined removal sets.
6. **Determinism check on the dev arm.** The rerun-equality binding assumes REA
   output determinism on identical bytes; the freeze dry run (QUALITY 84) must
   demonstrate it for the actual v3 toolchain (round-41 measured profiles were stable;
   re-verify for v3 LZMA).

## 6. Smallest safe corrections (predicate text deltas)

- Oracle section: "two producers that are not sasquatch — `unsquashfs` 4.7.5 and
  7-Zip — must both read the carrier and agree file-for-file on the regular-file
  inventory before a carrier freezes; the non-regular table's kinds come from the
  reader that reports them; every reader run is recorded in a frozen
  `reader-agreement.json`."
- Carriers section: "carriers are published third-party images; the REA input is the
  frozen carve of the SquashFS extent (length = the unblob chunk end, e.g. padded
  1024/4096), fetched under the pinned URL + md5/sha256 chain; trailing non-fs bytes
  are outside the carrier."
- Gap rule: keep `unknown-chunk-handler: 0` (carve route); add "published regular
  files ⊆ oracle regular rows" to the exact-path publication clause; add a v3 layout
  probe binding; add the per-carrier exact handler set.
- Kill rule: add CTL-C1-3 (oracle-closed fabricated receipt, scored 0/4 required)
  and the no-rerun-on-controls reservation sentence.
- Feasibility gate at freeze: four published gzip-v3 (or renegotiated reader pair)
  carriers readable by both pinned readers; if unavailable, the claim must be
  re-scoped before freeze, never after.

Evidence: `artifacts/R42CritC1Draft/probe-log.txt` (commands, versions, exit codes),
`reader-matrix.txt` (per-reader × per-input results), `dev-full-after.json`,
`dev-trunc-after.json` (fresh REA envelopes), `unsquashfs-err.txt`,
`7z-listing.txt` (the LZMA failure and the kind-less 7z listing).
