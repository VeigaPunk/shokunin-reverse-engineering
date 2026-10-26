# R40W2C1Fabricate — R39-CL5 attack on the R40-C1 rerun binding

**Verdict: DEFECTS FOUND.** A receipt fabricated from the frozen oracle/non-regular tables alone —
no REA run on the carrier, not even a sasquatch extraction — passes all 17 clauses of P40-C1 for L1
(`matched: true`), and fabricating V1, V2 and L1 reproduces the genuine lane's score exactly
(`carriers_matched: 3`, exit 1). The rerun clause therefore proves *carrier → oracle consistency
through the pinned toolchain*, not receipt provenance; the claim says so in prose, but its
executable control for that limit is vacuous. Separately, R40-C1 is **unsatisfiable at any revision**
with the frozen carrier set: L2's `nonregular_unpublished_ok` can never be true (proof in Defect B),
so the landing's "honest stop" is a permanent design blocker, not an empirical miss.

## What I attacked

The R40-C1 receipt clause: `projection_ok` ("the counter's own REA run of the REV carrier bytes has
the same `plus-extractor` projection as the committed receipt"), together with the other receipt-derived
clauses (`subject_pin_ok`, `operation_ok`, `handler_ok`, `chunks_ok`, `oracle_hits_ok`, `gaps_ok`,
`nonregular_unpublished_ok`, `run_provenance_ok`, `evidence_id_ok`, `receipt_fresh`). My seat asked:
build the strongest possible fabricated receipts for L1 (and a vendor carrier) without running REA on
that carrier; see which projection fields refuse each fabrication; decide whether a forger who extracts
with sasquatch reaches a projection-equal receipt; and state precisely what the binding does and does
not prove. No REA invocation was used to *construct* any receipt. The only REA runs in this seat are the
counter's own scoring reruns (that is the binding under test).

## Method and inputs

All work in a sandbox (`git clone --shared` of the lane into
`/fast/scratch/hyaku/kaidoku-r40/R40W2C1Fabricate`, `rev-parse --show-toplevel` verified, detached at
`42c10a58`, fixtures committed with `-c user.name=fx -c user.email=fx@fx`). Freeze
`7fce3086`, REV = a post-freeze sandbox commit. No VCS mutation in the lane.

Fabrication inputs per carrier — all of them already committed in the lane before the freeze:

| input | supplies |
|---|---|
| `.ufo/waves/round-40/c1/carriers.json` | pin (`subject_sha256`), carrier length |
| `corpus/evidence/round-40/c1/<id>/oracle.tsv` | `files` (rel, sha256, size), `published_bytes` |
| `corpus/evidence/round-40/c1/<id>/nonregular.tsv` | `extraction_gaps` (one per symlink), `unpublished_entries` |
| **one** committed `after.json` of a *different* carrier | the constants: `coverage='partial'`, the single derivation edge, the chunk tuple shape, `engine=['unblob','26.6.4']`, `max_depth=1`, file-record shape |
| `tools/round-27/xpin-attribute.mjs` | re-minted `evidence_id` (a pure function of the envelope) |

The fabricator is `artifacts/R40W2C1Fabricate/fab.py`. V1 and V2 envelopes were generated **before** the
vendor cache existed (no carrier bytes on disk, no sasquatch run); L1's envelope was generated from L2's
receipt + L1's two tables, and I did not read L1's own receipt or `run.json` to build it.

## Result 1 — the fabricated L1 receipt is accepted end to end

`score-fab-L1.json` (frozen counter, real REA 6.5.0 + unblob 26.6.4 + sasquatch-v4be 4.5.1 rerun on L1):

```
exit_code 1   carriers_matched 1   L1.matched true   projection_ok true   projection_diff []
failing clauses: []
receipt_first_add 73c7bf9c73bd7b4891c4e46c93d1d29c287e4541   receipt_fresh true
run_provenance_ok true   output_directory /fast/scratch/hyaku/kaidoku-r40/fab/extract
evidence_id_ok true      subject_pin_ok true          oracle_hits 7/7
```

17/17 clauses for a receipt no extractor ever produced. Two clauses are worth naming:

- `run_provenance_ok` (`c1-counter.py:596-604`) is an absolute-path test plus the substring
  `/kaidoku-r40/`; any string satisfies it. It carries no run evidence.
- `receipt_fresh` (`c1-counter.py:707-713`) reports the *first add* of the path. The scored bytes were
  committed later, in the sandbox's new commit; the clause still reports `73c7bf9c`, the original add.
  So "first added after the freeze" is a property of the path, not of the bytes: an edit after the add
  inherits freshness.

## Result 2 — the whole fabricated set scores identically to the genuine lane

`score-fab-all.json` (V1, V2, L1 receipts replaced by fabrications; L2's genuine receipt untouched;
vendor cache built with `fetch-vendor.py`, exit 0):

```
exit_code 1   carriers_matched 3   met_target false
V1 matched true  projection_ok true  projection_diff []   697 files, 264 gaps
V2 matched true  projection_ok true  projection_diff []     8 files,  86 gaps
L1 matched true  projection_ok true  projection_diff []     7 files,   3 gaps
L2 matched false failing ['nonregular_unpublished_ok']     6 files,   3 gaps
```

The genuine reading at `42c10a58` is `carriers_matched: 3`, exit 1, L2 failing exactly
`nonregular_unpublished_ok`. **The score is identical.** Receipt authenticity contributes nothing to
P40-C1's outcome.

`projection-equality.out` shows why, using the frozen module's own `projection()`/`projection_diff()`
at profile `plus-extractor`: for L1, V1, V2 **and** L2 (as a positive control, templated from V1's
receipt instead of L2's) all ten projection keys are equal to the real committed receipts' projections
(`differing keys=[]`).

## Which projection fields refuse each fabrication

`matrix.out` (frozen `projection()` against the real L1 projection) plus one real counter run per case
(`clauserun.out`):

| mutation of the fabricated L1 receipt | refused by | clause |
|---|---|---|
| gaps/unpublished omitted (tables-only forger who forgets the gap rule) | `extraction_gaps`, `unpublished_entries` | `gaps_ok` + `projection_ok` |
| one extra gap on a directory | `extraction_gaps` | `gaps_ok` |
| `unpublished_entries` dropped, gaps kept | `unpublished_entries` | `projection_ok` |
| chunk length block-aligned (231424 instead of 230884) | `chunks` | `projection_ok` |
| `coverage='complete'` | `coverage` | `projection_ok` |
| `engine=[unblob,6.4.9]` | `engine` | `projection_ok` |
| derivation child `$output/carrier.bin_extract` | `derivations` | `projection_ok` |
| `published_bytes` = compressed carrier size | `published_bytes` | `projection_ok` |
| one file size off by one | `files` | `projection_ok` |
| **per-file HashReport with the true sasquatch md5/sha1** | `files` | `projection_ok` |
| **truthful `mime_type` on each file** | `files` | `projection_ok` |
| one diagnostic attached | `diagnostics` | `projection_ok` |
| `handler='squashfs_v4_le'` | `chunks` | `handler_ok` |
| **`raw_result.execution` replaced with `/usr/bin/true --never-ran-unblob`, `limitations=['no extractor was executed']`, `authority='derived-from-oracle'`** | — | **accepted, `matched: true`** |
| **`provider={name:'Not Unblob At All', version:'6.4.9'}`, foreign `subject.name`, invented `evidence_links`, invented `analysis_profile`** | — | **accepted, `matched: true`** |
| unminted `evidence_id` | `evidence_id_ok` | `evidence_id_ok` |

Two of these are inverted. First, `plus-mime` and `plus-content` are inert: a genuine REA receipt carries
exactly one `HashReport`, on the staged carrier `firmware.bin` (`raw_result.report[1]`), never per
published file; every `files[].mime_type` is `null` in all four real receipts. The projection therefore
compares `[suffix, sha256, size, None, None, None]` per file and **rejects a forger who writes the true
mime type or the true md5/sha1** — the only accepted value is `null`. Second, everything the receipt
carries outside the projection (`raw_result.execution` — the extractor argv/stdout the claim itself says
REA does not record on success —, `limitations`, `authority`, `provider.name/version`, `subject.name`,
`parameters.path`) is unchecked; `operation_ok` looks only at `operation` and `provider.id`.

## Does a forger who extracts with sasquatch reach a projection-equal receipt?

Yes — and extraction is not needed. All ten compared keys are derivable from frozen data:

| projection key | source |
|---|---|
| `subject_sha256` | `carriers.json` pin |
| `files` | `oracle.tsv` (rel, sha256, size); mime/md5/sha1 are `null` by convention |
| `chunks` | `['squashfs_v4_be', 0, carrier_length, false]` |
| `extraction_gaps` | one `depth-limited` + one `unpublished-entry` per symlink in `nonregular.tsv` |
| `unpublished_entries` | the symlinks in `nonregular.tsv` |
| `published_bytes` | Σ `oracle.tsv` sizes |
| `diagnostics` | `[]` (constant) |
| `derivations` | one fixed `$input → $output/firmware.bin_extract` edge |
| `engine` | `['unblob','26.6.4']` (constant) |
| `coverage` | `'partial'` (constant while one structural gap exists) |

The gap formula is exact on all four carriers: 263/85/2/2 symlinks → 263/85/2/2 `unpublished-entry`
gaps, plus 1 `depth-limited` each. `published_bytes` equals the oracle size sum on all four
(238530 / 21681493 / 27008292 / 244251). So the projection is a re-expression of (oracle, nonregular,
pin, length) plus four constants; there is no extractor-determined field in it. A sasquatch extraction
adds nothing a forger can use: my per-file md5/sha1 variant is *rejected*, because unblob emits none.

## What the binding proves

Given a trusted rerun environment and the frozen tables:

1. The bytes at REV hash to the frozen pin and carry the AVM structural signature (`layout_probe` runs on
   the bytes, not the receipt).
2. At scoring time REA 6.5.0 + unblob 26.6.4 + sasquatch-v4be 4.5.1 at `max_depth` replayed from the
   receipt emit exactly one `squashfs_v4_be` chunk with no failure, publish exactly the frozen oracle's
   file set (suffix + sha256 + size), and emit only gap kinds the frozen rule allows.
3. The committed envelope is a *consistent transcription* of that result, and its evidence id is
   consistent with its own bytes.

That is genuine, oracle-independent coverage evidence: the oracle was frozen before any REA run and the
rerun is a different toolchain. It is also the entire content of the claim — the receipt adds nothing.

## What it does not prove

1. That REA ever ran on the carrier, or which process wrote the receipt. A receipt built from
   `oracle.tsv` + `nonregular.tsv` + one other carrier's receipt is accepted (Results 1 and 2).
2. Anything in the receipt outside the projection: the `raw_result` execution log/argv/stdout,
   `limitations`, `authority`, `confidence`, `provider.name`/`version`, `subject.name`,
   `parameters.path`, `analysis_profile`, `evidence_links`. Both fiction runs are `matched: true`.
3. That the receipt's current bytes are the bytes that were first added — `receipt_fresh` follows the
   path's first add.
4. That `mime_type`/`md5`/`sha1` are right: the only accepted values are `null`.
5. That `evidence_id` is anything more than a checksum of the envelope (an unminted id fails; a minted
   id for fabricated bytes passes).
6. `run_provenance_ok` proves a string was written in the right shape, nothing else.

## Defect A — the claim's executable control for this limit is vacuous

`plans/round-40-claims.md:80-81` cites, among the 65 red self-test cases, "a re-minted fabrication
refused by the rerun projection". The case is `c1-counter.py:1690-1693`:
`oracle_only = fabricate('V1', diags=[], chunk_handler='squashfs_v4_le')`, and `fabricate`
(`:1672-1682`) starts from `spec_data[k]` — the fixture's *modelled run* (files, gaps, unpublished,
published_bytes, derivations, coverage) — and only drops diagnostics and changes the handler. The
fixture's oracle is `rel\tsha\tsize` only. So the named "oracle-only" case is a two-field mutation of
true data; it never exercises oracle-derivability. Its rejection is true by construction because
`sim_runner` returns `rehost(green_envs[cid])`. The suite is green (I ran it: `cases: 70, green_ok: 5,
red_ok: 65, failures: []`), but it carries no evidence for the R39-CL5 threat model. The prose limit at
`plans/round-40-claims.md:85-87` is accurate; the control cited next to it is not the evidence it is
presented as.

## Defect B — R40-C1 is unsatisfiable, not merely unmet (counterexample)

`same_rel` (`c1-counter.py:606-608`) is a *path suffix* test. `nonregular_published` (`:643-649`)
applies it to published paths against every non-regular entry. L2's oracle contains the regular file
`usr/bin/busy`; L2's non-regular table contains the symlink `bin/busy`.

- `oracle_hits_ok` requires a published path `p` with `same_rel(p,'usr/bin/busy')` → `p` ends
  `.../usr/bin/busy`.
- `nonregular_published` then tests `same_rel(p,'bin/busy')` → `p.endswith('/bin/busy')`, which is
  implied: any string ending `/usr/bin/busy` ends `/bin/busy`.
- Therefore `nonregular_unpublished_ok` is false for *every* receipt that satisfies `oracle_hits_ok`,
  and true only for receipts that fail `oracle_hits_ok`. Checked in code on the committed tables
  (`bin/busy` vs `usr/bin/busy`, and on `firmware.bin_extract/usr/bin/busy` and bare `usr/bin/busy`):
  all three candidates collide.

L2 is the only carrier with a collision (V1: 697 files/263 symlinks → 0; V2: 8/85 → 0; L1: 7/2 → 0;
L2: 6/2 → 1). So `carriers_matched == 4` is unreachable at every revision that keeps the frozen
`carriers.json`, `nonregular.tsv` and `c1-counter.py` — no genuine extraction, no counter fix within the
round, and no fabricated receipt can change it. The landing's phrasing ("a path-suffix false positive",
"an honest stop") is correct about the mechanism but presents an unsatisfiable target as an empirical
miss; the frozen tables already contained the contradiction at the freeze, and it is derivable from
`oracle.tsv` + `nonregular.tsv` alone — a format control would have caught it before any data existed.

