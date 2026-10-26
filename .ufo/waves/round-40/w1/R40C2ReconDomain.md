# R40C2ReconDomain — C2 domain guard and out-of-domain class (round 40, wave 1)

**Verdict: CONFIRMED — and the routed defect R39-CL1 reproduces: the v1 interpreter labels every
out-of-domain envelope I could produce `no-squashfs-chunk`, on a feature vector that is *identical*
to the genuine in-domain `no-squashfs-chunk` envelope, so only the two domain-guard columns can
separate them. `inspect-firmware-regions` (provider `binwalk`) is the one real non-`extract_firmware`
operation that returns an `ok` envelope with a `normalized_result` on a bare SquashFS carrier, and its
decision features are stable across 3 trees × 2 endians (6/6).**

Seat bounds honoured: no REA/unblob run on any C1 carrier (V1/V2 or lane-built), no held-out carrier
built, REA/unblob only on fresh dev trees I authored plus round-39 receipts, writes only to this
report and `.ufo/waves/round-40/w1/artifacts/R40C2ReconDomain/`, no VCS mutation, no installs, no
pacman transaction, sasquatch/sasquatch-v4be/unblob untouched.

---

## 0. Environment and how to reproduce

Scratch `S=/fast/scratch/hyaku/kaidoku-r40/R40C2ReconDomain` (`TMPDIR`/`HYAKU_SCRATCH` exported,
`cd "$S"` before every REA run; scratch removed at the end of the seat — everything cited here is
copied into the artifacts dir or rebuildable from `build-dev-carriers.sh`).

Measured tool identities (recorded, not asserted from docs):

| tool | identity | how measured |
| --- | --- | --- |
| rea-agents | 6.5.0 (`npx -y rea-agents@6.5.0 --version`) | CLI |
| unblob | 26.6.4 (`$HOME/.local/bin/unblob --version`) | CLI; used only through `REA_UNBLOB_COMMAND` |
| binwalk | 3.1.0-1, `/usr/bin/binwalk`, sha256 `5fc19aac1f357a66a47e8b20a8038a84cb93971cb5d331bd4503b02fcc0a40d6` | `pacman -Qo`, `sha256sum`; REA's own `normalized_result.engine` block agrees |
| gen-squashfs.py | `tools/round-39/gen-squashfs.py` (`--endian le\|be\|avm --comp gzip\|xz`) | used for every dev carrier |
| sqfs-triage.py (v1) | `tools/round-39/sqfs-triage.py` + `SKILL.md` block 18 | all labels below |

**No tool was installed or upgraded** (nothing needed: binwalk, unblob, sasquatch, sasquatch-v4be
were already present). No pacman call of any kind.

Dev carriers (all fresh trees, `build-dev-carriers.sh`):

```sh
python3 tools/round-39/gen-squashfs.py tree/clean car-be-gzip.sqsh  --endian be  --comp gzip
python3 tools/round-39/gen-squashfs.py tree/clean car-le-gzip.sqsh  --endian le  --comp gzip
python3 tools/round-39/gen-squashfs.py tree/clean car-avm-gzip.sqsh --endian avm --comp gzip
# treedet/t1..t3 -> car-{1,2,3}-{be,le}.sqsh  (3 trees x 2 endians, for the determinism probe)
head -c 8192 /dev/urandom > blob-random.bin                     # in-domain no-squashfs-chunk contrast
(cd wrap && zip -q ../wrap-be.zip car-be-gzip.sqsh)             # second out-of-domain shape
```

sha256 of the carriers behind the committed envelopes: `artifacts/carriers.sha256`.
`build-dev-carriers.sh` rebuilds a *feature-equivalent* set deterministically (verified: two
independent runs of the `tree/clean --endian be --comp gzip` step both give
`78a078b6a587f4c416f5155545195e449012624a0569ac065bff54e2ce486058`); the committed envelopes came
from an earlier variant of the same trees with one `/dev/urandom` blob, so each envelope's own
`subject.digest.sha256` is authoritative for what it measured.

---

## 1. The whole REA 6.5.0 CLI surface

