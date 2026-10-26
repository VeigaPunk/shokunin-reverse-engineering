# kaidoku round 42 — frozen claims

Base `c4a38ea2fcd7a7da096358f9bf462c9a4be3c33c` (lane `main` at round start; the round-41 closure spot-check
`corpus/lessons/round-41-verifier-spotcheck.md` sits on it). `ae5dc3f3` (round-41 wave-2 evidence, landed by the
round-41 L1 at 21:44Z after this round started) and the draft commit `fdabdfa4` descend from it. L1 `KaidokuR42`
holds the §3 planner seat. Wave 1 (43 seats, `.ufo/waves/round-42/w1/`) built and attacked the draft; the rule for
each claim is the bytes of this file, its tools and its frozen inputs in the commit that first adds this version
(the freeze). Every change from the draft is in `## Changes from the draft`. Controls are scored before any claim
data.

Owned axes coverage/depth/calibration are tied at 10, none retired; on the tie every owned axis is a lowest axis.
R42-C1 works coverage, R42-C2 works depth. The round-41 `planned` row named depth first; its routed defect R41-CL4
(the v3 table sends every SquashFS v1–v3 chunk to `no-squashfs-chunk`/`unclassified`,
`corpus/knowledge/2026-10-26-r41-sqfs-triage-v3.md:22-25`) and the two A1 decisions below are why the depth claim is a
new table (v4) with new decisions and not a re-score of v3 (prompt §9).

## Freeze-integrity rule (both claims; carried from rounds 39–41)

A score at `REV` is admissible only if no commit in `FREEZE..REV` touches a frozen path of that claim; a later
restore does not un-block (exit 2 `frozen_path_changed`, never `met_target`). Control tables and their development
inputs are committed in the freeze. Every score receipt records the scorer's exit code and `counter_sha256`, the
sha256 of the counter file it ran (round-41 closure D4). QUALITY 84: both counters were dry-run end to end, as frozen,
on development arms before the freeze, every binding evaluated (`.ufo/waves/round-42/l1/dryrun-c1.json`,
`dryrun-c2.json`; the C1 dry run caught two probe defects first, `dryrun-c1-pre.json`, see `## Changes from the draft`).

## R42-C1 — coverage: SquashFS v3 (unblob `squashfs_v3` and `squashfs_v3_ddwrt`) through REA `extract-firmware`, Frontier → Core

Surface moved: the lane holds SquashFS v1–v3 only as a producer statement (`corpus/knowledge/2026-10-26-unblob-format-matrix.md`,
"coverage claim only, never an extraction outcome") and as the v3 table's cause text; no REA run on a v3 chunk is in
the committed corpus at the base (`w1/R42CritC1Draft.md` §1 sweep). After the move PROVINCE holds `## Round-42
additions to Core` naming the `squashfs_v3` handler family, the entry `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md`,
a README coverage-map row and SOURCES rows for the carriers' publishers. Command that shows it unmoved: the C1
counter at the freeze exits 1 (no round-42 receipts, no Core row).

