source: `corpus/evidence/round-27/c1/table.tsv` (48 committed REA 6.5.0 envelopes in `corpus/evidence/round-27/c1/envelopes/`, call records with package version and `package.json` sha256 per call in `corpus/evidence/round-27/c1/runs.tsv`); S082 tinyxxd 1.3.17-1 package record tying the second carrier's bytes to its Arch package (opened 2026-10-22); S079 installed `rea-agents@6.5.0` package source, re-opened 2026-10-22 for `dist/ghidra/GhidraTargetSnapshot.js` (sha256 `a27e410752f5474b3a97f7388bf8fdace65d21d5dad8858ad3c27e310f03f52b`)

verified-at: 2026-10-22, round 27; 48 CLI calls 14:54:51Z–14:57:40Z by eight wave-1 seats (`.ufo/waves/round-27/w1/Run*.md`), package root `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents/` (version 6.5.0, `package.json` sha256 `a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c`, read after every call)

recheck: `python3 -I -B tools/round-27/c1-rename-identity.py --root <LANE> --rev <REV>` re-derives each verdict from the committed envelopes offline (the counter was committed at `a4f674b343d8564e21f7eb8984630a95089c82d6`, before the runs). A live recheck copies the carrier to a path whose file name ends in a different extension (for example `.dat`), checks both sha256 values, and runs `analyze` on both.

# A renamed copy changes the `analyze`, `inspect` and `inspect-binary-layout` evidence ids at REA 6.5.0; five address verbs keep theirs — the file extension enters the id through the Ghidra program name

Coverage-map ground: evidence-ID identity per verb at the lane's carrier pin, extended from a
directory-only copy (round 26, `corpus/knowledge/2026-10-22-r26-native-reader-evidence-id-identity.md`)
to a copy with another directory, file name and extension, and to a second carrier.

## What was run

Eight verbs on two carriers, three runs each: `base` and same-path `repeat` on the `/usr/bin` path,
then `renamed` on a byte-identical copy under another directory, file name and extension.

| carrier | sha256 | base path | renamed path | address |
|---|---|---|---|---|
| jq 1.8.2-1 | `e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806` | `/usr/bin/jq` | `/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/jq-r27-renamed.dat` | `0x103fa0` (a function start, not the entry) |
| tinyxxd 1.3.17-1 (S082) | `7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65` | `/usr/bin/tinyxxd` | `/fast/scratch/hyaku/kaidoku-r27/carrier/renamed/tinyxxd-r27-renamed.dat` | `0x103d40` (ELF entry `0x3d40` at image base `0x100000`) |

## Result (`corpus/evidence/round-27/c1/table.tsv`)

| verb | jq | tinyxxd |
|---|---|---|
| analyze | rename-sensitive | rename-sensitive |
| inspect | rename-sensitive | rename-sensitive |
| inspect-binary-layout | rename-sensitive | rename-sensitive |
| decompile | content-keyed | content-keyed |
| xrefs | content-keyed | content-keyed |
| read-bytes | content-keyed | content-keyed |
| function | content-keyed | content-keyed |
| instructions | content-keyed | content-keyed |

Base and repeat ids are equal in all 16 pairs, so no pair is `unstable` on these carriers.
`analyze` and `inspect` give the same id on each path (jq base `ev_14f9d92f…d328`, renamed
`ev_a60580a9…3cd2`; tinyxxd base `ev_89338dd2…479b`, renamed `ev_65e0dbfb…7efb`).

## Why (observed in the 6.5.0 code and the envelopes)

- `analyze` and `inspect`: the only hashed leaf that differs between base and renamed is
  `.data.normalized_result.document`: `target-e815667571d0.bin` against `target-e815667571d0.dat`
  (jq), `target-7b1e5d0c970a.bin` against `target-7b1e5d0c970a.dat` (tinyxxd). REA copies the
  target to a snapshot named `target-<first 12 hex of sha256><suffix>` before Ghidra imports it,
  and the suffix is the caller's extension when it matches `^\.[A-Za-z0-9]{1,12}$`, else `.bin`
  (`dist/ghidra/GhidraTargetSnapshot.js:13-14` and `:76-78`, S079 family). The Ghidra program
  name is that snapshot name, and `binary_overview` reports it as `document`. The directory and
  the rest of the file name never enter the id: `subject.name` and `subject.local_path` are
  outside the projection (`dist/domain/evidence.js:156-182`).
- `inspect-binary-layout`: the run path itself is hashed, in `parameters.path`,
  `normalized_result.artifact.path` and `locations[0].path` (as round 26 found for a
  directory-only copy).
- The five address verbs: no hashed field differs between base and renamed on either carrier;
  only `subject.name`, `subject.local_path` and `meta.duration` differ.

The wave-1 scout `PredictWholeFile` predicted the three rename-sensitive verbs from the code
before reading any round-27 envelope, and its counterfactual (changing only `document` from
`.bin` to `.dat` in the round-26 `analyze` envelope and recomputing under the 6.5.0 rule) gives
`ev_a60580a9d89e287b2be3be092b710a1b08d55a7583c5d66d66833f31a9f53cd2`, the id the renamed jq run
then returned (`.ufo/waves/round-27/w1/PredictWholeFile.md`). The scout `PredictAddressVerbs`
predicted the five address verbs content-keyed from the same code, also without reading any
round-27 envelope (`.ufo/waves/round-27/w1/PredictAddressVerbs.md`): 8 of 8 verb predictions
matched the table.

## Decision rule

| You compare ids of the same bytes at two paths, at REA 6.5.0 | Then |
|---|---|
| `decompile`, `xrefs`, `read-bytes`, `function`, `instructions` | equal ids are expected whatever the path, name or extension; a difference means different bytes, address, parameters or pin |
| `analyze` or `inspect`, both paths have no extension or an extension outside `^\.[A-Za-z0-9]{1,12}$` (both become `.bin`), or the same extension | equal ids are expected |
| `analyze` or `inspect`, the extensions differ after that mapping | the ids differ; this is not a content change — compare `subject.digest.sha256` instead |
| `inspect-binary-layout` | the ids differ whenever the path string differs; never use its id as a content key |

This narrows the round-26 entry's "seven content-keyed verbs": `analyze` and `inspect` are
content-keyed across directories only while the extension class stays the same.

## Limits

- The renamed copy changes directory, file name and extension together. That only the
  extension matters for `analyze` and `inspect` rests on the code path above and the
  counterfactual recompute, not on a separate extension-only or name-only run.
- Two carriers, one pin, one address per carrier, three runs per pair. Nothing here covers 6.7.0
  runs, MCP sessions, other parameters, or error envelopes.
- The pin rests on the frozen invocation (`npx -y rea-agents@6.5.0`) and the per-call read of the
  6.5.0 `package.json`; the envelopes carry no version. All 48 ids recompute under the 6.5.0 rule
  (`tools/round-26/recompute-ids.py`).
- Counter result at the data commit `9dca26df135a2c558aaa575534ad42662b372d5d`: 15 of 16 rows
  complete. The tinyxxd `inspect-binary-layout` base and repeat runs (14:55:49Z and 14:55:50Z,
  separate output files) produced byte-identical envelopes (both `meta.duration` `132ms`), and the
  frozen counter refuses any envelope sha256 shared by two runs. Its verdict (rename-sensitive) is
  still derivable from the three ids; see `corpus/lessons/round-27.md` for the counter defect.