## Smallest safe correction

1. **Predicate (round 41 freeze, cannot be fixed inside round 40):** in `nonregular_published`, compare
   extraction-relative paths by equality instead of suffix: `rel_suffix(fp) == rel`. `rel_suffix`
   already strips the `<name>_extract/` prefix that motivated suffix matching, and the equality holds on
   all four real receipts (their published paths project to exactly the oracle rels — proven by
   `projection-equality.out`). That removes the cross-entry collision without weakening vendor support.
   Add a freeze-time control: no oracle row may satisfy `same_rel` against another non-regular row.
2. **Honesty of the receipt clause:** rename/redocument `projection_ok` as a transcription check and
   replace the vacuous selftest case with a *positive* control that builds a receipt from the fixture's
   oracle + non-regular tables + one template receipt and asserts the counter accepts it — so the
   executable control states the actual limit instead of a two-field mutation. If resistance is wanted,
   note that no field of the receipt is extractor-determined today (see the derivation table), so a
   genuinely unforgeable field would have to come from the unblob execution log, which the claim says is
   not recorded on success.
3. **Cheap hardening, no semantics change:** compare `provider.version`, `subject.name` and the
   `parameters` triple against the frozen spec, and require `output_directory` to equal a per-carrier
   path inside the run's scratch rather than to contain `/kaidoku-r40/`.