`npx -y rea-agents@6.5.0 --help` → **155 commands + 2 integrations** (`completions`, `mcp`), full
text saved as `artifacts/rea-6.5.0-commands.txt`. `capabilities --format json` reports
`data.open: false` (no deep-analysis provider configured) and four capability providers:
`native-macos` (unsupported on this host), `rea-artifact-graph` v1, `rea-dotnet-static` v1, `sqlite`.
Note that `unblob` and `binwalk` are *not* capability providers — they are extraction/inspection
engines recorded inside each envelope's `data.provider` / `normalized_result.engine`.

Surface split (from the help text, artifact above): 26 device/adb verbs, 28 process/web/runtime
verbs (need a live process, browser, CDP endpoint, JEB/Cutter/Frida session), 68 path-taking verbs,
27 JSON/Evidence verbs, 6 misc. Only the path-taking group can be pointed at a firmware blob.

---

## 2. Every path-taking operation I ran on a dev SquashFS carrier (BE and LE, plus BE-only extensions)

**33 distinct operations, 77 envelopes.** Every run is tabulated in `artifacts/features.tsv`
(17 columns: `ok`, `operation`, `provider_id`/`provider_version`, `handler:extraction_failed` pairs,
gap kinds, dependencies, unpublished kinds, diagnostic `__typename__`s, the recorded sasquatch argv,
published-file count, which `normalized_result` keys exist, error code, and the v1 verdict + exit),
and every envelope is committed gzipped under `artifacts/dev-envelopes/` (312 KB in total).

Result, in one line: **exactly one operation returns an `ok` envelope with `normalized_result` on a
bare SquashFS carrier besides `extract-firmware`:**

| operation (`data.operation`) | provider | exit | `ok` | `normalized_result` | chunks | extraction_gaps | files |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `extract_firmware` (in-domain) | `unblob` 26.6.4 | 0 | true | present (13 keys) | **yes** | **yes** | **yes** |
| `inspect_firmware_regions` | `binwalk` 3.1.0 | 0 | true | present (4 keys) | **no** | **no** | **no** |
| `inspect_artifact` on `wrap-be.zip` | `rea-artifact-graph` 1 | 0 | true | present (11 keys) | **no** | **no** | **no** |
| the other 31 operations on a bare carrier (list below) | — | **1** | false | **absent** | — | — | — |

The 31 format-gated operations — 21 of them run on **both** carriers, 10 more on BE only — each
`ok:false` with `data` absent: `inspect-artifact`, `extract-artifact`, `inspect-binary-layout`,
`analyze`, `inspect`, `inspect-go-binary`, `inspect-rust-binary`, `inspect-wasm-artifact`,
`inspect-plist`, `inspect-sqlite-database`, `inspect-managed-artifact`, `inspect-managed-members`,
`inspect-managed-native-boundaries`, `inspect-native-dispatch-metadata`, `inspect-native-load-image`,
`inspect-pe-resources`, `inspect-macho`, `inspect-signature`, `list-architectures`,
`inspect-dart-aot`, `inspect-electron-fuses`, `inspect-electron-page`, `inspect-evm-interface`,
`inspect-keyed-archive`, `inspect-asset-catalog`, `inspect-pcap-capture`, `inspect-recorded-crash`,
`decode-android-resources`, `decode-interface-builder`, `identify-flutter-build`, `demangle-swift`.
30 of them never produce an `ok` envelope in any shape I tried; `inspect-artifact` does once the
carrier is wrapped. Error codes over the 54 failing runs: `target_unavailable` 26,
`unsupported_target` 8, `invalid_request` 12, `capability_unavailable` 4, `VALIDATION_ERROR` 4 — the
last is the only non-kebab code I saw (`inspect-evm-interface`, `demangle-swift`,
`inspect-electron-page`), worth knowing for anything that switches on error codes; the LE carrier
reproduced the BE code for every one of the 21 operations.

Representative failure envelopes committed: `fail__inspect-artifact__car-be-gzip`,
`fail__inspect-binary-layout__car-be-gzip`, `fail__analyze__car-be-gzip`,
`fail__inspect-evm-interface__car-be-gzip`.