**Predicate P42-C1** (implemented by `tools/round-42/c1-counter.py`; its docstring's clause list is the full text).
At the measured revision, for each of the four frozen carriers, the committed round-42 REA 6.5.0
`extract-firmware --max-depth 1` after-receipt (unblob 26.6.4, plain `sasquatch` 4.5.1 under the fixed PATH), first
added in a commit descending from the freeze, names exactly the carrier's frozen handler with no failed chunk;
publishes exactly the frozen oracle's regular-file set (both directions: no oracle file missing, no extra file) at
exact, segment-bounded relative paths under the chunk extract root with equal sha256 and size, and no non-regular
oracle entry as a file; accounts for every non-regular row by the frozen gap rule
(`.ufo/waves/round-42/c1/gap-rule.json`: one `unpublished-entry` gap or one `MaliciousSymlinkRemoved` diagnostic
per symlink, devices and directories invisible, exactly one structural `depth-limited`, no `unknown-chunk-handler`);
has subject digest = carrier pin and a recomputable evidence id (frozen `tools/round-27/xpin-attribute.mjs` against
the REA package pinned by `tools/round-42/rea-pkg.json`); the carrier bytes hash to the pin, their length equals
unblob's chunk end, and the v3 superblock probe reads the frozen magic, major 3, endianness and compression; the
frozen fetch receipt chains https URL (HTTP 200, no redirect) → image sha256 → carve → pin; the committed
`extract-env.json` names the frozen `sasquatch`/`unblob` digests, the fixed PATH and an unblob log line running
`sasquatch` with `-le`/`-be` matching the carrier (never `sasquatch-v4be`); the pin is not in
`tools/round-42/prior-pins.json`; a counter-time REA rerun under the fixed PATH has the same projection; PROVINCE
holds the `## Round-42 additions to Core` row and a `Round-42 frontier note`, the entry exists and cites a SOURCES
row absent at the base whose used-by lists it, README maps the entry; no frozen C1 path changed after the freeze.

- Carriers (`.ufo/waves/round-42/c1/carriers.json`, fetch receipts `fetch-<id>.json`, oracles
  `corpus/evidence/round-42/c1/<id>/`), all LZMA SquashFS 3.0, all published bytes whose md5 equals the publisher's
  own md5sums line (`w1` fetch, L1 re-fetch 22:52Z):
  - **OW-A8092** OpenWrt Kamikaze 8.09.2 `atheros/openwrt-atheros-root.squashfs`, BE `sqsh`, `squashfs_v3`, carve
    [0, 1564672), 409 regular files / 272 non-regular rows;
  - **OW-X86FS** OpenWrt Kamikaze 8.09 `x86/openwrt-x86-squashfs.fs`, LE `hsqs`, `squashfs_v3`, [0, 1183744), 403 / 261;
  - **DW-MEGA** DD-WRT v24 `dd-wrt.v24_mega_generic.bin` (WRT54GL dir), LE `hsqt`, `squashfs_v3_ddwrt`,
    [923752, +5091328), 447 / 265;
  - **DW-FONERA** DD-WRT v24 `Atheros WiSoc/Fonera/linux.bin`, BE `tqsh`, `squashfs_v3_ddwrt`, [851968, +5832704), 569 / 250.
  Bytes are never committed; `tools/round-42/fetch-carrier.py` rebuilds them into a cache.
- Oracle (`tools/round-42/sqfs3-oracle.py`, run through `c1-run.sh oracle`): producer 1 backhand-cli 0.25.5 built by
  the L1 with features `v3,v3_lzma` (`/home/vgpnk/.local/opt/backhand-0.25.5-v3/bin/unsquashfs-backhand`, cargo
  install 2026-10-26), producer 2 7-Zip 26.04 (`7z l -slt` modes, `7z x` regular contents); unsquashfs 4.7.5 reads no
  LZMA v3 and is a third producer only where it reads. The DD-WRT magics are normalised to `hsqs`/`sqsh` on a copy
  for the readers only; the carrier pin is the published bytes. Both producers agree on every regular file of all four
  carriers (`oracle-run.json`: verdict `agree`). Neither producer is sasquatch or unblob.
- Target: `carriers_matched == 4`, every binding true, exit 0.
- Counting command: `python3 -I -B tools/round-42/c1-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --carrier-cache <CACHE> --work <SCRATCH> --json-out <OUT>`,
  with `<CACHE>` filled by `python3 -I -B tools/round-42/fetch-carrier.py --spec .ufo/waves/round-42/c1/fetch-spec.json --cache <CACHE> --work <SCRATCH>`.
- Data procedure (after the freeze, never before): `bash tools/round-42/c1-run.sh after <CACHE>/<pin>.bin corpus/evidence/round-42/c1/<id> <scratch under /kaidoku-r42/>`.
- Kill rule: a control meeting the target stops C1 before any carrier run. Controls scored at the freeze:
  CTL-C1-0 do-nothing (no receipts, no Core row); CTL-C1-1 the round-41 V3/V4/L3/L4 receipts copied to the round-42
  receipt paths. Control scoring never runs REA (no receipt → no rerun).
- Reservation: no REA, unblob or sasquatch run touched the four carrier images or their carves before the freeze;
  readers only (backhand, 7z, unsquashfs, the counter's pure superblock probe). Development carriers burned by the
  dry run: OpenWrt 7.09 atheros root and x86 image, DD-WRT v24 mini generic and Ubiquiti LS2.
- Disclosed limits: the counter-time rerun proves the carriers extract through the pinned toolchain at scoring time
  with the same projection; it cannot prove which process wrote the committed receipt (R40-CL2 stays open). None of
  the four images holds a device node, so the "devices invisible" clause is not exercised. All four are LZMA.
- Not claimed: v1/v2 images, `squashfs_v3_broadcom`/`_nonstandard`, v4 Broadcom, gzip v3, anything about extracted programs.

## R42-C2 — depth: SquashFS outcome-triage table v4 covering the whole SquashFS handler family

Surface moved: `SKILL.md` `## Queue-drain craft` gains rule block 21 with `<!-- sqfs-triage-table v4 -->`, its
action line and `corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md`; block 20 gains a supersession sentence.
Command that shows it unmoved: the frozen v4 interpreter on the base `SKILL.md` exits 2 (no v4 marker); the v3
table transcribed under the v4 marker (CTL-C2-0b) labels every legacy-chunk envelope `no-squashfs-chunk` or
`unclassified`.

Draft label precedence, **amendment A1 (2026-10-26 ~22:20Z, after `w1/R42CritC2Draft.md`, `w1/R42C2ReconCombo.md`,
`w1/R42C1DevRun.md`)** — the first draft widened the handler domain and added one row; the critic showed that is
mostly a re-score. A1 adds two further decisions the v3 table gets wrong on real REA envelopes: a SquashFS chunk
that sits below the depth budget inside a container (whole OpenWrt TRX at `--max-depth 1`: H = {`trx_v1`},
G = {`depth-limited`} — v3 says `no-squashfs-chunk`/`inspect-input`), and unclaimed bytes beside a SquashFS chunk
(carve tail: G ∋ `unknown-chunk-handler`, REA publishes `<start>-<end>.unknown` — v3 says `unclassified`).
Expected pairs come from this text through an independent evaluator.

Features of one REA envelope (round 41's, `plans/round-41-claims.md:109-115`, plus F, L, HF): OP = `operation`;
PR = `provider.id`; H = handler names in `normalized_result.chunks[].handler` ∪ `normalized_result.extraction_gaps[].handler`
(nulls dropped); F = {h ∈ H : h starts with `squashfs_`}; L = {h ∈ F : h matches `squashfs_v1*`, `squashfs_v2*` or
`squashfs_v3*`} (the v1–v3 family: `squashfs_v1`, `squashfs_v2`, `squashfs_v2_nonstandard`, `squashfs_v3`,
`squashfs_v3_ddwrt`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`); G = set of `extraction_gaps[].kind`;
D = union of the gaps' `dependencies` (exact names); HF = handlers of the `extractor-failure` gaps (nulls dropped;
if none carries a handler, HF = F); BE = `yes` if any recorded child argv in `diagnostics[].report.command` carries
the token `-be`, `no` if argvs are recorded and none does, `n/a` if none is recorded; SR = `yes` iff a
`MaliciousSymlinkRemoved` report is in `diagnostics`; P = number of `files` (absent reads 0). Steps, first match wins:

1. OP ≠ `extract_firmware` or PR ≠ `unblob` → (`unclassified`, `none`).
2. F = ∅ and `depth-limited` ∈ G → (`container-depth-limited`, `raise-depth`) [new: a SquashFS chunk may sit inside
   a container below the depth budget; no SquashFS handler at this depth is not evidence of no SquashFS image].
3. F = ∅ → (`no-squashfs-chunk`, `inspect-input`).
4. `missing-extractor-dependency` ∈ G: D holds `sasquatch-v4be` → (`dep-missing-be`, `install-extractor-be`); else
   D holds `sasquatch` → (`dep-missing-le`, `install-extractor-le`) — every v1–v3 chunk of either byte order and
   every v4 LE chunk resolves plain `sasquatch` (confirmed on real envelopes, `w1/R42C2ReconCombo.md` §2,
   `w1/R42CritC2Draft.md` §3); a dependency gap naming neither continues at step 5.
5. `extractor-failure` ∈ G and P > 0 → (`partial-body-failure`, `salvage-partial`).
6. `extractor-failure` ∈ G, P = 0, BE = `no`, `squashfs_v4_be` ∈ HF → (`avm-marker-be-dropped`, `wrap-extractor-be`).
7. `extractor-failure` ∈ G, P = 0, HF ∩ L ≠ ∅ → (`legacy-body-failure`, `cross-read-legacy`) [new: a v1–v3 chunk
   always runs plain `sasquatch` with an explicit `-be`/`-le` (S112 `squashfs.py:40-54`), so no byte-order
   handshake or AVM pre-check applies; cross-read the chunk with a non-sasquatch reader to separate damage from
   an extractor fault].
8. `extractor-failure` ∈ G, P = 0 → (`body-extractor-failure`, `preserve-failure`).
9. `unknown-chunk-handler` ∈ G → (`unknown-residue`, `isolate-residue`) [new: bytes beside the SquashFS chunk that
   no handler claimed; REA publishes them as a `.unknown` file; re-carve the SquashFS chunk to unblob's chunk end
   and never match the residue file against a filesystem oracle].
10. `depth-limited` ∈ G → (`depth-limited`, `raise-depth`).
11. SR = yes and `unpublished-entry` ∈ G → (`mixed-symlinks`, `audit-symlinks`).
12. SR = yes and G = ∅ → (`escaping-symlink-removed`, `expect-link-absent`).
13. G = {`unpublished-entry`} → (`in-tree-symlink-metadata`, `count-gap`).
14. G = ∅: P > 0 → (`clean`, `none`); P = 0 → (`clean-empty`, `confirm-empty`).
15. anything else → (`unclassified`, `none`).

**Predicate P42-C2.** At the measured revision the frozen interpreter `tools/round-42/sqfs-triage-v4.py`, reading
only the SKILL v4 table (rule block 21, 13 columns: `handler` globs over F, `failing handler` globs over HF, gap kinds
and dependencies take the `+` contains form), gives every held-out envelope the same (label, action) pair as the
frozen evaluator `tools/round-42/indep-eval-v4.py` (written from the precedence text: seat R42C2Eval rendered the
13-step draft, the L1 amended it to the 15 A1 steps from this text alone, without opening the table, the interpreter
or the generator); the held-out set is `tools/round-42/heldout-gen-v4.py --seed <FREEZE>` (fixtures from
`corpus/evidence/round-42/c2/fixtures/`, pins `tools/round-42/fixtures.json`): 27 named classes × 2 — the round-41 v4
classes, `container-depth-limited`, `unknown-residue`, `out-of-domain`, and the legacy classes `legacy-clean`,
`legacy-dep-missing-be`, `legacy-dep-missing-le`, `legacy-body-failure`, `legacy-partial` built from unblob 26.6.4
v1–v3 fixtures — plus 24 `combo` carriers, each drawing at least two decision factors; every envelope's observed
feature tuple equals the tuple the manifest declares under the ONE key `declared_features`, read by the counter under
exactly that key (R41-CL1); carriers regenerate byte-identically; the manifest is first added after the freeze; the
v4 block bytes equal the freeze bytes; the four round-41 C1 receipts and the committed round-42 dev-arm envelopes
(`corpus/evidence/round-42/c2/dev/`) get the evaluator's pair; `combo_unseen_majority`: at least half of the held-out
combos have an observed tuple outside the union of the dev named-class declared tuples (`dev/manifest.json`).

- Target: `matched == n` (n = 78), every claim binding of `tools/round-42/c2-counter.py` true, exit 0.
- Counting command: `python3 -I -B tools/round-42/c2-counter.py --root <LANE> --rev <REV> --freeze <FREEZE> --json-out <OUT>`.
- Data procedure (after the freeze, never before): `python3 -I -B tools/round-42/heldout-gen-v4.py --seed <FREEZE> --out corpus/evidence/round-42/c2/heldout --run --scratch <scratch under /kaidoku-r42/>`.
- Kill rule: a control at full score on the 78 development envelopes stops C2 before held-out generation. Controls
  (`.ufo/waves/round-42/controls/c2/`, scored before the freeze by `tools/round-42/c2-controls.py`,
  `dev-scores-prefreeze.json`): CTL-C2-0 base SKILL 0/78 (exit 2); CTL-C2-0b the v3 table under the v4 marker 0/78
  (exit 2; the do-nothing state of the surface); CTL-C2-0c v3 rows in the 13-column grammar 51/78; CTL-C2-1
  catch-all 8/78; CTL-C2-3 actions rotated 2/78; CTL-C2-4 exact gap sets 52/78; CTL-C2-7 per-label lookup induced
  from the dev named classes 66/78; CTL-C2-7b with a majority fallback 66/78; CTL-C2-7c 59/78; CTL-C2-7x exact-tuple
  lookup 26/78; CTL-C2-8 no legacy row 75/78; CTL-C2-9 handler cells `squashfs_v4_*` 2/78; CTL-C2-10 no
  container/residue rows 67/78. None at 78: the kill rule does not fire. CTL-C2-REF (the reference rows) is the
  positive witness, not a control.
- The lookup on held-out combos (CTL-C2-7) is scored and **reported, not bound**: a lookup with real labels can only
  be built by inducing rows from evaluator-labelled data, which is the claimed work learned from the labels
  (`w1/R42C2ControlTables.md` §7.2, `w1/R42CritC2Draft.md` Q4); the bound anti-enumeration witness is
  `combo_unseen_majority` (dev arm: 22/24).
- Disclosed limits: a held-out agreement test cannot tell the table from any other table that labels the same
  envelopes the same way (`w1/R42C2Shortcuts.md` F1: 15-row tables exist); the claim measures that the SKILL table
  implements the precedence on real REA envelopes, not that the precedence is the best triage. `squashfs_v4_broadcom`
  shares the v4-BE extractor branch but step 6 names only `squashfs_v4_be`; a Broadcom BE failure lands on the body
  row (no Broadcom envelope measured, `w1/R42C2TableDraft.md` A1-F1). Legacy fixtures hold no symlinks or devices,
  so rows 11–13 are not reachable on a legacy chunk; "per handler" means the runtime handler name.

## Separability

C1 reads PROVINCE/README/SOURCES/knowledge, its receipts, carriers, oracles and reruns. C2 reads SKILL.md, its
interpreter, evaluator, generator, controls, the pinned unblob fixtures (none of them a C1 carrier) and the round-41
C1 receipts. Neither reads the other's round-42 data. The shared file is this plan.

## Frozen paths

C1: this file; `tools/round-42/{c1-counter.py,c1-extra.py,c1-run.sh,fetch-carrier.py,sqfs3-oracle.py,unblob-logtee.sh,prior-pins.json,rea-pkg.json}`;
`tools/round-27/xpin-attribute.mjs`; `.ufo/waves/round-42/c1/{carriers.json,gap-rule.json,fetch-spec.json,fetch-*.json}`;
every oracle and non-regular table carriers.json names. C2: this file; `tools/round-42/{sqfs-triage-v4.py,indep-eval-v4.py,heldout-gen-v4.py,c2-counter.py,c2-controls.py,fixtures.json}`;
`tools/round-39/gen-squashfs.py`; `corpus/evidence/round-42/c2/{fixtures,dev}/`; the SKILL v4 block; the control tables.

## Changes from the draft

- C2 precedence: amendment A1 (container-depth row, residue row, HF = failing-chunk handlers with F fallback, steps
  renumbered 1–15) after `w1/R42CritC2Draft.md` showed the 13-step draft was mostly a re-score; grammar gains the
  `failing handler` column and the dependency contains form (`w1/R42C2Grammar.md`: 0 divergence classes over a
  4,478,976-tuple sweep).
- C2 lookup binding `lookup_combo_below_half` demoted to reported (see above); the counter's binding list and two
  selftest cases were changed accordingly before the freeze (selftest 79/79).
- C1 oracle: unsquashfs 4.7.5 reads no LZMA v3 (`w1/R42C1DevRun.md`, `R42CritC1Draft.md` §3); the oracle pair is
  backhand-cli (v3_lzma) + 7z (L1 decision, `w1/R42C1Oracle.md`); 7z's listing does carry symlink modes.
- C1 carriers: published images only, carved to unblob's chunk end (`R42CritC1Draft.md` §4); D-Link candidates
  refused (no valid https, `fetch_receipt_ok` requires https); two publishers, two handlers, both byte orders.
- C1 provenance and extractor bindings after `w1/R42C1Sentinel.md` H1–H5: fetch receipts, frozen prior pins, frozen
  REA package digests, fixed PATH (with the fnm node directory: `npx` is not under `/usr/bin` on this host), and an
  unblob log tee (`tools/round-42/unblob-logtee.sh`) so `extract-env.json` can name the extract command line REA
  otherwise deletes.
- C1 counter probe repairs found by the QUALITY 84 dry run (`l1/dryrun-c1-pre.json`: 0/4 then 3/4 on the dev arm):
  squashfs-lzma 3.0 writes metadata blocks as raw LZMA1 with no props header, so the header-only compression test
  read every carrier as undetermined (now a behavioural raw-LZMA1/zlib decode); a first metadata header that reads
  the same in both byte orders (DD-WRT mini, `0x0606`) is now settled by walking the whole chain. Dev arm after the
  repairs: 4/4 carriers, only the landing-document bindings false (`l1/dryrun-c1.json`).
- C1 supplementary `c1-extra.py` is reported, not part of the target.
- C2 counter interface repairs found by the QUALITY 84 dry run: the regeneration tree did not materialise the
  committed fixture copies (`l1/dryrun-c2-pre.json`: exit 2 `generator_failed`; the counter now materialises
  `corpus/evidence/round-42/c2/fixtures`, the generator defaults `--fixtures-dir` from `KAIDOKU_FIXTURES` or that
  lane path), and `legacy_dev_envelopes` rejected the dev arm's own `no-squashfs-chunk` class (`l1/dryrun-c2-pre2.json`:
  78/78 matched, that one binding false; it now forbids the label only on an envelope holding a legacy chunk).
  Selftest 79/79 after both. Final dry run: `l1/dryrun-c2.json`.
