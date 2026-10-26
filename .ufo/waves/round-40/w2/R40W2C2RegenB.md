# R40W2C2RegenB — C2 held-out regeneration + fresh-interpreter labelling

**Verdict: CONFIRMED (R40-C2 regeneration and labelling hold), with one measured reproducibility
defect in the harness (an intermittent REA publication failure, 1 of 58 invocations) and one
calibration observation that strengthens, not weakens, the row set.**
I attacked the C2 data path, not the C2 row semantics: I re-ran REA 6.5.0 `extract-firmware` (and
`inspect-firmware-regions` for the out-of-domain arm) on all 26 committed held-out carriers in their
manifest arms, compared every triage feature and the published file sets against the committed
envelopes/receipts, regenerated the 26 carriers from the freeze seed, and labelled my **fresh**
envelopes with the **freeze** interpreter against `SKILL.md` at `42c10a58`.

Headline numbers: **26/26 fresh REA runs ok**, **0 feature mismatches vs the committed envelopes**,
**26/26 published-file sets identical**, **26/26 carriers regenerate byte-identically**,
**26/26 fresh envelopes labelled exactly the generator's pairs**, and my independent re-execution of
the frozen C2 counter reproduces the L1 receipt bit for bit (`matched 26`, `exit 0`).

## 1. What was run (exact)

Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40W2C2RegenB` (removed at the end); every command below
ran with `cwd=$S`. Artifacts: `.ufo/waves/round-40/w2/artifacts/R40W2C2RegenB/`.

- Frozen inputs materialised read-only from git:
  `git show 7fce308631a8b457d6b7c5a4b39a923c4e9a49de:tools/round-40/sqfs-triage-v2.py`
  → sha256 `336c621c46e78ca528d08597e7ed652c89fe95e31dbfe339fbfd86381c6b8617`;
  `git show 42c10a58cb2cae3a4a0122af35a0cf95ac718043:SKILL.md`
  → sha256 `ab8c7463a243095663cefb4d4823edd3a23aab9fcaa20fffb90a2dd8a366561d`.
  The same `SKILL.md` sha256 is the freeze blob (`7fce308:SKILL.md`) **and** the tip blob
  (`4d62ee5:SKILL.md`) — the `42c10a58` measurement read identical bytes (`blob-identity.txt`).
- Fresh REA, one process per carrier, arm taken from the committed manifest
  (`corpus/evidence/round-40/c2/heldout/manifest.json`):
  `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <carrier> <fresh outdir>`
  for the 24 `extract_firmware` carriers and
  `npx -y rea-agents@6.5.0 inspect-firmware-regions --format json --full-output <carrier>` for
  H25/H26. `REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob` in every arm; for `arm=before` (H13–H16) the
  child PATH had `$HOME/.local/bin` removed exactly as `heldout-gen-v2.py:rea_env` does
  (`home_bin_on_path=false` in `fresh/H*/fresh-run.json` for those four, `true` for the other 22).
- Feature comparison: my own projection (`regen.py shape()`) plus the **freeze interpreter's**
  `features()` (`--json`) over both envelope sets. Labelling:
  `python3 -I -B frozen/sqfs-triage-v2.py --skill frozen/SKILL-at-42c10a58.md --json fresh/H*/envelope.json`.
- Carrier regeneration: `python3 -I -B tools/round-40/heldout-gen-v2.py --seed 7fce308…de --out
  $S/regen-carriers --scratch $S/regenscratch --gen tools/round-39/gen-squashfs.py` (no `--run`).
- Counter re-execution (read-only git, receipt into my artifacts dir):
  `python3 -I -B tools/round-40/c2-counter.py --root <LANE> --rev 42c10a58… --freeze 7fce308… --json-out
  .ufo/waves/round-40/w2/artifacts/R40W2C2RegenB/c2-reexec-at-42c10a58.json`.

## 2. Feature comparison (fresh vs committed) — 0 mismatches

Projection keys compared per carrier: `OP` (operation), `PV` (provider.id), `H` (squashfs handlers),
`G` (gap kinds), `D` (gap dependencies), `BE` (`-be` in a recorded sasquatch argv), `SR`
(`MaliciousSymlinkRemoved`), `P` (published file count). Also compared against the committed
`run.json` receipt fields `operation, provider, handlers, failed_chunks, gap_kinds,
gap_dependencies, files, coverage, diagnostics` — **26/26 equal** (`shape-compare.json`), and the
committed `run.json` is itself consistent with its own committed envelope (0 differences), so the
receipts were not recorded from a different run.

| id | class | arm | fresh OP / PV | H | G | D | BE | SR | P |
|---|---|---|---|---|---|---|---|---|---|
| H01,H02 | clean-be | after | extract_firmware/unblob | v4_be | — | — | n/a | no | 5,3 |
| H03,H04 | clean-le | after | extract_firmware/unblob | v4_le | — | — | n/a | no | 8,5 |
| H05,H06 | clean-empty | after | extract_firmware/unblob | v4_be / v4_le | — | — | n/a | no | 0,0 |
| H07,H08 | escaping-symlink-removed | after | extract_firmware/unblob | v4_be / v4_le | — | — | n/a | yes | 3,8 |
| H09,H10 | in-tree-symlink-metadata | after | extract_firmware/unblob | v4_be / v4_le | unpublished-entry | — | n/a | no | 8,5 |
| H11,H12 | mixed-symlinks | after | extract_firmware/unblob | v4_be / v4_le | unpublished-entry | — | n/a | yes | 5,4 |
| H13,H14 | dep-missing-be | before | extract_firmware/unblob | v4_be | missing-extractor-dependency | sasquatch-v4be | n/a | no | 0,0 |
| H15,H16 | dep-missing-le | before | extract_firmware/unblob | v4_le | missing-extractor-dependency | sasquatch | n/a | no | 0,0 |
| H17,H18 | avm-marker-be-dropped | after | extract_firmware/unblob | v4_be | extractor-failure | — | **no** | no | 0,0 |
| H19,H20 | body-extractor-failure | after | extract_firmware/unblob | v4_be | extractor-failure | — | **yes** | no | 0,0 |
| H21,H22 | partial-body-failure | after | extract_firmware/unblob | v4_be | extractor-failure | — | **yes** | no | 5,3 |
| H23,H24 | no-squashfs-chunk | after | extract_firmware/unblob | none | — | — | n/a | no | 0,0 |
| H25,H26 | out-of-domain | ood | **inspect_firmware_regions/binwalk** | none | — | — | n/a | no | 0,0 |

Supporting equalities:

- **Published files**: the `(relative_path, size, sha256)` set is identical committed↔fresh for
  **26/26** carriers.
- **Gaps**: 16/26 gap dicts are byte-identical *including* `continuation_id`; the other 10 differ in
  exactly one field, unblob's volatile blob id `provider_id` (`1522852:1`→`1154540:1` for H13, etc.).
  No difference in `kind`, `handler`, `range`, `dependencies` or `continuation_id` (`gap-identity.json`).
- **Subjects**: fresh envelope `subject.digest.sha256` equals the manifest pin and the committed
  carrier sha256 for 26/26.
- **Parameters**: the only `parameters` field that differs is `output_directory` (my scratch path);
  `max_depth = 3` on the 24 extract-firmware envelopes, absent (region scan) on H25/H26.
- **Toolchain**: fresh `normalized_result.engine` = unblob `26.6.4`
  (`0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`) / binwalk `3.1.0`
  (`5fc19aac1f357a66a47e8b20a8038a84cb93971cb5d331bd4503b02fcc0a40d6`) — the *same two shas* as the
  committed envelopes. No tool drift between generation and this re-run.
- **`SR` count sanity**: H07/H11 carry exactly **one** `MaliciousSymlinkRemoved` report each (the
  same dict appears once in `normalized_result.diagnostics` and once inside `raw_result`).

## 3. Carrier regeneration — 26/26 byte-identical

`heldout-gen-v2.py --seed 7fce308…de` into a fresh directory: all 26 `carrier.sqsh` sha256 equal the
manifest pins **and** the committed blobs; the regenerated manifest's `class, label, action, arm,
operation, endian, compression, tree, content, symlinks, corruption, damage, carrier, sha256` fields
are equal to the committed manifest for all 26 (`manifest field diffs: 0`), and the regenerated
`generator.sha256` = `644d8f6e44e0a46dfed0be4e8bfc4a365094b7f10b9415b2a7c5b2b98662af85` = committed.
The frozen counter's own `carriers_regenerated: true` binding agrees.

## 4. Labelling my fresh envelopes with the freeze interpreter — **26/26**

`frozen/sqfs-triage-v2.py` (freeze blob) against `SKILL.md@42c10a58`, on my 26 fresh envelopes:
`matched 26/26`, every pair equal to the generator's pre-run assignment, exit 0 (`label-fresh.json`).
Same run over the committed envelopes also gives 26/26 (control).

Row assignment (interpreter `rule` index, 1 = first row):

| label | action | row | labels→row |
|---|---|---|---|
| no-squashfs-chunk | inspect-input | 1 | clean-be + clean-le → 10 |
| dep-missing-be | install-extractor-be | 2 | 11 distinct rows for 11 labels |
| dep-missing-le | install-extractor-le | 3 | unclassified → no row (`rule: null`) |
| avm-marker-be-dropped | wrap-extractor-be | 4 | |
| body-extractor-failure | preserve-failure | 5 | |
| partial-body-failure | salvage-partial | 6 | |
| mixed-symlinks | audit-symlinks | 7 | |
| escaping-symlink-removed | expect-link-absent | 8 | |
| in-tree-symlink-metadata | count-gap | 9 | |
| clean | none | 10 | |
| clean-empty | confirm-empty | 11 | |

Feature-space facts that keep the score from being a row-order trick:

- The 26 envelopes carry **17 distinct feature vectors** (replicates split by `H` = `v4_be`/`v4_le`),
  and **no vector is shared by two labels** — each label is feature-separable on the observed set.
- **`--table-only`** on the measured SKILL prints 11 rules, exit 0.
- **The v1 block is not consulted**: I deleted the round-39 (v1) table rows from `SKILL.md`
  (`frozen/SKILL-no-v1-block.md`, v1 marker line kept) and re-labelled — identical 26/26 pairs, so
  the decision really is the v2 block alone.
- A failed REA run (`{ok:false,error:{code:"execution_failure"…}}`, the H10 flake in §6) is **not**
  silently labelled `unclassified`: the interpreter exits **2** with
  `no normalized_result or operation` (measured), i.e. the pipeline fails closed.

## 5. Freeze integrity, ordering, and the frozen counter

- `git diff --name-only 7fce308… 42c10a58… -- tools/round-40/{sqfs-triage-v2.py,heldout-gen-v2.py,
  c2-counter.py} tools/round-39/gen-squashfs.py SKILL.md plans/round-40-claims.md` → **empty**
  (and empty against the tip `4d62ee5`); no commit in the range touches a frozen C2 path.
- `manifest.json` and all 26 `envelope.json` files are first added in
  `2d1ac5bcd08f6828dbfdee9054bbeec0ea211b33` (2026-10-26T16:16:03-03:00), which descends from the
  freeze (`git merge-base --is-ancestor 7fce308 2d1ac5b` → yes); manifest is no later than its
  envelopes (same commit).
- Independent counter re-execution: `matched 26, n 26, met_target true, met_target_consistent true,
  bindings_ok true, bindings_false [], distinct_decisions 12, exit_code 0`, revision/freeze exactly
  as specified, and the per-carrier `(label, action, row, pair_match)` map is **identical** to the L1
  receipt `scores/c2-at-42c10a58.json`. Only the receipt path differs.

## 6. Defect found (harness, not the claim): one REA publication failure on H10

The first batch attempt at H10 returned `rc=1` with an `ok:false` CLI envelope (not evidence):

```
{"ok":false,"error":{"code":"execution_failure","category":"execution_failure","message":"Analysis could not complete. …","retryable":false,
  "details":{"provider_id":"unblob","operation":"extract_firmware","diagnostics":{
    "reason":"ENOENT: no such file or directory, readlink '/tmp/rea-firmware-pAY6tQ/extracted/firmware.bin_extract/m1l5kvd/ke9e0'"}}},
 "meta":{"command":"extract-firmware","duration":"1074ms"}}
