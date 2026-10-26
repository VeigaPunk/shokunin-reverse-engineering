# R41W2C1Fabricate — C1 landing attack: can fabrications reach 4/4 without a genuine REA run?

VERDICT: DEFECTS FOUND — the R41-C1 MET landing holds numerically (no tested fabrication reaches `met_target`),
but the claimed defense against oracle-fabricated receipts (R39-CL5 routing: "a receipt fabricated from the
oracle … cannot equal a real run") is FALSE for 3 of the 4 carriers. The frozen counter's rerun projection
accepted pure oracle-table fabrications of V3, L3 and L4 unchanged score 4/4; only V4's extractor-determined
removal set refused oracle-only fabrication. All semantic receipt edits (drop gap / add published file / move a
removal) were refused by `projection_ok` alone, with every other clause still true.

## What I attacked

Seat R41W2C1Fabricate (leaf). Target: the R41-C1 verdict (MET) — predicate P41-C1 at revision
e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 (freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f).
Hypothesis to test: a forger who holds the frozen oracle tables (`oracle.tsv`, `nonregular.tsv`) and
`carriers.json` pins can fabricate `after.json` receipts for V3/V4/L3/L4 that pass every counted clause —
including the counter-time REA rerun projection — without ever running REA. This is the R40-CL2 class
("the counter cannot prove which process wrote the committed receipt") re-tested against the round-41
`plus-extractor` projection.

## Method (sandbox, no VCS mutation of the lane)

- Scratch `S=/fast/scratch/hyaku/kaidoku-r41/R41W2C1Fabricate`; sandbox clone
  `D=/fast/scratch/hyaku/kaidoku-r41/R41W2C1Fabricate/fx.KdIh/lane` at e9a24d07
  (`git clone -q --shared <lane> $D/lane`; `rev-parse --show-toplevel` asserts `$D/lane`; every git call
  names `-C`; commits only inside the clone with `-c user.name=fx -c user.email=fx@fx`; no lane/fleet
  mutation, no `git add` on the lane).
- Vendor bytes: copied the already-materialised cache `/fast/scratch/hyaku/kaidoku-r41/cache/{c4f74f54…,
  ce27ebca…}.bin` into `$S/cache` (pins verified by sha256; AVM bytes never copied into artifacts).
- Frozen counter run verbatim (`tools/round-41/c1-counter.py` at e9a24d07, `--root $D/lane`,
  `--freeze d764389e…`, `--pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`,
  `--carrier-cache $S/cache`).
- Fabricated receipts were committed as new commits in the sandbox (round-41 receipt paths), then scored with
  the same frozen counter, which performs the genuine REA 6.5.0 rerun at scoring time (env
  `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob`, TMPDIR inside scratch; replay of `parameters.max_depth`).
- Evidence IDs: minted under the frozen rule with the lane's `tools/round-27/xpin-attribute.mjs
  --pkg65 <rea6.5.0> --pkg67 <rea6.5.0>` on `{'data': <envelope>}`; every fabricated receipt carries a
  freshly minted id and passes `evidence_id_ok` (checked by the counter).

Toolchain: python3 3.14.8, node v24.21.0, npx 11.19.0, git 2.56.0, unblob 26.6.4 (symlink in
~/.local/bin), sasquatch-v4be 4.5.1, jq 1.7.1. No installs performed (nothing missing); pacman untouched.

## Scenarios and results (all scored by the frozen counter at e9a24d07 tooling)

| # | fabrication | sandbox rev | carriers_matched | met_target | exit |
|---|-------------|-------------|------------------|------------|------|
| S0 | genuine receipts (baseline, no fab) | e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 | 4 | true | 0 |
| S1 | oracle-only fabrication, all four carriers | 13101bdbe95a843f89b832ffdb5ae6b7858aa82b | 3 | false | 1 |
| S2 | round-40 receipts relabeled to round-41 receipt paths (CTL-C1-1 replication) | cb0c76e8f3e1df6c5bca5265130680a118307b4d | 0 | false | 1 |
| S34 | edits of genuine receipts: L3 drop gap + add published file; V4 move a removal to another path | eda0d948a4f24436a5996292e31ff3211e718a7e | 0 | false | 1 |

Wall time each run ≈ 23–27 s (4 carriers × genuine rerun). Score receipts:
`artifacts/R41W2C1Fabricate/s{0,1,2,34}.json`.

### S1 — oracle-only fabrication (from the frozen tables alone, no REA run)

Receipts were constructed solely from `oracle.tsv` (rel, sha256, size), `nonregular.tsv` (rel, kind, detail),
`carriers.json` (pins, lengths), and the REA 6.5.0 envelope conventions visible in the round's own data
procedure. Per carrier: `files` = exactly the oracle rows (paths under `firmware.bin_extract/`, mime null,
no HashReport rows — identical to real receipts), chunks/derivations/selection standard, engine unblob
26.6.4, coverage "partial", `published_bytes` = Σ(regular-file sizes) from the oracle, a structural
`depth-limited` gap, and every symlink row disposed either as an `unpublished-entry` gap+entry or as a
`MaliciousSymlinkRemoved` diagnostic. Nothing was taken from the genuine after.json files; no extraction was
run. V4 variant b removed the first four absolute-target symlinks in table order (the closest oracle-only
guess: real V4 also has exactly 4 removals, all absolute-target).

Counter result (S1):

| carrier | matched | failing clauses |
|---------|---------|-----------------|
| V3 | **true** | none (all 19 clauses incl. `projection_ok`) |
| L3 | **true** | none (incl. `projection_ok`) |
| L4 | **true** | none (incl. `projection_ok`) |
| V4 | false | only `projection_ok` |

V4 `projection_ok` diff: `extraction_gaps` [612,612], `unpublished_entries` [611,611], `diagnostics`
[4,4] — counts identical, members differ (committed fabrications guessed removal set ≠ real removal set
`lib/libbroadbandcfg.so`, `lib/libbroadbandcfg.so.1`, `usr/www/avm/cgi-bin/system_status`,
`usr/www/avme/cgi-bin/system_status`).

That is: for V3/L3/L4 the oracle-only fabrication is **indistinguishable** from a genuine REA run under the
entire counted predicate, including the fresh rerun. The proof is the counter's own result: those three
carriers are `matched: true`, and the local projection comparison of fab vs genuine receipt shows zero
differing keys (projection equality). For completeness, the "all-gapped" V4 oracle-only variant (a) differs
from the genuine receipt by counts 616/615/0 vs 612/611/4.

### S2 — relabel round-40 receipts (CTL-C1-1 replication)

Copied `corpus/evidence/round-40/c1/{V1,V2,L1,L2}/after.json` to the round-41 receipt paths. Counter: 0/4.
Failing clauses per carrier: `subject_pin_ok` (round-40 subject digests ≠ round-41 pins),
`oracle_hits_ok` (round-40 published sets don't cover round-41 oracles), `gaps_ok` (round-40
gap/disposition layout doesn't fit round-41 non-regular tables), `run_provenance_ok` (round-40 output dirs
carry `/kaidoku-r40/`, not `/kaidoku-r41/`), `projection_ok`. `evidence_id_ok` stays true (unchanged
envelope), confirming the evidence-id check alone does not stop relabeling.

### S34 — edits of genuine receipts

- L3 "drop a gap + add a published file": removed the `bin/busy` gap and unpublished entry (leaves a
  required symlink with no disposition → `gaps_ok` false) and appended a fake published regular file
  `usr/bin/fake` (sha256 `aa…aa`, size 123; `oracle_hits_ok` unaffected because it is only one-directional).
  Counter: L3 not matched; failures `gaps_ok` + `projection_ok` (`files` 14 vs 13, `extraction_gaps` 3 vs
  4, `unpublished_entries` 2 vs 3, `published_bytes`).
- V4 "move a removal to another path": swapped disposition between two symlinks (removal moved from
  `lib/libbroadbandcfg.so` to `bin/ash`; `bin/ash`'s gap/entry moved to `lib/libbroadbandcfg.so`) keeping
  every count identical (612 gaps / 611 unpublished / 4 diagnostics). Counter: V4 matched false **with all
  18 non-projection clauses true** — `gaps_ok`, `oracle_hits_ok` (6349/6349), `evidence_id_ok`,
  `run_provenance_ok`, etc. The only failing clause is `projection_ok` (diff keys `extraction_gaps`,
  `unpublished_entries`, `diagnostics`, equal counts).

## What this means for the landing

1. `met_target` is NOT reachable by any tested fabrication: the four counter runs all exit 1, and the
   only carrier that refuses the oracle-only class (V4) has a removal set that is extractor-determined
   (unblob's directory-iteration order, per `plans/round-41-claims.md` "Disclosed limits") and hence not
   precomputable from the frozen tables. The numeric verdict MET stands.
2. But the claim's defense is narrower than stated. The claim (and counter docstring) asserts that
   `plus-extractor` is not oracle-closed: it "adds the extractor-determined fields (derivations, engine,
   published_bytes, coverage)". Empirically all four of those fields are oracle-reconstructible for these
   carriers: derivations are fixed by REA staging (`$input` → `$output/firmware.bin_extract`), engine
   name/version is the pinned toolchain, `published_bytes` ≡ Σ(regular-file sizes in the oracle) (verified
   for all four carriers: V3 31227104, V4 110187475, L3 194049, L4 174930), and coverage "partial" follows
   from the replayed `--max-depth 1` gap. The only genuinely extractor-determined datum in the whole
   projection is V4's *which*-symlinks-removed set. Consequently the rerun projection refused the oracle-only
   fabrication on 1 of 4 carriers, not 4 of 4; R40-CL2 is wide open on V3/L3/L4.
3. The "move a removal" edit shows a semantic change that defeats every local clause and is caught only by
   the projection — the rerun clause is doing the work the claim assigns it, but only when the carrier's
   extraction leaves non-oracle traces.
4. Collateral observation (not a falsifier): V4's `run.json` is absent from `corpus/evidence/round-41/c1/V4/`
   (`run-harness-failure.log`: `c1-run.sh: line 547: jq: Argument list too long`); commit 5ca6941b's message
   records this ("V4 run.json not written: c1-run.sh jq ARG_MAX on a 615-link summary, log kept"). Neither
   counter reads `run.json`, so the scored predicate is unaffected; the harness bookkeeping for V4 is
   incomplete, and the harness's own sampling of `gaps_detail`/`unpublished_entries` blew the ARG_MAX bound
   (615-link summary).

## Smallest safe correction (fixable defect)

The counter's refusal power rests entirely on carriers whose extraction leaves extractor-determined traces.
To make the R39-CL5 routing true for all four carriers, freeze a per-carrier binding that is not oracle-derivable
(as examples): (a) extend the projection to an extractor-determined set the oracle cannot fix — e.g. the
exact multiset of removal diagnostics plus the *unblob* output digest or `worker_count`/`k`-dependent
ordering, or (b) add a per-carrier "oracle-closed" disclosure: the claim should state that V3/L3/L4 are
oracle-closable and only V4's removal set is non-derivable, or (c) choose lane-built carriers that
deliberately exercise the removal path (escaping symlinks) so the oracle cannot precompute the disposition,
matching what V4 already does. Without one of these, the claim's routing text ("a receipt fabricated from
the oracle … cannot equal a real run") overstates what the counter enforces.

## Evidence and artifacts

- Score receipts (frozen counter output): `artifacts/R41W2C1Fabricate/s0.json` (baseline, exit 0),
  `s1.json` (oracle-only, exit 1, matched 3), `s2.json` (relabel, exit 1, matched 0), `s34.json` (edits,
  exit 1, matched 0); per-carrier clause detail inside each.
- `artifacts/R41W2C1Fabricate/overview.json`: machine-readable per-scenario × per-carrier clause matrix.
- Fabricated receipts: `s1-fab-{V3,V4,L3,L4}-after.json`, `s3-fab-L3-after.json`, `s4-fab-V4-after.json`;
  genuine receipts for comparison `real-{V3,V4,L3,L4}.json` (from e9a24d07).
- Generator: `artifacts/R41W2C1Fabricate/fab.py` (builds each fabrication, mints evidence ids via xpin,
  prints local projection comparison vs the genuine receipts).
- Evidence commands (exact):
  - baseline: `python3 -I -B tools/round-41/c1-counter.py --root $D/lane --rev e9a24d07256d1606f01aa4d2d65f74e649c5f3d4 --freeze d764389e9cbe61b9d1b07538ff3bff02d50bb34f --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents --carrier-cache $S/cache --json-out $S/scores/s0.json` → `exit 0`.
  - S1/S2/S34: same command with `--rev 13101bdbe95a843f89b832ffdb5ae6b7858aa82b` / `cb0c76e8f3e1df6c5bca5265130680a118307b4d` / `eda0d948a4f24436a5996292e31ff3211e718a7e` → `exit 1` each.
- sha256 of artifacts as listed in the artifacts dir (fab.py, overview.json, real-*.json, s*.json, fab after.json files) — all ≤ 3.4 MB, no vendor bytes anywhere.

No lane files were modified by this seat; all fabrication commits live only in the sandbox clone
(`$D/lane`), which is removed with scratch on exit.