**Skipped, with reason (not measured):** verbs that need an open analysis session/address
(`decompile`, `function`, `instructions`, `search`, `search-bytes`, `read-bytes`, `trace`, `xrefs`,
`address-to-file-offset`, `annotate-native-function`) — no rizin/analysis DB is available
(`capabilities.open == false`); device/browser/runtime verbs (adb family, `capture-*`, `observe-*`,
`list-*-targets`, `debug-*`, `open-jeb-project`, `decompile-jeb-item`, `instrument-with-frida`) —
they take a device/process/endpoint, not a file; `evidence-*`/`compare*`/`project-*`/`inspect-*-`
`application-graph` verbs — they take a JSON/Evidence path, not a firmware carrier.

---

## 3. Envelope shapes, field by field (what a v2 table may key on)

`extract_firmware` → `normalized_result` keys: `engine, selection, output_directory, coverage, files,
unpublished_entries, chunks, derivations, depth_limited_paths, diagnostics, extraction_gaps,
extraction_continuations, published_bytes`. `data.provider` = `{"id":"unblob","name":"Unblob",
"version":"26.6.4"}`; `data.operation` = `extract_firmware`.

`inspect_firmware_regions` → `normalized_result` keys: `engine, input_size, regions, coverage`
(`coverage: "signature_scan"`). `data.provider` = `{"id":"binwalk","name":"Binwalk","version":
"3.1.0"}`; `data.operation` = `inspect_firmware_regions`. A region looks like

```json
{"provider_id": "59b234e9-6214-4352-b87a-19c3ec304543", "offset": 0, "reported_size": 4524,
 "signature": "squashfs", "description": "SquashFS file system, big endian, version: 4.0,
 compression: gzip, inode count: 6, block size: 4096, image size: 4524 bytes,
 created: 2023-11-14 22:13:20", "reported_confidence": 250,
 "size_basis": "provider_reported_validation_unknown"}
```

`inspect_artifact` (zip-wrapped carrier) → `normalized_result` keys: `inspection_id, subject,
substeps, observations, hypotheses, contradictions, unexplored_branches, next_probes, coverage,
evidence_links, limitations`; `data.provider.id` = `rea-artifact-graph`.

**Three field traps, all measured:**

