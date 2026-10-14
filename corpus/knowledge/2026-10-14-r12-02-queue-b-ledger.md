<!-- corpus entry — kaidoku-shokunin round 12 goal-mode Queue-B, EXPAND Q2 lane (r12-02), finished 2026-10-14. Spec/authority: corpus/knowledge/2026-10-13-r4-16-frontier-rescan.md Queue B table lines 191–206 (row L203 = "compare-application-versions success path", the assignment's L203) + the r11-02 recon seed. Assignment check performed first: r4-10 (2026-10-13-r4-10-real-version-pair.md) does NOT hold this verb — its pipeline is analyze/search/function + compare/compareBundles/compareFunctions (rows 3, 13–16), compare-application-versions is invoked nowhere in it; repo-wide grep finds the verb only as the r2 typed refusal (2026-10-13-r2-version-diff-compare.md run-log row 13), the census cell (rescan line 203), PROVINCE frontier line 150, doc claims (r2-skill-references-deep line 58, r1 asar-surface line 57), and the r11-02 recon — so L203 was genuinely open, NOT a row-7-class defect close. Git clean at lane start and pre-write at HEAD 47d492a (no sibling landed mid-lane). All scratch /tmp/r12-02-scratch/; the only non-/tmp writes are this entry + the rescan erratum append. Substrates touched read-only and re-digested after (all unchanged): the two r4-09 obsidian Evidence files, /usr/lib/pinta/{Pinta,Pinta.Effects}.dll, the Godot debug APK, nvidia GSP/ucodes blobs, /usr/bin/jq, /tmp/wakaru-e2e/input.js, the wakaru ELF, the jadx jar. Secrets: env values shape-checked only; one fixture-adjacent token class none. Side-effect disclosed: the list-adb-devices spot-check auto-started the adb daemon on :5037; killed via `adb kill-server`, port verified closed. -->

# r12-02 — L203 discharged on BOTH input classes (obsidian 1.12.7↔1.13.7 JS-graphs: first real application-version diff; Pinta managed-graphs: honest all-unknown) + the FULL Queue-B exercised-set ledger (L195–L206)

Axes: **census-completion** (every Queue-B row classified held vs truly-open, with a
spot-check re-derivation per held row) / **verb-contract** (the version-compare
input ladder, match-tier semantics, identity laws observed live) / **determinism**
(byte-identical re-runs; cross-round id reproduction down to r9-02's projection
ids) / **defect-hunt** (the assignment's r4-10 check — answered negative) /
**citation-hygiene** (one phantom evidence id found in PROVINCE/LOG).

Inputs: `/tmp/app-1127-analysis.json` (obsidian `app.asar` **1.12.7** JS-graph,
`ev_a29ab2a01c5a2e62865997fd77daedff2cc5e0bc3e66c5c775f9df152effd708`, 10,541,236 B,
sha256 `a14de87a…7101`) and `/tmp/app-1137-analysis.json` (**1.13.7**,
`ev_4c3202c91275ad17b2220e287adfe8241d50381655097cd3daa737073c112da6`, 11,993,834 B,
sha256 `41152a79…7101`) — r4-09's held evidences (its run-log rows 4–5), still on
disk; both files' embedded ids re-derived byte-exact this lane before use, operation
`analyze_javascript_application` (the refusal message's "authenticated JavaScript
analysis" class). Managed side: fresh `inspect-managed-members` runs on
`/usr/lib/pinta/Pinta.dll` (sha `76472751…b9e8`, the all-rounds pin) and
`/usr/lib/pinta/Pinta.Effects.dll` (sha `468ed7c7…793b`).

## Candidate 1: L203 JS-graph class — the verb's first success on this host is a REAL cross-version verdict: obsidian 1.12.7→1.13.7 diffs 10 changed / 208 unknown over 218 items, every changed item semantic-key-paired

- claim: `rea compare-application-versions <inputJson>` (CLI verb, `--schema` =
  single `{inputJson: string}` "Inline workflow JSON or JSON file path") accepts
  `{"left":<Evidence>,"right":<Evidence>}` where both are JavaScript application
  analyses. Fed r4-09's two obsidian evidences (39,119,964 B composed input; jq
  pretty-printing, not minified), it returns **exit 0 in 3.3 s** (1,320,565 B
  envelope): `ev_7a8d0ec47cd613ad4f459bed7e2d746dad5301ea9073b8f79a0be8ac96cc4010`,
  operation `compare_application_versions`, provider `rea-javascript-application-
  workflows`, predicate `rea.application-version-comparison`, `confidence:"inferred"`,
  `authority:"analyst-inference"`, comparison_id
  `javc_efb02d28ebd9067bb8c91f127c6cc5a829f7bed8c4bf8ca37860821d18e37226`. Summary
  **`{unchanged:0, added:0, removed:0, changed:10, unknown:208}`** over a matching
  ladder of `{exact_node_identity:12, exact_content_digest:11,
  exact_module_source_digest:0, source_map_identity:0, structural_fingerprint:0,
  semantic_key:24, ambiguous:0, unmatched:171}` (= 218 items; 12+11 exact-paired
  items land `unchanged`, the 24 semantic-key pairs split 10 changed / 14 unknown,
  the 171 unmatched stay `unknown`). **All 10 `changed` items carry
  `match:{status:"matched", basis:"semantic-key", confidence:"medium"}`** — real
  cross-version correspondences that survived a version bump WITHOUT stable names,
  exactly the anti-ordinal law the r2 docs claim. Coverage `{left_graph_status:
  "partial", right_graph_status:"partial", status:"partial"}` — honest propagation
  of both r4-09 budget-truncated graphs, and the reason `added/removed` are 0:
  the envelope's own limitation states unmatched entities on the opposite side
  "remain unknown rather than added or removed". Changed-item node-kind census:
  2 artifact + 4 asar-entry + 2 javascript-asset + 2 package changed (dimensions
  `content`/`properties`); unknowns dominated by 140 javascript-module +
  28 ipc-channel. Side join digest-verified: `left.root_artifact_sha256
  a92d31a5…118e` == r4-09's recorded app.asar 1.12.7 sha; every item's
  `evidence_links` binds both source evidences (right id first). Per-item
  limitation verbatim: "Semantic-key pairing is a deterministic inference and is
  never promoted to exact identity."
- source: `/tmp/r12-02-scratch/cav-js.in.json` → `cav-js.run1.json` (also
  `cav-js.run2.json`); envelope anatomy via jq in transcript.
- verify: re-run the same command → **byte-identical output, same
  `ev_7a8d0ec4…`** (`cmp` clean) — the id is content-addressed. Re-derive the
  input ids: `jq -r .evidence_id /tmp/app-11{27,37}-analysis.json`.
- verified-at: 2026-10-14 (this lane).
- suggested: admit — L203's census cell ("two JS-graph/managed evidences — now
  self-provisionable; only the refusal datum is held") is hereby discharged on
  the JS class with a real verdict, not a fixture.

## Candidate 2: L203 managed-graph class also accepted — Pinta.dll↔Pinta.Effects.dll compares validly and returns an honest all-unknown non-verdict (4,114 items, 0 paired); the mechanism is that the managed projector emits the SAME JavaScriptApplicationGraph data model

- claim: fresh `inspect-managed-members` re-minted the held ids byte-exactly
  (Pinta.dll → `ev_f382333b…` == r4's `/tmp/r4-mem-pinta.json`, `cmp` clean —
  fourth independent confirmation; Pinta.Effects.dll → `ev_92faacb3…` == the
  r10-01 id). `project-managed-application-graph` with the strictObject input
  `{managed_members:<Evidence>}` (keys `managed_artifact`/`managed_members`/
  `managed_native_boundaries`, at least one — typed refusal on `{}`:
  "At least one managed artifact, member, or native-boundary Evidence record is
  required") projected Pinta.dll → **`ev_4d2b732d…`/`magp_8d35cc89…` (1,545
  nodes, 711 methods — r9-02's exact ids, byte-reproduced across rounds)** and
  Pinta.Effects.dll → `ev_35d2e7aa…`/`magp_32fd21a4…` (2,569 nodes, 1,671
  methods, new evidence). Feeding the two projections as left/right succeeds:
  `ev_b5fc998fe0978f4db2e9c4465120fad0c0f7013323ffd72ee85a40e62b7df6fc`,
  comparison_id `javc_9243603f…`, summary **`{unknown:4114}`**, matching ladder
  all-zero with `unmatched:4114`, coverage partial/partial — mechanically
  valid, honestly a non-verdict: two different assemblies share no node
  identity and the engine refuses to guess. Re-run byte-identical. Mechanism
  anchor: the projector's schema module imports `createJavaScriptApplicationGraph`
  (`dist/domain/managed/managedApplicationGraph.js:10-13`) — managed projections
  are JAG-shaped, which is precisely why the version-compare accepts them.
- source: `/tmp/r12-02-scratch/mem-pinta.json`, `mem-effects.json`,
  `pmag-{pinta,effects}.{in.json,json}`, `cav-mgd.in.json` (12,13 MB),
  `cav-mgd.json`, `cav-mgd.run2.json`; npx cache
  `~/.npm/_npx/9b9809298fe40d2c/node_modules/rea-agents/dist/domain/managed/
  managedApplicationGraph.js:23-40`.
- verify: the chain verbatim; `cmp cav-mgd.json cav-mgd.run2.json` clean.
- verified-at: 2026-10-14 (this lane).
- suggested: admit — both accepted input classes named by the r2 refusal
  ("authenticated JavaScript analysis, runtime reconciliation, or managed
  application graph Evidence") are now exercised except the runtime-reconciliation
  class, which stays open (no held reconcile evidence of a re-analyzable app was
  composed this lane; r4-08's sessions are gone by design).

## Candidate 3: the input ladder, negative side — `{}` → left/right missing; same-evidence id → superRefine "Application version Evidence must be distinct"; r2's schema claims confirmed live

- claim: `compare-application-versions '{}'` → `invalid_request`/`invalid_input`
  (retryable) with `issues:[{path:["left"],reason:"missing_argument",
  expected:"object"},{path:["right"],…}]` — the r2 schema note (two evidenceSchema
  + native-observation arrays) at its emptiest. Composing
  `{"left":<ev_a29ab2a0…>,"right":<same>}` fires the superRefine:
  `invalid_request`/`invalid_input`, `issues[0]:{path:["right"],
  reason:"invalid_value", message:"Application version Evidence must be
  distinct"}` — the distinct-ids identity rule observed live for the first time
  (r2 recorded it from source only,
  `javascriptApplicationVersionComparisonSchemas.js:38-44`).
- source: `/tmp/r12-02-scratch/cav-empty.json`, `cav-sameid.json`.
- verify: both commands verbatim; exit codes 1, typed envelopes.
- verified-at: 2026-10-14 (this lane).
- suggested: admit — completes the verb's refusal ladder alongside the r2
  native-records datum.

## Candidate 4: spot-check re-derivations — five held Queue-B ids re-minted BYTE-EXACT, one per-run-id class characterized, one citation defect found

- claim: (a) `inspect-binary-layout /usr/bin/jq` → **`ev_294a449c…` byte-identical
  to r4-13's held id**, subject digest == on-disk `/usr/bin/jq` sha256
  `e8156675…7806` — L195 current, not just historic; the r11-02 venv concern is
  refined: `import pwn` OK but `import unicorn` still fails on missing
  `pkg_resources` (r11-02's finding confirmed live), yet the verb succeeds —
  unicorn is NOT on the pwntools-elf layout import path, so the "one venv fix"
  caveat is latent-only for Queue B. (b) `decode-android-resources` on the Godot
  debug APK → **`ev_a78193a3…` byte-identical to r4u-02's content-deterministic
  id** (apktool 3.0.3, `subject:null`/`raw_result:null` law re-shown). (c)
  `list-adb-devices` → **`ev_d4d8cc77…` byte-identical to r4u-06** (daemon up;
  `devices:[]` unchanged). (d) `inspect-firmware-regions` on
  `gsp_tu10x.bin` → **56 regions, coverage `signature_scan`** — r4u-01's exact
  count; the id is per-run (`ev_154bf0eb…` ≠ `ev_0388cb9a…`) because raw_result
  embeds the mkdtemp staging path (same law as jadx; region census is the
  re-derivation). (e) `extract-firmware ucodes_tu10x.bin` → `coverage:"complete"`,
  `files:0` — the honest-empty law reproduces. (f) `recover-javascript-sources`
  on r4u-05's exact e2e input (`/tmp/wakaru-e2e/input.js`, still on disk) →
  exit 0, `raw_result` keys `execution,provenance,report,version`, version stdout
  `wakaru 1.14.0`, report total 1 — success reproduces; the id is run-shaped
  (`ev_dc2f39ce…` ≠ r4u-05's `ev_5cb1856a…`, which named a different outdir).
  (g) jadx jar sha256 re-hash == the r4u-02 pin exactly
  (`6e5eacf5…73ff75`). (h) DEFECT: `ev_4898906e…` — cited as r4u-05's lodash
  evidence at `PROVINCE.md:117` and `LOG.md:76` — appears NOWHERE in the corpus
  (repo-wide grep: only those two citations); the entry's actual success id is
  `ev_5cb1856a…` on `input.js`. Phantom citation, flagged for the parent
  (PROVINCE/LOG are not lane-writable).
- source: `/tmp/r12-02-scratch/{ibl-jq,dar,lad,ifr-tu,ef-tu,rjs}.json`,
  `all.sha256.after`, `jq.sha256.mid`.
- verify: each command in the run log; `cmp` against the held files where they
  survive (`/tmp/r4-mem-pinta.json`).
- verified-at: 2026-10-14 (this lane).
- suggested: admit + parent action: correct the `ev_4898906e…` citations.

## The Queue-B exercised-set ledger (rescan lines 191–206, current as of this lane)

Held = success path exercised in-corpus; each held row cites its holding entry
and this lane's spot-check. Open rows carry their provisioning gap. Line anchors
are the rescan's.

- **L195 `inspect-binary-layout` — HELD.** Holding: r4-13
  (`2026-10-13-r4-13-pwntools-persist.md` candidate 2, `ev_294a449c…` on jq;
  refusal datum for the non-x86-64 class in r4u-01 line 57). Spot-check:
  byte-identical re-run this lane (candidate 4a). Census note: the rescan's
  Queue-B header ("success path operator-gated; r5 can only re-confirm") was
  stale AT WRITE for this one row — r4-13 is wave 13, the census wave 16, and
  the census's exercised-set union (rescan lines 146–158) omits the verb: the
  sixth instance of the named row-7 class (census exercised-set blindness).
  Gap: none. Latent: venv `unicorn` import (not on this verb's path).
- **L196 `inspect-firmware-regions` — HELD.** Holding: r4u-01 (`ev_0388cb9a…`
  gsp_tu10x 56 regions; `ev_4009f834…` gsp_ga10x 156; verify line 19).
  Spot-check: 56 regions + `signature_scan` reproduced; per-run id class
  recorded (candidate 4d). Gap: none (`REA_BINWALK_COMMAND` ambient, binwalk
  3.1.0; nvidia-utils 610.57.04-1 unchanged, blobs re-pinned).
- **L197 `extract-firmware` — HELD.** Holding: r4u-03 (`ev_1d26a817…` ucodes
  empty; `ev_5c8a405e…`/`ev_82507d8e…` base-devel pkg; `ev_d33d8abb…`/
  `ev_b36536e5…` AppImage) + r4u-01 (`ev_305743ec…`/`ev_5964d108…`).
  Spot-check: ucodes re-run `complete`/`files:0` (candidate 4e). Gap: none
  (`REA_UNBLOB_COMMAND` ambient, unblob 26.6.4).
- **L198 `recover-javascript-sources` — HELD.** Holding: r4u-05
  (`ev_5cb1856a…` on `/tmp/wakaru-e2e/input.js`; fix = `REA_WAKARU_COMMAND`
  → the `@wakaru/cli-linux-x64` ELF; verify lines 95–97). Spot-check: e2e
  re-run exit 0 on the same held input (candidate 4f). Gap: none for small
  inputs (ELF binding ambient and re-verified: `file` → stripped ELF);
  `REA_JAVASCRIPT_PRLIMIT_COMMAND` still absent — large inputs keep the
  r4u-05 caveat. Citation defect: PROVINCE.md:117 / LOG.md:76 cite the
  phantom `ev_4898906e…` (candidate 4h).
- **L199 jadx family (6 verbs) — 4/6 HELD, 2 TRULY-OPEN, NO GAP.** Held:
  `inspect-android-package` (r3-06 120 nodes; r4u-02 `ev_d760cc5c…` debug /
  `ev_f05731d5…` release), `search-android-classes` (`ev_a89cefe1…`/
  `ev_edb28274…`), `inspect-android-class` (`ev_3dd12761…`),
  `inspect-android-method` (`ev_ec92f4d1…`). Open: **`trace-android-references`**
  (never invoked — only a docs claim, r2-skill-references-deep line 16) and
  **`project-android-application-graph`** (never invoked; named only as a
  frontier suggestion at r4u-02 candidate 2's close — distinct from the
  MANAGED projector this lane exercised). Gap: none — jar sha-continuity
  re-verified this lane, ~8 s/verb cost; these are the two cheapest open
  success paths in Queue B.
- **L200 — 1/2 HELD, 1 TRULY-OPEN, NO GAP.** `decode-android-resources` held
  (r4u-02 `ev_a78193a3…`; byte-identical re-derivation this lane).
  **`inspect-apktool-client`** open on success: only the r2 refusal datum
  (`capability_unavailable`/`unsupported_provider`,
  r2-provider-capability-matrix line 98); gate satisfied
  (`REA_APKTOOL_COMMAND=/usr/bin/apktool`, 3.0.3) — cheap-open.
- **L201 JEB family (4 verbs) — TRULY-OPEN, operator-gated.** Refusal datum:
  `inspect-jeb-client` `capability_unavailable`/"fetch failed" (r2 matrix line
  99; family doc r2-frontier-prereqs lines 116–139). Gap re-verified this
  lane: `REA_JEB_MCP_URL` UNSET, no JEB install, :8425 closed. Operator must
  start a JEB MCP client.
- **L202 adb surface (22 serial verbs) — TRULY-OPEN on success, device-gated.**
  The wall is fully typed (r4u-06: all 22 `unsupported_target`, three refusal
  shapes; the 2 serial-free verbs held — `inspect-adb-client` `ev_d850ccd0…`,
  `list-adb-devices` `ev_d4d8cc77…`, the latter byte-identical this lane).
  Gap: one device/emulator (adb 1.0.41 healthy, zero devices; emulator route
  heavy per r11-02).
- **L203 `compare-application-versions` success path — WAS TRULY-OPEN, NOW
  EXERCISED (this lane, both classes; candidates 1–3).** Prior state: r2
  refusal datum only + doc claims; the assignment's r4-10 defect-hunt check
  answered NEGATIVE (see header comment) — no defect close, a genuine drain.
  Residual open sub-class: the runtime-reconciliation input class
  (`reconcile_javascript_runtime` Evidence) — untested, needs a held reconcile
  evidence composed as input.
- **L204 `import-managed-reconstruction` — TRULY-OPEN, half-gated.** No corpus
  exercise. Real-decompiler route operator-gated (ilspy/dnSpy absent, no SDK);
  hand-crafted-JSON route self-provisionable since the r4-11 schema unlock —
  unchanged from the r11-02 recon, left to its owner row.
- **L205 ida provider (12 MCP ops) — TRULY-OPEN, operator-gated.** Gates
  re-verified: `REA_IDA_MCP_CONFIG` UNSET; provider `not_configured` (r2
  matrix line 64; r4-16 capabilities). 
- **L206 hopper provider (13 unique ops) — TRULY-OPEN, operator-gated.**
  `/opt/hopper/bin/Hopper` absent (re-verified); provider `executable_missing`
  (r2 matrix line 63).

Ledger verdict: **8 of 12 rows fully or partly held** (L195–L198 wholly;
L199 4/6; L200 1/2; L203 now wholly), **truly-open = 3 jadx/apktool verbs
with NO provisioning gap** (cheapest drain), 22 adb verbs (one device),
4 JEB + 12 ida + 13 hopper ops + L204's decompiler route (operator). The
census's Queue-B framing ("operator-gated; r5 can only re-confirm") was
right-at-write for L196–L200 (the r4u wave drained them after provisioning)
and wrong-at-write only for L195 (row-7 class, instance six).

## Evidence-id verifications (assignment requirement: at least one re-run — nine done)

Byte-identical re-derivations: `ev_7a8d0ec4…` (this lane's own L203 JS run, ×2),
`ev_b5fc998f…` (L203 managed run, ×2), `ev_294a449c…` (r4-13), `ev_a78193a3…`
(r4u-02), `ev_d4d8cc77…` (r4u-06), `ev_f382333b…` (r4/r10-01/r11-02 — fourth
confirmation), `ev_92faacb3…` (r10-01), `ev_4d2b732d…`+`magp_8d35cc89…` (r9-02,
ids byte-reproduced across rounds). Count-class re-derivations (per-run-id
families): firmware 56 regions (r4u-01), wakaru success shape (r4u-05).

## Run log

| # | command | rc | result |
|---|---|---|---|
| 1 | pins: sha256 of both obsidian evidences, Pinta DLLs, APK, blobs, jq, wakaru ELF+input, jadx jar (before) | 0 | `inputs.sha256.before`, `pinta.sha256.before` |
| 2 | `jq -r '.evidence_id,.operation'` both obsidian files | 0 | ids == r4-09's `ev_a29ab2a0…`/`ev_4c3202c9…` |
| 3 | `compare-application-versions --schema`; `{}` | 0/1 | `{inputJson}`; left/right missing_argument |
| 4 | `compare-application-versions cav-js.in.json` (39,119,964 B) | 0 | 3.3 s, `ev_7a8d0ec4…`/`javc_efb02d28…`, 10 changed/208 unknown |
| 5 | re-run + `cmp` | 0 | byte-identical |
| 6 | same-id probe (`cav-sameid.in.json`) | 1 | "Application version Evidence must be distinct" |
| 7 | `inspect-managed-members` Pinta.dll / Pinta.Effects.dll | 0 | `ev_f382333b…` (== r4 file), `ev_92faacb3…` (== r10-01) |
| 8 | `project-managed-application-graph` ×2 (`managed_members`) | 0 | `ev_4d2b732d…`/`magp_8d35cc89…` (== r9-02), `ev_35d2e7aa…`/`magp_32fd21a4…` |
| 9 | `compare-application-versions cav-mgd.in.json` ×2 | 0 | `ev_b5fc998f…`, `{unknown:4114}`, byte-identical |
| 10 | `decode-android-resources <debug.apk>` | 0 | `ev_a78193a3…` byte-identical |
| 11 | `inspect-binary-layout /usr/bin/jq` | 0 | `ev_294a449c…` byte-identical; subject digest == disk jq |
| 12 | `inspect-firmware-regions gsp_tu10x.bin` | 0 | 56 regions, `signature_scan`, per-run id |
| 13 | `extract-firmware ucodes_tu10x.bin <scratch out>` | 0 | `complete`, files:0 |
| 14 | `recover-javascript-sources /tmp/wakaru-e2e/input.js <scratch out>` | 0 | success; run-shaped id; `wakaru 1.14.0` |
| 15 | `list-adb-devices` | 0 | `ev_d4d8cc77…` byte-identical; daemon side-effect killed after |
| 16 | gate checks: env names, ports, /opt/hopper | — | JEB/IDA keys unset, :8425 closed, hopper absent |
| 17 | after-pins + `diff` vs before | 0 | all substrates unchanged |

Scratch (`/tmp/r12-02-scratch/`): `cav-js.{in,run1,run2}.json`,
`cav-sameid.{in,json}`, `cav-empty.json`, `cav.schema.json`,
`mem-{pinta,effects}.json`, `pmag-{pinta,effects}.{in,json}`,
`pmag-empty.json`, `pmag-pinta.probe1.{json,out}`, `cav-mgd.{in,json,run2.json}`,
spot-check outputs `ibl-jq.json`, `dar.json`, `lad.json`, `ifr-tu.json`,
`ef-tu.json`, `rjs.json` (+`.err`s), pins `inputs.sha256.before`,
`pinta.sha256.before`, `apk.sha256.before`, `jq.sha256.mid`,
`all.sha256.after`, `fw-ucodes-out/`, `wakaru-out/` (retained for
re-verification, r10-02 convention).

## Summary

L203 is discharged for real: the census's last compare-verb residue took two
held r4-09 obsidian evidences and returned this host's first genuine
application-version diff — 218 items over obsidian 1.12.7→1.13.7 with 10
changes, every one semantic-key-paired at medium confidence, added/removed
honestly zeroed by partial-graph coverage, byte-identical on re-run; the
managed-graph input class accepts Pinta projections and returns a disciplined
all-unknown on two different assemblies (4,114 items, zero guessed pairs), with
the r9-02 projection ids reproduced byte-exact en route. The defect-hunt
answer is negative: r4-10 held the native compare pipeline, never this verb.
The full Queue-B ledger classifies all 12 rows: L195–L198 wholly held (with
fresh byte-exact or count-exact re-derivations), L199 4/6 and L200 1/2 held,
L203 now held, leaving exactly three no-gap success verbs
(`trace-android-references`, `project-android-application-graph`,
`inspect-apktool-client`) as the cheapest drain, one device-gated family
(adb 22), and the operator-gated residue (JEB 4, ida 12, hopper 13, L204's
decompiler route). One citation defect for the parent: PROVINCE.md:117 and
LOG.md:76 cite `ev_4898906e…`, an id that exists nowhere in the corpus; the
real r4u-05 success id is `ev_5cb1856a…`. All substrates byte-identical
before/after; the single side-effect (adb daemon) killed and port-verified
closed; tree clean at write, HEAD `47d492a`.

## Addendum (post-write, 2026-10-14): sibling r12-01 landed mid-lane — L199/L200 "truly-open" rows superseded

This entry was written against a clean tree at `47d492a`; r12-01
(`2026-10-14-r12-01-queue-b-ready.md`, finished 06:39Z) landed afterwards
claiming rescan lines L195–L200. Its L195–L197 census-defect closes match
this ledger's independent classifications (including the byte-exact
`ev_294a449c…` and `ev_a78193a3…` re-derivations). Two ledger verdicts are
superseded by its live runs: L199's two open tail verbs are now exercised
(`trace-android-references` ×3: `ev_4093a663…`, `ev_123d8a6b…`,
`ev_f09ea5a2…`; `project-android-application-graph`: `ev_49d954f4…`/
`adp_d20f12ec…` — first Android application-graph projection on this
host), and L200's `inspect-apktool-client` holds its first success
(`ev_5dfddbf3…`). Its L195 one-fix correction stands: bare `setuptools`
84.0.0 no longer bundles `pkg_resources`; the pin is `setuptools<81`
(→ 80.10.2), proven in a disposable venv copy only. Queue B's remaining
open set after both lanes: L202's 22 adb verbs (device), L201 JEB ×4,
L205 ida ×12, L206 hopper ×13, L204's decompiler route (operator), and
L203's runtime-reconciliation input class. Zero row overlap with this
lane's L203 exercise.

## Errata (round-12 audit, 2026-10-14, append-only)

- **Ledger tally parenthetical**: "8 of 12 rows fully or partly held"
  enumerates only 7; the 8th partly-held row is L202 (its two serial-free
  verbs), described correctly in its own bullet but omitted from the
  parenthetical.
