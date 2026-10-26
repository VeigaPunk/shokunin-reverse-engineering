# R36ExecEvidenceIds — independent recomputation of the 8 committed C1 evidence ids

Seat: leaf executor, advisory only. Round 36 / wave 1. Lane root
`/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (HEAD when measured: `d2e46ef5e2b2e8ba681b2fa55d50f298c4c4b8be`).
Measured revision for the envelopes: `3310d8fa27bfaa95ad858c4aaad6f6377f853982` ("R36-C1 after receipts").
Freeze: `790561d4e3aca732a434081aa9573ec2fa5fd7d0`.

## Verdict

All 8 committed envelopes (`K{1..4}/{before,after}.json`) recompute to their stored `evidence_id`
under rea-agents 6.5.0's own hashing code, by three independent routes, with **0 mismatches**:

- route R1 — my own import of `dist/domain/canonicalDigest.js` (`digestCanonicalValue`) applied to the
  semantic projection transcribed from `dist/domain/evidence.js`: 8/8 equal to stored.
- route R2 — the package's own authenticated parser (`parseEvidence`, whose private `computeEvidenceId`
  is the only id owner): 8/8 **accepted**, 0 thrown.
- route R3 — the CLI verb `npx -y rea-agents@6.5.0 evidence-export` over a canonical 8-record bundle
  built with the package's `createEvidenceBundle`: exit 0, `records: 8`, every id preserved.

Tamper: one changed file sha inside `normalized_result` makes the stored id wrong — recomputed id differs
and both R2 and R3 reject it. No frozen predicate, counter, carrier or oracle was touched; no defect found.

## Method (no lane xpin dependency)

Primary routes import rea-agents 6.5.0 modules directly:

- `digestCanonicalValue` from
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/canonicalDigest.js`
- `parseEvidence` (schema `authenticatedEvidenceSchema`, which recomputes the id and adds the issue
  `evidence_id: Evidence semantic identifier does not match its record`) from
  `.../dist/domain/evidence.js`
- `createEvidenceBundle` from `.../dist/domain/evidenceBundle.js` for the CLI route

The lane's xpin tool (`tools/round-27/xpin-attribute.mjs`) is **not** used by R1/R2/R3. It was run once
afterwards only as an auxiliary agreement check (§7), from its freeze blob, and its 6.5.0 column agrees.

Envelopes were read from the commit, not the worktree: `git show 3310d8fa:<path>` into scratch, then
hashed. The worktree copies are byte-identical to that commit's blobs (sha256 of all 8 matched), so the
recomputation is bound to committed bytes either way.

Package version confirmed: `node -e 'require(".../rea-agents/package.json").version'` → `6.5.0`;
`npx -y rea-agents@6.5.0 --version` → `6.5.0`. Node `v24.21.0`.

Recompute code actually executed (scratch was removed; this is the whole script, rerunnable as-is):

```js
import { readFileSync } from "node:fs";
import { digestCanonicalValue } from "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/canonicalDigest.js";
import { parseEvidence } from "/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/dist/domain/evidence.js";
// verbatim transcription of semanticProjection from dist/domain/evidence.js (6.5.0)
const semanticProjection = (evidence) => ({
    subject: evidence.subject === null ? null : {
        digest: evidence.subject.digest, format: evidence.subject.format,
        architecture: evidence.subject.architecture },
    provider: evidence.provider, analysis_profile: evidence.analysis_profile,
    predicate_type: evidence.predicate_type, operation: evidence.operation,
    parameters: evidence.parameters, raw_result: evidence.raw_result,
    normalized_result: evidence.normalized_result, confidence: evidence.confidence,
    authority: evidence.authority, environment: evidence.environment,
    limitations: evidence.limitations,
    ...(evidence.relationship_coverage === null ? {} : { relationship_coverage: evidence.relationship_coverage }),
    locations: evidence.locations, evidence_links: evidence.evidence_links });
const computeEvidenceId = (e) => `ev_${digestCanonicalValue(semanticProjection(e), "Evidence")}`;
for (const name of process.argv.slice(2)) {
    const raw = JSON.parse(readFileSync(name, "utf8"));
    const recomputed = computeEvidenceId(raw);
    let parse = "accepted";
    try { parseEvidence(raw); } catch (err) {
        parse = "REJECTED: " + ((err?.issues ?? []).map(i => `${i.path.join(".")}: ${i.message}`).join(" | ") || err.message);
    }
    console.log(JSON.stringify({ name, stored: raw.evidence_id, recomputed, match: raw.evidence_id === recomputed, parse }));
}
```