1. `normalized_result.regions[].provider_id` is a **per-run UUID** (binwalk's own file-map id), not a
   provider. The provider guard must read `data.provider.id`. Two runs on the same carrier differ
   here (`59b234e9…` vs `c9955f16…`).
2. `meta.command` is the **CLI verb** (`inspect-firmware-regions`, kebab-case); the envelope's
   `data.operation` is snake_case (`inspect_firmware_regions`). A table cell must use the snake_case
   field — recommend the frozen claim text say `non-extract_firmware REA operation (`data.operation`)`
   instead of the current "non-`extract-firmware` REA operation", which names the CLI verb.
3. `inspect_firmware_regions` **names a squashfs signature** in `regions[].signature` and still has no
   `chunks`. That makes it adversarial in the right way: a table keyed on "the envelope says
   squashfs" instead of on `operation`/`provider` will misfire.

---

## 4. What v1 does with these envelopes — a false in-domain label, on an identical feature vector

`python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md --json <env>`:

| envelope | v1 features (H, G, D, BE, SR, P) | v1 label | row |
| --- | --- | --- | --- |
| `extract-firmware` on random 8 KiB (`ef-none`) | `[], [], [], n/a, no, 0` | `no-squashfs-chunk` | 1 |
| `inspect-firmware-regions` on BE carrier (`ifr-be`) | `[], [], [], n/a, no, 0` | **`no-squashfs-chunk`** | 1 |
| `inspect-firmware-regions` on LE carrier (`ifr-le`) | `[], [], [], n/a, no, 0` | **`no-squashfs-chunk`** | 1 |
| `inspect-firmware-regions` × 6 (3 trees × 2 endians) | `[], [], [], n/a, no, 0` | **`no-squashfs-chunk`** | 1 |
| `inspect-artifact` on `wrap-be.zip` | `[], [], [], n/a, no, 0` | **`no-squashfs-chunk`** | 1 |
| the 31 format-gated operations | — (no `normalized_result`) | **exit 2**, `no normalized_result …` | — |

So R39-CL1's defect is exactly one row wide: every `ok` envelope that carries no squashfs chunk lands
on row 1 (`handler: none`, everything else `*`), whatever produced it. The features are *byte-for-byte
the same set* as the legitimate in-domain `no-squashfs-chunk` case, which is why no v1 column can be
invented to fix this — only `operation` + `provider` can, exactly as claimed.

Same-carrier contrast pair (strongest demonstration, both committed):

| envelope | `subject.digest.sha256` | operation | provider | v1 label | v2 prototype label/action |
| --- | --- | --- | --- | --- | --- |
| `extract-firmware__car-be-gzip` | `ab58844f84ab593f…` | `extract_firmware` | `unblob` | `clean` | `clean` / `compare-oracle` |
| `inspect-firmware-regions__car-be-gzip` | `ab58844f84ab593f…` | `inspect_firmware_regions` | `binwalk` | **`no-squashfs-chunk`** | `unclassified` / `none` |
| `extract-firmware__car-le-gzip` | `de0892772c976c7d…` | `extract_firmware` | `unblob` | `clean` | `clean` / `compare-oracle` |
| `inspect-firmware-regions__car-le-gzip` | `de0892772c976c7d…` | `inspect_firmware_regions` | `binwalk` | **`no-squashfs-chunk`** | `unclassified` / `none` |

---

## 5. Determinism of the out-of-domain envelope

Three independently authored trees × two endians, `inspect-firmware-regions`, all exit 0:

```
env/det/ifr-1-be.json  op=inspect_firmware_regions pv=binwalk H=0 G=0 D=0 P=0 regions=1 engine=3.1.0
env/det/ifr-1-le.json  ... identical ...
env/det/ifr-2-be.json  ... identical ...
env/det/ifr-2-le.json  ... identical ...
env/det/ifr-3-be.json  ... identical ...
env/det/ifr-3-le.json  ... identical ...
```

Decision projection (what a table reads) is constant: `data.operation`, `data.provider.id`, empty
`chunks`/`extraction_gaps`/`files`. Non-decision fields that vary between replicates: endianness and
inode count inside `regions[].description` (`big endian` vs `little endian`), `input_size`,
`regions[].offset/reported_size`, tree shape. That satisfies the claim's "two replicates differ in a
non-decision feature" with room to spare.

**What is NOT stable, and must never be digested** (diff of two runs on the *same* carrier):

```
/data/evidence_id                                     ev_b156fe2f… vs ev_f950c900…
/data/normalized_result/regions[0]/provider_id        59b234e9-… vs c9955f16-…   (binwalk file-map UUID)
/data/raw_result/execution/args[5]                    /tmp/rea-firmware-NgEyOs/report.json vs …/VnYK4s/…
/data/raw_result/execution/args[6]                    /tmp/rea-firmware-NgEyOs/firmware.bin vs …
/data/raw_result/report[0]/Analysis/file_map[0]/id    (same UUID)
/data/raw_result/report[0]/Analysis/file_path         /tmp/rea-firmware-NgEyOs/firmware.bin vs …
/meta/duration                                        398ms vs 362ms
```

Everything else — `subject.digest`, `operation`, `provider`, `regions[].signature/offset/
reported_size/description/reported_confidence/size_basis`, `engine`, `coverage` — was byte-identical.
So the v2 counter must digest *carriers* and compare *(label, action)*, never envelope bytes. (The v1
`--selftest` fixture set is unaffected; this is a C2 counter/generator constraint.)

`inspect-firmware-regions` does not need `REA_UNBLOB_COMMAND`: with the variable unset the envelope's
features were identical (`inspect-firmware-regions__car-be-gzip__no-unblob-env`). It is also
independent of PATH for locating binwalk — I built a symlink PATH of 3753 `/usr/bin` entries with
every `binwalk*` name excluded and REA still recorded `engine.executable_path = /usr/bin/binwalk`,
same sha256 (`…__path-without-binwalk`). Mechanism unverified [INFERENCE: REA resolves well-known
absolute prefixes or a cached tool path]. Practical reading: the class needs `binwalk` present on the
host that regenerates it, and its identity is pinned in the envelope.

---

## 6. Recommended out-of-domain generator recipe (deterministic, stable, cheap)

**Recipe `out-of-domain`:**

* carrier: an ordinary fresh clean tree → `gen-squashfs.py … --endian {be,le} --comp gzip`
  (replicate A `be`, replicate B `le`; the endian only moves `regions[].description`, a non-decision
  field);
* operation: **`rea inspect-firmware-regions --format json --full-output <carrier>`** (no output
  directory, no `REA_UNBLOB_COMMAND`, no PATH arm);
* expected outcome, assigned *before* any run: label **`unclassified`**, action **`none`**;
* measured stability: 6/6 across 3 trees × 2 endians; every replicate exit 0 with `ok:true`;
* measured v1 behaviour on all six: `no-squashfs-chunk` — i.e. the class is a real discriminator
  against the v1 table and against any v2 table that leaves the domain cells `*`.

Why this and not something else: it is the only non-`extract_firmware` operation REA 6.5.0 offers
that returns `ok:true` with a `normalized_result` on a *bare* SquashFS carrier (33 operations tried,
§2). `inspect-artifact` needs the carrier wrapped (zip/tar), which changes the class definition, and
it is the recommended *secondary* probe if the L1 wants a second shape (measured: same false v1
label, provider `rea-artifact-graph`, input `wrap-be.zip`, envelope
`inspect-artifact__wrap-be.zip`).

Optional but recommended as a **kill control, not a held-out class**: run the same operation on the
*same carrier bytes* an in-domain class already uses (I did: `ab58844f…` gets `clean` under
`extract-firmware` and `unclassified` under `inspect-firmware-regions`). Identical subject, different
verdict — it isolates the guard from every other variable.

---

## 7. v2 grammar: prototype implemented and validated (advisory, for the L1)

Artifacts: `sqfs-triage-v2-proto.py` (13-case `--selftest`, 13/13 green) and `v2-table-proto.md`
(the proposed 11-row block, parsed and classified end to end). The prototype implements the draft
grammar as written: craft-section bounds, marker, first table after the marker, exact 12-column
header, actions vocabulary line directly above the header, first-full-match, unique labels, closed
action vocabulary, `.ufo`-style exit 2 on every malformation, features `OP/PV/H/G/D/BE/SR/P` with
H/G/D/BE/SR/P unchanged from v1.

Measured with the proposed table (`skill-proto.md` built from `v2-table-proto.md`):

| envelope | v1 label | v2 label | v2 action |
| --- | --- | --- | --- |
| `extract-firmware__car-be-gzip` | `clean` | `clean` | `compare-oracle` |
| `extract-firmware__car-le-gzip` | `clean` | `clean` | `compare-oracle` |
| `extract-firmware__car-avm-gzip` | `avm-marker-be-dropped` | `avm-marker-be-dropped` | `rerun-with-be` |
| `extract-firmware__blob-random` | `no-squashfs-chunk` | `no-squashfs-chunk` | `check-superblock` |
| `inspect-firmware-regions__car-be-gzip` (+LE, +6 det, +run2) | `no-squashfs-chunk` | **`unclassified`** | `none` |
| `inspect-artifact__wrap-be.zip` | `no-squashfs-chunk` | **`unclassified`** | `none` |
| round-39 `K1/after.json` | `escaping-symlink-removed` | `escaping-symlink-removed` | `expect-absent` |
| round-39 `K2/after.json` | `in-tree-symlink-metadata` | `in-tree-symlink-metadata` | `expect-absent` |

**Kill controls verified by execution:**

1. **v1 transcribed into v2 with `*` domain cells** (`sed -e 's/| \`extract_firmware\` | \`unblob\` |/| \`*\` | \`*\` |/g'`,
   11 rows rewritten): `inspect-firmware-regions` BE, LE and the zip envelope all become
   `no-squashfs-chunk` → the control is discriminating and the guard columns are load-bearing.
2. **operation swapped to `extract_firmware`, provider left `binwalk`** (synthetic: no real
   non-unblob `extract_firmware` envelope exists) → `unclassified`. This is the *only* way to
   exercise the provider column; without it the column is unexercised by real data.
3. **provider swapped to `unblob`, operation left `inspect_firmware_regions`** (synthetic) →
   `unclassified`.
4. selftest malformations: duplicate label, unreserved action token, missing actions line, malformed
   `published files` cell, absent marker, no-match fall-through, bare-vs-full envelope, error envelope
   (exit 2) — all 13 cases green.

### Six grammar points I recommend freezing (each measured or forced by a measurement)

1. **Reserve the label `unclassified`.** The draft says "no match -> (`unclassified`, `none`)" but does
   not forbid a row *named* `unclassified`; a catch-all row labelled `unclassified` would pass every
   label comparison while decision-matching the whole set. My prototype rejects it (exit 2,
   `label 'unclassified' is reserved…`, selftest `c_reserved_label`). Freeze the sentence.
2. **Spell out the actions-line adjacency.** My selftest hit a real ordering trap: with the v2 marker
   placed immediately above the header, the actions line cannot also be "directly above the table".
   Freeze: marker anywhere in the block, actions line directly above the header separated by blank
   lines only, and *nothing else* between them (`parse_actions` errors say which line failed).
3. **Name the fields.** `OP = data.operation` (snake_case), `PV = data.provider.id`; explicitly *not*
   `meta.command` and *not* `normalized_result.regions[].provider_id` (a per-run UUID).
4. **Error envelopes stay exit 2.** An `{ok:false,…}` envelope has no `data`, hence no
   `normalized_result`; v1 already exits 2 and the prototype keeps that. Consequence for the claim:
   every held-out envelope must be an `ok` envelope, so no class may be defined by a failing verb
   (`inspect-artifact` on a bare carrier is *not* usable as the out-of-domain class for this reason).
5. **`action` for the no-match outcome.** `none` may also be a real vocabulary token (my table uses it
   for `clean-empty`); uniqueness comes from the `(unclassified, none)` *pair*. Freeze the pair, and
   keep the vocabulary line mandatory (a missing line is exit 2, not an empty vocabulary).
6. **Provider amplitude is one value right now.** With `capabilities.open == false` and every
   `extract_firmware` run reporting `unblob`, no real envelope can pair `extract_firmware` with another
   provider; the provider column is a fail-closed guard plus a synthetic control, not something real
   data exercises. Say so in the frozen text so the coverage claim is not overstated.

---

## 8. Integration notes for the L1 (heldout-gen v2 / counter)

* `tools/round-39/heldout-gen.py` hardcodes the verb at `run_rea()` (`cmd = ['npx','-y',REA_PACKAGE,
  'extract-firmware','--format','json','--full-output',carrier,outdir]`) and every `RECIPES` entry
  assumes an output directory. An `out-of-domain` recipe needs a per-class argv override:
  `operation` (no outdir) vs `extract` (with outdir), and `record['rea_argv']` must show the verb.
  `rea_env(arm)` can be reused unchanged; the PATH arm is irrelevant for `inspect-firmware-regions`
  (measured above).
* `manifest.json` (round-39 shape) carries `label` only; v2 needs `action` too, since the counter
  scores the pair. The class must also record that no `carrier`-derived `oracle` applies (binwalk
  extracts nothing) — `tree.json` currently always writes an `oracle`.
* The counter must compare *carriers* (subject sha256) and *(label, action)*; envelope bytes are not
  reproducible (§5 four moving fields).
* Reserve the extra guard: the counter's "best table + catch-all" control needs both the star-domain
  control (measured to fail correctly) and the reserved-label rule (point 1 above), otherwise a
  catch-all row labelled `unclassified` is indistinguishable from the no-match outcome.
* `heldout-gen.py`'s class list needs the new class appended (never inserted ahead of the existing
  ten) if the RNG stream per class is to stay reproducible — `class_index = list(RECIPES).index(name)`
  feeds the seed (`rng = Random(int(seed[:16],16) ^ (class_index*1000+k))`), so inserting anywhere but
  the end re-seeds every later class.

