# WSourceTextControls — text-quality probe of `check_document_spec`/`Source`

Executor seat, round 33 w1 (builder-free evidence wave). Lane `kaidoku-shokunin`,
observed at `d7076120e4f00c6d18aa77b8764d14861e820eb2`. This is scoped
text-check/instrument evidence only. It is **not** an R33-C1 measurement, not a
replacement admission benchmark, and not a revival of the stopped carrier claim
(`claim-stop.json`). No classifier was invoked, no binary fixture or manifest was
constructed or supplied, and no held/quarantined artifact was opened or used.

## Axes

| axis | move taken |
|---|---|
| depth | pinned revision, pinned driver copy, direct function call, per-check records and exact byte-level cause |
| discrimination | fabricated quote-carrying sources, explicit-denial section, vocabulary-only section, quote-line and coverage controls |
| containment | scratch-only source/JSON snapshots; lane read-only; no binary fixture, classifier, manifest or held input |
| reproducibility | argv, UTC start/end, exits, source digests, retained stdout/stderr, unified patches, tiny scratch Git snapshot with refs |

## Inputs and observed state

- Lane `HEAD` = `d7076120e4f00c6d18aa77b8764d14861e820eb2` (equals the pinned admissible
  revision); 0 tracked modifications; 7 pre-existing untracked paths (six
  `.ufo/waves/round-33/` wave files plus `w1/`). Recorded in
  `receipts/lane-observed-state.txt`. Lane was read-only; no lane/fleet Git or jj writes.
- `tools/round-33/measure_driver.py` at the pinned rev and in the worktree both hash to
  sha256 `af5d86f15c22f9d1fc148d2a6b81004eb76967d50c314c9078633bc6ccee32ac`.
- `.ufo/waves/round-33/document-spec.json` at the pinned rev and in the worktree both hash to
  sha256 `df7ea3034dd582beaf578154cb37fb1c834a748a7c19cc45de5f8595de2694a5`.
- All nine `file_sha256` pins in the spec match `.ufo/waves/round-33/source-pins.json` and the
  pinned Git blobs, 9/9 (`receipts/source-pin-verification.json`).
- Private scratch snapshot base commit `69a039d0878b59f4b5e21897ed374830f85f2253`, materialized
  as 16 files from pinned Git blobs (not a clone). Base and case refs are in
  `receipts/scratch-repo-log.txt` and `receipts/scratch-repo-refs.txt`.

## Method

The only exercised interface is the existing driver:

```python
src = md.Source(repo, rev)                # git mode: git cat-file blob <commit>:<path>
raw = src.read(".ufo/waves/round-33/document-spec.json")
md.check_document_spec(raw, spec_sha256, src)
```

`instruments/measure_driver_pinned.py` is a byte copy of the pinned driver blob
(sha256 `af5d86…`). Each run receipt records the exact argv, start/end UTC, resolved
source commit, spec digest, all 15 per-check results, `docs_ok`, failures, and exit
(probe convention: 0 = `docs_ok`, 1 = docs mismatch, 2 = refusal; no refusal occurred).
stdout/stderr are retained; stderr is empty for every run; no processes remain.

Canonical runs read the lane's Git objects at `d707612…`; adversarial runs read commits in the
private scratch repo. All fixture writes are source/JSON only and each is below 1 MiB; the
largest retained patch is 320,991 bytes.

## Run matrix