## Impacted axes

Coverage (R40-C1): unchanged at 10 — the landing's NOT MET stands, and the demotion to a
measured-not-promoted record is correct. Calibration: the round's presentation overstates what the
rerun binding resists and understates why C1 could not land; the claim text itself (disclosed limits,
honest-stop rule) is accurate. Depth (R40-C2) untouched by this seat.

## Limits and inference

- The reference for clause attribution is the real committed L1 projection; I measured (Result 1)
  that a fabricated projection equals the *fresh rerun* projection, so using the committed one as the
  reference for the mutant matrix is measured, not assumed.
- `coverage` for a gap-free carrier is unobserved: every carrier here is depth-limited. A forger facing
  a gap-free carrier would need one receipt of a gap-free run for the constant `[INFERENCE]`.
- The sandbox clones the lane and adds commits; lane history, freeze and frozen paths are untouched
  (`frozen_path_changed: []` in every score).
- A receipt stored with the `{"data": …}` wrapper instead of the bare envelope makes the counter exit 2
  (`xpin: cannot digest projection … reading 'digest'`) — unevaluable, never met; noted only because it
  cost me one iteration.
- No old evidence was retired by this seat; nothing outside my artifacts dir and this report was written.

## Reproduction

```
S=/fast/scratch/hyaku/kaidoku-r40/R40W2C1Fabricate
python3 tools/round-40/fetch-vendor.py --root <LANE> --rev 7fce3086… --cache "$S/cache"
python3 artifacts/…/fab.py <other-carrier after.json> L1 2521ded6… 230884 \
        corpus/evidence/round-40/c1/L1/oracle.tsv corpus/evidence/round-40/c1/L1/nonregular.tsv \
        carrier.sqsh > fab/L1.json          # then set data.evidence_id from
node tools/round-27/xpin-attribute.mjs --pkg65 <rea-agents> --pkg67 <rea-agents> fab/L1.json
# bare `data` object into corpus/evidence/round-40/c1/L1/after.json of a sandbox clone, commit,
python3 -I -B tools/round-40/c1-counter.py --root $D/lane --rev <fab commit> \
        --freeze 7fce308631a8b457d6b7c5a4b39a923c4e9a49de --pkg65 <rea-agents> \
        --carrier-cache "$S/cache" --json-out score.json
```

Artifacts: `.ufo/waves/round-40/w2/artifacts/R40W2C1Fabricate/` (`fab.py`, `fab/*.env.json`, `cmp.py`,
`matrix.py`, `matrix.out`, `clauserun.py`, `clauserun.out`, `projection-equality.out`,
`score-fab-L1.json`, `score-fab-all.json`, `score-*.json`, `fetch-vendor.log`, `README.txt`).

## Tooling record

Nothing installed or upgraded (no pacman, uv, npx-cache or `~/.local/bin` change). Used the existing
REA 6.5.0 npx cache, unblob 26.6.4, sasquatch-v4be 4.5.1, node/python3 from PATH. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40W2C1Fabricate` (clone + 30 MB vendor cache) removed after copying
what this report cites.
