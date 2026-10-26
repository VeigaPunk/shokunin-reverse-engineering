# R40C1Harness — R40-C1 run harness (`c1-run.sh`) + carrier manifest emitter (`mk-carriers.py`)

**VERDICT: DONE** — both tools are written, exercised with the round-40 reader, REA 6.5.0 and
unblob 26.6.4 on development inputs only, and covered by a **111/111 green** selftest. Nothing was
frozen; no C1 carrier and no C2 held-out envelope was touched. One measured constraint for the
freeze is reported in §6 (REA staging budget on members that nest a large filesystem image).

Claim item: R40-C1 (coverage) — pre-freeze tooling. Receipt generation for the frozen carriers and
`carriers.json` are L1 work; this seat supplies the two tools and the receipts that prove them.

---

## 1. Axes (Godspeed)

| axis | what moves here |
|---|---|
| **coverage** | the C1 receipt producer is now deterministic and self-checking: one command writes the REA `data` object the counter reads, plus the independent oracle tables and a cross-tool agreement check that must pass before a carrier can be frozen. |
| **depth** | the oracle arm validates the frozen table grammar (closed kind vocabulary, sorted unique relpaths, no file/non-regular path overlap) and refuses a carrier whose independent reader and `sasquatch-v4be` disagree; the after arm surfaces the structured reason of a failed REA envelope instead of only its digest. |

## 2. Deliverables (all under `.ufo/waves/round-40/w1/artifacts/R40C1Harness/`)

| file | sha256 | role |
|---|---|---|
| `c1-run.sh` | `e2f93216e472e968129358a60def1ed327105b53deb9c703960186f31862d80f` | run harness, `after` / `oracle`; **copy to `tools/round-40/c1-run.sh`** |
| `mk-carriers.py` | `f4abdfb8a0e912b599d37c640adf8acde3c7e6076748503a5543ad14003f8448` | emits `.ufo/waves/round-40/c1/carriers.json`; **copy to `tools/round-40/mk-carriers.py`** |
| `selftest.sh` | `c76948af5f6897b30ba0aee9a3c9512267ec9b07e9589d789ed056cbe06e68dc` | 111-case selftest (evidence, not a frozen path) |
| `test-double-sqfs-list.py` | `7c1a36763122c749aa2a13b2e6cfb33784f90ffae536c4677f46c8ff79ddd524` | **test double only** (sasquatch-backed reader stand-in); never freeze, never cite as the oracle |
| `selftest-tally.json` | `a766539ef31dc066fb468b2d35e6968bd0109c682600d1cf94fd747684b38a3f` | 111 cases, 111 passed, reader sha recorded |
| `receipts/…` | see §5 | after/oracle receipts, dev manifest samples, vendor-member evidence |

Integration (L1): `c1-run.sh` and `mk-carriers.py` go next to the frozen reader in `tools/round-40/`.
`mk-carriers.py` defaults to `sqfs-list.py` in **its own directory**; `c1-run.sh oracle` defaults to
`sqfs-list.py` in its own directory too (`C1_READER` overrides both for development).