| case | source commit | `docs_ok` | checks ok/total | observed failures | exit |
|---|---|---|---|---|---|
| canonical-pinned (`d707612…`) | `d7076120e4f00c6d18aa77b8764d14861e820eb2` | false | 14/15 | `file_section` | 1 |
| canonical-scratch (materialized) | `69a039d0878b59f4b5e21897ed374830f85f2253` | false | 14/15 | `file_section` | 1 |
| A fabricated/off-topic quote sources | `8ea74f9f6f39607d56c9b57e902761cb9452cabd` | false | 12/15 | 2×`file_sha256`, `file_section` | 1 |
| B explicit-denial SKILL section | `aa6f7a5a73d2b5a4b79e11dffa6d3f800310965a` | false | 14/15 | `file_section` | 1 |
| C vocabulary-only SKILL bag | `b222fa1867507a694597acab66582b5872a449b5` | false | 14/15 | `file_section` | 1 |
| D normalization control | `89997bc452fae9a251ea4fe68277a9c1fcd40866` | true | 15/15 | none | 0 |
| E quote-line control | `807fc828f7b9912836f416e7e34519c8d0cb09f8` | false | 14/15 | `file_quote` (line 768) | 1 |
| F unpinned SKILL tail | `6cd5b33d8d0caafd70f956764cdf13ffc6e551cb` | true | 15/15 | none | 0 |

Run window: 2026-10-23T09:33:29Z through 2026-10-23T09:35:53Z (per-run start/end are in
`receipts/matrix.json`). Check-kind totals for every run: 9 `file_sha256`, 2 `file_quote`,
1 `file_section`, 3 `file_any_line`.

## Findings

### F1. The frozen canonical document spec fails its own `file_section` check at the pinned rev

Measured on both the lane's pinned Git objects and the byte-identical scratch materialization:
`docs_ok=false`, 14/15, failure `{"kind":"file_section","path":"SKILL.md","detail":"section bytes differ"}`.

The cause is a normalization asymmetry inside the existing driver, not a mismatch of the source
text. The raw SKILL.md section bytes are exactly the approved body file bytes (both sha256
`4977789211d81daba0075488d5bcde8f066a3fb9a7281bb0b61cb44e94eee946`). However:

- The observed section goes through `_section_bytes` → `_norm_body`, which strips leading and
  trailing blank lines.
- The approved file is normalized inline (`per-line rstrip`, `join`, `.rstrip() + "\n"`), which
  strips only trailing bytes and keeps leading blank lines.
- `expected-skill-body.txt` begins with exactly one blank line (byte 1 is `\n`).
- Normalized observed body: 4,868 bytes, sha256 `3750ce…`, line 0 = `Use \`python3 …`.
  Normalized approved text: 4,869 bytes, sha256 `4977789…`, line 0 = `` (empty).
  First differing normalized line: 0.

`receipts/normalization-observation.json` records the raw-section equality, both normalized
digests and the first differing line. Case D changes only that one leading blank line (and the
matching `text_file_sha256` in a scratch spec copy); every check then passes 15/15. No other byte
of SKILL.md or the approved body is changed. Case E and F also pass the section check after the
same one-byte normalization change.

Consequence: with the frozen spec as supplied, `check_document_spec` returns `docs_ok=false` on
canonical inputs. The check is fail-closed. The module docstring's wrapper mapping (`run()` would
return exit 1 when rows were evaluated but a docs check failed) is code-read, not executed here:
**INFERENCE**. This seat did not repair the predicate or the frozen artifact.

### F2. `file_quote` is line-anchored but context-blind

Case A replaced the two quote-bearing sources with off-topic bakery-ledger files:

- `corpus/evidence/round-33/sources/Object-COFF.h`: fabricated sha256
  `21ce2880f442a3d84d1dab3c35384cbc35a73e2d0b1cf39d2fcf8a6c6b43910a`, exact quote on line 768.
- `corpus/evidence/round-33/sources/pe-format.md`: fabricated sha256
  `ff61cee6396407deeb5101ae83b840c4e2b5d474bef535114198368f5611d1b7`, quote embedded inside a
  longer sentence on line 133.

Both `file_quote` checks passed (`2/2`); both `file_sha256` checks failed with the observed
digests above. This shows the quote check alone accepts fabricated context, and that the
whole-file `file_sha256` pin is what rejects it. The passing embedded line also shows the quote
test is a substring test (`quote.encode() in lines[line-1]`), not a whole-line equality test.

