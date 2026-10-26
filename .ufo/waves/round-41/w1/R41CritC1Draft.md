# R41CritC1Draft — attack on the drafted R41-C1 predicate

**Verdict: DEFECTS FOUND.** The draft's own kill-rule control — the round-40 carriers/tables and
the round-40 after-receipts relabelled `V3/V4/L3/L4` — reaches **4/4, every clause true**, on a
round-41-shaped port of the counter with exact path matching and with **no REA run behind any
receipt**. A do-nothing control cannot (0/4), and a suffix-matching counter cannot *iff* the
built collision has the discriminating direction — but neither fact saves the predicate. The
named exact-match prototype also mis-scores any carrier whose squashfs chunk does not start at
offset 0 and cover the whole file (measured: oracle hits 0/6). And the 5490/5491 reservation has
a control but no committed evidence and no binding. Claim as drafted is a **re-score of round-40
ground** (prompt §6 item 9: quality, never coverage), not a Frontier → Core surface move.

Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`, base `49096c7e`. No reserved image was
downloaded or run by this seat. Everything below is a plain read of committed bytes, a lane tool,
or a sandbox clone in `/fast/scratch/hyaku/kaidoku-r41/R41CritC1Draft` (removed before yield).

## 0. Evidence I produced

Artifacts: `.ufo/waves/round-41/w1/artifacts/R41CritC1Draft/`

| file | sha256 | what |
|---|---|---|
| `attack-controls.py` | `43b917352d516cde7322b878dacc8af6f37f8c24ff66a61bf80fbff3f2c48e3e` | builds and scores both controls (sandbox clone, applies the frozen refreeze diff, patches the counter's constants to a round-41 shape) |
| `reservation-scan.py` | `699aa65bd8d0cfc9e2d0ec973c3939daa4305708161507f8aecd95ce03bf50f1` | reservation audit prototype + planted red cases |
| `relabel-score.json` | `e23507fead7e78883baea8548ca43e1325dffe7e7dab51af48d3908349fcf68f` | `carriers_matched 4`, target 4, freeze `bb2e63cbfb0c`, rev `8aa48316ef88` |
| `carve-score.json` | `87d90691c1b10bb68bf891bb1bd895796e5eb84c525cc284c2f917690ba9dae2` | `carriers_matched 3`, L4 `oracle_hits 0/6`, `gaps_ok false` |
| `relabel.out.txt`, `carve.out.txt` | — | full per-carrier clause tables |
| `reservation-scan-now.json` | — | wave-1 scan at write time: 112 reserved-name lines, 0 red |

Commands (both exit 0 = "control behaved as predicted"):

```
python3 -I attack-controls.py relabel --base 49096c7e6f226af0c750c4b003be58883cb6049f \
        --work DIR --cache CACHE --keep      # relabel_exit=0, carriers_matched 4
python3 -I attack-controls.py carve   --base 49096c7e6f226af0c750c4b003be58883cb6049f \
        --work DIR --cache CACHE --keep      # carve_exit=0,   carriers_matched 3 (L4 red)