Running that over `git show 3310d8fa:corpus/evidence/round-36/c1/K*/{before,after}.json` (8 files):
`exit=0`, `all_match: true`, `all_accepted: true`.

## 1. Stored vs recomputed, per envelope

| envelope | git blob @3310d8fa | file bytes | file sha256 | stored `evidence_id` | recomputed (6.5.0) | match | `parseEvidence` |
|---|---|---|---|---|---|---|---|
| `K1/before.json` | `a974834fb504ed565b044e747b0a2d205ea04e58` | 7913 | `583f2bb6…7e7465f` | `ev_df7bef526779b3062cc0a8f149f6c32a2b5849ac2f40150df58b69df00178da3` | `ev_df7bef526779b3062cc0a8f149f6c32a2b5849ac2f40150df58b69df00178da3` | ✅ | accepted |
| `K1/after.json` | `0595e242fb8f2b53fb78895eefa25492c35f59f1` | 12230 | `a50bb972…9873acea` | `ev_b5bd2e7f0ea0b9f6e65d04d68826507464983c2d226b6fa4c542f4dcf64fc860` | `ev_b5bd2e7f0ea0b9f6e65d04d68826507464983c2d226b6fa4c542f4dcf64fc860` | ✅ | accepted |
| `K2/before.json` | `b7198b41edb9382dd49e81465d232e7fd382a1ce` | 7943 | `4c63514f…d4f45e7bc6` | `ev_7506d2a8715ac018b5b2f7aa1f1c16dd43d78c5f1bbd489fa19ceba6d5767b3c` | `ev_7506d2a8715ac018b5b2f7aa1f1c16dd43d78c5f1bbd489fa19ceba6d5767b3c` | ✅ | accepted |
| `K2/after.json` | `0d540a8361c5fb25f50c1c772889749a29ac14ed` | 19335 | `36473791…3013457f8` | `ev_c939cd88f616e8759ed2c8656f98745fd8e90aa6589a744b25f33b6366b0c88f` | `ev_c939cd88f616e8759ed2c8656f98745fd8e90aa6589a744b25f33b6366b0c88f` | ✅ | accepted |
| `K3/before.json` | `35e7cbfe00cf42cc98faefc2af9db206fb4f8dde` | 11978 | `6d2457a1…9526379b5` | `ev_91e4ab30b6a5edf4ab7a14d5a14867cac75b0e161090c5db7db6b73027e9a44a` | `ev_91e4ab30b6a5edf4ab7a14d5a14867cac75b0e161090c5db7db6b73027e9a44a` | ✅ | accepted |
| `K3/after.json` | `e51b223636c65527b19f8a8f5ed5de3a679bcce8` | 4362742 | `861736c9…148b8e01` | `ev_b83bd3056f103a72e2a611a5162f542715119490a44bb60135393b5002f5419b` | `ev_b83bd3056f103a72e2a611a5162f542715119490a44bb60135393b5002f5419b` | ✅ | accepted |
| `K4/before.json` | `cbbac53206976bbc0bad810466f87c3d69ef2a89` | 11971 | `58fcfc5c…a9c9cb67c` | `ev_fffca90bc4b70989308fcc378c3cdefdd5baaf8ee878d8e624dc31709f5b1a01` | `ev_fffca90bc4b70989308fcc378c3cdefdd5baaf8ee878d8e624dc31709f5b1a01` | ✅ | accepted |
| `K4/after.json` | `d5ab321e9982a63e5df1bfeb49f18f8a2d8339ff` | 4362857 | `8b19a191…22c806d7e` | `ev_ff0fdb798eea077df0b11dcdd3795794c9069c667424b85c5f67f566c97379fa` | `ev_ff0fdb798eea077df0b11dcdd3795794c9069c667424b85c5f67f566c97379fa` | ✅ | accepted |