Case E isolates line anchoring: it mirrors the case-A fabricated files and updates the scratch
spec's `file_sha256` pins to the fabricated digests, then moves the Object-COFF.h quote from
line 768 to line 769. Result: `9/9` `file_sha256` pass, both `file_quote` paths are checked, and
exactly one failure remains: `{"kind":"file_quote","path":"corpus/evidence/round-33/sources/Object-COFF.h","detail":"quote not on line 768"}`.

### F3. `file_section` rejects explicit denial and vocabulary-only substitution

- Case B replaced the section body with an explicit denial/withdrawal (411 bytes; patch 6,073
  bytes). Result: 14/15, only `file_section` fails. All nine whole-file pins, both quotes and all
  three any-line checks pass.
- Case C replaced the body with a deterministic shuffle of the approved body's whitespace tokens:
  659 tokens on each side, token multiset identical (`token_multiset_equal=true`), bag body
  4,865 bytes. Result: 14/15, only `file_section` fails.
- `receipts/section-semantic-controls.json` compares observed and approved bodies using the
  driver's own `_norm_body` on both sides to remove the F1 asymmetry: canonical-base, case D, E
  and F compare equal; case B and case C compare unequal. So B and C are genuine content/order
  substitutions, not merely repetitions of the F1 formatting issue.

This is a frozen-byte comparison after normalization. It makes no semantic judgment and does not
attempt to parse meaning; denial text and vocabulary bags are rejected because their bytes differ,
which is the intended behavior of this interface.

### F4. `docs_ok` is pin consistency, not source authenticity

Case E shows `docs_ok` machinery operating over a scratch spec whose own `file_sha256` pins were
updated to fabricated content: all nine pins pass there. Case A shows the same fabricated files
failing when the original pins are retained. Cases D and F show `docs_ok=true` with modified
approved-body formatting and a SKILL.md tail addition. Therefore `docs_ok=true` means “the
supplied spec's pins and frozen body text are satisfied by the supplied source object”; it does
not establish that the sources are genuine, on-topic or independently authoritative. Any use of
this gate must name the frozen spec digest (`df7ea303…` for the canonical spec) as the authority.

### F5. Coverage limit: SKILL.md is guarded only by the one frozen section

The spec has no `file_sha256` check for `SKILL.md`. Case F appends a 238-byte new section at the
end of SKILL.md, outside the checked CHPE section; the result is 15/15, `docs_ok=true`, exit 0.
The file-level change is invisible to this spec. Only the exact section body is pinned.

### F6. Canonical source positives hold

At the pinned rev, all nine `file_sha256`, both `file_quote` and all three `file_any_line` checks
pass (14/15 total). The sole canonical failure is F1. The source capture, its whole-file pins,
the two located quotes and the knowledge/SOURCES/lessons line checks are intact.

## What this shows and does not show

- Shows: the existing `check_document_spec`/`Source` interfaces work as a text-consistency probe;
  whole-file pins defeat quote-carrying fakes; `file_quote` is line-located but context-blind;
  `file_section` is exact frozen bytes; the frozen canonical pair currently fails due to the F1
  normalization asymmetry; the spec does not pin all of SKILL.md.
- Does not show: any agreement of a classifier, any carrier/fixture behavior, any R33-C1 row, or
  any admission result. No binary fixture, manifest, classifier, held artifact, k01/k02/k08
  derivative, or replacement study was used. No native carrier execution or external write
  occurred.
- No repair was applied. F1 and F5 are reported for L1 to decide; the scratch spec mutations
  (cases D/E) are diagnostic controls, not proposed predicates.

## Risks, limits and dependencies

- The probe calls `check_document_spec` directly rather than the CLI `run()`; no manifest or
  classifier path is involved. Function outputs are measured; wrapper exit mapping is inference
  (stated above).