No tool was installed or upgraded. Versions used: rea-agents **6.5.0**
(`/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`), unblob **26.6.4**
(`/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, sha256 `0ce7b624…cba1d09`),
`sasquatch-v4be` **4.5.1** (`/home/vgpnk/.local/bin/sasquatch-v4be`, sha256 `fac88740…b7214c6`),
round-40 reader sha256 `1079fa9b36a87e62b2de8ca594cfc0820e52b3450199076d9d7cc2e870353cd9`,
round-40 writer sha256 `309c502d21dfeef9b7b2a5a9a62bfa875270fdf79eec671461070996d291042e`.

## 3. Interfaces

### 3.1 `c1-run.sh after CARRIER OUTDIR [SCRATCH]`

Runs exactly (cwd = `$SCRATCH`, `TMPDIR=$SCRATCH`):

```
REA_UNBLOB_COMMAND=<default $HOME/.local/bin/unblob> \
  npx -y rea-agents@6.5.0 extract-firmware --format json --full-output CARRIER $SCRATCH/extract
```

* Writes `OUTDIR/after.json` = the envelope's **`data` object**, only when REA exits 0 with
  `ok=true` (the counter's required fields `operation`, `provider.id`, `subject.digest.sha256`,
  `parameters.output_directory`, `normalized_result.chunks[handler=squashfs_v4_be,
  extraction_failed=false]` all verified present on a real receipt, §5).
* Writes `OUTDIR/run.json`: schema `kaidoku-r40-c1-run-v1`, claim `R40-C1`, carrier
  path/sha256/size + big-endian superblock summary (`mkfs_time`, `bytes_used`, `avm_marker`),
  argv (array + shell), cwd, UTC start/end/duration, REA/unblob/sasquatch-v4be pins, envelope
  digest/size and — new in round 40 — `envelope.error` (the structured REA failure reason),
  receipt digest/evidence id, previous `after.json` digest.
* Preconditions (exit 2, no REA call): `npx`; `REA_UNBLOB_COMMAND` executable; `sasquatch-v4be`
  resolvable on the inherited PATH. `C1_KEEP_ENVELOPE=1` also stores the raw envelope.
* The **scratch (hence REA's `output_directory`, which is hashed into the evidence id) must contain
  a `/kaidoku-r40/` segment**; default scratch is `$HYAKU_SCRATCH/kaidoku-r40/c1-run.XXXXXX`.
  `C1_ALLOW_FOREIGN_SCRATCH=1` downgrades this to a warning and records
  `run_provenance_segment_ok:false` (development only). The third argument OUTDIR is not required
  to sit under `/kaidoku-r40/`: it is the evidence directory (`corpus/evidence/round-40/c1/<id>/`),
  while the segment clause is about the extraction root the receipt records. Scratch is removed on
  exit (including on failure).

### 3.2 `c1-run.sh oracle CARRIER OUTDIR [SCRATCH]`

Two independent producers, one frozen grammar:

1. **Independent reader** — `python3 -I sqfs-list.py --layout avm --files … --nonregular …
   --inspect CARRIER`. The harness first requires the reader's `--help` to advertise `--layout`,
   `--files` and `--nonregular` (exit 2 otherwise, so a changed reader CLI cannot silently pass).
   * `OUTDIR/oracle.tsv` — `relpath \t sha256 \t size` (regular files, bytewise-sorted).
   * `OUTDIR/nonregular.tsv` — `relpath \t kind \t detail`; kind closed vocabulary
     `dir|symlink|char-device|block-device|fifo|socket`; detail = link target / `major:minor` /
     empty. The harness **validates** both tables (3 fields, 64-hex sha, sorted unique relpaths,
     closed kind vocabulary, device detail `major:minor`, no path listed in both tables) before
     publishing them, so a malformed or unsorted table cannot be frozen.
2. **Cross-check extractor** — `sasquatch-v4be -f -no-exit-code -n [-o OFFSET] -d $SCRATCH/root
   CARRIER`, i.e. **no `-be`** (the AVM argv unblob 26.6.4 picks when
   `mkfs_time == bytes_used`). `-no-exit-code` is what unblob passes; an unprivileged run cannot
   create device nodes and that must not turn a complete regular-file extraction into a failure.
   The regular-file/sha256/size comparison is the real gate. `OUTDIR/oracle-check.tsv` uses the
   same grammar as `oracle.tsv`.

`OUTDIR/oracle-run.json` records both argv, both exit codes, reader/sasquatch pins, output digests,
table counts by kind, the cross-check verdict plus the first 20 mismatches (count is total), and
the reader's `--inspect` JSON. Exit: 0 only when reader exit 0, tables valid, `sasquatch-v4be`
exit 0 and **files_equal true**; 2 for usage/environment (including a `hsqs` carrier — this arm is
for AVM-layout BE images only); 3 for any tool failure/mismatch. The reader is run on a carrier
starting at offset 0; a leading-bytes carrier is located by magic and the offset is passed to
sasquatch (`squashfs_offset`, `-o`), but the reader itself must start at the magic.

### 3.3 `mk-carriers.py --root LANE --spec tuples.tsv | ID CARRIER ORACLE NONREGULAR …`

Emits `.ufo/waves/round-40/c1/carriers.json` (schema `kaidoku-r40-c1-carriers-v1`). Per carrier:
`id`, `layout:"avm"`, `magic`, `avm_marker`, `mkfs_time`, `bytes_used`, `path`, `sha256`,
`size_bytes`, `oracle`, `oracle_sha256`, `oracle_files`, `nonregular`, `nonregular_sha256`,
`nonregular_entries`, `nonregular_by_kind`, `receipt`
(`corpus/evidence/round-40/c1/<id>/after.json`). Paths are lane-relative.

Hard gates (all data, no REA):

* exactly ids **V1,V2,L1,L2 in that order** with distinct pins (the counter's frozen set; the
  manifest is emitted in that order). `--allow-any-ids` / `--ids` exist for development manifests
  only — a wrong set is exit 2.
* `sqsh` magic (`--magic be` default), `bytes_used` plausible (`0 < bytes_used <= file size`), and
  the **AVM marker** `mkfs_time == bytes_used` required (`--no-require-marker` is a negative-fixture
  escape only).
* both tables grammar-validated as above, no path overlap, bytewise-sorted unique relpaths.
* **`--layout-check reader` (default)** re-reads every carrier with the frozen reader under
  `--layout avm` and requires the regenerated oracle **and** nonregular rows to equal the supplied
  files exactly. This is the gate that rejects a marker-only standard-BE body
  (`gen-squashfs.py --endian avm`): it carries the marker but the reader's AVM walk — and the
  `sasquatch-v4be` no-`-be` cross-check — refuse it. `--layout-check off` is for development.
* `--out` defaults to `.ufo/waves/round-40/c1/carriers.json`; temp dirs honour `TMPDIR`.

## 4. What the selftest covers (111 cases; receipts in `receipts/`)

Run: `SELFTEST_KEEP=1 ./selftest.sh` → exit 0, `{cases:111, passed:111, failed:0}`; stderr empty.

* **Usage/env (13):** no args, bad mode, wrong arity, missing/unreadable carrier, foreign scratch
  refused, missing reader, reader without the three ADVERTISED flags, LE carrier refused, no magic,
  sasquatch-v4be absent from PATH, missing unblob.
* **Oracle arm (39):** genuine AVM-BE 4-file fixture, lane-built genuine AVM-layout gzip and xz,
  multiblock; cross-check equal every time; `-be` absent from argv; offset carrier found and `-o`
  passed; standard-BE K1 and marker-only `--endian avm` both exit 3 (no AVM layout); reader exit 1;
  malformed tables; missing oracle; non-JSON `--inspect`; cross-check sha disagreement (reported
  `mismatch_count:1`); foreign scratch allowed with `run_provenance_segment_ok:false`; default
  scratch segment true.
* **After arm (21, three real REA runs):** AVM-BE fixture → `squashfs_v4_be`, 4 files, 0 gaps,
  marker true, subject digest == pin, `parameters.output_directory` contains `/kaidoku-r40/`,
  `envelope.error:null`; standard-BE K1 → 5 files, marker false; `C1_KEEP_ENVELOPE=1` envelope kept
  and valid.
* **mk-carriers (38):** reader-mode manifest, record correctness, reader-mode == off-mode bytes,
  markerless refused, `--no-require-marker` allowed, LE refused, duplicate id/path, no carriers,
  missing oracle, path outside root, 2-field/unsorted/bad-sha oracle, bad kind, empty symlink
  target, file/non-regular path clash, frozen-table-vs-reader mismatch, `--spec` file, canonical
  V1,V2,L1,L2 emission, wrong-id set and missing-id refusals, two-carrier sort, byte determinism.

## 5. Measured evidence (exact commands, outputs, exit codes)

Scratch root in these receipts is `/fast/scratch/hyaku/kaidoku-r40/…` (removed at exit; receipts
copied here).

**a. Genuine AVM-BE dev fixture** — `/home/vgpnk/Projects/shokuknow/lanes/kaidoku/round11/work/avm-be.squashfs`,
sha256 `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32` (read-only source, copied):

```
C1_READER=…/R40C1Reader/sqfs-list.py ./c1-run.sh oracle fx/avm-dev.squashfs out/oracle-avm-dev
  exit 0; oracle_files=4; nonregular_entries=0; crosscheck.files_equal=true; check_files=4
REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob ./c1-run.sh after fx/avm-dev.squashfs out/after-avm
  exit 0; handler=squashfs_v4_be; files=4; gaps=0; marker=true; subject=c7f74691…;
  receipt after.json 13 862 B; output_directory contains /kaidoku-r40/.
  Its sha256/evidence_id are recorded in receipts/after-avm/run.json but vary with the
  random scratch name (both are hashes over parameters.output_directory), so the committed
  receipt's own run.json — not a transcript — is the digest source.
```

**b. Standard BE control** — round-37 K1 copy (sha256 `1cfb6c33…`): after arm exit 0, 5 files,
`avm_marker:false`; oracle arm exit 3 (that image is not AVM layout).

**c. Lane-built genuine AVM layout** — `gen-squashfs.py --endian avm-genuine --comp gzip|xz`:
gzip image (sha256 `c4e3e674…`) → 3 files / 6 non-regular (4 dirs, 2 symlinks), xz image 3/6,
20 000-byte multiblock image 1/1; all `crosscheck.files_equal:true`, `sasquatch_v4be` exit 0.

**d. Development vendor member (NOT V1)** —
`https://download.avm.de/fritzbox/fritzbox-7490/deutschland/fritz.os/FRITZ.Box_7490-07.62.image`,
38 092 800 B, sha256 `2ab05656563abe7fabdbbf62b3305123098b798e6f79c678f00baefc553f8ee9`; member
`./var/tmp/filesystem.image` → 35 012 616 B, sha256 `58d73b2f…474e5`, `sqsh`,
`mkfs_time == bytes_used == 35 008 578`.

```
./c1-run.sh oracle fx/dev7490-avm.squashfs out/oracle-dev7490-real
  exit 0; oracle_files=8; nonregular_entries=96 (dir 9, symlink 86, char-device 1);
  crosscheck.files_equal=true; check_files=8; check_symlinks=86;
  oracle.tsv sha256 4810291b…421cfc (701 B); nonregular.tsv sha256 e907a2b0…23206c (2 691 B);
  nonregular row: dev/led <TAB> char-device <TAB> 247:0
./c1-run.sh after fx/dev7490-avm.squashfs out/after-dev7490-keep
  exit 3; envelope ok=false, 588 B; error.code=unreadable_output,
  details.reason="Staging entry budget exceeded (10000)" (envelope digest in the receipt)
```

The after failure is REA's default-depth walk descending into the nested
`filesystem_core.squashfs` (34 422 784 B inside the member), exactly as `R40C1ReconGaps.md` §G9
measures for 7490/7430. It is recorded, not worked around: see §6.

**e. Dev manifest sample** — three development carriers, `--allow-any-ids`, reader-mode
`--layout-check reader`:

```
./mk-carriers.py --root $S --out out/carriers-dev.json --reader …/sqfs-list.py --allow-any-ids …
  exit 0; D1 58d73b2f… files=8 nonregular=96 (char-device:1, dir:9, symlink:86)
          D2 c4e3e674… files=3 nonregular=6  (dir:4, symlink:2)
          D3 c7f74691… files=4 nonregular=0
  manifest sha256 700d18c6742d0e49c14221dfd8046099ece046c8ca1de255892c7d7b6e192fb6
```

Canonical-id sample (development carriers named V1,V2,L1,L2):
`receipts/manifest-canonical-ids-dev.json`, ids emitted exactly `["V1","V2","L1","L2"]`
(oracle_files `[4,3,3,1]`), sha256 `3ea6f1251907a0b0eb0d3420766041de3d6224f237df4c23593cbd5df346f56c`.

## 6. Decisions, limits, and freeze risks

1. **REA argv is fixed** (no `--max-depth`, no `--max-output-files`): the counter's rerun clause and
   the committed receipt must be the same run shape. Consequence: a carrier whose member nests a
   large squashfs fails at the default depth 3 with the 10 000-entry staging budget (measured on
   the dev 7490 member, §5d; `R40C1ReconGaps.md` measures 7430 too). V1's member is the rootfs
   itself (697 regular files / 263 symlinks per the round-39 critic) so it should stay under the
   budget, but that is **[INFERENCE]** — it was not run here (frozen-carrier discipline). If the L1
   freezes a nested-container carrier, harness **and** counter must gain the same explicit flags in
   the same commit; do not add a flag to one side only.
2. `-no-exit-code` is added to the cross-check extractor deliberately: device nodes cannot be
   created unprivileged, and unblob passes the same flag. The regular-file cross-check — not the
   extractor exit code — is the agreement gate, so a real decompression failure still shows up as
   a file/sha mismatch (selftest `oracle-standard-be-K1`, `oracle-marker-only`).
3. **The layout gate is the reader check, not the marker.** `mk-carriers` requires the marker, but a
   marker-only standard-BE body passes that. It is rejected by `--layout-check reader` (default);
   therefore the freeze must not use `--layout-check off`.
4. `nonregular.tsv` carries every directory except the root (reader contract), so the frozen
   `gap-rule.json` needs `"dir": []` (confirmed legal with `R40C1Counter`: individual `allowed`
   values may be empty; dir rows are then inert). Kind strings pass through verbatim; the counter
   lowercases but never rewrites them, so `char-device`/`block-device` must appear identically in
   the rule.
5. `carriers.json` must hold exactly `V1,V2,L1,L2` (counter contract, enforced here), and the
   counter additionally requires ≥1 gzip-id and ≥1 xz-id carrier among them — the draft L1 gzip /
   L2 xz choice satisfies that; V1/V2 are xz (id 4).
6. The tested reader is sha256 `1079fa9b…` (final run; an earlier full run at `c06623b1…` also
   passed 111/111, and the vendor-member tables below are byte-identical under both) and was still
   being revised while this seat ran. The
   harness pins its **path and CLI contract** (`--layout`, `--files`, `--nonregular`, `--inspect`,
   exit 0/2) and records its sha256 in every `oracle-run.json`; a CLI change fails loudly with
   exit 2, not silently.
7. `test-double-sqfs-list.py` derives its tables from `sasquatch-v4be` itself, so its cross-check
   is trivially equal and proves nothing about AVM decoding. It exists only so the harness could be
   built before the reader landed; the final selftest ran against the real reader. Do not freeze it.
8. Frozen-carrier discipline observed: no REA/unblob call on V1/V2/L1/L2 or any C2 held-out
   carrier. REA/unblob ran only on: the round-37 K1 copy, the round-11 genuine AVM-BE fixture
   (copied from read-only shokuknow), lane-built `avm-genuine` images, and the 7490 07.62
   development image/member — all development inputs.

## 7. Files changed

Only `.ufo/waves/round-40/w1/artifacts/R40C1Harness/` (tools, selftest, receipts, tally) and this
report. Lane corpus/tools/plans/SKILL/README untouched; no git/jj mutation; scratch removed.