python3 -I reservation-scan.py --selftest     # green_rows=2 red_after_plant=1 red_after_unblob=2
```

The counter used is `git show 49096c7e:tools/round-40/c1-counter.py` with the round-40 wave-2
refreeze diff applied verbatim, then only these constants changed (the port the draft names):
`CARRIERS/GAPRULE` → round-41 paths, `AFTERDIR` → `corpus/evidence/round-41/c1`,
`IDS → ('V3','V4','L3','L4')`, `PROV_SEGMENT → '/kaidoku-r41/'`. Nothing else.

## (a) Can a control that skips the work reach 4/4?

### a1 — do-nothing: **no**, 0/4
`CLAUSES` begins with `carrier_present … receipt_present`, so a freeze with carriers but no
receipts scores 0/4 (each carrier's `matched` is the conjunction of all 17 clauses). This part of
the kill rule is fine.

### a2 — round-40 receipts relabelled: **YES, 4/4** ← the predicate is dead as drafted
Construction (`attack-controls.py relabel`): the freeze commit pins the round-40 carrier bytes and
the round-40 `oracle.tsv`/`nonregular.tsv` under `V3/V4/L3/L4` (V1→V3, V2→V4, L1→L3, L2→L4); a
**post-freeze** commit copies the four round-40 `after.json` receipts, rewrites only
`parameters.output_directory` into `/kaidoku-r41/…`, and re-mints `evidence_id` with the frozen
`tools/round-27/xpin-attribute.mjs`. No REA, unblob or sasquatch run happens anywhere.

Result (`relabel-score.json`): `V3 697/697`, `V4 8/8`, `L3 7/7`, `L4 6/6` oracle hits; every
clause `true` including `receipt_fresh`, `run_provenance_ok`, `evidence_id_ok`, `projection_ok`;
`carriers_matched 4`.

Why each "freshness" clause is not one:

- `receipt_fresh` checks only `git log --diff-filter=A` of the receipt path: a *copy* added after
  the freeze passes. My control adds exactly that.
- `run_provenance_ok` checks `PROV_SEGMENT in parameters.output_directory` and no `..` — a string
  the copier writes.
- `evidence_id_ok` recomputes the id from the receipt itself (`semanticProjection`, which *does*
  include `parameters`), so a self-consistent re-mint passes. This is well-formedness, not
  provenance — exactly R40-CL2, which the draft does not repair. The round-40 counter's own
  selftest fabricates receipts with `mint_many` and expects green.
- `projection_ok` re-runs REA on the *same bytes*; a deterministic replay of a genuine run matches
  by construction. R40-CL2's finding stands: the rerun proves carrier↔oracle consistency through
  the pinned toolchain, never that the committed receipt came from a run.

Nothing in the predicate or the counter distinguishes "these bytes were scored in round 40" from
"these bytes are new". `carriers_spec` checks 4 ids, pins pairwise-distinct and hex — it has no
concept of a previously-used pin. And the draft's carrier names (5490 member, 5491 nested core)
live only in prose: the counter reads `carriers.json`, so a freeze that pins round-40 bytes under
the new ids satisfies the predicate *as written*.

⇒ Under the draft's own rule ("a control meeting the target stops C1 before any carrier run"),
**C1 must stop**, because the cheapest control meets the target.

### a3 — round-40-style suffix counter: **no, 4/4 impossible — but only in one direction**
On the round-40 data the suffix matcher scored 3/4 (L2). On L3/L4 with the *regular-path-deeper*
collision (`usr/bin/busy` regular vs `bin/busy` symlink) a suffix matcher fails
`nonregular_unpublished_ok`/`oracle_hits_ok`. The *reverse* direction (a symlink whose path ends
with a regular file's path) is green under both matchers — it cannot discriminate, and it is not
even reachable for `nonregular_published` (the candidate is always the published regular path).
The rediff's own selftest shows the asymmetry: `deep_file` → exit 0 expected (discriminator),
`shallow_file` → exit 0 under both (guard only), `wrong_gap` → the one place the reverse direction
discriminates (`gaps_ok`). So the kill rule must name **which direction** makes the mutant red;
"both directions" alone lets a builder ship the shallow one and keep a suffix-proof claim.

## (b) Is this a coverage claim, or re-scoring round-40 data?

**Re-scoring.** The prompt's rule is explicit: "Re-scoring a rule the lane already holds on new
inputs … is quality work, never coverage or depth. A coverage claim names the surface it moves
(frontier → core, a new tool, operation or edge class)."

- The round-40 stop was an **instrument** defect, not a capability miss: V1, V2, L1 (vendor and
  lane-built) matched every clause; L2 failed only `nonregular_unpublished_ok` on the suffix bug
  (`corpus/lessons/round-40.md`; R40-CL1). The wave-2 sandbox counter with exact matching scores
  the *same* receipts 4/4 (`.ufo/waves/round-40/w2/R40W2C1Refreeze.md`), and my `relabel` control
  reproduces that end to end.
- The four new carriers add no unmapped class. Measured against the round-40 oracles:
  - **V3** (5490 `./var/tmp/filesystem.image`, 30233394 B, 104 inodes) = 8 regular + 9 dirs + 85
    symlinks + 1 char-device, **including a 29.6 MB `filesystem_core.squashfs` row** — the exact
    shape round-40 **V2** already scored (8 regular, 95 non-regular, `filesystem_core.squashfs`
    25.4 MB row at `corpus/evidence/round-40/c1/V2/oracle.tsv:3`).
  - **V4** (5491 nested `filesystem_core.squashfs`, carved to 32720860 B, 6349 regular + 1017
    non-regular, 7367 staging entries) is the same class as round-40 **V1** (697 files) and **L1**
    at more scale; it crosses no budget (7367 < 10000), so it does not even touch the round-40
    note's "vendor member exceeds the 10000-entry staging budget" observation.
  - **L3/L4** are fixtures for the *counter's* path matcher; they cannot fail on the extractor.
- PROVINCE already says the surface was measured: "AVM-BE is **measured, not promoted** — the
  genuine AVM layout extracted with every oracle file on two vendor members and two lane-built
  images … Still Frontier: AVM-BE bodies (this measurement included)". Promoting a measured record
  after fixing the instrument changes the **record**, not the surface the lane governs: that is
  calibration (honest re-classification of a self-inflicted stop) plus quality (the refreeze).

Smallest true framing: type R41-C1 as **calibration** (with the counter refreeze as quality), and
let the PROVINCE row cite both rounds' receipts. If the round wants a coverage claim, it must name
one of the surfaces PROVINCE actually leaves unmoved — e.g. *recursion into* the nested core at
depth 2 (V4's 6349-file core as a depth-2 extraction), LE AVM members (`hsqs`), or AVM kernels.
None of V3/V4/L3/L4 as drafted is such a surface.

## (c) Does exact extract-root matching need special cases? **Yes — measured three ways**

I ran REA 6.5.0 `extract-firmware` on fresh trees built from the lane-built L1/L2 carriers (allowed
dev inputs; no reserved image):

1. **carved chunk** — 8192 zero bytes + L2 bytes, chunk at `[8192, 249582)`:
   receipt paths are
   `firmware.bin_extract/8192-249582.squashfs_v4_be_extract/etc/hosts`.
   The refreeze helper `extract_rel()` drops only the **first** `_extract` component, so it returns
   `8192-249582.squashfs_v4_be_extract/etc/hosts`, never `etc/hosts`. Scored against L2's oracle
   (`carve-score.json`): `oracle_hits 0/6`, `gaps_ok false`, `published_files 7` vs 6 oracle rows
   (the `0-8192.padding` file). The predicate sentence "exact path **relative to the chunk's
   extract root**" is not what the named prototype implements.
2. **two chunks** — L1‖L2, `--max-depth 1`: chunks
   `[('squashfs_v4_be',{offset:230884,length:241390}),
     ('squashfs_v4_be',{offset:0,length:230884})]` (unsorted); **two** extraction roots
   `firmware.bin_extract/{0-230884,230884-472274}.squashfs_v4_be_extract/…`; **two**
   `depth-limited` gaps with `relative_path: null`. The frozen gap rule allows
   `structural.depth-limited: 1` **per carrier**, so any carrier with two squashfs chunks fails
   `gaps_ok` for a reason unrelated to the capability. The predicate must require exactly one
   `squashfs_v4_be` chunk per carrier (today `handler_ok` is `HANDLER in handlers`).
3. **whole-file chunk (offset 0, covers the file)** — the only shape where the root is the bare
   `<staged>_extract`: the staged name is **REA's** (`firmware.bin`), never the carrier's file name
   (`carrier.sqsh` produced `firmware.bin_extract/…`). V3 and V4 are both carved to `bytes_used`
   and their oracle runs report `squashfs_offset 0`; if the freeze keeps that property the bare
   root holds — but the predicate must say so, because "carved to `bytes_used`" does not by itself
   guarantee offset 0.

Naming/prefix facts the matcher must also carry: files carry no `$output/` prefix while gaps and
derivations do (`input_path: "$output/firmware.bin_extract/…"`); `path` is absolute; REA's
`relative_path` is relative to the extraction output root; `analysis_depth` is 1 under
`--max-depth 1`; padding/sibling chunks publish regular files under the outer root. R40-CL1's
"a suffix is not a path" is right; the replacement must also be "a `_extract` component is not the
chunk root".

## (d) Is the 5490/5491 reservation enforceable and evidenced?

**Controlled, not evidenced, and now partly contradicted by the wave's own procedure.**

- The control exists: the wave context (all 41 seats) names 3490/5490/5491/7560 and L3/L4 as
  reserved; only `R41C1VendorV3` / `R41C1VendorV4` may read their image, "NO REA, NO unblob on it
  or anything carved from it". M40-2's fix ("list every candidate as reserved before recon picks
  inputs") is implemented.
- Nothing **commits evidence** of it. No seat owns an audit; the counter has no clause; the
  predicate's "none of which any REA or unblob run touched before the freeze" is unverifiable
  after the fact (per-seat scratch is deleted, and unblob writes `unblob.log` into that scratch).
  A wave that ran REA on 5490 could not be caught from the tree.
- The reservation is narrower than it reads: the V4 item explicitly allows "direct
  `sasquatch-v4be` listing/extraction of the member into scratch" — the very decoder unblob
  invokes. So "fresh" here can only mean *REA orchestration never saw these bytes*; the extractor
  did, pre-freeze, to build the oracle. State it; do not write "none of which any extractor
  touched".
- Feasible and cheap: `reservation-scan.py` classifies every wave line naming a reserved URL/sha
  as `rea` / `unblob` (red), `reader` (green only for the owning seat), or `identity-read`
  (green). Selftest: 2 green rows → green; plant an `extract-firmware` line → 1 red; plant an
  `unblob` line → 2 red. Live wave at write time: 112 lines, 0 red (8 identity reads, 104
  mentions), exit 0.

## (e) Missing bindings and kill rules (concrete)

| # | missing | why it matters (evidence) |
|---|---|---|
| e1 | **freshness/identity**: pins must differ from every previously scored carrier | relabel control = 4/4 |
| e2 | **carrier identity per id** (V3 = 5490 member carve, V4 = 5491 nested core, L3/L4 = byte-identical rebuild of the frozen builder) | the predicate delegates identity to `carriers.json`; a freeze can pin anything AVM-shaped |
| e3 | **per-chunk extract root** + exactly one `squashfs_v4_be` chunk + `bytes_used == len(carrier)` + carrier starts with `sqsh` at 0 | carve control = 0/6; two-chunk = two depth-limited gaps |
| e4 | **published regular set == oracle set** (no extras) | the padding chunk publishes `0-8192.padding` (7 vs 6); offset-0 carriers satisfy equality (697/697, 8/8, 7/7, 6/6) |
| e5 | **fetch chain as a scored clause**: `external.member_sha256` + `nested.sha256` checked, with a red selftest (member digest mismatch, carve still matching) | `tools/round-40/fetch-vendor.py` has no `member_sha256` at all (R40-CL6); the draft leaves it prose |
| e6 | **reservation audit** clause + committed artifact with a proven red case | (d) |
| e7 | **provenance honesty**: `evidence_id_ok` is well-formedness, not provenance | relabel control; R40-CL2 |
| e8 | **kill-rule construction**: the relabel control must relabel *carriers and tables too* and must score **0/4**; the suffix mutant must be red on the **direction-1** collision of **both** L3 and L4 plus the gap-path case | a receipts-only relabel fails on `subject_pin_ok` and proves nothing |
| e9 | **V4 conditional resolved**: the seat measured the nested core as AVM-BE and 7367 < 10000 entries (pin `ce27ebca…`, nested `4d5de25c…`) — freeze one carrier, drop the fallback branch from the predicate | a predicate with a runtime branch is not one sentence |

## Proposed replacement predicate (P41-C1 draft → freeze text)

> At the measured revision, for each of the four frozen carriers V3, V4, L3, L4:
> **(i) identity** — the frozen table names, per id, one carrier: V3 the carve `[0,30233394)` of
> `./var/tmp/filesystem.image` of `FRITZ.Box_5490-07.31.image` (image sha256 `770efb4e…`, member
> sha256 `87cc5d6b…`); V4 the carve `[0,32720860)` of the nested `filesystem_core.squashfs` of
> `FRITZ.Box_5491-07.31.image` (image sha256 `a5a3a763…`, member `4cfc3016…`, nested `4d5de25c…`);
> L3/L4 the byte-identical rebuild of the frozen `mk-l-carriers.py` at the freeze, each holding a
> regular file whose path ends with a symlink's path **and** a symlink whose path ends with a
> regular file's path. **(ii) freshness** — no carrier pin equals the sha256 of any carrier, oracle,
> receipt subject or evidence envelope committed anywhere in the lane at or before the freeze, nor
> any pin listed in the frozen `prior_pins`, and the four pins are pairwise distinct. **(iii) bytes**
> — the carrier begins with the 96-byte `sqsh` v4.0 superblock at offset 0, carries the AVM marker,
> `bytes_used == len(carrier)`, its first metadata block length is little-endian exact, and it holds
> exactly one `squashfs_v4_be` chunk. **(iv) extraction** — the after-receipt
> (`extract-firmware --max-depth 1`, REA 6.5.0, unblob 26.6.4, sasquatch-v4be 4.5.1 on the child
> PATH) names that chunk with no failed chunk; **the published regular files under that chunk's own
> extract root — `<staged>_extract/` when the chunk covers `[0,len)` and
> `<staged>_extract/<start>-<end>.squashfs_v4_be_extract/` otherwise, derived from
> `normalized_result.chunks[].range` and never from the carrier's file name — equal the frozen
> oracle set exactly (same paths, same sha256, no extras)**; no non-regular entry is published at
> its exact path; gaps are only those the frozen gap rule allows. **(v) receipt** — first added in
> a commit after the freeze, `parameters.output_directory` inside `/kaidoku-r41/`, evidence id
> recomputes (well-formedness only; provenance is not claimed, R40-CL2); a counter-time rerun of
> the same bytes has the same `plus-extractor` projection; for vendor carriers the committed fetch
> record proves image sha256 → member sha256 → nested sha256 → carve length → carrier pin with the
> frozen `fetch-vendor.py`, whose selftest turns red on a member digest mismatch that still carves
> to the pin. **(vi) record** — PROVINCE.md holds `## Round-41 additions to Core` naming the layout
> and citing the round-41 entry, which cites a SOURCES row absent at the base; a `Round-41 frontier
> note` names the heading and entry stem, says it supersedes the round-40 measured-not-promoted
> record **and nothing else**, and the reservation audit (`w1/artifacts/R41C1Reservation/audit.json`,
> green) is committed.