---

## 9. Limits, risks, open items

* **The measured out-of-domain surface is one operation wide.** Across 33 path-taking operations, only
  `inspect_firmware_regions` (and `inspect_artifact` on a wrapped carrier) can produce an `ok`
  envelope on SquashFS input. No real envelope from a non-`extract_firmware` operation carries
  `normalized_result.chunks` at all, so the guard's behaviour on *chunk-carrying* out-of-domain
  envelopes is untestable from real data — cover it with the synthetic operation/provider swaps
  (§7) and say so in the claim rather than implying real coverage.
* **binwalk is a host dependency of the class.** `/usr/bin/binwalk` (pacman `binwalk 3.1.0-1`,
  sha256 `5fc19aac…`) must exist on the host that regenerates the held-out envelope; REA records that
  absolute path. I could not test absence (removing/moving tools is out of bounds, pacman is paused).
* **Device/runtime/JSON verbs were not exercised** (§2 skip list): with `capabilities.open == false`
  they cannot run here. That is a bounded, stated gap, not an assumption.
* **Envelope-level noise** (evidence id, binwalk region UUID, temp paths, duration) forbids
  byte-digesting envelopes; the claim already asks for carriers + a semantic projection — this report
  supplies the exact field list to exclude.
* No C1 data was read into this analysis beyond citing nothing: C1 carriers were never opened by REA
  or unblob here; probe carriers were fresh dev trees plus committed round-39 receipts (interpreter
  reads only).