(Full 64-hex file sha256 values: K1 before `583f2bb647668d2941e93091e903be727977b66b4fa01aa33feb09ed23e7465f`,
K1 after `a50bb972212b2e63da5eb87215ac406d596289dcd6380a6239456d299873acea`, K2 before
`4c63514f7ab6512dd181c497bb78a6053967362e8262770137a7b7d4f45e7bc6`, K2 after
`36473791aa34607765ade157d5c4481dc646bec02a4113efd6ca9291303457f8`, K3 before
`6d2457a165e7bc6fea071789a13f8900fcb8f75019894df67a96c999526379b5`, K3 after
`861736c9722465ea5058e04bb31f82ec4c686146016f6daab50951b8148b8e01`, K4 before
`58fcfc5c1dc958c8dcfa928470ead468ff1675644ca3aadf798602aa9c9cb67c`, K4 after
`8b19a19183f1b40d92f6eabf7fd380fe14b729286921564cb3c6e7822c806d7e`.)

All 8 ids are distinct. Envelope inventory is exhaustive for that commit: `git ls-tree -r 3310d8fa
corpus/evidence/round-36/c1` holds 24 receipt/oracle/envelope files (6 per carrier) plus `carriers.json`
and 10 fixture files; there is no other `before.json`/`after.json` anywhere in the tree, and the 12
`{before,after,oracle}-run.json` receipts carry no `evidence_id` key at all (`grep -c '"evidence_id"'` → 0
for each), so they are not evidence envelopes and are correctly outside this seat's 8.

## 2. Tampered copy fails (the falsifier)

`T1` — copy of `K1/after.json` with exactly one file sha changed:
`normalized_result.files[0].sha256` `88dc952ab79570963415341ba52c7e2a948aa69e0200987140a933c64d595961`
→ `000…000` (entry is `…/firmware.bin_extract/README.txt`; the record has 3 files).

| | value |
|---|---|
| stored id (unchanged in the file) | `ev_b5bd2e7f0ea0b9f6e65d04d68826507464983c2d226b6fa4c542f4dcf64fc860` |
| recomputed id after tamper | `ev_4e7c35261279134bafca239cc502f0f3ec11f697c86f757b9852f13e3b61c547` |
| match | **false** |
| `parseEvidence(tampered)` | `REJECTED: evidence_id: Evidence semantic identifier does not match its record` |

Same tampered record inside the 8-record bundle, through the CLI:

```
$ npx -y rea-agents@6.5.0 evidence-export bundle-8-tampered.json out-8-tampered.json
error: Analysis failed
code: evidence_integrity_mismatch
category: integrity_mismatch
message: "Evidence bundle does not match the bundle schema at records.2.evidence_id: Evidence semantic
identifier does not match its record. Supply an unmodified bundle written by export_evidence_bundle or
rea evidence-export."
retryable: false
$ echo $?
1
```