Kill rules to add at the freeze (each scored with the frozen counter, receipt committed):

- **CTL-C1-0** do-nothing → 0/4 (as drafted).
- **CTL-C1-relabel** round-40 carriers + tables under the new ids, receipts copied post-freeze,
  `output_directory` rewritten, ids re-minted → must be **0/4** because `carrier_fresh_ok` is false.
  (Measured: 4/4 under the draft.)
- **CTL-C1-carve** the 8192-offset fixture → 0/4 under a matcher that keeps the chunk root (proves
  the extract-root derivation).
- **CTL-C1-suffix** the round-40 matcher → red on the direction-1 collision of L3 **and** L4 and on
  the gap-path case; direction-2 is a false-positive guard only.

## Impacted axes

- **coverage** — not moved by the claim as drafted (V3 duplicates round-40 V2's shape; V4 is the
  same class at more scale; L3/L4 score the counter).
- **calibration** — harmed if `FRESH` / "none touched" / "recomputes to its evidence id" stand as
  provenance claims: the relabel control and the R40-CL2 finding both falsify them.
- **depth** — the gap-rule and extract-root text assume one whole-file chunk; two-chunk carriers
  produce two `depth-limited` gaps against an allowance of 1.

## Smallest safe correction (L1, before the freeze)

1. Add `carrier_fresh_ok` (freeze-state scan + `prior_pins`) and `carrier_identity_ok` to
   `CLAUSES`; commit the CTL-C1-relabel receipt at 0/4.