- The scratch repo is a 16-file materialization of pinned blobs, not a full clone; every check
  path is present, and canonical-pinned vs canonical-scratch agree 14/15 with the identical
  failure.
- Timestamps are system UTC observations from the receipts; no scheduling-duration claim beyond
  the recorded start/end pairs is made.
- No tool installs or updates were needed. No pacman transactions were attempted.
- This report is lane advice, not outside/non-author verification or admission.
- No missed check was silently replaced by a new predicate.

## Evidence index

Scratch root `R=/fast/scratch/hyaku/kaidoku-r33/w1/WSourceTextControls`.

| artifact | sha256 (or size) |
|---|---|
| `R/instruments/measure_driver_pinned.py` | `af5d86f15c22f9d1fc148d2a6b81004eb76967d50c314c9078633bc6ccee32ac` |
| `R/receipts/canonical-pinned.json` | `9a580860010107b572e3dbfb21706fb1289b2cf1164611bcfcd7a5ddc68bd42a` |
| `R/receipts/case-a-fabricated-quote.json` | `c8f60ca2dd7d24992f28f692d11859e8a31b53e8f83f032c7cbca262e156563e` |
| `R/receipts/case-b-explicit-denial.json` | `3910a6c9d8a527674c03912159cc1925fa90e88259d9efad8fb4cd5c6458f970` |
| `R/receipts/case-c-vocabulary-bag.json` | `30e2ff5aacffc2c6c2190fe68dd00ac83f67134921622bbaf296a992fb226bc5` |
| `R/receipts/case-d-normalization-control.json` | `a779d1612c4d8d92ca2e1a643d2b6efa784b95ec2e00f1df69fc3c258db6e4e4` |
| `R/receipts/case-e-quote-line-shift.json` | `83cc393e9e9d8ab01ab4f0b4881f6d71c5d69b52f38c69d038c03f2b167f5228` |
| `R/receipts/case-f-unpinned-skill-tail.json` | `15f21f0ea3b1ad1e03d730314106654a183ac914a2cf1b8d3ab50d0da5e3eed0` |
| `R/receipts/matrix.json` | `8c5c8d0ae260ce5aa5605e21ff3a077d6db41615d08c78d3eab38e81d451dcc1` |
| `R/receipts/normalization-observation.json` | `6b234d26e99fc268c2f6361a1d52dbdce50c14f716cad47c6364a378c497d43e` |
| `R/receipts/source-pin-verification.json` | `06a89acbd5637929444dead9e5714b45b3370f128978fb5eb6f93bd4d261dfe9` |
| `R/receipts/section-semantic-controls.json` | `872aecc868277a451eacb494e2952f70add1b00ad3d8603dc9c0b0b42098537e` |
| `R/receipts/evidence-manifest.sha256` | `336df2028da5bcc6fdf8585dda1b2e1e991e10021fb233963ae05d5eadb0c34b` |

Patches (`R/patches/`): case-a `319,029 B`, case-b `6,073 B`, case-c `10,582 B`,
case-d `1,299 B`, case-e `320,991 B`, case-f `1,089 B` (case-f is diffed against its case-D
parent). Each has a `*.stat.txt`. Raw probe argv/stdout/stderr and generation logs are under
`R/logs/`; all probe stderr files are 0 bytes. Reproduce from `R/receipts/commands.txt`.

Lane files referenced read-only: `tools/round-33/measure_driver.py`,
`.ufo/waves/round-33/document-spec.json`,
`.ufo/waves/round-33/expected-skill-body.txt`,
`.ufo/waves/round-33/source-pins.json`, `SKILL.md`, `corpus/evidence/round-33/sources/*`,
`corpus/knowledge/2026-10-23-r33-chpe-structural-profile.md`, `corpus/SOURCES.md`,
`corpus/lessons/round-33.md`.

This report is the only lane write from this seat:
`.ufo/waves/round-33/w1/WSourceTextControls.md`.