(`records.2` is the tampered record after the bundle's id sort — `ev_b5bd…`, i.e. `K1/after`.)
The untampered bundle of the same 8 records through the same verb:

```
$ npx -y rea-agents@6.5.0 evidence-export bundle-8.json out-8.json
path: …/out-8.json
bytes: 8797622
records: 8
$ echo $?
0
```

## 3. What the id actually covers (measured, not assumed)

`K1/after.json`, one field changed per row; "same id" means the stored id survives, i.e. the field is
purely display metadata:

| mutation | recomputed id | equals stored | `parseEvidence` |
|---|---|---|---|
| none | `ev_b5bd2e7f…f64fc860` | yes | accepted |
| `subject.name` → `renamed.sqsh` | unchanged | yes | accepted |
| `subject.local_path` → `/somewhere/else/k1-le-xz.sqsh` | unchanged | yes | accepted |
| `relationship_coverage` key deleted (was `null`) | unchanged | yes | accepted |
| `subject.digest.sha256` → `111…111` | `ev_316248ac…5c3d61321` | no | REJECTED |
| `parameters.output_directory` → `/tmp/out` | `ev_11d32858…ab095be` | no | REJECTED |
| `parameters.max_depth` 3 → 4 | `ev_14edb82f…44e92890` | no | REJECTED |
| `raw_result.execution.exit_code` 0 → 2 | `ev_405c9243…a7727180` | no | REJECTED |
| `raw_result.execution.stdout.text` + one space | `ev_71dddc15…7e9209f59` | no | REJECTED |
| `raw_result.execution.stdout.bytes` +1 | `ev_dabce319…2817761` | no | REJECTED |
| `confidence` observed → derived | `ev_85d6ef87…5fc01b2746` | no | REJECTED |
| `limitations` + one string | `ev_f7c9bdaf…6b18a145f701` | no | REJECTED |
| `normalized_result.files[0].sha256` → `000…` (T1) | `ev_4e7c3526…f13e3b61c547` | no | REJECTED |

`K1/before.json` spot checks: `raw_result.execution.exit_code` 1 → 0 → `ev_e548311e…e628eead5` (no);
`normalized_result.extraction_gaps[0].dependencies` emptied → `ev_fe0e517a…7869713598` (no).

Caveat on one discarded variant: a first pass mutated `K1/after.json`'s exit_code `1 -> 0`, which is a
no-op there (that envelope already stores `0`; the K1 after-run is a successful extraction) and therefore
correctly reported "unchanged". The genuinely-different mutation is the `0 -> 2` row above.

## 4. Invariance and canonical export

For all 8 envelopes, re-serialising the parsed record and recomputing gives the stored id unchanged:
original bytes, `JSON.stringify(..., 4)`, minified, and **every object key order reversed recursively**
all produce the identical id (`all_equal: true` for 8/8). The id is over canonical JSON of the semantics,
not over file bytes.

Canonical export is idempotent: `evidence-export bundle-8.json → out-8.json` then
`evidence-export out-8.json → out-8b.json` gives `records: 8` twice and
`sha256 f6d880c167c3795a8a25ad5c666a0e06f0ea1c4d2f0391cc54304d32261b989b` for **both** outputs, while the
input bundle file (my pretty-printed `createEvidenceBundle` output) hashes
`17b7ca0b6294a3ae3b34fb84b57fefeaefbf847e3633d66db79f805f12c4123c` — i.e. the export step normalises
formatting and is stable thereafter.

## 5. Freeze / identity bindings observed while doing this

- `before.json` blobs at freeze `790561d4` equal the blobs at `3310d8fa` for all four carriers
  (`git rev-parse 790561d4:<path>` = `git rev-parse 3310d8fa:<path>`; K1 `a974834f…`, K2 `b7198b41…`,
  K3 `35e7cbfe…`, K4 `cbbac532…`). `after.json` is **absent** at the freeze commit for all four
  (`git cat-file -e` fails), consistent with "after receipts land later".
- The four `subject.digest.sha256` values in the envelopes equal the four `carriers.json` sha256 values
  exactly: `93802938…c9b8a589` (K1), `ce5bf60e…36a2084f` (K2), `b644d034…c35f29fb` (K3),
  `8efcec73…c9efe1c2` (K4). Each envelope's `provider` is `unblob@26.6.4`, `operation` `extract_firmware`,
  `predicate_type` `rea.analysis` — i.e. the two receipts per carrier are indistinguishable in subject and
  provider and differ only in semantics, which is exactly what the tamper table above shows to be hashed.

## 6. Consequence for the R36-C1 predicate clause

P36-C1 requires that "both receipts recompute to their stored evidence id under the rea-agents 6.5.0
rule". For all four carriers that clause is **supported by this independent measurement** (8/8 stored ==
recomputed, 8/8 accepted by the package's own authenticated parser). I did not run the frozen counter and
I did not evaluate the other predicate clauses (file matching, gaps, PROVINCE row, knowledge entry,
SOURCES row); this seat speaks only to the id clause.

## 7. Auxiliary agreement check against the frozen xpin tool

Not part of the primary route — after R1/R2/R3 finished, I ran the freeze blob of
`tools/round-27/xpin-attribute.mjs` (`git show 790561d4:tools/round-27/xpin-attribute.mjs`) on the same 8
envelopes wrapped as `{"data": <envelope>}` (the wrapper the frozen counter also uses), with
`--pkg65 …` and `--pkg67 …` both pointing at the 6.5.0 root:

```
$ node xpin-frozen.mjs --pkg65 <rea-6.5.0-root> --pkg67 <rea-6.5.0-root> wrapped/*.json
…/K1-after.json  ev_b5bd2e7f…  ev_b5bd2e7f…  ev_b5bd2e7f…  both
… (8 lines) …
$ echo $?
0
```

Its 6.5.0 column matches stored for 8/8. Because `--pkg67` was the same root, the "6.7.0" column and the
`both` verdict are degenerate here and carry no information; only the 6.5.0 column is evidence. This check
is a consistency note for the counter's route, not an independence claim.

## 8. Limitations and risks (advisory, nothing repaired)

1. **Ids are scratch-path dependent.** `parameters.path`, `parameters.output_directory` and the absolute
   paths inside `raw_result` are hashed. The committed envelopes store
   `/fast/scratch/hyaku/kaidoku-r36/…` values for both. Consequence: the ids are reproducible from the
   committed files (as measured) but **not reproducible from the carriers alone** — an independent rerun in
   a different scratch directory yields different ids even with identical extraction output. This does not
   weaken the counter (which recomputes from the stored records) but it does bound any future claim that
   the ids are "independently regenerable".
2. **Display fields are excluded by design.** `subject.name` and `subject.local_path` do not affect the id
   (measured). A record whose display path was edited would still authenticate; nothing else in the
   envelope may be edited.
3. `K3/after.json` and `K4/after.json` are 4.36 MB each; recomputation is a full canonical hash of the
   whole payload (including `raw_result` stdout text). Any future verification step pays that cost per
   envelope (measured runs completed in a few seconds each under node v24.21.0).
4. The 6.7.0 rule was not exercised here (no 6.7.0 package was consulted); the seat's target is the 6.5.0
   rule as frozen.

## 9. Tooling record

Nothing was installed or upgraded. Used: `node v24.21.0` (pre-existing), the already-cached
`rea-agents@6.5.0` npx package at `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`, and
`npx -y rea-agents@6.5.0` for the two `evidence-export` runs. No pacman transaction; no service touched; no
`xd://mcp__rea_*` device used. `REA_UNBLOB_COMMAND` was not needed (`extract-firmware` was not run — this
seat only re-hashes committed receipts).

## 10. Scratch

All work lived in `S=/fast/scratch/hyaku/kaidoku-r36/R36ExecEvidenceIds` (`TMPDIR` pointed there); clones,
bundle exports and tampered copies are deleted at the end of this seat. Every fact cited above is either a
command line plus its exit status or a value copied into this report; no evidence rests on a scratch or
`/tmp` path. No file in the lane was modified except this report.