* `inspect-artifact` on the zip is a *wrapped* carrier: if the L1 prefers it over
  `inspect-firmware-regions` (no binwalk dependency, in-process provider `rea-artifact-graph`), the
  frozen class definition ("a non-`extract_firmware` REA operation on a SquashFS carrier") has to be
  amended to "…on a carrier containing a SquashFS member". Both were measured; my recommendation is
  `inspect-firmware-regions` on the bare carrier, as claimed.

---

## 10. Artifact index (`/.ufo/waves/round-40/w1/artifacts/R40C2ReconDomain/`)

| file | what it is |
| --- | --- |
| `features.tsv` | one row per committed envelope (77): ok, operation, provider id/version, `handler:extraction_failed` pairs, gap kinds, dependencies, unpublished kinds, diagnostic `__typename__`s, recorded sasquatch argv, published-file count, which `normalized_result` keys exist, error code, v1 label + v1 exit |
| `carriers.sha256` | sha256 of every dev carrier and wrapper behind the committed envelopes |
| `build-dev-carriers.sh` | rebuilds the carrier set (deterministic, `sh -n` clean, verified twice) |
| `dev-envelopes/*.json.gz` | the cited envelopes: `extract-firmware__*` (4), `inspect-firmware-regions__*` (9, incl. 6 determinism + run2 + no-unblob + no-binwalk-in-PATH), `inspect-artifact__wrap-be.zip`, `fail__*` (4), two synthetic single-cell controls, `rea-capabilities` |
| `dev-envelopes/probe/*.json.gz` | the 54 format-gated envelopes (21 ops × 2 carriers + 12 extra ops on BE) |
| `rea-6.5.0-commands.txt` | full `--help` text of the 155-command surface |
| `recon-log.txt` | captured transcript: versions, v1 labels, v2 prototype labels, selftest, all kill controls, determinism table, two-run diff |
| `sqfs-triage-v2-proto.py` | v2 grammar prototype, `--selftest` 13/13 |
| `v2-table-proto.md` | proposed 11-row block + the identical-feature evidence table |
| `skill-proto.md.gz` | SKILL-shaped fixture built from `v2-table-proto.md` (gunzip to run the prototype against it; verified: `inspect-firmware-regions__car-be-gzip` → `unclassified/none`, `extract-firmware__car-be-gzip` → `clean/compare-oracle`) |