2. Replace `extract_rel()` with a per-chunk root derived from `chunks[].range`; add
   `single_squashfs_chunk_ok`, `bytes_used == len`, `oracle_set_equal_ok`; selftests for the
   offset-8192 carrier, the two-chunk carrier and the padding file.
3. Re-type R41-C1 as calibration (counter refreeze = quality), or name a genuinely unmoved surface
   (depth-2 recursion into the nested core; LE AVM; kernels). Do not claim coverage for V3/V4/L3/L4
   as drafted.
4. Make the fetch chain (`member_sha256`, `nested.sha256`) a scored clause with a red selftest
   (R40-CL6), and commit the reservation audit (prototype here; selftest red on a planted REA or
   unblob line).
5. Freeze V4 as the nested core (seat-measured: AVM-BE, 7367 < 10000 entries); delete the fallback
   branch and the "fresh" wording that implies no extractor saw the bytes.

## Open items / inference

- `[INFERENCE]` the round-41 port keeps `PROV_SEGMENT` semantics but sets it to `/kaidoku-r41/`
  (`R41C1Run` item says so); my control rewrote the directory accordingly.
- `[INFERENCE]` the L3/L4 builder will place the *regular-path-deeper* collision, not only the
  shallow direction; the draft's "both directions" does not say which one the mutant is proven on.
- `[INFERENCE]` 3490 and 7560 image sha256 are not available in this lane; the reservation scan
  matches those two by URL prefix only (7560's exact file name unverified).
- V4's expected published set at depth 1 is 6349 regular files and 615 symlink gaps (seat
  artifacts), not yet measured under REA.