```

`ke9e0` is exactly H10's in-tree link (`tree.json` oracle symlink `m1l5kvd/ke9e0 → ../5z5b5p5d4`), so
this is a race between unblob's symlink publication and REA's staging `readlink`, i.e. a REA-side
publication defect on the in-tree-symlink class. Rate: **1 failure in 58 REA invocations in this seat**
(26 batch + 4 H10 retries + 28 targeted), and all of it on H10 — 1 failure in 17 H10 invocations
(5.9%); the follow-up probe was **0 failures in 28** (H10 ×12, H09 ×6, H11 ×6, H07 ×4)
(`flake.json`). Consequences, all benign for the claim but worth recording: at generation time such a
failure would leave the envelope *absent* — `run_rea` records `error: 'no JSON envelope on stdout'`
and the counter's `envelopes_valid` / `classes_two_each` bindings would fail, so it cannot produce a
false pass; and the error envelope itself is unlabellable (interpreter exit 2), so it cannot become a
false `unclassified`.

## 7. Calibration: which cells are load-bearing (188 one-cell mutants)

I mutated each fresh envelope one cell at a time (gap set flip, `MaliciousSymlinkRemoved` add/strip
across `normalized_result` *and* `raw_result` lists, published-count 0↔>0, handler null, dependency
add/strip, recorded `-be` toggle, operation swap, provider swap) and re-labelled with the same frozen
interpreter (`mutation-surface.json`). 188 mutants, `rc 0`.

| class | load-bearing cells | inert |
|---|---|---|
| clean, clean-empty | G, SR, P, H, D, OP, PV | — |
| escaping-symlink-removed | SR, G, H, OP, PV | D, P |
| in-tree-symlink-metadata, mixed-symlinks | G, SR, D, H, OP, PV | P |
| dep-missing-be / -le | D, G, SR, H, OP, PV | P |
| avm-marker-be-dropped | BE, D, G, H, OP, PV | P, SR |
| body / partial-body-failure | P, D, G, H, OP, PV | SR, BE (`BE` only exists for 6 envelopes) |
| no-squashfs-chunk | OP, PV | H(already none), G, D, P, SR |
| out-of-domain | — (never matches a row) | all |

Every class is held by ≥2 independent cells except the two singleton rows, and the neighbour collapses
are the semantically correct ones: `escaping −SR → clean` (the silent-removal hazard the row's cause
warns about), `mixed −SR → in-tree-symlink-metadata`, `body ↔ partial` on `P`,
`avm +-be → body-extractor-failure`, `handler nulled → no-squashfs-chunk`,
`operation or provider swapped → unclassified`. This also shows the provider cell is a live guard on
its own (a `PV`-only mutant falls to `unclassified`) even though the held-out set varies `OP` and `PV`
together, as the claims already disclose.

Artifact-level note for the partial row: H22 publishes 3 of 3 files present, but the last one is
**truncated** (8192 B vs oracle 9389 B, sha differs). The row's action (`salvage-partial`, match by
relative-path suffix) is what makes that outcome scoreable; a sha-strict oracle match would call it a
mismatch by design. H21 publishes all 5 files (its damage is in a directory block, so file bytes are
intact). This is the intended semantics, but it means "published set == oracle set" is *not* a
conformance test for this class.

## 8. Limits of this check

- Re-runs prove the *committed bytes* still produce the same envelopes today; they cannot prove which
  process wrote the committed envelopes (same limit C1 discloses for its receipts).
- Same class set only: nothing here tests a class the generator cannot produce (`unknown-chunk-handler`,
  `encrypted-chunk`, `depth-limited`, genuine AVM-layout success) — outside both claims as written.
- `provider_id` blob ids and `evidence_id` differ per run by construction; both are outside the triage
  projection and outside P40-C2. `evidence_id` recomputation was not attempted (not part of P40-C2).
- My batch driver is not the frozen generator's `run_rea` (it is an independent implementation), which
  is deliberate; the equality of its output with the committed receipts is the measurement.
- The mutation surface is a probe of *this* table against *these* feature vectors; it bounds which
  cells matter on the observed set, it does not prove cell necessity in general.

## 9. Evidence inventory (`.ufo/waves/round-40/w2/artifacts/R40W2C2RegenB/`)

- `fresh/H01…H26/{envelope.json,fresh-run.json}` — my fresh envelope data objects + per-run record
  (arm, argv, exit code, `home_bin_on_path`, shape); `fresh-index.json` carries the sha256 of every
  fresh `rea-full.json` (the full `{ok,data,meta}` wrappers stayed in scratch; ~0.9 MB total).
- `label-fresh.json` (26/26 + rule/row per envelope), `conformance.json` (oracle vs published),
  `shape-compare.json` (fresh vs committed shape + run.json vs its own envelope),
  `gap-identity.json` (gap dict identity incl. `continuation_id`/`provider_id`),
  `env-provenance.json` (params, engines, providers, evidence ids), `mutation-surface.json` (188
  mutants), `flake.json` (H10 failure rate), `c2-reexec-at-42c10a58.json` + `.stdout`/`.stderr`
  (independent counter run, exit 0), `blob-identity.txt` (frozen blob shas).

## 10. Tooling

No installs or upgrades in this seat; **no pacman transaction** (host-wide pause respected), nothing
touched in `~/.local/bin`. Tools used as found: `npx -y rea-agents@6.5.0` (already in the npx cache),
unblob `26.6.4`, `python3 -I -B`, read-only `git show/log/diff/merge-base/cat-file`. Scratch
`/fast/scratch/hyaku/kaidoku-r40/R40W2C2RegenB` removed after the artifacts were copied; no vendor
firmware bytes were touched or copied.
